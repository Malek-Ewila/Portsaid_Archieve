import { expect, test } from "@playwright/test";

test("home page presents an RTL archive and navigates to an era", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator("html")).toHaveAttribute("dir", "rtl");
  await expect(page.getByRole("img", { name: "واجهة بورسعيد على القناة، باتجاه الجنوب، بين 1934 و1939." })).toBeVisible();
  await expect(page.getByRole("heading", { name: "الحقب التاريخية" })).toBeVisible();
  await page.getByRole("link", { name: /1859 – 1869/ }).first().click();
  await expect(page).toHaveURL(/\/eras\/1859-1869$/);
  await expect(page.getByRole("heading", { level: 1 })).toContainText("1859");
  await expect(page.getByText("لم تُضف صور أرشيفية لهذه الحقبة بعد.")).toBeVisible();
});

test("1900s archive photos show local files, dates, and attribution", async ({ page }) => {
  await page.goto("/eras/1900-1909");
  const photos = page.locator(".image-list figure");
  await expect(photos).toHaveCount(2);
  await expect(photos.nth(0).getByRole("img")).toHaveAttribute("src", /url=%2Fimages%2Fsuez-canal-company-admin-building-1900\.webp/);
  await expect(photos.nth(1).getByRole("img")).toHaveAttribute("src", /url=%2Fimages%2Fport-said-coaling-steamer-1900\.webp/);
  await expect(photos.nth(0).getByText("1900", { exact: true })).toBeVisible();
  await expect(photos.nth(1).getByText(/1900 في سجل كومنز/)).toBeVisible();
  await expect(photos.getByRole("link", { name: "ملف الصورة ↗" }).first()).toHaveAttribute("href", /commons\.wikimedia\.org/);
  await expect(photos.getByText(/الملك العام/).first()).toBeVisible();
});

test("timeline links are keyboard reachable and period navigation works", async ({ page }) => {
  await page.goto("/");
  const firstEra = page.getByRole("navigation", { name: "الخط الزمني لحقب بورسعيد" }).getByRole("link").first();
  for (let step = 0; step < 10; step += 1) {
    if (await firstEra.evaluate((element) => element === document.activeElement)) break;
    await page.keyboard.press("Tab");
  }
  await expect(firstEra).toBeFocused();
  await page.keyboard.press("Enter");
  await expect(page).toHaveURL(/\/eras\/1859-1869$/);
  await expect(page.getByRole("navigation", { name: "التنقل بين الحقب" }).getByRole("link", { name: /الحقبة التالية/ })).toBeVisible();
});

test("mobile layout retains vertical scrolling and a horizontally scrollable timeline", async ({ page, isMobile }) => {
  test.skip(!isMobile, "Mobile viewport coverage runs in the Pixel project");
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/");
  const timeline = page.locator(".timeline-scroll");
  const dimensions = await page.evaluate(() => ({
    viewport: document.documentElement.clientWidth,
    document: document.documentElement.scrollWidth,
    timelineClient: document.querySelector(".timeline-scroll")?.clientWidth,
    timelineScroll: document.querySelector(".timeline-scroll")?.scrollWidth,
  }));
  expect(dimensions.document).toBeLessThanOrEqual(dimensions.viewport);
  expect(dimensions.timelineScroll).toBeGreaterThan(dimensions.timelineClient ?? 0);
  await expect(timeline).toHaveCSS("touch-action", "pan-x pan-y");
  await page.mouse.wheel(0, 500);
  await expect.poll(() => page.evaluate(() => window.scrollY)).toBeGreaterThan(0);
  await expect(timeline).toBeVisible();
});

test("touch taps can open a period from the timeline", async ({ page, isMobile }) => {
  test.skip(!isMobile, "Touch activation coverage runs in the Pixel project");
  await page.goto("/");
  const timeline = page.locator(".timeline-scroll");
  await timeline.scrollIntoViewIfNeeded();
  const firstEra = timeline.getByRole("link").first();
  await firstEra.tap();
  await expect(page).toHaveURL(/\/eras\/1859-1869$/);
});

test("reduced motion disables smooth scrolling", async ({ page }) => {
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.goto("/");
  await expect(page.locator("html")).toHaveCSS("scroll-behavior", "auto");
  await expect(page.locator(".timeline-scroll")).toHaveCSS("scroll-behavior", "auto");
  await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
  await expect(page.getByRole("img", { name: "واجهة بورسعيد على القناة، باتجاه الجنوب، بين 1934 و1939." })).toBeVisible();
});

test("responsive pages do not overflow the viewport", async ({ page }) => {
  for (const width of [320, 390, 768, 1024, 1440]) {
    await page.setViewportSize({ width, height: 900 });
    await page.goto("/");
    const dimensions = await page.evaluate(() => ({
      viewport: document.documentElement.clientWidth,
      document: document.documentElement.scrollWidth,
    }));
    expect(dimensions.document, `overflow at ${width}px`).toBeLessThanOrEqual(dimensions.viewport);
  }
});
