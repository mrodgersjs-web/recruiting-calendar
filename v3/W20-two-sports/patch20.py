# -*- coding: utf-8 -*-
"""W20: the manual patches the proofreader could not reach, or that a proofreader
must not make (they move a number or a date). Whitespace-flexible; each patch must
match exactly once or the script fails loudly."""
import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

WBB = [
    # 13.6.2.2 states the October 15 split once, in the visit chapter; the other two
    # mentions drop the loose phrase "one visit per player".
    ("Each school may pay for one visit per player. The coach does not have to pay for the best player in the country; he pays for the ones he chooses.",
     "Each school pays for the visit it offers, and it may pay for a second one on or after 15 October of the year she graduates (13.6.2.2). The coach does not have to pay for the best player in the country; he pays for the ones he chooses."),
    ("Visit requests pile up, and each school pays for one visit per player (13.6.2.2).",
     "Visit requests pile up, and each school pays for one visit."),
    ("<strong>Seven looks a year.</strong> Each school gets seven recruiting opportunities per player per year, counting in-person meetings and evaluations together (13.1.5.5).",
     "<strong>Seven per player, per year.</strong> Each school gets seven recruiting opportunities per player per year, counting in-person meetings and evaluations together (13.1.5.5)."),
    ("<li>A sit-in on a class visit or a meal in the dining hall, on her own.</li>",
     "<li>A seat in one real class, and a meal in the student dining hall, on her own.</li>"),
    ("<li>The academic support office, and what it does for players who miss class for travel.</li>",
     "<li>A meeting with the academic support office, and what it does for players who miss class to travel.</li>"),
    ("Send one update with new film. Expect silence in April and July; that is the rule, not a signal.",
     "Send one update with new film. Expect silence from 1 April through 31 July; that is the rule, not a signal."),
    ("It is 416 programs with no athletic aid, which makes it the biggest door and the one most families never open.",
     "There are 416 programs with no athletic aid, which makes Division 3 the biggest door and the one most families never open."),
    ("An unapproved tournament is invisible to a Division I staff, no matter how well she plays.",
     "An unapproved tournament is one that no Division 1 coach may watch, no matter how well she plays."),
    ("Junior college letters of intent may be signed from 1 November.",
     "Junior college letters of intent (a school-binding letter) may be signed from 1 November."),
    ("A $5,000 boarding camp is a holiday, not recruiting.",
     "A $5,000 boarding camp is a vacation, not recruiting."),
    ("The biggest set of seats, and the one families skip. 80% of D3 athletes still get help paying.",
     "The biggest set of seats, and the one families skip. The NCAA says 80% of Division 3 athletes still get help paying, from the school rather than the coach."),
    # The 2028-29 calendar cannot arrive in July 2027: the 2026-27 one arrived in July 2026.
    ("The 2028-29 women's calendar is not published yet; the NCAA will print it in July 2027.",
     "The 2028-29 women's calendar is not published yet. The NCAA prints each calendar in the summer before it starts, so hers lands in July 2028, and committees still move weeks after that."),
]

FB = [
    ("The 2028-29 calendar. It arrives in July 2027.",
     "The 2028-29 calendar. It arrives in the summer of 2028."),
]

def run(fn, pairs):
    p = pathlib.Path(fn)
    s = p.read_text(encoding="utf-8")
    bad = 0
    for old, new in pairs:
        pat = re.compile(r"\s+".join(re.escape(t) for t in re.split(r"\s+", old.strip())))
        hits = list(pat.finditer(s))
        if len(hits) != 1:
            print("PROBLEM %d matches: %r" % (len(hits), old[:80])); bad += 1; continue
        m = hits[0]
        s = s[:m.start()] + new + s[m.end():]
        print("ok  %r" % old[:70])
    p.write_text(s, encoding="utf-8")
    print("%s: %d patched, %d problems\n" % (fn, len(pairs) - bad, bad))

run("wbb-plain.py", WBB)
run("fb-plain.py", FB)
