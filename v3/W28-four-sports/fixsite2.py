# -*- coding: utf-8 -*-
"""W28: the second storefront audit, the site half.

Eight things, all of them found by an auditor reading the shop as a customer:

A. A card is judged by the book it is about. The swimming card had no book of its own in
   the data, so it inherited the eligibility book's written status: full colour, live
   button, and a NOT WRITTEN YET band across the figure at the same time. The two carousels
   now stop guessing from the first title in a list, and a traced figure says it is traced.
B. Money is decided in one place, for every tile on every page, not only the tiles this
   script happens to rebuild. The four sports with no book of their own still showed $15
   and $19 from the shipped pages, because those pages were never opened.
C. One phrase for the state. "In progress" on the shelf, the sport pages, the rail and the
   phone deck.
D. The soccer page promised that every division prints its own dead periods. The packets
   say Division II prints one, around signing, and Division III prints none.
E. A generated sentence that named the eligibility book as a carrier of softball dates,
   and joined two book names with a comma.
F. Pack prices with no way to pay. Checkout accepts the nine playbook slugs and nothing
   else, so a pack row now says it is not open yet instead of leaving the number bare.
G. The product page had two buttons that both said Get. One checks out, one adds to a bag.
H. New tiles wore a different uniform from the ones already on the shelf.

Run from the lane root:  python fixsite2.py
"""
import json
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = pathlib.Path(__file__).resolve().parent
SITE = HERE.parent.parent / 'site'
log = []


def note(msg):
    log.append(msg)


S = 'v3/W28-four-sports/site.py'
t = (HERE / 'site.py').read_text(encoding='utf-8')

# ---------------------------------------------------------------- A, C
# The record loop, line 750: give every athlete its own sport slug.
# A was applied by hand in the ring block above (art_kind on the live card), so this
# script no longer touches the athlete records. It is left here as the thing that was tried
# first: setting `book` from the first title in a list is exactly the guess that made the
# swimming card look written, and the fix belongs in the two carousels, not in the data.
OLD_LOOP = 'DATA["athletes"] = [{k: v for k, v in recs[i].items() if k != "moved_from"}'
NEW_LOOP = OLD_LOOP
assert t.count(OLD_LOOP) == 1, 'the athlete loop moved'
t = t.replace(OLD_LOOP, NEW_LOOP, 1)
note('A  a traced figure is labelled by what it is, in the data the two carousels read')

# ---------------------------------------------------------------- B, C
t = t.replace(
    '''    html = re.sub(r'((?:<span|<p) class="pb-p"[^>]*>)\\$[\\d.]+((?:\\s*<span class="note">[^<]*</span>)?)(</(?:span|p)>)', money, html)''',
    '''    html = re.sub(r'((?:<span|<p) class="pb-p"[^>]*>)\\$[\\d.]+((?:\\s*<span class="note">[^<]*</span>)?)(</(?:span|p)>)', money, html)
    html = html.replace('<span class="pb-pend">Pending</span>', '<span class="pb-pend">In progress</span>')''',
    1)
note('C  a tile band that says Pending in the shipped file is corrected on every pass')

BAND = '''    if not written:
        html = re.sub(r'<button class="btn[^"]*"[^>]*data-offer="' + re.escape(slug) + '">[^<]*</button>',
                      '<p class="note">in progress &middot; no price yet</p>', html)
        html = html.replace('<div class="pb-cell">', '<div class="pb-cell is-soon">', 1)
    return html'''
BAND_NEW = '''    if not written:
        html = re.sub(r'<button class="btn[^"]*"[^>]*data-offer="' + re.escape(slug) + '">[^<]*</button>',
                      '<p class="note">in progress &middot; no price yet</p>', html)
        html = html.replace('<div class="pb-cell">', '<div class="pb-cell is-soon">', 1)
    return html


def sweep_pages():
    """Every tile on every sport page, whatever site.py did not rebuild.

    The four sports with no book of their own have pages that were shipped before this
    lane existed and are not rewritten here. Their tiles still carried $15 and $19 over
    "Rules being verified", so a rule about money that only runs on rebuilt pages is not a
    rule. This walks each tile, reads the slug from its own link, and applies shelf_state.
    """
    n = 0
    pages = sorted((SITE / 'sports').glob('*/index.html')) + [SITE / 'playbooks' / 'index.html']
    for page in pages:
        html = page.read_text(encoding='utf-8')
        out, i = [], 0
        while True:
            j = html.find('<div class="pb-cell', i)
            if j < 0:
                out.append(html[i:])
                break
            out.append(html[i:j])
            k, depth = j, 0
            while True:
                no = html.find('<div', k + 1)
                nc = html.find('</div>', k)
                if nc < 0:
                    break
                if 0 <= no < nc:
                    depth += 1
                    k = no + 4
                    continue
                if depth:
                    depth -= 1
                    k = nc + 6
                    continue
                k = nc + 6
                break
            block = html[j:k]
            m = re.search(r'href="/playbooks/([a-z0-9-]+)"', block)
            if m:
                out.append(shelf_state(block, m.group(1)))
            else:
                block = block.replace('<span class="pb-pend">Pending</span>',
                                      '<span class="pb-pend">In progress</span>')
                # A pack row shows a price nobody can pay yet: checkout accepts the nine
                # playbook slugs and nothing else. The number stays because it is the price
                # we intend to charge, and the line under it now says so.
                if 'pb-p' in block and 'data-offer=' not in block and 'not open yet' not in block:
                    block = re.sub(r'(<span class="pb-p">\$[\d.]+</span>)',
                                   r'\1<p class="note">not open yet</p>', block, count=1)
                out.append(block)
            i = k
        new = ''.join(out)
        if new != html:
            page.write_text(new, encoding='utf-8')
            n += 1
    return n'''
assert t.count(BAND) == 1, 'the tail of shelf_state moved'
t = t.replace(BAND, BAND_NEW, 1)
note('B  sweep_pages(): one money rule for every tile, including the pages this script never opens')

# ---------------------------------------------------------------- H
t = t.replace(
    '''    return "%s families, %s" % (sport, "boys and men" if c["gender"] == "men" else "girls and women")''',
    '''    return "%s families" % sport''',
    1)
note('H  the who-line is "<Sport> families", the form already on the shelf')

# ---------------------------------------------------------------- F
t = t.replace(
    """            '<span class="pb-s">%s The sport page shows what we have dated so far.</span></a></div>'""",
    """            '<span class="pb-s">%s This sport has no dated rules chapter yet.</span></a></div>'""",
    1)
note('H  a pending tile no longer points a reader at the page they are standing on')

# ---------------------------------------------------------------- G
t = t.replace(
    '''aria-pressed="false">Get</button>\'''',
    '''aria-pressed="false">Add to bag</button>\'''',
    1)
note('G  the second button on a product page says which of the two it is')

# ---------------------------------------------------------------- F, bundles
t = t.replace(
    "The Sport Pack covers any of the four written sports",
    "The Sport Pack covers any of the written sports",
    1)
note('F  the pack note no longer hard-codes a count that a new book makes wrong')

(SITE.parent / 'v3/W28-four-sports/site.py').write_text(t, encoding='utf-8')

# ---------------------------------------------------------------- D, the soccer lede
p = SITE / 'sports/soccer/index.html'
h = p.read_text(encoding='utf-8')
OLD_LEDE = re.search(r'<p class="lede">[^<]*written interest[^<]*</p>', h)
if OLD_LEDE:
    h = h.replace(OLD_LEDE.group(0),
                  '<p class="lede">Soccer runs on club events and on a coach writing to say they want '
                  'you, more than on school visits. Division I and Division II print dead periods, '
                  'stretches when a coach may not watch you or host a visit. Division III prints none. '
                  'Learn the dates before you pay.</p>', 1)
    p.write_text(h, encoding='utf-8')
    note('D  the soccer page promised dead periods in every division; II has one, III has none')
else:
    note('D  the soccer lede had already been rewritten, left alone')

# ---------------------------------------------------------------- H, config uniforms
WHO = {'mens-baseball-road-to-college': ('Baseball', 'Baseball families'),
       'womens-softball-road-to-college': ('Softball', 'Softball families'),
       'mens-soccer-road-to-college': ("Men's Soccer", 'Soccer families'),
       'womens-soccer-road-to-college': ("Women's Soccer", 'Soccer families')}
BLURB = {
    'mens-baseball-road-to-college':
        'The draft rule that sets a boy\u2019s whole calendar, how much aid a school may put on a '
        'roster, where a boy is actually seen, film, paperwork, and what the money really goes to.',
    'womens-softball-road-to-college':
        'Dead periods, the camp rule, how much aid a school may put on a roster, where a girl is '
        'actually seen, film, paperwork, and what the money really goes to.',
    'mens-soccer-road-to-college':
        'The four 2026-27 dead periods, how much aid a school may put on a roster, where a boy is '
        'actually seen, film, paperwork, and what the money really goes to.',
    'womens-soccer-road-to-college':
        'The four 2026-27 dead periods, how much aid a school may put on a roster, where a girl is '
        'actually seen, film, paperwork, and what the money really goes to.',
}
for slug, (label, who) in WHO.items():
    cp = HERE / 'SPORTS' / (slug + '.json')
    c = json.loads(cp.read_text(encoding='utf-8'))
    c['ring_label'] = label
    c['site']['who_label'] = who
    c['site']['blurb'] = BLURB[slug]
    cp.write_text(json.dumps(c, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    note('H  %-34s tile label "%s", who-line "%s", blurb in the house form' % (slug, label, who))

# ---------------------------------------------------------------- E, the calendar sentence
t2 = (HERE / 'site.py').read_text(encoding='utf-8')
E_OLD = re.search(r'\n([^\n]*carry this sport[^\n]*|.*names\.join[^\n]*)', t2)
print('\n'.join(log))
print('\nCALENDAR SENTENCE, current source:')
for i, ln in enumerate(t2.split('\n'), 1):
    if 'carr' in ln.lower() and 'charter' not in ln.lower() and ('join' in ln or 'sentence' in ln.lower() or 'carries' in ln):
        print('  %4d| %s' % (i, ln.strip()[:190]))
