#!/usr/bin/env python3
"""
W14d: with the bios gone, a first name on any page is a loose end.

Three shapes to clear, each with a rule that reports how many sites it changed:
  1. "Stories that use it" chips on playbook pages:  Hunter . Football . D1
  2. Composite basis lines:                          (Derrick, a D2 school) source
  3. The emerging-sports page, which sold two of these paths by name.
"""
import html
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = pathlib.Path(__file__).resolve().parents[2]
SITE = ROOT / "site"

ROLE = {
    "Hunter": "the walk-on who never started", "Sara": "the two-sport kid who picked one",
    "Karsta": "the setter who transferred", "Olivia": "the walk-on pitcher",
    "Derrick": "the D2 starter who moved to D1", "Samantha": "the guard who redshirted",
    "Ali": "the lineman who picked his school", "Annie": "the distance runner who improved late",
    "Tori": "the goalie who started late", "Cedric": "the D3 star who moved up",
    "Cristelle": "the wrestle-over", "Jimmy": "the JUCO guard",
    "Chris": "the club player who walked on",
}
NAMES = "|".join(sorted(ROLE, key=len, reverse=True))

rules = [
    # 1. chips on playbook pages
    (rf"({NAMES})(?= &middot; |\s+·\s)", lambda m: ROLE[m.group(1)] + " (composite)"),
    # 2. basis parentheticals on composite pages: keep the claim, drop the person
    (rf"\s*\((?:Sam\s+)?(?:{NAMES})(?:,[^)]*)?\)\s*(?=source|<)", " "),
    # 3. named-subject phrasing
    ("what Derrick's family did in basketball", "what a basketball family in the same spot did"),
    ("A family sent a highlight video", "A family sent a highlight video"),
    # 4. the two paths emerging-sports sold by name
    ("Read Cristelle's path to NAIA Doane", "Read a composite NAIA wrestling path"),
    ("Read Tori's path", "Read a composite lacrosse path"),
    (rf"(?:{NAMES}): lacrosse goalie, started in 8th grade, D3",
     "The goalie who started late (composite): lacrosse goalie, started in 8th grade, D3"),
    (rf"(?:{NAMES}): NAIA women's wrestling at Doane",
     "The wrestle-over (composite): NAIA women's wrestling at Doane"),
    (rf"(?:{NAMES}): stepped away, came back, D3 wrestling",
     "The wrestler who stepped away (composite): stepped away, came back, D3 wrestling"),
    # the site no longer has real athletes on it, so the label has to change too
    ("Real athlete.", "Composite, built from sourced paths."),
]

tally = {}
for f in sorted(list(SITE.rglob("*.html")) + [SITE / "assets" / "stories.js"]):
    t0 = t = f.read_text(encoding="utf-8", errors="ignore")
    for pat, rep in rules:
        t, n = re.subn(pat, rep, t)
        if n:
            tally[pat[:46]] = tally.get(pat[:46], 0) + n
    # dead bio links on the pages that referenced them
    t = t.replace('href="/story/cristelle"', 'href="/sports/wrestling"')
    t = t.replace('href="/story/tori"', 'href="/sports/lacrosse"')
    t = t.replace('href="/athlete/cristelle"', 'href="/sports/wrestling"')
    t = t.replace('href="/athlete/tori"', 'href="/sports/lacrosse"')
    if t != t0:
        f.write_text(t, encoding="utf-8")

print("rule results:")
for pat, n in tally.items():
    print(f"   {n:3}  {pat}")

left = []
for p in sorted(SITE.rglob("*.html")):
    body = html.unescape(re.sub(r"<[^>]+>", " ", re.sub(
        r"<(script|style)[^>]*>.*?</\1>", " ", p.read_text(encoding="utf-8", errors="ignore"), flags=re.S | re.I)))
    for n in ROLE:
        for m in re.finditer(r"\b" + n + r"\b", body):
            left.append((str(p.relative_to(SITE)), n, re.sub(r"\s+", " ", body[max(0, m.start()-70):m.start()+90])))
print(f"\nreal first names still visible: {len(left)}")
for page, n, ctx in left[:12]:
    print(f"   {page}\n      [{n}] …{ctx.strip()}…")
