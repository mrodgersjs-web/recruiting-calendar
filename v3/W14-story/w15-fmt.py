import pathlib,sys,re
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
t=pathlib.Path("site/playbooks/walk-on/index.html").read_text(encoding="utf-8")
i=t.find("Stories that use it"); print("CHIPS:",repr(t[i-12:i+430]))
j=t.find('class="src-list"'); print("\nSOURCES:",re.sub(r"\s+"," ",t[j-40:j+700])[:760])
