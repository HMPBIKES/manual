import json, math, csv, re, collections, io, zipfile, os, datetime
import pandas as pd
from shapely.geometry import shape, Point, Polygon, MultiPolygon
from shapely.ops import unary_union, transform
from shapely.strtree import STRtree
from shapely.validation import make_valid
import pyproj

BASE = '/tmp/claude-0/-home-user-manual/388ed474-de23-51b8-a42a-e9a5d51078e5/scratchpad/market/'
RAW = BASE + 'raw/'
SITE_LAT, SITE_LON = 34.036264920367, -118.244701075709   # Census geocoder match for 768 Ceres Ave
SQM_PER_SQMI = 2589988.110336
MI = 1609.344
TODAY = datetime.date.today().isoformat()

fwd = pyproj.Transformer.from_crs('EPSG:4326', 'EPSG:26911', always_xy=True).transform  # NAD83 / UTM 11N
inv = pyproj.Transformer.from_crs('EPSG:26911', 'EPSG:4326', always_xy=True).transform
def to_m(g): return transform(fwd, g)
def sqmi(g_wgs): return to_m(g_wgs).area / SQM_PER_SQMI

# ---------------------------------------------------------------- polygons
def load_nc(fn, namef):
    d = json.load(open(fn))
    out = {}
    for f in d['features']:
        g = shape(f['geometry'])
        if not g.is_valid: g = make_valid(g)
        out[f['properties'][namef]] = g
    return out

nc_emp = load_nc(RAW + 'nc_Neighborhood_Council_Boundaries_2018_City_of_Los_Angeles.geojson', 'Name')  # EmpowerLA (official)
nc_bss = load_nc(RAW + 'nc_Neighborhood_Councils.geojson', 'NAME')  # LABSS copy (cross-check)

zone_def = {
    'Downtown':   ['Downtown Los Angeles', 'Arts District Little Tokyo'],
    'Koreatown':  ['Wilshire Center Koreatown'],
    'Westlake':   ['Westlake North', 'Westlake South'],
    'Pico-Union': ['Pico Union'],
    'USC':        ['Empowerment Congress North'],
}
bss_equiv = {'Downtown Los Angeles': 'DOWNTOWN LOS ANGELES', 'Arts District Little Tokyo': 'HISTORIC CULTURAL NC',
             'Wilshire Center Koreatown': 'WILSHIRE CENTER - KOREATOWN NC', 'Westlake North': 'WESTLAKE NORTH NC',
             'Westlake South': 'WESTLAKE SOUTH NC', 'Pico Union': 'PICO UNION NC',
             'Empowerment Congress North': 'EMPOWERMENT CONGRESS NORTH AREA NDC', 'Historic Cultural North': 'HISTORIC CULTURAL NORTH NC'}

polygons_used = []
for n, b in bss_equiv.items():
    polygons_used.append({'nc_name_empowerla': n, 'nc_name_labss': b,
                          'area_sqmi_empowerla': round(sqmi(nc_emp[n]), 3), 'area_sqmi_labss': round(sqmi(nc_bss[b]), 3),
                          'used_in_zone': next((z for z, ns in zone_def.items() if n in ns), 'not used (Chinatown; reported in notes only)')})

zones = {z: unary_union([nc_emp[n] for n in names]) for z, names in zone_def.items()}
site_pt = Point(SITE_LON, SITE_LAT)
site_m = to_m(site_pt)
for r in [1.5, 3, 5]:
    lab = f'radius_{r:g}mi'
    zones[lab] = transform(inv, site_m.buffer(r * MI, 256))
city = unary_union(list(nc_emp.values()))
if not city.is_valid: city = make_valid(city).buffer(0)
zones['City of LA'] = city
chinatown = nc_emp['Historic Cultural North']
zones_extra = {'Downtown+Chinatown': unary_union([zones['Downtown'], chinatown])}

# overlap check among selected NCs
sel = [nc_emp[n] for ns in zone_def.values() for n in ns]
tot_sel = sum(sqmi(g) for g in sel)
print('selected NC polygons: sum of individual areas %.3f vs union %.3f sq mi' % (tot_sel, sqmi(unary_union(sel))))
print('City union area %.2f sq mi; sum of NC areas %.2f' % (sqmi(city), sum(sqmi(g) for g in nc_emp.values())))

# ---------------------------------------------------------------- tracts
gaz_fn = RAW + '2024_gaz_tracts_06.txt' if os.path.exists(RAW + '2024_gaz_tracts_06.txt') else RAW + '2023_gaz_tracts_06.txt'
gaz = pd.read_csv(gaz_fn, sep='\t', dtype={'GEOID': str})
gaz.columns = [c.strip() for c in gaz.columns]
gaz = gaz[gaz['GEOID'].str.startswith('06037')].copy()
pop = pd.read_csv(RAW + 'acsdt5y2024-b01003_ca037tracts.dat', sep='|', dtype=str)
veh = pd.read_csv(RAW + 'acsdt5y2024-b25044_ca037tracts.dat', sep='|', dtype=str)
for df in (pop, veh):
    df['GEOID'] = df['GEO_ID'].str[-11:]
pop['POP'] = pd.to_numeric(pop['B01003_E001'], errors='coerce').fillna(0)
veh['HH'] = pd.to_numeric(veh['B25044_E001'], errors='coerce').fillna(0)
veh['HH0'] = pd.to_numeric(veh['B25044_E003'], errors='coerce').fillna(0) + pd.to_numeric(veh['B25044_E010'], errors='coerce').fillna(0)
tr = gaz.merge(pop[['GEOID', 'POP']], on='GEOID', how='left').merge(veh[['GEOID', 'HH', 'HH0']], on='GEOID', how='left')
print('tracts: gazetteer %d, with pop %d, pop total %d' % (len(gaz), tr['POP'].notna().sum(), tr['POP'].sum()))
tr['pt'] = [Point(x, y) for x, y in zip(tr['INTPTLONG'], tr['INTPTLAT'])]
tract_pts = list(tr['pt'])
pt_tree = STRtree(tract_pts)

def tract_stats(g):
    idx = pt_tree.query(g, predicate='contains')
    sub = tr.iloc[idx]
    return dict(population=int(sub['POP'].sum()), hh=int(sub['HH'].sum()), hh0=int(sub['HH0'].sum()),
                n_tracts=len(sub), aland_sqmi=sub['ALAND'].sum() / SQM_PER_SQMI)

# area-weighted cross-check with TIGER polygons
tiger_ok = False
try:
    import shapefile
    z = zipfile.ZipFile(RAW + 'tl_2024_06_tract.zip')
    names = {os.path.splitext(n)[1]: n for n in z.namelist()}
    rd = shapefile.Reader(shp=io.BytesIO(z.read(names['.shp'])), dbf=io.BytesIO(z.read(names['.dbf'])), shx=io.BytesIO(z.read(names['.shx'])))
    fields = [f[0] for f in rd.fields[1:]]
    tg, tgeo = [], []
    for sr in rd.iterShapeRecords():
        rec = dict(zip(fields, sr.record))
        if rec['GEOID'].startswith('06037'):
            g = shape(sr.shape.__geo_interface__)
            if not g.is_valid: g = make_valid(g)
            tg.append(rec['GEOID']); tgeo.append(g)
    tgeo_m = [to_m(g) for g in tgeo]
    tarea = [g.area for g in tgeo_m]
    tpop = dict(zip(tr['GEOID'], tr['POP']))
    ttree = STRtree(tgeo_m)
    tiger_ok = True
    print('TIGER tracts loaded for LA County:', len(tg))
except Exception as e:
    print('TIGER area-weighting unavailable:', e)

def pop_areaweighted(g):
    if not tiger_ok: return None
    gm = to_m(g)
    if not gm.is_valid: gm = make_valid(gm).buffer(0)
    idx = ttree.query(gm, predicate='intersects')
    tot = 0.0
    for i in idx:
        try:
            inter = tgeo_m[i].intersection(gm).area
        except Exception:
            inter = tgeo_m[i].buffer(0).intersection(gm.buffer(0)).area
        w = inter / tarea[i] if tarea[i] > 0 else 0
        tot += w * tpop.get(tg[i], 0)
    return int(round(tot))

# ---------------------------------------------------------------- restaurants, source A (Socrata NAICS)
soc = json.load(open(RAW + 'socrata_naics722_all.json'))
REST_NAICS = {'722110', '722211', '722212', '722213', '722511', '722513', '722514', '722515'}
BAR_NAICS = {'722410', '722400'}
def norm(s):
    s = (s or '').upper()
    s = re.sub(r'[^A-Z0-9 ]', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()
def soc_key(r):
    return (norm(r.get('dba_name') or r.get('business_name')), norm(r.get('street_address')))
def soc_pt(r):
    loc = r.get('location_1')
    if not loc or loc.get('latitude') in (None, '') or loc.get('longitude') in (None, ''): return None
    la, lo = float(loc['latitude']), float(loc['longitude'])
    if not (33.0 < la < 35.0 and -119.5 < lo < -117.0): return None
    return Point(lo, la)

def soc_set(codes):
    rows = [r for r in soc if (r.get('naics') or '') in codes]
    seen, uniq = set(), []
    for r in rows:
        k = soc_key(r)
        if k in seen: continue
        seen.add(k); uniq.append(r)
    pts = [(r, soc_pt(r)) for r in uniq]
    return dict(raw=len(rows), unique=len(uniq), with_xy=sum(1 for _, p in pts if p), pts=[(r, p) for r, p in pts if p])
socA = soc_set(REST_NAICS); socA_strict = soc_set({c for c in REST_NAICS if c.startswith('7225')}); socB = soc_set(BAR_NAICS)
for lab, s in [('restaurants (7221x/7222x/7225x)', socA), ('restaurants strict 7225x', socA_strict), ('drinking places 7224x', socB)]:
    print('Socrata %s: raw %d, unique name+addr %d, with coords %d (%.1f%% lacking)' % (lab, s['raw'], s['unique'], s['with_xy'], 100 * (1 - s['with_xy'] / s['unique'])))

# ---------------------------------------------------------------- restaurants, source B (DPH)
dph = json.load(open(RAW + 'dph_restaurant_market_inventory.geojson'))['features']
dph_rest = [f for f in dph if 'RESTAURANT' in (f['properties'].get('PE_DESCRIPTION') or '').upper()]
seen_fid, seen_key, dph_u = set(), set(), []
for f in dph_rest:
    p = f['properties']
    k1 = p.get('FACILITY_ID'); k2 = (norm(p.get('FACILITY_NAME')), norm(p.get('FACILITY_ADDRESS')), norm(p.get('FACILITY_CITY')))
    if k1 in seen_fid or k2 in seen_key: continue
    seen_fid.add(k1); seen_key.add(k2); dph_u.append(f)
def dph_pt(f):
    p = f['properties']; la, lo = p.get('FACILITY_LATITUDE'), p.get('FACILITY_LONGITUDE')
    if la is None or lo is None: return None
    if not (33.0 < la < 35.0 and -119.5 < lo < -117.0): return None
    return Point(lo, la)
dph_pts = [(f, dph_pt(f)) for f in dph_u]
dph_xy = [(f, p) for f, p in dph_pts if p]
print('DPH restaurant PEs: raw %d, unique facility %d, with valid coords %d (%.2f%% lacking)' % (len(dph_rest), len(dph_u), len(dph_xy), 100 * (1 - len(dph_xy) / len(dph_u))))

# ---------------------------------------------------------------- count points in polygons
def count_in(g, ptlist):
    tree = STRtree([p for _, p in ptlist])
    return len(tree.query(g, predicate='contains'))

rows = []
def build_row(zone, g, polygon_source, notes=''):
    ts = tract_stats(g)
    area = sqmi(g)
    nA = count_in(g, socA['pts']); nAs = count_in(g, socA_strict['pts']); nB = count_in(g, socB['pts']); nD = count_in(g, dph_xy)
    paw = pop_areaweighted(g)
    r = dict(zone=zone, polygon_source=polygon_source, area_sqmi=round(area, 2), population_acs=ts['population'], population_year='ACS 2020-2024 5-yr',
             zero_vehicle_hh_share=round(ts['hh0'] / ts['hh'], 3) if ts['hh'] else None,
             restaurants_naics7225=nA, drinking_places_naics7224=nB, restaurants_dph=nD,
             restaurants_per_sqmi=round(nD / area, 1), notes=notes,
             restaurants_socrata_strict7225_only=nAs, population_areaweighted_tiger=paw, n_tracts_by_centroid=ts['n_tracts'],
             tract_aland_sqmi=round(ts['aland_sqmi'], 2), socrata_restaurants_per_sqmi=round(nA / area, 1),
             pct_area_inside_city_of_la=round(100 * sqmi(g.intersection(city)) / area, 1))
    rows.append(r); return r

for z in ['Downtown', 'Koreatown', 'Westlake', 'Pico-Union', 'USC']:
    build_row(z, zones[z], 'LA GeoHub / EmpowerLA Neighborhood Council Boundaries: ' + ' + '.join(zone_def[z]))
for r_ in [1.5, 3, 5]:
    lab = f'radius_{r_:g}mi'
    build_row(lab, zones[lab], f'{r_:g}-mile circle around 768 Ceres Ave (34.03626,-118.24470), UTM 11N buffer')
build_row('City of LA', city, 'Union of all 99 Neighborhood Council polygons (EmpowerLA)')
# LA County (all tracts; DPH county-wide; Socrata not applicable)
cty_pop = int(tr['POP'].sum()); cty_hh = tr['HH'].sum(); cty_hh0 = tr['HH0'].sum(); cty_aland = tr['ALAND'].sum() / SQM_PER_SQMI
rows.append(dict(zone='LA County', polygon_source='All 2,498 LA County census tracts (Gazetteer ALAND, land only)', area_sqmi=round(cty_aland, 1),
                 population_acs=cty_pop, population_year='ACS 2020-2024 5-yr', zero_vehicle_hh_share=round(cty_hh0 / cty_hh, 3),
                 restaurants_naics7225=None, drinking_places_naics7224=None, restaurants_dph=len(dph_u),
                 restaurants_per_sqmi=round(len(dph_u) / cty_aland, 1),
                 notes='Socrata source covers City of LA only (N/A). DPH inventory excludes Pasadena, Long Beach and Vernon (own health depts). Area = land area of tracts incl. Channel Islands & mountains.',
                 restaurants_socrata_strict7225_only=None, population_areaweighted_tiger=None, n_tracts_by_centroid=len(tr),
                 tract_aland_sqmi=round(cty_aland, 1), socrata_restaurants_per_sqmi=None, pct_area_inside_city_of_la=None))

# extra: Chinatown variant (for notes only)
ct = build_row('Downtown+Chinatown (variant)', zones_extra['Downtown+Chinatown'], 'Downtown zone + Historic Cultural North NC (Chinatown)')
rows.pop()  # keep out of main CSV

# notes per row
soc_missing_share = 1 - socA['with_xy'] / socA['unique']
for r in rows:
    if r['zone'] == 'City of LA':
        r['notes'] = (f"Socrata counts here are geocoded rows only; citywide unique restaurants incl. rows without coordinates = {socA['unique']} "
                      f"(strict 7225x-only = {socA_strict['unique']}), drinking places = {socB['unique']}. City union of NC polygons (some NC edges overlap/gap slightly).")
    elif r['zone'].startswith('radius'):
        r['notes'] = (f"{r['pct_area_inside_city_of_la']}% of circle area is inside City of LA; Socrata (City-only) undercounts outside it. "
                      f"Socrata restaurant rows lack coordinates for {100*soc_missing_share:.1f}% of unique records citywide.")
    elif r['zone'] != 'LA County':
        r['notes'] = f"Socrata restaurant rows lack coordinates for {100*soc_missing_share:.1f}% of unique records citywide (not allocated to zones)."

cols = ['zone', 'polygon_source', 'area_sqmi', 'population_acs', 'population_year', 'zero_vehicle_hh_share', 'restaurants_naics7225',
        'drinking_places_naics7224', 'restaurants_dph', 'restaurants_per_sqmi', 'notes',
        'restaurants_socrata_strict7225_only', 'population_areaweighted_tiger', 'n_tracts_by_centroid', 'tract_aland_sqmi',
        'socrata_restaurants_per_sqmi', 'pct_area_inside_city_of_la']
pd.DataFrame(rows)[cols].to_csv(BASE + 'la_zones.csv', index=False)
print(pd.DataFrame(rows)[cols].to_string())
print('\nChinatown variant:', {k: ct[k] for k in ['area_sqmi', 'population_acs', 'restaurants_dph', 'restaurants_naics7225', 'population_areaweighted_tiger']})

# Socrata NAICS breakdown inside each zone
naics_break = {}
for z, g in zones.items():
    tree = STRtree([p for _, p in socA['pts']])
    idx = tree.query(g, predicate='contains')
    naics_break[z] = dict(collections.Counter(socA['pts'][i][0]['naics'] for i in idx))
dph_break = {}
for z, g in zones.items():
    tree = STRtree([p for _, p in dph_xy])
    idx = tree.query(g, predicate='contains')
    dph_break[z] = dict(collections.Counter(dph_xy[i][0]['properties']['PE_DESCRIPTION'] for i in idx))

notes = {
    'site_address': '768 Ceres Ave, Los Angeles, CA 90021',
    'site_latlon': [SITE_LAT, SITE_LON],
    'site_geocode': {'census_geocoder': [34.036264920367, -118.244701075709], 'nominatim_top': [34.0397338, -118.2414402],
                     'note': 'Census Public_AR_Current address-range match used; Nominatim returned street-level matches ~150-400 m away. Site falls inside Downtown Los Angeles NC.'},
    'date_accessed': TODAY,
    'sources': [
        {'name': 'City of LA Listing of Active Businesses (Socrata 6rrh-rzua)', 'url': 'https://data.lacity.org/resource/6rrh-rzua.json',
         'rows': {'naics_722_all': len(soc), 'naics_722_with_coords': sum(1 for r in soc if r.get('location_1')),
                  'restaurant_codes_raw': socA['raw'], 'restaurant_unique_name_addr': socA['unique'], 'restaurant_unique_with_coords': socA['with_xy'],
                  'strict_7225x_raw': socA_strict['raw'], 'strict_7225x_unique_with_coords': socA_strict['with_xy'],
                  'drinking_raw': socB['raw'], 'drinking_unique': socB['unique'], 'drinking_unique_with_coords': socB['with_xy']},
         'date_accessed': TODAY,
         'filters': "starts_with(naics,'722'); restaurants = NAICS in {722110,722211,722212,722213 (NAICS-2007 codes still used by most rows), 722511,722513,722514,722515 (NAICS-2012+)}; drinking places = 722410/722400; excluded 7223x (caterers, mobile food, food service contractors). Deduped on normalized (dba_name or business_name)+street_address. Coordinates from location_1 (lat rounded to 3 decimals in source).",
         'coverage': 'City of Los Angeles only (business tax registrations; includes some stale registrations).'},
        {'name': 'LA County DPH Environmental Health Restaurant and Market Inventory (07/01/2026 release)',
         'url': 'https://services.arcgis.com/RmCCgQtiZLDCtblq/arcgis/rest/services/Environmental_Health_Restaurant_and_Market_Inventory_33/FeatureServer/0/query',
         'hub_page': 'https://data.lacounty.gov/datasets/4f31c9a99e444a40a3806e3bbe7b5fdd',
         'rows': {'all': len(dph), 'restaurant_program_elements': len(dph_rest), 'restaurant_unique_facilities': len(dph_u), 'restaurant_unique_with_valid_coords': len(dph_xy)},
         'date_accessed': TODAY,
         'filters': "PE_DESCRIPTION contains 'RESTAURANT' (all seat-size and risk classes); FOOD MKT RETAIL rows excluded; deduped on FACILITY_ID then normalized name+address+city. Valid coords = within lat 33-35, lon -119.5 to -117.",
         'coverage': 'LA County excluding cities with their own health departments (Pasadena, Long Beach, Vernon).'},
        {'name': 'EmpowerLA Neighborhood Council Boundaries - City of Los Angeles (LA GeoHub)',
         'url': 'https://services5.arcgis.com/7nsPwEMP38bSkCjy/arcgis/rest/services/Neighborhood_Council_Boundaries_2018_City_of_Los_Angeles/FeatureServer/0/query?where=1%3D1&outFields=*&f=geojson',
         'rows': len(nc_emp), 'date_accessed': TODAY, 'filters': 'all 99 NC polygons; cross-checked against LABSS copy services1.arcgis.com/PTh9WC0Sf2WS7AAq/.../Neighborhood_Councils'},
        {'name': 'ACS 2020-2024 5-year table-based summary file, B01003 (total population) and B25044 (tenure by vehicles available)',
         'url': 'https://www2.census.gov/programs-surveys/acs/summary_file/2024/table-based-SF/data/5YRData/acsdt5y2024-b01003.dat (and -b25044.dat)',
         'rows': int(len(pop)), 'date_accessed': TODAY, 'filters': 'GEO_ID starting 1400000US06037 (LA County tracts). Census API (api.census.gov) refused key-less requests ("Missing Key"), so the FTP summary file was used instead.'},
        {'name': 'Census Gazetteer 2024 tracts (INTPTLAT/INTPTLONG, ALAND)', 'url': gaz_fn.replace(RAW, 'https://www2.census.gov/geo/docs/maps-data/data/gazetteer/2024_Gazetteer/'),
         'rows': int(len(gaz)), 'date_accessed': TODAY, 'filters': 'GEOID starts with 06037'},
        {'name': 'TIGER/Line 2024 tract polygons (area-weighted population cross-check)', 'url': 'https://www2.census.gov/geo/tiger/TIGER2024/TRACT/tl_2024_06_tract.zip',
         'rows': len(tg) if tiger_ok else 0, 'date_accessed': TODAY, 'filters': 'GEOID starts with 06037'},
        {'name': 'Census Geocoder (site geocode)', 'url': 'https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?address=768+Ceres+Ave+Los+Angeles+CA+90021&benchmark=Public_AR_Current&format=json', 'rows': 1, 'date_accessed': TODAY},
    ],
    'polygons_used': polygons_used + [
        {'zone': z, 'area_sqmi': round(sqmi(zones[z]), 3), 'components': zone_def.get(z, 'circle' if z.startswith('radius') else 'all NCs')} for z in zones],
    'usc_nc_check': 'USC campus point (34.0224,-118.2851) falls inside Empowerment Congress North Area NDC in both boundary files; that NC was used for the USC / University Park / Exposition Park zone.',
    'downtown_chinatown_variant': {k: ct[k] for k in ['area_sqmi', 'population_acs', 'population_areaweighted_tiger', 'restaurants_dph', 'restaurants_naics7225', 'drinking_places_naics7224']},
    'socrata_naics_breakdown_by_zone': naics_break,
    'dph_pe_breakdown_by_zone': dph_break,
    'caveats': [
        f"Socrata 'restaurants_naics7225' column actually counts NAICS 7221x/7222x/7225x (restaurants & other eating places under both NAICS-2007 and NAICS-2012+ coding): only {socA_strict['raw']} of {socA['raw']} restaurant rows citywide carry 7225x codes; a literal 7225-only filter would undercount ~7x. Strict counts are in restaurants_socrata_strict7225_only.",
        f"{100*soc_missing_share:.1f}% of unique Socrata restaurant records (and {100*(1-socB['with_xy']/socB['unique']):.1f}% of drinking places) have no coordinates and are not assigned to any zone/radius; zone counts from source A are therefore floors. DPH records are 100% geocoded ({len(dph_u)-len(dph_xy)} invalid).",
        "Socrata is a business-tax registry for the City of LA only: the 5-mile (and part of the 3-mile) circle extends into Vernon, Huntington Park, unincorporated East LA etc. where source A has no coverage; DPH (county-wide except Pasadena/Long Beach/Vernon) is used for restaurants_per_sqmi.",
        "Population is assigned by tract internal-point-in-polygon (ACS 2020-2024 5-yr); for small zones this is coarse, so an area-weighted TIGER interpolation is provided in population_areaweighted_tiger. The 'City of LA' polygon is the union of NC polygons, which has minor overlaps/slivers vs. the official city boundary. Downtown excludes Chinatown (Historic Cultural North NC); a variant with it is in the notes JSON.",
        "DPH restaurant PEs include institutional/hotel/stadium/school kitchens and every seating-size class, and Socrata includes stale registrations; neither source is a clean count of consumer-facing delivery restaurants. Source A vs B disagree by design; ratios between zones are more robust than absolute counts.",
    ],
    'failed_steps': [
        "Census API (api.census.gov/data/2023 and /2022 acs5) returned 'Missing Key' HTML for key-less requests; replaced by the ACS table-based summary-file .dat downloads (no key needed) — 2024 5-year vintage used (latest available).",
        "GeoHub service names 'Neighborhood_Councils_(Certified)' / 'Neighborhood_Council_Boundaries' were 400 / 'Token Required'; the EmpowerLA 'Neighborhood_Council_Boundaries_2018_City_of_Los_Angeles' service (public) was used instead, cross-checked with the LABSS copy.",
        "Socrata query with 'location IS NOT NULL' failed (column is 'location_1'); a literal NAICS starts_with('7225') filter returned only 1,325 rows because most rows use NAICS-2007 codes 722110/722211 — broadened to all 722 codes and re-filtered locally.",
        "LA Times Mapping L.A. neighborhoods GeoJSON was not needed (NC polygons sufficed) and was not fetched.",
    ],
}
json.dump(notes, open(BASE + 'la_zones_notes.json', 'w'), indent=1, default=str)
print('\nwrote la_zones.csv and la_zones_notes.json')
