import json,urllib.request,time
B='http://127.0.0.1:4912'
def post(p,b):
  for i in range(3):
    try:
      r=urllib.request.urlopen(urllib.request.Request(B+p,json.dumps(b).encode(),{'Content-Type':'application/json'}),timeout=15);return json.load(r)
    except Exception as e: time.sleep(1); err=e
  raise err
offers=json.load(open('../00-mm3-offers.json'))
def board(title,lanes,edges):
  cv=post('/api/canvases',{'title':title})['id']; ids={}
  for c,(lane,cards) in enumerate(lanes):
    x=c*380
    post('/api/nodes/add',{'canvas':cv,'kind':'note','data':{'title':'LANE: '+lane,'text':lane},'x':x,'y':0,'w':340})
    for r,(k,t,txt) in enumerate(cards):
      n=post('/api/nodes/add',{'canvas':cv,'kind':'note','data':{'title':t,'text':txt},'x':x,'y':120+r*190,'w':340})['node']
      ids[k]=n['id']
  ne=0
  for a,b,l in edges:
    if a in ids and b in ids: post('/api/edges/add',{'canvas':cv,'from':ids[a],'to':ids[b],'label':l}); ne+=1
  return cv,ne
olist='\n'.join('- '+o['name'] for o in offers)
A=[('Assets',[
 ('mm3','30 MM3 offers (research/00-mm3-offers.json)',olist),
 ('site','mm3sports.com: 160 articles + 402-term glossary','SEO surface + topical authority; source for lead magnets and copilot grounding.'),
 ('crm','Coach CRM','Coach contacts; seeds Coach/Club B2B and warm intros. Read-only until Mike approves outreach.'),
 ('census','D1 census','Program/roster census; powers roster & aid math and division pages.'),
 ('rules','Rule dataset (site/data.js)','Sourced, dated NCAA rules by sport x class year, each date cites its bylaw. The moat.')]),
 ('Offerings',[
 ('free','Free','Calendar for one sport/class year + email capture.'),
 ('side','Sideline $149/yr ($99 founding, first 100)','Alerts, tracker, roster/aid math. Proposed, not approved to publish.'),
 ('path','Pathway $499/yr','Sideline + camp triage, multi-sport, deeper tools.'),
 ('audit','Recruiting Audit $1,500','One-time sourced plan; no scholarship promise.'),
 ('coach','Coach/Club $299/yr','Team licence for HS coaches/clubs.')]),
 ('Acquisition workflows',[
 ('lm','Lead magnet','Free calendar PDF / checklist from MM3 offers.'),
 ('email','Email nurture','Dated rule alerts as nurture; no fake urgency.'),
 ('trial','Trial','30-day refund framing; no sales call.'),
 ('renew','Auto-renew','Annual renew timed to next class-year window.'),
 ('comm','Community answers','Cite-the-bylaw answers in parent forums (drafts only until approved).'),
 ('hudl','Hudl school sponsorship','School-level sponsored seats.'),
 ('b2b','Coach/club B2B','Coach CRM -> Coach/Club tier -> parent seats.')]),
 ('Delivery workflows',[
 ('refresh','Rule-refresh pipeline','NCAA bylaw diffs -> data.js update -> dated changelog.'),
 ('alerts','Alerts by class year','Contact/visit/signing windows pushed per class year.'),
 ('tracker','Hosted recruiting tracker','Contacts, visits, offers; evolves MM3 tracker spreadsheet.')]),
 ('Data / engines',[
 ('ruledb','Rule DB engine','data.js -> structured, versioned, cited rules.'),
 ('aid','Roster/aid math engine','Census x rules -> realistic odds/aid ranges (estimates labeled).'),
 ('camp','Camp triage engine','Scores camps vs. target programs.'),
 ('seo','Page generator','Glossary + articles + rules -> landing pages.')])]
E=[('rules','ruledb','structured'),('ruledb','refresh','versioned by'),('refresh','alerts','feeds'),('census','aid','input'),('ruledb','aid','input'),
 ('aid','side','powers'),('alerts','side','core value'),('tracker','side','included'),('camp','path','powers'),('mm3','lm','source'),('site','seo','content'),
 ('seo','lm','traffic to'),('lm','email','capture'),('email','trial','converts'),('trial','side','to paid'),('side','renew','annual'),('side','path','upsell'),
 ('path','audit','upsell'),('comm','free','traffic'),('crm','b2b','seeds'),('b2b','coach','sells'),('hudl','coach','sponsored'),('coach','free','parent seats'),
 ('free','email','list'),('mm3','tracker','template'),('ruledb','free','powers')]
cv1,e1=board('Recruiting Calendar — System Map',A,E)
def idea(t,lever,why,proof,kill,v): return (t,f'[{v}] {t}',f'Lever: {lever}\nCompounds: {why}\nFirst proof: {proof}\nKill: {kill}')
X=[('Assets 1000x',[
 idea('pages','Programmatic pages: sport x class year x division','Each rule refresh updates thousands of pages; long-tail parent queries','Generate 50 pages for 1 sport; index + impressions in 30 days','<100 GSC impressions/page avg after 60 days','HIGH'),
 idea('state','State-association rules layer','Nobody joins NCAA + state rules; 50x data moat','Encode 1 state (CO) for football; ask 10 parents if it matters','No paid upgrade/retention lift in test cohort','HIGH'),
 idea('glossary','Glossary syndication (402 terms) as embeddable widget','Backlinks from every school site that embeds it','Ship widget, offer to 5 boosters (drafts, Mike approves)','<2 embeds in 60 days','MEDIUM')]),
 ('Offerings 1000x',[
 idea('copilot','AI recruiting copilot grounded in rule DB','Every answer cites a bylaw; usage data improves DB','Internal copilot answering 50 real parent questions, judged vs bylaws','>2% uncited/wrong answers or no conversion lift','HIGH'),
 idea('coachside','Coach-side product (compliance calendar for HS coaches)','One coach brings a roster of parents','5 coach interviews from CRM (approved drafts)','<2 of 5 would pay $299','HIGH'),
 idea('whitelabel','Club white-label','Clubs resell to every family; low CAC','1 club pilot, free, measure parent activation','<30% parent activation','MEDIUM'),
 idea('allsports','Every NCAA sport','TAM x10 but each sport needs sourced rules','Add 1 sport (basketball, MM3 strength)','Refresh cost > revenue per sport','MEDIUM')]),
 ('Acquisition 1000x',[
 idea('camps','Camp affiliate','Camp triage engine turns into referral revenue','List 20 camps with affiliate terms; check conflict-of-interest disclosure','Disclosure hurts trust or <$1k/yr','MEDIUM - trust risk'),
 idea('hudlx','Hudl/school sponsorship at scale','One deal = thousands of seats','1 school sponsorship LOI draft','No sponsor after 10 asks','HIGH if lands'),
 idea('viral','Viral social clips / influencer push','Reach, not compounding','-','-','VANITY'),
 idea('ads','Paid ads before LTV known','Burns cash, no moat','-','-','VANITY')]),
 ('Delivery 1000x',[
 idea('autorefresh','Automated bylaw diff + human verify','Freshness is the product; cost per refresh -> ~0','Diff last 2 NCAA manuals automatically','Misses >1 change a human finds','HIGH'),
 idea('calendarsync','Calendar (ics) sync per class year','Lives on the family calendar = retention','Ship ics for 1 class year','<20% of members subscribe','HIGH')]),
 ('Data 1000x',[
 idea('licensing','Data licensing (rule DB API)','Sell the same DB to apps, Hudl, clubs','2 API conversations from coach CRM','No LOI after 5 talks','MEDIUM - later'),
 idea('benchmarks','Aggregate outcome benchmarks','Network data only we have','Needs members first','Privacy risk with minors -> aggregate only','LATER'),
 idea('dashboards','Fancy dashboards / app store app now','Looks big, adds no data','-','-','VANITY')])]
XE=[('pages','copilot','grounds'),('autorefresh','pages','keeps fresh'),('state','pages','x50 pages'),('coachside','whitelabel','evolves'),('copilot','licensing','same DB'),('autorefresh','licensing','enables'),('hudlx','coachside','channel'),('camps','copilot','recommendations')]
cv2,e2=board('Recruiting Calendar — 1000x',X,XE)
json.dump({'map':cv1,'x1000':cv2,'edges':[e1,e2]},open('ids.json','w'))
for cv in (cv1,cv2):
  s=json.load(urllib.request.urlopen(f'{B}/api/state?canvas={cv}'));print(cv,s.get('title'),len(s['nodes']),len(s.get('edges',[])))
