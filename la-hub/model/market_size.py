#!/usr/bin/env python3
"""
LA delivery-courier market size model (Task 1).

Four routes to the same quantity (daily-active app-based food couriers), each with
its own inputs, so they can be cross-checked instead of tuned to agree:

  M1  restaurant-ratio      riders = restaurants_zone x couriers_per_restaurant (benchmark) x LA adj.
  M2  order-volume          riders = (US orders/day x LA share x zone share) / orders per courier-day
  M3  top-down supply       riders = CA app workers x LA share x delivery share x daily-active share x zone share
  M4  SF-calibrated (HMP)   riders_addressable = HMP SF active customers per SF restaurant x LA restaurants x mode adj.

Every parameter carries a (conservative, base, aggressive) triple and a tag:
  FACT      public, verified, cited in la-hub/research/03-market-size.md
  ESTIMATE  derived from several sources, range given
  ASSUMPTION no direct evidence; must be replaced with HMP data or field tests
Run:  python3 market_size.py            -> prints scenario tables
      python3 market_size.py --mc 20000 -> adds a Monte Carlo P10/P50/P90 band
"""
import argparse
import json
import math
import random
import sys
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARAMS_FILE = HERE / "market_size_params.json"


@dataclass
class P:
    """A parameter with conservative / base / aggressive values."""
    lo: float
    base: float
    hi: float
    tag: str = "ASSUMPTION"
    note: str = ""

    def pick(self, s: str) -> float:
        return {"conservative": self.lo, "base": self.base, "aggressive": self.hi}[s]

    def sample(self) -> float:
        # triangular between lo and hi with mode at base; lo/hi are ordered by outcome
        a, b = min(self.lo, self.hi), max(self.lo, self.hi)
        return random.triangular(a, b, self.base)


def load_params() -> dict:
    raw = json.loads(PARAMS_FILE.read_text())
    out = {}
    for k, v in raw.items():
        if k.startswith("_"):
            continue
        out[k] = P(v["lo"], v["base"], v["hi"], v.get("tag", "ASSUMPTION"), v.get("note", ""))
    return out


def compute(p: dict, pick) -> dict:
    """pick: function P -> float (scenario pick or MC sample)."""
    g = lambda k: pick(p[k])
    r = {}

    # ---------- denominators (FACT from geodata) ----------
    rest_zone = g("restaurants_target_zone")          # DTLA + Ktown + Westlake + Pico-Union + USC
    rest_r3 = g("restaurants_radius_3mi")
    rest_city = g("restaurants_city_la")
    rest_county = g("restaurants_county_la")
    rest_sf_core = g("restaurants_sf_core")
    rest_sf_city = g("restaurants_sf_city")

    # ---------- M1 restaurant ratio ----------
    # couriers_per_restaurant benchmark: NYC weekly-active / NYC restaurants, converted to daily-active,
    # then scaled by LA's lower app-order intensity per restaurant.
    cpr_nyc_weekly = g("nyc_weekly_active_couriers") / g("nyc_restaurants")
    cpr_daily = cpr_nyc_weekly * g("weekly_to_daily_active")
    la_intensity = g("la_orders_per_restaurant_vs_nyc")   # <1: LA restaurants generate fewer app orders each
    r["M1_zone"] = rest_zone * cpr_daily * la_intensity
    r["M1_r3"] = rest_r3 * cpr_daily * la_intensity
    r["M1_city"] = rest_city * cpr_daily * la_intensity
    r["M1_county"] = rest_county * cpr_daily * la_intensity

    # ---------- M2 order volume ----------
    us_orders_day = g("us_delivery_orders_per_day")       # all platforms, US
    la_county_share = g("la_county_share_us_orders")      # LA County share of US orders
    opd = g("orders_per_courier_day")                     # daily-active courier productivity
    county_orders = us_orders_day * la_county_share
    r["M2_county"] = county_orders / opd
    r["M2_city"] = r["M2_county"] * (rest_city / rest_county)
    r["M2_zone"] = r["M2_county"] * (rest_zone / rest_county) * g("zone_order_intensity_vs_county")
    r["M2_r3"] = r["M2_county"] * (rest_r3 / rest_county) * g("zone_order_intensity_vs_county")

    # ---------- M3 top-down supply ----------
    ca_workers = g("ca_app_based_workers_annual")
    r["M3_county"] = (ca_workers * g("la_county_share_ca_gig") * g("delivery_share_of_app_workers")
                      * g("annual_to_daily_active"))
    r["M3_city"] = r["M3_county"] * (rest_city / rest_county)
    r["M3_zone"] = r["M3_county"] * (rest_zone / rest_county) * g("zone_order_intensity_vs_county")
    r["M3_r3"] = r["M3_county"] * (rest_r3 / rest_county) * g("zone_order_intensity_vs_county")

    # ---------- mode split (applied to zone/r3) ----------
    two_wheel = g("la_two_wheel_share")                   # share of deliveries on two wheels (all zones)
    zone_uplift = g("zone_two_wheel_uplift")              # dense zones above LA average
    tw_zone = min(0.95, two_wheel * zone_uplift)
    r["two_wheel_share_zone"] = tw_zone
    # within two-wheel: e-bike / e-moped vs gas scooter-motorcycle vs pedal bicycle
    r["ebike_emoped_share_of_two_wheel"] = g("ebike_emoped_share_of_two_wheel")
    r["gas_share_of_two_wheel"] = g("gas_scooter_share_of_two_wheel")
    r["bicycle_share_of_two_wheel"] = max(0.0, 1 - r["ebike_emoped_share_of_two_wheel"] - r["gas_share_of_two_wheel"])

    # ---------- combine M1-M3 (geometric mean = cross-check, not average) ----------
    for geo in ("county", "city", "zone", "r3"):
        vals = [r[f"M{i}_{geo}"] for i in (1, 2, 3)]
        r[f"ALL_{geo}"] = math.exp(sum(math.log(v) for v in vals) / len(vals))
        r[f"SPREAD_{geo}"] = max(vals) / min(vals)

    # ---------- TAM / SAM / SOM for the hub ----------
    tam_zone = r["ALL_zone"]
    r["TAM_zone_all_modes"] = tam_zone
    r["TAM_zone_two_wheel"] = tam_zone * tw_zone
    r["TAM_zone_ebike_emoped"] = r["TAM_zone_two_wheel"] * r["ebike_emoped_share_of_two_wheel"]
    car_convertible = tam_zone * (1 - tw_zone) * g("car_convertible_share")
    reachable = g("reachable_share_768ceres")
    r["SAM_hub"] = (r["TAM_zone_two_wheel"] * g("two_wheel_serviceable_share") + car_convertible) * reachable
    r["SOM_m12"] = r["SAM_hub"] * g("penetration_m12")
    r["SOM_m24"] = r["SAM_hub"] * g("penetration_m24")

    # ---------- M4 SF-calibrated (HMP's own numbers) ----------
    hmp_active_sf = g("hmp_sf_active_customers")
    # per-restaurant penetration, using SF citywide restaurants (customers come from all over SF)
    pen_per_rest = hmp_active_sf / rest_sf_city
    mode_ratio = tw_zone / g("sf_two_wheel_share")
    maturity = g("la_maturity_vs_sf_at_m24")            # LA at M24 vs SF at ~25 months
    r["M4_hmp_addressable_m24"] = pen_per_rest * rest_r3 * mode_ratio * maturity * reachable
    return r


def fmt(x):
    if isinstance(x, float):
        if abs(x) < 2:
            return f"{x:.2f}"
        return f"{x:,.0f}"
    return str(x)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mc", type=int, default=0, help="Monte Carlo draws (0 = off)")
    ap.add_argument("--json", action="store_true", help="dump results as JSON")
    args = ap.parse_args()
    p = load_params()
    scen = {s: compute(p, lambda q, s=s: q.pick(s)) for s in ("conservative", "base", "aggressive")}
    keys = list(scen["base"].keys())
    if args.json:
        print(json.dumps(scen, indent=1))
        return
    print(f"{'metric':38s} {'conservative':>14s} {'base':>14s} {'aggressive':>14s}")
    for k in keys:
        print(f"{k:38s} {fmt(scen['conservative'][k]):>14s} {fmt(scen['base'][k]):>14s} {fmt(scen['aggressive'][k]):>14s}")
    if args.mc:
        random.seed(7)
        draws = {k: [] for k in keys}
        for _ in range(args.mc):
            res = compute(p, lambda q: q.sample())
            for k in keys:
                draws[k].append(res[k])
        print("\nMonte Carlo (triangular on every parameter, independent):")
        print(f"{'metric':38s} {'P10':>12s} {'P50':>12s} {'P90':>12s}")
        for k in keys:
            v = sorted(draws[k])
            n = len(v)
            print(f"{k:38s} {fmt(v[int(n*0.1)]):>12s} {fmt(v[int(n*0.5)]):>12s} {fmt(v[int(n*0.9)]):>12s}")


if __name__ == "__main__":
    main()
