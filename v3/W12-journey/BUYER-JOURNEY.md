# The Commit Book: Buyer Journey and Value Map

Written 2026-11-07. Scope: six buyers from the live /segments page. Education for parents of high-school athletes. We do not recruit or place athletes, and we give no legal advice.

## How to read this

Step labels:
- `live`: the page exists today. The route is given.
- `needs-page`: the step needs a page we have not built. A route and contents are proposed.
- `gap`: no step exists. The doc names what would fill it.

Plain facts about the site today (checked in the repo on 2026-11-07):
- The 10 offerings each have a /tools/<slug> page. Every one of them is a "coming soon, leave your email" page, including the 8 whose deliverable file is BUILT. So no offering can be bought or even downloaded from the site today. This is a `needs-page` fact for every purchase step below.
- Checkout is OFF behind a flag (503 in preview). This is a deliberate readiness gate. /account says no card has been charged and none can be.
- Email capture exists (/api/capture) and saves email, sport and class year. Email copy exists only as drafts (funnel/emails/DRAFTS.md). No email product is live and no monitored support mailbox is published.
- /price offers Sideline $149/yr and Pathway $99 one-year, as a founding 100-slot price. Audit and Club are listed as not yet offered.
- Statuses: BUILT means the deliverable file exists in v3/W8-offerings/deliverables/. PROPOSED means announced, not sold, no fulfillment claimed.

Source names used inline: Aspen Project Play 2024, NFHS 2024-25, Social Fetch parent-problem sample. No other statistic appears here. Anything marked (inference) is our reading, not a sourced fact.

## Shared entry points (all six buyers)

- Search: parent types a rule question ("when can college coaches contact my kid"). Lands on an /answers page. `live`.
- Instagram, Reddit, Facebook groups: a parent shares a playbook or story link. Lands on /playbooks/* or /story/*. `live`. Posting and community work is not a page and is outside this doc. (inference: these are the places parents ask the questions in the Social Fetch parent-problem sample.)
- Referral: another parent sends a link. No referral mechanic exists. `gap` (see funnel spine).

## Not-for-claim rules that apply to every buyer

- We cannot promise a coach reply, an offer, a scholarship or a roster spot.
- The site is education, not legal advice.
- We do not recruit, place athletes, or contact anyone's kid.
- Athlete stories are built from public information. Composites are labeled composites.
- Every price on /price is a proposed founding price until checkout is on.

---

## Buyer 1: 9th/10th Grade Planner

**Who and their moment.** Parent of a 9th or 10th grader. No coach has called. In their words (inference, paraphrase): "Everyone says start early. I don't know what early means, and I don't want to pay for something too soon."

**Path**
1. Entry: search for a rules question, or a parent group post. `live` (/answers, /playbooks).
2. Landing: /start. `live`.
3. Aha: /calendar shows what a coach may and may not do for their sport and class year, so "no one has called" turns out to be normal. `live`.
4. Depth: /playbooks/eligibility-2-hard-deadlines. `live`.
5. First ask (email): /personalize (Denver pilot, announce-only) and the free guide capture on /start. Email is saved. `live` for capture. The follow-up emails are `gap` (drafts only, none sends).
6. Check: family spending check, #view-c on /segments. `live`.
7. Offer: Contact Log ($0) as the first thing to keep, then Season & Film Planner ($19) at sophomore summer. Download page for either: `needs-page` (/tools/contact-log and /tools/season-planner are notify-me shells today).
8. Purchase: Sideline $149/yr is not the right buy yet for most of this family (see objection). Checkout `gap` while the flag is off.
9. After: the yearly calendar rebuild email each fall. `gap`.

**What they should get out of it**
- Contact Log: one grid with a row per coach touch, ready before the first touch happens.
- Season & Film Planner: a season page with recruiting windows pre-marked and a clip list to start filming.
- Free pages: a dated list of what is allowed in their sport and class year, and the two eligibility deadlines that cannot be missed.

**Objection and honest answer.** "Why pay anything now?" Honest answer: most of this stage is free, and the site says so. Nothing recurring is needed before sophomore summer (spend note on /segments). The paid tier earns its place when the family starts contacting coaches.

**What we must not claim.** That starting earlier gets a coach to reply. That a young athlete should be paying a service now. That the Denver pilot is a placement program.

**How to measure.** One number: share of email captures who open /calendar a second time within 30 days. Event: `calendar_return_visit` keyed to the saved email's sport and class year.

---

## Buyer 2: Late-Start Junior/Senior Panic

**Who and their moment.** Junior or senior. No list, no film plan, no replies. Rosters are filling. In their words (inference): "We waited. Is it over? Who do I even email?"

**Path**
1. Entry: search ("late to recruiting", "senior year no offers"), Reddit or a Facebook group thread. `live` for the landing, community work is outside this doc.
2. Landing: /playbooks/late-bloomer. `live`. This is the aha: a late start has a path, with steps in order.
3. Next: /start. `live`.
4. Tool: /access (contact-date calculator, athlete-voice email builder with red-flag linter, 30-school tracker with CSV and .ics export). `live`. This is where the first concrete list is built.
5. Cost check: /answers/ncaa-eligibility-center-account-cost. `live`. Tells them what is a real required cost.
6. First ask (email): save the 30-school list or the .ics file by email. `needs-page` (the save-by-email step on /access is not built).
7. Offer: The First Contact Pack ($9, PROPOSED) for 12 email templates by moment, and Contact Log ($0). Both `needs-page`: the Pack is not written, the Log is a notify-me shell.
8. Purchase: Pathway $99 one-year fits this buyer better than Sideline (inference: one season of need). Checkout `gap`.
9. After: a weekly Sunday review email tied to the Contact Log. `gap`.

**What they should get out of it**
- /access: a 30-school list with contact dates and a first email ready to send, in their kid's voice.
- Contact Log: a record of who was emailed and when, with follow-up triggers (unanswered 10 days).
- First Contact Pack (once built): the right email for each moment, from first touch to offer follow-up.

**Objection and honest answer.** "Is it too late?" Honest answer: we cannot say it is not. We can say the late-bloomer playbook lays out what to do in what order, and that the free tools build the list. Roster math on /math shows how many spots exist at the levels they target.

**What we must not claim.** That a late start can be fixed. That emails will get replies. That any paid fast-track exists (that is the panic service the buyer is trying not to buy). Spend note: only verified essentials.

**How to measure.** One number: share of /access visitors who export the 30-school list (CSV or .ics). Event: `access_export`.

---

## Buyer 3: Burned by a Paid Recruiting Service or Showcase Circuit

**Who and their moment.** Paid $1,500-$4,200 (parents in the Social Fetch parent-problem sample report up to about $4K plus monthly fees). Wants out. In their words (inference): "Was it worth it? How do I cancel? What do I do now?"

**Path**
1. Entry: search ("recruiting service refund", "is X legit"), a parent group warning thread. Landing is the strongest word-of-mouth surface for this buyer (inference). `live` for the landing, community work outside this doc.
2. Landing: /recruitiq. `live`. The aha is seeing the standards and fit data that show what the service never told them.
3. Next: /compare. `live`. Then /calendar. `live`.
4. Red flags: /tools/red-flags. `needs-page` today. It is announce-only, a notify-me shell, while the 40-flag checklist is BUILT in v3/W8-offerings/deliverables/red-flags.md.
5. First ask (email): "Get the Red Flags checklist." This is the best free trade on the site for this buyer. Capture works. Delivery `needs-page` (checklist PDF or page not published).
6. Money step: budget reallocator. `gap`. Named in the segment plan, no route exists. Propose /tools/budget-reallocator: enter what was paid and the monthly fee, see what the same money covers (verified essentials, camps with real return from /playbooks/camp-roi).
7. Offer: Red Flags ($0) first. Then Offer Comparison ($29) if offers arrive, Contact Log ($0) to take over the work themselves. `needs-page` for each.
8. Purchase: Pathway $99 one-year is the natural size for a family who just lost money (inference). Checkout `gap`.
9. After: the cancellation question. `gap`. A plain "what to check in your contract" page: terms to find, who to write to, what to keep. Education, not legal advice.

**What they should get out of it**
- Red Flags: 40 warning signs in 4 groups (money, playing time, academic fit, treatment), with one line on what to ask instead.
- Contact Log: they run their own outreach and see every touch, so no service is needed.
- Offer Comparison: if an offer comes, the real dollar number behind each letter.

**Objection and honest answer.** "I already got burned. Why trust you?" Honest answer: we do not recruit or place athletes and nobody here contacts your kid. We sell tools you run yourself, and the free ones come first. We cannot tell you your service was a scam or get your money back.

**What we must not claim.** That a given service is fraud. That a refund is owed. Anything legal: cancellation terms vary by contract and this site gives education, not legal advice. That we can place the athlete where the service failed.

**How to measure.** One number: share of Red Flags requests who open the checklist and then start /access or the Contact Log within 14 days. Event: `redflags_delivered` then `access_start`.

---

## Buyer 4: High-Academic D3 / Ivy / Merit-Aid Family

**Who and their moment.** Strong student, often swim, tennis, lacrosse or golf. Interested in early action with coach support, and how athletic and academic aid stack. In their words (inference): "Do we get athletic money at all? How does a coach 'support' an application?"

**Path**
1. Entry: search ("D3 athletic scholarship", "Ivy recruiting early action"). `live` (/answers/does-d3-offer-athletic-scholarships).
2. Landing: /playbooks/d3-academic-aid-first. `live`. Aha: the aid is academic and need-based first, and that changes the plan.
3. Next: /math (roster math). `live`. Then /answers/does-d3-offer-athletic-scholarships. `live`. Then /playbooks/offer-and-signing. `live`.
4. First ask (email): "Get the aid stacking worksheet." `gap`. No worksheet exists. Propose /tools/aid-stack: athletic and academic aid, net price per school, side by side. (Offer Comparison already holds this shape.)
5. Offer: Offer Comparison & Negotiation Toolkit ($29, BUILT). Strongest fit for this buyer. Page is a notify-me shell: `needs-page`.
6. Purchase: Sideline $149/yr, since this family tracks several schools across a full year (inference). Checkout `gap`.
7. After: visit planning. Spend note: highest household spend band (Aspen Project Play 2024: $100K+ households spend about $1,591/yr on youth sports vs $604 under $50K). Spend on visits that matter, not volume. A visit-priority page is `gap`.

**What they should get out of it**
- Offer Comparison: a grid for up to six schools showing scholarship %, fees, room, books, stipend, and 12 questions to ask each coach after the offer.
- The worked example: two offers, one family, how they chose.
- /math: the number of roster spots and where an academic profile sits against them.

**Objection and honest answer.** "D3 has no athletic scholarships, so what is there to buy?" Honest answer: correct, D3 does not give athletic scholarships. The tool is for reading academic aid and any other offer correctly, so the comparison is on net price.

**What we must not claim.** That a coach will support an application. That any school will admit the athlete. That athletic and academic aid will stack at any given school. Rules differ by school and division.

**How to measure.** One number: share of /playbooks/d3-academic-aid-first readers who reach /answers/does-d3-offer-athletic-scholarships and then /playbooks/offer-and-signing. Event: `playbook_chain_complete`.

---

## Buyer 5: Clock/Mark Sport (Track, XC, Swim)

**Who and their moment.** Parent of a sprinter, distance runner or swimmer. The numbers are public. In their words (inference): "Her times are good. Does anyone see them? Do we need a highlight video?"

**Path**
1. Entry: search ("when can track coaches contact athletes"). `live` (/answers/when-can-track-coaches-contact-athletes).
2. Landing: /rules/track/2029. `live`. Aha: the contact rules for their sport and class year, in one view.
3. Next: /playbooks/track-field-marks. `live`. The lever is a verified mark at a meet coaches use, a clear list, and the right email, not a flashy video.
4. Tool: /access for the list and the email. `live`.
5. Swim: the same path with a swim rules view. A swim playbook does not exist. `needs-page`: /playbooks/swim-times, covering verified times, meets coaches read, and the email. Track and XC share the track playbook. The swimming story is /athlete/composite-swim. `live`.
6. First ask (email): save the list and get the meet calendar reminder. `needs-page` (reminders not built).
7. Offer: Season & Film Planner ($19, BUILT) for the season grid and per-sport stat prompts. It is not a film-first product, so we pitch it as a season and marks tracker. First Contact Pack ($9, PROPOSED) for the email. Pages are notify-me shells: `needs-page`.
8. Purchase: Pathway $99 one-year. Spend note: Aspen Project Play 2024 average for track about $191, swimming about $786. Sideline $149 is below the swim average and below the 'all sports' bands but far above the track average (inference from the two averages), so the track price story needs care.
9. After: a meet-result log. `gap`.

**What they should get out of it**
- Season & Film Planner: a season grid with windows marked, and the stats a coach in their sport reads.
- A list of schools at the right level for their mark, and the correct email to send.

**Objection and honest answer.** "My kid's times speak for themselves. Why pay?" Honest answer: the times do speak. What the paid tools save is the search and the follow-through. Track averages about $191 a year in youth spend (Aspen Project Play 2024), so the site should stay at the low end of the price ladder for them.

**What we must not claim.** That a time guarantees a look. That a swim time meets any specific school's standard unless the standard is shown from a source. That film replaces a verified mark.

**How to measure.** One number: share of /rules/track/2029 visitors who start /access. Event: `access_start` with `source_route`.

---

## Buyer 6: Emerging Sport or JUCO/NAIA Transfer Path

**Who and their moment.** Parent of a girls' flag football player, a women's wrestler, or an athlete heading JUCO then transfer. Few playbooks exist. In their words (inference): "Nobody around us has done this. Is there even a college path?"

**Path**
1. Entry: search ("girls flag football college", "JUCO to D1"), a parent group. `live` for landings.
2. Landing: /emerging-sports. `live`. Aha: yes there is a college path, and it is new.
3. Next: /playbooks/juco-to-d1, then /playbooks/walk-on. `live`.
4. Then: /start, then /playbooks. `live`.
5. First ask (email): "tell me when my sport's rules page opens." `needs-page`. Capture exists, but it is not tied to a sport watchlist.
6. Offer: Contact Log ($0) for the new, thin field where every coach touch counts. Offer Comparison ($29) for transfer offers. First Contact Pack ($9, PROPOSED). All `needs-page`.
7. Purchase: Pathway $99 one-year, fits the short window of a JUCO year (inference). Checkout `gap`.
8. After: transfer-portal and credit-transfer checklist. `gap`.

**What they should get out of it**
- /emerging-sports: a plain list of which sports have a pathway and what is known.
- JUCO playbook: the sequence from JUCO to a four-year program.
- Contact Log: proof of every conversation in a field where rules are still being written.

**Objection and honest answer.** "Is this even a real path?" Honest answer: we show what is known and label what is not. The field is new and few playbooks exist. We will not invent a pathway.

**What we must not claim.** That an emerging sport has scholarships at any school. That a JUCO transfer is easier than a freshman recruit. That credits will transfer.

**How to measure.** One number: share of /emerging-sports visitors who leave an email with a sport selected. Event: `capture_submit` with `sport`.

---

## The funnel spine (shared by all six)

| Stage | Handoff | What the reader gives | What we give | Status / blocker |
|---|---|---|---|---|
| 1. Unidentified reader | Search, group post or link lands on a free page | Attention | A true answer to one rule question (/answers, /playbooks, /calendar) | `live` |
| 2. Email | Reader leaves an email, sport and class year | Email, sport, class year | A free tool delivered (Red Flags, Contact Log, free guide) | Capture `live`. Delivery `needs-page`: every /tools page is a notify-me shell and no email product sends. Drafts only in funnel/emails/DRAFTS.md. No monitored support mailbox. |
| 3. Paying member | Reader buys Sideline $149 or Pathway $99, or a single tool | Money | Tools, playbooks, yearly calendar rebuild | Blocked: checkout is OFF behind a flag (503 in preview). Deliberate readiness gate. |
| 4. Renewed member | Member comes back for the next season | Second payment | Rebuilt yearly calendar, new class year rules | `gap`: no renewal email, no rebuild notice. |
| 5. Referring member | Member sends another parent | A name and a link | Credit or extension (inference: not decided) | `gap`: no referral link, no reward, no tracking. |

Event order to instrument across the spine: `page_view` -> `capture_submit` -> `free_tool_delivered` -> `checkout_start` -> `purchase` -> `renewal` -> `referral_sent`.

## Offering-to-buyer value matrix

Buyers: B1 9th/10th Planner, B2 Late-Start Panic, B3 Burned, B4 High-Academic, B5 Clock/Mark, B6 Emerging/JUCO. "—" means not for them. Deliverable status in brackets.

| Offering | B1 | B2 | B3 | B4 | B5 | B6 |
|---|---|---|---|---|---|---|
| Contact Log, $0 [BUILT] | Ready before the first touch happens | Who was emailed and when, with 10-day follow-up | Take the work back and see every touch | One grid for several schools across the year | Track which coaches saw which mark | Record every touch in a thin field |
| Red Flags, $0 [BUILT] | — | Screen camps and services before paying | The 40 signs, and what to ask instead | Check programs that oversell aid | — | Check programs that oversell a new sport |
| Offer Comparison, $29 [BUILT] | — | Compare the offers that do arrive | If an offer comes, see the real dollar number | Net price per school, 12 post-offer questions | — | Compare transfer offers |
| NIL Ledger Starter, $29 [BUILT] | — | — | — | — | — | — |
| NIL Tax Tracker, $19 [BUILT] | — | — | — | — | — | — |
| Local NIL Deal Kit, $19 [BUILT] | — | — | — | — | — | — |
| Season & Film Planner, $19 [BUILT] | Season grid with windows marked | Plan film nights fast | — | — | Season grid and sport stat prompts (not film-first) | — |
| Career Transition Workbook, $19 [BUILT] | — | — | — | Plan from junior year for the many athletes who do not play past college (the workbook's own 98% framing) | — | — |
| First Contact Pack, $9 [PROPOSED] | — | 12 emails by moment | Re-start outreach with the right email | — | The right email for a mark | 12 emails for a new field |
| Full Bundle, $79 [PROPOSED] | — | Everything once | — | — | — | — |
| Sideline, $149/yr | — | — | — | Everything, all year, several schools | Everything, but see price note | — |
| Pathway, $99 one-year | — | One season of need | One season, after a loss | — | One season | One JUCO or transfer year |
| Free interactive pages | /start, /calendar, /personalize | /access, /math | /recruitiq, /compare | /math, /compare | /rules, /access | /emerging-sports, /start |

Notes. The three NIL products are for athletes who are already in college or at least have a likely NIL deal; none of the six buyers is there yet, so they are left empty on purpose. Nothing in this table claims a NIL benefit for a high-school buyer. (inference: the Career Transition Workbook is the only post-roster product that might touch B4, and only for the student's own plan.)

## The $149 justification line, by buyer

What each buyer must believe before paying Sideline $149 (or Pathway $99). Reference points: parents in the Social Fetch parent-problem sample report paying $1,500-$4,200 (up to about $4K plus monthly fees) to a paid service. Aspen Project Play 2024 youth-sports spend: $100K+ households about $1,591/yr vs $604 under $50K; track about $191, swimming about $786.

- B1: "Nothing here needs paying for yet. When I start, $149 for a full year is less than one showcase, not more." They should NOT buy Sideline now. (inference)
- B2: "This is the cheap, verified version of what a panic service charges for. I run it myself, and the cost is a fraction of $1,500-$4,200." Pathway $99 fits.
- B3: "I will not repeat what I paid. This is a tool I run, not a service that runs me, and I can see every touch." Pathway $99 or free tools first.
- B4: "The comparison grid pays for itself the first time it shows a net price that differs from the letter." Sideline $149 fits.
- B5: "Track averages about $191 a year in youth spend (Aspen Project Play 2024), so $149 is a lot. It needs to be Pathway $99 or per-tool." Price story needs care.
- B6: "There is no other playbook for my sport. $99 for one transition year is fair, and the site is honest about what is not known." Pathway $99 fits.

## Sequenced build list

Smallest ordered list so no buyer's path hits a `needs-page` or `gap`.

1. Publish the 8 BUILT deliverables behind their /tools pages (turn the notify-me shells into real pages with a free download or a paid gate). Unblocks: every offer step for all six buyers.
2. Free-tool email delivery: send the Red Flags and Contact Log by email after capture, from a real sender, with a monitored support mailbox published on /account. Unblocks: stage 2 of the spine, B3 first ask, B1 first ask.
3. Turn checkout on after steps 1 and 2 (the readiness gate), with Sideline $149, Pathway $99 and single-tool purchase. Unblocks: every purchase step.
4. Write and publish The First Contact Pack ($9). Unblocks: B2 offer, B3 restart, B5 email, B6 email.
5. Welcome and weekly emails (from funnel/emails/DRAFTS.md): Sunday Contact Log review, 10-day follow-up reminder, yearly calendar rebuild. Unblocks: B1 after, B2 after, spine stage 4.
6. /tools/budget-reallocator and a contract-check education page. Unblocks: B3 money and after steps.
7. /playbooks/swim-times and a swim rules view. Unblocks: B5 swim path.
8. Save-by-email on /access (30-school list, .ics). Unblocks: B2 first ask, B5 first ask.
9. /tools/aid-stack worksheet and a visit-priority page. Unblocks: B4 first ask and after.
10. Sport watchlist on capture, transfer checklist. Unblocks: B6 first ask and after.
11. Referral link and tracking. Unblocks: spine stage 5.
12. Event instrumentation for the six numbers above. Unblocks: all measurement.
