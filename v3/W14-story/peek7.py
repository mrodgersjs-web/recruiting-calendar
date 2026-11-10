import re,pathlib,sys
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
pats=["Read the story","click to read","Story '+'",'"Story "','story-deck','dk-read']
for p in list(pathlib.Path("site").rglob("*.html"))+list(pathlib.Path("site/assets").rglob("*.js")):
    t=p.read_text(encoding="utf-8",errors="ignore")
    for pat in ["Read the story","click to read the story",'Story ','read the story']:
        for m in re.finditer(re.escape(pat),t):
            ctx=re.sub(r"\s+"," ",t[max(0,m.start()-90):m.start()+110])
            print(f"{str(p):40} {pat:24} {ctx[:180]}")
