"""Модул 14-15 — Хариуцлагатай дизайн ба CSS дадлага.

Ямар ч дэлгэцэн дээр ажиллах хуудас бичих. Дараа нь үзсэнээ нэгтгэж
дөрвөн бүрэлдэхүүн хэсэг угсарна.
"""

from app.content.html_css.common import css_page
from app.content.types import LessonSpec, ModuleSpec
from app.models.enums import LessonLanguage

CSS = LessonLanguage.CSS

RESPONSIVE = ModuleSpec(
    title="Модул 14 — Хариуцлагатай дизайн",
    description="Гар утаснаас том дэлгэц хүртэл ажиллах хуудас.",
    lessons=[
        LessonSpec(
            title="Viewport ба медиа асуулга",
            slug="viewport-ba-media-asuulga",
            description="Дэлгэцийн хэмжээнээс хамаарч загвар солих.",
            duration=450,
            language=CSS,
            content="""\
### Эхлээд viewport

CSS бичихээсээ өмнө HTML-д энэ мөр байх ёстой:

```html
<meta name="viewport" content="width=device-width, initial-scale=1" />
```

Үүнгүйгээр гар утас нь хуудсыг 980px өргөнтэй гэж үзээд бүхлээр нь
жижигрүүлж харуулна. Медиа асуулга бичсэн ч **ажиллахгүй**.

### Медиа асуулга

```css
@media (max-width: 640px) {
  .hajuu {
    display: none;
  }
}
```

Дотор нь бичсэн дүрэм нь нөхцөл биелэх үед л хэрэглэгдэнэ.

```css
@media (min-width: 768px) { … }   /* 768-аас ӨРГӨН үед */
@media (max-width: 767px) { … }   /* 767-аас НАРИЙН үед */
@media (min-width: 768px) and (max-width: 1023px) { … }
```

### Гар утас эхэндээ (mobile-first)

Суурь загвараа **нарийн дэлгэцэд** бичээд, `min-width`-ээр нэмж өргөтгө:

```css
/* Суурь — гар утас */
.kartuud {
  display: grid;
  gap: 16px;
}

/* Таблет ба түүнээс дээш */
@media (min-width: 768px) {
  .kartuud {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .kartuud {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

Яагаад энэ дараалал вэ:

- Гар утас нь хамгийн **хязгаарлагдмал** орчин — түүнд эхэлж бодвол
  чухал зүйлээ ялгаж сурна
- Гар утасны хөтөч цөөн дүрэм уншина
- Нэмэх нь хасахаас хялбар

### Таслах цэг сонгох

Алдартай төхөөрөмжийн хэмжээг таах хэрэггүй — тэдгээр нь жил бүр
өөрчлөгддөг. **Загвар эвдрэх** газраа таслах цэг тавь.

Цонхоо аажим нарийсгаж үз. Юу нь муухай харагдаж эхэлнэ, тэнд цэг тавь.

Ердийн эхлэл: 640px, 768px, 1024px, 1280px.

### Медиа асуулгагүй хариуцлага

Заримдаа огт хэрэггүй:

```css
.kartuud {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 16px;
}

.aguulga {
  width: min(100% - 32px, 960px);
  margin-inline: auto;
}
```

Хоёулаа дэлгэцийн хэмжээнд өөрөө дасна. **Эхлээд ийм шийдэл байгаа
эсэхийг бод**, дараа нь медиа асуулга бич.

### Бусад асуулгууд

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation: none !important;
    transition: none !important;
  }
}

@media print {
  nav,
  footer {
    display: none;
  }
}
```

Эхнийх нь хөдөлгөөнөөс толгой эргэдэг хэрэглэгчид зориулагдсан.
Хөдөлгөөн нэмэх бүрдээ энэ блокийг бич.
""",
            initial_code=css_page(
                title="Медиа асуулга",
                body="""\
<main class="aguulga">
  <h1>Ямар ч дэлгэцэнд тохирох хуудас</h1>
  <p>
    Цонхоо аажим нарийсгаж, өргөсгөж үзээрэй. 768px ба 1024px дээр
    загвар солигдоно.
  </p>

  <nav aria-label="Хуудасны цэс">
    <ul class="tses">
      <li><a href="#surgaltuud">Сургалтууд</a></li>
      <li><a href="#media-asuulgagui">Медиа асуулгагүй сүлжээ</a></li>
      <li><a href="https://developer.mozilla.org">MDN</a></li>
    </ul>
  </nav>

  <section id="surgaltuud">
    <h2>Сургалтууд</h2>
    <p>Гар утсанд нэг, таблетад хоёр, том дэлгэцэд гурван багана.</p>

    <div class="kartuud">
      <article>
        <h3>HTML</h3>
        <p>Хуудасны бүтэц: гарчиг, жагсаалт, холбоос.</p>
      </article>
      <article>
        <h3>CSS</h3>
        <p>Өнгө, фонт, зай ба байршуулалт.</p>
      </article>
      <article>
        <h3>JavaScript</h3>
        <p>Хуудсанд үйлдэл нэмэх хэл.</p>
      </article>
      <article>
        <h3>Python</h3>
        <p>Анхлан суралцагчдад ээлтэй хэл.</p>
      </article>
      <article>
        <h3>SQL</h3>
        <p>Өгөгдлийн сангаас мэдээлэл асуух.</p>
      </article>
      <article>
        <h3>Git</h3>
        <p>Кодынхоо түүхийг хадгалах.</p>
      </article>
    </div>
  </section>

  <aside class="hajuu">
    <h2>Нэмэлт зөвлөгөө</h2>
    <p>
      Энэ хэсэг зөвхөн 1024px ба түүнээс өргөн дэлгэцэд харагдана. Гар
      утсанд зай бага тул нуусан.
    </p>
  </aside>

  <section id="media-asuulgagui">
    <h2>Медиа асуулгагүй сүлжээ</h2>
    <p>Багана бүр дор хаяж 260px. Хэдэн багана багтахыг хөтөч өөрөө тооцно.</p>

    <div class="uur-kartuud">
      <article>
        <h3>auto-fit</h3>
        <p>Багтах хэмжээгээрээ багана үүсгэнэ.</p>
      </article>
      <article>
        <h3>min()</h3>
        <p>Агуулга 960px-ээс өргөсөхгүй, жижиг дэлгэцэд захаас зай үлдэнэ.</p>
      </article>
      <article>
        <h3>Хөдөлгөөн</h3>
        <p>Хөдөлгөөн багасгах тохиргоотой хэрэглэгчид хөдөлгөөн бараг мэдрэгдэхгүй.</p>
      </article>
    </div>
  </section>
</main>
""",
                css="""\
/* Гар утас эхэндээ: суурь загвар нь НАРИЙН дэлгэцэд зориулагдана */
.kartuud {
  display: grid;
  gap: 16px;
}

.hajuu {
  display: none;
}

.tses {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

/* Таблет — min-width-ээр НЭМЖ өргөтгөнө */
@media (min-width: 768px) {
  .kartuud {
    grid-template-columns: repeat(2, 1fr);
  }

  .tses {
    flex-direction: row;
    gap: 24px;
  }
}

/* Том дэлгэц */
@media (min-width: 1024px) {
  .kartuud {
    grid-template-columns: repeat(3, 1fr);
  }

  .hajuu {
    display: block;
  }
}

/* Медиа асуулга ОГТ хэрэггүй хувилбарууд */
.uur-kartuud {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 16px;
}

.aguulga {
  width: min(100% - 32px, 960px);
  margin-inline: auto;
}

/* Хөдөлгөөнөөс толгой эргэдэг хэрэглэгчид зориулж */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
""",
            ),
        ),
        LessonSpec(
            title="Гар утасны байршуулалт",
            slug="gar-utasnii-baiguulalt",
            description="Нарийн дэлгэцэд юуг эрэмбэлэх вэ.",
            duration=450,
            language=CSS,
            content="""\
Гар утсан дээр зай бага, хуруу нь хулгана шиг нарийн биш.

### Хүрэх талбай

Дарж болох зүйл **дор хаяж 44 × 44 пиксел** байх ёстой:

```css
.tovch,
.tses a {
  min-height: 44px;
  display: inline-flex;
  align-items: center;
  padding-inline: 16px;
}
```

Жижиг холбоос нь хуруугаараа онох боломжгүй бөгөөд хэрэглэгч буруу
зүйл дарна.

### Нэг багана

Нарийн дэлгэцэнд бараг бүх зүйл нэг багана болно:

```css
.baiguulalt {
  display: grid;
  gap: 16px;
}

@media (min-width: 768px) {
  .baiguulalt {
    grid-template-columns: 240px 1fr;
  }
}
```

### Цэсийг хумих

Хэвтээ цэс багтахгүй бол:

```css
.tses {
  display: flex;
  flex-direction: column;
}

@media (min-width: 768px) {
  .tses {
    flex-direction: row;
  }
}
```

JavaScript-гүйгээр нээгддэг цэс хийх бол `<details>` ашиглаж болно:

```html
<details class="hoto-tses">
  <summary>Цэс</summary>
  <nav>…</nav>
</details>
```

### Хэвтээ гүйлтээс сэргийл

Хуудас хэвтээгээр гүйлгэгдэж байвал ямар нэг зүйл дэлгэцээс халиж
байна. Хамгийн түгээмэл шалтгаанууд:

| Шалтгаан | Засвар |
|---|---|
| Том зураг | `img { max-width: 100%; }` |
| Тогтмол `width` | `max-width` болго |
| Урт үг, холбоос | `overflow-wrap: break-word;` |
| Хүснэгт | Саванд нь `overflow-x: auto;` |

```css
img,
video {
  max-width: 100%;
  height: auto;
}

body {
  overflow-wrap: break-word;
}

.husnegt-sav {
  overflow-x: auto;
}
```

### Зайг багасга

Том дэлгэцийн 64px зай нь гар утсанд хэт их. Уян хатан утга ашигла:

```css
.heseg {
  padding-block: clamp(24px, 6vw, 64px);
}
```

`clamp(доод, дуртай, дээд)` нь дэлгэцтэй хамт өсөх боловч хязгаараас
хэтрэхгүй.

### Юуг нуух вэ

> Гар утсан дээр агуулгыг **нуухаас** илүү **дараалуулах** нь дээр.
> Хэрэглэгч жижиг дэлгэцтэй байх нь тэд бага мэдээлэл хүсч байна гэсэн
> үг биш.

Чимэглэлийн зураг, хоёрдогч навигацийг нуух нь зүйтэй. Гол агуулгыг
хэзээ ч бүү нуу.
""",
            initial_code=css_page(
                title="Гар утасны байршуулалт",
                body="""\
<header class="heseg">
  <h1>Хариуцлагатай дизайны сургалт</h1>

  <nav aria-label="Үндсэн цэс">
    <ul class="tses">
      <li><a href="#tovchoo">Товчоо</a></li>
      <li><a href="#huvaari">Хуваарь</a></li>
      <li><a href="#eh-survalj">Эх сурвалж</a></li>
    </ul>
  </nav>
</header>

<main>
  <div class="baiguulalt heseg">
    <aside>
      <h2>Хичээлүүд</h2>
      <ol>
        <li>Viewport ба медиа асуулга</li>
        <li>Гар утасны байршуулалт</li>
        <li>Том дэлгэцийн байршуулалт</li>
      </ol>
    </aside>

    <section id="tovchoo">
      <h2>Товчоо</h2>
      <p>
        Гар утсан дээр зай бага, хуруу нь хулгана шиг нарийн биш. Энэ
        сургалтаар нарийн дэлгэцэд тохирох хуудас бичиж сурна.
      </p>
      <img src="/logos/html_css.png" alt="HTML ба CSS сургалтын лого" width="416" height="418" />
      <p><button class="tovch" type="button">Бүртгүүлэх</button></p>
    </section>
  </div>

  <section class="heseg" id="huvaari">
    <h2>Хуваарь</h2>
    <div class="husnegt-sav">
      <table>
        <caption>Аравдугаар сарын хичээлүүд</caption>
        <thead>
          <tr>
            <th>Өдөр</th>
            <th>Гараг</th>
            <th>Цаг</th>
            <th>Сэдэв</th>
            <th>Танхим</th>
            <th>Даалгавар</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><time datetime="2026-10-05">5</time></td>
            <td>Даваа</td>
            <td><time datetime="18:00">18:00</time></td>
            <td>Viewport</td>
            <td>301</td>
            <td>Медиа асуулга бичих</td>
          </tr>
          <tr>
            <td><time datetime="2026-10-07">7</time></td>
            <td>Лхагва</td>
            <td><time datetime="18:00">18:00</time></td>
            <td>Гар утас</td>
            <td>301</td>
            <td>Цэсийг хумих</td>
          </tr>
          <tr>
            <td><time datetime="2026-10-09">9</time></td>
            <td>Баасан</td>
            <td><time datetime="18:00">18:00</time></td>
            <td>Том дэлгэц</td>
            <td>305</td>
            <td>Хариуцлагатай хуудас</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>

  <section class="heseg" id="eh-survalj">
    <h2>Эх сурвалж</h2>
    <p>Урт холбоос ч дэлгэцээс халихгүй:</p>
    <p>
      <a href="https://developer.mozilla.org/docs/Web/CSS/overflow-wrap">https://developer.mozilla.org/docs/Web/CSS/overflow-wrap</a>
    </p>
  </section>
</main>
""",
                css="""\
*,
*::before,
*::after {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: system-ui, sans-serif;
  /* Урт үг, холбоосыг таслаж хэвтээ гүйлтээс сэргийлнэ */
  overflow-wrap: break-word;
}

/* Зураг дэлгэцээс халихгүй */
img,
video {
  max-width: 100%;
  height: auto;
}

/* Хүрэх талбай дор хаяж 44px */
.tovch,
.tses a {
  min-height: 44px;
  display: inline-flex;
  align-items: center;
  padding-inline: 16px;
}

/* Суурь: нэг багана */
.baiguulalt {
  display: grid;
  gap: 16px;
}

.tses {
  display: flex;
  flex-direction: column;
  gap: 4px;
  list-style: none;
  padding: 0;
}

/* Зай нь дэлгэцтэй хамт өснө, гэхдээ хязгаараас хэтрэхгүй */
.heseg {
  padding-block: clamp(24px, 6vw, 64px);
  padding-inline: clamp(16px, 4vw, 32px);
}

/* Хүснэгт нь саванд нь гүйлгэгдэнэ */
.husnegt-sav {
  overflow-x: auto;
}

@media (min-width: 768px) {
  .baiguulalt {
    grid-template-columns: 240px 1fr;
    gap: 32px;
  }

  .tses {
    flex-direction: row;
    gap: 24px;
  }
}
""",
            ),
        ),
        LessonSpec(
            title="Том дэлгэцийн байршуулалт",
            slug="tom-delgetsiin-baiguulalt",
            description="Өргөн дэлгэцэнд зайг хэрхэн зарцуулах вэ.",
            duration=450,
            language=CSS,
            content="""\
Том дэлгэц дээрх асуудал нь зай **дутагдах** биш, **илүүдэх**.

### Хэт өргөн текст бүү болго

```css
.aguulga {
  max-width: 65ch;
}
```

2000px өргөн дэлгэц дээр мөр бүтнээр сунавал нүд мөрийн эхлэлийг олж
чадахгүй.

### Агуулгыг голлуул

```css
.sav {
  width: min(100% - 48px, 1200px);
  margin-inline: auto;
}
```

### Илүү зайг баганад зарцуул

```css
.niitlel {
  display: grid;
  gap: 24px;
}

@media (min-width: 1024px) {
  .niitlel {
    grid-template-columns: 1fr 280px;
  }
}
```

Нарийн дэлгэцэд нэг багана, өргөн дэлгэцэд агуулга + хажуугийн хэсэг.

### Уян хатан утгууд

Таслах цэг бүрт тоо бичихийн оронд:

```css
h1 {
  font-size: clamp(1.75rem, 4vw + 1rem, 3rem);
}

.heseg {
  padding-block: clamp(32px, 8vw, 96px);
}
```

`4vw + 1rem` дотор `rem` байгаа нь чухал: хэрэглэгч фонтоо томруулсан
бол хэмжээ дагаж өснө. Зөвхөн `vw` бичвэл тэр тохиргоо үл тоомсорлогдоно.

### Сүлжээний хамгийн их багана

`auto-fit` нь өргөн дэлгэцэнд хэт олон нарийн багана үүсгэж болно:

```css
.kartuud {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 20px;
  /* Сав өөрөө хязгаартай тул багана нь хэт нарийсахгүй */
  max-width: 1200px;
  margin-inline: auto;
}
```

### Хоосон зайнаас бүү ай

Эхлэгчид өргөн дэлгэцийг «дүүргэх» гэж оролддог. Хоосон зай нь дизайны
хэрэгсэл — агуулгыг амьсгалуулж, чухал зүйлийг ялгаруулна.

### Шалгах арга

Хөгжүүлэгчийн хэрэгслийн төхөөрөмжийн горим (`Ctrl + Shift + M`) нь
өөр өөр хэмжээг дуурайна. Гэхдээ хамгийн найдвартай нь: **цонхны ирмэгээс
аажим чирж** үзэх. Юу эвдэрч байгаа нь шууд харагдана.
""",
            initial_code=css_page(
                title="Том дэлгэц",
                body="""\
<div class="sav">
  <header class="heseg">
    <h1>Өргөн дэлгэцэнд зайг зөв зарцуулах</h1>
    <p>Том дэлгэц дээрх асуудал нь зай дутагдах биш, илүүдэх.</p>
  </header>

  <div class="niitlel">
    <article class="niitleliin-tekst">
      <h2>Хэт урт мөр</h2>
      <p>
        2000px өргөн дэлгэц дээр мөр бүтнээр сунавал нүд дараагийн мөрийн
        эхлэлийг олж чадахгүй. Мөрийг 65 орчим тэмдэгтээр хязгаарлавал
        уншихад хялбар болно. Энэ догол мөр том дэлгэцэд ч гэсэн хэт
        сунахгүй.
      </p>
      <h2>Хоосон зайнаас бүү ай</h2>
      <p>
        Эхлэгчид өргөн дэлгэцийг «дүүргэх» гэж оролддог. Хоосон зай нь
        дизайны хэрэгсэл — агуулгыг амьсгалуулж, чухал зүйлийг ялгаруулна.
      </p>
      <p>
        Цонхоо 1024px-ээс өргөн болгоод үзээрэй: хажуугийн хэсэг баруун
        талд гарч ирнэ.
      </p>
    </article>

    <aside>
      <h2>Товчхон</h2>
      <ul>
        <li>Агуулгыг голлуул</li>
        <li>Мөрийг богино байлга</li>
        <li>Илүү зайг баганад зарцуул</li>
      </ul>
    </aside>
  </div>

  <section class="heseg">
    <h2>Бусад нийтлэл</h2>
    <div class="kartuud">
      <article>
        <h3>Viewport ба медиа асуулга</h3>
        <p>Дэлгэцийн хэмжээнээс хамаарч загвар солих.</p>
      </article>
      <article>
        <h3>Гар утасны байршуулалт</h3>
        <p>Нарийн дэлгэцэд юуг эрэмбэлэх вэ.</p>
      </article>
      <article>
        <h3>Хариуцлагатай вэбсайт</h3>
        <p>Толгой, хажуу, агуулга, хөл бүхий бүтэн бүтэц.</p>
      </article>
    </div>
  </section>
</div>
""",
                css="""\
/* Агуулгыг голлуулах */
.sav {
  width: min(100% - 48px, 1200px);
  margin-inline: auto;
}

/* Текстийн мөр хэт урт болохоос сэргийлнэ */
.niitleliin-tekst {
  max-width: 65ch;
}

/* Уян хатан хэмжээ: rem орсон тул хэрэглэгчийн
   фонтын тохиргоог дагана */
h1 {
  font-size: clamp(1.75rem, 4vw + 1rem, 3rem);
  line-height: 1.15;
}

h2 {
  font-size: clamp(1.35rem, 2vw + 0.8rem, 2rem);
}

.heseg {
  padding-block: clamp(32px, 8vw, 96px);
}

/* Нарийн дэлгэцэд нэг багана */
.niitlel {
  display: grid;
  gap: 24px;
}

/* Өргөн дэлгэцэд агуулга + хажуугийн хэсэг */
@media (min-width: 1024px) {
  .niitlel {
    grid-template-columns: minmax(0, 1fr) 280px;
    gap: 48px;
  }
}

/* Сав нь хязгаартай тул багана хэт нарийсахгүй */
.kartuud {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 20px;
  max-width: 1200px;
  margin-inline: auto;
}
""",
            ),
        ),
    ],
)

CSS_PRACTICE = ModuleSpec(
    title="Модул 15 — CSS дадлага",
    description="Бодит бүрэлдэхүүн хэсгүүдийг бичнэ.",
    lessons=[
        LessonSpec(
            title="Дадлага — Навигацийн мөр",
            slug="navigatsiin-mur",
            description="Лого, цэс, идэвхтэй холбоос, гар утасны хувилбар.",
            duration=600,
            language=CSS,
            content="""\
Бараг бүх сайтад байдаг хэсэг. Flexbox-ийн сонгодог хэрэглээ.

### Бүтэц

```html
<header class="tolgoi">
  <a class="logo" href="/">MedlegHub</a>

  <nav aria-label="Үндсэн цэс">
    <ul class="tses">
      <li><a href="/" aria-current="page">Нүүр</a></li>
      <li><a href="/courses">Сургалт</a></li>
    </ul>
  </nav>
</header>
```

### Гурван шаардлага

1. Лого зүүн, цэс баруун → `justify-content: space-between`
2. Босоогоор голд → `align-items: center`
3. Гар утсанд доош дараалах → `flex-wrap` эсвэл медиа асуулга

### Жагсаалтын цэгийг авах

```css
.tses {
  list-style: none;
  margin: 0;
  padding: 0;
}
```

Гурвуулаа хэрэгтэй — хөтөч гурвуулангид нь анхдагч утга өгдөг.

### Идэвхтэй холбоос

HTML-д `aria-current="page"` бичсэн бол CSS-ээр шууд сонгоно:

```css
.tses a[aria-current="page"] {
  color: teal;
  border-bottom: 2px solid currentColor;
}
```

Нэмэлт класс бичих шаардлагагүй бөгөөд дэлгэц уншигчид ч мэдэгдэнэ.

### `currentColor`

`color`-ийн одоогийн утгыг заана. Өнгө солиход хүрээ нь дагаж солигдоно —
хоёр газарт засах шаардлагагүй.

### Naалдмал толгой

```css
.tolgoi {
  position: sticky;
  top: 0;
  z-index: 10;
  background-color: white;
}
```

Дэвсгэрийн өнгийг **заавал** өг — үгүй бол доогуур нь агуулга харагдана.

### Даалгавар

1. Цэсэнд дөрөв дэх холбоос нэмээрэй.
2. Хулгана дээгүүр барихад өнгө солигдох `:hover` нэмээрэй.
3. 640px-ээс нарийн үед цэсийг доош дараалуулаарай.
""",
            initial_code=css_page(
                title="Навигацийн мөр",
                body="""\
<header class="tolgoi">
  <a class="logo" href="#nuur">Medleghub</a>

  <nav aria-label="Үндсэн цэс">
    <ul class="tses">
      <li><a href="#nuur" aria-current="page">Нүүр</a></li>
      <li><a href="#surgalt">Сургалт</a></li>
      <li><a href="#tuhai">Тухай</a></li>
    </ul>
  </nav>
</header>

<main>
  <section id="nuur">
    <h1>Програмчлалыг монгол хэлээр сур</h1>
    <p>Видео хичээл, хөтөч дээрх засварлагч, дасгал — бүгд нэг дор.</p>
    <p>Хуудсыг доош гүйлгээд үзээрэй: толгой нь дээд талд наалдаж үлдэнэ.</p>
  </section>

  <section id="surgalt">
    <h2>Сургалт</h2>
    <p>HTML ба CSS, JavaScript, Python, C/C++, SQL, Git.</p>
    <p>Хичээл бүр богино видео, тайлбар, шууд шалгагддаг дасгалтай.</p>
    <p>Эхний модулиуд үнэгүй.</p>
  </section>

  <section id="tuhai">
    <h2>Тухай</h2>
    <p>Medleghub нь програмчлалыг эх хэлээрээ сурахыг хүссэн хүмүүст зориулсан.</p>
    <p>Юу ч суулгах шаардлагагүй: кодоо хөтөч дээрээ бичиж, үр дүнг шууд харна.</p>
  </section>
</main>
""",
                css="""\
*,
*::before,
*::after {
  box-sizing: border-box;
}

:root {
  --undsen: #0f766e;
  --tekst: #1f2933;
  --huree: #e4e7eb;
}

body {
  margin: 0;
  font-family: system-ui, sans-serif;
  color: var(--tekst);
}

/* Наалдмал толгой — дэвсгэрийн өнгө ЗААВАЛ */
.tolgoi {
  position: sticky;
  top: 0;
  z-index: 10;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px 24px;
  padding: 12px clamp(16px, 4vw, 32px);
  background-color: white;
  border-bottom: 1px solid var(--huree);
}

.logo {
  font-weight: 700;
  font-size: 1.25rem;
  color: var(--undsen);
  text-decoration: none;
  flex-shrink: 0;
}

/* Жагсаалтын анхдагч утгыг гурвууланг нь авна */
.tses {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 4px 8px;
}

.tses a {
  display: inline-flex;
  align-items: center;
  min-height: 44px;
  padding-inline: 12px;
  color: inherit;
  text-decoration: none;
  border-radius: 6px;
}

.tses a:hover {
  background-color: #f5f7fa;
}

.tses a:focus-visible {
  outline: 2px solid var(--undsen);
  outline-offset: 2px;
}

/* Идэвхтэй холбоос — нэмэлт класс шаардлагагүй.
   currentColor нь дээрх color-ийг дагана. */
.tses a[aria-current="page"] {
  color: var(--undsen);
  font-weight: 600;
  box-shadow: inset 0 -2px 0 currentColor;
}

/* Агуулга толгойтой ижил захын зайтай */
main {
  padding-inline: clamp(16px, 4vw, 32px);
}

@media (max-width: 640px) {
  .tolgoi {
    flex-direction: column;
    align-items: flex-start;
  }
}
""",
            ),
        ),
        LessonSpec(
            title="Дадлага — Картын бүрэлдэхүүн",
            slug="kartiin-bureldehuun",
            description="Зураг, гарчиг, текст, товчтой дахин ашиглах карт.",
            duration=600,
            language=CSS,
            content="""\
Карт нь дэлгүүр, блог, самбар бүрт тааралдана.

### Бүтэц

```html
<article class="kart">
  <img class="kart-zurag" src="…" alt="…" />

  <div class="kart-bie">
    <h3 class="kart-garchig">Гарчиг</h3>
    <p class="kart-tekst">Тайлбар.</p>
    <a class="kart-tovch" href="#">Дэлгэрэнгүй</a>
  </div>
</article>
```

### Товчийг доод талд эгнүүлэх

Өөр өөр урттай картуудын товч нэг шугамд байх ёстой:

```css
.kart {
  display: flex;
  flex-direction: column;
}

.kart-bie {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.kart-tovch {
  margin-top: auto;
}
```

`margin-top: auto` нь үлдсэн зайг бүгдийг иднэ, товчийг доош түлхэнэ.
Энэ нь картыг эмх цэгцтэй харагдуулах хамгийн жижиг ч хамгийн мэдэгдэхүйц
дэлгэрэнгүй зүйл.

### Зургийн харьцаа

```css
.kart-zurag {
  aspect-ratio: 16 / 9;
  object-fit: cover;
  width: 100%;
}
```

`object-fit: cover` нь зургийг **сунгахгүйгээр** нүхийг дүүргэнэ. Илүү
хэсэг нь тайрагдана. Үүнгүй бол өөр өөр хэмжээтэй зурагнууд картыг
эвдэнэ.

### Бүхэл картыг дарах боломжтой болгох

```css
.kart {
  position: relative;
}

.kart-garchig a::after {
  content: "";
  position: absolute;
  inset: 0;
}
```

Холбоос нь семантикийн хувьд гарчигт хэвээр үлдэнэ (дэлгэц уншигч зөв
уншина) ч хэрэглэгч картын хаана ч дарж болно.

### Сүүдэр ба хөдөлгөөн

```css
.kart {
  transition: box-shadow 150ms, transform 150ms;
}

.kart:hover {
  box-shadow: 0 4px 12px rgb(0 0 0 / 10%);
  transform: translateY(-2px);
}
```

Хөдөлгөөнийг **богино** байлга. 150-250ms хангалттай.

### Даалгавар

1. Картад үнэ эсвэл шошгоны хэсэг нэмээрэй.
2. Картуудыг `auto-fit` сүлжээнд байрлуулаарай.
3. Хөдөлгөөнийг `prefers-reduced-motion` дотор унтраагаарай.
""",
            initial_code=css_page(
                title="Картын бүрэлдэхүүн",
                body="""\
<main>
  <h1>MDN дээрх гарын авлага</h1>

  <div class="kartuud">
    <article class="kart">
      <img class="kart-zurag" src="/logos/html_css.png" alt="HTML ба CSS-ийн лого" width="416" />
      <div class="kart-bie">
        <h2 class="kart-garchig">
          <a href="https://developer.mozilla.org/docs/Web/HTML">HTML</a>
        </h2>
        <p class="kart-tekst">Хуудасны бүтэц: гарчиг, жагсаалт, холбоос.</p>
        <a class="kart-tovch" href="https://developer.mozilla.org/docs/Web/HTML">Дэлгэрэнгүй</a>
      </div>
    </article>

    <article class="kart">
      <img class="kart-zurag" src="/logos/html_css.png" alt="HTML ба CSS-ийн лого" width="416" />
      <div class="kart-bie">
        <h2 class="kart-garchig">
          <a href="https://developer.mozilla.org/docs/Web/CSS">CSS</a>
        </h2>
        <p class="kart-tekst">
          Өнгө, фонт, зай ба байршуулалт. Flexbox, Grid-ээр элементүүдийг
          эгнүүлж, медиа асуулгаар дэлгэц бүрт тохируулна.
        </p>
        <a class="kart-tovch" href="https://developer.mozilla.org/docs/Web/CSS">Дэлгэрэнгүй</a>
      </div>
    </article>

    <article class="kart">
      <img class="kart-zurag" src="/logos/c.png" alt="C ба C++-ийн лого" width="256" />
      <div class="kart-bie">
        <h2 class="kart-garchig">
          <a href="https://developer.mozilla.org/docs/WebAssembly">WebAssembly</a>
        </h2>
        <p class="kart-tekst">C, C++ кодыг хөтөч дээр хурдан ажиллуулна.</p>
        <a class="kart-tovch" href="https://developer.mozilla.org/docs/WebAssembly">Дэлгэрэнгүй</a>
      </div>
    </article>
  </div>
</main>
""",
                css="""\
*,
*::before,
*::after {
  box-sizing: border-box;
}

:root {
  --undsen: #0f766e;
  --huree: #e4e7eb;
  --buden: #616e7c;
}

/* Картууд — медиа асуулгагүй сүлжээ */
.kartuud {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 20px;
  max-width: 1100px;
  margin-inline: auto;
  padding: 20px;
}

.kart {
  position: relative;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border: 1px solid var(--huree);
  border-radius: 10px;
  background-color: white;
  transition:
    box-shadow 150ms ease,
    transform 150ms ease;
}

.kart:hover {
  box-shadow: 0 4px 12px rgb(0 0 0 / 10%);
  transform: translateY(-2px);
}

/* Зургийг сунгахгүйгээр нүхийг дүүргэнэ */
.kart-zurag {
  width: 100%;
  aspect-ratio: 16 / 9;
  object-fit: cover;
}

.kart-bie {
  display: flex;
  flex-direction: column;
  flex: 1;
  gap: 8px;
  padding: 16px;
}

.kart-garchig {
  margin: 0;
  font-size: 1.125rem;
}

.kart-tekst {
  margin: 0;
  color: var(--buden);
}

/* Товчийг доод тал руу түлхэнэ — картууд өөр өөр урттай ч
   товч нь нэг шугамд эгнэнэ */
.kart-tovch {
  margin-top: auto;
  align-self: flex-start;
  padding: 8px 16px;
  border-radius: 6px;
  background-color: var(--undsen);
  color: white;
  text-decoration: none;
}

/* Бүхэл картыг дарж болно, холбоос нь гарчигт хэвээр */
.kart-garchig a::after {
  content: "";
  position: absolute;
  inset: 0;
}

@media (prefers-reduced-motion: reduce) {
  .kart {
    transition: none;
  }

  .kart:hover {
    transform: none;
  }
}
""",
            ),
        ),
        LessonSpec(
            title="Дадлага — Нүүр хуудас",
            slug="nuur-huudas",
            description="Баатар хэсэг, боломжууд, уриалга.",
            duration=660,
            language=CSS,
            content="""\
Бүтээгдэхүүн танилцуулах нэг хуудас (landing page).

### Ердийн хэсгүүд

```text
tolgoi     навигаци
baatar     том гарчиг + уриалга
bolomj     гурван боломжийн карт
unelgee    хэрэглэгчийн сэтгэгдэл
uriala     сүүлийн уриалга
hul        холбоосууд
```

### Баатар хэсэг (hero)

Хуудсанд орогчийн эхэлж харах зүйл. Гурван зүйлд хариулна:

1. Энэ юу вэ
2. Надад юугаараа хэрэгтэй вэ
3. Дараа нь юу хийх вэ

```css
.baatar {
  display: grid;
  place-items: center;
  text-align: center;
  gap: 16px;
  padding-block: clamp(48px, 12vw, 120px);
}
```

Энд текстийг голлуулах нь **зөв** — богино учраас.

### Хэсгийн хэмнэл

Хэсэг бүрт ижил зай өгвөл хуудас цэгцтэй харагдана:

```css
.heseg {
  padding-block: clamp(48px, 10vw, 96px);
}

.heseg + .heseg {
  border-top: 1px solid var(--huree);
}
```

### Уриалгын товч

Гол товч нь хуудсан дээрх хамгийн ялгаатай зүйл байх ёстой:

```css
.uriala-tovch {
  display: inline-flex;
  align-items: center;
  min-height: 48px;
  padding-inline: 28px;
  background-color: var(--undsen);
  color: white;
  border-radius: 8px;
  font-weight: 600;
  text-decoration: none;
}
```

Хоёрдогч товчийг зөвхөн хүрээтэй болго — хоёр товч ижил хүчтэй бол
хэрэглэгч алийг нь сонгохоо мэдэхгүй.

### Хэсгийн дэвсгэр

Ээлжлэн дэвсгэр өгөх нь хэсгүүдийг ялгаруулна:

```css
.heseg-sereg {
  background-color: #f5f7fa;
}
```

### Даалгавар

1. Хэрэглэгчийн сэтгэгдлийн хэсэг нэмээрэй.
2. Баатар хэсэгт дэвсгэр өнгө эсвэл градиент нэмээрэй.
3. Гурван боломжийн картыг гар утсанд нэг багана болгоорой.
""",
            initial_code=css_page(
                title="Нүүр хуудас",
                body="""\
<main>
  <section class="baatar sav">
    <h1>Програмчлалыг монгол хэлээр сур</h1>
    <p>
      Видео хичээл, хөтөч дээрх засварлагч, шууд шалгагддаг дасгал — бүгд
      нэг дор. Эхний хичээлүүд үнэгүй.
    </p>
    <div>
      <a class="uriala-tovch" href="#surgaltuud">Хичээл сонгох</a>
      <a class="hoyordogch-tovch" href="#bolomjuud">Дэлгэрэнгүй</a>
    </div>
  </section>

  <section class="heseg heseg-sereg" id="bolomjuud">
    <div class="sav">
      <h2>Яагаад Medleghub гэж?</h2>
      <div class="bolomjuud">
        <article class="bolomj">
          <h3>Монгол хэлээр</h3>
          <p>Бүх хичээл, тайлбар, дасгал монгол хэл дээр.</p>
        </article>
        <article class="bolomj">
          <h3>Юу ч суулгахгүй</h3>
          <p>Кодоо хөтөч дээрээ бичиж, үр дүнг шууд харна.</p>
        </article>
        <article class="bolomj">
          <h3>Шууд шалгана</h3>
          <p>Дасгал бүр тесттэй тул кодоо илгээмэгц зөв эсэхийг мэднэ.</p>
        </article>
      </div>
    </div>
  </section>

  <section class="heseg" id="surgaltuud">
    <div class="sav">
      <h2>Сургалтууд</h2>
      <ul>
        <li>HTML ба CSS</li>
        <li>JavaScript</li>
        <li>Python</li>
        <li>C/C++</li>
        <li>SQL</li>
      </ul>
    </div>
  </section>
</main>
""",
                css="""\
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
  --devsger: #f5f7fa;
}

body {
  margin: 0;
  font-family: system-ui, sans-serif;
  color: var(--tekst);
  line-height: 1.6;
}

.sav {
  width: min(100% - 32px, 1100px);
  margin-inline: auto;
}

/* Хэсэг бүрт ижил хэмнэл */
.heseg {
  padding-block: clamp(48px, 10vw, 96px);
}

.heseg-sereg {
  background-color: var(--devsger);
}

/* --- Баатар хэсэг --- */
.baatar {
  display: grid;
  place-items: center;
  text-align: center;
  gap: 16px;
  padding-block: clamp(48px, 12vw, 120px);
}

.baatar h1 {
  margin: 0;
  font-size: clamp(2rem, 5vw + 1rem, 3.5rem);
  line-height: 1.1;
  max-width: 18ch;
}

.baatar p {
  margin: 0;
  max-width: 52ch;
  color: var(--buden);
  font-size: 1.125rem;
}

/* Гол уриалга — хуудсан дээрх хамгийн ялгаатай зүйл */
.uriala-tovch {
  display: inline-flex;
  align-items: center;
  min-height: 48px;
  padding-inline: 28px;
  border-radius: 8px;
  background-color: var(--undsen);
  color: white;
  font-weight: 600;
  text-decoration: none;
}

/* Хоёрдогч товч — зөвхөн хүрээтэй */
.hoyordogch-tovch {
  display: inline-flex;
  align-items: center;
  min-height: 48px;
  padding-inline: 28px;
  border: 1px solid var(--undsen);
  border-radius: 8px;
  color: var(--undsen);
  text-decoration: none;
}

/* --- Боломжууд --- */
.bolomjuud {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 24px;
}

.bolomj h3 {
  margin: 0 0 8px;
}

.bolomj p {
  margin: 0;
  color: var(--buden);
}
""",
            ),
        ),
        LessonSpec(
            title="Дадлага — Хариуцлагатай вэбсайт",
            slug="hariutslagatai-vebsait",
            description="Толгой, хажуу, агуулга, хөл бүхий бүтэн бүтэц.",
            duration=720,
            language=CSS,
            content="""\
Бүх үзсэнээ нэгтгэн бүтэн хуудасны бүтэц бичнэ.

### Зорилтот бүтэц

Том дэлгэц:

```text
┌───────────────────────────┐
│         tolgoi            │
├─────────┬─────────────────┤
│  hajuu  │    aguulga      │
├─────────┴─────────────────┤
│          hul              │
└───────────────────────────┘
```

Гар утас: бүгд нэг баганад дараалан.

### Нэрлэсэн талбай ашиглах

Энэ нь байршуулалтыг **уншиж болохоор** болгоно:

```css
.huudas {
  display: grid;
  grid-template-areas:
    "tolgoi"
    "aguulga"
    "hajuu"
    "hul";
  grid-template-rows: auto 1fr auto auto;
  min-height: 100dvh;
}

@media (min-width: 900px) {
  .huudas {
    grid-template-columns: 260px 1fr;
    grid-template-rows: auto 1fr auto;
    grid-template-areas:
      "tolgoi  tolgoi"
      "hajuu   aguulga"
      "hul     hul";
  }
}
```

Гар утсанд хажуугийн хэсгийг **агуулгын дараа** тавьсныг анхаараарай.
HTML-д хүрэхгүйгээр дараалал өөрчиллөө.

### Хөл хэсгийг доод талд наах

`grid-template-rows`-д `1fr` нь агуулгын мөрөнд байгаа тул агуулга богино
байсан ч хөл нь доод талд үлдэнэ.

### Хажуугийн хэсгийг наалдмал болгох

```css
.hajuu {
  position: sticky;
  top: 16px;
  align-self: start;
}
```

`align-self: start` **заавал** — үгүй бол grid хүүхэд нь бүтэн өндөр
сунаж, наалдах зай үлдэхгүй.

### Шалгах жагсаалт

Дуусгахын өмнө:

- Цонхыг 320px хүртэл нарийсгахад хэвтээ гүйлт үүсэхгүй
- Tab дарж бүх холбоос, товчоор дамжиж болно, фокус нь харагдана
- Текст ба дэвсгэрийн ялгарал 4.5:1-ээс дээш
- Зураг бүр `alt`-тай
- Гарчгийн дараалал алгасаагүй

### Даалгавар

1. Хажуугийн хэсэгт холбоосын жагсаалт нэмээрэй.
2. Хөл хэсгийг гурван баганад хуваагаарай.
3. Харанхуй горим нэмээрэй (`prefers-color-scheme: dark`).
""",
            initial_code=css_page(
                title="Хариуцлагатай вэбсайт",
                body="""\
<div class="huudas">
  <header class="tolgoi">
    <a href="#ehlel"><strong>Medleghub</strong></a>

    <nav aria-label="Үндсэн цэс">
      <a href="#butets">Бүтэц</a>
      <a href="#shalgah">Жагсаалт</a>
    </nav>
  </header>

  <aside class="hajuu" aria-label="Хажуугийн хэсэг">
    <img src="/logos/html_css.png" alt="HTML ба CSS-ийн лого" width="416" height="418" />
    <p>
      Гар утсанд энэ хэсэг агуулгын <strong>дараа</strong>, том дэлгэцэд
      зүүн талд харагдана — HTML-ийг өөрчлөхгүйгээр.
    </p>
  </aside>

  <main class="aguulga" id="ehlel">
    <h1>Хариуцлагатай вэбсайт</h1>
    <p>Толгой, хажуу, агуулга, хөл бүхий бүтэн бүтэц.</p>

    <h2 id="butets">Бүтэц</h2>
    <p>
      Том дэлгэцэд хажуугийн хэсэг зүүн талд, агуулга баруун талд байна.
      Гар утсанд бүгд нэг баганад дараалана.
    </p>
    <p>
      Агуулга богино байсан ч хөл нь доод талдаа үлдэнэ: агуулгын мөр
      <code>1fr</code> учраас үлдсэн зайг бүгдийг авна.
    </p>

    <h2 id="shalgah">Шалгах жагсаалт</h2>
    <ul>
      <li>Цонхыг 320px хүртэл нарийсгахад хэвтээ гүйлт үүсэхгүй</li>
      <li>Tab дарж бүх холбоос, товчоор дамжиж болно, фокус нь харагдана</li>
      <li>Текст ба дэвсгэрийн ялгарал 4.5:1-ээс дээш</li>
      <li>Зураг бүр <code>alt</code>-тай</li>
      <li>Гарчгийн дараалал алгасаагүй</li>
    </ul>
  </main>

  <footer class="hul">
    <p>© 2026 Medleghub</p>
  </footer>
</div>
""",
                css="""\
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

/* Гар утас: бүгд нэг баганад.
   Хажуугийн хэсэг АГУУЛГЫН ДАРАА — HTML-д хүрэхгүйгээр. */
.huudas {
  display: grid;
  grid-template-areas:
    "tolgoi"
    "aguulga"
    "hajuu"
    "hul";
  grid-template-rows: auto 1fr auto auto;
  min-height: 100dvh;
  gap: 16px;
}

.tolgoi {
  grid-area: tolgoi;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  padding: 12px clamp(16px, 4vw, 32px);
  border-bottom: 1px solid var(--huree);
}

.hajuu {
  grid-area: hajuu;
  padding-inline: clamp(16px, 4vw, 32px);
}

.aguulga {
  grid-area: aguulga;
  padding-inline: clamp(16px, 4vw, 32px);
  max-width: 70ch;
}

.hul {
  grid-area: hul;
  padding: 24px clamp(16px, 4vw, 32px);
  background-color: var(--devsger-2);
  color: var(--buden);
}

/* Том дэлгэц: хажуу зүүн талдаа буцаж ирнэ */
@media (min-width: 900px) {
  .huudas {
    grid-template-columns: 260px 1fr;
    grid-template-rows: auto 1fr auto;
    grid-template-areas:
      "tolgoi  tolgoi"
      "hajuu   aguulga"
      "hul     hul";
    gap: 24px;
  }

  /* align-self: start ЗААВАЛ — үгүй бол бүтэн өндөр сунаж наалдахгүй */
  .hajuu {
    position: sticky;
    top: 16px;
    align-self: start;
  }
}
""",
            ),
        ),
    ],
)

RESPONSIVE_MODULES = [RESPONSIVE, CSS_PRACTICE]
