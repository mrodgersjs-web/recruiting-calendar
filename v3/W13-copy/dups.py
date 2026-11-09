import re,pathlib,sys,collections
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
dup=collections.Counter(); files={}
for p in pathlib.Path("site").rglob("*.html"):
    t=p.read_text(encoding="utf-8",errors="ignore")
    for m in re.finditer(r"\b([a-z]{2,})\s+\1\b",t):
        dup[m.group(0)]+=1; files.setdefault(m.group(0),set()).add(str(p.relative_to("site")))
    for m in re.finditer(r"\b(the|a|to|of|at) \1\b",t):
        dup[m.group(0)]+=1; files.setdefault(m.group(0),set()).add(str(p.relative_to("site")))
for k,v in dup.most_common(14): print(f"  {v:3}x  {k!r}   {sorted(files[k])[:2]}")
