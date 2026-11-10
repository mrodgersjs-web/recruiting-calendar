import pathlib,sys
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
p=pathlib.Path("site/assets/deck.js"); t=p.read_text(encoding="utf-8")
anchor = "   Desktop keeps <story-ring>. Names are placeholders; no real person is shown. */\n"
print("anchor present:", anchor in t, "| IIFE present:", "(function(){" in t.splitlines()[3] if len(t.splitlines())>3 else "?")
if "(function(){" not in t.split("\n")[3]:
    t = t.replace(anchor, anchor + "(function(){\n", 1)
    p.write_text(t, encoding="utf-8")
    print("IIFE restored")
