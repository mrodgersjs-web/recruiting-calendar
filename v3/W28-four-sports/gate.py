"""gate.py — the whole template's gate, in one command. (W28, 11 Nov 2026)

    python gate.py                  every book the template knows about, plus the shop
    python gate.py <slug> ...       those books, plus the shop
    python gate.py --shop           the shop only

Three parts per book: the lint that builds the deck (`deck.py`), the printed book
(`printcheck.py`), the evidence behind every date and number (`factcheck.py`). Then
fifteen checks on the shop itself, because a correct book behind a wrong price tab is
still a wrong shop. Run it from `v3/W28-four-sports`.

Written so that nobody has to remember the list. A FAIL here means the template was
not followed, not that the taste of the reviewer differs.
"""
import contextlib
import hashlib
import io
import json
import pathlib
import re
import subprocess
import sys

try:
    from pypdf import PdfReader
except ImportError:
    from PyPDF2 import PdfReader

import readability

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SITE = ROOT / "site"
SHOP = SITE / "playbooks"
Q = chr(34)
STORE = json.loads((HERE / "STORE.json").read_text(encoding="utf-8"))
CAT = json.loads((ROOT / "v3/W1-playbooks/CATALOG.json").read_text(encoding="utf-8"))
BOOKS = {b["slug"]: b for b in CAT["catalog"]}
GRADE_RE = re.compile("grade level:\\s*([\\d.]+)")
WORDS_RE = re.compile("words:\\s*(\\d+)")
results = []


def record(name, ok, detail=""):
    results.append((name, bool(ok), detail))
    print("  %-4s %-52s %s" % ("PASS" if ok else "FAIL", name, detail))


def sh(*cmd):
    p = subprocess.run([sys.executable] + list(cmd), cwd=HERE, capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip()


def last(out, n=120):
    return out.splitlines()[-1][:n] if out else ""


def lf(t):
    return t.replace("\r\n", "\n").replace("\r", "\n")


def key_of(path):
    bs = path.read_bytes()
    if path.suffix.lower() in (".html", ".js", ".css", ".json", ".svg", ".txt", ".xml"):
        bs = lf(bs.decode("utf-8")).encode("utf-8")
    return hashlib.md5(bs).hexdigest()[:8]


def served(slug):
    return ROOT / "funnel/deliver/pdfs" / ("%s.pdf" % slug)


def pages_of(path):
    return len(PdfReader(str(path)).pages)


def grade_of(html_body):
    """Grade one block of customer copy through the house grader, not a second one."""
    tmp = HERE / ".gate-copy.html"
    tmp.write_text("<html><head><title>t</title></head><body><p>" + html_body +
                   "</p></body></html>", encoding="utf-8")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        readability.audit(str(tmp), "copy")
    tmp.unlink()
    out = buf.getvalue()
    g, w = GRADE_RE.search(out), WORDS_RE.search(out)
    return (float(g.group(1)) if g else None, int(w.group(1)) if w else 0)


def body(text):
    return re.sub("<[^>]+>", " ", " ".join(text.split()))


# ============================================================ A the template itself
print("\nA the template's own housekeeping")
kp = {}
for f in ("deck.py", "printcheck.py"):
    t = (HERE / f).read_text(encoding="utf-8")
    m = re.search("def keyphrase\\(title\\):\\n(?:\\s*(?:#[^\\n]*|" + Q * 3 + "[\\s\\S]*?" + Q * 3 +
                  ")\\n)*((?:\\s{4}[^\\n]*\\n)+)", t)
    kp[f] = re.sub("\\s+", "", m.group(1)) if m else ""
record("keyphrase() has not drifted between deck.py and printcheck.py",
       kp["deck.py"] == kp["printcheck.py"] != "",
       "" if kp["deck.py"] == kp["printcheck.py"] else "the two copies differ")

copies = list(ROOT.rglob("readability.py"))
here = hashlib.md5((HERE / "readability.py").read_bytes()).hexdigest()
other = [str(p.relative_to(ROOT)) for p in copies
         if hashlib.md5(p.read_bytes()).hexdigest() != here]
print("  info  this lane's grader is the one deck.py and gate.py call; %d older copies sit in other "
      "lanes and are not used here%s" % (len(other), (": " + ", ".join(other[:4])) if other else ""))

price = STORE["sport_price"]
record("the store sells every sport playbook at one price, $%d" % price,
       all(BOOKS[s]["price_usd"] == price for s in STORE["written_order"] if s in BOOKS),
       ", ".join("%s $%s" % (s, BOOKS[s]["price_usd"]) for s in STORE["written_order"]
                 if s in BOOKS and BOOKS[s]["price_usd"] != price))

# ============================================================ B each book
if "--shop" not in sys.argv:
    books = [a for a in sys.argv[1:] if not a.startswith("-")] or STORE["written_order"]
    for slug in books:
        cfg_p = HERE / "SPORTS" / (slug + ".json")
        if not cfg_p.exists():
            continue                        # shipped before the template existed
        print("\nB %s" % slug)
        cfg = json.loads(cfg_p.read_text(encoding="utf-8"))
        rc, out = sh("deck.py", slug)
        record("deck.py builds it and every lint passes", rc == 0, last(out))
        man = HERE / ("manifest-%s.json" % slug)
        if man.exists():
            m = json.loads(man.read_text(encoding="utf-8"))
            e = m.get("email", {})
            record("the customer text reads at grade 8 or under", float(m.get("grade", 99)) <= 8.0,
                   "grade %s" % m.get("grade"))
            record("the sample email is 160-195 words, subject 55-80 letters",
                   160 <= e.get("words", 0) <= 195 and 55 <= e.get("letters", 0) <= 80, json.dumps(e))
            record("the made-up copy is marked tmpl, so the fact gate can see it is not a claim",
                   'class="tmpl"' in (HERE / (slug + "-deck.html")).read_text(encoding="utf-8"), "")
            record("the book carries all %d chapters and every claim the editor insisted on"
                   % len(cfg.get("chapters", [])),
                   len(m.get("chapters", [])) == len(cfg.get("chapters", [])) and not m.get("misses"),
                   "%d chapters, %s" % (len(m.get("chapters", [])), m.get("misses") or "no gaps"))
        else:
            record("a manifest was written", False, str(man))
        rc, out = sh("printcheck.py", slug)
        record("the printed book obeys the house print rules", rc == 0, last(out, 110))
        rc, out = sh("factcheck.py", slug)
        record("every date, figure and rule traces to the packet", rc == 0, last(out, 110))
        pdf = HERE / "pdfs" / (slug + ".pdf")
        record("the deck has been printed into this lane", pdf.exists(), pdf.name)
        if pdf.exists() and slug in BOOKS:
            record("the catalogue's page count is the real one", BOOKS[slug].get("pages") == pages_of(pdf),
                   "catalogue %s, PDF %d" % (BOOKS[slug].get("pages"), pages_of(pdf)))

# ============================================================ C the shop
print("\nC the shop")
written = [s for s, b in BOOKS.items() if b["status"] == "WRITTEN"]

bad = [s for s in written if not served(s).exists()]
record("every WRITTEN product has a served PDF", not bad, ", ".join(bad))

bad = []
for s in written:
    if not served(s).exists():
        continue
    n = pages_of(served(s))
    if BOOKS[s].get("pages") != n:
        bad.append("%s claims %s pages, %d served" % (s, BOOKS[s].get("pages"), n))
    if s in STORE["written_order"] and BOOKS[s]["price_usd"] != price:
        bad.append("%s is $%s, the store says $%d" % (s, BOOKS[s]["price_usd"], price))
record("page counts and prices in the catalogue match the files", not bad, " | ".join(bad)[:170])

missing, lying, naked = [], [], []
SOON = ("not on sale yet", "gets a buy button when")
for s, b in BOOKS.items():
    page = SHOP / s / "index.html"
    if not page.exists():
        if b["status"] == "WRITTEN":
            missing.append(s)
        continue
    t = page.read_text(encoding="utf-8")
    btn = ("data-offer=" + Q + s + Q) in t or ("data-checkout=" + Q + s + Q) in t
    priced = ("$%d" % b["price_usd"]) in t
    soon = any(k in t for k in SOON)
    if served(s).exists():
        if not btn:
            naked.append(s)
        if not priced:
            lying.append("%s (a written book with no $%d on its own page)" % (s, b["price_usd"]))
        if soon:
            lying.append("%s (says it is not on sale, yet the PDF is served)" % s)
    else:
        if btn:
            lying.append("%s (a button on a book we cannot serve)" % s)
        elif priced and not soon:
            lying.append("%s (a price with no words saying it is only a plan)" % s)
record("every written book has a product page", not missing, ", ".join(missing))
record("each product page tells the truth about buying it", not lying, ", ".join(lying)[:200])
record("every deliverable book has its button", not naked, ", ".join(naked))

st = (SHOP / "index.html").read_text(encoding="utf-8")
cells = list(re.finditer('<div class="pb-cell( is-pend)?">.*?</div>', st, re.S))
pend = [m.group(0) for m in cells if m.group(1)]
live_n = len(cells) - len(pend)
have = [s for s in STORE["written_order"] if BOOKS.get(s, {}).get("status") == "WRITTEN"
        and served(s).exists()]
record("the store shows every written sport book", live_n >= len(have),
       "%d live tiles, %d books to sell" % (live_n, len(have)))
bad = [re.sub("<[^>]+>", " ", b)[:70] for b in pend
       if re.search("class=" + Q + "(pb-price|pb-p)" + Q + "|[$]|data-offer|data-checkout", b)]
record("a pending tile carries no price and no button", not bad, str(bad[:2]))
record("there is a pending tile for every sport with no book yet", len(pend) >= len(STORE["pending"]),
       "%d tiles, %d sports still unwritten" % (len(pend), len(STORE["pending"])))
m = re.search("<p class=" + Q + "lede" + Q + ">(.*?)</p>", st, re.S)
g, n = grade_of(m.group(1) if m else "")
record("the store intro stays plain English", g is not None and g <= 8.0, "grade %s over %d words" % (g, n))
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    readability.audit(str(SHOP / "index.html"), "store page")
g2 = GRADE_RE.search(buf.getvalue())
print("  info  the whole store page reads at grade %s" % (g2.group(1) if g2 else "?"))

sj = (SITE / "assets/stories.js").read_text(encoding="utf-8")
recs = json.JSONDecoder().raw_decode(sj[sj.index("{"):])[0]["athletes"]
cards = [a for a in recs if a.get("book")]
bad = [a["id"] for a in cards if not served(a["book"]).exists()]
record("every live card's book is deliverable", not bad, ", ".join(bad))
bad = [a["id"] for a in cards if a.get("img") and not (SITE / str(a["img"]).split("?")[0][1:]).exists()]
record("every live card's figure is a file that exists", not bad, ", ".join(bad))


def cfg_of(book):
    p = HERE / "SPORTS" / (book + ".json")
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


bad = [a["id"] for a in cards if not a.get("img") and not cfg_of(a["book"]).get("art_note")]
record("a card with no figure says why in its own config", not bad, ", ".join(bad))
seen_art, shared = {}, []
for a in cards:
    f = str(a.get("img", "")).split("?")[0]
    if not f:
        continue
    if f in seen_art:
        shared.append("%s and %s" % (seen_art[f], a["id"]))
    seen_art[f] = a["id"]
record("no two live cards share a figure", not shared, ", ".join(shared))
names, arts = {}, {}
for a in recs:
    for k, d in ((a.get("name"), names), (a.get("sport"), arts)):
        d.setdefault(k, []).append(a["id"])
dup = [k + ": " + ", ".join(v) for k, v in names.items() if len(v) > 1]
record("no two cards print the same first name", not dup, ", ".join(dup)[:160])
bad = [a["id"] for a in cards if not str(a.get("ring_page", "")).startswith("/sports/")]
record("every live card knows its sport page", not bad, ", ".join(bad))
bad = [a["id"] for a in cards if a.get("composite") is not True or a.get("art_fictional") is not True]
record("every figure is labelled a composite illustration", not bad, ", ".join(bad))
rg = (SITE / "assets/ring.js").read_text(encoding="utf-8")
record("the ring decides what is built from the record, not a hardcoded list",
       "a.book" in rg and "builtInfoLegacy" in rg, "")
front = re.search("FRONT_IDS\\s*=\\s*\\[([^\\]]*)\\]", rg)
ids = re.findall(Q + "([a-z-]+)" + Q, front.group(1)) if front else []
record("the ring's front four are books we can sell today",
       bool(front) and all(i in [a["id"] for a in cards] for i in ids), ",".join(ids))

vj = (ROOT / "vercel.json").read_text(encoding="utf-8")
bad = []
for s, rep in STORE["retired"].items():
    if "playbooks/" + s not in vj:
        bad.append("%s has no redirect" % s)
    elif not (SHOP / rep / "index.html").exists():
        bad.append("%s redirects to a missing page %s" % (s, rep))
record("every retired slug has a 301 to a page that exists", not bad, ", ".join(bad))

sm = (SITE / "sitemap.xml").read_text(encoding="utf-8")
bad = [s for s in written if "/playbooks/" + s + "/" not in sm]
record("every written book is in the sitemap", not bad, ", ".join(bad))
bad = [u for u in set(re.findall("<loc>[^<]*/(playbooks/[a-z0-9-]+)/", sm))
       if not (SHOP / u.split("/")[1] / "index.html").exists()]
record("every sitemap playbook URL has a page behind it", not bad, ", ".join(bad))
bad = [u for u in set(re.findall("<loc>[^<]*/(sports/[a-z-]+)/?", sm))
       if not (SITE / u / "index.html").exists() and not (SITE / (u + ".html")).exists()]
record("every sitemap sport URL has a page behind it", not bad, ", ".join(bad))

stale = []
for p in list(SITE.rglob("*.html")) + list(SITE.rglob("*.js")):
    t = p.read_text(encoding="utf-8")
    rel = str(p.parent.relative_to(SITE)).replace(chr(92), "/")
    for url, k in re.findall("([^\\s'\"]+)\\?v=([0-9a-f]{8})", t):
        u = "/" + re.sub("//+", "/", url.lstrip("/"))
        cand = u if (SITE / u[1:]).exists() else "/" + re.sub("//+", "/", rel + "/" + url.lstrip("/"))
        f = SITE / cand[1:]
        if f.exists() and key_of(f) != k:
            stale.append(p.name + " -> " + url)
record("every cache key matches the bytes on disk", not stale, ", ".join(sorted(set(stale))[:6]))
record("the four new figures are registered in the image manifest",
       all(any("cut-%s" % x in json.dumps(r["file"]) for r in
               json.loads((SITE / "IMAGES.json").read_text(encoding="utf-8"))["images"])
           for x in ("alex", "nora", "nia")), "")

# ============================================================ report
print("\n" + "=" * 78)
fails = [r for r in results if not r[1]]
print("%d checks, %d pass, %d fail" % (len(results), len(results) - len(fails), len(fails)))
for n, _, d in fails:
    print("  FAIL  %s  %s" % (n, d))
sys.exit(1 if fails else 0)
