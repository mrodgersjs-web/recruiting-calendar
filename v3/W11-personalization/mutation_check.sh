#!/bin/sh
# Proves the W11 page tests can fail: mutate a COPY of site/personalize, expect red.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; ROOT="$(cd "$HERE/../.." && pwd)"; T="$(mktemp -d)"; fail=0
run() { # name, file, python-replace old, new
  rm -rf "$T/r"; mkdir -p "$T/r/site" "$T/r/v3"
  cp -R "$ROOT/site/personalize" "$T/r/site/personalize"; cp -R "$ROOT/site/assets" "$T/r/site/assets" 2>/dev/null
  cp -R "$ROOT/v3/W10-personalization" "$T/r/v3/W10-personalization"; cp -R "$HERE" "$T/r/v3/W11-personalization"
  python3 - "$T/r/site/personalize/$2" "$3" "$4" <<'PY'
import sys
p,old,new=sys.argv[1:4]; s=open(p).read()
if old not in s: print("MUTATION NOT APPLIED"); sys.exit(3)
open(p,'w').write(s.replace(old,new,1))
PY
  rc=$?; if [ $rc -ne 0 ]; then echo "MUTATION NOT APPLIED: $1"; fail=1; return; fi
  if (cd "$T/r/v3/W11-personalization" && python3 test_personalize_page.py >/dev/null 2>&1); then echo "SURVIVED (bad): $1"; fail=1; else echo "killed: $1"; fi
}
run "past rows no longer hidden"        personalize.js 'ends.every(function (e) { return e < today; })' 'false'
run "future read_on trusted"            personalize.js 'if (readOn > today)' 'if (false)'
run "sport filter off"                  personalize.js 'if (sm === null)' 'if (false)'
run "vetted label allowed"              personalize.js 'var PILOT_LABELS = ["listed", "observed", "verified"]' 'var PILOT_LABELS = ["listed", "observed", "verified", "vetted"]'
run "intake accepts extra fields"       personalize.js 'if (extra.length)' 'if (false)'
run "full ZIP retained"                 personalize.js 'return s.slice(0, 3); // full ZIP never retained' 'return s;'
run "ICS uses bare LF"                  personalize.js 'lines.join("\r\n") + "\r\n"' 'lines.join("\n") + "\n"'
run "ICS DTEND inclusive"               personalize.js 'ymd(e0 + DAY)' 'ymd(e0)'
run "seed drifts from W10"              seed.json '"usd": 75' '"usd": 76'
run "PII field added to form"           index.html '<label class="pz-check">' '<label>Child name<input id="f-child" type="text"></label><label class="pz-check">'
run "email input type added"            index.html 'id="f-budget" type="number"' 'id="f-budget" type="email"'
run "badge shows Vetted"                personalize.ui.js 'return it.highest_label === "verified" ? "Verified" : "Listed";' 'return it.highest_label === "verified" ? "Verified" : "Vetted";'
run "ui posts data"                     personalize.ui.js 'credentials: "omit"' 'credentials: "omit", method: "POST"'
run "intake sends extra field"          personalize.ui.js 'goal_level: GOAL_FOR_CATEGORY' 'goal_level: GOAL_FOR_CATEGORY, dob: "x"'
run "checklist drops insurance"         personalize.ui.js '"Insurance"' '"Gear"'
rm -rf "$T"; exit $fail
