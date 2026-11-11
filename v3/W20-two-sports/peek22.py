import sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
t = pathlib.Path("wbb-plain.py").read_text(encoding="utf-8")
i = t.find("132 pounds")
print(repr(t[i-160:i+220]))
