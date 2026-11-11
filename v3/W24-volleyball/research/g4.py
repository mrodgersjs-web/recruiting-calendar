import pathlib, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
t = pathlib.Path("02-measurables-by-position.md").read_text(encoding="utf-8").split("\n")
start = None
for i, ln in enumerate(t):
    if "ranked" in ln.lower() or "NCAA ranked" in ln or "5.21" in ln:
        start = i - 6
        break
print("\n".join(x[:220] for x in t[max(0,start):start+70]))
