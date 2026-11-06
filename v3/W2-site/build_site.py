import json,os,re,html,glob
R=os.path.expanduser('~/Developer/recruiting-calendar');SITE=R+'/site'
D=json.load(open(R+'/v3/W2-site/data.json'));A=D['athletes'];P=D['playbooks']
SEO=json.load(open(R+'/v3/W2-seo/head-tags.json'))
e=html.escape
HEADIN='<link rel="icon" href="/assets/logo/favicon.svg" type="image/svg+xml"><link rel="icon" href="/assets/logo/favicon-32.png" sizes="32x32"><link rel="apple-touch-icon" href="/assets/logo/favicon-256.png"><meta property="og:image" content="/assets/logo/social-card-dark.png"><meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#ffffff">'
import hashlib
RV=hashlib.md5(open(SITE+'/assets/ring.css','rb').read()).hexdigest()[:8];JV=hashlib.md5(open(SITE+'/assets/ring.js','rb').read()).hexdigest()[:8]
CV=hashlib.md5(open(SITE+'/assets/commit.css','rb').read()).hexdigest()[:8]
KV=hashlib.md5(open(SITE+'/checkout.js','rb').read()).hexdigest()[:8]
DV=hashlib.md5(open(SITE+'/assets/deck.js','rb').read()+open(SITE+'/assets/deck.css','rb').read()).hexdigest()[:8]
CSS='<script src="/checkout.js?v='+KV+'" defer></script><link rel="stylesheet" href="/assets/tokens.css"><link rel="stylesheet" href="/assets/commit.css?v='+CV+'">'
HDR='''<header class="site-header cb-header"><a class="brand" href="/" aria-label="The Commit Book home"><img src="/assets/logo/lockup-horizontal-light.svg" alt="The Commit Book" width="135" height="30"></a><button class="menu-btn" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button><nav id="site-nav" aria-label="Main"><a href="/">Stories</a><a href="/calendar">Calendar</a><a href="/playbooks">Playbooks</a><a href="/rules">Rules</a><a href="/price">Price</a></nav><a class="bag" href="/playbooks">Bag (<span data-bag-count>0</span>)</a></header>'''
FTR='''<footer class="cb-foot"><img src="/assets/logo/lockup-horizontal-dark.svg" alt="The Commit Book" width="180" height="40"><p class="footnav"><a href="/">Stories</a> · <a href="/playbooks">Playbooks</a> · <a href="/calendar">Calendar</a> · <a href="/rules">Rules by sport</a> · <a href="/math">Roster math</a> · <a href="/camps">Camps</a> · <a href="/compare">Compare</a> · <a href="/price">Price</a> · <a href="/about">About</a> · <a href="/legal/terms">Terms</a> · <a href="/legal/privacy">Privacy</a> · <a href="/legal/refund">Refunds</a> · <a href="/legal/auto-renewal">Auto-renewal</a></p><p>Education, not legal advice. We do not recruit or place athletes, and nobody here contacts your kid. No scholarship, offer or roster spot is promised. Stories of real athletes are built only from public sources, linked on each page; no likeness of a real person is generated. Images marked Illustration show fictional composites. Not affiliated with or endorsed by the NCAA, NAIA, NJCAA, any college, or any athlete named on this site.</p></footer>'''
def seo(path,title,desc):
  t=SEO.get(path)
  if t: t=re.sub(r'<meta charset[^>]*>|<meta name="viewport"[^>]*>','',t);return t
  return f'<title>{e(title)}</title><meta name="description" content="{e(desc)}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">'
def page(path,title,desc,body,extra_head='',scripts='',cls=''):
  return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">{seo(path,title,desc)}{HEADIN}{CSS}{extra_head}</head><body class="{cls}">{HDR}{body}{FTR}<div id="bag-status" role="status" aria-live="polite"></div><script src="/assets/stories.js"></script><script src="/assets/site.js" defer></script>{scripts}</body></html>'
def w(rel,s):
  p=os.path.join(SITE,rel);os.makedirs(os.path.dirname(p),exist_ok=True);open(p,'w').write(s)
# HOME
w('index.html',page('/','The Commit Book: real college athlete stories and the recruiting playbooks behind them','Pick an athlete. Read how they really got to a college roster, from public sources. Then get the dated playbook for your sport.',
 '<main><h1 class="vh">The Commit Book: real paths to a college roster</h1><story-ring></story-ring><story-deck></story-deck><section class="cb-band"><p class="lab">Every rule cites its bylaw</p><h2 class="d2">Then build your own calendar.</h2><p>Pick your sport and class year. See every date a coach may contact your athlete, linked to the NCAA bylaw.</p><a class="btn btn--primary" href="/calendar">Open the calendar</a> <button class="btn btn--outline" data-offer="eligibility-2-hard-deadlines">Get the Eligibility playbook, $9</button></section></main>',
 '<link rel="stylesheet" href="/assets/ring.css?v='+RV+'"><link rel="stylesheet" href="/assets/deck.css?v='+DV+'">','<script src="/assets/ring.js?v='+JV+'"></script><script src="/assets/deck.js?v='+DV+'"></script>','home'))
# STORIES
BN=['The ordinary start','What the family didn\'t know','A choice, not luck','The rule that mattered','The fit decision','What this story doesn\'t prove']
def BEATS(a):
  if not a.get('beats'):return ''
  r=a['rule']
  li=''.join(f'<li class="ev"><span class="evdate">{i+1:02d} · {BN[i]}</span>{e(x)}'+(f' <a href="{e(r["url"])}" rel="noopener">{e(r["bylaw"])}</a>' if i==3 else '')+'</li>' for i,x in enumerate(a['beats']))
  return f'<section class="st-tl st-beats"><p class="lab">The story, in seven beats (07 is the playbooks below)</p><ol class="timeline">{li}</ol></section>'
def src_list(a):
  urls=[];[urls.append(u) for u in [t['url'] for t in a['timeline']]+[m.group(0) for x in a.get('basis',[]) for m in [re.search(r"https?://[^ )]+",x)] if m] if u not in urls]
  return ''.join(f'<li><a href="{e(u)}" rel="noopener">{e(re.sub(r"^https?://(www\\.)?","",u).split("/")[0])}</a> <span class="mono">retrieved 2026-11-05</span></li>' for u in urls)
def ENV(sp):
  sp=sp.lower()
  if 'swim' in sp:return 'pool'
  if any(k in sp for k in ('basketball','volleyball','wrestling')):return 'gym'
  if 'track' in sp:return 'track'
  return 'field-dawn'
def SPW(sp):return re.split(r'[ (/&]',sp)[0].upper()
def BAND(a):
  if a['composite'] and a.get('img'):
    env=ENV(a['sport']);cut=a['img'].replace('-640','-1080')
    return f'<section class="st-band" aria-label="Illustration: {e(a["sport"])} scene"><picture class="st-band-bg"><source media="(max-width:640px)" srcset="/assets/media/env-{env}-640.webp"><img src="/assets/media/env-{env}-1080.webp" alt="" loading="lazy"></picture><img class="st-band-cut" src="{cut}" alt="Illustration of a fictional composite {e(a["sport"].lower())} athlete" loading="lazy"><span class="tag-ill st-band-tag">Illustration</span><div class="st-band-cap"><p class="st-band-word">{SPW(a["sport"])}</p><p class="lab">The playbooks for this stage</p></div></section>'
  h='hero-2' if sum(map(ord,a['id']))%2 else 'hero-3'
  return f'<section class="st-band st-band-r" aria-label="Illustration: campaign image, no real athlete depicted"><picture class="st-band-bg"><source media="(max-width:640px)" srcset="/assets/media/{h}-640.webp"><img src="/assets/media/{h}-1080.webp" alt="" loading="lazy"></picture><span class="tag-ill st-band-tag">Illustration</span><div class="st-band-cap"><p class="st-band-word">{SPW(a["sport"])}</p><p class="lab">The playbooks for this stage</p></div></section>'
def VIS(a,n):
  if a['composite']:
    env=ENV(a['sport']);cut=a['img'].replace('-640','-1080')
    cap=['The work nobody films.','The decision point.'][n-1]
    return f'<section class="beat vis vis-c" aria-label="Illustration: {e(a["sport"])} scene"><picture class="vis-bg"><source media="(max-width:640px)" srcset="/assets/media/env-{env}-640.webp"><img src="/assets/media/env-{env}-1080.webp" alt="" loading="lazy"></picture><img class="vis-cut" src="{cut}" alt="Illustration of a fictional composite {e(a["sport"].lower())} athlete" loading="lazy"><span class="tag-ill vis-tag">Illustration</span><div class="vis-cap"><p class="lab">0{n+1} / {e(a["div"])}</p><p class="vis-word">{cap}</p></div></section>'
  t=a['timeline'];f=t[min(n-1,len(t)-1)] if t else {'date':'','fact':''}
  if n==1:
    return f'<section class="beat vis vis-t" aria-label="{e(a["sport"])} at {e(a["college"])}"><p class="vis-giant" aria-hidden="true">{e(SPW(a["sport"]))}</p><div class="vis-tbody"><p class="lab">{e(a["div"])}</p><p class="vis-college">{e(a["college"])}</p><p class="vis-date">{e(f["date"])}</p><p class="vis-fact">{e(f["fact"])}</p></div></section>'
  return f'<section class="beat vis vis-v"><video src="{a["video"]}" poster="/assets/media/real-{a["id"]}-poster.jpg" muted playsinline loop preload="none" aria-label="Kinetic typography. No likeness of {e(a["name"])}."></video><div class="vis-vcap"><p class="vis-date">{e(f["date"])}</p><p class="vis-fact">{e(f["fact"])}</p><p class="note">Typography only. No image of {e(a["name"])} is shown or generated.</p></div></section>'
def HERO(a,kick):
  sw=e(SPW(a["sport"]))
  if a.get('composite') and a.get('img'):
    env=ENV(a['sport']);cut=a['img'].replace('-640','-1080')
    return f'<section class="beat b1 hx hx-c" aria-label="Illustration: {e(a["sport"])} scene"><picture class="hx-bg"><source media="(max-width:749px)" srcset="/assets/media/env-{env}-640.webp"><img src="/assets/media/env-{env}-1080.webp" alt="" fetchpriority="high"></picture><div class="hx-shade" aria-hidden="true"></div><span class="hx-shadow" aria-hidden="true"></span><img class="hx-cut" src="{cut}" alt="Illustration of a fictional composite {e(a["sport"].lower())} athlete" fetchpriority="high"><span class="tag-ill hx-tag">Illustration</span><div class="pin hx-txt"><p class="lab">{e(a["sport"])} · {e(a["div"])}</p><h1 class="hero">{e(a["short"])}</h1><p class="st-route">{e(a["from"])} <span>→</span> {e(a["college"])}</p><p class="lab st-k">{kick}</p></div></section>'
  return f'<section class="beat b1 hx hx-r"><p class="hx-word" aria-hidden="true">{sw}</p><div class="pin hx-txt"><p class="lab">Real athlete · {e(a["sport"])}</p><h1 class="hero hx-name">{e(a["name"])}</h1><p class="hx-col">{e(a["college"])} <span class="hx-div">{e(a["div"])}</span></p><p class="st-route">{e(a["from"])} <span>→</span> {e(a["college"])}</p><p class="note st-disc">Not affiliated with or endorsed by {e(a["name"])} or {e(a["college"])}. Facts from public sources.</p><p class="lab st-k">Every fact linked to a public source</p></div></section>'
for a in A:
  pb=a['playbooks'];tot=sum(P[p]['price'] for p in pb)
  if a['composite']:
    media=f'<figure class="st-fig"><span class="tag-ill">Illustration · Composite</span><img src="{a['img'].replace('-640','-1080')}" alt="Illustration of a fictional composite {e(a['sport'].lower())} athlete"></figure>'
    tl=''.join(f'<li class="ev"><span class="evdate">Basis {i+1}</span>{e(b.split(" (http")[0])} <a href="{e(re.search(r"https?://[^ )]+",b).group(0))}" rel="noopener">source</a></li>' for i,b in enumerate(a['basis']))
    kick=e(a['label'])
  else:
    media=f'<figure class="st-fig st-vid"><video src="{a["video"]}" poster="{a["poster"]}" muted playsinline loop preload="none" aria-label="Kinetic typography about {e(a["name"])}. No likeness."></video><figcaption>Typography only. No image of {e(a["name"])} is shown or generated.</figcaption></figure>'
    tl=''.join(f'<li class="ev"><span class="evdate">{e(t["date"])}</span>{e(t["fact"])} <a href="{e(t["url"])}" rel="noopener">source</a></li>' for t in a['timeline'])
    kick='Real athlete · every fact linked to a public source'
    kick+='</p><p class="note st-disc">'+e(f"Public facts only, sourced below. {a['name']} is not affiliated with, has not endorsed, and was not paid by The Commit Book. {a['college']} and the NCAA/NAIA/NJCAA are not affiliated with us.")
  body=f'''<main class="story"><div class="st-progress"></div>
{HERO(a,kick)}
<section class="beat b2"><div class="pin st-split"><div class="st-copy"><p class="lab">01 / The path</p><h2 class="d1">{e(a["path"])}</h2>{''.join(f'<p class="turn">{e(t)}</p>' for t in a["turning"])}</div><div class="st3d">{media}</div></div></section>
{VIS(a,1)}<section class="st-tl"><p class="lab">02 / What happened, in order</p><ol class="timeline">{tl}</ol></section>
{VIS(a,2)}{BEATS(a)}<section class="st-rep"><p class="lab">03 / What you can copy</p><ul>{''.join(f'<li>{e(r)}</li>' for r in a["replicate"])}</ul><p class="note">Paraphrased from the sources. No quotes are invented. Not a promise that the same path works for your athlete.</p></section>
{BAND(a)}<section class="st-end"><p class="lab">The playbooks in this story</p><h2 class="d1">The playbooks for this stage.</h2><p>These playbooks cover the rules and steps families ask about at this stage. They didn't produce this athlete's result, and they can't promise yours.</p><ul class="st-pbs">{''.join(f'<li><a href="/playbooks/{p}"><b>{e(P[p]["title"])}</b><span>${P[p]["price"]}, one-time{' · rules being verified' if P[p]['notify'] else ''}</span></a>{f'<a class="sr__add" href="/playbooks/{p}">Notify me</a>' if P[p]['notify'] else f'<button class="sr__add" data-add="{p}" aria-pressed="false">Get</button>'}</li>' for p in pb)}</ul>
<p><a class="btn btn--primary btn--l" {'data-notify' if P[pb[0]]['notify'] else 'data-checkout'}="{pb[0]}" data-offer="{pb[0]}" href="/playbooks/{pb[0]}">{'Notify me' if P[pb[0]]['notify'] else 'Get the playbook'}</a> <a class="btn btn--outline" href="/">Keep reading stories</a></p><p class="note">One-time price. No calls, no sales team, nobody contacts your kid. 30-day full refund. Checkout runs in test mode until payments go live.</p>
<details class="st-src"><summary>Sources ({len(a["timeline"]) or len(a["basis"])})</summary><ul>{src_list(a)}</ul></details></section></main>'''
  hold='<meta name="robots" content="noindex">' if a['hold'] else ''
  w(f'story/{a["id"]}/index.html',page(f'/stories/{a["id"]}/',f'{a["short"]}: {a["path"]} | The Commit Book',f'How {a["short"]} got from {a["from"]} to {a["college"]} ({a["div"]} {a["sport"]}). Sourced facts and the playbook behind it.',body,hold,'<script src="/assets/story.js" defer></script><script>addEventListener("DOMContentLoaded",function(){if(matchMedia("(prefers-reduced-motion: reduce)").matches)return;document.querySelectorAll(".vis-v video").forEach(function(v){new IntersectionObserver(function(es){es.forEach(function(x){x.isIntersecting?v.play().catch(function(){}):v.pause()})},{threshold:.3}).observe(v)})})</script>','story-page'+(' is-held' if a['hold'] else '')))
# PLAYBOOKS
def card(s,p):
  return f'<a class="pb-card" href="/playbooks/{s}"><span class="pb-thumb"><b>{e(p["title"].split(":")[0])}</b><i>{p["pages"]} pages · {e(p["format"])}</i></span><span class="lab">{e(p["who"].split(",")[0])}</span><span class="pb-t">{e(p["title"])}</span><span class="pb-s">{e(p["outcome"][:110])}{"…" if len(p["outcome"])>110 else ""}</span><span class="pb-p">${p["price"]}</span></a>'+('' if p['notify'] else f'<button class="btn btn--primary" data-offer="{s}">Get the playbook</button>')
grid=''.join('<div class="pb-cell">'+card(s,p)+('<p class="note">Rules being verified</p>' if p['notify'] else f'<button class="btn btn--primary" data-offer="{s}">Get the playbook</button>')+'</div>' for s,p in P.items())
bund=''.join(f'<li><b>{e(b["title"])}</b> <span>${b.get("price_usd",b.get("price_usd_per_year"))}{"/yr" if "price_usd_per_year" in b else ""}</span></li>' for b in D['bundles'])
w('playbooks/index.html',page('/playbooks/','Recruiting playbooks by sport and path | The Commit Book','Dated, sourced recruiting playbooks: football, baseball, track, walk-on, JUCO, D3, offers and signing. One-time prices.',
 f'<main class="cb-page"><p class="lab">Playbooks</p><h1 class="d1">Run recruiting yourself. With the rules in hand.</h1><p class="lede">Playbooks for the athlete to run, with parents in support. Every rule cites its bylaw.</p><div class="pb-grid">{grid}</div><section class="pb-bund"><h2 class="d2">Bundles</h2><ul>{bund}</ul><p class="note">Prices proposed for launch. Checkout runs in test mode until payments go live. 30-day full refund.</p></section></main>'))
def NOTIFY(s): return f'<p class="note">Some rules in this playbook are still being verified against the manual. Leave your email and we will tell you when it is ready.</p><form class="capture" data-src="notify-{s}" novalidate><input type="email" name="email" required placeholder="Your email" aria-label="Your email" autocomplete="email"><input type="hidden" name="plan" value="giveaway"><input type="hidden" name="source" value="notify-{s}"><input class="hp" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true"><button class="btn btn--primary" type="submit">Notify me</button><label class="consent"><input type="checkbox" name="consent" value="1"> Email me when this playbook is ready. Unsubscribe any time.</label></form><p class="note f5">For parents and guardians. We do not knowingly collect information from children under 13.</p>'
for s,p in P.items():
  stories=[a for a in A if s in a['playbooks'] and not a['hold']]
  body=f'''<main class="cb-page pdp"><div class="pdp-g"><div class="pdp-img"><span class="pb-thumb big"><b>{e(p["title"])}</b><i>{p["pages"]} pages · {e(p["format"])}</i></span></div><div class="pdp-info"><p class="lab">Playbook</p><h1 class="d2">{e(p["title"])}</h1><p class="pb-p">${p["price"]} <span class="note">one-time</span></p><p>{e(p["outcome"])}</p><p class="note">For: {e(p["who"])}</p>
{NOTIFY(s) if p['notify'] else f'<button class="btn btn--primary btn--l" data-checkout="{s}" data-offer="{s}">Get the playbook</button> <button class="btn btn--outline sr__add" data-add="{s}" aria-pressed="false">Get</button>'}
<p class="note">No calls, no sales team. 30-day full refund. Checkout runs in test mode until payments go live; if this playbook's file is not ready, checkout says so and you can leave your email instead.</p>
<details open><summary>What's inside</summary><ol>{''.join(f"<li>{e(t)}</li>" for t in p["toc"])}</ol>{'<p class="note">D3 aid rules: <a href="https://web3.ncaa.org/lsdbi/reports/getReport/90011" rel="noopener">NCAA Division III Manual, Bylaw 15</a></p>' if s=="d3-academic-aid-first" else ""}</details><details><summary>Tools included</summary><ul>{''.join(f"<li>{e(t)}</li>" for t in p["tools"])}</ul></details>
{f'<details><summary>Stories that use it</summary><ul>{"".join(f"<li><a href=/story/{a['id']}>{e(a['short'])}</a> · {e(a['sport'])} · {e(a['div'])}</li>" for a in stories)}</ul></details>' if stories else ''}</div></div></main>'''
  w(f'playbooks/{s}/index.html',page(f'/playbooks/{s}/',f'{p["title"]} | The Commit Book',p['outcome'],body))
# RESKIN v2 pages
for f in glob.glob(SITE+'/**/index.html',recursive=True):
  rel=os.path.relpath(f,SITE)
  if rel=='index.html' or rel.startswith(('story/','playbooks/')):continue
  s=open(f).read()
  s=re.sub(r'<header class="masthead">.*?</header>',HDR,s,flags=re.S)
  s=re.sub(r'<header class="site-header cb-header">.*?</header>',HDR,s,flags=re.S)
  s=re.sub(r'<footer class="(foot|cb-foot)">.*?</footer>',FTR,s,flags=re.S)
  s=re.sub(r'<link rel="icon".*?<meta name="theme-color" content="#ffffff">','',s,flags=re.S)
  s=re.sub(r'<script src="/checkout.js[^"]*" defer></script><link rel="stylesheet" href="/assets/tokens.css"><link rel="stylesheet" href="/assets/commit.css[^"]*">','',s)
  s=s.replace('<link rel="stylesheet" href="/style.css">','<link rel="stylesheet" href="/style.css">'+HEADIN+CSS)
  s=s.replace('<link rel="stylesheet" href="/assets/commit.css">','')
  s=s.replace(' class="intro-pending"','')
  if rel=='price/index.html' and 'pr-hero' not in s:
    s=s.replace('<body','<body data-page="price"',1)
    s=re.sub(r'(<div class="tiers")',r'<figure class="pr-hero" aria-hidden="true"><img src="/assets/media/env-gym-1080.webp" alt="" class="pr-bg"><img src="/assets/media/cut-volleyball-1080.webp" alt="" class="pr-fig" loading="eager"><span class="tag-ill">Illustration</span><figcaption>Less than one showcase. Every date cited to its bylaw.</figcaption></figure>\1',s,count=1)

  if '/assets/site.js' not in s: s=s.replace('</body>','<script src="/assets/stories.js"></script><script src="/assets/site.js" defer></script></body>')
  s=re.sub(r'(<form class="capture".*?</form>)(?!<p class="note f5">)',r'\1<p class="note f5">For parents and guardians. We do not knowingly collect information from children under 13.</p>',s,flags=re.S)
  s=s.replace('your receipt email says how to cancel online in one click.','manage or cancel your trial any time from the billing link on this page.')
  open(f,'w').write(s)
REP=[('<s>$149</s>',''),('leave your email and we will send the founding-member link','leave your email to hear when founding membership opens'),('Most families can run recruiting themselves','You can run recruiting without a paid service. Plenty of families do'),('Most families can run recruiting on their own','You can run recruiting without a paid service. Plenty of families do'),
 ('what each one costs if you miss it','what happens if you wait'),('what it costs to miss it','what happens if you wait'),
 ('Cancel any time by email or from your account; cancelling stops the next renewal','Cancel online any time from your billing page. Cancelling stops the next renewal'),
 ('Cancel any time online in one click','Cancel online any time from your billing page.'[:-1]),('Trial members: manage or cancel your trial any time from the billing link on this page','Trial members: cancel online any time from your billing page, linked below'),
 ('We email you 7 days before the trial ends',"We'll show your renewal date in your account and billing page"),('Members get an email 30 and 7 days before each date','Members get alerts 30 and 7 days before each date once email sending goes live'),('Email alerts 30 and 7 days before each date','Alerts 30 and 7 days before each date (email starts when sending goes live)'),('Online, in one click, any time','Online, any time, from your billing page'),('We email you before each renewal',"We'll show your renewal date in your account and billing page")]
AR="Paid memberships start with a 14-day free trial, then renew automatically every year at the price shown at checkout until you cancel. We'll show your renewal date in your account and billing page. Cancel online any time from your billing page; cancelling stops the next charge. You can get a full refund within 30 days of any charge, including a renewal."
PR="We collect your email, the sport, class year and plan you choose, and whether you agreed to email. We store it with our email provider (Resend) and, if you buy, Stripe processes your payment; we never see your card number. Our host (Vercel) keeps standard server logs. We do not collect athlete names, film, stats or photos, and we do not sell or share personal data. Ask us to see or delete your data by email and we will."
for f in glob.glob(SITE+'/**/index.html',recursive=True):
  s=open(f).read();o=s
  for a_,b_ in REP: s=s.replace(a_,b_)
  if f.endswith('legal/auto-renewal/index.html'): s=re.sub(r'Paid memberships renew automatically.*?refundable on request\.',AR,s,flags=re.S)
  if f.endswith('legal/privacy/index.html'): s=re.sub(r'We collect your email and the sport.*?by email and we will\.',PR,s,flags=re.S)
  if f.endswith('legal/refund/index.html') and 'every renewal' not in s: s=s.replace('No questions and no retention call.','No questions and no retention call. This covers the first purchase and every renewal.')
  if s!=o: open(f,'w').write(s)
print('ok',len(A),len(P))
