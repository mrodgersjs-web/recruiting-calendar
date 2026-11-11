# -*- coding: utf-8 -*-
"""Does any block get cut in half by a page break?

For each block (callout box, sample email, table, list, chapter lead line) the
text is cut into runs at the tag boundaries, and a block passes only if one single
printed page holds every run. That survives the things that break naive substring
matching: a numbered list restarts its markers in the extracted text, uppercase
headings come back letter-spaced, and a hyphen at a wrap point comes back as a
soft hyphen.

Blocks marked class="flow" are allowed to run over a page boundary, but only
between rows or items, so they are reported as FLOW with the pages they span.
"""
import re, sys, html, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SRC, DUMP = sys.argv[1], sys.argv[2]
MINRUN = 22          # characters; shorter runs are list markers and labels


def norm(t):
    t = html.unescape(t)
    for junk in ("\ufffe", "\u00ad", "-", "\u2014", "\u2013"):
        t = t.replace(junk, "")
    t = t.replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
    return re.sub(r"\s+", "", t).lower()


raw = pathlib.Path(SRC).read_text(encoding="utf-8")
pages = re.split(r"===== PAGE (\d+) =====", pathlib.Path(DUMP).read_text(encoding="utf-8"))
pn = {pages[i]: norm(pages[i + 1]) for i in range(1, len(pages) - 1, 2)}

blocks = []
for m in re.finditer(r'<div class="(box[^"]*|tmpl)">\s*(.*?)</div>', raw, re.S):
    blocks.append(("box", m.group(2)))
for m in re.finditer(r"<(table|ul|ol|div|p)([^>]*)>(.*?)</\1>", raw, re.S):
    tag, attrs, inner = m.group(1), m.group(2), m.group(3)
    if tag == "p" and "lead" not in attrs:
        continue
    if tag == "div" and ("two" not in attrs or "box" in attrs):
        continue
    blocks.append((tag + (" flow" if "flow" in attrs else ""), inner))

whole = split = 0
for kind, frag in blocks:
    runs = [norm(x) for x in re.split(r"<[^>]+>", frag)]
    runs = [r for r in runs if len(r) >= MINRUN]
    if not runs:
        continue
    where = None
    for p, txt in pn.items():
        if all(r in txt for r in runs):
            where = p
            break
    if where:
        whole += 1
        continue
    split += 1
    hits = sorted({p for r in runs for p, txt in pn.items() if r in txt}, key=int)
    label = "FLOW" if kind.endswith("flow") else "SPLIT"
    print("%-6s pages %-8s (%d of %d runs found) | %s" % (
        label, ",".join(hits) if hits else "none", len(hits) and len(runs) or 0, len(runs),
        re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", frag))).strip()[:66]))

print("\n%s: %d pages, %d blocks -> %d held together, %d crossed a page break" % (SRC, len(pn), whole + split, whole, split))
