"""Fix the two JS patches: the deck string, and ring.js's keyboard + view handlers."""
import pathlib
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = pathlib.Path(__file__).resolve().parents[2]
SITE = ROOT / "site"

# 1. the deck template must not carry its own outer quotes: the source string
#    stays open so it can continue with </div>'+
tpl = ROOT / "v3" / "W14-story" / "deck-cta.txt"
tpl.write_text(
    '<a class="btn btn--primary dk-read" href="/sports/\'+SLUG(a.sport)+\'/">Playbooks for '
    "\'+esc(a.sport)+'</a> <a class=\"dk-src\" style=\"font-size:13px\" href=\"/story/"
    '\'+esc(a.id)+\'/">How this played out</a>\n', encoding="utf-8")
print("deck template head/tail:", repr(tpl.read_text(encoding="utf-8")[:40]), "...",
      repr(tpl.read_text(encoding="utf-8")[-30:]))

# 2. ring.js: keyboard Enter and the [data-view] button still went to the bio page
p = SITE / "assets" / "ring.js"
t = p.read_text(encoding="utf-8")
before = t
t = t.replace("location.href='/story/'+this.A[this.index].id",
              "location.href=SPORT_PATH(this.A[this.index])")
t = t.replace("return location.href='/story/'+this.A[+b.dataset.view].id",
              "return location.href=SPORT_PATH(this.A[+b.dataset.view])")
p.write_text(t, encoding="utf-8")
print("ring.js handlers retargeted:", before != t)
print("ring.js /story/ left:", len(re.findall(r"/story/", t)))

# 3. re-apply the deck patch through the builder so there is one source of truth
r = subprocess.run([sys.executable, str(ROOT / "v3" / "W14-story" / "build_sports.py")],
                   cwd=ROOT, capture_output=True, text=True)
print("\nbuild:", r.stdout.strip().splitlines()[-4:])
if r.returncode:
    print(r.stderr[-600:])

# 4. syntax check both files with node
for js in ("ring.js", "deck.js", "stories.js"):
    f = SITE / "assets" / js
    proc = subprocess.run(["node", "--check", str(f)], capture_output=True, text=True, shell=True)
    print(f"node --check {js:11}", "OK" if proc.returncode == 0 else proc.stderr.strip()[:300])
