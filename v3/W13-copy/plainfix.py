#!/usr/bin/env python3
"""W13-copy: the plain-language pass, part 2.

Fixes what a name-by-name swap cannot: sentences that now read as repeated tier
labels, and insider shorthand a parent has to decode. Run with --dry to preview.
"""
import re, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
DRY = "--dry" in sys.argv
SCOPE = ["site", "v3/W9-experiences", "v3/W1-stories", "v3/W2-site", "v3/W2-seo",
         "v3/W2-scripts", "v3/W3-factcheck", "v3/W4-composites"]
EXTS = {".html", ".json", ".js", ".md", ".py", ".xml"}

# whole-sentence rewrites where the scrub left repeated tier labels
SENTENCES = {
 "Enter a time to compare against a D1 program, a D1 program, an Ivy League D1 program, a mid-major D1 program and a mid-major D1 program.":
   "Enter a time to compare it with five D1 programs that publish their standards.",
 "Men&#x27;s 400m as each D1 program publishes it: a D1 program &quot;consider for full aid&quot; 46.20; a mid-major D1 program &quot;scholarship&quot; 47.50; a D1 program &quot;walk on consideration&quot; 48.70; a mid-major D1 program &quot;target&quot; 49.60.":
   "The same event, the men&#x27;s 400m, as five D1 programs publish it: Program B wants 46.20 to consider full aid. Program D calls 47.50 a scholarship mark. Program A calls 48.70 walk-on consideration. Program E lists 49.60 as a target.",
 "Men's 400m as each D1 program publishes it: a D1 program \"consider for full aid\" 46.20; a mid-major D1 program \"scholarship\" 47.50; a D1 program \"walk on consideration\" 48.70; a mid-major D1 program \"target\" 49.60.":
   "The same event, the men's 400m, as five D1 programs publish it: Program B wants 46.20 to consider full aid. Program D calls 47.50 a scholarship mark. Program A calls 48.70 walk-on consideration. Program E lists 49.60 as a target.",
 "Programs: a D1 program, a D1 program, an Ivy League D1 program, a mid-major D1 program, a mid-major D1 program":
   "Programs: five D1 schools across three levels of competition",
}

# insider shorthand -> words a parent already knows
JARGON = [
 (r"\bPWO\b", "preferred walk-on"),
 (r"\bpREFERRED WALK-ON\b", "Preferred walk-on"),
 (r"\bChose preferred walk-on at\b", "Chose a preferred walk-on spot at"),
 (r"\bD1 \(FBS\)", "D1"),
 (r"\bD1 \(FCS\)", "D1"),
 (r"\(FBS\)", ""),
 (r"\(FCS\)", ""),
 (r"\bHS jr/sr\b", "junior and senior year of high school"),
 (r"\bHS jr year\b", "junior year of high school"),
 (r"\bHS sr year\b", "senior year of high school"),
 (r"\bHS years\b", "high school"),
 (r"\bHS\b", "high school"),
 (r"\bto soph year\b", "until sophomore year"),
 (r"\bsoph year\b", "sophomore year"),
 (r"\bJUCO\b", "JUCO"),
 (r"\bNLI\b", "a signed letter of intent"),
 (r"\beq\b", "equivalencies"),
 (r"\bQ&A\b", "questions and answers"),
]


def files():
    for base in SCOPE:
        p = ROOT / base
        if not p.exists():
            continue
        for f in p.rglob("*"):
            if f.is_file() and f.suffix.lower() in EXTS and "W13-copy" not in str(f):
                yield f


def main():
    n = 0
    for f in files():
        txt = f.read_text(encoding="utf-8", errors="ignore")
        new = txt
        for old, rep in SENTENCES.items():
            new = new.replace(old, rep)
        for pat, rep in JARGON:
            new = re.sub(pat, rep, new)
        new = re.sub(r"\s{2,}</", "</", new)
        if new != txt:
            if not DRY:
                f.write_text(new, encoding="utf-8")
            n += 1
    print(("would touch" if DRY else "touched") + f": {n} files")
    leftover = []
    for f in files():
        t = f.read_text(encoding="utf-8", errors="ignore")
        if re.search(r"\bPWO\b|\bHS\b|\(FBS\)|\bsoph\b", t):
            leftover.append(str(f.relative_to(ROOT)))
    print("files still holding shorthand:", len(leftover))
    for x in leftover[:8]:
        print("   ", x)


if __name__ == "__main__":
    main()
