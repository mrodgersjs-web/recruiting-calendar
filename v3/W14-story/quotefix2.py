import pathlib,sys,re,json
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
p=pathlib.Path("site/assets/stories.js"); t=p.read_text(encoding="utf-8")
t2,k=re.subn(r"Composite: \\\u0022(.+?)\\\u0022 \(", lambda m: "Composite: \u201c"+m.group(1)+"\u201d (", t)
print("rewritten:",k)
p.write_text(t2,encoding="utf-8")
d=json.JSONDecoder().raw_decode(t2[t2.index("{"):])[0]
print("sample:", [a["name"] for a in d["athletes"][:3]])
print("composite:true:", sum(1 for a in d["athletes"] if a.get("composite")), "of", len(d["athletes"]))
