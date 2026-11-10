import pathlib
p=pathlib.Path("v3/W14-story/build_sports.py")
lines=p.read_text(encoding="utf-8").split("\n")
assert lines[340].strip().startswith("new = ("), lines[340][:40]
assert lines[343].strip().startswith("new = new.replace"), lines[343][:40]
q=chr(39)
repl=[
 f'    new = ("{q}<a class=\\\\"btn btn--primary dk-read\\\\" href=\\\\"/sports/{q}"',
 f'           "+SLUG(a.sport)+{q}/\\\\"{q}"Playbooks for "+esc(a.sport)+{q}</a> "',
 f'           "<a class=\\\\"dk-src\\\\" style=\\\\"font-size:13px\\\\" href=\\\\"/story/{q}"',
 f'           "+esc(a.id)+{q}/\\\\"{q}How this played out</a>{q}")',
]
lines[340:344]=repl
p.write_text("\n".join(lines),encoding="utf-8")
print("\n".join(lines[338:346]))
