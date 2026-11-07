const fs=require('fs'),assert=require('assert');const p=JSON.parse(fs.readFileSync('panel.json'));
assert.equal(p.panel.length,10);assert.equal(p.criteria.length,30);assert.equal(new Set(p.criteria.map(c=>c.id)).size,30);
assert(p.meta.classification.includes('NOT REAL USER FEEDBACK'));assert(p.panel.every(x=>x.synthetic===true));
for(let i=0;i<30;i++){let c=p.criteria[i];assert.equal(c.id,'CB-'+String(i+1).padStart(2,'0'));assert(p.panel.some(x=>x.id===c.parent));assert(c.requirement&&c.acceptance&&c.evidenceRequired);assert.equal(c.status,'NOT TESTED');}
for(const name of ['jev-text-receipt.json','jev-plan.readiness-receipt.json','jev-ui.design-receipt.json']){let r=JSON.parse(fs.readFileSync(name));assert(Number.isInteger(r.decision_id));assert.equal(r.cache_hit,false);assert(r.state_sha256);}
const im=JSON.parse(fs.readFileSync('jev-image-blocker.json'));assert.equal(im.score,null);assert.equal(im.evaluationRan,false);
console.log(JSON.stringify({timestamp:new Date().toISOString(),structuralChecks:'PASS',syntheticPanelCount:10,criteriaCount:30,allProductCriteria:'NOT TESTED',liveTextReceipts:3,imageEvaluation:'BLOCKED',strictIndependentResearch:'BLOCKED',siteTesting:'NOT RUN'},null,2));
