import pathlib, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
t = pathlib.Path("03-club-season-and-events.md").read_text(encoding="utf-8").split("\n")
for i, ln in enumerate(t):
    low = ln.lower()
    if any(k in low for k in ["wiaa", "18,137", "148", "14,628", "925", "trickle", "baird", "90%"]):
        print(ln.strip()[:330]); print("-" * 36)
