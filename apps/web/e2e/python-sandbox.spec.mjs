/**
 * Python sandbox — хөтөч доторх гүйцэтгэл.
 *
 * Pyodide (WebAssembly дээрх CPython) нь сурагчийн кодыг worker дотор
 * ажиллуулна. Сервер рүү код илгээгддэггүй. Энэ файл нь дараахыг батална:
 *
 *   • Код үнэхээр ажиллаж, гаралт нь зөв (кирилл үсэг орсон ч),
 *   • Стандарт сан бүрэн байгаа (татах шаардлагагүй),
 *   • Алдааны мөрийн дугаар зөв,
 *   • Ачаалсны ДАРАА сүлжээ хаагдсан — код гадагш хандаж чадахгүй,
 *   • Төгсгөлгүй давталт хуудсыг зогсоохгүй, дараа нь дахин ажиллана.
 */

import {
  SEED,
  check,
  goto,
  login,
  newSession,
  setEditorValue,
  summary,
} from "./harness.mjs";

const LESSON = "/learn/python-programchlal/programm-gej-yu-ve";

/** Pyodide анх ачаалахад удаж болзошгүй тул хүлээх хугацаа урт. */
const RUN_TIMEOUT = 120_000;

const session = await newSession({ width: 1600, height: 1000 });
const { page, problems } = session;

/** Кодыг ажиллуулаад console-ийн гаралтыг буцаана. */
async function run(code, { timeout = RUN_TIMEOUT } = {}) {
  // Өмнөх гаралтыг арилгана. Товч идэвхгүй бол (гаралт байхгүй) алгасна.
  await page
    .locator('[aria-label="Console цэвэрлэх"]')
    .click({ timeout: 1500 })
    .catch(() => {});
  await setEditorValue(page, code);
  await page.getByRole("button", { name: "Код ажиллуулах" }).click();

  await page.waitForFunction(
    () => {
      const button = [...document.querySelectorAll("button")].find((element) =>
        element.textContent?.includes("Код ажиллуулах"),
      );
      return button && !button.disabled;
    },
    null,
    { timeout },
  );
  await page.waitForTimeout(250);
  return (await page.locator('[role="log"]').innerText()).replace(/^›\s*/gm, "").trim();
}

try {
  await login(page, SEED.student);
  await goto(page, LESSON, { waitFor: ".monaco-editor" });

  // --- Товч идэвхтэй болсон ------------------------------------------------
  check(
    "Python хичээл дээр Ажиллуулах товч идэвхтэй",
    !(await page.getByRole("button", { name: "Код ажиллуулах" }).isDisabled()),
  );

  // --- Үндсэн гүйцэтгэл ----------------------------------------------------
  const basic = await run('print("Сайн уу, Суралц!")\nprint(2 ** 10)\n');
  check("print ажиллана", basic.includes("Сайн уу, Суралц!"), basic);
  check("тооцоолол зөв", basic.includes("1024"), basic);

  const loop = await run("for i in range(1, 4):\n    print(i, i * i)\n");
  check("давталт бүх мөрийг хэвлэнэ", loop.includes("1 1") && loop.includes("3 9"), loop);

  // --- Стандарт сан --------------------------------------------------------
  // Багц татахгүйгээр ажиллах ёстой: python_stdlib.zip дотор бүгд ирдэг.
  const stdlib = await run(
    [
      "import math, json",
      "from dataclasses import dataclass",
      "from collections import Counter",
      "",
      "@dataclass",
      "class Suragch:",
      "    ner: str",
      "    onoo: int",
      "",
      'print(json.dumps({"pi": round(math.pi, 3)}))',
      'print(Suragch("Бат", 95))',
      'print(Counter("aabbbc").most_common(1))',
      "",
    ].join("\n"),
  );
  check("math ба json ажиллана", stdlib.includes('"pi": 3.142'), stdlib);
  check("dataclasses ажиллана", stdlib.includes("Suragch(ner='Бат', onoo=95)"), stdlib);
  check("collections ажиллана", stdlib.includes("('b', 3)"), stdlib);

  // --- Алдааны мэдээлэл ----------------------------------------------------
  const failure = await run("a = 5\nb = 0\nprint(a / b)\n");
  check("алдааны төрөл харагдана", failure.includes("ZeroDivisionError"), failure);
  check("алдаатай мөрийн дугаар зөв", /line 3/.test(failure), failure);
  check(
    "Pyodide-ийн дотоод мөрүүд нуугдсан",
    !failure.includes("_pyodide") && !failure.includes("/lib/python"),
    failure,
  );

  // Хаалт дутуу бичвэл Monaco автоматаар хаадаг тул цэг таслал дутуу
  // тохиолдлыг шалгана — энэ нь шинэ суралцагчийн хамгийн түгээмэл алдаа.
  const syntax = await run('if True\n    print("цэг таслалгүй")\n');
  check("SyntaxError мэдэгдэнэ", syntax.includes("SyntaxError"), syntax);

  // --- Стандарт оролт ------------------------------------------------------
  await page.getByRole("button", { name: "Оролт" }).click();
  await page.fill("#sandbox-stdin", "Болд\n7");

  const withStdin = await run(
    ['ner = input()', 'nas = int(input())', 'print(f"{ner} — {nas} нас")', ""].join("\n"),
  );
  check("input() оролтын мөрийг уншина", withStdin.includes("Болд — 7 нас"), withStdin);

  await page.fill("#sandbox-stdin", "");
  const noStdin = await run('x = input()\nprint(x)\n');
  check("оролт хоосон бол EOFError", noStdin.includes("EOFError"), noStdin);

  // --- Тусгаарлалт ---------------------------------------------------------
  // Ачаалсны дараа сүлжээний API устсан байх ёстой.
  const network = await run(
    [
      "from js import self as js_self",
      'for name in ("fetch", "XMLHttpRequest", "WebSocket", "importScripts", "indexedDB"):',
      "    print(name, getattr(js_self, name, None) is None)",
      "",
    ].join("\n"),
  );
  check(
    "fetch устсан",
    network.includes("fetch True"),
    network,
  );
  check("XMLHttpRequest устсан", network.includes("XMLHttpRequest True"), network);
  check("WebSocket устсан", network.includes("WebSocket True"), network);
  check("indexedDB устсан", network.includes("indexedDB True"), network);

  const dom = await run(
    [
      "from js import self as js_self",
      'print("document", getattr(js_self, "document", None) is None)',
      'print("localStorage", getattr(js_self, "localStorage", None) is None)',
      "",
    ].join("\n"),
  );
  check("DOM байхгүй", dom.includes("document True"), dom);
  check("localStorage байхгүй", dom.includes("localStorage True"), dom);

  // Backend рүү код илгээгддэггүй — sandbox нь ямар ч API дуудлага үүсгэхгүй.
  const apiCalls = session.requests.filter((entry) => entry.includes("run") || entry.includes("exec"));
  check("код сервер рүү илгээгдээгүй", apiCalls.length === 0, apiCalls.join(", "));

  // --- Төгсгөлгүй давталт --------------------------------------------------
  const hung = await run("while True:\n    pass\n", { timeout: 60_000 });
  check("төгсгөлгүй давталт тасалдана", hung.includes("хэт удаан"), hung);

  const responsive = await page.evaluate(() => {
    document.title = "amid";
    return document.title;
  });
  check("хуудас амьд хэвээр", responsive === "amid");

  // Worker-ыг дахин үүсгээд ажиллах ёстой.
  const afterKill = await run('print("дахин ажиллалаа")\n');
  check("тасалсны дараа дахин ажиллана", afterKill.includes("дахин ажиллалаа"), afterKill);

  // --- Console цэвэр -------------------------------------------------------
  check("console цэвэр", problems.length === 0, problems.slice(0, 3).join(" | "));
} finally {
  await session.close();
}

process.exit(summary("Python sandbox") > 0 ? 1 : 0);
