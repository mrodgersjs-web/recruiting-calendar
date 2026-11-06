/* Emerging & Fastest-Growing Sports hub. Renders sport tabs and the pathway checklist from data.json. */
(function () {
  "use strict";
  var KEY = "emerging-checklist-v1";

  var CHECKLIST = [
    {id: "level", q: "Which governing body sponsors the team: NCAA, NAIA, NJCAA, or none?",
     hint: "Ask the coach in writing. Then open the body's own sport page (ncaa.org, naia.org, njcaa.org) and find the school there."},
    {id: "status", q: "Is it a championship sport, an Emerging Sport, an invitational, or club?",
     hint: "NCAA Emerging Sport = recognized but no national championship yet. Club (ACHA, NCVF, a school club) = not varsity, no athletic aid rules apply."},
    {id: "varsity", q: "Is the program varsity at THIS school, funded by the athletic department?",
     hint: "Ask: Is the team on the athletics department budget? Is it listed on the school's athletics site roster page, not only a club page?"},
    {id: "season", q: "Has the school played a full season, or is it announced / starting next year?",
     hint: "AVCA and NCAA lists include announced programs. A program that has not played yet can be cut before it starts."},
    {id: "aid", q: "Does this level give athletic aid for the sport, and how many equivalencies?",
     hint: "NAIA: per-sport equivalency limit, splittable. D1 depends on opt-in. D2: equivalency counts. D3: none. NJCAA D3: none."},
    {id: "inst", q: "How much of the offer is athletic aid versus institutional (academic or need) aid?",
     hint: "Get both numbers in the written offer. Institutional aid can be the larger piece, especially at D3 and in new programs."},
    {id: "roster", q: "How many athletes are on the roster and how many are in the incoming class?",
     hint: "A new program may recruit its whole first roster. Ask how many openings are in your graduation year."},
    {id: "elig", q: "Have we registered with the right eligibility center (NCAA, NAIA, or NJCAA rules)?",
     hint: "NAIA uses its own center (PlayNAIA.org). NJCAA needs proof of graduation. Do this before any official visit."},
    {id: "deposit", q: "Before paying any deposit: is the sport status confirmed in writing, and is the deposit refundable?",
     hint: "Never pay a deposit on a team whose status you only heard verbally. Get the refund terms and the athletics contact in an email."},
    {id: "cut", q: "What happens to my aid if the program is cut or changes level?",
     hint: "Ask what the school's written policy is on guaranteed aid and transfer release if the sport is dropped."}
  ];

  function el(tag, attrs, html) {
    var n = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) { n.setAttribute(k, attrs[k]); });
    if (html != null) n.innerHTML = html;
    return n;
  }
  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return {"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}[c];
    });
  }

  function pathCard(label, p) {
    var warn = /not confirmed|emerging/i.test(p.status) ? " warn" : "";
    return '<div class="card"><h4>' + esc(label) + '</h4><span class="pill' + warn + '">' + esc(p.status) +
      '</span><p>' + esc(p.detail) + '</p><p class="src"><a href="' + esc(p.url) + '" rel="noopener">Source</a></p></div>';
  }

  function renderSports(data) {
    var tabs = document.getElementById("sport-tabs");
    var panels = document.getElementById("sport-panels");
    if (!tabs || !panels) return;
    tabs.innerHTML = ""; panels.innerHTML = "";
    data.sports.forEach(function (s, i) {
      var b = el("button", {"class": "tab", role: "tab", id: "tab-" + s.id, "aria-controls": "panel-" + s.id,
        "aria-selected": i === 0 ? "true" : "false", type: "button"}, esc(s.name));
      tabs.appendChild(b);
      var story = s.story ? '<p><a class="btn outline" href="' + esc(s.story) + '">Read the Commit Book story</a></p>' : "";
      var extra = s.doubled ? '<p class="fine">Since 2021-22: ' + esc(s.doubled) + '.</p>' : "";
      if (s.history) extra += '<p class="fine">Long run: ' + esc(s.history) + '.</p>';
      var html = '<div class="sport-nums"><div><span class="num">' + esc(s.participants_display) + '</span><small>NFHS 2024-25 participants</small></div>' +
        '<div><span class="num">' + esc(s.growth_display) + '</span><small>' + esc(s.growth_note) + '</small></div>' +
        '<div><span class="num">' + esc(s.schools_display) + '</span><small>schools</small></div></div>' +
        '<p class="src">Source: <a href="' + esc(s.nfhs_url) + '" rel="noopener">' + esc(s.nfhs_source) + '</a></p>' +
        '<p class="fine">' + esc(s.schools_note) + '</p>' + extra +
        '<div class="cards">' + pathCard("NCAA", s.pathway.ncaa) + pathCard("NAIA", s.pathway.naia) + pathCard("NJCAA", s.pathway.njcaa) + '</div>' + story;
      var p = el("div", {"class": "panel", role: "tabpanel", id: "panel-" + s.id, "aria-labelledby": "tab-" + s.id}, html);
      if (i !== 0) p.hidden = true;
      panels.appendChild(p);
    });
    var btns = tabs.querySelectorAll("button");
    function select(idx) {
      btns.forEach(function (x, j) {
        x.setAttribute("aria-selected", j === idx ? "true" : "false");
        x.tabIndex = j === idx ? 0 : -1;
        panels.children[j].hidden = j !== idx;
      });
      btns[idx].focus();
    }
    btns.forEach(function (x, j) {
      x.tabIndex = j === 0 ? 0 : -1;
      x.addEventListener("click", function () { select(j); });
      x.addEventListener("keydown", function (e) {
        if (e.key === "ArrowRight") { e.preventDefault(); select((j + 1) % btns.length); }
        if (e.key === "ArrowLeft") { e.preventDefault(); select((j - 1 + btns.length) % btns.length); }
      });
    });
    var h = (location.hash || "").replace("#", "");
    data.sports.forEach(function (s, j) { if (h === s.id) select(j); });
  }

  function load() { try { return JSON.parse(localStorage.getItem(KEY) || "{}"); } catch (e) { return {}; } }
  function save(o) { try { localStorage.setItem(KEY, JSON.stringify(o)); } catch (e) { /* private mode */ } }

  function renderChecklist() {
    var ul = document.getElementById("checklist");
    if (!ul) return;
    var state = load();
    ul.innerHTML = "";
    CHECKLIST.forEach(function (c) {
      var li = el("li");
      var lab = el("label");
      var cb = el("input", {type: "checkbox", id: "ck-" + c.id});
      cb.checked = !!state[c.id];
      var span = el("span", null, esc(c.q) + '<span class="hint">' + esc(c.hint) + '</span>');
      lab.appendChild(cb); lab.appendChild(span); li.appendChild(lab); ul.appendChild(li);
      cb.addEventListener("change", function () { state[c.id] = cb.checked; save(state); update(); });
    });
    function update() {
      var n = CHECKLIST.filter(function (c) { return state[c.id]; }).length;
      var bar = document.getElementById("progress-bar");
      var txt = document.getElementById("progress-text");
      if (bar) bar.style.width = Math.round(100 * n / CHECKLIST.length) + "%";
      if (txt) txt.textContent = n + " of " + CHECKLIST.length + " answered" + (n === CHECKLIST.length ? ". Ready to ask for the written offer." : ".");
    }
    update();
    var reset = document.getElementById("reset-checklist");
    if (reset) reset.addEventListener("click", function () {
      state = {}; save(state);
      ul.querySelectorAll("input").forEach(function (i) { i.checked = false; });
      update();
    });
  }

  function renderAid(data) {
    var tb = document.getElementById("aid-rows");
    if (!tb) return;
    tb.innerHTML = data.aid_rules.map(function (r) {
      return "<tr><td><strong>" + esc(r.level) + "</strong></td><td>" + esc(r.text) +
        ' <a href="' + esc(r.url) + '" rel="noopener">Source</a></td></tr>';
    }).join("");
  }

  renderChecklist();
  fetch("/emerging-sports/data.json").then(function (r) { return r.json(); }).catch(function () {
    return fetch("data.json").then(function (r) { return r.json(); });
  }).then(function (data) { renderSports(data); renderAid(data); }).catch(function () {
    var n = document.getElementById("sport-fallback");
    if (n) n.hidden = false;
  });
})();
