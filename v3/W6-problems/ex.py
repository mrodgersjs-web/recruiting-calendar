import json,sys,re
def load(f):
    t=open(f).read(); t=t[t.find('data: ')+6:] if 'data: ' in t else t
    d=json.loads(t.strip().split('\n')[0]); c=d['result']['content'][0]['text']
    return json.loads(c)
KEYS=('text','title','body','description','caption','snippet','content','name','url','memberCount','members','privacy','link','commentCount','viewCount','playCount','likes','bodyText','adText')
def walk(o,out,d=0):
    if isinstance(o,dict):
        row={k:o[k] for k in o if k in KEYS and isinstance(o[k],(str,int)) and o[k]}
        if row: out.append(row)
        for v in o.values():
            if isinstance(v,(dict,list)): walk(v,out,d+1)
    elif isinstance(o,list):
        for v in o: walk(v,out,d+1)
for f in sys.argv[2:]:
    out=[];walk(load(f),out)
    print('==',f,len(out))
    for r in out[:int(sys.argv[1])]:
        print(' |', json.dumps(r)[:300])
