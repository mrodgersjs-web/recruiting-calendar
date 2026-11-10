import pathlib,sys
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
p=pathlib.Path("v3/W15-pdf/index.py"); t=p.read_text(encoding="utf-8")
old = """    way = "served today" if slug in served else ("email capture only" if c.get("note") else "no PDF wired")"""
new = """    held = c.get("note_text") == "Rules being verified"
    way = "served today" if slug in served else ("button, no file wired" if not held else "email capture only")"""
assert old in t
t = t.replace(old, new)
t = t.replace("""    "3. **The four \\"Rules being verified\\" cards are the honest ones.** `d3-academic-aid-first`,",
    "   `juco-to-d1`, `late-bloomer` and `nil-high-school` show an email capture instead of a button.",
    "   Those are the ones whose rules I have not sourced to a bylaw yet.",""",
"""    "3. **The four \\"Rules being verified\\" cards are the honest ones.** `d3-academic-aid-first`,",
    "   `juco-to-d1`, `late-bloomer` and `nil-high-school` show an email capture instead of a button.",
    "   Those are the ones whose rules I have not sourced to a bylaw yet. `offer-and-signing` carries a",
    "   different note (prices proposed, checkout in test mode, 30-day refund) and still has a button.",""")
p.write_text(t,encoding="utf-8")
print("patched")
