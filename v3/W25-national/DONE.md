# W25 - every playbook goes national

Requested 11 Nov 2026 by Mike, verbatim: "The Volleyball playbook as a lot of Wisconis specific
items. None of these playbooks should be specific to a state. Look over them all, remove that and
rework the playbooks for they all fit across all states."

## What the inventory found

`inventory.py` and `where.py` scanned all four decks and their source fragments. The football,
girls basketball and men's basketball decks were already national: their only state marker was
", WI" inside the sample subject line, and the state names that remain there are coach-quote
attributions (Nebraska's player-personnel director, Stanford's David Shaw, Eastern Michigan's
Chris Creighton), which are evidence, not instructions to the reader. The volleyball deck was the
local one: 26 mentions of the state, 23 of a state university system, 16 of one named school, plus
one named club region, its qualifier venue, its championships, its member counts, and a camp price
list of seven named colleges.

## The national style now applied to all four books

1. A rule that belongs to a state association is printed as "your state association", with the
   things to look up named. Where a concrete calendar helps, it is printed as one state's example
   and labelled as an example.
2. A price, a date or a member count that came from one region keeps its number and loses its
   name: "one region reported 18,137 members and 148 clubs", "a private university's prep camp
   $310 commuting and $380 resident", "a public university's prospect camp $160 for 40 players".
3. The roster table in chapter 2 lost its school names and gained a level-by-level count, so the
   reader sees the method: 11 pages, four levels, 212 players, sizes 15 to 31. The names stay in
   chapter 11 as provenance, labelled one region's sample and not a shortlist.
4. Sample emails never named a real school and still do not; the state is gone from the subject
   lines, and the subject-line formula now says "school, and where you play. A coach only needs to
   know your time zone, because that decides travel."
5. Coach quotes keep their programs. A family in Florida reads "Nebraska's head coach" as an
   expert, not as a requirement to be in Nebraska.

## Gate fix, and a correction to what I reported earlier

`splitcheck2.py`, the whole-block print gate, compared source text to extracted PDF text without
decomposing typographic ligatures. The PDF hands back "diﬀerent" with U+FB00 and "ﬁrst" with
U+FB01, so any block containing those words was reported as missing, and I had been reading those
false positives as unimportant lines in the output. It now applies NFKC normalization first. After
the fix, all four decks are clean for the reason that matters: **zero blocks cross a page break**,
and the only things that continue across pages are the flow grids, with their header rows repeated
(men's 1, football 3, girls 2, volleyball 3). The rule itself was never broken; my earlier reports
on that point stand.

## Reprint QA, all four books

| book | pages | grade | header/footer/number | blocks split | side margins |
|-|-|-|-|-|-|
| men's basketball | 12 | 4.4 | 0 failures | 0 | 14.0-201.9 mm every page |
| football | 21 | 5.1 | 0 failures | 0 | same |
| girls basketball | 20 | 4.9 | 0 failures | 0 | same |
| women's volleyball | 32 (was 31) | 5.7 | 0 failures | 0 | same |

Volleyball gained a page because the national rework explains the look-up step instead of naming
the place. Reading levels are unchanged in the other three. The fact audit (`verify24.py`) still
shows only CSS values, the invented sample-email numbers, and the five sums this book computed and
labels as estimates.

## Site copy checked too

`site/` carries no state name. The only locality-flavored strings are "In-State" as a list tier on
the Access page and "your state attorney general" in the disclaimer, both of which are relative to
the reader and correct for a national product. No site change needed for this rule.

## Files in this lane

`inventory.py` (state tokens per deck, with context), `where.py` (which source file and line),
`qa25.py` (header, footer, page-number, chapter and thin-page checks for all four decks in one
pass), `grade.py` (one reading gate for the whole line), `sheet25.py` (contact sheet and the
three-panel proof), `splitcheck2.py` fix in `../W20-two-sports/`.
