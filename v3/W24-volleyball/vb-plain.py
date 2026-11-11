# -*- coding: utf-8 -*-
"""Girls volleyball playbook, plain-language edition. Reuses the W19 house CSS.
Chapters live in cNN-*.html fragments so no single write is huge."""
import io, sys, re, html as htmllib, pathlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HEAD = open("head.txt", encoding="utf-8").read().replace(
    "Basketball: The Whole Pathway", "Volleyball: The Whole Pathway")
LOGO = open("mark.b64", encoding="utf-8").read().strip()

ORDER = [
    "c01-cover.html",
    "c02-ch01.html",
    "c03-ch02.html",
    "c04-ch03.html",
    "c05-ch04.html",
    "c06-ch05.html",
    "c07-ch06ab.html",
    "c08-ch06c.html",
    "c08b-ch06d.html",
    "c09-ch07.html",
    "c10-ch08.html",
    "c12-ch09-10.html",
    "c13-sources.html",
]

parts = []
for f in ORDER:
    p = pathlib.Path(f)
    if not p.exists():
        raise SystemExit("missing fragment: " + f)
    parts.append(p.read_text(encoding="utf-8").rstrip() + "\n")

DOC = HEAD + "\n".join(parts).replace("@@LOGO@@", LOGO)

# ---- sample email checks (the house rule: about 180 words, subject about 70 letters)
blocks = re.findall(r'<div class="tmpl">(.*?)</div>', DOC, re.S)
subj = htmllib.unescape(blocks[0]).strip()
body = htmllib.unescape(blocks[1]).strip()
words = len(re.findall(r"[A-Za-z0-9$.'’\-]+", body))
letters = len(re.sub(r"\s", "", subj))
DOC = DOC.replace("@@SUBJ@@", str(letters)).replace("@@WORDS@@", str(words))
DOC += "</body></html>\n"
open("vb-playbook-plain.html", "w", encoding="utf-8").write(DOC)
print("wrote vb-playbook-plain.html  %.1f KB, %d fragments, %d sections"
      % (len(DOC) / 1024.0, len(ORDER), DOC.count("<section")))
print("subject letters (no spaces): %d   |   body words: %d" % (letters, words))
print("subject: " + subj)
if not (160 <= words <= 195):
    print("  !! body word count is off the 180-word house rule")
if not (55 <= letters <= 80):
    print("  !! subject length is off the 70-letter guide")

# ---- real names must not appear inside the sample email
banned = ["Geneva", "Badger", "Bellamy", "Sting", "Marquette", "Nebraska", "Husker", "414"]
hits = [b for b in banned if b.lower() in body.lower()]
print("banned names inside sample email: " + (", ".join(hits) if hits else "none"))
print("Anytown mentions in the whole deck: %d | Impact Athletic Development: %d"
      % (DOC.count("Anytown"), DOC.count("Impact Athletic Development")))

sys.path.insert(0, ".")
from readability import audit
audit("vb-playbook-plain.html", "GIRLS VOLLEYBALL plain edition, before the proofreader")
