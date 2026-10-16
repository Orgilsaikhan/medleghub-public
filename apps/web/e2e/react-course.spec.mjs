/**
 * React сургалт — react-tutorial.app маягийн засварлагч.
 *
 * Өгөгдлийн сан seed хийгдсэн, `public/sandbox/react-runtime.js` бүтээгдсэн
 * байх ёстой (`npm run dev`/`build` өөрөө бүтээнэ). Батлах зүйлс:
 *
 *   • Сургалтын хуудсанд урьдчилсан мэдлэгийн анхааруулга (JS, HTML & CSS),
 *   • Файлууд tab-аар, `main.jsx`, `index.html` түгжигдсэн,
 *   • Баруун талд «Заавар / Хөтөч», хичээл нээгдэхэд код автоматаар ажиллана,
 *   • «Ажиллуулах» нь тестийг шалгаж, унасан тестийн шалтгааныг харуулна,
 *   • Зөв код бүх тестийг давж хичээлийг дуусгана,
 *   • Синтакс алдаа «Хөтөч» дээр overlay, Console-д мөрийн дугаартай,
 *   • Console нь `console.log`-ийг, дадлагын API хариуг харуулна,
 *   • «Шалгах асуулт» (```quiz) хариултыг шалгана,
 *   • «Тусламж» шийдлийг харуулна, «Дахин эхлүүлэх» анхны кодыг сэргээнэ,
 *   • Нарийн дэлгэц дээр «Заавар / Код / Хөтөч» tab.
 */

import { check, goto, newSession, registerNew, summary } from "./harness.mjs";

const COURSE = "react-app-buteeh";
const FIRST = `/learn/${COURSE}/tavtai-moril`;
const ASYNC = `/learn/${COURSE}/js-module-async`;
const SOLUTION = "export default function App() {\n  return <h1>Сайн уу, React!</h1>;\n}\n";

const session = await newSession({ width: 1440, height: 900 });
const { page, problems } = session;

const preview = () => page.frameLocator('iframe[title="Таны аппын харагдац"]');

/** Нэг файлын Monaco model-ийг шууд солино (буулгах үйлдэлтэй ижил). */
async function setFile(name, code) {
  await page.waitForFunction(
    (file) =>
      (window.monaco?.editor?.getModels?.() ?? []).some((m) => m.uri.path.endsWith(`/${file}`)),
    name,
    { timeout: 60_000 },
  );
  await page.evaluate(
    ([file, next]) => {
      window.monaco.editor
        .getModels()
        .find((m) => m.uri.path.endsWith(`/${file}`))
        .setValue(next);
    },
    [name, code],
  );
  await page.waitForTimeout(300);
}

async function run() {
  await page.getByRole("button", { name: "Ажиллуулах" }).click();
  await page.waitForFunction(
    () =>
      ![...document.querySelectorAll("button")].some((b) =>
        b.textContent?.includes("Ажиллаж байна"),
      ),
    null,
    { timeout: 30_000 },
  );
  await page.waitForTimeout(400);
}

// --- Сургалтын хуудас ----------------------------------------------------------

await registerNew(page);
await goto(page, `/courses/${COURSE}`);
const prerequisites = page.getByRole("complementary", { name: "Урьдчилсан мэдлэг" });
check("Урьдчилсан мэдлэгийн анхааруулга харагдана", await prerequisites.isVisible());
check(
  "JavaScript, HTML & CSS сургалт руу холбоостой",
  (await prerequisites.getByRole("link", { name: "JavaScript үндэс" }).count()) === 1 &&
    (await prerequisites.getByRole("link", { name: "HTML & CSS үндэс" }).count()) === 1,
);
await page.getByRole("button", { name: "Сургалтад бүртгүүлэх" }).first().click();
await page.waitForTimeout(1500);

// --- Засварлагч ----------------------------------------------------------------------

await goto(page, FIRST, { waitFor: ".monaco-editor" });
const files = page.getByRole("tablist", { name: "Файлууд" });
const tabNames = (await files.getByRole("tab").allInnerTexts()).map((text) =>
  text.replace(/\s*\(түгжигдсэн\)/, "").trim(),
);
check(
  "Файлууд tab-аар: App.jsx, main.jsx, index.html",
  tabNames.join("|") === "App.jsx|main.jsx|index.html",
  tabNames.join(", "),
);
check(
  "main.jsx, index.html түгжигдсэн",
  (await files.getByRole("tab", { name: /main\.jsx \(түгжигдсэн\)/ }).count()) === 1 &&
    (await files.getByRole("tab", { name: /index\.html \(түгжигдсэн\)/ }).count()) === 1,
);
check(
  "App.jsx сонгогдсон",
  (await files.getByRole("tab", { name: "App.jsx" }).getAttribute("aria-selected")) === "true",
);
check(
  "Анхдагчаар «Заавар» нээлттэй",
  (await page.getByRole("tab", { name: "Заавар" }).getAttribute("aria-selected")) === "true",
);
check("Тестүүд (0 / 2) — ажиллуулаагүй", await page.getByText("Тестүүд (0 / 2)").isVisible());
check(
  "Шаардлагууд даалгаврын доор жагсана",
  await page.getByText("Шаардлага", { exact: true }).isVisible(),
);

await page.getByRole("tab", { name: "Хөтөч" }).click();
await preview().getByRole("heading", { name: "Hello!" }).waitFor({ timeout: 20_000 });
check("Хичээл нээгдэхэд код автоматаар ажиллана", true);
check(
  "Хаягийн мөрөнд localhost:5173/",
  (await page.getByRole("textbox", { name: /^Хаяг/ }).inputValue()) === "/",
);

// Түгжигдсэн файл өөрчлөгдөхгүй.
await files.getByRole("tab", { name: /main\.jsx/ }).click();
await page.locator(".view-lines").first().click();
await page.keyboard.type("xyz");
await page.waitForTimeout(300);
check(
  "Түгжигдсэн файлд бичихэд өөрчлөгдөхгүй",
  !(await page.locator(".view-lines").first().innerText()).includes("xyz"),
);
await files.getByRole("tab", { name: "App.jsx" }).click();

// --- Тест ----------------------------------------------------------------------------

await run();
check("Эхлэл код: 1 / 2", await page.getByText("Тестүүд (1 / 2)").isVisible());
check(
  "Унасан тестийн шалтгаан харагдана",
  await page.getByText('"Сайн уу, React!" байх ёстой, "Hello!" гарлаа.').isVisible(),
);
check(
  "«Дууссан» биш — тест давах шаардлагатай",
  await page.getByText("Даалгаврын бүх тестийг давж дуусгана").isVisible(),
);

await setFile(
  "App.jsx",
  "export default function App() {\n  return <h1>Сайн уу</h1>\n    <p>x</p>;\n}\n",
);
await run();
check(
  "Синтакс алдаа тест бүрт харагдана",
  (await page.getByText(/App\.jsx:\d+ — Синтакс алдаа/).count()) >= 1,
);
await page.getByRole("tab", { name: "Хөтөч" }).click();
check(
  "Синтакс алдаа «Хөтөч» дээр overlay",
  await preview().getByText("Синтакс алдаа").first().isVisible(),
);
check(
  "Синтакс алдаа Console-д",
  (await page.locator('[role="log"]').innerText()).includes("App.jsx:"),
);

await setFile("App.jsx", SOLUTION);
await run();
check("Зөв код: 2 / 2", await page.getByText("Тестүүд (2 / 2)").isVisible());
check(
  "Хичээл дууслаа гэсэн мэдэгдэл",
  await page.getByText("Бүх тест амжилттай — хичээл дууслаа!").isVisible(),
);
check(
  "«Дараагийн хичээл» холбоос",
  (await page.getByRole("link", { name: "Дараагийн хичээл" }).count()) >= 1,
);
check(
  "Доод мөрөнд «Дууссан»",
  await page.locator("span.text-success", { hasText: "Дууссан" }).isVisible(),
);
await preview().getByRole("heading", { name: "Сайн уу, React!" }).waitFor({ timeout: 10_000 });
check("«Хөтөч» шинэ кодыг харуулна", true);

// «Дахин эхлүүлэх»
await page.getByRole("button", { name: "Дахин эхлүүлэх" }).click();
await page.getByRole("dialog").getByRole("button", { name: "Тийм, дахин эхлүүлэх" }).click();
await preview().getByRole("heading", { name: "Hello!" }).waitFor({ timeout: 10_000 });
check(
  "«Дахин эхлүүлэх» анхны кодыг сэргээнэ",
  (await page.locator(".view-lines").first().innerText()).includes("Hello!"),
);

// «Тусламж»
await page.getByRole("button", { name: "Тусламж" }).click();
await page.getByRole("dialog").getByRole("button", { name: "Хариуг харах" }).click();
await page.getByRole("dialog").getByText("Жишиг шийдэл").waitFor({ timeout: 15_000 });
check(
  "«Тусламж» жишиг шийдлийг харуулна",
  (await page.getByRole("dialog").innerText()).includes("Сайн уу, React!"),
);
await page.keyboard.press("Escape");

// «Шалгах асуулт»
await page.getByRole("tab", { name: "Заавар" }).click();
const quiz = page.locator("fieldset").first();
await quiz.getByRole("radio").first().check();
await quiz.getByRole("button", { name: "Шалгах" }).click();
check("Буруу хариулт", await quiz.getByText("Буруу байна").isVisible());
await quiz.getByRole("radio").nth(1).check();
await quiz.getByRole("button", { name: "Шалгах" }).click();
check(
  "Зөв хариулт ба тайлбар",
  (await quiz.getByText("Зөв!").isVisible()) &&
    (await quiz.innerText()).includes("Тестүүд таны кодыг"),
);

// --- Console ба дадлагын API ------------------------------------------------------------

await goto(page, ASYNC, { waitFor: ".monaco-editor" });
await page.locator('[role="log"]').getByText("id = 2:").waitFor({ timeout: 15_000 });
check(
  "Console нь index.js-ийн хэвлэсэн утгыг харуулна",
  (await page.locator('[role="log"]').innerText()).includes("Бараанууд: []"),
);

// --- Нарийн дэлгэц ----------------------------------------------------------------------

await page.setViewportSize({ width: 390, height: 844 });
await page.waitForTimeout(800);
const mobileTabs = await page.getByRole("tab", { name: /^(Заавар|Код|Хөтөч)$/ }).allInnerTexts();
check(
  "Нарийн дэлгэц: Заавар / Код / Хөтөч",
  mobileTabs.map((text) => text.trim()).join("|") === "Заавар|Код|Хөтөч",
  mobileTabs.join(", "),
);
await page.getByRole("tab", { name: "Код" }).click();
check("«Код» tab-д засварлагч ба тест", await page.getByText("Тестүүд (0 / 4)").isVisible());

check("Хуудасны алдаа гараагүй", problems.length === 0, problems.join("\n"));

await session.close();
process.exit(summary("React сургалт") ? 1 : 0);
