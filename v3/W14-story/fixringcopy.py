"""Ring copy that promised a story now promises what the click actually gives."""
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = pathlib.Path(__file__).resolve().parents[2] / "site" / "assets" / "ring.js"
t = p.read_text(encoding="utf-8")
before = t

swaps = [
    # the button on the focused tile
    ('<button class="sr__cta" data-read>Read the story \u2192</button>',
     '<button class="sr__cta" data-read>See the playbooks \u2192</button>'),
    # intro line under "Pick a path."
    ("Drag to browse, click to read the story.",
     "Drag to browse. Click one to see the playbooks and dates for that sport."),
    # pagination ticks
    ('aria-label="Story ${i+1}: ${a.sport}"', 'aria-label="Path ${i+1}: ${a.sport}"'),
    # screen-reader live region
    ('this.querySelector(\'[data-live]\').textContent=`Story ${this.index+1}: ${a.name}`',
     'this.querySelector(\'[data-live]\').textContent=`Path ${this.index+1}: ${a.sport}`'),
    # and say the sport on the button once a tile is focused
    ("this.querySelector('[data-read]').onclick=()=>location.href=SPORT_PATH(a);",
     "var _rd=this.querySelector('[data-read]');_rd.textContent='Playbooks for '+a.sport+' \\u2192';"
     "_rd.onclick=()=>location.href=SPORT_PATH(a);"),
]
for old, new in swaps:
    if old not in t:
        print(f"  MISS  {old[:60]}")
        continue
    t = t.replace(old, new)
    print(f"  ok    {old[:60]}")

p.write_text(t, encoding="utf-8")
print("\nchanged:", before != t)
print("stale strings left:", len(re.findall(r"Read the story|click to read the story|Story \$\{", t)))
