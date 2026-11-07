#!/usr/bin/env python3
"""Local CLI. Reads data/rows.seed.json (or --rows), prints JSON or ICS to stdout. No network, no writes."""
import argparse, json, os, sys
from datetime import date
from personalize import parse_intake, IntakeError, personalize, to_ics

HERE = os.path.dirname(os.path.abspath(__file__))


def main(argv=None):
    ap = argparse.ArgumentParser(description="W10 personalization prototype")
    ap.add_argument("--intake-json", required=True, help="JSON object with exactly the 5 allowed fields")
    ap.add_argument("--rows", default=os.path.join(HERE, "data", "rows.seed.json"))
    ap.add_argument("--today", default=None, help="YYYY-MM-DD (default: system date)")
    ap.add_argument("--format", choices=("json", "ics"), default="json")
    ap.add_argument("--include-stale", action="store_true")
    a = ap.parse_args(argv)
    try:
        today = date.fromisoformat(a.today) if a.today else date.today()
        profile = parse_intake(json.loads(a.intake_json), today_year=today.year)
    except (IntakeError, ValueError) as e:
        sys.stderr.write("intake rejected: %s\n" % e)
        return 2
    try:
        rows = json.load(open(a.rows)).get("rows", [])
    except (OSError, ValueError):
        rows = []   # unreadable data => empty result with reason, never invented rows
    res = personalize(profile, rows, today, include_stale=a.include_stale)
    sys.stdout.write(to_ics(res) if a.format == "ics" else json.dumps(res, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
