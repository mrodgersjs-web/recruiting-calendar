#!/usr/bin/env python3
"""W14: read the rotator, the athlete data behind it, and the playbook catalog."""
import json, re, pathlib, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = pathlib.Path(__file__).resolve().parents[2]
SITE = ROOT / "site"

js = (SITE / "assets" / "stories.js").read_text(encoding="utf-8")
dec = json.JSONDecoder()
names = re.findall(r"window\.(\w+)\s*=", js)
print("== stories.js globals:", names)
i = js.index("{")
obj, _end = dec.raw_decode(js[i:])
ath = obj["athletes"]
print("athletes:", len(ath))
for a in ath:
    print(f"  {str(a.get('id')):18} {str(a.get('short') or a.get('name'))[:20]:20} "
          f"sport={str(a.get('sport'))[:11]:11} comp={str(a.get('composite')):5} "
          f"div={str(a.get('div'))[:10]:10} college={str(a.get('college'))[:16]:16}")
print("\nentry keys:", sorted(ath[0].keys()))
by_sport = {}
for a in ath:
    by_sport.setdefault(str(a.get("sport")), []).append(str(a.get("id")))
print("\nathletes by sport:")
for s, ids in sorted(by_sport.items()):
    print(f"   {s:14} {len(ids):2}  {' '.join(ids)}")

print("\n== rotator renderer")
for p in sorted((SITE / "assets").glob("*.js")):
    t = p.read_text(encoding="utf-8", errors="ignore")
    for m in re.finditer(r"customElements\.define\(\s*[\"']([\w-]+)[\"']", t):
        print(f"   {p.name}: defines <{m.group(1)}>")
    if "story-ring" in t:
        for m in re.finditer(r".{0,110}story-ring.{0,110}", t):
            print("   ctx:", re.sub(r"\s+", " ", m.group(0))[:220])
        j = t.find("/story/")
        if j > -1:
            print("   anchor:", re.sub(r"\s+", " ", t[max(0, j - 200):j + 120]))

print("\n== playbook catalog")
cat = json.loads((ROOT / "v3" / "W1-playbooks" / "CATALOG.json").read_text(encoding="utf-8"))
rows = cat if isinstance(cat, list) else (cat.get("playbooks") or cat.get("items") or list(cat.values())[0])
for r in rows:
    if isinstance(r, dict):
        print(f"   {str(r.get('slug')):32} {str(r.get('title'))[:38]:38} sport={r.get('sport')} "
              f"price={r.get('price')} status={r.get('status')}")
print("\n== deployed playbook pages")
print("   ", ", ".join(sorted(p.parent.name for p in (SITE / "playbooks").glob("*/index.html"))))
