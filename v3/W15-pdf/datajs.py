import re,sys,pathlib,json
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
t=pathlib.Path("site/data.js").read_text(encoding="utf-8")
i=t.index("{"); doc=json.JSONDecoder().raw_decode(t[i:])[0]
print("top keys:", list(doc))
for k,v in list(doc.items())[:10]:
    if isinstance(v,dict): print(f"  {k}: dict({len(v)}) -> {list(v)[:12]}")
    elif isinstance(v,list): print(f"  {k}: list({len(v)}) -> {str(v[:2])[:160]}")
    else: print(f"  {k}: {str(v)[:100]}")
