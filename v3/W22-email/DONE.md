# W22 - the outreach email, rebuilt from research

Mike's read of the football and girls' decks: "THE EMAIL to coaches are off. There are
GPA that are not possible and size and weights that are off as well." The 14.2 GPA, the
5.2 GPA, and the 6 foot 1, 148 pound middle linebacker were all real problems. He asked
for deep research on what a coach actually wants to see, for football and for both
basketball books, and for a template that answers 95% of a coach's questions.

## The research lane

Six agents, six files, all in `research/`, every claim tagged COACH, SERVICE, OFFICIAL,
DATA, FOLKLORE or UNCONFIRMED, every URL dated 11 November 2026.

| File | Lane | Size |
|---|---|---|
| `01-football-offense.md` | QB, RB, WR, TE, OL, ATH: stats, size, speed | 30 KB |
| `02-football-defense.md` | DL, LB, DB, K/P, and the tackle-total problem | 33 KB |
| `03-mens-basketball.md` | roster heights, weight, film spec, stat floors | 19 KB |
| `04-womens-basketball.md` | size floors, circuits, the academic screen | 23 KB |
| `05-grades-and-eligibility.md` | GPA scales, core courses, 2.3 and 2.2, no test | 33 KB |
| `06-email-form-and-etiquette.md` | subject line, length, links, follow-up | 18 KB |

The findings that changed the copy:

1. **No association publishes a size or speed standard.** Not the NCAA, not the NAIA,
   not the NJCAA. Every chart a family buys is a recruiting service's target. The decks
   now print the ladder and say what it is.
2. **A hand-timed 40 is 0.18 to 0.31 seconds fast**, from two peer-reviewed studies of
   the delay between a hand raise and a stopwatch. Trust order: the college's own camp,
   then an electronic combine, then a documented laser session. A missing number is read
   by a coach as a bad number, so skipping the shuttle hurts.
3. **Tackle totals are the stat a staff trusts least.** NCSA's linebacker, defensive line
   and defensive back guides carry no tackle number at any level. Print solo and assisted
   separately, tackles for loss, games played, and the schedule.
4. **No coach on record states a stat floor** for any position at any level. The floors in
   the decks are service floors and labelled as such.
5. **Roster heights are real data**: 12,714 player-seasons on 1,060 NCAA rosters, 2026-27,
   give D1/D2/D3 guard medians of 6'4"/6'3"/6'2", and school-listed heights run about an
   inch generous. Men's data, because no women's dataset that size is open.
6. **"14.2 GPA" cannot exist.** Scales top out at 4.0, 5.0, 6.0 or about 100. "5.2" is only
   readable with its scale named. The NCAA core-course GPA is its own number, on a 4.0
   scale: **Division 1 wants 2.3, Division 2 wants 2.2.**
7. **No SAT or ACT is needed to be eligible** at Division I or Division II. That requirement
   was removed on 1 August 2023 and it covers the class of 2029. A college may still want a
   score for admission or for its own money, and NAIA will take a 2.3 final GPA with no test.
8. **"My counselor can send a transcript today" is not true.** The counselor uploads official
   transcripts to the NCAA after the fourth and sixth semesters and after graduation. Print
   "unofficial transcript on request" and an Eligibility Center ID if he has one.
9. **Form**: subject line is a label, near 70 letters. Body 150 to 180 words, one phone
   screen. Two links, labelled, never an attachment, and the link must open with no login.
   One checkable reason for that school. The player's own address, parent line labelled.
   One FBS recruiting coordinator reported 75 emails a night in January and screening on
   size and speed before he reads a word.
10. **Film**: 2 minutes for basketball (6-coach women's panel), 3 to 5 for football, player
    circled inside the first three plays, defense shown, no free throws or warm-ups, then one
    full game and, for basketball, one game he lost.

## What shipped in the decks

* Both sample emails rewritten around one believable 2029 kid: 6 foot 0, 185 pounds,
  measured by the athletic trainer on a named date, hand-timed 4.94 with the method named,
  58 tackles split 34 solo, 3.62 unweighted GPA on a 4.0 scale. The girls' guard is 5 foot 7
  barefoot with a measured wingspan, 12.4 points and 6.1 assists over 26 games, and every
  shooting number carries its attempts. The old numbers were 6'1" 148 lb (42 to 72 pounds
  under every linebacker tier on the service ladder) and 22 points a game (Wisconsin's top
  sophomore guards in 2025-26 scored 13.5 to 18.0).
* New chapter 6 material in both decks: a "label every number" box, the service size ladder
  for football and the size and points floors for basketball, and a "leave these out" box.
* Chapter 2 glossary now separates unweighted GPA, weighted GPA, core-course GPA and verified
  time, in all three decks.
* The 11th-grade checklist row carries the 2.3 and 2.2 numbers and the four-courses-a-year rule.
* Chapter 11 gained 8 or 9 new source entries in each deck and two new honest gaps: no
  official size standard, and no coach-published stat floor.
* The men's deck's sample subject line named a real Wisconsin school; it now uses the same
  fictional town as the other two, and the GPA says unweighted.
* Football 18 -> 21 pages, girls 16 -> 19, men's unchanged at 12. Reading level moved from
  5.0 to 5.1 and from 4.8 to 4.9. No block splits across a page; only the three long grids
  continue, header repeated.

## Rebuild

`python email22fb.py` then `email22b.py` then `email22c.py` then `growth22b.py`, then
`python fb-plain.py` / `wbb-plain.py` (and `python bball-plain.py` in `../W19-plain`).
Print with the data-URL recipe; `splitcheck2.py`, `headfoot2.py`, `peek.py`, `score.py`,
`qa2.py` and `sheet22.py` are the QA set.

## Still open

* Per-position sophomore norms, and wingspan, hand-size, sprint and vertical norms by level:
  no open dataset. Settling it needs a published college or showcase combine table with
  sample sizes.
* Kicker numbers disagree at the bottom of the ladder (D3 kickoff 40-45 yards from one
  service, 60+ from another), so the deck prints the range and says the two disagree.
* Send-window data is a vendor's own tracking (correlation only). Timing is a tiebreaker.
* The follow-up advice in the decks came from the W20 lane (call in one to three business
  days). The email-form research says do not re-email inside two weeks. Both are in print,
  and they are about different actions; worth one careful pass before the next reprint.
