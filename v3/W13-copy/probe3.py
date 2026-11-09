import json,pathlib
d=json.loads(pathlib.Path("site/recruitiq/data.json").read_text(encoding="utf-8"))
for p in d["programs"]:
    print(f'{p["id"]:<16} name={p.get("name")!r:<18} level={p.get("level")!r:<6} conf={p.get("conference")!r:<12} note={p.get("label_note","")[:60]!r}')
    print(f'    url={p.get("url")}')
print("\nunno keys:",list(d.get("uno",{}).keys())[:8] if isinstance(d.get("uno"),dict) else type(d.get("uno")))
print("bucket3 sample:",json.dumps(d["bucket3"])[:300])
