import pathlib, re, sys, ast
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = pathlib.Path("v3/W14-story/build_sports.py")
t = p.read_text(encoding="utf-8")
stray = "        m = re.search(r'href=\"?(.*?)\\s|>', body)\n"
if stray in t:
    t = t.replace(stray, "")
    p.write_text(t, encoding="utf-8")
    ast.parse(t)
    print("stray line removed")
else:
    print("no stray line (already clean?)")
    print([l for l in t.splitlines() if "href=" in l and "body" in l][:3])
