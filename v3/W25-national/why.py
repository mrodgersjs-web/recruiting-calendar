# -*- coding: utf-8 -*-
"""Why does the split gate call a block 'missing'? Rebuild one block's runs the same way the
gate does, then walk the page text character by character to print where it stops matching."""
import re, sys, html, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SRC = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
DUMP = pathlib.Path(sys.argv[2]).read_text(encoding="utf-8")
NEEDLE = sys.argv[3]
MINRUN = 22


def norm(t):
    t = html.unescape(t)
    for junk in ("\ufffe", "\u00ad", "-", "\u2014", "\u2013"):
        t = t.replace(junk, "")
    t = t.replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
    return re.sub(r"\s+", "", t).lower()


pages = re.split(r"===== PAGE (\d+) =====", DUMP)
pn = {pages[i]: norm(pages[i + 1]) for i in range(1, len(pages) - 1, 2)}

# every run in the source, with the block it came from
for m in re.finditer(r'<div class="(box[^"]*|tmpl)">\s*(.*?)</div>|<(table|ul|ol)([^>]*)>(.*?)</\3>', SRC, re.S):
    frag = m.group(2) or m.group(5)
    for run in [norm(x) for x in re.split(r"<[^>]+>", frag)]:
        if len(run) < MINRUN or norm(NEEDLE) not in run:
            continue
        print("RUN  (%d chars): %s..." % (len(run), run[:80]))
        for p, txt in sorted(pn.items(), key=lambda kv: int(kv[0])):
            if run in txt:
                print("   found whole on page %s" % p)
                break
        else:
            # longest prefix of the run that survives on any page, and what follows it there
            best = (0, None, None)
            for p, txt in pn.items():
                for n in range(len(run), MINRUN, -20):
                    i = txt.find(run[:n])
                    if i >= 0:
                        if n > best[0]:
                            best = (n, p, txt[i + n:i + n + 60])
                        break
            print("   not whole. longest match %d chars on page %s" % (best[0], best[1]))
            print("   source continues : ...%s" % run[best[0]:best[0] + 60])
            print("   pdf continues    : ...%s" % (best[2] or ""))
            sys.exit(0)
