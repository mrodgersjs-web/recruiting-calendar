import pathlib
p=pathlib.Path("v3/W14-story/build_sports.py")
lines=p.read_text(encoding="utf-8").split("\n")
i=next(k for k,l in enumerate(lines) if l.strip().startswith("new = ("))
j=next(k for k,l in enumerate(lines) if l.strip()=="t = t.replace(old, new)")
print("replacing lines",i+1,"to",j)
for k,l in enumerate(lines[i:j]): print("   ",i+1+k,l)
lines[i:j]=['    new = pathlib.Path(__file__).with_name("deck-cta.txt").read_text(encoding="utf-8").strip()']
p.write_text("\n".join(lines),encoding="utf-8")
import ast; ast.parse(p.read_text(encoding="utf-8")); print("parses OK")
