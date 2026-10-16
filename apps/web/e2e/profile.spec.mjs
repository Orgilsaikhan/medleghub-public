/**
 * Профайл ба тэмдгүүд.
 *
 *   • Хэрэглэгчийн цэснээс «Профайл» руу орно,
 *   • Профайл нь нэр, статистик, 26 тэмдгийг харуулна; боломжтой тэмдэг бүрт хэдэн хувь нь
 *     авсан («Нийт хэрэглэгчдийн X% нь авсан»), «Тун удахгүй» тэмдэгт хувь байхгүй,
 *   • Шинэ хэрэглэгч «Ahead of Time»-тай, «First Commit»-гүй, онцлох амжилтгүй —
 *     «Онцлох амжилт сонгох» товчтой,
 *   • Нууц амжилт авах хүртэл «?» дүрстэй,
 *   • Онцлох амжилт сонгох цонх: авсан амжилтууд, байрны дугаар, 5-ын хязгаар, «Хадгалах»,
 *     «Болих»; хадгалсан дарааллаараа нэрийн хажууд харагдана,
 *   • Нэрийн хажуугийн дүрс: хулгана аваачих эсвэл Tab-аар очиход нэр, хувь нь tooltip-оор;
 *     дарахад хаягийг (#hash) өөрчлөхгүйгээр карт руу гүйлгэж фокуслана — «Буцах» эвдрэхгүй,
 *   • Хичээл дуусгахад «New achievement» мэдэгдэл гарч, профайл дээр тэмдэг авсан болно,
 *   • Өөр суралцагч нийтийн профайл (`/users/{id}`) дээр ижил онцлох амжилтуудыг засах
 *     товчгүй харна,
 *   • API аваагүй амжилтыг онцлуулахгүй.
 */

import {
  API_URL,
  SEED,
  check,
  goto,
  grantPlan,
  login,
  newSession,
  registerNew,
  submitReferenceSolution,
  summary,
} from "./harness.mjs";

const session = await newSession({ width: 1440, height: 1000 });
const { page, problems, requests } = session;
// API-г `page.context().request`-ээр — хуудсан доторх fetch нь dev CSP-д баригдана.
const api = page.context().request;

const GRID = 'section[aria-labelledby="badges-title"] li';
/** «Нийт хэрэглэгчдийн 45% нь авсан» — `formatPercent`: 45%, 2.5%, <0.1%, 0%. */
const RARITY = /Нийт хэрэглэгчдийн (<0\.1|\d+(\.\d)?)% нь авсан/;
/** Авсан картын огноо «…-нд авсан». Хувийн мөр ч «авсан» гэж төгсдөг тул ингэж ялгана. */
const EARNED_ON = /-нд авсан/;

/** Achievements жагсаалтын картууд, дарааллаар. Картын `id` нь `badge-<түлхүүр>`. */
const gridCards = (target = page) =>
  target.locator(GRID).evaluateAll((cards) =>
    cards.map((li) => ({
      key: li.id.replace(/^badge-/, ""),
      // Гарчгийн эхний текст нь нэр — ховор бол ард нь sr-only « — ховор амжилт».
      name: li.querySelector("h3")?.firstChild?.textContent?.trim() ?? "",
      earned: li.hasAttribute("data-earned"),
      text: li.innerText,
    })),
  );

/** Нэрийн хажуугийн онцлох амжилтууд (`BadgeShowcase`). */
const showcase = (target = page) =>
  target.getByRole("list", { name: "Онцлох амжилтууд", exact: true });

/** Онцлох амжилтуудын түлхүүр, дарааллаар — холбоос бүрийн `#badge-<түлхүүр>`-ээс. */
const showcaseKeys = (target = page) =>
  showcase(target)
    .getByRole("link")
    .evaluateAll((links) =>
      links.map((link) => link.getAttribute("href")?.replace(/^#badge-/, "")),
    );

/** Онцлох жагсаалт DOM-д байгаа эсэх — нээлттэй цонхны `aria-hidden`-ээс үл хамаарна. */
const showcaseRendered = async (target = page) =>
  (await target.locator('ul[aria-label="Онцлох амжилтууд"]').count()) > 0;

const chooseButton = (target = page) =>
  target.getByRole("button", { name: "Онцлох амжилт сонгох", exact: true });
const editButton = (target = page) =>
  target.getByRole("button", { name: "Онцлох амжилтаа засах", exact: true });

/** Онцлох амжилт сонгох цонх. */
const dialog = page.getByRole("dialog", { name: "Онцлох амжилтууд" });

/**
 * Цонхны сонголтын товчнууд, дарааллаар: нэр, дарагдсан эсэх, идэвхгүй эсэх, харагдах
 * дугаар ба дэлгэц уншигчид зориулсан «N-р байр».
 */
const pickerState = () =>
  dialog.locator("button[aria-pressed]").evaluateAll((buttons) =>
    buttons.map((button) => {
      // Эхний текст нь нэр — дүрс нь текстгүй (`alt=""`).
      const walker = document.createTreeWalker(button, NodeFilter.SHOW_TEXT);
      let name = "";
      while (!name && walker.nextNode()) name = walker.currentNode.textContent.trim();
      const text = button.textContent ?? "";
      return {
        name,
        pressed: button.getAttribute("aria-pressed") === "true",
        disabled: button.disabled,
        number: button.querySelector(":scope > [aria-hidden]")?.textContent ?? "",
        position: Number(text.match(/(\d+)-р байр/)?.[1]) || null,
        rarity: /Нийт хэрэглэгчдийн \S+ нь авсан/.test(text),
      };
    }),
  );

/** Цонхны тоолуур: «N / 5 сонгосон», дүүрвэл « · Хамгийн ихдээ 5 амжилт сонгоно.». */
const pickerCount = async () => (await dialog.locator("p[aria-live]").innerText()).trim();

/** Цонхонд амжилтыг нэрээр нь дарна (сонгох / болих). */
async function toggle(name) {
  await dialog.locator("button[aria-pressed]", { hasText: name }).click();
  await page.waitForTimeout(100);
}

const row = (state, name) => state.find((item) => item.name === name);

const showcasePuts = () =>
  requests.filter((item) => item.startsWith("PUT ") && item.endsWith("/me/showcase")).length;

/**
 * «Хадгалах» дарна. `PUT /me/showcase`-ээр илгээсэн түлхүүрүүд, мэдэгдэл гарсан эсэх, цонх
 * хаагдсан эсэхийг буцаана.
 */
async function saveShowcase() {
  const sent = page
    .waitForRequest((req) => req.method() === "PUT" && req.url().includes("/me/showcase"), {
      timeout: 15_000,
    })
    .catch(() => null);
  await dialog.getByRole("button", { name: "Хадгалах", exact: true }).click();
  const request = await sent;
  const toast = await page
    .locator("[data-sonner-toast]", { hasText: "Онцлох амжилтууд хадгалагдлаа." })
    .waitFor({ timeout: 15_000 })
    .then(
      () => true,
      () => false,
    );
  const closed = await dialog.waitFor({ state: "hidden", timeout: 10_000 }).then(
    () => true,
    () => false,
  );
  await page.waitForTimeout(300);
  return { keys: request?.postDataJSON()?.badge_keys ?? null, toast, closed };
}

/** Сервер дээр хадгалагдсан онцлох амжилтууд, байрных нь дарааллаар (`/me/profile`). */
async function savedShowcase() {
  const profile = await (await api.get(`${API_URL}/me/profile`)).json();
  return profile.badges
    .filter((badge) => badge.showcase_position != null)
    .sort((a, b) => a.showcase_position - b.showcase_position)
    .map((badge) => badge.key);
}

/**
 * Тухайн тексттэй tooltip (Radix) гартал хүлээнэ: харагдах агуулга
 * (`data-slot="tooltip-content"`) ба дэлгэц уншигчийн `role="tooltip"`. Одоогийн Radix
 * агуулга өөрөө `role="tooltip"`; хуучин хувилбар дотроо нуугдмал хуулбар гаргадаг байсан.
 * Гарахгүй бол `null`.
 */
async function openTooltip(target, text) {
  const content = target.locator('[data-slot="tooltip-content"]', { hasText: text }).first();
  try {
    await content.waitFor({ state: "visible", timeout: 5_000 });
  } catch {
    return null;
  }
  return content.evaluate((el) => ({
    text: el.innerText.replace(/\s+/g, " "),
    role: el.matches('[role="tooltip"]') || Boolean(el.querySelector('[role="tooltip"]')),
  }));
}

/** Тухайн тексттэй tooltip хаагдаж, DOM-оос гартал хүлээнэ. Хаагдахгүй бол `false`. */
async function tooltipClosed(target, text) {
  try {
    await target
      .locator('[data-slot="tooltip-content"]', { hasText: text })
      .first()
      .waitFor({ state: "detached", timeout: 5_000 });
    return true;
  } catch {
    return false;
  }
}

/** Одоо байгаа tooltip-уудын текст — унасан шалгалтын тайлбарт. */
const tooltipTexts = async (target = page) =>
  (await target.locator('[data-slot="tooltip-content"]').allInnerTexts())
    .map((text) => text.replace(/\s+/g, " "))
    .join(" | ") || "tooltip алга";

/** Жигд гүйлгэлт (`behavior: "smooth"`) дуусч, байрлал тогтвортой болтол хүлээнэ. */
async function scrollSettled(target) {
  let last = -1;
  let stable = 0;
  for (let i = 0; i < 50 && stable < 3; i += 1) {
    await target.waitForTimeout(100);
    const y = await target.evaluate(() => window.scrollY);
    stable = y === last ? stable + 1 : 0;
    last = y;
  }
  return last;
}

/** Картын байрлал, фокус, хаяг, түүх — дүрс дээр дарахаас өмнө ба дараа. */
const cardView = (target, key) =>
  target.locator(`#badge-${key}`).evaluate((el) => {
    const rect = el.getBoundingClientRect();
    const header = document.querySelector("header")?.getBoundingClientRect().bottom ?? 0;
    return {
      focused: document.activeElement === el,
      hash: window.location.hash,
      url: window.location.href,
      history: window.history.length,
      ring: getComputedStyle(el).boxShadow,
      top: Math.round(rect.top),
      bottom: Math.round(rect.bottom),
      header: Math.round(Math.max(header, 0)),
      height: window.innerHeight,
    };
  });

const inView = (view) => view.top >= view.header && view.bottom <= view.height;
const where = (view) =>
  `карт ${view.top}–${view.bottom}px, толгой ${view.header}px, цонх ${view.height}px`;

const waitForBadges = (target = page) =>
  target.getByRole("heading", { name: "Achievements", exact: true }).waitFor({ timeout: 20_000 });

try {
  const { email } = await registerNew(page, "Тэмдэг Цуглуулагч");

  // --- Цэснээс профайл руу -------------------------------------------------------
  await goto(page, "/dashboard");
  await page.getByRole("button", { name: "Цэс" }).click();
  await page.getByRole("menuitem", { name: "Профайл" }).click();
  await page.waitForURL(/\/profile$/, { timeout: 15_000 });
  await waitForBadges();

  check(
    "хэрэглэгчийн нэр харагдана",
    (await page.locator("h1").innerText()) === "Тэмдэг Цуглуулагч",
  );
  // «Where the Answers Hide» (2026-09-29)-ээс хойш харагдах тэмдэг 26.
  const cards = await gridCards();
  check("26 тэмдэг харагдана", cards.length === 26, String(cards.length));
  const byKey = (key) => cards.find((item) => item.key === key);
  check(
    "шинэ хэрэглэгч «Ahead of Time»-тай",
    byKey("ahead-of-time")?.earned && EARNED_ON.test(byKey("ahead-of-time").text),
    byKey("ahead-of-time")?.text.replace(/\s+/g, " "),
  );
  check(
    "«First Commit» хараахан аваагүй",
    byKey("first-commit") &&
      !byKey("first-commit").earned &&
      byKey("first-commit").text.includes("Аваагүй"),
  );
  check(
    "нууц амжилт жинхэнэ дүрсийн оронд «?» харуулна",
    (await page.locator("#badge-hidden-gem [data-secret]").count()) === 1 &&
      (await page.locator("#badge-hidden-gem img").count()) === 0,
  );
  check("өгөгдөлгүй тэмдэг «Тун удахгүй»", byKey("mentor")?.text.includes("Тун удахгүй"));

  // --- Ховор байдал: хэдэн хувь нь авсан -----------------------------------------
  const soon = cards.filter((item) => item.text.includes("Тун удахгүй"));
  const available = cards.filter((item) => !item.text.includes("Тун удахгүй"));
  const withoutRarity = available.filter((item) => !RARITY.test(item.text));
  check(
    "боломжтой тэмдэг бүр «Нийт хэрэглэгчдийн X% нь авсан» харуулна",
    available.length > 0 && withoutRarity.length === 0,
    withoutRarity.length
      ? `хувьгүй: ${withoutRarity.map((item) => item.key).join(", ")}`
      : `${available.length} карт`,
  );
  const soonWithRarity = soon.filter((item) => item.text.includes("Нийт хэрэглэгчдийн"));
  check(
    "«Тун удахгүй» тэмдэгт хувь харагдахгүй",
    soon.length > 0 && soonWithRarity.length === 0,
    soonWithRarity.length
      ? `хувьтай: ${soonWithRarity.map((item) => item.key).join(", ")}`
      : `${soon.length} карт`,
  );

  // --- Онцлох амжилт: шинэ хэрэглэгч ---------------------------------------------
  check(
    "шинэ хэрэглэгчид онцлох амжилт алга, «Онцлох амжилт сонгох» товч харагдана",
    !(await showcaseRendered()) &&
      (await chooseButton().isVisible()) &&
      (await editButton().count()) === 0,
  );

  // --- Сонгох цонх: эхний амжилт -------------------------------------------------
  const earnedNames = cards.filter((item) => item.earned).map((item) => item.name);
  await chooseButton().click();
  await dialog.waitFor({ timeout: 10_000 });
  const initial = await pickerState();
  const initialCount = await pickerCount();
  check(
    "цонхонд авсан амжилт бүр сонгоогүй (aria-pressed=false), хувьтайгаа; «0 / 5 сонгосон»",
    initial.length > 0 &&
      initial.map((item) => item.name).join() === earnedNames.join() &&
      initial.every((item) => !item.pressed && item.rarity) &&
      initialCount === "0 / 5 сонгосон",
    `цонхонд: ${initial.map((item) => item.name).join(", ")}; авсан: ${earnedNames.join(", ")}; ${initialCount}`,
  );

  await toggle("Ahead of Time");
  const picked = row(await pickerState(), "Ahead of Time");
  const pickedCount = await pickerCount();
  check(
    "«Ahead of Time»-ыг сонгоход 1-р байр, «1 / 5 сонгосон»",
    picked?.pressed &&
      picked.number === "1" &&
      picked.position === 1 &&
      pickedCount === "1 / 5 сонгосон",
    `${JSON.stringify(picked)}; ${pickedCount}`,
  );

  const firstSave = await saveShowcase();
  check(
    "«Хадгалах» → PUT /me/showcase [ahead-of-time], «Онцлох амжилтууд хадгалагдлаа.»",
    firstSave.keys?.join() === "ahead-of-time" && firstSave.toast && firstSave.closed,
    JSON.stringify(firstSave),
  );
  const shownFirst = await showcaseKeys();
  check(
    "нэрийн хажууд «Ahead of Time — ховор амжилт» дүрс (#badge-ahead-of-time)",
    shownFirst.join() === "ahead-of-time" &&
      (await showcase()
        .getByRole("link", { name: "Ahead of Time — ховор амжилт", exact: true })
        .count()) === 1,
    shownFirst.join(", ") || "жагсаалт алга",
  );
  check(
    "товч «Онцлох амжилтаа засах» (харандаа) болно",
    (await editButton().isVisible()) && (await chooseButton().count()) === 0,
  );
  // Цонх хаагдахад фокус түүнийг нээсэн товч руу буцна — энд солигдсон шинэ харандаа руу.
  // `<body>` руу унавал гарын хэрэглэгч дараагийн Tab-аар хуудасны эхнээс эхэлнэ.
  const focusAfterSave = await page.evaluate(
    () => document.activeElement?.getAttribute("aria-label") ?? document.activeElement?.tagName,
  );
  check(
    "хадгалсны дараа фокус «Онцлох амжилтаа засах» товч руу буцна",
    focusAfterSave === "Онцлох амжилтаа засах",
    String(focusAfterSave),
  );

  const listed = (await showcase().count()) === 1;
  const nameBox = await page.locator("h1").boundingBox();
  const listBox = listed ? await showcase().boundingBox() : null;
  const iconBox = listed ? await showcase().getByRole("link").first().boundingBox() : null;
  check(
    "дүрс нэрийн хажууд, нэг мөрөнд, 28px",
    listBox &&
      iconBox &&
      listBox.x >= nameBox.x + nameBox.width &&
      listBox.y < nameBox.y + nameBox.height &&
      listBox.y + listBox.height > nameBox.y &&
      Math.round(iconBox.width) === 28 &&
      Math.round(iconBox.height) === 28,
    iconBox ? `${iconBox.width}×${iconBox.height}px` : "дүрс алга",
  );

  // --- Tooltip: хулгана ба гар ---------------------------------------------------
  const aheadLink = showcase().getByRole("link", { name: /^Ahead of Time/ });
  // Хулгана аваачихад (150 мс хоцролттой) нэр, хувь нь гарна.
  await aheadLink.hover();
  const hovered = await openTooltip(page, "Ahead of Time");
  check(
    "хулгана аваачихад tooltip-д нэр, хувь нь гарна (role=tooltip)",
    hovered?.role && RARITY.test(hovered.text),
    hovered?.text ?? (await tooltipTexts()),
  );
  await page.mouse.move(8, 600, { steps: 4 });
  check(
    "хулганаа холдуулахад tooltip хаагдана",
    await tooltipClosed(page, "Ahead of Time"),
    await tooltipTexts(),
  );

  // Засах товч өөрийн tooltip-тэй. Түүнээс Shift+Tab — дүрс рүү жинхэнэ гарын шилжилт.
  // Хадгалсны дараа фокус аль хэдийн товч дээр байгаа тул эхлээд авч хаяна — эс бөгөөс
  // `focus()` шинэ focus үйл явдал үүсгэхгүй.
  await page.evaluate(() => {
    if (document.activeElement instanceof HTMLElement) document.activeElement.blur();
  });
  await editButton().focus();
  const editTip = await openTooltip(page, "Онцлох амжилтаа засах");
  check(
    "засах товч фокус авахад tooltip «Онцлох амжилтаа засах»",
    Boolean(editTip),
    await tooltipTexts(),
  );
  await page.keyboard.press("Shift+Tab");
  const focusedHref = await page.evaluate(() => document.activeElement?.getAttribute("href"));
  const focusedTip = await openTooltip(page, "Ahead of Time");
  // Холбоосын тайлбар (`aria-describedby`) — дэлгэц уншигчийн сонсох текст, `aria-hidden`-гүй.
  // Нэр нь холбоосын нэрэнд байгаа тул tooltip-оос хувийг нь л сонсоно.
  const described = await aheadLink.evaluate((link) => {
    const target = document.getElementById(link.getAttribute("aria-describedby") ?? "");
    if (!target) return null;
    const walker = document.createTreeWalker(target, NodeFilter.SHOW_TEXT);
    let text = "";
    while (walker.nextNode()) {
      if (!walker.currentNode.parentElement?.closest('[aria-hidden="true"]')) {
        text += walker.currentNode.textContent;
      }
    }
    return { role: target.getAttribute("role"), text: text.trim() };
  });
  check(
    "Shift+Tab-аар дүрс рүү очиход tooltip-д нэр, хувь; холбоосыг tooltip тайлбарлана",
    focusedHref === "#badge-ahead-of-time" &&
      focusedTip?.role &&
      RARITY.test(focusedTip.text) &&
      described?.role === "tooltip" &&
      RARITY.test(described.text),
    `фокус: ${focusedHref}; tooltip: ${await tooltipTexts()}; aria-describedby: ${described?.text ?? "алга"}`,
  );
  await page.keyboard.press("Escape");
  check(
    "Escape дарахад tooltip хаагдаж, фокус дүрс дээр үлдэнэ",
    (await tooltipClosed(page, "Ahead of Time")) &&
      (await page.evaluate(() => document.activeElement?.getAttribute("href"))) ===
        "#badge-ahead-of-time",
    await tooltipTexts(),
  );

  // --- Дүрс дарахад карт руу — хаяг, түүх өөрчлөгдөхгүй ---------------------------
  // Энгийн `#hash` холбоос түүхэнд Next.js-ийн мэдэхгүй бичлэг нэмдэг байсан: дараа нь
  // «Тохиргоо» руу ороод «Буцах» дарахад Тохиргоо хуудас дэлгэцэнд үлддэг байв.
  const beforeClick = await cardView(page, "ahead-of-time");
  await aheadLink.click();
  const scrolledTo = await scrollSettled(page);
  const afterClick = await cardView(page, "ahead-of-time");
  check(
    "дүрс дээр дарахад доорх карт фокус авч тодорно (#badge-ahead-of-time)",
    afterClick.focused && afterClick.ring !== beforeClick.ring,
    `фокус: ${await page.evaluate(() => document.activeElement?.id || document.activeElement?.tagName)}`,
  );
  check(
    "карт руу гүйлгэж, толгойн доор бүтэн харагдана",
    scrolledTo > 0 && inView(afterClick),
    where(afterClick),
  );
  check(
    "хаяг солигдохгүй (#hash-гүй), түүхэнд шинэ бичлэг нэмэгдэхгүй",
    afterClick.hash === "" &&
      afterClick.url === beforeClick.url &&
      afterClick.history === beforeClick.history,
    `${afterClick.url}; түүх ${beforeClick.history} → ${afterClick.history}`,
  );

  await page.getByRole("main").getByRole("link", { name: "Тохиргоо", exact: true }).click();
  await page.waitForURL(/\/settings$/, { timeout: 15_000 });
  await page.getByRole("heading", { level: 1, name: "Тохиргоо" }).waitFor({ timeout: 15_000 });
  await page.goBack().catch(() => null);
  const backOnProfile = await waitForBadges().then(
    () => true,
    () => false,
  );
  check(
    "«Тохиргоо» → «Буцах» дарахад профайл дахин харагдана",
    backOnProfile &&
      /\/profile$/.test(page.url()) &&
      (await page.getByRole("heading", { level: 1, name: "Тохиргоо" }).count()) === 0,
    page.url(),
  );

  // --- Хичээл дуусгахад мэдэгдэл ------------------------------------------------
  const course = await (await api.get(`${API_URL}/courses/${SEED.course.slug}`)).json();
  await api.post(`${API_URL}/courses/${course.id}/enroll`);
  const firstLesson = course.modules[0].lessons[0].slug;

  await goto(page, `/learn/${SEED.course.slug}/${firstLesson}`, { waitFor: ".monaco-editor" });
  await page.waitForTimeout(1200);
  // Эхний хичээл даалгавартай — бүх тестийг давж «Илгээх»-ээр дуусна.
  await submitReferenceSolution(page, SEED.course.slug, firstLesson);
  await page
    .locator("[data-sonner-toast]", { hasText: "New achievement: First Commit" })
    .waitFor({ timeout: 15_000 });
  check("«New achievement: First Commit» мэдэгдэл гарна", true);

  await goto(page, "/profile");
  await waitForBadges();
  const firstCommit = (await gridCards()).find((item) => item.key === "first-commit");
  check(
    "профайл дээр «First Commit» авсан болно",
    firstCommit?.earned && EARNED_ON.test(firstCommit.text),
    firstCommit?.text.replace(/\s+/g, " "),
  );

  // --- Сонголтоо засах: дараалал ---------------------------------------------------
  await editButton().click();
  await dialog.waitFor({ timeout: 10_000 });
  const reopened = await pickerState();
  const kept = row(reopened, "Ahead of Time");
  const fresh = row(reopened, "First Commit");
  check(
    "дахин нээхэд «Ahead of Time» 1-р байранд сонгогдсон, «First Commit» сонгоогүй",
    kept?.pressed &&
      kept.position === 1 &&
      kept.number === "1" &&
      fresh &&
      !fresh.pressed &&
      fresh.position === null,
    JSON.stringify({ kept, fresh }),
  );
  await toggle("First Commit");
  const added = row(await pickerState(), "First Commit");
  const addedCount = await pickerCount();
  check(
    "«First Commit»-ыг нэмэхэд 2-р байр, «2 / 5 сонгосон»",
    added?.pressed &&
      added.position === 2 &&
      added.number === "2" &&
      addedCount === "2 / 5 сонгосон",
    `${JSON.stringify(added)}; ${addedCount}`,
  );
  const secondSave = await saveShowcase();
  check(
    "«Хадгалах» → PUT /me/showcase [ahead-of-time, first-commit], мэдэгдэл гарна",
    secondSave.keys?.join() === "ahead-of-time,first-commit" &&
      secondSave.toast &&
      secondSave.closed,
    JSON.stringify(secondSave),
  );
  const shownSecond = await showcaseKeys();
  check(
    "нэрийн хажууд сонгосон дарааллаар: Ahead of Time, First Commit",
    shownSecond.join() === "ahead-of-time,first-commit" &&
      (await showcase().getByRole("link", { name: "First Commit", exact: true }).count()) === 1,
    shownSecond.join(", "),
  );

  // --- Багц ба үлдсэн хоног -------------------------------------------------------
  const plan = page.locator("section[aria-labelledby='plan-title']");
  check("шинэ хэрэглэгчид үнэгүй багц харагдана", (await plan.innerText()).includes("Үнэгүй багц"));

  await grantPlan(email, 1);
  await goto(page, "/profile", { waitFor: "#plan-title" });
  const planText = await plan.innerText();
  const days = Number(planText.match(/(\d+)\s*хоног үлдсэн/)?.[1] ?? 0);
  check(
    "1 сарын багцад 28–31 хоног үлдсэн харагдана",
    days >= 28 && days <= 31,
    planText.replace(/\s+/g, " "),
  );

  // --- 5-ын хязгаар ба «Болих» -----------------------------------------------------
  // 6-аас олон амжилтыг API-ер: JavaScript-ийн эхний 4 модуль (12 үнэгүй хичээл) →
  // «Hello, World!», «Unstoppable», «Code Smith»; нууц хуудасны «Through Another's Path».
  const failed = [];
  for (const lesson of course.modules.slice(0, 4).flatMap((module) => module.lessons)) {
    const done = await api.post(`${API_URL}/lessons/${lesson.id}/complete`);
    if (!done.ok()) failed.push(`${lesson.slug}: ${done.status()}`);
  }
  const claimed = await api.post(`${API_URL}/me/badges/through-anothers-path`);
  await goto(page, "/profile");
  await waitForBadges();
  const many = await gridCards();
  const manyEarned = many.filter((item) => item.earned);
  const enough = failed.length === 0 && claimed.ok() && manyEarned.length >= 6;
  check(
    "API-ер 6-аас олон амжилт авна",
    enough,
    failed.join(" | ") || manyEarned.map((item) => item.key).join(", "),
  );
  check(
    "нууц «Through Another's Path» авсны дараа жагсаалтад нэмэгдэнэ (27)",
    many.length === 27 && many.some((item) => item.key === "through-anothers-path" && item.earned),
    String(many.length),
  );

  await editButton().click();
  await dialog.waitFor({ timeout: 10_000 });
  const everything = await pickerState();
  check(
    "цонхонд бүх авсан амжилт, Achievements-ийн дарааллаар",
    everything.map((item) => item.name).join() === manyEarned.map((item) => item.name).join(),
    `цонхонд: ${everything.map((item) => item.name).join(", ")}`,
  );
  // Сонгоогүйгээс эхний гурвыг нэмж 5 хүргэнэ.
  const extra = enough
    ? everything
        .filter((item) => !item.pressed)
        .slice(0, 3)
        .map((item) => item.name)
    : [];
  for (const name of extra) await toggle(name);
  const full = await pickerState();
  const fullCount = await pickerCount();
  check(
    "5 сонгоход «5 / 5 сонгосон · Хамгийн ихдээ 5 амжилт сонгоно.»",
    fullCount === "5 / 5 сонгосон · Хамгийн ихдээ 5 амжилт сонгоно.",
    fullCount,
  );
  const rest = full.filter((item) => !item.pressed);
  check(
    "5 хүрэхэд сонгоогүй товч идэвхгүй, байр нь сонгосон дарааллаар 1–5",
    rest.length > 0 &&
      rest.every((item) => item.disabled) &&
      full.filter((item) => item.pressed).every((item) => !item.disabled) &&
      ["Ahead of Time", "First Commit", ...extra].every(
        (name, index) => row(full, name)?.position === index + 1,
      ),
    full
      .map((item) => `${item.name}:${item.position ?? "-"}${item.disabled ? " (идэвхгүй)" : ""}`)
      .join(", "),
  );
  if (extra.length > 0) await toggle(extra.at(-1));
  const eased = await pickerState();
  const easedCount = await pickerCount();
  check(
    "нэгийг болиход «4 / 5 сонгосон», сонгоогүй товч дахин идэвхжинэ",
    easedCount === "4 / 5 сонгосон" &&
      eased.filter((item) => !item.pressed).every((item) => !item.disabled),
    easedCount,
  );
  const putsBefore = showcasePuts();
  await dialog.getByRole("button", { name: "Болих", exact: true }).click();
  await dialog.waitFor({ state: "hidden", timeout: 10_000 });
  await page.waitForTimeout(300);
  const afterCancel = await showcaseKeys();
  check(
    "«Болих» дарахад юу ч хадгалахгүй — нэрийн хажууд хэвээр",
    showcasePuts() === putsBefore && afterCancel.join() === "ahead-of-time,first-commit",
    afterCancel.join(", "),
  );

  // --- Нийтийн профайл — өөр суралцагчийн нүдээр ----------------------------------
  // `/users/{id}/profile`-ийг нэвтэрсэн хэн ч үзнэ (профайлаа нуугаагүй бол). Өөрийн
  // id-г нээвэл `/profile` руу шилжүүлдэг тул seed сурагчаар тусдаа сессэд нэвтэрнэ.
  const me = await (await api.get(`${API_URL}/auth/me`)).json();
  const viewer = await newSession({ width: 1440, height: 1000 });
  try {
    await login(viewer.page, SEED.student);
    await goto(viewer.page, `/users/${me.id}`);
    await waitForBadges(viewer.page);
    const publicName = await viewer.page.locator("h1").innerText();
    const publicKeys = await showcaseKeys(viewer.page);
    check(
      "нийтийн профайл дээр нэрийн хажууд ижил онцлох амжилтууд, ижил дарааллаар",
      publicName === "Тэмдэг Цуглуулагч" && publicKeys.join() === "ahead-of-time,first-commit",
      `${publicName}: ${publicKeys.join(", ")}`,
    );
    check(
      "нийтийн профайл дээр сонгох, засах товч байхгүй",
      (await chooseButton(viewer.page).count()) === 0 &&
        (await editButton(viewer.page).count()) === 0,
    );

    const publicLink = showcase(viewer.page).getByRole("link", {
      name: "First Commit",
      exact: true,
    });
    const publicFound = (await publicLink.count()) === 1;
    if (publicFound) await publicLink.hover();
    const publicTip = publicFound ? await openTooltip(viewer.page, "First Commit") : null;
    check(
      "нийтийн профайл дээр ч tooltip-д нэр, хувь нь гарна",
      publicTip?.role && RARITY.test(publicTip.text),
      publicTip?.text ?? (await tooltipTexts(viewer.page)),
    );

    let publicView = null;
    let publicHistory = null;
    if (publicFound) {
      publicHistory = (await cardView(viewer.page, "first-commit")).history;
      await publicLink.click();
      await scrollSettled(viewer.page);
      publicView = await cardView(viewer.page, "first-commit");
    }
    check(
      "нийтийн профайл дээр дүрс дарахад карт фокус авч харагдана, хаяг солигдохгүй",
      publicView?.focused &&
        inView(publicView) &&
        publicView.hash === "" &&
        publicView.history === publicHistory,
      publicView ? `${where(publicView)}; ${publicView.url}` : "дүрс алга",
    );
    check(
      "нийтийн профайл — console цэвэр",
      viewer.problems.length === 0,
      viewer.problems.slice(0, 3).join(" | "),
    );
  } finally {
    await viewer.close();
  }

  // --- API: аваагүй амжилтыг онцлуулахгүй ------------------------------------------
  const notEarned = await api.put(`${API_URL}/me/showcase`, {
    data: { badge_keys: ["ahead-of-time", "century"] },
  });
  const notEarnedBody = await notEarned.json().catch(() => null);
  check(
    "API: аваагүй амжилт → 400 SHOWCASE_BADGE_NOT_EARNED",
    notEarned.status() === 400 && notEarnedBody?.detail?.code === "SHOWCASE_BADGE_NOT_EARNED",
    `${notEarned.status()} ${JSON.stringify(notEarnedBody?.detail ?? notEarnedBody)}`,
  );
  const tooMany = await api.put(`${API_URL}/me/showcase`, {
    data: { badge_keys: ["a", "b", "c", "d", "e", "f"] },
  });
  const twice = await api.put(`${API_URL}/me/showcase`, {
    data: { badge_keys: ["ahead-of-time", "ahead-of-time"] },
  });
  check(
    "API: 5-аас олон эсвэл давхардсан түлхүүр → 422",
    tooMany.status() === 422 && twice.status() === 422,
    `${tooMany.status()}, ${twice.status()}`,
  );
  const stored = await savedShowcase();
  check(
    "API: татгалзсан хүсэлт онцлолыг өөрчлөхгүй",
    stored.join() === "ahead-of-time,first-commit",
    stored.join(", "),
  );

  // --- Бүгдийг болих ----------------------------------------------------------------
  await goto(page, "/profile");
  await waitForBadges();
  await editButton().click();
  await dialog.waitFor({ timeout: 10_000 });
  await toggle("Ahead of Time");
  await toggle("First Commit");
  const emptyCount = await pickerCount();
  const cleared = await saveShowcase();
  check(
    "бүгдийг болиход «0 / 5 сонгосон»; хадгалахад хоосон жагсаалт илгээж, мэдэгдэл гарна",
    emptyCount === "0 / 5 сонгосон" &&
      Array.isArray(cleared.keys) &&
      cleared.keys.length === 0 &&
      cleared.toast &&
      cleared.closed,
    `${emptyCount}; ${JSON.stringify(cleared)}`,
  );
  const storedAfter = await savedShowcase();
  check(
    "онцлох амжилтгүй болоход жагсаалт алга болж, «Онцлох амжилт сонгох» буцаж гарна",
    !(await showcaseRendered()) &&
      (await chooseButton().isVisible()) &&
      (await editButton().count()) === 0 &&
      storedAfter.length === 0,
    storedAfter.join(", ") || "серверт хоосон",
  );

  check("console цэвэр", problems.length === 0, problems.slice(0, 3).join(" | "));
} finally {
  await session.close();
}

process.exit(summary("Профайл ба тэмдэг") > 0 ? 1 : 0);
