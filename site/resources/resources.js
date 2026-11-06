/* Third-party resource directory. Data: /resources/offers.json (from v3/W10-offers, live-verified 2026-11-06). Never pads a story past its verified offers. */
(function(){
  'use strict';
  var $=function(id){return document.getElementById(id)};
  var grid=$('directory'),status=$('status'),gap=$('gap'),fs=$('f-story'),fp=$('f-price'),fc=$('f-cat');
  var data,bySlug={};
  function title(s){return s.split('-').map(function(w){return w.charAt(0).toUpperCase()+w.slice(1)}).join(' ')}
  function el(tag,cls,txt){var e=document.createElement(tag);if(cls)e.className=cls;if(txt!=null)e.textContent=txt;return e}
  function card(o){
    var li=el('li','rs-card');
    li.appendChild(el('span','rs-cat',o.category));
    li.appendChild(el('h2',null,o.title));
    li.appendChild(el('span','rs-by','By McKinley Malbrough III, MM3 Sports'));
    var row=el('div','rs-row');
    var left=el('div');
    left.appendChild(el('div','rs-price'+(o.free?' free':''),o.price_label));
    left.appendChild(el('div','rs-kind',o.kind));
    row.appendChild(left);
    var a=el('a','rs-go','View on Gumroad');
    a.href=o.href;a.target='_blank';a.rel='noopener noreferrer';
    a.setAttribute('aria-label','View '+o.title+' on Gumroad (opens in a new tab)');
    row.appendChild(a);li.appendChild(row);return li;
  }
  function render(){
    var sv=fs.value,pv=fp.value,cv=fc.value,list,st=null;
    if(sv){st=data.stories.filter(function(s){return s.slug===sv})[0];list=st.offers.map(function(x){return bySlug[x]})}
    else list=data.offers.slice();
    if(pv==='free')list=list.filter(function(o){return o.free});
    if(pv==='paid')list=list.filter(function(o){return !o.free});
    if(cv)list=list.filter(function(o){return o.category===cv});
    grid.textContent='';list.forEach(function(o){grid.appendChild(card(o))});
    var msg=list.length+' of '+(st?st.count+' verified matches for this story':data.offers.length+' resources');
    status.textContent=list.length?msg:'No resources match these filters. Reset to see all.';
    if(st){
      gap.hidden=false;gap.textContent='';
      var b=el('strong',null,title(st.slug)+' ('+st.tags.join(', ')+'): ');
      gap.appendChild(b);
      gap.appendChild(document.createTextNode(st.relevance_basis+'. '));
      if(st.gap){gap.appendChild(document.createTextNode('Only '+st.count+' verified offers: '+st.gap.toLowerCase()+(st.no_sport_specific?' ('+st.no_sport_specific+').':'.')))}
      else gap.appendChild(document.createTextNode(st.count+' verified offers.'));
      if(st.held)gap.appendChild(document.createTextNode(' This story page is currently held (noindex), so it is not linked from here.'));
    } else {gap.hidden=true}
    var u=new URLSearchParams();if(sv)u.set('story',sv);if(pv)u.set('price',pv);if(cv)u.set('cat',cv);
    history.replaceState(null,'',u.toString()?'?'+u:location.pathname);
  }
  function init(d){
    data=d;d.offers.forEach(function(o){bySlug[o.slug]=o});
    d.stories.forEach(function(s){var o=el('option',null,title(s.slug)+' ('+s.tags[0]+') — '+s.count+' offers');o.value=s.slug;fs.appendChild(o)});
    d.categories.forEach(function(c){var o=el('option',null,c);o.value=c;fc.appendChild(o)});
    var p=new URLSearchParams(location.search);
    if(p.get('story'))fs.value=p.get('story');if(p.get('price'))fp.value=p.get('price');if(p.get('cat'))fc.value=p.get('cat');
    [fs,fp,fc].forEach(function(s){s.addEventListener('change',render)});
    $('f-reset').addEventListener('click',function(){fs.value=fp.value=fc.value='';render()});
    render();
  }
  fetch('/resources/offers.json').then(function(r){return r.json()}).then(init).catch(function(){
    status.textContent='Could not load the directory data. All 30 products are at malbrough6.gumroad.com.';
  });
})();
