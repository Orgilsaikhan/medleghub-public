/**
 * Хөнгөн E2E harness.
 *
 * Тусдаа test runner нэмэлгүйгээр Playwright дээр шууд ажиллана — MVP-д
 * хангалттай бөгөөд хамаарал цөөн байлгана.
 */

import { chromium, request } from "playwright";

export const BASE_URL = process.env.E2E_BASE_URL ?? "http://localhost:3000";
export const API_URL = process.env.E2E_API_URL ?? "http://localhost:8000/api/v1";

export const SEED = {
  admin: { email: "admin@suralts.mn", password: "Admin12345" },
  // Үнэгүй хэрэглэгч — төлбөрт хичээл дээр багцын санал харна.
  student: { email: "suragch@suralts.mn", password: "Suragch12345" },
  // Standard багцтай (seed үргэлж сунгана) — төлбөрт хичээлийн агуулгыг шалгахад.
  standard: { email: "standard@suralts.mn", password: "Standard12345" },
  course: { slug: "javascript-undes", title: "JavaScript үндэс" },
};

const results = [];
let failures = 0;

export function check(name, condition, detail = "") {
  const ok = Boolean(condition);
  if (!ok) failures += 1;
  results.push({ name, ok, detail });
  console.log(`  ${ok ? "PASS" : "FAIL"}  ${name}${detail ? ` — ${detail}` : ""}`);
  return ok;
}

export function checkEqual(name, actual, expected) {
  return check(name, Object.is(actual, expected), `хүлээсэн ${expected}, гарсан ${actual}`);
}

export function summary(label) {
  const passed = results.length - failures;
  console.log(`\n${label}: ${passed}/${results.length} passed`);
  return failures;
}

/**
 * Админы зарлал (popup) тестийн хуудсыг бүү халхал: `AnnouncementPopup` нэг
 * табын сесст нэг л цонх гаргадаг тул сессийг «аль хэдийн гарсан» гэж
 * тэмдэглэнэ. Хөгжүүлэгчийн санд идэвхтэй зарлал байсан ч бусад тест саадгүй.
 * Зарлалыг шалгадаг тест `newSession({ announcements: true })` дуудна.
 */
export async function suppressAnnouncements(context) {
  await context.addInitScript(() => {
    try {
      const key = "medleghub:announcement-shown";
      if (!window.sessionStorage.getItem(key)) window.sessionStorage.setItem(key, "e2e");
    } catch {
      // Хөтчийн санах ой хаалттай — зарлал ч гарахгүй.
    }
  });
}

/** Шинэ browser context. Алдаа болон 4xx/5xx хариуг цуглуулна. */
export async function newSession({
  width = 1440,
  height = 900,
  dark = false,
  announcements = false,
} = {}) {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width, height },
    colorScheme: dark ? "dark" : "light",
  });
  if (!announcements) await suppressAnnouncements(context);
  const page = await context.newPage();

  const problems = [];
  const requests = [];
  page.on("pageerror", (error) => problems.push(`pageerror: ${error}`));
  page.on("console", (message) => {
    if (message.type() === "error") problems.push(`console: ${message.text()}`);
  });
  // Серверийн алдааг хаягтай нь — «Failed to load resource: 500» гэхээс илүү тодорхой.
  page.on("response", (response) => {
    if (response.status() >= 500) {
      problems.push(`http ${response.status()}: ${response.request().method()} ${response.url()}`);
    }
  });
  page.on("request", (request) => {
    if (request.url().includes("/api/v1/")) {
      requests.push(`${request.method()} ${new URL(request.url()).pathname}`);
    }
  });

  return {
    browser,
    page,
    problems,
    requests,
    close: () => browser.close(),
  };
}

export async function goto(page, path, { waitFor } = {}) {
  await page.goto(`${BASE_URL}${path}`, { waitUntil: "domcontentloaded" });
  if (waitFor) await page.waitForSelector(waitFor, { timeout: 60_000 });
  // Hydration дуусахыг хүлээнэ — товч дарахад React бэлэн байх ёстой.
  await page.waitForFunction(() => document.readyState === "complete");
  await page.waitForTimeout(900);
}

export async function login(page, { email, password }) {
  await goto(page, "/login");
  await page.fill("#email", email);
  await page.fill("#password", password);
  await page.getByRole("button", { name: "Нэвтрэх" }).click();
  await page.waitForURL("**/dashboard", { timeout: 25_000 });
  await page.waitForTimeout(700);
}

/**
 * Хэрэглэгчид Standard багц олгоно — админ API-ер, UI-гүй.
 *
 * `registerNew`-ээр үүсгэсэн шинэ хэрэглэгч төлбөрт хичээлийг үзэх шаардлагатай
 * тестүүдэд. Жинхэнэ төлбөрийн урсгалыг Wire-ийн түлхүүргүйгээр шалгах
 * боломжгүй — түүнийг backend-ийн `tests/test_billing.py` хамарна.
 */
export async function grantPlan(email, months = 1) {
  const api = await request.newContext();
  try {
    const signedIn = await api.post(`${API_URL}/auth/login`, { data: SEED.admin });
    if (!signedIn.ok()) throw new Error(`Админ нэвтэрч чадсангүй: ${signedIn.status()}`);
    const granted = await api.post(`${API_URL}/billing/grants`, { data: { email, months } });
    if (!granted.ok()) throw new Error(`Багц олгож чадсангүй: ${granted.status()}`);
  } finally {
    await api.dispose();
  }
}

export async function logout(page) {
  await page.getByRole("button", { name: "Цэс" }).click();
  await page.getByRole("menuitem", { name: "Гарах" }).click();
  await page.waitForURL(`${BASE_URL}/`, { timeout: 20_000 });
  await page.waitForTimeout(500);
}

export async function registerNew(page, name = "Тест Хэрэглэгч") {
  const email = `e2e-${Date.now()}-${Math.random().toString(36).slice(2, 7)}@suralts.mn`;
  await goto(page, "/register");
  await page.fill("#name", name);
  await page.fill("#email", email);
  await page.fill("#password", "Nuuts12345");
  await page.getByLabel("Би 16 нас хүрсэн").check();
  await page.locator("#accept_terms").check();
  await page.getByRole("button", { name: "Бүртгүүлэх" }).click();
  await page.waitForURL("**/dashboard", { timeout: 25_000 });
  await page.waitForTimeout(700);
  return { email, password: "Nuuts12345" };
}

/**
 * Monaco засварлагчийн бүх кодыг солино.
 *
 * Санал болголтын цонх нээлттэй үед бичвэл гэнэт өөр үг орох тул бичихийн
 * өмнө болон дараа нь Escape дарж хаана.
 */
export async function setEditorCode(page, code) {
  await page.locator(".view-lines").first().click();
  await page.keyboard.press("Control+A");
  await page.keyboard.press("Delete");
  await page.keyboard.press("Escape");
  // `type` нь товчлуур дарахыг дуурайдаг тул Monaco-д тэмдэгт алдагддаг.
  // `insertText` нь текстийг шууд оруулна.
  await page.keyboard.insertText(code);
  await page.keyboard.press("Escape");
  await page.waitForTimeout(400);
}

/**
 * Кодыг Monaco-ийн модел рүү ШУУД бичнэ.
 *
 * `setEditorCode` нь товч дарахыг дуурайдаг тул Monaco нь автоматаар догол
 * мөр нэмж, хаалт хаадаг. Энэ нь хүн бичихэд ЗӨВ зан төлөв боловч
 * урьдчилан догол мөртэй бэлдсэн Python кодыг гажуудуулна. Тиймээс олон
 * мөрт Python кодыг ингэж оруулна — буулгах (paste) үйлдэлтэй ижил үр дүн.
 */
export async function setEditorValue(page, code) {
  await page.waitForFunction(() => (window.monaco?.editor?.getModels?.() ?? []).length > 0, null, {
    timeout: 60_000,
  });
  await page.evaluate((next) => {
    window.monaco.editor.getModels()[0].setValue(next);
  }, code);
  await page.waitForTimeout(300);
}

/**
 * Засварлагчид одоо байгаа код.
 *
 * Monaco нь DOM дотор зайг таслагдахгүй зай (U+00A0) болгон гаргадаг тул
 * энгийн зай болгож жигдэлнэ. Эс бөгөөс `includes(" ")` шалгалт бүтэлгүйтнэ.
 */
export async function editorCode(page) {
  const text = await page.locator(".view-lines").first().innerText();
  return text.replace(/ /g, " ");
}

export async function runCode(page) {
  await page.getByRole("button", { name: "Код ажиллуулах" }).click();
  await page.waitForTimeout(1800);
  return (await page.locator('[role="log"]').innerText()).trim();
}

/**
 * Даалгавартай хичээлийг ЖИНХЭНЭ замаар дуусгана: жишиг шийдлийг (сурагчийн
 * «Тусламж»-аас авдагтай ижил `/lessons/{id}/help`) засварлагчид бичиж,
 * «Илгээх» дарна. Бүх тест давж, хичээл дууссаныг хүлээнэ.
 *
 * `page.context().request` нь хөтчийн cookie-г хэрэглэдэг, CSP-д баригдахгүй.
 */
export async function submitReferenceSolution(page, courseSlug, lessonSlug) {
  const api = page.context().request;
  const player = await api.get(`${API_URL}/courses/${courseSlug}/lessons/${lessonSlug}`);
  if (!player.ok()) throw new Error(`Хичээл ачаалж чадсангүй: ${player.status()}`);
  const { lesson } = await player.json();
  const help = await api.get(`${API_URL}/lessons/${lesson.id}/help`);
  if (!help.ok()) throw new Error(`Шийдэл авч чадсангүй: ${help.status()}`);
  const { solution } = await help.json();

  await setEditorCode(page, solution);
  await page.getByRole("button", { name: "Илгээх" }).click();
  await page.getByText("Бүх тест амжилттай").first().waitFor({ timeout: 30_000 });
}
