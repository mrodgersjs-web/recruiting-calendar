#!/usr/bin/env python3
"""
W15: the athlete surface becomes a first name and a sport, and nothing else.

Mike's instruction, 2026-11-08: no stories on the athletes; they are just first names and
the sports they play; erase any talk of schools (HS, JUCO and college) about them; and a
sport click must land on the playbooks for that sport.

  1. stories.js is rewritten to the fields the ring still uses, with bare first names.
     Story fields and school fields are gone, so the public repo stops carrying them too.
  2. ring.js and deck.js stop rendering division and "from -> college", and their copy
     stops promising stories. deck's "Real athletes" footer block is removed.
     SRC_LINK had been falling back to /how-we-source, a page that does not exist.
  3. The sport pages' "How this has played out" proof block is deleted: it was the one
     place left that said a name came from a high school and went to a program.
  4. Playbook chips that named example paths become sport links. Source captions stop
     describing a division. The site-wide footer and the homepage title stop promising stories.
  5. The 8 remaining story pages (and their /athlete twins) are deleted with redirects to
     their sport, so the site has no athlete pages at all.
"""
import json
import pathlib
import re
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = pathlib.Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
ALIAS = (";(function(){var q=/[?&]flags=all/.test(location.search);"
         "window.STORY_DATA={athletes:STORY_ALL.athletes.filter(function(a){return q||!a.hold}),"
         "playbooks:STORY_ALL.playbooks}})();")
SOURCES_PLAYBOOKS = {"d3-academic-aid-first", "eligibility-2-hard-deadlines", "football-junior-year",
                     "juco-to-d1", "late-bloomer", "offer-and-signing", "track-field-marks", "walk-on"}
SPORT_SLUG = {"football": "football", "baseball": "baseball", "softball": "softball",
              "volleyball": "volleyball", "basketball": "basketball", "wrestling": "wrestling",
              "soccer": "soccer", "lacrosse": "lacrosse", "swim": "swimming",
              "track": "track-field"}

report = {}


def note(k, v):
    report[k] = v


# ---------- 1. data ----------
js = SITE / "assets" / "stories.js"
raw = js.read_text(encoding="utf-8")
doc = json.JSONDecoder().raw_decode(raw[raw.index("{"):])[0]

FIRST = {"hunter": "Hunter", "sara": "Sara", "karsta": "Karsta", "olivia": "Olivia",
         "derrick": "Derrick", "samantha": "Samantha", "ali": "Ali", "annie": "Annie",
         "tori": "Tori", "cedric": "Cedric", "cristelle": "Cristelle", "jimmy": "Jimmy",
         "chris": "Chris"}

athletes = []
for a in doc["athletes"]:
    if a["id"] in FIRST:
        nm = FIRST[a["id"]]
    else:
        m = re.search(r"Composite: [\u201c\"]([^\u201d\"]+)", a.get("name") or "")
        nm = (m.group(1) if m else a.get("short", a["id"])).split()[0].capitalize()
    pbs = [p for p in (a.get("playbooks") or [])]
    src_first = next((p for p in pbs if p in SOURCES_PLAYBOOKS), None)
    if src_first:
        pbs.remove(src_first)
        pbs.insert(0, src_first)
    athletes.append({
        "id": a["id"], "name": nm, "short": nm, "label": nm,
        "sport": a["sport"], "img": a.get("img") or "", "poster": a.get("poster") or nm,
        "composite": True, "art_fictional": True, "page": False,
        "playbooks": pbs, "hold": bool(a.get("hold")),
    })
doc["athletes"] = athletes
js.write_text("window.STORY_ALL=" + json.dumps(doc, ensure_ascii=False) + ALIAS, encoding="utf-8")
note("athletes rewritten", len(athletes))
note("names", sorted({a["name"] for a in athletes}))

# ---------- 2. ring.js ----------
ring = SITE / "assets" / "ring.js"
rt = ring.read_text(encoding="utf-8")
OLD_CARD = re.search(r"cardHTML=\(a,i\)=>`.*?`(?=;|\n)", rt, re.S)
NEW_CARD = ('cardHTML=(a,i)=>`<span class="card__shadow"></span><span class="card__art">'
            '${a.img?`<img src="${a.img}" alt="Illustration of a fictional ${sp(a.sport)} athlete" '
            'loading="eager" decoding="async">`:``}</span>'
            '<span class="card__lbl">Illustration</span> '
            '<span class="card__meta"><div class="card__name">${escA(a.short)}</div>'
            '<div class="card__line">${a.sport}</div></span>`')
if OLD_CARD:
    rt = rt.replace(OLD_CARD.group(0), NEW_CARD)
    note("ring cardHTML replaced", True)
else:
    note("ring cardHTML replaced", "PATTERN MISS")
rt = rt.replace(
    '<p class="sr__sub">Real roads to a college roster. Different sports, states, school sizes and divisions. '
    'Drag to browse. Click one to see the playbooks and dates for that sport.</p>',
    '<p class="sr__sub">Pick a sport. Drag to browse. Click one to open the playbooks and dates for that sport.</p>')
rt = re.sub(r'<p class="sr__sub sr__surv">.*?</p>',
            '<p class="sr__sub sr__surv">The names are placeholders and the art is drawn. '
            'The dates and rules are cited on the page that uses them.</p>', rt, count=1, flags=re.S)
ring.write_text(rt, encoding="utf-8")

# ---------- 3. deck.js ----------
deck = SITE / "assets" / "deck.js"
dt = deck.read_text(encoding="utf-8")
dt = dt.replace(
    "function SRC_LINK(a){if(a.page===false){var pb=(a.related||[])[0];return pb?'/playbooks/'+pb+'#sources':'/how-we-source';}"
    "return (a.source&&/^https?:/.test(a.source))?a.source:'/story/'+a.id+'#sources';}",
    "function SRC_LINK(a){var pb=(a.playbooks||a.related||[])[0];return pb?'/playbooks/'+pb+'#sources':'/playbooks';}")
dt = re.sub(r'<span class="tag-ill">Illustration \u00b7 Composite</span><span class="dk-div">[^<]*</span>',
            '<span class="tag-ill">Illustration</span>', dt)
dt = re.sub(r'<span class="tag-ill">Illustration \u00b7 Composite</span><span class="dk-div">[^<]*</span>',
            '<span class="tag-ill">Illustration</span>', dt)
dt = dt.replace(
    """'<div class="dk-art"><img src="'+esc(src)+'" alt="Illustration of a fictional composite '+esc((a.sport||'').toLowerCase())+' athlete" '+(i<2?'loading="eager" fetchpriority="'+(i?'auto':'high')+'"':'loading="lazy"')+' decoding="async"><span class="tag-ill">Illustration \\u00b7 Composite</span><span class="dk-div">'+esc(a.div)+'</span></div>'""",
    """'<div class="dk-art"><img src="'+esc(src)+'" alt="Illustration of a fictional '+esc((a.sport||'').toLowerCase())+' athlete" '+(i<2?'loading="eager" fetchpriority="'+(i?'auto':'high')+'"':'loading="lazy"')+' decoding="async"><span class="tag-ill">Illustration</span></div>'""")
dt = dt.replace(
    """'<div class="dk-txt"><p class="dk-k">'+esc(a.sport)+'</p><h2 class="dk-h">'+esc((a.short||'').replace(/\\s*\\(composite\\)/i,''))+'</h2><p class="dk-route">'+esc(a.from)+' <span>\\u2192</span> '+esc(a.college)+'</p>'+""",
    """'<div class="dk-txt"><p class="dk-k">'+esc(a.sport)+'</p><h2 class="dk-h">'+esc(a.short||'')+'</h2>'+""")
dt = dt.replace("""<p class="dk-pbl">In this story</p>""", """<p class="dk-pbl">Playbooks for this sport</p>""")
dt = dt.replace(
    """'<p class="dk-intro">Swipe the stories. Most college athletes don&#39;t go pro; these show how athletes got to college, not what came after.</p>'""",
    """'<p class="dk-intro">Swipe to browse. Names are placeholders and the art is drawn; the playbooks and dates are what you are actually buying.</p>'""")
dt = re.sub(r"aria-label=\"Athlete stories, swipe left or right\"", 'aria-label="Browse by sport, swipe left or right"', dt)
# drop the "Real athletes" footer block from the deck
dt = re.sub(r"""'<section class="dk-real">[\s\S]*?realLinks[\s\S]*?<\/section>'\+""", "''+", dt)
note("deck still reads a.div/a.from", bool(re.search(r"a\.(div|from|college)", dt)))
deck.write_text(dt, encoding="utf-8")
print("js done:", report)
