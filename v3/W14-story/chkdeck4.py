import pathlib,sys
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
t=pathlib.Path("site/assets/deck.js").read_text(encoding="utf-8")
i=t.find("""href="/story/'+esc(a.id)+'/""")
print(repr(t[max(0,i-320):i+180]))
