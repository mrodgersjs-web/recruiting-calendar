import os,re,collections
names=["Butler","Coward","Groenewegen","Lowe","Marpet","Perez","Pichardo","Pirosko","Renfrow","Rodriguez","Rodenfels","Wondolowski","Clemson","Appalachian","Alabama","Tampa Bay","Willamette","Eastern Washington","Washington State","UCLA","Hobart","Fordham","Marist","Holy Cross","Oglethorpe","Brown","Rutgers","Princeton","Eastern Michigan","Oral Roberts","Gannon","Doane","Centre","UCCS","Chico State","Culver","Marquette","Tyler JC","Minnesota","Allister","Ritter","Brunelli","Force","Vote","Owens","Williams","Socastee","Tomball","Legend","De La Salle","Eastlake","Buchanan","Dayton Christian","La Costa Canyon","Hastings"]
pat={n:re.compile(r"\b"+re.escape(n)+r"\b",re.I) for n in names}
loc=collections.defaultdict(lambda: collections.defaultdict(int))
for root,dirs,files in os.walk("."):
    if ".git" in root: continue
    for fn in files:
        if not fn.lower().endswith((".html",".js",".json",".md",".py",".txt",".xml",".css",".csv",".sh")): continue
        p=os.path.join(root,fn).replace(os.sep,"/")
        try: t=open(p,encoding="utf-8",errors="ignore").read()
        except: continue
        for n,r in pat.items():
            c=len(r.findall(t))
            if c: loc[n][p]+=c
top=("site","v3","funnel","research","api",".")
def bucket(p):
    for t in top:
        if p.startswith("./"+t+"/") or (t=="." and p.count("/")==1): return t if t!="." else "root"
    return p.split("/")[1] if p.startswith("./") else p.split("/")[0]
print(f"{'name':<18}{'tot':>6}   where")
for n in names:
    if n not in loc: continue
    b=collections.Counter()
    for p,c in loc[n].items(): b[bucket(p)]+=c
    print(f"{n:<18}{sum(loc[n].values()):>6}   "+", ".join(f"{k}:{v}" for k,v in b.most_common(4)))
print("\n=== files with the most name hits")
fc=collections.Counter()
for n,d in loc.items():
    for p,c in d.items(): fc[p]+=c
for p,c in fc.most_common(22): print(f"{c:>4}  {p}")
print("\n=== total distinct files touched:", len(fc))
