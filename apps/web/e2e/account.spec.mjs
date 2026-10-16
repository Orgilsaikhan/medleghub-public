/**
 * Тохиргоо — профайлын зураг, нууц үг солих.
 *
 * Шинэ хэрэглэгч зураг оруулж (толгойн цэс болон профайлд харагдах), устгаад,
 * нууц үгээ солино. Дараа нь хуучин нууц үгээр нэвтрэх боломжгүй, шинээр
 * нэвтэрнэ.
 */

import zlib from "node:zlib";

import { check, goto, login, logout, newSession, registerNew, summary } from "./harness.mjs";

const NEW_PASSWORD = "Shine12345";

/** 300×300 улбар шар PNG — хамааралгүйгээр гараар үүсгэнэ. */
function orangePng(size = 300) {
  const crcTable = Array.from({ length: 256 }, (_, n) => {
    let c = n;
    for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    return c >>> 0;
  });
  const crc = (buffer) => {
    let c = 0xffffffff;
    for (const byte of buffer) c = crcTable[(c ^ byte) & 0xff] ^ (c >>> 8);
    return (c ^ 0xffffffff) >>> 0;
  };
  const chunk = (type, data) => {
    const body = Buffer.concat([Buffer.from(type), data]);
    const length = Buffer.alloc(4);
    length.writeUInt32BE(data.length);
    const sum = Buffer.alloc(4);
    sum.writeUInt32BE(crc(body));
    return Buffer.concat([length, body, sum]);
  };
  const header = Buffer.alloc(13);
  header.writeUInt32BE(size, 0);
  header.writeUInt32BE(size, 4);
  header[8] = 8; // bit depth
  header[9] = 2; // RGB
  const row = Buffer.concat([Buffer.from([0]), Buffer.alloc(size * 3, Buffer.from([255, 153, 0]))]);
  const pixels = zlib.deflateSync(Buffer.concat(Array.from({ length: size }, () => row)));
  return Buffer.concat([
    Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]),
    chunk("IHDR", header),
    chunk("IDAT", pixels),
    chunk("IEND", Buffer.alloc(0)),
  ]);
}

const session = await newSession();
const { page, problems } = session;

try {
  const account = await registerNew(page, "Зурагтай Хэрэглэгч");

  // --- Профайлын зураг -----------------------------------------------------
  await goto(page, "/settings");
  await page.getByRole("heading", { name: "Профайлын зураг" }).waitFor();

  await page.locator("#avatar-file").setInputFiles({
    name: "avatar.png",
    mimeType: "image/png",
    buffer: orangePng(),
  });
  await page.getByText("Профайлын зураг шинэчлэгдлээ.").waitFor({ timeout: 20_000 });

  const headerImage = page.locator("header img[src*='/avatar?v=']");
  await headerImage.waitFor({ timeout: 20_000 });
  const size = await headerImage.evaluate((img) => [img.naturalWidth, img.naturalHeight]);
  check("толгойн цэсэнд зураг харагдана (256×256)", size[0] === 256 && size[1] === 256, `${size}`);

  await goto(page, "/profile");
  await page.locator("main img[src*='/avatar?v=']").waitFor({ timeout: 20_000 });
  check("профайл хуудсанд зураг харагдана", true);

  await goto(page, "/settings");
  await page.getByRole("button", { name: "Зураг устгах" }).click();
  await page.getByText("Профайлын зураг устгагдлаа.").waitFor({ timeout: 20_000 });
  check(
    "устгасны дараа толгойд зураг байхгүй",
    (await page.locator("header img[src*='/avatar?v=']").count()) === 0,
  );

  // --- Нууц үг солих ---------------------------------------------------------
  await page.fill("#current_password", "Buruu12345");
  await page.fill("#new_password", NEW_PASSWORD);
  await page.fill("#confirm_password", NEW_PASSWORD);
  await page.getByRole("button", { name: "Нууц үг солих" }).click();
  await page.getByText("Одоогийн нууц үг буруу байна.").waitFor({ timeout: 20_000 });
  check("буруу одоогийн нууц үг талбар дээр алдаа харуулна", true);

  await page.fill("#current_password", account.password);
  await page.getByRole("button", { name: "Нууц үг солих" }).click();
  await page.getByText("Нууц үг солигдлоо.").waitFor({ timeout: 20_000 });
  check("нууц үг солигдлоо", true);
  check(
    "солисны дараа нэвтэрсэн хэвээр",
    (await page.getByRole("button", { name: "Цэс" }).count()) === 1,
  );

  await logout(page);
  await goto(page, "/login");
  await page.fill("#email", account.email);
  await page.fill("#password", account.password);
  await page.getByRole("button", { name: "Нэвтрэх" }).click();
  await page.getByText("Имэйл эсвэл нууц үг буруу байна.").waitFor({ timeout: 20_000 });
  check("хуучин нууц үгээр нэвтрэхгүй", true);

  await login(page, { email: account.email, password: NEW_PASSWORD });
  check("шинэ нууц үгээр нэвтэрнэ", page.url().includes("/dashboard"));

  // Буруу нууц үгийн 400, 401 нь санаатай.
  const unexpected = problems.filter((line) => !/\b(400|401)\b/.test(line));
  check("console цэвэр", unexpected.length === 0, unexpected.slice(0, 3).join(" | "));
} finally {
  await session.close();
}

process.exit(summary("Account settings") > 0 ? 1 : 0);
