import pathlib,sys,re
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
for f in ["site/assets/ring.js","site/assets/deck.js"]:
    t=pathlib.Path(f).read_text(encoding="utf-8")
    print(f, "->", sorted({m.group(0) for m in re.finditer(r"a\.(div|from|college|short|sport|img|composite|art_fictional|name|playbooks|hold)", t)}))
    print("   Illustration · Composite still present:", "Illustration \u00b7 Composite" in t, "| dk-div:", "dk-div" in t, "| dk-route:", "dk-route" in t)
