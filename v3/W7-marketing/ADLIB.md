# ADLIB: competitor ad teardown (Meta Ad Library via Social Fetch)
Pulled 2026-11-06 (US). Sources: raw/ads_*.json (prior run) and raw/ads2_*.json (re-pulled with status=all because the first run's status value was rejected). Read-only. Ad copy below is a paraphrase or a short quote of a COMPANY's public ad, not a private person.

**Caveat on the "30":** the endpoint returns at most 30 ads per page, so 30 means "30 or more", not an exact count. `startedAt` is Meta's first-delivery date. Meta does not show spend or impressions for non-political US ads (null in every row). Long run time is only a PROXY for "this ad pays".

## 1. Who is running ads right now

|Advertiser|Ads returned|Active|Oldest start|Formats|CTAs|Landing pages|
|-|-|-|-|-|-|-|
|NCSA|30 (cap)|30|2025-07-29|DCO 30 (mostly video DCO)|Sign up 18, Learn more 12|ncsasports.org/join/get-recruited; /join/football, /softball, /baseball, /basketball, /soccer|
|Richie Contartesi / Next Play (gonextplay.com)|30 (cap)|30|2026-04-21|Video 19, Image 10, DCO 1|Learn more 13, none (comment-keyword) 9, See details 8|gonextplay.com/free-training-highlights, /application-ads, /free, /evaluation|
|Full Ride University|1|1|2026-11-01|DCO|Download|fb.me lead form (free 2026-27 football calendar)|
|SportsRecruits|1|1|2026-11-02|DCO|See details|fb.me (club-director positioning)|
|FieldLevel, Keith Mondillo, Recruit University|0|0|-|-|-|No ads in the Library on 2026-11-06|
|CaptainU, Rivals|not resolved|-|-|-|-|Name search returned unrelated pages (Captain D's, Football Rivals); no ID pulled|

Keyword searches (adq_*: AAU basketball, baseball showcase, softball, track, volleyball, wrestling, athletic scholarship, recruiting service, get recruited, college recruiting parents): **all failed or came back empty** (bad status parameter or empty body). There is no keyword ad search tool in Social Fetch; the only ad tool is per-page. So sport-level ad density is UNMEASURED. Do not quote it.

## 2. Longest-running ads (profitability proxy)

1. **NCSA, running since 2025-07-29 (~15 months, still active 2026-11-06).** 18 distinct creatives under one DCO campaign family. Evergreen lines:
   - "Gain Exposure. Get Recruited." (headline) / "largest recruiting service in the U.S." (authority)
   - "has helped over 300,000 student-athletes get recruited" (their claim, not ours)
   - "network of 40,000+ college coaches"
   - "Get a FREE recruiting assessment today" / "Create a free profile"
   - Sport-split camp-search ads: "Find the Perfect Baseball Camp", "Find Football Camps Near You", softball, basketball, soccer. Free tool as lead magnet, routed to a sport-specific /join page.
   - Expert-video ads: "Keep watching to learn from [a named IMG Academy coach]".
   - Parent call-out: "Attention parents of high school student-athletes!"
2. **Contartesi / Next Play, 9 creatives since 2026-04-21 (~6.5 months, active).** All organic-style talking-head video, no link CTA, comment-keyword ("Comment the word 'Evaluate'", "Comment WORKSHOP"). Topics: "How to earn a football scholarship in 2026", camp choice fear ("Don't let your son go to a camp where he can't get an offer"), a 50-60 school target list, "what to post on X", "'Let's stay in touch' is coach speak for 'I'm still deciding'", "D1 or nothing mindset is costing athletes".
3. Newer Next Play wave (2026-09-12 to 2026-10-27): direct-response, all open with **"Parents of High School Football Players in the 2027/28 Classes..."**, then a pain stack ("paying for camps, private training, travel, gear, but still no traction"), then a free training ("D1-style highlights in 60 minutes"), an application, or a paid "D1 evaluation" by a recruiting director.

## 3. Pattern teardown

|Element|NCSA|Next Play|Full Ride U / SportsRecruits|What we take|
|-|-|-|-|-|
|Hook|Aspiration ("If your dream is to play college sports")|Parent call-out by sport + class year, then a pain stack|Utility ("Free 2026-27 football recruiting calendar") / simplicity|Call out parent + sport + grade in line 1; lead with a dated, checkable fact|
|Offer|Free profile / free assessment (sales call follows; see PROBLEMS #3)|Free workshop or training -> application -> evaluation|Free calendar download (lead form)|Free /start page or free calendar PDF, no call, no account|
|Proof|Big counts (300K athletes, 40K coaches)|Founder story (D1 at 5'7"), "2,500+ families" (their bio claim)|None|Bylaw citations and sourced stories; no counts we can't prove|
|Format|Video DCO, camp-tool static|Talking-head reels, then static image with long copy|Static DCO|Talking-head or text-on-screen reel + one static calendar image|
|CTA|Sign up / Learn more|Comment keyword, Learn more|Download|"Get the free calendar" / "See your grade's steps"|
|Landing|Sport-specific join page|Sport-specific funnel pages|Facebook lead form|Sport/grade page on recruiting-calendar.vercel.app, no form wall for the free page|

## 4. Gaps we can occupy
- **Full Ride University started a free football recruiting-calendar ad on 2026-11-01.** That is our exact free offer. We differ on proof (every date cites its bylaw) and on scope (all sports, not football only). Head-to-head on football calendar ads is now contested; lead with sports they ignore (volleyball, softball, wrestling, girls flag, track).
- No one advertises to **girls' sports parents** in the pulls: NCSA's sport splits are baseball, football, softball, basketball, soccer; Next Play is football-only ("help your son").
- No one advertises **"is a recruiting service worth it?"** (PROBLEMS #3, ~22 mentions). NCSA can't; Next Play sells a service. A neutral compare page is open space (https://recruiting-calendar.vercel.app/compare/).
- No advertiser pulled offers a **price under $20**. A $9 playbook is a real contrast to "free assessment then a sales call".

## 5. What NOT to copy
- Big counts we cannot source (300K, 40K coaches, 2,500 families).
- "Earn a scholarship" / "get an offer" outcome promises; fear of a camp "costing him everything".
- Comment-keyword DM funnels: they need someone to reply in DMs, and our rule is no posting/messaging without approval.
