"""Модул 4-6 — Семантик бүтэц, форм, HTML дадлага.

Утга учиртай бүтэц бичих нь хайлтын систем болон дэлгэц уншигчид хоёуланд
нь тустай. Модул 6-д эхний гурван хуудсаа бүтнээр нь бичнэ.
"""

from app.content.html_css.common import files
from app.content.types import LessonSpec, ModuleSpec
from app.models.enums import LessonLanguage

HTML = LessonLanguage.HTML

SEMANTIC = ModuleSpec(
    title="Модул 4 — Семантик HTML",
    description="Утга учиртай элемент сонгох.",
    lessons=[
        LessonSpec(
            title="Семантик гэж юу вэ?",
            slug="semantik-gej-yu-ve",
            description="Яагаад div биш утгатай элемент сонгох ёстой вэ.",
            duration=400,
            language=HTML,
            content="""\
**Семантик** гэдэг нь элемент нь агуулгынхаа **утгыг** илэрхийлж байхыг
хэлнэ.

Доорх хоёр хуудас яг ижил харагдана:

```html
<!-- Семантик биш -->
<div class="deed">
  <div class="tses">…</div>
</div>
<div class="aguulga">…</div>
<div class="dood">…</div>
```

```html
<!-- Семантик -->
<header>
  <nav>…</nav>
</header>
<main>…</main>
<footer>…</footer>
```

Хоёр дахь нь **хэнд зориулагдсан бэ**:

| Хэн | Юу олж авах вэ |
|---|---|
| Дэлгэц уншигч | «Навигаци», «Үндсэн агуулга» гэж зарлана |
| Хайлтын систем | Аль хэсэг нь гол агуулга болохыг мэднэ |
| Хөтөч | Уншигч горимд зөв хэсгийг гаргана |
| Дараагийн хөгжүүлэгч | Кодыг уншаад л ойлгоно |

### Дэлгэц уншигч хэрхэн ашигладаг вэ

Хараагүй хэрэглэгч хуудсыг дээрээс доош сонсдоггүй. Тэд:

- Гарчгаас гарчиг руу үсэрнэ
- «Үндсэн агуулга руу оч» гэж тушаана
- Навигацийг алгасна

Бүх зүйл `<div>` бол эдгээр товчлол **аль нь ч** ажиллахгүй. Тэд бүхэл
хуудсыг дараалан сонсохоос өөр аргагүй болно.

### Дүрэм

> Утга нь тохирох элемент байвал түүнийг сонго. `<div>`-ийг зөвхөн
> **зөвхөн загварчлалын зорилгоор** бүлэглэх үед ашигла.

```html
<div onclick="…">Хадгалах</div>   <!-- муу -->
<button>Хадгалах</button>          <!-- сайн -->
```

`<button>` бол дарж болох товч (Модул 5-д нарийн үзнэ). Тэр нь
үнэгүйгээр: гараар сонгогдоно, Enter/Space дарахад
ажиллана, дэлгэц уншигч «товч» гэж зарлана. `<div>`-д эдгээрийг бүгдийг
нь гараар нэмэх шаардлагатай — ихэнхдээ мартагддаг.
""",
            initial_code="""\
<!DOCTYPE html>
<html lang="mn">
  <head>
    <meta charset="UTF-8" />
    <title>Семантик бүтэц</title>
  </head>

  <body>
    <!-- Бүх зүйл div байсан бол ижил харагдах байсан.
         Ялгаа нь дэлгэц уншигч болон хайлтын системд илэрнэ. -->
    <header>
      <h1>Миний блог</h1>
      <nav>
        <ul>
          <li><a href="/">Нүүр</a></li>
          <li><a href="/tuhai">Тухай</a></li>
        </ul>
      </nav>
    </header>

    <main>
      <article>
        <h2>Анхны нийтлэл</h2>
        <p>Семантик HTML нь хэнд ч илүү ажил үүсгэхгүй.</p>
      </article>
    </main>

    <footer>
      <p>&copy; 2026 Миний блог</p>
    </footer>
  </body>
</html>
""",
        ),
        LessonSpec(
            title="header, nav, footer",
            slug="header-nav-footer",
            description="Хуудасны дээд ба доод хэсэг, навигаци.",
            duration=400,
            language=HTML,
            content="""\
### `<header>`

Хэсгийн **танилцуулах** хэсэг. Ихэвчлэн лого, гарчиг, навигаци:

```html
<header>
  <h1>MedlegHub</h1>
  <nav>…</nav>
</header>
```

`<header>` нь хуудсанд **нэг л** байх албагүй. `<article>` бүр өөрийн
гэсэн `<header>`-тэй байж болно:

```html
<article>
  <header>
    <h2>Нийтлэлийн гарчиг</h2>
    <p>2026 оны 9-р сарын 13</p>
  </header>
  <p>Агуулга…</p>
</article>
```

### `<nav>`

**Гол** навигацийн холбоосууд. Хуудсан дээрх бүх холбоосыг `<nav>`-д
хийх шаардлагагүй — зөвхөн сайтын үндсэн цэсийг.

```html
<nav aria-label="Үндсэн цэс">
  <ul>
    <li><a href="/">Нүүр</a></li>
    <li><a href="/courses">Сургалт</a></li>
  </ul>
</nav>
```

Хэд хэдэн `<nav>` байвал `aria-label`-аар ялга. Эс бөгөөс дэлгэц уншигч
«навигаци, навигаци» гэж хоёуланг нь ижил нэрлэнэ.

### `<footer>`

Хэсгийн **төгсгөлийн** мэдээлэл: зохиогчийн эрх, холбоо барих, туслах
холбоосууд.

```html
<footer>
  <p>&copy; 2026 MedlegHub</p>
  <a href="/nuutslal">Нууцлалын бодлого</a>
</footer>
```

### Хамтдаа

```html
<body>
  <header>…</header>
  <main>…</main>
  <footer>…</footer>
</body>
```

Энэ гурав нь хуудасны хамгийн түгээмэл араг яс. Дараагийн хичээлд
голыг нь задлана.
""",
            initial_code="""\
<!DOCTYPE html>
<html lang="mn">
  <head>
    <meta charset="UTF-8" />
    <title>header, nav, footer</title>
  </head>

  <body>
    <header>
      <h1>MedlegHub</h1>

      <!-- Хоёр nav байвал aria-label-аар ялгана -->
      <nav aria-label="Үндсэн цэс">
        <ul>
          <li><a href="/">Нүүр</a></li>
          <li><a href="/courses">Сургалт</a></li>
          <li><a href="/tuhai">Тухай</a></li>
        </ul>
      </nav>
    </header>

    <main>
      <article>
        <!-- article өөрийн header-тэй байж болно -->
        <header>
          <h2>Семантик HTML</h2>
          <p><time datetime="2026-09-13">2026 оны 9 сарын 13</time></p>
        </header>

        <p>Нийтлэлийн агуулга.</p>
      </article>
    </main>

    <footer>
      <nav aria-label="Хуудасны доод цэс">
        <a href="/nuutslal">Нууцлал</a>
        <a href="/holbogdoh">Холбогдох</a>
      </nav>
      <p>&copy; 2026 MedlegHub</p>
    </footer>
  </body>
</html>
""",
        ),
        LessonSpec(
            title="main, section, article, aside",
            slug="main-section-article-aside",
            description="Агуулгыг утгаар нь хуваах.",
            duration=420,
            language=HTML,
            content="""\
### `<main>`

Хуудасны **гол** агуулга. Хуудсанд **зөвхөн нэг** байна.

Олон хуудсанд давтагддаг зүйл (цэс, хөл хэсэг) `<main>`-д **орохгүй**.

```html
<main>
  <h1>Сургалтууд</h1>
  …
</main>
```

Дэлгэц уншигч «үндсэн агуулга руу үсэр» гэсэн товчлолтой. Энэ элемент л
түүнийг ажиллуулна.

### `<article>`

**Дангаараа утга агуулах** хэсэг. Өөр газар хуулж тавьсан ч ойлгомжтой
байх ёстой:

- Блогийн нийтлэл
- Мэдээ
- Бүтээгдэхүүний карт
- Сэтгэгдэл

```html
<article>
  <h2>Нийтлэлийн гарчиг</h2>
  <p>Агуулга…</p>
</article>
```

### `<section>`

Сэдвээр нь бүлэглэсэн хэсэг. **Гарчигтай** байх ёстой:

```html
<section>
  <h2>Үнэ</h2>
  <p>…</p>
</section>
```

### `article` уу, `section` уу

Энэ бол хамгийн олон эргэлздэг сонголт. Энгийн шалгуур:

> Энэ хэсгийг өөр сайт руу хуулж тавихад **дангаараа утга агуулах уу**?
> Тийм бол `<article>`. Үгүй бол `<section>`.

Мөн: зөвхөн загварчлахын тулд бүлэглэж байгаа бол хоёулангийнх нь оронд
`<div>` ашигла. `<section>` нь утга илэрхийлдэг тул дэмий бүү хэрэглэ.

### `<aside>`

Гол агуулгатай **шууд холбоогүй** зүйл: зар, холбоотой нийтлэл,
тайлбарын хайрцаг.

```html
<main>
  <article>…</article>

  <aside>
    <h2>Холбоотой нийтлэл</h2>
    <ul>…</ul>
  </aside>
</main>
```

### Бүтэн жишээ

```html
<main>
  <h1>Блог</h1>

  <article>
    <h2>Эхний нийтлэл</h2>

    <section>
      <h3>Оршил</h3>
      <p>…</p>
    </section>
  </article>

  <aside>
    <h2>Зохиогчийн тухай</h2>
  </aside>
</main>
```
""",
            initial_code="""\
<!DOCTYPE html>
<html lang="mn">
  <head>
    <meta charset="UTF-8" />
    <title>Агуулгын бүтэц</title>
  </head>

  <body>
    <header>
      <nav aria-label="Үндсэн цэс"><a href="/">Нүүр</a></nav>
    </header>

    <!-- main нь хуудсанд ЗӨВХӨН НЭГ -->
    <main>
      <h1>Блог</h1>

      <!-- article — дангаараа утга агуулна -->
      <article>
        <h2>Семантик HTML яагаад чухал вэ</h2>

        <!-- section — сэдвээр бүлэглэсэн, гарчигтай -->
        <section>
          <h3>Оршил</h3>
          <p>Элемент бүр утгатай.</p>
        </section>

        <section>
          <h3>Дүгнэлт</h3>
          <p>Тохирох элемент байвал түүнийг сонго.</p>
        </section>
      </article>

      <!-- aside — гол агуулгатай шууд холбоогүй -->
      <aside>
        <h2>Холбоотой нийтлэл</h2>
        <ul>
          <li><a href="#">Хүртээмжийн үндэс</a></li>
        </ul>
      </aside>
    </main>

    <footer><p>&copy; 2026</p></footer>
  </body>
</html>
""",
        ),
    ],
)

FORMS = ModuleSpec(
    title="Модул 5 — Форм (Forms)",
    description="Хэрэглэгчээс мэдээлэл авах.",
    lessons=[
        LessonSpec(
            title="form ба input",
            slug="form-ba-input",
            description="Формын бүтэц, оролтын төрлүүд.",
            duration=450,
            language=HTML,
            content="""\
```html
<form action="/burtgel" method="post">
  <input type="text" name="ner" />
  <button type="submit">Илгээх</button>
</form>
```

### `action` ба `method`

| Шинж чанар | Утга |
|---|---|
| `action` | Өгөгдлийг хаашаа илгээх вэ |
| `method` | `get` (хайлт) эсвэл `post` (өөрчлөлт) |

`get` нь утгыг **хаяганд** бичнэ — хуваалцах, хадгалахад тохиромжтой.
Нууц үг зэрэг мэдрэмтгий зүйлд **хэзээ ч** `get` бүү ашигла.

### `name` — заавал

`name` байхгүй талбарын утга **огт илгээгдэхгүй**. Энэ бол хамгийн олон
тохиолддог алдаа:

```html
<input type="email" id="email" />            <!-- илгээгдэхгүй! -->
<input type="email" id="email" name="email" /> <!-- зөв -->
```

`id` нь шошготой холбоход, `name` нь илгээхэд хэрэгтэй. Хоёулаа бич.

### Оролтын төрлүүд

| `type` | Хэрэглээ |
|---|---|
| `text` | Энгийн текст |
| `email` | Имэйл — гар утсанд @ гарна |
| `password` | Нуугдсан текст |
| `number` | Тоо |
| `tel` | Утас — гар утсанд тоон гар |
| `date` | Огноо сонгогч |
| `checkbox` | Олон сонголт |
| `radio` | Нэг сонголт |
| `file` | Файл хавсаргах |

Зөв `type` сонгох нь гар утсан дээр **зөв гар** гаргаж ирнэ. Имэйл
бичихэд @ хайж тэнэх шаардлагагүй болно.

### radio — ижил `name`

Radio товчнууд ижил `name`-тэй байж л нэг бүлэг болно:

```html
<input type="radio" name="hel" value="mn" /> Монгол
<input type="radio" name="hel" value="en" /> Англи
```

`name` нь өөр байвал хоёуланг нь зэрэг сонгож болно — гарцаагүй алдаа.
""",
            initial_code="""\
<!DOCTYPE html>
<html lang="mn">
  <head>
    <meta charset="UTF-8" />
    <title>Форм ба оролт</title>
  </head>

  <body>
    <h1>Бүртгэлийн маягт</h1>

    <form action="/burtgel" method="post">
      <!-- name БАЙХГҮЙ бол утга илгээгдэхгүй -->
      <p><input type="text" name="ner" placeholder="Нэр" /></p>
      <p><input type="email" name="email" placeholder="Имэйл" /></p>
      <p><input type="password" name="nuuts" placeholder="Нууц үг" /></p>
      <p><input type="tel" name="utas" placeholder="Утас" /></p>
      <p><input type="date" name="ognoo" /></p>

      <!-- radio — ижил name-тэй байж нэг бүлэг болно -->
      <fieldset>
        <legend>Хэл</legend>
        <label><input type="radio" name="hel" value="mn" checked /> Монгол</label>
        <label><input type="radio" name="hel" value="en" /> Англи</label>
      </fieldset>

      <p><label><input type="checkbox" name="zuvshuurul" /> Нөхцөлийг зөвшөөрөх</label></p>

      <button type="submit">Бүртгүүлэх</button>
    </form>
  </body>
</html>
""",
        ),
        LessonSpec(
            title="label ба хүртээмж",
            slug="label-ba-hurteemj",
            description="Талбар бүрт шошго. Яагаад placeholder хангалтгүй вэ.",
            duration=420,
            language=HTML,
            content="""\
Талбар бүр **шошготой** байх ёстой. Хоёр арга бий:

```html
<!-- 1. for нь талбарын id-тай таарна -->
<label for="email">Имэйл</label>
<input type="email" id="email" name="email" />

<!-- 2. Талбарыг доторлоно -->
<label>
  Имэйл
  <input type="email" name="email" />
</label>
```

### Шошго юу өгдөг вэ

- Дэлгэц уншигч талбарт орохад нэрийг нь уншина
- **Шошгон дээр дарахад** талбар идэвхжинэ — жижиг checkbox-ыг олоход
  амархан болно
- Талбарын зорилго тодорхой болно

### `placeholder` нь шошго БИШ

```html
<!-- Муу -->
<input type="email" placeholder="Имэйл" />
```

Яагаад:

| Асуудал | Тайлбар |
|---|---|
| Бичиж эхлэхэд **алга болно** | Хэрэглэгч юу бичиж байгаагаа мартана |
| Өнгө нь бүдэг | Харааны бэрхшээлтэй хүнд уншигдахгүй |
| Зарим дэлгэц уншигч уншихгүй | Талбар нэргүй болно |
| Хоосон талбар дүүрсэн мэт харагдана | Алгасах эрсдэлтэй |

`placeholder`-ийг зөвхөн **жишээ** харуулахад ашигла:

```html
<label for="utas">Утас</label>
<input type="tel" id="utas" name="utas" placeholder="9911-2233" />
```

### `fieldset` ба `legend`

Холбоотой талбаруудыг бүлэглэнэ:

```html
<fieldset>
  <legend>Хүргэлтийн хаяг</legend>
  <label for="hot">Хот</label>
  <input id="hot" name="hot" />
</fieldset>
```

Radio бүлэгт энэ нь **шаардлагатай** — эс бөгөөс сонголтууд юуны тухай
болох нь тодорхойгүй болно.

### Заавал бөглөх талбар

```html
<label for="email">Имэйл <span aria-hidden="true">*</span></label>
<input type="email" id="email" name="email" required />
```

`required` нь дэлгэц уншигчид ч мэдэгдэнэ. Од тэмдэг нь зөвхөн нүдэнд
зориулагдсан тул `aria-hidden` тавьж давхардлыг болиулна.
""",
            initial_code="""\
<!DOCTYPE html>
<html lang="mn">
  <head>
    <meta charset="UTF-8" />
    <title>Шошго ба хүртээмж</title>
  </head>

  <body>
    <h1>Зөв шошготой форм</h1>

    <form action="/burtgel" method="post">
      <!-- 1 дэх арга: for нь id-тай таарна -->
      <p>
        <label for="ner">Нэр</label><br />
        <input type="text" id="ner" name="ner" />
      </p>

      <!-- placeholder нь ЖИШЭЭ харуулна, шошгыг орлохгүй -->
      <p>
        <label for="utas">Утас</label><br />
        <input type="tel" id="utas" name="utas" placeholder="9911-2233" />
      </p>

      <p>
        <label for="email">Имэйл <span aria-hidden="true">*</span></label><br />
        <input type="email" id="email" name="email" required />
      </p>

      <!-- 2 дахь арга: талбарыг доторлоно -->
      <p>
        <label><input type="checkbox" name="sanuulga" /> Мэдээлэл авах</label>
      </p>

      <!-- Radio бүлэгт fieldset ЗААВАЛ хэрэгтэй -->
      <fieldset>
        <legend>Хүргэх цаг</legend>
        <label><input type="radio" name="tsag" value="ugloo" /> Өглөө</label>
        <label><input type="radio" name="tsag" value="oroi" /> Орой</label>
      </fieldset>

      <p><button type="submit">Илгээх</button></p>
    </form>
  </body>
</html>
""",
        ),
        LessonSpec(
            title="textarea, select, button",
            slug="textarea-select-button",
            description="Урт текст, унждаг цэс, товчнууд.",
            duration=420,
            language=HTML,
            content="""\
### `<textarea>`

Олон мөрт текст. `<input>`-ээс ялгаатай нь **хаах шошготой**:

```html
<label for="setgegdel">Сэтгэгдэл</label>
<textarea id="setgegdel" name="setgegdel" rows="5"></textarea>
```

Анхны утгыг `value`-д биш, **шошгуудын хооронд** бичнэ:

```html
<textarea name="tailbar">Урьдчилан бичсэн текст</textarea>
```

Нээх шошгоны дараах хоосон зай, мөр таслалт нь агуулгад **орно**. Тиймээс
хоосон байлгах бол `<textarea></textarea>` гэж нааж бич.

### `<select>`

```html
<label for="hot">Хот</label>
<select id="hot" name="hot">
  <option value="">Сонгоно уу</option>
  <option value="ub">Улаанбаатар</option>
  <option value="darhan" selected>Дархан</option>
</select>
```

`value` илгээгдэнэ, шошгуудын хоорондох текст харагдана. `value` байхгүй
бол текст нь өөрөө илгээгдэнэ.

Бүлэглэх:

```html
<select name="hicheel">
  <optgroup label="Front-end">
    <option>HTML</option>
    <option>CSS</option>
  </optgroup>
  <optgroup label="Back-end">
    <option>Python</option>
  </optgroup>
</select>
```

> Сонголт 5-аас цөөн бол `select`-ийн оронд radio ашиглах нь илүү
> хурдан — бүх сонголт нэг дор харагдана.

### `<button>`

Гурван төрөлтэй:

| `type` | Үйлдэл |
|---|---|
| `submit` | Формыг илгээнэ — **анхдагч** |
| `button` | Юу ч хийхгүй, JavaScript-д зориулна |
| `reset` | Формыг цэвэрлэнэ |

```html
<button type="submit">Хадгалах</button>
<button type="button">Цуцлах</button>
```

> Форм доторх `<button>`-д `type` бичихээ мартвал **submit** болно.
> «Цуцлах» товч дарахад форм илгээгдэх нь ингэж үүсдэг.

`reset` товчийг бараг хэзээ ч бүү тавь — санамсаргүй дарж бүх ажлаа
алдах эрсдэл нь ашгаасаа их.

### `<button>` ба `<input type="submit">`

`<button>` нь дотроо HTML агуулж чадна (дүрс, тод текст). `<input>` нь
зөвхөн энгийн текст авна. Шинэ кодод `<button>` сонго.
""",
            initial_code="""\
<!DOCTYPE html>
<html lang="mn">
  <head>
    <meta charset="UTF-8" />
    <title>textarea, select, button</title>
  </head>

  <body>
    <h1>Санал хүсэлт</h1>

    <form action="/sanal" method="post">
      <p>
        <label for="hot">Хот</label><br />
        <select id="hot" name="hot">
          <option value="">Сонгоно уу</option>
          <option value="ub">Улаанбаатар</option>
          <option value="darhan" selected>Дархан</option>
          <option value="erdenet">Эрдэнэт</option>
        </select>
      </p>

      <p>
        <label for="hicheel">Сонирхож буй сургалт</label><br />
        <select id="hicheel" name="hicheel">
          <optgroup label="Front-end">
            <option>HTML &amp; CSS</option>
            <option>JavaScript</option>
          </optgroup>
          <optgroup label="Back-end">
            <option>Python</option>
          </optgroup>
        </select>
      </p>

      <p>
        <label for="setgegdel">Сэтгэгдэл</label><br />
        <!-- Хоосон байлгахын тулд шошгуудыг нааж бичнэ -->
        <textarea id="setgegdel" name="setgegdel" rows="5" cols="40"></textarea>
      </p>

      <!-- type бичихээ мартвал submit болно -->
      <button type="submit">Илгээх</button>
      <button type="button">Цуцлах</button>
    </form>
  </body>
</html>
""",
        ),
        LessonSpec(
            title="Формын шинж чанар ба шалгалт",
            slug="formiin-shinj-chanar",
            description="required, pattern, min, max болон хөтчийн шалгалт.",
            duration=450,
            language=HTML,
            content="""\
HTML өөрөө оролтыг шалгаж чадна — JavaScript бичихгүйгээр.

### Түгээмэл шинж чанарууд

| Шинж чанар | Үүрэг |
|---|---|
| `required` | Хоосон орхиж болохгүй |
| `minlength` / `maxlength` | Текстийн урт |
| `min` / `max` | Тоо, огнооны хязгаар |
| `step` | Тооны алхам |
| `pattern` | Загварт таарах ёстой |
| `autocomplete` | Хөтөч утгыг санана |
| `readonly` | Харагдана, засагдахгүй |
| `disabled` | Засагдахгүй, **илгээгдэхгүй** |

### Жишээ

```html
<input type="text" name="ner" required minlength="2" maxlength="50" />
<input type="number" name="nas" min="1" max="120" />
<input type="text" name="utas" pattern="[0-9]{8}" title="8 оронтой тоо" />
```

`pattern` ашиглахдаа `title` **заавал** бич — хөтөч түүнийг алдааны
мессежид харуулна.

### `readonly` ба `disabled`

Хоёулаа засагдахгүй болгоно. Ялгаа нь:

- `readonly` — утга нь **илгээгдэнэ**
- `disabled` — утга нь **илгээгдэхгүй**

Хэрэглэгчид харуулах ч сервер рүү явуулах шаардлагатай утгад `readonly`
сонго.

### `autocomplete`

```html
<input type="email" name="email" autocomplete="email" />
<input type="password" name="nuuts" autocomplete="current-password" />
```

Энэ нь хэрэглэгчийн цагийг хэмнэнэ. Нууц үгийн менежер зөв ажиллана.
`autocomplete="off"` гэж бичих нь ихэвчлэн хэрэглэгчид саад болдог.

### Хөтчийн шалгалт хангалтгүй

> Хэрэглэгч DevTools нээгээд `required`-ийг устгаж чадна. Тиймээс сервер
> дээр **дахин шалгах** нь заавал. HTML-ийн шалгалт нь тав тухын
> зориулалттай, аюулгүй байдлын биш.

### `novalidate`

Өөрийн шалгалт бичих бол хөтчийнхийг унтраа:

```html
<form novalidate>…</form>
```

Ингэснээр хөтөч бүрт өөр өөр харагддаг анхдагч мессежийн оронд өөрийн
загвартай, монгол хэлтэй мессеж харуулж болно.
""",
            initial_code="""\
<!DOCTYPE html>
<html lang="mn">
  <head>
    <meta charset="UTF-8" />
    <title>Формын шалгалт</title>
  </head>

  <body>
    <h1>Бүртгэл</h1>

    <form action="/burtgel" method="post">
      <p>
        <label for="ner">Нэр</label><br />
        <input type="text" id="ner" name="ner" required minlength="2" maxlength="50" />
      </p>

      <p>
        <label for="email">Имэйл</label><br />
        <input type="email" id="email" name="email" required autocomplete="email" />
      </p>

      <p>
        <label for="utas">Утас</label><br />
        <!-- pattern-тэй хамт title ЗААВАЛ — алдааны мессежид харагдана -->
        <input
          type="text"
          id="utas"
          name="utas"
          pattern="[0-9]{8}"
          title="8 оронтой тоо оруулна уу"
        />
      </p>

      <p>
        <label for="nas">Нас</label><br />
        <input type="number" id="nas" name="nas" min="1" max="120" />
      </p>

      <p>
        <label for="kod">Бүртгэлийн код</label><br />
        <!-- readonly — утга нь ИЛГЭЭГДЭНЭ -->
        <input type="text" id="kod" name="kod" value="SR-2026" readonly />
      </p>

      <button type="submit">Илгээх</button>
    </form>
  </body>
</html>
""",
        ),
    ],
)

HTML_PRACTICE = ModuleSpec(
    title="Модул 6 — HTML дадлага",
    description="Зөвхөн HTML-ээр бүтэн хуудас бичнэ.",
    lessons=[
        LessonSpec(
            title="Дадлага — Хувийн хуудас",
            slug="huviin-huudas",
            description="Танилцуулга, ур чадвар, холбоо барих хэсэгтэй хуудас.",
            duration=600,
            language=HTML,
            content="""\
Өөрийгөө танилцуулах нэг хуудас бичнэ. CSS одоогоор алга — **бүтцэд** л
анхаарна.

### Юу багтаах вэ

1. `<header>` — нэр, богино танилцуулга
2. `<nav>` — хуудасны хэсгүүд рүү холбоос
3. `<main>` — тухай, ур чадвар, туршлага
4. `<footer>` — холбоо барих

### Гарчгийн шатлал

Энэ хуудсанд `<h1>` нэг, түүний доор `<h2>` хэд хэд байна. Түвшин
алгасахгүй.

### Хуудасны доторх холбоос

```html
<a href="#tuhai">Миний тухай</a>
…
<section id="tuhai">…</section>
```

`href="#id"` нь тухайн `id`-тай элемент рүү үсэрнэ.

### Хүртээмжийн нэг зөвлөгөө

Хуудасны эхэнд «агуулга руу шууд очих» холбоос тавих нь сайн зуршил:

```html
<a href="#main" class="alga-boloh">Үндсэн агуулга руу</a>
```

Гар ашигладаг хэрэглэгч цэсийг бүхэлд нь дамжилгүй агуулга руугаа
шууд орно.

### Даалгавар

1. Өөрийн мэдээллээр гүйцээж бичээрэй.
2. Ур чадварын жагсаалтад өөрийн сурч буй зүйлсийг нэмээрэй.
3. Боловсрол эсвэл төслийн хэсэг нэмээрэй.
""",
            initial_code="""\
<!DOCTYPE html>
<html lang="mn">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Бат Болд — Вэб хөгжүүлэгч</title>
    <meta name="description" content="Бат Болдын хувийн хуудас." />
  </head>

  <body>
    <a href="#main">Үндсэн агуулга руу</a>

    <header>
      <h1>Бат Болд</h1>
      <p>Вэб хөгжүүлэгч, Улаанбаатар</p>

      <nav aria-label="Хуудасны хэсгүүд">
        <ul>
          <li><a href="#tuhai">Миний тухай</a></li>
          <li><a href="#chadvar">Ур чадвар</a></li>
          <li><a href="#holbogdoh">Холбогдох</a></li>
        </ul>
      </nav>
    </header>

    <main id="main">
      <section id="tuhai">
        <h2>Миний тухай</h2>
        <p>
          Би вэб хөгжүүлэлт сурч буй бөгөөд одоогоор
          <strong>HTML</strong> болон <strong>CSS</strong> дээр анхаарч байна.
        </p>
      </section>

      <section id="chadvar">
        <h2>Ур чадвар</h2>
        <ul>
          <li>HTML — семантик бүтэц, форм</li>
          <li>CSS — сурч байна</li>
          <li>JavaScript — сурахаар төлөвлөж байна</li>
        </ul>
      </section>

      <section id="holbogdoh">
        <h2>Холбогдох</h2>
        <dl>
          <dt>Имэйл</dt>
          <dd><a href="mailto:bat@medleghub.mn">bat@medleghub.mn</a></dd>
          <dt>Утас</dt>
          <dd><a href="tel:+97699112233">9911-2233</a></dd>
        </dl>
      </section>
    </main>

    <footer>
      <p>&copy; 2026 Бат Болд</p>
    </footer>
  </body>
</html>
""",
        ),
        LessonSpec(
            title="Дадлага — Бүтээгдэхүүний хуудас",
            slug="buteegdehuuniy-huudas",
            description="Зураг, үнэ, тодорхойлолт, захиалгын форм.",
            duration=600,
            language=HTML,
            content="""\
Дэлгүүрийн нэг бүтээгдэхүүний хуудас бичнэ.

### Бүтэц

```text
header      лого, цэс
main
  article   бүтээгдэхүүн
    зураг
    нэр, үнэ
    тодорхойлолт
    үзүүлэлтийн хүснэгт
    захиалгын форм
  aside     төстэй бүтээгдэхүүн
footer
```

Бүтээгдэхүүн нь **дангаараа утга агуулна** тул `<article>`.

### Хүснэгт

Үзүүлэлтийг хүснэгтээр харуулна:

```html
<table>
  <caption>Техникийн үзүүлэлт</caption>
  <tbody>
    <tr>
      <th scope="row">Жин</th>
      <td>250 г</td>
    </tr>
  </tbody>
</table>
```

`<th scope="row">` нь «энэ нүд бол мөрийн гарчиг» гэж хэлнэ. Дэлгэц
уншигч утга бүрийг нэртэй нь хамт уншина.

> Хүснэгтийг зөвхөн **өгөгдөлд** ашигла, байршуулалтад биш. Байршуулалтад
> Модул 12-13-ын Flexbox, Grid хэрэглэнэ.

### Үнэ ба хямдрал

```html
<p>
  <s>120,000₮</s>
  <strong>89,000₮</strong>
</p>
```

`<s>` нь хүчингүй болсныг илэрхийлнэ.

### Даалгавар

1. Өөр бүтээгдэхүүн сонгож мэдээллийг нь солиорой.
2. Үзүүлэлтийн хүснэгтэд мөр нэмээрэй.
3. Тоо ширхэг сонгох талбарт зөв `min` ба `max` тавиарай.
""",
            initial_code="""\
<!DOCTYPE html>
<html lang="mn">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Утасгүй чихэвч — Дэлгүүр</title>
  </head>

  <body>
    <header>
      <h1>Дэлгүүр</h1>
      <nav aria-label="Үндсэн цэс">
        <ul>
          <li><a href="/">Нүүр</a></li>
          <li><a href="/teknik">Техник</a></li>
        </ul>
      </nav>
    </header>

    <main>
      <article>
        <h2>Утасгүй чихэвч</h2>

        <img src="/zurag/chiheveh.jpg" alt="Хар өнгийн утасгүй чихэвч" width="400" height="400" />

        <p>
          <s>120,000₮</s>
          <strong>89,000₮</strong>
        </p>

        <p>Идэвхтэй дуу намсгагчтай, 30 цаг ажиллах чадвартай чихэвч.</p>

        <table>
          <caption>Техникийн үзүүлэлт</caption>
          <tbody>
            <tr>
              <th scope="row">Жин</th>
              <td>250 г</td>
            </tr>
            <tr>
              <th scope="row">Батерей</th>
              <td>30 цаг</td>
            </tr>
            <tr>
              <th scope="row">Холболт</th>
              <td>Bluetooth 5.3</td>
            </tr>
          </tbody>
        </table>

        <form action="/sagst" method="post">
          <p>
            <label for="too">Тоо ширхэг</label>
            <input type="number" id="too" name="too" value="1" min="1" max="10" />
          </p>
          <button type="submit">Сагсанд хийх</button>
        </form>
      </article>

      <aside>
        <h2>Төстэй бүтээгдэхүүн</h2>
        <ul>
          <li><a href="#">Утастай чихэвч — 45,000₮</a></li>
          <li><a href="#">Чанга яригч — 150,000₮</a></li>
        </ul>
      </aside>
    </main>

    <footer><p>&copy; 2026 Дэлгүүр</p></footer>
  </body>
</html>
""",
        ),
        LessonSpec(
            title="Дадлага — Энгийн вэбсайт",
            slug="engiin-vebsait",
            description="Хэд хэдэн хуудсыг хооронд нь холбох.",
            duration=660,
            language=HTML,
            content="""\
Одоо хэд хэдэн хуудастай жижиг сайт угсарна.

### Файлын бүтэц

```text
index.html      Нүүр
tuhai.html      Бидний тухай
holbogdoh.html  Холбоо барих
zurag/          Зургууд
```

`index.html` нь тусгай нэр — хавтас руу орвол сервер үүнийг өгнө.
Тиймээс `medleghub.mn/` нь `medleghub.mn/index.html`-тэй ижил.

### Хуудсуудыг холбох

Харьцангуй замаар холбоно:

```html
<a href="tuhai.html">Тухай</a>
<a href="index.html">Нүүр</a>
```

Дэд хавтаснаас дээш гарахдаа `../` ашиглана:

```html
<a href="../index.html">Нүүр</a>
```

### Давтагдах хэсэг

Цэс, хөл хэсэг нь хуудас болгонд **давтагдана**. Энгийн HTML-д үүнийг
хуулж бичихээс өөр арга байхгүй.

Хуудас олон болоход энэ нь асуудал болно — цэсэнд нэг холбоос нэмэхэд
бүх файлыг засах шаардлагатай. Тиймээс бодит төсөлд загвар хөдөлгүүр
(template engine) эсвэл React зэрэг хэрэгсэл ашигладаг.

### Одоогийн хуудсыг тэмдэглэх

```html
<a href="tuhai.html" aria-current="page">Тухай</a>
```

Дэлгэц уншигч «одоогийн хуудас» гэж хэлнэ. CSS-ээр ч онцолж болно.

### Даалгавар

1. Доорх нүүр хуудсыг үндэслэн `tuhai.html` бичээрэй.
2. Цэсэнд дөрөв дэх холбоос нэмээд бүх хуудсанд тусгаарай.
3. Хуудас бүрт өөр `<title>` болон `description` бичээрэй.
""",
            initial_code=files(
                (
                    "index.html",
                    """\
<!-- index.html — сайтын нүүр хуудас -->
<!DOCTYPE html>
<html lang="mn">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Нүүр — Гэрэл зургийн студи</title>
    <meta name="description" content="Улаанбаатар дахь гэрэл зургийн студи." />
  </head>

  <body>
    <header>
      <h1>Гэрэл зургийн студи</h1>

      <nav aria-label="Үндсэн цэс">
        <ul>
          <!-- Одоогийн хуудсыг тэмдэглэнэ -->
          <li><a href="index.html" aria-current="page">Нүүр</a></li>
          <li><a href="tuhai.html">Тухай</a></li>
          <li><a href="holbogdoh.html">Холбогдох</a></li>
        </ul>
      </nav>
    </header>

    <main>
      <section>
        <h2>Тавтай морил</h2>
        <p>Бид 2019 оноос хойш дурсгалт мөчүүдийг тань хадгалж байна.</p>
      </section>

      <section>
        <h2>Үйлчилгээ</h2>
        <ul>
          <li>Хурим</li>
          <li>Хөрөг</li>
          <li>Бүтээгдэхүүний зураг</li>
        </ul>
      </section>

      <section>
        <h2>Сүүлийн ажлууд</h2>
        <figure>
          <img src="zurag/ajil-1.jpg" alt="Намрын хуримын гэрэл зураг" width="400" height="300" />
          <figcaption>Хурим, 2026 оны намар</figcaption>
        </figure>
      </section>
    </main>

    <footer>
      <p>&copy; 2026 Гэрэл зургийн студи</p>
      <p><a href="holbogdoh.html">Холбоо барих</a></p>
    </footer>
  </body>
</html>
""",
                ),
                (
                    "tuhai.html",
                    """\
<!-- tuhai.html — «Бидний тухай» хуудас (1-р даалгавар).
     index.html-ийг үндэслэн толгой, цэс, хөлөө хуулаад агуулгаа энд бичээрэй.
     «Хөтөч» дээр нүүр хуудасны «Тухай» холбоосоор энэ хуудас нээгдэнэ. -->
<!DOCTYPE html>
<html lang="mn">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Тухай — Гэрэл зургийн студи</title>
  </head>

  <body>
    <h1>Бидний тухай</h1>

    <p><a href="index.html">Нүүр хуудас руу буцах</a></p>
  </body>
</html>
""",
                ),
            ),
        ),
    ],
)

HTML_STRUCTURE_MODULES = [SEMANTIC, FORMS, HTML_PRACTICE]
