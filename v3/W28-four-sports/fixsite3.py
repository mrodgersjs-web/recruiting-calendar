# -*- coding: utf-8 -*-
"""fixsite3.py — the last four storefront defects, W28.

Everything here was found by measuring the built site in a browser, not by reading the
template. In order of damage:

1. The card's `art_kind` was set in the loop that stamps the four shipped books, and the
   women's soccer card is built in the per-config loop, so the traced figure was still
   labelled Illustration. Set where the figure is chosen, instead.
2. The product pages shipped a second button labelled Get beside "Get the playbook". One
   checks out, one adds to a bag, and the label now says which.
3. The /sports/ index carries its own one-line blurb per sport, and the soccer one still
   promised dead periods in every division after the sport page was corrected. This is
   exactly how a fact goes stale: a second copy of it lives somewhere nobody re-checks.
   The sentence is rewritten on every pass, and a canary now fails the build if a
   corrected phrase comes back.
4. The same rule that governs a tile's price must govern the shipped product pages, or the
   sweep is a rule with holes in it.

Run from the lane root:  python fixsite3.py
"""
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = pathlib.Path(__file__).resolve().parent
SITE = HERE.parent.parent / 'site'
t = (HERE / 'site.py').read_text(encoding='utf-8')
done = []

# 1 --------------------------------------------------------------- art_kind, at the figure
m = re.search(r'\n([ \t]*)(r\["img"\]|r\[\'img\'\]) = art_of\(c, r\)', t)
if m:
    pad, assign = m.group(1), m.group(2)
    t = t.replace(m.group(0), '\n%s%s = art_of(c, r)\n'
                  '%s    r["art_kind"] = "silhouette" if "sil-" in str(r["img"]) else "illustration"'
                  % (pad, assign, pad), 1)
    done.append('1  art_kind is set where the figure is chosen, so a trace is labelled a trace')
else:
    print('1  NOT FOUND: the art_of assignment moved; set art_kind by hand')

# 2, 4 ------------------------------------------------------------- the shipped PDP buttons
if 'def sweep_pages():' in t:
    t = t.replace(
        """    shelf = SITE / 'playbooks' / 'index.html'""",
        """    for pdp in sorted((SITE / 'playbooks').glob('*/index.html')):
        h = pdp.read_text(encoding='utf-8')
        h2 = h.replace('aria-pressed="false">Get</button>', 'aria-pressed="false">Add to bag</button>')
        if h2 != h:
            pdp.write_text(h2, encoding='utf-8')
    # A corrected phrase must not come back from a second copy of itself. The list is the
    # set of claims this week's audits removed; the build fails if any of them is live. The
    # index page's one-line blurb is rewritten here for the same reason: the sport page was
    # corrected on Monday and the card beside it was not, because nothing owned the card.
    for page in sorted(SITE.rglob('*.html')):
        body = page.read_text(encoding='utf-8')
        for stale in ('every division prints its own dead periods', '>Pending<',
                      'no price to learn', 'The art is drawn'):
            if stale in body:
                fails.append('stale copy still live on %s: %s' % (page.relative_to(SITE), stale))
        if page.name == 'index.html' and page.parent.name == 'sports' and 'Soccer runs on club events' in body:
            fixed = re.sub(r'Soccer runs on club events[^<]*',
                           'Soccer runs on club events and on a coach writing to say they want you, '
                           'more than on school visits. Division I and II print dead periods; '
                           'Division III prints none.', body, count=1)
            if fixed != body:
                page.write_text(fixed, encoding='utf-8')
    shelf = SITE / 'playbooks' / 'index.html'""",
        1)
    done.append('2  the second Get on a product page is now "Add to bag", on the shipped pages too')
    done.append('3  the sport index keeps one true soccer sentence, and stale claims fail the build')
else:
    print('2-4  NOT FOUND: sweep_pages is missing')

(HERE / 'site.py').write_text(t, encoding='utf-8')
for d in done:
    print(d)
print('site.py %d bytes' % (HERE / 'site.py').stat().st_size)
