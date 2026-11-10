import re,pathlib,sys
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
t=pathlib.Path("site/assets/ring.js").read_text(encoding="utf-8")
for m in re.finditer(r"/story/",t):
    print("--- ring.js @",m.start())
    print("   ",repr(re.sub(r"\s+"," ",t[max(0,m.start()-190):m.start()+120])))
print("\nSPORT_PATH refs:",len(re.findall("SPORT_PATH",t)))
