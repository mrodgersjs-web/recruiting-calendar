# W2-seo drop-in pack (2026-11-05)
Drop `site/*` into repo `site/` (adds /answers/, sitemap.xml, robots.txt). Rebuild with `python3 build.py` (reads site/data.js, W1 CATALOG.json, STORIES.json).
- head-tags.json: path -> full <head> meta/OG/Twitter/canonical block for 59 pages (W2-1 pastes per page). META.md = review table.
- jsonld/: organization.json (every page), products.json (keyed by playbook slug), stories-articles.json (keyed by story id), faqpage-answers-hub.json.
- ANSWER-SOURCES.tsv: every rule/date/bylaw/URL on the 10 answer pages, all copied from site/data.js rows (verified_on 2026-11-05).
Assumptions / open items:
- Base URL https://recruiting-calendar.vercel.app (found in repo). Change BASE in build.py if a custom domain lands.
- og images assumed at /og/default.png and /logo.png: W2-1 must create them (W1-brand logo).
- Playbook URLs assumed /playbooks/<slug>/, stories /stories/<id>/. OUTLINE playbooks marked PreOrder in Product schema; prices are proposed (Mike approved showing them).
- Answer-page choice: DEMAND #1-#7 (scam, camps, level, exposure) are not rule questions and data.js has no source for them, so I wrote the 10 highest-mentioned questions that data.js can answer with a cited bylaw (#21 contact dates, #8 timing, #16 academics, #5 scholarships, #15 D3, #19 cost). No search-volume tool was used; "highest volume" = DEMAND mention counts, which are directional.
- Stories marked moderate/thin in STORIES.json (marpet, coward, pirosko) still get Article schema: W1-stories should verify before publish.
