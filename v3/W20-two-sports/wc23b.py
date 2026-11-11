import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
t = pathlib.Path("fb-plain.py").read_text(encoding="utf-8")
i = t.find('<div class="tmpl">')
print("======= FOOTBALL TMPL =======")
print(t[i:t.find("</div>", i)])
for m in re.finditer(r"[^.]{0,120}\b(words|word count)\b[^.]{0,80}\.", t):
    print("RULE >>>", re.sub(r"\s+", " ", m.group(0)))
u = pathlib.Path("wbb-plain.py").read_text(encoding="utf-8")
j = u.find('<div class="tmpl">')
print("======= GIRLS TMPL =======")
print(u[j:u.find("</div>", j)])
for m in re.finditer(r"[^.]{0,120}\b(words|word count)\b[^.]{0,80}\.", u):
    print("RULE >>>", re.sub(r"\s+", " ", m.group(0)))
