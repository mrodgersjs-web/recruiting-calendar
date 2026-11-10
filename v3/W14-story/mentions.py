"""Every visible mention of a real first name, in context, so the rewording can be read."""
import html
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = pathlib.Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
NAMES = ["Hunter", "Sara", "Karsta", "Olivia", "Derrick", "Samantha", "Ali", "Annie",
         "Tori", "Cedric", "Cristelle", "Jimmy", "Chris", "Maya"]

for p in sorted(SITE.rglob("*.html")):
    raw = p.read_text(encoding="utf-8", errors="ignore")
    body = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", raw, flags=re.S | re.I)
    text = html.unescape(re.sub(r"<[^>]+>", " ", body))
    text = re.sub(r"\s+", " ", text)
    hits = []
    for n in NAMES:
        for m in re.finditer(r"\b" + n + r"\b", text):
            hits.append((n, text[max(0, m.start() - 110):m.start() + 130]))
    if hits:
        print(f"\n### {p.relative_to(SITE)}")
        for n, ctx in hits:
            print(f"   [{n}] …{ctx.strip()}…")
