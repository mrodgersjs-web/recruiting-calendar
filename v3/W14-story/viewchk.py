import pathlib,sys,re
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
t=pathlib.Path("site/assets/ring.js").read_text(encoding="utf-8")
for m in re.finditer(r"data-view", t):
    print(repr(re.sub(r"\s+"," ",t[max(0,m.start()-200):m.start()+220])))
    print("---")
