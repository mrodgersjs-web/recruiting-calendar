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
