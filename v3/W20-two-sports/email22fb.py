# -*- coding: utf-8 -*-
"""W22: the football sample email and the size, stat and grade claims around it.

Mike's read: the GPA and the body in the sample email are not believable, and the
email does not answer what a coach actually asks. Research lane:
v3/W22-email/research/01 and /02 (football), /05 (grades), /06 (email form).

Three changes: the sample email is rewritten with a body a 2029 linebacker can
actually have at 16, every number in it names who measured it and how, and the
chapter now shows where the size targets come from, which is a recruiting service,
not a rule book.
"""
import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TMPL = """<div class="tmpl">Subject: 2029 MIKE LB Danny Whitfield, 6'0" 185, 4.94, Geneva Township HS, WI

Coach Ferraro,

I am a 2029 middle linebacker at Geneva Township High School in Wisconsin. I started 10
varsity games at MIKE and played two special-teams units. You run a 3-3-4 stack, and I have
spent two seasons reading the A gap against it.

Size, measured by our athletic trainer on 22 May 2027: 6 foot 0, 185 pounds. Tested at the
Badger Combine the same day, hand-timed: 40 in 4.94, shuttle in 4.68, vertical 27 inches. A
hand time runs about a fifth of a second fast, so please subtract mine rather than guess.

My line in 10 varsity games in 2026: 58 tackles, 34 solo and 24 assisted, 6 for loss, 1.5
sacks, 3 pass breakups, 2 interceptions. GPA 3.62 unweighted on a 4.0 scale. My counselor
sends the official transcript to the NCAA after my sixth semester, and an unofficial one on
request.

Highlights, 3 minutes, defense included: [link]. One full game, our best opponent: [link]. My
next three games with my number: [link]. High-school coach: Coach Bellamy, (414) 555-0112. I
am at your camp on 12 June. Are you the coach for linebackers, and what do you still need to
see?

Thank you for your time,
Danny Whitfield
(414) 555-0143 &middot; dwhitfield@example.com &middot; parent copied: whitfield@example.com
</div>"""

INTRO = """<h3>The email</h3>
  <p>Write the subject line as a label, not a greeting: class year, position, name, size, one
  number worth asking about, school, state. Stay near 70 letters, because a phone cuts the rest
  off. Send it from the player's own address, not a parent's. A coach at a big school reads these
  by the dozen in January: one FBS recruiting coordinator said he went through 75 emails a night,
  and he said he screens on size and speed before he reads a word. So the email has one job. It
  answers his first five questions without a reply, then it stops.</p>"""

AFTER = """
  <div class="box">
    <h3>Label every number, or a coach discounts all of them</h3>
    <ul class="tight" style="margin-bottom:0">
      <li><strong>Say who measured it, when, and how.</strong> "6 foot 0, 185 pounds, measured by
      our athletic trainer, 22 May 2027." Height is barefoot, or the email says it is not.</li>
      <li><strong>A hand-timed 40 is about a fifth of a second faster than the truth.</strong> Two
      studies of start-signal delay put hand times 0.18 to 0.31 seconds fast. Print the method and
      let the coach do his own math.</li>
      <li><strong>The trust order is the college's own camp, then an electronic combine, then a
      documented laser session.</strong> A self-reported time is not a number, and a coach treats
      it as one.</li>
      <li><strong>A missing number is read as a bad number.</strong> Skipping the shuttle does not
      hide it; the coach assumes you did not run it well. Run it at a camp where they write it
      down.</li>
      <li><strong>School-listed heights run about an inch generous</strong>, and star ratings come
      from a service that sells the star. Neither one is a measurement you made.</li>
    </ul>
  </div>

  <h3>What the size targets really are</h3>
  <p>No association publishes a football size or speed standard. Not the NCAA, not the NAIA, not
  the NJCAA. Every chart you are sold comes from a recruiting service. Here is one service's
  linebacker and defensive line ladder, so you can see the shape of it. The 40 in this table is a
  verified time.</p>
  <table class="flow">
    <thead><tr><th>Body</th><th>Power 4 FBS</th><th>Group of 6, high FCS</th><th>Low FCS, high D2, high NAIA</th><th>Low D2, NAIA, D3</th></tr></thead>
    <tbody>
      <tr><td class="d">Linebacker</td><td>6'2", 220 lb, 4.6</td><td>6'1", 210 lb, 4.65</td><td>6'0", 200 lb, 4.7</td><td>5'10", 190 lb, 4.75</td></tr>
      <tr><td class="d">Defensive line</td><td>6'4", 260 lb, 4.8</td><td>6'3", 240 lb, 4.9</td><td>6'2", 230 lb, 4.8</td><td>6'1", 220 lb, 4.9</td></tr>
      <tr><td class="d">Defensive back</td><td>6'0", 185 lb, 4.5</td><td>6'0", 180 lb, 4.6</td><td>5'10", 175 lb, 4.65</td><td>5'9", 160 lb, 4.7</td></tr>
      <tr><td class="d">Wide receiver</td><td>6'0"-6'2", 175-190 lb, 4.40-4.55</td><td>5'10"-6'0", 165-175 lb, 4.55-4.70</td><td>5'8"-5'10", 150-165 lb, 4.55-4.70</td><td>5'8", 150 lb, 4.65-4.80</td></tr>
      <tr><td class="d">Offensive line</td><td>6'3"-6'5", 270-280 lb, 5.00-5.30</td><td>6'2"-6'3", 260-270 lb, 5.15-5.45</td><td>6'1"-6'2", 240-260 lb, 5.15-5.45</td><td>6'1", 240 lb, 5.25-5.55</td></tr>
    </tbody>
  </table>
  <p class="small">Service targets from Go Big Recruiting and Coach &amp; Athletic Director
  benchmarks, both opened 11 November 2026. Targets, not rules, and no coach is obliged to hold
  you to them. Two real rosters for scale: a Division 3 roster carried a linebacker at 188 pounds
  and a Division 2 roster one at 195, so the bottom of the ladder is wider than any poster says.
  For a 15-year-old boy the American median is 5 foot 8 and 130 pounds, which is where most of
  your list started.</p>

  <div class="box red">
    <h3>Leave these out of the email</h3>
    <ul class="tight" style="margin-bottom:0">
      <li>Pancake and knockdown counts. No official scorer keeps them, and a service that asks for
      them is counting for you.</li>
      <li>Bench and squat maxes. One coach on record: "Of all stats, ignore this one."</li>
      <li>A 40 with no method, no event and no date.</li>
      <li>"I lead my team in tackles" with no games played, no solo split and no schedule. Tackle
      totals are the stat a staff trusts least.</li>
      <li>Team record on its own, star ratings, and anything another adult says about him without
      a link.</li>
      <li>Attachments, two video links with no labels, his birth date, and the home address.</li>
      <li>A weighted GPA with no scale next to it. 5.2 means something on a 6.0 scale and nothing
      on a 5.0 scale.</li>
    </ul>
  </div>
"""

ONE_LINE = ("<p>Everything a staff needs to fill its sheet, in the order the staff asks for it: "
 "name, class year, the exact position he plays and his number; school, city, state and "
 "conference; height and weight with the date and who measured; any timed number with its "
 "method, event and date; last season's line with games played; GPA with its scale, plus where "
 "he stands on the 16 core courses; one real reason this school; two links, highlights first and "
 "one full game second; both his coaches' names and phone numbers; his own phone and email, with "
 "the parent line labelled. A survey of college coaches found they were about 50% more likely to "
 "watch film when it went to the right coach and when a transcript came with it. Every field you "
 "leave out is a question he has to answer before he watches.</p>")

GLOSS = (
 '<tr><td class="d">Unweighted GPA</td><td>Grades on a plain 4.0 scale, no bonus for hard '
 'classes. This is the number a coach can compare across states. Print it first.</td></tr>\n'
 '      <tr><td class="d">Weighted GPA</td><td>The same grades with extra points for honors and '
 'Advanced Placement. Every school adds differently, on a 4.3, 5.0 or 6.0 scale, so the number is '
 'meaningless unless the scale is named next to it.</td></tr>\n'
 '      <tr><td class="d">Core-course GPA</td><td>His grade point average in only the 16 school '
 'subjects the NCAA counts, computed by the NCAA on a 4.0 scale. Division 1 wants at least 2.3 and '
 'Division 2 at least 2.2. It is not his overall GPA, and a counselor has to certify which of his '
 'classes count.</td></tr>\n'
 '      <tr><td class="d">Verified time</td><td>A number a third party took: the college\'s own '
 'camp, an electronic combine, or a documented laser session. Hand-timed is not verified, and runs '
 'about 0.2 seconds fast.</td></tr>\n'
 '      ')

for fn, anchors in (("fb-plain.py", {"dead": '<tr><td class="d">Dead period</td>',
                                     "grade11": '<td class="d">11th grade</td><td>'}),):
    p = pathlib.Path(fn); t = p.read_text(encoding="utf-8")
    old = re.search(r'<div class="tmpl">.*?</div>', t, re.S).group(0)
    t = t.replace(old, TMPL, 1)
    t = re.sub(r'<h3>The email</h3>\s*<p>Write the subject line.*?</p>', INTRO, t, count=1, flags=re.S)
    t = t.replace(TMPL, TMPL + AFTER, 1)
    t = re.sub(r'<p>Name, position, height and weight, class year.*?</p>', ONE_LINE, t, count=1, flags=re.S)
    i = t.find(anchors["dead"]); j = t.index("</tr>", i) + 5
    t = t[:j] + "\n      " + GLOSS + t[j:]
    k = t.find(anchors["grade11"]); e = t.index("</td>", k)
    t = t[:e] + " Four approved core courses a year keeps every door open. A 2.3 core GPA is the " \
        "Division 1 floor and 2.2 is the Division 2 floor; a 3.0 keeps the early-qualifier option. " + t[e:]
    p.write_text(t, encoding="utf-8")
    print(fn, "email replaced, 3 blocks added, glossary rows:", t.count("Core-course GPA"),
          "| 11th-grade cell updated:", "2.3 core GPA" in t)
