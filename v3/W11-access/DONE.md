# W11-access: DONE (2026-11-06)

Built the interactive Access page from `v3/W7-access/ACCESS.md` and the tested `v3/W10-access` kit. Write scope respected: only `site/access/` and `v3/W11-access/`.

## Files (absolute)
- `/Users/rig128gb/Developer/recruiting-calendar/site/access/index.html` (page, 4 tools, design system: tokens.css + commit.css, nav to `/`, `/start`, `/recruitiq`, `/personalize`, `/segments`, `/emerging-sports`, `/price`)
- `/Users/rig128gb/Developer/recruiting-calendar/site/access/access.js` (DOM wiring)
- `/Users/rig128gb/Developer/recruiting-calendar/site/access/access-rules.js` (dates + bylaw table)
- `/Users/rig128gb/Developer/recruiting-calendar/site/access/access-core.js` (email/DM builder, linter, target list, CSV, .ics)
- `/Users/rig128gb/Developer/recruiting-calendar/site/access/access.css`
- `/Users/rig128gb/Developer/recruiting-calendar/site/access/deliverables/` : 7 files, byte-identical to `v3/W10-access/deliverables/` (6 worksheets: 1-send-date-worksheet.md, 2-questionnaire-checklist.md, 3-contact-scripts.md, 4-highlight-link-checklist.md, 5-ask-your-coach-one-pager.md, 6-follow-log.csv; plus 6-follow-log-README.md column guide)
- `/Users/rig128gb/Developer/recruiting-calendar/v3/W11-access/test_access_page.py`

## Tests (run 2026-11-06)
- `cd v3/W11-access && python3 -m unittest test_access_page` : **Ran 32 tests, OK** (also OK with `-W error::ResourceWarning`).
- `cd v3/W10-access && python3 -m unittest discover -s tests` : **Ran 49 tests, OK** (also re-run inside the W11 suite and asserted at exactly 49).
- Mutation check (suite can fail): wrong baseball date, corrupted bylaw number, form POST added each made the suite FAIL; restored, back to OK.
- Browser check (local static server, Aside browser): all four tools rendered, selecting Baseball / NCAA D1 / Class of 2029 gave Aug 1 2027 with "D1 Bylaws 13.1.3.1.1, 13.4.1.1 / D1-specific", linter flagged "my son" and "elite", 30 target rows, zero console errors, zero non-GET requests.

## Decisions and honest limits
- **Bylaw source of truth is `site/data.js`** (2026-27 NCAA D1 Manual, verified 2026-11-05), not `contact_kit.py`: the kit contains no bylaw numbers or dates by design (caller supplies D1 dates). The test therefore asserts every cite on the page exists in `data.js`, the kit contains none, and the two agree on the division model, NAIA source and 30-school cap / 0-10-24-45 cadence.
- Dates are the verified **Class of 2029** record shifted by whole years for 2026-2030. Football/baseball/track D1 dates, D2 and D3 official visits are from `data.js`. Unverified cells say "Not verified: ask the program" (D3 off-campus, all NJCAA) or "Any time" per the cited source (NAIA, D2/D3 coach contact). Football unofficial visits are "any time, subject to the calendar" per `answers/when-can-college-coaches-contact-my-kid`. Class years 2026-2027 are in the past or imminent for some rows; the page tells users to check the NCAA sport calendar.
- D2 official-visit/in-person date (June 15 after sophomore year) is verified only in the baseball record of `data.js`; applied to all three sports with a "confirm for your sport" note.
- **Target list has 5 tiers (5/8/5/6/6 = 30), not 6.** The brief named five tiers (Reach / Match / Academic-Aid / In-State / JUCO-or-NAIA safety) while saying "6-tier"; I built the five named and did not invent a sixth. Easy to add one in `AccessCore.TIERS`.
- Privacy: no fetch/XHR/beacon/storage/cookies in any script (tested); first-name-only field; no tel/address/last-name/email fields; no form action. Target list is lost on reload by design; page says to download first.
- Not done / out of scope: `/recruitiq`, `/personalize`, `/segments`, `/emerging-sports` nav links point to sibling-agent pages that did not exist at build time (`site/recruitiq` etc. absent). `site/sitemap.xml` and the home page were not touched (outside write scope), so `/access` is not yet linked from anywhere.
- Copy has not been through the s1gate/SlopMonster text gate or Mike's exact-text approval; per standing rules it must before publishing. Cancellation guide is education only, not legal advice; no company is named or accused.
