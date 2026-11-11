# -*- coding: utf-8 -*-
"""W21: stop blocks being cut in half by a page break.

Mike's read of the football PDF: the "how long should his list be?" callout and the
sample email were each split over two pages, and chapter 3 started mid-page. So:
every callout, sample email, table, list, chapter heading and chapter opening line
now has to move whole to the next page if it does not fit, and the four blocks that
genuinely run longer than one page are marked class="flow" so they may break between
rows, with the header row repeated. Chapter 3 also gets its own page.
"""
import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

CSS = """
/* W21: nothing reads as half a thought. Blocks move whole; only .flow may split. */
.box, .tmpl, table, ul, ol, dl, blockquote, .two, h2, h3, .pagehead, .split {
  break-inside: avoid; page-break-inside: avoid }
table.flow, ul.flow, ol.flow, div.flow, dl.flow {
  break-inside: auto; page-break-inside: auto }
tr, li { break-inside: avoid; page-break-inside: avoid }
thead { break-after: avoid }
h2, h3 { break-after: avoid; page-break-after: avoid }
p { orphans: 2; widows: 2 }
"""

h = pathlib.Path("head.txt"); s = h.read_text(encoding="utf-8")
if "W21: nothing reads as half a thought" not in s:
    s = s.replace("</style>", CSS + "</style>")
    h.write_text(s, encoding="utf-8")
    print("head.txt: block rules added")
else:
    print("head.txt: already patched")


def add_class(src, anchor, tag, cls):
    """Give the nearest opening <tag> before `anchor` a class."""
    i = src.find(anchor)
    if i < 0:
        print("  MISSING anchor:", anchor[:48]); return src, False
    j = src.rfind("<" + tag, 0, i)
    if j < 0:
        print("  no tag before anchor:", anchor[:48]); return src, False
    end = src.index(">", j)
    opentag = src[j:end]
    if 'class="' in opentag:
        new = opentag.replace('class="', 'class="' + cls + " ", 1)
    else:
        new = opentag + ' class="' + cls + '"'
    return src[:j] + new + src[end:], True


def newpage(src, anchor):
    i = src.find(anchor)
    if i < 0:
        print("  MISSING chapter anchor:", anchor[:48]); return src, False
    j = src.rfind("<section>", 0, i)
    if j < 0:
        print("  no section before anchor:", anchor[:48]); return src, False
    return src[:j] + '<section class="newpage">' + src[j + len("<section>"):], True


FLOW = ["<th>What to do that month", "<th>Buy it or skip it", '<div class="two small">']
OL_FLOW = {"fb-plain.py": "They think 85 is the number that matters.",
           "wbb-plain.py": 'They read "15 scholarships" and stop.'}
CH3 = "3. The plan by date"

for fn in ("fb-plain.py", "wbb-plain.py"):
    p = pathlib.Path(fn); t = p.read_text(encoding="utf-8"); done = 0
    for anchor in FLOW:
        tag = "div" if anchor.startswith("<div") else "table"
        t, ok = add_class(t, anchor, tag, "flow"); done += ok
    t, ok = add_class(t, OL_FLOW[fn], "ol", "flow"); done += ok
    t, ok = newpage(t, CH3); done += ok
    p.write_text(t, encoding="utf-8")
    print("%s: %d of 5 marks applied" % (fn, done))
