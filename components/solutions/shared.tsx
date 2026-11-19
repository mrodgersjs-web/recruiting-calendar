"use client";

import Link from "next/link";
import type { ReactNode } from "react";
import type { SourceLink, SolutionDefinition } from "./types";

export const INPUT_CLASS =
  "min-h-11 w-full rounded-xl border border-[#d9d3c8] bg-white px-3 py-2 text-[14px] text-[#141413] outline-none focus:border-[#1d4ed8] focus:ring-2 focus:ring-[#1d4ed8]/15";
export const LABEL_CLASS = "mb-1.5 block text-[12px] font-semibold text-[#3f3b36]";
export const BUTTON_CLASS =
  "inline-flex min-h-11 items-center justify-center rounded-full bg-[#141413] px-5 py-2.5 text-[13px] font-semibold text-white transition hover:bg-[#1d4ed8] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#1d4ed8] disabled:cursor-not-allowed disabled:opacity-50";

export function ToolShell({
  definition,
  children,
}: {
  definition: SolutionDefinition;
  children: ReactNode;
}) {
  return (
    <div className="solution-tool">
      <style>{`
        @media print {
          header, footer, [data-testid="commitbook-chat-launcher"], #commitbook-chat-dialog, .no-print { display: none !important; }
          body, main, .solution-tool { background: white !important; }
          .solution-tool { padding: 0 !important; }
          .print-card { border: 0 !important; box-shadow: none !important; }
        }
      `}</style>
      <div className="mb-7 max-w-3xl">
        <p className="mb-2 font-mono text-[10px] font-semibold uppercase tracking-[0.12em] text-[#1d4ed8]">
          {definition.eyebrow}
        </p>
        <h1 className="font-serif text-4xl font-semibold tracking-tight text-[#141413] sm:text-5xl">
          {definition.title}
        </h1>
        <p className="mt-4 text-[16px] leading-relaxed text-[#57534e]">{definition.summary}</p>
        <p className="mt-2 text-[13px] text-[#57534e]">{definition.outcome}</p>
      </div>
      {children}
      <div className="mt-7 flex flex-wrap items-center gap-3 border-t border-[#d9d3c8] pt-5 text-[12px] no-print">
        <Link className="font-semibold text-[#1d4ed8] focus-visible:rounded focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#1d4ed8]" href="/solutions">← All family tools</Link>
        <SourceLinks links={definition.sourceLinks} />
      </div>
    </div>
  );
}

export function Field({
  label,
  children,
  hint,
}: {
  label: string;
  children: ReactNode;
  hint?: string;
}) {
  return (
    <label className="block">
      <span className={LABEL_CLASS}>{label}</span>
      {children}
      {hint ? <span className="mt-1 block text-[11px] text-[#57534e]">{hint}</span> : null}
    </label>
  );
}

export function ResultBox({ title, children }: { title: string; children: ReactNode }) {
  return (
    <section aria-live="polite" className="print-card rounded-2xl border border-[#d9d3c8] bg-white p-5 shadow-sm">
      <h2 className="mb-4 font-serif text-2xl font-semibold tracking-tight">{title}</h2>
      {children}
    </section>
  );
}

export function SourceLinks({ links }: { links: SourceLink[] }) {
  return (
    <span className="flex flex-wrap gap-3">
      {links.map((link) => (
        <Link className="font-semibold text-[#1d4ed8] underline-offset-2 hover:underline focus-visible:rounded focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#1d4ed8]" href={link.href} key={link.href}>
          {link.label} →
        </Link>
      ))}
    </span>
  );
}

export function currency(value: number): string {
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(value);
}

export function downloadJson(filename: string, value: unknown): boolean {
  try {
    const blob = new Blob([JSON.stringify(value, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = filename;
    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();
    window.setTimeout(() => URL.revokeObjectURL(url), 1000);
    return true;
  } catch {
    return false;
  }
}
