"""W15g: no athlete pages left at all. Delete them, redirect them, re-stamp, rebuild sitemap."""
import json
import pathlib
import shutil
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = pathlib.Path(__file__).resolve().parents[2]
SITE = ROOT / "site"

ID_TO_SLUG = {"composite-swim": "swimming", "composite-football": "football",
              "composite-baseball": "baseball", "composite-softball": "softball",
              "composite-wbasketball": "basketball", "composite-wrestling": "wrestling",
              "composite-volleyball": "volleyball", "composite-sprinter": "track-field"}

removed = []
for parent in ("story", "athlete"):
    d = SITE / parent
    if d.exists():
        for kid in sorted(d.iterdir()):
            if kid.is_dir():
                shutil.rmtree(kid)
                removed.append(f"/{parent}/{kid.name}")
        shutil.rmtree(d)
print("directories removed:", len(removed))

vj = ROOT / "vercel.json"
cfg = json.loads(vj.read_text(encoding="utf-8"))
have = {r["source"] for r in cfg.get("redirects", [])}
added = 0
for bid, slug in sorted(ID_TO_SLUG.items()):
    for kind in ("story", "athlete"):
        src = f"/{kind}/{bid}"
        if src in have:
            continue
        cfg["redirects"].append({"source": src, "destination": f"/sports/{slug}", "permanent": True})
        added += 1
vj.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")
print(f"redirects added: {added}, total now {len(cfg['redirects'])}")

for script in ("v3/W14-story/reversion.py", "v3/W13-copy/sitemap.py", "v3/W14-story/verifyw14b.py"):
    r = subprocess.run([sys.executable, str(ROOT / script)], capture_output=True, text=True, cwd=ROOT)
    tail = [l for l in (r.stdout or "").splitlines() if l.strip()][:4]
    print(f"--- {script}")
    for l in tail:
        print("   ", l)
