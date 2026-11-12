import re,sys,pathlib,json,html as H
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
t=pathlib.Path("site/data.js").read_text(encoding="utf-8")
i=t.index("{"); doc=json.JSONDecoder().raw_decode(t[i:])[0]
print("=== one deadline row, verbatim (football, first):")
print(json.dumps(doc["football"]["deadlines"][0], indent=1, ensure_ascii=False))
print("=== kinds used:", sorted({d["kind"] for s in doc.values() for d in s["deadlines"]}))
print("=== basketball research already in repo:")
hits=[p for p in pathlib.Path(".").rglob("*") if p.is_file() and re.search(r"(?i)basket|bball|hoops", p.name) and ".git" not in p.parts]
for p in hits[:20]: print("   ", str(p))
print("   total", len(hits))
print("=== research/ dir top level:")
for p in sorted(pathlib.Path("research").iterdir())[:20]: print("   ", ("dir " if p.is_dir() else "file"), p.name)
