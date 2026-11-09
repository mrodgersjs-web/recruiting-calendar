#!/usr/bin/env python3
"""W13-copy: undo the doubled words the school map produced, and check nothing else doubled."""
import pathlib, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
FIX = [
    ("an all-American mention at the JUCO level at a JUCO program, averaging", "an all-American mention at the JUCO level, averaging"),
    ("was an an all-American mention", "earned an all-American mention"),
    ("named to the the varsity roster roster, the first woman", "named to the varsity roster, the first woman"),
    ("Named to the varsity roster roster, first woman", "Named to the varsity roster, the first woman"),
    ("the varsity roster roster", "the varsity roster"),
    ("an an ", "an "),
    ("the the ", "the "),
    ("Per a D1 school, Jimmy earned an all-American mention at the JUCO level, averaging",
     "His own school lists Jimmy as an all-American mention at the JUCO level, averaging"),
]
roots = ["site", "v3/W9-experiences", "v3/W1-stories", "v3/W2-site", "v3/W2-seo",
         "v3/W2-scripts", "v3/W2-video", "v3/W4-composites", "v3/W3-factcheck"]
n = 0
for r in roots:
    for p in pathlib.Path(r).rglob("*"):
        if not (p.is_file() and p.suffix.lower() in {".html", ".js", ".json", ".md", ".py", ".csv"}):
            continue
        t = p.read_text(encoding="utf-8", errors="ignore")
        o = t
        for a, b in FIX:
            t = t.replace(a, b)
        if t != o:
            p.write_text(t, encoding="utf-8")
            n += 1
print("files with doubled words fixed:", n)
left = []
for p in pathlib.Path("site").rglob("*.html"):
    t = p.read_text(encoding="utf-8", errors="ignore")
    for m in re.finditer(r"\b(the|a|an|roster|of|to)\s+\1\b", t):
        left.append((str(p.relative_to("site")), m.group(0)))
print("doubled words left in deployed pages:", len(left), sorted(set(left))[:5])
