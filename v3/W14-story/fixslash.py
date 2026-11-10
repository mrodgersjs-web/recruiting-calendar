"""W14c: sport pages after the bios are gone, and URLs that match vercel.json.

- vercel.json says trailingSlash:false, so canonicals and internal links must not
  carry a trailing slash. They did, which meant every link on a sport page cost a
  308 hop and each page canonicalised onto a redirect.
- Entries with page:false no longer have a bio to link. Their proof line points at
  the playbook that now carries their sources instead.
"""
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = pathlib.Path(__file__).resolve().parents[2]
p = ROOT / "v3" / "W14-story" / "build_sports.py"
t = p.read_text(encoding="utf-8")

pairs = [
    # proof lines: only link a bio that still exists
    ("""    out = []
    for a in rows:
        out.append(f'<li><a href="/story/{a["id"]}/">{html.escape(a.get("short") or a["name"])}</a> '
                   f'<span>{html.escape(str(a.get("from") or "high school"))} &rarr; '
                   f'{html.escape(str(a.get("college") or ""))}. Public sources, listed on that '
                   f"page.</span></li>")""",
     """    out = []
    for a in rows:
        label = html.escape(a.get("short") or a["name"])
        route = (f'{html.escape(str(a.get("from") or "high school"))} &rarr; '
                 f'{html.escape(str(a.get("college") or ""))}')
        if a.get("page") is False:
            pb = (a.get("playbooks") or ["offer-and-signing"])[0]
            out.append(f'<li>{label} <span>{route}. Composite, built from public reporting; '
                       f'sources on <a href="/playbooks/{pb}/#sources">the playbook</a>.</span></li>')
        else:
            out.append(f'<li><a href="/story/{a["id"]}">{label}</a> <span>{route}. Public sources, '
                       f"listed on that page.</span></li>")"""),
    # no trailing slashes anywhere in generated markup
    ('canon = f"{LIVE}/sports/{slug}/"', 'canon = f"{LIVE}/sports/{slug}"'),
    ('href="/sports/{s["slug"]}/"', 'href="/sports/{s["slug"]}"'),
    ('href="/price/">Get the calendar', 'href="/price">Get the calendar'),
    ('href="/sports/">Every sport we cover', 'href="/sports">Every sport we cover'),
    ('href="/start/">Start free with your', 'href="/start">Start free with your'),
    ('href="/library/">Browse every tool', 'href="/library">Browse every tool'),
    ('href="/rules/">See the rules we have dated', 'href="/rules">See the rules we have dated'),
    ('href="/price/">Full price list', 'href="/price">Full price list'),
    ('href="/price/">See plans and price', 'href="/price">See plans and price'),
    ("""        f'<li><a href="/rules/{rs}/{y}/">Class of {y}</a>""",
     """        f'<li><a href="/rules/{rs}/{y}">Class of {y}</a>"""),
    ("""CARDS.setdefault("offer-and-signing" """, """CARDS.setdefault("offer-and-signing" """),  # no-op anchor
]
for old, new in pairs:
    if old not in t:
        print("MISS:", old[:56].replace("\n", " "))
        continue
    if old != new:
        t = t.replace(old, new)
        print("ok  :", old[:56].replace("\n", " "))

# the store's own cards use /playbooks/x with no slash; strip slashes from the copies too
t = t.replace("""        out[m.group(2)] = '<div class="pb-cell">' + body + "</div>\"""",
              """        body = re.sub(r'href="(/playbooks/[\\w-]+)/"', 'href="\\\\1"', body)
        out[m.group(2)] = '<div class="pb-cell">' + body + "</div>\"""")

p.write_text(t, encoding="utf-8")
import ast
ast.parse(t)
print("\nparses OK")
