# -*- coding: utf-8 -*-
"""How big is each block? Used to decide which ones are allowed to break across a
page and which must stay whole."""
import re, sys, html, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SRC = sys.argv[1]
raw = pathlib.Path(SRC).read_text(encoding="utf-8")

items = []
for m in re.finditer(r'<div class="(?:box|tmpl)[^"]*">(.*?)\n\s*</div>', raw, re.S):
    items.append(("box", m.start(), m.group(1)))
for m in re.finditer(r"<(table|ul|ol|p|div)([^>]*)>(.*?)</\1>", raw, re.S):
    tag, attrs, body = m.group(1), m.group(2), m.group(3)
    if tag == "p" and "lead" not in attrs:
        continue
    if tag == "div" and "two" not in attrs:
        continue
    items.append((tag, m.start(), body))

for kind, pos, frag in sorted(items, key=lambda x: x[1]):
    words = len(re.findall(r"\w+", html.unescape(re.sub(r"<[^>]+>", " ", frag))))
    head = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", frag))).strip()[:52]
    print("%-6s %5d chars %4d words | %s" % (kind, len(re.sub(r"<[^>]+>", " ", frag)), words, head))
