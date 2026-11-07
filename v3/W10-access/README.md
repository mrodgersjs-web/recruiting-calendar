# W10-access: Coach Contact Kit (worksheets, scripts, tests)
Built 2026-11-06 from `../W7-access/ACCESS.md` (sections 2a, 2c, 2d, 4, 7, 8, 9). Original work; no text copied from vendor templates. **No contact with anyone, no guarantees, no site edits.** Python stdlib only; offline.

## What is here
| File | Purpose |
|---|---|
| `deliverables/1-send-date-worksheet.md` | Where the family stands on "when may this coach answer," by division, with checked-on date |
| `deliverables/2-questionnaire-checklist.md` | What to have ready; per-program form tracker (links out only) |
| `deliverables/3-contact-scripts.md` | 5 athlete-voice drafts + 4-touch cadence + 30-school cap |
| `deliverables/4-highlight-link-checklist.md` | Public/unlisted, length, title, first 30 seconds |
| `deliverables/5-ask-your-coach-one-pager.md` | Hand-to-coach request, target list, three sentences |
| `deliverables/6-follow-log.csv` + `-README.md` | 16-column manual tracker |
| `contact_kit.py` | Library: window logic, templates, link checklist, log validation, KPI math, promise filter |
| `kit_cli.py` | CLI wrapper (draft-only output) |
| `build_worksheets.py` | Regenerates `deliverables/` deterministically |
| `tests/test_kit.py` | 49 tests |
| `KPI.md` | 10 KPIs, definitions, hard gates (K9 copy safety, K10 date freshness) |
| `INTEGRATION.md` | Contract for the site lane |

## Use
```
python3 build_worksheets.py
python3 kit_cli.py window --division D1 --open 2027-06-15
python3 kit_cli.py script dm_short --set coach_last=Reyes --set athlete_name="..." ...
python3 kit_cli.py link https://youtu.be/xyz --minutes 4 --title "Name 2029 Sport Position" --tested yes
python3 kit_cli.py log-new > mylog.csv ; python3 kit_cli.py log-check mylog.csv
python3 -m unittest discover -s tests
```

## Honest limits
- Cadence spacing (0/10/24/45 days) and the 30-school cap are HYPOTHESES from ACCESS.md, not rules.
- D1 reply dates are entered by the family from the NCAA sport calendar. The library never supplies one, because ACCESS.md 2a documents conflicting sources.
- The link checker is a checklist, not a fetch: it cannot tell if a video is really public. The family must open it in a private window.
- No KPI has been measured; no demand or willingness-to-pay is claimed.
