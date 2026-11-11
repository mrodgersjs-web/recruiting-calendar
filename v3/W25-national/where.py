# -*- coding: utf-8 -*-
"""Where do the local anchors live, per source file? Scans the fragment sources (not the
assembled decks) for state names, state abbreviations, state associations, in-state program
names and regional bodies, and prints a count per file plus each hit's line number."""
import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path(r"C:\Users\Jloeh\Developer\recruiting-calendar\v3")
FILES = sorted(ROOT.glob("W19-plain/*.html")) + sorted(ROOT.glob("W20-two-sports/*.html")) + sorted(
    p for p in sorted(ROOT.glob("W24-volleyball/*.html")) if "playbook-plain" not in p.name)
PAT = re.compile(r"(wisconsin|\bWI\b|\bWIAA\b|Badger|Marquette|UW-[A-Z]|Milwaukee|Oshkosh|Eau\s*Claire"
                 r"|Whitewater|La Crosse|Stevens\s*Point|Platteville|Green Bay|Manitowoc|Appleton"
                 r"|Viterbo|Grand View|Gophers|Baird|Miller'?s Picture|Gator\s*Call|Tippe|Held"
                 r"|In-state|in-state|B1G|Badger\s*Region|WVC|CVC|NVC|Badger\s*Grounds)", re.I)

for f in FILES:
    lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
    hits = [(i + 1, ln.strip()[:150]) for i, ln in enumerate(lines) if PAT.search(ln)]
    if not hits:
        continue
    print("\n===== %s  (%d hits)" % (f.parent.name + "/" + f.name, len(hits)))
    for n, ln in hits:
        print("  L%-4d %s" % (n, ln))
