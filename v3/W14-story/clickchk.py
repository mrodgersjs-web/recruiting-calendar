import pathlib,sys,re
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
t=pathlib.Path("site/assets/ring.js").read_text(encoding="utf-8")
i=t.find("closest('.card')")
if i<0:
    i=t.find(".sr__next")
print(re.sub(r"\s+"," ",t[i-260:i+700]))
