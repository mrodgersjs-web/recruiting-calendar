// Vercel serverless: Stripe webhook (TEST endpoint). Verifies signature, logs events. No emails sent until SEND_ENABLED.
// Events: checkout.session.completed, customer.subscription.trial_will_end (fires 3 days before; we schedule our own 7-day notice),
// invoice.paid (renewal receipt), customer.subscription.deleted, invoice.payment_failed.
import crypto from 'crypto';
export const config={api:{bodyParser:false}};
const raw=req=>new Promise(r=>{let d='';req.on('data',c=>d+=c);req.on('end',()=>r(d));});
export default async function handler(req,res){
  const body=await raw(req),sig=req.headers['stripe-signature']||'';
  const t=(sig.match(/t=(\d+)/)||[])[1],v=(sig.match(/v1=([a-f0-9]+)/)||[])[1];
  const exp=crypto.createHmac('sha256',process.env.STRIPE_TEST_WEBHOOK_SECRET||process.env.STRIPE_WEBHOOK_SECRET||'').update(`${t}.${body}`).digest('hex');
  if(!v||v.length!==exp.length||!crypto.timingSafeEqual(Buffer.from(v),Buffer.from(exp))||Math.abs(Date.now()/1000-t)>300)return res.status(400).end();
  const e=JSON.parse(body); if(e.livemode)return res.status(400).json({error:'live event rejected'});
  const map={'checkout.session.completed':'welcome','customer.subscription.trial_will_end':'trial-ending (backup)','invoice.paid':'renewal-receipt','customer.subscription.deleted':'cancel-confirm','invoice.payment_failed':'payment-failed'};
  console.log(JSON.stringify({type:e.type,template:map[e.type]||null,id:e.id}));
  return res.status(200).json({received:true});
}
