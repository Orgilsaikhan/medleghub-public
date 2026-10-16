/**
 * MVP §25 — Admin scenario.
 *
 * Админ сургалт үүсгээд нийтлэх хүртэл, тэгээд оюутан түүнээс суралцах
 * хүртэлх 11 алхмыг туулна.
 */

import {
  SEED,
  check,
  goto,
  login,
  logout,
  newSession,
  runCode,
  summary,
} from "./harness.mjs";

const stamp = Date.now();
const slug = `e2e-surgalt-${stamp}`;
const lessonSlug = "e2e-hicheel";

const session = await newSession({ width: 1600, height: 1000 });
const { page, problems } = session;

try {
  // 1. Оюутан админ руу орж чадахгүй
  await login(page, SEED.student);
  await goto(page, "/admin");
  await page.waitForTimeout(1800);
  check("оюутныг /admin-аас буцаана", !page.url().includes("/admin"), page.url());
  await logout(page);

  // 2. Админ нэвтэрнэ
  await login(page, SEED.admin);
  await goto(page, "/admin");
  check("админд удирдлагын хуудас нээгдэнэ", (await page.locator("h1").innerText()).length > 0);

  // Багцыг гараар нэмж, хасна. Standard хэрэглэгчид +1, −1 — нийт өөрчлөлтгүй.
  await goto(page, "/admin/billing", { waitFor: "#user-plan-email" });
  await page.fill("#user-plan-email", SEED.standard.email);
  await page.getByRole("button", { name: "Хайх" }).click();
  await page.locator("#user-plan-status").waitFor({ timeout: 15_000 });
  const statusBefore = await page.locator("#user-plan-status").innerText();
  check(
    "хэрэглэгчийн багц хэдэн хоног үлдсэнтэй харагдана",
    /хоног үлдсэн/.test(statusBefore),
    statusBefore,
  );

  const firstChange = page.locator("#user-plan-history + ul li").first();
  await page.getByRole("button", { name: "1 сар нэмэх" }).click();
  await page.getByText("Багц шинэчлэгдлээ.").first().waitFor({ timeout: 15_000 });
  check("нэмсэн сар түүхэнд үлдэнэ", (await firstChange.innerText()).includes("+1 сар"));

  await page.getByRole("button", { name: "1 сар хасах" }).click();
  await page.getByRole("dialog").getByRole("button", { name: "1 сар хасах" }).click();
  await page.waitForTimeout(1500);
  check("хассан сар түүхэнд үлдэнэ", (await firstChange.innerText()).includes("−1 сар"));
  check(
    "нэмээд хасахад дуусах хугацаа хэвээр",
    (await page.locator("#user-plan-status").innerText()) === statusBefore,
  );

  // 3. Сургалт үүсгэнэ
  await goto(page, "/admin/courses/new");
  await page.fill("#title", "E2E сургалт");
  await page.fill("#slug", slug);
  await page.fill("#description", "Автомат тестээр үүсгэсэн сургалт.");
  await page.getByRole("button", { name: "Хадгалах" }).click();
  await page.waitForURL(/\/admin\/courses\/[^/]+\/modules/, { timeout: 25_000 });
  const courseId = new URL(page.url()).pathname.split("/")[3];
  check("сургалт үүснэ", Boolean(courseId), courseId);

  // 4. Модул үүсгэнэ
  for (const title of ["E2E модул 1", "E2E модул 2"]) {
    await page.getByRole("button", { name: "Шинэ модул" }).click();
    await page.waitForTimeout(800);
    await page.fill("#module-title", title);
    await page.getByRole("button", { name: "Хадгалах" }).click();
    await page.waitForTimeout(2200);
  }
  const moduleTitles = await page.locator("ol > li > div:first-child p:first-child").allInnerTexts();
  check("хоёр модул үүснэ", moduleTitles.length === 2, moduleTitles.join(", "));

  // 5. Дараалал солино
  await page.getByRole("button", { name: "Дээш" }).nth(1).click();
  await page.waitForTimeout(2200);
  const reordered = await page.locator("ol > li > div:first-child p:first-child").allInnerTexts();
  check("дараалал солигдоно", reordered[0] === "E2E модул 2", reordered.join(", "));

  // 6-8. Видео, Markdown, анхны кодтой хичээл үүсгэнэ
  await page.getByRole("link", { name: "Шинэ хичээл" }).first().click();
  await page.waitForURL(/\/admin\/lessons\/new/, { timeout: 20_000 });
  await page.waitForTimeout(1200);
  await page.fill("#title", "E2E хичээл");
  await page.fill("#slug", lessonSlug);
  await page.fill("#description", "Автомат тестийн хичээл.");
  await page.fill("#video_url", "https://cdn.example.com/lesson.m3u8");
  await page.fill("#duration_minutes", "4");
  await page.fill("#content", "### Тестийн гарчиг\n\nЭнэ бол **markdown** агуулга.");
  await page.fill("#initial_code", "console.log(6 * 7);");

  // 9. Хичээлийг нийтэлнэ
  await page.locator("#published").click();
  await page.getByRole("button", { name: "Хадгалах" }).click();
  await page.waitForURL(/\/modules$/, { timeout: 25_000 });
  await page.waitForTimeout(2000);
  check("хичээл нийтлэгдсэн төлөвтэй үүснэ", (await page.locator("text=Нийтлэгдсэн").count()) > 0);

  // Markdown урьдчилан харах
  await page.getByRole("link", { name: "E2E хичээл" }).first().click();
  await page.waitForURL(/\/admin\/lessons\/[^/]+$/, { timeout: 20_000 });
  await page.waitForTimeout(1500);
  await page.getByRole("tab", { name: "Урьдчилан харах" }).click();
  await page.waitForTimeout(600);
  const previewText = await page.locator('[role="tabpanel"]').last().innerText();
  check("markdown урьдчилан харагдана", previewText.includes("markdown"), previewText.trim());

  // 10. Нийтлэгдээгүй сургалт нийтэд харагдахгүй
  await logout(page);
  await goto(page, `/courses/${slug}`);
  check(
    "нийтлэгдээгүй сургалт зочинд харагдахгүй",
    (await page.locator("body").innerText()).includes("Хуудас олдсонгүй"),
  );

  // Сургалтыг нийтэлнэ
  await login(page, SEED.admin);
  await goto(page, `/admin/courses/${courseId}`);
  await page.locator("#published").click();
  await page.getByRole("button", { name: "Хадгалах" }).click();
  await page.waitForTimeout(2500);
  await logout(page);

  // 11. Оюутан үзэж, бүртгүүлж, суралцана
  await login(page, SEED.student);
  await goto(page, `/courses/${slug}`);
  check("оюутанд нийтлэгдсэн сургалт харагдана", (await page.locator("h1").innerText()) === "E2E сургалт");

  await page.getByRole("button", { name: /Сургалтад бүртгүүлэх/ }).first().click();
  await page.waitForURL(/\/learn\//, { timeout: 25_000 });
  await page.waitForSelector(".monaco-editor", { timeout: 60_000 });
  await page.waitForTimeout(1800);

  const output = await runCode(page);
  check("админы бичсэн код оюутны талд ажиллана", output.includes("42"), output);
  check("админы markdown хичээл дээр харагдана", (await page.locator(".lesson-prose").innerText()).includes("markdown"));

  // Видеотой хичээлд тоглуулагч гарч ирнэ
  check("видео тоглуулагч ачаалагдана", (await page.locator("video, video-js").count()) > 0);

  // CSP нь тохируулсан видео домэйныг зөвшөөрч байгаа эсэхийг шалгана:
  // хаалт хийсэн бол "violates ... Content Security Policy" гэсэн алдаа гарна.
  check(
    "CSP тохируулсан видео домэйныг хаахгүй",
    !problems.some((item) => /Content Security Policy/.test(item)),
    problems.find((item) => /Content Security Policy/.test(item)) ?? "",
  );

  // cdn.example.com бол хуурамч хаяг — DNS болон тоглуулагчийн алдааг тооцохгүй.
  const realProblems = problems.filter(
    (item) => !/ERR_NAME_NOT_RESOLVED|VIDEOJS|MEDIA_ERR|Failed to load resource/.test(item),
  );
  check("console цэвэр", realProblems.length === 0, realProblems.slice(0, 3).join(" | "));
} finally {
  await session.close();
}

process.exit(summary("Admin journey") > 0 ? 1 : 0);
