#!/usr/bin/env python3
"""Candidate-site coverage: restaurants, population and a two-wheel-courier index within radii of candidate hub sites.
Inputs: LA County DPH restaurant inventory (geojson), NC polygons, ACS tract population + vehicles (already downloaded).
Output: site_coverage.csv + site_coverage.json in the market dir."""
import json, math, csv, re
from collections import defaultdict
from shapely.geometry import shape, Point
from shapely.strtree import STRtree

RAW = "/tmp/claude-0/-home-user-manual/388ed474-de23-51b8-a42a-e9a5d51078e5/scratchpad/market/raw"
OUT = "/tmp/claude-0/-home-user-manual/388ed474-de23-51b8-a42a-e9a5d51078e5/scratchpad/market"

# ---------- candidate sites (lat, lon) ----------
SITES = {
    "768 Ceres Ave (baseline, Warehouse District)": (34.0363, -118.2447),
    "DTLA South Park (Pico/Flower)": (34.0390, -118.2650),
    "DTLA Historic Core (6th/Spring)": (34.0455, -118.2500),
    "DTLA Financial (7th/Figueroa)": (34.0485, -118.2590),
    "Fashion District (9th/Santee)": (34.0380, -118.2545),
    "Arts District (Traction/Alameda)": (34.0430, -118.2335),
    "Little Tokyo (1st/Central)": (34.0500, -118.2400),
    "Chinatown (Broadway/College)": (34.0640, -118.2380),
    "Westlake / MacArthur Park (7th/Alvarado)": (34.0570, -118.2750),
    "Pico-Union (Pico/Union)": (34.0430, -118.2790),
    "Koreatown East (6th/Vermont)": (34.0632, -118.2917),
    "Koreatown Core (Wilshire/Western)": (34.0617, -118.3089),
    "Koreatown South (Olympic/Normandie)": (34.0525, -118.3005),
    "Koreatown West (Wilshire/Crenshaw)": (34.0620, -118.3255),
    "USC / Exposition (Figueroa/Jefferson)": (34.0250, -118.2790),
    "Hollywood (Hollywood/Vine)": (34.1016, -118.3267),
    "East Hollywood (Sunset/Vermont)": (34.0980, -118.2915),
    "Silver Lake (Sunset/Silver Lake Blvd)": (34.0905, -118.2705),
    "Echo Park (Sunset/Echo Park Ave)": (34.0780, -118.2600),
    "Mid-City (Pico/Fairfax)": (34.0480, -118.3610),
    "West Hollywood (Santa Monica/La Cienega)": (34.0900, -118.3765),
    "Boyle Heights (Cesar Chavez/Soto)": (34.0470, -118.2100),
    "Historic South Central (Central/Vernon)": (34.0030, -118.2560),
    "Vernon industrial (Vernon/Santa Fe)": (34.0045, -118.2300),
    "Lincoln Heights (Broadway/Daly)": (34.0700, -118.2170),
    "Westwood (Westwood/Wilshire)": (34.0590, -118.4440),
    "Santa Monica (Wilshire/4th)": (34.0230, -118.4950),
    "Culver City (Venice/Culver)": (34.0230, -118.3960),
    "Glendale (Brand/Broadway)": (34.1470, -118.2550),
    "Pasadena (Colorado/Lake)": (34.1455, -118.1320),
    "Long Beach (Pine/Broadway)": (33.7700, -118.1930),
}
RADII = [1.0, 1.5, 2.0, 3.0]

# two-wheel courier share by area (LA-reality review sub-zone view; LA-wide 0.34); used to weight restaurants
TW_SHARE_BY_AREA = [  # (name, polygon-ish centroid, radius mi, share) -- coarse
    ("DTLA core", (34.0450, -118.2520), 1.6, 0.50),
    ("Koreatown", (34.0610, -118.3000), 1.5, 0.35),
    ("Westlake/Pico-Union", (34.0530, -118.2790), 1.0, 0.45),
    ("USC", (34.0240, -118.2820), 1.2, 0.30),
    ("Hollywood", (34.1000, -118.3300), 1.8, 0.45),
    ("Silver Lake/Echo Park", (34.0850, -118.2650), 1.5, 0.40),
    ("Westwood", (34.0600, -118.4440), 1.2, 0.45),
    ("Santa Monica/Venice", (34.0150, -118.4900), 2.0, 0.50),
    ("West Hollywood", (34.0900, -118.3700), 1.5, 0.45),
]
DEFAULT_TW = 0.30

def haversine(lat1, lon1, lat2, lon2):
    R = 3958.8
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = p2 - p1
    dl = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))

def tw_share_at(lat, lon):
    best = DEFAULT_TW
    for name, (clat, clon), rad, share in TW_SHARE_BY_AREA:
        if haversine(lat, lon, clat, clon) <= rad:
            best = max(best, share) if best != DEFAULT_TW else share
    return best

# ---------- restaurants ----------
gj = json.load(open(f"{RAW}/dph_restaurant_market_inventory.geojson"))
feats = gj["features"]
props0 = feats[0]["properties"]
pe_key = next((k for k in props0 if "PE_DESC" in k.upper() or k.upper() == "PE_DESCRIPTION"), None)
name_key = next((k for k in props0 if k.upper() in ("FACILITY_NAME", "NAME")), None)
addr_key = next((k for k in props0 if "ADDRESS" in k.upper()), None)
rest = {}
for ft in feats:
    p = ft["properties"]
    pe = str(p.get(pe_key, "")).upper() if pe_key else "RESTAURANT"
    if "RESTAURANT" not in pe:
        continue
    g = ft.get("geometry")
    if not g or g.get("type") != "Point":
        continue
    lon, lat = g["coordinates"][:2]
    if not (33.5 < lat < 34.9 and -119 < lon < -117.5):
        continue
    key = (str(p.get(name_key, "")).strip().upper(), str(p.get(addr_key, "")).strip().upper())
    if key in rest:
        continue
    rest[key] = (lat, lon)
R = list(rest.values())
print("restaurants deduped:", len(R))

# ---------- tracts: population, zero-vehicle households ----------
tracts = {}
for line in open(f"{RAW}/2024_gaz_tracts_06.txt", encoding="latin-1"):
    parts = line.rstrip("\n").split("\t")
    if parts[0] == "USPS":
        continue
    geoid = parts[1].strip()
    if not geoid.startswith("06037"):
        continue
    try:
        tracts[geoid] = {"lat": float(parts[-2]), "lon": float(parts[-1]), "aland": float(parts[2] if False else parts[-6])}
    except Exception:
        pass
# population (B01003) and vehicles (B25044) from the summary .dat files used earlier
def load_dat(path, col_pop=None):
    out = {}
    with open(path, encoding="utf-8", errors="ignore") as fh:
        hdr = fh.readline().rstrip("\n").split("|")
        for line in fh:
            row = line.rstrip("\n").split("|")
            d = dict(zip(hdr, row))
            geo = d.get("GEO_ID", "")
            if "US06037" in geo:
                out[geo.split("US")[-1]] = d
    return out
pop = load_dat(f"{RAW}/acsdt5y2024-b01003_ca037tracts.dat")
veh = load_dat(f"{RAW}/acsdt5y2024-b25044_ca037tracts.dat")
for geoid, t in tracts.items():
    t["pop"] = float(pop.get(geoid, {}).get("B01003_E001", 0) or 0)
    v = veh.get(geoid, {})
    tot = float(v.get("B25044_E001", 0) or 0)
    zero = float(v.get("B25044_E003", 0) or 0) + float(v.get("B25044_E010", 0) or 0)
    t["hh"] = tot
    t["zero_veh_hh"] = zero
print("tracts:", len(tracts), "pop sum:", sum(t["pop"] for t in tracts.values()))

# ---------- compute ----------
rows = []
for name, (slat, slon) in SITES.items():
    row = {"site": name, "lat": slat, "lon": slon}
    dists = [haversine(slat, slon, lat, lon) for lat, lon in R]
    for rad in RADII:
        n = sum(1 for d in dists if d <= rad)
        row[f"rest_{rad}mi"] = n
    # two-wheel index: sum over restaurants within 3 mi of tw_share x distance decay (exp(-d/1.5))
    idx = 0.0
    for (lat, lon), d in zip(R, dists):
        if d <= 3.0:
            idx += tw_share_at(lat, lon) * math.exp(-d / 1.5)
    row["tw_index_3mi"] = round(idx, 1)
    for rad in (1.5, 3.0):
        P = Z = H = 0.0
        for t in tracts.values():
            if haversine(slat, slon, t["lat"], t["lon"]) <= rad:
                P += t["pop"]; Z += t["zero_veh_hh"]; H += t["hh"]
        row[f"pop_{rad}mi"] = int(P)
        row[f"zero_veh_share_{rad}mi"] = round(Z / H, 3) if H else None
    rows.append(row)
rows.sort(key=lambda r: -r["tw_index_3mi"])
with open(f"{OUT}/site_coverage.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
json.dump(rows, open(f"{OUT}/site_coverage.json", "w"), indent=1)
print(f"{'site':48s} {'r1':>5s} {'r1.5':>5s} {'r2':>5s} {'r3':>5s} {'twidx':>7s} {'pop1.5':>8s} {'pop3':>9s} {'0veh1.5':>8s}")
for r in rows:
    print(f"{r['site'][:48]:48s} {r['rest_1.0mi']:5d} {r['rest_1.5mi']:5d} {r['rest_2.0mi']:5d} {r['rest_3.0mi']:5d} {r['tw_index_3mi']:7.1f} {r['pop_1.5mi']:8d} {r['pop_3.0mi']:9d} {str(r['zero_veh_share_1.5mi']):>8s}")
