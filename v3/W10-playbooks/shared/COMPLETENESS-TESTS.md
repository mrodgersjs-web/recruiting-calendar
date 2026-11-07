# W10 Completeness Tests (cross-sport)
Written 2026-11-06. A playbook ships only if every line below is YES. Lines marked [AUTO] are checked by `tests/validate.py`; lines marked [HUMAN] need a reader.

## T1. Structure [AUTO]
- [ ] Header names the class (2029), the date the rules were read, the playbook id.
- [ ] Part A (picture), Part B (stages), Part C (worksheets), Part E (scripts), Part D (completeness), Sources used all exist.
- [ ] Every stage has a "Done when" line.
- [ ] At least 10 worksheets (C1..), at least 4 scripts (E1..E4: first email, follow-up, after camp, ask HS coach).

## T2. Citations [AUTO]
- [ ] Every factual date, number or rule sentence carries a source tag like `[S1 13.9.3.3]` or `[S7]`.
- [ ] Every S-id used appears in `SOURCES.md`.
- [ ] Every S-id in "Sources used" is actually cited in the body, and every cited id is listed.
- [ ] PROJECTED dates say PROJECTED. RECOMMENDED dates say RECOMMENDED. Neither is written as a rule.

## T3. Dates match the site rule rows [AUTO]
- [ ] Each key rule date in the manifest (`manifests/*.json` -> dates) appears in the playbook text, and the same date appears in `site/data.js` for that sport.
- [ ] Track states the 2027-06-15 off-campus change adopted 2026-10-07.

## T4. Integrity [AUTO]
- [ ] No outcome promises ("guarantee", "will get you", "you will earn a scholarship").
- [ ] No banned filler ("unlock", "empower", "synergy", "leverage", "disrupt", "hustle", "utilize", "iterate", "optimize").
- [ ] No named minor, no Jacob, no athlete claimed to have used the playbook.
- [ ] No price shown as final; no sales language, no checkout links, no "buy now".
- [ ] No text copied from paid products; no quote longer than a short phrase from any source.

## T5. Usability [HUMAN]
- [ ] A parent who has never recruited can start Stage 0 tonight with only this file.
- [ ] Each worksheet can be pasted into a sheet and filled without outside help.
- [ ] Each script fits in under 120 words and is written in the athlete's voice.
- [ ] A reader can tell which dates are law, which are projected, which are advice.

## T6. Integration [AUTO]
- [ ] Manifest JSON validates against `shared/INTEGRATION-CONTRACT.md`.
- [ ] Manifest stage and worksheet counts equal the counts in the markdown.
- [ ] Manifest `offer_links` use only slugs from W8 `OFFERINGS.json`; any not BUILT is flagged `notify`.
