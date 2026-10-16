/**
 * Админы зарлал (popup).
 *
 *   • Админ `/admin/announcements` дээр зарлал бичиж, урьдчилан харж, нийтэлнэ,
 *   • Шинэ (үнэгүй) хэрэглэгчид «Нэвтэрсэн бүх хэрэглэгч»-ийнх гарна, Standard-ынх,
 *     ноорог гарахгүй; товч нь хуудас руу аваачиж, цонх хаагдана,
 *   • Хаасан зарлал дахин гарахгүй; нэг сесст нэгээс илүү цонх гарахгүй,
 *   • Standard багцтай болмогц Standard-ынх гарна,
 *   • Нэвтрээгүй зочинд «Бүх зочин»-оос бусад нь гарахгүй.
 *
 * Үүсгэсэн зарлалыг төгсгөлд нь устгана — бусад тестэд цонх гарч саад болохгүй.
 */

import { request } from "playwright";

import {
  API_URL,
  BASE_URL,
  SEED,
  check,
  goto,
  grantPlan,
  login,
  logout,
  newSession,
  summary,
} from "./harness.mjs";

const stamp = Date.now().toString(36);
const TITLE = `E2E зарлал ${stamp}`;
const STANDARD_TITLE = `E2E Standard ${stamp}`;
const DRAFT_TITLE = `E2E ноорог ${stamp}`;

const admin = await request.newContext();
await admin.post(`${API_URL}/auth/login`, { data: SEED.admin });

/** Шинэ хэрэглэгч — өөрийн cookie, хөтчийн санах ойтой тусдаа context. */
async function registerIn(page) {
  const email = `e2e-zarlal-${Date.now()}@suralts.mn`;
  await goto(page, "/register");
  await page.fill("#name", "Зарлал Үзэгч");
  await page.fill("#email", email);
  await page.fill("#password", "Nuuts12345");
  await page.getByLabel("Би 16 нас хүрсэн").check();
  await page.locator("#accept_terms").check();
  await page.getByRole("button", { name: "Бүртгүүлэх" }).click();
  await page.waitForURL("**/dashboard", { timeout: 25_000 });
  return email;
}

/** Цонх `ms` хугацаанд гарахгүй байгаа эсэх (гарах хугацаа 1.2 сек). */
async function noPopup(page, ms = 3_000) {
  await page.waitForTimeout(ms);
  return (await page.getByRole("dialog").count()) === 0;
}

const sessions = [];

try {
  // --- Админ бичиж нийтэлнэ ---------------------------------------------------------
  const adminSession = await newSession({ width: 1280, height: 1000, announcements: true });
  sessions.push(adminSession);
  const page = adminSession.page;
  await login(page, SEED.admin);
  await goto(page, "/admin/announcements");
  await page.getByRole("heading", { name: "Шинэ зарлал" }).waitFor({ timeout: 20_000 });

  await page.getByLabel("Онцлох боломж").check();
  await page.fill("#announcement-title", TITLE);
  await page.fill("#announcement-body", "**Шинэ** боломж нэмэгдлээ.");
  await page.fill("#announcement-cta-label", "Багц үзэх");
  await page.fill("#announcement-cta-url", "pricing");
  await page.getByLabel("Нэвтэрсэн бүх хэрэглэгч").check();
  await page.getByRole("button", { name: "Хадгалах" }).click();
  check(
    "буруу холбоос алдаа өгнө",
    (await page.locator("#announcement-cta-url-error").innerText()).includes("https://"),
  );
  await page.fill("#announcement-cta-url", "/pricing");

  await page.getByRole("button", { name: "Урьдчилан харах" }).click();
  const preview = page.getByRole("dialog");
  await preview.waitFor({ timeout: 10_000 });
  const previewText = await preview.innerText();
  check(
    "урьдчилан харах цонх гарчиг, төрөл, товчтой",
    previewText.includes(TITLE) &&
      // Эхний мөрийг CSS томоор харуулдаг.
      previewText.toLowerCase().includes("онцлох боломж") &&
      (await preview.getByRole("link", { name: "Багц үзэх" }).count()) === 1,
    previewText.replace(/\s+/g, " "),
  );
  check(
    "Markdown тод бичвэр",
    (await preview.locator("strong", { hasText: "Шинэ" }).count()) === 1,
  );
  await preview.getByRole("button", { name: "Хаах", exact: true }).first().click();
  await preview.waitFor({ state: "hidden" });

  await page.getByRole("button", { name: "Хадгалах" }).click();
  await page
    .locator("[data-sonner-toast]", { hasText: "Зарлал хадгалагдлаа." })
    .waitFor({ timeout: 10_000 });
  const item = page.locator('section[aria-labelledby="announcement-list-title"] li', {
    hasText: TITLE,
  });
  await item.waitFor({ timeout: 10_000 });
  const itemText = await item.innerText();
  check(
    "жагсаалтад «Харагдаж байна», хүрээ",
    itemText.includes("Харагдаж байна") && itemText.includes("Нэвтэрсэн бүх хэрэглэгч"),
    itemText.replace(/\s+/g, " "),
  );

  // Засах: гарчиг маягт руу ачаалагдана.
  await item.getByRole("button", { name: "Засах" }).click();
  await page.getByRole("heading", { name: "Зарлал засах" }).waitFor();
  check("засахад утга бөглөгдөнө", (await page.inputValue("#announcement-title")) === TITLE);
  await page.getByRole("button", { name: "Болих" }).click();
  await page.getByRole("heading", { name: "Шинэ зарлал" }).waitFor();

  // Үлдсэн хоёрыг API-аар — Standard-д, ноорог.
  for (const data of [
    { title: STANDARD_TITLE, audience: "standard", active: true },
    { title: DRAFT_TITLE, audience: "everyone", active: false },
  ]) {
    const response = await admin.post(`${API_URL}/announcements`, {
      data: { kind: "update", body: "Шинэчлэл.", ...data },
    });
    check(`${data.title} үүсэв`, response.status() === 201, String(response.status()));
  }
  await logout(page);

  // --- Шинэ үнэгүй хэрэглэгч --------------------------------------------------------------
  const student = await newSession({ width: 1280, height: 900, announcements: true });
  sessions.push(student);
  const email = await registerIn(student.page);
  const popup = student.page.getByRole("dialog");
  await popup.waitFor({ timeout: 10_000 });
  const popupText = await popup.innerText();
  check(
    "үнэгүй хэрэглэгчид «Нэвтэрсэн»-ийнх гарна",
    popupText.includes(TITLE) &&
      !popupText.includes(STANDARD_TITLE) &&
      !popupText.includes(DRAFT_TITLE),
    popupText.replace(/\s+/g, " "),
  );
  await popup.getByRole("link", { name: "Багц үзэх" }).click();
  await student.page.waitForURL("**/pricing", { timeout: 15_000 });
  check("товч /pricing руу аваачна, цонх хаагдана", await noPopup(student.page, 1_500));

  await student.page.reload();
  check("хаасан зарлал дахин гарахгүй", await noPopup(student.page));

  // --- Standard болмогц ---------------------------------------------------------------
  await grantPlan(email, 1);
  // Шинэ сесс (таб) — нэг сесст нэг цонх дүрмийг шалгахын тулд.
  const paid = await newSession({ width: 1280, height: 900, announcements: true });
  sessions.push(paid);
  await login(paid.page, { email, password: "Nuuts12345" });
  const paidPopup = paid.page.getByRole("dialog");
  await paidPopup.waitFor({ timeout: 10_000 });
  check(
    "Standard хэрэглэгчид Standard-ынх гарна",
    (await paidPopup.innerText()).includes(STANDARD_TITLE),
  );
  await paidPopup.getByRole("button", { name: "Ойлголоо" }).click();
  await paidPopup.waitFor({ state: "hidden" });
  // Энэ context-д «Нэвтэрсэн»-ийнх хараахан хаагдаагүй ч нэг сесст нэг л цонх.
  await goto(paid.page, "/courses");
  check("нэг сесст хоёр дахь цонх гарахгүй", await noPopup(paid.page));

  // --- Нэвтрээгүй зочин -------------------------------------------------------------------
  const visitor = await newSession({ width: 1280, height: 900, announcements: true });
  sessions.push(visitor);
  await goto(visitor.page, "/");
  // Хөгжүүлэгчийн санд «Бүх зочин»-д зориулсан өөр зарлал байж болно — энэ
  // тестийн «Нэвтэрсэн», Standard, ноорог зарлал л гарах ёсгүй.
  await visitor.page.waitForTimeout(3_000);
  const visitorPopup =
    (await visitor.page.getByRole("dialog").count()) > 0
      ? await visitor.page.getByRole("dialog").innerText()
      : "";
  check(
    "зочинд «Бүх зочин»-оос бусад нь гарахгүй",
    ![TITLE, STANDARD_TITLE, DRAFT_TITLE].some((title) => visitorPopup.includes(title)),
    visitorPopup.replace(/\s+/g, " ").slice(0, 120),
  );

  for (const session of sessions) {
    const unexpected = session.problems.filter((problem) => !problem.includes("401"));
    check("консолд алдаагүй", unexpected.length === 0, unexpected.join(" | "));
  }
} catch (error) {
  check("тест бүрэн ажиллав", false, String(error));
} finally {
  // Бусад тестэд цонх гарахгүйн тулд энэ тестийн зарлалыг устгана.
  const all = await (await admin.get(`${API_URL}/announcements`)).json();
  for (const item of all.filter((entry) => entry.title.includes(stamp))) {
    await admin.delete(`${API_URL}/announcements/${item.id}`);
  }
  await admin.dispose();
  for (const session of sessions) await session.close();
}

console.log(`  (${BASE_URL})`);
process.exit(summary("announcements") > 0 ? 1 : 0);
