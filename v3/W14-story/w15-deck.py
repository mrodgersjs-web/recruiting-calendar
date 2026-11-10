import pathlib,sys,re
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
d=pathlib.Path("site/assets/deck.js").read_text(encoding="utf-8")
print("=== deck.js (first 3000 chars)")
print(d[:3000])
