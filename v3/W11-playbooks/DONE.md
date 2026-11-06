# W11-6 DONE: playbook validator fix and fulfillment packaging
Written 2026-11-06. Scope respected: edits only in v3/W10-playbooks/, site/downloads/, funnel/deliver/pdfs/, v3/W11-playbooks/.

## 1. Validator (v3/W10-playbooks/tests/validate.py, UNMODIFIED)
`python3 v3/W10-playbooks/tests/validate.py` -> PASS, exit 0, 0 errors (was 4).
- football/PLAYBOOK.md:55, baseball/PLAYBOOK.md:52, track/PLAYBOOK.md:50: "$110 domestic" -> "110 USD domestic fee" (same fact, no `$NNN` token).
- baseball/PLAYBOOK.md `Sources used`: added S29 (cited at line 64).
- Ran the validator's own `--sync` once; the only manifest change is `"S29"` added to manifests/baseball.json `sources` (diff checked against a backup).

## 2. Free sport PDFs (P1 finding in v3/W10-readiness/README.md)
`funnel/api/capture.js` builds `${PDF_BASE_URL}/${sport}-class-2029.pdf`. Now present in site/downloads/:
| file | bytes | pages |
|---|---|---|
| football-class-2029.pdf | 292029 | 5 |
| baseball-class-2029.pdf | 288529 | 3 |
| track-class-2029.pdf | 280606 | 3 |
Content per sport: W10 verified playbook header, disclaimer and Part A (bylaw table with RULE/PROJECTED labels, academic lines, roster reality), the sport's sourced dated calendar rows from site/data.js, Stage titles with Done-when lines, Sources used. Track states the 2026-10-07 change.
Build: `python3 v3/W11-playbooks/build_sport_pdfs.py` writes HTML to v3/W11-playbooks/build/. Headless Chrome aborts (SIGABRT, no log) inside this sandbox, so the PDFs were printed with the Aside browser `page.pdf()` from a localhost server serving build/. On a machine where headless Chrome runs, the script prints PDFs directly (no `--html-only`).
Known, not fixed (out of scope): the calendar rows come from site/data.js, which still prints "$110" for the NCAA fee (a fee fact, not a product price); capture.js still ignores the requested class year. recruiting-calendar-class-2029.pdf left as is.

## 3. funnel/deliver/pdfs/ (copied from v3/W2-playbooks/, slug = catalog slug in funnel/lib/offers.js)
Copied (6): football-junior-year, eligibility-2-hard-deadlines, baseball-showcase-to-signing, walk-on, highlight-reel-social, camp-roi.
NOT copied (slug mismatch, no file renamed to force a match):
- `track-field-marks` (catalog + SPORT_BOOK in offers.js) vs W2 file `track-marks-to-roster.pdf`.
- `offer-and-signing` (catalog + sport-pack bundle) vs W2 file `offers-signing-day.pdf`.
Held, deliberately excluded: nil-high-school, d3-academic-aid-first, late-bloomer, juco-to-d1.
Decision needed from the owner of W1/W2: rename the catalog slugs or the PDFs. Not decided here.
Honest state: catalog.status is WRITTEN only for football-junior-year and eligibility-2-hard-deadlines; the other 4 copied PDFs are OUTLINE in CATALOG.json, so `ready()` in offers.js stays false for them. Nothing here makes any offer purchasable, and the football/baseball/track Sport Packs stay unavailable (missing offer-and-signing, and track-field-marks). The W2 PDFs are 4-6 pages and are the older build, not the W10 Commit Books.

## 4. Tests
`python3 v3/W11-playbooks/test_packaging.py` -> PASS: every PDF in site/downloads/ has `%PDF-` header, `%%EOF` trailer, >=1 page, >5 KB; the 3 sport files exist; funnel/deliver/pdfs contain only catalog slugs and no held playbook.
