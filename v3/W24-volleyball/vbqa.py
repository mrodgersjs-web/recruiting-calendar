# -*- coding: utf-8 -*-
"""Print QA for the volleyball deck: per-page text dump, header and footer check,
page-number check, and a one-line peek at every page."""
import re, sys, pathlib
from pypdf import PdfReader
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LANE = pathlib.Path(__file__).parent
PDF = pathlib.Path(r"C:\Users\Jloeh\.aside\u\1\sessions\2026-11-08_sIbJ63jY5p1sXMzN\tmp\pb24\vb.pdf")
DUMP = LANE / "vb-text.txt"

r = PdfReader(str(PDF))
lines = []
with open(DUMP, "w", encoding="utf-8") as f:
    for i, p in enumerate(r.pages):
        f.write("\n===== PAGE %d =====\n" % (i + 1))
        try:
            f.write(p.extract_text() or "")
        except Exception as e:
            f.write("<<err %s>>" % e)
print("=== vb.pdf: %d pages ===" % len(r.pages))

raw = DUMP.read_text(encoding="utf-8")
parts = re.split(r"===== PAGE (\d+) =====", raw)
tot = (len(parts) - 1) // 2
fail = []
for i in range(1, len(parts) - 1, 2):
    n = parts[i]; t = parts[i + 1]
    flat = re.sub(r"\s+", "", t)
    head = "VOLLEYBALLPLAYBOOK" in flat.upper()
    foot = "EDUCATION,NOTLEGALADVICE" in flat.upper()
    m = re.search(r"(\d+)/(\d+)$", flat)
    ok = head and foot and m and m.group(1) == n and int(m.group(2)) == tot
    if not ok:
        fail.append((n, head, foot, m.group(0) if m else None))
    body = re.sub(r"\s+", " ", t.strip())
    lines.append("p%-3s %5d ch  head %s foot %s pg %-8s | %s" % (
        n, len(re.sub(r"\s+", "", t)), "Y" if head else "n", "Y" if foot else "n",
        m.group(0) if m else "-", body[:96]))
print("\n".join(lines))
print("\npages failing header/footer/number check:", fail if fail else "none")

# where do chapters start, and does any heading sit stranded at a page bottom?
for i in range(1, len(parts) - 1, 2):
    n = parts[i]; t = re.sub(r"\s+", " ", parts[i + 1])
    for h in re.findall(r"\b(\d{1,2})\.\s+[A-Z][^.]{6,60}", t):
        pass
    heads = re.findall(r"\b((?:1[01]|[1-9])\.\s[^|]{6,62}?)(?:\s[A-Z0-9]|$)", t)
    if heads:
        print("p%-3s headings: %s" % (n, " || ".join(x.strip()[:58] for x in heads[:3])))
