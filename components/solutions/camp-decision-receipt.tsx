"use client";

import { useState } from "react";
import { SOLUTION_MAP } from "./catalog";
import { BUTTON_CLASS, currency, downloadJson, Field, INPUT_CLASS, ResultBox, ToolShell } from "./shared";

type Decision = { label: "CONSIDER" | "SKIP" | "NEED MORE INFO"; reasons: string[]; total: number | null };
const ATTENDANCE_LABELS: Record<string, string> = { unknown: "Unknown", verified: "Verified in writing", "not-verified": "Claimed, not verified", none: "No relevant coach attending" };
const REFUND_LABELS: Record<string, string> = { unknown: "Unknown", written: "Written terms reviewed", none: "No refund" };
const FILM_LABELS: Record<string, string> = { unknown: "Unknown", included: "Film included", own: "May record our own film", none: "No usable film" };

export default function CampDecisionReceipt() {
  const definition = SOLUTION_MAP["camp-decision-receipt"];
  const [campName, setCampName] = useState("");
  const [campFee, setCampFee] = useState("");
  const [travelCost, setTravelCost] = useState("");
  const [attendance, setAttendance] = useState("unknown");
  const [format, setFormat] = useState("");
  const [refund, setRefund] = useState("unknown");
  const [film, setFilm] = useState("unknown");
  const [decision, setDecision] = useState<Decision | null>(null);
  const [exportStatus, setExportStatus] = useState("");

  const evaluate = () => {
    const reasons: string[] = [];
    const fee = campFee.trim() === "" ? null : Number(campFee);
    const travel = travelCost.trim() === "" ? null : Number(travelCost);
    const validCosts = fee !== null && travel !== null && Number.isFinite(fee) && Number.isFinite(travel) && fee >= 0 && travel >= 0;
    if (!validCosts) reasons.push("Enter numeric camp and travel costs, including $0 when that is the actual cost.");
    if (attendance === "unknown") reasons.push("Confirm whether coaches from relevant target programs will actually evaluate athletes.");
    if (!format.trim()) reasons.push("Enter the camp format and the athlete’s actual evaluation opportunity.");
    if (refund === "unknown") reasons.push("Confirm the refund terms if listed coaches cancel.");
    if (film === "unknown") reasons.push("Confirm whether film is included or may be recorded.");
    let label: Decision["label"] = "NEED MORE INFO";
    if (reasons.length === 0) {
      if (attendance === "verified") {
        label = "CONSIDER";
        reasons.push("Relevant coach attendance and all requested terms are marked verified or known.");
      } else {
        label = "SKIP";
        reasons.push(attendance === "none" ? "No relevant target-program coach is marked as attending." : "Relevant coach attendance is not verified.");
      }
    }
    setDecision({ label, reasons, total: validCosts ? Number(fee) + Number(travel) : null });
  };

  const receipt = () => ({ schemaVersion: 1, campName, campFee, travelCost, attendance, format, refund, film, decision });

  return (
    <ToolShell definition={definition}>
      <div className="grid gap-6 lg:grid-cols-2">
        <form className="print-card rounded-2xl border border-[#d9d3c8] bg-white p-5" onSubmit={(e) => { e.preventDefault(); evaluate(); }}>
          <div className="grid gap-4 sm:grid-cols-2">
            <div className="sm:col-span-2"><Field label="Camp or showcase label (optional)"><input className={INPUT_CLASS} value={campName} onChange={(e) => setCampName(e.target.value)} /></Field></div>
            <Field label="Camp fee"><input className={INPUT_CLASS} inputMode="decimal" min="0" placeholder="Enter 0 if free" type="number" value={campFee} onChange={(e) => setCampFee(e.target.value)} /></Field>
            <Field label="Travel and lodging cost"><input className={INPUT_CLASS} inputMode="decimal" min="0" placeholder="Enter 0 if none" type="number" value={travelCost} onChange={(e) => setTravelCost(e.target.value)} /></Field>
            <Field label="Relevant coach attendance"><select className={INPUT_CLASS} value={attendance} onChange={(e) => setAttendance(e.target.value)}><option value="unknown">Unknown</option><option value="verified">Verified in writing</option><option value="not-verified">Claimed, not verified</option><option value="none">No relevant coach attending</option></select></Field>
            <Field label="Refund terms"><select className={INPUT_CLASS} value={refund} onChange={(e) => setRefund(e.target.value)}><option value="unknown">Unknown</option><option value="written">Written terms reviewed</option><option value="none">No refund</option></select></Field>
            <div className="sm:col-span-2"><Field label="Evaluation format"><input className={INPUT_CLASS} placeholder="Example: live games plus measured skills" value={format} onChange={(e) => setFormat(e.target.value)} /></Field></div>
            <Field label="Film terms"><select className={INPUT_CLASS} value={film} onChange={(e) => setFilm(e.target.value)}><option value="unknown">Unknown</option><option value="included">Film included</option><option value="own">May record our own film</option><option value="none">No usable film</option></select></Field>
          </div>
          <button className={`${BUTTON_CLASS} mt-5 w-full no-print`} type="submit">{definition.primaryAction}</button>
        </form>
        <ResultBox title={decision ? decision.label : "Decision receipt"}>
          {decision ? <>
            {decision.total !== null ? <p className="mb-4 font-serif text-3xl font-semibold">Total entered cost: {currency(decision.total)}</p> : <p className="mb-4 text-[#57534e]">No total is shown until both costs are valid numbers.</p>}
            <ul className="list-disc space-y-2 pl-5 text-[13px] text-[#57534e]">{decision.reasons.map((reason) => <li key={reason}>{reason}</li>)}</ul>
            <dl className="mt-5 grid grid-cols-2 gap-3 border-t border-[#e5e0d6] pt-4 text-[12px]"><div><dt className="text-[#57534e]">Camp label</dt><dd className="font-semibold">{campName || "Not entered"}</dd></div><div><dt className="text-[#57534e]">Camp fee</dt><dd className="font-semibold">{campFee === "" ? "Missing" : currency(Number(campFee))}</dd></div><div><dt className="text-[#57534e]">Travel cost</dt><dd className="font-semibold">{travelCost === "" ? "Missing" : currency(Number(travelCost))}</dd></div><div><dt className="text-[#57534e]">Attendance</dt><dd className="font-semibold">{ATTENDANCE_LABELS[attendance]}</dd></div><div><dt className="text-[#57534e]">Format</dt><dd className="font-semibold">{format || "Missing"}</dd></div><div><dt className="text-[#57534e]">Refund</dt><dd className="font-semibold">{REFUND_LABELS[refund]}</dd></div><div><dt className="text-[#57534e]">Film</dt><dd className="font-semibold">{FILM_LABELS[film]}</dd></div></dl>
            <p className="mt-4 text-[11px] text-[#57534e]">This is a transparent heuristic using only your entries. It does not predict exposure, offers, or coach interest.</p>
            <div className="mt-5 flex flex-wrap gap-2 no-print"><button className={BUTTON_CLASS} onClick={() => setExportStatus(downloadJson("camp-decision-receipt.json", receipt()) ? "JSON receipt downloaded." : "Export failed. Print the receipt instead.")} type="button">Save JSON receipt</button><button className={BUTTON_CLASS} onClick={() => window.print()} type="button">Print</button></div>
            <p aria-live="polite" className="mt-3 text-[12px] text-[#57534e] no-print">{exportStatus}</p>
          </> : <p className="text-[14px] text-[#57534e]">Complete the known fields. Missing information stays visible instead of becoming a pass.</p>}
        </ResultBox>
      </div>
    </ToolShell>
  );
}
