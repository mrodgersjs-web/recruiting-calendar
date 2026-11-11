# -*- coding: utf-8 -*-
"""W22 part 3: repair the checklist cell the first patch put in the wrong column,
say the growth line without a vendor's number, and put the new sources and the new
"we could not settle this" items into Chapter 11 of both decks.
"""
import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SENT = ("Four approved core courses a year keeps every door open. A 2.3 core GPA is the Division 1 "
        "floor and 2.2 is the Division 2 floor; a 3.0 keeps the early-qualifier option. ")

def fix_cell(t, who):
    pat = re.compile(r'<td class="d">11th grade ' + re.escape(SENT) + r'</td><td>')
    t2, n = pat.subn('<td class="d">11th grade</td><td>' + SENT, t)
    print("  11th-grade cell repaired:", n, who)
    return t2

SRC_FB = """
    <src>Go Big Recruiting positional guidelines (linebacker, defensive line, wide receiver,
    offensive line, quarterback) and NCSA football recruiting guidelines, opened 11 November 2026,
    for the size and stat targets in Chapter 6. Both sell a service. Neither is a rule.
    gobigrecruiting.com/recruiting101/football/positional_guidelines and
    ncsasports.org/football/recruiting-guidelines</src>
    <src>Coach &amp; Athletic Director, "Recruiting Benchmarks: A Coaching Blueprint for Film and
    Combine Evaluation," 2026, for the verified 40 and shuttle bands. The article says its
    lower-division columns are the Division 1 column plus 0.15 to 0.25 seconds, so they are
    derived, not measured.</src>
    <src>Two peer-reviewed studies of the delay between a hand raise and a stopwatch, for the
    0.18 to 0.31 second gap between hand and laser times.
    intjexersci.com/files/ijes/vol12/iss6/2.pdf and pubmed.ncbi.nlm.nih.gov/29389695</src>
    <src>FootballScoop, "9 Things That College Coaches Want Parents to Understand About the
    Recruiting Process," 4 March 2025, for what coaches say they screen on, and Bleacher Report's
    "5 Most Deceiving College Football Recruiting Stats" for the tackle-total warning. National
    Scouting Report, "Do High School Stats Matter to College Coaches," for what a staff asks for
    instead of a stat.</src>
    <src>CDC growth chart data files, for the median American boy at 15.5 years of 5 foot 8 and
    130 pounds, and about one inch and nine pounds of growth left in the next year.
    cdc.gov/growthcharts/data/zscore/statage.csv</src>
    <src>Charles Walker, UMass recruiting coordinator, on the volume of recruiting email in
    January: 75 a night. SB Nation, 30 January 2017. NextCommit, "Coach Email Response Rates
    2026," for the finding that a family who emailed 50 or more schools heard back far more often
    than one who emailed fewer than 10. That is a vendor tracking its own users, and it shows
    correlation, not cause.</src>
    <src>NCAA initial-eligibility pages for Division I and Division II and the 2026-27 Guide for
    the College-Bound Student-Athlete, pages 11 to 15, for the 16 core courses, the 10 and 7 rule,
    the 2.3 and 2.2 core GPA minimums, and the removal of the SAT and ACT requirement on 1 August
    2023. ncaa.org/eligibility-center/initial-eligibility-requirements/division-i and the
    division-ii page beside it</src>
"""

SRC_WBB = """
    <src>All American Sports Recruiting women's basketball guidelines, Go Big Recruiting women's
    positional pages and StudBud women's guidelines, opened 11 November 2026, for the height and
    points floors in Chapter 6. These are services that sell a number, and none of them is a
    rule.</src>
    <src>Depth Chart, average height and weight by position and division: 12,714 player-seasons on
    1,060 NCAA rosters, computed 15 October 2026, for the roster heights in Chapter 6 and for the
    finding that school-listed heights run about an inch generous. Men's data, because no women's
    dataset of that size is open. mydepthchart.com/resources/data</src>
    <src>Two peer-reviewed studies of the delay between a hand raise and a stopwatch, for the
    0.18 to 0.31 second gap between a hand time and a laser time.
    intjexersci.com/files/ijes/vol12/iss6/2.pdf and pubmed.ncbi.nlm.nih.gov/29389695</src>
    <src>CDC growth chart data files, for where a 15-year-old American girl already sits against
    her adult height. cdc.gov/growthcharts/data/zscore/statage.csv</src>
    <src>NCAA initial-eligibility pages for Division I and Division II and the 2026-27 Guide for
    the College-Bound Student-Athlete, pages 11 to 15, for the 16 core courses, the 10 and 7 rule,
    the 2.3 and 2.2 core GPA minimums, and the removal of the SAT and ACT requirement on 1 August
    2023. ncaa.org/eligibility-center/initial-eligibility-requirements/division-i and the
    division-ii page beside it</src>
    <src>Charles Walker, UMass recruiting coordinator, on the volume of recruiting email in
    January: 75 a night. SB Nation, 30 January 2017. NextCommit, "Coach Email Response Rates
    2026," for the finding that a family who emailed 50 or more schools heard back far more often
    than one who emailed fewer than 10. A vendor tracking its own users, so it shows correlation,
    not cause.</src>
    <src>Division I graduation and academic progress rates for women's and men's basketball, the
    NCAA research report of May 2025 and the association's release of 5 May 2026, for the academic
    screen a women's staff is working inside.</src>
"""

SETTLE_FB = ("""    <li><strong>Nothing official sets a size or a speed.</strong> No association publishes a """
 """football standard by position: not the NCAA, not the NAIA, not the NJCAA. Every target in """
 """Chapter 6 is a service's floor, printed as one.</li>\n    <li><strong>No coach publishes a stat """
 """threshold.</strong> We found no named coach and no service stating a tackle, sack or reception """
 """number that gets a look at a given level. The chapter prints what staffs say they watch on """
 """film instead.</li>\n""")

SETTLE_WBB = ("""    <li><strong>No norms for a wing, a hand or a sprint.</strong> Nothing published gives a """
 """wingspan, hand size, sprint or vertical figure by position and college level. The only open """
 """numbers are NBA combine averages for professional men, and the claim that a college player sits """
 """10 to 20 percent below them is folklore with no source.</li>\n    <li><strong>No coach states a """
 """stat floor.</strong> The points and assists in Chapter 6 are service floors, and no women's """
 """coach we could find puts a number on paper.</li>\n""")

for fn, src, settle, growth_fix in (
    ("fb-plain.py", None, None, None),
    ("wbb-plain.py", None, None, None)):
    pass

# ---- football deck ---------------------------------------------------------
p = pathlib.Path("fb-plain.py"); t = p.read_text(encoding="utf-8")
t = fix_cell(t, "football")
p.write_text(t, encoding="utf-8")

p = pathlib.Path("fb-sources.html"); t = p.read_text(encoding="utf-8")
t = t.replace('  </div>\n\n  <h3>What we could not settle</h3>', '  </div>\n' + SRC_FB + '\n  <h3>What we could not settle</h3>', 1)
t = t.replace('    <li><strong>The junior college February date.</strong>', SETTLE_FB + '    <li><strong>The junior college February date.</strong>', 1)
p.write_text(t, encoding="utf-8")
print("  football sources added:", t.count("Go Big Recruiting positional"), "| settle items:", t.count("Nothing official sets"))

# ---- girls deck ------------------------------------------------------------
p = pathlib.Path("wbb-plain.py"); t = p.read_text(encoding="utf-8")
t = fix_cell(t, "girls")
t = t.replace("One dataset of 12,714 college roster entries", "One dataset of 12,714 men's college roster entries")
t = t.replace("For scale, the median American girl at 15 is 5 foot 4 and 132 pounds, so a 5'7\" sophomore guard is "
              "already tall for her age, and a 5'8\" one is close to done growing.",
              "For scale, most girls are within about an inch of their adult height by 15, so the size line she "
              "sends as a sophomore is close to the final one.")
p.write_text(t, encoding="utf-8")
print("  girls wording:", "men's college roster entries" in t, "| growth line rewritten:", "132 pounds" not in t)

p = pathlib.Path("wbb-sources.html"); t = p.read_text(encoding="utf-8")
t = t.replace('  </div>\n\n  <h3>What we could not settle</h3>', '  </div>\n' + SRC_WBB + '\n  <h3>What we could not settle</h3>', 1)
t = t.replace('    <li><strong>What share of basketball players get aid.</strong>', SETTLE_WBB + '    <li><strong>What share of basketball players get aid.</strong>', 1)
p.write_text(t, encoding="utf-8")
print("  girls sources added:", t.count("All American Sports Recruiting"), "| settle items:", t.count("No norms for a wing"))
