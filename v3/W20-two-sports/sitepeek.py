import re,sys,json,pathlib
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
s=pathlib.Path("site/data.js").read_text(encoding="utf-8")
s=s[s.index("{"):s.rindex("}")+1]
d=json.loads(s)
for k,v in d.items():
    if isinstance(v,dict):
        dl=v.get("deadlines",[])
        print("KEY %-22s rows=%d  class_year=%s" % (k,len(dl),v.get("class_year")))
        for r in dl:
            if "contact" in r["event"].lower() or "13.1.1" in r.get("rule",""):
                print("     %s | %s | %s" % (r["iso_date"], r["event"][:64], r.get("rule","")))
    else:
        print("KEY %-22s %r" % (k,v))
