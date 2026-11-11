# -*- coding: utf-8 -*-
"""W27 step 1: the four written sport decks become real products.

Mike, 11 Nov 2026: "Under the Playbooks menu item on the site, it should show these 4 playbooks.
Other sports are pending." So the catalogue gains volleyball and both basketball books, the
football entry stops claiming 24 pages when it has 21, and the served PDFs move into
funnel/deliver/pdfs, which is where /api/deliver reads from.

Run: python v3/W27-nav/catalog_pass.py
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
ART = pathlib.Path(r"C:\Users\Jloeh\.aside\u\1\sessions\2026-11-08_sIbJ63jY5p1sXMzN\artifacts")
CATF = ROOT / "v3/W1-playbooks/CATALOG.json"
PDFS = ROOT / "funnel/deliver/pdfs"
fails = []

# The four decks, read from their own cover pages, not from memory.
DECKS = [
    dict(slug="football-junior-year", art="The-Commit-Book-Football-Playbook-SAMPLE.pdf",
         title="Football: The Whole Road to College", sport="Football", pages=21, usd=29,
         who="Football families, any class year, grades 9 to 12",
         outcome="A dated plan for every football recruiting window, with what a coach may and may not do, what film to send, and what the paperwork means",
         toc="How football recruiting is timed; How many players a team can take; The plan by date, class of 2029; What a coach may and may not do; Camps, 7-on-7, combines, and visits; What to send, and what good video looks like; What the paperwork really means; What it costs, and what is wasted; Checklist by grade; Ten ways families get this wrong; Sources, and what we could not settle".split("; "),
         tools=["Dated plan by month", "What a coach can and cannot do", "Camps, 7-on-7 and combine guidance", "Film length and target list steps", "Grade by grade checklist"],
         levels="FBS - FCS - D2 - D3 - NAIA - junior college", checked="11 November 2026"),
    dict(slug="volleyball-road-to-college", art="The-Commit-Book-Volleyball-Playbook-SAMPLE.pdf",
         title="Volleyball: The Whole Road to College", sport="Volleyball", pages=32, usd=29,
         who="Volleyball families, any class year, grades 9 to 12",
         outcome="What to do, when to do it, who pays, and what a coach is and is not allowed to tell you, from the 2026-27 rule text",
         toc="Read this first; How many players a team can take; The plan by date, class of 2029; What a coach may and may not do; Club, region, camps, and where she is seen; What to send, and what good video looks like; What the paperwork really means; What it costs, and what is wasted; Checklist by grade; Ten ways families get volleyball wrong; Sources, and what we could not settle".split("; "),
         tools=["Dated plan by month", "Roster seat math by level", "Club and camp money guidance", "Film length and target list steps", "Grade by grade checklist"],
         levels="D1 - D2 - D3 - NAIA - junior college", checked="11 November 2026"),
    dict(slug="basketball-road-to-college", art="The-Commit-Book-Basketball-Playbook-SAMPLE.pdf",
         title="Basketball: The Whole Road to College", sport="Basketball", pages=12, usd=19,
         who="Basketball families, boys and girls, grades 9 to 12",
         outcome="How many players a team can carry, and how that number decides how many schools to write to, when to start, and how much to spend",
         toc="How many players a team can take; The plan by date, class of 2029; What the school is really offering; What to send, and when; Summer teams, visits, and the July rule; What it costs, and what is wasted; Checklist by grade; Sources, and what we could not settle".split("; "),
         tools=["Roster seat math by level", "Dated plan by month", "Offer letter reading steps", "Cost and waste list", "Grade by grade checklist"],
         levels="NCAA D1 - D2 - D3 - NAIA - junior college", checked="10 November 2026"),
    dict(slug="girls-basketball-road-to-college", art="The-Commit-Book-Girls-Basketball-Playbook-SAMPLE.pdf",
         title="Girls' Basketball: The Whole Road to College", sport="Girls' basketball", pages=20, usd=19,
         who="Girls' basketball families, any class year, grades 9 to 12",
         outcome="The girls' clock instead of the boys' one: fewer legal ways for a coach to find you, so the list gets built earlier and pushed harder",
         toc="Read this first; How many players a team can take; The plan by date, class of 2029; What a coach may and may not do; Summer teams, visits, and the July rule; What to send, and what good video looks like; What the paperwork really means; What it costs, and what is wasted; Checklist by grade; Ten ways families get this wrong; Sources, and what we could not settle".split("; "),
         tools=["Dated plan by month", "Roster seat math by level", "Film length and target list steps", "Cost and waste list", "Grade by grade checklist"],
         levels="NCAA D1 - D2 - D3 - NAIA - junior college", checked="11 November 2026"),
]

cat = json.loads(CATF.read_text(encoding="utf-8"))
books = {b["slug"]: b for b in cat["catalog"]}

for d in DECKS:
    entry = books.get(d["slug"])
    body = dict(slug=d["slug"], title=d["title"], who=d["who"], outcome=d["outcome"], toc=d["toc"],
                tools=d["tools"], status="WRITTEN", price_usd=d["usd"], pages=d["pages"],
                format="PDF", sport=d["sport"], rules_checked=d["checked"], levels=d["levels"])
    if entry is None:
        body["story_beats"] = ["first coach contact", "the visit", "the offer", "signing day"]
        cat["catalog"].append(body)
        print("added    %-32s %2d pages  $%d" % (d["slug"], d["pages"], d["usd"]))
    else:
        before = entry.get("pages")
        entry.update(body)
        print("updated  %-32s %s -> %s pages, %s, %s" % (d["slug"], before, entry["pages"],
                                                         entry["status"], entry["format"]))

# The served file for every written deck, and the page count it really has.
try:
    from pypdf import PdfReader
except ImportError:
    from PyPDF2 import PdfReader
for d in DECKS:
    src = ART / d["art"]
    if not src.exists():
        fails.append("missing artifact " + d["art"])
        continue
    real = len(PdfReader(str(src)).pages)
    if real != d["pages"]:
        fails.append("%s claims %d pages, the file has %d" % (d["slug"], d["pages"], real))
        print("  FAIL %-30s claims %d, PDF has %d" % (d["slug"], d["pages"], real))
    else:
        print("  ok   %-30s %d pages, as claimed" % (d["slug"], real))
    dst = PDFS / (d["slug"] + ".pdf")
    old = dst.read_bytes() if dst.exists() else None
    dst.write_bytes(src.read_bytes())
    print("  served %s -> funnel/deliver/pdfs/%s.pdf (%d KB%s)"
          % (d["art"], d["slug"], dst.stat().st_size // 1024,
             ", replaced %d KB" % (len(old) // 1024) if old else ""))

ala_carte = sum(b["price_usd"] for b in cat["catalog"])
# Every book marked WRITTEN must say what its served file really holds, not what was planned.
for b in cat["catalog"]:
    if b["status"] != "WRITTEN":
        continue
    served = PDFS / (b["slug"] + ".pdf")
    if not served.exists():
        fails.append("%s is marked WRITTEN but nothing is served for it" % b["slug"])
        continue
    real = len(PdfReader(str(served)).pages)
    if real != b["pages"]:
        print("  truth    %-30s claimed %d, the served PDF has %d -> claiming %d"
              % (b["slug"], b["pages"], real, real))
        b["pages"] = real
    ala_carte = sum(x["price_usd"] for x in cat["catalog"])
for b in cat["bundles"]:
    if b["slug"] == "all-playbooks":
        b["note"] = "all %d a la carte $%d" % (len(cat["catalog"]), ala_carte)
    if b["slug"] == "sport-pack":
        b["includes_note"] = "One of the four written sport playbooks: football, volleyball, basketball, girls' basketball."
cat["updated"] = "2026-11-11 (W27: the four written sport decks are products; football page count corrected)"
CATF.write_bytes(json.dumps(cat, indent=1).encode("utf-8"))
print("\ncatalog: %d products, %d WRITTEN, a la carte $%d" % (len(cat["catalog"]),
      sum(1 for b in cat["catalog"] if b["status"] == "WRITTEN"), ala_carte))

OFF = ROOT / "funnel/lib/offers.js"
t = OFF.read_text(encoding="utf-8")
new_sports = "export const SPORTS=['football','volleyball','basketball','girls-basketball'];"
new_book = ("const SPORT_BOOK={football:'football-junior-year',volleyball:'volleyball-road-to-college',"
            "basketball:'basketball-road-to-college','girls-basketball':'girls-basketball-road-to-college'};")
if new_sports in t and new_book in t:
    print("offers.js: the Sport Pack already covers the four written sports")
else:
    t2 = re.sub(r"export const SPORTS=\[[^\]]*\];", new_sports, t, count=1)
    t2 = re.sub(r"const SPORT_BOOK=\{[^}]*\};", new_book, t2, count=1)
    if t2 == t:
        fails.append("offers.js SPORTS/SPORT_BOOK not found")
    else:
        OFF.write_bytes(t2.encode("utf-8"))
        print("offers.js: the Sport Pack now covers the four written sports, not football/baseball/track")

CSS = ROOT / "site/assets/commit.css"
c = CSS.read_text(encoding="utf-8")
block = """
/* W27: a sport whose playbook is still being written. Same language as the athlete ring: grey art,
   a PENDING band, no price, no button. */
.pb-cell.is-pend .pb-thumb{filter:grayscale(1);opacity:.55}
.pb-cell.is-pend .pb-t,.pb-cell.is-pend .pb-s,.pb-cell.is-pend .lab{color:var(--c-muted)}
.pb-cell.is-pend .pb-card{position:relative}
.pb-pend{position:absolute;left:-8%;top:44%;width:116%;transform:rotate(-14deg);background:var(--c-ink);
  color:var(--c-paper);font:600 var(--fs-label)/1 var(--font-condensed);letter-spacing:var(--ls-label);
  text-transform:uppercase;text-align:center;padding:6px 0;pointer-events:none}
.pb-soon{display:block;margin:10px 0 0;font:400 14px/1.5 var(--font-text);color:var(--c-muted)}
.pdp-soon{border-left:3px solid var(--c-line);padding-left:14px;color:var(--c-muted)}
"""
if ".pb-cell.is-pend" in c:
    print("commit.css already has the pending styles")
else:
    CSS.write_bytes((c.rstrip() + "\n" + block).encode("utf-8"))
    print("commit.css: added the pending card styles")

print("\n%s" % ("FAILED: " + "; ".join(fails) if fails else "step 1 clean"))
sys.exit(1 if fails else 0)
