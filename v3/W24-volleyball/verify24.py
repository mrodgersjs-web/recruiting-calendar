# -*- coding: utf-8 -*-
"""Fact audit for the volleyball deck: pull every dollar figure, percentage, stat line,
roster count and quoted height out of the assembled HTML and check that the same token
appears somewhere in the six research files. Anything that does not is either derived
(arithmetic this book did) or wrong. Prints both groups for a human read."""
import re, sys, pathlib, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LANE = pathlib.Path(__file__).parent
DOC = html.unescape(re.sub(r"<[^>]+>", " ", (LANE / "vb-playbook-plain.html").read_text(encoding="utf-8")))
DOC = re.sub(r"\s+", " ", DOC)
RES = " ".join(p.read_text(encoding="utf-8", errors="replace") for p in sorted((LANE / "research").glob("*.md")))
RES = html.unescape(RES)
RESN = RES.replace(",", "")

money = sorted(set(re.findall(r"\$[\d,]+(?:\.\d\d)?", DOC)), key=len)
stats = sorted(set(re.findall(r"\d\.\d\d(?![\d])", DOC)))
pcts = sorted(set(re.findall(r"\d+(?:\.\d)? percent", DOC)))
hts = sorted(set(re.findall(r"\d'\d{1,2}\"", DOC)))
counts = sorted(set(re.findall(r"\b\d{2,4} players\b", DOC)))


def report(label, toks):
    print("\n=== %s: %d tokens ===" % (label, len(toks)))
    miss = []
    for t in toks:
        if t in RES:
            continue
        bare = re.sub(r"[^0-9.]", "", t)
        if bare and (bare in RESN or bare.lstrip("0") in RESN or ("0." + bare) in RESN):
            continue
        miss.append(t)
    print("found   :", " ".join(t for t in toks if t not in miss))
    print("MISSING :", " ".join(miss) if miss else "none")


report("dollar amounts", money)
report("two-decimal stat lines", stats)
report("percentages", pcts)
report("heights and touches", hts)
report("player counts", counts)

print("\n=== sentences naming a roster size or a seat count ===")
for m2 in re.finditer(r"[^.]{0,100}\b(?:players|seats|roster limit|equivalents)\b[^.]{0,50}\.", DOC):
    frag = m2.group(0).strip()
    if re.search(r"\d", frag):
        digits = re.findall(r"\d+", frag)
        tag = "OK" if all(d.replace(",", "") in RESN for d in digits) else "??"
        print("  %s  %s" % (tag, frag[:150]))
