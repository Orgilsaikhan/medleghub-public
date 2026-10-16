"""Модул 7-9 — CSS-ийн үндэс, сонгогч, өнгө ба текст.

Хуудсыг гоёж эхэлнэ. Анхны код нь гадаад загварын файл (`style.css`)
хэлбэртэй — Модул 7-д үзсэнээр энэ бол зөвлөж буй арга.
"""

from app.content.html_css.common import css_page, files
from app.content.types import LessonSpec, ModuleSpec
from app.models.enums import LessonLanguage

CSS = LessonLanguage.CSS
HTML = LessonLanguage.HTML

CSS_BASICS = ModuleSpec(
    title="Модул 7 — CSS-ийн үндэс",
    description="Загварын хэлний синтакс ба холбох аргууд.",
    lessons=[
        LessonSpec(
            title="CSS гэж юу вэ",
            slug="css-gej-yu-ve",
            description="Дүрмийн бүтэц: сонгогч, шинж чанар, утга.",
            duration=400,
            language=CSS,
            content="""\
**CSS** (Cascading Style Sheets) нь HTML элементүүд ямар харагдахыг
тодорхойлно.

### Дүрмийн бүтэц

```css
h1 {
  color: teal;
  font-size: 32px;
}
```

```text
h1 {                      ← сонгогч: юунд хэрэглэх вэ
  color: teal;            ← шинж чанар: утга;
  font-size: 32px;
}
```

Нэр томьёо:

| Хэсэг | Нэр |
|---|---|
| `h1` | Сонгогч (selector) |
| `color` | Шинж чанар (property) |
| `teal` | Утга (value) |
| `color: teal;` | Зарлалт (declaration) |
| Бүхэлдээ | Дүрэм (rule) |

Зарлалт бүрийн төгсгөлд **цэг таслал** тавина. Сүүлийнхийг нь орхиж
болох ч үргэлж бичих нь дараа нь мөр нэмэхэд алдаанаас сэргийлнэ.

### Каскад — нэрийн учир

«Cascading» гэдэг нь дүрмүүд **дараалан урсаж**, доорхи нь дээрхийг
дарж бичихийг хэлнэ:

```css
p {
  color: gray;
}
p {
  color: black;  /* энэ хүчинтэй */
}
```

Ижил хүчтэй хоёр дүрэм байвал **сүүлчийнх** ялна.

### Өв залгамжлал

Зарим шинж чанар хүүхэд элементэд **өвлөгдөнө**:

```css
body {
  font-family: sans-serif;
  color: navy;
}
```

Энэ хоёр нь `body` доторх бүх элементэд дамжина. Тиймээс фонт, өнгийг
`body`-д нэг удаа тавьбал хангалттай.

Хэмжээ, хүрээ, дэвсгэр зэрэг нь **өвлөгддөггүй**.

### Тайлбар

```css
/* Энэ бол CSS тайлбар */
```

CSS-д зөвхөн энэ хэлбэр бий. HTML-ийн `<!-- -->` энд ажиллахгүй.

### Нэгжүүд

| Нэгж | Утга |
|---|---|
| `px` | Пиксел — тогтмол |
| `rem` | Үндсэн фонтын хэмжээний дахин |
| `em` | Эцгийн фонтын хэмжээний дахин |
| `%` | Эцгийн хэмжээний хувь |

Текстийн хэмжээнд `rem` ашиглах нь дээр — хэрэглэгч хөтчийнхөө фонтын
хэмжээг томруулсан бол дагаж томорно.
""",
            initial_code=css_page(
                title="CSS гэж юу вэ",
                body="""\
<h1>CSS-ийн дүрэм</h1>
<p>
  CSS нь HTML элементүүд ямар харагдахыг тодорхойлно. Дүрэм бүр сонгогч,
  шинж чанар, утгаас бүрдэнэ.
</p>
<p>
  Каскад: <code>p</code>-д хоёр дүрэм бий. Сүүлчийнх нь ялсан тул энэ
  догол мөр саарал биш, бараан өнгөтэй.
</p>
<ul>
  <li>Энэ жагсаалтад фонт, өнгө заагаагүй.</li>
  <li>Гэвч <code>body</code>-д тавьсныг өвлөсөн тул ижил харагдана.</li>
</ul>
<blockquote>
  <p>Хүрээ, дэвсгэр өвлөгддөггүй — энэ ишлэлд тэдгээрийг шууд тавьсан.</p>
</blockquote>
""",
                css="""\
/* style.css — дүрмийн бүтцийг ажиглаарай */

/* body-д тавьсан фонт, өнгө нь бүх хүүхдэд ӨВЛӨГДӨНӨ */
body {
  font-family: system-ui, sans-serif;
  color: #1f2933;
  line-height: 1.6;
}

h1 {
  color: teal;
  font-size: 2rem;
}

/* Каскад: ижил хүчтэй хоёр дүрмээс СҮҮЛЧИЙНХ нь ялна */
p {
  color: gray;
}

p {
  color: #1f2933;
}

/* Хүрээ, дэвсгэр нь өвлөгддөггүй — заавал өөрт нь тавина.
   border-left — зүүн талын хүрээ, padding-left — хүрээний дотор талын зай,
   background-color — дэвсгэр өнгө (Модул 9–10-д нарийн үзнэ) */
blockquote {
  border-left: 4px solid teal;
  padding-left: 16px;
  background-color: #f5f7fa;
}
""",
            ),
        ),
        LessonSpec(
            title="CSS-ийг холбох гурван арга",
            slug="css-holboh-gurvan-arga",
            description="Inline, internal, external. Аль нь хэзээ.",
            duration=400,
            language=HTML,
            content="""\
### 1. Гадаад (external) — зөвлөж байна

```html
<head>
  <link rel="stylesheet" href="style.css" />
</head>
```

| Давуу тал | Тайлбар |
|---|---|
| Дахин ашиглалт | Нэг файлыг бүх хуудас хуваалцана |
| Cache | Хөтөч нэг л удаа татна |
| Цэгцтэй | Бүтэц ба загвар тусдаа |

Бараг үргэлж энэ аргыг сонго.

### 2. Дотоод (internal)

```html
<head>
  <style>
    h1 {
      color: teal;
    }
  </style>
</head>
```

Ганц хуудсанд л хамаарах загварт тохиромжтой. Мөн жижиг туршилтад
хурдан.

### 3. Мөрийн (inline)

```html
<h1 style="color: teal;">Гарчиг</h1>
```

| Асуудал | Тайлбар |
|---|---|
| Дахин ашиглах боломжгүй | Элемент бүрт дахин бичнэ |
| Дарж бичихэд хэцүү | Хамгийн өндөр хүчтэй |
| Кодыг бохирдуулна | HTML уншихад хэцүү болно |

Зөвхөн JavaScript-ээр динамикаар өөрчлөх үед, эсвэл имэйлийн загварт
ашигла.

### Аль нь ялах вэ

Ижил шинж чанарыг гурвуулаа заасан бол:

```text
inline  >  internal ба external  >  хөтчийн анхдагч
```

`internal` ба `external` хоёрын хооронд **аль нь сүүлд бичигдсэн** нь
ялна. Тиймээс `<link>`-ийн дараа `<style>` бичвэл `<style>` ялна.

### `!important`

```css
p {
  color: red !important;
}
```

Бүгдийг дарж бичнэ. **Бараг хэзээ ч бүү ашигла** — нэг удаа ашиглавал
дараа нь түүнийг дарахын тулд дахин `!important` бичих шаардлагатай
болж, цааш нь гинж үүснэ.

### Хэдэн файл вэ

Эхлээд нэг `style.css` хангалттай. Том болоход хуваана:

```html
<link rel="stylesheet" href="suuri.css" />
<link rel="stylesheet" href="huudas.css" />
```

Дараалал чухал — сүүлчийнх нь дарж бичнэ.
""",
            initial_code=files(
                (
                    "index.html",
                    """\
<!DOCTYPE html>
<html lang="mn">
  <head>
    <meta charset="UTF-8" />
    <title>CSS холбох гурван арга</title>

    <!-- 1. Гадаад — зөвлөж буй арга -->
    <link rel="stylesheet" href="style.css" />

    <!-- 2. Дотоод — зөвхөн энэ хуудсанд -->
    <style>
      h1 {
        color: teal;
      }
      p {
        color: gray;
      }
    </style>
  </head>

  <body>
    <h1>Гарчиг</h1>

    <p>Энэ догол мөр дотоод загвараас саарал өнгөтэй.</p>

    <!-- 3. Мөрийн — хамгийн өндөр хүчтэй тул дотоод дүрмийг дарна -->
    <p style="color: crimson;">Энэ нь улаан — мөрийн загвар бүгдийг дарна.</p>

    <p>Мөрийн загварыг зөвхөн онцгой тохиолдолд ашиглана.</p>
  </body>
</html>
""",
                ),
                (
                    "style.css",
                    """\
/* style.css — гадаад загвар. index.html-ийн <link> мөр үүнийг холбоно. */

/* Холбосон хуудас бүрт үйлчилнэ */
body {
  font-family: system-ui, sans-serif;
  line-height: 1.6;
}

/* index.html-ийн <style> нь <link>-ийн ДАРАА бичигдсэн тул
   гарчиг navy биш teal болно — сүүлд бичигдсэн нь ялна */
h1 {
  color: navy;
}
""",
                ),
            ),
        ),
    ],
)

SELECTORS = ModuleSpec(
    title="Модул 8 — Сонгогч (Selectors)",
    description="Аль элементэд загвар хэрэглэхээ заах.",
    lessons=[
        LessonSpec(
            title="Элемент, класс, id сонгогч",
            slug="element-class-id-songogch",
            description="Гурван үндсэн сонгогч.",
            duration=400,
            language=CSS,
            content="""\
### Элемент сонгогч

Тухайн нэртэй **бүх** элементэд хэрэглэнэ:

```css
p {
  line-height: 1.6;
}
```

Суурь загвар тавихад тохиромжтой.

### Класс сонгогч

Цэгээр эхэлнэ. Хамгийн их хэрэглэгддэг:

```css
.tovch {
  color: teal;
}
```

```html
<button class="tovch">Хадгалах</button>
<a class="tovch" href="/">Нүүр</a>
```

Ижил класс олон элементэд, олон класс нэг элементэд байж болно.

### Id сонгогч

Тэмдэгтээр (`#`) эхэлнэ:

```css
#undsen-tses {
  font-size: 1.25rem;
}
```

**Зөвлөдөггүй**. Хүч нь хэт өндөр тул дараа нь дарж бичихэд хэцүү. Мөн
хуудсанд нэг л удаа тохиолдох тул дахин ашиглах боломжгүй.

> Дүрэм: загварт **класс** ашигла. `id`-г зөвхөн холбоос болон
> шошгонд үлдээ.

### Бүгдийг сонгох

```css
* {
  box-sizing: border-box;
}
```

Энэ нэг дүрмийг бараг бүх төсөл эхэндээ бичдэг (Модул 10).

### Хэд хэдэн сонгогчид нэг дүрэм

Таслалаар тусгаарлана:

```css
h1,
h2,
h3 {
  font-family: Georgia, serif;
}
```

### Хуурамч ангилал (pseudo-class)

Элементийн **төлөвийг** сонгоно:

```css
a:hover {
  text-decoration: underline;
}

button:focus-visible {
  outline: 2px solid teal;
}

li:first-child {
  font-weight: bold;
}
```

`:focus-visible` нь гарын товчоор шилжсэн үед л харагдана — хулганаар
дарахад биш. Фокусын хүрээг **хэзээ ч бүү устга**, эс бөгөөс гар
ашигладаг хэрэглэгч хаана байгаагаа мэдэхгүй болно.
""",
            initial_code=css_page(
                title="Элемент, класс, id",
                body="""\
<h1>Сонгогчид</h1>
<p>Элемент сонгогч нь тухайн нэртэй бүх элементэд хэрэглэгдэнэ.</p>

<h2>Класс сонгогч</h2>
<p>Ижил класс олон элементэд, олон класс нэг элементэд байж болно.</p>
<p>
  <button class="tovch tovch-undsen" type="button">Хадгалах</button>
  <button class="tovch" type="button">Цуцлах</button>
  <a class="tovch" href="#tuluv">Төлөв рүү очих</a>
</p>

<h2 id="tuluv">Хуурамч ангилал</h2>
<h3>Туршиж үзээрэй</h3>
<ul>
  <li>Эхний мөр тод — <code>li:first-child</code></li>
  <li>Товч дээр хулганаа аваачаарай.</li>
  <li>Tab дарж товчнуудын хооронд шилжээд фокусын хүрээг хараарай.</li>
</ul>
""",
                css="""\
/* Элемент сонгогч — суурь загварт */
body {
  font-family: system-ui, sans-serif;
  line-height: 1.6;
}

p {
  margin-block: 12px;
}

/* Класс сонгогч — хамгийн түгээмэл.
   display, padding, border нь холбоосыг товч шиг харагдуулна —
   Модул 10–11-д нарийн үзнэ. Одоо сонгогчид анхаар. */
.tovch {
  display: inline-block;
  padding: 8px 16px;
  border: 1px solid teal;
  border-radius: 6px;
  color: teal;
  text-decoration: none;
}

.tovch-undsen {
  background-color: teal;
  color: white;
}

/* Хэд хэдэн сонгогчид нэг дүрэм */
h1,
h2,
h3 {
  font-family: Georgia, serif;
  color: #102a43;
}

/* Хуурамч ангилал — төлөв. color-ийг давтана: үгүй бол «tovch-undsen»-ий
   цагаан текст цайвар дэвсгэр дээр харагдахгүй болно. */
.tovch:hover {
  background-color: #e0f2f1;
  color: teal;
}

/* Гараар шилжихэд л харагдана. Фокусын хүрээг бүү устга. */
.tovch:focus-visible {
  outline: 2px solid teal;
  outline-offset: 2px;
}

li:first-child {
  font-weight: bold;
}
""",
            ),
        ),
        LessonSpec(
            title="Шинж чанарын сонгогч ба нэгтгэх",
            slug="shinj-chanariin-songogch",
            description="Атрибутаар сонгох, сонгогчдыг хослуулах.",
            duration=420,
            language=CSS,
            content="""\
### Шинж чанарын сонгогч

Дөрвөлжин хаалтанд бичнэ:

```css
[disabled] {
  opacity: 0.5;
}

input[type="email"] {
  border-color: teal;
}

a[href^="https"] {
  color: green;
}

a[href$=".pdf"]::after {
  content: " (PDF)";
}
```

| Хэлбэр | Утга |
|---|---|
| `[ner]` | Шинж чанар байна |
| `[ner="utga"]` | Яг тэнцүү |
| `[ner^="utga"]` | Ингэж эхэлнэ |
| `[ner$="utga"]` | Ингэж төгсөнө |
| `[ner*="utga"]` | Агуулна |

### Сонгогч нэгтгэх

| Бичлэг | Утга | Жишээ |
|---|---|---|
| `A B` | A **доторх** бүх B | `nav a` |
| `A > B` | A-ийн **шууд** хүүхэд B | `ul > li` |
| `A + B` | A-ийн **дараах** B | `h2 + p` |
| `A ~ B` | A-ийн дараах **бүх** B | `h2 ~ p` |
| `A.b` | A бөгөөд b класстай | `button.undsen` |

```css
/* nav ДОТОРХ бүх холбоос — хэдэн ч давхар гүнзгий байсан */
nav a {
  text-decoration: none;
}

/* ul-ийн ШУУД хүүхэд li — үүрлэсэн жагсаалтад хамаарахгүй */
ul > li {
  margin-block: 4px;
}

/* Гарчгийн ДАРАА шууд ирэх догол мөр */
h2 + p {
  font-size: 1.1rem;
}
```

### Хэт гүн бүү ор

```css
/* Муу — эмзэг, удаан, дарж бичихэд хэцүү */
body div.aguulga ul li a span {
  color: red;
}

/* Сайн */
.tses-holboos {
  color: red;
}
```

HTML-ийн бүтэц өөрчлөгдөхөд эхний дүрэм чимээгүй ажиллахаа болино.
Класс нэрлэх нь эрүүл.

### `:not()` ба `:is()`

```css
/* Сүүлчийнхээс бусад бүх li */
li:not(:last-child) {
  border-bottom: 1px solid #e4e7eb;
}

/* Гурван сонгогчийг товчлох */
:is(h1, h2, h3) + p {
  margin-top: 4px;
}
```
""",
            initial_code=css_page(
                title="Сонгогч нэгтгэх",
                body="""\
<header>
  <h1>Сонгогч нэгтгэх</h1>
  <nav aria-label="Үндсэн цэс">
    <ul class="tses">
      <li><a href="#burtgel">Бүртгэл</a></li>
      <li><a href="#material">Материал</a></li>
      <li>
        <a href="#material">Сургалт</a>
        <ul>
          <li><a href="#material">HTML</a></li>
          <li><a href="#material">CSS</a></li>
        </ul>
      </li>
    </ul>
  </nav>
</header>

<main>
  <h2 id="burtgel">Бүртгүүлэх</h2>
  <p>Гарчгийн дараа шууд ирсэн догол мөр томоор харагдана.</p>
  <p>Энэ догол мөр гарчгийн шууд дараа биш тул энгийн хэвээр.</p>
  <form>
    <p>
      <label for="email">Имэйл</label>
      <input id="email" type="email" name="email" />
    </p>
    <p>
      <label for="nuuts-ug">Нууц үг</label>
      <input id="nuuts-ug" type="password" name="nuuts-ug" />
    </p>
    <button type="submit" disabled>Илгээх</button>
  </form>

  <h2 id="material">Материал</h2>
  <p>Холбоосын төгсгөлийн тэмдгийг CSS өөрөө нэмнэ.</p>
  <ul class="jagsaalt">
    <li><a href="https://developer.mozilla.org">MDN — CSS-ийн гарын авлага</a></li>
    <li><a href="tailan.pdf" download>Хичээлийн тайлан</a></li>
    <li><a href="#burtgel">Бүртгэл рүү буцах</a></li>
  </ul>
</main>
""",
                css="""\
/* Энэ хичээлийн гол нь СОНГОГЧ. opacity, cursor, padding, border, margin,
   display зэрэг шинж чанарыг Модул 10–11-д нарийн үзнэ. */

/* Шинж чанарын сонгогч */
[disabled] {
  opacity: 0.5;
  cursor: not-allowed;
}

input[type="email"],
input[type="password"] {
  border: 1px solid #9aa5b1;
  padding: 8px;
}

/* Гадаад холбоосыг ялгаж харуулна */
a[href^="https"]::after {
  content: " ↗";
}

/* PDF холбоосыг тэмдэглэнэ */
a[href$=".pdf"]::after {
  content: " (PDF)";
}

/* --- Нэгтгэх --- */

/* nav ДОТОРХ бүх холбоос */
nav a {
  text-decoration: none;
  color: #102a43;
}

/* ul-ийн ШУУД хүүхэд — үүрлэсэн жагсаалтад хамаарахгүй */
.tses > li {
  display: inline-block;
  margin-right: 16px;
}

/* Гарчгийн дараа ШУУД ирэх догол мөр */
h2 + p {
  font-size: 1.1rem;
  color: #486581;
}

/* Сүүлчийнхээс бусад бүгд */
.jagsaalt li:not(:last-child) {
  border-bottom: 1px solid #e4e7eb;
}
""",
            ),
        ),
        LessonSpec(
            title="Тодорхойлол ба каскад",
            slug="todorhoilol-ba-kaskad",
            description="Хоёр дүрэм зөрчилдвөл аль нь ялах вэ.",
            duration=420,
            language=CSS,
            content="""\
Хоёр дүрэм ижил элементийн ижил шинж чанарыг заавал хөтөч аль нэгийг нь
сонгох ёстой. Дараалал нь:

1. `!important` байгаа эсэх
2. **Тодорхойлол** (specificity)
3. Файл дахь **дараалал** — сүүлчийнх ялна

### Тодорхойлол хэрхэн тоологддог вэ

Гурван оронтой тоо гэж төсөөл:

| Сонгогч | Оноо |
|---|---|
| `id` | 1-0-0 |
| Класс, шинж чанар, хуурамч ангилал | 0-1-0 |
| Элемент, хуурамч элемент | 0-0-1 |

```css
#tses            /* 1-0-0 */
.tses .holboos   /* 0-2-0 */
nav ul li a      /* 0-0-4 */
```

`#tses` нь `nav ul li a`-аас **ялна** — дөрвөн элемент нэг `id`-г давж
чадахгүй. Оноог нэмдэггүй, зүүнээс баруун тийш **харьцуулдаг**.

### Практик үр дагавар

Ийм учраас `id`-аар загварчлахгүй байх нь чухал. `#tses` дүрмийг дарахын
тулд өөр `id` эсвэл `!important` хэрэгтэй болно — хоёулаа муу.

Бүх зүйлээ **нэг класс** түвшинд байлгавал каскад энгийн байна: сүүлд
бичсэн нь ялна, тэгээд л болоо.

### Өв залгамжлал ялдаггүй

```css
body {
  color: navy;
}
p {
  color: gray;
}
```

Догол мөр саарал болно. Өвлөсөн утга нь **шууд заасан** утгатай
өрсөлдөхгүй — хамгийн сул нь.

### Анхдагч утга

```css
color: inherit;   /* эцгээсээ ав */
color: initial;   /* хөтчийн анхдагч */
color: unset;     /* өвлөгддөг бол inherit, үгүй бол initial */
```

`inherit` нь товч, оролт зэрэг өөрийн анхдагч өнгөтэй элементэд хэрэгтэй:

```css
button {
  font: inherit;   /* товч эцгийнхээ фонтыг авна */
}
```

Үүнгүй бол товч нь хөтчийн жижиг системийн фонтоор харагдана.

### Каскадыг хэрхэн шалгах вэ

DevTools-ийн **Elements** табд элемент сонгоод баруун талыг хар. Дарагдсан
дүрэм нь **зураастай** харагдана. Энэ нь «яагаад миний CSS ажиллахгүй
байна вэ» гэсэн асуултын хамгийн хурдан хариулт.
""",
            initial_code=css_page(
                title="Тодорхойлол ба каскад",
                body="""\
<h1>Аль дүрэм ялах вэ</h1>
<p>
  Нэг холбоос дөрвөн удаа — тус бүр өмнөхөөсөө нэг сонгогчоор илүү таарна.
  Тодорхойлол нь хамгийн өндөр дүрмийн өнгө ялна.
</p>
<ul>
  <li><a href="#ov">Нүүр</a> — <code>a</code>, 0-0-1</li>
  <li><a class="holboos" href="#ov">Нүүр</a> — <code>.holboos</code>, 0-1-0</li>
  <li><a class="holboos idevhtei" href="#ov">Нүүр</a> — <code>.holboos.idevhtei</code>, 0-2-0</li>
  <li><a id="nuur" class="holboos idevhtei" href="#ov">Нүүр</a> — <code>#nuur</code>, 1-0-0</li>
</ul>

<h2 id="ov">Өв залгамжлал хамгийн сул</h2>
<p>
  <code>body</code>-д navy өнгө тавьсан ч энэ догол мөрөнд шууд заасан өнгө
  ялсан. Гарчиг, жагсаалт харин navy өнгийг өвлөсөн.
</p>

<h2>Товч ба оролт</h2>
<form>
  <p>
    <label for="ner">Нэр</label>
    <input id="ner" type="text" name="ner" />
  </p>
  <p>
    <label for="sedev">Сэдэв</label>
    <select id="sedev" name="sedev">
      <option>Сонгогч</option>
      <option>Каскад</option>
    </select>
  </p>
  <p>
    <label for="sanal">Санал</label>
    <textarea id="sanal" name="sanal"></textarea>
  </p>
  <button type="submit">Илгээх</button>
</form>
""",
                css="""\
/* Тодорхойлолын харьцуулалт.
   Доорх бүх дүрэм НЭГ элементэд хамаарч болно:
   <a id="nuur" class="holboos idevhtei" href="/">Нүүр</a> */

/* 0-0-1 — хамгийн сул */
a {
  color: gray;
}

/* 0-1-0 — элементийг дарна */
.holboos {
  color: teal;
}

/* 0-2-0 — нэг класснаас хүчтэй */
.holboos.idevhtei {
  color: crimson;
}

/* 1-0-0 — бүгдийг дарна. Тиймээс id-аар загварчлахгүй байх нь дээр. */
#nuur {
  color: navy;
}

/* --- Өв залгамжлал хамгийн сул --- */
body {
  color: navy; /* p-д шууд заасан утга байвал ялагдана */
}

p {
  color: #486581;
}

/* --- inherit хэрэгтэй нэг тохиолдол --- */
button,
input,
select,
textarea {
  font: inherit; /* үүнгүй бол хөтчийн жижиг системийн фонт хэрэглэгдэнэ */
}
""",
            ),
        ),
    ],
)

COLORS_TEXT = ModuleSpec(
    title="Модул 9 — Өнгө ба текст",
    description="Унших тав тухтай, ялгарал сайтай текст.",
    lessons=[
        LessonSpec(
            title="Өнгө",
            slug="ungu",
            description="Нэр, hex, rgb, hsl болон ялгаралын шаардлага.",
            duration=400,
            language=CSS,
            content="""\
### Бичих аргууд

```css
color: teal;                    /* нэр — 140 орчим */
color: #008080;                 /* hex */
color: rgb(0 128 128);          /* улаан, ногоон, цэнхэр */
color: rgb(0 128 128 / 50%);    /* тунгалаг байдалтай */
color: hsl(180 100% 25%);       /* өнгө, ханалт, гэрэлтэлт */
```

Дөрвүүлээ ижил өнгө.

### Hex товчлол

```css
color: #ffffff;  /* = #fff */
color: #112233;  /* = #123 */
```

### Яагаад `hsl` вэ

`hsl` нь хүний ойлголтод ойр. Нэг өнгөний сүүдрүүд гаргахад хялбар:

```css
--undsen: hsl(180 100% 25%);
--undsen-tod: hsl(180 100% 35%);
--undsen-buden: hsl(180 100% 15%);
```

Зөвхөн гурав дахь тоог өөрчилж байна. `hex`-ээр ийм зүйл хийхэд тооны
машин хэрэгтэй.

### Дэвсгэр

```css
background-color: #f5f7fa;
```

`color` нь **текстийн**, `background-color` нь **дэвсгэрийн** өнгө.

### Ялгарал (contrast) — заавал шалга

Текст ба дэвсгэрийн хооронд хангалттай ялгаа байх ёстой:

| Текст | Шаардлагатай харьцаа |
|---|---|
| Энгийн текст | 4.5 : 1 |
| Том текст (24px+) | 3 : 1 |

Цайвар саарал дэвсгэр дээрх цайвар саарал текст нь дизайнерын дэлгэц
дээр гоё харагдаж болох ч нарны гэрэлд, эсвэл хараа султай хүнд
уншигдахгүй.

DevTools-ийн өнгө сонгогч нь харьцааг шууд харуулна. Хэрэв 4.5-аас бага
бол засах шаардлагатай.

> **Өнгө дангаараа мэдээлэл дамжуулж болохгүй.** «Улаан талбарыг
> засна уу» гэвэл өнгө ялгадаггүй хүн юуг засахаа мэдэхгүй. Дүрс эсвэл
> текст нэм.

### CSS хувьсагч

Өнгөө нэг газар тодорхойлж, хаа сайгүй ашиглана:

```css
:root {
  --undsen: #008080;
  --tekst: #1f2933;
}

h1 {
  color: var(--undsen);
}
```

Өнгө солих шаардлага гарвал нэг мөр засахад хангалттай.
""",
            initial_code=css_page(
                title="Өнгө",
                body="""\
<h1>Өнгө</h1>
<p class="tailbar">Бүдэг текст ч гэсэн ялгарал нь 4.5 : 1-ээс багагүй байх ёстой.</p>

<section class="hayrtsag">
  <h2>Дөрвөн бичлэг — нэг өнгө</h2>
  <ul>
    <li class="jishee-1"><code>teal</code></li>
    <li class="jishee-2"><code>#008080</code></li>
    <li class="jishee-3"><code>rgb(0 128 128)</code></li>
    <li class="jishee-4"><code>hsl(180 100% 25%)</code></li>
  </ul>
</section>

<p class="davhar">Энэ дэвсгэр нь 10% тунгалаг teal: <code>rgb(0 128 128 / 10%)</code></p>

<p>
  Ялгаралын тухай <a href="https://developer.mozilla.org">MDN</a>-ээс
  уншаарай. Холбоос дээр хулганаа аваачвал өнгө нь тодорно.
</p>
""",
                css="""\
/* Өнгөө нэг газар тодорхойлно */
:root {
  --undsen: hsl(180 100% 25%);
  --undsen-tod: hsl(180 100% 35%);
  --tekst: #1f2933;
  --tekst-buden: #616e7c;
  --devsger: #f5f7fa;
}

body {
  color: var(--tekst);
  background-color: white;
  font-family: system-ui, sans-serif;
}

h1 {
  color: var(--undsen);
}

/* Бүдэг текст — гэхдээ ялгарал 4.5:1-ээс дээш байх ёстой */
.tailbar {
  color: var(--tekst-buden);
}

/* padding — дотор зай, border-radius — булан бөөрөнхийлөх (Модул 10) */
.hayrtsag {
  background-color: var(--devsger);
  padding: 16px;
  border-radius: 8px;
}

/* Дөрвөн бичлэг — ижил өнгө */
.jishee-1 { color: teal; }
.jishee-2 { color: #008080; }
.jishee-3 { color: rgb(0 128 128); }
.jishee-4 { color: hsl(180 100% 25%); }

/* Тунгалаг байдал */
.davhar {
  background-color: rgb(0 128 128 / 10%);
}

a:hover {
  color: var(--undsen-tod);
}
""",
            ),
        ),
        LessonSpec(
            title="Фонт ба хэмжээ",
            slug="font-ba-hemjee",
            description="font-family, font-size, font-weight.",
            duration=400,
            language=CSS,
            content="""\
### `font-family`

Жагсаалт бичнэ — хөтөч эхний олдсоныг ашиглана:

```css
body {
  font-family: "Inter", system-ui, sans-serif;
}
```

Сүүлд нь **ерөнхий бүлэг** заавал бич (`sans-serif`, `serif`,
`monospace`). Бусад нь олдохгүй бол энэ нь аврана.

### Системийн фонт

```css
font-family: system-ui, sans-serif;
```

Хэрэглэгчийн үйлдлийн системийн фонтыг ашиглана. Татах шаардлагагүй тул
**шууд** харагдана.

### Кирилл үсэг

> Бүх фонт кирилл дэмждэггүй. Google Fonts-оос авахдаа `cyrillic`
> дэд олонлогийг заавал сонго. Үгүй бол монгол текст огт өөр фонтоор
> харагдана.

### `font-size`

```css
h1 { font-size: 2rem; }     /* үндсэн хэмжээний 2 дахин */
p  { font-size: 1rem; }     /* ихэвчлэн 16px */
small { font-size: 0.875rem; }
```

`rem` нь хөтчийн үндсэн хэмжээнээс тооцогдоно. Хэрэглэгч хараа муутай
тул фонтоо томруулсан бол таны хуудас **дагаж** томорно. `px` ашиглавал
тэр тохиргоог үл тоомсорлоно.

Биет текстийг 16px-ээс жижиг бүү болго.

### `font-weight`

```css
font-weight: 400;   /* энгийн */
font-weight: 700;   /* тод */
```

100-900 хооронд. Фонт тухайн жинг агуулаагүй бол хөтөч ойролцоог нь
сонгоно, эсвэл хиймлээр тодруулж муухай харагдана.

### `font` товчлол

```css
font: 700 1.5rem/1.4 system-ui, sans-serif;
```

`жин хэмжээ/мөрийн-өндөр гэр бүл`. Товч боловч бичээгүй зүйлсийг
анхдагч утга руу **буцаадаг** тул болгоомжтой ашигла.

### Хэмжээний шатлал

Санамсаргүй тоо сонгохын оронд харьцаа ашигла:

```css
h1 { font-size: 2.5rem; }
h2 { font-size: 1.75rem; }
h3 { font-size: 1.25rem; }
p  { font-size: 1rem; }
```

Тогтсон шатлал нь хуудсыг эмх цэгцтэй харагдуулна.
""",
            initial_code=css_page(
                title="Фонт ба хэмжээ",
                body="""\
<h1>Фонт ба хэмжээ</h1>
<p>Энэ хуудас системийн фонтыг ашиглана — татах шаардлагагүй тул шууд харагдана.</p>

<h2>Хэмжээний шатлал</h2>
<p>Гарчгууд санамсаргүй тоогоор биш, тогтсон харьцаагаар жижгэрнэ.</p>

<h3>Кодын фонт</h3>
<p>Код нь <code>monospace</code> бүлгийн фонтоор харагдана: <code>font-size: 1rem;</code></p>
<p><small>Жижиг тайлбар — 0.875rem. Үндсэн текстийг 16px-ээс жижиг бүү болго.</small></p>

<form>
  <p>
    <label for="ner">Нэр</label>
    <input id="ner" type="text" name="ner" />
    <button type="submit">Хадгалах</button>
  </p>
</form>
""",
                css="""\
:root {
  --font-undsen: system-ui, "Segoe UI", Roboto, sans-serif;
  --font-kod: "JetBrains Mono", Consolas, monospace;
}

body {
  /* Ерөнхий бүлгийг СҮҮЛД нь заавал бич */
  font-family: var(--font-undsen);
  font-size: 1rem;
  color: #1f2933;
}

/* Хэмжээний шатлал — санамсаргүй тоо биш, харьцаа */
h1 {
  font-size: 2.5rem;
  font-weight: 700;
}

h2 {
  font-size: 1.75rem;
  font-weight: 700;
}

h3 {
  font-size: 1.25rem;
  font-weight: 600;
}

p {
  font-size: 1rem;
  font-weight: 400;
}

small {
  font-size: 0.875rem;
}

/* Кодын фонт */
code,
pre {
  font-family: var(--font-kod);
  font-size: 0.9375rem;
}

/* Товч, оролт нь эцгийнхээ фонтыг авахгүй тул заавал заана */
button,
input,
select,
textarea {
  font: inherit;
}
""",
            ),
        ),
        LessonSpec(
            title="Текстийн загвар",
            slug="tekstiin-zagvar",
            description="text-align, line-height, text-decoration, зай.",
            duration=420,
            language=CSS,
            content="""\
### `line-height`

Мөр хоорондын зай. Уншигдац дээр хамгийн их нөлөөтэй ганц шинж чанар:

```css
body {
  line-height: 1.6;
}
```

**Нэгжгүй** тоо бич. `1.6` нь «фонтын хэмжээний 1.6 дахин» гэсэн утгатай
бөгөөд хүүхэд элемент өөрийн хэмжээнд тааруулж тооцно. `24px` гэж бичвэл
тогтмол утга өвлөгдөж, том текст шахагдана.

| Агуулга | Тохиромжтой |
|---|---|
| Урт текст | 1.5 - 1.7 |
| Гарчиг | 1.1 - 1.3 |

### `text-align`

```css
text-align: left;    /* анхдагч */
text-align: center;
text-align: right;
text-align: justify;
```

> Урт текстийг **голлуулж бүү бич**. Мөр бүрийн эхлэл өөр байрлалд байх
> тул нүд дараагийн мөрийг олоход хүндрэнэ. Гарчиг, богино текстэд л
> голлуул.

`justify` нь үгсийн хооронд жигд бус зай үүсгэдэг тул вэбэд бараг
хэрэглэдэггүй.

### `text-decoration`

```css
a {
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
```

> Холбоосын доогуур зураасыг **устгахдаа** өөр ялгаа нэм — өнгө
> дангаараа хангалтгүй. Өнгө ялгадаггүй хэрэглэгч холбоосыг олохгүй болно.

### Мөрийн урт

```css
.aguulga {
  max-width: 65ch;
}
```

`ch` нь «0» тэмдэгтийн өргөн. Нэг мөрөнд 50-75 тэмдэгт байхад хамгийн
тав тухтай уншигдана. Бүтэн дэлгэцийн өргөнтэй текст нь нүдийг
ядраана.

### Зайнуудын шинж чанар

```css
letter-spacing: 0.02em;   /* үсэг хооронд */
word-spacing: 0.1em;      /* үг хооронд */
text-transform: uppercase;
```

Том үсгээр бичсэн текстэд бага зэрэг `letter-spacing` нэмбэл уншигдац
сайжирна.

### Хэтэрсэн текст

```css
.nert {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
```

Гурвуулаа хамт байж л «…» гарна.
""",
            initial_code=css_page(
                title="Текстийн загвар",
                body="""\
<header class="gar-heseg">
  <p class="shoshgo">Модул 9 · Текстийн загвар</p>
  <h1>Уншихад тав тухтай текст</h1>
</header>

<main class="aguulga">
  <p>
    Мөр хоорондын зай уншигдацад хамгийн их нөлөөлдөг. Нэгжгүй
    <code>1.6</code> гэж бичвэл хүүхэд элемент бүр өөрийн фонтын хэмжээнд
    тааруулж тооцно. Нэг мөрөнд 50-75 тэмдэгт байхад нүд ядрахгүй тул энэ
    текст 65ch-ээс өргөсөхгүй — цонхоо өргөсгөөд үзээрэй.
  </p>

  <h2>Холбоос</h2>
  <p>
    Доогуур зураасыг устгасан ч <a href="https://developer.mozilla.org">энэ
    холбоос</a> доод хүрээгээрээ ялгарна.
  </p>

  <h2>Хэтэрсэн текст</h2>
  <p>240px-д багтахгүй урт нэр «…»-аар тасарна:</p>
  <p class="nert">HTML ба CSS — вэб хуудас бүтээх анхан шатны бүрэн сургалт</p>
</main>
""",
                css="""\
body {
  font-family: system-ui, sans-serif;
  /* Нэгжгүй тоо — хүүхэд элемент өөрийн хэмжээнд тааруулж тооцно */
  line-height: 1.6;
  color: #1f2933;
}

/* Мөрийн урт: 50-75 тэмдэгт хамгийн тав тухтай */
.aguulga {
  max-width: 65ch;
  margin-inline: auto;
}

h1,
h2 {
  line-height: 1.2;
}

/* Гарчгийг голлуулж болно, урт текстийг БОЛОХГҮЙ */
.gar-heseg {
  text-align: center;
}

/* Холбоосын зураасыг устгавал өөр ялгаа нэмнэ */
a {
  color: teal;
  text-decoration: none;
  border-bottom: 1px solid currentColor;
}

a:hover,
a:focus-visible {
  border-bottom-width: 2px;
}

/* Том үсэгт бага зэрэг үсгийн зай нэмбэл уншигдац сайжирна */
.shoshgo {
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-size: 0.75rem;
  color: #616e7c;
}

/* Хэтэрсэн текстийг «…» болгоно — гурвуулаа хамт байх ёстой */
.nert {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 240px;
}
""",
            ),
        ),
    ],
)

CSS_BASIC_MODULES = [CSS_BASICS, SELECTORS, COLORS_TEXT]
