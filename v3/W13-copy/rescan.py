import re,pathlib
surs=["butler","coward","groenewegen","lowe","marpet","perez","pichardo","pirosko","renfrow","rodriguez","rodenfels","wondolowski","white"]
hits={}
for p in pathlib.Path("site").rglob("*"):
    if not p.is_file(): continue
    if p.suffix.lower() not in {".html",".js",".json",".xml",".css",".txt",".md"}: continue
    t=p.read_text(encoding="utf-8",errors="ignore")
    for s in surs:
        for m in re.finditer(r"\b"+s+r"\b",t,re.I):
            ctx=re.sub(r"\s+"," ",t[max(0,m.start()-70):m.end()+50])
            hits.setdefault(s.lower(),[]).append((str(p.relative_to("site")),ctx))
for s,v in hits.items():
    print(f"\n### {s}  ({len(v)} hits)")
    seen=set()
    for f,c in v[:6]:
        if c in seen: continue
        seen.add(c); print("   ",f,"::",c[:150])
print("\n=== poster / real-* assets on disk")
print([str(p.relative_to('site')) for p in pathlib.Path('site/assets/media').glob('*poster*')][:12])
