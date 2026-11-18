import type { Metadata } from "next";
import { SiteFooter, SiteHeader } from "@/components/layout/site-chrome";
import CampAndAidAuditor from "@/components/upgrade/camp-and-aid-auditor";

export const metadata: Metadata = {
  title: "Camp Invite Red-Flag Test & 4-Year Aid Estimator | The Commit Book",
  description:
    "Evaluate any camp or showcase invite in 60 seconds and compare realistic 4-year out-of-pocket costs across NCAA D1, D2, D3, NAIA, and NJCAA.",
};

export default function AuditorPage() {
  return (
    <div className="flex min-h-screen flex-col bg-[#f7f5f0]">
      <SiteHeader activePath="/auditor" />
      <main className="mx-auto w-full max-w-7xl flex-1 px-4 py-10 sm:px-6">
        <CampAndAidAuditor />
      </main>
      <SiteFooter />
    </div>
  );
}
