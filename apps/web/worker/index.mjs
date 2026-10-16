/**
 * Cloudflare Worker-ийн оролт (`wrangler.jsonc` → `main`).
 *
 * OpenNext-ийн үүсгэсэн worker-ийг (`npm run cf:build` → `.open-next/worker.js`)
 * ороож, `/api/v1` хүсэлтэд зочны гарын үсэгтэй IP-г нэмнэ — API-ийн rate limit
 * Cloudflare-ийн нэг IP биш, зочин тус бүрээр тоолно (`client-ip.mjs`).
 */

import openNext from "../.open-next/worker.js";
import { withSignedClientIp } from "./client-ip.mjs";

// OpenNext-ийн Durable Object классууд (ашиглавал binding-д хэрэгтэй).
export * from "../.open-next/worker.js";

const worker = {
  /**
   * @param {Request} request
   * @param {{ CLIENT_IP_SECRET?: string }} env
   * @param {unknown} ctx
   */
  async fetch(request, env, ctx) {
    return openNext.fetch(await withSignedClientIp(request, env.CLIENT_IP_SECRET), env, ctx);
  },
};

export default worker;
