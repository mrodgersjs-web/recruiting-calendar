# W11-8 DONE (2026-11-06)
Status: built locally, DRAFT only. Nothing posted, launched, published or deployed.

## Deliverables
- `site/resources/{index.html,resources.js,resources.css,offers.json}`: third-party Gumroad directory. Headline "Third-Party Resource Directory — Created & Sold by McKinley Malbrough III on Gumroad", explicit not-authored-by-Commit-Book notice, 30 cards with verified `malbrough6.gumroad.com/l/...` links (`target=_blank rel="noopener noreferrer"`) and live-verified prices. Filters: Athlete story (21), Price ($0+ vs paid), Category (NIL, Coach Outreach, Recruiting Trackers, Mental/Performance, Parent Guides). 14 stories show 6 offers; 7 stories show 5 plus a gap notice (no 6th offer fabricated). Page is `noindex` until Mike releases it.
- `v3/W11-marketing/`: `CAMPAIGN-MATRIX.md`, `landing-page-map.json`, `cards.json`, `index.html` (interactive playbook: 15 draft creative cards, filter by segment/route), `test_resources_and_marketing.py`, build scripts (`build_offers.cjs`, `build_map.cjs`, `build_playbook.cjs`).

## Verification
- `python3 v3/W11-marketing/test_resources_and_marketing.py`: 16 tests, OK (30 URLs, prices vs LIVE-CHECK, 14x6 + 7x5 mapping vs STORY-OFFERS/GAPS, attribution text, design tokens, 6 segments, 7 routes, draft-only, write scope).
- Browser check on a local static server: wondolowski shows 5 cards + gap notice; renfrow+free = 1; NIL = 5; free = 5; paid = 25 of 30; all links carry the safe rel/target.

## Notes and deviations for the parent
1. **Paid range:** the brief said paid is $7-$45; the verified data includes bundles at $65 and $79, so the filter reads "Paid ($7-$79)". Free = 5 products at $0.
2. **Gap count:** ATTRIBUTION.md says 8 stories lack a sport-specific product; GAPS.json `fewer_than_six` lists 7 (matching the brief); the 8th (pichardo/groenewegen overlap) still gets 6. 7x5 used.
3. **Six segments:** MARKETING.json has 10 segments. The 6 paid-ad segments with drafted concepts are mapped (football, travel baseball/softball, club volleyball, wrestling incl. girls, AAU basketball, late-start jr/sr); flag football and track are small $50 tests; coaches/directors/first-gen are out of scope for paid.
4. **Routes not live:** only `/start` exists in `site/`. `/access`, `/recruitiq`, `/personalize`, `/segments`, `/emerging-sports` are mapped but not live; no ad may run until they are and Mike approves exact text. `/resources` itself is built but unreleased.
5. **Category assignment** (5 filter buckets) is my judgment per product (see `build_offers.cjs`); the source data had no categories. Review if wording matters.
6. **Rodenfels** story is HELD (noindex); directory notes that and the playbook says not to link offers from it.
7. Design: reused the live `/assets/tokens.css` (Anton / Barlow Condensed / Inter Tight / JetBrains Mono; #0a0a0a #f5f3ef #d2321e) rather than the older `site/style.css`.
8. Write scope respected: only `site/resources/` and `v3/W11-marketing/` written. Other modified files in git status belong to sibling agents.
