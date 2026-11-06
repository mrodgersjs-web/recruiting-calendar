import json,urllib.request,time
B='http://127.0.0.1:4912';CV='cv_iq7tz77i'
def post(p,b):
  for i in range(3):
    try: return json.load(urllib.request.urlopen(urllib.request.Request(B+p,json.dumps(b).encode(),{'Content-Type':'application/json'}),timeout=15))
    except Exception as e: time.sleep(1);err=e
  raise err
st=json.load(urllib.request.urlopen(f'{B}/api/state?canvas={CV}'));n0,e0=len(st['nodes']),len(st.get('edges',[]))
T={nd['data'].get('title',''):nd['id'] for nd in st['nodes']}
tier={k:next(i for t,i in T.items() if t.startswith(p)) for k,p in [('Free','Free'),('Sideline','Sideline'),('Pathway','Pathway'),('Recruiting Audit','Recruiting Audit'),]}
F=json.load(open('../L2-jacob-studio/FEATURES.json'))['features']
ids={};y={'P':1300,'I':1300}
for r in F:
  if r['bucket']=='KEEP_PRIVATE': continue
  p=r['bucket']=='PRODUCTIZE'
  title=(f"[{r['tier']}] " if p else '[engine] ')+(r['parent_feature'] if p else r['id'])
  x=380 if p else 1520; k='P' if p else 'I'
  ids[r['id']]=post('/api/nodes/add',{'canvas':CV,'kind':'note','data':{'title':title,'text':f"{r['capability']}\nL2 id: {r['id']} | effort {r['build_effort']} | src: {r['source_path']}"},'x':x,'y':y[k],'w':340})['node']['id']; y[k]+=190
  if p: post('/api/edges/add',{'canvas':CV,'from':ids[r['id']],'to':tier[r['tier']],'label':'feature of'})
E=[('coach-identity-resolver','coach-directory'),('coach-identity-resolver','coach-follow-tracker'),('coach-census-refresh','coach-activity-benchmarks'),('program-list','coach-directory'),('program-list','target-school-list'),('film-assembly','film-reel-brief'),('maxpreps-stats-pull','outreach-tracker'),('eden-publisher','content-calendar'),('agents-roster','recruiting-profile-audit'),('dashboard','kpi-scorecard'),('harness-governance','approval-gate')]
for a,b in E: post('/api/edges/add',{'canvas':CV,'from':ids[a],'to':ids[b],'label':'powers'})
s=json.load(urllib.request.urlopen(f'{B}/api/state?canvas={CV}'));print('before',n0,e0,'after',len(s['nodes']),len(s.get('edges',[])),'added',len(ids))
