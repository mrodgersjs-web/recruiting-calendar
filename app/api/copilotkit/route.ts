import {
  CopilotRuntime,
  ExperimentalEmptyAdapter,
  copilotRuntimeNextJSAppRouterEndpoint,
} from "@copilotkit/runtime";
import {
  AbstractAgent,
  EventType,
  type BaseEvent,
  type Message,
  type RunAgentInput,
} from "@ag-ui/client";
import { createOpenAI } from "@ai-sdk/openai";
import { gateway } from "ai";
import { streamText, type ModelMessage } from "ai";
import { Observable } from "rxjs";
import { checkIpRateLimit } from "@/lib/rate-limit";
import {
  commitBookAgentService,
  type AnswerTurn,
} from "@/lib/copilotkit-service";

export const runtime = "nodejs";
export const maxDuration = 60;

const AGENT_ID = "commit_book_guide";
const AGENT_DESCRIPTION =
  "Commit Book recruiting guide. Answers NCAA, NAIA, and NJCAA recruiting questions from the site knowledge base, unpublished internal research drafts, and approved public pages only.";

function getClientIp(req: Request): string {
  const forwarded = req.headers.get("x-forwarded-for");
  if (forwarded) {
    const first = forwarded.split(",")[0]?.trim();
    if (first) return first;
  }
  const realIp = req.headers.get("x-real-ip")?.trim();
  if (realIp) return realIp;
  return "127.0.0.1";
}

function messageText(message: Message): string {
  if (!("content" in message) || message.content == null) return "";
  const content = message.content;
  if (typeof content === "string") return content;
  if (!Array.isArray(content)) return "";
  return content
    .map((part) => {
      if (part && typeof part === "object" && "text" in part && typeof part.text === "string") {
        return part.text;
      }
      return "";
    })
    .join(" ")
    .trim();
}

function toTurns(messages: Message[]): AnswerTurn[] {
  const turns: AnswerTurn[] = [];
  for (const message of messages) {
    if (message.role !== "user" && message.role !== "assistant") continue;
    const content = messageText(message).trim();
    if (!content) continue;
    turns.push({ role: message.role, content });
  }
  return turns.slice(-10);
}

class CommitBookAgUiAgent extends AbstractAgent {
  constructor() {
    super({
      agentId: AGENT_ID,
      description: AGENT_DESCRIPTION,
    });
  }

  override clone(): CommitBookAgUiAgent {
    const next = new CommitBookAgUiAgent();
    next.middlewares = [...this.middlewares];
    return next;
  }

  run(input: RunAgentInput): Observable<BaseEvent> {
    return new Observable<BaseEvent>((subscriber) => {
      const abort = new AbortController();
      void this.execute(input, subscriber, abort.signal);
      return () => abort.abort();
    });
  }

  private async execute(
    input: RunAgentInput,
    subscriber: { next: (event: BaseEvent) => void; complete: () => void },
    signal: AbortSignal
  ): Promise<void> {
    const threadId = input.threadId;
    const runId = input.runId;
    subscriber.next({ type: EventType.RUN_STARTED, threadId, runId });
    const messageId = `msg_${crypto.randomUUID()}`;
    try {
      const plan = await commitBookAgentService.prepareAnswer(toTurns(input.messages ?? []));
      subscriber.next({ type: EventType.TEXT_MESSAGE_START, messageId, role: "assistant" });
      if (plan.directText) {
        subscriber.next({ type: EventType.TEXT_MESSAGE_CONTENT, messageId, delta: plan.directText });
      } else {
        await this.streamModel(plan.system, plan.turns, messageId, subscriber, signal);
      }
      subscriber.next({ type: EventType.TEXT_MESSAGE_END, messageId });
      subscriber.next({ type: EventType.RUN_FINISHED, threadId, runId });
      subscriber.complete();
    } catch (error) {
      if (signal.aborted) {
        subscriber.complete();
        return;
      }
      const message = error instanceof Error ? error.message : "The recruiting guide failed to answer.";
      subscriber.next({
        type: EventType.RUN_ERROR,
        message,
        code: "agent_error",
      });
      subscriber.complete();
    }
  }

  private async streamModel(
    system: string,
    turns: AnswerTurn[],
    messageId: string,
    subscriber: { next: (event: BaseEvent) => void },
    signal: AbortSignal
  ): Promise<void> {
    const apiKey = process.env.OPENAI_API_KEY?.trim();
    const modelId = process.env.OPENAI_MODEL?.trim() || "openai/gpt-4o";
    let model;
    if (apiKey) {
      const baseURL = process.env.OPENAI_BASE_URL?.trim() || undefined;
      const openai = createOpenAI({
        apiKey,
        ...(baseURL ? { baseURL } : {}),
      });
      model = baseURL ? openai.chat(modelId) : openai(modelId);
    } else {
      model = gateway(modelId);
    }
    const messages: ModelMessage[] = turns.map((turn) => ({
      role: turn.role,
      content: turn.content,
    }));
    const result = streamText({
      model,
      system,
      messages,
      maxOutputTokens: 700,
      temperature: 0.2,
      abortSignal: signal,
    });
    let wrote = false;
    for await (const delta of result.textStream) {
      if (!delta) continue;
      wrote = true;
      subscriber.next({ type: EventType.TEXT_MESSAGE_CONTENT, messageId, delta });
    }
    if (!wrote) {
      subscriber.next({
        type: EventType.TEXT_MESSAGE_CONTENT,
        messageId,
        delta:
          "I could not ground an answer from the recruiting sources just now. Open the Athlete SOP Playbooks at /sops or the window calculator at /window.",
      });
    }
  }
}

const serviceAdapter = new ExperimentalEmptyAdapter();
const copilotRuntime = new CopilotRuntime({
  agents: {
    default: new CommitBookAgUiAgent(),
    [AGENT_ID]: new CommitBookAgUiAgent(),
  },
});

async function handle(req: Request): Promise<Response> {
  const ip = getClientIp(req);
  const forceRateLimit =
    process.env.NODE_ENV !== "production" &&
    req.headers.get("x-commitbook-test-ratelimit") === "1";
  const rl = forceRateLimit
    ? { allowed: false, limit: 15, remaining: 0, retryAfterSec: 45 }
    : checkIpRateLimit(ip);

  if (!rl.allowed) {
    return Response.json(
      {
        error: "rate_limited",
        message: `Too many questions from this connection. Please wait ${rl.retryAfterSec} seconds or open the Athlete SOP Playbooks directly at /sops.`,
        retryAfterSec: rl.retryAfterSec,
      },
      {
        status: 429,
        headers: {
          "Retry-After": String(rl.retryAfterSec),
          "X-RateLimit-Limit": String(rl.limit),
          "X-RateLimit-Remaining": "0",
        },
      }
    );
  }

  if (req.method === "POST" && !process.env.OPENAI_API_KEY?.trim()) {
    // Vercel AI Gateway resolves OIDC inside the function; only the pure-local
    // dev case without any gateway credentials should 503 early.
    if (process.env.VERCEL !== "1" && !process.env.AI_GATEWAY_API_KEY) {
    return Response.json(
      {
        error: "provider_not_configured",
        message:
          "Live AI answers are awaiting model configuration on this environment. You can use the Athlete SOP Playbooks (/sops) and 30-Second Window Calculator (/window) right now.",
      },
      { status: 503 }
    );
    }
  }

  const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
    runtime: copilotRuntime,
    serviceAdapter,
    endpoint: "/api/copilotkit",
  });
  const response = await handleRequest(req);
  response.headers.set("X-RateLimit-Limit", String(rl.limit));
  response.headers.set("X-RateLimit-Remaining", String(rl.remaining));
  return response;
}

export const POST = handle;
export const GET = handle;
