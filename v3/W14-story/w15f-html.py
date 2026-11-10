#!/usr/bin/env python3
"""W15f: the HTML side of "first names and a sport, no school talk, click to playbooks"."""
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = pathlib.Path(__file__).resolve().parents[2]
SITE = ROOT / "site"

SLUGS = {"football": "football", "baseball": "baseball", "softball": "softball",
         "volleyball": "volleyball", "basketball": "basketball", "wrestling": "wrestling",
         "soccer": "soccer", "lacrosse": "lacrosse", "swimming": "swimming",
         "swim": "swimming", "track": "track-field", "track/xc": "track-field",
         "track & field": "track-field"}
BIO_IDS = ["hunter", "sara", "karsta", "olivia", "derrick", "samantha", "ali", "annie",
           "tori", "cedric", "cristelle", "jimmy", "chris", "composite-swim",
           "composite-football", "composite-baseball", "composite-softball",
           "composite-wbasketball", "composite-wrestling", "composite-volleyball",
           "composite-sprinter"]
ID_TO_SLUG = {"hunter": "football", "sara": "softball", "karsta": "volleyball", "olivia": "baseball",
              "derrick": "basketball", "samantha": "basketball", "ali": "football", "annie": "track-field",
              "tori": "lacrosse", "cedric": "basketball", "cristelle": "wrestling", "jimmy": "basketball",
              "chris": "soccer", "composite-swim": "swimming", "composite-football": "football",
              "composite-baseball": "baseball", "composite-softball": "softball",
              "composite-wbasketball": "basketball", "composite-wrestling": "wrestling",
              "composite-volleyball": "volleyball", "composite-sprinter": "track-field"}

count = {}


def bump(k):
    count[k] = count.get(k, 0) + 1


CHIP_BLOCK = re.compile(r"<details><summary>Stories that use it</summary><ul>.*?</ul></details>", re.S)
PROOF = re.compile(r"<h2>How this has played out</h2><p class=\"note\">.*?</ul>", re.S)
CAPTION = re.compile(r"<span>([A-Z][\w &/().'-]{2,28}):\s*[^<]{1,80}\.</span>")

for p in sorted(SITE.rglob("*.html")):
    t0 = t = p.read_text(encoding="utf-8")

    # 1. playbook chips: name-and-division lists become sport links
    def chips(m):
        sports = re.findall(r"\u00b7\s*([A-Z][A-Za-z &/]+?)\s*\u00b7", m.group(0))
        seen, items = set(), []
        for s in sports:
            key = s.strip().lower()
            slug = SLUGS.get(key) or SLUGS.get(key.split("/")[0])
            if slug and slug not in seen:
                seen.add(slug)
                items.append(f'<li><a href="/sports/{slug}">{s.strip()} playbooks</a></li>')
        if not items:
            return ""
        bump("chip blocks")
        return ("<details><summary>Where this applies</summary><ul>" + "".join(items) + "</ul></details>")

    t = CHIP_BLOCK.sub(chips, t)

    # 2. sport pages: the proof block is the last place that said where a name went to school
    t2 = PROOF.sub("", t)
    if t2 != t:
        bump("proof blocks removed")
        t = t2

    # 3. source captions stop describing a division or a role
    t2, n = CAPTION.subn(lambda m: f"<span>{m.group(1)}: an example from public reporting.</span>", t)
    if n:
        bump("source captions")
        t = t2

    # 4. disclaimers and taglines that promised stories
    t = t.replace("not to imply that any athlete or school endorses this site.",
                  "not to imply that any person or program endorses this site.")
    t = t.replace("No story to read first.", "Straight to the playbooks.")
    t = t.replace("<h2 id=\"h-stories\">Stories and tools for these sports</h2>",
                  "<h2 id=\"h-stories\">Playbooks and tools for these sports</h2>")
    t = t.replace("Composite stories are illustrations built from sourced paths.",
                  "The names are placeholders and the art is drawn.")
    t = t.replace("Every story is a composite, built only from public sources, linked where the claim is made; "
                  "no real athlete is named, pictured, or implied. Images marked Illustration show fictional composites.",
                  "Every athlete named here is a placeholder and every image marked Illustration is drawn, "
                  "not photographed. The rules, dates and numbers come from public sources, linked on the page "
                  "that uses them.")
    t = t.replace("The Commit Book: real college athlete stories and the recruiting playbooks behind them",
                  "The Commit Book: playbooks and dates for college recruiting")
    t = re.sub(r"(<meta name=\"description\" content=\")[^\"]*(stories)[^\"]*(\")",
               r"\1Playbooks, dates and tools for families navigating college recruiting and NIL. "
               r"Pick a sport and start there.\3", t)

    # 5. nothing may point at a bio page any more
    for bid, slug in ID_TO_SLUG.items():
        for kind in ("story", "athlete"):
            for q in (f'href="/{kind}/{bid}"', f"href=/{kind}/{bid}"):
                if q in t:
                    t = t.replace(q, f'href="/sports/{slug}"')
                    bump("bio links repointed")

    if t != t0:
        p.write_text(t, encoding="utf-8")
print("html pass:", count)

# 6. emerging-sports: replace the athlete-link block outright
es = SITE / "emerging-sports" / "index.html"
t = es.read_text(encoding="utf-8")
m = re.search(r"<div class=\"links\">.*?</div>", t, re.S)
if m and "wrestle-over" in m.group(0):
    repl = ('<div class="links">'
            '<a href="/sports/wrestling">Wrestling playbooks<small>What a late start looks like on paper, '
            'with the dates attached.</small></a>'
            '<a href="/sports/lacrosse">Lacrosse playbooks<small>A goalie path that begins later than people expect.</small></a>'
            '<a href="/sports/volleyball">Volleyball playbooks<small>Late specialising and staying close to home.</small></a>'
            '<a href="/playbooks/late-bloomer">The late-bloomer playbook<small>For a kid whose numbers changed in the last year.</small></a>'
            '</div>')
    es.write_text(t.replace(m.group(0), repl), encoding="utf-8")
    print("emerging-sports links block replaced")
