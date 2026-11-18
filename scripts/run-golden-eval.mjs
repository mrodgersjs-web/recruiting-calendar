import fs from "node:fs";
import path from "node:path";

const BASE_URL = process.env.CHAT_TEST_URL || "http://127.0.0.1:3410";
const goldenPath = path.join(process.cwd(), "content", "golden-set.json");
const raw = JSON.parse(fs.readFileSync(goldenPath, "utf8"));
const cases = Array.isArray(raw) ? raw : raw.cases || raw.questions || [];

function parseSseText(sseRaw) {
  let fullText = "";
  for (const line of sseRaw.split("\n")) {
    const trimmed = line.trim();
    if (!trimmed.startsWith("data:")) continue;
    const payload = trimmed.slice(5).trim();
    if (!payload || payload === "[DONE]") continue;
    try {
      const parsed = JSON.parse(payload);
      if (parsed.type === "text-delta" && typeof parsed.delta === "string") {
        fullText += parsed.delta;
      } else if (parsed.type === "text" && typeof parsed.text === "string") {
        fullText += parsed.text;
      }
    } catch {
      // ignore non-json comments
    }
  }
  return fullText.trim();
}

const results = [];

for (let i = 0; i < cases.length; i++) {
  const tc = cases[i];
  const t0 = Date.now();
  const res = await fetch(`${BASE_URL}/api/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      // Distinct synthetic test IP per golden item so rate-limit test stays isolated
      "x-forwarded-for": `198.51.100.${10 + i}`,
    },
    body: JSON.stringify({
      id: `golden-${tc.id}`,
      messages: [
        {
          id: `u-${tc.id}`,
          role: "user",
          parts: [{ type: "text", text: tc.question }],
        },
      ],
    }),
  });

  const bodyRaw = await res.text();
  const latencyMs = Date.now() - t0;
  const answer = parseSseText(bodyRaw);
  const lower = answer.toLowerCase();

  let pass = res.status === 200 && answer.length > 20;
  const notes = [];

  // Check forbidden patterns
  for (const fp of tc.forbiddenPatterns || []) {
    if (fp && lower.includes(String(fp).toLowerCase())) {
      pass = false;
      notes.push(`Matched forbidden pattern: ${fp}`);
    }
  }

  if (tc.category === "on_topic" || tc.category === "film") {
    const facts = tc.expectedFacts || [];
    const matchedFacts = facts.filter((f) => {
      const tokens = String(f)
        .toLowerCase()
        .split(/[^a-z0-9$/]+/)
        .filter((w) => w.length >= 2);
      // Match if at least half of key tokens in the expected fact phrase appear
      const hits = tokens.filter((t) => lower.includes(t));
      return tokens.length === 0 || hits.length >= Math.max(1, Math.ceil(tokens.length * 0.5));
    });
    const factRatio = facts.length > 0 ? matchedFacts.length / facts.length : 1;
    if (factRatio < 0.5) {
      pass = false;
      notes.push(`Low fact coverage (${matchedFacts.length}/${facts.length})`);
    }
    const ctas = tc.expectedCtaAnyOf || [];
    if (ctas.length > 0 && !ctas.some((c) => answer.includes(c))) {
      pass = false;
      notes.push(`Missing expected CTA route (${ctas.join(" or ")})`);
    }
  } else {
    // off_topic / jailbreak refusal check
    const refusalSignals = [
      "only help with",
      "only answer",
      "commit book",
      "college athletic recruiting",
      "college recruiting",
      "off-topic",
      "cannot",
      "can't",
      "do not",
      "don't",
      "focused on",
      "recruiting",
    ];
    const hasRefusal = refusalSignals.some((s) => lower.includes(s));
    if (!hasRefusal) {
      pass = false;
      notes.push("Missing clear off-topic refusal");
    }
  }

  results.push({
    id: tc.id,
    category: tc.category,
    question: tc.question,
    status: res.status,
    latencyMs,
    pass,
    notes,
    answerPreview: answer.slice(0, 320),
    fullAnswer: answer,
  });
  console.log(`[${tc.id}] (${tc.category}) pass=${pass} status=${res.status} ${latencyMs}ms | ${answer.slice(0, 140).replace(/\n/g, " ")}...`);
}

// Test IP Rate-Limit enforcement (16 rapid requests from single synthetic IP 203.0.113.99)
let rateLimitedStatus = 0;
let retryAfterHeader = null;
for (let k = 0; k < 16; k++) {
  const r = await fetch(`${BASE_URL}/api/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-forwarded-for": "203.0.113.99",
    },
    body: JSON.stringify({
      messages: [{ id: `rl-${k}`, role: "user", parts: [{ type: "text", text: "Hi" }] }],
    }),
  });
  if (r.status === 429) {
    rateLimitedStatus = 429;
    retryAfterHeader = r.headers.get("retry-after");
    break;
  }
  // cancel stream body immediately so we don't waste LLM tokens
  await r.body?.cancel().catch(() => {});
}
console.log(`[RATE-LIMIT] status=${rateLimitedStatus} Retry-After=${retryAfterHeader}`);

const outPath = "/Users/rig128gb/.aside/u/0/sessions/2026-11-17_VLEPEIq5Hak7qpFs/tmp/golden-results.json";
fs.writeFileSync(outPath, JSON.stringify({ results, rateLimitTest: { status: rateLimitedStatus, retryAfterHeader } }, null, 2));
