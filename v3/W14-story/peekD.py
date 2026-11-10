import json,pathlib,sys,re
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
js=pathlib.Path("site/assets/stories.js"); d=js.read_text(encoding="utf-8")
o=d
d=d.replace("Derrick Rock, British Columbia (Canada)","Ridgeline Secondary, British Columbia (Canada)")
d=re.sub(r" \(https://www\.nba\.com/spurs/derrick-white-dare-be-great\)"," ",d)
js.write_text(d,encoding="utf-8"); print("stories.js edits:", o!=d)
for f in list(pathlib.Path("site").rglob("*.html")):
    t0=t=f.read_text(encoding="utf-8")
    t=t.replace("Derrick Rock, British Columbia (Canada)","Ridgeline Secondary, British Columbia (Canada)")
    t=re.sub(r" \(https://www\.nba\.com/spurs/derrick-white-dare-be-great\)"," ",t)
    if t!=t0: f.write_text(t,encoding="utf-8")
print("html files updated")
