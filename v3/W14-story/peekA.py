import json,pathlib,sys,re
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
js=pathlib.Path("site/assets/stories.js").read_text(encoding="utf-8")
d=json.JSONDecoder().raw_decode(js[js.index("{"):])[0]
for a in d["athletes"]:
    if a["id"] in ("sara","composite-swim","composite-softball"):
        print(a["id"],"| name:",a["name"],"| from:",a.get("from"),"| college:",a.get("college"))
        print("   basis:",str(a.get("basis"))[:200])
"--- what the value was before the recast (git HEAD)"
import subprocess
old=subprocess.run(["git","show","HEAD:site/assets/stories.js"],capture_output=True,text=True).stdout
o=json.JSONDecoder().raw_decode(old[old.index("{"):])[0]
for a in o["athletes"]:
    if a["id"]=="sara":
        print("   BEFORE from:",a.get("from"),"| school:",a.get("school"))
