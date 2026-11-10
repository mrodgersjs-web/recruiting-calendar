import pathlib,sys,re,html
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
for f in ["site/assets/ring.js","site/assets/deck.js","site/assets/stories.js"]:
    t=pathlib.Path(f).read_text(encoding="utf-8")
    hits=sorted({m.group(0) for m in re.finditer(r"(?i)high school|junior college|\bjuco\b|division|real athlete|composite\b|from\"|college\"",t)})
    print(f, "->", hits[:8])
