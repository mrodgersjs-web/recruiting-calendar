"use client";

import Link from "next/link";
import { useState } from "react";
import { SOLUTION_MAP } from "./catalog";
import { BUTTON_CLASS, Field, INPUT_CLASS, ResultBox, ToolShell } from "./shared";
import { CLASS_YEARS, LEVELS, SPORTS } from "./types";

type Need = "start" | "film" | "camp" | "eligibility";
type Action = { title: string; detail: string; href: string; link: string };

const PRIMARY: Record<Need, Action> = {
  start: { title: "Check the applicable window", detail: "Use your sport, class year, and target level. Save the source before planning outreach.", href: "/window", link: "Open Window Finder" },
  film: { title: "Audit the film package", detail: "Choose the clearest highlights, keep the full game available, and test both links logged out.", href: "/sops", link: "Open Athlete SOPs" },
  camp: { title: "Run the camp decision check", detail: "Record total cost, relevant coach attendance, refund terms, and the free outreach alternative.", href: "/solutions/camp-decision-receipt", link: "Open Camp Decision Receipt" },
  eligibility: { title: "Review the academic checkpoints", detail: "Take the transcript and core-course questions to the counselor. Record what still needs verification.", href: "/sops", link: "Open Athlete SOPs" },
};

export default function Next30Days() {
  const definition = SOLUTION_MAP["next-30-days"];
  const [sport, setSport] = useState("Football");
  const [classYear, setClassYear] = useState("2029");
  const [level, setLevel] = useState("Undecided");
  const [need, setNeed] = useState<Need>("start");
  const [submitted, setSubmitted] = useState(false);

  const primary = PRIMARY[need];
  const actions: Action[] = [
    primary,
    {
      title: `Prepare the ${sport.toLowerCase()} evidence`,
      detail: need === "film" ? "Finish the link checks, then record where the film was sent and when to follow up." : `Create one current ${sport.toLowerCase()} film link and one full-game fallback. Keep both usable on a phone.`,
      href: "/solutions/film-outreach-brief",
      link: "Build Film + Outreach Brief",
    },
    {
      title: "Save the family receipt",
      detail: `Athlete: mark each completed action. Parent: hold one weekly review for the Class of ${classYear} plan and ${level.toLowerCase()} questions.`,
      href: "/solutions/family-recruiting-receipt",
      link: "Open Family Recruiting Receipt",
    },
  ];

  return (
    <ToolShell definition={definition}>
      <div className="grid gap-6 lg:grid-cols-[0.8fr_1.2fr]">
        <form className="print-card h-fit rounded-2xl border border-[#d9d3c8] bg-white p-5" onSubmit={(event) => { event.preventDefault(); setSubmitted(true); }}>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-1">
            <Field label="Sport"><select className={INPUT_CLASS} value={sport} onChange={(e) => { setSport(e.target.value); setSubmitted(false); }}>{SPORTS.map((x) => <option key={x}>{x}</option>)}</select></Field>
            <Field label="Class year"><select className={INPUT_CLASS} value={classYear} onChange={(e) => { setClassYear(e.target.value); setSubmitted(false); }}>{CLASS_YEARS.map((x) => <option key={x}>{x}</option>)}</select></Field>
            <Field label="Target level"><select className={INPUT_CLASS} value={level} onChange={(e) => { setLevel(e.target.value); setSubmitted(false); }}>{LEVELS.map((x) => <option key={x}>{x}</option>)}</select></Field>
            <Field label="What do you need first?"><select className={INPUT_CLASS} value={need} onChange={(e) => { setNeed(e.target.value as Need); setSubmitted(false); }}><option value="start">Where to start</option><option value="film">Film and outreach</option><option value="camp">A camp decision</option><option value="eligibility">Eligibility and grades</option></select></Field>
          </div>
          <button className={`${BUTTON_CLASS} mt-5 w-full no-print`} type="submit">{definition.primaryAction}</button>
          <p className="mt-3 text-[11px] leading-relaxed text-[#57534e]">No dates are guessed here. Use the linked rule tools to verify the details you would act on.</p>
        </form>
        <ResultBox title={submitted ? `Class of ${classYear}: the next three actions` : "Your plan will appear here"}>
          {submitted ? <ol className="space-y-4">{actions.map((action, index) => <li className="border-t border-[#e5e0d6] pt-4 first:border-0 first:pt-0" key={action.title}><p className="font-mono text-[10px] text-[#1d4ed8]">ACTION {index + 1}</p><h3 className="mt-1 font-semibold">{action.title}</h3><p className="mt-1 text-[13px] leading-relaxed text-[#57534e]">{action.detail}</p><Link className="mt-2 inline-block text-[12px] font-semibold text-[#1d4ed8]" href={action.href}>{action.link} →</Link></li>)}</ol> : <p className="text-[14px] text-[#57534e]">Choose the athlete’s context and build the plan. Nothing is uploaded or saved.</p>}
          <div className="mt-5 rounded-xl bg-[#f7f5f0] p-4 text-[13px]"><b>Parent support action:</b> schedule one check-in, review the receipt, and let the athlete own the next message or task.</div>
        </ResultBox>
      </div>
    </ToolShell>
  );
}
