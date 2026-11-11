import pathlib, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = pathlib.Path("head.txt"); t = p.read_text(encoding="utf-8")
old = ".box, .tmpl, table, ul, ol, dl, blockquote, .two, h2, h3, .pagehead, .split {"
new = ".box, .tmpl, table, ul, ol, dl, blockquote, .two, .lead, h2, h3, .pagehead, .split {"
print("patched" if old in t else "MISSING")
p.write_text(t.replace(old, new), encoding="utf-8")
