# -*- coding: utf-8 -*-
"""Which blocks get cut in half by a page break?

Parses the deck HTML for the blocks that must read as one piece (the callout
boxes, the sample email, each table, each list, the opening line of a chapter),
then checks the printed page text for each one. A block whose text is spread
over two pages reports as SPLIT.

Whitespace, letter-spacing and the soft-hyphen that Chromium leaves at a wrap
point are all normalised away, so an uppercase heading still matches its source.
"""
import re, sys, html, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SRC, DUMP = sys.argv[1], sys.argv[2]
MIN_WORDS = int(sys.argv[3]) if len(sys.argv) > 3 else 4


def norm(t):
    t = html.unescape(t)
    t = t.replace("\ufffe", "").replace("\u00ad", "").replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
    t = t.replace("-", "").replace("\u2014", "").replace("\u2013", "")
    return re.sub(r"\s+", "", t).lower()


raw = pathlib.Path(SRC).read_text(encoding="utf-8")
pages = re.split(r"===== PAGE (\d+) =====", pathlib.Path(DUMP).read_text(encoding="utf-8"))
pn = {pages[i]: norm(pages[i + 1]) for i in range(1, len(pages) - 1, 2)}


def text_of(fragment):
    return norm(re.sub(r"<[^>]+>", " ", fragment))


def blocks():
    out = []
    # callout boxes and the sample email
    for m in re.finditer(r'<div class="(?:box|tmpl)[^"]*">(.*?)</div>', raw, re.S):
        out.append(("box", m.group(1)))
    # tables, lists and the lead line of each chapter
    for m in re.finditer(r"<(table|ul|ol|p)([^>]*)>(.*?)</\1>", raw, re.S):
        tag, attrs, body = m.group(1), m.group(2), m.group(3)
        if tag == "p" and 'class="lead"' not in attrs and 'class="small"' not in attrs:
            continue
        out.append((tag, body))
    return out


splits = []
for kind, frag in blocks():
    t = text_of(frag)
    if len(re.findall(r"\w+", html.unescape(re.sub(r"<[^>]+>", " ", frag)))) < MIN_WORDS:
        continue
    found = [p for p, txt in pn.items() if t in txt]
    if found:
        continue
    # not on one page: is it on more than one?
    parts = [p for p, txt in pn.items() if t[:60] in txt]
    head = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", frag))).strip()
    splits.append((kind, head[:78], parts))

print("== %s: %d pages, %d blocks checked" % (SRC, len(pn), len(blocks())))
if not splits:
    print("no block is split across pages")
for kind, head, where in splits:
    print("SPLIT  %-6s starts on page %s | %s" % (kind, where or "?", head))
