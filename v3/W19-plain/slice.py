import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
t = pathlib.Path("bball-plain.py").read_text(encoding="utf-8")
i = t.find("We could not settle two dates")
print(repr(t[i - 60:i + 900]))
