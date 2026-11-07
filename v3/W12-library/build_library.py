#!/usr/bin/env python3
"""Build the Commit Book Library page (/library).

Mike's ruling 2026-11-07 (verbatim): "remove all mckinley malbrough III references and
rebrand as the 'The commit book'". This page is The Commit Book's own catalog: our tools,
our playbooks, our free interactive pages, our paid tier. No third-party attribution.

Writes four files into the W11 overlay (the sync script copies them into site/):
  v3/W11-site-overlay/library/index.html
  v3/W11-site-overlay/library/library.css
  v3/W11-site-overlay/library/library.js
  v3/W11-site-overlay/library/library.json
"""
import json, os, re, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "v3", "W11-site-overlay", "library")
os.makedirs(OUT, exist_ok=True)

OFF = json.load(open(os.path.join(ROOT, "v3", "W8-offerings", "OFFERINGS.json")))

SEG_NAMES = {1: "Early planner (9th-10th)", 2: "Late start (junior/senior)",
             3: "Burned by a service", 4: "High-academic D3 / merit aid",
             5: "Clock / mark sport", 6: "Emerging sport or JUCO"}

# Which buyer each offering serves, and the one line of value for them. Kept true to the
# offering's own contents list in OFFERINGS.json - no stretching.
AUDIENCE = {
  "contact-log":       ([2, 5], "build",   "Your coach list stops living in your inbox."),
  "red-flags":         ([3, 2, 4], "verify", "Judge a program yourself before you pay it anything."),
  "offer-comparison":  ([4, 3], "decide",  "Compare offers on the dollar number, not the letter."),
  "nil-starter":       ([4, 1, 3], "protect", "A first NIL deal without signing away the wrong clause."),
  "nil-tax":           ([4, 3], "protect",  "Money you kept in sport does not become an April surprise."),
  "local-nil":         ([6, 5, 4], "protect", "Three local deals you can find yourself, in your own town."),
  "season-planner":    ([1, 2, 5], "build", "One page that tells you what to film and when to send it."),
  "career-transition": ([1, 6, 3], "after", "A plan for the 98% that does not wait until the last game."),
  "coach-emails":      ([2, 5, 1], "build", "Twelve moments, twelve subject lines that get opened."),
  "bundle":            ([4, 3, 1], "buy",   "Every tool and playbook, one purchase, no upsell ladder.")
}

FREE_PAGES = [
  ("/start", "Start here by grade", "The 9th-to-12th-grade sequence, with the rule number next to every date.", [1, 2, 6], "orient"),
  ("/calendar", "Rule calendar", "Every NCAA date that matters for your sport and class year, cited to its bylaw.", [1, 2, 5], "orient"),
  ("/access", "Reach coaches yourself", "Earliest legal contact date by sport and class, an athlete-voice email builder with a red-flag linter, and a 30-school tracker you can export.", [2, 5, 3], "build"),
  ("/recruitiq", "Standards & fit explorer", "Real Division I marks and times for the event, with the roster and aid math behind them.", [2, 3, 5], "verify"),
  ("/math", "Roster and aid math", "How many spots actually exist, and what aid can stack on top.", [4, 3], "verify"),
  ("/compare", "Compare recruiting services", "What a paid service does, what you can do yourself, and how to get out.", [3, 1], "verify"),
  ("/emerging-sports", "Emerging sports hub", "Flag football, women's wrestling, men's volleyball: the first three steps where no playbook existed.", [6], "orient"),
  ("/personalize", "Denver metro checks", "Camps and trainers near you, each row with its source and check date. Denver area only.", [1, 2], "verify"),
  ("/segments", "Where are we right now?", "Six parent situations, each with a plan you can work this week.", [1, 2, 3, 4, 5, 6], "orient"),
  ("/answers", "Parent answers", "Ten recruiting rules answered plainly, each cited to its bylaw.", [1, 2, 5], "orient")
]

PLAY_TITLES = {
  "baseball-showcase-to-signing": ("Baseball: showcase to signing", [2, 5]),
  "camp-roi": ("Camp ROI", [1, 3]),
  "d3-academic-aid-first": ("D3 path: academic aid first", [4]),
  "eligibility-2-hard-deadlines": ("Eligibility: the 2 hard deadlines", [1, 2]),
  "football-junior-year": ("Football: junior year", [2, 5]),
  "highlight-reel-social": ("Highlight reel and social", [2, 6]),
  "juco-to-d1": ("JUCO to D1", [6, 2]),
  "late-bloomer": ("Late bloomer", [2, 6]),
  "nil-high-school": ("NIL for high schoolers", [1, 4]),
  "offer-and-signing": ("Offers and signing day", [4, 3]),
  "track-field-marks": ("Track and field: marks to roster", [5]),
  "walk-on": ("Walk-on", [6, 2])
}

STAGES = [("orient", "Get oriented"), ("build", "Build the list and the message"),
          ("verify", "Verify the level and the pitch"), ("decide", "Decide on an offer"),
          ("protect", "Protect the money"), ("after", "Life after the roster"),
          ("buy", "Own the whole shelf")]

now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
offers = []
for o in OFF["offerings"]:
    aud, stage, why = AUDIENCE[o["slug"]]
    offers.append({
      "slug": o["slug"], "title": o["title"], "price": o["price"],
      "price_label": "$0+ (free)" if o["price"] == 0 else "$%d" % o["price"],
      "status": o["status"], "tagline": o["tagline"], "contents": o["contents"], "price_num": o["price"],
      "audience": aud, "stage": stage, "why": why,
      "href": "/tools/" + o["slug"],
      "action": "Notify me when it ships"
    })

playbooks = []
pb_dir = os.path.join(ROOT, "site", "playbooks")
for slug in sorted(os.listdir(pb_dir)):
    if slug in PLAY_TITLES and os.path.isdir(os.path.join(pb_dir, slug)):
        title, aud = PLAY_TITLES[slug]
        playbooks.append({"slug": slug, "title": title, "href": "/playbooks/%s/" % slug,
                          "audience": aud, "stage": "build"})

data = {"generated": now, "source": "v3/W8-offerings/OFFERINGS.json + v3/W12-journey/BUYER-JOURNEY.json (if present) + site/playbooks",
        "brand": "The Commit Book",
        "checkout": "Preview: purchases are off until the payment gateway flag is flipped. Every tool below is notify-only until its download page goes live.",
        "ready_means": "Ready = the full contents are written and checked. The download page is the next build item, so every tool asks for an email first.",
        "tiers": [{"name": "Sideline", "price": 149, "cadence": "per year", "offered": True,
                   "line": "Every date, every playbook, every tool, all year."},
                  {"name": "Pathway", "price": 99, "cadence": "one year", "offered": True,
                   "line": "One class year, start to signing.", "note": "Founding price, 100 slots"},
                  {"name": "Audit", "price": None, "cadence": "one-off", "offered": False,
                   "line": "Announced, not sold yet."},
                  {"name": "Club", "price": None, "cadence": "per team", "offered": False,
                   "line": "Announced, not sold yet."}],
        "stages": [{"key": k, "label": v} for k, v in STAGES],
        "segments": [{"id": i, "name": SEG_NAMES[i]} for i in range(1, 7)],
        "offers": offers,
        "free_pages": [{"href": h, "title": t, "why": w, "audience": a, "stage": g, "kind": "free"} for (h, t, w, a, g) in FREE_PAGES],
        "playbooks": playbooks}

open(os.path.join(OUT, "library.json"), "w").write(json.dumps(data, indent=1))

# ---- HTML ----
NAV = ('<header class="site-header cb-header"><a class="brand" href="/" aria-label="The Commit Book home">'
       '<img src="/assets/logo/lockup-horizontal-light.svg" alt="The Commit Book" width="135" height="30"></a>'
       '<button class="menu-btn" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>'
       '<nav id="site-nav" aria-label="Main"><a href="/start">Start here</a><a href="/">Stories</a>'
       '<a href="/access">Access</a><a href="/recruitiq">RecruitIQ</a><a href="/personalize">Personalize</a>'
       '<a href="/segments">Segments</a><a href="/emerging-sports">Emerging sports</a>'
       '<a href="/library">Library</a><a href="/playbooks">Playbooks</a><a href="/price">Price</a></nav>'
       '<a class="bag" href="/playbooks">Bag (<span data-bag-count>0</span>)</a></header>')

HTML = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Commit Book Library: every tool, playbook and calendar in one place</title>
<meta name="description" content="The Commit Book's own catalog: free rule calendar, contact-date calculator and standards explorer, 12 playbooks, 10 tools for NIL, offers, film and life after the roster. Prices, what is ready, and what is announced only.">
<meta name="robots" content="noindex"><!-- DRAFT: pending Mike's approval to publish -->
<link rel="stylesheet" href="/assets/tokens.css">
<link rel="stylesheet" href="/assets/commit.css?v=6ac59abf">
<link rel="stylesheet" href="/library/library.css">
</head><body>
<a class="skip" href="#catalog">Skip to the catalog</a>
__NAV__
<main class="lb-page">
<section class="lb-hero">
  <p class="lb-kicker">THE COMMIT BOOK LIBRARY</p>
  <h1 class="lb-h1">Everything we make, in one place, with the honest status of each</h1>
  <p class="lb-lead">Free pages you can use now, playbooks written from the rulebook, and tools for the parts that cost a family money: offers, NIL, film, and life after the roster. Nothing here is a third party's product. Purchases are in preview, so announced items are notify-only.</p>
</section>
<section class="lb-tiers" id="tiers" aria-label="Membership"></section>
<section class="lb-filters" aria-label="Filter the catalog">
  <div class="lb-field"><label for="f-seg">Where you are now</label>
    <select id="f-seg"><option value="">Any parent situation</option></select></div>
  <div class="lb-field"><label for="f-stage">Journey stage</label>
    <select id="f-stage"><option value="">Any stage</option></select></div>
  <div class="lb-field"><label for="f-kind">Kind</label>
    <select id="f-kind"><option value="">Everything</option><option value="free">Free interactive page</option><option value="playbook">Playbook</option><option value="ready">Tool: ready</option><option value="soon">Tool: announced only</option></select></div>
  <button class="lb-reset" id="f-reset" type="button">Reset</button>
</section>
<p class="lb-status" id="status" role="status" aria-live="polite"></p>
<div id="catalog"></div>
<noscript><p class="lb-fine">Turn on JavaScript to filter the catalog. The playbooks are all at <a href="/playbooks">/playbooks</a> and the paid tools are listed on <a href="/price">/price</a>.</p></noscript>
<p class="lb-foot"><span id="ready-means"></span> Education, not legal advice. We do not recruit or place athletes and nobody here contacts your kid. No scholarship, offer or roster spot is promised. Prices checked __DATE__.</p>
</main>
<script src="/library/library.js" defer></script>
<script src="/assets/stories.js?v=3af55b96"></script><script src="/assets/site.js" defer></script></body></html>"""

today = datetime.date.today().isoformat()
html = HTML.replace("__NAV__", NAV).replace("__DATE__", today)
open(os.path.join(OUT, "index.html"), "w").write(html)

CSS = """/* The Commit Book Library. Brand tokens: Anton / Barlow Condensed / Inter Tight / JetBrains Mono; ink #0a0a0a, paper #f5f3ef, red #d2321e, blue #1151ff. */
.lb-page{max-width:1180px;margin:0 auto;padding:0 var(--gutter,24px) 96px;color:var(--ink,#0a0a0a);font-family:var(--font-text,'Inter Tight',sans-serif)}
body{background:#fff}
.lb-hero{margin:0 -100vw;padding:64px calc(100vw - ((100vw - var(--gutter,24px) * 2) / 2)) 56px;background:var(--ink,#0a0a0a);color:var(--paper,#f5f3ef)}
.lb-kicker{margin:0 0 12px;color:#d2321e;font:700 12px/1 var(--font-condensed,'Barlow Condensed',sans-serif);letter-spacing:.22em}
.lb-h1{margin:0 0 18px;font:400 clamp(38px,7.4vw,88px)/.92 var(--font-display,Anton,Impact,sans-serif);text-transform:uppercase;letter-spacing:-.01em}
.lb-lead{margin:0;max-width:62ch;color:var(--body,#46423b);font:400 clamp(17px,1.5vw,21px)/1.5 var(--font-text,'Inter Tight',sans-serif)}
.lb-hero .lb-lead{color:#f5f3ef}
.lb-tiers{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px;margin:28px 0 4px}
.lb-tier{border:1.5px solid var(--rule,#cacacb);background:#fff;padding:18px}
.lb-tier.on{border-color:var(--ink,#0a0a0a)}
.lb-tier h2{margin:0 0 6px;font:700 20px/1.05 var(--font-condensed,'Barlow Condensed',sans-serif);text-transform:uppercase;letter-spacing:.06em}
.lb-tier .amt{font:500 24px/1 var(--font-mono,'JetBrains Mono',monospace);color:var(--ink,#0a0a0a)}
.lb-tier .amt small{font-size:13px;color:#46423b}
.lb-tier p{margin:8px 0 0;font-size:14.5px;line-height:1.45;color:#46423b}
.lb-tier .note{display:inline-block;margin-top:8px;padding:3px 8px;border-radius:999px;background:#fff3b0;border:1px solid var(--ink,#0a0a0a);font:600 11px var(--font-condensed,sans-serif);letter-spacing:.08em;text-transform:uppercase}
.lb-filters{display:flex;flex-wrap:wrap;gap:16px;align-items:flex-end;padding:24px 0;border-bottom:1px solid var(--rule,#cacacb);position:sticky;top:60px;background:#fff;z-index:20}
.lb-field{display:flex;flex-direction:column;gap:6px;flex:1;min-width:210px}
.lb-field label{font:600 12px/1 var(--font-condensed,'Barlow Condensed',sans-serif);letter-spacing:.14em;text-transform:uppercase;color:#46423b}
.lb-field select{font:400 16px var(--font-text,'Inter Tight',sans-serif);padding:12px;border:1.5px solid var(--ink,#0a0a0a);background:#f5f3ef;border-radius:0;height:48px}
.lb-field select:focus-visible,.lb-reset:focus-visible,.lb-card a:focus-visible{outline:2px solid #1151ff;outline-offset:2px}
.lb-reset{height:48px;padding:0 24px;border:1.5px solid var(--rule,#cacacb);background:none;border-radius:30px;font:500 15px var(--font-text,'Inter Tight',sans-serif);cursor:pointer}
.lb-reset:hover{border-color:var(--ink,#0a0a0a)}
.lb-status{font:500 13px/1.4 var(--font-mono,'JetBrains Mono',monospace);color:#46423b;margin:20px 0 8px}
.lb-group{margin-top:34px}
.lb-group h2{margin:0 0 4px;font:700 26px/1 var(--font-condensed,'Barlow Condensed',sans-serif);text-transform:uppercase;letter-spacing:.04em;color:var(--ink,#0a0a0a)}
.lb-group .sub{margin:0 0 14px;color:#46423b;font-size:14.5px;line-height:1.45}
.lb-grid{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:12px}
.lb-card{position:relative;border:1.5px solid var(--rule,#cacacb);background:#fff;padding:18px 18px 16px;display:flex;flex-direction:column;gap:8px;border-radius:4px}
.lb-card.ready,.lb-card.playbook{border-color:var(--ink,#0a0a0a)}
.lb-kind{display:inline-block;padding:3px 8px;border:1px solid var(--rule,#cacacb);border-radius:999px;font:600 11px/1 var(--font-condensed,'Barlow Condensed',sans-serif);letter-spacing:.1em;text-transform:uppercase;color:#46423b;align-self:flex-start}
.lb-kind.free{border-color:#1151ff;color:#1151ff}
.lb-kind.ready{border-color:#007d48;color:#007d48}
.lb-kind.soon{border-color:#9a4a00;color:#9a4a00}
.lb-card h3{margin:2px 0 0;font:400 clamp(22px,2.1vw,29px)/1.02 var(--font-display,Anton,Impact,sans-serif);text-transform:uppercase;letter-spacing:-.005em}
.lb-why{margin:0;color:var(--red,#d2321e);font:500 13px/1.35 var(--font-text,'Inter Tight',sans-serif)}
.lb-tag{margin:0;color:#46423b;font-size:14.5px;line-height:1.45}
.lb-contents{margin:0;padding-left:18px;color:#46423b;font-size:13.5px;line-height:1.45}
.lb-seg{margin:0;display:flex;flex-wrap:wrap;gap:6px;padding:0;list-style:none}
.lb-seg li{padding:3px 8px;border:1px solid var(--rule,#cacacb);border-radius:999px;font:600 11px/1 var(--font-condensed,'Barlow Condensed',sans-serif);letter-spacing:.06em;text-transform:uppercase;color:#46423b}
.lb-act{margin-top:auto;padding-top:10px;display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.lb-price{font:500 13px/1 var(--font-mono,'JetBrains Mono',monospace);color:var(--ink,#0a0a0a)}
.lb-link{display:inline-block;padding:10px 16px;border-radius:999px;background:var(--ink,#0a0a0a);color:#fff;text-decoration:none;font:600 13px/1 var(--font-condensed,'Barlow Condensed',sans-serif);letter-spacing:.08em;text-transform:uppercase}
.lb-link:hover{background:var(--red,#d2321e)}
.lb-fine{margin:8px 0 0;font:500 13px/1.45 var(--font-mono,'JetBrains Mono',monospace);color:#46423b}
.lb-foot{margin-top:40px;padding-top:20px;border-top:1px solid var(--rule,#cacacb);font-size:13px;color:#46423b;max-width:52em}
@media (max-width:749px){.lb-hero{padding-top:40px}.lb-filters{position:static}.lb-field{min-width:100%}}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
"""
open(os.path.join(OUT, "library.css"), "w").write(CSS)

JS = """/* The Commit Book Library renderer. Data: /library/library.json. Brand: all items are ours; no third-party attribution. */
(function(){
  'use strict';
  function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e}
  function segNames(d,ids){return ids.map(function(i){for(var k=0;k<d.segments.length;k++){if(d.segments[k].id===i)return d.segments[k].name}return 'Segment '+i})}
  function stageLabel(d,k){for(var i=0;i<d.stages.length;i++){if(d.stages[i].key===k)return d.stages[i].label}return k}
  function card(o){
    var li=el('li','lb-card '+o.kind);
    var badge=el('span','lb-kind '+o.kind,o.badge);li.appendChild(badge);
    li.appendChild(el('h3',null,o.title));
    if(o.why)li.appendChild(el('p','lb-why',o.why));
    if(o.tagline)li.appendChild(el('p','lb-tag',o.tagline));
    if(o.contents){var ul=el('ul','lb-contents');o.contents.forEach(function(c){ul.appendChild(el('li',null,c))});li.appendChild(ul)}
    var segs=el('ul','lb-seg');segNames(DATA,o.audience).forEach(function(n){segs.appendChild(el('li',null,n))});li.appendChild(segs);
    var act=el('div','lb-act');
    if(o.price_label)act.appendChild(el('span','lb-price',o.price_label));
    var a=el('a','lb-link',o.cta);a.href=o.href;act.appendChild(a);
    li.appendChild(act);
    li.dataset.audience=JSON.stringify(o.audience);li.dataset.stage=o.stage;li.dataset.kind=o.kind;
    return li;
  }
  var DATA,grid,status,fs,fk,fg,reset;
  function allCards(){return Array.prototype.slice.call(grid.querySelectorAll('li'))}
  function render(){
    var sv=fs.value,kv=fk.value,gv=fg.value,shown=0;
    allCards().forEach(function(li){
      var ok=true;
      if(sv){ok=ok&&(JSON.parse(li.dataset.audience).indexOf(+sv)>=0)}
      if(kv){ok=ok&&li.dataset.kind===kv}
      if(gv){ok=ok&&li.dataset.stage===gv}
      li.hidden=!ok;
      if(ok)shown++;
    });
    Array.prototype.slice.call(grid.querySelectorAll('.lb-group')).forEach(function(g){
      var any=g.querySelectorAll('li:not([hidden])').length;g.hidden=!any;
    });
    status.textContent=shown+' of '+allCards().length+' items'+(sv||kv||gv?' match your filters':' in the library');
    var q=new URLSearchParams();if(sv)q.set('seg',sv);if(kv)q.set('kind',kv);if(gv)q.set('stage',gv);
    history.replaceState(null,'',q.toString()?'?'+q:location.pathname);
  }
  function tiers(d){
    var box=document.getElementById('tiers');if(!box)return;
    d.tiers.forEach(function(t){
      var c=el('div','lb-tier'+(t.offered?' on':''));
      c.appendChild(el('h2',null,t.name));
      var amt=el('div','amt');
      amt.textContent=t.price?('+'===String(t.price).charAt(0)?String(t.price):'$'+t.price):'Price TBC';
      if(t.cadence&&t.price)amt.appendChild(el('small',null,' / '+t.cadence));
      c.appendChild(amt);c.appendChild(el('p',null,t.line));
      if(t.note)c.appendChild(el('span','note',t.note));
      if(!t.offered)c.appendChild(el('span','note','Announced, not sold yet'));
      box.appendChild(c);
    });
  }
  function groups(d){
    d.stages.forEach(function(st){
      var sec=el('section','lb-group');sec.dataset.stage=st.key;
      sec.appendChild(el('h2',null,st.label));
      var ul=el('ul','lb-grid');
      d.free_pages.forEach(function(p){if(p.stage===st.key)ul.appendChild(card(mk(p,'free','Free interactive page')))});
      d.playbooks.forEach(function(p){if(p.stage===st.key)ul.appendChild(card(mk(p,'playbook','Playbook')))});
      d.offers.forEach(function(o){if(o.stage===st.key)ul.appendChild(card(mk(o,'soon'==='x'?'ready':(o.status==='BUILT'?'ready':'soon'),(o.status==='BUILT'?'Contents written':'Announced only'))})});
      sec.appendChild(ul);grid.appendChild(sec);
    });
  }
  function mk(p,kind,badge){
    var cta=p.cta||(kind==='playbook'?'Read':(kind==='free'?'Open':'Notify me'));
    return {kind:kind,badge:badge,title:p.title,why:p.why||'',tagline:p.tagline||'',contents:p.contents||[],
            audience:p.audience,stage:p.stage,href:p.href,price_label:p.price_label||'',cta:cta};
  }
  function init(d){
    DATA=d;grid=document.getElementById('catalog');status=document.getElementById('status');
    fs=document.getElementById('f-seg');fk=document.getElementById('f-kind');fg=document.getElementById('f-stage');
    reset=document.getElementById('f-reset');
    tiers(d);groups(d);
    var rm=document.getElementById('ready-means');if(rm&&d.ready_means)rm.textContent=d.ready_means;
    d.segments.forEach(function(s){var o=el('option',null,s.name);o.value=s.id;fs.appendChild(o)});
    d.stages.forEach(function(s){var o=el('option',null,s.label);o.value=s.key;fg.appendChild(o)});
    [fs,fk,fg].forEach(function(x){x.addEventListener('change',render)});
    reset.addEventListener('click',function(){fs.value='';fk.value='';fg.value='';render()});
    var q=new URLSearchParams(location.search);
    if(q.get('seg'))fs.value=q.get('seg');if(q.get('kind'))fk.value=q.get('kind');if(q.get('stage'))fg.value=q.get('stage');
    render();
  }
  fetch('/library/library.json').then(function(r){return r.json()}).then(init).catch(function(){
    var s=document.getElementById('status');if(s)s.textContent='Could not load the library data. The playbooks are at /playbooks and paid tools are on /price.';
  });
})();
"""
open(os.path.join(OUT, "library.js"), "w").write(JS)

# forbidden: the third-party attribution Mike killed
blob = html + CSS + JS + json.dumps(data)
for w in ["McKinley", "Malbrough", "MM3", "Gumroad", "gumroad", "malbrough6"]:
    assert w not in blob, "attribution leaked into /library: " + w
print("library.json", len(json.dumps(data)), "bytes | offers", len(offers), "| playbooks", len(playbooks),
      "| free pages", len(FREE_PAGES), "| attribution words: 0")
