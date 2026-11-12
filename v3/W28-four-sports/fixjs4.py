# -*- coding: utf-8 -*-
"""W28: the tag, the alt text and the caption name the art the record actually has.

The first pass of this patch reported ten swaps as MISSING because it guessed at the
minified text. This one was written from the lines printed out of the files. Line numbers
are printed alongside every change so a later reader can find them again.

Run from the lane root:
    python fixjs4.py
"""
import pathlib
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = pathlib.Path(__file__).resolve().parent
SITE = HERE.parent.parent / 'site'
DOT = '\u00b7'

KIND_FN = ("const KIND=(a)=>(a&&(a.art_kind==='silhouette'))?'Silhouette':'Illustration';")

pairs = [
    # ---- ring.js -------------------------------------------------------
    ('assets/ring.js',
     "const PEND=(a)=>STATE(a)==='rewrite'?'New edition in progress':'Not written yet';",
     KIND_FN + "\nconst PEND=(a)=>STATE(a)==='rewrite'?'New edition in progress':'Playbook in progress';",
     'one phrase for the state everywhere, and a helper that names the art'),
    ('assets/ring.js',
     'aria-label="${kind(a)} of',
     'aria-label="${KIND(a)} of',
     'the helper, spelled as it is defined'),
    ('assets/ring.js',
     'const ball=/soccer|football/i.test(s)?`<circle cx="84" cy="150" r="11"/><path d="M73 150h22M84 139v22" stroke="#f5f1e8" stroke-width="2" fill="none"/>`:`<circle cx="76" cy="152" r="10"/>`;',
     'const ball=/soccer|football/i.test(s)?`<circle cx="84" cy="150" r="11"/><path d="M73 150h22M84 139v22" stroke="#f5f1e8" stroke-width="2" fill="none"/>`:\'\';',
     'a wrestler and a swimmer do not hold a ball'),
    ('assets/ring.js',
     'const cardHTML=(a,i)=>{const bi=builtInfo(a);',
     'const cardHTML=(a,i)=>{const bi=builtInfo(a);const kd=KIND(a);',
     'the card carries its art kind once'),
    ('assets/ring.js',
     'alt="Illustration of ${escA(a.short)}, a fictional ${altline(a)}"',
     'alt="${kd} of ${escA(a.short)}, a fictional ${altline(a)}"',
     'the desktop alt text'),
    ('assets/ring.js',
     '</span><span class="card__lbl">Illustration</span>',
     '</span><span class="card__lbl">${kd}</span>',
     'the tag on the desktop card'),
    ('assets/ring.js',
     "'${a.short} " + DOT + " ${builtInfo(a).label} " + DOT + " Illustration. The name is a placeholder; the dates and rules are cited on the page that uses them.'",
     "'${a.short} " + DOT + " ${builtInfo(a).label} " + DOT + " ${KIND(a)}. The name is a placeholder; every date and rule is cited on the page that uses it.'",
     'the caption beside the figure'),
    ('assets/ring.js',
     '`${a.short} ' + DOT + ' ${builtInfo(a).label} ' + DOT + ' Illustration. The name is a placeholder; the dates and rules are cited on the page that uses them.`',
     '`${a.short} ' + DOT + ' ${builtInfo(a).label} ' + DOT + ' ${KIND(a)}. The name is a placeholder; every date and rule is cited on the page that uses it.`',
     'the caption beside the figure, template form'),
    ('assets/ring.js',
     '// two cues that still read at 300 pixels: hair tied back, and a skirt that flares',
     '// two cues that still read at 300 pixels: hair tied back, and shorts cut wide at the',
     'the comment says what the figure now wears'),
    ('assets/ring.js',
     '// where the legs hang straight. A ball at the feet names the sport, because a',
     '// hem. A ball at the feet names the sport, because a',
     'the comment, second line'),
    # ---- deck.js -------------------------------------------------------
    ('assets/deck.js',
     "  function ALTL(a){var s=String((a&&a.sport)||'').toLowerCase(),n=NOUN(s);return n==='player'?s+' '+n:n}",
     "  function ALTL(a){var s=String((a&&a.sport)||'').toLowerCase(),n=NOUN(s);return n==='player'?s+' '+n:n}\n"
     "  function KIND(a){return (a&&a.art_kind==='silhouette')?'Silhouette':'Illustration'}",
     'the same helper on the phone side'),
    ('assets/deck.js',
     "alt=\"Illustration of '+esc(a.short)+', a fictional '",
     "alt=\"'+KIND(a)+' of '+esc(a.short)+', a fictional '",
     'the phone alt text'),
    ('assets/deck.js',
     "decoding=\"async\"><span class=\"tag-ill\">Illustration</span>",
     "decoding=\"async\"><span class=\"tag-ill\">'+KIND(a)+'</span>",
     'the tag on the phone card, photo branch'),
    ('assets/deck.js',
     "<span class=\"tag-ill\">'+(WRITTEN(a,P)?'Illustration coming':'Playbook in progress')+'</span>",
     "<span class=\"tag-ill\">'+(WRITTEN(a,P)?KIND(a):'Playbook in progress')+'</span>",
     'a written book never says the art is coming'),
]

done = 0
for rel, old, new, what in pairs:
    p = SITE / rel
    t = p.read_text(encoding='utf-8')
    n = t.count(old)
    if n != 1:
        print('SKIP (%d matches) %s :: %s' % (n, rel, what))
        continue
    p.write_text(t.replace(old, new, 1), encoding='utf-8')
    done += 1
print('applied %d of %d' % (done, len(pairs)))

for rel in ('assets/ring.js', 'assets/deck.js'):
    t = (SITE / rel).read_text(encoding='utf-8')
    print('%-16s lines %3d  kind helpers %d  bare Illustration literals %d'
          % (rel, t.count('\n') + 1, t.count('KIND'), len([x for x in ['>Illustration<', "'Illustration coming'", 'Illustration of'] if x in t])))
