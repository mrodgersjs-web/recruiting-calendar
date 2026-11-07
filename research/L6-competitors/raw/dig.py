import json,glob,os,datetime
def B(f):
    try:return json.loads(json.load(open(f))["result"]["content"][0]["text"])
    except:return {}
now=datetime.datetime(2026,11,5,tzinfo=datetime.timezone.utc)
for f in sorted(glob.glob("raw/*.json")):
    n=os.path.basename(f)[:-5];d=B(f).get("data") or {}
    if n.startswith(("ig_","ig2_","tt_","x_","ytch")):
        p=d.get("profile") or d.get("channel") or {}
        if not p:continue
        st={k:v for k,v in p.items() if isinstance(v,(int,float)) and not isinstance(v,bool)}
        for k in("stats","metrics","counts"):
            if isinstance(p.get(k),dict):st.update(p[k])
        print("PROF",n,p.get("handle"),st)
        rm=d.get("recentMedia") or []
        if isinstance(rm,dict):rm=rm.get("items") or rm.get("media") or []
        for m in rm[:12]:
            print("  M",str(m.get("takenAt") or m.get("createdAt") or m.get("timestamp"))[:10],m.get("mediaType") or m.get("type"),{k:v for k,v in (m.get("metrics") or m.get("stats") or {}).items()} or (m.get("likeCount"),m.get("commentCount"),m.get("playCount")),(m.get("caption") or m.get("text") or "")[:110].replace("\n"," "),m.get("url") or m.get("permalink"))
    elif n.startswith("igreels"):
        for m in (d.get("items") or d.get("media") or [])[:12]:
            print("  R",n,str(m.get("takenAt") or m.get("createdAt"))[:10],m.get("metrics") or m.get("stats"),(m.get("caption") or "")[:110].replace("\n"," "),m.get("url"))
    elif n.startswith(("yt_","ytsearch")):
        for v in (d.get("videos") or d.get("results") or d.get("items") or [])[:10]:
            print("  V",n,str(v.get("publishedAt") or v.get("publishedTime"))[:12],v.get("viewCount") or (v.get("metrics") or v.get("stats") or {}),(v.get("title") or "")[:100],v.get("url"))
    elif n.startswith("fbads"):
        ads=d.get("ads") or []
        print("ADS",n,len(ads),d.get("page",{}).get("hasMore"))
        for a in ads[:6]:
            s=json.dumps(a);
            print("  A",a.get("startDate") or a.get("startedAt") or a.get("deliveryStartTime"),(a.get("body") or a.get("text") or a.get("title") or (a.get("snapshot") or {}).get("body") or s[200:420])[:200].replace("\n"," "),a.get("url"))
    elif n.startswith(("reddit_","threads")):
        for p in (d.get("posts") or [])[:8]:
            print("  P",n,str(p.get("createdAt") or p.get("created"))[:10],p.get("subredditPrefixedName"),p.get("score"),p.get("numComments") or p.get("commentCount"),p["title"][:100],p.get("url") or p.get("permalink"))
    elif n.startswith("rcom"):
        cs=d.get("comments") or []
        print("COM",n,d.get("post",{}).get("url") if isinstance(d.get("post"),dict) else "")
        for c in cs[:14]:
            print("  C",c.get("score"),(c.get("body") or c.get("text") or "")[:260].replace("\n"," "),c.get("permalink") or c.get("url"))
