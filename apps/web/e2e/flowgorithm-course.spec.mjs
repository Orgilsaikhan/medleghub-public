/**
 * Flowgorithm: сайт дээрх блок схем ба автоматаар шалгагддаг даалгавар.
 *
 *   • Каталог, 8 модуль, даалгавар ба жишээ гаралт уншлагын хэсэгт харагдана,
 *   • Эхлэл схем жишээ тестэд унаж, дүрсийг засахад «Илгээх» хичээлийг дуусгана,
 *   • «Тусламж»-ийн жишиг шийдэл JSON биш блок схемээр харагдана,
 *   • Оролттой даалгаварт асуулт шалгалтад орохгүй, «Ажиллуулах» хэвээр асууна,
 *   • Дүрс нэмж байгуулсан схем нууц тестүүдийг давна,
 *   • Утасны өргөнд хуудас хэвтээгээр сунахгүй.
 */

import { check, goto, newSession, registerNew, summary } from "./harness.mjs";

const session = await newSession({ width: 1600, height: 1000 });
const { page, problems, requests } = session;
const courseSlug = "flowgorithm-undes";
const editor = '[data-testid="flow-editor"]';

/** Сайтын `/api/v1` proxy-оор — CSP-ийн `connect-src 'self'`-д багтана. */
function api(path, init) {
  return page.evaluate(
    async ([url, options]) => {
      const response = await fetch(url, { credentials: "include", ...options });
      return { status: response.status, body: await response.json().catch(() => null) };
    },
    [`/api/v1${path}`, init ?? {}],
  );
}

const testsPanel = () => page.locator('[role="log"][aria-label="Тест"]').innerText();

/** Товч дараад шалгалт дуусахыг (товчнууд дахин идэвхжихийг) хүлээнэ. */
async function press(name) {
  await page.getByRole("button", { name, exact: true }).click();
  await page.waitForFunction(() =>
    [...document.querySelectorAll("button")].some(
      (button) => button.textContent?.includes("Илгээх") && !button.disabled,
    ),
  );
  await page.waitForTimeout(300);
}

/** Сумны «+» дээр дарж шинэ (хоосон) дүрс нэмнэ. */
async function insertShape(connector, paletteLabel) {
  await page.getByRole("button", { name: `Дүрс нэмэх: ${connector}`, exact: true }).click();
  await page.getByRole("button", { name: paletteLabel }).click();
}

/** Схемийн дүрс дээр дарж талбаруудыг бөглөөд хадгална. */
async function fillShape(kind, index, fields) {
  await page.locator(`${editor} [data-node-kind="${kind}"]`).nth(index).click();
  const dialog = page.getByRole("dialog");
  await dialog.waitFor();
  for (const [id, value] of Object.entries(fields)) {
    const field = dialog.locator(`#flow-${id}`);
    if (id === "data-type") await field.selectOption(value);
    else await field.fill(value);
  }
  await dialog.getByRole("button", { name: "Хадгалах" }).click();
  await dialog.waitFor({ state: "hidden" });
}

async function openLesson(slug) {
  await goto(page, `/learn/${courseSlug}/${slug}`, { waitFor: editor });
  await page.locator(`${editor} [data-node-kind]`).first().waitFor();
}

try {
  await registerNew(page, "Схем Шалгагч");
  await goto(page, "/courses?category=flowgorithm");
  const catalog = await page.locator("main").innerText();
  check("Flowgorithm ангиллаар сургалт олдоно", catalog.includes("програмчлалын анхны алхам"));
  check("24 хичээлтэй", catalog.includes("24 хичээл"));

  await goto(page, `/courses/${courseSlug}`);
  const detail = await page.locator("main").innerText();
  check("8 модультай", (detail.match(/Модул \d+/g) ?? []).length === 8);

  const course = (await api(`/courses/${courseSlug}`)).body;
  const enrolled = await api(`/courses/${course.id}/enroll`, { method: "POST" });
  check("сургалтад бүртгүүлэв", enrolled.status === 201, String(enrolled.status));

  // --- Модул 0: Input-ууд бэлэн, сурагч Output-ийг засна -------------------------
  await openLesson("program-gej-yu-ve");
  const body = await page.locator("body").innerText();
  check(
    "даалгавар ба жишээ гаралт харагдана",
    body.includes("Даалгавар") && body.includes("Жишээ гаралт 1") && body.includes("5500"),
  );
  check(
    "даалгавартай хичээлд «Хичээл дууссан» товч байхгүй",
    (await page.getByRole("button", { name: "Хичээл дууссан" }).count()) === 0,
  );

  await press("Тест ажиллуулах");
  let panel = await testsPanel();
  check(
    "эхлэл схем жишээ тестэд унана",
    panel.includes("0/1 тест амжилттай") && panel.includes("3500"),
    panel.slice(0, 200),
  );

  await fillShape("output", 0, { expression: "price1 + price2" });
  await press("Илгээх");
  panel = await testsPanel();
  check("засварласан схем бүх тестийг давна", panel.includes("5/5 тест амжилттай"), panel);
  check("хичээл дууслаа гэж мэдэгдэнэ", panel.includes("хичээл дууслаа"), panel.slice(0, 200));
  let progress = (await api(`/courses/${course.id}/progress`)).body;
  check("ахиц сервер дээр хадгалагдав", progress.completed_lessons === 1, JSON.stringify(progress));

  // --- Тусламж: жишиг шийдэл блок схемээр -----------------------------------------
  await page.getByRole("button", { name: "Тусламж" }).click();
  await page.getByRole("dialog").getByRole("button", { name: "Хариуг харах" }).click();
  await page.getByText("Жишиг шийдэл").waitFor({ timeout: 15_000 });
  const help = page.getByRole("dialog");
  // Схемийн component-ийг dynamic import-оор ачаална.
  const solutionShape = help.locator('[aria-label="Блок схем"] [data-node-kind="output"]');
  await solutionShape.first().waitFor({ timeout: 15_000 });
  const helpText = await help.innerText();
  check(
    "жишиг шийдэл блок схемээр харагдана",
    (await solutionShape.count()) === 1 &&
      (await solutionShape.getAttribute("title")) === "price1 + price2",
  );
  check(
    "JSON ба «Хуулах» товч харагдахгүй",
    !helpText.includes("medleghub-flowgorithm") &&
      (await help.getByRole("button", { name: "Хуулах" }).count()) === 0,
    helpText.slice(0, 200),
  );
  check("тусламжийг нэг удаа татна", requests.filter((url) => url.endsWith("/help")).length === 1);
  await page.keyboard.press("Escape");
  await help.waitFor({ state: "hidden" });

  // --- Оролттой даалгавар: асуулт шалгалтад орохгүй -------------------------------
  await openLesson("input-mendchilgee");
  check(
    "оролтын дүрмийг тайлбарлана",
    (await page.locator("body").innerText()).includes("сүүлчийн Input-ээс хойшх"),
  );

  await page.getByRole("button", { name: "Ажиллуулах", exact: true }).click();
  await page.locator("#flow-live-input").fill("Сараа");
  await page.getByRole("button", { name: "Оруулах" }).click();
  const outputLog = page.locator('[role="log"][aria-label="Схемийн гаралт"]');
  await outputLog.filter({ hasText: "Сайн уу, Сараа!" }).waitFor();
  const output = await outputLog.innerText();
  check(
    "«Ажиллуулах» асуултыг харуулна",
    output.includes("Нэрээ оруулна уу:") && output.includes("Сайн уу, Сараа!"),
    output,
  );

  await press("Тест ажиллуулах");
  panel = await testsPanel();
  check(
    "тестийн гаралтад асуулт орохгүй",
    panel.includes("0/1 тест амжилттай") &&
      panel.includes("Сайн уу, Сараа!") &&
      !panel.includes("Нэрээ оруулна уу:"),
    panel.slice(0, 300),
  );

  // Хотыг асууж авах гурван дүрс нэмээд эцсийн Output-ийг засна.
  await insertShape("Main 2", "Declare — Хувьсагч зарлах");
  await fillShape("declare", 1, { name: "city", "data-type": "String" });
  await insertShape("Main 5", "Output — Гаралт харуулах");
  await fillShape("output", 1, { expression: '"Хаана амьдардаг вэ?"' });
  await insertShape("Main 6", "Input — Оролт авах");
  await fillShape("input", 1, { name: "city" });
  await fillShape("output", 2, {
    expression: '"Сайн уу, " & name & "! " & city & " хотын цаг агаар ямар байна?"',
  });

  await press("Илгээх");
  panel = await testsPanel();
  check("байгуулсан схем нууц тестүүдийг давна", panel.includes("4/4 тест амжилттай"), panel);
  progress = (await api(`/courses/${course.id}/progress`)).body;
  check("хоёр дахь хичээл дууслаа", progress.completed_lessons === 2, JSON.stringify(progress));

  // --- Төгсгөлийн төсөл, утасны өргөн ---------------------------------------------
  await openLesson("tusul-dundaj-soril");
  check("Төгсгөлийн төсөл нээгдэнэ", (await page.locator("h1").innerText()).includes("Төсөл 2"));
  check(
    "Дараагийн сургалтын холбоос зөв",
    (await page.locator('.lesson-prose a[href="/courses/python-programchlal"]').count()) === 1,
  );
  await page.setViewportSize({ width: 390, height: 844 });
  check("Утасны өргөнд агуулга харагдана", await page.locator(".lesson-prose").first().isVisible());
  check(
    "Хуудас хэвтээгээр сунахгүй",
    await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth),
  );
  check("Хөтчийн алдаагүй", problems.length === 0, problems.slice(0, 3).join(" | "));
} finally {
  await session.close();
}

process.exit(summary("Flowgorithm course") > 0 ? 1 : 0);
