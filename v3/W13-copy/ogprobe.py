import re,pathlib,sys,collections
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
forms=collections.Counter()
for p in pathlib.Path("site").rglob("*.html"):
    t=p.read_text(encoding="utf-8",errors="ignore")
    for m in re.finditer(r'(?:og|twitter):image"?\s+content="([^"]+)"',t): forms[m.group(1)]+=1
for k,v in forms.most_common(8): print(f"  {v:4}x  {k}")
