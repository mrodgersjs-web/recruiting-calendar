import fs from "node:fs";
import path from "node:path";

const ROOT = process.cwd();
const SITE_DIR = path.join(ROOT, "site");
const PUBLIC_DIR = path.join(ROOT, "public");

function copyNonHtmlRecursive(srcDir, destDir) {
  if (!fs.existsSync(srcDir)) return 0;
  let copied = 0;
  for (const entry of fs.readdirSync(srcDir, { withFileTypes: true })) {
    if (entry.name === "node_modules" || entry.name === ".DS_Store") continue;
    const srcPath = path.join(srcDir, entry.name);
    const destPath = path.join(destDir, entry.name);
    if (entry.isDirectory()) {
      copied += copyNonHtmlRecursive(srcPath, destPath);
    } else if (entry.isFile() && !entry.name.endsWith(".html") && entry.name !== "package.json") {
      fs.mkdirSync(path.dirname(destPath), { recursive: true });
      fs.copyFileSync(srcPath, destPath);
      copied += 1;
    }
  }
  return copied;
}

const total = copyNonHtmlRecursive(SITE_DIR, PUBLIC_DIR);

// Build combined legacy CSS without render-blocking Google Fonts @import (loaded via next/font in layout.tsx)
const legacyCssFiles = [
  "site/assets/tokens.css",
  "site/assets/commit.css",
  "site/assets/ring.css",
  "site/assets/deck.css",
  "site/style.css",
];
let combined = "/* Auto-generated from site/ CSS in @layer legacy */\n@layer legacy {\n";
for (const rel of legacyCssFiles) {
  const full = path.join(ROOT, rel);
  if (fs.existsSync(full)) {
    const raw = fs.readFileSync(full, "utf8").replace(/@import\s+url\([^)]+\);?/g, "");
    combined += `\n/* --- ${rel} --- */\n` + raw + "\n";
  }
}
combined += "\n}\n";
fs.writeFileSync(path.join(ROOT, "app", "legacy-bundle.css"), combined, "utf8");

console.log(`[sync-public-assets] Synced ${total} static assets + built app/legacy-bundle.css`);
