"""Second pass, from the real markup: <a href=/story/hunter>Hunter</a> . Football . D1

Bio links on these pages are unquoted, so the first checker never saw them.
A chip for a retired bio becomes plain text: the role, marked composite.
"""
import html
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = pathlib.Path(__file__).resolve().parents[2]
SITE = ROOT / "site"

ROLE = {
    "hunter": ("Hunter", "the walk-on who never started"),
    "sara": ("Sara", "the two-sport kid who picked one"),
    "karsta": ("Karsta", "the setter who transferred"),
    "olivia": ("Olivia", "the walk-on pitcher"),
    "derrick": ("Derrick", "the D2 starter who moved to D1"),
    "samantha": ("Samantha", "the guard who redshirted"),
    "ali": ("Ali", "the lineman who picked his school"),
    "annie": ("Annie", "the distance runner who improved late"),
    "tori": ("Tori", "the goalie who started late"),
    "cedric": ("Cedric", "the D3 star who moved up"),
    "cristelle": ("Cristelle", "the wrestle-over"),
    "jimmy": ("Jimmy", "the JUCO guard"),
    "chris": ("Chris", "the club player who walked on"),
}
FIRST = "|".join(sorted({v[0] for v in ROLE.values()}, key=len, reverse=True))
LABEL = {v[0]: v[1] for v in ROLE.values()}

CHIP = re.compile(r'<a\s+href=?["\']?/(?:story|athlete)/(\w+)["\']?[^>]*>(' + FIRST + r')(?:[^<]*)</a>')
BARE = re.compile(r'(?<=>)(' + FIRST + r')(?=</\w+>\s*(?:\u00b7|&middot;))')
POSSE = re.compile(r'\b(' + FIRST + r")'s path to NAIA Doane\b")
POSSE2 = re.compile(r'\b(' + FIRST + r")'s path\b")
FAMBALL = re.compile(r'\b(' + FIRST + r")'s family did in basketball\b")
FAM = re.compile(r'\b(' + FIRST + r")'s family\b")

tally = dict(chip=0, bare=0, possessive=0, prose=0)
for f in sorted(list(SITE.rglob("*.html")) + [SITE / "assets" / "stories.js"]):
    t0 = t = f.read_text(encoding="utf-8", errors="ignore")

    def chip(m):
        ident = m.group(1)
        if ident not in ROLE:
            return m.group(0)
        tally["chip"] += 1
        return ROLE[ident][1] + " (composite)"

    t, n = CHIP.subn(chip, t)
    t, n = BARE.subn(lambda m: LABEL[m.group(1)] + " (composite)", t)
    tally["bare"] += n
    t, n = POSSE.subn("a composite NAIA wrestling path", t)
    tally["possessive"] += n
    t, n = POSSE2.subn("a composite path in that sport", t)
    tally["possessive"] += n
    t, n = FAMBALL.subn("a family in the same spot did in basketball", t)
    tally["prose"] += n
    t, n = FAM.subn("a family in the same spot", t)
    tally["prose"] += n

    if t != t0:
        f.write_text(t, encoding="utf-8")

print("changes:", tally)

left = []
for p in sorted(SITE.rglob("*.html")):
    body = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", re.sub(
        r"<(script|style)[^>]*>.*?</\1>", " ", p.read_text(encoding="utf-8", errors="ignore"),
        flags=re.S | re.I))))
    for n in LABEL:
        for m in re.finditer(r"\b" + n + r"\b", body):
            left.append((str(p.relative_to(SITE)), n, body[max(0, m.start()-70):m.start()+90]))
print(f"\nreal first names still visible: {len(left)}")
for page, n, ctx in left[:10]:
    print(f"   {page}\n      [{n}] ...{ctx.strip()}...")

dead = {}
for p in sorted(SITE.rglob("*.html")):
    t = p.read_text(encoding="utf-8", errors="ignore")
    for m in re.finditer(r'href=?["\']?(/(?:story|athlete)/[\w-]+)', t):
        u = m.group(1).strip("\"'")
        if not (SITE / u.strip("/") / "index.html").exists():
            dead.setdefault(u, set()).add(str(p.relative_to(SITE)))
print(f"\nlinks to deleted bios: {len(dead)}")
for u, srcs in sorted(dead.items())[:10]:
    print(f"   {u:28} <- {sorted(srcs)[0]}")
