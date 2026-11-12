"""site.py — the site half of the sport template (W28, 11 Nov 2026).

    python site.py                  every book listed in STORE.json whose PDF is built
    python site.py <slug> <slug>    a subset
    python site.py --plan           say what would change, write nothing

Run it after `python deck.py <slug>` and the print step have left `pdfs/<slug>.pdf`
in this lane. TEMPLATE.md is the contract, this file is the machine. It is
idempotent: run it twice, the second run changes nothing.

Ten steps, in order: catalogue, served files, offers, store page, product pages,
sport pages, ring, redirects, sitemap, cache keys. Shipped copy is carried, not
rewritten: a book that already has a store tile keeps its words and gets its
price and page count refreshed from the catalogue, which is the only owner.
"""
import hashlib
import json
import pathlib
import re
import shutil
import sys

try:
    from pypdf import PdfReader
except ImportError:
    from PyPDF2 import PdfReader

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SITE = ROOT / "site"
CAT_F = ROOT / "v3/W1-playbooks/CATALOG.json"
DELIVER = ROOT / "funnel/deliver/pdfs"
STORE = json.loads((HERE / "STORE.json").read_text(encoding="utf-8"))
SPORT_KEY = STORE.get("sport_key", {})
PLAN = "--plan" in sys.argv
PRICE = STORE["sport_price"]
fails, skips, repriced = [], [], []
DAY = "2026-11-11"


# A ?v= reference, matched without any escaping that would fight this file's quotes.
_KEYRX = re.compile("([^" + chr(34) + "'()" + chr(92) + "s]+)" + chr(92) + "?v=([0-9a-f]{8})")


def lf(t):
    return t.replace("\r\n", "\n").replace("\r", "\n")


def key_of(path):
    """The cache key Vercel answers with: md5 of the LF bytes, first 8."""
    bs = path.read_bytes()
    if path.suffix.lower() in (".html", ".js", ".css", ".json", ".svg", ".txt", ".xml"):
        bs = lf(bs.decode("utf-8")).encode("utf-8")
    return hashlib.md5(bs).hexdigest()[:8]


def write(path, text):
    want = lf(text).encode("utf-8")
    rel = path.relative_to(ROOT)
    if PLAN:
        print("  plan   %-50s %7d bytes" % (rel, len(want)))
    elif path.exists() and path.read_bytes() == want:
        print("  same   %-50s" % rel)
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(want)
        print("  wrote  %-50s %7d bytes" % (rel, len(want)))
    return want


def configs():
    out = {}
    for p in sorted((HERE / "SPORTS").glob("*.json")):
        c = json.loads(p.read_text(encoding="utf-8"))
        out[c["slug"]] = c
    return out


CFG = configs()


def asked():
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    for s in a:
        if s not in CFG:
            raise SystemExit("no config for %s (looked in %s)" % (s, HERE / "SPORTS"))
    return a or [s for s in STORE["written_order"] if s in CFG]


def buildable():
    out = []
    for s in asked():
        c = CFG[s]
        if not (HERE / ("manifest-%s.json" % s)).exists():
            skips.append("%s: no manifest. Run deck.py first." % s)
        elif not (HERE / "pdfs" / (s + ".pdf")).exists():
            skips.append("%s: no PDF. Run deck.py, then the print step." % s)
        elif c["price"] != PRICE:
            fails.append("%s: config price %s, store price %s" % (s, c["price"], PRICE))
        elif "site" not in c:
            fails.append("%s: no site block, so the store has no copy for it" % s)
        else:
            out.append(s)
    return out


NEW = buildable()
CAT = json.loads(CAT_F.read_text(encoding="utf-8"))
BOOKS = {b["slug"]: b for b in CAT["catalog"]}
# One price for every sport playbook, Mike's rule in W28: the two basketball books were
# $19 and come up with the rest. Cross-sport titles keep their own prices, which is a
# different decision, and `flat_all_titles` is the one-line flip if that ever changes.
for _s in STORE["written_order"]:
    if _s in BOOKS and BOOKS[_s].get("price_usd") != PRICE:
        BOOKS[_s]["price_usd"] = PRICE
        repriced.append(_s)
if STORE.get("flat_all_titles"):
    for b in CAT["catalog"]:
        b["price_usd"] = PRICE
GOT = [s for s in STORE["written_order"] if s in NEW or BOOKS.get(s, {}).get("status") == "WRITTEN"]


def checked_date(c):
    m = re.search(r"\d{1,2}\s+\w+\s+\d{4}", c.get("rules_checked", ""))
    return m.group(0) if m else c["rules_checked"]


def who_label(c):
    if "who_label" in c["site"]:
        return c["site"]["who_label"]
    sport = re.sub(r"^(Men's|Women's)\s+", "", c["ring_label"])
    return "%s families, %s" % (sport, "boys and men" if c["gender"] == "men" else "girls and women")


def sources_of(slug):
    """The last chapter names the documents behind the book, and the store page lists them.
    The house style is a document name plus the day it was read, not a bare URL: a nine-word
    link is not something a parent checks, and it drags the reading grade up for nothing. So
    a link is used when the book carries one, and the printed name is used when it does not."""
    d = HERE / "fragments" / slug
    files = sorted(d.glob("c*.html"))
    if not files:
        return []
    t = files[-1].read_text(encoding="utf-8")
    # The chapter ends with what the book could NOT settle. Those lines are open questions,
    # not sources, so the store page must stop at that heading.
    t = re.split(r'(?i)<h3[^>]*>\s*(?:What we could not settle|What the next edition)', t)[0]
    out, seen = [], set()
    # The house chapter prints each document inside a <src> block: its name, what was read
    # from it, and the address. That is where the store page's source list comes from.
    for block in re.findall(r"(?is)<src\b[^>]*>(.*?)</src>", t):
        raw = re.sub(r"\s+", " ", block).strip()
        url = ""
        m = re.search(r'https?://[^\s]+', raw)
        if m:
            url = m.group(0).rstrip(".,)")
            raw = (raw[:m.start()] + " " + raw[m.end():]).strip()
        lab = raw.split(". ")[0].strip().strip(",.")
        if len(lab) >= 12 and lab not in seen:
            seen.add(lab)
            out.append([url, lab])
    for u, lab in re.findall(r'<a href="(https?://[^"]+)"[^>]*>(.*?)</a>', t, re.S):
        lab = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", lab)).strip()
        if lab and u not in seen:
            seen.add(u)
            out.append([u, lab])
    for item in re.findall(r"(?is)<li\b[^>]*>(.*?)</li>", t):
        first = re.findall(r"(?is)<(strong|b|a)\b[^>]*>(.*?)</\1>", item)
        lab = first[0][1] if first else item
        lab = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", lab)).strip().rstrip(",.")
        url = ""
        m = re.search(r'https?://[^\s"]+', re.sub(r"<[^>]+>", " ", item))
        if m:
            url = m.group(0).rstrip(".,)")
        if len(lab) >= 12 and lab not in seen:
            seen.add(lab)
            out.append([url, lab])
    return out[:12]


def claim_html(c, pages):
    return "<b>%d pages</b> &middot; <i>%s</i>" % (pages, c["site"]["claim"])


def tile_claim(c, pages):
    """The caption inside a tile thumbnail. The shipped tiles print "%d pages · PDF" in
    small mono, so a new book may not print a huge bold page count next to a wrapped
    sentence. The claim line belongs under the title, not on the thumbnail."""
    return "%d pages &middot; PDF" % pages


def shelf_list(own, ids):
    """The playbook rows on a ring card. A card leads with its own book, because a
    baseball family who came for the baseball playbook should not see two general titles
    and a link first. Everything else is whatever is written: a title that is still an
    outline cannot be added to a bag for $19, so it does not appear. If that leaves a
    card with one row, the eligibility book fills it, since every sport has the two dates.
    """
    keep = [own] if own else []
    for x in ids:
        if x != own and BOOKS.get(x, {}).get("status") == "WRITTEN":
            keep.append(x)
    if len(keep) < 2 and "eligibility-2-hard-deadlines" not in keep:
        keep.append("eligibility-2-hard-deadlines")
    return keep



def shelf_state(html, slug):
    """What a tile may say, decided by the catalogue and nothing else.

    A written book carries its price and a Get button. A book that is still an outline
    carries neither: no price, because there is nothing to charge for, and no button,
    because a click would sell a file that does not exist. This replaces the older pass
    that hid the button and left the price standing, which read as a free book.
    """
    b = BOOKS.get(slug) or {}
    if b.get("status") == "WRITTEN":
        return re.sub(r'<span class="pb-p">\$\d+</span>',
                      '<span class="pb-p">$%d</span>' % b["price_usd"], html)
    html = re.sub(r'<span class="pb-p">\$\d+</span>',
                  '<span class="pb-p is-soon">in progress</span>', html)
    html = re.sub(r'<button class="btn[^"]*" data-offer="%s">[^<]*</button>' % re.escape(slug),
                  '<p class="note">in progress &middot; no price yet</p>', html)
    return html.replace('<div class="pb-cell">', '<div class="pb-cell is-soon">', 1)


def cell(slug):
    c, b = CFG[slug], BOOKS[slug]
    return ('<div class="pb-cell"><a class="pb-card" href="/playbooks/%s">'
            '<span class="pb-thumb"><b>%s</b><i>%s</i></span>'
            '<span class="lab">%s</span><span class="pb-t">%s</span><span class="pb-s">%s</span>'
            '<span class="pb-p">$%d</span></a>'
            '<button class="btn btn--primary" data-offer="%s">Get the playbook</button></div>' % (
                slug, c["ring_label"].replace("&", "&amp;"), tile_claim(c, b["pages"]),
                who_label(c), c["title"].replace("&", "&amp;"),
                "%d chapters. %s" % (len(c["chapters"]), c["site"]["blurb"]),
                b["price_usd"], slug))


def pend_cell(p):
    return ('<div class="pb-cell is-pend"><a class="pb-card" href="/sports/%s">'
            '<span class="pb-thumb"><b>%s</b><i>Playbook in progress &middot; no price yet</i>'
            '<span class="pb-pend">In progress</span></span>'
            '<span class="lab">%s</span><span class="pb-t">%s</span>'
            '<span class="pb-s">%s The sport page shows what we have dated so far.</span></a></div>'
            % tuple(p))


def cells_by_slug(grid_html):
    """Every tile in a grid, keyed by the playbook it points at, in the order they sit.
    Tiles nest a div inside a div, so this walks the depth instead of trusting a regex."""
    out, i, n = {}, 0, len(grid_html)
    while i < n:
        j = grid_html.find('<div class="pb-cell', i)
        if j < 0:
            break
        k, depth = j, 0
        while k < n:
            nxt_open = grid_html.find('<div', k + 1)
            nxt_close = grid_html.find('</div>', k)
            if nxt_close < 0:
                break
            if 0 <= nxt_open < nxt_close:
                depth, k = depth + 1, nxt_open
            else:
                k = nxt_close + len('</div>')
                if depth == 0:
                    break
                depth -= 1
        body = grid_html[j:k]
        m = re.search(r'/playbooks/([a-z0-9-]+)', body)
        if m and m.group(1) not in out:
            out[m.group(1)] = body
        i = k
    return out


def grid_span(t, i):
    j, depth = i + len('<div class="pb-grid">'), 1
    while depth:
        m = re.compile(r"<div\b|</div>").search(t, j)
        if not m:
            raise SystemExit("unbalanced pb-grid at %d" % i)
        depth += 1 if m.group(0).startswith("<div") else -1
        j = m.end()
    return i, j


def tiles_in(html):
    out = {}
    for c in re.findall(r'<div class="pb-cell(?: is-(?:pend|soon))?">.*?</div>', html, re.S):
        m = re.search(r'href="/playbooks/([a-z0-9-]+)"', c)
        if m:
            out[m.group(1)] = c
    return out


# ------------------------------------------------------------------ 1 catalogue
print("\n1 catalogue")
for slug in NEW:
    c = CFG[slug]
    man = json.loads((HERE / ("manifest-%s.json" % slug)).read_text(encoding="utf-8"))
    pages = len(PdfReader(str(HERE / "pdfs" / (slug + ".pdf"))).pages)
    if len(c["chapters"]) != len(man["chapters"]):
        fails.append("%s: config lists %d chapters, the manifest %d"
                     % (slug, len(c["chapters"]), len(man["chapters"])))
    entry = BOOKS.get(slug, {})
    entry.update({
        "slug": slug, "title": c["title"], "who": who_label(c), "outcome": c["site"]["outcome"],
        "toc": c["chapters"], "tools": c["site"]["tools"], "status": "WRITTEN", "price_usd": PRICE,
        "pages": pages, "format": "PDF", "sport": c["ring_label"],
        "levels": re.sub(r"(?i)\s+and\s+", " \u00b7 ", c["levels"]), "rules_checked": checked_date(c),
        "gender": c["gender"], "athlete": c["athlete"], "class_year": c["class_year"],
        "edition": c["edition"], "doc_sha": man.get("doc_sha", ""), "deck_grade": man.get("grade", ""),
        "claim": c["site"]["claim"], "story_beats": entry.get("story_beats", [
            "first coach contact", "the visit", "the offer", "signing day"])})
    BOOKS[slug] = entry
    if entry not in CAT["catalog"]:
        CAT["catalog"].append(entry)
    print("  %-32s %2d pages $%d, grade %s, %d sources named"
          % (slug, pages, PRICE, entry["deck_grade"], len(sources_of(slug))))

ala = sum(b["price_usd"] for b in CAT["catalog"])
for bd in CAT["bundles"]:
    if bd["slug"] == "all-playbooks":
        bd["note"] = "all %d a la carte $%d" % (len(CAT["catalog"]), ala)
    elif bd["slug"] == "sport-pack":
        tot = sum(BOOKS[p]["price_usd"] for p in ["eligibility-2-hard-deadlines", "offer-and-signing",
                                                 "camp-roi"] + GOT if p in BOOKS)
        bd["note"] = "a $%d pack against $%d for the same books apart" % (bd["price_usd"], tot)
        bd["includes_note"] = ("One of the %d written sport playbooks: %s."
                               % (len(GOT), ", ".join(BOOKS[s]["sport"] for s in GOT)))
for s, rep in STORE["retired"].items():
    if s in BOOKS:
        BOOKS[s]["note"] = "Replaced by %s." % rep
        print("  retired %s, pointed at %s" % (s, rep))
print("  %d products, %d written sport books, $%d a la carte" % (len(CAT["catalog"]), len(GOT), ala))
write(CAT_F, json.dumps(CAT, indent=1, ensure_ascii=False) + "\n")

# ------------------------------------------------------------------ 2 served files
print("\n2 served files")
for slug in NEW:
    src = HERE / "pdfs" / (slug + ".pdf")
    dst = DELIVER / (slug + ".pdf")
    kb = len(src.read_bytes()) // 1024
    if PLAN:
        print("  plan   funnel/deliver/pdfs/%s.pdf (%d KB)" % (slug, kb))
    elif dst.exists() and dst.read_bytes() == src.read_bytes():
        print("  same   funnel/deliver/pdfs/%s.pdf" % slug)
    else:
        DELIVER.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        print("  wrote  funnel/deliver/pdfs/%s.pdf (%d KB)" % (slug, kb))

# ------------------------------------------------------------------ 3 offers
print("\n3 offers")
OFF = ROOT / "funnel/lib/offers.js"
off = OFF.read_text(encoding="utf-8")
keys = [SPORT_KEY.get(s) or CFG[s].get("sport_key") or s for s in GOT]
if len(set(keys)) != len(keys):
    fails.append("offers: two written books want the same Sport Pack key: %s" % keys)
for needle, rep in ((r"export const SPORTS=\[[^\]]*\];",
                     "export const SPORTS=[%s];" % ",".join("'%s'" % k for k in keys)),
                    (r"const SPORT_BOOK=\{[^}]*\};",
                     "const SPORT_BOOK={%s};" % ",".join("'%s':'%s'" % kv for kv in zip(keys, GOT)))):
    off, n = re.subn(needle, rep, off, count=1)
    if not n:
        fails.append("offers.js: no line matched %s" % needle[:28])
print("  the Sport Pack can now be pointed at %d books" % len(GOT))
write(OFF, off)

# ------------------------------------------------------------------ 4 store page
print("\n4 store page")
store = SITE / "playbooks/index.html"
t = store.read_text(encoding="utf-8")
head, rest = t.split("<main", 1)
main_open, tail = rest.split("</main>", 1)
have = tiles_in(main_open)


def tile(slug):
    """A new book is built from its config. A book already on the page keeps its
    words, and the catalogue keeps its price and its page count."""
    if slug in NEW:
        return cell(slug)
    old = have.get(slug)
    if not old:
        fails.append("store: %s should be on the page and is not, and has no new-book config here" % slug)
        return ""
    old = re.sub(r"<b>\d+ pages</b>", "<b>%d pages</b>" % BOOKS[slug]["pages"], old)
    return shelf_state(old, slug)


craft = []
for slug, c in have.items():
    if slug in GOT or slug in STORE["retired"]:
        continue
    if slug in BOOKS:
        c = shelf_state(c, slug)
    craft.append(c)
bundles = re.search(r'<section class="pb-bund".*?</section>', main_open, re.S).group(0)
unfinished = [s for s in ("offer-and-signing", "camp-roi")
                if BOOKS.get(s, {}).get("status") != "WRITTEN"]
bundles = re.sub(r"(?:one of the )(?:four|eight|five|six|seven) (?:written|finished) sport playbooks",
                 "one of the %d finished sport playbooks" % len(GOT), bundles)
if bundles != re.search(r'<section class="pb-bund".*?</section>', main_open, re.S).group(0):
    print("  the Sport Pack counts the finished books on the shelf")
if unfinished:
    bundles = bundles.replace(
        "Eligibility + Offers &amp; Signing + Camp ROI)",
        "Eligibility + Offers &amp; Signing + Camp ROI, the last two still being written)")
    print("  the Sport Pack names the two titles that are not written yet")


def cfg_pend_cell(slug):
    """A sport with a config but no printed PDF yet: on the page, greyed, no price."""
    c = CFG[slug]
    return pend_cell((c["sport_page"], c["ring_label"].replace("&", "&amp;"),
                      c["title"].replace("&", "&amp;"), who_label(c), c["pending_line"]))


soon = [s for s in STORE["written_order"] if s in CFG and s not in GOT]
pending_tiles = [cfg_pend_cell(s) for s in soon] + [pend_cell(p) for p in STORE["pending"]]
checked = BOOKS[GOT[0]]["rules_checked"]
main = ['<main class="cb-page"><p class="lab">Playbooks</p>'
        '<h1 class="d1">Run recruiting yourself, with the rules in hand.</h1>'
        '<p class="lede">%s</p>' % STORE["intro_written"],
        '<h2 class="d2">Ready now: %d sport playbooks</h2>' % len(GOT),
        "<p>Each one is a whole book, not a checklist. A sport playbook is $%d. Rules checked %s "
        "against the NCAA rule text and the printed calendars.</p>" % (PRICE, checked),
        '<div class="pb-grid">' + "".join(tile(s) for s in GOT) + "</div>",
        '<h2 class="d2">Every sport: the books that are not about one sport</h2>',
        "<p>%s</p>" % STORE["cross_note"],
        '<div class="pb-grid">' + "".join(craft) + "</div>",
        '<h2 class="d2">Sports still being written</h2>',
        "<p>%s</p>" % STORE["pending_note"],
        '<div class="pb-grid">' + "".join(pending_tiles) + "</div>",
        bundles + "</main>"]
new_store = head + "".join(main) + tail
desc = STORE["desc"] % len(GOT) if "%d" in STORE["desc"] else STORE["desc"]
new_store = re.sub(r'<meta name="description" content="[^"]*">',
                   '<meta name="description" content="%s">' % desc, new_store, count=1)
new_store = re.sub(r'(<meta (?:property|name)="(?:og|twitter):description" content=")[^"]*(">)',
                   r"\g<1>%s\g<2>" % desc, new_store)
write(store, new_store)
print("  %d written sport tiles, %d cross-sport tiles, %d pending sports (%d of them configured)"
      % (len(GOT), len(craft), len(pending_tiles), len(soon)))
if len(craft) != 9:
    fails.append("store: carried %d cross-sport tiles, the page has had 9" % len(craft))

# ------------------------------------------------------------------ 5 product pages
print("\n5 product pages")
pdp_src = (SITE / "playbooks/football-junior-year/index.html").read_text(encoding="utf-8")
NAV_HEAD = pdp_src[: pdp_src.find("<main")]
NAV_FOOT = pdp_src[pdp_src.find("</main>"):]


def pdp(slug):
    c, b = CFG[slug], BOOKS[slug]
    links = sources_of(slug)
    d = " ".join(b["outcome"].split())
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
                c["ring_label"].replace("&", "&amp;"), tile_claim(c, b["pages"]),
                c["title"].replace("&", "&amp;"), b["price_usd"], d, who_label(c).lower(),
                b["levels"].replace(" \u00b7 ", ", "), b["rules_checked"], slug, slug, slug,
                "".join("<li>%s</li>" % x for x in b["toc"]),
                "".join("<li>%s</li>" % x for x in b["tools"]),
                '<li><a href="/sports/%s">%s playbooks</a></li>' % (c["sport_page"], c["ring_label"]))]
    docs = re.sub(r'^[^,]+,\s*against\s+', '', str(c["rules_checked"]))
    body.append('<section class="src-list" id="sources"><h2>Where these dates come from</h2>'
                '<p class="note">Built from %s. Levels covered: %s.</p><ul>%s</ul>'
                '<p class="note">The book ends with the documents behind every date, and a list of '
                "what we could not settle. Dates worked out from the rule text instead of read off a "
                'page are marked PROJECTED inside it.</p></section>' % (
                    docs if docs != str(c["rules_checked"]) else 'the rule text checked %s' % c["rules_checked"],
                    b["levels"].replace(" \u00b7 ", ", "),
                    "".join('<li><a href="%s" rel="noopener">%s</a></li>' % (u, l) if u else "<li>%s</li>" % l
                            for u, l in links)))
    page = NAV_HEAD + "".join(body) + NAV_FOOT
    title = c["title"].replace("&", "&amp;")
    for pat, rep in ((r"<title>[^<]*</title>", "<title>%s | The Commit Book</title>" % title),
                     (r'(<meta property="og:title" content=")[^"]*(">)',
                      r"\g<1>%s | The Commit Book\g<2>" % title),
                     (r'(<meta name="twitter:title" content=")[^"]*(">)',
                      r"\g<1>%s | The Commit Book\g<2>" % title),
                     (r'(<meta (?:property|name)="(?:og|twitter):description" content=")[^"]*(">)',
                      r"\g<1>%s\g<2>" % d),
                     (r'(<meta name="description" content=")[^"]*(">)', r"\g<1>%s\g<2>" % d),
                     (r'<link rel="canonical" href="[^"]*">',
                      '<link rel="canonical" href="https://recruiting-calendar.vercel.app/playbooks/%s/">' % slug)):
        page, n = re.subn(pat, rep, page, count=1)
        if not n:
            fails.append("%s: the product page template has no %s" % (slug, pat[:30]))
    if len(links) < 3:
        fails.append("%s: only %d sources named for the product page" % (slug, len(links)))
    write(SITE / "playbooks" / slug / "index.html", page)


for slug in NEW:
    pdp(slug)

# ----------------------------------------------------- 5b a book already on the shelf keeps
# its words, but a price change has to reach its own page too, or the store and the page
# tell the customer two numbers.
if repriced and not PLAN:
    print("\n5b prices")
    for slug in repriced:
        f = SITE / "playbooks" / slug / "index.html"
        if not f.exists():
            continue
        t = f.read_text(encoding="utf-8")
        t2 = t.replace("$19", "$%d" % PRICE)
        if t2 != t:
            write(f, t2)
            print("  %s product page now says $%d" % (slug, PRICE))

# ------------------------------------------------------------------ 6 sport pages
print("\n6 sport pages")
per_page = {}
for s in NEW:
    per_page.setdefault(CFG[s]["sport_page"], []).append(s)
for page, slugs in sorted(per_page.items()):
    p = SITE / "sports" / page / "index.html"
    if not p.exists():
        fails.append("no sport page at /sports/%s" % page)
        continue
    t = p.read_text(encoding="utf-8")
    i = t.find('<div class="pb-grid">')
    if i < 0:
        fails.append("%s: no playbook grid to update" % p)
        continue
    a, b = grid_span(t, i)
    # Rebuild the grid by key, not by appending. A run that appends gives a book a second
    # tile every time the script is run, and this script is run more than once a sitting.
    keep = cells_by_slug(t[a:b])
    for slug in slugs + list(keep):
        if slug in keep and (slug in slugs or keep[slug].find("is-pend") >= 0):
            del keep[slug]
    t = (t[:a] + '<div class="pb-grid">' + "".join(cell(slug) for slug in slugs)
         + "".join(keep.values()) + '</div>' + t[b:])
    for drop in re.findall(r'<p class="pb-soon">.*?</p>', t, re.S):
        if page in drop or "playbook" in drop:
            t = t.replace(drop, "")
    # A sport page that now carries a dated book may not still tell the reader that no
    # dated calendar exists for its sport. The calendar tool is what is missing; the book
    # carries the dates, chapter by chapter, each with its bylaw.
    dated = [s for s in slugs if BOOKS[s]["status"] == "WRITTEN"]
    if dated:
        s0 = dated[0]
        say = ('<p>The %s playbook carries this sport\u2019s 2026-27 dates chapter by chapter, each '
               'one beside the rule that sets it. A calendar tool that answers &ldquo;what do I do '
               'this month&rdquo; for one athlete is not live yet. <a href="/playbooks/%s/">Read '
               'the book</a>.</p>' % (CFG[s0]["ring_label"].lower(), s0))
        t = re.sub(r'<p>No dated calendar for this sport yet\..*?</p>', say, t, count=1, flags=re.S)
    write(p, t)
    print("  /sports/%s carries %s" % (page, " then ".join(CFG[s]["ring_label"] for s in slugs)))

# ------------------------------------------------------------------ 7 ring
print("\n7 ring")
SJ = SITE / "assets/stories.js"
sj = SJ.read_text(encoding="utf-8")
pre, rest = sj.split("window.STORY_ALL=", 1)
DATA, end = json.JSONDecoder().raw_decode(rest)
recs = {a["id"]: a for a in DATA["athletes"]}
for old, new in STORE.get("rename", {}).items():
    """A pending card gives up its id and first name so a written book can take them.
    This is a one-time move. Once the name is taken, and for as long as the old card
    carries a sold book, the pass must leave the pair alone, or the second run renames
    the live card into the pending slot and the shelf loses a sport."""
    if old not in recs or new.lower() in recs or recs[old].get("book"):
        continue
    r = recs.pop(old)
    r["id"] = new.lower()
    for f in ("name", "short", "label", "poster"):
        r[f] = new
    r.pop("book", None)
    # A card's figure is named for the athlete on the card, so a renamed card takes the
    # new file when the repo has it, and keeps the old one when it does not.
    _new = "/assets/media/cut-%s-640.webp" % new.lower()
    if (SITE / _new[1:]).exists():
        r["img"] = _new + "?v=00000000"
    else:
        fails.append("rename to %s has no figure at %s" % (new, _new))
    r["moved_from"] = old
    recs[r["id"]] = r
    print("  pending card %s is now %s" % (old, r["id"]))
for _id, (_slug, _label, _page) in STORE.get("live_books", {}).items():
    r = recs.get(_id)
    if r is not None and r.get("moved_from"):
        # This is the athlete who gave the name up, not the one who took it. Stamping the
        # new sport on it hid the lacrosse card: the ring prints one card per name, so a
        # lacrosse card wearing Women's Soccer reads as the soccer card and is dropped.
        print("  card %-20s keeps its own sport (%s)" % (_id, r.get("sport")))
        continue
    if r is None:
        fails.append("ring: the live book %s names a card that does not exist: %s" % (_slug, _id))
        continue
    r.update({"sport": _label, "book": _slug, "ring_page": "/sports/%s" % _page})
    r["playbooks"] = shelf_list(_slug, r.get("playbooks", []))
    print("  card %-20s %-18s live    keeping its own figure" % (_id, _label))

def art_of(c, r):
    """Which figure a card shows: the config may name one, else the template's own
    name, else whatever the card already pointed at. Only a file on disk counts."""
    for a in (c.get("art"), "/assets/media/cut-%s-640.webp" % c["athlete_id"],
              re.sub(r"\?.*$", "", str((r or {}).get("img", "")))):
        if a and a.startswith("/assets/media/") and (SITE / a[1:]).exists():
            return a
    return c.get("art") or "/assets/media/cut-%s-640.webp" % c["athlete_id"]


for slug in [s for s in STORE["written_order"] if s in CFG]:
    c, live = CFG[slug], slug in GOT
    r = recs.get(c["athlete_id"])
    if r is None:
        r = {"id": c["athlete_id"], "composite": True, "art_fictional": True, "page": False,
             "playbooks": ["eligibility-2-hard-deadlines", "offer-and-signing"], "hold": False}
        recs[c["athlete_id"]] = r
        print("  new card for %s" % c["athlete_id"])
    r.update({"name": c["athlete"], "short": c["athlete"], "label": c["athlete"],
              "poster": c["athlete"], "sport": c["ring_label"],
              "ring_page": "/sports/%s" % c["sport_page"]})
    art = "" if c.get("art") == "" else art_of(c, r)
    if live:
        r["book"] = slug
        if not art:
            # An empty art field in the config is a decision, not an oversight: the card
            # draws the ring silhouette and the cover draws the crest. It has to be written down.
            if not c.get("art_note"):
                fails.append("%s: no figure and no art_note saying why" % slug)
            else:
                print("  warn %-20s no figure yet: the card draws the ring silhouette" % slug)
        elif not (SITE / art[1:]).exists():
            fails.append("%s: a live card needs its own figure, and %s is not in the repo" % (slug, art))
    else:
        r.pop("book", None)
        if art and not (SITE / art[1:]).exists():
            # A grey card keeps whatever it drew before, and a new one draws the
            # ring's own silhouette rather than a broken image.
            art = str(r.get("img") or "").split("?")[0]
    r["img"] = (art + "?v=00000000") if art else ""
    r["playbooks"] = shelf_list(slug if live else "", r.get("playbooks", []))
    print("  card %-20s %-18s %-7s figure %s" % (c["athlete_id"], c["ring_label"],
          "live" if live else "pending", art.split("/")[-1]))

missing = [i for i in STORE["ring_ids"] if i not in recs]
extra = [r["id"] for r in recs.values() if r["id"] not in STORE["ring_ids"]]
if missing:
    fails.append("ring: STORE.json orders ids with no record: %s" % ", ".join(missing))
if extra:
    fails.append("ring: records missing from the STORE.json order: %s" % ", ".join(extra))
if not (missing or extra):
    if len(STORE["ring_ids"]) != len(recs):
        fails.append("ring: STORE.json names %d cards, the file holds %d" % (
            len(STORE["ring_ids"]), len(recs)))
    # The ring prints one card per name on the front row. A card that wears the same
    # sport as a front-row card is dropped by the page, so the shelf loses a figure
    # silently. Two live books for one name is the same fault in the other direction.
    front = set(STORE["ring_ids"][:4])
    byname, bysport = {}, {}
    for i in STORE["ring_ids"]:
        r = recs[i]
        for bad, table, what in ((r.get("label"), byname, "name"), (r.get("sport"), bysport, "sport")):
            # The ring prints one card per name on the front row, and the page keys that
            # row by the name on the card. Two cards wearing one name or one sport means
            # the shelf quietly loses a figure, so it is a failure, not a note.
            if bad in table:
                fails.append("ring: %s and %s both carry the %s %s, so the page shows one card, not two"
                             % (table[bad], i, what, bad))
            table.setdefault(bad, i)
    for _s in STORE["written_order"]:
        if _s not in GOT:
            continue
        _b = BOOKS[_s]
        # The catalogue the ring and the phone deck read is the same rows the store page
        # is built from, so a book with no config in this lane (the shipped volleyball
        # book) is as sellable here as one written this week.
        DATA["playbooks"][_s] = {"title": _b["title"], "price": _b["price_usd"],
                                 "type": "Playbook", "who": _b["who"],
                                 "outcome": _b["outcome"], "toc": _b["toc"],
                                 "status": "WRITTEN"}
        print("  catalogue %s $%d" % (_s, _b["price_usd"]))
    DATA["athletes"] = [{k: v for k, v in recs[i].items() if k != "moved_from"}
                        for i in STORE["ring_ids"]]
    write(SJ, pre + "window.STORY_ALL="
         + json.dumps(DATA, separators=(", ", ": "), ensure_ascii=False) + rest[end:])
    RJ = SITE / "assets/ring.js"
    rj = RJ.read_text(encoding="utf-8")
    # Both of these leave their own search text in the file, so an unguarded
    # builder stamps another copy of the clause on every single build. That is
    # how one line of ring.js ended up with thirteen copies of itself.
    if "function SPORT_PATH(a){if(a.ring_page)" not in rj:
        rj = rj.replace("function SPORT_PATH(a){",
                        "function SPORT_PATH(a){if(a.ring_page)return a.ring_page;", 1)
    if "builtInfoLegacy" not in rj:
        rj = rj.replace("function builtInfo(a){",
                        "function builtInfo(a){if(a.book){return{built:true,label:a.sport}}"
                        "return builtInfoLegacy(a)}\nfunction builtInfoLegacy(a){", 1)
    rj = re.sub(r"var FRONT_IDS=\[[^\]]*\];", 'var FRONT_IDS=[%s];'
                % ",".join('"%s"' % i for i in STORE["ring_ids"][:4]), rj, count=1)
    rj = re.sub(r"// The four written playbooks lead the ring[^\n]*(?:\n//[^\n]*)*",
                "// The written playbooks lead the ring, in the order STORE.json gives. A card is\n"
                "// greyed, stamped PENDING and inert to clicks while its record carries no book field.",
                rj, count=1)
    for needle in ("a.ring_page", "builtInfoLegacy", "a.book"):
        if needle not in rj:
            fails.append("ring.js: the %s patch did not land" % needle)
    write(RJ, rj)

# ------------------------------------------------------------------ 8 redirects
print("\n8 redirects")
VJ = ROOT / "vercel.json"
vj = VJ.read_text(encoding="utf-8")
have_r = set(re.findall(r'"source"\s*:\s*"([^"]*)"', vj))
add = []
for s, rep in STORE["retired"].items():
    for tail_ in ("", "/"):
        src, dst = "/playbooks/%s%s" % (s, tail_), "/playbooks/%s%s" % (rep, tail_)
        if src in have_r:
            vj = re.sub(r'("source"\s*:\s*"%s"\s*,\s*"destination"\s*:\s*)"[^"]*"' % re.escape(src),
                        r'\1"%s"' % dst, vj)
            print("  301 %s -> %s (already listed, destination updated)" % (src, dst))
        else:
            add.append(json.dumps({"source": src, "destination": dst, "permanent": True}))
if add:
    m = re.search(r'"redirects"\s*:\s*\[', vj)
    if not m:
        fails.append("vercel.json: no redirects array")
    else:
        vj = vj[:m.end()] + "\n    " + ",\n    ".join(add) + "," + vj[m.end():]
        for a in add:
            print("  301 %s" % json.loads(a)["source"])
write(VJ, vj)

# ------------------------------------------------------------------ 9 sitemap
print("\n9 sitemap")
SM = SITE / "sitemap.xml"
sm = SM.read_text(encoding="utf-8")
for s in STORE["retired"]:
    sm = re.sub(r"\s*<url>\s*<loc>[^<]*/playbooks/%s/?</loc>[^<]*(?:<lastmod>[^<]*</lastmod>)?\s*</url>" % s,
                "", sm)
add = [s for s in NEW if "/playbooks/%s/" % s not in sm]
sm = sm.replace("</urlset>", "".join(
    '<url><loc>https://recruiting-calendar.vercel.app/playbooks/%s/</loc>'
    '<lastmod>%s</lastmod></url>' % (s, DAY) for s in add) + "\n</urlset>")
write(SM, sm)
print("  %d new urls, %d in the file" % (len(add), sm.count("<loc>")))

# ------------------------------------------------------------------ 10 cache keys
print("\n10 cache keys")
def rekey():
    """Point every ?v= at the bytes now on disk. Repeat until nothing changes: an asset
    that carries keyed references of its own changes hash when it is re-pointed."""
    KEYS = {}
    for base in (SITE, ROOT / "funnel"):
        for p_ in base.rglob("*"):
            if p_.is_file() and p_.suffix.lower() in (".html", ".js", ".css", ".json", ".svg",
                                                      ".webp", ".png", ".jpg", ".woff2", ".xml",
                                                      ".txt", ".pdf"):
                KEYS["/" + str(p_.relative_to(base)).replace(chr(92), "/")] = key_of(p_)
    return KEYS


def lookup(url, page_dir, KEYS):
    for cand in (url if url.startswith("/") else "/" + url,
                 "/" + str(pathlib.PurePosixPath(page_dir, url)).replace(chr(92), "/").lstrip("/")):
        norm = re.sub(r"/{2,}", "/", pathlib.PurePosixPath(cand).as_posix())
        if norm in KEYS:
            return KEYS[norm]
    return None


changed = 0
for _round in range(4):
    KEYS = rekey()
    moved = 0

    def fix(m, rel_dir="", KEYS=KEYS):
        global changed, moved
        k = lookup(m.group(1), rel_dir, KEYS)
        if k is None or k == m.group(2):
            return m.group(0)
        moved += 1
        return "%s?v=%s" % (m.group(1), k)

    for p_ in list(SITE.rglob("*.html")) + list(SITE.rglob("*.js")) + [OFF]:
        if not p_.exists():
            continue
        rel_dir = "" if SITE not in p_.parents else str(p_.parent.relative_to(SITE)).replace(chr(92), "/")
        t0 = p_.read_text(encoding="utf-8")
        t1 = _KEYRX.sub(lambda m, rd=rel_dir: fix(m, rd, KEYS), t0)
        if t1 != t0:
            write(p_, t1)
    changed += moved
    if not moved:
        break

print("\n" + "=" * 78)
for s in skips:
    print("SKIP  " + s)
if fails:
    for f in fails:
        print("FAIL  " + f)
    print("%d failures. The store does not change until they are fixed." % len(fails))
    sys.exit(1)
print("site pass clean. Next: python gate.py, then look at it in a browser.")
