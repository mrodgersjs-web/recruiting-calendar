import pathlib,sys,re
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
t=pathlib.Path("site/assets/deck.js").read_text(encoding="utf-8")
i=t.find("dk-route"); print("dk-route idx",i); print("bytes:",repr(t[i-30:i+140]))
j=t.find("dk-real"); print("\ndk-real idx",j); print("bytes:",repr(t[j-20:j+60]))
k=t.find("In this story"); print("\nin-this-story idx",k); print("bytes:",repr(t[k-40:k+30]))
