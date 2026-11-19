"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import {
  ArrowUpRight,
  BadgeCheck,
  BookOpen,
  Camera,
  Check,
  ChevronDown,
  CircleAlert,
  ClipboardList,
  Clock,
  DollarSign,
  Film,
  Flag,
  GraduationCap,
  Layers,
  Lightbulb,
  ListChecks,
  MessageSquare,
  Printer,
  Search,
  ShieldAlert,
  Target,
  TriangleAlert,
  X,
} from "lucide-react";
import type {
  AthleteSop,
  DivisionRuleRow,
  GradeChecklist,
  SopStep,
} from "./sop-types";

/* ------------------------------------------------------------------ */
/* Palette: Commit Book editorial field manual                          */
/* ------------------------------------------------------------------ */
const PAPER = "#f7f5f0";
const CARD = "#ffffff";
const INK = "#141413";
const STONE = "#57534e";
const LINE = "#e5e0d6";
const BLUE = "#1d4ed8";
const CRIMSON = "#b91c1c";

const GRADE_FILTERS = ["All", "9th", "10th", "11th", "12th"] as const;
type GradeFilter = (typeof GRADE_FILTERS)[number];

const CATEGORY_FILTERS = [
  "All",
  "Academics",
  "Film",
  "Outreach",
  "Camps",
  "Paperwork",
] as const;
type CategoryFilter = (typeof CATEGORY_FILTERS)[number];

const VIEWS = [
  { id: "checklist", label: "Grade 9-12 Checklist", icon: ListChecks },
  { id: "division", label: "Division Rules & Caps", icon: Layers },
  { id: "film", label: "Highlight Film", icon: Film },
  { id: "camps", label: "Camps & Cost vs Waste", icon: DollarSign },
  { id: "mistakes", label: "10 Mistakes Families Make", icon: TriangleAlert },
] as const;
type ViewId = (typeof VIEWS)[number]["id"];

const STORAGE_KEY = "commitbook_sop_progress_v1";

/* ------------------------------------------------------------------ */
/* Resilient accessors: tolerate minor data shape variation            */
/* ------------------------------------------------------------------ */
function list<T>(value: T[] | null | undefined): T[] {
  return Array.isArray(value) ? value : [];
}

function text(value: string | null | undefined, fallback = ""): string {
  if (typeof value === "string") return value;
  if (value == null) return fallback;
  return String(value);
}

function gradeDigit(grade: string): string {
  const match = grade.match(/\d+/);
  return match ? match[0] : "";
}

function stepKey(sportSlug: string, grade: string, stepId: string): string {
  return `${sportSlug || "sop"}::${gradeDigit(grade) || grade}::${stepId}`;
}

function norm(value: string): string {
  return value.toLowerCase().trim();
}

function categoryMatches(stepCategory: string, filter: CategoryFilter): boolean {
  if (filter === "All") return true;
  return norm(stepCategory).includes(norm(filter));
}

function askGuide(prompt: string): void {
  if (typeof window === "undefined") return;
  window.dispatchEvent(new CustomEvent("commitbook:ask", { detail: { prompt } }));
}

/* ------------------------------------------------------------------ */
/* Small shared presentational pieces                                   */
/* ------------------------------------------------------------------ */
function SectionLead({
  icon: Icon,
  title,
  note,
}: {
  icon: typeof BookOpen;
  title: string;
  note?: string;
}) {
  return (
    <div className="soph-sec-lead">
      <span className="soph-sec-icon" aria-hidden="true">
        <Icon size={18} />
      </span>
      <div>
        <h3 className="soph-sec-title">{title}</h3>
        {note ? <p className="soph-sec-note">{note}</p> : null}
      </div>
    </div>
  );
}

function Bullets({ items, tone }: { items: string[]; tone: "good" | "bad" | "plain" }) {
  if (items.length === 0) {
    return <p className="soph-quiet">No entries recorded in this playbook yet.</p>;
  }
  return (
    <ul className={`soph-bullets is-${tone}`}>
      {items.map((item, i) => (
        <li key={`${tone}-${i}`}>
          <span className="soph-bullet-mark" aria-hidden="true">
            {tone === "good" ? <Check size={13} /> : tone === "bad" ? <X size={13} /> : <ChevronDown size={13} />}
          </span>
          <span>{item}</span>
        </li>
      ))}
    </ul>
  );
}

/* ------------------------------------------------------------------ */
/* Panel 1: Grade 9-12 checklist                                        */
/* ------------------------------------------------------------------ */
function ChecklistPanel({
  sop,
  done,
  onToggle,
}: {
  sop: AthleteSop;
  done: Record<string, boolean>;
  onToggle: (key: string) => void;
}) {
  const [grade, setGrade] = useState<GradeFilter>("All");
  const [category, setCategory] = useState<CategoryFilter>("All");

  const grades = list<GradeChecklist>(sop.gradeChecklists);

  const totals = useMemo(() => {
    let total = 0;
    let complete = 0;
    for (const g of grades) {
      for (const step of list(g.steps)) {
        total += 1;
        if (done[stepKey(sop.sportSlug, g.grade, step.id)]) complete += 1;
      }
    }
    return { total, complete };
  }, [grades, done, sop.sportSlug]);

  const visibleGrades = useMemo(
    () => grades.filter((g) => (grade === "All" ? true : gradeDigit(g.grade) === gradeDigit(grade))),
    [grades, grade],
  );

  function toggle(g: GradeChecklist, step: SopStep) {
    onToggle(stepKey(sop.sportSlug, g.grade, step.id));
  }

  return (
    <div className="soph-panel">
      <SectionLead
        icon={ListChecks}
        title="Grade 9-12 SOP checklist"
        note="Work the steps in order. Check them off as you finish. Progress saves to this browser."
      />

      <div className="soph-check-toolbar">
        <div className="soph-progress">
          <div className="soph-progress-bar" aria-hidden="true">
            <span
              className="soph-progress-fill"
              style={{ width: totals.total ? `${Math.round((totals.complete / totals.total) * 100)}%` : "0%" }}
            />
          </div>
          <p className="soph-progress-text">
            <span className="soph-num">{totals.complete}</span> of{" "}
            <span className="soph-num">{totals.total}</span> steps complete
          </p>
        </div>
        <button
          type="button"
          className="soph-print"
          onClick={() => {
            if (typeof window !== "undefined") window.print();
          }}
        >
          <Printer size={15} aria-hidden="true" />
          Print / Save Progress
        </button>
      </div>

      <div className="soph-filters">
        <div className="soph-filter-row" role="tablist" aria-label="Filter by grade">
          <span className="soph-filter-label">Grade</span>
          {GRADE_FILTERS.map((g) => (
            <button
              key={g}
              type="button"
              role="tab"
              aria-selected={grade === g}
              className={grade === g ? "soph-chip is-on" : "soph-chip"}
              onClick={() => setGrade(g)}
            >
              {g}
            </button>
          ))}
        </div>
        <div className="soph-filter-row" role="tablist" aria-label="Filter by category">
          <span className="soph-filter-label">Category</span>
          {CATEGORY_FILTERS.map((c) => (
            <button
              key={c}
              type="button"
              role="tab"
              aria-selected={category === c}
              className={category === c ? "soph-chip is-on" : "soph-chip"}
              onClick={() => setCategory(c)}
            >
              {c}
            </button>
          ))}
        </div>
      </div>

      {visibleGrades.length === 0 ? (
        <p className="soph-quiet">No checklist data is attached to this playbook for the selected grade.</p>
      ) : (
        visibleGrades.map((g) => {
          const steps = list(g.steps).filter((s) => categoryMatches(text(s.category), category));
          return (
            <section key={`${g.grade}-${g.windowLabel}`} className="soph-grade">
              <header className="soph-grade-head">
                <div>
                  <p className="soph-grade-label">
                    <GraduationCap size={16} aria-hidden="true" />
                    {text(g.grade)}
                    {text(g.windowLabel) ? <span className="soph-grade-window">{text(g.windowLabel)}</span> : null}
                  </p>
                  {text(g.goal) ? <p className="soph-grade-goal">{text(g.goal)}</p> : null}
                </div>
              </header>
              {steps.length === 0 ? (
                <p className="soph-quiet">No steps in this category for {text(g.grade)}.</p>
              ) : (
                <ul className="soph-steps">
                  {steps.map((step) => {
                    const key = stepKey(sop.sportSlug, g.grade, step.id);
                    const checked = Boolean(done[key]);
                    return (
                      <li key={key} className={checked ? "soph-step is-done" : "soph-step"}>
                        <button
                          type="button"
                          role="checkbox"
                          aria-checked={checked}
                          className="soph-checkbox"
                          onClick={() => toggle(g, step)}
                        >
                          <span className="soph-box" aria-hidden="true">
                            {checked ? <Check size={14} /> : null}
                          </span>
                        </button>
                        <div className="soph-step-body">
                          <p className="soph-step-title">{text(step.title)}</p>
                          {text(step.detail) ? <p className="soph-step-detail">{text(step.detail)}</p> : null}
                          <div className="soph-step-meta">
                            {text(step.timing) ? (
                              <span className="soph-timing">
                                <Clock size={12} aria-hidden="true" />
                                {text(step.timing)}
                              </span>
                            ) : null}
                            {text(step.category) ? <span className="soph-cat">{text(step.category)}</span> : null}
                          </div>
                        </div>
                        <button
                          type="button"
                          className="soph-ask"
                          onClick={() =>
                            askGuide(
                              `Walk me through this recruiting step for my athlete: "${text(
                                step.title,
                              )}". Timing: ${text(step.timing, "not set")}. What exactly should we do, and what does "done" look like?`,
                            )
                          }
                        >
                          <MessageSquare size={14} aria-hidden="true" />
                          Ask Scout
                        </button>
                      </li>
                    );
                  })}
                </ul>
              )}
            </section>
          );
        })
      )}

      <PaperworkTable sop={sop} />
    </div>
  );
}

function PaperworkTable({ sop }: { sop: AthleteSop }) {
  const rows = list(sop.paperworkAndDeadlines);
  return (
    <section className="soph-sub">
      <SectionLead
        icon={ClipboardList}
        title="Paperwork, registrations and deadlines"
        note="Dates and rules move. Confirm every deadline against the current rulebook before you act."
      />
      {rows.length === 0 ? (
        <p className="soph-quiet">No paperwork milestones recorded for this playbook.</p>
      ) : (
        <div className="soph-table-wrap">
          <table className="soph-table">
            <thead>
              <tr>
                <th scope="col">Milestone</th>
                <th scope="col">When</th>
                <th scope="col">Cost</th>
                <th scope="col">Rule</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((row, i) => (
                <tr key={`paper-${i}`}>
                  <th scope="row">{text(row.milestone)}</th>
                  <td className="soph-num">{text(row.when)}</td>
                  <td className="soph-num">{text(row.cost)}</td>
                  <td>{text(row.rule)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

/* ------------------------------------------------------------------ */
/* Panel 2: Division rules and roster caps                              */
/* ------------------------------------------------------------------ */
function DivisionPanel({ sop }: { sop: AthleteSop }) {
  const rows = list<DivisionRuleRow>(sop.divisionMatrix);
  return (
    <div className="soph-panel">
      <SectionLead
        icon={Layers}
        title="Division rules and roster caps"
        note="One honest comparison across NCAA D1, D2, D3, NAIA and NJCAA. Read the reality note before you set expectations."
      />
      {rows.length === 0 ? (
        <p className="soph-quiet">No division matrix is attached to this playbook yet.</p>
      ) : (
        <div className="soph-table-wrap">
          <table className="soph-table soph-table-wide">
            <thead>
              <tr>
                <th scope="col">Level</th>
                <th scope="col">Roster cap / limit</th>
                <th scope="col">Aid model</th>
                <th scope="col">First direct contact</th>
                <th scope="col">Official visits start</th>
                <th scope="col">Reality note</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((row, i) => (
                <tr key={`div-${i}`}>
                  <th scope="row" className="soph-level">
                    {text(row.level)}
                  </th>
                  <td className="soph-num">{text(row.rosterCapOrLimit)}</td>
                  <td>{text(row.aidModel)}</td>
                  <td className="soph-num">{text(row.firstDirectContact)}</td>
                  <td className="soph-num">{text(row.officialVisitsStart)}</td>
                  <td className="soph-reality">{text(row.realityNote)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

/* ------------------------------------------------------------------ */
/* Panel 3: Highlight film standard                                     */
/* ------------------------------------------------------------------ */
function FilmPanel({ sop }: { sop: AthleteSop }) {
  const video = sop.videoStandard;
  const first30 = list(video?.mustShowFirst30Sec);
  const camera = list(video?.cameraAndFormatRules);
  const cuts = list(video?.cutImmediately);
  return (
    <div className="soph-panel">
      <SectionLead
        icon={Film}
        title="Highlight film standard"
        note="A coach decides in seconds. Build the tape to that standard, not to what looks impressive to family."
      />
      <div className="soph-film-length">
        <Target size={18} aria-hidden="true" />
        <div>
          <p className="soph-film-length-label">Ideal length</p>
          <p className="soph-film-length-value">{text(video?.idealLength, "Set the target length in this playbook.")}</p>
        </div>
      </div>
      <div className="soph-film-grid">
        <section className="soph-film-col">
          <h4 className="soph-film-h">
            <Camera size={15} aria-hidden="true" />
            First 30 seconds must show
          </h4>
          <Bullets items={first30} tone="good" />
        </section>
        <section className="soph-film-col">
          <h4 className="soph-film-h">
            <Film size={15} aria-hidden="true" />
            Camera and format rules
          </h4>
          <Bullets items={camera} tone="plain" />
        </section>
        <section className="soph-film-col is-alert">
          <h4 className="soph-film-h">
            <CircleAlert size={15} aria-hidden="true" />
            Cut immediately
          </h4>
          <Bullets items={cuts} tone="bad" />
        </section>
      </div>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/* Panel 4: Camps, clubs and cost vs waste                              */
/* ------------------------------------------------------------------ */
function CampsPanel({ sop }: { sop: AthleteSop }) {
  const filter = sop.campAndCircuitFilter;
  const worth = list(filter?.worthPayingFor);
  const skip = list(filter?.skipOrTrap);
  const redFlags = list(filter?.redFlagTest);
  const costs = list(sop.costVsWaste);

  const groups = useMemo(() => {
    const essential: typeof costs = [];
    const selective: typeof costs = [];
    const skipG: typeof costs = [];
    for (const row of costs) {
      const verdict = norm(text(row.verdict));
      if (verdict.includes("essential") || verdict.includes("must")) essential.push(row);
      else if (verdict.includes("skip") || verdict.includes("trap") || verdict.includes("waste")) skipG.push(row);
      else selective.push(row);
    }
    return { essential, selective, skip: skipG };
  }, [costs]);

  return (
    <div className="soph-panel">
      <SectionLead
        icon={DollarSign}
        title="Camps, clubs and cost vs waste"
        note="Where the money actually helps, where it is optional, and where families burn it. Then the red-flag test before you pay."
      />

      <div className="soph-cost-split">
        <section>
          <h4 className="soph-film-h">
            <BadgeCheck size={15} aria-hidden="true" />
            Worth paying for
          </h4>
          <Bullets items={worth} tone="good" />
        </section>
        <section>
          <h4 className="soph-film-h">
            <ShieldAlert size={15} aria-hidden="true" />
            Skip or trap
          </h4>
          <Bullets items={skip} tone="bad" />
        </section>
      </div>

      <div className="soph-sub">
        <h4 className="soph-film-h">
          <DollarSign size={15} aria-hidden="true" />
          Essential vs selective vs skip spend
        </h4>
        {costs.length === 0 ? (
          <p className="soph-quiet">No spend breakdown is recorded for this playbook.</p>
        ) : (
          <div className="soph-table-wrap">
            <table className="soph-table">
              <thead>
                <tr>
                  <th scope="col">Item</th>
                  <th scope="col">Typical spend</th>
                  <th scope="col">Verdict</th>
                  <th scope="col">Why</th>
                </tr>
              </thead>
              <tbody>
                {[
                  { label: "Essential", rows: groups.essential, cls: "is-essential" },
                  { label: "Selective", rows: groups.selective, cls: "is-selective" },
                  { label: "Skip", rows: groups.skip, cls: "is-skip" },
                ].map((group) =>
                  group.rows.length === 0 ? null : (
                    <FragmentRows key={group.label} label={group.label} cls={group.cls} rows={group.rows} />
                  ),
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <div className="soph-redflag">
        <h4 className="soph-film-h">
          <Flag size={15} aria-hidden="true" />
          Camp red-flag test: five questions before you pay
        </h4>
        {redFlags.length === 0 ? (
          <p className="soph-quiet">No red-flag test recorded for this playbook.</p>
        ) : (
          <ol className="soph-redflag-list">
            {redFlags.map((q, i) => (
              <li key={`rf-${i}`}>
                <span className="soph-num soph-rf-num">{i + 1}</span>
                <span>{q}</span>
              </li>
            ))}
          </ol>
        )}
      </div>
    </div>
  );
}

function FragmentRows({
  label,
  cls,
  rows,
}: {
  label: string;
  cls: string;
  rows: { item: string; typicalSpend: string; verdict: string; why: string }[];
}) {
  return (
    <>
      <tr className={`soph-group-row ${cls}`}>
        <th scope="rowgroup" colSpan={4}>
          {label}
        </th>
      </tr>
      {rows.map((row, i) => (
        <tr key={`${label}-${i}`}>
          <th scope="row">{text(row.item)}</th>
          <td className="soph-num">{text(row.typicalSpend)}</td>
          <td>
            <span className={`soph-verdict ${cls}`}>{text(row.verdict)}</span>
          </td>
          <td>{text(row.why)}</td>
        </tr>
      ))}
    </>
  );
}

/* ------------------------------------------------------------------ */
/* Panel 5: 10 mistakes families make                                   */
/* ------------------------------------------------------------------ */
function MistakesPanel({ sop }: { sop: AthleteSop }) {
  const [query, setQuery] = useState("");
  const [open, setOpen] = useState<number | null>(null);
  const mistakes = list(sop.tenMistakes);

  const filtered = useMemo(() => {
    const q = norm(query);
    if (!q) return mistakes;
    return mistakes.filter(
      (m) => norm(text(m.mistake)).includes(q) || norm(text(m.fix)).includes(q),
    );
  }, [mistakes, query]);

  return (
    <div className="soph-panel">
      <SectionLead
        icon={TriangleAlert}
        title="10 mistakes families make"
        note="The costly errors, and the exact fix for each. Search by the problem you are worried about."
      />

      <label className="soph-search">
        <Search size={16} aria-hidden="true" />
        <span className="soph-sr">Search mistakes and fixes</span>
        <input
          type="search"
          value={query}
          placeholder="Search a mistake or a fix"
          onChange={(event) => setQuery(event.target.value)}
        />
        {query ? (
          <button type="button" className="soph-clear" onClick={() => setQuery("")} aria-label="Clear search">
            <X size={15} aria-hidden="true" />
          </button>
        ) : null}
      </label>

      {filtered.length === 0 ? (
        <p className="soph-quiet">No mistakes match that search. Clear the search to see all ten.</p>
      ) : (
        <ul className="soph-mistakes">
          {filtered.map((m, i) => {
            const id = typeof m.number === "number" ? m.number : i + 1;
            const isOpen = open === id;
            return (
              <li key={`mistake-${id}`} className={isOpen ? "soph-mistake is-open" : "soph-mistake"}>
                <button
                  type="button"
                  className="soph-mistake-head"
                  aria-expanded={isOpen}
                  onClick={() => setOpen(isOpen ? null : id)}
                >
                  <span className="soph-mistake-num soph-num">{String(id).padStart(2, "0")}</span>
                  <span className="soph-mistake-title">{text(m.mistake)}</span>
                  <ChevronDown size={18} aria-hidden="true" className={isOpen ? "is-open" : ""} />
                </button>
                {isOpen ? (
                  <div className="soph-mistake-body">
                    <p className="soph-mistake-fix-label">
                      <Lightbulb size={15} aria-hidden="true" />
                      The fix
                    </p>
                    <p className="soph-mistake-fix">{text(m.fix)}</p>
                    <button
                      type="button"
                      className="soph-ask"
                      onClick={() =>
                        askGuide(
                          `My family may be making this recruiting mistake: "${text(
                            m.mistake,
                          )}". The suggested fix is: ${text(m.fix)} Give me a concrete plan to correct it this month.`,
                        )
                      }
                    >
                      <MessageSquare size={14} aria-hidden="true" />
                      Ask Scout
                    </button>
                  </div>
                ) : null}
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}

/* ------------------------------------------------------------------ */
/* Preview summary (previewMode = true)                                */
/* ------------------------------------------------------------------ */
function PreviewSummary({ sop }: { sop: AthleteSop }) {
  const grades = list<GradeChecklist>(sop.gradeChecklists);
  return (
    <div className="soph-panel soph-preview">
      <SectionLead
        icon={BookOpen}
        title="Grade 9-12 at a glance"
        note="A short summary of the four-year path. Open the full workstation for filters, checkboxes, rules and the film standard."
      />
      <div className="soph-preview-grades">
        {grades.length === 0 ? (
          <p className="soph-quiet">No grade summary is attached to this playbook yet.</p>
        ) : (
          grades.map((g) => (
            <article key={`pv-${g.grade}`} className="soph-preview-card">
              <p className="soph-preview-grade soph-num">{text(g.grade)}</p>
              {text(g.windowLabel) ? <p className="soph-preview-window">{text(g.windowLabel)}</p> : null}
              <p className="soph-preview-goal">{text(g.goal)}</p>
              <p className="soph-preview-count">
                <span className="soph-num">{list(g.steps).length}</span> steps
              </p>
            </article>
          ))
        )}
      </div>
      <a className="soph-full-link" href="/sops">
        Open the full SOP workstation
        <ArrowUpRight size={16} aria-hidden="true" />
      </a>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/* Main hub                                                             */
/* ------------------------------------------------------------------ */
export default function AthleteSopHub({
  sops,
  initialSport,
  previewMode = false,
}: {
  sops: AthleteSop[];
  initialSport?: string;
  previewMode?: boolean;
}) {
  const catalog = useMemo(() => list<AthleteSop>(sops), [sops]);

  const resolveSlug = useCallback(
    (value: string | undefined): string => {
      if (!value) return catalog[0]?.sportSlug ?? "";
      const needle = norm(value);
      const match =
        catalog.find((s) => norm(s.sportSlug) === needle) ??
        catalog.find((s) => norm(s.sportLabel) === needle) ??
        catalog.find((s) => norm(s.athleteName) === needle);
      return match?.sportSlug ?? catalog[0]?.sportSlug ?? "";
    },
    [catalog],
  );

  const [activeSlug, setActiveSlug] = useState<string>("");
  const [view, setView] = useState<ViewId>("checklist");
  const [done, setDone] = useState<Record<string, boolean>>({});
  const [loaded, setLoaded] = useState(false);

  // Resolve the active sport after mount so initialSport can match label or slug.
  useEffect(() => {
    setActiveSlug(resolveSlug(initialSport));
  }, [initialSport, resolveSlug]);

  // Load saved progress once.
  useEffect(() => {
    try {
      const raw = typeof window !== "undefined" ? window.localStorage.getItem(STORAGE_KEY) : null;
      if (raw) {
        const parsed: unknown = JSON.parse(raw);
        if (parsed && typeof parsed === "object" && !Array.isArray(parsed)) {
          setDone(parsed as Record<string, boolean>);
        }
      }
    } catch {
      // Ignore malformed saved progress and start clean.
    }
    setLoaded(true);
  }, []);

  // Persist progress after load.
  useEffect(() => {
    if (!loaded) return;
    try {
      if (typeof window !== "undefined") {
        window.localStorage.setItem(STORAGE_KEY, JSON.stringify(done));
      }
    } catch {
      // Storage may be unavailable; progress stays in memory for this session.
    }
  }, [done, loaded]);

  const active = useMemo(() => {
    if (catalog.length === 0) return undefined;
    return catalog.find((s) => s.sportSlug === activeSlug) ?? catalog[0];
  }, [catalog, activeSlug]);

  const toggleStep = useCallback((key: string) => {
    setDone((current) => {
      const next = { ...current };
      if (next[key]) delete next[key];
      else next[key] = true;
      return next;
    });
  }, []);

  if (catalog.length === 0 || !active) {
    return (
      <section className="soph" aria-label="Athlete SOP playbook hub">
        <style>{css}</style>
        <div className="soph-empty-state">
          <BookOpen size={22} aria-hidden="true" />
          <p>No athlete playbooks are loaded yet. Add a playbook to begin.</p>
        </div>
      </section>
    );
  }

  const bodies = list(active.governingBodies);

  return (
    <section className="soph" aria-label={`${active.sportLabel} athlete SOP playbook hub`}>
      <style>{css}</style>

      <header className="soph-mast">
        <div className="soph-mast-top">
          <p className="soph-kicker">Commit Book · Athlete SOP field manual</p>
          <div className="soph-stamps">
            <span className="soph-persona">
              <GraduationCap size={14} aria-hidden="true" />
              Athlete: {text(active.athleteName, "Unnamed athlete")}
            </span>
            <span className="soph-verified">
              <BadgeCheck size={14} aria-hidden="true" />
              Verified rulebook {text(active.verifiedDate)}
            </span>
          </div>
        </div>

        <div className="soph-pills" role="tablist" aria-label="Choose a sport playbook">
          {catalog.map((s) => (
            <button
              key={s.sportSlug}
              type="button"
              role="tab"
              aria-selected={s.sportSlug === active.sportSlug}
              className={s.sportSlug === active.sportSlug ? "soph-pill is-on" : "soph-pill"}
              onClick={() => setActiveSlug(s.sportSlug)}
            >
              {text(s.sportLabel, s.sportSlug)}
            </button>
          ))}
        </div>

        <h2 className="soph-title">{text(active.sportLabel)} recruiting playbook</h2>
        {text(active.subtitle) ? <p className="soph-sub-title">{text(active.subtitle)}</p> : null}

        {text(active.headlineReality) ? (
          <p className="soph-headline">
            <TriangleAlert size={16} aria-hidden="true" />
            <span>{text(active.headlineReality)}</span>
          </p>
        ) : null}

        {bodies.length > 0 ? (
          <ul className="soph-bodies">
            {bodies.map((b, i) => (
              <li key={`body-${i}`}>
                <BookOpen size={12} aria-hidden="true" />
                {b}
              </li>
            ))}
          </ul>
        ) : null}
      </header>

      {previewMode ? (
        <PreviewSummary sop={active} />
      ) : (
        <>
          <nav className="soph-views" role="tablist" aria-label="Playbook sections">
            {VIEWS.map((v) => {
              const Icon = v.icon;
              return (
                <button
                  key={v.id}
                  type="button"
                  role="tab"
                  aria-selected={view === v.id}
                  className={view === v.id ? "soph-view is-on" : "soph-view"}
                  onClick={() => setView(v.id)}
                >
                  <Icon size={16} aria-hidden="true" />
                  {v.label}
                </button>
              );
            })}
          </nav>

          {view === "checklist" ? <ChecklistPanel sop={active} done={done} onToggle={toggleStep} /> : null}
          {view === "division" ? <DivisionPanel sop={active} /> : null}
          {view === "film" ? <FilmPanel sop={active} /> : null}
          {view === "camps" ? <CampsPanel sop={active} /> : null}
          {view === "mistakes" ? <MistakesPanel sop={active} /> : null}
        </>
      )}
    </section>
  );
}

/* ------------------------------------------------------------------ */
/* Styles: Commit Book editorial field manual                           */
/* ------------------------------------------------------------------ */
const css = `


.soph{
  ${"" /* Commit Book editorial field manual palette */}
  --soph-paper:${PAPER};
  --soph-card:${CARD};
  --soph-ink:${INK};
  --soph-stone:${STONE};
  --soph-line:${LINE};
  --soph-blue:${BLUE};
  --soph-crimson:${CRIMSON};
  box-sizing:border-box;
  margin:0;
  width:100%;
  background:var(--soph-paper);
  color:var(--soph-ink);
  font-family:'Inter Tight',system-ui,-apple-system,'Segoe UI',sans-serif;
  font-size:16px;
  line-height:1.55;
  padding:28px clamp(16px,3vw,40px) 40px;
  border:1px solid var(--soph-line);
}
.soph *,.soph *::before,.soph *::after{box-sizing:border-box}
.soph h2,.soph h3,.soph h4{font-family:'Newsreader',Georgia,'Times New Roman',serif;font-weight:600;letter-spacing:-.01em;margin:0}
.soph p{margin:0}
.soph button{font-family:inherit;cursor:pointer}
.soph-num{font-family:'JetBrains Mono',ui-monospace,monospace;font-variant-numeric:tabular-nums;letter-spacing:-.01em}
.soph-sr{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}

/* mast */
.soph-mast{border-bottom:1px solid var(--soph-line);padding-bottom:22px;margin-bottom:22px}
.soph-mast-top{display:flex;flex-wrap:wrap;gap:12px;align-items:center;justify-content:space-between}
.soph-kicker{font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--soph-stone);font-weight:600}
.soph-stamps{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.soph-persona,.soph-verified{display:inline-flex;align-items:center;gap:6px;font-size:11px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;padding:5px 11px;border-radius:999px}
.soph-persona{background:var(--soph-ink);color:var(--soph-paper)}
.soph-verified{background:rgba(29,78,216,.1);color:var(--soph-blue);border:1px solid rgba(29,78,216,.35)}

.soph-pills{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0 20px}
.soph-pill{border:1px solid var(--soph-line);background:var(--soph-card);color:var(--soph-stone);padding:8px 16px;border-radius:999px;font-size:13px;font-weight:600;letter-spacing:.01em;transition:background .15s,color .15s,border-color .15s}
.soph-pill:hover{border-color:var(--soph-ink);color:var(--soph-ink)}
.soph-pill.is-on{background:var(--soph-blue);border-color:var(--soph-blue);color:#fff}

.soph-title{font-size:clamp(28px,4vw,42px);line-height:1.02}
.soph-sub-title{margin-top:8px;font-size:16px;color:var(--soph-stone);max-width:70ch}
.soph-headline{display:flex;gap:10px;align-items:flex-start;margin-top:16px;padding:12px 15px;background:rgba(185,28,28,.07);border-left:3px solid var(--soph-crimson);color:var(--soph-ink);font-size:14.5px}
.soph-headline svg{color:var(--soph-crimson);flex:none;margin-top:2px}
.soph-bodies{list-style:none;display:flex;flex-wrap:wrap;gap:8px;padding:0;margin:16px 0 0}
.soph-bodies li{display:inline-flex;align-items:center;gap:6px;font-size:11px;font-weight:600;letter-spacing:.05em;text-transform:uppercase;color:var(--soph-stone);border:1px solid var(--soph-line);padding:4px 10px;border-radius:999px}

/* view tabs */
.soph-views{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 22px;border-bottom:1px solid var(--soph-line);padding-bottom:18px}
.soph-view{display:inline-flex;align-items:center;gap:8px;border:1px solid transparent;background:transparent;color:var(--soph-stone);padding:9px 15px;border-radius:8px;font-size:13.5px;font-weight:600;transition:background .15s,color .15s}
.soph-view:hover{background:var(--soph-card);color:var(--soph-ink)}
.soph-view.is-on{background:var(--soph-ink);color:var(--soph-paper)}

/* panel + section lead */
.soph-panel{background:var(--soph-card);border:1px solid var(--soph-line);border-radius:4px;padding:22px}
.soph-preview{background:var(--soph-card)}
.soph-sec-lead{display:flex;gap:12px;align-items:flex-start;margin-bottom:16px}
.soph-sec-icon{display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;border-radius:8px;background:rgba(29,78,216,.1);color:var(--soph-blue);flex:none}
.soph-sec-title{font-size:20px;line-height:1.2}
.soph-sec-note{margin-top:3px;font-size:13.5px;color:var(--soph-stone);max-width:72ch}
.soph-sub{margin-top:26px;padding-top:22px;border-top:1px solid var(--soph-line)}
.soph-quiet{font-size:13.5px;color:var(--soph-stone);font-style:italic}

/* checklist toolbar */
.soph-check-toolbar{display:flex;flex-wrap:wrap;gap:16px;align-items:center;justify-content:space-between;margin-bottom:16px}
.soph-progress{flex:1 1 240px;min-width:220px}
.soph-progress-bar{height:8px;border-radius:999px;background:var(--soph-paper);border:1px solid var(--soph-line);overflow:hidden}
.soph-progress-fill{display:block;height:100%;background:var(--soph-blue);border-radius:999px;transition:width .3s var(--soph-ease,cubic-bezier(.16,1,.3,1))}
.soph-progress-text{margin-top:8px;font-size:13px;color:var(--soph-stone);font-weight:500}
.soph-print{display:inline-flex;align-items:center;gap:8px;background:var(--soph-ink);color:var(--soph-paper);border:1px solid var(--soph-ink);padding:9px 15px;border-radius:8px;font-size:13px;font-weight:600}
.soph-print:hover{background:#2c2a27}

/* filters */
.soph-filters{display:flex;flex-direction:column;gap:12px;margin-bottom:20px}
.soph-filter-row{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.soph-filter-label{font-size:11px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--soph-stone);margin-right:4px}
.soph-chip{border:1px solid var(--soph-line);background:var(--soph-paper);color:var(--soph-stone);padding:6px 13px;border-radius:999px;font-size:12.5px;font-weight:600;transition:background .15s,color .15s,border-color .15s}
.soph-chip:hover{border-color:var(--soph-ink);color:var(--soph-ink)}
.soph-chip.is-on{background:var(--soph-ink);border-color:var(--soph-ink);color:var(--soph-paper)}

/* grade block + steps */
.soph-grade{margin-bottom:8px}
.soph-grade-head{margin:18px 0 10px}
.soph-grade-label{display:flex;align-items:center;gap:8px;font-family:'Newsreader',Georgia,serif;font-size:17px;font-weight:600}
.soph-grade-window{margin-left:6px;font-family:'Inter Tight',sans-serif;font-size:11px;font-weight:600;letter-spacing:.05em;text-transform:uppercase;color:var(--soph-blue);background:rgba(29,78,216,.1);padding:3px 9px;border-radius:999px}
.soph-grade-goal{margin-top:5px;font-size:13.5px;color:var(--soph-stone);max-width:80ch}
.soph-steps{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:10px}
.soph-step{display:flex;gap:12px;align-items:flex-start;background:var(--soph-paper);border:1px solid var(--soph-line);border-radius:6px;padding:14px 15px}
.soph-step.is-done{background:rgba(29,78,216,.05);border-color:rgba(29,78,216,.28)}
.soph-checkbox{flex:none;background:none;border:0;padding:0;margin-top:1px}
.soph-box{display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;border:1.5px solid var(--soph-stone);border-radius:5px;background:var(--soph-card);color:transparent;transition:background .15s,border-color .15s,color .15s}
.soph-step.is-done .soph-box{background:var(--soph-blue);border-color:var(--soph-blue);color:#fff}
.soph-step-body{flex:1 1 auto;min-width:0}
.soph-step-title{font-size:15px;font-weight:600;line-height:1.35}
.soph-step.is-done .soph-step-title{color:var(--soph-stone);text-decoration:line-through}
.soph-step-detail{margin-top:4px;font-size:13.5px;color:var(--soph-stone);line-height:1.5}
.soph-step-meta{display:flex;flex-wrap:wrap;gap:8px;margin-top:9px;align-items:center}
.soph-timing{display:inline-flex;align-items:center;gap:5px;font-family:'JetBrains Mono',monospace;font-variant-numeric:tabular-nums;font-size:11px;color:var(--soph-stone)}
.soph-cat{font-size:10.5px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--soph-stone);border:1px solid var(--soph-line);padding:2px 9px;border-radius:999px}
.soph-ask{flex:none;display:inline-flex;align-items:center;gap:6px;background:transparent;color:var(--soph-blue);border:1px solid rgba(29,78,216,.4);padding:7px 12px;border-radius:8px;font-size:12px;font-weight:600;white-space:nowrap}
.soph-ask:hover{background:rgba(29,78,216,.08);border-color:var(--soph-blue)}

/* tables */
.soph-table-wrap{overflow-x:auto;border:1px solid var(--soph-line);border-radius:6px}
.soph-table{width:100%;border-collapse:collapse;font-size:13.5px;min-width:560px}
.soph-table-wide{min-width:860px}
.soph-table thead th{background:var(--soph-ink);color:var(--soph-paper);text-align:left;font-size:11px;font-weight:600;letter-spacing:.07em;text-transform:uppercase;padding:11px 13px;white-space:nowrap}
.soph-table tbody th,.soph-table tbody td{padding:11px 13px;border-top:1px solid var(--soph-line);vertical-align:top;text-align:left}
.soph-table tbody th{font-weight:600;color:var(--soph-ink);background:var(--soph-paper)}
.soph-table tbody tr:hover td,.soph-table tbody tr:hover th{background:rgba(29,78,216,.035)}
.soph-level{font-family:'Newsreader',Georgia,serif;font-size:15px}
.soph-reality{color:var(--soph-stone)}
.soph-group-row th{background:var(--soph-paper);font-family:'Inter Tight',sans-serif;font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase}
.soph-group-row.is-essential th{color:var(--soph-blue)}
.soph-group-row.is-skip th{color:var(--soph-crimson)}
.soph-verdict{display:inline-flex;align-items:center;font-size:11px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;padding:3px 10px;border-radius:999px;white-space:nowrap}
.soph-verdict.is-essential{background:rgba(29,78,216,.12);color:var(--soph-blue)}
.soph-verdict.is-selective{background:rgba(87,83,78,.12);color:var(--soph-stone)}
.soph-verdict.is-skip{background:rgba(185,28,28,.1);color:var(--soph-crimson)}

/* film */
.soph-film-length{display:flex;gap:12px;align-items:center;background:var(--soph-paper);border:1px solid var(--soph-line);border-radius:6px;padding:14px 16px;margin-bottom:18px}
.soph-film-length svg{color:var(--soph-blue);flex:none}
.soph-film-length-label{font-size:11px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--soph-stone)}
.soph-film-length-value{font-family:'Newsreader',Georgia,serif;font-size:19px;font-weight:600}
.soph-film-grid{display:grid;grid-template-columns:1fr;gap:16px}
@media(min-width:820px){.soph-film-grid{grid-template-columns:1fr 1fr 1fr}}
.soph-film-col{background:var(--soph-paper);border:1px solid var(--soph-line);border-radius:6px;padding:16px}
.soph-film-col.is-alert{border-color:rgba(185,28,28,.35);background:rgba(185,28,28,.05)}
.soph-film-h{display:flex;align-items:center;gap:8px;font-family:'Inter Tight',sans-serif;font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--soph-ink);margin-bottom:11px}
.soph-film-h svg{color:var(--soph-blue);flex:none}
.soph-film-col.is-alert .soph-film-h svg{color:var(--soph-crimson)}

/* bullets */
.soph-bullets{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:9px}
.soph-bullets li{display:flex;gap:9px;align-items:flex-start;font-size:13.5px;line-height:1.5}
.soph-bullet-mark{flex:none;display:inline-flex;align-items:center;justify-content:center;width:19px;height:19px;border-radius:5px;margin-top:1px}
.soph-bullets.is-good .soph-bullet-mark{background:rgba(29,78,216,.12);color:var(--soph-blue)}
.soph-bullets.is-bad .soph-bullet-mark{background:rgba(185,28,28,.12);color:var(--soph-crimson)}
.soph-bullets.is-plain .soph-bullet-mark{background:rgba(87,83,78,.1);color:var(--soph-stone)}

/* camps */
.soph-cost-split{display:grid;grid-template-columns:1fr;gap:18px;margin-bottom:6px}
@media(min-width:760px){.soph-cost-split{grid-template-columns:1fr 1fr}}
.soph-redflag{margin-top:26px;padding-top:22px;border-top:1px solid var(--soph-line)}
.soph-redflag-list{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:11px;counter-reset:rf}
.soph-redflag-list li{display:flex;gap:12px;align-items:flex-start;background:var(--soph-paper);border:1px solid var(--soph-line);border-left:3px solid var(--soph-crimson);border-radius:6px;padding:12px 15px;font-size:14px;line-height:1.5}
.soph-rf-num{flex:none;display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;border-radius:999px;background:var(--soph-crimson);color:#fff;font-size:12px;font-weight:700}

/* mistakes */
.soph-search{display:flex;align-items:center;gap:9px;background:var(--soph-paper);border:1px solid var(--soph-line);border-radius:8px;padding:10px 13px;margin-bottom:16px}
.soph-search svg{color:var(--soph-stone);flex:none}
.soph-search input{flex:1 1 auto;border:0;background:transparent;font-family:inherit;font-size:14px;color:var(--soph-ink);outline:none;min-width:0}
.soph-clear{flex:none;background:none;border:0;color:var(--soph-stone);display:inline-flex;padding:2px}
.soph-clear:hover{color:var(--soph-crimson)}
.soph-mistakes{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:9px}
.soph-mistake{border:1px solid var(--soph-line);border-radius:6px;overflow:hidden;background:var(--soph-paper)}
.soph-mistake.is-open{border-color:var(--soph-ink)}
.soph-mistake-head{width:100%;display:flex;align-items:center;gap:13px;background:none;border:0;padding:15px 16px;text-align:left}
.soph-mistake-num{flex:none;display:inline-flex;align-items:center;justify-content:center;width:30px;height:30px;border-radius:7px;background:var(--soph-ink);color:var(--soph-paper);font-size:12px;font-weight:700}
.soph-mistake-title{flex:1 1 auto;font-family:'Newsreader',Georgia,serif;font-size:16px;font-weight:600;line-height:1.3}
.soph-mistake-head svg{flex:none;color:var(--soph-stone);transition:transform .2s}
.soph-mistake-head svg.is-open{transform:rotate(180deg);color:var(--soph-ink)}
.soph-mistake-body{padding:0 16px 17px 59px}
.soph-mistake-fix-label{display:flex;align-items:center;gap:7px;font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--soph-blue);margin-bottom:6px}
.soph-mistake-fix{font-size:14px;line-height:1.6;color:var(--soph-ink);max-width:80ch}
.soph-mistake-body .soph-ask{margin-top:13px}

/* preview */
.soph-preview-grades{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}
@media(min-width:820px){.soph-preview-grades{grid-template-columns:repeat(4,1fr)}}
.soph-preview-card{background:var(--soph-paper);border:1px solid var(--soph-line);border-radius:6px;padding:16px}
.soph-preview-grade{font-family:'Newsreader',Georgia,serif;font-size:24px;font-weight:600;line-height:1}
.soph-preview-window{margin-top:6px;font-size:11px;font-weight:600;letter-spacing:.05em;text-transform:uppercase;color:var(--soph-blue)}
.soph-preview-goal{margin-top:9px;font-size:13px;color:var(--soph-stone);line-height:1.5}
.soph-preview-count{margin-top:11px;font-size:12px;color:var(--soph-stone);font-weight:600}
.soph-full-link{display:inline-flex;align-items:center;gap:8px;margin-top:20px;background:var(--soph-blue);color:#fff;text-decoration:none;padding:12px 20px;border-radius:8px;font-size:14px;font-weight:600}
.soph-full-link:hover{background:#1a45c0}

/* empty state */
.soph-empty-state{display:flex;flex-direction:column;align-items:center;gap:12px;padding:48px 20px;color:var(--soph-stone);text-align:center}
.soph-empty-state svg{color:var(--soph-blue)}

@media print{
  .soph{border:0;padding:0}
  .soph-views,.soph-pills,.soph-print,.soph-ask,.soph-search{display:none!important}
  .soph-panel{border:0;padding:0}
}
`;
