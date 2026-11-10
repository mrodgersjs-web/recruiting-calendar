import re,pathlib,sys
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
t=pathlib.Path("site/playbooks/football-junior-year/index.html").read_text(encoding="utf-8")
i=t.find("Stories that use it")
print(repr(t[i-120:i+700]))
