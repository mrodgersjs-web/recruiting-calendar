import { defineConfig, devices } from "@playwright/test";

/**
 * Plain Playwright config for the Commit Book chatbot.
 *
 * Ports are fixed so every Playwright worker re-evaluates this file against
 * the same servers `.e2e/dev-server.mjs` started. A freePort() at module load
 * handed each worker a different pair and the tests never reached the app.
 *
 *   npx playwright test --config=e2e.config.ts
 *
 * 32110: next with a dummy OPENAI_API_KEY pointed at `.e2e/openai-stub.mjs`
 * 32111: next with OPENAI_API_KEY stripped, so the real 503 path renders
 */
const stubAppPort = "32110";
const nokeyPort = "32111";
const only = process.env.COMMITBOOK_E2E_ONLY;
const runStub = only !== "nokey";
const runNokey = only !== "stub";

export default defineConfig({
  testDir: "./tests",
  testMatch: "chatbot.spec.ts",
  fullyParallel: false,
  forbidOnly: true,
  retries: 0,
  workers: 1,
  timeout: 90_000,
  expect: { timeout: 25_000 },
  reporter: [["list"]],
  use: {
    trace: "retain-on-failure",
    screenshot: "only-on-failure",
  },
  projects: [
    ...(runStub
      ? [
          {
            name: "stub",
            grep: /@stub/,
            use: {
              ...devices["Desktop Chrome"],
              baseURL: `http://127.0.0.1:${stubAppPort}`,
            },
          },
        ]
      : []),
    ...(runNokey
      ? [
          {
            name: "nokey",
            grep: /@nokey/,
            use: {
              ...devices["Desktop Chrome"],
              baseURL: `http://127.0.0.1:${nokeyPort}`,
            },
          },
        ]
      : []),
  ],
  webServer: {
    command: "node .e2e/dev-server.mjs",
    cwd: ".",
    url: `http://127.0.0.1:${runStub ? stubAppPort : nokeyPort}`,
    timeout: 180_000,
    reuseExistingServer: false,
    env: {
      COMMITBOOK_E2E_MODE: only === "nokey" ? "nokey" : only === "stub" ? "stub" : "both",
      COMMITBOOK_E2E_PORT: stubAppPort,
      COMMITBOOK_E2E_PORT_NOKEY: nokeyPort,
    },
  },
});
