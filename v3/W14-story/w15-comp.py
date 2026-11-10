import pathlib,sys,re
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
for f in ["site/assets/ring.js","site/assets/deck.js"]:
    t=pathlib.Path(f).read_text(encoding="utf-8")
    print("###",f)
    for m in re.finditer(r"(?i)composite", t):
        print("   ...", re.sub(r"\s+"," ",t[max(0,m.start()-70):m.start()+60]))
