/* Pure client-side logic for the Access page. No network, no storage, no athlete data leaves the tab. */
(function (root) {
  var HYPE = ["elite", "guaranteed", "must-see", "must see", "best in the country", "can't miss", "cant miss", "generational", "mvp", "future pro", "top recruit", "five-star", "5-star", "unstoppable"];
  var PARENT = [/\bmy (son|daughter|child|kid|boy|girl)\b/i, /\bour (son|daughter|child|kid)\b/i, /\bwe are (looking|hoping|writing)\b/i, /\bas (his|her) (mom|mother|dad|father|parent)\b/i, /\bi am (his|her) (mom|mother|dad|father|parent)\b/i];
  var PROMISE = [/\bguarantee[sd]?\b/i, /\bfull[- ]ride\b/i, /\byou will (love|regret)\b/i, /\bdon'?t (miss|pass) (out|on)\b/i];
  function esc(s) { return String(s == null ? "" : s); }
  function subjectLine(f) {
    var parts = [];
    var head = [esc(f.gradYear), esc(f.position)].filter(Boolean).join(" ");
    if (head) parts.push(head);
    if (esc(f.metric).trim()) parts.push(esc(f.metric).trim());
    if (esc(f.gpa).trim()) parts.push(esc(f.gpa).trim().replace(/^gpa:?\s*/i, "") + " GPA");
    return parts.join(" \u2014 ");
  }
  function build(f) {
    var school = esc(f.school).trim() || "your program";
    var coach = esc(f.coachLast).trim() ? "Coach " + esc(f.coachLast).trim() : "Coach";
    var name = esc(f.firstName).trim() || "[first name]";
    var pos = esc(f.position).trim() || "[position/event]";
    var sport = esc(f.sport).trim();
    var metric = esc(f.metric).trim();
    var gpa = esc(f.gpa).trim();
    var film = esc(f.film).trim();
    var lines = [];
    lines.push(coach + ",", "");
    lines.push("My name is " + name + ". I am a " + pos + (sport ? " in " + sport : "") + " in the Class of " + (esc(f.gradYear) || "[year]") + ", and I am writing because I am interested in " + school + ".");
    if (metric) lines.push("My verified mark: " + metric + ".");
    if (gpa) lines.push("Academics: " + (/gpa/i.test(gpa) ? gpa : gpa + " GPA") + (esc(f.interest).trim() ? "; I am interested in " + esc(f.interest).trim() + "." : "."));
    else if (esc(f.interest).trim()) lines.push("I am interested in studying " + esc(f.interest).trim() + ".");
    if (film) lines.push("My film: " + film);
    lines.push("", "If there is anything else you would like from me, I will send it. I understand if the timing is not right yet.", "", "Thank you for your time.", name);
    var dm = coach + ", I am " + name + ", " + pos + ", Class of " + (esc(f.gradYear) || "[year]") + (metric ? ", " + metric : "") + (gpa ? ", " + gpa + (/gpa/i.test(gpa) ? "" : " GPA") : "") + ". " + (film ? "Film: " + film + ". " : "") + "Thank you for your time.";
    return { subject: subjectLine(f), body: lines.join("\n"), dm: dm };
  }
  function lint(f, text) {
    var flags = [], t = esc(text) + "\n" + esc(f.metric) + "\n" + esc(f.interest);
    PARENT.forEach(function (rx) { var m = t.match(rx); if (m) flags.push({ level: "red", code: "parent-voice", msg: "Parent-voice phrase \u201c" + m[0] + "\u201d. Coaches want to hear from the athlete. Rewrite in first person as the athlete." }); });
    var low = t.toLowerCase();
    HYPE.forEach(function (w) { if (low.indexOf(w) >= 0) flags.push({ level: "red", code: "hype", msg: "Unverified hype word \u201c" + w + "\u201d. Replace with a verified number a coach can check." }); });
    PROMISE.forEach(function (rx) { var m = t.match(rx); if (m) flags.push({ level: "red", code: "promise", msg: "Promise language \u201c" + m[0] + "\u201d. Remove it." }); });
    if (!esc(f.film).trim()) flags.push({ level: "amber", code: "no-film", msg: "No film link. Coaches open a link, not an attachment." });
    else if (!/^https:\/\//i.test(esc(f.film).trim())) flags.push({ level: "amber", code: "film-https", msg: "Film link should start with https://" });
    if (!esc(f.metric).trim()) flags.push({ level: "amber", code: "no-metric", msg: "No verified metric or mark. Add one a coach can check (time, distance, velocity, stat line)." });
    if (!esc(f.gpa).trim()) flags.push({ level: "amber", code: "no-gpa", msg: "No GPA. Add your unweighted GPA or your academic interest." });
    if (!esc(f.firstName).trim()) flags.push({ level: "amber", code: "no-name", msg: "Add your first name." });
    if (!esc(f.coachLast).trim()) flags.push({ level: "amber", code: "no-coach", msg: "Add the coach's last name. A generic note gets ignored." });
    return flags;
  }
  var TIERS = [
    { tier: "Reach", n: 5, hint: "Programs above your current level. Worth a note; do not count on a reply." },
    { tier: "Match", n: 8, hint: "Your film and numbers fit the roster's typical level." },
    { tier: "Academic-Aid", n: 5, hint: "Schools where grades and test scores can earn academic aid." },
    { tier: "In-State", n: 6, hint: "Closer to home and cheaper to visit; often lower travel and tuition cost." },
    { tier: "JUCO-or-NAIA Safety", n: 6, hint: "NAIA and junior-college programs that fill rosters late and have no NCAA calendar." }
  ];
  function seedRows() {
    var rows = [];
    TIERS.forEach(function (t) { for (var i = 0; i < t.n; i++) rows.push({ tier: t.tier, school: "", division: "", coach: "", questionnaire: "", firstSend: "", status: "" }); });
    return rows;
  }
  function csvCell(v) { v = esc(v); return /[",\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; }
  var COLS = ["tier", "school", "division", "coach", "questionnaire", "firstSend", "status"];
  function toCsv(rows) { return [COLS.join(",")].concat(rows.map(function (r) { return COLS.map(function (c) { return csvCell(r[c]); }).join(","); })).join("\n") + "\n"; }
  var CADENCE = [{ n: 1, d: 0, label: "Touch 1: intro email" }, { n: 2, d: 10, label: "Touch 2: still-recruiting check-in" }, { n: 3, d: 24, label: "Touch 3: post-camp follow-up" }, { n: 4, d: 45, label: "Touch 4: final check-in" }];
  function addDays(isoDate, n) { var p = isoDate.split("-").map(Number); var d = new Date(Date.UTC(p[0], p[1] - 1, p[2] + n)); return d.toISOString().slice(0, 10); }
  function icsEscape(s) { return esc(s).replace(/\\/g, "\\\\").replace(/;/g, "\\;").replace(/,/g, "\\,").replace(/\n/g, "\\n"); }
  function toIcs(rows, stampIso) {
    var out = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//The Commit Book//Access//EN", "CALSCALE:GREGORIAN"];
    var stamp = (stampIso || "2026-01-01").replace(/-/g, "") + "T000000Z", uid = 0;
    rows.forEach(function (r) {
      if (!esc(r.school).trim() || !/^\d{4}-\d{2}-\d{2}$/.test(esc(r.firstSend))) return;
      CADENCE.forEach(function (c) {
        uid++; var day = addDays(r.firstSend, c.d).replace(/-/g, "");
        var nxt = addDays(r.firstSend, c.d + 1).replace(/-/g, "");
        out.push("BEGIN:VEVENT", "UID:access-" + uid + "-" + day + "@thecommitbook", "DTSTAMP:" + stamp, "DTSTART;VALUE=DATE:" + day, "DTEND;VALUE=DATE:" + nxt,
          "SUMMARY:" + icsEscape(c.label + " - " + r.school), "DESCRIPTION:" + icsEscape("Reminder only. You send it yourself from the athlete's own account, parent copied. No reply is promised."), "END:VEVENT");
      });
    });
    out.push("END:VCALENDAR"); return out.join("\r\n") + "\r\n";
  }
  root.AccessCore = { build: build, lint: lint, subjectLine: subjectLine, TIERS: TIERS, seedRows: seedRows, toCsv: toCsv, toIcs: toIcs, CADENCE: CADENCE, COLS: COLS, addDays: addDays, TARGET_CAP: 30 };
})(typeof window !== "undefined" ? window : globalThis);
