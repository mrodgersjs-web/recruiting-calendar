import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
bad = ["Pewaukee","Badger","Camp Road","FootballScoop","Next Football","Milwaukee"," Rise","Pump","EYBL","adidas","Nike","TheGoto","Goto","Bellamy","(414)","Geneva","whitfield","Weber","weber","Powers"]
for f in ("W20-two-sports/fb-plain.py","W20-two-sports/wbb-plain.py","W19-plain/bball-plain.py"):
    t = pathlib.Path(f).read_text(encoding="utf-8")
    print("### " + f)
    for b in bad:
        for m in re.finditer(re.escape(b), t):
            s = re.sub(r"\s+"," ", t[max(0,m.start()-70):m.end()+70])
            print("   " + b + " ->  ..." + s + "...")
