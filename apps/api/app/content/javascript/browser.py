"""Модул 10-13 — Хөтчийн JavaScript: DOM, үйлдэл, форм, хадгалалт.

АНХААР: Код ажиллуулагч нь Web Worker дотор ажилладаг тул жинхэнэ
`document`, `localStorage` байхгүй. Тиймээс эдгээр хичээлийн анхны код нь
ижил нэртэй метод бүхий ЖИЖИГ ЗАГВАРЫГ өөрөө үүсгэж ажиллуулна.
Хичээлийн текст дэх жишээ нь жинхэнэ хөтөчид ажиллах бодит код.
"""

from app.content.types import ExerciseSpec, LessonSpec, ModuleSpec, TestCaseSpec

DOM = ModuleSpec(
    title="Модул 10 — DOM",
    description="Хуудасны бүтцийг JavaScript-ээр уншиж, өөрчлөх.",
    lessons=[
        LessonSpec(
            title="DOM гэж юу вэ?",
            slug="dom-gej-yu-ve",
            description="Хөтөч HTML-ийг объектын мод болгон хөрвүүлдэг.",
            duration=420,
            content="""\
Хуудас ачаалагдахад хөтөч HTML-ийг уншаад **объектын мод** болгон
хөрвүүлнэ. Үүнийг DOM (Document Object Model) гэнэ.

```html
<body>
  <h1>Гарчиг</h1>
  <p>Тайлбар</p>
</body>
```

Дээрх HTML нь ийм мод болно:

```text
document
└── html
    └── body
        ├── h1  → "Гарчиг"
        └── p   → "Тайлбар"
```

### Яагаад чухал вэ

JavaScript нь HTML файлыг **шууд** өөрчилдөггүй. Санах ой дахь энэ модыг
өөрчилдөг бөгөөд хөтөч түүнийг дэлгэц дээр дахин зурдаг.

Тиймээс:

- Хуудсыг дахин ачаалахгүйгээр агуулга солигдоно
- Файл дээрх өөрчлөлт **хадгалагдахгүй** — сэргээхэд бүх зүйл буцна

### Зангилаа (node) ба элемент

Модны хэсэг бүрийг *зангилаа* гэнэ. Текст ч, тайлбар ч зангилаа. Харин
**элемент** гэдэг нь тэгээс `<h1>` гэх мэт шошготой зангилаа.

### `document` объект

Модны оройд `document` байрлана. Бүх хайлт эндээс эхэлнэ:

```javascript
document.title;                   // хуудасны гарчиг
document.body;                    // body элемент
document.querySelector("h1");     // эхний h1
```

### Хөгжүүлэгчийн хэрэгслээр харах

DevTools-ийн **Elements** таб нь яг энэ модыг харуулдаг. Тэнд элемент
дээр дарж утгыг нь шууд өөрчилж үзэж болно.
""",
            initial_code="""\
// Код ажиллуулагчид жинхэнэ DOM байхгүй тул модыг өөрсдөө загварчилъя.
// Зангилаа бүр нь объект, хүүхдүүд нь huuhduud массивд байна.
const body = { shoshgo: "body", text: "", huuhduud: [] };

// Мөрүүдийг оролт дуустал уншина.
let mur = prompt();
while (mur !== null) {
  // TODO: "h1 Гарчиг" мөрөөс { shoshgo: "h1", text: "Гарчиг", huuhduud: [] }
  //       зангилаа үүсгэнэ. "-"-ээр эхэлсэн бол body-ийн сүүлийн хүүхдэд,
  //       бусад үед body-д нэмнэ.
  mur = prompt();
}

// Нэг зангилааг догол мөртэй хэвлэнэ. Текстгүй бол зөвхөн шошгыг нь.
function hevleh(zangilaa, zai) {
  if (zangilaa.text) {
    console.log(`${zai}${zangilaa.shoshgo} → "${zangilaa.text}"`);
  } else {
    console.log(`${zai}${zangilaa.shoshgo}`);
  }
}

// Модыг давхарга давхаргаар нь явна: body → хүүхдүүд → ач нар.
hevleh(body, "");
for (const huuhed of body.huuhduud) {
  hevleh(huuhed, "  ");
  for (const ach of huuhed.huuhduud) {
    hevleh(ach, "    ");
  }
}

// TODO: "Элемент: ..." ба "Текст: ..." мөрүүдийг хэвлэнэ.
""",
            exercise=ExerciseSpec(
                statement="""\
Хуудасны DOM модыг оролтоос байгуулж, догол мөртэйгөөр хэвлэ. Модны орой нь
`body`. Код ажиллуулагчид жинхэнэ DOM байхгүй тул зангилаа бүрийг
`{ shoshgo, text, huuhduud }` объект, хүүхдүүдийг `huuhduud` массивд хадгална
(`body` ба хэвлэх `hevleh` функц эхлэл кодод бэлэн).

**Оролт:** мөр бүрт нэг элемент: `<шошго> <текст>`. Текст нь зайтай байж
болно, эсвэл огт байхгүй (`ul`). `-`-ээр эхэлсэн мөр (`-li Нэг`) нь **өмнөх**
`-`-гүй элементийн хүүхэд, бусад нь `body`-ийн хүүхэд. Эхний мөр `-`-ээр
эхлэхгүй.

**Гаралт:** модыг `body`-оос эхлэн давхарга бүрт хоёр зай нэмж хэвлэ.
Тексттэй элементийн ард `→ "<текст>"` нэмнэ. Эцэст нь элементийн тоо (`body`-г
оруулаад) ба текст агуулсан элементийн тоо:

```text
body
  <шошго> → "<текст>"
  <шошго>
    <шошго> → "<текст>"
Элемент: <тоо>
Текст: <тоо>
```
""",
                tests=(
                    TestCaseSpec(
                        stdin="h1 Гарчиг\np Тайлбар\n",
                        expected_output='body\n  h1 → "Гарчиг"\n  p → "Тайлбар"\nЭлемент: 3\nТекст: 2\n',
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="h1 MedlegHub\nul\n-li Нэг\n-li Хоёр\np Холбоо барих\n",
                        expected_output='body\n  h1 → "MedlegHub"\n  ul\n    li → "Нэг"\n    li → "Хоёр"\n  p → "Холбоо барих"\nЭлемент: 6\nТекст: 4\n',
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="div\n-h2 Мэдээ\n-p Өнөөдөр бороо орно\ndiv\n-img\n",
                        expected_output='body\n  div\n    h2 → "Мэдээ"\n    p → "Өнөөдөр бороо орно"\n  div\n    img\nЭлемент: 6\nТекст: 2\n',
                    ),
                    TestCaseSpec(
                        stdin="main\n",
                        expected_output="body\n  main\nЭлемент: 2\nТекст: 0\n",
                    ),
                    TestCaseSpec(
                        stdin="nav\n-a Нүүр\n-a Хичээлүүд\n-a Үнэ\nfooter © 2026 MedlegHub\n",
                        expected_output='body\n  nav\n    a → "Нүүр"\n    a → "Хичээлүүд"\n    a → "Үнэ"\n  footer → "© 2026 MedlegHub"\nЭлемент: 6\nТекст: 4\n',
                    ),
                ),
                solution="""\
const body = { shoshgo: "body", text: "", huuhduud: [] };

// "h1 Гарчиг" → { shoshgo: "h1", text: "Гарчиг", huuhduud: [] }
function zangilaaUusgeh(mur) {
  const hesguud = mur.split(" ");
  return { shoshgo: hesguud[0], text: hesguud.slice(1).join(" "), huuhduud: [] };
}

let mur = prompt();
while (mur !== null) {
  if (mur.startsWith("-")) {
    const etseg = body.huuhduud[body.huuhduud.length - 1];
    etseg.huuhduud.push(zangilaaUusgeh(mur.slice(1)));
  } else {
    body.huuhduud.push(zangilaaUusgeh(mur));
  }
  mur = prompt();
}

// Нэг зангилааг догол мөртэй хэвлэнэ. Текстгүй бол зөвхөн шошгыг нь.
function hevleh(zangilaa, zai) {
  if (zangilaa.text) {
    console.log(`${zai}${zangilaa.shoshgo} → "${zangilaa.text}"`);
  } else {
    console.log(`${zai}${zangilaa.shoshgo}`);
  }
}

let elementToo = 1; // body
let textToo = 0;

hevleh(body, "");
for (const huuhed of body.huuhduud) {
  hevleh(huuhed, "  ");
  elementToo++;
  if (huuhed.text) {
    textToo++;
  }
  for (const ach of huuhed.huuhduud) {
    hevleh(ach, "    ");
    elementToo++;
    if (ach.text) {
      textToo++;
    }
  }
}

console.log(`Элемент: ${elementToo}`);
console.log(`Текст: ${textToo}`);
""",
                tips="""\
- `"h1 Гарчиг".split(" ")`-ийн эхний хэсэг нь шошго. Үлдсэнийг
  `slice(1).join(" ")` гэж нийлүүлбэл текст болно — зайтай текст ч эвдрэхгүй,
  текстгүй бол `""`.
- `mur.startsWith("-")` бол `mur.slice(1)`-ээс үүсгэсэн зангилааг `body`-ийн
  **сүүлийн** хүүхдийн `huuhduud`-д нэм: `body.huuhduud[body.huuhduud.length - 1]`.
- Хоосон мөр `""` нь falsy — `if (zangilaa.text)` текстгүй элементийг ялгана.
- Тоолохдоо хэвлэх давталттайгаа нэг дор тоол. `body`-г мартаж болохгүй.
""",
            ),
        ),
        LessonSpec(
            title="Элемент сонгох",
            slug="element-songoh",
            description="querySelector болон бусад сонгох аргууд.",
            duration=420,
            content="""\
Элементийг өөрчлөхийн өмнө эхлээд **олох** хэрэгтэй.

### `querySelector`

CSS сонгогч ашиглана — CSS дээр мэддэг бүх зүйл энд ажиллана:

```javascript
document.querySelector("h1");         // эхний h1
document.querySelector(".zurag");     // class
document.querySelector("#garchig");   // id
document.querySelector("ul li");      // ul доторх эхний li
```

**Эхний** таарсныг л буцаана. Олдохгүй бол `null`.

### `querySelectorAll`

Бүх таарсныг жагсаалт болгон буцаана:

```javascript
const buhLi = document.querySelectorAll("li");

console.log(buhLi.length);
buhLi.forEach((li) => console.log(li.textContent));
```

Буцаах зүйл нь `NodeList` — массив **биш**. `forEach` ажиллах ч `map`,
`filter` ажиллахгүй. Массив болгохын тулд:

```javascript
const massiv = Array.from(buhLi);
```

### Хуучин аргууд

```javascript
document.getElementById("garchig");
document.getElementsByClassName("zurag");
```

Ажиллах боловч `querySelector` нь нэг л дүрэм сурахад хангалттай тул
шинэ кодод түүнийг сонго.

### `null` шалгах

Элемент олдохгүй байх нь түгээмэл алдаа:

```javascript
const el = document.querySelector("#baihgui");
el.textContent = "сайн уу"; // TypeError
```

Тиймээс шалгах нь зүйтэй:

```javascript
if (el) {
  el.textContent = "сайн уу";
}
```

Хамгийн түгээмэл шалтгаан нь `<script>` нь элементээс **өмнө** ажилласан
байдаг — `defer` ашиглаж засна.
""",
            initial_code="""\
// Хуудасны элементүүдийн жижиг загвар. angi нь зайгаар тусгаарласан классууд.
const elementuud = [
  { shoshgo: "h1", id: "garchig", angi: "tod", text: "MedlegHub" },
  { shoshgo: "p", id: "", angi: "tailbar", text: "Эхний догол" },
  { shoshgo: "p", id: "tanilts", angi: "tailbar tod", text: "Хоёр дахь догол" },
  { shoshgo: "a", id: "", angi: "holboos", text: "Хичээлүүд" },
  { shoshgo: "button", id: "hadgalah", angi: "tovch tod", text: "Хадгалах" },
  { shoshgo: "button", id: "", angi: "tovch", text: "Цуцлах" },
];

// el нь songogch-тэй таарах эсэх
function tohiroh(el, songogch) {
  // TODO: "#нэр" бол id-аар, ".нэр" бол классаар тааруулна.
  return el.shoshgo === songogch;
}

function querySelector(songogch) {
  // TODO: эхний таарсан элементийг, олдохгүй бол null буцаана.
  return null;
}

function querySelectorAll(songogch) {
  // TODO: бүх таарсан элементийг массиваар буцаана.
  return [];
}

// Сонгогч бүрийг шалгаж хэвлэнэ — энэ хэсгийг бүү өөрчил.
let songogch = prompt();
while (songogch !== null) {
  const ehnii = querySelector(songogch);
  if (ehnii) {
    const bugd = querySelectorAll(songogch);
    console.log(`${songogch} → ${bugd.length} ширхэг, эхнийх: ${ehnii.text}`);
  } else {
    console.log(`${songogch} → null`);
  }
  songogch = prompt();
}
""",
            exercise=ExerciseSpec(
                statement="""\
`querySelector`, `querySelectorAll`-ийг жижиг загвараар бич. Хуудасны
элементүүд `elementuud` массивт бэлэн (эхлэл кодыг хар). Сонгогч гурван
төрөлтэй:

| Сонгогч | Таарах элемент |
|---|---|
| `#нэр` | `id` нь `нэр` |
| `.нэр` | `angi`-д `нэр` класс **бүтэн үгээр** байгаа — `"tailbar tod"` нь `tailbar`, `tod` хоёр класстай |
| `нэр` | шошго нь `нэр` |

`querySelector` нь эхний таарсныг, олдохгүй бол `null`; `querySelectorAll` нь
бүх таарсныг массиваар буцаана. Том, жижиг үсэг ялгаатай.

**Оролт:** мөр бүрт нэг сонгогч.

**Гаралт:** сонгогч бүрт нэг мөр (хэвлэх код эхлэл кодод бэлэн):

```text
<сонгогч> → <тоо> ширхэг, эхнийх: <эхний элементийн текст>
<сонгогч> → null
```
""",
                tests=(
                    TestCaseSpec(
                        stdin="h1\n#garchig\n.tailbar\n#baihgui\n",
                        expected_output="h1 → 1 ширхэг, эхнийх: MedlegHub\n#garchig → 1 ширхэг, эхнийх: MedlegHub\n.tailbar → 2 ширхэг, эхнийх: Эхний догол\n#baihgui → null\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin=".tod\nbutton\n",
                        expected_output=".tod → 3 ширхэг, эхнийх: MedlegHub\nbutton → 2 ширхэг, эхнийх: Хадгалах\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin=".tail\ntod\n#tanilts\n",
                        expected_output=".tail → null\ntod → null\n#tanilts → 1 ширхэг, эхнийх: Хоёр дахь догол\n",
                    ),
                    TestCaseSpec(
                        stdin="p\n.tovch\n#hadgalah\nH1\n",
                        expected_output="p → 2 ширхэг, эхнийх: Эхний догол\n.tovch → 2 ширхэг, эхнийх: Хадгалах\n#hadgalah → 1 ширхэг, эхнийх: Хадгалах\nH1 → null\n",
                    ),
                    TestCaseSpec(
                        stdin="a\n.holboos\nul\n",
                        expected_output="a → 1 ширхэг, эхнийх: Хичээлүүд\n.holboos → 1 ширхэг, эхнийх: Хичээлүүд\nul → null\n",
                    ),
                ),
                solution="""\
// Хуудасны элементүүдийн жижиг загвар. angi нь зайгаар тусгаарласан классууд.
const elementuud = [
  { shoshgo: "h1", id: "garchig", angi: "tod", text: "MedlegHub" },
  { shoshgo: "p", id: "", angi: "tailbar", text: "Эхний догол" },
  { shoshgo: "p", id: "tanilts", angi: "tailbar tod", text: "Хоёр дахь догол" },
  { shoshgo: "a", id: "", angi: "holboos", text: "Хичээлүүд" },
  { shoshgo: "button", id: "hadgalah", angi: "tovch tod", text: "Хадгалах" },
  { shoshgo: "button", id: "", angi: "tovch", text: "Цуцлах" },
];

function tohiroh(el, songogch) {
  if (songogch.startsWith("#")) {
    return el.id === songogch.slice(1);
  }
  if (songogch.startsWith(".")) {
    // "tailbar tod" → ["tailbar", "tod"] — бүтэн классаар харьцуулна
    return el.angi.split(" ").includes(songogch.slice(1));
  }
  return el.shoshgo === songogch;
}

function querySelector(songogch) {
  const oldson = elementuud.find((el) => tohiroh(el, songogch));
  // find олдохгүй бол undefined өгнө. querySelector шиг null буцаая.
  return oldson || null;
}

function querySelectorAll(songogch) {
  return elementuud.filter((el) => tohiroh(el, songogch));
}

// Сонгогч бүрийг шалгаж хэвлэнэ — энэ хэсгийг бүү өөрчил.
let songogch = prompt();
while (songogch !== null) {
  const ehnii = querySelector(songogch);
  if (ehnii) {
    const bugd = querySelectorAll(songogch);
    console.log(`${songogch} → ${bugd.length} ширхэг, эхнийх: ${ehnii.text}`);
  } else {
    console.log(`${songogch} → null`);
  }
  songogch = prompt();
}
""",
                tips="""\
- `"#garchig".startsWith("#")` → `true`, `"#garchig".slice(1)` → `"garchig"`.
- Классыг `el.angi.includes(...)`-ээр шалгавал `.tail` нь `"tailbar"`-т
  таарчихна. Эхлээд `split(" ")`-ээр классуудын **массив** болгоод массивын
  `includes`-ийг ашигла.
- `find` олдохгүй бол `undefined` өгнө — `|| null` нэмбэл жинхэнэ
  `querySelector` шиг `null` болно.
- `querySelectorAll`-д `filter` яг тохирно.
""",
            ),
        ),
        LessonSpec(
            title="Агуулга ба загвар өөрчлөх",
            slug="aguulga-ba-zagvar-uurchluh",
            description="textContent, classList, style ашиглах.",
            duration=450,
            content="""\
### Текст солих

```javascript
const garchig = document.querySelector("h1");

garchig.textContent = "Шинэ гарчиг";
```

### `textContent` ба `innerHTML`

```javascript
el.textContent = "<b>тод</b>"; // текст болгож харуулна
el.innerHTML = "<b>тод</b>";   // HTML болгож ажиллуулна
```

> **Аюулгүй байдал:** хэрэглэгчээс ирсэн текстийг `innerHTML`-д хэзээ ч
> бүү тавь. Хортой script шигтгэх боломж үүснэ (XSS халдлага).
> Эргэлзвэл `textContent` ашигла.

### Шинж чанар (attribute)

```javascript
zurag.src = "shine.png";
holboos.href = "/courses";
oruulga.value = "";

el.setAttribute("data-id", "42");
console.log(el.getAttribute("data-id"));
```

### Загвар өөрчлөх

Хоёр арга бий. **Class солих нь бараг үргэлж дээр**:

```javascript
// Сайн — CSS дотор загвар үлдэнэ
el.classList.add("idevhtei");
el.classList.remove("nuutsalsan");
el.classList.toggle("neelttei");
console.log(el.classList.contains("idevhtei"));

// Хязгаартай — загвар JavaScript дотор тархана
el.style.color = "red";
el.style.backgroundColor = "black"; // CSS-ийн background-color
```

CSS дэх зураастай нэрс JavaScript дээр `camelCase` болдгийг анхаар.

### Яагаад class нь дээр вэ

- Загвар CSS дотроо үлдэнэ — нэг газраас удирдана
- Нэг класс олон шинжийг зэрэг өөрчилнө
- Хөтөч илүү хурдан зурна
""",
            initial_code="""\
// Элементийн зан төлөвийг загварчилсан жижиг объект. Жинхэнэ хөтөчид
// querySelector("h1") ийм талбар, методтой объект буцаана.
const garchig = {
  shoshgo: "h1",
  textContent: "Хуучин гарчиг",
  style: {},
  classList: {
    angiuud: [], // одоо байгаа классууд
    add(ner) {
      if (!this.angiuud.includes(ner)) {
        this.angiuud.push(ner);
      }
    },
    remove(ner) {
      this.angiuud = this.angiuud.filter((a) => a !== ner);
    },
    contains(ner) {
      return this.angiuud.includes(ner);
    },
    toggle(ner) {
      if (this.contains(ner)) {
        this.remove(ner);
      } else {
        this.add(ner);
      }
    },
  },
  // Классуудыг зайгаар нийлүүлсэн мөр (жинхэнэ DOM-ийн className шиг)
  className() {
    return this.classList.angiuud.join(" ");
  },
};

function harah() {
  // TODO: "Текст: ...", "Класс: ...", "Загвар: ..." гурван мөрийг хэвлэнэ.
}

let mur = prompt();
while (mur !== null) {
  // "style color red" → komand "style", utga "color red"
  const hesguud = mur.split(" ");
  const komand = hesguud[0];
  const utga = hesguud.slice(1).join(" ");

  switch (komand) {
    case "text":
      garchig.textContent = utga;
      break;
    // TODO: add, remove, toggle, contains, style командуудыг нэмнэ.
    case "harah":
      harah();
      break;
  }

  mur = prompt();
}
""",
            exercise=ExerciseSpec(
                statement="""\
Гарчгийн элементийг командаар өөрчил. Элементийн загвар (`garchig`) эхлэл
кодод бэлэн: `textContent`, `style` объект, `classList`-ийн `add`, `remove`,
`toggle`, `contains` методтой, `className()` нь классуудыг зайгаар нийлүүлнэ.
Эхэндээ текст нь `Хуучин гарчиг`, класс, загвар хоосон.

| Команд | Үйлдэл |
|---|---|
| `text <текст>` | `textContent`-ийг солино (текст зайтай байж болно) |
| `add <класс>`, `remove <класс>`, `toggle <класс>` | `classList`-ийн тэр методыг дуудна |
| `contains <класс>` | `<класс>: true` эсвэл `<класс>: false` гэж хэвлэнэ |
| `style <шинж> <утга>` | `garchig.style`-д тэр шинжийг онооно (`style color red`) |
| `harah` | элементийн одоогийн төлөвийг хэвлэнэ |

**Оролт:** мөр бүрт нэг команд.

**Гаралт:** `contains` нэг мөр, `harah` гурван мөр хэвлэнэ:

```text
Текст: <textContent>
Класс: <классууд зайгаар тусгаарлагдаж>
Загвар: <шинж>: <утга>; <шинж>: <утга>
```

Класс байхгүй бол `Класс: (байхгүй)`, загвар байхгүй бол `Загвар: (байхгүй)`.
Классууд нэмсэн дарааллаараа, загварын шинжүүд анх оноосон дарааллаараа гарна.
""",
                tests=(
                    TestCaseSpec(
                        stdin="text Шинэ гарчиг\nadd idevhtei\nadd tom\ntoggle idevhtei\ncontains tom\nstyle color red\nharah\n",
                        expected_output="tom: true\nТекст: Шинэ гарчиг\nКласс: tom\nЗагвар: color: red\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="harah\n",
                        expected_output="Текст: Хуучин гарчиг\nКласс: (байхгүй)\nЗагвар: (байхгүй)\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="add a\nadd a\nremove b\ntoggle c\ncontains a\ncontains b\nstyle fontSize 20px\nstyle fontSize 24px\nstyle backgroundColor black\nharah\n",
                        expected_output="a: true\nb: false\nТекст: Хуучин гарчиг\nКласс: a c\nЗагвар: fontSize: 24px; backgroundColor: black\n",
                    ),
                    TestCaseSpec(
                        stdin="text <b>тод</b>\nharah\ntext Дахин өөрчиллөө\nadd ulaan\nharah\n",
                        expected_output="Текст: <b>тод</b>\nКласс: (байхгүй)\nЗагвар: (байхгүй)\nТекст: Дахин өөрчиллөө\nКласс: ulaan\nЗагвар: (байхгүй)\n",
                    ),
                    TestCaseSpec(
                        stdin="toggle neelttei\nharah\ntoggle neelttei\nadd ulaan\nremove ulaan\nharah\n",
                        expected_output="Текст: Хуучин гарчиг\nКласс: neelttei\nЗагвар: (байхгүй)\nТекст: Хуучин гарчиг\nКласс: (байхгүй)\nЗагвар: (байхгүй)\n",
                    ),
                ),
                solution="""\
// Элементийн зан төлөвийг загварчилсан жижиг объект. Жинхэнэ хөтөчид
// querySelector("h1") ийм талбар, методтой объект буцаана.
const garchig = {
  shoshgo: "h1",
  textContent: "Хуучин гарчиг",
  style: {},
  classList: {
    angiuud: [], // одоо байгаа классууд
    add(ner) {
      if (!this.angiuud.includes(ner)) {
        this.angiuud.push(ner);
      }
    },
    remove(ner) {
      this.angiuud = this.angiuud.filter((a) => a !== ner);
    },
    contains(ner) {
      return this.angiuud.includes(ner);
    },
    toggle(ner) {
      if (this.contains(ner)) {
        this.remove(ner);
      } else {
        this.add(ner);
      }
    },
  },
  // Классуудыг зайгаар нийлүүлсэн мөр (жинхэнэ DOM-ийн className шиг)
  className() {
    return this.classList.angiuud.join(" ");
  },
};

function harah() {
  console.log(`Текст: ${garchig.textContent}`);
  console.log(`Класс: ${garchig.className() || "(байхгүй)"}`);

  // { color: "red", fontSize: "24px" } → "color: red; fontSize: 24px"
  const shinjuud = Object.keys(garchig.style).map((ner) => `${ner}: ${garchig.style[ner]}`);
  console.log(`Загвар: ${shinjuud.length > 0 ? shinjuud.join("; ") : "(байхгүй)"}`);
}

let mur = prompt();
while (mur !== null) {
  // "style color red" → komand "style", utga "color red"
  const hesguud = mur.split(" ");
  const komand = hesguud[0];
  const utga = hesguud.slice(1).join(" ");

  switch (komand) {
    case "text":
      garchig.textContent = utga;
      break;
    case "add":
      garchig.classList.add(utga);
      break;
    case "remove":
      garchig.classList.remove(utga);
      break;
    case "toggle":
      garchig.classList.toggle(utga);
      break;
    case "contains":
      console.log(`${utga}: ${garchig.classList.contains(utga)}`);
      break;
    case "style": {
      // "color red" → шинж "color", утга "red"
      const [shinj, shinjUtga] = utga.split(" ");
      garchig.style[shinj] = shinjUtga;
      break;
    }
    case "harah":
      harah();
      break;
  }

  mur = prompt();
}
""",
                tips="""\
- `garchig.style[shinj] = ...` — дөрвөлжин хаалт нь хувьсагчид байгаа нэрээр
  талбар онооно. `garchig.style.shinj` гэвэл яг `"shinj"` нэртэй талбар үүснэ.
- `style`-ийн `utga` нь `"color red"` — дахин `split(" ")` хийж шинж, утгаа ав.
- Загварын мөрийг `Object.keys(garchig.style)` + `map` + `join("; ")`-ээр бүтээ.
- `garchig.className()` хоосон бол `""` — falsy тул `|| "(байхгүй)"` ажиллана.
- `add` давхар класс нэмэхгүй, байхгүй классыг `remove` хийхэд алдаа гарахгүй —
  загвар өөрөө үүнийг зохицуулна.
""",
            ),
        ),
        LessonSpec(
            title="Элемент үүсгэх ба устгах",
            slug="element-uusgeh-ba-ustgah",
            description="createElement, append, remove.",
            duration=450,
            content="""\
### Шинэ элемент үүсгэх

Гурван алхам: үүсгэ, дүүрг, залга.

```javascript
const li = document.createElement("li");   // 1. үүсгэнэ
li.textContent = "Шинэ мөр";               // 2. дүүргэнэ

const jagsaalt = document.querySelector("ul");
jagsaalt.append(li);                       // 3. модонд залгана
```

Гурав дахь алхмыг хийх хүртэл элемент дэлгэц дээр **харагдахгүй**.

### Байрлуулах аргууд

| Метод | Хаана оруулах |
|---|---|
| `append` | Эцгийн төгсгөлд |
| `prepend` | Эцгийн эхэнд |
| `before` | Энэ элементийн урд |
| `after` | Энэ элементийн ард |

### Устгах

```javascript
li.remove();
```

### Олон элемент нэмэх

Давталт бүрт DOM-д хүрэх нь удаан. Эхлээд мөрүүдээ бэлдээд нэг удаа
залгах нь хурдан:

```javascript
const muruud = ugugduluud.map((zuil) => {
  const li = document.createElement("li");
  li.textContent = zuil.ner;
  return li;
});

jagsaalt.append(...muruud); // нэг л удаа хүрнэ
```

`append` нь хэдэн ч элемент зэрэг авч чадна. `...muruud` нь массивын
элементүүдийг задлаад тус тусад нь аргумент болгож дамжуулна —
`append(muruud[0], muruud[1], ...)` гэж бичсэнтэй адил. Модул 7-д үзсэн
тараах оператор энд ч ажилладаг (Модул 15-д дэлгэрэнгүй үзнэ).

### Бүгдийг цэвэрлэх

```javascript
jagsaalt.replaceChildren(); // бүх хүүхдийг устгана
```

Хуучин кодод `innerHTML = ""` тааралдана. Ажиллах боловч
`replaceChildren` нь зорилгоо илүү тодорхой хэлж байна.
""",
            initial_code="""\
// Жагсаалтын (<ul>) зан төлөвийг загварчилъя.
const jagsaalt = {
  huuhduud: [],
  // ...elementuud нь дуудахад өгсөн бүх аргументыг нэг массив болгон
  // цуглуулна — append(a) ч, append(a, b, c) ч ажиллана (Модул 15-д үзнэ).
  append(...elementuud) {
    for (const el of elementuud) {
      el.etseg = this;
      this.huuhduud.push(el);
    }
  },
  prepend(el) {
    el.etseg = this;
    this.huuhduud.unshift(el);
  },
  replaceChildren() {
    this.huuhduud = [];
  },
  harah() {
    console.log(`<ul> (${this.huuhduud.length} мөр)`);
    for (const el of this.huuhduud) {
      console.log(`  <li>${el.textContent}</li>`);
    }
  },
};

function createElement(shoshgo) {
  return {
    shoshgo: shoshgo,
    textContent: "",
    etseg: null,
    // Элемент өөрийгөө эцгийнхээ хүүхдүүдээс хасна
    remove() {
      if (this.etseg) {
        this.etseg.huuhduud = this.etseg.huuhduud.filter((el) => el !== this);
        this.etseg = null;
      }
    },
  };
}

let mur = prompt();
while (mur !== null) {
  // "append Шинэ мөр" → komand "append", utga "Шинэ мөр"
  const hesguud = mur.split(" ");
  const komand = hesguud[0];
  const utga = hesguud.slice(1).join(" ");

  switch (komand) {
    // TODO: append, prepend, olon, remove, clear командуудыг нэмнэ.
    //       Гурван алхам: createElement("li") → textContent → залгах.
    case "harah":
      jagsaalt.harah();
      break;
  }

  mur = prompt();
}
""",
            exercise=ExerciseSpec(
                statement="""\
Жагсаалтын (`<ul>`) мөрүүдийг командаар үүсгэж, устга. `jagsaalt` (`append`,
`prepend`, `replaceChildren`, `harah` методтой) ба `createElement` эхлэл кодод
бэлэн. `createElement("li")`-ийн буцаасан элемент `textContent`-тэй, өөрийгөө
жагсаалтаас хасдаг `remove()` методтой.

| Команд | Үйлдэл |
|---|---|
| `append <текст>` | тэр тексттэй `li` үүсгээд төгсгөлд залгана |
| `prepend <текст>` | эхэнд залгана |
| `olon <текст>,<текст>,...` | таслалаар тусгаарласан текст бүрт `li` үүсгээд бүгдийг **нэг** `append` дуудлагаар залгана |
| `remove <n>` | `n`-р мөрийг (1-ээс тоолно) `remove()`-оор устгана; байхгүй бол `<n>-р мөр алга` гэж хэвлэнэ |
| `clear` | бүх мөрийг устгана |
| `harah` | `jagsaalt.harah()`-ийг дуудна |

**Оролт:** мөр бүрт нэг команд. Текст зайтай байж болно.

**Гаралт:** `harah` бүр жагсаалтыг хэвлэнэ, байхгүй мөрийг устгах гэвэл
мессеж хэвлэнэ:

```text
<ul> (<мөрийн тоо> мөр)
  <li><текст></li>
<n>-р мөр алга
```
""",
                tests=(
                    TestCaseSpec(
                        stdin="append Хичээл үзэх\nappend Дасгал хийх\nprepend Өглөөний цай\nharah\nremove 2\nharah\n",
                        expected_output="<ul> (3 мөр)\n  <li>Өглөөний цай</li>\n  <li>Хичээл үзэх</li>\n  <li>Дасгал хийх</li>\n<ul> (2 мөр)\n  <li>Өглөөний цай</li>\n  <li>Дасгал хийх</li>\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="olon Алим,Банана,Интоор\nharah\nclear\nharah\n",
                        expected_output="<ul> (3 мөр)\n  <li>Алим</li>\n  <li>Банана</li>\n  <li>Интоор</li>\n<ul> (0 мөр)\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="append А\nremove 3\nremove 1\nremove 1\nharah\n",
                        expected_output="3-р мөр алга\n1-р мөр алга\n<ul> (0 мөр)\n",
                    ),
                    TestCaseSpec(
                        stdin="prepend B\nprepend A\nolon C,D\nappend E\nremove 6\nremove 3\nharah\nclear\nappend F\nharah\n",
                        expected_output="6-р мөр алга\n<ul> (4 мөр)\n  <li>A</li>\n  <li>B</li>\n  <li>D</li>\n  <li>E</li>\n<ul> (1 мөр)\n  <li>F</li>\n",
                    ),
                    TestCaseSpec(
                        stdin="olon Нэг\nolon Хоёр,Гурав\nremove 2\nharah\n",
                        expected_output="<ul> (2 мөр)\n  <li>Нэг</li>\n  <li>Гурав</li>\n",
                    ),
                ),
                solution="""\
// Жагсаалтын (<ul>) зан төлөвийг загварчилъя.
const jagsaalt = {
  huuhduud: [],
  // ...elementuud нь дуудахад өгсөн бүх аргументыг нэг массив болгон
  // цуглуулна — append(a) ч, append(a, b, c) ч ажиллана (Модул 15-д үзнэ).
  append(...elementuud) {
    for (const el of elementuud) {
      el.etseg = this;
      this.huuhduud.push(el);
    }
  },
  prepend(el) {
    el.etseg = this;
    this.huuhduud.unshift(el);
  },
  replaceChildren() {
    this.huuhduud = [];
  },
  harah() {
    console.log(`<ul> (${this.huuhduud.length} мөр)`);
    for (const el of this.huuhduud) {
      console.log(`  <li>${el.textContent}</li>`);
    }
  },
};

function createElement(shoshgo) {
  return {
    shoshgo: shoshgo,
    textContent: "",
    etseg: null,
    // Элемент өөрийгөө эцгийнхээ хүүхдүүдээс хасна
    remove() {
      if (this.etseg) {
        this.etseg.huuhduud = this.etseg.huuhduud.filter((el) => el !== this);
        this.etseg = null;
      }
    },
  };
}

function muruusgeh(text) {
  const li = createElement("li");
  li.textContent = text;
  return li;
}

let mur = prompt();
while (mur !== null) {
  // "append Шинэ мөр" → komand "append", utga "Шинэ мөр"
  const hesguud = mur.split(" ");
  const komand = hesguud[0];
  const utga = hesguud.slice(1).join(" ");

  switch (komand) {
    case "append":
      jagsaalt.append(muruusgeh(utga));
      break;
    case "prepend":
      jagsaalt.prepend(muruusgeh(utga));
      break;
    case "olon": {
      // Эхлээд бүх мөрийг бэлдээд нэг л удаа залгана
      const muruud = utga.split(",").map((text) => muruusgeh(text));
      jagsaalt.append(...muruud);
      break;
    }
    case "remove": {
      const li = jagsaalt.huuhduud[Number(utga) - 1];
      if (li) {
        li.remove();
      } else {
        console.log(`${utga}-р мөр алга`);
      }
      break;
    }
    case "clear":
      jagsaalt.replaceChildren();
      break;
    case "harah":
      jagsaalt.harah();
      break;
  }

  mur = prompt();
}
""",
                tips="""\
- Гурван алхам: `createElement("li")` → `li.textContent = ...` → `jagsaalt.append(li)`.
  Давтагдах тул жижиг функцэд гаргавал амар.
- `n`-р мөр бол `jagsaalt.huuhduud[n - 1]`. Индекс хэтэрвэл `undefined` —
  `if` шалгаад л `remove()` дууд.
- `olon`: `split(",")` + `map`-ээр элементийн массив бэлдээд
  `jagsaalt.append(...muruud)` — `...` массивыг тусдаа аргументууд болгоно.
- `clear`-т `replaceChildren()`.
""",
            ),
        ),
    ],
)

EVENTS = ModuleSpec(
    title="Модул 11 — Үйлдэл (Events)",
    description="Хэрэглэгчийн үйлдэлд хариу үзүүлэх.",
    lessons=[
        LessonSpec(
            title="Event listener",
            slug="event-listener",
            description="addEventListener ашиглан үйлдэл сонсох.",
            duration=420,
            content="""\
Хуудас нь хэрэглэгчийн үйлдлийг **үйл явдал** (event) болгон зарладаг.
JavaScript түүнийг сонсож хариу үзүүлнэ.

```javascript
const tovch = document.querySelector("#hadgalah");

tovch.addEventListener("click", () => {
  console.log("Товч дарагдлаа");
});
```

`addEventListener` нь хоёр зүйл авна:

1. Үйл явдлын **нэр** (`"click"`)
2. Тохиолдоход дуудагдах **функц**

### Түгээмэл үйл явдлууд

| Нэр | Хэзээ |
|---|---|
| `click` | Элемент дээр дарахад |
| `input` | Талбарын утга өөрчлөгдөхөд |
| `change` | Утга өөрчлөгдөж, фокус алдахад |
| `submit` | Форм илгээхэд |
| `keydown` | Товч дарахад |
| `DOMContentLoaded` | HTML бүрэн уншигдахад |

### Сонсогчийг арилгах

```javascript
function hariult() {
  console.log("нэг удаа");
}

tovch.addEventListener("click", hariult);
tovch.removeEventListener("click", hariult);
```

Арилгахын тулд функц нь **нэртэй** байх ёстой — сум функцийг шууд бичвэл
дараа нь заах боломжгүй болно.

Ганц удаа ажиллуулах бол илүү хялбар арга бий:

```javascript
tovch.addEventListener("click", hariult, { once: true });
```

### `onclick`-ээс юугаараа дээр вэ

```javascript
tovch.onclick = hariult; // зөвхөн НЭГ сонсогч
```

`addEventListener` нь нэг үйл явдалд **хэдэн ч** сонсогч нэмэх боломж
олгоно. Тиймээс үүнийг сонго.
""",
            initial_code="""\
// Товчны үйл явдлын жижиг загвар — хөтөчийн addEventListener шиг ажиллана.
const tovch = {
  sonsogchid: [], // { ajil, neg } объектууд, нэмсэн дарааллаар

  addEventListener(turul, ajil, songolt) {
    // Хөтөч ИЖИЛ функцийг хоёр дахь удаа нэмдэггүй
    if (turul !== "click" || this.sonsogchid.find((s) => s.ajil === ajil)) {
      return;
    }
    const neg = songolt ? songolt.once === true : false;
    this.sonsogchid.push({ ajil: ajil, neg: neg });
  },

  removeEventListener(turul, ajil) {
    this.sonsogchid = this.sonsogchid.filter((s) => s.ajil !== ajil);
  },

  // Хөтөч товч дарагдахад үүнийг өөрөө дууддаг. Ажилласан сонсогчийн тоог буцаана.
  darah() {
    const jagsaalt = this.sonsogchid;
    // { once: true } сонсогчийг дуудахаас өмнө хасна
    this.sonsogchid = jagsaalt.filter((s) => !s.neg);
    for (const s of jagsaalt) {
      s.ajil();
    }
    return jagsaalt.length;
  },
};

// TODO: Нэр бүрийн сонсогч функцийг энд хадгална: funktsuud[ner] = ...
const funktsuud = {};

let daraltToo = 0;

let mur = prompt();
while (mur !== null) {
  // "nemeh Хадгалах" → komand "nemeh", ner "Хадгалах"
  const hesguud = mur.split(" ");
  const komand = hesguud[0];
  const ner = hesguud.slice(1).join(" ");

  switch (komand) {
    // TODO: nemeh, neg, hasah командуудыг нэмнэ.

    case "darah": {
      daraltToo++;
      console.log(`--- Даралт ${daraltToo} ---`);
      const ajillasan = tovch.darah();
      if (ajillasan === 0) {
        console.log("(сонсогч алга)");
      }
      break;
    }
  }

  mur = prompt();
}
""",
            exercise=ExerciseSpec(
                statement="""\
Товчны сонсогчдыг командаар нэмж, хас. Товчны загвар (`tovch`) эхлэл кодод
бэлэн — хөтөчийнх шиг `addEventListener`, `removeEventListener`-тэй,
`{ once: true }` сонголтыг ойлгодог, **ижил функцийг** хоёр дахь удаа
нэмдэггүй. Товч дарахыг (`darah`) эхлэл код хийнэ.

| Команд | Үйлдэл |
|---|---|
| `nemeh <нэр>` | `click`-д сонсогч нэмнэ; дуудагдахдаа `<нэр>: ажиллав` гэж хэвлэнэ |
| `neg <нэр>` | мөн адил, гэхдээ `{ once: true }` — ганц л удаа ажиллана |
| `hasah <нэр>` | тэр нэрийн сонсогчийг `removeEventListener`-ээр хасна |
| `darah` | товч дарна |

Нэг нэрд нэг л функц байх ёстой: нэр бүрийн функцийг анх удаа үүсгээд
хадгалж, дараа нь (`hasah`, давтан `nemeh`) **тэр функцээ** дамжуул. Шинээр
үүсгэсэн функцийг хөтөч өөр функц гэж үзнэ — хасахгүй, давхар нэмнэ.

**Оролт:** мөр бүрт нэг команд. Нэр зайтай байж болно.

**Гаралт:** `darah` бүрт гарчиг, дараа нь сонсогчид нэмсэн дарааллаараа
хэвлэнэ. Сонсогч байхгүй бол гарчгийн дор `(сонсогч алга)`:

```text
--- Даралт <дугаар> ---
<нэр>: ажиллав
```
""",
                tests=(
                    TestCaseSpec(
                        stdin="nemeh Хадгалах\nnemeh Мэдэгдэх\ndarah\nhasah Хадгалах\ndarah\n",
                        expected_output="--- Даралт 1 ---\nХадгалах: ажиллав\nМэдэгдэх: ажиллав\n--- Даралт 2 ---\nМэдэгдэх: ажиллав\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="neg Тавтай морил\nnemeh Лог\ndarah\ndarah\n",
                        expected_output="--- Даралт 1 ---\nТавтай морил: ажиллав\nЛог: ажиллав\n--- Даралт 2 ---\nЛог: ажиллав\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="nemeh A\nnemeh A\nhasah B\ndarah\nhasah A\ndarah\n",
                        expected_output="--- Даралт 1 ---\nA: ажиллав\n--- Даралт 2 ---\n(сонсогч алга)\n",
                    ),
                    TestCaseSpec(
                        stdin="neg Нэг\nhasah Нэг\ndarah\nnemeh Нэг\ndarah\ndarah\n",
                        expected_output="--- Даралт 1 ---\n(сонсогч алга)\n--- Даралт 2 ---\nНэг: ажиллав\n--- Даралт 3 ---\nНэг: ажиллав\n",
                    ),
                    TestCaseSpec(
                        stdin="nemeh Гурав\nnemeh Нэг\nnemeh Хоёр\nhasah Нэг\ndarah\n",
                        expected_output="--- Даралт 1 ---\nГурав: ажиллав\nХоёр: ажиллав\n",
                    ),
                ),
                solution="""\
// Товчны үйл явдлын жижиг загвар — хөтөчийн addEventListener шиг ажиллана.
const tovch = {
  sonsogchid: [], // { ajil, neg } объектууд, нэмсэн дарааллаар

  addEventListener(turul, ajil, songolt) {
    // Хөтөч ИЖИЛ функцийг хоёр дахь удаа нэмдэггүй
    if (turul !== "click" || this.sonsogchid.find((s) => s.ajil === ajil)) {
      return;
    }
    const neg = songolt ? songolt.once === true : false;
    this.sonsogchid.push({ ajil: ajil, neg: neg });
  },

  removeEventListener(turul, ajil) {
    this.sonsogchid = this.sonsogchid.filter((s) => s.ajil !== ajil);
  },

  // Хөтөч товч дарагдахад үүнийг өөрөө дууддаг. Ажилласан сонсогчийн тоог буцаана.
  darah() {
    const jagsaalt = this.sonsogchid;
    // { once: true } сонсогчийг дуудахаас өмнө хасна
    this.sonsogchid = jagsaalt.filter((s) => !s.neg);
    for (const s of jagsaalt) {
      s.ajil();
    }
    return jagsaalt.length;
  },
};

// Нэр бүрийн сонсогч функц — нэг нэрд нэг л функц үүснэ
const funktsuud = {};

function funktsAvah(ner) {
  if (!funktsuud[ner]) {
    funktsuud[ner] = () => console.log(`${ner}: ажиллав`);
  }
  return funktsuud[ner];
}

let daraltToo = 0;

let mur = prompt();
while (mur !== null) {
  // "nemeh Хадгалах" → komand "nemeh", ner "Хадгалах"
  const hesguud = mur.split(" ");
  const komand = hesguud[0];
  const ner = hesguud.slice(1).join(" ");

  switch (komand) {
    case "nemeh":
      tovch.addEventListener("click", funktsAvah(ner));
      break;
    case "neg":
      tovch.addEventListener("click", funktsAvah(ner), { once: true });
      break;
    case "hasah":
      // Нэмсэн ТЭР функцийг дамжуулна — шинэ функц хасагдахгүй
      tovch.removeEventListener("click", funktsAvah(ner));
      break;

    case "darah": {
      daraltToo++;
      console.log(`--- Даралт ${daraltToo} ---`);
      const ajillasan = tovch.darah();
      if (ajillasan === 0) {
        console.log("(сонсогч алга)");
      }
      break;
    }
  }

  mur = prompt();
}
""",
                tips="""\
- Функцүүдийг объектод нэрээр нь хадгал: `funktsuud[ner] = () => console.log(...)`.
- Үүсгэхээсээ өмнө `if (!funktsuud[ner])` гэж шалга — байгаа бол **тэрийгээ**
  ашигла. Ингэвэл давтан `nemeh` хийхэд хөтөч давхар нэмэхгүй.
- `hasah`-д `tovch.removeEventListener("click", funktsuud[ner])` — нэмсэн тэр л
  функц. Шинэ сум функц бичвэл хасагдахгүй.
- `neg`: `tovch.addEventListener("click", funkts, { once: true })`.
- Сум функц бүр үүссэн үеийнхээ `ner`-ийг хэвлэнэ.
""",
            ),
        ),
        LessonSpec(
            title="Click ба input үйлдэл",
            slug="click-ba-input-uildel",
            description="Товч дарах, талбарт бичихэд хариу үзүүлэх.",
            duration=420,
            content="""\
### Click

```javascript
const tovch = document.querySelector("#nemeh");
let toolol = 0;

tovch.addEventListener("click", () => {
  toolol++;
  document.querySelector("#toolol").textContent = toolol;
});
```

### Input

Бичих бүрт ажиллана:

```javascript
const talbar = document.querySelector("#haih");

talbar.addEventListener("input", (event) => {
  console.log(event.target.value);
});
```

Сонсогч функц нь `event` гэсэн объект хүлээн авдаг. `event.target` нь
үйлдэл болсон элемент — энд бол талбар өөрөө, `.value` нь түүний одоогийн
утга. `event` объектыг дараагийн хичээлд дэлгэрэнгүй үзнэ.

`change` нь зөвхөн фокус алдахад ажиллана. Шууд хайлтад `input`, харин
`select` цэсэнд `change` тохиромжтой.

### Утга үргэлж мөр

```javascript
const too = talbar.value;        // "42" — мөр!
const zuv = Number(talbar.value); // 42 — тоо
```

Энэ бол формтой ажиллахад гардаг хамгийн олон алдаа.

### Хэт олон дуудалтыг сааруулах

Бичих бүрт сервер рүү хүсэлт явуулах нь үрэлгэн. Хэрэглэгч бичихээ
болих хүртэл хүлээх аргыг *debounce* гэнэ. Үүнд хөтчийн хоёр функц
хэрэгтэй:

- `setTimeout(функц, 300)` — функцийг **300 миллисекундын дараа** дуудна.
  Хүлээлтийн дугаарыг буцаана.
- `clearTimeout(дугаар)` — хараахан болоогүй хүлээлтийг цуцална.

```javascript
let tsag;

talbar.addEventListener("input", (event) => {
  clearTimeout(tsag);
  tsag = setTimeout(() => haih(event.target.value), 300);
});
```

`clearTimeout` нь өмнөх хүлээлтийг цуцалдаг тул зөвхөн **сүүлийн**
дуудалт ажиллана.
""",
            initial_code="""\
// Хуудасны элементийн жижиг загвар: утга, текст, сонсогчидтой.
function element(ner) {
  return {
    ner: ner,
    value: "",
    textContent: "",
    sonsogchid: {}, // үйл явдлын нэр → функцүүдийн массив
    addEventListener(turul, ajil) {
      if (!this.sonsogchid[turul]) {
        this.sonsogchid[turul] = [];
      }
      this.sonsogchid[turul].push(ajil);
    },
    // Үйлдэл болоход хөтөч сонсогч бүрийг event объекттой дууддаг.
    dispatch(turul) {
      const event = { type: turul, target: this };
      for (const ajil of this.sonsogchid[turul] || []) {
        ajil(event);
      }
    },
  };
}

const alhamTalbar = element("alham"); // <input id="alham">
const tovch = element("nemeh"); // <button id="nemeh">
const delgets = element("toolol"); // <span id="toolol">
delgets.textContent = "0";

// ---- Чиний код ----
let alham = 1;
let toolol = 0;

// TODO: alhamTalbar-т "input" сонсогч нэмнэ.
// TODO: tovch-т "click" сонсогч нэмнэ.

// ---- Хэрэглэгчийн үйлдлийг дуурайна — энэ хэсгийг бүү өөрчил ----
let mur = prompt();
while (mur !== null) {
  if (mur === "darah") {
    tovch.dispatch("click");
  } else {
    // "bichih 5" → талбарт "5" бичээд input үйл явдал үүснэ
    alhamTalbar.value = mur.split(" ").slice(1).join(" ");
    alhamTalbar.dispatch("input");
  }
  mur = prompt();
}
console.log(`Дэлгэц: ${delgets.textContent}`);
""",
            exercise=ExerciseSpec(
                statement="""\
Алхамтай тоолуур бич. Хуудсанд гурван элемент бий (загвар нь эхлэл кодод):
алхмын талбар `alhamTalbar` (`<input>`), товч `tovch`, тоолуур харуулах
`delgets`. Хэрэглэгчийн үйлдлийг (бичих, дарах) эхлэл код дуурайна — чи
зөвхөн **сонсогчдыг** бич.

- `alhamTalbar`-ийн `input` сонсогч: `event.target.value`-г тоо болго. Тоо бол
  алхмыг шинэчилж `Алхам: <алхам>`, тоо биш бол (`NaN`) алхмыг хэвээр үлдээж
  `Алхам тоо биш: <бичсэн утга>` гэж хэвлэ.
- `tovch`-ийн `click` сонсогч: тоолуурыг алхмаар нэмэгдүүлж,
  `delgets.textContent`-д бичээд `Тоолуур: <утга>` гэж хэвлэ.

Эхэндээ алхам `1`, тоолуур `0`.

**Оролт:** мөр бүрт нэг үйлдэл — `darah` (товч дарах) эсвэл `bichih <утга>`
(талбарт утга бичих).

**Гаралт:** сонсогчдын хэвлэсэн мөрүүд, эцэст нь эхлэл код дэлгэцийг хэвлэнэ:

```text
Алхам: <алхам>
Тоолуур: <утга>
...
Дэлгэц: <delgets.textContent>
```
""",
                tests=(
                    TestCaseSpec(
                        stdin="darah\ndarah\nbichih 5\ndarah\n",
                        expected_output="Тоолуур: 1\nТоолуур: 2\nАлхам: 5\nТоолуур: 7\nДэлгэц: 7\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="bichih 10\nbichih abc\ndarah\n",
                        expected_output="Алхам: 10\nАлхам тоо биш: abc\nТоолуур: 10\nДэлгэц: 10\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="bichih -3\ndarah\ndarah\n",
                        expected_output="Алхам: -3\nТоолуур: -3\nТоолуур: -6\nДэлгэц: -6\n",
                    ),
                    TestCaseSpec(
                        stdin="bichih 2.5\ndarah\nbichih 0\ndarah\ndarah\n",
                        expected_output="Алхам: 2.5\nТоолуур: 2.5\nАлхам: 0\nТоолуур: 2.5\nТоолуур: 2.5\nДэлгэц: 2.5\n",
                    ),
                    TestCaseSpec(
                        stdin="bichih 12abc\nbichih 7\ndarah\ndarah\ndarah\n",
                        expected_output="Алхам тоо биш: 12abc\nАлхам: 7\nТоолуур: 7\nТоолуур: 14\nТоолуур: 21\nДэлгэц: 21\n",
                    ),
                ),
                solution="""\
// Хуудасны элементийн жижиг загвар: утга, текст, сонсогчидтой.
function element(ner) {
  return {
    ner: ner,
    value: "",
    textContent: "",
    sonsogchid: {}, // үйл явдлын нэр → функцүүдийн массив
    addEventListener(turul, ajil) {
      if (!this.sonsogchid[turul]) {
        this.sonsogchid[turul] = [];
      }
      this.sonsogchid[turul].push(ajil);
    },
    // Үйлдэл болоход хөтөч сонсогч бүрийг event объекттой дууддаг.
    dispatch(turul) {
      const event = { type: turul, target: this };
      for (const ajil of this.sonsogchid[turul] || []) {
        ajil(event);
      }
    },
  };
}

const alhamTalbar = element("alham"); // <input id="alham">
const tovch = element("nemeh"); // <button id="nemeh">
const delgets = element("toolol"); // <span id="toolol">
delgets.textContent = "0";

let alham = 1;
let toolol = 0;

alhamTalbar.addEventListener("input", (event) => {
  // Талбарын утга үргэлж мөр — тоо болгож шалгана
  const utga = Number(event.target.value);
  if (Number.isNaN(utga)) {
    console.log(`Алхам тоо биш: ${event.target.value}`);
  } else {
    alham = utga;
    console.log(`Алхам: ${alham}`);
  }
});

tovch.addEventListener("click", () => {
  toolol += alham;
  delgets.textContent = String(toolol);
  console.log(`Тоолуур: ${toolol}`);
});

// ---- Хэрэглэгчийн үйлдлийг дуурайна — энэ хэсгийг бүү өөрчил ----
let mur = prompt();
while (mur !== null) {
  if (mur === "darah") {
    tovch.dispatch("click");
  } else {
    // "bichih 5" → талбарт "5" бичээд input үйл явдал үүснэ
    alhamTalbar.value = mur.split(" ").slice(1).join(" ");
    alhamTalbar.dispatch("input");
  }
  mur = prompt();
}
console.log(`Дэлгэц: ${delgets.textContent}`);
""",
                tips="""\
- `event.target` нь үйлдэл болсон элемент — энд талбар өөрөө. `.value` нь
  үргэлж **мөр**.
- `Number("5")` → `5`, `Number("abc")` → `NaN`. `NaN`-ийг
  `Number.isNaN(...)`-ээр шалга — `=== NaN` хэзээ ч `true` болохгүй.
- `Number()`-гүй бол `0 + "5"` → `"05"` — тоолуур мөр болж хувирна.
- `alham`, `toolol` сонсогчоос **гадна** зарлагдсан — сонсогч дотор шинээр
  `let` бичвэл дуудалт бүрт утгаа мартна.
- `delgets.textContent`-д `String(toolol)` гэх мэтээр мөр бич — жинхэнэ DOM-д
  `textContent` үргэлж мөр.
""",
            ),
        ),
        LessonSpec(
            title="Event объект",
            slug="event-obyekt",
            description="target, preventDefault, дэгдэлт (bubbling).",
            duration=450,
            content="""\
Сонсогч функц нь **event объект** хүлээн авна. Түүнд юу болсон тухай
бүх мэдээлэл байна.

```javascript
tovch.addEventListener("click", (event) => {
  console.log(event.type);   // "click"
  console.log(event.target); // дарагдсан элемент
});
```

### Хамгийн хэрэгтэй талбарууд

| Талбар | Утга |
|---|---|
| `event.target` | Үйлдэл **эхэлсэн** элемент |
| `event.currentTarget` | Сонсогч **хавсаргасан** элемент |
| `event.type` | Үйл явдлын нэр |
| `event.key` | Дарагдсан товчны нэр |

### `preventDefault`

Хөтчийн анхдагч үйлдлийг зогсооно:

```javascript
form.addEventListener("submit", (event) => {
  event.preventDefault(); // хуудас дахин ачаалагдахаас сэргийлнэ
  // ...өөрийн кодоо ажиллуулна
});
```

Холбоос дээр дарахад шилжихээс сэргийлэхэд ч ашиглана.

### Дэгдэлт (bubbling)

Үйл явдал дотроос гадагш, эцэг элементүүдээрээ **дээшээ дамжина**:

```text
li дээр дарлаа
  → li сонсогч
  → ul сонсогч
  → body сонсогч
```

### Төлөөлөгч сонсогч (delegation)

Дэгдэлтийг ашиглан **нэг** сонсогчоор олон хүүхдийг удирдана:

```javascript
jagsaalt.addEventListener("click", (event) => {
  if (event.target.matches(".ustgah")) {
    event.target.closest("li").remove();
  }
});
```

`matches(".ustgah")` нь элемент тухайн CSS сонгогчтой таарч байгаа эсэхийг
(`true`/`false`), `closest("li")` нь элементээс дээш явж хамгийн ойрын
`li`-г олно.

Энэ нь хожим нэмэгдсэн мөрүүдэд ч ажиллана — тэдэнд тусад нь сонсогч
хавсаргах шаардлагагүй. Урт жагсаалтад маш их ялгаа гаргана.

### Дэгдэлтийг зогсоох

```javascript
event.stopPropagation();
```

Ховор хэрэгтэй. Хэрэглэхээсээ өмнө үнэхээр шаардлагатай эсэхийг бод —
энэ нь бусад сонсогчийг чимээгүйхэн тасалж, дараа нь олоход хэцүү алдаа
үүсгэдэг.
""",
            initial_code="""\
// Элементийн жижиг загвар. etseg нь эцэг элемент, huuhduud нь хүүхдүүд.
function element(shoshgo, angi, text, etseg) {
  const el = {
    shoshgo: shoshgo,
    angi: angi,
    textContent: text,
    etseg: etseg,
    huuhduud: [],
    sonsogchid: [],
    addEventListener(turul, ajil) {
      this.sonsogchid.push(ajil);
    },
    // ".ner" → класс нь "ner" эсэх, "li" → шошго нь "li" эсэх
    matches(songogch) {
      if (songogch.startsWith(".")) {
        return this.angi === songogch.slice(1);
      }
      return this.shoshgo === songogch;
    },
    // Өөрөөсөө эхлэн дээш явж тэр шошготой хамгийн ойрын элементийг олно
    closest(shoshgo) {
      let odoo = this;
      while (odoo && odoo.shoshgo !== shoshgo) {
        odoo = odoo.etseg;
      }
      return odoo || null;
    },
    // Өөрийгөө эцгийнхээ хүүхдүүдээс хасна
    remove() {
      if (this.etseg) {
        this.etseg.huuhduud = this.etseg.huuhduud.filter((h) => h !== this);
        this.etseg = null;
      }
    },
  };
  if (etseg) {
    etseg.huuhduud.push(el);
  }
  return el;
}

// Хөтөч даралтыг ингэж дэгдээдэг: target-аас эхлэн эцэг рүү дээшилнэ.
function darah(target) {
  const event = {
    type: "click",
    target: target,
    currentTarget: null,
    zogsson: false,
    stopPropagation() {
      this.zogsson = true;
    },
  };
  let odoo = target;
  while (odoo && !event.zogsson) {
    event.currentTarget = odoo;
    for (const ajil of odoo.sonsogchid) {
      ajil(event);
    }
    odoo = odoo.etseg;
  }
}

const body = element("body", "", "", null);
const ul = element("ul", "jagsaalt", "", body);

// Эхний мөрийн бараа бүрт: li > span.ner + button.ustgah. Энгийн болгохын
// тулд li-ийн textContent нь зөвхөн барааны нэр.
for (const ner of prompt().split(",")) {
  const li = element("li", "mur", ner, ul);
  element("span", "ner", ner, li);
  element("button", "ustgah", "×", li);
}

body.addEventListener("click", (event) => {
  console.log(`body: ${event.target.shoshgo} дээр дарлаа`);
});

// ---- Чиний код ----
// TODO: ul-д ганц "click" сонсогч нэмнэ (төлөөлөгч сонсогч).
//       event.target нь ".ustgah" эсвэл ".ner" эсэхийг matches-ээр шалгана.

// ---- Хэрэглэгчийн даралтыг дуурайна — энэ хэсгийг бүү өөрчил ----
let mur = prompt();
while (mur !== null) {
  // "ner 2" → 2-р мөрийн нэр дээр, "ustgah 1" → 1-р мөрийн товч дээр
  const [uildel, dugaar] = mur.split(" ");
  if (uildel === "ul") {
    darah(ul);
  } else {
    const li = ul.huuhduud[Number(dugaar) - 1];
    if (!li) {
      console.log(`${dugaar}-р мөр алга`);
    } else if (uildel === "ner") {
      darah(li.huuhduud[0]);
    } else {
      darah(li.huuhduud[1]);
    }
  }
  mur = prompt();
}

const uldsen = ul.huuhduud.map((li) => li.textContent);
console.log(`Үлдсэн: ${uldsen.length > 0 ? uldsen.join(", ") : "(хоосон)"}`);
""",
            exercise=ExerciseSpec(
                statement="""\
Дэлгүүрийн жагсаалтыг **нэг** төлөөлөгч сонсогчоор удирд. Хуудасны мод:
`body` → `ul` → мөр бүр `li`, түүний дотор нэр (`span.ner`) ба устгах товч
(`button.ustgah`). Загвар нь эхлэл кодод: элемент бүр `shoshgo`,
`textContent`, `addEventListener`, `matches(".класс")`, `closest("шошго")`,
`remove()`-тэй. Даралт `target`-аас эцэг рүү дэгдэнэ (`span` → `li` → `ul` →
`body`). `body`-ийн сонсогч бэлэн: хүрч ирсэн даралт бүрт
`body: <target-ийн шошго> дээр дарлаа` гэж хэвлэнэ.

`ul`-д ганц `click` сонсогч нэм:

- `event.target` нь `.ustgah` бол түүний `li`-г (`closest("li")`) устгаж,
  `Устгалаа: <li-ийн textContent>` гэж хэвлээд `event.stopPropagation()`
  дууд — устгах даралт `body`-д хүрэхгүй.
- `event.target` нь `.ner` бол
  `Сонгосон: <нэр> (target: <target-ийн шошго>, currentTarget: <currentTarget-ийн шошго>)`
  гэж хэвлэ. Энэ даралт `body` хүртэл дэгдэнэ.
- `ul`-ийн хоосон зайд дарвал юу ч хийхгүй.

**Оролт:** эхний мөрөнд таслалаар тусгаарласан барааны нэрс. Дараагийн мөр бүр
нэг даралт: `ner <n>` (n-р мөрийн нэр дээр), `ustgah <n>` (n-р мөрийн товч
дээр), `ul` (жагсаалтын хоосон зайд). `n` нь одоогийн жагсаалтад 1-ээс
тоологдоно.

**Гаралт:** сонсогчдын хэвлэсэн мөрүүд (байхгүй мөр дээр эхлэл код
`<n>-р мөр алга` гэж хэвлэнэ), эцэст нь эхлэл код үлдсэн барааг хэвлэнэ:

```text
Сонгосон: <нэр> (target: span, currentTarget: ul)
body: span дээр дарлаа
Устгалаа: <нэр>
Үлдсэн: <нэр>, <нэр>
```
""",
                tests=(
                    TestCaseSpec(
                        stdin="Сүү,Талх,Өндөг\nner 2\nustgah 1\n",
                        expected_output="Сонгосон: Талх (target: span, currentTarget: ul)\nbody: span дээр дарлаа\nУстгалаа: Сүү\nҮлдсэн: Талх, Өндөг\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="Алим,Банана\nul\nustgah 2\nustgah 1\n",
                        expected_output="body: ul дээр дарлаа\nУстгалаа: Банана\nУстгалаа: Алим\nҮлдсэн: (хоосон)\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="Ном,Дэвтэр,Үзэг,Харандаа\nustgah 3\nner 3\nner 1\nustgah 5\n",
                        expected_output="Устгалаа: Үзэг\nСонгосон: Харандаа (target: span, currentTarget: ul)\nbody: span дээр дарлаа\nСонгосон: Ном (target: span, currentTarget: ul)\nbody: span дээр дарлаа\n5-р мөр алга\nҮлдсэн: Ном, Дэвтэр, Харандаа\n",
                    ),
                    TestCaseSpec(
                        stdin="Нэг\nner 1\nner 1\nul\n",
                        expected_output="Сонгосон: Нэг (target: span, currentTarget: ul)\nbody: span дээр дарлаа\nСонгосон: Нэг (target: span, currentTarget: ul)\nbody: span дээр дарлаа\nbody: ul дээр дарлаа\nҮлдсэн: Нэг\n",
                    ),
                    TestCaseSpec(
                        stdin="А,Б,В\nustgah 1\nustgah 1\nner 1\n",
                        expected_output="Устгалаа: А\nУстгалаа: Б\nСонгосон: В (target: span, currentTarget: ul)\nbody: span дээр дарлаа\nҮлдсэн: В\n",
                    ),
                ),
                solution="""\
// Элементийн жижиг загвар. etseg нь эцэг элемент, huuhduud нь хүүхдүүд.
function element(shoshgo, angi, text, etseg) {
  const el = {
    shoshgo: shoshgo,
    angi: angi,
    textContent: text,
    etseg: etseg,
    huuhduud: [],
    sonsogchid: [],
    addEventListener(turul, ajil) {
      this.sonsogchid.push(ajil);
    },
    // ".ner" → класс нь "ner" эсэх, "li" → шошго нь "li" эсэх
    matches(songogch) {
      if (songogch.startsWith(".")) {
        return this.angi === songogch.slice(1);
      }
      return this.shoshgo === songogch;
    },
    // Өөрөөсөө эхлэн дээш явж тэр шошготой хамгийн ойрын элементийг олно
    closest(shoshgo) {
      let odoo = this;
      while (odoo && odoo.shoshgo !== shoshgo) {
        odoo = odoo.etseg;
      }
      return odoo || null;
    },
    // Өөрийгөө эцгийнхээ хүүхдүүдээс хасна
    remove() {
      if (this.etseg) {
        this.etseg.huuhduud = this.etseg.huuhduud.filter((h) => h !== this);
        this.etseg = null;
      }
    },
  };
  if (etseg) {
    etseg.huuhduud.push(el);
  }
  return el;
}

// Хөтөч даралтыг ингэж дэгдээдэг: target-аас эхлэн эцэг рүү дээшилнэ.
function darah(target) {
  const event = {
    type: "click",
    target: target,
    currentTarget: null,
    zogsson: false,
    stopPropagation() {
      this.zogsson = true;
    },
  };
  let odoo = target;
  while (odoo && !event.zogsson) {
    event.currentTarget = odoo;
    for (const ajil of odoo.sonsogchid) {
      ajil(event);
    }
    odoo = odoo.etseg;
  }
}

const body = element("body", "", "", null);
const ul = element("ul", "jagsaalt", "", body);

// Эхний мөрийн бараа бүрт: li > span.ner + button.ustgah. Энгийн болгохын
// тулд li-ийн textContent нь зөвхөн барааны нэр.
for (const ner of prompt().split(",")) {
  const li = element("li", "mur", ner, ul);
  element("span", "ner", ner, li);
  element("button", "ustgah", "×", li);
}

body.addEventListener("click", (event) => {
  console.log(`body: ${event.target.shoshgo} дээр дарлаа`);
});

// Ганц сонсогч бүх мөрийг удирдана — хожим нэмэгдсэн мөрд ч ажиллана
ul.addEventListener("click", (event) => {
  if (event.target.matches(".ustgah")) {
    const li = event.target.closest("li");
    console.log(`Устгалаа: ${li.textContent}`);
    li.remove();
    // Устгах даралт body-д хүрэх шаардлагагүй
    event.stopPropagation();
  } else if (event.target.matches(".ner")) {
    console.log(
      `Сонгосон: ${event.target.textContent} (target: ${event.target.shoshgo}, currentTarget: ${event.currentTarget.shoshgo})`,
    );
  }
});

// ---- Хэрэглэгчийн даралтыг дуурайна — энэ хэсгийг бүү өөрчил ----
let mur = prompt();
while (mur !== null) {
  // "ner 2" → 2-р мөрийн нэр дээр, "ustgah 1" → 1-р мөрийн товч дээр
  const [uildel, dugaar] = mur.split(" ");
  if (uildel === "ul") {
    darah(ul);
  } else {
    const li = ul.huuhduud[Number(dugaar) - 1];
    if (!li) {
      console.log(`${dugaar}-р мөр алга`);
    } else if (uildel === "ner") {
      darah(li.huuhduud[0]);
    } else {
      darah(li.huuhduud[1]);
    }
  }
  mur = prompt();
}

const uldsen = ul.huuhduud.map((li) => li.textContent);
console.log(`Үлдсэн: ${uldsen.length > 0 ? uldsen.join(", ") : "(хоосон)"}`);
""",
                tips="""\
- `event.target` нь дарагдсан хамгийн дотор талын элемент (`span` эсвэл
  `button`), `event.currentTarget` нь сонсогч хавсаргасан элемент — энд үргэлж
  `ul`.
- `event.target.matches(".ustgah")` нь `true`/`false` өгнө.
- `event.target.closest("li")` нь товчноос дээш явж мөрийг нь олно —
  `li.remove()` бүхэл мөрийг устгана.
- `stopPropagation()`-ийг зөвхөн устгах үед дууд — нэр дээрх даралт `body`-д
  хүрэх ёстой.
- Мөр бүрт тусдаа сонсогч хэрэггүй: `ul` дээрх ганц сонсогч хүүхдүүдийнхээ
  бүх даралтыг хүлээн авна.
""",
            ),
        ),
    ],
)

FORMS = ModuleSpec(
    title="Модул 12 — Форм (Forms)",
    description="Хэрэглэгчээс өгөгдөл авах, шалгах.",
    lessons=[
        LessonSpec(
            title="Формын утга унших",
            slug="formiin-utga-unshih",
            description="Талбарын утгыг авах, submit үйлдлийг барих.",
            duration=420,
            content="""\
### Талбарын утга

```javascript
const ner = document.querySelector("#ner").value;
const zuvshuurul = document.querySelector("#zuvshuurul").checked;
```

| Талбарын төрөл | Уншиж авах талбар |
|---|---|
| `text`, `email`, `password`, `number` | `value` |
| `checkbox`, `radio` | `checked` |
| `select` | `value` |

### Утга үргэлж мөр

`type="number"` байсан ч `value` нь **мөр**:

```javascript
const nas = Number(document.querySelector("#nas").value);
```

### Submit-ийг барих

```javascript
const form = document.querySelector("#burtgel");

form.addEventListener("submit", (event) => {
  event.preventDefault();

  const ner = form.ner.value;
  console.log("Илгээх:", ner);
});
```

`preventDefault` **заавал** хэрэгтэй — эс бөгөөс хөтөч хуудсыг дахин
ачаалж, таны код хагас дутуу зогсоно.

### `FormData`

Талбар бүрийг нэрлэхийн оронд бүгдийг нэг дор авна:

```javascript
form.addEventListener("submit", (event) => {
  event.preventDefault();

  const ugugdul = Object.fromEntries(new FormData(form));
  console.log(ugugdul); // { ner: "Бат", email: "..." }
});
```

`new FormData(form)` нь формын бүх талбарыг `[нэр, утга]` хосуудаар
цуглуулна. `Object.fromEntries` нь ийм хосуудаас энгийн объект үүсгэнэ.

Ингэхийн тулд талбар бүрт `name` шинж чанар байх ёстой. `id` биш `name`
гэдгийг анхаар — энэ нь олон цаг үрүүлдэг алдаа.

### Талбарыг цэвэрлэх

```javascript
form.reset();
```
""",
            initial_code="""\
// Бүртгэлийн формын жижиг загвар: талбар бүр value (checkbox нь checked)-тэй.
const form = {
  ner: { value: "" },
  nas: { value: "" }, // type="number" ч гэсэн value нь мөр
  email: { value: "" },
  zuvshuurul: { checked: false }, // checkbox
  sonsogchid: [],

  addEventListener(turul, ajil) {
    if (turul === "submit") {
      this.sonsogchid.push(ajil);
    }
  },

  reset() {
    this.ner.value = "";
    this.nas.value = "";
    this.email.value = "";
    this.zuvshuurul.checked = false;
  },
};

// Хөтөч "Илгээх" дарахад ингэж ажиллана: сонсогчдыг дуудаад, анхдагч
// үйлдлийг цуцлаагүй бол хуудсыг дахин ачаална.
function ilgeeh() {
  const event = {
    type: "submit",
    target: form,
    defaultPrevented: false,
    preventDefault() {
      this.defaultPrevented = true;
    },
  };
  for (const ajil of form.sonsogchid) {
    ajil(event);
  }
  if (!event.defaultPrevented) {
    console.log("Хуудас дахин ачаалагдлаа — өгөгдөл алга боллоо!");
  }
}

// ---- Чиний код ----
// TODO: form-д "submit" сонсогч нэмнэ: preventDefault, дөрвөн мөр хэвлэх,
//       эцэст нь form.reset().

// ---- Хэрэглэгчийн үйлдлийг дуурайна — энэ хэсгийг бүү өөрчил ----
let mur = prompt();
while (mur !== null) {
  // "ner Бат Дорж" → талбар "ner", утга "Бат Дорж"
  const hesguud = mur.split(" ");
  const talbar = hesguud[0];
  const utga = hesguud.slice(1).join(" ");

  if (talbar === "ilgeeh") {
    ilgeeh();
  } else if (talbar === "zuvshuurul") {
    form.zuvshuurul.checked = true;
  } else {
    form[talbar].value = utga;
  }
  mur = prompt();
}
""",
            exercise=ExerciseSpec(
                statement="""\
Бүртгэлийн формын `submit`-ийг барьж, талбаруудын утгыг хэвлэ. Формын загвар
(`form`) эхлэл кодод: `form.ner`, `form.nas`, `form.email` нь `value`-тэй,
`form.zuvshuurul` (checkbox) нь `checked`-тэй, мөн `addEventListener`,
`reset()` методтой. Талбарт бичих, «Илгээх» дарахыг эхлэл код дуурайна.

`submit` сонсогч:

1. `event.preventDefault()` дуудна — эс бөгөөс эхлэл код
   `Хуудас дахин ачаалагдлаа — өгөгдөл алга боллоо!` гэж хэвлэнэ.
2. Доорх дөрвөн мөрийг хэвлэнэ. Хоосон талбарын утгын оронд `(хоосон)`, нас
   хоосон бол зөвхөн `Нас: (хоосон)`.
3. `form.reset()`-ээр формыг цэвэрлэнэ.

**Оролт:** мөр бүрт нэг үйлдэл: `ner <утга>`, `nas <утга>`, `email <утга>`
(талбарт бичих), `zuvshuurul` (checkbox чагтлах), `ilgeeh` (формыг илгээх).

**Гаралт:** илгээлт бүрт:

```text
Нэр: <нэр>
Нас: <нас> (ирэх жил <нас + 1>)
Имэйл: <имэйл>
Зөвшөөрөл: <тийм эсвэл үгүй>
```
""",
                tests=(
                    TestCaseSpec(
                        stdin="ner Бат\nnas 20\nemail bat@medleghub.mn\nzuvshuurul\nilgeeh\n",
                        expected_output="Нэр: Бат\nНас: 20 (ирэх жил 21)\nИмэйл: bat@medleghub.mn\nЗөвшөөрөл: тийм\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="ner Сараа\nnas 17\nilgeeh\nemail sara@mail.mn\nilgeeh\n",
                        expected_output="Нэр: Сараа\nНас: 17 (ирэх жил 18)\nИмэйл: (хоосон)\nЗөвшөөрөл: үгүй\nНэр: (хоосон)\nНас: (хоосон)\nИмэйл: sara@mail.mn\nЗөвшөөрөл: үгүй\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="ilgeeh\n",
                        expected_output="Нэр: (хоосон)\nНас: (хоосон)\nИмэйл: (хоосон)\nЗөвшөөрөл: үгүй\n",
                    ),
                    TestCaseSpec(
                        stdin="ner Дорж Батын\nnas 35\nzuvshuurul\nilgeeh\nner Анар\nnas 9\nzuvshuurul\nilgeeh\n",
                        expected_output="Нэр: Дорж Батын\nНас: 35 (ирэх жил 36)\nИмэйл: (хоосон)\nЗөвшөөрөл: тийм\nНэр: Анар\nНас: 9 (ирэх жил 10)\nИмэйл: (хоосон)\nЗөвшөөрөл: тийм\n",
                    ),
                    TestCaseSpec(
                        stdin="nas 0\nemail a@b.mn\nner Ану\nilgeeh\nzuvshuurul\nilgeeh\n",
                        expected_output="Нэр: Ану\nНас: 0 (ирэх жил 1)\nИмэйл: a@b.mn\nЗөвшөөрөл: үгүй\nНэр: (хоосон)\nНас: (хоосон)\nИмэйл: (хоосон)\nЗөвшөөрөл: тийм\n",
                    ),
                ),
                solution="""\
// Бүртгэлийн формын жижиг загвар: талбар бүр value (checkbox нь checked)-тэй.
const form = {
  ner: { value: "" },
  nas: { value: "" }, // type="number" ч гэсэн value нь мөр
  email: { value: "" },
  zuvshuurul: { checked: false }, // checkbox
  sonsogchid: [],

  addEventListener(turul, ajil) {
    if (turul === "submit") {
      this.sonsogchid.push(ajil);
    }
  },

  reset() {
    this.ner.value = "";
    this.nas.value = "";
    this.email.value = "";
    this.zuvshuurul.checked = false;
  },
};

// Хөтөч "Илгээх" дарахад ингэж ажиллана: сонсогчдыг дуудаад, анхдагч
// үйлдлийг цуцлаагүй бол хуудсыг дахин ачаална.
function ilgeeh() {
  const event = {
    type: "submit",
    target: form,
    defaultPrevented: false,
    preventDefault() {
      this.defaultPrevented = true;
    },
  };
  for (const ajil of form.sonsogchid) {
    ajil(event);
  }
  if (!event.defaultPrevented) {
    console.log("Хуудас дахин ачаалагдлаа — өгөгдөл алга боллоо!");
  }
}

// Хоосон талбарт "(хоосон)" гэж харуулна
function haruulah(utga) {
  return utga === "" ? "(хоосон)" : utga;
}

form.addEventListener("submit", (event) => {
  // Эс бөгөөс хөтөч хуудсыг дахин ачаалж, код хагас дутуу зогсоно
  event.preventDefault();

  console.log(`Нэр: ${haruulah(form.ner.value)}`);

  const nasMur = form.nas.value;
  if (nasMur === "") {
    console.log("Нас: (хоосон)");
  } else {
    // value нь мөр — Number()-гүй бол "20" + 1 → "201"
    const nas = Number(nasMur);
    console.log(`Нас: ${nas} (ирэх жил ${nas + 1})`);
  }

  console.log(`Имэйл: ${haruulah(form.email.value)}`);
  console.log(`Зөвшөөрөл: ${form.zuvshuurul.checked ? "тийм" : "үгүй"}`);

  form.reset();
});

// ---- Хэрэглэгчийн үйлдлийг дуурайна — энэ хэсгийг бүү өөрчил ----
let mur = prompt();
while (mur !== null) {
  // "ner Бат Дорж" → талбар "ner", утга "Бат Дорж"
  const hesguud = mur.split(" ");
  const talbar = hesguud[0];
  const utga = hesguud.slice(1).join(" ");

  if (talbar === "ilgeeh") {
    ilgeeh();
  } else if (talbar === "zuvshuurul") {
    form.zuvshuurul.checked = true;
  } else {
    form[talbar].value = utga;
  }
  mur = prompt();
}
""",
                tips="""\
- `form.addEventListener("submit", (event) => { ... })` — эхний мөрөнд
  `event.preventDefault()`.
- `value` нь `type="number"` байсан ч **мөр**: `Number(form.nas.value) + 1`.
  `Number()`-гүй бол `"20" + 1` → `"201"`.
- `checked` нь boolean: `form.zuvshuurul.checked ? "тийм" : "үгүй"`.
- Хоосон эсэх: `value === ""`. Давтагдах шалгалтыг жижиг функцэд гарга.
- `reset()`-ийг хэвлэсний **дараа** дууд — эс бөгөөс хоосон утга хэвлэнэ.
""",
            ),
        ),
        LessonSpec(
            title="Шалгах ба алдаа харуулах",
            slug="formiig-shalgah",
            description="Оруулсан утгыг шалгаж, ойлгомжтой мессеж харуулах.",
            duration=480,
            content="""\
### Хоёр давхарга

| Давхарга | Зорилго |
|---|---|
| Хөтөч дээр | Хэрэглэгчид **хурдан** хариу өгөх |
| Сервер дээр | Өгөгдлийг **үнэхээр** хамгаалах |

> Хөтөч дээрх шалгалтыг хэрэглэгч тойрч гарч чадна. Тиймээс сервер
> талын шалгалт **хэзээ ч** орхигдож болохгүй. Хөтөч дээрх шалгалт нь
> тав тухын зориулалттай, аюулгүй байдлын биш.

### HTML-ийн суурь шалгалт

```html
<input type="email" required minlength="3" />
```

Үнэгүй, хурдан. Гэхдээ мессежийг нь өөрчлөх боломж хязгаартай.

### Гараар шалгах

Алдааг **цуглуулаад** нэг дор харуулах нь дээр:

```javascript
function shalgah(ugugdul) {
  const aldaanuud = {};

  if (!ugugdul.ner.trim()) {
    aldaanuud.ner = "Нэрээ оруулна уу";
  }

  if (!ugugdul.email.includes("@")) {
    aldaanuud.email = "Имэйл хаяг буруу байна";
  }

  if (ugugdul.nuuts.length < 8) {
    aldaanuud.nuuts = "Нууц үг дор хаяж 8 тэмдэгт байна";
  }

  return aldaanuud;
}
```

### Сайн алдааны мессеж

| Муу | Сайн |
|---|---|
| "Алдаа" | "Имэйл хаяг буруу байна" |
| "Буруу утга" | "Нууц үг дор хаяж 8 тэмдэгт байна" |
| "Талбар хоосон" | "Нэрээ оруулна уу" |

Мессеж нь **юу буруу байгааг** биш **юу хийхийг** хэлэх ёстой.

### Хэзээ шалгах вэ

- Бичиж байх үед шалгах нь эвгүй — хараахан дуусаагүй байхад загнана
- Талбараас гарахад (`blur`) шалгах нь тохиромжтой
- Илгээхэд бүгдийг шалгана

### Хүртээмж

Алдааны текстийг талбартай холбоно:

```html
<input id="email" aria-describedby="email-aldaa" aria-invalid="true" />
<p id="email-aldaa">Имэйл хаяг буруу байна</p>
```

Дэлгэц уншигч ингэж л алдааг хэрэглэгчид хэлж чадна.
""",
            initial_code="""\
function shalgah(ugugdul) {
  const aldaanuud = {};

  if (!ugugdul.ner.trim()) {
    aldaanuud.ner = "Нэрээ оруулна уу";
  }

  // TODO: email, nuuts, nas талбаруудыг даалгаврын дүрмээр шалгана.

  return aldaanuud;
}

let mur = prompt();
while (mur !== null) {
  // "Бат|bat@mail.mn|nuutsUg123|20" → дөрвөн талбар
  const [ner, email, nuuts, nas] = mur.split("|");
  const aldaanuud = shalgah({ ner: ner, email: email, nuuts: nuuts, nas: nas });

  // TODO: Алдаагүй бол "✓ Бүртгэл амжилттай", алдаатай бол "✗ 2 алдаа:" ба
  //       алдаа бүрийг "   ner: Нэрээ оруулна уу" хэлбэрээр хэвлэнэ.

  mur = prompt();
}
""",
            exercise=ExerciseSpec(
                statement="""\
Бүртгэлийн өгөгдлийг шалгаж, алдааг нэг дор харуул. `shalgah(ugugdul)` нь
алдаатай талбар бүрийн нэрийг түлхүүр, мессежийг утга болгосон объект
буцаана (алдаагүй бол `{}`). Хүснэгтийн дарааллаар шалгана:

| Талбар | Дүрэм | Мессеж |
|---|---|---|
| `ner` | эхэн, төгсгөлийн зайг хассаны дараа хоосон биш | `Нэрээ оруулна уу` |
| `email` | `@` агуулсан | `Имэйл хаяг буруу байна` |
| `nuuts` | дор хаяж 8 тэмдэгт | `Нууц үг дор хаяж 8 тэмдэгт байна` |
| `nas` | `Number()`-оор хөрвүүлэхэд бүхэл тоо | `Насаа бүхэл тоогоор оруулна уу` |
| `nas` | бүхэл бол 16-аас багагүй | `16 нас хүрсэн байх ёстой` |

Насны хоёр дүрмийн зөвхөн нэг нь л алдаа болно.

**Оролт:** мөр бүрт нэг бүртгэл: `нэр|имэйл|нууц үг|нас` — `|`-ээр
тусгаарласан яг дөрвөн талбар, аль нь ч хоосон байж болно.

**Гаралт:** бүртгэл бүрт алдаагүй бол нэг мөр:

```text
✓ Бүртгэл амжилттай
```

алдаатай бол алдааны тоо, дараа нь алдаа бүр гурван зайн догол мөртэй:

```text
✗ <алдааны тоо> алдаа:
   <талбар>: <мессеж>
```
""",
                tests=(
                    TestCaseSpec(
                        stdin="Бат|bat@medleghub.mn|nuutsUg123|20\n|bat.medleghub.mn|123|хорь\n",
                        expected_output="✓ Бүртгэл амжилттай\n✗ 4 алдаа:\n   ner: Нэрээ оруулна уу\n   email: Имэйл хаяг буруу байна\n   nuuts: Нууц үг дор хаяж 8 тэмдэгт байна\n   nas: Насаа бүхэл тоогоор оруулна уу\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="Сараа|sara@mail.mn|12345678|15\n",
                        expected_output="✗ 1 алдаа:\n   nas: 16 нас хүрсэн байх ёстой\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="   |a@b|abcdefgh|16\n",
                        expected_output="✗ 1 алдаа:\n   ner: Нэрээ оруулна уу\n",
                    ),
                    TestCaseSpec(
                        stdin="Дорж|dorj@mail|1234567|16.5\nАнар|anar@mail.mn|password|99\n",
                        expected_output="✗ 2 алдаа:\n   nuuts: Нууц үг дор хаяж 8 тэмдэгт байна\n   nas: Насаа бүхэл тоогоор оруулна уу\n✓ Бүртгэл амжилттай\n",
                    ),
                    TestCaseSpec(
                        stdin="Ану|anu|секрет123|0\nТэмүүлэн|t@m.mn|12345678|18\nЗаяа|z@z|1|abc\n",
                        expected_output="✗ 2 алдаа:\n   email: Имэйл хаяг буруу байна\n   nas: 16 нас хүрсэн байх ёстой\n✓ Бүртгэл амжилттай\n✗ 2 алдаа:\n   nuuts: Нууц үг дор хаяж 8 тэмдэгт байна\n   nas: Насаа бүхэл тоогоор оруулна уу\n",
                    ),
                ),
                solution="""\
function shalgah(ugugdul) {
  const aldaanuud = {};

  if (!ugugdul.ner.trim()) {
    aldaanuud.ner = "Нэрээ оруулна уу";
  }

  if (!ugugdul.email.includes("@")) {
    aldaanuud.email = "Имэйл хаяг буруу байна";
  }

  if (ugugdul.nuuts.length < 8) {
    aldaanuud.nuuts = "Нууц үг дор хаяж 8 тэмдэгт байна";
  }

  // Number.isInteger нь бүхэл тоо эсэхийг шалгана. "хорь" → NaN → false.
  const nas = Number(ugugdul.nas);
  if (!Number.isInteger(nas)) {
    aldaanuud.nas = "Насаа бүхэл тоогоор оруулна уу";
  } else if (nas < 16) {
    aldaanuud.nas = "16 нас хүрсэн байх ёстой";
  }

  return aldaanuud;
}

let mur = prompt();
while (mur !== null) {
  // "Бат|bat@mail.mn|nuutsUg123|20" → дөрвөн талбар
  const [ner, email, nuuts, nas] = mur.split("|");
  const aldaanuud = shalgah({ ner: ner, email: email, nuuts: nuuts, nas: nas });

  const too = Object.keys(aldaanuud).length;

  if (too === 0) {
    console.log("✓ Бүртгэл амжилттай");
  } else {
    console.log(`✗ ${too} алдаа:`);
    for (const [talbar, messej] of Object.entries(aldaanuud)) {
      console.log(`   ${talbar}: ${messej}`);
    }
  }

  mur = prompt();
}
""",
                tips="""\
- `!ugugdul.ner.trim()` — зөвхөн зайтай нэр ч хоосон мөр болж, falsy гарна.
- `Number.isInteger(Number("16.5"))` → `false`, `Number("хорь")` → `NaN` →
  `false`. Бүхэл бол л `nas < 16`-г шалга — `if` / `else if`.
- Алдааг объектод **цуглуул**: `aldaanuud.email = "..."`. Талбарууд нэмсэн
  дарааллаараа хадгалагдана.
- Алдааны тоо: `Object.keys(aldaanuud).length`. Хэвлэхдээ
  `Object.entries(aldaanuud)`-ийн `[талбар, мессеж]` хосуудыг дамж.
- ✓, ✗ тэмдгийг эхлэл кодын тайлбараас хуулж ав.
""",
            ),
        ),
    ],
)

STORAGE = ModuleSpec(
    title="Модул 13 — Хөтчийн хадгалалт",
    description="Өгөгдлийг хэрэглэгчийн хөтөчид үлдээх.",
    lessons=[
        LessonSpec(
            title="localStorage ба sessionStorage",
            slug="local-storage-ba-session-storage",
            description="Хуудас сэргээсэн ч алга болохгүй өгөгдөл.",
            duration=420,
            content="""\
Хөтөч нь жижиг өгөгдлийг хадгалах хоёр сан өгдөг.

| Сан | Хэдий болтол үлдэх |
|---|---|
| `localStorage` | Устгах хүртэл — хөтөч хаагдсан ч үлдэнэ |
| `sessionStorage` | Таб хаагдах хүртэл |

### Үндсэн дөрвөн үйлдэл

```javascript
localStorage.setItem("hel", "mn");
const hel = localStorage.getItem("hel"); // "mn"
localStorage.removeItem("hel");
localStorage.clear(); // бүгдийг
```

### Зөвхөн мөр хадгална

Энэ бол хамгийн чухал хязгаарлалт:

```javascript
localStorage.setItem("nas", 20);
console.log(localStorage.getItem("nas")); // "20" — МӨР!
```

Объект хадгалах гэвэл ойлгомжгүй үр дүн гарна:

```javascript
localStorage.setItem("hereglegch", { ner: "Бат" });
console.log(localStorage.getItem("hereglegch")); // "[object Object]"
```

Шийдэл нь JSON — дараагийн хичээлээр үзнэ.

### Байхгүй түлхүүр

`null` буцаана, алдаа заахгүй. Тиймээс Модул 2-т үзсэн `||`-ээр анхдагч
утга өгч болно:

```javascript
console.log(localStorage.getItem("baihgui")); // null
const hel = localStorage.getItem("hel") || "mn"; // хадгалаагүй бол "mn"
```

### Юуг хадгалж болохгүй вэ

> Нууц үг, токен, картын дугаар зэргийг `localStorage`-д **хэзээ ч** бүү
> хадгал. Хуудсан дээр ажиллаж буй ямар ч script түүнийг уншиж чадна.

Тохиромжтой зүйлс: харанхуй горим асаалттай эсэх, сүүлд үзсэн хуудас,
хадгалагдаагүй ноорог.

### Багтаамж

Домэйн тутамд 5 MB орчим. Хэтэрвэл алдаа шиднэ. Хэрэглэгч мөн хөтчийн
өгөгдлийг цэвэрлэж болно — тиймээс хадгалалтад **найдаж болохгүй**.
""",
            initial_code="""\
// Worker дотор жинхэнэ сан байхгүй тул ижил методтой загвар бичье.
function sanUusgeh() {
  return {
    ugugdul: {}, // түлхүүр → мөр

    setItem(tulhuur, utga) {
      this.ugugdul[tulhuur] = String(utga); // үргэлж мөр болгоно
    },
    getItem(tulhuur) {
      return tulhuur in this.ugugdul ? this.ugugdul[tulhuur] : null;
    },
    removeItem(tulhuur) {
      delete this.ugugdul[tulhuur];
    },
    clear() {
      this.ugugdul = {};
    },
  };
}

const localStorage = sanUusgeh(); // хөтөч хаагдсан ч үлдэнэ
const sessionStorage = sanUusgeh(); // таб хаагдах хүртэл

// ---- Чиний код ----
function huudasAchaalah() {
  // TODO: "uzsen" (localStorage), "tabUzsen" (sessionStorage)-ийг 1-ээр нэмж
  //       хадгалаад "Зочилсон: 1 удаа (энэ табд 1), хэл: mn" гэж хэвлэнэ.
}

function helSongoh(kod) {
  // TODO: localStorage-д "hel" түлхүүрээр хадгална.
}

function helUstgah() {
  // TODO: "hel"-ийг устгана.
}

// ---- Хэрэглэгчийн үйлдлийг дуурайна — энэ хэсгийг бүү өөрчил ----
let mur = prompt();
while (mur !== null) {
  const hesguud = mur.split(" ");
  const komand = hesguud[0];

  if (komand === "achaalah") {
    huudasAchaalah();
  } else if (komand === "hel") {
    helSongoh(hesguud[1]);
  } else if (komand === "hel-ustgah") {
    helUstgah();
  } else if (komand === "tab-haah") {
    sessionStorage.clear(); // шинэ таб — sessionStorage хоосон
  } else if (komand === "buh-ustgah") {
    localStorage.clear(); // хэрэглэгч хөтчийн өгөгдлөө цэвэрлэв
  }
  mur = prompt();
}
""",
            exercise=ExerciseSpec(
                statement="""\
Зочилсон тоо ба хэлний тохиргоог хөтчийн санд хадгал. `localStorage`,
`sessionStorage`-ийн загвар эхлэл кодод бэлэн: `setItem`, `getItem`,
`removeItem`, `clear` — жинхэнэ шигээ зөвхөн **мөр** хадгалж, байхгүй
түлхүүрт `null` буцаана. Хэрэглэгчийн үйлдлийг эхлэл код дуурайна; чи гурван
функцийг бич:

- `huudasAchaalah()` — хуудас ачаалагдах бүрт дуудагдана. `localStorage`-ийн
  `"uzsen"` (нийт зочилсон) ба `sessionStorage`-ийн `"tabUzsen"` (энэ табд)
  тоог 1-ээр нэмж хадгалаад доорх мөрийг хэвлэнэ. Хэл хадгалаагүй бол `mn`.
- `helSongoh(kod)` — `localStorage`-д `"hel"` түлхүүрээр хадгална.
- `helUstgah()` — `"hel"`-ийг устгана.

**Оролт:** мөр бүрт нэг үйлдэл: `achaalah` (хуудас ачаалах), `hel <код>` (хэл
сонгох), `hel-ustgah` (хэлийг устгах), `tab-haah` (таб хааж шинээр нээх —
`sessionStorage` цэвэрлэгдэнэ), `buh-ustgah` (хөтчийн өгөгдлөө устгах —
`localStorage` цэвэрлэгдэнэ).

**Гаралт:** ачаалалт бүрт нэг мөр:

```text
Зочилсон: <нийт> удаа (энэ табд <табын тоо>), хэл: <хэл>
```
""",
                tests=(
                    TestCaseSpec(
                        stdin="achaalah\nachaalah\ntab-haah\nachaalah\n",
                        expected_output="Зочилсон: 1 удаа (энэ табд 1), хэл: mn\nЗочилсон: 2 удаа (энэ табд 2), хэл: mn\nЗочилсон: 3 удаа (энэ табд 1), хэл: mn\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="hel en\nachaalah\nhel-ustgah\nachaalah\n",
                        expected_output="Зочилсон: 1 удаа (энэ табд 1), хэл: en\nЗочилсон: 2 удаа (энэ табд 2), хэл: mn\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="achaalah\nhel ru\ntab-haah\ntab-haah\nachaalah\nachaalah\n",
                        expected_output="Зочилсон: 1 удаа (энэ табд 1), хэл: mn\nЗочилсон: 2 удаа (энэ табд 1), хэл: ru\nЗочилсон: 3 удаа (энэ табд 2), хэл: ru\n",
                    ),
                    TestCaseSpec(
                        stdin="achaalah\nbuh-ustgah\nachaalah\nhel kk\nachaalah\n",
                        expected_output="Зочилсон: 1 удаа (энэ табд 1), хэл: mn\nЗочилсон: 1 удаа (энэ табд 2), хэл: mn\nЗочилсон: 2 удаа (энэ табд 3), хэл: kk\n",
                    ),
                    TestCaseSpec(
                        stdin="hel mn\nhel en\nachaalah\ntab-haah\nhel-ustgah\nachaalah\nachaalah\n",
                        expected_output="Зочилсон: 1 удаа (энэ табд 1), хэл: en\nЗочилсон: 2 удаа (энэ табд 1), хэл: mn\nЗочилсон: 3 удаа (энэ табд 2), хэл: mn\n",
                    ),
                ),
                solution="""\
// Worker дотор жинхэнэ сан байхгүй тул ижил методтой загвар бичье.
function sanUusgeh() {
  return {
    ugugdul: {}, // түлхүүр → мөр

    setItem(tulhuur, utga) {
      this.ugugdul[tulhuur] = String(utga); // үргэлж мөр болгоно
    },
    getItem(tulhuur) {
      return tulhuur in this.ugugdul ? this.ugugdul[tulhuur] : null;
    },
    removeItem(tulhuur) {
      delete this.ugugdul[tulhuur];
    },
    clear() {
      this.ugugdul = {};
    },
  };
}

const localStorage = sanUusgeh(); // хөтөч хаагдсан ч үлдэнэ
const sessionStorage = sanUusgeh(); // таб хаагдах хүртэл

function huudasAchaalah() {
  // getItem мөр эсвэл null буцаана: Number(null) → 0, Number("2") → 2
  const niit = Number(localStorage.getItem("uzsen")) + 1;
  localStorage.setItem("uzsen", niit);

  const tab = Number(sessionStorage.getItem("tabUzsen")) + 1;
  sessionStorage.setItem("tabUzsen", tab);

  // Хадгалаагүй бол null → анхдагч "mn"
  const hel = localStorage.getItem("hel") || "mn";
  console.log(`Зочилсон: ${niit} удаа (энэ табд ${tab}), хэл: ${hel}`);
}

function helSongoh(kod) {
  localStorage.setItem("hel", kod);
}

function helUstgah() {
  localStorage.removeItem("hel");
}

// ---- Хэрэглэгчийн үйлдлийг дуурайна — энэ хэсгийг бүү өөрчил ----
let mur = prompt();
while (mur !== null) {
  const hesguud = mur.split(" ");
  const komand = hesguud[0];

  if (komand === "achaalah") {
    huudasAchaalah();
  } else if (komand === "hel") {
    helSongoh(hesguud[1]);
  } else if (komand === "hel-ustgah") {
    helUstgah();
  } else if (komand === "tab-haah") {
    sessionStorage.clear(); // шинэ таб — sessionStorage хоосон
  } else if (komand === "buh-ustgah") {
    localStorage.clear(); // хэрэглэгч хөтчийн өгөгдлөө цэвэрлэв
  }
  mur = prompt();
}
""",
                tips="""\
- `getItem` **мөр** эсвэл `null` буцаана. `Number(null)` → `0`, `Number("2")` →
  `2` — тэгээд нэм. `Number()`-гүй бол `"1" + 1` → `"11"`.
- `setItem`-д тоо өгсөн ч мөр болж хадгалагдана — дараагийн удаа дахин
  `Number()`.
- Анхдагч хэл: `localStorage.getItem("hel") || "mn"`.
- Нийт тоо `localStorage`-д, табын тоо `sessionStorage`-д — `tab-haah`,
  `buh-ustgah`-ийг эхлэл код хийнэ, чиний функц санд байгааг л уншина.
""",
            ),
        ),
        LessonSpec(
            title="JSON-той хамт ашиглах",
            slug="json-tei-hamt-ashiglah",
            description="Объект, массивыг хадгалж буцааж унших.",
            duration=450,
            content="""\
`localStorage` зөвхөн мөр хадгалдаг тул объектыг эхлээд мөр болгоно.

### JSON гэж юу вэ

JavaScript Object Notation — өгөгдлийг текст болгон бичих формат. Бараг
бүх програмчлалын хэл үүнийг уншиж чадна.

```json
{ "ner": "Бат", "nas": 20, "hicheeluud": ["JS", "Python"] }
```

### Хоёр функц

```javascript
const mur = JSON.stringify(obyekt);  // объект → мөр
const obyekt = JSON.parse(mur);      // мөр → объект
```

### Хадгалж, буцааж унших

```javascript
const ajluud = [{ id: 1, garchig: "Хичээл үзэх" }];

localStorage.setItem("ajluud", JSON.stringify(ajluud));

const butsaasan = JSON.parse(localStorage.getItem("ajluud"));
console.log(butsaasan[0].garchig);
```

### `JSON.parse` алдаа шиднэ

Эвдэрсэн текст ирвэл `JSON.parse` алдаа **шидэж**, програм тэр дороо
зогсоно. Үүнээс хамгаалахын тулд `try { ... } catch { ... }` бичнэ:
`try` доторх код алдаа шидвэл програм зогсохгүй, `catch` доторх код
ажиллана. Алдаа гараагүй бол `catch`-ийг алгасна. (Алдаа боловсруулахыг
Модул 17-д дэлгэрэнгүй үзнэ.)

```javascript
function unshih(tulhuur, anhdagch) {
  try {
    const tur = localStorage.getItem(tulhuur);
    return tur === null ? anhdagch : JSON.parse(tur);
  } catch {
    return anhdagch; // эвдэрсэн байвал анхдагч утгыг буцаана
  }
}
```

Өгөгдөл эвдэрсэн байх нь ховор ч тохиолддог — хуучин хувилбарын формат
үлдсэн, хэрэглэгч гараар өөрчилсөн гэх мэт.

### JSON юуг хадгалж чадахгүй вэ

| Утга | Болох уу |
|---|---|
| Мөр, тоо, boolean, `null` | Тийм |
| Массив, энгийн объект | Тийм |
| `undefined` | Үгүй — талбар нь алга болно |
| Функц | Үгүй — алга болно |
| `Date` | Мөр болж хувирна, буцахдаа `Date` болохгүй |

Огноог буцааж уншихдаа `new Date(mur)` гэж гараар сэргээх хэрэгтэй.
""",
            initial_code="""\
// Өмнөх хичээлийн localStorage загвар.
const localStorage = {
  ugugdul: {},
  setItem(tulhuur, utga) {
    this.ugugdul[tulhuur] = String(utga);
  },
  getItem(tulhuur) {
    return tulhuur in this.ugugdul ? this.ugugdul[tulhuur] : null;
  },
};

// ---- Чиний код ----
function unshih() {
  // TODO: "ajluud"-ийг уншаад null бол [], үгүй бол JSON.parse хийж буцаана.
  return [];
}

function hadgalah(ajluud) {
  // TODO: JSON.stringify хийгээд "ajluud" түлхүүрээр хадгална.
}

function nemeh(garchig) {
  // TODO: unshih → { id, garchig, duussan: false } нэмэх → hadgalah.
}

function duusgah(id) {
  // TODO: unshih → тэр ажлыг duussan: true болгох → hadgalah.
}

function harah() {
  // TODO: "[x] 1. ..." / "[ ] 2. ..." мөрүүд, эцэст нь "Нийт: 2".
}

// ---- Хөтөч ба хэрэглэгчийг дуурайна — энэ хэсгийг бүү өөрчил ----
const ehlel = prompt(); // санд урьдаас байгаа JSON эсвэл "-"
if (ehlel !== "-") {
  localStorage.setItem("ajluud", ehlel);
}

let mur = prompt();
while (mur !== null) {
  const hesguud = mur.split(" ");
  const komand = hesguud[0];
  const utga = hesguud.slice(1).join(" ");

  if (komand === "nemeh") {
    nemeh(utga);
  } else if (komand === "duusgah") {
    duusgah(Number(utga));
  } else if (komand === "harah") {
    harah();
  } else if (komand === "hadgalsan") {
    console.log(localStorage.getItem("ajluud"));
  } else if (komand === "busad-tab") {
    localStorage.setItem("ajluud", utga); // өөр таб санг дарж бичлээ
  }
  mur = prompt();
}
""",
            exercise=ExerciseSpec(
                statement="""\
Хийх ажлын жагсаалтыг `localStorage`-д JSON болгон хадгал. Санд `"ajluud"`
түлхүүрээр `[{"id":1,"garchig":"...","duussan":false}]` хэлбэрийн мөр
хадгалагдана (`localStorage`-ийн загвар эхлэл кодод). Функц бүр жагсаалтыг
**сангаас уншиж** (`JSON.parse`), өөрчилсөн бол **буцааж хадгална**
(`JSON.stringify`). Өөр таб санг өөрчилж болох тул жагсаалтыг хувьсагчид бүү
барь.

- `unshih()` — санд байхгүй (`null`) бол `[]`, байвал задалсан массив.
- `nemeh(garchig)` — `{ id, garchig, duussan: false }` нэмнэ. `id` нь
  жагсаалтын хамгийн их `id` + 1 (хоосон бол `1`).
- `duusgah(id)` — тэр ажлыг `duussan: true` болгоно (байхгүй бол юу ч хийхгүй).
- `harah()` — ажил бүрийг `[x] 1. <гарчиг>` / `[ ] 2. <гарчиг>`, эцэст нь
  `Нийт: <тоо>` гэж хэвлэнэ.

**Оролт:** эхний мөр — санд урьдаас байгаа JSON мөр, эсвэл `-` (хоосон сан).
Дараагийн мөр бүр нэг команд: `nemeh <гарчиг>`, `duusgah <id>`, `harah`,
`hadgalsan` (сан дахь мөрийг хэвлэх), `busad-tab <JSON>` (өөр таб санг дарж
бичих). Сан дахь JSON үргэлж зөв — эвдэрсэн JSON-ийг `try`/`catch`-аар барихыг
Модул 17-д үзнэ.

**Гаралт:** `harah` ба `hadgalsan`-ий хэвлэсэн мөрүүд. `hadgalsan` нь сан дахь
мөрийг хэвээр нь (хоосон бол `null`) хэвлэнэ:

```text
[x] 1. <гарчиг>
[ ] 2. <гарчиг>
Нийт: <тоо>
```
""",
                tests=(
                    TestCaseSpec(
                        stdin="-\nnemeh Хичээл үзэх\nnemeh Дасгал хийх\nduusgah 1\nhadgalsan\nharah\n",
                        expected_output='[{"id":1,"garchig":"Хичээл үзэх","duussan":true},{"id":2,"garchig":"Дасгал хийх","duussan":false}]\n[x] 1. Хичээл үзэх\n[ ] 2. Дасгал хийх\nНийт: 2\n',
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin='[{"id":4,"garchig":"Ном унших","duussan":false}]\nharah\nnemeh Гүйх\nhadgalsan\n',
                        expected_output='[ ] 4. Ном унших\nНийт: 1\n[{"id":4,"garchig":"Ном унших","duussan":false},{"id":5,"garchig":"Гүйх","duussan":false}]\n',
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="-\nhadgalsan\nharah\n",
                        expected_output="null\nНийт: 0\n",
                    ),
                    TestCaseSpec(
                        stdin='-\nnemeh A\nbusad-tab [{"id":7,"garchig":"Өөр табаас","duussan":true}]\nnemeh B\nharah\n',
                        expected_output="[x] 7. Өөр табаас\n[ ] 8. B\nНийт: 2\n",
                    ),
                    TestCaseSpec(
                        stdin='[{"id":3,"garchig":"Гурав","duussan":true},{"id":1,"garchig":"Нэг","duussan":false}]\nduusgah 1\nduusgah 9\nnemeh Дөрөв\nhadgalsan\n',
                        expected_output='[{"id":3,"garchig":"Гурав","duussan":true},{"id":1,"garchig":"Нэг","duussan":true},{"id":4,"garchig":"Дөрөв","duussan":false}]\n',
                    ),
                ),
                solution="""\
// Өмнөх хичээлийн localStorage загвар.
const localStorage = {
  ugugdul: {},
  setItem(tulhuur, utga) {
    this.ugugdul[tulhuur] = String(utga);
  },
  getItem(tulhuur) {
    return tulhuur in this.ugugdul ? this.ugugdul[tulhuur] : null;
  },
};

function unshih() {
  const tur = localStorage.getItem("ajluud");
  return tur === null ? [] : JSON.parse(tur);
}

function hadgalah(ajluud) {
  localStorage.setItem("ajluud", JSON.stringify(ajluud));
}

function nemeh(garchig) {
  const ajluud = unshih();
  // Хамгийн их id + 1 — дараалал нь эмх замбараагүй байж болно
  let id = 1;
  for (const ajil of ajluud) {
    if (ajil.id >= id) {
      id = ajil.id + 1;
    }
  }
  ajluud.push({ id: id, garchig: garchig, duussan: false });
  hadgalah(ajluud);
}

function duusgah(id) {
  const ajluud = unshih();
  const ajil = ajluud.find((a) => a.id === id);
  if (ajil) {
    ajil.duussan = true;
    hadgalah(ajluud);
  }
}

function harah() {
  const ajluud = unshih();
  for (const ajil of ajluud) {
    console.log(`${ajil.duussan ? "[x]" : "[ ]"} ${ajil.id}. ${ajil.garchig}`);
  }
  console.log(`Нийт: ${ajluud.length}`);
}

// ---- Хөтөч ба хэрэглэгчийг дуурайна — энэ хэсгийг бүү өөрчил ----
const ehlel = prompt(); // санд урьдаас байгаа JSON эсвэл "-"
if (ehlel !== "-") {
  localStorage.setItem("ajluud", ehlel);
}

let mur = prompt();
while (mur !== null) {
  const hesguud = mur.split(" ");
  const komand = hesguud[0];
  const utga = hesguud.slice(1).join(" ");

  if (komand === "nemeh") {
    nemeh(utga);
  } else if (komand === "duusgah") {
    duusgah(Number(utga));
  } else if (komand === "harah") {
    harah();
  } else if (komand === "hadgalsan") {
    console.log(localStorage.getItem("ajluud"));
  } else if (komand === "busad-tab") {
    localStorage.setItem("ajluud", utga); // өөр таб санг дарж бичлээ
  }
  mur = prompt();
}
""",
                tips="""\
- `unshih`: `const tur = localStorage.getItem("ajluud");` → `null` бол `[]`,
  үгүй бол `JSON.parse(tur)`.
- `JSON.stringify` талбаруудыг объектод бичсэн дарааллаар нь гаргана —
  `{ id, garchig, duussan }` дарааллыг барь, эс бөгөөс `hadgalsan` таарахгүй.
- Хамгийн их `id`-г давталтаар, эсвэл
  `Math.max(0, ...ajluud.map((a) => a.id)) + 1`-ээр ол.
- Сангаас уншсан массивыг өөрчилсний дараа `hadgalah` дуудахгүй бол өөрчлөлт
  алга болно — санд хуучин мөр хэвээр үлдэнэ.
- `busad-tab`-ийн дараа `nemeh` шинэ өгөгдөл дээр ажиллах ёстой — функц бүрийн
  эхэнд `unshih()`.
""",
            ),
        ),
    ],
)

BROWSER_MODULES = [DOM, EVENTS, FORMS, STORAGE]
