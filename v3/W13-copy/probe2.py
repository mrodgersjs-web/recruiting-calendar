import json,pathlib
d=json.loads(pathlib.Path("site/recruitiq/data.json").read_text(encoding="utf-8"))
print("top keys:",list(d.keys()))
for k,v in d.items():
    if isinstance(v,list) and v and isinstance(v[0],dict) and "programs" in json.dumps(v)[:4000]:
        for row in v:
            if "programs" in row:
                print("\nbucket:",row.get("event_group") or row.get("sport") or list(row.keys())[:4])
                for p in row["programs"]:
                    print("   ", {kk:p.get(kk) for kk in ("id","name","level","conference","label_style","vintage","url")})
                break
        break
print("\n=== standards rows sample")
import re
t=pathlib.Path("site/recruitiq/data.json").read_text(encoding="utf-8")
i=t.find('"programs"'); print(t[i-200:i+1400])
