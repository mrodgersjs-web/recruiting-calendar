// POST /api/checkout {offer, sport?, email?} -> Stripe Checkout (TEST MODE ONLY, sandbox guard).
// offer: <playbook slug> | sport-pack (+sport) | all-playbooks | sideline. Legacy {plan:"sideline"} still works.
// One-time offers use inline price_data (no live products created). Sideline uses STRIPE_TEST_PRICE_SIDELINE if set.
// Env: STRIPE_TEST_SECRET_KEY|STRIPE_SECRET_KEY, STRIPE_EXPECTED_TEST_ACCOUNT, STRIPE_TEST_PRICE_SIDELINE, SITE_URL, PREORDER_ENABLED
import { resolveOffer, available, TRIAL_DAYS } from '../lib/offers.js';
import { stripe, guard, body, fail, testKey } from '../lib/stripe.js';
export default async function handler(req,res){
  if(req.method!=='POST')return res.status(405).json({error:'POST only'});
  try{
    if(!testKey())return res.status(500).json({error:'Test key required; live mode disabled in this build'});
    const b=body(req); const o=resolveOffer(String(b.offer||b.plan||''),b.sport);
    if(!o)return res.status(400).json({error:'Unknown offer'});
    if(!available(o))return res.status(409).json({error:'Not available yet. Leave your email and we will send the link when it is.'});
    await guard();
    const site=process.env.SITE_URL||'http://localhost:3000';
    const p={mode:o.mode,'line_items[0][quantity]':'1',
      success_url:`${site}/welcome?session_id={CHECKOUT_SESSION_ID}`,cancel_url:`${site}/price`,
      'metadata[offer]':o.offer,'metadata[sport]':o.sport||'','metadata[slugs]':o.slugs.join(',').slice(0,500)};
    if(o.mode==='subscription'){
      if(process.env.STRIPE_TEST_PRICE_SIDELINE)p['line_items[0][price]']=process.env.STRIPE_TEST_PRICE_SIDELINE;
      else Object.assign(p,{'line_items[0][price_data][currency]':'usd','line_items[0][price_data][unit_amount]':String(o.usd*100),
        'line_items[0][price_data][recurring][interval]':'year','line_items[0][price_data][product_data][name]':o.title});
      Object.assign(p,{'subscription_data[trial_period_days]':String(TRIAL_DAYS),
        'subscription_data[trial_settings][end_behavior][missing_payment_method]':'cancel',
        'subscription_data[metadata][offer]':o.offer,payment_method_collection:'always',
        'consent_collection[terms_of_service]':'required','custom_text[submit][message]':o.disclosure});
    } else Object.assign(p,{'line_items[0][price_data][currency]':'usd','line_items[0][price_data][unit_amount]':String(o.usd*100),
      'line_items[0][price_data][product_data][name]':o.title,'custom_text[submit][message]':'One-time price. No subscription. Download link appears right after payment.'});
    if(b.email)p.customer_email=String(b.email).slice(0,254);
    const s=await stripe('POST','checkout/sessions',p);
    return res.status(200).json({url:s.url,id:s.id});
  }catch(e){return fail(res,e);}
}
