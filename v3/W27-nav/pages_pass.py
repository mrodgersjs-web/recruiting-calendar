# -*- coding: utf-8 -*-
"""W27 step 2: the HTML. Store page, three new product pages, sport pages, and a sweep that
removes every buy button for a book that cannot be delivered.

Mike, 11 Nov 2026: "Under the Playbooks menu item on the site, it should show these 4 playbooks.
Other sports are pending."

Run after catalog_pass.py:  python v3/W27-nav/pages_pass.py
"""
import hashlib
import json
import pathlib
import re
import sys

try:
    from pypdf import PdfReader
except ImportError:
    from PyPDF2 import PdfReader

ROOT = pathlib.Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
CAT = json.loads((ROOT / "v3/W1-playbooks/CATALOG.json").read_text(encoding="utf-8"))
BOOKS = {b["slug"]: b for b in CAT["catalog"]}
PDF_DIR = ROOT / "funnel/deliver/pdfs"
DOT = "\u00b7"
fails = []

WRITTEN = ["football-junior-year", "volleyball-road-to-college", "basketball-road-to-college",
           "girls-basketball-road-to-college"]
PAGE_BOOK = {"football": ["football-junior-year"], "volleyball": ["volleyball-road-to-college"],
             "basketball": ["basketball-road-to-college", "girls-basketball-road-to-college"]}
PENDING_SPORTS = [
    ("baseball", "Baseball", "Baseball: From Showcase to Signing", "Baseball families",
     "The plan is drafted. Each date is being checked against the rule that sets it."),
    ("softball", "Softball", "Softball: The Whole Road to College", "Softball families",
     "Roster math and the season calendar are researched. The dated plan is not written yet."),
    ("track-field", "Track &amp; Field", "Track &amp; Field: Marks to Roster",
     "Track and cross-country families",
     "Times into a target list is drafted. Invitational and signing dates are being checked."),
    ("swimming", "Swimming", "Swimming &amp; Diving: The Whole Road to College",
     "Swimming and diving families",
     "College titles run on a club calendar, not a school one. That needs its own book."),
    ("wrestling", "Wrestling", "Wrestling: The Whole Road to College", "Wrestling families",
     "Dual meets, tournaments and weight rules need a plan of their own, not a shared one."),
    ("lacrosse", "Lacrosse", "Lacrosse: The Whole Road to College", "Lacrosse families",
     "New programs every year, so the dates keep moving. Being checked now."),
    ("soccer", "Soccer", "Soccer: The Whole Road to College", "Soccer families",
     "The biggest roster numbers of any sport here. The seat math is done; the dates are next."),
]
BLURB = {
    "football-junior-year": "11 chapters. Roster seats by level, the plan by date, what a coach may and may not do, camps and combines, film, paperwork, and what the money really goes to.",
    "volleyball-road-to-college": "11 chapters. Roster seats, club and camp money, where a player is actually seen, film, paperwork, and what the money really goes to.",
    "basketball-road-to-college": "8 chapters. How many players a team can carry, and what that number says about how many schools to write to, when to start, and how much to spend.",
    "girls-basketball-road-to-college": "11 chapters. The girls' clock instead of the boys' one, the July rule, film, paperwork, and costs. Fewer legal ways for a coach to find you, so the list starts earlier.",
}
WHO_LABEL = {
    "football-junior-year": "Football families",
    "volleyball-road-to-college": "Volleyball families",
    "basketball-road-to-college": "Basketball families, boys and girls",
    "girls-basketball-road-to-college": "Girls' basketball families",
}
THUMB = {"football-junior-year": "Football", "volleyball-road-to-college": "Volleyball",
         "basketball-road-to-college": "Basketball",
         "girls-basketball-road-to-college": "Girls Basketball"}
RULES_DOC = {
    "volleyball-road-to-college": ("Built from the 2026-27 NCAA rule text, USA Volleyball's junior calendar, a regional club schedule, and a state association's season dates. Levels covered: D1, D2, D3, NAIA, junior college.",
                                   [("https://www.ncaa.org/sports/wvball", "NCAA women's volleyball rules"),
                                    ("https://www.usavolleyball.org/", "USA Volleyball junior calendar"),
                                    ("https://www.naia.org/sports/wvball", "NAIA volleyball rules")]),
    "basketball-road-to-college": ("Built from the 2026-27 NCAA Division I rule book, the printed sport calendar, and the NAIA and junior college rule books. Levels covered: D1, D2, D3, NAIA, junior college.",
                                   [("https://www.ncaa.org/sports/mbball", "NCAA men's basketball rules"),
                                    ("https://www.naia.org/sports/mbball", "NAIA basketball rules")]),
    "girls-basketball-road-to-college": ("Built from the 2026-27 NCAA Division I rule book, the printed women's basketball calendar, and the NAIA and junior college rule books. Levels covered: D1, D2, D3, NAIA, junior college.",
                                          [("https://www.ncaa.org/sports/wbball", "NCAA women's basketball rules"),
                                           ("https://www.naia.org/sports/wbball", "NAIA basketball rules")]),
    "football-junior-year": ("Built from the 2026-27 NCAA Division I rule book, the printed football calendars for both subdivisions, and the NAIA and junior college rule books. Levels covered: FBS, FCS, D2, D3, NAIA, junior college.", None),
}


SPORT_PAGE = {"volleyball-road-to-college": "volleyball", "basketball-road-to-college": "basketball",
              "girls-basketball-road-to-college": "basketball", "football-junior-year": "football"}


def ready(slug):
    return BOOKS[slug]["status"] == "WRITTEN" and (PDF_DIR / (slug + ".pdf")).exists()


def claim(slug):
    """What the card may say about length: the real count of the served file, or a plan."""
    if not (PDF_DIR / (slug + ".pdf")).exists():
        return "%d pages planned" % BOOKS[slug]["pages"]
    n = len(PdfReader(str(PDF_DIR / (slug + ".pdf"))).pages)
    if n != BOOKS[slug]["pages"]:
        fails.append("%s: catalogue says %d pages, the served PDF has %d" % (slug, BOOKS[slug]["pages"], n))
    return "%d pages %s PDF" % (n, DOT)


def cell(slug):
    b = BOOKS[slug]
    return ('<div class="pb-cell"><a class="pb-card" href="/playbooks/%s">'
            '<span class="pb-thumb"><b>%s</b><i>%s</i></span>'
            '<span class="lab">%s</span><span class="pb-t">%s</span><span class="pb-s">%s</span>'
            '<span class="pb-p">$%d</span></a>%s</div>' % (
                slug, THUMB[slug], claim(slug), WHO_LABEL[slug], b["title"].replace("&", "&amp;"),
                BLURB[slug], b["price_usd"],
                '<button class="btn btn--primary" data-offer="%s">Get the playbook</button>' % slug
                if ready(slug) else '<p class="note">Rules being verified</p>'))


def pend_cell(sport_slug, thumb, title, lab, line):
    """A sport whose book is not finished: grey art, a PENDING band, no price, no button."""
    return ('<div class="pb-cell is-pend"><a class="pb-card" href="/sports/%s">'
            '<span class="pb-thumb"><b>%s</b><i>Playbook in progress %s no price yet</i></span>'
            '<span class="pb-pend">Pending</span>'
            '<span class="lab">%s</span><span class="pb-t">%s</span>'
            '<span class="pb-s">%s The sport page shows what we have dated so far.</span></a></div>'
            % (sport_slug, thumb, DOT, lab, title, line))


def grid_span(t, i):
    """The slice of text for the <div class="pb-grid"> block starting at i, depth-walked."""
    j = i + len('<div class="pb-grid">')
    depth = 1
    while depth:
        m = re.compile(r"<div\b|</div>").search(t, j)
        if not m:
            raise SystemExit("unbalanced grid at %d" % i)
        depth += 1 if m.group(0).startswith("<div") else -1
        j = m.end()
    return i, j


def sweep(html):
    """No buy button and no bag button for a book that cannot be delivered."""
    n = 0
    for slug in BOOKS:
        if ready(slug):
            continue
        html, k = re.subn(r'<button class="btn[^"]*" data-offer="%s">[^<]*</button>' % slug,
                          '<p class="note">Rules being verified</p>', html)
        html, k2 = re.subn(r'\s*<button class="btn[^"]*" data-add="%s"[^>]*>[^<]*</button>' % slug, "", html)
        n += k + k2
    return html, n


SPORT_SLUGS = ["baseball-showcase-to-signing", "track-field-marks"]

# ---------------------------------------------------------------- the store page
store = SITE / "playbooks/index.html"
t = store.read_text(encoding="utf-8")
head, rest = t.split("<main", 1)
main_open, tail = rest.split("</main>", 1)
cells_old = re.findall(r'<div class="pb-cell">.*?</div>', main_open, re.S)
craft = []
for c in cells_old:
    m = re.search(r'href="/playbooks/([a-z0-9-]+)"', c)
    if not m:            # an already pending tile, from a previous run
        continue
    slug = m.group(1)
    if slug in WRITTEN or slug in SPORT_SLUGS:
        continue
    c = re.sub(r"<i>[^<]*</i>", "<i>%s</i>" % claim(slug), c)
    craft.append(sweep(c)[0])
bundles = re.search(r'<section class="pb-bund".*?</section>', main_open, re.S).group(0)
bundles = bundles.replace(
    "<b>Sport Pack (your sport playbook + Eligibility + Offers &amp; Signing + Camp ROI)</b>",
    "<b>Sport Pack (one of the four written sport playbooks + Eligibility + Offers &amp; Signing + Camp ROI)</b>")
if "The Sport Pack covers any of the four" not in bundles:
    bundles = bundles.replace("Prices proposed for launch.",
                              "Prices proposed for launch. The Sport Pack covers any of the four written sports. "
                              "A sport playbook gets a price and a button when its rules are all checked.")
main = ['<main class="cb-page"><p class="lab">Playbooks</p>'
        '<h1 class="d1">Run recruiting yourself, with the rules in hand.</h1>'
        '<p class="lede">Four sport playbooks are done and ready to download. They cover football, '
        'volleyball, and basketball for boys and girls. The other sports are still being written, so '
        'they show no price and no button. Every date in a done book shows the rule behind it.</p>'
        '<h2 class="d2">Ready now: four sport playbooks</h2>'
        "<p>Each one is a whole book, not a checklist. Rules checked 11 November 2026 against the NCAA "
        "rule text and the printed calendars.</p>"
        '<div class="pb-grid">' + "".join(cell(s) for s in WRITTEN) + "</div>"
        '<h2 class="d2">Every sport: the books that are not about one sport</h2>'
        "<p>These apply no matter what you play. One is ready to download now. The rest show a button "
        "as soon as their rules are re-checked.</p>"
        '<div class="pb-grid">' + "".join(craft) + "</div>"
        '<h2 class="d2">Sports still being written</h2>'
        "<p>We price a sport book only when every date in it is checked against the rule that sets it. "
        "These seven are in progress. Nothing here has a price, so nothing can be bought by accident.</p>"
        '<div class="pb-grid">' + "".join(pend_cell(*p) for p in PENDING_SPORTS) + "</div>"
        + bundles + "</main>"]
new_store = head + "".join(main) + tail
desc = ("Four sport playbooks you can download today: football, volleyball, and the two basketball "
        "books. Every date shows the rule it comes from, and the sports still being written say so.")
new_store = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % desc,
                   new_store, count=1)
new_store = re.sub(r'(<meta (?:property|name)="(?:og|twitter):description" content=")[^"]*(">)',
                   r"\g<1>%s\g<2>" % desc, new_store)
store.write_bytes(new_store.encode("utf-8"))
print("store page: %d written sport cards, %d cross-sport cards, %d pending sports"
      % (len(WRITTEN), len(craft), len(PENDING_SPORTS)))
if len(craft) != 9:
    fails.append("expected 9 cross-sport cards, carried %d" % len(craft))

# ---------------------------------------------------------------- product pages
pdp_src = (SITE / "playbooks/football-junior-year/index.html").read_text(encoding="utf-8")
NAV_HEAD = pdp_src[: pdp_src.find("<main")]
NAV_FOOT = pdp_src[pdp_src.find("</main>"):]


def pdp(slug):
    b, d = BOOKS[slug], " ".join(BOOKS[slug]["outcome"].split())
    note, links = RULES_DOC[slug]
    body = ['<main class="cb-page pdp"><div class="pdp-g"><div class="pdp-img">'
            '<span class="pb-thumb big"><b>%s</b><i>%s</i></span></div>'
            '<div class="pdp-info"><p class="lab">Playbook</p><h1 class="d2">%s</h1>'
            '<p class="pb-p">$%d <span class="note">one-time</span></p><p>%s</p>'
            '<p class="note">For %s. Levels covered: %s. Rules checked %s.</p>'
            ' <button class="btn btn--primary btn--l" data-checkout="%s" data-offer="%s">Get the playbook</button>'
            ' <button class="btn btn--outline sr__add" data-add="%s" aria-pressed="false">Get</button>'
            ' <p class="note">No sales calls. Full refund for 30 days. Checkout is in test mode until we go live.</p>'
            ' <details open><summary>What\'s inside</summary><ol>%s</ol></details>'
            ' <details><summary>What you can use from it</summary><ul>%s</ul></details>'
            ' <details><summary>Where this applies</summary><ul>%s</ul></details>'
            "</div></div>" % (
                THUMB[slug], claim(slug), b["title"].replace("&", "&amp;"), b["price_usd"], d,
                b["who"].lower(), b["levels"].replace(" - ", ", "), b["rules_checked"], slug, slug, slug,
                "".join("<li>%s</li>" % x for x in b["toc"]),
                "".join("<li>%s</li>" % x for x in b["tools"]),
                '<li><a href="/sports/%s">%s playbooks</a></li>' % (SPORT_PAGE[slug], b["sport"]))]
    body.append('<section class="src-list" id="sources"><h2>Where these dates come from</h2>'
                '<p class="note">%s</p><ul>%s</ul>'
                '<p class="note">The book ends with the documents behind every date, and a list of what we '
                "could not settle. Dates worked out from the rule text instead of read off a page are marked "
                "PROJECTED inside it.</p></section>" % (
                    note, "".join('<li><a href="%s" rel="noopener">%s</a></li>' % (u, l) for u, l in links)))
    page = NAV_HEAD + "".join(body) + NAV_FOOT
    title = b["title"].replace("&", "&amp;")
    page = re.sub(r"<title>[^<]*</title>", "<title>%s | The Commit Book</title>" % title, page, count=1)
    page = re.sub(r'(<meta property="og:title" content=")[^"]*(">)', r"\g<1>%s | The Commit Book\g<2>" % title, page)
    page = re.sub(r'(<meta name="twitter:title" content=")[^"]*(">)', r"\g<1>%s | The Commit Book\g<2>" % title, page)
    page = re.sub(r'(<meta (?:property|name)="(?:og|twitter):description" content=")[^"]*(">)',
                  r"\g<1>%s\g<2>" % d, page)
    page = re.sub(r'(<meta name="description" content=")[^"]*(">)', r"\g<1>%s\g<2>" % d, page, count=1)
    page = re.sub(r'<link rel="canonical" href="[^"]*">',
                  '<link rel="canonical" href="https://recruiting-calendar.vercel.app/playbooks/%s/">' % slug,
                  page, count=1)
    page = re.sub(r'<meta property="og:url" content="[^"]*">',
                  '<meta property="og:url" content="https://recruiting-calendar.vercel.app/playbooks/%s/">' % slug,
                  page, count=1)
    return page


for slug in ["volleyball-road-to-college", "basketball-road-to-college", "girls-basketball-road-to-college"]:
    d = SITE / "playbooks" / slug
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_bytes(pdp(slug).encode("utf-8"))
    print("product page: /playbooks/%s/" % slug)

# football's product page, retitled to what the book is now
fb = SITE / "playbooks/football-junior-year/index.html"
f = fb.read_text(encoding="utf-8")
f = f.replace("Football: Junior Year Playbook", BOOKS["football-junior-year"]["title"].replace("&", "&amp;"))
f = re.sub(r"<i>[^<]*</i>", "<i>%s</i>" % claim("football-junior-year"), f, count=1)
for pat, repl in ((r"<details open><summary>What's inside</summary><ol>.*?</ol></details>",
                   "<details open><summary>What's inside</summary><ol>%s</ol></details>" % "".join(
                       "<li>%s</li>" % x for x in BOOKS["football-junior-year"]["toc"])),
                  (r"<details><summary>Tools included</summary><ul>.*?</ul></details>",
                   "<details><summary>What you can use from it</summary><ul>%s</ul></details>" % "".join(
                       "<li>%s</li>" % x for x in BOOKS["football-junior-year"]["tools"])),
                  (r'<section class="src-list" id="sources">.*?</section>',
                   '<section class="src-list" id="sources"><h2>Where these dates come from</h2>'
                   '<p class="note">%s</p><p class="note">The book ends with the documents behind every date, '
                   "and a list of what we could not settle. Dates worked out from the rule text instead of read "
                   "off a page are marked PROJECTED inside it.</p></section>" % RULES_DOC["football-junior-year"][0])):
    m = re.search(pat, f, re.S)
    if not m:
        if repl[:48] in f:
            continue          # a re-run: this block is already rewritten
        fails.append("football product page: no match for %s" % pat[:34])
        continue
    f = f[: m.start()] + repl + f[m.end():]
for tag in ("og:description", "twitter:description", "description"):
    f = re.sub(r'(<meta (?:property|name)="%s" content=")[^"]*(">)' % tag,
               r"\g<1>%s\g<2>" % " ".join(BOOKS["football-junior-year"]["outcome"].split()), f)
fb.write_bytes(f.encode("utf-8"))
print("product page: /playbooks/football-junior-year/ retitled, real page count, its own sources")

# every book that cannot be delivered yet says so on its own page, and loses its buttons
for d in sorted((SITE / "playbooks").iterdir()):
    f = d / "index.html"
    slug = d.name
    if not (d.is_dir() and f.exists()) or slug not in BOOKS or ready(slug):
        continue
    x = f.read_text(encoding="utf-8")
    x, k1 = re.subn(r'<button class="btn btn--primary btn--l" data-checkout="%s"[^>]*>[^<]*</button>' % slug,
                    '<p class="note">Rules being verified</p>', x, count=1)
    x, k2 = re.subn(r'\s*<button class="btn btn--outline sr__add" data-add="%s"[^>]*>[^<]*</button>' % slug, "", x, count=1)
    x = re.sub(r"<i>[^<]*</i>", "<i>%s</i>" % claim(slug), x, count=1)
    if re.search(r'data-(?:offer|add|checkout)="%s"' % slug, x):
        fails.append("%s: a buy or bag button survived" % slug)
    if slug in SPORT_SLUGS:
        x, k3 = re.subn(r'<p class="pb-p">\$\d+\s*<span class="note">one-time</span></p>',
                        '<p class="pb-p">Price set when the book is done</p>', x, count=1)
    else:
        x, k3 = re.subn(r'(<p class="pb-p">\$\d+\s*)<span class="note">one-time</span></p>',
                        r'\g<1><span class="note">proposed, not on sale yet</span></p>', x, count=1)
    soon = ('<p class="pdp-soon">This book is being checked date by date. It gets a buy button when '
            'every date in it shows the rule behind it.</p>') if slug not in SPORT_SLUGS else ''
    if soon:
        x, k4 = re.subn(r'(<p class="pb-p">.*?</p>)', r'\g<1>' + soon, x, count=1)
        if k4 != 1 and soon not in x:
            fails.append("%s: the price line was not found" % slug)
    if k3 != 1 and 'one-time' not in x:
        fails.append("%s: the price line was not found" % slug)
    f.write_bytes(x.encode("utf-8"))
    print("product page: /playbooks/%s/ -> no buttons, and it says why" % slug)

# the two sports whose books were priced here before, and never had a file
for slug, line in (("baseball-showcase-to-signing",
                    "Baseball families: the plan is drafted and each date is being checked against the rule that sets it."),
                   ("track-field-marks",
                    "Track and cross-country families: the plan is drafted and the dates are being checked.")):
    p = SITE / "playbooks" / slug / "index.html"
    x = p.read_text(encoding="utf-8")
    x = x.replace('<p class="note">No sales calls.', '<p class="pdp-soon">%s</p><p class="note">No sales calls.' % line, 1)
    p.write_bytes(x.encode("utf-8"))
    print("product page: /playbooks/%s/ notes the dated plan is still being checked" % slug)

# ---------------------------------------------------------------- sport pages
for page in sorted((SITE / "sports").iterdir()):
    f = page / "index.html"
    if not f.exists():
        continue
    name = page.name
    t = f.read_text(encoding="utf-8")
    i = t.find('<div class="pb-grid">')
    if i < 0:
        fails.append("/sports/%s has no playbook grid" % name)
        continue
    a, b = grid_span(t, i)
    cells = re.findall(r'<div class="pb-cell">.*?</div>', t[a:b], re.S)
    keep = []
    for c in cells:
        m = re.search(r'href="/playbooks/([a-z0-9-]+)"', c)
        if not m:
            continue
        slug = m.group(1)
        if slug in WRITTEN or slug in SPORT_SLUGS:
            continue
        c = re.sub(r"<i>[^<]*</i>", "<i>%s</i>" % claim(slug), c)
        keep.append(sweep(c)[0])
    if name in PAGE_BOOK:
        lead = "".join(cell(s) for s in PAGE_BOOK[name])
        soon = ""
    else:
        pend = next(p for p in PENDING_SPORTS if p[0] == name)
        lead = pend_cell(*pend)
        soon = ('<p class="pb-soon">The %s playbook is being written. It will sit here with a price when '
                "every date in it is checked against the rule that sets it.</p>" % pend[1].replace("&amp;", " and"))
    t = t[:a] + '<div class="pb-grid">' + lead + "".join(keep) + "</div>" + t[b:]
    if soon:
        t = t.replace("<p>Each playbook is a plan you run, priced on its own. No subscription needed.</p>",
                      "<p>Each playbook is a plan you run, priced on its own. No subscription needed.</p>" + soon, 1)
    f.write_bytes(t.encode("utf-8"))
    print("sport page: /sports/%s/ -> %s" % (name, "its own book first" if name in PAGE_BOOK else "a pending tile"))

# every other product page says what its served file really holds
for d in sorted((SITE / "playbooks").iterdir()):
    f = d / "index.html"
    if not d.is_dir() or not f.exists():
        continue
    slug = d.name
    if slug in SPORT_SLUGS or slug not in BOOKS:
        continue
    x = f.read_text(encoding="utf-8")
    x2 = re.sub(r"<i>[^<]*</i>", "<i>%s</i>" % claim(slug), x, count=1)
    if x2 != x:
        f.write_bytes(x2.encode("utf-8"))
        print("product page: /playbooks/%s/ length line now reads \"%s\"" % (slug, claim(slug)))

# ---------------------------------------------------------------- buy-button sweep
total = 0
for f in sorted(SITE.rglob("*.html")):
    rel = f.relative_to(SITE).parts
    if "sports" in rel[:-1] or "playbooks" in rel[:-1]:
        continue
    t = f.read_text(encoding="utf-8")
    t2, n = sweep(t)
    if n:
        f.write_bytes(t2.encode("utf-8"))
        total += n
        print("  %d dead buy button(s) removed in %s" % (n, f.relative_to(SITE)))
print("sweep: %d buttons removed site-wide" % total)

# ---------------------------------------------------------------- sitemap
sm = SITE / "sitemap.xml"
s = sm.read_text(encoding="utf-8")
before = s.count("<url>")
rows = "".join("<url><loc>https://recruiting-calendar.vercel.app/playbooks/%s/</loc>"
               "<lastmod>2026-11-11</lastmod><changefreq>monthly</changefreq></url>" % slug for slug in WRITTEN[1:])
s2 = re.sub(r"(<url><loc>https://recruiting-calendar\.vercel\.app/playbooks/football-junior-year/</loc>[^<]*(?:<[^>]*>[^<]*)*</url>)",
            r"\1" + rows, s, count=1)
if s2 == s:
    fails.append("sitemap: no new URLs were added")
sm.write_bytes(s2.encode("utf-8"))
print("sitemap: %d -> %d URLs" % (before, s2.count("<url>")))

# ---------------------------------------------------------------- cache keys
keys = {}
for f in sorted(SITE.rglob("*.html")):
    t = f.read_text(encoding="utf-8")

    def fix(m):
        url = m.group(1)
        p = SITE / url.lstrip("/").replace("/", "\\")
        if not p.exists():
            fails.append("asset %s is referenced but missing" % url)
            return m.group(0)
        # core.autocrlf is on: git stores LF and Vercel serves LF, so the key
        # has to be the hash of the committed bytes, not of the working copy.
        real = hashlib.md5(p.read_bytes().replace(b"\r\n", b"\n")).hexdigest()[:8]
        keys.setdefault(url, {}).setdefault(m.group(2), 0)
        keys[url][m.group(2)] += 1
        return m.group(0).replace(m.group(2), real)

    t2 = re.sub(r'(?:href|src)="(/[^"]+\.(?:js|css))\?v=([0-9a-f]{6,8})"', fix, t)
    if t2 != t:
        f.write_bytes(t2.encode("utf-8"))
for url, c in sorted(keys.items()):
    print("  %-24s stale keys rewritten: %s" % (url, c))

print("\n%s" % ("FAILED: " + "; ".join(fails) if fails else "step 2 clean"))
sys.exit(1 if fails else 0)
