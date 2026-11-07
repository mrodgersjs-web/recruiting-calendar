import json,subprocess,os,textwrap
FF=os.path.expanduser('~/.local/bin/ffmpeg'); FONT='/System/Library/Fonts/Avenir Next Condensed.ttc'
LOGO='../W1-brand/logo/png/lockup-stacked-dark.png'
def esc(s): return s.replace('\\','').replace("'","\u2019").replace(':','\\:').replace('%','\\%').replace(',','\\,')
def txt(t,size,y,a,b,color='white',fade=0.4):
    al=f"if(lt(t,{a}),0,if(lt(t,{a+fade}),(t-{a})/{fade},if(lt(t,{b-fade}),1,if(lt(t,{b}),({b}-t)/{fade},0))))"
    yy=f"{y}+30*(1-min(1,max(0,(t-{a})/{fade})))"
    return f"drawtext=fontfile='{FONT}':text='{esc(t)}':fontsize={size}:fontcolor={color}:x=(w-text_w)/2:y='{yy}':alpha='{al}':enable='between(t,{a},{b})'"
def render(name,dur,draws,bg='black'):
    vf=','.join(draws)
    base=['-f','lavfi','-i',f'color=c={bg}:s=1920x1080:r=30:d={dur}']
    fc=f"[0]{vf}[o]"
    out1=f'{name}-1080p.mp4'
    subprocess.run([FF,'-y','-loglevel','error',*base,'-filter_complex',fc,'-map','[o]','-c:v','libx264','-pix_fmt','yuv420p','-crf','26','-preset','slow','-movflags','+faststart','-an',out1],check=True)
    subprocess.run([FF,'-y','-loglevel','error','-i',out1,'-vf','scale=1280:720','-c:v','libx264','-pix_fmt','yuv420p','-crf','27','-movflags','+faststart','-an',f'{name}-720p.mp4'],check=True)
    subprocess.run([FF,'-y','-loglevel','error','-ss',str(dur-1.5),'-i',out1,'-frames:v','1',f'{name}-poster.jpg'],check=True)
    return {'id':name,'duration_s':dur,'files':[out1,f'{name}-720p.mp4',f'{name}-poster.jpg'],'sizes_bytes':{f:os.path.getsize(f) for f in [out1,f'{name}-720p.mp4']}}
man=[]
SCHOOL={'white':'UCCS or the University of Colorado','coward':'Willamette University','rodriguez':'Doane University','butler':'Tyler Junior College or Marquette University'}
# hero: typography only (composite imagery not yet landed)
words=['FOOTBALL','SOFTBALL','VOLLEYBALL','WRESTLING','LACROSSE','TRACK','D1','D2','D3','NAIA','JUCO']
d=[];t=0
for w_ in words: d.append(txt(w_,260,'(h-text_h)/2-60',t,t+1.2,fade=0.2)); t=round(t+1.1,2)
d.append(txt('EVERY PATH IS A STORY.',110,'(h-text_h)/2',t,t+3)); t+=3
dur=round(t+3,1)
pass
S=json.load(open('../W1-stories/STORIES.json'))['stories']
for s in S:
    if s.get('composite'): continue
    d=[];t=0
    d.append(txt(s['name'].upper(),180,'(h-text_h)/2-80',0,4))
    d.append(txt(f"{s['sport']}  /  {s['college']}  /  {s['division']}".upper(),56,'(h-text_h)/2+110',0.4,4))
    t=4
    for f in s['timeline']:
        lines=textwrap.wrap(f['fact'],46)[:4]
        d.append(txt(f['date'],140,'200',t,t+5,color='white@0.5'))
        for i,l in enumerate(lines): d.append(txt(l,72,str(420+i*95),t+0.2*i,t+5))
        src=f['url'].split('/')[2].replace('www.','')
        d.append(txt('Source: '+src+'  (retrieved '+f['retrieved']+')',34,'h-110',t,t+5,color='0xC8C8C8'))
        t+=5
    d.append(txt('No generated likeness. Facts sourced; see story page.',38,'h-80',0,4,color='0xC8C8C8'))
    sch=SCHOOL.get(s['id'],s['college'])
    d.append(txt('Not affiliated with or endorsed by',64,'(h-text_h)/2-140',t,t+4))
    d.append(txt(f"{s['name']} or {sch}.",64,'(h-text_h)/2-50',t,t+4))
    d.append(txt('Facts from public sources, checked 2026-11-05.',52,'(h-text_h)/2+70',t+0.2,t+4))
    t+=4
    r=render('real-'+s['id'],t,d); r['type']='real athlete, kinetic typography, no faces'; r['athlete']=s['name']; man.append(r)
old=json.load(open('manifest.json'));keep=[v for v in old['videos'] if not v['id'].startswith('real-')]
man=keep+[dict(v,end_card='non-affiliation text, no logo',source_line_color='#C8C8C8 on #000 (12.6:1)') for v in man]
json.dump({'generated':'2026-11-05','integrity':'No faces or generated likeness of any real person. Composite story videos pending W2-images and W2-scripts.','videos':man,'pending':old.get('pending',[])},open('manifest.json','w'),indent=1)
