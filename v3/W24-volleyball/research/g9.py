import pathlib, sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
t = pathlib.Path("02-measurables-by-position.md").read_text(encoding="utf-8")
for m in re.finditer("Northern Michigan", t):
    print(t[max(0,m.start()-200):m.start()+260].replace("\n", " ")); print("-"*40)
i = t.find("Method: I read")
print(t[i:i+320])
for k in ["212", "2a", "rosters above"]:
    j = t.find(k)
    print("###", k, "->", t[max(0,j-120):j+220].replace("\n"," ") if j>0 else "not found")
