const fs=require('fs');const R=require('./rules.json');const C=JSON.parse(fs.readFileSync('../W1-playbooks/CATALOG.json')).catalog;
const S=[...require('./stories-src.cjs'),...require('./stories-src2.cjs')];
const wc=s=>s.trim().split(/\s+/).length;
const B6="One path, not a formula. Your athlete's path will differ, and the ending here is not a typical result. Nothing in this story proves that any playbook, camp or service caused it. This athlete never used our playbooks. We do not contact coaches, and we never contact your kid. The rule shown is real and cited; the outcome is the athlete's own.";
const out=[];let md="# W2 Story Scripts (2026-11-05)\nParaphrase only, no quotes. Real athletes: no generated likeness (typography / school motifs only). Composite: every image labeled Illustration.\n\n";
for(const s of S){
 const r=s.rule?R[s.rule]:null;
 const b4=r?`The rule that mattered. ${r.card} Rule then, rule now: ${s.then} The rule did not cause this outcome and guarantees nothing. It is a date your family can check yourself, at the source below, before your athlete messages a coach.`:`[HOLD] ${s.hold}`;
 const pbs=s.pb.map(sl=>{const p=C.find(c=>c.slug===sl);return {slug:sl,title:p.title,price_usd:p.price_usd,status:p.status}});
 const b7=`The steps in this story, as a playbook. ${s.composite?"This composite athlete's":s.name.split(' ')[0]+"'s"} path came down to a few moves you just read about. These playbooks turn those steps into tools your athlete can run: ${pbs.map(p=>`${p.title} ($${p.price_usd}, one-time)`).join('; ')}. For the athlete to run, parents support. No calls, no sales team, nobody contacts your kid. Checkout isn't live yet: leave your email and we'll send the link when it is.`;
 const beats=[["hook",s.b[0]],["stakes",s.b[1]],["turning_point_1",s.b[2]],["rule",b4],["fit_decision",s.b[4]],["does_not_prove",B6],["offer",b7]].map(([k,t],i)=>({n:i+1,beat:k,text:t,words:wc(t)}));
 const f=s.composite?"Maya":s.name.split(' ').slice(-1)[0];
 const narr=`${s.composite?"This is a composite story, built from three real recruiting paths. ":""}${s.b[0].split('. ').slice(0,2).join('. ')}. ${s.b[1].split('. ').slice(0,2).join('. ')}. ${s.b[2].split('. ').slice(0,2).join('. ')}. ${r?`One rule mattered here: ${r.card.split(':')[0]} ${r.card.split(':').slice(1).join(':').split('.')[0].trim()}.`:""} ${s.b[4].split('. ').slice(0,2).join('. ')}. This is one path, not a formula, and no playbook caused it. If you want the steps from this story as tools your athlete can run, they're below.`.replace(/\s+/g,' ');
 let narr2=narr; if(wc(narr)>220){narr2=narr.replace(s.b[1].split('. ').slice(0,2).join('. ')+'. ','')} const nw=wc(narr2);
 const issues=[];beats.forEach(b=>{if(b.n<=5&&b.n!==4&&(b.words<60||b.words>80))issues.push(`beat${b.n} ${b.words}w`)});
 if(/[“”"]/.test(s.b.join(''))) issues.push('quote char');
 if(!r) issues.push('beat4 HOLD: no cited rule');
 out.push({id:s.id,name:s.name,composite:!!s.composite,label:s.label||null,sport:s.sport,level:s.level,image_policy:s.composite?"Generated illustration allowed, label 'Illustration' on every image":"NO generated likeness; typography/school/sport motifs only",rule:r?{bylaw:r.rule,url:r.url,verified_against:"site/data.js verified_on 2026-11-05"}:null,sources:s.src.map(u=>({url:u,retrieved:"2026-11-05"})),beats,in_this_story:pbs,narration:{text:narr2,words:nw,est_seconds:Math.round(nw/2.5)},qa_issues:issues});
 md+=`## ${s.name} — ${s.sport}, ${s.level}${s.composite?`\n**${s.label}** (every image: Illustration)`:""}\n\n`+beats.map(b=>`**${b.n}. ${b.beat}** (${b.words}w)\n${b.text}\n`).join('\n')+(r?`\nRule: ${r.rule} — ${r.url}\n`:"")+`\n**In this story:** ${pbs.map(p=>`${p.title} $${p.price_usd} [${p.status}]`).join(' · ')}\n\n**Narration (${nw}w, ~${Math.round(nw/2.5)}s):** ${narr2}\n\nSources: ${s.src.join(' ; ')}\n\nQA: ${issues.join('; ')||'clean'}\n\n---\n\n`;
}
fs.writeFileSync('SCRIPTS.json',JSON.stringify({generated:"2026-11-05",lane:"W2-scripts",integrity:"Paraphrase only; no quotes; no generated likeness of real athletes; bylaws from site/data.js",stories:out},null,1));
fs.writeFileSync('SCRIPTS.md',md);
out.forEach(o=>console.log(o.id,o.beats.map(b=>b.words).join(','),'narr',o.narration.words,o.qa_issues.join('|')));
