import type { Metadata } from "next";
import Link from "next/link";
import { SiteFooter, SiteHeader } from "@/components/layout/site-chrome";
import { SOLUTIONS } from "@/components/solutions/catalog";

export const metadata: Metadata = {
  title: "Family Recruiting Tools | The Commit Book",
  description: "Six local-first tools for recruiting plans, camp decisions, film outreach, family receipts, offer comparisons, and program fit questions.",
};

export default function SolutionsPage() {
  return (
    <div className="flex min-h-screen flex-col bg-[#f7f5f0]">
      <SiteHeader activePath="/solutions" />
      <main className="mx-auto w-full max-w-7xl flex-1 px-4 py-10 sm:px-6">
        <div className="max-w-3xl">
          <p className="font-mono text-[10px] font-semibold uppercase tracking-[0.12em] text-[#1d4ed8]">The family decision layer</p>
          <h1 className="mt-3 font-serif text-4xl font-semibold tracking-tight sm:text-5xl">Tools for the next recruiting decision.</h1>
          <p className="mt-4 text-[16px] leading-relaxed text-[#57534e]">Answer the immediate question, keep the assumptions visible, and leave with an athlete-owned action. These tools run in your browser and do not require an account.</p>
        </div>
        <div className="mt-8 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {SOLUTIONS.map((solution, index) => (
            <Link className="group flex min-h-64 flex-col rounded-2xl border border-[#d9d3c8] bg-white p-5 transition hover:-translate-y-0.5 hover:border-[#1d4ed8] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#1d4ed8]" href={`/solutions/${solution.slug}`} key={solution.slug}>
              <div className="flex items-center"><span className="font-mono text-[11px] text-[#1d4ed8]">{String(index + 1).padStart(2, "0")}</span></div>
              <h2 className="mt-5 font-serif text-2xl font-semibold tracking-tight">{solution.title}</h2>
              <p className="mt-3 flex-1 text-[13px] leading-relaxed text-[#57534e]">{solution.summary}</p>
              <p className="mt-3 text-[12px] leading-relaxed text-[#141413]">{solution.outcome}</p>
              <span className="mt-5 text-[13px] font-semibold text-[#1d4ed8]">{solution.primaryAction} →</span>
            </Link>
          ))}
        </div>
        <p className="mt-8 rounded-xl border border-[#d9d3c8] bg-white p-4 text-[12px] leading-relaxed text-[#57534e]">Education, not legal advice. These tools use your entries and the linked reference pages. They do not promise coach interest, admission, aid, offers, or roster spots.</p>
      </main>
      <SiteFooter />
    </div>
  );
}
