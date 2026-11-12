# The RecruitIQ sport playbook template

One locked way to add a sport. The four books written on this branch (football, volleyball, and the two
basketball books) were built by hand, one lane each. This file is the rules those four follow, so the next
sport is a content job, not an archaeology job.

A new sport needs five things: **a fact packet, an eleven-chapter deck, a gender-correct ring figure, the
store side, and the gate.** Everything below is what each of those means.

## 1. The book itself

| Item | Locked value |
|---|---|
| Price | **$29**, flat, for every playbook in the store (Mike, 11 Nov 2026) |
| Title form | `<Gender> <Sport>: The Whole Road to College` |
| Slug form | `<gender>-<sport>-road-to-college`, always with the gender, because a men's soccer book and a women's soccer book are two products. The four printed before this rule keep their slugs so old links and emailed receipts still work, and a retired slug gets a `301` |
| Levels covered | NCAA D1, D2, D3, NAIA, junior college, in every book |
| Sample athlete | class of 2029 |
| Cover | logo, red kicker, two-line title, sub paragraph, three-cell stamp, the "What is inside" list, an edge hook, the education-not-advice paragraph |
| Reading level | grade 8 or simpler, measured by `readability.py` on customer text only. The four books today grade 4.4 / 4.9 / 5.1 / 5.7 |
| Print | US Letter, `--paper #f5f1e8 --ink #141414 --red #b5281a --green #1f4d3a`, Barlow Condensed headings, PT Serif body, 14 mm side margins, header, footer and `page N of M` on every page |
| Page breaks | one chapter per fresh page; only `class="flow"` grids and lists may split, and only between rows, with the header row repeated |
| Words | US spelling, jargon explained on first use, no sentence over about 28 words in the plain chapters |
| Nobody named | a real school, camp, club or service never appears in a sample email or subject. `Anytown South High School`, `Impact Athletic Development`, `(555)` numbers, `player@example.com` |
| Nobody in a customer PDF who is a minor | Jacob is never named in a buyer-facing file |

### The eleven chapters, in this order

1. Read this first
2. How many players a team can take
3. The plan by date, class of 2029
4. What a coach may and may not do
5. Club, region, camps, and where the player is seen
6. What to send, and what good video looks like
7. What the paperwork really means
8. What it costs, and what is wasted
9. Checklist by grade
10. Ten ways families get `<sport>` wrong
11. Sources, and what we could not settle

Chapter 2 is the roster and scholarship maths, and it comes before any chapter that spends the family's money,
because in most sports it is the number that matters. Chapter 6 holds the sample email: about 180 words, a
subject of about 70 letters, no state named, and the family's time zone asked for instead.

**The counted-school sample is a slot, not a chapter.** The volleyball book lists every program in one region by
division level with the roster method printed. When a new sport has that count verified, it goes in as chapter 5b
or 6b and the book grows; until then the chapter says plainly how to build the list and does not guess at it.

### Truth tags, printed not hidden

- `UNCONFIRMED`: a claim with no document behind it yet.
- `SERVICE`: a price or number from a vendor's own page, not a governing body.
- `PROJECTED`: a date worked out from rule text that the NCAA has not printed. These live in chapter 3 and are
  listed there as worked-out dates.
- Where two official sources disagree, both figures print, in the chapter that uses them, with both dates.
- Nothing is state-specific outside chapter 11. State association rules read "your state association"; a number
  from one region keeps the number and loses the region's name; school names survive only in chapter 11, labelled
  as one region's sample and not a shortlist.

## 2. Building it

```
python deck.py <slug>          # assemble, lint, write <slug>-deck.html and manifest.json
```
then print in the REPL (headless Chrome aborts in this sandbox, so the browser does the printing):

```js
await pg.goto('data:text/html;charset=utf-8,' + encodeURIComponent(htmlText));
await pg.pdf({ path, format: 'Letter', printBackground: true, preferCSSPageSize: true,
               displayHeaderFooter: true, margin: { top: 0, bottom: 0, left: 0, right: 0 },
               headerTemplate: HEAD, footerTemplate: FOOT });   // both padded 0 14mm
```

Then `python factcheck.py <slug>` before the PDF is trusted, and `python gate.py <slug>` after it is printed.

### Files

| File | What it is |
|---|---|
| `head.txt` | the house CSS, one copy, copied from the volleyball book. Do not fork it per sport |
| `mark.b64` | the logo, inlined so the PDF needs no network |
| `readability.py` | Flesch-Kincaid on customer text only, stripped of tags, tables and source lines |
| `SPORTS/<slug>.json` | the sport's facts-about-the-book: title, kicker, sub, edge, price, ring label, athlete, chapter list, fragment order |
| `fragments/<slug>/cNN-<chapter>.html` | the chapters. Fragments, not one big write: a single long write dies, and a patch script can target one chapter |
| `deck.py` | assembles in the order the JSON names, substitutes `@@LOGO@@`, `@@SPORT@@`, `@@TITLE@@`, `@@SUB@@`, `@@KICK@@`, `@@EDGE@@`, `@@CHECKED@@`, `@@LEVELS@@`, then lints |
| `factcheck.py` | every dollar figure, decimal, percentage, mark and count in the deck must appear in the lane's research files, or be labelled as derived. Generalised from `v3/W24-volleyball/verify24.py` |
| `gate.py` | the printed PDF: page count, header, footer, page number on every page, margins, ink per page, no block split across a page, no banned name outside chapter 11, every claim tag present where a tag is due, the store and ring agree with the PDF. Generalised from `v3/W25-national/qa25.py`, `v3/W20-two-sports/splitcheck2.py` and `v3/W27-nav/check.py` |

`deck.py` fails the build, not the print, on: a fragment missing or orphaned, the contents list not matching the
chapter count, a state name outside chapter 11, a real name inside a sample email, an email off the house length,
a grade above 8, a PROJECTED or SERVICE claim with no tag, or a source line with no document behind it.

## 3. The site side

The store, the product page, the sport page, the ring card and the sitemap are generated from the same
`SPORTS/<slug>.json`, so a book and its listing cannot disagree. `site.py` does this in one pass:

- a `CATALOG.json` product: status `WRITTEN` only when the PDF passed the gate, price 29, page count read out of
  the served file, never typed.
- the PDF copied to `funnel/deliver/pdfs/<slug>.pdf`. That is the only folder `/api/deliver` reads, so a product
  with no file there has no buy button anywhere on the site.
- the store card in the right section, and the section headings re-counted.
- the product page, with the chapter list taken from the deck's own contents block.
- the sport page cell: the sport's own book first, and for a sport with two books both of them, men's first.
- the ring record, with the gender read from the JSON rather than guessed from an id, plus the figure at both
  `-640` and `-1080` because `deck.js` swaps them on phones.
- the sitemap, then a full pass over every `?v=` key. Keys are `md5[:8]` of the **LF** bytes, because
  `core.autocrlf` is on and the deploy serves LF.
- old slugs keep a `301` in `vercel.json`, so a link in an emailed receipt never dies.

A sport whose book is not written shows as a grey tile with a `PENDING` band, no price and no button, and it links
to the free sport page. A pending sport never appears in a bundle promise.

## 4. The ring figure

One card per sport, and men's and women's basketball, baseball, softball and soccer count as different sports.
The figure must read as the right gender at 390 px, be a transparent cutout, keep the ~9:16 canvas with the figure
covering about a third of it, and carry no chroma-green residue. Prompt form used for the existing eight:

> Flat editorial illustration, single athlete, full body, slight three-quarter view, `<kit and equipment>`,
> `<hair and build cues that carry the gender>`, muted print palette on `#f5f1e8`, hard edges, no gradient, no text,
> isolated on pure chroma green `#00b140` for cutout.

Then: cut the green, verify the alpha, produce both sizes, and check the two basketball figures differ by a mean
channel delta of at least 20 of 255 so they are visibly different pictures.

## 5. Who checks the work

Every deck gets four passes from readers with no context: a rules auditor against the primary documents, a numbers
auditor on every figure, a copy auditor on grade and jargon, and a print auditor on the geometry. The lane's own
author is not the auditor. Findings are applied only where they leave every digit and bylaw number where it was.

## 6. The site side of a new sport (what `site.py` does, and the ring rules it enforces)

Read `SPORTS/*.json` plus `manifest-<slug>.json` plus `pdfs/<slug>.pdf`, then, in this order:

1. **Catalogue.** Upsert the product into `v3/W1-playbooks/CATALOG.json`: status WRITTEN only when the gate has
   passed, page count read out of the served PDF and never typed, price 29, chapters from the manifest, and the
   store copy from the config's `site` block. The catalogue is the store's only source of prices and page counts.
2. **Files.** Copy the deck PDF to `funnel/deliver/pdfs/<slug>.pdf`, which is where `/api/deliver` reads from.
3. **Offers.** Rewrite `SPORTS` and `SPORT_BOOK` in `funnel/lib/offers.js` from the written books, so the Sport
   Pack can only be pointed at a book that exists, and recompute the a-la-carte note on both bundles.
4. **Store page.** Rebuild all three sections of `/playbooks`: ready sport books in `STORE.json` order, the
   cross-sport books carried from the current markup, pending tiles for sports with no book. Nothing pending
   carries a price or a button.
5. **Product page.** Write `site/playbooks/<slug>/index.html` from the same template the shipped books use, with
   the chapter list from the manifest and the source links scraped out of the book's own sources chapter.
6. **Sport page.** Put the book's cell on `/sports/<sport_page>`, and on a page that carries two books, the men's
   first and the women's second. A sport page with no book keeps the pending tile and the plain sentence.
7. **Ring record.** Set `name`, `short`, `label`, `poster` to the config's athlete, `sport` to `ring_label`, `img`
   to `cut-<id>-640.webp`, and add `book: "<slug>"`. `ring.js` decides pending-ness from that one field:
   `builtInfo(a)` returns built when `a.book` exists, with the old sport-string guesses kept only as a fallback.
   Order the `athletes` array in the order the ring should show them, and keep `FRONT_IDS` as the first four ids.
8. **Redirects and sitemap.** A retired slug gets a `301` in `vercel.json`; the sitemap gains the new product
   pages; then the cache-key pass, hashing the **LF** bytes of every changed asset and rewriting every `?v=` ref.

**Renames this pass owes, and why.** The softball record was Kayla and the art is a female player; the config's
athlete is Casey, so the name changes and the art does not. The soccer record was `chris` wearing `cut-sprinter`
(the same art as the track card), and men's soccer is now Alex with his own figure. `tori` was the pending lacrosse
card; women's soccer takes the name Tori, so the pending lacrosse record becomes `nora` / "Nora" and keeps its art.
Two cards may not print the same first name, and no card may print art from another sport.

**Art rule.** A card's figure must match the sport and the gender of the book it sells. Check by looking at the
file, not the folder name. Until the image service answers from this machine, the two soccer figures are the gap:
`cut-alex-640/1080.webp` and `cut-tori-640/1080.webp` do not exist, and the store may not ship a soccer card that
shows a track sprinter. If the service stays off, the fallback is a flat figure drawn in-house at the same size and
palette as the others, and the two soccer cards stay pending until it is drawn.

## 7. What the gates were validated on, and the one thing they flag on a shipped book

`deck.py`, `factcheck.py` and `printcheck.py` were all run against the book that
shipped in W24, using `fixtures/volleyball-road-to-college.json` (a config copy, kept out of
`SPORTS/` so the site pass does not treat a shipped book as a new one) and the served volleyball PDF.

- `deck.py` passes it, at grade 5.7, 11 chapters, subject 74 letters, body 175 words.
- `factcheck.py` finds 75 dates, 240 figures and no unsupported date, against the raw source text in
  `v3/W24-volleyball/vb-text.txt`. The only findings were line-heights and column widths read out of
  the stylesheet (1.02, 1.12, 1.35, 1.42, 1.45, 1.46, 1.6, 16%, 30%, 38%); the checker now cuts
  `<style>`, `<script>` and any `class="tmpl"` block before it scrapes, because a line-height is not a
  figure and a sample email is not a claim. **A drafter may not invent a
  ratio: it reports every sum it makes, and the editor puts it in the config's `math_ok` with the
  working shown.**
- `printcheck.py` passes US Letter on all 32 pages, the brand and the page number on every page, 83 date
  cells with none split across a page, and no block cut in half at a break. It reports 3 findings, all the
  same kind: chapters 5, 6 and 8 print a short banner ("Where she is seen", "The email ...", "Prices ...")
  instead of the title their own contents page promises. That is grandfathered on the shipped book and
  **not allowed on a new one: a chapter page prints the title the config lists.**
- `keyphrase()` exists in both `deck.py` and `printcheck.py`. `gate.py` compares the two sources, because a
  template that disagrees with itself about where a chapter starts is worse than no template.
### The document title is part of the book

The deck's `<title>` becomes the PDF's own metadata title, so it is what a family sees in their
Downloads folder and in a browser tab. The house wording, taken from the metadata of the four books
already served, is `<Sport>: The Whole Pathway — The Commit Book Playbook`, set by the `@@DOCTYPE@@`
token in `head.txt` from the config's `pagehead_word`. Never leave a sport name hardcoded in
`head.txt`: it shipped once as Basketball and every book after it would have inherited it.

## 8. Rules this round added (four sports at once, and the audits that caught us)

These came out of building baseball, softball and both soccer books against the
volleyball spine. Each one is a trap we fell into once.

**The stylesheet is the whole head.** Anything after `<body>` prints on page one.
When `head.txt` grew rules in earlier weeks they were appended at the end of the
file, which is *after* `<body>`, and every cover printed
`/* W28: a lead-in line ... */` above the title. Insert into the `<style>` block.

**Chromium print ignores `orphans` and `widows`.** A lead-in line that must not sit
alone at the foot of a page gets `class="keepnext"`; a closing note that belongs to
the block above gets `class="keepwith"`. Both rules are in `head.txt`. The print
auditor judges a cut page by whether an atomic block (a leaf `li`, `blockquote`,
`dd`, `dt`, or a class block holding no markup) was split, not by whether the next
page starts with a lowercase letter.

**The calendar grid belongs to the template.** A table with a `class="d"` date cell
is a calendar: `deck.py` labels it `cal` (or `cal four` when it has four columns) and
writes the `<colgroup>`. `head.txt` sets the widths. Without this, five books set the
same table five different ways, and the WHEN column drifts between 1.2 and 1.8 inches.

**A `math_ok` line has to be written the way the book prints it.** The fact gate reads
money as `$404`, percentages as `7.9 percent`, and plain numbers only when they carry a
thousands comma or a decimal point. A bare `404` in the config proves nothing about a
printed `$404`. Write the sum with its sign: `$379 + the $25 fee is $404`.

**The sources chapter has one citation form: `<src>` blocks.** Name, what was read from
it, then the address. The store page's "Where these dates come from" list is built from
those blocks and stops at the chapter's own `What we could not settle` heading, because
an open question is not a source. If the store pass reports zero sources for a book, it
is reading the wrong end of the chapter.

**`site.py` is only idempotent if you make it so.** Two bugs cost a card:
the sport-page grid was rebuilt by appending, so each tile appeared seven times;
and the pending-card rename ran on every pass, so the second run renamed the *live*
soccer card into the lacrosse slot and the ring printed one card instead of two. The
rename now stops if the new id exists or the old card carries a sold book. The pass
also refuses to write the store when two cards share a name or a sport, because the
ring prints one card per name and the page will not tell you it dropped one.

**The cache-key sweep runs to a fixed point.** `stories.js` carries `?v=` keys for its
own figures, so changing it changes the file behind the pages that link it. One pass
leaves stale keys; the sweep loops until nothing moves.

**Cross-sport strings have one form each.** If a fact appears in four books it is
written once, in these words:
- The junior college chart: `the NJCAA Sports Procedures Chart for 2026-27` plus
  `The chart is reissued during the year, so check the association's own page.` Never a
  file date: three books, three different dates for one chart is a mistake readers can see.
- The NAIA handbook: name the edition the book actually read, and if a newer edition
  exists and was not read, say so.
- Showcase and camp money: a showcase is not a camp. If the fee is added at sign-up,
  the cover prints the total and shows the split.
- The levels line on a cover joins with the middot, never with "and":
  `D1 · D2 · D3 · NAIA · junior college`. `deck.py` builds it from the config.
- Every sport book is $29. `STORE.json`'s `flat_all_titles` is the one-line flip when a
  price changes; the two live basketball product pages get repriced by name.

**The sample email has house placeholders.** `Anytown South HS`, a made-up surname that no
other book uses, `(555)` numbers, `player@example.com`, and a video link written as
`example.com/<name>-video`. A club is `the Anytown Aces, for players 16 and under`, never a
word that reads as a real training business. Two books may not share a coach surname, and
a find-and-replace that leaves "the high school weight room 16U" in a sample email is a
defect, not a draft.

**Email captions state what the machine counted.** Subject lines are counted in characters
not counting spaces; body length is rounded to the nearest five and says "about". A precise
number that is three words off reads worse than a rounded one that is honest.

**Print recipe (nothing else has worked).** Write the deck to a data URL, open it, wait for
fonts, then print:
`goto('data:text/html;base64,...')` then `evaluate(() => document.fonts.ready)` then
`emulateMedia({media:'print'})` then `page.pdf({preferCSSPageSize:true, displayHeaderFooter:true,
headerTemplate, footerTemplate, printBackground:true})`. `path` must be inside the session
directory; the sandbox will not let the browser write elsewhere. Copy the file into the lane
afterwards.

**Two shipped deviations, deliberate.** Cream paper is a design token the printed books do
not use: the page background is white and the cream lives inside boxes, because that is what
every sold PDF looks like. The brand running head is 6.4 pt and the truth tags are 6.6 pt,
under a 7 pt floor, for the same reason. Both are one-line changes for a second edition of
all five books; do not "fix" one book alone.

**A reprint of the first edition needs three page breaks.** The volleyball book predates
one-chapter-per-page, so the print gate flags three chapter pages on it. That is expected
until the book is reprinted with the breaks in.
## 9. Two house rules about the files themselves

**A cover sentence lives in the config, not in the fragment.** The cover is
`@@SUB@@`, `@@EDGE@@` and `@@LEVELS@@` filled from `SPORTS/<slug>.json`. When an audit
flags a cover claim, a drafter that replaces the token with literal text fixes one
build and breaks the rule that the store blurb, the cover and the product page come from
one place. Both times this happened the fix was the same: move the corrected sentence
into the config, restore the token, rebuild. If a fragment ever arrives with a literal
cover line, that is the repair.

**`write_text` on Windows writes CRLF.** Any script in this lane that saves a fragment
with `Path.write_text` flips the file's line endings, which changes the bytes the
manifest hashed, which makes the next reader think someone edited the book. Write repo
text with `Path.write_bytes(t.encode("utf-8"))`, and if a pass leaves CRLF behind, sweep
`fragments/**.html` back to LF and rebuild before comparing hashes.
## 10. What the cover is, and what the print gate reads

**A cover is two sections.** The only rule in the house sheet that starts a fresh page is
`section + section { break-before: page }`. One section holding both the title page and the
contents list puts the contents on page 2 only when the cover happens to be tall enough, and
that is how three of the first four new books landed while the fourth started its contents on
page 1. So `c01-cover.html` closes the cover section after the edge line and opens
`<section class="newpage">` at `<h2 ...>What is inside</h2>`. `lint_cover` reads the cover
*spread* (the first section, plus the second when it carries the contents list), so the lint
still checks the logo, the kicker, the stamp, the contents and the education-not-advice line
without caring where the section break goes.

**The print gate reads page numbers off the footer line only.** A page of source links is
full of digit-slash-digit: `/news/2026/8/24/` and a rule note reading "Adopted: 6/24/26" both
look like a page number to a bare regex, and the first such pair on a page is rarely the
footer. `printcheck.py` now searches the line that contains the footer brand and takes the
pair from there. Anything that scans a PDF text layer for a number must name the line it
trusts.

**Two page-weight rules, and what they mean.** A page under 120 characters is a FAIL: that is
a block the previous page could not hold, not a page. A page under 400 characters is a WARN:
the last page of a chapter, carrying a heading and three real lines, is thin and printable.
Nine warnings across four books were all of that kind and were left alone on purpose. A WARN
that a block "could not be matched whole" is the text layer hyphenating or reflowing a
paragraph, not a split: split blocks are counted separately and every book reports zero.


## 11. What the second half of this round taught, in the order it hurt

**A builder replacement needs a guard when its own search text survives it.**
`site.py` patched `ring.js` with `rj.replace("function builtInfo(a){", "function
builtInfo(a){...}\nfunction builtInfoLegacy(a){", 1)`. The search text is still in the file
after the swap, so every build stamped another copy: 24 copies of one function line and 23
copies of one `SPORT_PATH` clause, and `node --check` called the file a duplicate
declaration. The store still looked fine, because the first definition wins and the rest are
dead weight. Any `site.py` patch that is not naturally idempotent now starts with
`if "<the thing it inserts>" not in <file>`. Syntax-check both scripts after a build:
`node --check site/assets/ring.js` and the same for `deck.js`. A blank ring is not always
missing data; twice now it was a broken script.

**Print a date cell by its pieces, never by the glued string.** The house marks a worked out
date with a chip inside the same cell, so the obvious test is "is `1 Jun 2027 PROJECTED` on
one page". Chromium paints a styled span as its own group, so the text layer can put the chip
between the cell's two lines, and `text-transform` means the layer holds a different case than
the deck. Baseball reported 11 "split" date cells and not one of them was split. The rule now:
every line of a cell, with the marks stripped out, has to appear on one page,
case-insensitively; and the marks are *counted* over the whole file, because a chip that
failed to print is the failure the test exists to catch.

**The footer glues its two halves together.** `recruitingiq · the commit book10 / 27`: flex
puts the brand and the number at opposite ends of the line and the text layer gets no space
between them. The page-number pattern must not use a word boundary, or every page reads as
unnumbered. It is `(?<![\d/])(\d{1,3})\s*/\s*(\d{1,3})(?![\d/])`, applied to the footer line
only.

**The running head and the folio come from the print call, not the deck.** In a browser print
the deck's own `.pagehead` sits inside the page and the margin boxes come from
`headerTemplate` / `footerTemplate`, so a deck that relies on its markup for the head prints
no head at all. `printhead.txt` and `printfoot.txt` in this lane hold the exact two strings,
built at 8 px, which is the ~6 pt ink the sold books measure. The head word is taken from the
deck's own label, so a new sport cannot print a head that disagrees with its cover.

**Never write a note into `head.txt`.** In this lane `head.txt` *is* the book's stylesheet:
`deck.py` concatenates it in front of the fragments, and the only thing in it that changes per
sport is the `<title>` token. A 468-byte note about print furniture was written over it at
17:16, the four books rebuilt with no CSS at all, and the first thing to fail was `readability.py`
somewhere downstream with `"</head>" not found`. The softball drafter had happened to save a
byte-exact copy, so the recovery cost nothing and the lesson cost a rebuild. Two guards are in
now: notes about printing live in `printhead.txt` and `printfoot.txt`, and `deck.py` refuses to
build when `head.txt` has no `</style>` or is under 4,000 bytes, and says which.

**One unbreakable address can shrink an entire book.** Chromium fits a page that overflows
horizontally by scaling it down, so two web addresses in a two-column source list that could not
break made the whole softball print come out at 80 percent of the others: chapter title capitals
9.3 pt where baseball's are 11.6 pt, table headers 4.25 pt against 5.2 pt, a smaller cover
lockup. It looked like a stylesheet problem and it was one `<li>`. The sheet now sets
`overflow-wrap:anywhere; word-break:break-all` on the `src` element, in every book. A print
auditor that measures one book smaller than its siblings should be believed and asked for the
cause, because "the fragments set their own type sizes" is the wrong conclusion to draw from it.

**Grade the sentence, not the source line.** Fragments wrap at about 90 characters, so
grading line by grade cut every long sentence in half and handed the book a grade four levels
easier than a reader gets. `readability.py` joins wrapped lines first. Volleyball, the shipped
book, grades 7.3 on that measure; the four new books sit 4.3 to 4.8 and each chapter under 6.0.

**One counter for the sample email.** `deck.py` counts the subject and the body and prints the
caption, so the caption cannot disagree with the book it describes. The gate used to carry its
own count and drifted by up to seven words across four books.

**A shelf tile may show money only for a book that exists.** `shelf_state()` in `site.py` is
the one place that decides: a WRITTEN row gets a price and a button, anything else gets one
band and no button. A tile can carry `is-soon`, and every state class a tile can carry has to
appear in the store page's own class sweep regex, or the tile is dropped in silence: `is-soon`
was missing once and took eight cards off the page with it. `shelf_list()` makes every product
page lead with its own book, and an add-on strip only ever lists written rows.

**The ring figure rules, so a card is never a lie.** A card with no figure draws the ring
silhouette, and the silhouette is labelled: `role="img"` and an `aria-label` saying it is a
silhouette of a fictional player. A women's sport gets the two cues that still read at 300
pixels, hair tied back and a skirt that flares where the legs hang straight; the plain standing
pose reads as a man, which is how Women's Soccer ended up with a restroom-sign figure. A ball
at the feet names the sport. Alt text on a photograph names the placeholder, calls the person
fictional, and uses the sport's own noun: swimmer, wrestler, track athlete, player.
`IMAGES.json` lists only files that are in the repo, and every row points at the card that
uses it. A female placeholder name must stand on a female figure: the Track & Field card wore
the name Nia over a male sprinter while a female runner sat unused in the media folder for a
month.

**A placeholder's full name gets searched, the same way a brand name would.** Three of the four
first surnames were taken: a real softball recruit with the book's exact name, a public figure
with the soccer book's name, and a college assistant coach whose surname was sitting on the
position the book's player plays. A drafter that renames must report the candidates tested,
what came back for each, and which is clean, and the surname has to be different in every book.

**A citation says which numbering it uses.** The women's professional labour contract's page 22
is printed page 15. A reader who types "page 22" into the PDF and a reader who turns to printed
page 22 get different documents, so the book says "page 22 of the PDF file (printed page 15)".

## 12. The storefront rules the four books forced into the open

These belong to the store, not to a book. Sport five will trip on them the same way.

**Three states, not one flag.** A book is `written`, `rewrite` or `unwritten`. The catalogue's
`status` field gives `written`; the presence of a PDF under `funnel/deliver/pdfs/` is what
separates a book being redone from one that does not exist. `site.py` writes all three into the
ring data as `state`, and every label the carousels print derives from it. The word "Pending"
alone is not allowed on the storefront: it cannot tell a buyer whether money will work.

**A price and a purchase control appear only on a written book.** A stale row in generated data
can put a "Get" button on a book nobody can buy: `stories.js` carried a WRITTEN row for the track
and field outline for weeks. Anything the catalogue knows is normalised to the catalogue on every
build, so a row older than this lane cannot lie.

**Every helper a phone needs must exist in the phone file.** `deck.js` renders the carousel at
749 px and under; `ring.js` renders the desktop ring. They are two files with two templates. A
call to a helper that only exists in the other one empties the whole carousel, and the console
stayed clean because the throw happened inside a `map`. After any edit to either file, look at
the page at 390 px and count the cards. The phone deck measured 10,121 px tall when an unmatched
`</div>` closed a card early; it is 1,977 px now.

**A sport's link comes from `ring_page`, never from the sport label.** Taking the first word of
"Women's Soccer" gives `/sports/women%E2%80%99s`, which is a 404 on eight cards at once.

**Alt text names the person, and the noun replaces the sport instead of following it.**
"Illustration of Casey, a fictional softball player". "a fictional swimming swimmer" is what
appending produces. In both files the helper is `altline` in `ring.js` and `ALTL` in `deck.js`,
and the two must stay in step. The word "lacrosse" contains "cross", so a track test written
against "cross country" mislabels her as a track athlete. Test on "track".

**A figure can be traced when the image model is blocked.** The provider returns 403 on this
account, so the women's soccer card had no illustration. Pillow filled the alpha of an unused
cutout from `v3/W5-athletes/v1media` with the house ink and cropped it to the aspect of its
neighbours: `site/assets/media/sil-womens-soccer-640.webp`. It reads as a person at 300 px, which
a hand-drawn pictogram did not. When the model is enabled, regenerate for real and drop the trace.

**Two commands now take `--all`:** `factcheck.py --all` and `readability.py --all`. The grade is
measured on the finished deck with wrapped lines joined. Long URLs and all-caps table headers
score as hard sentences, so read the list of worst sentences before reacting to the number; the
worst "sentence" in the softball book is a web address at grade 22.9.

## 13. Running the lane, in order

```
python deck.py <slug>            one book, and it refuses to build on a bad stylesheet
python factcheck.py --all        every number and date against the packets
python readability.py --all      the grade a parent reads at
print.js in the browser REPL     the books to PDF, with the house head and footer
python printcheck.py <slug>      per book: geometry, split blocks, split date cells
python site.py --apply           twice. The ring data is written after the pages that
                                 link it, so the cache keys only settle on the second run
python gate.py                   62 checks over the books, the store and the four PDFs
```

Two build habits cost time this week and will cost them again.

**Replace a whole line, do not splice one.** A card template is a chain of quoted
fragments; cutting a `</div>` out of the middle of a literal takes the closing quote with
it, and four rounds of one-character repairs later the file still did not parse. Print the
line, write the line you want, replace the line.

**A generated file is not a source.** `stories.js` and every page under `site/` are output.
Edits belong in `site.py`, `STORE.json`, `SPORTS/*.json`, `head.txt` or a fragment. The
symptom of editing output is that the change is gone the next morning and nothing says so.

**The lane is LF; the repo is mostly CRLF.** It matters only for the twelve fragments per
book whose byte hashes sit in a manifest, because a fresh checkout rewrites them and the
manifest then disagrees. After a checkout, build before you gate.

### The print template, in rules (round four made these binding)

- The `headerTemplate` and `footerTemplate` are HTML documents of their own. A style attribute
  carries no quote character of any kind inside it: `font-family:Arial,Helvetica,sans-serif`,
  never a quoted family name. Put the size in longhand (`font-size:8px`), not in a `font:`
  shorthand. If the value needs quotes, the attribute silently ends there and everything after it
  is thrown away, including the layout. This happened twice, and both times a text-layer check
  passed the book.
- The head names the sport the way the shelf names it, from `pagehead_word`: "MEN'S BASEBALL
  PLAYBOOK · EDITION 2026-27". The footer carries the disclaimer at the left and the page number
  at the right, in a table. Flexbox is not available to a template that lost its style, and
  Chromium's own default style for the template is a bit over half a point.
- 8 px is 6.6 pt on paper, and that is what the shipped books measure. `printcheck.py` fails a
  book whose head or footer prints under 4.5 pt, and fails it per page.
- No `word-break:break-all` in a book. URLs and long words use `overflow-wrap:anywhere`, which
  breaks when a word cannot fit alone instead of breaking everything everywhere.
- A note under a table is a `<tfoot>` row of that table, with the note's class on the cell. A
  paragraph after a table can be separated from it by a page break, and neither `break-before:
  avoid` nor a wrapper div prevents it.
- The calendar grid is fixed in the template, in percentages of this page box: 8.5in of paper
  less two 14 mm margins is a 7.4in text column, so the date column is 24.7%, the second 38%, the
  third the rest. The four-column variant keeps the first two boundaries and splits what is left.
  Measured on paper: the date rule lands at 1.83in, the third column at 4.64in, as the shipped
  book draws them.
- A splitting table glues its first four rows and never leaves its last row alone at the top of a
  page. The template does this for every `.flow` table.
- Print with `print.js`, then run `printcheck.py` per slug, `factcheck.py --all`, then
  `site.py --apply` twice so the catalogue takes the new page counts, then `gate.py`. The checker
  reads geometry off the content stream, so a head that a reader cannot read fails the book.

### Round five, added to the template contract

- A calendar's column widths are markup, on every header cell, at the numbers the book on the
  shelf carries: 20% for the date column, 38% for the second. `deck.py`'s `lint_grid` reads the
  shipped book's fragments when it runs, so nothing is copied into a constant. The `table.cal`
  rules in `head.txt` are a fallback for a table that opts in, not the mechanism, and a template
  rule that governs no markup is how four books came to disagree with a shelf and with each other.
- A grid check on paper cannot work here. A printed page draws a text run per word with no cell
  boundaries, and justified prose splits into "columns" at any gap threshold you pick. Measure the
  claim where it is made.
- The furniture is `font-size:9px;font-weight:400;color:#5a5a5a`, uppercase, tracked .2em. Bold
  near-black at 8 px measures fine and looks wrong next to the books already on the shelf, and
  "looks wrong next to the rest of the series" is a failure a reader can see and no checker has.
- The back section of a book carries `class="keep"` (`break-inside: avoid`). A short last page is
  right; a last page holding nothing but a rule is not.
- Read a cell tag as `<th(\s[^>]*)?>`. `<th([^>]*)>` also matches inside `<thead>`, because
  "thead" starts with "th", and every column then reads one place late.
- A pending tile's cover may not carry `filter: grayscale()` while the band sits inside it. Mute
  the cover with a wash on its own background and filter its text; the band is the one element
  that has to keep its colour.
- A phone deck's "Playbooks for this sport" heading prints only when a written playbook is in the
  list. The $9 eligibility checker is a tool and does not make a shelf.
- Do not glue words to a price. "at launch" belongs in the row's note; on the number it wraps to
  three lines on a phone and strands the separator.
- Prove a new lint by breaking the thing it forbids and reading the failure. Three of today's
  checks passed books they could not have failed.
