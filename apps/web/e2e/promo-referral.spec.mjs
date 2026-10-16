/**
 * Промо код ба найзаа урих.
 *
 *   • Админ `/admin/promo` дээр seed-ийн HELLOWORLD2026-г харж, үнэгүй сарын
 *     код үүсгэж, засаж, идэвхгүй болгоод буцааж идэвхжүүлнэ,
 *   • Хэрэглэгч профайл дээрээ урилгын холбоосоо авна,
 *   • Найз `/register?ref=…`-ээр бүртгүүлэхэд код бөглөгдсөн байна; буруу код алдаа өгнө,
 *   • Урилгаар бүртгүүлсэн найз `/pricing` дээр 10% хөнгөлөлттэй; HELLOWORLD2026 оруулбал
 *     30% биш 20%; буруу код алдаа; үнэгүй сарын код багцыг шууд сунгана,
 *   • Хэрэглэгчийн цэсэнд урилгын код харагдаж, дарахад хуулагдана,
 *   • Урьсан хүн хөнгөлөлтгүй, профайл дээр 1 найз, 0 багц авсан.
 *
 * Checkout (Wire) дарахгүй — жинхэнэ төлбөрийг `tests/test_promo_codes.py`,
 * `tests/test_referrals.py` хамарна.
 */

import { BASE_URL, SEED, check, goto, login, logout, newSession, summary } from "./harness.mjs";

const session = await newSession({ width: 1280, height: 1000 });
const { page, problems } = session;

const stamp = Date.now().toString(36).toUpperCase();
const giftCode = `GIFT${stamp}`;
const friendEmail = `e2e-naiz-${Date.now()}@suralts.mn`;

async function fillRegister(name, email) {
  await page.fill("#name", name);
  await page.fill("#email", email);
  await page.fill("#password", "Nuuts12345");
  await page.getByLabel("Би 16 нас хүрсэн").check();
  await page.locator("#accept_terms").check();
}

/** Админы жагсаалтын нэг код (toast ч бас `li` тул хэсгээр хязгаарлана). */
function promoItem(code) {
  return page.locator('section[aria-labelledby="promo-list-title"] li', { hasText: code });
}

/** Standard картын «Нийт» мөр. */
async function totalLine() {
  return page.locator("p[aria-live=polite]", { hasText: "Нийт" }).innerText();
}

try {
  // --- Админ ------------------------------------------------------------------------
  await login(page, SEED.admin);
  await goto(page, "/admin/promo");
  await page.getByRole("heading", { name: "Промо кодууд" }).waitFor({ timeout: 20_000 });
  const seeded = promoItem("HELLOWORLD2026");
  check("seed-ийн HELLOWORLD2026 жагсаалтад", (await seeded.count()) === 1);
  check("HELLOWORLD2026 — 20% хөнгөлөлт", (await seeded.innerText()).includes("20% хөнгөлөлт"));

  await page.fill("#promo-code", giftCode.toLowerCase());
  await page.getByLabel("Үнэгүй сар", { exact: true }).check();
  await page.fill("#promo-months", "2");
  await page.fill("#promo-expires", "2027-06-30");
  await page.fill("#promo-max-uses", "1");
  await page.getByRole("button", { name: "Код үүсгэх" }).click();
  await page
    .locator("[data-sonner-toast]", { hasText: `${giftCode} код үүслээ.` })
    .waitFor({ timeout: 10_000 });
  const gift = promoItem(giftCode);
  const giftText = await gift.innerText();
  check("шинэ код томоор хадгалагдав", giftText.includes(giftCode));
  check(
    "үнэгүй сар ба дээд тоо харагдана",
    giftText.includes("2 сар үнэгүй") && giftText.includes("0 / 1 ашигласан"),
  );

  await gift.getByRole("button", { name: "Засах" }).click();
  const dialog = page.getByRole("dialog");
  check(
    "засах цонх өдрийг бөглөсөн",
    (await dialog.locator("#promo-edit-expires").inputValue()) === "2027-06-30",
  );
  await dialog.locator("#promo-edit-max-uses").fill("5");
  await dialog.getByRole("button", { name: "Хадгалах" }).click();
  await dialog.waitFor({ state: "hidden", timeout: 10_000 });
  check("дээд тоо шинэчлэгдэв", (await gift.innerText()).includes("0 / 5 ашигласан"));

  await gift.getByRole("button", { name: "Идэвхгүй болгох" }).click();
  await gift.getByText("Идэвхгүй", { exact: true }).waitFor({ timeout: 10_000 });
  check("идэвхгүй болов", true);
  await gift.getByRole("button", { name: "Идэвхжүүлэх" }).click();
  await gift.getByText("Идэвхтэй", { exact: true }).waitFor({ timeout: 10_000 });
  check("буцаж идэвхжэв", true);
  await logout(page);

  // --- Урьсан хүн ----------------------------------------------------------------------
  const referrerEmail = `e2e-urigch-${Date.now()}@suralts.mn`;
  await goto(page, "/register");
  await fillRegister("Урьсан Хүн", referrerEmail);
  await page.getByRole("button", { name: "Бүртгүүлэх" }).click();
  await page.waitForURL("**/dashboard", { timeout: 25_000 });

  await goto(page, "/profile");
  await page.getByRole("heading", { name: "Найзаа урь" }).waitFor({ timeout: 20_000 });
  const link = await page.getByLabel("Урилгын холбоос").inputValue();
  const referralCode = new URL(link).searchParams.get("ref");
  check("урилгын холбоос /register?ref=…", link.startsWith(`${BASE_URL}/register?ref=`), link);
  check("8 тэмдэгт код", /^[A-Z2-9]{8}$/.test(referralCode ?? ""), referralCode ?? "");
  check(
    "эзний бичсэн дүрэм харагдана",
    (await page.locator("section[aria-labelledby=referral-title]").innerText()).includes(
      "Таны урьсан найзуудаас 3 нь багц авах бүрд танд 1 сар үнэгүй бэлэглэнэ.",
    ),
  );
  await logout(page);

  // --- Найз бүртгүүлнэ ---------------------------------------------------------------------
  await goto(page, "/register?ref=NOTACODE");
  await fillRegister("Найз", friendEmail);
  check(
    "холбоосын код бөглөгдсөн",
    (await page.locator("#referral_code").inputValue()) === "NOTACODE",
  );
  await page.getByRole("button", { name: "Бүртгүүлэх" }).click();
  await page.locator("#referral_code-error").waitFor({ timeout: 10_000 });
  check(
    "буруу урилгын код алдаа өгнө",
    (await page.locator("#referral_code-error").innerText()).includes("Урилгын код олдсонгүй"),
  );

  await goto(page, `/register?ref=${referralCode}`);
  await fillRegister("Найз", friendEmail);
  check("зөв код бөглөгдсөн", (await page.locator("#referral_code").inputValue()) === referralCode);
  await page.getByRole("button", { name: "Бүртгүүлэх" }).click();
  await page.waitForURL("**/dashboard", { timeout: 25_000 });
  check("найз урилгын кодоор бүртгүүлэв", true);

  // --- Найзын 10%, промо код /pricing дээр ------------------------------------------------
  await goto(page, "/pricing");
  await page
    .getByText("Найзын урилгаар бүртгүүлсэн тул 10% хөнгөлөлт энэ төлбөрт автоматаар орно.")
    .waitFor({ timeout: 15_000 });
  const friendTotal = await totalLine();
  check(
    "урилгаар бүртгүүлсэн найз 10% хөнгөлөлттэй: 22,410₮",
    friendTotal.includes("22,410₮") && friendTotal.includes("10% хөнгөлөлт"),
    friendTotal,
  );

  await page.getByRole("button", { name: "Промо код байна уу?" }).click();
  const promoInput = page.getByLabel("Промо код", { exact: true });
  const focused = await page
    .waitForFunction(
      () => document.activeElement?.getAttribute("placeholder") === "HELLOWORLD2026",
      null,
      {
        timeout: 3_000,
      },
    )
    .then(() => true)
    .catch(() => false);
  check("промо кодын талбар фокустай", focused);
  await promoInput.fill("wrongcode");
  await page.getByRole("button", { name: "Хэрэглэх" }).click();
  await page
    .getByRole("alert")
    .filter({ hasText: "Промо код буруу байна." })
    .waitFor({ timeout: 10_000 });
  check("буруу промо код алдаа өгнө", true);

  await promoInput.fill("helloworld2026");
  await page.getByRole("button", { name: "Хэрэглэх" }).click();
  await page.getByText("HELLOWORLD2026 — 20% хөнгөлөлт хэрэглэгдлээ.").waitFor({ timeout: 10_000 });
  const discounted = await totalLine();
  check(
    "1 сар 20% хөнгөлөлттэй: 19,920₮",
    discounted.includes("19,920₮") && discounted.includes("24,900₮"),
    discounted,
  );
  check(
    "промо ба урилга нийлж 30% болохгүй",
    discounted.includes("20% хөнгөлөлт") && !discounted.includes("17,430₮"),
    discounted,
  );
  check(
    "урилгын 10% дараагийн төлбөрт хадгалагдана гэж хэлнэ",
    (await page
      .getByText("Хөнгөлөлт нийлэхгүй — урилгын 10% хөнгөлөлт тань дараагийн төлбөрт хадгалагдана.")
      .count()) === 1,
  );

  await page.getByRole("button", { name: "Цуцлах" }).click();
  check("цуцлахад урилгын 10% буцаж орно", (await totalLine()).includes("22,410₮"));

  // Цуцалсны дараа талбар нээлттэй хэвээр — өөр код оруулж болно.
  await page.getByLabel("Промо код", { exact: true }).fill(giftCode);
  await page.getByRole("button", { name: "Хэрэглэх" }).click();
  await page.getByRole("button", { name: "2 сар үнэгүй идэвхжүүлэх" }).click();
  // Идэвхжүүлмэгц баримт хэвлэгч рүү (`/billing/success?redemption=…`).
  await page.waitForURL(/\/billing\/success\?redemption=/, { timeout: 15_000 });
  await page.locator('section[data-stage="complete"]').waitFor({ timeout: 15_000 });
  check(
    "үнэгүй сарын код багцыг идэвхжүүлж, баримт хэвлэнэ",
    (await page.locator("article").innerText()).includes(`Промо код ${giftCode}`),
  );

  // --- Хэрэглэгчийн цэсэнд урилгын код ------------------------------------------------------
  await page
    .context()
    .grantPermissions(["clipboard-read", "clipboard-write"], { origin: BASE_URL });
  await page.getByRole("button", { name: "Цэс" }).click();
  const codeItem = page.getByRole("menuitem", { name: /^Урилгын код [A-Z2-9]{8} — хуулах$/ });
  await codeItem.waitFor({ timeout: 10_000 });
  const menuText = await codeItem.innerText();
  const friendCode = menuText.match(/[A-Z2-9]{8}/)?.[0] ?? "";
  check("цэсэнд урилгын код харагдана", friendCode.length === 8, menuText.replace(/\s+/g, " "));
  await codeItem.click();
  await page
    .locator("[data-sonner-toast]", { hasText: "Урилгын код хуулагдлаа." })
    .waitFor({ timeout: 10_000 });
  const clipboard = await page.evaluate(() => navigator.clipboard.readText());
  check("код хуулагдав", clipboard === friendCode, clipboard);
  check("хуулсны дараа цэс нээлттэй", await codeItem.isVisible());
  await page.keyboard.press("Escape");
  await logout(page);

  // --- Урьсан хүн хөнгөлөлт авахгүй -----------------------------------------------------------
  await login(page, { email: referrerEmail, password: "Nuuts12345" });
  await goto(page, "/pricing");
  await page.getByRole("button", { name: "Промо код байна уу?" }).waitFor({ timeout: 15_000 });
  const referrerTotal = await totalLine();
  check(
    "урьсан хүн бүтэн үнээр: 24,900₮",
    referrerTotal.includes("24,900₮") &&
      !referrerTotal.includes("22,410₮") &&
      (await page.getByText("Найзын урилгаар бүртгүүлсэн тул").count()) === 0,
    referrerTotal,
  );

  await goto(page, "/profile");
  const card = page.locator("section[aria-labelledby=referral-title]");
  await card.waitFor({ timeout: 20_000 });
  const stat = async (label) =>
    (
      await card
        .locator("dl > div", { has: page.locator("dt", { hasText: label }) })
        .locator("dd")
        .innerText()
    ).trim();
  check(
    "профайл: 1 найз, 0 багц авсан, 0 сар",
    (await stat("Урьсан найз")) === "1" &&
      (await stat("Багц авсан найз")) === "0" &&
      (await stat("Бэлэглэсэн сар")) === "0",
  );
  check(
    "дараагийн үнэгүй сар хүртэл 3 найз",
    (await card.innerText()).includes("Дахиад 3 найз багц авбал танд 1 сар үнэгүй нэмэгдэнэ."),
  );

  // Буруу код, буруу урилгын кодын 400 нь хүлээгдсэн хариу.
  const unexpected = problems.filter((problem) => !problem.includes("400"));
  check("консолд алдаагүй", unexpected.length === 0, unexpected.join(" | "));
} catch (error) {
  check("тест бүрэн ажиллав", false, String(error));
} finally {
  await session.close();
}

process.exit(summary("promo-referral") > 0 ? 1 : 0);
