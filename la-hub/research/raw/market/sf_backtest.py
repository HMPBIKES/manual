#!/usr/bin/env python3
"""SF back-test of the LA market-size model (same route logic, SF inputs).
Run from /home/user/manual/la-hub/model so market_size.py is importable."""
import json, math, random, sys
sys.path.insert(0, "/home/user/manual/la-hub/model")
import market_size as ms

P = ms.P
la_params = ms.load_params()
SC = ms.SCENARIOS

# ---------------- SF parameters (lo = fewer riders, base, hi = more riders) ----------------
sf = {
    # FACT denominators
    "rest_city": P(4514, 4514, 4514, "FACT"),
    "rest_r3": P(3458, 3458, 3458, "FACT"),      # 3 mi around 261 6th St
    "rest_core": P(1628, 1628, 1628, "FACT"),
    "pop_city": P(836321, 836321, 836321, "FACT"),
    "pop_r3": P(437238, 437238, 437238, "FACT"),
    # shared with LA model (identical values)
    "nyc_weekly_active_couriers": la_params["nyc_weekly_active_couriers"],
    "nyc_restaurants": la_params["nyc_restaurants"],
    "nyc_deliveries_per_courier_week": la_params["nyc_deliveries_per_courier_week"],
    "doordash_us_deliveries_per_day": la_params["doordash_us_deliveries_per_day"],
    "doordash_us_share": la_params["doordash_us_share"],
    "ca_app_based_workers_quarter_active": la_params["ca_app_based_workers_quarter_active"],
    "delivery_share_of_app_workers": la_params["delivery_share_of_app_workers"],
    "quarterly_to_weekly_active": la_params["quarterly_to_weekly_active"],
    "two_wheel_delivery_to_courier_share": la_params["two_wheel_delivery_to_courier_share"],
    "doordash_share_of_two_wheel_couriers": la_params["doordash_share_of_two_wheel_couriers_la"],
    "nyc_miles_calibration": la_params["nyc_miles_calibration"],
    # SF-specific
    # SF per-capita delivery intensity vs NYC 0.7/0.85/1.0 (Seattle 0.25 offers/resident-wk vs NYC 0.32),
    # divided by SF/NYC restaurants-per-capita ratio (5.40 vs 2.71 per 1,000 = 1.99) -> per-restaurant
    "sf_orders_per_restaurant_vs_nyc": P(0.35, 0.43, 0.50, "ESTIMATE"),
    # more career/two-wheel riders than LA (LA model 28/22/17); NYC 39-45, Seattle 12.7
    "sf_deliveries_per_courier_week": P(32, 25, 19, "ESTIMATE"),
    # more full-timers than LA (LA 0.3/0.4/0.5)
    "weekly_to_daily_active": P(0.35, 0.45, 0.55, "ESTIMATE"),
    # r3 holds 77% of SF restaurants; downtown/SoMa/Mission core
    "r3_order_intensity_vs_city": P(1.0, 1.1, 1.2, "ASSUMPTION"),
    # SF County share of US orders = pop share 0.246% x intensity vs US avg 1.8/2.3/2.8 (NYC ~3.0x, Seattle ~2.3x)
    "sf_share_us_orders": P(0.00246 * 1.8, 0.00246 * 2.3, 0.00246 * 2.8, "ESTIMATE"),
    # LA model 12/9/7; two-wheel riders do more per hour but SF has many casual riders too
    "orders_per_courier_day": P(11, 8.5, 6.5, "ESTIMATE"),
    # SF share of CA quarter-active app workers: pop 2.11%, NAICS 492 nonemployers 1.86%, NAICS 722 employment 3.8%
    "sf_share_ca_gig": P(0.019, 0.023, 0.028, "ESTIMATE"),
    # DoorDash SF 72%; Uber Eats unknown; hi = Santa Clara/Sunnyvale 75%
    "sf_two_wheel_delivery_share": P(0.65, 0.72, 0.75, "FACT"),
    "r3_two_wheel_uplift": P(1.0, 1.05, 1.10, "ASSUMPTION"),
    "sf_two_wheel_miles_per_day_doordash": P(21413128 / 61, 21413128 / 61, 21413128 / 61, "FACT"),
    # SF label = city & county; lo allows label to include Daly City/South SF
    "city_share_of_label_miles": P(0.85, 1.0, 1.0, "ASSUMPTION"),
    # compact 7x7 city, shorter legs than LA (LA 80/60/45)
    "miles_per_two_wheel_courier_day": P(70, 52, 40, "ESTIMATE"),
    "hmp_sf_active_customers": la_params["hmp_sf_active_customers"],
}


def compute_sf(p, pick):
    g = lambda k: pick(p[k])
    r = {}
    rest = {"city": g("rest_city"), "r3": g("rest_r3"), "core": g("rest_core")}
    inten = {"city": 1.0, "r3": g("r3_order_intensity_vs_city"), "core": g("r3_order_intensity_vs_city") * 1.1}
    w2d = g("weekly_to_daily_active")

    # M1 restaurant ratio
    cpr_nyc = g("nyc_weekly_active_couriers") / g("nyc_restaurants")
    cpr_sf = cpr_nyc * g("sf_orders_per_restaurant_vs_nyc") * g("nyc_deliveries_per_courier_week") / g("sf_deliveries_per_courier_week")
    for geo in rest:
        r[f"M1_{geo}"] = rest[geo] * cpr_sf * inten[geo] * w2d

    # M2 order volume
    us_orders = g("doordash_us_deliveries_per_day") / g("doordash_us_share")
    sf_orders = us_orders * g("sf_share_us_orders")
    r["sf_orders_per_day"] = sf_orders
    r["sf_orders_per_resident_week"] = sf_orders * 7 / g("pop_city")
    for geo in rest:
        r[f"M2_{geo}"] = sf_orders * (rest[geo] / rest["city"]) * inten[geo] / g("orders_per_courier_day")

    # M3 top-down supply
    sf_weekly = g("ca_app_based_workers_quarter_active") * g("sf_share_ca_gig") * g("delivery_share_of_app_workers") * g("quarterly_to_weekly_active")
    r["M3_city_weekly_active"] = sf_weekly
    for geo in rest:
        r[f"M3_{geo}"] = sf_weekly * w2d * (rest[geo] / rest["city"]) * inten[geo]

    for geo in rest:
        vals = [r[f"M{i}_{geo}"] for i in (1, 2, 3)]
        r[f"DAILY_{geo}"] = math.exp(sum(math.log(v) for v in vals) / 3)
        r[f"WEEKLY_{geo}"] = r[f"DAILY_{geo}"] / w2d
        r[f"SPREAD_{geo}"] = max(vals) / min(vals)

    # mode split
    tw_city = g("sf_two_wheel_delivery_share") * g("two_wheel_delivery_to_courier_share")
    tw_r3 = min(0.90, tw_city * g("r3_two_wheel_uplift"))
    r["two_wheel_courier_share_city"] = tw_city
    r["two_wheel_courier_share_r3"] = tw_r3
    r["DAILY_city_two_wheel"] = r["DAILY_city"] * tw_city
    r["DAILY_r3_two_wheel"] = r["DAILY_r3"] * tw_r3
    r["DAILY_core_two_wheel"] = r["DAILY_core"] * tw_r3

    # M5 DoorDash two-wheel miles (same construction as LA)
    m5_city = (g("sf_two_wheel_miles_per_day_doordash") * g("city_share_of_label_miles")
               / g("miles_per_two_wheel_courier_day") / g("doordash_share_of_two_wheel_couriers")
               * g("nyc_miles_calibration"))
    r["M5_city_two_wheel_daily"] = m5_city
    r["M5_vs_M123_city_two_wheel"] = m5_city / r["DAILY_city_two_wheel"]
    r["M5_r3_two_wheel_daily"] = m5_city * (rest["r3"] / rest["city"]) * inten["r3"] * (tw_r3 / tw_city)
    # uncalibrated M5 (what the miles say with no NYC fudge)
    r["M5_city_two_wheel_daily_uncal"] = m5_city / g("nyc_miles_calibration")
    # implied DoorDash two-wheel miles per DoorDash two-wheel delivery under M2's order volume
    dd_tw_deliv = sf_orders * g("doordash_us_share") * g("sf_two_wheel_delivery_share")
    r["implied_dd_miles_per_two_wheel_delivery"] = g("sf_two_wheel_miles_per_day_doordash") / dd_tw_deliv

    for geo in ("city", "r3"):
        a, b = r[f"DAILY_{geo}_two_wheel"], r[f"M5_{geo}_two_wheel_daily"]
        r[f"BLEND_{geo}_two_wheel_daily"] = math.sqrt(a * b)
        r[f"BLEND_{geo}_two_wheel_weekly_people"] = r[f"BLEND_{geo}_two_wheel_daily"] / w2d
        r[f"M123_{geo}_two_wheel_weekly_people"] = a / w2d
        r[f"M5_{geo}_two_wheel_weekly_people"] = b / w2d

    # HMP penetration (against city pool and r3 pool)
    hmp = g("hmp_sf_active_customers")
    r["HMP_pen_city_two_wheel_weekly_blend"] = hmp / r["BLEND_city_two_wheel_weekly_people"]
    r["HMP_pen_city_two_wheel_weekly_M123"] = hmp / r["M123_city_two_wheel_weekly_people"]
    r["HMP_pen_city_two_wheel_weekly_M5"] = hmp / r["M5_city_two_wheel_weekly_people"]
    r["HMP_pen_r3_two_wheel_weekly_blend"] = hmp / r["BLEND_r3_two_wheel_weekly_people"]
    r["HMP_pen_city_all_modes_weekly"] = hmp / r["WEEKLY_city"]
    return r


def run(params, fn, mc=20000):
    scen = {s: fn(params, lambda q, s=s: q.pick(s)) for s in SC}
    keys = list(scen["base"].keys())
    random.seed(7)
    draws = {k: [] for k in keys}
    for _ in range(mc):
        res = fn(params, lambda q: q.sample())
        for k in keys:
            draws[k].append(res[k])
    mcq = {}
    for k in keys:
        v = sorted(draws[k]); n = len(v)
        mcq[k] = {"p10": v[int(n * .1)], "p50": v[int(n * .5)], "p90": v[int(n * .9)]}
    return scen, mcq


def fmt(x):
    return f"{x:.3f}" if abs(x) < 2 else f"{x:,.0f}"


if __name__ == "__main__":
    sf_scen, sf_mc = run(sf, compute_sf)
    la_scen, la_mc = run(la_params, ms.compute)
    print(f"{'SF metric':44s} {'cons':>10s} {'base':>10s} {'aggr':>10s} | {'P10':>9s} {'P50':>9s} {'P90':>9s}")
    for k in sf_scen["base"]:
        m = sf_mc[k]
        print(f"{k:44s} {fmt(sf_scen['conservative'][k]):>10s} {fmt(sf_scen['base'][k]):>10s} {fmt(sf_scen['aggressive'][k]):>10s} | {fmt(m['p10']):>9s} {fmt(m['p50']):>9s} {fmt(m['p90']):>9s}")

    print("\n---- LA/SF ratios (base / MC P50) ----")
    def ratio(la_k, sf_k):
        return {s: la_scen[s][la_k] / sf_scen[s][sf_k] for s in SC} | {"p50": la_mc[la_k]["p50"] / sf_mc[sf_k]["p50"]}
    for la_k, sf_k in [("BLEND_r3_two_wheel_daily", "BLEND_r3_two_wheel_daily"),
                       ("DAILY_r3_two_wheel", "DAILY_r3_two_wheel"),
                       ("M5_r3_two_wheel_daily", "M5_r3_two_wheel_daily"),
                       ("BLEND_r3_two_wheel_daily", "BLEND_city_two_wheel_daily"),
                       ("BLEND_r3_two_wheel_weekly_people", "BLEND_city_two_wheel_weekly_people"),
                       ("BLEND_r3_two_wheel_weekly_people", "BLEND_r3_two_wheel_weekly_people"),
                       ("BLEND_zone_two_wheel_weekly_people", "BLEND_city_two_wheel_weekly_people"),
                       ("DAILY_r3", "DAILY_r3"), ("DAILY_city", "DAILY_city"), ("DAILY_county", "DAILY_city"),
                       ("DAILY_county_two_wheel", "BLEND_city_two_wheel_daily"),
                       ("M5_county_two_wheel_daily", "M5_city_two_wheel_daily")]:
        rr = ratio(la_k, sf_k)
        print(f"LA {la_k} / SF {sf_k}: " + " ".join(f"{s}={rr[s]:.3f}" for s in SC) + f" p50={rr['p50']:.3f}")

    print("\n---- M4 recomputed on per-two-wheel-courier basis ----")
    out = {}
    for s in SC:
        g = lambda k: la_params[k].pick(s)
        pen_city = sf_scen[s]["HMP_pen_city_two_wheel_weekly_blend"]
        pen_r3 = sf_scen[s]["HMP_pen_r3_two_wheel_weekly_blend"]
        la_pool_r3 = la_scen[s]["BLEND_r3_two_wheel_weekly_people"]
        la_pool_zone = la_scen[s]["BLEND_zone_two_wheel_weekly_people"]
        mat, reach = g("la_maturity_vs_sf_at_m24"), g("reachable_share_768ceres")
        m4_old = la_scen[s]["M4_hmp_customers_r3_m24"]
        m4_new_city = pen_city * la_pool_r3 * mat * reach
        m4_new_r3 = pen_r3 * la_pool_r3 * mat * reach
        m4_new_noreach = pen_city * la_pool_r3 * mat
        m4_new_reach_adj = pen_city * la_pool_r3 * mat * {"conservative": 0.6, "base": 0.8, "aggressive": 1.0}[s]
        out[s] = dict(pen_city=pen_city, pen_r3=pen_r3, la_pool_r3=la_pool_r3, m4_old=m4_old, m4_new_city=m4_new_city,
                      m4_new_r3=m4_new_r3, m4_new_noreach=m4_new_noreach, m4_new_reach_adj=m4_new_reach_adj,
                      som_m24=la_scen[s]["SOM_people_m24"], sam=la_scen[s]["SAM_people_hub"])
        print(s, {k: round(v, 3) if v < 2 else round(v) for k, v in out[s].items()})
    # MC version of M4 new: sample jointly
    random.seed(11)
    vals = []
    for _ in range(20000):
        pk = lambda q: q.sample()
        rs = compute_sf(sf, pk); rl = ms.compute(la_params, pk)
        vals.append(rs["HMP_pen_city_two_wheel_weekly_blend"] * rl["BLEND_r3_two_wheel_weekly_people"]
                    * la_params["la_maturity_vs_sf_at_m24"].sample() * la_params["reachable_share_768ceres"].sample())
    vals.sort(); n = len(vals)
    print("M4_new MC p10/p50/p90:", round(vals[int(n*.1)]), round(vals[int(n*.5)]), round(vals[int(n*.9)]))
    json.dump({"sf_scen": sf_scen, "sf_mc": sf_mc, "m4": out}, open("/tmp/claude-0/-home-user-manual/388ed474-de23-51b8-a42a-e9a5d51078e5/scratchpad/market/sf_backtest_raw.json", "w"), indent=1, default=float)
