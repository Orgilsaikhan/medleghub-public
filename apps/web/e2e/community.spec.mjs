/**
 * Community.
 *
 *   • Зочинд цэсэнд «Community» харагдахгүй, `/community` нэвтрэх рүү илгээнэ,
 *   • Эхний удаа ороход дүрэм (7 → 14 → 30 хоног → бүрмөсөн) хаагдахгүй цонхоор гарна,
 *   • Нийтлэл хэл, төрлийн шошгогүй нийтлэгдэхгүй,
 *   • Нийтлэл Markdown-аар (код блок) харагдана, зураг, HTML харагдахгүй,
 *   • Лайк асааж, унтраана; сэтгэгдэл нэмнэ,
 *   • Хэлээр шүүнэ,
 *   • Өөр хэрэглэгч нийтлэл, сэтгэгдлийг мэдэгдэнэ — устгах товчгүй,
 *   • Админ гомдлыг «Санал хүсэлт»-д харж, холбоосоор орж устгана,
 *   • Админ зохиогчийг түдгэлзүүлнэ — тэр зөвхөн уншина; админ цуцална.
 */

import {
  BASE_URL,
  SEED,
  check,
  goto,
  login,
  logout,
  newSession,
  registerNew,
  summary,
} from "./harness.mjs";

const session = await newSession({ width: 1280, height: 900 });
const { page, problems } = session;

const TITLE = `C++ дээр vector-ийг яаж эрэмбэлэх вэ? ${Date.now()}`;
const BODY = [
  "Тоонуудын vector-ийг багаас их рүү эрэмбэлмээр байна.",
  "",
  "```cpp",
  "std::vector<int> v = {3, 1, 2};",
  "```",
  "",
  '<img src="x" onerror="window.__xss = 1">',
  "![зураг](https://example.com/a.png)",
].join("\n");
const COMMENT = "std::sort(v.begin(), v.end()) ашиглаарай.";

/** Radix Select — шошгоор нь нээгээд сонголтыг дарна. */
async function choose(label, option) {
  await page.getByRole("combobox", { name: label }).click();
  await page.getByRole("option", { name: option, exact: true }).click();
}

const guidelines = () => page.getByRole("dialog", { name: "Community-ийн дүрэм" });

async function acceptGuidelines() {
  await guidelines().getByRole("button", { name: "Дүрмийг зөвшөөрч байна" }).click();
  await guidelines().waitFor({ state: "hidden", timeout: 10_000 });
}

/** Seed-ийн админ өмнө нь зөвшөөрсөн байж магадгүй. */
async function acceptIfAsked() {
  await page.waitForTimeout(1200);
  if (await guidelines().isVisible()) await acceptGuidelines();
}

const likeButton = () => page.getByRole("button", { name: /^Таалагдлаа/ });
/** Товчны текстэд дэлгэц уншигчийн шошго ч орно — сүүлийн тоог л авна. */
const likeCount = async () => Number((await likeButton().innerText()).match(/(\d+)\s*$/)?.[1]);

try {
  // --- Зочин -------------------------------------------------------------------
  await goto(page, "/courses");
  check(
    "зочны цэсэнд «Community» байхгүй",
    (await page.getByRole("link", { name: "Community", exact: true }).count()) === 0,
  );
  await goto(page, "/community");
  await page.waitForURL(/\/login\?next=%2Fcommunity/, { timeout: 15_000 });
  check("зочин нэвтрэх хуудас руу шилжинэ", true);

  // --- Нийтлэл бичих -----------------------------------------------------------
  const asker = await registerNew(page, "Асуулт Асуугч");
  await page.getByRole("link", { name: "Community", exact: true }).first().click();
  await page.waitForURL(/\/community$/, { timeout: 15_000 });
  await page.getByRole("heading", { name: "Community", level: 1 }).waitFor();
  check("цэснээс Community руу орно", true);

  // --- Дүрэм ---------------------------------------------------------------------
  await guidelines().waitFor({ timeout: 10_000 });
  const rulesText = await guidelines().innerText();
  check(
    "эхний удаа дүрэм гарч, шийтгэлийн шатлалыг тайлбарлана",
    [
      "1-р зөрчил — 7 хоног",
      "2-р зөрчил — 14 хоног",
      "3-р зөрчил — 30 хоног",
      "4-р зөрчлөөс",
    ].every((line) => rulesText.includes(line)) && rulesText.includes("бүрмөсөн"),
  );
  await page.keyboard.press("Escape");
  await page.waitForTimeout(400);
  check("дүрмийг Escape-ээр хаахгүй", await guidelines().isVisible());
  await acceptGuidelines();
  check("зөвшөөрөхөд дүрэм хаагдана", true);
  await goto(page, "/community");
  await page.waitForTimeout(800);
  check("дахин ороход дүрэм гарахгүй", !(await guidelines().isVisible()));
  await page.getByRole("button", { name: "Дүрэм" }).click();
  await guidelines().waitFor();
  await page.keyboard.press("Escape");
  await guidelines().waitFor({ state: "hidden" });
  check("«Дүрэм» товчоор дахин уншиж, хааж болно", true);

  await page.getByRole("link", { name: "Нийтлэл бичих" }).first().click();
  await page.waitForURL(/\/community\/new$/, { timeout: 15_000 });
  await page.waitForTimeout(700);
  await page.getByRole("button", { name: "Нийтлэх" }).click();
  await page.getByText("Хэлээ сонгоно уу.").waitFor({ timeout: 5_000 });
  check("хэлгүй нийтлэл илгээгдэхгүй", true);
  check("төрөлгүй нийтлэл илгээгдэхгүй", await page.getByText("Төрлөө сонгоно уу.").isVisible());

  await choose("Хэл", "C++");
  await choose("Төрөл", "Тусламж");
  await page.fill("#post-title", TITLE);
  await page.fill("#post-body", BODY);
  await page.getByRole("button", { name: "Нийтлэх" }).click();
  await page.waitForURL(/\/community\/[0-9a-f-]{36}$/, { timeout: 15_000 });
  const postUrl = new URL(page.url()).pathname;
  await page.getByRole("heading", { name: TITLE, level: 1 }).waitFor();
  check("нийтлэгдээд нийтлэлийн хуудас руу орно", true);

  const article = page.locator("article");
  const articleText = await article.innerText();
  check(
    "хэл, төрлийн шошго харагдана",
    /C\+\+/.test(articleText) && articleText.includes("Тусламж"),
  );
  check(
    "код блок `pre` болж харагдана",
    (await article.locator("pre").innerText()).includes("std::vector<int>"),
  );
  check("нийтлэлд зураг гарахгүй", (await article.locator("img").count()) === 0);
  check("HTML ажиллахгүй", (await page.evaluate(() => window.__xss)) === undefined);

  // --- Лайк -------------------------------------------------------------------
  await likeButton().click();
  await page.waitForTimeout(600);
  check(
    "лайк дарахад 1 болж, дарагдсан төлөвтэй",
    (await likeButton().getAttribute("aria-pressed")) === "true" && (await likeCount()) === 1,
  );
  await likeButton().click();
  await page.waitForTimeout(600);
  check(
    "дахин дарахад 0 болно",
    (await likeButton().getAttribute("aria-pressed")) === "false" && (await likeCount()) === 0,
  );
  await likeButton().click();
  await page.waitForTimeout(600);

  // --- Сэтгэгдэл -----------------------------------------------------------------
  await page.getByRole("button", { name: "Илгээх" }).click();
  await page.getByText("Сэтгэгдлээ бичнэ үү.").waitFor({ timeout: 5_000 });
  check("хоосон сэтгэгдэл илгээгдэхгүй", true);
  await page.fill("#comment-body", COMMENT);
  await page.getByRole("button", { name: "Илгээх" }).click();
  const comments = page.locator('section[aria-labelledby="comments-title"] li');
  await comments.first().waitFor({ timeout: 10_000 });
  check(
    "сэтгэгдэл жагсаалтад нэмэгдэнэ",
    (await comments.first().innerText()).includes("std::sort"),
  );
  check("сэтгэгдлийн талбар цэвэрлэгдэнэ", (await page.inputValue("#comment-body")) === "");
  check(
    "өөрийн нийтлэлд «Мэдэгдэх» товч байхгүй",
    (await page.getByRole("button", { name: "Мэдэгдэх" }).count()) === 0,
  );

  // --- Жагсаалт ба шүүлтүүр -----------------------------------------------------
  await goto(page, "/community");
  const card = page.locator("article", { hasText: TITLE });
  await card.waitFor({ timeout: 15_000 });
  const cardText = await card.innerText();
  check(
    "жагсаалтад код блокгүй богино хэсэг",
    cardText.includes("Тоонуудын vector-ийг") && !cardText.includes("std::vector"),
  );
  check(
    "карт дээр 1 лайк, 1 сэтгэгдэл",
    /Таалагдлаа:\s*1/.test(cardText) && /Сэтгэгдэл:\s*1/.test(cardText),
  );

  await choose("Хэл", "C++");
  await page.waitForURL(/language=cpp/, { timeout: 10_000 });
  await card.waitFor({ timeout: 10_000 });
  check("C++ шүүлтүүрт нийтлэл харагдана", true);
  await choose("Хэл", "Python");
  await page.waitForURL(/language=python/, { timeout: 10_000 });
  await page.waitForTimeout(1200);
  check("Python шүүлтүүрт нийтлэл харагдахгүй", (await card.count()) === 0);

  // --- Өөр хэрэглэгч мэдэгдэнэ --------------------------------------------------
  await logout(page);
  await registerNew(page, "Мэдэгдэгч");
  await goto(page, postUrl);
  // Дүрмийн цонх нээлттэй үед ард нь байгаа хуудас дэлгэц уншигчаас нуугдана.
  await guidelines().waitFor({ timeout: 15_000 });
  check("нийтлэлийн холбоосоор шууд орсон ч дүрэм гарна", true);
  await acceptGuidelines();
  await page.getByRole("heading", { name: TITLE, level: 1 }).waitFor({ timeout: 15_000 });
  check(
    "бусдын нийтлэлд устгах товч байхгүй",
    (await page.getByRole("button", { name: "Устгах" }).count()) === 0,
  );

  await page.locator("article").getByRole("button", { name: "Мэдэгдэх" }).click();
  const dialog = page.getByRole("dialog");
  await dialog.waitFor();
  await choose("Шалтгаан", "Доромжилсон, зохисгүй агуулга");
  await dialog.getByLabel("Нэмэлт тайлбар (заавал биш)").fill("E2E гомдол");
  await dialog.getByRole("button", { name: "Мэдэгдэх" }).click();
  await page
    .locator("[data-sonner-toast]", { hasText: "Админ шалгаж үзнэ" })
    .first()
    .waitFor({ timeout: 10_000 });
  check("нийтлэлийн гомдол илгээгдэнэ", true);

  await page.waitForTimeout(500);
  await comments.first().getByRole("button", { name: "Мэдэгдэх" }).click();
  await dialog.waitFor();
  await dialog.getByRole("button", { name: "Мэдэгдэх" }).click();
  await page.waitForTimeout(1500);
  check("сэтгэгдлийн гомдол илгээгдэнэ", (await dialog.count()) === 0);

  // --- Админ гомдлыг харж, устгана ----------------------------------------------
  await logout(page);
  await login(page, SEED.admin);
  await goto(page, "/admin/feedback");
  const report = page.locator("li", { hasText: TITLE }).filter({ hasText: "E2E гомдол" });
  await report.waitFor({ timeout: 15_000 });
  const reportText = await report.innerText();
  check(
    "админд «Гомдол» төрлөөр ирнэ",
    reportText.includes("Гомдол") && reportText.includes("Доромжилсон"),
  );
  const commentReport = page.locator("li", { hasText: "Гомдол · Сэтгэгдэл" }).filter({
    hasText: "std::sort",
  });
  check("сэтгэгдлийн гомдол ирнэ", (await commentReport.count()) > 0);

  await commentReport
    .first()
    .getByRole("link", { name: /#comment-/ })
    .click();
  await page.waitForURL(/\/community\/.+/, { timeout: 15_000 });
  await page.locator("h1", { hasText: TITLE }).waitFor({ timeout: 15_000 });
  await acceptIfAsked();
  check(
    "гомдлын холбоос сэтгэгдлийг тодруулна",
    (await comments.first().getAttribute("class")).includes("bg-accent"),
  );

  // --- Админ зохиогчийг түдгэлзүүлнэ ---------------------------------------------
  await page.locator("article").getByRole("button", { name: "Түдгэлзүүлэх" }).click();
  const suspendDialog = page.getByRole("dialog", { name: "Хэрэглэгчийг түдгэлзүүлэх" });
  await suspendDialog.waitFor();
  await suspendDialog.getByRole("button", { name: "Түдгэлзүүлэх" }).click();
  check(
    "шалтгаангүй түдгэлзүүлэхгүй",
    await suspendDialog.getByText("Шалтгааныг дор хаяж 5 тэмдэгтээр").isVisible(),
  );
  await suspendDialog
    .getByLabel("Шалтгаан (хэрэглэгчид харагдана)")
    .fill("E2E: бусдыг доромжилсон нийтлэл.");
  await suspendDialog.getByRole("button", { name: "Түдгэлзүүлэх" }).click();
  await page
    .locator("[data-sonner-toast]", { hasText: "түдгэлзлээ (1-р удаа)" })
    .waitFor({ timeout: 10_000 });
  check("эхний зөрчилд 1-р удаа түдгэлзүүлнэ", true);

  await comments.first().getByRole("button", { name: "Устгах" }).click();
  await page.getByRole("dialog").getByRole("button", { name: "Устгах" }).click();
  await page.waitForTimeout(1000);
  check("админ сэтгэгдэл устгана", (await comments.count()) === 0);

  await page.locator("article").getByRole("button", { name: "Устгах" }).click();
  await page.getByRole("dialog").getByRole("button", { name: "Устгах" }).click();
  await page.waitForURL(/\/community$/, { timeout: 15_000 });
  await page.waitForTimeout(1200);
  check("админ нийтлэл устгана", (await page.locator("article", { hasText: TITLE }).count()) === 0);

  await goto(page, postUrl);
  await page.getByText("Нийтлэл олдсонгүй").waitFor({ timeout: 15_000 });
  check("устгасан нийтлэл «олдсонгүй»", true);

  await goto(page, "/admin/community");
  const suspensionRow = page.locator("li", { hasText: asker.email });
  await suspensionRow.waitFor({ timeout: 15_000 });
  const suspensionText = await suspensionRow.innerText();
  check(
    "админы жагсаалтад идэвхтэй түдгэлзүүлэлт",
    suspensionText.includes("Идэвхтэй") &&
      suspensionText.includes("1-р удаа") &&
      suspensionText.includes("доромжилсон"),
  );

  // --- Түдгэлзсэн хэрэглэгч зөвхөн уншина -----------------------------------------
  await logout(page);
  await login(page, asker);
  await goto(page, "/community");
  const banner = page.getByRole("status").filter({ hasText: "түдгэлзсэн" });
  await banner.waitFor({ timeout: 15_000 });
  const bannerText = await banner.innerText();
  check(
    "түдгэлзсэн тухай огноо, шалтгаантай мэдэгдэл",
    bannerText.includes("хүртэл") && bannerText.includes("доромжилсон"),
  );
  check(
    "түдгэлзсэн үед «Нийтлэл бичих» байхгүй",
    (await page.getByRole("link", { name: "Нийтлэл бичих" }).count()) === 0,
  );
  await goto(page, "/community/new");
  await banner.waitFor({ timeout: 15_000 });
  check(
    "түдгэлзсэн үед нийтлэлийн маягт гарахгүй",
    (await page.locator("#post-title").count()) === 0,
  );

  // --- Админ цуцална -------------------------------------------------------------
  await logout(page);
  await login(page, SEED.admin);
  await goto(page, "/admin/community");
  await suspensionRow.getByRole("button", { name: "Цуцлах" }).click();
  await page
    .locator("[data-sonner-toast]", { hasText: "Түдгэлзүүлэлт цуцлагдлаа" })
    .waitFor({ timeout: 10_000 });
  await page.waitForTimeout(1000);
  check("цуцалсан түдгэлзүүлэлт идэвхтэй жагсаалтаас гарна", (await suspensionRow.count()) === 0);

  // Устгасан нийтлэлийн 404 нь хүлээгдсэн хариу.
  const unexpected = problems.filter((line) => !line.includes("404"));
  check("console цэвэр", unexpected.length === 0, unexpected.slice(0, 3).join(" | "));
} finally {
  await session.close();
}

console.log(`(${BASE_URL})`);
process.exit(summary("Community") > 0 ? 1 : 0);
