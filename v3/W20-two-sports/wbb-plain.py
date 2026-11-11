# -*- coding: utf-8 -*-
"""Girls basketball playbook, plain-language edition. Reuses the W19 house CSS."""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HEAD = open("head.txt", encoding="utf-8").read().replace(
    "Basketball: The Whole Pathway", "Girls Basketball: The Whole Pathway")
LOGO = open("mark.b64", encoding="utf-8").read().strip()
P = []
def A(x): P.append(x)

A("""<section class="cover">
  <div class="lockwrap"><img src="data:image/svg+xml;base64,""" + LOGO + """ alt="The Commit Book"></div>
  <div class="kicker label red">Basketball &middot; girls &middot; grades 9 to 12 &middot; sport playbook</div>
  <h1>Girls' Basketball:<br>The Whole Road to College</h1>
  <p class="sub">What to do, when to do it, who pays, and what a coach is and is not allowed to tell you. Built from the
  2026-27 NCAA Division I rule book, the printed women's basketball calendar, and the NAIA and junior college rule books.</p>
  <div class="stamp">
    <div><span class="label k">Version</span><span class="small">2026-27 &middot; sample player: class of 2029</span></div>
    <div><span class="label k">Rules checked</span><span class="small">11 November 2026, against the rule text and the current calendar</span></div>
    <div><span class="label k">Levels covered</span><span class="small">NCAA D1 &middot; D2 &middot; D3 &middot; NAIA &middot; junior college</span></div>
  </div>
  <p class="edge">Girls' basketball does not run on the same clock as boys' basketball. A girls' list has to be built
  earlier and pushed harder, because the coach has fewer legal ways to find out who you are. This book starts with how
  many players a team can carry. That number decides how many schools to write to, when to start, and how much to spend.</p>
  <h2 style="border-top-width:1.5px;margin-top:8mm">What is inside</h2>
  <ol class="contents">
    <li>Read this first</li>
    <li>How many players a team can take</li>
    <li>The plan by date, class of 2029</li>
    <li>What a coach may and may not do</li>
    <li>Summer teams, visits, and the July rule</li>
    <li>What to send, and what good video looks like</li>
    <li>What the paperwork really means</li>
    <li>What it costs, and what is wasted</li>
    <li>Checklist by grade</li>
    <li>Ten ways families get this wrong</li>
    <li>Sources, and what we could not settle</li>
  </ol>
  <p class="small" style="margin-top:6mm">This is education. It is not legal advice or school advice. It promises no
  result, no playing time, no acceptance, and no money. The NCAA Eligibility Center makes the final call on school
  rules, and each school decides its own aid. Dates marked PROJECTED are worked out from the rule text, not printed by
  the NCAA yet. Chapter 3 lists them.</p>
</section>""")

A("""<section class="newpage">
  <div class="pagehead"><span class="label">The Commit Book &middot; Girls' Basketball</span><span class="label">Before you start</span></div>
  <h2>1. Read this first</h2>
  <p class="lead">Read Chapter 2 before you spend any money. Then put the plan in Chapter 3 on one page and cross items
  off. The rest is for reference: what the rules allow, what to send, what good video looks like, and what it costs.</p>

  <h3>The main idea</h3>
  <p>A family that knows the roster limit, the signing dates, and the video standard competes with families spending
  three times as much. Most of what a $5,000 service sells you is phone calls and follow-ups. The rules, the dates, and
  the right questions are free, and almost nobody writes them down.</p>

  <h3>Why girls' basketball is a different problem</h3>
  <p>Among NCAA schools, there are more teams for girls than for boys: 1,077 women's programs against 1,070 men's. Per player, a
  girl is also more likely to play in college. The NCAA's own figure is 4.7% of high-school girls, against 3.6% of boys.</p>
  <p>The catch is timing. A boys' coach may meet a player off campus in the fall of his junior year. A girls' coach may
  not meet her off campus until 1 September of her senior year. And from 1 April to the end of July a girls' coach may
  not call, text, or email her at all. So a girls' family has to do the work earlier, with fewer tools.</p>

  <h3>Three rules that surprise families</h3>
  <ul class="tight">
    <li>A coach may email or call your daughter from 1 June after 10th grade. He still may not meet her off campus
    until 1 September of 12th grade. Both dates come from the same rule book.</li>
    <li>Each school pays for the visit it offers, and it may pay for a second one on or after 15 October of the year she graduates (13.6.2.2). The coach does not have to pay for the best player in the country; he pays for the ones he chooses. Asking is still your job.</li>
    <li>A coach may watch her play in the summer only at events the NCAA has approved ahead of time. An unapproved tournament is one that no Division 1 coach may watch, no matter how well she plays.</li>
  </ul>

  <h3>Words this book uses</h3>
  <table>
    <thead><tr><th>Word</th><th>What it means here</th></tr></thead>
    <tbody>
      <tr><td class="d">Aid, grant, scholarship</td><td>Money toward tuition, room, food, and books. Same idea, three words. A partial scholarship is less than a full one.</td></tr>
      <tr><td class="d">Equivalency</td><td>How a school adds up partial aid. Ten full grants, or twenty half grants, both equal 10.0.</td></tr>
      <tr><td class="d">Contact</td><td>In the rule book, contact means an in-person meeting. Email and phone calls are separate rules with separate dates.</td></tr>
      <tr><td class="d">Dead period</td><td>No visits and no in-person meetings. Calls and email are still allowed.</td></tr>
      <tr><td class="d">Unweighted GPA</td><td>Grades on a plain 4.0 scale, no bonus for hard classes. This is the number a coach can compare across states. Print it first.</td></tr>
      <tr><td class="d">Weighted GPA</td><td>The same grades with extra points for honors and Advanced Placement. Schools add differently, on a 4.3, 5.0 or 6.0 scale, so the number means nothing unless the scale is named next to it.</td></tr>
      <tr><td class="d">Verified time</td><td>A number a third party took: the college's own camp, an electronic combine, or a documented laser session. Hand-timed is not verified, and runs about 0.2 seconds fast.</td></tr>
      
      <tr><td class="d">Recruiting shutdown</td><td>The strictest period. No contact at all, not even email or calls.</td></tr>
      <tr><td class="d">Certified event</td><td>A summer team or tournament the NCAA approved in advance, so college coaches are allowed to watch it.</td></tr>
      <tr><td class="d">Core-course GPA</td><td>Her grade point average in only the 16 school subjects the NCAA counts, computed by the NCAA on a 4.0 scale. Division 1 wants at least 2.3 and Division 2 at least 2.2. It is not her overall GPA, and a counselor has to certify which of her classes count.</td></tr>
    </tbody>
  </table>
</section>""")

A("""<section>
  <div class="pagehead"><span class="label">The Commit Book &middot; Girls' Basketball</span><span class="label">The numbers</span></div>
  <h2>2. How many players a team can take</h2>
  <p class="lead">This is the chapter that decides everything else. Every school has a limit on how many players it may
  carry or how much aid it may hand out. Multiply the limit by the number of schools and you know how many seats exist.</p>

  <table>
    <thead><tr><th>Level</th><th>What the rule caps</th><th>Schools that play this level</th><th>What that means for your list</th></tr></thead>
    <tbody>
      <tr><td class="d">NCAA Division 1</td><td>15 players on the roster at the schools that signed the NCAA settlement, the 2025 deal that set team-size limits and ended the old letter of intent (Bylaw 17.2, live since 1 July 2025). Aid may be full or partial.</td><td>363 women's programs</td><td>About 5,400 seats a year, and a school may fill them with transfers or players from abroad.</td></tr>
      <tr><td class="d">NCAA Division 2</td><td>10.0 worth of aid per team, split however the coach likes. No cap on roster size (Bylaw 15.4.2.1.2).</td><td>298 programs</td><td>Most D2 players pay part of their own way. Expect a partial offer, not a full ride.</td></tr>
      <tr><td class="d">NCAA Division 3</td><td>No athletic aid at all (Bylaw 15.01.3). Aid comes from the normal financial aid office.</td><td>416 programs</td><td>The biggest set of seats, and the one families skip. The NCAA says 80% of Division 3 athletes still get help paying, from the school rather than the coach.</td></tr>
      <tr><td class="d">NAIA</td><td>8 full-grant equivalents per team, splittable. No limit on roster size.</td><td>Roughly 240 programs</td><td>Real money, and a lower cost of living at many schools. Read the school's own paper; see Chapter 7.</td></tr>
      <tr><td class="d">Junior college (NJCAA)</td><td>15 letters of intent per team. Division II schools may pay tuition only; Division III none.</td><td>About 400 programs</td><td>A one-year deal, and a second start. The paperwork binds for one year only.</td></tr>
    </tbody>
  </table>

  <h3>The two groups already holding Division 1 seats</h3>
  <p>Before your daughter competes for a Division 1 seat, two other groups have taken a share of them.</p>
  <ul class="tight">
    <li><strong>Players from outside the United States.</strong> In 2025-26 the count on Division 1 women's rosters was
    1,042, up from 951 the year before (FIBA and CIES, October 2026). Against about 5,000 players, that is close to one
    seat in five. The NCAA's own tournament count found 130 international players at the 2025 women's tournament, 15% of the players there.</li>
    <li><strong>Transfers.</strong> Of the players on 2026-27 Division 1 women's rosters, 20.8% were new transfers from
    another four-year school (Pathley, October 2026, built from published rosters). In 2022 the NCAA reported 1,276
    women's players entered the transfer portal, the NCAA list where players say they want to transfer, and 93% of them already had aid.</li>
  </ul>
  <p>Put the two together and roughly four of every ten Division 1 seats are filled by someone who was not a
  high-school senior that year. That is not a reason to skip Division 1. It is the reason not to build a list of only
  twelve schools.</p>

  <div class="box red">
    <h3>So how long should her list be?</h3>
    <p>Build the list around the schools she can really reach. For most players that means Division 2, Division 3,
    NAIA, and junior college, with Division 1 as the bonus. A good starting list has all five levels on it:</p>
    <ul class="tight" style="margin-bottom:1.5mm">
      <li>8 to 12 Division 1 schools where she plays a position they need</li>
      <li>10 to 15 Division 2 schools</li>
      <li>10 to 15 Division 3 schools where her grades qualify and the aid fits your family</li>
      <li>5 to 10 NAIA schools</li>
      <li>3 to 5 junior college schools she would truly attend if the spring went badly</li>
    </ul>
    <p>Aim for 40 to 55 schools in total. The lists above add up close to that. If the list is shorter than that, it is a wish, not a plan. If she
    only wants five states, cut the number of schools and start earlier: begin writing in 10th grade, not 11th.</p>
  </div>

  <h3>What the odds really say</h3>
  <p>The NCAA's own math, published March 2026: 356,240 girls played high-school basketball in 2024-25, and 16,823
  played in the NCAA. That is 4.7% overall: 1.4% to Division 1, 1.4% to Division 2, 1.9% to Division 3. The figure
  leaves out the NAIA and junior college entirely, so the real chance of playing after high school is better than
  4.7%. It also means most of the list will be schools she pays to attend, with academic aid on top.</p>
</section>""")


A("""<section class="newpage">
  <div class="pagehead"><span class="label">The Commit Book &middot; Girls' Basketball</span><span class="label">Class of 2029</span></div>
  <h2>3. The plan by date, class of 2029</h2>
  <p class="lead">She graduates in 2029, so her sophomore year ends in June 2027 and her senior year starts in August
  2028. Print this page. The 2028-29 women's calendar is not published yet. The NCAA prints each calendar in the summer before it starts, so hers lands in July 2028, and committees still move weeks after that. Dates
  marked PROJECTED come from the rule text, so treat them as one week either way until the calendar lands.</p>

  <table class="flow">
    <thead><tr><th>Date</th><th>Kind</th><th>What happens</th><th>What to do that month</th></tr></thead>
    <tbody>
      <tr><td class="d">Now, in 10th grade</td><td><span class="tag t-hard">ACTION</span></td><td>Nothing is open yet, and that is the advantage.</td><td>Build the list of 40 to 55 schools. Get her highlight video made once, properly. Send grades to the schools on the list every semester.</td></tr>
      <tr><td class="d">Jun 2027</td><td><span class="tag t-opening">OPENING</span></td><td>Coaches may email, text, and call her. Rule 13.1.3.1.5 and 13.4.1.6.</td><td>Send the first round of email that week. A coach who cannot reply to a 50-word email will not reply to a 500-word one.</td></tr>
      <tr><td class="d">Jul 2027</td><td><span class="tag t-hard">HARD</span></td><td>Summer teams: only NCAA-certified events count for Division 1 coaches.</td><td>Ask the club three questions before you pay: is the event certified, which college staff are invited, and who pays for the film. Get the answers in writing.</td></tr>
      <tr><td class="d">Sep 2027</td><td><span class="tag t-hard">HARD</span></td><td>11th grade begins. Core GPA and the 16 subjects start to matter for real (14.3.1.1).</td><td>Ask the counselor to check her credits against the NCAA list. Fix a bad schedule now, not in December of senior year.</td></tr>
      <tr><td class="d">Jan 2028</td><td><span class="tag t-opening">OPENING</span></td><td>Paid visits may begin. Rule 13.6.2.1.6. This is the earliest date in any women's sport a family can use.</td><td>Ask for a paid visit by email. Name the date you can travel. Bring the questions in Chapter 5.</td></tr>
      <tr><td class="d">Mar 2028</td><td><span class="tag t-opening">OPENING</span></td><td>The March contact period. It is only for seniors and junior-college players, so for her March is a month when coaches can watch her play but cannot contact her. In the rule book's words: it is a watch-only month.</td><td>Use the quiet month: register the no-cost Eligibility Center profile page and fill in her school record.</td></tr>
      <tr><td class="d">Apr&ndash;Jun 2028</td><td><span class="tag t-hard">HARD</span></td><td>Evaluation weekends at certified events: late April, mid May, mid June, and two weekends in July on the current calendar.</td><td>Play on teams that attend those weekends. Ask the club for the event list in March, not in June.</td></tr>
      <tr class="sub"><td colspan="4">Senior year begins</td></tr>
      <tr><td class="d">Jun&ndash;Jul 2028</td><td><span class="tag t-hard">HARD</span></td><td>No contact at all between 1 April and 31 July: no calls, no texts, no email, and no visits during July evaluation periods unless she has already signed.</td><td>Send the last update in March and assume silence until August. Silence in summer is the rule, not disinterest.</td></tr>
      <tr><td class="d">Aug 2028</td><td><span class="tag t-opening">OPENING</span></td><td>Written aid offers may go out. Rule 13.9.3.1.</td><td>Ask each coach one question: what does the written offer say, and when does it arrive? Verbal numbers move; paper does not.</td></tr>
      <tr><td class="d">Sep 2028</td><td><span class="tag t-opening">OPENING</span></td><td>A coach may meet her off campus for the first time. Rule 13.1.1.1.5.</td><td>Take the meetings. Bring the note sheet. Ask about the position, the plan, and the number.</td></tr>
      <tr><td class="d">Oct&ndash;Nov 2028</td><td><span class="tag t-hard">HARD</span></td><td>Visit requests pile up, and each school pays for one visit.</td><td>Choose the three schools you would truly attend and take those visits. Ask the rest to wait until after signing.</td></tr>
      <tr><td class="d">8&ndash;15 Nov 2028 <span class="tag t-projected">PROJECTED</span></td><td><span class="tag t-hard">HARD</span></td><td>Early signing period for basketball, the second Wednesday in November through the following Wednesday (13.02.13.1).</td><td>Have every number, every paper, and every question settled before this week. Ask for the written offer in October.</td></tr>
      <tr><td class="d">Nov 2028</td><td><span class="tag t-hard">HARD</span></td><td>Junior college letters of intent (a school-binding letter) may be signed from 1 November.</td><td>If junior college is a real option, sign there in November and keep the NCAA list alive at the same time.</td></tr>
      <tr><td class="d">Dec 2028&ndash;Feb 2029</td><td><span class="tag t-hard">HARD</span></td><td>Academic final requirements: the 16 subjects, the core GPA, and the diploma (14.3.1.3).</td><td>Do not let grades dip in the senior spring. A coach cannot put a player on the court who the NCAA will not clear.</td></tr>
      <tr><td class="d">11 Apr 2029 <span class="tag t-projected">PROJECTED</span></td><td><span class="tag t-opening">OPENING</span></td><td>Regular signing period opens, the Wednesday one week after the NCAA championships (13.02.13.1). There is no late period in basketball.</td><td>For families who sign late, the school sets the closing date, so ask for it in writing.</td></tr>
    </tbody>
  </table>

  <div class="box">
    <h3>Cost if you miss it</h3>
    <p>Miss the certified-event window and no Division 1 coach sees her play all summer. Miss the paid-visit year and
    you pay for the trip yourself. That stops most families at four schools instead of twelve. Miss the November
    window and, in basketball, there is no late period. She waits for the April date, and the seats are fewer by then.
    Miss the academic finish and a signed offer can be put on hold while the Eligibility Center sorts it out.</p>
  </div>
</section>""")


A("""<section>
  <div class="pagehead"><span class="label">The Commit Book &middot; Girls' Basketball</span><span class="label">The rules that protect you</span></div>
  <h2>4. What a coach may and may not do</h2>
  <p class="lead">These rules exist to stop coaches from putting too much pressure on a 14-year-old. They also explain behavior that
  families often read as rude. A coach who has not called since April has probably not changed his mind. He has hit a limit in the rules.</p>

  <h3>The four kinds of period, and what each one allows</h3>
  <table>
    <thead><tr><th>Period</th><th>In-person meetings</th><th>Visits</th><th>Calls, text, email</th></tr></thead>
    <tbody>
      <tr><td class="d">Contact</td><td>Allowed, on or off campus</td><td>Allowed</td><td>Allowed</td></tr>
      <tr><td class="d">Evaluation</td><td>Off campus, watch only, no talking to her</td><td>Allowed</td><td>Allowed</td></tr>
      <tr><td class="d">Quiet</td><td>On campus only</td><td>Allowed</td><td>Allowed</td></tr>
      <tr><td class="d">Dead</td><td>Not allowed</td><td>Not allowed</td><td>Still allowed</td></tr>
      <tr><td class="d">Shutdown</td><td>Not allowed</td><td>Not allowed</td><td>Not allowed</td></tr>
    </tbody>
  </table>
  <p>The 2026-27 women's calendar, for reference: August is quiet, with a shutdown from the 10th to the 16th.
  September is a contact month, but only for players already in 12th grade. October through February is the evaluation period, at school games only. Christmas is dead for three days. March is a contact month, again only for 12th graders and
  junior-college players. April 1 to 5 is dead, and after that the months are quiet with short evaluation weekends.
  The full grid is one PDF on ncaa.org; print it the year she is a junior.</p>

  <h3>Three limits on how hard a staff may push</h3>
  <ul class="tight">
    <li><strong>Seven per player, per year.</strong> Each school gets seven recruiting opportunities per player per year, counting in-person meetings and evaluations together (13.1.5.5). A coach cannot follow her team every weekend, so
    the events where he can watch her are worth more than an extra tournament.</li>
    <li><strong>65 working days.</strong> The whole women's staff is capped at 65 recruiting days in a year (13.1.7.6).
    Every school has limited staff time. That is why an email that is short, specific and easy to answer gets a
    reply.</li>
    <li><strong>Silence in the spring and summer.</strong> A women's staff may not call, text, or email the player, her
    family, or her club coach from 1 April through July. A men's staff may still reach the family in May and June. If
    your daughter's club coach says "the coach went quiet," ask what month it is.</li>
  </ul>

  <h3>What a coach is allowed to say</h3>
  <p>Before 1 August of 12th grade, a Division 1 school may not put aid in writing for basketball (13.9.3.1). Every
  number you hear before that date is spoken, not written. Coaches know this. It is not a lie; it is a rule. The right
  answer is not to push harder but to ask for a date: "When will that be in writing?"</p>

  <h3>What your family must not do</h3>
  <ul class="tight">
    <li>Do not let a post go out that talks about a school before she is allowed to receive a written offer. Public
    talk counts as a promise to a coach, even when it is not one.</li>
    <li>Do not miss a course in the senior year. The final certification happens after graduation, and the diploma is
    part of it (14.3.1.3).</li>
    <li>Do not sign a junior-college letter of intent as a backup without asking how to get out of it. See Chapter 7.</li>
  </ul>
</section>""")

A("""<section>
  <div class="pagehead"><span class="label">The Commit Book &middot; Girls' Basketball</span><span class="label">Summer and visits</span></div>
  <h2>5. Summer teams, visits, and the July rule</h2>
  <p class="lead">Two decisions cost a girls' family more money than anything else: which club team to join, and which
  visits to say yes to. Both are decided by one rule: a Division 1 coach may watch club basketball only at events
  the NCAA approved in advance.</p>

  <h3>The certification rule, in plain words</h3>
  <p>The NCAA runs a system called the Basketball Certification System. Leagues and tournaments apply to be approved,
  and teams are built inside that system. A Division 1 coach may not attend an event that is not approved, even if ten
  of his rivals are there (Bylaw 13.18). High-school games always count: a coach may watch a school game any time.</p>
  <div class="box red">
    <h3>Ask the club these three questions before you pay</h3>
    <ul class="tight" style="margin-bottom:0">
      <li>Which of our tournaments are NCAA-certified this year? Ask for the list in writing, by name and date.</li>
      <li>Who pays for travel, film, and the entry fees, and what happens to the money if we cut the season short?</li>
      <li>Which college staffs have been invited, and do you invite them or does the event?</li>
    </ul>
  </div>
  <p>One honest note: the big-name circuits concentrate the attention of big schools, but a regional circuit is where most college recruiting happens. A regional circuit costs a fraction as much as the big-name ones. Do not buy the top price for a player who is not yet playing at that level.</p>

  <h3>When a coach may watch her in the summer</h3>
  <p>The girls' window is wider in hours but shorter in days than the boys'. Approved women's events may run from
  8 a.m. to 10 p.m. daily in spring and July. In June the window is noon Thursday to 6 p.m. Saturday. The boys' June
  window is noon Friday to 6 p.m. Sunday. If a club advertises a "Sunday final" in June for a girls' team, ask who can
  actually watch it.</p>

  <h3>Visits: what is free, and what is not</h3>
  <ul class="tight">
    <li><strong>Paid visit.</strong> The school may pay from 1 January of 11th grade (13.6.2.1.6). Each school may pay
    for one visit before 15 October of the year after she graduates, and one more after that date (13.6.2.2). She needs a transcript and an Eligibility Center registration first (13.6.3).</li>
    <li><strong>Free visit.</strong> Her family pays. There is no limit on the number, and it is allowed at any time
    except during dead periods and shutdowns (13.7.1.5).</li>
    <li><strong>Free tickets.</strong> A school may give up to three free tickets to its own events, if the event is within 30 miles of campus, in general seating. No free tickets during a dead period (13.7.3.1).</li>
    <li><strong>The July catch.</strong> In July, no visit at all, paid or free, unless she has already signed the
    school's offer of admission or aid, or put down a deposit (13.6.2.1.6.1 and 13.7.2.2).</li>
  </ul>
  <p>Family travel is never free. A weekend of two nights runs about $500 to $1,500 once you add gas or airfare, the
  room, and meals. Plan one target school per summer, not one per month.</p>

  <h3>Ask for these four things on a visit</h3>
  <ol class="tight">
    <li>A meeting with the position coach, not only the head coach.</li>
    <li>A seat in one real class, and a meal in the student dining hall, on her own.</li>
    <li>A plain answer on what she would be asked to do in year one, and who is ahead of her.</li>
    <li>A meeting with the academic support office, and what it does for players who miss class to travel.</li>
  </ol>
</section>""")


A("""<section>
  <div class="pagehead"><span class="label">The Commit Book &middot; Girls' Basketball</span><span class="label">Film and outreach</span></div>
  <h2>6. What to send, and what good video looks like</h2>
  <p class="lead">Only one in three Division 1 coaches watches all the video that is sent to them. Most coaches decide in
  about two minutes. So the video has to be short, honest, and easy to follow, and the email has to answer the questions
  a coach would otherwise have to ask.</p>

  <h3>The video</h3>
  <ul class="tight">
    <li><strong>Two minutes.</strong> A panel of college women's coaches asked for two minutes and no tricks: no slow
    motion, no music, no free throws. Show range in a small number of games.</li>
    <li><strong>Her first, and in the first three plays.</strong> Mark her with an arrow or a box on every clip. Do not
    make a coach hunt. If he cannot find her in three seconds, he stops.</li>
    <li><strong>One full game, ready to send.</strong> A highlight reel is the advertisement; the full game is the proof.
    Shoot wide, from a high angle, so the whole floor is visible.</li>
    <li><strong>Defense and rebounding.</strong> Guard your own player, box out, and move without the ball. Most girls'
    video is only catches and layups, and coaches notice.</li>
    <li><strong>No mistakes hidden.</strong> Do not cut every miss. A coach who finds out later stops trusting the tape.</li>
  </ul>

  <h3>The email</h3>
  <p>Write the subject line as a label, not a greeting: class year, position, name, size, one
  number worth asking about, school, state. Stay near 70 letters, because a phone cuts the rest
  off. Send it from the player's own address, not a parent's. A coach reads dozens of these a week
  in season, so the email has one job: answer his first five questions without a reply, then
  stop. A girl's academic line matters more here than in the men's game, because a women's staff
  screens on whether she can be admitted, not only on whether she can play.</p>
  <div class="tmpl">Subject: 2029 PG Madison Weber, 5'7", 12.4 ppg, Geneva Township HS, WI - film inside

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
</div>
  <div class="box">
    <h3>Label every number, or a coach discounts all of them</h3>
    <ul class="tight" style="margin-bottom:0">
      <li><strong>Say who measured it, when, and how.</strong> Height barefoot, or the email says
      it is not. One dataset of 12,714 men's college roster entries found that school-listed heights run
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
  November 2026, with the two sets merged. Nothing in this table is an association rule. For scale, most girls are within about an inch of their adult height by 15, so the size line she sends as a sophomore is close to the final one.</p>

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


  <h3>What goes on the one page she sends with it</h3>
  <table>
    <thead><tr><th>Field</th><th>Why a coach needs it</th></tr></thead>
    <tbody>
      <tr><td class="d">Name, position, barefoot height, wingspan</td><td>A coach fills a role, not a seat. Give him the role, and give him the size measured the way he will measure it.</td></tr>
      <tr><td class="d">Class year, school, city, state, club and circuit</td><td>Tells him which calendar she is on and what level of competition the stats came against.</td></tr>
      <tr><td class="d">Per-game stats with games played, and attempts on every percentage</td><td>Let him check the line in one look instead of asking three questions.</td></tr>
      <tr><td class="d">GPA with its scale, and where she stands on the 16 core courses</td><td>Academic fit decides whether an offer is usable at all. A women's staff screens on it early.</td></tr>
      <tr><td class="d">Two links: 2-minute highlights, then one full game</td><td>Label which is which. Link, never an attachment, and the link must open with no login.</td></tr>
      <tr><td class="d">Her summer club, the circuit, and the dates</td><td>Summer 2027 is where most women's staffs make their mind up. He needs the dates to plan a trip.</td></tr>
      <tr><td class="d">Both coaches, with phone numbers</td><td>The next two calls he will make. Put the numbers on the page so he does not have to ask.</td></tr>
      <tr><td class="d">Her own phone and email, with the parent line labelled</td><td>A parent writing in the player's voice is the first thing a coach notices, and not in a good way.</td></tr>
    </tbody>
  </table>

  <h3>What coaches say they want</h3>
  <p>Two things repeat in what women's coaches say in public. The first is that a coach must see a player more than
  once in person before he can judge her. One great weekend proves very little. The second is that playing well in a
  certified summer event, in the months when coaches are legally allowed to watch, is the cheapest way to get on a
  staff's list. Everything else, including a paid service, just puts another person between you and the coach.</p>

  <h3>How to follow up, and how to ask for a number</h3>
  <ul class="tight">
    <li>Wait one to three business days after an email, then call the office number and ask for the coach who covers
    her position and her region.</li>
    <li>Ask two questions: where do I stand on your list, and what do you still need to see. Do not ask about a
    scholarship on the first call.</li>
    <li>If a coach gives a cell number, ask before texting. Text between 8 in the morning and 9 at night in the
    coach's own time zone, and sign your full name.</li>
    <li>Send an update every eight to ten weeks, with one new fact in it. New film, a new average, a new award, a
    schedule change. Anything that gives the coach a reason to look again.</li>
  </ul>
</section>""")

A("""<section>
  <div class="pagehead"><span class="label">The Commit Book &middot; Girls' Basketball</span><span class="label">The paperwork</span></div>
  <h2>7. What the paperwork really means</h2>
  <p class="lead">There is exactly one moment when a promise becomes a deal: the day a paper is signed. Everything
  before that is talk, and a coach is allowed to talk. Here is each document, and what it does.</p>

  <table class="flow">
    <thead><tr><th>Document</th><th>When it may be signed</th><th>What it does</th></tr></thead>
    <tbody>
      <tr><td class="d">Verbal commitment</td><td>Any time, by phone or text</td><td>Nothing. It binds neither family nor school. It only tells other coaches to stop calling.</td></tr>
      <tr><td class="d">Written offer of aid</td><td>Division 1: on or after 1 August of 12th grade (13.9.3.1)</td><td>States the number. She still cannot accept it until the signing window opens.</td></tr>
      <tr><td class="d">Athletics aid agreement</td><td>Early: 8 to 15 Nov 2028 (PROJECTED). Regular: from 11 Apr 2029. No late period.</td><td>The real deal. Once she signs, the other schools must stop recruiting her.</td></tr>
      <tr><td class="d">Division 2 award letter</td><td>From the sport's signing date</td><td>Binds one year of aid on written terms. Renewal is not automatic, even when a coach says four years.</td></tr>
      <tr><td class="d">Division 3 aid package</td><td>Ordinary admissions calendar</td><td>Admission plus a roster spot plus regular aid. Letters of intent are banned in Division 3 (13.9.1).</td></tr>
      <tr><td class="d">NAIA school letter</td><td>School policy</td><td>The NAIA does not run a national letter program and will not enforce one. Her school writes its own letter, and that letter may or may not bind.</td></tr>
      <tr><td class="d">Junior college letter of intent</td><td>From 1 November</td><td>Binds one school year, August to July. A parent signs too if she is under 18, and leaving takes a written release.</td></tr>
    </tbody>
  </table>

  <h3>What the settlement changed, in one paragraph</h3>
  <p>The National Letter of Intent no longer exists. The NCAA ended it in October 2024, for both Division 1 and
  Division 2, and the website that ran it is now offline. Written offers of aid replaced it. In basketball the offer may
  go out on or after 1 August of senior year, but she may only sign it in the November window or from the April date.
  Nothing else in this process is enforceable. A coach who says "we have a spot for you" in March of junior year is
  allowed to say it and wrong to hold you to it.</p>

  <h3>The protections you do have</h3>
  <ul class="tight">
    <li>School aid cannot be cut during the year she signed because of a coach's opinion of her play, or because of an injury. The rule lists six reasons, and she gets a hearing first (15.3.4.1, 15.3.4.2).</li>
    <li>After she signs, other schools may not contact her, which protects her from a bidding war she cannot win.</li>
    <li>At a school using the new rules, a roster seat cannot be handed to a transfer until she leaves. The NCAA has said plainly that a spot lost for roster reasons does not let a school take the money back.</li>
  </ul>

  <div class="box">
    <h3>Four questions to ask about any paper you are sent</h3>
    <ol class="tight" style="margin-bottom:0">
      <li>Who has to sign this on the school's side for it to be valid?</li>
      <li>What exactly does it cover: tuition, fees, books, room, food?</li>
      <li>How long does it last, and what has to happen for it to be renewed?</li>
      <li>If she transfers or is injured, what happens to the money, and who decides?</li>
    </ol>
  </div>
</section>""")


A("""<section>
  <div class="pagehead"><span class="label">The Commit Book &middot; Girls' Basketball</span><span class="label">Money</span></div>
  <h2>8. What it costs, and what is wasted</h2>
  <p class="lead">These are published prices, checked 11 November 2026. One row below has no published price. It is the recruiting service row, and its numbers come from other companies, not from the NCAA.
  A family that plans on $3,000 to $6,000 a year and skips the expensive packages can finish this whole
  process with money left over.</p>

  <div class="box">
    <h3>The whole-year number</h3>
    <p>One of the largest services in the market says a recruiting family spends $3,000 to $10,000 a year, and
    $15,000 to $50,000 across high school. That number comes from a company that sells this work, so treat it as the high end of a realistic range. In 10th
    and 11th grade a family can do this well for $3,000 to $6,000. Travel is the biggest line, and a $50 to $95 film
    breakdown is the cheapest item with real value.</p>
  </div>
<table class="flow">
    <thead><tr><th>What you buy</th><th>Real price</th><th>Buy it or skip it</th></tr></thead>
    <tbody>
      <tr><td class="d">Club or AAU team, one season</td><td>$700 to $4,400, plus $100 to $430 in uniforms. The big-name national circuits start near $4,000.</td><td>Buy it once a year, and only for a team whose events are NCAA-certified. Ask what the fee covers before you sign.</td></tr>
      <tr><td class="d">AAU membership</td><td>$22 to $24</td><td>Not optional if she plays AAU. One membership covers 1 September to 31 August.</td></tr>
      <tr><td class="d">Tournament entry</td><td>$185 to $700 per team. The national championship entry is $545, or $445 if you pay before the early date.</td><td>Ask the club how much sits inside the team fee and how much arrives later as a bill.</td></tr>
      <tr><td class="d">College camp</td><td>$125 to $425 for a day camp or team camp. Boarding camps run $1,500 to $5,400.</td><td>Pay for a day camp at a school that has already written to her. A $5,000 boarding camp is a vacation, not recruiting.</td></tr>
      <tr><td class="d">Video, do it yourself</td><td>$0 with free tools, or about $20 a month for a good editor.</td><td>Start here. Cut it yourself once so you know what is on the tape.</td></tr>
      <tr><td class="d">Video, one freelance edit</td><td>$150 to $250 for 10 to 20 clips. A game-by-game breakdown runs $50 to $95.</td><td>The best value in this book. Buy one edit, not a season package.</td></tr>
      <tr><td class="d">Video, full-service company</td><td>$250 to $2,459, by package.</td><td>Only when a coach has asked for more film than you can shoot yourself.</td></tr>
      <tr><td class="d">A recruiting service</td><td>The big names do not publish prices. Third-party reports say $250 to $2,100 a year, and others say up to $4,200.</td><td>Get any quote in writing and ask what they do that you cannot. Never pay a sign-up fee the week before a camp.</td></tr>
      <tr><td class="d">Eligibility Center</td><td>$120 on the live registration page today. The NCAA's own printed checklist still says $110. Trust the page where you pay.</td><td>The fee is waived for families who qualify for a test-fee waiver or free school lunch. Ask the counselor to file it at registration.</td></tr>
      <tr><td class="d">Unofficial visit weekend</td><td>$500 to $1,500 for two nights with travel, a room, and meals.</td><td>One target school per summer. A free visit is paid by you, so it costs whatever you decide it costs.</td></tr>
      <tr><td class="d">SAT or ACT</td><td>$68 and $70, plus small add-ons. Fee waivers are widely available.</td><td>Only if a college needs the score for admission or aid. The NCAA no longer requires a score to clear her.</td></tr>
    </tbody>
  </table>

  

  <h3>Free, and still the most useful</h3>
  <ul class="tight">
    <li>The Eligibility Center profile page costs nothing until a school asks her to register for certification.</li>
    <li>Every school's roster, schedule, and staff list is public on its own website.</li>
    <li>The recruiting calendar for her sport is one free PDF on ncaa.org.</li>
    <li>A counselor can check her credits against the NCAA list twice a year, for free, if you ask.</li>
  </ul>
</section>""")


A("""<section>
  <div class="pagehead"><span class="label">The Commit Book &middot; Girls' Basketball</span><span class="label">Year by year</span></div>
  <h2>9. Checklist by grade</h2>
  <p class="lead">One row per year. Cross items off. If a year slips, the fix is usually more schools and one more
  month, not more money.</p>
  <table>
    <thead><tr><th>Year</th><th>Do this</th></tr></thead>
    <tbody>
      <tr><td class="d">9th grade</td><td>Play the highest level she can handle. Keep every grade, including the subjects she is not good at. Start a folder for film dates and stats. Spend nothing on recruiting yet.</td></tr>
      <tr><td class="d">10th grade</td><td>Make the video once and make it good. Build the list of 40 to 55 schools across all five levels. Learn the calendar in Chapter 3. From 1 June after this year a coach may email and call, so send the first round that month.</td></tr>
      <tr><td class="d">11th grade</td><td>Four approved core courses a year keeps every door open. A 2.3 core GPA is the Division 1 floor and 2.2 is the Division 2 floor; a 3.0 keeps the early-qualifier option. Counselor checks every credit against the NCAA list. Register the free Eligibility Center page. Ask for paid visits from 1 January. Play on a certified summer team and film two games. Send grades in the fall.</td></tr>
      <tr><td class="d">12th grade, before Aug 1</td><td>Send one update with new film. Expect silence from 1 April through 31 July; that is the rule, not a signal. Make sure a full game sits behind the highlight reel.</td></tr>
      <tr><td class="d">12th grade, Aug to Nov</td><td>Ask each school for the written number and the date it arrives. Take the three visits that matter. Settle every question before the November window, then sign if the paper is right.</td></tr>
      <tr><td class="d">After signing</td><td>Do not let grades fall. Finish the 16 subjects and graduate. Send the final transcript the week the school asks for it.</td></tr>
    </tbody>
  </table>

  <h2 style="margin-top:6mm"></section>
<section>
<h2 style="margin-top:6mm">10. Ten ways families get this wrong</h2>
  <ol class="flow tight">
    <li><strong>They read "15 scholarships" and stop.</strong> At a school on the new rules, 15 is a roster of people, not 15 free rides. The coach decides how much of each seat is paid for.</li>
    <li><strong>They build a list of twelve schools.</strong> With transfers and players from abroad holding close to four of every ten Division 1 seats, twelve schools is one coaching change away from nothing.</li>
    <li><strong>They read silence as rejection.</strong> From 1 April to 31 July a women's staff may not call, text, or email. Send the update in March and go quiet with them.</li>
    <li><strong>They pay a club without asking about certification.</strong> If the event is not NCAA-approved, a Division 1 coach cannot legally watch it.</li>
    <li><strong>They send 500-word emails written by a parent.</strong> Coaches say it plainly: they want to hear from the player.</li>
    <li><strong>They send highlights with no full game.</strong> Forty made shots and no defense tells a coach you are hiding something. He will assume it is the truth.</li>
    <li><strong>They ask about money on the first call.</strong> Ask where she stands and what he still needs to see.</li>
    <li><strong>They skip Division 3.</strong> There are 416 programs with no athletic aid, which makes Division 3 the biggest door and the one most families never open.</li>
    <li><strong>They sign a junior-college letter to keep a spot warm.</strong> It binds a school year, and leaving takes paper signed by the school.</li>
    <li><strong>They plan the money backwards.</strong> The trip costs more than the camp. Budget travel first, then cut the $2,000 packages.</li>
  </ol>
</section>""")


A(open("wbb-sources.html", encoding="utf-8").read())
open("wbb-playbook-plain.html", "w", encoding="utf-8").write(HEAD + "\n".join(P) + "</body></html>\n")
print("wrote wbb-playbook-plain.html  %.1f KB, %d sections" % (len(HEAD + "".join(P)) / 1024.0, len(P)))
