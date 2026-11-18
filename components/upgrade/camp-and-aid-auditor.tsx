"use client";

import { useMemo, useState } from "react";
import {
  BookOpen,
  CircleDollarSign,
  ClipboardCheck,
  Mail,
  MapPin,
  Users,
} from "lucide-react";

type TabId = "camp" | "aid";
type VerdictKind = "green" | "selective" | "skip";
type GpaId = "g370" | "g330" | "g300" | "g230" | "g220" | "glow";

type GpaRow = {
  id: GpaId;
  label: string;
  d3: [number, number];
  other: [number, number];
};

type AidRow = {
  id: string;
  name: string;
  rule: string;
  base: number;
  baseLabel: string;
  athletic: [number, number];
  academic: [number, number];
  athleticNote: string;
  stackNote: string;
  fourYear: [number, number];
};

const LOCAL_CAP = 400;
const DESTINATION_FLOOR = 1500;
const ONE_DAY_CAMP = [49, 125] as const;
const SHOWCASE_PACKAGE = 1950;

const GPA_ROWS: GpaRow[] = [
  { id: "g370", label: "3.70 or higher", d3: [0.45, 0.7], other: [0.15, 0.35] },
  { id: "g330", label: "3.30 to 3.69", d3: [0.35, 0.55], other: [0.1, 0.25] },
  { id: "g300", label: "3.00 to 3.29", d3: [0.25, 0.45], other: [0.05, 0.15] },
  { id: "g230", label: "2.30 to 2.99", d3: [0.15, 0.3], other: [0, 0.08] },
  { id: "g220", label: "2.20 to 2.29", d3: [0.1, 0.22], other: [0, 0.05] },
  { id: "glow", label: "Below 2.20", d3: [0.05, 0.15], other: [0, 0] },
];

const QUESTIONS: {
  key: "email" | "staff" | "ratio" | "cost" | "film";
  n: string;
  title: string;
  detail: string;
  icon: typeof Mail;
}[] = [
  {
    key: "email",
    n: "01",
    title: "Personal email from the position coach?",
    detail:
      "A named position coach wrote your athlete. A mass camp blast from a third-party promoter does not count.",
    icon: Mail,
  },
  {
    key: "staff",
    n: "02",
    title: "Target-list coaches on the field, in a legal window?",
    detail:
      "Coaches from schools he can actually reach will work that field or court during a legal evaluation period. A logo on a flyer is not a staff.",
    icon: Users,
  },
  {
    key: "ratio",
    n: "03",
    title: "Coach-to-athlete ratio under 1:12, with a verified roster?",
    detail:
      "Under 1 coach per 12 athletes, and the camp publishes who is testing and how times are recorded. A college's own camp, an electronic combine, or a documented laser session is a verified time. Hand-timed is not.",
    icon: ClipboardCheck,
  },
  {
    key: "cost",
    n: "04",
    title: "All-in trip under $400, not a $1,500 destination?",
    detail:
      "Hotel, flights, entry, and meals. The book checked one-day school camps at $49 to $125, and multi-day camps at $400 to $800 before travel. A visit weekend runs $500 to $1,500. A showcase package runs about $1,950.",
    icon: MapPin,
  },
  {
    key: "film",
    n: "05",
    title: "Film and transcript already sent, two weeks prior?",
    detail:
      "Verified game film and the academic transcript are already with those coaches, at least two weeks before the camp. Staffs use camp to look at players already on their list.",
    icon: BookOpen,
  },
];

function money(value: number): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(Math.round(value));
}

function clampMoney(raw: string, fallback: number): number {
  const n = Number(raw.replace(/[^0-9.]/g, ""));
  if (!Number.isFinite(n) || n < 0) return fallback;
  return Math.min(250000, Math.round(n));
}

function span(base: number, band: [number, number]): [number, number] {
  return [Math.round(base * band[0]), Math.round(base * band[1])];
}

function payRange(base: number, aidLow: number, aidHigh: number): [number, number] {
  const highPay = Math.max(0, base - aidLow);
  const lowPay = Math.max(0, base - Math.min(base, aidHigh));
  return [lowPay, highPay];
}

function verdictOf(flags: boolean[], trip: number): VerdictKind {
  const [email, staff, , cheap] = flags;
  const yesCount = flags.filter(Boolean).length;
  if (email && staff && cheap && yesCount >= 4) return "green";
  if (yesCount <= 1 || (!email && !staff) || (trip >= DESTINATION_FLOOR && !email)) return "skip";
  return "selective";
}

function savedDollars(kind: VerdictKind, trip: number): number {
  if (kind === "skip") return trip;
  if (kind === "selective") return Math.max(0, trip - LOCAL_CAP);
  return 0;
}

const VERDICT_COPY: Record<
  VerdictKind,
  { stamp: string; tone: "green" | "blue" | "red"; lead: string }
> = {
  green: {
    stamp: "GREEN LIGHT: WORTH THE TRIP",
    tone: "green",
    lead: "A position coach wrote you, staff from the target list will be on the field in a legal window, and the bill is in the local range. That is the camp the book says to pay for.",
  },
  selective: {
    stamp: "SELECTIVE: GO ONLY IF LOCAL",
    tone: "blue",
    lead: "Some checks pass. Go only if this is a drive, the all-in bill stays under $400, and a coach who can recruit him has already answered. If it needs a flight, skip it.",
  },
  skip: {
    stamp: "SKIP: CLASSIC CAMP MONEY TRAP",
    tone: "red",
    lead: "This reads like a promoter blast, a field without your target staff, or a destination bill. Named coaches have said 7-on-7 film does not recruit, and paid services go in the trash. Stay home.",
  },
};

function buildAidRows(sticker: number, juco: number, gpa: GpaRow): AidRow[] {
  const d1Athletic: [number, number] =
    gpa.id === "glow" || gpa.id === "g220" ? [0, 0] : [0, 0.5];
  const d2Athletic: [number, number] = gpa.id === "glow" ? [0, 0] : [0, 0.5];
  const naiaAthletic: [number, number] = [0, 0.5];
  const jucoAthletic: [number, number] = [0, 1];
  const jucoAcademic: [number, number] = [0, 0.15];

  const d1Academic = gpa.other;
  const d2Academic = gpa.other;
  const d3Academic = gpa.d3;
  const naiaAcademic = gpa.other;

  const rows: Omit<AidRow, "fourYear">[] = [
    {
      id: "d1",
      name: "NCAA Division I",
      rule: "Roster cap 105 at settlement schools (Bylaw 17.2, 1 July 2025). Non-opted schools still work to 85 counters. FCS aid is 63.0 equivalencies, and a partial is the normal outcome.",
      base: sticker,
      baseLabel: "Four-year sticker",
      athletic: span(sticker, d1Athletic),
      academic: span(sticker, d1Academic),
      athleticNote:
        gpa.id === "glow" || gpa.id === "g220"
          ? "Core-course floor for Division I is 2.3. Below that, do not plan on Division I athletic aid."
          : "70% of Division I athletes receive some athletic aid. Plan the partial, not a full grant. Revenue share is not a scholarship and is not in this figure.",
      stackNote:
        "Ask whether academic money counts against the team limit. Count both only after the school says so in writing.",
    },
    {
      id: "d2",
      name: "NCAA Division II",
      rule: "36.0 equivalencies per team. No national roster cap. Real money, spread thin.",
      base: sticker,
      baseLabel: "Four-year sticker",
      athletic: span(sticker, d2Athletic),
      academic: span(sticker, d2Academic),
      athleticNote:
        gpa.id === "glow"
          ? "Core-course floor for Division II is 2.2. Below that, do not plan on Division II athletic aid."
          : "77% receive some athletic aid. The book says expect a quarter or a half of one year's bill, then compare that partial with academic aid.",
      stackNote:
        "Do not add the partial and the academic award until the aid office confirms they can sit together.",
    },
    {
      id: "d3",
      name: "NCAA Division III",
      rule: "No athletic aid at all (15.01.3). Aid comes from the normal financial aid office. Largest group of football players, and the group most families skip.",
      base: sticker,
      baseLabel: "Four-year sticker",
      athletic: [0, 0],
      academic: span(sticker, d3Academic),
      athleticNote:
        "Athletic scholarship: $0. 80% of Division III athletes receive help from the aid office. That help is often part of the bill, not a free ride.",
      stackNote: "There is no athletic grant to stack. The aid-office range is the planning number.",
    },
    {
      id: "naia",
      name: "NAIA",
      rule: "24 full-grant equivalents per team, splittable. No roster cap in the playbook. Genuine money, often at a lower cost of living.",
      base: sticker,
      baseLabel: "Four-year sticker",
      athletic: span(sticker, naiaAthletic),
      academic: span(sticker, naiaAcademic),
      athleticNote:
        "Partials are the normal shape of 24 equivalents. Read the school's own paper. This band is not an NAIA award letter.",
      stackNote: "Stack only what that school's award letter names. A verbal stack is not money.",
    },
    {
      id: "njcaa",
      name: "NJCAA",
      rule: "85 letters per team, and the paper binds one year, not four. NJCAA Division 2 pays tuition only. NJCAA Division 3 pays nothing. Those are NJCAA divisions, not NCAA ones.",
      base: juco,
      baseLabel: "Junior college annual cost",
      athletic: span(juco, jucoAthletic),
      academic: span(juco, jucoAcademic),
      athleticNote:
        "High end is tuition covered, and only at a junior college that actually pays tuition. The low end is a school that pays nothing.",
      stackNote:
        "Treat this as a two-year runway, then a transfer. No four-year athletic aid is promised on the other side.",
    },
  ];

  return rows.map((row) => {
    if (row.id !== "njcaa") {
      const single = payRange(
        row.base,
        Math.max(row.athletic[0], row.academic[0]),
        Math.max(row.athletic[1], row.academic[1]),
      );
      return { ...row, fourYear: [single[0] * 4, single[1] * 4] };
    }
    const jucoSingle = payRange(
      juco,
      Math.max(row.athletic[0], row.academic[0]),
      Math.max(row.athletic[1], row.academic[1]),
    );
    const transferMerit = span(sticker, gpa.other);
    const transferPay = payRange(sticker, transferMerit[0], transferMerit[1]);
    return {
      ...row,
      fourYear: [
        jucoSingle[0] * 2 + transferPay[0] * 2,
        jucoSingle[1] * 2 + transferPay[1] * 2,
      ],
    };
  });
}

export function CampAndAidAuditor() {
  const [tab, setTab] = useState<TabId>("camp");
  const [email, setEmail] = useState(false);
  const [staff, setStaff] = useState(false);
  const [ratio, setRatio] = useState(false);
  const [film, setFilm] = useState(false);
  const [tripRaw, setTripRaw] = useState("1500");
  const [asked, setAsked] = useState(false);
  const [stickerRaw, setStickerRaw] = useState("45000");
  const [jucoRaw, setJucoRaw] = useState("6500");
  const [gpaId, setGpaId] = useState<GpaId>("g330");

  const trip = clampMoney(tripRaw, 1500);
  const sticker = clampMoney(stickerRaw, 45000);
  const juco = clampMoney(jucoRaw, 6500);
  const cheap = trip < LOCAL_CAP;
  const flags = [email, staff, ratio, cheap, film];
  const yesCount = flags.filter(Boolean).length;
  const kind = verdictOf(flags, trip);
  const saved = savedDollars(kind, trip);
  const copy = VERDICT_COPY[kind];
  const gpa = GPA_ROWS.find((row) => row.id === gpaId) ?? GPA_ROWS[1];

  const aidRows = useMemo(() => buildAidRows(sticker, juco, gpa), [sticker, juco, gpa]);

  const answers = {
    email,
    staff,
    ratio,
    cheap,
    film,
  };

  function setFlag(key: (typeof QUESTIONS)[number]["key"], yes: boolean) {
    setAsked(false);
    if (key === "email") setEmail(yes);
    if (key === "staff") setStaff(yes);
    if (key === "ratio") setRatio(yes);
    if (key === "film") setFilm(yes);
    if (key === "cost") setTripRaw(yes ? (trip < LOCAL_CAP ? String(trip) : "350") : trip >= LOCAL_CAP ? String(trip) : "1500");
  }

  function flagValue(key: (typeof QUESTIONS)[number]["key"]): boolean {
    if (key === "email") return email;
    if (key === "staff") return staff;
    if (key === "ratio") return ratio;
    if (key === "film") return film;
    return cheap;
  }

  function askGuide() {
    const lines = QUESTIONS.map((q) => `${q.n} ${flagValue(q.key) ? "YES" : "NO"}: ${q.title}`).join("\n");
    const prompt = [
      "Audit this camp invite against Commit Book camp rules.",
      `Scorer verdict: ${copy.stamp}.`,
      `Yes count: ${yesCount} of 5.`,
      `All-in trip cost: ${money(trip)}.`,
      `Estimated dollars saved by not taking the trap path: ${money(saved)}.`,
      lines,
      "Rules to apply: go only where a coach has answered in writing and will watch; skip promoter blasts, 7-on-7 circuits sold as recruiting, and destination showcases at $1,500 or more. One-day school camps the book checked were $49 to $125.",
    ].join("\n");
    window.dispatchEvent(new CustomEvent("commitbook:ask", { detail: { prompt, source: "camp-and-aid-auditor", verdict: kind, answers, tripCost: trip, saved } }));
    setAsked(true);
  }

  return (
    <section className="caa" aria-label="Camp invite red-flag test and college aid reality calculator">
      <style>{css}</style>
      <header className="caa-mast">
        <p className="caa-kicker">Field manual · Camps and aid</p>
        <h2>Camp Invite Red-Flag Test and 4-Year College Aid Reality Calculator</h2>
        <p className="caa-lede">
          Two checks before a family spends. A camp is worth the money when a coach who can recruit him will be there and already knows his name. Aid is a published limit and an aid-office letter, not a camp brochure.
        </p>
      </header>

      <div className="caa-tabs" role="tablist" aria-label="Auditor">
        <button type="button" role="tab" aria-selected={tab === "camp"} className={tab === "camp" ? "is-on" : ""} onClick={() => setTab("camp")}>
          5-point camp scorer
        </button>
        <button type="button" role="tab" aria-selected={tab === "aid"} className={tab === "aid" ? "is-on" : ""} onClick={() => setTab("aid")}>
          Division aid reality
        </button>
      </div>

      {tab === "camp" ? (
        <div className="caa-split" role="tabpanel">
          <div className="caa-card">
            <p className="caa-label">Five questions. Yes only if you can point to the email, the staff list, or the receipt.</p>
            <ol className="caa-qs">
              {QUESTIONS.map((q) => {
                const on = flagValue(q.key);
                const Icon = q.icon;
                return (
                  <li key={q.key}>
                    <div className="caa-qhead">
                      <span className="caa-num">{q.n}</span>
                      <Icon size={16} aria-hidden="true" />
                      <h3>{q.title}</h3>
                    </div>
                    <p>{q.detail}</p>
                    <div className="caa-toggle" role="group" aria-label={q.title}>
                      <button type="button" aria-pressed={on} className={on ? "is-yes" : ""} onClick={() => setFlag(q.key, true)}>
                        Yes
                      </button>
                      <button type="button" aria-pressed={!on} className={!on ? "is-no" : ""} onClick={() => setFlag(q.key, false)}>
                        No
                      </button>
                    </div>
                  </li>
                );
              })}
            </ol>
            <label className="caa-field">
              <span>All-in trip cost (entry, hotel, flights, meals)</span>
              <input
                inputMode="numeric"
                value={tripRaw}
                onChange={(event) => {
                  setAsked(false);
                  setTripRaw(event.target.value);
                }}
                aria-describedby="caa-cost-note"
              />
            </label>
            <p id="caa-cost-note" className="caa-note">
              Under {money(LOCAL_CAP)} marks question 04 yes. {money(DESTINATION_FLOOR)} or more is the destination column. One-day school camps checked 11 Nov 2026: {money(ONE_DAY_CAMP[0])} to {money(ONE_DAY_CAMP[1])}.
            </p>
          </div>

          <aside className="caa-card caa-verdict">
            <p className="caa-label">
              {yesCount} of 5 checks
            </p>
            <p className={`caa-stamp ${copy.tone}`}>{copy.stamp}</p>
            <p className="caa-lead">{copy.lead}</p>
            <p className="caa-saved-label">Estimated dollars saved</p>
            <p className="caa-saved">{money(saved)}</p>
            <p className="caa-note">
              {kind === "green"
                ? "Skipping a camp a coach already agreed to watch does not save money. It costs the look. A trap weekend at this same time of year is $1,500 or more, or about $1,950 for a full showcase package."
                : kind === "selective"
                  ? saved > 0
                    ? `That figure is this trip minus a local camp under ${money(LOCAL_CAP)}. Pay the local bill only if the coach checks still hold.`
                    : "The bill is already in the local range. Go only if the coach email and the staff list are real."
                  : `Stay home and this ${money(trip)} stays in the family account. A full showcase package the book priced at about ${money(SHOWCASE_PACKAGE)} is the same trap, one size up.`}
            </p>
            <button type="button" className="caa-ask" onClick={askGuide}>
              <CircleDollarSign size={16} aria-hidden="true" />
              Ask Commit Book Guide to Audit My Camp Invite
            </button>
            <p className="caa-note" role="status">
              {asked
                ? "Sent to the guide in this browser. Nothing was emailed, and no camp was booked."
                : "The button hands this score to the guide. It does not contact a coach."}
            </p>
          </aside>
        </div>
      ) : (
        <div role="tabpanel">
          <div className="caa-card caa-inputs">
            <label className="caa-field">
              <span>Annual four-year sticker (tuition, fees, room, board)</span>
              <input
                inputMode="numeric"
                value={stickerRaw}
                onChange={(event) => setStickerRaw(event.target.value)}
              />
            </label>
            <label className="caa-field">
              <span>Junior college annual cost</span>
              <input inputMode="numeric" value={jucoRaw} onChange={(event) => setJucoRaw(event.target.value)} />
            </label>
            <label className="caa-field">
              <span>Unweighted GPA band</span>
              <select value={gpaId} onChange={(event) => setGpaId(event.target.value as GpaId)}>
                {GPA_ROWS.map((row) => (
                  <option key={row.id} value={row.id}>
                    {row.label}
                  </option>
                ))}
              </select>
            </label>
            <p className="caa-note">
              Replace both dollar fields with the school&apos;s published cost. GPA here is a planning proxy. The NCAA number is core-course GPA: 2.3 for Division I, 2.2 for Division II. A counselor certifies which classes count.
            </p>
          </div>

          <div className="caa-aid">
            {aidRows.map((row) => {
              const singleLow = Math.max(row.athletic[0], row.academic[0]);
              const singleHigh = Math.max(row.athletic[1], row.academic[1]);
              const singlePay = payRange(row.base, singleLow, singleHigh);
              const stackPay = payRange(
                row.base,
                row.athletic[0] + row.academic[0],
                row.athletic[1] + row.academic[1],
              );
              return (
                <article key={row.id} className="caa-card">
                  <header className="caa-aid-head">
                    <h3>{row.name}</h3>
                    <p className="caa-num">{row.baseLabel}</p>
                  </header>
                  <p>{row.rule}</p>
                  <dl className="caa-dl">
                    <div>
                      <dt>Sticker used</dt>
                      <dd>{money(row.base)}</dd>
                    </div>
                    <div>
                      <dt>Athletic planning range</dt>
                      <dd>
                        {money(row.athletic[0])} to {money(row.athletic[1])}
                      </dd>
                    </div>
                    <div>
                      <dt>Academic or aid-office range</dt>
                      <dd>
                        {money(row.academic[0])} to {money(row.academic[1])}
                      </dd>
                    </div>
                    <div>
                      <dt>Family pays, no double count</dt>
                      <dd>
                        {money(singlePay[0])} to {money(singlePay[1])}
                      </dd>
                    </div>
                    <div>
                      <dt>Family pays if stacking is in writing</dt>
                      <dd>
                        {money(stackPay[0])} to {money(stackPay[1])}
                      </dd>
                    </div>
                    <div>
                      <dt>4-year family planning total</dt>
                      <dd>
                        {money(row.fourYear[0])} to {money(row.fourYear[1])}
                      </dd>
                    </div>
                  </dl>
                  <p className="caa-note">{row.athleticNote}</p>
                  <p className="caa-note">{row.stackNote}</p>
                </article>
              );
            })}
          </div>

          <div className="caa-card caa-compare">
            <h3>Same sticker, four years, no double count</h3>
            <table>
              <thead>
                <tr>
                  <th>Path</th>
                  <th>4-year family range</th>
                  <th>Versus paying sticker for 4 years ({money(sticker * 4)})</th>
                </tr>
              </thead>
              <tbody>
                {aidRows.map((row) => {
                  const gapLow = sticker * 4 - row.fourYear[1];
                  const gapHigh = sticker * 4 - row.fourYear[0];
                  return (
                    <tr key={row.id}>
                      <td>{row.name}</td>
                      <td>
                        {money(row.fourYear[0])} to {money(row.fourYear[1])}
                      </td>
                      <td>
                        {gapHigh < 0
                          ? "Not comparable: junior college years use the lower bill, then two transfer years with no athletic aid promised."
                          : `${money(Math.min(gapLow, gapHigh))} to ${money(Math.max(gapLow, gapHigh))} less than full sticker, if the planning band holds.`}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
            <p className="caa-note">
              Educational planning ranges from The Commit Book Football Playbook 2026-27 and the roster-math page: NCAA March 2026 figures (70% of Division I athletes and 77% in Division II receive some athletic aid; 80% of Division III athletes receive aid-office help), Bylaw 17.2 roster limit 105, Division II 36.0 equivalencies, Division III Bylaw 15.01.3, NAIA 24 equivalents, NJCAA one-year letters. &quot;Some aid&quot; often means part of tuition. Nothing here is an offer, a revenue-share promise, or a guarantee.
            </p>
          </div>
        </div>
      )}
    </section>
  );
}

export default CampAndAidAuditor;

const css = `
.caa{background:#f7f5f0;color:#141413;font-family:"Inter Tight","Plus Jakarta Sans",Georgia,system-ui,sans-serif;padding:28px 20px 40px;border:1px solid #e5e0d6}
.caa-mast h2{font-family:Georgia,"Iowan Old Style","Palatino Linotype",serif;font-size:clamp(28px,4vw,40px);line-height:1.15;font-weight:650;margin:8px 0 10px;letter-spacing:-0.02em}
.caa-kicker{margin:0;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:#57534e}
.caa-lede,.caa p,.caa-lead{font-size:16px;line-height:1.5;color:#141413}
.caa-lede{max-width:68ch;margin:0}
.caa-tabs{display:flex;gap:8px;margin:22px 0 16px;flex-wrap:wrap}
.caa-tabs button{background:#fff;color:#141413;border:1px solid #e5e0d6;padding:10px 14px;font:inherit;cursor:pointer}
.caa-tabs button.is-on{background:#141413;color:#f7f5f0;border-color:#141413}
.caa-split{display:grid;grid-template-columns:minmax(0,1.45fr) minmax(260px,.8fr);gap:16px;align-items:start}
.caa-card{background:#fff;border:1px solid #e5e0d6;padding:16px 16px 18px}
.caa-label{margin:0 0 12px;color:#57534e;font-size:13px;letter-spacing:.04em;text-transform:uppercase}
.caa-qs{list-style:none;margin:0;padding:0;display:grid;gap:14px}
.caa-qs li{border-top:1px solid #e5e0d6;padding-top:12px}
.caa-qs li:first-child{border-top:0;padding-top:0}
.caa-qhead{display:flex;gap:8px;align-items:flex-start}
.caa-qhead h3{margin:0;font-size:16px;line-height:1.35;font-weight:650}
.caa-qhead svg{flex:none;margin-top:2px;color:#1d4ed8}
.caa-num{font-family:"JetBrains Mono",ui-monospace,monospace;font-variant-numeric:tabular-nums;color:#1d4ed8;font-size:13px;flex:none}
.caa-qs p{margin:6px 0 10px;color:#57534e;font-size:14px}
.caa-toggle{display:flex;gap:8px}
.caa-toggle button{font:inherit;border:1px solid #e5e0d6;background:#f7f5f0;color:#141413;padding:8px 14px;cursor:pointer;min-width:72px}
.caa-toggle button.is-yes{background:#15803d;color:#fff;border-color:#15803d}
.caa-toggle button.is-no{background:#141413;color:#fff;border-color:#141413}
.caa-field{display:grid;gap:6px;margin-top:16px;font-size:14px}
.caa-field span{color:#57534e}
.caa-field input,.caa-field select{font:inherit;border:1px solid #e5e0d6;background:#fff;color:#141413;padding:10px 12px;font-family:"JetBrains Mono",ui-monospace,monospace;font-variant-numeric:tabular-nums}
.caa-note{color:#57534e;font-size:13px;line-height:1.45;margin:8px 0 0}
.caa-verdict{position:sticky;top:12px}
.caa-stamp{display:inline-block;margin:8px 0 12px;border:2px solid currentColor;padding:8px 10px;font-weight:750;letter-spacing:.04em;text-transform:uppercase;font-size:14px;line-height:1.3;transform:rotate(-1.5deg)}
.caa-stamp.green{color:#15803d}
.caa-stamp.blue{color:#1d4ed8}
.caa-stamp.red{color:#b91c1c}
.caa-saved-label{margin:16px 0 0;color:#57534e;font-size:12px;letter-spacing:.12em;text-transform:uppercase}
.caa-saved{margin:4px 0;font-family:"JetBrains Mono",ui-monospace,monospace;font-variant-numeric:tabular-nums;font-size:36px;line-height:1;color:#141413}
.caa-ask{margin-top:16px;width:100%;display:inline-flex;gap:8px;align-items:center;justify-content:center;background:#1d4ed8;color:#fff;border:0;padding:12px 14px;font:inherit;font-weight:650;cursor:pointer;text-align:center}
.caa-ask:hover{background:#1e40af}
.caa-inputs{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-bottom:16px}
.caa-inputs .caa-note{grid-column:1/-1}
.caa-aid{display:grid;gap:12px}
.caa-aid-head{display:flex;justify-content:space-between;gap:12px;align-items:baseline}
.caa-aid-head h3,.caa-compare h3{margin:0 0 8px;font-family:Georgia,"Iowan Old Style",serif;font-size:22px}
.caa-dl{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px 12px;margin:12px 0}
.caa-dl div{border-top:1px solid #e5e0d6;padding-top:8px}
.caa-dl dt{color:#57534e;font-size:12px;letter-spacing:.04em;text-transform:uppercase}
.caa-dl dd{margin:4px 0 0;font-family:"JetBrains Mono",ui-monospace,monospace;font-variant-numeric:tabular-nums;font-size:15px}
.caa-compare{margin-top:16px;overflow-x:auto}
.caa-compare table{width:100%;border-collapse:collapse;font-size:14px}
.caa-compare th,.caa-compare td{text-align:left;vertical-align:top;border-bottom:1px solid #e5e0d6;padding:10px 8px}
.caa-compare th{color:#57534e;font-size:12px;letter-spacing:.04em;text-transform:uppercase;font-weight:600}
.caa-compare td:nth-child(2),.caa-dl dd,.caa-saved,.caa-field input{font-variant-numeric:tabular-nums}
.caa-compare td:nth-child(2){font-family:"JetBrains Mono",ui-monospace,monospace;white-space:nowrap}
@media (max-width:860px){
  .caa-split,.caa-inputs,.caa-dl{grid-template-columns:1fr}
  .caa-verdict{position:static}
}
`;
