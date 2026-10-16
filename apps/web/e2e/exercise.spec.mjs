/**
 * C/C++ дасгал — HackerRank маягийн «Тест ажиллуулах» ба «Илгээх».
 *
 * Хөрвүүлэгч асаалттай, өгөгдлийн сан seed хийгдсэн байх ёстой. Энэ файл
 * нь дараахыг батална:
 *
 *   • Даалгавар болон жишээ оролт/гаралт уншлагын хэсэгт харагдана,
 *   • «Оролт» эхний жишээгээр бөглөгдсөн, «Код ажиллуулах» урьдын адил,
 *   • Эхлэл код жишээ тестэд унаж, оролт/гаралтыг хажуу хажуугаар харуулна,
 *   • Зөв код жишээ тестийг давна, «Илгээх» бүх тестийг давж хичээлийг дуусгана,
 *   • Нууц тест унавал түүний оролт, гаралт харагдахгүй,
 *   • Дасгалтай хичээлд «Хичээл дууссан» товч байхгүй,
 *   • Python (Pyodide) дээр ч мөн адил — input()-ийн асуулт тооцогдохгүй,
 *   • «Тусламж» дарах бүрд анхааруулна, «Дахиж анхааруулах хэрэггүй»-г санана,
 *     зөвшөөрсний дараа л зөвлөгөө ба жишиг шийдлийг татна.
 */

import {
  API_URL,
  check,
  goto,
  newSession,
  registerNew,
  setEditorValue,
  summary,
} from "./harness.mjs";

const COURSE = "c-cpp-undes";
const LESSON = "scanf-ba-orolt";

const PY_COURSE = "python-programchlal";
const PY_LESSON = "oroltiin-utga";
// Асуулттай input() болон шинэ мөргүй төгссөн сүүлийн мөр — тестэд тооцогдохгүй.
const PY_SOLUTION = [
  'ner = input("Барааны нэр: ")',
  'une = int(input("Үнэ: "))',
  'too = int(input("Тоо: "))',
  'print(f"Бараа: {ner}")',
  'print(f"Нийт: {une * too}₮", end="")',
  "",
].join("\n");

const SOLUTION = `#include <stdio.h>

int main(void) {
    int on;
    double undur;
    scanf("%d", &on);
    scanf("%lf", &undur);
    printf("2030 онд та %d настай болно.\\n", 2030 - on);
    printf("Таны өндөр %.0f см.\\n", undur * 100);
    return 0;
}
`;

/** Кэшгүй анхны хөрвүүлэлт хэдэн секунд болж болзошгүй. */
const TIMEOUT = 90_000;

const session = await newSession({ width: 1600, height: 1000 });
const { page, problems, requests } = session;

/** Ажиллуулалт, шалгалт дуустал хүлээнэ — тэр үед товчнууд дахин идэвхжинэ. */
async function waitIdle() {
  await page.waitForFunction(
    () => {
      const button = [...document.querySelectorAll("button")].find((element) =>
        element.textContent?.includes("Илгээх"),
      );
      return button && !button.disabled;
    },
    null,
    { timeout: TIMEOUT },
  );
  await page.waitForTimeout(300);
}

async function press(name) {
  await page.getByRole("button", { name }).click();
  await waitIdle();
}

const testsPanel = () => page.locator('[role="log"][aria-label="Тест"]').innerText();

/** API-г хөтчийн cookie-гоор — хуудсан доторх `fetch` нь хөгжүүлэлтийн CSP-д баригдана. */
async function api(path, init = {}) {
  const response = await page.context().request.fetch(`${API_URL}${path}`, {
    method: init.method ?? "GET",
    headers: init.headers,
    data: init.body,
  });
  return { status: response.status(), body: await response.json().catch(() => null) };
}

try {
  await registerNew(page, "Дасгал Шалгагч");

  const course = (await api(`/courses/${COURSE}`)).body;
  const enrolled = await api(`/courses/${course.id}/enroll`, { method: "POST" });
  check("сургалтад бүртгүүлэв", enrolled.status === 201, String(enrolled.status));

  const player = (await api(`/courses/${COURSE}/lessons/${LESSON}`)).body;
  const tests = player.lesson.exercise?.tests ?? [];
  const samples = tests.filter((test) => test.sample).length;
  check("хичээл дасгалтай", samples > 0 && tests.length > samples, `${samples}/${tests.length}`);

  await goto(page, `/learn/${COURSE}/${LESSON}`, { waitFor: ".monaco-editor" });
  await page.waitForTimeout(1200);

  const body = await page.locator("body").innerText();
  check("даалгавар харагдана", body.includes("Даалгавар") && body.includes("Жишээ оролт 1"));
  check(
    "«Хичээл дууссан» товчны оронд сануулга",
    body.includes("Даалгаврын бүх тестийг давж дуусгана") &&
      (await page.getByRole("button", { name: "Хичээл дууссан" }).count()) === 0,
  );

  await page.getByRole("button", { name: "Оролт" }).click();
  check(
    "«Оролт» эхний жишээгээр бөглөгдсөн",
    (await page.inputValue("#sandbox-stdin")) === tests[0].stdin,
  );

  // --- Эхлэл код ----------------------------------------------------------------
  await press("Тест ажиллуулах");
  let panel = await testsPanel();
  check(
    "эхлэл код жишээ тестэд унана",
    panel.includes(`0/${samples} тест амжилттай`),
    panel.slice(0, 120),
  );
  check(
    "оролт, гаралтыг хажуу хажуугаар харуулна",
    panel.includes("Хүлээгдэж буй гаралт") && panel.includes("Таны гаралт"),
  );

  // --- «Код ажиллуулах» урьдын адил ---------------------------------------------
  await setEditorValue(page, SOLUTION);
  await press("Код ажиллуулах");
  const consoleText = await page.locator('[role="log"][aria-label="Console"]').innerText();
  check(
    "«Код ажиллуулах» өөрийн оролтоор ажиллана",
    consoleText.includes("25 настай") && consoleText.includes("175 см"),
    consoleText,
  );

  // --- Зөв код ------------------------------------------------------------------
  await press("Тест ажиллуулах");
  panel = await testsPanel();
  check(
    "зөв код жишээ тестүүдийг давна",
    panel.includes(`${samples}/${samples} тест амжилттай`),
    panel.slice(0, 160),
  );

  await press("Илгээх");
  await page.waitForTimeout(1500);
  panel = await testsPanel();
  check(
    "илгээхэд бүх тест давна",
    panel.includes(`${tests.length}/${tests.length} тест амжилттай`),
    panel.slice(0, 160),
  );
  check("хичээл дууслаа гэж мэдэгдэнэ", panel.includes("хичээл дууслаа"), panel.slice(0, 200));

  const progress = (await api(`/courses/${course.id}/progress`)).body;
  check("ахиц сервер дээр хадгалагдав", progress.completed_lessons === 1, JSON.stringify(progress));

  // --- Нууц тест ----------------------------------------------------------------
  // Жишээнүүдэд таарах ч 2030 онд төрсөн хүнд буруу — нууц тестэд л баригдана.
  await setEditorValue(page, SOLUTION.replace("2030 - on", "2030 - on + (on == 2030)"));
  await press("Илгээх");
  panel = await testsPanel();
  check(
    "нууц тест унавал дэлгэрэнгүйг нууна",
    panel.includes(`${tests.length - 1}/${tests.length}`) && panel.includes("Нууц тестийн оролт"),
    panel.slice(0, 300),
  );
  // Унасан нууц тестийн оролтын хоёр дахь утга (өндөр) хаана ч харагдах ёсгүй —
  // он («2030») нь гаралтын текстэд ч байдаг тул түүгээр шалгахгүй.
  const hidden = tests.find((test) => !test.sample && test.stdin.startsWith("2030"));
  const hiddenHeight = hidden?.stdin.trim().split(/\s+/)[1] ?? "";
  check(
    "нууц тестийн оролт харагдахгүй",
    hiddenHeight !== "" && !panel.includes(hiddenHeight),
    hiddenHeight,
  );

  // --- Тусламж -------------------------------------------------------------------
  const helpRequests = () => requests.filter((entry) => entry.endsWith("/help")).length;
  const warningText = "Тусламж авахдаа итгэлтэй байна уу?";

  await page.getByRole("button", { name: "Тусламж" }).click();
  let dialog = page.getByRole("dialog");
  await dialog.waitFor();
  check("«Тусламж» анхааруулга харуулна", (await dialog.innerText()).includes(warningText));
  check(
    "«Дахиж анхааруулах хэрэггүй» сонголттой",
    (await dialog.getByRole("checkbox", { name: "Дахиж анхааруулах хэрэггүй" }).count()) === 1,
  );
  await dialog.getByRole("button", { name: "Болих" }).click();
  await dialog.waitFor({ state: "hidden" });
  check("«Болих» дарвал хариу татагдахгүй", helpRequests() === 0, requests.join(", "));

  // Дахин дарахад мөн анхааруулна. Энэ удаа «дахиж битгий» гэж сонгоно.
  await page.getByRole("button", { name: "Тусламж" }).click();
  dialog = page.getByRole("dialog");
  check("дахин дарахад дахин анхааруулна", (await dialog.innerText()).includes(warningText));
  await dialog.getByRole("checkbox", { name: "Дахиж анхааруулах хэрэггүй" }).check();
  await dialog.getByRole("button", { name: "Хариуг харах" }).click();
  await page.getByText("Жишиг шийдэл").waitFor({ timeout: 15_000 });
  let helpText = await page.getByRole("dialog").innerText();
  check(
    "зөвлөгөө ба жишиг шийдэл харагдана",
    helpText.includes("Зөвлөгөө") && helpText.includes("int main"),
    helpText.slice(0, 200),
  );
  await page.keyboard.press("Escape");
  await page.getByRole("dialog").waitFor({ state: "hidden" });

  await page.getByRole("button", { name: "Тусламж" }).click();
  await page.getByText("Жишиг шийдэл").waitFor();
  helpText = await page.getByRole("dialog").innerText();
  check("сонгосны дараа анхааруулгагүй шууд харуулна", !helpText.includes(warningText));
  await page.keyboard.press("Escape");

  // --- Хөрвүүлэлтийн алдаа ------------------------------------------------------
  await setEditorValue(page, "int main(void) {\n    return x;\n}\n");
  await press("Тест ажиллуулах");
  panel = await testsPanel();
  check(
    "хөрвүүлэлтийн алдаа харагдана",
    panel.includes("Хөрвүүлэлтийн алдаа"),
    panel.slice(0, 200),
  );

  // --- Python ---------------------------------------------------------------------
  // Pyodide дээр ижил урсгал: тест бүр цэвэр нэрийн талбарт, input()-ийн
  // асуулт гаралтад тооцогдохгүй, шинэ мөргүй төгссөн гаралт ч харагдана.
  const pyCourse = (await api(`/courses/${PY_COURSE}`)).body;
  await api(`/courses/${pyCourse.id}/enroll`, { method: "POST" });
  const pyTests =
    (await api(`/courses/${PY_COURSE}/lessons/${PY_LESSON}`)).body.lesson.exercise?.tests ?? [];
  const pySamples = pyTests.filter((test) => test.sample).length;

  await goto(page, `/learn/${PY_COURSE}/${PY_LESSON}`, { waitFor: ".monaco-editor" });
  await page.waitForTimeout(1200);
  await press("Тест ажиллуулах");
  panel = await testsPanel();
  check(
    "Python: эхлэл код жишээ тестэд унана",
    panel.includes(`0/${pySamples} тест амжилттай`),
    panel.slice(0, 120),
  );

  await setEditorValue(page, PY_SOLUTION);
  await press("Илгээх");
  await page.waitForTimeout(1500);
  panel = await testsPanel();
  check(
    "Python: асуулттай input, шинэ мөргүй гаралттай шийдэл бүх тестийг давна",
    panel.includes(`${pyTests.length}/${pyTests.length} тест амжилттай`) &&
      panel.includes("хичээл дууслаа"),
    panel.slice(0, 200),
  );

  await setEditorValue(page, "ner = input()\nprint(f'Бараа: {ner}')\nprint(1 / 0)\n");
  await press("Тест ажиллуулах");
  panel = await testsPanel();
  check(
    "Python: ажиллах үеийн алдаа traceback-тайгаа",
    panel.includes("ZeroDivisionError") && panel.includes("line 3"),
    panel.slice(0, 300),
  );

  // Хөрвүүлэлтийн алдаа нь 422 хариу — хөтөч үүнийг console-д бичдэг.
  const realProblems = problems.filter(
    (entry) => !(entry.includes("Failed to load resource") && entry.includes("422")),
  );
  check("console цэвэр", realProblems.length === 0, realProblems.slice(0, 3).join(" | "));
} finally {
  await session.close();
}

process.exit(summary("Дасгал (C/C++, Python)") > 0 ? 1 : 0);
