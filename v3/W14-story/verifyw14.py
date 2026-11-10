"""Post-composite verification: dead links, leaked names, reading level."""
import html
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = pathlib.Path(__file__).resolve().parents[2]
SITE = ROOT / "site"

# ---------------------------------------------------------------- 1. dead links
pages = list(SITE.rglob("*.html"))
print(f"pages on disk: {len(pages)}")
dead = {}
for p in pages:
    t = p.read_text(encoding="utf-8", errors="ignore")
    for href in re.findall(r'href="(/[^"#?]*)', t):
        target = href.rstrip("/") or "/"
        if target.startswith("//"):
            continue
        cand = [SITE / target.strip("/") / "index.html", SITE / (target.strip("/") + ".html")]
        if not any(c.exists() for c in cand):
            dead.setdefault(href, set()).add(str(p.relative_to(SITE)))

print(f"\nbroken internal links: {len(dead)} distinct targets")
for href, srcs in sorted(dead.items())[:20]:
    print(f"   {href:44} <- {len(srcs)} page(s), e.g. {sorted(srcs)[0]}")

# ------------------------------------------------------------- 2. name leakage
map_txt = (ROOT / "v3" / "W13-copy" / "NAME-MAP.local.md").read_text(encoding="utf-8")
surnames, schools = set(), set()
for line in map_txt.splitlines():
    m = re.match(r"\|\s*([A-Z][\w'’-]+)\s+([A-Z][\w'’-]+)\s*\|", line)
    if m:
        surnames.add(m.group(2))
    for s in re.findall(r"\b(Clemson|Minnesota|Drake|Northwestern|Syracuse|Oregon|Iowa|Gonzaga|"
                        r"Belmont|Wichita|Pewaukee|UCLA|Stanford|Duke|Kentucky|Kansas)\b", line):
        schools.add(s)
terms = {s for s in surnames if s.lower() not in ("from", "and", "the")} | schools
print(f"\nwatching {len(terms)} real surnames/schools from the local name map")

visible_hits, href_hits = {}, {}
for p in pages:
    raw = p.read_text(encoding="utf-8", errors="ignore")
    body = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", raw, flags=re.S | re.I)
    text = html.unescape(re.sub(r"<[^>]+>", " ", body))
    for term in terms:
        if re.search(r"\b" + re.escape(term) + r"\b", text):
            visible_hits.setdefault(term, set()).add(str(p.relative_to(SITE)))
        for m in re.finditer(r'href="([^"]*?' + re.escape(term) + r'[^"]*)"', raw):
            href_hits.setdefault(term, set()).add(m.group(1)[:70])

print("VISIBLE name leaks:", "none" if not visible_hits else "")
for term, srcs in sorted(visible_hits.items()):
    print(f"   {term:14} {len(srcs)} page(s): {sorted(srcs)[:3]}")
print(f"\nnames inside citation hrefs (deliberate): {len(href_hits)} terms")
for term, urls in sorted(href_hits.items()):
    print(f"   {term:14} {sorted(urls)[0]}")
