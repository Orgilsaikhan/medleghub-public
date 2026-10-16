/**
 * Зочны жинхэнэ IP-г API-д гарын үсэгтэйгээр дамжуулна (rate limit-д).
 *
 * `/api/v1/*`-ийг OpenNext нь api.medleghub.com руу fetch-ээр proxy хийж, ирсэн
 * толгойг бүгдийг нь дамжуулдаг — зөвхөн `cf-connecting-ip`-г хасна
 * (@opennextjs/aws `overrides/proxyExternalRequest/fetch`). Caddy нь
 * X-Forwarded-For-ыг TCP хаягаар (Cloudflare) солидог. Тиймээс энд Cloudflare-ийн
 * тавьсан `CF-Connecting-IP`-г (хэрэглэгч хуурамчаар бичиж чадахгүй) өөрийн
 * толгойд хуулж, HMAC-аар гарын үсэг зурна.
 *
 * api.medleghub.com-д шууд хандах боломжтой тул API нь гарын үсгийг заавал
 * шалгана (`apps/api/app/core/rate_limit.py`). Нууц нь сүлжээгээр дамждаггүй.
 */

export const CLIENT_IP_HEADER = "x-medleghub-client-ip";
export const CLIENT_IP_SIGNATURE_HEADER = "x-medleghub-client-ip-signature";

const encoder = new TextEncoder();

/** @type {{ secret: string, key: Promise<CryptoKey> } | undefined} */
let cachedKey;

/** @param {string} secret */
function hmacKey(secret) {
  if (cachedKey?.secret !== secret) {
    const key = crypto.subtle.importKey(
      "raw",
      encoder.encode(secret),
      { name: "HMAC", hash: "SHA-256" },
      false,
      ["sign"],
    );
    cachedKey = { secret, key };
  }
  return cachedKey.key;
}

/**
 * `t=<unix>,v1=<hex(HMAC_SHA256(secret, "<t>.<ip>"))>` — API-ийн `sign_client_ip`-тэй ижил.
 *
 * @param {string} secret
 * @param {string} ip
 * @param {number} timestamp Unix секунд.
 */
export async function signClientIp(secret, ip, timestamp) {
  const mac = await crypto.subtle.sign(
    "HMAC",
    await hmacKey(secret),
    encoder.encode(`${timestamp}.${ip}`),
  );
  const hex = Array.from(new Uint8Array(mac), (byte) => byte.toString(16).padStart(2, "0")).join(
    "",
  );
  return `t=${timestamp},v1=${hex}`;
}

/** @param {string} pathname */
function isApiPath(pathname) {
  return pathname === "/api/v1" || pathname.startsWith("/api/v1/");
}

/**
 * `/api/v1` хүсэлтэд гарын үсэгтэй зочны IP нэмнэ. Хэрэглэгчийн илгээсэн ижил
 * нэртэй толгойг үргэлж хаяна. Өөрчлөх зүйлгүй бол анхны хүсэлтийг буцаана.
 *
 * @param {Request} request
 * @param {string | undefined} secret Worker-ийн `CLIENT_IP_SECRET`.
 * @param {number} [now] Миллисекунд — тестэд.
 * @returns {Promise<Request>}
 */
export async function withSignedClientIp(request, secret, now = Date.now()) {
  const ip = request.headers.get("cf-connecting-ip");
  const sign = Boolean(secret && ip && isApiPath(new URL(request.url).pathname));
  const forged =
    request.headers.has(CLIENT_IP_HEADER) || request.headers.has(CLIENT_IP_SIGNATURE_HEADER);
  if (!sign && !forged) return request;

  const headers = new Headers(request.headers);
  headers.delete(CLIENT_IP_HEADER);
  headers.delete(CLIENT_IP_SIGNATURE_HEADER);
  if (sign && secret && ip) {
    headers.set(CLIENT_IP_HEADER, ip);
    headers.set(CLIENT_IP_SIGNATURE_HEADER, await signClientIp(secret, ip, Math.floor(now / 1000)));
  }
  return new Request(request, { headers });
}
