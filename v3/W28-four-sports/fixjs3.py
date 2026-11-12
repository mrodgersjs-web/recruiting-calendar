# -*- coding: utf-8 -*-
"""W28: second storefront audit round, the JavaScript half.

Two auditors looked at the same card and disagreed, which is the useful outcome. The copy
reader found three basketball tells in a traced soccer silhouette and said a parent reads
"that is a basketball player"; the art reader checked the same pixels and said the card now
reads as a woman athlete and not as a missing image. Both are honest reads of one image, and
the image model that would settle it is blocked on this account. So the answer is to say what
it is: the tag on that card becomes SILHOUETTE, its alt text says silhouette, and the caption
stops promising art that is coming for a book that already costs $29.

The rest is what both auditors found together: the desktop rail sold books that are not
written, and my own price fix turned "$0" into "$undefined" because I removed the key from
the data and left the template reading it out loud.

Run from the lane root:
    python fixjs3.py
"""
import pathlib
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = pathlib.Path(__file__).resolve().parent
SITE = HERE.parent.parent / 'site'
DOT = '\u00b7'
swaps = []


def swap(rel, old, new, what):
    swaps.append((rel, old, new, what))


# ---------------------------------------------------------------- ring.js
R = 'assets/ring.js'
swap(R,
     "if(!p)return'Pending';",
     "if(!p)return'In progress';",
     'one phrase for the state, the same on every surface')
swap(R,
     "'Playbook not written yet';",
     "'Playbook in progress';",
     'the rail band says what the shelf says')
swap(R,
     "(STATE(a)==='rewrite'?'Read the playbook':'Playbook not written yet')",
     "(STATE(a)==='rewrite'?'Read the playbook':'Playbook in progress')",
     'and so does the disabled control')
swap(R,
     "const c=a=>a&&a.color||'#1f4d3a';",
     "const c=a=>a&&a.color||'#1f4d3a';\n"
     "  const ok=(p)=>{const r=this.P[p];return !!r&&STATE(r)==='written';};\n"
     "  const kind=(a)=>(a&&a.art_kind==='silhouette')?'Silhouette':'Illustration';",
     'a rail row may only list a book that exists, and the label names the art truthfully')
swap(R,
     "ul.innerHTML=a.playbooks.filter(p=>!!this.P[p])",
     "ul.innerHTML=a.playbooks.filter(ok)",
     'unwritten titles no longer print a price or an Add button')
swap(R,
     "this.querySelector('[data-count]').textContent=a.playbooks.length+' playbooks';",
     "this.querySelector('[data-count]').textContent=a.playbooks.filter(ok).length+' playbooks';",
     'the count above the list counts the rows that exist')
swap(R,
     "${p.price?' " + DOT + " $'+p.price+', one-time':''}",
     "${(p.price&&+p.price>0)?' " + DOT + " $'+p.price+', one-time':''}",
     'no "$undefined" where the data holds no price')
swap(R,
     "const skirt=fem?`<path d=\"M33 70h34l6 23H27z\"/>`:'';",
     "const skirt=fem?`<path d=\"M34 68h32v20h-13v-9h-6v9H34z\"/>`:'';\n"
     " const feet=`<rect x=\"19\" y=\"143\" width=\"13\" height=\"5\" rx=\"2\"/><rect x=\"66\" y=\"143\" width=\"13\" height=\"5\" rx=\"2\"/>`;",
     'the silhouette stops wearing a tunic and grows feet')
swap(R,
     'const ball=/soccer|football/i.test(s)?`<circle cx="76" cy="166" r="10"/>`:\'\';',
     'const ball=/soccer|football/i.test(s)?`<circle cx="84" cy="150" r="11"/><path d="M73 150h22M84 139v22" stroke="#f5f1e8" stroke-width="2" fill="none"/>`:`<circle cx="76" cy="152" r="10"/>`;',
     'the ball rests on the ground beside a foot, panelled when the sport is soccer')
swap(R,
     '<path d="${poses[i%2]}"/>${hair}${skirt}${ball}',
     '<path d="${poses[i%2]}"/>${hair}${skirt}${feet}${ball}',
     'so the figure stands on something')
swap(R,
     'aria-label="Silhouette of ${sp(a&&a.name||"the player")}, a fictional ${altline(a||{})}"',
     'aria-label="${kind(a)} of ${sp(a&&a.name||"the player")}, a fictional ${altline(a||{})}"',
     'the alt text names the kind of art the record actually has')
swap(R,
     'cap.textContent=`${a.name} ' + DOT + ' ${sp(bi.raw)} ' + DOT + ' Illustration. The name is a placeholder; the dates and rules are cited on the page that uses them.`;',
     'cap.textContent=`${a.name} ' + DOT + ' ${sp(bi.raw)} ' + DOT + ' ${kind(a)}. The name is a placeholder; every date and rule is cited on the page that uses it.`;',
     'and so does the caption line beside the figure')

# ---------------------------------------------------------------- deck.js
D = 'assets/deck.js'
swap(D,
     "const PAGE=(a)=>[a.short,a.sport,'Illustration'].filter(Boolean).join(' \\u00b7 ');",
     "const PAGE=(a)=>[a.short,a.sport,((a.art_kind||'')==='silhouette'?'Silhouette':'Illustration')].filter(Boolean).join(' " + DOT + " ');",
     'the phone caption reads SILHOUETTE where the figure is a trace')
swap(D,
     "src='The art is drawn. The name is a placeholder; the dates and rules are cited on the page that uses them.';",
     "src='The figure is traced from a photograph, not a photo of her. The name is a placeholder; every date and rule is cited on the page that uses it.';",
     'a trace is described as a trace')
swap(D,
     "if(WRITTEN(a)){p.push('Illustration coming');t='dk-read dk-soon';}",
     "if(WRITTEN(a)){p.push(((a.art_kind||'')==='silhouette')?'Silhouette':'Illustration');t='dk-read dk-soon';}",
     'a card for a $29 book never says something is coming')
swap(D,
     "aria-label=`Illustration of ${esc(a.name)}, a fictional ${esc(altline(a))}`",
     "aria-label=`${((a.art_kind||'')==='silhouette')?'Silhouette':'Illustration'} of ${esc(a.name)}, a fictional ${esc(altline(a))}`",
     'the phone alt text matches the artwork too')
swap(D,
     "alt=`Illustration of ${esc(a.name)}, a fictional ${esc(altline(a))}`",
     "alt=`${((a.art_kind||'')==='silhouette')?'Silhouette':'Illustration'} of ${esc(a.name)}, a fictional ${esc(altline(a))}`",
     'and the photo alt on the phone deck')

bad = []
for rel, old, new, what in swaps:
    p = SITE / rel
    t = p.read_text(encoding='utf-8')
    n = t.count(old)
    if n == 0:
        bad.append((rel, 'MISSING', old[:60]))
        continue
    if n > 1:
        bad.append((rel, 'AMBIGUOUS x%d' % n, old[:60]))
        continue
    p.write_text(t.replace(old, new, 1), encoding='utf-8')

for rel, why, old in bad:
    print('NOT APPLIED %-16s %-13s %s' % (rel, why, old.replace('\n', ' ')))
print('applied %d of %d' % (len(swaps) - len(bad), len(swaps)))
