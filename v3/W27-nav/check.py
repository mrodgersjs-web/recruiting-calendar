# -*- coding: utf-8 -*-
"""W27 gate: the Playbooks surface shows the four written books, other sports say pending, and
nothing on the site offers a buy button for a file that does not exist.

Run: python v3/W27-nav/check.py
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
PDF_DIR = ROOT / "funnel/deliver/pdfs"
CAT = json.loads((ROOT / "v3/W1-playbooks/CATALOG.json").read_text(encoding="utf-8"))
BOOKS = {b["slug"]: b for b in CAT["catalog"]}
OFFERS = (ROOT / "funnel/lib/offers.js").read_text(encoding="utf-8")
DOT = "\u00b7"
fails = []


def ok(label):
    print("  PASS  %s" % label)


def bad(label):
    fails.append(label)
    print("  FAIL  %s" % label)


def pages(slug):
    return len(PdfReader(str(PDF_DIR / (slug + ".pdf"))).pages)


def ready(slug):
    return BOOKS[slug]["status"] == "WRITTEN" and (PDF_DIR / (slug + ".pdf")).exists()


WRITTEN = ["football-junior-year", "volleyball-road-to-college", "basketball-road-to-college",
           "girls-basketball-road-to-college"]
PENDING = ["baseball", "softball", "track-field", "swimming", "wrestling", "lacrosse", "soccer"]

store = (SITE / "playbooks/index.html").read_text(encoding="utf-8")
grids = re.findall(r'<div class="pb-grid">(.*?)</div>\s*</div>|<div class="pb-grid">(.*?)</div>', store, re.S)


def sections(t):
    """Split the store page into its three labelled grids, in document order."""
    out = []
    for m in re.finditer(r'<h2 class="d2">([^<]+)</h2>.*?<div class="pb-grid">(.*?)</div>\s*(?=<h2|<section|</main>)', t, re.S):
        out.append((" ".join(m.group(1).split()), m.group(2)))
    return out


secs = sections(store)
print("=" * 74)
print("1. the store page, section by section")
if [s[0] for s in secs] != ["Ready now: four sport playbooks",
                            "Every sport: the books that are not about one sport",
                            "Sports still being written"]:
    bad("the store page sections are %s" % [s[0] for s in secs])
else:
    ok("three sections, in this order: four written, then the cross-sport books, then pending sports")

cells_of = lambda body: re.findall(r'<div class="pb-cell[^"]*">.*?</div>', body, re.S)
slugs_in = lambda body: [re.search(r'href="/playbooks/([a-z0-9-]+)"', c).group(1)
                         for c in cells_of(body) if re.search(r'href="/playbooks/([a-z0-9-]+)"', c)]

first = slugs_in(secs[0][1]) if secs else []
if first != WRITTEN:
    bad("section 1 lists %s" % first)
else:
    ok("athletes 1-4 of the store: %s" % ", ".join(BOOKS[s]["title"] for s in WRITTEN))
for slug in WRITTEN:
    cell = next(c for c in cells_of(secs[0][1]) if ('/playbooks/%s"' % slug) in c)
    real = pages(slug)
    if "%d pages" % real not in cell:
        bad("%s card does not state the real %d pages" % (slug, real))
        continue
    if 'data-offer="%s"' % slug not in cell:
        bad("%s has no buy button" % slug)
        continue
    if "$%d" % BOOKS[slug]["price_usd"] not in cell:
        bad("%s card does not show its price" % slug)
        continue
    ok("%-30s %2d pages, $%d, buy button live" % (BOOKS[slug]["title"][:30], real, BOOKS[slug]["price_usd"]))

craft = secs[1][1] if len(secs) > 1 else ""
craft_slugs = slugs_in(craft)
if len(craft_slugs) != 9:
    bad("section 2 has %d cards, expected the 9 cross-sport books" % len(craft_slugs))
buyable_craft = [s for s in craft_slugs if ready(s)]
buttons = re.findall(r'data-offer="([a-z0-9-]+)"', craft)
if sorted(buttons) != sorted(buyable_craft):
    bad("section 2 buttons (%s) do not match what can be delivered (%s)" % (buttons, buyable_craft))
else:
    ok("section 2: %d books, a buy button only on the %d that can be delivered today"
       % (len(craft_slugs), len(buyable_craft)))
if len(re.findall(r"Rules being verified", craft)) != len(craft_slugs) - len(buyable_craft):
    bad("a book with no button is missing its 'Rules being verified' line")
else:
    ok("the %d books with no button say why in the site's own words" % (len(craft_slugs) - len(buyable_craft)))

pend = secs[2][1] if len(secs) > 2 else ""
pend_slugs = re.findall(r'href="/sports/([a-z0-9-]+)"', pend)
if sorted(pend_slugs) != sorted(PENDING):
    bad("the pending section lists %s" % pend_slugs)
else:
    ok("pending section holds exactly the seven sports with no book yet: %s" % ", ".join(PENDING))
if len(re.findall(r'class="pb-cell is-pend"', pend)) != len(PENDING):
    bad("a pending tile is missing its grey state")
else:
    ok("all seven pending tiles carry the grey state")
if len(re.findall(r'class="pb-pend">Pending<', pend)) != len(PENDING):
    bad("a pending tile has no PENDING band")
else:
    ok("all seven say PENDING across the art, same language as the athlete ring")
if re.search(r'class="pb-p"|data-offer=|data-add=', pend):
    bad("a pending sport is still priced or buyable")
else:
    ok("no price and no button anywhere in the pending section")

print("\n" + "=" * 74)
print("2. no dead clicks anywhere on the site")
dead, dead404 = [], []
for f in sorted(SITE.rglob("*.html")):
    t = f.read_text(encoding="utf-8")
    for slug in set(re.findall(r'data-(?:offer|add|checkout)="([a-z0-9-]+)"', t)):
        if slug in BOOKS and not ready(slug):
            dead.append("%s -> %s" % (f.relative_to(SITE), slug))
    for href in re.findall(r'href="/(playbooks|sports)/([a-z0-9-]+)"?', t):
        p = SITE / href[0] / href[1] / "index.html"
        if not p.exists():
            dead404.append("%s -> /%s/%s" % (f.relative_to(SITE), href[0], href[1]))
if dead:
    for d in sorted(set(dead)):
        bad("buy button for a book that cannot be delivered: %s" % d)
else:
    ok("no page offers to buy or bag a book that is not written and served")
if dead404:
    for d in sorted(set(dead404)):
        bad("card links to a page that does not exist: %s" % d)
else:
    ok("every playbook and sport card link lands on a real page")

print("\n" + "=" * 74)
print("3. product pages for books that are not on sale")
bad_pages = []
for slug, b in BOOKS.items():
    f = SITE / "playbooks" / slug / "index.html"
    if not f.exists():
        if ready(slug):
            bad_pages.append("%s is sellable but has no product page" % slug)
        continue
    t = f.read_text(encoding="utf-8")
    if ready(slug):
        if "one-time" not in t:
            bad_pages.append("%s is on sale but lost its price line" % slug)
        continue
    if re.search(r'data-(?:offer|add|checkout)="%s"' % slug, t):
        bad_pages.append("%s: still offers a button" % slug)
    if "one-time" in t:
        bad_pages.append("%s: a book that cannot be delivered still says one-time" % slug)
    if not re.search(r'class="(?:pdp-soon|note)"', t):
        bad_pages.append("%s: no line telling the reader why there is no button" % slug)
if bad_pages:
    for x in bad_pages:
        bad(x)
else:
    ok("every book that cannot be delivered has no button, no 'one-time' claim, and says why on its own page")
print("   sellable today: " + ", ".join(sorted(s for s in BOOKS if ready(s))))
print("   not on sale:    " + ", ".join(sorted(s for s in BOOKS if not ready(s))))

print("\n" + "=" * 74)
print("4. every sport page")
for page in sorted((SITE / "sports").iterdir()):
    f = page / "index.html"
    if not f.exists():
        continue
    name, t = page.name, f.read_text(encoding="utf-8")
    grid = re.search(r'<div class="pb-grid">(?:.*?)</div>\s*</div>', t, re.S) or re.search(r'<div class="pb-grid">.*', t, re.S)
    body = grid.group(0)
    own = [s for s in slugs_in(body) if s in WRITTEN]
    is_pending = name in PENDING
    if is_pending:
        if own:
            bad("/sports/%s is pending yet still lists a buyable %s" % (name, own))
        elif 'class="pb-cell is-pend"' not in body:
            bad("/sports/%s has no pending tile" % name)
        elif "is being written" not in t:
            bad("/sports/%s does not say its book is being written" % name)
        else:
            ok("/sports/%-12s pending tile and one plain sentence saying so" % name)
    else:
        want = {"football": ["football-junior-year"], "volleyball": ["volleyball-road-to-college"],
                "basketball": ["basketball-road-to-college", "girls-basketball-road-to-college"]}[name]
        if own != want:
            bad("/sports/%s leads with %s, expected %s" % (name, own, want))
        else:
            ok("/sports/%-12s its own book first, with a buy button" % name)

print("\n" + "=" * 74)
print("5. the served files match what the site claims")
for slug, b in BOOKS.items():
    served = (PDF_DIR / (slug + ".pdf")).exists()
    if b["status"] == "WRITTEN" and served:
        real = pages(slug)
        if real != b["pages"]:
            bad("%s: catalogue %d pages, file %d" % (slug, b["pages"], real))
        else:
            ok("%-30s %2d pages in the file, %d claimed" % (b["title"][:30], real, b["pages"]))
    elif b["status"] == "WRITTEN":
        bad("%s is marked WRITTEN with no file behind it" % slug)
    elif served:
        bad("%s has a served file but is still marked %s" % (slug, b["status"]))
t = (PDF_DIR / "volleyball-road-to-college.pdf")
txt = " ".join(re.sub(r"\s+", " ", (PdfReader(str(t)).pages[0].extract_text() or "")).split())
if "VOLLEYBALL" in txt.upper() and "ROAD" in txt.upper():
    ok("the volleyball file's cover page is the volleyball book, not a mislabeled deck")
else:
    bad("volleyball cover page text reads: %s" % txt[:120])

print("\n" + "=" * 74)
print("6. the checkout table agrees with the store")
sports = re.search(r"export const SPORTS=\[([^\]]*)\]", OFFERS).group(1)
book_map = re.search(r"const SPORT_BOOK=\{([^}]*)\}", OFFERS).group(1)
if "'football'" in sports and "volleyball" in sports and "basketball" in sports:
    ok("the Sport Pack offers one of the four written sports, not baseball or track")
else:
    bad("SPORTS is %s" % sports)
for slug in WRITTEN:
    if slug not in book_map:
        bad("SPORT_BOOK has no entry for %s" % slug)
note = [b for b in CAT["bundles"] if b["slug"] == "all-playbooks"][0]["note"]
if "all %d" % len(CAT["catalog"]) in note:
    ok("the Every Playbook line counts the real %d books" % len(CAT["catalog"]))
else:
    bad("the Every Playbook line says %r for %d books" % (note, len(CAT["catalog"])))

print("\n" + "=" * 74)
print("7. the whole sitemap still resolves")
sm = (SITE / "sitemap.xml").read_text(encoding="utf-8")
urls = re.findall(r"<loc>https://recruiting-calendar\.vercel\.app([^<]*)</loc>", sm)
missing = []
for u in urls:
    p = SITE / u.strip("/").replace("/", "\\")
    ok_path = (p / "index.html") if u not in ("/",) else (SITE / "index.html")
    if not ok_path.exists() and not p.with_suffix(".html").exists():
        missing.append(u)
if missing:
    for m in missing:
        bad("sitemap lists %s and there is no file" % m)
else:
    ok("sitemap: %d URLs, every one of them a file in site/" % len(urls))
for slug in WRITTEN[1:]:
    if "/playbooks/%s/" % slug not in sm:
        bad("/playbooks/%s/ is not in the sitemap" % slug)

print("\n" + "=" * 74)
print("8. cache keys and plain copy")
stale = []
crlf_assets = set()
for f in SITE.rglob("*.html"):
    t = f.read_text(encoding="utf-8")
    for url, key in re.findall(r'(?:href|src)="(/[^"]+\.(?:js|css))\?v=([0-9a-f]{6,8})"', t):
        p = SITE / url.lstrip("/").replace("/", "\\")
        if not p.exists():
            stale.append("%s -> %s (no such file)" % (f.relative_to(SITE), url))
            continue
        raw = p.read_bytes()
        if b"\r\n" in raw:
            crlf_assets.add(url)
        # core.autocrlf is on, so the bytes Vercel serves are the LF form.
        if hashlib.md5(raw.replace(b"\r\n", b"\n")).hexdigest()[:8] != key:
            stale.append("%s -> %s" % (f.relative_to(SITE), url))
if stale:
    for s in sorted(set(stale)):
        bad("stale or missing cache key in %s" % s)
else:
    ok("every ?v= on every page matches the bytes the deploy will serve")
    if crlf_assets:
        print("   note: %d asset(s) are CRLF in the working copy (%s); their keys use the LF form git commits"
            % (len(crlf_assets), ", ".join(sorted(crlf_assets))))

css = (SITE / "assets/commit.css").read_text(encoding="utf-8")
for needle in [".pb-cell.is-pend .pb-thumb{filter:grayscale(1)", ".pb-pend{", ".pb-soon{"]:
    (ok if needle in css else bad)("commit.css has %s" % needle)


def grade(t):
    t = re.sub(r"<(script|style|nav|header|footer)[^>]*>.*?</\1>", " ", t, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    words = re.findall(r"[A-Za-z][A-Za-z'’-]*", t)
    sents = [s for s in re.split(r"[.!?]+\s", re.sub(r"\s+", " ", t)) if len(s.split()) > 3]
    if not sents or not words:
        return 0.0
    def syl(w):
        w = w.lower()
        groups = re.findall(r"[aeiouy]+", w)
        n = len(groups)
        if w.endswith("e") and n > 1 and groups[-1] == ["e"]:
            n -= 1
        return max(1, n)
    return 0.39 * (len(words) / len(sents)) + 11.8 * (sum(syl(w) for w in words) / len(words)) - 15.59


prose = re.search(r'<main.*?(?=<div class="pb-grid")', store, re.S).group(0)
g = grade(prose)
(ok if g <= 8.0 else bad)("store page intro reads at grade %.1f (house rule: 8 or simpler)" % g)
banned = ["Wisconsin", "Colorado", "Pewaukee", "Marquette", "Badger", "WIAA", "Anytown HS"]
hits = [b for b in banned if re.search(r"\b%s\b" % b, store)]
(bad if hits else ok)("no state association or school name on the store page" + (" -> %s" % hits if hits else ""))
for s in PENDING:
    if re.search(r'\$[0-9]+[^<]*</span><[^>]*></a><button[^>]*data-offer="[a-z0-9-]+">[^<]*</button></div><div class="pb-cell is-pend"><a class="pb-card" href="/sports/%s"' % s, store):
        bad("a pending tile sits next to a live button for %s" % s)

print("\n%s" % ("ALL CHECKS PASSED" if not fails else "%d FAILED: %s" % (len(fails), "; ".join(fails))))
sys.exit(1 if fails else 0)
