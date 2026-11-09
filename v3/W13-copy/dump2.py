#!/usr/bin/env python3
"""W13-copy: print the long sentences still holding a page's grade level up."""
import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
for f in sys.argv[1:]:
    t = pathlib.Path(f).read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"<main[^>]*>(.*?)</main>", t, re.S | re.I)
    body = m.group(1) if m else t
    body = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", body, flags=re.S | re.I)
    txt = re.sub(r"<[^>]+>", " ", body)
    txt = re.sub(r"&[a-z]+;", " ", txt)
    txt = re.sub(r"\s+", " ", txt).strip()
    sents = re.split(r"(?<=[.!?:])\s+", txt)
    print("=== " + f)
    for i, s in enumerate(sents):
        if len(s.split()) >= 17:
            print(f"  [{i}] ({len(s.split())}w) {s}")
