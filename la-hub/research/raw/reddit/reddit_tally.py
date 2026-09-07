#!/usr/bin/env python3
"""Tally LA neighborhood mentions in the scraped Reddit corpus, split by vehicle-mode context,
and extract candidate quotes for qualitative review. Writes reddit_tally.json / reddit_quotes.jsonl / corpus_la.jsonl"""
import json, re, collections, datetime
D = "/tmp/claude-0/-home-user-manual/388ed474-de23-51b8-a42a-e9a5d51078e5/scratchpad/reddit"

PLACES = {
    "DTLA": r"\b(dtla|downtown la|downtown los angeles|(?<!long beach )(?<!burbank )(?<!glendale )(?<!pasadena )(?<!santa monica )(?<!culver city )downtown(?! (?:long beach|burbank|glendale|pasadena|santa monica|culver|san diego|la jolla|fullerton|anaheim|santa ana|riverside|san bernardino|ventura|oxnard|sacramento|san jose|seattle|chicago|phoenix|denver|austin|dallas|houston|miami|atlanta|portland|vegas|las vegas|brooklyn|manhattan|boston|philly|philadelphia|detroit|minneapolis|nashville|indianapolis|columbus|cleveland|pittsburgh|baltimore|orlando|tampa|charlotte|raleigh|st\\.? louis|kansas city|milwaukee|cincinnati|louisville|memphis|new orleans|oklahoma|tulsa|omaha|salt lake|boise|spokane|tucson|albuquerque|el paso|san antonio|fort worth|jacksonville|honolulu))|little tokyo|arts district|fashion district|south park|historic core|skid row|financial district|bunker hill|grand central market|crypto\\.com arena|staples center|la live)\b",
    "Koreatown": r"\b(koreatown|k-?town|wilshire/western|western ave|vermont ave|normandie)\b",
    "Westlake/MacArthur Park": r"\b(westlake|macarthur park|alvarado)\b",
    "Pico-Union": r"\b(pico[- ]union)\b",
    "USC/Exposition": r"\b(usc|exposition park|university park|figueroa corridor)\b",
    "Hollywood": r"\b((?<!north )(?<!west )(?<!n\\. )(?<!w\\. )hollywood(?! hills)|hollywood blvd|sunset strip|thai town|east hollywood)\b",
    "West Hollywood": r"\b(west hollywood|weho)\b",
    "Silver Lake/Echo Park": r"\b(silver ?lake|echo park|los feliz|atwater)\b",
    "Santa Monica/Venice": r"\b(santa monica|venice|marina del rey|playa)\b",
    "Westwood/UCLA": r"\b(westwood|ucla)\b",
    "Beverly Hills/Century City": r"\b(beverly hills|century city)\b",
    "Mid-City/Fairfax": r"\b(mid[- ]?city|fairfax|la brea|miracle mile|mid[- ]?wilshire|pico[- ]robertson)\b",
    "Culver City": r"\b(culver city)\b",
    "Pasadena": r"\b(pasadena)\b",
    "Glendale/Burbank": r"\b(glendale|burbank)\b",
    "Valley": r"\b(the valley|sfv|san fernando valley|van nuys|sherman oaks|studio city|north hollywood|noho|encino|northridge)\b",
    "Long Beach": r"\b(long beach)\b",
    "South LA": r"\b(south central|south la|south los angeles|inglewood|compton|watts|crenshaw)\b",
    "East LA/Boyle Heights": r"\b(boyle heights|east la|east los angeles|lincoln heights|highland park|eagle rock)\b",
    "SGV": r"\b(san gabriel|alhambra|monterey park|rosemead|arcadia|el monte)\b",
    "South Bay": r"\b(torrance|redondo|hermosa|manhattan beach|el segundo|gardena)\b",
}
TWO_WHEEL = re.compile(r"\b(e-?bike|ebike|bike|bicycle|scooter|moped|motorcycle|moto|sur-?ron|ruckus|two wheels|2 wheels|vespa|cycling|pedal)\b", re.I)
CAR = re.compile(r"\b(car|prius|gas|parking|park(ed|ing)|drive|driving)\b", re.I)
EARN = re.compile(r"\$\s?\d{2,3}(?:\.\d+)?\s?(?:/|per|an?)\s?(?:hr|hour)|\d{2,3}\s?(?:/|per|an?)\s?(?:hr|hour)|\$\s?\d{2,4}\s?(?:/|per|a)\s?(?:day|week|wk)", re.I)
THEFT = re.compile(r"\b(stolen|theft|robbed|robbery|steal|stole|jacked)\b", re.I)
LIVE = re.compile(r"\b(i live in|live in|living in|from|commute from|drive in from|based in)\s+([A-Z][\w\- ]{2,30})", re.I)

posts = [json.loads(l) for l in open(f"{D}/posts.jsonl")]
comments = []
try:
    comments = [json.loads(l) for l in open(f"{D}/comments.jsonl")]
except FileNotFoundError:
    pass
post_by_id = {p["id"]: p for p in posts}

def year(ts):
    try:
        return datetime.datetime.utcfromtimestamp(float(ts)).year
    except Exception:
        return None

docs = []
for p in posts:
    txt = f"{p.get('title') or ''}\n{p.get('selftext') or ''}"
    docs.append({"kind": "post", "id": p["id"], "sub": p.get("subreddit"), "text": txt, "score": p.get("score") or 0,
                 "year": year(p.get("created_utc")), "url": "https://www.reddit.com" + (p.get("permalink") or ""), "title": p.get("title")})
for c in comments:
    p = post_by_id.get(c["post_id"], {})
    docs.append({"kind": "comment", "id": c["id"], "sub": c.get("subreddit") or p.get("subreddit"), "text": c.get("body") or "",
                 "score": c.get("score") or 0, "year": year(c.get("created_utc")),
                 "url": "https://www.reddit.com" + (p.get("permalink") or "") + (c["id"] or ""), "title": p.get("title")})

place_re = {k: re.compile(v, re.I) for k, v in PLACES.items()}
tally = {k: collections.Counter() for k in PLACES}
quotes = []
la_docs = []
for d in docs:
    t = d["text"]
    hits = [k for k, rx in place_re.items() if rx.search(t)]
    if not hits:
        continue
    la_docs.append(d)
    tw = bool(TWO_WHEEL.search(t)); car = bool(CAR.search(t)); th = bool(THEFT.search(t)); er = EARN.findall(t)
    for k in hits:
        tally[k]["mentions"] += 1
        tally[k]["two_wheel_ctx"] += tw
        tally[k]["car_ctx"] += car
        tally[k]["theft_ctx"] += th
        tally[k]["earn_ctx"] += bool(er)
        tally[k][f"y{d['year']}"] += 1
        tally[k]["score_sum"] += max(0, d["score"])
    if tw or er or th:
        quotes.append({"places": hits, "two_wheel": tw, "car": car, "theft": th, "earnings": er[:3], "kind": d["kind"],
                       "sub": d["sub"], "year": d["year"], "score": d["score"], "url": d["url"], "title": d["title"],
                       "text": t[:900]})
quotes.sort(key=lambda q: (-(q["two_wheel"]), -q["score"]))
json.dump({k: dict(v) for k, v in tally.items()}, open(f"{D}/reddit_tally.json", "w"), indent=1)
with open(f"{D}/reddit_quotes.jsonl", "w") as fh:
    for q in quotes:
        fh.write(json.dumps(q) + "\n")
with open(f"{D}/corpus_la.jsonl", "w") as fh:
    for d in la_docs:
        fh.write(json.dumps(d) + "\n")
print(f"posts {len(posts)}  comments {len(comments)}  LA-place docs {len(la_docs)}  quotes {len(quotes)}")
print(f"{'place':28s} {'mentions':>8s} {'2wheel':>7s} {'car':>5s} {'theft':>5s} {'earn':>5s} {'2024+':>6s}")
for k, v in sorted(tally.items(), key=lambda kv: -kv[1]["mentions"]):
    recent = sum(n for yk, n in v.items() if yk.startswith("y") and yk[1:].isdigit() and int(yk[1:]) >= 2024)
    print(f"{k:28s} {v['mentions']:8d} {v['two_wheel_ctx']:7d} {v['car_ctx']:5d} {v['theft_ctx']:5d} {v['earn_ctx']:5d} {recent:6d}")
