import json,os,html
R=os.path.expanduser('~/Developer/recruiting-calendar')
S=json.load(open(R+'/v3/W1-stories/STORIES.json'))['stories']
C=json.load(open(R+'/v3/W1-playbooks/CATALOG.json'))
# Flag resolution (W2-scripts FLAG-RESOLUTION.md): corrections applied; held stories behind flag.
FIX={
 'white':{'tl':{1:{'date':'2012','fact':'His one offer was a D2 preferred walk-on at UCCS with a $3,000 partial scholarship; the other option was a junior college in Wyoming','url':'https://andscape.com/features/derrick-white-started-as-the-ultimate-underdog-in-his-journey-to-the-nba-finals/'}}},
 'pichardo':{'tl':{1:{'date':'2022 fall','fact':'Had several college options but chose Brown with no guarantee; went through walk-on tryouts','url':'https://www.nancybkennedy.com/a-walk-on-wonder'}}},
 'rodriguez':{'hs':'Buchanan High School, Clovis, CA','add':[{'date':'NAIA rule','fact':'NAIA: register with the NAIA Eligibility Center (PlayNAIA.org). A 2.3 high school GPA makes a freshman eligible, or two of three: ACT 18/SAT 970, 2.0 GPA, top half of class. NAIA contact rules are far looser than NCAA. (NAIA Bylaws Art. V Sec. C, 2026-27 NAIA Handbook p.70)','url':'https://www.naia.org/legislative/2026-27/NAIA_Handbook.pdf'}]},
 'marpet':{'hs':'Hastings High School, Hastings-on-Hudson, NY','add':[{'date':'HS','fact':'FCS interest (Fordham, Marist, Holy Cross) was walk-on only, no scholarship','url':'https://www.buccaneers.com/news/5-things-to-know-about-ali-marpet-15227691'}]},
 'lowe':{'hs':'La Costa Canyon HS, Carlsbad, CA','add':[{'date':'college','fact':'Came as a walk-on; coach later awarded a scholarship','url':'https://www.espn.com/espnw/news-commentary/article/11930309/ucla-karsta-lowe-blossoming-fiery-new-attitude'}]},
 'pirosko':{'add':[{'date':'2018-05','fact':'Signed National Letter of Intent with Gannon in the spring 2018 signing period','url':'https://gannonsports.com/story.aspx?file_date=5-2-2018&filename=gannon-womens-basketball-program-adds-pair-to-recruiting-class'}]},
 'coward':{'college':'Willamette (D3) then Eastern Washington and Washington State','timeline':[
  {'date':'out of HS','fact':'Chose Willamette (D3) as the best fit out of high school','url':'https://www.spokesman.com/stories/2022/dec/19/eastern-washingtons-cedric-coward-carving-out-impo'},
  {'date':'2021-22','fact':'Averaged 19.5 points and 12.0 rebounds at Willamette','url':'https://www.nba.com/draft/2025/prospects/cedric-coward'},
  {'date':'2022-25','fact':'Transferred to Eastern Washington (D1), then Washington State','url':'https://wsucougars.com/sports/mens-basketball/roster/player/cedric-coward'},
  {'date':'2025','fact':'Picked 11th in the 2025 NBA Draft','url':'https://www.nba.com/draft/2025/prospects/cedric-coward'}]},
}
HOLD={'rodenfels'}   # single-source path; behind ?flags=all until second source
SOCCER={'id':'wondolowski','name':'Chris Wondolowski','sport':'Soccer','hs':'De La Salle HS, Danville, CA','college':'Chico State','division':'D2','path':'D1 interest was mostly for track; found at a tournament',
 'timeline':[{'date':'HS','fact':'Not heavily recruited for soccer; D1 interest was mostly for track','url':'https://www.ncaa.com/news/soccer-men/article/2019-08-29/how-chris-wondolowski-went-dii-mls-record-book'},
  {'date':'HS','fact':'Chico State coach saw him at a San Diego tournament','url':'https://www.ncaa.com/news/soccer-men/article/2019-08-29/how-chris-wondolowski-went-dii-mls-record-book'},
  {'date':'college','fact':'Scored 39 goals at Chico State and was named All-American','url':'https://www.ncaa.com/news/soccer-men/article/2019-08-29/how-chris-wondolowski-went-dii-mls-record-book'},
  {'date':'2005','fact':'Taken 41st in the MLS Supplemental Draft','url':'https://www.ncaa.com/news/soccer-men/article/2019-08-29/how-chris-wondolowski-went-dii-mls-record-book'}],
 'turning':['A tournament put him in front of the right coach'],'replicate':['Play the events lower-division coaches attend','Treat D2 as a real path to the pros']}
PB={p['slug']:p for p in C['catalog']}
MAP={'Football':['football-junior-year','walk-on','offer-and-signing'],'Baseball':['baseball-showcase-to-signing','walk-on','camp-roi'],
 'Track/XC':['track-field-marks','late-bloomer','d3-academic-aid-first'],'Basketball':['highlight-reel-social','offer-and-signing','eligibility-2-hard-deadlines'],
 'Volleyball':['walk-on','highlight-reel-social','offer-and-signing'],'Softball':['camp-roi','highlight-reel-social','eligibility-2-hard-deadlines'],
 'Wrestling':['late-bloomer','juco-to-d1','eligibility-2-hard-deadlines'],'Soccer':['camp-roi','highlight-reel-social','offer-and-signing'],
 'Swimming':['highlight-reel-social','d3-academic-aid-first','eligibility-2-hard-deadlines']}
def pbs(x):
  b=list(MAP.get(x['sport'],MAP['Basketball'])) if 'Lacrosse' not in x['sport'] else ['late-bloomer','d3-academic-aid-first','eligibility-2-hard-deadlines']
  d=x['division']
  if 'JUCO' in d: b[1]='juco-to-d1'
  if d.startswith('D3') and 'd3-academic-aid-first' not in b: b[1]='d3-academic-aid-first'
  if 'walk-on' in x.get('path','') and 'walk-on' not in b: b[1]='walk-on'
  return b
MAP2={'renfrow':['walk-on','football-junior-year','offer-and-signing'],'groenewegen':['offer-and-signing','eligibility-2-hard-deadlines'],'lowe':['walk-on','offer-and-signing'],'pichardo':['walk-on','eligibility-2-hard-deadlines'],'white':['offer-and-signing','eligibility-2-hard-deadlines'],'pirosko':['offer-and-signing','eligibility-2-hard-deadlines'],'marpet':['d3-academic-aid-first','walk-on','football-junior-year'],'rodenfels':['track-field-marks','d3-academic-aid-first','late-bloomer'],'perez':['late-bloomer','d3-academic-aid-first'],'coward':['d3-academic-aid-first','offer-and-signing'],'rodriguez':['late-bloomer','offer-and-signing'],'butler':['juco-to-d1','offer-and-signing'],'wondolowski':['offer-and-signing','eligibility-2-hard-deadlines'],'composite-swim':['eligibility-2-hard-deadlines','offer-and-signing']}
VID={x['id'] for x in S}-{'composite-swim'}
out=[]
for x in S+[SOCCER]:
  x=dict(x);f=FIX.get(x['id'],{})
  for k in('hs','college','timeline'):
    if k in f:x[k]=f[k]
  x['timeline']=list(x.get('timeline',[]))+f.get('add',[])
  for i,v in f.get('tl',{}).items(): x['timeline'][i]=v
  if x['id']=='coward': x['hs']='Fresno, CA'
  if x.get('basis'): x['basis']=[b.replace('Swimmer recruiting relies on club coach advocacy and posted times','Swimmer recruiting weighs past results, potential and conference fit, with club coach advocacy') for b in x['basis'] if 'athletes.org' not in b]
  x.pop('ethnicity',None)
  comp=bool(x.get('composite'))
  out.append({'id':x['id'],'name':x['name'],'short':'Maya (composite)' if comp else x['name'],'composite':comp,'label':x.get('label',''),'sport':x['sport'],
   'from':(x.get('hs') or 'Club swimmer').split(';')[0],'school':x.get('hs') or '','college':x.get('college') or 'D2 program','div':x['division'],'path':x['path'],
   'timeline':x['timeline'],'basis':x.get('basis',[]),'turning':x.get('turning',[]),'replicate':x.get('replicate',[]),
   'img':'/assets/media/cut-swimmer-640.webp' if comp else '','video':('/assets/media/real-%s-720p.mp4'%x['id']) if x['id'] in VID else '',
   'poster':('/assets/media/real-%s-poster.jpg'%x['id']) if x['id'] in VID else '','hold':x['id'] in HOLD,'playbooks':MAP2[x['id']]})
P={k:{'title':v['title'],'price':v['price_usd'],'type':'Playbook','who':v['who'],'outcome':v['outcome'],'toc':v['toc'],'tools':v['tools'],'pages':v['pages'],'format':v['format'],'status':v['status'],'notify':k in ('nil-high-school','d3-academic-aid-first','late-bloomer','juco-to-d1'),'beats':v['story_beats']} for k,v in PB.items()}
json.dump({'athletes':out,'playbooks':P,'bundles':C['bundles']},open(R+'/v3/W2-site/data.json','w'),indent=1)
open(R+'/site/assets/stories.js','w').write('window.STORY_ALL='+json.dumps({'athletes':out,'playbooks':P})+';(function(){var q=/[?&]flags=all/.test(location.search);window.STORY_DATA={athletes:STORY_ALL.athletes.filter(function(a){return q||!a.hold}),playbooks:STORY_ALL.playbooks}})();')
print(len(out),[a['id'] for a in out if a['hold']])
