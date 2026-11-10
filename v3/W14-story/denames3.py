"""Final name pass. Apostrophes on these pages are typographic (U+2019), which the
earlier rules did not match. 'Derrick Rock' is a place name invented in W13, not a person."""
import html
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = pathlib.Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
A = r"['\u2019]"

SUBS = [
    (rf"what Derrick{A}s family did in basketball", "what a basketball family in the same spot did"),
    (rf"Like Derrick{A}s family in basketball, ", "Like a family in the same spot, "),
    (r"\(Derrick: (https://[^)]+)\)", r"(\1)"),
    (r"\(Kendall Sara, Minnesota\)", "(public reporting)"),
]

files = 0
for f in sorted(list(SITE.rglob("*.html")) + list(SITE.rglob("*.js"))):
    t0 = t = f.read_text(encoding="utf-8", errors="ignore")
    for pat, rep in SUBS:
        t = re.sub(pat, rep, t)
    if t != t0:
        f.write_text(t, encoding="utf-8")
        files += 1
print("files edited:", files)

PLACE = {"Derrick Rock"}  # invented place name from the W13 anonymization
NAMES = ["Hunter", "Sara", "Karsta", "Olivia", "Derrick", "Samantha", "Ali", "Annie",
         "Tori", "Cedric", "Cristelle", "Jimmy", "Chris", "Maya"]
left = []
for p in sorted(SITE.rglob("*.html")):
    body = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", re.sub(
        r"<(script|style|svg)[^>]*>.*?</\1>", " ",
        p.read_text(encoding="utf-8", errors="ignore"), flags=re.S | re.I))))
    for n in NAMES:
        for m in re.finditer(r"\b" + n + r"\b", body):
            window = body[m.start():m.start() + 12]
            if any(window.startswith(pl) for pl in PLACE):
                continue
            left.append((str(p.relative_to(SITE)), n, body[max(0, m.start()-60):m.start()+80]))
print(f"real first names still visible: {len(left)}")
for page, n, ctx in left[:8]:
    print(f"   {page}\n      [{n}] ...{ctx.strip()}...")

dead = {}
for p in sorted(SITE.rglob("*.html")):
    t = p.read_text(encoding="utf-8", errors="ignore")
    for m in re.finditer(r'href=?["\']?(/(?:story|athlete)/[\w-]+)', t):
        u = m.group(1).strip("\"'")
        if not (SITE / u.strip("/") / "index.html").exists():
            dead.setdefault(u, set()).add(str(p.relative_to(SITE)))
print(f"links to deleted bios: {len(dead)}")
