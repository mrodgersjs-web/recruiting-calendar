import re,sys,pathlib,collections
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
hits=collections.Counter()
for p in sorted(pathlib.Path("site").rglob("*.html")):
    t=p.read_text(encoding="utf-8",errors="ignore")
    for m in re.finditer(r'href=?["\']?(/downloads/[\w.-]+)',t):
        hits[(m.group(1).strip('"\''),str(p.relative_to("site")))]+=1
for (u,page),n in sorted(hits.items()):
    print(f"{u:44} on {page}")
print("distinct files linked:", len({u for u,_ in hits}))
