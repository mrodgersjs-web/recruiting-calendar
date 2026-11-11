import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = pathlib.Path("wbb-plain.py"); t = p.read_text(encoding="utf-8")
pat = re.compile(r"For scale, the median American girl at 15 is 5 foot 4 and 132 pounds, so a 5'7\" sophomore "
                 r"guard is\s+already tall for her age, and a 5'8\" one is\s+close to done growing\.")
new = ("For scale, most girls are within about an inch of their adult height by 15, so the size line she "
       "sends as a sophomore is close to the final one.")
t, n = pat.subn(new, t)
print("growth sentence replaced:", n)
p.write_text(t, encoding="utf-8")
