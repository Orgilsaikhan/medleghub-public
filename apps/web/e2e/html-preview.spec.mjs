/**
 * HTML & CSS сургалтын «Хөтөч» — код бичих зуур шинэчлэгдэх урьдчилсан харагдац.
 *
 * Өгөгдлийн сан seed хийгдсэн байх ёстой (CSS хичээлүүд `index.html` +
 * `style.css`-тэй). Батлах зүйлс:
 *
 *   • Файлууд tab-аар, баруун талд «Заавар / Хөтөч», байрлал солих товчгүй,
 *   • HTML засвар «Хөтөч»-ид өөрөө орно,
 *   • CSS засвар хуудсыг дахин ачаалалгүй солигдоно; `<link>`-гүй бол CSS нөлөөлөхгүй,
 *   • `#id` холбоос хуудас дотроо гүйлгэнэ, iframe манай сайт руу шилжихгүй,
 *   • Гадаад, байхгүй, `mailto:` холбоос, форм илгээлт мэдэгдэл болно,
 *   • Олон хуудастай хичээлд холбоосоор хуудас солигдож, «Буцах» ажиллана,
 *   • Утас / таблет өргөн, «Дахин эхлүүлэх», нарийн дэлгэцийн tab.
 */

import { check, goto, login, newSession, SEED, summary } from "./harness.mjs";

const COURSE = "html-css-undes";
const LINKS = `/learn/${COURSE}/holboos`;
const FORM = `/learn/${COURSE}/form-ba-input`;
const SITE = `/learn/${COURSE}/engiin-vebsait`;
const CSS = `/learn/${COURSE}/css-gej-yu-ve`;

const FRAME = 'iframe[title="Таны хуудасны харагдац"]';
const TEAL = "rgb(0, 128, 128)";
const CRIMSON = "rgb(220, 20, 60)";

const session = await newSession({ width: 1440, height: 900 });
const { page, problems } = session;

const preview = () => page.frameLocator(FRAME);
const frame = async () => (await page.$(FRAME)).contentFrame();
const address = () => page.getByRole("textbox", { name: /Хаяг/ });

async function waitForModel(name) {
  await page.waitForFunction(
    (file) =>
      (window.monaco?.editor?.getModels?.() ?? []).some((m) => m.uri.path.endsWith(`/${file}`)),
    name,
    { timeout: 60_000 },
  );
}

async function getFile(name) {
  await waitForModel(name);
  return page.evaluate(
    (file) =>
      window.monaco.editor
        .getModels()
        .find((m) => m.uri.path.endsWith(`/${file}`))
        .getValue(),
    name,
  );
}

/** Нэг файлын Monaco model-ийг шууд солино (буулгах үйлдэлтэй ижил). */
async function setFile(name, code) {
  await waitForModel(name);
  await page.evaluate(
    ([file, next]) => {
      window.monaco.editor
        .getModels()
        .find((m) => m.uri.path.endsWith(`/${file}`))
        .setValue(next);
    },
    [name, code],
  );
}

async function openBrowser() {
  await page.getByRole("tab", { name: "Хөтөч" }).click();
  await preview().locator("body").waitFor({ timeout: 15_000 });
  await page.waitForTimeout(300);
}

async function visible(locator, timeout = 5000) {
  try {
    await locator.waitFor({ timeout });
    return true;
  } catch {
    return false;
  }
}

const colorOf = (locator) => locator.evaluate((element) => getComputedStyle(element).color);

await login(page, SEED.standard);

// --- HTML хичээл: нэг файл, холбоосууд ---------------------------------------------------

await goto(page, LINKS, { waitFor: ".monaco-editor" });
check("«index.html» файлын tab", await page.getByRole("tab", { name: "index.html" }).isVisible());
check(
  "Байрлал солих товч HTML хичээлд алга",
  (await page.getByRole("button", { name: /байрлал$/ }).count()) === 0,
);
await openBrowser();
check(
  "«Хөтөч» хуудсыг харуулна",
  await visible(preview().locator("h1", { hasText: "Холбоосын төрлүүд" })),
);
check("Хаягийн мөрөнд index.html", (await address().inputValue()) === "index.html");

const links = await getFile("index.html");
await setFile(
  "index.html",
  links
    .replace("Холбоосын төрлүүд", "Миний холбоосууд")
    .replace('<h2 id="tugsgul">', '<p class="zai">Урт хуудас</p>\n    <h2 id="tugsgul">'),
);
check(
  "HTML засвар «Хөтөч»-ид өөрөө орно",
  await visible(preview().locator("h1", { hasText: "Миний холбоосууд" })),
);
// Хуудсыг гүйлгэх зайтай болгоно — `#tugsgul` руу үсрэхийг шалгахын тулд.
await (
  await frame()
).evaluate(() => {
  document.querySelector(".zai").style.height = "2000px";
});
await preview().getByRole("link", { name: "Төгсгөл рүү" }).click();
await page.waitForTimeout(400);
const afterJump = await (
  await frame()
).evaluate(() => ({
  y: window.scrollY,
  href: location.href,
}));
check(
  "#id холбоос хуудас дотроо гүйлгэнэ",
  afterJump.y > 1000 && afterJump.href === "about:srcdoc",
  JSON.stringify(afterJump),
);

await preview().getByRole("link", { name: /MDN/ }).click();
check(
  "Гадаад холбоос мэдэгдэл болно",
  await visible(page.getByText("Гадаад холбоос", { exact: true })),
);
check(
  "Шинэ табд нээх холбоос MDN руу",
  (await page.getByRole("link", { name: "Шинэ табд нээх" }).getAttribute("href")) ===
    "https://developer.mozilla.org/",
);
await preview().getByRole("link", { name: "Сургалтууд" }).click();
check("Байхгүй хуудас мэдэгдэл", await visible(page.getByText("Хуудас олдсонгүй")));
await preview().getByRole("link", { name: "Бидэнтэй холбогдох" }).click();
check("mailto: холбоос мэдэгдэл", await visible(page.getByText("Өөр апп-ын холбоос")));
check(
  "Холбоос дарсны дараа ч iframe хуудсандаа",
  (await (await frame()).evaluate(() => location.href)) === "about:srcdoc",
);

// --- Форм ------------------------------------------------------------------------------------

await goto(page, FORM, { waitFor: ".monaco-editor" });
await openBrowser();
await preview().locator('input[name="ner"]').fill("Бат");
await preview().locator('input[name="zuvshuurul"]').check();
await preview().getByRole("button", { name: "Бүртгүүлэх" }).click();
const submitted = page.getByText("Форм илгээгдлээ");
check("Форм илгээлт мэдэгдэл болно", await visible(submitted));
const submitCard = page.locator("div").filter({ has: submitted }).last();
const submitText = (await submitCard.innerText().catch(() => "")) ?? "";
check(
  "Илгээх байсан өгөгдлийг харуулна",
  submitText.includes("POST /burtgel") && submitText.includes("Бат"),
  submitText.replace(/\s+/g, " ").slice(0, 200),
);

// --- Олон хуудас -------------------------------------------------------------------------------

await goto(page, SITE, { waitFor: ".monaco-editor" });
check(
  "Олон хуудастай хичээлд index.html, tuhai.html",
  (await page.getByRole("tab", { name: "index.html" }).isVisible()) &&
    (await page.getByRole("tab", { name: "tuhai.html" }).isVisible()),
);
await openBrowser();
await preview().getByRole("link", { name: "Тухай" }).click();
check(
  "Холбоосоор tuhai.html нээгдэнэ",
  await visible(preview().locator("h1", { hasText: "Бидний тухай" })),
);
check("Хаягийн мөрөнд tuhai.html", (await address().inputValue()) === "tuhai.html");
await page.getByRole("button", { name: "Буцах" }).click();
check(
  "«Буцах» нүүр хуудас руу",
  await visible(preview().locator("h1", { hasText: "Гэрэл зургийн студи" })),
);
await address().fill("tuhai.html");
await address().press("Enter");
check("Хаяг бичээд Enter", await visible(preview().locator("h1", { hasText: "Бидний тухай" })));

// --- CSS хичээл ----------------------------------------------------------------------------------

await goto(page, CSS, { waitFor: ".monaco-editor" });
const styleTab = page.getByRole("tab", { name: "style.css" });
check(
  "CSS хичээлд index.html + style.css, style.css нээлттэй",
  (await page.getByRole("tab", { name: "index.html" }).isVisible()) &&
    (await styleTab.getAttribute("aria-selected")) === "true",
);
await openBrowser();
const heading = preview().locator("h1");
await heading.waitFor({ timeout: 15_000 });
check("style.css хуудсанд хэрэглэгдэнэ", (await colorOf(heading)) === TEAL);

await (
  await frame()
).evaluate(() => {
  window.__sameDocument = true;
});
const css = await getFile("style.css");
await setFile("style.css", css.replace("color: teal;", "color: crimson;"));
await page.waitForTimeout(700);
check("CSS засвар шууд харагдана", (await colorOf(heading)) === CRIMSON);
check(
  "CSS засвар хуудсыг дахин ачаалахгүй",
  (await (await frame()).evaluate(() => window.__sameDocument)) === true,
);

// Monaco нь файлын model-ийг tab нээгдэхэд л үүсгэнэ.
await page.getByRole("tab", { name: "index.html" }).click();
const html = await getFile("index.html");
await setFile("index.html", html.replace(/\s*<link rel="stylesheet" href="style.css" \/>/, ""));
await page.waitForTimeout(1200);
check(
  "<link>-гүй бол style.css нөлөөлөхгүй",
  (await colorOf(preview().locator("h1"))) === "rgb(0, 0, 0)",
);

await page.getByRole("button", { name: "Утас (375px)" }).click();
await page.waitForTimeout(300);
const box = await page.locator(FRAME).boundingBox();
check("Утасны өргөн 375px", Math.round(box?.width ?? 0) === 375, String(box?.width));
check("Өргөн пикселээр", await page.getByText("375px", { exact: true }).isVisible());
await page.getByRole("button", { name: "Бүтэн өргөн" }).click();

await page.getByRole("button", { name: "Дахин эхлүүлэх" }).click();
await page.getByRole("button", { name: "Тийм, дахин эхлүүлэх" }).click();
await page.waitForTimeout(800);
await styleTab.click();
check(
  "«Дахин эхлүүлэх» анхны кодыг сэргээнэ",
  (await getFile("style.css")) === css && (await colorOf(preview().locator("h1"))) === TEAL,
);

// --- Нарийн дэлгэц ----------------------------------------------------------------------------

await page.setViewportSize({ width: 390, height: 844 });
await page.waitForTimeout(800);
const mobileTabs = await page.getByRole("tab", { name: /^(Заавар|Код|Хөтөч)$/ }).allInnerTexts();
check(
  "Нарийн дэлгэц: Заавар / Код / Хөтөч",
  mobileTabs.map((text) => text.trim()).join("|") === "Заавар|Код|Хөтөч",
  mobileTabs.join(", "),
);
await page.getByRole("tab", { name: "Хөтөч" }).click();
check("Нарийн дэлгэц дээр «Хөтөч»", await visible(preview().locator("h1")));

check("Хуудасны алдаа гараагүй", problems.length === 0, problems.join("\n"));

await session.close();
process.exit(summary("HTML & CSS «Хөтөч»") ? 1 : 0);
