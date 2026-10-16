"""Модул 16-19 — Төгсгөлийн төслүүд.

Дөрвөн бүтэн хуудас. Модул 16-18-ийн анхны код нь нэг HTML файл бөгөөд
загварыг нь `<style>` дотор бичсэн. Модул 19 нь олон хуудастай сайт тул
бодит төсөл шиг `index.html`, хуваалцсан `style.css` (Модул 7), сурагчийн
бичих `uilchilgee.html` гэсэн файлуудтай (`common.py`).
"""

from app.content.html_css.common import files
from app.content.types import LessonSpec, ModuleSpec
from app.models.enums import LessonLanguage

HTML = LessonLanguage.HTML

PORTFOLIO = ModuleSpec(
    title="Модул 16 — Хувийн портфолио",
    description="Өөрийгөө танилцуулах бүтэн хуудас.",
    lessons=[
        LessonSpec(
            title="Төсөл — Хувийн портфолио",
            slug="huviin-portfolio",
            description="Баатар хэсэг, төслүүд, холбоо барих.",
            duration=900,
            language=HTML,
            content="""\
Модул 6-д бичсэн хувийн хуудсаа одоо CSS-ээр бүрэн гүйцээнэ.

### Юу багтаах вэ

| Хэсэг | Агуулга |
|---|---|
| Толгой | Нэр, навигаци |
| Баатар | Хэн бэ, юу хийдэг, холбоо барих товч |
| Тухай | Хоёр догол мөр |
| Ур чадвар | Шошгоны жагсаалт |
| Төслүүд | Карт сүлжээ |
| Холбоо барих | Имэйл, сүлжээ |

### Хэрэглэх зүйлс

- CSS хувьсагч (Модул 9)
- Grid сүлжээ `auto-fit`-тэй (Модул 13)
- `clamp()` уян хатан хэмжээ (Модул 14)
- `margin-top: auto` товч эгнүүлэх (Модул 15)

### Шошгоны жагсаалт

Ур чадварыг жагсаалтаар бич, CSS-ээр шошго болго:

```css
.chadvaruud {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  list-style: none;
  padding: 0;
}

.chadvaruud li {
  padding: 4px 12px;
  border-radius: 999px;
  background-color: var(--devsger-2);
  font-size: 0.875rem;
}
```

Семантик нь жагсаалт хэвээр — дэлгэц уншигч «зургаан зүйлтэй жагсаалт»
гэж хэлнэ.

### Даалгавар

1. Өөрийн мэдээллээр гүйцээ.
2. Төслийн карт нэмээд зураг оруул.
3. Харанхуй горим нэмээрэй.
4. Цонхыг 320px хүртэл нарийсгаад эвдрээгүйг шалга.
""",
            initial_code="""\
<!DOCTYPE html>
<html lang="mn">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Бат Болд — Вэб хөгжүүлэгч</title>
    <meta name="description" content="Бат Болдын портфолио." />

    <style>
      *,
      *::before,
      *::after {
        box-sizing: border-box;
      }

      :root {
        --undsen: #0f766e;
        --tekst: #1f2933;
        --buden: #616e7c;
        --huree: #e4e7eb;
        --devsger: #ffffff;
        --devsger-2: #f5f7fa;
      }

      body {
        margin: 0;
        font-family: system-ui, sans-serif;
        color: var(--tekst);
        background-color: var(--devsger);
        line-height: 1.6;
      }

      img {
        max-width: 100%;
        height: auto;
      }

      .sav {
        width: min(100% - 32px, 960px);
        margin-inline: auto;
      }

      .heseg {
        padding-block: clamp(40px, 9vw, 80px);
      }

      /* --- Толгой --- */
      .tolgoi {
        position: sticky;
        top: 0;
        z-index: 10;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 8px 24px;
        padding: 12px clamp(16px, 4vw, 32px);
        background-color: var(--devsger);
        border-bottom: 1px solid var(--huree);
      }

      .tolgoi nav ul {
        display: flex;
        flex-wrap: wrap;
        gap: 4px 8px;
        list-style: none;
        margin: 0;
        padding: 0;
      }

      .tolgoi nav a {
        display: inline-flex;
        align-items: center;
        min-height: 44px;
        padding-inline: 12px;
        color: inherit;
        text-decoration: none;
        border-radius: 6px;
      }

      .tolgoi nav a:hover {
        background-color: var(--devsger-2);
      }

      /* --- Баатар --- */
      .baatar {
        display: grid;
        gap: 16px;
        padding-block: clamp(48px, 11vw, 100px);
      }

      .baatar h1 {
        margin: 0;
        font-size: clamp(2rem, 5vw + 1rem, 3.25rem);
        line-height: 1.1;
      }

      .baatar p {
        margin: 0;
        max-width: 52ch;
        color: var(--buden);
        font-size: 1.125rem;
      }

      .tovch {
        display: inline-flex;
        align-items: center;
        min-height: 48px;
        padding-inline: 24px;
        border-radius: 8px;
        background-color: var(--undsen);
        color: white;
        font-weight: 600;
        text-decoration: none;
        justify-self: start;
      }

      /* --- Ур чадвар --- */
      .chadvaruud {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        list-style: none;
        margin: 0;
        padding: 0;
      }

      .chadvaruud li {
        padding: 4px 12px;
        border-radius: 999px;
        background-color: var(--devsger-2);
        font-size: 0.875rem;
      }

      /* --- Төслүүд --- */
      .tusluud {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
        gap: 20px;
      }

      .kart {
        display: flex;
        flex-direction: column;
        gap: 8px;
        padding: 16px;
        border: 1px solid var(--huree);
        border-radius: 10px;
      }

      .kart h3 {
        margin: 0;
      }

      .kart p {
        margin: 0;
        color: var(--buden);
      }

      .kart a {
        margin-top: auto;
        align-self: flex-start;
        color: var(--undsen);
      }

      .hul {
        padding: 24px 0;
        border-top: 1px solid var(--huree);
        color: var(--buden);
      }
    </style>
  </head>

  <body>
    <header class="tolgoi">
      <strong>Бат Болд</strong>
      <nav aria-label="Үндсэн цэс">
        <ul>
          <li><a href="#tuhai">Тухай</a></li>
          <li><a href="#chadvar">Ур чадвар</a></li>
          <li><a href="#tusul">Төслүүд</a></li>
          <li><a href="#holbogdoh">Холбогдох</a></li>
        </ul>
      </nav>
    </header>

    <main>
      <section class="baatar sav">
        <h1>Вэб хуудас бүтээдэг Бат байна</h1>
        <p>
          Би семантик HTML, цэвэр CSS ашиглан хурдан, хүртээмжтэй хуудас
          бүтээдэг. Одоогоор JavaScript сурч байна.
        </p>
        <a class="tovch" href="#holbogdoh">Холбоо барих</a>
      </section>

      <section class="heseg sav" id="tuhai">
        <h2>Миний тухай</h2>
        <p>
          2025 оноос хойш вэб хөгжүүлэлт сурч эхэлсэн. Хамгийн их сонирхдог
          зүйл маань хүртээмж — хуудас бүр бүх хэрэглэгчид ажиллах ёстой
          гэж боддог.
        </p>
      </section>

      <section class="heseg sav" id="chadvar">
        <h2>Ур чадвар</h2>
        <ul class="chadvaruud">
          <li>HTML</li>
          <li>CSS</li>
          <li>Flexbox</li>
          <li>Grid</li>
          <li>Хариуцлагатай дизайн</li>
          <li>Хүртээмж</li>
        </ul>
      </section>

      <section class="heseg sav" id="tusul">
        <h2>Төслүүд</h2>

        <div class="tusluud">
          <article class="kart">
            <h3>Гэрэл зургийн студи</h3>
            <p>Гурван хуудастай танилцуулга сайт. Grid ба Flexbox.</p>
            <a href="#">Үзэх</a>
          </article>

          <article class="kart">
            <h3>Бүтээгдэхүүний хуудас</h3>
            <p>Дэлгүүрийн нэг бүтээгдэхүүний дэлгэрэнгүй хуудас.</p>
            <a href="#">Үзэх</a>
          </article>

          <article class="kart">
            <h3>Нүүр хуудас</h3>
            <p>Уриалга бүхий бүтээгдэхүүн танилцуулах хуудас.</p>
            <a href="#">Үзэх</a>
          </article>
        </div>
      </section>

      <section class="heseg sav" id="holbogdoh">
        <h2>Холбоо барих</h2>
        <p><a href="mailto:bat@medleghub.mn">bat@medleghub.mn</a></p>
      </section>
    </main>

    <footer class="hul">
      <div class="sav"><p>&copy; 2026 Бат Болд</p></div>
    </footer>
  </body>
</html>
""",
        ),
    ],
)

LANDING = ModuleSpec(
    title="Модул 17 — Бүтээгдэхүүний нүүр хуудас",
    description="Уриалга бүхий борлуулалтын хуудас.",
    lessons=[
        LessonSpec(
            title="Төсөл — Бүтээгдэхүүний нүүр хуудас",
            slug="buteegdehuuniy-nuur-huudas",
            description="Баатар, боломж, үнэ, сэтгэгдэл, уриалга.",
            duration=900,
            language=HTML,
            content="""\
Бүтээгдэхүүн танилцуулж, хэрэглэгчийг нэг үйлдэл рүү чиглүүлэх хуудас.

### Хэсгүүдийн дараалал

1. **Баатар** — гол амлалт, уриалгын товч
2. **Боломжууд** — гурван давуу тал
3. **Үнэ** — хэдэн багц
4. **Сэтгэгдэл** — итгэл төрүүлэх
5. **Уриалга** — сүүлийн боломж
6. **Хөл** — холбоосууд

### Нэг уриалга

> Хуудасны **гол уриалга нэг** байх ёстой. Хэрэглэгчид зургаан сонголт
> өгвөл тэд нэгийг нь ч сонгохгүй.

Гол товчийг давтаж болно (дээр нэг, доор нэг) — гэхдээ ижил үйлдэл байх
ёстой.

### Үнийн хүснэгт

```css
.bagtsuud {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 20px;
  align-items: start;
}
```

`align-items: start` нь багцуудыг тэгшитгэхээс сэргийлнэ — онцлох багц
нь өндөр байж болно.

### Онцлох багцыг ялгаруулах

```css
.bagts-ontsloh {
  border-color: var(--undsen);
  border-width: 2px;
}
```

> Зөвхөн хүрээний өнгөөр бүү ялгаруул — өнгө ялгадаггүй хэрэглэгчид
> харагдахгүй. Шошго эсвэл текст нэм.

### Даалгавар

1. Дөрөв дэх боломж нэмээрэй.
2. Сэтгэгдлийн хэсэг нэмээрэй.
3. Асуулт хариултын хэсгийг `<details>` ашиглан бичээрэй.
""",
            initial_code="""\
<!DOCTYPE html>
<html lang="mn">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Sain Tems — Цагийн бүртгэл</title>
    <meta name="description" content="Багийн цагийн бүртгэлийг хялбар болгоно." />

    <style>
      *,
      *::before,
      *::after {
        box-sizing: border-box;
      }

      :root {
        --undsen: #0f766e;
        --tekst: #1f2933;
        --buden: #616e7c;
        --huree: #e4e7eb;
        --devsger-2: #f5f7fa;
      }

      body {
        margin: 0;
        font-family: system-ui, sans-serif;
        color: var(--tekst);
        line-height: 1.6;
      }

      .sav {
        width: min(100% - 32px, 1080px);
        margin-inline: auto;
      }

      .heseg {
        padding-block: clamp(48px, 10vw, 96px);
      }

      .heseg-sereg {
        background-color: var(--devsger-2);
      }

      .heseg h2 {
        font-size: clamp(1.5rem, 3vw + 0.6rem, 2.25rem);
        margin-top: 0;
      }

      /* --- Толгой --- */
      .tolgoi {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
        padding: 14px 0;
        border-bottom: 1px solid var(--huree);
      }

      /* --- Баатар --- */
      .baatar {
        display: grid;
        place-items: center;
        text-align: center;
        gap: 16px;
        padding-block: clamp(56px, 13vw, 120px);
      }

      .baatar h1 {
        margin: 0;
        max-width: 18ch;
        font-size: clamp(2rem, 5vw + 1rem, 3.5rem);
        line-height: 1.1;
      }

      .baatar p {
        margin: 0;
        max-width: 52ch;
        color: var(--buden);
        font-size: 1.125rem;
      }

      .tovchnuud {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        justify-content: center;
      }

      .tovch {
        display: inline-flex;
        align-items: center;
        min-height: 48px;
        padding-inline: 28px;
        border-radius: 8px;
        font-weight: 600;
        text-decoration: none;
      }

      .tovch-undsen {
        background-color: var(--undsen);
        color: white;
      }

      /* Хоёрдогч товч — зөвхөн хүрээтэй */
      .tovch-hoyordogch {
        border: 1px solid var(--undsen);
        color: var(--undsen);
      }

      /* --- Боломжууд --- */
      .bolomjuud {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 24px;
      }

      .bolomj h3 {
        margin: 0 0 6px;
      }

      .bolomj p {
        margin: 0;
        color: var(--buden);
      }

      /* --- Үнэ --- */
      .bagtsuud {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
        gap: 20px;
        align-items: start;
      }

      .bagts {
        display: flex;
        flex-direction: column;
        gap: 12px;
        padding: 24px;
        border: 1px solid var(--huree);
        border-radius: 12px;
        background-color: white;
      }

      /* Өнгөнөөс гадна ШОШГО-оор ч ялгаруулна */
      .bagts-ontsloh {
        border: 2px solid var(--undsen);
      }

      .shoshgo {
        align-self: flex-start;
        padding: 2px 10px;
        border-radius: 999px;
        background-color: var(--undsen);
        color: white;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
      }

      .une {
        font-size: 2rem;
        font-weight: 700;
      }

      .bagts ul {
        margin: 0;
        padding-left: 20px;
        color: var(--buden);
      }

      .bagts .tovch {
        margin-top: auto;
      }

      .hul {
        padding-block: 32px;
        border-top: 1px solid var(--huree);
        color: var(--buden);
      }
    </style>
  </head>

  <body>
    <header class="sav tolgoi">
      <strong>Sain Tems</strong>
      <a class="tovch tovch-undsen" href="#une">Эхлэх</a>
    </header>

    <main>
      <section class="baatar sav">
        <h1>Багийн цагийг нэг дороос хянана</h1>
        <p>
          Хэн юун дээр хэр удаж байгааг хормын дотор хар. Тохируулга
          шаардлагагүй.
        </p>
        <div class="tovchnuud">
          <a class="tovch tovch-undsen" href="#une">Үнэгүй эхлэх</a>
          <a class="tovch tovch-hoyordogch" href="#bolomj">Боломжуудыг үзэх</a>
        </div>
      </section>

      <section class="heseg heseg-sereg" id="bolomj">
        <div class="sav">
          <h2>Яагаад Sain Tems вэ</h2>

          <div class="bolomjuud">
            <article class="bolomj">
              <h3>Нэг товшилт</h3>
              <p>Цаг бүртгэх нь нэг товч дарахтай адил хялбар.</p>
            </article>

            <article class="bolomj">
              <h3>Тайлан автоматаар</h3>
              <p>Долоо хоног бүр имэйлээр хураангуй ирнэ.</p>
            </article>

            <article class="bolomj">
              <h3>Багийн харагдац</h3>
              <p>Хэн юун дээр ажиллаж байгааг нэг дэлгэцээс хар.</p>
            </article>
          </div>
        </div>
      </section>

      <section class="heseg" id="une">
        <div class="sav">
          <h2>Үнэ</h2>

          <div class="bagtsuud">
            <article class="bagts">
              <h3>Эхлэл</h3>
              <p class="une">Үнэгүй</p>
              <ul>
                <li>3 хүртэл хэрэглэгч</li>
                <li>Үндсэн тайлан</li>
              </ul>
              <a class="tovch tovch-hoyordogch" href="#">Сонгох</a>
            </article>

            <article class="bagts bagts-ontsloh">
              <span class="shoshgo">Хамгийн түгээмэл</span>
              <h3>Баг</h3>
              <p class="une">49,000₮</p>
              <ul>
                <li>20 хүртэл хэрэглэгч</li>
                <li>Дэлгэрэнгүй тайлан</li>
                <li>Имэйл хураангуй</li>
              </ul>
              <a class="tovch tovch-undsen" href="#">Сонгох</a>
            </article>

            <article class="bagts">
              <h3>Байгууллага</h3>
              <p class="une">149,000₮</p>
              <ul>
                <li>Хязгааргүй хэрэглэгч</li>
                <li>Тэргүүлэх дэмжлэг</li>
              </ul>
              <a class="tovch tovch-hoyordogch" href="#">Сонгох</a>
            </article>
          </div>
        </div>
      </section>
    </main>

    <footer class="hul">
      <div class="sav"><p>&copy; 2026 Sain Tems</p></div>
    </footer>
  </body>
</html>
""",
        ),
    ],
)

BLOG = ModuleSpec(
    title="Модул 18 — Энгийн блог",
    description="Нийтлэлийн жагсаалт ба нийтлэлийн хуудас.",
    lessons=[
        LessonSpec(
            title="Төсөл — Энгийн блог",
            slug="engiin-blog",
            description="Уншихад тав тухтай бичвэрийн загвар.",
            duration=900,
            language=HTML,
            content="""\
Блогийн гол зорилго нь **унших**. Тиймээс энэ төсөлд гоё харагдахаас
илүү уншигдац чухал.

### Уншигдацын гурван дүрэм

1. **Мөрийн урт** — 60-75 тэмдэгт (`max-width: 70ch`)
2. **Мөрийн өндөр** — 1.6-1.7
3. **Ялгарал** — текст ба дэвсгэрийн хооронд 4.5:1-ээс дээш

Эдгээрийг зөв тохируулбал энгийн хар цагаан хуудас ч сайхан уншигдана.

### Бичвэрийн хэмнэл

Элементүүдийн хоорондын зайг тууштай өг:

```css
.niitlel > * + * {
  margin-top: 1.2em;
}

.niitlel h2 {
  margin-top: 2em;
}
```

Эхний дүрэм нь «эхнийхээс бусад бүх шууд хүүхдэд дээш зай» гэсэн утгатай.
Элемент бүрт тусад нь margin бичих шаардлагагүй болно.

`em` ашигласан нь чухал — фонтын хэмжээтэй хамт зай нь өснө.

### Нийтлэлийн толгой

```html
<article>
  <header>
    <h1>Гарчиг</h1>
    <p>
      <time datetime="2026-09-13">2026 оны 9 сарын 13</time>
      · 5 минут
    </p>
  </header>
  …
</article>
```

`<time datetime="…">` нь машинд уншигдах огноо өгнө.

### Код ба эшлэл

```css
code {
  padding: 2px 6px;
  border-radius: 4px;
  background-color: var(--devsger-2);
  font-size: 0.9em;
}

blockquote {
  margin-inline: 0;
  padding-left: 16px;
  border-left: 3px solid var(--undsen);
  color: var(--buden);
}
```

### Даалгавар

1. Нийтлэлийн жагсаалтын хуудас нэмээрэй.
2. Шошгоны (tag) жагсаалт нэмээрэй.
3. Урт кодын блокт `overflow-x: auto` тавьж хэвтээ гүйлтээс сэргийлээрэй.
""",
            initial_code="""\
<!DOCTYPE html>
<html lang="mn">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Семантик HTML яагаад чухал вэ — Блог</title>

    <style>
      *,
      *::before,
      *::after {
        box-sizing: border-box;
      }

      :root {
        --undsen: #0f766e;
        --tekst: #1f2933;
        --buden: #616e7c;
        --huree: #e4e7eb;
        --devsger-2: #f5f7fa;
      }

      body {
        margin: 0;
        font-family: Georgia, "Times New Roman", serif;
        color: var(--tekst);
        /* Уншигдацад хамгийн их нөлөөтэй ганц шинж чанар */
        line-height: 1.7;
        font-size: 1.0625rem;
      }

      img {
        max-width: 100%;
        height: auto;
      }

      .sav {
        width: min(100% - 32px, 70ch);
        margin-inline: auto;
      }

      .tolgoi {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 16px;
        padding-block: 16px;
        border-bottom: 1px solid var(--huree);
        font-family: system-ui, sans-serif;
      }

      .tolgoi a {
        color: inherit;
        text-decoration: none;
      }

      .niitlel {
        padding-block: clamp(32px, 7vw, 64px);
      }

      .niitlel h1 {
        margin: 0;
        font-size: clamp(1.75rem, 4vw + 0.8rem, 2.75rem);
        line-height: 1.2;
      }

      .tsag {
        margin-top: 8px;
        color: var(--buden);
        font-family: system-ui, sans-serif;
        font-size: 0.9375rem;
      }

      /* «Эхнийхээс бусад бүх шууд хүүхдэд дээш зай».
         em ашигласан тул фонттой хамт зай нь өснө. */
      .niitlel > * + * {
        margin-top: 1.2em;
      }

      .niitlel h2 {
        margin-top: 2em;
        font-size: 1.5rem;
        line-height: 1.3;
      }

      code {
        padding: 2px 6px;
        border-radius: 4px;
        background-color: var(--devsger-2);
        font-family: "JetBrains Mono", Consolas, monospace;
        font-size: 0.9em;
      }

      pre {
        overflow-x: auto;
        padding: 16px;
        border-radius: 8px;
        background-color: var(--devsger-2);
      }

      pre code {
        padding: 0;
        background: none;
      }

      blockquote {
        margin-inline: 0;
        padding-left: 16px;
        border-left: 3px solid var(--undsen);
        color: var(--buden);
        font-style: italic;
      }

      a {
        color: var(--undsen);
      }

      .hul {
        padding-block: 24px;
        border-top: 1px solid var(--huree);
        color: var(--buden);
        font-family: system-ui, sans-serif;
        font-size: 0.9375rem;
      }
    </style>
  </head>

  <body>
    <header class="sav tolgoi">
      <a href="/"><strong>Батын блог</strong></a>
      <nav aria-label="Үндсэн цэс"><a href="/tuhai">Тухай</a></nav>
    </header>

    <main>
      <article class="sav niitlel">
        <header>
          <h1>Семантик HTML яагаад чухал вэ</h1>
          <p class="tsag">
            <time datetime="2026-09-13">2026 оны 9 сарын 13</time> · 5 минут
          </p>
        </header>

        <p>
          Вэб хуудас бичиж эхлэхэд бүх зүйлийг <code>&lt;div&gt;</code>-ээр
          шийдэх нь хялбар санагддаг. Гэвч энэ зуршил хожим үнэтэй тусдаг.
        </p>

        <h2>Хэн ялгааг мэдрэх вэ</h2>

        <p>
          Дэлгэц уншигч ашигладаг хэрэглэгч хуудсыг дээрээс доош сонсдоггүй.
          Тэд гарчгаас гарчиг руу үсэрч, навигацийг алгасдаг.
        </p>

        <blockquote>
          Утга нь тохирох элемент байвал түүнийг сонго. div-ийг зөвхөн
          загварчлалын зорилгоор ашигла.
        </blockquote>

        <h2>Жишээ</h2>

        <pre><code>&lt;header&gt;
  &lt;nav&gt;…&lt;/nav&gt;
&lt;/header&gt;
&lt;main&gt;…&lt;/main&gt;
&lt;footer&gt;…&lt;/footer&gt;</code></pre>

        <p>
          Энэ бүтэц нь нэмэлт ажил шаардахгүй бөгөөд хэнд ч хохиролгүй.
        </p>
      </article>
    </main>

    <footer class="hul">
      <div class="sav"><p>&copy; 2026 Батын блог</p></div>
    </footer>
  </body>
</html>
""",
        ),
    ],
)

MULTIPAGE = ModuleSpec(
    title="Модул 19 — Хариуцлагатай олон хуудаст сайт",
    description="Курсийн бүх зүйлийг нэгтгэсэн эцсийн төсөл.",
    lessons=[
        LessonSpec(
            title="Төсөл — Олон хуудаст сайт",
            slug="olon-huudast-sait",
            description="Хуваалцсан загвар, нийтлэг бүтэц, шалгах жагсаалт.",
            duration=960,
            language=HTML,
            content="""\
Эцсийн төсөл: гурваас доошгүй хуудастай, бүх дэлгэцэн дээр ажиллах сайт.

### Файлын бүтэц

```text
index.html
uilchilgee.html
holbogdoh.html
style.css          ← бүх хуудас хуваалцана
zurag/
```

Загварыг **нэг файлд** гарга. Хуудас бүрт `<style>` хуулах нь засварыг
олон дахин хийхэд хүргэнэ.

### Хуваалцсан бүтэц

Хуудас бүр ижил `<header>` ба `<footer>`-тэй. Энгийн HTML-д үүнийг хуулж
бичихээс өөр арга байхгүй. Гурван хуудсанд энэ нь тэвчихүйц; гуч болоход
загвар хөдөлгүүр хэрэгтэй болно.

### Одоогийн хуудсыг тэмдэглэ

```html
<a href="uilchilgee.html" aria-current="page">Үйлчилгээ</a>
```

```css
nav a[aria-current="page"] {
  color: var(--undsen);
  font-weight: 600;
}
```

### Хуудас бүр өөрийн гарчиг, тайлбартай

```html
<title>Үйлчилгээ — Гэрэл зургийн студи</title>
<meta name="description" content="Хурим, хөрөг, бүтээгдэхүүний зураг." />
```

Хуулж орхивол хайлтын үр дүнд бүх хуудас ижил харагдана.

### Дуусгахын өмнөх шалгах жагсаалт

| Шалгах зүйл | Хэрхэн |
|---|---|
| Хэвтээ гүйлт | Цонхыг 320px хүртэл нарийсга |
| Гарын навигаци | Tab дарж бүх холбоосоор дамж |
| Фокус харагдац | Tab дарахад хүрээ харагдаж байна уу |
| Ялгарал | DevTools-ийн өнгө сонгогч |
| Зургийн `alt` | Бүрд нь бий юу |
| Гарчгийн дараалал | h1 нэг, түвшин алгасаагүй |
| Хуудасны гарчиг | Хуудас бүрт өөр |
| Холбоос ажиллаж байна уу | Бүгд дээр дарж үз |

### Гүйцэтгэлийн богино зөвлөгөө

- Зургийг вэбэд тавихаас өмнө хэмжээг нь багасга
- `width` ба `height` зааж өгч агуулга үсрэхээс сэргийл
- Фонтыг хэт олон бүү ачаал — хоёр гэр бүл хангалттай

### Даалгавар

1. Доорх хуудсыг үндэслэн `uilchilgee.html` бичээрэй.
2. Холбоо барих хуудсанд форм нэмээрэй (Модул 5).
3. Харанхуй горим нэмээрэй.
4. Дээрх шалгах жагсаалтыг бүхэлд нь дамжуулаарай.
""",
            initial_code=files(
                (
                    "index.html",
                    """\
<!-- index.html — style.css-ийг бүх хуудас хуваалцана -->
<!DOCTYPE html>
<html lang="mn">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Нүүр — Гэрэл зургийн студи</title>
    <meta name="description" content="Улаанбаатар дахь гэрэл зургийн студи." />

    <!-- Загвар нь бүх хуудас хуваалцах style.css файлд -->
    <link rel="stylesheet" href="style.css" />
  </head>

  <body>
    <header class="tolgoi">
      <div class="sav">
        <strong>Гэрэл зургийн студи</strong>

        <nav aria-label="Үндсэн цэс">
          <ul>
            <li><a href="index.html" aria-current="page">Нүүр</a></li>
            <li><a href="uilchilgee.html">Үйлчилгээ</a></li>
            <li><a href="holbogdoh.html">Холбогдох</a></li>
          </ul>
        </nav>
      </div>
    </header>

    <main>
      <section class="baatar sav">
        <h1>Дурсгалт мөчийг тань хадгална</h1>
        <p>2019 оноос хойш Улаанбаатарт хурим, хөрөг, бүтээгдэхүүний зураг авч байна.</p>
        <a class="tovch" href="holbogdoh.html">Цаг захиалах</a>
      </section>

      <section class="heseg heseg-sereg">
        <div class="sav">
          <h2>Үйлчилгээ</h2>

          <div class="torhuud">
            <article class="torol">
              <h3>Хурим</h3>
              <p>Бүтэн өдрийн зураг авалт, засварласан 200 зураг.</p>
              <a href="uilchilgee.html">Дэлгэрэнгүй</a>
            </article>

            <article class="torol">
              <h3>Хөрөг</h3>
              <p>Студи эсвэл гадаа, нэг цагийн зураг авалт.</p>
              <a href="uilchilgee.html">Дэлгэрэнгүй</a>
            </article>

            <article class="torol">
              <h3>Бүтээгдэхүүн</h3>
              <p>Цагаан дэвсгэр дээрх дэлгүүрийн зураг.</p>
              <a href="uilchilgee.html">Дэлгэрэнгүй</a>
            </article>
          </div>
        </div>
      </section>
    </main>

    <footer class="hul">
      <div class="sav hul-torhuud">
        <p>&copy; 2026 Гэрэл зургийн студи</p>
        <p><a href="holbogdoh.html">Холбоо барих</a></p>
      </div>
    </footer>
  </body>
</html>
""",
                ),
                (
                    "style.css",
                    """\
/* style.css — index.html, uilchilgee.html, holbogdoh.html бүгд энэ нэг файлыг холбоно */

*,
*::before,
*::after {
  box-sizing: border-box;
}

:root {
  --undsen: #0f766e;
  --tekst: #1f2933;
  --buden: #616e7c;
  --huree: #e4e7eb;
  --devsger: #ffffff;
  --devsger-2: #f5f7fa;
}

@media (prefers-color-scheme: dark) {
  :root {
    --tekst: #e4e7eb;
    --buden: #9aa5b1;
    --huree: #323f4b;
    --devsger: #1f2933;
    --devsger-2: #243b53;
  }
}

body {
  margin: 0;
  min-height: 100dvh;
  display: grid;
  grid-template-rows: auto 1fr auto;
  font-family: system-ui, sans-serif;
  color: var(--tekst);
  background-color: var(--devsger);
  line-height: 1.6;
  overflow-wrap: break-word;
}

img {
  max-width: 100%;
  height: auto;
}

.sav {
  width: min(100% - 32px, 1080px);
  margin-inline: auto;
}

/* --- Толгой --- */
.tolgoi {
  border-bottom: 1px solid var(--huree);
}

.tolgoi .sav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px 24px;
  padding-block: 12px;
}

.tolgoi ul {
  display: flex;
  flex-wrap: wrap;
  gap: 4px 8px;
  list-style: none;
  margin: 0;
  padding: 0;
}

.tolgoi a {
  display: inline-flex;
  align-items: center;
  min-height: 44px;
  padding-inline: 12px;
  border-radius: 6px;
  color: inherit;
  text-decoration: none;
}

.tolgoi a:hover {
  background-color: var(--devsger-2);
}

.tolgoi a:focus-visible {
  outline: 2px solid var(--undsen);
  outline-offset: 2px;
}

/* Одоогийн хуудас — нэмэлт класс шаардлагагүй */
.tolgoi a[aria-current="page"] {
  color: var(--undsen);
  font-weight: 600;
}

/* --- Баатар --- */
.baatar {
  display: grid;
  gap: 16px;
  padding-block: clamp(48px, 11vw, 104px);
}

.baatar h1 {
  margin: 0;
  max-width: 20ch;
  font-size: clamp(2rem, 5vw + 1rem, 3.25rem);
  line-height: 1.1;
}

.baatar p {
  margin: 0;
  max-width: 52ch;
  color: var(--buden);
  font-size: 1.125rem;
}

.tovch {
  display: inline-flex;
  align-items: center;
  min-height: 48px;
  padding-inline: 26px;
  border-radius: 8px;
  background-color: var(--undsen);
  color: white;
  font-weight: 600;
  text-decoration: none;
  justify-self: start;
}

/* --- Хэсгүүд --- */
.heseg {
  padding-block: clamp(40px, 9vw, 80px);
}

.heseg-sereg {
  background-color: var(--devsger-2);
}

.torhuud {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
}

.torol {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 16px;
  border: 1px solid var(--huree);
  border-radius: 10px;
  background-color: var(--devsger);
}

.torol h3 {
  margin: 0;
}

.torol p {
  margin: 0;
  color: var(--buden);
}

.torol a {
  margin-top: auto;
  align-self: flex-start;
  color: var(--undsen);
}

/* --- Хөл --- */
.hul {
  padding-block: 28px;
  border-top: 1px solid var(--huree);
  color: var(--buden);
  font-size: 0.9375rem;
}

.hul-torhuud {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 20px;
}
""",
                ),
                (
                    "uilchilgee.html",
                    """\
<!-- uilchilgee.html — 1-р даалгавар: index.html-ийг үндэслэн «Үйлчилгээ» хуудсаа бичээрэй.
     Толгой, хөлийг хуулж, цэсний aria-current="page"-ийг энэ хуудасны холбоос руу шилжүүл.
     style.css-ийг холбосон тул загвар нь нүүр хуудастай ижил. -->
<!DOCTYPE html>
<html lang="mn">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Үйлчилгээ — Гэрэл зургийн студи</title>
    <link rel="stylesheet" href="style.css" />
  </head>

  <body>
    <main class="sav">
      <h1>Үйлчилгээ</h1>

      <p><a href="index.html">Нүүр хуудас руу буцах</a></p>
    </main>
  </body>
</html>
""",
                ),
            ),
        ),
    ],
)

PROJECT_MODULES = [PORTFOLIO, LANDING, BLOG, MULTIPAGE]
