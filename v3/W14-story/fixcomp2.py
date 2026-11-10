"""Only delete a person-named asset once nothing left on the site points at it."""
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = pathlib.Path(__file__).resolve().parents[2] / "v3" / "W14-story" / "composite.py"
t = p.read_text(encoding="utf-8")

old = """media_deleted = []
for a in REAL:
    media_deleted += sorted(owned_media(a))
for name in sorted(set(media_deleted)):
    f = SITE / "assets" / "media" / name
    if f.exists() and not DRY:
        f.unlink()
print("assets named after a real person removed:", len(set(media_deleted)))
for name in sorted(set(media_deleted))[:6]:
    print("   e.g.", name)"""
new = """person_assets = set()
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
        print("   deleted e.g.", name)"""

assert old in t, "media block not found"
t = t.replace(old, new)
# `gone` must be populated before the media step
assert t.index("gone.append") < t.index("person_assets = set()"), "ordering wrong"
p.write_text(t, encoding="utf-8")
import ast
ast.parse(t)
print("patched, parses OK")
