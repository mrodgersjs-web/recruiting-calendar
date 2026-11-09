#!/usr/bin/env python3
"""W13-copy: rewrite the playbook store and its detail pages at an 8th grade level.

Rules used: one idea per sentence, average under ~16 words, active voice, second
person, no unexplained jargon, no nominalizations. Facts, prices and dates are
unchanged. Run: python v3/W13-copy/rewrite_playbooks.py
"""
import re, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
DRY = "--dry" in sys.argv

# slug: (card blurb, page lede, for-line)
COPY = {
 "football-junior-year": (
   "A month-by-month plan for football recruiting. It starts in the spring of sophomore year and ends at signing.",
   "Football has set windows. Miss one and you cannot get it back. This playbook gives you the dates, who is allowed to call, and what to send them.",
   "For football families, class of 2029."),
 "eligibility-2-hard-deadlines": (
   "Two school rules can end a D1 or D2 dream late. You cannot fix them at the last minute.",
   "Two school rules can end a D1 or D2 dream, and late is too late to fix them. Here is how to get them done early, plus a script for the meeting with your counselor.",
   "For any family aiming at NCAA D1 or D2, grades 9 to 11."),
 "baseball-showcase-to-signing": (
   "Baseball opens later than football. Use the August 1 and September 1 dates and skip the wasted showcase money.",
   "Baseball runs on a later clock than football. Know the August 1 and September 1 dates and the November signing period. Then spend showcase money on the right ones.",
   "For baseball families, class of 2029."),
 "track-field-marks": (
   "Turn your times into a target list, then send the right email for your event.",
   "In track, your time does the talking. Find the schools your marks actually fit, then send each coach the right note for your event.",
   "For track and cross-country families."),
 "d3-academic-aid-first": (
   "D3 schools give no athletic aid. So compare real cost, not a promise.",
   "D3 schools give no athletic money at all. Aid comes from the school, not the coach. Compare the real cost before you fall in love with a roster spot.",
   "For families who want a strong school and a roster spot."),
 "walk-on": (
   "No offer does not mean you are done. Know the two kinds of walk-on first.",
   "No aid offer does not mean you are done. But there are two kinds of walk-on, and one of them is a real trap. Know the difference before you commit.",
   "For athletes with no aid offer who still want to play."),
 "juco-to-d1": (
   "A JUCO year can be a path, not a fallback. Plan your credits first.",
   "A JUCO year can be a path up, not a step down. Plan the credits you can transfer, and know when four-year coaches are allowed to recruit you.",
   "For athletes weighing a JUCO year."),
 "late-bloomer": (
   "Started late? So did some of them. Here is a 90-day plan.",
   "Late to the sport, late to the film, or both. Here is a 90-day plan, who still needs players in the fall, and how to reach them.",
   "For seniors and post-grads who got ready late."),
 "highlight-reel-social": (
   "Make a film a coach will finish watching. Then clean up what they see next.",
   "Coaches watch a few clips, not ten minutes. Build a film they finish. Then fix the profiles they look at before they answer you.",
   "For any athlete building film and an online profile."),
 "camp-roi": (
   "Score a camp before you pay. Know when recruiting talk is allowed there.",
   "Camps can waste a season and a lot of money. Score one before you sign up. Know when coaches are allowed to talk recruiting, then follow up the right way.",
   "For families deciding which camps to pay for."),
 "nil-high-school": (
   "Check a deal against your state and school rules before anyone signs.",
   "A local business can pay your athlete. But your state and your school association set the rules, and they are not the same everywhere. Screen a deal before you sign it.",
   "For high school athletes and parents who were offered a deal."),
 "offer-and-signing": (
   "Put every offer on the same page. Know what binds, and by when.",
   "Offers do not arrive in the same words, so you cannot compare them as they come. Put them on one page, and know what binds you, what binds them, and by when.",
   "For families holding one or more offers."),
}

TRUST_OLD = re.compile(
 r"<p class=\"note\">No calls, no sales team\.[^<]*</p>")
TRUST_NEW = ("<p class=\"note\">No sales calls. Full refund for 30 days. Checkout is in test "
            "mode until we go live. If this file is not ready yet, checkout will say so, and you "
            "can leave your email instead.</p>")

INTRO_OLD = re.compile(r"<p class=\"lede\">Playbooks for the athlete to run[^<]*</p>")
INTRO_NEW = ("<p class=\"lede\">Playbooks your athlete can run, with you helping. Every date "
             "shows the rule it comes from.</p>")

# inside-list labels that assume you already know the jargon
LIST_SWAP = {
 "<li>The 10/7 lock</li>": "<li>The 10/7 core-course rule</li>",
 "<li>The 16-core, 2.3 finish</li>": "<li>16 core courses and a 2.3 GPA</li>",
 "<li>Eligibility Center account</li>": "<li>Setting up the Eligibility Center account</li>",
 "<li>Counselor meeting script</li>": "<li>Script for the counselor meeting</li>",
 "<li>Core GPA worksheet</li>": "<li>Core-course and GPA worksheet</li>",
 "<li>Year-by-year checklist</li>": "<li>Checklist for grades 9, 10 and 11</li>",
 "<li>Baseball&#x27;s different clock</li>": "<li>Baseball runs on a different clock</li>",
 "<li>Aug 1 junior-year contact</li>": "<li>The August 1 contact rule</li>",
 "<li>Sep 1 visits and camps</li>": "<li>September 1 visits and camps</li>",
 "<li>Signing in November</li>": "<li>Signing in November</li>",
 "<li>How D3 aid works (Bylaw 15)</li>": "<li>How D3 aid works (Bylaw 15)</li>",
 "<li>Jan 1 junior-year official visits</li>": "<li>The January 1 visit rule</li>",
 "<li>Net price calculators</li>": "<li>Net price tools</li>",
 "<li>Admissions vs coach support</li>": "<li>School aid vs coach help</li>",
 "<li>When 4-year coaches recruit you</li>": "<li>When four-year coaches can recruit you</li>",
 "<li>Transfer credit planning</li>": "<li>Planning credits you can move</li>",
 "<li>Gap-year cautions</li>": "<li>What to watch before a gap year</li>",
 "<li>When camp recruiting talk opens (by sport)</li>": "<li>When camp talk is allowed, by sport</li>",
}


def sub_lede(html, slug, new):
    """replace the pb-s card blurb inside the cell for this slug"""
    pat = re.compile(r'(<a class="pb-card" href="/playbooks/' + re.escape(slug) +
                     r'".*?<span class="pb-s">)(.*?)(</span>)', re.S)
    def r(m):
        return m.group(1) + new + m.group(3)
    return pat.subn(r, html, count=1)


def sub_detail(html, new_lede, new_for):
    n = 0
    # first plain <p> after the price line is the lede
    pat = re.compile(r'(<p class="pb-p">.*?</p>\s*)<p>.*?</p>', re.S)
    html, c = pat.subn(lambda m: m.group(1) + "<p>" + new_lede + "</p>", html, count=1)
    n += c
    fpat = re.compile(r'<p class="note">For:[^<]*</p>')
    html, c = fpat.subn('<p class="note">' + new_for + "</p>", html, count=1)
    n += c
    return html, n


def main():
    idx_p = ROOT / "site" / "playbooks" / "index.html"
    idx = idx_p.read_text(encoding="utf-8")
    before = idx
    idx = INTRO_OLD.sub(INTRO_NEW, idx)
    idx = idx.replace('<h1 class="d1">Run recruiting yourself. With the rules in hand.</h1>',
                      '<h1 class="d1">Run recruiting yourself, with the rules in hand.</h1>')
    # the store page rendered two identical primary buttons on every card
    idx = re.sub(r'(<button class="btn btn--primary" data-offer="[\w-]+">Get the playbook</button>)\s*'
                 r'<button class="btn btn--primary" data-offer="[\w-]+">Get the playbook</button>',
                 r"\1", idx)
    done = []
    for slug, (card, lede, forline) in COPY.items():
        idx, c = sub_lede(idx, slug, card)
        d = ROOT / "site" / "playbooks" / slug / "index.html"
        if d.is_file():
            t = d.read_text(encoding="utf-8")
            t = TRUST_OLD.sub(TRUST_NEW, t)
            for o, v in LIST_SWAP.items():
                t = t.replace(o, v)
            t, c2 = sub_detail(t, lede, forline)
            if t != d.read_text(encoding="utf-8"):
                if not DRY:
                    d.write_text(t, encoding="utf-8")
                done.append(slug + (" " if c2 else " NO-LEDE-MATCH"))
        else:
            done.append(slug + " MISSING-PAGE")
        if not c:
            done[-1] += " NO-CARD"
    if idx != before and not DRY:
        idx_p.write_text(idx, encoding="utf-8")
    print("cards updated on the store page:", len(COPY))
    for d in done:
        print("  ", d)


if __name__ == "__main__":
    main()
