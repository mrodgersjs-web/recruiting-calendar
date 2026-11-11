import re, os, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
src = r"C:\Users\Jloeh\.aside\u\1\sessions\2026-11-08_sIbJ63jY5p1sXMzN\tmp\subagent_wait-result-U4rr80F4mrTOi1HD.txt"
t = open(src, encoding="utf-8", errors="replace").read()
out = r"v3\W20-two-sports\research"
os.makedirs(out, exist_ok=True)
parts = re.split(r'<subagent_result task_id="([A-Za-z0-9]+)"', t)
names = {"Xx7BpxpJJXDEx3IZ":"01-wbb-rules","LIjE8EFqN0A9pDWl":"02-wbb-numbers","G40C9m8qw9EH2wnS":"03-fb-rules",
         "hYAxpI9YpeR3PseY":"04-fb-numbers","29RzmzDMYXu8XHNx":"05-film-outreach","3HaKPlvuDEtxmszr":"06-costs",
         "7DgxtT42mfuucNlz":"07-paperwork","dXaQYkofApyIxYKm":"08-men-vs-women"}
n=0
for i in range(1, len(parts), 2):
    tid = parts[i]; body = parts[i+1]
    body = re.sub(r'</subagent_result>\s*', '', body)
    fn = os.path.join(out, names.get(tid, tid) + ".md")
    open(fn, "w", encoding="utf-8").write(body.strip())
    n+=1
    print("%-22s %7d chars  lines=%d" % (os.path.basename(fn), len(body), body.count(chr(10))+1))
