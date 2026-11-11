import pathlib, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
t = pathlib.Path("04-film-and-outreach.md").read_text(encoding="utf-8").split("\n")
for i, ln in enumerate(t):
    if "Ellmann" in ln or "Jenkins" in ln or "Perkins" in ln or "defensive" in ln.lower() and "email" in ln.lower():
        print(ln.strip()[:700]); print("=" * 30)
