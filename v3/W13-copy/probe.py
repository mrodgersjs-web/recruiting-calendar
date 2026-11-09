import re,pathlib,collections
print("=== 'White' outside story scope, in context")
for f in ["site/playbooks/offer-and-signing/index.html","site/playbooks/eligibility-2-hard-deadlines/index.html","site/personalize/seed.json"]:
    t=pathlib.Path(f).read_text(encoding="utf-8",errors="ignore")
    for m in re.finditer(r".{90}\bWhite\b.{90}",t,re.S):
        print(f"  {f}: ...{re.sub(chr(92)+'s+',' ',m.group(0))}...")
print("\n=== 'Brown' context in recruitiq")
for f in ["site/recruitiq/index.html","site/recruitiq/data.json","site/recruitiq/recruitiq.js"]:
    p=pathlib.Path(f)
    if not p.exists(): continue
    t=p.read_text(encoding="utf-8",errors="ignore")
    for m in re.finditer(r".{110}\bBrown\b.{110}",t,re.S):
        print(f"  {f}: ...{re.sub(chr(92)+'s+',' ',m.group(0))}...")
print("\n=== story image assets: how many, what kinds, are they referenced?")
files=list(pathlib.Path("site/assets/media").rglob("*"))
names=[f.name for f in files if f.is_file()]
print(" media files:",len(names))
print(" surname-named:",sum(1 for n in names if re.search(r"(butler|coward|groenewegen|lowe|marpet|perez|pichardo|pirosko|renfrow|rodriguez|rodenfels|white|wondolowski)",n)))
ref=collections.Counter()
for p in pathlib.Path("site").rglob("*.html"):
    t=p.read_text(encoding="utf-8",errors="ignore")
    for m in re.finditer(r"ax-([a-z]+)-(1080|1600)",t): ref[m.group(1)]+=1
print(" referenced in HTML:",dict(ref))
js=pathlib.Path("site/assets/stories.js").read_text(encoding="utf-8",errors="ignore")
print(" referenced in stories.js:",len(re.findall(r"ax-([a-z]+)-",js)))
print("\n=== sample: what does the story page do with the image?")
t=pathlib.Path("site/story/renfrow/index.html").read_text(encoding="utf-8",errors="ignore")
for m in re.finditer(r"<img[^>]*>",t): print("  ",m.group(0)[:220])
for m in re.finditer(r"ax-[a-z]+-\d+",t): print("   ref:",m.group(0))
