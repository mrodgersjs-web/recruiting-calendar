#!/usr/bin/env python3
"""
W14: make the carousel click land on the product, not on a biography.

/sports/<slug>/ = the playbooks for that sport + what we do for that sport's families.
/sports/       = the hub that replaces the old "Stories" nav item.

Athlete bios stop being the entry point. They become one-line proof on the sport page
("how this has played out") and stay readable at /story/<id>/ for anyone who wants the
sourced path behind it.

Only existing CSS classes are used (.btn, .btn--primary, .btn--outline, .pb-grid,
.pb-card, .lab, .lede, .note, .cb-page), plus one small inline <style> scoped to the
new pages, so nothing on the site can regress.

Run:  python v3/W14-story/build_sports.py [--dry]
"""
import html
import json
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = pathlib.Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
LIVE = "https://recruiting-calendar.vercel.app"
DRY = "--dry" in sys.argv

# ---------------------------------------------------------------- sport data
# playbooks must be real files under site/playbooks/  (checked at build time)
# rules = the /rules/<rules_sport>/<year>/ family that exists for this sport
SPORTS = [
    dict(slug="football", name="Football",
         blurb="Football starts earlier than most sports. The plan runs from the spring of "
               "sophomore year to signing day, and the rules about when a coach may contact you "
               "are the reason to have dates before you need them.",
         playbooks=["football-junior-year", "walk-on", "offer-and-signing",
                    "eligibility-2-hard-deadlines", "highlight-reel-social", "camp-roi"],
         rules="football"),
    dict(slug="baseball", name="Baseball",
         blurb="Baseball opens later than football, and the showcase calendar has hard entry "
               "dates. Those dates decide who can see your film, so they are worth having in "
               "writing before August.",
         playbooks=["baseball-showcase-to-signing", "eligibility-2-hard-deadlines",
                    "juco-to-d1", "walk-on", "offer-and-signing", "highlight-reel-social"],
         rules="baseball"),
    dict(slug="track-field", name="Track and field",
         blurb="In track, your mark does the first half of the talking. The work is turning times "
               "into a target list and knowing what each program can actually offer you.",
         playbooks=["track-field-marks", "d3-academic-aid-first", "late-bloomer",
                    "eligibility-2-hard-deadlines", "offer-and-signing"],
         rules="track"),
    dict(slug="basketball", name="Basketball",
         blurb="Basketball rosters are small, so most players reach a college program through "
               "film, grades and money rather than one visit. Roster math tells you which of the "
               "three to work on.",
         playbooks=["offer-and-signing", "highlight-reel-social", "eligibility-2-hard-deadlines",
                    "juco-to-d1", "d3-academic-aid-first", "walk-on"],
         rules=None),
    dict(slug="softball", name="Softball",
         blurb="Softball runs on tournaments, camps and film, and on a small number of "
               "scholarship spots per roster. Price the visit before you pay for it.",
         playbooks=["offer-and-signing", "camp-roi", "eligibility-2-hard-deadlines",
                    "highlight-reel-social", "walk-on", "d3-academic-aid-first"],
         rules=None),
    dict(slug="volleyball", name="Volleyball",
         blurb="Volleyball offers come early and in small pieces, so a program's real money and "
               "real roster room matter more than one highlight.",
         playbooks=["walk-on", "highlight-reel-social", "offer-and-signing",
                    "eligibility-2-hard-deadlines", "d3-academic-aid-first"],
         rules=None),
    dict(slug="wrestling", name="Wrestling",
         blurb="Wrestling rosters are deep and most spots open late, so a plan that starts after "
               "junior year still works here. It just has to be a plan.",
         playbooks=["late-bloomer", "d3-academic-aid-first", "offer-and-signing",
                    "highlight-reel-social"],
         rules=None),
    dict(slug="soccer", name="Soccer",
         blurb="Soccer runs through clubs and tryouts more than through school visits, which "
               "makes written interest and academic money the things to track.",
         playbooks=["offer-and-signing", "eligibility-2-hard-deadlines",
                    "highlight-reel-social", "camp-roi", "d3-academic-aid-first"],
         rules=None),
    dict(slug="lacrosse", name="Lacrosse",
         blurb="Lacrosse grew fast, so programs differ more than the label suggests. What a coach "
               "can offer, and when, depends on the level they play at.",
         playbooks=["late-bloomer", "d3-academic-aid-first", "offer-and-signing",
                    "highlight-reel-social"],
         rules=None),
    dict(slug="swimming", name="Swimming and diving",
         blurb="Swimming has the clearest roster math on this list: times, scholarship splits and "
               "relays. The paperwork side still has two dates that can end a plan.",
         playbooks=["eligibility-2-hard-deadlines", "offer-and-signing",
                    "d3-academic-aid-first", "highlight-reel-social"],
         rules=None),
]

FIRST_STEPS = [
    "Set the class year, then get the dated calendar for this sport. Dates come from the rule, "
    "not from a guess.",
    "Build a target list of programs that fit your level, your grades and your family's money.",
    "Make one film a coach will finish watching. Keep the rest of your online presence clean.",
    "Start contact when the rule says a coach may reply, and log every answer in one place.",
]

DO = [
    ("Your dates, in writing", "A calendar for this sport and your class year, each date tied to "
     "the rule it comes from.", "/price/"),
    ("Alerts before every date", "An email 30 days out and another 7 days out, so a window is "
     "never something you find out about after it closed.", "/price/"),
    ("A tracker you own", "Every coach you contact, what they said, and what happens next, in one "
     "place instead of a group chat.", "/tools/contact-log/"),
    ("Scripts, scorecards and checklists", "What to write, what to ask on a visit, and what a red "
     "flag looks like before you sign anything.", "/library/"),
    ("Sport standards and roster math", "What it takes to make a team in this sport at each "
     "level, in numbers a parent can read.", "/recruitiq/"),
    ("NIL checklist for high schoolers", "Check a local deal against your state and school rules "
     "before anyone signs.", "/playbooks/nil-high-school/"),
]

DONT = [
    "We are not an agent. We do not pick your school, contact programs for you, or take a cut of "
    "your deals. Some state and school rules void eligibility when an agent does that, so we stay "
    "out of it.",
    "We do not sell your contact list to colleges or to camps.",
    "We do not promise an offer. We promise the dates, the rules they come from, and the tools to "
    "run the process.",
]

EXTRA_CSS = ("<style>"
             ".cta-band{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:18px 0}"
             ".svc-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));"
             "gap:16px;margin:18px 0}"
             ".svc{border:1px solid var(--c-line);padding:16px;border-radius:10px}"
             ".svc h3{margin:0 0 6px;font-size:inherit}"
             ".svc p{margin:0}"
             ".plans{margin:18px 0}"
             "</style>")

# --------------------------------------------------------------- store slices
STORE_PATH = SITE / "playbooks" / "index.html"
STORE = STORE_PATH.read_text(encoding="utf-8")
head = STORE[:STORE.find("</head>") + 7]
HEADER = STORE[STORE.find("<header"):STORE.find("</header>") + 9]
FOOTER = STORE[STORE.find("<footer"):STORE.find("</footer>") + 9]

def store_cards():
    """Cards lifted out of the live store page, so sport pages and the store cannot disagree."""
    grid_at = STORE.find('<div class="pb-grid">')
    depth = 0
    end = len(STORE)
    for m in re.finditer(r"<(/?)div\b", STORE[grid_at:]):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            end = grid_at + m.end() + len("</div>") - len(">")
            break
    seg = STORE[grid_at:end]
    out = {}
    for chunk in seg.split('<div class="pb-cell">')[1:]:
        # no cell nests another div, so the first close ends it; anything past that
        # is the store's own bundles block and does not belong on a sport page
        body = chunk.split("</div>")[0].strip()
        m = re.search(r'href="?(.*?)\s|>', body)
        m = re.search(r'href="?(/playbooks/([\w-]+))', body)
        if m:
            body = re.sub(r'href="(/playbooks/[\w-]+)/"', 'href="\\1"', body)
        out[m.group(2)] = '<div class="pb-cell">' + body + "</div>"
    return out


CARDS = store_cards()
if not CARDS:
    raise SystemExit("no playbook cards found in the store page")

_js = (SITE / "assets" / "stories.js").read_text(encoding="utf-8")
ATHLETES = json.JSONDecoder().raw_decode(_js[_js.index("{"):])[0]["athletes"]
SPORT_OF = {a["id"]: a.get("sport") or "" for a in ATHLETES}


def sport_slug(sport):
    s = str(sport or "").lower()
    if "track" in s:
        return "track-field"
    if "swim" in s:
        return "swimming"
    if "lacrosse" in s:
        return "lacrosse"
    return re.split(r"[\s(/]+", s)[0]


def match_athletes(sport):
    """Bios that belong on this sport page, keyed off stories.js rather than a hand list."""
    want = sport_slug(sport)
    return [a for a in ATHLETES if sport_slug(a.get("sport")) == want]


# ------------------------------------------------------------------ templates
def make_page(slug, title, desc, main):
    canon = f"{LIVE}/sports/{slug}"
    h = head
    h = re.sub(r"<title>.*?</title>", f"<title>{html.escape(title)}</title>", h, count=1)
    h = re.sub(r'<meta name="description" content="[^"]*"',
               f'<meta name="description" content="{html.escape(desc, quote=True)}"', h, count=1)
    h = re.sub(r'<link rel="canonical" href="[^"]*"', f'<link rel="canonical" href="{canon}"', h, count=1)
    for key, val in (("og:title", title), ("og:description", desc),
                     ("twitter:title", title), ("twitter:description", desc)):
        h = re.sub(rf'<meta (?:property|name)="{key}" content="[^"]*"',
                   f'<meta property="{key}" content="{html.escape(val, quote=True)}"', h, count=1)
    h = re.sub(r'<meta (?:property|name)="(?:og|twitter):image" content="[^"]*"[^>]*>',
               f'<meta property="og:image" content="{LIVE}/assets/logo/social-card-dark.png">', h)
    h = re.sub(r'<meta (?:property|name)="(?:og|twitter):url" content="[^"]*"[^>]*>',
               f'<meta property="og:url" content="{canon}">', h)
    seen = set()  # drop the duplicate social tags the store head carries
    def dedupe(m):
        key = re.search(r'(?:property|name)="([^"]+)"', m.group(0)).group(1)
        if key in seen and key.startswith(("og:", "twitter:")):
            return ""
        seen.add(key)
        return m.group(0)
    h = re.sub(r"<meta (?:property|name)=\"(?:og|twitter):[^\"]+\"[^>]*>", dedupe, h)
    return h + EXTRA_CSS + HEADER + main + FOOTER + (
        f'<script type="application/ld+json">{{"@context":"https://schema.org","@type":'
        f'"CollectionPage","name":{json.dumps(title)},"about":{json.dumps(slug + " recruiting")},'
        f'"isPartOf":"{LIVE}/","url":"{canon}"}}</script></body></html>')


def first_sentence(blurb):
    """Card text has to end on a sentence, or the page reads as one long run."""
    return re.split(r"(?<=\.)\s", blurb)[0]


def headline_tail(sport):
    """Do not promise dates for a sport whose rules we have not checked yet."""
    return "with the dates in hand" if sport["rules"] else "with a plan you can hold"


def cards_for(slugs):
    missing = [s for s in slugs if s not in CARDS or not (SITE / "playbooks" / s / "index.html").exists()]
    if missing:
        raise SystemExit(f"unknown playbook slug(s): {missing}")
    return '<div class="pb-grid">' + "".join(CARDS[s] for s in slugs) + "</div>"


def bullets(items):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def rules_block(sport):
    rs = sport["rules"]
    if not rs:
        return ('<h2>Dates for this sport</h2><p>No dated calendar for this sport yet. We '
                "publish one when every date is checked against the bylaw that sets it, and we "
                "would rather say that than sell you a guess. "
                '<a href="/rules">See the rules we have dated</a>.</p>')
    yrs = "".join(
        f'<li><a href="/rules/{rs}/{y}">Class of {y}</a> <span>contact periods, quiet periods, '
        f"signing dates, and the rule behind each one.</span></li>"
        for y in (2027, 2028, 2029, 2030))
    return (f'<h2>Your dates, by class year</h2><p>These are the {html.escape(sport["name"])} '
            "dates that come straight from the association rule, class year by class year."
            f"<ul>{yrs}</ul>")


def proof_block(sport):
    rows = match_athletes(sport["name"])
    if not rows:
        return ""
    out = []
    for a in rows:
        label = html.escape(a.get("short") or a["name"])
        route = (f'{html.escape(str(a.get("from") or "high school"))} &rarr; '
                 f'{html.escape(str(a.get("college") or ""))}')
        if a.get("page") is False:
            pb = (a.get("playbooks") or ["offer-and-signing"])[0]
            out.append(f'<li>{label} <span>{route}. Composite, built from public reporting; '
                       f'sources on <a href="/playbooks/{pb}/#sources">the playbook</a>.</span></li>')
        else:
            out.append(f'<li><a href="/story/{a["id"]}">{label}</a> <span>{route}. Public sources, '
                       f"listed on that page.</span></li>")
    return ('<h2>How this has played out</h2><p class="note">Not endorsements, and not ads. '
            "Publicly reported recruiting paths, shortened to what a parent can copy.</p>"
            "<ul>" + "".join(out) + "</ul>")


def build_sport(sport):
    name = sport["name"]
    title = f"{name} recruiting: playbooks, dates and tools for parents"
    desc = (f"{name} recruiting plans for parents: playbooks, dated rules where we have them, "
            "alerts, a tracker, and what we do not do.")
    main = "".join([
        '<main class="cb-page">',
        f'<p class="lab">{html.escape(name)}</p>',
        f'<h1 class="d1">Run {html.escape(name.lower())} recruiting {headline_tail(sport)}</h1>',
        f'<p class="lede">{html.escape(sport["blurb"])}</p>',
        '<p class="cta-band"><a class="btn btn--primary" href="/price">Get the calendar for your '
        'class year</a> <a class="btn btn--outline" href="/sports">Every sport we cover</a></p>',
        "<h2>Playbooks for this sport</h2>",
        "<p>Each playbook is a plan you run, priced on its own. No subscription needed.</p>",
        cards_for(sport["playbooks"]),
        rules_block(sport),
        f'<h2>What we do for {html.escape(name.lower())} families</h2>',
        '<div class="svc-grid">' + "".join(
            f'<div class="svc"><h3>{t}</h3><p class="note">{b} <a href="{href}">Details</a></p></div>'
            for t, b, href in DO) + "</div>",
        "<h2>What to do first</h2>",
        bullets(FIRST_STEPS),
        "<h2>What we do not do</h2>",
        bullets(DONT),
        '<p class="plans note">Plans: free preview, Sideline $149 per year with a 14-day free '
        'trial, Pathway $499 planned and not for sale yet. <a href="/price">Full price list</a>.</p>',
        proof_block(sport),
        '<p class="cta-band"><a class="btn btn--primary" href="/start">Start free with your '
        'sport and class year</a> <a class="btn btn--outline" href="/library">Browse every tool</a></p>',
        "</main>",
    ])
    return make_page(sport["slug"], title, desc, main)


def build_hub():
    title = "Recruiting playbooks and dates, by sport"
    desc = ("Pick your sport and get the playbooks, the dates that come from the rule, the alerts "
            "and the tracker.")
    tiles = "".join(
        f'<div class="pb-cell"><a class="pb-card" href="/sports/{s["slug"]}">'
        f'<span class="pb-thumb"><b>{html.escape(s["name"])}</b>'
        f'<i>{len(s["playbooks"])} playbooks'
        f'{" &middot; dated rules" if s["rules"] else " &middot; rules coming"}</i></span>'
        f'<span class="lab">{"Dated rules live" if s["rules"] else "Playbooks and tools"}</span>'
        f'<span class="pb-t">{html.escape(s["name"])}</span>'
        f'<span class="pb-s">{html.escape(first_sentence(s["blurb"]))}</span></a></div>'
        for s in SPORTS)
    main = ('<main class="cb-page">'
            '<p class="lab">By sport</p>'
            '<h1 class="d1">Every plan, by the sport you actually play</h1>'
            '<p class="lede">Pick a sport. You get its playbooks, its dates, and the tools that keep '
            "you on schedule. No story to read first.</p>"
            f'<div class="pb-grid">{tiles}</div>'
            "<h2>Why the plans are split by sport</h2>"
            "<p>A football timeline does not fit a softball family. The rules on when a coach can call "
            "you differ by sport. So do camp dates, signing dates, and how many spots a team "
            "can hand out. So each page lists only what we checked for that sport. Where we "
            "have not checked it yet, the page says so plain.</p>"
            '<p class="cta-band"><a class="btn btn--primary" href="/start">Start free with your '
            'sport and class year</a> <a class="btn btn--outline" href="/price">See plans and price</a></p>'
            "</main>")
    return make_page("index", title, desc, main)


# ----------------------------------------------------------- rotator retarget
def patch_ring():
    p = SITE / "assets" / "ring.js"
    t = p.read_text(encoding="utf-8")
    before = t
    t = t.replace("location.href='/story/'+a.id", "location.href=SPORT_PATH(a)")
    if "function SPORT_PATH" not in t:
        t = ("function SPORT_PATH(a){var s=String(a.sport||'').toLowerCase();"
             "if(s.indexOf('track')>-1)return'/sports/track-field/';"
             "if(s.indexOf('swim')>-1)return'/sports/swimming/';"
             "if(s.indexOf('lacrosse')>-1)return'/sports/lacrosse/';"
             "return '/sports/'+s.split(/[\\s(/]+/)[0]+'/';}\n" + t)
    return p, before, t


def patch_deck():
    p = SITE / "assets" / "deck.js"
    t = p.read_text(encoding="utf-8")
    before = t
    old = '''<a class="btn btn--primary dk-read" href="/story/'+esc(a.id)+'/">Read the story</a>'''
    new = pathlib.Path(__file__).with_name("deck-cta.txt").read_text(encoding="utf-8").strip()
    t = t.replace(old, new)
    if "function SLUG" not in t:
        t = ("function SLUG(s){s=String(s||'').toLowerCase();"
             "if(s.indexOf('track')>-1)return'track-field';if(s.indexOf('swim')>-1)return'swimming';"
             "if(s.indexOf('lacrosse')>-1)return'lacrosse';return s.split(/[\\s(/]+/)[0];}\n" + t)
    return p, before, t


# ------------------------------------------------- story pages get a sport CTA
BAND = ('<p class="cta-band" style="display:flex;flex-wrap:wrap;gap:10px;margin:18px 0">'
        '<a class="btn btn--primary" href="/sports/{slug}/">Playbooks and dates for {name}</a> '
        '<a class="btn btn--outline" href="/sports/">Every sport</a></p>')


def patch_story_pages():
    n = 0
    for p in sorted((SITE / "story").glob("*/index.html")) + sorted((SITE / "athlete").glob("*/index.html")):
        t = p.read_text(encoding="utf-8")
        if "/sports/" in t:
            continue
        sport = SPORT_OF.get(p.parent.name)
        if not sport:
            continue
        band = BAND.format(slug=sport_slug(sport), name=html.escape(sport.split(" (")[0]))
        i = t.find("<main")
        j = t.find(">", i) + 1
        p.write_text(t[:j] + band + t[j:], encoding="utf-8")
        n += 1
    return n


# --------------------------------------------------------------- nav + footer
def patch_nav():
    """'Stories' in the header and footer now points at the sport hub."""
    n = 0
    pats = [(f'<a href="{a}"{sp}>Stories</a>', f'<a href="{b}"{sp}>By sport</a>')
            for a, b in (("/", "/sports"), ("/story", "/sports"), ("/story/", "/sports/"))
            for sp in ("", " ")]
    for p in sorted(SITE.rglob("*.html")):
        t = p.read_text(encoding="utf-8", errors="ignore")
        orig = t
        for pat, rep in pats:
            t = t.replace(pat, rep)
        if t != orig:
            p.write_text(t, encoding="utf-8")
            n += 1
    return n


def main():
    pages = {f"sports/{s['slug']}/index.html": build_sport(s) for s in SPORTS}
    pages["sports/index.html"] = build_hub()
    print("== pages that will be written")
    for path, body in pages.items():
        urls = sorted(set(re.findall(r'href="?(/[\w/-]+)', body)))
        dead = [u for u in urls if u.rstrip("/").split("/")[-1] not in ("", "story")
                and not (SITE / u.strip("/") / "index.html").exists()
                and not (SITE / (u.strip("/") + ".html")).exists()]
        print(f"   /{path.replace('index.html', ''):24} {len(body):7,} bytes  "
              f"links={len(urls):3}  unresolved={dead or 'none'}")
        if DRY:
            continue
        f = SITE / path
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(body, encoding="utf-8")
    if DRY:
        print("\n(dry run: nothing written)")
        print(build_sport(SPORTS[0]))
        return
    for p, before, new in (patch_ring(), patch_deck()):
        p.write_text(new, encoding="utf-8")
        print(f"== {p.name}: {'patched' if before != new else 'NO CHANGE (pattern missed!)'}")
    print(f"== story pages given a sport CTA: {patch_story_pages()}")
    print(f"== pages whose Stories link moved to /sports/: {patch_nav()}")


main()
