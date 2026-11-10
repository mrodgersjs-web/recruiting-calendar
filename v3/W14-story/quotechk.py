import pathlib,sys,re
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
js=pathlib.Path("site/assets/stories.js").read_text(encoding="utf-8")
print("names in data:", re.findall(r'"name":\s*"([^"]*)"', js)[:4])
print("escaped-as-quote form:", js.count('Composite: \\"'))
pat = re.compile(r'aria-label="[^"]*"[^>]*')
tot=0; shapes=set()
for p in pathlib.Path("site").rglob("*.html"):
    t=p.read_text(encoding="utf-8")
    for m in pat.finditer(t):
        s=m.group(0)
        if 'Composite' in s:
            tot+=1; shapes.add(s[:120])
print("malformed aria-labels:", tot)
for s in list(shapes)[:4]: print("   ", s)
rjs=pathlib.Path("site/assets/ring.js").read_text(encoding="utf-8")
print("ring.js esc:", re.findall(r"function esc[\s\S]{0,200}", rjs)[:1])
print("aria-label builders:", re.findall(r"aria-label=.{0,80}", rjs)[:4])
