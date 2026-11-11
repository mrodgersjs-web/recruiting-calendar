# -*- coding: utf-8 -*-
"""W23: placeholder names in the sample emails (Mike, 11 Nov 2026).
Any real high school, camp, combine, club or service name is out of every sample email.
High school = "Anytown South High School". Camp = "Impact Athletic Development".
Both email bodies are also reflowed so no line break lands inside a sentence with a
stray indent (the block renders with white-space: pre-wrap), and trimmed to the length
a coach can read on one phone screen."""
import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

FB = """<div class="tmpl">Subject: 2029 MIKE LB Danny Whitfield, 6'0" 185, 4.94, Anytown South HS, WI

Coach Ferraro,

I am a 2029 middle linebacker at Anytown South High School. I started 10 varsity games at
MIKE and played two special-teams units. You run a 3-3-4 stack, and I have spent two
seasons reading the A gap against it.

Size, measured by our athletic trainer on 22 May 2027: 6 foot 0, 185 pounds. Tested the same
day at Impact Athletic Development, hand-timed 40 in 4.94, shuttle 4.68, vertical 27 inches.
A hand time runs about a fifth of a second fast, so subtract mine rather than guess it.

In 10 varsity games in 2026: 58 tackles, 34 solo, 6 for loss, 1.5 sacks, 3 pass breakups, 2
interceptions. GPA 3.62 unweighted on a 4.0 scale, on track with the 16 core courses.
Highlights, 3 minutes, defense included: [link]. One full game, our best opponent: [link].
My next three games, number 44: 2, 9 and 16 September. High-school coach: Coach Rivera, (555)
555-0112. I am at your 12 June camp.

Are you the coach for linebackers, and what do you still need to see?

Thank you for your time,
Danny Whitfield
(555) 555-0143 &middot; player@example.com &middot; parent copied: parent@example.com
"""

WBB = """<div class="tmpl">Subject: 2029 PG Madison Weber, 5'7", 12.4 ppg, Anytown South HS, WI - film inside

Coach Duarte,

I am a 2029 point guard at Anytown South High School. I started 26 varsity games last season
and broke the press against two 1-2-1 pressures. You press for 40 minutes and want a guard
who needs no help body.

Size, measured barefoot by our club trainer on 22 May 2027: 5 foot 7, wingspan 5 foot 10,
148 pounds. In 26 varsity games in 2026: 12.4 points, 6.1 assists, 3.8 rebounds, 2.1 steals,
2.3 assists per turnover. Shooting, with attempts: 41% from the field (132 of 322), 31% from
three (28 of 91), 82% from the line (61 of 74). GPA 3.62 unweighted on a 4.0 scale, on track
with the 16 core courses.

Highlights, 2 minutes, I am circled inside the first three plays, defense included: [link].
One full game we won and one we lost: [link]. Club team and summer dates: [link]. My first
camp is Impact Athletic Development this July, and I will send their verified numbers.
High-school coach: Coach Rivera, (555) 555-0112.

Are you the coach for guards, and what do you still need to see?

Thank you for your time,
Madison Weber
(555) 555-0143 &middot; player@example.com &middot; parent copied: parent@example.com
"""


def replace_tmpl(path, newblock, which=1):
    p = pathlib.Path(path); t = p.read_text(encoding="utf-8")
    starts = [m.start() for m in re.finditer(r'<div class="tmpl">', t)]
    s = starts[which]
    e = t.index("</div>", s)
    t = t[:s] + newblock.rstrip("\n") + "\n\n" + t[e:]
    p.write_text(t, encoding="utf-8")
    body = newblock.split("\n", 1)[1].split("Thank you for your time")[0]
    words = len(re.findall(r"[A-Za-z0-9'%.]+", body))
    lines = [len(x) for x in newblock.split("\n")]
    subj = re.sub(r"\s+", " ", newblock.split("\n")[0].replace('<div class="tmpl">', "")).strip()
    print("%-16s body words %3d | longest source line %3d | subject letters %d"
          % (path.split("/")[-1], words, max(lines), len(subj) - 9))


replace_tmpl("fb-plain.py", FB, 0)
replace_tmpl("wbb-plain.py", WBB, 0)
print("longest football source line check:", max(len(x) for x in FB.split("\n")))
