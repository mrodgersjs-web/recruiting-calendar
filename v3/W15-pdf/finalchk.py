import json,sys,re,pathlib
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
p=pathlib.Path(r"C:\Users\Jloeh\.aside\u\1\sessions\2026-11-08_sIbJ63jY5p1sXMzN\artifacts\recruitiq-basketball-playbook.md")
t=p.read_text(encoding="utf-8")
rows=json.loads(re.search(r"```json\n(.*?)\n```", t, re.S).group(1))
print("calendar rows valid:", len(rows), "| projected rows:", [r["iso_date"] for r in rows if r["kind"]=="projected"])
print("every row has owner+done_when:", all("owner" in r and "done_when" in r for r in rows))
