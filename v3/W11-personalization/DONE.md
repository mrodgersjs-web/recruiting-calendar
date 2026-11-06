# W11-3 DONE: Denver Metro Personalization web page

Date: 2026-11-06. Scope: wrote only `site/personalize/` and `v3/W11-personalization/`.

## Built (`site/personalize/`)
| File | What it is |
|---|---|
| `index.html` | The page. Commit Book chrome (`/assets/tokens.css` + `commit.css`), then `personalize.css`. Sections A (intake), B (provenance cards), C (checklist), D (.ics). |
| `personalize.js` | Faithful JS port of W10 `engine.py`, `freshness.py`, `geo.py`, `ics.py`, `intake.py`. Works in browser (`window.CBPersonalize`) and Node (`require`). |
| `personalize.ui.js` | DOM glue: filters, cards, checklist, downloads. Extra file beyond the four named in the brief, kept separate so the engine port stays pure and testable. |
| `personalize.css` | Scoped `.pz-*` styles. `#0a0a0a` / `#f5f3ef` / `#d2321e`; Anton, Barlow Condensed, Inter Tight, JetBrains Mono come from `tokens.css`. Print stylesheet shows only the checklist. |
| `seed.json` | Byte-identical copy of `v3/W10-personalization/data/rows.seed.json` (12 rows). |
| `package.json` | `{"type":"commonjs"}`. Needed because the repo root is `"type":"module"`, which made `require('./personalize.js')` return an empty object under Node. |

## Requirement check
- **A. Intake.** Sport (Football, Baseball, Track & Field, Multi-sport), Category (Mental Performance / CMPC, Speed & Strength, Governing body / CHSAA, College ID Camp / Showcase), Verification (Verified / Listed), ZIP + radius (15 / 40 / 100 mi), monthly budget cap, graduating class. Only the five W10 allowlisted fields reach the engine (`sport, class_year, area, budget_band, goal_level`). ZIP is cut to 3 digits.
- **B. Cards.** Run through the ported engine with today's date. Past rows are hidden, undated event rows go to a separate "Not yet announced" group, stale rows are dropped. Toggle "Show historical/undated reference rows" shows past/undated rows labelled "reference only", never bookable. Each card shows badge, source URL, `read_on` date (labelled "Checked on"), miles, dates, price, flags.
- **C. Checklist.** 12 items: SB24-113 background check via consumer reporting agency, mandatory-reporter training, SafeSport, prohibited-conduct policy, one-on-one observation, insurance, emergency readiness, named coach + credential, CMPC/CSCS verification, refunds, contracts, no outcome promises. Print button and `.txt` download.
- **D. .ics.** Client-side, exports exactly the dated rows on screen. Output is byte-identical to Python `to_ics` for 7 intakes.

## Decisions and honest limits
- **"Vetted" is never shown.** Badge logic returns only `Verified` or `Listed`. W10 `Observed` rows display as `Listed`, because the brief defines Verified as a registry row and nothing else. The .ics description still says `Label: observed` because that is the engine's own string and parity with `ics.py` was the requirement.
- **Only 1 of 12 seed rows is Verified** (the AASP CMPC row). The page does not pad that.
- **CHSAA / governing-body category has zero rows in the seed.** The page says so ("Nothing is invented") instead of fabricating a calendar. Seed rows would need to be added by the research lane.
- **Track & Field matches only multi-sport providers.** The seed has no track-specific rows. The engine treats `multi` as a match for any sport, so Track and Baseball both surface the same multi-sport trainers. That is W10 behaviour, preserved on purpose.
- **Multi-sport filter** keeps only rows tagged `multi`.
- **Budget cap** is a view filter on the page (hides priced rows above the cap). Unpriced rows stay visible and flagged "price unknown", matching W10, where budget is a score input and not a hard filter. The brief says "monthly" but seed prices are per session, so the cap compares against the lowest listed per-session price. Read it as a rough cap, not a monthly total.
- **Distance** is straight-line miles from ZIP-prefix centers (Denver 802, Aurora 801, Golden 804, Boulder 803, Colo. Springs 809). Not drive time. An unknown ZIP3 shows "Unknown", never a guess. Labelled "Denver center" only for ZIP prefix 802.
- **SB26-100** is not cited as law (postponed indefinitely 2026-04-30). The CPR/AED item says it is not currently required by Colorado law.
- Not verified here: the legal wording of SB24-113 beyond what `PERSONALIZATION.md` section 5a quotes. Education, not legal advice, is stated on the page.

## Proof
- `python3 v3/W11-personalization/test_personalize_page.py` -> `Ran 28 tests ... OK` (also clean under `-W error::ResourceWarning`).
- The 28 include a subprocess run of W10's suite: `Ran 54 tests ... OK`, asserted equal to exactly 54.
- `v3/W11-personalization/mutation_check.sh` -> 15 mutants, 15 killed, 0 survived. First run had 3 survivors (future `read_on`, `vetted` label, checklist insurance); I added tests until they died.
- Parity: JS and Python engines agree on ranking order, scores, score parts, reasons, flags, hidden counts and `.ics` bytes across 7 intakes, plus a future-date run and a synthetic `vetted/endorsed` row.
- Zero minor PII: form controls are exactly 8 allowed ids; no `name/email/tel/date/file` inputs; `autocomplete=off`; no `<form action/method>`; no `fetch` except the static seed with `credentials: omit`; no storage, cookies, beacons or third-party scripts.
- Live browser run (local static server, Aside browser): 0 console errors. Exercised every filter, the bad-ZIP rejection, the historical toggle, a real `.ics` download (CRLF only) and a 390px mobile layout.
- Bug found by parity test and fixed: Python prints `0.0 mi`, JS printed `0 mi`.

## Not done
- Not linked from `site/index.html` or the nav (out of scope).
- Not deployed. Vercel `cleanUrls` should serve `/personalize`, but I only tested `/personalize/index.html` locally.
- No git commit.
