import re,pathlib,sys,html
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
F=[
("Every competitor fact below comes from a public page we read on 2026-11-05; anything we didn't check says \"Not checked\".","Every competitor fact below came from a public page. We read it on 2026-11-05. Anything we did not check says \"Not checked\"."),
("Every number below was read on its primary source by an independent audit on 2026-11-06 (W10) and links to it.","Every number below was read from the source that owns it, on 2026-11-06. Each one links to that source."),
("Each page lists the dates in order, the bylaw behind each one, and what happens if you wait.","Each page lists the dates in order. It shows the bylaw behind each date and what happens if you wait."),
("This is the working draft, checked against the rulebook and the sources, not a polished product page.","This is a working draft. It is checked against the rulebook and the sources. It is not a polished product page yet."),
("Offers do not arrive in the same words, so you cannot compare them as they come.","Offers do not arrive in the same words. You cannot compare them as they arrive."),
("Two school rules can end a D1 or D2 dream, and late is too late to fix them.","Two school rules can end a D1 or D2 dream. Late is too late to fix them."),
("Here is how to get them done early, plus a script for the meeting with your counselor.","Here is how to get them done early. There is also a script for the meeting with your counselor."),
("Everything we make, in one place, with the honest status of each","Everything we make, in one place, with the honest status of each item"),
("and tools for the parts that cost a family money:","and tools for the parts that cost a family money. Here is what is where:"),
("Rules that moved recently Under the old D1 model baseball had 11.7 equivalencies across at most 27 aided counters; an opted-in school may now in principle aid all 34 rostered players.","Rules that moved recently. Under the old D1 model, baseball had 11.7 scholarships across at most 27 aided players. A school that opted in may now aid all 34 players on the roster."),
]
n=0
for p in pathlib.Path("site").rglob("*.html"):
    t=p.read_text(encoding="utf-8",errors="ignore"); o=t
    for a,b in F: t=t.replace(a,b)
    if t!=o: p.write_text(t,encoding="utf-8"); n+=1
print("pages touched by the last prose pass:",n)
def prose(t):
    t=re.sub(r"<(script|style|noscript|svg)[^>]*>.*?</\1>"," ",t,flags=re.S|re.I)
    t=re.sub(r"<table\b.*?</table>"," ",t,flags=re.S|re.I)
    t=re.sub(r"<nav\b.*?</nav>|<footer\b.*?</footer>"," ",t,flags=re.S|re.I)
    t=re.sub(r"<[^>]*>"," ",t); return re.sub(r"\s+"," ",html.unescape(t)).strip()
t=prose(pathlib.Path("site/playbooks/eligibility-2-hard-deadlines/index.html").read_text(encoding="utf-8"))
for s in re.split(r"(?<=[.!?])\s+",t):
    if len(s.split())>=14: print("   LONG:",s[:180])
