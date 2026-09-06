import json, math, random, sys, copy
sys.path.insert(0, "/tmp/claude-0/-home-user-manual/388ed474-de23-51b8-a42a-e9a5d51078e5/scratchpad/market/critic")
import market_size as ms

p = ms.load_params()
base = ms.compute(p, lambda q: q.pick("base"))

print("=== A. M1 vs M2 collapse ===")
for s in ("conservative", "base", "aggressive"):
    g = lambda k: p[k].pick(s)
    nyc_orders_wk = g("nyc_weekly_active_couriers") * g("nyc_deliveries_per_courier_week")
    nyc_opr_wk = nyc_orders_wk / g("nyc_restaurants")
    la_orders_day_M1 = nyc_opr_wk * g("la_orders_per_restaurant_vs_nyc") * g("restaurants_county_la") / 7
    la_orders_day_M2 = g("doordash_us_deliveries_per_day") / g("doordash_us_share") * g("la_county_share_us_orders")
    opd_implied_M1 = g("la_deliveries_per_courier_week") / (7 * g("weekly_to_daily_active"))
    opd_M2 = g("orders_per_courier_day")
    # derive la_orders_per_restaurant_vs_nyc from M2 inputs as the note describes
    us_per_res_wk = g("doordash_us_deliveries_per_day") / g("doordash_us_share") * 7 / 340.1e6
    nyc_per_res_wk = 2.77e6 / 8.478e6
    la_int = g("la_county_share_us_orders") / 0.0287
    ratio_from_M2 = us_per_res_wk * la_int / nyc_per_res_wk
    print(f"{s:13s} NYC orders/wk {nyc_orders_wk/1e6:.2f}M  NYC orders/rest-wk {nyc_opr_wk:.0f} | LA county orders/day: M1 {la_orders_day_M1:,.0f} vs M2 {la_orders_day_M2:,.0f} (ratio {la_orders_day_M1/la_orders_day_M2:.2f})"
          f" | opd implied by M1 (dpcw/(7*w2d)) {opd_implied_M1:.2f} vs M2 opd {opd_M2} (ratio {opd_implied_M1/opd_M2:.2f})"
          f" | la_orders_per_restaurant_vs_nyc param {g('la_orders_per_restaurant_vs_nyc')} vs derived-from-M2-inputs {ratio_from_M2:.3f}")

print("\n=== B. NYC implied hours / deliveries per hour ===")
dl_wk = 2.72e6; acc_trip = 60e3; acc_tot = 70e3; trip_h = 888e3; tot_h = 1074e3
print(f"deliveries per trip-performing account-week {dl_wk/acc_trip:.1f}; per total account {dl_wk/acc_tot:.1f}")
print(f"total hrs per trip-performing account-wk {tot_h/acc_trip:.1f}; per total account {tot_h/acc_tot:.1f}; deliveries per total hr {dl_wk/tot_h:.2f}; per trip hr {dl_wk/trip_h:.2f}")
for dedup in (1.0, 1.2, 1.5, 1.8):
    ppl = acc_trip / dedup
    for w2d in (0.8, 0.85):
        daily = ppl * w2d
        print(f"  accounts/person {dedup}: weekly people {ppl:,.0f}; daily-active @w2d {w2d}: {daily:,.0f}; orders per courier-day {dl_wk/7/daily:.1f}; hrs per courier-day {tot_h/7/daily:.1f}")
print("Model note used 61k x 0.8 = 49k daily -> ", dl_wk/7/49e3)

print("\n=== C. LA implied hours from (opd, w2d, dpcw) ===")
for s in ("conservative", "base", "aggressive"):
    g = lambda k: p[k].pick(s)
    opd = g("orders_per_courier_day"); w2d = g("weekly_to_daily_active"); dpcw = g("la_deliveries_per_courier_week")
    for rate in (1.0, 1.3, 1.5):
        print(f"{s:13s} opd {opd} w2d {w2d} dpcw {dpcw} | at {rate}/online-hr: hrs per active day {opd/rate:.1f}, days/wk {dpcw/opd:.2f} (identity days/wk = 7*w2d = {7*w2d:.2f}), online hrs/wk {dpcw/rate:.1f}")
print("Seattle: 12.7 offers/account-wk at 12.0 online hrs -> 1.06/online hr; DoorDash CA ~6 engaged hrs/wk (Q4 2023); DoorDash US ~4 hrs/wk")
# DoorDash bottom-up
dd_weekly_us = 8e6 * 10/52
dd_orders_wk_us = 3.6e6*7
print(f"DoorDash bottom-up: 8M annual x 10/52 = {dd_weekly_us/1e6:.2f}M weekly-active US; orders per weekly-active Dasher-week = {dd_orders_wk_us/dd_weekly_us:.1f} (model LA dpcw base 22)")
la_dd_weekly = dd_weekly_us * 0.0344
la_dd_orders_day = 3.6e6*0.0344
print(f"  LA County weekly-active Dashers {la_dd_weekly:,.0f}; DD orders/day {la_dd_orders_day:,.0f}; at opd 9 -> daily {la_dd_orders_day/9:,.0f} -> w2d {la_dd_orders_day/9/la_dd_weekly:.2f}; at opd 7 -> w2d {la_dd_orders_day/7/la_dd_weekly:.2f}; at w2d 0.40 -> opd {la_dd_orders_day/(0.4*la_dd_weekly):.1f}")
print(f"  all-app weekly-active LA County if DD = 62% of orders and other-app couriers same productivity: {la_dd_weekly/0.62:,.0f}; with 15% overlap dedup: {la_dd_weekly/0.62*0.85:,.0f}  (model WEEKLY_county {base['WEEKLY_county']:,.0f})")

print("\n=== D. M5 NYC calibration recomputed ===")
nyc_mi_day = 45238991/61; la_mi_day = 38304846/61
for dd_nyc_share in (0.28, 0.35, 0.45):
    nyc_dd_2w_daily = 63000*dd_nyc_share*0.55*0.85
    for mpd in (45, 50, 60, 80):
        cal = nyc_dd_2w_daily / (nyc_mi_day/mpd)
        print(f"DD NYC share {dd_nyc_share}: NYC DD two-wheel daily-active {nyc_dd_2w_daily:,.0f}; at mpd {mpd}: miles route {nyc_mi_day/mpd:,.0f}; consistent cal {cal:.2f}")
print("Model cal lo/base/hi = 0.45/0.60/0.80 paired with mpd lo/base/hi = 80/60/45 (params are sampled independently)")
# consistent M5 (mpd cancels)
for dd_nyc_share in (0.28, 0.35, 0.45):
    nyc_dd_2w_daily = 63000*dd_nyc_share*0.55*0.85
    for cs in (0.9, 1.0, 1.5):
        m5 = nyc_dd_2w_daily * (la_mi_day/nyc_mi_day) * cs / 0.6
        print(f"  consistent M5 county two-wheel (mpd cancels): DD NYC share {dd_nyc_share}, county/label {cs}: {m5:,.0f}  vs M1-3 county two-wheel {base['DAILY_county_two_wheel']:,.0f} -> ratio {m5/base['DAILY_county_two_wheel']:.2f}")
# miles per delivery sanity
nyc_deliv_day = 2.72e6/7
for dd_nyc_share in (0.28, 0.45):
    dd2w = nyc_deliv_day*dd_nyc_share*0.55
    print(f"  NYC DD two-wheel deliveries/day @share {dd_nyc_share}: {dd2w:,.0f} -> implied on-app miles per two-wheel delivery {nyc_mi_day/dd2w:.1f} (DCWP avg delivery distance 1.77 mi)")
# LA: M1-3 implied DD two-wheel deliveries city/county
la_city_orders = base['county_orders_per_day']*11396/28161
print(f"  LA M1-3: county two-wheel deliveries/day {base['county_orders_per_day']*0.46:,.0f}; city {la_city_orders*0.46:,.0f}; DD share 0.6 -> county DD 2w {base['county_orders_per_day']*0.46*0.6:,.0f}, city DD 2w {la_city_orders*0.46*0.6:,.0f}; LA DD 2w miles/day {la_mi_day:,.0f} -> mi per DD 2w delivery: county-label {la_mi_day/(base['county_orders_per_day']*0.46*0.6):.1f}, city-label {la_mi_day/(la_city_orders*0.46*0.6):.1f}")

print("\n=== E. Zone allocation implications ===")
zone_orders = base['county_orders_per_day']*1962/28161*1.15
print(f"zone orders/day {zone_orders:,.0f}; per resident-week {zone_orders*7/319377:.3f} (NYC-wide 2.77M/8.48M = {2.77e6/8.478e6:.3f}; US avg {3.6e6/0.62*7/340.1e6:.3f}; LA county {base['county_orders_per_day']*7/9808667:.3f})")
print(f"zone orders per restaurant-week {zone_orders*7/1962:.0f} vs NYC-wide {2.72e6/23000:.0f}; restaurants per 1000 pop: zone {1962/319.377:.2f}, county {28161/9808.667:.2f}, NYC {23000/8478:.2f}")
# population-based allocation alternative
pop_alloc = base['county_orders_per_day']*319377/9808667
print(f"population-share allocation would give zone orders/day {pop_alloc:,.0f} ({pop_alloc/zone_orders:.2f}x restaurant-based)")
for z, rest, pop in (("Downtown",910,65583),("Koreatown",611,93936),("Westlake",104,49512),("Pico-Union",126,36797),("USC",211,73549)):
    o = base['county_orders_per_day']*rest/28161*1.15
    print(f"  {z:10s} orders/day {o:,.0f}; per resident-week {o*7/pop:.2f}")

print("\n=== F. DPH vs NAICS/QCEW denominators ===")
print(f"LA County DPH restaurants 28,161 vs QCEW NAICS 722 establishments Jun 2025 23,099 -> {28161/23099:.2f}x")
print(f"SF DPH 4,514 vs SF NAICS 722 5,364 -> {4514/5364:.2f}x ; LA City DPH 11,396 vs NAICS7225 geocoded 8,568 -> {11396/8568:.2f}x, vs all incl. non-geocoded 12,399 -> {11396/12399:.2f}x")
print(f"LA r3 DPH 2,021 vs NAICS geocoded 1,568 -> {2021/1568:.2f}x; SF/LA DPH-to-NAICS mismatch factor {(2021/1568)/(4514/5364):.2f}")
m4_naics = 800/5364 * 1568 * (base['two_wheel_courier_share_zone']/0.6) * 0.8 * 0.5
m4_naics_adj = 800/5364 * 1568/(1-0.266) * (base['two_wheel_courier_share_zone']/0.6) * 0.8 * 0.5
print(f"M4 with NAICS denominators: {m4_naics:.0f} (geocoded) / {m4_naics_adj:.0f} (missing-coords scaled) vs model {base['M4_hmp_customers_r3_m24']:.0f}; if only 80% of SF customers are couriers: {m4_naics*0.8:.0f}-{m4_naics_adj*0.8:.0f}")

print("\n=== G. Mode-specific weekly-to-daily ===")
for w_tw, w_car in ((0.55,0.28),(0.6,0.3),(0.65,0.25)):
    tw_w = base['BLEND_zone_two_wheel_daily']/w_tw
    car_w = base['DAILY_zone_car']/w_car
    blend = (base['BLEND_zone_two_wheel_daily']*w_tw + base['DAILY_zone_car']*w_car)/(base['BLEND_zone_two_wheel_daily']+base['DAILY_zone_car'])
    sam = (tw_w*0.75 + car_w*0.05)*0.5
    print(f"w2d two-wheel {w_tw}, car {w_car} (implied blended {blend:.2f}): two-wheel weekly people {tw_w:,.0f} (model {base['BLEND_zone_two_wheel_weekly_people']:,.0f}); car weekly {car_w:,.0f}; SAM {sam:,.0f} (model {base['SAM_people_hub']:,.0f}); SOM m12 {sam*0.1:.0f} m24 {sam*0.2:.0f}")

print("\n=== H. Correlated Monte Carlo (tie shared quantities) ===")
random.seed(7)
N = 20000
def sample_corr():
    d = {k: v.sample() for k, v in p.items()}
    # tie LA order intensity: derive la_orders_per_restaurant_vs_nyc from la_county_share_us_orders & DoorDash inputs (as its note does)
    us_per_res_wk = d["doordash_us_deliveries_per_day"] / d["doordash_us_share"] * 7 / 340.1e6
    d["la_orders_per_restaurant_vs_nyc"] = us_per_res_wk * (d["la_county_share_us_orders"]/0.0287) / (2.77e6/8.478e6)
    # tie opd to identity with dpcw and w2d
    d["orders_per_courier_day"] = d["la_deliveries_per_courier_week"] / (7*d["weekly_to_daily_active"])
    # tie M5 calibration to mpd (NYC-consistent)
    nyc_dd = 63000*0.28*0.55*0.85
    d["nyc_miles_calibration"] = nyc_dd / (nyc_mi_day/d["miles_per_two_wheel_courier_day"])
    return d
keys = ["DAILY_zone","WEEKLY_zone","SPREAD_zone","DAILY_county","BLEND_zone_two_wheel_daily","M5_county_two_wheel_daily","M5_vs_M123_county_two_wheel","SAM_people_hub","SOM_people_m24","M4_hmp_customers_r3_m24"]
draws = {k: [] for k in keys}
for _ in range(N):
    d = sample_corr()
    r = ms.compute(p, lambda q, d=d: d[[k for k,v in p.items() if v is q][0]])
    for k in keys: draws[k].append(r[k])
for k in keys:
    v = sorted(draws[k]); n = len(v)
    print(f"{k:32s} P10 {v[int(n*.1)]:>9,.2f}  P50 {v[int(n*.5)]:>9,.2f}  P90 {v[int(n*.9)]:>9,.2f}   (P90/P10 {v[int(n*.9)]/v[int(n*.1)]:.2f})")
