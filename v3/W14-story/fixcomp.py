"""composite.py fixes: match assets by exact name parts, order the source lists."""
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = pathlib.Path(__file__).resolve().parents[2] / "v3" / "W14-story" / "composite.py"
t = p.read_text(encoding="utf-8")

pairs = [
    # 1. glob "*ali*" matched half the media folder. Use the paths the entry
    #    declares, then a delimiter-bounded filename match.
    ("""media_deleted = 0
for a in REAL:
    for sub in (SITE / "assets" / "media").glob(f"*{a['id']}*"):
        media_deleted += 1
        if not DRY:
            sub.unlink()
print("assets named after a real person removed:", media_deleted)""",
     """def owned_media(entry):
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


media_deleted = []
for a in REAL:
    media_deleted += sorted(owned_media(a))
for name in sorted(set(media_deleted)):
    f = SITE / "assets" / "media" / name
    if f.exists() and not DRY:
        f.unlink()
print("assets named after a real person removed:", len(set(media_deleted)))
for name in sorted(set(media_deleted))[:6]:
    print("   e.g.", name)"""),
    # 2. a 26-link reference block reads better grouped by sport
    ("""    seen, items = set(), []
    for url, sport, role in rows:
        if url in seen:
            continue
        seen.add(url)
        items.append(f'<li><a href="{url}" rel="noopener">{label_of(url)}</a> '
                     f"<span>{sport}: {role}.</span></li>")""",
     """    seen, items = set(), []
    for url, sport, role in sorted(rows, key=lambda r: (r[1], r[2], r[0])):
        if url in seen:
            continue
        seen.add(url)
        items.append(f'<li><a href="{url}" rel="noopener">{label_of(url)}</a> '
                     f"<span>{sport}: {role}.</span></li>")"""),
]
for old, new in pairs:
    if old not in t:
        print("MISS:", old[:60].replace("\n", " "))
        continue
    t = t.replace(old, new)
    print("ok  :", old[:56].replace("\n", " "))

p.write_text(t, encoding="utf-8")
import ast
ast.parse(t)
print("parses OK")
