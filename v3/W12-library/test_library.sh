#!/usr/bin/env bash
# Truth checks for the /library catalog. Run after the build pipeline.
set -u
cd "$(git rev-parse --show-toplevel)"
fail=0
chk(){ if [ "$2" = "$3" ]; then echo "ok   $1"; else echo "FAIL $1 (want '$3' got '$2')"; fail=1; fi; }
[ -f site/library/index.html ]; chk "site/library/index.html exists" "$?" "0"
[ -f site/library/library.json ]; chk "site/library/library.json exists" "$?" "0"
[ ! -e site/resources ]; chk "site/resources is gone" "$?" "0"
for w in McKinley Malbrough MM3 Gumroad gumroad malbrough6; do
  n=$(grep -o "$w" site/library/index.html site/library/library.json site/library/library.js 2>/dev/null | wc -l | tr -d ' ')
  chk "no '$w' in library" "$n" "0"
done
n=$(grep -rIl -E 'McKinley|Malbrough|MM3|Gumroad|malbrough6' site/ 2>/dev/null | wc -l | tr -d ' ')
chk "no attribution words anywhere in site/" "$n" "0"
n=$(grep -o 'href="/library"' site/index.html | wc -l | tr -d ' '); chk "home links /library twice (nav and footer)" "$n" "2"
python3 - <<'PY'
import json,os,sys
d=json.load(open('site/library/library.json')); miss=[]
for it in d['offers']+d['playbooks']+d['free_pages']:
    h=it['href']
    if h.startswith('http'): continue
    p='site'+h.rstrip('/')
    if not (os.path.exists(p+'.html') or os.path.isdir(p) or os.path.exists(p)): miss.append(h)
print(('FAIL broken hrefs: '+' '.join(miss)) if miss else 'ok   every library href resolves on disk')
sys.exit(1 if miss else 0)
PY
[ $? -ne 0 ] && fail=1
grep -q '"/resources"' vercel.json && echo "ok   /resources redirects to /library" || { echo "FAIL no /resources redirect"; fail=1; }
[ "$fail" = 0 ] && { echo "PASS library checks"; exit 0; } || { echo "FAILED library checks"; exit 1; }
