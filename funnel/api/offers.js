// GET /api/offers -> offer list with prices, availability and the trial disclosure (UI renders it next to every trial button).
import { listOffers, TRIAL_DISCLOSURE } from '../lib/offers.js';
export default function handler(req,res){ if(req.method!=='GET')return res.status(405).json({error:'GET only'});
  return res.status(200).json({test_mode:true,trial_disclosure:TRIAL_DISCLOSURE,offers:listOffers()}); }
