#!/usr/bin/env python3
"""Builds site/recruitiq/data.json from W10-verified rows (v3/W10-recruitiq/AUDIT.md).
Times are stored in seconds (lower is better); display strings are kept beside them."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "site", "recruitiq", "data.json")

def t(s):
    if ":" in s:
        m, r = s.split(":")
        return round(int(m) * 60 + float(r), 2)
    return round(float(s), 2)

def mark(display, label):
    return {"display": display, "seconds": t(display), "tier": label}

SRC_NCAA_BYLAW = "https://web3.ncaa.org/lsdbi/bylaw?refDate=20250830&ruleId=106414"
SRC_D1_BYLAW15 = "https://ncaaorg.s3.amazonaws.com/governance/d1/legislation/2026-27/2024-25D1GMS_Bylaw15.pdf"
SRC_D2 = "https://www.ncaa.org/division-ii/governance/membership-and-institutional-resources/athletics-scholarships"
SRC_D3 = "https://www.ncaa.org/eligibility-center/initial-eligibility-requirements/division-iii"
SRC_D1_IE = "https://www.ncaa.org/eligibility-center/initial-eligibility-requirements/division-i"
SRC_BROCHURE = "http://fs.ncaa.org/Docs/eligibility_center/Student_Resources/IE_Brochure.pdf"
SRC_NAIA_HB = "https://www.naia.org/wp-content/uploads/2026/05/2025_Official_Handbook.pdf"
SRC_NAIA_GUIDE = "https://www.naia.org/wp-content/uploads/2026/05/naia_guide_college_bound_student.pdf"
SRC_NAIA_AID = "https://www.naia.org/student-athletes/current/financial-aid"
SRC_NJCAA = "https://media.ardorsportshub.com/files/404933495157163011/3fb3dae3297443a688333ba7d0cbef68-2026-2027-Sports-Procedures-Chart-9-9-26.pdf"
SRC_HOUSE = "https://www.ncaa.org/news/media-center-di-board-of-directors-formally-adopts-changes-to-roster-limits/"
SRC_QA = "https://ncaaorg.s3.amazonaws.com/governance/d1/legislation/Feb2026D1Gov_PhaseSevenSetQuestionandAnswer.pdf"
SRC_AGE = "https://www.ncaa.org/news/division-i-adopts-age-based-eligibility-model"
SRC_TRANSFER = "http://fs.ncaa.org/Docs/eligibility_center/Transfer/TwoYearGuide.pdf"
SRC_PROB = "https://ncaaorg.s3.amazonaws.com/research/pro_beyond/RES_ProbabilityBeyondHSFiguresMethod.pdf"
SRC_PROB_PAGE = "https://www.ncaa.org/student-athletes/probability-of-competing-beyond-high-school"

def cite(label, url, note=""):
    return {"label": label, "url": url, "note": note}

NJCAA_NOTE = ("NJCAA 2026-27 Sports Procedures Chart (dated 9-9-26), column "
              "'# of Letter of Intent Signees/Scholarships'.")

def row(division, sport, roster, aid, gpa, sources, caveat=""):
    return {"division": division, "sport": sport, "roster_cap": roster,
            "aid_cap": aid, "gpa_rule": gpa, "sources": sources, "caveat": caveat}

D1_GPA = ("16 core courses; 10 of 16 (7 in English/math/science) before the 7th semester "
          "(10/7); minimum 2.3 core GPA; final transcript with proof of graduation.")
D2_GPA = "16 core courses; minimum 2.2 core GPA; final transcript with proof of graduation."
D1_SRC = [cite("NCAA D1 initial eligibility", SRC_D1_IE), cite("NCAA Eligibility Center brochure", SRC_BROCHURE)]
D2_SRC = [cite("NCAA Eligibility Center brochure (D2 2.2)", SRC_BROCHURE)]

eligibility = []
# D1 opted-in
for sport, roster, label in [("Football", 105, "105"), ("Baseball", 34, "34"), ("Track & Field / XC", 45, "45 (Men's Indoor and Outdoor T&F); Men's XC 17")]:
    eligibility.append(row("D1 opted-in", sport, label,
        "No sport-specific scholarship limit; aid may go to any rostered athlete up to the roster limit.",
        D1_GPA,
        [cite("Bylaw 17.2 roster limits", SRC_NCAA_BYLAW), cite("NCAA D1 Board roster-limit release (2025-06-23)", SRC_HOUSE),
         cite("D1 Governance Q&A (updated 2026-02-11)", SRC_QA)] + D1_SRC,
        "Aid cannot be revoked for roster management, performance or injury unless the athlete chooses to transfer. Designated Student-Athletes do not count toward the roster limit. A conference may set a lower roster limit, but not below the sport's 2024-25 D1 scholarship limit."))
# D1 legacy
eligibility.append(row("D1 non-opted-in (legacy)", "Football", "n/a (old model)",
    "FBS: 85 counters. FCS: 63 equivalencies and 85 counters.", D1_GPA,
    [cite("D1 Bylaw 15.5.6.1 / 15.5.6.2", SRC_D1_BYLAW15)] + D1_SRC))
eligibility.append(row("D1 non-opted-in (legacy)", "Baseball", "n/a (old model)",
    "11.7 equivalencies and 27 counters.", D1_GPA,
    [cite("D1 Bylaw 15.5.4", SRC_D1_BYLAW15)] + D1_SRC))
eligibility.append(row("D1 non-opted-in (legacy)", "Track & Field / XC", "n/a (old model)",
    "Not read by W10 for this sport. Ask the program.", D1_GPA,
    [cite("D1 Bylaw 15 (2024-25 text)", SRC_D1_BYLAW15)] + D1_SRC,
    "W10 verified the football and baseball legacy caps only; no track/XC legacy figure is claimed here."))
# D2
for sport, aid in [("Football", "36.0"), ("Baseball", "9.0"), ("Track & Field / XC", "12.6")]:
    eligibility.append(row("D2", sport, "n/a", aid + " equivalencies", D2_GPA,
        [cite("NCAA D2 athletics scholarships page", SRC_D2)] + D2_SRC,
        "The page's header date (2026-05-20) was not visible in W10's rendered text; treat the date as unconfirmed."))
# D3
for sport in ["Football", "Baseball", "Track & Field / XC"]:
    eligibility.append(row("D3", sport, "n/a", "0 (no athletics scholarships)",
        "No NCAA academic minimum; the school sets admissions and eligibility. Register for an NCAA ID.",
        [cite("NCAA D3 initial eligibility", SRC_D3)]))
# NAIA
for sport, aid in [("Football", "24"), ("Baseball", "12"), ("Track & Field / XC", "12")]:
    eligibility.append(row("NAIA", sport, "n/a", aid + " equivalencies",
        "NAIA Eligibility Center (separate from NCAA). Accredited HS graduate and 2.3+ GPA, or two of three: 18 ACT / 970 SAT, 2.0 HS GPA, class rank. The NAIA does not recognize the NCAA five-year rule or age limits.",
        [cite("NAIA Official Handbook, Upper Limits for Institutional Aid", SRC_NAIA_HB),
         cite("NAIA guide for the college-bound student", SRC_NAIA_GUIDE),
         cite("NAIA financial aid", SRC_NAIA_AID)],
        "Track figure is Indoor and Outdoor Track and Field."))
# NJCAA
for sport, aid in [("Football", "85"), ("Baseball", "30"), ("Track & Field / XC", "20")]:
    eligibility.append(row("NJCAA", sport, "n/a", aid + " letter-of-intent signees/scholarships",
        "Proof of graduation (or equivalency/GED). Bylaws 2026-27.",
        [cite("NJCAA 2026-27 Sports Procedures Chart", SRC_NJCAA, NJCAA_NOTE)],
        "The NJCAA divisional aid rules (D1 full aid, D2 tuition/fees/books, D3 none) were NOT re-verified by W10."))

rules_moving = [
    {"title": "D1 age-based eligibility",
     "text": "Approved by the D1 Cabinet 2026-06-23; NCAA noted the changes were not final until the meeting concluded Wednesday 2026-06-24. The 2026-07-31 deadline for waiver requests under the old rules is past. Up to five years if the athlete enrolls no later than the academic year after the 19th birthday; fully effective for fall 2027 first-time enrollees; fall 2026 enrollees get the better of old or new rules.",
     "source": cite("NCAA: Division I adopts age-based eligibility model", SRC_AGE)},
    {"title": "Two-year transfer GPA (D1)",
     "text": "The 2025-26 NCAA Two-Year Transfer Guide still reads 2.5 for D1 (and 2.2 for D2). A change to 2.0 is unconfirmed by any NCAA primary document.",
     "source": cite("NCAA Two-Year Transfer Guide (2025-26 edition)", SRC_TRANSFER)},
]

# ---- Bucket 2: published track standards (men's), W10-verified D1 programs ----
events = [{"id": "100", "label": "100m", "unit": "s"}, {"id": "400", "label": "400m", "unit": "s"},
          {"id": "800", "label": "800m", "unit": "min:s"}, {"id": "1500", "label": "1500m", "unit": "min:s"}]
DISC = "Achieving the marks does not guarantee a scholarship offer or roster spot."
DISC_ORU = {"text": DISC, "by": "school"}
def disc_generic(extra=""):
    return {"text": DISC, "by": "recruitiq", "extra": extra}

def prog(pid, name, conf, vintage, cycle, url, label_note, marks, disclaimer, notes=None):
    return {"id": pid, "name": name, "level": "D1", "conference": conf, "vintage": vintage,
            "cycle": cycle, "url": url, "label_note": label_note, "marks": marks,
            "disclaimer": disclaimer, "notes": notes or []}

programs = [
    prog("brown", "Brown", "Ivy", "2026-08-24", "2026-27",
         "https://brownbears.com/documents/download/2026/8/24/Recruiting_Standards_2026-27.pdf",
         "Brown labels: Target Performance / Walk On Consideration.",
         {"100": [mark("10.55", "Target Performance"), mark("10.75", "Walk-On Consideration")],
          "400": [mark("47.50", "Target Performance"), mark("48.70", "Walk-On Consideration")],
          "800": [mark("1:53.50", "Target Performance"), mark("1:55.50", "Walk-On Consideration")],
          "1500": [mark("3:55.00", "Target Performance"), mark("3:58.00", "Walk-On Consideration")]},
         disc_generic()),
    prog("rutgers", "Rutgers", "Big Ten", "2025-10-10", "2025-26 (not 2026-27)",
         "https://scarletknights.com/documents/download/2025/10/10/TF_RecruitingStandards.pdf",
         "Rutgers labels: Roster spot consideration / Consider for full athletic aid. All sprint times FAT.",
         {"100": [mark("10.35", "Consider for Full Aid"), mark("10.65", "Roster Spot Consideration")],
          "400": [mark("46.20", "Consider for Full Aid"), mark("47.90", "Roster Spot Consideration")],
          "800": [mark("1:49.00", "Consider for Full Aid"), mark("1:53.50", "Roster Spot Consideration")],
          "1500": [mark("3:45.00", "Consider for Full Aid"), mark("3:58.00", "Roster Spot Consideration")]},
         disc_generic("Rutgers itself lists scholarship availability, team needs, \"Academic performance is a critical aspect\" and \"Consistency at standard is heavily favored\"."),
         ["Rutgers lists: scholarship availability varies yearly, team needs, \"Academic performance is a critical aspect\", state/national meet performances, \"Consistency at standard is heavily favored\", coaches' development evaluation, character, and FAT timing only."]),
    prog("princeton", "Princeton", "Ivy", "2024-07-17", "page dated 2024-07-17 (at least two cycles old unless edited)",
         "https://goprincetontigers.com/sports/2024/7/17/princeton-mens-track-field-standards-for-recruitment",
         "Princeton label: standards to qualify for recruitment; should be achieved by the start of senior year. One mark per event.",
         {"100": [mark("10.80", "Standard to Qualify for Recruitment")],
          "400": [mark("48.80", "Standard to Qualify for Recruitment")],
          "800": [mark("1:53.00", "Standard to Qualify for Recruitment")],
          "1500": [mark("3:55.00", "Standard to Qualify for Recruitment")]},
         disc_generic()),
    prog("emu", "Eastern Michigan", "MAC", "2026-09-02", "2026-27",
         "https://emueagles.com/documents/download/2026/9/2/Eastern_Michigan_Track___Field_Recruiting_Standards.pdf",
         "EMU labels: Target recruits / Scholarship / Walk-on consideration.",
         {"100": [mark("10.30", "Target Performance"), mark("10.50", "Scholarship"), mark("10.70", "Walk-On Consideration")],
          "400": [mark("46.65", "Target Performance"), mark("47.50", "Scholarship"), mark("48.50", "Walk-On Consideration")],
          "800": [mark("1:49.50", "Target Performance"), mark("1:52.00", "Scholarship"), mark("1:54.00", "Walk-On Consideration")],
          "1500": [mark("3:47.50", "Target Performance"), mark("3:54.00", "Scholarship"), mark("3:58.00", "Walk-On Consideration")]},
         disc_generic()),
    prog("oru", "Oral Roberts", "Summit League", "2025-10-24", "2026-27 target standards",
         "https://s3.us-east-2.amazonaws.com/sidearm.nextgen.sites/oruathletics.com/documents/2025/10/24/Men_s_2026-2027_Target_Standards.pdf",
         "ORU labels: Target marks, with Summit League winning/qualifying marks beside them.",
         {"100": [mark("10.75", "Target Performance")],
          "400": [mark("49.60", "Target Performance")],
          "800": [mark("1:54.00", "Target Performance")],
          "1500": [mark("3:55.00", "Target Performance")]},
         DISC_ORU),
]

uno = {"id": "uno", "name": "New Orleans", "level": "D1",
       "vintage": "2026-08-19", "cycle": "2026",
       "url": "https://dxbhsrqyrr690.cloudfront.net/sidearm.nextgen.sites/unoprivateers.com/documents/2026/8/19/2026_Track_and_Field_Recruiting_Standards.pdf",
       "policy_note": "Athletic scholarships \"may range from 1%-100%\" and weigh GPA, test scores, aid availability and team needs. This language is New Orleans-only; it is not in the Eastern Michigan PDF. No per-event marks from this PDF are compared in the calculator.",
       "in_calculator": False}

excluded = [
    {"id": "mit", "name": "MIT (D3)", "reason": "Source page down on 2026-11-06; not re-read in W10. Excluded from the live calculator until re-verified.",
     "url": "https://scripts.mit.edu/~mtfxc/recruiting/TeamPerformanceStandards.php"},
    {"id": "vsu", "name": "Virginia State (D2)", "reason": "Not re-read in W10; not in the live calculator.",
     "url": "https://dxbhsrqyrr690.cloudfront.net/sidearm.nextgen.sites/vsu.sidearmsports.com/documents/2025/8/14/VSU_Recruiting_Standards_Track___Field_XC.pdf"},
    {"id": "seton", "name": "Seton Hill (D2)", "reason": "Not re-read in W10; not in the live calculator.",
     "url": "https://athletics.setonhill.edu/sports/2018/5/22/track-field-recruiting-standards.aspx"},
]

# ---- Bucket 4: NCAA participation ratios 2024-25 ----
ratios = [
    {"sport": "Football", "hs": 1029588, "ncaa": 83794, "overall": 8.1, "d1": 3.4, "d2": 2.1, "d3": 2.6},
    {"sport": "Baseball", "hs": 472598, "ncaa": 41580, "overall": 8.8, "d1": 2.7, "d2": 2.6, "d3": 3.5},
    {"sport": "Track & Field", "hs": 644235, "ncaa": 34747, "overall": 5.4, "d1": 1.9, "d2": 1.5, "d3": 2.0},
]
previous_edition = [
    {"sport": "Football", "previous_pct": 7.5, "current_pct": 8.1},
    {"sport": "Baseball", "previous_pct": 8.1, "current_pct": 8.8},
]

data = {
    "meta": {
        "built_from": "v3/W10-recruitiq/AUDIT.md (VERIFIED rows only)",
        "audit_date": "2026-11-06",
        "name": "RecruitIQ Standards & Fit Explorer",
        "disclaimer": "Education, not legal advice. A fit-evidence organizer, not a predictor: no score, no probability, no scholarship promise.",
    },
    "eligibility": eligibility,
    "rules_moving": rules_moving,
    "events": events,
    "programs": programs,
    "uno": uno,
    "excluded_from_calculator": excluded,
    "bucket3": {
        "why_unpublished": "No football program and no baseball program with a published numeric cutoff was found in the W7 pass. Absence is 'not found', not proof none exist. Track programs publish marks because the event is measured by a clock; football and baseball fit depends on position, scheme, roster need and film.",
        "evaluated": [
            "Game film (position-specific, against comparable competition)",
            "Verified camp or showcase measurables, dated and tied to a named event (40-yard time, height/weight, pitch velocity, exit velocity, pop time)",
            "Position depth and roster need in the class you would sign in",
            "Academics against that school's own admissions bar",
            "Character, coachability and what your own coaches say",
        ],
        "aggregator_note": "Third-party tables (NCSA, NextCommit, Go Big, Premier Athletes, Scorability) are a vendor's composite or estimate, not NCAA standards and not any program's statement. They disagree with each other: the D1 pitcher floor is '84 mph consistently' (NCSA, Go Big) vs '88 to 92 mid-major' (NextCommit) vs 'average fastball 85 / top 88.4 D1 mid-major' (Premier Athletes). Two guides state outright that no official chart exists.",
        "action": "Ask the coach what they evaluate. A number that fits one program may not describe another.",
    },
    "ratios": ratios,
    "ratio_source": {"label": "NCAA Estimated Probability of Competing Beyond High School (2024-25 data, updated March 2026)", "url": SRC_PROB, "page": SRC_PROB_PAGE},
    "ratio_method": [
        "A ratio of two headcounts in the same year: NCAA participants in 2024-25 divided by high school participants in 2024-25.",
        "High school counts exclude club teams.",
        "NCAA counts exclude NAIA and NJCAA, so the all-levels figure for a family considering every level is understated.",
        "Counts every rostered athlete (walk-ons, transfers, international athletes), not only recruited high school seniors.",
        "Not an individual athlete's probability and says nothing about any athlete's measurables.",
    ],
    "previous_edition": previous_edition,
    "previous_edition_label": "previous NCAA edition (2023RES file; base year not read off the PDF header)",
    "fact_sheet": {"text": "NCAA fact sheet: only about 2% of high school athletes are awarded athletics scholarships.",
                   "label": "pre-House settlement figure; no data-year label printed in the text W10 extracted",
                   "url": "https://ncaaorg.s3.amazonaws.com/compliance/recruiting/NCAA_RecruitingFactSheet.pdf"},
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w") as f:
    json.dump(data, f, indent=1, ensure_ascii=False)
    f.write("\n")
print("wrote", OUT)
