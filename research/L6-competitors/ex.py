import json,glob,os,re
def body(f):
    r=json.load(open(f));t=r.get("result",{}).get("content",[{}])[0].get("text","")
    try:return json.loads(t)
    except:return t
for f in sorted(glob.glob("raw/*.json")):
    b=body(f);n=os.path.basename(f)[:-5]
    s=json.dumps(b)
    if n.startswith(("ig_","tt_","x_")):
        d=b.get("data",b) if isinstance(b,dict) else {}
        def find(o,keys,out):
            if isinstance(o,dict):
                for k,v in o.items():
                    if k in keys and not isinstance(v,(dict,list)):out.setdefault(k,v)
                    find(v,keys,out)
            elif isinstance(o,list):
                for x in o[:1]:find(x,keys,out)
            return out
        print(n,find(d,{"username","handle","followers","followerCount","followersCount","follower_count","fullName","name","postsCount","mediaCount","videoCount","heartCount","isVerified","biography","bio","description"},{}))
    else: print(n,len(s),s[:200])
