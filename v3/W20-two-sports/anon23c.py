# -*- coding: utf-8 -*-
"""W23 second pass: trim both sample emails to about 180 words, so the sample obeys the
length the research says a coach reads on one phone screen."""
import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

FB = """<div class="tmpl">Subject: 2029 MIKE LB Danny Whitfield, 6'0" 185, 4.94, Anytown South HS, WI

Coach Ferraro,

I am a 2029 middle linebacker at Anytown South High School. I started 10 varsity games at
MIKE and played two special-teams units. You run a 3-3-4 stack. I have spent two seasons
reading the A gap against it.

Size, measured by our athletic trainer on 22 May 2027: 6 foot 0, 185 pounds. Tested the same
day at Impact Athletic Development: hand-timed 40 in 4.94, shuttle 4.68, vertical 27 inches.
A hand time runs about a fifth of a second fast, so subtract it rather than guess.

In 10 varsity games in 2026: 58 tackles, 34 solo, 6 for loss, 1.5 sacks, 3 pass breakups, 2
interceptions. GPA 3.62 unweighted on a 4.0 scale, on track with the 16 core courses.
Highlights, 3 minutes, defense included: [link]. One full game, our best opponent: [link].
My next three games, number 44: 2, 9 and 16 September. High-school coach: Coach Rivera, (555)
555-0112. I am at your 12 June camp.

Are you the coach for linebackers? What do you still need to see?

Thank you for your time,
Danny Whitfield
(555) 555-0143 &middot; player@example.com &middot; parent copied: parent@example.com
"""

WBB = """<div class="tmpl">Subject: 2029 PG Madison Weber, 5'7", 12.4 ppg, Anytown South HS, WI - film inside

Coach Duarte,

I am a 2029 point guard at Anytown South High School. I started 26 varsity games and broke
the press against two 1-2-1 pressures. You press for 40 minutes and want a guard who needs
no help body.

Size, measured barefoot by our club trainer on 22 May 2027: 5 foot 7, wingspan 5 foot 10,
148 pounds. In 26 varsity games in 2026: 12.4 points, 6.1 assists, 3.8 rebounds, 2.1 steals,
2.3 assists per turnover. Shooting, with attempts: 41% from the field (132/322), 31% from
three (28/91), 82% from the line (61/74). GPA 3.62 unweighted on a 4.0 scale, on track with
the 16 core courses.

Highlights, 2 minutes, I am circled in the first three plays, defense included: [link]. One
full game won and one lost: [link]. Club team and summer dates: [link]. My first camp is
Impact Athletic Development this July, and I will send their numbers. High-school coach:
Coach Rivera, (555) 555-0112.

Are you the coach for guards? What do you still need to see?

Thank you for your time,
Madison Weber
(555) 555-0143 &middot; player@example.com &middot; parent copied: parent@example.com
"""


def replace_tmpl(path, newblock):
    p = pathlib.Path(path); t = p.read_text(encoding="utf-8")
    s = t.index('<div class="tmpl">')
    e = t.index("</div>", s)
    t = t[:s] + newblock.rstrip("\n") + "\n\n" + t[e:]
    p.write_text(t, encoding="utf-8")
    body = newblock.split("\n", 1)[1].split("Thank you for your time")[0]
    words = len(re.findall(r"[A-Za-z0-9'%.]+", body))
    subj = re.sub(r"\s+", " ", newblock.split("\n")[0].replace('<div class="tmpl">', "")).strip()
    print("%-16s body words %3d | longest line %3d | subject letters %d"
          % (path, words, max(len(x) for x in newblock.split("\n")), len(subj) - 9))


replace_tmpl("fb-plain.py", FB)
replace_tmpl("wbb-plain.py", WBB)
