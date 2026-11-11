# -*- coding: utf-8 -*-
"""W19: the same playbook, written for an eighth-grade reader.

Design and brand are unchanged: this reuses the CSS and logo from W18 and only
replaces the prose. Sentences are short, jargon is explained the first time it
appears, spelling is US, and no idiom is left unexplained. Facts, dates and
figures are the same as the research packet.
"""
import base64, pathlib, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = pathlib.Path(r"C:\Users\Jloeh\Developer\recruiting-calendar")
SRC = (REPO / "v3" / "W18-bball-pdf" / "basketball-playbook.html").read_text(encoding="utf-8")
HEAD = SRC.split("<body>", 1)[0]   # doctype + fonts + CSS only
mark = (REPO / "site/assets/logo/mark-light.svg").read_text(encoding="utf-8")
lockup = (REPO / "site/assets/logo/lockup-stacked-light.svg").read_text(encoding="utf-8")
mark64 = base64.b64encode(mark.encode("utf-8")).decode()
lock64 = base64.b64encode(lockup.encode("utf-8")).decode()
png64 = base64.b64encode((REPO / "site/assets/logo/favicon-256.png").read_bytes()).decode()
(OUT := REPO / "v3" / "W19-plain").mkdir(parents=True, exist_ok=True)
(OUT / "mark.b64").write_text(mark64, encoding="utf-8")

# date, what happens, who does it, how you know it is done, tag
PLAN = [
 ("15 Oct 2026", "Sit with the school counselor. Check every class your child has taken and plans to take against the school's list of NCAA-approved classes. Not every good class counts.",
  "Parent, with the counselor", "You both have a printed copy of the class list, marked up and signed", "DO IT"),
 ("15 Jun 2027", "First day a Division I men's basketball coach may contact you. Before this day a coach may watch and rate you. From this day the coach may email, text, call, or send you a form. The rule is on the coach, not on you.",
  "Athlete", "You have 40 to 60 schools on your list, and you have filled out the sports form on each school's website", "OPENS"),
 ("1 Aug 2027", "Paid campus visits become allowed. Check the printed rule book for the exact day for boys and for girls. The dates we found did not match, so look it up before you book travel.",
  "Parent", "Your visit plan is written down, with your top three schools in order and your questions ready", "OPENS"),
 ("1 Jul 2028", "No self-paid visits in July. In Division I, your child may not visit a campus during July. The one exception: your child already signed a written offer of aid, or paid a deposit to the school.",
  "Parent", "July trips move to August, or you paid the deposit on purpose", "HARD"),
 ("1 Jun 2028", "Before you pay for a summer team, ask the team what events are NCAA-certified. A Division I coach may only watch players at events on the NCAA's approved list. Ask in writing, and keep the answer.",
  "Parent", "You wrote down the name of the league and whether it is certified", "DO IT"),
 ("30 Sep 2028", "Highlight video is finished. It runs under four minutes, shows defense, and marks your child in every clip. Send a link, not a file. Keep two full games ready.",
  "Athlete", "One link that works, one full-game link that works, and no password needed", "DO IT"),
 ("8 Nov 2028", "Early signing period opens (worked out from the rule, not yet printed by the NCAA). If your child signs here, the schools that offered aid must stop contacting you. Do not sign just to please a friendly coach.",
  "Athlete", "The choice is made before the window opens, not during it", "PROJECTED"),
 ("15 Nov 2028", "Early signing period closes. A few days around this week are usually a dead period, a stretch when coaches may not talk to you in person. Missing this week costs nothing in basketball. April is a real second chance to sign.",
  "Athlete", "You signed the paper, or you chose to wait for April on purpose", "PROJECTED"),
 ("1 Dec 2028", "College teams must hand in their roster lists by this day, or the day before their first real game. After that, a spot opens only if a player leaves or gets hurt.",
  "Athlete", "A January email with new video goes to every school that still has room", "HARD"),
 ("24 Dec 2028", "Dead period, December 24 to 26, every year. No visits, no contact, no ratings. It falls in the holidays on purpose.",
  "Parent", "You checked the visit dates against the rule book before you booked anything", "HARD"),
 ("1 Apr 2029", "Ask for the final amateurism check. This is the NCAA's last review of your child's grades and classes. You may ask starting April 1 of senior year for a fall start. The school cannot play your child until the file is done.",
  "Both", "The account shows the word CERTIFIED", "DO IT"),
 ("11 Apr 2029", "The regular signing period opens (worked out from the rule). In basketball this period closes on each school's own date, not on one national date. Basketball has no late signing period.",
  "Athlete", "You signed, or you have a written reason why the school is not signing", "PROJECTED"),
 ("15 Jun 2029", "The final high school transcript, with proof of graduation, must reach the NCAA Eligibility Center. The counselor sends it.",
  "Parent, with the counselor", "The account shows the transcript was received", "HARD"),
 ("1 Nov 2029", "If you chose the junior college route: this is the day you sign the junior college letter of intent. It holds your child for one school year. It stops your child from signing with any other junior college. A four-year school is still open to you.",
  "Athlete", "One letter signed, or none, and you chose which", "WINDOW"),
]
plan_html = "\n".join(
    "<tr><td class='d'>%s</td><td class='w'>%s</td><td class='o'>%s</td><td class='n'>%s</td></tr>"
    % (d, what, who, done) +
    "<tr class='sub'><td></td><td colspan='3'><span class='tag t-%s'>%s</span></td></tr>"
    % (tag.lower().replace(" ", ""), tag)
    for d, what, who, done, tag in PLAN)

BODY = f"""
<body>

<section class="cover">
  <div class="lockwrap"><img src="data:image/svg+xml;base64,{lock64}" alt="The Commit Book"></div>
  <div class="kicker label red">Basketball &middot; boys and girls &middot; grades 9 to 12 &middot; sport playbook</div>
  <h1>Basketball:<br>The Whole Road to College</h1>
  <p class="sub">What to do, when to do it, who pays, and what a coach is and is not allowed to tell you. Based on the
  2026-27 NCAA Division I rule book, the printed sport calendar, and the NAIA and junior college rule books.</p>

  <div class="stamp">
    <div><span class="label k">Version</span><span class="small">2026-27 &middot; sample player: class of 2029</span></div>
    <div><span class="label k">Rules checked</span><span class="small">10 November 2026, against the rule text and the current calendar</span></div>
    <div><span class="label k">Levels covered</span><span class="small">NCAA D1 &middot; D2 &middot; D3 &middot; NAIA &middot; junior college</span></div>
  </div>

  <p class="edge">This is not a list of camps and team showcases. It starts with how many players a team can carry, because
  that number decides how many schools to write to, when to start, and how much to spend.</p>

  <h2 style="border-top-width:1.5px;margin-top:8mm">What is inside</h2>
  <ol class="contents">
    <li>How many players a team can take</li>
    <li>The plan by date, class of 2029</li>
    <li>What the school is really offering</li>
    <li>What to send, and when</li>
    <li>Summer teams, visits, and the July rule</li>
    <li>What it costs, and what is wasted</li>
    <li>Checklist by grade</li>
    <li>Sources, and what we could not settle</li>
  </ol>

  <p class="small" style="margin-top:6mm">This is education. It is not legal advice or school advice. It promises no
  result, no playing time, no acceptance, and no money. The NCAA Eligibility Center makes the final call on school
  rules, and each school decides its own aid. Some rules differ for boys and girls, by division, and by school. Dates
  marked PROJECTED are worked out from the rule text, not printed by the NCAA yet. Chapter 8 lists them.</p>
</section>

<section>
  <div class="pagehead"><span class="label">The Commit Book &middot; Basketball</span><span class="label">Before you start</span></div>
  <h2>Read this first</h2>
  <p class="lead">Read Chapter 1 before you spend any money. Then follow the plan in Chapter 2 counselor. Go one line at a time. Cross off each item when you finish it. Chapters 3 to 6 are for reference: what
  the paperwork means, what to send, what good video looks like, and what it costs.</p>

  <h3>The main idea of this book</h3>
  <p>A family that knows the team size limit, the signing dates, and the video standard compete with families that spend
  far more money. Most of what a $5,000 service sells you is setting up appointments and sending follow-ups. The rules,
  the dates, and the right questions are free, and almost nobody writes them down. That is why a written plan helps.</p>

  <h3>Three rules that surprised families last year</h3>
  <ul class="tight">
    <li><strong>The National Letter of Intent is gone.</strong> Division I ended it in October 2024 and Division II
    followed within weeks. The website that ran it for sixty years closed on 1 May 2025. What you sign now is a
    written offer of aid from one school. If something you read says "sign your NLI (National Letter of Intent)," it is a year out of date. That
    can include advice from your own coach.</li>
    <li><strong>In Division I, the number that limits a coach is how many players the team can carry, not how many
    scholarships it has.</strong> The limit is fifteen players on the team. They may be paid or unpaid. A coach can
    have fifteen players and pay only six of them.</li>
    <li><strong>Summer teams are watched by the NCAA.</strong> A Division I coach may only see players at events the
    NCAA has approved. The league has to handle this, not you. Ask before you pay.</li>
  </ul>

  <h3>Keep this log from the very first email</h3>
  <table>
    <thead><tr><th>What to write down</th><th>Why you will want it later</th></tr></thead>
    <tbody>
      <tr><td class="d">Coach name and job title</td><td>Staff changes. The person who recruited you is the one who has to reply to you.</td></tr>
      <tr><td class="d">Date and how you talked</td><td>"We talked" becomes "you emailed me on 12 November and said a spot was open."</td></tr>
      <tr><td class="d">What they asked for</td><td>Full games, a transcript, a visit: each one is a real step forward.</td></tr>
      <tr><td class="d">The number they gave</td><td>How much aid, which position, and when they would put it in writing.</td></tr>
      <tr><td class="d">Next touch</td><td>This column turns a list of schools into real progress. It is the column families leave blank.</td></tr>
    </tbody>
  </table>
</section>

<section>
  <div class="pagehead"><span class="label">The Commit Book &middot; Basketball</span><span class="label">1 &middot; Team limits</span></div>
  <h2>1. How many players a team can take</h2>
  <p>Every plan in this book comes from one question: how many players can a team carry, and how many of them can the
  team pay for? In basketball the team is small and the pool of players is huge, so the answer matters more here
  than in most sports.</p>

  <table>
    <thead><tr><th>Level</th><th>The rule today</th><th>What it means for your list</th></tr></thead>
    <tbody>
      <tr><td class="d">D1</td>
          <td><strong>Fifteen players</strong> on the team. There is no cap on the amount of aid, and no one is promised more than one year
          at a time. The old limit was 13 for men and 15 for women.</td>
          <td>Ask how many of the fifteen will be <em>paid</em> next year, and whether one is set aside for your
          position. "How many scholarships do you have" is the wrong question.</td></tr>
      <tr><td class="d">D1, other schools</td>
          <td>No national team-size rule. The conference or the school sets the size.</td>
          <td>Ask the same question. A coach who will not answer it is telling you something.</td></tr>
      <tr><td class="d">D2</td>
          <td>Ten full scholarships to spread across the whole team.</td>
          <td>Most offers are for half or a third. Compare real cost, not reputation.</td></tr>
      <tr><td class="d">D3</td>
          <td>No money for sports at all.</td>
          <td>The offer is about getting on the team, plus the aid the school gives for your grades or your family's money needs. The coach can speak up
          for you but cannot pay you.</td></tr>
      <tr><td class="d">NAIA</td>
          <td>Eight scholarships. No calendar, no rules on when a coach may contact you, and no national letter program.</td>
          <td>The lowest requirements and the fastest coach contact. But the letter you sign does not protect you the
          way you might think. Read what the school's own paper says.</td></tr>
      <tr><td class="d">Junior college</td>
          <td>Fifteen scholarships, one school year at a time, and one letter that stops your child from signing with other junior colleges.</td>
          <td>A real second path. Your child can earn credits, play right away, and move up to a four-year school a year later.</td></tr>
    </tbody>
  </table>

  <h3>The odds, in the NCAA's own numbers</h3>
  <p>There are <strong>540,704</strong> boys playing high school basketball. <strong>3.6%</strong> reach any NCAA
  school: 1.1% at Division I, 1.1% at Division II, and 1.5% at Division III. Across all high school sports, about
  <strong>2%</strong> of athletes get any money for sports. Now look at the same numbers from the other side. Last year there were
  1,187 first-year players at Division I, 988 at Division II, and 897 at Division III. <strong>61% of those open team spots
  were at Division II and Division III.</strong> The NCAA prints both numbers. Most families have only seen the first one.</p>

  <div class="box red">
    <h3>So how long should your list be?</h3>
    <p>Build your list around the schools you can really reach. For most players that means Division II, Division III,
    NAIA, or junior college, with Division I as the bonus. A good starting list has all five levels on it:</p>
    <ul class="tight" style="margin-bottom:1.5mm">
      <li>8 to 12 Division I schools where you fit a position they need</li>
      <li>10 to 15 Division II schools</li>
      <li>10 to 15 Division III schools where your grades qualify and the aid they offer fits your family</li>
      <li>5 to 10 NAIA schools</li>
      <li>3 to 5 junior college programs your child would really attend if nothing else came through</li>
    </ul>
    <p style="margin-bottom:0">Add those up and you have 40 to 55 schools. If your list is shorter than this, it is only a wish, not a working plan.</p>
  </div>
</section>

<section>
  <div class="pagehead"><span class="label">The Commit Book &middot; Basketball</span><span class="label">2 &middot; The plan by date</span></div>
  <h2>2. The plan by date, class of 2029</h2>
  <p>These dates are for a player in the class of 2029: 9th grade in 2025-26, signing in 2028-29, starting college in
  the fall of 2029. Each line names the person who owns it and what "done" means. The three lines marked
  <span class="tag t-projected">PROJECTED</span> are worked out from the rule. The rule says early signing starts on the second Wednesday in November and runs to the next Wednesday. It also says the regular period starts on the second Wednesday in April. That math matches the dates the NCAA printed for 2026-27: November 11 to 18, 2026 and April 14,
  2027. Basketball has <strong>no late signing period</strong>, so if you miss April, you wait a year.</p>

  <table>
    <thead><tr><th>Date</th><th>What happens</th><th>Who owns it</th><th>Done when</th></tr></thead>
    <tbody>
    {plan_html}
    </tbody>
  </table>
</section>

<section>
  <div class="pagehead"><span class="label">The Commit Book &middot; Basketball</span><span class="label">3 &middot; The paperwork</span></div>
  <h2>3. What the school is really offering</h2>
  <p>"Aid" means money from the school that lowers what your family pays. Each level uses a different form, and each form sets different limits on what you can do.</p>
  <table>
    <thead><tr><th>Level</th><th>The paper that counts</th><th>Earliest they can give it to you</th><th>What it does not do</th></tr></thead>
    <tbody>
      <tr><td class="d">D1</td><td>Written offer of aid from the school. It may be the school's own form or a standard
          one-page offer. Transfers sign a different paper.</td>
          <td>On or after <strong>1 August of senior year</strong>. Before that day the school may not put aid in writing.</td>
          <td>It does not hold a spot on the team for you, and it goes away if you do not qualify in school.</td></tr>
      <tr><td class="d">D2</td><td>Award letter, which is a formal financial aid document</td>
          <td>On or after <strong>1 September of senior year</strong></td>
          <td>It does not promise the same money next year. Most offers are written one year at a time.</td></tr>
      <tr><td class="d">D3</td><td>The school's own aid letter plus your acceptance letter</td>
          <td>With the acceptance letter. There is no sports aid paper at all.</td>
          <td>A Division III coach may not even use a letter of intent. Nothing you sign holds you in place.</td></tr>
      <tr><td class="d">NAIA</td><td>A letter of intent, but the NAIA does <strong>not make schools follow</strong> it</td>
          <td>Any time. The NAIA has no calendar.</td>
          <td>It gives you no protection under the national rules. Read what the school's paper says about backing out.</td></tr>
      <tr><td class="d">Junior college</td><td>One letter of intent per sport, signed on <strong>1 November</strong></td>
          <td>Binds your child for one school year</td>
          <td>It does not stop a four-year school. It does stop every other junior college.</td></tr>
    </tbody>
  </table>

  <h3>Four questions that turn "we like you" into a number</h3>
  <ol class="tight">
    <li>How many of the fifteen will be paid next year, and how many are set aside for my position?</li>
    <li>Is there room for me on the team list you hand in this December, or does a player ahead of me have to leave?</li>
    <li>What would have to be true for you to put the aid in writing on or after 1 August?</li>
    <li>If I sign in November, what happens to my money in year two?</li>
  </ol>
  <p>Coaches may answer questions one and two. The new rules that came out of a court settlement say coaches may share team-size numbers. A coach
  who answers them is recruiting you. A coach who changes the subject is telling you where you sit on the list, and
  that is worth more than a compliment.</p>
</section>

<section>
  <div class="pagehead"><span class="label">The Commit Book &middot; Basketball</span><span class="label">4 &middot; What to send</span></div>
  <h2>4. What to send, and when</h2>
  <p><strong>Who sends it.</strong> The player, from the player's own email, with the high school coach copied. Coaches
  rarely say it out loud, and NAIA coaches say it plainly: if a parent writes the email, the coach assumes the player
  cannot read or write well. The parent's job is the paperwork and the dates, not the inbox.</p>
  <p><strong>The subject line.</strong> Class year, position, height, GPA (grade point average), town, and one number that matters:</p>
  <div class="tmpl">2029 PG | 6'2" | 3.6 GPA | 14.1 PPG | Pewaukee, WI - film inside</div>
  <p><strong>The email.</strong> Under 180 words, in the player's own words. One honest line on why this school. The
  video link and the facts. One question. No attachments. Then fill out the sports form on the school's website the
  same day. Many schools put the form in their system and never open the email.</p>
  <div class="tmpl">Coach {{name}},

I am a {{grade}} grade point guard at {{high school}} in {{town}}. I am {{height}}, {{weight}}, and I run
a {{GPA}}. I averaged {{PPG}} points per game, {{RPG}} rebounds per game and {{APG}} assists per game in {{games}} varsity games
last winter ({{source}}). Our team won {{n}} games and made the {{round}}. I also grab {{n}} rebounds a game in half court. That is the part of my game I want to turn into a college job.

Film, {{duration}} minutes, defense included: {{link}}
Full games are available if you ask.

I am looking at {{division}} programs where a guard can guard two spots and run an offense. {{School}} is on
my list because {{one true reason}}. Can you tell me if you have room on the team for a guard in {{year}},
and if you want me to fill out a form?

Thank you for your time.
{{first last}} | {{high school}} class of {{class}} | {{phone}} | {{email}}
High school coach: {{name}}, {{phone}}</div>

  <p><strong>How often.</strong> First email on the day the division allows it. If no one answers, send one short
  follow-up 12 to 14 days later with one new thing in it: your numbers from the weekend, a better clip, a new grade, or
  an invitation to come watch you play. Do not write "just checking in." Do not send two emails in one day. After a
  coach gives you a phone number, a short text every four to six weeks is normal.</p>

  <h3>The one page to include: what a coach will actually use</h3>
  <ul class="tight">
    <li>Name, position, height (measured in the off-season, and say so), weight, class year, eligibility number (the ID from your child's NCAA file)</li>
    <li>High school, summer team, jersey number and color, and the town where the video was shot</li>
    <li>GPA, test scores if you have them, and where you stand on required classes</li>
    <li>This season's stats with the source named, plus two or three numbers that show your role</li>
    <li>Video link, full-game link, player email and phone, high school coach name and phone, parent contact</li>
    <li>One honest line on what you want to study</li>
  </ul>
  <p class="small">Do not put a star ranking on it. If a service ranks you 4,000th, that number will not change a
  coach's mind. A strong defensive rebounding number might.</p>

  <h2>The video, exactly</h2>
  <table>
    <thead><tr><th>Item</th><th>The standard</th><th>Why</th></tr></thead>
    <tbody>
      <tr><td class="d">Length</td><td>3:00 to 3:45, never over 4:00</td><td>Coaches say they stop watching at the first minute of music.</td></tr>
      <tr><td class="d">Clips</td><td>15 to 25 clips, 5 to 7 seconds each, plus two or three full plays shown start to finish</td><td>A full play shows the player's choices. A short clip shows editing skill.</td></tr>
      <tr><td class="d">Order</td><td>Your best three plays in the first 30 seconds, before any title screen</td><td>An intro longer than three seconds gets skipped.</td></tr>
      <tr><td class="d">Sections</td><td>Shooting &middot; passing &middot; <strong>defense</strong> &middot; full possessions</td><td>Defense is the cheapest way to stand out, and most reels have none.</td></tr>
      <tr><td class="d">Marking</td><td>An arrow or spotlight on you in every clip, no exceptions</td><td>Coaches stop watching when they have to hunt for the player.</td></tr>
      <tr><td class="d">Sound</td><td>Game sound or silence. <strong>No music.</strong></td><td>NAIA coaches say this twice in their own guides.</td></tr>
      <tr><td class="d">Camera</td><td>High up at mid-court, on a tripod, no zoom, scoreboard in frame, clean jersey</td><td>Hand-held video from the stands is the top reason a reel gets skipped.</td></tr>
      <tr><td class="d">Delivery</td><td>Unlisted YouTube link (anyone with the link can watch it, and it is not listed in searches), no password, plus a separate <strong>full game</strong>. Cut a new reel every 6 to 8 weeks and finish it by the end of junior year.</td><td>Coaches ask for the whole game. Having one ready sets you apart.</td></tr>
    </tbody>
  </table>
</section>

<section>
  <div class="pagehead"><span class="label">The Commit Book &middot; Basketball</span><span class="label">5 &middot; Summer and visits</span></div>
  <h2>5. Summer teams, visits, and the July rule</h2>
  <h3>The summer team approval system</h3>
  <p>In Division I, a coach may only watch non-school basketball at events the NCAA has approved. The system is called
  the Basketball Certification System. That is where a summer team is set up. It is also where the adults are checked. Extra paperwork shows up if a player lives with a family that is not his own. The hours a coach may watch are limited, and they differ for boys and girls. In June, men's coaches may watch from noon Friday to 6pm Sunday. Women's coaches may watch from noon Thursday to 6pm Saturday.</p>
  <div class="box">
    <h3>Ask the team these four things in writing, before you pay</h3>
    <ul class="tight">
      <li>Is this team and this event on the NCAA's approved list?</li>
      <li>Which college coaches came last year? Names and job titles, please.</li>
      <li>Where is it filmed, and does the video meet the camera standard in Chapter 4?</li>
      <li>Who is the adult in charge of my child, and has that paperwork been filed?</li>
    </ul>
  </div>
  <h3>Visits, and the rule that surprises people</h3>
  <p>A paid visit is called an official visit. It is allowed starting on the date printed in that year's calendar. It may not fall inside a dead period, when coaches are not allowed to contact recruits. The school pays for one visit per school. A
  school may host no more than five recruits at a time when it pays. There is no rule about how often you may take an
  <em>unofficial</em> visit, or how much you spend on it. Now for the rule that catches most families. <strong>In
  Division I, an unofficial visit is not allowed during the month of July.</strong> It is allowed only if your child
  already signed a written offer of aid or admission, or paid a deposit to the school. That July trip becomes a trip
  you pay for yourself, because the coach cannot host you.</p>
  <p><strong>Dead periods</strong> are December 24 to 26, plus the dates printed on each sport's calendar. In the
  2026-27 men's calendar there is also a short dead period around the November signing week and one in late February.
  In a dead period nothing is allowed: no visits, no contact, no in-person ratings.</p>
</section>

<section>
  <div class="pagehead"><span class="label">The Commit Book &middot; Basketball</span><span class="label">6 &middot; Costs</span></div>
  <h2>6. What it costs, and what is wasted</h2>
  <table>
    <thead><tr><th>Item</th><th>Real price range</th><th>When to pay, and when not to</th></tr></thead>
    <tbody>
      <tr><td class="d">Camps</td><td>$100 to $800 per camp, plus $500 to $2,000 to get there</td>
          <td>A branch of a top camp is worth it because the college coaches and staff who run the main camp show up. A plain
              invite sent to thousands of players is an ad.</td></tr>
      <tr><td class="d">Summer team</td><td>$2,000 to $5,000 a year, and sometimes $500 to $1,500 more for uniforms and travel</td>
          <td>Only if the team is on the NCAA's approved list and the event list checks out. This is the biggest cost,
              and the one families question the least.</td></tr>
      <tr><td class="d">Showcases</td><td>$250 to $950 per event, three to six times a year</td>
          <td>Pay after a coach you can name says he will be there. In basketball most coaches watch at summer-team
              events, not at big showcases.</td></tr>
      <tr><td class="d">Recruiting service</td><td>$250 to over $6,000. The two biggest ones publish no price.</td>
          <td>Ask how many college coaches actually logged in last season. A service gives you a page and a form. It
              does not give you a relationship.</td></tr>
      <tr><td class="d">Video, do it yourself</td><td>$0 to $80</td><td>Phone on a tripod, free editing software, your school's own stream.</td></tr>
      <tr><td class="d">Video, hired help</td><td>$700 to $1,200</td><td>The real cost is the person who watches your games and picks clips: $450 to
          $679. The editing itself runs $150 to $279. A studio package runs $250 to $550.</td></tr>
      <tr><td class="d">Video, full service</td><td>$1,500 to $4,000 a year</td><td>Buy it for the contacts and the scheduling, not for the graphics.</td></tr>
      <tr><td class="d">Eligibility Center</td><td>$110 in the US (fee waivers are possible)</td>
          <td>A free profile page is not the same as approval. You need approval before a Division I official visit.</td></tr>
      <tr><td class="d">Standardized tests</td><td>$68 to $70, waivers available</td>
          <td>The NCAA has not required a score for students starting college from 1 August 2023. <strong>The NAIA
              still uses test scores</strong>, and many junior college and Division II offices do too.</td></tr>
    </tbody>
  </table>
  <p>Expect to spend <strong>$3,000 to $10,000 a year</strong> while your child is in high school. Most of it is summer team fees,
  travel, and video. Two ways to do it. Handle it yourself for $700 to $2,000 a year: build the profile, keep the classes on track, send the emails yourself, and shoot your own video. Or pay for help at $1,000 to $3,500 a year, on top of the camp money you were already spending. Either can lead to an offer. The difference is time and follow-through,
  not rules.</p>

  <div class="box red">
    <h3>Six ways families waste money, biggest first</h3>
    <ol class="tight">
      <li>Paying for a showcase before a coach you can name says he will be there.</li>
      <li>Paying for the top summer circuit when your child is not the kind of player those coaches recruit. Regional events are where the
          Division II, Division III, and NAIA coaches are, and 61% of the places are with those coaches.</li>
      <li>Paying a recruiting service for a ranking. Ask how many coaches logged in last season instead.</li>
      <li>Music, free throws, warm-up dunks, and offense-only video. Defense and full possessions cost nothing and set
          you apart.</li>
      <li>Parent-written emails. Coaches say they give those less attention, and several NAIA coaches say it openly.</li>
      <li>Waiting for a camp invite from a school that is already texting you. A school that is already texting you has already invited you in.</li>
    </ol>
  </div>
</section>

<section>
  <div class="pagehead"><span class="label">The Commit Book &middot; Basketball</span><span class="label">7 &middot; Checklist</span></div>
  <h2>7. Checklist by grade</h2>
  <div class="two check">
    <p><b>9th grade</b><br>
    [ ] check every planned class against the school's NCAA-approved list, and keep a signed copy<br>
    [ ] start a lifting and shooting routine, and play a second sport if you can<br>
    [ ] find out who films your school's games at mid-court<br>
    [ ] pick a summer team; ask the approval question in writing<br>
    [ ] set up a recruiting email and one folder for everything</p>
    <p><b>10th grade</b><br>
    [ ] re-check the class list by November; fix any class that does not count<br>
    [ ] first full game video posted; first reel at 2 to 3 minutes<br>
    [ ] put the free academic testing date on the calendar<br>
    [ ] open the free Eligibility Center profile<br>
    [ ] build the school list to 40 to 55 schools across all five levels</p>
    <p><b>Summer after 10th grade</b><br>
    [ ] Division I men's contact opens June 15 (for girls, see the note in Chapter 8)<br>
    [ ] first email out with the video link; fill out the school form the same day<br>
    [ ] open the paid Eligibility Center account, or ask for the fee waiver<br>
    [ ] start visiting; write down every talk with a name and a date</p>
    <p><b>11th grade</b><br>
    [ ] send the transcript after the season; work out your core GPA (the grade point average for classes the NCAA counts)<br>
    [ ] finish the video to the Chapter 4 standard by spring<br>
    [ ] confirm the summer team is approved before the season<br>
    [ ] check visit dates against the dead periods<br>
    [ ] ask the four questions in Chapter 3 of every school that is serious about recruiting you</p>
    <p><b>Fall of 12th grade</b><br>
    [ ] read every written offer for the amount, the years, and the fine print<br>
    [ ] rank the schools that pay, on purpose, not by who texts first<br>
    [ ] decide before the window opens, not during it<br>
    [ ] November signing: sign, or wait for April on purpose</p>
    <p><b>Spring of 12th grade</b><br>
    [ ] April 1: ask for the final amateurism check<br>
    [ ] finish the remaining required classes and pass them<br>
    [ ] send the final transcript the day the school issues it<br>
    [ ] confirm the classes for the major you want<br>
    [ ] junior college route: sign one letter on November 1, or none</p>
  </div>
</section>

<section>
  <div class="pagehead"><span class="label">The Commit Book &middot; Basketball</span><span class="label">8 &middot; Sources</span></div>
  <h2>8. Sources, and what we could not settle</h2>
  <p class="small">We could not settle two dates, so we are telling you instead of guessing. First, the day a Division
  I <strong>women's</strong> coach may contact you first: One source says March 1 of junior year. Another says June 1 after 10th grade. Treat the men's June 15 date as firm. Confirm the women's date, and the first paid-visit date for boys and girls, in the current rule book before you plan a trip. Second, one page that lists the 2026-27 signing dates prints November 19. The rule text and the recruiting page give November 11 to 18. Both notes are
  printed here on purpose. A rule book that admits what it has not checked is more trustworthy than one that hides it.</p>

  <div class="box" style="background:#fffdf7">
    <h3>Start here, this week</h3>
    <ol class="tight" style="margin-bottom:0">
      <li>Print the class checklist in Chapter 7. Book the counselor meeting for the first open slot this term.</li>
      <li>Ask the summer team, in writing, whether its events are NCAA-approved.</li>
      <li>Build the school list to 40 to 55 schools before you send one email.</li>
      <li>Cut the video to the Chapter 4 standard, then send the first emails on the date your division allows.</li>
      <li>Put the three PROJECTED dates in the family calendar now, so next November is a choice and not a rush.</li>
    </ol>
  </div>

  <div class="box">
    <h3>The rest of this set</h3>
    <p class="small" style="margin-bottom:0">Football, baseball, and track and field playbooks. The eligibility
    playbook, which covers the two school deadlines that cannot be fixed later. The junior college to Division I
    playbook. And the free calendar for your sport and your child's class year, which prints the dates in Chapter 2 on
    one page. Ask us about the bundle if you want all of them.</p>
  </div>

  <div class="two small">
    <src>2026-27 NCAA Division I Manual. Rule numbers used in this book: 13.02.13, 13.1.7, 13.6, 13.9.3.1, 13.10.4,
    14.2, 14.3.1.1, 14.3.4, 17.1, 17.2. Full text: web3.ncaa.org/lsdbi/reports/getReport/90008. Checked 2026-11-10.</src>
    <src>Division I men's basketball recruiting calendar, 2026-27.
    ncaaorg.s3.amazonaws.com/compliance/recruiting/calendar/2026-27/2026-27D1Rec_MBBRecruitingCalendar.pdf. Checked 2026-11-10.</src>
    <src>Signing periods and dates, NCAA Eligibility Center. ncaa.org/eligibility-center/recruiting/. Checked 2026-11-10.</src>
    <src>NCAA news release, Division I ends the National Letter of Intent, 9 October 2024.
    ncaa.org/news/2024/10/9/division-i-eliminates-national-letter-of-intent. Checked 2026-11-10.</src>
    <src>NCAA news release on team limits, adopted 6 June 2025, plus the settlement text and the questions-and-answers
    file posted by the Division I cabinet. ncaaorg.s3.amazonaws.com. Checked 2026-11-10.</src>
    <src>Basketball Certification System pages for men and women. ncaa.org. Checked 2026-11-10.</src>
    <src>Starting school rules and the test score change. ncaa.org/eligibility-center/initial-eligibility-requirements/division-i,
    plus the how-to-request-final-certification guide at fs.ncaa.org. Checked 2026-11-10.</src>
    <src>NAIA rules: 8 scholarships, no letter program the NAIA enforces, test scores still used. getplayingeligible.com,
    play.naia.org, naia.org. Checked 2026-11-10.</src>
    <src>Junior college (NJCAA) rules for 2026-27: one letter of intent, 15 scholarships, November 1 signing date.
    njcaa.org. Checked 2026-11-10.</src>
    <src>Player counts and odds: 540,704 players, 3.6%, 2%. NCAA survey PDF and ncaa.org news, 25 October 2023. Checked 2026-11-10.</src>
    <src>Prices and video standards: sportsrecruitingteam.com, athletesportsonline.com, basketballinternals.com, NCSA
    reel guides, public freelance editing price lists, and coach interviews at blog.ncsasports.org. Checked 2026-11-10.</src>
  </div>

  <div class="sig">
    <table style="border:0"><tr>
      <td style="border:0;width:50%;padding:0"><img src="data:image/png;base64,{png64}" width="40" height="40" alt="The Commit Book"></td>
      <td style="border:0;padding:0" class="small"><strong>The Commit Book</strong> &middot; basketball playbook &middot; version 2026-27<br>
      Questions, or to tell us a rule moved: thecommitbook@example &middot; thecommitbook.com<br>
      This is education, not legal advice. No result, playing time, acceptance, or money is promised.</td>
    </tr></table>
  </div>
</section>

</body></html>
"""

(OUT / "basketball-playbook-plain.html").write_text(HEAD + BODY, encoding="utf-8")
print("plain html:", len(HEAD + BODY), "bytes ->", OUT / "basketball-playbook-plain.html")
print("plan rows:", len(PLAN))
