# -*- coding: utf-8 -*-
"""W20 batch three: the football fixes the applier could not reach (the proofreader
read the PDF, so table labels and descriptions run together there but are split by
tags in the source), plus the items the proofreader queued and did not reach, plus
the plain-language problems it named in its report.
"""
import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

FB = [
    # --- from the proofreader, re-anchored to the source ---
    ("smaller rosters of aid and a real playoff",
     "less total aid to go around and a real playoff"),
    ("At settlement schools, football is 105",
     "At schools that signed the NCAA settlement (the deal that set the roster limits and ended the old letter-of-intent system), football is 105"),
    ("85 letters of intent per team. Division 2 schools pay",
     "85 letters of intent per team. These are NJCAA divisions, not NCAA ones: NJCAA Division 2 schools pay"),
    ("could sign in a year in 2023, so",
     "could sign in a year in 2023. That is why"),
    ("the real chance of playing somewhere is better than the headline",
     "the real chance of playing somewhere is better than the 8.1% figure"),
    ("ratify it and the NCAA publishes it in July 2028",
     "approve it and the NCAA publishes it in July 2028"),
    ("a staff may evaluate a given player once, and the whole FBS",
     "a staff may evaluate each player once. The whole FBS"),
    ("A verified 40 time and measured height and weight",
     "A verified 40-yard dash time and measured height and weight"),
    # --- named by the proofreader, not reached before it stopped ---
    ("2029 MLB, Geneva Township",
     "2029 LB, Geneva Township"),
    ("the website that ran it has gone dark",
     "the website that ran it has shut down"),
    ("<strong>They treat 7-on-7 as currency.</strong>",
     "<strong>They pay for 7-on-7 and expect credit for it.</strong>"),
    ("they were half again as likely to watch film",
     "they were about 50% more likely to watch film"),
    ("$150 to $538, most of it in the $150 to $250 band.",
     "$150 to $538 per reel. Most jobs land between $150 and $250."),
    ("Expect a quarter or a half, and compare it against academic aid.",
     "Expect a quarter or a half of one year's bill, and compare it against academic aid."),
    ("The largest single group of football seats in the country",
     "The largest single group of football players in the country"),
    ("Stance, fit, run fit versus pass fit, and space. Show him diagnosing, not only hitting. Cover one drop into a zone.",
     "Stance, first step, run defense versus pass coverage, and space in the open field. Show him reading the play before he moves, not only hitting. Add one drop into a zone."),
    ("A back who only shows carries looks like a high-school back.",
     "A back who only shows runs, and never blocks, looks like a high-school player."),
    ("so no rule stands behind the guarantee",
     "so no rule backs the promise"),
]


def run(fn, pairs):
    p = pathlib.Path(fn); s = p.read_text(encoding="utf-8"); bad = 0
    for old, new in pairs:
        pat = re.compile(r"\s+".join(re.escape(t) for t in re.split(r"\s+", old.strip())))
        hits = list(pat.finditer(s))
        if len(hits) != 1:
            print("PROBLEM %d matches: %r" % (len(hits), old[:70])); bad += 1; continue
        m = hits[0]; s = s[:m.start()] + new + s[m.end():]
    p.write_text(s, encoding="utf-8")
    print("%s: %d patched, %d problems" % (fn, len(pairs) - bad, bad))


run("fb-plain.py", FB)

w = pathlib.Path("wbb-plain.py").read_text(encoding="utf-8")
for probe in ("settlement (the deal", "settlement schools", "Subject: ", "as currency", "half again", "gone dark"):
    i = w.find(probe)
    print("WBB %-22s %s" % (probe, "MISSING" if i < 0 else re.sub(r"\s+", " ", w[max(0, i - 90):i + 150])))
