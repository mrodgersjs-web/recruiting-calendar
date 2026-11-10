import subprocess,sys,re
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
old=subprocess.run(["git","show","ab44c79~1:site/assets/stories.js"],capture_output=True,text=True).stdout
print("bytes:",len(old))
i=old.find("STORY_DATA")
while i>=0:
    print("at",i,"->",repr(old[max(0,i-90):i+240]))
    i=old.find("STORY_DATA",i+1)
