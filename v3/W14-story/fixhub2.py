import pathlib,re,sys,ast
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
p=pathlib.Path("v3/W14-story/build_sports.py"); t=p.read_text(encoding="utf-8")
t=t.replace('"have not checked it yet, the page says so plain.</p>",\n',
            '"have not checked it yet, the page says so plain.</p>"\n')
t=t.replace("""'<p class="lede">Pick a sport and you get the playbooks, the dates that come from the '
            "rule, the alerts and the tracker. No story to read first.</p>\"""",
            """'<p class="lede">Pick a sport. You get its playbooks, its dates, and the tools that keep '
            "you on schedule. No story to read first.</p>\"""")
p.write_text(t,encoding="utf-8"); ast.parse(t)
print("comma fixed:", '"have not checked it yet, the page says so plain.</p>"\n' in t)
print("lede fixed:", "you on schedule. No story to read first" in t)
