"use client";

import { useChat } from "@ai-sdk/react";
import { DefaultChatTransport, type UIMessage } from "ai";
import {
  Accordion,
  AccordionHeader,
  AccordionItem,
  AccordionPanel,
  AccordionTrigger,
} from "@ui-sdk/react/accordion";
import {
  AlertTriangle,
  ArrowRight,
  BookOpen,
  Calculator,
  Clock,
  Compass,
  FileCheck2,
  RotateCcw,
  ShieldCheck,
  X,
} from "lucide-react";
import Link from "next/link";
import React, { useCallback, useEffect, useMemo, useRef, useState } from "react";
import AI_Prompt, { type PromptCommand } from "@/components/kokonutui/ai-prompt";
import AITextLoading from "@/components/kokonutui/ai-text-loading";

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-[#1d4ed8] focus-visible:outline-offset-2";

export const STARTER_PROMPTS = [
  {
    id: "sp-1",
    tag: "CONTACT DATES",
    shortLabel: "Contact dates",
    question:
      "When can D1 vs D3 college coaches first contact a Class of 2029 football or volleyball athlete?",
  },
  {
    id: "sp-2",
    tag: "ATHLETE SOPs",
    shortLabel: "Athlete SOPs",
    question:
      "What belongs in the first 30 seconds of a recruiting highlight video, and what gets turned off immediately?",
  },
  {
    id: "sp-3",
    tag: "CAMP RED FLAGS",
    shortLabel: "Camp red flags",
    question:
      "How do we tell if a $600 showcase camp invite is worth attending or a money trap?",
  },
  {
    id: "sp-4",
    tag: "HIGHLIGHT FILM",
    shortLabel: "Highlight film",
    question:
      "What camera angle and reel length should we use for a football, basketball, baseball, softball, or volleyball recruiting reel?",
  },
] as const;

const SLASH_COMMANDS: PromptCommand[] = [
  {
    id: "window",
    label: "window",
    description: "Check coach contact dates for my sport & grad year",
  },
  {
    id: "football",
    label: "football",
    description: "Summarize the Men's Football SOP & 105-man roster cap",
  },
  {
    id: "volleyball",
    label: "volleyball",
    description: "Summarize the Women's Volleyball SOP & June 15 window",
  },
  {
    id: "basketball",
    label: "basketball",
    description: "Summarize Basketball live periods, film & roster rules",
  },
  {
    id: "camps",
    label: "camps",
    description: "Run the 5-point camp & showcase red-flag check",
  },
  {
    id: "film",
    label: "film",
    description: "Highlight reel rules: camera, length, clips, second link",
  },
];

interface RateLimitState {
  retryAfterSec: number;
  message: string;
}

function getMessageText(message: UIMessage): string {
  if (!Array.isArray(message.parts)) return "";
  return message.parts
    .filter((p): p is { type: "text"; text: string } => p.type === "text")
    .map((p) => p.text)
    .join("");
}

function renderFormattedLine(line: string, lineKey: string): React.ReactNode[] {
  // Parse markdown links [Label](/path) and **bold** spans safely without dangerouslySetInnerHTML
  const tokens: React.ReactNode[] = [];
  const pattern = /(\[([^\]]+)\]\(([^)]+)\)|\*\*([^*]+)\*\*)/g;
  let lastIdx = 0;
  let match: RegExpExecArray | null = pattern.exec(line);
  let idx = 0;

  while (match !== null) {
    if (match.index > lastIdx) {
      tokens.push(line.slice(lastIdx, match.index));
    }
    if (match[2] && match[3]) {
      const label = match[2];
      const href = match[3];
      const isInternal = href.startsWith("/");
      if (isInternal) {
        tokens.push(
          <Link
            className="inline-flex items-center gap-1 rounded border border-[#1d4ed8]/25 bg-[#1d4ed8]/[0.07] px-2 py-0.5 font-medium text-[#1d4ed8] text-xs underline-offset-2 transition-colors hover:bg-[#1d4ed8]/[0.14]"
            href={href}
            key={`${lineKey}-lnk-${idx}`}
          >
            <span>{label}</span>
            <ArrowRight aria-hidden="true" className="size-3" />
          </Link>
        );
      } else {
        tokens.push(
          <a
            className="font-medium text-[#1d4ed8] underline underline-offset-2"
            href={href}
            key={`${lineKey}-ext-${idx}`}
            rel="noopener noreferrer"
            target="_blank"
          >
            {label}
          </a>
        );
      }
    } else if (match[4]) {
      tokens.push(
        <strong className="font-semibold text-[#141413]" key={`${lineKey}-b-${idx}`}>
          {match[4]}
        </strong>
      );
    }
    lastIdx = match.index + match[0].length;
    idx += 1;
    match = pattern.exec(line);
  }

  if (lastIdx < line.length) {
    tokens.push(line.slice(lastIdx));
  }
  return tokens;
}

type GuideSource = { id: string; title: string; href: string };

type PlaybookRecommendation = {
  id: string;
  title: string;
  price: number;
  description: string;
};

const PLAYBOOKS: Record<string, PlaybookRecommendation> = {
  "football-junior-year": {
    id: "football-junior-year",
    title: "Football: Junior Year Playbook",
    price: 29,
    description: "A dated plan for contact windows, coach outreach, visits, and signing.",
  },
  "eligibility-2-hard-deadlines": {
    id: "eligibility-2-hard-deadlines",
    title: "Eligibility: the 2 Hard Deadlines",
    price: 9,
    description: "The core-course checkpoints, counselor script, and eligibility checklist.",
  },
  "camp-roi": {
    id: "camp-roi",
    title: "Camp ROI Playbook",
    price: 15,
    description: "Score a camp before paying, track the cost, and plan the follow-up.",
  },
  "highlight-reel-social": {
    id: "highlight-reel-social",
    title: "Highlight Reel & Social Playbook",
    price: 15,
    description: "A practical reel brief, athlete profile template, and follow-up log.",
  },
  "offer-and-signing": {
    id: "offer-and-signing",
    title: "Offers & Signing Day",
    price: 19,
    description: "Compare offers on the same terms and know what is binding and when.",
  },
  "walk-on": {
    id: "walk-on",
    title: "Walk-On Playbook",
    price: 15,
    description: "Understand walk-on types and the questions to ask before committing.",
  },
  "juco-to-d1": {
    id: "juco-to-d1",
    title: "JUCO to D1",
    price: 19,
    description: "Plan transferable credits and the two-year recruiting window.",
  },
  "late-bloomer": {
    id: "late-bloomer",
    title: "Late Bloomer Playbook",
    price: 15,
    description: "A 90-day plan for a late start, late growth, or late film.",
  },
  "d3-academic-aid-first": {
    id: "d3-academic-aid-first",
    title: "D3 Path: Academic Aid First",
    price: 19,
    description: "Compare D3 net cost, academic aid, admissions, and coach support.",
  },
};

function recommendPlaybook(prompt: string): PlaybookRecommendation | null {
  const text = prompt.toLowerCase();
  const pick = (id: string) => PLAYBOOKS[id] ?? null;
  if (/camp|showcase/.test(text)) return pick("camp-roi");
  if (/highlight|film|reel|video|camera/.test(text)) return pick("highlight-reel-social");
  if (/offer|signing|commit|verbal/.test(text)) return pick("offer-and-signing");
  if (/walk.?on/.test(text)) return pick("walk-on");
  if (/juco|junior college|njcaa/.test(text)) return pick("juco-to-d1");
  if (/too late|late start|senior year|post.?grad/.test(text)) return pick("late-bloomer");
  if (/d3|division iii|division 3/.test(text) && /aid|cost|academic|afford/.test(text)) {
    return pick("d3-academic-aid-first");
  }
  if (/eligib|core course|gpa|grades|transcript/.test(text)) {
    return pick("eligibility-2-hard-deadlines");
  }
  if (/football/.test(text) && /junior|2029|contact|text|coach|window/.test(text)) {
    return pick("football-junior-year");
  }
  return null;
}

function PlaybookCard({ playbook }: { playbook: PlaybookRecommendation }) {
  return (
    <aside
      aria-label={`Recommended playbook: ${playbook.title}`}
      className="mt-2 w-full max-w-[94%] rounded-[18px] border border-[#e5e0d6] bg-white p-3.5 shadow-[0_1px_2px_rgba(20,20,19,0.04)]"
      data-testid="scout-playbook-recommendation"
    >
      <p className="mb-2 font-mono text-[10px] font-semibold uppercase tracking-[0.08em] text-[#57534e]">
        Recommended next step
      </p>
      <div className="flex items-center gap-3">
        <div className="min-w-0 flex-1">
          <Link
            className={`block text-[14px] font-semibold leading-snug text-[#141413] hover:underline ${FOCUS_RING}`}
            href={`/playbooks/${playbook.id}`}
          >
            {playbook.title}
          </Link>
          <p className="mt-1 text-[12px] leading-snug text-[#57534e]">
            ${playbook.price} one-time · {playbook.description}
          </p>
        </div>
        <Link
          aria-label={`Get ${playbook.title} for $${playbook.price}`}
          className={`inline-flex min-h-10 shrink-0 items-center justify-center rounded-full bg-[#1d4ed8] px-4 text-[13px] font-semibold text-white transition-colors hover:bg-[#1e40af] ${FOCUS_RING}`}
          href={`/playbooks/${playbook.id}`}
        >
          Get
        </Link>
      </div>
    </aside>
  );
}

function extractGuideSources(message: UIMessage): GuideSource[] {
  const sources: GuideSource[] = [];
  const seen = new Set<string>();
  const add = (title: string, href: string) => {
    const key = href.trim();
    if (!key || seen.has(key)) return;
    seen.add(key);
    sources.push({ id: key, title: title.trim() || key, href: key });
  };
  if (Array.isArray(message.parts)) {
    for (const part of message.parts) {
      if (part.type !== "source-url") continue;
      const url = "url" in part && typeof part.url === "string" ? part.url : "";
      const title =
        "title" in part && typeof part.title === "string" && part.title
          ? part.title
          : url;
      if (url) add(title, url);
    }
  }
  const pattern = /\[([^\]]+)\]\(([^)]+)\)/g;
  const text = getMessageText(message);
  let match: RegExpExecArray | null = pattern.exec(text);
  while (match !== null) {
    if (match[1] && match[2]) add(match[1], match[2]);
    match = pattern.exec(text);
  }
  return sources;
}

function GuideSources({ sources }: { sources: GuideSource[] }) {
  if (sources.length === 0) return null;
  const label = sources.length === 1 ? "1 source" : `${sources.length} sources`;
  return (
    <Accordion className="mt-2 border-[#141413]/10 border-t" multiple>
      <AccordionItem value="sources">
        <AccordionHeader>
          <AccordionTrigger
            className={`text-xs font-medium text-[#1d4ed8] ${FOCUS_RING}`}
          >
            {label}
          </AccordionTrigger>
        </AccordionHeader>
        <AccordionPanel>
          <ul className="space-y-1 py-1">
            {sources.map((source) => {
              const internal = source.href.startsWith("/");
              const className = `text-[13px] text-[#1d4ed8] underline underline-offset-2 ${FOCUS_RING}`;
              return (
                <li key={source.id}>
                  {internal ? (
                    <Link className={className} href={source.href}>
                      {source.title}
                    </Link>
                  ) : (
                    <a
                      className={className}
                      href={source.href}
                      rel="noopener noreferrer"
                      target="_blank"
                    >
                      {source.title}
                    </a>
                  )}
                </li>
              );
            })}
          </ul>
        </AccordionPanel>
      </AccordionItem>
    </Accordion>
  );
}

function FormattedAnswer({ text }: { text: string }) {
  const lines = text.split("\n");
  const blocks: React.ReactNode[] = [];
  let currentBullets: string[] = [];

  const flushBullets = (keyPrefix: string) => {
    if (currentBullets.length === 0) return;
    blocks.push(
      <ul className="my-2 space-y-1.5 pl-4 list-disc marker:text-[#1d4ed8]" key={keyPrefix}>
        {currentBullets.map((b, i) => (
          <li className="text-[14px] text-[#141413] leading-relaxed" key={`${keyPrefix}-${i}`}>
            {renderFormattedLine(b, `${keyPrefix}-li-${i}`)}
          </li>
        ))}
      </ul>
    );
    currentBullets = [];
  };

  lines.forEach((rawLine, idx) => {
    const trimmed = rawLine.trim();
    if (!trimmed) {
      flushBullets(`ul-${idx}`);
      return;
    }
    const bulletMatch = /^[-*]\s+(.*)$/.exec(trimmed) || /^\d+\.\s+(.*)$/.exec(trimmed);
    if (bulletMatch?.[1]) {
      currentBullets.push(bulletMatch[1]);
      return;
    }
    flushBullets(`ul-pre-${idx}`);
    if (trimmed.startsWith("### ") || trimmed.startsWith("## ")) {
      const heading = trimmed.replace(/^#{2,3}\s+/, "");
      blocks.push(
        <p
          className="mt-2.5 mb-1 font-semibold text-[#141413] text-[14px] tracking-tight"
          key={`h-${idx}`}
        >
          {heading}
        </p>
      );
      return;
    }
    blocks.push(
      <p className="my-1.5 text-[14px] text-[#141413] leading-relaxed" key={`p-${idx}`}>
        {renderFormattedLine(trimmed, `p-${idx}`)}
      </p>
    );
  });
  flushBullets("ul-final");

  return <div className="space-y-1">{blocks}</div>;
}

export interface CommitBookChatbotProps {
  open: boolean;
  onClose: () => void;
  initialPrompt?: string | null;
  onInitialPromptConsumed?: () => void;
}

export default function CommitBookChatbot({
  open,
  onClose,
  initialPrompt,
  onInitialPromptConsumed,
}: CommitBookChatbotProps) {
  const [rateLimited, setRateLimited] = useState<RateLimitState | null>(null);
  const [customError, setCustomError] = useState<string | null>(null);
  const [lastSubmittedPrompt, setLastSubmittedPrompt] = useState<string>("");
  const scrollContainerRef = useRef<HTMLDivElement | null>(null);

  const transport = useMemo(
    () =>
      new DefaultChatTransport({
        api: "/api/chat",
        fetch: async (input, init) => {
          const res = await globalThis.fetch(input, init);
          if (res.status === 429) {
            let retrySec = Number(res.headers.get("Retry-After") || "45");
            let msg =
              "You have reached the question limit for this minute. Please pause briefly or explore the Athlete SOP Playbooks directly.";
            try {
              const cloned = res.clone();
              const data = (await cloned.json()) as {
                retryAfterSec?: number;
                message?: string;
              };
              if (typeof data.retryAfterSec === "number") retrySec = data.retryAfterSec;
              if (data.message) msg = data.message;
            } catch {
              // keep header fallback
            }
            setRateLimited({
              retryAfterSec: Math.max(1, retrySec),
              message: msg,
            });
          } else if (!res.ok) {
            try {
              const cloned = res.clone();
              const data = (await cloned.json()) as { message?: string };
              if (data.message) setCustomError(data.message);
            } catch {
              setCustomError("Unable to reach Scout right now.");
            }
          } else {
            setRateLimited(null);
            setCustomError(null);
          }
          return res;
        },
      }),
    []
  );

  const { messages, sendMessage, status, stop, error, clearError } = useChat({
    transport,
  });

  const isStreaming = status === "submitted" || status === "streaming";

  // Countdown timer when rate-limited
  useEffect(() => {
    if (!rateLimited || rateLimited.retryAfterSec <= 0) return;
    const timer = window.setInterval(() => {
      setRateLimited((prev) => {
        if (!prev || prev.retryAfterSec <= 1) return null;
        return { ...prev, retryAfterSec: prev.retryAfterSec - 1 };
      });
    }, 1000);
    return () => window.clearInterval(timer);
  }, [rateLimited]);

  // Auto-scroll to latest message
  useEffect(() => {
    const el = scrollContainerRef.current;
    if (!el) return;
    el.scrollTop = el.scrollHeight;
  }, [messages, status, rateLimited, customError]);

  const handleSend = useCallback(
    async (rawText: string, command?: PromptCommand | null) => {
      const trimmed = rawText.trim();
      let finalPrompt = trimmed;
      if (command) {
        const prefixMap: Record<string, string> = {
          window: "Check coach contact window: ",
          football: "Using the Men's Football SOP playbook: ",
          volleyball: "Using the Women's Volleyball SOP playbook: ",
          basketball: "Using the Basketball SOP playbooks: ",
          camps: "Run the 5-point camp red-flag test on this: ",
          film: "Using the Commit Book highlight-reel research: ",
        };
        const prefix = prefixMap[command.id] ?? "";
        finalPrompt = trimmed
          ? `${prefix}${trimmed}`
          : `${prefix}Give me the key rules, dates, and next steps.`;
      }
      if (!finalPrompt) return;
      setCustomError(null);
      clearError();
      setLastSubmittedPrompt(finalPrompt);
      await sendMessage({ text: finalPrompt });
    },
    [clearError, sendMessage]
  );

  // Consume external prompt dispatched via commitbook:ask
  useEffect(() => {
    if (open && initialPrompt && !isStreaming) {
      const promptToSend = initialPrompt;
      onInitialPromptConsumed?.();
      void handleSend(promptToSend, null);
    }
  }, [open, initialPrompt, isStreaming, handleSend, onInitialPromptConsumed]);

  // Dialog owns Escape, inert background, and the focus trap. This moves focus in
  // after the lazy panel mounts, including when the chunk arrives a frame late.
  useEffect(() => {
    if (!open) return;
    const move = () => {
      const panel = document.querySelector<HTMLElement>(
        '[data-testid="commitbook-chat-panel"]'
      );
      if (!panel) return;
      const active = document.activeElement;
      if (active instanceof HTMLElement && panel.contains(active)) return;
      panel
        .querySelector<HTMLElement>(
          'button:not([disabled]), a[href], textarea, input, select'
        )
        ?.focus();
    };
    const frame = window.requestAnimationFrame(move);
    return () => window.cancelAnimationFrame(frame);
  }, [open]);

  if (!open) return null;

  const lastMessage = messages[messages.length - 1];
  const waitingForFirstToken =
    status === "submitted" ||
    (status === "streaming" &&
      lastMessage?.role === "assistant" &&
      getMessageText(lastMessage).trim().length === 0);

  const showErrorBanner = Boolean((error || customError) && !rateLimited);
  const errorMessage =
    customError ||
    (error?.message && !/failed to fetch|networkerror|network request failed/i.test(error.message)
      ? error.message
      : "Scout could not reach the model. Check your connection, retry, or open a playbook instead.");

  return (
    <div
      className="cb-kokonut-root flex h-full min-h-0 w-full flex-col overflow-hidden bg-[#f7f5f0] text-[#141413] shadow-[0_24px_64px_-16px_rgba(20,20,19,0.34)] ring-1 ring-[#141413]/15 sm:rounded-2xl"
      data-testid="commitbook-chat-panel"
    >
      <div className="relative z-10 flex h-full min-h-0 w-full flex-col overflow-hidden">
        {/* iMessage-style Scout header */}
        <header className="flex shrink-0 items-center justify-between border-[#e5e0d6] border-b bg-white px-4 py-3">
          <div className="flex min-w-0 items-center gap-3">
            <span className="flex size-10 shrink-0 items-center justify-center rounded-full border border-[#141413]/10 bg-[#f7f5f0] text-[#141413]">
              <Compass aria-hidden="true" className="size-5" strokeWidth={1.5} />
            </span>
            <div className="min-w-0">
              <p className="font-sans text-[17px] font-semibold leading-tight tracking-tight text-[#141413]">
                Scout
              </p>
              <p className="mt-0.5 text-[12px] leading-snug text-[#57534e]">
                NCAA rules, cited · AI assistant
              </p>
            </div>
          </div>

          <div className="flex items-center gap-1">
            {isStreaming && (
              <button
                aria-label="Stop generating response"
                className={`rounded-md border border-[#b91c1c]/30 bg-[#b91c1c]/10 px-2.5 py-1 font-mono text-[11px] font-semibold text-[#b91c1c] transition-colors hover:bg-[#b91c1c]/20 ${FOCUS_RING}`}
                data-testid="commitbook-chat-stop-header"
                onClick={() => stop()}
                type="button"
              >
                Stop
              </button>
            )}
            <button
              aria-label="Close Scout"
              className={`flex size-8 items-center justify-center rounded-lg text-[#57534e] transition-colors hover:bg-[#141413]/[0.06] hover:text-[#141413] ${FOCUS_RING}`}
              data-testid="commitbook-chat-close"
              onClick={onClose}
              type="button"
            >
              <X aria-hidden="true" className="size-4" />
            </button>
          </div>
        </header>

        {/* Scrollable Message & State Viewport */}
        <div
          className="scout-messages flex-1 space-y-3 overflow-y-auto bg-[#f7f5f0] px-3.5 py-4"
          data-testid="commitbook-chat-messages"
          ref={scrollContainerRef}
        >
          {/* EMPTY STATE */}
          {messages.length === 0 && !rateLimited && !showErrorBanner && (
            <div className="space-y-4" data-testid="commitbook-chat-empty">
              <div className="flex items-end gap-2">
                <span className="flex size-7 shrink-0 items-center justify-center rounded-full border border-[#141413]/10 bg-white">
                  <Compass aria-hidden="true" className="size-4" strokeWidth={1.5} />
                </span>
                <div className="max-w-[86%] rounded-[18px] rounded-bl-[6px] border border-[#e5e0d6] bg-white px-3.5 py-3 text-[14px] leading-relaxed text-[#141413]">
                  <p className="font-semibold">Hi, I’m Scout.</p>
                  <p className="mt-1">
                    Ask about your sport, class year, or division. I’ll check the rulebook and point you to the next step.
                  </p>
                </div>
              </div>

              <div>
                <p className="mb-2 px-1 font-mono text-[10px] font-semibold uppercase tracking-[0.08em] text-[#57534e]">
                  Start with a question
                </p>
                <div className="grid grid-cols-2 gap-2">
                  {STARTER_PROMPTS.map((item, index) => (
                    <button
                      className={`group flex min-h-[72px] w-full flex-col items-start justify-center gap-1 rounded-2xl border border-[#e5e0d6] bg-white px-3 py-2.5 text-left transition-colors hover:border-[#1d4ed8]/50 ${FOCUS_RING}`}
                      data-testid={`starter-prompt-${index}`}
                      key={item.id}
                      onClick={() => void handleSend(item.question, null)}
                      type="button"
                    >
                      <span className="font-mono text-[9px] font-semibold tracking-[0.08em] text-[#1d4ed8]">
                        {item.tag}
                      </span>
                      <span className="text-[13px] font-medium leading-snug text-[#141413]">
                        {item.shortLabel}
                      </span>
                    </button>
                  ))}
                </div>
              </div>

              <div className="flex flex-wrap items-center gap-x-3 gap-y-2 px-1 pt-1">
                <Link
                  className={`inline-flex items-center gap-1.5 text-[12px] font-medium text-[#1d4ed8] ${FOCUS_RING}`}
                  href="/sops"
                  onClick={onClose}
                >
                  <FileCheck2 aria-hidden="true" className="size-3.5" /> Athlete SOPs
                </Link>
                <Link
                  className={`inline-flex items-center gap-1.5 text-[12px] font-medium text-[#1d4ed8] ${FOCUS_RING}`}
                  href="/window"
                  onClick={onClose}
                >
                  <Calculator aria-hidden="true" className="size-3.5" /> Window Finder
                </Link>
                <Link
                  className={`inline-flex items-center gap-1.5 text-[12px] font-medium text-[#1d4ed8] ${FOCUS_RING}`}
                  href="/offers"
                  onClick={onClose}
                >
                  <Compass aria-hidden="true" className="size-3.5" /> Offers
                </Link>
                <Link
                  className={`inline-flex items-center gap-1.5 text-[12px] font-medium text-[#1d4ed8] ${FOCUS_RING}`}
                  href="/start"
                  onClick={onClose}
                >
                  <BookOpen aria-hidden="true" className="size-3.5" /> Free Plan
                </Link>
              </div>
            </div>
          )}

          {/* CONVERSATION BUBBLES */}
          {messages.map((msg, index) => {
            const text = getMessageText(msg);
            const isUser = msg.role === "user";
            if (!isUser && !text.trim()) return null;
            const showAvatar = !isUser && messages[index - 1]?.role !== "assistant";
            const priorUser = isUser
              ? null
              : messages
                  .slice(0, index)
                  .reverse()
                  .find((item) => item.role === "user");
            const recommendation = priorUser
              ? recommendPlaybook(getMessageText(priorUser))
              : null;

            return (
              <div
                className={`flex flex-col ${isUser ? "items-end" : "items-start"}`}
                data-testid={`chat-message-${msg.role}`}
                key={msg.id}
              >
                <div
                  className={`flex w-full items-end gap-2 ${isUser ? "justify-end" : "justify-start"}`}
                >
                  {!isUser &&
                    (showAvatar ? (
                      <span className="flex size-7 shrink-0 items-center justify-center rounded-full border border-[#141413]/10 bg-white text-[#141413]">
                        <Compass aria-hidden="true" className="size-4" strokeWidth={1.5} />
                      </span>
                    ) : (
                      <span aria-hidden="true" className="size-7 shrink-0" />
                    ))}
                  <div
                    aria-live={isUser ? undefined : "polite"}
                    className={
                      isUser
                        ? "max-w-[78%] rounded-[18px] rounded-br-[6px] bg-[#141413] px-3.5 py-2.5 text-[14px] leading-relaxed text-[#f7f5f0]"
                        : "max-w-[86%] rounded-[18px] rounded-bl-[6px] border border-[#e5e0d6] bg-white px-3.5 py-3 text-[#141413] shadow-[0_1px_2px_rgba(20,20,19,0.04)]"
                    }
                  >
                    {isUser ? (
                      <p className="whitespace-pre-wrap">{text}</p>
                    ) : (
                      <>
                        <FormattedAnswer text={text} />
                        <GuideSources sources={extractGuideSources(msg)} />
                        <div className="mt-2 flex items-center gap-1.5 border-t border-[#141413]/10 pt-2 font-mono text-[9px] font-medium uppercase tracking-[0.06em] text-[#57534e]">
                          <ShieldCheck aria-hidden="true" className="size-3 text-[#15803d]" />
                          2026-27 rulebook · cited sources
                        </div>
                      </>
                    )}
                  </div>
                </div>
                {isUser && index === messages.length - 1 && (
                  <span className="mr-1 mt-1 text-[10px] text-[#57534e]">Delivered</span>
                )}
                {!isUser && recommendation && (
                  <div className="ml-9 w-[calc(100%-2.25rem)]">
                    <PlaybookCard playbook={recommendation} />
                  </div>
                )}
              </div>
            );
          })}

          {/* LOADING / THINKING STATE (Kokonut UI AITextLoading) */}
          {waitingForFirstToken && (
            <div
              className="flex flex-col items-start"
              data-testid="commitbook-chat-loading"
            >
              <span className="mb-1 px-1 font-mono text-[10px] text-[#57534e] uppercase">
                Scout
              </span>
              <div className="rounded-2xl rounded-bl-sm border border-[#e5e0d6] bg-[#ffffff] px-4 py-2.5 shadow-[0_1px_2px_rgba(20,20,19,0.04)]">
                <AITextLoading
                  className="!text-[14px] !font-medium !text-[#141413]"
                  interval={1300}
                  label="Checking the bylaws"
                  showElapsed
                  texts={[
                    "Checking rulebooks",
                    "Verifying contact window",
                    "Pulling Athlete SOP",
                  ]}
                />
              </div>
            </div>
          )}

          {/* RATE-LIMITED STATE (429) */}
          {rateLimited && (
            <div
              className="rounded-xl border border-[#b91c1c]/35 bg-[#ffffff] p-3.5 shadow-sm"
              data-testid="commitbook-chat-ratelimited"
              role="status"
            >
              <div className="flex items-start gap-2.5">
                <Clock
                  aria-hidden="true"
                  className="mt-0.5 size-4 shrink-0 text-[#b91c1c]"
                />
                <div className="space-y-2 text-xs">
                  <div className="flex items-center justify-between gap-2">
                    <span className="font-mono font-semibold text-[#b91c1c] uppercase">
                      Rate Limit Active
                    </span>
                    <span className="rounded bg-[#b91c1c]/10 px-2 py-0.5 font-mono font-semibold text-[#b91c1c] tabular-nums">
                      Retry in {rateLimited.retryAfterSec}s
                    </span>
                  </div>
                  <p className="text-[#57534e] leading-relaxed">
                    {rateLimited.message}
                  </p>
                  <div className="flex flex-wrap gap-2 pt-0.5">
                    <Link
                      className="inline-flex items-center gap-1 rounded border border-[#e5e0d6] bg-[#f7f5f0] px-2.5 py-1 font-medium text-[#141413] hover:border-[#141413]/30"
                      href="/sops"
                      onClick={onClose}
                    >
                      Open Athlete SOPs
                      <ArrowRight aria-hidden="true" className="size-3" />
                    </Link>
                    <Link
                      className="inline-flex items-center gap-1 rounded border border-[#e5e0d6] bg-[#f7f5f0] px-2.5 py-1 font-medium text-[#141413] hover:border-[#141413]/30"
                      href="/window"
                      onClick={onClose}
                    >
                      30-Sec Window Calc
                      <ArrowRight aria-hidden="true" className="size-3" />
                    </Link>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* ERROR STATE */}
          {showErrorBanner && (
            <div
              className="rounded-xl border border-[#b91c1c]/35 bg-[#ffffff] p-3.5 shadow-sm"
              data-testid="commitbook-chat-error"
              role="alert"
            >
              <div className="flex items-start gap-2.5">
                <AlertTriangle
                  aria-hidden="true"
                  className="mt-0.5 size-4 shrink-0 text-[#b91c1c]"
                />
                <div className="space-y-2 text-xs">
                  <p className="font-mono font-semibold text-[#b91c1c] uppercase">
                    Connection Interrupted
                  </p>
                  <p className="text-[#57534e] leading-relaxed">
                    {errorMessage}
                  </p>
                  <div className="flex flex-wrap items-center gap-2 pt-0.5">
                    {lastSubmittedPrompt && (
                      <button
                        className="inline-flex items-center gap-1 rounded bg-[#141413] px-2.5 py-1 font-medium text-[#f7f5f0] hover:bg-[#141413]/90"
                        data-testid="commitbook-chat-retry"
                        onClick={() => void handleSend(lastSubmittedPrompt, null)}
                        type="button"
                      >
                        <RotateCcw aria-hidden="true" className="size-3" />
                        Retry Question
                      </button>
                    )}
                    <Link
                      className="inline-flex items-center gap-1 rounded border border-[#e5e0d6] bg-[#f7f5f0] px-2.5 py-1 font-medium text-[#141413]"
                      href="/sops"
                      onClick={onClose}
                    >
                      Browse SOPs
                    </Link>
                    <Link
                      className="inline-flex items-center gap-1 rounded border border-[#e5e0d6] bg-[#f7f5f0] px-2.5 py-1 font-medium text-[#141413]"
                      href="/start"
                      onClick={onClose}
                    >
                      Free Plan
                    </Link>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Scout composer */}
        <footer className="cb-prompt-contrast shrink-0 border-[#e5e0d6] border-t bg-white px-3 pb-[max(0.5rem,env(safe-area-inset-bottom))] pt-1">
          <style>{
            `.cb-prompt-contrast textarea::placeholder { color: #57534e !important; opacity: 1 !important; }
            .cb-prompt-contrast [role="option"] > span:last-child { color: #57534e !important; }
            .cb-prompt-contrast [role="listbox"] + div { color: #57534e !important; }`
          }</style>
          <AI_Prompt
            className="!max-w-none !py-1.5"
            commands={SLASH_COMMANDS}
            disabled={Boolean(rateLimited)}
            footerHint={
              rateLimited
                ? `Cooldown: ${rateLimited.retryAfterSec}s`
                : "Type / for sport SOP shortcuts"
            }
            headerText=""
            isStreaming={isStreaming}
            onStop={() => stop()}
            onSubmit={async (value, _model, opts) => {
              await handleSend(value, opts.command);
            }}
            placeholder="Ask about your sport, grad year, camps, or film..."
            showAttachButton={false}
            showModelControls={false}
          />
          <p className="px-1 pb-1 text-center text-[10px] leading-snug text-[#57534e]">
            AI assistant, not the NCAA. Verify rules before acting.
          </p>
        </footer>
      </div>
    </div>
  );
}
