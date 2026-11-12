import re,sys,pathlib,json,html
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
SITE=pathlib.Path("site")
# what each sport page offers
for d in sorted((SITE/"sports").glob("*/index.html")):
    t=d.read_text(encoding="utf-8")
    cards=re.findall(r'href="/playbooks/([\w-]+)"',t)
    seen=[]
    for c in cards:
        if c not in seen: seen.append(c)
    dated = len(re.findall(r'<tr[^>]*>',t))
    print(f"{d.parent.name:14} playbook cards {len(seen):2}  table rows(dates) {dated:3}  first: {', '.join(seen[:4])}")
