# -*- coding: utf-8 -*-
"""W20: let chapters flow instead of forcing one chapter per page.

The forced break left four pages in each deck holding 200 to 1,600 characters - a
chapter tail alone on a page. Chapters now run on, with a break kept before the
opening chapter and before the sources chapter.
"""
import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

h = pathlib.Path("head.txt")
s = h.read_text(encoding="utf-8")
before = s
s = s.replace("section + section\n    {page-break-before:always}", "section + section\n    {page-break-before:auto}")
s = s.replace("section + section {page-break-before:always}", "section + section {page-break-before:auto}")
if s == before:
    s = re.sub(r"section\s*\+\s*section\s*\{[^}]*page-break-before\s*:\s*always[^}]*\}",
               "section + section { page-break-before: auto } section.newpage { page-break-before: always; break-before: page }", s)
    s = s.replace("</style>", "\nsection + section { page-break-before: auto }\nsection.newpage { page-break-before: always; break-before: page }\nh2 { break-after: avoid }\n</style>")
else:
    s = s.replace("</style>", "\nsection.newpage { page-break-before: always; break-before: page }\nh2 { break-after: avoid }\n</style>")
h.write_text(s, encoding="utf-8")
print("head.txt: forced break released:", "page-break-before:auto" in s or "page-break-before: auto" in s)

for gen in ("wbb-plain.py", "fb-plain.py"):
    p = pathlib.Path(gen); t = p.read_text(encoding="utf-8")
    m = re.search(r'<section>\s*<div class="pagehead">(.{0,400}?1\. Read this first)', t, re.S)
    if not m:
        print(gen, "MISSING chapter 1 anchor"); continue
    t = t[:m.start()] + '<section class="newpage">' + t[m.end() - len("1. Read this first"):]
    p.write_text(t, encoding="utf-8")
    print(gen, "chapter 1 marked newpage")

for name in ("wbb-sources.html", "fb-sources.html"):
    p = pathlib.Path(name); t = p.read_text(encoding="utf-8")
    t = t.replace("<section>", '<section class="newpage">', 1)
    p.write_text(t, encoding="utf-8")
    print(name, "sources chapter marked newpage")
