(function(){
 const FREE=3, M=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
 const $=id=>document.getElementById(id);
 $('today')&&($('today').textContent=new Date().toLocaleDateString('en-US',{weekday:'long',month:'long',day:'numeric',year:'numeric'}));
 const NAMES={baseball:'Baseball',football:'Football',track:'Track & field / cross country'};
 function render(){
  const sport=$('sport').value, cls=+$('cls').value, set=(window.RC_DATA||{})[sport];
  $('dates-title').textContent=NAMES[sport]+', Class of '+cls;
  const ledger=$('ledger'); ledger.innerHTML='';
  if(!set){ledger.innerHTML='<li><div></div><p>Dates for this sport are being verified.</p></li>';return;}
  const shift=cls-set.class_year;
  const sh=s=>{const t=new Date(s+'T12:00:00');t.setFullYear(t.getFullYear()+shift);return t;};const rows=set.deadlines.map(d=>({...d,dt:d.iso_date?sh(d.iso_date):null,sk:sh(d.sort)})).sort((a,b)=>a.sk-b.sk);
  $('dates-meta').textContent=rows.length+' dates · verified '+set.verified_on+' · '+set.source_label;
  rows.forEach((d,i)=>{
   const li=document.createElement('li'); if(i>=FREE)li.className='locked';
   const K={opening:'Opening',window:'Window opens',projected:'Projected',hard:'Hard limit',action:'Our recommended date'};li.dataset.kind=d.kind;if(d.dt)li.dataset.ts=d.dt.getTime();li.innerHTML=(d.dt?'<div><div class="day">'+d.dt.getDate()+'</div><span class="when">'+M[d.dt.getMonth()]+' '+d.dt.getFullYear()+'</span>':'<div><div class="day sm">Your school\'s date</div>')+'<span class="tag">'+K[d.kind]+'</span></div>'+
    '<div><h3>'+d.event+'</h3><p>'+d.plain_english+'</p><p class="src">'+(d.rule?d.rule+' · ':'')+'<a href="'+d.citation_url+'" target="_blank" rel="noopener">source</a></p></div>'+
    '<div class="cost"><b>'+(d.kind==='hard'?'If you miss it':'If you wait')+'</b>'+d.cost_if_missed+'</div>';
   ledger.appendChild(li);
  });
  $('gate-n').textContent=Math.max(0,rows.length-FREE);
  $('gate').style.display=rows.length>FREE?'':'none';if(window.RC_led)window.RC_led();
 }
 $('go').addEventListener('click',()=>{render();document.getElementById('dates').scrollIntoView();});
 $('sport').addEventListener('change',render);$('cls').addEventListener('change',render);
 render();
})();
