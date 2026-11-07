# W10 SOURCES ledger (2026-11-06)
Every factual claim in a W10 playbook carries a source ID from this table, written like [S1] or [S1 13.9.3.3]. A claim with no ID is not a fact claim: it is a labeled RECOMMENDED step, a worksheet field, or a question to ask.
"Seen" = date a lane read it (from the v3 reports named in the last column). W10 did not re-fetch these pages; it reuses what earlier v3 lanes read. Anything marked VERIFY is not safe to state as fact until someone re-reads it.

| ID | Source | URL | Seen | Kind | Reported by |
|---|---|---|---|---|---|
| S1 | NCAA Division I Manual 2026-27 (LSDBi report 90008). Bylaws used: 13.1.1.1.1, 13.1.1.1.6, 13.1.1.1.9, 13.1.3.1, 13.1.3.1.1, 13.1.4.3, 13.1.5.3, 13.1.5.3.2, 13.4.1, 13.4.1.1, 13.6.2.1.1, 13.6.2.1.2, 13.6.2.1.7, 13.6.2.1.7.1, 13.6.3, 13.7.1.1, 13.7.1.2, 13.9.3.1, 13.9.3.3, 13.12.1.5.1, 13.12.1.5.2, 13.02.13.1(c)(e)(f), 14.3.1.1, 14.3.1.3, 17.2 | https://web3.ncaa.org/lsdbi/reports/getReport/90008 | 2026-11-05 | rule | site/data.js; W1-playbooks; W2-playbooks |
| S2 | NCAA Division II Manual (LSDBi 90010): Bylaws 13.1.1.1, 13.3.1.2 | https://web3.ncaa.org/lsdbi/reports/getReport/90010 | 2026-11-05 | rule (VERIFY against current printing) | site/data.js |
| S3 | NCAA Division III Manual (LSDBi 90011): Bylaw 13.6.1.1.1 | https://web3.ncaa.org/lsdbi/reports/getReport/90011 | 2026-11-05 | rule (VERIFY against current printing) | site/data.js; W3-factcheck |
| S4 | NCAA Eligibility Center registration checklist | https://fs.ncaa.org/Docs/eligibility_center/Student_Resources/Registration_Checklist.pdf | 2026-11-05 | procedure | site/data.js (W3 noted fs.ncaa.org PDFs did not load from that host: re-check) |
| S5 | NCAA final amateurism certification instructions | https://fs.ncaa.org/Docs/eligibility_center/Student_Resources/How_to_Request_Final_Amateurism_Certification.pdf | 2026-11-05 | procedure | site/data.js |
| S6 | NCAA Eligibility Center IE brochure | https://fs.ncaa.org/Docs/eligibility_center/Student_Resources/IE_Brochure.pdf | 2026-11-05 | procedure | site/data.js |
| S7 | NCAA initial-eligibility pages (D1, D2, D3), 2026-05-15 | https://www.ncaa.org/eligibility-center/initial-eligibility-requirements/division-i (and /division-iii; D2 at /initial-eligibility-requirements) | 2026-11-06 | rule summary | W7-recruitiq 1B |
| S8 | NCAA D1 roster-limit adoption news, 2025-06-23 | https://www.ncaa.org/news/media-center-di-board-of-directors-formally-adopts-changes-to-roster-limits/ | 2026-11-06 | rule summary | W7-recruitiq 1A |
| S9 | NCAA D1 Bylaw 17.2 roster limits (Football 105, Baseball 34, Track 45, Men's XC 17) | https://web3.ncaa.org/lsdbi/bylaw?refDate=20250830&ruleId=106414 | 2026-11-06 | rule | W7-recruitiq 1A |
| S10 | NCAA D1 Q&A on Designated Student-Athletes, 2026-02-11 | https://ncaaorg.s3.amazonaws.com/governance/d1/legislation/Feb2026D1Gov_PhaseSevenSetQuestionandAnswer.pdf | 2026-11-06 | rule Q&A | W7-recruitiq 1A |
| S11 | NCAA D2 athletics scholarships page (equivalency limits: Football 36.0, Baseball 9.0, Track/XC 12.6), 2026-05-20 | https://www.ncaa.org/division-ii/governance/membership-and-institutional-resources/athletics-scholarships | 2026-11-06 | rule | W7-recruitiq 1A |
| S12 | NAIA financial aid page, 2026-05-11 | https://www.naia.org/student-athletes/current/financial-aid | 2026-11-06 | rule | W7-recruitiq 1A |
| S13 | NAIA 2026-27 Official Handbook, Art. V Sec. C, p.70 | https://www.naia.org/wp-content/uploads/2026/07/2026_Official_Handbook.pdf | 2026-11-05 | rule | W3-factcheck |
| S14 | NAIA guide for the college-bound student ("register at PlayNAIA.org") | https://www.naia.org/wp-content/uploads/2026/05/naia_guide_college_bound_student-1.pdf | 2026-11-05 | procedure | W3-factcheck |
| S15 | NAIA recruiting page (no recruiting calendar, no communication limit) | https://www.naia.org/why-naia/recruiting | 2026-11-06 | rule summary | W7-access 2a |
| S16 | NJCAA divisional structure (aid by division) | https://www.njcaa.org/member_colleges/Divisional_Structure | 2026-11-06 | rule | W7-recruitiq 1A |
| S17 | NCAA probability of competing beyond high school, 2024-25 data (updated 2026-03) | https://www.ncaa.org/student-athletes/probability-of-competing-beyond-high-school ; method file https://ncaaorg.s3.amazonaws.com/research/pro_beyond/RES_ProbabilityBeyondHSFiguresMethod.pdf | 2026-11-06 | statistic (ratio of two headcounts, not odds) | W7-recruitiq 1D |
| S18 | NCAA recruiting fact sheet (about 2% of HS athletes get athletics scholarships; 2022-23 data) | https://ncaaorg.s3.amazonaws.com/compliance/recruiting/NCAA_RecruitingFactSheet.pdf | 2026-11-06 | statistic | W7-recruitiq 1D |
| S19 | NCAA recruiting page (communication rules "vary by division and grade level"; boosters may not contact prospects) | https://www.ncaa.org/eligibility-center/recruiting | 2026-11-06 | rule summary | W7-access 2a, 2e |
| S20 | 2026-27 D1 baseball recruiting calendar PDF | https://ncaaorg.s3.amazonaws.com/compliance/recruiting/calendar/2026-27/2026-27D1Rec_MBARecruitingCalendar.pdf | 2026-11-06 | calendar (linked; contents not read by W10) | W7-access 2a |
| S21 | Brown Track & Field Recruiting Standards 2026-27 (updated 9/1/26) | https://brownbears.com/documents/download/2026/8/24/Recruiting_Standards_2026-27.pdf | 2026-11-06 | program-published thresholds | W7-recruitiq 1C |
| S22 | Rutgers Track & Field recruiting standards (2025-10-10) | https://scarletknights.com/documents/download/2025/10/10/TF_RecruitingStandards.pdf | 2026-11-06 | program-published thresholds | W7-recruitiq 1C |
| S23 | Oral Roberts target standards 2026-27 ("achieving the marks does not guarantee a scholarship offer or roster spot") | https://s3.us-east-2.amazonaws.com/sidearm.nextgen.sites/oruathletics.com/documents/2025/10/24/Men_s_2026-2027_Target_Standards.pdf | 2026-11-06 | program-published thresholds | W7-recruitiq 1C |
| S24 | Eastern Michigan T&F recruiting standards | https://emueagles.com/documents/download/2026/9/2/Eastern_Michigan_Track___Field_Recruiting_Standards.pdf | 2026-11-06 | program-published thresholds | W7-recruitiq 1C |
| S25 | MIT team performance standards (D3, no athletic scholarships) | https://scripts.mit.edu/~mtfxc/recruiting/TeamPerformanceStandards.php | 2026-11-06 | program-published thresholds | W7-recruitiq 1C |
| S26 | Oriel Admissions: baseball programs do not publish numeric standards; families can always write first (2026-09-23) | https://orieladmissions.com/baseball-college-recruiting/ ; https://orieladmissions.com/when-can-college-coaches-contact-you/ | 2026-11-06 | secondary guidance | W7-recruitiq 1C; W7-access 2a |
| S27 | Pathley: no governing body publishes official baseball/football benchmarks | https://www.pathley.ai/blog-posts/baseball-recruiting-standards-guide | 2026-11-06 | secondary guidance | W7-recruitiq 1C |
| S28 | Kang Zhao et al., "Keeping it 100", Big Data, 2019-03-14 (2,644 class-of-2016 football recruits; self-promotion on Twitter associated with more offers; survey of 477 coaches: 85% search recruits online) | https://www.biz.uiowa.edu/faculty/kangzhao/pub/BigData_2019.pdf | 2026-11-05 | measured study | W1-recruit-behavior M1 |
| S29 | Cornerstone College Athletics Survey, 2015-08-19 (600+ coaches: 83% searched athletes online; 17% of staffs rescinded an offer over online content) | https://finance.yahoo.com/news/cornerstone-college-athletics-survey-reveals-131000575.html | 2026-11-05 | survey | W1-recruit-behavior M2 |
| S30 | NCAA DI SAAC Early Recruiting Survey, 2017-10-05 (timing pre-dates 2019 rules; only the ordering across sports is usable) | https://ncaaorg.s3.amazonaws.com/research/d1/2017D1RES_SAACEarlyRecruitingSurvey.pdf | 2026-11-05 | survey | W1-recruit-behavior M3 |
| S31 | NCSA highlight video guide (3-5 min / 15-30 plays; best plays first; decide in 30-60 s), 2023-01-30 | https://www.ncsasports.org/blog/tips-creating-great-highlight-video | 2026-11-05 | vendor guidance | W1-recruit-behavior C1 |
| S32 | NCSA football recruiting video (info slide: HT/WT, position, contact, GPA/test, head coach contact) | https://www.ncsasports.org/football/recruiting-video | 2026-11-05 | vendor guidance | W1-recruit-behavior C3 |
| S33 | NCSA baseball recruiting video (<= 5 min, best first) and guidelines (velocity, pop time, 60 time; pop time "verified by a neutral source") | https://www.ncsasports.org/baseball/recruiting-video ; https://www.ncsasports.org/baseball/recruiting-guidelines | 2026-11-05 | vendor guidance | W1-recruit-behavior C4, C5 |
| S34 | Perfect Game FAQ: 60-yard and 10-yard split recorded for every showcase attendee | https://www.perfectgame.org/articles/View.aspx?article=18167 | 2026-11-05 | vendor statement | W1-recruit-behavior C10 |
| S35 | r/CrossCountry thread by a D1 XC coach, 2016 (paraphrased only): improvement curve, consistency, state-meet place, responsiveness, athlete not parent drives | https://www.reddit.com/r/CrossCountry/comments/4v16xp/ | 2026-11-05 | anecdote (one coach) | W1-recruit-behavior F1 |
| S36 | Hudl support: share links, recruiting opt-in, public links | https://support.hudl.com/s/article/recruiting-faq-hudl-v3 (2026-02-02) ; https://productiverecruit.com/docs/profile/videos | 2026-11-06 | vendor help | W7-access 2c |
| S37 | YouTube help: unlisted works with the link, private does not; "Made for Kids" setting | https://support.google.com/youtube/answer/9632097 ; https://captainu.com/your-highlights-deserve-to-be-seen-how-to-upload-your-recruiting-video-to-youtube/ (2026-11-03) | 2026-11-06 | vendor help | W7-access 2c |
| S38 | D1 questionnaire rules (compliance material; sources conflict by date: VERIFY before stating a rule) | https://ncaaorg.s3.amazonaws.com/compliance/rrs/2021/presentations/d1/Division_I_Bylaw_13_Hot_Topics--STATIC.pdf ; https://compliance.sports.uga.edu/coaches-staff/recruiting/recruiting-materials (2025-09-12) | 2026-11-06 | compliance material | W7-access 2d |
| S39 | NFHS: rules on communication with minor athletes (2025-11-05) | https://nfhs.org/stories/rules-guidelines-on-communication-with-minor-athletes | 2026-11-06 | rule summary | W7-access 2b |
| S40 | Parent-problem research: W6 PROBLEMS.md (2026-11-06) and W1 DEMAND.md (2026-11-05). Directional hand-tagged counts; never quoted as statistics | v3/W6-problems/PROBLEMS.md ; v3/W1-parent-demand/DEMAND.md | 2026-11-06 | directional research | W6; W1 |
| S41 | NCAA D1 age-based eligibility adoption (2026-06-23; effective for fall 2027 first-time enrollees) | https://www.ncaa.org/news/division-i-adopts-age-based-eligibility-model | 2026-11-06 | rule summary | W7-recruitiq 1B |

## Citation forms
- Rule claim: `[S1 13.9.3.3]` means source S1, bylaw 13.9.3.3.
- Date from the site's data: `[S1 13.1.3.1] (v3 data.js verified 2026-11-05)`. The playbooks use the first form only; data.js is the machine copy of the same rows.
- A projected date is always written PROJECTED and never as an NCAA-published date.

## Items the earlier lanes flagged and W10 therefore does not state as fact
- D2 and D3 bylaw numbers (S2, S3): VERIFY against current printings.
- Any NAIA contact calendar: none exists [S15]. Do not invent one.
- D1 sport calendars (dead and quiet periods): not read by any lane; every playbook sends the family to the NCAA sport calendar for that week.
- NAIA and NJCAA scholarship counts from third-party tables: not used.
- Any universal "D1 needs X" measurable: not used (S26, S27).
