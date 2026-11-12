function SRC_LINK(a){var pb=(a.playbooks||a.related||[])[0];return pb?'/playbooks/'+pb+'#sources':'/playbooks';}
function SLUG(s){s=String(s||'').toLowerCase();if(s.indexOf('track')>-1)return'track-field';if(s.indexOf('swim')>-1)return'swimming';if(s.indexOf('lacrosse')>-1)return'lacrosse';return s.split(/[\s(/]+/)[0];}
/* Phone deck (<=749px): one illustration card per sport, swipe snaps card to card.
   Desktop keeps <story-ring>. Names are placeholders; no real person is shown. */
(function(){
  var MQ=matchMedia('(max-width:749px)');
  function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  function build(){
    var D=window.STORY_DATA;if(!D)return;var host=document.querySelector('story-deck');if(!host||host.dataset.built)return;
    var comps=D.athletes.filter(function(a){return a.composite}),reals=D.athletes.filter(function(a){return !a.composite});
    var P=D.playbooks;
    var cards=comps.map(function(a,i){
      var pbs=(a.playbooks||[]).filter(function(id){return P[id]&&P[id].status==='WRITTEN'}).slice(0,2).map(function(id){var p=P[id];if(!p)return'';
        return '<li><span class="dk-pb-t">'+esc(p.title)+'</span><span class="dk-pb-p">$'+p.price+'</span>'+
          (p.notify?'<a class="dk-pb-b ghost" href="/playbooks/'+id+'">Notify me</a>':'<button class="dk-pb-b" data-offer="'+id+'">Get</button>')+'</li>'}).join('');
      var src=a.img.replace('-640','-1080');
      return '<article class="dk-card" id="dk-'+esc(a.id)+'" aria-roledescription="slide" aria-label="'+(i+1)+' of '+comps.length+': '+esc(a.short)+'">'+
        '<div class="dk-art">'+(a.img?'<img src="'+esc(src)+'" alt="Illustration of '+esc(a.short)+', a fictional '+esc((a.sport||'').toLowerCase())+' '+NOUN(a.sport)+'" '+(i<2?'loading="eager" fetchpriority="'+(i?'auto':'high')+'"':'loading="lazy"')+' decoding="async"><span class="tag-ill">Illustration</span>':'<span class="dk-none">'+esc(a.sport)+'</span><span class="tag-ill">Playbook in progress</span>')+'</div>'+
        '<div class="dk-txt"><p class="dk-k">'+esc(a.sport)+'</p><h2 class="dk-h">'+esc((a.short||'').replace(/\s*\(composite\)/i,''))+'</h2>'+
        '<a class="btn btn--primary dk-read" href="/sports/'+SLUG(a.sport)+'">Playbooks for '+esc(a.sport)+'</a> <a class="dk-src" style="font-size:13px" href="'+SRC_LINK(a)+'">'+(a.page===false?'Where this comes from':'How this played out')+'</a></div></div>'+
        '<div class="dk-pbs"><p class="dk-pbl">Playbooks for this sport</p><ul>'+pbs+'</ul></div></article>'}).join('');
    var dots=comps.map(function(a,i){return '<button class="dk-dot" aria-label="Go to '+esc(a.short)+'" data-i="'+i+'"'+(i?'':' aria-current="true"')+'></button>'}).join('');
    var realLinks=reals.filter(function(a){return !a.hold}).map(function(a){return '<a href="'+(a.page===false?'/sports/'+SLUG(a.sport):'/story/'+esc(a.id))+'"><b>'+esc(a.short)+'</b><span>'+esc(a.sport)+' · '+esc(a.div)+'</span></a>'}).join('');
    host.innerHTML='<p class="dk-intro">Swipe to browse. Names are placeholders and the art is drawn; the playbooks and dates are what you are actually buying.</p>'+
      '<div class="dk-track" tabindex="0" role="region" aria-roledescription="carousel" aria-label="Browse by sport, swipe left or right">'+cards+'</div>'+
      '<div class="dk-dots">'+dots+'</div>';
    host.dataset.built='1';
    var tr=host.querySelector('.dk-track'),ds=[].slice.call(host.querySelectorAll('.dk-dot'));
    function cur(){return Math.round(tr.scrollLeft/Math.max(1,tr.clientWidth))}
    var t=0;tr.addEventListener('scroll',function(){cancelAnimationFrame(t);t=requestAnimationFrame(function(){var c=cur();ds.forEach(function(d,j){d.toggleAttribute('aria-current',j===c)})})},{passive:true});
    ds.forEach(function(d){d.addEventListener('click',function(){tr.scrollTo({left:+d.dataset.i*tr.clientWidth,behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'})})});
    tr.addEventListener('keydown',function(e){if(e.key==='ArrowRight'||e.key==='ArrowLeft'){e.preventDefault();var c=cur()+(e.key==='ArrowRight'?1:-1);c=Math.max(0,Math.min(ds.length-1,c));tr.scrollTo({left:c*tr.clientWidth})}});
  }
  function apply(){document.documentElement.classList.toggle('use-deck',MQ.matches);if(MQ.matches)build()}
  if(document.readyState!=='loading')apply();else document.addEventListener('DOMContentLoaded',apply);
  MQ.addEventListener?MQ.addEventListener('change',apply):MQ.addListener(apply);
})();
