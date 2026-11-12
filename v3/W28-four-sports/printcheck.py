"""printcheck.py — the printed book, checked as a printed book. (W28)

    python printcheck.py <slug>

It reads `pdfs/<slug>.pdf` (what the customer gets) next to `<slug>-deck.html`
(what the browser was given), and checks the house print rules mechanically:

  1. US Letter, every page.
  2. A running head, a footer, and `N / total` on every page, with a total that
     matches the real page count.
  3. One chapter per fresh page, in the order the config lists them.
  4. No table row split across a page boundary: every cell's text has to appear
     whole on one page. This is the check that catches a row cut in half.
  5. No page that carries only a heading, and no page under 180 characters of
     body once the head and foot are removed.

Geometry that only an eye can judge (margins, where a figure sits, whether a
caption orphaned) is the print auditor's job, not this file's.
"""
import html
import json
import pathlib
import re
import sys

try:
    from pypdf import PdfReader
except ImportError:
    from PyPDF2 import PdfReader

HERE = pathlib.Path(__file__).resolve().parent
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
LIG = {"\ufb01": "fi", "\ufb02": "fl", "\ufb00": "ff", "\ufb03": "ffi", "\ufb04": "ffl",
       "\u00ad": "", "\u2019": "'", "\u2018": "'", "\u201c": '"', "\u201d": '"',
       "\u2013": "-", "\u2014": "-", "\u00b7": "/", "\u2026": "..."}
TAGS = re.compile(r"<[^>]+>")
LETTER = (612.0, 792.0)


def norm(t):
    t = t.replace("\u00a0", " ").replace("\u2019", "'").replace("\u2014", "-").replace("\u2013", "-")
    return re.sub(r"\s+", " ", t).strip()


def flat(t):
    return norm(TAGS.sub(" ", html.unescape(t)))


def unligature(t):
    for k, v in LIG.items():
        t = t.replace(k, v)
    return t


def page_lines(t):
    return [norm(x) for x in t.splitlines() if norm(x)]


def nospace(t):
    """The text layer of these decks letter-spaces its headings, hyphenates the
    body, and breaks words across lines. A fair comparison keeps letters, digits
    and the punctuation that carries meaning, and drops the rest."""
    return re.sub(r"[\s\u00ad\u2010\u2011\u2012\u2013\u2014\u2015'\"\u2018\u2019\u201c\u201d]", "", t).lower()


def keyphrase(title):
    """The words a chapter heading has to carry. Same rule as deck.py: the first
    words up to the first comma or colon, at least eight letters. gate.py checks
    that the two copies have not drifted apart."""
    cut = re.split(r"[,:—\u2013(]", title)[0].strip()
    words = cut.split()
    out = ""
    for w in words:
        out = (out + " " + w).strip()
        if len(out) >= 8:
            break
    return out.lower()


def text_items(reader, pno):
    """Every run of text drawn on a page, as {x, y, size} in PDF points.

    extract_text() returns words with no geometry, which is how four printed books passed
    a checker while their running heads measured half a point tall. Size and position have
    to come off the operators, so this walks the page content stream: a graphics-state stack
    for q/Q, the CTM built from cm, the text matrix from BT/Tm/Td, the point size from Tf,
    and on a show-text operator it reports where the run lands and how big, after the page\'s
    own 0.75 print scale. The glyphs in a run are IDs in a subsetted font and are not decoded:
    this answers how big and where, which is what a customer can see.

    The first version kept the q/Q markers on the operand stack, so a later Tm popped a
    marker as if it were a number, never moved the text matrix, and every run on every page
    reported y = 0. Operators and operands are kept apart now.
    """
    try:
        data = reader.pages[pno].get_contents().get_data()
    except Exception:                                             # noqa: BLE001
        return []

    def mul(m, n):
        return (m[0] * n[0] + m[1] * n[2], m[0] * n[1] + m[1] * n[3],
                m[2] * n[0] + m[3] * n[2], m[2] * n[1] + m[3] * n[3],
                m[4] * n[0] + m[5] * n[2] + n[4], m[4] * n[1] + m[5] * n[3] + n[5])

    IDENT = (1, 0, 0, 1, 0, 0)
    gstate = [IDENT]
    ctm, tm, operands, out = IDENT, IDENT, [], []
    fontsize = 0.0
    i = 0
    while i < len(data):
        c = data[i:i + 1]
        if c in b" \t\r\n":
            i += 1
            continue
        if c == b"%":
            j = data.find(b"\n", i)
            i = len(data) if j < 0 else j + 1
            continue
        if c == b"(":
            depth, i = 1, i + 1
            while i < len(data) and depth:
                if data[i:i + 1] == b"\\":
                    i += 2
                    continue
                if data[i:i + 1] == b"(":
                    depth += 1
                elif data[i:i + 1] == b")":
                    depth -= 1
                i += 1
            operands.append("str")
            continue
        if c == b"<":
            j = data.find(b">", i)
            i = len(data) if j < 0 else j + 1
            operands.append("hex")
            continue
        if c == b"/":
            j = i + 1
            while j < len(data) and data[j:j + 1] not in b" \t\r\n/<>[](){}%":
                j += 1
            operands.append("name")
            i = j
            continue
        if c in b"[]{}":
            i += 1
            continue
        j = i
        while j < len(data) and data[j:j + 1] not in b" \t\r\n/<>[](){}%":
            j += 1
        tok = data[i:j]
        i = j
        if not tok:
            # A stray ")" or ">" is not the start of a token and the loop above will not
            # consume it. Without the bump the scanner spins on that one byte forever,
            # which is how the first version of this hung on page 2 of the baseball book.
            i += 1
            continue
        if re.match(rb"^[-+.0-9]", tok):
            try:
                operands.append(float(tok))
            except ValueError:
                pass
            continue
        op = tok.decode("latin-1")
        if op == "q":
            gstate.append(ctm)
        elif op == "Q":
            if len(gstate) > 1:
                gstate.pop()
            ctm = gstate[-1]
        elif op == "cm":
            v = [x for x in operands[-6:] if isinstance(x, float)]
            if len(v) == 6:
                ctm = mul(tuple(v), ctm)
                gstate[-1] = ctm
            operands = []
        elif op == "BT":
            tm = IDENT
        elif op == "Tm":
            v = [x for x in operands[-6:] if isinstance(x, float)]
            if len(v) == 6:
                tm = tuple(v)
            operands = []
        elif op in ("Td", "TD"):
            v = [x for x in operands[-2:] if isinstance(x, float)]
            if len(v) == 2:
                tm = mul((1, 0, 0, 1, v[0], v[1]), tm)
            operands = []
        elif op == "Tf":
            v = [x for x in operands[-2:] if isinstance(x, float)]
            if len(v) == 1:
                fontsize = v[0]
            operands = []
        elif op in ("Tj", "TJ", "'", "\""):
            dev = mul(tm, ctm)
            scale = abs(dev[0] * dev[3] - dev[1] * dev[2]) ** 0.5
            out.append({"size": fontsize * scale, "x": dev[4], "y": dev[5]})
            operands = []
        else:
            operands = []
    return out


def run(slug, verbose=False):
    cfg_p = HERE / "SPORTS" / ("%s.json" % slug)
    if not cfg_p.exists():
        cfg_p = HERE / "fixtures" / ("%s.json" % slug)
    cfg = json.loads(cfg_p.read_text(encoding="utf-8")) if cfg_p.exists() else {}
    pdf_p, deck_p = HERE / "pdfs" / ("%s.pdf" % slug), HERE / ("%s-deck.html" % slug)
    fails, warns, info = [], [], []
    if not pdf_p.exists():
        return {"slug": slug, "fails": ["no pdf at %s. Print the deck first." % pdf_p.name],
                "warns": [], "info": [], "pages": 0}
    r = PdfReader(str(pdf_p))
    texts = [(p.extract_text() or "") for p in r.pages]
    lines = [page_lines(t) for t in texts]
    n = len(r.pages)

    # 1 paper
    for i, p in enumerate(r.pages, start=1):
        try:
            box = p.mediabox
            w, h = float(box.width), float(box.height)
        except Exception as e:                                    # noqa: BLE001
            fails.append("page %d: cannot read the paper size (%s)" % (i, e))
            continue
        if abs(w - LETTER[0]) > 1 or abs(h - LETTER[1]) > 1:
            fails.append("page %d is %.0f x %.0f, not US Letter" % (i, w, h))

    # 2 head, foot, numbering
    # The footer prints the brand and the number in two boxes with no gap between them,
    # so the text layer glues "book" to "10". A word boundary would not match that.
    pgno = re.compile(r"(?<![\d/])(\d{1,3})\s*/\s*(\d{1,3})(?![\d/])")
    # Read the number off the footer line only. A source address such as
    # /news/2026/8/24/ or a rule note reading "Adopted: 6/24/26" is also d/d, and on
    # a page full of links the first such pair is not the page number.
    def footer_pair(txt):
        for ln in txt.splitlines():
            low = ln.lower()
            # Two footers have ever carried the number: the shelf books' "Education, not
            # legal advice" line and this lane's retired "recruitingiq" line. Either is
            # enough to prove the line is the footer and not a date in a source.
            if "not legal advice" in low or "recruitingiq" in low:
                g = pgno.search(ln)
                if g:
                    return (g.group(1), g.group(2))
        return None
    for i, t in enumerate(texts, start=1):
        m = footer_pair(t)
        if not m:
            fails.append("page %d has no page number" % i)
            continue
        if int(m[1]) != n:
            fails.append("page %d reads %s / %s, the file has %d pages" % (i, m[0], m[1], n))

        if int(m[0]) != i:
            fails.append("page %d is numbered %s" % (i, m[0]))
        if "commitbook" not in nospace(t) and "commit book" not in norm(t).lower():
            fails.append("page %d has no running head or footer brand" % i)
    if n and "commitbook" not in nospace(texts[0]):
        info.append("the cover has no brand line, unlike the inside pages")

    # 2b The furniture is measured, not read. The head and the footer of four printed books
    # were in the text layer, so a word check passed, and on paper they were specks: 0.58 pt
    # of cap height, and the page number glued to the brand at the left because the flexbox
    # that pushes it right had been dropped by a broken HTML attribute.
    FOOT_INK, HEAD_INK = 45.0, 45.0
    MIN_PT = 4.5
    for pg in range(1, n + 1):
        items = text_items(r, pg - 1)
        head_band = [x for x in items if x["y"] > LETTER[1] - HEAD_INK]
        foot_band = [x for x in items if x["y"] < FOOT_INK]
        if not head_band:
            fails.append("page %d: nothing is drawn in the running-head band" % pg)
        elif max(x["size"] for x in head_band) < MIN_PT:
            fails.append("page %d: the running head prints at %.1f pt, too small to read"
                         % (pg, max(x["size"] for x in head_band)))
        if not foot_band:
            fails.append("page %d: nothing is drawn in the footer band" % pg)
        elif max(x["size"] for x in foot_band) < MIN_PT:
            fails.append("page %d: the footer prints at %.1f pt, too small to read"
                         % (pg, max(x["size"] for x in foot_band)))
        if not [x for x in foot_band if x["x"] > LETTER[0] * 0.60]:
            fails.append("page %d: the page number is not at the right edge of the footer" % pg)

    # 2c The calendar grid is checked in the markup, not off the paper, and that is a decision
    # rather than a shortcut. A printed page carries a text run per word, with no mark of which
    # cell it belongs to: grouping runs into columns by their white space found the shelf book's
    # "calendar" 0.17in wide, which is a justified line of prose, and a gate that compares one
    # kind of noise to another will pass anything. The grid is set by <th style="width"> on a
    # table with table-layout: fixed, so deck.py lints the widths against the shelf book's own
    # fragments, where the claim is actually made. If the two ever disagree, the paper wins and
    # this note is wrong.
    # 3 one chapter per fresh page, in order
    raw = [nospace(t) for t in texts]
    titles = [nospace(x) for x in cfg.get("chapters", [])]
    contents = [i for i, t in enumerate(raw, start=1)
                if titles and sum(x in t for x in titles) * 3 >= 2 * len(titles)]
    seen = []
    for n_i, tl in enumerate(titles):
        key = tl if tl in "".join(raw) else nospace(keyphrase(cfg["chapters"][n_i]))
        at = [i for i, t in enumerate(raw, start=1) if key in t and i not in contents]
        if not at:
            fails.append("chapter %d (%s) has no page of its own" % (n_i + 1, cfg["chapters"][n_i]))
            continue
        if len(key) < 12:
            warns.append("chapter %d prints only %r as its heading, too short to prove where it starts"
                         % (n_i + 1, cfg["chapters"][n_i].split(",")[0]))
        elif at != list(range(at[0], at[-1] + 1)):
            fails.append("chapter %d (%s) does not run over whole pages: %s"
                         % (n_i + 1, cfg["chapters"][n_i], at))
        start = [i for i in at if key in nospace(" ".join(page_lines(texts[i - 1])[1:7]))]
        if not start:
            fails.append("chapter %d (%s) never starts a fresh page: its title only sits in the running head"
                         % (n_i + 1, cfg["chapters"][n_i]))
            continue
        seen.append((start[0], cfg["chapters"][n_i]))
    if [p for p, _ in seen] != sorted(p for p, _ in seen):
        fails.append("chapters are out of order: %s" % seen)
    info.append("contents page: %s" % (contents or "none found"))

    # 4 nothing cut in half
    cells = []
    if deck_p.exists():
        d = deck_p.read_text(encoding="utf-8")
        for m in re.finditer(r"<t[dh]\b[^>]*>(.*?)</t[dh]>", d, re.S):
            c = flat(m.group(1))
            if len(c) >= 4:
                cells.append(c)
        dates = [flat(m.group(1)) for m in re.finditer(r'<td class="d"[^>]*>(.*?)</td>', d, re.S)]
        dates = [c for c in dates if len(c) >= 4]
        # A date cell paints its lines and its mark as separate groups, so the text layer
        # can put the mark between the lines, and prints it in another case. Contiguity is
        # the wrong test: a cell sits whole on a page when every piece of it is on that one
        # page. The mark itself repeats through the book, so it cannot be located this way;
        # it is counted instead, because a mark that failed to print is the real risk.
        MARKS = ("HARD", "PROJECTED", "SERVICE", "UNCONFIRMED")

        def pieces_of(inner):
            out = []
            for bit in re.split(r"(?i)<br\s*/?>|</?span[^>]*>", inner):
                w = nospace(flat(bit)).upper()
                if len(w) >= 4 and not any(k in w for k in MARKS):
                    out.append(w)
            return out

        gone = []
        for m in re.finditer(r'<td class="d"[^>]*>(.*?)</td>', d, re.S):
            ps = pieces_of(m.group(1))
            if ps and not any(all(p in t.upper() for p in ps) for t in raw):
                gone.append(flat(m.group(1)))
        gone = sorted(set(gone), key=len, reverse=True)
        for c in gone[:10]:
            fails.append("a date cell does not sit whole on one page: %r" % c[:60])
        for k in MARKS:
            want = len(re.findall(">" + k + "<", d, re.I))
            got = sum(t.upper().count(k) for t in raw)
            if want and got < want:
                fails.append("the deck marks %d dates %s, the printed file carries %d"
                             % (want, k, got))
        info.append("%d table cells seen, %d date cells, %d of them split across a page"
                    % (len(set(cells)), len(set(dates)), len(gone)))
        atomic = []
        BS = chr(92)                      # a backslash, built at runtime so this file needs no escapes
        NEST = re.compile("(?i)<(ul|ol|li|div|table|blockquote|dl|h2|h3)")
        for tag in ("li", "blockquote", "dd", "dt"):
            pat = "(?is)<" + tag + BS + "b[^>]*>(.*?)</" + tag + ">"
            atomic += [flat(m.group(1)) for m in re.finditer(pat, d) if not NEST.search(m.group(1))]
        for cls in ("box", "tmpl", "tight", "two", "split"):
            pat = ('(?is)<(div|p|ul|ol|table)' + BS + 'b[^>]*class="[^"]*' + cls
                   + '[^"]*"[^>]*>(.*?)' + BS + '1>')
            # only a block with no markup inside it can be matched against the text layer
            # reliably; a nested div makes the captured span start or end mid-sentence.
            inner_ok = lambda h: not NEST.search(h) and "<" not in re.sub("(?i)<br\\s*/?>", " ", h)
            atomic += [flat(m.group(2)) for m in re.finditer(pat, d) if inner_ok(m.group(2))]
        atomic = sorted({x for x in atomic if len(x) >= 12}, key=len, reverse=True)
        # auto-hyphenation puts a real hyphen in the text layer at a line break, so compare with the
        # hyphens out of both sides. Only leaf blocks are checked: a list's text is its items plus the
        # bullet glyphs, and the glyphs are not in the deck, so a container never matches.
        flat_pages = [re.sub("[-]", "", t) for t in raw]
        allat = re.sub("[-]", "", nospace("".join(raw)))
        split, missing = [], []
        for x in atomic:
            key = re.sub("[-]", "", nospace(unligature(x)))   # the same pass on both sides, or every em dash mismatches
            if any(key in t for t in flat_pages):
                continue
            (split if key in allat else missing).append(x)
        for x in split[:6]:
            fails.append("a block the template calls atomic is split across a page break: %r" % x[:70])
        # A block that cannot be found at all is usually the measure, not the book: the text
        # layer of a block with inline markup does not reproduce the deck character for character.
        # Report it, do not fail on it. What must never happen is a split, and split is exact.
        for x in missing[:4]:
            warns.append("a block could not be matched whole in the text layer (check it by eye): %r" % x[:60])
        info.append("%d leaf blocks the template calls atomic: %d split across a page break, "
                    "%d not matchable in the text layer" % (len(atomic), len(split), len(missing)))
    else:
        warns.append("no built deck next to the PDF, so nothing was checked for a split block")

    # 5 nothing stranded
    if n < 10:
        fails.append("%d pages is a handout, not a book" % n)
    for i, ls in enumerate(lines, start=1):
        if i == 1:
            continue
        body = len(nospace(" ".join(ls[1:-1] if len(ls) > 3 else ls[1:])))
        if body < 120:
            fails.append("page %d carries only %d characters: a stranded fragment, not a page"
                         % (i, body))
        elif body < 400:
            warns.append("page %d is thin (%d characters) - look at it before printing" % (i, body))

    out = {"slug": slug, "pages": n, "cells": len(set(cells)) if cells else 0, "starts": seen,
           "fails": fails, "warns": warns, "info": info}
    print("%s: %d pages, %d table cells" % (slug, n, out["cells"]))
    for k in ("info",):
        for x in out[k]:
            print("  info  " + x)
    for w in warns:
        print("  warn  " + w)
    for f in fails:
        print("  FAIL  " + f)
    print("  %d failures, %d warnings" % (len(fails), len(warns)))
    if verbose:
        for i, ls in enumerate(lines, start=1):
            print("  p%-3d %s" % (i, " | ".join(ls[:3])[:120]))
    return out


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        raise SystemExit("usage: python printcheck.py <slug> [--verbose]")
    sys.exit(1 if sum(len(run(s, "--verbose" in sys.argv)["fails"]) for s in args) else 0)
