export type SolutionSlug =
  | "next-30-days"
  | "camp-decision-receipt"
  | "film-outreach-brief"
  | "family-recruiting-receipt"
  | "offer-aid-comparison"
  | "program-fit-check";

export type SourceLink = { label: string; href: string };

export type SolutionDefinition = {
  slug: SolutionSlug;
  title: string;
  eyebrow: string;
  summary: string;
  outcome: string;
  mechanism: string;
  primaryAction: string;
  sourceLinks: SourceLink[];
};

export const SPORTS = [
  "Baseball",
  "Basketball",
  "Football",
  "Lacrosse",
  "Soccer",
  "Softball",
  "Swimming",
  "Track & Field",
  "Volleyball",
  "Wrestling",
  "Other",
] as const;

export const CLASS_YEARS = ["2027", "2028", "2029", "2030", "2031"] as const;
export const LEVELS = ["Undecided", "NCAA D1", "NCAA D2", "NCAA D3", "NAIA", "NJCAA"] as const;
