import pathlib,sys,re
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
for f in ["site/athlete/composite-swim/index.html","site/story/composite-swim/index.html"]:
    t=pathlib.Path(f).read_text(encoding="utf-8")
    for m in re.finditer("Derrick",t):
        print(f, "->", repr(t[max(0,m.start()-40):m.start()+70]))
