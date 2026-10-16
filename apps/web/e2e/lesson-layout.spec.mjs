/**
 * Хичээлийн дэлгэцийн бүтэц.
 *
 * Гурван зүйлийг батална:
 *   • Хуудас БҮХЭЛДЭЭ гүйлгэгдэхгүй — зөвхөн доторх хэсгүүд гүйлгэгдэнэ.
 *     Үгүй бол агуулга дуусахад хоосон дэвсгэр рүү гүйлгэгдэнэ.
 *   • Зүүн талын хөтөлбөрийг эвхэж, кодод илүү зай гаргаж болно.
 *   • Тайлбар ба засварлагчийн хоорондын зурвасыг чирж, эсвэл товчоор
 *     эвхэж хэмжээг өөрчилж болно. Сонголт нь хадгалагдана.
 *   • Анхдагч «шинэ» байрлал: засварлагч зүүн, «Заавар» баруун. Дээд мөрний
 *     товчоор «хуучин» (заавар дээр) болгоход бүртгэлд хадгалагдаж, дахин
 *     ачаалсан ч үлдэнэ. Тест төгсгөлд нь шинэ байрлалыг буцааж тавина.
 */

import { SEED, check, goto, login, newSession, summary } from "./harness.mjs";

const LESSON = "/learn/javascript-undes/tanilzuulga";
const SECOND_LESSON = "/learn/javascript-undes/huvisagch";

const CURRICULUM = "Хөтөлбөр";
const CONTENT = "Хичээлийн агуулга";
const INSTRUCTIONS = "Заавар";
const TO_LEGACY = "Хуучин байрлал";
const TO_NEW = "Шинэ байрлал";

/** Шинэ байрлалд засварлагч «Заавар»-ын зүүн талд, ижил мөрөнд байна. */
async function sideBySide(page) {
  const editor = await page.locator(".monaco-editor").first().boundingBox();
  const instructions = await page.getByRole("region", { name: INSTRUCTIONS }).boundingBox();
  if (!editor || !instructions) return false;
  return editor.x + editor.width <= instructions.x + 2 && Math.abs(editor.y - instructions.y) < 120;
}

/** Хуудас бүхэлдээ хэдэн пиксел гүйлгэгдэх боломжтой вэ. */
async function pageOverflow(page) {
  return page.evaluate(() => {
    const root = document.scrollingElement ?? document.documentElement;
    return root.scrollHeight - root.clientHeight;
  });
}

/** Тайлбарын хэсгийн өндөр. */
async function readingHeight(page) {
  const box = await page.locator(`[role="region"][aria-label="${CONTENT}"]`).boundingBox();
  return box ? Math.round(box.height) : 0;
}

const session = await newSession({ width: 1600, height: 900 });
const { page, problems } = session;

try {
  await login(page, SEED.student);
  await goto(page, LESSON, { waitFor: ".monaco-editor" });

  // --- Шинэ байрлал (анхдагч) ----------------------------------------------------
  await page.getByRole("region", { name: INSTRUCTIONS }).waitFor({ timeout: 15_000 });
  check("анхдагч нь шинэ байрлал: засварлагч зүүн, заавар баруун", await sideBySide(page));
  check("шинэ байрлалд хуудас гүйлгэгдэхгүй", (await pageOverflow(page)) <= 2);
  check(
    "шинэ байрлалд тайлбар ба засварлагчийн хуваагч байхгүй",
    (await page.getByRole("separator", { name: CONTENT }).count()) === 0,
  );

  // Хуучин байрлал руу — доорх шалгалтууд түүн дээр.
  await page.getByRole("button", { name: TO_LEGACY }).click();
  await page.getByRole("separator", { name: CONTENT }).waitFor({ timeout: 10_000 });
  check(
    "товчоор хуучин байрлал болно",
    (await page.getByRole("region", { name: INSTRUCTIONS }).count()) === 0,
  );
  await page.reload();
  await page.waitForSelector(".monaco-editor", { timeout: 60_000 });
  await page.getByRole("separator", { name: CONTENT }).waitFor({ timeout: 15_000 });
  check("хуучин байрлал дахин ачаалсан ч хадгалагдана", true);

  // --- Хуудас гүйлгэгдэхгүй ------------------------------------------------
  check(
    "хуудас бүхэлдээ гүйлгэгдэхгүй",
    (await pageOverflow(page)) <= 2,
    `${await pageOverflow(page)} px`,
  );

  // Гүйлгэхийг оролдоод ч байрандаа үлдэнэ.
  await page.mouse.wheel(0, 3000);
  await page.waitForTimeout(400);
  const scrolled = await page.evaluate(
    () => (document.scrollingElement ?? document.documentElement).scrollTop,
  );
  check("гүйлгэхийг оролдоход хөдлөхгүй", scrolled === 0, `scrollTop=${scrolled}`);

  // Харин тайлбарын хэсэг нь ДОТРОО гүйлгэгдэнэ. Богино хичээлийн агуулга нь
  // хэсэгтээ багтаж магадгүй тул эхлээд хэсгийг нарийсгаж баталгаажуулна.
  await page.getByRole("separator", { name: CONTENT }).focus();
  for (let i = 0; i < 6; i += 1) await page.keyboard.press("ArrowUp");
  await page.waitForTimeout(400);

  const readingScroll = await page.evaluate((label) => {
    const pane = document.querySelector(`[role="region"][aria-label="${label}"]`);
    if (!pane) return null;
    pane.scrollTop = 120;
    return { top: pane.scrollTop, overflowing: pane.scrollHeight > pane.clientHeight };
  }, CONTENT);
  check(
    "тайлбарын хэсэг дотроо гүйлгэгдэнэ",
    readingScroll?.overflowing && readingScroll.top > 0,
    JSON.stringify(readingScroll),
  );

  // Дараагийн шалгалтуудад нөлөөлөхгүйн тулд хэмжээг буцаана.
  for (let i = 0; i < 6; i += 1) await page.keyboard.press("ArrowDown");
  await page.waitForTimeout(400);

  // --- Хөтөлбөрийг эвхэх ---------------------------------------------------
  const sidebarToggle = page.getByRole("button", { name: CURRICULUM });
  const sidebar = page.locator("aside").first();

  const openWidth = (await sidebar.boundingBox())?.width ?? 0;
  check("хөтөлбөр анхандаа нээлттэй", openWidth > 200, `${Math.round(openWidth)} px`);

  await sidebarToggle.click();
  await page.waitForTimeout(500);
  const closedWidth = (await sidebar.boundingBox())?.width ?? 0;
  check("эвхэхэд өргөн нь тэг болно", closedWidth < 2, `${Math.round(closedWidth)} px`);

  const editorAfterCollapse =
    (await page.locator(".monaco-editor").first().boundingBox())?.width ?? 0;
  check(
    "засварлагч илүү өргөн болно",
    editorAfterCollapse > 1200,
    `${Math.round(editorAfterCollapse)} px`,
  );

  // Эвхэгдсэн хөтөлбөр рүү Tab-аар орж болохгүй (`inert`).
  const reachable = await page.evaluate(() => {
    const aside = document.querySelector("aside");
    const link = aside?.querySelector("a");
    if (!link) return false;
    link.focus();
    return document.activeElement === link;
  });
  check("эвхэгдсэн хөтөлбөр фокус авахгүй", reachable === false);

  await sidebarToggle.click();
  await page.waitForTimeout(500);
  check("дахин нээгдэнэ", ((await sidebar.boundingBox())?.width ?? 0) > 200);

  // Сонголт хадгалагдана.
  await sidebarToggle.click();
  await page.waitForTimeout(400);
  await goto(page, SECOND_LESSON, { waitFor: ".monaco-editor" });
  check(
    "эвхсэн төлөв хичээл солиход хадгалагдана",
    ((await sidebar.boundingBox())?.width ?? 0) < 2,
  );
  await sidebarToggle.click();
  await page.waitForTimeout(400);

  // --- Хэмжээ өөрчлөх ------------------------------------------------------
  const separator = page.getByRole("separator", { name: CONTENT });
  check("хуваагч зурвас байна", (await separator.count()) === 1);

  const before = await readingHeight(page);

  // Гараар: дээш сум дарахад тайлбарын хэсэг багасна.
  await separator.focus();
  await page.keyboard.press("ArrowUp");
  await page.keyboard.press("ArrowUp");
  await page.waitForTimeout(400);
  const afterKeys = await readingHeight(page);
  check("сум товчоор багасна", afterKeys < before, `${before} → ${afterKeys}`);

  await page.keyboard.press("ArrowDown");
  await page.keyboard.press("ArrowDown");
  await page.keyboard.press("ArrowDown");
  await page.waitForTimeout(400);
  check("сум товчоор томорно", (await readingHeight(page)) > afterKeys);

  // Хулганаар чирэх.
  const box = await separator.boundingBox();
  const dragFrom = { x: box.x + box.width / 2, y: box.y + box.height / 2 };
  const dragged = await readingHeight(page);

  await page.mouse.move(dragFrom.x, dragFrom.y);
  await page.mouse.down();
  await page.mouse.move(dragFrom.x, dragFrom.y - 180, { steps: 12 });
  await page.mouse.up();
  await page.waitForTimeout(400);
  check("чирэхэд хэмжээ өөрчлөгдөнө", (await readingHeight(page)) < dragged - 100);

  // Товчоор бүрэн эвхэх.
  const collapseButton = page.getByRole("button", { name: CONTENT });
  await collapseButton.click();
  await page.waitForTimeout(400);
  check("тайлбарыг бүрэн эвхэж болно", (await readingHeight(page)) <= 1);

  const editorWhileCollapsed =
    (await page.locator(".monaco-editor").first().boundingBox())?.height ?? 0;
  check(
    "эвхсэн үед засварлагч томорно",
    editorWhileCollapsed > 250,
    `${Math.round(editorWhileCollapsed)} px`,
  );

  await collapseButton.click();
  await page.waitForTimeout(400);
  check("дахин дэлгэнэ", (await readingHeight(page)) > 1);

  // Эвхсэн/дэлгэсэн үед ч хуудас гүйлгэгдэхгүй.
  check("хэмжээ өөрчилсний дараа ч гүйлгэгдэхгүй", (await pageOverflow(page)) <= 2);

  // --- Нарийн дэлгэц -------------------------------------------------------
  await page.setViewportSize({ width: 900, height: 800 });
  await page.waitForTimeout(600);
  check(
    "нарийн дэлгэц дээр ч гүйлгэгдэхгүй",
    (await pageOverflow(page)) <= 2,
    `${await pageOverflow(page)} px`,
  );

  await page.setViewportSize({ width: 420, height: 820 });
  await page.waitForTimeout(600);
  check(
    "гар утсан дээр ч гүйлгэгдэхгүй",
    (await pageOverflow(page)) <= 2,
    `${await pageOverflow(page)} px`,
  );

  // --- Шинэ байрлал руу буцаах (анхдагч) ----------------------------------------------
  await page.setViewportSize({ width: 1600, height: 900 });
  await page.waitForTimeout(600);
  await page.getByRole("button", { name: TO_NEW }).click();
  await page.getByRole("region", { name: INSTRUCTIONS }).waitFor({ timeout: 10_000 });
  check("товчоор шинэ байрлал руу буцна", await sideBySide(page));
  await page.setViewportSize({ width: 420, height: 820 });
  await page.waitForTimeout(600);
  check(
    "шинэ байрлал гар утсан дээр «Унших / Код» tab",
    (await page.getByRole("tab", { name: "Код" }).count()) === 1,
  );
  check("шинэ байрлалд гар утсан дээр ч гүйлгэгдэхгүй", (await pageOverflow(page)) <= 2);

  check("console цэвэр", problems.length === 0, problems.slice(0, 3).join(" | "));
} finally {
  await session.close();
}

process.exit(summary("Lesson layout") > 0 ? 1 : 0);
