/**
 * Код ажиллуулагчийн аюулгүй байдал (MVP §11, §21).
 *
 * Хэрэглэгчийн код нь sandbox-ын гаднах юунд ч хүрч болохгүй бөгөөд
 * төгсгөлгүй давталт хуудсыг зогсоож болохгүй.
 */

import {
  SEED,
  check,
  goto,
  login,
  newSession,
  runCode,
  setEditorCode,
  summary,
} from "./harness.mjs";

const session = await newSession();
const { page, problems } = session;

try {
  await login(page, SEED.student);
  await goto(page, `/learn/${SEED.course.slug}/tanilzuulga`, { waitFor: ".monaco-editor" });
  await page.waitForTimeout(1500);

  // --- Тусгаарлалт --------------------------------------------------------

  await setEditorCode(
    page,
    "console.log(typeof fetch, typeof XMLHttpRequest, typeof WebSocket, typeof importScripts);",
  );
  const network = await runCode(page);
  check(
    "сүлжээний API-ууд байхгүй",
    (network.match(/undefined/g) ?? []).length === 4,
    network,
  );

  await setEditorCode(
    page,
    "console.log(typeof document, typeof window, typeof localStorage, typeof indexedDB);",
  );
  const dom = await runCode(page);
  check("DOM болон хадгалалт байхгүй", (dom.match(/undefined/g) ?? []).length === 4, dom);

  await setEditorCode(page, "console.log(typeof self.navigator, typeof self.caches);");
  const misc = await runCode(page);
  check("navigator болон caches байхгүй", (misc.match(/undefined/g) ?? []).length === 2, misc);

  // --- Хугацааны хязгаар ---------------------------------------------------

  const before = Date.now();
  await setEditorCode(page, "while (true) {}");
  await page.getByRole("button", { name: "Код ажиллуулах" }).click();
  await page.waitForTimeout(5000);
  const timeoutText = await page.locator('[role="log"]').innerText();
  const elapsed = Date.now() - before;
  check("төгсгөлгүй давталт таслагдана", timeoutText.includes("хэт удаан"), timeoutText.trim());
  check("хязгаар нь 10 секундээс богино", elapsed < 10_000, `${elapsed}ms`);
  check("хуудас хариу үзүүлсээр байна", await page.locator("h1").isVisible());

  // Таслагдсаны дараа дахин ажиллуулах боломжтой хэвээр.
  await setEditorCode(page, "console.log('дахин ажиллаж байна');");
  const afterTimeout = await runCode(page);
  check("timeout-ийн дараа дахин ажиллана", afterTimeout.includes("дахин"), afterTimeout);

  // --- Алдаа боловсруулалт -------------------------------------------------

  await setEditorCode(page, "const = ;");
  const syntax = await runCode(page);
  check("syntax алдаа харагдана", syntax.includes("SyntaxError"), syntax);

  await setEditorCode(page, "throw new Error('миний алдаа');");
  const thrown = await runCode(page);
  check("шидсэн алдаа харагдана", thrown.includes("миний алдаа"), thrown);

  await setEditorCode(page, "console.warn('сэрэмжлүүлэг'); console.error('алдаа');");
  const levels = await runCode(page);
  check("warn болон error харагдана", levels.includes("сэрэмжлүүлэг") && levels.includes("алдаа"));

  // --- Хэрэглээний чанар ---------------------------------------------------

  await setEditorCode(page, "const o = {}; o.self = o; console.log(o);");
  const circular = await runCode(page);
  check("мөчлөгт бүтэц console-ыг унагаахгүй", circular.includes("Circular"), circular);

  await setEditorCode(page, "for (let i = 0; i < 3000; i++) console.log(i);");
  const flood = await runCode(page);
  check("хэт олон мөр таслагдана", flood.includes("таслав"), flood.slice(-80));

  await setEditorCode(
    page,
    "await new Promise((r) => setTimeout(r, 10));\nconsole.log('top-level await ажиллана');",
  );
  const topLevelAwait = await runCode(page);
  check("top-level await дэмжигдэнэ", topLevelAwait.includes("ажиллана"), topLevelAwait);

  await setEditorCode(page, "console.log('Монгол үсэг: өүяёжшч');");
  const unicode = await runCode(page);
  check("кирилл үсэг зөв харагдана", unicode.includes("өүяёжшч"), unicode);

  check("console цэвэр", problems.length === 0, problems.slice(0, 3).join(" | "));
} finally {
  await session.close();
}

process.exit(summary("Sandbox") > 0 ? 1 : 0);
