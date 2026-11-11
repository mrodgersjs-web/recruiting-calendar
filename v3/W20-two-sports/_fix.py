import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
t = open("wbb-plain.py", encoding="utf-8").read()
i = t.index('open("wbb-plain.py", "w"')
open("wbb-plain.py", "w", encoding="utf-8").write(t[:i])
print("trimmed to %d chars, tail:" % i)
print(t[i-120:i])
