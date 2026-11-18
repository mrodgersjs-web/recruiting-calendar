import Link from "next/link";
import LegacyPageScripts from "@/components/layout/legacy-page-scripts";
import AthleteSopHub from "@/components/upgrade/athlete-sop-hub";
import RecruitingWindowFinder from "@/components/upgrade/recruiting-window-finder";
import TenOffersLab from "@/components/upgrade/ten-offers-lab";
import {
  loadAllAthleteSops,
  loadOffersCatalog,
  parseLegacyHtmlFile,
} from "@/lib/site-data";

export default function HomePage() {
  const legacyHome = parseLegacyHtmlFile("index.html");
  const sops = loadAllAthleteSops();
  const offersCatalog = loadOffersCatalog();

  if (!legacyHome) {
    return (
      <main className="mx-auto max-w-5xl px-6 py-16">
        <h1 className="font-serif text-4xl font-semibold">The Commit Book</h1>
      </main>
    );
  }

  // Split legacy home before <footer class="cb-foot"> so our 1000x interactive command deck sits right above the footer
  const footerIdx = legacyHome.bodyHtmlWithoutScripts.indexOf('<footer class="cb-foot"');
  const beforeFooter =
    footerIdx !== -1
      ? legacyHome.bodyHtmlWithoutScripts.slice(0, footerIdx)
      : legacyHome.bodyHtmlWithoutScripts;
  const footerAndAfter =
    footerIdx !== -1 ? legacyHome.bodyHtmlWithoutScripts.slice(footerIdx) : "";

  return (
    <>
      <link
        as="image"
        href="/assets/media/hero-football-1080.webp"
        rel="preload"
        type="image/webp"
      />
      {legacyHome.extraStylesheets.map((href) => (
        <link href={href} key={href} rel="stylesheet" />
      ))}

      <div dangerouslySetInnerHTML={{ __html: beforeFooter }} />

      {/* Below-the-fold 1000x Interactive Athlete Command Deck (content-visibility: auto preserves LCP/TBT) */}
      <section
        aria-label="Interactive Recruiting Workstations"
        className="cb-below-fold border-[#e5e0d6] border-t bg-[#f7f5f0] py-16"
      >
        <div className="mx-auto max-w-7xl space-y-16 px-4 sm:px-6">
          {/* 1. 30-Second Recruiting Window & Roster Cap Calculator */}
          <div className="space-y-4">
            <div className="flex flex-wrap items-end justify-between gap-4">
              <div>
                <p className="font-mono text-[11px] font-semibold uppercase tracking-widest text-[#1d4ed8]">
                  Interactive Rulebook Tool · 01
                </p>
                <h2 className="mt-1 font-serif text-3xl font-semibold text-[#141413]">
                  Check your athlete&apos;s legal contact window in 30 seconds.
                </h2>
              </div>
              <Link
                className="font-mono text-xs font-semibold text-[#1d4ed8] hover:underline"
                href="/window"
              >
                Open full-screen calculator →
              </Link>
            </div>
            <RecruitingWindowFinder compact />
          </div>

          {/* 2. James's Official Athlete SOP Playbooks */}
          <div className="space-y-4">
            <div className="flex flex-wrap items-end justify-between gap-4">
              <div>
                <p className="font-mono text-[11px] font-semibold uppercase tracking-widest text-[#1d4ed8]">
                  Official Grade 9-12 Field Manuals · 02
                </p>
                <h2 className="mt-1 font-serif text-3xl font-semibold text-[#141413]">
                  Step-by-step Athlete SOP Playbooks by sport.
                </h2>
                <p className="mt-1 max-w-2xl text-sm text-[#57534e]">
                  Verified against 2026-27 NCAA D1/D2/D3, NAIA, and NJCAA manuals: roster caps, highlight tape specs, camp waste filters, and checkable grade-by-grade milestones.
                </p>
              </div>
              <Link
                className="rounded-full bg-[#141413] px-4 py-2 font-mono text-xs font-semibold text-[#f7f5f0] hover:bg-[#1d4ed8]"
                href="/sops"
              >
                Open Full SOP Workstation →
              </Link>
            </div>
            <AthleteSopHub previewMode sops={sops} />
          </div>

          {/* 3. Camp & Aid Reality Banner */}
          <div className="rounded-2xl border border-[#e5e0d6] bg-[#ffffff] p-6 sm:p-8 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div className="max-w-2xl space-y-1.5">
              <p className="font-mono text-[11px] font-semibold uppercase tracking-widest text-[#b91c1c]">
                Before You Spend $600 on a Weekend Showcase · 03
              </p>
              <h3 className="font-serif text-2xl font-semibold text-[#141413]">
                Run the 5-Point Camp Invite Red-Flag Test and 4-Year Aid Estimator.
              </h3>
              <p className="text-sm text-[#57534e]">
                Score any camp invite before booking flights, and compare realistic 4-year out-of-pocket net price across D1, D2, D3 academic merit, NAIA, and NJCAA.
              </p>
            </div>
            <Link
              className="shrink-0 rounded-xl border border-[#141413] bg-[#f7f5f0] px-5 py-3 text-center font-mono text-xs font-semibold text-[#141413] hover:bg-[#141413] hover:text-[#f7f5f0] transition-colors"
              href="/auditor"
            >
              Run Camp &amp; Aid Test →
            </Link>
          </div>

          {/* 4. 10 New Recruiting Offerings Lab (Social Fetch Demand-Backed) */}
          <div className="space-y-4">
            <div className="flex flex-wrap items-end justify-between gap-4">
              <div>
                <p className="font-mono text-[11px] font-semibold uppercase tracking-widest text-[#1d4ed8]">
                  Next-Gen Family Stack ({offersCatalog.socialSignalsCount} Social Signals Analyzed) · 04
                </p>
                <h2 className="mt-1 font-serif text-3xl font-semibold text-[#141413]">
                  10 focused recruiting tools we are building next.
                </h2>
              </div>
              <Link
                className="font-mono text-xs font-semibold text-[#1d4ed8] hover:underline"
                href="/offers"
              >
                Explore all 10 offerings &amp; demand evidence →
              </Link>
            </div>
            <TenOffersLab catalog={offersCatalog} previewMode />
          </div>
        </div>
      </section>

      {footerAndAfter && (
        <div dangerouslySetInnerHTML={{ __html: footerAndAfter }} />
      )}

      <LegacyPageScripts
        dataPage={legacyHome.dataPage}
        externalScripts={legacyHome.externalScripts}
        inlineScripts={legacyHome.inlineScripts}
      />
    </>
  );
}
