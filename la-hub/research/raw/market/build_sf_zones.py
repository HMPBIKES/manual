import json, re, math, collections
import pandas as pd
from shapely.geometry import shape, Point
from shapely.ops import unary_union, transform
from shapely import STRtree
import pyproj

RAW = "/tmp/claude-0/-home-user-manual/388ed474-de23-51b8-a42a-e9a5d51078e5/scratchpad/market/raw/"
OUT = "/tmp/claude-0/-home-user-manual/388ed474-de23-51b8-a42a-e9a5d51078e5/scratchpad/market/"

SHOP_LAT, SHOP_LON = 37.779201641761, -122.406384839161
MI = 1609.344
CORE = ["South of Market", "Mission", "Tenderloin", "Financial District/South Beach"]
RING = ["Chinatown", "Nob Hill", "Hayes Valley", "Western Addition", "Castro/Upper Market", "Potrero Hill", "Mission Bay"]
RADII = [1.5, 3, 5]

# projection: NAD83 / California zone 3 (ftUS) is common for SF; use EPSG:26910 UTM10N (metres) for area+distance
to_utm = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:26910", always_xy=True).transform
def proj(geom): return transform(to_utm, geom)

# ---------- polygons ----------
gj = json.load(open(RAW + "nhood_ajp5-b2md.geojson"))
nh = {}
nh_src_sqmi = {}
ALIAS = {"Financial District": "Financial District/South Beach"}
for f in gj["features"]:
    name = ALIAS.get(f["properties"]["nhood"], f["properties"]["nhood"])
    nh[name] = shape(f["geometry"])
    nh_src_sqmi[name] = float(f["properties"]["sum_sqmi"])
missing = [n for n in CORE + RING if n not in nh]
assert not missing, f"missing neighborhoods: {missing}; have {sorted(nh)}"
nh_utm = {k: proj(v) for k, v in nh.items()}
city_utm = unary_union(list(nh_utm.values()))
shop_utm = proj(Point(SHOP_LON, SHOP_LAT))
print("shop inside:", [k for k, v in nh_utm.items() if v.contains(shop_utm)])
circles = {r: shop_utm.buffer(r * MI, quad_segs=64) for r in RADII}

names = list(nh_utm)
tree = STRtree([nh_utm[n] for n in names])
def nhood_of(pt_utm):
    idx = tree.query(pt_utm, predicate="within")
    return names[idx[0]] if len(idx) else None

def zone_masks(df, xcol="x", ycol="y", nhcol="nhood"):
    """Return dict zone -> boolean mask."""
    m = {}
    for n in CORE + RING:
        m[n] = df[nhcol] == n
    m["CORE"] = df[nhcol].isin(CORE)
    m["RING"] = df[nhcol].isin(RING)
    for r in RADII:
        d = ((df[xcol] - shop_utm.x) ** 2 + (df[ycol] - shop_utm.y) ** 2) ** 0.5
        m[f"radius_{r:g}mi"] = d.notna() & (d <= r * MI)
    m["City of SF"] = df["in_sf"]
    return m

# ---------- registry (NAICS 722) ----------
reg = pd.DataFrame(json.load(open(RAW + "g8m3_food_active.json")))
print("registry rows pulled:", len(reg))
for c in ["administratively_closed", "neighborhoods_analysis_boundaries", "lic_code_descriptions_list", "location", "city"]:
    if c not in reg.columns: reg[c] = None; print(f"NOTE: column {c} absent in pull (all null)")
print("administratively_closed values:", reg["administratively_closed"].value_counts(dropna=False).to_dict())
reg["naics"] = reg["self_reported_naics_code"].fillna("")
reg["is722"] = reg["naics"].str.startswith("722")
reg["lic_rest"] = reg["lic_code_descriptions_list"].fillna("").str.upper().str.contains("RESTAURANT|TAKE-OUT|FAST FOOD", regex=True)
def norm(s):
    s = (s or "").lower()
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    s = re.sub(r"\b(the|llc|inc|corp|co|ltd|dba)\b", " ", s)
    return re.sub(r"\s+", " ", s).strip()
reg["k_name"] = reg["dba_name"].map(norm)
reg["k_addr"] = reg["full_business_address"].map(norm)
reg["has_loc"] = reg["location"].notna()
def xy(loc):
    if isinstance(loc, dict) and loc.get("coordinates"):
        lon, lat = loc["coordinates"][:2]
        p = proj(Point(lon, lat)); return p.x, p.y
    return (math.nan, math.nan)
reg[["x", "y"]] = pd.DataFrame(reg["location"].map(xy).tolist(), index=reg.index)
reg["nhood"] = [nhood_of(Point(x, y)) if not math.isnan(x) else None for x, y in zip(reg["x"], reg["y"])]
reg["nhood_field"] = reg["neighborhoods_analysis_boundaries"].replace(ALIAS)
print("registry field FiDi labels:", reg["neighborhoods_analysis_boundaries"].dropna()[reg["neighborhoods_analysis_boundaries"].dropna().str.contains("Financial")].unique())
# fallback to the dataset's own neighborhood field when no point
reg["nhood"] = reg["nhood"].where(reg["nhood"].notna(), reg["nhood_field"])
reg["city_sf"] = reg["city"].fillna("").str.strip().str.lower().str.replace(".", "", regex=False).str.startswith("san fran")
reg["in_sf"] = reg["nhood"].notna() | (~reg["has_loc"] & reg["city_sf"])
# agreement check between PIP and field
both = reg[reg["has_loc"] & reg["nhood_field"].notna()]
agree = (both["nhood"] == both["nhood_field"]).mean()
print(f"PIP vs field neighborhood agreement: {agree:.3%} on {len(both)} rows")

adm_closed = reg["administratively_closed"].fillna("").str.lower().str.contains("closed")
r722 = reg[reg["is722"] & ~adm_closed].copy()
print("NAICS722 active rows (excl admin-closed):", len(r722), "| admin-closed dropped:", int((reg["is722"] & adm_closed).sum()))
r722_dedup = r722.drop_duplicates(subset=["k_name", "k_addr"])
print("NAICS722 after dba+address dedupe:", len(r722_dedup))
share_noloc = 1 - r722_dedup["has_loc"].mean()
noloc_in_sf = int((~r722_dedup["has_loc"] & r722_dedup["in_sf"]).sum())
print(f"share lacking location: {share_noloc:.3%}; of which SF-city (kept for city count, assigned by nhood field if present): {noloc_in_sf}")
print("NAICS722 dedup in SF:", int(r722_dedup["in_sf"].sum()), "| outside SF / unknown:", int((~r722_dedup["in_sf"]).sum()))
# LIC-based cross-check (restaurant health permit on the business license) — any NAICS
lic = reg[reg["lic_rest"] & ~adm_closed].drop_duplicates(subset=["k_name", "k_addr"])
print("LIC RESTAURANT/TAKE-OUT/FAST FOOD dedup:", len(lic), "in SF:", int(lic["in_sf"].sum()))
# within-722 breakdown
print("722 codes:", r722_dedup["naics"].str[:6].value_counts().head(12).to_dict())

m722 = zone_masks(r722_dedup)
mlic = zone_masks(lic)

# ---------- DPH ----------
dph = pd.DataFrame(json.load(open(RAW + "dph_facilities.json")))
print("dph grouped rows:", len(dph), "| null permit_number:", int(dph["permit_number"].isna().sum()))
dph["pt"] = dph["permit_type"].fillna("").str.upper()
dph["is_rest"] = dph["pt"].str.contains(r"RESTAURANT|TAKE-OUT|FAST FOOD", regex=True)
dph["is_food_broad"] = dph["is_rest"] | dph["pt"].str.contains(r"BARS/TAVERNS W/FOOD|BAKERIES WITH FOOD|MOBILE FOOD|CATER|FOOD PREP AND SERVICE|RETAIL MKTS W/FOOD", regex=True)
dph["lat"] = pd.to_numeric(dph["latitude"], errors="coerce"); dph["lon"] = pd.to_numeric(dph["longitude"], errors="coerce")
bad = (dph["lat"].abs() < 1) | (dph["lon"].abs() < 1)
dph.loc[bad, ["lat", "lon"]] = math.nan
dph["key"] = dph["permit_number"].where(dph["permit_number"].notna(), "NP:" + dph["dba"].map(norm) + "|" + dph["street_address_clean"].map(norm))
dph = dph.sort_values("last_insp", ascending=False)
def xy2(lat, lon):
    if math.isnan(lat) or math.isnan(lon): return (math.nan, math.nan)
    p = proj(Point(lon, lat)); return p.x, p.y
dph[["x", "y"]] = pd.DataFrame([xy2(a, b) for a, b in zip(dph["lat"], dph["lon"])], index=dph.index)
dph["nhood_pip"] = [nhood_of(Point(x, y)) if not math.isnan(x) else None for x, y in zip(dph["x"], dph["y"])]
dph["analysis_neighborhood"] = dph["analysis_neighborhood"].replace(ALIAS)
print("dph field FiDi labels:", dph["analysis_neighborhood"].dropna()[dph["analysis_neighborhood"].dropna().str.contains("Financial")].unique())
dph["nhood"] = dph["nhood_pip"].where(dph["nhood_pip"].notna(), dph["analysis_neighborhood"])
dph["in_sf"] = True  # DPH SF permits only
drest = dph[dph["is_rest"]].drop_duplicates(subset=["key"])
dbroad = dph[dph["is_food_broad"]].drop_duplicates(subset=["key"])
print("DPH restaurant facilities (distinct permits):", len(drest), "| lacking coords:", int(drest["x"].isna().sum()), "| lacking nhood:", int(drest["nhood"].isna().sum()))
print("DPH broad food-service facilities:", len(dbroad))
b2 = drest[drest["nhood_pip"].notna() & drest["analysis_neighborhood"].notna()]
print(f"DPH PIP vs field agreement: {(b2['nhood_pip']==b2['analysis_neighborhood']).mean():.3%}")
mdph = zone_masks(drest)
mdphb = zone_masks(dbroad)

# ---------- Census ----------
pop = pd.read_csv(RAW + "acsdt5y2023-b01003_sf_tracts.txt", sep="|", dtype=str)
veh = pd.read_csv(RAW + "acsdt5y2023-b08201_sf_tracts.txt", sep="|", dtype=str)
gaz = pd.read_csv(RAW + "2023_gaz_tracts_06.txt", sep="\t", dtype=str)
gaz.columns = [c.strip() for c in gaz.columns]
gaz = gaz[gaz["GEOID"].str.startswith("06075")].copy()
pop["GEOID"] = pop["GEO_ID"].str[-11:]; veh["GEOID"] = veh["GEO_ID"].str[-11:]
tr = pop[["GEOID", "B01003_E001"]].merge(veh[["GEOID", "B08201_E001", "B08201_E002"]], on="GEOID", how="left").merge(
    gaz[["GEOID", "ALAND_SQMI", "INTPTLAT", "INTPTLONG"]], on="GEOID", how="left")
for c in ["B01003_E001", "B08201_E001", "B08201_E002", "ALAND_SQMI", "INTPTLAT", "INTPTLONG"]:
    tr[c] = pd.to_numeric(tr[c], errors="coerce")
print("tracts:", len(tr), "| no gazetteer match:", int(tr["INTPTLAT"].isna().sum()), "| city pop:", int(tr["B01003_E001"].sum()))
tr[["x", "y"]] = pd.DataFrame([xy2(a, b) for a, b in zip(tr["INTPTLAT"], tr["INTPTLONG"])], index=tr.index)
tr["nhood"] = [nhood_of(Point(x, y)) if not math.isnan(x) else None for x, y in zip(tr["x"], tr["y"])]
un = tr[tr["nhood"].isna()]
print("tracts with centroid outside all polygons:", len(un), un[["GEOID", "B01003_E001"]].to_dict("records"))
# snap unassigned tracts to nearest neighborhood polygon (so city sums stay whole)
for i, row in un.iterrows():
    p = Point(row["x"], row["y"])
    tr.loc[i, "nhood"] = min(names, key=lambda n: nh_utm[n].distance(p))
tr["in_sf"] = True
mtr = zone_masks(tr)

# ---------- assemble ----------
def area_sqmi(zone):
    if zone in nh_utm: g = nh_utm[zone]
    elif zone == "CORE": g = unary_union([nh_utm[n] for n in CORE])
    elif zone == "RING": g = unary_union([nh_utm[n] for n in RING])
    elif zone.startswith("radius"): g = circles[float(zone.split("_")[1][:-2])].intersection(city_utm)
    else: g = city_utm
    return g.area / MI ** 2

rows = []
zones = CORE + ["CORE", "RING"] + [f"radius_{r:g}mi" for r in RADII] + ["City of SF"]
for z in zones:
    a = area_sqmi(z)
    p = int(tr.loc[mtr[z], "B01003_E001"].sum())
    hh = tr.loc[mtr[z], "B08201_E001"].sum(); zv = tr.loc[mtr[z], "B08201_E002"].sum()
    n722 = int(m722[z].sum()); ndph = int(mdph[z].sum())
    notes = []
    if z in nh_src_sqmi: notes.append(f"DataSF polygon sum_sqmi={nh_src_sqmi[z]:.2f}")
    if z.startswith("radius"):
        r = float(z.split("_")[1][:-2]); full = math.pi * r ** 2
        notes.append(f"area = SF land within {r:g} mi circle (full circle {full:.1f} sqmi incl. bay/outside SF); pop = SF tracts w/ centroid in circle")
    notes.append(f"LIC-restaurant cross-check={int(mlic[z].sum())}; DPH broad food-service={int(mdphb[z].sum())}; tracts={int(mtr[z].sum())}")
    if z == "City of SF":
        notes.append(f"NAICS722 w/o coordinates but city=SF included={noloc_in_sf}")
    rows.append(dict(zone=z, area_sqmi=round(a, 2), population_acs=p, population_year="ACS 2023 5-yr",
                     zero_vehicle_hh_share=round(zv / hh, 3) if hh else None,
                     restaurants_naics722=n722, restaurants_dph=ndph,
                     restaurants_per_sqmi=round(n722 / a, 1) if a else None, notes="; ".join(notes)))
df = pd.DataFrame(rows)
df.to_csv(OUT + "sf_zones.csv", index=False)
print(df.drop(columns=["notes"]).to_string(index=False))

# per-neighborhood detail for reference
detail = []
for n in names:
    mk = r722_dedup["nhood"] == n; md = drest["nhood"] == n; mt = tr["nhood"] == n
    detail.append(dict(nhood=n, area_sqmi=round(nh_utm[n].area / MI ** 2, 2), pop=int(tr.loc[mt, "B01003_E001"].sum()),
                       naics722=int(mk.sum()), dph_rest=int(md.sum())))
pd.DataFrame(detail).sort_values("naics722", ascending=False).to_csv(OUT + "sf_all_neighborhoods.csv", index=False)

stats = dict(
    registry_rows_pulled=int(len(reg)), naics722_rows=int(len(r722)), naics722_dedup=int(len(r722_dedup)),
    naics722_dedup_in_sf=int(r722_dedup["in_sf"].sum()), naics722_share_lacking_location=round(float(share_noloc), 4),
    naics722_admin_closed_dropped=int((reg["is722"] & adm_closed).sum()),
    lic_restaurant_dedup_in_sf=int(lic["in_sf"].sum()),
    pip_vs_field_agreement_registry=round(float(agree), 4),
    dph_restaurant_facilities=int(len(drest)), dph_restaurant_lacking_coords=int(drest["x"].isna().sum()),
    dph_broad_food_service=int(len(dbroad)), dph_inspection_window="2024-01-02 to present (dataset tvy3-wexg)",
    tracts=int(len(tr)), tracts_snapped_to_nearest_polygon=[dict(GEOID=g, pop=int(pp)) for g, pp in zip(un["GEOID"], un["B01003_E001"])],
    city_area_from_polygons_sqmi=round(city_utm.area / MI ** 2, 2), city_area_gazetteer_land_sqmi=round(float(tr["ALAND_SQMI"].sum()), 2),
)
json.dump(stats, open(OUT + "_stats.json", "w"), indent=1)
print(json.dumps(stats, indent=1))
