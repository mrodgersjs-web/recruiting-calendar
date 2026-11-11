# -*- coding: utf-8 -*-
import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
h = pathlib.Path("head.txt").read_text(encoding="utf-8")
css = re.search(r"<style>(.*?)</style>", h, re.S).group(1)
for rule in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
    sel = re.sub(r"\s+", " ", rule[0]).strip()
    if re.match(r"^(section|\.pagehead|table|thead|tr|td|th|\.lead|h2|h3|ol,|ul|\.box|body|@page|\*|\.tmpl|hr)", sel):
        print("%-42s %s" % (sel, re.sub(r"\s+", " ", rule[1]).strip()))
