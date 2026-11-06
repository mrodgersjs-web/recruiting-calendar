// GET /api/order?session_id=cs_test_... -> what the /welcome page shows: paid/trialing status + download links for purchased PDFs.
import { stripe, guard, fail } from '../lib/stripe.js';
import { books, hasPdf } from '../lib/offers.js';
export async function paidSession(id){
  if(!/^cs_test_[A-Za-z0-9]+$/.test(String(id||'')))throw Object.assign(new Error('Invalid session'),{code:400});
  await guard(); const s=await stripe('GET',`checkout/sessions/${id}`);
  if(s.livemode)throw Object.assign(new Error('live session rejected'),{code:400});
  const ok=s.status==='complete'&&(s.payment_status==='paid'||(s.mode==='subscription'&&s.payment_status==='no_payment_required'));
  if(!ok)throw Object.assign(new Error('Payment not complete'),{code:402});
  return {s,slugs:String(s.metadata?.slugs||'').split(',').filter(x=>books[x])};
}
export default async function handler(req,res){
  if(req.method!=='GET')return res.status(405).json({error:'GET only'});
  try{ const q=req.query||Object.fromEntries(new URL(req.url,'http://x').searchParams);
    const {s,slugs}=await paidSession(q.session_id);
    return res.status(200).json({offer:s.metadata?.offer,mode:s.mode,items:slugs.map(x=>({slug:x,title:books[x].title,
      ready:hasPdf(x),url:hasPdf(x)?`/api/deliver?session_id=${s.id}&slug=${x}`:null}))});
  }catch(e){return fail(res,e);}
}
