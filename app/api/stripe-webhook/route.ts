import { invokeLegacyHandler } from "@/lib/legacy-api-adapter";
import handler from "../../../funnel/api/stripe-webhook.js";

export const runtime = "nodejs";

export async function POST(req: Request) {
  return invokeLegacyHandler(req, handler, { rawStream: true });
}
