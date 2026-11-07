#!/usr/bin/env python3
"""CLI for the Coach Contact Kit. Local only: prints text, never sends or fetches.
  kit_cli.py script <template> --set key=value ...   render a draft for the athlete to send themselves
  kit_cli.py cadence YYYY-MM-DD                      4 reminder dates
  kit_cli.py window --division D1 --open YYYY-MM-DD [--today ..] [--verified ..]
  kit_cli.py link URL [--minutes N] [--title T] [--first30 yes|no] [--tested yes|no]
  kit_cli.py log-new                                 blank follow-log CSV on stdout
  kit_cli.py log-check FILE [--today ..]             validate + due actions + KPIs
Exit codes: 0 ok, 1 usage/validation failure, 2 input file problem.
"""
import argparse, datetime as dt, json, sys
import contact_kit as ck

def _yn(v):
    return None if v is None else v.lower() in ("yes", "y", "true", "1")

def main(argv=None):
    p = argparse.ArgumentParser(prog="kit_cli")
    sp = p.add_subparsers(dest="cmd", required=True)
    s = sp.add_parser("script"); s.add_argument("template"); s.add_argument("--set", action="append", default=[])
    c = sp.add_parser("cadence"); c.add_argument("first_send")
    w = sp.add_parser("window"); w.add_argument("--division", required=True); w.add_argument("--open")
    w.add_argument("--today"); w.add_argument("--verified")
    l = sp.add_parser("link"); l.add_argument("url"); l.add_argument("--minutes", type=float)
    l.add_argument("--title"); l.add_argument("--first30"); l.add_argument("--tested")
    sp.add_parser("log-new")
    k = sp.add_parser("log-check"); k.add_argument("file"); k.add_argument("--today")
    a = p.parse_args(argv)
    today = getattr(a, "today", None) or dt.date.today().isoformat()
    try:
        if a.cmd == "script":
            if a.template not in ck.TEMPLATES:
                print("unknown template; choose: " + ", ".join(ck.TEMPLATES), file=sys.stderr); return 1
            f = dict(x.split("=", 1) for x in a.set if "=" in x)
            r = ck.render_template(a.template, f)
            print(("Subject: " + r["subject"] + "\n\n" if r["subject"] else "") + r["body"])
            print("\n-- DRAFT ONLY. Athlete sends from their own account, parent copied. --")
        elif a.cmd == "cadence":
            print(json.dumps(ck.cadence(a.first_send), indent=1))
        elif a.cmd == "window":
            print(json.dumps(ck.send_window(a.division, a.open, today, a.verified), indent=1))
        elif a.cmd == "link":
            r = ck.check_video_link(a.url, a.minutes, a.title, None if a.first30 is None else _yn(a.first30),
                                    None if a.tested is None else _yn(a.tested))
            print(json.dumps(r, indent=1)); return 0 if r["ok"] else 1
        elif a.cmd == "log-new":
            sys.stdout.write(ck.blank_log_csv())
        elif a.cmd == "log-check":
            try:
                text = open(a.file, newline="").read()
            except OSError as e:
                print("cannot read: %s" % e, file=sys.stderr); return 2
            v = ck.validate_log(text, today)
            out = {"ok": v["ok"], "errors": v["errors"]}
            if v["ok"]:
                out["due"] = ck.due_actions(v["rows"], today); out["kpis"] = ck.kpis(v["rows"], 14, today)
            print(json.dumps(out, indent=1)); return 0 if v["ok"] else 1
    except (ck.MissingField, ValueError, KeyError) as e:
        print("error: %s" % e, file=sys.stderr); return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
