import type { Metadata } from "next";
import { SiteFooter, SiteHeader } from "@/components/layout/site-chrome";
import RecruitingWindowFinder from "@/components/upgrade/recruiting-window-finder";

export const metadata: Metadata = {
  title: "30-Second Recruiting Window & Roster Cap Calculator | The Commit Book",
  description:
    "Select your sport, graduation year, and division target to see exact legal coach contact dates, official visit openings, and roster limits.",
};

export default function WindowCalculatorPage() {
  return (
    <div className="flex min-h-screen flex-col bg-[#f7f5f0]">
      <SiteHeader activePath="/window" />
      <main className="mx-auto w-full max-w-7xl flex-1 px-4 py-10 sm:px-6">
        <RecruitingWindowFinder />
      </main>
      <SiteFooter />
    </div>
  );
}
