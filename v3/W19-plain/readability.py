# -*- coding: utf-8 -*-
"""Reading-level audit for the playbook, prose only. Sentences from source
lists and bare labels are left out, because URLs and one-word table cells
make the formulas lie."""
import pathlib, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
W = re.compile(r"[A-Za-z][A-Za-z'\u2019\-]*")

def syl(w):
    w = re.sub(r"[^a-z]", "", w.lower())
    if not w: return 0
    if len(w) <= 3: return 1
    w = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", w); w = re.sub(r"^y", "", w)
    return max(1, len(re.findall(r"[aeiouy]{1,2}", w)))

def fk(sent):
    ws = W.findall(sent)
    if not ws: return None
    return 0.39 * len(ws) / max(1, 1) + 11.8 * (sum(syl(x) for x in ws) / len(ws)) - 15.59

def text_blocks(path):
    h = pathlib.Path(path).read_text(encoding="utf-8").split("</head>", 1)[1]
    h = re.sub(r"</(p|li|h1|h2|h3|td|th|tr|div|ol|ul|section|table|src)>", "\n", h)
    h = re.sub(r"<[^>]+>", " ", h)
    for a, b in {"&nbsp;": " ", "&middot;": "/", "&amp;": "&", "&rsquo;": "'"}.items(): h = h.replace(a, b)
    out = []
    for line in h.split("\n"):
        t = re.sub(r"\s+", " ", line).strip()
        if len(t) > 3 and not re.search(r"https?://|\.org|\.com|\.pdf|\.amazonaws", t):
            out.append(t)
    seen, uniq = set(), []
    for b in out:
        if b in seen: continue
        seen.add(b); uniq.append(b)
    return uniq

def audit(path, label):
    sents = []
    for b in text_blocks(path):
        for s in re.split(r"(?<=[.!?])\s+", b):
            ws = W.findall(s)
            if len(ws) >= 6: sents.append(s)
    tot_w = sum(len(W.findall(s)) for s in sents)
    tot_s = sum(syl(w) for s in sents for w in W.findall(s))
    grades = [fk(s) for s in sents]
    hard = sorted(zip(grades, sents), key=lambda r: -(r[0] or 0))
    over9 = [g for g in grades if g and g >= 9]
    long_s = [(len(W.findall(s)), s) for s in sents if len(W.findall(s)) >= 22]
    print("=== %s" % label)
    print("  sentences read: %d | words: %d | avg words per sentence: %.1f" % (len(sents), tot_w, tot_w / len(sents)))
    print("  Flesch-Kincaid grade level: %.1f | reading ease: %.1f | words of 3+ syllables: %.1f%%" % (
        0.39 * (tot_w / len(sents)) + 11.8 * (tot_s / tot_w) - 15.59,
        206.835 - 1.015 * (tot_w / len(sents)) - 84.6 * (tot_s / tot_w),
        100 * sum(1 for s in sents for w in W.findall(s) if syl(w) >= 3) / tot_w))
    print("  sentences at grade 9+: %d of %d (%.0f%%) | sentences of 22+ words: %d" % (len(over9), len(sents), 100 * len(over9) / len(sents), len(long_s)))
    for g, s in hard[:6]:
        print("    grade %4.1f  %s" % (g, s[:135]))
    print()

audit(r"v3\W18-bball-pdf\basketball-playbook.html", "BEFORE (the version Mike read)")
audit(r"v3\W19-plain\basketball-playbook-plain.html", "AFTER (plain rewrite)")
