"""Pre-deploy check: links that would round-trip a redirect, and readability of changed pages."""
import html
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = pathlib.Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
sys.path.insert(0, str(ROOT / "v3" / "W13-copy"))
from readability import flesch_ease  # noqa: E402

slashed = {}
for p in sorted(SITE.rglob("*.html")):
    t = p.read_text(encoding="utf-8", errors="ignore")
    for m in re.finditer(r'href="(/[^"]?[^/"]*/)"', t):
        slashed.setdefault(m.group(1), set()).add(str(p.relative_to(SITE)))
print(f"internal links with a trailing slash (each is a 308 round-trip): {len(slashed)}")
for u, srcs in sorted(slashed.items())[:10]:
    print(f"   {u:34} <- {len(srcs)} page(s), e.g. {sorted(srcs)[0]}")

worst = []
for p in sorted(SITE.rglob("*.html")):
    t = p.read_text(encoding="utf-8", errors="ignore")
    body = re.sub(r"<(script|style|svg|noscript)[^>]*>.*?</\1>", " ", t, flags=re.S | re.I)
    text = html.unescape(re.sub(r"<[^>]+>", ". ", body))
    text = re.sub(r"[|·…—-]+", ". ", text)
    text = re.sub(r"\s+", " ", text)
    m = re.search(r"<title>([^<]+)</title>", t)
    if m:
        worst.append((flesch_ease(text), m.group(1), str(p.relative_to(SITE))))
worst.sort()
print("\nhardest pages now:")
for fk, t, p in worst[:6]:
    print(f"   {fk:5.1f}  {t[:44]:46} {p}")
print(f"\npages over 12: {sum(1 for s, _, _ in worst if s > 12)} of {len(worst)}")
