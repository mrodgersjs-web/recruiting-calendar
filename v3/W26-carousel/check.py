# -*- coding: utf-8 -*-
"""W26 gate for the athlete carousel: one athlete per sport, the four written playbooks first,
pending sports greyed and inert, and no trace of the deleted duplicates except their 301s.

Run: python v3/W26-carousel/check.py
"""
import hashlib
import json
import pathlib
import re
import sys
from collections import Counter

import PIL
from PIL import Image

SITE = pathlib.Path(__file__).resolve().parents[2] / "site"
ROOT = pathlib.Path(__file__).resolve().parents[2]
html = (SITE / "index.html").read_text(encoding="utf-8")
js = (SITE / "assets" / "ring.js").read_text(encoding="utf-8")
css = (SITE / "assets" / "ring.css").read_text(encoding="utf-8")
stories = (SITE / "assets" / "stories.js").read_text(encoding="utf-8")

DROPPED = ["hunter", "ali", "karsta", "samantha", "cedric", "jimmy", "sara", "olivia", "cristelle", "annie"]
NAMES = ["Hunter", "Ali", "Karsta", "Samantha", "Cedric", "Jimmy", "Sara", "Olivia", "Cristelle", "Annie"]
WRITTEN = ["Women's Volleyball", "Men's Football", "Men's Basketball", "Women's Basketball"]

fails = []


def ok(label):
    print("  PASS  %s" % label)


def bad(label):
    fails.append(label)
    print("  FAIL  %s" % label)


data = json.loads(re.search(r"window\.STORY_ALL=(\{.*?\});\(function", stories, re.S).group(1))
athletes = data["athletes"]
womens_bb = set(re.findall(r'"([^"]+)":1', re.search(r"var WOMENS_BB=\{(.*?)\}", js).group(1)))


def built_info(a):
    s = a["sport"].lower()
    if "volleyball" in s:
        return True, "Women's Volleyball"
    if "football" in s:
        return True, "Men's Football"
    if "basketball" in s:
        return True, "Women's Basketball" if a["id"] in womens_bb else "Men's Basketball"
    return False, a["sport"]


front_ids = re.findall(r'"([^"]+)"', re.search(r"var FRONT_IDS=\[(.*?)\]", js).group(1))


def ring_order():
    """orderBuilt, reimplemented: front four, then one per sport, written sports first."""
    L = list(athletes)
    first, live, pend, seen = [], [], [], {}
    for i in front_ids:
        for a in list(L):
            if a["id"] == i:
                first.append(a)
                seen[built_info(a)[1]] = 1
                L.remove(a)
                break
    for a in L:
        label = built_info(a)[1]
        if label in seen:
            continue
        seen[label] = 1
        (pend if not built_info(a)[0] else live).append(a)
    return first + live + pend


order = ring_order()

# 1. one athlete per sport ------------------------------------------------------------
print("the ring, one card per sport")
for i, a in enumerate(order, 1):
    is_built, label = built_info(a)
    print("  %2d  %-8s %-22s %s   %s" % (i, a["name"], label, a["img"].split("?")[0],
                                         "" if is_built else " <- greyed, stamped, inert"))
labels = [built_info(a)[1] for a in order]
if len(labels) != len(set(labels)):
    bad("a sport appears twice: %s" % [k for k, v in Counter(labels).items() if v > 1])
else:
    ok("%d cards, no sport appears twice" % len(labels))
if labels[:4] != WRITTEN:
    bad("the first four are %s" % labels[:4])
else:
    ok("athletes 1-4 are women's volleyball, men's football, men's basketball, women's basketball")
if all(not built_info(a)[0] for a in order[4:]):
    ok("%d pending sports sit after the four written ones" % (len(order) - 4))
else:
    bad("a pending sport is mixed in with the written ones")
for a in athletes:
    if a.get("hold"):
        bad("%s is still held back instead of deleted" % a["id"])

# 2. the deleted duplicates are gone from the shipped site ----------------------------
print("\nno trace of the deleted duplicates")
for p in sorted(SITE.rglob("*")):
    if p.suffix.lower() not in (".html", ".js", ".json", ".css", ".xml") or not p.is_file():
        continue
    rel = str(p.relative_to(SITE)).replace("\\", "/")
    t = p.read_text(encoding="utf-8", errors="ignore")
    # "Jimmy Butler" on two playbook pages is a real person in a source citation, not our athlete
    t = re.sub(r"(?i)jimmy[ _-]butler", "CITEDPERSON", t)
    hits = [n for n in NAMES + DROPPED if re.search(r"(?<![A-Za-z-])" + n + r"(?![A-Za-z-])", t)]
    if rel == "IMAGES.json":
        hits = [h for h in hits if h in NAMES]
    if hits:
        bad("%s still mentions %s" % (rel, ", ".join(sorted(set(hits)))))
if not fails:
    ok("no shipped file mentions a deleted athlete")
redir = (ROOT / "vercel.json").read_text(encoding="utf-8")
missing = [i for i in DROPPED if '/story/%s' % i not in redir]
if missing:
    bad("301s missing for %s" % missing)
else:
    ok("every deleted athlete still 301s to its sport page, so old links and bookmarks survive")
man = json.loads((SITE / "IMAGES.json").read_text(encoding="utf-8"))
blob = json.dumps(man)
leftover = [d for d in DROPPED if '"cut-%s-' % d in blob]
if leftover:
    bad("IMAGES.json still has rows for %s" % leftover)
else:
    ok("IMAGES.json: %d rows, none of them a deleted athlete" % len(man["images"]))

# 3. no page links to a deleted athlete page -----------------------------------------
print("\nstory links")
bad_hrefs = []
for rel in ("segments/segments.json", "emerging-sports/data.json"):
    t = (SITE / rel).read_text(encoding="utf-8")
    bad_hrefs += [rel + " -> " + h for h in re.findall(r"/(?:story|athlete)/[a-z0-9-]+", t)]
if bad_hrefs:
    for b in bad_hrefs:
        bad(b)
else:
    ok("segments and emerging-sports point straight at /sports pages, no surname labels")
bd = (ROOT / "v3/W11-segments/build_data.py").read_text(encoding="utf-8")
if re.search(r'"href":"/athlete/', bd):
    bad("build_data.py would put the athlete links back on the next build")
else:
    ok("the segments generator itself emits /sports links, so a rebuild keeps this")
surnames = ["Perez", "Coward", "Marpet", "Rodriguez"]
if [s for s in surnames if s in bd]:
    bad("a real surname is back in the segments generator")
else:
    ok("no real surnames left in the segment story labels")

# 4. Derrick's figure ---------------------------------------------------------------
print("\nthe men's basketball figure")
derrick = next(a for a in athletes if a["id"] == "derrick")
if derrick["img"].startswith("/assets/media/cut-derrick-640.webp"):
    ok("Derrick's card points at cut-derrick-640.webp")
else:
    bad("Derrick's card points at %s" % derrick["img"])
media = SITE / "assets" / "media"
for f in ("cut-derrick-640.webp", "cut-derrick-1080.webp"):
    p = media / f
    if not p.exists():
        bad("%s is missing (deck.js swaps -640 for -1080 at runtime)" % f)
        continue
    im = Image.open(p).convert("RGBA")
    a = im.getchannel("A")
    cov = sum(1 for v in a.getdata() if v > 8) / (im.size[0] * im.size[1])
    aspect = im.size[0] / im.size[1]
    rgb = list(im.getdata())
    solid = [(r, g, b) for (r, g, b, al) in rgb if al > 200]
    orange = sum(1 for c in solid if c[0] > 150 and 40 < c[1] < 130 and c[2] < 80)
    chroma = sum(1 for c in solid if c[1] > 170 and c[0] < 110 and c[2] < 110)
    good = abs(aspect - 0.5625) < 0.01 and cov > 0.10 and orange / len(solid) > 0.03 and chroma / len(solid) < 0.002
    (ok if good else bad)("%s: %s aspect %.4f, figure covers %.0f%%, basketball orange %.1f%%, chroma residue %.3f%%"
                          % (f, "verified" if good else "check failed", aspect, 100 * cov,
                             100 * orange / len(solid), 100 * chroma / len(solid)))
same = (media / "cut-derrick-640.webp").read_bytes() == (media / "cut-wbasketball-640.webp").read_bytes()
(bad if same else ok)("it is a different figure from the women's basketball one, not a copy")

# 5. styles and the blocked exit paths ----------------------------------------------
print("\nstyles and blocked paths")
for needle in [".card.is-pending{cursor:default}", "grayscale(1)", ".card__pend{", "rotate(-14deg)",
               ".sr__tick.is-pend", ".sr__cta[disabled]"]:
    (ok if needle in css else bad)("ring.css has %s" % needle)
if "overflow:hidden" in re.search(r"\.card\{[^}]*\}", css).group(0):
    bad(".card clips overflow, so the stamp would be cut off")
else:
    ok(".card does not clip, so the stamp runs past both edges")
guards = {
    "hero card click": r"\[data-view\]'\)\)\{const va=this\.A\[\+b\.dataset\.view\];if\(isPending\(va\)\)return",
    "ring card click": r"\[data-go\]'\)\)\{if\(isPending\(this\.A\[\(\+b\.dataset\.go\)%this\.n\]\)\)return",
    "sport button": r"_rd\.disabled=isPending\(a\)",
    "Enter key on the stage": r"e\.key==='Enter'&&e\.target===st&&!isPending",
    "hover cursor": r"\[data-view\]:not\(\.is-pending\)",
    "tab order": r"tabIndex=\(j===this\.index&&!isPending\(this\.A\[j\]\)\)\?0:-1",
}
for label, pat in guards.items():
    (ok if re.search(pat, js) else bad)("%s is blocked for pending sports" % label)
if "seen[k]" in js and "function take(a)" in js:
    ok("orderBuilt drops a second athlete of a sport it has already placed")
else:
    bad("orderBuilt has no one-per-sport rule")

# 6. cache keys ---------------------------------------------------------------------
print("\ncache keys")
for url, key in re.findall(r'(?:href|src)="([^"]+)\?v=([0-9a-f]{8})"', html):
    path = SITE / url.lstrip("/").replace("/", "\\")
    if not path.exists():
        bad("%s is referenced but %s is missing" % (url, path))
        continue
    real = hashlib.md5(path.read_bytes()).hexdigest()[:8]
    (ok if key == real else bad)("%s %s" % (url, "key matches the bytes" if key == real else "key is stale, file is %s" % real))

# 7. copy stays plain ---------------------------------------------------------------
print("\ncopy")
for phrase in ["Grey cards are sports whose playbooks are still being written.", "Playbook pending",
               "This playbook is still being written, so it is not open yet."]:
    (ok if phrase in js else bad)("says it plainly: %s" % phrase[:48])
for banned in ["coming soon", "Coming Soon", "TBD", "under construction"]:
    (bad if banned in js else ok)("no %r placeholder language" % banned)

print("\nPillow %s" % PIL.__version__)
print("%s" % ("ALL CHECKS PASSED" if not fails else "%d FAILED: %s" % (len(fails), "; ".join(fails))))
sys.exit(1 if fails else 0)
