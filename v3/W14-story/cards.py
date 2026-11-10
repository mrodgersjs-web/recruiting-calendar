import re,pathlib,sys,json
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
t=pathlib.Path("site/playbooks/index.html").read_text(encoding="utf-8")
cells=re.findall(r'<div class="pb-cell">(.*?)</div>\s*(?=<div class="pb-cell">|</div>$|$)',t,re.S)
out=[]
for c in cells:
    href=re.search(r'href="?(/playbooks/[\w-]+)',c)
    thumb=re.search(r'<span class="pb-thumb"><b>(.*?)</b><i>(.*?)</i>',c)
    lab=re.search(r'<span class="lab">(.*?)</span>',c)
    ttl=re.search(r'<span class="pb-t">(.*?)</span>',c)
    sub=re.search(r'<span class="pb-s">(.*?)</span>',c)
    pr=re.search(r'<span class="pb-p">(.*?)</span>',c)
    offer=re.search(r'data-offer="([\w-]+)"',c)
    if not (href and thumb and ttl): continue
    out.append(dict(href=href.group(1),badge=thumb.group(1),fmt=thumb.group(2),audience=lab.group(1) if lab else "",
                    title=ttl.group(1),blurb=sub.group(1) if sub else "",price=pr.group(1) if pr else "",offer=offer.group(1) if offer else None))
print(len(out),"cards")
for o in out: print(f"  {o['href']:44} badge={o['badge']:14} fmt={o['fmt']:22} price={o['price']:10} offer={bool(o['offer'])}\n      {o['title']} :: {o['blurb'][:70]}")
json.dump(out,open("v3/W14-story/store-cards.json","w",encoding="utf-8"),indent=1)
print("\nalso: story pages -> playbooks mapping from stories.js")
js=pathlib.Path("site/assets/stories.js").read_text(encoding="utf-8")
d=json.loads(re.search(r"window\.STORY_ALL\s*=\s*(\{.*?\})\s*\nwindow\.",js,re.S).group(1)) if re.search(r"window\.STORY_ALL\s*=\s*(\{.*?\})\s*\nwindow\.",js,re.S) else json.JSONDecoder().raw_decode(js[js.index("{"):])[0]
for a in d["athletes"]:
    print(f"  {a['id']:20} {a['sport']:16} playbooks={a.get('playbooks')}")
