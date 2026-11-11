# -*- coding: utf-8 -*-
"""Boys football playbook, plain-language edition. Reuses the W19 house CSS."""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HEAD = open("head.txt", encoding="utf-8").read().replace(
    "Basketball: The Whole Pathway", "Football: The Whole Pathway")
LOGO = open("mark.b64", encoding="utf-8").read().strip()
P = []
def A(x): P.append(x)

A("""<section class="cover">
  <div class="lockwrap"><img src="data:image/svg+xml;base64,""" + LOGO + """ alt="The Commit Book"></div>
  <div class="kicker label red">Football &middot; boys &middot; grades 9 to 12 &middot; sport playbook</div>
  <h1>Football:<br>The Whole Road to College</h1>
  <p class="sub">What to do, when to do it, who pays, and what a coach is and is not allowed to tell you. Built from the
  2026-27 NCAA Division I rule book, the printed football calendars for both subdivisions, and the NAIA and junior
  college rule books.</p>
  <div class="stamp">
    <div><span class="label k">Version</span><span class="small">2026-27 &middot; sample player: class of 2029</span></div>
    <div><span class="label k">Rules checked</span><span class="small">11 November 2026, against the rule text and both printed calendars</span></div>
    <div><span class="label k">Levels covered</span><span class="small">FBS &middot; FCS &middot; D2 &middot; D3 &middot; NAIA &middot; junior college</span></div>
  </div>
  <p class="edge">Football has more college seats than any other sport. More players chase them than in any other sport. than any other
  sport. This book starts with how many players a team may carry, because that number decides how many schools to write
  to, when to start, and how much to spend.</p>
  <h2 style="border-top-width:1.5px;margin-top:8mm">What is inside</h2>
  <ol class="contents">
    <li>Read this first</li>
    <li>How many players a team can take</li>
    <li>The plan by date, class of 2029</li>
    <li>What a coach may and may not do</li>
    <li>Camps, 7-on-7, combines, and visits</li>
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
  <div class="pagehead"><span class="label">The Commit Book &middot; Football</span><span class="label">Before you start</span></div>
  <h2>1. Read this first</h2>
  <p class="lead">Read Chapter 2 before you spend any money. Then put the plan in Chapter 3 on one page and cross items
  off. The rest is for reference: what the rules allow, what to send, what good video looks like, and what it costs.</p>

  <h3>The main idea</h3>
  <p>A family that knows the roster limit, the signing dates, and the video standard competes with families spending
  three times as much. Most of what a $5,000 service sells you is phone calls and follow-ups. The rules, the dates, and
  the right questions are free, and almost nobody writes them down.</p>

  <h3>What makes football different from basketball</h3>
  <p>A 12th grader can be met off campus in January of his junior year, a full two years before the first written
  offer. The sport has 670 college teams in the NCAA alone, and rosters of 105 players at the top level, so the seats
  exist. But 1.03 million boys play high-school football, so the same seat is chased by far more people than in any
  other sport. And the calendar moved: the day-by-day recruiting calendar is no longer printed in the rule book. The football committees approve it each year and the NCAA publishes it in July.</p>

  <h3>Three rules that surprise families</h3>
  <ul class="tight">
    <li>A coach may call, text, or email from 15 June after 10th grade (13.1.3.1). He may meet him off campus from
    1 January of 11th grade (13.1.1.1.6). But he may not put money in writing before 15 November of 12th grade
    (13.9.3.3). Talk is early. Paper is late.</li>
    <li>There is no limit on how many players a school may sign in a signing period. The only real limit is the roster
    cap. So a staff can sign 30 players in December and still owe none of them a spot in August.</li>
    <li>Once he signs, every other school must stop contacting him. That is a rule, not a courtesy, and it is why a
    family should never sign early just to feel settled.</li>
  </ul>

  <h3>Words this book uses</h3>
  <table>
    <thead><tr><th>Word</th><th>What it means here</th></tr></thead>
    <tbody>
      <tr><td class="d">FBS and FCS</td><td>The two Division 1 subdivisions. Bigger schools and TV games in the FBS, less total aid to go around and a real playoff in the FCS. The calendars are different, so always read yours.</td></tr>
      <tr><td class="d">Head-count</td><td>Each player on aid takes one whole seat, whatever the size of the grant. Division 1 football works this way.</td></tr>
      <tr><td class="d">Equivalency</td><td>How a school adds up partial aid. Thirty-six full grants, or seventy-two half grants, both equal 36.0. Division 2 works this way at 36.0, and the FCS at 63.0.</td></tr>
      <tr><td class="d">Counter</td><td>A player whose aid counts against the team limit.</td></tr>
      <tr><td class="d">Roster cap</td><td>The number of players a team may carry. At schools that signed the NCAA settlement (the deal that set the roster limits and ended the old letter-of-intent system), football is 105, and a walk-on now uses one of those seats.</td></tr>
      <tr><td class="d">Contact</td><td>In the rule book, contact means an in-person meeting. Calls, texts, and email are separate rules with separate dates.</td></tr>
      <tr><td class="d">Dead period</td><td>No visits and no in-person meetings. Calls and email are still allowed.</td></tr>
      <tr><td class="d">Unweighted GPA</td><td>Grades on a plain 4.0 scale, no bonus for hard classes. This is the number a coach can compare across states. Print it first.</td></tr>
      <tr><td class="d">Weighted GPA</td><td>The same grades with extra points for honors and Advanced Placement. Every school adds differently, on a 4.3, 5.0 or 6.0 scale, so the number is meaningless unless the scale is named next to it.</td></tr>
      <tr><td class="d">Core-course GPA</td><td>His grade point average in only the 16 school subjects the NCAA counts, computed by the NCAA on a 4.0 scale. Division 1 wants at least 2.3 and Division 2 at least 2.2. It is not his overall GPA, and a counselor has to certify which of his classes count.</td></tr>
      <tr><td class="d">Verified time</td><td>A number a third party took: the college's own camp, an electronic combine, or a documented laser session. Hand-timed is not verified, and runs about 0.2 seconds fast.</td></tr>
      
      <tr><td class="d">The portal</td><td>The system a college player uses to move schools. It is how most rosters get filled now, and it takes spots from high-school players.</td></tr>
    </tbody>
  </table>
</section>""")


A("""<section>
  <div class="pagehead"><span class="label">The Commit Book &middot; Football</span><span class="label">The numbers</span></div>
  <h2>2. How many players a team can take</h2>
  <p class="lead">This is the chapter that decides everything else. Every school has a limit on how many players it may
  carry, or how much aid it may hand out, or both. Multiply the limit by the number of schools and you know how many
  seats exist.</p>

  <table>
    <thead><tr><th>Level</th><th>What the rule caps</th><th>Teams that play this level</th><th>What that means for your list</th></tr></thead>
    <tbody>
      <tr><td class="d">FBS</td><td>105 players on the roster at the schools using the settlement rules (Bylaw 17.2, live since 1 July 2025), with aid of any size on any of them. Schools that stayed out of the settlement still work to 85 counters (15.5.6.1).</td><td>138 programs</td><td>The 105 cap is why rosters got smaller and why a walk-on now takes a seat that used to be free.</td></tr>
      <tr><td class="d">FCS</td><td>63.0 worth of aid, splittable, plus 85 counters at schools outside the settlement (15.5.6.2).</td><td>128 programs</td><td>Twenty-two unpaid players is the normal picture. A partial offer is the normal outcome.</td></tr>
      <tr><td class="d">NCAA Division 2</td><td>36.0 worth of aid per team. No national roster cap.</td><td>161 programs</td><td>Real money, spread thin. Expect a quarter or a half of one year's bill, and compare it against academic aid.</td></tr>
      <tr><td class="d">NCAA Division 3</td><td>No athletic aid at all (15.01.3). Aid comes from the normal financial aid office.</td><td>243 programs</td><td>The largest single group of football players in the country, and the one most families skip.</td></tr>
      <tr><td class="d">NAIA</td><td>24 full-grant equivalents per team, splittable. No limit on roster size.</td><td>96 programs</td><td>Genuine money at a lower cost of living. Read the school's own paper; see Chapter 7.</td></tr>
      <tr><td class="d">Junior college (NJCAA)</td><td>85 letters of intent per team. These are NJCAA divisions, not NCAA ones: NJCAA Division 2 schools pay tuition only; division 3 pays nothing.</td><td>59 teams</td><td>A one-year deal and a second start. The paper binds one year, not four.</td></tr>
    </tbody>
  </table>

  <h3>Who else is holding those seats</h3>
  <p>In January 2026 more than 10,500 college players entered the transfer portal, and the football spring window was
  gone, all in one 15-day stretch. The NCAA lifted the old cap on how many new players a school could sign in a year in 2023. That is why a staff with a new head coach can rebuild a roster from the portal in one winter. One program took 50
  transfers that month. There is no NCAA rule limiting how much of a football roster can arrive that way.</p>
  <p>That does not shut a high-school player out. It changes the competition: at many schools the seat he wants is being offered to a 21-year-old who is already college-ready, on and off the field.</p>

  <div class="box red">
    <h3>So how long should his list be?</h3>
    <p>Build the list around the schools he can really reach. For most players that means FCS, Division 2, Division 3,
    NAIA, and junior college, with the FBS as the bonus. A good starting list has all five levels on it:</p>
    <ul class="tight" style="margin-bottom:1.5mm">
      <li>8 to 12 FBS schools where he fits a position they need</li>
      <li>10 to 15 FCS and Division 2 schools</li>
      <li>10 to 15 Division 3 schools where his grades qualify and the aid fits your family</li>
      <li>5 to 10 NAIA schools</li>
      <li>3 to 5 junior college schools he would truly attend if the fall went badly</li>
    </ul>
    <p>Add those up and you have 40 to 55 schools. Football is the one sport where a player can be signed by 20
    programs and still be cut in August, so a long list is not a source of worry. It is arithmetic.</p>
  </div>

  <h3>What the odds really say</h3>
  <p>The NCAA's own math, published March 2026: 1,029,588 boys played high-school football in 2024-25 and 83,794
  played in the NCAA. That is 8.1% overall: 3.4% to Division 1, 2.1% to Division 2, and 2.6% to Division 3. Those
  figures leave out the NAIA and junior college, so the real chance of playing somewhere is better than the 8.1% figure.
  On aid, the NCAA's division-wide figures are 70% of Division 1 athletes and 77% in Division 2 receiving some athletic aid. And 80% of Division 3 athletes receiving help from the aid office. "Some aid" is the honest phrase: it often
  means part of tuition, not a free ride.</p>
</section>""")


A("""<section class="newpage">
  <div class="pagehead"><span class="label">The Commit Book &middot; Football</span><span class="label">Class of 2029</span></div>
  <h2>3. The plan by date, class of 2029</h2>
  <p class="lead">He graduates in 2029, so his sophomore year ends in June 2027 and his junior year starts in August
  2027. Print this page. The football recruiting calendar for 2028-29 does not exist yet. The committees approve it and the NCAA publishes it in July 2028. Dates marked PROJECTED come from the rule text, so treat them as one week early or one week late until the calendar lands.</p>

  <table class="flow">
    <thead><tr><th>Date</th><th>Kind</th><th>What happens</th><th>What to do that month</th></tr></thead>
    <tbody>
      <tr><td class="d">Now, in 10th grade</td><td><span class="tag t-hard">ACTION</span></td><td>Nothing is open yet, and that is the advantage.</td><td>Build the list of 40 to 55 schools. Get the video made once, properly. Send grades to every school on the list each semester.</td></tr>
      <tr><td class="d">Jun 2027</td><td><span class="tag t-opening">OPENING</span></td><td>Coaches may call, text, and email. Rule 13.1.3.1.</td><td>Send the first round of email that week, to the position coach, not the head coach.</td></tr>
      <tr><td class="d">Jul 2027</td><td><span class="tag t-hard">ACTION</span></td><td>Camp season. Coaches watch camps to look at players already on their list.</td><td>Go to the camp only where a coach has answered your email. Ask, in writing, who will be evaluating.</td></tr>
      <tr><td class="d">Sep 2027</td><td><span class="tag t-hard">HARD</span></td><td>11th grade starts. The 16 core subjects and the core GPA start to matter for real (14.3.1.1).</td><td>Ask the counselor to check every credit against the NCAA list. Fix a bad schedule now, not in January.</td></tr>
      <tr><td class="d">Jan 2028</td><td><span class="tag t-opening">OPENING</span></td><td>A coach may meet him off campus for the first time. Rule 13.1.1.1.6. The current FBS calendar still puts a quiet spell over early January.</td><td>Take the meetings. Bring the one-page sheet. Ask about the position, the plan, and the number.</td></tr>
      <tr><td class="d">Apr 1 to Jun 25, 2028</td><td><span class="tag t-opening">OPENING</span></td><td>Paid visits are allowed in this window for football (13.6.2.1.7). Each school pays for one visit per player.</td><td>Ask for the paid visit by email and name the dates you can travel. Use this window before the summer camps eat the calendar.</td></tr>
      <tr><td class="d">Jun 28 to Aug 31, 2028</td><td><span class="tag t-hard">HARD</span></td><td>On the current FBS calendar this is a dead period: no visits and no in-person contact at all. Calls and email are still allowed.</td><td>Send one update with new film and grades. Do not read the silence as rejection.</td></tr>
      <tr class="sub"><td colspan="4">Senior year begins</td></tr>
      <tr><td class="d">Sep 1 to Nov 28, 2028</td><td><span class="tag t-opening">OPENING</span></td><td>In the FBS this is an evaluation period: coaches may watch, but may not speak to him in person, and get one look per player, against a staff limit of 33 evaluation days for the season. In the FCS the same weeks are now a contact period.</td><td>Play every game on one camera, from a high wide angle. Tell each coach the schedule. This is the month he is actually seen.</td></tr>
      <tr><td class="d">Nov 15, 2028</td><td><span class="tag t-opening">OPENING</span></td><td>Written aid offers may go out. Rule 13.9.3.3.</td><td>Ask each coach one question: what does the written offer say, and when does it arrive?</td></tr>
      <tr><td class="d">29 Nov to 1 Dec 2028 <span class="tag t-projected">PROJECTED</span></td><td><span class="tag t-hard">HARD</span></td><td>Early signing period for football: the Wednesday before the first Saturday in December (13.02.13.1). In 2026 those dates are 2 to 4 December. That is how we know the rule works this way.</td><td>Have every number and every question settled before that week. Ask for the paper in October, not December.</td></tr>
      <tr><td class="d">Jan 2029</td><td><span class="tag t-hard">HARD</span></td><td>The transfer portal opens for about ten days, and rosters move again.</td><td>Ask where he stands if the staff loses players to the portal. A roster seat can change hands in that week.</td></tr>
      <tr><td class="d">Feb 2029</td><td><span class="tag t-opening">OPENING</span></td><td>Junior college letters of intent: the recent NJCAA date for fall football is 3 February.</td><td>If junior college is a real option, sign there and keep the NCAA list alive at the same time.</td></tr>
      <tr><td class="d">7 Feb 2029 <span class="tag t-projected">PROJECTED</span></td><td><span class="tag t-opening">OPENING</span></td><td>Regular signing period opens, the first Wednesday in February (13.02.13.1). Families who did not sign in December sign here.</td><td>Do not plan on this date as a backup. The good seats are gone by then, and the school sets the closing date.</td></tr>
      <tr><td class="d">Apr to Jun 2029</td><td><span class="tag t-hard">HARD</span></td><td>Academic finish: the 16 subjects, the core GPA, the diploma, and the final certification (14.3.1.3).</td><td>Do not let grades fall in the spring. A coach cannot put on a roster a player the NCAA will not clear.</td></tr>
    </tbody>
  </table>

  <div class="box">
    <h3>Cost if you miss it</h3>
    <p>Miss the autumn film window and no coach has seen him play against real competition. Miss the paid-visit window
    and you pay for the trip yourself, which stops most families at four schools instead of twelve. Miss the December
    week and he signs in February, into a smaller set of seats. Miss the academic finish and a signed offer can be put
    on hold while the Eligibility Center sorts it out.</p>
  </div>
</section>""")


A("""<section>
  <div class="pagehead"><span class="label">The Commit Book &middot; Football</span><span class="label">The rules that protect you</span></div>
  <h2>4. What a coach may and may not do</h2>
  <p class="lead">These rules exist to keep a staff from wearing a 15-year-old down. They also explain behavior that
  families read as rude. A coach who has not called since June has probably not changed his mind. He has hit a rule.</p>

  <h3>The four kinds of period, and what each one allows</h3>
  <table>
    <thead><tr><th>Period</th><th>In-person meetings</th><th>Visits</th><th>Calls, text, email</th></tr></thead>
    <tbody>
      <tr><td class="d">Contact</td><td>Allowed, on or off campus</td><td>Allowed</td><td>Allowed</td></tr>
      <tr><td class="d">Evaluation</td><td>Watch only, off campus, no talking to him</td><td>Allowed</td><td>Allowed</td></tr>
      <tr><td class="d">Quiet</td><td>On campus only</td><td>Allowed</td><td>Allowed</td></tr>
      <tr><td class="d">Dead</td><td>Not allowed</td><td>Not allowed</td><td>Still allowed</td></tr>
    </tbody>
  </table>
  <p>The 2026-27 FBS calendar, for reference: quiet in early January, contact for about half of January, dead in
  February, quiet in early March, contact in the spring, dead over the transfer window, dead again across most of the
  summer, then an evaluation period from 1 September to 28 November and dead from the end of November. The FCS calendar
  is the same pattern, except the autumn weeks are a contact period instead of an evaluation period. That one difference changes what a visit can look like in October, so read your own subdivision's PDF and nothing else.</p>

  <h3>Three limits on how hard a staff may push</h3>
  <ul class="tight">
    <li><strong>One look per player.</strong> During the autumn evaluation period a staff may evaluate each player once. The whole FBS staff gets 33 evaluation days for the season, rising to 50 days in 2027 (13.1.7.4). That is
    why a film link beats a second visit to the same stadium.</li>
    <li><strong>No written money before 15 November of 12th grade</strong> (13.9.3.3), and no signable paper before the
    December window (13.9.3.2). Every number you hear before that is spoken, not written. Coaches know this. The right
    move is not to push harder but to ask for a date: "When will that be in writing?"</li>
    <li><strong>After he signs, the other schools must go quiet</strong> (13.1.1.2). The rule ends his recruiting,
    which is why the paper itself, not the smile, is the thing to study.</li>
  </ul>

  <h3>What your family must not do</h3>
  <ul class="tight">
    <li>Do not announce a school on social media before the written offer exists. A public post reads like a promise to
    a staff, and it can end his other options without making anyone sign anything.</li>
    <li>Do not miss a course in the senior spring. Final certification happens after graduation and the diploma is part
    of it (14.3.1.3).</li>
    <li>Do not sign a junior-college letter to hold a place without asking how the release works. See Chapter 7.</li>
  </ul>

  <div class="box">
    <h3>Where these dates live now</h3>
    <p>In October 2026 the NCAA moved the day-by-day sport calendars out of the rule book. The rule book now says to
    look at the calendars published on ncaa.org, and in football they are approved by the FBS and FCS oversight
    committees, then printed each July. That is why an older guide, a school's own web page, or a service's handout can
    be wrong about a specific week, and why Chapter 3 marks the 2028-29 dates as PROJECTED.</p>
  </div>
</section>""")


A("""<section>
  <div class="pagehead"><span class="label">The Commit Book &middot; Football</span><span class="label">Exposure</span></div>
  <h2>5. Camps, 7-on-7, combines, and visits</h2>
  <p class="lead">Families spend more money here than anywhere else in football, and this is where the honest answers
  matter. Coaches have said, in public and by name, what each of these events is worth to them.</p>

  <h3>What coaches actually say</h3>
  <table class="flow">
    <thead><tr><th>Event</th><th>What a named coach has said</th><th>So what should you pay for</th></tr></thead>
    <tbody>
      <tr><td class="d">7-on-7</td><td>David Shaw, then Stanford head coach: it "means absolutely nothing to me as an evaluator," and he has never watched 7-on-7 film. Brian Strandley, Eastern Washington: asked if it helps in recruiting, "It's not. It's not at all." Chris Fore, recruiting coordinator: 7-on-7 film and stats "mean nothing to college coaches."</td><td>Play it for reps and for team chemistry. Do not pay for a national 7-on-7 circuit expecting recruiting credit.</td></tr>
      <tr><td class="d">Combines</td><td>A verified 40-yard dash time and measured height and weight let a staff check what you claim. Coaches are rarely there, and one coach quoted in Bleacher Report called it delusional to think combines get you offered.</td><td>One combine, for honest numbers to put on the one-page sheet. Not four.</td></tr>
      <tr><td class="d">College camps</td><td>Dan Mullen, then Mississippi State: "The satellite camps, they're recruiting camps ... we've probably had 1,000 kids on campus in camps and there's probably a couple guys who will be SEC players out of that group." NCSA tells parents most staffs attend their own camps to look at players already on their list.</td><td>Go when a coach has answered your email and said, in writing, that he will watch you.</td></tr>
      <tr><td class="d">All-star games</td><td>We found no named college coach on what high-school all-star games are worth. One real fact: NFL scouts may not attend a game where players paid to play.</td><td>Go if you are invited and it is free or nearly free. Do not buy a seat.</td></tr>
      <tr><td class="d">Paid services</td><td>James Franklin, Penn State, on paid recruiting services: "They go right in the trash." Chris Creighton, Eastern Michigan: "you don't have to go through an outside agency for us to see the film."</td><td>Buy help with film or with a schedule. Buy e-mail sent in your son's name.</td></tr>
    </tbody>
  </table>

  <h3>Visits: what is free, and what is not</h3>
  <ul class="tight">
    <li><strong>Paid visit.</strong> Allowed from 1 April of 11th grade through the Sunday before the last Wednesday in
    June (13.6.2.1.7), then again from 1 September of 12th grade. There is also a window around the school's own home
    game in August, 48 hours either side.</li>
    <li><strong>One per school.</strong> Each school may pay for one visit before 15 October after graduation and one
    after (13.6.2.2). A school that hires a new head coach may offer one more (13.6.2.2.1). The old cap on how many
    paid visits a program could hand out in a year was removed in April 2026, so asking costs nothing.</li>
    <li><strong>Free visit.</strong> His family pays, at any time, subject to the calendar. No limit on the number.</li>
    <li><strong>Free tickets.</strong> Up to three, inside 30 miles of campus, general seating, and none during a dead
    period (13.7.3.1).</li>
  </ul>
  <p>Family travel is never free. A weekend of two nights runs about $500 to $1,500 with gas or airfare, a room, and
  meals. Plan one target school per trip, and stack a second school in the same state.</p>

  <h3>Ask for these four things on a visit</h3>
  <ol class="tight">
    <li>Time with the position coach, not only the head coach.</li>
    <li>A look at the academic support office, and what it does for players who miss class to travel.</li>
    <li>A plain answer on what he would be asked to do in year one, and who is ahead of him on the depth chart.</li>
    <li>What happens to his aid if he is hurt, and who decides. The answer is in Chapter 7.</li>
  </ol>
</section>""")


A("""<section>
  <div class="pagehead"><span class="label">The Commit Book &middot; Football</span><span class="label">Film and outreach</span></div>
  <h2>6. What to send, and what good video looks like</h2>
  <p class="lead">Only about one in three Division 1 coaches watches all of the film that is sent to them. A staff
  decides in about two minutes, and Nebraska's player-personnel director says the first 30 to 60 seconds decide
  whether he plays the rest. So the tape goes short, and it goes best-first.</p>

  <h3>The video, for every position</h3>
  <ul class="tight">
    <li><strong>Best plays first.</strong> Ryan Gunderson, Nebraska director of player personnel: "Always put your best
    stuff first ... if that doesn't impress them right away, they're not going to turn your film back on."</li>
    <li><strong>Three to five minutes, no more.</strong> Roughly 25 plays. No music, no sound effects, no slow motion,
    no sped-up clips.</li>
    <li><strong>Shot high and wide.</strong> From a press-box angle that shows all 22 players. Line coaches need to see
    alignment and footwork, so a tight end-zone cut of the ten linemen is worth paying for.</li>
    <li><strong>Mark him on every play.</strong> Start each clip a couple of seconds before the snap, with an arrow or
    a shadow. If a coach spends five seconds looking for him, he stops watching.</li>
    <li><strong>Full games ready.</strong> A staff will ask for a full game, case by case. Film the whole season on one
    camera and cut the reel from it. Do not edit mistakes out; a coach who finds them later stops trusting the tape.</li>
  </ul>

  <h3>By position, what a staff is looking for</h3>
  <table>
    <thead><tr><th>Position</th><th>Put this on the tape</th></tr></thead>
    <tbody>
      <tr><td class="d">Quarterback</td><td>A short skills video, 2 to 4 minutes, with 2 or 3 reps per drill: moving in the pocket, throwing on a platform, throwing every route, and throws to all fields. Accuracy and repetition matter more than one deep ball.</td></tr>
      <tr><td class="d">Wide back, receiver</td><td>Route running and hands, plus blocking. A back who only shows runs, and never blocks, looks like a high-school player. Show catches, then show the block on the next play.</td></tr>
      <tr><td class="d">Line</td><td>Use of hands, first-step punch, change of direction, and leg drive. Bag work, then live snaps. Show the kick slide, which line coaches call the most important drill.</td></tr>
      <tr><td class="d">Linebacker</td><td>Stance, first step, run defense versus pass coverage, and space in the open field. Show him reading the play before he moves, not only hitting. Add one drop into a zone.</td></tr>
    </tbody>
  </table>

  <h3>The email</h3>
  <p>Write the subject line as a label, not a greeting: class year, position, name, size, one
  number worth asking about, school, state. Stay near 70 letters, because a phone cuts the rest
  off. Send it from the player's own address, not a parent's. A coach at a big school reads these
  by the dozen in January: one FBS recruiting coordinator said he went through 75 emails a night,
  and he said he screens on size and speed before he reads a word. So the email has one job. It
  answers his first five questions without a reply, then it stops. Keep the body near 180 words, which is what fits one phone screen. The sample below is 182.</p>
  <div class="tmpl">Subject: 2029 MIKE LB Danny Whitfield, 6'0" 185, 4.94, Anytown South HS, WI

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

</div>
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


  <h3>The one page that goes with it</h3>
  <p>Everything a staff needs to fill its sheet, in the order the staff asks for it: name, class year, the exact position he plays and his number; school, city, state and conference; height and weight with the date and who measured; any timed number with its method, event and date; last season's line with games played; GPA with its scale, plus where he stands on the 16 core courses; one real reason this school; two links, highlights first and one full game second; both his coaches' names and phone numbers; his own phone and email, with the parent line labelled. A survey of college coaches found they were about 50% more likely to watch film when it went to the right coach and when a transcript came with it. Every field you leave out is a question he has to answer before he watches.</p>

  <h3>How to follow up, and how to ask</h3>
  <ul class="tight">
    <li>Wait one to three business days, then call the number on the staff page and ask for the coach who covers his
    position and his state. Every number is published; you do not need a service to get one.</li>
    <li>Ask two questions: where do I stand on your list, and what do you still need to see. Do not ask about a
    scholarship on the first call.</li>
    <li>If a coach gives a cell number, ask before texting. Text between 8 in the morning and 9 at night in the
    coach's time zone, and sign your full name. Persistent is good; five texts is not.</li>
    <li>Send an update every six to eight weeks with one new fact in it: new film, a new number, a new award, a
    schedule change.</li>
  </ul>
</section>""")


A("""<section>
  <div class="pagehead"><span class="label">The Commit Book &middot; Football</span><span class="label">The paperwork</span></div>
  <h2>7. What the paperwork really means</h2>
  <p class="lead">There is exactly one moment when a promise becomes a deal: the day a paper is signed. Everything
  before that is talk, and a coach is allowed to talk. Here is each document, and what it does.</p>

  <table class="flow">
    <thead><tr><th>Document</th><th>When it may be signed</th><th>What it does</th></tr></thead>
    <tbody>
      <tr><td class="d">Verbal commitment</td><td>Any time, by phone or text</td><td>Nothing. It binds neither family nor school. It only tells the other coaches to stop calling.</td></tr>
      <tr><td class="d">Written offer of aid</td><td>Football: on or after 15 November of 12th grade (13.9.3.3)</td><td>States the number. He still cannot accept it until the signing window opens.</td></tr>
      <tr><td class="d">Athletics aid agreement</td><td>Early: 2 to 4 Dec 2026 pattern, so 29 Nov to 1 Dec 2028 PROJECTED. Regular: the first Wednesday in February. The FCS and FBS use the same dates.</td><td>The real deal. Once he signs, the other schools must stop recruiting him.</td></tr>
      <tr><td class="d">Division 2 award letter</td><td>From the sport's signing date. There is no early window for football in Division 2.</td><td>Binds one year of aid on written terms. Renewal is not automatic, even when a coach says four years.</td></tr>
      <tr><td class="d">Division 3 aid package</td><td>Ordinary admissions calendar</td><td>Admission plus a roster spot plus regular aid. Letters of intent are banned in Division 3 (13.9.1).</td></tr>
      <tr><td class="d">NAIA school letter</td><td>School policy</td><td>The NAIA runs no national letter program and says it will not enforce one against either side. The school's own paper may or may not bind.</td></tr>
      <tr><td class="d">Junior college letter of intent</td><td>Recent NJCAA date for fall football: 3 February</td><td>Binds one school year, August to July. A parent signs too if he is under 18, and leaving takes a written release.</td></tr>
    </tbody>
  </table>

  <h3>What the settlement changed, in one paragraph</h3>
  <p>The National Letter of Intent no longer exists. The NCAA ended it in October 2024, in Division 1 and Division 2,
  and the website that ran it has shut down. Written offers of aid replaced it, and the old signing-date formula was
  kept and applied to the new paper. Nothing else in this process is enforceable. A coach who says "we have a spot for
  you" in June of junior year is allowed to say it, and wrong to hold you to it.</p>

  <h3>The protections you do have</h3>
  <ul class="tight">
    <li>Aid cannot be cut during the year of the award because of a coach's opinion of his play, or because of an
    injury or illness. There are six listed reasons and he gets a hearing first (15.3.4.1, 15.3.4.2).</li>
    <li>The NCAA said plainly that a player who loses a roster spot for roster management, for performance, or because
    of injury keeps his aid unless he chooses to leave.</li>
    <li>After he signs, other schools may not contact him, which protects him from a bidding war he cannot win.</li>
  </ul>

  <div class="box red">
    <h3>The preferred walk-on, honestly</h3>
    <p>The NCAA's own student guide says it this way: a preferred walk-on is a coach who wants you on the team but has
    no scholarship for you, and you are guaranteed a place on the roster. That is a real compliment and a real roster
    seat. It is also not money. We searched the whole 412-page Division 1 rule book: the phrase "preferred walk-on"
    appears zero times, so no rule backs the promise. Treat it as an offer that pays nothing, and ask what it
    becomes in year two. He still has to register with the Eligibility Center and clear the same academic rules as a
    scholarship player.</p>
  </div>

  <div class="box">
    <h3>Four questions to ask about any paper you are sent</h3>
    <ol class="tight" style="margin-bottom:0">
      <li>Who has to sign this on the school's side for it to be valid?</li>
      <li>What exactly does it cover: tuition, fees, books, room, food?</li>
      <li>How long does it last, and what has to happen for it to be renewed?</li>
      <li>If he transfers or is hurt, what happens to the money, and who decides?</li>
    </ol>
  </div>
</section>""")


A("""<section>
  <div class="pagehead"><span class="label">The Commit Book &middot; Football</span><span class="label">Money</span></div>
  <h2>8. What it costs, and what is wasted</h2>
  <p class="lead">These are published prices, checked 11 November 2026. Where the seller is also the advertiser, the
  line says so. A family that plans on $3,000 to $6,000 a year and skips the packages can finish this whole process
  with money left over.</p>

  <div class="box">
    <h3>The whole-year number</h3>
    <p>One of the largest services in the market says a recruiting family spends $3,000 to $10,000 a year, and
    $15,000 to $50,000 across high school. That is a vendor figure, so read it as the top of an honest range. One
    father quoted $40,000 spent on a quarterback's camps, combines, and unofficial trips; that is the ceiling of a real
    case, not the plan. The national sports survey puts average family spend on a single child at about $1,500 a year,
    and $634 for tackle football, which is what the sport costs when nobody is selling you exposure.</p>
  </div>
<table class="flow">
    <thead><tr><th>What you buy</th><th>Real price</th><th>Buy it or skip it</th></tr></thead>
    <tbody>
      <tr><td class="d">College camp, one day</td><td>$49 to $125 at the schools we checked, from a small-school prospect camp to an FBS specialist camp. A multi-day camp with room and board runs $400 to $800 before travel.</td><td>Pay when the coach has answered your email and said he will watch him. Otherwise it is a jersey and a bus ride.</td></tr>
      <tr><td class="d">7-on-7 entry</td><td>$200 to $530 per team, or $20 to $34 per player where it is priced that way. Families pay travel, not entry.</td><td>Play if the high-school team goes. Do not build a summer around it.</td></tr>
      <tr><td class="d">Combine</td><td>$49 to $299.</td><td>One, for honest numbers on the one-page sheet.</td></tr>
      <tr><td class="d">Showcase</td><td>$96 to $399 per event, and about $1,950 for a full package with games.</td><td>Pay when the list of attending staffs is published. Skip the open ones.</td></tr>
      <tr><td class="d">All-star game</td><td>$0 at the good ones, and up to $425 at others. Some take a refundable deposit.</td><td>Go when invited. NFL scouts may not attend a game where players paid to play.</td></tr>
      <tr><td class="d">Video, do it yourself</td><td>$0 with free tools, or about $20 a month for a good editor.</td><td>Film the season yourself, from a high wide angle. That single habit replaces most of what a service sells.</td></tr>
      <tr><td class="d">Video, one freelance edit</td><td>$150 to $538 per reel. Most jobs land between $150 and $250.</td><td>Buy one edit, not a season package.</td></tr>
      <tr><td class="d">Video, full-service company</td><td>$250 to $2,459 by package. Having someone else pick the plays from your game film runs $450 to $700 per game.</td><td>Only when a coach has asked for more film than you can cut. A $50 to $95 per-game breakdown does the same job.</td></tr>
      <tr><td class="d">A recruiting service</td><td>The big names do not publish prices. Third-party reports say $250 to $2,100 a year, and others say up to $4,200.</td><td>Get the quote in writing and ask what, exactly, they do that a parent with a calendar cannot.</td></tr>
      <tr><td class="d">Eligibility Center</td><td>$120 on the live registration page today; the NCAA's printed checklist still says $110. Trust the page where you pay.</td><td>Free if the family qualifies for a test-fee waiver or free school lunch. Ask the counselor to file it at registration.</td></tr>
      <tr><td class="d">Visit weekend</td><td>$500 to $1,500 for two nights with travel, a room, and meals.</td><td>One target school per trip. Stack a second school in the same state.</td></tr>
      <tr><td class="d">SAT or ACT</td><td>$68 and $70, plus small add-ons. Fee waivers are widely available.</td><td>Only if the college needs the score for admission or aid. The NCAA no longer requires one to clear him.</td></tr>
    </tbody>
  </table>

  

  <h3>Free, and still the most useful</h3>
  <ul class="tight">
    <li>The Eligibility Center profile page costs nothing until a school asks him to register for certification.</li>
    <li>Every school's depth chart, schedule, and staff list is public on its own website, including every office phone number.</li>
    <li>The recruiting calendar for his subdivision is one free PDF on ncaa.org.</li>
    <li>A counselor can check his credits against the NCAA list twice a year, for free, if you ask.</li>
  </ul>
</section>""")


A("""<section>
  <div class="pagehead"><span class="label">The Commit Book &middot; Football</span><span class="label">Year by year</span></div>
  <h2>9. Checklist by grade</h2>
  <p class="lead">One row per year. Cross items off. If a year slips, the fix is usually more schools and one more
  month, not more money.</p>
  <table>
    <thead><tr><th>Year</th><th>Do this</th></tr></thead>
    <tbody>
      <tr><td class="d">9th grade</td><td>Get on the field, any unit. Lift with a plan you can write down. Keep every grade. Start one folder for film, one for stats, and one for every email a coach sends. Spend nothing on recruiting.</td></tr>
      <tr><td class="d">10th grade</td><td>Film the whole season from a high wide angle. Build the list of 40 to 55 schools across all five levels. Learn the calendar in Chapter 3. On 15 June after this year, send the first email round.</td></tr>
      <tr><td class="d">11th grade</td><td>Four approved core courses a year keeps every door open. A 2.3 core GPA is the Division 1 floor and 2.2 is the Division 2 floor; a 3.0 keeps the early-qualifier option. Counselor checks every credit against the NCAA list. Register the free Eligibility Center page. Ask for a paid visit inside the April window. Go to one camp at a school that has answered you. Send grades in the fall.</td></tr>
      <tr><td class="d">12th grade, before Sep 1</td><td>Send one update with new film. Expect the summer silence on the FBS calendar. Make sure full games sit behind the reel, and get measured numbers at one combine.</td></tr>
      <tr><td class="d">12th grade, Sep to Nov</td><td>Play. Send the schedule to every coach on the list. On 15 November the written offer becomes possible, so ask for the number and the date in the same email.</td></tr>
      <tr><td class="d">12th grade, December</td><td>Settle every question before the early signing week, then sign if the paper is right. If it is not right, do not sign to feel settled.</td></tr>
      <tr><td class="d">After signing</td><td>Do not let grades fall. Finish the 16 subjects and graduate. Send the final transcript the week the school asks for it.</td></tr>
    </tbody>
  </table>

  <h2 style="margin-top:6mm"></section>
<section>
<h2 style="margin-top:6mm">10. Ten ways families get football wrong</h2>
  <ol class="flow tight">
    <li><strong>They think 85 is the number that matters.</strong> At a school on the new rules the number is 105 seats, and aid of any size can sit on any of them. The scarce thing is a seat, not a scholarship.</li>
    <li><strong>They read one guide and stop.</strong> The calendar moved out of the rule book in October 2026 and is re-ratified each July, and the FCS and FBS calendars are different. A 2024 handout is wrong about a week, and a July evaluation period no longer exists.</li>
    <li><strong>They pay for 7-on-7 and expect credit for it.</strong> Three coaches on the record, including a former Stanford head coach, say the film and the stats mean nothing to them.</li>
    <li><strong>They pay for a camp before anyone has answered an email.</strong> A staff's own camp is full of players already on its list.</li>
    <li><strong>They build a list of twelve schools.</strong> About 10,500 players moved through the portal in one winter, and no rule limits how many seats a school may fill that way.</li>
    <li><strong>They take the parent email as the plan.</strong> Coaches say they want to hear from the player first.</li>
    <li><strong>They skip Division 3 and NAIA.</strong> Division 3 alone is 243 football programs. Families who only chase a scholarship leave the biggest door closed.</li>
    <li><strong>They sign a junior-college letter to hold a place.</strong> It binds a school year, and getting out takes a release signed by that school.</li>
    <li><strong>They ask "can he get in on academic aid" at the visit and not on the phone.</strong> The answer changes the number on the paper.</li>
    <li><strong>They plan the money backwards.</strong> Travel is the big line, not the camp fee. Budget four trips and skip the $2,000 packages.</li>
  </ol>
</section>""")


A(open("fb-sources.html", encoding="utf-8").read())
open("fb-playbook-plain.html", "w", encoding="utf-8").write(HEAD + "\n".join(P) + "</body></html>\n")
print("wrote fb-playbook-plain.html  %.1f KB, %d sections" % (len(HEAD + "".join(P)) / 1024.0, len(P)))
import sys; sys.path.insert(0, ".")
from readability import audit
audit("fb-playbook-plain.html", "BOYS FOOTBALL plain edition, before the proofreader")
