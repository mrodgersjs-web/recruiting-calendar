"use client";

import { useChat } from "@ai-sdk/react";
import { DefaultChatTransport, type UIMessage } from "ai";
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
  Sparkles,
  X,
} from "lucide-react";
import Link from "next/link";
import React, { useCallback, useEffect, useMemo, useRef, useState } from "react";
import AI_Prompt, { type PromptCommand } from "@/components/kokonutui/ai-prompt";
import AITextLoading from "@/components/kokonutui/ai-text-loading";

export const STARTER_PROMPTS = [
  {
    id: "sp-1",
    tag: "CONTACT DATES",
    question:
      "When can D1 vs D3 college coaches first contact a Class of 2029 football or volleyball athlete?",
  },
  {
    id: "sp-2",
    tag: "ATHLETE SOPs",
    question:
      "What belongs in the first 30 seconds of a recruiting highlight video, and what gets turned off immediately?",
  },
  {
    id: "sp-3",
    tag: "CAMP RED FLAGS",
    question:
      "How do we tell if a $600 showcase camp invite is worth attending or a money trap?",
  },
  {
    id: "sp-4",
    tag: "HIGHLIGHT FILM",
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
              setCustomError("Unable to reach the Commit Book Guide right now.");
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

  // Close sheet on Escape when not actively streaming
  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape" && !isStreaming) {
        onClose();
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, isStreaming, onClose]);

  if (!open) return null;

  const lastMessage = messages[messages.length - 1];
  const waitingForFirstToken =
    status === "submitted" ||
    (status === "streaming" &&
      lastMessage?.role === "assistant" &&
      getMessageText(lastMessage).trim().length === 0);

  const showErrorBanner = Boolean((error || customError) && !rateLimited);

  return (
    <div
      aria-label="Commit Book Recruiting Guide"
      aria-modal="true"
      className="cb-kokonut-root fixed inset-0 z-[90] flex items-end justify-end sm:inset-auto sm:right-5 sm:bottom-5"
      data-testid="commitbook-chat-panel"
      role="dialog" style={{ backgroundColor: "#f7f5f0", color: "#141413" }}
    >
      {/* Mobile backdrop */}
      <div
        aria-hidden="true"
        className="fixed inset-0 bg-[#141413]/40 backdrop-blur-[1px] sm:hidden"
        onClick={onClose}
      />

      <div className="relative z-10 flex h-[100dvh] w-full flex-col overflow-hidden bg-[#f7f5f0] text-[#141413] shadow-[0_24px_64px_-16px_rgba(20,20,19,0.34)] ring-1 ring-[#141413]/15 sm:h-[min(690px,86dvh)] sm:w-[436px] sm:rounded-2xl">
        {/* Editorial Header */}
        <header className="flex shrink-0 items-center justify-between border-[#e5e0d6] border-b bg-[#ffffff] px-4 py-3.5">
          <div className="flex items-center gap-2.5 min-w-0">
            <span className="flex size-8 shrink-0 items-center justify-center rounded-lg bg-[#141413] font-serif text-[#f7f5f0] text-sm font-semibold">
              CB
            </span>
            <div className="min-w-0">
              <div className="flex items-center gap-2">
                <h2 className="truncate font-serif text-[16px] font-semibold text-[#141413] leading-tight">
                  Commit Book Guide
                </h2>
                <span className="inline-flex items-center gap-1 rounded border border-[#15803d]/25 bg-[#15803d]/10 px-1.5 py-0.5 font-mono text-[10px] font-medium text-[#15803d] uppercase">
                  <ShieldCheck aria-hidden="true" className="size-2.5" />
                  Verified KB
                </span>
              </div>
              <p className="truncate font-mono text-[11px] text-[#57534e]">
                2026-27 NCAA D1-D3, NAIA & NJCAA + Athlete SOPs
              </p>
            </div>
          </div>

          <div className="flex items-center gap-1">
            {isStreaming && (
              <button
                aria-label="Stop generating response"
                className="rounded-md border border-[#b91c1c]/30 bg-[#b91c1c]/10 px-2.5 py-1 font-mono text-[11px] font-semibold text-[#b91c1c] transition-colors hover:bg-[#b91c1c]/20"
                data-testid="commitbook-chat-stop-header"
                onClick={() => stop()}
                type="button"
              >
                Stop
              </button>
            )}
            <button
              aria-label="Close Commit Book Guide"
              className="flex size-8 items-center justify-center rounded-lg text-[#57534e] transition-colors hover:bg-[#141413]/[0.06] hover:text-[#141413]"
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
          className="flex-1 overflow-y-auto px-4 py-4 space-y-4"
          data-testid="commitbook-chat-messages"
          ref={scrollContainerRef}
        >
          {/* EMPTY STATE */}
          {messages.length === 0 && !rateLimited && !showErrorBanner && (
            <div className="space-y-4" data-testid="commitbook-chat-empty">
              <div className="rounded-xl border border-[#e5e0d6] bg-[#ffffff] p-4 shadow-[0_1px_2px_rgba(20,20,19,0.04)]">
                <div className="mb-1.5 flex items-center gap-1.5 font-mono text-[11px] font-medium text-[#1d4ed8] uppercase tracking-wider">
                  <Sparkles aria-hidden="true" className="size-3.5" />
                  Rulebook-Grounded Answers in Under 10s
                </div>
                <p className="text-[13.5px] text-[#57534e] leading-relaxed">
                  Ask about coach contact windows, the 105-man roster cap, highlight film specs, camp money traps, or grade 9-12 Athlete SOPs. No agency sales pitch.
                </p>
              </div>

              <div className="space-y-2">
                <p className="px-0.5 font-mono text-[11px] font-semibold text-[#57534e] uppercase tracking-wider">
                  Top Family & Athlete Questions
                </p>
                <div className="space-y-2">
                  {STARTER_PROMPTS.map((item, index) => (
                    <button
                      className="group flex w-full flex-col items-start gap-1 rounded-xl border border-[#e5e0d6] bg-[#ffffff] px-3.5 py-3 text-left transition-all hover:border-[#1d4ed8]/50 hover:shadow-[0_4px_12px_-4px_rgba(29,78,216,0.14)]"
                      data-testid={`starter-prompt-${index}`}
                      key={item.id}
                      onClick={() => void handleSend(item.question, null)}
                      type="button"
                    >
                      <span className="font-mono text-[10px] font-semibold text-[#1d4ed8] tracking-wider">
                        {item.tag}
                      </span>
                      <span className="flex w-full items-center justify-between gap-2 text-[13.5px] font-medium text-[#141413] leading-snug">
                        <span>{item.question}</span>
                        <ArrowRight
                          aria-hidden="true"
                          className="size-3.5 shrink-0 text-[#57534e] transition-transform group-hover:translate-x-0.5 group-hover:text-[#1d4ed8]"
                        />
                      </span>
                    </button>
                  ))}
                </div>
              </div>

              {/* Direct Self-Serve Quick Jump Pills */}
              <div className="pt-1">
                <p className="mb-2 px-0.5 font-mono text-[11px] font-semibold text-[#57534e] uppercase tracking-wider">
                  Or Jump Straight To A Tool
                </p>
                <div className="grid grid-cols-2 gap-2">
                  <Link
                    className="flex items-center gap-2 rounded-lg border border-[#e5e0d6] bg-[#ffffff] px-3 py-2 text-xs font-medium text-[#141413] transition-colors hover:border-[#141413]/30"
                    href="/sops"
                    onClick={onClose}
                  >
                    <FileCheck2 aria-hidden="true" className="size-3.5 text-[#1d4ed8]" />
                    <span>Athlete SOPs</span>
                  </Link>
                  <Link
                    className="flex items-center gap-2 rounded-lg border border-[#e5e0d6] bg-[#ffffff] px-3 py-2 text-xs font-medium text-[#141413] transition-colors hover:border-[#141413]/30"
                    href="/window"
                    onClick={onClose}
                  >
                    <Calculator aria-hidden="true" className="size-3.5 text-[#1d4ed8]" />
                    <span>Window Finder</span>
                  </Link>
                  <Link
                    className="flex items-center gap-2 rounded-lg border border-[#e5e0d6] bg-[#ffffff] px-3 py-2 text-xs font-medium text-[#141413] transition-colors hover:border-[#141413]/30"
                    href="/offers"
                    onClick={onClose}
                  >
                    <Compass aria-hidden="true" className="size-3.5 text-[#1d4ed8]" />
                    <span>10 New Offers</span>
                  </Link>
                  <Link
                    className="flex items-center gap-2 rounded-lg border border-[#e5e0d6] bg-[#ffffff] px-3 py-2 text-xs font-medium text-[#141413] transition-colors hover:border-[#141413]/30"
                    href="/start"
                    onClick={onClose}
                  >
                    <BookOpen aria-hidden="true" className="size-3.5 text-[#1d4ed8]" />
                    <span>Free Plan</span>
                  </Link>
                </div>
              </div>
            </div>
          )}

          {/* CONVERSATION BUBBLES */}
          {messages.map((msg) => {
            const text = getMessageText(msg);
            const isUser = msg.role === "user";
            if (!isUser && !text.trim()) return null;

            return (
              <div
                className={`flex flex-col ${isUser ? "items-end" : "items-start"}`}
                data-testid={`chat-message-${msg.role}`}
                key={msg.id}
              >
                <span className="mb-1 px-1 font-mono text-[10px] text-[#57534e] uppercase">
                  {isUser ? "You" : "Commit Book Guide"}
                </span>
                <div
                  className={
                    isUser
                      ? "max-w-[86%] rounded-2xl rounded-br-sm bg-[#141413] px-3.5 py-2.5 text-[14px] text-[#f7f5f0] leading-relaxed"
                      : "max-w-[94%] rounded-2xl rounded-bl-sm border border-[#e5e0d6] bg-[#ffffff] px-3.5 py-3 text-[#141413] shadow-[0_1px_2px_rgba(20,20,19,0.04)]"
                  }
                >
                  {isUser ? (
                    <p className="whitespace-pre-wrap">{text}</p>
                  ) : (
                    <FormattedAnswer text={text} />
                  )}
                </div>
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
                Commit Book Guide
              </span>
              <div className="rounded-2xl rounded-bl-sm border border-[#e5e0d6] bg-[#ffffff] px-4 py-2.5 shadow-[0_1px_2px_rgba(20,20,19,0.04)]">
                <AITextLoading
                  className="!text-[14px] !font-medium !text-[#141413]"
                  interval={1300}
                  label="Checking Commit Book rulebooks and Athlete SOPs"
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
                    {customError ||
                      error?.message ||
                      "We could not complete that answer right now."}
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

        {/* Kokonut UI AI_Prompt Input Footer */}
        <footer className="shrink-0 border-[#e5e0d6] border-t bg-[#f7f5f0] px-3 pt-1 pb-2">
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
        </footer>
      </div>
    </div>
  );
}
