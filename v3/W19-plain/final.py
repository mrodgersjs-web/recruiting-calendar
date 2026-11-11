import re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
raw = open(r"C:\Users\Jloeh\.aside\u\1\sessions\2026-11-08_sIbJ63jY5p1sXMzN\artifacts\The-Commit-Book-Basketball-Playbook-SAMPLE.pdf","rb").read()
print("pages:", len(re.findall(rb"/Type\s*/Page[^s]", raw)), "| embedded fonts:", len(re.findall(rb"/BaseFont", raw)), "| raster images:", len(re.findall(rb"/Subtype\s*/Image", raw)))
txt = open(r"C:\Users\Jloeh\Developer\recruiting-calendar\v3\W19-plain\customer-text.txt", encoding="utf-8").read()
for probe in ["40 to 55", "wish, not a working plan", "position-group", "went sideways", "programme", "defence", "counsellor", "Amateurism", "amateurism check"]:
    print("  %-24s %s" % (probe, "present" if probe.lower() in txt.lower() else "gone"))
