import re,pathlib,sys
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
SUR={"butler":"jimmy","coward":"cedric","groenewegen":"sara","lowe":"karsta","marpet":"ali","perez":"tori","pichardo":"olivia","pirosko":"samantha","renfrow":"hunter","rodriguez":"cristelle","rodenfels":"annie","white":"derrick","wondolowski":"chris"}
# 1. story pages kept the old plural canonical/og:url prefix, and their media refs were stale
n=0
for p in pathlib.Path("site").rglob("*.html"):
    t=p.read_text(encoding="utf-8",errors="ignore"); o=t
    for sur,first in SUR.items():
        t=re.sub(r"/stories/"+sur+r"/","/story/"+first+"/",t)
        t=re.sub(r"/stories/"+sur+r"(?!/)","/story/"+first+"/",t)
        t=re.sub(r"(/assets/media/[a-z-]*?)-"+sur+r"-",r"\g<1>-"+first+"-",t)
    if t!=o: p.write_text(t,encoding="utf-8"); n+=1
print("html files repaired:",n)

# 2. verify every root-relative href/src and json path resolves on disk
bad=[]
for p in list(pathlib.Path("site").rglob("*.html"))+list(pathlib.Path("site").rglob("*.js"))+list(pathlib.Path("site").rglob("*.json")):
    t=p.read_text(encoding="utf-8",errors="ignore")
    vals=re.findall(r'(?:href|src|poster|video|img|image|file|url)\s*=\s*"?(/[\w./-]+)',t)
    vals+=re.findall(r'"(/[A-Za-z0-9./_-]+)"',t)
    for u in set(vals):
        u=u.split("?")[0].split("#")[0]
        if u.startswith("//"): continue
        tgt=pathlib.Path("site")/u.lstrip("/")
        ok = tgt.exists() or (tgt/"index.html").exists()
        if not ok: bad.append((str(p.relative_to("site")),u))
seen=set(); uniq=[x for x in bad if not (x in seen or seen.add(x))]
print("broken root-relative references:",len(uniq))
for f,u in uniq[:15]: print("   ",f,"->",u)

# 3. surname sweep on the deployed tree, case sensitive on keys, any case in paths
surs=list(SUR)
left=set()
for p in pathlib.Path("site").rglob("*"):
    if not (p.is_file() and p.suffix.lower() in {".html",".js",".json",".xml",".css"}): continue
    t=p.read_text(encoding="utf-8",errors="ignore")
    for s in surs:
        for m in re.finditer(r"[\"'>/:(]"+s+r"[\-\".,/)>:']",t): left.add((str(p.relative_to("site")),m.group(0)))
    for m in re.finditer(r"\b[A-Z][a-z]+\s+(Renfrow|Butler|Coward|Groenewegen|Marpet|Pichardo|Pirosko|Rodenfels|Wondolowski)\b",t):
        left.add((str(p.relative_to("site")),m.group(0)))
print("surname tokens left in deployed html/json:",len(left))
for x in sorted(left)[:10]: print("   ",x)
