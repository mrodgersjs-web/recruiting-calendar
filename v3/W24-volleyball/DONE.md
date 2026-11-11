# W24 - Women's volleyball playbook (sample), house format

Requested 11 Nov 2026 by Mike, verbatim: "Let's get one more sport, full work up, using
everything we have already implemented - Women's Volleyball. Full workup, run down, using
same formatiing and language."

Everything already implemented = the W19 house CSS, the W21 print rules (blocks move whole,
only `class="flow"` grids split, one chapter per fresh page), the W22 email research
(subject as a label, ~180-word body, two links, no login wall, follow-up cadence) and the
W23 placeholder rule (no real school, club, camp, circuit or service name inside a sample
email or subject line).

## What is in the lane

* `research/01..06.md` - six research files, 227 KB, ~540 claims, each tagged
  OFFICIAL / COACH / SERVICE / DATA / FOLKLORE / UNCONFIRMED with a URL and "Checked
  2026-11-11", each ending with a "Could not settle" list. 01 numbers and rules, 02
  measurables by position, 03 club season and events, 04 film and outreach, 05 costs and
  value, 06 paperwork and the boys lane.
* `cNN-*.html` - the deck in 13 chapter fragments, so no single write is huge.
* `vb-plain.py` - assembles `head.txt` + the fragments in its ORDER list, injects
  `mark.b64` into `@@LOGO@@`, measures the sample email and fills its own `@@SUBJ@@` and
  `@@WORDS@@` labels, writes `vb-playbook-plain.html`, then runs `readability.audit`.
* `vbqa.py` - per-page text dump (`vb-text.txt`), header / footer / page-number check, page
  peek, chapter-start map.
* `verify24.py` - pulls every dollar figure, stat, percentage, height and player count out
  of the assembled deck and checks each one against the six research files. The only tokens
  that do not appear in research are CSS values, the invented sample-email numbers, and four
  sums this book did itself, each labelled as an estimate in the page that prints it.
* `sheet24.py` - contact sheet and the email-page proof.

## Print QA (vb.pdf, 31 pages)

* 31 pages. Header, footer and the correct `N / 31` on every page: 0 failures.
* Chapters start on a fresh page: ch1 p3, ch2 p5 and p6, ch3 p8, ch4 p10, ch5 p12,
  ch6 p14 / p16 / p17 / p19, ch7 p21, ch8 p23 / p26, ch9 p28, ch10 p29, ch11 p30.
* Only the flow grids cross a page boundary, and each continuation repeats its header row
  (calendar p9, price list p24 and p25, sources p31).
* The sample email sits whole on one page: 178 words, subject 73 letters, zero banned names.
* Thin pages left: the brother box, the closing box of the outreach chapter, the price-grid
  tail and the free-things list tail. That is the accepted cost of the W21 whole-block rule,
  the same trade the football and girls basketball decks make.
* Reading level: Flesch-Kincaid grade 5.7, 10,800 words, 11.4 words per sentence average,
  13 sentences over 22 words. Every flagged over-grade line is a proper noun in the sources
  chapter, not teaching text.

## Deliberate calls

* Jump, reach and block figures are printed as **SERVICE targets**, never as rules, set
  against counted roster heights from 11 nearby college rosters. No program publishes
  approach numbers, and one service's chart has a row labelled "weight" that holds heights.
* Contact and visit dates come from USA Volleyball's own recruiting timeline, not from a
  club-hosted 2026-27 rules sheet: that sheet says Division II communication is allowed "any
  time", which USAV's page contradicts.
* The 2022 AVCA camp-conversation rule is printed with a visible flag: not re-checked
  against the 2026-27 manual.
* Camp invite is not interest, carried by USAV and JVA quotes rather than opinion.
* The boys lane is one box in chapter 2, labelled as thinner evidence.
* Two roster rows were cut during the fact audit because no research file carried them
  (Northern Michigan, and a second-hand "21 players" line). Everything printed now traces to
  a roster page, an association page or a named quote.

## Honest gaps, printed in chapter 11

Which Division I schools opted in (no published list); her own signing date and the dead
period around it (both derived from the second-Wednesday rule); the camp rule for 2026-27;
the real Eligibility Center fee ($120 on the live page, $110 in the association's own guide,
$75 athletics-only); whether Division II still uses the old letter (two NCAA pages disagree);
NAIA and junior college team counts (226 and 300-545 in circulation) and the 14-player junior
college limit behind a login; travel cost for a Wisconsin family; any official size or jump
standard; any volleyball-specific reply-rate study; "letter of assurance"; a year-by-year
growth chart.

## Shipped

`artifacts/The-Commit-Book-Volleyball-Playbook-SAMPLE.pdf` (31 pages), beside the football,
girls basketball and men's basketball samples. Nothing deployed: production is still
`a8b25e9`, and the branch is `copy/anon-and-plain-english`.
