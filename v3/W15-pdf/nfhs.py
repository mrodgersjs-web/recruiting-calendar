import re,sys,pathlib,html
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
t=pathlib.Path("site/emerging-sports/index.html").read_text(encoding="utf-8")
rows=re.findall(r"<tr>(.*?)</tr>", t, re.S)
for r in rows:
    cells=[html.unescape(re.sub(r"<[^>]+>"," ",c)).strip() for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", r, re.S)]
    if cells: print(" | ".join(c[:26] for c in cells))
