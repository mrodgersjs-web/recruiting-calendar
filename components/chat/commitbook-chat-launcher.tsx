"use client";

import {
  Dialog,
  DialogBackdrop,
  DialogContent,
  DialogDescription,
  DialogTitle,
} from "@ui-sdk/react/dialog";
import dynamic from "next/dynamic";
import { useEffect, useRef, useState } from "react";

const LazyCommitBookChatbot = dynamic(
  () => import("@/components/chat/commitbook-chatbot"),
  { ssr: false }
);

const FOCUS_RING =
  "focus-visible:outline-2 focus-visible:outline-[#1d4ed8] focus-visible:outline-offset-2";

export default function CommitBookChatLauncher() {
  const [open, setOpen] = useState(false);
  const [shouldMountSheet, setShouldMountSheet] = useState(false);
  const [queuedPrompt, setQueuedPrompt] = useState<string | null>(null);
  const launcherRef = useRef<HTMLButtonElement>(null);

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

    const handleOpen = () => {
      setShouldMountSheet(true);
      setOpen(true);
    };
    window.addEventListener("commitbook:ask", handleAskEvent);
    window.addEventListener("commitbook:open", handleOpen);
    return () => {
      window.removeEventListener("commitbook:ask", handleAskEvent);
      window.removeEventListener("commitbook:open", handleOpen);
    };
  }, []);

  return (
    <Dialog
      modal
      onOpenChange={(next) => {
        if (next) setShouldMountSheet(true);
        setOpen(next);
      }}
      open={open}
      persistentElements={() => (launcherRef.current ? [launcherRef.current] : [])}
      presentation="sheet"
    >
      <style>{`
        .cb-chat-dialog[popover],
        .cb-chat-dialog {
          position: fixed !important;
          inset: 0 !important;
          width: 100% !important;
          height: 100dvh !important;
          max-width: none !important;
          max-height: none !important;
          margin: 0 !important;
          padding: 0 !important;
          border: 0 !important;
          overflow: visible !important;
          background: transparent !important;
          color: #141413 !important;
        }
        .cb-chat-backdrop[popover],
        .cb-chat-backdrop {
          position: fixed !important;
          inset: 0 !important;
          width: 100% !important;
          height: 100% !important;
          margin: 0 !important;
          padding: 0 !important;
          border: 0 !important;
          background: rgba(20, 20, 19, 0.4) !important;
        }
        @media (min-width: 640px) {
          .cb-chat-dialog[popover],
          .cb-chat-dialog {
            inset: auto !important;
            top: auto !important;
            left: auto !important;
            right: 2rem !important;
            bottom: 11rem !important;
            width: min(400px, calc(100vw - 4rem)) !important;
            height: min(640px, 72dvh) !important;
          }
        }
      `}</style>
      <button
        aria-controls="commitbook-chat-dialog"
        aria-expanded={open}
        aria-haspopup="dialog"
        aria-label="Ask the Recruiting Guide"
        className={`fixed right-4 bottom-24 z-[85] inline-flex items-center gap-2.5 rounded-full border border-[#141413]/15 bg-[#141413] px-4 py-3 text-[#f7f5f0] shadow-[0_12px_30px_-8px_rgba(20,20,19,0.42)] transition-transform duration-150 hover:-translate-y-0.5 sm:right-8 sm:bottom-28 ${FOCUS_RING}`}
        data-testid="commitbook-chat-launcher"
        onClick={() => {
          setShouldMountSheet(true);
          setOpen(true);
        }}
        onFocus={warmChunk}
        onMouseEnter={warmChunk}
        ref={launcherRef}
        type="button"
      >
        <span className="font-sans text-[13.5px] font-semibold tracking-tight">
          Ask Recruiting Guide
        </span>
        <span className="hidden rounded bg-[#f7f5f0]/15 px-1.5 py-0.5 font-mono text-[10px] text-[#f7f5f0]/90 sm:inline">
          SOPs + Rules
        </span>
      </button>

      {shouldMountSheet && (
        <>
          <DialogBackdrop className="cb-chat-backdrop" />
          <DialogContent
            className="cb-chat-dialog"
            finalFocus={() => launcherRef.current}
            id="commitbook-chat-dialog"
            initialFocus={() => {
              const panel = document.querySelector(
                '[data-testid="commitbook-chat-panel"]'
              );
              return (
                panel?.querySelector<HTMLElement>(
                  'button:not([disabled]), a[href], textarea, input, select'
                ) ?? null
              );
            }}
            keepMounted
          >
            <DialogTitle className="sr-only">Recruiting Guide</DialogTitle>
            <DialogDescription className="sr-only">
              SOPs, contact windows, and camp rules.
            </DialogDescription>
            <LazyCommitBookChatbot
              initialPrompt={queuedPrompt}
              onClose={() => setOpen(false)}
              onInitialPromptConsumed={() => setQueuedPrompt(null)}
              open={open}
            />
          </DialogContent>
        </>
      )}
    </Dialog>
  );
}
