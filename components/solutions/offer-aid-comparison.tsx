"use client";

import { useState } from "react";
import { SOLUTION_MAP } from "./catalog";
import { BUTTON_CLASS, currency, INPUT_CLASS, ResultBox, ToolShell } from "./shared";

type OfferRow = { id: number; school: string; offerStatus: string; totalCost: string; athleticAid: string; academicAid: string; needAid: string; signingDate: string; dateStatus: string };
const blankRow = (id: number): OfferRow => ({ id, school: "", offerStatus: "none", totalCost: "", athleticAid: "", academicAid: "", needAid: "", signingDate: "", dateStatus: "unknown" });
const numberOrZero = (value: string) => value.trim() === "" ? 0 : Number(value);
const validNumber = (value: string) => value.trim() !== "" && Number.isFinite(Number(value)) && Number(value) >= 0;
const moneyLabel = (value: string) => value.trim() === "" ? "left blank, counted as $0" : currency(Number(value));

export default function OfferAidComparison() {
  const definition = SOLUTION_MAP["offer-aid-comparison"];
  const [rows, setRows] = useState<OfferRow[]>([blankRow(1), blankRow(2)]);
  const [compared, setCompared] = useState<OfferRow[] | null>(null);
  const update = (id: number, key: keyof OfferRow, value: string) => { setRows((current) => current.map((row) => row.id === id ? { ...row, [key]: value } : row)); setCompared(null); };
  const net = (row: OfferRow) => validNumber(row.totalCost) ? Number(row.totalCost) - numberOrZero(row.athleticAid) - numberOrZero(row.academicAid) - numberOrZero(row.needAid) : null;

  return (
    <ToolShell definition={definition}>
      <form className="print-card rounded-2xl border border-[#d9d3c8] bg-white p-5" onSubmit={(e) => { e.preventDefault(); setCompared(rows.map((row) => ({ ...row }))); }}>
        <div aria-label="Program comparison inputs" className="overflow-x-auto" role="region" tabIndex={0}>
          <table className="w-full min-w-[1040px] border-collapse text-left text-[12px]">
            <thead><tr className="bg-[#f7f5f0]"><th className="p-2">Program</th><th className="p-2">Offer status</th><th className="p-2">Annual total cost</th><th className="p-2">Athletic aid</th><th className="p-2">Academic aid</th><th className="p-2">Need-based aid</th><th className="p-2">Signing date</th><th className="p-2">Date status</th></tr></thead>
            <tbody>{rows.map((row) => <tr className="border-t border-[#e5e0d6]" key={row.id}>
              <td className="p-2"><input aria-label={`Program ${row.id}`} className={INPUT_CLASS} value={row.school} onChange={(e) => update(row.id, "school", e.target.value)} /></td>
              <td className="p-2"><select aria-label={`Program ${row.id} offer status`} className={INPUT_CLASS} value={row.offerStatus} onChange={(e) => update(row.id, "offerStatus", e.target.value)}><option value="none">No offer entered</option><option value="verbal">Verbal</option><option value="written">Written</option></select></td>
              {(["totalCost", "athleticAid", "academicAid", "needAid"] as const).map((key) => <td className="p-2" key={key}><input aria-label={`Program ${row.id} ${key}`} className={INPUT_CLASS} inputMode="decimal" min="0" placeholder={key === "totalCost" ? "Required for net cost" : "Blank = 0"} type="number" value={row[key]} onChange={(e) => update(row.id, key, e.target.value)} /></td>)}
              <td className="p-2"><input aria-label={`Program ${row.id} signing date`} className={INPUT_CLASS} placeholder="Family-entered" value={row.signingDate} onChange={(e) => update(row.id, "signingDate", e.target.value)} /></td>
              <td className="p-2"><select aria-label={`Program ${row.id} date status`} className={INPUT_CLASS} value={row.dateStatus} onChange={(e) => update(row.id, "dateStatus", e.target.value)}><option value="unknown">Unknown</option><option value="published">Published</option><option value="projected">Projected</option></select></td>
            </tr>)}</tbody>
          </table>
        </div>
        <div className="mt-4 flex flex-wrap gap-2 no-print"><button className={BUTTON_CLASS} type="submit">{definition.primaryAction}</button><button className={BUTTON_CLASS} disabled={rows.length >= 4} onClick={() => setRows((current) => [...current, blankRow(Date.now())])} type="button">Add program</button><button className={BUTTON_CLASS} disabled={rows.length <= 1} onClick={() => { setRows((current) => current.slice(0, -1)); setCompared(null); }} type="button">Remove last</button></div>
      </form>
      <div className="mt-6"><ResultBox title="Comparison using only entered values">
        {compared ? <div aria-label="Program comparison results" className="overflow-x-auto" role="region" tabIndex={0}><table className="w-full min-w-[760px] border-collapse text-[12px]"><thead><tr className="border-b border-[#d9d3c8] text-left"><th className="p-2">Program</th><th className="p-2">Offer</th><th className="p-2">Annual net</th><th className="p-2">Signing date</th><th className="p-2">Aid assumptions</th></tr></thead><tbody>{compared.map((row) => { const value = net(row); return <tr className="border-b border-[#e5e0d6]" key={row.id}><td className="p-2 font-semibold">{row.school || `Program ${row.id}`}</td><td className="p-2">{row.offerStatus}</td><td className="p-2">{value === null ? <span className="text-[#b91c1c]">Annual total cost left blank or invalid; no net cost.</span> : <><b>{currency(Math.max(0, value))}</b>{value < 0 ? <span className="block text-[#b91c1c]">Raw result {currency(value)}; floored to $0 because entered aid exceeds cost.</span> : null}</>}</td><td className="p-2">{row.signingDate || "Not entered"} <span className="block uppercase text-[#57534e]">{row.dateStatus}</span></td><td className="p-2">Athletic: {moneyLabel(row.athleticAid)}<br />Academic: {moneyLabel(row.academicAid)}<br />Need-based: {moneyLabel(row.needAid)}</td></tr>; })}</tbody></table></div> : <p className="text-[14px] text-[#57534e]">Enter up to four programs. Blank aid is shown as blank-as-zero in the result, never as aid you received.</p>}
        <p className="mt-4 text-[11px] text-[#57534e]">All values and dates are user-entered. Verify the actual documents and published sources before making a decision.</p>
        <button className={`${BUTTON_CLASS} mt-4 no-print`} onClick={() => window.print()} type="button">Print comparison</button>
      </ResultBox></div>
    </ToolShell>
  );
}
