# -*- coding: utf-8 -*-
"""Print the neighbourhood of each pattern in a deck generator, so manual
patches can be written against the real source text."""
import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

fn = sys.argv[1]
s = pathlib.Path(fn).read_text(encoding="utf-8")
for p in sys.argv[2:]:
    hits = list(re.finditer(re.escape(p), s))
    if not hits:
        print("MISS  %r" % p)
    for m in hits:
        print("HIT   %r :: %s" % (p, re.sub(r"\s+", " ", s[max(0, m.start() - 170):m.end() + 200])))
