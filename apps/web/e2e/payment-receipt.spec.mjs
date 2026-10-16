/**
 * Төлбөрийн баримт хэвлэгч (`/billing/success`).
 *
 *   • Үнэгүй сарын промо код: `/pricing` дээр идэвхжүүлэхэд баримтын хуудас руу
 *     шилжиж, принтер «шалгаж» → «хэвлэж» → «амжилттай», 0₮-ийн баримт гарна,
 *   • Wire-ийн төлбөр: төлөвийн хариуг дуурайж (жинхэнэ Wire-гүй) хөнгөлөлт,
 *     промо код, гүйлгээний дугаартай баримт,
 *   • Хуучин `/billing/return?payment=` шинэ хуудас руу шилжинэ,
 *   • Хөдөлгөөн багасгах тохиргоотой үед ч баримт гарна,
 *   • Баримт бүрэн гартал дэлгэц уншигчид нуугдана; axe (гэрэл, харанхуй).
 */

import fs from "node:fs";

import { request } from "playwright";

import { API_URL, SEED, check, goto, newSession, registerNew, summary } from "./harness.mjs";

const axeSource = fs.readFileSync("node_modules/axe-core/axe.min.js", "utf8");
const stamp = Date.now().toString(36).toUpperCase();
const GIFT = `GIFT${stamp}`;

const admin = await request.newContext();
await admin.post(`${API_URL}/auth/login`, { data: SEED.admin });
const created = await admin.post(`${API_URL}/billing/promo-codes`, {
  data: { code: GIFT, kind: "free_months", free_months: 2, max_uses: 1 },
});
const giftId = (await created.json()).id;

/** Принтерийн `data-stage`-ийг дараалан тэмдэглэнэ (давхардалгүй). */
async function recordStages(page, until = "complete", timeout = 15_000) {
  const seen = [];
  const deadline = Date.now() + timeout;
  while (Date.now() < deadline) {
    const stage = await page
      .locator("section[data-stage]")
      .getAttribute("data-stage")
      .catch(() => null);
    if (stage && seen.at(-1) !== stage) seen.push(stage);
    if (stage === until) break;
    await page.waitForTimeout(100);
  }
  return seen;
}

async function axe(page) {
  // Дууссаны дараах бичвэр 300 мс-д тодордог — дундуур нь шалгавал бүдэг өнгө гарна.
  await page.waitForTimeout(500);
  await page.addScriptTag({ content: axeSource });
  const results = await page.evaluate(() =>
    window.axe.run(document, {
      runOnly: { type: "tag", values: ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"] },
    }),
  );
  return results.violations
    .filter((item) => item.impact !== "minor")
    .map(
      (item) =>
        `[${item.impact}] ${item.id}: ${item.nodes
          .slice(0, 3)
          .map((node) => `${node.html.slice(0, 90)} (${node.any[0]?.message ?? ""})`)
          .join(" ; ")}`,
    );
}

const FAKE_ID = "3f0c2a9e-7d41-4b8e-9a55-0c1d2e3f4a5b";
const fakePayment = {
  id: FAKE_ID,
  status: "succeeded",
  plan: {
    has_plan: true,
    plan_expires_at: "2027-03-30T08:00:00Z",
    price_mnt: 24900,
    options: [],
    discount: null,
  },
  receipt: {
    kind: "payment",
    months: 6,
    free_months: 1,
    list_price_mnt: 124500,
    discount_percent: 20,
    discount_mnt: 24900,
    discount_source: "promo",
    promo_code: "HELLOWORLD2026",
    amount_mnt: 99600,
    currency: "MNT",
    reference: "pi_test123",
    created_at: "2026-09-30T06:00:00Z",
    paid_at: "2026-09-30T06:01:00Z",
  },
};

const sessions = [];

try {
  // --- Үнэгүй сарын промо код -------------------------------------------------------
  const student = await newSession({ width: 1280, height: 1000 });
  sessions.push(student);
  const { page } = student;
  await registerNew(page, "Баримт Шалгагч");
  await goto(page, "/pricing");
  await page.getByRole("button", { name: "Промо код байна уу?" }).click();
  await page.getByLabel("Промо код", { exact: true }).fill(GIFT.toLowerCase());
  await page.getByRole("button", { name: "Хэрэглэх" }).click();
  await page.getByRole("button", { name: "2 сар үнэгүй идэвхжүүлэх" }).click();
  await page.waitForURL(/\/billing\/success\?redemption=/, { timeout: 15_000 });
  check("идэвхжүүлэхэд баримтын хуудас руу шилжинэ", true);

  const stages = await recordStages(page);
  check(
    "принтер шалгаж → хэвлэж → дууссан",
    stages.join(">") === "processing>printing>complete",
    stages.join(" > "),
  );
  const paper = page.locator("article");
  check(
    "баримт бүрэн гартал дэлгэц уншигчид нуугдана, дараа нь нээгдэнэ",
    (await paper.locator("xpath=..").getAttribute("aria-hidden")) !== "true",
  );
  const text = await paper.innerText();
  check(
    "баримтад промо код, 2 сар, 0₮, хэрэглэгч",
    text.includes(`Промо код ${GIFT}`) &&
      text.includes("2 сар үнэгүй") &&
      text.includes("НИЙТ ТӨЛСӨН") &&
      text.includes("0₮") &&
      text.includes("Баримт Шалгагч"),
    text.replace(/\s+/g, " ").slice(0, 300),
  );
  check(
    "принтерийн төлөв «Төлбөр амжилттай»",
    (await page.getByRole("status").first().innerText()).includes("Төлбөр амжилттай"),
  );
  await page.getByText("2 сар үнэгүй нэмэгдлээ!").waitFor({ timeout: 5_000 });
  check(
    "дууссаны дараа «Миний сургалтууд» товч",
    await page.getByRole("main").getByRole("link", { name: "Миний сургалтууд" }).isVisible(),
  );
  const lightViolations = await axe(page);
  check(
    "баримтын хуудас хүртээмжийн зөрчилгүй (гэрэл)",
    lightViolations.length === 0,
    lightViolations.join(" | "),
  );

  // Бусдын эсвэл байхгүй баримт.
  await goto(page, `/billing/success?redemption=${FAKE_ID}`);
  await page.getByText("Промо кодын баримт олдсонгүй.").waitFor({ timeout: 15_000 });
  check("байхгүй промо баримт «олдсонгүй»", true);

  // --- Wire-ийн төлбөр (хариуг дуурайна) ---------------------------------------------------
  const paid = await newSession({ width: 390, height: 900, dark: true });
  sessions.push(paid);
  await registerNew(paid.page, "Төлсөн Хэрэглэгч");
  await paid.page.route(`**/billing/payments/${FAKE_ID}`, (route) =>
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(fakePayment),
    }),
  );
  await goto(paid.page, `/billing/return?payment=${FAKE_ID}`);
  await paid.page.waitForURL(new RegExp(`/billing/success\\?payment=${FAKE_ID}`), {
    timeout: 15_000,
  });
  check("хуучин /billing/return шинэ хуудас руу шилжинэ", true);
  const paidStages = await recordStages(paid.page);
  check("төлбөрийн баримт хэвлэгдэнэ", paidStages.at(-1) === "complete", paidStages.join(" > "));
  const paidText = await paid.page.locator("article").innerText();
  check(
    "төлбөрийн баримтад хөнгөлөлт, код, дүн, гүйлгээ",
    paidText.includes("6 сар (1 сар үнэгүй)") &&
      paidText.includes("124,500₮") &&
      paidText.includes("Хөнгөлөлт 20% (HELLOWORLD2026)") &&
      paidText.includes("−24,900₮") &&
      paidText.includes("99,600₮") &&
      paidText.includes("pi_test123") &&
      paidText.includes("3F0C2A9E"),
    paidText.replace(/\s+/g, " ").slice(0, 400),
  );
  const overflow = await paid.page.evaluate(
    () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
  );
  check("гар утсан дээр хэвтээ гүйлгээгүй", overflow <= 1, `${overflow} px`);
  const darkViolations = await axe(paid.page);
  check(
    "баримтын хуудас хүртээмжийн зөрчилгүй (харанхуй, утас)",
    darkViolations.length === 0,
    darkViolations.join(" | "),
  );

  // --- Хөдөлгөөн багасгах ----------------------------------------------------------------
  const calm = await newSession({ width: 1280, height: 900 });
  sessions.push(calm);
  await calm.page.emulateMedia({ reducedMotion: "reduce" });
  await registerNew(calm.page, "Тайван Хэрэглэгч");
  await calm.page.route(`**/billing/payments/${FAKE_ID}`, (route) =>
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(fakePayment),
    }),
  );
  await goto(calm.page, `/billing/success?payment=${FAKE_ID}`);
  const calmStages = await recordStages(calm.page);
  const calmAnimation = await calm.page
    .locator("article")
    .locator("xpath=..")
    .evaluate((element) => getComputedStyle(element).animationName);
  check(
    "хөдөлгөөн багасгахад ч баримт гарна, хөдөлгөөнгүй",
    calmStages.at(-1) === "complete" && calmAnimation === "none",
    `${calmStages.join(" > ")} · ${calmAnimation}`,
  );

  for (const session of sessions) {
    // Байхгүй баримтын 404 нь хүлээгдсэн хариу.
    const unexpected = session.problems.filter((problem) => !problem.includes("404"));
    check("консолд алдаагүй", unexpected.length === 0, unexpected.join(" | "));
  }
} catch (error) {
  check("тест бүрэн ажиллав", false, String(error));
} finally {
  // Туршилтын кодыг идэвхгүй болгоно (устгах API байхгүй).
  await admin.patch(`${API_URL}/billing/promo-codes/${giftId}`, { data: { active: false } });
  await admin.dispose();
  for (const session of sessions) await session.close();
}

process.exit(summary("payment-receipt") > 0 ? 1 : 0);
