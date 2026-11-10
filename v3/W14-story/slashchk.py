import pathlib,re,sys
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
SITE=pathlib.Path("site"); slash={}
for p in sorted(SITE.rglob("*.html")):
    t=p.read_text(encoding="utf-8",errors="ignore")
    for m in re.finditer(r'href="(/[^"]?[^/"]*/)"',t):
        slash.setdefault(m.group(1),set()).add(str(p.relative_to(SITE)))
print("trailing-slash internal links:",len(slash))
for u,s in sorted(slash.items())[:8]: print("  ",u,"<-",len(s),"pages e.g.",sorted(s)[0])
