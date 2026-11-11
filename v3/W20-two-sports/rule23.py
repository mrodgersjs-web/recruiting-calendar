import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
for f in ("fb-plain.py","wbb-plain.py"):
    t = pathlib.Path(f).read_text(encoding="utf-8")
    print("##### " + f)
    for pat in (r"phone screen", r"\b180\b", r"\b150\b", r"one screen", r"letters"):
        for m in re.finditer(pat, t):
            print("  [" + pat + "] ...", re.sub(r"\s+"," ", t[max(0,m.start()-150):m.end()+150]))
