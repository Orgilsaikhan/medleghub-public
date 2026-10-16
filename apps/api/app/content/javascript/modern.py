"""Модул 15-17 — Орчин үеийн синтакс, хамрах хүрээ, алдаа боловсруулах.

Анхан шатнаас дунд шат руу шилжих гүүр. Эндээс эхлээд кодыг зөвхөн
"ажиллуулах" биш "найдвартай ажиллуулах" тухай ярина.
"""

from app.content.types import ExerciseSpec, LessonSpec, ModuleSpec, TestCaseSpec

MODERN = ModuleSpec(
    title="Модул 15 — Орчин үеийн JavaScript",
    description="ES6-аас хойшхи бичлэгүүд, өдөр тутам хэрэглэгддэг.",
    lessons=[
        LessonSpec(
            title="Задлах, тараах, цуглуулах",
            slug="destructuring-ba-rest",
            description="Destructuring, spread, rest-ийг гүнзгийрүүлэх.",
            duration=480,
            content="""\
Модул 7-д үзсэн задлалт, тараалтыг гүнзгийрүүлье.

### Үүрлэсэн задлалт

```javascript
const hereglegch = {
  ner: "Бат",
  hayag: { hot: "Улаанбаатар", duureg: "Баянзүрх" },
};

const { hayag: { hot } } = hereglegch;
console.log(hot); // "Улаанбаатар"
```

Гүн үүрлэвэл уншихад хэцүү болдог тул хоёр давхраас цааш бүү ор.

### Солих

Түр хувьсагчгүйгээр:

```javascript
let a = 1;
let b = 2;

[a, b] = [b, a];
```

### Rest — үлдсэнийг цуглуулах

`...` нь **зүүн талд** байвал эсрэг үүрэг гүйцэтгэнэ:

```javascript
const [negdugeer, ...uldsen] = [1, 2, 3, 4];
console.log(uldsen); // [2, 3, 4]

const { ner, ...busad } = hereglegch;
console.log(busad); // ner-ээс бусад бүх талбар
```

Талбар хасах хамгийн цэвэрхэн арга нь энэ:

```javascript
const { nuutsUg, ...aydgui } = hereglegch;
```

### Rest параметр

Тодорхойгүй тооны аргумент хүлээн авна:

```javascript
function niilber(...toonuud) {
  return toonuud.reduce((dun, t) => dun + t, 0);
}

console.log(niilber(1, 2, 3, 4)); // 10
```

### Spread — задлан тараах

```javascript
const toonuud = [5, 1, 9];

console.log(Math.max(...toonuud)); // 9 — массивыг аргумент болгож задлана
```

### Rest уу, spread уу

Ижил `...` тэмдэг хоёр өөр үүрэгтэй:

| Байрлал | Нэр | Үйлдэл |
|---|---|---|
| Зүүн тал, параметр | rest | **Цуглуулна** |
| Баруун тал, дуудалт | spread | **Тараана** |
""",
            initial_code="""\
// Rest параметр: хэдэн ч аргумент ирсэн нэг массив болгон цуглуулна.
function niilber(...toonuud) {
  // TODO: toonuud-ийн нийлбэрийг буцаа
  return 0;
}

// Оролт (бүү өөрчил): 1-р мөр — хэрэглэгчийн JSON, 2-р мөр — оноонууд
const hereglegch = JSON.parse(prompt());
const onoonuud = (prompt() || "").split(" ").map(Number);

// TODO: үүрлэсэн задлалтаар ner, hot, duureg-ийг аваад мэндчил
//   "Сайн уу, <ner>! (<hot>, <duureg>)"

// TODO: rest-ээр nuutsUg-ээс бусад талбарыг цуглуулж JSON-оор хэвлэ
//   "Аюулгүй: <JSON>"

// TODO: [эхнийх, ...бусад] — "Эхний оноо: …", "Бусад оноо: …"

// TODO: оноонуудыг spread-ээр тарааж "Хамгийн их: …", "Нийлбэр: …"
""",
            exercise=ExerciseSpec(
                statement="""\
Хэрэглэгчийн мэдээлэл ба оноонуудыг задлалт, rest, spread ашиглан
боловсруул.

**Оролт:** хоёр мөр:

1. Хэрэглэгчийн JSON объект: `ner`, `nuutsUg`, `hayag` (`hot`, `duureg`
   талбартай объект), мөн өөр талбарууд байж болно.
2. Зайгаар тусгаарласан бүхэл тоонууд (оноо), дор хаяж нэг.

**Гаралт:** яг зургаан мөр:

```text
Сайн уу, <ner>! (<hot>, <duureg>)
Аюулгүй: <nuutsUg-гүй объектын JSON.stringify>
Эхний оноо: <эхний тоо>
Бусад оноо: <бусад тоонууд ", "-ээр тусгаарласан>
Хамгийн их: <хамгийн их оноо>
Нийлбэр: <бүх онооны нийлбэр>
```

- «Аюулгүй» объект нь `nuutsUg`-ээс бусад **бүх** талбарыг анхны
  дарааллаар нь агуулна.
- Эхнийхээс өөр оноо байхгүй бол `Бусад оноо: байхгүй`.
- `niilber` функцийг rest параметртэйгээр гүйцээж, оноонуудыг түүнд болон
  `Math.max`-д spread-ээр тарааж өг.
""",
                tests=(
                    TestCaseSpec(
                        stdin=(
                            '{"ner":"Бат","nuutsUg":"nuuts123",'
                            '"hayag":{"hot":"Улаанбаатар","duureg":"Баянзүрх"}}\n75 92 58\n'
                        ),
                        expected_output=(
                            "Сайн уу, Бат! (Улаанбаатар, Баянзүрх)\n"
                            'Аюулгүй: {"ner":"Бат","hayag":{"hot":"Улаанбаатар","duureg":"Баянзүрх"}}\n'
                            "Эхний оноо: 75\n"
                            "Бусад оноо: 92, 58\n"
                            "Хамгийн их: 92\n"
                            "Нийлбэр: 225\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin=(
                            '{"id":7,"ner":"Сараа","nuutsUg":"s@raa",'
                            '"hayag":{"hot":"Дархан","duureg":"4-р баг"},"nas":19}\n100\n'
                        ),
                        expected_output=(
                            "Сайн уу, Сараа! (Дархан, 4-р баг)\n"
                            'Аюулгүй: {"id":7,"ner":"Сараа","hayag":{"hot":"Дархан","duureg":"4-р баг"},"nas":19}\n'
                            "Эхний оноо: 100\n"
                            "Бусад оноо: байхгүй\n"
                            "Хамгийн их: 100\n"
                            "Нийлбэр: 100\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin=(
                            '{"nuutsUg":"12345678","ner":"Дорж",'
                            '"hayag":{"hot":"Эрдэнэт","duureg":"Баян-Өндөр"},"email":"dorj@mail.mn"}\n'
                            "-5 -2 -9 0\n"
                        ),
                        expected_output=(
                            "Сайн уу, Дорж! (Эрдэнэт, Баян-Өндөр)\n"
                            'Аюулгүй: {"ner":"Дорж","hayag":{"hot":"Эрдэнэт","duureg":"Баян-Өндөр"},'
                            '"email":"dorj@mail.mn"}\n'
                            "Эхний оноо: -5\n"
                            "Бусад оноо: -2, -9, 0\n"
                            "Хамгийн их: 0\n"
                            "Нийлбэр: -16\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin=(
                            '{"ner":"Туяа","hayag":{"duureg":"Сүхбаатар","hot":"Улаанбаатар"},'
                            '"nuutsUg":"t"}\n10 20 30 40 50 60\n'
                        ),
                        expected_output=(
                            "Сайн уу, Туяа! (Улаанбаатар, Сүхбаатар)\n"
                            'Аюулгүй: {"ner":"Туяа","hayag":{"duureg":"Сүхбаатар","hot":"Улаанбаатар"}}\n'
                            "Эхний оноо: 10\n"
                            "Бусад оноо: 20, 30, 40, 50, 60\n"
                            "Хамгийн их: 60\n"
                            "Нийлбэр: 210\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin=(
                            '{"ner":"Ганаа","hayag":{"hot":"Мөрөн","duureg":"1-р баг"},'
                            '"nuutsUg":"g2026"}\n88 88\n'
                        ),
                        expected_output=(
                            "Сайн уу, Ганаа! (Мөрөн, 1-р баг)\n"
                            'Аюулгүй: {"ner":"Ганаа","hayag":{"hot":"Мөрөн","duureg":"1-р баг"}}\n'
                            "Эхний оноо: 88\n"
                            "Бусад оноо: 88\n"
                            "Хамгийн их: 88\n"
                            "Нийлбэр: 176\n"
                        ),
                    ),
                ),
                solution="""\
// Rest параметр: хэдэн ч аргумент ирсэн нэг массив болгон цуглуулна.
function niilber(...toonuud) {
  return toonuud.reduce((dun, t) => dun + t, 0);
}

// Оролт (бүү өөрчил): 1-р мөр — хэрэглэгчийн JSON, 2-р мөр — оноонууд
const hereglegch = JSON.parse(prompt());
const onoonuud = (prompt() || "").split(" ").map(Number);

// Үүрлэсэн задлалт — hayag гэсэн хувьсагч үүсэхгүй, зөвхөн hot, duureg
const {
  ner,
  hayag: { hot, duureg },
} = hereglegch;
console.log(`Сайн уу, ${ner}! (${hot}, ${duureg})`);

// Rest — nuutsUg-ээс бусад бүх талбар aydgui-д цугларна
const { nuutsUg, ...aydgui } = hereglegch;
console.log(`Аюулгүй: ${JSON.stringify(aydgui)}`);

// Массивын задлалт + rest — busad нь үргэлж массив (хоосон ч байж болно)
const [ehnii, ...busad] = onoonuud;
console.log(`Эхний оноо: ${ehnii}`);
console.log(`Бусад оноо: ${busad.length > 0 ? busad.join(", ") : "байхгүй"}`);

// Spread — массивыг тусдаа аргументууд болгож тараана
console.log(`Хамгийн их: ${Math.max(...onoonuud)}`);
console.log(`Нийлбэр: ${niilber(...onoonuud)}`);
""",
                tips="""\
- Үүрлэсэн задлалт хичээлийн `const { hayag: { hot } } = ...` жишээтэй
  адил — `ner`, `duureg`-ийг ч мөн нэг задлалтад нэм.
- Талбар хасах хамгийн цэвэрхэн арга нь rest: хасах талбараа нэрлээд,
  үлдсэнийг `...`-ээр шинэ объектод цуглуул. Анхны объект өөрчлөгдөхгүй.
- `[ehnii, ...busad]` — `busad` нь үргэлж массив. Оноо ганц бол хоосон
  (`busad.length === 0`).
- `Math.max(onoonuud)` нь `NaN` — массивыг `...`-ээр тусдаа аргумент болгож
  тараа. `niilber`-ийг ч мөн адил дууд.
- Оноо сөрөг ч байж болно — хамгийн ихийг 0-ээс эхэлж хайвал буруу гарна.
""",
            ),
        ),
        LessonSpec(
            title="Анхдагч утга, ?. ба ??",
            slug="anhdagch-parametr-ba-optional-chaining",
            description="Default parameter, optional chaining, nullish coalescing.",
            duration=450,
            content="""\
### Анхдагч параметр

```javascript
function mendchileh(ner = "зочин", temdeg = "!") {
  return `Сайн уу, ${ner}${temdeg}`;
}

console.log(mendchileh());          // "Сайн уу, зочин!"
console.log(mendchileh("Бат"));     // "Сайн уу, Бат!"
console.log(mendchileh(undefined, "?")); // хоёр дахийг л өгөх
```

Анхдагч утга нь зөвхөн аргумент `undefined` үед ажиллана. `null` өгвөл
ажиллахгүй.

### Заавал бус хандалт — `?.`

Байхгүй объект дотор орох гэвэл програм унана:

```javascript
const hereglegch = { ner: "Бат" };

console.log(hereglegch.hayag.hot);  // TypeError — програм зогсоно
console.log(hereglegch.hayag?.hot); // undefined — аюулгүй
```

`?.` нь зүүн тал нь `null` эсвэл `undefined` бол шалгалтыг зогсоож
`undefined` буцаана.

Метод болон массивд ч ажиллана:

```javascript
hereglegch.mendchileh?.();  // метод байхгүй бол дуудахгүй
jagsaalt?.[0];              // массив байхгүй бол алдаа заахгүй
```

### Хоосон нөхөх — `??`

`||`-ээс ялгаатай нь зөвхөн `null` ба `undefined`-ийг л орлуулна:

```javascript
const shirheg = 0;

console.log(shirheg || 10); // 10 — 0 нь falsy тул орлуулав
console.log(shirheg ?? 10); // 0  — 0 нь бодит утга тул үлдээв
```

| Утга | ЭСВЭЛ оператор | `??` оператор |
|---|---|---|
| `0` | Орлуулна | Үлдээнэ |
| `""` | Орлуулна | Үлдээнэ |
| `false` | Орлуулна | Үлдээнэ |
| `null` | Орлуулна | Орлуулна |
| `undefined` | Орлуулна | Орлуулна |

Тоо болон boolean-той ажиллаж байвал `??` сонго.

### Хамтад нь

```javascript
const hot = hereglegch.hayag?.hot ?? "тодорхойгүй";
```

Энэ нэг мөр нь урьд нь хэдэн мөр `if` шаарддаг байсан.
""",
            initial_code="""\
// TODO: ner өгөгдөөгүй (undefined) үед "зочин" болгох анхдагч параметр нэм
function neriinMur(ner) {
  return ner;
}

let niit = 0;
let mur = prompt();
while (mur !== null) {
  const h = JSON.parse(mur);

  // TODO: hayag байхгүй, null ч бай програм унахгүйгээр hot-ыг ав;
  //       байхгүй бол "тодорхойгүй"
  const hot = "тодорхойгүй";

  // TODO: захиалга — 0 бол 0 хэвээр, null/байхгүй бол "мэдээлэлгүй"
  const zahialga = "мэдээлэлгүй";

  // TODO: утас — utas массивын эхний элемент, байхгүй бол "байхгүй"
  const utas = "байхгүй";

  console.log(`${neriinMur(h.ner)} | ${hot} | захиалга: ${zahialga} | утас: ${utas}`);

  // TODO: niit-д захиалгын тоог нэм (байхгүй бол 0)

  mur = prompt();
}

console.log(`Нийт захиалга: ${niit}`);
""",
            exercise=ExerciseSpec(
                statement="""\
Хэрэглэгчдийн жагсаалтыг хэвлэ. Өгөгдөл дутуу ирнэ — зарим талбар байхгүй,
`null` эсвэл `0` байж болно. Програм унахгүй, `0`-ийг алдахгүй байх ёстой.

**Оролт:** мөр бүрт нэг хэрэглэгчийн JSON объект, оролт дуустал. Доорх
талбар бүр байхгүй байж болно:

- `ner` — нэр (байвал текст);
- `hayag` — объект эсвэл `null`; дотор нь `hot` байж болно;
- `zahialga` — захиалгын тоо эсвэл `null`;
- `utas` — утасны дугааруудын массив (хоосон ч байж болно) эсвэл `null`.

**Гаралт:** хэрэглэгч бүрт нэг мөр, төгсгөлд нийлбэр:

```text
<нэр> | <хот> | захиалга: <захиалга> | утас: <эхний утас>
Нийт захиалга: <захиалгын нийлбэр>
```

Утга дутуу бол: нэр — `зочин`, хот — `тодорхойгүй`, захиалга —
`мэдээлэлгүй`, утас — `байхгүй`. `0` захиалга бол `0` хэвээр үлдэнэ.
Нийлбэрт захиалгагүйг `0` гэж тооцно. Нэрийг `neriinMur` функцийн
**анхдагч параметрээр** шийд.
""",
                tests=(
                    TestCaseSpec(
                        stdin=(
                            '{"ner":"Бат","hayag":{"hot":"Улаанбаатар"},"zahialga":0,'
                            '"utas":["99112233","88001122"]}\n'
                            '{"ner":"Сараа"}\n'
                            '{"ner":"Дорж","hayag":{"hot":"Дархан"},"zahialga":5,"utas":[]}\n'
                        ),
                        expected_output=(
                            "Бат | Улаанбаатар | захиалга: 0 | утас: 99112233\n"
                            "Сараа | тодорхойгүй | захиалга: мэдээлэлгүй | утас: байхгүй\n"
                            "Дорж | Дархан | захиалга: 5 | утас: байхгүй\n"
                            "Нийт захиалга: 5\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="{}\n",
                        expected_output=(
                            "зочин | тодорхойгүй | захиалга: мэдээлэлгүй | утас: байхгүй\n"
                            "Нийт захиалга: 0\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin=(
                            '{"ner":"Болд","hayag":null,"zahialga":null}\n'
                            '{"hayag":{},"zahialga":3,"utas":["70112233"]}\n'
                            '{"ner":"Туяа","hayag":{"hot":"Эрдэнэт"},"zahialga":12}\n'
                        ),
                        expected_output=(
                            "Болд | тодорхойгүй | захиалга: мэдээлэлгүй | утас: байхгүй\n"
                            "зочин | тодорхойгүй | захиалга: 3 | утас: 70112233\n"
                            "Туяа | Эрдэнэт | захиалга: 12 | утас: байхгүй\n"
                            "Нийт захиалга: 15\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin=(
                            '{"ner":"Номин","utas":null,"zahialga":7}\n'
                            '{"ner":"Ганаа","hayag":{"hot":"Мөрөн","gudamj":"1-р"},'
                            '"utas":["95001122"]}\n'
                        ),
                        expected_output=(
                            "Номин | тодорхойгүй | захиалга: 7 | утас: байхгүй\n"
                            "Ганаа | Мөрөн | захиалга: мэдээлэлгүй | утас: 95001122\n"
                            "Нийт захиалга: 7\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin=(
                            '{"ner":"Анар","zahialga":0}\n'
                            '{"ner":"Цэцэг","zahialga":0,"hayag":{"hot":"Ховд"}}\n'
                        ),
                        expected_output=(
                            "Анар | тодорхойгүй | захиалга: 0 | утас: байхгүй\n"
                            "Цэцэг | Ховд | захиалга: 0 | утас: байхгүй\n"
                            "Нийт захиалга: 0\n"
                        ),
                    ),
                ),
                solution="""\
// Анхдагч параметр — ner өгөгдөөгүй (undefined) үед "зочин" болно.
function neriinMur(ner = "зочин") {
  return ner;
}

let niit = 0;
let mur = prompt();
while (mur !== null) {
  const h = JSON.parse(mur);

  // ?. — hayag нь null эсвэл undefined бол цааш орохгүй, undefined өгнө
  const hot = h.hayag?.hot ?? "тодорхойгүй";

  // ?? — зөвхөн null/undefined-ийг орлуулна, 0 хэвээр үлдэнэ
  const zahialga = h.zahialga ?? "мэдээлэлгүй";

  // ?.[0] — массив байхгүй бол алдаа заахгүй; хоосон массивт undefined
  const utas = h.utas?.[0] ?? "байхгүй";

  console.log(`${neriinMur(h.ner)} | ${hot} | захиалга: ${zahialga} | утас: ${utas}`);

  niit += h.zahialga ?? 0;

  mur = prompt();
}

console.log(`Нийт захиалга: ${niit}`);
""",
                tips="""\
- `h.hayag.hot` нь `hayag` байхгүй (эсвэл `null`) үед TypeError өгнө.
  `?.` нь зүүн тал нь `null`/`undefined` бол зогсоод `undefined` буцаана.
- Массивын элементэд ч ажиллана: `?.[0]`. Хоосон массивын `[0]` нь
  `undefined`.
- `||` нь `0`-ийг ч орлуулна — захиалгад `??` хэрэглэ.
- Анхдагч параметр зөвхөн аргумент `undefined` үед ажиллана. `ner`
  талбаргүй объектын `h.ner` яг `undefined` байдаг.
- Нийлбэрт нэмэхдээ ч `??` хэрэгтэй — `null`-ыг нэмбэл `0` болж хувирах ч,
  `undefined` нэмбэл `NaN` болно.
""",
            ),
        ),
    ],
)

SCOPE = ModuleSpec(
    title="Модул 16 — Хамрах хүрээ ба closure",
    description="Хувьсагч хаанаас харагдах вэ.",
    lessons=[
        LessonSpec(
            title="Хамрах хүрээ (Scope)",
            slug="hamrah-huree",
            description="Global, функц, блокийн хүрээ.",
            duration=450,
            content="""\
**Хамрах хүрээ** гэдэг нь хувьсагч хаанаас харагдахыг тодорхойлно.

### Гурван түвшин

```javascript
const global = "хаанаас ч харагдана";

function funkts() {
  const funktsiin = "зөвхөн энэ функц дотор";

  if (true) {
    const blokiin = "зөвхөн энэ хаалт дотор";
    console.log(global, funktsiin, blokiin); // гурвуулаа харагдана
  }

  console.log(blokiin); // ReferenceError
}
```

### Гадагшаа хардаг, дотогшоо хардаггүй

Дотоод хүрээ нь гаднахыг **харна**. Гадаад хүрээ нь дотоодыг **харахгүй**.

```text
global
└── функцийн хүрээ      ← global-ыг харна
    └── блокийн хүрээ   ← хоёуланг нь харна
```

### `let` ба `var`-ийн ялгаа

Энэ нь `var`-аас зайлсхийх гол шалтгаан:

```javascript
if (true) {
  var a = 1;   // блокоос ЗУГТАНА
  let b = 2;   // блок дотроо үлдэнэ
}

console.log(a); // 1
console.log(b); // ReferenceError
```

### Давталт дахь сонгодог алдаа

```javascript
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
// 3, 3, 3 — бүгд ижил i-г хуваалцана

for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
// 0, 1, 2 — давталт бүрт шинэ i
```

`let` нь давталт бүрт **шинэ** хувьсагч үүсгэдэг.

### Сүүдэрлэх (shadowing)

Дотоод хүрээнд ижил нэр өгвөл гаднахыг түр далдална:

```javascript
const ner = "гадна";

function tuhai() {
  const ner = "дотор";
  console.log(ner); // "дотор"
}
```

Ажиллах боловч уншихад төөрөгдөл үүсгэдэг — өөр нэр өгөх нь дээр.

### Global-ыг хэмнэ

Global хувьсагч олон байвал нэр давхардах, санамсаргүй өөрчлөгдөх эрсдэл
өснө. Хувьсагчаа **хамгийн жижиг** хүрээнд зарла.
""",
            initial_code="""\
// Товч бүрт "дарах" функц давталтаар үүсгэнэ.
// TODO: энэ кодод хамрах хүрээний ГУРВАН алдаа бий — олж зас.
const nernuud = (prompt() || "").split(" ");
const tovchnuud = [];
let niitDarsan = 0; // бүх товчийг нийт хэдэн удаа дарсан

for (var i = 0; i < nernuud.length; i++) {
  var too = 0; // энэ товчийг хэдэн удаа дарсан
  tovchnuud.push(() => {
    let niitDarsan = 0;
    too++;
    niitDarsan++;
    console.log(`${i + 1}-р товч: ${nernuud[i]} (${too} дахь удаа)`);
  });
}

// Мөр бүр — дарсан товчны дугаар (1-ээс эхэлнэ)
let mur = prompt();
while (mur !== null) {
  const dugaar = Number(mur);
  // TODO: ийм дугаартай товч байхгүй бол "Ийм товч алга: <мөр>" гэж хэвлэ
  tovchnuud[dugaar - 1]();
  mur = prompt();
}

console.log(`Нийт дарсан: ${niitDarsan}`);
""",
            exercise=ExerciseSpec(
                statement="""\
Эхлэл кодод товч бүрийн «дарах» функцийг давталтаар үүсгэдэг жижиг апп бий.
Гэвч **хамрах хүрээний гурван алдаа**-тай: одоогоор бүх товч ижил дугаар,
`undefined` нэр хэвлэж, тоолуурууд нь холилдож, нийт тоо үргэлж `0` гарна.
Алдаануудыг засаад, буруу дугаарыг шалгадаг болго.

**Оролт:** эхний мөрөнд зайгаар тусгаарласан товчны нэрс. Дараагийн мөр бүр
дарсан товчны дугаар (1-ээс эхэлнэ).

**Гаралт:** товч дарах бүрд:

```text
<дугаар>-р товч: <нэр> (<энэ товчийг хэд дэх удаагаа дарсан> дахь удаа)
```

- Товч бүр **өөрийн** тоолууртай: өөр товч дарах нь түүнд нөлөөлөхгүй.
- Дугаар нь 1-ээс товчны тоо хүртэлх завсарт биш (эсвэл тоо биш) бол
  `Ийм товч алга: <мөр>` — ийм даралтыг тоолохгүй.
- Төгсгөлд `Нийт дарсан: <бүх товчийг нийт дарсан тоо>`.
""",
                tests=(
                    TestCaseSpec(
                        stdin="Нүүр Сургалт Профайл\n2\n1\n2\n",
                        expected_output=(
                            "2-р товч: Сургалт (1 дахь удаа)\n"
                            "1-р товч: Нүүр (1 дахь удаа)\n"
                            "2-р товч: Сургалт (2 дахь удаа)\n"
                            "Нийт дарсан: 3\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="А Б\n3\n0\n1\n",
                        expected_output=(
                            "Ийм товч алга: 3\n"
                            "Ийм товч алга: 0\n"
                            "1-р товч: А (1 дахь удаа)\n"
                            "Нийт дарсан: 1\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="Ганц\n",
                        expected_output="Нийт дарсан: 0\n",
                    ),
                    TestCaseSpec(
                        stdin="X Y Z W\n4\n4\n4\n1\n",
                        expected_output=(
                            "4-р товч: W (1 дахь удаа)\n"
                            "4-р товч: W (2 дахь удаа)\n"
                            "4-р товч: W (3 дахь удаа)\n"
                            "1-р товч: X (1 дахь удаа)\n"
                            "Нийт дарсан: 4\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="Нэг Хоёр Гурав\n3\n2\n1\n3\n5\nabc\n",
                        expected_output=(
                            "3-р товч: Гурав (1 дахь удаа)\n"
                            "2-р товч: Хоёр (1 дахь удаа)\n"
                            "1-р товч: Нэг (1 дахь удаа)\n"
                            "3-р товч: Гурав (2 дахь удаа)\n"
                            "Ийм товч алга: 5\n"
                            "Ийм товч алга: abc\n"
                            "Нийт дарсан: 4\n"
                        ),
                    ),
                ),
                solution="""\
// Товч бүрт "дарах" функц давталтаар үүсгэнэ.
const nernuud = (prompt() || "").split(" ");
const tovchnuud = [];
let niitDarsan = 0; // бүх товчийг нийт хэдэн удаа дарсан

// let — давталт бүрт ШИНЭ i, ШИНЭ too: товч бүр өөрийнхөө утгыг санана
for (let i = 0; i < nernuud.length; i++) {
  let too = 0; // энэ товчийг хэдэн удаа дарсан
  tovchnuud.push(() => {
    too++;
    niitDarsan++; // гаднах хувьсагч — дотор нь дахин зарлавал сүүдэрлэнэ
    console.log(`${i + 1}-р товч: ${nernuud[i]} (${too} дахь удаа)`);
  });
}

// Мөр бүр — дарсан товчны дугаар (1-ээс эхэлнэ)
let mur = prompt();
while (mur !== null) {
  const dugaar = Number(mur);
  if (dugaar >= 1 && dugaar <= tovchnuud.length) {
    tovchnuud[dugaar - 1]();
  } else {
    console.log(`Ийм товч алга: ${mur}`);
  }
  mur = prompt();
}

console.log(`Нийт дарсан: ${niitDarsan}`);
""",
                tips="""\
- `var` нь блокоос зугтаж бүх програмд **ганц** хувьсагч болно. Давталт
  дотор үүсгэсэн функцүүд бүгд нэг `i`-г хуваалцана — дуудах үед давталт
  аль хэдийн дуусч, `i` нь сүүлийн утгатай болсон байна.
- `let` нь давталт бүрт **шинэ** хувьсагч үүсгэнэ. Давталтын биед зарласан
  тоолуурт ч мөн адил хамаарна.
- Функц дотор гаднах хувьсагчтай ижил нэртэй хувьсагч зарлавал гаднахыг
  **сүүдэрлэнэ** — гаднах `niitDarsan` огт өөрчлөгдөхгүй.
- `Number("abc")` нь `NaN`, `NaN >= 1` нь `false` — нэг нөхцөл тоо биш
  оролтыг ч барина.
""",
            ),
        ),
        LessonSpec(
            title="Closure",
            slug="closure",
            description="Функц төрсөн орчноо санадаг шинж.",
            duration=480,
            content="""\
**Closure** гэдэг нь функц өөрийг нь үүсгэсэн орчны хувьсагчдыг санаж
үлддэг шинж.

```javascript
function toolourUusgeh() {
  let toolol = 0;

  return function () {
    toolol++;
    return toolol;
  };
}

const toolooh = toolourUusgeh();

console.log(toolooh()); // 1
console.log(toolooh()); // 2
```

`toolourUusgeh` дуусч, түүний хүрээ алга болох ёстой мэт. Гэтэл дотоод
функц `toolol`-ыг **хадгалж** үлдэж байна. Энэ бол closure.

### Тусдаа санах ой

Дуудалт бүр **шинэ** орчин үүсгэнэ:

```javascript
const a = toolourUusgeh();
const b = toolourUusgeh();

a(); a();  // 1, 2
b();       // 1 — тусдаа тоолуур
```

### Хувийн өгөгдөл

Closure нь гаднаас хүрч болохгүй өгөгдөл үүсгэх сонгодог арга:

```javascript
function dansUusgeh(ehleliin) {
  let uldegdel = ehleliin;

  return {
    nemeh(dun) {
      uldegdel += dun;
      return uldegdel;
    },
    harah() {
      return uldegdel;
    },
  };
}

const dans = dansUusgeh(1000);
dans.nemeh(500);
console.log(dans.harah());   // 1500
console.log(dans.uldegdel);  // undefined — гаднаас хүрэхгүй
```

### Хаана таарах вэ

Closure-ийг мэдэлгүй ч өдөр бүр ашигладаг:

- Event listener нь гаднах хувьсагчаа санадаг
- `setTimeout`-д дамжуулсан функц
- `map`, `filter`-т дамжуулсан функц

### Санах ойн анхааруулга

Closure нь хувьсагчийг **амьд** байлгана. Том өгөгдлийг closure дотор
удаан барих нь санах ой үрэлгэн ашиглахад хүргэж болно.
""",
            initial_code="""\
function dansUusgeh(ehleliin) {
  // TODO: үлдэгдэл ба амжилттай гүйлгээний тоог энд хадгал —
  //       гаднаас харагдахгүй, зөвхөн доорх методууд л хүрнэ

  return {
    nemeh(dun) {
      // TODO: үлдэгдэлд нэмж, гүйлгээг тоолоод шинэ үлдэгдлийг буцаа
      return 0;
    },
    hasah(dun) {
      // TODO: хүрэлцэхгүй бол юу ч өөрчлөхгүй null буцаа;
      //       эс бөгөөс хасаж, гүйлгээг тоолоод шинэ үлдэгдлийг буцаа
      return null;
    },
    harah() {
      return 0; // TODO: одоогийн үлдэгдэл
    },
    guilgeeToo() {
      return 0; // TODO: амжилттай гүйлгээний тоо
    },
  };
}

// --- Доорх хэсэг бэлэн (бүү өөрчил) ----------------------------------------
const [ehnii1, ehnii2] = (prompt() || "0 0").split(" ").map(Number);
const dansuud = [dansUusgeh(ehnii1), dansUusgeh(ehnii2)];

let mur = prompt();
while (mur !== null) {
  const [dugaar, uildel, dunText] = mur.split(" ");
  const dans = dansuud[Number(dugaar) - 1];
  const dun = Number(dunText);

  if (uildel === "нэмэх") {
    console.log(`Данс ${dugaar}: +${dun} → ${dans.nemeh(dun)}`);
  } else if (uildel === "хасах") {
    const ur = dans.hasah(dun);
    if (ur === null) {
      console.log(`Данс ${dugaar}: хүрэлцэхгүй (${dans.harah()})`);
    } else {
      console.log(`Данс ${dugaar}: -${dun} → ${ur}`);
    }
  } else {
    console.log(`Данс ${dugaar}: ${dans.harah()}`);
  }

  mur = prompt();
}

dansuud.forEach((dans, i) => {
  console.log(`Данс ${i + 1}: ${dans.harah()} (${dans.guilgeeToo()} гүйлгээ)`);
});
console.log("Гаднаас:", dansuud[0].uldegdel);
""",
            exercise=ExerciseSpec(
                statement="""\
Closure ашиглан хоёр банкны данс хий. `dansUusgeh` дуудалт бүрт **тусдаа**
үлдэгдэл, гүйлгээний тоотой данс буцаана. Үлдэгдлийг гаднаас шууд уншиж,
өөрчлөх боломжгүй — зөвхөн методуудаар.

Тушаал уншиж хэвлэдэг хэсэг эхлэл кодод бэлэн. Чи `dansUusgeh`-ийн
методуудыг гүйцээнэ:

| Метод | Үйлдэл |
|---|---|
| `nemeh(dun)` | Үлдэгдэлд нэмж, шинэ үлдэгдлийг буцаана. |
| `hasah(dun)` | Үлдэгдэл хүрэлцэхгүй бол юу ч өөрчлөхгүй `null` буцаана; эс бөгөөс хасаж, шинэ үлдэгдлийг буцаана. |
| `harah()` | Одоогийн үлдэгдэл. |
| `guilgeeToo()` | Амжилттай `nemeh`, `hasah`-ын тоо (`nemeh(0)` ч тоологдоно). |

**Оролт:** эхний мөрөнд хоёр дансны эхний үлдэгдэл, зайгаар. Дараагийн мөр
бүр: `<данс> нэмэх <дүн>`, `<данс> хасах <дүн>` эсвэл `<данс> харах`
(`<данс>` нь `1` эсвэл `2`).

**Гаралт** (хэвлэх код бэлэн):

```text
Данс <n>: +<дүн> → <үлдэгдэл>
Данс <n>: -<дүн> → <үлдэгдэл>
Данс <n>: хүрэлцэхгүй (<үлдэгдэл>)
Данс <n>: <үлдэгдэл>
…
Данс 1: <үлдэгдэл> (<гүйлгээ> гүйлгээ)
Данс 2: <үлдэгдэл> (<гүйлгээ> гүйлгээ)
Гаднаас: undefined
```

Эхний дөрвөн мөр нь `нэмэх`, амжилттай `хасах`, хүрэлцээгүй `хасах`, `харах`
тушаалынх. Сүүлийн мөр нь `dans.uldegdel` гэж гаднаас хандахад юу ч
олдохгүйг харуулна.
""",
                tests=(
                    TestCaseSpec(
                        stdin="1000 200\n1 нэмэх 500\n2 хасах 50\n1 хасах 2000\n2 харах\n",
                        expected_output=(
                            "Данс 1: +500 → 1500\n"
                            "Данс 2: -50 → 150\n"
                            "Данс 1: хүрэлцэхгүй (1500)\n"
                            "Данс 2: 150\n"
                            "Данс 1: 1500 (1 гүйлгээ)\n"
                            "Данс 2: 150 (1 гүйлгээ)\n"
                            "Гаднаас: undefined\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="100 100\n1 хасах 100\n2 нэмэх 0\n1 харах\n",
                        expected_output=(
                            "Данс 1: -100 → 0\n"
                            "Данс 2: +0 → 100\n"
                            "Данс 1: 0\n"
                            "Данс 1: 0 (1 гүйлгээ)\n"
                            "Данс 2: 100 (1 гүйлгээ)\n"
                            "Гаднаас: undefined\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="5 7\n",
                        expected_output=(
                            "Данс 1: 5 (0 гүйлгээ)\nДанс 2: 7 (0 гүйлгээ)\nГаднаас: undefined\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="0 50\n2 нэмэх 25\n2 хасах 80\n2 хасах 75\n2 харах\n1 хасах 1\n",
                        expected_output=(
                            "Данс 2: +25 → 75\n"
                            "Данс 2: хүрэлцэхгүй (75)\n"
                            "Данс 2: -75 → 0\n"
                            "Данс 2: 0\n"
                            "Данс 1: хүрэлцэхгүй (0)\n"
                            "Данс 1: 0 (0 гүйлгээ)\n"
                            "Данс 2: 0 (2 гүйлгээ)\n"
                            "Гаднаас: undefined\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin=(
                            "300 300\n1 хасах 100\n1 хасах 100\n1 хасах 100\n1 хасах 100\n"
                            "2 нэмэх 1000\n"
                        ),
                        expected_output=(
                            "Данс 1: -100 → 200\n"
                            "Данс 1: -100 → 100\n"
                            "Данс 1: -100 → 0\n"
                            "Данс 1: хүрэлцэхгүй (0)\n"
                            "Данс 2: +1000 → 1300\n"
                            "Данс 1: 0 (3 гүйлгээ)\n"
                            "Данс 2: 1300 (1 гүйлгээ)\n"
                            "Гаднаас: undefined\n"
                        ),
                    ),
                ),
                solution="""\
function dansUusgeh(ehleliin) {
  // Зөвхөн доорх методууд л эдгээрийг хардаг — closure
  let uldegdel = ehleliin;
  let guilgee = 0;

  return {
    nemeh(dun) {
      uldegdel += dun;
      guilgee++;
      return uldegdel;
    },
    hasah(dun) {
      if (dun > uldegdel) {
        return null;
      }
      uldegdel -= dun;
      guilgee++;
      return uldegdel;
    },
    harah() {
      return uldegdel;
    },
    guilgeeToo() {
      return guilgee;
    },
  };
}

// --- Доорх хэсэг бэлэн (бүү өөрчил) ----------------------------------------
const [ehnii1, ehnii2] = (prompt() || "0 0").split(" ").map(Number);
const dansuud = [dansUusgeh(ehnii1), dansUusgeh(ehnii2)];

let mur = prompt();
while (mur !== null) {
  const [dugaar, uildel, dunText] = mur.split(" ");
  const dans = dansuud[Number(dugaar) - 1];
  const dun = Number(dunText);

  if (uildel === "нэмэх") {
    console.log(`Данс ${dugaar}: +${dun} → ${dans.nemeh(dun)}`);
  } else if (uildel === "хасах") {
    const ur = dans.hasah(dun);
    if (ur === null) {
      console.log(`Данс ${dugaar}: хүрэлцэхгүй (${dans.harah()})`);
    } else {
      console.log(`Данс ${dugaar}: -${dun} → ${ur}`);
    }
  } else {
    console.log(`Данс ${dugaar}: ${dans.harah()}`);
  }

  mur = prompt();
}

dansuud.forEach((dans, i) => {
  console.log(`Данс ${i + 1}: ${dans.harah()} (${dans.guilgeeToo()} гүйлгээ)`);
});
console.log("Гаднаас:", dansuud[0].uldegdel);
""",
                tips="""\
- Үлдэгдэл, гүйлгээний тоог `dansUusgeh` **дотор** `let`-ээр зарла.
  Буцаах объектын талбар болговол гаднаас харагдаж, `Гаднаас:` мөр тоо
  хэвлэнэ.
- Методууд тэдгээрийг closure-оор санана. `dansUusgeh`-ийг хоёр удаа
  дуудахад хоёр **тусдаа** орчин үүснэ.
- Хувьсагчаа `dansUusgeh`-ээс гадна зарлавал хоёр данс нэг үлдэгдлийг
  хуваалцаж, бие биедээ нөлөөлнө.
- Хүрэлцэхгүй үед гүйлгээг бүү тоол. Бүх үлдэгдлээ хасах (`dun` нь
  үлдэгдэлтэй тэнцүү) нь зөвшөөрөгдөнө.
""",
            ),
        ),
    ],
)

ERRORS = ModuleSpec(
    title="Модул 17 — Алдаа боловсруулах",
    description="Алдаа гарахад програм унахгүй байх.",
    lessons=[
        LessonSpec(
            title="try, catch, finally",
            slug="try-catch-finally",
            description="Алдааг барьж авч зохицуулах.",
            duration=450,
            content="""\
Алдаа гарвал програм тэр дороо зогсоно. `try/catch` нь түүнийг барьж авна.

```javascript
try {
  const ugugdul = JSON.parse("{ эвдэрхий");
  console.log(ugugdul);
} catch (aldaa) {
  console.log("Алдаа гарлаа:", aldaa.message);
}

console.log("Програм үргэлжилж байна");
```

### `finally`

Алдаа гарсан эсэхээс **үл хамааран** ажиллана:

```javascript
try {
  ajil();
} catch (aldaa) {
  console.log("Амжилтгүй");
} finally {
  console.log("Энэ үргэлж ажиллана");
}
```

Ачаалж буй тэмдэглэгээг унтраах, файл хаах зэрэгт тохиромжтой.

### Алдааны объект

```javascript
catch (aldaa) {
  console.log(aldaa.name);    // "SyntaxError"
  console.log(aldaa.message); // тайлбар
  console.log(aldaa.stack);   // хаанаас гарсан
}
```

Аргумент хэрэггүй бол орхиж болно: `catch { ... }`

### Бүгдийг бүү ороо

```javascript
// Муу — алдааг нууж байна
try {
  ajil();
} catch {}
```

Чимээгүй барьж авсан алдаа нь дараа нь олоход хамгийн хэцүү. Дор хаяж
бүртгэ.

### Зөвхөн хүлээгдэж буйг ороо

`try` дотор аль болох цөөн мөр байлга:

```javascript
// Муу — алин нь унасныг мэдэхгүй
try {
  const a = unshih();
  const b = bodoh(a);
  hadgalah(b);
} catch { }

// Сайн — зөвхөн эрсдэлтэй хэсэг
let a;
try {
  a = unshih();
} catch {
  a = anhdagch;
}
```

### `try/catch` нь юуг барихгүй вэ

Асинхрон кодыг барихгүй (`throw`-ийг дараагийн хичээлд үзнэ — энд
«алдаа үүсгэнэ» гэж ойлгоход хангалттай):

```javascript
try {
  setTimeout(() => {
    throw new Error("энэ баригдахгүй");
  }, 100);
} catch {
  // хэзээ ч ажиллахгүй
}
```

Асинхрон алдааг Модул 18-д үзнэ.
""",
            initial_code="""\
let niitMur = 0;
let amjilttai = 0;
let niitOnoo = 0;

// TODO: try нь БҮХ давталтыг ороосон тул эхний алдаатай мөр дээр уншилт
//       бүхэлдээ зогсоно. Мөр бүрийн эрсдэлтэй хэсгийг л тусад нь барь:
//       алдаа гарвал "✗ <дугаар>-р мөр: <алдааны нэр>" гээд үргэлжлүүл,
//       мөрийг амжилттай эсэхээс үл хамааран finally дотор тоол.
try {
  let mur = prompt();
  while (mur !== null) {
    const ugugdul = JSON.parse(mur); // эвдэрхий JSON → SyntaxError
    const ner = ugugdul.ner.trim(); // ner байхгүй → TypeError
    console.log(`✓ ${ner}: ${ugugdul.onoo}`);
    amjilttai++;
    niitOnoo += ugugdul.onoo;
    niitMur++;
    mur = prompt();
  }
} catch (aldaa) {
  console.log("Алдаа гарлаа");
}

console.log(`Нийт ${niitMur} мөр: ${amjilttai} амжилттай, ${niitMur - amjilttai} алдаатай`);
// TODO: амжилттай мөр байвал "Дундаж оноо: <1 оронтой>",
//       эс бөгөөс "Дундаж оноо: байхгүй"
""",
            exercise=ExerciseSpec(
                statement="""\
Оноо бичсэн JSON мөрүүдийг уншина. Зарим мөр эвдэрхий, заримд нь нэр алга.
Алдаатай мөр програмыг зогсоох ёсгүй — барьж аваад дараагийн мөр рүү
үргэлжлүүл.

Эхлэл кодод `try` нь **бүх давталтыг** ороосон тул эхний алдаатай мөр дээр
уншилт бүхэлдээ зогсдог — хичээлийн «Бүгдийг бүү ороо» алдаа. Засаж, мөр
бүрийг тусад нь барь.

**Оролт:** мөр бүрт `{"ner":"…","onoo":<тоо>}` хэлбэрийн JSON, оролт
дуустал. Эвдэрхий JSON, эсвэл `ner` талбаргүй утга ч ирж болно.

**Мөр бүрийг:** `JSON.parse`-аар задлаад нэрийг `ugugdul.ner.trim()` гэж ав
(эхлэл кодод бэлэн).

- Амжилттай бол: `✓ <нэр>: <оноо>`
- Алдаа гарвал: `✗ <мөрийн дугаар>-р мөр: <алдааны нэр>` — алдааны `name`
  (`SyntaxError`, `TypeError`, …). `message`-ийг хэвлэхгүй: түүний текст
  хөтөч бүрт өөр.
- Мөр бүрийг амжилттай эсэхээс үл хамааран `finally` дотор тоол.

**Гаралт** төгсгөлд:

```text
Нийт <мөрийн тоо> мөр: <амжилттай> амжилттай, <алдаатай> алдаатай
Дундаж оноо: <амжилттай мөрүүдийн дундаж, аравтын 1 оронтой>
```

Амжилттай мөр нэг ч байхгүй бол `Дундаж оноо: байхгүй`.
""",
                tests=(
                    TestCaseSpec(
                        stdin=(
                            '{"ner":"Бат","onoo":85}\n{ эвдэрхий\n{"onoo":70}\n'
                            '{"ner":"Сараа","onoo":92}\n'
                        ),
                        expected_output=(
                            "✓ Бат: 85\n"
                            "✗ 2-р мөр: SyntaxError\n"
                            "✗ 3-р мөр: TypeError\n"
                            "✓ Сараа: 92\n"
                            "Нийт 4 мөр: 2 амжилттай, 2 алдаатай\n"
                            "Дундаж оноо: 88.5\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="null\nabc\n",
                        expected_output=(
                            "✗ 1-р мөр: TypeError\n"
                            "✗ 2-р мөр: SyntaxError\n"
                            "Нийт 2 мөр: 0 амжилттай, 2 алдаатай\n"
                            "Дундаж оноо: байхгүй\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin=(
                            '{"ner":"  Дорж ","onoo":60}\n[1,2]\n{"ner":"Туяа","onoo":75}\n'
                            '{"ner":"Болд","onoo":80}\n'
                        ),
                        expected_output=(
                            "✓ Дорж: 60\n"
                            "✗ 2-р мөр: TypeError\n"
                            "✓ Туяа: 75\n"
                            "✓ Болд: 80\n"
                            "Нийт 4 мөр: 3 амжилттай, 1 алдаатай\n"
                            "Дундаж оноо: 71.7\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin='{"ner":"Ганаа","onoo":100}\n',
                        expected_output=(
                            "✓ Ганаа: 100\nНийт 1 мөр: 1 амжилттай, 0 алдаатай\nДундаж оноо: 100.0\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin=(
                            '{"ner":"Бат","onoo":85,}\n'
                            "{'ner':'Бат'}\n"
                            '"Бат"\n'
                            '{"ner":"Номин","onoo":0}\n'
                        ),
                        expected_output=(
                            "✗ 1-р мөр: SyntaxError\n"
                            "✗ 2-р мөр: SyntaxError\n"
                            "✗ 3-р мөр: TypeError\n"
                            "✓ Номин: 0\n"
                            "Нийт 4 мөр: 1 амжилттай, 3 алдаатай\n"
                            "Дундаж оноо: 0.0\n"
                        ),
                    ),
                ),
                solution="""\
let niitMur = 0;
let amjilttai = 0;
let niitOnoo = 0;

let mur = prompt();
while (mur !== null) {
  const dugaar = niitMur + 1; // энэ мөрийн дугаар

  try {
    const ugugdul = JSON.parse(mur); // эвдэрхий JSON → SyntaxError
    const ner = ugugdul.ner.trim(); // ner байхгүй → TypeError
    console.log(`✓ ${ner}: ${ugugdul.onoo}`);
    // Алдаа гарвал эдгээр мөр ажиллахгүй — зөвхөн амжилттайг тоолно
    amjilttai++;
    niitOnoo += ugugdul.onoo;
  } catch (aldaa) {
    console.log(`✗ ${dugaar}-р мөр: ${aldaa.name}`);
  } finally {
    niitMur++; // алдаа гарсан ч, гараагүй ч ажиллана
  }

  mur = prompt();
}

console.log(`Нийт ${niitMur} мөр: ${amjilttai} амжилттай, ${niitMur - amjilttai} алдаатай`);
if (amjilttai > 0) {
  console.log(`Дундаж оноо: ${(niitOnoo / amjilttai).toFixed(1)}`);
} else {
  console.log("Дундаж оноо: байхгүй");
}
""",
                tips="""\
- `try`-г давталтын **дотор** шилжүүл: алдаа гарсан мөрийн дараа `catch`
  ажиллаад, давталт дараагийн мөр рүү үргэлжилнэ. `mur = prompt()`-г
  алдаа гарсан ч ажиллах газар (`try`-аас гадна) байлга — эс бөгөөс ижил
  мөрийг дахин дахин шалгаж, давталт гацна.
- `JSON.parse` эвдэрхий текстэд `SyntaxError` шиднэ. `null.ner`, эсвэл
  `undefined.trim()` нь `TypeError`. Хоёуланг нь нэг `catch` барина.
- Алдааны төрлийг `aldaa.name`-ээс ав.
- `amjilttai++`, `niitOnoo += …`-г `try` дотор, нэрийг авсны **дараа** бич —
  алдаа гарсан мөрт тэд ажиллахгүй.
- `finally` нь алдаа гарсан ч, гараагүй ч ажилладаг — мөрийн тоолуурт яг
  тохирно.
- Дундажийг `toFixed(1)`-ээр: `88.5`, `100.0`. Тэгд хуваахгүйн тулд
  амжилттай мөр байгаа эсэхийг эхлээд шалга.
""",
            ),
        ),
        LessonSpec(
            title="throw ба өөрийн алдаа",
            slug="throw-ba-uuriin-aldaa",
            description="Алдааг зориудаар үүсгэх, төрөлжүүлэх.",
            duration=450,
            content="""\
### `throw`

Функц нь буруу нөхцөлд алдаа шидэж болно:

```javascript
function huvaah(a, b) {
  if (b === 0) {
    throw new Error("Тэгд хуваах боломжгүй");
  }
  return a / b;
}
```

Ямар ч утга шидэж болох ч **үргэлж `Error` шид** — зөвхөн тэр нь мөр
(stack trace) авч явдаг.

```javascript
throw "буруу";              // муу
throw new Error("зөв");     // сайн
```

### Хэзээ шидэх, хэзээ буцаах вэ

| Нөхцөл | Сонголт |
|---|---|
| Хүлээгдэж буй үр дүн (олдсонгүй) | `null` буцаа |
| Дуудсан код буруу ажиллаж байна | `throw` |
| Сэргээж болохооргүй төлөв | `throw` |

Хэрэглэгч буруу утга оруулах нь **хүлээгдэж буй** зүйл — тэрийг алдаа
болгохоос илүү шалгалтын үр дүн болгон буцаах нь ихэвчлэн дээр.

### Өөрийн алдааны төрөл

`new Error(...)`-оор үүсгэсэн алдаа бүгд ижил төрөлтэй. Өөрийн төрлийг
`class` (класс) гэсэн бичлэгээр үүсгэнэ. Классыг энэ курст дэлгэрэнгүй
үзэхгүй — энэ жишээнд хэрэгтэй хэсгийг нь л тайлбарлая:

```javascript
class ShalgahAldaa extends Error {
  constructor(messej, talbar) {
    super(messej);
    this.name = "ShalgahAldaa";
    this.talbar = talbar;
  }
}

throw new ShalgahAldaa("Имэйл буруу", "email");
```

- `class ShalgahAldaa extends Error` — `Error`-ийн бүх шинжийг (message,
  stack) өвлөсөн шинэ төрөл үүсгэнэ.
- `constructor(...)` — `new ShalgahAldaa(...)` гэж дуудахад ажиллах функц.
  `this` нь шинээр үүсэж буй алдааны объект.
- `super(messej)` — `Error`-ийн өөрийнх нь хэсгийг ажиллуулж, мессежийг
  тохируулна. `this`-ийг ашиглахаас өмнө заавал дуудна.
- `this.talbar = talbar` — стандарт алдаанд байдаггүй нэмэлт талбар.

Ингэснээр алдааны **төрлөөр** ялгаж боловсруулж болно. `aldaa instanceof
ShalgahAldaa` нь «энэ алдаа ShalgahAldaa төрлийнх үү?» гэж асууж, `true`
эсвэл `false` өгнө:

```javascript
try {
  burtgeh(ugugdul);
} catch (aldaa) {
  if (aldaa instanceof ShalgahAldaa) {
    aldaaHaruulah(aldaa.talbar, aldaa.message);
  } else {
    throw aldaa; // танихгүй алдааг дээш нь дамжуул
  }
}
```

### Танихгүй алдааг дахин шид

Энэ бол чухал зуршил. Зөвхөн **боловсруулж чадах** алдааг барь. Бусдыг
нь дээш нь дамжуулаад, дээд түвшний боловсруулагчид даатга.

### Алдааны мессеж

Сайн мессеж нь дараах гурвыг агуулна:

1. Юу бүтэлгүйтсэн
2. Ямар утгатай
3. Юу хийх ёстой

```text
Муу:  "Алдаа гарлаа"
Сайн: "Хэрэглэгч олдсонгүй (id: 42). Дугаарыг шалгана уу."
```
""",
            initial_code="""\
// Error-ийг өвлөсөн өөрийн алдааны төрөл (хичээлийн тайлбарыг үз).
class ShalgahAldaa extends Error {
  constructor(messej, talbar) {
    super(messej);
    this.name = "ShalgahAldaa";
    this.talbar = talbar;
  }
}

const burtgesen = []; // амжилттай бүртгэгдсэн имэйлүүд

function burtgeh(hereglegch) {
  if (!hereglegch.email?.includes("@")) {
    throw new ShalgahAldaa("Имэйл хаяг буруу байна", "email");
  }
  // TODO: имэйл аль хэдийн бүртгэгдсэн бол ShalgahAldaa шид
  if ((hereglegch.nuuts ?? "").length < 8) {
    throw new ShalgahAldaa("Нууц үг дор хаяж 8 тэмдэгт байна", "nuuts");
  }
  // TODO: 16 нас хүрээгүй бол ShalgahAldaa шид
  // TODO: бүх шалгалтыг давсан имэйлийг burtgesen-д нэм
  return `${hereglegch.email} бүртгэгдлээ`;
}

let mur = prompt();
while (mur !== null) {
  try {
    console.log(`✓ ${burtgeh(JSON.parse(mur))}`);
  } catch (aldaa) {
    // TODO: зөвхөн ShalgahAldaa-г ингэж хэвлэ; танихгүй алдаа бол
    //       "! Санаандгүй алдаа: <алдааны нэр>"
    console.log(`✗ ${aldaa.talbar}: ${aldaa.message}`);
  }
  mur = prompt();
}

console.log(`Бүртгэгдсэн: ${burtgesen.length}`);
""",
            exercise=ExerciseSpec(
                statement="""\
Бүртгэлийн шалгалтыг `throw` ба өөрийн алдааны төрлөөр (`ShalgahAldaa`) хий.
Хүлээгдэж буй (шалгалтын) алдааг хэрэглэгчид ойлгомжтой харуулж, танихгүй
алдааг тусад нь мэдээл.

**Оролт:** мөр бүрт нэг хэрэглэгчийн JSON — `email`, `nuuts`, `nas` (тоо),
оролт дуустал. Эвдэрхий JSON эсвэл `null` ч ирж болно.

**Шалгалт.** `burtgeh` дараах дарааллаар шалгаж, эхний зөрчил дээр
`ShalgahAldaa` шиднэ:

| Нөхцөл | Мессеж | Талбар |
|---|---|---|
| `email`-д `@` байхгүй (эсвэл `email` алга) | `Имэйл хаяг буруу байна` | `email` |
| Энэ имэйл өмнө нь амжилттай бүртгэгдсэн | `<имэйл> аль хэдийн бүртгэлтэй` | `email` |
| `nuuts` 8-аас цөөн тэмдэгттэй (эсвэл алга) | `Нууц үг дор хаяж 8 тэмдэгт байна` | `nuuts` |
| `nas` 16-аас бага | `16 нас хүрээгүй байна (нас: <нас>)` | `nas` |

Бүх шалгалтыг давсан имэйлийг бүртгэгдсэнд тооцно.

**Гаралт:** оролтын мөр бүрт нэг мөр:

- Амжилттай: `✓ <имэйл> бүртгэгдлээ`
- `ShalgahAldaa`: `✗ <талбар>: <мессеж>`
- Бусад алдаа (жишээ нь `null`-ийн `email` → `TypeError`, эвдэрхий JSON →
  `SyntaxError`): `! Санаандгүй алдаа: <алдааны нэр>`

Төгсгөлд `Бүртгэгдсэн: <амжилттай бүртгэгдсэн тоо>`.
""",
                tests=(
                    TestCaseSpec(
                        stdin=(
                            '{"email":"bat","nuuts":"nuutsUg123","nas":20}\n'
                            '{"email":"bat@medleghub.mn","nuuts":"123","nas":20}\n'
                            '{"email":"bat@medleghub.mn","nuuts":"nuutsUg123","nas":20}\n'
                            "null\n"
                        ),
                        expected_output=(
                            "✗ email: Имэйл хаяг буруу байна\n"
                            "✗ nuuts: Нууц үг дор хаяж 8 тэмдэгт байна\n"
                            "✓ bat@medleghub.mn бүртгэгдлээ\n"
                            "! Санаандгүй алдаа: TypeError\n"
                            "Бүртгэгдсэн: 1\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin=(
                            '{"email":"saraa@mail.mn","nuuts":"saraa2026","nas":15}\n'
                            '{"email":"saraa@mail.mn","nuuts":"saraa2026","nas":16}\n'
                            '{"email":"saraa@mail.mn","nuuts":"busadUg99","nas":30}\n'
                        ),
                        expected_output=(
                            "✗ nas: 16 нас хүрээгүй байна (нас: 15)\n"
                            "✓ saraa@mail.mn бүртгэгдлээ\n"
                            "✗ email: saraa@mail.mn аль хэдийн бүртгэлтэй\n"
                            "Бүртгэгдсэн: 1\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin='{ эвдэрхий\n{"nuuts":"nuutsUg123","nas":22}\n',
                        expected_output=(
                            "! Санаандгүй алдаа: SyntaxError\n"
                            "✗ email: Имэйл хаяг буруу байна\n"
                            "Бүртгэгдсэн: 0\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin=(
                            '{"email":"a@a.mn","nuuts":"12345678","nas":18}\n'
                            '{"email":"b@b.mn","nuuts":"87654321","nas":40}\n'
                            '{"email":"c@c.mn","nuuts":"abcdefgh","nas":16}\n'
                        ),
                        expected_output=(
                            "✓ a@a.mn бүртгэгдлээ\n"
                            "✓ b@b.mn бүртгэгдлээ\n"
                            "✓ c@c.mn бүртгэгдлээ\n"
                            "Бүртгэгдсэн: 3\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin=(
                            '{"email":"dorj","nuuts":"1","nas":10}\n'
                            '{"email":"dorj@mail.mn","nas":25}\n'
                            "[1,2]\n"
                            '{"email":"dorj@mail.mn","nuuts":"dorj1234","nas":9}\n'
                        ),
                        expected_output=(
                            "✗ email: Имэйл хаяг буруу байна\n"
                            "✗ nuuts: Нууц үг дор хаяж 8 тэмдэгт байна\n"
                            "✗ email: Имэйл хаяг буруу байна\n"
                            "✗ nas: 16 нас хүрээгүй байна (нас: 9)\n"
                            "Бүртгэгдсэн: 0\n"
                        ),
                    ),
                ),
                solution="""\
// Error-ийг өвлөсөн өөрийн алдааны төрөл (хичээлийн тайлбарыг үз).
class ShalgahAldaa extends Error {
  constructor(messej, talbar) {
    super(messej);
    this.name = "ShalgahAldaa";
    this.talbar = talbar;
  }
}

const burtgesen = []; // амжилттай бүртгэгдсэн имэйлүүд

function burtgeh(hereglegch) {
  if (!hereglegch.email?.includes("@")) {
    throw new ShalgahAldaa("Имэйл хаяг буруу байна", "email");
  }
  if (burtgesen.includes(hereglegch.email)) {
    throw new ShalgahAldaa(`${hereglegch.email} аль хэдийн бүртгэлтэй`, "email");
  }
  if ((hereglegch.nuuts ?? "").length < 8) {
    throw new ShalgahAldaa("Нууц үг дор хаяж 8 тэмдэгт байна", "nuuts");
  }
  if (hereglegch.nas < 16) {
    throw new ShalgahAldaa(`16 нас хүрээгүй байна (нас: ${hereglegch.nas})`, "nas");
  }
  burtgesen.push(hereglegch.email);
  return `${hereglegch.email} бүртгэгдлээ`;
}

// Зөвхөн боловсруулж чадах алдааг (ShalgahAldaa) барина, бусдыг дээш нь.
function oroldoh(mur) {
  try {
    console.log(`✓ ${burtgeh(JSON.parse(mur))}`);
  } catch (aldaa) {
    if (aldaa instanceof ShalgahAldaa) {
      console.log(`✗ ${aldaa.talbar}: ${aldaa.message}`);
    } else {
      throw aldaa; // танихгүй алдааг дахин шид
    }
  }
}

let mur = prompt();
while (mur !== null) {
  // Дээд түвшний боловсруулагч — танихгүй алдааг бүртгээд үргэлжилнэ.
  try {
    oroldoh(mur);
  } catch (aldaa) {
    console.log(`! Санаандгүй алдаа: ${aldaa.name}`);
  }
  mur = prompt();
}

console.log(`Бүртгэгдсэн: ${burtgesen.length}`);
""",
                tips="""\
- `throw new ShalgahAldaa(мессеж, талбар)` — класс эхлэл кодод бэлэн.
  Мессежид утгыг нь оруул: сайн мессеж «юу, ямар утгатай» гэдгийг хэлнэ.
- Давхардлыг шалгахын тулд амжилттай бүртгэгдсэн имэйлүүдийг `burtgesen`
  массивт нэмж, `includes`-ээр хар. Шалгалтыг хүснэгтийн дарааллаар бич.
- `catch` дотор `aldaa instanceof ShalgahAldaa`-аар ялга. Танихгүй алдааг
  `throw aldaa`-аар дээш нь дамжуулж, гаднах `try/catch` дээр «Санаандгүй
  алдаа» болгож хэвлэх нь хичээлийн сайн зуршил.
- Танихгүй алдааны `message` хөтөч бүрт өөр текстэй — зөвхөн `name`-ийг
  хэвлэ.
""",
            ),
        ),
    ],
)

MODERN_MODULES = [MODERN, SCOPE, ERRORS]
