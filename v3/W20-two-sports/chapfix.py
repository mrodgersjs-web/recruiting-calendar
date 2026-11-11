import pathlib, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = pathlib.Path("head.txt"); t = p.read_text(encoding="utf-8")
if "W21b: one chapter, one fresh page" not in t:
    css = """
/* W21b: one chapter, one fresh page, like the men's book */
section + section { break-before: page; page-break-before: always }
"""
    t = t.replace("</style>", css + "</style>")
    p.write_text(t, encoding="utf-8"); print("added")
else:
    print("already")
