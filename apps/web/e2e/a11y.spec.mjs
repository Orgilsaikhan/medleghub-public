/**
 * Хүртээмжийн шалгалт (axe-core, WCAG 2.1 A/AA).
 *
 * Гэрэл болон харанхуй горим хоёуланд нь ажиллана:
 *   node e2e/a11y.spec.mjs
 *   node e2e/a11y.spec.mjs --dark
 *   A11Y_ONLY=exercise,flowgorithm-tests node e2e/a11y.spec.mjs   # зөвхөн эдгээр хуудас
 *
 * Monaco болон Video.js-ийн дотоод DOM нь бидний хяналтад байхгүй тул
 * шалгалтаас хасагдсан.
 */

import fs from "node:fs";

import { chromium, request } from "playwright";

import {
  API_URL,
  BASE_URL,
  SEED,
  check,
  login,
  summary,
  suppressAnnouncements,
} from "./harness.mjs";

const DARK = process.argv.includes("--dark") || Boolean(process.env.A11Y_DARK);
const axeSource = fs.readFileSync("node_modules/axe-core/axe.min.js", "utf8");

const PAGES = [
  ["home", "/", null],
  ["courses", "/courses", null],
  // Нээлттэй хайлтын панел — сонгосон ба сонгоогүй ангилал, түвшний сонголт.
  ["courses-search", "/courses", null, "open-course-search"],
  ["detail", "/courses/javascript-undes", null],
  ["pricing", "/pricing", null],
  // Промо код хэрэглэсэн үе — хөнгөлөлттэй үнэ, «Цуцлах».
  ["pricing-promo", "/pricing", "student", "apply-promo"],
  ["privacy", "/privacy", null],
  ["terms", "/terms", null],
  ["login", "/login", null],
  ["register", "/register", null],
  // Урилгын холбоосоор — код бөглөгдсөн талбар.
  ["register-referral", "/register?ref=ABCD2345", null],
  ["dashboard", "/dashboard", "student"],
  ["profile", "/profile", "student"],
  // Онцлох амжилт сонгох цонх — сонгосон (байрны дугаартай) ба сонгоогүй амжилт. Шинэ
  // хэрэглэгчээр (`prepareShowcaseUser`).
  ["profile-showcase-dialog", "/profile", "showcase", "showcase-dialog"],
  // Нэрийн хажуугийн онцлох амжилт — фокус авахад нэр, хувь нь tooltip-оор гарна.
  ["profile-showcase-tooltip", "/profile", "showcase", "showcase-tooltip"],
  ["settings", "/settings", "student"],
  // Нэвтэрсэн үед хажуу самбарт суралцагчдын жагсаалт нэмэгдэнэ.
  ["detail-student", "/courses/javascript-undes", "student"],
  // Жагсаалтаас өөр суралцагчийн профайл руу орно.
  ["classmate", "/courses/javascript-undes", "student", "open-classmate"],
  ["feedback", "/dashboard", "student", "open-feedback"],
  // Хэрэглэгчийн цэс — урилгын код, хуулах товч.
  ["user-menu", "/dashboard", "student", "open-menu"],
  // Нууц хуудас — хөлийн логоноос олдоно, тэмдэг олгоно.
  ["footprints", "/footprints", "student"],
  ["community", "/community", "student"],
  ["community-new", "/community/new", "student"],
  // Жагсаалтаас эхний нийтлэлийг нээнэ (байхгүй бол сурагчаар нэгийг үүсгэнэ).
  ["community-post", "/community", "student", "open-post"],
  // Админд өөрийнх биш нийтлэл дээр «Мэдэгдэх» товч харагдана.
  ["community-report", "/community", "admin", "open-report"],
  // «Дүрэм» товчоор дүрмийг дахин уншина (эхний удаагийн цонх нь ижил агуулгатай).
  ["community-guidelines", "/community", "student", "open-guidelines"],
  // Суралцагчийн нийтлэл дээр админы «Түдгэлзүүлэх» цонх.
  ["community-suspend", "/community", "admin", "open-suspend"],
  ["learn", "/learn/javascript-undes/huvisagch", "student"],
  // Төлбөрт хичээл — үнэгүй сурагчид агуулгын оронд багцын санал.
  ["paywall", "/learn/javascript-undes/funkts", "student"],
  // C/C++ дасгал — «Тест ажиллуулах» дарсны дараах үр дүнгийн хэсгийг ч шалгана.
  ["exercise", "/learn/c-cpp-undes/scanf-ba-orolt", "student", "run-tests"],
  // «Тусламж»-ийн анхааруулга — «Дахиж анхааруулах хэрэггүй» сонголттой.
  ["exercise-help", "/learn/c-cpp-undes/scanf-ba-orolt", "student", "open-help"],
  // Хэцүү хичээл — «Заавар» хэсэгт шар «Хэцүү» шошго.
  ["challenging-lesson", "/learn/c-cpp-undes/c-arifmetik-ba-onooh", "student"],
  // SQL-ийн мөрдөгчийн хэрэг — «Хариулт» мөр, буруу хариултын мессеж.
  ["sql-case", "/learn/mssql-mysql-undes/hereg-01-shoniin-duudlaga", "student", "case-answer"],
  // React — урьдчилсан мэдлэгийн анхааруулга, react-tutorial маягийн засварлагч.
  ["react-detail", "/courses/react-app-buteeh", null],
  ["react-lesson", "/learn/react-app-buteeh/tavtai-moril", "student", "react-run"],
  ["react-browser", "/learn/react-app-buteeh/tavtai-moril", "student", "react-browser"],
  ["react-quiz", "/learn/react-app-buteeh/tavtai-moril", "student", "react-quiz"],
  // HTML & CSS — файлын tab, шууд шинэчлэгдэх «Хөтөч», холбоосын мэдэгдэл.
  ["html-lesson", "/learn/html-css-undes/holboos", "student"],
  ["html-browser", "/learn/html-css-undes/holboos", "student", "html-browser"],
  // Flowgorithm — блок схемийн засварлагч, даалгаврын тест, «Тусламж»-ийн схем.
  ["flowgorithm-tests", "/learn/flowgorithm-undes/input-mendchilgee", "student", "run-tests"],
  ["flowgorithm-help", "/learn/flowgorithm-undes/input-mendchilgee", "student", "open-solution"],
  ["admin", "/admin", "admin"],
  ["admin-new", "/admin/courses/new", "admin"],
  ["admin-feedback", "/admin/feedback", "admin"],
  ["admin-billing", "/admin/billing", "admin"],
  ["admin-promo", "/admin/promo", "admin"],
  ["admin-promo-edit", "/admin/promo", "admin", "open-promo-edit"],
  ["admin-announcements", "/admin/announcements", "admin"],
  // Зарлалын цонх — хэрэглэгчид гарахтай ижил бүрэлдэхүүн, «Урьдчилан харах»-аар.
  ["announcement-popup", "/admin/announcements", "admin", "announcement-preview"],
  ["admin-community", "/admin/community", "admin"],
  // MedlegHub Live — бэлэн материалыг `prepareLive()` API-аар бэлдэнэ; `:material`,
  // `:topic`-ийг түүний id-аар орлуулна. `LIVE_ACCESS=admins` үед ч админд нээлттэй.
  ["live", "/live", "admin"],
  ["live-set", "/live/materials/:material", "admin"],
  // Сэдвийн «Судлах арга» цонх (Заавар / Картууд / Тест).
  ["live-topic-menu", "/live/materials/:material", "admin", "open-topic-menu"],
  ["live-guide", "/live/materials/:material/guide/:topic", "admin", "live-guide"],
  // Эргүүлсэн карт — ар тал, үнэлгээний гурван товч.
  ["live-cards", "/live/materials/:material/cards?topic=:topic", "admin", "flip-card"],
  // Хариулсан асуулт — зөв/буруу тэмдэг, тайлбар, «Дараагийн асуулт».
  ["live-quiz", "/live/materials/:material/quiz?topic=:topic", "admin", "answer-quiz"],
  // Шалгалтын таамаг — магадлалын шошго, нээлттэй «Хариултын санаа», төлөвлөгөө.
  ["live-exam", "/live/materials/:material/exam", "admin", "open-exam-answer"],
  ["admin-live", "/admin/live", "admin"],
];

const LIVE_TITLE = "Хүртээмжийн шалгалтын лекц";
const LIVE_LECTURE = `# Вэб хуудасны бүтэц

## HTML

HTML нь хуудасны агуулга, бүтцийг тэмдэглэнэ. \`<h1>\` нь гарчиг, \`<p>\` нь догол мөр.

## CSS

CSS нь өнгө, зай, байрлалыг тодорхойлно. \`color\` нь текстийн өнгө, \`margin\` нь гадна зай.

## JavaScript

JavaScript нь хуудсыг интерактив болгоно. \`addEventListener\` нь товч дарахыг сонсоно.
`;

/** `check` нь хүлээх нөхцөл: утга буцаавал дуусна, `null` бол `ms`-ийн дараа дахин. */
async function poll(check, timeout, ms = 2_000) {
  const until = Date.now() + timeout;
  while (Date.now() < until) {
    const value = await check();
    if (value !== null) return value;
    await new Promise((resolve) => setTimeout(resolve, ms));
  }
  throw new Error("Хугацаа хэтэрлээ");
}

/**
 * Live-ийн хуудсуудад бэлэн материал (админаар). Өмнө нь үүссэн бол дахин
 * ашиглана. Заавар, сэдвийн тест, таамгийг урьдчилан үүсгэж бэлэн болтол
 * хүлээнэ — хуудас AI-г хүлээлгүй шалгагдана. Хөгжүүлэлтийн хуурамч AI хэрэгтэй.
 */
async function prepareLive() {
  const api = await request.newContext();
  try {
    await api.post(`${API_URL}/auth/login`, { data: SEED.admin });
    const config = await (await api.get(`${API_URL}/live/config`)).json();
    if (!config.enabled) {
      // `LIVE_ACCESS=off` (анхдагч) — Live-ийн хуудсууд байхгүй тул алгасна.
      console.log("  SKIP  Live-ийн хуудсууд — API-д LIVE_ACCESS=off");
      return null;
    }
    const list = await api.get(`${API_URL}/live/materials`);
    if (!list.ok()) throw new Error(`Материалын жагсаалт: ${list.status()}`);
    let material = (await list.json()).find(
      (item) => item.title === LIVE_TITLE && item.status !== "failed",
    );
    if (!material) {
      const body = Buffer.from(LIVE_LECTURE, "utf8");
      const created = await api.post(`${API_URL}/live/materials`, {
        data: {
          filename: "a11y-lekts.md",
          size_bytes: body.length,
          title: LIVE_TITLE,
        },
      });
      if (!created.ok()) throw new Error(`Материал үүсгэж чадсангүй: ${created.status()}`);
      material = await created.json();
      const uploaded = await api.put(`${API_URL}/live/materials/${material.id}/content`, {
        data: body,
        headers: { "Content-Type": "application/octet-stream" },
      });
      if (!uploaded.ok()) throw new Error(`Файл илгээж чадсангүй: ${uploaded.status()}`);
    }
    const detail = await poll(async () => {
      const current = await (await api.get(`${API_URL}/live/materials/${material.id}`)).json();
      if (current.status === "failed") throw new Error(`Боловсруулалт: ${current.error_message}`);
      return current.status === "ready" ? current : null;
    }, 180_000);
    const topic = detail.sections[0].topics[0];
    for (const input of [
      { kind: "guide", topic_id: topic.id },
      { kind: "quiz", topic_id: topic.id },
      { kind: "exam", topic_id: null },
    ]) {
      const requested = await api.post(`${API_URL}/live/materials/${material.id}/generations`, {
        data: input,
      });
      if (!requested.ok())
        throw new Error(`${input.kind} захиалж чадсангүй: ${requested.status()}`);
      const { id } = await requested.json();
      await poll(async () => {
        const generation = await (await api.get(`${API_URL}/live/generations/${id}`)).json();
        if (generation.status === "failed") throw new Error(`${input.kind}: амжилтгүй`);
        return generation.status === "ready" ? generation : null;
      }, 120_000);
    }
    return { material: material.id, topic: topic.id };
  } finally {
    await api.dispose();
  }
}

/**
 * Community-ийн хуудсууд эхний удаа хаагдахгүй дүрмийн цонх гаргадаг тул сурагч,
 * админ хоёулаа API-аар зөвшөөрнө. Хоосон сан дээр ч (эсвэл зөвхөн MedlegHub-ийн
 * нийтлэлтэй үед) нийтлэлийн хуудас шалгагдахаар сурагчаар нэг нийтлэл үүсгэнэ.
 */
async function prepareCommunity() {
  const api = await request.newContext();
  try {
    await api.post(`${API_URL}/auth/login`, { data: SEED.admin });
    await api.post(`${API_URL}/community/guidelines`);
    await api.post(`${API_URL}/auth/login`, { data: SEED.student });
    await api.post(`${API_URL}/community/guidelines`);
    const posts = await (
      await api.get(`${API_URL}/community/posts`, { params: { page_size: 50 } })
    ).json();
    if (posts.items.some((post) => post.author !== null)) return;
    const created = await api.post(`${API_URL}/community/posts`, {
      data: {
        title: "Хүртээмжийн шалгалтын нийтлэл",
        body: 'Жишээ код:\n\n```js\nconsole.log("Сайн уу");\n```',
        language: "javascript",
        type: "discussion",
      },
    });
    const { id } = await created.json();
    await api.post(`${API_URL}/community/posts/${id}/comments`, {
      data: { body: "`console.log` нь console руу хэвлэнэ." },
    });
  } finally {
    await api.dispose();
  }
}

/**
 * Онцлох амжилтын хуудсуудад зориулсан шинэ хэрэглэгч — seed хэрэглэгчийн профайлыг
 * өөрчлөхгүй тул давталт алдаагаар зогссон ч сэргээх зүйл үлдэхгүй. API-аар бэлдэнэ:
 * профайл нээхэд «Ahead of Time» олгогдоно, нууц хуудасны «Through Another's Path»-ыг
 * авч, эхнийхийг нь онцолно — цонхонд сонгосон ба сонгоогүй товч хоёулаа шалгагдана.
 */
async function prepareShowcaseUser() {
  const account = { email: `e2e-showcase-${Date.now()}@suralts.mn`, password: "Nuuts12345" };
  const api = await request.newContext();
  try {
    const registered = await api.post(`${API_URL}/auth/register`, {
      data: { ...account, name: "Онцлох Амжилт", is_16_or_older: true, accept_terms: true },
    });
    if (!registered.ok()) throw new Error(`Бүртгүүлж чадсангүй: ${registered.status()}`);
    await api.get(`${API_URL}/me/profile`);
    await api.post(`${API_URL}/me/badges/through-anothers-path`);
    const saved = await api.put(`${API_URL}/me/showcase`, {
      data: { badge_keys: ["ahead-of-time"] },
    });
    if (!saved.ok()) throw new Error(`Онцлох амжилт хадгалж чадсангүй: ${saved.status()}`);
  } finally {
    await api.dispose();
  }
  return account;
}

await prepareCommunity();

const browser = await chromium.launch();
const only = process.env.A11Y_ONLY?.split(",").filter(Boolean);
// Онцлох амжилтын хуудас шалгагдах үед л хэрэглэгч үүсгэнэ.
const showcaseUser = PAGES.some(
  ([name, , role]) => role === "showcase" && (!only || only.includes(name)),
)
  ? await prepareShowcaseUser()
  : null;
// Live-ийн хуудас шалгагдах үед л материал бэлдэнэ.
let live = null;
if (PAGES.some(([name, path]) => path.startsWith("/live") && (!only || only.includes(name)))) {
  try {
    live = await prepareLive();
  } catch (error) {
    check("Live — материал бэлдэв", false, String(error));
  }
}

for (const [name, path, role, action] of PAGES) {
  if (only && !only.includes(name)) continue;
  // Live хаалттай эсвэл материал бэлдэж чадаагүй — Live-ийн хуудсуудыг алгасна.
  if (path.startsWith("/live") && !live) continue;
  const context = await browser.newContext({
    viewport: { width: 1280, height: 900 },
    colorScheme: DARK ? "dark" : "light",
  });
  await suppressAnnouncements(context);
  const page = await context.newPage();

  if (role === "admin") await login(page, SEED.admin);
  else if (role === "student") await login(page, SEED.student);
  else if (role === "showcase") await login(page, showcaseUser);

  const target = live
    ? path.replace(":material", live.material).replace(":topic", live.topic)
    : path;
  await page.goto(BASE_URL + target, { waitUntil: "domcontentloaded" });
  if (path.startsWith("/live") || path === "/admin/live") {
    await page.locator("h1").waitFor({ timeout: 60_000 });
  }
  if (name === "paywall") {
    // Түгжээтэй хичээлд засварлагч байхгүй — багцын санал л гарна.
    await page.getByText("Энэ хичээл Standard багцад багтана").waitFor({ timeout: 60_000 });
  } else if (path.includes("/learn/flowgorithm-undes/")) {
    await page.waitForSelector('[data-testid="flow-editor"] [data-node-kind]', { timeout: 60_000 });
  } else if (path.includes("/learn/")) {
    await page.waitForSelector(".monaco-editor", { timeout: 60_000 });
  }
  await page.waitForTimeout(2200);

  if (action === "open-help") {
    await page.getByRole("button", { name: "Тусламж" }).click();
    await page.getByRole("dialog").waitFor();
    await page.waitForTimeout(300);
  }

  if (action === "open-solution") {
    await page.getByRole("button", { name: "Тусламж" }).click();
    await page.getByRole("dialog").getByRole("button", { name: "Хариуг харах" }).click();
    await page
      .getByRole("dialog")
      .locator('[aria-label="Блок схем"] [data-node-kind]')
      .first()
      .waitFor({ timeout: 15_000 });
    await page.waitForTimeout(300);
  }

  if (action === "open-classmate") {
    const classmate = page.locator('aside a[href^="/users/"]').first();
    // Хоосон сан дээр өөр суралцагч байхгүй байж болно — тэр үед хуудас л шалгагдана.
    check(`${name} — өөр суралцагч жагсаалтад байна`, (await classmate.count()) > 0);
    if ((await classmate.count()) > 0) {
      await classmate.click();
      await page.waitForURL("**/users/**");
      await page.locator("h1").waitFor();
      await page.waitForTimeout(1200);
    }
  }

  if (action === "open-guidelines") {
    await page.getByRole("button", { name: "Дүрэм" }).click();
    await page.getByRole("dialog").waitFor();
    await page.waitForTimeout(300);
  }

  if (action === "open-post" || action === "open-report" || action === "open-suspend") {
    // MedlegHub-ийн нийтлэлд зохиогч байхгүй — түдгэлзүүлэхэд суралцагчийнхыг нээнэ.
    const cards =
      action === "open-suspend"
        ? page.locator("article").filter({ hasNotText: "Албан ёсны" })
        : page.locator("article");
    await cards.locator('a[href^="/community/"]').first().click();
    await page.waitForURL(/\/community\/[0-9a-f-]{36}/);
    await page.locator("h1").waitFor();
    await page.waitForTimeout(1200);
    if (action === "open-report" || action === "open-suspend") {
      const name = action === "open-report" ? "Мэдэгдэх" : "Түдгэлзүүлэх";
      await page.locator("article").getByRole("button", { name }).click();
      await page.getByRole("dialog").waitFor();
      await page.waitForTimeout(300);
    }
  }

  if (action === "open-course-search") {
    // Гарчгийн хажуудах хайлтын товч — ангиллын логотой товчнууд, түвшний сонголт.
    await page.getByRole("button", { name: "Сургалт хайх" }).click();
    await page.locator("#course-search").waitFor({ state: "visible" });
    await page.getByRole("group", { name: "Ангилал" }).getByRole("button", { name: "Python" }).click();
    await page.waitForURL(/category=python/, { timeout: 15_000 });
    await page.waitForTimeout(700);
  }

  if (action === "apply-promo") {
    await page.getByRole("button", { name: "Промо код байна уу?" }).click();
    await page.getByLabel("Промо код", { exact: true }).fill("HELLOWORLD2026");
    await page.getByRole("button", { name: "Хэрэглэх" }).click();
    await page.getByText("20% хөнгөлөлт хэрэглэгдлээ").waitFor({ timeout: 15_000 });
    await page.waitForTimeout(300);
  }

  if (action === "announcement-preview") {
    await page.getByLabel("Онцлох боломж").check();
    await page.fill("#announcement-title", "Шинэ React сургалт");
    await page.fill("#announcement-body", "**111 хичээл** нэмэгдлээ. [Үзэх](/courses)");
    await page.fill("#announcement-cta-label", "Үзэх");
    await page.fill("#announcement-cta-url", "/courses/react-app-buteeh");
    await page.getByRole("button", { name: "Урьдчилан харах" }).click();
    await page.getByRole("dialog").waitFor();
    await page.waitForTimeout(300);
  }

  if (action === "open-promo-edit") {
    await page
      .locator('section[aria-labelledby="promo-list-title"] li')
      .first()
      .getByRole("button", { name: "Засах" })
      .click();
    await page.getByRole("dialog").waitFor();
    await page.waitForTimeout(300);
  }

  if (action === "open-menu") {
    await page.getByRole("button", { name: "Цэс" }).click();
    await page.getByRole("menuitem", { name: /^Урилгын код/ }).waitFor();
    await page.waitForTimeout(300);
  }

  if (action === "showcase-dialog") {
    await page.getByRole("button", { name: "Онцлох амжилтаа засах", exact: true }).click();
    await page.getByRole("dialog", { name: "Онцлох амжилтууд" }).waitFor();
    await page.waitForTimeout(300);
  }

  if (action === "showcase-tooltip") {
    await page
      .getByRole("list", { name: "Онцлох амжилтууд", exact: true })
      .getByRole("link")
      .first()
      .focus();
    await page.getByRole("tooltip").filter({ hasText: "Нийт хэрэглэгчдийн" }).waitFor();
    await page.waitForTimeout(300);
  }

  if (action === "open-feedback") {
    await page.getByRole("button", { name: "Цэс" }).click();
    await page.getByRole("menuitem", { name: "Санал хүсэлт" }).click();
    await page.getByRole("dialog").waitFor();
    await page.waitForTimeout(300);
  }

  if (action === "case-answer") {
    await page.getByLabel("Хариулт", { exact: true }).fill("Батбаяр");
    await page.getByRole("button", { name: "Шалгах", exact: true }).click();
    await page.getByText("Буруу байна").waitFor({ timeout: 15_000 });
    await page.waitForTimeout(300);
  }

  if (action === "react-run") {
    await page.getByRole("button", { name: "Ажиллуулах" }).click();
    await page.getByRole("status").filter({ hasText: /тест/i }).waitFor({ timeout: 30_000 });
    await page.waitForTimeout(400);
  }

  if (action === "react-browser") {
    await page.getByRole("tab", { name: "Хөтөч" }).click();
    await page.waitForTimeout(800);
  }

  if (action === "html-browser") {
    await page.getByRole("tab", { name: "Хөтөч" }).click();
    await page
      .frameLocator('iframe[title="Таны хуудасны харагдац"]')
      .getByRole("link", { name: /MDN/ })
      .click();
    await page.getByText("Гадаад холбоос", { exact: true }).waitFor({ timeout: 15_000 });
    await page.waitForTimeout(300);
  }

  if (action === "react-quiz") {
    const quiz = page.locator("fieldset").first();
    await quiz.getByRole("radio").first().check();
    await quiz.getByRole("button", { name: "Шалгах" }).click();
    await page.waitForTimeout(300);
  }

  if (action === "run-tests") {
    await page.getByRole("button", { name: "Тест ажиллуулах" }).click();
    await page.waitForSelector('[role="log"][aria-label="Тест"]', { timeout: 60_000 });
    await page.waitForFunction(
      () =>
        document
          .querySelector('[role="log"][aria-label="Тест"]')
          ?.textContent?.includes("тест амжилттай"),
      null,
      { timeout: 60_000 },
    );
  }

  if (action === "open-topic-menu") {
    await page.locator('section button[aria-haspopup="menu"]').first().click();
    await page.getByRole("menu").waitFor();
    await page.waitForTimeout(300);
  }

  if (action === "live-guide") {
    await page.locator("article").first().waitFor({ timeout: 60_000 });
    await page.waitForTimeout(300);
  }

  if (action === "flip-card") {
    const card = page.getByRole("button", { name: /Нэр томьёо/ });
    const reviewAll = page.getByRole("button", { name: "Бүгдийг давтах" });
    await Promise.race([card.waitFor({ timeout: 30_000 }), reviewAll.waitFor({ timeout: 30_000 })]);
    if (await reviewAll.isVisible()) await reviewAll.click();
    await card.click();
    await page.getByRole("group", { name: "Хэр сайн мэдэж байна вэ?" }).waitFor();
    // 3D эргэлт дуусахыг хүлээнэ.
    await page.waitForTimeout(800);
  }

  if (action === "answer-quiz") {
    await page.getByRole("button", { name: "Эхлэх" }).click({ timeout: 60_000 });
    await page.getByText(/^Асуулт 1 \/ \d+$/).waitFor();
    await page.keyboard.press("1");
    await page.getByRole("button", { name: /^(Дараагийн асуулт|Дүн харах)$/ }).waitFor();
    await page.waitForTimeout(300);
  }

  if (action === "open-exam-answer") {
    await page.getByText("Энэ бол AI-ийн таамаг").waitFor({ timeout: 60_000 });
    const outline = page.getByRole("button", { name: "Хариултын санаа" }).first();
    if ((await outline.count()) > 0) await outline.click();
    await page.waitForTimeout(300);
  }

  await page.addScriptTag({ content: axeSource });
  // Нээлттэй цэс: Radix цэсийн гадна талыг `aria-hidden` болгодог тул (цэс бүрт
  // адил) зөвхөн цэсний агуулгыг шалгана.
  const scope = action === "open-menu" || action === "open-topic-menu" ? '[role="menu"]' : ":root";
  const results = await page.evaluate(
    async (include) =>
      // `exclude` нь ЭХНИЙ аргумент (context)-д байх ёстой — options-д бичвэл
      // axe чимээгүй үл тоож, Monaco-г ч шалгана.
      window.axe.run(
        { include: [[include]], exclude: [[".monaco-editor"], [".video-js"]] },
        { runOnly: { type: "tag", values: ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"] } },
      ),
    scope,
  );

  // `minor` зэрэглэл нь ихэвчлэн зөвлөмжийн шинжтэй тул хаалт болгохгүй.
  const violations = results.violations.filter((item) => item.impact !== "minor");

  check(
    `${name} — хүртээмжийн зөрчилгүй`,
    violations.length === 0,
    violations.map((item) => `[${item.impact}] ${item.id}: ${item.help}`).join(" | "),
  );

  for (const violation of violations) {
    for (const node of violation.nodes.slice(0, 2)) {
      console.log(`      ${node.html.slice(0, 110)}`);
    }
  }

  await context.close();
}

await browser.close();
process.exit(summary(`A11y (${DARK ? "dark" : "light"})`) > 0 ? 1 : 0);
