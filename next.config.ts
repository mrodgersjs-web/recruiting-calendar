import path from "node:path";
import { fileURLToPath } from "node:url";
import type { NextConfig } from "next";

const projectRoot = path.dirname(fileURLToPath(import.meta.url));

const nextConfig: NextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,
  outputFileTracingRoot: projectRoot,
  // The chat routes read content/ from disk at runtime; force-trace those files
  // into the serverless function bundles or the KB silently reads as empty.
  outputFileTracingIncludes: {
    "/api/chat": ["./content/**/*"],
    "/api/copilotkit": ["./content/**/*"],
  },
  eslint: {
    ignoreDuringBuilds: false,
  },
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
