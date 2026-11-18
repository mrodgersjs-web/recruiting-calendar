"use client";

import { useEffect } from "react";

export default function LegacyPageScripts({
  dataPage,
  externalScripts,
  inlineScripts,
}: {
  dataPage?: string;
  externalScripts: string[];
  inlineScripts: string[];
}) {
  useEffect(() => {
    if (dataPage) {
      document.body.setAttribute("data-page", dataPage);
    } else {
      document.body.removeAttribute("data-page");
    }

    // Wire header "Ask Guide" trigger inside legacy HTML
    const onDocClick = (e: MouseEvent) => {
      const target = e.target as HTMLElement | null;
      const askTrigger = target?.closest?.("[data-cb-ask-trigger]");
      if (askTrigger) {
        e.preventDefault();
        const prompt = askTrigger.getAttribute("data-prompt") || undefined;
        window.dispatchEvent(
          new CustomEvent("commitbook:ask", { detail: { prompt } })
        );
      }
    };
    document.addEventListener("click", onDocClick);

    // Load external scripts sequentially after hydration/idle so LCP is untouched
    let cancelled = false;
    const loadScripts = async () => {
      for (const src of externalScripts) {
        if (cancelled) return;
        const cleanBase = src.split("?")[0];
        if (document.querySelector(`script[data-cb-legacy-src="${cleanBase}"]`)) {
          continue;
        }
        await new Promise<void>((resolve) => {
          const s = document.createElement("script");
          s.src = src;
          s.async = false;
          s.defer = true;
          s.setAttribute("data-cb-legacy-src", cleanBase);
          s.onload = () => resolve();
          s.onerror = () => resolve();
          document.body.appendChild(s);
        });
      }

      for (let i = 0; i < inlineScripts.length; i += 1) {
        if (cancelled) return;
        const code = inlineScripts[i];
        try {
          const fn = new Function(code);
          fn();
        } catch {
          // ignore legacy inline script mismatch
        }
      }
    };

    if ("requestIdleCallback" in window) {
      window.requestIdleCallback(() => {
        void loadScripts();
      });
    } else {
      setTimeout(() => {
        void loadScripts();
      }, 120);
    }

    return () => {
      cancelled = true;
      document.removeEventListener("click", onDocClick);
    };
  }, [dataPage, externalScripts, inlineScripts]);

  return null;
}
