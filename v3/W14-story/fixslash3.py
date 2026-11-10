import pathlib,sys,re
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
for name in ["site/assets/deck.js","site/assets/ring.js"]:
    p=pathlib.Path(name); t=p.read_text(encoding="utf-8"); o=t
    for slug in ["track-field","swimming","lacrosse"]:
        t=t.replace("'/sports/%s/'" % slug, "'/sports/%s'" % slug)
    t=t.replace("href='/sports/'", "href='/sports'")
    t=t.replace('href="/sports/"', 'href="/sports"')
    if t!=o:
        p.write_text(t,encoding="utf-8"); print("patched",name)
    for m in re.finditer(r"href=[^ ]{0,34}", t):
        s=m.group(0)
        if any(k in s for k in ("/sports","/athlete","/story","/playbooks")):
            print("   ", name.split("/")[-1], s)
