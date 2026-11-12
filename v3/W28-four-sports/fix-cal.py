# -*- coding: utf-8 -*-
"""W28: the calendar columns get the shelf book's widths, cell by cell, verified before writing.

The first attempt used a % format string and ate a header row. The second used a greedy <tr>.*</tr>
and collapsed two header rows into one, which the assertion below caught before anything was
written. A pass over the files that hold a customer's book has to check its own output.
"""
import re, pathlib, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
F = pathlib.Path(__file__).parent / "fragments"
NEW = ("mens-baseball-road-to-college", "womens-softball-road-to-college",
       "mens-soccer-road-to-college", "womens-soccer-road-to-college")
WANT = {2: ["20%", "80%"], 3: ["20%", "38%", "42%"], 4: ["20%", "38%", "22%", "20%"]}


def rows_of(head):
    return re.findall(r"<tr[^>]*>.*?</tr>", head, re.S)


def rebuild_row(row, want):
    cells = re.findall(r"<th([^>]*)>(.*?)</th>", row, re.S)
    if len(cells) != len(want):
        return None
    pieces = []
    for i, (attrs, inner) in enumerate(cells):
        rest = re.sub(r'\s*style="[^"]*"', "", attrs)
        pieces.append('<th style="width:' + want[i] + '"' + rest + '>' + inner + "</th>")
    return "<tr>" + "".join(pieces) + "</tr>"


done = 0
for slug in NEW:
    for f in sorted((F / slug).glob("c*.html")):
        t = f.read_text(encoding="utf-8")
        edits = []
        for m in re.finditer(r"<thead>.*?</thead>", t, re.S):
            head = m.group(0)
            first = re.findall(r"<th[^>]*>(.*?)</th>", head, re.S)
            if not first or re.sub(r"<[^>]+>", "", first[0]).strip().lower() != "when":
                continue
            nrows = rows_of(head)
            want = WANT.get(len(re.findall(r"<th[^>]*>", nrows[0], re.S)))
            if not want or any(len(re.findall(r"<th[^>]*>", r0, re.S)) != len(want) for r0 in nrows):
                print("   left alone (not a plain calendar):", f.name)
                continue
            new = head
            for r0 in nrows:
                built = rebuild_row(r0, want)
                assert built is not None
                got = re.findall(r"<th([^>]*)>", built, re.S)
                assert len(got) == len(want), "cell count moved in " + f.name
                for i, a in enumerate(got):
                    assert ("width:" + want[i]) in a, "cell %d lost its width in %s: %r" % (i, f.name, a)
                new = new.replace(r0, built, 1)
            edits.append((m.start(), m.end(), new))
        for s0, s1, new in reversed(edits):
            t = t[:s0] + new + t[s1:]
        if edits:
            f.write_text(t, encoding="utf-8")
            done += len(edits)
print("calendar headers carry the shelf book's widths in %d tables" % done)

# The two keeps the auditor asked for. The back page of a book is short on purpose; what it must
# not be is separated from the heading and rule that introduce it.
sb = F / "womens-softball-road-to-college" / "c08-ch07.html"
s = sb.read_text(encoding="utf-8")
i = s.find("<h3>The NAIA: grades can make room for her</h3>")
assert i > 0, "the NAIA heading is not where the auditor left it"
at = s.index("<p>", i)
sb.write_text(s[:at] + '<p class="keepnext">' + s[at + 3:], encoding="utf-8")
for slug in NEW:
    last = sorted((F / slug).glob("c*.html"))[-1]
    t = last.read_text(encoding="utf-8")
    t2 = t.replace('<section class="newpage">', '<section class="newpage keep">', 1)
    assert t2 != t, "no plain back section in " + last.name
    last.write_text(t2, encoding="utf-8")
print("softball lead-in tagged, and the back section of all four carries .keep")
