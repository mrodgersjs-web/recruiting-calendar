"""W11 verification: resource directory + marketing pack. Offline; reads W10 sources + site/resources + W11 outputs."""
import json, re, unittest
from pathlib import Path
R = Path(__file__).resolve().parents[2]
W10, W7, W11, RES = R/'v3/W10-offers', R/'v3/W7-marketing', R/'v3/W11-marketing', R/'site/resources'
J = lambda p: json.loads(Path(p).read_text())
LIVE, OFFERS, STORY, GAPS = J(W10/'LIVE-CHECK.json'), J(W10/'OFFERS.json'), J(W10/'STORY-OFFERS.json'), J(W10/'GAPS.json')
DIR = J(RES/'offers.json')
HTML, JS = (RES/'index.html').read_text(), (RES/'resources.js').read_text()
URL = re.compile(r'^https://malbrough6\.gumroad\.com/l/[a-z0-9-]+$')

class Gumroad(unittest.TestCase):
    def test_30_urls(self):
        self.assertEqual(len(DIR['offers']), 30)
        self.assertEqual(len({o['href'] for o in DIR['offers']}), 30)
        for o in DIR['offers']:
            self.assertRegex(o['href'], URL)
            self.assertTrue(o['href'].endswith('/l/'+o['slug']))
    def test_prices_match_live_check(self):
        lv = {l['slug']: l for l in LIVE}
        self.assertEqual(set(lv), {o['slug'] for o in DIR['offers']})
        for o in DIR['offers']:
            l = lv[o['slug']]
            self.assertEqual(l['http'], 200)
            self.assertEqual(o['price'], float(l['live_price']))
            self.assertEqual(o['price'], OFFERS[o['slug']]['price'])
            self.assertEqual(o['href'], l['url'])
            self.assertIn('$'+str(int(o['price'])) if o['price'] else '$0', o['price_label'])
    def test_free_vs_paid_split(self):
        free = [o for o in DIR['offers'] if o['free']]
        self.assertTrue(free); self.assertTrue(all(o['price'] == 0 for o in free))
        self.assertTrue(all(o['price'] >= 7 for o in DIR['offers'] if not o['free']))
    def test_categories(self):
        self.assertEqual(DIR['categories'], ['NIL','Coach Outreach','Recruiting Trackers','Mental/Performance','Parent Guides'])
        for c in DIR['categories']:
            self.assertTrue(any(o['category'] == c for o in DIR['offers']), c)
        self.assertTrue(all(o['category'] in DIR['categories'] for o in DIR['offers']))
    def test_links_safe_in_js(self):
        self.assertIn("a.target='_blank'", JS); self.assertIn("a.rel='noopener noreferrer'", JS)
        self.assertIn('o.price_label', JS); self.assertIn('o.href', JS)

class StoryMapping(unittest.TestCase):
    def test_21_stories_14x6_7x5(self):
        self.assertEqual(len(DIR['stories']), 21)
        gap = {g['story'] for g in GAPS['fewer_than_six']}
        self.assertEqual(len(gap), 7)
        for s in DIR['stories']:
            self.assertEqual(len(s['offers']), len(set(s['offers'])))
            if s['slug'] in gap:
                self.assertEqual((s['count'], len(s['offers'])), (5, 5), s['slug']); self.assertTrue(s['gap'])
            else:
                self.assertEqual((s['count'], len(s['offers'])), (6, 6), s['slug']); self.assertIsNone(s['gap'])
        self.assertEqual(sum(1 for s in DIR['stories'] if s['count'] == 6), 14)
        self.assertEqual(sum(1 for s in DIR['stories'] if s['count'] == 5), 7)
    def test_matches_source_and_no_fabrication(self):
        slugs = {o['slug'] for o in DIR['offers']}
        for s in DIR['stories']:
            src = [x['slug'] for x in STORY[s['slug']]['offers']]
            self.assertEqual(s['offers'], src)
            self.assertTrue(set(s['offers']) <= slugs)
    def test_gap_notice_rendered(self):
        self.assertIn('st.gap', JS); self.assertIn("'Only '+st.count+' verified offers", JS)
    def test_rodenfels_held(self):
        s = next(x for x in DIR['stories'] if x['slug'] == 'rodenfels')
        self.assertTrue(s['held']); self.assertIn('HELD', s['no_sport_specific'])

class Attribution(unittest.TestCase):
    def test_headline_and_notice(self):
        self.assertIn('Third-Party Resource Directory — Created &amp; Sold by McKinley Malbrough III on Gumroad', HTML)
        self.assertIn('malbrough6.gumroad.com', HTML)
        self.assertIn('independent third-party downloads hosted on Gumroad', HTML)
        self.assertIn('not authored by The Commit Book', HTML)
        self.assertIn('30 sports resources', HTML)
        self.assertIn('Educational material, not legal, tax or financial advice', HTML)
        self.assertIn('By McKinley Malbrough III, MM3 Sports. Educational material, not legal, tax or financial advice.', DIR['attribution'])
    def test_each_card_attributed(self):
        self.assertIn('By McKinley Malbrough III, MM3 Sports', JS)
    def test_design_system(self):
        css = (RES/'resources.css').read_text()
        for t in ('#0a0a0a', '#f5f3ef', '#d2321e', 'Anton', 'Barlow Condensed', 'Inter Tight', 'JetBrains Mono'):
            self.assertIn(t, css, t)
        for f in ('resources.css', 'resources.js', 'offers.json'): self.assertTrue((RES/f).exists())

ROUTES = ['/start','/access','/recruitiq','/personalize','/segments','/emerging-sports','/resources']
class Marketing(unittest.TestCase):
    M = J(W7/'MARKETING.json'); MAP = J(W11/'landing-page-map.json')
    def test_routes_and_six_segments(self):
        self.assertEqual(list(self.MAP['routes']), ROUTES)
        self.assertEqual(len(self.MAP['buyer_segments']), 6)
        used = set()
        for s in self.MAP['buyer_segments']:
            self.assertIn(s['primary_route'], ROUTES)
            self.assertTrue(set(s['secondary_routes']) <= set(ROUTES))
            self.assertIn(s['id'], self.M['segments'])
            self.assertEqual(s['ads'], self.M['segments'][s['id']]['ads'])
            self.assertEqual(s['stories'], self.M['segments'][s['id']]['stories'])
            self.assertIn(s['resources_story_filter'], {x['slug'] for x in DIR['stories']})
            used |= {s['primary_route'], *s['secondary_routes']}
        self.assertEqual(used, set(ROUTES))
    def test_stories_exist(self):
        slugs = {x['slug'] for x in DIR['stories']}
        for s in self.MAP['buyer_segments']: self.assertTrue(set(s['stories']) <= slugs)
    def test_draft_only(self):
        self.assertIn('DRAFT', self.MAP['status'])
        cards = J(W11/'cards.json')
        self.assertEqual(cards['status'], 'DRAFT')
        self.assertTrue(all('DRAFT' in c['status'] and c['new_route'] in ROUTES for c in cards['cards']))
        ids = {c['id'] for c in cards['cards']}
        self.assertEqual(ids, {a for s in self.M['segments'].values() for a in s['ads']})
        md = (W11/'CAMPAIGN-MATRIX.md').read_text()
        self.assertIn('100% DRAFT', md)
        for r in ROUTES: self.assertIn(r, md)
        self.assertIn('third-party', md)
        self.assertIn('HELD', md)
        pb = (W11/'index.html').read_text()
        self.assertIn('Draft only', pb)
    def test_write_scope(self):
        self.assertTrue({p.name for p in RES.iterdir()} == {'index.html','resources.js','resources.css','offers.json'})

if __name__ == '__main__': unittest.main(verbosity=2)
