/**
 * `node --test worker/` (npm run test:worker).
 *
 * Гарын үсгийн жишээ нь `apps/api/tests/test_client_ip.py`-тай ИЖИЛ — Worker,
 * API хоёр зөрвөл хоёулаа унана.
 */

import assert from "node:assert/strict";
import { test } from "node:test";

import {
  CLIENT_IP_HEADER,
  CLIENT_IP_SIGNATURE_HEADER,
  signClientIp,
  withSignedClientIp,
} from "./client-ip.mjs";

const SECRET = "s".repeat(40);
const NOW_MS = 1_790_000_000_500;

test("signature matches the API", async () => {
  const secret = "medleghub-test-vector-secret";
  assert.equal(
    await signClientIp(secret, "203.0.113.7", 1790000000),
    "t=1790000000,v1=e80954e099859c48d4f2333580fb37f57ff75bb0e08a3532a7447a554cf9ca92",
  );
  assert.equal(
    await signClientIp(secret, "2001:db8::1", 1790000000),
    "t=1790000000,v1=4835ee01277d71b73aec401340292d5ce8e26b21fd183dd6681b66be98430a1e",
  );
});

test("API requests carry the signed visitor IP", async () => {
  const request = new Request("https://medleghub.com/api/v1/auth/login", {
    method: "POST",
    headers: { "cf-connecting-ip": "203.0.113.7", "content-type": "application/json" },
    body: JSON.stringify({ email: "a@b.mn" }),
  });
  const signed = await withSignedClientIp(request, SECRET, NOW_MS);

  assert.equal(signed.headers.get(CLIENT_IP_HEADER), "203.0.113.7");
  assert.equal(
    signed.headers.get(CLIENT_IP_SIGNATURE_HEADER),
    await signClientIp(SECRET, "203.0.113.7", 1_790_000_000),
  );
  // Хүсэлтийн бусад хэсэг хэвээр.
  assert.equal(signed.method, "POST");
  assert.equal(signed.headers.get("content-type"), "application/json");
  assert.deepEqual(await signed.json(), { email: "a@b.mn" });
});

test("a visitor cannot pass their own IP headers through", async () => {
  const forged = {
    "cf-connecting-ip": "203.0.113.7",
    [CLIENT_IP_HEADER]: "192.0.2.1",
    [CLIENT_IP_SIGNATURE_HEADER]: "t=1,v1=00",
  };
  // API зам: Cloudflare-ийн IP-гаар дарж бичнэ.
  const api = await withSignedClientIp(
    new Request("https://medleghub.com/api/v1/auth/password/forgot", { headers: forged }),
    SECRET,
    NOW_MS,
  );
  assert.equal(api.headers.get(CLIENT_IP_HEADER), "203.0.113.7");
  assert.notEqual(api.headers.get(CLIENT_IP_SIGNATURE_HEADER), "t=1,v1=00");

  // Бусад зам, эсвэл нууцгүй үед: хаяна.
  for (const [url, secret] of [
    ["https://medleghub.com/courses", SECRET],
    ["https://medleghub.com/api/v1/auth/login", undefined],
  ]) {
    const stripped = await withSignedClientIp(new Request(url, { headers: forged }), secret);
    assert.equal(stripped.headers.has(CLIENT_IP_HEADER), false, url);
    assert.equal(stripped.headers.has(CLIENT_IP_SIGNATURE_HEADER), false, url);
  }
});

test("only /api/v1 is signed; other requests pass through untouched", async () => {
  const headers = { "cf-connecting-ip": "203.0.113.7" };
  for (const path of ["/", "/courses/c-cpp-undes", "/api/v10/x", "/_next/static/a.js"]) {
    const request = new Request(`https://medleghub.com${path}`, { headers });
    assert.equal(await withSignedClientIp(request, SECRET, NOW_MS), request, path);
  }
  const bare = await withSignedClientIp(
    new Request("https://medleghub.com/api/v1", { headers }),
    SECRET,
    NOW_MS,
  );
  assert.equal(bare.headers.get(CLIENT_IP_HEADER), "203.0.113.7");
});

test("without CF-Connecting-IP nothing is signed", async () => {
  const request = new Request("https://medleghub.com/api/v1/courses");
  assert.equal(await withSignedClientIp(request, SECRET, NOW_MS), request);
});
