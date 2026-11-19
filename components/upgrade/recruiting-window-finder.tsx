"use client";

import { useMemo, useState, type ReactNode } from "react";
import {
  ArrowRight,
  CalendarDays,
  ChevronDown,
  ClipboardList,
  MessageSquareText,
  Stamp,
} from "lucide-react";

/* ------------------------------------------------------------------ */
/*  The 30-Second Recruiting Window & Roster Cap Calculator            */
/*  Rules checked 11 November 2026 against the 2026-27 rule text,      */
/*  the printed football, basketball and volleyball playbooks, and     */
/*  the site rule rows (data.js, verified 2026-11-05).                 */
/* ------------------------------------------------------------------ */

type SportKey =
  | "football"
  | "volleyball"
  | "mens-basketball"
  | "womens-basketball"
  | "baseball"
  | "softball"
  | "mens-soccer"
  | "womens-soccer"
  | "womens-lacrosse"
  | "swimming"
  | "wrestling"
  | "track-field";

type DivisionKey = "d1" | "d2" | "d3" | "naia" | "njcaa";

type GradYear = 2026 | 2027 | 2028 | 2029 | 2030;

interface MonthDay {
  year: number;
  month: number; // 1-12
  day: number;
}

interface RuleWindowSpec {
  kind: "date" | "anytime" | "unprinted";
  anchor: ((gradYear: number) => MonthDay) | null;
  when: string;
  cite: string;
  projected: boolean;
  note?: string;
}

interface ResolvedWindow {
  kind: "date" | "anytime" | "unprinted";
  date: MonthDay | null;
  when: string;
  cite: string;
  projected: boolean;
  note?: string;
}

interface RosterNote {
  headline: string;
  detail: string;
  verified: boolean;
}

interface SportConfig {
  key: SportKey;
  label: string;
  noun: string;
  filmNote: string;
  sopsSlug: string | null;
  contact: Record<DivisionKey, RuleWindowSpec>;
  visit: Record<DivisionKey, RuleWindowSpec>;
  writtenOffer: Partial<Record<DivisionKey, RuleWindowSpec>>;
  roster: Record<DivisionKey, RosterNote>;
}

/* ----------------------------- date math ----------------------------- */

const MONTHS = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
] as const;

const MONTHS_ABBR = [
  "JAN",
  "FEB",
  "MAR",
  "APR",
  "MAY",
  "JUN",
  "JUL",
  "AUG",
  "SEP",
  "OCT",
  "NOV",
  "DEC",
] as const;

function fmtStamp(date: MonthDay): string {
  return `${date.day} ${MONTHS_ABBR[date.month - 1]} ${date.year}`;
}

function _fmtLong(date: MonthDay): string {
  return `${date.day} ${MONTHS[date.month - 1]} ${date.year}`;
}

function toUtc(date: MonthDay): number {
  return Date.UTC(date.year, date.month - 1, date.day);
}

/* Grade anchors. Graduation is spring of gradYear.
   10th grade = school year (gradYear-3)/(gradYear-2), so its summer is gradYear-2.
   11th grade ends in June gradYear-1; 12th grade is the (gradYear-1)/gradYear year. */
const after10thJun15 = (g: number): MonthDay => ({ year: g - 2, month: 6, day: 15 });
const after10thJun1 = (g: number): MonthDay => ({ year: g - 2, month: 6, day: 1 });
const juniorAug1 = (g: number): MonthDay => ({ year: g - 2, month: 8, day: 1 });
const juniorSep1 = (g: number): MonthDay => ({ year: g - 2, month: 9, day: 1 });
const juniorJan1 = (g: number): MonthDay => ({ year: g - 1, month: 1, day: 1 });
const seniorAug1 = (g: number): MonthDay => ({ year: g - 1, month: 8, day: 1 });
const seniorSep1 = (g: number): MonthDay => ({ year: g - 1, month: 9, day: 1 });
const seniorNov15 = (g: number): MonthDay => ({ year: g - 1, month: 11, day: 15 });

/* Football's junior-year visit window closes the Sunday before the
   last Wednesday in June (13.6.2.1.7). For the class of 2029 that is
   25 June 2028, which matches the verified site row. */
function lastWednesdayOfJune(year: number): number {
  for (let d = 30; d >= 1; d -= 1) {
    if (new Date(Date.UTC(year, 5, d)).getUTCDay() === 3) return d;
  }
  return 28;
}

function footballVisitClose(year: number): MonthDay {
  return { year, month: 6, day: lastWednesdayOfJune(year) - 3 };
}

/* --------------------------- rule builders --------------------------- */

function dateRule(
  anchor: (gradYear: number) => MonthDay,
  when: string,
  cite: string,
  opts?: { projected?: boolean; note?: string },
): RuleWindowSpec {
  return {
    kind: "date",
    anchor,
    when,
    cite,
    projected: opts?.projected ?? false,
    note: opts?.note,
  };
}

function anytimeRule(when: string, cite: string, opts?: { note?: string }): RuleWindowSpec {
  return { kind: "anytime", anchor: null, when, cite, projected: false, note: opts?.note };
}

function unprintedRule(note: string): RuleWindowSpec {
  return {
    kind: "unprinted",
    anchor: null,
    when: "No national rule printed",
    cite: "Ask the school and get the answer in writing",
    projected: true,
    note,
  };
}

function resolveWindow(spec: RuleWindowSpec, gradYear: number): ResolvedWindow {
  return {
    kind: spec.kind,
    date: spec.anchor ? spec.anchor(gradYear) : null,
    when: spec.when,
    cite: spec.cite,
    projected: spec.projected,
    note: spec.note,
  };
}

/* Lower divisions: D3, NAIA and junior college coaches may answer any
   time. Verified in the volleyball playbook ("A D3, NAIA or junior
   college coach may answer: any time") and the basketball playbook
   ("NAIA: no calendar, no rules on when a coach may contact you"). */
const CONTACT_LOWER = {
  d3: anytimeRule(
    "Any time",
    "NCAA D3 contact, checked 11 Nov 2026",
    { note: "No NCAA contact date holds a D3 coach back. Write today." },
  ),
  naia: anytimeRule(
    "Any time",
    "NAIA prints no contact calendar (basketball playbook, checked 11 Nov 2026)",
    { note: "Small staffs. The head coach usually answers the email directly." },
  ),
  njcaa: anytimeRule(
    "Any time",
    "NJCAA contact, checked 11 Nov 2026",
    { note: "Ask the college, not the club or high school coach, what the program carries." },
  ),
};

const VISIT_LOWER = {
  d3: dateRule(
    juniorJan1,
    "1 January of 11th grade",
    "D3 Bylaw 13.6.1.1.1",
    { note: "No athletic money, so the trip is about the school and the roster. Ask about academic and need aid in the same email." },
  ),
  naia: unprintedRule("No national visit rule is printed. Ask the school what the trip covers before anyone books travel."),
  njcaa: dateRule(
    juniorAug1,
    "First day of classes of 11th grade (about 1 August)",
    "NJCAA visit rule, checked 11 Nov 2026",
    { note: "Ask the college what the trip covers." },
  ),
};

/* D2 pattern from the verified site row (D2 Bylaws 13.1.1.1, 13.3.1.2):
   calls, texts and emails allowed at any time; in-person contact and
   paid visits open 15 June after 10th grade. */
const D2_CONTACT_ANYTIME = anytimeRule(
  "Any time by phone, text or email",
  "D2 Bylaws 13.1.1.1, 13.3.1.2",
  { note: "In-person contact and paid visits open 15 June after 10th grade. Verify against your sport's printed calendar." },
);
const D2_CONTACT_JUN15 = dateRule(
  after10thJun15,
  "15 June after 10th grade",
  "D2 Bylaws 13.1.1.1, 13.3.1.2",
  { projected: true, note: "Worked out from the D2 rule text, not from a printed calendar. Check the school's own dates." },
);
const D2_VISIT_JUN15 = dateRule(
  after10thJun15,
  "15 June after 10th grade",
  "D2 Bylaw 13.1.1.1",
  { note: "Earlier than Division I, and a real lever when a D2 staff is honest in June." },
);

const CONTACT_ANYTIME_LOWER = CONTACT_LOWER;
const VISIT_ANY_LOWER = VISIT_LOWER;

/* ----------------------------- roster notes ---------------------------- */

const ROSTER_MODEL: Record<DivisionKey, RosterNote> = {
  d1: {
    headline: "Roster limit model at opted-in schools",
    detail:
      "At schools that signed the NCAA settlement (live since 1 July 2025), the cap counts players, not dollars, and aid may be any size on any of them. There is no printed list of who opted in. The number that decides the odds is how many spots open in this graduating class.",
    verified: false,
  },
  d2: {
    headline: "Equivalency model",
    detail:
      "A money ceiling the staff may cut into pieces. Most offers are a half or a third of one year's bill. Compare the real cost of the school, not the name on the sweatshirt.",
    verified: false,
  },
  d3: {
    headline: "No athletic aid at all",
    detail:
      "Aid comes from the normal financial aid office: academic and need-based (D3 Bylaw 15.01.3). The coach can speak up for an admit but cannot pay. The largest single group of athletes in most sports plays here.",
    verified: true,
  },
  naia: {
    headline: "Equivalency model, no roster limit",
    detail:
      "Genuine money at a lower cost of living. Read the school's own paper before anyone signs anything.",
    verified: false,
  },
  njcaa: {
    headline: "Junior college letters",
    detail:
      "NJCAA divisions are not NCAA ones. Ask the college which division it plays in and exactly what its letter covers.",
    verified: false,
  },
};

const ROSTER_FOOTBALL: Record<DivisionKey, RosterNote> = {
  d1: {
    headline: "105 roster cap at settlement schools",
    detail:
      "105 players on the roster at schools using the settlement rules (Bylaw 17.2, live since 1 July 2025), with aid of any size on any of them. Schools that stayed out still work to 85 counters (15.5.6.1). A walk-on now takes one of the 105 seats. There is no limit on how many players a school may sign in a signing period: the roster cap is the only real limit.",
    verified: true,
  },
  d2: {
    headline: "36.0 equivalencies per team",
    detail:
      "36.0 worth of aid per team, split however the staff wants it. No national roster cap. Expect a quarter or a half of one year's bill, and compare it against academic aid.",
    verified: true,
  },
  d3: ROSTER_MODEL.d3,
  naia: {
    headline: "24 full-grant equivalents per team",
    detail: "24 full-grant equivalents per team, splittable, and no limit on roster size. Read the school's own paper; see the playbook chapter on paperwork.",
    verified: true,
  },
  njcaa: {
    headline: "85 letters of intent per team",
    detail:
      "85 letters of intent per team. These are NJCAA divisions, not NCAA ones: NJCAA Division 2 schools pay tuition only, and Division 3 pays nothing.",
    verified: true,
  },
};

const ROSTER_VOLLEYBALL: Record<DivisionKey, RosterNote> = {
  d1: {
    headline: "18-player roster limit at opted-in schools",
    detail:
      "No aid cap. A roster limit of 18 players on aid in any amount, up from the old 12 head-count scholarships, in place since 1 July 2025. A conference may set a lower number, but not below 12. There is no printed list of who opted in. The scarce thing is a seat.",
    verified: true,
  },
  d2: {
    headline: "8.0 equivalencies per team",
    detail:
      "A money ceiling the staff may cut into pieces. A staff can spread 8.0 across many players, so ask how the money is split, not just how much exists. Half of most aid ladders is talk.",
    verified: true,
  },
  d3: {
    headline: "No athletic aid, no roster limit",
    detail:
      "No athletic aid at all, and no roster limit. 417 programs, the biggest door in the sport, and the one families walk past.",
    verified: true,
  },
  naia: {
    headline: "8 aid equivalents, no roster limit",
    detail: "8 aid equivalents, and no roster limit. Small staffs: the head coach usually answers the email directly.",
    verified: true,
  },
  njcaa: {
    headline: "14 with exempt athletes outside the count",
    detail:
      "14, and athletes named as exempt do not count against it. Two counts are in circulation and the published table sits inside a login, so ask the college for its own number.",
    verified: true,
  },
};

const ROSTER_BASKETBALL: Record<DivisionKey, RosterNote> = {
  d1: {
    headline: "15 players on the team",
    detail:
      "Fifteen players on the team, paid or unpaid. The old limit was 13 for men and 15 for women. A coach can carry 15 and pay only 6. Ask how many of the fifteen will be paid next year and whether one is set aside for the position. There is no cap on the amount of aid and nobody is promised more than one year at a time.",
    verified: true,
  },
  d2: {
    headline: "10 full scholarships to spread",
    detail: "Ten full scholarships to spread across the whole team. Most offers are a half or a third. Compare real cost, not reputation.",
    verified: true,
  },
  d3: {
    headline: "No money for sports at all",
    detail:
      "The offer is getting on the team, plus the aid the school gives for grades or family need. The coach can speak up but cannot pay.",
    verified: true,
  },
  naia: {
    headline: "8 scholarships",
    detail: "Eight scholarships, no calendar, and no rules on when a coach may contact an athlete. The letter a school signs does not protect the family the way it thinks it does. Read the school's own paper.",
    verified: true,
  },
  njcaa: {
    headline: "15 scholarships, one school year at a time",
    detail:
      "Fifteen scholarships, one school year at a time, and one letter that binds only to other junior colleges. A real second path: the athlete can earn credits and play.",
    verified: true,
  },
};

const ROSTER_BASEBALL: Record<DivisionKey, RosterNote> = {
  d1: {
    headline: "34-player roster limit at opted-in schools",
    detail:
      "34 players on the roster at opted-in schools, where the old scholarship cap no longer applies (settlement rules, live since 1 July 2025). There is no printed list of who opted in.",
    verified: true,
  },
  d2: {
    headline: "9.0 equivalencies per team",
    detail: "Division II baseball still caps aid at 9.0 equivalencies for the whole team. Most offers are partial.",
    verified: true,
  },
  d3: ROSTER_MODEL.d3,
  naia: ROSTER_MODEL.naia,
  njcaa: ROSTER_MODEL.njcaa,
};

/* ------------------------------ sports -------------------------------- */

function commonContactD1Jun15(projected: boolean): RuleWindowSpec {
  return dateRule(
    after10thJun15,
    "15 June after 10th grade",
    projected ? "Common NCAA pattern (the June 15 date most sports use)" : "D1 Bylaw 13.1.3.1",
    {
      projected,
      note: projected
        ? "Worked out from the rule text, not printed for this sport in our checked sources. Verify against the printed calendar."
        : "Before this day a coach may watch and rate an athlete. From this day the coach may email, text or call.",
    },
  );
}

const GENERIC_VISIT_D1 = dateRule(
  juniorAug1,
  "1 August before 11th grade",
  "D1 visit rule pattern (13.6.2)",
  {
    projected: true,
    note: "Worked out from the rule text. Each school pays for one visit per athlete, and a certification account is required before a D1 official visit.",
  },
);

const SPORTS: SportConfig[] = [
  {
    key: "football",
    label: "Men's Football",
    noun: "football",
    filmNote: "Play every game on one camera from a high wide angle, and keep full-game links ready.",
    sopsSlug: "football",
    contact: {
      d1: dateRule(after10thJun15, "15 June after 10th grade", "D1 Bylaw 13.1.3.1", {
        note: "Off-campus meetings open 1 January of 11th grade (13.1.1.1.6). From January 2027, FBS schools get four recruiting opportunities per prospect between 1 January and 31 May, at most one a week. No written money before 15 November of 12th grade (13.9.3.3). Talk is early, paper is late.",
      }),
      d2: D2_CONTACT_ANYTIME,
      ...CONTACT_ANYTIME_LOWER,
    },
    visit: {
      d1: {
        kind: "date",
        anchor: (g: number) => ({ year: g - 1, month: 4, day: 1 }),
        when: "1 April of 11th grade, through the Sunday before the last Wednesday in June",
        cite: "D1 Bylaws 13.6.2.1.7, 13.6.2.2",
        projected: false,
        note: "Each school pays for one visit per athlete before 15 October after graduation and one after. The window reopens 1 September of 12th grade.",
      },
      d2: D2_VISIT_JUN15,
      ...VISIT_ANY_LOWER,
    },
    writtenOffer: {
      d1: dateRule(seniorNov15, "15 November of 12th grade", "D1 Bylaw 13.9.3.3", {
        note: "A written athletics aid offer cannot be made before this day (rule adopted October 2025). A verbal offer binds neither side. Early signing runs the Wednesday before the first Saturday in December; the regular date is the first Wednesday in February.",
      }),
    },
    roster: ROSTER_FOOTBALL,
  },
  {
    key: "volleyball",
    label: "Women's Volleyball",
    noun: "volleyball",
    filmNote: "The club season, not the high school season, is where staffs watch. Put the club schedule in the email.",
    sopsSlug: "volleyball",
    contact: {
      d1: dateRule(after10thJun15, "15 June after 10th grade", "USA Volleyball recruiting timeline, checked 11 Nov 2026", {
        note: "No rule stops an athlete from emailing, texting or calling today. Division I and II coaches cannot reply directly before this day. It is not a no-contact rule, it is a no-answer rule.",
      }),
      d2: dateRule(after10thJun15, "15 June after 10th grade", "USA Volleyball recruiting timeline, checked 11 Nov 2026", {
        note: "The same date for Division II. The athlete may write today; the coach may not answer before it.",
      }),
      ...CONTACT_ANYTIME_LOWER,
    },
    visit: {
      d1: dateRule(juniorAug1, "1 August before 11th grade", "D1 visit rule (13.6.2 pattern)", {
        projected: true,
        note: "Worked out from the rule text. Five official visits in a lifetime, and a paid certification account is needed before the first one. Unofficial visits at the family's own cost are allowed from the same date.",
      }),
      d2: D2_VISIT_JUN15,
      ...VISIT_ANY_LOWER,
    },
    writtenOffer: {
      d1: {
        kind: "date",
        anchor: (g: number) => {
          /* second Wednesday in November of 12th grade */
          const first = new Date(Date.UTC(g - 1, 10, 1)).getUTCDay();
          const day = 1 + ((3 - first + 7) % 7) + 7;
          return { year: g - 1, month: 11, day };
        },
        when: "Second Wednesday in November of 12th grade",
        cite: "D1 signing rule (13.02.13.1(f) pattern)",
        projected: true,
        note: "There is no National Letter of Intent any more. What gets signed is a written offer of athletics aid, and once it is signed every other school must stop recruiting. The 2028-29 sheet is not printed yet.",
      },
    },
    roster: ROSTER_VOLLEYBALL,
  },
  {
    key: "mens-basketball",
    label: "Men's Basketball",
    noun: "basketball",
    filmNote: "Summer teams are watched by the NCAA at approved events only. Ask before paying for a showcase.",
    sopsSlug: "mens-basketball",
    contact: {
      d1: dateRule(after10thJun15, "15 June after 10th grade", "D1 men's basketball, checked 11 Nov 2026", {
        note: "Before this day a coach may watch and rate an athlete. From this day the coach may email, text, call, or send a form. The rule is on the coach, not on the athlete.",
      }),
      d2: D2_CONTACT_ANYTIME,
      ...CONTACT_ANYTIME_LOWER,
    },
    visit: {
      d1: dateRule(juniorAug1, "1 August before 11th grade", "D1 visit rule (checked 11 Nov 2026)", {
        projected: true,
        note: "The printed dates for boys and girls did not match in our sources. Look up the exact day before booking travel.",
      }),
      d2: D2_VISIT_JUN15,
      ...VISIT_ANY_LOWER,
    },
    writtenOffer: {
      d1: dateRule(seniorAug1, "1 August of 12th grade", "D1 aid offer table, checked 11 Nov 2026", {
        note: "Before this day a school may not put aid in writing. The paper does not hold a roster spot and it goes away if the athlete does not qualify. Early signing opens the second Wednesday in November.",
      }),
      d2: dateRule(seniorSep1, "1 September of 12th grade", "D2 award letter table, checked 11 Nov 2026", {
        note: "A D2 award letter is a financial aid document, one school year at a time.",
      }),
    },
    roster: ROSTER_BASKETBALL,
  },
  {
    key: "womens-basketball",
    label: "Women's Basketball",
    noun: "basketball",
    filmNote: "Summer teams are watched by the NCAA at approved events only. Ask before paying for a showcase.",
    sopsSlug: "womens-basketball",
    contact: {
      d1: dateRule(after10thJun1, "1 June after 10th grade", "D1 Bylaw 13.1.3.1.5", {
        note: "Calls, texts and email may not start before this day. A coach may not meet an athlete off campus before 1 September of 12th grade (13.1.1.1.5). Different from the men's game and from almost every other sport.",
      }),
      d2: D2_CONTACT_ANYTIME,
      ...CONTACT_ANYTIME_LOWER,
    },
    visit: {
      d1: dateRule(juniorJan1, "1 January of 11th grade", "D1 Bylaw 13.6.2.1.6", {
        note: "The paid visit may not start before this day. Five official visits in a lifetime, and a certification account before the first one.",
      }),
      d2: D2_VISIT_JUN15,
      ...VISIT_ANY_LOWER,
    },
    writtenOffer: {
      d1: dateRule(seniorAug1, "1 August of 12th grade", "D1 aid offer table, checked 11 Nov 2026", {
        note: "Before this day a school may not put aid in writing. Early signing opens the second Wednesday in November of 12th grade.",
      }),
      d2: dateRule(seniorSep1, "1 September of 12th grade", "D2 award letter table, checked 11 Nov 2026", {
        note: "A D2 award letter is a financial aid document, one school year at a time.",
      }),
    },
    roster: ROSTER_BASKETBALL,
  },
  {
    key: "baseball",
    label: "Baseball",
    noun: "baseball",
    filmNote: "Keep full-game links and one reel a coach will finish watching. Verified times beat hand-timed ones.",
    sopsSlug: null,
    contact: {
      d1: dateRule(juniorAug1, "1 August of 11th grade", "D1 Bylaws 13.1.3.1.1, 13.4.1.1", {
        note: "Baseball is different: D1 baseball opens 1 August of junior year, not the June 15 date most sports use. Before this day a coach cannot answer a recruiting message, even one the athlete sends first. Off-campus contact and recruiting talk at college camps open 1 September of 11th grade (13.1.1.1.1, 13.7.1.2).",
      }),
      d2: anytimeRule("Any time by phone, text or email", "D2 Bylaws 13.1.1.1, 13.3.1.2", {
        note: "In-person contact and paid visits open 15 June after 10th grade.",
      }),
      ...CONTACT_ANYTIME_LOWER,
    },
    visit: {
      d1: dateRule(juniorSep1, "1 September of 11th grade", "D1 Bylaws 13.6.2.1.2, 13.7.1.2", {
        note: "Official visits, unofficial visits involving the athletics department, and off-campus contact all open on this day. The recruiting calendar can still close a specific week.",
      }),
      d2: D2_VISIT_JUN15,
      ...VISIT_ANY_LOWER,
    },
    writtenOffer: {
      d1: {
        kind: "date",
        anchor: (g: number) => {
          const first = new Date(Date.UTC(g - 1, 10, 1)).getUTCDay();
          const day = 1 + ((3 - first + 7) % 7) + 7;
          return { year: g - 1, month: 11, day };
        },
        when: "Second Wednesday in November of 12th grade",
        cite: "D1 Bylaw 13.02.13.1(f)",
        projected: true,
        note: "Projected from the rule text: signing opens this day. No penalty for signing later, but an offer can expire, and signing ends recruiting by other schools.",
      },
    },
    roster: ROSTER_BASEBALL,
  },
  {
    key: "track-field",
    label: "Track & Field",
    noun: "track and field",
    filmNote: "Verified time is what counts: a third party took the number. Hand-timed runs about 0.2 seconds fast.",
    sopsSlug: null,
    contact: {
      d1: dateRule(after10thJun15, "15 June after 10th grade", "D1 Bylaws 13.1.1.1.9, 13.1.3.1, 13.4.1", {
        note: "Changed 7 October 2026: track and cross country off-campus contact now opens the same day as calls and texts. Older guides still say 1 August. Written offers may not arrive before 1 August of 12th grade (13.9.3.1).",
      }),
      d2: D2_CONTACT_JUN15,
      ...CONTACT_ANYTIME_LOWER,
    },
    visit: {
      d1: dateRule(juniorAug1, "1 August of 11th grade", "D1 Bylaws 13.6.2.1.1, 13.7.1.1", {
        note: "Official visits and unofficial visits involving the athletics department may begin. Visiting too early is a violation.",
      }),
      d2: D2_VISIT_JUN15,
      ...VISIT_ANY_LOWER,
    },
    writtenOffer: {
      d1: dateRule(seniorAug1, "1 August of 12th grade", "D1 Bylaw 13.9.3.1", {
        note: "A written athletics aid offer cannot come before this day. Compare any offer against the full net price.",
      }),
    },
    roster: ROSTER_MODEL,
  },
  {
    key: "softball",
    label: "Softball",
    noun: "softball",
    filmNote: "The club season is where college staffs watch. Keep the club schedule in the email and full-game links ready.",
    sopsSlug: null,
    contact: {
      d1: commonContactD1Jun15(true),
      d2: D2_CONTACT_JUN15,
      ...CONTACT_ANYTIME_LOWER,
    },
    visit: {
      d1: GENERIC_VISIT_D1,
      d2: D2_VISIT_JUN15,
      ...VISIT_ANY_LOWER,
    },
    writtenOffer: {},
    roster: ROSTER_MODEL,
  },
  {
    key: "mens-soccer",
    label: "Men's Soccer",
    noun: "soccer",
    filmNote: "One reel a coach will finish watching, plus full-game links. Keep the highlight reel under the length coaches actually watch.",
    sopsSlug: null,
    contact: {
      d1: commonContactD1Jun15(true),
      d2: D2_CONTACT_JUN15,
      ...CONTACT_ANYTIME_LOWER,
    },
    visit: {
      d1: GENERIC_VISIT_D1,
      d2: D2_VISIT_JUN15,
      ...VISIT_ANY_LOWER,
    },
    writtenOffer: {},
    roster: ROSTER_MODEL,
  },
  {
    key: "womens-soccer",
    label: "Women's Soccer",
    noun: "soccer",
    filmNote: "One reel a coach will finish watching, plus full-game links. The club schedule matters more than the camp brochure.",
    sopsSlug: null,
    contact: {
      d1: commonContactD1Jun15(true),
      d2: D2_CONTACT_JUN15,
      ...CONTACT_ANYTIME_LOWER,
    },
    visit: {
      d1: GENERIC_VISIT_D1,
      d2: D2_VISIT_JUN15,
      ...VISIT_ANY_LOWER,
    },
    writtenOffer: {},
    roster: ROSTER_MODEL,
  },
  {
    key: "womens-lacrosse",
    label: "Women's Lacrosse",
    noun: "lacrosse",
    filmNote: "One reel a coach will finish watching, plus full-game links and a measured profile.",
    sopsSlug: null,
    contact: {
      d1: commonContactD1Jun15(true),
      d2: D2_CONTACT_JUN15,
      ...CONTACT_ANYTIME_LOWER,
    },
    visit: {
      d1: GENERIC_VISIT_D1,
      d2: D2_VISIT_JUN15,
      ...VISIT_ANY_LOWER,
    },
    writtenOffer: {},
    roster: ROSTER_MODEL,
  },
  {
    key: "swimming",
    label: "Swimming",
    noun: "swimming",
    filmNote: "Times are the film in this sport: keep verified results with the meet name and the date next to each one.",
    sopsSlug: null,
    contact: {
      d1: commonContactD1Jun15(true),
      d2: D2_CONTACT_JUN15,
      ...CONTACT_ANYTIME_LOWER,
    },
    visit: {
      d1: GENERIC_VISIT_D1,
      d2: D2_VISIT_JUN15,
      ...VISIT_ANY_LOWER,
    },
    writtenOffer: {},
    roster: ROSTER_MODEL,
  },
  {
    key: "wrestling",
    label: "Wrestling",
    noun: "wrestling",
    filmNote: "Verified time and documented results beat claims. Keep one reel plus full-match links.",
    sopsSlug: null,
    contact: {
      d1: commonContactD1Jun15(true),
      d2: D2_CONTACT_JUN15,
      ...CONTACT_ANYTIME_LOWER,
    },
    visit: {
      d1: GENERIC_VISIT_D1,
      d2: D2_VISIT_JUN15,
      ...VISIT_ANY_LOWER,
    },
    writtenOffer: {},
    roster: ROSTER_MODEL,
  },
];

const DIVISIONS: Array<{ key: DivisionKey; label: string }> = [
  { key: "d1", label: "NCAA D1" },
  { key: "d2", label: "NCAA D2" },
  { key: "d3", label: "NCAA D3" },
  { key: "naia", label: "NAIA" },
  { key: "njcaa", label: "NJCAA" },
];

const GRAD_YEARS: GradYear[] = [2026, 2027, 2028, 2029, 2030];

/* ------------------------------- status ------------------------------- */

type StatusKey = "open" | "prep" | "late";

interface StatusInfo {
  key: StatusKey;
  stamp: string;
  headline: string;
  body: string;
  color: string;
  border: string;
}

const STATUS_OPEN: StatusInfo = {
  key: "open",
  stamp: "COACH CONTACT OPEN NOW",
  headline: "The coach may legally contact your athlete today",
  body: "Calls, texts and email are open on this date for this sport and division. Silence from here on is a choice, not a rule.",
  color: "#15803d",
  border: "#15803d",
};

const STATUS_PREP: StatusInfo = {
  key: "prep",
  stamp: "PRE-CONTACT PREPARATION WINDOW",
  headline: "Nothing is open yet, and that is the advantage",
  body: "The contact date has not arrived for this sport and class year. The list, the film and the grades are the whole job right now.",
  color: "#1d4ed8",
  border: "#1d4ed8",
};

const STATUS_LATE: StatusInfo = {
  key: "late",
  stamp: "LATE-CYCLE ROSTER SEARCH",
  headline: "This is signing season and roster math, not introductions",
  body: "The class year is at the end of the calendar. Portal transfers fill most seats first, paper comes due, and every week costs options.",
  color: "#b91c1c",
  border: "#b91c1c",
};

function gradeNowOf(gradYear: number): number {
  /* School year 2026-27: class of 2027 is in 12th grade. */
  return 2039 - gradYear;
}

/* ------------------------------- moves -------------------------------- */

function movesFor(
  sport: SportConfig,
  divisionLabel: string,
  gradYear: number,
  contact: ResolvedWindow,
  visit: ResolvedWindow,
): string[] {
  const gradeNow = gradeNowOf(gradYear);

  if (gradYear <= 2027) {
    return [
      "Ask for the number and the date in the same email this week. If a coach says the program wants an athlete and no paper follows, the coach is still shopping.",
      gradYear === 2026
        ? `Run the roster search, not the introduction tour. Portal transfers fill most seats first, so write the ${divisionLabel} and lower-level programs that still carry ${sport.noun} rosters. D3, NAIA and junior college coaches may answer any time.`
        : `This is signing season. Do not sign early just to feel settled: once the athlete signs, every other school must stop contacting. Compare each offer against the real cost of the school.`,
      "Read the paper before anything is signed. There is no National Letter of Intent any more: what gets signed is a written offer of athletics aid from one school, and it binds that school only.",
    ];
  }

  if (contact.kind === "anytime" || (contact.date !== null && toUtc(contact.date) <= Date.now())) {
    return [
      `Send the full email round this week to the position coach, not the head coach: film, current grades, an unweighted GPA on a 4.0 scale, and measured numbers with the device and date next to each one.`,
      `Ask in writing who will be evaluating ${sport.noun} film and when, then log every answer with the date. "We talked" becomes "you emailed me on 12 November and said a spot was open."`,
      visit.date !== null && toUtc(visit.date) <= Date.now()
        ? `Ask for the paid visit by email and name the dates the family can travel. ${sport.label} visits are allowed from ${fmtStamp(visit.date)}.`
        : `Put the visit window on the calendar now: ${visit.when.toLowerCase()}. Ask for the paid visit before camp season eats the calendar, and open the NCAA Eligibility Center certification account ($110 domestic, fee waivers possible) before any D1 official visit.`,
    ];
  }

  return [
    `Build the list of 40 to 55 schools across every level that fits, before any coach can call. The list is the work right now, and it is free.`,
    `Make the film once, properly. ${sport.filmNote} Send grades to every school on the list each semester.`,
    gradeNow <= 10
      ? "Have the counselor check every course against the NCAA-approved list now. A bad schedule is fixed in 9th or 10th grade, not in 12th."
      : "Have the counselor check every course against the NCAA-approved list this month. The core GPA starts locking before senior year.",
  ];
}

/* ------------------------------ component ----------------------------- */

export function RecruitingWindowFinder({ compact = false }: { compact?: boolean }) {
  const [sportKey, setSportKey] = useState<SportKey>("football");
  const [gradYear, setGradYear] = useState<GradYear>(2029);
  const [divisionKey, setDivisionKey] = useState<DivisionKey>("d1");

  const sport = useMemo(() => {
    const found = SPORTS.find((s) => s.key === sportKey);
    return found ?? SPORTS[0];
  }, [sportKey]);

  const divisionLabel = useMemo(
    () => (DIVISIONS.find((d) => d.key === divisionKey)?.label ?? "NCAA D1"),
    [divisionKey],
  );

  const contact = useMemo(
    () => resolveWindow(sport.contact[divisionKey], gradYear),
    [sport, divisionKey, gradYear],
  );
  const visit = useMemo(
    () => resolveWindow(sport.visit[divisionKey], gradYear),
    [sport, divisionKey, gradYear],
  );
  const writtenOfferSpec = sport.writtenOffer[divisionKey];
  const writtenOffer = useMemo(
    () => (writtenOfferSpec ? resolveWindow(writtenOfferSpec, gradYear) : null),
    [writtenOfferSpec, gradYear],
  );
  const roster = sport.roster[divisionKey];

  const now = useMemo(() => new Date(), []);
  const todayStamp = fmtStamp({
    year: now.getFullYear(),
    month: now.getMonth() + 1,
    day: now.getDate(),
  });

  const status: StatusInfo = useMemo(() => {
    if (gradYear <= 2027) return STATUS_LATE;
    const openNow =
      contact.kind === "anytime" ||
      (contact.date !== null && toUtc(contact.date) <= Date.UTC(now.getFullYear(), now.getMonth(), now.getDate()));
    return openNow ? STATUS_OPEN : STATUS_PREP;
  }, [contact, gradYear, now]);

  const moves = useMemo(
    () => movesFor(sport, divisionLabel, gradYear, contact, visit),
    [sport, divisionLabel, gradYear, contact, visit],
  );

  const sopsHref = sport.sopsSlug ? `/sops?sport=${sport.sopsSlug}` : "/sops";

  function askGuide() {
    const prompt =
      `My athlete plays ${sport.label} (Class of ${gradYear}, targeting ${divisionLabel}). ` +
      "What can college coaches legally do right now, and what are our top 3 priorities this month?";
    window.dispatchEvent(new CustomEvent("commitbook:ask", { detail: { prompt } }));
  }

  const pad = compact ? "p-4" : "p-6 sm:p-8";
  const gap = compact ? "gap-3" : "gap-5";

  return (
    <section
      aria-label="Recruiting window and roster cap calculator"
      className="w-full bg-[#f7f5f0] text-[#141413] font-sans"
    >
      <div className={`mx-auto w-full max-w-4xl ${compact ? "py-6" : "py-10 sm:py-14"} px-4 sm:px-6`}>
        {/* masthead */}
        <header className={compact ? "mb-4" : "mb-8"}>
          <p className="font-mono text-[11px] uppercase tracking-[0.14em] text-[#57534e]">
            The Commit Book · Rules checked 11 November 2026
          </p>
          <h2
            className={`font-serif ${
              compact ? "mt-2 text-2xl" : "mt-3 text-3xl sm:text-4xl"
            } leading-[1.1] text-[#141413]`}
          >
            The 30-Second Recruiting Window &amp; Roster Cap Calculator
          </h2>
          {!compact && (
            <p className="mt-3 max-w-2xl text-[15px] leading-relaxed text-[#57534e]">
              Pick the sport, the class year, and the division. The dates below come from the rule
              text and the printed calendars, with the bylaw next to each one. The roster number is
              what decides the odds, so it sits on the same card.
            </p>
          )}
        </header>

        {/* selectors */}
        <div className={`grid grid-cols-1 sm:grid-cols-3 ${gap}`}>
          <Selector
            id="rwf-sport"
            label="Sport"
            value={sportKey}
            onChange={(value) => setSportKey(value as SportKey)}
            options={SPORTS.map((s) => ({ value: s.key, label: s.label }))}
          />
          <Selector
            id="rwf-grad"
            label="Graduation year"
            value={String(gradYear)}
            onChange={(value) => setGradYear(Number(value) as GradYear)}
            options={GRAD_YEARS.map((year) => ({ value: String(year), label: `Class of ${year}` }))}
          />
          <Selector
            id="rwf-division"
            label="Target division"
            value={divisionKey}
            onChange={(value) => setDivisionKey(value as DivisionKey)}
            options={DIVISIONS.map((d) => ({ value: d.key, label: d.label }))}
          />
        </div>

        {/* diagnostic card */}
        <article
          className={`mt-6 border border-[#e5e0d6] bg-white ${pad}`}
          aria-live="polite"
        >
          {/* status stamp */}
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div className="min-w-0">
              <p className="font-mono text-[11px] uppercase tracking-[0.14em] text-[#57534e]">
                Live status · as of {todayStamp}
              </p>
              <h3 className={`font-serif ${compact ? "mt-1 text-xl" : "mt-2 text-2xl"} leading-tight`}>
                {status.headline}
              </h3>
              <p className="mt-2 max-w-xl text-[14px] leading-relaxed text-[#57534e]">{status.body}</p>
            </div>
            <p
              className="shrink-0 border-2 px-3 py-2 font-mono text-[11px] font-medium uppercase tracking-[0.12em]"
              style={{ color: status.color, borderColor: status.border }}
            >
              <span className="inline-flex items-center gap-2">
                <Stamp size={14} aria-hidden="true" />
                {status.stamp}
              </span>
            </p>
          </div>

          {/* computed rows */}
          <dl className={`mt-6 border-t border-[#e5e0d6]`}>
            <Row label="Coach may first contact you">
              <div>
                {contact.kind === "date" && contact.date ? (
                  <p className="font-mono tabular-nums text-[17px] text-[#141413]">
                    {fmtStamp(contact.date)}
                  </p>
                ) : contact.kind === "anytime" ? (
                  <p className="font-mono tabular-nums text-[17px] text-[#15803d]">ANY TIME</p>
                ) : (
                  <p className="font-mono tabular-nums text-[17px] text-[#b91c1c]">NOT PRINTED</p>
                )}
                <p className="mt-1 text-[13px] leading-relaxed text-[#57534e]">{contact.when}</p>
                {contact.note && (
                  <p className="mt-1 text-[13px] leading-relaxed text-[#57534e]">{contact.note}</p>
                )}
                <p className="mt-1 font-mono text-[11px] uppercase tracking-[0.12em] text-[#57534e]">
                  {contact.cite}
                  {contact.projected ? " · PROJECTED" : ""}
                </p>
              </div>
            </Row>

            <Row label="Official visit opens">
              <div>
                {visit.date ? (
                  <p className="font-mono tabular-nums text-[17px] text-[#141413]">
                    {fmtStamp(visit.date)}
                    {sport.key === "football" && divisionKey === "d1" ? (
                      <span className="text-[#57534e]">
                        {" "}
                        to {fmtStamp(footballVisitClose(visit.date.year))}
                      </span>
                    ) : null}
                  </p>
                ) : (
                  <p className="font-mono tabular-nums text-[17px] text-[#b91c1c]">NOT PRINTED</p>
                )}
                <p className="mt-1 text-[13px] leading-relaxed text-[#57534e]">{visit.when}</p>
                {visit.note && (
                  <p className="mt-1 text-[13px] leading-relaxed text-[#57534e]">{visit.note}</p>
                )}
                <p className="mt-1 font-mono text-[11px] uppercase tracking-[0.12em] text-[#57534e]">
                  {visit.cite}
                  {visit.projected ? " · PROJECTED" : ""}
                </p>
              </div>
            </Row>

            {writtenOffer ? (
              <Row label="Earliest written aid offer">
                <div>
                  {writtenOffer.date ? (
                    <p className="font-mono tabular-nums text-[17px] text-[#141413]">
                      {fmtStamp(writtenOffer.date)}
                    </p>
                  ) : (
                    <p className="font-mono tabular-nums text-[17px] text-[#b91c1c]">NOT PRINTED</p>
                  )}
                  <p className="mt-1 text-[13px] leading-relaxed text-[#57534e]">{writtenOffer.when}</p>
                  {writtenOffer.note && (
                    <p className="mt-1 text-[13px] leading-relaxed text-[#57534e]">{writtenOffer.note}</p>
                  )}
                  <p className="mt-1 font-mono text-[11px] uppercase tracking-[0.12em] text-[#57534e]">
                    {writtenOffer.cite}
                    {writtenOffer.projected ? " · PROJECTED" : ""}
                  </p>
                </div>
              </Row>
            ) : null}

            <Row label="Roster cap / scholarship model">
              <div>
                <p className="font-mono tabular-nums text-[15px] font-medium text-[#141413]">
                  {roster.headline}
                </p>
                <p className="mt-1 text-[13px] leading-relaxed text-[#57534e]">{roster.detail}</p>
                <p className="mt-1 font-mono text-[11px] uppercase tracking-[0.12em] text-[#57534e]">
                  {roster.verified
                    ? "Verified 11 Nov 2026 against the rule text"
                    : "Model only: the exact number is not in our checked rulebook. Ask the school for its own paper."}
                </p>
              </div>
            </Row>
          </dl>

          {/* next moves */}
          <div className="mt-6 border border-[#e5e0d6] bg-[#f7f5f0] p-4 sm:p-5">
            <p className="flex items-center gap-2 font-mono text-[11px] uppercase tracking-[0.14em] text-[#57534e]">
              <ClipboardList size={14} aria-hidden="true" />
              Your next 3 moves this week · {sport.label} · class of {gradYear}
            </p>
            <ol className="mt-3 space-y-3">
              {moves.map((move, index) => (
                <li key={index} className="flex gap-3">
                  <span className="mt-[2px] font-mono tabular-nums text-[12px] text-[#1d4ed8]">
                    {String(index + 1).padStart(2, "0")}
                  </span>
                  <span className="text-[14px] leading-relaxed text-[#141413]">{move}</span>
                </li>
              ))}
            </ol>
          </div>
        </article>

        {/* action bar */}
        <div className={`mt-6 flex flex-wrap items-center ${compact ? "gap-2" : "gap-3"}`}>
          <a
            href={sopsHref}
            className="inline-flex items-center gap-2 border border-[#e5e0d6] bg-white px-4 py-2.5 text-[13px] font-medium text-[#141413] transition-colors hover:border-[#141413]"
          >
            <CalendarDays size={15} aria-hidden="true" />
            {sport.sopsSlug ? `Open the ${sport.label} SOPs` : "Open the recruiting SOPs"}
            <ArrowRight size={14} aria-hidden="true" />
          </a>
          <a
            href="/start"
            className="inline-flex items-center gap-2 bg-[#1d4ed8] px-4 py-2.5 text-[13px] font-medium text-white transition-colors hover:bg-[#1e40af]"
          >
            Get Your Free Printable Plan
            <ArrowRight size={14} aria-hidden="true" />
          </a>
          <button
            type="button"
            onClick={askGuide}
            className="inline-flex items-center gap-2 border border-[#141413] bg-[#141413] px-4 py-2.5 text-[13px] font-medium text-white transition-colors hover:bg-[#3d3d3d]"
          >
            <MessageSquareText size={15} aria-hidden="true" />
            Ask Scout About My Window
          </button>
        </div>

        {/* footer note */}
        <p className="mt-6 max-w-2xl text-[12px] leading-relaxed text-[#57534e]">
          Education, not legal advice. Dates marked PROJECTED are worked out from the rule text, not
          printed by the NCAA yet, so treat them as one week early or one week late until the
          calendar lands. The NCAA Eligibility Center makes the final call on school rules, and each
          school decides its own aid.
        </p>
      </div>
    </section>
  );
}

function Row({ label, children }: { label: string; children: ReactNode }) {
  return (
    <div className="grid grid-cols-1 gap-2 border-b border-[#e5e0d6] py-4 sm:grid-cols-[220px_1fr] sm:gap-6">
      <dt className="font-mono text-[11px] uppercase tracking-[0.14em] text-[#57534e]">{label}</dt>
      <dd className="min-w-0">{children}</dd>
    </div>
  );
}

function Selector({
  id,
  label,
  value,
  onChange,
  options,
}: {
  id: string;
  label: string;
  value: string;
  onChange: (value: string) => void;
  options: Array<{ value: string; label: string }>;
}) {
  return (
    <label htmlFor={id} className="block">
      <span className="font-mono text-[11px] uppercase tracking-[0.14em] text-[#57534e]">
        {label}
      </span>
      <span className="relative mt-2 block">
        <select
          id={id}
          value={value}
          onChange={(event) => onChange(event.target.value)}
          className="w-full appearance-none border border-[#e5e0d6] bg-white px-3 py-2.5 pr-10 text-[15px] text-[#141413] focus:outline-none focus-visible:ring-2 focus-visible:ring-[#1d4ed8]"
        >
          {options.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
        <ChevronDown
          size={16}
          aria-hidden="true"
          className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-[#57534e]"
        />
      </span>
    </label>
  );
}

export default RecruitingWindowFinder;
