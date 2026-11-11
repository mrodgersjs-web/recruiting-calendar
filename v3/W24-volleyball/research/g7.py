import pathlib, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
for f in ["02-measurables-by-position.md", "01-numbers-and-rules.md"]:
    t = pathlib.Path(f).read_text(encoding="utf-8").split("\n")
    print("#" * 20, f)
    for ln in t:
        low = ln.lower()
        if any(k in low for k in ["haley", "rose", "giacomazzi", "growth", "grow", "period", "menarche", "final height", "swedish", "cook", "hallisey", "sheffield", "86", "89", "middle", "composition"]):
            print(ln.strip()[:340]); print("-" * 24)
