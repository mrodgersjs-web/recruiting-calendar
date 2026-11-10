import pathlib,sys,re
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
rjs=pathlib.Path("site/assets/ring.js").read_text(encoding="utf-8")
i=rjs.find("data-go")
print("card label builder:", repr(rjs[max(0,i-260):i+160]))
print("has esc:", re.findall(r"(?:function|const|var)\s+esc[\s\S]{0,170}", rjs)[:1])
d=pathlib.Path("site/assets/deck.js").read_text(encoding="utf-8")
print("deck esc:", re.findall(r"function esc[\s\S]{0,140}", d)[:1])
