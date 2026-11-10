import re,sys,pathlib,json
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
html=pathlib.Path("site/playbooks/index.html").read_text(encoding="utf-8")
for ch in html.split('<div class="pb-cell">')[1:]:
    b=ch[:1600]
    s=re.search(r'href="/playbooks/([\w-]+)"',b)
    n=re.search(r'<p class="note">([^<]*)</p>',b)
    if s: print(f"{s.group(1):30} note={re.sub(chr(60)+'[^'+chr(62)+']*'+chr(62),'',n.group(1)).strip() if n else '-':24} button={'yes' if 'Get the playbook' in b else 'no'}")
