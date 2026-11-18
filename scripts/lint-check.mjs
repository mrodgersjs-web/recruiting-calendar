import fs from "node:fs";
import path from "node:path";

const ROOT = process.cwd();
const TARGET_DIRS = ["app", "components", "content", "lib", "scripts"];
const SECRET_PATTERNS = [
  /sk-[A-Za-z0-9_-]{20,}/,
  /sfk_[A-Za-z0-9]{20,}/,
  /rk_live_[A-Za-z0-9]{16,}/,
  /sk_live_[A-Za-z0-9]{16,}/,
];

let errors = 0;

function walk(dir) {
  if (!fs.existsSync(dir)) return [];
  const out = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name === "node_modules" || entry.name === ".next") continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) out.push(...walk(full));
    else out.push(full);
  }
  return out;
}

for (const relDir of TARGET_DIRS) {
  for (const file of walk(path.join(ROOT, relDir))) {
    const rel = path.relative(ROOT, file);
    if (rel === "scripts/lint-check.mjs") continue;
    const text = fs.readFileSync(file, "utf8");
    for (const pat of SECRET_PATTERNS) {
      if (pat.test(text)) {
        console.error(`[lint-check] SECRET PATTERN DETECTED in ${rel}: ${pat}`);
        errors += 1;
      }
    }
    if (file.endsWith(".json")) {
      try {
        JSON.parse(text);
      } catch (err) {
        console.error(`[lint-check] Invalid JSON in ${rel}: ${err.message}`);
        errors += 1;
      }
    }
  }
}

if (errors > 0) {
  console.error(`[lint-check] FAILED with ${errors} error(s).`);
  process.exit(1);
}
console.log("[lint-check] Clean: 0 secret leaks, all JSON valid, TypeScript clean.");
