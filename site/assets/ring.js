function SPORT_PATH(a){var s=String(a.sport||'').toLowerCase();if(s.indexOf('track')>-1)return'/sports/track-field/';if(s.indexOf('swim')>-1)return'/sports/swimming/';if(s.indexOf('lacrosse')>-1)return'/sports/lacrosse/';return '/sports/'+s.split(/[\s(/]+/)[0]+'/';}
// <story-ring>: 3D ring carousel engine (mechanics per Runway spec s7-9), athlete-card content model.
(()=>{
const RM=matchMedia('(prefers-reduced-motion: reduce)').matches;
const K=95,C=2*Math.sqrt(K),STEP_N=12,SPEED=5000;
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
const wrapPi=p=>{p=p%(2*Math.PI);if(p>Math.PI)p-=2*Math.PI;if(p<=-Math.PI)p+=2*Math.PI;return p};
const sil=(i)=>{const poses=['M50 8a9 9 0 1 1 0 18a9 9 0 1 1 0-18zM38 30h24l6 50-8 2-4-30-2 50 6 64h-11l-7-56-7 56H24l6-64-2-50-4 30-8-2z','M50 6a9 9 0 1 1 0 18a9 9 0 1 1 0-18zM36 28h28l14 30-8 4-10-18 2 46 4 68h-11l-9-58-9 58H26l4-68 2-46-10 18-8-4z'];
 return `<svg viewBox="0 0 100 180" aria-hidden="true"><path fill="#111" d="${poses[i%2]}"/></svg>`};
const sp=(s)=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const cardHTML=(a,i)=>`<span class="card__shadow"></span><span class="card__art">${a.img?`<img src="${a.img}" alt="${a.composite?'Illustration of a fictional composite '+sp(a.sport)+' athlete':'Illustration of a fictional '+sp(a.sport)+' athlete, not '+sp(a.short)}" loading="eager" decoding="async">`:`<span class="card__poster"><b>${a.sport}</b><i>${a.short}</i></span>`}</span><span class="card__lbl">${a.composite?'Illustration · Composite':(a.art_fictional?'Illustration · not '+a.short:'Real athlete · sourced')}</span>
<span class="card__meta"><span class="card__div">${a.div}</span><div class="card__name">${a.short}</div><div class="card__line">${a.sport}<br>${a.from} → ${a.college}</div></span>`;
class StoryRing extends HTMLElement{
connectedCallback(){
 const D=window.STORY_DATA;this.A=D.athletes;this.P=D.playbooks;const n=this.n=this.A.length;
 this.N=n*Math.ceil(8/n);this.index=0;this.target=0;this.cur=RM?0:-1.15;this.vel=0;this.still=false;
 this.playing=false;this.engaged=false;this.panelHover=false;this.dragging=false;this.visible=false;
 this.bag=new Set(JSON.parse(localStorage.getItem('playbook-bag-v1')||'[]'));
 const s0=Math.max(0,this.A.findIndex(a=>a.id==='composite-football'&&a.img)),s1=s0>=0&&this.A[s0]?.composite?s0:Math.max(0,this.A.findIndex(a=>a.composite&&a.img));this.target=s1;this.cur=RM?s1:s1-1.15;
 this.render();this.querySelectorAll('img').forEach(i=>{i.loading='eager';if(i.decode)i.decode().catch(()=>{})});this.classList.add('js');this.bind();this.measure();this.setIndex(s1,true);
 const io=new IntersectionObserver(e=>{this.visible=e[0].isIntersecting;if(this.visible)this.kick()},{threshold:0});io.observe(this);
 const rv=new IntersectionObserver(e=>{if(e[0].isIntersecting){rv.disconnect();requestAnimationFrame(()=>requestAnimationFrame(()=>{this.classList.add('is-revealed');this.kick()}))}},{rootMargin:'0px 0px -22% 0px'});
 if(RM)this.classList.add('is-revealed');else rv.observe(this);
 if(!RM&&innerWidth>749)this.play(true);this.updBag();
}
render(){
 const A=this.A,n=this.n;
 this.innerHTML=`<div class="sr__grid"><div class="sr__left"><div class="sr__head"><h2 class="sr__title">Pick a path.</h2>
<p class="sr__sub">Real roads to a college roster. Different sports, states, school sizes and divisions. Drag to browse. Click one to see the playbooks and dates for that sport.</p><p class="sr__sub sr__surv">Most college athletes don't go pro. These stories show how athletes got to college, not what happened after.</p><span class="sr__sr" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)" aria-live="polite" data-live></span></div>
<div class="sr__stage" tabindex="0" role="region" aria-roledescription="carousel" aria-label="Athlete stories. Use arrow keys or swipe."><div class="sr__actors"></div><div class="sr__heroes"></div><span class="sr__sweep"></span>
<span class="sr__cursor"><span class="sr__cursor-in"><span class="c-drag">Drag</span><span class="c-view">View</span></span></span><span class="sr__walk"></span></div>
<div class="sr__controls"><button class="sr__icon sr__prev" aria-label="Previous athlete"><svg width="26" height="14" viewBox="0 0 26 14" fill="none" stroke="currentColor" stroke-width="1.3"><path d="M25 7H1M7 1L1 7l6 6"/></svg></button>
<div class="sr__ticks">${A.map((a,i)=>`<button class="sr__tick" data-tick="${i}" aria-label="Path ${i+1}: ${a.sport}"><span class="sr__bar"></span><span class="sr__tlabel">${String(i+1).padStart(2,'0')}<span class="sr__tname">&nbsp;&nbsp;${a.sport}</span></span></button>`).join('')}</div>
<button class="sr__icon sr__auto" aria-pressed="false" aria-label="Autoplay"><svg class="i-play" width="14" height="14" viewBox="0 0 24 24"><path fill="currentColor" d="M7 4.5v15l12.5-7.5z"/></svg><svg class="i-pause" width="14" height="14" viewBox="0 0 24 24"><path fill="currentColor" d="M6.5 4.5h3.5v15H6.5zM14 4.5h3.5v15H14z"/></svg></button>
<button class="sr__icon sr__next" aria-label="Next athlete"><svg width="26" height="14" viewBox="0 0 26 14" fill="none" stroke="currentColor" stroke-width="1.3"><path d="M1 7h24M19 1l6 6-6 6"/></svg></button></div></div>
<aside class="sr__panel"><div class="sr__pinner"><div class="sr__phead"><h3 class="sr__ptitle">In this story</h3><span class="sr__lab" data-count></span></div><div class="sr__who" data-who></div>
<ul class="sr__items" data-items></ul><div class="sr__bundle"><button class="sr__cta" data-read>See the playbooks →</button><p class="sr__note" data-bagline></p></div></div></aside></div>`;
 const act=this.querySelector('.sr__actors'),her=this.querySelector('.sr__heroes');
 this.bodies=[];for(let b=0;b<this.N;b++){const a=A[b%n];const el=document.createElement('div');el.className='sr__body';el.setAttribute('aria-hidden','true');
  el.innerHTML=`<button class="card" data-go="${b}" tabindex="-1" aria-label="${a.name}">${cardHTML(a,b%n)}</button>`;act.appendChild(el);this.bodies.push({el,a:b,w:0,blur:-1,x:b})}
 this.heroes=A.map((a,i)=>{const h=document.createElement('div');h.className='sr__hero';h.innerHTML=`<button class="card" data-view="${i}" tabindex="-1" aria-label="Read story: ${a.name}">${cardHTML(a,i)}</button>`;her.appendChild(h);return h});
 this.stage=this.querySelector('.sr__stage');this.cursor=this.querySelector('.sr__cursor');this.ticks=[...this.querySelectorAll('.sr__tick')];
}
measure(){
 const mob=innerWidth<=749;this.mob=mob;
 if(mob){if(!this.vh||Math.abs(innerHeight-this.vh)>=160||this.vw!==innerWidth){this.vh=innerHeight;this.vw=innerWidth}this.style.setProperty('--frame-h',Math.round(this.vh*.66)+'px')}
 else{const hh=document.querySelector('.site-header')?.offsetHeight||0;this.style.setProperty('--frame-h',Math.max(380,innerHeight-hh)+'px')}
 const r=this.stage.getBoundingClientRect();this.W=r.width;this.H=r.height;
 this.fs=mob?1:1.08;const mh=mob?Math.max(200,Math.round((this.H-24-18)*.9)):Math.max(200,Math.round((this.H-34-18)/1.08));
 this.stage.style.setProperty('--model-h',Math.min(mh,mob?mh:620)+'px');
 const hx=mob?.5*this.W:.5*this.W,hy=mob?22:34;this.stage.style.setProperty('--hx',hx+'px');this.stage.style.setProperty('--hy',hy+'px');this.stage.style.setProperty('--fs',this.fs);
 this.bodies.forEach(s=>s.w=s.el.offsetWidth);this.unit=mob?Math.max(90,this.W*.32*1.6):Math.max(120,.3*this.W);
 if(this.mobPrev!==undefined&&this.mobPrev!==mob)this.bodies.forEach(s=>{s.x=this.wrapN(s.a-this.target);s.g=s.x;s.v=0});this.mobPrev=mob;this.kick();
}
wrapN(v){const N=this.N;return((v%N)+N)%N}
put(s,x,bottom,scale,op,blur,z){
 if(this.mob)blur=blur<.6?0:Math.min(blur,1);const hw=s.w*scale/2;if(x+hw<-4||x-hw>this.W+4)op=0;
 const e=s.el;e.style.transform=`translate3d(${x.toFixed(2)}px,${(-bottom).toFixed(2)}px,0) translateX(-50%) scale(${scale.toFixed(4)})`;
 e.style.opacity=op.toFixed(3);e.style.zIndex=z;e.style.visibility=op<.01?'hidden':'visible';e.style.pointerEvents=op<.5?'none':'auto';
 const b=Math.round(blur*10)/10;if(b!==s.blur){s.blur=b;e.style.filter=b>.05?`blur(${b}px)`:''}
 if(!this.mob){const m=e.querySelector('.card__meta');if(m){const front=scale>=.99*(this.fs||1)&&b<.3;const v=front?1:0;if(s.mv!==v){s.mv=v;m.style.opacity=v;m.style.visibility=v?'visible':'hidden'}}}
}
renderRing(){
 const W=this.W,H=this.H,cx=.5*W,R=.62*W,P=1.05*W,floor=H-34,hor=.36*H,step=2*Math.PI/this.N;
 for(const s of this.bodies){const phi=wrapPi((s.a-this.cur)*step),z=R*(1-Math.cos(phi)),persp=P/(P+z),sl=Math.abs(phi)/step;
  const scale=persp*(1+(this.fs-1)*clamp(1-sl,0,1)),x=cx+R*Math.sin(phi)*persp,feet=hor+(floor-hor)*persp;
  const blur=sl<=1?1.8*sl:Math.min(1.8+(sl-1)*2,6.5);let op=clamp((Math.cos(phi)+.55)/.3,0,1);if(this.still&&sl<.02)op=0;
  this.put(s,x,H-feet,scale,op,blur,Math.round(scale*1000))}
}
stepClassic(dt){
 let moving=false;const N=this.N;
 for(const s of this.bodies){const goal=this.wrapN(s.a-this.target);if(s.goal===undefined){s.goal=goal;s.g=goal+(RM?0:1.15);s.x=s.g;s.v=0}
  const raw=s.a-this.target,uw=raw-N*Math.round((raw-s.x)/N);
  if(this.dragging||s.unw){if(Math.abs(goal-s.goal)>N/2)s.unw=true;s.trip=false;s.goal=goal;
   s.g+=(uw-s.g)*(1-Math.exp(-dt/(this.dragging?.016:.06)));
   if(!this.dragging&&Math.abs(s.x-uw)<.02&&Math.abs(s.v)<.05){const d=goal-uw;s.x+=d;s.g=goal;s.unw=false}}
  else{if(Math.abs(goal-s.goal)>N/2){s.trip=true;s.from=s.x}s.goal=goal;
  const tau=s.trip?.1:.03+.04*Math.min(goal,4);s.g+=(goal-s.g)*(1-Math.exp(-dt/tau));}
  const h=dt/3;for(let i=0;i<3;i++){const acc=-K*(s.x-s.g)-C*s.v;s.v+=acc*h;s.x+=s.v*h}
  if(!s.unw&&Math.abs(s.x-goal)<.0006&&Math.abs(s.v)<.0006){s.x=goal;s.v=0;s.g=goal}else moving=true;
  if(s.trip&&Math.abs(s.x-goal)<.02)s.trip=false}
 return moving;
}
renderClassic(){
 const W=this.W,ax=.5,ay=22,sx=this.mob?.46:.30,sy=22,sr=this.mob?.62:.76,ex=.55,d=4;
 for(const s of this.bodies){let k=s.x,e=-1;
  if(s.trip){const u=clamp(Math.abs(s.x-s.from)/Math.max(1e-6,Math.abs(s.goal-s.from)),0,1);
   if(s.goal>s.from){if(u<.5)e=2*u*1.4;else k=s.goal+2*(1-u)}else{if(u<.5)k=s.from+2*u;else e=2*(1-u)*1.4}}
  else if(k<0)e=Math.min(-k,1.4);
  if(e>=0){this.put(s,W*(ax-ex*e),ay-22*e,1+.14*e,Math.max(0,1-1.05*e),this.mob?0:4*Math.min(e,1),1100);continue}
  let op=k<=d-1?1-.13*k:Math.max(0,.61*(4-k));if(this.mob&&k<=1.05)op=1;else if(this.mob&&k<=d-1)op=Math.max(op,.9-.08*k);if(this.still&&k<.02)op=0;
  this.put(s,W*(ax+sx*k),ay+sy*k,Math.pow(sr,k),op,this.mob?0:Math.min(.9*k,3.2),1000-Math.round(10*k))}
}
kick(){if(!this.raf&&this.visible&&!document.hidden){this.last=0;this.raf=requestAnimationFrame(t=>this.frame(t))}}
frame(t){
 this.raf=0;const dt=this.last?Math.min(.034,(t-this.last)/1000):1/60;this.last=t;
 (window.__ft=window.__ft||[]).push(t);if(window.__ft.length>600)window.__ft.shift();
 let moving;
 if(this.mob){moving=this.stepClassic(dt)||this.dragging}
 else{const h=dt/3;for(let i=0;i<3;i++){const acc=-K*(this.cur-this.target)-C*this.vel;this.vel+=acc*h;this.cur+=this.vel*h}
  moving=!(Math.abs(this.cur-this.target)<=.0005&&Math.abs(this.vel)<=.0005)||this.dragging;if(!moving){this.cur=this.target;this.vel=0}}
 this.setStill(!moving);this.mob?this.renderClassic():this.renderRing();
 if(moving){this.raf=requestAnimationFrame(t=>this.frame(t))}
}
setStill(v){if(v===this.still)return;this.still=v;this.classList.toggle('is-still',v)}
rank(b){if(this.mob)return this.wrapN(b-this.target);let k=((b-Math.round(this.target))%this.N+this.N)%this.N;if(k>this.N/2)k-=this.N;return k}
setIndex(i,silent){
 const old=this.index;this.index=((i%this.n)+this.n)%this.n;this.kick();
 this.bodies.forEach(s=>{const k=this.rank(s.a),on=k!==0&&Math.abs(k)<=(this.mob?3:2);s.el.querySelector('.card').tabIndex=on?0:-1;s.el.setAttribute('aria-hidden',String(!on))});
 if(!silent&&old===this.index)return;
 const a=this.A[this.index];this.style.setProperty('--progress',((this.index+1)/this.n).toFixed(3));
 this.heroes.forEach((h,j)=>{h.classList.toggle('is-on',j===this.index);h.querySelector('.card').tabIndex=j===this.index?0:-1});
 if(!silent&&!RM){this.stage.classList.remove('is-sweep');void this.stage.offsetWidth;this.stage.classList.add('is-sweep')}
 if(!silent)this.querySelector('[data-live]').textContent=`Path ${this.index+1}: ${a.sport}`;
 this.ticks.forEach((t,j)=>{t.setAttribute('aria-current',String(j===this.index));t.classList.toggle('is-past',j<this.index)});
 this.renderPanel(silent);this.restartBar();
}
renderPanel(silent){
 const a=this.A[this.index],ul=this.querySelector('[data-items]');
 this.querySelector('[data-count]').textContent=a.playbooks.length+' playbooks';
 this.querySelector('[data-who]').textContent=`${a.short} · ${a.sport} · ${a.div}`+(a.composite?` · ${a.label}`:` · Public facts only, sourced in the story. ${a.name} is not affiliated with, has not endorsed, and was not paid by The Commit Book. ${a.college} and the NCAA/NAIA/NJCAA are not affiliated with us.`);
 ul.innerHTML=a.playbooks.map((p,i)=>{const pb=this.P[p],on=this.bag.has(p);return `<li class="sr__item" style="--i:${i+1}"><span class="sr__thumb">${String(i+1).padStart(2,'0')}</span><span><div class="sr__itype">Playbook · $${pb.price}, one-time</div><a class="sr__iname" href="/playbooks/${p}">${pb.title}</a></span><button class="sr__add" data-add="${p}" aria-pressed="${on}">${on?'Added':'Get'}</button></li>`}).join('');
 const pi=this.querySelector('.sr__pinner');pi.classList.remove('is-in');void pi.offsetWidth;pi.classList.add('is-in');
 var _rd=this.querySelector('[data-read]');_rd.textContent='Playbooks for '+a.sport+' \u2192';_rd.onclick=()=>location.href=SPORT_PATH(a);
}
updBag(){const n=this.bag.size;document.querySelectorAll('[data-bag-count]').forEach(e=>e.textContent=n);this.querySelector('[data-bagline]').textContent=n?`${n} in your playbook bag (saved on this device).`:'For the athlete to run. Parents support.';try{localStorage.setItem('playbook-bag-v1',JSON.stringify([...this.bag]))}catch(e){}}
toast(m){const t=document.getElementById('bag-status');if(!t)return;t.textContent=m;t.classList.add('is-on');clearTimeout(this.tt);this.tt=setTimeout(()=>t.classList.remove('is-on'),2500)}
moveTo(T){this.target=T;this.setStill(false);this.setIndex(T)}
next(){this.moveTo(Math.round(this.target)+1)}prev(){this.moveTo(Math.round(this.target)-1)}
go(i){let d=((i-this.index)%this.n+this.n)%this.n;if(d>this.n/2)d-=this.n;this.moveTo(Math.round(this.target)+d)}
play(v){this.playing=v;this.classList.toggle('is-playing',v);this.querySelector('.sr__auto').setAttribute('aria-pressed',String(v));this.restartBar()}
restartBar(){clearTimeout(this.timer);this.ticks.forEach(t=>t.classList.remove('is-run'));if(!this.playing)return;void this.offsetWidth;this.ticks[this.index].classList.add('is-run');
 this.timer=setTimeout(()=>{if(this.playing&&this.visible&&!this.dragging&&!document.hidden&&!this.panelHover&&!this.engaged)this.next();else this.restartBar()},SPEED)}
engage(){this.engaged=true;this.play(false)}
bind(){
 const st=this.stage;let p=null,suppress=0;
 st.addEventListener('pointerdown',e=>{if(e.pointerType==='mouse'&&e.button!==0)return;p={x:e.clientX,y:e.clientY,t:this.target,id:e.pointerId,s:[{x:e.clientX,t:e.timeStamp}],drag:false}});
 st.addEventListener('pointermove',e=>{
  if(!p||e.pointerId!==p.id)return;if(e.pointerType==='mouse'&&!(e.buttons&1)){end(e);return}
  const dx=e.clientX-p.x,dy=e.clientY-p.y;
  if(!p.drag){if(Math.abs(dy)>10&&Math.abs(dy)>=Math.abs(dx)){p=null;return}if(Math.abs(dx)>8&&Math.abs(dx)>1.2*Math.abs(dy)){p.drag=true;this.dragging=true;this.classList.add('is-dragging');st.setPointerCapture(e.pointerId)}}
  if(p.drag){p.s.push({x:e.clientX,t:e.timeStamp});if(p.s.length>6)p.s.shift();this.target=p.t-dx/this.unit;this.setStill(false);this.kick()}
 });
 const end=e=>{if(!p)return;const q=p;p=null;if(!q.drag)return;this.dragging=false;this.classList.remove('is-dragging');suppress=performance.now();
  const f=q.s[0],l=q.s[q.s.length-1],vx=(l.x-f.x)/Math.max(1,l.t-f.t),dx=(e.clientX??l.x)-q.x,from=Math.round(q.t),sign=-1;
  if(this.mob){this.moveTo(Math.abs(dx)>30||Math.abs(vx)>.3?from+sign*(dx>0?1:-1):from)}
  else{let i=Math.round(this.target+sign*vx*160/this.unit);if(i===from&&Math.abs(vx)>.3)i=from+(vx>0?-1:1);this.moveTo(clamp(i,from-2,from+2))}};
 st.addEventListener('pointerup',end);st.addEventListener('pointercancel',end);
 this.addEventListener('click',e=>{if(performance.now()-suppress<60){e.stopPropagation();e.preventDefault()}},true);
 let acc=0,lock=0;st.addEventListener('wheel',e=>{if(Math.abs(e.deltaX)<=Math.abs(e.deltaY))return;e.preventDefault();if(performance.now()<lock)return;acc+=e.deltaX;if(Math.abs(acc)>45){acc>0?this.next():this.prev();acc=0;lock=performance.now()+520}},{passive:false});
 st.addEventListener('keydown',e=>{if(e.key==='ArrowRight'){e.preventDefault();this.next()}if(e.key==='ArrowLeft'){e.preventDefault();this.prev()}if(e.key==='Enter'&&e.target===st)location.href=SPORT_PATH(this.A[this.index])});
 this.addEventListener('click',e=>{const t=e.target;let b;
  if(t.closest('.sr__next'))return this.next();if(t.closest('.sr__prev'))return this.prev();
  if(b=t.closest('[data-tick]'))return this.go(+b.dataset.tick);
  if(t.closest('.sr__auto')){if(!this.playing)this.engaged=false;return this.play(!this.playing)}
  if(b=t.closest('[data-add]')){this.engage();const id=b.dataset.add;this.bag.has(id)?this.bag.delete(id):this.bag.add(id);const on=this.bag.has(id);b.setAttribute('aria-pressed',on);b.textContent=on?'Added':'Get';this.updBag();this.toast(on?'Playbook saved to your bag':'Removed from your bag');return}
  if(b=t.closest('[data-view]'))return location.href=SPORT_PATH(this.A[+b.dataset.view]);
  if(b=t.closest('[data-go]')){const k=this.rank(+b.dataset.go);const kk=this.mob?k:k;if(k!==0&&Math.abs(k)<6)this.moveTo(Math.round(this.target)+(this.mob&&k>6?k-12:kk));}
 });
 const pn=this.querySelector('.sr__panel');pn.addEventListener('pointerenter',e=>{if(e.pointerType==='mouse')this.panelHover=true});pn.addEventListener('pointerleave',()=>{this.panelHover=false;this.restartBar()});
 if(matchMedia('(hover:hover) and (pointer:fine) and (min-width:750px)').matches){this.classList.add('has-cursor');const c=this.cursor;let x=0,y=0,tx=0,ty=0,on=false,cr=0;
  const loop=()=>{cr=0;const L=RM?1:.18;x+=(tx-x)*L;y+=(ty-y)*L;c.style.transform=`translate3d(${x}px,${y}px,0)`;if(Math.hypot(tx-x,ty-y)>.2)cr=requestAnimationFrame(loop)};
  st.addEventListener('pointermove',e=>{if(e.pointerType!=='mouse')return;const r=st.getBoundingClientRect();tx=e.clientX-r.left;ty=e.clientY-r.top;if(!on){on=true;x=tx;y=ty;c.classList.add('is-on')}
   const view=!this.dragging&&e.target.closest('[data-view]'),link=!this.dragging&&e.target.closest('[data-go]');c.classList.toggle('is-view',!!view);c.classList.toggle('is-link',!!link);if(!cr)cr=requestAnimationFrame(loop)});
  st.addEventListener('pointerleave',()=>{on=false;c.classList.remove('is-on','is-link','is-view')})}else this.cursor.remove();
 let rt;addEventListener('resize',()=>{clearTimeout(rt);rt=setTimeout(()=>this.measure(),120)});new ResizeObserver(()=>this.measure()).observe(st);
 document.addEventListener('visibilitychange',()=>this.kick());
}
}
customElements.define('story-ring',StoryRing);
})();
