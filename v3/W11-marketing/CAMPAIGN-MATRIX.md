# W11 CAMPAIGN-MATRIX: segments x stories x routes
Built 2026-11-06. **100% DRAFT. Nothing posted, launched, joined or bought.** Every creative needs Mike's OK on the exact text before any run. Source: `v3/W7-marketing/{ACCESS,ADLIB,STORIES,AD-PLAN,MARKETING}.json|md`. Machine-readable twin: `landing-page-map.json`.

## Route status (honest)
|Route|What it is|Live in `site/` today?|
|-|-|-|
|/start|Free recruiting steps by grade|Yes|
|/access|Access routes for families|Not yet (W10-access build exists)|
|/recruitiq|Readiness check|Not yet (W10-recruitiq)|
|/personalize|Personalized plan|Not yet (W10-personalization)|
|/segments|Sport/segment hub|Not yet|
|/emerging-sports|Girls wrestling, flag football|Not yet|
|/resources|Third-party Gumroad directory (McKinley Malbrough III)|Built in `site/resources/`, held for Mike's release|

Rule: no ad may point at a route that is not live. Until then the fallback landing is the AD-PLAN landing (`/start/`, `/calendar/`, `/compare/`, `/playbooks/...`, `/story/<slug>/`).

## The 6 buyer segments (paid-ad segments with drafted concepts)
|Segment|Ads|Stories carried|Hook (claim-safe)|Primary route|Secondary routes|/resources story filter|
|-|-|-|-|-|-|-|
|Football parents|F1 F2 F3|marpet, renfrow, composite-football|Every date a coach can contact your kid, with the rule number|/start|/personalize, /recruitiq, /resources|renfrow|
|Travel baseball/softball|S1 S2 S3|composite-softball, composite-baseball, groenewegen, pichardo|Check which showcases fit before the next one|/start|/personalize, /segments, /resources|groenewegen|
|Club volleyball|V1 V2 V3|composite-volleyball, lowe|The recruiting dates are different for your sport|/start|/personalize, /segments, /resources|lowe|
|Wrestling incl. girls|W1 W2|rodriguez, composite-wrestling|Women's wrestling is now an NCAA D-III championship sport|/emerging-sports|/start, /recruitiq, /resources|rodriguez|
|AAU basketball|L1|butler, white, coward, composite-wbasketball, pirosko|Late isn't over: an honest next 30 days|/access|/start, /recruitiq, /resources|butler|
|Late-start junior/senior|L1 L2 F2|marpet, butler, composite-baseball|The two dates that can cost eligibility ($9, no sales call)|/recruitiq|/personalize, /start, /resources|butler|

Small $50 tests: **G1 girls flag football** -> /emerging-sports (no story exists; program list is a sourcing gap, copy says "where to look"); **T1 track** -> /segments (rodenfels is HELD/noindex: use composite-sprinter in creative links until released). Not paid now: HS coaches/ADs, club directors, single-parent/first-gen (partnership or direct outreach only).

## Story arcs -> routes
|Arc|Stories|Route|Draft angle|
|-|-|-|-|
|1 We're late. Is it over?|marpet, butler, composite-baseball|/recruitiq then /personalize|Honest next 30 days|
|2 Nobody told us the dates|composite-wrestling|/start, /recruitiq|Two eligibility dates|
|3 We paid and nothing happened|composite-softball|/compare/ (live) then /resources|Free compare + $-checked alternatives|
|4 Undersized, found the fit|renfrow, composite-football|/personalize|Right level, not raw talent|
|5 What do we say to a coach?|composite-volleyball|/start, /resources (Coach Outreach)|Give me the words|
|6 Her sport just became a college sport|rodriguez, composite-wrestling|/emerging-sports|New-sport pride|
|7 Academics opened the door|rodenfels (HELD), composite-sprinter|/segments|Academic package|

## Claim and safety rules (inherited from AD-PLAN, binding)
- Address the parent; never target or address under-18s; no personal-attribute implication.
- No scholarship/offer promises, no counts we can't source, no false countdowns; every rule or date matches `site/data.js` with its bylaw.
- Real athletes: typography or licensed press imagery only. Composites labeled "Composite"; images "Illustration".
- **/resources rule:** the Gumroad products are third-party (McKinley Malbrough III). Ads or posts must never present them as Commit Book products, never quote paid content, and always carry "By McKinley Malbrough III, MM3 Sports. Educational material, not legal, tax or financial advice." Rodenfels story page is HELD: do not link offers from it.
- Kill rule default: after $60 / 3 days kill if CTR < 0.8% or cost per free signup > $20; $9 offer: kill if no purchase after $100.

## Draft creative cards
Each card is DRAFT / not posted. Full first-3-second text, format and kill rule live in AD-PLAN.md; the interactive playbook (`index.html`) renders them with route mapping.

|Card|Segment|Angle|New route|Interim landing (AD-PLAN)|
|-|-|-|-|-|
|F1|football|Proof over hype|/start|/calendar/|
|F2|football|Late isn't over|/recruitiq|/playbooks/late-bloomer/|
|F3|football|We paid, nothing happened|/personalize|/compare/|
|S1|travel baseball/softball|Showcase ROI|/segments|/playbooks/camp-roi/|
|S2|travel baseball/softball|Money math|/segments|/math/|
|S3|travel baseball/softball|Late isn't over|/start|/story/composite-baseball/|
|V1|club volleyball|Sport-specific rules|/segments|/calendar/|
|V2|club volleyball|Late specializer|/personalize|/story/composite-volleyball/|
|V3|club volleyball|Give me the words|/start|/start/|
|W1|wrestling incl. girls|New-sport pride|/emerging-sports|/story/rodriguez/|
|W2|wrestling incl. girls|Nobody told us|/recruitiq|/playbooks/eligibility-2-hard-deadlines/|
|L1|late-start / AAU basketball|Late isn't over|/recruitiq|/playbooks/late-bloomer/|
|L2|late-start|Two dates, $9|/recruitiq|/playbooks/eligibility-2-hard-deadlines/|
|G1|girls flag football (test)|Emerging sport|/emerging-sports|/start/|
|T1|track (test)|Academics|/segments|/story/rodenfels/ (HELD)|

`/access` is the primary route for the AAU-basketball segment; `/resources` is the secondary route for every segment (filtered by the story named in the segment table).
