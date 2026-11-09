#!/usr/bin/env python3
"""W13-copy: rebuild site/sitemap.xml from the pages that actually exist.

The shipped sitemap listed 13 story URLs under /stories/, a prefix that was
never deployed, and it left out 8 story pages that were deployed. Deriving the
file from the tree fixes both and keeps it honest after the slug changes.
Run: python v3/W13-copy/sitemap.py
"""
import datetime, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
BASE = "https://recruiting-calendar.vercel.app"
SKIP = {"welcome"}          # disallowed in robots.txt
NOW = datetime.date.today().isoformat()
DRY = "--dry" in sys.argv

urls = []
for p in sorted(SITE.rglob("index.html")):
    rel = p.parent.relative_to(SITE).as_posix()
    if any(part in SKIP for part in rel.split("/")[:1]):
        continue
    urls.append(BASE + ("/" if not rel else "/" + rel + "/"))

out = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in urls:
    out.append(f"  <url><loc>{u}</loc><lastmod>{NOW}</lastmod></url>")
out.append("</urlset>\n")
text = "\n".join(out)

old = (SITE / "sitemap.xml")
had = old.read_text(encoding="utf-8") if old.exists() else ""
old_locs = re.findall(r"<loc>(.*?)</loc>", had)
missing_before = [u for u in urls if u not in old_locs]
dead_before = [u for u in old_locs if u not in urls]
print(f"urls after rebuild: {len(urls)}")
print(f"previously missing from the sitemap: {len(missing_before)}")
for u in missing_before[:12]:
    print("   +", u)
print(f"in the old sitemap but not deployed: {len(dead_before)}")
for u in dead_before[:6]:
    print("   -", u)
if not DRY:
    old.write_text(text, encoding="utf-8")
