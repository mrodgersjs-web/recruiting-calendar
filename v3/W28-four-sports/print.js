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
  *   - the head and the footer render at 8 px. That is about 6 pt, under a print
  *     auditor's 7 pt floor, and it is what the three books already on the shelf measure,
  *     because a 14 mm-tall head set larger steals ink from the calendar grid;
  *   - printBackground, or the cream chips print as outlines and the date cells lose
  *     their marks.
  *
  * After printing, copy the four PDFs into pdfs/, run site.py --apply twice so the
  * catalogue picks up the page counts, and run gate.py.
  */
const LANE = process.env.PWD ? process.env.PWD + '/' : 'C:/Users/Jloeh/Developer/recruiting-calendar/v3/W28-four-sports/';
const PAD = 'width:100%;padding:0 14mm;box-sizing:border-box;font:600 8px "Barlow Condensed",Arial,sans-serif;color:#141414';
const FOOT = '<div style="' + PAD + ';display:flex;justify-content:space-between;letter-spacing:.08em">'
  + '<span>recruitingiq \u00b7 the commit book</span>'
  + '<span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>';

function headWord(html) {
  const m = /class="label"[^>]*>The Commit Book\s*(?:&middot;|\u00b7)\s*([^<]+)</i.exec(html);
  if (!m) throw new Error('this deck has no .pagehead label; the running head would come out blank');
  return m[1].trim();
}

async function printBook(slug, outDir) {
  const html = await fs.readFile(LANE + slug + '-deck.html', 'utf8');
  const word = headWord(html);
  const head = '<div style="' + PAD + ';letter-spacing:.25em;text-transform:uppercase">The Commit Book \u00b7 ' + word + '</div>';
  const tab = await openTab('data:text/html;base64,' + Buffer.from(html, 'utf8').toString('base64'));
  await tab.emulateMedia({ media: 'print' });
  await tab.evaluate(() => document.fonts.ready);
  const path = outDir + slug + '.pdf';
  await tab.pdf({
    path, preferCSSPageSize: true, displayHeaderFooter: true,
    headerTemplate: head, footerTemplate: FOOT, printBackground: true,
    margin: { top: 0, bottom: 0, left: 0, right: 0 },
  });
  await closeTab(tab);
  const bytes = (await fs.stat(path)).size;
  console.log('printed ' + slug + '.pdf  head: THE COMMIT BOOK \u00b7 ' + word.toUpperCase() + '  ' + Math.round(bytes / 1024) + ' KB');
  return path;
}
