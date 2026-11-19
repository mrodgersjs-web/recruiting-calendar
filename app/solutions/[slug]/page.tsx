import type { Metadata } from "next";
import { notFound } from "next/navigation";
import type { ComponentType } from "react";
import { SiteFooter, SiteHeader } from "@/components/layout/site-chrome";
import CampDecisionReceipt from "@/components/solutions/camp-decision-receipt";
import { isSolutionSlug, SOLUTION_MAP, SOLUTIONS } from "@/components/solutions/catalog";
import FamilyRecruitingReceipt from "@/components/solutions/family-recruiting-receipt";
import FilmOutreachBrief from "@/components/solutions/film-outreach-brief";
import Next30Days from "@/components/solutions/next-30-days";
import OfferAidComparison from "@/components/solutions/offer-aid-comparison";
import ProgramFitCheck from "@/components/solutions/program-fit-check";
import type { SolutionSlug } from "@/components/solutions/types";

const COMPONENTS: Record<SolutionSlug, ComponentType> = {
  "next-30-days": Next30Days,
  "camp-decision-receipt": CampDecisionReceipt,
  "film-outreach-brief": FilmOutreachBrief,
  "family-recruiting-receipt": FamilyRecruitingReceipt,
  "offer-aid-comparison": OfferAidComparison,
  "program-fit-check": ProgramFitCheck,
};

export function generateStaticParams() {
  return SOLUTIONS.map((solution) => ({ slug: solution.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  if (!isSolutionSlug(slug)) return { title: "Tool Not Found | The Commit Book" };
  const definition = SOLUTION_MAP[slug];
  return { title: `${definition.title} | The Commit Book`, description: definition.summary };
}

export default async function SolutionPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  if (!isSolutionSlug(slug)) notFound();
  const Component = COMPONENTS[slug];
  return (
    <div className="flex min-h-screen flex-col bg-[#f7f5f0]">
      <SiteHeader activePath="/solutions" />
      <main className="mx-auto w-full max-w-7xl flex-1 px-4 py-10 sm:px-6">
        <Component />
      </main>
      <SiteFooter />
    </div>
  );
}
