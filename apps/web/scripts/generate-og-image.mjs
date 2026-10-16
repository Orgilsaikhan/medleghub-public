/**
 * Сошиал сүлжээнд хуваалцахад харагдах зураг — `public/og.png` (1200×630).
 *
 *   npm run og:image
 *
 * Facebook, Messenger, LinkedIn, X, Discord бүгд 1200×630 (1.91:1)-ийг бүтнээр
 * нь харуулна. Брэнд нь сайтын толгой, имэйлийн загвартай ижил: хар дэвсгэр,
 * «Medleg» цагаан, «hub» улбар шар (#ff9900). Текстийг өөрчилбөл дахин
 * ажиллуулаад үүссэн PNG-ийг commit хийнэ. Фонт Google Fonts-оос (сүлжээ хэрэгтэй).
 */

import { chromium } from "playwright";

const OUTPUT = new URL("../public/og.png", import.meta.url).pathname;

const LANGUAGES = ["C", "C++", "Python", "JavaScript", "HTML/CSS", "SQL", "Git"];

const html = `<!doctype html>
<html lang="mn">
<head>
<meta charset="utf-8" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=JetBrains+Mono:wght@400;600&display=block&subset=cyrillic" rel="stylesheet" />
<style>
  * { box-sizing: border-box; margin: 0; }
  body {
    width: 1200px; height: 630px; overflow: hidden;
    font-family: Inter, sans-serif; color: #fafafa;
    background:
      radial-gradient(circle at 88% 12%, rgba(255,153,0,.22), transparent 42%),
      radial-gradient(circle at 8% 100%, rgba(255,153,0,.10), transparent 38%),
      #0b0b0b;
    display: flex; padding: 64px 72px; gap: 56px;
  }
  .left { flex: 1; display: flex; flex-direction: column; }
  .logo { display: inline-flex; align-items: center; gap: 4px; background: #000;
          border: 1px solid #262626; border-radius: 12px; padding: 10px 14px 10px 18px;
          font-size: 34px; font-weight: 800; letter-spacing: -1px; align-self: flex-start; }
  .logo .hub { background: #ff9900; color: #000; border-radius: 8px; padding: 0 9px 2px; }
  h1 { margin-top: 44px; font-size: 62px; line-height: 1.08; font-weight: 800; letter-spacing: -2px; }
  p { margin-top: 20px; font-size: 25px; line-height: 1.45; color: #a3a3a3; max-width: 560px; }
  .langs { margin-top: auto; display: flex; flex-wrap: wrap; gap: 10px; }
  .langs span { font-size: 19px; font-weight: 600; padding: 7px 14px; border-radius: 999px;
                border: 1px solid #333; color: #e5e5e5; background: #141414; }
  .right { width: 420px; display: flex; flex-direction: column; justify-content: center; gap: 16px; }
  .editor { border: 1px solid #2a2a2a; border-radius: 16px; background: #111; overflow: hidden;
            box-shadow: 0 30px 80px rgba(0,0,0,.55); }
  .bar { display: flex; gap: 8px; padding: 14px 16px; border-bottom: 1px solid #222; }
  .bar i { width: 12px; height: 12px; border-radius: 50%; background: #333; display: block; }
  .bar i:first-child { background: #ff9900; }
  pre { font-family: "JetBrains Mono", monospace; font-size: 19px; line-height: 1.6; padding: 20px 22px; color: #d4d4d4; }
  .k { color: #ff9900; } .s { color: #86efac; } .c { color: #737373; }
  .out { border: 1px solid #2a2a2a; border-radius: 12px; background: #0f0f0f; padding: 14px 18px;
         font-family: "JetBrains Mono", monospace; font-size: 18px; color: #86efac; }
  .out b { color: #737373; font-weight: 400; margin-right: 10px; }
  .url { font-size: 22px; font-weight: 600; color: #ff9900; text-align: right; }
</style>
</head>
<body>
  <div class="left">
    <div class="logo">Medleg<span class="hub">hub</span></div>
    <h1>Монгол хэлээр<br />код бичиж сур.</h1>
    <p>Хичээлээ үзэж, кодоо хөтөч дотроо шууд бичиж, ажиллуулж сурна.</p>
    <div class="langs">${LANGUAGES.map((name) => `<span>${name}</span>`).join("")}</div>
  </div>
  <div class="right">
    <div class="editor">
      <div class="bar"><i></i><i></i><i></i></div>
<pre><span class="k">#include</span> &lt;stdio.h&gt;

<span class="k">int</span> main() {
    printf(<span class="s">"Сайн уу!\\n"</span>);
    <span class="k">return</span> 0;
}</pre>
    </div>
    <div class="out"><b>$</b>Сайн уу!</div>
    <div class="url">medleghub.com</div>
  </div>
</body>
</html>`;

const browser = await chromium.launch();
try {
  const page = await browser.newPage({ viewport: { width: 1200, height: 630 } });
  await page.setContent(html, { waitUntil: "networkidle" });
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: OUTPUT, type: "png" });
  console.log(`og-image: ${OUTPUT}`);
} finally {
  await browser.close();
}
