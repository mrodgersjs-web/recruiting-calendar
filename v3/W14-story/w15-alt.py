import pathlib,sys
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
p=pathlib.Path("site/assets/deck.js"); t=p.read_text(encoding="utf-8")
old = """alt=\"Illustration of a fictional composite '"""; new = """alt=\"Illustration of a fictional '"""
print("alt text present:", old in t)
t=t.replace(old,new)
p.write_text(t,encoding="utf-8")
