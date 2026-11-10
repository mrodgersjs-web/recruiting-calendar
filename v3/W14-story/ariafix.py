import pathlib,sys,hashlib
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
p=pathlib.Path("site/assets/ring.js"); t=p.read_text(encoding="utf-8")
old='aria-label="Read story: ${escA(a.name)}"'
new='aria-label="${escA("Playbooks for " + (a.sport||"this sport") + ": " + a.name)}"'
print("found:", old in t)
p.write_text(t.replace(old,new),encoding="utf-8")
print("ring.js md5[:8]:", hashlib.md5(p.read_bytes()).hexdigest()[:8])
