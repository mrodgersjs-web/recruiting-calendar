import pathlib,sys,re
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
t=pathlib.Path("site/assets/deck.js").read_text(encoding="utf-8")
i=t.find("var realLinks")
print(re.sub(r"\s+"," ",t[i:i+1200]))
