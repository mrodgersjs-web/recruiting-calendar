import json,sys,re
def load(f):
    s=open(f).read()
    m=[l[5:] for l in s.splitlines() if l.startswith('data:')]
    r=json.loads(m[-1] if m else s)
    t=r['result']['content'][0]['text']
    try: return json.loads(t)
    except: return t
def walk(o,out):
    if isinstance(o,dict):
        out.append(o); [walk(v,out) for v in o.values()]
    elif isinstance(o,list): [walk(v,out) for v in o]
for f in sys.argv[1:]:
    d=load(f); print('==',f)
    L=[];walk(d,L)
    for x in L:
        u=x.get('url') or x.get('link'); tx=x.get('snippet') or x.get('description') or x.get('desc') or x.get('title') or x.get('text')
        vid=x.get('aweme_id') or x.get('videoId') or x.get('video_id')
        if (u or vid) and tx: print('-',vid or '',u or '','|',str(tx)[:240].replace('\n',' '))
