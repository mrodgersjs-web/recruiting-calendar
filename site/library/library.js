/* The Commit Book Library renderer. Data: /library/library.json. Brand: all items are ours; no third-party attribution. */
(function(){
  'use strict';
  function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e}
  function segNames(d,ids){return ids.map(function(i){for(var k=0;k<d.segments.length;k++){if(d.segments[k].id===i)return d.segments[k].name}return 'Segment '+i})}
  function stageLabel(d,k){for(var i=0;i<d.stages.length;i++){if(d.stages[i].key===k)return d.stages[i].label}return k}
  function card(o){
    var li=el('li','lb-card '+o.kind);
    var badge=el('span','lb-kind '+o.kind,o.badge);li.appendChild(badge);
    li.appendChild(el('h3',null,o.title));
    if(o.why)li.appendChild(el('p','lb-why',o.why));
    if(o.tagline)li.appendChild(el('p','lb-tag',o.tagline));
    if(o.contents){var ul=el('ul','lb-contents');o.contents.forEach(function(c){ul.appendChild(el('li',null,c))});li.appendChild(ul)}
    var segs=el('ul','lb-seg');segNames(DATA,o.audience).forEach(function(n){segs.appendChild(el('li',null,n))});li.appendChild(segs);
    var act=el('div','lb-act');
    if(o.price_label)act.appendChild(el('span','lb-price',o.price_label));
    var a=el('a','lb-link',o.cta);a.href=o.href;act.appendChild(a);
    li.appendChild(act);
    li.dataset.audience=JSON.stringify(o.audience);li.dataset.stage=o.stage;li.dataset.kind=o.kind;
    return li;
  }
  var DATA,grid,status,fs,fk,fg,reset;
  function allCards(){return Array.prototype.slice.call(grid.querySelectorAll('li'))}
  function render(){
    var sv=fs.value,kv=fk.value,gv=fg.value,shown=0;
    allCards().forEach(function(li){
      var ok=true;
      if(sv){ok=ok&&(JSON.parse(li.dataset.audience).indexOf(+sv)>=0)}
      if(kv){ok=ok&&li.dataset.kind===kv}
      if(gv){ok=ok&&li.dataset.stage===gv}
      li.hidden=!ok;
      if(ok)shown++;
    });
    Array.prototype.slice.call(grid.querySelectorAll('.lb-group')).forEach(function(g){
      var any=g.querySelectorAll('li:not([hidden])').length;g.hidden=!any;
    });
    status.textContent=shown+' of '+allCards().length+' items'+(sv||kv||gv?' match your filters':' in the library');
    var q=new URLSearchParams();if(sv)q.set('seg',sv);if(kv)q.set('kind',kv);if(gv)q.set('stage',gv);
    history.replaceState(null,'',q.toString()?'?'+q:location.pathname);
  }
  function tiers(d){
    var box=document.getElementById('tiers');if(!box)return;
    d.tiers.forEach(function(t){
      var c=el('div','lb-tier'+(t.offered?' on':''));
      c.appendChild(el('h2',null,t.name));
      var amt=el('div','amt');
      amt.textContent=t.price?('+'===String(t.price).charAt(0)?String(t.price):'$'+t.price):'Price TBC';
      if(t.cadence&&t.price)amt.appendChild(el('small',null,' / '+t.cadence));
      c.appendChild(amt);c.appendChild(el('p',null,t.line));
      if(t.note)c.appendChild(el('span','note',t.note));
      if(!t.offered)c.appendChild(el('span','note','Announced, not sold yet'));
      box.appendChild(c);
    });
  }
  function groups(d){
    d.stages.forEach(function(st){
      var sec=el('section','lb-group');sec.dataset.stage=st.key;
      sec.appendChild(el('h2',null,st.label));
      var ul=el('ul','lb-grid');
      d.free_pages.forEach(function(p){if(p.stage===st.key)ul.appendChild(card(mk(p,'free','Free interactive page')))});
      d.playbooks.forEach(function(p){if(p.stage===st.key)ul.appendChild(card(mk(p,'playbook','Playbook')))});
      d.offers.forEach(function(o){if(o.stage===st.key)ul.appendChild(card(mk(o,'soon'==='x'?'ready':(o.status==='BUILT'?'ready':'soon'),(o.status==='BUILT'?'Contents written':'Announced only'))})});
      sec.appendChild(ul);grid.appendChild(sec);
    });
  }
  function mk(p,kind,badge){
    var cta=p.cta||(kind==='playbook'?'Read':(kind==='free'?'Open':'Notify me'));
    return {kind:kind,badge:badge,title:p.title,why:p.why||'',tagline:p.tagline||'',contents:p.contents||[],
            audience:p.audience,stage:p.stage,href:p.href,price_label:p.price_label||'',cta:cta};
  }
  function init(d){
    DATA=d;grid=document.getElementById('catalog');status=document.getElementById('status');
    fs=document.getElementById('f-seg');fk=document.getElementById('f-kind');fg=document.getElementById('f-stage');
    reset=document.getElementById('f-reset');
    tiers(d);groups(d);
    var rm=document.getElementById('ready-means');if(rm&&d.ready_means)rm.textContent=d.ready_means;
    d.segments.forEach(function(s){var o=el('option',null,s.name);o.value=s.id;fs.appendChild(o)});
    d.stages.forEach(function(s){var o=el('option',null,s.label);o.value=s.key;fg.appendChild(o)});
    [fs,fk,fg].forEach(function(x){x.addEventListener('change',render)});
    reset.addEventListener('click',function(){fs.value='';fk.value='';fg.value='';render()});
    var q=new URLSearchParams(location.search);
    if(q.get('seg'))fs.value=q.get('seg');if(q.get('kind'))fk.value=q.get('kind');if(q.get('stage'))fg.value=q.get('stage');
    render();
  }
  fetch('/library/library.json').then(function(r){return r.json()}).then(init).catch(function(){
    var s=document.getElementById('status');if(s)s.textContent='Could not load the library data. The playbooks are at /playbooks and paid tools are on /price.';
  });
})();
