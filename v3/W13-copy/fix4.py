#!/usr/bin/env python3
"""W13-copy: last small wording fixes the name swap left behind."""
import pathlib, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
PAIRS = [
    ("a preferred walk-on spot at dream school", "a preferred walk-on spot at his dream school"),
    ("offered aid (scholarship) while", "offered a scholarship, while"),
    ("offered aid (scholarship) but", "offered a scholarship, but"),
]
n = 0
for p in list(pathlib.Path("site").rglob("*.html")) + [pathlib.Path("site/assets/stories.js")]:
    if not p.is_file():
        continue
    t = p.read_text(encoding="utf-8", errors="ignore")
    o = t
    for a, b in PAIRS:
        t = t.replace(a, b)
    if t != o:
        p.write_text(t, encoding="utf-8")
        n += 1
print("copy touch-ups:", n)
