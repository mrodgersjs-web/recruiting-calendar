# W28: four more sports, and the template they were built from

Branch `copy/anon-and-plain-english`. Nothing is deployed: production is still `a8b25e9`,
and `vercel deploy --prod` is Mike's call. Three commits in this lane: `a6b37b0` (four
books, template, packets), `1edfeeb` (storefront audit round one), and the one that
follows this file (audit round two, the four final PDFs, the locked run order).

## The four books

| Book | Pages | Deck bytes | Deck hash | Grade | Fact-check | Print-check |
|---|---|---|---|---|---|---|
| Men's Baseball: The Whole Road to College | 25 | 90,098 | `9219c4e9` | 4.4 | 0 failures, 0 approximations | 0 failures, 4 warnings, 332 cells |
| Women's Softball: The Whole Road to College | 33 | 104,542 | `713775fb` | 4.7 | 0 failures, 1 approximation | 0 failures, 4 warnings, 392 cells |
| Men's Soccer: The Whole Road to College | 27 | 92,680 | `2e5cb0b4` | 4.7 | 0 failures, 1 approximation | 0 failures, 5 warnings, 218 cells |
| Women's Soccer: The Whole Road to College | 27 | 89,355 | `340351df` | 4.5 | 0 failures, 1 approximation | 0 failures, 6 warnings, 274 cells |

Grades are Flesch-Kincaid over the printed prose. All four are simpler than the volleyball
book that sold (7.3). PDFs are in `funnel/deliver/pdfs/` beside the five already sold, so
the delivery folder now holds nine.

Athletes and coaches: Diego Whitlock / Coach Tolliver (baseball), Casey Lindqvist / Coach
Mardian (softball), Alex Nkemdi / Coach Halloway (men's soccer), Tori Marchetti / Coach
Aldridge (women's soccer). Five coach surnames across five books, no two the same, none of
them a real athlete, recruit, coach or recruiting profile in that sport.

## What the audits forced

Nine agents read this work: four writers, a copy auditor, a fact auditor, a print auditor,
a store auditor and an art auditor. The list of things they caught, because it is the
useful part.

**The books.** Eleven `UNCONFIRMED` chips in the baseball draft, printed as chips where the
sold book prints plain words in the date cell: reversed, and the rule is in the template.
A chapter 8 that promised its sources sit in chapter 11 "each with the page it came from"
when chapter 11 prints no address: the promise now points at the label, and says outright
that the book names no seller. "Signee", "ID camp", "sport sponsorship", "extra rounds",
"bracket", "the academic test", "designated student-athletes", "institutional request list",
"electronic correspondence", "12U/14U/18U": ten pieces of administrator vocabulary that were
explained, or moved behind a plain sentence first. Two sentences with four dates in them
became a list of three lines. One book's email closed with the same sentence as another's,
so one changed.

**A page count that lied.** The softball book printed at 24 pages on the first pass and 33
on the second. Nothing had grown: two unbreakable URLs made Chromium shrink the whole sheet
to 80 per cent, which hid nine pages. The fix is `overflow-wrap` on the sources chapter, and
the lesson is that a page count is only evidence once the geometry audit passes at full scale.

**Names.** Fourteen candidate surnames went through three rounds of searching, and the bar
moved once the data came back: no ordinary American surname returns zero people. What the
rule became, and what is written in the template: nothing in the same sport, no recruiting
profile, no named plaintiff. Dalton, Marlow, Hartwell, Wheelock, Bergstrom, Lindgren,
Ferraro (twenty years of articles against a women's coach of that name), Rutherford (a youth
coach with a profile), Delaney, Ostrander, Whitfield, Doll, Bramley (a real college head
coach), Brannigan (a school bulletin prints it beside a softball notice), Ellison (a real
recruit), Varnell (the named plaintiff in a published Tenth Circuit case about a school
coach: the worst collision of the whole pass), Sappington (a current Division I head coach),
Ridenour (two), Netherton (a head softball coach and a Colorado recruit), Thurber (an
athletic-department employee), Hallowell (a business under that name), Wendling (a former
head coach), Pennebaker, Lineberry, Haldeman, Kenworthy, Fennimore, Dunmore, Kessler (three
softball coaches, one of them a travel team that carries the name). Kessler was my pick and
the softball writer's own search killed it an hour after I sent it, which is the reason the
writer searches and I do not.

**The storefront.** The phone carousel called a helper that only exists in the desktop file,
so below 750px the entire ring rendered empty and the console stayed clean. My own price fix
turned `$0` into `$undefined` because I removed the key and left the template reading it out
loud. The desktop rail sold books that are not written: it listed them, priced them, and a
Get button took the click and filled the bag. The four sports with no book of their own still
showed `$15` and `$19` on their own pages, because those pages are shipped files this script
never opened; `sweep_pages()` now walks every tile on every sport page and reads the money
rule from the catalogue. The swimming card wore full colour, a live button and a NOT WRITTEN
YET band at the same time, because a card with no book of its own was guessing from the first
title in its list. Four different phrases described one state; there is now one, "in progress".
The `/sports/` index counted planned titles as playbooks. The soccer page promised dead
periods in every division when Division II prints one and Division III prints none, and the
index card beside it repeated the claim after the page was fixed, which is how a fact goes
stale: a second copy of it lives somewhere nobody re-checks. The build now fails on four
banned phrases. New tiles wore the uniform upside down (the whole title in the 9-pixel label,
the audience where the title goes). Two product-page buttons both said Get.

## Four things I decided rather than fixed

1. **The women's soccer figure is a traced silhouette, labelled as one.** The image model on
   this account returns 403 (`Settings > Models`: a provider has to be enabled, and only Mike
   or James can do it), so no new athlete could be generated. I traced the alpha of an unused
   cutout in `v3/W5-athletes/v1media/cut-pirosko-1080.webp` into house ink at the house aspect
   (`trace_figure.py`, 1080x1920, the same 1.777 ratio as its eleven neighbours). The art
   auditor says it reads as a woman athlete and not as a missing image. The copy auditor says
   three things lean basketball: the ball palmed at the hip, knee-length shorts, high-top
   shoes. Both are right about the same pixels. The card's tag now says SILHOUETTE, the alt
   text says silhouette, the caption says it is traced from a photograph, and no card for a
   $29 book says anything is coming. When the model is enabled: generate the figure, save it
   as `cut-womens-soccer-640.webp` and `-1080`, point the config's `art` at it, delete the
   two `sil-` files.
2. **Alex, the men's soccer cutout, has real flaws** (a white ball, guards over the socks, no
   headroom). It shipped in W25 and I left it. Redrawing it is an hour and an image model.
3. **Pending tiles point at the sport page, not at a waitlist.** There is no list to join, so
   "notify me" would be a promise with nothing behind it. If Mike wants one, the affordance is
   half an hour on the price page.
4. **The three pack prices stay on the shelf without buttons** because checkout accepts the
   nine playbook slugs and nothing else. The line under them says the prices are proposed for
   launch, which is true, and a button that did nothing would be worse.

## Tight pages, for whoever edits next

Baseball chapter 6 has 4 to 5 mm left before its box: one more row splits the page. Men's
soccer chapter 4 ends with about two lines of room on its last page; the writer measured it
in the browser before printing, and the print agrees. Women's soccer pages 19 and 23 are thin
by design: they close a chapter. Nothing else has room for a sentence.

## Running it again, or for the first time

```
git clone https://github.com/rodgemd2/recruiting-calendar
git checkout copy/anon-and-plain-english
cd recruiting-calendar/v3/W28-four-sports
python -m pip install -r requirements.txt        # pypdf and Pillow only
python deck.py mens-baseball-road-to-college     # once per book: autocrlf rewrote the
                                                 # fragment hashes on checkout
python factcheck.py --all
python print.js in the browser REPL, then copy the four PDFs into pdfs/
python printcheck.py mens-baseball-road-to-college
python site.py --apply                           # twice: the cache keys settle on run two
python site.py --apply
python gate.py                                   # 62 checks
```

`TEMPLATE.md` is the contract: thirteen sections, from what a chapter is for to the order the
scripts run in. `print.js` is the house print recipe and `trace_figure.py` the figure recipe.
Nothing in `site/` is edited by hand; `site.py`, `STORE.json`, `SPORTS/*.json`, `head.txt` and
the twelve fragments per book own everything you can see.

## Scratch left out of the commit

Sixteen scripts in `v3/W15-pdf/` and `v3/W25-national/artifacts-check.py` are untracked and
predate this lane. `fixjs3.py`, `fixjs4.py`, `fixsite2.py` and `fixsite3.py` in this lane are
this week's patches: they are kept because each one prints what it changed and refuses to
apply twice, and they can go in a housekeeping commit once the store stops moving.

## Third storefront pass, after the auditor read the rebuild

The auditor came back "fix first" on my own round-two work, and was right on eight counts. A
paragraph pattern written with `re.S` and a permissive tail walked past its own `</p>` and ate
`</main>`, the footer and the closing tags on two sport pages; the fix for a truncated page had
to come from two commits back, because the truncation went in with the commit that fixed the
claim. A CSS rule I added to lift a tag above a figure carried `position:relative`, which
overrode the absolute anchor two rules earlier and put the tag across every athlete's thighs.
A count line said "1 playbooks" and, at zero, "0 PLAYBOOKS" over an empty list, which is a
finding wearing a heading. A tick for a sport with no book was cut mid-word. Two of three
bundle rows priced something with no contents. The phone menu did nothing on ten pages because
`site.js` was never loaded there, which predates this lane.

And the same class of bug the auditor had already caught once, in a new place: the sentence that
retracts "no dated calendar for this sport yet" ran only on pages this script rebuilds, so the
shipped volleyball, basketball and girls' basketball pages still told a reader there were no
dated rules for their sport, under books that carry every date in them. The retraction now runs
on every sport page, and the pending three keep it because for them it is true.

One thing the auditor asked for that I did not build: a way to leave an email on the four sports
with no book. The cross-sport titles have Notify forms because they have product pages; the four
planned sport books have neither, so the honest affordance today is the sport page. That is a
decision for Mike, not a fix.

## Print round four: the checker learned to measure, and the books changed because of it

The print auditor failed all four books on two defects, and both were invisible to every check
I had. The running head and footer printed at 0.58 pt: the words were in the text layer, so a
text check called them present. The cause was my own template. A style attribute cannot contain
a quote character, and I had a font family name in quotes inside it, twice: first in double
quotes inside a double-quoted attribute, then, "fixed", in single quotes inside a single-quoted
one. Both truncated the declaration list where the family name started, which is also where the
flexbox lived, so the page number printed glued to the brand on the left instead of at the right
edge. Chapter 11 broke ordinary words mid-word ("Byl / aws", "Cont / act") because the sources
rule carried `word-break:break-all`, copied in from a 2024 lane and never questioned.

printcheck.py now measures both, off the page content stream: every page must have a run of at
least 4.5 pt in the head band and the footer band, and a footer run right of 60% of the paper.
The calendar grid is measured too, at 1.83in and 4.64in from the margin, where the shipped book
draws its rules. The scanner took three attempts to get right, and each wrong version failed in a
way the previous version's own output hid: q/Q markers left on the operand stack, the text matrix
folded with the page CTM, and a substring patch that hit `ctm =` while aiming at `tm =`, which
threw away the page's own 0.24 scale and reported every coordinate four times too large. A checker
comparing big numbers with big numbers called that a pass.

Then the fix for the fix: the head printed correctly and said "SOFTBALL PLAYBOOK", so the configs
now carry the sport's full name, the way the shelf names it. `pagehead_word` is "Men's Baseball"
and "Women's Softball", and 22 chapter pageheads with it.

41 notes that sat under a table were moved into that table's own `<tfoot>` row. A paragraph after
a table is a separate object to the print engine: it split the SERVICE note away from the prices
it qualifies, `break-before: avoid` on the paragraph did not stop it, and neither did wrapping the
pair in a div with `break-inside: avoid`. Inside the table it travels with the table or nowhere.
Two long tables were also allowed to split with their first four rows glued, so no chapter ends
with one row alone on a page, and the glossary heading no longer leads a page with a single entry
under it.

Softball is 33 pages and women's soccer 28, one page each than at the last audit, from the
word-break change and the footer notes. All four pass the grown checker, factcheck and the gate at
62 of 62. One page the auditor flagged stays as it is: men's soccer p23 holds the closing
one-page recap, which is short because it is a recap, and the shipped book has two pages the same
size. The store auditor's six cosmetics went in the same commit: the in-progress band is clipped
by the cover that carries it (it was a red strip loitering next to a tile, and off-screen at 390),
the phone deck prints no heading over an empty list, a panel with no heading keeps its top space,
the four pending tiles no longer promise the page they are standing on, the lacrosse title says
Women's on its own page, the track card on the index no longer claims dated rules, and the three
bundle prices say "at launch" beside the number.

## Store round two, on the auditor's re-check: a bounding box is not a test

The band fix had landed in the generator and not on the pages the build patches in place, and my
two proofs were both vacuous. Band at 93-534 against a cover at 120-507 is not a clipped band, it
is 27 px of overhang on each side of the tile it labels. And `scrollWidth` on the document element
always passes when `html, body` carry `overflow-x: clip`, because the clipping is the thing making
it pass; `body.scrollWidth` was 379 against a 375 viewport. The test that catches this shape is
structural rather than geometric: the band's parent element has to be the cover. It is, on all four
sport pages and on the shelf, and `site.py` now raises instead of shipping the other shape.

Two nits the price fix introduced are also gone. The membership row read "&middot; at launch"
directly above "Not open at launch.", because my price rule had a lazy prefix that could cross a
row boundary: once the two named rows carried the words, it attached them to the first un-suffixed
price in the list. It now matches each row by name and cannot leave it. The track card said
"Playbook in progress" and "Book in progress" on successive lines, because an earlier one-way
rewrite had already replaced its label; the four pending cards share one label now.

The four books went into that commit. The previous one staged `site` and `v3` only, so the handoff
folder under `funnel/deliver/pdfs` still held the last build. Lane and handoff hold the same nine
files, checked by hash.

## Print round five: what the auditor's numbers said, and a gate that could not fail

Three books passed and women's soccer failed one page. The furniture passed on position and size
and failed on look: it printed near-black bold, tracked wider than the shelf books, so a series
that should read as one reads as four newcomers. The head and footer now print 9 px, normal
weight, mid-grey, which is what the books already on the shelf measure.

The calendar columns were the real finding, and the real embarrassment. I had written
`table.cal` rules into the template and told myself the grid was fixed, then the auditor measured
that the books disagreed with the shelf and, in one book, with each other, and that the numbers
had not moved between rounds. They could not have moved: no book uses `class="cal"`. The widths
live in each table's own `<th style>`, and most header cells carried no width at all, so the
column took whatever its content wanted. The fix is to set the widths on every cell of every
calendar to the numbers the shelf book's own fragments carry (20% then 38%), and the rule is
enforced by `deck.py` against those fragments read at run time. I proved the lint bites by
changing one width to 31% and watching it fail, then putting it back.

My replacement grid check in `printcheck.py` was worse than the one it replaced, and finding that
out is the useful part of the round. It grouped text runs into columns by the white space between
them. A printed page carries a run per word, not per cell, and the book's prose is justified, so
the "shelf book's calendar" it measured came out 0.17in wide, which is a line of prose. A gate
that compares one kind of noise with another will pass anything, which is precisely the fault I
was trying to correct. The paper-level check is retired, with the reason written where the check
used to be, and the markup lint is the rule now. If the two ever disagree, the paper wins.

Two of the debugging detours were mine and both are worth keeping. A `%s` format string in the
first width pass ate part of a header row and I read it as corruption in the files. The second
pass used `<th([^>]*)>` to read header cells, which also matches inside `<thead>`, because
"thead" begins with "th": every cell came back shifted one place, so a book with widths of 20 and
38 read as one width of 38, and I spent four probes concluding the reference file had lost its
widths. The markup was fine both times; my reading of it was not.

The two content findings are fixed the cheap way. The softball NAIA lead-in carries `.keepnext` so
it cannot leave its table behind. The back page of each book carries `.keep`: the auditor offered
either keeping the colophon with its rule or filling the page, and the first is honest, because a
back page is meant to be short. Men's soccer p23 stays as it is, which the auditor accepted.

On the storefront, the in-progress band had gone grey. Putting it inside the cover is what did
that, because the cover's greyscale filter applies to its children, and the one element on the
tile that says "in progress" was the thing being desaturated. The cover now carries a wash over
its own background and a filter on its text only; the band prints at rgb(210,50,30) again and the
phone page still measures 375 of scroll against a 375 viewport. The deck stopped printing
"Playbooks for this sport" over a list that holds only the $9 eligibility checker: the heading now
requires a written book in the list, measured on the served page for all twelve sports. And the
words "at launch" came off the price numbers, where they broke into three lines on a phone and
left the dot stranded; each row says it in a note instead.

Page counts moved with the wider date column: baseball 26, softball 33, men's soccer 28, women's
soccer 28, and the product pages quote those numbers. Gate 62 of 62. The lane folder holds five
PDFs, the four new books and the shelf reference; the handoff folder holds nine. An earlier record
line said the two folders hold the same nine files, which was wrong in a way the auditor caught:
the comparison was five pairs against nine files.

Left alone, on purpose: at 1440 the three bundle prices do not sit in one column, which is how the
shelf markup has always laid them out and the store auditor called it non-blocking, and the print
auditor's warning on women's soccer p28, which is now short and whole rather than short and split.
