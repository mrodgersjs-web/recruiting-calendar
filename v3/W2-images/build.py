import json,os
from PIL import Image,ImageDraw,ImageFont
g=json.load(open('src/gen.json'));man=[];thumbs=[]
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
    c.paste(im,((cw-im.width)//2,c.height-im.height),im);return c
for e in g:
    im=Image.open(e['path']); cut=e['file'].startswith('cut')
    if cut: im=key(im)
    im.save('src/%s.png'%e['file'])
    outs=[]
    for W in (640,1080):
        r=im.resize((W,int(im.height*W/im.width)),Image.LANCZOS);f='%s-%d.webp'%(e['file'],W);r.save(f,'WEBP',quality=82);outs.append(f)
    man.append(dict(file=outs,subject=e['subject'],kind=e['type'],label="Illustration",real_person=False,transparent=cut,aspect="9:16" if cut else "%dx%d"%im.size,prompt=e['prompt']))
    thumbs.append((e['file'],im))
json.dump(dict(rule="BRIEF-V3 rule 2: no generated likeness of any real person; every image is a fictional composite or environment, display with 'Illustration' tag top-left.",images=man),open('IMAGES.json','w'),indent=1)
T=300;sh=Image.new('RGB',(T*4+50,(T+30)*4+10),'white');d=ImageDraw.Draw(sh)
for i,(n,im) in enumerate(thumbs):
    t=im.copy();t.thumbnail((T,T));bg=Image.new('RGBA',(T,T),(235,235,235,255));bg.paste(t,((T-t.width)//2,(T-t.height)//2),t.convert('RGBA'))
    x=10+(i%4)*(T+10);y=10+(i//4)*(T+30);sh.paste(bg.convert('RGB'),(x,y));d.text((x,y+T+4),n+"  [Illustration]",fill='black')
sh.save('contact-sheet.png')
