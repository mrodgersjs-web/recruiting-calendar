import json,sys,pathlib,re
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
c=json.loads(pathlib.Path("v3/W1-playbooks/CATALOG.json").read_text(encoding="utf-8"))
print("generated:", c.get("generated"), "| rules_verified_against:", json.dumps(c.get("rules_verified_against"), ensure_ascii=False)[:400])
print("integrity:", json.dumps(c.get("integrity"), ensure_ascii=False)[:500])
print("price_comps:", json.dumps(c.get("price_comps"), ensure_ascii=False)[:300])
for p in sorted(pathlib.Path("v3/W2-playbooks").glob("*.pdf")):
    t=p.read_bytes()
    m=[int(x) for x in re.findall(rb"/Count (\d+)", t)]
    print(f"{p.name:36} {len(t):8} bytes  declared pages {max(m) if m else '?'}  mtime {p.stat().st_mtime_ns and __import__('datetime').datetime.fromtimestamp(p.stat().st_mtime).date()}")
