import sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
t = pathlib.Path("fb-plain.py").read_text(encoding="utf-8")
print("===== HEAD 1-60 =====")
print("\n".join(t.split("\n")[:58]))
i = t.find("SECTIONS") if "SECTIONS" in t else t.find('HTML =')
print("===== ASSEMBLY TAIL =====")
print("\n".join(t.split("\n")[-42:]))
