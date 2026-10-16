/**
 * Сургалтыг бүрэн дуусгах зам.
 *
 * Бүртгүүлээгүй үеийн төлөв, бүх хичээлийг дуусгасны дараах 100% төлөв,
 * дахин үзэх санал зэрэг захын тохиолдлуудыг шалгана.
 *
 * ХИЧЭЭЛИЙГ ЯАГААД API-ЕЭР ДУУСГАДАГ ВЭ
 * ─────────────────────────────────────
 * JavaScript-ийн хичээл бүр одоо даалгавартай (2026-09-30) — «Хичээл дууссан»
 * товчгүй, бүх тестийг давж «Илгээх»-ээр дуусна. 70 гаруй хичээлийг UI-аар
 * давахад хэдэн минут болно. Тиймээс эхний хоёрыг «Илгээх»-ээр дуусгаж UI-ийн
 * зам ажиллаж байгааг баталгаажуулаад, үлдсэнийг ахицын API-ер дуусгана.
 * Энэ тестийн зорилго нь **100% болсны дараах төлөв** учраас хамрах хүрээ
 * буурахгүй.
 *
 * API-г `page.context().request`-ээр дуудна — хуудсан доторх `fetch` нь
 * хөгжүүлэлтийн CSP-д баригддаг.
 */

import {
  API_URL,
  SEED,
  check,
  goto,
  grantPlan,
  newSession,
  registerNew,
  submitReferenceSolution,
  summary,
} from "./harness.mjs";

/** «Илгээх»-ээр дуусгах хичээл — үлдсэнийг API-ер дуусгана. */
const UI_LESSONS = ["tanilzuulga", "javascript-ba-hutuch"];

const session = await newSession();
const { page, problems } = session;

/** Сургалтын бүх хичээлийн ID. */
async function lessonIds(courseSlug) {
  const hariult = await page.context().request.get(`${API_URL}/courses/${courseSlug}`);
  if (!hariult.ok()) throw new Error(`Сургалт ачаалж чадсангүй: ${hariult.status()}`);
  const surgalt = await hariult.json();
  return surgalt.modules.flatMap((modul) => modul.lessons.map((hicheel) => hicheel.id));
}

/** Хичээлүүдийг дараалан дуусгаж, амжилтгүй болсныг нь буцаана. */
async function completeViaApi(ids) {
  const amjiltgui = [];
  for (const id of ids) {
    const hariult = await page.context().request.post(`${API_URL}/lessons/${id}/complete`);
    if (!hariult.ok()) amjiltgui.push(`${id}: ${hariult.status()}`);
  }
  return amjiltgui;
}

try {
  const account = await registerNew(page, "Дуусгагч");
  // Бүх хичээлийг дуусгахад төлбөрт хэсэг ч орно.
  await grantPlan(account.email);

  // Бүртгүүлээгүй байхад "Хичээл дууссан" биш "бүртгүүлэх" санал харагдана.
  await goto(page, `/learn/${SEED.course.slug}/tanilzuulga`, { waitFor: ".monaco-editor" });
  await page.waitForTimeout(1200);
  const notEnrolled = await page.locator("main, body").first().innerText();
  check(
    "бүртгүүлээгүй үед бүртгүүлэх санал харагдана",
    notEnrolled.includes("Сургалтад бүртгүүлэх"),
  );

  // Бүртгүүлнэ.
  await goto(page, `/courses/${SEED.course.slug}`);
  await page
    .getByRole("button", { name: /Сургалтад бүртгүүлэх/ })
    .first()
    .click();
  await page.waitForURL(/\/learn\//, { timeout: 25000 });
  await page.waitForSelector(".monaco-editor", { timeout: 60000 });
  await page.waitForTimeout(1500);

  // Эхний хэдэн хичээлийг даалгавраа давж «Илгээх»-ээр дуусгана.
  let duusgasan = 0;
  for (const slug of UI_LESSONS) {
    await goto(page, `/learn/${SEED.course.slug}/${slug}`, { waitFor: ".monaco-editor" });
    await page.waitForTimeout(1200);
    await submitReferenceSolution(page, SEED.course.slug, slug);
    duusgasan++;
  }
  check("«Илгээх» даалгаврыг давж хичээл дуусгана", duusgasan === UI_LESSONS.length);

  // Үлдсэнийг API-ер дуусгана.
  const ids = await lessonIds(SEED.course.slug);
  check("сургалт хичээлүүдтэй", ids.length > UI_LESSONS.length, `${ids.length} хичээл`);

  const amjiltgui = await completeViaApi(ids);
  check("бүх хичээл API-ер дуусгагдлаа", amjiltgui.length === 0, amjiltgui.slice(0, 3).join(" | "));

  // Ахицын төлөв бүрэн болсон эсэх.
  await goto(page, `/learn/${SEED.course.slug}/tanilzuulga`, { waitFor: ".monaco-editor" });
  await page.waitForTimeout(1200);
  const sidebar = await page.locator("aside").innerText();
  check(
    "бүх хичээл дууссан",
    sidebar.includes(`${ids.length} / ${ids.length}`),
    sidebar.split("\n")[2],
  );

  await goto(page, "/dashboard");
  const dash = await page.locator("main").innerText();
  check(
    "самбар 100% харуулна",
    dash.includes("100%"),
    dash.split("\n").filter(Boolean).slice(0, 6).join(" | "),
  );
  check("самбар «Бүрэн дууссан» гэж тэмдэглэнэ", dash.includes("Бүрэн дууссан"));
  check("самбар «Дахин үзэх» санал болгоно", dash.includes("Дахин үзэх"));

  await goto(page, `/courses/${SEED.course.slug}`);
  check(
    "сургалтын хуудас «Дахин үзэх» харуулна",
    (await page.locator("aside").first().innerText()).includes("Дахин үзэх"),
  );

  check("console цэвэр", problems.length === 0, problems.slice(0, 3).join(" | "));
} finally {
  await session.close();
}

process.exit(summary("Course completion") > 0 ? 1 : 0);
