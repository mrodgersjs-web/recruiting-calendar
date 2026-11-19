"use client";

import { useState } from "react";
import { SOLUTION_MAP } from "./catalog";
import { BUTTON_CLASS, Field, INPUT_CLASS, ResultBox, ToolShell } from "./shared";
import { CLASS_YEARS, SPORTS } from "./types";

export default function FilmOutreachBrief() {
  const definition = SOLUTION_MAP["film-outreach-brief"];
  const [sport, setSport] = useState("Volleyball");
  const [classYear, setClassYear] = useState("2029");
  const [position, setPosition] = useState("");
  const [measurable, setMeasurable] = useState("");
  const [highlightLink, setHighlightLink] = useState("");
  const [fullGameLink, setFullGameLink] = useState("");
  const [brief, setBrief] = useState("");
  const [status, setStatus] = useState("");

  const createBrief = () => {
    if (!position.trim() || !highlightLink.trim()) {
      setStatus("Enter the position and highlight link before creating the brief.");
      setBrief("");
      return;
    }
    const lines = [
      `Subject: Class of ${classYear} ${position.trim()} - ${sport} recruiting information`,
      "",
      "Hello Coach,",
      "",
      `I am a Class of ${classYear} ${position.trim()} interested in your ${sport.toLowerCase()} program.`,
    ];
    if (measurable.trim()) lines.push(`Family-entered measurable (not checked by this tool): ${measurable.trim()}.`);
    lines.push(`Highlight film: ${highlightLink.trim()}`);
    if (fullGameLink.trim()) lines.push(`Full game: ${fullGameLink.trim()}`);
    lines.push("", "Please let me know which recruiting information or upcoming steps you would like from me.", "", "Thank you for your time.");
    setBrief(lines.join("\n"));
    setStatus("Brief created. Check both links before using the message.");
  };

  const copy = async () => {
    try {
      await navigator.clipboard.writeText(brief);
      setStatus("Copied to clipboard.");
    } catch {
      setStatus("Copy was blocked. Select the brief text and copy it manually.");
    }
  };

  return (
    <ToolShell definition={definition}>
      <div className="grid gap-6 lg:grid-cols-2">
        <form className="print-card rounded-2xl border border-[#d9d3c8] bg-white p-5" onSubmit={(e) => { e.preventDefault(); createBrief(); }}>
          <div className="grid gap-4 sm:grid-cols-2">
            <Field label="Sport"><select className={INPUT_CLASS} value={sport} onChange={(e) => { setSport(e.target.value); setBrief(""); }}>{SPORTS.map((x) => <option key={x}>{x}</option>)}</select></Field>
            <Field label="Class year"><select className={INPUT_CLASS} value={classYear} onChange={(e) => { setClassYear(e.target.value); setBrief(""); }}>{CLASS_YEARS.map((x) => <option key={x}>{x}</option>)}</select></Field>
            <Field label="Position or event"><input className={INPUT_CLASS} value={position} onChange={(e) => { setPosition(e.target.value); setBrief(""); }} /></Field>
            <Field label="Measurable (optional)" hint="Leave blank rather than estimating."><input className={INPUT_CLASS} value={measurable} onChange={(e) => { setMeasurable(e.target.value); setBrief(""); }} /></Field>
            <div className="sm:col-span-2"><Field label="Highlight film link"><input className={INPUT_CLASS} placeholder="https://" type="url" value={highlightLink} onChange={(e) => { setHighlightLink(e.target.value); setBrief(""); }} /></Field></div>
            <div className="sm:col-span-2"><Field label="Full-game link (optional fallback)"><input className={INPUT_CLASS} placeholder="https://" type="url" value={fullGameLink} onChange={(e) => { setFullGameLink(e.target.value); setBrief(""); }} /></Field></div>
          </div>
          <button className={`${BUTTON_CLASS} mt-5 w-full no-print`} type="submit">{definition.primaryAction}</button>
          <p aria-live="polite" className="mt-3 text-[12px] text-[#57534e]">{status}</p>
        </form>
        <ResultBox title="Coach message + pre-send checks">
          {brief ? <><textarea aria-label="Generated coach message" className={`${INPUT_CLASS} min-h-72 font-mono text-[12px] leading-relaxed`} readOnly value={brief} /><button className={`${BUTTON_CLASS} mt-3 no-print`} onClick={copy} type="button">Copy message</button></> : <p className="text-[14px] text-[#57534e]">The message uses only the details you enter. It never adds a metric or implies coach interest.</p>}
          <fieldset className="mt-5 rounded-xl bg-[#f7f5f0] p-4"><legend className="px-1 text-[12px] font-semibold">Before sending</legend><label className="flex min-h-11 items-center gap-2 text-[13px]"><input type="checkbox" /> I opened the highlight link while logged out</label><label className="flex min-h-11 items-center gap-2 text-[13px]"><input type="checkbox" /> I opened the full-game fallback while logged out and confirmed it is ready</label><label className="flex min-h-11 items-center gap-2 text-[13px]"><input type="checkbox" /> Athlete checked spelling, class year, position, and program</label></fieldset>
        </ResultBox>
      </div>
    </ToolShell>
  );
}
