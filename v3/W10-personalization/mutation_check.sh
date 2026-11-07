#!/bin/sh
# Proves the suite can fail: apply each mutation to a COPY, expect the tests to go red.
set -u
SRC="$(cd "$(dirname "$0")" && pwd)"; T="$(mktemp -d)"; fail=0
run() { # name, file, sed-expr
  rm -rf "$T/w"; mkdir "$T/w"; cp -R "$SRC/personalize" "$SRC/tests" "$SRC/data" "$SRC/cli.py" "$T/w/"
  sed -i.bak "$3" "$T/w/$2"; if cmp -s "$T/w/$2" "$T/w/$2.bak"; then echo "MUTATION NOT APPLIED: $1"; fail=1; return; fi
  if (cd "$T/w" && python3 -m unittest discover -s . -t . -p "test_*.py" >/dev/null 2>&1); then echo "SURVIVED (bad): $1"; fail=1; else echo "killed: $1"; fi
}
run "past events no longer hidden"         personalize/freshness.py 's/all(e < today for e in ends)/False/'
run "future read_on trusted"               personalize/freshness.py 's/if read_on > today:/if False:/'
run "stale rows shown"                     personalize/freshness.py 's/if age > window:/if False:/'
run "sport filter off"                     personalize/engine.py 's/if sm is None:/if False:/'
run "vetted label allowed"                 personalize/engine.py 's/PILOT_LABELS = {"listed", "observed", "verified"}/PILOT_LABELS = {"listed","observed","verified","vetted","endorsed"}/'
run "intake accepts extra fields"          personalize/intake.py 's/if extra:/if False:/'
run "full ZIP retained"                    personalize/intake.py 's/return s\[:3\]/return s/'
run "malformed rows shown"                 personalize/engine.py 's/not row.get("url") \\/not row.get("url") and False \\/'
run "unknown price scored zero-cost-free"  personalize/engine.py 's/return "unknown", 4/return "unknown", 15/'
rm -rf "$T"; exit $fail
