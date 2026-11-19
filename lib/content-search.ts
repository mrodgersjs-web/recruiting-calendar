import fs from "node:fs";
import path from "node:path";
import type { ApprovedPage, ReelDraftId } from "@/lib/copilotkit-types";

export const APPROVED_WEB_HOSTS = [
  "ncaa.org",
  "www.ncaa.org",
  "naia.org",
  "www.naia.org",
  "njcaa.org",
  "www.njcaa.org",
  "recruiting-calendar.vercel.app",
] as const;

const SITE_ORIGIN_DEFAULT = "https://recruiting-calendar.vercel.app";

export interface ReelDraftSource {
  id: ReelDraftId;
  fileName: string;
  title: string;
  keywords: string[];
}

/** Five internal review drafts. File names stay server-side and are not citations. */
export const REEL_DRAFT_SOURCES: readonly ReelDraftSource[] = [
  {
    id: "basketball",
    fileName: "Commit-Book-Basketball-Highlight-Reel-Research-Report_v1.txt",
    title: "Basketball highlight-reel research",
    keywords: ["basketball", "aau", "point guard", "layup", "free throw"],
  },
  {
    id: "fastpitch-softball",
    fileName: "Commit-Book-Fastpitch-Softball-Highlight-Reel-Research-Report_v1.txt",
    title: "Fastpitch softball highlight-reel research",
    keywords: ["softball", "fastpitch", "circle", "pitching", "43-foot"],
  },
  {
    id: "football",
    fileName: "Commit-Book-Highlight-Reel-Playbook_Football_Review_v3.txt",
    title: "Football highlight-reel research",
    keywords: ["football", "quarterback", "linebacker", "all-22", "lineman"],
  },
  {
    id: "volleyball",
    fileName: "Commit-Book-Highlight-Reel-Playbook_Volleyball_Review_v3.txt",
    title: "Volleyball highlight-reel research",
    keywords: ["volleyball", "setter", "libero", "hitter", "rally"],
  },
  {
    id: "baseball",
    fileName: "Commit-Book-Mens-Baseball-Highlight-Reel-Research-Report_v1.txt",
    title: "Baseball highlight-reel research",
    keywords: ["baseball", "pitcher", "radar", "bullpen", "infield"],
  },
];

const RECRUITING_TERMS = [
  "recruit",
  "ncaa",
  "naia",
  "njcaa",
  "scholarship",
  "eligibility",
  "roster",
  "commit",
  "athlete",
  "coach",
  "camp",
  "showcase",
  "highlight",
  "reel",
  "film",
  "hudl",
  "gpa",
  "core course",
  "division",
  "walk-on",
  "walk on",
  "financial aid",
  "contact period",
  "dead period",
  "quiet period",
  "signing",
  "playbook",
  "sop",
  "football",
  "basketball",
  "volleyball",
  "baseball",
  "softball",
  "fastpitch",
  "soccer",
  "track",
  "lacrosse",
  "window",
  "transcript",
  "nil",
];

const FILM_TERMS = [
  "film",
  "reel",
  "highlight",
  "video",
  "camera",
  "clip",
  "footage",
  "hudl",
  "editing",
  "tripod",
  "angle",
  "montage",
];

const BLOCK_TERMS = [
  "ignore previous",
  "ignore all previous",
  "system prompt",
  "developer message",
  "api key",
  "jailbreak",
  "do anything now",
  "write code",
  "crypto",
  "recipe",
  "politics",
  "betting",
  "homework",
  "verbatim",
  "paste the entire",
  "paste the full",
  "paste the whole",
  "dump the draft",
  "unpublished file",
  "print the draft",
  "reveal the research",
];

export function assertServerOnly(feature: string): void {
  if (typeof window !== "undefined") {
    throw new Error(`${feature} is server-only and is not published.`);
  }
}

export function tokenize(query: string): string[] {
  return query
    .toLowerCase()
    .replace(/[^a-z0-9$./ -]/g, " ")
    .split(/[^a-z0-9$./]+/)
    .map((token) => token.trim())
    .filter((token) => token.length > 2)
    .slice(0, 60);
}

export function scoreText(text: string, tokens: string[]): number {
  if (tokens.length === 0 || text.length === 0) return 0;
  const lower = text.toLowerCase();
  let score = 0;
  for (const token of tokens) {
    if (lower.includes(token)) score += token.length > 4 ? 2 : 1;
  }
  return score;
}

export function chunkText(text: string, maxChars: number): string[] {
  const clean = text.replace(/\r/g, "").trim();
  if (!clean) return [];
  const pages = clean.split(/===\s*PAGE\s+\d+\s*===/i).map((part) => part.trim());
  const source = pages.length > 1 ? pages.filter((part) => part.length > 40) : [clean];
  const chunks: string[] = [];
  for (const page of source) {
    if (page.length <= maxChars) {
      chunks.push(page);
      continue;
    }
    let start = 0;
    while (start < page.length) {
      const end = Math.min(page.length, start + maxChars);
      const slice = page.slice(start, end).trim();
      if (slice.length > 40) chunks.push(slice);
      if (end >= page.length) break;
      start = end - 120;
    }
  }
  return chunks;
}

export function htmlToText(html: string): string {
  return html
    .replace(/<script[\s\S]*?<\/script>/gi, " ")
    .replace(/<style[\s\S]*?<\/style>/gi, " ")
    .replace(/<noscript[\s\S]*?<\/noscript>/gi, " ")
    .replace(/<[^>]+>/g, " ")
    .replace(/&nbsp;/gi, " ")
    .replace(/&amp;/gi, "&")
    .replace(/&lt;/gi, "<")
    .replace(/&gt;/gi, ">")
    .replace(/&quot;/gi, '"')
    .replace(/&#39;|&apos;/gi, "'")
    .replace(/\s+/g, " ")
    .trim();
}

export function siteOrigin(): string {
  const fromEnv = process.env.COMMIT_BOOK_SITE_ORIGIN?.trim();
  return (fromEnv || SITE_ORIGIN_DEFAULT).replace(/\/$/, "");
}

export function approvedHosts(extraOrigin?: string): Set<string> {
  const hosts = new Set<string>(APPROVED_WEB_HOSTS);
  const origin = extraOrigin ?? siteOrigin();
  try {
    hosts.add(new URL(origin).hostname.toLowerCase());
  } catch {
    hosts.add("recruiting-calendar.vercel.app");
  }
  return hosts;
}

/** Accept only https URLs on the approved host list. Rejects user-supplied hosts. */
export function approvedUrl(raw: string, hosts: Set<string>): URL | null {
  let parsed: URL;
  try {
    parsed = new URL(raw);
  } catch {
    return null;
  }
  if (parsed.protocol !== "https:") return null;
  if (parsed.username || parsed.password) return null;
  if (!hosts.has(parsed.hostname.toLowerCase())) return null;
  return parsed;
}

export function approvedPageCatalog(origin = siteOrigin()): ApprovedPage[] {
  const site = origin.replace(/\/$/, "");
  const sitePages: ApprovedPage[] = [
    { url: `${site}/`, title: "Commit Book home", keywords: ["commit book", "home", "start", "recruiting"] },
    { url: `${site}/window`, title: "Recruiting window", keywords: ["window", "contact", "date", "when", "period"] },
    { url: `${site}/sops`, title: "Athlete SOP playbooks", keywords: ["sop", "playbook", "grade", "checklist"] },
    { url: `${site}/calendar`, title: "Recruiting calendar", keywords: ["calendar", "dead", "quiet", "evaluation"] },
    { url: `${site}/auditor`, title: "Camp and aid auditor", keywords: ["camp", "showcase", "aid", "red flag"] },
    { url: `${site}/offers`, title: "Family recruiting offers", keywords: ["offer", "waitlist", "tool"] },
    { url: `${site}/price`, title: "Commit Book pricing", keywords: ["price", "pricing", "refund", "pass"] },
    { url: `${site}/playbooks`, title: "Sport playbooks", keywords: ["playbook", "sport", "road"] },
    { url: `${site}/sports`, title: "Browse by sport", keywords: ["sport", "film", "football", "basketball"] },
    { url: `${site}/start`, title: "Free class-year plan", keywords: ["plan", "class", "free", "start"] },
  ];
  const associationPages: ApprovedPage[] = [
    { url: "https://www.ncaa.org/", title: "NCAA", keywords: ["ncaa", "division", "eligibility", "recruiting"] },
    { url: "https://www.ncaa.org/sports/2015/2/13/recruiting.aspx", title: "NCAA recruiting", keywords: ["ncaa", "recruiting", "contact", "coach"] },
    { url: "https://www.naia.org/", title: "NAIA", keywords: ["naia", "eligibility", "scholarship"] },
    { url: "https://www.naia.org/eligibility/index", title: "NAIA eligibility", keywords: ["naia", "eligibility", "gpa"] },
    { url: "https://www.njcaa.org/", title: "NJCAA", keywords: ["njcaa", "juco", "junior college"] },
    { url: "https://www.njcaa.org/eligibility/index", title: "NJCAA eligibility", keywords: ["njcaa", "eligibility", "juco"] },
  ];
  return [...sitePages, ...associationPages];
}

export function selectApprovedPages(query: string, origin = siteOrigin(), limit = 3): ApprovedPage[] {
  const tokens = tokenize(query);
  const ranked = approvedPageCatalog(origin)
    .map((page) => {
      const hay = `${page.title} ${page.keywords.join(" ")} ${page.url}`;
      return { page, score: scoreText(hay, tokens) };
    })
    .filter((row) => row.score > 0)
    .sort((a, b) => b.score - a.score);
  return ranked.slice(0, limit).map((row) => row.page);
}

const reelChunkCache = new Map<string, { id: string; title: string; text: string }[]>();

export function loadReelChunks(reelDirectory?: string): { id: string; title: string; text: string }[] {
  assertServerOnly("Highlight-reel review drafts");
  const dir = reelDirectory ?? path.join(process.cwd(), "content", "reels");
  const cached = reelChunkCache.get(dir);
  if (cached) return cached;
  const chunks: { id: string; title: string; text: string }[] = [];
  for (const source of REEL_DRAFT_SOURCES) {
    const full = path.join(dir, source.fileName);
    if (!fs.existsSync(full)) continue;
    const raw = fs.readFileSync(full, "utf8");
    const parts = chunkText(raw, 1400);
    parts.forEach((text, index) => {
      chunks.push({
        id: `${source.id}:${index + 1}`,
        title: source.title,
        text: `${source.title}\n${source.keywords.join(", ")}\n${text}`,
      });
    });
  }
  reelChunkCache.set(dir, chunks);
  return chunks;
}

export function queryLooksRecruiting(query: string): boolean {
  const lower = query.toLowerCase();
  if (RECRUITING_TERMS.some((term) => lower.includes(term))) return true;
  if (lower.trim().length > 0 && lower.trim().length < 24 && /^(hi|hello|hey|help)\b/.test(lower.trim())) {
    return true;
  }
  return false;
}

export function queryLooksLikeFilm(query: string): boolean {
  const lower = query.toLowerCase();
  return FILM_TERMS.some((term) => lower.includes(term));
}

export function queryIsBlocked(query: string): boolean {
  const lower = query.toLowerCase();
  return BLOCK_TERMS.some((term) => lower.includes(term));
}

export function draftQueryMatches(query: string, title: string, keywords: string[]): boolean {
  const tokens = tokenize(query);
  return scoreText(`${title} ${keywords.join(" ")}`, tokens) > 0 || queryLooksLikeFilm(query);
}
