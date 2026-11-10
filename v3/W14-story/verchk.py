import pathlib,sys,re,hashlib
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
for s in ["v3/W14-story/composite.py","v3/W2-site/build_site.py"]:
    t=pathlib.Path(s).read_text(encoding="utf-8",errors="ignore")
    for m in re.finditer(r"(?:def ver|version|hashlib[^
]*|digest\(\)\[:\d+\])[\s\S]{0,120}", t):
        print(s, "->", re.sub(r"\s+"," ",m.group(0))[:150])
        print("---")
