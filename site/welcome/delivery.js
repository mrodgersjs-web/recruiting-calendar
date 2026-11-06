/* /welcome?session_id=cs_test_... -> lists purchased playbooks with download links from /api/order. */
(function(){var id=new URLSearchParams(location.search).get('session_id'),box=document.getElementById('delivery');if(!box)return;
if(!id){box.textContent='No order found on this link. Check your receipt email for your download link.';return;}
fetch('/api/order?session_id='+encodeURIComponent(id)).then(function(r){return r.json().then(function(j){return[r.ok,j]})}).then(function(x){
 if(!x[0]){box.textContent=x[1].error||'We could not load your order.';return;}
 var h=document.getElementById('welcome-title');if(h)h.textContent=x[1].mode==='subscription'?'Your trial has started.':'Your playbooks are ready.';
 var ul=document.createElement('ul');ul.className='downloads';x[1].items.forEach(function(it){var li=document.createElement('li');
  if(it.url){var a=document.createElement('a');a.href=it.url;a.textContent='Download: '+it.title;li.appendChild(a);}else li.textContent=it.title+' (this edition is still being prepared; check back on this page)';ul.appendChild(li);});
 box.innerHTML='';box.appendChild(ul);}).catch(function(){box.textContent='Delivery is not connected in this preview.';});})();
