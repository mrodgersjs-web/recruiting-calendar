import re,pathlib,sys
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
def main(p):
    t=pathlib.Path(p).read_text(encoding="utf-8")
    return t[t.find("<main"):t.find("</main>")+7]
t=main("site/playbooks/index.html")
i=t.find("Football: Junior Year")
print("=== store card region ===")
print(re.sub(r"\s+"," ",t[max(0,i-700):i+700]))
print("\n=== rules index: sport links ===")
r=main("site/rules/index.html")
print("\n".join(sorted(set(re.findall(r'href="?(/rules/[\w/-]+)',r)))))
print("\n=== price page: tiers/what you get ===")
pr=main("site/price/index.html")
print(re.sub(r"<[^>]+>"," ",pr).replace("  "," ")[:1500])
