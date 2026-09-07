#!/usr/bin/env python3
"""Address-level coverage for the shortlisted listings: geocode via Census geocoder, then count DPH restaurants within radii
and LAPD robbery/assault within 0.5 mi. Output listing_coverage.json"""
import json, math, urllib.request, urllib.parse, ssl, os, time
RAW = "raw"
ADDRS = {
 "18th St btwn Grand & Olive (South Park) [approx: 1800 S Grand Ave]": "1800 S Grand Ave, Los Angeles, CA 90015",
 "1738 Cordova St (Pico-Union)": "1738 Cordova St, Los Angeles, CA 90007",
 "856 S Vermont Ave (Koreatown)": "856 S Vermont Ave, Los Angeles, CA 90005",
 "3651 Beverly Blvd (Koreatown N / East Hollywood)": "3651 Beverly Blvd, Los Angeles, CA 90004",
 "710 S Alvarado St (Westlake)": "710 S Alvarado St, Los Angeles, CA 90057",
 "2474 W Pico Blvd (Pico-Union)": "2474 W Pico Blvd, Los Angeles, CA 90006",
 "1824 S Magnolia Ave (Pico-Union)": "1824 S Magnolia Ave, Los Angeles, CA 90006",
 "525 S Los Angeles St (Historic Core)": "525 S Los Angeles St, Los Angeles, CA 90013",
 "121 E 6th St (Historic Core)": "121 E 6th St, Los Angeles, CA 90014",
 "726 E 12th St (Fashion District)": "726 E 12th St, Los Angeles, CA 90021",
 "951 Crocker St (Fashion District)": "951 Crocker St, Los Angeles, CA 90021",
 "785 E 14th St (Warehouse District)": "785 E 14th St, Los Angeles, CA 90021",
 "2473 Hunter St (Arts District S)": "2473 Hunter St, Los Angeles, CA 90021",
 "768 Ceres Ave (baseline)": "768 Ceres Ave, Los Angeles, CA 90021",
 "1312 S Boyle Ave (Boyle Heights)": "1312 S Boyle Ave, Los Angeles, CA 90023",
 "2832 E Olympic Blvd (Boyle Heights)": "2832 E Olympic Blvd, Los Angeles, CA 90023",
 "159 S Anderson St (Boyle Heights)": "159 S Anderson St, Los Angeles, CA 90033",
 "1350 E 41st St (Central-Alameda)": "1350 E 41st St, Los Angeles, CA 90011",
 "2440 Daly St (Lincoln Heights)": "2440 Daly St, Los Angeles, CA 90031",
 "2960 Leonis Blvd (Vernon)": "2960 Leonis Blvd, Vernon, CA 90058",
}
def geocode(a):
    u = "https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?" + urllib.parse.urlencode({"address": a, "benchmark": "Public_AR_Current", "format": "json"})
    for i in range(3):
        try:
            with urllib.request.urlopen(u, timeout=40) as r:
                d = json.load(r)
            m = d["result"]["addressMatches"]
            if m:
                c = m[0]["coordinates"]; return float(c["y"]), float(c["x"]), m[0]["matchedAddress"]
            return None
        except Exception as e:
            time.sleep(3)
    return None
def hav(a,b,c,d):
    R=3958.8;p1,p2=math.radians(a),math.radians(c);x=math.sin((p2-p1)/2)**2+math.cos(p1)*math.cos(p2)*math.sin(math.radians(d-b)/2)**2;return 2*R*math.asin(math.sqrt(x))
gj=json.load(open(f"{RAW}/dph_restaurant_market_inventory.geojson"))
feats=gj['features']; p0=feats[0]['properties']
pe_key=next((k for k in p0 if 'PE_DESC' in k.upper() or k.upper()=='PE_DESCRIPTION'),None)
name_key=next((k for k in p0 if k.upper() in ('FACILITY_NAME','NAME')),None)
addr_key=next((k for k in p0 if 'ADDRESS' in k.upper()),None)
rest={}
for ft in feats:
    p=ft['properties']
    if 'RESTAURANT' not in str(p.get(pe_key,'')).upper(): continue
    g=ft.get('geometry')
    if not g or g.get('type')!='Point': continue
    lon,lat=g['coordinates'][:2]
    if not (33.5<lat<34.9 and -119<lon<-117.5): continue
    rest.setdefault((str(p.get(name_key,'')).strip().upper(), str(p.get(addr_key,'')).strip().upper()),(lat,lon))
R=list(rest.values())
crimes=[(float(r['lat']),float(r['lon']),r['crm_cd']) for r in json.load(open(f"{RAW}/lapd_crimes_2023_24q1.json")) if r.get('lat') and float(r['lat'])!=0]
out=[]
for label,a in ADDRS.items():
    g=geocode(a)
    if not g:
        out.append({"listing":label,"geocode":"FAILED"}); print("FAILED", label); continue
    lat,lon,matched=g
    d=[hav(lat,lon,x,y) for x,y in R]
    rec={"listing":label,"matched":matched,"lat":round(lat,5),"lon":round(lon,5)}
    for rad in (1.0,1.5,2.0,3.0): rec[f"rest_{rad}mi"]=sum(1 for v in d if v<=rad)
    near=[c for c in crimes if hav(lat,lon,c[0],c[1])<=0.5]
    rec["robbery_0.5mi"]=sum(1 for c in near if c[2] in ('210','220')); rec["assault_0.5mi"]=sum(1 for c in near if c[2]=='230'); rec["bike_stolen_0.5mi"]=sum(1 for c in near if c[2]=='480')
    out.append(rec); print(f"{label[:52]:52s} r1={rec['rest_1.0mi']:5d} r1.5={rec['rest_1.5mi']:5d} r2={rec['rest_2.0mi']:5d} r3={rec['rest_3.0mi']:5d} rob.5={rec['robbery_0.5mi']:4d} asl.5={rec['assault_0.5mi']:4d} bike.5={rec['bike_stolen_0.5mi']:3d}  ({lat:.4f},{lon:.4f})")
    time.sleep(1)
json.dump(out,open("listing_coverage.json","w"),indent=1)
