/**
 * IndexNow — Bing, Yandex, Naver, Seznam-д шинэ/өөрчлөгдсөн хуудсыг шууд мэдэгдэнэ.
 * Google IndexNow дэмждэггүй: түүнд Search Console-оор sitemap илгээнэ.
 *
 *   npm run indexnow                                   # sitemap-ийн бүх URL
 *   npm run indexnow -- https://medleghub.com/courses/x   # зөвхөн эдгээр
 *
 * Түлхүүр нь нууц биш — `public/<түлхүүр>.txt` дээр нийтэд харагдах ёстой.
 * Deploy хийсний ДАРАА ажиллуулна (түлхүүрийн файл сайт дээр байх ёстой).
 */

const HOST = "medleghub.com";
const KEY = "597002c4862d817b4fb6b55d11b448a1";

async function sitemapUrls() {
  const response = await fetch(`https://${HOST}/sitemap.xml`);
  if (!response.ok) throw new Error(`sitemap.xml: ${response.status}`);
  return [...(await response.text()).matchAll(/<loc>([^<]+)<\/loc>/g)].map((match) => match[1]);
}

const urls = process.argv.length > 2 ? process.argv.slice(2) : await sitemapUrls();
const response = await fetch("https://api.indexnow.org/indexnow", {
  method: "POST",
  headers: { "content-type": "application/json; charset=utf-8" },
  body: JSON.stringify({
    host: HOST,
    key: KEY,
    keyLocation: `https://${HOST}/${KEY}.txt`,
    urlList: urls,
  }),
});
// 200/202 — хүлээж авсан. 403 — түлхүүрийн файл сайт дээр алга (deploy хийсэн үү?).
console.log(`IndexNow: ${response.status} — ${urls.length} URL`);
process.exit(response.ok ? 0 : 1);
