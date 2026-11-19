"use client";

import { useState } from "react";
import { SOLUTION_MAP } from "./catalog";
import { BUTTON_CLASS, INPUT_CLASS, ResultBox, ToolShell } from "./shared";

type Status = "unknown" | "strong" | "concern";
type EvidenceItem = { id: string; label: string; question: string; status: Status; evidence: string };
const INITIAL: EvidenceItem[] = [
  { id: "retention", label: "Roster retention", question: "How many athletes remain in the program across their college years?", status: "unknown", evidence: "" },
  { id: "coaching", label: "Coaching continuity", question: "How long has the current staff been in place, and what has changed?", status: "unknown", evidence: "" },
  { id: "academics", label: "Academic support", question: "What tutoring, advising, travel, and missed-class support is available?", status: "unknown", evidence: "" },
  { id: "development", label: "Athlete development", question: "How does the program develop athletes beyond the immediate starters?", status: "unknown", evidence: "" },
  { id: "transfers", label: "Transfer and roster pattern", question: "What do recent entries, exits, and roster composition show?", status: "unknown", evidence: "" },
];

export default function ProgramFitCheck() {
  const definition = SOLUTION_MAP["program-fit-check"];
  const [items, setItems] = useState<EvidenceItem[]>(INITIAL);
  const [reviewed, setReviewed] = useState<EvidenceItem[] | null>(null);
  const update = (id: string, key: "status" | "evidence", value: string) => { setItems((current) => current.map((item) => item.id === id ? { ...item, [key]: value } : item)); setReviewed(null); };
  const concerns = reviewed?.filter((item) => item.status === "concern") ?? [];
  const unknowns = reviewed?.filter((item) => item.status === "unknown" || !item.evidence.trim()) ?? [];

  return (
    <ToolShell definition={definition}>
      <form className="print-card rounded-2xl border border-[#d9d3c8] bg-white p-5" onSubmit={(e) => { e.preventDefault(); setReviewed(items.map((item) => ({ ...item }))); }}>
        <div className="space-y-5">{items.map((item) => <fieldset className="rounded-xl border border-[#e5e0d6] p-4" key={item.id}><legend className="px-1 text-[13px] font-semibold">{item.label}</legend><p className="mb-3 text-[12px] text-[#57534e]">{item.question}</p><div className="grid gap-3 md:grid-cols-[0.6fr_1.4fr]"><label><span className="mb-1.5 block text-[12px] font-semibold">Evidence assessment</span><select aria-label={`${item.label} evidence assessment`} className={INPUT_CLASS} value={item.status} onChange={(e) => update(item.id, "status", e.target.value)}><option value="unknown">Unknown</option><option value="strong">Strong evidence</option><option value="concern">Concern</option></select></label><label><span className="mb-1.5 block text-[12px] font-semibold">Evidence note or source</span><input aria-label={`${item.label} evidence note or source`} className={INPUT_CLASS} placeholder="Record what you actually checked" value={item.evidence} onChange={(e) => update(item.id, "evidence", e.target.value)} /></label></div></fieldset>)}</div>
        <button className={`${BUTTON_CLASS} mt-5 no-print`} type="submit">{definition.primaryAction}</button>
      </form>
      <div className="mt-6"><ResultBox title="Evidence gaps + questions to ask">
        {reviewed ? <div className="grid gap-6 md:grid-cols-2"><section><h3 className="font-semibold text-[#b91c1c]">Red flags from your entries</h3>{concerns.length ? <ul className="mt-2 space-y-3 text-[13px]">{concerns.map((item) => <li className="rounded-xl bg-[#f7ecea] p-3" key={item.id}><b>{item.label}</b><p className="mt-1">Input: {item.evidence || "Concern selected without an evidence note"}</p><p className="mt-1">{item.question}</p></li>)}</ul> : <p className="mt-2 text-[13px] text-[#57534e]">No concern was selected. This does not clear the unknowns.</p>}</section><section><h3 className="font-semibold">Unknowns, not passes</h3>{unknowns.length ? <ul className="mt-2 list-disc space-y-2 pl-5 text-[13px]">{unknowns.map((item) => <li key={item.id}><b>{item.label}:</b> {item.status === "unknown" ? "No assessment entered" : "Assessment entered without an evidence note"}. {item.question}</li>)}</ul> : <p className="mt-2 text-[13px] text-[#57534e]">Every item has an assessment and evidence note. Recheck the underlying sources before deciding.</p>}</section></div> : <p className="text-[14px] text-[#57534e]">Unanswered items remain unknown. The result is a question list, not a score or college choice.</p>}
        <button className={`${BUTTON_CLASS} mt-5 no-print`} onClick={() => window.print()} type="button">Print question list</button>
      </ResultBox></div>
    </ToolShell>
  );
}
