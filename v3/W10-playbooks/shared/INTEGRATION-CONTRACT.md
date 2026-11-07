# W10 Integration Contract
Written 2026-11-06. Defines how the three W10 playbooks plug into the Commit Book site, offers, and experiences without edits to the site in this wave. A later wave (the integrator) reads only this contract and `manifests/*.json`.

## 1. Files and ownership
| File | Role |
|---|---|
| `{sport}/PLAYBOOK.md` | Human text. Source of truth for wording. |
| `manifests/{sport}.json` | Machine summary. Source of truth for ids, slugs, dates, counts, links. |
| `shared/SOURCES.md` | Ledger S1..S41. Citation targets. |
| `shared/COMPLETENESS-TESTS.md` | Ship test. |
| `tests/validate.py` | Runs the AUTO checks. Exit 0 = pass. |

## 2. Manifest schema (version 1)
```
{
 "schema": "w10-playbook-manifest/1",
 "id": "w10-football",
 "sport": "football",
 "class_year": 2029,
 "rules_read": "2026-11-05",
 "written": "2026-11-06",
 "file": "football/PLAYBOOK.md",
 "site_mapping": {
   "catalog_title": "Football: Junior Year Playbook",
   "site_slug": "football-junior-year",
   "relation": "supersedes_on_integration | extends",
   "catalog_status_before": "WRITTEN | OUTLINE"
 },
 "price_proposal": {"amount_usd": 29, "status": "PROPOSED_NOT_APPROVED", "note": "..."},
 "stages": [{"n": 0, "title": "...", "has_done_when": true}],
 "worksheets": ["C1", "..."],
 "scripts": ["E1", "E2", "E3", "E4"],
 "dates": [{"date": "2027-06-15", "kind": "RULE|PROJECTED|RECOMMENDED", "label": "...", "sources": ["S1"], "site_data_key": "..."}],
 "sources": ["S1", "..."],
 "story_beats": ["first coach contact", "..."],
 "offer_links": [{"slug": "contact-log", "w8_status": "BUILT", "action": "link|notify", "placement": "Worksheet C3"}],
 "integrity": {"no_outcome_promise": true, "no_minor_names": true, "no_athlete_claimed_user": true, "no_outreach": true}
}
```
Field rules:
- `dates[].kind`: RULE needs a bylaw source; PROJECTED needs the bylaw it is calculated from; RECOMMENDED is advice and has no bylaw.
- `dates[].date` must be ISO. RULE and PROJECTED dates must also appear in the playbook text.
- `offer_links[].action`: `link` only when W8 status is BUILT. PROPOSED or OUTLINE offers use `notify` (a "tell me when it exists" form, no purchase flow). Matches W3 legal and W9 rules.
- `price_proposal.status` must stay `PROPOSED_NOT_APPROVED` until Mike approves a price. The integrator must not render a price as final or open a payment path on this basis.

## 3. Integration steps (for the later wave)
1. Read `manifests/{sport}.json`; run `python3 tests/validate.py`. Stop if it fails.
2. Render `PLAYBOOK.md` in the existing playbook page template as the long form. Keep Part A and Part D visible. Worksheets render as printable blocks; scripts render as copyable text.
3. Link from each stage/worksheet to the W8 offer in `offer_links` (link) or the notify form (notify).
4. Attach `story_beats` to the existing W1 story-beat map; do not invent new beats.
5. Date rows: the site's rule rows in `site/data.js` stay authoritative for RULE dates. If a manifest RULE date and a site date differ, the site date wins and the validator shows the diff; fix the playbook, not the site.
6. Public wording for the page: "Education, not legal advice." Keep the disclaimer block from the top of each playbook.

## 4. Do and do not
Do: cite bylaws by id; keep PROJECTED labeled; keep the athlete as the sender; say the PDF/tracker are our own.
Do not: copy any paid MM3 or competitor text; quote a source beyond a short phrase; name a minor or Jacob; say an athlete used the playbook; promise an offer, aid or roster spot; show a checkout; contact coaches or athletes; edit `site/`.

## 5. Change control
- Rules change each NCAA manual year. When S1, S2 or S3 changes, re-read the bylaws, update Part A and manifest dates, re-run the validator, bump `rules_read`.
- Items marked VERIFY in SOURCES.md must be re-checked before launch.
- Version bump is the `written` date; keep prior files under `archive/` if replaced.

## 6. Known open items (for Mike or the integrator)
- Price is a proposal only (Football $29, Baseball $29, Track $25 per W1 catalog).
- Sideline membership ($149/yr) is unapproved and not referenced by the playbooks.
- Offers not yet BUILT (coach-emails, bundle) are `notify` links.
- Questionnaire timing rules vary by date; S38 is marked VERIFY.
