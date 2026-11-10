import pathlib,sys,re
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
t=pathlib.Path("site/assets/stories.js").read_text(encoding="utf-8")
print("STORY_DATA occurrences:", t.count("STORY_DATA"))
print("tail 400:", repr(t[-400:]))
print("has STORY_ALL:", t.count("STORY_ALL"))
