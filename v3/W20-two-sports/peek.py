# -*- coding: utf-8 -*-
import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
for name in ("wbb-text.txt", "fb-text.txt"):
    raw = pathlib.Path(name).read_text(encoding="utf-8")
    parts = re.split(r"===== PAGE (\d+) =====", raw)
    print("\n=== %s ===" % name)
    for i in range(1, len(parts) - 1, 2):
        body = re.sub(r"\s+", " ", parts[i + 1]).strip()
        head = body[:118]
        print("p%-3s %4d ch | %s" % (parts[i], len(body), head))
