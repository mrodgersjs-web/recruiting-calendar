// Stripe TEST-mode client with the sandbox account guard. Never talks to a live key or the live account.
// Env (Preview names): STRIPE_TEST_SECRET_KEY (falls back to STRIPE_SECRET_KEY, the name created in Vercel Preview),
// STRIPE_EXPECTED_TEST_ACCOUNT (acct_1TocAGPmz9ZnR3g8).
export const SANDBOX='acct_1TocAGPmz9ZnR3g8';
export function testKey(){const k=process.env.STRIPE_TEST_SECRET_KEY||process.env.STRIPE_SECRET_KEY||'';return k.startsWith('sk_test_')?k:null;}
export async function stripe(method,p,params){
  const key=testKey(); if(!key)throw Object.assign(new Error('Test key required; live mode disabled in this build'),{code:500});
  const opt={method,headers:{Authorization:`Bearer ${key}`}};
  if(params){opt.headers['Content-Type']='application/x-www-form-urlencoded';opt.body=new URLSearchParams(params);}
  const r=await fetch(`https://api.stripe.com/v1/${p}`,opt); const j=await r.json();
  if(!r.ok)throw Object.assign(new Error(j.error?.message||'Stripe error'),{code:502}); return j;
}
export async function guard(){
  const expected=process.env.STRIPE_EXPECTED_TEST_ACCOUNT||SANDBOX;
  if(expected!==SANDBOX)throw Object.assign(new Error('Unexpected Stripe account'),{code:500});
  const a=await stripe('GET','account');
  if(a.id!==SANDBOX)throw Object.assign(new Error('Unexpected Stripe account'),{code:500});
}
export const body=req=>typeof req.body==='string'?JSON.parse(req.body||'{}'):(req.body||{});
export const fail=(res,e)=>res.status(e.code||500).json({error:e.message});
