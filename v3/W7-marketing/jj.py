import json
def load(f):
    t=open(f).read(); s=t[t.find('{'):]
    d,_=json.JSONDecoder(strict=False).raw_decode(s)
    sc=d.get('result',{}).get('structuredContent')
    if sc: return sc
    return json.loads(d['result']['content'][0]['text'],strict=False)
