import pathlib,re,sys
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
t=pathlib.Path("site/assets/stories.js").read_text(encoding="utf-8")
i=t.find("dk-read")
print("has SLUG:", "function SLUG" in t)
print("ctx around dk-read:")
print(repr(t[max(0,i-260):i+260]))
