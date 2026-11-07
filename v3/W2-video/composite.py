import json,subprocess,os,textwrap
FF=os.path.expanduser('~/.local/bin/ffmpeg'); FP=FF.replace('ffmpeg','ffprobe'); FONT='/System/Library/Fonts/Avenir Next Condensed.ttc'
I='../W2-images/'; T='/tmp/w2v/c/'; os.makedirs(T,exist_ok=True)
def r(*a): subprocess.run([FF,'-y','-loglevel','error',*a],check=True)
def esc(s): return s.replace("'","\u2019").replace(':','\\:').replace('%','\\%').replace(',','\\,')
S=[s for s in json.load(open('composite-swim-short.json'))['stories'] if s.get('composite')]
out=[]
for s in S:
  sp={'Swimming':('swimmer','pool')}.get(s['sport'],('swimmer','pool'))
  plates=[sp[1],'dorm-desk',sp[1],'gym','dorm-desk',sp[1]]
  segs=[]
  for i,b in enumerate(s['beats']):
    d=len(b['text'].split())/2.6+0.6
    lines=textwrap.wrap(b['text'],62); n=len(lines); per=d/max(1,(n+1)//2)
    cap=[]
    for k in range(0,n,2):
      st=per*(k//2); en=st+per
      for j,l in enumerate(lines[k:k+2]):
        cap.append(f"drawtext=fontfile='{FONT}':text='{esc(l)}':fontsize=46:fontcolor=white:box=1:boxcolor=black@0.55:boxborderw=10:x=(w-text_w)/2:y=h-200+{j*62}:enable='between(t,{st:.2f},{en:.2f})'")
    head=f"drawtext=fontfile='{FONT}':text='{esc(b['beat'].replace('_',' ').upper())}':fontsize=40:fontcolor=white@0.7:x=w-text_w-40:y=40"
    lab=f"drawtext=fontfile='{FONT}':text='ILLUSTRATION':fontsize=30:fontcolor=white:box=1:boxcolor=black@0.6:boxborderw=12:x=40:y=40"
    pl=plates[i%len(plates)]
    fc=(f"[0]scale=2133:1200,crop=1920:1080:x='106*t/{d:.2f}':y=60,eq=brightness=-0.18[bg];[1]scale=-1:900,format=rgba[c];"
        f"[bg][c]overlay=x='W-w-80-40*t/{d:.2f}':y=H-h,{head},{lab},{','.join(cap)},fade=in:st=0:d=0.3,fade=out:st={d-0.3:.2f}:d=0.3[v]")
    o=T+f"{s['id']}-{i}.mp4"
    r('-loop','1','-t',f'{d:.2f}','-r','30','-i',I+f'env-{pl}-1080.webp','-loop','1','-t',f'{d:.2f}','-r','30','-i',I+f'cut-{sp[0]}-1080.webp','-f','lavfi','-t',f'{d:.2f}','-i','anullsrc=r=48000:cl=stereo',
      '-filter_complex',fc,'-map','[v]','-map','2:a','-af','apad','-t',f'{d:.2f}','-c:v','libx264','-pix_fmt','yuv420p','-crf','22','-c:a','aac','-ar','48000',o); segs.append(o)
  e=T+f"{s['id']}-end.mp4"
  r('-f','lavfi','-i','color=c=black:s=1920x1080:r=30:d=4','-f','lavfi','-i','anullsrc=r=48000:cl=stereo','-filter_complex',
    f"[0]drawtext=fontfile='{FONT}':text='EVERY PATH IS A STORY.':fontsize=90:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2-60,drawtext=fontfile='{FONT}':text='{esc(s['label'])}. Illustrations, not a real person.':fontsize=34:fontcolor=0xC8C8C8:x=(w-text_w)/2:y=h-160[v]",
    '-map','[v]','-map','1:a','-t','4','-c:v','libx264','-pix_fmt','yuv420p','-c:a','aac','-ar','48000',e); segs.append(e)
  open(T+'l.txt','w').write(''.join(f"file '{x}'\n" for x in segs))
  n=s['id']
  r('-f','concat','-safe','0','-i',T+'l.txt','-c:v','libx264','-pix_fmt','yuv420p','-crf','24','-c:a','aac','-movflags','+faststart',f'{n}-1080p.mp4')
  r('-i',f'{n}-1080p.mp4','-vf','scale=1280:720','-c:v','libx264','-pix_fmt','yuv420p','-crf','25','-c:a','copy','-movflags','+faststart',f'{n}-720p.mp4')
  r('-ss','3','-i',f'{n}-1080p.mp4','-frames:v','1',f'{n}-poster.jpg')
  dur=float(subprocess.run([FP,'-v','error','-show_entries','format=duration','-of','csv=p=0',f'{n}-1080p.mp4'],capture_output=True,text=True).stdout)
  out.append({'id':n,'duration_s':round(dur,1),'beats':len(s['beats']),'words':sum(len(b['text'].split()) for b in s['beats']),'narration':'NONE: macOS say -o writes empty 4 KB aiff and ffmpeg has no flite filter; captioned, silent audio track','script':'composite-swim-short.json','files':[f'{n}-1080p.mp4',f'{n}-720p.mp4',f'{n}-poster.jpg']})
print(json.dumps(out))
m=json.load(open('manifest.json'))
m['videos']=[v for v in m['videos'] if not v['id'].startswith('composite')]+[dict(v,type='composite story, captioned (no narration), Illustration-labeled, ~200 words') for v in out]
for v in m['videos']:
  if v['id']=='hero-loop': v.update(type='hero silent loop: 8 composite cut-outs (baseball, softball, swimmer, volleyball, wbasketball, football, wrestling, sprinter) on plates, Illustration overlay, logo end card',duration_s=27.5,sizes_bytes={f:os.path.getsize(f) for f in ['hero-loop-1080p.mp4','hero-loop-720p.mp4']})
m['pending']=[]
json.dump(m,open('manifest.json','w'),indent=1)
