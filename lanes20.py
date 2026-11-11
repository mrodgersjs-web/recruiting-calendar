# -*- coding: utf-8 -*-
"""W20: add the two basketball lanes to the site calendar data.

The live site ships baseball, football and track only. The girls' and boys' rules
below are the ones verified against the 2026-27 bylaws on 11 Nov 2026, with the
same 12 keys the other sports use. Class year 2029, like the rest of the file:
app.js shifts every date for a different class year.

Dates marked projected come from the bylaw formula, not a published calendar. The
2028-29 calendars are not out.
"""
import json, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

P = pathlib.Path("site/data.js")
raw = P.read_text(encoding="utf-8")
data = json.loads(raw[raw.index("{"):raw.rindex("}") + 1])

EC = "https://web3.ncaa.org/lsdbi/reports/getReport/90008"
CAL = "https://ncaaorg.s3.amazonaws.com/compliance/recruiting/calendar/2026-27/2026-27D1Rec_Women%27sBasketballRecruitingCalendar.pdf"
CALM = "https://ncaaorg.s3.amazonaws.com/compliance/recruiting/calendar/2026-27/2026-27D1Rec_Men%27sBasketballRecruitingCalendar.pdf"


def row(iso, kind, event, plain, cost, rule, url, sort=None):
    return {"iso_date": iso, "kind": kind, "event": event, "plain_english": plain,
            "cost_if_missed": cost, "rule": rule, "citation_url": url,
            "sort": sort or iso}


GIRLS = [
 row("2026-11-15", "action", "Have the counselor check every course against the NCAA list",
      "Map completed and planned classes against your school's NCAA-approved course list. Not every class counts. This is our recommended date, not an NCAA one.",
      "Problems found in 12th grade are often too late to fix.", "D1 Bylaw 14.3.1.1", EC),
 row("2027-06-01", "opening", "D1 women's basketball coaches may start calling, texting and emailing",
      "A coach may phone, text or email her on this date, one day earlier than in men's basketball. Off-campus meetings are still months away.",
      "None for starting later. A coach who calls earlier than this is behind on the rule.",
      "D1 Bylaws 13.1.3.1.5, 13.4.1.6", EC),
 row("2028-01-01", "opening", "Paid campus visits may begin",
      "The school pays. In men's basketball this date is August 1 of 11th grade, seven months earlier.",
      "You lose a full season of free look-rounds at the schools she wants most.",
      "D1 Bylaw 13.6.2.1.6", EC),
 row("2028-04-01", "window", "Contact stops completely until 31 July",
      "No calls, no texts, no email, no visits with her, her family or her club coach from 1 April through 31 July. Evaluation happens only at approved events on set weekends. Silence in this window is the rule, not a lack of interest.",
      "Families read the silence as a no and stop working their list. A coach who replies in this window may be out of rule.",
      "D1 Bylaws 13.1.5.5.2, 13.1.3.1.5.1; women's basketball calendar", CAL),
 row("2028-08-01", "opening", "Written aid offers may go out",
      "In every sport except football, a school may not put an aid number in writing before 1 August of 12th grade. Ask for the number in writing in October.",
      "A verbal number she cannot hold. Coaches may talk before this date, and they do.",
      "D1 Bylaw 13.9.3.1", EC),
 row("2028-09-01", "opening", "Off-campus contact may begin",
      "A coach may meet her away from campus, only at her school or her home. In men's basketball this is allowed a full school year earlier.",
      "Late meetings cost her the fall, when every other family is already in the gym.",
      "D1 Bylaw 13.1.1.1.5", EC),
 row("2028-10-01", "action", "Ask every school the same two questions",
      "Where do I stand on your list, and what do you still need to see? Do this in writing, the same week, to every school on the list.",
      "A school that is not asked does not always answer on its own.", "Our recommended date", EC),
 row("2028-11-08", "projected", "Early signing period for basketball (projected 8 to 15 Nov)",
      "The rule is the second Wednesday in November through the following Wednesday. The 2028-29 calendar is not published yet, so hold this a week either way.",
      "She can still sign in April. What she loses is the chance to finish recruiting in November.",
      "D1 Bylaw 13.02.13.1", EC),
 row("2028-11-01", "hard", "Junior college letters of intent may be signed",
      "A junior college letter binds one school year at one school, and a parent signs it if she is under 18. Leaving early needs that school's written release.",
      "One letter can stop her from signing with any other junior college that fall.",
      "NJCAA 2026-27 Sports Procedures Chart", "https://www.njcaa.org/"),
 row("2029-04-11", "projected", "Regular signing period for basketball (projected 11 Apr)",
      "The second Wednesday in April. There is no late period in basketball, so this is the last clear door for a regular aid agreement.",
      "After this date a school must find room on the roster during the year.", "D1 Bylaw 13.02.13.1", EC),
]

BOYS = [
 row("2026-11-15", "action", "Have the counselor check every course against the NCAA list",
      "Map completed and planned classes against your school's NCAA-approved course list. Not every class counts. This is our recommended date, not an NCAA one.",
      "Problems found in 12th grade are often too late to fix.", "D1 Bylaw 14.3.1.1", EC),
 row("2027-06-15", "opening", "D1 men's basketball coaches may start calling, texting and emailing",
      "A coach may phone, text or email him from this date. This is the single date most guides get wrong for basketball.",
      "None for starting later. A coach who calls earlier than this is behind on the rule.",
      "D1 Bylaw 13.1.3.1.6", EC),
 row("2027-08-01", "opening", "Paid campus visits may begin",
      "The school pays. In women's basketball this date is 1 January of 11th grade instead.",
      "You lose the fall and winter look-rounds at the schools he wants most.",
      "D1 Bylaw 13.6.2.1.5", EC),
 row("2027-09-01", "opening", "Off-campus contact may begin, on the first day of 11th grade",
      "Use your school's real first day, not September 1. Through 11th grade a coach may only meet him at his school, except during the April windows.",
      "A meeting a week early is a violation, and it can wipe out his paperwork at that school.",
      "D1 Bylaw 13.1.1.1.3", EC),
 row("2028-04-01", "window", "April evaluation and contact windows",
      "The men's calendar gives April recruiting periods that other sports do not get. This is the month a family can push hardest.",
      "Miss the April windows and the next real chance is the grassroots season.",
      "D1 men's basketball recruiting calendar", CALM),
 row("2028-08-01", "opening", "Written aid offers may go out",
      "In every sport except football, a school may not put an aid number in writing before 1 August of 12th grade. Ask for the number in writing in October.",
      "A verbal number he cannot hold. Coaches may talk before this date, and they do.",
      "D1 Bylaw 13.9.3.1", EC),
 row("2028-10-01", "action", "Ask every school the same two questions",
      "Where do I stand on your list, and what do you still need to see? Do this in writing, the same week, to every school on the list.",
      "A school that is not asked does not always answer on its own.", "Our recommended date", EC),
 row("2028-11-08", "projected", "Early signing period for basketball (projected 8 to 15 Nov)",
      "The rule is the second Wednesday in November through the following Wednesday. The 2028-29 calendar is not published yet, so hold this a week either way.",
      "He can still sign in April. What he loses is the chance to finish recruiting in November.",
      "D1 Bylaw 13.02.13.1", EC),
 row("2028-11-01", "hard", "Junior college letters of intent may be signed",
      "A junior college letter binds one school year at one school, and a parent signs it if he is under 18. Leaving early needs that school's written release.",
      "One letter can stop him from signing with any other junior college that fall.",
      "NJCAA 2026-27 Sports Procedures Chart", "https://www.njcaa.org/"),
 row("2029-04-11", "projected", "Regular signing period for basketball (projected 11 Apr)",
      "The second Wednesday in April. There is no late period in basketball, so this is the last clear door for a regular aid agreement.",
      "After this date a school must find room on the roster during the year.", "D1 Bylaw 13.02.13.1", EC),
]

data["basketball_girls"] = {"class_year": 2029, "verified_on": "2026-11-11",
    "source_label": "2026-27 NCAA Division I Manual", "deadlines": GIRLS}
data["basketball_boys"] = {"class_year": 2029, "verified_on": "2026-11-11",
    "source_label": "2026-27 NCAA Division I Manual", "deadlines": BOYS}

out = "window.RC_DATA=" + json.dumps(data, indent=1, ensure_ascii=True) + ";\n"
P.write_text(out, encoding="utf-8")
print("data.js rows now:", {k: len(v["deadlines"]) for k, v in data.items()}, "bytes", len(out))
