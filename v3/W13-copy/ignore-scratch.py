import pathlib
p=pathlib.Path(".gitignore"); t=p.read_text(encoding="utf-8")
add = "\n# W13-copy scratch diagnostics: one-off probes, not part of the lane\nv3/W13-copy/dump*.py\nv3/W13-copy/probe*.py\nv3/W13-copy/insp.py\nv3/W13-copy/rescan.py\nv3/W13-copy/verify.py\nv3/W13-copy/dups.py\nv3/W13-copy/grade2.py\nv3/W13-copy/grade3.py\nv3/W13-copy/ogprobe.py\nv3/W13-copy/livecheck*.py\nv3/W13-copy/equiv*.py\nv3/W13-copy/ghcheck.py\n"
if "W13-copy scratch" not in t:
    p.write_text(t.rstrip() + "\n" + add, encoding="utf-8")
print("gitignore updated")
