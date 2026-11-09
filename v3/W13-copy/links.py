import re,pathlib,os
root=pathlib.Path("site")
def exists(p):
    p=str(p).split("#")[0].split("?")[0]
    if p.startswith("http") or p.startswith("mailto:") or p.startswith("data:"): return True
    if p.startswith("/"): p=p.lstrip("/")
    else: p=os.path.relpath(os.path.join(base_dir,p),str(root))
    if p=="": p="."
    tgt=root/p
    return (tgt/"index.html").exists() or tgt.exists() or (root/(p+"/index.html")).exists()
bad=[]
for f in root.rglob("*.html"):
    base_dir=str(f.parent); t=f.read_text(encoding="utf-8",errors="ignore")
    for m in re.finditer(r'href="([^"]+)"',t):
        u=m.group(1)
        if not exists(u): bad.append((str(f.relative_to(root)),u))
    for m in re.finditer(r"href=([/\w][^\s>]*)",t):   # unquoted attrs, which this site uses
        u=m.group(1)
        if not exists(u): bad.append((str(f.relative_to(root)),u))
seen=set(); out=[]
for a,b in bad:
    if (a,b) in seen: continue
    seen.add((a,b)); out.append((a,b))
print("broken internal links:",len(out))
for a,b in out[:20]: print(f"   {a}  ->  {b}")
