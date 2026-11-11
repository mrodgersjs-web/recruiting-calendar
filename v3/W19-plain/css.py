import pathlib, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = pathlib.Path(r"v3\W18-bball-pdf\bball-pdf.py")
t = p.read_text(encoding="utf-8")
pairs = [
 ("font:400 10.4pt/1.5", "font:400 10pt/1.46"),
 ("td{padding:1.6mm 2mm;border-bottom:1px solid var(--rule);vertical-align:top;font-size:9.4pt}",
  "td{padding:1.15mm 1.8mm;border-bottom:1px solid var(--rule);vertical-align:top;font-size:9.05pt}"),
 ("tr.sub td{border-bottom:1.5px solid var(--ink);font-size:8.8pt", "tr.sub td{border-bottom:1.5px solid var(--ink);font-size:8.5pt"),
 ("td.o{width:16%;font-size:8.8pt", "td.o{width:16%;font-size:8.5pt"),
 ("td.n{width:30%;font-size:8.8pt", "td.n{width:30%;font-size:8.5pt"),
 (".box{border:1px solid var(--ink);background:var(--paper);padding:3.5mm 4mm;margin:0 0 3.5mm}",
  ".box{border:1px solid var(--ink);background:var(--paper);padding:2.8mm 3.4mm;margin:0 0 3mm}"),
 ("p{margin:0 0 2.4mm}", "p{margin:0 0 2mm}"),
 ("ul.tight li,ol.tight li{margin-bottom:1.2mm}", "ul.tight li,ol.tight li{margin-bottom:.9mm}"),
 ("h2{font-size:15pt;margin:0 0 2mm;padding-top:3mm", "h2{font-size:14.4pt;margin:0 0 1.6mm;padding-top:2.4mm"),
 (".tmpl{font:400 9.2pt/1.45", ".tmpl{font:400 8.9pt/1.42"),
 (".lead{font-size:11.6pt", ".lead{font-size:11.1pt"),
 (".check{font-size:9.5pt", ".check{font-size:9.2pt"),
 ("table{width:100%;border-collapse:collapse;margin:2mm 0 3mm}", "table{width:100%;border-collapse:collapse;margin:1.6mm 0 2.4mm}"),
]
hit = 0
for a, b in pairs:
    if a in t:
        t = t.replace(a, b); hit += 1
    else:
        print("  miss:", a[:60])
p.write_text(t, encoding="utf-8")
print("css rules tightened:", hit, "of", len(pairs))
