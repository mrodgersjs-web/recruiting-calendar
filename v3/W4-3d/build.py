import json
import numpy as np
from PIL import Image,ImageFilter,ImageDraw
g=json.load(open('src/gen.json'));man=[];cuts=[]
def key(im):
    a=np.asarray(im.convert('RGB')).astype(int);r,gg,b=a[...,0],a[...,1],a[...,2]
    d=gg-np.maximum(r,b);al=np.clip((40-d)/28*255,0,255).astype(np.uint8)
    gg2=np.where(d>12,np.maximum(r,b),gg)
    out=np.dstack([r,gg2,b,al]).astype(np.uint8);im=Image.fromarray(out,'RGBA')
    bb=im.getchannel('A').point(lambda v:255 if v>40 else 0).getbbox();im=im.crop(bb)
    H=int(im.height*1.04);cw=max(im.width+40,int(H*9/16));ch=int(cw*16/9)
    c=Image.new('RGBA',(cw,ch),(0,0,0,0))
    # soft contact shadow ellipse at feet
    sh=Image.new('L',(cw,ch),0);ImageDraw.Draw(sh).ellipse((cw//2-im.width*0.42,ch-int(ch*0.03)-14,cw//2+im.width*0.42,ch-int(ch*0.03)+14),fill=110)
    sh=sh.filter(ImageFilter.GaussianBlur(12));c.paste(Image.new('RGBA',(cw,ch),(0,0,0,255)),(0,0),sh)
    c.alpha_composite(im,((cw-im.width)//2,ch-int(ch*0.03)-im.height));return c
for k,e in g.items():
    c=key(Image.open(e['path']));c.save('src/cut-%s.png'%k);outs=[]
    for W in (640,1080):
        f='cut-%s-%d.webp'%(k,W);c.resize((W,int(W*16/9)),Image.LANCZOS).save(f,'WEBP',quality=84);outs.append(f)
    man.append(dict(file=outs,subject=e['subject'],kind='composite',label='Illustration',real_person=False,transparent=True,aspect='9:16',
      tool='Aside imagegen (photoreal) + PIL chroma key and synthetic contact shadow',license='Generated for RIG; no third-party model or asset; not a real person',prompt=e['prompt']))
    cuts.append(c)
json.dump(dict(rule="BRIEF-V3 rule 2: fictional composites only, label 'Illustration'.",lane='W4-3d',replaces='W2-images cut-* (same filenames)',images=man),open('IMAGES.json','w'),indent=1)
# ring-style strip on white, depth blur on outer
W,H=1800,900;strip=Image.new('RGBA',(W,H),'white');order=[6,4,2,0,1,3,5,7]
for i,idx in enumerate(order):
    c=cuts[idx];dist=abs(i-3.5);s=0.95-0.08*dist;t=c.resize((int(H*s*9/16),int(H*s)))
    if dist>1: t=t.filter(ImageFilter.GaussianBlur(dist*1.5))
    strip.alpha_composite(t,(int(60+i*210-t.width/2+60),H-t.height-20))
ref=Image.open('/Users/rig128gb/.aside/u/0/sessions/2026-11-05_vDWfWwrS181z6OQU/attachments/Screenshot 2026-11-05 at 11.09.59_PM.png').convert('RGB')
ref=ref.resize((int(ref.width*H/ref.height),H))
cmp=Image.new('RGB',(ref.width+W+30,H+50),'white');cmp.paste(ref,(0,50));cmp.paste(strip.convert('RGB'),(ref.width+30,50))
d=ImageDraw.Draw(cmp);d.text((10,15),'TARGET: Nike Try the Look (Mike screenshot)',fill='black');d.text((ref.width+40,15),'W4-3d: 8 composite athletes [Illustration], unbranded apparel',fill='black')
cmp.save('comparison.png')
