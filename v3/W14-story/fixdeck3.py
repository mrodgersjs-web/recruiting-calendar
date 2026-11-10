import pathlib,sys,re
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
p=pathlib.Path("site/assets/deck.js"); t=p.read_text(encoding="utf-8")
t=re.sub(r"^function SRC_LINK\(a\)\{.*?\}\n",
 "function SRC_LINK(a){if(a.page===false){var pb=(a.related||[])[0];return pb?'/playbooks/'+pb+'#sources':'/how-we-source';}"
 "return (a.source&&/^https?:/.test(a.source))?a.source:'/story/'+a.id+'#sources';}\n", t, count=1)
t=t.replace('href="/sports/\'+SLUG(a.sport)+\'/"','href="/sports/\'+SLUG(a.sport)+\'"')
t=t.replace('"/playbooks/"+encodeURIComponent(p.id)+"/"','"/playbooks/"+encodeURIComponent(p.id)')
p.write_text(t,encoding="utf-8")
print(t.splitlines()[0])
print("sports href:", "href=\"/sports/' + SLUG(a.sport) + \"" in t or "href='/sports/" in t)
print("playbook chip:", '"/playbooks/"+encodeURIComponent(p.id))+"' in t or 'encodeURIComponent(p.id))' in t)
