import json,os,shutil
from PIL import Image
R=os.path.expanduser('~/Developer/recruiting-calendar')
L=R+'/v3/W5-athletes'; SITE=R+'/site/assets/media'
roster=json.load(open(L+'/ROSTER2.json'))['roster']; gen=json.load(open(L+'/src2/GEN.json'))
FIX9=['cut-swimmer','cut-baseball','cut-softball','cut-wrestling','cut-volleyball','cut-groenewegen','cut-pichardo','cut-rodenfels','cut-butler']
def key(im):
    im=im.convert('RGBA');px=im.load();w,h=im.size
    for y in range(h):
        for x in range(w):
            r,gg,b,a=px[x,y]
            d=gg-max(r,b)
            if d>40: px[x,y]=(r,min(gg,max(r,b)),b,0)
            elif d>12: px[x,y]=(r,max(r,b),b,int(255*(40-d)/28))
    bb=im.getchannel('A').point(lambda v:255 if v>20 else 0).getbbox()
    im=im.crop(bb)
    cw=max(im.width,int(im.height*9/16)); ch=int(cw*16/9)
    s=min(1.0,(ch*0.88)/im.height)
    if s<1.0: im=im.resize((max(1,int(im.width*s)),max(1,int(im.height*s))),Image.LANCZOS)
    c=Image.new('RGBA',(cw,ch),(0,0,0,0))
    c.paste(im,((cw-im.width)//2,ch-im.height),im)
    return c
tiles=[];smalls=[]
for e in roster:
    f=e['file']
    if f not in FIX9: continue
    cut=key(Image.open(gen[f]))
    cut.save(L+'/src2/%s.png'%f)
    for Wd in (640,1080):
        r=cut.resize((Wd,int(cut.height*Wd/cut.width)),Image.LANCZOS)
        r.save(L+'/%s-%d.webp'%(f,Wd)); shutil.copy(L+'/%s-%d.webp'%(f,Wd),SITE+'/%s-%d.webp'%(f,Wd))
    base=Image.new('RGB',(480,854),(16,18,24)); bg=cut.resize((480,int(cut.height*480/cut.width)),Image.LANCZOS)
    base.paste(bg,(0,854-bg.height),bg); tiles.append(base)
    smalls.append(cut.resize((96,int(cut.height*96/cut.width)),Image.LANCZOS))
    print(f,'figure_h/canvas_h=%.2f'%(cut.getbbox()[3]/cut.height if cut.getbbox() else 0))
def sheet(items,cols,path,th,tw):
    rows=(len(items)+cols-1)//cols
    s=Image.new('RGB',(cols*(tw+8)+8,rows*(th+8)+8),(60,60,70))
    for i,t in enumerate(items): s.paste(t,(8+(i%cols)*(tw+8),8+(i//cols)*(th+8)))
    s.save(path)
sheet(tiles,3,L+'/sheet2/sheet-fix9b-figures.png',854,480)
sheet(smalls,5,L+'/sheet2/sheet-fix9b-cardsize.png',125,84)
