"""deck.js: a composite with no bio page points at its sources, not at a dead URL."""
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
f = pathlib.Path(__file__).resolve().parents[2] / "site" / "assets" / "deck.js"
t = f.read_text(encoding="utf-8")
before = t

old = """<a class="dk-src" style="font-size:13px" href="/story/'+esc(a.id)+'/">How this played out</a>"""
new = """<a class="dk-src" style="font-size:13px" href="'+SRC_LINK(a)+'">'+(a.page===false?'Where this comes from':'How this played out')+'</a>"""
if old in t:
    t = t.replace(old, new)
    print("ok  : secondary link made conditional")
else:
    print("MISS: secondary link")

helper = ("function SRC_LINK(a){if(a.page===false&&a.playbooks&&a.playbooks.length)"
          "return'/playbooks/'+a.playbooks[0]+'/#sources';return'/story/'+a.id+'/';}\n")
if "function SRC_LINK" not in t:
    t = helper + t
    print("ok  : SRC_LINK added")

f.write_text(t, encoding="utf-8")
print("changed:", before != t)
print("story hrefs in deck.js:", re.findall(r'"/story/[^"]*', t))
