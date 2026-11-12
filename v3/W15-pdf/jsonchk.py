import json,re,sys,pathlib
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
p=pathlib.Path(r"C:\Users\Jloeh\.aside\u\1\sessions\2026-11-08_sIbJ63jY5p1sXMzN\artifacts\recruitiq-basketball-playbook.md")
t=p.read_text(encoding="utf-8")
m=re.search(r"```json\n(.*?)\n```", t, re.S)
body=m.group(1)
ok=False
for fix in (body, "["+body, body if body.strip().startswith("[") else "["+body):
    try:
        rows=json.loads(fix); ok=True; break
    except Exception as e:
        err=str(e)
print("parses:", ok, "" if ok else err)
if ok:
    print("rows:", len(rows))
    print("kinds:", sorted({r["kind"] for r in rows}))
    missing=[r["event"][:40] for r in rows if not all(k in r for k in ("iso_date","kind","event","plain_english","cost_if_missed","rule","citation_url","owner","done_when"))]
    print("rows missing a field:", missing)
    if not body.strip().startswith("["):
        p.write_text(t.replace("```json\n"+body, "```json\n[\n"+body.rstrip().rstrip("]")+"\n]\n```") if False else t, encoding="utf-8")
    dates=sorted(r["iso_date"] for r in rows); print("date range:", dates[0], "to", dates[-1])
