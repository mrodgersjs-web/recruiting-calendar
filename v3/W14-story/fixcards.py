"""Extract the store cards by walking the grid, not by guessing where it ends."""
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = pathlib.Path(__file__).resolve().parents[2]
p = ROOT / "v3" / "W14-story" / "build_sports.py"
t = p.read_text(encoding="utf-8")

old_start = t.index("CARDS = {}")
old_end = t.index("_js = (SITE")
new_block = '''def store_cards():
    """Cards lifted out of the live store page, so sport pages and the store cannot disagree."""
    grid_at = STORE.find('<div class="pb-grid">')
    depth = 0
    end = len(STORE)
    for m in re.finditer(r"<(/?)div\\b", STORE[grid_at:]):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            end = grid_at + m.end() + len("</div>") - len(">")
            break
    seg = STORE[grid_at:end]
    out = {}
    for chunk in seg.split('<div class="pb-cell">')[1:]:
        # no cell nests another div, so the first close ends it; anything past that
        # is the store's own bundles block and does not belong on a sport page
        body = chunk.split("</div>")[0].strip()
        m = re.search(r'href="?(.*?)\\s|>', body)
        m = re.search(r'href="?(/playbooks/([\\w-]+))', body)
        if m:
            out[m.group(2)] = '<div class="pb-cell">' + body + "</div>"
    return out


CARDS = store_cards()
if not CARDS:
    raise SystemExit("no playbook cards found in the store page")

'''
t = t[:old_start] + new_block + t[old_end:]
p.write_text(t, encoding="utf-8")
import ast
ast.parse(t)
print("block swapped; hand card gone:", "Any sport" not in t[t.index("def store_cards"):t.index("_js = (SITE")])
