import json,sys,pathlib
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
c=json.loads(pathlib.Path("v3/W1-playbooks/CATALOG.json").read_text(encoding="utf-8"))
print("keys:", list(c))
for p in c["catalog"]:
    keep={k:p[k] for k in ("slug","title","price_usd","status","pages","pages_a4","audience","file","pdf","filename") if k in p}
    print(json.dumps(keep, ensure_ascii=False))
print("BUNDLES:", json.dumps(c.get("bundles"), ensure_ascii=False)[:800])
