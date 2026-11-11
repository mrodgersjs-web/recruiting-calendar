import pathlib, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
for f in ["01-numbers-and-rules.md", "02-measurables-by-position.md"]:
    t = pathlib.Path(f).read_text(encoding="utf-8").split("\n")
    print("#" * 20, f)
    for ln in t:
        low = ln.lower()
        if any(k in low for k in ["5.21", ".405", "4.69", "10.51", "0.51", "dig leader", "dig leaders", "147", "5'1", "usav", "average about"]):
            print(ln.strip()[:400]); print("-" * 30)
