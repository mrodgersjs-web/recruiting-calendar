import pathlib, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = pathlib.Path("site/app.js"); t = p.read_text(encoding="utf-8")
good = "const NAMES={baseball:'Baseball',football:'Football',track:'Track & field / cross country',basketball_girls:'Girls\\\\' basketball',basketball_boys:'Boys\\\\' basketball'};"
t2 = re.sub(r"const NAMES=\{[^}]*\};", good, t, count=1)
p.write_text(t2, encoding="utf-8")
print([l for l in t2.splitlines() if "NAMES={" in l][0])
print("nonascii:", sum(1 for b in p.read_bytes() if b > 127))
