"""Модул 5-8 — Функц, массив, объект, мөр.

Өгөгдлийг бүлэглэж, кодыг дахин ашиглах боломжтой хэсгүүдэд хуваах.
"""

from app.content.types import ExerciseSpec, LessonSpec, ModuleSpec, TestCaseSpec

FUNCTIONS = ModuleSpec(
    title="Модул 5 — Функц (Functions)",
    description="Кодоо дахин ашиглах боломжтой хэсгүүдэд хуваах.",
    lessons=[
        LessonSpec(
            title="Функц (Function)",
            slug="funkts",
            description="Функц зарлах, дуудах.",
            duration=400,
            content="""Функц нь давтагдах кодыг нэг нэрийн дор багцлана.

```javascript
function mendchilgee() {
  console.log("Сайн байна уу!");
}

mendchilgee(); // функцийг дуудна
```

Сум функц (arrow function) нь ижил зүйлийн богино бичлэг (энэ модулийн
сүүлийн хичээлд дэлгэрэнгүй үзнэ):

```javascript
const mendchilgee = () => {
  console.log("Сайн байна уу!");
};
```

`return` ашиглан утга буцаана:

```javascript
function nemeh(a, b) {
  return a + b;
}

console.log(nemeh(2, 3)); // 5
```

### `return`-ийн дараа код ажиллахгүй

`return` нь функцийг тэр дороо дуусгана:

```javascript
function shalgah(nas) {
  if (nas < 18) {
    return "хүүхэд";
  }
  return "насанд хүрсэн";
}
```

Энэ шинжийг ашиглан `else` бичихээс зайлсхийж болно — кодын догол мөр
цөөрч, уншихад хялбар болно.

### `return` байхгүй бол

Функц `undefined` буцаана:

```javascript
function hevleh() {
  console.log("сайн уу");
}

const ur = hevleh();
console.log(ur); // undefined
```

Тиймээс "хэвлэдэг" функц ба "буцаадаг" функцийг сайн ялгах хэрэгтэй.
Ихэнх тохиолдолд **буцаадаг** функц илүү ашигтай — үр дүнг нь цааш
ашиглаж болно.
""",
            initial_code="""\
// Насны ангиллыг БУЦААДАГ функц — хэвлэхгүй, return хийнэ
function angilal(nas) {
  // TODO: 13-аас бага бол "хүүхэд" буцаа
  // TODO: 18-аас бага бол "өсвөр" буцаа
  // TODO: 60-аас бага бол "насанд хүрсэн" буцаа
  // TODO: бусад бүх тохиолдолд "ахмад" буцаа
}

const n = Number(prompt());
for (let i = 0; i < n; i++) {
  const nas = Number(prompt());
  // Функц юу ч буцаахгүй бол энд undefined хэвлэгдэнэ
  console.log(`${nas} нас: ${angilal(nas)}`);
}
""",
            exercise=ExerciseSpec(
                statement="""\
Насыг ангилдаг **функц** бичээд, олон хүний насыг түүгээр ангил.

`angilal(nas)` функц насны ангиллыг **буцаана** (`return`) — өөрөө
хэвлэхгүй. Хэвлэх ажлыг функцийн гадна, давталт дотор хий.

| Нас | Ангилал |
|---|---|
| 0–12 | `хүүхэд` |
| 13–17 | `өсвөр` |
| 18–59 | `насанд хүрсэн` |
| 60 ба түүнээс дээш | `ахмад` |

**Оролт:** эхний мөрөнд хүний тоо `n` (1 ба түүнээс их), дараагийн `n`
мөр бүрт нэг хүний нас (0 ба түүнээс их бүхэл тоо).

**Гаралт:** хүн бүрт нэг мөр:

```text
<нас> нас: <ангилал>
```
""",
                tests=(
                    TestCaseSpec(
                        stdin="4\n5\n15\n30\n70\n",
                        expected_output="5 нас: хүүхэд\n15 нас: өсвөр\n30 нас: насанд хүрсэн\n70 нас: ахмад\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="4\n12\n13\n17\n18\n",
                        expected_output="12 нас: хүүхэд\n13 нас: өсвөр\n17 нас: өсвөр\n18 нас: насанд хүрсэн\n",
                    ),
                    TestCaseSpec(
                        stdin="3\n59\n60\n0\n",
                        expected_output="59 нас: насанд хүрсэн\n60 нас: ахмад\n0 нас: хүүхэд\n",
                    ),
                    TestCaseSpec(
                        stdin="1\n100\n",
                        expected_output="100 нас: ахмад\n",
                    ),
                    TestCaseSpec(
                        stdin="2\n1\n45\n",
                        expected_output="1 нас: хүүхэд\n45 нас: насанд хүрсэн\n",
                    ),
                ),
                solution="""\
function angilal(nas) {
  // return функцийг тэр дор нь дуусгадаг тул else хэрэггүй
  if (nas < 13) {
    return "хүүхэд";
  }
  if (nas < 18) {
    return "өсвөр";
  }
  if (nas < 60) {
    return "насанд хүрсэн";
  }
  return "ахмад";
}

const n = Number(prompt());
for (let i = 0; i < n; i++) {
  const nas = Number(prompt());
  console.log(`${nas} нас: ${angilal(nas)}`);
}
""",
                tips="""\
- Функц дотор `console.log` биш `return` бич — `angilal(15)` нь `"өсвөр"`
  гэсэн **утга** өгөх ёстой.
- `return` функцийг тэр дороо дуусгана. Шалгалтуудыг жижиг наснаас эхлэн
  дараалуулж бичвэл `else` хэрэггүй: эхлээд `nas < 13`, дараа нь `nas < 18` …
- Сүүлийн «бусад» тохиолдлын `return`-ийг мартвал функц `undefined` буцааж,
  гаралтад `70 нас: undefined` гарна.
- Хил дээрх насыг шалга: 12 → хүүхэд, 13 → өсвөр, 18 → насанд хүрсэн,
  60 → ахмад.
""",
            ),
        ),
        LessonSpec(
            title="Параметр (Parameters)",
            slug="parametr",
            description="Функцэд утга дамжуулах.",
            duration=380,
            content="""Параметр нь функц рүү утга дамжуулах зам.

```javascript
function mendchileh(ner) {
  return "Сайн байна уу, " + ner + "!";
}

console.log(mendchileh("Бат"));
```

### Анхдагч утга (Default parameter)

```javascript
function mendchileh(ner = "зочин") {
  return "Сайн байна уу, " + ner + "!";
}

console.log(mendchileh()); // "Сайн байна уу, зочин!"
```

### Template literal

Мөр нийлүүлэхэд `+` биш backtick ашиглавал уншихад хялбар:

```javascript
const ner = "Бат";
console.log(`Сайн байна уу, ${ner}!`);
```

### Параметр ба аргумент

Хоёр нэр төстэй ч ялгаатай:

- **Параметр** — функцийг зарлахад бичсэн нэр (`ner`)
- **Аргумент** — функцийг дуудахад өгсөн бодит утга (`"Бат"`)

```javascript
function mendchileh(ner) {   // ner — параметр
  return `Сайн уу, ${ner}`;
}

mendchileh("Бат");           // "Бат" — аргумент
```

### Дутуу аргумент

JavaScript дутуу аргументад гомдоллохгүй — зүгээр л `undefined` болгоно:

```javascript
function nemeh(a, b) {
  return a + b;
}

console.log(nemeh(5)); // NaN — b нь undefined
```

Тиймээс анхдагч утга өгөх нь алдаанаас хамгаална.

> Анхдагч утга нь аргументыг **өгөөгүй** (`undefined`) үед л ажиллана.
> `null` өгвөл параметр `null` болно — анхдагч утга ажиллахгүй.
""",
            initial_code="""\
// Нэг барааны баримтын мөрийг БУЦААДАГ функц
// TODO: too параметрт анхдагч утга 1 өг
function barimt(ner, une, too) {
  // TODO: нийт үнийг (une × too) тооцоод мөрөнд оруул
  return `${ner}: ${too} ш, нийт ? төгрөг`;
}

const ner = prompt();
const une = Number(prompt());
const tooMur = prompt(); // тоо ширхэгийг бичээгүй бол null

// TODO: tooMur нь null бол barimt-ийг ХОЁР аргументтай (тоо ширхэггүй),
//       эс бөгөөс Number(tooMur)-тэй ГУРВАН аргументтай дууд
console.log(barimt(ner, une, Number(tooMur)));
""",
            exercise=ExerciseSpec(
                statement="""\
Дэлгүүрийн баримтын нэг мөрийг бүтээдэг `barimt(ner, une, too)` функц бич.
Мөрөө template literal-аар бүтээж **буцаа**.

Тоо ширхэгийг оруулаагүй бол **1** гэж үзнэ — үүнийг `too` параметрийн
**анхдагч утгаар** шийд.

**Оролт:**

- 1-р мөр — барааны нэр;
- 2-р мөр — нэг ширхэгийн үнэ (бүхэл тоо);
- 3-р мөр — тоо ширхэг (0 ба түүнээс их бүхэл тоо). Энэ мөр **байхгүй** байж
  болно — тэгвэл `prompt()` нь `null` буцаана.

**Гаралт:** нэг мөр:

```text
<нэр>: <тоо ширхэг> ш, нийт <үнэ × тоо ширхэг> төгрөг
```
""",
                tests=(
                    TestCaseSpec(
                        stdin="Талх\n2500\n3\n",
                        expected_output="Талх: 3 ш, нийт 7500 төгрөг\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="Сүү\n3200\n",
                        expected_output="Сүү: 1 ш, нийт 3200 төгрөг\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="Өндөг\n450\n12\n",
                        expected_output="Өндөг: 12 ш, нийт 5400 төгрөг\n",
                    ),
                    TestCaseSpec(
                        stdin="Ус\n1000\n",
                        expected_output="Ус: 1 ш, нийт 1000 төгрөг\n",
                    ),
                    TestCaseSpec(
                        stdin="Алим\n1500\n0\n",
                        expected_output="Алим: 0 ш, нийт 0 төгрөг\n",
                    ),
                ),
                solution="""\
function barimt(ner, une, too = 1) {
  return `${ner}: ${too} ш, нийт ${une * too} төгрөг`;
}

const ner = prompt();
const une = Number(prompt());
const tooMur = prompt();

if (tooMur === null) {
  // Гурав дахь аргументгүй — too нь анхдагч утга 1 болно
  console.log(barimt(ner, une));
} else {
  console.log(barimt(ner, une, Number(tooMur)));
}
""",
                tips="""\
- Анхдагч утгыг параметрийн жагсаалтад `=`-ээр бичнэ — хичээлийн
  `ner = "зочин"` жишээ шиг.
- Анхдагч утга нь аргументыг **огт өгөөгүй** үед л ажиллана. `null`
  дамжуулбал `too` нь `null` хэвээр — тиймээс `prompt()` `null` буцаасан бол
  функцийг хоёр аргументтай дууд.
- `prompt()` текст буцаадаг: үнэ, тоо ширхэгийг `Number()`-оор тоо болго.
- `0` ширхэг бол 0 хэвээрээ: «0 ш, нийт 0 төгрөг». `Number(tooMur) || 1` гэх
  мэт бичвэл 0 нь falsy тул 1 болж алдана.
""",
            ),
        ),
        LessonSpec(
            title="Функц илэрхийлэл ба сум функц",
            slug="funkts-ilerhiilel-ba-sum-funkts",
            description="Функцийг утга мэт дамжуулах. Arrow function.",
            duration=420,
            content="""\
JavaScript дээр функц бол **утга**. Түүнийг хувьсагчид хийж, өөр функц рүү
дамжуулж болно.

### Гурван бичлэг

```javascript
// 1. Зарлалт (declaration)
function nemeh(a, b) {
  return a + b;
}

// 2. Илэрхийлэл (expression)
const nemeh2 = function (a, b) {
  return a + b;
};

// 3. Сум функц (arrow)
const nemeh3 = (a, b) => {
  return a + b;
};
```

### Сум функцийн богино хэлбэр

Бие нь ганц `return` бол хаалт болон `return`-ийг хасаж болно:

```javascript
const nemeh = (a, b) => a + b;
const guravDahin = (x) => x * 3;
```

Объект (Модул 7-д үзнэ) буцаахдаа дугуй хаалтанд хийнэ, эс бөгөөс хөтөч
`{`-ийг функцийн биеийн эхлэл гэж ойлгоно:

```javascript
const buteeh = (ner) => ({ ner: ner });
```

### Hoisting-ийн ялгаа

`function` зарлалтыг **зарлахаас өмнө** дуудаж болно. Илэрхийлэл болон
сум функцийг **болохгүй**:

```javascript
console.log(nemeh(1, 2)); // 3 — ажиллана

function nemeh(a, b) {
  return a + b;
}
```

```javascript
console.log(hasah(1, 2)); // ReferenceError

const hasah = (a, b) => a - b;
```

### Функцийг аргумент болгох

Энэ бол JavaScript-ийн хамгийн хүчтэй санаануудын нэг:

```javascript
function hoyorDahinHiih(ajil) {
  ajil();
  ajil();
}

hoyorDahinHiih(() => console.log("сайн уу"));
```

Модул 6-д үзэх массивын `map`, `filter` зэрэг метод яг ингэж ажилладаг.
""",
            initial_code="""\
// Дарааллын i-р гишүүнийг буцаадаг сум функцууд (i = 1, 2, 3, ...)
const tegsh = (i) => 2 * i;
// TODO: sondgoi — i-р сондгой тоо (1, 3, 5, ...)
// TODO: kvadrat — i-ийн квадрат (1, 4, 9, ...)

// Эхний n гишүүнийг нэг мөрөнд хэвлэнэ. gishuun нь ФУНКЦ.
function daraalal(n, gishuun) {
  let mur = "";
  for (let i = 1; i <= n; i++) {
    // TODO: gishuun(i)-ийн утгыг mur-т нэмээд ард нь зай тавь
  }
  console.log(mur);
}

const turul = prompt();
const n = Number(prompt());

// TODO: turul-аас хамаарч тохирох функцийг daraalal руу дамжуул
daraalal(n, tegsh);
""",
            exercise=ExerciseSpec(
                statement="""\
Функцийг **утга** болгон дамжуулж тооны дараалал хэвлэ.

`daraalal(n, gishuun)` функц дарааллын эхний `n` гишүүнийг нэг мөрөнд,
зайгаар тусгаарлан хэвлэнэ. `gishuun` нь **функц**: `i` дугаарыг (1, 2, 3, …)
аваад дарааллын `i`-р гишүүнийг буцаана. Гурван дарааллыг гурван **сум
функцээр** бич:

| Төрөл | Гишүүд |
|---|---|
| `тэгш` | 2 4 6 8 … |
| `сондгой` | 1 3 5 7 … |
| `квадрат` | 1 4 9 16 … |

**Оролт:** 1-р мөрөнд дарааллын төрөл (`тэгш`, `сондгой` эсвэл `квадрат`),
2-р мөрөнд `n` (1 ба түүнээс их бүхэл тоо).

**Гаралт:** нэг мөр — эхний `n` гишүүн, хооронд нь нэг зай:

```text
<1-р гишүүн> <2-р гишүүн> … <n-р гишүүн>
```
""",
                tests=(
                    TestCaseSpec(stdin="тэгш\n5\n", expected_output="2 4 6 8 10\n", sample=True),
                    TestCaseSpec(stdin="квадрат\n4\n", expected_output="1 4 9 16\n", sample=True),
                    TestCaseSpec(stdin="сондгой\n6\n", expected_output="1 3 5 7 9 11\n"),
                    TestCaseSpec(stdin="квадрат\n1\n", expected_output="1\n"),
                    TestCaseSpec(stdin="тэгш\n1\n", expected_output="2\n"),
                    TestCaseSpec(
                        stdin="сондгой\n10\n", expected_output="1 3 5 7 9 11 13 15 17 19\n"
                    ),
                ),
                solution="""\
const tegsh = (i) => 2 * i;
const sondgoi = (i) => 2 * i - 1;
const kvadrat = (i) => i * i;

function daraalal(n, gishuun) {
  let mur = "";
  for (let i = 1; i <= n; i++) {
    mur += gishuun(i) + " ";
  }
  console.log(mur);
}

const turul = prompt();
const n = Number(prompt());

// Функцийг хаалтгүй нэрээр нь дамжуулна — daraalal өөрөө дуудна
if (turul === "тэгш") {
  daraalal(n, tegsh);
} else if (turul === "сондгой") {
  daraalal(n, sondgoi);
} else {
  daraalal(n, kvadrat);
}
""",
                tips="""\
- Бие нь ганц илэрхийлэл бол сум функцийг богино бичнэ: `(i) => …` —
  `return`, `{}` хэрэггүй.
- `i`-р сондгой тоо нь `i`-р тэгш тооноос 1-ээр бага.
- Функцийг дамжуулахдаа **хаалтгүй** нэрийг нь өг: `daraalal(n, kvadrat)`.
  `kvadrat()` гэж бичвэл функцийг тэр дор нь дуудаж, үр дүнг нь дамжуулна.
- `daraalal` дотор `gishuun(i)`-ийг дуудаж, мөр рүү `+=`-ээр нэм. Мөрийн
  төгсгөлийн илүү зай тоологдохгүй, харин эхэнд нь зай гарвал тест унана.
""",
            ),
        ),
    ],
)

ARRAYS = ModuleSpec(
    title="Модул 6 — Массив (Arrays)",
    description="Олон утгыг нэг жагсаалтад цуглуулах.",
    lessons=[
        LessonSpec(
            title="Массив үүсгэх ба хандах",
            slug="massiv-uusgeh",
            description="Жагсаалт үүсгэх, элементэд индексээр хандах.",
            duration=360,
            content="""\
Массив нь **эрэмбэлэгдсэн** утгуудын жагсаалт.

```javascript
const jimsnuud = ["алим", "гадил", "усан үзэм"];
const toonuud = [10, 20, 30];
const holimog = [1, "хоёр", true, null];
```

### Индексээр хандах

Индекс **0-ээс** эхэлнэ:

```javascript
console.log(jimsnuud[0]); // "алим"
console.log(jimsnuud[2]); // "усан үзэм"
console.log(jimsnuud[9]); // undefined — алдаа заахгүй!
```

### Урт

```javascript
console.log(jimsnuud.length); // 3
```

Сүүлийн элементийг авах хоёр арга:

```javascript
jimsnuud[jimsnuud.length - 1];
jimsnuud.at(-1); // илүү шинэ, илүү ойлгомжтой
```

### `const` массив өөрчлөгдөнө

Энэ нь эхэндээ эргэлзээ төрүүлдэг:

```javascript
const jagsaalt = [1, 2, 3];
jagsaalt[0] = 99;   // зөвшөөрнө — доторх утгыг сольж байна
jagsaalt = [5];     // АЛДАА — өөр массив оноох гэж байна
```

`const` нь **хувьсагч өөр массив руу заахыг** хориглоно. Массивын
**доторх** утгыг өөрчлөхийг хориглохгүй.

### Хоёр хэмжээст массив

Массив дотор массив байж болно:

```javascript
const husnegt = [
  [1, 2],
  [3, 4],
];

console.log(husnegt[1][0]); // 3
```
""",
            initial_code="""\
// TODO: 7 өдрийн нэрийг Даваагаас Ням хүртэл дарааллаар нь массивт бич
const udruud = ["Даваа", "Мягмар"];

const n = Number(prompt());
for (let i = 0; i < n; i++) {
  const k = Number(prompt());
  // TODO: k-р өдөр массивын аль индекст байгааг бод (индекс 0-ээс эхэлнэ)
  // TODO: k нь 1-ээс udruud.length хүртэлх тоо биш бол "байхгүй" гэж хэвлэ
  console.log(`${k}: ${udruud[k]}`);
}
""",
            exercise=ExerciseSpec(
                statement="""\
Долоо хоногийн өдрүүдийг **массивт** хадгалаад, дугаараар нь нэрийг ол.

Өдрүүд Даваагаас эхэлнэ: 1 — Даваа, 2 — Мягмар, 3 — Лхагва, 4 — Пүрэв,
5 — Баасан, 6 — Бямба, 7 — Ням.

Массивын индекс **0-ээс** эхэлдэг ч өдрийн дугаар 1-ээс эхэлнэ — үүнийг
анхаар. 1–7-оос гадуурх дугаарт `байхгүй` гэж хэвлэ.

**Оролт:** эхний мөрөнд дугаарын тоо `n`, дараагийн `n` мөр бүрт нэг бүхэл
тоо.

**Гаралт:** дугаар бүрт нэг мөр:

```text
<дугаар>: <өдрийн нэр эсвэл байхгүй>
```
""",
                tests=(
                    TestCaseSpec(
                        stdin="3\n1\n5\n7\n",
                        expected_output="1: Даваа\n5: Баасан\n7: Ням\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="2\n0\n8\n",
                        expected_output="0: байхгүй\n8: байхгүй\n",
                    ),
                    TestCaseSpec(
                        stdin="1\n3\n",
                        expected_output="3: Лхагва\n",
                    ),
                    TestCaseSpec(
                        stdin="4\n2\n4\n6\n-1\n",
                        expected_output="2: Мягмар\n4: Пүрэв\n6: Бямба\n-1: байхгүй\n",
                    ),
                    TestCaseSpec(
                        stdin="7\n7\n6\n5\n4\n3\n2\n1\n",
                        expected_output="7: Ням\n6: Бямба\n5: Баасан\n4: Пүрэв\n3: Лхагва\n2: Мягмар\n1: Даваа\n",
                    ),
                ),
                solution="""\
const udruud = ["Даваа", "Мягмар", "Лхагва", "Пүрэв", "Баасан", "Бямба", "Ням"];

const n = Number(prompt());
for (let i = 0; i < n; i++) {
  const k = Number(prompt());
  if (k >= 1 && k <= udruud.length) {
    // k-р өдөр нь k - 1 индекст: Даваа → udruud[0]
    console.log(`${k}: ${udruud[k - 1]}`);
  } else {
    console.log(`${k}: байхгүй`);
  }
}
""",
                tips="""\
- Массивын `[ ]` дотор утгуудыг таслалаар тусгаарлан бичнэ — бүгдийг нь
  бичсэний дараа `udruud.length` нь 7 болно.
- `k`-р өдөр нь `k - 1` индекст байна: Даваа нь `udruud[0]`.
- Байхгүй индекс алдаа заахгүй, `undefined` буцаадаг. Тиймээс хэвлэхээсээ
  өмнө дугаар 1-ээс `udruud.length` хүртэл байгаа эсэхийг шалга.
- `0`, `8`, сөрөг тоо — бүгд `байхгүй`.
""",
            ),
        ),
        LessonSpec(
            title="Элемент нэмэх, хасах",
            slug="massiv-element-nemeh-hasah",
            description="push, pop, shift, unshift, splice, slice.",
            duration=420,
            content="""\
### Төгсгөлд

```javascript
const jagsaalt = ["a", "b"];

jagsaalt.push("c");  // ["a", "b", "c"] — нэмнэ
jagsaalt.pop();      // "c"-г буцааж, массиваас хасна
```

### Эхэнд

```javascript
jagsaalt.unshift("z"); // эхэнд нэмнэ
jagsaalt.shift();      // эхнийхийг хасна
```

`shift` ба `unshift` нь бүх элементийг зөөдөг тул том массив дээр
`push`/`pop`-оос удаан.

### Дундаас — `splice`

```javascript
const uduud = ["Даваа", "Мягмар", "Лхагва"];

uduud.splice(1, 1);            // 1-р индексээс 1 ширхэг хасна
uduud.splice(1, 0, "Мягмар");  // хасалгүйгээр оруулна
```

### `slice` — хуулбар авна

`splice`-ээс ялгаатай нь эх массивыг **өөрчлөхгүй**:

```javascript
const toonuud = [1, 2, 3, 4, 5];

console.log(toonuud.slice(1, 3)); // [2, 3]
console.log(toonuud);             // [1, 2, 3, 4, 5] — хэвээрээ
```

| Метод | Эх массивыг өөрчлөх үү |
|---|---|
| `push`, `pop`, `shift`, `unshift`, `splice` | Тийм |
| `slice`, `concat`, `map`, `filter` | Үгүй |

### Элемент байгаа эсэх

```javascript
console.log(jimsnuud.includes("алим")); // true
console.log(jimsnuud.indexOf("гадил")); // 1, олдохгүй бол -1
```

### Нэгтгэх

```javascript
const a = [1, 2];
const b = [3, 4];

console.log(a.concat(b)); // [1, 2, 3, 4]
console.log(a);           // [1, 2] — хэвээрээ
```

Модул 7-д үзэх `...` (тараах) оператороор ч массив нэгтгэж болно.
""",
            initial_code="""\
const daraalal = [];

const n = Number(prompt());
for (let i = 0; i < n; i++) {
  const mur = prompt();

  if (mur === "дараах") {
    // TODO: дугаарлалт хоосон бол "Дугаарлалт хоосон" гэж хэвлэ,
    //       эс бөгөөс эхний хүнийг гаргаж (shift) "Үйлчлүүлэв: <нэр>" гэж хэвлэ
  } else {
    // TODO: нэр аль хэдийн байвал (includes) "Аль хэдийн байна: <нэр>, <байр>-р байр"
    //       гэж хэвлэ — байр = indexOf + 1
    // TODO: эс бөгөөс төгсгөлд нь нэмээд (push) "Нэмэгдлээ: <нэр>, <байр>-р байр"
  }
}

console.log(`Үлдсэн: ${daraalal.length} хүн`);
""",
            exercise=ExerciseSpec(
                statement="""\
Үйлчилгээний **дугаарлалтыг** массиваар удирд.

Мөр бүр нэг үйл явдал:

- хүний **нэр** — тэр хүн дугаарлалтын **төгсгөлд** зогсоно. Аль хэдийн
  дугаарлалтад байвал дахин нэмэхгүй.
- `дараах` гэсэн үг — дугаарлалтын **эхний** хүнд үйлчилж, дугаарлалтаас
  гаргана.

Байр гэдэг нь дугаарлалт дахь дугаар: эхний хүн 1-р байранд байна.

**Оролт:** эхний мөрөнд үйл явдлын тоо `n`, дараагийн `n` мөр бүрт нэр
эсвэл `дараах`.

**Гаралт:** үйл явдал бүрт дараах мөрүүдийн аль нэг нь:

```text
Нэмэгдлээ: <нэр>, <байр>-р байр
Аль хэдийн байна: <нэр>, <байр>-р байр
Үйлчлүүлэв: <нэр>
Дугаарлалт хоосон
```

`дараах` ирэхэд хүн байхгүй бол `Дугаарлалт хоосон`. Эцэст нь нэг мөр:

```text
Үлдсэн: <хүний тоо> хүн
```
""",
                tests=(
                    TestCaseSpec(
                        stdin="6\nБат\nСараа\nБат\nдараах\nДорж\nдараах\n",
                        expected_output=(
                            "Нэмэгдлээ: Бат, 1-р байр\n"
                            "Нэмэгдлээ: Сараа, 2-р байр\n"
                            "Аль хэдийн байна: Бат, 1-р байр\n"
                            "Үйлчлүүлэв: Бат\n"
                            "Нэмэгдлээ: Дорж, 2-р байр\n"
                            "Үйлчлүүлэв: Сараа\n"
                            "Үлдсэн: 1 хүн\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="3\nдараах\nБолд\nдараах\n",
                        expected_output=(
                            "Дугаарлалт хоосон\n"
                            "Нэмэгдлээ: Болд, 1-р байр\n"
                            "Үйлчлүүлэв: Болд\n"
                            "Үлдсэн: 0 хүн\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="5\nАнар\nдараах\nАнар\nТуяа\nАнар\n",
                        expected_output=(
                            "Нэмэгдлээ: Анар, 1-р байр\n"
                            "Үйлчлүүлэв: Анар\n"
                            "Нэмэгдлээ: Анар, 1-р байр\n"
                            "Нэмэгдлээ: Туяа, 2-р байр\n"
                            "Аль хэдийн байна: Анар, 1-р байр\n"
                            "Үлдсэн: 2 хүн\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="4\nОюун\nТэмүүлэн\nНомин\nТэмүүлэн\n",
                        expected_output=(
                            "Нэмэгдлээ: Оюун, 1-р байр\n"
                            "Нэмэгдлээ: Тэмүүлэн, 2-р байр\n"
                            "Нэмэгдлээ: Номин, 3-р байр\n"
                            "Аль хэдийн байна: Тэмүүлэн, 2-р байр\n"
                            "Үлдсэн: 3 хүн\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="2\nдараах\nдараах\n",
                        expected_output="Дугаарлалт хоосон\nДугаарлалт хоосон\nҮлдсэн: 0 хүн\n",
                    ),
                ),
                solution="""\
const daraalal = [];

const n = Number(prompt());
for (let i = 0; i < n; i++) {
  const mur = prompt();

  if (mur === "дараах") {
    if (daraalal.length === 0) {
      console.log("Дугаарлалт хоосон");
    } else {
      // shift нь гаргасан элементээ буцаана
      const ehnii = daraalal.shift();
      console.log(`Үйлчлүүлэв: ${ehnii}`);
    }
  } else if (daraalal.includes(mur)) {
    console.log(`Аль хэдийн байна: ${mur}, ${daraalal.indexOf(mur) + 1}-р байр`);
  } else {
    daraalal.push(mur);
    console.log(`Нэмэгдлээ: ${mur}, ${daraalal.length}-р байр`);
  }
}

console.log(`Үлдсэн: ${daraalal.length} хүн`);
""",
                tips="""\
- Төгсгөлд нэмэх нь `push`, эхнийхийг гаргах нь `shift`. `shift` гаргасан
  элементээ буцаадаг тул нэрийг нь шууд хувьсагчид авч болно.
- `push` хийсний дараа шинэ хүний байр нь массивын урт (`length`) болно.
- Нэр байгаа эсэхийг `includes`-ээр, байрыг `indexOf`-оор ол — индекс
  0-ээс эхэлдэг тул байр = индекс + 1.
- Хоосон массиваас `shift` хийвэл `undefined` буцна — эхлээд `length`-ийг
  шалга.
""",
            ),
        ),
        LessonSpec(
            title="Массивыг давтах",
            slug="massiv-davtah",
            description="for, for...of, forEach ашиглан элемент бүрийг дамжих.",
            duration=400,
            content="""\
### Гурван арга

```javascript
const toonuud = [10, 20, 30];

// 1. Сонгодог for — индекс хэрэгтэй үед
for (let i = 0; i < toonuud.length; i++) {
  console.log(i, toonuud[i]);
}

// 2. for...of — хамгийн уншигдахуйц
for (const too of toonuud) {
  console.log(too);
}

// 3. forEach — функц дамжуулна
toonuud.forEach((too, i) => {
  console.log(i, too);
});
```

### `forEach` хэрхэн ажилладаг вэ

`forEach` нь бидний өгсөн функцийг элемент бүр дээр нэг нэгээр дуудна.
Функцийн эхний параметр нь **утга**, хоёр дахь нь **индекс**. Индекс
хэрэггүй бол хоёр дахийг нь бичихгүй орхиж болно:

```javascript
toonuud.forEach((too) => {
  console.log(too * 2);
});
```

### Алийг нь сонгох вэ

| Хэрэгцээ | Сонголт |
|---|---|
| Зөвхөн утга хэрэгтэй | `for...of` |
| Индекс ч хэрэгтэй | `for` эсвэл `forEach` |
| Дунд нь зогсоох хэрэгтэй | `for` эсвэл `for...of` |

`forEach` дотор `break` ажиллахгүй — зөвхөн `return` нь тухайн дуудалтыг
дуусгана.

### Хоосон нүд

`forEach` нь хоосон нүдийг алгасдаг бол `for` алгасахгүй. Ердийн кодод
энэ ялгаа тааралдахгүй ч мэдэж байх нь зүйтэй.

### Давталтын доторх `await`

Асинхрон код бичихдээ `forEach` бүү ашигла — тэр хүлээхгүй. `for...of`
ашигла (Модул 18).
""",
            initial_code="""\
const n = Number(prompt());
const dunguud = [];
for (let i = 0; i < n; i++) {
  dunguud.push(Number(prompt()));
}

// 1. Нийлбэр ба дундаж
let niilber = 0;
// TODO: dunguud-ийг for...of-оор давтаж дүн бүрийг niilber-т нэм
const dundaj = niilber / dunguud.length;

// 2. Дунджаас их дүнгүүд — дугаар хэрэгтэй тул for эсвэл forEach (утга, индекс)
let too = 0;
// TODO: дунджаас ИХ дүн бүрийг "<дугаар>-р шалгалт: <дүн>" гэж хэвлээд too-г нэмэгдүүл

console.log(`Дунджаас дээш: ${too} шалгалт`);
""",
            exercise=ExerciseSpec(
                statement="""\
Шалгалтын дүнгүүдээс **дунджаас өндөр** дүнг нь ол.

Дунджийг мэдэхийн тулд эхлээд бүх дүнг үзэх хэрэгтэй, дараа нь дүн бүрийг
дундажтай дахин харьцуулна. Тиймээс дүнгүүдээ **массивт** цуглуулаад (эхлэл
кодод бэлэн), массиваа **хоёр удаа** давт: эхлээд нийлбэр, дараа нь
дунджаас их дүнгүүд.

**Оролт:** эхний мөрөнд шалгалтын тоо `n` (1 ба түүнээс их), дараагийн `n`
мөр бүрт нэг дүн (бүхэл тоо).

**Гаралт:** дунджаас **их** (тэнцүү биш) дүн бүрт, оролтын дарааллаар, нэг
мөр. `<дугаар>` нь шалгалтын 1-ээс эхэлсэн дугаар:

```text
<дугаар>-р шалгалт: <дүн>
```

Эцэст нь:

```text
Дунджаас дээш: <тоо> шалгалт
```
""",
                tests=(
                    TestCaseSpec(
                        stdin="5\n75\n82\n58\n91\n64\n",
                        expected_output="1-р шалгалт: 75\n2-р шалгалт: 82\n4-р шалгалт: 91\nДунджаас дээш: 3 шалгалт\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="4\n80\n80\n80\n80\n",
                        expected_output="Дунджаас дээш: 0 шалгалт\n",
                    ),
                    TestCaseSpec(
                        stdin="3\n10\n20\n31\n",
                        expected_output="3-р шалгалт: 31\nДунджаас дээш: 1 шалгалт\n",
                    ),
                    TestCaseSpec(
                        stdin="6\n50\n90\n70\n60\n100\n40\n",
                        expected_output="2-р шалгалт: 90\n3-р шалгалт: 70\n5-р шалгалт: 100\nДунджаас дээш: 3 шалгалт\n",
                    ),
                    TestCaseSpec(
                        stdin="2\n0\n1\n",
                        expected_output="2-р шалгалт: 1\nДунджаас дээш: 1 шалгалт\n",
                    ),
                ),
                solution="""\
const n = Number(prompt());
const dunguud = [];
for (let i = 0; i < n; i++) {
  dunguud.push(Number(prompt()));
}

let niilber = 0;
for (const dun of dunguud) {
  niilber += dun;
}
const dundaj = niilber / dunguud.length;

let too = 0;
// forEach-ийн хоёр дахь параметр нь индекс
dunguud.forEach((dun, i) => {
  if (dun > dundaj) {
    console.log(`${i + 1}-р шалгалт: ${dun}`);
    too++;
  }
});

console.log(`Дунджаас дээш: ${too} шалгалт`);
""",
                tips="""\
- Эхний давталтад индекс хэрэггүй, зөвхөн утга: `for (const dun of dunguud)`.
- Дундаж = нийлбэр / тоо. Бутархай гарч болно — хэвлэхгүй, зөвхөн харьцуулна.
- Хоёр дахь давталтад дугаар хэрэгтэй: `forEach`-ийн функцийн хоёр дахь
  параметр нь индекс (0-ээс эхэлнэ), дугаар = индекс + 1.
- «Дунджаас их» гэдэг нь `>` — дундажтай тэнцүү дүн тоологдохгүй.
""",
            ),
        ),
        LessonSpec(
            title="map, filter, find",
            slug="map-filter-find",
            description="Массивыг хувиргах, шүүх, хайх.",
            duration=480,
            content="""\
Эдгээр метод нь давталт бичихгүйгээр массивтай ажиллах боломж олгоно.
Гурвуулаа **шинэ утга буцаана** — эх массивыг өөрчлөхгүй.

### `map` — хувиргана

Элемент бүрийг өөр утга болгож, **ижил урттай** шинэ массив өгнө:

```javascript
const toonuud = [1, 2, 3];
const hoyorDahin = toonuud.map((too) => too * 2);

console.log(hoyorDahin); // [2, 4, 6]
console.log(toonuud);    // [1, 2, 3] — хэвээрээ
```

### `filter` — шүүнэ

Нөхцөлд таарсан элементүүдийг л үлдээнэ:

```javascript
const toonuud = [4, 9, 12, 7];
const tomuud = toonuud.filter((too) => too > 8);

console.log(tomuud); // [9, 12]
```

Буцаах функц нь `true` эсвэл `false` өгөх ёстой.

### `find` — эхний таарсныг олно

```javascript
const nasuud = [15, 17, 22, 30];

const oldson = nasuud.find((nas) => nas >= 18);
console.log(oldson); // 22 — 30 ч таарах боловч эхнийх нь л буцна
```

Олдохгүй бол `undefined` буцаана. Индексийг хүсвэл `findIndex`.
Модул 7-д үзэх объекттой хамт хэрэглэвэл жишээ нь «нэр нь Сараа
хэрэглэгчийг ол» гэх мэт ажилд хамгийн их хэрэг болно.

### Харьцуулалт

| Метод | Буцаах зүйл |
|---|---|
| `map` | Ижил урттай шинэ массив |
| `filter` | Богиносч болох шинэ массив |
| `find` | Ганц элемент эсвэл `undefined` |
| `some` | Аль нэг нь таарвал `true` |
| `every` | Бүгд таарвал `true` |

### Гинжлэх

Метод бүр массив буцаадаг тул дараалуулж бичиж болно:

```javascript
const ur = toonuud
  .filter((too) => too > 5)
  .map((too) => too * 10);
```
""",
            initial_code="""\
const n = Number(prompt());
const dunguud = [];
for (let i = 0; i < n; i++) {
  dunguud.push(Number(prompt()));
}

// Дүнг үсгэн үнэлгээ болгоно — бэлэн
const useg = (dun) => {
  if (dun >= 90) {
    return "A";
  }
  if (dun >= 80) {
    return "B";
  }
  if (dun >= 70) {
    return "C";
  }
  if (dun >= 60) {
    return "D";
  }
  return "F";
};

// TODO 1: map — дүн бүрийг "<дүн>: <үнэлгээ>" мөр болгоод, мөр бүрийг хэвлэ

// TODO 2: filter — 60 ба түүнээс дээш дүнг шүүгээд тоог нь хэвлэ
console.log("Тэнцсэн: ?");

// TODO 3: find — 90 ба түүнээс дээш ЭХНИЙ дүн (олдохгүй бол "байхгүй")
console.log("Эхний онц: ?");

// TODO 4: every — бүх дүн 60 ба түүнээс дээш үү? ("тийм" эсвэл "үгүй")
console.log("Бүгд тэнцсэн: ?");
""",
            exercise=ExerciseSpec(
                statement="""\
Шалгалтын дүнгүүдийг `map`, `filter`, `find`, `every`-ээр боловсруул.

Үсгэн үнэлгээний дүрмийг эхлэл кодын `useg` функц бэлэн хийдэг:

| Дүн | Үнэлгээ |
|---|---|
| 90 ба түүнээс дээш | A |
| 80–89 | B |
| 70–79 | C |
| 60–69 | D |
| 60-аас доош | F |

**Оролт:** эхний мөрөнд дүнгийн тоо `n` (1 ба түүнээс их), дараагийн `n`
мөр бүрт нэг дүн (0–100 бүхэл тоо).

**Гаралт:** эхлээд дүн бүрт нэг мөр (оролтын дарааллаар), дараа нь гурван
мөр:

```text
<дүн>: <үнэлгээ>
…
Тэнцсэн: <60 ба түүнээс дээш дүнгийн тоо>
Эхний онц: <90 ба түүнээс дээш ЭХНИЙ дүн, эсвэл байхгүй>
Бүгд тэнцсэн: <тийм эсвэл үгүй>
```
""",
                tests=(
                    TestCaseSpec(
                        stdin="4\n75\n92\n58\n88\n",
                        expected_output="75: C\n92: A\n58: F\n88: B\nТэнцсэн: 3\nЭхний онц: 92\nБүгд тэнцсэн: үгүй\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="3\n60\n70\n80\n",
                        expected_output="60: D\n70: C\n80: B\nТэнцсэн: 3\nЭхний онц: байхгүй\nБүгд тэнцсэн: тийм\n",
                    ),
                    TestCaseSpec(
                        stdin="1\n100\n",
                        expected_output="100: A\nТэнцсэн: 1\nЭхний онц: 100\nБүгд тэнцсэн: тийм\n",
                    ),
                    TestCaseSpec(
                        stdin="5\n59\n90\n95\n0\n89\n",
                        expected_output="59: F\n90: A\n95: A\n0: F\n89: B\nТэнцсэн: 3\nЭхний онц: 90\nБүгд тэнцсэн: үгүй\n",
                    ),
                    TestCaseSpec(
                        stdin="2\n10\n69\n",
                        expected_output="10: F\n69: D\nТэнцсэн: 1\nЭхний онц: байхгүй\nБүгд тэнцсэн: үгүй\n",
                    ),
                ),
                solution="""\
const n = Number(prompt());
const dunguud = [];
for (let i = 0; i < n; i++) {
  dunguud.push(Number(prompt()));
}

const useg = (dun) => {
  if (dun >= 90) {
    return "A";
  }
  if (dun >= 80) {
    return "B";
  }
  if (dun >= 70) {
    return "C";
  }
  if (dun >= 60) {
    return "D";
  }
  return "F";
};

const muruud = dunguud.map((dun) => `${dun}: ${useg(dun)}`);
muruud.forEach((mur) => console.log(mur));

const tentssen = dunguud.filter((dun) => dun >= 60);
console.log(`Тэнцсэн: ${tentssen.length}`);

const onts = dunguud.find((dun) => dun >= 90);
console.log(`Эхний онц: ${onts === undefined ? "байхгүй" : onts}`);

const bugdTentssen = dunguud.every((dun) => dun >= 60);
console.log(`Бүгд тэнцсэн: ${bugdTentssen ? "тийм" : "үгүй"}`);
""",
                tips="""\
- `map` нь ижил урттай **шинэ** массив буцаана — дүн бүрээс нэг мөр. Дараа
  нь мөр бүрийг `forEach`-ээр хэвлэ.
- `filter`-ийн үр дүн нь массив — тоог нь `.length`-ээр ав.
- `find` олдохгүй бол `undefined` буцаана; тэр үед `байхгүй` гэж хэвлэ
  (гурвалсан оператор тохирно).
- `every` нь `true`/`false` өгнө — `тийм`/`үгүй` болгож хэвлэ.
- Callback бүр **утга буцаах** ёстой: `(dun) => dun >= 60` гэх мэт богино
  хэлбэр хамгийн тохиромжтой.
""",
            ),
        ),
        LessonSpec(
            title="reduce",
            slug="reduce",
            description="Массивыг ганц утга болгон нэгтгэх.",
            duration=480,
            content="""\
`reduce` нь массивыг **ганц утга** болгон хумина. Нийлбэр, дундаж,
бүлэглэлт зэрэгт ашиглана.

```javascript
const toonuud = [10, 20, 30];

const niilber = toonuud.reduce((huriml, too) => huriml + too, 0);
console.log(niilber); // 60
```

### Хоёр аргумент

```text
reduce(callback, ehleliinUtga)
```

`callback` нь хоёр зүйл авна:

| Нэр | Утга |
|---|---|
| Хуримтлуулагч | Өмнөх алхмуудын үр дүн |
| Одоогийн элемент | Массивын энэ удаагийн утга |

### Алхам алхмаар

`[10, 20, 30]` дээр эхлэлийн утга `0` байвал:

| Алхам | Хуримтлуулагч | Элемент | Үр дүн |
|---|---|---|---|
| 1 | 0 | 10 | 10 |
| 2 | 10 | 20 | 30 |
| 3 | 30 | 30 | 60 |

### Эхлэлийн утгыг бүү мартаарай

Өгөхгүй бол эхний элемент нь эхлэлийн утга болно. Хоосон массив дээр
алдаа заана:

```javascript
[].reduce((a, b) => a + b);     // TypeError
[].reduce((a, b) => a + b, 0);  // 0 — аюулгүй
```

### Зөвхөн нийлбэрт зориулагдаагүй

Хуримтлуулагч нь «одоог хүртэлх хариу» гэж бодоход л болно. Жишээ нь
хэдэн удаа тааралдсаныг тоолж болно:

```javascript
const uguuluud = ["алим", "гадил", "алим"];

const alimToo = uguuluud.reduce((too, ug) => {
  if (ug === "алим") {
    return too + 1;
  }
  return too;
}, 0);

console.log(alimToo); // 2
```

### Хэзээ ашиглахгүй байх вэ

Энгийн нийлбэрээс хэтэрсэн үед `reduce` хурдан уншихад хэцүү болдог.
Тодорхойгүй санагдвал энгийн `for...of` давталт бич — буруу зүйл биш.
""",
            initial_code="""\
const n = Number(prompt());
const guilgee = [];
for (let i = 0; i < n; i++) {
  guilgee.push(Number(prompt()));
}

// Бүх гүйлгээний нийлбэр — жишээ болгож бэлэн бичсэн
const uldegdel = guilgee.reduce((niit, dun) => niit + dun, 0);

// TODO: зөвхөн ЭЕРЭГ гүйлгээг нэмдэг reduce (сөрөг дүнг алгас)
const orlogo = 0;

// TODO: зарлагын нийлбэр, эерэг тоогоор (-12000 → 12000)
const zarlaga = 0;

// TODO: хамгийн том зарлага — хуримтлуулагч нь «одоог хүртэлх хамгийн их зарлага»
const ihZarlaga = 0;

console.log(`Орлого: ${orlogo}`);
console.log(`Зарлага: ${zarlaga}`);
console.log(`Үлдэгдэл: ${uldegdel}`);
console.log(`Хамгийн их зарлага: ${ihZarlaga}`);
""",
            exercise=ExerciseSpec(
                statement="""\
Дансны гүйлгээнүүдийг `reduce`-ээр нэгтгэ.

Гүйлгээ бүр бүхэл тоо: **эерэг** бол орлого, **сөрөг** бол зарлага.
Жишээ нь `-12000` нь 12000 төгрөгийн зарлага.

**Оролт:** эхний мөрөнд гүйлгээний тоо `n` (1 ба түүнээс их), дараагийн `n`
мөр бүрт нэг гүйлгээ.

**Гаралт:** яг дөрвөн мөр:

```text
Орлого: <эерэг гүйлгээнүүдийн нийлбэр>
Зарлага: <зарлагуудын нийлбэр, эерэг тоогоор>
Үлдэгдэл: <бүх гүйлгээний нийлбэр>
Хамгийн их зарлага: <хамгийн том зарлага, эерэг тоогоор; зарлагагүй бол 0>
```
""",
                tests=(
                    TestCaseSpec(
                        stdin="5\n50000\n-12000\n-20000\n8000\n-3000\n",
                        expected_output="Орлого: 58000\nЗарлага: 35000\nҮлдэгдэл: 23000\nХамгийн их зарлага: 20000\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="3\n1000\n2000\n3000\n",
                        expected_output="Орлого: 6000\nЗарлага: 0\nҮлдэгдэл: 6000\nХамгийн их зарлага: 0\n",
                    ),
                    TestCaseSpec(
                        stdin="2\n-500\n-700\n",
                        expected_output="Орлого: 0\nЗарлага: 1200\nҮлдэгдэл: -1200\nХамгийн их зарлага: 700\n",
                    ),
                    TestCaseSpec(
                        stdin="1\n-5\n",
                        expected_output="Орлого: 0\nЗарлага: 5\nҮлдэгдэл: -5\nХамгийн их зарлага: 5\n",
                    ),
                    TestCaseSpec(
                        stdin="4\n-100\n100\n-100\n100\n",
                        expected_output="Орлого: 200\nЗарлага: 200\nҮлдэгдэл: 0\nХамгийн их зарлага: 100\n",
                    ),
                ),
                solution="""\
const n = Number(prompt());
const guilgee = [];
for (let i = 0; i < n; i++) {
  guilgee.push(Number(prompt()));
}

const uldegdel = guilgee.reduce((niit, dun) => niit + dun, 0);

// Нөхцөл таарахгүй бол хуримтлуулагчаа өөрчлөлгүй буцаана
const orlogo = guilgee.reduce((niit, dun) => (dun > 0 ? niit + dun : niit), 0);

// Сөрөг дүнг хасвал эерэг болж нэмэгдэнэ: 0 - (-12000) = 12000
const zarlaga = guilgee.reduce((niit, dun) => (dun < 0 ? niit - dun : niit), 0);

const ihZarlaga = guilgee.reduce((ih, dun) => (-dun > ih ? -dun : ih), 0);

console.log(`Орлого: ${orlogo}`);
console.log(`Зарлага: ${zarlaga}`);
console.log(`Үлдэгдэл: ${uldegdel}`);
console.log(`Хамгийн их зарлага: ${ihZarlaga}`);
""",
                tips="""\
- Хуримтлуулагч бол «одоог хүртэлх хариу». Орлогын хувьд: дүн эерэг бол
  нэм, үгүй бол хуримтлуулагчаа **өөрчлөлгүй** буцаа.
- Callback нөхцөл бүрт утга буцаах ёстой — эс бөгөөс дараагийн алхамд
  хуримтлуулагч `undefined` болно. Гурвалсан оператор тохиромжтой.
- Зарлагыг эерэг тоо болгохын тулд сөрөг дүнг **хас**: `niit - dun`.
- Хамгийн том зарлага: хуримтлуулагч нь «одоог хүртэлх хамгийн их зарлага».
  Энэ удаагийн зарлага (`-dun`) түүнээс их бол түүнийг, үгүй бол
  хуримтлуулагчаа буцаа. Эхлэлийн утга `0` тул зарлагагүй бол 0 гарна.
""",
            ),
        ),
    ],
)

OBJECTS = ModuleSpec(
    title="Модул 7 — Объект (Objects)",
    description="Холбоотой өгөгдлийг нэр бүхий талбаруудад бүлэглэх.",
    lessons=[
        LessonSpec(
            title="Объект ба шинж чанар",
            slug="obyekt-ba-shinj-chanar",
            description="Түлхүүр-утгын хос үүсгэх, хандах.",
            duration=400,
            content="""\
Объект нь холбоотой өгөгдлийг **нэртэй** талбаруудад хадгална.

```javascript
const hereglegch = {
  ner: "Бат",
  nas: 20,
  idevhtei: true,
};
```

Массив нь **дараалал** чухал үед, объект нь **нэр** чухал үед
тохиромжтой.

### Хандах хоёр арга

```javascript
console.log(hereglegch.ner);      // цэгээр — ердийн
console.log(hereglegch["ner"]);   // хаалтаар
```

Хаалтат хэлбэр нь талбарын нэр **хувьсагчид** байгаа үед хэрэгтэй:

```javascript
const talbar = "nas";
console.log(hereglegch[talbar]); // 20
```

### Үүрлэсэн объект

```javascript
const hereglegch = {
  ner: "Бат",
  hayag: {
    hot: "Улаанбаатар",
    duureg: "Баянзүрх",
  },
};

console.log(hereglegch.hayag.hot);
```

### Байхгүй талбар

Алдаа заахгүй, `undefined` буцаана:

```javascript
console.log(hereglegch.utas); // undefined
```

Гэхдээ байхгүй объектын дотор орох гэвэл алдаа заана:

```javascript
console.log(hereglegch.ajil.albanTushaal); // TypeError
```

Үүнээс сэргийлэхийн тулд `?.` оператор бий (Модул 15).

### Талбаруудыг жагсаах

```javascript
console.log(Object.keys(hereglegch));   // талбаруудын нэр
console.log(Object.values(hereglegch)); // утгууд
console.log(Object.entries(hereglegch)); // хосууд
```
""",
            initial_code="""\
// Үнийн жагсаалт — түлхүүр нь барааны нэр, утга нь үнэ
const une = {
  талх: 2500,
  // TODO: хүснэгтийн үлдсэн 4 барааг нэм
};

// TODO: жагсаалтад хэдэн төрлийн бараа байгааг Object.keys-ээр тоол
console.log("Бараа: ? төрөл");

let niit = 0;
const n = Number(prompt());
for (let i = 0; i < n; i++) {
  const ner = prompt();
  // TODO: une[ner] нь undefined бол "<нэр>: олдсонгүй" гэж хэвлэ,
  //       эс бөгөөс "<нэр>: <үнэ>" гэж хэвлээд үнийг niit-д нэм
}

console.log(`Нийт: ${niit}`);
""",
            exercise=ExerciseSpec(
                statement="""\
Дэлгүүрийн үнийн жагсаалтыг **объектоор** хадгалаад, захиалсан барааг
нэрээр нь хай.

| Бараа | Үнэ |
|---|---|
| талх | 2500 |
| сүү | 3200 |
| өндөг | 450 |
| алим | 1500 |
| ус | 1000 |

Барааны нэр нь объектын түлхүүр, үнэ нь утга. Нэрийг оролтоос уншдаг тул
хаалтат хэлбэрээр (`une[ner]`) хандана. Нэр жагсаалтынхтай **яг** таарах
ёстой — `Талх` нь `талх` биш.

**Оролт:** эхний мөрөнд захиалсан барааны тоо `n`, дараагийн `n` мөр бүрт
нэг барааны нэр.

**Гаралт:** эхний мөрөнд жагсаалт дахь барааны төрлийн тоо, дараа нь
захиалсан бараа бүрт нэг мөр, эцэст нь олдсон бараануудын нийт үнэ:

```text
Бараа: <төрлийн тоо> төрөл
<нэр>: <үнэ эсвэл олдсонгүй>
…
Нийт: <олдсон бараануудын үнийн нийлбэр>
```
""",
                tests=(
                    TestCaseSpec(
                        stdin="3\nталх\nсүү\nталх\n",
                        expected_output="Бараа: 5 төрөл\nталх: 2500\nсүү: 3200\nталх: 2500\nНийт: 8200\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="2\nкофе\nус\n",
                        expected_output="Бараа: 5 төрөл\nкофе: олдсонгүй\nус: 1000\nНийт: 1000\n",
                    ),
                    TestCaseSpec(
                        stdin="1\nөндөг\n",
                        expected_output="Бараа: 5 төрөл\nөндөг: 450\nНийт: 450\n",
                    ),
                    TestCaseSpec(
                        stdin="4\nалим\nалим\nшоколад\nсүү\n",
                        expected_output="Бараа: 5 төрөл\nалим: 1500\nалим: 1500\nшоколад: олдсонгүй\nсүү: 3200\nНийт: 6200\n",
                    ),
                    TestCaseSpec(
                        stdin="2\nТалх\nөндөг\n",
                        expected_output="Бараа: 5 төрөл\nТалх: олдсонгүй\nөндөг: 450\nНийт: 450\n",
                    ),
                ),
                solution="""\
const une = {
  талх: 2500,
  сүү: 3200,
  өндөг: 450,
  алим: 1500,
  ус: 1000,
};

console.log(`Бараа: ${Object.keys(une).length} төрөл`);

let niit = 0;
const n = Number(prompt());
for (let i = 0; i < n; i++) {
  const ner = prompt();
  // Түлхүүр ner хувьсагчид байгаа тул цэг биш хаалт
  if (une[ner] === undefined) {
    console.log(`${ner}: олдсонгүй`);
  } else {
    console.log(`${ner}: ${une[ner]}`);
    niit += une[ner];
  }
}

console.log(`Нийт: ${niit}`);
""",
                tips="""\
- Объектын хос бүр `түлхүүр: утга`, хосуудын хооронд таслал.
- Түлхүүр хувьсагчид байгаа үед цэг биш хаалт хэрэглэнэ: `une.ner` нь
  `"ner"` нэртэй талбарыг хайна, `une[ner]` нь хувьсагчийн **утгаар** хайна.
- Байхгүй түлхүүр алдаа заахгүй, `undefined` буцаана — үүгээр «олдсонгүй»-г
  танина.
- `Object.keys(une)` нь түлхүүрүүдийн массив — `.length` нь төрлийн тоо.
""",
            ),
        ),
        LessonSpec(
            title="Метод, талбар нэмэх ба хасах",
            slug="obyekt-metod",
            description="Объектын доторх функц. Талбар нэмэх, устгах.",
            duration=420,
            content="""\
### Метод

Объектын доторх функцийг **метод** гэнэ:

```javascript
const hereglegch = {
  ner: "Бат",
  mendchileh() {
    return `Сайн уу, би ${this.ner}`;
  },
};

console.log(hereglegch.mendchileh());
```

### `this`

`this` нь **методыг дуудсан объектыг** заана. Дээрх жишээнд
`hereglegch.mendchileh()` гэж дуудсан тул `this` нь `hereglegch`.

> Сум функц дотор `this` өөрөөр ажилладаг тул метод бичихдээ энгийн
> хэлбэрийг ашигла.

```javascript
const buruu = {
  ner: "Бат",
  mendchileh: () => `Сайн уу, ${this.ner}`, // ажиллахгүй
};
```

### Талбар нэмэх, өөрчлөх

```javascript
hereglegch.utas = "99112233"; // нэмнэ
hereglegch.nas = 21;          // өөрчилнө
```

### Талбар хасах

```javascript
delete hereglegch.utas;
```

### Талбар байгаа эсэх

```javascript
console.log("ner" in hereglegch);              // true
console.log(hereglegch.utas !== undefined);    // false
```

`in` нь утга нь `undefined` байсан ч талбар өөрөө байгаа эсэхийг хэлнэ —
хоёр шалгалт өөр зүйл гэдгийг анхаар.

### Богино бичлэг

Хувьсагчийн нэр талбарын нэртэй ижил бол дахин бичих шаардлагагүй:

```javascript
const ner = "Бат";
const nas = 20;

const hereglegch = { ner, nas }; // { ner: "Бат", nas: 20 }
```
""",
            initial_code="""\
const baatar = {
  ner: prompt(),
  ami: 100,
  tsohiulah(dun) {
    // TODO: this.ami-г dun-аар багасга; 0-ээс доош орвол 0 болго
  },
  emchleh(dun) {
    // TODO: this.ami-г dun-аар нэмэгдүүл; 100-аас хэтэрвэл 100 болго
  },
  tuluv() {
    // TODO: ами 0 бол "<нэр> ялагдлаа" гэж буцаа
    return `${this.ner}: ${this.ami} ами`;
  },
};

const n = Number(prompt());
for (let i = 0; i < n; i++) {
  const uildel = prompt();
  const dun = Number(prompt());
  // TODO: uildel нь "цохилт" бол tsohiulah, "эмчилгээ" бол emchleh методыг дууд
  console.log(baatar.tuluv());
}
""",
            exercise=ExerciseSpec(
                statement="""\
Тоглоомын баатрыг **метод**-той объектоор загварчил.

Баатар `ner` (нэр) ба `ami` (ами, эхэндээ 100) талбартай, гурван методтой:

- `tsohiulah(dun)` — амийг `dun`-аар багасгана, гэхдээ 0-ээс доош
  оруулахгүй;
- `emchleh(dun)` — амийг `dun`-аар нэмнэ, гэхдээ 100-аас хэтрүүлэхгүй;
- `tuluv()` — төлвийг мөр болгож **буцаана**: ами 0 бол
  `<нэр> ялагдлаа`, эс бөгөөс `<нэр>: <ами> ами`.

Методууд өөрийн объектын талбарт `this`-ээр хандана.

**Оролт:** 1-р мөрөнд баатрын нэр, 2-р мөрөнд үйлдлийн тоо `n`. Дараа нь
үйлдэл бүр хоёр мөр: үйлдлийн нэр (`цохилт` эсвэл `эмчилгээ`) ба тоо (эерэг
бүхэл тоо).

**Гаралт:** үйлдэл бүрийн дараа `tuluv()`-ийн буцаасан мөр:

```text
<нэр>: <ами> ами
<нэр> ялагдлаа
```
""",
                tests=(
                    TestCaseSpec(
                        stdin="Бат\n3\nцохилт\n30\nэмчилгээ\n10\nцохилт\n50\n",
                        expected_output="Бат: 70 ами\nБат: 80 ами\nБат: 30 ами\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="Сараа\n2\nэмчилгээ\n50\nцохилт\n120\n",
                        expected_output="Сараа: 100 ами\nСараа ялагдлаа\n",
                    ),
                    TestCaseSpec(
                        stdin="Дорж\n3\nцохилт\n100\nэмчилгээ\n40\nцохилт\n39\n",
                        expected_output="Дорж ялагдлаа\nДорж: 40 ами\nДорж: 1 ами\n",
                    ),
                    TestCaseSpec(
                        stdin="Туяа\n1\nцохилт\n1\n",
                        expected_output="Туяа: 99 ами\n",
                    ),
                    TestCaseSpec(
                        stdin="Болд\n4\nцохилт\n60\nцохилт\n60\nэмчилгээ\n200\nцохилт\n5\n",
                        expected_output="Болд: 40 ами\nБолд ялагдлаа\nБолд: 100 ами\nБолд: 95 ами\n",
                    ),
                ),
                solution="""\
const baatar = {
  ner: prompt(),
  ami: 100,
  tsohiulah(dun) {
    this.ami -= dun;
    if (this.ami < 0) {
      this.ami = 0;
    }
  },
  emchleh(dun) {
    this.ami += dun;
    if (this.ami > 100) {
      this.ami = 100;
    }
  },
  tuluv() {
    if (this.ami === 0) {
      return `${this.ner} ялагдлаа`;
    }
    return `${this.ner}: ${this.ami} ами`;
  },
};

const n = Number(prompt());
for (let i = 0; i < n; i++) {
  const uildel = prompt();
  const dun = Number(prompt());
  if (uildel === "цохилт") {
    baatar.tsohiulah(dun);
  } else {
    baatar.emchleh(dun);
  }
  console.log(baatar.tuluv());
}
""",
                tips="""\
- Метод дотор объектын талбарт `this.ami` гэж хандана — `baatar.tsohiulah(…)`
  гэж дуудахад `this` нь `baatar` болно.
- Методыг энгийн `нэр(параметр) { … }` хэлбэрээр бич — сум функц дотор
  `this` объектыг заахгүй.
- Хязгаарыг өөрчилсний **дараа** шалга: эхлээд хас, дараа нь 0-ээс бага
  болсон бол 0 болго.
- `tuluv()` хэвлэхгүй, мөр **буцаана** — хэвлэх нь давталтын ажил.
""",
            ),
        ),
        LessonSpec(
            title="Задлах ба тараах",
            slug="zadlah-ba-taraah",
            description="Destructuring болон spread оператор.",
            duration=450,
            content="""\
### Объект задлах (destructuring)

Талбаруудыг шууд хувьсагч болгож гаргаж авна:

```javascript
const hereglegch = { ner: "Бат", nas: 20, hot: "Улаанбаатар" };

const { ner, nas } = hereglegch;
console.log(ner, nas); // "Бат" 20
```

Уртаар бичсэнтэй адил:

```javascript
const ner = hereglegch.ner;
const nas = hereglegch.nas;
```

### Нэр солих ба анхдагч утга

```javascript
const { ner: neriinUtga, utas = "байхгүй" } = hereglegch;

console.log(neriinUtga); // "Бат"
console.log(utas);       // "байхгүй" — талбар байхгүй тул анхдагч
```

### Массив задлах

```javascript
const unguud = ["улаан", "ногоон", "цэнхэр"];
const [negdugeer, hoyordugaar] = unguud;

console.log(negdugeer); // "улаан"
```

### Функцийн параметрт

Хамгийн их хэрэглэгддэг газар нь энэ:

```javascript
function hevleh({ ner, nas }) {
  console.log(`${ner} — ${nas} настай`);
}

hevleh(hereglegch);
```

### Тараах оператор (spread)

`...` нь объект эсвэл массивын агуулгыг задлан "асгана":

```javascript
const suuri = { ner: "Бат", nas: 20 };
const delgerengui = { ...suuri, hot: "Улаанбаатар" };

console.log(delgerengui); // гурван талбартай шинэ объект
```

Хуулбар авах хамгийн түгээмэл арга нь энэ. Эх объект **өөрчлөгдөхгүй**.

```javascript
const shine = { ...suuri, nas: 21 }; // nas-ийг дарж бичнэ
```

### Гүехэн хуулбар

`...` нь зөвхөн **эхний давхаргыг** хуулна. Дотор нь объект байвал
хоёулаа ижил объектыг зааж байх болно:

```javascript
const a = { hayag: { hot: "УБ" } };
const b = { ...a };

b.hayag.hot = "Дархан";
console.log(a.hayag.hot); // "Дархан" — а ч өөрчлөгдлөө!
```
""",
            initial_code="""\
const ner = prompt();
const nas = Number(prompt());
const hot = prompt();
const shineHot = prompt(); // "-" бол хот өөрчлөгдөхгүй

const umnu = { ner, nas, hot };

// TODO: параметрийг { ner, nas, hot } гэж задалж ав —
//       hereglegch.ner гэж бичих шаардлагагүй болно
function tanilzuulah(hereglegch) {
  return `${hereglegch.ner}, ${hereglegch.nas} нас, ${hereglegch.hot}`;
}

// TODO: umnu-г ...-аар хуулж, nas-ийг 1-ээр нэмэгдүүлж, hot-ийг shineHot болго
//       (shineHot нь "-" бол хот хэвээрээ). umnu өөрөө өөрчлөгдөх ёсгүй!
const odoo = umnu;

console.log(`Өмнө: ${tanilzuulah(umnu)}`);
console.log(`Одоо: ${tanilzuulah(odoo)}`);
""",
            exercise=ExerciseSpec(
                statement="""\
Хэрэглэгчийн мэдээллийг **хуулбар** дээр шинэчил — эх объект өөрчлөгдөх
ёсгүй.

Нэг жил өнгөрөхөд хэрэглэгчийн нас 1-ээр нэмэгдэж, магадгүй өөр хот руу
нүүнэ. Шинэ мэдээллийг `...` (тараах) оператороор **шинэ объект** болгож
үүсгэ, дараа нь хуучин ба шинэ мэдээллийг хоёуланг нь хэвлэ.

Мэдээллийг мөр болгодог `tanilzuulah` функц объектыг **параметртээ
задалж** (`{ ner, nas, hot }`) авна.

**Оролт:** дөрвөн мөр — нэр, нас (бүхэл тоо), хот, шинэ хот. Шинэ хот нь
`-` бол хот өөрчлөгдөхгүй.

**Гаралт:** яг хоёр мөр:

```text
Өмнө: <нэр>, <нас> нас, <хот>
Одоо: <нэр>, <нас + 1> нас, <шинэ хот>
```
""",
                tests=(
                    TestCaseSpec(
                        stdin="Бат\n20\nУлаанбаатар\nДархан\n",
                        expected_output="Өмнө: Бат, 20 нас, Улаанбаатар\nОдоо: Бат, 21 нас, Дархан\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="Сараа\n17\nЭрдэнэт\n-\n",
                        expected_output="Өмнө: Сараа, 17 нас, Эрдэнэт\nОдоо: Сараа, 18 нас, Эрдэнэт\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="Дорж\n0\nХовд\nМөрөн\n",
                        expected_output="Өмнө: Дорж, 0 нас, Ховд\nОдоо: Дорж, 1 нас, Мөрөн\n",
                    ),
                    TestCaseSpec(
                        stdin="Бат Болд\n45\nДархан\nДархан\n",
                        expected_output="Өмнө: Бат Болд, 45 нас, Дархан\nОдоо: Бат Болд, 46 нас, Дархан\n",
                    ),
                    TestCaseSpec(
                        stdin="Анар\n99\nЗуунмод\n-\n",
                        expected_output="Өмнө: Анар, 99 нас, Зуунмод\nОдоо: Анар, 100 нас, Зуунмод\n",
                    ),
                ),
                solution="""\
const ner = prompt();
const nas = Number(prompt());
const hot = prompt();
const shineHot = prompt();

const umnu = { ner, nas, hot };

function tanilzuulah({ ner, nas, hot }) {
  return `${ner}, ${nas} нас, ${hot}`;
}

// Эхлээд бүх талбарыг хуулна, ард нь бичсэн талбар түүнийг дарж бичнэ
const odoo = {
  ...umnu,
  nas: umnu.nas + 1,
  hot: shineHot === "-" ? umnu.hot : shineHot,
};

console.log(`Өмнө: ${tanilzuulah(umnu)}`);
console.log(`Одоо: ${tanilzuulah(odoo)}`);
""",
                tips="""\
- `{ ...umnu, nas: … }` — эхлээд бүх талбарыг хуулна, ард нь бичсэн талбар
  хуулсныг **дарж** бичнэ. `...umnu`-г сүүлд бичвэл хуучин утга буцаад дарна.
- `const odoo = umnu;` нь хуулбар биш — хоёр нэр **нэг** объектыг заана.
  `odoo.nas++` хийвэл «Өмнө» мөр ч өөрчлөгдөнө.
- Задалсан параметр `function tanilzuulah({ ner, nas, hot })` нь функцийн
  эхэнд `const { ner, nas, hot } = hereglegch;` бичсэнтэй адил.
- `-` эсэхийг шалгахад гурвалсан оператор тохиромжтой.
""",
            ),
        ),
    ],
)

STRINGS = ModuleSpec(
    title="Модул 8 — Мөр (Strings)",
    description="Текст боловсруулах, хайх, хэлбэржүүлэх.",
    lessons=[
        LessonSpec(
            title="Мөрийн метод",
            slug="muriin-metod",
            description="Урт, том жижиг үсэг, зай авах, хэсэг тасдах.",
            duration=400,
            content="""\
Мөр нь массив шиг индекстэй:

```javascript
const ner = "MedlegHub";

console.log(ner.length);      // 9
console.log(ner[0]);          // "M"
console.log(ner.at(-1));      // "b"
```

### Түгээмэл метод

| Метод | Үйлдэл |
|---|---|
| `toUpperCase()` | Том үсэг болгоно |
| `toLowerCase()` | Жижиг үсэг болгоно |
| `trim()` | Хоёр талын зайг авна |
| `slice(a, b)` | Хэсэг тасдана |
| `replace(a, b)` | Эхний тохиолдлыг солино |
| `replaceAll(a, b)` | Бүх тохиолдлыг солино |
| `repeat(n)` | n удаа давтана |
| `padStart(n, "0")` | Урд нь тэмдэгт нэмж уртасгана |
| `padEnd(n)` | Ард нь зай нэмж уртасгана — баганаар жагсаахад |

### Мөр өөрчлөгддөггүй

Метод бүр **шинэ мөр** буцаана. Эх мөр хэвээрээ үлдэнэ:

```javascript
const ner = "бат";
ner.toUpperCase();
console.log(ner); // "бат" — хэвээрээ

const tom = ner.toUpperCase();
console.log(tom); // "БАТ"
```

Энэ бол шинэ суралцагчийн байнгын алдаа — үр дүнг **хадгалахаа** бүү мартаарай.

### `slice`

```javascript
const text = "JavaScript";

console.log(text.slice(0, 4));  // "Java"
console.log(text.slice(4));     // "Script"
console.log(text.slice(-6));    // "Script" — сүүлээс
```

### Хэлбэржүүлэлтэд хэрэгтэй

```javascript
console.log(String(7).padStart(2, "0")); // "07"
```

Цаг, огноо харуулахад байнга хэрэглэгдэнэ.
""",
            initial_code="""\
const n = Number(prompt());

for (let i = 1; i <= n; i++) {
  const tuuhii = prompt();

  // TODO: хоёр талын илүү зайг ав (trim)
  const tseverlesen = tuuhii;

  // TODO: эхний үсгийг том, бусдыг нь жижиг болго (slice, toUpperCase, toLowerCase)
  const ner = tseverlesen;

  // TODO: дугаарыг 2 оронтой болго: 1 → "01" (String, padStart)
  const dugaar = i;

  console.log(`${dugaar}. ${ner}`);
}
""",
            exercise=ExerciseSpec(
                statement="""\
Хэрэглэгчдийн бичсэн нэрийг цэвэрлээд дугаарласан жагсаалт болго.

Нэр бүрийг:

1. хоёр талын илүү зайгүй болго;
2. эхний үсгийг **том**, бусдыг нь **жижиг** болго (`бАТ` → `Бат`);
3. урд нь 2 оронтой дугаар тавь: `01`, `02`, … `10`, `11`.

**Оролт:** эхний мөрөнд нэрийн тоо `n` (1–99), дараагийн `n` мөр бүрт нэг
нэр — нэг үг, урд хойно нь илүү зай байж болно, том жижиг үсэг холилдсон
байж болно.

**Гаралт:** нэр бүрт нэг мөр:

```text
<2 оронтой дугаар>. <Цэвэрлэсэн нэр>
```
""",
                tests=(
                    TestCaseSpec(
                        stdin="3\n  бат  \nСАРАА\nдОрЖ\n",
                        expected_output="01. Бат\n02. Сараа\n03. Дорж\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="1\nөнөр\n",
                        expected_output="01. Өнөр\n",
                    ),
                    TestCaseSpec(
                        stdin="2\n   ҮЙЛСТ\nа\n",
                        expected_output="01. Үйлст\n02. А\n",
                    ),
                    TestCaseSpec(
                        stdin="4\nmedlegHUB\n  js\nPYTHON  \nбАт\n",
                        expected_output="01. Medleghub\n02. Js\n03. Python\n04. Бат\n",
                    ),
                    TestCaseSpec(
                        stdin="10\nбат\nсараа\nдорж\nтуяа\nболд\nанар\nномин\nоюун\nтэмүүлэн\n  ЗОЛОО  \n",
                        expected_output=(
                            "01. Бат\n02. Сараа\n03. Дорж\n04. Туяа\n05. Болд\n"
                            "06. Анар\n07. Номин\n08. Оюун\n09. Тэмүүлэн\n10. Золоо\n"
                        ),
                    ),
                ),
                solution="""\
const n = Number(prompt());

for (let i = 1; i <= n; i++) {
  const tseverlesen = prompt().trim();
  // Эхний үсэг том + үлдсэн нь жижиг
  const ner = tseverlesen.slice(0, 1).toUpperCase() + tseverlesen.slice(1).toLowerCase();
  const dugaar = String(i).padStart(2, "0");
  console.log(`${dugaar}. ${ner}`);
}
""",
                tips="""\
- Мөрийн метод **шинэ** мөр буцаана — үр дүнг хувьсагчид хадгал, эс бөгөөс
  өөрчлөлт алга болно.
- Эхлээд `trim()` хий — эс бөгөөс «эхний үсэг» нь зай болно.
- Эхний үсэг: `slice(0, 1)`, үлдсэн хэсэг: `slice(1)`. Тус тусад нь том,
  жижиг болгоод `+`-ээр нийлүүл.
- Дугаар нь тоо — `padStart` мөрийн метод тул эхлээд `String(i)` болго.
""",
            ),
        ),
        LessonSpec(
            title="Хайх ба хуваах",
            slug="muriig-haih-ba-huvaah",
            description="includes, indexOf, startsWith, split, join.",
            duration=420,
            content="""\
### Хайх

```javascript
const text = "Сайн байна уу, MedlegHub";

console.log(text.includes("MedlegHub"));   // true
console.log(text.startsWith("Сайн"));    // true
console.log(text.endsWith("!"));         // false
console.log(text.indexOf("байна"));      // 5, олдохгүй бол -1
```

`includes` нь `indexOf`-оос уншихад хялбар тул зөвхөн "байгаа эсэх"
шалгах бол түүнийг сонго.

### Том, жижиг үсэг ялгана

Хайлт нь **үсгийн том жижгийг ялгана**:

```javascript
console.log("MedlegHub".includes("medleghub")); // false
```

Ялгаагүй хайхын тулд хоёуланг нь жижиг үсэг болго:

```javascript
const haih = (text, ug) =>
  text.toLowerCase().includes(ug.toLowerCase());
```

### Хуваах — `split`

Мөрийг массив болгоно:

```javascript
const uguuluud = "алим,гадил,интоор";
console.log(uguuluud.split(",")); // ["алим", "гадил", "интоор"]

const ug = "Сайн байна уу";
console.log(ug.split(" ")); // ["Сайн", "байна", "уу"]

console.log("Бат".split("")); // ["Б", "а", "т"] — үсэг тус бүрээр
```

Мөр таслах тэмдгээр хуваахдаа `split("\\n")` гэж бичнэ.

### Нийлүүлэх — `join`

`split`-ийн эсрэг үйлдэл:

```javascript
const nershuud = ["Бат", "Сараа", "Дорж"];

console.log(nershuud.join(", ")); // "Бат, Сараа, Дорж"
console.log(nershuud.join(""));   // "БатСарааДорж"
```

`split` ба `join`-ийг хослуулан мөр боловсруулах олон ажлыг гүйцэтгэж
болно.
""",
            initial_code="""\
const n = Number(prompt());
const domainuud = [];

for (let i = 0; i < n; i++) {
  const imeil = prompt();

  // TODO: хаягийг "@"-оор хуваа (split) — зөв хаяг яг хоёр хэсэгтэй
  // TODO: хэрэглэгчийн нэр хоосон биш, домэйн "." агуулсан (includes),
  //       "."-аар эхлээгүй (startsWith), "."-аар төгсөөгүй (endsWith) эсэхийг шалга
  const zuv = imeil.includes("@"); // одоохондоо дутуу шалгалт

  if (zuv) {
    // TODO: домэйныг domainuud-д нэмээд хаалтанд хэвлэ
    console.log(`${imeil}: зөв (?)`);
  } else {
    console.log(`${imeil}: буруу`);
  }
}

// TODO: domainuud-ийг ", "-ээр нийлүүл (join); хоосон бол "байхгүй"
console.log("Домэйнууд: байхгүй");
""",
            exercise=ExerciseSpec(
                statement="""\
Имэйл хаягуудыг шалгаж, зөв хаягуудын домэйныг цуглуул.

Имэйл **зөв** байх нөхцөл:

- `@` тэмдэг **яг нэг** удаа орсон;
- `@`-ийн өмнөх хэсэг (хэрэглэгчийн нэр) хоосон биш;
- `@`-ийн дараах хэсэг (домэйн) `.` агуулсан, гэхдээ `.`-аар эхлээгүй,
  `.`-аар төгсөөгүй.

**Оролт:** эхний мөрөнд хаягийн тоо `n`, дараагийн `n` мөр бүрт нэг хаяг
(зайгүй).

**Гаралт:** хаяг бүрт нэг мөр (`зөв` эсвэл `буруу`), эцэст нь зөв
хаягуудын домэйныг оролтын дарааллаар `, `-ээр тусгаарласан мөр. Зөв хаяг
байхгүй бол `Домэйнууд: байхгүй`.

```text
<хаяг>: зөв (<домэйн>)
<хаяг>: буруу
…
Домэйнууд: <домэйн>, <домэйн>, …
```
""",
                tests=(
                    TestCaseSpec(
                        stdin="3\nbat@gmail.com\nsaraa.gmail.com\ndorj@num.edu.mn\n",
                        expected_output=(
                            "bat@gmail.com: зөв (gmail.com)\n"
                            "saraa.gmail.com: буруу\n"
                            "dorj@num.edu.mn: зөв (num.edu.mn)\n"
                            "Домэйнууд: gmail.com, num.edu.mn\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="2\n@gmail.com\nbat@\n",
                        expected_output="@gmail.com: буруу\nbat@: буруу\nДомэйнууд: байхгүй\n",
                    ),
                    TestCaseSpec(
                        stdin="3\na@b@c.mn\nbold@.mn\ntuya@mail.\n",
                        expected_output=(
                            "a@b@c.mn: буруу\nbold@.mn: буруу\ntuya@mail.: буруу\nДомэйнууд: байхгүй\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="1\nanar@mail.mn\n",
                        expected_output="anar@mail.mn: зөв (mail.mn)\nДомэйнууд: mail.mn\n",
                    ),
                    TestCaseSpec(
                        stdin="4\nx@y.z\nnoatsign\nq@localhost\nm@a.b.c\n",
                        expected_output=(
                            "x@y.z: зөв (y.z)\n"
                            "noatsign: буруу\n"
                            "q@localhost: буруу\n"
                            "m@a.b.c: зөв (a.b.c)\n"
                            "Домэйнууд: y.z, a.b.c\n"
                        ),
                    ),
                ),
                solution="""\
const n = Number(prompt());
const domainuud = [];

for (let i = 0; i < n; i++) {
  const imeil = prompt();
  // "bat@gmail.com" → ["bat", "gmail.com"]
  const heseg = imeil.split("@");
  const zuv =
    heseg.length === 2 &&
    heseg[0] !== "" &&
    heseg[1].includes(".") &&
    !heseg[1].startsWith(".") &&
    !heseg[1].endsWith(".");

  if (zuv) {
    domainuud.push(heseg[1]);
    console.log(`${imeil}: зөв (${heseg[1]})`);
  } else {
    console.log(`${imeil}: буруу`);
  }
}

const jagsaalt = domainuud.length === 0 ? "байхгүй" : domainuud.join(", ");
console.log(`Домэйнууд: ${jagsaalt}`);
""",
                tips="""\
- `split("@")` нь массив буцаана: `"bat@gmail.com"` → `["bat", "gmail.com"]`.
  `@` хоёр байвал 3 хэсэг, огт байхгүй бол 1 хэсэг гарна — тиймээс
  `length`-ээр «яг нэг `@`»-ийг шалгана.
- `"@gmail.com"`-ийг хуваахад эхний хэсэг нь хоосон мөр `""` болно.
- Нөхцлүүдийг `&&`-ээр холбож нэг `zuv` хувьсагчид хадгалвал уншихад
  хялбар. «Эхлээгүй» гэдэг нь `!…startsWith(".")`.
- `join(", ")` нь элементүүдийн **хооронд** л тусгаарлагч тавина — төгсгөлд
  илүү таслал гарахгүй.
""",
            ),
        ),
        LessonSpec(
            title="Template literal ба хэлбэржүүлэлт",
            slug="template-literal-ba-helberjuulelt",
            description="Олон мөрт текст, тоо болон огноо хэлбэржүүлэх.",
            duration=420,
            content="""\
### Template literal

Backtick дотор `${}` ашиглан ямар ч илэрхийллийг шигтгэнэ:

```javascript
const ner = "Бат";
const nas = 20;

console.log(`${ner} нь ${nas} настай, ирэх жил ${nas + 1} болно.`);
```

### Олон мөрт текст

Backtick дотор мөр таслалт шууд хадгалагдана:

```javascript
const zahia = `Эрхэм ${ner},

Таны захиалга бүртгэгдлээ.

Хүндэтгэсэн,
MedlegHub`;
```

Энгийн хашилттай бол `\\n` бичих шаардлагатай байсан.

### Тоо хэлбэржүүлэх

```javascript
const une = 1234567.891;

console.log(une.toFixed(2));        // "1234567.89"
console.log(une.toLocaleString());  // "1,234,567.891"
```

Мөнгө харуулахад `toLocaleString` нь мянгатын таслалыг автоматаар тавина.

### Огноо

Огноог `Date` хадгална. `new Date(жил, сар, өдөр)` нь тухайн өдрийн огноог
**шинээр үүсгэнэ** — `new` түлхүүр үг нь «шинээр үүсгэ» гэсэн утгатай.
Үүссэн огнооноос `getFullYear()` зэрэг методоор хэсгийг нь авна:

```javascript
const odoo = new Date(2026, 8, 12); // сар 0-ээс эхэлнэ!

console.log(odoo.getFullYear()); // 2026
console.log(odoo.getMonth());    // 8 — есдүгээр сар
console.log(odoo.getDate());     // 12
```

> `getMonth()` нь **0-ээс** эхэлдэг. Нэгдүгээр сар нь 0, арванхоёрдугаар
> сар нь 11. Энэ бол хамгийн олон алдаа үүсгэдэг зүйлсийн нэг.

Сарын өдрийн тооноос хэтэрсэн өдөр өгвөл `Date` дараагийн сар руу өөрөө
шилжүүлнэ — хоног нэмэхэд тохиромжтой:

```javascript
const shine = new Date(2026, 11, 30 + 5); // 12-р сарын 35 гэж байхгүй
console.log(shine.getFullYear(), shine.getMonth() + 1, shine.getDate()); // 2027 1 4
```

### Хэлбэржүүлсэн огноо

```javascript
function ogno(date) {
  const jil = date.getFullYear();
  const sar = String(date.getMonth() + 1).padStart(2, "0");
  const udur = String(date.getDate()).padStart(2, "0");
  return `${jil}-${sar}-${udur}`;
}
```
""",
            initial_code="""\
const ner = prompt();
const ognooMur = prompt(); // жишээ нь "2026-9-30"
const honog = Number(prompt());
const uneMur = prompt(); // зайгаар тусгаарласан үнүүд

// Огноог ЖЖЖЖ-СС-ӨӨ хэлбэрт оруулна — бэлэн
function helberjuuleh(date) {
  const jil = date.getFullYear();
  const sar = String(date.getMonth() + 1).padStart(2, "0");
  const udur = String(date.getDate()).padStart(2, "0");
  return `${jil}-${sar}-${udur}`;
}

// TODO: ognooMur-ийг "-"-ээр хувааж жил, сар, өдрийг тоо болго
// TODO: new Date(...)-ээр захиалсан өдөр ба honog хоногийн дараах хүргэлтийн
//       өдрийг үүсгэ (сар 0-ээс эхэлдгийг сана)

// TODO: uneMur-ийг хувааж тоо болгоод нийт ба дунджийг ол (дундаж — toFixed(2))

// TODO: баримтыг НЭГ олон мөрт template literal-аар бүтээж хэвлэ
console.log(`Захиалагч: ${ner}`);
""",
            exercise=ExerciseSpec(
                statement="""\
Захиалгын баримтыг **олон мөрт template literal**-аар бүтээж хэвлэ.

Баримтад захиалсан ба хүргэгдэх огноо орно. Хүргэлт захиалснаас хойш
өгөгдсөн хоногийн дараа ирнэ — огноог `new Date(жил, сар, өдөр)`-ээр
үүсгэвэл сар, жилийн шилжилтийг (өндөр жилийн 2-р сар ч) `Date` өөрөө
бодно. Огноог `ЖЖЖЖ-СС-ӨӨ` хэлбэрээр, сар ба өдрийг 2 оронтой бич
(`helberjuuleh` функц эхлэл кодод бэлэн). Дундаж үнийг `toFixed(2)`-оор
2 орон хүртэл тоймло.

**Оролт:** дөрвөн мөр:

1. захиалагчийн нэр;
2. захиалсан огноо `жил-сар-өдөр` хэлбэрээр — сар, өдөр нь 1 оронтой байж
   болно (`2026-9-5`);
3. хүргэлтийн хоног (0 ба түүнээс их бүхэл тоо);
4. барааны үнүүд — нэг зайгаар тусгаарласан бүхэл тоонууд.

**Гаралт:** яг зургаан мөр:

```text
Захиалагч: <нэр>
Захиалсан: <ЖЖЖЖ-СС-ӨӨ>
Хүргэгдэх: <ЖЖЖЖ-СС-ӨӨ>
Барааны тоо: <үнийн тоо>
Нийт: <үнийн нийлбэр>
Дундаж: <нийт / тоо, 2 орны нарийвчлалтай>
```
""",
                tests=(
                    TestCaseSpec(
                        stdin="Бат\n2026-09-30\n3\n4500 3000 6000\n",
                        expected_output=(
                            "Захиалагч: Бат\n"
                            "Захиалсан: 2026-09-30\n"
                            "Хүргэгдэх: 2026-10-03\n"
                            "Барааны тоо: 3\n"
                            "Нийт: 13500\n"
                            "Дундаж: 4500.00\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="Сараа\n2026-12-30\n5\n1000 2000\n",
                        expected_output=(
                            "Захиалагч: Сараа\n"
                            "Захиалсан: 2026-12-30\n"
                            "Хүргэгдэх: 2027-01-04\n"
                            "Барааны тоо: 2\n"
                            "Нийт: 3000\n"
                            "Дундаж: 1500.00\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="Дорж\n2028-2-27\n2\n999 1000 1000\n",
                        expected_output=(
                            "Захиалагч: Дорж\n"
                            "Захиалсан: 2028-02-27\n"
                            "Хүргэгдэх: 2028-02-29\n"
                            "Барааны тоо: 3\n"
                            "Нийт: 2999\n"
                            "Дундаж: 999.67\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="Туяа\n2027-2-28\n1\n5\n",
                        expected_output=(
                            "Захиалагч: Туяа\n"
                            "Захиалсан: 2027-02-28\n"
                            "Хүргэгдэх: 2027-03-01\n"
                            "Барааны тоо: 1\n"
                            "Нийт: 5\n"
                            "Дундаж: 5.00\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="Болд\n2026-1-5\n0\n100 200 300 400\n",
                        expected_output=(
                            "Захиалагч: Болд\n"
                            "Захиалсан: 2026-01-05\n"
                            "Хүргэгдэх: 2026-01-05\n"
                            "Барааны тоо: 4\n"
                            "Нийт: 1000\n"
                            "Дундаж: 250.00\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="Анар\n2026-9-1\n30\n1 2\n",
                        expected_output=(
                            "Захиалагч: Анар\n"
                            "Захиалсан: 2026-09-01\n"
                            "Хүргэгдэх: 2026-10-01\n"
                            "Барааны тоо: 2\n"
                            "Нийт: 3\n"
                            "Дундаж: 1.50\n"
                        ),
                    ),
                ),
                solution="""\
const ner = prompt();
const ognooMur = prompt();
const honog = Number(prompt());
const uneMur = prompt();

function helberjuuleh(date) {
  const jil = date.getFullYear();
  const sar = String(date.getMonth() + 1).padStart(2, "0");
  const udur = String(date.getDate()).padStart(2, "0");
  return `${jil}-${sar}-${udur}`;
}

const [jil, sar, udur] = ognooMur.split("-").map(Number);
const zahialsan = new Date(jil, sar - 1, udur);
// Илүү гарсан өдрийг Date дараагийн сар руу өөрөө шилжүүлнэ
const hurgelt = new Date(jil, sar - 1, udur + honog);

const uneud = uneMur.split(" ").map(Number);
const niit = uneud.reduce((dun, une) => dun + une, 0);
const dundaj = niit / uneud.length;

const barimt = `Захиалагч: ${ner}
Захиалсан: ${helberjuuleh(zahialsan)}
Хүргэгдэх: ${helberjuuleh(hurgelt)}
Барааны тоо: ${uneud.length}
Нийт: ${niit}
Дундаж: ${dundaj.toFixed(2)}`;

console.log(barimt);
""",
                tips="""\
- Олон мөрт template literal: backtick дотор Enter дарж шинэ мөр эхлүүлнэ —
  `\\n` бичих шаардлагагүй. Мөрийн эхэнд догол (зай) бүү тавь — тэр нь
  гаралтад орно.
- `"2026-9-5".split("-")` нь **текстийн** массив — `map(Number)`-ээр тоо
  болго. Задлах (`const [jil, sar, udur] = …`) тохиромжтой.
- `new Date(jil, sar - 1, udur)` — сар 0-ээс эхэлнэ. Хүргэлтийн огноонд
  өдөр дээр хоногоо нэм: `Date` илүү гарсан өдрийг дараагийн сар руу
  шилжүүлнэ.
- `toFixed(2)` нь мөр буцаана: `4500` → `"4500.00"`, `999.666…` → `"999.67"`.
""",
            ),
        ),
    ],
)

FUNCTION_DATA_MODULES = [FUNCTIONS, ARRAYS, OBJECTS, STRINGS]
