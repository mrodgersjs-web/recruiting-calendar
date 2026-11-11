import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
for f in ("W20-two-sports/fb-plain.py","W20-two-sports/wbb-plain.py","W19-plain/bball-plain.py"):
    t = pathlib.Path(f).read_text(encoding="utf-8")
    print("\n############ " + f)
    for m in re.finditer(r'<div class="tmpl">(.*?)</div>', t, re.S):
        print("---- TMPL ----")
        print(m.group(1).strip())
