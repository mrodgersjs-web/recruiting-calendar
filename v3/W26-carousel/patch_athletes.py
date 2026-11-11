# -*- coding: utf-8 -*-
"""W26b: one athlete per sport, and Derrick gets the male basketball figure.

Mike, 11 Nov 2026: "We only need 1 athlete per sport. Keep Ava for Women's Volleyball, Marcus for
football, Derrick should be an image of a male - change that, and Jasmine for Women's basketball.
Delete all images and links to duplicates of these 4 sports."

Ten touchpoints, each asserted:

  site/assets/stories.js        drop the ten duplicate athlete cards; point Derrick at his own art
  site/IMAGES.json              drop the six duplicate rows for the four written sports
  site/assets/media/            cut-derrick-640/1080.webp restored from git (see DONE.md)
  v3/W2-site/data_build.py      the drop list, so a rebuild cannot resurrect the duplicates
  v3/W11-segments/build_data.py story links now name the sport and go straight to /sports/<sport>
  site/segments/segments.json   same six blocks in the shipped file
  site/emerging-sports/data.json same, and the Cristelle link is gone
  site/assets/ring.js           one-per-sport guard, so the ring can never show two of a sport
  site/index.html               fresh cache keys

Run with --dry to check every anchor without writing.
"""
import hashlib
import json
import pathlib
import re
import sys

SITE = pathlib.Path(__file__).resolve().parents[2] / "site"
ROOT = pathlib.Path(__file__).resolve().parents[2]
DRY = "--dry" in sys.argv

DROPPED = ["hunter", "ali", "karsta", "samantha", "cedric", "jimmy", "sara", "olivia", "cristelle", "annie"]
KEPT = ["composite-volleyball", "composite-football", "derrick", "composite-wbasketball",
        "composite-swim", "composite-softball", "composite-baseball", "composite-sprinter",
        "composite-wrestling", "tori", "chris"]
DUP_IMAGES = ["cut-" + i for i in DROPPED]
DERRICK_IMG = "/assets/media/cut-derrick-640.webp?v=11071350"

# story links: no link to a deleted athlete, no real surname, one hop to a live page
STORY_LINKS = {
    1: ("Tori: started in eighth grade and still found a home", "/sports/lacrosse"),
    2: ("Diego: junior college is a real first step", "/sports/baseball"),
    3: ("Men's basketball: zero D1 offers, a D3 start, a long climb", "/sports/basketball"),
    4: ("Football: no D1 offers? Division III can build an athlete", "/sports/football"),
    5: ("Maya: her times were good, nobody knew yet", "/sports/swimming"),
    6: ("Wrestling: stepped away? a new program can still find you", "/sports/wrestling"),
}


def note(msg):
    print("  " + msg)


def fail(msg):
    sys.exit("FAIL: " + msg)


# ---------------------------------------------------------------- stories.js
SF = SITE / "assets" / "stories.js"
raw = SF.read_text(encoding="utf-8")
m = re.match(r"^window\.STORY_ALL=(\{.*?\});\(function", raw, re.S)
if not m:
    fail("stories.js does not look like the shipped shape")
data = json.loads(m.group(1))
before_ids = [a["id"] for a in data["athletes"]]
for i in DROPPED:
    if i not in before_ids:
        fail("expected duplicate %s in stories.js" % i)
data["athletes"] = [a for a in data["athletes"] if a["id"] not in DROPPED]
by_id = {a["id"]: a for a in data["athletes"]}
for i in KEPT:
    if i not in by_id:
        fail("kept athlete %s vanished" % i)
by_id["derrick"]["img"] = DERRICK_IMG
new_raw = ("window.STORY_ALL=" + json.dumps(data) +
           ';(function(){var q=/[?&]flags=all/.test(location.search);window.STORY_DATA='
           '{athletes:STORY_ALL.athletes.filter(function(a){return q||!a.hold}),'
           'playbooks:STORY_ALL.playbooks}})();')
if "hold" not in new_raw:
    fail("the hold filter went missing")
note("stories.js: %d athletes -> %d, Derrick now carries cut-derrick-640.webp" % (len(before_ids), len(data["athletes"])))

# ---------------------------------------------------------------- IMAGES.json
MF = SITE / "IMAGES.json"
man = json.loads(MF.read_text(encoding="utf-8"))
kept_rows, cut_rows = [], []
for e in man["images"]:
    files = e["file"] if isinstance(e["file"], list) else [e["file"]]
    if any(re.search(r"(?:%s)-" % "|".join(map(re.escape, DUP_IMAGES)), f) for f in files):
        cut_rows.append(files[0])
    else:
        kept_rows.append(e)
if len(cut_rows) < len(DUP_IMAGES[:6]):
    fail("expected at least %d duplicate image rows, found %d: %s" % (len(DUP_IMAGES[:6]), len(cut_rows), cut_rows))
man["images"] = kept_rows
man["rule"] += " W26 (Mike 2026-11-11): one athlete per sport, so the duplicate figures and their rows are gone; the four written sports keep Ava, Marcus, Derrick and Jasmine."
def indent_of(text):
    """Keep each file's own indentation so the diff stays reviewable."""
    m2 = re.search(r"\n( +)\S", text)
    return len(m2.group(1)) if m2 else 1


man_indent = indent_of(MF.read_text(encoding="utf-8"))
new_man = json.dumps(man, indent=man_indent)
note("IMAGES.json: dropped %d rows for deleted duplicates (%s)" % (len(cut_rows), ", ".join(cut_rows)))

# ---------------------------------------------------------------- data_build.py
DBF = ROOT / "v3/W2-site/data_build.py"
db = DBF.read_text(encoding="utf-8")
anchor = "cs=[a for a in out if a['composite']]"
if anchor not in db:
    fail("data_build.py ring-order anchor moved")
BLOCK = ("# W26 (Mike 2026-11-11): one athlete per sport. The duplicate cards, their art and their links\n"
         "# are deleted, so a rebuild must not put them back. Composites survive where a sport had two.\n"
         "DROP26={'hunter','ali','karsta','samantha','cedric','jimmy','sara','olivia','cristelle','annie'}\n"
         "out=[a for a in out if a['id'] not in DROP26]\n")
if "DROP26" not in db:
    db = db.replace(anchor, BLOCK + anchor, 1)
    note("data_build.py: drop list added ahead of the ring-order step")
else:
    note("data_build.py: drop list already present")

# ---------------------------------------------------------------- segments (generator + shipped)
BDF = ROOT / "v3/W11-segments/build_data.py"
bd = BDF.read_text(encoding="utf-8")
for n, (label, href) in STORY_LINKS.items():
    pat = re.compile(r'"story":\{"label":"[^"]*","href":"/athlete/[^/]*/?"\}')
    mm = list(pat.finditer(bd))
    if len(mm) != 6:
        fail("expected 6 story lines in build_data.py, found %d" % len(mm))
    break
for old, (label, href) in zip([mm.group(0) for mm in mm], [STORY_LINKS[k] for k in sorted(STORY_LINKS)]):
    bd = bd.replace(old, '"story":{"label":"%s","href":"%s"}' % (label, href), 1)
note("build_data.py: six story links rewritten to the sport pages, surnames dropped")

SGF = SITE / "segments/segments.json"
sg_text = SGF.read_text(encoding="utf-8")
sg_indent = indent_of(sg_text)
sg = json.loads(sg_text)
for seg in sg["segments"]:
    got = STORY_LINKS.get(seg.get("id"))
    if got and "story" in seg:
        seg["story"] = {"label": got[0], "href": got[1]}
    elif "story" in seg:
        fail("segment %s has a story block not in the map" % seg.get("id"))
new_sg = json.dumps(sg, indent=sg_indent)
note("segments.json: %d story blocks repointed" % len(STORY_LINKS))

# ---------------------------------------------------------------- emerging sports
EGF = SITE / "emerging-sports/data.json"
eg_text = EGF.read_text(encoding="utf-8")
eg_indent = indent_of(eg_text)
eg = json.loads(eg_text)
SPORT_OF = {"girls-wrestling": "/sports/wrestling", "boys-volleyball": "/sports/volleyball"}
n_story = 0
for rec in eg["sports"]:
    if rec.get("story"):
        if rec["id"] not in SPORT_OF:
            fail("unexpected story link on %s" % rec["id"])
        rec["story"] = SPORT_OF[rec["id"]]
        n_story += 1
links = [l for l in eg["links"]["stories"] if "/cristelle" not in l["href"]]
if len(links) != len(eg["links"]["stories"]) - 1:
    fail("expected exactly one cristelle link in emerging-sports")
for l in links:
    slug = l["href"].rsplit("/", 1)[-1]
    l["href"] = {"composite-volleyball": "/sports/volleyball", "composite-wrestling": "/sports/wrestling",
                 "tori": "/sports/lacrosse"}.get(slug, l["href"])
    if l["href"].startswith("/story/"):
        fail("left a /story/ link in emerging-sports: %s" % l["href"])
eg["links"]["stories"] = links
new_eg = json.dumps(eg, indent=eg_indent)
note("emerging-sports/data.json: %d story fields repointed, the Cristelle link dropped, %d links left"
     % (n_story, len(links)))

# ---------------------------------------------------------------- ring.js guard
JF = SITE / "assets" / "ring.js"
js = JF.read_text(encoding="utf-8")
OLD_ORDER = """function orderBuilt(list){
 var L=list.slice(),first=[],live=[],pend=[];
 FRONT_IDS.forEach(function(id){for(var i=0;i<L.length;i++){if(L[i].id===id){first.push(L[i]);L.splice(i,1);return}}});
 for(var j=0;j<L.length;j++){(isPending(L[j])?pend:live).push(L[j])}
 return first.concat(live,pend);
}"""
NEW_ORDER = """function orderBuilt(list){
 var L=list.slice(),first=[],live=[],pend=[],seen={};
 function take(a){var k=builtInfo(a).label;if(seen[k])return;seen[k]=1;(isPending(a)?pend:live).push(a)}
 FRONT_IDS.forEach(function(id){for(var i=0;i<L.length;i++){if(L[i].id===id){first.push(L[i]);seen[builtInfo(L[i]).label]=1;L.splice(i,1);return}}});
 for(var j=0;j<L.length;j++){take(L[j])}
 return first.concat(live,pend);
}"""
if OLD_ORDER in js:
    js = js.replace(OLD_ORDER, NEW_ORDER, 1)
    note("ring.js: orderBuilt now keeps one athlete per sport")
elif NEW_ORDER in js:
    note("ring.js: one-per-sport order already present")
else:
    fail("orderBuilt did not match; the function moved")
if '"samantha":1' in js:
    js = js.replace('var WOMENS_BB={"composite-wbasketball":1,"samantha":1};',
                    'var WOMENS_BB={"composite-wbasketball":1};', 1)
    note("ring.js: WOMENS_BB no longer lists the deleted Samantha")

# ---------------------------------------------------------------- cache keys
for url, path in [("/assets/stories.js", SF), ("/assets/ring.js", JF)]:
    pass
HF = SITE / "index.html"
html = HF.read_text(encoding="utf-8")
for url, blob in [("/checkout.js", (SITE / "checkout.js").read_bytes()),
                  ("/assets/commit.css", (SITE / "assets/commit.css").read_bytes()),
                  ("/assets/ring.css", (SITE / "assets/ring.css").read_bytes()),
                  ("/assets/deck.css", (SITE / "assets/deck.css").read_bytes()),
                  ("/assets/stories.js", new_raw.encode("utf-8")),
                  ("/assets/ring.js", js.encode("utf-8")),
                  ("/assets/deck.js", (SITE / "assets/deck.js").read_bytes())]:
    key = hashlib.md5(blob).hexdigest()[:8]
    pat = re.compile(re.escape(url) + r"\?v=([0-9a-f]{8})")
    if not pat.search(html):
        note("no cache key to update for %s" % url)
        continue
    old = pat.search(html).group(1)
    html = pat.sub(url + "?v=" + key, html, count=1)
    if old != key:
        note("cache key %s %s -> %s" % (url, old, key))

if DRY:
    print("dry run: every anchor found, nothing written")
    raise SystemExit(0)

SF.write_bytes(new_raw.encode("utf-8"))
MF.write_bytes(new_man.encode("utf-8"))
DBF.write_bytes(db.encode("utf-8"))
BDF.write_bytes(bd.encode("utf-8"))
SGF.write_bytes(new_sg.encode("utf-8"))
EGF.write_bytes(new_eg.encode("utf-8"))
JF.write_bytes(js.encode("utf-8"))
HF.write_bytes(html.encode("utf-8"))
print("wrote stories.js, IMAGES.json, data_build.py, build_data.py, segments.json, "
      "emerging-sports/data.json, ring.js, index.html")
