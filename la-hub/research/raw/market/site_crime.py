#!/usr/bin/env python3
"""Street-crime exposure around candidate hub sites from LAPD 'Crime Data from 2020 to Present' (data.lacity.org 2nrs-mtv8).
Window: 2023-01-01 .. 2024-03-07 (14.2 months; LAPD switched RMS in March 2024 so later months are incomplete).
Codes: 210 robbery, 220 attempted robbery, 230 aggravated assault, 480 bike stolen, 510 vehicle stolen.
Output: site_crime.csv / site_crime.json (counts within 0.5 and 1.0 mi, night share, per-sq-mi rates, city index)."""
import json, math, csv, ast, re

def haversine(lat1, lon1, lat2, lon2):
    R = 3958.8
    p1, p2 = math.radians(lat1), math.radians(lat2)
    a = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(lon2 - lon1) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))

_src = open("/tmp/claude-0/-home-user-manual/388ed474-de23-51b8-a42a-e9a5d51078e5/scratchpad/market/site_coverage.py").read()
SITES = ast.literal_eval(re.search(r"SITES = (\{.*?\n\})", _src, re.S).group(1))  # same candidate list as site_coverage.py

RAW = "/tmp/claude-0/-home-user-manual/388ed474-de23-51b8-a42a-e9a5d51078e5/scratchpad/market/raw"
OUT = "/tmp/claude-0/-home-user-manual/388ed474-de23-51b8-a42a-e9a5d51078e5/scratchpad/market"
MONTHS = 14.2
CITY_SQMI = 469.0

rows = json.load(open(f"{RAW}/lapd_crimes_2023_24q1.json"))
pts = []
for r in rows:
    try:
        lat, lon = float(r["lat"]), float(r["lon"])
    except Exception:
        continue
    if lat == 0 or lon == 0:
        continue
    t = int(r.get("time_occ") or 0)
    night = t >= 2000 or t < 600
    pts.append((lat, lon, r["crm_cd"], night))
print("points:", len(pts))

GROUPS = {"robbery": {"210", "220"}, "agg_assault": {"230"}, "bike_stolen": {"480"}, "vehicle_stolen": {"510"}}
city_rate = {g: sum(1 for p in pts if p[2] in codes) / MONTHS / CITY_SQMI for g, codes in GROUPS.items()}

out = []
for name, (slat, slon) in SITES.items():
    if name.startswith(("Pasadena", "Long Beach", "Glendale", "Culver", "Santa Monica", "West Hollywood", "Vernon")):
        continue  # outside LAPD jurisdiction (own PD), data not comparable
    rec = {"site": name}
    for rad in (0.5, 1.0):
        area = math.pi * rad * rad
        near = [p for p in pts if haversine(slat, slon, p[0], p[1]) <= rad]
        for g, codes in GROUPS.items():
            n = sum(1 for p in near if p[2] in codes)
            rec[f"{g}_{rad}mi"] = n
            rec[f"{g}_{rad}mi_per_sqmi_mo"] = round(n / MONTHS / area, 2)
            rec[f"{g}_{rad}mi_x_city"] = round((n / MONTHS / area) / city_rate[g], 1) if city_rate[g] else None
        viol = [p for p in near if p[2] in GROUPS["robbery"] | GROUPS["agg_assault"]]
        rec[f"violent_{rad}mi"] = len(viol)
        rec[f"violent_night_share_{rad}mi"] = round(sum(1 for p in viol if p[3]) / len(viol), 2) if viol else None
    out.append(rec)
out.sort(key=lambda r: r["robbery_0.5mi"] + r["agg_assault_0.5mi"])
json.dump({"window": "2023-01-01..2024-03-07", "months": MONTHS, "city_rate_per_sqmi_mo": city_rate, "sites": out},
          open(f"{OUT}/site_crime.json", "w"), indent=1)
with open(f"{OUT}/site_crime.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(out[0].keys()))
    w.writeheader(); w.writerows(out)
print("city rate per sqmi per month:", {k: round(v, 2) for k, v in city_rate.items()})
print(f"{'site':46s} {'rob.5':>5s} {'asl.5':>5s} {'bike.5':>6s} {'veh.5':>5s} {'xcity_rob.5':>11s} {'rob1':>5s} {'asl1':>5s} {'bike1':>5s} {'xcity_rob1':>10s} {'night%':>6s}")
for r in out:
    print(f"{r['site'][:46]:46s} {r['robbery_0.5mi']:5d} {r['agg_assault_0.5mi']:5d} {r['bike_stolen_0.5mi']:6d} {r['vehicle_stolen_0.5mi']:5d} {str(r['robbery_0.5mi_x_city']):>11s} {r['robbery_1.0mi']:5d} {r['agg_assault_1.0mi']:5d} {r['bike_stolen_1.0mi']:5d} {str(r['robbery_1.0mi_x_city']):>10s} {str(r['violent_night_share_1.0mi']):>6s}")
