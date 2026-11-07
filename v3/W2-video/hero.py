import subprocess,os
FF=os.path.expanduser('~/.local/bin/ffmpeg'); FONT='/System/Library/Fonts/Avenir Next Condensed.ttc'
I='../W2-images/'; T='/tmp/w2v/'; os.makedirs(T,exist_ok=True)
def r(*a): subprocess.run([FF,'-y','-loglevel','error',*a],check=True)
scenes=[('baseball','field-dawn','BASEBALL'),('softball','field-dawn','SOFTBALL'),('swimmer','pool','SWIMMING'),('volleyball','gym','VOLLEYBALL'),('wbasketball','gym','BASKETBALL'),('football','field-dawn','FOOTBALL'),('wrestling','gym','WRESTLING'),('sprinter','track','TRACK')]
D=3.0; segs=[]
lab=f"drawtext=fontfile='{FONT}':text='ILLUSTRATION':fontsize=30:fontcolor=white:box=1:boxcolor=black@0.6:boxborderw=12:x=40:y=40"
for i,(c,e,w) in enumerate(scenes):
    o=f'{T}h{i}.mp4'
    fc=(f"[0]scale=2133:1200,crop=1920:1080:x='106*t/{D}':y=60,eq=brightness=-0.12[bg];"
        f"[bg]drawtext=fontfile='{FONT}':text='{w}':fontsize=300:fontcolor=white@0.9:x=(w-text_w)/2-'150*t/{D}':y=h-text_h-60[b2];"
        f"[1]scale=-1:1000,format=rgba[c];[b2][c]overlay=x='(W-w)/2+120-60*t/{D}':y=H-h+20,{lab},fade=in:st=0:d=0.3,fade=out:st={D-0.3}:d=0.3[o]")
    r('-loop','1','-t',str(D),'-r','30','-i',I+f'env-{e}-1080.webp','-loop','1','-t',str(D),'-r','30','-i',I+f'cut-{c}-1080.webp','-filter_complex',fc,'-map','[o]','-c:v','libx264','-pix_fmt','yuv420p','-crf','24',o); segs.append(o)
o=T+'hend.mp4'
r('-f','lavfi','-i','color=c=black:s=1920x1080:r=30:d=3.5','-loop','1','-t','3.5','-r','30','-i','../W1-brand/logo/png/lockup-stacked-dark.png','-filter_complex',
  f"[1]scale=700:-1[l];[0][l]overlay=(W-w)/2:(H-h)/2-40,drawtext=fontfile='{FONT}':text='EVERY PATH IS A STORY.':fontsize=60:fontcolor=white:x=(w-text_w)/2:y=h-200,fade=in:st=0:d=0.4,fade=out:st=3.1:d=0.4[o]",'-map','[o]','-c:v','libx264','-pix_fmt','yuv420p','-crf','24',o); segs.append(o)
open(T+'list.txt','w').write(''.join(f"file '{s}'\n" for s in segs))
r('-f','concat','-safe','0','-i',T+'list.txt','-c:v','libx264','-pix_fmt','yuv420p','-crf','27','-preset','slow','-movflags','+faststart','-an','hero-loop-1080p.mp4')
r('-i','hero-loop-1080p.mp4','-vf','scale=1280:720','-c:v','libx264','-pix_fmt','yuv420p','-crf','28','-movflags','+faststart','-an','hero-loop-720p.mp4')
r('-ss','4.5','-i','hero-loop-1080p.mp4','-frames:v','1','hero-loop-poster.jpg')
