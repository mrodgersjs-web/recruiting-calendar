import json,os,shutil
from PIL import Image
R=os.path.expanduser('~/Developer/recruiting-calendar')
L=R+'/v3/W5-athletes'; SITE=R+'/site/assets/media'
os.makedirs(L+'/src2',exist_ok=True); os.makedirs(L+'/sheet2',exist_ok=True); os.makedirs(L+'/v1media',exist_ok=True)
roster=json.load(open(L+'/ROSTER2.json'))['roster']
gen=json.load(open(L+'/src2/GEN.json'))
assert len(gen)==21, 'need all 21 v2 prompts generated before keying'
# backup v1 keyed webp once
for p in os.listdir(SITE):
    if p.startswith('cut-') and p.endswith('.webp') and not os.path.exists(L+'/v1media/'+p):
        shutil.copy(SITE+'/'+p, L+'/v1media/'+p)
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
man=[];tiles=[];crests=[];smalls=[]
for e in roster:
    f=e['file']; src=gen[f]
    im=Image.open(src); cut,bb=key(im)
    cut.save(L+'/src2/%s.png'%f)
    outs=[]
    for W in (640,1080):
        r=cut.resize((W,int(cut.height*W/cut.width)),Image.LANCZOS)
        p='%s-%d.webp'%(f,W); r.save(L+'/'+p,'WEBP',quality=82)
        shutil.copy(L+'/'+p, SITE+'/'+p)
        outs.append(p)
    man.append(dict(file=outs,story=e['story'],div=e['div'],subject=e['subject'],kind='composite',
                    label='Illustration',real_person=False,transparent=True,aspect='9:16',prompt=e['body']))
    # audit tiles: 480px on dark site bg, plus 96px card-size strip
    base64=Image.new('RGB',(480,854),(16,18,24)); bg=cut.resize((480,int(cut.height*480/cut.width)),Image.LANCZOS)
    base64.paste(bg,(0,854-bg.height),bg); base64.save(L+'/sheet2/%s.png'%f)
    tiles.append(base64)
    ch=cut.height; chest=cut.crop((int(cut.width*0.25),int(ch*0.28),int(cut.width*0.75),int(ch*0.62)))
    chest.save(L+'/sheet2/crest-%s.png'%f); crests.append(chest)
    sm=cut.resize((96,int(cut.height*96/cut.width)),Image.LANCZOS); smalls.append(sm)
def sheet(items,cols,path,th,tw=None):
    tw=tw or th*9//16; rows=(len(items)+cols-1)//cols
    s=Image.new('RGB',(cols*(tw+8)+8,rows*(th+8)+8),(60,60,70))
    for i,t in enumerate(items):
        s.paste(t.convert('RGB') if t.mode!='RGB' else t,(8+(i%cols)*(tw+8),8+(i//cols)*(th+8)))
    s.save(path)
sheet(tiles,4,L+'/sheet2/sheet-v2-figures.png',854,480)
sheet(crests,6,L+'/sheet2/sheet-v2-crests.png',300)
sheet(smalls,7,L+'/sheet2/sheet-v2-cardsize.png',125,84)
json.dump(dict(rule="v2 after Mike 2026-11-06: jersey on every athlete, large near-miss crest, headroom; gear in hands. Fictional composites only, labelled Illustration.",images=man),
          open(L+'/IMAGES-v2.json','w'),indent=1)
print('built',len(man))
