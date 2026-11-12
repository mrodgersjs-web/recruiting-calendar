import re,sys,pathlib,json
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
t=pathlib.Path("site/data.js").read_text(encoding="utf-8")
i=t.index("{"); doc=json.JSONDecoder().raw_decode(t[i:])[0]
for s,v in doc.items():
    dl=v["deadlines"]
    cited=sum(1 for d in dl if re.search(r"https?://|NCAA|Bylaw|bylaw", json.dumps(d)))
    print(f"{s:10} class {v['class_year']} verified {v['verified_on']}  deadlines {len(dl):2}  with a citation {cited:2}  label {v['source_label'][:40]}")
    print("           fields:", list(dl[0]))
print("=== rules pages on disk")
for p in sorted(pathlib.Path("site/rules").rglob("index.html")) if pathlib.Path("site/rules").exists() else []:
    print("  ", str(p.relative_to("site")))
print("=== every sport the site names anywhere")
sports=set()
for p in pathlib.Path("site").rglob("*.html"):
    pass
print("  sports/* pages:", ", ".join(sorted(p.parent.name for p in pathlib.Path("site/sports").glob("*/index.html"))))
