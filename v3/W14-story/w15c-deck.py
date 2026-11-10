"""W15c: the deck's strings escape their quotes, so match that."""
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
SITE = pathlib.Path(__file__).resolve().parents[2] / "site"

dk = SITE / "assets" / "deck.js"
t = dk.read_text(encoding="utf-8")
t, n_route = re.subn(r"\\'</h2><p class=\"dk-route\">\\'\+esc\(a\.from\)\+' <span>\u2192</span> \\'"
                     r"\+esc\(a\.college\)\+\\'</p>\+'", "</h2>\\'+", t)
t, n_real = re.subn(r"\+\s*'<section class=\"dk-real\">.*?</section>'(?=;)", "", t, flags=re.S)
t, n_cmt = re.subn(r"/\* Phone story deck[^\n]*\n(?:[^\n]*\n){0,2}",
                   "/* Phone deck (<=749px): one illustration card per sport, swipe snaps card to card.\n"
                   "   Desktop keeps <story-ring>. Names are placeholders; no real person is shown. */\n", t)
dk.write_text(t, encoding="utf-8")
print(f"deck: route {n_route}, real-athlete section {n_real}, comment {n_cmt}")

rk = SITE / "assets" / "ring.js"
r = rk.read_text(encoding="utf-8")
r, n_panel = re.subn(r"In this story", "Playbooks for this sport", r)
r, n_aria = re.subn(r"Athlete stories\. Use arrow keys or swipe\.", "Browse by sport. Use arrow keys or swipe.", r)
rk.write_text(r, encoding="utf-8")
print(f"ring: panel label {n_panel}, region aria-label {n_aria}")
for f in ("deck.js", "ring.js"):
    txt = (SITE / "assets" / f).read_text(encoding="utf-8")
    words = sorted({m.group(0) for m in re.finditer(
        r"(?i)(stor(?:y|ies)|real athlete[s]?|high school|junior college|juco|division[s]?)", txt)})
    print(f"{f}: story/school words -> {words}")
    print(f"   field refs: {sorted({m.group(0) for m in re.finditer(r'a[.](div|from|college)', txt)})}")
    print(f"   parses: {'yes' if txt.count('{') == txt.count('}') else 'brace mismatch'}")
