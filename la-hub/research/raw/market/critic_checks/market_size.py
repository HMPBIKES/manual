#!/usr/bin/env python3
"""
LA delivery-courier market size model (Task 1).

Three routes to the same quantity (daily-active app-based food couriers), each with
its own inputs, so they can be cross-checked instead of tuned to agree, plus a fourth
route that uses HMP's own SF numbers to size what HMP can address:

  M1  restaurant-ratio   riders = restaurants x NYC weekly-active per restaurant x LA/NYC order
                         intensity x (NYC / LA deliveries per courier-week) x daily/weekly
  M2  order-volume       riders = US deliveries/day x LA County share / orders per courier-day
  M3  top-down supply    riders = CA quarter-active app workers x LA share x delivery share
                         x quarterly->weekly x weekly->daily
  M4  SF-calibrated      HMP-addressable customers within 3 mi = HMP SF active customers per SF
                         restaurant x LA restaurants x mode ratio x maturity x reachability

Every parameter lives in market_size_params.json with (lo, base, hi) and a tag:
  FACT / ESTIMATE / ASSUMPTION  (see _readme in that file).
Run:  python3 market_size.py            -> scenario tables
      python3 market_size.py --mc 20000 -> adds Monte Carlo P10/P50/P90 (triangular, independent)
      python3 market_size.py --json     -> machine-readable
"""
import argparse
import json
import math
import random
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARAMS_FILE = HERE / "market_size_params.json"
SCENARIOS = ("conservative", "base", "aggressive")


@dataclass
class P:
    lo: float
    base: float
    hi: float
    tag: str = "ASSUMPTION"
    note: str = ""

    def pick(self, s: str) -> float:
        return {"conservative": self.lo, "base": self.base, "aggressive": self.hi}[s]

    def sample(self) -> float:
        a, b = min(self.lo, self.hi), max(self.lo, self.hi)
        if a == b:
            return a
        return random.triangular(a, b, self.base)


def load_params() -> dict:
    raw = json.loads(PARAMS_FILE.read_text())
    return {k: P(v["lo"], v["base"], v["hi"], v.get("tag", "ASSUMPTION"), v.get("note", ""))
            for k, v in raw.items() if not k.startswith("_")}


def compute(p: dict, pick) -> dict:
    g = lambda k: pick(p[k])
    r = {}

    # ---------- denominators (FACT) ----------
    rest = {
        "zone": g("restaurants_target_zone"),
        "r1_5": g("restaurants_radius_1_5mi"),
        "r3": g("restaurants_radius_3mi"),
        "city": g("restaurants_city_la"),
        "county": g("restaurants_county_la"),
    }
    zone_int = g("zone_order_intensity_vs_county")
    intensity = {"zone": zone_int, "r1_5": zone_int, "r3": zone_int, "city": 1.0, "county": 1.0}
    w2d = g("weekly_to_daily_active")

    # ---------- M1 restaurant ratio (daily-active) ----------
    cpr_weekly_nyc = g("nyc_weekly_active_couriers") / g("nyc_restaurants")
    cpr_weekly_la = (cpr_weekly_nyc * g("la_orders_per_restaurant_vs_nyc")
                     * g("nyc_deliveries_per_courier_week") / g("la_deliveries_per_courier_week"))
    for geo in rest:
        r[f"M1_{geo}"] = rest[geo] * cpr_weekly_la * intensity[geo] * w2d

    # ---------- M2 order volume (daily-active) ----------
    us_orders_day = g("doordash_us_deliveries_per_day") / g("doordash_us_share")
    county_orders_day = us_orders_day * g("la_county_share_us_orders")
    opd = g("orders_per_courier_day")
    r["county_orders_per_day"] = county_orders_day
    for geo in rest:
        r[f"M2_{geo}"] = county_orders_day * (rest[geo] / rest["county"]) * intensity[geo] / opd

    # ---------- M3 top-down supply (daily-active) ----------
    county_weekly = (g("ca_app_based_workers_quarter_active") * g("la_county_share_ca_gig")
                     * g("delivery_share_of_app_workers") * g("quarterly_to_weekly_active"))
    r["M3_county_weekly_active"] = county_weekly
    for geo in rest:
        r[f"M3_{geo}"] = county_weekly * w2d * (rest[geo] / rest["county"]) * intensity[geo]

    # ---------- cross-check: geometric mean + spread ----------
    for geo in rest:
        vals = [r[f"M{i}_{geo}"] for i in (1, 2, 3)]
        r[f"DAILY_{geo}"] = math.exp(sum(math.log(v) for v in vals) / 3)
        r[f"WEEKLY_{geo}"] = r[f"DAILY_{geo}"] / w2d          # people active in a typical week
        r[f"SPREAD_{geo}"] = max(vals) / min(vals)

    # ---------- mode split ----------
    tw_deliv = g("la_two_wheel_delivery_share")
    tw_courier_la = tw_deliv * g("two_wheel_delivery_to_courier_share")
    tw_zone = min(0.90, tw_courier_la * g("zone_two_wheel_uplift"))
    r["two_wheel_courier_share_la"] = tw_courier_la
    r["two_wheel_courier_share_zone"] = tw_zone
    e_share = g("ebike_emoped_share_of_two_wheel")
    gas_share = g("gas_scooter_share_of_two_wheel")
    ped_share = max(0.0, 1 - e_share - gas_share)
    for geo in ("zone", "r3"):
        d = r[f"DAILY_{geo}"]
        r[f"DAILY_{geo}_car"] = d * (1 - tw_zone)
        r[f"DAILY_{geo}_two_wheel"] = d * tw_zone
        r[f"DAILY_{geo}_ebike_emoped"] = d * tw_zone * e_share
        r[f"DAILY_{geo}_gas_scooter_moto"] = d * tw_zone * gas_share
        r[f"DAILY_{geo}_pedal_bicycle"] = d * tw_zone * ped_share
    r["DAILY_county_two_wheel"] = r["DAILY_county"] * tw_courier_la
    r["DAILY_city_two_wheel"] = r["DAILY_city"] * tw_courier_la


    # ---------- M5 DoorDash two-wheel miles (independent check on the two-wheel count) ----------
    m5_county_tw = (g("la_two_wheel_miles_per_day_doordash") * g("county_share_of_doordash_label_miles")
                    / g("miles_per_two_wheel_courier_day") / g("doordash_share_of_two_wheel_couriers_la")
                    * g("nyc_miles_calibration"))
    r["M5_county_two_wheel_daily"] = m5_county_tw
    r["M5_vs_M123_county_two_wheel"] = m5_county_tw / r["DAILY_county_two_wheel"]
    # allocate to zone: restaurant share x intensity x (zone uplift relative to LA-wide share)
    r["M5_zone_two_wheel_daily"] = (m5_county_tw * (rest["zone"] / rest["county"]) * zone_int
                                    * (tw_zone / tw_courier_la))
    r["M5_r3_two_wheel_daily"] = (m5_county_tw * (rest["r3"] / rest["county"]) * zone_int
                                  * (tw_zone / tw_courier_la))
    # blended two-wheel count for the zone: geometric mean of the M1-3 route and the M5 route
    for geo in ("zone", "r3"):
        a, b = r[f"DAILY_{geo}_two_wheel"], r[f"M5_{geo}_two_wheel_daily"]
        r[f"BLEND_{geo}_two_wheel_daily"] = math.sqrt(a * b)
        r[f"BLEND_{geo}_two_wheel_weekly_people"] = r[f"BLEND_{geo}_two_wheel_daily"] / w2d
        r[f"BLEND_{geo}_ebike_emoped_daily"] = r[f"BLEND_{geo}_two_wheel_daily"] * e_share

    # ---------- TAM / SAM / SOM (people = weekly-active) ----------
    tam_people = r["WEEKLY_zone"]
    tw_people = r["BLEND_zone_two_wheel_weekly_people"]
    r["TAM_people_zone_all_modes"] = tam_people
    r["TAM_people_zone_two_wheel"] = tw_people
    r["TAM_people_zone_ebike_emoped"] = tw_people * e_share
    reach = g("reachable_share_768ceres")
    sam = (tw_people * g("two_wheel_serviceable_share")
           + max(0.0, tam_people - tw_people) * g("car_convertible_share")) * reach
    r["SAM_people_hub"] = sam
    r["SOM_people_m12"] = sam * g("penetration_m12")
    r["SOM_people_m24"] = sam * g("penetration_m24")

    # ---------- M4 SF-calibrated (HMP's own numbers) ----------
    pen_per_rest = g("hmp_sf_active_customers") / g("restaurants_sf_city")
    r["M4_hmp_customers_r3_m24"] = (pen_per_rest * rest["r3"] * (tw_zone / g("sf_two_wheel_courier_share"))
                                    * g("la_maturity_vs_sf_at_m24") * reach)
    r["M4_vs_SOM_m24_ratio"] = r["M4_hmp_customers_r3_m24"] / r["SOM_people_m24"]
    return r


def fmt(x):
    if isinstance(x, float):
        return f"{x:.2f}" if abs(x) < 2 else f"{x:,.0f}"
    return str(x)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mc", type=int, default=0)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    p = load_params()
    scen = {s: compute(p, lambda q, s=s: q.pick(s)) for s in SCENARIOS}
    keys = list(scen["base"].keys())
    out = {"scenarios": scen}
    if args.mc:
        random.seed(7)
        draws = {k: [] for k in keys}
        for _ in range(args.mc):
            res = compute(p, lambda q: q.sample())
            for k in keys:
                draws[k].append(res[k])
        mc = {}
        for k in keys:
            v = sorted(draws[k])
            n = len(v)
            mc[k] = {"p10": v[int(n * 0.1)], "p50": v[int(n * 0.5)], "p90": v[int(n * 0.9)]}
        out["monte_carlo"] = mc
    if args.json:
        print(json.dumps(out, indent=1))
        return
    print(f"{'metric':36s} {'conservative':>13s} {'base':>13s} {'aggressive':>13s}", end="")
    if args.mc:
        print(f" | {'MC P10':>10s} {'MC P50':>10s} {'MC P90':>10s}")
    else:
        print()
    for k in keys:
        line = f"{k:36s} {fmt(scen['conservative'][k]):>13s} {fmt(scen['base'][k]):>13s} {fmt(scen['aggressive'][k]):>13s}"
        if args.mc:
            m = out["monte_carlo"][k]
            line += f" | {fmt(m['p10']):>10s} {fmt(m['p50']):>10s} {fmt(m['p90']):>10s}"
        print(line)


if __name__ == "__main__":
    main()
