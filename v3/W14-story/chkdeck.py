import pathlib,sys
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
t=pathlib.Path("site/assets/deck.js").read_text(encoding="utf-8")
for l in t.splitlines():
    if "SLUG(a.sport)" in l or "encodeURIComponent(p.id)" in l:
        print(l.strip()[:190])
