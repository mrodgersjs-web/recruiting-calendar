"""A sport we have not dated yet must not promise dates in its headline."""
import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = pathlib.Path(__file__).resolve().parents[2] / "v3" / "W14-story" / "build_sports.py"
t = p.read_text(encoding="utf-8")

pairs = [
    ("""        f'<h1 class="d1">Run {html.escape(name.lower())} recruiting with the dates in hand</h1>',""",
     """        f'<h1 class="d1">Run {html.escape(name.lower())} recruiting {headline_tail(sport)}</h1>',"""),
    ("""def cards_for(slugs):""",
     """def headline_tail(sport):
    \"\"\"Do not promise dates for a sport whose rules we have not checked yet.\"\"\"
    return "with the dates in hand" if sport["rules"] else "with a plan you can hold"


def cards_for(slugs):"""),
    ("""        return ('<h2>Your dates, by class year</h2><p>No dated calendar for this sport yet. We '""",
     """        return ('<h2>Dates for this sport</h2><p>No dated calendar for this sport yet. We '"""),
]
for old, new in pairs:
    if old not in t:
        print("MISS:", old[:70])
        continue
    t = t.replace(old, new)
    print("ok  :", old[:60])

p.write_text(t, encoding="utf-8")
import ast
ast.parse(t)
print("parses OK")
