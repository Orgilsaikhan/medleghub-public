/**
 * MedlegHub Live — AI Study.
 *
 *   • Толгойд «Live» холбоос; `/live` дээр хэрэглээ, файл оруулах хэсэг,
 *   • Жижиг `.md` лекц оруулна (материалын тоо харагдахгүй): явц, дараа нь
 *     жагсаалтад «Боловсруулж байна» → «Бэлэн»,
 *   • Судлах сет: хэсэг эвхэгдэнэ, сэдвийн цонх (Заавар / Картууд / Тест), баруун
 *     баганын гурван карт,
 *   • Заавар: AI шошго, гарчгийн бүтэц (`h1` ганцхан), «уншсан» тэмдэглэгдэнэ,
 *   • Картууд: Space-ээр эргүүлж 3-аар үнэлнэ, хулганаар эргүүлж «Эргэлзсэн»,
 *   • Сэдвийн тест: 1–4 товчоор хариулж, тайлбартай, дүнгийн дэлгэц хүртэл,
 *   • Бүтэн тест, «Шалгалтад бэлтгэх» (магадлалын шошго, хариултын санаа,
 *     төлөвлөгөөний тэмдэглэгээ дахин ачаалахад үлдэнэ),
 *   • Утасны өргөнд хэвтээ гүйлгээгүй; `/admin/live` тойм ба багц олгох,
 *   • Нэр солих, устгах; бүх хуудсанд консолын алдаагүй.
 *
 * Шаардлага: API `LIVE_ACCESS=admins` (эсвэл `all`) ба хуурамч AI —
 * `AI_MODELS=fake:local` (түлхүүргүй, текстээс тогтмол хэсэг, сэдэв, карт,
 * заавар, тест, таамаг гаргана), файл `LIVE_STORAGE_DIR`-д. Админаар ажиллана —
 * `admins` горимд ч нээлттэй. Үүсгэсэн материалыг төгсгөлд нь устгана.
 */

import { request } from "playwright";

import { API_URL, BASE_URL, SEED, check, goto, login, newSession, summary } from "./harness.mjs";

const stamp = Date.now().toString(36);
const TITLE = `E2E лекц ${stamp}`;
const RENAMED = `E2E лекц (засвар) ${stamp}`;

/** Хуурамч AI хэсэг, сэдэв гаргахад хангалттай бүтэцтэй богино лекц. */
const LECTURE = `# Python-ийн үндэс

## Хувьсагч ба төрөл

Хувьсагч гэдэг нь утгыг нэрээр хадгалах сав юм. \`nas = 17\` гэж бичвэл
\`nas\` нэртэй хувьсагчид 17 гэсэн бүхэл тоо хадгалагдана.

Python-д үндсэн төрлүүд: \`int\` (бүхэл тоо), \`float\` (бутархай тоо),
\`str\` (текст), \`bool\` (үнэн эсвэл худал).

## Нөхцөл шалгах

\`if\` нөхцөл үнэн бол доторх код ажиллана. \`elif\` нь өөр нөхцөл, \`else\`
нь аль нь ч биелээгүй үед ажиллана. Жишээ нь оноо 90-ээс их бол «A» үнэлгээ.

## Давталт

\`for\` давталт нь жагсаалтын элемент бүрээр явна. \`while\` давталт нь нөхцөл
үнэн байх хугацаанд давтана. \`break\` нь давталтыг зогсооно.

## Функц

Функцийг \`def\` түлхүүр үгээр тодорхойлно. \`return\` нь үр дүнг буцаана.
Функц нь кодыг дахин ашиглах боломж олгоно.
`;

const admin = await request.newContext();
await admin.post(`${API_URL}/auth/login`, { data: SEED.admin });

const sessions = [];

/** Материалын жагсаалтын карт (toast ч текст агуулдаг тул `article`-аар хязгаарлана). */
function materialCard(page, title) {
  return page.locator("article", { hasText: title });
}

/** Жагсаалтын картад төлөв гарахыг хүлээнэ (3 сек тутам шинэчлэгддэг). */
async function waitForStatus(page, title, statuses, timeout = 180_000) {
  const handle = await page.waitForFunction(
    ({ title: name, statuses: wanted }) => {
      const card = [...document.querySelectorAll("article")].find((item) =>
        item.textContent?.includes(name),
      );
      const text = card?.textContent ?? "";
      return wanted.find((status) => text.includes(status)) ?? false;
    },
    { title, statuses },
    { timeout, polling: 1_000 },
  );
  return handle.jsonValue();
}

try {
  const configResponse = await admin.get(`${API_URL}/live/config`);
  const config = configResponse.ok() ? await configResponse.json() : null;
  check(
    "Live админд нээлттэй (LIVE_ACCESS=admins эсвэл all)",
    config?.enabled === true,
    `${configResponse.status()} ${JSON.stringify(config)?.slice(0, 160)}`,
  );
  if (!config?.enabled) throw new Error("Live хаалттай — API-г LIVE_ACCESS=admins-тай асаана уу.");

  // --- /live ------------------------------------------------------------------------
  const session = await newSession({ width: 1280, height: 1000 });
  sessions.push(session);
  const { page, requests } = session;
  await login(page, SEED.admin);

  const liveLink = page.locator('header nav a[data-nav-href="/live"]');
  await liveLink.waitFor({ timeout: 15_000 });
  check("толгойд «Live» холбоос", (await liveLink.innerText()).trim() === "Live");
  await liveLink.click();
  await page.waitForURL("**/live", { timeout: 15_000 });
  await page.getByRole("heading", { name: "Шинэ материал оруулах" }).waitFor({ timeout: 20_000 });
  // AI хэрэглээ нь `meter` (0–100%) — материалын тоо харагдахгүй.
  const usageMeter = page.getByRole("meter", { name: /AI хэрэглээ/ });
  const usageValue = Number(
    await usageMeter.getAttribute("aria-valuenow", { timeout: 5_000 }).catch(() => null),
  );
  check(
    "гарчиг ба хэрэглээний хэмжүүр",
    (await page.locator("h1").innerText()).includes("MedlegHub Live") &&
      (await usageMeter.count()) === 1 &&
      usageValue >= 0 &&
      usageValue <= 100 &&
      (await page.getByText(/Материал \d+/).count()) === 0,
    `meter ${await usageMeter.count()}, value ${usageValue}`,
  );

  await page.getByLabel("Лекцийн файл").setInputFiles({
    name: "python-undes.md",
    mimeType: "text/markdown",
    buffer: Buffer.from(LECTURE, "utf8"),
  });
  check("сонгосон файл харагдана", (await page.getByText("python-undes.md").count()) === 1);
  await page.getByLabel("Нэр (заавал биш)").fill(TITLE);

  await page.getByRole("button", { name: "Оруулах" }).click();
  await page
    .locator("[data-sonner-toast]", { hasText: "Материал хүлээн авлаа" })
    .waitFor({ timeout: 30_000 });
  check(
    "файлын агуулга PUT-ээр илгээгдэв",
    requests.some((line) => /^PUT .*\/content$/.test(line)),
  );

  const first = await waitForStatus(
    page,
    TITLE,
    ["Дараалалд", "Боловсруулж байна", "Бэлэн", "Амжилтгүй"],
    20_000,
  );
  check("жагсаалтад шинэ материал гарав", Boolean(first), String(first));
  const final = await waitForStatus(page, TITLE, ["Бэлэн", "Амжилтгүй"]);
  check("материал «Бэлэн» болов", final === "Бэлэн", String(final));
  if (final !== "Бэлэн") {
    throw new Error(`Материал боловсрогдсонгүй: ${await materialCard(page, TITLE).innerText()}`);
  }
  check(
    "картад сэдвийн тоо, эзэмшил",
    /\d+ сэдэв/.test(await materialCard(page, TITLE).innerText()) &&
      (await materialCard(page, TITLE).getByRole("progressbar").count()) === 1,
  );

  // --- Судлах сет --------------------------------------------------------------------
  await materialCard(page, TITLE).getByRole("link", { name: TITLE }).click();
  await page.waitForURL(/\/live\/materials\/[0-9a-f-]{36}$/, { timeout: 15_000 });
  const materialId = page.url().split("/").pop();
  await page.locator("h1", { hasText: TITLE }).waitFor({ timeout: 20_000 });

  const sectionToggle = page.getByRole("button", { name: /^Хэсэг 1:/ });
  check(
    "«Хэсэг 1: …» эвхэх товч нээлттэй",
    (await sectionToggle.getAttribute("aria-expanded")) === "true",
  );
  await sectionToggle.click();
  check("хэсэг эвхэгдэнэ", (await sectionToggle.getAttribute("aria-expanded")) === "false");
  await sectionToggle.click();

  const aside = page.locator("aside");
  check(
    "баруун баганад бүтэн картууд, бүтэн тест, шалгалт",
    (await aside.getByRole("link", { name: /Бүтэн картууд/ }).count()) === 1 &&
      (await aside.getByRole("link", { name: /Бүтэн тест/ }).count()) === 1 &&
      (await aside.getByRole("link", { name: /Шалгалтад бэлтгэх/ }).count()) === 1,
  );
  check(
    "эзэмшлийн тайлбар",
    (await page.getByText("Заавар уншсан 10% · Картууд 40% · Тест 50%").count()) === 1,
  );

  const topicRow = page.locator('section button[aria-haspopup="menu"]').first();
  const topicName = (await topicRow.locator("span.block").first().innerText()).trim();
  await topicRow.click();
  const menu = page.getByRole("menu");
  await menu.waitFor({ timeout: 10_000 });
  check(
    "сэдвийн цонх: Заавар / Картууд / Тест",
    (await menu.getByRole("menuitem").allInnerTexts()).map((text) => text.trim()).join("|") ===
      "Заавар|Картууд|Тест",
  );
  await menu.getByRole("menuitem", { name: "Заавар" }).click();

  // --- Заавар --------------------------------------------------------------------------
  await page.waitForURL(/\/guide\/[0-9a-f-]{36}$/, { timeout: 15_000 });
  const topicId = page.url().split("/").pop();
  await page.locator("article").first().waitFor({ timeout: 120_000 });
  check(
    "заавар — гарчиг нь сэдвийн нэр",
    (await page.locator("h1").innerText()).trim() === topicName,
  );
  check("заавар — «AI бэлтгэсэн» шошго", (await page.getByText("AI бэлтгэсэн").count()) >= 1);
  check("заавар — хуудсанд ганц h1", (await page.locator("h1").count()) === 1);
  await page.waitForTimeout(1_500);
  check(
    "заавар уншсан гэж тэмдэглэгдэв",
    requests.some((line) => line === `POST /api/v1/live/topics/${topicId}/guide-read`),
  );

  // --- Картууд ------------------------------------------------------------------------
  await page.getByRole("link", { name: "Картаар давтах" }).click();
  await page.waitForURL(/\/cards\?topic=/, { timeout: 15_000 });
  const card = page.getByRole("button", { name: /Нэр томьёо/ });
  const reviewAll = page.getByRole("button", { name: "Бүгдийг давтах" });
  await Promise.race([card.waitFor({ timeout: 30_000 }), reviewAll.waitFor({ timeout: 30_000 })]);
  if (await reviewAll.isVisible()) await reviewAll.click();
  await card.waitFor({ timeout: 15_000 });
  const progressBefore = await page.getByText(/^1 \/ \d+$/).innerText();
  const deckSize = Number(progressBefore.split("/")[1]);
  check("картын явц «1 / N»", deckSize >= 1, progressBefore);

  await card.focus();
  await page.keyboard.press("Space");
  const flipped = page.getByRole("button", { name: /Тайлбар/ });
  await flipped.waitFor({ timeout: 5_000 });
  check(
    "Space — карт эргэнэ, ар тал дэлгэц уншигчид",
    (await page.getByRole("status").filter({ hasText: "Ар тал:" }).count()) === 1,
  );
  check(
    "үнэлгээний гурван товч",
    (await page
      .getByRole("group", { name: "Хэр сайн мэдэж байна вэ?" })
      .getByRole("button")
      .count()) === 3,
  );
  await page.keyboard.press("3");
  if (deckSize >= 2) {
    await page.getByText(/^2 \/ \d+$/).waitFor({ timeout: 10_000 });
    check("3 товч — «Мэднэ», дараагийн карт", true);
    await page.getByRole("button", { name: /Нэр томьёо/ }).click();
    await page.getByRole("button", { name: /Эргэлзсэн/ }).click();
    await page.waitForTimeout(800);
    check(
      "хулганаар эргүүлж «Эргэлзсэн»",
      deckSize === 2
        ? (await page.getByRole("heading", { name: "Давталт дууслаа!" }).count()) === 1
        : (await page.getByText(/^3 \/ \d+$/).count()) === 1,
    );
  } else {
    await page.getByRole("heading", { name: "Давталт дууслаа!" }).waitFor({ timeout: 10_000 });
  }
  check(
    "карт бүр серверт үнэлэгдэв",
    requests.filter((line) => /^POST .*\/live\/cards\/.*\/review$/.test(line)).length ===
      Math.min(2, deckSize),
  );

  // --- Сэдвийн тест --------------------------------------------------------------------
  await goto(page, `/live/materials/${materialId}/quiz?topic=${topicId}`);
  const start = page.getByRole("button", { name: "Эхлэх" });
  await start.waitFor({ timeout: 120_000 });
  check(
    "тест — «AI бэлтгэсэн», асуултын тоо",
    (await page.getByText("AI бэлтгэсэн").count()) >= 1 &&
      (await page.getByText(/^\d+ асуулт$/).count()) === 1,
  );
  await start.click();
  let answered = 0;
  for (let guard = 0; guard < 40; guard += 1) {
    const counter = page.getByText(/^Асуулт \d+ \/ \d+$/);
    await counter.waitFor({ timeout: 15_000 });
    await page.keyboard.press("1");
    const feedback = page.getByText(/^(Зөв!|Буруу\. Зөв хариулт: \d\.)$/);
    await feedback.waitFor({ timeout: 15_000 });
    answered += 1;
    const finish = page.getByRole("button", { name: "Дүн харах" });
    if (await finish.isVisible()) {
      await finish.click();
      break;
    }
    // «Дараагийн асуулт» фокустай — Enter.
    await page.keyboard.press("Enter");
  }
  await page.getByRole("heading", { name: "Тестийн дүн" }).waitFor({ timeout: 15_000 });
  check("тестийн дүн — хувь", (await page.getByText(/^\d+%$/).count()) >= 1);
  check(
    "асуулт бүрт хариулт илгээгдэв",
    requests.filter((line) => /^POST .*\/live\/attempts\/.*\/answers$/.test(line)).length ===
      answered,
    String(answered),
  );
  check(
    "сэдэв тус бүрийн эзэмшил",
    (await page.getByRole("heading", { name: "Сэдэв тус бүрээр" }).count()) === 1,
  );

  // --- Бүтэн тест --------------------------------------------------------------------
  await goto(page, `/live/materials/${materialId}/quiz`);
  await page.getByRole("button", { name: "Эхлэх" }).waitFor({ timeout: 120_000 });
  check("бүтэн тест нээгдэв", (await page.locator("h1").innerText()).trim() === "Бүтэн тест");

  // --- Шалгалтад бэлтгэх --------------------------------------------------------------------
  await goto(page, `/live/materials/${materialId}/exam`);
  await page.getByRole("heading", { name: "Шалгалтад бэлтгэх" }).waitFor({ timeout: 20_000 });
  await page.getByText("Энэ бол AI-ийн таамаг").waitFor({ timeout: 120_000 });
  check(
    "таамаг — магадлалын шошго бичвэртэй",
    (await page.getByText(/^(Өндөр|Дунд|Бага) магадлал$/).count()) >= 1,
  );
  const outline = page.getByRole("button", { name: "Хариултын санаа" }).first();
  if ((await outline.count()) > 0) {
    await outline.click();
    check("хариултын санаа нээгдэнэ", (await outline.getAttribute("aria-expanded")) === "true");
  }
  const planItem = page.locator("section[aria-labelledby=exam-plan] input[type=checkbox]").first();
  if ((await planItem.count()) > 0) {
    await planItem.check();
    await page.reload({ waitUntil: "domcontentloaded" });
    await page.getByText("Энэ бол AI-ийн таамаг").waitFor({ timeout: 30_000 });
    check(
      "төлөвлөгөөний тэмдэглэгээ хадгалагдана",
      await page
        .locator("section[aria-labelledby=exam-plan] input[type=checkbox]")
        .first()
        .isChecked(),
    );
  }

  // --- Буцаад судлах сет -------------------------------------------------------------------
  await goto(page, `/live/materials/${materialId}`);
  await page.locator("h1", { hasText: TITLE }).waitFor({ timeout: 20_000 });
  check("«Сүүлд судалсан» шошго", (await page.getByText("Сүүлд судалсан").count()) >= 1);
  const overall = await page
    .getByRole("progressbar", { name: "Нийт эзэмшил" })
    .getAttribute("aria-valuenow");
  check("нийт эзэмшил өссөн", Number(overall) > 0, String(overall));

  // --- Утасны өргөн --------------------------------------------------------------------
  const phone = await newSession({ width: 390, height: 844 });
  sessions.push(phone);
  await login(phone.page, SEED.admin);
  for (const path of [
    "/live",
    `/live/materials/${materialId}`,
    `/live/materials/${materialId}/guide/${topicId}`,
    `/live/materials/${materialId}/exam`,
  ]) {
    await goto(phone.page, path);
    await phone.page.locator("h1").waitFor({ timeout: 30_000 });
    await phone.page.waitForTimeout(1_000);
    const overflow = await phone.page.evaluate(
      () => document.documentElement.scrollWidth - window.innerWidth,
    );
    check(
      `утас: ${path.replace(materialId, ":id").replace(topicId, ":topic")} — хэвтээ гүйлгээгүй`,
      overflow <= 0,
      String(overflow),
    );
  }
  // Утсан дээр хэрэгслүүд товч агуулга ба хэсгүүдийн хооронд.
  await goto(phone.page, `/live/materials/${materialId}`);
  await phone.page.locator("aside").waitFor({ timeout: 20_000 });
  const order = await phone.page.evaluate(() => {
    const top = (selector) => document.querySelector(selector)?.getBoundingClientRect().top ?? -1;
    return [top("h1"), top("aside"), top("section button[aria-expanded]")];
  });
  check(
    "утас: гарчиг → хэрэгслүүд → хэсгүүд",
    order[0] < order[1] && order[1] < order[2],
    order.join(" < "),
  );

  // --- Админ ---------------------------------------------------------------------------
  const student = `e2e-live-${Date.now()}@suralts.mn`;
  const registrar = await request.newContext();
  await registrar.post(`${API_URL}/auth/register`, {
    data: {
      email: student,
      password: "Nuuts12345",
      name: "Live Суралцагч",
      is_16_or_older: true,
      accept_terms: true,
    },
  });
  await registrar.dispose();

  await goto(page, "/admin/live");
  await page.getByRole("heading", { name: "Энэ сарын тойм" }).waitFor({ timeout: 20_000 });
  check(
    "админ — хандалт, AI, төсвийн зураас",
    (await page.getByRole("progressbar", { name: "Сарын төсвийн хэрэглээ" }).count()) === 1,
  );
  await page.fill("#live-grant-email", student);
  await page.getByRole("button", { name: "Хайх" }).click();
  await page.getByText("Live Суралцагч").waitFor({ timeout: 10_000 });
  check(
    "шинэ хэрэглэгч — Standard багцгүй",
    (await page.getByText("Standard багцгүй").count()) === 1,
  );
  await page.fill("#live-grant-months", "2");
  await page.getByRole("button", { name: "Premium · 2 сар олгох" }).click();
  await page
    .locator("[data-sonner-toast]", { hasText: "Premium олгогдлоо." })
    .waitFor({ timeout: 10_000 });
  check("Premium олгогдов", (await page.getByText(/^Premium · .* хүртэл$/).count()) === 1);
  check(
    "AI загварууд харагдана",
    (await page.getByRole("heading", { name: "AI загварууд" }).count()) === 1,
  );

  // --- Нэр солих, устгах -------------------------------------------------------------------
  await goto(page, "/live");
  await materialCard(page, TITLE).waitFor({ timeout: 20_000 });
  await materialCard(page, TITLE)
    .getByRole("button", { name: `«${TITLE}» — үйлдэл` })
    .click();
  await page.getByRole("menuitem", { name: "Нэр солих" }).click();
  const renameDialog = page.getByRole("dialog");
  await renameDialog.getByLabel("Нэр").fill(RENAMED);
  await renameDialog.getByRole("button", { name: "Хадгалах" }).click();
  await materialCard(page, RENAMED).waitFor({ timeout: 10_000 });
  check("нэр солигдов", (await materialCard(page, RENAMED).count()) === 1);

  await materialCard(page, RENAMED)
    .getByRole("button", { name: `«${RENAMED}» — үйлдэл` })
    .click();
  await page.getByRole("menuitem", { name: "Устгах" }).click();
  await page.getByRole("dialog").getByRole("button", { name: "Устгах" }).click();
  await page
    .locator("[data-sonner-toast]", { hasText: "Материал устгагдлаа." })
    .waitFor({ timeout: 10_000 });
  check("материал устгагдав", (await materialCard(page, RENAMED).count()) === 0);

  for (const current of sessions) {
    const unexpected = current.problems.filter((problem) => !problem.includes("401"));
    check("консолд алдаагүй", unexpected.length === 0, unexpected.join(" | "));
  }
} catch (error) {
  check("тест бүрэн ажиллав", false, String(error));
} finally {
  // Алдаагаар зогссон ч энэ тестийн материал үлдэхгүй.
  const list = await admin.get(`${API_URL}/live/materials`);
  if (list.ok()) {
    for (const item of await list.json()) {
      if (item.title.includes(stamp)) await admin.delete(`${API_URL}/live/materials/${item.id}`);
    }
  }
  await admin.dispose();
  for (const current of sessions) await current.close();
}

console.log(`  (${BASE_URL})`);
process.exit(summary("live-study") > 0 ? 1 : 0);
