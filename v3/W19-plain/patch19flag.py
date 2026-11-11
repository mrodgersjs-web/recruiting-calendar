# -*- coding: utf-8 -*-
"""W20 follow-up: close the mens deck open flag about the womens contact date.

Settled 11 Nov 2026 by reading Bylaws 13.1.1.1.5, 13.1.3.1.5, 13.1.3.1.6,
13.1.1.1.3, 13.6.2.1.5 and 13.6.2.1.6 in the 2026-27 manual itself. The November 19
vs November 11-18 discrepancy is left flagged, because it is still open.
"""
import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OLD = ("We could not settle two dates, so we are telling you instead of guessing. First, the day a Division\n"
       "  I <strong>women's</strong> coach may contact you first: One source says March 1 of junior year. Another says June 1 after 10th grade. Treat the men's June 15 date as firm. Confirm the women's date, and the first paid-visit date for boys and girls, in the current rule book before you plan a trip. Second, one page that lists the 2026-27 signing dates prints November 19. The rule text and the recruiting page give November 11 to 18. Both notes are\n"
       "  printed here on purpose. A rule book that admits what it has not checked is more trustworthy than one that hides it.")
NEW = ("One date we could not settle is still open, and one is now closed. Closed: the day a Division\n"
       "  I <strong>women's</strong> coach may make first contact. We read the rule book itself. Calls, texts and email may not\n"
       "  start before June 1 after 10th grade (Bylaw 13.1.3.1.5), and a coach may not meet her off campus before September 1\n"
       "  of 12th grade (13.1.1.1.5). Her paid visit may not start before January 1 of 11th grade (13.6.2.1.6), where a boy may\n"
       "  from August 1 of 11th grade (13.6.2.1.5). If you are reading this book beside a sister or a teammate, use the girls'\n"
       "  dates for her. Still open: one page that lists the 2026-27 signing dates prints November 19, and the rule text and the\n"
       "  recruiting page give November 11 to 18. That note is printed here on purpose. A rule book that admits what it has not\n"
       "  checked is more trustworthy than one that hides it.")

p = pathlib.Path("bball-plain.py"); s = p.read_text(encoding="utf-8")
pat = re.compile(r"\s+".join(re.escape(t) for t in re.split(r"\s+", OLD.strip())))
hits = list(pat.finditer(s))
print("flag paragraph matches:", len(hits))
if len(hits) == 1:
    m = hits[0]; s = s[:m.start()] + NEW + s[m.end():]
    old2 = "[ ] Division I men's contact opens June 15 (for girls, see the note in Chapter 8)"
    new2 = "[ ] Division I men's contact opens June 15 (for a girl, calls open June 1 after 10th grade and off-campus meetings September 1 of 12th grade)"
    if s.count(old2) == 1:
        s = s.replace(old2, new2); print("checklist line updated")
    else:
        print("checklist line matches:", s.count(old2))
    p.write_text(s, encoding="utf-8")
