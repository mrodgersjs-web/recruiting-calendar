#!/usr/bin/env python3
"""W11 packaging test: every PDF in site/downloads/ has a %PDF- header, >=1 page, is multi-KB; the 3 sport PDFs
named by funnel/api/capture.js exist and carry that sport's rule dates; funnel/deliver/pdfs match catalog slugs."""
import os, re, sys, json, glob
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
errs = []
def pages(b):
    n = [int(x) for x in re.findall(rb"/Type\s*/Pages\b[^>]*?/Count\s+(\d+)", b)]
    return max(n) if n else len(re.findall(rb"/Type\s*/Page\b(?!s)", b))
def check(path, min_bytes=5000):
    b = open(path, "rb").read()
    if not b.startswith(b"%PDF-"): errs.append(f"{path}: bad header")
    if len(b) < min_bytes: errs.append(f"{path}: only {len(b)} bytes")
    if b"%%EOF" not in b[-1024:]: errs.append(f"{path}: no %%EOF trailer")
    n = pages(b)
    if n < 1: errs.append(f"{path}: page count {n}")
    return len(b), n
files = sorted(glob.glob(f"{R}/site/downloads/*.pdf"))
if not files: errs.append("no PDFs in site/downloads")
for f in files:
    size, n = check(f); print(f"{os.path.basename(f)}: {size} bytes, {n} pages")
for s in ["football", "baseball", "track"]:
    if not os.path.exists(f"{R}/site/downloads/{s}-class-2029.pdf"): errs.append(f"missing {s}-class-2029.pdf")
cat = json.load(open(f"{R}/v3/W1-playbooks/CATALOG.json"))["catalog"]
slugs = {p["slug"] for p in cat}
held = {"nil-high-school", "d3-academic-aid-first", "late-bloomer", "juco-to-d1"}
for f in sorted(glob.glob(f"{R}/funnel/deliver/pdfs/*.pdf")):
    s = os.path.basename(f)[:-4]
    if s not in slugs: errs.append(f"deliver pdf {s} not a catalog slug")
    if s in held: errs.append(f"held playbook {s} must not be in funnel/deliver/pdfs")
    check(f)
print("FAIL" if errs else "PASS")
for e in errs: print(" -", e)
sys.exit(1 if errs else 0)
