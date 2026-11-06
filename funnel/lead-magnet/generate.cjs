// Builds one printable HTML calendar per sport from ../../site/data.js.
// Only entries with a rule + citation_url are included; kind "projected" is labeled PROJECTED.
// Render to PDF: open the HTML in Chrome and print, or run render-pdf (headless Chrome).
const fs=require('fs'),path=require('path'),vm=require('vm');
const src=fs.readFileSync(path.join(__dirname,'../../site/data.js'),'utf8');
const ctx={window:{}};vm.runInNewContext(src,ctx);const D=ctx.window.RC_DATA;
const esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const label={hard:'HARD DEADLINE',opening:'Opens',window:'Window',action:'Recommended (not NCAA)',projected:'PROJECTED (not yet published)'};
function page(sport,d){
 const rows=d.deadlines.filter(x=>x.rule&&x.citation_url).sort((a,b)=>a.sort<b.sort?-1:1).map(x=>`
 <tr class="${x.kind}"><td class="dt">${esc(x.iso_date)}</td><td><b>${esc(label[x.kind]||x.kind)}</b><br>${esc(x.event)}
 <div class="pe">${esc(x.plain_english)}</div><div class="miss">If missed: ${esc(x.cost_if_missed)}</div>
 <div class="src">${esc(x.rule)} · <a href="${esc(x.citation_url)}">${esc(x.citation_url)}</a></div></td></tr>`).join('');
 return `<section><h1>${esc(sport[0].toUpperCase()+sport.slice(1))} recruiting calendar, Class of ${d.class_year}</h1>
 <p class="meta">Checked against the ${esc(d.source_label)} on ${esc(d.verified_on)}. Every date cites its bylaw. Dates marked PROJECTED follow last year's pattern and are not yet published by the NCAA. "Recommended" dates are ours, not NCAA deadlines. This is a planning aid, not legal advice and not a promise of any roster spot or scholarship.</p>
 <table>${rows}</table><p class="foot">The Recruiting Calendar · Rules change; check the cited source before acting.</p></section>`;}
const css=`body{font:11pt/1.4 Georgia,serif;color:#111;margin:0}section{padding:28px 36px;page-break-after:always}h1{font-size:20pt;margin:0 0 6px}
.meta{font-size:9pt;color:#444}table{border-collapse:collapse;width:100%}td{border-top:1px solid #ccc;padding:7px 6px;vertical-align:top}
.dt{white-space:nowrap;font-family:monospace;width:90px}.pe{margin-top:3px}.miss{font-size:9pt;color:#7a2a00}.src{font-size:8pt;color:#555;word-break:break-all}
tr.hard td{background:#fff3ef}tr.projected td{background:#f3f3f3;font-style:italic}.foot{font-size:8pt;color:#666}`;
const out=path.join(__dirname,'out');fs.mkdirSync(out,{recursive:true});
const only=process.argv[2];const sports=Object.keys(D).filter(s=>!only||s===only);
for(const s of sports)fs.writeFileSync(path.join(out,`${s}-class-${D[s].class_year}.html`),`<!doctype html><meta charset=utf-8><style>${css}</style>${page(s,D[s])}`);
fs.writeFileSync(path.join(out,'all-sports.html'),`<!doctype html><meta charset=utf-8><style>${css}</style>${sports.map(s=>page(s,D[s])).join('')}`);
console.log('wrote',sports.map(s=>`${s}:${D[s].deadlines.filter(x=>x.rule&&x.citation_url).length}`).join(' '));
