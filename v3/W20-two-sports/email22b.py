# -*- coding: utf-8 -*-
"""W22 part 2: a shorter football email, the girls' email rebuilt the same way, and
the men's sample cleaned of the one thing that identifies a real school.

Research lane: v3/W22-email/research/03, /04, /05, /06.
"""
import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

FB = """<div class="tmpl">Subject: 2029 MIKE LB Danny Whitfield, 6'0" 185, 4.94, Geneva Township HS, WI

Coach Ferraro,

I am a 2029 middle linebacker at Geneva Township High School in Wisconsin. I started 10 varsity
games at MIKE and played two special-teams units. You run a 3-3-4 stack, and I have spent two
seasons reading the A gap against it.

Size, measured by our athletic trainer on 22 May 2027: 6 foot 0, 185 pounds. Tested at the Badger
Combine that day, hand-timed: 40 in 4.94, shuttle in 4.68, vertical 27 inches. A hand time runs
about a fifth of a second fast, so please subtract mine rather than guess.

My line in 10 varsity games in 2026: 58 tackles, 34 solo, 6 for loss, 1.5 sacks, 3 pass breakups,
2 interceptions. GPA 3.62 unweighted on a 4.0 scale, on track with the 16 core courses.
Highlights, 3 minutes, defense included: [link]. One full game, our best opponent: [link]. My next
three games, number 44: 2, 9 and 16 September. Coach Bellamy, my high-school coach, (414)
555-0112. I am at your camp on 12 June.

Are you the coach for linebackers, and what do you still need to see?

Thank you for your time,
Danny Whitfield
(414) 555-0143 &middot; dwhitfield@example.com &middot; parent copied: whitfield@example.com
</div>"""

WBB = """<div class="tmpl">Subject: 2029 PG Madison Weber, 5'7", 12.4 ppg, Geneva Township HS, WI - film inside

Coach Duarte,

I am a 2029 point guard at Geneva Township High School in Wisconsin. I started 26 varsity games
last season and I broke the press against two 1-2-1 pressures. You press for 40 minutes and want
a guard who does not need a help body, so that is the fit I am writing about.

Size, measured barefoot by our club trainer on 22 May 2027: 5 foot 7, wingspan 5 foot 10, 148
pounds. My line in 26 varsity games in 2026: 12.4 points, 6.1 assists and 3.8 rebounds, with 2.1
steals and 2.3 assists for every turnover. Shooting, with attempts: 41% from the field (132 of
322), 31% from three (28 of 91), 82% from the line (61 of 74). GPA 3.62 unweighted on a 4.0 scale,
on track with the 16 core courses.

Highlights, 2 minutes, circled inside the first three plays, defense included: [link]. One full
game where we won and one where we did not: [link]. Club team and summer dates: [link]. Coach
Bellamy, my high-school coach, (414) 555-0112.

Are you the coach for guards, and what do you still need to see?

Thank you for your time,
Madison Weber
(414) 555-0143 &middot; mweber@example.com &middot; parent copied: weber@example.com
</div>"""

W_INTRO = """<h3>The email</h3>
  <p>Write the subject line as a label, not a greeting: class year, position, name, size, one
  number worth asking about, school, state. Stay near 70 letters, because a phone cuts the rest
  off. Send it from the player's own address, not a parent's. A coach reads dozens of these a week
  in season, so the email has one job: answer his first five questions without a reply, then
  stop. A girl's academic line matters more here than in the men's game, because a women's staff
  screens on whether she can be admitted, not only on whether she can play.</p>"""

W_AFTER = """
  <div class="box">
    <h3>Label every number, or a coach discounts all of them</h3>
    <ul class="tight" style="margin-bottom:0">
      <li><strong>Say who measured it, when, and how.</strong> Height barefoot, or the email says
      it is not. One dataset of 12,714 college roster entries found that school-listed heights run
      about an inch generous.</li>
      <li><strong>Put attempts next to every percentage.</strong> "38% from three" is nothing until
      a coach knows whether that is 28 of 91 or 3 of 8, in what league, over how many games.</li>
      <li><strong>Give the assist-to-turnover ratio with the assists</strong>, because a guard who
      scores 20 and turns it over 6 times is a liability at the next level.</li>
      <li><strong>There is no published size standard.</strong> No association, and no women's
      coach on record, states a height, wingspan or sprint minimum by position and level. Every
      floor in the market comes from a service that wants your money. Read the next table that way.</li>
      <li><strong>A missing number is read as a bad number.</strong> Leave the wingspan off and the
      coach assumes it is short. Measure it once, properly, and put the date on it.</li>
    </ul>
  </div>

  <h3>What the services say a body has to look like</h3>
  <p>Two recruiting services publish the ladder below. They are floors, not rules, and no coach is
  obliged to hold you to them. The points and assists are per game, over a season.</p>
  <table class="flow">
    <thead><tr><th>Position</th><th>High D1</th><th>Low D1, high D2</th><th>Low D2, NAIA, high D3</th><th>D3, junior college</th></tr></thead>
    <tbody>
      <tr><td class="d">Point guard</td><td>5'8", 10 ppg, 4 apg</td><td>5'7", 10 ppg, 3 apg</td><td>5'6", 8 ppg, 2.5 apg</td><td>5'5", 6 ppg, 2 apg</td></tr>
      <tr><td class="d">Two guard</td><td>5'10", 12+ ppg</td><td>5'8", 10+ ppg</td><td>5'8", 9+ ppg</td><td>5'8", 8+ ppg</td></tr>
      <tr><td class="d">Three</td><td>5'11", 12 ppg, 8 rpg</td><td>5'10", 11 ppg, 5 rpg</td><td>5'9", 9 ppg, 4 rpg</td><td>5'8", 7 ppg, 3 rpg</td></tr>
      <tr><td class="d">Four</td><td>6'0", 12 ppg, 10 rpg</td><td>5'11", 9 ppg, 6 rpg</td><td>5'10", 8 ppg, 5 rpg</td><td>5'9", 6 ppg, 5 rpg</td></tr>
      <tr><td class="d">Five</td><td>6'2", 12 ppg, 12 rpg</td><td>6'0", 11 ppg, 8 rpg</td><td>5'11", 9 ppg, 7 rpg</td><td>5'11", 7 ppg, 6 rpg</td></tr>
    </tbody>
  </table>
  <p class="small">Floors from All American Sports Recruiting and Go Big Recruiting, both opened 11
  November 2026, with the two sets merged. Nothing in this table is an association rule. For
  scale, the median American girl at 15 is 5 foot 4 and 132 pounds, so a 5'7" sophomore guard is
  already tall for her age, and a 5'8" one is close to done growing.</p>

  <div class="box red">
    <h3>Leave these out of the email</h3>
    <ul class="tight" style="margin-bottom:0">
      <li>A team ranking nobody can link to. "First in the state" invites one search, and if the
      search fails the whole email reads as spin.</li>
      <li>A weighted GPA with no scale next to it. There is no scale anywhere in the country that
      produces 14.2.</li>
      <li>Hand size, sprint times and verticals with no named measurer and no date.</li>
      <li>Free throws, warm-ups, and a dunk reel in the highlight. Six women's coaches on record
      want two minutes, the player circled inside the first three plays, and defense shown.</li>
      <li>Talk of other offers, star ratings, and any ask about money on the first contact.</li>
      <li>Attachments, more than three links, her birth date, and the home address.</li>
    </ul>
  </div>
"""

W_ROWS = """
      <tr><td class="d">Name, position, barefoot height, wingspan</td><td>A coach fills a role, not a seat. Give him the role, and give him the size measured the way he will measure it.</td></tr>
      <tr><td class="d">Class year, school, city, state, club and circuit</td><td>Tells him which calendar she is on and what level of competition the stats came against.</td></tr>
      <tr><td class="d">Per-game stats with games played, and attempts on every percentage</td><td>Let him check the line in one look instead of asking three questions.</td></tr>
      <tr><td class="d">GPA with its scale, and where she stands on the 16 core courses</td><td>Academic fit decides whether an offer is usable at all. A women's staff screens on it early.</td></tr>
      <tr><td class="d">Two links: 2-minute highlights, then one full game</td><td>Label which is which. Link, never an attachment, and the link must open with no login.</td></tr>
      <tr><td class="d">Her summer club, the circuit, and the dates</td><td>Summer 2027 is where most women's staffs make their mind up. He needs the dates to plan a trip.</td></tr>
      <tr><td class="d">Both coaches, with phone numbers</td><td>The next two calls he will make. Put the numbers on the page so he does not have to ask.</td></tr>
      <tr><td class="d">Her own phone and email, with the parent line labelled</td><td>A parent writing in the player's voice is the first thing a coach notices, and not in a good way.</td></tr>
    </tbody>"""

GLOSS2 = (
 '<tr><td class="d">Unweighted GPA</td><td>Grades on a plain 4.0 scale, no bonus for hard classes. '
 'This is the number a coach can compare across states. Print it first.</td></tr>\n'
 '      <tr><td class="d">Weighted GPA</td><td>The same grades with extra points for honors and '
 'Advanced Placement. Schools add differently, on a 4.3, 5.0 or 6.0 scale, so the number means '
 'nothing unless the scale is named next to it.</td></tr>\n'
 '      <tr><td class="d">Verified time</td><td>A number a third party took: the college\'s own '
 'camp, an electronic combine, or a documented laser session. Hand-timed is not verified, and runs '
 'about 0.2 seconds fast.</td></tr>\n'
 '      ')

# ---- football: shorter email -----------------------------------------------
p = pathlib.Path("fb-plain.py"); t = p.read_text(encoding="utf-8")
t = re.sub(r'<div class="tmpl">.*?</div>', FB, t, count=1, flags=re.S)
p.write_text(t, encoding="utf-8")
print("fb: email shortened to", len(re.findall(r"\w+", FB)), "words")

# ---- girls: the same surgery -----------------------------------------------
p = pathlib.Path("wbb-plain.py"); t = p.read_text(encoding="utf-8")
t = re.sub(r'<h3>The email</h3>\s*<p>Write the subject line.*?</p>', W_INTRO, t, count=1, flags=re.S)
t = re.sub(r'<div class="tmpl">.*?</div>', WBB + W_AFTER, t, count=1, flags=re.S)
t = re.sub(r'(<thead><tr><th>Field</th><th>Why a coach needs it</th></tr></thead>\s*<tbody>).*?</tbody>',
           lambda m: m.group(1) + W_ROWS, t, count=1, flags=re.S)
t = re.sub(r'<tr><td class="d">Core GPA</td>.*?</tr>',
           '<tr><td class="d">Core-course GPA</td><td>Her grade point average in only the 16 school '
           'subjects the NCAA counts, computed by the NCAA on a 4.0 scale. Division 1 wants at least '
           '2.3 and Division 2 at least 2.2. It is not her overall GPA, and a counselor has to '
           'certify which of her classes count.</td></tr>', t, count=1, flags=re.S)
i = t.find('<tr><td class="d">Dead period</td>'); j = t.index("</tr>", i) + 5
t = t[:j] + "\n      " + GLOSS2 + t[j:]
k = t.find('<td class="d">11th grade</td><td>'); e = t.index("</td>", k)
t = t[:e] + " Four approved core courses a year keeps every door open. A 2.3 core GPA is the " \
    "Division 1 floor and 2.2 is the Division 2 floor; a 3.0 keeps the early-qualifier option. " + t[e:]
p.write_text(t, encoding="utf-8")
print("wbb: email replaced, rows:", t.count("<tr><td class=\"d\">Name, position, barefoot height"),
      "| glossary:", t.count("Unweighted GPA"), "| checklist:", "2.3 core GPA" in t)

# ---- men's: drop the real school name, name the GPA scale ------------------
pm = pathlib.Path(r"..\\W19-plain\\bball-plain.py"); m = pm.read_text(encoding="utf-8")
n0 = m.count("Pewaukee")
m = m.replace("Pewaukee, WI", "Geneva Township, WI").replace("3.6 GPA |", "3.6 GPA unweighted |")
pm.write_text(m, encoding="utf-8")
print("mens: Pewaukee mentions", n0, "->", m.count("Pewaukee"), "| scale label:", "3.6 GPA unweighted" in m)
