"""Restore the STORY_DATA derivation my composite rewrite dropped, and fix the footer
line that still promises stories about real athletes."""
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = pathlib.Path(__file__).resolve().parents[2]
SITE = ROOT / "site"

ALIAS = (";(function(){var q=/[?&]flags=all/.test(location.search);"
         "window.STORY_DATA={athletes:STORY_ALL.athletes.filter(function(a){return q||!a.hold}),"
         "playbooks:STORY_ALL.playbooks}})();")

js = SITE / "assets" / "stories.js"
t = js.read_text(encoding="utf-8")
print("STORY_DATA present before:", "STORY_DATA" in t)
if "STORY_DATA" not in t:
    js.write_text(t.rstrip() + ALIAS, encoding="utf-8")
    print("alias restored, file bytes:", len(t.rstrip() + ALIAS))

OLD = ("Stories of real athletes are built only from public sources, linked on each page; "
       "no likeness of a real person is generated.")
NEW = ("Every story is a composite, built only from public sources, linked where the claim is made; "
       "no real athlete is named, pictured, or implied.")
n = 0
for p in SITE.rglob("*.html"):
    t0 = t = p.read_text(encoding="utf-8")
    t = t.replace(OLD, NEW)
    t = t.replace("or any athlete named on this site.", "or any athlete.")
    if t != t0:
        p.write_text(t, encoding="utf-8")
        n += 1
print("pages with the footer line updated:", n)

import hashlib  # noqa: E402
h = hashlib.md5((SITE / "assets" / "stories.js").read_bytes()).hexdigest()[:8]
print("new stories.js version:", h)
