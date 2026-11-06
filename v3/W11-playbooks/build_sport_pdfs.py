#!/usr/bin/env python3
"""Build site/downloads/{football,baseball,track}-class-2029.pdf.
Content = (1) W10 PLAYBOOK.md header + Part A (verified bylaw table, academic lines, roster reality)
          (2) the sport's sourced calendar rows from funnel/lead-magnet/out/<sport>-class-2029.html (built from site/data.js)
          (3) Stage titles with their Done-when lines, and the Sources-used list.
Rendered via headless Chrome. Read-only on W10; writes only site/downloads/ and v3/W11-playbooks/build/."""
import re, os, html, subprocess, sys
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT = f"{R}/site/downloads"; BUILD = f"{R}/v3/W11-playbooks/build"
os.makedirs(OUT, exist_ok=True); os.makedirs(BUILD, exist_ok=True)
esc = html.escape
def inline(s):
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    return s
def md_to_html(block):
    out, lines, i = [], block.split("\n"), 0
    while i < len(lines):
        l = lines[i]
        if l.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                if not re.match(r"^\|[-| ]+\|$", lines[i]): rows.append([c.strip() for c in lines[i].strip("|").split("|")])
                i += 1
            t = "<table class=t><tr>" + "".join(f"<th>{inline(c)}</th>" for c in rows[0]) + "</tr>"
            for r in rows[1:]: t += "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>"
            out.append(t + "</table>"); continue
        if l.startswith("> "): out.append(f"<blockquote>{inline(l[2:])}</blockquote>")
        elif l.strip() and l.strip() != "---": out.append(f"<p>{inline(l)}</p>")
        i += 1
    return "\n".join(out)
CSS = """body{font:10.5pt/1.4 Georgia,serif;color:#111;margin:0}section{padding:26px 34px}h1{font-size:20pt;margin:0 0 4px}h2{font-size:14pt;margin:18px 0 6px;border-bottom:2px solid #222}
.sub{color:#444;font-size:9.5pt;margin-bottom:8px}blockquote{border-left:3px solid #999;margin:8px 0;padding:2px 10px;font-size:9.5pt;color:#333;background:#f6f6f6}
table.t{border-collapse:collapse;width:100%;font-size:9.5pt;margin:6px 0}table.t td,table.t th{border:1px solid #ccc;padding:4px 6px;text-align:left;vertical-align:top}table.t th{background:#eee}
code{font-size:9pt}.stage{margin:5px 0;font-size:10pt}.pb{page-break-before:always}.foot{font-size:8pt;color:#666;margin-top:14px}
td.dt{white-space:nowrap;font-family:monospace}.pe{margin-top:3px}.miss{font-size:9pt;color:#7a2a00}.src{font-size:8pt;color:#555;word-break:break-all}
tr.hard td{background:#fff3ef}tr.projected td{background:#f3f3f3;font-style:italic}table{border-collapse:collapse;width:100%}td{border-top:1px solid #ccc;padding:6px;vertical-align:top}"""
for sport in ["football", "baseball", "track"]:
    md = open(f"{R}/v3/W10-playbooks/{sport}/PLAYBOOK.md").read()
    title = md.split("\n")[0].lstrip("# ").strip()
    sub = md.split("\n")[1].lstrip("# ").strip().replace("`", "")
    disc = re.search(r"^> .+$", md, re.M).group(0)
    partA = md.split("## Part A.")[1].split("## Part B.")[0]
    partA_title = partA.split("\n")[0].strip()
    partA_body = "\n".join(partA.split("\n")[1:])
    partB = md.split("## Part B.")[1].split("## Part C.")[0]
    stages = re.findall(r"^### (Stage \d+\. .+)$", partB, re.M)
    blocks = re.split(r"^### Stage ", partB, flags=re.M)[1:]
    dones = [re.search(r"\*\*Done when[^\n]*", b).group(0) if re.search(r"\*\*Done when[^\n]*", b) else "" for b in blocks]
    srcs = md.split("## Sources used")[1].strip().split("\n")[0]
    cal = open(f"{R}/funnel/lead-magnet/out/{sport}-class-2029.html").read()
    table = re.search(r"<table>.*?</table>", cal, re.S).group(0)
    stg = "".join(f"<div class=stage><b>{esc(s)}</b><br>{inline(d)}</div>" for s, d in zip(stages, dones))
    page = f"""<!doctype html><meta charset=utf-8><style>{CSS}</style><section>
<h1>{esc(sport.capitalize())} recruiting calendar, Class of 2029</h1><div class=sub>{esc(sub)}</div>{md_to_html(disc)}
<h2>Part A.{esc(partA_title)}</h2>{md_to_html(partA_body)}
<h2 class=pb>Dated calendar (each row cites its bylaw)</h2>{table}
<h2>The stages at a glance</h2>{stg}
<p class=foot>Sources used: {esc(srcs)} Full source table is in the Commit Book. Education, not legal advice. Rules change; check the cited source and each school's compliance office before acting. The Recruiting Calendar.</p></section>"""
    hp = f"{BUILD}/{sport}-class-2029.html"; open(hp, "w").write(page)
    pdf = f"{OUT}/{sport}-class-2029.pdf"
    if "--html-only" in sys.argv:
        print(sport, "html", os.path.getsize(hp), "bytes"); continue
    try:
        subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={pdf}", f"file://{hp}"], check=True, capture_output=True, timeout=90)
        print(sport, os.path.getsize(pdf), "bytes")
    except Exception as e:
        print(sport, "headless Chrome unavailable in this sandbox (", type(e).__name__, "); HTML written, print it via a browser page.pdf() (see DONE.md)")
