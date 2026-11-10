import re,pathlib,sys
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
t=pathlib.Path("site/playbooks/index.html").read_text(encoding="utf-8")
main=t[t.find("<main"):t.find("</main>")+7]
i=main.find('<div class="pb-grid">')
print("grid starts at",i)
# depth scan to find the matching close
d=0; j=i
for m in re.finditer(r"<(/?)div\b",main[i:]):
    d += -1 if m.group(1) else 1
    if d==0:
        j=i+m.end()+6; break
print("grid ends at",j,"len",j-i)
seg=main[i:j]
print("divs inside grid:",len(re.findall(r"<div\b",seg)))
print("after grid:",re.sub(r"\s+"," ",main[j:j+400]))
cells=seg.split('<div class="pb-cell">')[1:]
print("\ncells:",len(cells))
for c in cells[:3]:
    print("   nested divs:",len(re.findall(r"<div\b",c)),"| len",len(c),"|",re.sub(r"\s+"," ",c)[:110])
