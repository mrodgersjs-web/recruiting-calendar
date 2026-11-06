// POST /api/portal {customer} -> Stripe customer portal (TEST). Cancellation lives here: one click, no survey gate.
export default async function handler(req,res){
  const key=process.env.STRIPE_TEST_SECRET_KEY||'';if(!key.startsWith('sk_test_'))return res.status(500).end();
  const b=typeof req.body==='string'?JSON.parse(req.body||'{}'):(req.body||{});
  const r=await fetch('https://api.stripe.com/v1/billing_portal/sessions',{method:'POST',headers:{Authorization:`Bearer ${key}`,'Content-Type':'application/x-www-form-urlencoded'},body:new URLSearchParams({customer:String(b.customer||''),return_url:process.env.SITE_URL||'http://localhost:3000'})});
  const s=await r.json();return r.ok?res.status(200).json({url:s.url}):res.status(502).json({error:s.error?.message});
}
