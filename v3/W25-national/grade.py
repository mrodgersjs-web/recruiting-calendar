# -*- coding: utf-8 -*-
"""One reading gate for the whole product line: prints the Flesch-Kincaid grade for every
customer deck in one pass, so a national rework cannot quietly raise the reading level."""
import sys, pathlib, importlib.util
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

V3 = pathlib.Path(r"C:\Users\Jloeh\Developer\recruiting-calendar\v3")
spec = importlib.util.spec_from_file_location("readability", V3 / "W20-two-sports" / "readability.py")
rd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rd)

DECKS = [
    ("mens basketball", V3 / "W19-plain/basketball-playbook-plain.html"),
    ("football", V3 / "W20-two-sports/fb-playbook-plain.html"),
    ("girls basketball", V3 / "W20-two-sports/wbb-playbook-plain.html"),
    ("volleyball", V3 / "W24-volleyball/vb-playbook-plain.html"),
]
for label, path in DECKS:
    rd.audit(path, label)
