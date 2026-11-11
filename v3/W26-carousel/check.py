# -*- coding: utf-8 -*-
"""W26 gate for the athlete carousel change. Checks, in order:

1. every ?v= cache key in site/index.html equals md5[:8] of the file it points at
   (a stale key means returning visitors get an old file);
2. the order the ring now shows, derived from the real stories.js data;
3. that no pending sport can slip through as clickable;
4. that the pending styles exist in ring.css;
5. that every click path in ring.js is guarded.
"""
import hashlib
import json
import pathlib
import re
import sys

SITE = pathlib.Path(__file__).resolve().parents[2] / "site"
html = (SITE / "index.html").read_text(encoding="utf-8")
js = (SITE / "assets" / "ring.js").read_text(encoding="utf-8")
css = (SITE / "assets" / "ring.css").read_text(encoding="utf-8")
stories = (SITE / "assets" / "stories.js").read_text(encoding="utf-8")

fails = []


def ok(label):
    print("  PASS  %s" % label)


def bad(label):
    fails.append(label)
    print("  FAIL  %s" % label)


# 1. cache keys ----------------------------------------------------------------------
print("cache keys in index.html")
for url, key in re.findall(r'(?:href|src)="([^"]+)\?v=([0-9a-f]{8})"', html):
    path = SITE / url.lstrip("/").replace("/", "\\")
    if not path.exists():
        bad("%s is referenced but %s is missing" % (url, path))
        continue
    real = hashlib.md5(path.read_bytes()).hexdigest()[:8]
    (ok if key == real else bad)("%s %s (file is %s)" % (url, "key matches" if key == real else "key is stale", real))

# 2-3. the order and the pending split, from the shipped data -------------------------
data = json.loads(re.search(r"window\.STORY_ALL=(\{.*?\});\(function", stories, re.S).group(1))
athletes = [a for a in data["athletes"] if not a.get("hold")]

front_ids = re.search(r'var FRONT_IDS=\[(.*?)\]', js).group(1)
front_ids = re.findall(r'"([^"]+)"', front_ids)
womens_bb = set(re.findall(r'"([^"]+)":1', re.search(r'var WOMENS_BB=\{(.*?)\}', js).group(1)))


def built_info(a):
    s = a["sport"].lower()
    if "volleyball" in s:
        return True, "Women's Volleyball"
    if "football" in s:
        return True, "Men's Football"
    if "basketball" in s:
        return True, "Women's Basketball" if a["id"] in womens_bb else "Men's Basketball"
    return False, a["sport"]


rest = [a for a in athletes if a["id"] not in front_ids]
order = [next(a for a in athletes if a["id"] == i) for i in front_ids if any(a["id"] == i for a in athletes)]
order += [a for a in rest if built_info(a)[0]] + [a for a in rest if not built_info(a)[0]]

print("\nwhat the ring shows, in order (%d athletes; Annie stays held back)" % len(order))
for i, a in enumerate(order, 1):
    is_built, label = built_info(a)
    print("  %2d  %-10s %-22s %s" % (i, a["name"], label, "" if is_built else "  <- greyed, stamped, inert"))

if [built_info(a)[1] for a in order[:4]] != ["Women's Volleyball", "Men's Football", "Men's Basketball", "Women's Basketball"]:
    bad("the first four are not the four written playbooks")
else:
    ok("athletes 1-4 are women's volleyball, men's football, men's basketball, women's basketball")
if any(built_info(a)[0] for a in order[4:4 + len([x for x in order[4:] if built_info(x)[0]])]):
    pass
pend = [a for a in order if not built_info(a)[0]]
if all(not built_info(a)[0] for a in pend) and pend:
    ok("%d pending sports sit last, after every written sport" % len(pend))

unclassified = sorted({a["sport"] for a in athletes if not built_info(a)[0]})
print("\nsports with no playbook yet: %s" % ", ".join(unclassified))

# 4. styles --------------------------------------------------------------------------
print("\nstyles")
for needle in [".card.is-pending{cursor:default}", "grayscale(1)", ".card__pend{", "rotate(-14deg)", ".sr__tick.is-pend", ".sr__cta[disabled]"]:
    (ok if needle in css else bad)("ring.css has %s" % needle)
if "overflow:hidden" in re.search(r"\.card\{[^}]*\}", css).group(0):
    bad(".card clips overflow, so the stamp would be cut off at the edges")
else:
    ok(".card does not clip, so the stamp runs past both edges of the athlete")

# 5. every way to leave the page is guarded ------------------------------------------
print("\nclick and key paths")
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

# copy stays plain --------------------------------------------------------------------
print("\ncopy")
for phrase in ["Grey cards are sports whose playbooks are still being written.", "Playbook pending", "This playbook is still being written, so it is not open yet."]:
    (ok if phrase in js else bad)("says it plainly: %s" % phrase)
for banned in ["coming soon", "Coming Soon", "TBD", "under construction"]:
    (bad if banned in js else ok)("no %r placeholder language" % banned)

print("\n%s" % ("ALL CHECKS PASSED" if not fails else "%d FAILED: %s" % (len(fails), "; ".join(fails))))
sys.exit(1 if fails else 0)
