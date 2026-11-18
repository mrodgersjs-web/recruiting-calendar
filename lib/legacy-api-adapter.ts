import { EventEmitter } from "node:events";

type LegacyHandler = (req: unknown, res: unknown) => Promise<unknown> | unknown;

export async function invokeLegacyHandler(
  request: Request,
  handler: LegacyHandler,
  options?: { rawStream?: boolean }
): Promise<Response> {
  const url = new URL(request.url);
  const query = Object.fromEntries(url.searchParams.entries());
  const headersObj: Record<string, string> = {};
  request.headers.forEach((v, k) => {
    headersObj[k.toLowerCase()] = v;
  });

  const rawText =
    request.method === "GET" || request.method === "HEAD"
      ? ""
      : await request.text();

  const emitter = new EventEmitter();
  let parsedBody: unknown = rawText;
  if (!options?.rawStream && rawText) {
    try {
      parsedBody = JSON.parse(rawText);
    } catch {
      parsedBody = rawText;
    }
  }

  const req = Object.assign(emitter, {
    method: request.method,
    url: url.pathname + url.search,
    headers: headersObj,
    query,
    body: parsedBody,
  });

  let statusCode = 200;
  const outHeaders = new Headers();
  let responseBody: BodyInit | null = null;

  const res = {
    status(code: number) {
      statusCode = code;
      return res;
    },
    setHeader(key: string, val: string) {
      outHeaders.set(key, String(val));
      return res;
    },
    json(payload: unknown) {
      if (!outHeaders.has("Content-Type")) {
        outHeaders.set("Content-Type", "application/json; charset=utf-8");
      }
      responseBody = JSON.stringify(payload);
      return res;
    },
    send(payload: unknown) {
      if (Buffer.isBuffer(payload) || payload instanceof Uint8Array) {
        responseBody = new Uint8Array(payload);
      } else if (typeof payload === "string") {
        responseBody = payload;
      } else if (payload !== undefined && payload !== null) {
        responseBody = JSON.stringify(payload);
      }
      return res;
    },
    end(payload?: string) {
      if (payload !== undefined) responseBody = payload;
      return res;
    },
  };

  const promise = Promise.resolve(handler(req, res));
  if (options?.rawStream) {
    queueMicrotask(() => {
      if (rawText) emitter.emit("data", rawText);
      emitter.emit("end");
    });
  }
  await promise;

  return new Response(responseBody, {
    status: statusCode,
    headers: outHeaders,
  });
}
