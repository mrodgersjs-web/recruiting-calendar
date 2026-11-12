/* print.js — the house print recipe for one playbook, run in the Aside browser REPL.
  *
  * There is no Playwright in this Python or in this repo's node_modules: the print step
  * runs in the agent's own browser, which is also the only place the Barlow Condensed and
  * PT Serif subsets are guaranteed present. Paste this whole file into one REPL call, or
  * call printBook(slug) per book. It is the recipe four auditors measured, and the numbers
  * in it are not suggestions:
  *
  *   - the deck goes in as a data: URL, because this build has no file:// browsing;
  *   - media is forced to print, and document.fonts.ready is awaited, or the book prints
  *     in the fallback face at the wrong width;
  *   - preferCSSPageSize with zero Playwright margins, so @page owns the paper and the
  *     14 mm side margins come from the stylesheet;
  *   - the running head comes from headerTemplate, not from the page: a head in the page
  *     would print on the cover, and the cover is a spread;
   *   - the head and the footer render at 9 px, normal weight, mid-grey. A print auditor
      *     measured the shelf books near 6.4 pt of ink; at 8 px in bold this one printed
      *     darker and heavier than its neighbours on the same shelf, which is the one
      *     thing a customer notices about a series that is not quite a series. That is about 6 pt, under a print
  *     auditor's 7 pt floor, and it is what the three books already on the shelf measure,
  *     because a 14 mm-tall head set larger steals ink from the calendar grid;
  *   - printBackground, or the cream chips print as outlines and the date cells lose
  *     their marks.
  *
  * After printing, copy the four PDFs into pdfs/, run site.py --apply twice so the
  * catalogue picks up the page counts, and run gate.py.
  */
const LANE = (typeof process !== 'undefined' && process.env && process.env.PWD)
  ? process.env.PWD + '/'
  : 'C:/Users/Jloeh/Developer/recruiting-calendar/v3/W28-four-sports/';
const PAD = "width:100%;padding:0 14mm;box-sizing:border-box";
/* The style goes in a SINGLE-quoted attribute. In a double-quoted attribute a font
   family name carrying quotes ends the attribute early, and every declaration after
   the truncated font shorthand was dropped: the head printed 0.6 pt tall, and the
   flexbox that pushes the page number to the right edge printed nothing, so the
   number sat glued to the brand on the left. A print auditor measured both, and no
   text-layer check could see either. The family is Arial Narrow, not Barlow
   Condensed, because the template is its own document and loads no webfont. */
/* No quote character of any kind may appear inside this value. The attribute that carries
   it is single-quoted, and a family name in single quotes closed the attribute mid-declaration
   just as happily as one in double quotes: the head printed at 0.7 pt with no font size, no
   letter spacing and no colour at all, and only the content-stream measurement caught it,
   twice, from two different directions. Arial stands in for Barlow Condensed because the
   template is its own document and loads no webfont. */
const HFONT = "font-family:Arial Narrow,Arial,Helvetica,sans-serif;font-size:8.7px;font-weight:400;color:#8a8271";

function headBand(word) {
  return "<div style='" + PAD + ";" + HFONT + ";letter-spacing:.25em;text-transform:uppercase'>"
    + word.toUpperCase() + " PLAYBOOK \u00b7 EDITION 2026-27</div>";
}

/* The footer is a table, not flexbox: the page number belongs at the right edge of
   the paper, and the wording is the one the shelf books carry. */
const FOOT_BAND = "<div style='" + PAD + ";" + HFONT + ";letter-spacing:.08em'>"
  + "<table style=\"width:100%;border-collapse:collapse\"><tr>"
  + "<td style=\"text-align:left;font-weight:400\">The Commit Book \u00b7 Education, not legal advice \u00b7 no outcome promised</td>"
  + "<td style=\"text-align:right\"><span class=\"pageNumber\"></span> / <span class=\"totalPages\"></span></td>"
  + "</tr></table></div>";

function headWord(html) {
  const m = /class="label"[^>]*>The Commit Book\s*(?:&middot;|\u00b7)\s*([^<]+)</i.exec(html);
  if (!m) throw new Error('this deck has no .pagehead label; the running head would come out blank');
  return m[1].trim();
}

async function printBook(slug, outDir) {
  const html = await fs.readFile(LANE + slug + '-deck.html', 'utf8');
  const word = headWord(html);
  const head = headBand(word);
  const tab = await openTab('data:text/html;base64,' + Buffer.from(html, 'utf8').toString('base64'));
  await tab.emulateMedia({ media: 'print' });
  await tab.evaluate(() => document.fonts.ready);
  const path = outDir + slug + '.pdf';
  await tab.pdf({
    path, preferCSSPageSize: true, displayHeaderFooter: true,
    headerTemplate: head, footerTemplate: FOOT_BAND, printBackground: true,
    margin: { top: 0, bottom: 0, left: 0, right: 0 },
  });
  await closeTab(tab);
  const bytes = (await fs.stat(path)).size;
  console.log('printed ' + slug + '.pdf  running head: ' + word.toUpperCase() + ' PLAYBOOK / EDITION 2026-27  ' + Math.round(bytes / 1024) + ' KB');
  return path;
}
