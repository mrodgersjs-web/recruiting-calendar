# -*- coding: utf-8 -*-
"""W20: let chapters flow instead of forcing one chapter per page.

The forced break left pages holding 235 to 1,600 characters: a chapter tail alone
on a page. Chapters now run on, with a real break kept before the opening chapter
and before the sources chapter.
"""
import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

h = pathlib.Path("head.txt")
s = h.read_text(encoding="utf-8")
s2 = re.sub(r"section[ ]*[+][ ]*section[ ]*\{[^}]*page-break-before[ ]*:[ ]*always[^}]*\}",
            "section + section { page-break-before: auto }", s)
print("head.css changed:", s2 != s)
s2 = s2.replace("</style>", "\nsection.newpage { page-break-before: always; break-before: page }\n</style>")
h.write_text(s2, encoding="utf-8")

def mark(gen, anchor):
    p = pathlib.Path(gen); t = p.read_text(encoding="utf-8")
    i = t.find(anchor)
    if i < 0:
        print(gen, "MISSING anchor", anchor); return
    j = t.rfind("<section>", 0, i)
    if j < 0:
        print(gen, "no section tag before anchor"); return
    t = t[:j] + '<section class="newpage">' + t[j + len("<section>"):]
    p.write_text(t, encoding="utf-8")
    print(gen, "marked newpage before", repr(anchor))

for gen in ("wbb-plain.py", "fb-plain.py"):
    mark(gen, "1. Read this first")
for name in ("wbb-sources.html", "fb-sources.html"):
    p = pathlib.Path(name); t = p.read_text(encoding="utf-8")
    t = t.replace("<section>", '<section class="newpage">', 1)
    p.write_text(t, encoding="utf-8")
    print(name, "sources chapter marked newpage")
