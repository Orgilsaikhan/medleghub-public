/**
 * MySQL sandbox — кодыг серверийн тусгаарлагдсан MySQL дээр ажиллуулна.
 *
 * `apps/sql-runner` үйлчилгээ асаалттай, API-ийн `SQL_RUNNER_URL` түүн рүү
 * заасан байх ёстой. Энэ файл нь дараахыг батална:
 *
 *   • Хичээлийн анхны код алдаагүй ажиллана,
 *   • SELECT-ийн үр дүн кирилл тексттэй хүснэгт болж харагдана,
 *   • SQL алдаа код, SQLSTATE, мөрийн дугаартай харагдана,
 *   • Сурагчийн өөрчлөлт дараагийн ажиллагаанд үлдэхгүй,
 *   • DELIMITER-тэй процедур үүсч, CALL ажиллана,
 *   • Удаан асуулга тасалдаж, дараа нь дахин ажиллана,
 *   • Хуучин T-SQL хичээл (`limit-top-offset-fetch`) одоо MySQL дээр ажиллана —
 *     сургалт бүхэлдээ MySQL (2026-09-29).
 */

import { SEED, check, goto, login, newSession, setEditorValue, summary } from "./harness.mjs";

const MYSQL_LESSON = "/learn/mssql-mysql-undes/select-ba-from";
const LIMIT_LESSON = "/learn/mssql-mysql-undes/limit-top-offset-fetch";

/** Ажиллуулагчийн 10 секундийн хязгаар + сүлжээ. */
const RUN_TIMEOUT = 40_000;

const session = await newSession({ width: 1600, height: 1000 });
const { page, problems, requests } = session;

const runCalls = () => requests.filter((entry) => entry === "POST /api/v1/sql/run").length;

/** Кодыг ажиллуулаад console-ийн гаралтыг буцаана. `code` байхгүй бол анхны код. */
async function run(code, { timeout = RUN_TIMEOUT } = {}) {
  // Өмнөх гаралтыг арилгана. Товч идэвхгүй бол (гаралт байхгүй) алгасна.
  await page
    .locator('[aria-label="Console цэвэрлэх"]')
    .click({ timeout: 1500 })
    .catch(() => {});
  if (code !== undefined) await setEditorValue(page, code);
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
  await goto(page, MYSQL_LESSON, { waitFor: ".monaco-editor" });

  check(
    "MySQL хичээл дээр Ажиллуулах товч идэвхтэй",
    !(await page.getByRole("button", { name: "Код ажиллуулах" }).isDisabled()),
  );

  // --- Хичээлийн анхны код ------------------------------------------------------
  const initial = await run();
  check("анхны код сервер рүү илгээгдэнэ", runCalls() === 1, requests.join(", "));
  check("анхны код алдаагүй ажиллана", !initial.includes("ERROR"), initial);
  check("анхны код хүснэгт гаргана", initial.includes("+--") && initial.includes("мөр ("), initial);

  // --- Хүснэгт ------------------------------------------------------------------
  const table = await run(
    "USE delguur;\n\nSELECT baraa_id, ner, une\nFROM baraa\nWHERE baraa_id <= 3\nORDER BY baraa_id;\n",
  );
  check("баганын нэр хүснэгтийн толгойд", table.includes("| baraa_id | ner"), table);
  check("кирилл утга харагдана", table.includes("Ухаалаг утас") && table.includes("Чихэвч"), table);
  check("мөрийн тоо харагдана", table.includes("3 мөр"), table);

  // --- SQL алдаа ----------------------------------------------------------------
  const failed = await run(
    "USE delguur;\nSELECT * FROM baihgui_husnegt;\nSELECT 'ажиллах ёсгүй';\n",
  );
  check("алдааны код ба SQLSTATE", failed.includes("ERROR 1146 (42S02)"), failed);
  check("алдаатай мөрийн дугаар", failed.includes("2-р мөр"), failed);
  check("алдааны дараах statement ажиллахгүй", !failed.includes("ажиллах ёсгүй"), failed);

  // --- Өөрчлөлт үлдэхгүй --------------------------------------------------------
  const deleted = await run("DELETE FROM delguur.zahialgiin_mur;\n");
  check("DELETE нөлөөлсөн мөрийн тоог хэлнэ", deleted.includes("19 мөр өөрчлөгдлөө"), deleted);

  const restored = await run("SELECT COUNT(*) AS too FROM delguur.zahialgiin_mur;\n");
  check("дараагийн ажиллагаанд сан анхны төлөвтөө", /\|\s+19 \|/.test(restored), restored);

  // --- DELIMITER ба процедур ----------------------------------------------------
  const procedure = await run(
    [
      "USE delguur;",
      "",
      "DELIMITER $$",
      "CREATE PROCEDURE angilal_too(OUT p_too INT)",
      "BEGIN",
      "    SELECT COUNT(*) INTO p_too FROM angilal;",
      "END$$",
      "DELIMITER ;",
      "",
      "CALL angilal_too(@too);",
      "SELECT @too AS angilal_too;",
      "",
    ].join("\n"),
  );
  check(
    "DELIMITER-тэй процедур ажиллана",
    !procedure.includes("ERROR") && /\|\s+5 \|/.test(procedure),
    procedure,
  );

  // --- Хугацаа --------------------------------------------------------------------
  const slow = await run("SELECT 'эхэллээ' AS tuluv;\nSELECT SLEEP(30);\n");
  check("удаан асуулга тасалдана", slow.includes("хэт удаан ажиллаж зогсоогдлоо"), slow);
  check("тасрахаас өмнөх үр дүн үлдэнэ", slow.includes("эхэллээ"), slow);

  const afterKill = await run("SELECT 'дахин ажиллалаа' AS tuluv;\n");
  check("тасалсны дараа дахин ажиллана", afterKill.includes("дахин ажиллалаа"), afterKill);

  // --- Хуучин T-SQL хичээл — одоо MySQL ------------------------------------------------
  await goto(page, LIMIT_LESSON, { waitFor: ".monaco-editor" });
  check(
    "LIMIT хичээл дээр Ажиллуулах товч идэвхтэй",
    await page.getByRole("button", { name: "Код ажиллуулах" }).isEnabled(),
  );
  check("SSMS-ийн анхааруулга алга", (await page.getByText("SSMS эсвэл sqlcmd").count()) === 0);
  const limited = await run();
  check("LIMIT/OFFSET-тэй анхны код алдаагүй", !limited.includes("ERROR"), limited);

  check("console цэвэр", problems.length === 0, problems.slice(0, 3).join(" | "));
} finally {
  await session.close();
}

process.exit(summary("MySQL sandbox") > 0 ? 1 : 0);
