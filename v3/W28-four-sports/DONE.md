# W28, four sports at once: what shipped and what is still open

Built against the volleyball spine: men's baseball, women's softball, men's soccer,
women's soccer. The template in `TEMPLATE.md` is the deliverable as much as the four
books are; sport five should be a config, eight research files, twelve fragments and a
build.

Nothing here is deployed. Production is still `a8b25e9`. Deploy is Mike's word, and the
CLI is the only way to give it.

## The four books

| Book | Player | Coach | Pages | Reading grade | Facts | Print |
|---|---|---|---|---|---|---|
| Men's Baseball | Diego Whitlock | Coach Tolliver | 26, being reprinted | 4.3 | 0 failures, 0 warnings | 0 failures, 4 warnings |
| Women's Softball | Casey Lindqvist | Coach Brannigan | 33 | 4.8 | 0 failures, 1 approximation | 0 failures, 5 warnings |
| Men's Soccer | Alex Nkemdi | Coach Halloway | 27 | 4.8 | 0 failures, 1 approximation | 0 failures, 5 warnings |
| Women's Soccer | Tori Ellison | Coach Bramley | 27 | 4.5 | 0 failures, 1 approximation | 0 failures, 6 warnings |

The softball book printed at 24 pages on an earlier run and 33 on this one, with no words
added in between. Two web addresses in a two-column source list could not wrap, so Chromium
shrank the whole sheet to fit the width: every chapter title came out at 9.3 pt where the
other books measure 11.6 pt. The shared sheet now lets an address break. The 33 pages are
the book's real length, and the 24-page print was a lie about it that only a geometry audit
could catch.

All four are $29, cover all five divisions, and carry the same eleven chapters, the same
cover furniture, the same sample-email placeholders and the same sources chapter shape as
the volleyball book. Grades are measured on joined lines, not on fragment source lines;
the shipped volleyball book grades 7.3 on the same measure, and that is a v2 job.

`gate.py` runs **62 checks** across the lane, the store and the four books.

## What the audits found, and where it went

Nine auditors were pointed at this work: four on rules and dates, two on numbers and
figures, one on copy, one on print geometry, one on the store at two viewports, one on the
art. Every finding went back to the drafter who owned the sentence, or into a packet row,
or into the shared sheet. Nothing was patched in prose alone.

The three that changed how the lane works:

- **The contract citation was wrong in my own packet.** The five-year limit in the women's
  professional labour agreement is Section 13.7. Article 7A is trialists and amateurs. The
  auditor opened all 129 pages; the packet is corrected and both books now cite 13.7 alone,
  with the numbering stated ("page 22 of the PDF file (printed page 15)").
- **The NAIA's 12 for soccer and baseball is an aid ceiling, not a roster limit.** The
  numbers auditor downloaded the 2026-2027 handbook (41st edition) on 11 November, read
  printed page 123, and found the table heading is "H. Upper Limits for Institutional Aid"
  and that printed page 121 says "No limit will be placed on the number of student-athletes
  on any varsity roster." Every packet row that hedged "no newer edition was located" is
  replaced, and the books say what the number is.
- **Three of the four placeholder surnames were real people.** A class-of-2026 softball
  recruit, a public figure, and a college assistant coach whose surname sat on exactly the
  position his book's player plays. Renamed, with the searches reported in each drafter's
  note. A placeholder's full name now gets the same test a brand name would.

## Store work the audits forced

- A shelf tile shows money only for a book that exists. Nothing unwritten carries a price or
  a button, and the Sport Pack names the two titles in it that are not written yet. Nine books are
  delivered PDFs today; the other seven sports are dated outlines. The word "Pending" is gone
  from the storefront: a band now says "Not written yet", and the ring data carries three states
  (written, rewrite, unwritten) so a book being redone will not read as a book that is missing.
- The ring's data was missing the catalogue rows, which is what blanked the landing ring:
  `undefined.price` in a card template. Any new catalogue row has to be in `playbooks` too.
- Two builder patches in `site.py` were not idempotent and each build stamped another copy
  of the same clause. `ring.js` had 24 copies of one function line. Both are guarded now, and
  both scripts are syntax-checked as part of the build.
- The women's soccer card had no figure, because the image service returns 403 on this
  account. It draws a labelled silhouette instead of a bare pictogram. See *blocked*.
- The Track & Field card is called Nia and stood on a male sprinter while a female runner sat
  unused in the repo; it uses the runner now. The lacrosse goalie is Nora in all three places
  that name her, so the site has one Tori, and she plays women's soccer.

## Deliberate deviations

1. Cream paper prints white, because the four sold PDFs print white. `--paper` is for screens.
2. The brand head and the truth tags print at 8 px (roughly 6 pt), under the auditor's 7 pt
   floor, because they match the sold books. "Match the other playbooks" outranks the floor.
3. The volleyball book's print gate flags three chapter pages, and grades 7.3. It predates
   one-chapter-per-page and the joined-line grader. Both are a v2 reprint of one shipped book,
   not a change to the template.
4. The football book keeps its shipped title. Retitling a sold book to match a template is a
   worse trade than a slightly inconsistent shelf.

## Blocked, and it needs Mike

**Tori has no figure.** `imagegen.generate()` returns `403 {"detail":"Forbidden"}` on this
account, with or without a reference image. The image provider is not configured in
Settings > Models, and only Mike or James can enable it. Until then the women's soccer card
draws the ring silhouette, and the cover draws the crest. The same 403 is why `cut-tori-640`
and `cut-tori-1080` do not exist; the config no longer points at them.

Two known cosmetic things, both optional:

- `IMAGES.json` at the repo root carries prompts for the first generation of renders. The
  live files match `IMAGES-v2.json`. Nothing reads the root file except a human.
- `cut-alex-640.webp` is byte-identical to the repo's only soccer cutout. It is ours and it
  reads clearly as a man holding a ball, but the ball is all white, the shin guards sit over
  the socks, and there is no headroom. A redraw is a nice-to-have.

## To deploy

```
cd C:\Users\Jloeh\Developer\recruiting-calendar
git checkout copy/anon-and-plain-english
python v3/W28-four-sports/gate.py      # 62 checks
vercel deploy --prod
```

## Two notes for whoever builds sport five

After a fresh checkout, run `deck.py` for every book before `gate.py`. The manifests store byte
hashes of the fragments, and Git's autocrlf rewrites them on checkout, so the stored hashes
belong to the machine that built the deck.

`readability.py` and `factcheck.py` both take `--all`. The grade they print is measured on the
finished deck with wrapped lines joined, not on the fragment source. A long URL or an
all-caps table header scores as a hard sentence, which is why the worst "sentence" in the
softball book is a web address at grade 22.9. Judge the prose by the list, not by the number.
