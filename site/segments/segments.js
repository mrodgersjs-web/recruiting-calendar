/* Segments page. Renders from /segments/segments.json (built from v3/W7 + W6 markdown). No network calls beyond that file; nothing is stored. */
(function () {
  'use strict';
  var D = null;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var esc = function (t) { return String(t).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };
  var money = function (n) { return '$' + Math.round(n).toLocaleString('en-US'); };
  var state = { seg: null, chain: 1, layer: 1, seen: {} };

  /* ---------- tabs ---------- */
  function showView(v, focus) {
    ['a', 'b', 'c'].forEach(function (k) {
      var on = k === v, t = $('#tab-' + k), p = $('#view-' + k);
      t.setAttribute('aria-selected', on); t.tabIndex = on ? 0 : -1; p.hidden = !on;
    });
    if (focus) $('#tab-' + v).focus();
    if (history.replaceState) history.replaceState(null, '', '#view-' + v);
  }
  function initTabs() {
    var tabs = document.querySelectorAll('.sg-tabs [role=tab]');
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { showView(t.dataset.view); });
      t.addEventListener('keydown', function (e) {
        var j = e.key === 'ArrowRight' ? (i + 1) % 3 : e.key === 'ArrowLeft' ? (i + 2) % 3 : -1;
        if (j >= 0) { e.preventDefault(); showView(tabs[j].dataset.view, true); }
      });
    });
    var h = (location.hash || '').replace('#view-', '');
    showView(['a', 'b', 'c'].indexOf(h) >= 0 ? h : 'a');
  }

  /* ---------- A: diagnostic ---------- */
  function renderSegGrid() {
    $('#seg-grid').innerHTML = D.segments.map(function (s) {
      return '<button type="button" role="radio" aria-checked="false" class="sg-seg" data-id="' + s.id + '"><span class="n">' + String(s.id).padStart(2, '0') + '</span><b>' + esc(s.name) + '</b><span class="t">' + esc(s.tag) + '</span></button>';
    }).join('');
    document.querySelectorAll('.sg-seg').forEach(function (b) {
      b.addEventListener('click', function () { pickSeg(+b.dataset.id, true); });
      b.addEventListener('keydown', function (e) {
        var all = Array.prototype.slice.call(document.querySelectorAll('.sg-seg')), i = all.indexOf(b), j = -1;
        if (e.key === 'ArrowRight' || e.key === 'ArrowDown') j = (i + 1) % all.length;
        if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') j = (i + all.length - 1) % all.length;
        if (j >= 0) { e.preventDefault(); all[j].focus(); }
      });
    });
  }
  function pickSeg(id, scroll) {
    var s = D.segments.filter(function (x) { return x.id === id; })[0]; if (!s) return;
    state.seg = id;
    document.querySelectorAll('.sg-seg').forEach(function (b) { b.setAttribute('aria-checked', +b.dataset.id === id); });
    var steps = s.plan.map(function (p) {
      var internal = p.href.charAt(0) === '#';
      return '<li><div><b>' + esc(p.step) + '</b><p>' + esc(p.why) + '</p></div><a class="sg-go" data-view-link="' + (internal ? p.href.slice(-1) : '') + '" href="' + esc(p.href) + '">' + esc(p.tool) + ' &rarr;</a></li>';
    }).join('');
    var chips = s.chains.map(function (c) {
      var ch = D.chains.filter(function (x) { return x.id === c; })[0];
      return '<button type="button" class="sg-chip" data-chain="' + c + '">Problem ' + c + ': ' + esc(ch.title) + '</button>';
    }).join('');
    $('#seg-plan').innerHTML =
      '<p class="lab">Your plan &middot; segment ' + s.id + ' of ' + D.segments.length + '</p><h3>' + esc(s.name) + '</h3><p>' + esc(s.who) + '</p>' +
      '<ol>' + steps + '</ol>' +
      '<p class="lab">A family like yours</p><p class="story"><a href="' + esc(s.story.href) + '">' + esc(s.story.label) + '</a></p>' +
      '<p class="lab">The problems behind this plan</p><div class="sg-chips">' + chips + '</div>' +
      '<p class="note">' + esc(s.spend_note) + '</p>';
    document.querySelectorAll('[data-view-link]').forEach(function (a) {
      if (!a.dataset.viewLink) return;
      a.addEventListener('click', function (e) { e.preventDefault(); showView(a.dataset.viewLink); window.scrollTo({ top: 0 }); });
    });
    document.querySelectorAll('.sg-chip').forEach(function (c) {
      c.addEventListener('click', function () { openChain(+c.dataset.chain, 1); showView('b'); window.scrollTo({ top: 0 }); });
    });
    if (history.replaceState) history.replaceState(null, '', '?segment=' + s.key + '#view-a');
    if (scroll) { var p = $('#seg-plan'); p.focus({ preventScroll: true }); p.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion:reduce)').matches ? 'auto' : 'smooth', block: 'start' }); }
  }

  /* ---------- B: ten-layer drilldown ---------- */
  function badge(status) {
    var ev = status === 'EVIDENCED';
    return '<span class="sg-badge ' + (ev ? 'ev' : 'inf') + '">[' + esc(D.badges[status]) + ']</span>';
  }
  function renderHonesty() {
    var h = D.honesty;
    $('#honesty').innerHTML =
      '<div><strong>' + h.evidenced + '</strong>layers evidenced</div><div><strong>' + h.inferred + '</strong>layers inferred</div><div><strong>' + (h.evidenced + h.inferred) + '</strong>layers in all (6 &times; 10)</div>' +
      '<div class="note">' + esc(h.note) + ' Counts of mentions are directional, not statistics.</div>';
  }
  function renderChainPick() {
    $('#chain-pick').innerHTML = D.chains.map(function (c) {
      return '<button type="button" role="tab" aria-selected="false" data-chain="' + c.id + '">' + c.id + '. ' + esc(c.title) + '</button>';
    }).join('');
    document.querySelectorAll('#chain-pick button').forEach(function (b) {
      b.addEventListener('click', function () { openChain(+b.dataset.chain, 1); });
    });
  }
  function openChain(id, layer) { state.chain = id; state.layer = layer; renderChain(); }
  function renderChain() {
    var c = D.chains.filter(function (x) { return x.id === state.chain; })[0];
    var L = c.layers.filter(function (l) { return l.n === state.layer; })[0];
    state.seen[c.id + ':' + L.n] = true;
    document.querySelectorAll('#chain-pick button').forEach(function (b) { b.setAttribute('aria-selected', +b.dataset.chain === c.id); });
    var ev = c.layers.filter(function (l) { return l.status === 'EVIDENCED'; }).length;
    var rail = c.layers.map(function (l) {
      return '<button type="button" data-layer="' + l.n + '" class="' + (l.status === 'INFERRED' ? 'inf ' : '') + (state.seen[c.id + ':' + l.n] ? 'seen' : '') + '" ' + (l.n === state.layer ? 'aria-current="true"' : '') + ' aria-label="Layer ' + l.n + ', ' + l.status.toLowerCase() + '">' + l.n + '</button>';
    }).join('');
    var solve = '';
    if (L.n === 10) {
      var segs = D.segments.filter(function (s) { return s.chains.indexOf(c.id) >= 0; });
      solve = '<div class="sg-solve"><p class="lab">Where this chain ends: the free tools</p>' + segs.map(function (s) {
        return '<p><b>' + esc(s.name) + ':</b> <a href="' + esc(s.plan[0].href) + '">' + esc(s.plan[0].tool) + '</a></p>';
      }).join('') + '</div>';
    }
    var src = L.source && L.source !== '-' ? esc(L.source) : 'No source: our working hypothesis';
    $('#chain-view').innerHTML =
      '<h3>' + c.id + '. ' + esc(c.title) + '</h3><p class="note">Hits hardest: ' + esc(c.hardest.join(', ')) + ' &middot; ' + ev + ' evidenced, ' + (c.layers.length - ev) + ' inferred in this chain</p>' +
      '<div class="sg-ladder"><div class="sg-rail" role="group" aria-label="Layers 1 to 10">' + rail + '</div>' +
      '<div class="sg-card"><span class="lno">LAYER ' + L.n + ' OF 10</span><h4>' + esc(L.name) + '</h4><p class="txt">' + esc(L.text) + '</p>' + badge(L.status) +
      '<p class="sg-src">Source: ' + src + '</p>' + solve +
      '<div class="sg-nav"><button type="button" class="p" id="l-prev" ' + (L.n === 1 ? 'disabled' : '') + '>&larr; Layer ' + (L.n - 1) + '</button><button type="button" class="p" id="l-next" ' + (L.n === 10 ? 'disabled' : '') + '>Layer ' + (L.n + 1) + ' &rarr;</button>' +
      (L.n === 10 && c.id < 6 ? '<button type="button" id="l-nextchain">Next problem &rarr;</button>' : '') + '</div></div></div>';
    document.querySelectorAll('.sg-rail button').forEach(function (b) { b.addEventListener('click', function () { openChain(c.id, +b.dataset.layer); }); });
    var pv = $('#l-prev'), nx = $('#l-next'), nc = $('#l-nextchain');
    if (pv) pv.addEventListener('click', function () { openChain(c.id, L.n - 1); });
    if (nx) nx.addEventListener('click', function () { openChain(c.id, L.n + 1); });
    if (nc) nc.addEventListener('click', function () { openChain(c.id + 1, 1); });
  }

  /* ---------- C: spending + reallocator ---------- */
  function renderBench() {
    var S = D.spending, max = Math.max.apply(null, S.by_income.map(function (x) { return x.amt; }).concat(S.by_sport_2024.map(function (x) { return x.amt; })));
    var bars = function (arr, hi) {
      return arr.map(function (x) { return '<div class="sg-bar' + (x.label === hi ? ' hi' : '') + '"><span>' + esc(x.label) + '</span><i style="width:' + Math.round(x.amt / max * 100) + '%"></i><b>' + money(x.amt) + '</b></div>'; }).join('');
    };
    $('#bench').innerHTML =
      '<div><p class="lab">Average spend on the primary sport, by household income (per year)</p><div class="sg-bars">' + bars(S.by_income, '$100K+') + '</div>' +
      '<p class="note">$100K+ households: ' + money(1591) + ' a year. Under $50K: ' + money(604) + '. Average across all: ' + money(S.avg_primary_sport) + ' on the primary sport plus ' + money(S.avg_other_sports) + ' on other sports. Travel and lodging is the biggest line (' + money(S.travel_lodging_avg) + ' average, ' + money(S.travel_lodging_100k) + ' for $100K+).</p></div>' +
      '<div><p class="lab">Average spend by primary sport, 2024 (only six reported)</p><div class="sg-bars">' + bars(S.by_sport_2024, 'Baseball') + '</div>' +
      '<p class="note">Baseball: ' + money(1113) + ' a year on the primary sport. Source: <a href="' + esc(S.url) + '" rel="noopener">' + esc(S.source) + '</a>. These are youth sports averages, not recruiting costs.</p></div>';
  }
  function renderCalc() {
    var S = D.spending;
    $('#calc').innerHTML =
      '<h3>Budget reallocator</h3><p class="note">Illustration only. Enter what you would spend on generic, many-school showcases and see what the same money covers. Nothing is saved or sent.</p>' +
      '<div class="row"><label for="in-show">Generic showcase / many-school camp spend this year</label><div><output id="o-show"></output><input type="range" id="in-show" min="0" max="4200" step="50" value="1500" aria-describedby="o-show"></div></div>' +
      '<div class="row"><label for="in-camps">Single-school camps you would attend <em>after</em> that coach has replied</label><div><output id="o-camps"></output><input type="range" id="in-camps" min="0" max="3" step="1" value="1"></div></div>' +
      '<div class="row"><label for="in-camp$">Cost of one such camp</label><div><output id="o-camp$"></output><input type="range" id="in-camp$" min="50" max="600" step="25" value="250"></div></div>' +
      '<div class="row"><label for="in-meets">Verified mark meets entered (clock sports)</label><div><output id="o-meets"></output><input type="range" id="in-meets" min="0" max="8" step="1" value="2"></div></div>' +
      '<div class="row"><label for="in-fee">Entry fee per meet</label><div><output id="o-fee"></output><input type="range" id="in-fee" min="10" max="60" step="5" value="25"></div></div>' +
      '<div class="res" aria-live="polite"><div class="red"><strong id="r-show"></strong>generic spend moved out</div><div><strong id="r-ess"></strong>verified essentials</div><div><strong id="r-left"></strong>left over, unspent</div></div>' +
      '<ul class="sg-ess"><li><span>NCAA Eligibility Center certification (domestic; fee waivers possible)</span><b>' + money(S.ncaa_cert_fee) + '</b></li><li><span>Single-school camp(s), only after coach contact</span><b id="e-camps"></b></li><li><span>Verified mark meets</span><b id="e-meets"></b></li></ul>' +
      '<p class="note">Fee: <a href="' + esc(S.ncaa_cert_url) + '" rel="noopener">NCAA Registration Checklist</a>. Camp and meet prices are yours to enter; they are not benchmarks. The tool does not tell you what to spend, it shows what leaving the generic line frees up.</p>';
    var ids = ['show', 'camps', 'camp$', 'meets', 'fee'];
    function upd() {
      var v = {}; ids.forEach(function (k) { v[k] = +document.getElementById('in-' + k).value; });
      $('#o-show').textContent = money(v.show); $('#o-camps').textContent = v.camps + (v.camps === 1 ? ' camp' : ' camps');
      $('[id="o-camp$"]').textContent = money(v['camp$']); $('#o-meets').textContent = v.meets + (v.meets === 1 ? ' meet' : ' meets'); $('#o-fee').textContent = money(v.fee);
      var camps = v.camps * v['camp$'], meets = v.meets * v.fee, ess = S.ncaa_cert_fee + camps + meets;
      $('#e-camps').textContent = money(camps); $('#e-meets').textContent = money(meets);
      $('#r-show').textContent = money(v.show); $('#r-ess').textContent = money(ess);
      var left = v.show - ess; $('#r-left').textContent = left >= 0 ? money(left) : 'over by ' + money(-left);
    }
    ids.forEach(function (k) { document.getElementById('in-' + k).addEventListener('input', upd); });
    upd();
  }
  function renderSizing() {
    var Z = D.sizing, top = Z.rows.slice(0, 8);
    $('#sizing').innerHTML =
      '<span class="tag">' + esc(Z.label.toUpperCase()) + '</span><h3>How many families might this serve? A model, not a census.</h3>' +
      '<p>Our working estimate is about <b>' + Z.total_serviceable_families.toLocaleString('en-US') + '</b> serviceable families (this double counts multi-sport kids). It is built from these assumptions:</p><ul>' +
      Z.assumptions.map(function (a) { return '<li>' + esc(a) + '</li>'; }).join('') + '</ul>' +
      '<p class="note">Participation: ' + esc(Z.participation_source) + '. The college-intent and paying-share rates are our guesses, not survey results. The right-hand column is a ceiling, not a forecast.</p>' +
      '<div class="sg-table-wrap"><table><caption class="vh">Largest sports by modeled serviceable families</caption><thead><tr><th>Sport</th><th class="num">HS participants 2024-25</th><th class="num">Modeled paying families (ESTIMATE)</th></tr></thead><tbody>' +
      top.map(function (r) { return '<tr><td>' + esc(r.sport) + '</td><td class="num">' + esc(r.hs) + '</td><td class="num">' + esc(r.paying) + '</td></tr>'; }).join('') + '</tbody></table></div>';
  }

  /* ---------- boot ---------- */
  function boot() {
    initTabs();
    fetch('/segments/segments.json').then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); }).then(function (d) {
      D = d; renderSegGrid(); renderHonesty(); renderChainPick(); renderChain(); renderBench(); renderCalc(); renderSizing();
      var m = /[?&]segment=([a-z]+)/.exec(location.search);
      if (m) { var s = D.segments.filter(function (x) { return x.key === m[1]; })[0]; if (s) pickSeg(s.id, false); }
    }).catch(function () {
      $('#seg-plan').innerHTML = '<p>The data file did not load. The free tools are still here: <a href="/start/">Start here</a>, <a href="/calendar/">Calendar</a>, <a href="/playbooks/">Playbooks</a>.</p>';
    });
    var mb = $('.menu-btn'); if (mb) mb.addEventListener('click', function () { var n = $('#site-nav'); var o = n.classList.toggle('open'); mb.setAttribute('aria-expanded', o); });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
