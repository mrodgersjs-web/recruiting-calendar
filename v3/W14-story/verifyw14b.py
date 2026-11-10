"""Round two: only flag a target if no file exists at all, and match names case-insensitively."""
import html
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = pathlib.Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
pages = list(SITE.rglob("*.html"))

missing = {}
points_at_deleted = {}
for p in pages:
    t = p.read_text(encoding="utf-8", errors="ignore")
    for href in re.findall(r'href="(/[^"#?]*)', t):
        clean = href.split("?")[0].rstrip("/") or "index"
        base = SITE / clean.strip("/")
        ok = ((base.is_dir() and (base / "index.html").exists()) or base.exists()
              or (SITE / (clean.strip("/") + ".html")).exists()
              or (base.parent / (base.name + ".html")).exists())
        if not ok:
            missing.setdefault(href, set()).add(str(p.relative_to(SITE)))
        if re.match(r"/(story|athlete)/", href):
            parts = href.strip("/").split("/")
            tgt = SITE / parts[0] / parts[-1] / "index.html"
            if not tgt.exists():
                points_at_deleted.setdefault(href, set()).add(str(p.relative_to(SITE)))

print(f"missing files behind internal links: {len(missing)}")
for href, srcs in sorted(missing.items())[:12]:
    print(f"   {href:52} <- {sorted(srcs)[0]}")
print(f"\nlinks pointing at a deleted bio page: {len(points_at_deleted)}")
for href, srcs in sorted(points_at_deleted.items())[:12]:
    print(f"   {href:36} <- {len(srcs)} page(s): {sorted(srcs)[0]}")

map_txt = (ROOT / "v3" / "W13-copy" / "NAME-MAP.local.md").read_text(encoding="utf-8")
real_names = set()
for line in map_txt.splitlines():
    m = re.match(r"\|\s*((?:[A-Z][\w'’-]+\s+)+[A-Z][\w'’-]+)\s*\|", line)
    if m:
        real_names.update(w for w in m.group(1).split() if len(w) > 3)
    for s in re.findall(r"\b(Clemson|Minnesota|Drake|Northwestern|Syracuse|Oregon|Pewaukee|"
                        r"UCLA|Stanford|Duke|Kentucky|Gonzaga|Belmont|Marquette|Iowa)\b", line):
        real_names.add(s)
terms = sorted(real_names - {"from", "and", "the", "with"})

visible, hrefs = {}, {}
for p in pages:
    raw = p.read_text(encoding="utf-8", errors="ignore")
    body = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", raw, flags=re.S | re.I)
    text = html.unescape(re.sub(r"<[^>]+>", " ", body))
    for term in terms:
        pat = re.compile(r"\b" + re.escape(term) + r"\b", re.I)
        if pat.search(text):
            visible.setdefault(term, set()).add(str(p.relative_to(SITE)))
        for m in re.finditer(r'href="([^"]+)"', raw):
            if pat.search(m.group(1)):
                hrefs.setdefault(term, set()).add(m.group(1)[:78])

js = (SITE / "assets" / "stories.js").read_text(encoding="utf-8")
blob = {t: len(re.findall(r"\b" + re.escape(t) + r"\b", js, re.I))
        for t in terms if re.search(r"\b" + re.escape(t) + r"\b", js, re.I)}

print(f"\nVISIBLE text containing a real name or school: {len(visible)}")
for term, srcs in sorted(visible.items()):
    print(f"   {term:14} {len(srcs)} page(s): {sorted(srcs)[:2]}")
print(f"\nterms surviving inside citation hrefs (deliberate): {len(hrefs)}")
for term, urls in sorted(hrefs.items()):
    print(f"   {term:14} {sorted(urls)[0]}")
print(f"\nterms inside the story data file: {blob or 'none'}")
