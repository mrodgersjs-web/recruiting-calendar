import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = pathlib.Path("fb-plain.py"); s = p.read_text(encoding="utf-8")
old = "both equal 36.0. Division 2 and the FCS work this way."
new = "both equal 36.0. Division 2 works this way at 36.0, and the FCS at 63.0."
pat = re.compile(r"\s+".join(re.escape(t) for t in re.split(r"\s+", old)))
m = list(pat.finditer(s)); print("matches:", len(m))
if len(m) == 1:
    s = s[:m[0].start()] + new + s[m[0].end():]; p.write_text(s, encoding="utf-8")
