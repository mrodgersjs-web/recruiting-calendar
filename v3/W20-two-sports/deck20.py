#!/usr/bin/env python3
"""Build one sport playbook HTML from a content module, reusing the plain-edition head."""
import sys, io, importlib, html as H
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

def esc(s): return H.escape(str(s), quote=False)

def render(b):
    k = b[0]
    if k == "chapter":
        return '<div class="ch"><span class="ch-n">%s</span><h2>%s</h2><p class="ch-sub">%s</p></div>' % (esc(b[1]), esc(b[2]), esc(b[3]))
    if k == "h":  return "<h3>%s</h3>" % esc(b[1])
    if k == "p":  return "<p>%s</p>" % b[1]
    if k == "ul": return "<ul>" + "".join("<li>%s</li>" % x for x in b[1]) + "</ul>"
    if k == "cols":
        return '<div class="cols">' + "".join('<div class="col"><h4>%s</h4><ul>%s</ul></div>' % (esc(t), "".join("<li>%s</li>" % x for x in rows)) for t, rows in b[1]) + "</div>"
    if k == "stats":
        return '<div class="stats">' + "".join('<div class="stat"><span class="num">%s</span><span class="lab">%s</span></div>' % (esc(n), esc(l)) for n, l in b[1]) + "</div>"
    if k == "table":
        head, rows, widths = b[1], b[2], (b[3] if len(b) > 3 else None)
        th = "".join("<th>%s</th>" % esc(x) for x in head)
        cols = ('<colgroup>' + "".join('<col style="width:%s">' % w for w in widths) + '</colgroup>') if widths else ""
        body = "".join("<tr>" + "".join("<td class=\"%s\">%s</td>" % (("kind-%s" % c[1].lower()) if c[0] == "kind" else "", c[1]) for c in row) + "</tr>" for row in rows)
        return "<table>%s<thead><tr>%s</tr></thead><tbody>%s</tbody></table>" % (cols, th, body)
    if k == "checklist":
        return '<div class="cl"><div class="cl-row"><span class="box"></span><span>%s</span></div>%s</div>' % (
            esc(b[1]), "".join('<div class="cl-row"><span class="box"></span><span>%s</span></div>' % esc(x) for x in b[2]))
    if k == "callout":
        return '<div class="callout co-%s"><div class="co-title">%s</div><div class="co-body">%s</div></div>' % (b[1], esc(b[2]), b[3])
    if k == "quote":
        return '<div class="quote"><blockquote>%s</blockquote><div class="attrib">%s</div></div>' % (esc(b[1]), esc(b[2]))
    if k == "next":
        return '<div class="next"><span class="next-n">%s</span><span>%s</span></div>' % (esc(b[1]), esc(b[2]))
    if k == "page": return '<div class="page-break"></div>'
    if k == "raw":  return b[1]
    raise ValueError("bad block " + k)

def build(module, title_line, edition, out):
    m = importlib.import_module(module)
    head = open("head.txt", encoding="utf-8").read()
    head = head.replace("Basketball: The Whole Pathway", title_line).replace("Men's basketball playbook", edition).replace("Men's basketball playbook.", edition)
    cover = open("cover.txt", encoding="utf-8").read().replace("@@EDITION@@", edition).replace("@@SUB@@", m.SUB).replace("@@KICK@@", m.KICK).replace("@@N@@", str(m.NPAGES))
    toc = '<div class="page-break"></div><div class="toc"><h2>What is in this book</h2><ul>' + "".join(
        '<li><span class="toc-n">%s</span><span class="t">%s</span><span class="p">p %s</span></li>' % (n, t, p) for n, t, p in m.TOC) + "</ul></div>"
    body = "".join(render(b) for b in m.PARTS)
    src = '<div class="page-break"></div><h3>Sources for every rule in this book</h3>' + m.SOURCES + \
          '<p style="font-size:7pt;line-height:1.35;margin-top:6pt;color:var(--ink-2)">Every rule, limit and date was checked against the documents named above on 11 November 2026. Where two official sources disagree, both figures are printed. Rules change: the NCAA moves its sport-by-sport calendars outside the bylaws, so confirm against the current calendar before you act on a date. This is education, not legal advice, and no outcome is promised.</p>'
    open(out, "w", encoding="utf-8").write(head + "<body>" + cover + toc + body + src + "</body></html>")
    print("wrote", out, "%.1f KB" % (len(head + body) / 1024.0))

if __name__ == "__main__":
    import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
