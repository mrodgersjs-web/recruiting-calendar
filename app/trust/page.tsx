import type { Metadata } from "next";
import Link from "next/link";
import { SiteFooter, SiteHeader } from "@/components/layout/site-chrome";

export const metadata: Metadata = {
  title: "Source-First Trust Center | The Commit Book",
  description:
    "Every Commit Book date and rule cites its bylaw and the day it was checked. See the sources, the verification stamps, and what is still in review.",
};

const PILLARS = [
  {
    title: "Every date cites its bylaw",
    body: "Each recruiting date on the site carries the NCAA, NAIA, or NJCAA bylaw it comes from, plus the day we checked it. If a rule changes, the page changes and the stamp moves.",
  },
  {
    title: "Conflicts stay visible",
    body: "When two official sources disagree, we print both numbers and say so. We never average two sources into a cleaner-looking answer.",
  },
  {
    title: "Drafts are labeled as drafts",
    body: "Playbooks still in review are marked as review drafts with no price set. They never appear as published products, and checkout stays off until they ship.",
  },
  {
    title: "No outcome promises",
    body: "Nothing here promises a scholarship, an offer, a roster spot, or a coach reply. Education, not legal advice. We do not recruit or place athletes.",
  },
];

const SOURCES = [
  { label: "NCAA Division I, II, III manuals", note: "Recruiting calendars, contact rules, eligibility bylaws", href: "https://www.ncaa.org/sports/2021/2/8/about-resources-media-center-publications.aspx" },
  { label: "NCAA Eligibility Center", note: "Core-course and certification rules", href: "https://web3.ncaa.org/ecwr3/" },
  { label: "NAIA eligibility", note: "NAIA eligibility center rules", href: "https://www.naia.org/eligibility-center/index" },
  { label: "NJCAA eligibility", note: "Junior college eligibility rules", href: "https://www.njcaa.org/eligibility" },
  { label: "NFHS rules", note: "High school playing and filming rules", href: "https://www.nfhs.org/" },
];

export default function TrustCenterPage() {
  return (
    <div className="flex min-h-screen flex-col bg-[#f7f5f0]">
      <SiteHeader activePath="/trust" />
      <main className="mx-auto w-full max-w-5xl flex-1 px-4 py-10 sm:px-6">
        <p className="font-mono text-[10px] font-semibold uppercase tracking-[0.12em] text-[#1d4ed8]">Source-First Trust Center</p>
        <h1 className="mt-3 font-serif text-4xl font-semibold tracking-tight sm:text-5xl">Where every answer comes from.</h1>
        <p className="mt-4 max-w-3xl text-[16px] leading-relaxed text-[#57534e]">
          The Commit Book and Scout answer from a verified knowledge base built on the sources below. This page shows the standard every page is held to.
        </p>

        <div className="mt-10 grid gap-4 md:grid-cols-2">
          {PILLARS.map((pillar) => (
            <div key={pillar.title} className="rounded-2xl border border-[#d9d3c8] bg-white p-6">
              <h2 className="font-serif text-xl font-semibold tracking-tight">{pillar.title}</h2>
              <p className="mt-3 text-[13px] leading-relaxed text-[#57534e]">{pillar.body}</p>
            </div>
          ))}
        </div>

        <h2 className="mt-12 font-serif text-2xl font-semibold tracking-tight">Primary sources</h2>
        <div className="mt-4 divide-y divide-[#e5e0d6] rounded-2xl border border-[#d9d3c8] bg-white">
          {SOURCES.map((source) => (
            <a
              key={source.label}
              className="flex flex-col gap-1 p-4 transition hover:bg-[#f7f5f0] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#1d4ed8]"
              href={source.href}
              rel="noreferrer"
              target="_blank"
            >
              <span className="text-[14px] font-semibold text-[#141413]">{source.label}</span>
              <span className="text-[12px] text-[#57534e]">{source.note}</span>
            </a>
          ))}
        </div>

        <p className="mt-8 rounded-xl border border-[#d9d3c8] bg-white p-4 text-[12px] leading-relaxed text-[#57534e]">
          Something looks wrong on a page? Tell us through <Link className="font-semibold text-[#1d4ed8]" href="/about">the contact page</Link> and include the bylaw you are looking at. Corrections ship with a new checked-on stamp.
        </p>
      </main>
      <SiteFooter />
    </div>
  );
}
