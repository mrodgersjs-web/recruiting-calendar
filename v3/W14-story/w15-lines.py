import pathlib,sys
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
ls=pathlib.Path("site/assets/deck.js").read_text(encoding="utf-8").splitlines()
for i,l in enumerate(ls[28:40],start=29):
    print(i, repr(l[:200]))
