/**
 * Standard багц — төлбөрт хичээлийн түгжээ.
 *
 * JavaScript сургалтын эхний 15 хичээл үнэгүй, 16 дахь нь («Функц») төлбөрт.
 * Үнэгүй сурагч хөтөлбөр, өмнөх/дараагийн холбоосоо харж, агуулгын оронд
 * багцын санал авна. Багцтай сурагч бүх хичээлийг үзнэ.
 *
 * Wire-ийн төлбөрийн хуудсыг энд дуудахгүй — CI-д түлхүүр байхгүй. Урсгалыг
 * backend-ийн `tests/test_billing.py` Wire-ийг загварчилж шалгана.
 */

import { API_URL, SEED, check, goto, login, newSession, summary } from "./harness.mjs";

const COURSE = "javascript-undes";
const FREE_LESSON = "break-ba-continue"; // #15
const LOCKED_LESSON = "funkts"; // #16

/**
 * API-г `page.request`-ээр дуудна — хөтчийн cookie-г хуваалцдаг ч хуудасны
 * CSP-д захирагдахгүй. (Хөгжүүлэлтэд сайт API-г `/api/v1` proxy-оор дууддаг
 * тул хуудас доторх `fetch` нь `localhost:8000` руу хүрч чадахгүй.)
 */
async function lockedLessonId(page) {
  const surgalt = await (await page.request.get(`${API_URL}/courses/${COURSE}`)).json();
  await page.request.post(`${API_URL}/courses/${surgalt.id}/enroll`);
  return surgalt.modules.flatMap((m) => m.lessons).find((l) => l.slug === LOCKED_LESSON).id;
}

let session = await newSession();
let { page, problems } = session;

try {
  await login(page, SEED.student);

  // --- Сургалтын хуудас ----------------------------------------------------
  await goto(page, `/courses/${COURSE}`);
  const detail = await page.locator("main").innerText();
  check("«15 хичээл үнэгүй» тэмдэг харагдана", detail.includes("15 хичээл үнэгүй"));
  check("үнэ, үлдсэн хичээлийн тоо харагдана", detail.includes("24,900₮ / сар"));
  check(
    "төлбөрт хичээлүүд түгжээтэй гэж тэмдэглэгдэнэ",
    (await page.getByText("Standard багц шаардлагатай").count()) > 0,
  );

  // --- Үнэгүй хичээл бүрэн ажиллана ----------------------------------------
  await goto(page, `/learn/${COURSE}/${FREE_LESSON}`, { waitFor: ".monaco-editor" });
  check("үнэгүй хичээлд засварлагч байна", (await page.locator(".monaco-editor").count()) === 1);

  // --- Төлбөрт хичээл -----------------------------------------------------
  await goto(page, `/learn/${COURSE}/${LOCKED_LESSON}`);
  await page.getByText("Энэ хичээл Standard багцад багтана").waitFor({ timeout: 20_000 });
  check("төлбөрт хичээлд засварлагч байхгүй", (await page.locator(".monaco-editor").count()) === 0);
  const cta = page.getByRole("link", { name: "Standard багц авах" });
  check(
    "санал нь энэ хичээл рүү буцах хаягтай үнийн хуудас руу хөтөлнө",
    (await cta.getAttribute("href")) ===
      `/pricing?next=${encodeURIComponent(`/learn/${COURSE}/${LOCKED_LESSON}`)}`,
  );
  check(
    "өмнөх хичээл рүү буцах боломжтой",
    (await page.getByRole("link", { name: /Өмнөх хичээл/ }).count()) > 0,
  );

  // Агуулга сервер дээрээ үлддэг — API ч 402 буцаана.
  const lessonId = await lockedLessonId(page);
  const statuses = [
    (await page.request.get(`${API_URL}/lessons/${lessonId}`)).status(),
    (await page.request.post(`${API_URL}/lessons/${lessonId}/complete`)).status(),
  ];
  check(
    "API түгжээтэй хичээлийг 402-оор хаана",
    statuses.every((s) => s === 402),
    statuses.join(","),
  );

  // --- Үнийн хуудас --------------------------------------------------------
  await cta.click();
  await page.waitForURL("**/pricing?next=**", { timeout: 20_000 });
  await page.waitForTimeout(900);
  const pricing = await page.locator("main").innerText();
  check("үнийн хуудас 24,900₮ харуулна", pricing.includes("24,900₮"));
  check("үнэгүй багц «Одоогийн багц»", pricing.includes("Одоогийн багц"));

  // Түгжээтэй хичээлийн API 402 нь санаатай — бусад console алдааг л тоолно.
  const unexpected = problems.filter((line) => !line.includes("402"));
  check("console цэвэр", unexpected.length === 0, unexpected.slice(0, 3).join(" | "));

  // --- Буцах хуудас: байхгүй төлбөр (санаатай 404 — console шалгалтын дараа) --
  await goto(page, "/billing/return?payment=00000000-0000-0000-0000-000000000000");
  await page.getByText("Төлбөрийн мэдээлэл олдсонгүй.").waitFor({ timeout: 20_000 });
  check("байхгүй төлбөр «олдсонгүй» гэж харагдана", true);
} finally {
  await session.close();
}

// --- Standard багцтай сурагч -------------------------------------------------
session = await newSession();
({ page, problems } = session);

try {
  await login(page, SEED.standard);
  await goto(page, `/learn/${COURSE}/${LOCKED_LESSON}`, { waitFor: ".monaco-editor" });
  check(
    "багцтай сурагч төлбөрт хичээлийг үзнэ",
    (await page.locator(".monaco-editor").count()) === 1,
  );
  check(
    "багцтай сурагчид санал харагдахгүй",
    (await page.getByText("Энэ хичээл Standard багцад багтана").count()) === 0,
  );

  await page.getByRole("button", { name: "Цэс" }).click();
  const menu = await page.getByRole("menu").innerText();
  check("цэс багцын хугацааг харуулна", menu.includes("Standard ·"), menu.split("\n").join(" | "));

  check("console цэвэр", problems.length === 0, problems.slice(0, 3).join(" | "));
} finally {
  await session.close();
}

process.exit(summary("Paywall") > 0 ? 1 : 0);
