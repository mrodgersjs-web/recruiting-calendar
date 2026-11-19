import { expect, test } from "@playwright/test";
import fs from "node:fs/promises";

const slugs = [
  "next-30-days",
  "camp-decision-receipt",
  "film-outreach-brief",
  "family-recruiting-receipt",
  "offer-aid-comparison",
  "program-fit-check",
] as const;

const titles: Record<(typeof slugs)[number], string> = {
  "next-30-days": "Your Next 30 Days",
  "camp-decision-receipt": "Camp Decision Receipt",
  "film-outreach-brief": "Film + Outreach Brief",
  "family-recruiting-receipt": "Family Recruiting Receipt",
  "offer-aid-comparison": "Offer + Aid Comparison",
  "program-fit-check": "Program Fit Red-Flag Check",
};

test("catalog links all six tools", async ({ page }) => {
  await page.goto("/solutions");
  await expect(page.getByRole("heading", { level: 1 })).toContainText("Tools for the next recruiting decision");
  for (const slug of slugs) await expect(page.locator(`a[href="/solutions/${slug}"]`)).toBeVisible();
});

for (const slug of slugs) {
  test(`${slug} renders and stays within a 390px viewport`, async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto(`/solutions/${slug}`);
    await expect(page.getByRole("heading", { level: 1 })).toHaveText(titles[slug]);
    const sizes = await page.evaluate(() => ({ scroll: document.documentElement.scrollWidth, client: document.documentElement.clientWidth }));
    expect(sizes.scroll).toBeLessThanOrEqual(sizes.client);
    await expect(page.getByRole("button", { name: /build my plan|evaluate this camp|create my brief|save receipt|compare programs|review the evidence/i }).first()).toBeVisible();
  });
}

test("Next 30 Days changes the primary action and links to the exact tool", async ({ page }) => {
  await page.goto("/solutions/next-30-days");
  await page.getByLabel("What do you need first?").selectOption("camp");
  await page.getByRole("button", { name: "Build my plan" }).click();
  await expect(page.getByRole("heading", { name: "Run the camp decision check" })).toBeVisible();
  await expect(page.getByRole("link", { name: "Open Camp Decision Receipt" })).toHaveAttribute("href", "/solutions/camp-decision-receipt");
  const result = await page.getByRole("heading", { name: /Class of 2029: the next three actions/ }).locator("..").innerText();
  expect(result).not.toMatch(/\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d/);
  expect(await page.evaluate(() => localStorage.getItem("commitbook.family-recruiting-receipt.v1"))).toBeNull();
});

test("Camp Receipt keeps unknowns visible, calculates cost, and never CONSIDERs unverified attendance", async ({ page }) => {
  const requests: string[] = [];
  await page.goto("/solutions/camp-decision-receipt");
  page.on("request", (request) => {
    const frameworkRead = request.url().includes("/_next/") || request.url().includes("_rsc=");
    if (["fetch", "xhr"].includes(request.resourceType()) && !frameworkRead) requests.push(request.url());
  });
  await page.getByLabel("Camp fee").fill("600");
  await page.getByLabel("Travel and lodging cost").fill("200");
  await page.getByLabel("Evaluation format").fill("Live games and measured skills");
  await page.getByLabel("Refund terms").selectOption("written");
  await page.getByLabel("Film terms").selectOption("included");
  await page.getByRole("button", { name: "Evaluate this camp" }).click();
  await expect(page.getByRole("heading", { name: "NEED MORE INFO" })).toBeVisible();
  await expect(page.getByText("Total entered cost: $800")).toBeVisible();
  await page.getByLabel("Relevant coach attendance").selectOption("not-verified");
  await page.getByRole("button", { name: "Evaluate this camp" }).click();
  await expect(page.getByRole("heading", { name: "SKIP" })).toBeVisible();
  await page.getByLabel("Relevant coach attendance").selectOption("verified");
  await page.getByRole("button", { name: "Evaluate this camp" }).click();
  await expect(page.getByRole("heading", { name: "CONSIDER" })).toBeVisible();
  expect(requests).toEqual([]);
  expect(await page.evaluate(() => localStorage.length)).toBe(0);
});

test("Camp Receipt does not turn blank costs into a $0 decision", async ({ page }) => {
  await page.goto("/solutions/camp-decision-receipt");
  await page.getByRole("button", { name: "Evaluate this camp" }).click();
  await expect(page.getByRole("heading", { name: "NEED MORE INFO" })).toBeVisible();
  await expect(page.getByText("No total is shown until both costs are valid numbers.")).toBeVisible();
});

test("Film Brief uses entered evidence and keeps full-game and logged-out checks", async ({ page }) => {
  await page.goto("/solutions/film-outreach-brief");
  await page.getByLabel("Position or event").fill("Outside Hitter");
  await page.getByLabel("Highlight film link").fill("https://example.com/highlight");
  await page.getByLabel("Full-game link (optional fallback)").fill("https://example.com/full-game");
  await page.getByRole("button", { name: "Create my brief" }).click();
  const message = page.getByLabel("Generated coach message");
  await expect(message).toHaveValue(/Class of 2029 Outside Hitter/);
  await expect(message).toHaveValue(/https:\/\/example.com\/highlight/);
  await expect(message).toHaveValue(/https:\/\/example.com\/full-game/);
  await expect(message).not.toHaveValue(/verified measurable/i);
  await expect(page.getByText("I opened the full-game fallback while logged out and confirmed it is ready")).toBeVisible();
  await expect(page.getByText("I opened the highlight link while logged out")).toBeVisible();
  expect(await page.evaluate(() => localStorage.length)).toBe(0);
});

test("Family Receipt persists valid values and exports schema version 1", async ({ page }) => {
  await page.goto("/solutions/family-recruiting-receipt");
  await page.getByLabel("Next family-entered date").fill("2027-01-15");
  await page.getByLabel("Prepared highlight film").check();
  await page.getByRole("button", { name: "Save receipt" }).click();
  await expect(page.getByText("Saved on this device.")).toBeVisible();
  await page.reload();
  await expect(page.getByLabel("Next family-entered date")).toHaveValue("2027-01-15");
  await expect(page.getByLabel("Prepared highlight film")).toBeChecked();
  const downloadEvent = page.waitForEvent("download");
  await page.getByRole("button", { name: "Export JSON" }).click();
  const download = await downloadEvent;
  const file = await download.path();
  expect(file).not.toBeNull();
  const exported = JSON.parse(await fs.readFile(file!, "utf8"));
  expect(exported.schemaVersion).toBe(1);
  expect(exported.nextDate).toBe("2027-01-15");
  expect(exported.tasks).toContain("Prepared highlight film");
});

test("Family Receipt recovers from malformed local storage", async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem("commitbook.family-recruiting-receipt.v1", "{bad-json"));
  await page.goto("/solutions/family-recruiting-receipt");
  await expect(page.getByText("The saved receipt could not be read. A blank receipt is shown.")).toBeVisible();
  await expect(page.getByLabel("Prepared highlight film")).not.toBeChecked();
});

test("Offer Comparison computes blank-as-zero aid and preserves verbal and projected labels", async ({ page }) => {
  await page.goto("/solutions/offer-aid-comparison");
  await page.getByLabel("Program 1", { exact: true }).fill("Example College");
  await page.getByLabel("Program 1 offer status").selectOption("verbal");
  await page.getByLabel("Program 1 totalCost").fill("50000");
  await page.getByLabel("Program 1 athleticAid").fill("20000");
  await page.getByLabel("Program 1 academicAid").fill("5000");
  await page.getByLabel("Program 1 signing date").fill("Family date TBD");
  await page.getByLabel("Program 1 date status").selectOption("projected");
  await page.getByLabel("Program 2", { exact: true }).fill("Second Example College");
  await page.getByLabel("Program 2 offer status").selectOption("verbal");
  await page.getByLabel("Program 2 totalCost").fill("40000");
  await page.getByLabel("Program 2 signing date").fill("Second family date");
  await page.getByLabel("Program 2 date status").selectOption("projected");
  await page.getByRole("button", { name: "Compare programs" }).click();
  const row = page.getByRole("row").filter({ hasText: /^Example College/ }).last();
  await expect(row).toContainText("$25,000");
  await expect(row).toContainText("verbal");
  await expect(row).toContainText("projected");
  await expect(row).toContainText("Need-based: left blank, counted as $0");
  await expect(row).not.toContainText(/binding|written/i);
  const secondRow = page.getByRole("row").filter({ hasText: "Second Example College" }).last();
  await expect(secondRow).toContainText("verbal");
  await expect(secondRow).toContainText("projected");
  await expect(page.getByRole("region", { name: "Program comparison results" })).toHaveClass(/overflow-x-auto/);
  expect(await page.evaluate(() => localStorage.length)).toBe(0);
});

test("Offer Comparison shows raw negative and floored zero", async ({ page }) => {
  await page.goto("/solutions/offer-aid-comparison");
  await page.getByLabel("Program 1", { exact: true }).fill("Overentered Aid College");
  await page.getByLabel("Program 1 totalCost").fill("10000");
  await page.getByLabel("Program 1 athleticAid").fill("12000");
  await page.getByRole("button", { name: "Compare programs" }).click();
  const row = page.getByRole("row").filter({ hasText: "Overentered Aid College" }).last();
  await expect(row).toContainText("Raw result -$2,000");
  await expect(row).toContainText("floored to $0");
});

test("Offer Comparison does not calculate net cost from a blank annual cost", async ({ page }) => {
  await page.goto("/solutions/offer-aid-comparison");
  await page.getByLabel("Program 1", { exact: true }).fill("Missing Cost College");
  await page.getByLabel("Program 1 athleticAid").fill("12000");
  await page.getByRole("button", { name: "Compare programs" }).click();
  const row = page.getByRole("row").filter({ hasText: "Missing Cost College" }).last();
  await expect(row).toContainText("Annual total cost left blank or invalid; no net cost.");
  await expect(row).not.toContainText("floored to $0");
});

test("Program Fit keeps unanswered evidence unknown and quotes concern inputs", async ({ page }) => {
  await page.goto("/solutions/program-fit-check");
  await page.getByRole("button", { name: "Review the evidence" }).click();
  await expect(page.getByText("Unknowns, not passes")).toBeVisible();
  await expect(page.getByText(/Roster retention: No assessment entered/)).toBeVisible();
  await page.getByLabel("Roster retention evidence assessment").selectOption("concern");
  await page.getByLabel("Roster retention evidence note or source").fill("Four athletes left after last season");
  await page.getByRole("button", { name: "Review the evidence" }).click();
  await expect(page.getByText("Input: Four athletes left after last season")).toBeVisible();
  await expect(page.getByRole("heading", { name: "Evidence gaps + questions to ask" })).toBeVisible();
  expect(await page.evaluate(() => localStorage.length)).toBe(0);
});

test("unknown solution slug returns not found", async ({ page }) => {
  const response = await page.goto("/solutions/not-a-real-tool");
  expect(response?.status()).toBe(404);
  await expect(page.getByText(/not found/i).first()).toBeVisible();
});
