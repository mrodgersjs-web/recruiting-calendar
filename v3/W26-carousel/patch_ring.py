# -*- coding: utf-8 -*-
"""W26: the four finished playbooks lead the athlete ring; every other sport is
greyed, stamped PENDING and cannot be clicked. Mike's call, 11 Nov 2026.

Edits site/assets/ring.js, site/assets/ring.css and the cache-busting query strings
in site/index.html. Every replacement is asserted, so a changed anchor fails loudly
instead of half-patching. Run with --dry to only check the anchors.
"""
import hashlib
import pathlib
import re
import sys

SITE = pathlib.Path(__file__).resolve().parents[2] / "site"
JSF = SITE / "assets" / "ring.js"
CSSF = SITE / "assets" / "ring.css"
HTMLF = SITE / "index.html"

js = JSF.read_text(encoding="utf-8")
css = CSSF.read_text(encoding="utf-8")
html = HTMLF.read_text(encoding="utf-8")


def sub(text, old, new, label):
    if old not in text and new in text:
        print("  already applied: %s" % label)
        return text
    if text.count(old) != 1:
        sys.exit("FAIL %s: anchor found %d times\n%s" % (label, text.count(old), old[:200]))
    return text.replace(old, new, 1)


HELPERS = """
// The four written playbooks lead the ring (Mike, 11 Nov 2026). Every other sport
// renders greyed, is stamped PENDING and does nothing when clicked until its own
// product is built. Order: women's volleyball, men's football, men's basketball,
// women's basketball, then the rest of the written sports, then the pending sports.
var FRONT_IDS=["composite-volleyball","composite-football","derrick","composite-wbasketball"];
var WOMENS_BB={"composite-wbasketball":1,"samantha":1};
function builtInfo(a){
 var s=String(a.sport||"").toLowerCase();
 if(s.indexOf("volleyball")>-1)return{built:true,label:"Women's Volleyball"};
 if(s.indexOf("football")>-1)return{built:true,label:"Men's Football"};
 if(s.indexOf("basketball")>-1)return{built:true,label:WOMENS_BB[a.id]?"Women's Basketball":"Men's Basketball"};
 return{built:false,label:a.sport};
}
function isPending(a){return!builtInfo(a).built}
function orderBuilt(list){
 var L=list.slice(),first=[],live=[],pend=[];
 FRONT_IDS.forEach(function(id){for(var i=0;i<L.length;i++){if(L[i].id===id){first.push(L[i]);L.splice(i,1);return}}});
 for(var j=0;j<L.length;j++){(isPending(L[j])?pend:live).push(L[j])}
 return first.concat(live,pend);
}
"""

# 1. helpers, straight after the SPORT_PATH line -------------------------------------
head = "function SPORT_PATH(a){"
if "function builtInfo(" not in js:
    i = js.index(head)
    nl = js.index("\n", i)
    js = js[:nl] + "\n" + HELPERS.strip() + js[nl:]

# 2. sort the athletes, start on the first written sport ------------------------------
js = sub(
    js,
    "const D=window.STORY_DATA;this.A=D.athletes;this.P=D.playbooks;",
    "const D=window.STORY_DATA;this.A=orderBuilt(D.athletes);this.P=D.playbooks;",
    "athletes sorted",
)
js = sub(
    js,
    "const s0=Math.max(0,this.A.findIndex(a=>a.id==='composite-football'&&a.img)),s1=s0>=0&&this.A[s0]?.composite?s0:Math.max(0,this.A.findIndex(a=>a.composite&&a.img));",
    "const s0=Math.max(0,this.A.findIndex(a=>a.composite&&a.img&&!isPending(a))),s1=s0>=0?s0:0;",
    "start index",
)

# 3. the card: built label, and the stamp across the athlete --------------------------
OLD_CARD = 'const cardHTML=(a,i)=>`<span class="card__shadow"></span><span class="card__art">${a.img?`<img src="${a.img}" alt="Illustration of a fictional ${sp(a.sport)} athlete" loading="eager" decoding="async">`:``}</span><span class="card__lbl">Illustration</span> <span class="card__meta"><div class="card__name">${escA(a.short)}</div><div class="card__line">${a.sport}</div></span>`;'
NEW_CARD = 'const cardHTML=(a,i)=>{const bi=builtInfo(a);return `<span class="card__shadow"></span><span class="card__art">${a.img?`<img src="${a.img}" alt="Illustration of a fictional ${sp(a.sport)} athlete" loading="eager" decoding="async">`:``}</span><span class="card__lbl">Illustration</span>${bi.built?``:`<span class="card__pend">Pending</span>`} <span class="card__meta"><div class="card__name">${escA(a.short)}</div><div class="card__line">${sp(bi.label)}</div></span>`};'
js = sub(js, OLD_CARD, NEW_CARD, "card html")

# 4. cards in the ring and in the front (hero) slot -----------------------------------
js = sub(
    js,
    'el.innerHTML=`<button class="card" data-go="${b}" tabindex="-1" aria-label="${escA(a.name)}">${cardHTML(a,b%n)}</button>`;',
    'el.innerHTML=`<button class="card${isPending(a)?\' is-pending\':\'\'}" data-go="${b}" tabindex="-1" aria-label="${escA(a.name)}">${cardHTML(a,b%n)}</button>`;',
    "ring card class",
)
js = sub(
    js,
    'h.innerHTML=`<button class="card" data-view="${i}" tabindex="-1" aria-label="${escA("Playbooks for " + (a.sport||"this sport") + ": " + a.name)}">${cardHTML(a,i)}</button>`;',
    'h.innerHTML=`<button class="card${isPending(a)?\' is-pending\':\'\'}" data-view="${i}" tabindex="-1" aria-label="${escA((isPending(a)?"Pending, not open yet. Playbook for ":"Playbooks for ") + (builtInfo(a).label||"this sport") + ": " + a.name)}">${cardHTML(a,i)}</button>`;',
    "hero card class",
)

# 5. the tick strip ------------------------------------------------------------------
OLD_TICK = '''<button class="sr__tick" data-tick="${i}" aria-label="Path ${i+1}: ${a.sport}"><span class="sr__bar"></span><span class="sr__tlabel">${String(i+1).padStart(2,'0')}<span class="sr__tname">&nbsp;&nbsp;${a.sport}</span></span></button>'''
NEW_TICK = '''<button class="sr__tick${isPending(a)?' is-pend':''}" data-tick="${i}" aria-label="${isPending(a)?"Pending: "+a.sport:"Path "+(i+1)+": "+builtInfo(a).label}"><span class="sr__bar"></span><span class="sr__tlabel">${String(i+1).padStart(2,'0')}<span class="sr__tname">&nbsp;&nbsp;${isPending(a)?'Pending':builtInfo(a).label}</span></span></button>'''
js = sub(js, OLD_TICK, NEW_TICK, "ticks")

# 6. helper line under the title -----------------------------------------------------
js = sub(
    js,
    '<p class="sr__sub">Pick a sport. Drag to browse. Click one to open the playbooks and dates for that sport.</p>',
    '<p class="sr__sub">Pick a sport. Drag to browse. Click one to open the playbooks and dates for that sport. Grey cards are sports whose playbooks are still being written.</p>',
    "helper copy",
)

# 7. live region, who-line, sport button ---------------------------------------------
js = sub(
    js,
    "if(!silent)this.querySelector('[data-live]').textContent=`Path ${this.index+1}: ${a.sport}`;",
    "if(!silent)this.querySelector('[data-live]').textContent=isPending(a)?`Pending: ${a.sport}`:`Path ${this.index+1}: ${builtInfo(a).label}`;",
    "live region",
)
js = sub(
    js,
    "this.querySelector('[data-who]').textContent=`${a.short} \u00b7 ${a.sport} \u00b7 Illustration. The name is a placeholder; the dates and rules are cited on the page that uses them.`;",
    "this.querySelector('[data-who]').textContent=isPending(a)?`${a.short} \u00b7 ${a.sport}. This playbook is still being written, so it is not open yet.`:`${a.short} \u00b7 ${builtInfo(a).label} \u00b7 Illustration. The name is a placeholder; the dates and rules are cited on the page that uses them.`;",
    "who line",
)
js = sub(
    js,
    "var _rd=this.querySelector('[data-read]');_rd.textContent='Playbooks for '+a.sport+' \\u2192';_rd.onclick=()=>location.href=SPORT_PATH(a);",
    "var _rd=this.querySelector('[data-read]');_rd.disabled=isPending(a);_rd.textContent=isPending(a)?'Playbook pending':'Playbooks for '+builtInfo(a).label+' \\u2192';_rd.onclick=isPending(a)?null:()=>location.href=SPORT_PATH(a);",
    "read button",
)

# 8. keyboard reach, and the two click paths -----------------------------------------
js = sub(
    js,
    "h.querySelector('.card').tabIndex=j===this.index?0:-1",
    "h.querySelector('.card').tabIndex=(j===this.index&&!isPending(this.A[j]))?0:-1",
    "tab order",
)
js = sub(
    js,
    "if(b=t.closest('[data-view]'))return location.href=SPORT_PATH(this.A[+b.dataset.view]);",
    "if(b=t.closest('[data-view]')){const va=this.A[+b.dataset.view];if(isPending(va))return;return location.href=SPORT_PATH(va)}",
    "hero click",
)
js = sub(
    js,
    "if(b=t.closest('[data-go]')){const k=this.rank(+b.dataset.go);",
    "if(b=t.closest('[data-go]')){if(isPending(this.A[(+b.dataset.go)%this.n]))return;const k=this.rank(+b.dataset.go);",
    "ring card click",
)
js = sub(
    js,
    "if(e.key==='Enter'&&e.target===st)location.href=SPORT_PATH(this.A[this.index])",
    "if(e.key==='Enter'&&e.target===st&&!isPending(this.A[this.index]))location.href=SPORT_PATH(this.A[this.index])",
    "enter key",
)
js = sub(
    js,
    "const view=!this.dragging&&e.target.closest('[data-view]'),link=!this.dragging&&e.target.closest('[data-go]');",
    "const view=!this.dragging&&e.target.closest('[data-view]:not(.is-pending)'),link=!this.dragging&&e.target.closest('[data-go]:not(.is-pending)');",
    "cursor states",
)

# 9. styles --------------------------------------------------------------------------
EXTRA = """
/* Pending sports: greyed out, stamped across the athlete, not clickable (W26). */
.card.is-pending{cursor:default}
.card.is-pending .card__art{filter:grayscale(1) brightness(.95) contrast(.85);opacity:.55}
.card.is-pending .card__name,.card.is-pending .card__line,.card.is-pending .card__div,.card.is-pending .card__lbl{opacity:.45}
.card__pend{position:absolute;left:-10%;right:-10%;top:36%;z-index:4;padding:11px 0;text-align:center;font:700 clamp(17px,2.1vw,28px)/1 var(--font-display);letter-spacing:.24em;text-transform:uppercase;color:#fff;background:rgba(17,17,17,.66);border-top:2px solid #fff;border-bottom:2px solid #fff;transform:rotate(-14deg);pointer-events:none}
.sr__tick.is-pend{opacity:.42}
.sr__tick.is-pend .sr__bar::after{background:var(--muted)}
.sr__cta[disabled]{background:var(--muted);cursor:default}
"""
if ".card__pend" not in css:
    css = css.rstrip() + "\n" + EXTRA

# 10. honest cache keys --------------------------------------------------------------
REFS = [
    ("/checkout.js", "0c590745", SITE / "checkout.js"),
    ("/assets/commit.css", "6ac59abf", SITE / "assets" / "commit.css"),
    ("/assets/ring.css", "79a5ec3a", None),
    ("/assets/deck.css", "d43c6a09", SITE / "assets" / "deck.css"),
    ("/assets/stories.js", "54a73737", SITE / "assets" / "stories.js"),
    ("/assets/ring.js", "5db6b2b3", None),
    ("/assets/deck.js", "ccef33c0", SITE / "assets" / "deck.js"),
]
new_html = html
for url, old, path in REFS:
    if url == "/assets/ring.css":
        data = css.encode("utf-8")
    elif url == "/assets/ring.js":
        data = js.encode("utf-8")
    else:
        data = path.read_bytes()
    new = hashlib.md5(data).hexdigest()[:8]
    if old == new:
        continue
    pat = re.compile(re.escape(url) + r"\?v=" + re.escape(old))
    if not pat.search(new_html):
        pat = re.compile(re.escape(url) + r"\?v=[0-9a-f]{8}")
        if not pat.search(new_html):
            print("  note: %s is not referenced in index.html" % url)
            continue
    new_html = pat.sub(url + "?v=" + new, new_html, count=1)
    print("  cache key %s %s -> %s" % (url, old, new))

if "--dry" in sys.argv:
    print("dry run: every anchor found")
else:
    JSF.write_bytes(js.encode("utf-8"))
    CSSF.write_bytes(css.encode("utf-8"))
    HTMLF.write_text(new_html, encoding="utf-8")
    print("wrote ring.js, ring.css, index.html")
