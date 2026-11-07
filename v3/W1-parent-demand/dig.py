import json,glob,os,sys
def B(f):
    try:return json.loads(json.load(open(f))["result"]["content"][0]["text"])
    except Exception as e:return {}
for f in sorted(glob.glob("raw/"+sys.argv[1]+"*.json")):
    d=B(f).get("data") or {}
    items=d.get("posts") or d.get("videos") or d.get("results") or d.get("items") or d.get("comments") or d.get("threads") or []
    print("==",f,len(items), list(d.keys())[:6])
    for p in items[:int(sys.argv[2]) if len(sys.argv)>2 else 10]:
        t=(p.get("title") or "")+" | "+(p.get("body") or p.get("text") or p.get("selftext") or p.get("description") or p.get("caption") or p.get("snippet") or "")[:200]
        print(" ",str(p.get("createdAt") or p.get("publishedAt") or "")[:10],p.get("subredditPrefixedName") or "",p.get("score") or p.get("likeCount") or "",p.get("numComments") or p.get("commentCount") or "",t.replace("\n"," ")[:300],p.get("url") or p.get("permalink") or "")
