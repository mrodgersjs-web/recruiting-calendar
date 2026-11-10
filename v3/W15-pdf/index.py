"""W16: build the playbook index from CATALOG.json, the live store card HTML, and the PDFs themselves."""
import json
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = pathlib.Path(r"C:\Users\Jloeh\.aside\u\1\sessions\2026-11-08_sIbJ63jY5p1sXMzN\artifacts")
PDF = OUT / "playbook-pdfs"

CAT = json.loads((ROOT / "v3/W1-playbooks/CATALOG.json").read_text(encoding="utf-8"))
html = (ROOT / "site/playbooks/index.html").read_text(encoding="utf-8")

cards = {}
for ch in html.split('<div class="pb-cell">')[1:]:
    b = ch[:1600]
    slug = re.search(r'href="/playbooks/([\w-]+)"', b)
    if not slug:
        continue
    claim = re.search(r"<i>(\d+) pages", b)
    note = re.search(r'<p class="note">([^<]*)</p>', b)
    blurb = re.search(r'<span class="pb-s">(.*?)</span>', b, re.S)
    cards[slug.group(1)] = {
        "claim": claim.group(1) if claim else "?",
        "price": (re.search(r"\$(\d+)", b) or [None, "?"])[1],
        "button": "Get the playbook" in b,
        "note": bool(note),
        "note_text": re.sub(r"\s+", " ", note.group(1)).strip() if note else "",
        "blurb": re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", blurb.group(1))).strip() if blurb else "",
    }
print("cards parsed:", len(cards), "| claim matches catalog in every case:",
      all(cards.get(p["slug"], {}).get("claim") == str(p["pages"]) for p in CAT["catalog"]))

served = {p.stem for p in (ROOT / "funnel/deliver/pdfs").glob("*.pdf")}

# measured with aside.pdf.extractText on the copied files, 2026-11-10
PAGECOUNTS = {"football-junior-year": 6, "eligibility-2-hard-deadlines": 5,
              "baseball-showcase-to-signing": 5, "track-field-marks": 5,
              "d3-academic-aid-first": 4, "walk-on": 4, "juco-to-d1": 4, "late-bloomer": 4,
              "highlight-reel-social": 4, "camp-roi": 4, "nil-high-school": 4,
              "offer-and-signing": 4}

lines = [
    "# Every playbook on offer, as a PDF",
    "",
    "Files are in `playbook-pdfs/`. Built 2026-11-10 from the catalog of record",
    "(`v3/W1-playbooks/CATALOG.json`, generated 2026-11-05, rules checked against the 2026-27 NCAA",
    "Division I Manual), the live store markup on `/playbooks`, and the PDFs themselves. Page counts",
    "in the last column were read out of the files, not taken from the listing.",
    "",
    "| # | Playbook | Price | Card says | PDF is | Catalog status | Checkout | File |",
    "|---|---|---|---|---|---|---|---|",
]
for i, p in enumerate(CAT["catalog"], 1):
    slug, c = p["slug"], cards.get(p["slug"], {})
    n = PAGECOUNTS.get(slug, "?")
    held = c.get("note_text") == "Rules being verified"
    way = "served today" if slug in served else ("button, no file wired" if not held else "email capture only")
    lines.append(
        f"| {i} | {p['title']} | ${p['price_usd']} | {c.get('claim','?')} pages | {n} pages | "
        f"{p['status']} | {way} | `{slug}.pdf` |"
    )

lines += [
    "",
    "## What this table makes obvious",
    "",
    "1. **The page counts on the site are the plan, not the product.** Every card promises 12 to 24",
    "   pages; every PDF on disk is 4 to 6. A customer who buys \"Football: Junior Year Playbook, 24",
    "   pages\" for $29 and gets six pages is a refund and a bad review, before anybody reads a word",
    "   of it. Either the cards get retyped to the real length or the PDFs get written out to the",
    "   promise. My vote: retype the cards now, write the PDFs up when a sale justifies it.",
    "2. **Only two PDFs are reachable through checkout.** `funnel/deliver/pdfs/` holds",
    "   `eligibility-2-hard-deadlines.pdf` and `football-junior-year.pdf`, and those two are",
    "   byte-identical to the copies here. The other ten have a \"Get the playbook\" button and no",
    "   served file, which is why the bag link goes nowhere useful. Stripe is still test-mode.",
    "3. **The four \"Rules being verified\" cards are the honest ones.** `d3-academic-aid-first`,",
    "   `juco-to-d1`, `late-bloomer` and `nil-high-school` show an email capture instead of a button.",
    "   Those are the ones whose rules I have not sourced to a bylaw yet. `offer-and-signing` carries a",
    "   different note (prices proposed, checkout in test mode, 30-day refund) and still has a button.",
    "4. **Ten of twelve are marked OUTLINE in the catalog** even though a finished-looking PDF exists",
    "   for each. The catalog flag was set on 5 Nov and nobody moved it after the PDFs were built, so",
    "   the purchasability rule (`status == WRITTEN` and a file in the delivery folder) currently",
    "   blocks ten products on a stale label as much as on real content.",
    "",
    "## Free offers, same folder",
    "",
    "The Free tier on `/price` is $0 and its call to action is the class-year calendar. Those are",
    "in `playbook-pdfs/free/`:",
    "",
    "- `recruiting-calendar-class-2029.pdf`: all sports, the general lead magnet",
    "- `football-class-2029.pdf`, `baseball-class-2029.pdf`, `track-class-2029.pdf`: the three",
    "  sport-specific versions the funnel generates",
    "",
    "## The bundles, for context",
    "",
    f"- Sport Pack ${CAT['bundles'][0]['price_usd']}: your sport's playbook plus Eligibility, Offers &",
    "  Signing, and Camp ROI, against roughly $72 bought separately",
    f"- Every Playbook ${CAT['bundles'][1]['price_usd']}: all twelve, against roughly $234 separately",
    f"- Sideline ${CAT['bundles'][2]['price_usd_per_year']}/yr: every playbook plus the hosted tracker,",
    "  calendar alerts and benchmarks. Marked \"Preview. Not yet for sale\" on `/price`.",
    "- Planned and explicitly not for sale: Pathway $499/yr, audit $1,500 once, club $299/yr.",
    "",
    "Prices are still the proposed set you approved showing on 5 Nov; nothing here has been charged",
    "to a customer. The $99 founding rate is gone from the offers code, which is one of the two price",
    "conflicts still sitting with you.",
    "",
]
(OUT / "playbooks-index.md").write_text("\n".join(lines), encoding="utf-8")
print("wrote index;", len(CAT["catalog"]), "rows; cards matched:", len(cards))
print("served:", sorted(served))
