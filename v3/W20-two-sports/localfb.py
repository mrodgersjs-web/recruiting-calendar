import re, sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
t = open(r"site/data.js", encoding="utf-8").read()
rows = re.findall(r"\{[^{}]*?iso_date[^{}]*?\}", t, re.S)
def f(b, k):
    mm = re.search(r"'%s'\s*:\s*'((?:[^'\\]|\\.)*)'" % k, b) or re.search(r'"%s"\s*:\s*"((?:[^"\\]|\\.)*)"' % k, b)
    return mm.group(1) if mm else ""
def num(b, k):
    mm = re.search(r"'%s'\s*:\s*'?'?(\d{4}-\d{2}-\d{2})" % k, b)
    return mm.group(1) if mm else ""
print("total deadline rows in data.js:", len(rows))
import collections
c = collections.Counter()
for b in rows:
    d = f(b, "iso_date") or num(b, "iso_date")
    c[("fb" if re.search(r"(?i)football|gridiron|combine|pro day|early signing", b) else "other")] += 1
print(c)
for b in rows[:60]:
    print("  %-11s %-9s %-58s %-26s %s" % (f(b,"iso_date"), f(b,"kind"), f(b,"event")[:58], f(b,"rule")[:26], f(b,"citation_url")[:52]))
