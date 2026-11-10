import pathlib,sys
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
p=pathlib.Path("site/assets/deck.js"); t=p.read_text(encoding="utf-8")
old = """return \'<a href="/story/\'+esc(a.id)+\'/"><b>\'+esc(a.short)+\'</b>"""
new = """return \'<a href="\'+(a.page===false?\'/sports/\'+SLUG(a.sport):\'/story/\'+esc(a.id))+\'"><b>\'+esc(a.short)+\'</b>"""
print("pattern present:", old in t)
p.write_text(t.replace(old,new),encoding="utf-8")
