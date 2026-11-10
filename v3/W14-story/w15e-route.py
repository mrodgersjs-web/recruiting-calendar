import pathlib,sys
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
p=pathlib.Path("site/assets/deck.js"); t=p.read_text(encoding="utf-8")
old = "</h2><p class=\"dk-route\">'+esc(a.from)+' <span>\u2192</span> '+esc(a.college)+'</p>'+"
new = "</h2>'+"
print("plain-old present:", old in t)
t=t.replace(old,new)
p.write_text(t,encoding="utf-8")
import re
print("field refs left:", sorted({m.group(0) for m in re.finditer(r"a[.](div|from|college)", t)}))
i=t.find("dk-read"); print("cta line:", re.sub(r"\s+"," ",t[i-230:i+130]))
