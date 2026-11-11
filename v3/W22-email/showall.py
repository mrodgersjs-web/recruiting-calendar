import re, html, pathlib, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def clean(x):
    x = re.sub(r"<br\s*/?>", "\n", x)
    x = re.sub(r"</(p|li|div|h3|tr)>", "\n", x)
    x = re.sub(r"<[^>]+>", " ", x)
    x = html.unescape(x)
    return re.sub(r"[ \t]+", " ", x).strip()

for n in ("W20-two-sports/fb-playbook-plain.html", "W20-two-sports/wbb-playbook-plain.html", "W19-plain/basketball-playbook-plain.html"):
    t = pathlib.Path(n).read_text(encoding="utf-8")
    print("\n########", n)
    for m in re.finditer(r'<div class="tmpl">(.*?)</div>', t, re.S):
        print("--- SAMPLE EMAIL ---"); print(clean(m.group(1)))
    for kw in ("SAT", "ACT", "one to three", "six to eight weeks", "test score"):
        for m in re.finditer(re.escape(kw), t):
            seg = clean(t[max(0, m.start()-320):m.start()+320])
            print(">>", kw, "::", re.sub(r"\s+", " ", seg)[:330]); break
