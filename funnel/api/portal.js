// POST /api/portal {checkout_session_id, email} -> Stripe billing portal (TEST). Cancellation lives here: one click, no survey gate.
// Gated: POST only, PORTAL_ENABLED==="true" (503 preview-disabled by default), test key + sandbox account guard.
// Ownership: the caller never supplies a customer id. We fetch the Checkout Session from Stripe, require it to be a complete
// test-mode subscription session, and require the caller's email to match the session's customer_email / customer_details.email.
// The customer used for the portal is taken from the Stripe session only.
import { stripe, guard, body, fail, testKey } from '../lib/stripe.js';
const same=(a,b)=>!!a&&!!b&&String(a).trim().toLowerCase()===String(b).trim().toLowerCase();
export default async function handler(req,res){
  if(req.method!=='POST'){res.setHeader&&res.setHeader('Allow','POST');return res.status(405).json({error:'POST only'});}
  if(process.env.PORTAL_ENABLED!=='true')return res.status(503).json({error:'Billing portal is disabled in this preview. No subscriptions exist.'});
  try{
    if(!testKey())return res.status(500).json({error:'Test key required; live mode disabled in this build'});
    const b=body(req); const id=String(b.checkout_session_id||''); const email=String(b.email||'');
    if(!/^cs_test_[A-Za-z0-9]+$/.test(id))return res.status(400).json({error:'Valid checkout_session_id required'});
    if(!email)return res.status(400).json({error:'email required'});
    await guard();
    const s=await stripe('GET',`checkout/sessions/${id}`);
    if(s.livemode)return res.status(400).json({error:'live session rejected'});
    if(s.status!=='complete'||s.mode!=='subscription'||!s.customer)return res.status(403).json({error:'No active subscription for this session'});
    if(!same(email,s.customer_email)&&!same(email,s.customer_details?.email))return res.status(403).json({error:'Session does not belong to this email'});
    const cust=typeof s.customer==='string'?s.customer:s.customer.id;
    const p=await stripe('POST','billing_portal/sessions',{customer:cust,return_url:`${process.env.SITE_URL||'http://localhost:3000'}/billing`});
    return res.status(200).json({url:p.url});
  }catch(e){return fail(res,e);}
}
