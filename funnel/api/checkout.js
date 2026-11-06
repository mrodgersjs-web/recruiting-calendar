// Vercel serverless: POST /api/checkout {email?, plan:"sideline"} -> Stripe Checkout (TEST MODE ONLY).
// Refuses any key that is not sk_test_ and any account other than the sandbox, so it cannot charge.
// Env: STRIPE_TEST_SECRET_KEY, STRIPE_TEST_PRICE_SIDELINE, STRIPE_EXPECTED_TEST_ACCOUNT (acct_1TocAGPmz9ZnR3g8), SITE_URL
export default async function handler(req,res){
  if(req.method!=='POST')return res.status(405).json({error:'POST only'});
  const key=process.env.STRIPE_TEST_SECRET_KEY||'';
  if(!key.startsWith('sk_test_'))return res.status(500).json({error:'Test key required; live mode disabled in this build'});
  const auth={Authorization:`Bearer ${key}`};
  const acct=await (await fetch('https://api.stripe.com/v1/account',{headers:auth})).json();
  if(acct.id!==process.env.STRIPE_EXPECTED_TEST_ACCOUNT)return res.status(500).json({error:'Unexpected Stripe account'});
  const b=typeof req.body==='string'?JSON.parse(req.body||'{}'):(req.body||{});
  const site=process.env.SITE_URL||'http://localhost:3000';
  const p=new URLSearchParams({
    mode:'subscription','line_items[0][price]':process.env.STRIPE_TEST_PRICE_SIDELINE,'line_items[0][quantity]':'1',
    'subscription_data[trial_period_days]':'14',
    'subscription_data[trial_settings][end_behavior][missing_payment_method]':'cancel',
    payment_method_collection:'always','consent_collection[terms_of_service]':'required',
    'custom_text[submit][message]':'Free for 14 days, then $149 per year, renewing yearly until you cancel. Cancel any time online in one click. We email you 7 days before the trial ends.',
    success_url:`${site}/welcome?session_id={CHECKOUT_SESSION_ID}`,cancel_url:`${site}/#pricing`});
  if(b.email)p.set('customer_email',String(b.email));
  const r=await fetch('https://api.stripe.com/v1/checkout/sessions',{method:'POST',headers:{...auth,'Content-Type':'application/x-www-form-urlencoded'},body:p});
  const s=await r.json(); if(!r.ok)return res.status(502).json({error:s.error?.message});
  return res.status(200).json({url:s.url});
}
