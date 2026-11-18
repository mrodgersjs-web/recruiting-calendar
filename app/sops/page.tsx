import type { Metadata } from "next";
import { SiteFooter, SiteHeader } from "@/components/layout/site-chrome";
import AthleteSopHub from "@/components/upgrade/athlete-sop-hub";
import { loadAllAthleteSops, normalizeSportSlug } from "@/lib/site-data";

export const metadata: Metadata = {
  title: "Official Athlete SOP Playbooks (Grades 9-12) | The Commit Book",
  description:
    "Step-by-step college recruiting SOP checklists, verified NCAA/NAIA/NJCAA roster caps, highlight film standards, and camp spend rules for Football, Men's Basketball, Women's Basketball, and Women's Volleyball.",
};

export default async function SopsPage({
  searchParams,
}: {
  searchParams: Promise<{ sport?: string }>;
}) {
  const params = await searchParams;
  const sops = loadAllAthleteSops();
  const initialSport = normalizeSportSlug(params?.sport);

  return (
    <div className="flex min-h-screen flex-col bg-[#f7f5f0]">
      <SiteHeader activePath="/sops" />
      <main className="mx-auto w-full max-w-7xl flex-1 px-4 py-10 sm:px-6">
        <div className="mb-8 max-w-3xl space-y-2">
          <p className="font-mono text-xs font-semibold uppercase tracking-widest text-[#1d4ed8]">
            Official Commit Book Field Manuals · Grades 9-12
          </p>
          <h1 className="font-serif text-3xl font-semibold text-[#141413] sm:text-4xl">
            Athlete Recruiting SOP Playbooks
          </h1>
          <p className="text-base text-[#57534e] leading-relaxed">
            Every date, roster limit, video rule, and grade-by-grade action item verified against the 2026-27 NCAA D1/D2/D3, NAIA, and NJCAA rulebooks. Check off steps as your family completes them.
          </p>
        </div>
        <AthleteSopHub initialSport={initialSport} sops={sops} />
      </main>
      <SiteFooter />
    </div>
  );
}
