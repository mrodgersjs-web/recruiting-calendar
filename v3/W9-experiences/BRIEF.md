# W9 brief: authored parent experience per athlete (Mike 2026-11-06)
Mike: "build out each athlete's story using an authored experience walking parents through what was happening, what they did with the commit book and how it helped them. Separate page per athlete. Imagery to match. Each athlete has six offerings."

Input: v3/W9-experiences/INPUT.json (athletes + every offer slug with title/price/status/contents).

## Output, one file per athlete: v3/W9-experiences/out/<id>.json
{
 "id": "...",
 "headline": "<= 10 words, parent-facing",
 "dek": "1-2 sentences",
 "chapters": [  // 5 to 7 chapters, in order, each a scroll section
   {"kicker":"Sophomore spring","title":"...","what_was_happening":"2-4 sentences, the family's real situation at that moment","what_they_did":"2-3 sentences: the concrete step, naming which Commit Book offering (by slug) supports this step","how_it_helps":"1-2 sentences, honest, no promised outcome","offer":"<slug>","source_url":"<url from the athlete's timeline/basis, or null>","image_prompt":"one scene prompt (see imagery rules)"}
 ],
 "offers": ["six distinct slugs, most relevant first"],
 "closing":"1-2 sentences"
}

## TRUTH RULES (hard; a violation fails the file)
1. REAL athletes (composite=false): you may ONLY state facts present in their timeline/turning/replicate with the URL. You may NOT claim the athlete or their family used The Commit Book (it did not exist). Frame the Commit Book parts as "If your family is here today: <step> with <offer>". The parent-narrative voice is about a family in the same spot, explicitly hypothetical. No invented quotes, feelings or private details.
2. COMPOSITE athletes (composite=true): fictional; you may narrate the family using The Commit Book, but label it composite in the dek ("A composite story built from sourced paths") and never promise outcomes (no "got the scholarship because of").
3. Offers with status containing "notify" are not for sale yet: copy must say "coming soon" not "buy". Never invent prices, contents or offers outside INPUT.json.
4. No minors depicted; all figures college-age adults.

## IMAGERY RULES (image_prompt)
- Real athletes: NO likeness, no person resembling them. Use scene/object imagery only: empty stadium of the sport at dawn, gear on a bench, a parent's kitchen table with a laptop and a printed calendar, a recruiting letter envelope (no readable real logos), etc.
- Composites: may show a fictional adult athlete of the right sport, plus parent scenes with fictional adults.
- Every prompt: no real school, NCAA, brand or league logos or wordmarks; cinematic editorial photo, 16:9.

Plain, warm, specific, parent-to-parent. No hype words (unlock, empower, leverage, journey). Short sentences.
