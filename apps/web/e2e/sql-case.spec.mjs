/**
 * SQL-ийн мөрдөгчийн хэрэг — асуулгаар хариултыг олж, «Хариулт» мөрөнд бичнэ.
 *
 * `apps/sql-runner` (`medleg_hot` сантай image) асаалттай байх ёстой. Энэ
 * файл нь дараахыг батална:
 *
 *   • Хэргийн хичээл «Хэрэг» хэсэг, «Хариулт» мөртэй, гараар дуусгах товчгүй,
 *   • Зөв хариулт хуудсанд (HTML, JSON) хэзээ ч ирэхгүй,
 *   • Эхлэл код `medleg_hot` дээр ажиллаж, хариултыг шууд харуулахгүй,
 *   • Буруу хариулт «Буруу байна», дараалан 3 удаа бол урам өгөх үг,
 *   • Зөв хариулт (том жижиг үсэг, зай үл тооно) хичээлийг дуусгаж, хадгална.
 */

import {
  API_URL,
  check,
  goto,
  newSession,
  registerNew,
  setEditorValue,
  summary,
} from "./harness.mjs";

const COURSE = "mssql-mysql-undes";
const CASE_LESSON = `/learn/${COURSE}/hereg-01-shoniin-duudlaga`;
const ANSWER = "Сарангэрэл";
const SOLUTION = "USE medleg_hot;\n\nTABLE duudlaga;\n";

/** Ажиллуулагчийн 10 секундийн хязгаар + сүлжээ. */
const RUN_TIMEOUT = 40_000;

const session = await newSession({ width: 1600, height: 1000 });
const { page, problems } = session;

/** API-г хөтчийн cookie-гоор — хуудсан доторх `fetch` нь хөгжүүлэлтийн CSP-д баригдана. */
async function api(path, init = {}) {
  const response = await page.context().request.fetch(`${API_URL}${path}`, {
    method: init.method ?? "GET",
    headers: init.headers,
    data: init.body,
  });
  return { status: response.status(), body: await response.json().catch(() => null) };
}

/** Кодыг ажиллуулаад console-ийн гаралтыг буцаана. `code` байхгүй бол анхны код. */
async function run(code) {
  await page
    .locator('[aria-label="Console цэвэрлэх"]')
    .click({ timeout: 1500 })
    .catch(() => {});
  if (code !== undefined) await setEditorValue(page, code);
  await page.getByRole("button", { name: "Код ажиллуулах" }).click();
  await page.waitForFunction(
    () => {
      const button = [...document.querySelectorAll("button")].find((element) =>
        element.textContent?.includes("Код ажиллуулах"),
      );
      return button && !button.disabled;
    },
    null,
    { timeout: RUN_TIMEOUT },
  );
  await page.waitForTimeout(250);
  return (await page.locator('[role="log"]').innerText()).replace(/^›\s*/gm, "").trim();
}

const answerInput = () => page.getByLabel("Хариулт", { exact: true });
const verdict = () => page.locator('[role="status"]').filter({ hasText: /\S/ }).last();

/** Хариулт бичиж «Шалгах» дарна, шалгалтын хариуг буцаана. */
async function answer(text) {
  await answerInput().fill(text);
  const response = page.waitForResponse((res) => res.url().includes("/answer"));
  await page.getByRole("button", { name: "Шалгах", exact: true }).click();
  await response;
  await page.waitForTimeout(300);
  return (await verdict().innerText()).trim();
}

try {
  await registerNew(page, "Мөрдөгч Шалгагч");
  const course = (await api(`/courses/${COURSE}`)).body;
  const enrolled = await api(`/courses/${course.id}/enroll`, { method: "POST" });
  check("сургалтад бүртгүүлэв", enrolled.status === 201, String(enrolled.status));

  const player = page.waitForResponse((res) => res.url().includes("/lessons/hereg-01"));
  await goto(page, CASE_LESSON, { waitFor: ".monaco-editor" });
  const playerJson = await (await player).text();

  // --- Хуудас ----------------------------------------------------------------------
  check(
    "«Хэрэг» гарчиг",
    (await page.getByRole("heading", { name: "Хэрэг", exact: true }).count()) === 1,
  );
  check("«Хариулт» мөр", await answerInput().isVisible());
  check(
    "гараар дуусгах товч алга",
    (await page.getByRole("button", { name: "Дуусгах" }).count()) === 0,
  );
  check("дуусгах тайлбар", (await page.getByText("Хэргийн хариултыг олж дуусгана").count()) > 0);
  check(
    "хариулт хичээлийн JSON-д алга",
    !playerJson.includes(ANSWER) && !playerJson.includes('"answers"'),
  );
  check("хариулт хуудсанд алга", !(await page.content()).includes(ANSWER));

  // --- Асуулга ------------------------------------------------------------------------
  const initial = await run();
  check("эхлэл код алдаагүй", !initial.includes("ERROR"), initial);
  check("эхлэл код хүснэгтүүдийг жагсаана", initial.includes("duudlaga"), initial);
  check("эхлэл код хариултыг харуулахгүй", !initial.includes(ANSWER), initial);

  const solved = await run(SOLUTION);
  check("шийдлийн асуулга хариултыг олно", solved.includes(ANSWER), solved);

  // --- Хариулт ------------------------------------------------------------------------
  check(
    "хоосон үед «Шалгах» идэвхгүй",
    await page.getByRole("button", { name: "Шалгах", exact: true }).isDisabled(),
  );

  const wrong = await answer("Батбаяр");
  check("буруу хариулт", wrong.includes("Буруу байна"), wrong);
  await answer("Нарангэрэл");
  await answer("Гэрэлмаа");
  const motivation = page.getByRole("dialog");
  check("3 буруу хариултын дараа урам өгөх үг", await motivation.isVisible().catch(() => false));
  await page.keyboard.press("Escape");
  await motivation.waitFor({ state: "hidden", timeout: 5000 }).catch(() => {});

  const right = await answer(`  ${ANSWER.toLowerCase()} `);
  check("зөв хариулт (жижиг үсэг, зай)", right.includes("Зөв! Хэрэг илэрлээ"), right);
  check(
    "дараагийн хичээлийн холбоос",
    (await page.getByRole("link", { name: "Дараагийн хичээл" }).count()) > 0,
  );
  check("хичээл дууссан", (await page.getByText("Дууссан", { exact: true }).count()) > 0);

  // --- Хадгалагдсан эсэх --------------------------------------------------------------
  await goto(page, CASE_LESSON, { waitFor: ".monaco-editor" });
  check(
    "дахин ачаалахад дууссан хэвээр",
    (await page.getByText("Дууссан", { exact: true }).count()) > 0,
  );
  const progress = await api(`/courses/${course.id}/progress`);
  check("ахицад тоологдсон", progress.body?.completed_lessons === 1, JSON.stringify(progress.body));

  check("console цэвэр", problems.length === 0, problems.slice(0, 3).join(" | "));
} finally {
  await session.close();
}

process.exit(summary("SQL мөрдөгчийн хэрэг") > 0 ? 1 : 0);
