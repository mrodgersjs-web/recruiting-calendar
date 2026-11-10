import pathlib,sys,re
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
t=pathlib.Path("site/assets/ring.js").read_text(encoding="utf-8")
for key in ["STORY_ALL","athletes","filter(","hold","connectedCallback","SPORT_PATH(","page"]:
    for m in list(re.finditer(re.escape(key), t))[:3]:
        print(key, "->", re.sub(r"\s+"," ",t[max(0,m.start()-90):m.start()+130]))
        print("  --")
