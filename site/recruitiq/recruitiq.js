/* RecruitIQ Standards & Fit Explorer. All figures come from data.json (W10-verified rows).
   Nothing typed here is stored or sent anywhere. */
(function () {
  'use strict';
  var D = null;
  var $ = function (id) { return document.getElementById(id); };
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function link(c) {
    return '<span class="riq-cite"><a href="' + esc(c.url) + '" rel="noopener" target="_blank">' + esc(c.label) + '</a>' +
      (c.note ? '<br>' + esc(c.note) : '') + '</span>';
  }

  /* ---------- Bucket 1 ---------- */
  function renderB1() {
    var sport = $('b1sport').value, div = $('b1div').value;
    var rows = D.eligibility.filter(function (r) { return r.sport === sport && r.division === div; });
    var out = $('b1out');
    if (!rows.length) { out.innerHTML = '<div class="riq-empty">No verified row for this combination.</div>'; return; }
    out.innerHTML = rows.map(function (r) {
      var roster = r.roster_cap && r.roster_cap.indexOf('n/a') !== 0
        ? '<div class="lab">Roster limit (Bylaw 17.2)</div><div class="big">' + esc(r.roster_cap) + '</div>' : '';
      return '<div class="riq-card"><span class="riq-tag mono">' + esc(r.division) + '</span><h3>' + esc(r.sport) + '</h3>' +
        roster +
        '<div class="lab" style="margin-top:12px">Athletics aid</div><div class="big" style="font-size:clamp(24px,3vw,34px)">' + esc(r.aid_cap) + '</div>' +
        '<div class="lab" style="margin-top:12px">GPA &amp; course rules</div><p>' + esc(r.gpa_rule) + '</p>' +
        (r.caveat ? '<p class="riq-note">' + esc(r.caveat) + '</p>' : '') +
        r.sources.map(link).join('') + '</div>';
    }).join('');
  }
  function renderMoving() {
    $('b1moving').innerHTML = D.rules_moving.map(function (m) {
      return '<div class="riq-card"><h3>' + esc(m.title) + '</h3><p>' + esc(m.text) + '</p>' + link(m.source) + '</div>';
    }).join('');
  }

  /* ---------- Bucket 2 ---------- */
  function parseTime(s) {
    s = String(s || '').trim();
    if (!s) return null;
    var m = /^(\d+):(\d{1,2}(?:\.\d+)?)$/.exec(s);
    if (m) { var sec = parseFloat(m[2]); if (sec >= 60) return null; return parseInt(m[1], 10) * 60 + sec; }
    if (/^\d+(\.\d+)?$/.test(s)) return parseFloat(s);
    return null;
  }
  function fmt(sec) {
    if (sec >= 60) { var m = Math.floor(sec / 60), r = (sec - m * 60).toFixed(2); return m + ':' + (r < 10 ? '0' : '') + r; }
    return sec.toFixed(2);
  }
  function placement(prog, ev, t) {
    // marks are ordered fastest tier first; lower seconds are better
    var marks = prog.marks[ev];
    var met = marks.filter(function (m) { return t <= m.seconds + 1e-9; });
    var best = met.length ? met[0] : null;
    var nextMark = null;
    for (var i = marks.length - 1; i >= 0; i--) { if (t > marks[i].seconds + 1e-9) { nextMark = marks[i]; } }
    return { marks: marks, met: met, best: best, miss: marks.filter(function (m) { return t > m.seconds + 1e-9; }) };
  }
  function renderB2() {
    var ev = $('b2event').value, raw = $('b2time').value, t = parseTime(raw), out = $('b2out');
    if (t === null) { out.innerHTML = '<div class="riq-empty">Enter a valid time (for example 10.62 or 1:54.20) to compare.</div>'; return; }
    var lo = { '100': 8, '400': 35, '800': 90, '1500': 190 }[ev];
    if (t < lo) { out.innerHTML = '<div class="riq-empty">That time is faster than any plausible high school mark for this event. Check the format.</div>'; return; }
    var evLabel = D.events.filter(function (e) { return e.id === ev; })[0].label;
    out.innerHTML = D.programs.map(function (p) {
      var pl = placement(p, ev, t);
      var rows = pl.marks.map(function (m) {
        var ok = t <= m.seconds + 1e-9;
        var diff = ok ? 'meets by ' + (m.seconds - t).toFixed(2) + ' s' : 'needs ' + (t - m.seconds).toFixed(2) + ' s faster';
        return '<tr><td>' + esc(m.tier) + '</td><td class="num">' + esc(m.display) + '</td><td>' +
          '<span class="riq-tag ' + (ok ? 'hit' : '') + '">' + (ok ? 'At or faster' : 'Slower') + '</span> ' + diff + '</td></tr>';
      }).join('');
      var verdict = pl.best
        ? 'Your ' + esc(fmt(t)) + ' is at or faster than this school\'s published "' + esc(pl.best.tier) + '" mark (' + esc(pl.best.display) + ').'
        : 'Your ' + esc(fmt(t)) + ' is slower than every mark this school publishes for the ' + esc(evLabel) + '.';
      var dd = p.disclaimer;
      var disc = (dd.by === 'school'
        ? '<strong>School disclaimer:</strong> "' + esc(dd.text) + '"'
        : '<strong>Standing reminder:</strong> ' + esc(dd.text)) + (dd.extra ? ' ' + esc(dd.extra) : '');
      return '<div class="riq-result"><h3>' + esc(p.name) + ' <span class="riq-tag mono">' + esc(p.level) + ' · ' + esc(p.conference) + '</span></h3>' +
        '<div class="meta">Source dated ' + esc(p.vintage) + ' · cycle ' + esc(p.cycle) + ' · ' + esc(evLabel) + ' · FAT</div>' +
        '<p class="verdict">' + verdict + '</p>' +
        '<div class="riq-tw"><table><thead><tr><th>Published tier</th><th>Mark</th><th>Your time</th></tr></thead><tbody>' + rows + '</tbody></table></div>' +
        '<p class="disc">' + disc + '</p>' +
        '<span class="riq-cite"><a href="' + esc(p.url) + '" rel="noopener" target="_blank">School PDF/page, dated ' + esc(p.vintage) + '</a></span></div>';
    }).join('');
  }
  function renderB2Static() {
    var u = D.uno;
    $('b2unopolicy').innerHTML = '<h3>' + esc(u.name) + ' <span class="riq-tag mono">' + esc(u.level) + '</span> policy note</h3>' +
      '<p>' + esc(u.policy_note) + '</p>' +
      '<span class="riq-cite"><a href="' + esc(u.url) + '" rel="noopener" target="_blank">New Orleans PDF, dated ' + esc(u.vintage) + '</a></span>';
    $('b2vint').querySelector('tbody').innerHTML = D.programs.concat([u]).map(function (p) {
      return '<tr><td>' + esc(p.name) + '</td><td class="num">' + esc(p.vintage) + '</td><td>' + esc(p.cycle) + '</td><td class="riq-cite"><a href="' + esc(p.url) + '" rel="noopener" target="_blank">source</a></td></tr>';
    }).join('');
    $('b2excl').innerHTML = '<strong>Not in the live comparator:</strong> ' + D.excluded_from_calculator.map(function (x) {
      return esc(x.name) + ' (' + esc(x.reason) + ')';
    }).join('; ') + '.';
  }

  /* ---------- Bucket 3 ---------- */
  function renderB3() {
    var b = D.bucket3;
    $('b3why').textContent = b.why_unpublished;
    $('b3list').innerHTML = b.evaluated.map(function (x) { return '<li>' + esc(x) + '</li>'; }).join('');
    $('b3agg').textContent = b.aggregator_note;
    $('b3act').textContent = b.action;
  }

  /* ---------- Bucket 4 ---------- */
  function renderB4() {
    var s = $('b4sport').value, lvl = $('b4lvl').value;
    var rows = document.querySelectorAll('#b4tab tbody tr');
    for (var i = 0; i < rows.length; i++) {
      rows[i].hidden = !(s === 'all' || rows[i].getAttribute('data-sport') === s);
    }
    var names = { overall: 'NCAA overall', d1: 'D1', d2: 'D2', d3: 'D3' };
    var list = D.ratios.filter(function (r) { return s === 'all' || r.sport === s; });
    var max = Math.max.apply(null, D.ratios.map(function (r) { return r[lvl]; }));
    $('b4bars').innerHTML = list.map(function (r) {
      return '<div><strong>' + esc(r.sport) + '</strong> · ' + esc(names[lvl]) + ': <span class="riq-tag mono">' + r[lvl].toFixed(1) + '% of high school participants appear on an NCAA roster in the same year</span>' +
        '<div class="riq-bar" role="img" aria-label="' + r[lvl].toFixed(1) + ' percent"><i style="width:' + (r[lvl] / max * 100).toFixed(1) + '%"></i></div></div>';
    }).join('');
  }
  function renderB4Static() {
    $('b4method').innerHTML = D.ratio_method.map(function (m) { return '<li>' + esc(m) + '</li>'; }).join('');
    $('b4src').innerHTML = '<a href="' + esc(D.ratio_source.url) + '" rel="noopener" target="_blank">' + esc(D.ratio_source.label) + '</a>';
    $('b4prev').innerHTML = 'Versus the ' + esc(D.previous_edition_label) + ': ' + D.previous_edition.map(function (p) {
      return esc(p.sport) + ' ' + p.previous_pct.toFixed(1) + '% to ' + p.current_pct.toFixed(1) + '%';
    }).join(', ') + '. The House settlement raised some roster caps (football 85 to 105), so numerator and denominator are both moving.';
    $('b4fact').innerHTML = esc(D.fact_sheet.text) + ' <span class="riq-tag warn">' + esc(D.fact_sheet.label) + '</span> <a href="' + esc(D.fact_sheet.url) + '" rel="noopener" target="_blank">NCAA recruiting fact sheet</a>';
  }

  function init() {
    renderB1(); renderMoving(); renderB2Static(); renderB3(); renderB4Static(); renderB4();
    ['b1sport', 'b1div'].forEach(function (id) { $(id).addEventListener('change', renderB1); });
    ['b4sport', 'b4lvl'].forEach(function (id) { $(id).addEventListener('change', renderB4); });
    $('b2event').addEventListener('change', renderB2);
    $('b2form').addEventListener('submit', function (e) { e.preventDefault(); renderB2(); });
    $('b2time').addEventListener('input', renderB2);
  }

  fetch('/recruitiq/data.json').then(function (r) { return r.json(); }).then(function (d) { D = d; init(); })
    .catch(function () {
      var r = new XMLHttpRequest();
      r.open('GET', 'data.json'); r.onload = function () { D = JSON.parse(r.responseText); init(); }; r.send();
    });
})();
