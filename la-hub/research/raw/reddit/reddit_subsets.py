#!/usr/bin/env python3
"""Build per-area / per-topic subsets of the LA corpus (posts + comments) for reader agents."""
import json, re, os, collections
from reddit_tally import PLACES, TWO_WHEEL, CAR, EARN, THEFT, D
OUT = f"{D}/subsets"; os.makedirs(OUT, exist_ok=True)
docs = [json.loads(l) for l in open(f"{D}/corpus_la.jsonl")]
place_re = {k: re.compile(v, re.I) for k, v in PLACES.items()}
LA_MARK = re.compile(r"\b(los angeles|l\.a\.|\bLA\b|dtla|koreatown|k-?town|socal|california|santa monica|westwood|ucla|usc|silver ?lake|echo park|culver|inglewood|sfv|the valley|405|101|110|wilshire|sunset blvd|hollywood blvd|figueroa|alvarado|vermont ave|western ave|olympic blvd|pico blvd|skid row|little tokyo|arts district)\b", re.I)
OUT_STATE = re.compile(r"\b(florida|fl\b|miami|fort lauderdale|broward|tampa|orlando|arizona|az\b|phoenix|tempe|texas|tx\b|houston|dallas|austin|new york|nyc|brooklyn|long island|louisiana|baton rouge|new orleans|lafayette|shreveport|ohio|oregon|nashville|tennessee|seattle|chicago|denver|atlanta|las vegas|vegas)\b", re.I)
VEH = re.compile(r"\b(sur-?ron|talaria|ruckus|zuma|49cc|50cc|125cc|150cc|pcx|grom|moped|e-?moped|class ?3|28 ?mph|30 ?mph|35 ?mph|40 ?mph|45 ?mph|throttle|range|miles per charge|battery swap|swap(ping)? batter|charg(e|ing) (station|my|the)|lock(ed|ing)? (it|my|the) (bike|scooter))\b", re.I)
STAGE = re.compile(r"\b(hotspot|hot spot|ghost kitchen|cloud ?kitchen|colony|food (co|depot)|wait(ing)? (at|outside|in)|hang(ing)? out|park(ed|ing)? (at|outside|in front)|line of (drivers|dashers)|drivers (waiting|camped)|staging|meet ?up|gather)\b", re.I)
NIGHT = re.compile(r"\b(night|late|after dark|2 ?am|midnight|11 ?pm|10 ?pm)\b", re.I)
sets = collections.defaultdict(list)
for d in docs:
    t = d["text"]
    if not d["sub"] or d["sub"].lower() not in ("losangeles","asklosangeles","koreatown","dtla","losangelesbikes","ucla","usc","lalist"):
        if OUT_STATE.search(t) and not LA_MARK.search(t):
            continue  # likely out-of-state
    hits = [k for k, rx in place_re.items() if rx.search(t)]
    tw = bool(TWO_WHEEL.search(t)); th = bool(THEFT.search(t)); er = bool(EARN.search(t)); ve = bool(VEH.search(t)); st = bool(STAGE.search(t)); ni = bool(NIGHT.search(t))
    rec = dict(d); rec["places"] = hits; rec["flags"] = {"two_wheel": tw, "theft": th, "earn": er, "vehicle": ve, "staging": st, "night": ni}
    for k in hits:
        sets[f"area_{k.replace('/','_').replace(' ','_')}"].append(rec)
    if tw: sets["topic_two_wheel"].append(rec)
    if th: sets["topic_theft_safety"].append(rec)
    if er: sets["topic_earnings"].append(rec)
    if ve: sets["topic_vehicle_spec"].append(rec)
    if st: sets["topic_staging"].append(rec)
    if ni and (th or tw): sets["topic_night"].append(rec)
    if any(k in hits for k in ("Koreatown","Westlake/MacArthur Park","Pico-Union","USC/Exposition")):
        sets["area_KTOWN_WESTLAKE_PICOUNION_USC"].append(rec)
for k, v in sets.items():
    v.sort(key=lambda r: -(r.get("score") or 0))
    with open(f"{OUT}/{k}.jsonl", "w") as fh:
        for r in v: fh.write(json.dumps(r) + "\n")
print(f"{'subset':44s} {'docs':>6s} {'chars':>9s} {'posts':>6s} {'comments':>8s} {'2wheel':>6s}")
for k, v in sorted(sets.items(), key=lambda kv: -len(kv[1])):
    print(f"{k:44s} {len(v):6d} {sum(len(r['text']) for r in v):9d} {sum(1 for r in v if r['kind']=='post'):6d} {sum(1 for r in v if r['kind']=='comment'):8d} {sum(1 for r in v if r['flags']['two_wheel']):6d}")
