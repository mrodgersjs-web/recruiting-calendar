# -*- coding: utf-8 -*-
"""Final check on the four artifacts as a buyer receives them: page count, and every page where a
state, a state association or a state university still appears, so the answer to 'is this national
now?' comes from the shipped files."""
import re, sys, pathlib
from pypdf import PdfReader
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ART = pathlib.Path(r"C:\Users\Jloeh\.aside\u\1\sessions\2026-11-08_sIbJ63jY5p1sXMzN\artifacts")
PAT = re.compile(r"(wisconsin|\bwiaa\b|\bbadger\b|\buw-|oshkosh|eau claire|whitewater|la crosse|stevens point"
                 r"|viterbo|grand view|marquette|green bay|milwaukee|\bWI\b|illinois|minnesota|nebraska"
                 r"|in-state|\b,\s*WI\b)", re.I)

for f in sorted(ART.glob("*SAMPLE.pdf")):
    r = PdfReader(str(f))
    print("\n=== %s : %d pages ===" % (f.name, len(r.pages)))
    for i, p in enumerate(r.pages):
        t = re.sub(r"\s+", " ", p.extract_text() or "")
        hits = sorted({m.group(0) for m in PAT.finditer(t)})
        if hits:
            print("   p%-3d %s" % (i + 1, ", ".join(hits)))
    subj = [re.sub(r"\s+", " ", m) for p in r.pages for m in re.findall(r"Subject[^|]{0,140}", p.extract_text() or "")]
    for s in subj[:2]:
        print("   subject line as printed: %s" % s[:130])
