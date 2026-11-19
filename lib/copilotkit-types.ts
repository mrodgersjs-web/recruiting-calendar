/**
 * Shared types for the Commit Book CopilotKit retrieval service.
 * Reel drafts are internal review material. They are never a public source.
 */

export const INTERNAL_DRAFT_CITATION = "internal research draft, not published" as const;

export type RetrievalSource = "site-kb" | "reel-draft" | "approved-web";

export type ReelDraftId =
  | "basketball"
  | "fastpitch-softball"
  | "football"
  | "volleyball"
  | "baseball";

export interface ScopeDecision {
  inScope: boolean;
  /** True when the question is about film, reels, or a sport that has a review draft. */
  includeInternalDrafts: boolean;
  /** Jailbreak, prompt extraction, or a request to paste an unpublished draft. */
  blocked: boolean;
  reason: string;
}

export interface SearchHit {
  id: string;
  source: RetrievalSource;
  title: string;
  /** Exact citation the model must use. Reel hits always use INTERNAL_DRAFT_CITATION. */
  citation: string;
  text: string;
  score: number;
  /** Public URL only for approved-web hits. Reel hits never carry a URL or file path. */
  url?: string;
}

export interface SearchResult {
  source: RetrievalSource;
  query: string;
  hits: SearchHit[];
  /** Non-fatal fetch or match notes. Never includes draft file paths. */
  warnings: string[];
}

export interface ComposedContext {
  query: string;
  scope: ScopeDecision;
  siteKb: SearchResult;
  reelDrafts: SearchResult;
  approvedWeb: SearchResult;
  /** Server-only prompt block. Empty when the query is out of scope. */
  promptBlock: string;
  citations: string[];
}

export interface AnswerTurn {
  role: "user" | "assistant";
  content: string;
}

export interface CommitBookAnswerPlan {
  system: string;
  turns: AnswerTurn[];
  /** Set when the model must not be called. Stream this text as the whole answer. */
  directText: string | null;
}

export interface ApprovedPage {
  url: string;
  title: string;
  keywords: string[];
}

export interface CommitBookAgentServiceOptions {
  /** Override for tests. Defaults to content/reels under process.cwd(). */
  reelDirectory?: string;
  fetchImpl?: typeof fetch;
  /** Public origin for this site's own pages. Defaults to the Vercel host. */
  siteOrigin?: string;
  kbLoader?: (query: string) => string;
}
