/* The Commit Book: personalization UI glue (W11-3). Depends on personalize.js (window.CBPersonalize).
 * Renders only what the engine returns. Never shows "Vetted". Never collects minor identifiers.
 */
(function () {
  "use strict";
  var P = window.CBPersonalize;
  var $ = function (id) { return document.getElementById(id); };
  var state = { rows: [], lastResult: null };

  // Category -> engine row types. CHSAA/governing-body rows do not exist in the seed: shown honestly empty.
  var CATEGORY_TYPES = {
    mental: ["mental_performance"],
    speed: ["strength_conditioning"],
    governing: [],
    camp: ["college_prospect_camp", "showcase", "camp"]
  };
  // Page sport -> engine sport. Multi-sport keeps rows tagged "multi" only.
  var SPORT_MAP = { football: "football", baseball: "baseball", track: "track", multi: "football" };
  var GOAL_FOR_CATEGORY = "college_prospect"; // widest allowed type set; Category filter narrows it

  function today() {
    var d = new Date();
    return Date.UTC(d.getFullYear(), d.getMonth(), d.getDate());
  }
  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text !== undefined) e.textContent = text;
    return e;
  }
  // Display badge: only two honest values. "Observed" is a dated read, not a registry => Listed.
  function badgeFor(it) { return it.highest_label === "verified" ? "Verified" : "Listed"; }
  function fmtDates(it) {
    if (!it.dates || !it.dates.length) return "No date published";
    return it.dates.map(function (d) {
      var s = d.start === (d.end || d.start) ? d.start : d.start + " to " + d.end;
      return d.is_window ? s + " (window, not a confirmed day)" : s;
    }).join("; ");
  }
  function fmtPrice(it) {
    if (!it.price_items || !it.price_items.length) return "Price not published";
    return it.price_items.map(function (p) { return "$" + p.usd + " " + p.label; }).join("; ");
  }

  function readForm() {
    var sport = $("f-sport").value;
    return {
      sport: sport,
      category: $("f-category").value,
      verif: $("f-verif").value,
      zip: $("f-zip").value,
      radius: $("f-radius").value,
      budget: $("f-budget").value,
      showHistorical: $("f-hist").checked
    };
  }

  function run() {
    var f = readForm(), msg = $("form-msg"), out = $("results");
    msg.textContent = ""; out.textContent = "";
    var profile;
    try {
      // EXACTLY the five allowed fields; nothing else is ever passed to the engine.
      profile = P.parseIntake({
        sport: SPORT_MAP[f.sport], class_year: $("f-class").value, area: f.zip,
        budget_band: bandForBudget(f.budget), goal_level: GOAL_FOR_CATEGORY
      }, new Date().getFullYear());
    } catch (e) {
      msg.textContent = e.message; return;
    }
    var res = P.personalize(profile, state.rows, today(), f.showHistorical);
    state.lastResult = res;
    var types = CATEGORY_TYPES[f.category] || null;
    var wanted = f.category === "all" ? null : types;
    var maxMiles = f.radius === "any" ? null : Number(f.radius);
    var budgetCap = f.budget === "" ? null : Number(f.budget);

    function keep(it) {
      if (f.sport === "multi" && !isMulti(it)) return false;
      if (wanted !== null && wanted.indexOf(it.type) < 0) return false;
      if (f.verif !== "all" && badgeFor(it).toLowerCase() !== f.verif) return false;
      if (maxMiles !== null && (it.miles === null || it.miles > maxMiles)) return false;
      if (budgetCap !== null && it.price_items.length &&
          Math.min.apply(null, it.price_items.map(function (p) { return p.usd; })) > budgetCap) return false;
      return true;
    }
    var ranked = res.ranked.filter(keep), tbd = res.not_yet_announced.filter(keep);
    renderSummary(res, ranked.length, tbd.length, f);
    ranked.forEach(function (it) { out.appendChild(card(it, false)); });
    if (tbd.length) {
      out.appendChild(el("h3", "pz-sub", "Not yet announced"));
      tbd.forEach(function (it) { out.appendChild(card(it, false)); });
    }
    var shownIds = {}; ranked.concat(tbd).forEach(function (it) { shownIds[it.entity_id] = 1; });
    if (f.showHistorical) renderHistorical(out, profile, f, shownIds);
    if (!ranked.length && !tbd.length) {
      var why = f.category === "governing"
        ? "No governing-body (CHSAA) calendar rows are in this pilot's dataset. Nothing is invented. Check the official CHSAA calendar directly."
        : (res.empty_reason || "No rows match these filters after the freshness gate. Nothing is invented to fill the list.");
      out.appendChild(el("p", "pz-empty", why));
    }
    state.exportable = ranked.filter(datedAndBookable);
    $("btn-ics").disabled = state.exportable.length === 0;
  }
  function isMulti(it) { return state.rows.some(function (r) { return r.entity_id === it.entity_id && (r.sport || []).indexOf("multi") >= 0; }); }
  function datedAndBookable(it) { return (it.dates || []).length > 0; }
  function bandForBudget(b) {
    if (b === "" || b === null) return "any";
    var n = Number(b);
    return n <= 0 ? "free" : n <= 150 ? "low" : n <= 400 ? "mid" : n <= 1000 ? "high" : "any";
  }

  function renderSummary(res, nRanked, nTbd, f) {
    var s = $("summary"); s.textContent = "";
    s.appendChild(el("p", "pz-disc", res.disclosure));
    var h = res.hidden;
    s.appendChild(el("p", "pz-count",
      nRanked + " shown, " + nTbd + " not yet announced. Hidden by rule: " + h.past + " past, " + h.stale + " not recently checked, " +
      h.sport_mismatch + " other sport, " + h.goal_mismatch + " other type, " + h.grade_mismatch + " other grade, " + h.malformed + " missing provenance."));
    res.standing_notes.forEach(function (n) { s.appendChild(el("p", "pz-note", n)); });
  }

  function renderHistorical(out, profile, f, shownIds) {
    // "Show historical/undated reference rows": past rows and rows with no usable date, labelled, never bookable.
    var t = today(), shown = 0;
    var box = el("div", "pz-hist");
    box.appendChild(el("h3", "pz-sub", "Historical and undated reference rows (not bookable)"));
    state.rows.forEach(function (row) {
      var st = P.rowState(row, t), isUndated = !(row.dates || []).length;
      if (st[0] !== "past" && !isUndated) return;
      if (st[0] === "stale" && !isUndated) return;
      if (shownIds[row.entity_id]) return;
      var types = CATEGORY_TYPES[f.category];
      if (f.category !== "all" && types.indexOf(row.type) < 0) return;
      var c = el("article", "pz-card pz-card--hist");
      c.appendChild(el("span", "pz-flag", st[0] === "past" ? "PAST: reference only" : "UNDATED: reference only"));
      c.appendChild(el("h4", "", row.name));
      c.appendChild(el("p", "pz-meta", (row.dates && row.dates.length ? row.dates[0].start : "No date published") + " | read " + row.read_on));
      var a = el("a", "pz-src", "Source: " + row.url); a.href = row.url; a.rel = "noopener nofollow"; a.target = "_blank";
      c.appendChild(a);
      box.appendChild(c); shown++;
    });
    if (!shown) box.appendChild(el("p", "pz-empty", "No historical or undated rows match this category."));
    out.appendChild(box);
  }

  function card(it) {
    var b = badgeFor(it);
    var c = el("article", "pz-card");
    c.setAttribute("data-entity", it.entity_id);
    var top = el("div", "pz-top");
    var badge = el("span", "pz-badge pz-badge--" + b.toLowerCase(), b);
    badge.title = b === "Verified" ? "A third-party registry entry was read for this row." : "The provider or a directory says so. Not independently verified.";
    top.appendChild(badge);
    top.appendChild(el("span", "pz-type", it.type.replace(/_/g, " ")));
    c.appendChild(top);
    c.appendChild(el("h4", "", it.name));
    var dl = el("dl", "pz-dl");
    function row(k, v) { dl.appendChild(el("dt", "", k)); dl.appendChild(el("dd", "", v)); }
    row("Distance", it.miles === null ? "Unknown (ZIP prefix not in the pilot table)" : it.miles + " mi straight-line from " + (readForm().zip.slice(0,3) === "802" ? "Denver center" : "your ZIP area") + " (" + (it.location || "CO") + ")");
    row("Dates", fmtDates(it));
    row("Price", fmtPrice(it));
    row("Checked on", it.read_on + (b === "Verified" ? " (registry read)" : " (page read, not independently verified)"));
    dl.appendChild(el("dt", "", "Source"));
    var dd = el("dd"); var a = el("a", "pz-src", it.url); a.href = it.url; a.rel = "noopener nofollow"; a.target = "_blank"; dd.appendChild(a); dl.appendChild(dd);
    c.appendChild(dl);
    if (it.credential_checks && it.credential_checks.length) {
      var cc = it.credential_checks[0];
      c.appendChild(el("p", "pz-cred", cc.credential + " per " + cc.issuer + " profile, certified " + cc.certified + ", recertification due " + cc.recert_due + ". " +
        "A credential is not a safety guarantee."));
    }
    if (it.flags.length) c.appendChild(el("p", "pz-flags", it.flags.join(" | ")));
    if (it.safeguarding_questions) {
      var det = el("details", "pz-det"); det.appendChild(el("summary", "", "Ask before paying (" + it.safeguarding_questions.length + " questions)"));
      var ul = el("ul"); it.safeguarding_questions.forEach(function (q) { ul.appendChild(el("li", "", q)); });
      det.appendChild(ul); det.appendChild(el("p", "pz-note", it.safeguarding_status)); c.appendChild(det);
    }
    return c;
  }

  // ---------- checklist ----------
  var CHECKLIST = [
    ["bg", "Background check", "Does every coach and staff member who works with minors get a pre-hire criminal history check through a consumer reporting agency (the Colorado SB24-113 standard)? Ask for the date of the most recent check and the name of the policy that requires it."],
    ["mr", "Mandatory-reporter training", "Has every coach completed mandatory-reporter training this calendar year? Ask to see a completion record or the written policy."],
    ["ss", "SafeSport / abuse prevention", "Do coaches complete SafeSport or an equivalent abuse-prevention course? SB24-113 encourages annual abuse-prevention training; ask whether it is required here."],
    ["pc", "Prohibited-conduct policy", "Is there a written prohibited-conduct policy, and is the parent notice posted or handed to you? Ask for a copy before you pay."],
    ["oo", "One-on-one observation", "What is the one-on-one policy? Can you or another adult watch every session, or is the space open and interruptible? A closed-door 1-on-1 with a minor is a reason to walk away."],
    ["ins", "Insurance", "Does the business carry general liability insurance that covers athletes? Ask for the certificate and the coverage dates."],
    ["aed", "Emergency readiness", "Is a first-aid/CPR/AED-certified adult on site during sessions, and where is the AED? (This is good practice. It is not currently required by Colorado law.)"],
    ["nm", "Named coach and credential", "Which named coach will work with your child? What is their credential number, so you can check it with the issuer yourself?"],
    ["cred", "Verifiable credentials", "Check, do not trust a badge. Mental performance: AASP CMPC via the AASP certified-consultant directory. Strength and conditioning: NSCA CSCS via the NSCA directory or written verification request. A CMPC is not a mental-health clinician; only a state licence is."],
    ["ref", "Refund and cancellation policy", "Get the refund, make-up and cancellation terms in writing before paying. Ask what happens if your child is injured or the camp is cancelled."],
    ["pay", "Payment and contracts", "Is there an auto-renewal or multi-month commitment? Never pay in cash with no receipt. Do not sign anything you have not read."],
    ["out", "No outcome promises", "Walk away from any promise of a scholarship, an offer, or a guaranteed result. No one can sell you a roster spot."]
  ];
  function renderChecklist() {
    var ul = $("checklist"); ul.textContent = "";
    CHECKLIST.forEach(function (c) {
      var li = el("li", "pz-ck");
      var id = "ck-" + c[0];
      var cb = document.createElement("input"); cb.type = "checkbox"; cb.id = id;
      var lab = document.createElement("label"); lab.setAttribute("for", id);
      lab.appendChild(el("b", "", c[1])); lab.appendChild(el("span", "", c[2]));
      li.appendChild(cb); li.appendChild(lab); ul.appendChild(li);
    });
  }
  function checklistText() {
    var out = ["The Commit Book: Parent vetting checklist for private trainers, facilities and camps",
      "Colorado SB24-113 (Safer Youth Sports) and SafeSport. Education, not legal advice. We have not verified any provider's safety.", ""];
    CHECKLIST.forEach(function (c, i) {
      var done = $("ck-" + c[0]).checked;
      out.push((done ? "[x] " : "[ ] ") + (i + 1) + ". " + c[1] + ": " + c[2], "    Provider's answer / date: ______________________", "");
    });
    out.push("Do not leave a minor athlete with a provider until you are satisfied with the answers above.");
    return out.join("\r\n") + "\r\n";
  }
  function download(name, mime, text) {
    var blob = new Blob([text], { type: mime });
    var a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = name;
    document.body.appendChild(a); a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 0);
  }

  function init() {
    renderChecklist();
    var cy = $("f-class"), y = new Date().getFullYear();
    for (var i = 0; i <= 7; i++) { var o = document.createElement("option"); o.value = y + i + (new Date().getMonth() >= 7 ? 1 : 0); o.textContent = "Class of " + o.value; cy.appendChild(o); }
    ["f-sport", "f-category", "f-verif", "f-zip", "f-radius", "f-budget", "f-class", "f-hist"].forEach(function (id) {
      $(id).addEventListener("change", run);
    });
    $("intake").addEventListener("submit", function (e) { e.preventDefault(); run(); });
    $("btn-ics").addEventListener("click", function () {
      if (!state.lastResult || !state.exportable || !state.exportable.length) return;
      var r = JSON.parse(JSON.stringify(state.lastResult));
      r.ranked = state.exportable; // exactly the dated, bookable rows currently shown
      download("commit-book-denver-pilot.ics", "text/calendar;charset=utf-8", P.toIcs(r));
    });
    $("btn-print").addEventListener("click", function () { window.print(); });
    $("btn-ck-dl").addEventListener("click", function () { download("parent-vetting-checklist.txt", "text/plain;charset=utf-8", checklistText()); });
    fetch("/personalize/seed.json", { credentials: "omit", cache: "no-store" }).then(function (r) { return r.json(); }).then(function (j) {
      state.rows = j.rows || []; run();
    }).catch(function () {
      state.rows = []; run();
    });
  }
  window.CBPersonalizeUI = { run: run, badgeFor: badgeFor, CHECKLIST: CHECKLIST, checklistText: checklistText };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
