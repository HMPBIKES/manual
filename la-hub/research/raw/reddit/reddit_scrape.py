#!/usr/bin/env python3
"""Reddit scrape via headless Chromium (Playwright) using Reddit's public JSON endpoints.
Writes posts.jsonl / comments.jsonl / log.txt under OUT. Rate-limited, resumable."""
import asyncio, json, os, re, time, random
from playwright.async_api import async_playwright

OUT = "/tmp/claude-0/-home-user-manual/388ed474-de23-51b8-a42a-e9a5d51078e5/scratchpad/reddit"
os.makedirs(OUT, exist_ok=True)
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
FLAGS = ["--no-sandbox", "--disable-dev-shm-usage", "--ssl-version-max=tls1.2", "--disable-quic",
         "--disable-features=PostQuantumKyber,UseMLKEM,EncryptedClientHello"]
DELAY = 3.5  # seconds between requests
MAX_PAGES = 3          # 100 results per page
MAX_THREADS = 450      # comment threads to fetch

COURIER_SUBS = ["doordash_drivers", "UberEATS", "couriersofreddit", "grubhubdrivers", "doordash", "Sparkdriver"]
COURIER_QUERIES = [
    "los angeles", "LA bike", "LA ebike", "LA e-bike", "LA scooter", "LA moped", "LA motorcycle",
    "koreatown", "ktown", "DTLA", "downtown LA", "downtown los angeles", "hollywood", "west hollywood",
    "santa monica", "westwood", "USC", "silver lake", "echo park", "culver city", "pasadena", "long beach",
    "burbank", "glendale", "venice", "mid city", "boyle heights", "skid row", "beverly hills", "east LA",
    "south central", "LA hotspot", "LA zone", "LA best area", "LA market", "LA earnings", "LA per hour",
    "surron", "ruckus", "sur-ron",
]
LA_SUBS = ["LosAngeles", "AskLosAngeles", "Koreatown", "DTLA", "LosAngelesBikes", "UCLA", "USC", "LAlist"]
LA_QUERIES = ["doordash bike", "doordash ebike", "uber eats bike", "uber eats scooter", "delivery ebike",
              "delivery scooter", "delivery moped", "food delivery driver", "delivery driver bike",
              "doordash", "uber eats", "e-bike delivery", "surron delivery", "delivery rider"]
EBIKE_SUBS = ["ebikes", "ElectricScooters", "Surron", "electricmopeds", "Ebike", "mopeds"]
EBIKE_QUERIES = ["doordash los angeles", "uber eats los angeles", "delivery los angeles", "delivery LA",
                 "doordash LA", "koreatown", "DTLA delivery"]

LA_TERMS = re.compile(r"\b(los angeles|l\.a\.|\bLA\b|dtla|downtown|koreatown|k-?town|hollywood|santa monica|westwood|"
                      r"usc|ucla|silver ?lake|echo park|culver|pasadena|long beach|burbank|glendale|venice|mid[- ]?city|"
                      r"boyle heights|skid row|beverly|east la|south central|inglewood|torrance|sherman oaks|studio city|"
                      r"north hollywood|noho|van nuys|the valley|sfv|wilshire|vermont|figueroa|alvarado|westlake|"
                      r"pico|olympic|sunset blvd|melrose|fairfax|la brea|crenshaw|highland park|eagle rock|"
                      r"el segundo|marina del rey|playa|brentwood|century city|little tokyo|arts district|chinatown|"
                      r"compton|lynwood|huntington park|vernon|montebello|whittier|alhambra|monterey park|"
                      r"san gabriel|rosemead|el monte|pomona|santa clarita|palmdale|malibu|redondo|hermosa|manhattan beach)\b",
                      re.I)

def log(msg):
    line = f"{time.strftime('%H:%M:%S')} {msg}"
    print(line, flush=True)
    with open(f"{OUT}/log.txt", "a") as f:
        f.write(line + "\n")

class Fetcher:
    def __init__(self, page):
        self.page = page
        self.n = 0
    async def warm(self, sub="doordash_drivers"):
        try:
            await self.page.goto("https://old.reddit.com/", wait_until="domcontentloaded", timeout=45000)
            await asyncio.sleep(1.5)
            await self.page.goto(f"https://old.reddit.com/r/{sub}/", wait_until="domcontentloaded", timeout=45000)
            await asyncio.sleep(1.5)
            log(f"warmed cookies via old.reddit.com (r/{sub})")
        except Exception as e:
            log(f"warm failed: {str(e)[:80]}")
    async def get_json(self, url):
        for attempt in range(5):
            try:
                r = await self.page.goto(url, wait_until="domcontentloaded", timeout=45000)
                self.n += 1
                txt = await self.page.evaluate("document.body.innerText")
                if r and r.status == 200:
                    try:
                        return json.loads(txt)
                    except Exception:
                        log(f"non-json 200 for {url[:100]}")
                        return None
                if r and r.status == 429:
                    wait = 30 * (attempt + 1)
                    log(f"429 -> sleep {wait}s ({url[:80]})")
                    await asyncio.sleep(wait)
                    continue
                if r and r.status == 403:
                    log(f"403 -> re-warm (attempt {attempt}) for {url[:80]}")
                    m = re.search(r"/r/([^/]+)/", url)
                    await self.warm(m.group(1) if m else "doordash_drivers")
                    await asyncio.sleep(3 + 5 * attempt)
                    continue
                if r and r.status == 404:
                    log(f"404 for {url[:100]}")
                    return None
                await asyncio.sleep(5)
            except Exception as e:
                msg = str(e)
                if "HTTP_RESPONSE_CODE_FAILURE" in msg or "429" in msg:
                    wait = 45 * (attempt + 1)
                    log(f"rate-limited? sleep {wait}s then re-warm ({url[:70]})")
                    await asyncio.sleep(wait)
                    m = re.search(r"/r/([^/]+)/", url)
                    await self.warm(m.group(1) if m else "doordash_drivers")
                    continue
                log(f"ERR {msg[:100]} for {url[:80]}")
                await asyncio.sleep(10)
        return None

async def search(f, sub, q, seen, out):
    after = None
    got = 0
    for page_i in range(MAX_PAGES):
        url = (f"https://www.reddit.com/r/{sub}/search.json?q={q.replace(' ', '+')}&restrict_sr=1&sort=relevance"
               f"&t=all&limit=100&raw_json=1" + (f"&after={after}" if after else ""))
        d = await f.get_json(url)
        await asyncio.sleep(DELAY + random.random())
        if not d or "data" not in d:
            break
        ch = d["data"].get("children", [])
        for c in ch:
            p = c.get("data", {})
            pid = p.get("id")
            if not pid or pid in seen:
                continue
            seen.add(pid)
            rec = {k: p.get(k) for k in ("id", "subreddit", "title", "selftext", "score", "num_comments",
                                         "created_utc", "permalink", "url", "link_flair_text", "author", "upvote_ratio")}
            rec["query"] = q
            rec["search_sub"] = sub
            out.write(json.dumps(rec) + "\n")
            out.flush()
            got += 1
        after = d["data"].get("after")
        if not after or len(ch) < 100:
            break
    return got

def flatten_comments(children, post_id, depth, acc):
    for c in children:
        if c.get("kind") != "t1":
            continue
        d = c.get("data", {})
        acc.append({"id": d.get("id"), "post_id": post_id, "body": d.get("body"), "score": d.get("score"),
                    "created_utc": d.get("created_utc"), "author": d.get("author"), "depth": depth,
                    "subreddit": d.get("subreddit")})
        rep = d.get("replies")
        if isinstance(rep, dict):
            flatten_comments(rep.get("data", {}).get("children", []), post_id, depth + 1, acc)

async def main():
    posts_path = f"{OUT}/posts.jsonl"
    seen = set()
    if os.path.exists(posts_path):
        for line in open(posts_path):
            try:
                seen.add(json.loads(line)["id"])
            except Exception:
                pass
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True, executable_path="/opt/pw-browsers/chromium",
                                    proxy={"server": os.environ["HTTPS_PROXY"]}, args=FLAGS)
        ctx = await b.new_context(user_agent=UA, locale="en-US")
        page = await ctx.new_page()
        f = Fetcher(page)
        await f.warm()
        log(f"start; already have {len(seen)} posts")
        with open(posts_path, "a") as out:
            plan = [(s, q) for s in COURIER_SUBS for q in COURIER_QUERIES] + \
                   [(s, q) for s in LA_SUBS for q in LA_QUERIES] + \
                   [(s, q) for s in EBIKE_SUBS for q in EBIKE_QUERIES]
            done_path = f"{OUT}/done_queries.txt"
            done = set(open(done_path).read().splitlines()) if os.path.exists(done_path) else set()
            for i, (s, q) in enumerate(plan):
                key = f"{s}|{q}"
                if key in done:
                    continue
                got = await search(f, s, q, seen, out)
                with open(done_path, "a") as df:
                    df.write(key + "\n")
                log(f"[{i+1}/{len(plan)}] r/{s} '{q}' -> {got} new (total {len(seen)}, req {f.n})")
        # ---- comments for LA-relevant posts ----
        posts = [json.loads(l) for l in open(posts_path)]
        def relevant(p):
            txt = f"{p.get('title','')} {p.get('selftext','')}"
            if p["search_sub"] in LA_SUBS:
                return True
            return bool(LA_TERMS.search(txt))
        rel = [p for p in posts if relevant(p) and (p.get("num_comments") or 0) > 0]
        rel.sort(key=lambda p: -(p.get("num_comments") or 0) - (p.get("score") or 0))
        rel = rel[:MAX_THREADS]
        cpath = f"{OUT}/comments.jsonl"
        have = set()
        if os.path.exists(cpath):
            for line in open(cpath):
                try:
                    have.add(json.loads(line)["post_id"])
                except Exception:
                    pass
        log(f"comment fetch: {len(rel)} relevant threads, {len(have)} already done")
        with open(cpath, "a") as cout:
            for j, pst in enumerate(rel):
                if pst["id"] in have:
                    continue
                url = f"https://www.reddit.com/comments/{pst['id']}.json?limit=200&depth=4&raw_json=1"
                d = await f.get_json(url)
                await asyncio.sleep(DELAY + random.random())
                if not d or not isinstance(d, list) or len(d) < 2:
                    continue
                acc = []
                flatten_comments(d[1].get("data", {}).get("children", []), pst["id"], 0, acc)
                for c in acc:
                    cout.write(json.dumps(c) + "\n")
                cout.flush()
                if j % 20 == 0:
                    log(f"comments [{j+1}/{len(rel)}] {pst['id']} -> {len(acc)} (req {f.n})")
        log("DONE")
        await b.close()

asyncio.run(main())
