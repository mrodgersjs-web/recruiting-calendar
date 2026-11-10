import json,pathlib,sys,re
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
t=pathlib.Path("site/assets/stories.js").read_text(encoding="utf-8")
d=json.JSONDecoder().raw_decode(t[t.index("{"):])[0]
A=d["athletes"]
print("athletes:",len(A))
for a in A:
    print("  ", a["id"], "|", a.get("name"), "|", a.get("sport"), "| div:", a.get("div"), "| from:", str(a.get("from"))[:26], "| college:", str(a.get("college"))[:22], "| hold:", a.get("hold"), "| keys:", len(a))
print("\nfield union:", sorted({k for a in A for k in a}))
rj=pathlib.Path("site/assets/ring.js").read_text(encoding="utf-8")
i=rj.find("function cardHTML")
if i<0: i=rj.find("cardHTML=")
print("\ncardHTML source:\n", re.sub(r"\s+"," ",rj[i:i+700]))
