/* Playbook bag checkout wiring (TEST MODE). Any element with data-offer (+ optional data-sport) starts checkout.
   Every trial button (data-offer="sideline" or data-checkout="sideline") gets the auto-renew disclosure placed
   directly after it if one is not already adjacent. Text must match funnel/lib/offers.js TRIAL_DISCLOSURE. */
(function(){
var D='Free for 14 days, then $149 per year (proposed), renewing yearly until you cancel. Cancel online any time from your billing page. We'll show your renewal date in your account and billing page.';
function disclose(b){var n=b.nextElementSibling;if(n&&n.classList.contains('disclose'))return;var p=document.createElement('p');p.className='note disclose trial-disclosure';p.textContent=D;b.insertAdjacentElement('afterend',p);var l=document.createElement('label');l.className='note ar-consent';l.innerHTML='<input type="checkbox" required> I agree that my membership renews automatically each year until I cancel.';p.insertAdjacentElement('afterend',l);var c=l.querySelector('input');b.disabled=true;b.setAttribute('aria-disabled','true');c.addEventListener('change',function(){b.disabled=!c.checked;b.setAttribute('aria-disabled',String(!c.checked))});}
document.querySelectorAll('[data-offer="sideline"],[data-checkout="sideline"]').forEach(disclose);
document.querySelectorAll('[data-offer]').forEach(function(b){b.addEventListener('click',function(ev){ev.preventDefault();
 var em=document.querySelector('form.capture [name=email]');
 fetch('/api/checkout',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({offer:b.dataset.offer,sport:b.dataset.sport,email:em&&em.value||undefined})})
 .then(function(r){return r.json()}).then(function(j){if(j.url)location.href=j.url;else throw j;})
 .catch(function(j){var f=document.querySelector('form.capture');if(f){var pl=f.querySelector('[name=plan]');if(pl)pl.value=b.dataset.offer;f.scrollIntoView();var m=f.querySelector('.form-msg');if(m)m.textContent=(j&&j.error)||'Checkout isn\'t live yet. Leave your email and we\'ll send the playbook link when it is.';}});});});
})();
