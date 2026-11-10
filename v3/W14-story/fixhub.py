import pathlib,re,sys
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
p=pathlib.Path("v3/W14-story/build_sports.py"); t=p.read_text(encoding="utf-8")

# 1. cards get a whole sentence, not a mid-word cut
t=t.replace('f\'<span class="pb-s">{html.escape(s["blurb"][:110])}</span></a></div>\'',
            'f\'<span class="pb-s">{html.escape(first_sentence(s["blurb"]))}</span></a></div>\'')
t=t.replace('def cards_for(slugs):',
            'def first_sentence(blurb):\n'
            '    """Card text has to end on a sentence, or the page reads as one long run."""\n'
            '    return re.split(r"(?<=\\.)\\s", blurb)[0]\n\n\n'
            'def cards_for(slugs):')

# 2. hub lede and the "why split" paragraph, in short sentences
t=re.sub(r"'<p class=\"lede\">Pick a sport.*?first\.</p>'",
         "'<p class=\"lede\">Pick a sport. You get its playbooks, its dates, and the tools that keep '"
         "\"you on schedule. No story to read first.</p>'\",", t, flags=re.S)
t=re.sub(r'"<p>Contact windows.*?yet\.</p>"',
         '"<p>A football timeline does not fit a softball family. The rules on when a coach can call "\n'
         '            "you differ by sport. So do camp dates, signing dates, and how many spots a team "\n'
         '            "can hand out. So each page lists only what we checked for that sport. Where we "\n'
         '            "have not checked it yet, the page says so plain.</p>",', t, flags=re.S)
p.write_text(t,encoding="utf-8")
import ast; ast.parse(t)
print("first_sentence helper:", "def first_sentence(blurb)" in t)
print("tile uses it:", "first_sentence(s[\"blurb\"])" in t)
print("hub lede swapped:", "No story to read first.</p>'" in t)
print("why-split swapped:", "does not fit a softball family" in t)
