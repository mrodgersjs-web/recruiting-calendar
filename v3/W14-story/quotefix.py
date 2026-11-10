import pathlib,sys,re,json
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
p=pathlib.Path("site/assets/stories.js"); t=p.read_text(encoding="utf-8")
t2=re.sub(r'(\\"name\\": \\")Composite: \\\"([^"]*?)\\\"( \([^"]*?\))(\\"\\s*[,}])',
          lambda m: m.group(1)+"Composite: \u201c"+m.group(2)+"\u201d"+m.group(3)+m.group(4), t)
print("name values re-quoted:", t.count('\\"name\\"')-t2.count('\\"name\\"') if False else t2.count("\u201c"))
p.write_text(t2,encoding="utf-8")

r=pathlib.Path("site/assets/ring.js"); rt=r.read_text(encoding="utf-8")
helper="function escA(s){return String(s==null?\'\':s).replace(/[&<>\"]/g,function(c){return{\'&\':\'&amp;\',\'<\':\'&lt;\',\'>\':\'&gt;\',\'\"\':\'&quot;\'}[c]})}\n"
if "escA" not in rt:
    rt=re.sub(r"^", helper, rt, count=1)
n1=rt.count('aria-label="${a.name}"'); n2=rt.count('aria-label="Read story: ${a.name}"')
rt=rt.replace('aria-label="${a.name}"','aria-label="${escA(a.name)}"').replace('aria-label="Read story: ${a.name}"','aria-label="Read story: ${escA(a.name)}"')
r.write_text(rt,encoding="utf-8")
print("ring.js patched aria-labels:", n1, n2)
d=json.JSONDecoder().raw_decode(t2[t2.index("{"):])[0]
print("sample names:", [a["name"] for a in d["athletes"][:3]])
