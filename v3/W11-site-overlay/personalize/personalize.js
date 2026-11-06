/* The Commit Book: Denver Metro personalization (W11-3).
 * Faithful JS port of v3/W10-personalization/personalize/{engine,freshness,geo,ics,intake}.py.
 * Parent-safe: the ONLY inputs are sport, class year, ZIP3 area, budget band, goal level.
 * No names, birthdates, phones, schools or schedules are asked for, stored, or sent anywhere.
 * Nothing leaves the browser: no fetch beyond the static seed.json, no cookies, no storage.
 */
(function (root) {
  "use strict";

  // ---------- freshness.py ----------
  var EVENT_NEAR_DAYS = 60, EVENT_FAR_RECHECK = 7, EVENT_NEAR_WINDOW = 30, PROVIDER_RECHECK_DAYS = 90;
  var EVENT_TYPES = ["college_prospect_camp", "showcase", "camp", "recreational_league"];

  // Python date.fromisoformat: strict YYYY-MM-DD. Returns UTC-midnight ms or null.
  function parseD(s) {
    if (typeof s !== "string" || !/^\d{4}-\d{2}-\d{2}$/.test(s)) return null;
    var y = +s.slice(0, 4), m = +s.slice(5, 7), d = +s.slice(8, 10);
    var t = Date.UTC(y, m - 1, d);
    var c = new Date(t);
    if (c.getUTCFullYear() !== y || c.getUTCMonth() !== m - 1 || c.getUTCDate() !== d) return null;
    return t;
  }
  var DAY = 86400000;
  function daysBetween(a, b) { return Math.round((a - b) / DAY); }
  function iso(t) { return new Date(t).toISOString().slice(0, 10); }

  function recheckWindowDays(row, today) {
    if (EVENT_TYPES.indexOf(row.type) >= 0) {
      var starts = (row.dates || []).map(function (x) { return parseD(x.start); }).filter(function (x) { return x !== null; });
      if (starts.length) {
        var delta = daysBetween(Math.min.apply(null, starts), today);
        if (delta >= 0 && delta <= EVENT_NEAR_DAYS) return EVENT_FAR_RECHECK;
      }
      return EVENT_NEAR_WINDOW;
    }
    return PROVIDER_RECHECK_DAYS;
  }

  function rowState(row, today) {
    var dates = row.dates || [];
    var ends = dates.map(function (x) { return parseD(x.end || x.start); }).filter(function (x) { return x !== null; });
    if (dates.length && ends.length && ends.every(function (e) { return e < today; }))
      return ["past", "all dated windows ended before " + iso(today)];
    if (row.status === "past") return ["past", "row marked past"];
    var readOn = parseD(row.read_on);
    if (readOn === null) return ["stale", "read_on missing or unparseable"];
    if (readOn > today) return ["stale", "read_on is in the future; cannot be trusted"];
    var age = daysBetween(today, readOn);
    var win = recheckWindowDays(row, today);
    if (age > win) return ["stale", "not recently checked (" + age + " days old, window " + win + ")"];
    var isEvent = EVENT_TYPES.indexOf(row.type) >= 0;
    if (row.status === "tbd" || (isEvent && !ends.length)) return ["tbd", "Not yet announced"];
    if (row.status === "stale") return ["stale", "row marked stale"];
    return ["bookable", "read " + age + " days ago, window " + win];
  }

  // ---------- geo.py (ZIP3 centroids, straight-line miles) ----------
  var ZIP3 = { "802": [39.74, -104.99], "801": [39.60, -104.85], "804": [39.75, -105.22],
               "809": [38.83, -104.82], "803": [40.02, -105.27] };
  function rad(x) { return x * Math.PI / 180; }
  function pyRound1(x) { // Python round(x, 1) is banker's-on-binary; matches Math.round for these values except exact halves
    var r = Math.round(x * 10) / 10;
    return r;
  }
  function miles(a, b) {
    var A = ZIP3[a], B = ZIP3[b];
    if (!A || !B) return null;
    var la1 = rad(A[0]), lo1 = rad(A[1]), la2 = rad(B[0]), lo2 = rad(B[1]);
    var h = Math.pow(Math.sin((la2 - la1) / 2), 2) + Math.cos(la1) * Math.cos(la2) * Math.pow(Math.sin((lo2 - lo1) / 2), 2);
    return pyRound1(3958.8 * 2 * Math.asin(Math.sqrt(h)));
  }
  // Python str(float): 0.0 prints "0.0", 12.2 prints "12.2". JS prints "0" for 0.0, so force one decimal.
  function pyFloat(x) { return Number.isInteger(x) ? x.toFixed(1) : String(x); }
  function band(m) {
    if (m === null) return "unknown";
    return m <= 15 ? "local" : m <= 40 ? "metro" : m <= 100 ? "regional" : "far";
  }

  // ---------- intake.py ----------
  var ALLOWED_FIELDS = ["sport", "class_year", "area", "budget_band", "goal_level"];
  var SPORTS = ["football", "basketball", "baseball", "softball", "hockey", "volleyball", "soccer",
                "lacrosse", "track", "wrestling", "swimming", "tennis", "golf"];
  var BUDGET_BANDS = { free: 0, low: 150, mid: 400, high: 1000, any: null };
  var GOAL_LEVELS = ["recreational", "development", "college_prospect"];
  var GOAL_TYPES = {
    recreational: ["recreational_league", "camp"],
    development: ["recreational_league", "camp", "strength_conditioning", "mental_performance"],
    college_prospect: ["college_prospect_camp", "showcase", "camp", "strength_conditioning", "mental_performance"]
  };
  function IntakeError(msg) { this.name = "IntakeError"; this.message = msg; }
  IntakeError.prototype = Object.create(Error.prototype);

  function zip3(area) {
    var s = String(area).trim();
    if (/^\d{3}$/.test(s)) return s;
    if (/^\d{5}$/.test(s)) return s.slice(0, 3); // full ZIP never retained
    throw new IntakeError("area must be a 3-digit ZIP prefix (a 5-digit ZIP is truncated to 3)");
  }
  function parseIntake(raw, todayYear) {
    todayYear = todayYear || 2026;
    if (raw === null || typeof raw !== "object" || Array.isArray(raw)) throw new IntakeError("intake must be an object");
    var extra = Object.keys(raw).filter(function (k) { return ALLOWED_FIELDS.indexOf(k) < 0; }).sort();
    if (extra.length) throw new IntakeError("disallowed intake field(s): " + extra.join(", ") + " (minimum-data rule: only " + ALLOWED_FIELDS.join(", ") + ")");
    var missing = ALLOWED_FIELDS.filter(function (f) { return !(f in raw); });
    if (missing.length) throw new IntakeError("missing intake field(s): " + missing.join(", "));
    var sport = String(raw.sport).trim().toLowerCase();
    if (SPORTS.indexOf(sport) < 0) throw new IntakeError("unsupported sport '" + sport + "'");
    var cyS = String(raw.class_year).trim();
    if (!/^[+-]?\d+$/.test(cyS)) throw new IntakeError("class_year must be a graduation year (not a birth date)");
    var cy = parseInt(cyS, 10);
    if (!(todayYear <= cy && cy <= todayYear + 12)) throw new IntakeError("class_year out of range (" + todayYear + ".." + (todayYear + 12) + ")");
    var bb = String(raw.budget_band).trim().toLowerCase();
    if (!(bb in BUDGET_BANDS)) throw new IntakeError("budget_band must be one of " + Object.keys(BUDGET_BANDS).sort().join(", "));
    var goal = String(raw.goal_level).trim().toLowerCase();
    if (GOAL_LEVELS.indexOf(goal) < 0) throw new IntakeError("goal_level must be one of " + GOAL_LEVELS.join(", "));
    return { sport: sport, class_year: cy, zip3: zip3(raw.area), budget_band: bb, budget_max_usd: BUDGET_BANDS[bb], goal_level: goal };
  }
  function gradeFor(classYear, ym) {
    var end = ym[0] + (ym[1] >= 8 ? 1 : 0);
    return 12 - (classYear - end);
  }

  // ---------- engine.py ----------
  var LABEL_RANK = { listed: 1, observed: 2, verified: 3, vetted: 4, endorsed: 5 };
  var PILOT_LABELS = ["listed", "observed", "verified"];
  var DISCLOSURE = "Ranked by fit, location, cost clarity, checkability and freshness. Not by who pays us.";
  var STANDING_NOTES = ["Not medical advice.", "We have not verified safety.",
    "Mental performance consulting is not a substitute for medical or mental-health care."];
  var BANNED = ["safe", "medically supervised", "prevents injury", "injury prevention", "treats", "cures",
    "guaranteed", "reduces anxiety", "improves mental health"];
  var PROVIDER_TYPES = ["strength_conditioning", "mental_performance"];
  var SAFEGUARDING_QUESTIONS = [
    "Do all coaches get a background check from a consumer reporting agency?",
    "Is annual mandatory-reporter training completed this year?",
    "Is a written prohibited-conduct / one-on-one interaction policy available?",
    "Is a first-aid/CPR/AED-certified adult present?",
    "Which named coach will work with my child, and what credential number can I check?"
  ];

  function highestLabel(row) {
    var vals = {}; var fl = row.field_labels || {};
    Object.keys(fl).forEach(function (k) { vals[fl[k]] = 1; });
    var ls = Object.keys(vals).filter(function (l) { return PILOT_LABELS.indexOf(l) >= 0; });
    if (!ls.length) return "listed";
    return ls.reduce(function (a, b) { return LABEL_RANK[b] > LABEL_RANK[a] ? b : a; });
  }
  function sportMatch(row, sport) {
    var sports = (row.sport || []).map(function (s) { return String(s).toLowerCase(); });
    if (sports.indexOf(sport) >= 0) return "exact";
    if (sports.indexOf("multi") >= 0) return "multi";
    return null;
  }
  function gradeMatch(row, grade, classYear) {
    var ag = row.ages_or_grades;
    if (!ag) return "unknown";
    if ("grades" in ag) return ag.grades.indexOf(grade) >= 0 ? "match" : "mismatch";
    if ("age_min" in ag) { var a = grade + 5; return (ag.age_min <= a && a <= ag.age_max + 1) ? "match" : "mismatch"; }
    if ("birth_years" in ag) { var by = classYear - 18; return (ag.birth_years[0] <= by && by <= ag.birth_years[1]) ? "match" : "mismatch"; }
    return "unknown";
  }
  function cost(row, budgetMax) {
    var items = row.price_items || [];
    if (!items.length) return ["unknown", 4];
    var usd = Math.min.apply(null, items.map(function (i) { return i.usd; }));
    if (budgetMax === null || budgetMax === undefined || usd <= budgetMax) return ["within", 15];
    return ["over", 0];
  }
  function verif(row) {
    var checks = (row.credential_checks || []).filter(function (c) { return c.status === "verified"; });
    if (checks.length) return 15;
    return (row.field_labels || {}).overall === "observed" ? 3 : 2;
  }
  function freshScore(row, today) {
    var ro = parseD(row.read_on);
    if (ro === null || ro > today) return 0;
    var age = daysBetween(today, ro);
    return age <= 7 ? 10 : age <= 30 ? 7 : 3;
  }
  function clean(text) {
    var out = text || "", low = out.toLowerCase();
    for (var i = 0; i < BANNED.length; i++) if (low.indexOf(BANNED[i]) >= 0)
      return "[claim withheld: provider text contained a restricted health/outcome claim]";
    return out;
  }
  function esc(n) { return n; }

  function personalize(profile, rows, today, includeStale) {
    rows = rows || [];
    var ty = new Date(today).getUTCFullYear(), tm = new Date(today).getUTCMonth() + 1;
    var grade = gradeFor(profile.class_year, [ty, tm]);
    var result = { disclosure: DISCLOSURE, standing_notes: STANDING_NOTES, as_of: iso(today), ranked: [],
      not_yet_announced: [], hidden: { past: 0, stale: 0, sport_mismatch: 0, grade_mismatch: 0, goal_mismatch: 0, malformed: 0 },
      stale_rows: [], empty_reason: null,
      profile_echo: { sport: profile.sport, class_year: profile.class_year, area_zip3: profile.zip3,
                      budget_band: profile.budget_band, goal_level: profile.goal_level } };
    if (!rows.length) { result.empty_reason = "No rows loaded. Nothing is shown rather than guessing."; return result; }
    var allowed = GOAL_TYPES[profile.goal_level];
    rows.forEach(function (row) {
      if (row === null || typeof row !== "object" || !row.entity_id || !row.url || !row.read_on) { result.hidden.malformed++; return; }
      var st = rowState(row, today), state = st[0], why = st[1];
      if (state === "past") { result.hidden.past++; return; }
      if (state === "stale") { result.hidden.stale++; if (includeStale) result.stale_rows.push({ entity_id: row.entity_id, reason: why }); return; }
      var sm = sportMatch(row, profile.sport);
      if (sm === null) { result.hidden.sport_mismatch++; return; }
      if (allowed.indexOf(row.type) < 0) { result.hidden.goal_mismatch++; return; }
      var gm = gradeMatch(row, grade, profile.class_year);
      if (gm === "mismatch") { result.hidden.grade_mismatch++; return; }
      var mi = miles(profile.zip3, (row.location_coarse || {}).zip3);
      var fit = (sm === "exact" ? 22 : 14) + (gm === "match" ? 10 : 4) + (allowed.indexOf(row.type) >= 0 ? 8 : 0);
      var geoS = mi === null ? 0 : mi <= 15 ? 20 : mi <= 40 ? 14 : mi <= 100 ? 7 : 2;
      var c = cost(row, profile.budget_max_usd), costState = c[0], costS = c[1];
      var v = verif(row), f = freshScore(row, today);
      var total = Math.min(40, fit) + geoS + costS + v + f;
      var item = {
        entity_id: row.entity_id, name: clean(row.name), type: row.type, score: total,
        tiebreak: row.source_is_aggregator ? 0 : 1,
        score_parts: { fit: Math.min(40, fit), geography: geoS, cost_clarity: costS, verifiability: v, freshness: f },
        reasons: ["sport: " + sm, "grade: " + gm,
          "distance: " + (mi === null ? "unknown" : pyFloat(mi) + " mi straight-line (" + band(mi) + ")"),
          "cost: " + costState, "freshness: " + why],
        highest_label: highestLabel(row), read_on: row.read_on, url: row.url, who_runs: row.who_runs || null,
        state: state, flags: [], dates: row.dates || [], miles: mi,
        price_items: row.price_items || [],
        location: (row.location_coarse || {}).city || null,
        credential_checks: (row.credential_checks || []).filter(function (cc) { return cc.status === "verified"; }),
        safeguarding: PROVIDER_TYPES.indexOf(row.type) >= 0 ? "questions_for_parent" : null
      };
      if (PROVIDER_TYPES.indexOf(row.type) >= 0) {
        item.safeguarding_questions = SAFEGUARDING_QUESTIONS;
        item.safeguarding_status = "not collected (no outreach); self-reported until a document is seen";
      }
      if (costState === "unknown") item.flags.push("price unknown");
      if (costState === "over") item.flags.push("over budget band");
      if (mi === null) item.flags.push("distance unknown");
      if (row.source_is_aggregator) item.flags.push("aggregator source: lead only, dates not verified");
      if ((row.dates || []).some(function (d) { return d.is_window; })) item.flags.push("date is a window, not a confirmed day");
      (state === "tbd" ? result.not_yet_announced : result.ranked).push(item);
    });
    result.ranked.sort(function (a, b) {
      return (b.score - a.score) || (b.tiebreak - a.tiebreak) || (a.entity_id < b.entity_id ? -1 : a.entity_id > b.entity_id ? 1 : 0);
    });
    result.not_yet_announced.sort(function (a, b) { return a.entity_id < b.entity_id ? -1 : a.entity_id > b.entity_id ? 1 : 0; });
    if (!result.ranked.length && !result.not_yet_announced.length)
      result.empty_reason = "No rows match this sport/grade/goal after the freshness gate. Nothing is invented to fill the list.";
    return result;
  }

  // ---------- ics.py (RFC 5545: CRLF line endings, escaped text, all-day DTEND exclusive) ----------
  function icsEsc(s) { return String(s).replace(/\\/g, "\\\\").replace(/;/g, "\\;").replace(/,/g, "\\,").replace(/\n/g, "\\n"); }
  function ymd(t) { return iso(t).replace(/-/g, ""); }
  function toIcs(result) {
    var lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//W10 personalization prototype//EN"];
    (result.ranked || []).forEach(function (it) {
      (it.dates || []).forEach(function (d, i) {
        var s = parseD(d.start), e0 = parseD(d.end || d.start);
        if (s === null || e0 === null) return;
        var desc = "Label: " + it.highest_label + ". Read on " + it.read_on + ". Source: " + it.url;
        if (d.is_window) desc += ". Date is a window, not a confirmed day; confirm with the organizer.";
        lines.push("BEGIN:VEVENT", "UID:" + it.entity_id + "-" + i + "@w10.invalid",
          "DTSTAMP:" + result.as_of.replace(/-/g, "") + "T000000Z",
          "DTSTART;VALUE=DATE:" + ymd(s), "DTEND;VALUE=DATE:" + ymd(e0 + DAY),
          "SUMMARY:" + icsEsc(it.name), "DESCRIPTION:" + icsEsc(desc), "END:VEVENT");
      });
    });
    lines.push("END:VCALENDAR");
    return lines.join("\r\n") + "\r\n";
  }

  var API = { parseD: parseD, pyFloat: pyFloat, rowState: rowState, recheckWindowDays: recheckWindowDays, miles: miles, band: band,
    parseIntake: parseIntake, IntakeError: IntakeError, gradeFor: gradeFor, personalize: personalize, toIcs: toIcs,
    highestLabel: highestLabel, ALLOWED_FIELDS: ALLOWED_FIELDS, SPORTS: SPORTS, BUDGET_BANDS: BUDGET_BANDS,
    GOAL_LEVELS: GOAL_LEVELS, GOAL_TYPES: GOAL_TYPES, ZIP3: ZIP3, SAFEGUARDING_QUESTIONS: SAFEGUARDING_QUESTIONS,
    DISCLOSURE: DISCLOSURE, STANDING_NOTES: STANDING_NOTES, iso: iso };
  root.CBPersonalize = API;
  if (typeof module !== "undefined" && module.exports) module.exports = API;
})(typeof window !== "undefined" ? window : globalThis);
