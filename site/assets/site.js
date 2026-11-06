(function(){
var K='playbook-bag-v1',bag;try{bag=new Set(JSON.parse(localStorage.getItem(K)||'[]'))}catch(e){bag=new Set()}
function save(){try{localStorage.setItem(K,JSON.stringify([...bag]))}catch(e){}document.querySelectorAll('[data-bag-count]').forEach(function(x){x.textContent=bag.size})}
function toast(m){var t=document.getElementById('bag-status');if(!t)return;t.textContent=m;t.classList.add('is-on');setTimeout(function(){t.classList.remove('is-on')},2500)}
save();
document.querySelectorAll('[data-add]').forEach(function(b){if(b.closest('story-ring'))return;var on=bag.has(b.dataset.add);b.setAttribute('aria-pressed',on);b.textContent=on?'Added':'Get'});
document.addEventListener('click',function(e){
 var b=e.target.closest('[data-add]');if(b&&!b.closest('story-ring')){var id=b.dataset.add;bag.has(id)?bag.delete(id):bag.add(id);var on=bag.has(id);b.setAttribute('aria-pressed',on);b.textContent=on?'Added':'Get';save();toast(on?'Playbook saved to your bag':'Removed from your bag');return}
 var c=e.target.closest('[data-checkout]:not([data-offer])');if(c){e.preventDefault();location.href='/price?offer='+encodeURIComponent(c.dataset.checkout)+'#join'}
});
// menu (v2 pages bind it in forms.js)
if(!document.querySelector('script[src="/forms.js"]')){var m=document.querySelector('.menu-btn'),n=document.getElementById('site-nav');if(m&&n)m.addEventListener('click',function(){var o=m.getAttribute('aria-expanded')==='true';m.setAttribute('aria-expanded',String(!o));n.classList.toggle('open',!o)})}
})();
