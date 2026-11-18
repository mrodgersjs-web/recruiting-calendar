import type { Metadata } from "next";
import { SiteFooter, SiteHeader } from "@/components/layout/site-chrome";
import TenOffersLab from "@/components/upgrade/ten-offers-lab";
import { loadOffersCatalog } from "@/lib/site-data";

export const metadata: Metadata = {
  title: "10 Athlete & Family Recruiting Offerings | The Commit Book",
  description:
    "Ten focused, plain-price recruiting diagnostics and playbooks grounded in 348 real parent, athlete, and coach conversations.",
};

export default function OffersPage() {
  const catalog = loadOffersCatalog();

  return (
    <div className="flex min-h-screen flex-col bg-[#f7f5f0]">
      <SiteHeader activePath="/offers" />
      <main className="mx-auto w-full max-w-7xl flex-1 px-4 py-10 sm:px-6">
        <TenOffersLab catalog={catalog} />
      </main>
      <SiteFooter />
    </div>
  );
}
