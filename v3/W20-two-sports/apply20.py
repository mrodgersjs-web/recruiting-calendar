# -*- coding: utf-8 -*-
"""W20: apply a proofreader's FIND|||REPLACE list to a deck generator.

Matching is whitespace-flexible, because the generator is hard-wrapped and the
proofreader read the PDF text. A fix is skipped if it moves a number or a rule
reference: facts are not the proofreader's to change.
Usage: python apply20.py <generator.py> <fixes.txt>
"""
import pathlib, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

gen = pathlib.Path(sys.argv[1])
fixes = pathlib.Path(sys.argv[2])
src = gen.read_text(encoding="utf-8")
original = src

def flex(text):
    out = []
    for tok in re.split(r"\s+", text.strip()):
        out.append(re.escape(tok).replace("\\ ", "\\s+"))
    return r"\s+".join(out).replace("\ ", r"\s+")

def facts(text):
    """Digits and bylaw references, sorted. Must not change."""
    d = re.findall(r"\d[\d,\.]*", text)
    r = re.findall(r"\b1\d\.\d[\.\d]*", text)
    return (sorted(d), sorted(r))

applied = skipped = 0
for line in fixes.read_text(encoding="utf-8").splitlines():
    if "|||" not in line:
        continue
    find, repl = [p.strip() for p in line.split("|||", 1)]
    find = re.sub(r"\s+", " ", find)
    repl = re.sub(r"\s+", " ", repl)
    if len(find.split()) < 6:
        print("SKIP short find: %r" % find[:60]); skipped += 1; continue
    if facts(find) != facts(repl):
        print("SKIP facts moved: %r -> %r" % (find[:70], repl[:70])); skipped += 1; continue
    pat = re.compile(flex(find))
    m = pat.search(src)
    if not m:
        print("NOT FOUND: %r" % find[:90]); skipped += 1; continue
    src = src[:m.start()] + repl + src[m.end():]
    applied += 1

if src != original:
    gen.write_text(src, encoding="utf-8")
print("\n%s: applied %d, skipped %d" % (gen.name, applied, skipped))
