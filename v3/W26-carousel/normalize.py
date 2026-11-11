# -*- coding: utf-8 -*-
"""W26b cleanup: drop the sentence that named the deleted wrestling athlete, put line endings back
the way they were, and recompute the cache keys so they match the bytes on disk."""
import hashlib
import pathlib
import re

SITE = pathlib.Path(__file__).resolve().parents[2] / "site"

EG = SITE / "emerging-sports/data.json"
t = EG.read_text(encoding="utf-8")
old = " Cristelle became an NAIA program's first NAIA champion in 2024."
if old not in t:
    raise SystemExit("FAIL: the Cristelle sentence moved or is already gone")
EG.write_bytes(t.replace(old, "", 1).encode("utf-8"))
print("dropped the sentence that named the deleted wrestling athlete")

for f in ("assets/ring.js", "index.html", "segments/segments.json", "emerging-sports/data.json",
          "IMAGES.json", "assets/stories.js"):
    p = SITE / f
    b = p.read_bytes()
    if b"\r\n" in b:
        p.write_bytes(b.replace(b"\r\n", b"\n"))
        print("  normalized %s to LF" % f)

h = (SITE / "index.html").read_text(encoding="utf-8")
for url in ["/checkout.js", "/assets/commit.css", "/assets/ring.css", "/assets/deck.css",
            "/assets/stories.js", "/assets/ring.js", "/assets/deck.js"]:
    path = SITE / url.lstrip("/").replace("/", "\\")
    key = hashlib.md5(path.read_bytes()).hexdigest()[:8]
    new = re.sub(re.escape(url) + r"\?v=[0-9a-f]{8}", url + "?v=" + key, h, count=1)
    if new != h:
        print("  cache key %s -> %s" % (url, key))
    h = new
(SITE / "index.html").write_bytes(h.encode("utf-8"))
print("cache keys match the bytes on disk")
