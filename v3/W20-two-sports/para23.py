import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
for f in ("fb-plain.py","wbb-plain.py"):
    t = pathlib.Path(f).read_text(encoding="utf-8")
    i = t.find("Stay near 70 letters")
    print("##### " + f)
    print(t[max(0,i-700):i+900])
