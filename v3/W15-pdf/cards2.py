import re,sys,pathlib
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
t=pathlib.Path("site/playbooks/index.html").read_text(encoding="utf-8")
for m in re.finditer(r'.{420}?\d+\s*pages\s*\u00b7\s*PDF', t):
    print(re.sub(r"\s+"," ",m.group(0))[-330:])
    print("   ---")
