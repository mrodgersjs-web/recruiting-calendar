import json,pathlib,sys,re
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
js=pathlib.Path("site/assets/stories.js").read_text(encoding="utf-8")
d=json.JSONDecoder().raw_decode(js[js.index("{"):])[0]
C=[a for a in d["athletes"] if a.get("composite")]
R=[a for a in d["athletes"] if not a.get("composite")]
print("=== a composite entry (the pattern to copy)")
for k,v in sorted(C[0].items()):
    print(f"   {k:12} {str(json.dumps(v) if not isinstance(v,str) else v)[:130]}")
print("\n=== media by sport: composite art vs real art")
for a in d["athletes"]:
    print(f"   {str(a.get('composite')):5} {a['sport'][:12]:12} {a['id'][:20]:20} img={str(a.get('img'))[:46]:46} poster={str(a.get('poster'))[:40]}")
print("\n=== trailingSlash config")
vj=json.loads(pathlib.Path("vercel.json").read_text(encoding="utf-8"))
print("   trailingSlash:",vj.get("trailingSlash"),"cleanUrls:",vj.get("cleanUrls"))
print("   redirects:",len(vj.get("redirects",[])),"rewrites:",len(vj.get("rewrites",[])))
for r in vj.get("redirects",[])[:4]: print("     ",r)
