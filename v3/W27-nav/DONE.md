# W27: the Playbooks surface shows the four written books, and everything else says pending

Mike, 11 Nov 2026: "Under the Playbooks menu item on the site, it should show these 4 playbooks.
Other sports are pending."

The nav item "Playbooks" is a plain link to `/playbooks` (no dropdown exists on this site), so the
work landed on the page it opens, plus every page that sells the same books.

## What the store page looks like now

Three labelled sections, in this order:

1. **Ready now: four sport playbooks**, in the same order as the athlete ring.

   | Book | Pages | Price | File served |
   |---|---|---|---|
   | Football: The Whole Road to College | 21 | $29 | `funnel/deliver/pdfs/football-junior-year.pdf` |
   | Volleyball: The Whole Road to College | 32 | $29 | `volleyball-road-to-college.pdf` |
   | Basketball: The Whole Road to College | 12 | $19 | `basketball-road-to-college.pdf` |
   | Girls' Basketball: The Whole Road to College | 20 | $19 | `girls-basketball-road-to-college.pdf` |

   Titles, chapter counts and page counts come from each deck's own cover page, read out of the lane
   source, not written from memory. The four PDFs now sit in `funnel/deliver/pdfs/`, which is the only
   folder `/api/deliver` reads, so a purchase actually returns the book.

2. **Every sport: the books that are not about one sport**, the nine cross-sport titles. Only
   Eligibility keeps a buy button, because it is the only one of the nine with a served file. The
   other eight say "Rules being verified", which is the wording the page already used.

3. **Sports still being written**: baseball, softball, track and field, swimming and diving,
   wrestling, lacrosse, soccer. Grey art, a PENDING band across it, no price, no button. The tile
   links to the sport page, which is free information, not a checkout.

## The claims that stopped being true today

- Football's card said 24 pages and an XLSX tracker. The book is 21 pages and ships as a PDF. The
  catalogue, the card, and the product page all now say 21 and PDF, and the card title became the
  book's real title instead of "Junior Year Playbook" for a book that covers grades 9 to 12.
- Eligibility said 12 pages; the file on the server has 5. Cards now say 5. The catalogue is
  corrected to 5, so the gap is visible instead of buried. If Mike wants the 12-page book, that is a
  writing job, not a copy fix.
- Eight cross-sport cards had live buy buttons for books that were never deliverable: a buyer would
  have paid and been told "This edition is still being prepared". Those buttons are gone, and each
  product page says the book is being checked date by date and gets a button when it is done.
- The two sports whose own books were priced here, baseball and track and field, now show "Price set
  when the book is done" instead of a price with no way to pay it.
- Every `?v=` cache key on every page was refreshed against the bytes the deploy will actually
  serve. 82 pages carried the pre-W26 `commit.css`, 70 a stale `stories.js`, 78 a stale
  `checkout.js`, plus one each for `deck.js` and `deck.css`.
- The keys now hash the LF form of each asset, not the working copy. `core.autocrlf` is `true` on
  this checkout, so `checkout.js`, `deck.js` and `deck.css` sit on disk with CRLF while git stores
  and Vercel serves LF. Hashing the disk bytes makes a key that no deployed file ever matches, which
  is how `deck.js` got stuck at the wrong value. Both the pass and the gate normalise before hashing
- `funnel/lib/offers.js`: the Sport Pack's sport list became the four written sports, so the bundle
  can no longer promise a baseball or track book that does not exist. The "Every Playbook" note now
  counts 15 books, $291 a la carte.

## Files

- `v3/W27-nav/catalog_pass.py`: the catalogue (3 new products, football corrected, every WRITTEN
  product's page count set to what its served file really holds), the four served PDFs, the Sport
  Pack list, the pending card styles.
- `v3/W27-nav/pages_pass.py`: the store page, three new product pages, the football page corrected,
  the ten not-on-sale product pages, all ten sport pages, the sitemap, and the cache-key sweep.
- `v3/W27-nav/check.py`: the gate. `v3/W27-nav/pixels27.py`: the pixel measurements below.
  `v3/W27-nav/eol.py`: the CRLF probe behind the cache-key rule.

Both passes are safe to re-run: the second run changes nothing.

## Verified

- Gate: all eight sections pass. Card order and prices, one buy button per deliverable book and none
  for the rest, seven pending tiles with the band and no price, no `/playbooks/` or `/sports/` card
  linking to a missing page, all 83 sitemap URLs resolving to files, every product page for a
  non-sellable book free of buttons and of the "one-time" claim, every cache key matching the bytes
  the deploy serves, the store intro reading at grade 6.7, and no state association or school name on
  the page.
- Page counts cross-checked by opening the served PDFs: 21 / 32 / 12 / 20 as claimed, and the
  volleyball file's cover page really is the volleyball book.
- Browser at 1440: three sections with 4, 9 and 7 cards; buttons on exactly five slugs
  (the four sports plus Eligibility). At 390 the grid is one column with no sideways scroll.
- Pending art is measurably grey: the live thumb averages 82.8 brightness, the pending thumb 150.0,
  and the band is white letters on a dark strip.
- Clicks: volleyball card -> `/playbooks/volleyball-road-to-college/` (buy button, $29, 11 chapters).
  Pending baseball tile -> `/sports/baseball/`. No console errors. The home athlete ring still
  renders 11 ticks with 7 pending after the cache-key sweep.

## Left for Mike

- Prices on the three new books ($29 volleyball, $19 both basketball) are mine, and the page already
  labels all prices as proposed for launch. Change them in `v3/W1-playbooks/CATALOG.json` and re-run
  both passes.
- The eligibility book is a 5-page file. Either the claim drops to 5 everywhere (done) or the book
  gets written up to 12.
- The men's deck's own cover says "boys and girls", while the ring calls that slot Men's Basketball.
  One of the two should move; I did not touch either.
- Nothing deployed. Production is still `a8b25e9`, which shows the old 12-card store.
