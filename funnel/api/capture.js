// Vercel serverless: POST /api/capture {email, sport, class_year, plan?, consent:true}
// Stores the lead in Resend Audiences (recommended) and returns the PDF link. Sends NOTHING
// unless SEND_ENABLED==="true" (stays false until Mike approves exact email text).
// Env (names only): RESEND_API_KEY, RESEND_AUDIENCE_ID, SEND_ENABLED, PDF_BASE_URL
const SPORTS=['football','baseball','track'];
export default async function handler(req,res){
  if(req.method!=='POST')return res.status(405).json({error:'POST only'});
  const b=typeof req.body==='string'?JSON.parse(req.body||'{}'):(req.body||{});
  const email=String(b.email||'').trim().toLowerCase();
  if(!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)||email.length>254)return res.status(400).json({error:'Valid email required'});
  if(b.website)return res.status(200).json({ok:true}); // honeypot
  if(b.consent!==true)return res.status(400).json({error:'Consent required'});
  const sport=SPORTS.includes(b.sport)?b.sport:'football';
  const plan=['free','sideline','pathway','audit','club'].includes(b.plan)?b.plan:'free';
  const r=await fetch(`https://api.resend.com/audiences/${process.env.RESEND_AUDIENCE_ID}/contacts`,{
    method:'POST',headers:{Authorization:`Bearer ${process.env.RESEND_API_KEY}`,'Content-Type':'application/json'},
    body:JSON.stringify({email,unsubscribed:false,first_name:`${sport}|${b.class_year||''}|${plan}`})});
  if(!r.ok&&r.status!==409)return res.status(502).json({error:'Could not save. Try again.'});
  if(process.env.SEND_ENABLED==='true'){/* welcome email send goes here after approval */}
  return res.status(200).json({ok:true,pdf:`${process.env.PDF_BASE_URL||''}/${sport}-class-2029.pdf`});
}
