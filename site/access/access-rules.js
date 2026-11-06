/* Access rules table. Every NCAA date below is copied from site/data.js (system of record,
   2026-27 NCAA Division I Manual, verified_on 2026-11-05) for the Class of 2029 and expressed
   as an OFFSET from the class so other classes shift by whole years. Where we have no verified
   source the value is null and the UI says "verify with the NCAA sport calendar". Nothing invented. */
(function (root) {
  var VERIFIED_ON = "2026-11-05", MANUAL = "2026-27 NCAA Division I Manual", REF_CLASS = 2029;
  var URL_D1 = "https://web3.ncaa.org/lsdbi/reports/getReport/90008";
  var URL_D2 = "https://web3.ncaa.org/lsdbi/reports/getReport/90010";
  var URL_D3 = "https://web3.ncaa.org/lsdbi/reports/getReport/90011";
  /* md = month-day, yo = years added to the class year to get the calendar year (class 2029 -> 2027 = -2) */
  var SPORTS = {
    football: { label: "Football", d1: {
      coach: { md: "06-15", yo: -2, rule: "D1 Bylaws 13.1.3.1, 13.4.1", note: "After sophomore year, coaches may call, text and send recruiting messages." },
      unofficial: { md: null, rule: "D1 Bylaws 13.1.3.1, 13.4.1", note: "Unofficial visits involving the athletics department are allowed at any age, subject to the NCAA recruiting calendar (quiet and dead periods)." },
      official: { md: "04-01", yo: -1, rule: "D1 Bylaws 13.6.2.1.7, 13.6.3", note: "Junior-year window opens April 1 and needs a transcript and an Eligibility Center certification account." },
      offcampus: { md: "01-01", yo: -1, rule: "D1 Bylaws 13.1.1.1.6, 13.1.5.3", note: "Off-campus contact opens January 1 of junior year." } } },
    baseball: { label: "Baseball", d1: {
      coach: { md: "08-01", yo: -2, rule: "D1 Bylaws 13.1.3.1.1, 13.4.1.1", note: "D1 baseball opens August 1 of junior year, not the June 15 date most sports use." },
      unofficial: { md: "09-01", yo: -2, rule: "D1 Bylaws 13.1.1.1.1, 13.6.2.1.2, 13.7.1.2", note: "Unofficial visits involving the athletics department open September 1 of junior year." },
      official: { md: "09-01", yo: -2, rule: "D1 Bylaws 13.1.1.1.1, 13.6.2.1.2, 13.7.1.2", note: "Official visits open September 1 of junior year." },
      offcampus: { md: "09-01", yo: -2, rule: "D1 Bylaws 13.1.1.1.1, 13.6.2.1.2, 13.7.1.2", note: "Off-campus contact opens September 1 of junior year." } } },
    track: { label: "Track & Field / XC", d1: {
      coach: { md: "06-15", yo: -2, rule: "D1 Bylaws 13.1.1.1.9, 13.1.3.1, 13.4.1", note: "Changed October 7, 2026: calls, messages and off-campus contact open together June 15 after sophomore year. Older guides still say August 1." },
      unofficial: { md: "08-01", yo: -2, rule: "D1 Bylaws 13.6.2.1.1, 13.7.1.1", note: "Unofficial visits involving the athletics department open August 1 of junior year." },
      official: { md: "08-01", yo: -2, rule: "D1 Bylaws 13.6.2.1.1, 13.7.1.1", note: "Official visits open August 1 of junior year." },
      offcampus: { md: "06-15", yo: -2, rule: "D1 Bylaws 13.1.1.1.9, 13.1.3.1, 13.4.1", note: "Off-campus contact opens with calls and messages." } } }
  };
  var DIVISIONS = ["NCAA D1", "NCAA D2", "NCAA D3", "NAIA", "NJCAA"];
  var CLASSES = [2026, 2027, 2028, 2029, 2030];
  function iso(year, md) { return year + "-" + md; }
  function d1Row(s, key, cls) {
    var r = SPORTS[s].d1[key];
    if (!r.md) return { date: null, anytime: true, rule: r.rule, scope: "D1-specific", note: r.note };
    return { date: iso(cls + r.yo, r.md), rule: r.rule, scope: "D1-specific", note: r.note, url: URL_D1 };
  }
  function lookup(sport, division, cls) {
    if (!SPORTS[sport]) throw new Error("unknown sport");
    if (DIVISIONS.indexOf(division) < 0) throw new Error("unknown division");
    cls = Number(cls);
    if (CLASSES.indexOf(cls) < 0) throw new Error("unknown class");
    var out = { sport: sport, division: division, cls: cls, verified_on: VERIFIED_ON, manual: MANUAL, rows: {}, banner: "" };
    var athlete = { date: null, anytime: true, rule: "D1 Bylaw 13.4.1 (limits what coaches send or say, not what a prospect writes)", scope: "all divisions",
      note: "A prospect or family may write a coach or fill in a questionnaire at any time. The dates below limit the coach, not you. A coach may not be able to answer before their date." };
    out.rows.athlete = athlete;
    if (division === "NCAA D1") {
      out.rows.coach = d1Row(sport, "coach", cls); out.rows.unofficial = d1Row(sport, "unofficial", cls);
      out.rows.official = d1Row(sport, "official", cls); out.rows.offcampus = d1Row(sport, "offcampus", cls);
      out.banner = "These dates are D1-specific. D2, D3, NAIA and NJCAA follow different rules. Check your sport calendar for dead and quiet periods.";
    } else if (division === "NCAA D2") {
      out.rows.coach = { date: null, anytime: true, rule: "D2 Bylaws 13.1.1.1, 13.3.1.2", scope: "D2-specific", note: "D2 calls, texts and emails are allowed at any time.", url: URL_D2 };
      out.rows.unofficial = { date: null, anytime: true, rule: "D2 Bylaws 13.1.1.1, 13.3.1.2", scope: "D2-specific", note: "Verify unofficial-visit limits for your sport with the school's compliance office." };
      out.rows.official = { date: iso(cls - 2, "06-15"), rule: "D2 Bylaws 13.1.1.1, 13.3.1.2", scope: "D2-specific", note: "D2 in-person contact and official visits may begin June 15 after sophomore year (verified in the baseball record of site/data.js; confirm for your sport).", url: URL_D2 };
      out.rows.offcampus = { date: iso(cls - 2, "06-15"), rule: "D2 Bylaws 13.1.1.1, 13.3.1.2", scope: "D2-specific", note: "D2 in-person contact begins June 15 after sophomore year.", url: URL_D2 };
      out.banner = "These are D2 rules, not D1. They differ from the D1 dates for the same sport.";
    } else if (division === "NCAA D3") {
      out.rows.coach = { date: null, anytime: true, rule: "D3 Bylaw 13.6.1.1.1 (visits); contact has almost no timing limits", scope: "D3-specific", note: "D3 has almost no timing limits on calls and messages. Verify with the school.", url: URL_D3 };
      out.rows.unofficial = { date: null, anytime: true, rule: "D3 Bylaw 13.6.1.1.1", scope: "D3-specific", note: "Verify with the school's compliance office.", url: URL_D3 };
      out.rows.official = { date: iso(cls - 1, "01-01"), rule: "D3 Bylaw 13.6.1.1.1", scope: "D3-specific", note: "D3 paid visits open January 1 of junior year. D3 offers no athletic scholarships.", url: URL_D3 };
      out.rows.offcampus = { date: null, verify: true, rule: "Not verified in our data", scope: "D3-specific", note: "We have not verified a D3 off-campus contact date. Ask the school's compliance office." };
      out.banner = "These are D3 rules, not D1. Fewer timing limits apply.";
    } else if (division === "NAIA") {
      var na = { date: null, anytime: true, rule: "No NCAA bylaw applies. See naia.org/why-naia/recruiting", scope: "NAIA (not NCAA)", note: "NAIA has no recruiting calendar and no limit on communication per its recruiting page. Confirm visit rules with each school.", url: "https://www.naia.org/why-naia/recruiting" };
      ["coach", "unofficial", "official", "offcampus"].forEach(function (k) { out.rows[k] = na; });
      out.banner = "NAIA is not governed by NCAA bylaws. No NCAA citation applies.";
    } else {
      var nj = { date: null, verify: true, rule: "No NCAA bylaw applies. NJCAA rules: njcaa.org", scope: "NJCAA (not NCAA)", note: "We have not verified NJCAA contact or visit dates. Ask the program and check njcaa.org." };
      ["coach", "unofficial", "official", "offcampus"].forEach(function (k) { out.rows[k] = nj; });
      out.banner = "NJCAA is not governed by NCAA bylaws. We show no date we have not verified.";
    }
    return out;
  }
  var api = { SPORTS: SPORTS, DIVISIONS: DIVISIONS, CLASSES: CLASSES, VERIFIED_ON: VERIFIED_ON, MANUAL: MANUAL, REF_CLASS: REF_CLASS, lookup: lookup };
  root.AccessRules = api;
})(typeof window !== "undefined" ? window : globalThis);
