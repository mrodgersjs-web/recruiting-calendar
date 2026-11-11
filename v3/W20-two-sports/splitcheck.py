# -*- coding: utf-8 -*-
"""Which blocks get cut in half by a page break?

Parses the deck HTML for the blocks that should read as one piece (callout boxes,
the sample email, tables, lists, the lead line of a chapter), then looks for each
one inside the printed page text. A block found whole on a single page passes. A
block marked class="flow" may be split, but only between rows or items, so it
reports as FLOW rather than as a defect.

Whitespace, CSS letter-spacing and the soft-hyphen Chromium leaves at a wrap point
are normalised away, so an uppercase heading still matches its source text.
"""
import re, sys, html, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SRC, DUMP = sys.argv[1], sys.argv[2]


def norm(t):
    t = html.unescape(t)
    for junk in ("\ufffe", "\u00ad", "-", "\u2014", "\u2013"):
        t = t.replace(junk, "")
    t = t.replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
    return re.sub(r"\s+", "", t).lower()


raw = pathlib.Path(SRC).read_text(encoding="utf-8")
pages = re.split(r"===== PAGE (\d+) =====", pathlib.Path(DUMP).read_text(encoding="utf-8"))
pn = {pages[i]: norm(pages[i + 1]) for i in range(1, len(pages) - 1, 2)}


def body(frag):
    return re.sub(r"<[^>]+>", " ", frag)


blocks = []
for m in re.finditer(r'<div class="(box[^"]*|tmpl)">\s*(.*?)</div>', raw, re.S):
    blocks.append(("box " + m.group(1), m.group(2)))
for m in re.finditer(r"<(table|ul|ol|div|p)([^>]*)>(.*?)</\1>", raw, re.S):
    tag, attrs, inner = m.group(1), m.group(2), m.group(3)
    if tag == "p" and "lead" not in attrs:
        continue
    if tag == "div" and "two" not in attrs:
        continue
    if tag == "div" and "box" in attrs:
        continue
    blocks.append((tag + (" flow" if "flow" in attrs else ""), inner))

bad = ok = flow = 0
for kind, frag in blocks:
    t = norm(body(frag))
    if len(re.findall(r"\w+", body(frag))) < 4:
        continue
    whole = [p for p, txt in pn.items() if t in txt]
    if whole:
        ok += 1
        continue
    bad += 1
    starts = [p for p, txt in pn.items() if t[:70] in txt]
    print("%-9s page %-6s | %s" % ("SPLIT" if "flow" not in kind else "FLOW?", starts or "?",
                                   re.sub(r"\s+", " ", html.unescape(body(frag))).strip()[:74]))

print("\n%s: %d pages, %d blocks: %d whole on one page, %d split" % (SRC, len(pn), len(blocks), ok, bad))
