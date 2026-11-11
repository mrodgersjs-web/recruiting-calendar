# -*- coding: utf-8 -*-
"""Print QA for the whole line at once. For each deck: a per-page text dump in the format
splitcheck2 reads, then the header / footer / page-number check, the chapter-start map and a
flag for any page that came out thin. Usage rules: no CLI args, the DECKS list is the config."""
import re, sys, pathlib, unicodedata
from pypdf import PdfReader
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TMP = pathlib.Path(r"C:\Users\Jloeh\.aside\u\1\sessions\2026-11-08_sIbJ63jY5p1sXMzN\tmp\pb25")
V3 = pathlib.Path(r"C:\Users\Jloeh\Developer\recruiting-calendar\v3")
DECKS = [
    ("mens", "Men\u2019s basketball playbook", V3 / "W19-plain/basketball-playbook-plain.html"),
    ("football", "Football playbook", V3 / "W20-two-sports/fb-playbook-plain.html"),
    ("girls", "Girls basketball playbook", V3 / "W20-two-sports/wbb-playbook-plain.html"),
    ("vb", "Volleyball playbook", V3 / "W24-volleyball/vb-playbook-plain.html"),
]
FOOT = "Education, not legal advice"
CHAP = re.compile(r"(\d{1,2})\.\s*([A-Z][A-Za-z ,:/\u2019()-]{6,60})")

for key, head, src in DECKS:
    pdf = TMP / (key + ".pdf")
    pages = [p.extract_text() or "" for p in PdfReader(str(pdf)).pages]
    n = len(pages)
    dump = "".join("===== PAGE %d =====\n%s\n" % (i + 1, t) for i, t in enumerate(pages))
    (TMP / (key + "-text.txt")).write_text(dump, encoding="utf-8")

    print("\n########## %s: %d pages (%s)" % (key, n, src.name))
    bad = []
    for i, t in enumerate(pages):
        flat = re.sub(r"\s+", "", t)              # the running head comes back letter-spaced
        if i == 0:
            continue                              # the cover carries no running header
        head_ok = re.sub(r"\s+", "", head).upper() in flat.upper()
        foot_ok = "EDUCATION,NOTLEGALADVICE" in flat.upper()
        m = re.search(r"(\d+)/(\d+)$", flat)
        if not (head_ok and foot_ok and m and int(m.group(1)) == i + 1 and int(m.group(2)) == n):
            bad.append((i + 1, head_ok, foot_ok, m.group(0) if m else None))
    print("   pages failing header/footer/number check: %s" % (bad if bad else "none"))

    starts = {}
    for i, t in enumerate(pages):
        flat = re.sub(r"\s+", " ", unicodedata.normalize("NFKC", t))
        for m in CHAP.finditer(flat):
            starts.setdefault(int(m.group(1)), i + 1)
    print("   chapter first page: " + ", ".join("ch%d p%d" % (k, v) for k, v in sorted(starts.items())))
    thin = [(i + 1, len(re.sub(r"\s+", " ", t))) for i, t in enumerate(pages)]
    print("   thinnest pages: " + ", ".join("p%d(%d ch)" % (a, b) for a, b in sorted(thin, key=lambda x: x[1])[:4]))
