import re,pathlib,sys,collections
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
GOOD="https://recruiting-calendar.vercel.app/assets/logo/social-card-dark.png"
BAD=["/assets/logo/social-card-dark.png","https://recruiting-calendar.vercel.app/og/default.png"]
n=0
for p in pathlib.Path("site").rglob("*.html"):
    t=p.read_text(encoding="utf-8",errors="ignore"); o=t
    for b in BAD:
        t=re.sub(r"((?:og|twitter):image\"?\s+content=\")"+re.escape(b)+"\"", lambda m: m.group(1)+GOOD+"\"", t)
    if t!=o: p.write_text(t,encoding="utf-8"); n+=1
print("pages with a fixed social card:",n)
f=collections.Counter()
for p in pathlib.Path("site").rglob("*.html"):
    for m in re.finditer(r"(?:og|twitter):image\"?\s+content=\"([^\"]+)\"",p.read_text(encoding="utf-8",errors="ignore")): f[m.group(1)]+=1
for k,v in f.most_common(5): print(f"  {v:4}x  {k}")
