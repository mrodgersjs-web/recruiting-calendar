import type { SolutionDefinition, SolutionSlug } from "./types";

export const SOLUTIONS: SolutionDefinition[] = [
  {
    slug: "next-30-days",
    title: "Your Next 30 Days",
    eyebrow: "Athlete-owned action plan",
    summary: "Turn sport, class year, and the current concern into three clear actions and one parent check-in.",
    outcome: "Leave with a short plan and exact site tools for the dated rules.",
    mechanism: "Public-good guidance",
    primaryAction: "Build my plan",
    sourceLinks: [
      { label: "Window Finder", href: "/window" },
      { label: "Athlete SOPs", href: "/sops" },
      { label: "Free class-year plan", href: "/start" },
    ],
  },
  {
    slug: "camp-decision-receipt",
    title: "Camp Decision Receipt",
    eyebrow: "Pay, skip, or get more information",
    summary: "Compare the full cost and actual evaluation opportunity against what is still unknown.",
    outcome: "Save a transparent decision receipt without a dollar-value promise.",
    mechanism: "Counterfactual comparison",
    primaryAction: "Evaluate this camp",
    sourceLinks: [{ label: "Camp & Aid Auditor", href: "/auditor" }],
  },
  {
    slug: "film-outreach-brief",
    title: "Film + Outreach Brief",
    eyebrow: "One athlete, one clear message",
    summary: "Build a concise coach email with the sport, class year, position, film, and full-game fallback.",
    outcome: "Copy a practical message and check both links before sending.",
    mechanism: "Verified proof packet",
    primaryAction: "Create my brief",
    sourceLinks: [
      { label: "Athlete SOPs", href: "/sops" },
      { label: "Playbooks", href: "/playbooks" },
    ],
  },
  {
    slug: "family-recruiting-receipt",
    title: "Family Recruiting Receipt",
    eyebrow: "A portable record of the work",
    summary: "Save completed actions, the next family-entered date, and source links in one athlete-owned receipt.",
    outcome: "Keep the plan on this device, print it, or export JSON.",
    mechanism: "Portable receipt",
    primaryAction: "Save receipt",
    sourceLinks: [
      { label: "Window Finder", href: "/window" },
      { label: "Athlete SOPs", href: "/sops" },
    ],
  },
  {
    slug: "offer-aid-comparison",
    title: "Offer + Aid Comparison",
    eyebrow: "Compare the actual terms",
    summary: "Put up to four programs side by side without turning verbal interest or projected dates into certainties.",
    outcome: "See user-entered annual net cost, offer status, and signing-date status together.",
    mechanism: "Independent verification",
    primaryAction: "Compare programs",
    sourceLinks: [
      { label: "Offers & Signing playbook", href: "/playbooks/offer-and-signing" },
      { label: "Camp & Aid Auditor", href: "/auditor" },
    ],
  },
  {
    slug: "program-fit-check",
    title: "Program Fit Red-Flag Check",
    eyebrow: "Evidence before a college decision",
    summary: "Record what is known about roster retention, coaching, academics, development, and transfers.",
    outcome: "Leave with red flags, unknowns, and questions to ask, not a school recommendation.",
    mechanism: "Anti-adversarial review",
    primaryAction: "Review the evidence",
    sourceLinks: [
      { label: "Athlete SOPs", href: "/sops" },
      { label: "Offers & Signing playbook", href: "/playbooks/offer-and-signing" },
    ],
  },
];

export const SOLUTION_MAP = Object.fromEntries(
  SOLUTIONS.map((solution) => [solution.slug, solution]),
) as Record<SolutionSlug, SolutionDefinition>;

export function isSolutionSlug(value: string): value is SolutionSlug {
  return Object.hasOwn(SOLUTION_MAP, value);
}
