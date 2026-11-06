const fs=require('fs');
const M=JSON.parse(fs.readFileSync('../W7-marketing/MARKETING.json','utf8'));
const map=JSON.parse(fs.readFileSync('landing-page-map.json','utf8'));
// Cards transcribed from W7-marketing/AD-PLAN.md (draft concepts); route = new solution route mapped in landing-page-map.json
const C=[
['F1','football','Proof over hype','Football parents: every date a college coach is allowed to contact your son. With the rule number.','FREE-PDF','Static + 9:16 text reel, FB/IG feed + Reels','/start','/calendar/',null],
['F2','football','Late isn\'t over (Arc 1)','He\'s a senior with no film sent. Here\'s what an honest next 30 days looks like.','FREE-START then late-bloomer','Talking-head or text reel','/recruitiq','/playbooks/late-bloomer/','marpet (typography only)'],
['F3','football','We paid, nothing happened (Arc 3)','Before you pay a recruiting service, read this comparison.','FREE /compare/ + $9 upsell','Carousel','/personalize','/compare/','Marcus (composite)'],
['S1','travel_baseball_softball','Camp/showcase ROI','Spending weekends at showcases? Check which ones fit before the next one.','FREE-START','Reel','/segments','/playbooks/camp-roi/','Kayla (composite)'],
['S2','travel_baseball_softball','Honest money math','Baseball parents: scholarships at D1 are split across a roster. See the math with sources.','FREE /math/','Static','/segments','/math/',null],
['S3','travel_baseball_softball','Late isn\'t over','JUCO first is a real route. Here\'s one composite path.','FREE-START','Carousel','/start','/story/composite-baseball/','Diego (composite)'],
['V1','club_volleyball','Sport-specific rules','Volleyball parents: the recruiting dates are different for your sport. Here they are.','FREE-PDF','Static calendar image, IG feed/Stories','/segments','/calendar/',null],
['V2','club_volleyball','Late specializer','Two-sport kid, started club late. Here\'s the path that composite followed.','FREE-START','Reel, Illustration-labeled','/personalize','/story/composite-volleyball/','Ava (composite, labeled)'],
['V3','club_volleyball','Give me the words (Arc 5)','What to write in the first email to a college volleyball coach.','FREE-START','Text reel','/start','/start/',null],
['W1','wrestling_incl_girls','New-sport pride (Arc 6)','Women\'s wrestling is now an NCAA championship sport at D-III. Here\'s how recruiting works.','FREE-START','Static + reel','/emerging-sports','/story/rodriguez/','Cristelle Rodriguez, NAIA (typography)'],
['W2','wrestling_incl_girls','Nobody told us (Arc 2)','Two NCAA Eligibility Center steps families miss. Both explained for $9.','$9','Static','/recruitiq','/playbooks/eligibility-2-hard-deadlines/','Tyler (composite)'],
['L1','late_start_jr_sr','Arc 1 (also AAU basketball)','Junior or senior and nothing sent yet? Start here. (addressed to parents in body copy)','FREE-START','Reel','/recruitiq','/playbooks/late-bloomer/','Jimmy Butler JUCO path (typography)'],
['L2','late_start_jr_sr','Arc 2 + anti-service','The two dates that can cost eligibility. $9, no sales call.','$9','Static','/recruitiq','/playbooks/eligibility-2-hard-deadlines/',null],
['G1','girls_flag_football','Emerging sport (small $50 test)','Girls flag football grew 60% in one year (NFHS 2024-25). Where can she play in college?','FREE-START','Static','/emerging-sports','/start/','Program list is a sourcing GAP: say where to look, do not list schools'],
['T1','track_xc','Academics opened the door (Arc 7; small $50 test)','Track parents: the real question is often the academic package. See the aid math.','FREE /math/','Static','/segments','/story/rodenfels/','Annie Rodenfels (story HELD/noindex: do not link until released)']
].map(a=>({id:a[0],segment:a[1],angle:a[2],first_3_seconds:a[3],offer:a[4],format:a[5],new_route:a[6],ad_plan_landing:a[7],story:a[8],status:'DRAFT - not posted, not launched, needs Mike OK on exact text'}));
// consistency: every card id must appear in MARKETING.json segments' ads
const known=new Set(Object.values(M.segments).flatMap(s=>s.ads));
for(const c of C) if(!known.has(c.id)) throw new Error('unknown ad '+c.id);
fs.writeFileSync('cards.json',JSON.stringify({status:'DRAFT',cards:C},null,1));
const esc=s=>String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
const segs=map.buyer_segments.map(s=>s.id).concat(['girls_flag_football','track_xc']);
const segLabel=Object.fromEntries(map.buyer_segments.map(s=>[s.id,s.label]).concat([['girls_flag_football','Girls flag football (small test)'],['track_xc','Track / XC (small test)']]));
const html=`<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">
<title>W11 Ad &amp; Story Angle Playbook (DRAFT)</title>
<style>
:root{--ink:#0a0a0a;--paper:#f5f3ef;--red:#d2321e}*{box-sizing:border-box}
body{margin:0;font:16px/1.6 'Inter Tight','Helvetica Neue',Arial,sans-serif;background:#fff;color:var(--ink)}
header{background:var(--ink);color:var(--paper);padding:40px 32px}
h1{font:400 clamp(30px,5vw,60px)/.95 'Anton',Impact,sans-serif;text-transform:uppercase;margin:0 0 12px}
.banner{background:#fff3b0;color:#0a0a0a;border-bottom:2px solid #0a0a0a;padding:12px 32px;font:600 14px 'Barlow Condensed',sans-serif;letter-spacing:.06em;text-transform:uppercase}
main{max-width:1180px;margin:0 auto;padding:24px 32px 80px}
.bar{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:20px}
select{font:16px inherit;padding:10px;border:1.5px solid var(--ink);background:var(--paper);height:46px;min-width:220px}
label{display:flex;flex-direction:column;font:700 12px 'Barlow Condensed',sans-serif;letter-spacing:.14em;text-transform:uppercase;gap:6px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:12px;list-style:none;padding:0}
.card{border:1.5px solid var(--ink);background:var(--paper);padding:18px;display:flex;flex-direction:column;gap:8px}
.card .id{font:500 13px 'JetBrains Mono',monospace;color:var(--red)}
.card h2{font:700 20px/1.15 'Barlow Condensed',sans-serif;margin:0}
.card blockquote{margin:0;border-left:4px solid var(--red);padding-left:12px}
.card dl{margin:0;font-size:13px;display:grid;grid-template-columns:96px 1fr;gap:4px 8px}
.card dt{font:700 11px 'Barlow Condensed',sans-serif;letter-spacing:.12em;text-transform:uppercase;color:#46423b}.card dd{margin:0}
.route{font:500 13px 'JetBrains Mono',monospace}
.tag{display:inline-block;background:var(--ink);color:#fff;padding:2px 8px;font:600 11px 'Barlow Condensed',sans-serif;letter-spacing:.1em;text-transform:uppercase;align-self:flex-start}
.status{font:500 12px 'JetBrains Mono',monospace}
</style></head><body>
<header><h1>Ad &amp; Story Angle Playbook</h1><p>Draft creative cards from v3/W7-marketing, mapped to /start, /access, /recruitiq, /personalize, /segments, /emerging-sports and /resources.</p></header>
<div class="banner">Draft only. Nothing here is posted, launched or scheduled. Every card needs Mike's OK on the exact text. Routes other than /start are not yet live in site/.</div>
<main>
<div class="bar"><label>Buyer segment<select id="seg"><option value="">All segments</option>${segs.map(s=>`<option value="${s}">${esc(segLabel[s])}</option>`).join('')}</select></label>
<label>Landing route<select id="route"><option value="">All routes</option>${['/start','/access','/recruitiq','/personalize','/segments','/emerging-sports','/resources'].map(r=>`<option>${r}</option>`).join('')}</select></label></div>
<p class="status" id="count" role="status" aria-live="polite"></p>
<ul class="grid" id="cards"></ul>
<p style="font-size:13px;color:#46423b">/resources links third-party Gumroad products by McKinley Malbrough III (MM3 Sports); they are not Commit Book products. Rodenfels story is HELD (noindex): no offers are linked from it.</p>
</main>
<script>
const CARDS=${JSON.stringify(C)};const LABEL=${JSON.stringify(segLabel)};
const ul=document.getElementById('cards'),seg=document.getElementById('seg'),rt=document.getElementById('route'),cnt=document.getElementById('count');
function mk(t,c,x){const e=document.createElement(t);if(c)e.className=c;e.textContent=x;return e}
function render(){ul.textContent='';const l=CARDS.filter(c=>(!seg.value||c.segment===seg.value)&&(!rt.value||c.new_route===rt.value));
 l.forEach(c=>{const li=mk('li','card');li.appendChild(mk('span','id',c.id));li.appendChild(mk('span','tag','DRAFT'));li.appendChild(mk('h2','',c.angle));
 const q=document.createElement('blockquote');q.textContent=c.first_3_seconds;li.appendChild(q);
 const dl=document.createElement('dl');[['Segment',LABEL[c.segment]],['Offer',c.offer],['Format',c.format],['New route',c.new_route],['Interim landing',c.ad_plan_landing],['Story',c.story||'none']].forEach(p=>{dl.appendChild(mk('dt','',p[0]));dl.appendChild(mk('dd',p[0].includes('route')?'route':'',p[1]))});li.appendChild(dl);ul.appendChild(li)});
 cnt.textContent=l.length+' of '+CARDS.length+' draft cards';}
seg.onchange=rt.onchange=render;render();
</script></body></html>`;
fs.writeFileSync('index.html',html);
console.log(C.length,'cards');
