// Vercel serverless: POST /api/capture {email, sport, class_year, plan?, source?, tool_slug?, consent:true}
// Stores the lead in Resend Audiences (recommended) and returns the PDF link. Sends NOTHING
// unless SEND_ENABLED==="true" (stays false until Mike approves exact email text).
// Env (names only): RESEND_API_KEY, RESEND_AUDIENCE_ID, SEND_ENABLED, PDF_BASE_URL
// Routing: source / tool_slug (which tool the visitor asked to be notified about) and class_year are preserved in the stored
// record (first_name = sport|class_year|plan|source) and echoed in the response. Sport is normalised to football|baseball|track;
// an unspecified/unknown sport is NOT guessed and falls back to the generic recruiting-calendar-class-2029.pdf.
import { books, SPORTS } from '../lib/offers.js';
const slug=v=>String(v||'').toLowerCase().replace(/[^a-z0-9_-]/g,'').slice(0,64);
// plan may be the free giveaway or any offer slug (checkout fallback posts the offer here).
export default async function handler(req,res){
  if(req.method!=='POST')return res.status(405).json({error:'POST only'});
  const b=typeof req.body==='string'?JSON.parse(req.body||'{}'):(req.body||{});
  const email=String(b.email||'').trim().toLowerCase();
  if(!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)||email.length>254)return res.status(400).json({error:'Valid email required'});
  if(b.website)return res.status(200).json({ok:true}); // honeypot
  if(b.consent!==true)return res.status(400).json({error:'Consent required'});
  const sp=String(b.sport||'').trim().toLowerCase();
  const sport=SPORTS.includes(sp)?sp:null;
  const OFFERS=['free','giveaway','sideline','sport-pack','all-playbooks','pathway','audit','club',...Object.keys(books)];
  const plan=OFFERS.includes(b.plan)?b.plan:'free';
  const source=slug(b.source||b.tool_slug), tool_slug=slug(b.tool_slug||b.source);
  const class_year=/^20\d{2}$/.test(String(b.class_year||''))?String(b.class_year):'';
  if(!process.env.RESEND_API_KEY||!process.env.RESEND_AUDIENCE_ID)return res.status(503).json({error:'Sign-up is not connected in this preview. Nothing was saved.'});
  const r=await fetch(`https://api.resend.com/audiences/${process.env.RESEND_AUDIENCE_ID}/contacts`,{
    method:'POST',headers:{Authorization:`Bearer ${process.env.RESEND_API_KEY}`,'Content-Type':'application/json'},
    body:JSON.stringify({email,unsubscribed:false,first_name:`${sport||'unspecified'}|${class_year}|${plan}|${source}`})});
  if(!r.ok&&r.status!==409)return res.status(502).json({error:'Could not save. Try again.'});
  if(process.env.SEND_ENABLED==='true'){/* welcome email send goes here after approval */}
  // Only class-2029 PDFs exist, so class_year is recorded but does not build the path.
  const pdf=`${process.env.PDF_BASE_URL||''}/${sport?`${sport}-class-2029`:'recruiting-calendar-class-2029'}.pdf`;
  return res.status(200).json({ok:true,pdf,sport,class_year,plan,source,tool_slug});
}
