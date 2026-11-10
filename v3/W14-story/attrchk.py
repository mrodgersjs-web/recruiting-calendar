import pathlib,sys,re
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
t=pathlib.Path("site/assets/ring.js").read_text(encoding="utf-8")
print("attr interpolations:", re.findall(r'(?:aria-label|title|alt)="[^"]{0,60}\$\{[^}]{1,40}\}[^"]{0,30}"', t)[:6])
print("count of ${a.name}:", t.count("${a.name}"), " ${a.short}:", t.count("${a.short}"))
