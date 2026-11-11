# W20 - two more sports, grade 8 first draft

Built 11 Nov 2026. Two customer decks plus a men-versus-women memo, in the same
shape as the W19 men's basketball book, but written at grade 8 from the first
draft instead of rewritten down to it.

## What shipped this lane

| File | What it is | Pages | Reading level |
|---|---|---|---|
| `wbb-playbook-plain.html` -> `The-Commit-Book-Girls-Basketball-Playbook-SAMPLE.pdf` | Girls' basketball playbook, 11 chapters | 13 | grade 4.8, ease 80.7, 11.2 words per sentence |
| `fb-playbook-plain.html` -> `The-Commit-Book-Football-Playbook-SAMPLE.pdf` | Boys' football playbook, 11 chapters | 13 | grade 5.0, ease 80.5, 11.8 words per sentence |
| `research/01..08-*.md` | The eight research reports behind both decks, with bylaw numbers and URLs | - | - |
| `artifacts/commit-book-men-vs-women-basketball.md` (session folder) | Internal memo: what differs between the men's and the women's game, and what that means for the product | - | - |

Also in this lane, from the same research: the men's sample was reprinted with
the open flag in its chapter 8 closed (`v3/W19-plain`, 12 pages, grade 4.4), and
the site calendar gained the two missing basketball lanes (`site/data.js`,
`site/app.js`, `site/calendar/index.html`). Nothing deployed.

## How to rebuild

```
python wbb-plain.py     # writes wbb-playbook-plain.html, then scores it
python fb-plain.py
python score.py <html> "<label>"     # Flesch-Kincaid on the customer text only
python apply20.py <generator> <fixes.txt>   # FIND|||REPLACE list, refuses to move a number
python headfoot2.py     # header, footer and page number on every page
python qa2.py <png dir> "<label>"     # ink, margins and white-gap audit
python peek.py          # per-page character counts, to catch spill pages
```

Printing is a REPL step: navigate the HTML as a data URL, then `page.pdf()` with
`preferCSSPageSize`, `displayHeaderFooter`, and the header and footer templates
padded `0 14mm`. `head.txt` is the W19 head, extracted once, so both decks carry
the same house style.

## Two calls worth remembering

1. **Chapters flow now.** `head.txt` used to force `section + section
   { page-break-before: always }`, which left four pages per deck holding 235 to
   1,600 characters, a chapter tail alone on a page. Forced breaks are kept only
   before chapter 1 and the sources chapter, with `class="newpage"`. Both decks
   went from 15 and 17 pages to 13, filled evenly.
2. **`apply20.py` refuses a fix that moves a digit or a bylaw number.** The
   proofreader owns words, not facts. Everything it wanted to change that touched
   a date went through `patch20*.py` by hand, where the reason is in the comment.

## Corrections found while building

* Both decks first said the 2028-29 calendar "arrives in July 2027". The
  2026-27 calendars arrived in July 2026, so the right year is 2028. Fixed in
  `patch20.py` and `patch20b.py`.
* The women's paid-visit line said "one visit per player". Bylaw 13.6.2.2 allows
  one visit before 15 October after high school and one beginning that date.
  Fixed in both places, and the rule is now quoted once, in the visit chapter.
* The first look at the site data flagged a "wrong women's row" in `site/data.js`.
  That row was **track**, and it is right (13.1.1.1.9, changed 7 Oct 2026). The
  real gap was that the site had no basketball lane at all. Added both.
* A proofreader questioned "130 international players, 15% of the field". The
  NCAA's own article says exactly that, so the figure stands.
* 13.9.3.1 blocks a written aid offer in every sport except football until
  1 August of senior year; 13.9.3.3 puts football at 15 November. Read from the
  manual itself, and both decks cite the right one. Verbatim quotes are shelved
  at the end of `research/01-wbb-rules.md`.

## Unresolved, and how each one is handled in the product

* The 2028-29 calendars are not published; every week computed from a formula is
  tagged PROJECTED in the date tables.
* The printed FBS calendar puts the November dead period at 29 November, the
  NCAA recruiting page at 30 November. The deck prints the PDF and says so.
* The FCS claim that a school may sign only 26 players a year is repeated by
  services and is not in the current football bylaws. Not printed as fact.
* The "July report day" rule that several services describe has no matching text
  in the 2026-27 book. Not printed.
* The NJCAA chart that carries the February football date prints its own note
  that the document is not final. The deck says to confirm with the college.
* No NAIA or NJCAA program counts are published by those associations, so the
  decks print rough figures and label them rough.

## Next, in order

1. Girls' volleyball at the same depth (the cheapest next lane: the Big Ten and
   the AVCA publish their numbers).
2. Price the basketball books and put page counts on the store card.
3. Decide whether the three playbooks go on the site now or after one more lane.
4. Print rule now lives in `head.txt`. Any new sport deck inherits it, so a new
   lane needs no layout work, only the `flow` marks on grids that run long.

## W21: nothing cut in half by a page break (Mike, 11 Nov 2026)

Mike read the football PDF and called out three things: the "how long should his
list be?" box split over two pages, chapter 3 starting mid-page, and a split box
in the film chapter. Requested standard: no box, message, point list or callout
may cross a page.

What changed, all in `head.txt` plus four class attributes:

* `break-inside: avoid` on `.box, .tmpl, table, ul, ol, dl, blockquote, .two,
  .lead, h2, h3, .pagehead`, plus `tr, li { break-inside: avoid }` and
  `orphans/widows: 2`. A block that does not fit moves whole to the next page.
* `class="flow"` opts a block out, and only four blocks carry it: the chapter 3
  date grid, the chapter 8 price grid, the chapter 6 camp-cost table and the
  sources list. Those split between rows or items, and the header row repeats on
  the next page.
* `section + section { break-before: page }`: every chapter starts on a fresh
  page, the way the men's book reads. Chapter 3 was the specific ask; the rule
  generalises it. This also exposed a real markup bug: chapter 10 was nested
  inside chapter 9's `<section>` in both generators, so it never got its own
  page. Fixed in `sectfix.py`.
* Four boxes that had been last in their chapter were re-seated so they do not
  strand alone on a page (`flowmore.py` moved the whole-year cost box above the
  price grid). An earlier attempt to move four boxes up at once made things
  worse and was reverted with `git checkout` on the two generators.

Page counts went 13 -> 16 (girls) and 13 -> 18 (football). Reading level is
unchanged at 4.8 and 5.0, because no sentence was touched.

QA scripts written for this pass, worth keeping for the next lane:

* `splitcheck2.py <html> <dump>` - the real gate. Cuts every block into runs at
  the tag boundaries and passes only if one page holds all of them. It survives
  list renumbering, `text-transform: uppercase` letter-spacing and the soft
  hyphen Chromium leaves at a wrap point, all of which break naive substring
  matching. Result: 36 of 38 and 37 of 39 blocks whole, the rest are the marked
  flow grids.
* `headfoot2.py` - header, footer and page number on every page: still clean.
* `peek.py`, `sizes.py`, `qa2.py` - page fill, block size, ink and margin audit.

Known and accepted: four chapter-end pages are light (football p9 and p13, girls
p13 are the thinnest). That is what happens when a chapter runs about 15% over
one page and its last block may not split. If Mike wants those pages full, the
cost is one short paragraph per chapter, and the split rule has to bend for a
box or two.
