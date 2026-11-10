import re,pathlib,sys
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
t=pathlib.Path("site/assets/deck.js").read_text(encoding="utf-8")
print("listeners:",re.findall(r"addEventListener\([\w'\"+, ]{0,40}",t)[:6])
for m in re.finditer(r"closest\(['\"]([^'\"]+)",t):
    print("   delegated on:",m.group(1))
print("\nSLUG defined:", "function SLUG" in t)
print("story hrefs left in deck.js:", re.findall(r"/story/[\w'+/.-]*",t))
r=pathlib.Path("site/assets/ring.js").read_text(encoding="utf-8")
print("\nring story-ish hrefs:", re.findall(r"['\"]/story/[^'\"]*['\"]",r))
print("ring SPORT_PATH uses:", len(re.findall("SPORT_PATH\\(",r)))
