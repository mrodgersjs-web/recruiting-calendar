"""W9: render /athlete/<id>/ authored parent experiences. Imports page() etc from build_site by exec-ing its header only."""
import json,os,re,html,glob
R=os.path.expanduser('~/Developer/recruiting-calendar');SITE=R+'/site';L=R+'/v3/W9-experiences'
e=html.escape
import time;VER=time.strftime('%m%d%H%M')
src=open(R+'/v3/W2-site/build_site.py').read()
hdr=src.split('# HOME')[0]          # imports, CSS/HDR/FTR, seo(), page(), w()
exec(hdr)
INP=json.load(open(L+'/INPUT.json'));OF=INP['offers'];ATH={a['id']:a for a in INP['athletes']}
IMG=json.load(open(L+'/IMAGES.json')) if os.path.exists(L+'/IMAGES.json') else {}
CSS2='''<style>
.ax{background:#0b0b0c;color:#f4f4f2}
.ax-hero{min-height:88vh;display:grid;align-items:end;position:relative;overflow:hidden;padding:0 6vw 8vh}
.ax-hero img.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.55}
.ax-hero .fig{position:absolute;right:6vw;bottom:0;height:86%;width:auto;filter:drop-shadow(0 20px 40px #000)}
.ax-hero .txt{position:relative;max-width:820px}
.ax-hero h1{font:400 clamp(44px,8vw,120px)/.9 var(--font-display,Impact);text-transform:uppercase;margin:.2em 0}
.ax-dek{font-size:20px;line-height:1.5;max-width:640px;color:#d7d7d2}
.ax-ch{display:grid;grid-template-columns:1.1fr 1fr;gap:5vw;padding:12vh 6vw;border-top:1px solid #222;align-items:center}
.ax-ch:nth-child(even) .ax-pic{order:-1}
.ax-pic{position:relative;aspect-ratio:16/10;overflow:hidden;border-radius:4px;background:#161616}
.ax-pic img.sc{width:100%;height:100%;object-fit:cover;opacity:.7}.ax-pic img.cut{position:absolute;bottom:0;left:50%;transform:translateX(-50%);height:96%;width:auto;filter:drop-shadow(0 12px 24px #000)}
.ax-k{font:600 12px/1 Arial;letter-spacing:.16em;text-transform:uppercase;color:#e0473d}
.ax-ch h2{font:400 clamp(32px,4.4vw,64px)/.95 var(--font-display,Impact);text-transform:uppercase;margin:.3em 0 .5em}
.ax-ch h3{font:600 12px/1 Arial;letter-spacing:.14em;text-transform:uppercase;color:#8a8a86;margin:1.6em 0 .5em}
.ax-ch p{font-size:18px;line-height:1.6;color:#e2e2de;margin:0}
.ax-offer{display:flex;justify-content:space-between;gap:12px;align-items:center;margin-top:1.6em;padding:14px 16px;border:1px solid #333;border-radius:4px;color:#fff;text-decoration:none}
.ax-offer b{font-size:16px}.ax-offer span{color:#aaa;font-size:14px}
.ax-src{font-size:13px;color:#8a8a86;margin-top:1em}.ax-src a{color:#bbb}
.ax-six{padding:12vh 6vw;border-top:1px solid #222}
.ax-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:32px}
.ax-card{border:1px solid #333;border-radius:4px;padding:22px;color:#fff;text-decoration:none;display:flex;flex-direction:column;gap:10px;min-height:180px}
.ax-card .p{margin-top:auto;font-size:15px;color:#ccc}.ax-card .soon{color:#e0a43d}
.tag-ill2{position:absolute;top:12px;left:12px;background:#000c;color:#fff;font:600 10px/1 Arial;letter-spacing:.14em;text-transform:uppercase;padding:6px 8px}
@media(max-width:800px){.ax-ch{grid-template-columns:1fr;padding:8vh 6vw}.ax-ch:nth-child(even) .ax-pic{order:0}.ax-grid{grid-template-columns:1fr}.ax-hero .fig{opacity:.35;right:-10vw}}
</style>'''

import os as _os
def chfig(a,i,pic,cutimg):
    f=f'{SITE}/assets/media/ch-{a["id"]}-{i}.webp'
    if _os.path.exists(f):
        return f'<figure class="ax-pic"><img class="sc" style="opacity:1" src="/assets/media/ch-{a["id"]}-{i}.webp?v={VER}" alt="Illustration: {e(a["sport"].lower())} scene" loading="lazy"><span class="tag-ill2">Illustration</span></figure>'
    return f'<figure class="ax-pic"><img class="sc" src="{pic}" alt="" loading="lazy">{cutimg}<span class="tag-ill2">Illustration</span></figure>'
def offer_line(s):
    o=OF[s];soon='notify' in o['status']
    price='Free' if o['price']==0 else f'${o["price"]}'
    href=f'/playbooks/{s}' if o['kind']=='playbook' else f'/tools/{s}'
    return href,price,soon
def page_for(x):
    a=ATH[x['id']];comp=a['composite']
    im=IMG.get(x['id'],{})
    hero_bg=im.get('hero') or '/assets/media/env-field-dawn-1080.webp'
    fig=f'<img class="fig" src="{a["img"].replace("-640","-1080")}?v={VER}" alt="Illustration of a fictional {e(a["sport"].lower())} athlete{"" if comp else ", not "+e(a["name"])}">' if a.get('img') else ''
    cutimg=(f'<img class="cut" src="{a["img"].replace("-640","-1080")}?v={VER}" alt="" loading="lazy">' if a.get('img') else '')
    chs=''
    for i,c in enumerate(x['chapters']):
        pic=(im.get('chapters') or [None]*20)[i] if i<len(im.get('chapters') or []) else None
        pic=pic or hero_bg
        off=''
        if c.get('offer') in OF:
            href,price,soon=offer_line(c['offer'])
            off=f'<a class="ax-offer" href="{href}"><b>{e(OF[c["offer"]]["title"])}</b><span>{price}{" · coming soon" if soon else ""}</span></a>'
        srcl=f'<p class="ax-src">Source: <a href="{e(c["source_url"])}" rel="noopener">{e(re.sub(r"^https?://(www\\.)?","",c["source_url"]).split("/")[0])}</a></p>' if c.get('source_url') else ''
        chs+=f'''<section class="ax-ch"><div><p class="ax-k">{e(c.get("kicker",""))}</p><h2>{e(c["title"])}</h2>
<h3>What was happening</h3><p>{e(c["what_was_happening"])}</p>
<h3>{"What they did" if comp else "If your family is here today"}</h3><p>{e(c["what_they_did"])}</p>
<h3>How it helps</h3><p>{e(c["how_it_helps"])}</p>{off}{srcl}</div>
{chfig(a,i,pic,cutimg)}</section>'''
    cards=''
    for s in x['offers']:
        href,price,soon=offer_line(s);o=OF[s]
        cards+=f'<a class="ax-card" href="{href}"><span class="ax-k">{"Playbook" if o["kind"]=="playbook" else "Tool"}</span><b>{e(o["title"])}</b><span class="p{" soon" if soon else ""}">{price}{" · coming soon" if soon else ""}</span></a>'
    disc='' if comp else f'<p class="note" style="color:#888">Real athlete. Facts from public sources, each linked. {e(a["name"])} and their family did not use The Commit Book; the steps shown are what a family in the same spot can do today. Not affiliated with or endorsed by {e(a["name"])} or {e(a["college"] or "")}.</p>'
    body=f'''<main class="ax">
<section class="ax-hero"><img class="bg" src="{hero_bg}" alt="">{fig}<span class="tag-ill2">Illustration</span>
<div class="txt"><p class="ax-k">{e(a["sport"])} · {e(a["div"])} · {"Composite story" if comp else "Real athlete"}</p><h1>{e(x["headline"])}</h1><p class="ax-dek">{e(x["dek"])}</p>{disc}</div></section>
{chs}
<section class="ax-six"><p class="ax-k">Six tools for this path</p><h2 class="d1" style="color:#fff">What a family on this road uses.</h2><p class="ax-dek">{e(x.get("closing",""))} None of these caused this athlete's result, and none can promise yours.</p><div class="ax-grid">{cards}</div>
<p style="margin-top:32px"><a class="btn btn--primary btn--l" href="/story/{a["id"]}">Read the sourced timeline</a> <a class="btn btn--outline" href="/">All stories</a></p></section></main>'''
    w(f'athlete/{a["id"]}/index.html',page(f'/athlete/{a["id"]}/',f'{x["headline"]} | The Commit Book',x['dek'],body,CSS2,'','ax-page'))
# /tools/<slug>: notify-only pages (W8 drafts are in review; never sold or downloadable here)
for s,o in OF.items():
    if o['kind']!='tool':continue
    li=''.join(f'<li>{e(c)}</li>' for c in o.get('contents',[]))
    body=f'''<main class="cb-page pdp"><p class="lab">Tool · coming soon</p><h1 class="d2">{e(o["title"])}</h1><p class="pb-p">{"Free" if o["price"]==0 else "$"+str(o["price"])} <span class="note">planned price</span></p>
<p>This tool is being written and checked. It is not for sale yet. Leave your email and we will tell you when it is ready.</p>
<details open><summary>Planned contents</summary><ul>{li}</ul></details>
<form class="capture" data-src="notify-{s}" novalidate><input type="email" name="email" required placeholder="Your email" aria-label="Your email" autocomplete="email"><input type="hidden" name="plan" value="giveaway"><input type="hidden" name="source" value="notify-{s}"><input class="hp" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true"><button class="btn btn--primary" type="submit">Notify me</button><label class="consent"><input type="checkbox" name="consent" value="1"> Email me when this tool is ready. Unsubscribe any time.</label></form><p class="note f5">For parents and guardians. We do not knowingly collect information from children under 13.</p></main>'''
    w(f'tools/{s}/index.html',page(f'/tools/{s}/',f'{o["title"]} (coming soon) | The Commit Book',o['title'],body))
n=0
for f in sorted(glob.glob(L+'/out/*.json')):
    x=json.load(open(f));assert len(set(x['offers']))>=6 and all(s in OF for s in x['offers']),f;page_for(x);n+=1
print('athlete pages',n)

# patch story pages with the parent-walkthrough link (idempotent)
import glob as _g, re as _re
for _f in _g.glob('site/story/*/index.html'):
    _id=_f.split('/')[-2]; _s=open(_f).read()
    if f'href="/athlete/{_id}"' in _s or not __import__('os').path.isdir(f'site/athlete/{_id}'): continue
    _n=_s.replace('<a class="btn btn--outline" href="/">Keep reading stories</a>', f'<a class="btn btn--outline" href="/athlete/{_id}">The parent walkthrough</a> <a class="btn btn--outline" href="/">Keep reading stories</a>',1)
    if _n!=_s: open(_f,'w').write(_n)
