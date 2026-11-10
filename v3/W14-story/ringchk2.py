import pathlib,sys,re
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
t=pathlib.Path("site/assets/ring.js").read_text(encoding="utf-8")
i=t.find("connectedCallback")
seg=t[i:i+1400]
print("connectedCallback head:"); print(re.sub(r"\s+"," ",seg)[:700])
print()
for k in ["kick(","render(","build(","innerHTML="]:
    j=t.find(k)
    print(k, "first at", j, "->", re.sub(r"\s+"," ",t[max(0,j-120):j+120])[:220] if j>=0 else None)
    print("  --")
css=pathlib.Path("site/assets/ring.css").read_text(encoding="utf-8")
print("story-ring css rules:", re.findall(r"story-ring[^{]*\{[^}]{0,120}\}", css)[:3])
print("min-height rules:", re.findall(r"[^{}]{0,40}min-height[^;}]{0,40}", css)[:4])
