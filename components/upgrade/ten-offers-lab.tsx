"use client";

import { useMemo, useState, type FormEvent } from "react";
import {
  Check,
  ChevronDown,
  ExternalLink,
  MessageSquare,
  Plus,
  Search,
  X,
} from "lucide-react";
import type { OffersCatalog, RecruitingOffer } from "./offer-types";

const STAGES = [
  "All stages",
  "Middle school",
  "Freshman",
  "Sophomore",
  "Junior",
  "Senior",
  "Transfer",
  "Parent",
] as const;

const STAGE_NEEDLES: Record<(typeof STAGES)[number], string[]> = {
  "All stages": [],
  "Middle school": ["middle school", "8th", "7th", "youth"],
  Freshman: ["freshman", "9th", "class of 2029", "class of 2030"],
  Sophomore: ["sophomore", "10th", "class of 2028"],
  Junior: ["junior", "11th", "class of 2027"],
  Senior: ["senior", "12th", "class of 2026"],
  Transfer: ["transfer", "portal"],
  Parent: ["parent", "family", "families"],
};

function deliverablesOf(offer: RecruitingOffer): string[] {
  const raw = offer.deliverable as unknown;
  if (Array.isArray(raw)) return raw.map((item) => String(item));
  if (raw == null || raw === "") return [];
  return [String(raw)];
}

function padRank(rank: number): string {
  return String(rank).padStart(2, "0");
}

function haystack(offer: RecruitingOffer): string {
  return [
    offer.title,
    offer.category,
    offer.whoItsFor,
    offer.problemSolved,
    offer.whyExistingFails,
    ...deliverablesOf(offer),
  ]
    .join(" ")
    .toLowerCase();
}

function matchesStage(offer: RecruitingOffer, stage: (typeof STAGES)[number]): boolean {
  if (stage === "All stages") return true;
  const text = haystack(offer);
  return STAGE_NEEDLES[stage].some((needle) => text.includes(needle));
}

function moneyParts(priceDisplay: string): number | null {
  const match = priceDisplay.replace(/,/g, "").match(/\$(\d+(?:\.\d+)?)/);
  if (!match) return null;
  const value = Number(match[1]);
  return Number.isFinite(value) ? value : null;
}

export default function TenOffersLab({
  catalog,
  previewMode = false,
}: {
  catalog: OffersCatalog;
  previewMode?: boolean;
}) {
  const offers = useMemo(() => catalog.offers ?? [], [catalog.offers]);
  const categories = useMemo(() => {
    const seen = new Set<string>();
    for (const offer of offers) {
      if (offer.category) seen.add(offer.category);
    }
    return ["All 10 Offers", ...seen];
  }, [offers]);

  const [category, setCategory] = useState("All 10 Offers");
  const [query, setQuery] = useState("");
  const [stage, setStage] = useState<(typeof STAGES)[number]>("All stages");
  const [openDemand, setOpenDemand] = useState<string | null>(null);
  const [waitlistFor, setWaitlistFor] = useState<string | null>(null);
  const [stack, setStack] = useState<string[]>([]);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return offers
      .filter((offer) => category === "All 10 Offers" || offer.category === category)
      .filter((offer) => matchesStage(offer, stage))
      .filter((offer) => (q ? haystack(offer).includes(q) : true))
      .slice()
      .sort((a, b) => a.rank - b.rank);
  }, [offers, category, stage, query]);

  const visible = previewMode ? offers.slice().sort((a, b) => a.rank - b.rank).slice(0, 4) : filtered;

  const stackedOffers = offers.filter((offer) => stack.includes(offer.id));
  const listedSum = stackedOffers.reduce((sum, offer) => {
    const part = moneyParts(offer.priceDisplay);
    return part == null ? sum : sum + part;
  }, 0);
  const allPriced = stackedOffers.length > 0 && stackedOffers.every((offer) => moneyParts(offer.priceDisplay) != null);

  function toggleStack(id: string) {
    setStack((current) => (current.includes(id) ? current.filter((item) => item !== id) : [...current, id]));
  }

  return (
    <section className="tol" aria-label="Athlete and family offerings lab">
      <style>{css}</style>
      <header className="tol-mast">
        <p className="tol-kicker">Field manual · Social Fetch demand</p>
        <div className="tol-mast-row">
          <h2>10 Athlete &amp; Family Offerings</h2>
          <p className="tol-meta">
            {catalog.socialSignalsCount != null ? (
              <span className="tol-num">{catalog.socialSignalsCount.toLocaleString()}</span>
            ) : null}
            {catalog.socialSignalsCount != null ? " social signals" : "Demand catalog"}
            {catalog.platformsQueried && catalog.platformsQueried.length > 0
              ? ` · ${catalog.platformsQueried.join(", ")}`
              : ""}
            {catalog.generatedAt ? ` · ${catalog.generatedAt}` : ""}
          </p>
        </div>
        <p className="tol-lede">
          Roadmap offers only. Status stays Priority Waitlist until a real product ships. Price lines are targets, not a checkout.
        </p>
      </header>

      {previewMode ? null : (
        <div className="tol-controls">
          <div className="tol-cats" role="tablist" aria-label="Offer categories">
            {categories.map((name) => (
              <button
                key={name}
                type="button"
                role="tab"
                aria-selected={category === name}
                className={category === name ? "is-on" : ""}
                onClick={() => setCategory(name)}
              >
                {name}
              </button>
            ))}
          </div>
          <div className="tol-filters">
            <label className="tol-search">
              <Search size={16} aria-hidden="true" />
              <span className="sr">Search offers</span>
              <input
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                placeholder="Search title, problem, deliverable"
                type="search"
              />
            </label>
            <label className="tol-stage">
              <span>Athlete stage</span>
              <select
                value={stage}
                onChange={(event) => setStage(event.target.value as (typeof STAGES)[number])}
              >
                {STAGES.map((name) => (
                  <option key={name} value={name}>
                    {name}
                  </option>
                ))}
              </select>
            </label>
          </div>
        </div>
      )}

      <div className={previewMode ? "tol-grid is-preview" : "tol-layout"}>
        <div className={previewMode ? "tol-grid-cards" : "tol-cards"}>
          {visible.length === 0 ? (
            <p className="tol-empty">No offers match that filter. Clear search or pick All 10 Offers.</p>
          ) : (
            visible.map((offer) => (
              <OfferCard
                key={offer.id}
                offer={offer}
                compact={previewMode}
                demandOpen={openDemand === offer.id}
                waitlistOpen={waitlistFor === offer.id}
                inStack={stack.includes(offer.id)}
                onToggleDemand={() => setOpenDemand((current) => (current === offer.id ? null : offer.id))}
                onToggleWaitlist={() => setWaitlistFor((current) => (current === offer.id ? null : offer.id))}
                onToggleStack={() => toggleStack(offer.id)}
              />
            ))
          )}
        </div>

        {previewMode ? (
          <a className="tol-all" href="/offers">
            Explore All 10 Recruiting Offers &amp; Demand Signals
          </a>
        ) : (
          <StackRail
            offers={stackedOffers}
            listedSum={listedSum}
            allPriced={allPriced}
            onRemove={toggleStack}
            onClear={() => setStack([])}
          />
        )}
      </div>
    </section>
  );
}

function OfferCard({
  offer,
  compact,
  demandOpen,
  waitlistOpen,
  inStack,
  onToggleDemand,
  onToggleWaitlist,
  onToggleStack,
}: {
  offer: RecruitingOffer;
  compact: boolean;
  demandOpen: boolean;
  waitlistOpen: boolean;
  inStack: boolean;
  onToggleDemand: () => void;
  onToggleWaitlist: () => void;
  onToggleStack: () => void;
}) {
  const items = deliverablesOf(offer).slice(0, 4);
  const evidence = offer.demandEvidence;
  const honestStatus = offer.status && !/live|buy now|stripe|checkout|for sale|purchase/i.test(offer.status)
    ? offer.status
    : null;

  return (
    <article className="tol-card">
      <header className="tol-card-head">
        <span className="tol-rank">#{padRank(offer.rank)}</span>
        <span className="tol-stamp">Priority Waitlist</span>
        {honestStatus && honestStatus !== "Priority Waitlist" ? (
          <span className="tol-status">{honestStatus}</span>
        ) : null}
      </header>
      <p className="tol-cat">{offer.category}</p>
      <h3>{offer.title}</h3>
      <p className="tol-price">{offer.priceDisplay}</p>
      <p className="tol-who">
        <span>Who it is for</span>
        {offer.whoItsFor}
      </p>
      <p className="tol-problem">{offer.problemSolved}</p>

      {compact ? null : (
        <>
          {items.length > 0 ? (
            <ul className="tol-deliv">
              {items.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          ) : null}
          <p className="tol-fail">
            <span>Why $3,000 agencies fail here</span>
            {offer.whyExistingFails}
          </p>

          <button type="button" className="tol-demand-btn" aria-expanded={demandOpen} onClick={onToggleDemand}>
            Verified Social Demand Signal
            <ChevronDown size={16} aria-hidden="true" className={demandOpen ? "is-open" : ""} />
          </button>
          {demandOpen ? (
            <div className="tol-demand">
              <p>{evidence?.summary || "No sourced summary is attached to this offer yet."}</p>
              {evidence?.postCount != null ? (
                <p className="tol-count">
                  <span className="tol-num">{evidence.postCount.toLocaleString()}</span> posts in the sample
                </p>
              ) : null}
              {evidence?.sampleSources && evidence.sampleSources.length > 0 ? (
                <ul>
                  {evidence.sampleSources.map((source) => (
                    <li key={source.url}>
                      <a href={source.url} target="_blank" rel="noopener noreferrer">
                        {source.platform}
                        <ExternalLink size={12} aria-hidden="true" />
                      </a>
                      <span>{source.signal}</span>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="tol-quiet">Sample links are not in this catalog cut.</p>
              )}
            </div>
          ) : null}

          <div className="tol-actions">
            <button type="button" className="tol-primary" onClick={onToggleWaitlist}>
              Vote + Request Early Access
            </button>
            <button type="button" className="tol-ghost" onClick={() => askGuide(offer)}>
              <MessageSquare size={15} aria-hidden="true" />
              Ask Guide If We Need This
            </button>
            <button type="button" className={inStack ? "tol-stack is-on" : "tol-stack"} onClick={onToggleStack}>
              {inStack ? <Check size={15} aria-hidden="true" /> : <Plus size={15} aria-hidden="true" />}
              {inStack ? "In stack" : "Add to stack"}
            </button>
          </div>
          {waitlistOpen ? <WaitlistForm offer={offer} /> : null}
        </>
      )}
    </article>
  );
}

function askGuide(offer: RecruitingOffer) {
  const prompt =
    offer.chatStarterPrompt ||
    `Does my athlete need ${offer.title}? Walk me through what it covers and what we can do free today.`;
  window.dispatchEvent(new CustomEvent("commitbook:ask", { detail: { prompt } }));
}

function WaitlistForm({ offer }: { offer: RecruitingOffer }) {
  const [email, setEmail] = useState("");
  const [sport, setSport] = useState("");
  const [gradYear, setGradYear] = useState("");
  const [note, setNote] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    const cleanEmail = email.trim().toLowerCase();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(cleanEmail)) {
      setNote("Enter a real parent or athlete email.");
      return;
    }
    if (!sport.trim()) {
      setNote("Name the sport.");
      return;
    }
    if (!/^20\d{2}$/.test(gradYear.trim())) {
      setNote("Graduation year needs four digits, like 2028.");
      return;
    }
    setBusy(true);
    const body = {
      email: cleanEmail,
      sport: sport.trim(),
      gradYear: gradYear.trim(),
      class_year: gradYear.trim(),
      source: `offer-waitlist:${offer.id}`,
      consent: true,
    };
    try {
      const response = await fetch("/api/capture", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      if (response.ok) {
        setNote("Request saved. This is a waitlist, not a purchase.");
      } else {
        setNote("We could not reach the list. Your request is noted on this page. Try again when you are online.");
      }
    } catch {
      setNote("Offline. Your request is noted on this page. Nothing was charged.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <form className="tol-form" onSubmit={onSubmit}>
      <p>Early access vote for {offer.title}. No card. No charge.</p>
      <label>
        Email
        <input
          type="email"
          autoComplete="email"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          required
        />
      </label>
      <label>
        Sport
        <input value={sport} onChange={(event) => setSport(event.target.value)} required />
      </label>
      <label>
        Graduation year
        <input
          inputMode="numeric"
          value={gradYear}
          onChange={(event) => setGradYear(event.target.value)}
          placeholder="2028"
          required
        />
      </label>
      <button type="submit" className="tol-primary" disabled={busy}>
        {busy ? "Sending" : "Send waitlist request"}
      </button>
      {note ? <p className="tol-note">{note}</p> : null}
    </form>
  );
}

function StackRail({
  offers,
  listedSum,
  allPriced,
  onRemove,
  onClear,
}: {
  offers: RecruitingOffer[];
  listedSum: number;
  allPriced: boolean;
  onRemove: (id: string) => void;
  onClear: () => void;
}) {
  return (
    <aside className="tol-rail" aria-label="Offer stack">
      <p className="tol-kicker">Stack builder</p>
      <h3>Family stack</h3>
      <p className="tol-quiet">Targets only. Adding an offer does not buy it.</p>
      {offers.length === 0 ? (
        <p>Add offers from the cards. The stack stays on this page.</p>
      ) : (
        <ul>
          {offers.map((offer) => (
            <li key={offer.id}>
              <span>
                <strong>#{padRank(offer.rank)}</strong> {offer.title}
                <em>{offer.priceDisplay}</em>
              </span>
              <button type="button" onClick={() => onRemove(offer.id)} aria-label={`Remove ${offer.title}`}>
                <X size={14} aria-hidden="true" />
              </button>
            </li>
          ))}
        </ul>
      )}
      <p className="tol-sum">
        {offers.length === 0
          ? "No price target yet"
          : allPriced
            ? `Listed targets add to $${listedSum.toLocaleString()}`
            : "Mixed price lines. Read each card. No combined checkout."}
      </p>
      {offers.length > 0 ? (
        <button type="button" className="tol-textbtn" onClick={onClear}>
          Clear stack
        </button>
      ) : null}
    </aside>
  );
}

const css = `
.tol{background:#f7f5f0;color:#141413;font-family:"Inter Tight","Plus Jakarta Sans",system-ui,sans-serif;padding:28px 20px 40px;border:1px solid #e5e0d6}
.tol *{box-sizing:border-box}
.tol-num{font-variant-numeric:tabular-nums;font-family:"JetBrains Mono",ui-monospace,monospace}
.tol-kicker{margin:0 0 8px;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#57534e;font-weight:600}
.tol-mast h2{margin:0;font-family:"Barlow Condensed","Arial Narrow",sans-serif;font-weight:700;font-size:clamp(32px,5vw,52px);letter-spacing:-.01em;line-height:.95;text-transform:uppercase}
.tol-mast-row{display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px;align-items:end}
.tol-meta,.tol-lede,.tol-quiet{color:#57534e}
.tol-lede{max-width:68ch;margin:12px 0 0;line-height:1.55}
.tol-controls{margin-top:22px;display:grid;gap:12px}
.tol-cats{display:flex;flex-wrap:wrap;gap:8px}
.tol-cats button,.tol-stage select,.tol-search input,.tol-form input{font:inherit;color:#141413;background:#fff;border:1px solid #e5e0d6}
.tol-cats button{padding:8px 12px;border-radius:999px;cursor:pointer}
.tol-cats button.is-on{background:#141413;color:#fff;border-color:#141413}
.tol-filters{display:flex;flex-wrap:wrap;gap:10px}
.tol-search{display:flex;align-items:center;gap:8px;background:#fff;border:1px solid #e5e0d6;padding:0 12px;min-width:min(100%,280px);flex:1}
.tol-search input{border:0;padding:10px 0;width:100%;outline:none}
.tol-stage{display:flex;flex-direction:column;gap:4px;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:#57534e}
.tol-stage select{padding:10px 12px;text-transform:none;letter-spacing:0;font-size:15px}
.tol-layout{margin-top:22px;display:grid;grid-template-columns:minmax(0,1fr) 280px;gap:18px;align-items:start}
.tol-cards,.tol-grid-cards{display:grid;gap:14px}
.tol-grid{margin-top:22px}
.tol-grid-cards{grid-template-columns:1fr 1fr}
.tol-card{background:#fff;border:1px solid #e5e0d6;padding:18px 18px 16px}
.tol-card-head{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.tol-rank{font-family:"JetBrains Mono",ui-monospace,monospace;font-variant-numeric:tabular-nums;font-size:13px;color:#1d4ed8}
.tol-stamp{background:#b91c1c;color:#fff;font-size:11px;letter-spacing:.08em;text-transform:uppercase;padding:4px 8px;font-weight:600}
.tol-status{font-size:12px;color:#57534e;border:1px solid #e5e0d6;padding:3px 8px}
.tol-cat{margin:12px 0 0;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:#57534e}
.tol-card h3{margin:6px 0 0;font-size:22px;line-height:1.2;font-family:"Newsreader",Georgia,serif;font-weight:560}
.tol-price{margin:8px 0 0;font-family:"JetBrains Mono",ui-monospace,monospace;font-variant-numeric:tabular-nums;font-size:18px}
.tol-who,.tol-fail{margin:12px 0 0;font-size:14px;line-height:1.5}
.tol-who span,.tol-fail span{display:block;font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#57534e;margin-bottom:4px}
.tol-problem{margin:10px 0 0;line-height:1.55}
.tol-deliv{margin:12px 0 0;padding:0;list-style:none;display:grid;gap:6px}
.tol-deliv li{padding-left:14px;position:relative;font-size:14px;line-height:1.45}
.tol-deliv li:before{content:"";position:absolute;left:0;top:.55em;width:6px;height:6px;background:#1d4ed8}
.tol-demand-btn,.tol-primary,.tol-ghost,.tol-stack,.tol-textbtn{font:inherit;cursor:pointer}
.tol-demand-btn{margin-top:14px;width:100%;display:flex;justify-content:space-between;align-items:center;background:transparent;border:0;border-top:1px solid #e5e0d6;padding:12px 0 0;color:#141413;text-align:left}
.tol-demand-btn svg{transition:transform .2s ease}
.tol-demand-btn svg.is-open{transform:rotate(180deg)}
.tol-demand{margin-top:10px;padding:12px;background:#f7f5f0;border:1px solid #e5e0d6;font-size:14px;line-height:1.5}
.tol-demand ul{margin:10px 0 0;padding:0;list-style:none;display:grid;gap:8px}
.tol-demand a{color:#1d4ed8;display:inline-flex;gap:4px;align-items:center}
.tol-demand li span{display:block;color:#57534e}
.tol-count{font-variant-numeric:tabular-nums}
.tol-actions{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.tol-primary{background:#1d4ed8;color:#fff;border:0;padding:10px 12px}
.tol-primary:disabled{opacity:.6}
.tol-ghost,.tol-stack{background:#fff;border:1px solid #e5e0d6;padding:10px 12px;display:inline-flex;gap:6px;align-items:center}
.tol-stack.is-on{border-color:#141413}
.tol-form{margin-top:12px;display:grid;gap:8px;padding:12px;border:1px solid #e5e0d6;background:#f7f5f0}
.tol-form label{display:grid;gap:4px;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:#57534e}
.tol-form input{padding:10px;text-transform:none;letter-spacing:0;font-size:15px}
.tol-note{margin:0;font-size:14px}
.tol-rail{position:sticky;top:16px;background:#fff;border:1px solid #e5e0d6;padding:16px}
.tol-rail h3{margin:0 0 8px;font-family:"Barlow Condensed","Arial Narrow",sans-serif;text-transform:uppercase;font-size:28px;line-height:1}
.tol-rail ul{list-style:none;margin:12px 0 0;padding:0;display:grid;gap:8px}
.tol-rail li{display:flex;justify-content:space-between;gap:8px;align-items:start;font-size:14px}
.tol-rail em{display:block;font-style:normal;color:#57534e;font-variant-numeric:tabular-nums;font-family:"JetBrains Mono",ui-monospace,monospace;font-size:12px}
.tol-rail button{background:transparent;border:0;cursor:pointer;color:#141413}
.tol-sum{margin:14px 0 0;font-variant-numeric:tabular-nums;font-weight:600}
.tol-textbtn{margin-top:8px;background:transparent;border:0;color:#1d4ed8;padding:0}
.tol-all{display:inline-block;margin-top:16px;color:#1d4ed8;font-weight:600}
.tol-empty{margin:0}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
@media (max-width:860px){
  .tol-layout,.tol-grid-cards{grid-template-columns:1fr}
  .tol-rail{position:static}
}
`;
