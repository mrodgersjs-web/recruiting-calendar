import pathlib,sys,re
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
for f in ["site/assets/ring.js","site/assets/deck.js"]:
    t=pathlib.Path(f).read_text(encoding="utf-8")
    print("###",f)
    for m in re.finditer(r"a\.(div|from|college)", t):
        print("   ...", re.sub(r"\s+"," ",t[max(0,m.start()-130):m.start()+110]))
