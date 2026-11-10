import pathlib,sys,re
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
p=pathlib.Path("site/assets/deck.js"); t=p.read_text(encoding="utf-8")
pat = r"\\'</h2><p class=\"dk-route\">\\'\+esc\(a\.from\)\+\\' <span>\u2192</span> \\'\\+esc\(a\.college\)\+\\'</p>\\'"
t2,n = re.subn(pat, "\\\'</h2>", t)
print("route removed:", n)
p.write_text(t2,encoding="utf-8")
print("field refs left:", sorted({m.group(0) for m in re.finditer(r"a[.](div|from|college)", t2)}))
i=t2.find("dk-read"); print("cta line:", re.sub(r"\s+"," ",t2[i-200:i+120]))
