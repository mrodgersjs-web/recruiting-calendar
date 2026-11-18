import { invokeLegacyHandler } from "@/lib/legacy-api-adapter";
import handler from "../../../funnel/api/portal.js";

export const runtime = "nodejs";

export async function GET(req: Request) {
  return invokeLegacyHandler(req, handler);
}

export async function POST(req: Request) {
  return invokeLegacyHandler(req, handler);
}
