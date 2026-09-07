import json, re, collections, datetime, sys
sys.path.insert(0, '/tmp/claude-0/-home-user-manual/388ed474-de23-51b8-a42a-e9a5d51078e5/scratchpad/reddit')
from tag import PL, CAR, NOT_LA

D = '/tmp/claude-0/-home-user-manual/388ed474-de23-51b8-a42a-e9a5d51078e5/scratchpad/reddit/'
corp = json.load(open(D + 'corpus_tagged.json'))
posts = {}
for l in open(D + 'posts.jsonl'):
    p = json.loads(l)
    if not p.get('permalink') or p.get('score') is None or not p.get('subreddit'): continue  # junk subreddit-list rows from r/LosAngelesBikes
    posts[p['id']] = p
def ptxt(p): return (p['title'] or '') + '\n' + (p.get('selftext') or '')
def pyr(p): return datetime.datetime.utcfromtimestamp(p['created_utc']).year
def purl(p): return 'https://www.reddit.com' + p['permalink']

# ---------- LA verification (stricter than the original tally) ----------
VERIFY = re.compile(r"\b(los angeles|l\.a\.|dtla|downtown la|koreatown|k-?town|socal|southern california|california|the 405|405 freeway|the 101|the 110|the 10 fwy|santa monica|westwood|ucla|usc|san fernando valley|sfv|silver ?lake|echo park|culver city|inglewood|beverly hills|west hollywood|weho|burbank|glendale|pasadena|long beach|compton|torrance|el segundo|marina del rey|playa vista|playa del rey|brentwood|sawtelle|wilshire|melrose|sunset blvd|sunset boulevard|figueroa|alvarado|macarthur park|skid row|boyle heights|east la|south central|south la|san gabriel|alhambra|monterey park|van nuys|sherman oaks|studio city|north hollywood|noho|encino|northridge|reseda|canoga|woodland hills|calabasas|malibu|pacific palisades|century city|mid-?city|fairfax|los feliz|highland park|eagle rock|atwater|whittier|downey|norwalk|lakewood|cerritos|hawthorne|gardena|san pedro|redondo|hermosa|manhattan beach|lax|hollywood hills|hollywood blvd|hollywood ?(/|and|&) ?highland|griffith|dodger|staples|crypto\.com|la live|arts district|little tokyo|fashion district|leimert|crenshaw|baldwin hills|westchester|mar vista|west la|west los angeles|la brea|la cienega|the grove|farmers market|cahuenga|vermont ave|normandie|la county|los angeles county|orange county|irvine|anaheim|huntington beach|riverside|san bernardino|santa clarita|palmdale|lancaster|pomona|west covina|azusa|glendora|la verne|claremont|rancho cucamonga|el monte|baldwin park|rosemead|montebello|pico rivera|south gate|huntington park|lynwood|paramount|bellflower|costa mesa|newport|laguna|fullerton|santa ana|buena park|la habra|la mirada|palos verdes|watts|prop ?22|thai town|little armenia|hollywood,? ca(lifornia)?\b|lausd|lapd|angeleno)", re.I)
CORE = re.compile(r"\b(los angeles|l\.a\.|dtla|downtown la|koreatown|k-?town|socal|southern california|california|santa monica|ucla|usc|west hollywood|weho|san fernando valley|beverly hills|prop ?22|lapd|lausd|hollywood,? ca)\b", re.I)
MANUAL_VERIFIED = {'dm0jhp', 'djzc4p', 'ffvecm'}  # Hollywood e-scooter series; companion posts e9pn3f / fah04r say "Hollywood California"/"Hollywood CA"
MANUAL_EXCLUDE = {'1c00k1q', 'wkb5w3', '1s1uuhx', 'hmouo7', '123b3b4', 'f2k4yb', '9pgcx2', 'r2oy6v', '1kkammj', 'id69eg', 'c4isga', '1dkpsbh', '1mcr4ze', '1ndoo0i', '1i8c1xo', 'klue13', '1sehgnu', '12ukvr2', 'w1rsi0', '1dmdxe9', '1ktc3qp'}
def verified(doc):
    if doc['id'] in MANUAL_EXCLUDE: return False
    if doc['id'] in MANUAL_VERIFIED: return True
    t = doc['text']
    if not VERIFY.search(t): return False
    if NOT_LA.search(t) and not CORE.search(t): return False
    return True
for c in corp: c['ver'] = verified(c)
by_id = {c['id']: c for c in corp}

AREAS = ['DTLA', 'Westlake/MacArthur Park', 'Pico-Union', 'Koreatown', 'USC/Exposition', 'Hollywood/East Hollywood',
         'Silver Lake/Echo Park', 'Westwood/UCLA', 'Santa Monica/Venice', 'West Hollywood', 'Culver City', 'Mid-City/Fairfax',
         'Beverly Hills/Century City', 'Valley/SFV', 'Glendale/Burbank', 'Pasadena', 'South LA', 'South Bay', 'Long Beach', 'East LA/Boyle Heights']

# ---------- curated two-wheel docs (courier's OWN two-wheel vehicle; LA-verified; read in full) ----------
# id: (areas, vehicle, status, sentiment)   status: active|planned|considering|question
TW = {
 'nq3ho0': (['DTLA'], 'e-scooter (standing)', 'active', 'positive'),
 'ujwab7': (['DTLA'], 'bike + scooter mode', 'active', 'negative'),
 '12vic27': (['DTLA'], 'bicycle/scooter mode', 'active', 'negative'),
 'syz06v': (['DTLA'], 'regular bike -> wants e-bike/e-scooter', 'active', 'mixed'),
 'srp8mj': (['DTLA'], 'scooter', 'active', 'negative'),
 '1dmru9y': (['DTLA'], 'bicycle (non-electric)', 'active', 'mixed'),
 'ps4sre': (['DTLA'], 'bike', 'active', 'positive'),
 'ift0z2': (['DTLA', 'Culver City'], 'bike', 'active', 'positive'),
 'avp2wa': (['DTLA', 'Westwood/UCLA', 'Hollywood/East Hollywood'], 'bicycle', 'active', 'positive'),
 'igu9bi': (['DTLA'], 'bicycle', 'active', 'mixed'),
 'q0yp2w': (['DTLA'], 'bike/foot', 'active', 'mixed'),
 'er4dw9': (['DTLA'], 'bicycle', 'active', 'negative'),
 'exguvj': (['DTLA', 'Santa Monica/Venice', 'Glendale/Burbank'], 'fixie bicycle', 'planned', 'mixed'),
 'hadavv': (['DTLA'], 'bike', 'question', 'mixed'),
 'nqiyyx': (['DTLA'], 'bike (part-time)', 'planned', 'mixed'),
 '1ce67b8': (['DTLA'], 'e-scooter (standing)', 'planned', 'mixed'),
 '191gamv': (['DTLA'], 'e-bike (Dirwin)', 'planned', 'mixed'),
 '14ah15y': (['DTLA'], 'Ninebot e-scooter', 'planned', 'mixed'),
 'xmdxgz': (['DTLA'], 'e-bike vs Honda Ruckus/Yamaha Zuma', 'considering', 'mixed'),
 'plw6fe': (['DTLA'], 'bike/foot/scooter', 'planned', 'mixed'),
 'brglc9': (['DTLA'], 'bicycle', 'question', 'mixed'),
 'pvyfqo': (['DTLA'], 'foot vs bicycle', 'question', 'mixed'),
 '1qlhg3s': (['DTLA', 'Hollywood/East Hollywood'], 'bike + bus', 'planned', 'mixed'),
 'dm5uhi': (['DTLA', 'Glendale/Burbank'], '49cc gas scooter', 'planned', 'mixed'),
 'udhb8g': (['DTLA', 'Pasadena'], 'e-bike (Grubhub app had only car/motorcycle)', 'planned', 'negative'),
 '11khbg4': (['Hollywood/East Hollywood', 'Silver Lake/Echo Park', 'Koreatown', 'DTLA'], 'bike (considering, parking)', 'considering', 'mixed'),
 '7u8jh1': (['DTLA', 'Beverly Hills/Century City', 'Hollywood/East Hollywood'], 'bicycle', 'active', 'positive'),
 '1dnmppt': (['DTLA'], 'e-bike (international student)', 'planned', 'mixed'),
 '1tydibj': (['DTLA'], '72V 1000W e-scooter/e-moped', 'planned', 'mixed'),
 'ur25fd': (['Westwood/UCLA'], 'Ninebot G30P e-scooter (Duffl store fleet)', 'active', 'mixed'),
 'wmx6he': (['Westwood/UCLA'], 'bicycle (Citi Bike)', 'question', 'mixed'),
 '18i6zgk': ([], 'e-bike RENTAL for delivery (asks for LA rental companies)', 'planned', 'mixed'),
 'dm0jhp': (['Hollywood/East Hollywood'], 'e-scooter (standing)', 'active', 'positive'),
 'djzc4p': (['Hollywood/East Hollywood'], 'scooter', 'active', 'positive'),
 'e9pn3f': (['Hollywood/East Hollywood'], 'big electric scooters', 'active', 'positive'),
 'fah04r': (['Hollywood/East Hollywood'], 'e-scooter', 'active', 'positive'),
 'ffvecm': (['Hollywood/East Hollywood'], 'e-scooter', 'active', 'positive'),
 'piraz3': (['Hollywood/East Hollywood'], 'bicycle', 'question', 'mixed'),
 'pvdxq6': (['Hollywood/East Hollywood'], 'bicycle', 'active', 'negative'),
 '1kyp7be': (['Valley/SFV', 'West Hollywood', 'Hollywood/East Hollywood'], 'bicycle', 'active', 'mixed'),
 '1f9x83i': (['Hollywood/East Hollywood', 'Glendale/Burbank', 'Valley/SFV'], 'bike', 'planned', 'negative'),
 '1ke5hch': (['Culver City', 'Santa Monica/Venice', 'Hollywood/East Hollywood'], 'road bike -> e-bike (currently car)', 'considering', 'mixed'),
 'f9p8t5': (['Silver Lake/Echo Park'], 'bike', 'active', 'negative'),
 'iowfiq': (['Koreatown'], 'bicycle mode', 'active', 'negative'),
 '162vejl': (['Koreatown'], 'bike', 'question', 'mixed'),
 '10k0vso': (['West Hollywood'], 'bike', 'planned', 'mixed'),
 '7sdaho': (['West Hollywood', 'Beverly Hills/Century City'], 'bicycle (bike messenger)', 'active', 'mixed'),
 '1gn3r1q': (['Santa Monica/Venice'], 'e-bike', 'considering', 'positive'),
 '1d5qonh': (['Santa Monica/Venice'], 'e-bike', 'active', 'positive'),
 '1e612mu': (['Santa Monica/Venice'], 'e-bike', 'active', 'positive'),
 'fj5pr9': (['Santa Monica/Venice', 'Pasadena'], 'bicycle', 'active', 'mixed'),
 '15dae0o': (['USC/Exposition'], 'bike', 'planned', 'mixed'),
 'rkx1qz': (['Valley/SFV'], 'bike or car', 'considering', 'mixed'),
 'zoqc22': (['Valley/SFV'], 'Unagi e-scooter + Metro bus', 'active', 'positive'),
 '1iwx1s0': (['Valley/SFV'], 'bicycle', 'question', 'mixed'),
 'uwesb7': (['Glendale/Burbank'], 'gas scooter/moped', 'active', 'mixed'),
 '4ptffv': (['Pasadena'], 'bicycle', 'planned', 'mixed'),
 '84qfz0': (['Pasadena'], 'e-scooter', 'active', 'positive'),
 'obd8b4': (['South Bay'], 'e-bike 20+ mph', 'planned', 'mixed'),
 # LA-wide, area unspecified
 '7t0m96': ([], 'bicycle', 'active', 'positive'),
 'kz19g9': ([], 'e-bike, 3 apps', 'active', 'positive'),
 '10wb6ye': ([], 'bicycle', 'question', 'mixed'),
 'sft6h6': ([], 'scooter/motorcycle', 'considering', 'mixed'),
 '1v45xof': ([], 'cheap e-scooter', 'planned', 'mixed'),
 'ex3goz': ([], 'e-bike', 'planned', 'mixed'),
 'cmgyui': ([], 'motorcycle', 'active', 'positive'),
 '144jb34': ([], 'bicycle (Chicago courier considering LA)', 'considering', 'mixed'),
 'q0lu13': ([], 'bicycle (no option on Grubhub LA)', 'planned', 'negative'),
 '4pqv83': ([], 'bicycle', 'planned', 'mixed'),
 '1nu0ot9': ([], 'e-bike', 'active', 'negative'),
 '16v4et6': ([], 'bike -> 49cc motor scooter', 'active', 'mixed'),
 'm9kmek': ([], 'Artomoto enclosed motorcycle rental', 'considering', 'mixed'),
 '1fmnd57': ([], 'motorcycle', 'active', 'mixed'),
 '1czczag': ([], 'e-bike (video)', 'active', 'positive'),
 '10y11ow': ([], 'Honda Monkey 125cc', 'planned', 'mixed'),
 '1lcn2d4': ([], '40+ mph e-bike marked as car', 'active', 'positive'),
 '1daqn0k': ([], 'e-bike vs car', 'considering', 'mixed'),
 '1dizbwm': ([], 'electric bicycle', 'active', 'negative'),
 'tahh6s': ([], 'bike courier', 'considering', 'mixed'),
 '15rop35': ([], 'bike delivery apps', 'active', 'negative'),
}
CROSSPOSTS = {'syz06v': ['syyzri', 'syz2gj'], '1ke5hch': ['1ke5hv7', '1ke5gt4'], '10k0vso': ['10k0wio'], 'rkx1qz': ['rkx2s2'], '15dae0o': ['15cydh0'],
              '1czczag': ['1d1abiy', '1cmgzlb', '1czcx3m', '1czcyi7', '1cr31lo', '1d84sf6', '1dw5p1l', '1dtfkmh', '1dkyzy1', '1cupbqg', '1di5ut3', '1dh1p5h', '1dg0spl', '1ddzzv5', '1dbbri7', '1d84py2', '1d24p1m', '1d24ni9', '1cy7sod', '1cw2n8c', '1cw2k42', '1cupamb', '1co2s0e', '1d1ac05', '1csfsiu']}
OBSERVATIONAL = {  # two-wheel presence reported by others / not courier's own vehicle
 'dcno96': 'Beverly Hills "drivers" use Bird scooters around busy areas',
 '1hcdfx9': 'one of ~9 dashers camping at an LA hotspot restaurant was "laying down on his motorcycle"',
 'igu9bi': 'first-timer saw three other food-delivery bikers in Downtown LA, all with delivery backpacks',
 'c1xrog': 'r/LosAngeles: scooter sidewalk riding "5x more popular than street riding at least in K-town/DTLA" (LAPD ticketing)',
 '17074h9': 'Phoenix customer: bicycle delivery "works in places like NYC or Downtown LA"',
 '1ra98ko': 'Riverside e-scooter courier: "in LA and NY people can do alright on electric scooters and bikes"',
 '1hpwtns': 'r/LosAngeles: Figueroa & Expo restaurant row, Postmates drivers park in the median, new bike-lane bollards',
 'j9vs4j': 'Culver City courier hit by a sidewalk e-scooter rider while waiting outside a restaurant',
 'buha32': 'r/ucla 2019: a delivery service recruiting riders for "Westwood rides into UCLA, but on electric scooters"',
 '1isnll6': 'r/ucla 2025 (42 upvotes): joke post confirming Duffl (student-run 10-minute delivery) runs on standing scooters in Westwood',
 'yug8io': 'r/ebikes: "all the videos I watch online of bike delivery people has them in downtown cities like Chicago or LA"',
}

def doc(i):
    if i in by_id:
        c = by_id[i]; return dict(id=i, sub=c['sub'], year=c['year'], score=c['score'], url=c['url'], text=c['text'])
    p = posts[i]; return dict(id=i, sub=p['subreddit'], year=pyr(p), score=p['score'], url=purl(p), text=ptxt(p))

def norm(s): return re.sub(r'\s+', ' ', s.replace('\u2019', "'").replace('\u2018', "'").replace('\u201c', '"').replace('\u201d', '"')).strip()
def Q(i, quote, why=None):
    d = doc(i)
    assert norm(quote) in norm(d['text']), f'QUOTE NOT VERBATIM in {i}: {quote[:60]}'
    assert len(quote) <= 300, f'quote too long {i} {len(quote)}'
    o = dict(quote=quote, url=d['url'], sub='r/' + d['sub'], year=d['year'], score=d['score'])
    if why: o['why_it_matters'] = why
    return o

# ---------- area ranking ----------
area_docs = {a: [c for c in corp if c['ver'] and PL[a].search(c['text'])] for a in AREAS}
tw_by_area = collections.defaultdict(list)
for i, (areas, veh, st, sen) in TW.items():
    for a in areas: tw_by_area[a].append(i)

AREA_NOTES = {
 'DTLA': dict(sent='mixed', conf='medium', why="By far the most two-wheel courier discussion of any LA area (29 unique posts, 2017-2026): riders on bicycles, standing e-scooters, Ninebot, a 72V e-moped and a 49cc scooter all work or plan to work DTLA; the top-scoring post in the whole corpus (1,172 upvotes) is a car-to-e-scooter switch in Downtown LA, and an r/dtla bicycle courier found DTLA busier than Beverly Hills or Hollywood. Recurring complaints: bicycle mode gets almost no orders (only scooter/car mode does), orders get sent far outside the core, inclines are tiring on a pedal bike, homeless encounters, and volume has been thin since 2020.", samples=['nq3ho0', '7u8jh1', 'ujwab7']),
 'Westlake/MacArthur Park': dict(sent='none', conf='low', why="Only 1 LA-verified courier-sub doc mentions Westlake/MacArthur Park (a car driver passing through) plus one r/AskLosAngeles resident post worrying about bike theft near the park; none describe two-wheel delivery there. The neighborhood sits inside the Hollywood-Silverlake/Koreatown-DTLA zones riders describe but is never named as a base.", samples=['g5xv03', '5px3e9']),
 'Pico-Union': dict(sent='none', conf='low', why="Three docs: one East Hollywood driver who sometimes ends up in Pico-Union, and two posts naming the ghost-kitchen hub at 1842 W Washington Blvd (CloudKitchens, ~30 restaurants) where all-app drivers cluster (inferred location: Pico-Union/West Adams edge). No two-wheel rider mentions.", samples=['12i4jje', '1245m4q', '8n99nv']),
 'Koreatown': dict(sent='negative', conf='low', why="Small count (<5 two-wheel docs). A 2020 screenshot of Koreatown morning bicycle mode is captioned 'depressing'; a 2023 rider who just moved to K-town asks if bike delivery is doable; a Hollywood/Silverlake driver notes the DoorDash zone includes Koreatown and considers a bike for parking. Car drivers report bad reception, tip-baits and 'not worth it' vs Santa Monica; the Sweetgreen Koreatown hotspot is a closed store.", samples=['iowfiq', '162vejl', '11khbg4']),
 'USC/Exposition': dict(sent='none', conf='low', why="One USC grad student plans to deliver by bike and asks about safety; car dashers say the USC area 'at least gets some orders' but tips are ~$1 because customers are students; DoorDash created a 'USC island' zone in 2019; Grand Food Depot (358 W 38th St) ghost kitchen and the Figueroa/Expo restaurant row are pickup clusters.", samples=['15dae0o', '1mgovuq', '1245m4q']),
 'Hollywood/East Hollywood': dict(sent='positive', conf='medium', why="Second-largest two-wheel cluster (14 posts). A 2019-2020 rider series on 'big electric scooters' in Hollywood reports 'unicorn' orders and $5 peak pay 'all done on scooter'; car drivers in the Hollywood-Silverlake DoorDash zone say Silverlake is 'flooded with orders' while Beverly Hills is dead; downsides are Hollywood Hills climbs on a pedal bike and post-2023 saturation ($8/hr peak-hour reports).", samples=['dm0jhp', '1mottyz', 'pvdxq6']),
 'Silver Lake/Echo Park': dict(sent='mixed', conf='low', why="Only 2 two-wheel docs: a bike courier says Silver Lake tippers are cheap and 'biking up some of those curvy hills is no joke'; the Hollywood-Silverlake zone is repeatedly described (by car drivers) as the busy half of Hollywood. Echo Park/Dodger Stadium traffic and Baxter St hills are complaints.", samples=['f9p8t5', '1mottyz', 'nzb8ga']),
 'Westwood/UCLA': dict(sent='mixed', conf='low', why="Three two-wheel docs plus a student-run scooter fleet: a bicycle dasher names 'Westwood blvd x Ohio Ave' as one of only two bike hotspots (with 6th & Spring DTLA); Duffl's Westwood couriers ride Ninebot G30P standing scooters on 3-hour shifts and say the scooters 'break constantly' on hilly, broken roads; a student asks if Westwood is compact enough to dash on a Citi Bike. Car drivers complain of UCLA dorm/hospital runs with no parking, red-zone tickets, hills, $3 incentives nobody takes, and hour-long waits.", samples=['avp2wa', 'ur25fd', '1t5n6cg']),
 'Santa Monica/Venice': dict(sent='positive', conf='medium', why="Six two-wheel docs, the most positive e-bike sentiment in the corpus: two 2024 e-bike riders cite the Santa Monica Prop 22 floor (~$20-21/hr active) and 'bike lanes everywhere'; a Pasadena bicyclist rides all the way to SM to dash. Car drivers call SM the worst place to dash (traffic, parking, cops) and report heavy saturation ($14-15 for 5-7.5 hrs in 2024-25).", samples=['1e612mu', '1d5qonh', 'e8om7y']),
 'West Hollywood': dict(sent='mixed', conf='low', why="Three two-wheel docs: a 2018 night bike messenger (6pm-midnight) repeatedly stopped by LAPD in BH/WeHo, a NYC bike courier planning to work WeHo, and a Valley bicyclist who ventures into WeHo/Hollywood. Car drivers historically earned $18-30/hr here (2024) but 20-driver pileups at popular restaurants and dead afternoons are common.", samples=['7sdaho', '10k0vso', '1gmn1zo']),
 'Culver City': dict(sent='mixed', conf='low', why="Two two-wheel docs (a DTLA bike dasher asking about Culver, and a car driver in Culver/SM/Hollywood considering an e-bike). Car drivers call the Culver City zone slow (urban 'donut'), and roam Venice Blvd (Robertson-Sepulveda) and Palms (Overland-National) between pings; Culver City Cuisine ghost kitchen is a pickup cluster.", samples=['ift0z2', '1c10313', '1245m4q']),
 'Mid-City/Fairfax': dict(sent='none', conf='low', why="No two-wheel docs. Evidence is car-based: a 2026 armed robbery of a BevMo delivery at Olympic & Cochran, a Mid-City courier naming the CloudKitchens hub on W Washington Blvd, a Mid-Wilshire/Pico ghost-kitchen hub, and Park La Brea access complaints.", samples=['1vcgl9x', '8n99nv', '1vxn88f']),
 'Beverly Hills/Century City': dict(sent='negative', conf='low', why="One two-wheel doc (2018 bike messenger harassed by police in BH/WeHo) plus an observation that 'Beverly hill drivers use Bird'. Car drivers describe BH as dead most days, evil traffic, valet-only restaurants and low tips from upscale customers.", samples=['7sdaho', 'dcno96', '1mottyz']),
 'Valley/SFV': dict(sent='mixed', conf='low', why="Five two-wheel docs including the corpus's most experienced e-scooter courier (5,500+ deliveries on an Unagi + Metro bus, West SFV, McDonald's 'command center'); other riders in NoHo/818 ask whether a bike beats a car for parking. Not a candidate hub area but a source of riders who ride into Hollywood/WeHo.", samples=['zoqc22', '1kyp7be', '1f9x83i']),
 'Glendale/Burbank': dict(sent='mixed', conf='low', why="Four two-wheel docs: a Glendale 49cc scooter owner planning to ride into downtown, a Glendale moped rider whose Uber navigation routed onto freeways, a Burbank/NoHo bike hopeful. Not a candidate hub.", samples=['dm5uhi', 'uwesb7', '1f9x83i']),
 'Pasadena': dict(sent='positive', conf='low', why="Four two-wheel docs (2016-2022): an e-scooter courier says Pasadena is 'working out great' (2018); an e-bike applicant plans to try Pasadena because downtown had no e-bike option. Outside the candidate list.", samples=['84qfz0', 'udhb8g', 'fj5pr9']),
 'South LA': dict(sent='none', conf='low', why="No two-wheel docs. Car drivers report feeling unsafe on late-night Compton/Watts runs and lower-income areas tipping better; Grand Food Depot ghost kitchen (W 38th St) is a pickup cluster.", samples=['spranu', '1bzlapj', '1245m4q']),
 'South Bay': dict(sent='mixed', conf='low', why="One e-bike planner in Torrance asks LA bike couriers whether 20+ mph suffices; Gardena/Hawthorne zone car earnings are dismal ($90 in 31 hrs, 2026).", samples=['obd8b4', '1v0bins']),
 'Long Beach': dict(sent='none', conf='low', why="No two-wheel docs among LA-verified mentions; car-driver posts only.", samples=[]),
 'East LA/Boyle Heights': dict(sent='none', conf='low', why="No two-wheel docs; an East LA resident drives to Westwood/USC to find orders.", samples=['1aw4ual']),
}
area_ranking = []
for a in AREAS:
    docs = area_docs[a]
    twids = sorted(set(tw_by_area.get(a, [])))
    n_tw_docs = len(twids) + sum(len(CROSSPOSTS.get(i, [])) for i in twids)
    car = sum(1 for c in docs if CAR.search(c['text']) and c['id'] not in TW)
    note = AREA_NOTES[a]
    area_ranking.append(dict(
        area=a,
        la_verified_mentions=len(docs),
        two_wheel_mentions=len(twids),
        two_wheel_docs_incl_crossposts=n_tw_docs,
        two_wheel_ids=twids,
        car_mentions=car,
        sentiment_for_two_wheel=note['sent'],
        why=note['why'],
        confidence=note['conf'],
        sample_urls=[doc(i)['url'] for i in note['samples'][:3]],
    ))
area_ranking.sort(key=lambda r: (-r['two_wheel_mentions'], -r['la_verified_mentions']))

# ---------- two-wheel hotspots ----------
two_wheel_hotspots = [
 dict(place='Downtown LA core (Historic Core / Financial District; hotspot named at 6th St & Spring St)', evidence_count=29, quotes=[
   Q('nq3ho0', 'I used to dash with a car, now an electric scooter, Downtown LA'),
   Q('7u8jh1', "i worked this with UberEATS on my bicycle, I am surprised with the number of requests, it's more than what I get in Beverly Hills or Hollywood. I thought nobody lives in downtown, it's only offices,  but I guess I was wrong, so many foreigners rent there. A lot of Asians and international students."),
   Q('avp2wa', "I'm a dasher that has the insane privilege to ride a bike-- We get Westwood-Westwood blvd. x Ohio Ave. & DTLA- Spring St. x 6th St."),
 ]),
 dict(place='Hollywood (Hollywood & Highland / Sunset-La Brea corridor) and the DoorDash Hollywood-Silverlake zone', evidence_count=13, quotes=[
   Q('dm0jhp', "Unicorns in Hollywood 🦄 - My acceptance rate is about 15%. I’m on an electric scooter and these are the jobs that I really make a killing on. Anything with a 10 to 1 $ to miles ratio is a unicorn to me"),
   Q('1mottyz', "I live in Hollywood and dash in both Hollywood-Beverly Hills as well as Hollywood-Silverlake zones. It’s crazy to me how Bev zone is SOOOOO dead every day and Silverlake be flooded with orders."),
   Q('11khbg4', 'I also dash mainly in Hollywood/Silverlake, which already has bad parking, but that delivery zone also has Koreatown in it and sometimes sends you to customers in DTLA, so I think parking would be a lot easier.'),
 ]),
 dict(place='Santa Monica (flat, bike lanes, Prop 22 wage floor pegged to SM minimum wage)', evidence_count=6, quotes=[
   Q('1e612mu', 'Prop 22 in CA makes it that if you are working you are making at least $21 an hour during a delivery in Santa Monica, CA. (Downside is LOTS of drivers).'),
   Q('1d5qonh', "with prop 22 in Los Angeles I’m guaranteed 120% of the minutes wage of Santa Monica ($16.90). So if I’m trying to just make $20 an hour wouldn’t it be worth it to say yes to every delivery?"),
   Q('1gn3r1q', "I see some around 300$ - 500$ on Amazon with 50-60 miles of range. There’s bike lanes everywhere so it won’t be a problem."),
 ]),
 dict(place='Westwood Village (Westwood Blvd & Ohio Ave named as a bicycle hotspot; Duffl student scooter fleet)', evidence_count=3, quotes=[
   Q('avp2wa', 'But what is the closest area to that HOTSPOT in Westwood that you can start Dashing at? Closer to Hollywood.'),
   Q('ur25fd', "I work at a company called Duffl which has 3 hour delivery shifts. Don’t need crazy range. max of 3 hours worth. I live in Westwood, Los Angeles, California where the roads are SHIT and filled with hills everywhere. Our store scooters are G30P’s but they break constantly because of the shit roads."),
   Q('wmx6he', 'Is Westwood compact enough to deliver DoorDash on a bicycle? Does DD even give a bike option there?'),
 ]),
 dict(place='Koreatown (inside the Hollywood-Silverlake zone; Melrose Food Co ghost kitchen at 615 N Western)', evidence_count=3, quotes=[
   Q('iowfiq', 'LA/Koreatown Area Morning Bicycle Mode ! This is depressing lol'),
   Q('162vejl', 'Does anyone deliver on bike? Any tips and information is much appreciated! I live in la ktown just moved here.'),
   Q('1245m4q', "Melrose Food Co: 615 N Western Ave, Los Angeles, CA 90004"),
 ]),
 dict(place='West Hollywood (night bike-messenger territory; 20-driver pileups at popular restaurants)', evidence_count=3, quotes=[
   Q('7sdaho', 'i am a bike messenger in LA , i deliver during dinner time , from 6 to 12am , and i have to cover myself with a hoodie and wear gloves'),
   Q('10k0vso', 'likely going to be doing ubereats & grubhub in LA, more specifically West Hollywood & surrounding areas, on a bike.'),
   Q('139c1kf', 'I got a really good offer, $14 for less than 2 miles away, but when I arrived, there were about 20 other drivers waiting for a pick up.'),
 ]),
 dict(place='Pasadena (Old Town) - outside candidate list but explicit e-scooter success', evidence_count=4, quotes=[
   Q('84qfz0', 'I have been doing deliveries using my electric scooter in Pasadena and working out great'),
 ]),
 dict(place='West San Fernando Valley (e-scooter + Metro bus model; McDonald\'s near the mall as base)', evidence_count=5, quotes=[
   Q('zoqc22', "I’m a DoorDasher from the West San Fernando Valley part of Los Angeles, and I’m currently at over 5500 deliveries using just my Unagi electric scooter and the Metro Bus system to save battery (I can fold it and store it under the seats)."),
 ]),
]

# ---------- vehicle types ----------
def ids_with(rx):
    r = re.compile(rx, re.I)
    return sorted(i for i in TW if r.search(TW[i][1]) or r.search(doc(i)['text']))
vehicle_types = dict(
  counting_note="Counts are unique LA-verified courier posts (cross-posts merged) where the poster uses or is choosing that vehicle for delivery; a post can count in several rows. Total unique two-wheel courier posts = %d (%d docs incl. cross-posts). Area-unspecified LA posts = %d." % (len(TW), len(TW) + sum(len(v) for v in CROSSPOSTS.values()), sum(1 for v in TW.values() if not v[0])),
  ebike=dict(count=len(ids_with(r'e-?bike|electric bike|electric bicycle|ebike')), ids=ids_with(r'e-?bike|electric bike|electric bicycle|ebike'), quotes=[
     Q('1lcn2d4', "I deliver by my e-bike (which isn't your typical e-bike, it can travel up to speeds of 40+ MPH, and has a range of about 40 miles on a full charge), and I have my app marked as delivering by car to get more deliveries."),
     Q('syz06v', "Ideally I’d like one that goes at least 20-25 mph and has a range of at least 40-50 miles. Also, one that is easy to lock up to prevent theft while picking up orders and dropping them off."),
     Q('1dizbwm', "now i have an Electric bicycle that makes climbing hills a breeze, but I've noticed i only get around two offers in an hour"),
     Q('1nu0ot9', 'Does Ebike Dash still work in Los Angeles? I have got 1 offer in a week.'),
     Q('kz19g9', 'E-bike... Started a few weeks ago. Los Angeles.... 3 apps at a time, getting the hang of it!'),
     Q('18i6zgk', 'Please recommend me e-bike rental companies in Los Angeles. E-bike for delivery not for personal use'),
     Q('1dnmppt', "I’m in downtown LA and also an international student who needs to make ends meet."),
     Q('1tydibj', 'i live in LA urban area. Might use it to pick up nephews from school or go to Ralphs to buy some stuff. Thinking about riding it in downtown too to do some local delivery jobs.'),
  ], rental_demand_note='One explicit 2023 request for an LA e-bike RENTAL company "for delivery not for personal use" (r/ebikes) and a 2024 international student in DTLA asking which e-bike to buy for DoorDash; a 2024 Chinese-language rider posts ~25 "Ubereats, Doordash, Grabhub Ebike Adventure Los Angeles" POV videos to r/ebikes and r/doordash.'),
  standing_escooter=dict(count=len(ids_with(r'e-?scooter|electric scooter|ninebot|unagi|scooter \(standing\)')), ids=ids_with(r'e-?scooter|electric scooter|ninebot|unagi|scooter \(standing\)'), quotes=[
     Q('nq3ho0', 'I used to dash with a car, now an electric scooter, Downtown LA'),
     Q('zoqc22', "While waiting for orders, I hang out at the McDonald’s closest to the mall and plug in what I like to call “the command center”; iPad, iPhone, Nintendo Switch, 2 portable power banks, and my scooter all charging at once."),
     Q('14ah15y', "I have a Ninebot scooter. Going to be installing a Ulip (amazon) rear rack on top of the back tire."),
     Q('1v45xof', "Trying to start dashing in Los Angeles, but I don’t have a car and I suck at riding a bike so I thought I’d buy an electric scooter"),
     Q('ur25fd', "Our store scooters are G30P’s but they break constantly because of the shit roads."),
  ]),
  gas_scooter_moped_49cc_ruckus=dict(count=len(ids_with(r'49cc|ruckus|zuma|moped|gas scooter|motor scooter|125cc|monkey')), ids=ids_with(r'49cc|ruckus|zuma|moped|gas scooter|motor scooter|125cc|monkey'), quotes=[
     Q('16v4et6', 'Switched from bike to motor scooter 49cc. Not have one trip in  almost 2 weeks.'),
     Q('16v4et6', 'Got  a few on my bike but the scoot is the best for deliveries. Fast and efficient.'),
     Q('xmdxgz', "Guys im stuck between buying a e-bike or scooter (something like honda ruckus or Yamaha Zuma) The e bike can go on the curb but if i put my motorcycle on the curb for 10mins would i get a ticket?"),
     Q('dm5uhi', 'I would be using a 49cc scooter to do deliveries.'),
     Q('uwesb7', 'my scooter is freeway legal but will not reach the acceleration needed for the freeway.. I\'m a bit concerned.'),
  ]),
  motorcycle=dict(count=len(ids_with(r'motorcycle')), ids=ids_with(r'motorcycle'), quotes=[
     Q('cmgyui', "Today it finally started giving motorcycle shifts (I'm in Los Angeles) And it looks like it's actually giving preference to the motorcycle.... It lets me grab a shift with the bike but not when I switch to car. Smart... The bike (motorcycle) is 20 times faster than the car in LA"),
     Q('10y11ow', 'I am planning on working for Door Dash using my Honda Monkey throughout Los Angeles City and its surrounding Suburbs.'),
  ]),
  surron_talaria=dict(count=0, ids=[], note='Zero LA courier posts mention Sur-Ron or Talaria as a delivery vehicle. The only "Talaria" hit is an apartment building in Burbank, and every r/Surron post matching "delivery LA"/"doordash los angeles" is about Alibaba bikes arriving at the Port of LA or a SoCal reseller pricing Light Bees. Searched all posts including r/Surron, r/ebikes and r/ElectricScooters.'),
  pedal_bike=dict(count=len(ids_with(r'\bbike\b|bicycle|fixie|road bike|foot')), ids=ids_with(r'\bbike\b|bicycle|fixie|road bike|foot'), quotes=[
     Q('7t0m96', "i asked uber support, if there are people who do it like me on a bike in LA, they said not in LA , we have in SF and NYC mainly but in LA it's rare."),
     Q('syz06v', 'I tried delivering food in downtown LA on a regular bike but it was so damn tiring. Going up inclines was hell.'),
     Q('pvdxq6', 'For Uber Eats, on the bike a 3 mile, 40 minute delivery up the Hollywood Hills is too exhausting.'),
     Q('f9p8t5', 'Cheap ass people in Silver Lake and biking up some of those curvy hills is no joke'),
     Q('igu9bi', 'I saw three other food delivery bikers, and all of them had delivery backpacks and absolutely no rear rack.'),
  ]),
  range_speed_battery=dict(evidence=[
     Q('syz06v', "Ideally I’d like one that goes at least 20-25 mph and has a range of at least 40-50 miles."),
     Q('1lcn2d4', "it can travel up to speeds of 40+ MPH, and has a range of about 40 miles on a full charge"),
     Q('1gn3r1q', "I see some around 300$ - 500$ on Amazon with 50-60 miles of range."),
     Q('obd8b4', 'To LA bike couriers: you think this is a good idea? Will ebikes going 20+mph suffice?'),
     Q('zoqc22', 'using just my Unagi electric scooter and the Metro Bus system to save battery (I can fold it and store it under the seats)'),
  ], battery_swapping_mentions=0, note='No LA courier post mentions battery swapping or carrying spare batteries; the only battery-management tactic described is folding a standing e-scooter onto Metro buses and charging at McDonald\'s. Stated wants: 20-25 mph minimum, 40-50 mi range, lockable, hill-capable.'),
  app_vehicle_mode_in_LA=dict(evidence=[
     Q('ujwab7', 'not one delivery is bike friendly, only scooter mode gets orders, and they always go far away from downtown Core or inner ring road.'),
     Q('12vic27', 'I had to use scooter mode to get anything and I had to cherry pick ones that I can deliver by bike.'),
     Q('1lcn2d4', 'I have my app marked as delivering by car to get more deliveries.  Prop 22 pays me 1.2 times minimum wage, plus 34 cents for every mile travelled'),
     Q('udhb8g', "I already tried downtown and I think they don't have it as an option . When I put my 1st application in there was no option for ebike only car or motorcycle."),
     Q('q0lu13', 'Why is there no bicycle option when applying in Los Angeles? Only car/motorcycle.'),
     Q('cmgyui', "I originally signed up with a motorcycle but they'd never let me do a shift. Switched to car and have been working ever since. Today it finally started giving motorcycle shifts (I'm in Los Angeles)"),
     Q('1ke5hch', "I've seen posts online saying that bike and e-bike modes across all delivery apps are dead as far as the volume of orders recevied"),
     Q('16v4et6', 'Switched from bike to motor scooter 49cc. Not have one trip in  almost 2 weeks. Support said my account is all clear for deliveries but getting nothing.'),
  ], summary="Consistent pattern 2019-2025: DoorDash 'bike'/'bicycle' mode in LA is described as nearly dead, 'scooter' mode (which DoorDash treats like a motor vehicle for dispatch radius) gets orders but sends riders far, Grubhub's LA sign-up offered only car/motorcycle (no bike/e-bike) in 2021-22, and fast e-bike/e-moped riders register as 'car' to get volume and Prop 22 mileage pay. Implication: an e-moped/Class-3 product that lets a rider legitimately run car or scooter mode is what the market rewards; a pure bicycle-mode rider is starved."),
)

# ---------- where riders live / commute / hang out ----------
where = dict(
  rider_home_bases_stated=[
    dict(area='DTLA (lives downtown, delivers downtown)', ids=['1ce67b8', '6qyzrg', 'hadavv'], quote=Q('1ce67b8', 'I plan to use an electric scooter (that I own) and an insulated backpack to make deliveries within the downtown city part of Los Angeles, where I\'ve lived for several years now.')),
    dict(area='Koreatown (lives K-town)', ids=['162vejl', '1hcs3ic'], quote=Q('1hcs3ic', 'I live in the Koreatown area of Los Angeles and I schedule myself to dash Mon-Friday from 11am-1pm')),
    dict(area='Hollywood / Thai Town / East Hollywood (lives and delivers)', ids=['1mottyz', 'piraz3', '12i4jje'], quote=Q('12i4jje', 'I live and deliver in the Thai Town/East Hollywood area, sometimes ending up going as far as Santa Monica, Pico-Union, Pasadena, or Burbank.')),
    dict(area='Silver Lake / Echo Park (moved there, car)', ids=['s2hmy6', 'pfchdn'], quote=Q('pfchdn', "I’ll be living in the Silverlake/Echo Park area (I’m pretty sure this is relevant in regards to ‘zones’).")),
    dict(area='San Fernando Valley / NoHo / Burbank edge - riders who commute INTO Hollywood/WeHo', ids=['1kyp7be', '1f9x83i', 'rkx1qz', 'zoqc22', '1iwx1s0'], quote=Q('1kyp7be', "I’m in the valley and sometimes venture out in WeHo/Hollywood area but feel like there’s got to be a better area to do bicycle deliveries")),
    dict(area='Glendale - 49cc scooter rider commuting into downtown', ids=['dm5uhi'], quote=Q('dm5uhi', "I live in Glendale (10 miles north of downtown LA) and wouldn't mind driving out into the city to do deliveries.")),
    dict(area='Pasadena - bicyclist riding to Santa Monica to dash', ids=['fj5pr9'], quote=Q('fj5pr9', 'Im new to the LA door dash scene and am on a bicycle. I live in pasadena but have been going all the way to santa monica to dash.')),
    dict(area='Riverside / Inland Empire - carless rider planning bus+bike into DTLA/Hollywood', ids=['1qlhg3s'], quote=Q('1qlhg3s', 'Hey I have no car and live in Riverside, I do have a bike, I plan on commuting to Anaheim and DTLA then testing for any notification')),
    dict(area='Culver City / Playa Vista - drivers living in vehicles overnight (car)', ids=['1m1mlfb'], quote=Q('1m1mlfb', 'He is known to drive for Uber Eats (unsure about DoorDash) and has covered areas such as **Venice, Santa Monica, Culver City, Pasadena, and Playa Vista.** He often parks/stays in those areas overnight.')),
    dict(area='East LA resident driving to Westwood/USC for orders (car)', ids=['1aw4ual'], quote=Q('1aw4ual', "I’m in the East LA area and I usually go around Westwood or USC and that’s where I get deliveries")),
    dict(area='San Gabriel Valley / La Verne dashers weighing a 30-min drive into Beverly Hills/Hollywood (car)', ids=['1pxwvvo'], quote=Q('1pxwvvo', "I’m wondering if it’d be worth it driving 30 min to Beverly Hills, Hollywood, etc.")),
  ],
  students=[
    Q('15dae0o', 'I am a graduate student at USC and want to make some money for living expenses.'),
    Q('1mgovuq', "I’m suspecting because the college kids are dipping into doing delivery for summer vacation."),
    Q('1mgovuq', 'USC area I at least get some orders, although the trade off is 1 dollar tips because I guess most of the deliveries are to college students...'),
    Q('jfezl3', "Couriers in Los Angeles: We're a team of MBA students from UCLA doing market research for interest in e-bikes for food delivery."),
    Q('cbpi9m', 'I started DD in March 2019 when I was in my last semester at college.'),
    Q('7u8jh1', 'I thought nobody lives in downtown, it\'s only offices,  but I guess I was wrong, so many foreigners rent there. A lot of Asians and international students.'),
    Q('1dnmppt', "I’m in downtown LA and also an international student who needs to make ends meet."),
    Q('m2g94t', 'If someone at the Lorenzo orders Uber Eats can you please let me know so i can go online & deliver it for you, tryna make some side money rn'),
    Q('ur25fd', 'I work at a company called Duffl which has 3 hour delivery shifts.'),
    Q('17exg6x', "Does anybody drive for Doordash or Uber Eats around ucla? How bad is the LA driving, and how much does it make?"),
  ],
  students_note='USC/UCLA students appear as couriers (bike, Duffl scooter, car) and as the dominant low-tipping customers; two Daily Bruin reporters (2023, 2024) solicited student couriers, and an r/dtla bicycle courier attributes DTLA order density to Asian/international student renters.',
  immigrant_or_spanish_speaking=dict(note='Very thin in this English-language corpus. No post describes Spanish-speaking or immigrant two-wheel courier groups in LA. Indirect signals only: account-sharing/purchased accounts (one undocumented Armenian dasher running 3 phones ~40 mi from LA; West LA customers noting drivers never match the profile photo), an AxelHire courier complaining about "immigrants working" in the LA market, the missing-driver family checking the ICE database, a Chinese-language e-bike courier posting ~25 LA POV delivery videos (titles partly in Chinese) to r/ebikes, and an r/dtla bicycle courier who moved from New York and credits DTLA demand to "foreigners", "Asians and international students".', evidence=[
    Q('188pvss', "I noticed a guy with THREE 😧 phones and all of them had the dasher app turned on. I started a conversation with him, and it turned out that he came from Armenia and doesn’t have legal documents, so he works from fake accounts."),
    Q('1q8stp9', "I’m in West Los Angeles area. I’ve only been here for a handful of months and I don’t even order DoorDash that often but I feel like I haven’t had a single delivery driver match the photo of the person who’s listed."),
    Q('10xidqd', 'I work in the Los Angeles Market. 9. Allot of immigrants working. This causes routes to be very, very hard to get.'),
    Q('1pxwvvo', "it seems like there’s vulture-like dashers everywhere you go. Now I’m not afraid of the competition as I am at platinum level so I have a good advantage, but I heard people out there have multiple phones to get more orders."),
  ]),
  hangouts_and_staging=[
    dict(place='Ghost-kitchen hubs (drivers stage in the lot and get pinged immediately)', quotes=[
      Q('1245m4q', 'Colony: 11419 Santa Monica Blvd, Los Angeles, CA 90025'),
      Q('1245m4q', 'Washington Food Co: 1842 W Washington Blvd, Los Angeles, CA 90007'),
      Q('1245m4q', "These spots are my go-to spots when I start my day delivering for Uber Eats. It’s easy to quickly get an order as soon as you park by one of these. It’s the equivalent of an Uber X driver going to the airport and waiting for a passenger ride."),
      Q('8n99nv', "HOTSPOT for drivers to pickup orders is at 1842 W. Washington Blvd, LA, CA 90007.  It's CLOUDKITCHEN with about 30 restaurants.  I see mostly, Ubereats, postmates, grubhub, and doordash drivers there."),
      Q('10la8af', 'So here in Los Angeles, Sugarfish has a few ghost kitchen locations around the city to accommodate most of their Uber Eats/Postmates orders.'),
      Q('1nzxlk1', "They closed the shops and boutiques during Covid, boarded up the building, and it’s become a food delivery ghost kitchen hub. And a constant eyesore. Doesn’t the city regulate landlords about these things? Can they just do this forever? (Mid-Wilshire on Pico)"),
    ]),
    dict(place="McDonald's (Valley e-scooter courier's charging/wifi 'command center'; Crenshaw McDonald's restroom dispute; dashers chatting at McDonald's)", quotes=[
      Q('zoqc22', "While waiting for orders, I hang out at the McDonald’s closest to the mall and plug in what I like to call “the command center”"),
      Q('tsmdog', "I’m doing a pickup at this McDonald’s on 4292 Crenshaw in Los Angeles told me I have to buy something just to use the restroom"),
    ]),
    dict(place='Popular restaurants where 9-20 drivers camp (unnamed hip LA restaurant; Gardens of Taxco WeHo; Beverly Hills pickups)', quotes=[
      Q('1hcdfx9', "The restaurant is a hot spot high tip and a lot of dashers like to camp outside of it. It’s also one of those hip restaurants in Los Angeles that have a line of people waiting to sit down and eat."),
      Q('139c1kf', 'there were about 20 other drivers waiting for a pick up.'),
      Q('1aifudt', 'There are 4, yes, FOUR other Door Dash drivers at this second spot.'),
    ]),
    dict(place='Named bicycle hotspots (2019)', quotes=[Q('avp2wa', 'We get Westwood-Westwood blvd. x Ohio Ave. & DTLA- Spring St. x 6th St.')]),
    dict(place='Culver City zone roaming corridors (car)', quotes=[Q('1c10313', "So lately I’ve been roaming east and west along Venice from Robertson to Sepulveda. Sometimes, I’ll crawl Palms from Overland to  National.")]),
    dict(place='Library / bus as waiting spots for carless riders', quotes=[Q('1qlhg3s', 'wait an hour in a library or just ride around restaurants and tourist areas getting some exercise for like 3 days waiting for any order')]),
    dict(place='Not found', quotes=[], note='No LA post mentions Grand Central Market, Whole Foods, 7-Eleven, hotel lobbies or Koreatown plazas as courier gathering places. CB-radio and Reddit are the only rider-community channels mentioned; riders describe the job as solitary.'),
  ],
)

# ---------- safety / theft ----------
safety = dict(
  summary='Across ~1,950 LA-verified posts there are no first-person reports of a delivery bike, e-bike or scooter being stolen; the theft anxiety that appears is prospective (wanting a lockable e-bike) and about phones left in cars. Violence reports are car-based robberies/attempted robberies (DTLA-to-West Adams van ambush, Olympic & Cochran BevMo robbery, a warehouse-complex jumping near LA), sketchy Skid Row drop-offs, women declining night deliveries in Koreatown/Hollywood-Silverlake and South LA, police stops of a night bike messenger in Beverly Hills/WeHo, and traffic danger (sidewalk e-scooter collision in Culver City, cars in DTLA bike lanes).',
  by_area=[
    dict(area='DTLA / Skid Row', items=[
      Q('uaf1v3', 'It all felt a little weird, but my first priority was to just gtfo skid row without getting hassled, which I immediately did.'),
      Q('1ooco56', "it is on skid row homeless everywhere how can if I leave it in front of them well at last finally he showed up after 10 minutes"),
      Q('1r6o88g', 'I work security in a homeless shelter in skid row , Los Angeles… genuinely have so much respect for my drivers that actually come thru . I always tip em ten bucks minimum.'),
      Q('15qno06', "This particular order was from Popeyes, near dtla area. The drop off was in the west adams neighborhood, for those not familiar with deep LA neighborhoods, it’s near the 10 fwy."),
      Q('15qno06', 'Immediately 6 men dressed in all black with some sort of leggings over their head trying to cover up their face jump out the van, and start running towards my car.'),
      Q('ps4sre', 'If you park in the bike lane in DTLA You are a garbage human.  You are putting every delivery person on a bike at risk'),
      Q('syz06v', 'one that is easy to lock up to prevent theft while picking up orders and dropping them off.'),
      Q('luqhar', 'Obviously downtown LA would be a big nightmare for someone who isn’t familiar with the area.'),
      Q('bzt91s', "it looks like biking through Skid Row down 6th St. would be way quicker than the bus."),
    ]),
    dict(area='Westlake / MacArthur Park', items=[
      Q('5px3e9', "I'd like to get a bike as well so I have easier access to Wilshire/Ktown (~1.5 miles away) but I'm not sure of bike racks and safety from theft."),
    ], note='No courier incident reports; one prospective resident worries about bike theft near MacArthur Park (2017).'),
    dict(area='Koreatown / Hollywood-Silverlake zone', items=[
      Q('1hcs3ic', 'I am a female and after a couple of bad experiences I will no longer risk doing deliveries at night.'),
      Q('cbpi9m', 'I started to grow really tired of the poor reception in Koreatown LA which caused my app to crash constantly'),
      Q('c1xrog', 'Just moved from Florida and was issued a $200 ticket for riding a scooter on Wilshire.'),
    ]),
    dict(area='Hollywood / West Hollywood / Beverly Hills', items=[
      Q('qsv5ea', 'I’m a girl driving alone so I don’t like to continue dashing once it gets dark out. Too sketchy.  Too many fucking apartments with no parking in sketchy areas.'),
      Q('fhj1er', "I have the most stolen car in America, and I'm a blatantly white dude. I felt rather unsafe in Hollywood, I'll say"),
      Q('7sdaho', 'they stop and ask me what i am doing , or they block me with their car , and ask me questions like  , i am clean as a whistle , i am a 22yo  Caucasian dude , i just believe they suspect every young person ,  and they bother most in beverly hills and weho'),
      Q('10oy016', 'While taking a double-order in West Hollywood, I was waiting for the light and heard a car honk at people who were walking when it wasn’t their turn.'),
      Q('r0k9xt', 'Scariest moment was when I got out of the car for a 7-11 pick up 5-10 minutes away from Dodger stadium. (Riots simmering) homeless off their shit.'),
    ]),
    dict(area='Mid-City / West Adams', items=[
      Q('1vcgl9x', 'They took the alcohol, and along with the staff, they went back inside of the home on the corner of Olympic and Cochran. I spent the next hour wasting my time and my breath. DoorDash nor the police did anything'),
      Q('awuuop', 'I saw an LAPD officer at the front door, a huge ass gun strapped across his chest. He yelled at me "COME OUT!" Oh fuck.'),
    ]),
    dict(area='South LA / Compton / Watts', items=[
      Q('spranu', 'I am a female that delivers in the southern Los Angeles area and twice i have been sent to Compton after 10pm.'),
      Q('1bzlapj', 'Also throughout the day I notice the deliveries take me further and deeper in to south central Compton area. After delivering there I go offline until I get back to an area I’m familiar with.'),
      Q('myuh4s', 'the app seeming to constantly offer you orders going further south to rougher areas is a turn off.'),
    ]),
    dict(area='Westside (Culver City / Santa Monica / Westwood)', items=[
      Q('j9vs4j', 'I was waiting outside a restaurant in Culver City and a man comes by on the sidewalk on an electric scooter at full speed and swerved to hit me.'),
      Q('198c16x', 'Just left a customer’s food at door, here in Santa Monica. As soon as I got in my car I seen a homeless guy just grab it and kept walking.'),
      Q('1t5n6cg', 'I hate delivering at ucla campus specially the hospitals there. Many of these nurses know we can’t park in the emergency area and the valet doesn’t allow us to park our cars too.'),
      Q('1l2s5lh', 'She flashes a $100 bill and asks if I have change. I say nope, but I can check in the car. I walk away for like 15 seconds and she snatches the pizza and runs inside like she just pulled off a heist in GTA.'),
      Q('twbyrh', 'Just saw at the Veteran & Strathmore intersection a Parking Enforcement officer parking in the red zone, giving a ticket to someone else parking in the red zone. I think the other person was probably a food delivery driver'),
      Q('7u8jh1', 'especially when homeless people tell you,  don\'t take pictures haha  it\'s like the own downtown now,  DTLA aka the home of the homeless'),
    ]),
    dict(area='Near LA (city redacted) - warehouse ambush', items=[
      Q('ke3232', 'Just want to share i was just jumped while dashing in (city redacted)* in California near Los Angeles by 2 guys.'),
    ]),
  ],
  bike_theft_incidents_reported_by_couriers=0,
  night_riding=[
    Q('7sdaho', 'at certain time of the night LA streets are empty , and me i take advantages and deliver , but the cops really bother me'),
    Q('1ljf3jq', 'Los Angeles - WeHo & Silverlake areas. If I dash at these odd times I get multiple offers. After only a few hours, apparently it gets oversaturated cause I stop receiving orders.'),
    Q('yn1trc', 'Stay consistent and dash when other dashers typically do not. (11pm-10am)'),
  ],
)

# ---------- earnings ----------
earnings = [
  dict(area='DTLA', vehicle='bike/foot', year=2021, figure='UE ~$16-20/hr ($95-100 per 5-6 h); DD ~$10-12/hr ($62.75 per 5-6 h)', q=Q('q0yp2w', 'Downtown L.A. big market.  UE 5-6 hours on bike/foot. $95-100 on multiple days.  DD 5-6 hours on bike/foot $62.75')),
  dict(area='DTLA + Hollywood', vehicle='unspecified (car implied)', year=2024, figure='$8/hr on weekend peak hours', q=Q('1dnuui4', 'Making $8 an hour in Los Angeles Peak Hours & Days')),
  dict(area='DTLA', vehicle='car', year=2021, figure='$215 + $19 cash tips in one day (security guard side gig)', q=Q('lc22gg', 'literally that day Before work i made $215+$19 in cash tips So I’m very well aware of how much you CAN make doing DD.')),
  dict(area='DTLA (e-scooter, planned)', vehicle='e-scooter', year=2024, figure='needs >= $350/month to be worthwhile', q=Q('1ce67b8', 'Including all my bills, I\'ll have to clear a *bare minimum* of $350/month to make this work profitable.')),
  dict(area='Downtown, Hollywood, Santa Monica', vehicle='car', year=2019, figure='$15-30/hr (2018-19, DD)', q=Q('c3ltdn', 'I was paid between 15 to 30$ an hour . Downtown, Hollywood Santa Monica , San Diego .')),
  dict(area='Santa Monica', vehicle='e-bike', year=2024, figure='Prop 22 floor ~$20-21/hr of active delivery time', q=Q('1e612mu', 'Prop 22 in CA makes it that if you are working you are making at least $21 an hour during a delivery in Santa Monica, CA.')),
  dict(area='Santa Monica', vehicle='car', year=2023, figure='$22-25/hr (~$100 per 4 h) fell to $60-70 per 8 h', q=Q('1787jmo', "I’ve went from making a decent $22-$25hr in the Santa Monica area. Literally would work a 4hr shift and come out with at least $100")),
  dict(area='Santa Monica zone', vehicle='car', year=2024, figure='$15 in 5 h', q=Q('1hj9yaf', 'I logged in the other day in Santa Monica zone and made only $15.00 (two orders) in 5 hours.')),
  dict(area='Santa Monica zone', vehicle='car', year=2025, figure='$14 in 7.5 h (Sunday)', q=Q('1ir8hmm', 'I Dashed in Santa Monica zone and only made $14.00.')),
  dict(area='West Hollywood', vehicle='car', year=2024, figure='$18-30/hr usual', q=Q('1gmn1zo', 'I usually make about $18-$30 an hour in West Hollywood.')),
  dict(area='Hollywood / West Hollywood', vehicle='car (Grubhub)', year=2022, figure='$200/day (8-9 h) in 2021 -> $120-150 -> $50-70', q=Q('wh3f3f', 'I use to make up to $200 a day, working eight to nine hours a day. Now, I’m lucky to make $120-150 a day')),
  dict(area='Hollywood', vehicle='car (Uber Eats)', year=2023, figure='$30/hr in 2021 pandemic, fraction by 2023', q=Q('14zp36s', 'The orders I got at the height of the pandemic were flying in and I was able to make $30 an hour easily at least.')),
  dict(area='Hollywood-Silverlake zone', vehicle='car', year=2024, figure='$5.25 in 3 h (first day)', q=Q('1ddwoir', 'This one order earned me $5.25, no tip given despite delivering to a $4 million home')),
  dict(area='WeHo & Silverlake (3-7am)', vehicle='car', year=2025, figure='$15 for 2 deliveries 5-6:30am then nothing', q=Q('1ljf3jq', 'I made $15 with 2 deliveries btwn 5-6:30am and then stopped receiving offers after that.')),
  dict(area='Beverly Hills / WeHo / Westwood', vehicle='car', year=2021, figure='Postmates $25/hr min -> DD $61 in 4.5 h, $35 in 2.5 h', q=Q('o28sec', 'I used to consistently make a minimum of $25 an hour if not more on postmates, but I’ve been making very bad money on Doordash.')),
  dict(area='Beverly Hills / Westwood', vehicle='car', year=2025, figure='$5-7 per 2 h', q=Q('1n4lqe8', "I sometimes go two hours and make $5 to $7. Keep in mind that I'm in Beverly hills and Westwood.")),
  dict(area='Westwood', vehicle='car', year=2024, figure='$50 in 4 h', q=Q('19f1gt5', 'yesterday I made 50 bucks in 4 hours which is horrible in my opinion I only had 3 orders this was in Westwood by UCLA.')),
  dict(area='Westwood', vehicle='car', year=2018, figure='$15/hr guarantee promo (pulled)', q=Q('8yn3td', 'Did anybody else sign in at 11am for guaranteed $15 an hour, but now it\'s changed to $1.50 bonus per order?')),
  dict(area='Culver City / Santa Monica / Hollywood', vehicle='car', year=2025, figure='~$25/hr gross before gas', q=Q('1ke5hch', 'I currently average \\~$25/hour before gas expenses and tax delivering in a car.')),
  dict(area='Culver / Venice / Marina / Santa Monica', vehicle='car (Grubhub)', year=2020, figure='best night $78 in 6 h', q=Q('eslp1f', 'My best night is $78 in a 6 hour shift, mainly around Culver/Venice/Marina and The People\'s Republic of Santa Monica.')),
  dict(area='Culver City, DTLA, East LA, Pasadena', vehicle='car', year=2025, figure='$20-30 per 3-4 h session', q=Q('1hrbc0u', 'after a 3-4 hour session I typically only make about $20-30.')),
  dict(area='Culver City', vehicle='car', year=2023, figure='friends $200/day vs poster $50', q=Q('158yk5n', 'My friends tell me they make $200 daily average whereas I can barely make $50 if I’m lucky.')),
  dict(area='Koreatown', vehicle='car', year=2019, figure='~$10/hr net of gas (700 trips)', q=Q('cbpi9m', 'I averaged about $10 per hour accounting for gas and whatnot.')),
  dict(area='Mid-City', vehicle='car (Uber Eats)', year=2018, figure='$492 / 52 trips / 25 h online (~$20/hr)', q=Q('8n99nv', 'last week I made $492 on 52 trips, 25 hours online.')),
  dict(area='Midtown / La Brea', vehicle='car', year=2024, figure='$70 in 3 h (good night)', q=Q('1bujlqx', 'Funny cause last night I made $70 in 3 hours.')),
  dict(area='Gardena/Hawthorne zone (South Bay)', vehicle='car', year=2026, figure='$90 in 31 h', q=Q('1v0bins', 'This was all in Los Angeles in the “Gardena/Hawthorne zone where I Dashed in El Segundo/South Bay/Hermosa/Manhattan Beach areas.')),
  dict(area='Los Angeles market (Platinum vs Gold)', vehicle='car', year=2025, figure='Platinum $20/hr baseline, up to $40/hr; Gold rarely $20', q=Q('1k0di81', "Once you hit Platinum here, $20/hr is the baseline and can even sometimes go all the way up to $40/hr.")),
  dict(area='Los Angeles (Platinum, accept-all)', vehicle='car', year=2026, figure='$1,066 in 31 h (~$34/hr gross)', q=Q('1w8eelv', '$1066 in 31 hours This is with platinum and accepting every single order in Los Angeles.')),
  dict(area='Los Angeles county', vehicle='car', year=2022, figure='~$1,000/wk for ~40 h (Top Dasher, early mornings)', q=Q('yn1trc', 'Ive consistently made around $1,000 a week for about 40ish hours of work. Im located in Los angeles county.')),
  dict(area='East of LA (La Verne/Azusa/Glendora)', vehicle='car', year=2025, figure='$20-25/hr at 85% AR', q=Q('1pxwvvo', 'I make very average earning ($20-25hr) with accepting most orders AR 85%.')),
  dict(area='LA (e-bike marked as car)', vehicle='40+ mph e-bike', year=2025, figure='Prop 22: 1.2x min wage + $0.34/mi', q=Q('1lcn2d4', 'Prop 22 pays me 1.2 times minimum wage, plus 34 cents for every mile travelled (assuming it\'s meant for gas/car maintenance).')),
]
earnings_by_area = [dict(area=e['area'], vehicle=e['vehicle'], year=e['year'], figure=e['figure'], quote=e['q']['quote'], url=e['q']['url'], sub=e['q']['sub'], score=e['q']['score']) for e in earnings]

# ---------- DTLA vs Koreatown vs Hollywood vs Westside ----------
comparison = dict(
  DTLA="Densest restaurant/apartment core and the only LA area where multiple riders describe two-wheel delivery as normal (bike couriers seen with backpacks, e-scooter switch post with 1,172 upvotes, named bike hotspot at 6th & Spring, an r/dtla bicycle courier getting more requests than in Beverly Hills or Hollywood thanks to downtown renters and international students). Downsides riders name: DoorDash bicycle mode gets no orders so riders run 'scooter' mode and get sent 'far away from downtown Core', inclines (Bunker Hill) exhaust pedal bikes, high-rise drop-offs with no parking, Skid Row drop-offs feel unsafe, and volume has been thin since 2020 ('slow as hell'). Grubhub's 'LA - Westside' region historically stretched from DTLA to Venice/Culver.",
  Koreatown="Riders treat K-town as part of the DoorDash 'Hollywood-Silverlake' zone rather than a destination: dense, flat, short trips but bicycle mode 'depressing', poor cell reception, tip-baiters, closed Sweetgreen 'hotspot', and a 2026 newcomer says 'high order zones like downtown or koreatown haven't seemed worth it'. Only 3 two-wheel docs, all questions or complaints; no rider community described.",
  Hollywood="Best documented two-wheel earnings sentiment (2019-2020 e-scooter 'unicorn' orders, $5 peak pay 'all done on scooter'); Silverlake side of the Hollywood-Silverlake zone 'flooded with orders' vs the Hollywood-Beverly Hills zone 'SOOOOO dead'. Parking is bad (a reason car drivers consider bikes), Hollywood Hills climbs punish pedal bikes, women avoid night work, 2024-25 posts report $8/hr peak and oversaturation.",
  Westside="Santa Monica/Venice: flat, bike lanes, and the Prop 22 floor is pegged to Santa Monica's higher minimum wage (~$20-21/hr active) which two e-bike riders explicitly exploit; but 'LOTS of drivers', worst traffic/parking/cops for cars, 2024-25 car earnings of $14-15 for 5-7.5 h. Westwood: one named bicycle hotspot (Westwood Blvd & Ohio), otherwise UCLA dorm/hospital pain, hills, $3 incentives. Beverly Hills/WeHo: dead zone, valet-only restaurants, police stops of a night bike messenger, Bird-riding locals. Culver City: slow 'donut', ghost-kitchen pickups.",
  zones_riders_use="DoorDash zone names used by LA riders: 'Hollywood-Silverlake' (includes Koreatown; sends to DTLA), 'Hollywood-Beverly Hills' / 'Beverly Hills-WeHo', 'Santa Monica zone', 'Culver City zone', 'West Los Angeles zone', 'Westwood', 'Glendale zone', 'Gardena/Hawthorne zone', 'DTLA' as 'my market'; 2019 'USC island' and 'Hawthorne island'. Grubhub regions: 'LA - Westside' (DTLA to Venice/Culver), later split (drivers lost BH/WeHo/Hollywood/K-town/downtown). Caviar bonus areas: WeHo, BH, Venice, Mid-Wilshire, Playa del Rey, West LA.",
  implication_for_hub="Rider evidence points to a hub inside the DTLA-Koreatown-Hollywood triangle: DTLA has the most two-wheel riders and the named bike hotspot, Hollywood-Silverlake is the zone riders say has volume and where Koreatown riders live, and Valley/Glendale/Pasadena riders commute in. The Westside (Santa Monica) is the only other cluster with positive e-bike sentiment but riders there cite Prop 22 economics rather than rider density. Westlake/MacArthur Park and Pico-Union have essentially no rider voice in this corpus (they sit between the clusters and are transited, not discussed).",
)

# ---------- zone names with counts (regex over all LA-verified posts, delivery subs + LA subs) ----------
la_posts = [p for p in posts.values() if (VERIFY.search(ptxt(p)) and (not NOT_LA.search(ptxt(p)) or CORE.search(ptxt(p)))) or p['subreddit'] in ('LosAngeles', 'AskLosAngeles')]
ZONES = {
 'Hollywood-Silverlake (DoorDash zone)': r"hollywood\s*[-/–]\s*silver ?lake",
 'Hollywood-Beverly Hills / Beverly Hills-WeHo (DoorDash zone)': r"hollywood\s*[-/–]\s*beverly ?hills|beverly ?hills\s*[-/–]\s*(west ?hollywood|weho)|beverly hills/weho|weho/beverly hills|west hollywood beverly hills zone|bh weho|bev hills/weho",
 'Santa Monica zone/market': r"santa monica (zone|market)",
 'Culver City zone': r"culver city zone",
 'West Los Angeles zone': r"west los angeles zone",
 'Westwood (zone/hotspot)': r"westwood",
 'DTLA / Downtown LA market': r"\b(dtla|downtown la|downtown los angeles|downtown l\.a\.)\b",
 'Koreatown / K-town': r"\b(koreatown|k-?town)\b",
 'Glendale zone': r"glendale zone",
 'Gardena/Hawthorne zone': r"gardena/hawthorne",
 'USC island / Hawthorne island (2019 DoorDash)': r"(usc|hawthorne) island",
 'LA - Westside (Grubhub region)': r"la\s*-\s*westside",
 'Los Angeles Metro (Rapidus zone)': r"zone: los angeles metro",
 'West LA / Westside (generic)': r"\b(west la|west los angeles|westside|west side)\b",
 'Central LA': r"\bcentral la\b",
 'South Bay': r"\bsouth bay\b",
 'hotspot / hot spot (any)': r"hot ?spots?",
}
doordash_zone_names = []
for name, rx in ZONES.items():
    r = re.compile(rx, re.I)
    hits = [p for p in la_posts if r.search(ptxt(p))]
    doordash_zone_names.append(dict(zone=name, count=len(hits), sample_urls=[purl(p) for p in sorted(hits, key=lambda p: -p['score'])[:3]]))

# ---------- data limits ----------
la_posts = [p for p in posts.values() if (VERIFY.search(ptxt(p)) and (not NOT_LA.search(ptxt(p)) or CORE.search(ptxt(p)))) or p['subreddit'] in ('LosAngeles', 'AskLosAngeles', 'dtla', 'ucla', 'USC', 'LAlist')]
data_limits = [
 "Source is English-language Reddit only (r/doordash_drivers, r/UberEATS, r/doordash, r/grubhubdrivers, r/couriersofreddit, r/Sparkdriver plus r/LosAngeles and r/AskLosAngeles); Spanish-speaking and immigrant couriers who dominate LA's two-wheel delivery workforce on the street are almost entirely absent, and no post describes a Latino/immigrant rider community, hangout or WhatsApp group.",
 f"Car drivers are the overwhelming majority: ~{len(la_posts):,} LA-verified posts (all subs) vs {len(TW)} unique posts ({len(TW) + sum(len(v) for v in CROSSPOSTS.values())} docs incl. cross-posts and one rider's ~25 video posts) in which the poster uses or is choosing a two-wheel vehicle; {len(tw_by_area['DTLA'])} of those are DTLA. Most area-level counts for two-wheel riders are < 5 and should be read as anecdotes, not rates.",
 "Zero mentions of Sur-Ron/Talaria as courier vehicles; only 1 Ruckus/Zuma mention and 2 gas-scooter (49cc) riders. E-moped/Class-3 riders are essentially invisible on these subreddits, so the corpus cannot size that segment.",
 "Time skew: posts span 2016-2026; the most positive two-wheel posts (Hollywood e-scooter series, DTLA e-scooter switch, bike hotspots) are 2019-2021 and predate the 2023-2025 oversaturation and Platinum/AR tier changes. Earnings figures are self-reported, unaudited and often gross of expenses.",
 "Place-name confounds were removed but not perfectly: 'Hollywood, Florida', 'Venice FL', 'Glendale AZ', 'Pasadena TX', 'Long Beach NY', 'Westlake TX' and 'Louisiana LA' posts were excluded by regex + manual review; three Hollywood e-scooter posts were kept as LA on the strength of companion posts by the same author saying 'Hollywood California'.",
 "Sub-neighborhood granularity is poor: riders say 'DTLA' or 'downtown', almost never Arts District, Little Tokyo, Fashion District, Historic Core or South Park (0-2 mentions each); Westlake/MacArthur Park has 2 mentions and Pico-Union 3, so the ranking cannot distinguish candidate DTLA sites from each other.",
 "Selection bias toward complaints and newcomers: many posts are 'is X worth it' questions from people who have not yet delivered; successful full-time riders rarely post. Upvote scores measure sub engagement, not truth.",
 "Search-based scraping (not exhaustive): only the queries listed in done_queries.txt were run. r/Koreatown and r/LosAngelesBikes returned 0 posts for every delivery query; r/dtla returned 5 (one bicycle-courier post), r/ucla 108, r/USC 49, r/LAlist 97, r/ebikes 220, r/ElectricScooters 157, r/Surron 23 - almost all customer-side, marketplace or shipping posts; only ~8 of them are LA courier two-wheel posts.",
 "Sentiment labels and 'own vehicle' classification are the analyst's manual reading of each post; cross-posts of the same text to 2-3 subreddits were merged into one post for two-wheel counts but appear as separate docs in raw mention counts.",
]

# ---------- top 25 quotes ----------
top25 = [
 Q('nq3ho0', 'I used to dash with a car, now an electric scooter, Downtown LA', 'Highest-scoring post in the corpus (1,172 upvotes): the car-to-e-scooter switch is a DTLA story, signalling DTLA as the one LA area where two-wheel delivery is culturally accepted.'),
 Q('ujwab7', 'once I tried it not one delivery is bike friendly, only scooter mode gets orders, and they always go far away from downtown Core or inner ring road.', 'DTLA dispatch reality: bike mode starves, scooter mode gets orders but long trips - argues for e-moped/Class-3 range (not pedal bikes) and a hub that supports 10-15 mi round trips.'),
 Q('avp2wa', "I'm a dasher that has the insane privilege to ride a bike-- We get Westwood-Westwood blvd. x Ohio Ave. & DTLA- Spring St. x 6th St.", 'Only explicitly named bicycle hotspots in LA: 6th & Spring (Historic Core) and Westwood Blvd & Ohio.'),
 Q('1mottyz', "I live in Hollywood and dash in both Hollywood-Beverly Hills as well as Hollywood-Silverlake zones. It’s crazy to me how Bev zone is SOOOOO dead every day and Silverlake be flooded with orders.", 'Zone-level demand signal: Hollywood-Silverlake (which includes Koreatown) has volume; Beverly Hills does not.'),
 Q('11khbg4', 'I also dash mainly in Hollywood/Silverlake, which already has bad parking, but that delivery zone also has Koreatown in it and sometimes sends you to customers in DTLA, so I think parking would be a lot easier.', 'Shows the DTLA-Koreatown-Hollywood triangle is one operating zone for riders and that parking pain pushes car drivers toward two wheels.'),
 Q('dm0jhp', "Unicorns in Hollywood 🦄 - My acceptance rate is about 15%. I’m on an electric scooter and these are the jobs that I really make a killing on. Anything with a 10 to 1 $ to miles ratio is a unicorn to me", '71-upvote proof that a standing e-scooter courier cherry-picking short Hollywood orders made good money (2019).'),
 Q('1e612mu', 'Prop 22 in CA makes it that if you are working you are making at least $21 an hour during a delivery in Santa Monica, CA. (Downside is LOTS of drivers).', 'Santa Monica e-bike economics: Prop 22 floor tied to SM minimum wage; the Westside case rests on wage law, not rider density.'),
 Q('1lcn2d4', "I deliver by my e-bike (which isn't your typical e-bike, it can travel up to speeds of 40+ MPH, and has a range of about 40 miles on a full charge), and I have my app marked as delivering by car to get more deliveries.", 'Exactly the HMP FLASH/e-moped use case: fast two-wheeler registered as a car to get volume + Prop 22 mileage; 40 mi range is the working spec.'),
 Q('syz06v', "Ideally I’d like one that goes at least 20-25 mph and has a range of at least 40-50 miles. Also, one that is easy to lock up to prevent theft while picking up orders and dropping them off.", 'DTLA rider states the product spec (speed, range, lockability) after a pedal bike failed on downtown inclines.'),
 Q('q0yp2w', 'Downtown L.A. big market.  UE 5-6 hours on bike/foot. $95-100 on multiple days.  DD 5-6 hours on bike/foot $62.75', 'Only per-hour two-wheel earnings datapoint for DTLA (~$16-20/hr UE vs ~$10-12/hr DD, 2021).'),
 Q('zoqc22', "I’m a DoorDasher from the West San Fernando Valley part of Los Angeles, and I’m currently at over 5500 deliveries using just my Unagi electric scooter and the Metro Bus system to save battery (I can fold it and store it under the seats).", 'Most experienced two-wheel courier in the corpus; battery range is managed via transit, and his base is a McDonald\'s - the kind of amenity a hub should replicate (charging, wifi, restroom, water).'),
 Q('1245m4q', "These spots are my go-to spots when I start my day delivering for Uber Eats. It’s easy to quickly get an order as soon as you park by one of these. It’s the equivalent of an Uber X driver going to the airport and waiting for a passenger ride.", 'Ghost-kitchen hubs (Colony on Santa Monica Blvd, Melrose Food Co on N Western, Washington Food Co on W Washington, Grand Food Depot on W 38th) are where LA couriers actually stage - candidate hub-adjacency targets.'),
 Q('8n99nv', "HOTSPOT for drivers to pickup orders is at 1842 W. Washington Blvd, LA, CA 90007.  It's CLOUDKITCHEN with about 30 restaurants.  I see mostly, Ubereats, postmates, grubhub, and doordash drivers there.", 'Independent 2018 confirmation of the W Washington Blvd (Pico-Union/West Adams edge) courier cluster.'),
 Q('7t0m96', "i asked uber support, if there are people who do it like me on a bike in LA, they said not in LA , we have in SF and NYC mainly but in LA it's rare.", 'Baseline: in 2018 Uber itself considered LA bike couriers rare - the two-wheel segment is small and must be built, not just served.'),
 Q('1ke5hch', "I've been delivering in L.A. (Culver City, Santa Monica, Hollywood) for almost 6 months but am just getting tired of traffic. Currently considering buying an e-bike to start delivering on instead", '2025 car driver at ~$25/hr contemplating an e-bike: the conversion target persona (traffic-weary, fit, Westside/Hollywood).'),
 Q('udhb8g', "I already tried downtown and I think they don't have it as an option . When I put my 1st application in there was no option for ebike only car or motorcycle.", 'Grubhub LA onboarding had no e-bike option (2022); riders need guidance on registering as motorcycle/car - a service a hub can provide.'),
 Q('cmgyui', "Today it finally started giving motorcycle shifts (I'm in Los Angeles) And it looks like it's actually giving preference to the motorcycle.... It lets me grab a shift with the bike but not when I switch to car. Smart... The bike (motorcycle) is 20 times faster than the car in LA", 'DoorDash motorcycle mode in LA got shift priority (2019) - supports positioning e-mopeds as motorcycle-class.'),
 Q('1hcs3ic', 'I am a female and after a couple of bad experiences I will no longer risk doing deliveries at night.', 'Koreatown resident in the Hollywood-Silverlake zone: night safety limits hours; a staffed hub with lighting/parking addresses a stated pain.'),
 Q('uaf1v3', 'It all felt a little weird, but my first priority was to just gtfo skid row without getting hassled, which I immediately did.', 'Skid Row drop-offs are the DTLA safety complaint; relevant to a 768 Ceres Ave (Skid Row edge) site.'),
 Q('1vcgl9x', 'They took the alcohol, and along with the staff, they went back inside of the home on the corner of Olympic and Cochran. I spent the next hour wasting my time and my breath. DoorDash nor the police did anything', 'Most recent (2026) robbery report, Mid-City; couriers feel unsupported after incidents - an opening for a rider-community hub.'),
 Q('7u8jh1', "i worked this with UberEATS on my bicycle, I am surprised with the number of requests, it's more than what I get in Beverly Hills or Hollywood. I thought nobody lives in downtown, it's only offices,  but I guess I was wrong, so many foreigners rent there. A lot of Asians and international students.", 'Only direct DTLA-vs-Westside-vs-Hollywood comparison from a bicycle courier (r/dtla, 2018): DTLA wins on request volume, driven by downtown renters/students.'),
 Q('1swmlx1', "Santa Monica seems like a nice spot, but high order zones like downtown or koreatown haven’t seemed worth it to me.", '2026 newcomer (car) ranks SM above DTLA/K-town on worth - the Westside counter-argument.'),
 Q('e8om7y', '1 Santa Monica   This is by far the worst place to dash. There is tons of traffic hard to find parking at some places and cops are everywhere.', 'Santa Monica is the worst area for cars - which is precisely why two wheels have an edge there.'),
 Q('188pvss', "I noticed a guy with THREE 😧 phones and all of them had the dasher app turned on. I started a conversation with him, and it turned out that he came from Armenia and doesn’t have legal documents, so he works from fake accounts.", 'Only direct evidence of the undocumented / rented-account courier economy near LA; relevant to KYC and rental terms for a subscription fleet.'),
 Q('c1xrog', 'sidewalk riding seems 5x more popular than street riding at least in K-town/DTLA. Apparently the bus lane is safer than the sidewalk?', '349-upvote r/LosAngeles post: K-town/DTLA is where scooters are ridden (and ticketed) - infrastructure and enforcement context for rider training.'),
]
assert len(top25) == 25

out = dict(
  meta=dict(generated='2026-09-07', corpus_docs=len(corp), corpus_docs_la_verified=sum(1 for c in corp if c['ver']), all_posts=len(posts), la_verified_posts_all_subs=len(la_posts),
            two_wheel_unique_posts=len(TW), two_wheel_docs_incl_crossposts=len(TW) + sum(len(v) for v in CROSSPOSTS.values()),
            method="Every two-wheel/earnings/theft doc and all docs for the small candidate areas were read in full; counts come from curated ID lists (see two_wheel_ids) and regex tallies over docs that pass a stricter LA-verification rule (LA marker present and no out-of-state marker unless a core LA marker also appears). All quotes were asserted to be verbatim substrings of the source post."),
  area_ranking=area_ranking,
  two_wheel_hotspots=two_wheel_hotspots,
  vehicle_types=vehicle_types,
  observational_two_wheel_presence=[dict(id=k, note=v, url=doc(k)['url'], year=doc(k)['year'], score=doc(k)['score']) for k, v in OBSERVATIONAL.items()],
  where_riders_live_or_commute_from=where,
  safety_theft=safety,
  earnings_by_area=earnings_by_area,
  dtla_vs_koreatown_vs_westside=comparison,
  doordash_zone_names=doordash_zone_names,
  data_limits=data_limits,
  top_25_quotes=top25,
)
json.dump(out, open(D + 'analysis_posts.json', 'w'), indent=1, ensure_ascii=False)
json.load(open(D + 'analysis_posts.json'))
print('OK wrote analysis_posts.json')
print('corpus verified', out['meta'])
for r in area_ranking:
    print(f"{r['area']:28s} la={r['la_verified_mentions']:4d} tw={r['two_wheel_mentions']:2d} (docs {r['two_wheel_docs_incl_crossposts']:2d}) car={r['car_mentions']:4d} sent={r['sentiment_for_two_wheel']}")
for z in doordash_zone_names: print(z['count'], z['zone'])
