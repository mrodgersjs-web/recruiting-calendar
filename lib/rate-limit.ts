interface Bucket {
  timestamps: number[];
}

const store = new Map<string, Bucket>();

const DEFAULT_WINDOW_MS = 60_000;
const DEFAULT_MAX_REQUESTS = 15;

export interface RateLimitResult {
  allowed: boolean;
  limit: number;
  remaining: number;
  retryAfterSec: number;
}

export function checkIpRateLimit(
  ip: string,
  options?: { windowMs?: number; maxRequests?: number }
): RateLimitResult {
  const windowMs = options?.windowMs ?? DEFAULT_WINDOW_MS;
  const maxRequests =
    options?.maxRequests ??
    (Number(process.env.CHAT_RATE_LIMIT_PER_MIN) > 0
      ? Number(process.env.CHAT_RATE_LIMIT_PER_MIN)
      : DEFAULT_MAX_REQUESTS);

  const now = Date.now();
  const cutoff = now - windowMs;
  const key = ip || "anonymous";

  // Periodic cleanup to avoid unbounded memory growth
  if (store.size > 2000) {
    for (const [k, bucket] of store.entries()) {
      const active = bucket.timestamps.filter((t) => t > cutoff);
      if (active.length === 0) store.delete(k);
      else bucket.timestamps = active;
    }
  }

  const existing = store.get(key) ?? { timestamps: [] };
  existing.timestamps = existing.timestamps.filter((t) => t > cutoff);

  if (existing.timestamps.length >= maxRequests) {
    const oldest = existing.timestamps[0] ?? now;
    const retryAfterSec = Math.max(1, Math.ceil((oldest + windowMs - now) / 1000));
    store.set(key, existing);
    return {
      allowed: false,
      limit: maxRequests,
      remaining: 0,
      retryAfterSec,
    };
  }

  existing.timestamps.push(now);
  store.set(key, existing);
  return {
    allowed: true,
    limit: maxRequests,
    remaining: Math.max(0, maxRequests - existing.timestamps.length),
    retryAfterSec: 0,
  };
}
