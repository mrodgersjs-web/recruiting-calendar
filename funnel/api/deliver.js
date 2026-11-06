// GET /api/deliver?session_id=&slug= -> streams a purchased PDF from funnel/deliver/pdfs (private, not under site/).
// Re-verifies the Stripe test session on every download; slug must be in that session's metadata.
import fs from 'fs'; import path from 'path';
import { paidSession } from './order.js';
import { PDF_DIR, hasPdf } from '../lib/offers.js';
import { fail } from '../lib/stripe.js';
export default async function handler(req,res){
  if(req.method!=='GET')return res.status(405).json({error:'GET only'});
  try{ const q=req.query||Object.fromEntries(new URL(req.url,'http://x').searchParams);
    const {slugs}=await paidSession(q.session_id); const slug=String(q.slug||'');
    if(!slugs.includes(slug))return res.status(403).json({error:'Not in this order'});
    if(!hasPdf(slug))return res.status(404).json({error:'This edition is still being prepared'});
    res.setHeader('Content-Type','application/pdf');res.setHeader('Content-Disposition',`attachment; filename="${slug}.pdf"`);
    res.setHeader('Cache-Control','private, no-store');
    return res.status(200).send(fs.readFileSync(path.join(PDF_DIR,`${slug}.pdf`)));
  }catch(e){return fail(res,e);}
}
