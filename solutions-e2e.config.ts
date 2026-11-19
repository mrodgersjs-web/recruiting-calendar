import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests",
  testMatch: "solutions.spec.ts",
  fullyParallel: false,
  workers: 1,
  timeout: 60_000,
  expect: { timeout: 15_000 },
  reporter: [["list"]],
  use: {
    baseURL: "http://127.0.0.1:32123",
    viewport: { width: 1280, height: 900 },
    trace: "retain-on-failure",
    screenshot: "only-on-failure",
  },
  webServer: {
    command: "npm run build && npm run start -- --port 32123",
    cwd: ".",
    url: "http://127.0.0.1:32123/solutions",
    timeout: 180_000,
    reuseExistingServer: false,
    env: {
      OPENAI_API_KEY: "",
      OPENROUTER_API_KEY: "",
      ANTHROPIC_API_KEY: "",
      AI_GATEWAY_API_KEY: "",
      VERCEL_OIDC_TOKEN: "",
    },
  },
});
