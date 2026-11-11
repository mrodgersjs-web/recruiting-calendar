import pathlib, sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
pat = re.compile(r'(<h2 style="margin-top:6mm">)(10\. Ten ways)')
for n in ("wbb-plain.py", "fb-plain.py"):
    p = pathlib.Path(n); t = p.read_text(encoding="utf-8")
    t2, k = pat.subn(r'\1</section>\n<section>\n\1\2', t)
    print(n, "chapters split:", k)
    p.write_text(t2, encoding="utf-8")
