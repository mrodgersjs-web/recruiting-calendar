// Offer table for the playbook bag, built from v3/W1-playbooks/CATALOG.json. Prices are PROPOSED (Mike approved showing them 2026-11-05).
// Purchasable = every included playbook has status WRITTEN and a PDF in funnel/deliver/pdfs/, unless PREORDER_ENABLED==="true".
import fs from 'fs'; import path from 'path'; import { fileURLToPath } from 'url';
const here=path.dirname(fileURLToPath(import.meta.url));
export const ROOT=path.resolve(here,'../..');
export const PDF_DIR=path.join(ROOT,'funnel/deliver/pdfs');
const CAT=JSON.parse(fs.readFileSync(path.join(ROOT,'v3/W1-playbooks/CATALOG.json'),'utf8'));
export const SPORTS=['football','baseball','track'];
const SPORT_BOOK={football:'football-junior-year',baseball:'baseball-showcase-to-signing',track:'track-field-marks'};
export const TRIAL_DAYS=14, SIDELINE_USD=149;
// Exact auto-renew disclosure. Must render next to EVERY trial button and in Stripe's submit text.
export const TRIAL_DISCLOSURE=`Free for ${TRIAL_DAYS} days, then $${SIDELINE_USD} per year, renewing yearly until you cancel. Cancel any time online in one click. We email you 7 days before the trial ends.`;
export const books=Object.fromEntries(CAT.catalog.map(p=>[p.slug,p]));
export const hasPdf=slug=>fs.existsSync(path.join(PDF_DIR,`${slug}.pdf`));
const ready=slug=>books[slug]?.status==='WRITTEN'&&hasPdf(slug);
const bundle=s=>CAT.bundles.find(b=>b.slug===s);
export function resolveOffer(offer,sport){
  if(books[offer])return {offer,kind:'playbook',mode:'payment',title:books[offer].title,usd:books[offer].price_usd,slugs:[offer]};
  if(offer==='sport-pack'){ if(!SPORTS.includes(sport))return null;
    return {offer,sport,kind:'bundle',mode:'payment',title:`Sport Pack: ${sport}`,usd:bundle('sport-pack').price_usd,
      slugs:[SPORT_BOOK[sport],'eligibility-2-hard-deadlines','offer-and-signing','camp-roi']}; }
  if(offer==='all-playbooks')return {offer,kind:'bundle',mode:'payment',title:'Every Playbook',usd:bundle('all-playbooks').price_usd,slugs:Object.keys(books)};
  if(offer==='sideline')return {offer,kind:'trial',mode:'subscription',title:'Sideline membership',usd:SIDELINE_USD,slugs:Object.keys(books),disclosure:TRIAL_DISCLOSURE};
  return null;
}
export const available=o=>process.env.PREORDER_ENABLED==='true'||o.slugs.every(ready);
export function listOffers(){
  const out=[];
  for(const s of Object.keys(books))out.push(resolveOffer(s));
  for(const sp of SPORTS)out.push(resolveOffer('sport-pack',sp));
  out.push(resolveOffer('all-playbooks'),resolveOffer('sideline'));
  return out.map(o=>({...o,available:available(o),ready_slugs:o.slugs.filter(ready)}));
}
