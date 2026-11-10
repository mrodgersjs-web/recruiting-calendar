import pathlib,sys,re
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
for name in ["site/assets/deck.js","site/assets/ring.js"]:
    p=pathlib.Path(name); t=p.read_text(encoding="utf-8"); o=t
    t=t.replace("""href="/playbooks/'+id+'/\">""", """href="/playbooks/'+id+'">""")
    t=re.sub(r"""(['\"])/sports/\1\s*\+\s*(\w+\(?\w*\)?|\w+)\s*\+\s*(['\"])/""", r"\1/sports/\2\3", t)
    t=re.sub(r"""(['\"])/athlete/\1\s*\+\s*([^+]+?)\s*\+\s*(['\"])/""", r"\1/athlete/\2\3", t)
    if t!=o: p.write_text(t,encoding="utf-8"); print("patched",name)
    for m in re.finditer(r"['\"]/(sports|athlete|playbooks|story)/[^'\"]{0,24}['\"]", t):
        print("   ",m.group(0))
