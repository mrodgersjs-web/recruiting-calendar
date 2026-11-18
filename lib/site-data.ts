import fs from "node:fs";
import path from "node:path";
import type { OffersCatalog } from "@/components/upgrade/offer-types";
import type { AthleteSop } from "@/components/upgrade/sop-types";

const ROOT = process.cwd();
const SITE_DIR = path.join(ROOT, "site");
const CONTENT_DIR = path.join(ROOT, "content");

const GLOBAL_STYLES_SKIP = new Set([
  "/style.css",
  "/assets/tokens.css",
  "/assets/commit.css",
  "/assets/ring.css",
  "/assets/deck.css",
]);

export interface ParsedLegacyPage {
  title: string;
  description: string;
  dataPage: string;
  extraStylesheets: string[];
  bodyHtmlWithoutScripts: string;
  externalScripts: string[];
  inlineScripts: string[];
}

function stripVersionQuery(href: string): string {
  return href.split("?")[0] || href;
}

export function upgradeLegacyNavHtml(html: string): string {
  // Inject Athlete SOPs, Window Finder, Camp Auditor, and 10 Offers into #site-nav if not already present
  let out = html;
  if (out.includes('id="site-nav"') && !out.includes('href="/sops"')) {
    out = out.replace(
      /(<nav[^>]*id="site-nav"[^>]*>)/i,
      '$1<a href="/sops" class="cb-nav-pill-new">Athlete SOPs</a><a href="/window">Window Calc</a><a href="/auditor">Camp &amp; Aid Test</a><a href="/offers">10 Offers</a>'
    );
  }
  // Add an inline "Ask Guide" trigger right before the closing </header> on cb-header
  if (out.includes("cb-header") && !out.includes("data-cb-ask-trigger")) {
    out = out.replace(
      /<\/header>/i,
      '<button type="button" class="cb-header-ask-btn" data-cb-ask-trigger="1" aria-label="Open Commit Book Recruiting Guide">Ask Guide</button></header>'
    );
  }
  return out;
}

export function parseLegacyHtmlFile(relHtmlPath: string): ParsedLegacyPage | null {
  const absPath = path.join(SITE_DIR, relHtmlPath);
  if (!fs.existsSync(absPath)) return null;

  const raw = fs.readFileSync(absPath, "utf8");

  const titleMatch = /<title>([\s\S]*?)<\/title>/i.exec(raw);
  const descMatch = /<meta\s+name="description"\s+content="([^"]*)"/i.exec(raw);
  const bodyOpenMatch = /<body([^>]*)>([\s\S]*?)<\/body>/i.exec(raw);

  const title = titleMatch ? titleMatch[1].trim() : "The Commit Book";
  const description = descMatch
    ? descMatch[1].trim()
    : "Real paths, NCAA/NAIA/NJCAA dates, and Athlete SOPs for college recruiting.";

  const bodyAttrs = bodyOpenMatch ? bodyOpenMatch[1] : "";
  const dataPageMatch = /data-page="([^"]*)"/i.exec(bodyAttrs);
  const dataPage = dataPageMatch ? dataPageMatch[1] : "";

  const headMatch = /<head[^>]*>([\s\S]*?)<\/head>/i.exec(raw);
  const headHtml = headMatch ? headMatch[1] : "";

  const extraStylesheets: string[] = [];
  const linkRegex = /<link\b[^>]*rel="stylesheet"[^>]*href="([^"]+)"[^>]*>/gi;
  let linkMatch: RegExpExecArray | null = linkRegex.exec(headHtml);
  while (linkMatch !== null) {
    const href = linkMatch[1];
    const baseHref = stripVersionQuery(href);
    if (
      href.startsWith("/") &&
      !GLOBAL_STYLES_SKIP.has(baseHref) &&
      !extraStylesheets.includes(href)
    ) {
      extraStylesheets.push(href);
    }
    linkMatch = linkRegex.exec(headHtml);
  }

  let bodyInner = bodyOpenMatch ? bodyOpenMatch[2] : raw;
  const externalScripts: string[] = [];
  const inlineScripts: string[] = [];

  // Extract head defer scripts as well
  const scriptRegex = /<script\b([^>]*)>([\s\S]*?)<\/script>/gi;
  let headScriptMatch: RegExpExecArray | null = scriptRegex.exec(headHtml);
  while (headScriptMatch !== null) {
    const attrs = headScriptMatch[1] || "";
    const srcMatch = /\bsrc="([^"]+)"/i.exec(attrs);
    if (srcMatch?.[1]) {
      if (!externalScripts.includes(srcMatch[1])) {
        externalScripts.push(srcMatch[1]);
      }
    }
    headScriptMatch = scriptRegex.exec(headHtml);
  }

  // Extract and strip scripts from bodyInner so React hydration stays clean
  bodyInner = bodyInner.replace(
    /<script\b([^>]*)>([\s\S]*?)<\/script>/gi,
    (_full, attrs: string, code: string) => {
      const typeMatch = /\btype="([^"]+)"/i.exec(attrs || "");
      if (typeMatch && typeMatch[1] === "application/ld+json") {
        return _full; // preserve structured data JSON-LD inline
      }
      const srcMatch = /\bsrc="([^"]+)"/i.exec(attrs || "");
      if (srcMatch?.[1]) {
        if (!externalScripts.includes(srcMatch[1])) {
          externalScripts.push(srcMatch[1]);
        }
      } else if (code && code.trim().length > 0) {
        inlineScripts.push(code.trim());
      }
      return "";
    }
  );

  const upgradedBody = upgradeLegacyNavHtml(bodyInner);

  return {
    title,
    description,
    dataPage,
    extraStylesheets,
    bodyHtmlWithoutScripts: upgradedBody,
    externalScripts,
    inlineScripts,
  };
}

export function listAllLegacyStaticSlugs(): string[][] {
  const slugs: string[][] = [];
  function walk(currentDir: string, parts: string[]) {
    if (!fs.existsSync(currentDir)) return;
    for (const entry of fs.readdirSync(currentDir, { withFileTypes: true })) {
      if (entry.name === "node_modules" || entry.name.startsWith(".")) continue;
      const fullPath = path.join(currentDir, entry.name);
      if (entry.isDirectory()) {
        walk(fullPath, [...parts, entry.name]);
      } else if (entry.isFile() && entry.name === "index.html" && parts.length > 0) {
        // Skip routes owned by native React pages if any overlap
        const top = parts[0];
        if (top !== "sops" && top !== "offers" && top !== "window" && top !== "auditor") {
          slugs.push(parts);
        }
      }
    }
  }
  walk(SITE_DIR, []);
  return slugs;
}

export function loadAllAthleteSops(): AthleteSop[] {
  const sopsDir = path.join(CONTENT_DIR, "sops");
  const orderedFiles = [
    "football.json",
    "boys-basketball.json",
    "girls-basketball.json",
    "volleyball.json",
  ];
  const loaded: AthleteSop[] = [];
  for (const filename of orderedFiles) {
    const filePath = path.join(sopsDir, filename);
    if (!fs.existsSync(filePath)) continue;
    try {
      const parsed = JSON.parse(fs.readFileSync(filePath, "utf8")) as AthleteSop;
      loaded.push(parsed);
    } catch {
      // ignore malformed file
    }
  }
  return loaded;
}

export function normalizeSportSlug(input?: string | null): string | undefined {
  if (!input) return undefined;
  const clean = input.toLowerCase().trim();
  if (clean === "mens-basketball" || clean === "basketball") return "boys-basketball";
  if (clean === "womens-basketball") return "girls-basketball";
  if (clean === "womens-volleyball") return "volleyball";
  if (clean === "mens-football") return "football";
  return clean;
}

export function loadOffersCatalog(): OffersCatalog {
  const filePath = path.join(CONTENT_DIR, "offers-10x.json");
  if (!fs.existsSync(filePath)) {
    return {
      generatedAt: "2026-11-17",
      socialSignalsCount: 0,
      platformsQueried: [],
      offers: [],
    };
  }
  return JSON.parse(fs.readFileSync(filePath, "utf8")) as OffersCatalog;
}
