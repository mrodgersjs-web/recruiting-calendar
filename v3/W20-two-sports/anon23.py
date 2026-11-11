import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def subn(path, pairs):
    p = pathlib.Path(path); t = p.read_text(encoding="utf-8"); n0 = t
    for pat, rep in pairs:
        t, n = re.subn(pat, rep, t)
        print("%-46s %-34s -> %d" % (path.split("/")[-1], pat[:34], n))
    p.write_text(t, encoding="utf-8")
    return t != n0

common = [
    (r"Geneva Township HS, WI", "Anytown South HS, WI"),
    (r"Geneva Township High School in Wisconsin", "Anytown South High School in Wisconsin"),
    (r"\(414\)", "(555)"),
    (r"Coach\s+Bellamy", "Coach Rivera"),
]
subn("W20-two-sports/fb-plain.py", common + [
    (r"Tested at the Badger\s+Combine that day,", "Tested the same day at Impact Athletic\n  Development,"),
    (r"dwhitfield@example\.com", "player@example.com"),
    (r"parent copied: whitfield@example\.com", "parent copied: parent@example.com"),
])
subn("W20-two-sports/wbb-plain.py", common + [
    (r"mweber@example\.com", "player@example.com"),
    (r"parent copied: weber@example\.com", "parent copied: parent@example.com"),
    (r"Club team and summer dates: \[link\]\.",
     "Club team and summer dates: [link]. My camp record and any\nverified numbers will come from Impact Athletic Development this July."),
])
subn("W19-plain/bball-plain.py", [
    (r"Geneva Township, WI", "Anytown South, WI"),
    (r"High school coach: \{\{name\}\}, \{\{phone\}\}",
     "High school coach: {{name}}, {{phone}}\nCamp and combine record: {{camp name, or 'no invite yet'}}"),
])
