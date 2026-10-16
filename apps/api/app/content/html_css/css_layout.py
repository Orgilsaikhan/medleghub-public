"""Модул 10-13 — Хайрцгийн загвар, байрлал, Flexbox, Grid.

Элементүүдийг хуудсан дээр байршуулах. CSS-ийн хамгийн их асуулт
төрүүлдэг хэсэг.
"""

from app.content.html_css.common import css_page
from app.content.types import LessonSpec, ModuleSpec
from app.models.enums import LessonLanguage

CSS = LessonLanguage.CSS

BOX_MODEL = ModuleSpec(
    title="Модул 10 — Хайрцгийн загвар",
    description="Элемент бүр хайрцаг. Түүний давхаргууд.",
    lessons=[
        LessonSpec(
            title="Агуулга ба дотор зай",
            slug="aguulga-ba-dotor-zai",
            description="content, padding — хайрцгийн дотор тал.",
            duration=400,
            language=CSS,
            content="""\
CSS-д **бүх зүйл хайрцаг**. Хайрцаг бүр дөрвөн давхаргатай:

```text
┌─────────────────────────────┐
│         margin              │  гадна зай
│  ┌───────────────────────┐  │
│  │       border          │  │  хүрээ
│  │  ┌─────────────────┐  │  │
│  │  │     padding     │  │  │  дотор зай
│  │  │  ┌───────────┐  │  │  │
│  │  │  │  content  │  │  │  │  агуулга
│  │  │  └───────────┘  │  │  │
│  │  └─────────────────┘  │  │
│  └───────────────────────┘  │
└─────────────────────────────┘
```

### Агуулгын хэмжээ

```css
.hayrtsag {
  width: 300px;
  height: 200px;
}
```

Блок элемент нь `width` заагаагүй бол эцгийнхээ **бүтэн өргөнийг** эзэлнэ.
Өндөр нь агуулгаараа тодорхойлогдоно.

> `height`-ыг тогтмол утгаар зааж өгөхөөс болгоомжил. Агуулга урт болвол
> хайрцгаас халина. Ихэвчлэн `min-height` илүү аюулгүй.

### `padding` — дотор зай

Агуулга ба хүрээ хоорондын зай:

```css
padding: 16px;                    /* дөрвөн тал */
padding: 16px 24px;               /* дээш-доош | хажуу */
padding: 8px 16px 12px 16px;      /* дээш | баруун | доош | зүүн */
```

Тус тусад нь:

```css
padding-top: 16px;
padding-inline: 24px;   /* зүүн ба баруун */
padding-block: 16px;    /* дээш ба доош */
```

`padding-inline` болон `padding-block` нь бичгийн чиглэлийг дагадаг тул
олон хэлтэй сайтад илүү зөв.

### `padding` нь дэвсгэрийн өнгийг авна

```css
.tovch {
  background-color: teal;
  padding: 12px 24px;
}
```

Дэвсгэр нь агуулга **болон** дотор зайг хамарна. Тиймээс товч томрох нь
дотор зайгаар зохицуулагддаг — `width` заах шаардлагагүй.

### Сөрөг утга байхгүй

`padding` нь сөрөг байж болохгүй. `margin` болно.
""",
            initial_code=css_page(
                title="Дотор зай",
                body="""\
<h1>Агуулга ба дотор зай</h1>

<div class="hayrtsag">
  Энэ хайрцаг 300px өргөн, өндөр нь 200px-аас багагүй. Дотор зай байхгүй
  тул текст ирмэгтээ наалдсан.
</div>

<h2>padding бичих дөрвөн арга</h2>
<p>Товч бүрийн дотор зай өөр, тиймээс хэмжээ нь ч өөр:</p>
<p>
  <button type="button" class="zai-1">16px</button>
  <button type="button" class="zai-2">16px 24px</button>
  <button type="button" class="zai-3">8px 16px 12px 16px</button>
  <button type="button" class="zai-4">block 16px, inline 24px</button>
</p>

<h2>Дэвсгэр дотор зайг хамарна</h2>
<p><button type="button" class="tovch">Бүртгүүлэх</button></p>

<div class="buten-urgun">
  Блок элементэд width заагаагүй тул эцгийнхээ бүтэн өргөнийг эзэлж байна.
</div>
""",
                css="""\
.hayrtsag {
  width: 300px;
  /* height биш min-height — агуулга урт болвол сунана */
  min-height: 200px;
  background-color: #e0f2f1;
}

/* Дөрвөн талд ижил */
.zai-1 {
  padding: 16px;
}

/* дээш-доош | хажуу */
.zai-2 {
  padding: 16px 24px;
}

/* дээш | баруун | доош | зүүн */
.zai-3 {
  padding: 8px 16px 12px 16px;
}

/* Бичгийн чиглэлийг дагадаг хувилбар */
.zai-4 {
  padding-block: 16px;
  padding-inline: 24px;
}

/* padding нь дэвсгэрийн өнгийг авна — товч ингэж томордог */
.tovch {
  background-color: teal;
  color: white;
  padding: 12px 24px;
  border: none;
  border-radius: 6px;
}

/* Блок элемент нь width заагаагүй бол эцгийнхээ бүтэн өргөнийг эзэлнэ */
.buten-urgun {
  background-color: #f5f7fa;
  padding: 24px;
}
""",
            ),
        ),
        LessonSpec(
            title="Хүрээ ба гадна зай",
            slug="huree-ba-gadna-zai",
            description="border, margin болон margin-ийн нийлэх зан төлөв.",
            duration=420,
            language=CSS,
            content="""\
### `border`

```css
border: 1px solid #cbd2d9;
```

Гурван утга: **өргөн**, **хэв маяг**, **өнгө**.

```css
border-style: solid;   /* dashed, dotted, double, none */
border-width: 2px;
border-color: teal;
border-bottom: 2px solid teal;   /* зөвхөн доод тал */
```

### `border-radius`

```css
border-radius: 8px;
border-radius: 50%;    /* дугуй */
```

### `outline` нь `border` биш

`outline` нь зай эзэлдэггүй тул хайрцгийн хэмжээг өөрчлөхгүй. Фокусын
тэмдэгт тохиромжтой нь ийм учиртай:

```css
button:focus-visible {
  outline: 2px solid teal;
  outline-offset: 2px;
}
```

### `margin` — гадна зай

Хайрцгуудын **хоорондын** зай:

```css
margin: 16px;
margin-block: 24px;
margin-inline: auto;
```

`margin` нь тунгалаг — дэвсгэрийн өнгийг авахгүй.

### Голлуулах

```css
.aguulga {
  max-width: 960px;
  margin-inline: auto;
}
```

`auto` нь үлдсэн зайг хоёр тал руу **тэнцүү** хуваарилна. Энэ бол блок
элементийг хэвтээгээр голлуулах стандарт арга.

### Margin нийлэх (collapsing)

Энэ нь шинэ суралцагчийг гайхшруулдаг:

```css
.deed { margin-bottom: 20px; }
.dood { margin-top: 30px; }
```

Хоорондын зай нь 50px **биш, 30px** болно. Дээш-доош чиглэлийн margin-ууд
нийлж, **хамгийн том нь** ялна.

Дүрмүүд:

- Зөвхөн **дээш-доош** чиглэлд нийлнэ, хажуу тийш нийлэхгүй
- `padding`, `border` дундуур нь орвол нийлэхгүй
- Flex болон grid савны хүүхдүүдэд нийлэхгүй

Тиймээс `gap` (Модул 12) ашиглавал энэ асуудал огт гарахгүй.

### Нэг чиглэлд бич

Margin-ийг зөвхөн **нэг чиглэлд** (жишээ нь доош) тавьбал нийлэх нөхцөл
багасч, тооцоолоход хялбар болно:

```css
.mur + .mur {
  margin-top: 16px;
}
```

Энэ нь «эхнийхээс бусад бүрд дээш зай» гэсэн утгатай.
""",
            initial_code=css_page(
                title="Хүрээ ба гадна зай",
                body="""\
<main class="aguulga">
  <h1 class="tabl">Хүрээ ба гадна зай</h1>

  <div class="kart">
    <img class="profil" src="/logos/html_css.png" alt="HTML ба CSS сургалтын лого" width="64" height="64" />
    <h2>HTML ба CSS</h2>
    <p>Хулганаа карт дээр аваачвал хүрээ нь өнгөө солино.</p>
    <p>Tab дарж товч дээр очвол хүрээнээс 2px зайтай outline гарна.</p>
    <button type="button">Дагах</button>
  </div>

  <h2>Margin нийлэх</h2>
  <div class="kart deed">Доороо 20px гадна зайтай.</div>
  <div class="kart dood">Дээрээ 30px. Хооронд нь 50px биш, 30px зай гарлаа.</div>

  <h2>Нэг чиглэлд бичих</h2>
  <div class="kart mur">Эхний мөрийн дээр нэмэлт зай байхгүй.</div>
  <div class="kart mur">Хоёр дахь мөр: дээр нь 16px.</div>
  <div class="kart mur">Гурав дахь мөр: дээр нь 16px.</div>
</main>
""",
                css="""\
.kart {
  border: 1px solid #cbd2d9;
  border-radius: 8px;
  padding: 16px;
  background-color: white;
}

.kart:hover {
  border-color: teal;
}

/* Зөвхөн доод хүрээ */
.tabl {
  border-bottom: 2px solid teal;
  padding-bottom: 8px;
}

/* outline нь зай эзэлдэггүй тул хэмжээг өөрчлөхгүй */
button:focus-visible {
  outline: 2px solid teal;
  outline-offset: 2px;
}

/* Голлуулах стандарт арга */
.aguulga {
  max-width: 960px;
  margin-inline: auto;
  padding-inline: 16px;
}

/* Margin нийлэх: 20 + 30 = 50 БИШ, 30 болно */
.deed {
  margin-bottom: 20px;
}

.dood {
  margin-top: 30px;
}

/* Нэг чиглэлд бичих нь тооцоолоход хялбар:
   «эхнийхээс бусад бүрд дээш зай» */
.mur + .mur {
  margin-top: 16px;
}

/* Дугуй зураг */
.profil {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  border: 2px solid teal;
}
""",
            ),
        ),
        LessonSpec(
            title="box-sizing",
            slug="box-sizing",
            description="Яагаад бүх төсөл border-box-оор эхэлдэг вэ.",
            duration=380,
            language=CSS,
            content="""\
### Асуудал

```css
.hayrtsag {
  width: 300px;
  padding: 20px;
  border: 5px solid teal;
}
```

Энэ хайрцаг дэлгэц дээр хэдэн пиксел эзлэх вэ? Хариулт нь **350px**:

```text
300 (агуулга) + 20 + 20 (дотор зай) + 5 + 5 (хүрээ) = 350
```

Анхдагчаар `width` нь зөвхөн **агуулгыг** хэмждэг. Дотор зай, хүрээ нь
дээр нь нэмэгддэг.

Энэ нь байршуулалтад толгой өвдөөнө. «Хоёр багана тус бүр 50%» гэж
бичээд дотор зай нэмэхэд нийлбэр нь 100%-иас хэтэрч, багана доош унана.

### Шийдэл

```css
* {
  box-sizing: border-box;
}
```

Одоо `width: 300px` нь **бүх зүйлийг оруулаад** 300px гэсэн утгатай.
Дотор зай, хүрээ нь дотогшоо иднэ.

### Бүх төслийн эхний мөр

```css
*,
*::before,
*::after {
  box-sizing: border-box;
}
```

Энэ гурван мөрийг CSS файлынхаа эхэнд бичээд март. Дараа нь бүх хэмжээ
зөв ойлгогдоно.

### Харьцуулалт

| | `content-box` (анхдагч) | `border-box` |
|---|---|---|
| `width: 300px` + 20px зай | 340px эзэлнэ | 300px эзэлнэ |
| Тооцоолол | Толгойд нэмэх шаардлагатай | Бичсэн тоо нь эцсийн тоо |

### Ердийн эхлэлийн блок

Олон хөгжүүлэгч дараах хэдэн мөрөөр эхэлдэг:

```css
*,
*::before,
*::after {
  box-sizing: border-box;
}

body {
  margin: 0;
}

img,
video {
  max-width: 100%;
  height: auto;
}
```

Сүүлийн дүрэм чухал: зураг эцгийнхээ өргөнөөс **хэтрэхгүй** болно. Үүнгүй
бол том зураг гар утсан дээр хуудсыг хэвтээгээр сунгана.
""",
            initial_code=css_page(
                title="box-sizing",
                body="""\
<h1>box-sizing</h1>

<p>Хоёр хайрцагт адилхан width: 300px, padding: 20px, 5px хүрээ өгсөн.</p>
<div class="border-box">border-box — нийт 300px</div>
<p>Харин content-box нь 300 + 40 + 10 = 350px эзэлнэ:</p>
<div class="content-box">content-box — нийт 350px</div>

<div class="baraadag">
  <h2>Зүүн тал</h2>
  <p>
    width: 50% ба padding: 16px. Дотор зай нь дотогшоо иддэг тул хоёр тал
    нэг мөрөнд багтана.
  </p>
</div>
<div class="baraadag">
  <h2>Баруун тал</h2>
  <img src="/logos/html_css.png" alt="HTML ба CSS сургалтын лого" width="416" height="418" />
  <p>Зураг 416px өргөн ч баганаасаа хэтрэхгүй.</p>
</div>
""",
                css="""\
/* Бүх төслийн эхний мөрүүд */
*,
*::before,
*::after {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: system-ui, sans-serif;
}

/* Зураг эцгийнхээ өргөнөөс ХЭТРЭХГҮЙ.
   Үүнгүй бол том зураг гар утсан дээр хуудсыг сунгана. */
img,
video {
  max-width: 100%;
  height: auto;
}

/* --- Ялгааг харьцуулах --- */

/* border-box: бичсэн 300px нь ЭЦСИЙН өргөн */
.border-box {
  box-sizing: border-box;
  width: 300px;
  padding: 20px;
  border: 5px solid teal;
}

/* content-box: 300 + 40 + 10 = 350px эзэлнэ */
.content-box {
  box-sizing: content-box;
  width: 300px;
  padding: 20px;
  border: 5px solid crimson;
}

/* border-box байхад л энэ найдвартай ажиллана */
.baraadag {
  width: 50%;
  padding: 16px;
  float: left;
}
""",
            ),
        ),
    ],
)

DISPLAY = ModuleSpec(
    title="Модул 11 — Харагдац ба байрлал",
    description="display, position, z-index.",
    lessons=[
        LessonSpec(
            title="display",
            slug="display",
            description="block, inline, inline-block, none.",
            duration=420,
            language=CSS,
            content="""\
`display` нь элемент бусадтайгаа хэрхэн зэрэгцэхийг тодорхойлно.

### `block`

```css
display: block;
```

- Бүтэн мөр эзэлнэ
- Шинэ мөрөөс эхэлнэ
- `width`, `height`, бүх `margin` ажиллана

Анхдагчаар: `div`, `p`, `h1`-`h6`, `section`, `main`.

### `inline`

```css
display: inline;
```

- Зөвхөн хэрэгтэй зайгаа эзэлнэ
- Мөр дотор урсана
- `width`, `height` **үл тоомсорлогдоно**
- Дээш-доош `margin` ажиллахгүй

Анхдагчаар: `a`, `span`, `strong`, `em`.

> Холбоост `padding` тавьсан ч дээш-доош талдаа бусад мөртэй давхцана.
> Товч мэт харагдуулах бол `inline-block` эсвэл `block` болго.

### `inline-block`

```css
display: inline-block;
```

Хоёрын завсрын хувилбар:

- Мөр дотор зэрэгцэнэ (inline шиг)
- `width`, `height`, бүх `margin` ажиллана (block шиг)

Холбоосыг товч болгоход тохиромжтой.

### `none`

```css
display: none;
```

Элементийг бүрэн **устгана** — зай ч эзлэхгүй, дэлгэц уншигч ч уншихгүй.

`visibility: hidden`-тэй андуурч болохгүй: тэр нь нууна ч **зайг нь
үлдээнэ**.

> Зөвхөн нүднээс нуух ч дэлгэц уншигчид үлдээх бол `display: none` бүү
> ашигла. Оронд нь `sr-only` хэв маягийн техник хэрэглэнэ.

### `flex` ба `grid`

```css
display: flex;
display: grid;
```

Хүүхдүүдээ хэрхэн байрлуулахыг өөрчилнө. Модул 12-13-т үзнэ.

### Анхдагчийг өөрчилж болно

```css
li {
  display: inline-block;  /* цэсний мөрүүдийг хажуу хажууд нь */
}
```

Гэхдээ семантикт нөлөөлөхгүй — `<li>` нь `<li>` хэвээрээ.
""",
            initial_code=css_page(
                title="display",
                body="""\
<header>
  <h1>display</h1>
  <nav aria-label="Хуудасны цэс">
    <ul class="tses">
      <li><a href="#blok">block</a></li>
      <li><a href="#inline">inline</a></li>
      <li><a href="#inline-block">inline-block</a></li>
      <li><a href="#none">none</a></li>
    </ul>
  </nav>
</header>

<main>
  <h2 id="blok">block</h2>
  <p>
    Энэ мөрийн дундах <span class="blok">span блок болсон</span> тул өмнө,
    хойно нь шинэ мөр эхэлж, 200px өргөн нь ажилласан.
  </p>

  <h2 id="inline">inline</h2>
  <p>
    Inline элемент мөр дотор урсана. <span class="mur">Энэ span-д width: 200px</span>
    өгсөн ч нөлөөлсөнгүй. Дотор зай нь хажуу тийшээ ажиллаж байгаа ч дээш-доош
    талдаа <span class="mur">бусад мөртэй давхцана</span>.
  </p>

  <h2 id="inline-block">inline-block</h2>
  <p>
    <span class="mur-blok">Нэг</span>
    <span class="mur-blok">Хоёр</span>
    <span class="mur-blok">Гурав</span>
  </p>
  <p><a class="tovch-holboos" href="#none">Товч шиг холбоос</a></p>

  <h2 id="none">none ба visibility: hidden</h2>
  <p>Эхний мөр.</p>
  <p class="nuuson">display: none — энэ мөр зай ч эзлэхгүй.</p>
  <p>Дээр нь нэг мөр нуугдсан ч зай үлдсэнгүй.</p>
  <p class="uzegdehgui">visibility: hidden — энэ мөр зайгаа үлдээнэ.</p>
  <p>Дээр нь хоосон зай үлдлээ.</p>
</main>
""",
                css="""\
/* Блок — бүтэн мөр эзэлнэ, шинэ мөрөөс эхэлнэ */
.blok {
  display: block;
  width: 200px;
  background-color: #e0f2f1;
  padding: 8px;
}

/* Inline — width, height үл тоомсорлогдоно */
.mur {
  display: inline;
  width: 200px; /* нөлөөлөхгүй */
  background-color: #fff3c4;
  padding: 8px; /* хажуу тийш ажиллана, дээш-доош давхцана */
}

/* Inline-block — зэрэгцэнэ, гэхдээ хэмжээ ажиллана */
.mur-blok {
  display: inline-block;
  width: 120px;
  padding: 8px;
  text-align: center;
  background-color: #e0f2f1;
}

/* Холбоосыг товч болгох */
.tovch-holboos {
  display: inline-block;
  padding: 10px 20px;
  background-color: teal;
  color: white;
  text-decoration: none;
  border-radius: 6px;
}

/* Цэсний мөрүүдийг хажуу хажууд нь */
.tses li {
  display: inline-block;
  margin-right: 16px;
}

/* none — зай ч эзлэхгүй, дэлгэц уншигч ч уншихгүй */
.nuuson {
  display: none;
}

/* visibility: hidden — нуугдана ч ЗАЙГ НЬ ҮЛДЭЭНЭ */
.uzegdehgui {
  visibility: hidden;
}
""",
            ),
        ),
        LessonSpec(
            title="position",
            slug="position",
            description="static, relative, absolute, fixed, sticky.",
            duration=450,
            language=CSS,
            content="""\
### `static` — анхдагч

Элемент ердийн урсгалдаа байна. `top`, `left` зэрэг үл тоомсорлогдоно.

### `relative`

```css
position: relative;
top: 10px;
left: 20px;
```

**Өөрийн байрнаасаа** шилжинэ. Гэхдээ анхны зай нь **хэвээр үлдэнэ** —
бусад элемент хөдлөхгүй.

Гол хэрэглээ нь: доторх `absolute` элементийн **тулгуур** болох.

### `absolute`

```css
position: absolute;
top: 0;
right: 0;
```

Ердийн урсгалаас **гарна** — зай эзлэхээ болино. Хамгийн ойрын
`position: relative` (эсвэл absolute/fixed) эцгийнхээ хувьд байрлана.

Тийм эцэг байхгүй бол **хуудсанд** харьцангуй байрлана. Энэ бол
байнгын алдааны эх үүсвэр:

```css
/* Тэмдэг картын өнцөгт байх ёстой */
.kart {
  position: relative;   /* ← үүнийг мартвал тэмдэг хуудасны өнцөгт очно */
}

.temdeg {
  position: absolute;
  top: 8px;
  right: 8px;
}
```

### `fixed`

```css
position: fixed;
bottom: 16px;
right: 16px;
```

**Цонхны** хувьд байрлана. Гүйлгэхэд хөдлөхгүй. Хөвөгч товч, cookie
мэдэгдэлд тохиромжтой.

### `sticky`

```css
position: sticky;
top: 0;
```

Ердийн байрандаа байгаад **гүйлгэхэд наалдана**. Хүснэгтийн толгой,
хэсгийн гарчигт төгс тохирно.

`top` (эсвэл бусад чиглэл) **заавал** зааж өгнө — үгүй бол юу ч болохгүй.
Мөн эцэг нь `overflow: hidden` байвал ажиллахгүй.

### Харьцуулалт

| Утга | Урсгалд байх уу | Юуны хувьд |
|---|---|---|
| `static` | Тийм | — |
| `relative` | Тийм | Өөрийн байр |
| `absolute` | Үгүй | Байрлалтай эцэг |
| `fixed` | Үгүй | Цонх |
| `sticky` | Тийм | Гүйлгэх сав |

### Байршуулалтад бүү ашигла

Багана, сүлжээ үүсгэхэд `absolute` **бүү** ашигла. Flexbox, Grid нь
хамаагүй найдвартай. `absolute` нь зөвхөн дээр нь **давхарлах** зүйлд
(тэмдэг, хаах товч, унждаг цэс).
""",
            initial_code=css_page(
                title="position",
                body="""\
<header id="deed">
  <h1>position</h1>
  <p>
    Хуудсыг доош гүйлгээрэй: «Таван утга» гарчиг хэсгээ дуустал дээд талдаа
    наалдаж, баруун доод өнцгийн товч байрнаасаа хөдлөхгүй.
  </p>
</header>

<main>
  <section>
    <h2 class="naalddag-tolgoi">Таван утга</h2>
    <dl>
      <dt>static</dt>
      <dd>Анхдагч. Ердийн урсгалдаа байх тул top, left үл тоомсорлогдоно.</dd>
      <dt>relative</dt>
      <dd>
        Өөрийн байрнаасаа шилжих ч анхны зай нь үлдэнэ. Доторх absolute
        элементийн тулгуур болно.
      </dd>
      <dt>absolute</dt>
      <dd>Урсгалаас гарч, хамгийн ойрын байрлалтай эцгийнхээ хувьд байрлана.</dd>
      <dt>fixed</dt>
      <dd>Цонхны хувьд байрлах тул гүйлгэхэд хөдлөхгүй.</dd>
      <dt>sticky</dt>
      <dd>
        Ердийн байрандаа байгаад гүйлгэхэд наалдана — яг энэ гарчиг шиг. top
        заавал хэрэгтэй.
      </dd>
    </dl>
  </section>

  <section>
    <h2>relative</h2>
    <p>
      Энэ өгүүлбэрийн <mark class="shiljsen">тэмдэглэсэн үг</mark> өөрийн
      байрнаасаа 20px баруун, 10px доош шилжсэн ч анхны зай нь хоосон үлдсэн.
    </p>
  </section>

  <section>
    <h2>absolute</h2>
    <article class="kart">
      <span class="temdeg">Шинэ</span>
      <h3>CSS Grid</h3>
      <p>Мөр ба багана хоёуланг нэг дор удирдана.</p>
    </article>
    <p>Тэмдэг картын өнцөгт байгаа нь карт position: relative учраас.</p>
    <article class="kart">
      <span class="temdeg">Үнэгүй</span>
      <h3>Flexbox</h3>
      <p>Нэг чиглэлийн байршуулалт.</p>
    </article>
  </section>

  <section>
    <h2>fixed</h2>
    <p>«Дээш буцах» товч цонхны баруун доод өнцөгт байрласан тул гүйлгэхэд хөдлөхгүй.</p>
    <p>
      Багана, сүлжээ үүсгэхэд absolute бүү ашигла — Flexbox, Grid хамаагүй
      найдвартай. absolute нь тэмдэг, хаах товч, унждаг цэс зэрэг дээр нь
      давхарлах зүйлд л тохирно.
    </p>
  </section>
</main>

<a class="hovugch-tovch" href="#deed">Дээш буцах</a>
""",
                css="""\
/* relative — доторх absolute элементийн ТУЛГУУР болно */
.kart {
  position: relative;
  padding: 16px;
  border: 1px solid #cbd2d9;
  border-radius: 8px;
}

/* Картын өнцөгт наалдсан тэмдэг.
   Эцэг нь relative биш бол ХУУДАСНЫ өнцөгт очно. */
.kart .temdeg {
  position: absolute;
  top: 8px;
  right: 8px;
  background-color: crimson;
  color: white;
  padding: 2px 8px;
  border-radius: 999px;
  font-size: 0.75rem;
}

/* fixed — цонхны хувьд, гүйлгэхэд хөдлөхгүй */
.hovugch-tovch {
  position: fixed;
  right: 16px;
  bottom: 16px;
  padding: 12px 20px;
  border-radius: 999px;
  background-color: teal;
  color: white;
}

/* sticky — гүйлгэхэд наалдана. top заавал хэрэгтэй. */
.naalddag-tolgoi {
  position: sticky;
  top: 0;
  background-color: white;
  border-bottom: 1px solid #cbd2d9;
  padding: 12px 0;
}

/* relative нь ӨӨРИЙН байрнаасаа шилжинэ, анхны зай нь үлдэнэ */
.shiljsen {
  position: relative;
  top: 10px;
  left: 20px;
}
""",
            ),
        ),
        LessonSpec(
            title="z-index ба давхарлалт",
            slug="z-index",
            description="Аль элемент дээр нь харагдах вэ.",
            duration=400,
            language=CSS,
            content="""\
Элементүүд давхацвал аль нь дээр байхыг `z-index` тодорхойлно:

```css
.tses {
  position: relative;
  z-index: 10;
}
```

### `position` шаардлагатай

> `z-index` нь `position: static` элементэд **ажиллахгүй**. Энэ бол
> хамгийн олон тохиолддог «яагаад ажиллахгүй байна вэ» асуулт.

Ажиллуулахын тулд `relative`, `absolute`, `fixed` эсвэл `sticky` байх
ёстой. (Flex болон grid хүүхдэд `position`-гүйгээр ч ажиллана.)

### Анхдагч дараалал

`z-index` огт заагаагүй бол HTML дэх **дараалал** шийднэ — сүүлд бичигдсэн
нь дээр байна.

### Давхарлалтын хүрээ (stacking context)

Энэ нь ойлгоход хэцүү ч чухал:

```css
.a {
  position: relative;
  z-index: 1;
}

.a .huuhed {
  position: relative;
  z-index: 9999;
}

.b {
  position: relative;
  z-index: 2;
}
```

`.a .huuhed` нь `z-index: 9999` ч гэсэн `.b`-ийн **доор** үлдэнэ. Учир нь
тэр `.a`-ийн хүрээнд хоригдсон — эцэг нь 1, `.b` нь 2.

Шинэ хүрээ үүсгэдэг зүйлс: `z-index`-тэй `position`, `opacity` нэгээс
бага, `transform`, `filter`.

Тиймээс асар том тоо бичих нь тусалдаггүй. **Эцгийн** `z-index`-ийг олж
засах хэрэгтэй.

### Утгаа төлөвлө

Санамсаргүй `z-index: 99999` бичихийн оронд шатлалаа тодорхойл:

```css
:root {
  --z-aguulga: 1;
  --z-naalddag: 10;
  --z-unjdag: 100;
  --z-tsonh: 1000;
}
```

Ингэснээр шинэ давхарга нэмэхэд хаана байрлахыг нь мэдэж байна.

### Сөрөг утга

```css
z-index: -1;
```

Агуулгын **ард** байрлуулна. Чимэглэлийн дэвсгэрт тохиромжтой ч
болгоомжтой — дарагдсан элемент дээр дарж болохгүй болно.
""",
            initial_code=css_page(
                title="z-index",
                body="""\
<header class="naalddag-tolgoi">
  <h1>z-index ба давхарлалт</h1>
  <nav aria-label="Унждаг цэс">
    <ul class="unjdag-tses">
      <li><a href="#tses">Унждаг цэс</a></li>
      <li><a href="#zanga">Давхарлалтын хүрээ</a></li>
      <li><a href="#chimeg">Чимэглэл</a></li>
    </ul>
  </nav>
</header>

<main>
  <p>
    <img src="/logos/html_css.png" alt="HTML ба CSS сургалтын лого" width="120" height="120" />
  </p>
  <p id="tses">
    Унждаг цэс (z-index: 100) толгой хэсгийн доор гарч, дээрх зургийг дарсан.
    Толгой хэсэг нь 10 тул цэс агуулгаас дээгүүр харагдана.
  </p>

  <section id="zanga">
    <h2>Давхарлалтын хүрээний занга</h2>
    <p>
      Доорх цонхны дэвсгэр (z-index: 1000) одоохондоо hidden шинж чанараар
      нуугдсан. index.html-ээс hidden-ийг устгаад хараарай: дэвсгэр хуудсыг
      бүдгэрүүлнэ, гэхдээ .huuhed дотор байгаа тул .a-ийн хүрээнд (1)
      хоригдоно. Тиймээс толгой хэсэг (10) ба .b (2) түүнээс дээгүүр тод үлдэнэ.
    </p>
    <div class="a">
      <p>.a — z-index: 1</p>
      <div class="huuhed">
        <p>.a .huuhed — z-index: 9999</p>
        <div class="tsonh-devsger" hidden></div>
      </div>
    </div>
    <div class="b" id="chimeg">
      <div class="chimeg"></div>
      <h3>.b — z-index: 2</h3>
      <p>Ард нь .chimeg (z-index: -1) өнгөт дэвсгэр болжээ.</p>
    </div>
  </section>
</main>
""",
                css="""\
/* Давхаргын шатлалаа урьдчилан төлөвлө */
:root {
  --z-aguulga: 1;
  --z-naalddag: 10;
  --z-unjdag: 100;
  --z-tsonh: 1000;
}

/* z-index нь position: static элементэд АЖИЛЛАХГҮЙ */
.naalddag-tolgoi {
  position: sticky;
  top: 0;
  z-index: var(--z-naalddag);
  background-color: white;
}

.unjdag-tses {
  position: absolute;
  top: 100%;
  left: 0;
  z-index: var(--z-unjdag);
  background-color: white;
  border: 1px solid #cbd2d9;
}

.tsonh-devsger {
  position: fixed;
  inset: 0;
  z-index: var(--z-tsonh);
  background-color: rgb(0 0 0 / 50%);
}

/* Чимэглэл агуулгын АРД */
.chimeg {
  position: absolute;
  inset: 0;
  z-index: -1;
  background: linear-gradient(180deg, #e0f2f1, transparent);
}

/* --- Давхарлалтын хүрээний занга ---
   .a .huuhed нь z-index 9999 ч гэсэн .b-ийн ДООР үлдэнэ,
   учир нь эцэг .a нь 1, харин .b нь 2. */
.a {
  position: relative;
  z-index: 1;
}

.a .huuhed {
  position: relative;
  z-index: 9999;
}

.b {
  position: relative;
  z-index: 2;
}
""",
            ),
        ),
    ],
)

FLEXBOX = ModuleSpec(
    title="Модул 12 — Flexbox",
    description="Нэг чиглэлийн байршуулалт.",
    lessons=[
        LessonSpec(
            title="Flex сав ба чиглэл",
            slug="flex-sav-ba-chiglel",
            description="display: flex болон flex-direction.",
            duration=420,
            language=CSS,
            content="""\
```css
.sav {
  display: flex;
}
```

Энэ нэг мөр нь **шууд хүүхдүүдийг** хажуу хажууд нь эгнүүлнэ.

### Хоёр талтай

| Тал | Юуг удирдах |
|---|---|
| Сав (container) | Хүүхдүүд хэрхэн байрлах |
| Хүүхэд (item) | Тухайн хүүхэд хэрхэн сунах |

Ихэнх шинж чанар нь **савд** бичигдэнэ.

### Тэнхлэг

Flexbox нь хоёр тэнхлэгтэй:

```text
flex-direction: row (анхдагч)

  үндсэн тэнхлэг →
  ┌─────┬─────┬─────┐
  │  1  │  2  │  3  │   ↓ хөндлөн тэнхлэг
  └─────┴─────┴─────┘
```

Энэ ойлголт чухал: `justify-content` нь **үндсэн** тэнхлэгт,
`align-items` нь **хөндлөн** тэнхлэгт ажиллана. `flex-direction`
өөрчлөхөд хоёул байраа солино.

### `flex-direction`

```css
flex-direction: row;             /* → анхдагч */
flex-direction: column;          /* ↓ */
flex-direction: row-reverse;     /* ← */
flex-direction: column-reverse;  /* ↑ */
```

`column` үед үндсэн тэнхлэг нь **доошоо** болно. Тиймээс `justify-content`
нь одоо босоо байрлалыг удирдана.

> `*-reverse` нь зөвхөн **харагдах** дарааллыг сольдог. Гараар шилжих
> дараалал HTML-ийнхээрээ үлдэнэ. Хэрэглэгч нүдээрээ харж байгаагаас өөр
> дараалалтай Tab дарвал төөрөгдөнө. Тиймээс ховор ашигла.

### Хүүхдүүд автоматаар шахагдана

Flex хүүхэд нь анхдагчаар агуулгынхаа хэмжээнд байх боловч зай хүрэхгүй
бол **шахагдана**. Шахагдахыг хориглох:

```css
.huuhed {
  flex-shrink: 0;
}
```

Лого, дүрс зэрэг гажуудаж болохгүй зүйлд хэрэгтэй.

### Хэзээ Flexbox, хэзээ Grid

| Нөхцөл | Сонголт |
|---|---|
| Нэг эгнээ эсвэл нэг багана | Flexbox |
| Мөр **ба** багана хоёулаа | Grid |
| Агуулгын хэмжээгээр нь тараах | Flexbox |
| Тогтсон бүтэцтэй хуудас | Grid |
""",
            initial_code=css_page(
                title="Flex сав",
                body="""\
<header class="tolgoi">
  <img class="logo" src="/logos/html_css.png" alt="HTML ба CSS сургалтын лого" width="40" height="40" />
  <nav aria-label="Үндсэн цэс">
    <ul class="tses">
      <li><a href="#flex">Flexbox</a></li>
      <li><a href="#grid">Grid</a></li>
      <li><a href="https://developer.mozilla.org">MDN</a></li>
    </ul>
  </nav>
</header>

<main>
  <h1>Flex сав ба чиглэл</h1>

  <div class="sav">
    <nav class="hajuu-tses" aria-label="Хажуугийн цэс">
      <a href="#flex">Flexbox</a>
      <a href="#grid">Grid</a>
      <a href="https://developer.mozilla.org">MDN</a>
    </nav>

    <article class="kart" id="flex">
      <h2>Flexbox</h2>
      <p>Нэг эгнээ эсвэл нэг багана.</p>
      <a href="https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_flexible_box_layout">MDN-ээс унших</a>
    </article>

    <article class="kart" id="grid">
      <h2>Grid</h2>
      <p>Мөр ба багана хоёулаа.</p>
      <a href="https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout">MDN-ээс унших</a>
    </article>
  </div>
</main>
""",
                css="""\
/* Нэг мөр — хүүхдүүд хажуу хажууд нь эгнэнэ */
.sav {
  display: flex;
  gap: 16px;
}

/* Хэвтээ цэс */
.tses {
  display: flex;
  flex-direction: row;
  gap: 24px;
  list-style: none;
  margin: 0;
  padding: 0;
}

/* Босоо жагсаалт — үндсэн тэнхлэг доошоо болно */
.hajuu-tses {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

/* Лого гажуудаж болохгүй тул шахагдахыг хориглоно */
.logo {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
}

/* Толгой хэсэг: лого зүүн, цэс баруун */
.tolgoi {
  display: flex;
  flex-direction: row;
  gap: 16px;
  padding: 12px 24px;
  border-bottom: 1px solid #cbd2d9;
}

/* Картын дотор босоо байршуулалт */
.kart {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 16px;
  border: 1px solid #cbd2d9;
  border-radius: 8px;
}
""",
            ),
        ),
        LessonSpec(
            title="justify-content ба align-items",
            slug="justify-content-ba-align-items",
            description="Хоёр тэнхлэгт байрлуулах.",
            duration=450,
            language=CSS,
            content="""\
### `justify-content` — үндсэн тэнхлэг

```css
justify-content: flex-start;     /* эхэнд — анхдагч */
justify-content: center;         /* голд */
justify-content: flex-end;       /* төгсгөлд */
justify-content: space-between;  /* захад нь наана, зайг дундуур нь */
justify-content: space-around;   /* тус бүрийн хоёр талд тэнцүү */
justify-content: space-evenly;   /* бүх зай тэнцүү */
```

`space-between` нь хамгийн түгээмэл — толгой хэсэгт лого зүүн, цэс баруун
байрлуулахад яг тохирно:

```css
.tolgoi {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
```

### `align-items` — хөндлөн тэнхлэг

```css
align-items: stretch;     /* бүтэн өндөр — анхдагч */
align-items: center;      /* голд */
align-items: flex-start;  /* дээр */
align-items: flex-end;    /* доор */
align-items: baseline;    /* текстийн суурь шугамаар */
```

`stretch` нь анхдагч байдгийг анхаар — тиймээс өөр өндөртэй картууд
автоматаар **тэгширнэ**. Энэ ихэвчлэн хүссэн үр дүн.

### Голлуулах

Хуучин CSS-д хамгийн хэцүү ажил байсан нь одоо хоёр мөр:

```css
.golld {
  display: flex;
  justify-content: center;
  align-items: center;
}
```

Хэвтээ ба босоо хоёуланд нь голд байрлана.

### `align-self`

Ганц хүүхдийг өөрөөр байрлуулах:

```css
.ontsgoi {
  align-self: flex-start;
}
```

### `margin: auto` заль мэх

Flex дотор `auto` margin нь боломжтой бүх зайг иднэ:

```css
.tses .suuliinh {
  margin-left: auto;
}
```

Энэ нь тухайн элементийг **баруун тийш түлхэнэ**, бусад нь зүүн талдаа
үлдэнэ. `space-between`-ээс илүү нарийн хяналт өгнө.

### Түгээмэл загварууд

```css
/* Лого зүүн, цэс баруун */
.tolgoi {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Дүрс ба текст зэрэгцээ, босоогоор голд */
.mur {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* Товчнууд баруун доод өнцөгт */
.tovchnuud {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}
```
""",
            initial_code=css_page(
                title="Flex тэнхлэгүүд",
                body="""\
<header class="tolgoi">
  <div class="mur">
    <img src="/logos/html_css.png" alt="HTML ба CSS сургалтын лого" width="32" height="32" />
    <strong>HTML ба CSS</strong>
  </div>
  <button type="button">Нэвтрэх</button>
</header>

<nav class="tses mur" aria-label="Хуудасны цэс">
  <a href="#golluulah">Голлуулах</a>
  <a href="#shuult">Шүүлтүүр</a>
  <a class="suuliinh" href="https://developer.mozilla.org">Тусламж</a>
</nav>

<main>
  <h1>justify-content ба align-items</h1>

  <h2 id="golluulah">Голлуулах</h2>
  <div class="golld">
    <p>Энэ бичиг хэвтээ ба босоо чиглэлд голд байна.</p>
  </div>

  <h2 id="shuult">Шүүлтүүр</h2>
  <p>
    Бүлгүүд ижил өндөртэй болсон нь align-items: stretch. «Үнэ» нь .ontsgoi
    тул өөрийн өндрөөрөө дээд талдаа үлдсэн.
  </p>
  <form>
    <div class="kartuud">
      <fieldset>
        <legend>Хэл</legend>
        <label><input type="checkbox" name="hel" value="html" checked /> HTML</label><br />
        <label><input type="checkbox" name="hel" value="css" checked /> CSS</label><br />
        <label><input type="checkbox" name="hel" value="js" /> JavaScript</label><br />
        <label><input type="checkbox" name="hel" value="python" /> Python</label>
      </fieldset>
      <fieldset>
        <legend>Түвшин</legend>
        <label><input type="radio" name="tuvshin" value="anhan" checked /> Анхан</label><br />
        <label><input type="radio" name="tuvshin" value="dund" /> Дунд</label>
      </fieldset>
      <fieldset class="ontsgoi">
        <legend>Үнэ</legend>
        <label><input type="checkbox" name="une" value="unegui" /> Үнэгүй</label>
      </fieldset>
    </div>
    <div class="tovchnuud">
      <button type="reset">Цэвэрлэх</button>
      <button type="button">Шүүх</button>
    </div>
  </form>
</main>
""",
                css="""\
/* Хамгийн түгээмэл загвар: лого зүүн, цэс баруун */
.tolgoi {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 24px;
}

/* Хэвтээ БА босоогоор голд — хуучин CSS-ийн хамгийн хэцүү ажил */
.golld {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}

/* Дүрс ба текст зэрэгцээ */
.mur {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* Товчнууд баруун тийш */
.tovchnuud {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

/* align-items: stretch нь анхдагч — картууд автоматаар тэгширнэ */
.kartuud {
  display: flex;
  gap: 16px;
  align-items: stretch;
}

/* Ганц хүүхдийг өөрөөр байрлуулах */
.ontsgoi {
  align-self: flex-start;
}

/* margin: auto нь боломжтой бүх зайг иднэ —
   энэ элементийг баруун тийш түлхэнэ */
.tses .suuliinh {
  margin-left: auto;
}
""",
            ),
        ),
        LessonSpec(
            title="gap, flex-wrap ба сунах",
            slug="gap-flex-wrap",
            description="Зай, мөр таслах, flex-grow.",
            duration=450,
            language=CSS,
            content="""\
### `gap`

Хүүхдүүдийн хоорондын зай:

```css
.sav {
  display: flex;
  gap: 16px;
}

.sav-2 {
  gap: 16px 24px;   /* мөр хооронд | багана хооронд */
}
```

`gap` нь `margin`-аас хамаагүй дээр:

- Зөвхөн **хооронд** зай тавина — захад нь тавихгүй
- «Сүүлчийнхээс бусад» гэсэн дүрэм бичих шаардлагагүй
- Margin нийлэх асуудал үүсэхгүй

### `flex-wrap`

Анхдагчаар flex хүүхдүүд **хэзээ ч мөр таслахгүй** — зай хүрэхгүй бол
шахагдана.

```css
.sav {
  display: flex;
  flex-wrap: wrap;
}
```

Одоо багтахгүй бол шинэ мөр рүү шилжинэ. Энэ нь хариуцлагатай
байршуулалтын хамгийн энгийн арга.

### Хариуцлагатай карт

```css
.kartuud {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.kart {
  flex: 1 1 280px;
}
```

Медиа асуулга бичихгүйгээр: карт бүр 280px-аас багагүй байхыг хичээнэ,
зай хүрэхгүй бол доош шилжинэ.

### `flex` товчлол

```css
flex: 1 1 280px;
```

Гурван утга:

| Утга | Нэр | Утга учир |
|---|---|---|
| `1` | `flex-grow` | Илүү зайг эзлэх эсэх |
| `1` | `flex-shrink` | Шахагдах эсэх |
| `280px` | `flex-basis` | Эхлэлийн хэмжээ |

Түгээмэл товчлолууд:

```css
flex: 1;      /* = 1 1 0 — бүх зайг тэнцүү хуваана */
flex: auto;   /* = 1 1 auto — агуулгаараа, дараа нь сунана */
flex: none;   /* = 0 0 auto — огт өөрчлөгдөхгүй */
```

### `flex: 1` хамгийн түгээмэл

```css
.hajuu {
  width: 240px;
  flex-shrink: 0;
}

.aguulga {
  flex: 1;   /* үлдсэн бүх зайг эзэлнэ */
}
```

Хажуугийн хэсэг тогтмол, агуулга нь үлдсэнийг иднэ. Хоёр багана
байршуулалтын стандарт арга.

### `align-content`

Мөр таслагдсан үед **мөрүүдийг** байрлуулна:

```css
align-content: flex-start;
```

`align-items` нь мөр доторх элементүүдийг, `align-content` нь мөрүүдийг
өөрсдийг нь байрлуулдгийг ялгаж ойлгоорой.
""",
            initial_code=css_page(
                title="gap ба flex-wrap",
                body="""\
<header class="sav">
  <img class="logo" src="/logos/html_css.png" alt="HTML ба CSS сургалтын лого" width="40" height="40" />
  <nav aria-label="Үндсэн цэс">
    <ul class="tses">
      <li><a href="#hicheeluud">Хичээлүүд</a></li>
      <li><a href="#hoyor-bagana">Хоёр багана</a></li>
      <li><a href="https://developer.mozilla.org">MDN</a></li>
    </ul>
  </nav>
</header>

<main>
  <h1>gap, flex-wrap ба сунах</h1>

  <h2 id="hicheeluud">Хариуцлагатай картууд</h2>
  <p>
    Карт бүр 280px-аас багагүй. Багтахгүй бол дараагийн мөр рүү шилжээд
    үлдсэн зайг эзэлнэ.
  </p>
  <div class="kartuud">
    <article class="kart">
      <h3>HTML</h3>
      <p>Хуудасны бүтэц, агуулга.</p>
    </article>
    <article class="kart">
      <h3>CSS</h3>
      <p>Өнгө, хэмжээ, байршуулалт.</p>
    </article>
    <article class="kart">
      <h3>JavaScript</h3>
      <p>Хуудсанд үйлдэл нэмнэ.</p>
    </article>
  </div>

  <h2 id="hoyor-bagana">Хоёр багана</h2>
  <div class="baiguulalt">
    <aside class="hajuu">
      <h3>Хажуу хэсэг</h3>
      <p>Өргөн нь 240px, шахагдахгүй.</p>
    </aside>
    <section class="aguulga">
      <h3>Агуулга</h3>
      <p>
        flex: 1 тул үлдсэн бүх зайг эзэлнэ. Цонх өргөсөхөд зөвхөн энэ хэсэг
        сунана.
      </p>
    </section>
  </div>
</main>
""",
                css="""\
/* gap — зөвхөн ХООРОНД зай тавина, захад нь тавихгүй */
.sav {
  display: flex;
  gap: 16px;
}

/* Хариуцлагатай карт — медиа асуулгагүйгээр.
   Карт бүр 280px-аас багагүй, зай хүрэхгүй бол доош шилжинэ. */
.kartuud {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.kart {
  flex: 1 1 280px;
  padding: 16px;
  border: 1px solid #cbd2d9;
  border-radius: 8px;
}

/* Хоёр багана: хажуу тогтмол, агуулга үлдсэнийг иднэ */
.baiguulalt {
  display: flex;
  gap: 24px;
}

.hajuu {
  width: 240px;
  flex-shrink: 0;
}

.aguulga {
  flex: 1;
}

/* Хэвтээ цэс — багтахгүй бол доош шилжинэ */
.tses {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 24px;
  list-style: none;
  padding: 0;
}

/* flex: none — огт өөрчлөгдөхгүй */
.logo {
  flex: none;
  width: 40px;
}
""",
            ),
        ),
    ],
)

GRID = ModuleSpec(
    title="Модул 13 — CSS Grid",
    description="Хоёр чиглэлийн байршуулалт.",
    lessons=[
        LessonSpec(
            title="Grid сав, багана ба мөр",
            slug="grid-sav-bagana-mur",
            description="display: grid болон grid-template-columns.",
            duration=450,
            language=CSS,
            content="""\
Grid нь **мөр ба багана хоёуланг** нэг дор удирдана. Flexbox нэг чиглэлд
ажилладаг бол Grid хоёр чиглэлд.

```css
.sav {
  display: grid;
  grid-template-columns: 200px 200px 200px;
  gap: 16px;
}
```

### `fr` нэгж

Grid-ийн өөрийн нэгж — **үлдсэн зайн хэсэг**:

```css
grid-template-columns: 1fr 1fr 1fr;   /* гурван тэнцүү багана */
grid-template-columns: 2fr 1fr;       /* эхнийх нь хоёр дахин өргөн */
grid-template-columns: 240px 1fr;     /* тогтмол + үлдсэн бүгд */
```

Сүүлийнх нь хажуугийн цэстэй хуудасны стандарт бүтэц.

### `repeat`

```css
grid-template-columns: repeat(3, 1fr);
grid-template-columns: repeat(4, 1fr);
```

### Хариуцлагатай сүлжээ

Энэ нэг мөрийг сайн сурч ав:

```css
grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
```

Утга нь: «240px-аас багагүй багана аль болох олон багтаа, үлдсэн зайг
тэнцүү хуваа».

Медиа асуулга **огт бичихгүйгээр** хариуцлагатай сүлжээ болно. Дэлгэц
нарийсахад багана нь өөрөө цөөрнө.

| Утга | Ялгаа |
|---|---|
| `auto-fit` | Хоосон баганыг хумина — элементүүд сунана |
| `auto-fill` | Хоосон баганыг үлдээнэ |

Ихэвчлэн `auto-fit` хэрэгтэй.

### Мөр

```css
grid-template-rows: 80px 1fr 60px;
```

Заагаагүй мөр нь агуулгаараа өндөртэй болно. Ихэнхдээ мөрийг зааж өгөх
шаардлагагүй.

### `gap`

```css
gap: 16px;
gap: 24px 16px;   /* мөр хооронд | багана хооронд */
```

Flexbox-тэй ижил ажиллана.

### Автомат байршуулалт

Хүүхдүүд зааж өгөөгүй бол **зүүнээс баруун, дээрээс доош** дараалан
байрлана. Ихэнх тохиолдолд энэ хангалттай — зөвхөн саваа тодорхойлоод
болоо.
""",
            initial_code=css_page(
                title="Grid сүлжээ",
                body="""\
<main>
  <h1>Grid сав, багана ба мөр</h1>

  <h2>Гурван тэнцүү багана</h2>
  <div class="sulzhee">
    <div class="kart">1</div>
    <div class="kart">2</div>
    <div class="kart">3</div>
    <div class="kart">4</div>
    <div class="kart">5</div>
    <div class="kart">6</div>
  </div>

  <h2>Тогтмол хажуу ба үлдсэн зай</h2>
  <div class="baiguulalt">
    <div class="kart">240px</div>
    <div class="kart">1fr — үлдсэн бүх зай</div>
  </div>

  <h2>Эхнийх нь хоёр дахин өргөн</h2>
  <div class="hoyor-bagana">
    <div class="kart">2fr</div>
    <div class="kart">1fr</div>
  </div>

  <h2>Хариуцлагатай сүлжээ</h2>
  <p>
    240px-аас багагүй багана аль болох олон багтана. Цонх нарийсахад багана
    нь өөрөө цөөрнө.
  </p>
  <div class="kartuud">
    <article class="kart">
      <h3>HTML</h3>
      <p>Хуудасны бүтэц.</p>
    </article>
    <article class="kart">
      <h3>CSS</h3>
      <p>Хуудасны загвар.</p>
    </article>
    <article class="kart">
      <h3>JavaScript</h3>
      <p>Хуудасны үйлдэл.</p>
    </article>
    <article class="kart">
      <h3>Python</h3>
      <p>Өгөгдөл боловсруулах.</p>
    </article>
  </div>

  <h2>Мөр</h2>
  <div class="togtson-mur">
    <div class="kart">Толгой — 80px</div>
    <div class="kart">Агуулга — 1fr, үлдсэн өндөр</div>
    <div class="kart">Хөл — 60px</div>
  </div>
</main>
""",
                css="""\
/* Гурван тэнцүү багана */
.sulzhee {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

/* Тогтмол хажуу + үлдсэн бүгд */
.baiguulalt {
  display: grid;
  grid-template-columns: 240px 1fr;
  gap: 24px;
}

/* Эхнийх нь хоёр дахин өргөн */
.hoyor-bagana {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 32px;
}

/* ХАРИУЦЛАГАТАЙ СҮЛЖЭЭ — медиа асуулга огт хэрэггүй.
   «240px-аас багагүй багана аль болох олон багтаа». */
.kartuud {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
}

.kart {
  padding: 16px;
  border: 1px solid #cbd2d9;
  border-radius: 8px;
}

/* Мөрийг ч зааж болно — ихэнхдээ шаардлагагүй */
.togtson-mur {
  display: grid;
  grid-template-rows: 80px 1fr 60px;
  min-height: 100vh;
}
""",
            ),
        ),
        LessonSpec(
            title="grid-template ба талбай",
            slug="grid-template-ba-talbai",
            description="Элементийг тодорхой нүдэнд байрлуулах.",
            duration=450,
            language=CSS,
            content="""\
### Шугамаар байрлуулах

Grid-ийн шугамууд 1-ээс эхэлж дугаарлагдана:

```text
1     2     3     4
│  A  │  B  │  C  │
```

```css
.uragsh {
  grid-column: 1 / 3;   /* 1-ээс 3 дахь шугам хүртэл = хоёр багана */
}

.busad {
  grid-row: 2 / 4;
}
```

### `span`

Хэдэн нүд эзлэхийг шууд бичих нь илүү ойлгомжтой:

```css
.tom {
  grid-column: span 2;
  grid-row: span 2;
}
```

### Бүх баганыг эзлэх

```css
.buten {
  grid-column: 1 / -1;
}
```

`-1` нь **сүүлчийн шугам**. Багана хэд ч байсан ажиллана — гарчиг,
тусгаарлагчид тохиромжтой.

### Нэрлэсэн талбай

Хамгийн уншигдахуйц арга. Байршуулалтаа **зурж** бичнэ:

```css
.huudas {
  display: grid;
  grid-template-columns: 240px 1fr;
  grid-template-rows: auto 1fr auto;
  grid-template-areas:
    "tolgoi tolgoi"
    "hajuu  aguulga"
    "hul    hul";
  min-height: 100vh;
  gap: 16px;
}

.tolgoi  { grid-area: tolgoi; }
.hajuu   { grid-area: hajuu; }
.aguulga { grid-area: aguulga; }
.hul     { grid-area: hul; }
```

Кодыг харангуутаа бүтэц нь харагдана. Хоосон нүд хэрэгтэй бол цэг бич:

```css
grid-template-areas:
  "tolgoi tolgoi"
  ".      aguulga";
```

### Байршуулалтыг өөрчлөх

Нэрлэсэн талбайн гол давуу тал нь: гар утсанд зориулж **зөвхөн зургийг**
дахин бичихэд болно. Доорх `@media (max-width: 640px) { … }` нь «дэлгэцийн
өргөн 640 пиксел буюу түүнээс нарийн үед л доторх дүрмүүдийг хэрэглэ»
гэсэн нөхцөл. Үүнийг дараагийн модульд (Модул 14) нарийн үзнэ — одоо
зөвхөн талбайн зургийг хэрхэн дахин зурж байгааг ажигла.

```css
@media (max-width: 640px) {
  .huudas {
    grid-template-columns: 1fr;
    grid-template-areas:
      "tolgoi"
      "aguulga"
      "hajuu"
      "hul";
  }
}
```

HTML-д огт хүрэхгүйгээр хажуугийн хэсгийг агуулгын доош шилжүүллээ.

### Голлуулах

Grid дээр ч хоёр мөр:

```css
.golld {
  display: grid;
  place-items: center;
}
```

`place-items` нь `align-items` ба `justify-items`-ийн товчлол.
""",
            initial_code=css_page(
                title="Grid талбай",
                body="""\
<div class="huudas">
  <header class="tolgoi">
    <h1>Нэрлэсэн талбай</h1>
  </header>

  <nav class="hajuu" aria-label="Хажуугийн цэс">
    <ul>
      <li><a href="#span">Шугам ба span</a></li>
      <li><a href="#golluulah">Голлуулах</a></li>
    </ul>
  </nav>

  <main class="aguulga">
    <h2 id="span">Шугам ба span</h2>
    <p>«0» товч хоёр багана, «=» товч бүх баганыг эзэлнэ.</p>
    <div class="sulzhee">
      <button type="button">7</button>
      <button type="button">8</button>
      <button type="button">9</button>
      <button type="button">4</button>
      <button type="button">5</button>
      <button type="button">6</button>
      <button type="button">1</button>
      <button type="button">2</button>
      <button type="button">3</button>
      <button type="button" class="tom">0</button>
      <button type="button">.</button>
      <button type="button" class="buten">=</button>
    </div>

    <h2 id="golluulah">Голлуулах</h2>
    <div class="golld">
      <p>Энэ бичиг хоёр чиглэлд голд байна.</p>
    </div>
  </main>

  <footer class="hul">
    <p>Цонхыг 640px-ээс нарийсгавал хажуу хэсэг агуулгын доор шилжинэ.</p>
  </footer>
</div>
""",
                css="""\
/* --- Нэрлэсэн талбай: байршуулалтаа ЗУРЖ бичнэ --- */
.huudas {
  display: grid;
  grid-template-columns: 240px 1fr;
  grid-template-rows: auto 1fr auto;
  grid-template-areas:
    "tolgoi tolgoi"
    "hajuu  aguulga"
    "hul    hul";
  min-height: 100vh;
  gap: 16px;
}

.tolgoi {
  grid-area: tolgoi;
}

.hajuu {
  grid-area: hajuu;
}

.aguulga {
  grid-area: aguulga;
}

.hul {
  grid-area: hul;
}

/* Гар утсанд — HTML-д хүрэхгүйгээр дарааллыг өөрчилнө.
   @media (max-width: 640px) доторх дүрэм зөвхөн дэлгэц 640px-ээс нарийн
   үед ажиллана (Модул 14-т нарийн үзнэ). */
@media (max-width: 640px) {
  .huudas {
    grid-template-columns: 1fr;
    grid-template-areas:
      "tolgoi"
      "aguulga"
      "hajuu"
      "hul";
  }
}

/* --- Шугам ба span --- */
.sulzhee {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

/* Хоёр багана эзэлнэ */
.tom {
  grid-column: span 2;
}

/* Багана хэд ч байсан бүгдийг эзэлнэ */
.buten {
  grid-column: 1 / -1;
}

/* Хоёр мөрөөр голлуулах */
.golld {
  display: grid;
  place-items: center;
  min-height: 200px;
}
""",
            ),
        ),
        LessonSpec(
            title="Үндсэн байршуулалтууд",
            slug="undsen-baiguulaltuud",
            description="Бодит хуудсанд тохиолддог гурван бүтэц.",
            duration=480,
            language=CSS,
            content="""\
### 1. Бүтэн хуудасны бүтэц

Хөл хэсгийг доод талд нь наах сонгодог бодлого:

```css
body {
  min-height: 100vh;
  display: grid;
  grid-template-rows: auto 1fr auto;
}
```

Гурван мөр: толгой агуулгаараа, агуулга үлдсэнийг иднэ, хөл агуулгаараа.
Агуулга богино байсан ч хөл нь дэлгэцийн доод хэсэгт наалдана.

`100vh`-ийн оронд `100dvh` бичвэл гар утасны хаягийн мөр нуугдахад ч
зөв ажиллана.

### 2. Голлосон агуулга

```css
.aguulga {
  width: min(100% - 32px, 960px);
  margin-inline: auto;
}
```

`min()` нь хоёрын жижигийг сонгоно: жижиг дэлгэцэнд 16px-ийн хажуугийн
зайтай бүтэн өргөн, том дэлгэцэнд 960px.

Хоёр дүрэм (`max-width` + `padding`) оронд нэг мөр.

### 3. Карт сүлжээ

```css
.kartuud {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 20px;
}
```

### Картын дотор

Карт бүр өөрөө flex сав байх нь түгээмэл:

```css
.kart {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.kart-tovch {
  margin-top: auto;
}
```

`margin-top: auto` нь товчийг **доод тал руу** түлхэнэ. Тиймээс өөр өөр
урттай картуудын товч нэг шугамд эгнэнэ — жижиг нарийн ширийн зүйл ч
цэгцтэй харагдуулна.

### Grid ба Flexbox хамт

Энэ бол ердийн хослол:

- **Grid** — хуудасны ерөнхий бүтэц, карт сүлжээ
- **Flexbox** — картын дотор, товчны эгнээ, дүрс+текст

Хоёрын хооронд сонгох шаардлагагүй. Аль давхаргад аль нь тохирохыг бод.

### Хуучин аргууд

`float` болон `table` ашиглан байршуулдаг байсан. Хуучин кодод
тааралдвал танина, гэхдээ шинээр **бүү бич**. Grid, Flexbox нь бүх
орчин үеийн хөтөчид ажиллана.
""",
            initial_code=css_page(
                title="Хуудасны бүтэц",
                body="""\
<header class="aguulga tolgoi">
  <strong>HTML ба CSS</strong>
  <nav aria-label="Үндсэн цэс">
    <a href="#kartuud">Хичээлүүд</a>
    <a href="#hul">Холбоо барих</a>
  </nav>
</header>

<main class="aguulga">
  <h1>Үндсэн байршуулалтууд</h1>
  <p>
    Агуулга богино ч хөл хэсэг дэлгэцийн доод талд наалдана. Картуудын
    товчнууд нэг шугамд эгнэсэн.
  </p>

  <div class="kartuud" id="kartuud">
    <article class="kart">
      <h2>HTML</h2>
      <p>Хуудасны бүтэц.</p>
      <a class="kart-tovch" href="https://developer.mozilla.org/en-US/docs/Web/HTML">Унших</a>
    </article>
    <article class="kart">
      <h2>CSS</h2>
      <p>Өнгө, хэмжээ, байршуулалт. Flexbox ба Grid-ээр хуудсаа бүтээнэ.</p>
      <a class="kart-tovch" href="https://developer.mozilla.org/en-US/docs/Web/CSS">Унших</a>
    </article>
  </div>
</main>

<footer class="aguulga" id="hul">
  <p>&copy; 2026 HTML ба CSS сургалт</p>
</footer>
""",
                css="""\
*,
*::before,
*::after {
  box-sizing: border-box;
}

/* 1. Бүтэн хуудас — хөл хэсэг доод талд наалдана */
body {
  margin: 0;
  min-height: 100dvh;
  display: grid;
  grid-template-rows: auto 1fr auto;
  font-family: system-ui, sans-serif;
}

/* 2. Голлосон агуулга — нэг мөрөөр */
.aguulga {
  width: min(100% - 32px, 960px);
  margin-inline: auto;
}

/* 3. Карт сүлжээ — медиа асуулгагүй */
.kartuud {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 20px;
}

/* Картын дотор нь Flexbox */
.kart {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 16px;
  border: 1px solid #cbd2d9;
  border-radius: 8px;
}

/* Товчийг доод тал руу түлхэнэ — өөр өөр урттай картуудын
   товч нэг шугамд эгнэнэ */
.kart-tovch {
  margin-top: auto;
  align-self: flex-start;
  padding: 8px 16px;
  background-color: teal;
  color: white;
  border-radius: 6px;
  text-decoration: none;
}

/* Толгой хэсэгт Flexbox */
.tolgoi {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
}
""",
            ),
        ),
    ],
)

CSS_LAYOUT_MODULES = [BOX_MODEL, DISPLAY, FLEXBOX, GRID]
