#!/usr/bin/env python3
"""W13-copy: repair what the first scrub pass missed.

scrub.py renamed the asset files and the page URLs, but it only rewrote
references of the form ax-<surname>-. The media folder also carries cut- and
real- files, and the story data keys its rows by surname id. Those references
were left pointing at files that no longer exist.

This pass fixes ids, every media path prefix, and the phrasing artifacts a
name-by-name swap produces. Run: python v3/W13-copy/fixrefs.py
"""
import re, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
DRY = "--dry" in sys.argv

SUR = {"butler": "jimmy", "coward": "cedric", "groenewegen": "sara", "lowe": "karsta",
       "marpet": "ali", "perez": "tori", "pichardo": "olivia", "pirosko": "samantha",
       "renfrow": "hunter", "rodriguez": "cristelle", "rodenfels": "annie",
       "white": "derrick", "wondolowski": "chris"}

FILES = ["site/assets/stories.js", "site/IMAGES.json", "site/data.js",
         "v3/W9-experiences/IMAGES.json", "v3/W9-experiences/INPUT.json",
         "v3/W1-stories/STORIES.json", "v3/W2-site/data.json",
         "v3/W2-seo/head-tags.json", "v3/W2-seo/jsonld/stories-articles.json",
         "v3/W2-scripts/SCRIPTS.json", "v3/W2-scripts/SCRIPTS.md",
         "v3/W2-video/manifest.json", "v3/W4-composites/make.py"]

# phrases the swap mangled, in the order they should be tried
ARTIFACTS = [
 ("(Sam Samantha)", "(Samantha)"), ("Sam Samantha", "Samantha"),
 ("(Chris Chris)", "(Chris)"),
 ("Chose a preferred walk-on spot at dream school", "Chose a preferred walk-on spot at his dream school"),
 ("a signed letter of intent with a D2 program", "signed her letter of intent with a D2 program"),
 ("Signed a signed letter of intent", "Signed a letter of intent"),
 ("high school quarterback at a suburban high school", "quarterback at a suburban high school"),
 ("at at ", "at "),
 (" and  ", " and "),
]


def fix_text(t: str) -> str:
    for sur, first in SUR.items():
        # "id": "renfrow" / "story": "renfrow" / slug fields
        t = re.sub(r'((?:id|story|slug|athlete|athlete_id)"\s*:\s*")' + sur + r'(")',
                   r"\g<1>" + first + r"\2", t)
        # single-quoted python keys in make.py
        t = re.sub(r'(?<=\')' + sur + r'(?=\'\s*:)', first, t)
        # media paths, any prefix
        t = re.sub(r"(/assets/media/)([a-z-]*?)-" + sur + r"-", r"\g<1>\g<2>-" + first + "-", t)
        t = re.sub(r"(assets/media/)([a-z-]*?)-" + sur + r"-", r"\g<1>\g<2>-" + first + "-", t)
        # bare file names inside IMAGES.json "file" arrays
        t = re.sub(r'("' + r"(?:ax|cut|real|hero|art)" + r"[-\w]*?)-" + sur + r"(-)", r"\g<1>-" + first + r"\2", t)
    for old, new in ARTIFACTS:
        t = t.replace(old, new)
    return t


def main():
    touched = 0
    for rel in FILES:
        p = ROOT / rel
        if not p.is_file():
            continue
        t = p.read_text(encoding="utf-8", errors="ignore")
        n = fix_text(t)
        if n != t:
            if not DRY:
                p.write_text(n, encoding="utf-8")
            touched += 1
    print(("would fix" if DRY else "fixed") + f": {touched} data files")
    left = []
    for p in (ROOT / "site").rglob("*"):
        if not (p.is_file() and p.suffix.lower() in {".html", ".js", ".json", ".xml"}):
            continue
        t = p.read_text(encoding="utf-8", errors="ignore")
        for sur in SUR:
            # a leftover is a bare surname, not a color word like "white female"
            for m in re.finditer(r'[">/:\'(\[]' + sur + r'[-".,/)>:\']', t):
                left.append((str(p.relative_to(ROOT)), m.group(0)))
    seen = set()
    uniq = [x for x in left if not (x in seen or seen.add(x))]
    print("leftover surname keys or paths:", len(uniq))
    for f, s in uniq[:12]:
        print("   ", f, s)


if __name__ == "__main__":
    main()
