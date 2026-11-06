# W11-5 Emerging & Fastest-Growing Sports Hub: DONE

Built 2026-11-06. Files (write scope respected):
- site/emerging-sports/index.html, emerging.js, emerging.css, data.json
- v3/W11-emerging-sports/test_emerging.py, DONE.md

## What shipped
- /emerging-sports: NFHS 2024-25 stat row, tabbed sport panels (flag football, girls wrestling, boys volleyball) with NCAA / NAIA / NJCAA status + source link per body, a 10-question Emerging Sport Pathway & Question Checklist (progress bar, localStorage ticks, reset), a NCAA/NAIA/NJCAA/club label table, an aid-by-level table, and links to /story/rodriguez, /story/composite-volleyball, /story/composite-wrestling, /story/perez, /access, /recruitiq.
- Key numbers are in static HTML (work without JS); tabs, checklist and aid table are JS-driven from data.json.

## Brief figures that did NOT verify (corrected on the page, disclosed in a visible notice)
| Brief said | Primary source says | Used |
|---|---|---|
| Overall 8,215,882 | NFHS 2024-25 survey totals table: 8,266,244 (4,726,648 boys + 3,539,596 girls). 8,215,882 appears in no NFHS doc or in this repo. | 8,266,244 |
| Flag football 1,781 schools | NFHS table: 2,736 schools (release: nearly 1,000 added in a year) | 2,736 |
| Boys volleyball 2,900+ schools | NFHS table: 4,303 schools (32 reporting states) | 4,303 |
| Boys volleyball +24.2% as NFHS growth | 2-yr growth from NCAA's reprint of NFHS tables (in MARKET.md); AVCA gives +12.57% YoY | labelled two-year |
| NCAA "voted to establish... first championship 2026" | Added Jan 2025 as 91st championship; first held March 2026, Coralville IA. D3 separate championship from 2027-28 | stated as such |
| NAIA wrestling "established" | NAIA invitational 2018, championship sport 2022 | stated as such |
Confirmed as briefed: 68,847 (+60%), 74,064 (+15%), 95,972, flag football added to NCAA Emerging Sports for Women Jan 2026, NAIA Bylaws Art. V Sec. C (per W4-composites rule record). Also found: NAIA flag football championship from 2026-27, NJCAA flag football championship from 2027-28, NJCAA men's volleyball first national championship 2026.

Gaps: NJCAA women's wrestling status not confirmed (page says so). The Article V Section C cite comes from the repo's composite-wbasketball rule record (NAIA 2026-27 Handbook p.70), not re-read in the handbook PDF. /access and /recruitiq routes do not exist yet in site/ (linked as requested; W10 owns them).

## Verification
`python3 v3/W11-emerging-sports/test_emerging.py` -> Ran 26 tests, OK (numbers vs page/data.json/MARKET.md, citations and primary domains, pathway claims, story/tool links and file existence, checklist structure, a11y basics).
Browser check on local server: 3 tabs render, tab switch shows only the volleyball panel, 10 checkboxes, progress reads "2 of 10 answered", 5 aid rows, state saved to localStorage.
