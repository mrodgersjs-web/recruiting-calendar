import fs from "node:fs";
import path from "node:path";

export interface KbSection {
  id: string;
  label: string;
  text: string;
  tags: string[];
  always?: boolean;
}

const SOURCE_FILES: { rel: string; prefix: string }[] = [
  { rel: "content/kb.md", prefix: "kb" },
  { rel: "content/reels.md", prefix: "reel" },
  { rel: "content/reels/Commit-Book-Highlight-Reel-Playbook_Football_Review_v3.txt", prefix: "reel-fb" },
  { rel: "content/reels/Commit-Book-Highlight-Reel-Playbook_Volleyball_Review_v3.txt", prefix: "reel-vb" },
  { rel: "content/reels/Commit-Book-Mens-Baseball-Highlight-Reel-Research-Report_v1.txt", prefix: "reel-bb" },
  { rel: "content/reels/Commit-Book-Basketball-Highlight-Reel-Research-Report_v1.txt", prefix: "reel-bk" },
  { rel: "content/reels/Commit-Book-Fastpitch-Softball-Highlight-Reel-Research-Report_v1.txt", prefix: "reel-sb" },
  { rel: "content/sops/football-and-boys-basketball.md", prefix: "sopfb" },
  { rel: "content/sops/girls-basketball-and-volleyball.md", prefix: "sopgv" },
];

function readIfExists(relPath: string): string {
  const full = path.join(process.cwd(), relPath);
  if (!fs.existsSync(full)) return "";
  return fs.readFileSync(full, "utf8");
}

const TAG_KEYWORDS: Record<string, string[]> = {
  film: [
    "film", "reel", "video", "highlight", "camera", "tripod", "angle", "clip",
    "footage", "editing", "edit", "hudl", "youtube", "radar", "measurable",
    "music", "slow motion", "montage", "title card", "duration",
  ],
  football: ["football", "quarterback", "wide receiver", "linebacker", "safety", "lineman", "kicker", "punter", "snapper", "all-22"],
  basketball: ["basketball", "point guard", "shooting guard", "forward", "center", "aau", "free throw", "layup", "pick-and-roll"],
  volleyball: ["volleyball", "setter", "libero", "outside hitter", "middle blocker", "opposite", "rally", "serve receive", "dig", "spike", "jva"],
  baseball: ["baseball", "pitcher", "pitching", "batter", "hitting", "infield", "outfield", "catcher", "radar gun", "pop time", "bbcor", "usabat", "wood bat", "bullpen"],
  softball: ["softball", "fastpitch", "circle", "dugout", "nfhs", "pickoff", "43-foot", "60-foot"],
  pricing: ["price", "cost", "pricing", "refund", "billing", "subscription", "renewal", "free", "trial", "checkout", "pay"],
  offers: ["offer", "tool", "audit", "diagnostic", "teardown", "waitlist", "walk-on", "nil", "eligibility center", "jucо", "transfer"],
  camps: ["camp", "showcase", "combine", "invite", "fee", "red flag", "money trap"],
  calendar: ["calendar", "window", "contact", "dead period", "quiet period", "evaluation", "when can", "date", "timeline", "off-campus", "junior", "sophomore", "senior", "class of"],
  eligibility: ["eligibility", "core course", "10/7", "gpa", "transcript", "counselor", "sat", "act", "ncaa", "naia", "njcaa", "division", "d1", "d2", "d3", "bylaw"],
  aid: ["scholarship", "aid", "financial", "money", "tuition", "grant", "walk on", "walk-on", "full ride", "partial", "roster cap", "105", "85", "11.7"],
  outreach: ["email", "emailing", "contact coach", "write", "dm", "message", "reply", "response", "silence", "ignored", "recruiting service", "profile"],
  sop: ["sop", "playbook", "step", "checklist", "grade", "month", "plan", "road to college"],
  site: ["website", "site", "page", "account", "login", "support", "how do i", "where do i"],
};

let sectionCache: KbSection[] | null = null;

function tagFor(label: string, text: string): string[] {
  const hay = (label + " " + text).toLowerCase();
  const tags: string[] = [];
  for (const [tag, kws] of Object.entries(TAG_KEYWORDS)) {
    if (kws.some((k) => hay.includes(k))) tags.push(tag);
  }
  return tags;
}

function buildSections(): KbSection[] {
  if (sectionCache) return sectionCache;
  const sections: KbSection[] = [];

  for (const { rel, prefix } of SOURCE_FILES) {
    const raw = readIfExists(rel);
    if (!raw.trim()) continue;
    const parts = raw.split(/^(#{2,3}) /m);
    const preamble = parts[0] ?? "";
    if (preamble.trim().length > 40) {
      const label = preamble.trim().split("\n")[0].slice(0, 90);
      sections.push({
        id: prefix + "-preamble",
        label,
        text: preamble.trim(),
        tags: tagFor(label + " " + rel, preamble),
        always: prefix === "kb",
      });
    }
    // parts: [pre, "##", body, "###", body, ...]. Track the parent ## heading so
    // ### subsections carry their sport/topic context.
    let parentLabel = "";
    for (let i = 1; i + 1 < parts.length; i += 2) {
      const hashes = parts[i];
      const body = parts[i + 1];
      const nl = body.indexOf("\n");
      const label = (nl === -1 ? body : body.slice(0, nl)).trim().slice(0, 110);
      if (hashes === "##") parentLabel = label;
      const rest = nl === -1 ? "" : body.slice(nl).trimStart();
      const display = hashes === "###" && parentLabel ? `${parentLabel} - ${label}` : label;
      const text = `## ${display}\n${rest}`.trim();
      if (text.length < 60) continue;
      sections.push({
        id: prefix + "-" + i,
        label: display,
        text,
        tags: tagFor(display + " " + rel, body),
      });
    }

    // Any oversized section gets split into page-sized chunks so one big
    // section (a sport SOP or a reel report) never crowds out the others.
    {
      const chunkSize = 3000;
      for (let i = sections.length - 1; i >= 0; i--) {
        const s = sections[i];
        if (s.text.length <= chunkSize * 1.5) continue;
        if (s.always) continue;
        sections.splice(i, 1);
        for (let c = 0; c * chunkSize < s.text.length; c++) {
          const chunk = s.text.slice(c * chunkSize, (c + 1) * chunkSize);
          sections.push({
            id: `${s.id}-c${c}`,
            label: s.label,
            text: chunk,
            tags: s.tags,
          });
        }
      }
    }
  }

  sectionCache = sections;
  return sections;
}

function tokenize(q: string): string[] {
  return q
    .toLowerCase()
    .replace(/[^a-z0-9$./ ]/g, " ")
    .split(/\s+/)
    .filter((w) => w.length > 2)
    .slice(0, 60);
}

function scoreSection(sec: KbSection, qTokens: string[]): number {
  if (!qTokens.length) return 0;
  let score = 0;
  for (const t of sec.tags) {
    const kws = TAG_KEYWORDS[t] ?? [];
    for (const k of kws) {
      if (qTokens.some((qt) => qt.includes(k) || k.includes(qt))) {
        score += 2;
        break;
      }
    }
  }
  const lower = sec.text.toLowerCase();
  const labelLower = sec.label.toLowerCase();
  for (const qt of qTokens) {
    if (qt.length > 4 && lower.includes(qt)) score += 1;
    // Label hits are strong signals: a section titled with the query's sport or
    // topic beats a body mention.
    if (qt.length > 3 && labelLower.includes(qt)) score += 3;
  }
  // Exact number/date phrases from the query (e.g. "2029", "43-foot") are
  // high-precision: reward them separately.
  for (const qt of qTokens) {
    if (/\d/.test(qt) && lower.includes(qt)) score += 2;
  }
  return score;
}

const CHAR_BUDGET = Number(process.env.KB_CHAR_BUDGET ?? 15000);

export function loadCommitBookKnowledgeBase(query = ""): string {
  const sections = buildSections();
  const qTokens = tokenize(query);

  const scored = sections
    .map((sec) => ({ sec, score: sec.always ? 100000 : scoreSection(sec, qTokens) }))
    .sort((a, b) => b.score - a.score);

  // Always include the single best-scoring chunk per section label, plus the
  // top hits overall, so a multi-sport question (football AND volleyball) gets
  // both sports even when one sport's chunks dominate the raw ranking.
  const bestByLabel = new Map<string, { sec: KbSection; score: number }>();
  for (const { sec, score } of scored) {
    if (score <= 0 || score >= 100000) continue;
    const prev = bestByLabel.get(sec.label);
    if (!prev || score > prev.score) bestByLabel.set(sec.label, { sec, score });
  }
  const diverse = [...bestByLabel.values()].sort((a, b) => b.score - a.score);

  const picked: KbSection[] = [];
  let chars = 0;
  const always = scored.filter(({ score }) => score >= 100000);
  for (const { sec } of always) {
    picked.push(sec);
    chars += sec.text.length;
  }
  // First pass: one best chunk per distinct section label (coverage).
  const pickedIds = new Set(picked.map((s) => s.id));
  for (const { sec } of diverse) {
    if (pickedIds.has(sec.id)) continue;
    if (chars + sec.text.length > CHAR_BUDGET) continue;
    picked.push(sec);
    pickedIds.add(sec.id);
    chars += sec.text.length;
  }
  // Second pass: fill remaining budget with the highest-scoring chunks (depth).
  for (const { sec, score } of scored) {
    if (score <= 0 || score >= 100000 || pickedIds.has(sec.id)) continue;
    if (chars + sec.text.length > CHAR_BUDGET) continue;
    picked.push(sec);
    pickedIds.add(sec.id);
    chars += sec.text.length;
  }

  if (picked.length === 0) {
    const fallback = sections.filter((s) => s.always).concat(sections.slice(0, 2));
    return fallback.map((s) => s.text.slice(0, 4000)).join("\n\n---\n\n");
  }

  return picked.map((s) => s.text).join("\n\n---\n\n");
}

export function kbStats() {
  const sections = buildSections();
  return {
    sections: sections.length,
    totalChars: sections.reduce((n, s) => n + s.text.length, 0),
  };
}
