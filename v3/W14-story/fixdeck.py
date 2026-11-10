import pathlib,re,sys
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
# 1. point patch_deck at deck.js
p=pathlib.Path("v3/W14-story/build_sports.py"); t=p.read_text(encoding="utf-8")
t=t.replace('def patch_deck():\n    p = SITE / "assets" / "stories.js"',
            'def patch_deck():\n    p = SITE / "assets" / "deck.js"')
p.write_text(t,encoding="utf-8")
print("patch_deck -> deck.js:", 'p = SITE / "assets" / "deck.js"' in t)
# 2. undo the stray SLUG prepend in stories.js
s=pathlib.Path("site/assets/stories.js"); js=s.read_text(encoding="utf-8")
if js.startswith("function SLUG"):
    js=js[js.index("\n")+1:]
    s.write_text(js,encoding="utf-8")
    print("stories.js restored, starts:",js[:22])
