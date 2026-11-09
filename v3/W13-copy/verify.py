import re,pathlib,sys
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
root=pathlib.Path("site")
bad=[]
for p in list(root.rglob("*.html"))+list(root.rglob("*.js"))+list(root.rglob("*.json"))+list(root.rglob("*.xml")):
    t=p.read_text(encoding="utf-8",errors="ignore")
    for m in re.finditer(r"/(assets|downloads|story|athlete|playbooks|tools|legal|api)/([\w./?=&-]+)",t):
        u=("/"+m.group(1)+"/"+m.group(2)).split("?")[0].split("#")[0]
        if u.endswith("/"): tgt=root/u.lstrip("/")/"index.html"
        else: tgt=root/u.lstrip("/")
        if not tgt.exists() and not (root/u.lstrip("/")).exists():
            bad.append((str(p.relative_to(root)),u))
seen=set(); u2=[x for x in bad if not(x in seen or seen.add(x))]
print("broken local references:",len(u2))
for f,u in u2[:20]: print("   ",f,"->",u)
surs=["butler","coward","groenewegen","lowe","marpet","perez","pichardo","pirosko","renfrow","rodriguez","rodenfels","wondolowski"]
left=[(str(p.relative_to('site')),s) for p in root.rglob("*") if p.is_file() and p.suffix.lower() in {".html",".js",".json",".xml"} for s in surs for _ in re.finditer(r"[\"'>/:(]"+s+r"[-\".,/)>:']",p.read_text(encoding="utf-8",errors="ignore"))]
print("surname leftovers in deployed data keys/paths:",len(set(left)))
for x in list(set(left))[:8]: print("   ",x)
