import pathlib,sys,re,collections
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
SITE=pathlib.Path("site")
PAT=re.compile(r"(stor(y|ies)|high school|junior college|JUCO|juco|Division \w|college athlete|not what happened after|real athlete)",re.I)
c=collections.Counter(); samples={}
for p in sorted(SITE.rglob("*.html")):
    t=p.read_text(encoding="utf-8",errors="ignore")
    # visible text only, scripts stripped
    body=re.sub(r"(?is)<(script|style|svg)[^>]*>.*?</\1>"," ",t)
    body=re.sub(r"(?is)<!--.*?-->"," ",body)
    txt=re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",body))
    for m in PAT.finditer(txt):
        key=(m.group(0).lower(), "BODY")
        c[key]+=1; samples.setdefault(key, str(p.relative_to(SITE)))
    for m in PAT.finditer(t):
        key=(m.group(0).lower(),"RAW")
        c[key]+=1
for (k,kind),n in sorted(c.items(), key=lambda x:-x[1]):
    print(f"{n:6}  {kind:5}  {k:22} e.g. {samples.get((k,'BODY'),'-')}")
print("\n--- <title>s containing 'stor'")
tt=collections.Counter()
for p in SITE.rglob("*.html"):
    m=re.search(r"<title>([^<]*)</title>", p.read_text(encoding="utf-8",errors="ignore"))
    if m and "stor" in m.group(1).lower(): tt[m.group(1)]+=1
for t,n in tt.most_common(6): print(f"   {n:4}  {t}")
