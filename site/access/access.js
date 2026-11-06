/* Access page wiring. Everything runs in this tab. Nothing is sent to a server, saved in
   browser storage or cookies, or logged. Reload the page and the athlete's details are gone. */
(function () {
  var R = window.AccessRules, C = window.AccessCore;
  function $(s, r) { return (r || document).querySelector(s); }
  function el(tag, attrs, html) { var e = document.createElement(tag); for (var k in (attrs || {})) e.setAttribute(k, attrs[k]); if (html != null) e.innerHTML = html; return e; }
  function h(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function fmt(iso) { if (!iso) return ""; var p = iso.split("-").map(Number); return new Date(Date.UTC(p[0], p[1] - 1, p[2])).toLocaleDateString("en-US", { timeZone: "UTC", year: "numeric", month: "long", day: "numeric" }); }
  function download(name, text, type) {
    var a = el("a", { href: URL.createObjectURL(new Blob([text], { type: type })), download: name });
    document.body.appendChild(a); a.click(); a.remove();
  }
  /* nav */
  var mb = $(".menu-btn"), nav = $("#site-nav");
  if (mb && nav) mb.addEventListener("click", function () { var o = mb.getAttribute("aria-expanded") === "true"; mb.setAttribute("aria-expanded", String(!o)); nav.classList.toggle("open", !o); });

  /* ---------- A. calculator ---------- */
  var ROWS = [["athlete", "Athlete-initiated email or questionnaire"], ["coach", "Coach calls, texts and direct messages"], ["unofficial", "Unofficial visits"], ["official", "Official visits"], ["offcampus", "Off-campus contact"]];
  function fill(sel, vals, lab) { vals.forEach(function (v) { sel.appendChild(el("option", { value: v }, h(lab ? lab(v) : v))); }); }
  var sSport = $("#a-sport"), sDiv = $("#a-div"), sCls = $("#a-cls");
  if (sSport) {
    Object.keys(R.SPORTS).forEach(function (k) { sSport.appendChild(el("option", { value: k }, h(R.SPORTS[k].label))); });
    fill(sDiv, R.DIVISIONS); fill(sCls, R.CLASSES, function (c) { return "Class of " + c; }); sCls.value = "2029";
    var renderA = function () {
      var r = R.lookup(sSport.value, sDiv.value, sCls.value), out = $("#a-out");
      var html = '<p class="ac-banner">' + h(r.banner) + '</p><div class="ac-rows">';
      ROWS.forEach(function (row) {
        var x = r.rows[row[0]], when;
        if (x.date) when = fmt(x.date); else if (x.anytime) when = "Any time"; else when = "Not verified: ask the program";
        html += '<div class="ac-row"><div><p class="lab">' + h(row[1]) + '</p><p class="ac-date">' + h(when) + '</p></div><div><p class="ac-note">' + h(x.note) + '</p><p class="mono ac-cite">' + h(x.rule) + ' &middot; <span class="ac-scope">' + h(x.scope) + '</span></p></div></div>';
      });
      html += '</div><p class="note">Dates copied from the ' + h(r.manual) + ', checked ' + h(r.verified_on) + '. Class years other than 2029 shift by whole years from the verified 2029 record; check the NCAA sport calendar for the exact day and for dead or quiet periods. A date is when a rule opens, not a promise that a coach will reply. Education, not legal advice.</p>';
      out.innerHTML = html;
    };
    [sSport, sDiv, sCls].forEach(function (s) { s.addEventListener("change", renderA); }); renderA();
  }

  /* ---------- B. builder + linter ---------- */
  var form = $("#b-form");
  if (form) {
    var ids = ["firstName", "gradYear", "sport", "position", "metric", "gpa", "interest", "film", "school", "coachLast"];
    var vals = function () { var f = {}; ids.forEach(function (i) { f[i] = $("#b-" + i).value; }); return f; };
    var renderB = function () {
      var f = vals(), b = C.build(f), flags = C.lint(f, b.body + "\n" + b.dm + "\n" + f.interest);
      $("#b-subject").value = b.subject; $("#b-body").value = b.body; $("#b-dm").value = b.dm;
      var box = $("#b-lint");
      box.innerHTML = flags.length ? flags.map(function (x) { return '<li class="ac-flag ' + x.level + '"><b>' + (x.level === "red" ? "Fix" : "Check") + '</b> ' + h(x.msg) + '</li>'; }).join("") : '<li class="ac-flag ok"><b>Clear</b> No red flags found. You still send it yourself, from your own account.</li>';
      $("#b-dmcount").textContent = b.dm.length + " characters";
    };
    form.addEventListener("input", renderB); form.addEventListener("submit", function (e) { e.preventDefault(); });
    document.querySelectorAll("[data-copy]").forEach(function (btn) {
      btn.addEventListener("click", function () { var t = $("#" + btn.getAttribute("data-copy")); t.select(); try { navigator.clipboard.writeText(t.value); } catch (e) { document.execCommand("copy"); } btn.textContent = "Copied"; setTimeout(function () { btn.textContent = btn.getAttribute("data-label"); }, 1400); });
    });
    var clr = $("#b-clear"); if (clr) clr.addEventListener("click", function () { form.reset(); renderB(); });
    renderB();
  }

  /* ---------- C. target list ---------- */
  var tbody = $("#c-body");
  if (tbody) {
    var rows = C.seedRows(), DIVS = ["", "NCAA D1", "NCAA D2", "NCAA D3", "NAIA", "NJCAA"], STAT = ["", "To contact", "Questionnaire done", "Email sent", "Reply received", "Not recruiting", "Dropped"];
    var opt = function (arr, cur) { return arr.map(function (v) { return '<option' + (v === cur ? " selected" : "") + ">" + h(v) + "</option>"; }).join(""); };
    var draw = function () {
      tbody.innerHTML = rows.map(function (r, i) {
        return '<tr><td data-th="Tier"><span class="ac-tier">' + h(r.tier) + '</span></td>' +
          '<td data-th="School"><input data-i="' + i + '" data-k="school" value="' + h(r.school) + '" aria-label="School, row ' + (i + 1) + '"></td>' +
          '<td data-th="Division"><select data-i="' + i + '" data-k="division" aria-label="Division, row ' + (i + 1) + '">' + opt(DIVS, r.division) + '</select></td>' +
          '<td data-th="Coach last name"><input data-i="' + i + '" data-k="coach" value="' + h(r.coach) + '" aria-label="Coach, row ' + (i + 1) + '"></td>' +
          '<td data-th="Questionnaire link"><input data-i="' + i + '" data-k="questionnaire" value="' + h(r.questionnaire) + '" placeholder="https://" aria-label="Questionnaire, row ' + (i + 1) + '"></td>' +
          '<td data-th="First send date"><input type="date" data-i="' + i + '" data-k="firstSend" value="' + h(r.firstSend) + '" aria-label="First send date, row ' + (i + 1) + '"></td>' +
          '<td data-th="Status"><select data-i="' + i + '" data-k="status" aria-label="Status, row ' + (i + 1) + '">' + opt(STAT, r.status) + '</select></td></tr>';
      }).join("");
      var filled = rows.filter(function (r) { return r.school.trim(); }).length;
      $("#c-count").textContent = filled + " of " + C.TARGET_CAP + " schools entered";
    };
    tbody.addEventListener("input", function (e) { var t = e.target; if (t.dataset.i != null) { rows[+t.dataset.i][t.dataset.k] = t.value; var f = rows.filter(function (r) { return r.school.trim(); }).length; $("#c-count").textContent = f + " of " + C.TARGET_CAP + " schools entered"; } });
    $("#c-csv").addEventListener("click", function () { download("my-target-list.csv", C.toCsv(rows), "text/csv"); });
    $("#c-ics").addEventListener("click", function () {
      var ready = rows.filter(function (r) { return r.school.trim() && r.firstSend; }).length;
      if (!ready) { $("#c-msg").textContent = "Enter a school and a first send date on at least one row, then try again."; return; }
      $("#c-msg").textContent = "Calendar file created for " + ready + " schools (4 reminders each). Reminders only: you send every message yourself.";
      download("follow-up-reminders.ics", C.toIcs(rows, new Date().toISOString().slice(0, 10)), "text/calendar");
    });
    $("#c-reset").addEventListener("click", function () { rows = C.seedRows(); draw(); $("#c-msg").textContent = ""; });
    draw();
  }

  /* ---------- D. decision guide: checklist state in memory only ---------- */
  document.querySelectorAll(".ac-check input").forEach(function (cb) {
    cb.addEventListener("change", function () { var done = document.querySelectorAll(".ac-check input:checked").length, all = document.querySelectorAll(".ac-check input").length; $("#d-progress").textContent = done + " of " + all + " steps checked"; });
  });
})();
