import json, math, itertools
from site_coverage import SITES, R, haversine, tw_share_at  # reuses loaded data (module re-runs its prints)
TOP = ["768 Ceres Ave (baseline, Warehouse District)","DTLA Financial (7th/Figueroa)","DTLA Historic Core (6th/Spring)",
       "DTLA South Park (Pico/Flower)","Fashion District (9th/Santee)","Westlake / MacArthur Park (7th/Alvarado)",
       "Pico-Union (Pico/Union)","Koreatown East (6th/Vermont)","Koreatown Core (Wilshire/Western)",
       "Koreatown South (Olympic/Normandie)","Hollywood (Hollywood/Vine)","East Hollywood (Sunset/Vermont)",
       "USC / Exposition (Figueroa/Jefferson)","Little Tokyo (1st/Central)","Silver Lake (Sunset/Silver Lake Blvd)"]
def cover(site_list, rad):
    n=0; idx=0.0
    for lat,lon in R:
        d=min(haversine(lat,lon,*SITES[s]) for s in site_list)
        if d<=rad:
            n+=1; idx+=tw_share_at(lat,lon)*math.exp(-d/1.5)
    return n, idx
rows=[]
for a,b in itertools.combinations(TOP,2):
    n2,i2=cover([a,b],2.0); n15,_=cover([a,b],1.5)
    rows.append((i2,n2,n15,a,b))
rows.sort(reverse=True)
print("best pairs by two-wheel index (2 mi union):")
for i2,n2,n15,a,b in rows[:15]:
    print(f"  idx {i2:6.1f}  rest2mi {n2:5d}  rest1.5mi {n15:5d} | {a[:34]:34s} + {b[:34]}")
print("\npairs including 768 Ceres:")
for i2,n2,n15,a,b in [r for r in rows if "Ceres" in r[3] or "Ceres" in r[4]][:6]:
    print(f"  idx {i2:6.1f}  rest2mi {n2:5d}  rest1.5mi {n15:5d} | {a[:34]:34s} + {b[:34]}")
print("\nsingle sites (2 mi):")
for s in TOP:
    n2,i2=cover([s],2.0); print(f"  idx {i2:6.1f}  rest2mi {n2:5d} | {s}")
json.dump([{"idx":r[0],"rest2mi":r[1],"rest1_5mi":r[2],"a":r[3],"b":r[4]} for r in rows[:40]], open("site_pairs.json","w"), indent=1)
