# -*- coding: utf-8 -*-
import re,sys,pathlib
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
raw=pathlib.Path(r"v3\W19-plain\customer-text.txt").read_text(encoding="utf-8")
pages=re.split(r"===== PAGE (\d+) =====", raw)
items=[(int(pages[i]), re.sub(r"\s+"," ",pages[i+1]).strip()) for i in range(1,len(pages)-1,2)]
print("pages:",len(items))
for n,t in items:
    head = bool(re.search(r"T\s*H\s*E\s*C\s*O\s*M\s*M\s*I\s*T", t))
    foot = bool(re.search(r"EDUCAT\s*I?O?N,? NOT LEGA", t))
    num  = bool(re.search(r"/\s*\d+\s*$|/\s*1\s*6\s*$", t.strip()))
    first= t.replace("T H E C O M M I T B O O K","").strip()[:56]
    print(" p%-3d head %s foot %s pgno %s | %s" % (n,"Y" if head else "-","Y" if foot else "-","Y" if num else "-",first))
h=pathlib.Path(r"v3\W19-plain\basketball-playbook-plain.html").read_text(encoding="utf-8")
brit=sorted(set(re.findall(r"(?i)\b(programme|programmes|defence|counsellor|centre|behaviour|organis\w+|recognis\w+|analyse\w*|licence|labour|colour|travelling|judgement|prioritis\w+|realis\w+|utilis\w+|deprioritis\w+)\b", h)))
print("british spellings left:", brit)
jargon=sorted(set(re.findall(r"(?i)\b(roster math|went sideways|position-group|unrecruitable|equivalenc\w+|permissible|nonqualifier|settlement school\w*|institutional money event|grassroots|amateurism|core GPA|on the board|a wish, not a plan)\b", h)))
print("insider terms present (must be defined in plain words nearby):", jargon)
for term in jargon:
    m=re.search(r"(?i)[^<>]{0,150}\b%s\b[^<>]{0,150}" % re.escape(term.strip('\\b')), h)
    print("   *", term, "->", re.sub(r"\s+"," ",m.group(0))[:210] if m else "")
