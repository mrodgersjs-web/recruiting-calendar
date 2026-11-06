import json,re,os,html
R=os.path.dirname(os.path.abspath(__file__));ROOT=os.path.join(R,'..','..')
BASE='https://recruiting-calendar.vercel.app';BRAND='The Commit Book';CHK='2026-11-05'
d=json.loads(re.sub(r'^window\.RC_DATA=|;\s*$','',open(ROOT+'/site/data.js').read().strip()))
cat=json.load(open(ROOT+'/v3/W1-playbooks/CATALOG.json'))['catalog']
st=json.load(open(ROOT+'/v3/W1-stories/STORIES.json'))['stories']
pb={p['slug']:p for p in cat}
def row(sport,pred):
  for r in d[sport]['deadlines']:
    if pred(r): return r
  raise SystemExit('missing '+sport)
E=html.escape
# ---------- answer pages: every fact pulled from data.js rows ----------
A=[
('when-can-college-coaches-contact-my-kid','When can college coaches contact my kid?',
 'Most D1 sports: June 15 after sophomore year. D1 baseball: August 1 of junior year. D2: calls any time, in-person June 15.',
 [('football',lambda r:r['event'].startswith('D1 football coaches may start')),('baseball',lambda r:r['event'].startswith('D1 baseball coaches may start')),('track',lambda r:r['event'].startswith('Calls, messages')),('baseball',lambda r:r['event'].startswith('Division II'))],'football-junior-year'),
('when-does-d1-baseball-recruiting-start','When does D1 baseball recruiting start?',
 'D1 baseball coaches may start calling, texting and emailing August 1 of junior year; off-campus contact and visits open September 1.',
 [('baseball',lambda r:r['event'].startswith('D1 baseball coaches')),('baseball',lambda r:r['event'].startswith('D1 baseball off-campus'))],'baseball-showcase-to-signing'),
('when-can-track-coaches-contact-athletes','When can track and cross country coaches contact athletes?',
 'June 15 after sophomore year for calls, messages and off-campus contact (changed October 7, 2026). Visits open August 1 of junior year.',
 [('track',lambda r:r['event'].startswith('Calls, messages')),('track',lambda r:r['event'].startswith('Official and unofficial'))],'track-field-marks'),
('when-are-official-visits-allowed','When are NCAA official visits allowed?',
 'It depends on sport and division: D1 football April 1 of junior year, D1 track August 1, D1 baseball September 1, D3 January 1 of junior year.',
 [('football',lambda r:r['event'].startswith('Junior-year official')),('track',lambda r:r['event'].startswith('Official and unofficial')),('baseball',lambda r:r['event'].startswith('D1 baseball off-campus')),('baseball',lambda r:r['event'].startswith('Division III'))],'football-junior-year'),
('ncaa-10-7-core-course-rule','What is the NCAA 10/7 core course rule?',
 'D1 requires 10 of 16 core courses, 7 of them English, math or science, finished before the seventh semester. Those grades lock.',
 [('football',lambda r:r['event'].startswith('Finish 10'))],'eligibility-2-hard-deadlines'),
('ncaa-d1-minimum-core-gpa','What GPA does my kid need for NCAA Division I?',
 'At least a 2.3 core-course GPA across all 16 NCAA core courses. A transcript GPA is not the same as a core GPA.',
 [('football',lambda r:r['event'].startswith('Graduate'))],'eligibility-2-hard-deadlines'),
('ncaa-eligibility-center-account-cost','Does my kid need an NCAA Eligibility Center account, and what does it cost?',
 'D1 and D2 recruits need a certification account ($110 domestic, fee waivers possible) before any D1 official visit. The free Profile Page is not enough.',
 [('football',lambda r:r['event'].startswith('Open the NCAA'))],'eligibility-2-hard-deadlines'),
('when-can-a-scholarship-offer-be-made','When can a college make a written scholarship offer?',
 'D1 football: not before November 15 of senior year (rule adopted October 2025). D1 track: not before August 1 of senior year. Verbal offers are not binding.',
 [('football',lambda r:r['event'].startswith('Written')),('track',lambda r:r['event'].startswith('Written'))],'offer-and-signing'),
('when-is-signing-day-class-of-2029','When is signing day for the Class of 2029?',
 'Projected from current rules: D1 football early period Nov 29 to Dec 1, 2028 and regular date Feb 7, 2029; D1 baseball and track open Nov 8, 2028. Not yet published by the NCAA.',
 [('football',lambda r:r['event'].startswith('Projected early')),('football',lambda r:r['event'].startswith('Projected regular')),('baseball',lambda r:r['event'].startswith('Projected D1 baseball')),('track',lambda r:r['event'].startswith('Projected signing'))],'offer-and-signing'),
('does-d3-offer-athletic-scholarships','Does Division III offer athletic scholarships?',
 'No. D3 offers no athletic scholarships; aid is academic and need-based. D3 official visits open January 1 of junior year.',
 [('baseball',lambda r:r['event'].startswith('Division III'))],'d3-academic-aid-first'),
]
DEMAND={'when-can-college-coaches-contact-my-kid':'#21, #8','when-does-d1-baseball-recruiting-start':'#8','when-can-track-coaches-contact-athletes':'#8, #21','when-are-official-visits-allowed':'#21','ncaa-10-7-core-course-rule':'#16','ncaa-d1-minimum-core-gpa':'#16','ncaa-eligibility-center-account-cost':'#19','when-can-a-scholarship-offer-be-made':'#5','when-is-signing-day-class-of-2029':'#8','does-d3-offer-athletic-scholarships':'#5, #15'}
SL={'football':'Football','baseball':'Baseball','track':'Track & XC'}
def ld(o): return '<script type="application/ld+json">'+json.dumps(o,ensure_ascii=False)+'</script>'
ORG={"@context":"https://schema.org","@type":"Organization","@id":BASE+"/#org","name":BRAND,"url":BASE+"/","logo":BASE+"/logo.png","description":"Dated NCAA recruiting calendars and playbooks for parents, every calendar date cited to its NCAA bylaw."}
def head(title,desc,path,typ='website',img='/og/default.png'):
  u=BASE+path
  return f'''<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><link rel="canonical" href="{u}">
<meta property="og:type" content="{typ}"><meta property="og:site_name" content="{BRAND}"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{u}"><meta property="og:image" content="{BASE}{img}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(title)}"><meta name="twitter:description" content="{E(desc)}"><meta name="twitter:image" content="{BASE}{img}">'''
os.makedirs(R+'/site/answers',exist_ok=True)
idx=[];audit=[]
for slug,q,short,rows,pslug in A:
  rs=[(s,row(s,p)) for s,p in rows]
  p=pb[pslug];path=f'/answers/{slug}/'
  faq={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":short+" Source: NCAA bylaws as listed, checked "+CHK+"."}}]}
  art={"@context":"https://schema.org","@type":"Article","headline":q,"dateModified":CHK,"author":{"@id":BASE+"/#org"},"publisher":{"@id":BASE+"/#org"},"mainEntityOfPage":BASE+path,"citation":sorted({r['citation_url'] for _,r in rs})}
  lis=''
  for s,r in rs:
    dt=r['iso_date'] or 'School-set date'
    proj=' (projected)' if r['kind']=='projected' else ''
    lis+=f'<li><strong>{SL[s]}, Class of {d[s]["class_year"]}: {E(r["event"])}</strong><br>Date: {dt}{proj}<br>{E(r["plain_english"])}<br>Rule: <a href="{r["citation_url"]}" rel="nofollow">{E(r["rule"])}</a> · {E(d[s]["source_label"])} · checked {d[s]["verified_on"]}</li>\n'
    audit.append(f'{slug}\t{s}\t{r["rule"]}\t{dt}\t{r["citation_url"]}')
  title=q+' | '+BRAND; desc=short[:155]
  page=f'''<!doctype html><html lang="en"><head>{head(title,desc,path,'article')}
<link rel="stylesheet" href="/style.css">{ld(ORG)}{ld(faq)}{ld(art)}</head><body><main class="answer">
<p class="eyebrow"><a href="/answers/">Parent answers</a></p><h1>{E(q)}</h1>
<p class="lede"><strong>The short answer:</strong> {E(short)}</p>
<h2>The rule, the date, the bylaw</h2><ul class="rules">{lis}</ul>
<p class="checked">Rules checked {CHK} against the {E(d['football']['source_label'])}. NCAA rules change; follow the bylaw link for the current text. Projected dates are calculated from current rules and are not published NCAA dates.</p>
<aside class="cta"><h2>Turn this into a plan</h2><p>{E(p['title'])}: {E(p['outcome'])}.</p><a class="btn" href="/playbooks/{pslug}/">Get the playbook · ${p['price_usd']}</a> <a href="/rules/">See the full dated calendar</a></aside>
</main></body></html>'''
  os.makedirs(R+'/site'+path,exist_ok=True);open(R+'/site'+path+'index.html','w').write(page)
  idx.append((path,q,short,pslug))
il=''.join(f'<li><a href="{p}">{E(q)}</a><br>{E(s)}</li>' for p,q,s,_ in idx)
open(R+'/site/answers/index.html','w').write(f'<!doctype html><html lang="en"><head>{head("Parent answers: NCAA recruiting rules, dates and bylaws | "+BRAND,"Plain answers to the recruiting questions parents ask most, each with the rule, the date, the NCAA bylaw and the day we checked it.","/answers/")}<link rel="stylesheet" href="/style.css">{ld(ORG)}</head><body><main class="answer"><h1>Parent answers</h1><ul>{il}</ul></main></body></html>')
# ---------- head tags for existing + v3 pages ----------
P=[('/','The Commit Book: real college athlete stories and the recruiting playbooks behind them','Real college athlete paths, then the dated NCAA plan for your kid: contact openings, visits, offers and signing, each rule cited to its bylaw.'),
('/rules/','NCAA recruiting rules by sport and class year | '+BRAND,'Football, baseball and track & field recruiting dates for Classes of 2027-2030, with the D1, D2 and D3 bylaw behind every date.'),
('/camps/','Camp and showcase triage: what is worth paying for | '+BRAND,'Score a camp or showcase before you pay, and know when recruiting conversations at camps are allowed under NCAA rules.'),
('/coaches/','For high school and club coaches | '+BRAND,'A cited, dated recruiting calendar you can hand to every family on your roster.'),
('/compare/','Compare recruiting services honestly | '+BRAND,'What NCSA-style services charge versus what you can do yourself, so you know what you are paying for.'),
('/free/','Free Class of 2029 recruiting calendar (PDF) | '+BRAND,'Download the free dated NCAA recruiting calendar for the Class of 2029, every row cited to its bylaw.'),
('/math/','Roster and scholarship aid math | '+BRAND,'How roster limits and scholarship equivalency work, explained with the rules behind them.'),
('/price/','Playbook prices | '+BRAND,'One-time playbook prices for families. No subscriptions sold by phone, no access promises.'),
('/about/','About | '+BRAND,'Who builds The Commit Book and how every rule is checked against the NCAA manual.'),
('/playbooks/','Recruiting playbooks for parents | '+BRAND,'Dated, cited recruiting playbooks by sport and path: D1, D2, D3, JUCO, walk-on and late bloomer.'),
('/stories/','How real athletes got recruited | '+BRAND,'Sourced recruiting paths of adult college athletes across D1, D2, D3, NAIA and JUCO, each mapped to a playbook.'),
('/answers/','Parent answers: NCAA recruiting rules and dates | '+BRAND,'Plain answers to the recruiting questions parents ask most.')]
for s in d:
  for y in (2027,2028,2029,2030): P.append((f'/rules/{s}/{y}/',f'{SL[s]} recruiting calendar, Class of {y} | {BRAND}',f'Every NCAA {SL[s].lower()} recruiting date for the Class of {y}: contact, visits, offers and signing, each with its bylaw.'))
for p in cat: P.append((f'/playbooks/{p["slug"]}/',f'{p["title"]} | {BRAND}',(p['outcome']+'.')[:155]))
for x in st:
  nm=x['name'];comp=x.get('composite')
  dest=x.get('college') or x.get('destination') or x['division']
  t=f'{nm}: {x["sport"]}, {x["division"]}' if comp else f'How {nm} got to {dest} ({x["sport"]}, {x["division"]})'
  P.append((f'/stories/{x["id"]}/',t+' | '+BRAND,('A composite story built from sourced recruiting paths. Illustration.' if comp else f'The sourced recruiting path of {nm}, {x["sport"]}, {x["division"]}, with the playbook it maps to.')))
for path,q,s,_ in idx: P.append((path,q+' | '+BRAND,s[:155]))
heads={pth:head(t,ds,pth,'article' if pth.startswith(('/stories/','/answers/')) and pth.count('/')>3 else ('product' if pth.startswith('/playbooks/') and pth!='/playbooks/' else 'website')) for pth,t,ds in P}
json.dump(heads,open(R+'/head-tags.json','w'),indent=1)
open(R+'/META.md','w').write('# Titles and meta descriptions (W2-seo, '+CHK+')\n\n| Path | Title | Description | len |\n|---|---|---|---|\n'+''.join(f'| {p} | {t} | {ds} | {len(ds)} |\n' for p,t,ds in P))
# ---------- JSON-LD ----------
os.makedirs(R+'/jsonld',exist_ok=True)
json.dump(ORG,open(R+'/jsonld/organization.json','w'),indent=1)
prods={p['slug']:{"@context":"https://schema.org","@type":"Product","name":p['title'],"description":p['outcome'],"brand":{"@id":BASE+"/#org"},"url":f"{BASE}/playbooks/{p['slug']}/","category":"Digital download ("+p['format']+")","offers":{"@type":"Offer","price":str(p['price_usd']),"priceCurrency":"USD","availability":"https://schema.org/InStock" if p['status']=='WRITTEN' else "https://schema.org/PreOrder","url":f"{BASE}/playbooks/{p['slug']}/"}} for p in cat}
json.dump(prods,open(R+'/jsonld/products.json','w'),indent=1)
arts={}
for x in st:
  src=sorted({t['url'] for t in x.get('timeline',[]) if t.get('url')})
  arts[x['id']]={"@context":"https://schema.org","@type":"Article","headline":heads and [t for p,t,_ in P if p==f'/stories/{x["id"]}/'][0].split(' | ')[0],"dateModified":CHK,"author":{"@id":BASE+"/#org"},"publisher":{"@id":BASE+"/#org"},"mainEntityOfPage":f"{BASE}/stories/{x['id']}/","citation":src,**({"about":{"@type":"Person","name":x['name']}} if not x.get('composite') else {"genre":"Composite story (illustration)"})}
json.dump(arts,open(R+'/jsonld/stories-articles.json','w'),indent=1)
json.dump({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":s}} for _,q,s,_ in idx]},open(R+'/jsonld/faqpage-answers-hub.json','w'),indent=1)
# ---------- sitemap / robots ----------
sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{BASE}{p}</loc><lastmod>{CHK}</lastmod></url>\n' for p,_,_ in P)+'<url><loc>'+BASE+'/start/</loc><lastmod>2026-11-06</lastmod></url>\n'+'<url><loc>'+BASE+'/downloads/recruiting-calendar-class-2029.pdf</loc><lastmod>'+CHK+'</lastmod></url>\n</urlset>\n'
open(R+'/site/sitemap.xml','w').write(sm)
open(R+'/site/robots.txt','w').write(f'User-agent: *\nAllow: /\nDisallow: /welcome/\nDisallow: /api/\n\nSitemap: {BASE}/sitemap.xml\n')
open(R+'/ANSWER-SOURCES.tsv','w').write('page\tsport\trule\tdate\turl\n'+'\n'.join(audit)+'\n')
print(len(P),'pages;',len(idx),'answers;',len(prods),'products;',len(arts),'stories;',len(audit),'cited rows')
