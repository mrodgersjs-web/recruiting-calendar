import re,pathlib,sys
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
t=pathlib.Path("site/assets/deck.js").read_text(encoding="utf-8")
i=t.find("addEventListener('click'")
print(re.sub(r"\s+"," ",t[i:i+420]))
