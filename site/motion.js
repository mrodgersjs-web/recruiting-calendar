(function(){
 var R=matchMedia('(prefers-reduced-motion: reduce)').matches,H=document.documentElement;
 if(R){H.classList.remove('intro-pending');}
 // FadeUp
 var els=document.querySelectorAll('[data-fade]');
 if(!R&&'IntersectionObserver' in window){els.forEach(function(e){e.classList.add('fade');e.style.transitionDelay=(e.dataset.delay||0)+'s';});
  var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target);}});},{threshold:.3});els.forEach(function(e){io.observe(e);});}
 // ledger stagger + pulse nearest-today row
 function led(){var li=document.querySelectorAll('.ledger li:not(.locked)');var now=Date.now(),best=null,bd=1e15;li.forEach(function(l,i){if(!R)l.style.animationDelay=Math.min(i,6)*.06+'s';var d=l.dataset.ts?+l.dataset.ts:null;if(d&&d>=now&&d-now<bd){bd=d-now;best=l;}});if(best&&!R)best.classList.add('pulse');}
 led();window.RC_led=led;
 // spotlight
 document.querySelectorAll('[data-spot]').forEach(function(c){c.addEventListener('pointermove',function(e){var r=c.getBoundingClientRect();c.style.setProperty('--spot-x',(e.clientX-r.left)+'px');c.style.setProperty('--spot-y',(e.clientY-r.top)+'px');});});
 // accordion: one open at a time
 document.querySelectorAll('.acc').forEach(function(a){a.querySelectorAll('.acc-q').forEach(function(q){q.addEventListener('click',function(){var it=q.parentNode,o=it.classList.contains('open');a.querySelectorAll('.acc-i').forEach(function(i){i.classList.remove('open');i.querySelector('.acc-q').setAttribute('aria-expanded','false');});if(!o){it.classList.add('open');q.setAttribute('aria-expanded','true');}});});});
 // sport cards
 document.querySelectorAll('[data-sport-card]').forEach(function(c){c.addEventListener('click',function(){var s=document.getElementById('sport');if(s){s.value=c.dataset.sportCard;s.dispatchEvent(new Event('change'));document.getElementById('dates').scrollIntoView({behavior:R?'auto':'smooth'});}});});
 // intro (WAAPI) with failsafe
 if(!R&&H.classList.contains('intro-pending')&&Element.prototype.animate){var done=false;function go(){if(done)return;done=true;H.classList.remove('intro-pending');var E=[['.masthead .row,.dateline',0],['.hero h1,.hero .lede,.hero .kicker',300],['.hero .picker,.sport-cards',700]],ez='cubic-bezier(.22,1,.36,1)';E.forEach(function(g){document.querySelectorAll(g[0]).forEach(function(el,i){el.animate([{opacity:0,transform:'translateY(16px)'},{opacity:1,transform:'none'}],{duration:600,delay:g[1]+i*85,easing:ez,fill:'backwards'});});});}
  (document.fonts&&document.fonts.ready||Promise.resolve()).then(go);setTimeout(go,500);setTimeout(function(){H.classList.remove('intro-pending');},3800);}
 else H.classList.remove('intro-pending');
})();
