import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = pathlib.Path("wbb-plain.py"); t = p.read_text(encoding="utf-8")
new = ("For scale, most girls are within about an inch of their adult height by 15, so the size line "
       "she sends as a sophomore is close to the final one.")
t, n = re.subn(r"For\s+scale.*?done growing\.", new, t, count=1, flags=re.S)
print("replaced:", n)
p.write_text(t, encoding="utf-8")
