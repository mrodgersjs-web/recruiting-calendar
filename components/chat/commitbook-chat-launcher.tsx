"use client";

import dynamic from "next/dynamic";
import { useEffect, useState } from "react";

const LazyCommitBookChatbot = dynamic(
  () => import("@/components/chat/commitbook-chatbot"),
  { ssr: false }
);

export default function CommitBookChatLauncher() {
  const [open, setOpen] = useState(false);
  const [shouldMountSheet, setShouldMountSheet] = useState(false);
  const [queuedPrompt, setQueuedPrompt] = useState<string | null>(null);

  const warmChunk = () => {
    if (!shouldMountSheet) {
      setShouldMountSheet(true);
    }
  };

  // Listen for custom "commitbook:ask" events dispatched anywhere on the site (SOP hub, Window Finder, Offers Lab, static pages)
  useEffect(() => {
    const handleAskEvent = (event: Event) => {
      const custom = event as CustomEvent<{ prompt?: string }>;
      const prompt = custom.detail?.prompt?.trim();
      setShouldMountSheet(true);
      if (prompt) {
        setQueuedPrompt(prompt);
      }
      setOpen(true);
    };

    const handleOpen = () => { setShouldMountSheet(true); setOpen(true); };
    window.addEventListener("commitbook:ask", handleAskEvent);
    window.addEventListener("commitbook:open", handleOpen);
    return () => {
      window.removeEventListener("commitbook:ask", handleAskEvent);
      window.removeEventListener("commitbook:open", handleOpen);
    };
  }, []);

  return (
    <>
      {!open && (
        <button
          aria-label="Ask the Commit Book Recruiting Guide"
          className="fixed right-4 bottom-4 z-[85] inline-flex items-center gap-2.5 rounded-full border border-[#141413]/15 bg-[#141413] px-4 py-3 text-[#f7f5f0] shadow-[0_12px_30px_-8px_rgba(20,20,19,0.42)] transition-transform duration-150 hover:-translate-y-0.5 focus-visible:outline-2 focus-visible:outline-[#1d4ed8] focus-visible:outline-offset-2 sm:right-6 sm:bottom-6"
          data-testid="commitbook-chat-launcher"
          onClick={() => {
            setShouldMountSheet(true);
            setOpen(true);
          }}
          onFocus={warmChunk}
          onMouseEnter={warmChunk}
          type="button"
        >
          <span
            aria-hidden="true"
            className="flex size-2.5 rounded-full bg-[#22c55e] ring-4 ring-[#22c55e]/25"
          />
          <span className="font-sans text-[13.5px] font-semibold tracking-tight">
            Ask Recruiting Guide
          </span>
          <span className="hidden rounded bg-[#f7f5f0]/15 px-1.5 py-0.5 font-mono text-[10px] text-[#f7f5f0]/90 sm:inline">
            SOPs + Rules
          </span>
        </button>
      )}

      {shouldMountSheet && (
        <LazyCommitBookChatbot
          initialPrompt={queuedPrompt}
          onClose={() => setOpen(false)}
          onInitialPromptConsumed={() => setQueuedPrompt(null)}
          open={open}
        />
      )}
    </>
  );
}
