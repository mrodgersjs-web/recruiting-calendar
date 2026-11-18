import fs from "node:fs";
import path from "node:path";

export interface ParsedLegacyPage {
  title: string;
  description: string;
  canonical?: string;
  stylesheets: string[];
  inlineStyles: string[];
  bodyClass: string;
  bodyHtml: string;
  scripts: { src?: string; inline?: string; type?: string }[];
}

const SITE_ROOT = path.join(process.cwd(), "site");

function stripTags(s: string): string {
  return s.replace(/<[^>]*>/g, "").trim();
}

export function resolveLegacyHtmlPath(slugParts: string[]): string | null {
  const clean = slugParts.filter(Boolean);
  if (clean.some((p) => p.includes("..") || p.startsWith("."))) return null;

  const relDir = clean.join("/");
  const candidates =
    clean.length === 0
      ? [path.join(SITE_ROOT, "index.html")]
      : [
          path.join(SITE_ROOT, relDir, "index.html"),
          path.join(SITE_ROOT, `${relDir}.html`),
        ];

  for (const c of candidates) {
    if (fs.existsSync(c) && fs.statSync(c).isFile()) {
      return c;
    }
  }
  return null;
}

export function listAllLegacySlugs(): string[][] {
  const results: string[][] = [];
  function walk(dir: string, relParts: string[]) {
    if (!fs.existsSync(dir)) return;
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      if (entry.name === "node_modules" || entry.name.startsWith(".")) continue;
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        walk(full, [...relParts, entry.name]);
      } else if (entry.isFile() && entry.name === "index.html" && relParts.length > 0) {
        results.push(relParts);
      }
    }
  }
  walk(SITE_ROOT, []);
  return results;
}

const WORKBENCH_RIBBON = `</header>
<div class="cb-workbench-ribbon" role="region" aria-label="Athlete Recruiting Workbench">
  <div class="cb-workbench-ribbon__inner">
    <div class="cb-workbench-ribbon__links">
      <span class="cb-workbench-ribbon__tag">Athlete Workbench</span>
      <a href="/sops" class="cb-workbench-ribbon__link">4 Official Athlete SOPs</a>
      <span aria-hidden="true" style="color:#b8b1a3">/</span>
      <a href="/window" class="cb-workbench-ribbon__link">30-Sec Contact Window Calculator</a>
      <span aria-hidden="true" style="color:#b8b1a3">/</span>
      <a href="/auditor" class="cb-workbench-ribbon__link">Camp &amp; Aid Red-Flag Test</a>
      <span aria-hidden="true" style="color:#b8b1a3">/</span>
      <a href="/offers" class="cb-workbench-ribbon__link">10 Family Recruiting Offers</a>
    </div>
    <button type="button" onclick="window.dispatchEvent(new CustomEvent('commitbook:open'))" class="cb-workbench-ribbon__ask">Ask Commit Book Guide</button>
  </div>
</div>`;

export function parseLegacyHtml(filePath: string): ParsedLegacyPage {
  const raw = fs.readFileSync(filePath, "utf8");

  const headMatch = raw.match(/<head[^>]*>([\s\S]*?)<\/head>/i);
  const head = headMatch ? headMatch[1] : "";

  const titleMatch = head.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
  const title = titleMatch ? stripTags(titleMatch[1]) : "The Commit Book";

  const descMatch =
    head.match(/<meta[^>]+name=["']description["'][^>]+content=["']([^"']*)["']/i) ??
    head.match(/<meta[^>]+content=["']([^"']*)["'][^>]+name=["']description["']/i);
  const description = descMatch ? descMatch[1] : "Real paths to a college roster.";

  const canonMatch = head.match(/<link[^>]+rel=["']canonical["'][^>]+href=["']([^"']*)["']/i);
  const canonical = canonMatch ? canonMatch[1] : undefined;

  const stylesheets: string[] = [];
  const linkRe = /<link\b[^>]*rel=["']stylesheet["'][^>]*>/gi;
  let lm: RegExpExecArray | null;
  while ((lm = linkRe.exec(head)) !== null) {
    const tag = lm[0];
    const hrefMatch = tag.match(/href=["']([^"']+)["']/i);
    if (!hrefMatch) continue;
    const href = hrefMatch[1];
    if (href.includes("fonts.googleapis.com") || href.includes("fonts.gstatic.com")) continue;
    if (href === "/assets/tokens.css" || href === "/assets/commit.css" || href === "/style.css") continue;
    stylesheets.push(href);
  }

  const inlineStyles: string[] = [];
  const styleRe = /<style[^>]*>([\s\S]*?)<\/style>/gi;
  let sm: RegExpExecArray | null;
  while ((sm = styleRe.exec(head)) !== null) {
    if (sm[1].trim()) inlineStyles.push(sm[1]);
  }

  const bodyOpenMatch = raw.match(/<body([^>]*)>([\s\S]*?)<\/body>/i);
  const bodyAttrs = bodyOpenMatch ? bodyOpenMatch[1] : "";
  let bodyContent = bodyOpenMatch ? bodyOpenMatch[2] : raw;

  const classMatch = bodyAttrs.match(/class=["']([^"']*)["']/i);
  const bodyClass = classMatch ? classMatch[1] : "";

  const scripts: { src?: string; inline?: string; type?: string }[] = [];
  const scriptRe = /<script\b([^>]*)>([\s\S]*?)<\/script>/gi;
  bodyContent = bodyContent.replace(scriptRe, (_full, attrs: string, inner: string) => {
    const typeMatch = attrs.match(/type=["']([^"']+)["']/i);
    const type = typeMatch ? typeMatch[1] : undefined;
    if (type === "application/ld+json") {
      return _full;
    }
    const srcMatch = attrs.match(/src=["']([^"']+)["']/i);
    if (srcMatch) {
      scripts.push({ src: srcMatch[1], type });
    } else if (inner.trim()) {
      scripts.push({ inline: inner, type });
    }
    return "";
  });

  if (bodyContent.includes("</header>")) {
    bodyContent = bodyContent.replace("</header>", WORKBENCH_RIBBON);
  }

  return {
    title,
    description,
    canonical,
    stylesheets,
    inlineStyles,
    bodyClass,
    bodyHtml: bodyContent,
    scripts,
  };
}
