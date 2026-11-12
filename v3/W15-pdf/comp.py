import json,sys,pathlib,re
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
p=pathlib.Path("research/00-mm3-offers.json")
if p.exists():
    d=json.loads(p.read_text(encoding="utf-8"))
    items=d if isinstance(d,list) else d.get("offers") or list(d.values())[0]
    print("offers:", len(items))
    for o in items:
        t=json.dumps(o, ensure_ascii=False)
        if re.search(r"(?i)basket", t): print("   ", t[:220])
