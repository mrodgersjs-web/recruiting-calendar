"use client";

import { useEffect, useState } from "react";
import { SOLUTION_MAP } from "./catalog";
import { BUTTON_CLASS, downloadJson, Field, INPUT_CLASS, ResultBox, ToolShell } from "./shared";
import { CLASS_YEARS, LEVELS, SPORTS } from "./types";

const STORAGE_KEY = "commitbook.family-recruiting-receipt.v1";
const TASKS = ["Checked the contact window", "Prepared highlight film", "Prepared full-game fallback", "Sent athlete-owned outreach", "Reviewed academic checkpoints", "Evaluated camp spending"] as const;
type Task = (typeof TASKS)[number];
type ReceiptData = { sport: string; classYear: string; level: string; nextDate: string; source: string; tasks: Task[] };
const EMPTY: ReceiptData = { sport: "Football", classYear: "2029", level: "Undecided", nextDate: "", source: "", tasks: [] };

function validReceipt(value: unknown): value is ReceiptData {
  if (!value || typeof value !== "object") return false;
  const item = value as Partial<ReceiptData>;
  return typeof item.sport === "string" && typeof item.classYear === "string" && typeof item.level === "string" && typeof item.nextDate === "string" && typeof item.source === "string" && Array.isArray(item.tasks) && item.tasks.every((task) => TASKS.includes(task as Task));
}

export default function FamilyRecruitingReceipt() {
  const definition = SOLUTION_MAP["family-recruiting-receipt"];
  const [data, setData] = useState<ReceiptData>(EMPTY);
  const [loaded, setLoaded] = useState(false);
  const [status, setStatus] = useState("");

  useEffect(() => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        const parsed: unknown = JSON.parse(raw);
        if (validReceipt(parsed)) setData(parsed);
        else setStatus("The saved receipt had an invalid shape. A blank receipt is shown.");
      }
    } catch {
      setStatus("The saved receipt could not be read. A blank receipt is shown.");
    } finally {
      setLoaded(true);
    }
  }, []);

  const update = <K extends keyof ReceiptData>(key: K, value: ReceiptData[K]) => setData((current) => ({ ...current, [key]: value }));
  const save = () => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
      setStatus("Saved on this device.");
    } catch {
      setStatus("This browser blocked local saving. Export JSON instead.");
    }
  };

  return (
    <ToolShell definition={definition}>
      <div className="grid gap-6 lg:grid-cols-2">
        <form className="print-card rounded-2xl border border-[#d9d3c8] bg-white p-5" onSubmit={(e) => { e.preventDefault(); save(); }}>
          <div className="grid gap-4 sm:grid-cols-2">
            <Field label="Sport"><select className={INPUT_CLASS} value={data.sport} onChange={(e) => update("sport", e.target.value)}>{SPORTS.map((x) => <option key={x}>{x}</option>)}</select></Field>
            <Field label="Class year"><select className={INPUT_CLASS} value={data.classYear} onChange={(e) => update("classYear", e.target.value)}>{CLASS_YEARS.map((x) => <option key={x}>{x}</option>)}</select></Field>
            <Field label="Target level"><select className={INPUT_CLASS} value={data.level} onChange={(e) => update("level", e.target.value)}>{LEVELS.map((x) => <option key={x}>{x}</option>)}</select></Field>
            <Field label="Next family-entered date" hint="Planning date only, not presented as an NCAA deadline."><input className={INPUT_CLASS} type="date" value={data.nextDate} onChange={(e) => update("nextDate", e.target.value)} /></Field>
            <div className="sm:col-span-2"><Field label="Source link (optional)"><input className={INPUT_CLASS} placeholder="https://" type="url" value={data.source} onChange={(e) => update("source", e.target.value)} /></Field></div>
          </div>
          <fieldset className="mt-5"><legend className="mb-2 text-[12px] font-semibold">Completed athlete-owned actions</legend>{TASKS.map((task) => <label className="flex min-h-11 items-center gap-2 border-t border-[#e5e0d6] text-[13px]" key={task}><input checked={data.tasks.includes(task)} onChange={(e) => update("tasks", e.target.checked ? [...data.tasks, task] : data.tasks.filter((x) => x !== task))} type="checkbox" />{task}</label>)}</fieldset>
          <button className={`${BUTTON_CLASS} mt-5 w-full no-print`} disabled={!loaded} type="submit">{definition.primaryAction}</button>
          <p aria-live="polite" className="mt-3 text-[12px] text-[#57534e]">{status}</p>
        </form>
        <ResultBox title={`${data.sport} · Class of ${data.classYear}`}>
          <dl className="grid grid-cols-2 gap-4 text-[13px]"><div><dt className="text-[#57534e]">Target level</dt><dd className="font-semibold">{data.level}</dd></div><div><dt className="text-[#57534e]">Next planning date</dt><dd className="font-semibold">{data.nextDate || "Not entered"}</dd></div></dl>
          <h3 className="mt-5 text-[13px] font-semibold">Completed actions</h3>
          {data.tasks.length ? <ul className="mt-2 list-disc space-y-1 pl-5 text-[13px]">{data.tasks.map((task) => <li key={task}>{task}</li>)}</ul> : <p className="mt-2 text-[13px] text-[#57534e]">No action marked complete yet.</p>}
          {data.source ? <p className="mt-4 break-all text-[12px]"><b>Entered source:</b> {data.source}</p> : null}
          <p className="mt-5 rounded-xl bg-[#f7f5f0] p-4 text-[12px] text-[#57534e]">Athlete owns the actions. Parent supports the weekly review. Dates and sources on this receipt are family-entered until checked against the linked rule tools.</p>
          <div className="mt-5 flex flex-wrap gap-2 no-print"><button className={BUTTON_CLASS} disabled={!loaded} onClick={() => setStatus(downloadJson("family-recruiting-receipt.json", { schemaVersion: 1, ...data }) ? "JSON receipt downloaded." : "Export failed. Print the receipt instead.")} type="button">Export JSON</button><button className={BUTTON_CLASS} disabled={!loaded} onClick={() => window.print()} type="button">Print receipt</button><button className={BUTTON_CLASS} disabled={!loaded} onClick={() => { setData(EMPTY); localStorage.removeItem(STORAGE_KEY); setStatus("Local receipt cleared."); }} type="button">Clear local receipt</button></div>
        </ResultBox>
      </div>
    </ToolShell>
  );
}
