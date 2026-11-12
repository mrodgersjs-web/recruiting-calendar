# -*- coding: utf-8 -*-
"""W28 print round five, written against the print auditor's re-verdict. Prints what it changed.

Every edit below answers a measurement, not a preference:
  1. the furniture prints near-black, bold and over-tracked where the shelf book prints mid-grey
     at a normal weight, about half a point smaller;
  2. the calendar columns do not land where the shelf book's land. The template rules I wrote
     govern a class no book uses: the widths live in each table's own <th style>, and most header
     cells carry no width at all, so the first column is whatever its content makes it;
  3. a softball table parted from its lead-in;
  4. a back page parted from its own heading;
  5. the in-progress band inherits the cover's greyscale, so the one thing on the tile that says
     "in progress" is grey;
  6. the phone deck prints a heading over a list that holds only the $9 checker;
  7. prices that break across three lines on a phone, and a lane folder holding five books while
     the record claimed nine pairs were compared.
"""
import re, pathlib, sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LANE = pathlib.Path(__file__).parent
SITE = LANE.parents[1] / "site"
F = LANE / "fragments"
NEW = ("mens-baseball-road-to-college", "womens-softball-road-to-college",
       "mens-soccer-road-to-college", "womens-soccer-road-to-college")
log = []

# 1 ------------------------------------------------------------------ furniture, like the shelf
pj = (LANE / "print.js").read_text(encoding="utf-8")
old = 'const HFONT = "font-family:Arial,Helvetica,sans-serif;font-size:8px;font-weight:600;color:#141414";'
assert pj.count(old) == 1, "the furniture font is not where the last commit left it"
pj = pj.replace(old, 'const HFONT = "font-family:Arial,Helvetica,sans-serif;font-size:9px;font-weight:400;color:#5a5a5a";', 1)
pj = pj.replace(";letter-spacing:.25em;text-transform:uppercase",
                ";letter-spacing:.2em;text-transform:uppercase", 1)
(LANE / "print.js").write_text(pj, encoding="utf-8")
log.append("print.js: head and footer print 9 px, normal weight, mid-grey, tracked as the shelf book is")

# 2 ------------------------------------------------- the calendar, on the shelf book's own numbers
# The shelf book's calendar sets its header cells to 20% and 38%. A table whose first header cell
# says When is a calendar in any book, so it gets those numbers on every cell. A header cell with
# no width is the bug, not a detail: the column then takes whatever width its content wants, which
# is why one book's three calendars disagreed with each other.
def setw(cells, want):
    out = []
    for i, (attrs, inner) in enumerate(cells):
        w = want[i] if i < len(want) else None
        a = re.sub(r'\s*style="[^"]*"', "", attrs)
        if w:
            a = ' style="width:%s"' % w + a
        out.append("<th%s>%s</th>" % (a, inner))
    return "".join(out)


def fix_table(path):
    t = path.read_text(encoding="utf-8")
    n = [0]

    def go(m):
        head = m.group(0)
        cells = re.findall(r"<th([^>]*)>(.*?)</th>", head, re.S)
        if not cells or re.sub(r"<[^>]+>", "", cells[0][1]).strip().lower() != "when":
            return head
        want = {2: ["20%", "80%"], 3: ["20%", "38%", "42%"], 4: ["20%", "38%", "22%", "20%"]}.get(len(cells))
        if not want:
            return head
        new = setw(cells, want)
        if new != re.sub(r"(<th[^>]*>.*?</th>)", r"\1", head, flags=re.S):
            n[0] += 1
        return "<thead><tr>%s</tr></thead>" % new if "<tr>" not in head else head.replace(
            re.search(r"<tr>.*?</tr>", head, re.S).group(0), "<tr>%s</tr>" % new, 1)

    t2 = re.sub(r"<thead>.*?</thead>", go, t, flags=re.S)
    if t2 != t:
        path.write_text(t2, encoding="utf-8")
    return n[0]


cal = sum(fix_table(f) for slug in NEW for f in sorted((F / slug).glob("c*.html")))
log.append("fragments: %d calendar tables now carry the shelf book's widths on every header cell" % cal)

# 3 -------------------------------------------------------------- softball, kept with its own lead
sb = F / "womens-softball-road-to-college" / "c08-ch07.html"
s = sb.read_text(encoding="utf-8")
i = s.find("<h3>The NAIA: grades can make room for her</h3>")
assert i > 0, "the NAIA heading is not where the auditor left it"
m = re.search(r"<p>(?!</p>)", s[i:])
assert m, "no lead-in paragraph after the NAIA heading"
at = i + m.start()
sb.write_text(s[:at] + '<p class="keepnext">' + s[at + 3:], encoding="utf-8")
log.append("softball: the NAIA lead-in carries .keepnext, so it cannot leave its table behind")

# 4 ------------------------------------------------------- the back page, whole, in every new book
ht = (LANE / "head.txt").read_text(encoding="utf-8")
if ".keep {" not in ht:
    ht += ("\n/* The back page is short on purpose, but it must not be split from its own heading.\n"
           "   A rule with nothing under it is the last thing a reader sees. Tag it .keep. */\n"
           ".keep { break-inside: avoid; page-break-inside: avoid }\n")
    (LANE / "head.txt").write_text(ht, encoding="utf-8")
tagged = []
for slug in NEW:
    files = sorted((F / slug).glob("c*.html"))
    last = files[-1]
    t = last.read_text(encoding="utf-8")
    t2 = t.replace('<section class="newpage">', '<section class="newpage keep">', 1)
    if t2 != t:
        last.write_text(t2, encoding="utf-8")
        tagged.append(slug[4:].replace("-road-to-college", ""))
log.append("head.txt defines .keep; the back section carries it in: " + ", ".join(tagged))

# 5 ------------------------------------------------------ the band stays the colour of the finding
css = (SITE / "assets" / "commit.css").read_text(encoding="utf-8")
old = ".pb-cell.is-pend .pb-thumb{filter:grayscale(1);opacity:.55}"
assert css.count(old) == 1, "the greyscale rule is not where the last commit left it"
css = css.replace(old, ".pb-cell.is-pend .pb-thumb{background-image:linear-gradient(rgba(203,197,184,.62),rgba(203,197,184,.62))}\n"
                       ".pb-cell.is-pend .pb-thumb>b,.pb-cell.is-pend .pb-thumb>i{filter:grayscale(1);opacity:.55}\n"
                       ".pb-cell.is-pend .pb-pend{z-index:2}", 1)
(SITE / "assets" / "commit.css").write_text(css, encoding="utf-8")
log.append("commit.css: the cover is muted by a wash on its own background, so the band keeps its red")

# 6 ----------------------------------------------------- a heading that has to mean what it says
dj = (SITE / "assets" / "deck.js").read_text(encoding="utf-8")
assert dj.count("(pbs?'<p class=\"dk-pbl\">Playbooks for this sport</p>':'')") == 1, "the deck heading moved"
dj = dj.replace("(pbs?'<p class=\"dk-pbl\">Playbooks for this sport</p>':'')",
                "(HASBOOK?'<p class=\"dk-pbl\">Playbooks for this sport</p>':'')", 1)
old = "    var P=D.playbooks;\n"
assert dj.count(old) == 1
dj = dj.replace(old, old + "    // A list holding only the $9 checker is not a shelf of playbooks, and the heading over\n"
                           "    // it is the kind of thing a reader photographs to ask what is for sale.\n"
                           "    function hasBook(a){return (a.playbooks||[]).some(function(id){var p=P[id];\n"
                           "      return p&&p.status==='WRITTEN'&&!/Eligibility/i.test(String(p.title))})}\n", 1)
dj = dj.replace("      var pbs=(a.playbooks||[])", "      var HASBOOK=hasBook(a);\n      var pbs=(a.playbooks||[])", 1)
(SITE / "assets" / "deck.js").write_text(dj, encoding="utf-8")
log.append("deck.js: the strip prints only when a written playbook is in the list, not for the checker alone")

# 7 ------------------------------------------------------ prices that do not break in a hand
sp = LANE / "site.py"
t = sp.read_text(encoding="utf-8")
start = t.index("    # Two of the three bundle rows")
end = t.index("    for page2 in [SITE / 'sports' / 'index.html'")
NEW7 = """    # The words 'at launch' glued to a price break into three lines on a phone and strand the
    # dot. The rows carry them in a note instead, where the membership row already said it, and
    # the line under the list says it once for all three.
    hb = shelf.read_text(encoding='utf-8')
    hb = re.sub(r'(<span>\\$[0-9]+(?:/yr)?) &middot; at launch(</span>)', r'\\1\\2', hb)
    for row, say in (
        ('Sport Pack', 'A sport playbook and the two tools, once the tools exist.'),
        ('Every Playbook', 'All nine playbooks, and each new one as it is written.'),
        ('Sideline membership', 'The calendar tool, once it exists. Not open at launch.'),
    ):
        hb = re.sub(r'(<b>' + re.escape(row) + r'[^<]*</b>\\s*<span>[^<]*</span>)(?!\\s*<p class="note">)',
                    r'\\1 <p class="note">' + say + '</p>', hb, count=1)
    if hb != shelf.read_text(encoding='utf-8'):
        shelf.write_text(hb, encoding='utf-8')
        print('    the bundle rows carry the words in a note, not on the price')
"""
sp.write_text(t[:start] + NEW7 + t[end:], encoding="utf-8")
log.append("site.py: the suffix comes off the prices, and each of the three rows gets a note")

# 8 ------------------------------------------------- a grid gate that measures like the auditor
# text_items() answers where and how big, not what: the glyphs in a printed book are IDs in a
# subsetted font. So the calendar is measured the only way it can be: group the runs on a page
# into lines, keep the lines with exactly as many runs as the table has columns and a run at the
# margin, and take the mode across the book. The same recipe runs on the shelf book at run time,
# so the target comes off the paper rather than out of the head of whoever wrote the check.
pc = (LANE / "printcheck.py").read_text(encoding="utf-8")
g0, g1 = pc.index("    # 2c"), pc.index("    # 3 one chapter per fresh page")
NEW8 = '''    # 2c The calendar grid, measured off the paper. A run carries position and size but no
    # text, because the glyphs in a printed book are IDs in a subsetted font, so the calendar is
    # found by shape: lines with exactly as many runs as the table has columns, one of them at the
    # left margin. The target is the shelf book, measured by this same recipe when the check runs,
    # not a number typed into a comment by the person who wrote it.
    MARGIN_L = 14 / 25.4 * 72

    def grid_lines(reader):
        """Every line that looks like a row of the calendar: (left edges) and how often it recurs."""
        from collections import Counter
        tally = Counter()
        for i in range(len(reader.pages)):
            items = [x for x in text_items(reader, i)
                     if str(x.get("t", "")).strip() != "x" and MARGIN_L - 3 < x["x"] < LETTER[0] - MARGIN_L]
            rows = {}
            for x in items:
                k = round(x["y"] / 2.0)
                rows.setdefault(k, []).append(round(x["x"], 1))
            for k in rows:
                xs = sorted(set(rows[k]))
                if 2 <= len(xs) <= 4 and abs(xs[0] - MARGIN_L) <= 3.0:
                    tally[tuple(xs)] += 1
        return tally

    ref = pathlib.Path(__file__).parent / "pdfs" / "volleyball-road-to-college.pdf"
    if ref.exists():
        rr = grid_lines(PdfReader(str(ref)))
        wide = [(k, v) for k, v in rr.items() if len(k) >= 3]
        if not wide:
            fails.append("the shelf book gives no calendar grid to measure against")
        else:
            tgt = max(wide, key=lambda kv: kv[1])[0]
            mine = grid_lines(r)
            got = [(k, v) for k, v in mine.items() if len(k) >= 3 and k[0] <= MARGIN_L + 3]
            if not got:
                fails.append("no calendar row was found to measure")
            else:
                best = max(got, key=lambda kv: kv[1])[0]
                for j, nm in ((1, "second"), (2, "third")):
                    if j >= len(tgt) or j >= len(best):
                        continue
                    if abs(best[j] - tgt[j]) > 4.5:
                        fails.append("the calendar's %s column prints %.2fin from where the shelf book prints it"
                                     % (nm, (best[j] - tgt[j]) / 72))

'''
pc = pc[:g0] + NEW8 + pc[g1:]
if "from collections import" in pc and "\nimport collections" not in pc:
    pass
if re.search(r"^import .*pathlib", pc, re.M) is None:
    pc = pc.replace("import ", "import pathlib, ", 1)
(LANE / "printcheck.py").write_text(pc, encoding="utf-8")
log.append("printcheck.py: the grid gate takes its target from the shelf book at run time")

for L in log:
    print("  " + L)
