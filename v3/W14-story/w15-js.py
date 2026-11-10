"""W15b: finish the JS templates with the real bytes, and list any story language left."""
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
SITE = pathlib.Path(__file__).resolve().parents[2] / "site"

# ---- deck.js ----
dk = SITE / "assets" / "deck.js"
t = dk.read_text(encoding="utf-8")
before = t

t, n1 = re.subn(r"</h2><p class=\"dk-route\">'\+esc\(a\.from\)\+' <span>\u2192</span> '\+esc\(a\.college\)\+'</p>\+'",
                "</h2>'+", t)
t, n2 = re.subn(r"\+ '<section class=\"dk-real\">.*?realLinks.*?</section>'(?=;)", "", t, flags=re.S)
t, n3 = re.subn(r"<p class=\"dk-pbl\">In this story</p>", "<p class=\"dk-pbl\">Playbooks for this sport</p>", t)
dk.write_text(t, encoding="utf-8")
print(f"deck: route removed {n1}, real-athlete section removed {n2}, panel label {n3}")

# ---- ring.js ----
rk = SITE / "assets" / "ring.js"
r = rk.read_text(encoding="utf-8")
r, m1 = re.subn(r"this\.querySelector\('\[data-who\]'\)\.textContent=[^;]+;",
                "this.querySelector('[data-who]').textContent=`${a.short} \u00b7 ${a.sport}"
                " \u00b7 Illustration. The name is a placeholder; the dates and rules are cited on the page that uses them.`;",
                r)
rk.write_text(r, encoding="utf-8")
print(f"ring: data-who line replaced {m1}")

# ---- what story language is still in the two scripts ----
for f in ("deck.js", "ring.js"):
    txt = (SITE / "assets" / f).read_text(encoding="utf-8")
    hits = sorted({m.group(0) for m in re.finditer(r"(?i)[\w ]{0,14}(stor(?:y|ies)|real athlete|high school|junior college|juco|division)[\w .,'\\${}()?!-]{0,24}", txt)})
    print(f"\n{f} story/school language ({len(hits)}):")
    for h in hits[:14]:
        print("   ", re.sub(r"\s+", " ", h).strip()[:96])
    print("   field refs:", sorted({m.group(0) for m in re.finditer(r"a\.(div|from|college)", txt)}))
