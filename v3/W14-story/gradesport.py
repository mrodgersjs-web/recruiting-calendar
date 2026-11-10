import re, pathlib, sys, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def prose(t):
    t = re.sub(r"<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", t, flags=re.S | re.I)
    t = re.sub(r"<table\b.*?</table>", " ", t, flags=re.S | re.I)
    t = re.sub(r"<nav\b.*?</nav>", " ", t, flags=re.S | re.I)
    t = re.sub(r"<footer\b.*?</footer>", " ", t, flags=re.S | re.I)
    t = re.sub(r"<[^>]*>", " ", t)
    return re.sub(r"\s+", " ", html.unescape(t)).strip()


def mask(t):
    t = re.sub(r"\b\d+(?:[.-]\d+)+\b", " x ", t)
    t = re.sub(r"\b\d{4}-\d{2}-\d{2}\b", " x ", t)
    t = re.sub(r"\b\d{4}-\d{2}\b", " x ", t)
    t = re.sub(r"[·|]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def syl(w):
    w = re.sub(r"[^a-z]", "", w.lower())
    if not w:
        return 0
    n = len(re.findall(r"[aeiouy]+", w))
    if w.endswith("e") and n > 1:
        n -= 1
    return max(1, n)


def fk(text):
    s = re.findall(r"[A-Za-z][A-Za-z'\- ]*[.!?]", text) or [text]
    W = re.findall(r"[A-Za-z][A-Za-z'\-]*", text)
    S = max(len(s), 1)
    return 0 if len(W) < 40 else round(0.39 * len(W) / S + 11.8 * sum(syl(w) for w in W) / len(W) - 15.59, 1)


for p in sorted(pathlib.Path("site/sports").rglob("*.html")):
    body = mask(prose(p.read_text(encoding="utf-8", errors="ignore")))
    url = "/sports/" if p.parent.name == "sports" else f"/sports/{p.parent.name}/"
    W = len(re.findall(r"[A-Za-z][A-Za-z'\-]*", body))
    S = max(len(re.findall(r"[A-Za-z][A-Za-z'\- ]*[.!?]", body)), 1)
    print(f"  {fk(body):5}  {url:26} words={W:4} sentences={S:3} words_per_sentence={W/S:.1f}")
