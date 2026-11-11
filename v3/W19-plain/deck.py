# -*- coding: utf-8 -*-
"""W19: pull the customer-visible text out of the playbook HTML, number the
blocks, and measure how hard it actually reads (Flesch-Kincaid grade +
Flesch reading ease + average sentence length)."""
import json, pathlib, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = pathlib.Path(r"C:\Users\Jloeh\Developer\recruiting-calendar")
OUT = REPO / "v3" / "W19-plain"
OUT.mkdir(parents=True, exist_ok=True)
html = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else REPO / "v3" / "W18-bball-pdf" / "basketball-playbook.html").read_text(encoding="utf-8")
html = html.split("</head>", 1)[1]

html = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S)
html = re.sub(r"<br\s*/?>", "\n", html)
html = re.sub(r"</(p|li|h1|h2|h3|td|th|tr|div|ol|ul|section|table)>", "\n", html)
html = re.sub(r"<[^>]+>", " ", html)
ent = {"&nbsp;": " ", "&middot;": "·", "&amp;": "&", "&mdash;": "--",
       "&rsquo;": "'", "&lsquo;": "'", "&ldquo;": '"', "&rdquo;": '"'}
for k, v in ent.items():
    html = html.replace(k, v)
blocks = []
for line in html.split("\n"):
    t = re.sub(r"\s+", " ", line).strip()
    if len(t) < 2 or re.fullmatch(r"[·\-\|/\\.,]*", t):
        continue
    blocks.append(t)

seen, ordered = set(), []
for b in blocks:
    if b in seen and len(b) < 60:
        continue
    seen.add(b)
    ordered.append(b)

words_re = re.compile(r"[A-Za-z][A-Za-z'’\-]*")


def syllables(w):
    w = re.sub(r"[^a-z]", "", w.lower())
    if not w:
        return 0
    if len(w) <= 3:
        return 1
    w = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", w)
    w = re.sub(r"^y", "", w)
    return max(1, len(re.findall(r"[aeiouy]{1,2}", w)))


def scores(text):
    sents = [s for s in re.split(r"(?<=[.!?:])\s+|\n", text) if words_re.findall(s)]
    words = words_re.findall(text)
    if not words or not sents:
        return None
    syl = sum(syllables(w) for w in words)
    W, S = len(words), len(sents)
    long_words = sum(1 for w in words if syllables(w) >= 3)
    return dict(words=W, sents=S, wps=round(W / S, 1),
                fk=round(0.39 * (W / S) + 11.8 * (syl / W) - 15.59, 1),
                ease=round(206.835 - 1.015 * (W / S) - 84.6 * (syl / W), 1),
                pct3=round(100 * long_words / W, 1))


full = "\n".join(ordered)
(OUT / "deck.txt").write_text("\n".join("[%03d] %s" % (i + 1, b) for i, b in enumerate(ordered)), encoding="utf-8")
(OUT / "blocks.json").write_text(json.dumps(ordered, indent=1, ensure_ascii=False), encoding="utf-8")

print("text blocks:", len(ordered), "| visible words:", len(words_re.findall(full)))
print("BASELINE, whole document:", scores(full))

hard = []
for i, b in enumerate(ordered):
    s = scores(b)
    if s and (s["fk"] >= 10 or s["wps"] >= 20):
        hard.append((i + 1, s, b))
hard.sort(key=lambda r: -r[1]["fk"])
print("\nblocks at grade 10+ or with a 20+ word sentence:", len(hard))
for idx, s, b in hard[:20]:
    print("  [%03d] grade %s ease %s words/sentence %s :: %s" % (idx, s["fk"], s["ease"], s["wps"], b[:118]))

brit = sorted({w for w in words_re.findall(full) if re.search(r"(?i)(programme|defence|counsellor|centre|behaviour|organis|recognis|analyse|licence|labour|colour|travelling|judgement|prioritis|realis|utilis)", w)})
print("\nBritish spellings:", brit)
pat = r"(?i)(went sideways|the upside|bites|bites families|wish, not a plan|on the board|keep your grades up|dissolves|scramble|roster math|half full|paper\b|air pocket|to the inch|in the family's voice|possession)"
idiom = [b for b in ordered if re.search(pat, b)]
print("blocks with idiom or insider phrasing:", len(idiom))
