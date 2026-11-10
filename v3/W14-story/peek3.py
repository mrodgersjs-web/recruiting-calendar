import pathlib,re,sys
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
t=pathlib.Path("v3/W14-story/build_sports.py").read_text(encoding="utf-8")
i=t.find("def build_hub")
print(t[i:i+1500])
