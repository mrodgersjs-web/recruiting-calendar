#!/usr/bin/env python3
"""
W14b: composite only. Mike's call on 2026-11-09.

The 13 biographies of real athletes come down. Their sourcing does not: every
citation moves onto the playbook pages that the path was used to sell, where a
named source backing a factual claim is at its strongest and the site is not
borrowing a face to open a wallet. The ring keeps 21 tiles; all 21 are composites.

Order matters. Read the pages, write the sources, recast the data, then delete.

Run:  python v3/W14-story/composite.py [--dry]
"""
import json
import pathlib
import re
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = pathlib.Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
DRY = "--dry" in sys.argv

JS_PATH = SITE / "assets" / "stories.js"
js = JS_PATH.read_text(encoding="utf-8")
pre, rest = js.split("=", 1)
payload = json.JSONDecoder().raw_decode(rest.strip().lstrip("=").strip()[rest.strip().lstrip("=").strip().index("{"):])[0]
END_GLOBAL = rest.index("\nwindow.STORY_DATA") if "\nwindow.STORY_DATA" in rest else len(rest)
after = rest[END_GLOBAL:]

REAL = [a for a in payload["athletes"] if not a.get("composite")]
print(f"real bios to retire: {len(REAL)}")

ROLE = {  # the identifying feat goes; what a parent can copy stays
    "hunter": "the walk-on who never started",
    "sara": "the two-sport kid who picked one",
    "karsta": "the setter who transferred",
    "olivia": "the walk-on pitcher",
    "derrick": "the D2 starter who went D1",
    "samantha": "the guard who redshirted",
    "ali": "the lineman who picked his school",
    "annie": "the distance runner who improved late",
    "tori": "the goalie who started late",
    "cedric": "the D3 star who moved up",
    "cristelle": "the wrestle-over",
    "jimmy": "the JUCO guard",
    "chris": "the club player who walked on",
}
SPORT_ART = {  # composite art is keyed by sport, not by person
    "Football": "cut-football-640.webp", "Baseball": "cut-baseball-640.webp",
    "Softball": "cut-softball-640.webp", "Volleyball": "cut-volleyball-640.webp",
    "Basketball": "cut-wbasketball-640.webp", "Wrestling": "cut-wrestling-640.webp",
    "Swimming": "cut-swimmer-640.webp", "Track & Field": "cut-sprinter-640.webp",
    "Track/XC": "cut-sprinter-640.webp", "Soccer": "cut-sprinter-640.webp",
    "Lacrosse (goalie)": "cut-wrestling-640.webp",
}
NO_STATE = re.compile(r"\s*(in|at)\s+(South Carolina|New York|California|Texas|Ohio|Illinois|Florida|"
                      r"Georgia|Michigan|Pennsylvania|Wisconsin|Colorado|Minnesota|Washington|"
                      r"North Carolina|Virginia|Arizona|Indiana|Iowa|Kansas|Louisiana|Missouri|"
                      r"Tennessee|Kentucky|Alabama|Oklahoma|Nebraska|Oregon|Utah|Nevada|Arkansas)\b")


def sport_slug(sport):
    s = str(sport or "").lower()
    if "track" in s:
        return "track-field"
    if "swim" in s:
        return "swimming"
    if "lacrosse" in s:
        return "lacrosse"
    return re.split(r"[\s(/]+", s)[0]


def citations_of(entry_id):
    """External links actually cited on the bio page, in order, deduped."""
    urls = []
    for part in ("story", "athlete"):
        f = SITE / part / entry_id / "index.html"
        if not f.exists():
            continue
        t = f.read_text(encoding="utf-8")
        for m in re.finditer(r'<a[^>]+href="(https?://[^"]+)"', t):
            u = m.group(1).split("#")[0]
            if "recruiting-calendar.vercel.app" in u:
                continue
            if u not in urls:
                urls.append(u)
    return urls


def label_of(url):
    host = re.sub(r"^www\.", "", re.match(r"https?://([^/]+)", url).group(1))
    return {"si.com": "Sports Illustrated", "www.ncaa.com": "NCAA.com", "ncaa.com": "NCAA.com",
            "espn.com": "ESPN", "www.espn.com": "ESPN"}.get(host, host)


# ------------------------------------------------- 1. sources land on playbooks
by_playbook = {}
for a in REAL:
    role = ROLE.get(a["id"], "a real recruiting path")
    for url in citations_of(a["id"]):
        for pb in a.get("playbooks") or []:
            by_playbook.setdefault(pb, []).append((url, a["sport"], role))

moved = 0
for pb, rows in sorted(by_playbook.items()):
    f = SITE / "playbooks" / pb / "index.html"
    if not f.exists():
        print(f"   skip (no page): {pb}")
        continue
    t = f.read_text(encoding="utf-8")
    seen, items = set(), []
    for url, sport, role in sorted(rows, key=lambda r: (r[1], r[2], r[0])):
        if url in seen:
            continue
        seen.add(url)
        items.append(f'<li><a href="{url}" rel="noopener">{label_of(url)}</a> '
                     f"<span>{sport}: {role}.</span></li>")
    if not items:
        continue
    block = ('<section class="src-list" id="sources"><h2>Where these paths come from</h2>'
             '<p class="note">Public reporting behind the examples on this page. Sources are cited to '
             "back a rule or a step, not to imply that any athlete or school endorses this site.</p>"
             f"<ul>{''.join(items)}</ul></section>")
    if 'id="sources"' in t:
        t = re.sub(r'<section class="src-list" id="sources">.*?</section>', block, t, count=1, flags=re.S)
    else:
        i = t.rfind("</main>")
        t = t[:i] + block + t[i:]
    if not DRY:
        f.write_text(t, encoding="utf-8")
    moved += len(items)
    print(f"   /playbooks/{pb}/ <- {len(items)} sources")
print(f"sources moved: {moved}")

# ------------------------------------------------------- 2. recast the entries
def generic(text):
    text = NO_STATE.sub("", str(text or ""))
    return text.strip(" ,.")


for a in REAL:
    role = ROLE.get(a["id"], "a real recruiting path")
    urls = citations_of(a["id"])
    n = max(len(urls), 1)
    a["composite"] = True
    a["art_fictional"] = True
    a["name"] = f'Composite: "{role}" ({str(a["sport"]).split(" (")[0].lower()})'
    a["short"] = f"{role} (composite)"
    a["label"] = f"Composite story built from {n} sourced recruiting paths"
    a["from"] = generic(a.get("from")) or "Public high school"
    a["school"] = generic(a.get("school"))
    a["basis"] = urls
    a["beats"] = [f'This is a composite. It stands for a real, publicly reported path on this '
                 f"sport's page, shortened to what a parent can copy, with no name, no school and no "
                 f"photo. Sources are listed on the playbooks that sell this path."]
    a["timeline"] = []
    a["turning"] = []
    a["img"] = f'/assets/media/{SPORT_ART.get(a["sport"], "cut-sprinter-640.webp")}?v=11071350'
    a["poster"] = ""
    a["video"] = ""
    a["page"] = False

if not DRY:
    JS_PATH.write_text(pre + "=" + json.dumps(payload, ensure_ascii=False) + after, encoding="utf-8")
print("entries recast:", len(REAL), "| remaining real:",
      sum(1 for a in payload["athletes"] if not a.get("composite")))

# ------------------------------------------------------------- 3. pages go away
gone = []
for a in REAL:
    for part in ("story", "athlete"):
        d = SITE / part / a["id"]
        if d.exists():
            gone.append((part, a["id"], sport_slug(a["sport"])))
            if not DRY:
                shutil.rmtree(d)
print("page directories deleted:", len(gone))

def owned_media(entry):
    out = set()
    for key in ("img", "poster", "video"):
        v = str(entry.get(key) or "")
        if v:
            out.add(v.split("?")[0].split("/")[-1])
    # cut-<id>-640.webp and real-<id>-poster.jpg, but not every file containing "ali"
    pat = re.compile(r"(^|[-_.])" + re.escape(entry["id"]) + r"([-_.]|$)")
    for f in (SITE / "assets" / "media").iterdir():
        if pat.search(f.name):
            out.add(f.name)
    return out


person_assets = set()
for a in REAL:
    person_assets |= owned_media(a)

# what still points at them, ignoring the pages we are about to delete
doomed = {str((SITE / part / pid)) for part, pid, _slug in gone}
still_used = set()
for f in list(SITE.rglob("*.html")) + list((SITE / "assets").rglob("*.js")) + list(SITE.rglob("*.css")):
    if any(str(f).startswith(d) for d in doomed):
        continue
    body = f.read_text(encoding="utf-8", errors="ignore")
    for name in person_assets:
        if name in body:
            still_used.add(name)

media_deleted = sorted(person_assets - still_used)
for name in media_deleted:
    f = SITE / "assets" / "media" / name
    if f.exists() and not DRY:
        f.unlink()
print(f"person-named assets: {len(person_assets)} found, {len(still_used)} still referenced elsewhere, "
      f"{len(media_deleted)} deleted")
for name in list(still_used)[:5]:
    print("   kept, referenced:", name)
if not DRY and media_deleted:
    for name in media_deleted[:4]:
        print("   deleted e.g.", name)

# --------------------------------------------------------- 4. vercel.json 301s
vj_path = ROOT / "vercel.json"
vj = json.loads(vj_path.read_text(encoding="utf-8"))
redirects = vj.get("redirects", [])
dest = {f"/{part}/{pid}": f"/sports/{slug}" for part, pid, slug in gone}
changed = 0
for r in redirects:
    tgt = r["destination"].rstrip("/")
    if tgt in dest:  # the W13 surname redirects now aim at a deleted page
        r["destination"] = dest[tgt]
        r["permanent"] = True
        changed += 1
for part, pid, slug in gone:
    for prefix in (f"/{part}/{pid}", f"/{part}/{pid}/"):
        if not any(r.get("source").rstrip("/") == f"/{part}/{pid}" for r in redirects):
            redirects.append({"source": prefix, "destination": f"/sports/{slug}", "permanent": True})
vj["redirects"] = redirects
if not DRY:
    vj_path.write_text(json.dumps(vj, indent=2) + "\n", encoding="utf-8")
print(f"redirects: {changed} repointed, total {len(redirects)}")

if DRY:
    print("\n(dry run: nothing written)")
