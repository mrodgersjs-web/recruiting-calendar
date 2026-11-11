import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
raw = pathlib.Path("vb-text.txt").read_text(encoding="utf-8")
parts = re.split(r"===== PAGE (\d+) =====", raw)
for i in range(1, len(parts)-1, 2):
    t = parts[i+1]
    if "THECOMMITBOOK" not in re.sub(r"\s+","",t).upper():
        print("PAGE", parts[i], "no header token. tail repr:")
        print(repr(t[-240:]))
        print("head repr:", repr(t[:160]))
