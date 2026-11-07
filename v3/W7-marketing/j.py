import json,sys
def load(f):
    t=open(f).read(); t=t[t.find('{'):]
    d=json.loads(t)
    try: return json.loads(d['result']['content'][0]['text'])
    except Exception: return d
