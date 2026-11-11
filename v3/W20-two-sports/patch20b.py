# -*- coding: utf-8 -*-
"""W20 batch two: the football calendar year, and the two chapter headings that
blamed the player for things the family does."""
import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

FB = [
    ("The football recruiting calendar for 2028-29 does not exist yet: the committees ratify it and the NCAA publishes it in July 2027.",
     "The football recruiting calendar for 2028-29 does not exist yet. The committees ratify it and the NCAA publishes it in July 2028."),
    ("<h3>What he must not do</h3>", "<h3>What your family must not do</h3>"),
]
WBB = [
    ("<h3>What she must not do</h3>", "<h3>What your family must not do</h3>"),
]

SRC = ("<src>NCAA recruiting fact sheets, 2026-27 edition, for the athletics-aid rates printed in Chapter 2 "
       "(70% of Division 1 athletes and 77% of Division 2 athletes receive athletics aid; in Division 3 there "
       "is no athletics aid and 80% of athletes receive nonathletics aid). ncaa.org</src>")

def run(fn, pairs):
    p = pathlib.Path(fn); s = p.read_text(encoding="utf-8"); bad = 0
    for old, new in pairs:
        pat = re.compile(r"\s+".join(re.escape(t) for t in re.split(r"\s+", old.strip())))
        hits = list(pat.finditer(s))
        if len(hits) != 1:
            print("PROBLEM %d matches: %r" % (len(hits), old[:80])); bad += 1; continue
        m = hits[0]; s = s[:m.start()] + new + s[m.end():]
        print("ok  %r" % old[:70])
    p.write_text(s, encoding="utf-8")
    print("%s: %d patched, %d problems" % (fn, len(pairs) - bad, bad))

run("fb-plain.py", FB)
run("wbb-plain.py", WBB)

for name in ("wbb-sources.html", "fb-sources.html"):
    p = pathlib.Path(name); s = p.read_text(encoding="utf-8")
    if "recruiting fact sheet" in s.lower():
        print(name, "already cites the fact sheet"); continue
    anchor = "NCAA Research, estimated probability"
    if anchor not in s:
        print(name, "MISSING ANCHOR"); continue
    s = s.replace(anchor, SRC + "\n    <src>" + anchor, 1)
    p.write_text(s, encoding="utf-8")
    print(name, "added the fact-sheet source line")
