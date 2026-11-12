import re,sys,pathlib
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
p=pathlib.Path("v3/W2-playbooks/eligibility-2-hard-deadlines.pdf"); raw=p.read_bytes()
print("images in existing PDF:", len(re.findall(rb"/Subtype\s*/Image", raw)), "| fonts:", sorted({f.decode() for f in re.findall(rb"/BaseFont\s*/([A-Za-z0-9+-]+)", raw)})[:6])
print("generator:", re.findall(rb"/Producer\s*\(([^)]{0,60})", raw)[:2])
