import re,pathlib,sys,html
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
def prose(t):
    t=re.sub(r"<(script|style|noscript|svg)[^>]*>.*?</\1>"," ",t,flags=re.S|re.I)
    t=re.sub(r"<table\b.*?</table>"," ",t,flags=re.S|re.I)
    t=re.sub(r"<nav\b.*?</nav>"," ",t,flags=re.S|re.I)
    t=re.sub(r"<footer\b.*?</footer>"," ",t,flags=re.S|re.I)
    t=re.sub(r"<[^>]*>"," ",t); t=html.unescape(t); return re.sub(r"\s+"," ",t).strip()
def mask(t):
    t=re.sub(r"\b\d+(?:[.-]\d+)+\b"," x ",t)                 # bylaw numbers 13.6.2.1.7
    t=re.sub(r"\b\d{4}-\d{2}-\d{2}\b"," x ",t)               # dates
    t=re.sub(r"\b\d{4}-\d{2}\b"," x ",t)                      # 2026-27
    t=re.sub(r"[·|]"," ",t)
    return re.sub(r"\s+"," ",t)
def fk(text):
    s=re.findall(r"[A-Za-z][A-Za-z'\- ]*[.!?]",text) or [text]
    def syl(w):
        w=re.sub(r"[^a-z]","",w.lower())
        if not w: return 0
        n=len(re.findall(r"[aeiouy]+",w))
        if w.endswith("e") and n>1: n-=1
        return max(1,n)
    W=re.findall(r"[A-Za-z][A-Za-z'\-]*",text); S=max(len(s),1)
    return 0 if len(W)<40 else round(0.39*len(W)/S+11.8*sum(syl(w) for w in W)/len(W)-15.59,1)
rows=[]
for p in sorted(pathlib.Path("site").rglob("*.html")):
    g=fk(mask(prose(p.read_text(encoding="utf-8",errors="ignore"))))
    if g: rows.append((g,str(p.relative_to("site").parent).replace("\\","/")))
rows.sort(reverse=True); sc=sorted(r[0] for r in rows)
med=sc[len(sc)//2] if len(sc)%2 else (sc[len(sc)//2-1]+sc[len(sc)//2])/2
print(f"prose only, citations masked, {len(sc)} pages: median {med:.1f}  above 8.9: {sum(1 for g in sc if g>8.9)}  above 10.5: {sum(1 for g in sc if g>10.5)}")
for g,p in rows[:8]: print(f"  {g:5}  {p}")
