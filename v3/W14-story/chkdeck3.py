import pathlib,sys
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
t=pathlib.Path("site/assets/deck.js").read_text(encoding="utf-8")
i=0
while True:
    i=t.find("/playbooks/",i+1)
    if i<0: break
    print("...",repr(t[i-70:i+90]))
