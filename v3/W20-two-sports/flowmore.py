import pathlib, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def add_class(t, anchor):
    i = t.find(anchor)
    if i < 0:
        print("  MISSING", anchor); return t, False
    j = t.rfind("<table", 0, i)
    e = t.index(">", j)
    op = t[j:e]
    new = op.replace('class="', 'class="flow ') if 'class="' in op else op + ' class="flow"'
    return t[:j] + new + t[e:], True

PLAN = {
    "fb-plain.py": ["<th>So what should you pay for", "<th>When it may be signed"],
    "wbb-plain.py": ["<th>When it may be signed"],
}
for fn, anchors in PLAN.items():
    p = pathlib.Path(fn); t = p.read_text(encoding="utf-8"); n = 0
    for a in anchors:
        t, ok = add_class(t, a); n += ok
    # the summary box reads better before the price grid than alone on a page
    i = t.find("<h3>The whole-year number</h3>")
    if i > 0:
        s = t.rfind('<div class="box', 0, i); e = t.index("</div>", i) + 6
        block = t[s:e].strip(); t = t[:s] + t[e:]
        k = t.rfind("<table", 0, t.find("<th>What you buy"))
        t = t[:k] + block + "\n" + t[k:]
        print(fn, "boxes to flow:", n, "| whole-year box moved before the price grid")
    else:
        print(fn, "boxes to flow:", n, "| no whole-year box")
    p.write_text(t, encoding="utf-8")
