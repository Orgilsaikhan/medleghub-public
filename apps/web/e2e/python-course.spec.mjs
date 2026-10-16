/**
 * Python сургалт.
 *
 * Агуулга (модул, хичээл, кирилл бичвэр, Monaco-ийн Python горим) зөв
 * харагдаж байгааг шалгана. Кодын ГҮЙЦЭТГЭЛИЙГ `python-sandbox.spec.mjs`
 * тусад нь шалгадаг — тэр нь Pyodide ачаалдаг тул удаан ажиллана.
 */

import { SEED, check, editorCode, goto, login, newSession, summary } from "./harness.mjs";

const COURSE_SLUG = "python-programchlal";
const EXPECTED_MODULES = 29;
const EXPECTED_LESSONS = 44;

const session = await newSession({ width: 1600, height: 1000 });
const { page, problems } = session;

try {
  // «Класс ба объект» (#30) нь төлбөрт хэсэгт — багцтай хэрэглэгчээр.
  await login(page, SEED.standard);

  // --- Каталог -------------------------------------------------------------
  await goto(page, "/courses");
  const catalog = await page.locator("main").innerText();
  check("каталогт Python сургалт байна", catalog.includes("Python Программчлал"));
  check(
    "хичээлийн тоо зөв",
    catalog.includes(`${EXPECTED_LESSONS} хичээл`),
    catalog.match(/\d+ хичээл/g)?.join(", "),
  );

  // --- Сургалтын хуудас ----------------------------------------------------
  await goto(page, `/courses/${COURSE_SLUG}`);
  const detail = await page.locator("main").innerText();
  check("гарчиг зөв", (await page.locator("h1").innerText()) === "Python Программчлал");
  check("Модул 0 эхэнд байна", detail.includes("Модул 0 — Програмчлалын үндэс"));
  check("Модул 28 төгсгөлд байна", detail.includes("Модул 28 — Дунд шатны төсөл"));

  const moduleCount = (detail.match(/Модул \d+/g) ?? []).length;
  check(`${EXPECTED_MODULES} модул харагдана`, moduleCount === EXPECTED_MODULES, `${moduleCount}`);

  // --- Бүртгүүлээд эхний хичээл --------------------------------------------
  const enrollButton = page.getByRole("button", { name: /Сургалтад бүртгүүлэх/ });
  if (await enrollButton.count()) {
    await enrollButton.first().click();
  } else {
    await page
      .getByRole("link", { name: /Үргэлжлүүлэх|Дахин үзэх/ })
      .first()
      .click();
  }
  await page.waitForURL(/\/learn\//, { timeout: 25_000 });
  await page.waitForSelector(".monaco-editor", { timeout: 60_000 });
  await page.waitForTimeout(2500);

  check(
    "эхний хичээл нээгдэнэ",
    page.url().includes("programm-gej-yu-ve"),
    new URL(page.url()).pathname,
  );
  check(
    "монгол агуулга харагдана",
    // Эхнийх нь хичээлийн тайлбар, дараагийнх нь дасгалын даалгавар.
    (await page.locator(".lesson-prose").first().innerText()).includes("цай чанах жор"),
  );
  check("дасгалын даалгавар харагдана", (await page.locator("#exercise-title").count()) === 1);

  // --- Ажиллуулах боломжтой ------------------------------------------------
  // Гүйцэтгэлийн дэлгэрэнгүй шалгалт нь `python-sandbox.spec.mjs` дотор.
  check(
    "Ажиллуулах товч идэвхтэй",
    !(await page.getByRole("button", { name: "Код ажиллуулах" }).isDisabled()),
  );
  check("оролтын хэсэг нээгдэнэ", (await page.getByRole("button", { name: "Оролт" }).count()) > 0);

  // --- Monaco Python-ийг таньсан эсэх --------------------------------------
  const languages = await page.evaluate(() =>
    (window.monaco?.editor?.getModels?.() ?? []).map((model) => model.getLanguageId()).join(","),
  );
  check("Monaco Python горимд", languages.includes("python"), languages || "(monaco олдсонгүй)");
  check("өнгөт ялгаралт ажиллаж байна", (await page.locator(".mtk6, .mtk1").count()) > 0);

  // --- Дунд шатны хичээл ---------------------------------------------------
  await goto(page, `/learn/${COURSE_SLUG}/klass-ba-obekt`, { waitFor: ".monaco-editor" });
  await page.waitForFunction(
    () => document.querySelector(".view-lines")?.innerText.includes("class"),
    null,
    { timeout: 30_000 },
  );
  check("дунд шатны хичээл ачаална", (await page.locator("h1").innerText()) === "Класс ба объект");
  // Засварлагчид дасгалын эхлэл код, хуучин жишээ нь хичээлийн «Жишээ програм»-д.
  check("Python код зөв ачаалагдсан", (await editorCode(page)).includes("class Dans"));
  check(
    "жишээ програм тайлбарт үлдсэн",
    (await page.locator(".lesson-prose").first().innerText()).includes("class Oyutan"),
  );

  check("console цэвэр", problems.length === 0, problems.slice(0, 3).join(" | "));
} finally {
  await session.close();
}

process.exit(summary("Python course") > 0 ? 1 : 0);
