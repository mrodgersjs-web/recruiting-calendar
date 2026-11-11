# -*- coding: utf-8:: coding: utf-8 -*-
"""W18: render the basketball playbook as the customer-facing PDF.

Reads the logo assets and the class-of-2029 calendar rows, writes one
self-contained HTML file with the brand system already used on the site
(paper #f5f1e8, ink #141414, red #b5281a, green #1f4d3a, Barlow Condensed
labels over a serif body). The browser then prints it.
"""
import base64, json, pathlib, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = pathlib.Path(r"C:\Users\Jloeh\Developer\recruiting-calendar")
ART = pathlib.Path(r"C:\Users\Jloeh\.aside\u\1\sessions\2026-11-08_sIbJ63jY5p1sXMzN\artifacts")
OUT = REPO / "v3" / "W18-bball-pdf"
OUT.mkdir(parents=True, exist_ok=True)

mark = (REPO / "site/assets/logo/mark-light.svg").read_text(encoding="utf-8")
lockup = (REPO / "site/assets/logo/lockup-stacked-light.svg").read_text(encoding="utf-8")
mark64 = base64.b64encode(mark.encode("utf-8")).decode()
lock64 = base64.b64encode(lockup.encode("utf-8")).decode()
png = (REPO / "site/assets/logo/favicon-256.png").read_bytes()
png64 = base64.b64encode(png).decode()

rows = json.loads((ART / "basketball-deadlines-class-2029.json").read_text(encoding="utf-8"))["deadlines"]

# (date, what happens, who owns it, done when, flag)
def fmt(iso):
    import datetime as dt
    d = dt.date.fromisoformat(iso)
    return "%d %s %d" % (d.day, d.strftime("%b"), d.year)

def kind_label(k):
    return {"action": "DO IT", "hard": "HARD", "opening": "OPENS", "projected": "PROJECTED", "window": "WINDOW"}[k]

plan_rows = []
for r in sorted(rows, key=lambda r: r["iso_date"]):
    plan_rows.append(
        "<tr><td class='d'>%s</td><td class='w'>%s</td><td class='o'>%s</td><td class='n'>%s</td></tr>"
        % (fmt(r["iso_date"]), r["event"], r["owner"], r["done_when"])
        + ("<tr class='sub'><td></td><td colspan='3'>%s <span class='tag t-%s'>%s</span></td></tr>"
           % (r["plain_english"], r["kind"], kind_label(r["kind"])))
    )
plan_html = "\n".join(plan_rows)

CSS = """
@page { size: Letter; margin: 15mm 14mm 16mm 14mm; }
:root{
  --paper:#f5f1e8; --paper2:#ebe5d6; --ink:#141414; --ink2:#46423b; --ink3:#665f54;
  --rule:#d3cbb8; --red:#b5281a; --green:#1f4d3a;
}
*{box-sizing:border-box}
body{margin:0;background:#fff;color:var(--ink);
  font:400 10pt/1.46 "Iowan Old Style","Charter","Palatino Linotype",Georgia,serif;
  -webkit-print-color-adjust:exact;print-color-adjust:exact}
.label{font:700 7.4pt/1 "Barlow Condensed","Arial Narrow",sans-serif;letter-spacing:.18em;text-transform:uppercase;color:var(--ink2)}
.label.red{color:var(--red)}
h1,h2,h3{font:700 1.05em/1.12 "Barlow Condensed","Arial Narrow",sans-serif;letter-spacing:.02em;margin:0;text-transform:uppercase}
h1{font-size:30pt;letter-spacing:-.005em;line-height:1.02}
h2{font-size:14.4pt;margin:0 0 1.6mm;padding-top:2.4mm;border-top:2px solid var(--ink);page-break-after:avoid}
h3{font-size:10.6pt;margin:4mm 0 1.2mm;letter-spacing:.09em;color:var(--ink);page-break-after:avoid}
section + section{page-break-before:always}
tr{page-break-inside:avoid}
p{margin:0 0 2mm}
.lead{font-size:11.1pt;line-height:1.45;color:var(--ink2);max-width:44em}
a{color:var(--ink);text-decoration:none;word-break:break-all}
.small{font-size:8.6pt;color:var(--ink3);line-height:1.42}
strong{font-weight:700}
hr.dbl{border:0;border-top:3px double var(--ink);margin:3mm 0}
/* cover */
.cover{padding-top:0}
.cover .band{display:flex;justify-content:space-between;align-items:baseline;border-bottom:3px double var(--ink);padding-bottom:2.5mm}
.cover .rule{height:8mm}
.cover .kicker{margin-top:9mm}
.cover h1{margin:4mm 0 0}
.cover .sub{margin-top:5mm;font-size:12pt;line-height:1.42;color:var(--ink2);max-width:34em}
.cover .stamp{margin-top:9mm;border:1px solid var(--ink);background:var(--paper);padding:4mm 5mm;display:flex;gap:8mm;flex-wrap:wrap}
.cover .stamp div{flex:1 1 30%}
.cover .stamp .k{display:block;margin-bottom:1mm}
.lockwrap{display:flex;justify-content:center;padding:6mm 0 3mm}
.lockwrap img{width:62mm}
.edge{margin-top:7mm;border-left:3px solid var(--red);padding-left:4mm;font-size:10pt;color:var(--ink2);max-width:40em}
/* running bits */
.pagehead{display:flex;justify-content:space-between;align-items:baseline;border-bottom:1px solid var(--ink);padding-bottom:1.6mm;margin-bottom:4mm}
.contents{columns:2;column-gap:8mm;font-size:9.6pt;page-break-inside:avoid;margin-top:0}
.contents li{margin-bottom:1.2mm}
ol.contents{padding-left:5mm}
/* tables */
table{width:100%;border-collapse:collapse;margin:1.6mm 0 2.4mm}
th{font:700 7.4pt/1.2 "Barlow Condensed","Arial Narrow",sans-serif;letter-spacing:.14em;text-transform:uppercase;
   text-align:left;padding:1.6mm 2mm;border-bottom:1.5px solid var(--ink);color:var(--ink2)}
td{padding:1.15mm 1.8mm;border-bottom:1px solid var(--rule);vertical-align:top;font-size:9.05pt}
tr.sub td{border-bottom:1.5px solid var(--ink);font-size:8.5pt;color:var(--ink2);padding-top:0}
td.d{white-space:nowrap;font:700 9.2pt/1.35 "Barlow Condensed","Arial Narrow",sans-serif;letter-spacing:.06em;text-transform:uppercase}
td.w{width:38%}
td.o{width:16%;font-size:8.5pt;color:var(--ink2)}
td.n{width:30%;font-size:8.5pt;color:var(--ink2)}
.tag{font:700 6.6pt/1 "Barlow Condensed","Arial Narrow",sans-serif;letter-spacing:.14em;padding:.6mm 1.4mm;border:1px solid var(--ink2);color:var(--ink2);white-space:nowrap}
.t-projected{border-color:var(--red);color:var(--red)}
.t-hard{background:var(--ink);color:#fff;border-color:var(--ink)}
.t-opening{border-color:var(--green);color:var(--green)}
/* boxes */
.box{border:1px solid var(--ink);background:var(--paper);padding:2.8mm 3.4mm;margin:0 0 3mm}
.box.red{border-color:var(--red)}
.box h3{margin-top:0}
.tmpl{font:400 8.9pt/1.42 "Iowan Old Style",Georgia,serif;background:#fffdf7;border:1px solid var(--rule);padding:3mm 3.5mm;margin:0 0 3mm;white-space:pre-wrap}
ul.tight,ol.tight{margin:0 0 3mm;padding-left:5mm;font-size:9.5pt}
ul.tight li,ol.tight li{margin-bottom:.9mm}
.check{font-size:9.2pt;line-height:1.6}
.check b{font:700 8pt/1 "Barlow Condensed","Arial Narrow",sans-serif;letter-spacing:.12em;text-transform:uppercase}
.two{column-count:2;column-gap:7mm}
.sig{margin-top:6mm;border-top:3px double var(--ink);padding-top:2.5mm}
.avoid{page-break-inside:avoid}td,th{page-break-inside:avoid}
src{display:block;font-size:8.4pt;color:var(--ink3);margin-bottom:1.6mm}
"""

HTML = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>Basketball: The Whole Pathway — The Commit Book Playbook</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=PT+Serif:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body>

<!-- ============ COVER ============ -->
<section class="cover">
  <div class="lockwrap"><img src="data:image/svg+xml;base64,{lock64}" alt="The Commit Book"></div>

  <div class="kicker label red">Basketball &middot; boys and girls &middot; grades 9 to 12 &middot; sport overlay</div>
  <h1>Basketball:<br>The Whole Pathway</h1>
  <p class="sub">What to do, when to do it, who writes the check, and what the coach is allowed to say to you.
  Built on the 2026-27 NCAA Division&nbsp;I Manual, the published sport recruiting calendar, the NAIA and NJCAA
  rulebooks, and film standards coaches have said out loud.</p>

  <div class="stamp">
    <div><span class="label k">Edition</span><span class="small">2026-27 &middot; worked example: class of 2029</span></div>
    <div><span class="label k">Rules checked</span><span class="small">10 November 2026, against the bylaw text and the current calendar</span></div>
    <div><span class="label k">Levels covered</span><span class="small">NCAA D1 &middot; D2 &middot; D3 &middot; NAIA &middot; NJCAA</span></div>
  </div>

  <p class="edge">This is not a list of camps and combines. It starts with roster math, because that number
  decides how many programmes you should be emailing, when you should start, and how much you should spend.</p>

  <h2 style="border-top-width:1.5px;margin-top:12mm">Contents</h2>
  <ol class="contents">
    <li>Roster math before anything else</li>
    <li>The dated plan, class of 2029</li>
    <li>What they are actually offering you</li>
    <li>What to send, and when</li>
    <li>Grassroots, visits, and the rulebook around your summer</li>
    <li>What it costs, and what is wasted</li>
    <li>Checklist by grade</li>
    <li>Sources, and what is still flagged</li>
  </ol>

  <p class="small" style="margin-top:9mm">Education, not legal advice or academic advising. No outcome, playing time, admission or dollars promised. The Eligibility Centre makes the final academic decision and each school makes its own aid decision. Some rules differ by sex, division and school; dated items marked PROJECTED are computed from the bylaw formula and flagged in chapter 8.</p>
</section>

<!-- ============ HOW TO USE ============ -->
<section>
  <div class="pagehead"><span class="label">The Commit Book &middot; Basketball</span><span class="label">How to use this</span></div>
  <h2>How to use this playbook</h2>  <p class="lead">Read chapter one before you spend anything. Then work the dated plan in chapter two with your
  school counsellor and the athlete's club coach, one line at a time, crossing off the "done when" tests. Chapters
  three to six are reference: what the paperwork means, what to send, what film has to look like, and what it all costs.</p>

  <h3>The one idea in this book</h3>
  <p>A family that knows the roster limit, the signing formula and the film standard competes with families that have
  a bigger camp budget. Most of what a $5,000 service sells you is scheduling and follow-through; the rules, the dates
  and the questions are free, and almost nobody writes them down. That is the whole argument for a plan on paper.</p>
  <h3>What to log, from the first email</h3>
  <table>
    <thead><tr><th>Column</th><th>Why it matters later</th></tr></thead>
    <tbody>
      <tr><td class="d">Coach name and title</td><td>Staff changes; the person who recruited you is the person who owes you an answer</td></tr>
      <tr><td class="d">Date and channel</td><td>"We spoke" becomes "you emailed me on 12 November and said room existed at 15"</td></tr>
      <tr><td class="d">What they asked for</td><td>Full games, a transcript, a visit date: each one is a real stage of interest</td></tr>
      <tr><td class="d">The number they gave</td><td>Fraction of aid, position group, and when it would be written down</td></tr>
      <tr><td class="d">Next agreed touch</td><td>This is the field that turns a list into a pipeline, and the one every family leaves blank</td></tr>
    </tbody>
  </table>
  <div class="box">
    <h3>Three things that surprised families last year</h3>    <ul class="tight">
      <li><strong>The National Letter of Intent no longer exists.</strong> Division&nbsp;I eliminated it in October 2024 and
      Division&nbsp;II followed within weeks. The site that ran it for sixty years went dark on 1 May 2025. What you sign now
      is a school's <em>written offer of athletics aid</em>. Anything you read that says "sign your NLI" is a year out of date,
      including your own coach's advice.</li>
      <li><strong>In Division&nbsp;I the number that binds a coach is a roster limit, not a scholarship limit.</strong> At
      settlement schools, fifteen players in the program, funded or not. A coach can hold fifteen people and fund six.</li>
      <li><strong>Grassroots events are gated.</strong> A Division&nbsp;I coach may only evaluate at NCAA-certified events.
      The league, not the parent, is responsible for that. Ask before you pay.</li>
    </ul>
  </div>
</section>

<!-- ============ 1 ROSTER MATH ============ -->
<section>
  <div class="pagehead"><span class="label">The Commit Book &middot; Basketball</span><span class="label">1 &middot; Roster math</span></div>
  <h2>1. Roster math before anything else</h2>
  <p>Every plan in this book follows from one question: how many players can a team actually carry, and how many of
  them can it pay? Basketball answers it more brutally than almost any other sport, because the roster is small, the
  participation pool is enormous, and the aid is almost never full.</p>

  <table class="">
    <thead><tr><th>Level</th><th>What the limit is now</th><th>What that means for your list</th></tr></thead>
    <tbody>
      <tr><td class="d">D1, settlement school</td>
          <td><strong>15 people</strong> in the program, aid not capped and not guaranteed. Previously 13 for men, 15 for women.</td>
          <td>Ask how many of the 15 will be <em>funded</em> next year, and whether one is held for your position group.
              "How many scholarships do you have" is the wrong question.</td></tr>
      <tr><td class="d">D1, non-settlement</td>
          <td>No national roster law; the conference or the school sets it.</td>
          <td>Ask the same question. The answer may be a conference rule, and a coach who cannot answer it is telling you something.</td></tr>
      <tr><td class="d">D2</td>
          <td>10 equivalencies for the whole squad.</td>
          <td>Offers are usually halves and thirds. Compare real cost, not prestige.</td></tr>
      <tr><td class="d">D3</td>
          <td>No athletic aid at all.</td>
          <td>The offer is an admissions decision plus an institutional aid package. The coach can advocate, not pay.</td></tr>
      <tr><td class="d">NAIA</td>
          <td>8 scholarships. No recruiting calendar, no evaluation restriction, no enforced letter of intent.</td>
          <td>Lowest academic bar and the most direct coach contact, but the paperwork binds you to nothing and to everything at once. Read the school's own paper.</td></tr>
      <tr><td class="d">NJCAA</td>
          <td>15 scholarships, one academic year per sport, one letter of intent that closes every other JUCO door.</td>
          <td>A genuine second path with transfer credit, and the one route where a late bloomer can rebuild a class year.</td></tr>
    </tbody>
  </table>

  <h3>The odds, in the NCAA's own numbers</h3>
  <p>Of <strong>540,704</strong> high-school boys players, <strong>3.6%</strong> reach any NCAA school: 1.1% at
  Division&nbsp;I, 1.1% at Division&nbsp;II, 1.5% at Division&nbsp;III. Across all high-school athletes in every sport,
  about <strong>2%</strong> receive any athletic aid. Count the doors from the other direction and there were 1,187
  first-year students at D1, 988 at D2 and 897 at D3: <strong>61% of the doors are D2 and D3.</strong> The NCAA publishes
  both figures and most families have seen only the first.</p>

  <div class="box red avoid">
    <h3>So what the plan looks like</h3>
    <p style="margin-bottom:0">Build the list for the doors you can actually reach and treat Division&nbsp;I as the upside.
    A realistic basketball list is roughly <strong>8 to 12 Division&nbsp;I</strong> programs where you have a position-group
    case, <strong>10 to 15 Division&nbsp;II</strong>, <strong>10 to 15 Division&nbsp;III</strong> where the academic fit and the aid
    package work, <strong>5 to 10 NAIA</strong>, and <strong>3 to 5 JUCO</strong> programs you would genuinely attend if the spring
    went sideways. Anything narrower is a wish, not a plan.</p>
  </div>
</section>
<!-- ============ 2 DATED PLAN ============ -->
<section>
  <div class="pagehead"><span class="label">The Commit Book &middot; Basketball</span><span class="label">2 &middot; The dated plan</span></div>
  <h2>2. The dated plan, class of 2029</h2>
  <p>Dates below are for a player in the class of 2029: ninth grade in 2025-26, signing in 2028-29, enrolling in
  autumn 2029. Every line has an owner and a test for what "done" means. The three items marked
  <span class="tag t-projected">PROJECTED</span> are computed from the bylaw formula ("second Wednesday in November
  through the following Wednesday"; the regular period opens the second Wednesday in April), and that formula
  reproduces the published 2026-27 dates exactly, 11 to 18 November 2026 and 14 April 2027. Basketball has
  <strong>no late signing period</strong>, so a missed April is a missed year.</p>

  <table>
    <thead><tr><th>Date</th><th>What happens</th><th>Who owns it</th><th>Done when</th></tr></thead>
    <tbody>
    {plan_html}
    </tbody>
  </table>
</section>

<!-- ============ 3 THE PAPER ============ -->
<section>
  <div class="pagehead"><span class="label">The Commit Book &middot; Basketball</span><span class="label">3 &middot; The paper</span></div>
  <h2>3. What they are actually offering you</h2>
  <table class="">
    <thead><tr><th>Level</th><th>The binding document</th><th>When it may be issued</th><th>What it does not do</th></tr></thead>
    <tbody>
      <tr><td class="d">D1</td><td>Written offer of athletics aid (school form, may be an admissions letter or a generic
          NLI-style form), or a National Transfer Agreement for transfers</td>
          <td>On or after <strong>1 August of senior year</strong> (Bylaw 13.9.3.1); before that a school may not put aid in writing</td>
          <td>Does not reserve a roster spot past the roster submission date, and does not survive an eligibility failure</td></tr>
      <tr><td class="d">D2</td><td>Award letter (formal financial aid document, by definition)</td>
          <td>On or after <strong>1 September of senior year</strong></td>
          <td>Does not guarantee multi-year payment; renewal is annual</td></tr>
      <tr><td class="d">D3</td><td>Institutional aid award letter plus the admissions decision</td>
          <td>With admission, no athletic-aid paper at all</td>
          <td>Letters of intent are prohibited (13.9.1): a D3 coach cannot hold you to anything</td></tr>
      <tr><td class="d">NAIA</td><td>A letter of intent, but the NAIA runs <strong>no enforcement programme</strong> for it</td>
          <td>Any time; the NAIA has no recruiting calendar</td>
          <td>Gives you no national protection; read what the school's own document says about withdrawal</td></tr>
      <tr><td class="d">NJCAA</td><td>One letter of intent per sport, national signing date <strong>1 November</strong></td>
          <td>Binding for one academic year</td>
          <td>Does not make you unrecruitable to four-year schools; does bind you against every other JUCO</td></tr>
    </tbody>
  </table>

  <h3>Four questions that turn "we're interested" into a number</h3>
  <ol class="tight">
    <li>How many of the 15 will be funded next year, and how many are held for my position group?</li>
    <li>Is there room for me at the roster limit you submit in December, or does someone ahead of me have to leave?</li>
    <li>What would have to be true for you to write the aid down on or after 1 August?</li>
    <li>If I sign in November, what happens to my aid in year two?</li>
  </ol>
  <p>Questions one and two are legal to ask and answerable under the settlement rules. A coach who answers them is
  recruiting you; one who changes the subject is telling you where you are on the board, and that is worth more than
  a compliment.</p>
</section>

<!-- ============ 4 WHAT TO SEND ============ -->
<section>
  <div class="pagehead"><span class="label">The Commit Book &middot; Basketball</span><span class="label">4 &middot; What to send</span></div>
  <h2>4. What to send, and when</h2>
  <p><strong>Who presses send.</strong> The athlete, from the athlete's address, with the high-school coach copied.
  Coaches will not always say it, and NAIA coaches say it plainly: if a parent writes, they assume nobody can read.
  The parent's job is the paperwork and the deadline, not the inbox.</p>
  <p><strong>The subject line.</strong> Class year, position, height, GPA, town, and one number that matters:</p>
  <div class="tmpl">2029 PG | 6'2" | 3.6 GPA | 14.1 PPG | Pewaukee, WI - film inside</div>
  <p><strong>The body.</strong> Under 180 words, in the player's own voice. One honest sentence on why this school.
  The film link and the data block. One ask. No attachments. Send it, then file the questionnaire on the athletics
  site the same day, because most programs enter the questionnaire into the database and never open the email.</p>
  <div class="tmpl avoid">Coach {{name}},

I am a {{grade}} class point guard at {{high school}} in {{town}}. I am {{height}}, {{weight}}, and I run
a {{GPA}} with {{test line}}. I averaged {{PPG}} points, {{RPG}} rebounds and {{APG}} assists in {{games}} varsity games
last winter ({{source}}); our team won {{n}} and made the {{round}}. I am also {{n}} in the {{shot chart stat}},
which is the part of my game I am trying to turn into a college role.

Film, {{duration}} minutes, defence included: {{link}}
Full games available on request.

I am looking at {{division}} programs where a guard can defend two positions and run an offense. {{School}} is on
my list because {{one true, specific reason}}. Could you tell me whether you have room in the roster limit for a
guard in {{year}}, and whether you would want a questionnaire?

Thank you for your time.
{{first last}} | {{high school}} {{class}} | {{phone}} | {{email}}
High-school coach: {{name}}, {{phone}}</div>

  <p><strong>The cadence.</strong> First contact on the day the division allows it. If there is no answer, one follow-up
  after 12 to 14 days with one new thing in it: a weekend stat line, a better clip, a grade, an invitation to see you
  play. Never "just checking in", never two emails in the same day. After a contact number exists, a short text every
  four to six weeks is normal and expected; the phone number is yours to give once they ask for it.</p>

  <h3>The one-sheet: fields a coach will use</h3>
  <ul class="tight">
    <li>Name, position, height (barefoot in the off-season, and say which), weight, class year, eligibility number</li>
    <li>High school, club program, jersey number and colour, and the town the film was shot in</li>
    <li>GPA, test scores if you have them (NAIA still uses them), and course list status</li>
    <li>Season stats with the source named, and the two or three numbers that describe your role rather than your ceiling</li>
    <li>Film link, full-game link, athlete email and phone, high-school coach name and phone, parent contact</li>
    <li>One honest line on what you want to study</li>
  </ul>
  <p class="small">Put no ranking on it. If a service ranks you 4,000th, that number will not change anyone's mind;
  your defensive rebounding rate will.</p>

  <h2>The film, to the inch</h2>
  <table class="">
    <thead><tr><th>Item</th><th>The standard</th><th>Why</th></tr></thead>
    <tbody>
      <tr><td class="d">Length</td><td>3:00 to 3:45, hard ceiling 4:00</td><td>Coaches describe stopping at the first minute of music</td></tr>
      <tr><td class="d">Count</td><td>15 to 25 clips, 5-7 seconds each, plus two or three full possessions</td><td>A sequence shows a decision; an isolated highlight shows editing</td></tr>
      <tr><td class="d">Order</td><td>Best three plays in the first 30 seconds, before any title card</td><td>An intro longer than three seconds is a skip</td></tr>
      <tr><td class="d">Sections</td><td>Shooting &middot; playmaking &middot; <strong>defence</strong> &middot; full possessions</td><td>Defence is the least contested way to stand out, and most reels have none</td></tr>
      <tr><td class="d">Marking</td><td>Arrow or spotlight on you in every clip, no exceptions</td><td>Four-on-one film is how coaches quit watching</td></tr>
      <tr><td class="d">Audio</td><td>Original sound or silence. <strong>No music.</strong></td><td>Say it twice in the NAIA coaching literature</td></tr>
      <tr><td class="d">Capture</td><td>Elevated mid-court, tripod, no zoom, scoreboard visible, clean jersey</td><td>Handheld bleacher video is the most common reason a reel is skipped</td></tr>
      <tr><td class="d">Delivery</td><td>Unlisted YouTube link, no password, plus a separate hosted <strong>full game</strong>; re-cut every 6-8 weeks, finished by the end of junior year</td><td>Coaches ask for the whole game; having it ready is the differentiator</td></tr>
    </tbody>
  </table>
</section>

<!-- ============ 5 GRASSROOTS ============ -->
<section>
  <div class="pagehead"><span class="label">The Commit Book &middot; Basketball</span><span class="label">5 &middot; Grassroots and visits</span></div>
  <h2>5. Grassroots, visits, and the rulebook around your summer</h2>
  <h3>The certification system</h3>
  <p>Division&nbsp;I coaches may evaluate non-scholastic basketball only at events and on teams that go through the NCAA
  <strong>Basketball Certification System</strong> (Bylaw 13.10.4). That is where a grassroots program is built, where adults are
  screened, and where a 16- or 17-year-old's non-parent host-family address creates extra paperwork. The permissible
  windows are narrower than families expect and differ by sex: in the June men's window, coaches may evaluate from noon
  Friday to 6pm Sunday; the women's June window runs noon Thursday to 6pm Saturday, with separate contact windows in
  September, at national association events, and in April.</p>
  <div class="box">
    <h3>Ask the program, in writing, before you pay</h3>
    <ul class="tight">
      <li>Is this team and this event certified in the Basketball Certification System?</li>
      <li>Which college coaches attended last year, by name and title, from the division I am targeting?</li>
      <li>Where exactly is it broadcast, and does the film meet the elevated-camera standard in chapter four?</li>
      <li>Who is the non-parent adult on my roster, and will the host-family documentation be filed?</li>
    </ul>
  </div>
  <h3>Visits, and the rule nobody expects</h3>
  <p>Official (paid) visits open on the first date printed in that year's recruiting calendar and may not fall inside
  an evaluation or dead period; each school may pay for one visit, and a school may host a maximum of five visitors at
  an institutional money event at a time. There is no rule limiting how many times you may take an
  <em>unofficial</em> visit or how much you may spend on it. One date bites families: <strong>in Division I an unofficial
  visit is not permissible during the month of July</strong> unless the player has signed a written offer of admission or aid,
  or paid an admissions deposit. The July scouting trip becomes a road trip; the coach cannot host you.</p>
  <p><strong>Dead periods</strong> are 24 to 26 December and the dates printed on each sport's calendar. In the 2026-27
  men's calendar there is also a short dead period around the November signing window and one in late February. Nothing
  is permissible in a dead period: no visits, no contact, no evaluations.</p>
</section>

<!-- ============ 6 COSTS ============ -->
<section>
  <div class="pagehead"><span class="label">The Commit Book &middot; Basketball</span><span class="label">6 &middot; Costs</span></div>
  <h2>6. What it costs, and what is wasted</h2>
  <table class="">
    <thead><tr><th>Line</th><th>Real published range</th><th>When to pay, or not</th></tr></thead>
    <tbody>
      <tr><td class="d">Camps and clinics</td><td>$100-$800 per event, plus $500-$2,000 in travel</td>
          <td>A branch of an elite camp is the one that puts you in front of the college staff who attend it. A generic
              invitation is marketing sent to thousands.</td></tr>
      <tr><td class="d">Grassroots season</td><td>$2,000-$5,000 per year, sometimes with a $500-$1,500 uniform-and-travel charge on top</td>
          <td>Only if the program is certified and the event list is one you can verify. This is the single largest ticket,
              and the one least often questioned.</td></tr>
      <tr><td class="d">Showcases</td><td>$250-$950 per event, three to six times a year</td>
          <td>Pay after a named coach confirms attendance in writing. In basketball most attendance comes from the
              grassroots schedule, not from invitationals.</td></tr>
      <tr><td class="d">Recruiting service</td><td>$250 to more than $6,000; the largest two publish no price at all</td>
          <td>Ask for the number of coaches who actually logged in last season. The service is a mailbox and a
              questionnaire; it is not a relationship.</td></tr>
      <tr><td class="d">Film, do it yourself</td><td>$0-$80</td><td>Phone on a tripod, free editor, your school's stream.</td></tr>
      <tr><td class="d">Film, freelance</td><td>$700-$1,200</td><td>The play-picker is the real cost, $450-$679 for someone to watch your games and choose clips.
          Editing is $150-$279; a full-service studio package is $250-$550.</td></tr>
      <tr><td class="d">Film, full service</td><td>$1,500-$4,000 a year</td><td>Buy it for the network and the scheduling, not the graphics.</td></tr>
      <tr><td class="d">Eligibility Centre</td><td>$110 domestic (fee waivers possible; one published guide still says $65)</td>
          <td>Free Profile Page is not certification. Certification is required before a D1 official visit.</td></tr>
      <tr><td class="d">Standardised tests</td><td>$68-$70, fee waivers available</td>
          <td>The NCAA has not required a score for students enrolling from 1 August 2023. <strong>The NAIA still uses test
              scores</strong>, and many JUCO and D2 admission offices do too.</td></tr>
    </tbody>
  </table>
  <p>Plausible total, spread across four years: <strong>$3,000-$10,000 a year</strong>, most of it grassroots registration,
  travel and film. Two service tiers, for comparison: a build-it-yourself year at $700-$2,000 (profile, core courses,
  self-scheduled emails, DIY film) against a full-service year at $1,000-$3,500 on top of the camp money you were
  already spending. Both can produce an offer. The difference is time and follow-through, not rules.</p>

  <div class="box red">
    <h3>Six ways families waste money, in order of size</h3>    <ol class="tight">
      <li>Paying for a showcase before a named coach confirms he will be there.</li>
      <li>Buying the elite grassroots circuit for a body type the circuit does not target. The regional events are where
          the D2, D3 and NAIA coaches, who are 61% of your doors, actually are.</li>
      <li>Buying a recruiting service for the ranking it gives you. Ask instead how many coaches logged in last season.</li>
      <li>Music, free throws, warm-up dunks, and offence-only film. Defence and full possessions are the cheapest edge in
          the sport.</li>
      <li>Parent-voiced emails. Coaches report deprioritising them, and several NAIA coaches say it out loud.</li>
      <li>Waiting for a camp invitation you already received at a school that is already texting you. The second invitation
          is not an evaluation; the first one was.</li>
    </ol>
  </div>
</section>

<!-- ============ 7 CHECKLIST ============ -->
<section>
  <div class="pagehead"><span class="label">The Commit Book &middot; Basketball</span><span class="label">7 &middot; Checklist by grade</span></div>
  <h2>7. Checklist by grade</h2>
  <div class="two check">
    <p><b>Ninth grade</b><br>
    [ ] every planned course mapped against the school's NCAA-approved list, signed copy kept<br>
    [ ] strength and shooting routine started; play both sports if you can<br>
    [ ] full-game source identified (school stream, Sideline, PlayOn)<br>
    [ ] club program shortlisted; certification question asked in writing<br>
    [ ] recruiting email and calendar created, one folder for everything</p>
    <p><b>Tenth grade</b><br>
    [ ] recheck the course map in November; fix any off-list course now<br>
    [ ] first full-game cut hosted; first highlight reel at 2-3 minutes<br>
    [ ] Elite 24 or equivalent academic date entered<br>
    [ ] free Eligibility Centre Profile Page<br>
    [ ] target list built to 60 programs by position group</p>
    <p><b>Summer after tenth</b><br>
    [ ] D1 men's first contact opens 15 June (women's: see the flag in chapter 8)<br>
    [ ] first email sent with the film link; questionnaire filed the same day<br>
    [ ] certification account opened and paid or waiver requested<br>
    [ ] unofficial visits started; log every conversation with a name and a date</p>
    <p><b>Junior year</b><br>
    [ ] transcript sent after the season; core GPA calculated<br>
    [ ] reel finished to the chapter-four standard by spring<br>
    [ ] certification confirmed before the grassroots season<br>
    [ ] official-visit window checked against dead periods<br>
    [ ] the four questions in chapter three asked of every serious program</p>
    <p><b>Fall of senior year</b><br>
    [ ] written offers read for amount, years and renewal language<br>
    [ ] aid-offering schools ranked deliberately, not by which coach texts first<br>
    [ ] decision made before the window opens, not inside it<br>
    [ ] November signing: sign, or choose April on purpose</p>
    <p><b>Spring of senior year</b><br>
    [ ] 1 April: request final amateurism certification<br>
    [ ] remaining core courses scheduled and passing<br>
    [ ] final transcript with graduation proof sent the day it is issued<br>
    [ ] academic requirements for the major confirmed with the department<br>
    [ ] if JUCO: one letter of intent on 1 November, or none</p>
  </div>
</section>

<!-- ============ 8 SOURCES ============ -->
<section>
  <div class="pagehead"><span class="label">The Commit Book &middot; Basketball</span><span class="label">8 &middot; Sources</span></div>
  <h2>8. Sources, and what is still flagged</h2>
  <div class="box" style="background:#fffdf7">
    <h3>Start here, this week</h3>
    <ol class="tight" style="margin-bottom:0">
      <li>Print the course map in chapter 7 and book the counsellor meeting for the first free slot this term.</li>
      <li>Ask the club program, in writing, whether it is certified in the Basketball Certification System.</li>
      <li>Build the target list to 40 to 50 programs across all five levels before you send a single email.</li>
      <li>Cut the film to the chapter-four standard, then send the first emails on the date your division allows.</li>
      <li>Put the three PROJECTED dates in the family calendar now, so next November is a decision and not a scramble.</li>
    </ol>
  </div>
  <div class="box">
    <h3>The rest of the set</h3>
    <p class="small" style="margin-bottom:0">Football, baseball and track &amp; field playbooks, the eligibility
    playbook (the two hard deadlines), the JUCO-to-D1 playbook, and the free class-year calendar that prints the dates
    in chapter two for your sport and your graduating class. Ask us for the bundle if you want all of them.</p>
  </div>
  <p class="small">Two research passes disagreed on when a Division&nbsp;I <strong>women's</strong> basketball coach may first
  initiate contact: one read 1 March of the player's junior year, the other 1 June after the sophomore year. Treat the
  men's 15 June date as firm, and confirm the women's date, and the first official-visit date for both sexes, in the
  current calendar before you plan around them. The same page that carries the 2026-27 signing dates prints 19 November
  where the bylaw formula and the recruiting page give 11-18 November. We flag both rather than pick silently.</p>
  <div class="two small">
    <src>2026-27 NCAA Division I Manual, Bylaws 13.02.13, 13.1.7, 13.6, 13.9.3.1, 13.10.4, 14.2, 14.3.1.1, 14.3.4, 17.1, 17.2
    (LSDBi, full text) &middot; web3.ncaa.org/lsdbi/reports/getReport/90008 &middot; checked 2026-11-10</src>
    <src>Division I men's basketball recruiting calendar, 2026-27 &middot; ncaaorg.s3.amazonaws.com/compliance/recruiting/calendar/2026-27/2026-27D1Rec_MBBRecruitingCalendar.pdf &middot; checked 2026-11-10</src>
    <src>Signing periods and dates, NCAA Eligibility Center &middot; ncaa.org/eligibility-center/recruiting/ &middot; checked 2026-11-10</src>
    <src>NCAA News, Division I eliminates National Letter of Intent, 9 October 2024 &middot; ncaa.org/news/2024/10/9/division-i-eliminates-national-letter-of-intent &middot; checked 2026-11-10</src>
    <src>NCAA News, roster limits adopted 6 June 2025; settlement text at athleticsaid.s3.amazonaws.com/settlement/NCAA-Basketball-Roster-Limits-Settlement-Text-(Final)-05.09.25.pdf; settlement Q&amp;A at ncaaorg.s3.amazonaws.com/governance/d1/legislation/2024-25/June2025D1Gov_PhaseThreeInstSetQuestionandAnswer.pdf &middot; checked 2026-11-10</src>
    <src>Basketball Certification System &middot; ncaa.org/sports/mbball/2023-24-division-i-basketball-certification-system.aspx; women's windows page at ncaa.org/sports/wbball/2022-23/news/2021/9/3/womens-basketball-certification-system.aspx &middot; checked 2026-11-10</src>
    <src>Initial eligibility requirements &middot; ncaa.org/eligibility-center/initial-eligibility-requirements/division-i; test-score relief news release, 16 November 2021; How to Request Final Amateurism Certification PDF at fs.ncaa.org &middot; checked 2026-11-10</src>
    <src>NAIA eligibility and recruiting (8 scholarships, 9 players, no enforced letter-of-intent programme, test scores still used) &middot; getplayingeligible.com; play.naia.org; naia.org &middot; checked 2026-11-10</src>
    <src>NJCAA bylaws and rules, 2026-27 (one letter of intent, 15 scholarships, 1 November signing date) &middot; njcaa.org &middot; checked 2026-11-10</src>
    <src>Participation and odds figures (540,704; 3.6%; 2%) &middot; NCAA Interassociation Questionnaire research PDF at ncaaorg.s3.amazonaws.com/research/popco/2023/2023IQ_Boys_Participation.pdf; ncaa.org/news/2023/10/25/what-it-takes-to-play-college-basketball; college sports commission brief &middot; checked 2026-11-10</src>
    <src>Cost and film standards &middot; sportsrecruitingteam.com pricing and film guides; athletesportsonline.com camp costs; basketballinternals.com grassroots fees; NCSA reel guides; public freelance editing ladders; coach statements at blog.ncsasports.org and the I want a coach podcast &middot; checked 2026-11-10</src>
  </div>

  <div class="sig">
    <table style="border:0"><tr>
      <td style="border:0;width:50%;padding:0"><img src="data:image/png;base64,{png64}" width="40" height="40" alt="The Commit Book"></td>
      <td style="border:0;padding:0" class="small"><strong>The Commit Book</strong> &middot; basketball sport overlay &middot; edition 2026-27<br>
      Questions, or to report a rule that has moved: thecommitbook@example &middot; thecommitbook.com<br>
      Education, not legal advice. No outcome, playing time, admission or dollars promised.</td>
    </tr></table>
  </div>
</section>

</body></html>
"""

(OUT / "basketball-playbook.html").write_text(HTML, encoding="utf-8")
(OUT / "mark.b64").write_text(mark64, encoding="utf-8")
print("html:", len(HTML), "bytes ->", OUT / "basketball-playbook.html")
print("rows rendered:", len(plan_rows))
