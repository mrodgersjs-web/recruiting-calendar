# -*- coding: utf-8 -*-
"""fixsite5.py — the third storefront pass, W28.

Four things, all of them the auditor's, none of them arguable:

1. A tick for a sport with no book showed "10 Playbook in progress · Women's Lacrosse" in a
   190-pixel slot and was cut mid-word. The state is already carried by the dimmed bar and by
   the band on the card, so the tick now names the sport and nothing else.
2. The rail heading read "PLAYBOOKS FOR THIS SPORT · 0 PLAYBOOKS" over an empty list for three
   sports. An empty list is the finding, not a layout: the heading hides itself at zero, and
   one playbook reads as one playbook.
3. Two of the three bundle rows said a price and nothing else. A price with no contents reads
   as a typo, so each row now states what it holds and when it opens.
4. The phone Menu did nothing on the sport pages, because the script that owns it was never
   loaded there. That predates this lane; it is fixed here because this pass owns the pages.
   The same pass settles Lacrosse against Women's Lacrosse on the two cards that disagree.

Run from the lane root:  python fixsite5.py
"""
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = pathlib.Path(__file__).resolve().parent
SITE = HERE.parent.parent / 'site'
done = []

rj = SITE / 'assets/ring.js'
t = rj.read_text(encoding='utf-8')

OLD = "this.querySelector('[data-count]').textContent=a.playbooks.filter(ok).length+' playbooks';"
NEW = ("var _n=a.playbooks.filter(ok).length;"
       "this.querySelector('[data-count]').textContent=_n===1?'1 playbook':_n+' playbooks';"
       "this.querySelector('.sr__phead').style.display=_n?'':'none';")
if t.count(OLD) == 1:
    t = t.replace(OLD, NEW, 1)
    done.append('1  the rail heading hides itself over an empty list, and one playbook is one playbook')
else:
    print('1  NOT FOUND: %d copies of the count line' % t.count(OLD))

OLD = "${isPending(a)?PEND(a)+' \\u00b7 '+sp(a.sport):builtInfo(a).label}"
NEW = "${isPending(a)?sp(a.sport):builtInfo(a).label}"
if t.count(OLD) == 1:
    t = t.replace(OLD, NEW, 1)
    done.append('2  a pending tick names the sport and nothing else, so it stops being cut mid-word')
else:
    print('2  NOT FOUND: %d copies of the tick label' % t.count(OLD))

rj.write_text(t, encoding='utf-8')

t2 = (HERE / 'site.py').read_text(encoding='utf-8')
ANCH = "    if shelf.exists():"
INS = """    # The phone menu is driven by site.js, which the sport pages never loaded: the button sat
    # at the top of ten pages and did nothing at all.
    for page2 in sorted((SITE / 'sports').glob('*/index.html')) + [SITE / 'sports' / 'index.html']:
        b2 = page2.read_text(encoding='utf-8')
        if 'assets/site.js' not in b2 and '</body>' in b2:
            page2.write_text(b2.replace('</body>', '<script src="/assets/site.js" defer></script>\\n</body>', 1),
                             encoding='utf-8')
    # One card said Lacrosse, the shelf tile beside it said Women's Lacrosse. The book is for
    # girls' lacrosse, so the cards say what the shelf says.
    for page2 in [SITE / 'sports' / 'index.html', SITE / 'sports' / 'lacrosse' / 'index.html']:
        b2 = page2.read_text(encoding='utf-8')
        b3 = b2.replace('<b>Lacrosse</b>', "<b>Women's Lacrosse</b>")
        if b3 != b2:
            page2.write_text(b3, encoding='utf-8')
    # Two of the three bundle rows said a price and nothing else. The note pattern carries its
    # own search text, so a second pass leaves the row alone instead of stacking notes.
    hb = shelf.read_text(encoding='utf-8')
    for row, say in (
        ('Every Playbook', 'All nine playbooks, and each new one as it is written.'),
        ('Sideline membership', 'The calendar tool, once it exists. Not open at launch.'),
    ):
        hb = re.sub(r'(<b>' + re.escape(row) + r'</b>\\s*<span>[^<]*</span>)(?!\\s*<p class="note">)',
                    r'\\1 <p class="note">' + say + '</p>', hb, count=1)
    if hb != shelf.read_text(encoding='utf-8'):
        shelf.write_text(hb, encoding='utf-8')
""" + ANCH
assert t2.count(ANCH) == 1, 'the shelf block moved'
t2 = t2.replace(ANCH, INS, 1)
(HERE / 'site.py').write_text(t2, encoding='utf-8')
done.append('3  Every Playbook and the Sideline membership now say what they hold')
done.append("4  the sport pages load site.js, and the two Lacrosse cards agree with the shelf")

for d in done:
    print(d)
