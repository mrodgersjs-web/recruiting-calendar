import re,pathlib,sys,html
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
def prose(t):
    t=re.sub(r"<(script|style|noscript|svg)[^>]*>.*?</\1>"," ",t,flags=re.S|re.I)
    t=re.sub(r"<table\b.*?</table>"," ",t,flags=re.S|re.I)          # data grids
    t=re.sub(r"<nav\b.*?</nav>"," ",t,flags=re.S|re.I)
    t=re.sub(r"<footer\b.*?</footer>"," ",t,flags=re.S|re.I)
    t=re.sub(r"<[^>]*class=\"[^\"]*(chip|tag|kicker|src|cite|badge|pill|stat)[^\"]*\"[^>]*>[^<]*</[^>]+>"," ",t,flags=re.I)
    t=re.sub(r"<[^>]*>"," ",t); t=html.unescape(t); return re.sub(r"\s+"," ",t).strip()
def fk(text):
    s=re.findall(r"[A-Za-z][A-Za-z'\- ]*[.!?]",text) or [text]
    def syl(w):
        w=re.sub(r"[^a-z]","",w.lower());
        if not w: return 0
        g=re.findall(r"[aeiouy]+",w); n=len(g)
        if w.endswith("e") and n>1: n-=1
        return max(1,n)
    W=re.findall(r"[A-Za-z][A-Za-z'\-]*",text); S=max(len(s),1)
    return 0 if len(W)<40 else round(0.39*len(W)/S+11.8*sum(syl(w) for w in W)/len(W)-15.59,1)
rows=[]
for p in sorted(pathlib.Path("site").rglob("*.html")):
    g=fk(prose(p.read_text(encoding="utf-8",errors="ignore")))
    if g: rows.append((g,str(p.relative_to("site").parent).replace("\\","/")))
rows.sort(reverse=True)
sc=[r[0] for r in rows]
sc_sorted=sorted(sc); med=sc_sorted[len(sc_sorted)//2] if len(sc)%2 else (sc_sorted[len(sc)//2-1]+sc_sorted[len(sc)//2])/2
print(f"prose-only scores on {len(sc)} pages: median {med:.1f}  above 8.9: {sum(1 for g in sc if g>8.9)}  above 12: {sum(1 for g in sc if g>12)}")
for g,p in rows[:10]: print(f"  {g:5}  {p}")
