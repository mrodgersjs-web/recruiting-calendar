import json,re,sys,pathlib
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
art=pathlib.Path(r"C:\Users\Jloeh\.aside\u\1\sessions\2026-11-08_sIbJ63jY5p1sXMzN\artifacts")
p=art/"recruitiq-basketball-playbook.md"
t=p.read_text(encoding="utf-8")
m=re.search(r"```json\n(.*?)\n```", t, re.S)
rows=json.loads("["+m.group(1))
rows.sort(key=lambda r:r["iso_date"])
pretty="```json\n"+json.dumps(rows, indent=2, ensure_ascii=False)+"\n```"
t=t[:m.start()]+pretty+t[m.end():]
p.write_text(t,encoding="utf-8")
(art/"basketball-deadlines-class-2029.json").write_text(json.dumps({"class_year":2029,"verified_on":"2026-11-10","source_label":"2026-27 NCAA Division I Manual + NCAA recruiting calendar and signing-date pages","deadlines":rows}, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
chk=json.loads(re.search(r"```json\n(.*?)\n```", p.read_text(encoding="utf-8"), re.S).group(1))
print("fence now a valid array:", len(chk), "rows; file also written separately")
print("sizes:", {f.name: f.stat().st_size for f in [p, art/"basketball-deadlines-class-2029.json", art/"recruitiq-basketball-research.md", art/"recruitiq-focus-catalog.md"]})
