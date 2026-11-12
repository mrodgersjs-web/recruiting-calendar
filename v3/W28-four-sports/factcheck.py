"""factcheck.py — nothing in a book that the packet does not carry. (W28)

    python factcheck.py <slug>            one book
    python factcheck.py <slug> --json     machine-readable, for gate.py
    python factcheck.py --all             every book with a built deck

The deck is read as built HTML (`<slug>-deck.html`, written by deck.py). The
supporting evidence is the sport's own research packets, named in the config's
`packets` list. The rule is the one in TEMPLATE.md: a date, a dollar figure, a
count, a percentage or a bylaw number appears in the book only if the packet
carries it, or the book's own config allows the arithmetic.

A date the packet computed rather than read ([DERIVED]) may only print inside a
date cell tagged PROJECTED. A date the packet read in an official document may
print tagged HARD, or in prose. A date in neither is a failure.

Numbers the book works out itself (a total, a per-year ceiling) go in the
config's `math_ok` list with the sentence that shows the working, so the next
reader can see the sum.
"""
import html
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
MONTHS = {m: m[:3].lower() for m in
          ("january february march april may june july august september october november december".split())}
MONTHS.update({"sept": "sep"})
MONTHS_BY_NUM = dict(enumerate(
    "january february march april may june july august september october november december".split(), 1))
ORDD = r"(?:st|nd|rd|th)?"
MO = r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sept(?:ember)?|Sep|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"          # a month, the whole word, optionally abbreviated
DATE = re.compile(r"\b(\d{1,2})" + ORDD + r"\s*((?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sept(?:ember)?|Sep|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?))\.?"
                  r"(?:,?\s*(\d{4}))?\b", re.I)
RANGE = re.compile(r"\b(\d{1,2})\s*(?:to|-|to–|-–)\s*(\d{1,2})\s+((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|"
                   r"Sep|Oct|Nov|Dec)[a-z]*)\.?", re.I)
YEARLED = re.compile(r"\b((?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sept(?:ember)?|Sep|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?))\.?\s+(\d{1,2})"
                    + ORDD + r"(?:,?\s*(\d{4}))?\b", re.I)
BYLAW = re.compile(r"\b(\d{1,2}(?:\.\d+){2,})\b")
MONEY = re.compile(r"\$\s?\d[\d,]*(?:\.\d+)?")
PCT = re.compile(r"\b(\d{1,2}(?:\.\d+)?)\s*(?:percent|%)", re.I)
NUM = re.compile(r"\b\d{1,3}(?:,\d{3})+\b|\b\d+\.\d+\b")
TAGS = re.compile(r"<[^>]+>")


def norm_month(m):
    m = m.lower().rstrip(".")
    return MONTHS.get(m, m[:3] if m[:3] in ("jan", "feb", "mar", "apr", "may", "jun",
                                            "jul", "aug", "sep", "oct", "nov", "dec") else m[:3])


RANGE2 = re.compile(r"\b((?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sept(?:ember)?|Sep|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?))\.?\s+"
                    r"(\d{1,2})\s*(?:to|-|\u2013|\u2014)\s*(\d{1,2})(?:,?\s*(\d{4}))?\b", re.I)
NUMD = re.compile(r"\b(\d{1,2})[/-](\d{1,2})[/-](\d{4}|\d{2})\b")
ISOD = re.compile(r"\b(\d{4})-(\d{1,2})-(\d{1,2})\b")   # the packets date-stamp every line this way


def days(a, b):
    a, b = sorted((int(a), int(b)))
    return range(a, min(b, 31) + 1)


def dates_in(text):
    """Normalised (day, month, year-or-None) triples from any prose, ranges opened up to
    every day they cover. A packet that prints NOV 9-12 supports 9, 10, 11 and 12 November;
    a book that prints 12 Nov 2026 then matches it, and the year is allowed to come from the
    book's own class year."""
    out = set()
    # A URL is not a claim about a date. Packet lines carry source links, and 2025-08-FINAL-2019
    # reads as three dates to a pattern-matcher.
    text = re.sub(r"(?i)\b(?:https?|ftp)://\S+", " ", text)
    text = re.sub(r"(?i)\b[\w./%-]+\.(?:pdf|html?|php|aspx|com|org|net|gov)\b", " ", text)
    for d, m, y in DATE.findall(text):
        out.add((int(d), norm_month(m), int(y) if y else None))
    for m, d, y in YEARLED.findall(text):
        out.add((int(d), norm_month(m), int(y) if y else None))
    for a, b, m in RANGE.findall(text):
        for d in (a, b):          # endpoints only: the book quotes a range, it does not name every day in it
            out.add((int(d), norm_month(m), None))
    for m, a, b, y in RANGE2.findall(text):
        for d in (a, b):
            out.add((int(d), norm_month(m), int(y) if y else None))
    for mo, d, y in NUMD.findall(text):        # the rule pages print 4/15/26 and 10-27-26
        mo, d, y = int(mo), int(d), int(y)
        if 1 <= mo <= 12 and 1 <= d <= 31:     # "2025-2026" is a handbook edition, not a date
            out.add((d, norm_month(MONTHS_BY_NUM[mo]), 2000 + y if y < 100 else y))
    for y, mo, d in ISOD.findall(text):        # and 2026-04-19
        mo, d = int(mo), int(d)
        if 1 <= mo <= 12 and 1 <= d <= 31:
            out.add((d, norm_month(MONTHS_BY_NUM[mo]), int(y)))
    return {t for t in out if 1 <= t[0] <= 31}


def numbers_in(text):
    out = set()
    for t in MONEY.findall(text):
        out.add("$" + re.sub(r"[,\s]", "", t[1:]).replace(".00", ""))   # $50.00 and $50 are one price
    for t in PCT.findall(text):
        out.add(re.sub(r"\.0$", "", t) + "%")
    for t in NUM.findall(text):
        out.add(re.sub(r"[,]", "", t))
    return out


def bylaws_in(text):
    return set(BYLAW.findall(text))


TMPL = re.compile(r'(?is)<(div|p|aside|table)\b[^>]*class="[^"]*tmpl[^"]*".*?</\1>')
BOILER = re.compile(r'(?is)<(style|script)[^>]*>.*?</\1>')


def strip(t):
    """Plain text of the customer-facing prose. Two things are not claims about the
    world and are cut before anything is scraped: the stylesheet (its 1.46 and 38% are
    line-heights, not figures), and any block marked tmpl, which is the sample email and
    the other made-up copy the house rules insist on (Anytown South HS, a coach surname,
    a 3.5 GPA)."""
    t = BOILER.sub(' ', t)
    t = TMPL.sub(' ', t)
    return re.sub(r"\s+", " ", html.unescape(TAGS.sub(" ", t))).strip()


def windows(text, needle, span=200):
    out, i = [], 0
    flat = re.sub(r"\s+", " ", text)
    while True:
        i = flat.find(needle, i)
        if i < 0:
            return out
        out.append(flat[max(0, i - 60):i + len(needle) + span])
        i += 1


def packet_lines(root, names):
    """The packet text, and the dates split by whether a document printed them."""
    all_text, official, derived, service = [], set(), set(), set()
    for n in names:
        p = (root / "research" / n).resolve()
        if not p.exists():
            raise SystemExit("no packet %s. The config names packets it cannot find." % p)
        t = p.read_text(encoding="utf-8")
        all_text.append(t)
        for line in t.splitlines():
            ds = dates_in(line)
            if "[DERIVED]" in line or "DERIVED, not printed" in line:
                derived |= ds
            elif re.search(r"\[(OFFICIAL|DATA|SERVICE|COACH)\]", line):
                official |= ds
            elif "-" in line[:3].strip():     # a bare bullet, no tag
                service |= ds
    return "\n".join(all_text), official, derived, service


def run(slug, as_json=False):
    cfg_p = HERE / "SPORTS" / ("%s.json" % slug)
    if not cfg_p.exists():
        cfg_p = HERE / "fixtures" / ("%s.json" % slug)
    if not cfg_p.exists():
        raise SystemExit("no config for %s" % slug)
    cfg = json.loads(cfg_p.read_text(encoding="utf-8"))
    deck = HERE / ("%s-deck.html" % slug)
    if not deck.exists():
        raise SystemExit("no built deck for %s. Run deck.py first." % slug)
    raw = deck.read_text(encoding="utf-8")
    body = strip(raw)
    pk, official, derived, untagged = packet_lines(HERE, cfg["packets"])
    pk_dates = dates_in(pk)
    pk_numbers = numbers_in(pk)
    pk_bylaws = bylaws_in(pk)
    math_ok = cfg.get("math_ok", {})
    allowed = numbers_in(json.dumps(math_ok, ensure_ascii=False))
    derived |= dates_in(json.dumps(math_ok, ensure_ascii=False))
    pk_dates |= derived        # the book's own arithmetic is support, under the PROJECTED tag rule
    # A date the book worked out itself is allowed, but only under PROJECTED: same rule the
    # packets apply to their own [DERIVED] lines.
    derived |= dates_in(json.dumps(math_ok, ensure_ascii=False))
    fails, warns, info = [], [], []

    pk_daymonth = {(d, m) for d, m, _ in pk_dates}
    for d, m, y in sorted(dates_in(body), key=lambda x: (x[2] or 0, x[1], x[0])):
        # A book sentence may name a day with no year ("the dead period starts 9 November") and a
        # packet may name it with one ("November 9-12, 2026"), or the other way round. A day the
        # packet carries in any year is a day the packet carries. Whether it prints as HARD or
        # PROJECTED is the separate rule below.
        exact = (d, m, y) in pk_dates
        loose = (d, m) in pk_daymonth
        if not (exact or loose):
            fails.append("date %d %s %s is in the book and in no packet" % (d, m, y or "?"))
            continue
        if (d, m, y) in derived or (not exact and (d, m, None) in derived):
            hits = windows(raw, "%d %s" % (d, m)) or windows(raw, "%s %d" % (m, d))
            if hits and not any("PROJECTED" in w[:260] for w in hits):
                fails.append("date %d %s was computed from rule text and prints untagged: %s"
                             % (d, m, hits[0][:110]))
        elif (d, m, y) in official:
            hits = windows(raw, "%d %s" % (d, m)) or windows(raw, "%s %d" % (m, d))
            intd = [w for w in hits if 'class="d"' in w or "PROJECTED" in w or "HARD" in w]
            if intd and not any(("HARD" in w[:260] or "PROJECTED" in w[:260]) for w in intd):
                warns.append("date %d %s sits in a date cell with no tag: %s" % (d, m, intd[0][:110]))
    for rng in RANGE.findall(body):
        a, b, m = rng
        if not any(mo == norm_month(m) for _, mo, _ in pk_dates):
            fails.append("date range %s-%s %s has no packet support" % (a, b, m))
    for n in sorted(numbers_in(body)):
        if n in pk_numbers or n in allowed:
            continue
        approx = any(re.sub(r"\D", "", n) and w in body[max(0, body.find(n) - 60):body.find(n)]
                     for w in ("about ", "roughly ", "close to "))
        near = [p for p in pk_numbers if p.replace("$", "").isdigit() and n.replace("$", "").isdigit()
                and abs(float(p.replace("$", "").replace(",", "")) -
                        float(n.replace("$", "").replace(",", ""))) /
                max(1.0, float(p.replace("$", "").replace(",", ""))) < 0.02]
        if approx and near:
            info.append("%s is an approximation of packet figure %s" % (n, sorted(near)[0]))
        else:
            fails.append("figure %s is in the book and in no packet (or list it in math_ok)" % n)
    for b in sorted(bylaws_in(body)):
        if b not in pk_bylaws:
            fails.append("citation %s is in the book and in no packet" % b)
    for s in cfg.get("must_say", []):
        if s.lower() not in body.lower():
            fails.append("must-say fact is missing from the book: %s" % s)
    says = [s for s in cfg.get("must_say", [])]
    res = {"slug": slug, "fails": fails, "warns": warns, "info": sorted(set(info)),
           "dates": len(dates_in(body)), "figures": len(numbers_in(body)),
           "citations": len(bylaws_in(body)), "packet_dates_official": len(official),
           "packet_dates_derived": len(derived), "must_say": len(says)}
    if as_json:
        print(json.dumps(res, indent=1))
    else:
        print("%s: %d dates, %d figures, %d citations checked against %s"
              % (slug, res["dates"], res["figures"], res["citations"], " and ".join(cfg["packets"])))
        for f in fails:
            print("  FAIL  " + f)
        for w in warns:
            print("  warn  " + w)
        for i in res["info"]:
            print("  info  " + i)
        print("  %d failures, %d warnings, %d noted approximations" % (len(fails), len(warns), len(res["info"])))
    return res


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    js = "--json" in sys.argv
    if "--all" in sys.argv:
        args = [p.stem[: -len("-deck")] for p in HERE.glob("*-deck.html")]
    if not args:
        raise SystemExit("usage: python factcheck.py <slug> [--json]   or   --all")
    sys.exit(1 if sum(len(run(s, js)["fails"]) for s in args) else 0)
