"""Re-point the ?v= cache-busters for assets edited by hand.

build_site.py stamps ?v=md5[:8] (deck's is md5 of deck.js+deck.css). Hand edits to
those files therefore served stale JS to any browser that had already visited.
This recomputes the hashes and rewrites each tag's own version, per asset.
"""
import hashlib
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = pathlib.Path(__file__).resolve().parents[2]
SITE = ROOT / "site"


def digest(*files):
    h = hashlib.md5()
    for f in files:
        h.update((SITE / f).read_bytes())
    return h.hexdigest()[:8]


NEW = {
    "assets/stories.js": digest("assets/stories.js"),
    "assets/ring.js": digest("assets/ring.js"),
    "assets/deck.js": digest("assets/deck.js", "assets/deck.css"),
}
print("new versions:", {k.split("/")[-1]: v for k, v in NEW.items()})

TAG = re.compile(r'(<(?:script|link)[^>]*(?:src|href)=")(/assets/(?:stories|ring|deck)\.js)\?v=([0-9a-f]{6,12})("[^>]*>)')
touched = 0
changed = 0
for p in sorted(SITE.rglob("*.html")):
    t0 = t = p.read_text(encoding="utf-8")

    def fix(m):
        global changed
        want = NEW[m.group(2).lstrip("/")]
        if m.group(3) == want:
            return m.group(0)
        changed += 1
        return m.group(1) + m.group(2) + "?v=" + want + m.group(4)

    t = TAG.sub(fix, t)
    if t != t0:
        p.write_text(t, encoding="utf-8")
        touched += 1
print(f"tags rewritten: {changed} across {touched} pages")

leftover = set()
for p in SITE.rglob("*.html"):
    for m in re.finditer(r'/assets/(stories|ring|deck)\.js\?v=([0-9a-f]{6,12})', p.read_text(encoding="utf-8")):
        key = "assets/" + m.group(1) + ".js"
        if m.group(2) != NEW[key]:
            leftover.add((key, m.group(2), str(p.relative_to(SITE))))
print("stale tags left:", len(leftover))
for row in sorted(leftover)[:5]:
    print("   ", row)
