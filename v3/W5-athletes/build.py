import json,os,shutil
from PIL import Image
R=os.path.expanduser('~/Developer/recruiting-calendar')
L=R+'/v3/W5-athletes'; SITE=R+'/site/assets/media'
os.makedirs(L+'/src',exist_ok=True); os.makedirs(L+'/sheet',exist_ok=True)
roster=json.load(open(L+'/ROSTER.json'))['roster']
gen=json.load(open(L+'/src/GEN.json'))
def key(im):
    im=im.convert('RGBA');px=im.load();w,h=im.size
    for y in range(h):
        for x in range(w):
            r,gg,b,a=px[x,y]
            d=gg-max(r,b)
            if d>40: px[x,y]=(r,min(gg,max(r,b)),b,0)
            elif d>12: px[x,y]=(r,max(r,b),b,int(255*(40-d)/28))
    bb=im.getchannel('A').point(lambda v:255 if v>20 else 0).getbbox()
    im=im.crop(bb);cw=max(im.width,int(im.height*9/16));c=Image.new('RGBA',(cw,int(cw*16/9)),(0,0,0,0))
    c.paste(im,((cw-im.width)//2,c.height-im.height),im);return c,bb
man=[]
for e in roster:
    f=e['file']; src=gen[f]
    im=Image.open(src); cut,bb=key(im)
    cut.save(L+'/src/%s.png'%f)
    outs=[]
    for W in (640,1080):
        r=cut.resize((W,int(cut.height*W/cut.width)),Image.LANCZOS)
        p='%s-%d.webp'%(f,W); r.save(L+'/'+p,'WEBP',quality=82)
        shutil.copy(L+'/'+p, SITE+'/%s-%d.webp'%(f.replace('cut-','cut-',1),W) if False else SITE+'/'+p)
        outs.append(p)
    man.append(dict(file=outs,story=e['story'],div=e['div'],subject=e['subject'],kind='composite',
                    label='Illustration',real_person=False,transparent=True,aspect='9:16',prompt=e['body']))
json.dump(dict(rule="BRIEF-V3 rule 2 honoured: no generated likeness of a real named person; every figure is a fictional composite labelled Illustration. Mike 2026-11-06: gear in hand/on, invented near-miss college crest on every jersey.",images=man),
          open(L+'/IMAGES.json','w'),indent=1)
json.dump(man,open(SITE.replace('/assets/media','')+'/IMAGES.json','w').file and open(SITE.replace('/assets/media','')+'/IMAGES.json')) if False else None
print('built',len(man))
