# -*- coding: utf-8 -*-
"""Assemble and lint one RecruitIQ sport playbook. See TEMPLATE.md.

    python deck.py <slug>

Reads SPORTS/<slug>.json (or fixtures/<slug>.json for a book that shipped before the template)
and fragments/<slug>/cNN-*.html, writes <slug>-deck.html and
manifest-<slug>.json for the print step, the site pass and the gate. Linting happens here,
before printing, because a rule that only bites after 30 pages are printed gets skipped.

The rules encoded below are the ones the shipped volleyball book follows, read off that book.
"""
import json, re, sys, io, hashlib, html as H, pathlib, datetime, contextlib

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LANE = pathlib.Path(__file__).parent
# The fifty state names, built in two pieces so a stray non-breaking space in this
# file can never turn "south" or "new" into a state name and fail a book on an ordinary word.
_SINGLE = ("alabama alaska arizona arkansas california colorado connecticut delaware florida hawaii idaho "
           "illinois indiana iowa kansas kentucky louisiana maine maryland massachusetts michigan minnesota "
           "mississippi missouri montana nebraska nevada ohio oklahoma oregon pennsylvania tennessee texas utah "
           "vermont georgia "
           "virginia washington wisconsin wyoming").replace("\u00a0", " ").split()
_PAIRS = [("new", "hampshire"), ("new", "jersey"), ("new", "mexico"), ("new", "york"),
          ("north", "carolina"), ("north", "dakota"), ("rhode", "island"),
          ("south", "carolina"), ("south", "dakota"), ("west", "virginia")]
if len(_SINGLE) != 40:
    raise SystemExit("the single-word state list should hold 40 names, it holds %d" % len(_SINGLE))
STATES = _SINGLE + [x + " " + y for x, y in _PAIRS]
assert len(STATES) == 50, STATES
ASSOCIATIONS = ["WIAA", "UIL", "TAPPS", "CIF", "ODAA", "CIAC", "FHSAA", "GHSA", "OHSAA", "MHSAA", "UIHSAA",
                "NYSPHSAA", "PIAA", "NIAA", "OSSAA", "ISAA", "KHSA", "OSAA", "UHSAA", "NPSAA", "CIIL",
                "OIA", "SISAA", "MIAC"]
PLACEHOLDER_WORDS = ["anytown", "impact athletic", "rivera", "smith", "jones", "williams", "brown", "garcia"]
fails, warns, notes = [], [], []

if (LANE / "readability.py").exists():
    sys.path.insert(0, str(LANE))
    import readability
else:
    readability = None


def cfg_read(slug):
    p = LANE / "SPORTS" / (slug + ".json")
    if not p.exists():
        p = LANE / "fixtures" / (slug + ".json")   # a shipped book, re-linted against the template
    if not p.exists():
        raise SystemExit("no sport config at %s" % p)
    return json.loads(p.read_text(encoding="utf-8"))


def sents(t):
    t = re.sub(r"\s+", " ", t)
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", t) if s.strip()]


def strip_tags(t):
    return H.unescape(re.sub(r"(?is)<[^>]+>", " ", t))


def sections(doc):
    return re.findall(r"(?is)<section\b.*?</section>", doc)


def calendar_grid(doc):
    """The tables that carry a date column are the book's calendars. Give them the
    template's grid: one class, one colgroup, the same column widths in every book,
    so the five playbooks set their date columns alike."""
    out, i = [], 0
    while True:
        j = doc.find("<table", i)
        if j < 0:
            out.append(doc[i:])
            break
        k = doc.find(">", j)
        end = doc.find("</table>", k)
        block = doc[k + 1:end]
        first_row = block[:block.find("</tr>") + 5] if "</tr>" in block else block
        n = len(re.findall(r"<t[dh]\b", first_row))
        out.append(doc[i:j])
        if "class=\"d\"" in block and n in (3, 4):
            names = ["c-when", "c-what", "c-why", "c-where"][:n]
            cls = "cal four" if n == 4 else "cal"
            tag = doc[j:k + 1]
            if 'class="' in tag:
                tag = re.sub(r'class="([^"]*)"', lambda m: 'class="%s %s"' % (m.group(1), cls), tag, count=1)
            else:
                tag = tag[:-1] + ' class="%s">' % cls
            out.append(tag)
            out.append("<colgroup>" + "".join('<col class="%s">' % x for x in names) + "</colgroup>")
        else:
            out.append(doc[j:k + 1])
        i = k + 1
    return "".join(out)


def build(c):
    slug = c["slug"]
    order = c["fragments"]
    d = LANE / "fragments" / slug
    present = sorted(p.name for p in d.glob("*.html"))
    for f in order:
        if not (d / f).exists():
            fails.append("named in the config, missing on disk: %s" % f)
    for f in present:
        if f not in order:
            fails.append("on disk but not in the config order, so it would never print: %s" % f)
    if fails:
        return None
    toks = {"@@LOGO@@": (LANE / "mark.b64").read_text(encoding="utf-8").strip(),
            "@@SPORT@@": c["ring_label"], "@@TITLE@@": c["title_html"], "@@SUB@@": c["sub"],
            "@@KICK@@": c["kicker"], "@@EDGE@@": c["edge"], "@@CHECKED@@": c["rules_checked"],
            "@@LEVELS@@": re.sub(r"(?i)\s+and\s+", " \u00b7 ", c["levels"]), "@@PRICE@@": "$%d" % c["price"], "@@YEAR@@": c["class_year"],
            "@@DOCTYPE@@": c.get("pagehead_word") or c["title"].split(":")[0]}
    # The tab and the PDF metadata carry the book's title, the same words the store page
# prints. A second title for the same book, however good it reads, is one more thing
# a customer has to reconcile.
    toks["@@DOCTYPE@@"] = "%s \u2014 The Commit Book Playbook" % c["title"]
    head = (LANE / "head.txt").read_text(encoding="utf-8")
    if "</style>" not in head or len(head) < 4000:
        fails.append("head.txt is %d bytes and holds no </style>: the shared stylesheet "
                       "is not in it, so nothing could print right" % len(head))
        return None
    doc = head + "\n".join(
        (d / f).read_text(encoding="utf-8").rstrip() for f in order)
    for k, v in toks.items():
        doc = doc.replace(k, v)
    doc = calendar_grid(doc)
    tmpl0 = re.findall(r'(?is)<div class="tmpl">(.*?)</div>', doc)
    if len(tmpl0) >= 2:
        doc = doc.replace("@@SUBJ@@", str(len(re.sub(r"\s", "", H.unescape(tmpl0[0]).strip()))))
        doc = doc.replace("@@WORDS@@", str(5 * round(len(re.sub(r"<[^>]+>", " ", H.unescape(tmpl0[1])).split()) / 5)))
    left = sorted(set(re.findall(r"@@[A-Z_]+@@", doc)))
    if left:
        fails.append("tokens with no value in the config: %s" % ", ".join(left))
    return doc + "\n</body></html>\n"


def keyphrase(title):
    """The words a chapter heading has to carry: the first words up to the first comma or
    colon, and at least eight letters, so 'What to send, part 1: the email' still matches
    the spine title 'What to send, and what good video looks like'."""
    cut = re.split(r"[,:—\u2013(]", title)[0].strip()
    words = cut.split()
    out = ""
    for w in words:
        out = (out + " " + w).strip()
        if len(out) >= 8:
            break
    return out.lower()


def lint_cover(doc, c):
    # The cover is two sections in the W28 template: the title page, then the contents on
    # a page of its own, because the only rule that starts a fresh page is a section break.
    # The lint therefore reads the cover spread, not the first section.
    cov = sections(doc)[0]
    if len(sections(doc)) > 1 and 'class="contents"' not in cov and 'class="contents"' in sections(doc)[1]:
        cov = cov + "\n" + sections(doc)[1]
    for needle, why in [('<div class="lockwrap">', "the logo"),
                        ('class="kicker label', "the red kicker line"),
                        ("<h1", "a title"),
                        ('class="sub"', "the sub paragraph"),
                        ('class="stamp"', "the three-cell stamp"),
                        ('class="edge"', "the edge hook"),
                        ('class="contents"', "the what-is-inside list"),
                        ("not legal advice", "the education-not-advice line")]:
        if needle not in cov:
            fails.append("cover is missing %s (%s)" % (why, needle))
    items = re.findall(r'(?is)<ol class="contents">(.*?)</ol>', cov)
    if not items:
        return
    listed = [strip_tags(x).strip() for x in re.findall(r"(?is)<li>(.*?)</li>", items[0])]
    if len(listed) != len(c["chapters"]):
        fails.append("the cover lists %d chapters, the config names %d" % (len(listed), len(c["chapters"])))
    for want, got in zip(c["chapters"], listed):
        if keyphrase(want) not in got.lower():
            fails.append("cover line %r is not the chapter %r" % (got[:44], want[:44]))
    if len(re.findall(r'(?is)<div><span class="label k">', cov)) < 3:
        fails.append("the cover stamp needs three cells: version, rules checked, levels covered")


def lint_chapters(doc, c):
    found = []
    for s in sections(doc):
        for m in re.finditer(r'(?is)<h2[^>]*>\s*(\d+)\.\s*(.*?)</h2>', s):
            found.append((int(m.group(1)), strip_tags(m.group(2)).strip(), s))
    nums = [n for n, _, _ in found]
    if nums != sorted(nums):
        fails.append("chapters are out of order: %s" % nums)
    firsts, seen = [], set()
    for n, t, _ in found:
        if n not in seen:
            seen.add(n)
            firsts.append((n, t))
    if [n for n, _ in firsts] != list(range(1, len(firsts) + 1)):
        fails.append("chapter numbers skip or repeat at first use: %s" % [n for n, _ in firsts])
    if len(firsts) < len(c["chapters"]):
        fails.append("the deck has %d chapters, the config names %d" % (len(firsts), len(c["chapters"])))
    for (n, t), want in zip(firsts, c["chapters"]):
        if keyphrase(want) not in t.lower():
            fails.append("chapter %d reads %r, the config says %r" % (n, t[:44], want[:44]))
    for n, t, s in found:
        if 'class="pagehead"' not in s:
            fails.append("chapter %d has no pagehead, so it prints with no running header" % n)
        elif c["pagehead_word"].lower() not in s.split('class="pagehead"', 1)[1][:220].lower():
            warns.append("chapter %d pagehead does not name the sport (%s)" % (n, c["pagehead_word"]))
    return found


def lint_states(doc):
    secs = sections(doc)
    body = secs[:-1]
    for i, s in enumerate(body):
        # contexts where a place name is geography or attribution, not a state's rules
        zones = re.findall(r'(?is)<table\b.*?</table>|<blockquote>.*?</blockquote>|<div class="tmpl">.*?</div>|<p class="small">.*?</p>', s)
        rest = s
        for z in zones:
            rest = rest.replace(z, " ")
        rest = rest.replace("\u00a0", " ")   # a link or a paste may hide a non-breaking space
        for st in STATES:
            for m in re.finditer(r"\b(?:%s)\b" % "|".join(x.replace(" ", r"\s+") for x in [st]), rest, re.I):
                sent = next((x for x in sents(strip_tags(rest)) if m.group(0).lower() in x.lower()), "")
                if '"' in sent or "\u201c" in sent:
                    notes.append("chapter %d names %s inside a quotation: %s" % (i + 1, m.group(0), sent[:110]))
                    continue
                fails.append("chapter %d names a state outside a table, a quote or the sample email: %s"
                             % (i + 1, sent[:130] or m.group(0)))
        for a in ASSOCIATIONS:
            if re.search(r"(?<![A-Za-z])%s(?![A-Za-z])" % a, rest):
                fails.append("chapter %d names a state association (%s); the book says \"your state association\""
                             % (i + 1, a))
        for s2 in sents(strip_tags(rest)):
            if re.search(r"(?i)state association", s2):
                notes.append("chapter %d says: %s" % (i + 1, s2[:120]))
    src = secs[-1]
    if not re.search(r"(?i)one region|example|not a shortlist|used here as", strip_tags(src)):
        warns.append("the sources chapter should label any named school or region as one sample, not a shortlist")
    for st in STATES:
        for m in re.finditer(r"\b%s\b" % st.replace(" ", r"\s+"), strip_tags(src), re.I):
            notes.append("sources chapter names %s (allowed: it is the paper trail)" % m.group(0))
            break


def lint_email(doc, c):
    blocks = re.findall(r'(?is)<div class="tmpl">(.*?)</div>', doc)
    if len(blocks) < 2:
        fails.append("the book needs a subject and a body as two .tmpl blocks; found %d" % len(blocks))
        return None
    subj, body = (H.unescape(x).strip() for x in blocks[:2])
    letters, words = len(re.sub(r"\s", "", subj)), len(re.findall(r"[A-Za-z0-9$.''\u2019\-]+", body))
    if not 55 <= letters <= 80:
        fails.append("the sample subject is %d letters; the house rule is about 70 (55 to 80)" % letters)
    if not 160 <= words <= 195:
        fails.append("the sample body is %d words; the house rule is about 180 (160 to 195)" % words)
    both = subj + "\n" + body
    for st in STATES:
        if re.search(r"\b%s\b" % st.replace(" ", r"\s+"), both, re.I):
            fails.append("the sample email names a state (%s); it asks for a time zone instead" % st)
    for org in re.findall(r"\b[A-Z][a-z]{2,}(?:\s+[A-Z][a-z]{2,})?\s+(?:High\s+School|High|HS|Athletic|Academy|Club|Camp|Classic|Showcase|Tournament|Region|Center|Centre|Volleyball|Baseball|Softball|Soccer|United|FC|SC)\b",
                          both):
        if not any(p in org.lower() for p in PLACEHOLDER_WORDS):
            fails.append("the sample email names an organisation that is not a placeholder: %s" % org)
    for bad in c.get("banned_names", []):
        if bad.lower() in both.lower():
            fails.append("the sample email uses a name this book must not use: %s" % bad)
    for tel in re.findall(r"\(?\d{3}\)?[\s.\-]\d{3}[\s.\-]\d{4}", both):
        if "555" not in tel:
            fails.append("the sample email carries a real-looking phone number: %s" % tel)
    return {"subject": subj, "letters": letters, "words": words}


def lint_grid(doc, c):
    """A calendar has to set its columns the way the book on the shelf does.

    The reference is read off the shipped book's own fragments when this runs, not typed in
    here, for the reason the print checker learned the hard way: a target somebody writes down
    passes whatever they expected to see. A print auditor measured four new books disagreeing
    with the shelf and, in one book, with each other. The cause was not the template: most
    calendar header cells carried no width at all, so the column took whatever its content
    wanted. The widths therefore live on every cell of every calendar, and this is where that
    is enforced.
    """
    ref = LANE / "fragments" / "volleyball-road-to-college" / "c04-ch03.html"
    if not ref.exists() or c["slug"] == "volleyball-road-to-college":
        return
    head = re.search(r"<thead>.*?</thead>", ref.read_text(encoding="utf-8"), re.S)
    cells = re.findall(r"<th(\s[^>]*)?>(.*?)</th>", head.group(0), re.S) if head else []
    want = [re.findall(r"width:\s*([0-9.]+%)", x[0]) for x in cells][:2]
    want = [w[0] for w in want if w]
    if len(want) < 2:
        fails.append("the book on the shelf carries no calendar widths to copy; check " + ref.name)
        return
    for m in re.finditer(r"<thead>.*?</thead>", doc.decode("utf-8") if isinstance(doc, bytes) else doc, re.S):
        cs = re.findall(r"<th(\s[^>]*)?>(.*?)</th>", m.group(0), re.S)
        if not cs or re.sub(r"<[^>]+>", "", cs[0][1]).strip().lower() != "when":
            continue
        got = [re.findall(r"width:\s*([0-9.]+%)", x[0]) for x in cs]
        got = [g[0] if g else None for g in got][:2]
        # The date column always has to match, because that is the column a reader runs a finger
        # down. The second one only means anything against a table with the same number of
        # columns; a two-column calendar spends the rest of the page on its answer column.
        bad = got[:1] != want[:1] or (len(cs) == len(cells) and got != want)
        if bad:
            fails.append("a calendar sets its first columns to %s; the book on the shelf prints %s" % (got, want))



def lint_tags(doc):
    cal = [s for s in sections(doc) if re.search(r"(?is)<h2[^>]*>\s*\d+\.\s*[^<]*(plan by date|calendar)", s)]
    for s in cal:
        for cell in re.findall(r'(?is)<td class="d">(.*?)</td>', s):
            txt = strip_tags(cell)
            if re.search(r"\d", txt) and not re.search(r"(?i)(HARD|PROJECTED|OPENING|t-hard|t-projected|t-opening)", cell):
                fails.append("a date in the calendar chapter carries no tag: %r" % txt.strip()[:60])
        for row in re.findall(r'(?is)<tr\b[^>]*>.*?</tr>', s):
            if "PROJECTED" in row and "t-projected" not in row and ">PROJECTED<br" not in row:
                fails.append("a calendar row says PROJECTED outside the date cell: %s" % strip_tags(row).strip()[:110])
    if re.search(r"\bPROJECTED\b", doc):
        if not re.search(r"(?i)projected[^.]{0,160}(worked out|not printed|calculated|figured)", strip_tags(doc)):
            fails.append("PROJECTED appears but is never defined for the reader")
        else:
            notes.append("PROJECTED is defined in text and carried in the date cell")
    if "t-hard" not in doc:
        warns.append("no HARD tag anywhere: chapter 3 usually tags the dates a document prints")
    if re.search(r"\bUNCONFIRMED\b", strip_tags("\n".join(sections(doc)[:-1]))):
        fails.append("UNCONFIRMED appears in a chapter; it belongs in the sources chapter, where the reader can see what is missing")


def lint_must_say(doc, c):
    for want in c.get("must_say", []):
        if want.lower() not in strip_tags(doc).lower():
            fails.append("this book never says %r, and it is a number the family came for" % want)


BRITISH = ["organisation", "organisational", "programme", "colour", "behaviour", "favour", "labour",
           "neighbour", "centre", "metre", "realise", "recognise", "prioritise", "utilise", "minimise",
           "maximise", "analyse", "defence", "offence", "licence", "travelling", "cancelled", "labelled",
           "focussed", "judgement", "acknowledgement", "practise", "cheque", "grey colour"]


def lint_spelling(doc):
    """US spelling, house rule. Caught as a list, not a shrug."""
    for m in re.finditer(r"(?i)\b(%s)\b" % "|".join(BRITISH), strip_tags(doc)):
        warns.append("British spelling: %s" % m.group(0).lower())


def lint_grade(path, c):
    if readability is None:
        warns.append("readability.py is missing, so the grade gate did not run")
        return None
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        readability.audit(str(path), c["ring_label"])
    out = buf.getvalue()
    m = re.search(r"Flesch-Kincaid grade level:\s*([\d.]+)", out)
    if not m:
        fails.append("the grader printed no grade")
        return None
    g = float(m.group(1))
    if g > 8.0:
        fails.append("the customer text reads at grade %.1f; the house rule is 8 or simpler" % g)
    for line in out.splitlines():
        if "sentences at grade 9+" in line or "avg words per sentence" in line:
            notes.append(line.strip())
    return g


def main():
    slug = sys.argv[1] if len(sys.argv) > 1 else None
    if not slug:
        raise SystemExit("usage: python deck.py <slug>")
    if "--" in (slug or ""):
        print("STATES parses to %d entries; suspicious: %s" % (len(STATES), [s for s in STATES if " " not in s and len(s) < 6]))
    c = cfg_read(slug)
    doc = build(c)
    if doc is None:
        finish(slug, None)
    out = LANE / (slug + "-deck.html")
    out.write_bytes(doc.encode("utf-8"))
    lint_cover(doc, c)
    found = lint_chapters(doc, c)
    lint_states(doc)
    email = lint_email(doc, c)
    lint_grid(doc, c)
    lint_tags(doc)
    lint_must_say(doc, c)
    lint_spelling(doc)
    g = lint_grade(out, c)
    man = {"slug": slug, "title": c["title"], "ring_label": c["ring_label"], "gender": c["gender"],
           "athlete": c["athlete"], "athlete_id": c["athlete_id"], "sport_page": c["sport_page"],
           "price": c["price"], "class_year": c["class_year"], "edition": c["edition"],
           "chapters": [t for _, t, _ in dict((n, (n, t, s)) for n, t, s in found).values()],
           "fragments": c["fragments"],
           "fragment_sha": {f: hashlib.sha256((LANE / "fragments" / slug / f).read_bytes()).hexdigest()[:8]
                            for f in c["fragments"]},
           "doc_bytes": len(doc.encode("utf-8")), "doc_sha": hashlib.sha256(doc.encode("utf-8")).hexdigest()[:8],
           "grade": round(g, 1) if g else None, "email": email,
           "built": datetime.date.today().isoformat()}
    (LANE / ("manifest-" + slug + ".json")).write_bytes(
        json.dumps(man, indent=1, ensure_ascii=False).encode("utf-8"))
    print("wrote %-42s %6.1f KB  %2d fragments  %2d chapters  grade %s"
          % (out.name, man["doc_bytes"] / 1024.0, len(c["fragments"]), len(man["chapters"]),
             ("%.1f" % g) if g else "?"))
    if email:
        print("sample email: subject %d letters, body %d words" % (email["letters"], email["words"]))
    finish(slug, man)


def finish(slug, man):
    for n in notes:
        print("   note: " + n)
    for w in warns:
        print("   warn: " + w)
    if fails:
        for f in fails:
            print("   FAIL: " + f)
        print("\n%s: %d problems, %d warnings" % (slug, len(fails), len(warns)))
        sys.exit(1)
    print("   %s passes the template lints" % slug)


main()
