"""W15 verifier: the athlete surface must be a first name and a sport, with no school talk."""
import html
import json
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = pathlib.Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
SCHOOL = re.compile(r"(?i)(?:\ba (?:suburban|public|large|private|mid-size)[^.;]{0,28}high school"
                    r"|\bhigh school\)? \u2192|\brarr; a? ?(?:power|division|d[123]|naia|junior|d1)"
                    r"|junior college|\bjuco\b|division\s+[id]\b|\bd[123]\b"
                    r"|illustration \u00b7 composite|real athlete|in this story|stories that use it"
                    r"|\bfrom a (?:club|public|two-sport)[^.;]{0,24}school)")

surface = [SITE / "index.html", SITE / "sports" / "index.html", SITE / "emerging-sports" / "index.html"]
surface += sorted((SITE / "sports").glob("*/index.html"))
bad = []
for p in surface:
    t = p.read_text(encoding="utf-8", errors="ignore")
    body = re.sub(r"(?is)<(script|style|svg)[^>]*>.*?</\1>", " ", t)
    txt = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", body)))
    for m in SCHOOL.finditer(txt):
        bad.append((str(p.relative_to(SITE)), m.group(0), txt[max(0, m.start()-60):m.start()+70].strip()))
print(f"school words in visible text on the athlete surface: {len(bad)}")
for page, term, ctx in bad[:12]:
    print(f"   {page:36} [{term}] ...{ctx}...")

raw = (SITE / "assets" / "stories.js").read_text(encoding="utf-8")
doc = json.JSONDecoder().raw_decode(raw[raw.index("{"):])[0]
BANNED = {"from", "college", "school", "div", "timeline", "turning", "basis", "rule",
          "replicate", "beats", "path", "video", "blurb"}
leaks = {}
for a in doc["athletes"]:
    extra = BANNED & set(a)
    if extra:
        leaks[a["id"]] = sorted(extra)
    if not (a["name"] == a["short"] == a["label"]):
        leaks.setdefault(a["id"], []).append("name/short/label differ")
    if not re.fullmatch(r"[A-Z][a-z]+", str(a["name"])):
        leaks.setdefault(a["id"], []).append(f"name not a bare first name: {a['name']!r}")
    if not a.get("sport"):
        leaks.setdefault(a["id"], []).append("no sport")
print(f"\nathlete entries: {len(doc['athletes'])} | entries leaking story or school fields: {len(leaks)}")
for k, v in leaks.items():
    print("   ", k, v)
print("names on the tiles:", ", ".join(sorted({a["name"] for a in doc["athletes"]})))
print("sports on the tiles:", ", ".join(sorted({a["sport"] for a in doc["athletes"]})))

dead = {}
for p in sorted(SITE.rglob("*.html")):
    t = p.read_text(encoding="utf-8", errors="ignore")
    for m in re.finditer(r'href=?["\']?(/(?:story|athlete)/[\w-]+)', t):
        dead.setdefault(m.group(1).strip("\"'"), set()).add(str(p.relative_to(SITE)))
print(f"\nlinks to athlete pages anywhere on the site: {len(dead)}")

cfg = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))
missing = [r for r in cfg["redirects"]
           if r["destination"].startswith("/sports/")
           and not (SITE / r["destination"].strip("/" ) / "index.html").exists()]
print(f"redirects pointing at a sport page that does not exist: {len(missing)}")
print(f"pages on disk: {len(list(SITE.rglob('*.html')))} | redirects: {len(cfg['redirects'])}")
