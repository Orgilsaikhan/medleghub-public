/**
 * C/C++ sandbox — серверт хөрвүүлж, хөтөч дотор ажиллуулна.
 *
 * `apps/compiler` үйлчилгээ асаалттай, API-ийн `COMPILER_URL` түүн рүү заасан
 * байх ёстой. Энэ файл нь дараахыг батална:
 *
 *   • C ба C++ код хөрвүүлэгдэж, кирилл гаралт зөв харагдана,
 *   • scanf/cin «Оролт»-ын мөр бүрийг уншиж, хариулт нь асуултын ард гарна,
 *   • Хөрвүүлэлтийн алдаа мөр/баганатай, серверийн дотоод замгүй харагдана,
 *   • -Wall анхааруулга харагдана,
 *   • Ажиллах үеийн алдаа, барьж аваагүй exception ойлгомжтой,
 *   • Төгсгөлгүй давталт тасалдаж, түүнээс өмнөх гаралт үлдэнэ,
 *   • Зөвхөн «Оролт» өөрчлөхөд сервер рүү дахин хандахгүй.
 */

import { SEED, check, goto, login, newSession, setEditorValue, summary } from "./harness.mjs";

const C_LESSON = "/learn/c-cpp-undes/c-gej-yu-ve";
const CPP_LESSON = "/learn/c-cpp-undes/cout-garalt";

/** Кэшгүй анхны хөрвүүлэлт хэдэн секунд болж болзошгүй. */
const RUN_TIMEOUT = 60_000;

const session = await newSession({ width: 1600, height: 1000 });
const { page, problems, requests } = session;

const compileCalls = () => requests.filter((entry) => entry === "POST /api/v1/compile").length;

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

async function openStdin(lines) {
  if ((await page.locator("#sandbox-stdin").count()) === 0) {
    await page.getByRole("button", { name: "Оролт" }).click();
  }
  await page.fill("#sandbox-stdin", lines);
}

const SCANF = [
  "#include <stdio.h>",
  "",
  "int main(void) {",
  "    char ner[32];",
  "    int nas;",
  '    printf("Нэрээ оруулна уу: ");',
  '    scanf("%31s", ner);',
  '    printf("Насаа оруулна уу: ");',
  '    scanf("%d", &nas);',
  '    printf("%s, %d нас\\n", ner, nas);',
  "    return 0;",
  "}",
  "",
].join("\n");

try {
  // C++ хичээл (#28) нь төлбөрт хэсэгт — багцтай хэрэглэгчээр.
  await login(page, SEED.standard);
  await goto(page, C_LESSON, { waitFor: ".monaco-editor" });

  check(
    "C хичээл дээр Ажиллуулах товч идэвхтэй",
    !(await page.getByRole("button", { name: "Код ажиллуулах" }).isDisabled()),
  );
  check("Оролт товч харагдана", (await page.getByRole("button", { name: "Оролт" }).count()) > 0);

  // Сурагч тайлбараа уншиж байх зуур анхны код хөрвүүлэгдэж эхэлнэ.
  for (let attempt = 0; attempt < 40 && compileCalls() === 0; attempt++) {
    await page.waitForTimeout(250);
  }
  check("анхны код урьдчилан хөрвүүлэгдэнэ", compileCalls() >= 1, requests.join(", "));

  // --- Гаралт ---------------------------------------------------------------
  const hello = await run(
    '#include <stdio.h>\n\nint main(void) {\n    printf("Сайн байна уу, MedlegHub!\\n");\n    printf("%d\\n", 6 * 7);\n    return 0;\n}\n',
  );
  check(
    "C код ажиллаж кирилл гаралт харагдана",
    hello.includes("Сайн байна уу, MedlegHub!"),
    hello,
  );
  check("тооцоолол зөв", hello.includes("42"), hello);

  // --- Хөрвүүлэлтийн алдаа ----------------------------------------------------
  const broken = await run(
    "#include <stdio.h>\n\nint main(void) {\n    int b = 3\n    return b;\n}\n",
  );
  check("хөрвүүлэлтийн алдаа гарчигтай харагдана", broken.includes("Хөрвүүлэлтийн алдаа"), broken);
  check("алдаатай мөр, багана зөв", broken.includes("main.c:4:"), broken);
  check(
    "серверийн дотоод зам харагдахгүй",
    !broken.includes("/tmp") && !broken.includes("/emsdk") && !broken.includes("emcc: error"),
    broken,
  );

  // --- Анхааруулга ------------------------------------------------------------
  const warned = await run(
    '#include <stdio.h>\n\nint main(void) {\n    int nas;\n    printf("%d\\n", nas);\n    return 0;\n}\n',
  );
  check(
    "-Wall анхааруулга харагдана",
    warned.includes("Хөрвүүлэгчийн анхааруулга") && warned.includes("-Wuninitialized"),
    warned,
  );

  // --- Стандарт оролт ---------------------------------------------------------
  await openStdin("Бат\n20");
  const withInput = await run(SCANF);
  check("scanf оролтын мөрийг уншина", withInput.includes("Бат, 20 нас"), withInput);
  check("хариулт асуултын ард харагдана", withInput.includes("Нэрээ оруулна уу: Бат"), withInput);

  const callsBefore = compileCalls();
  await openStdin("Дорж\n31");
  const again = await run(SCANF);
  check(
    "зөвхөн оролт солиход дахин хөрвүүлэхгүй",
    compileCalls() === callsBefore && again.includes("Дорж, 31 нас"),
    `${callsBefore} → ${compileCalls()}: ${again}`,
  );

  await openStdin("");
  const noInput = await run(SCANF);
  check("оролт хоосон бол сануулга гарна", noInput.includes("«Оролт» хэсэгт мөр нэмээд"), noInput);

  // --- Ажиллах үеийн алдаа -----------------------------------------------------
  const crash = await run(
    '#include <stdio.h>\n\nint main(void) {\n    volatile int zero = 0;\n    printf("эхэлсэн\\n");\n    printf("%d\\n", 10 / zero);\n    return 0;\n}\n',
  );
  check("тэгд хуваалт ойлгомжтой алдаа өгнө", crash.includes("тэгд хуваалаа"), crash);
  check("алдаанаас өмнөх гаралт үлдэнэ", crash.includes("эхэлсэн"), crash);

  const exited = await run(
    '#include <stdio.h>\n\nint main(void) {\n    printf("гарлаа\\n");\n    return 3;\n}\n',
  );
  check("main-ийн буцаасан код харагдана", exited.includes("Програм 3 кодоор дууслаа"), exited);

  // --- Төгсгөлгүй давталт ------------------------------------------------------
  const hung = await run(
    '#include <stdio.h>\n\nint main(void) {\n    printf("давталт эхэллээ\\n");\n    for (;;) {\n    }\n}\n',
  );
  check("төгсгөлгүй давталт тасалдана", hung.includes("хэт удаан"), hung);
  check("тасрахаас өмнөх гаралт харагдана", hung.includes("давталт эхэллээ"), hung);

  const afterKill = await run(
    '#include <stdio.h>\n\nint main(void) {\n    printf("дахин ажиллалаа\\n");\n    return 0;\n}\n',
  );
  check("тасалсны дараа дахин ажиллана", afterKill.includes("дахин ажиллалаа"), afterKill);

  // --- C++ ------------------------------------------------------------------------
  await goto(page, CPP_LESSON, { waitFor: ".monaco-editor" });

  const caught = await run(
    [
      "#include <iostream>",
      "#include <stdexcept>",
      "#include <vector>",
      "",
      "int main() {",
      "    std::vector<int> toonuud{1, 2, 3};",
      "    try {",
      "        std::cout << toonuud.at(10) << std::endl;",
      "    } catch (const std::out_of_range &) {",
      '        std::cout << "exception барьлаа" << std::endl;',
      "    }",
      '    std::cout << "Нийт: " << toonuud.size() << std::endl;',
      "    return 0;",
      "}",
      "",
    ].join("\n"),
  );
  check(
    "C++ exception барьж ажиллана",
    caught.includes("exception барьлаа") && caught.includes("Нийт: 3"),
    caught,
  );

  const uncaught = await run(
    [
      "#include <iostream>",
      "#include <stdexcept>",
      "",
      "int main() {",
      '    std::cout << "шидэх гэж байна" << std::endl;',
      '    throw std::runtime_error("баригдаагүй алдаа");',
      "}",
      "",
    ].join("\n"),
  );
  check(
    "барьж аваагүй exception төрөл, мессежтэйгээ харагдана",
    uncaught.includes("шидэх гэж байна") &&
      uncaught.includes("std::runtime_error") &&
      uncaught.includes("баригдаагүй алдаа"),
    uncaught,
  );

  await openStdin("Бат Болд\n25");
  const cin = await run(
    [
      "#include <iostream>",
      "#include <string>",
      "",
      "int main() {",
      "    std::string ner;",
      "    int nas;",
      '    std::cout << "Нэр: ";',
      "    std::getline(std::cin, ner);",
      '    std::cout << "Нас: ";',
      "    std::cin >> nas;",
      '    std::cout << ner << " — " << nas << " нас" << std::endl;',
      "}",
      "",
    ].join("\n"),
  );
  check("cin ба getline оролтыг уншина", cin.includes("Бат Болд — 25 нас"), cin);

  // --- Console цэвэр ---------------------------------------------------------------
  // Хөрвүүлэлтийн алдаа нь 422 хариу — хөтөч үүнийг console-д бичдэг ч энэ нь
  // хүлээгдсэн зан төлөв.
  const realProblems = problems.filter(
    (entry) => !(entry.includes("Failed to load resource") && entry.includes("422")),
  );
  check("console цэвэр", realProblems.length === 0, realProblems.slice(0, 3).join(" | "));
} finally {
  await session.close();
}

process.exit(summary("Native (C/C++) sandbox") > 0 ? 1 : 0);
