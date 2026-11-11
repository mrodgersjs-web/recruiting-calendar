import re,sys,pathlib
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
raw=pathlib.Path(r"C:\Users\Jloeh\.aside\u\1\sessions\2026-11-08_sIbJ63jY5p1sXMzN\artifacts\The-Commit-Book-Basketball-Playbook-SAMPLE.pdf").read_bytes()
print("final pdf bytes:", len(raw), "| pages:", len(re.findall(rb"/Type\s*/Page[^s]", raw)), "| raster images:", len(re.findall(rb"/Subtype\s*/Image", raw)), "| fonts:", len(re.findall(rb"/BaseFont", raw)))
