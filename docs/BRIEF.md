# Commit Book Guide

A grounded recruiting chatbot on The Commit Book site, for athletes and parents who need NCAA, NAIA, and NJCAA answers without a sales pitch. v1.1. Decided from the landed integration, not a new interview.

## Replaces

The v1.0 Kokonut guide that answered only from a sliced local knowledge base. v1.1 adds a second runtime that can also read unpublished reel drafts and a fixed list of public pages. The visible panel is still the v1.0 Kokonut composer.

## Main jobs

1. Answer an in-scope recruiting question from the site knowledge base, and point to a real site path such as `/sops` or `/window`.
2. When the question is about film or a sport with a review draft, use that draft and cite it as unpublished.
3. Refuse off-topic questions, prompt extraction, and any request to paste an unpublished draft.

## Data

- Site knowledge base: `content/kb.md` and the section loader in `lib/kb.ts`. Citation: "Commit Book knowledge base".
- Internal reel drafts: five text files under `content/reels/` (basketball, fastpitch softball, football, volleyball, baseball). Citation must be the exact phrase "internal research draft, not published". No file path, no URL, no full paste. Not a public source.
- Approved web: https pages on `ncaa.org`, `naia.org`, `njcaa.org`, and `recruiting-calendar.vercel.app` only. Other hosts are rejected.

## Shape

A sheet on the existing Next.js 15 site, not a Mac app. Paper `#f7f5f0`, ink `#141413`, link `#1d4ed8`. Works only with a network for live answers. No accounts. Offline fallback is the SOP hub and the window calculator.

## Architecture

- Runtime: `app/api/copilotkit/route.ts`. `CopilotRuntime` from `@copilotkit/runtime` 1.89.0, agent id `commit_book_guide`, `ExperimentalEmptyAdapter`.
- AG-UI: `CommitBookAgUiAgent` extends `AbstractAgent` from `@ag-ui/client` 1.0.5 and emits run and text events.
- Model: Vercel AI SDK `streamText` (`ai` ^6) through `@ai-sdk/openai` `createOpenAI`. Cap 700 output tokens, temperature 0.2. Same IP rate limit as `/api/chat`.
- Retrieval: `lib/copilotkit-service.ts` and `lib/content-search.ts`.
- vercel-labs/ui: `@ui-sdk/react` and `@ui-sdk/core` at `0.1.0-beta.10` are installed. Nothing imports them. A3's chrome-only adopt (Dialog, Accordion, TriggerMenu, Textarea) is not in the components. Do not replace the Kokonut message list. `@copilotkit/react-core` and `@copilotkit/react-ui` are installed and also unused. The launcher still talks to `/api/chat`.

## Env vars

Names only. No values belong in the repo.

- `OPENAI_API_KEY`: required for a live answer. Missing key returns HTTP 503 `provider_not_configured`.
- `OPENAI_BASE_URL`: optional. Unset uses the provider default.
- `OPENAI_MODEL`: optional. Default `gpt-4o-mini`.
- `CHAT_RATE_LIMIT_PER_MIN`: optional. Default 15.
- `KB_CHAR_BUDGET`: optional. Default 15000. Used by the site knowledge loader.
- `COMMIT_BOOK_SITE_ORIGIN`: optional. Default `https://recruiting-calendar.vercel.app`.
- `COPILOTKIT_TELEMETRY_DISABLED`: set `true` to opt out. The 2026-11-18 build logged telemetry as on.

## System hooks

None. No menu bar, no global shortcut, no CLI. The page dispatches `commitbook:ask` and `commitbook:open`.

## Reference

Kokonut `AI_Prompt` for the composer. vercel-labs/ui is headless chrome only, and it is not wired. AI Elements was considered and rejected for this version.

## Look

Site tokens already on the launcher. Not a new brand. A6 measured contrast failures on the placeholder (2.43:1) and slash descriptions (2.82:1), and a dialog that claims `aria-modal` without trapping focus.

## Not in version one

- Checkout, Stripe, email capture, or any paid path.
- Publishing reel drafts, or treating a draft as a live playbook.
- Replacing `useChat` or the Kokonut thread with CopilotKit React or with AI Elements.
- Production alias, public push, or writing `OPENAI_API_KEY` onto Vercel. Those still need a separate approval.
- A green end-to-end run. The Playwright harness failed 7/7 on 2026-11-18 because each worker picked a port nothing was listening on.
