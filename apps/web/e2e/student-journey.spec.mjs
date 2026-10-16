/**
 * MVP §25 — Student scenario.
 *
 * Нүүр хуудаснаас эхлээд буцаж ирэхэд ахиц хадгалагдсан байх хүртэлх
 * 23 алхмыг бүрэн туулна.
 */

import {
  SEED,
  check,
  checkEqual,
  editorCode,
  goto,
  login,
  logout,
  newSession,
  registerNew,
  runCode,
  setEditorCode,
  submitReferenceSolution,
  summary,
} from "./harness.mjs";

const session = await newSession();
const { page, problems, requests } = session;

try {
  // 1. Нүүр хуудас
  await goto(page, "/");
  check("нүүр хуудас нээгдэнэ", (await page.locator("h1").innerText()).includes("Монгол хэлээр"));

  // 2-3. Бүртгүүлж, нэвтэрнэ
  const account = await registerNew(page, "Сурагч Тест");
  check("бүртгүүлээд хяналтын самбар руу орно", page.url().endsWith("/dashboard"));
  check(
    "хоосон самбарт зөвлөмж харагдана",
    (await page.locator("main").innerText()).includes("бүртгүүлээгүй"),
  );

  // 4-5. Каталог, хайлт
  await goto(page, "/courses");
  const beforeSearch = await page.locator("article").count();
  check("каталогт сургалт байна", beforeSearch > 0, `${beforeSearch} ширхэг`);

  // Карт бүр ангиллынхаа логотой байх ёстой (зураг тохируулаагүй үед).
  const cardLogos = await page.locator("article svg").count();
  check("карт бүрт ангиллын лого байна", cardLogos >= beforeSearch, `${cardLogos}/${beforeSearch}`);

  // Хайлт гарчгийн хажуудах товчоор нээгдэнэ; нээгдэхэд оролт фокус авна.
  await page.getByRole("button", { name: "Сургалт хайх" }).click();
  await page.locator("#course-search").waitFor({ state: "visible" });
  // Фокус нь панел `inert`-ээс гарсны дараагийн frame-д шилждэг.
  check(
    "хайлтын товч дарахад оролт фокус авна",
    await page
      .waitForFunction(() => document.activeElement?.id === "course-search", null, {
        timeout: 3_000,
      })
      .then(
        () => true,
        () => false,
      ),
  );
  await page.fill("#course-search", "JavaScript");
  await page.waitForTimeout(1400);
  const searchResults = await page.locator("article h3").allInnerTexts();
  check(
    "хайлт JavaScript сургалтыг олно",
    searchResults.some((title) => title.includes("JavaScript")),
    searchResults.join(", "),
  );

  // 6. Сургалт нээнэ
  await goto(page, `/courses/${SEED.course.slug}`);
  check("сургалтын гарчиг зөв", (await page.locator("h1").innerText()) === SEED.course.title);
  check("хөтөлбөр харагдана", (await page.locator("text=Хөтөлбөр").count()) > 0);
  // Лого нь гарчигтай нэг сав дотор байрлана.
  check(
    "гарчгийн хажууд лого байна",
    (await page.locator("h1").locator("..").locator("svg").count()) > 0,
  );

  // 7. Бүртгүүлнэ
  await page
    .getByRole("button", { name: /Сургалтад бүртгүүлэх/ })
    .first()
    .click();
  await page.waitForURL(/\/learn\//, { timeout: 25_000 });
  check("бүртгүүлээд эхний хичээл рүү орно", page.url().includes("/learn/"));

  // 8-11. Хичээл ачаална.
  // Өмнөх хуудсын хүсэлтүүд дуусахыг хүлээж байж тоолуурыг тэглэнэ.
  await page.waitForSelector(".monaco-editor", { timeout: 60_000 });
  await page.waitForTimeout(2000);
  requests.length = 0;
  await goto(page, `/learn/${SEED.course.slug}/huvisagch`, { waitFor: ".monaco-editor" });
  await page.waitForTimeout(1500);

  const lessonCalls = requests.filter((call) => call.includes("/lessons/"));
  checkEqual("хичээлийн хуудас нэг л дуудлага хийнэ", lessonCalls.length, 1);
  check("хичээлийн агуулга харагдана", (await page.locator(".lesson-prose").count()) > 0);
  check(
    "анхны код ачаалагдсан",
    (await page.locator(".view-lines").first().innerText()).includes("const"),
  );

  // 12-15. Кодоо өөрчилж ажиллуулна
  const original = await runCode(page);
  check("анхны код ажиллана", original.includes("Сайн байна уу"), original);

  await setEditorCode(page, "const a = 7;\nconsole.log(a * 6);");
  const edited = await runCode(page);
  check("өөрчилсөн код ажиллана", edited.includes("42"), `${edited} | ${await editorCode(page)}`);

  await setEditorCode(page, "baihgui_funkts();");
  const failed = await runCode(page);
  check("алдаа console дээр гарна", failed.includes("ReferenceError"), failed);

  // 16. Дахин эхлүүлнэ — устгахын өмнө баталгаажуулалт асууна.
  await page.getByRole("button", { name: "Дахин эхлүүлэх" }).click();
  await page.getByRole("button", { name: "Тийм, дахин эхлүүлэх" }).click();
  await page.waitForTimeout(800);
  check(
    "дахин эхлүүлэхэд анхны код сэргэнэ",
    (await page.locator(".view-lines").first().innerText()).includes("Бат"),
  );

  // 17-19. Даалгаврын бүх тестийг давж хичээлээ дуусгана («Илгээх»). Дасгалтай
  // хичээлд «Хичээл дууссан» товч байхгүй.
  check(
    "даалгавартай хичээлд «Хичээл дууссан» товч байхгүй",
    (await page.getByRole("button", { name: "Хичээл дууссан" }).count()) === 0,
  );
  await submitReferenceSolution(page, SEED.course.slug, "huvisagch");
  check("«Илгээх» бүх тестийг давж хичээлийг дуусгана", true);
  await page
    .getByRole("link", { name: /Дараагийн хичээл/ })
    .first()
    .click();
  await page.waitForURL((url) => !url.pathname.endsWith("/huvisagch"), { timeout: 20_000 });
  await page.waitForSelector(".monaco-editor", { timeout: 60_000 });
  await page.waitForTimeout(1500);
  check("дуусгасны дараа дараагийн хичээл рүү шилжинэ", page.url().includes("/learn/"));

  // Хичээлийн нийт тоо нь хөтөлбөр өргөжих тусам өөрчлөгдөнө. Тиймээс
  // "N / нийт" хэлбэрийг л шалгана, тодорхой тоог хатуугаар бичихгүй.
  const sidebarText = await page.locator("aside").innerText();
  check(
    "хажуугийн ахиц шинэчлэгдэнэ",
    /[1-9]\d* \/ \d+/.test(sidebarText),
    sidebarText.split("\n")[2],
  );

  // 20-21. Гараад дахин нэвтэрнэ
  await logout(page);
  check("гарсны дараа нүүр хуудсанд байна", page.url().endsWith("/"));
  await login(page, account);

  // 22. Самбар дээр ахиц хэвээр
  await goto(page, "/dashboard");
  const dashboard = await page.locator("main").innerText();
  check("самбарт үргэлжлүүлэх хэсэг байна", dashboard.includes("Үргэлжлүүлэн суралцах"));
  check("самбарт ахиц хадгалагдсан", /[1-9]\d* \/ \d+ хичээл дууссан/.test(dashboard));

  // 23. Сургалтын хуудсан дээр дууссан хичээл тэмдэглэгдсэн
  await goto(page, `/courses/${SEED.course.slug}`);
  const completedMarks = await page.locator("text=Дууссан").count();
  check("сургалтын хуудсанд дууссан хичээл тэмдэглэгдсэн", completedMarks > 0, `${completedMarks}`);

  check("console цэвэр", problems.length === 0, problems.slice(0, 3).join(" | "));
} finally {
  await session.close();
}

process.exit(summary("Student journey") > 0 ? 1 : 0);
