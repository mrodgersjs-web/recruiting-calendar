# Commit Book: 10 New Offerings from Social Fetch Research

Date: 2026-11-17
Lane: commitbook (source: commitbook-10-offers)
Method: Social Fetch read-only GET queries on Reddit, X, and YouTube.

## Run receipt

| Metric | Value |
|---|---|
| Balance before | 9,163 credits |
| Calls made | 18 (all HTTP 200) |
| Credits spent | 18 (1 per call, under the 20 budget) |
| Balance after | 9,145 credits |
| Normalized signals collected | 348 (Reddit 103, X 126, YouTube 119) |
| Platforms queried | reddit, x, youtube |
| Ledger | 18 rows appended to ~/.rig/state/socialfetch/ledger.jsonl, lane "commitbook", source "commitbook-10-offers" |

## Queries run

Reddit, subreddit-scoped (`/v1/reddit/subreddits/search`, sort top, timeframe year):
r/ApplyingToCollege "recruiting coach emails silence", r/CFB "105 roster cap House settlement walk on",
r/bootroom "college recruiting highlight video", r/volleyball "club volleyball recruiting cost scholarship",
r/trackandfield "college recruiting scholarship process", r/baseball "showcase camp recruiting money",
r/Parenting "teen athlete recruiting stressful".

Reddit, global search (`/v1/reddit/search`, sort top, timeframe year):
"105 roster cap walk on recruiting", "NCSA recruiting service money worth",
"showcase camp recruiting waste money email coaches". Global search returned the strongest Reddit evidence; the subreddit-scoped calls mostly surfaced general sub traffic.

X (`/v1/twitter/search`, section top):
"college recruiting 105 roster cap", "NCSA recruiting service worth it", "college recruiting coach email no response",
"highlight film D2 D3 NAIA recruiting", "NCAA eligibility center confusing".

YouTube (`/v1/youtube/search`, sortBy relevance):
"college recruiting mistakes parents athletes", "highlight video college recruiting tips",
"walk on preferred walk on college recruiting".

## What the signals say

- Roster math is the loudest confusion right now: the 105-player cap, roster spot versus scholarship, and walk-on odds under new rules dominate X recruiting accounts and Reddit threads.
- Email silence and blast-email fatigue are named openly by coaches: generic recruiting blasts get deleted on sight, and second emails that ask for offers get no reply.
- Camp and showcase spending draws money-grab skepticism; event workers say pre-event coach contact is what separates a donation from an evaluation.
- Highlight film mistakes are one of the deepest content clusters on YouTube, with near-identical mistake lists across sports.
- Eligibility Center account types and D3 certification exceptions keep catching families off guard.
- Parent behavior and service upsells ($1,500 to $3K called out in posts) are a recurring pain thread.

## The 10 offerings

| # | Offer | Category | Price | Core evidence |
|---|---|---|---|---|
| 1 | Highlight Video Teardown | Film & Outreach | $49 audit | 42 signals; [3nxztEcy4sk](https://www.youtube.com/watch?v=3nxztEcy4sk), [UFssYVVLZBw](https://www.youtube.com/watch?v=UFssYVVLZBw), [85OOMfDp9iA](https://www.youtube.com/watch?v=85OOMfDp9iA) |
| 2 | Camp and Showcase Invite Audit | Camp & Showcase Audit | $29 audit | 18 signals; [event worker donation warning](https://www.reddit.com/r/youthsoccer/comments/1ur2cq0/ive_worked_recruiting_events_for_8_years_if_you/), [showcase money grab thread](https://www.reddit.com/r/volleyball/comments/1x7fp2q/canadian_volleyball_showcase_for_a_toptier_d1t1/), [college coach camps](https://www.reddit.com/r/Homeplate/comments/1sg5k89/college_coach_camps/), [12FJH0an-pA](https://www.youtube.com/watch?v=12FJH0an-pA) |
| 3 | Coach Email Silence Plan | Film & Outreach | $39 one-time | 27 signals; [blast emails get deleted](https://x.com/One11Recruiting/status/2122797045354246333), [second email advice](https://x.com/One11Recruiting/status/2122359158884233285), [standing out when emailing coaches](https://www.reddit.com/r/CollegeSoccer/comments/1xkmze7/advice_on_standing_out_when_emailing_coaches/), [jakedaltrui](https://x.com/jakedaltrui/status/2120173904429764672) |
| 4 | 105 Roster Cap Readiness Check | Roster & Aid Math | $29 one-time | 31 signals; [105 cap explainer](https://x.com/One11Recruiting/status/2122464854753649080), [roster spot vs scholarship](https://x.com/SDProspectsFB/status/2122028023629197754), [105 limit thread](https://www.reddit.com/r/footballstrategy/comments/1tzz3cd/what_is_the_point_of_the_105_man_roster_limit/), [walk-on odds thread](https://www.reddit.com/r/collegebaseball/comments/1pm7kvk/what_are_my_odds_at_walking_on_d1_with_new_ncaa/) |
| 5 | Walk-On Offer Decoder | Roster & Aid Math | $29 one-time | 24 signals; [PWO vs walk-on](https://www.youtube.com/watch?v=bkI77LbsUAc), [PWO red flag](https://www.youtube.com/watch?v=T0DDTybZpuw), [D1 walk-on vs D2/D3 aid](https://www.youtube.com/watch?v=gtIxuYKE5lA), [long snapper walk-on](https://www.reddit.com/r/highschoolfootball/comments/1x9k23x/walk_on_as_a_long_snapper/) |
| 6 | Eligibility Center Checklist | Eligibility & NIL | $29 one-time | 15 signals; [three account types](https://x.com/ncaaec/status/2120234410888864177), [certification account warning](https://x.com/SycamoreRules/status/2120554393678352769), [D3 certification note](https://x.com/_baseballfuture/status/2122015542231945222) |
| 7 | High School NIL and Eligibility Rules Brief | Eligibility & NIL | $29 one-time | 21 signals; [five-year eligibility window](https://x.com/V2Sports_/status/2120594008581771557), [Big Ten NIL proposal](https://x.com/2aDays_Ratings/status/2122774030696481233), [medical hardship change](https://x.com/heitner/status/2122665626862862365), [5-in-5 model](https://x.com/cack92/status/2122744826504282364) |
| 8 | D2, D3, and NAIA Aid Stacking Diagnostic | Roster & Aid Math | $79 diagnostic | 12 signals; [D1 walk-on vs D2/D3 aid](https://www.youtube.com/watch?v=gtIxuYKE5lA), [eligibility checklist post](https://x.com/chrisrandle_/status/2120639336534196638), [any-level offers](https://x.com/CoachDaniels06/status/2122086435691880951) |
| 9 | JUCO and Transfer Path Map | Parent Guidance | $39 one-time | 16 signals; [JUCO open roster spot](https://www.reddit.com/r/bootroom/comments/1vyndve/seeking_goalkeeper_delaware_county_community/), [any-level opportunity](https://x.com/ExpoRecruits/status/2122089883972030515), [boards being built now](https://x.com/vm_nextchapter/status/2121988912235290903) |
| 10 | Junior and Senior Rescue Plan | Parent Guidance | Included in $39 Pass | 36 signals; [parent mistakes](https://www.youtube.com/watch?v=F-AMA53Hk2c), [wrong fit not skill](https://www.youtube.com/watch?v=pcuUTmZiNqk), [unsigned senior roll call](https://x.com/ExpoRecruits/status/2122681661481447687), [$3K mistake](https://www.youtube.com/watch?v=phr3lthGiaA) |

Full structured data, including deliverables and chat starter prompts per offer: `content/offers-10x.json`.

## Notes

- All sample URLs are real URLs returned by Social Fetch in this run. Signal text is a short quote from the returned item.
- Demand counts (postCount) are the number of matching items seen per theme across the 18 calls, not audited totals.
- Intel shows what people are saying. Numbers and rule details cited above (105 cap, five-year eligibility window, account fees) must be confirmed against the primary source before any of this copy goes outward.
