# ACCESS: how families reach college coaches (buyer jobs, gaps, features, providers, MVP, metrics)
Lane W7-access. Written 2026-11-06 (MT). Read-only research: no social actions, no minors' data, no outreach.
Status tags: **FACT** = read on a cited public page or saved raw file; **EVIDENCED** = repeated in saved W6/W7 evidence; **HYPOTHESIS** = our inference, untested.
Local evidence paths are relative to `~/Developer/recruiting-calendar/v3/`. Parent/athlete wording is paraphrased; no usernames.

## 0. Bottom line
- **The Commit Book cannot sell "access."** It does not contact coaches, place athletes or promise introductions (site footer: "We do not recruit or place athletes, and nobody here contacts your kid"). The honest lane is: **make the family's own access work** (rules, scripts, profile, video link, questionnaire, tracker), and **route to people who can vouch** (HS/club coach).
- Parents want access ("get a reply from the coaches who fit us" is the stated job, TEN-LAYERS #4 L8, INFERRED). The loudest evidence is that they are **burned by paid access** (NCSA cost/cancel, W6 problem #3, ~22 mentions, directional).
- Highest-confidence build: a **free-to-low-price "Coach Contact Kit"**: rule-gated send dates by sport/division, questionnaire finder checklist, athlete-voice email/DM scripts, highlight-link checker, and a follow-up log. All of it is education and tooling the family runs itself.

## 1. Buyer jobs (who is hiring what)
| # | Buyer | Job to be done | Evidence | Status |
|---|---|---|---|---|
| J1 | Parent (project manager) | "Tell me what to say, to whom, on which channel, and when I'm allowed to expect an answer." | W6 PROBLEMS #4 (~14), #5 (~12); TEN-LAYERS #4, #5 | EVIDENCED |
| J2 | Parent | "Get what a service gives (timeline, organization) without the price or pressure." | TEN-LAYERS #3 L8 (EVIDENCED via `W7-segments/raw/fbc_3051766708336417.json`, a parent liked the contact timeline) | EVIDENCED |
| J3 | Athlete (14-18; we market to the parent) | "Make my video and profile something a coach opens and finishes." | W6 PROBLEMS #8 (~9); video is "the #1 coach filter" | EVIDENCED |
| J4 | Parent/athlete | "Find the coach's questionnaire, fill it right, and know it is not an offer." | Public: NCSA questionnaire guide; D1 questionnaire rules (section 3). In saved evidence only as a sub-point of #4 | FACT (rules) / HYPOTHESIS (demand size) |
| J5 | Parent of athlete with unhelpful HS/club coach | "Get an adult coach to vouch for us or make one call." | W6 PROBLEMS #9 (~6) | EVIDENCED (small) |
| J6 | Parent in no-network family (single parent, first-gen) | "Do this without knowing anyone." | W6 PROBLEMS #12 (~4) | EVIDENCED (small) |
| J7 | HS/club coach or AD | "Stop answering the same contact-date question 40 times a season; hand families one sheet." | Product page `site/coaches/index.html` ($299/yr program plan, "proposed"); demand not yet validated | HYPOTHESIS |

## 2. What happens today (current facts about channels)
### 2a. Coach contact: who may start, and when (FACT, but sport-specific)
- Families can always write first. Per one admissions-advisory summary, nothing in the NCAA manual limits when a prospect may write a coach, fill in a questionnaire, or attend a camp; the dates limit what the coach may send or say back. https://orieladmissions.com/when-can-college-coaches-contact-you/ (published 2026-09-23). The NCAA's own page says communication rules "vary by division and grade level." https://www.ncaa.org/eligibility-center/recruiting (2026-05-15)
- **Dates differ by sport and are described differently across sources.** Examples read 2026-11-06:
  - Most D1 sports: June 15 after sophomore year for calls/texts/DMs (https://www.pathley.ai/blog-posts/ncaa-recruiting-rules-explained; LSU compliance https://www.compliance.lsu.edu/recruiting-1 lists June 15 for most sports, August 1 baseball, June 1 women's basketball, September 1 softball).
  - Some D1 sports differ: SportsRecruits says D1 women's lacrosse opens September 1 of junior year at noon ET, and that for the Class of 2028 the first day is **September 9, 2026, 7 a.m. ET** (a listing for a sport whose page we did not match; verify per sport). https://sportsrecruits.com/resources/contacting-college-coaches/ncaa-contact-periods (2026-10-26), https://sportsrecruits.com/resources/contacting-college-coaches/ncaa-rules-and-regulations (2026-11-03).
  - D2: coaches can call/text/email any time; D3: almost no timing limits (https://www.pathley.ai/blog-posts/ncaa-recruiting-rules-explained). **NAIA has no recruiting calendar** and no limit on communication (https://www.naia.org/why-naia/recruiting).
- **CONFLICT FLAG:** one older blog says DMs are allowed only after September 1 of junior year (https://usabdevelops.com/page/5015/blog/17918/phone-calls-and-electronic-communication, undated); 2026 sources say June 15 for most D1 sports. Do not publish any date unless it is read from the NCAA sport calendar and tied to the bylaw, as `site/data.js` already does. Source of truth: https://www.ncaa.org/eligibility-center/recruiting and the sport PDFs linked there (e.g. 2026-27 D1 baseball calendar https://ncaaorg.s3.amazonaws.com/compliance/recruiting/calendar/2026-27/2026-27D1Rec_MBARecruitingCalendar.pdf).
- **What a coach may do on social early (HYPOTHESIS-GRADE, from one vendor summary):** follow and like are generally allowed, public comments/tags and recruiting DMs are not until the class is open. https://www.pathley.ai/blog-posts/ncaa-recruiting-rules-explained. Verify against NCAA interpretations before we state it as a rule.
- Athlete-initiated calls are allowed at any time, but a coach who misses the call may not call back before the permitted date (NCAA rule as relayed by https://captainu.com/how-your-high-school-coaches-can-help-your-recruiting/, 2020; re-verify).
- Silence is often the rule, not rejection: TEN-LAYERS #4 L5 (EVIDENCED, `W7-segments/raw/ws5.json`). Coaches also say "ask him directly if he's recruiting you" after a camp (coach post, https://x.com/coachdrew94/status/1849114486369554727, 2024-10-23).

### 2b. X and social profiles
- Coaches (not parents) dominate X on this topic; recurring PSA: do not pay recruiting services, coaches delete their emails (e.g. https://x.com/CoachHubb2/status/1433139050588766217, 2021; https://x.com/MRittCGS/status/1898868428074570065, 2025-03-09, a $4,000 football package criticized; https://x.com/CoachRoland77/status/1732802004483768537, 2023). EVIDENCED in `W6-problems/raw/x1.json`, `x2.json`.
- Coach-voiced norms, as opinion not rule: athlete should write and send, parent should organize (https://x.com/diamondconnbsb/status/2117738960784912856, 2026-11-03; https://x.com/CoachCarm/status/2064370062811697629, 2026-06-09: a parent speaking for the athlete is a "red flag").
- A competitor-ish product founder posts that he used to charge $3,000, "coaches want to hear from the athlete, not from a middleman" (https://x.com/rekrut_app/status/2118516001117762039, 2026-11-06). Treat as a signal that DIY-platform positioning is already being contested.
- **Our rule for this product:** teach the profile audit and the "what not to post" list. We do not post, follow, DM or run any family's account. The existing playbook already covers a social audit (`site/playbooks/highlight-reel-social`, $15).
- Minors' safety: SafeSport-style rules bar private one-on-one electronic contact between adults and minor athletes except in set conditions (https://nfhs.org/stories/rules-guidelines-on-communication-with-minor-athletes, 2025-11-05). That is directed at coaches, but it means a family-visible channel (parent copied) is the safe default we should teach. HYPOTHESIS that this helps parents' comfort; the rule text is FACT.

### 2c. Highlight hosting
- Consensus across vendor and club guidance: host on a link coaches can click (YouTube, Hudl, Vimeo), 3-5 minutes, best clips in the first 30 seconds, no attachments. https://www.hudl.com/support/athlete-recruiting/guides/how-to-get-noticed; https://www.ncsasports.org/college-recruiting-video ("12 times more likely to be viewed" is NCSA's own claim; do not repeat as fact); https://www.coachup.com/nation/articles/the-dos-donts-of-highlight-reels (2026-06-16).
- **Failure mode we can fix:** private/unreachable links. Hudl share links must be public, test in a private window (https://productiverecruit.com/docs/profile/videos); YouTube "unlisted" works with the link, "private" does not (https://captainu.com/your-highlights-deserve-to-be-seen-how-to-upload-your-recruiting-video-to-youtube/, 2026-11-03). W6 saw parents hitting Vimeo link trouble (PROBLEMS #8). A link checker is a real, small, deliverable feature.
- **Hudl specifics:** an athlete needs a Hudl team that buys Hudl; athletes must opt in to recruiting to be visible to registered recruiters; profiles can be shared to .edu/.ca addresses; recruiters log in with a free account; highlights may show ads (https://www.hudl.com/parents-fans-faq; https://support.hudl.com/s/article/recruiting-faq-hudl-v3, 2026-02-02; https://support.hudl.com/s/article/share-your-profile-with-a-recruiter-hudl-v3, 2026-01-21). So Hudl is not an open family tool; we should integrate by link only, not scrape.
- **YouTube "Made for Kids":** the setting disables comments, notifications and personalized ads (https://support.google.com/youtube/answer/9632097). Teen recruiting reels are not child-directed, so the checklist should say choose "No, not made for kids" and unlisted/public as appropriate. Do not give legal advice; link YouTube's help page.
- Hosting does not equal hosting-by-us. **Recommendation: do not host athlete video.** Hosting minors' video creates privacy, COPPA-adjacent and moderation duties we do not need (section 7).

### 2d. Questionnaires
- A questionnaire is a form on a program's site that a prospect fills out; very common, usually asks for video link, NCAA ID (D1/D2), stats, social links. https://www.ncsasports.org/recruiting/managing-recruiting-process/recruiting-questionnaires (vendor page).
- D1 rules in NCAA compliance material: questionnaires may be provided to a prospect at any time, but one sent before the permissible date for general correspondence may not include recruiting language, general program information or facility images with descriptions, and may not have a detachable portion (NCAA Division I Bylaw 13 hot-topics deck, 2021: https://ncaaorg.s3.amazonaws.com/compliance/rrs/2021/presentations/d1/Division_I_Bylaw_13_Hot_Topics--STATIC.pdf; UGA compliance 2025-09-12: https://compliance.sports.uga.edu/coaches-staff/recruiting/recruiting-materials). One vendor page says a 2024 D1 change allows questionnaires to be sent only after the first permissible date (https://www.ncsasports.org/recruiting/managing-recruiting-process/recruiting-questionnaires); a school page (VCU) says the same. **Sources conflict by date; re-verify before stating any rule.**
- Real examples: Brown posts per-sport questionnaires via ARMS software (https://brownbears.com/sports/2025/10/30/recruiting-questionnaires); a D2/D3-style form runs on Front Rush (https://apply.unwsp.edu/register/form?id=a6628bf5-c8fc-45c4-a4eb-9fa24294356b). These are public pages; we link, we never submit for a family.
- A filled questionnaire is **interest data to the program, not an offer or evidence of interest from the coach.** Parents may confuse this (HYPOTHESIS; the NCSA guide frames it as a standard step, not a guarantee).

### 2e. Introductions
- Legitimate paths found in public sources: the HS/club coach makes an introduction or a scheduled call (https://captainu.com/how-your-high-school-coaches-can-help-your-recruiting/), the coach sends film through team software, or a parent/athlete asks a coach for a reference. EVIDENCED as a gap: W6 problem #9 (HS/club coach won't help).
- NCAA: boosters generally may not contact prospects for recruiting purposes (https://www.ncaa.org/eligibility-center/recruiting). So "a friend of the program" introductions are limited at the institution end; the safe version is the athlete's own coach or an official camp contact.
- **We cannot deliver introductions.** The deliverable is a **"ask your coach" kit**: a one-page request the athlete hands the HS/club coach (target list, film link, 3 sentences to say on a call), plus a polite reference-request script. Delivered as a document, not a relationship.

### 2f. Networks and platforms (what exists, what we are not)
- NCSA (free profile; paid plans not publicly priced; BBB profile snippet read 2026-11-06: 123 complaints in the last 3 years, 37 in the last 12 months (a different BBB page via RawRecruit, 2026-09-24, showed 124; counts move), https://www.bbb.org/us/fl/bradenton/profile/athletic-organizations/national-collegiate-scouting-association-llc-0653-90457895; NCSA is the NAIA's official North American recruiting services partner, https://www.naia.org/findyourpath/highschool/index). SportsRecruits joined IMG Academy (NCSA's parent) in 2025 (https://rawrecruit.io/resources/compare/best-recruiting-platforms, 2026-03-01).
- Facebook parent groups are where parents ask; the largest ban recruiting services, outside links and school-specific questions (W6 GROUPS rows 1, 5, 15). EVIDENCED.

## 3. Unmet needs (gap between the jobs and what exists)
| # | Unmet need | Why existing options fail | Evidence | Status |
|---|---|---|---|---|
| U1 | **Rule-gated send dates**: "when may this coach answer, for our sport and division?" in one place, with the bylaw. | Sources disagree by sport/date; services say "start freshman year"; groups ban school-specific questions. | W6 #5; sources above conflict (section 2a) | EVIDENCED |
| U2 | **Neutral, no-pitch contact scripts in the athlete's voice** with a follow-up cadence. | Templates are generic; parent-written mail is a red flag to coaches; paid blasts are "templated email" (https://x.com/playgolfcollege/status/2020525684502778103, 2026-02-08). | W6 #4; TEN-LAYERS #4 | EVIDENCED |
| U3 | **A working video link** (public, mobile, correct privacy, identified athlete, first 30 seconds). | Guidance is scattered across vendors that each push their own host. | W6 #8; hosting guidance above | EVIDENCED (demand) / FACT (guidance) |
| U4 | **Where is the questionnaire, and did I fill it right?** | Questionnaires live on 100s of school sites on different software (ARMS, Front Rush, custom); no neutral index for families. | Public examples only; demand not measured | HYPOTHESIS |
| U5 | **"Service vs DIY" with cancel steps**, because parents buy access out of panic. | NCSA pricing is unpublished; BBB complaints cluster on cancellation and sales pressure. | W6 #3; BBB link 2f | EVIDENCED |
| U6 | **An "ask my coach" one-pager** for families with weak HS/club support. | Nothing structured exists; creators say "ask your coach." | W6 #9 (~6) | EVIDENCED (small) |
| U7 | **Progress proof**: who did I contact, what did they say, what is the next legal date. | Spreadsheets; paid platforms' dashboards require a plan. | TEN-LAYERS #4 L10, #1 L10 (INFERRED metrics) | HYPOTHESIS |

## 4. Features (map to existing Commit Book products; effort S/M/L)
| Feature | Job/Need | Deliver as | Effort | Already have? |
|---|---|---|---|---|
| **Send-date finder** (sport x division x class year, bylaw link, NAIA "no calendar" note, D2/D3 "any time") | J1, U1 | Web page + email reminders | S (data exists) | Yes: `site/calendar/`, `site/answers/when-can-college-coaches-contact-my-kid/` |
| **Questionnaire checklist + finder links**: what to have ready (NCAA ID for D1/D2, video link, transcript, coach contact), how to find a program's form; **links to public forms only**, no auto-submit | J4, U4 | PDF checklist + curated links per sport page | S | No |
| **Email/DM scripts by sport + 4-touch cadence**, athlete's voice, parent-copied, never sent from our tools | J1, U2 | Playbook add-on | M | Partial: `site/playbooks/highlight-reel-social` ($15) |
| **Highlight link checker** (paste a URL: is it public, unlisted not private, mobile-playable, does the title include name/class/sport?). Read-only HTTP fetch of the family's own link. | J3, U3 | Free web tool | S-M | No |
| **Follow log / contact tracker** (manual entry; reply and date columns) | U7 | Template (Sheet/PDF) + web later | S | Partial: "Follow log" in playbook |
| **"Ask your coach" kit** (request one-pager, target list sheet, reference request script) | J5, U6 | PDF | S | No |
| **Service vs DIY compare + cancel guide** | J2, U5 | Page | S | Partial: `site/compare/` (cancel guide missing, per `W7-segments/SOLUTIONS.md`) |
| **Program seats for coaches** (rule sheet for the parent night) | J7 | Existing $299/yr page | S | Yes (proposed, unvalidated) |

**Explicitly not features (cannot deliver, do not imply):** introductions to college coaches; guaranteed replies, views or offers; posting/following/messaging on a family's accounts; submitting questionnaires for a family; hosting athlete video; a searchable athlete database; "access to 50,000 coaches."

## 5. Providers and what to do with each
| Provider | What it is (FACT, with source) | Pricing seen | Our stance |
|---|---|---|---|
| NCSA | Network + paid coaching tiers (Free, Champion, Elite, MVP, MVP+); prices "by call" https://www.ncsasports.org/who-is-ncsa/what-does-ncsa-do/what-does-ncsa-cost-how-much | Unpublished. Third-party reports vary: $250-$2,100 (Scholarships360 via RawRecruit), $1,320-$4,200 (a sales-call quote, RawRecruit), "$2,000-$6,000+" (NextCommit, a competitor; RawRecruit says it found no dated source). https://rawrecruit.io/resources/compare/how-much-do-college-recruiting-services-cost (2026-09-25). Parents in W6 report up to ~$4K. | Competitor. Compare honestly; **do not state a price as NCSA's**. Cite "unpublished; families report ranges." |
| SportsRecruits (IMG Academy, 2025) | Free profile, unlimited video, highlight editor; Pro paid https://www.nextcommit.ai/blog/sportsrecruits-review (2026-09-30) | Pro unpublished; clubs/families report ~$99/mo or ~$399/yr, lacrosse/field hockey sources only | Competitor/neutral. Single-source pricing: label "reported." |
| CaptainU | Published plans https://captainu.com/athlete-plans/ (page dated 2026-08-18) | Bronze free; Silver $22.50/mo; Gold $39.95/mo; Platinum $199.95/mo | Closest honest competitor on price transparency. |
| FieldLevel | Athlete plans https://www.fieldlevel.com/app/account/plans/athletes ; help page https://support.fieldlevel.com/en/articles/2034971-explaining-fieldlevel-s-premium-plans | Free; Silver $29/mo ($278/yr); Gold $49/mo ($470/yr); Platinum $79/mo ($758/yr); coach "Prime" $99/yr (https://support.fieldlevel.com/en/articles/6308122-prime-and-prime-benefits) | Competitor; its "contact colleges" tiers are what we do not sell. |
| Hudl | Team video; athlete profile comes via team plan; recruiter sharing to .edu | School program plans $1,500-$4,000/program/yr (https://www.hudl.com/pricing/high-school, 2026-03-09). No family plan listed. | Integrate by link only. Not a partner yet. |
| Front Rush / ARMS / school forms | Software behind coach questionnaires (examples in 2d) | n/a to families | Link out only. |
| YouTube / Vimeo | Free link hosting | Free | Recommend; teach privacy settings. |
| NCAA / NAIA | Rules sources | n/a | Primary citation for every date. |

Other small tools (ScoutStreak, NextCommit, Pathley, RawRecruit, OfferSecured, ProductiveRecruit) publish their own pricing or comparisons. Their pages are marketing and often cite each other; use only as pointers, never as the sole source for a competitor's price. E.g. ScoutStreak's comparison lists NCSA at "$1,500-$4,200 (opaque)" https://www.scoutstreak.com/pricing (2026-10-06).

## 6. Pricing evidence (only what is supported)
- **Willingness-to-pay anchors for a DIY product, FACT:** published family prices of competitors: $0 to $22.50/mo (CaptainU) up to $79/mo (FieldLevel Platinum, $758/yr); SportsRecruits Pro reported at ~$399/yr; NCSA unpublished with reported four-figure totals.
- **Spend context, FACT:** families spend about $1,016/yr on their primary sport in 2024 (+46% vs 2019), with $1,591 for $100K+ income households (Aspen Project Play, n=1,848, https://www.aspeninstitute.org/wp-content/uploads/2025/06/National-Youth-Sports-Parent-Survey-FINAL.pdf), as already recorded in `W7-segments/MARKET.md`.
- **Our current price points:** $15 per playbook; $149/yr membership proposed ($99 founding) pending Mike's decision (`DECISIONS-FOR-MIKE.md` #1); $299/yr program plan "proposed" (`site/coaches/index.html`). **No evidence in this lane shows that parents will pay for a contact kit at any specific price.** Do not claim demand; treat the kit as bundled into the existing $15 playbook / membership and measure attach (section 8).
- **Evidence that "cheap and honest" is the wedge:** W6 problem #3 and `W7-segments/raw/fbc_2777699965737115.json`, `fbc_3051766708336417.json` (parents who paid report coaches ignoring service email, and refund refusal); BBB complaint themes (cancellation, sales pressure, loan-like payment plans) at the BBB link in 2f. These are complaint narratives on a public page, not proof of any company's overall record. NCSA disputes complaints in its own replies on that page.

## 7. Risks
1. **Promise risk (highest).** Any copy implying access, introductions, or replies repeats the claims that drew regulators: the New York AG settled with National Scouting Report in 2017 over unsubstantiated success claims (e.g. 90% of prospects receiving offers) https://ag.ny.gov/press-release/2017/ag-schneiderman-announces-settlement-major-college-athletic-scouting-company. FTC guidance on scholarship services: legitimate firms never guarantee scholarships (quoted at https://rawrecruit.io/resources/compare/is-ncsa-worth-it). **Mitigation:** language limited to "rules, scripts, checklists"; no outcome numbers; keep the site disclaimer.
2. **Wrong date in a rule = harm** (family emails too early or waits too long). Sources disagree (2a). **Mitigation:** every date cites the NCAA sport calendar and bylaw; show "last verified" date; "ask the school's compliance office" fallback.
3. **Minors.** Our buyer is the parent. Do not collect athlete names, photos, video, grades or social handles in the MVP. A link checker should check a URL the parent pastes and not store it (or store only the host and a pass/fail). COPPA applies to operators who collect personal data from under-13s; the amended rule's compliance date was April 22, 2026 (https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule; https://www.davispolk.com/insights/client-update/ftc-prioritizes-coppa-enforcement-new-compliance-obligations-take-effect). The site already states it does not knowingly collect from under-13s. Not legal advice; counsel review is already an open item (`DECISIONS-FOR-MIKE.md` #4).
4. **Social/automation.** Any feature that posts, DMs or follows for a family (or scrapes profiles) breaks platform terms and, if it contacts a coach, breaks our own "nobody contacts" promise. Out of scope.
5. **Scripts misused as spam.** Mass-DM scripts could worsen the coach-inbox problem; coaches say they delete service blasts. **Mitigation:** cap the template to a short target list (matches the "30-school list" idea in `SOLUTIONS.md`), teach personalization.
6. **Competitor ownership shifts.** NCSA and SportsRecruits now share an owner (IMG Academy, 2025) per RawRecruit; competitor facts go stale. **Mitigation:** date every fact; refresh the compare page.
7. **Vendor-pricing hearsay.** NCSA totals vary by source and some are competitor-authored. Quote ranges with the source or say "unpublished."
8. **Trust/operator visibility.** Jev gate flagged missing operator identity (`DECISIONS-FOR-MIKE.md` #5); a contact-kit offer raises the trust bar.

## 8. MVP (smallest thing worth shipping, all within existing promises)
**"Coach Contact Kit" v0 (S, 1-2 weeks of work; no new backend required for the PDF path).**
1. Send-date finder pointing at the existing calendar, adding a "families can write any time" line for each division, with last-verified date and NAIA "no calendar."
2. Questionnaire checklist page + 20 public example links across 5-6 sports (Brown/ARMS-type, Front Rush-type), clearly labeled as external.
3. Script pack (email, X DM, post-camp follow-up, "are you still recruiting me?" nudge), 4-touch cadence, parent-copied rule, built into the $15 Highlight Reel & Social playbook.
4. Highlight link checker v0: client-side checklist first (public/unlisted, 3-5 min, first-30-seconds, title format); fetch-based checker only after a counsel/privacy check.
5. "Ask your coach" one-pager.
**Gate before shipping copy:** s1gate/SlopMonster text gate, every rule cited, no outcome numbers, Mike's exact-text approval for anything outward (per standing rules).
**Out of MVP:** accounts for athletes, video hosting, coach database, messaging, introductions.

## 9. Metrics (what proves it works; none measured yet)
- Attach rate: share of playbook buyers who open/download the kit (HYPOTHESIS target set after first 30 days of real traffic).
- Activation: users who open the send-date finder for their sport and then the scripts within 7 days.
- Self-reported proof (survey email, optional): "emails sent in 14 days" and "first coach reply," mirrors TEN-LAYERS proof metrics (#1 L10, #4 L10). Report as self-reported; never publish reply-rate as an outcome claim.
- Link checker pass rate (aggregate only).
- Support/refund signal: refund requests and "what date" questions per 100 buyers (lower is better).
- Trust: share of visitors who reach /compare/ then /price/ (watch for the anti-service wedge).
- Do not report vanity "athletes helped" counts (BRIEF-V3 integrity rule 3: no fake member counts or outcomes).

## 10. Open questions / what this pass did NOT verify
- NCAA's own wording on questionnaire timing after the 2024 rule change (vendor and school pages conflict by date). Next step: read the current D1 manual bylaw 13.4.1 through https://web3.ncaa.org/lsdbi.
- Per-sport D1 dates for every sport (only examples checked). The site's `data.js` is the system of record.
- Whether families pay for a contact kit separately (no willingness-to-pay data in saved W6/W7 evidence).
- Questionnaire and "ask my coach" demand size (small samples; W6 counts are directional, hand-tagged, never publish as statistics).
- X DM etiquette beyond coach opinion; no social platform terms reviewed this pass.
- NCSA/SportsRecruits/FieldLevel plan features were read from third-party and vendor pages dated 2026-03 to 2026-10; re-read before putting any competitor fact on the site (the compare page rule: "every competitor fact comes from a public page we read on <date>").

## Sources of local evidence used
`W6-problems/PROBLEMS.md`, `W6-problems/GROUPS.md`, `W6-problems/raw/x1.json`, `x2.json`; `W7-segments/MARKET.md`, `TEN-LAYERS.md`, `SOLUTIONS.md`, `raw/ws*.json`, `raw/fbc_*.json`; `BRIEF-V3.md`; `DECISIONS-FOR-MIKE.md`; `site/coaches/index.html`, `site/compare/index.html`, `site/playbooks/highlight-reel-social/index.html`. No minors' names or comments were extracted into this file.
