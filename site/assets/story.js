(function(){var RM=matchMedia('(prefers-reduced-motion: reduce)').matches,root=document.documentElement,beats=[].slice.call(document.querySelectorAll('.beat')),tk=0;
function upd(){tk=0;var vh=innerHeight;root.style.setProperty('--sp',(scrollY/Math.max(1,root.scrollHeight-vh)).toFixed(4));
 beats.forEach(function(b){var r=b.getBoundingClientRect();var p=Math.max(0,Math.min(1,(vh-r.top)/(vh+r.height)));b.style.setProperty('--p',RM?.5:p.toFixed(4))})}
addEventListener('scroll',function(){if(!tk){tk=1;requestAnimationFrame(upd)}},{passive:true});addEventListener('resize',upd);upd();
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting)e.target.classList.add('on')})},{threshold:.3,rootMargin:'0px 0px -10% 0px'});
document.querySelectorAll('.timeline .ev').forEach(function(e){RM?e.classList.add('on'):io.observe(e)});
var v=document.querySelector('.st-vid video');if(v&&!RM){new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){v.play().catch(function(){})}else v.pause()})},{threshold:.4}).observe(v)}
})();
