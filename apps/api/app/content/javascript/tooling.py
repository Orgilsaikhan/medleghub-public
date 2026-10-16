"""Модул 20-21 — Модул систем ба debugging.

Код олширч эхлэхэд файл хооронд хуваах, алдааг олох чадвар шаардлагатай
болно. Код ажиллуулагч нь ганц файл ажиллуулдаг тул `import` бичих
боломжгүй — даалгавар нь модулийн санааг функц, объектоор дуурайлгана
(файл = функц, export = буцаах объект). Debugging-ийн даалгавар нь алдаатай
програмыг засуулж, зөв гаралтыг тестээр баталгаажуулна.
"""

from app.content.types import ExerciseSpec, LessonSpec, ModuleSpec, TestCaseSpec

MODULES = ModuleSpec(
    title="Модул 20 — Модул (Modules)",
    description="Кодыг файлуудад хувааж, хооронд нь холбох.",
    lessons=[
        LessonSpec(
            title="import ба export",
            slug="import-ba-export",
            description="Кодыг файл хооронд хуваах.",
            duration=420,
            content="""\
Нэг файлд бүх кодоо бичих нь удахгүй боломжгүй болно. Модул систем нь
кодыг файлуудад хувааж, шаардлагатайг нь татаж авах боломж өгнө.

### Экспортлох

```javascript
// tootsoolol.js
export function nemeh(a, b) {
  return a + b;
}

export const PI = 3.14159;
```

### Импортлох

```javascript
// app.js
import { nemeh, PI } from "./tootsoolol.js";

console.log(nemeh(2, 3));
```

Зам нь `./`-ээр эхлэх ёстой бөгөөд өргөтгөлийг нь бичнэ. Үүнгүйгээр
хөтөч түүнийг **багц** (npm сан) гэж үзнэ.

### HTML-д холбох

```html
<script type="module" src="app.js"></script>
```

`type="module"` заавал. Үүнгүйгээр `import` нь синтаксийн алдаа болно.

### Модулийн онцлог

| Шинж | Тайлбар |
|---|---|
| Хамрах хүрээ | Файл тус бүр өөрийн хүрээтэй — global бохирдохгүй |
| `defer` | Модул үргэлж HTML уншигдсаны дараа ажиллана |
| Нэг удаа | Олон газраас импортлосон ч нэг л удаа ажиллана |
| Strict | `"use strict"` бичихгүйгээр хүчинтэй |

Сүүлийн шинж нь чухал: модул нь **нэг удаа** ажиллаад үр дүнгээ хадгална.
Тиймээс модулийн дээд түвшний код нь тохиргоо бэлдэхэд тохиромжтой.

### Нэр солих

```javascript
import { nemeh as nemehFunkts } from "./tootsoolol.js";
```

### Бүгдийг нэг объект болгож

```javascript
import * as tootsoolol from "./tootsoolol.js";

console.log(tootsoolol.nemeh(2, 3));
```

### Файлын тойрог хамаарал

A нь B-г, B нь A-г импортлох нь алдаа үүсгэнэ. Ийм тохиолдолд хамтын
хэсгийг гурав дахь файл руу гарга.

### Код ажиллуулагч дээр модулийг дуурайх

Код ажиллуулагч ганц файл ажиллуулдаг тул `import`/`export` бичвэл
синтаксийн алдаа болно. Даалгаварт модулийг **функцээр** дуурайна: файлын
бүх код нэг функц дотор, буцаасан объект нь export-ууд. Функцийн хүрээ
(Модул 16) нь файлын хүрээ шиг ажиллана — export хийгээгүй зүйл гаднаас
харагдахгүй.
""",
            initial_code="""\
// Код ажиллуулагч ганц файл ажиллуулдаг тул import/export бичиж болохгүй.
// Файл бүрийг НЭГ функц болгож, export хийх зүйлсээ объектоор буцаая.

// --- tootsoolol.js --------------------------------------------------------
function tootsoololModul() {
  // Модулийн дотоод туслах функц — export хийхгүй тул гаднаас харагдахгүй.
  // 0.1 + 0.2 → 0.3 гэх мэтээр 2 орон хүртэл бөөрөнхийлнө.
  function oirtuulah(too) {
    return Math.round(too * 100) / 100;
  }

  function nemeh(a, b) {
    return oirtuulah(a + b);
  }

  // TODO 1: hasah(a, b), urjuuleh(a, b), huvaah(a, b) функцуудыг бич.
  //         Бүгд хариугаа oirtuulah()-аар дамжуулж буцаана.
  //         huvaah нь b === 0 үед Error("0-д хуваах боломжгүй") шиднэ.

  // TODO 2: export-уудаа ЭНЭ дарааллаар буцаа: nemeh, hasah, urjuuleh, huvaah
  return { nemeh };
}

// --- app.js ---------------------------------------------------------------
// import * as tootsoolol from "./tootsoolol.js"; гэсэнтэй ижил санаа
const tootsoolol = tootsoololModul();

const uildel = prompt();
const a = Number(prompt());
const b = Number(prompt());

console.log(`Export: ${Object.keys(tootsoolol).join(", ")}`);

// TODO 3: tootsoolol[uildel] нь функц биш бол «<uildel>» гэсэн export алга
//         гэж хэвлэ. Функц бол дуудаад "<uildel>(<a>, <b>) = <хариу>" гэж
//         хэвлэ. Алдаа шидвэл "Алдаа: <мессеж>" гэж хэвлэ.
""",
            exercise=ExerciseSpec(
                statement="""\
Код ажиллуулагч `import`/`export`-ийг дэмждэггүй тул модулийг **функцээр**
дуурайна: `tootsoololModul()` нь `tootsoolol.js` файлын бүх кодыг агуулж,
буцаасан объект нь тэр файлын **export**-ууд болно. Функц дотор үлдсэн зүйл
(`oirtuulah`) гаднаас харагдахгүй — жинхэнэ модулийн хүрээ шиг.

1. Модулид `hasah`, `urjuuleh` (үржүүлэх), `huvaah` функцуудыг нэм. Бүгд
   хариугаа `oirtuulah()`-аар дамжуулна. `huvaah` нь `b` нь 0 бол
   `Error("0-д хуваах боломжгүй")` шиднэ.
2. `nemeh, hasah, urjuuleh, huvaah`-ийг **яг энэ дарааллаар** export хий
   (буцаах объектод нэм).
3. `app.js` хэсэгт оролтын үйлдлийн нэрээр export-ийг олж ажиллуул —
   `import * as tootsoolol`-той адил `tootsoolol[uildel]`.

**Оролт:** гурван мөр — үйлдлийн нэр (`nemeh`, `hasah`, …), `a`, `b` тоо.

**Гаралт:** эхний мөр нь export-уудын жагсаалт (эхлэл кодод бэлэн),
дараагийн мөр нь үйлдлийн хариу:

```text
Export: nemeh, hasah, urjuuleh, huvaah
<үйлдэл>(<a>, <b>) = <хариу>
```

- Ийм нэртэй **функц** export-д байхгүй бол (жишээ нь дотоод `oirtuulah`):
  `«<үйлдэл>» гэсэн export алга`
- Функц алдаа шидвэл: `Алдаа: <мессеж>`
""",
                tests=(
                    TestCaseSpec(
                        stdin="nemeh\n7\n5\n",
                        expected_output="Export: nemeh, hasah, urjuuleh, huvaah\nnemeh(7, 5) = 12\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="huvaah\n10\n4\n",
                        expected_output="Export: nemeh, hasah, urjuuleh, huvaah\nhuvaah(10, 4) = 2.5\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="hasah\n3\n8\n",
                        expected_output="Export: nemeh, hasah, urjuuleh, huvaah\nhasah(3, 8) = -5\n",
                    ),
                    TestCaseSpec(
                        stdin="urjuuleh\n1.5\n1.5\n",
                        expected_output="Export: nemeh, hasah, urjuuleh, huvaah\nurjuuleh(1.5, 1.5) = 2.25\n",
                    ),
                    TestCaseSpec(
                        stdin="huvaah\n10\n3\n",
                        expected_output="Export: nemeh, hasah, urjuuleh, huvaah\nhuvaah(10, 3) = 3.33\n",
                    ),
                    TestCaseSpec(
                        stdin="huvaah\n5\n0\n",
                        expected_output="Export: nemeh, hasah, urjuuleh, huvaah\nАлдаа: 0-д хуваах боломжгүй\n",
                    ),
                    TestCaseSpec(
                        stdin="oirtuulah\n1\n2\n",
                        expected_output="Export: nemeh, hasah, urjuuleh, huvaah\n«oirtuulah» гэсэн export алга\n",
                    ),
                    TestCaseSpec(
                        stdin="nemeh\n0.1\n0.2\n",
                        expected_output="Export: nemeh, hasah, urjuuleh, huvaah\nnemeh(0.1, 0.2) = 0.3\n",
                    ),
                ),
                solution="""\
// --- tootsoolol.js --------------------------------------------------------
function tootsoololModul() {
  // Модулийн дотоод туслах функц — export хийгдэхгүй тул гаднаас харагдахгүй.
  function oirtuulah(too) {
    return Math.round(too * 100) / 100;
  }

  function nemeh(a, b) {
    return oirtuulah(a + b);
  }

  function hasah(a, b) {
    return oirtuulah(a - b);
  }

  function urjuuleh(a, b) {
    return oirtuulah(a * b);
  }

  function huvaah(a, b) {
    if (b === 0) {
      throw new Error("0-д хуваах боломжгүй");
    }
    return oirtuulah(a / b);
  }

  // Буцаасан объект = энэ модулийн export-ууд
  return { nemeh, hasah, urjuuleh, huvaah };
}

// --- app.js ---------------------------------------------------------------
// import * as tootsoolol from "./tootsoolol.js"; гэсэнтэй ижил санаа
const tootsoolol = tootsoololModul();

const uildel = prompt();
const a = Number(prompt());
const b = Number(prompt());

console.log(`Export: ${Object.keys(tootsoolol).join(", ")}`);

const funkts = tootsoolol[uildel];

if (typeof funkts !== "function") {
  console.log(`«${uildel}» гэсэн export алга`);
} else {
  try {
    console.log(`${uildel}(${a}, ${b}) = ${funkts(a, b)}`);
  } catch (aldaa) {
    console.log(`Алдаа: ${aldaa.message}`);
  }
}
""",
                tips="""\
- Модул = функц, export = буцаах объект. `return { nemeh, hasah }` нь
  `{ nemeh: nemeh, hasah: hasah }`-ийн товч бичиглэл.
- `Object.keys()` нь түлхүүрүүдийг бичсэн дарааллаар нь буцаана — эхний мөр
  таны `return`-ийн дарааллыг яг харуулна.
- `tootsoolol[uildel]` — хувьсагчид байгаа нэрээр шинж чанар авна. Ийм
  export байхгүй бол `undefined`. `typeof … === "function"`-оор шалга.
- `huvaah` дотор `throw`, `app.js` дотор `try/catch` — алдаа модулиас гарч,
  дуудсан газарт баригдана.
- Хариуг `oirtuulah()`-аар дамжуулахаа бүү мартаарай: `0.1 + 0.2` нь
  `0.30000000000000004`.
""",
            ),
        ),
        LessonSpec(
            title="Нэрлэсэн ба анхдагч export",
            slug="nerlesen-ba-anhdagch-export",
            description="Хоёр төрлийн экспортын ялгаа, аль нь хэзээ.",
            duration=420,
            content="""\
### Нэрлэсэн export (named)

Нэг файлаас **хэдэн ч** зүйл экспортлож болно:

```javascript
// tootsoolol.js
export function nemeh(a, b) { return a + b; }
export function hasah(a, b) { return a - b; }
```

Импортлохдоо нэрийг нь **яг таг** бичнэ:

```javascript
import { nemeh, hasah } from "./tootsoolol.js";
```

Төгсгөлд нэг дор экспортлож ч болно:

```javascript
function nemeh(a, b) { return a + b; }
function hasah(a, b) { return a - b; }

export { nemeh, hasah };
```

### Анхдагч export (default)

Файл тутамд **зөвхөн нэг**:

```javascript
// hereglegch.js
export default function hereglegchUusgeh(ner) {
  return { ner };
}
```

Импортлохдоо ямар ч нэр өгч болно — хаалт байхгүй:

```javascript
import hereglegchUusgeh from "./hereglegch.js";
import uusgeh from "./hereglegch.js"; // ижил зүйл
```

### Хамтад нь

```javascript
export default hereglegchUusgeh;
export const ANHDAGCH_NAS = 18;
```

```javascript
import hereglegchUusgeh, { ANHDAGCH_NAS } from "./hereglegch.js";
```

### Алийг нь сонгох вэ

| Нөхцөл | Сонголт |
|---|---|
| Файл нь нэг зүйлд зориулагдсан (нэг компонент, нэг гол функц) | default |
| Файл нь хэд хэдэн туслах агуулна | named |

Олон баг **зөвхөн named** ашиглахыг шаарддаг. Шалтгаан нь:

- Нэр нь тогтмол байдаг тул хайхад амархан
- Автомат импорт болон дахин нэрлэлт найдвартай ажиллана
- Үсгийн алдаа нь шууд алдаа болж илэрнэ

Аль нь ч буруу биш. Гол нь **төсөл дотроо нэг журамтай** байх.

### Түгээмэл алдаа

```javascript
// export default байхад
import { hereglegchUusgeh } from "./hereglegch.js"; // undefined!
```

Хаалт нэмэх, хасахаа андуурах нь хамгийн олон тохиолддог алдаа. Алдааны
мессеж нь тодорхойгүй байдаг тул эхлээд үүнийг шалга.

### Код ажиллуулагч дээр

`import * as m from "./hereglegch.js"` гэвэл анхдагч export нь `m.default`
шинж дээр байдаг. Даалгаварт модулиудыг яг ийм объектоор дуурайж, хаалттай,
хаалтгүй import тус бүр ямар утга авдгийг кодоор тодорхойлно.
""",
            initial_code="""\
// Файл бүрийг нэг удаа дуудагдах функцээр дуурайна (өмнөх хичээлийн адил).
// «default» түлхүүр нь анхдагч export-ийн байр.

// --- hereglegch.js: export default + нэрлэсэн export ----------------------
function hereglegchFail() {
  const ANHDAGCH_NAS = 18;

  function hereglegchUusgeh(ner, nas = ANHDAGCH_NAS) {
    return { ner, nas };
  }

  return { default: hereglegchUusgeh, ANHDAGCH_NAS };
}

// --- tools.js: зөвхөн нэрлэсэн export -------------------------------------
function toolsFail() {
  const tomUseg = (mur) => mur[0].toUpperCase() + mur.slice(1);
  const tovchloh = (mur, urt) => (mur.length > urt ? mur.slice(0, urt) + "…" : mur);

  return { tomUseg, tovchloh };
}

// Зам → модулийн export-ууд (хөтөч ч модул бүрийг нэг удаа ачаалаад хадгалдаг)
const failuud = {
  "./hereglegch.js": hereglegchFail(),
  "./tools.js": toolsFail(),
};

// Утгыг тайлбарлана (бэлэн). Функцийн .name нь түүний жинхэнэ нэр.
function tailbar(utga) {
  if (utga === undefined) {
    return "undefined — ийм export алга";
  }
  if (typeof utga === "function") {
    return `функц ${utga.name}`;
  }
  return String(utga);
}

const zam = prompt().trim();
const hesseg = prompt().trim(); // import ба from хоорондох хэсэг

const modul = failuud[zam];

if (modul === undefined) {
  console.log(`Модул олдсонгүй: ${zam}`);
} else {
  // TODO 1: hesseg нь "{"-ээр эхэлбэл — НЭРЛЭСЭН import.
  //         Хаалтыг хасаад таслалаар хуваа. Нэр бүр "tomUseg" эсвэл
  //         "tomUseg as tom" хэлбэртэй. Нэр бүрт нэг мөр хэвлэ:
  //         <дотоод нэр> ← <export нэр>: <tailbar(modul[export нэр])>

  // TODO 2: хаалтгүй бол — АНХДАГЧ import. Нэр нь дурын, утга нь modul.default:
  //         <нэр> ← default: <tailbar(modul.default)>
  console.log("TODO:", hesseg);
}
""",
            exercise=ExerciseSpec(
                statement="""\
Жинхэнэ модулд `import * as m from "./x.js"` гэвэл анхдагч export нь
`m.default` дээр байдаг. Эхлэл код яг ийм объектуудыг бэлдсэн:
`failuud["./hereglegch.js"]` нь `{ default: hereglegchUusgeh, ANHDAGCH_NAS }`,
`failuud["./tools.js"]` нь `{ tomUseg, tovchloh }` (default-гүй).

`import … from "<зам>"` мөрийн **дундах хэсгийг** уншиж, нэр бүрт ямар утга
холбогдохыг хэвлэ:

- Хэсэг `{`-ээр эхэлбэл — **нэрлэсэн** import. Хаалтан доторх нэрс таслалаар
  тусгаарлагдана; нэр бүр `tomUseg` эсвэл `tomUseg as tom` хэлбэртэй. Утга нь
  `modul[<export нэр>]` — нэр **яг таарах** ёстой.
- Хаалтгүй бол — **анхдагч** import. Нэр нь дурын, утга нь `modul.default`.

**Оролт:** хоёр мөр — модулийн зам (`./hereglegch.js`), дараа нь `import`
ба `from`-ын хоорондох хэсэг (`uusgeh` эсвэл `{ tomUseg, tovchloh as tovch }`).

**Гаралт:** холбоос бүрт нэг мөр, нэрлэсэн import-д хаалтан доторх
дарааллаар:

```text
<дотоод нэр> ← <export нэр>: <tailbar(утга)>
```

Анхдагч import-д `<export нэр>` нь `default`. Утгыг эхлэл кодын `tailbar()`
тайлбарлана — байхгүй export-д `undefined — ийм export алга` гэж гарна.
Зам `failuud`-д байхгүй бол ганц мөр: `Модул олдсонгүй: <зам>` (бэлэн).
""",
                tests=(
                    TestCaseSpec(
                        stdin="./hereglegch.js\nuusgeh\n",
                        expected_output="uusgeh ← default: функц hereglegchUusgeh\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="./tools.js\n{ tomUseg, tovchloh }\n",
                        expected_output="tomUseg ← tomUseg: функц tomUseg\ntovchloh ← tovchloh: функц tovchloh\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="./hereglegch.js\n{ hereglegchUusgeh }\n",
                        expected_output="hereglegchUusgeh ← hereglegchUusgeh: undefined — ийм export алга\n",
                    ),
                    TestCaseSpec(
                        stdin="./tools.js\ntools\n",
                        expected_output="tools ← default: undefined — ийм export алга\n",
                    ),
                    TestCaseSpec(
                        stdin="./hereglegch.js\n{ ANHDAGCH_NAS as nas }\n",
                        expected_output="nas ← ANHDAGCH_NAS: 18\n",
                    ),
                    TestCaseSpec(
                        stdin="./tuslah.js\nx\n",
                        expected_output="Модул олдсонгүй: ./tuslah.js\n",
                    ),
                    TestCaseSpec(
                        stdin="./hereglegch.js\nhereglegchUusgeh\n",
                        expected_output="hereglegchUusgeh ← default: функц hereglegchUusgeh\n",
                    ),
                    TestCaseSpec(
                        stdin="./tools.js\n{tovchloh as tovch,tomUseg as tom}\n",
                        expected_output="tovch ← tovchloh: функц tovchloh\ntom ← tomUseg: функц tomUseg\n",
                    ),
                ),
                solution="""\
// --- hereglegch.js: export default + нэрлэсэн export ----------------------
function hereglegchFail() {
  const ANHDAGCH_NAS = 18;

  function hereglegchUusgeh(ner, nas = ANHDAGCH_NAS) {
    return { ner, nas };
  }

  return { default: hereglegchUusgeh, ANHDAGCH_NAS };
}

// --- tools.js: зөвхөн нэрлэсэн export -------------------------------------
function toolsFail() {
  const tomUseg = (mur) => mur[0].toUpperCase() + mur.slice(1);
  const tovchloh = (mur, urt) => (mur.length > urt ? mur.slice(0, urt) + "…" : mur);

  return { tomUseg, tovchloh };
}

const failuud = {
  "./hereglegch.js": hereglegchFail(),
  "./tools.js": toolsFail(),
};

function tailbar(utga) {
  if (utga === undefined) {
    return "undefined — ийм export алга";
  }
  if (typeof utga === "function") {
    return `функц ${utga.name}`;
  }
  return String(utga);
}

const zam = prompt().trim();
const hesseg = prompt().trim();

const modul = failuud[zam];

if (modul === undefined) {
  console.log(`Модул олдсонгүй: ${zam}`);
} else if (hesseg.startsWith("{")) {
  // import { a, b as c } from "..." — нэрлэсэн: нэр нь яг таарах ёстой
  const nernuud = hesseg.slice(1, -1).split(",");
  for (const ner of nernuud) {
    const [exportNer, dotoodNer = exportNer] = ner.trim().split(" as ");
    console.log(`${dotoodNer} ← ${exportNer}: ${tailbar(modul[exportNer])}`);
  }
} else {
  // import ner from "..." — анхдагч: нэр нь дурын, утга нь default
  console.log(`${hesseg} ← default: ${tailbar(modul.default)}`);
}
""",
                tips="""\
- Хаалт байгаа эсэх (`hesseg.startsWith("{")`) нь л нэрлэсэн, анхдагч хоёрыг
  ялгана. Хичээлийн «Түгээмэл алдаа» яг энэ: `{ hereglegchUusgeh }` гэвэл
  `modul.hereglegchUusgeh` хайгаад `undefined` авна.
- Хаалтыг `slice(1, -1)`-ээр хасаад `split(",")`, нэр бүрийг `trim()`.
- `"tomUseg as tom".split(" as ")` → `["tomUseg", "tom"]`. `as` байхгүй бол
  ганц элемент гарна — задлахдаа анхдагч утга өгч болно: `[a, b = a]`.
- Анхдагч export-д нэр хамаарахгүй: `import yuChBaisan from` гэсэн ч
  `modul.default` ирнэ.
- Мөр бүрийн дараалал хаалтан доторх дарааллыг дагана.
""",
            ),
        ),
    ],
)

DEBUGGING = ModuleSpec(
    title="Модул 21 — Debugging",
    description="Алдааг олох, уншиж ойлгох арга барил.",
    lessons=[
        LessonSpec(
            title="Console ба алдаа унших",
            slug="console-ba-aldaa-unshih",
            description="Алдааны мессежийг задлан унших, console-ийн хэрэгслүүд.",
            duration=450,
            content="""\
### Алдааны мессежийг унших

```text
TypeError: Cannot read properties of undefined (reading 'ner')
    at haruulah (app.js:14:22)
    at HTMLButtonElement.<anonymous> (app.js:31:5)
```

Гурван хэсэгт хуваан унш:

| Хэсэг | Утга |
|---|---|
| `TypeError` | Алдааны **төрөл** |
| `Cannot read properties of undefined` | Юу болсон |
| `app.js:14:22` | Хаана болсон — файл, мөр, багана |

Дээд мөр нь алдаа гарсан газар. Доод мөрүүд нь түүнийг **хэн дуудсаныг**
харуулна.

### Түгээмэл алдаанууд

| Мессеж | Ихэвчлэн шалтгаан |
|---|---|
| `Cannot read properties of undefined` | Объект байхгүй байхад дотор нь орсон |
| `x is not a function` | Нэрээ андуурсан, эсвэл утга нь функц биш |
| `x is not defined` | Бичиглэлийн алдаа, эсвэл хамрах хүрээнээс гадуур |
| `Unexpected token` | Хаалт, хашилт дутуу |
| `Cannot access before initialization` | `let`/`const`-ыг зарлахаас өмнө ашигласан |

### Console-ийн хэрэгслүүд

```javascript
console.log(utga);
console.table(massiv);      // массивыг хүснэгтээр
console.group("Нэр");       // бүлэглэнэ
console.groupEnd();
console.time("achaalt");    // хугацаа хэмжинэ
console.timeEnd("achaalt");
console.assert(nuhtsul, "мессеж"); // зөвхөн худал үед хэвлэнэ
```

`console.table` нь объектын массивыг шалгахад маш хэрэгтэй.

### Шошготой хэвлэ

```javascript
console.log(hereglegch);            // юу нь вэ гэдэг нь тодорхойгүй
console.log("hereglegch:", hereglegch); // дээр
console.log({ hereglegch });        // хамгийн дээр — нэр автоматаар орно
```

Сүүлийн заль мэх нь олон хувьсагч хэвлэхэд цаг хэмнэнэ.

### Хоёртын хайлт

Алдаа хаана байгаа нь ойлгомжгүй бол кодын **дунд** нь хэвлэ. Алдаа
түүнээс өмнө үү, хойно юу гэдгийг олоод дахин хагаслана. Хэдхэн алхмаар
олдоно.

Даалгаварт алдааны мөр, stack-ийн мөрийг кодоор задлан уншиж, дээрх
хүснэгтээс зөвлөгөө өгдөг жижиг «алдаа тайлбарлагч» бичнэ.
""",
            initial_code="""\
// Мессежид орсон хэсэг → зөвлөгөө (хичээлийн «Түгээмэл алдаанууд» хүснэгт)
const ZUVLUGUUNUUD = [
  ["Cannot read properties of", "Объект байхгүй (undefined/null) байхад дотор нь орсон"],
  ["is not a function", "Нэрээ андуурсан, эсвэл утга нь функц биш"],
  ["is not defined", "Бичиглэлийн алдаа, эсвэл хамрах хүрээнээс гадуур"],
  ["Unexpected token", "Хаалт, хашилт дутуу"],
  ["before initialization", "let/const-ыг зарлахаас өмнө ашигласан"],
];

const aldaaMur = prompt(); // "TypeError: Cannot read properties of undefined (reading 'ner')"
const stackMur = prompt(); // "    at haruulah (app.js:14:22)" — байхгүй бол null

// Шошготой хэвлэх заль: юу ирснийг харах гэж түр нэмсэн мөр.
// Гаралтад орж тестийг унагаана — ойлгосныхоо дараа устгаарай.
console.log({ aldaaMur, stackMur });

// TODO 1: aldaaMur-ийг ЭХНИЙ ": "-ээр хоёр хуваа (мессеж дотор ": " дахин
//         байж болно). "Төрөл: …", "Мессеж: …" гэж хэвлэ.

// TODO 2: stackMur null эсвэл хоосон бол "Байршил: тодорхойгүй".
//         Эс бөгөөс эхний "at "-ийг хасаад:
//           - " (" байвал түүний өмнөх нь функцийн нэр, хаалтан доторх нь байршил;
//           - байхгүй бол функц нь "(дээд түвшин)", үлдсэн бүх мөр нь байршил.
//         Байршлыг ":"-ээр файл, мөр, багана болгон хувааж хэвлэ.

// TODO 3: ZUVLUGUUNUUD-ээс мессежид ОРСОН эхний хэсгийг олж зөвлөгөөг нь
//         хэвлэ. Олдохгүй бол "Мессежийг бүтнээр нь хайж үзээрэй".
""",
            exercise=ExerciseSpec(
                statement="""\
Алдааны мессежийг гурван хэсэгт хуваан уншдаг програм бич: **төрөл**,
**юу болсон**, **хаана**. Дээр нь хичээлийн «Түгээмэл алдаанууд» хүснэгтээс
зөвлөгөө өг (эхлэл кодод `ZUVLUGUUNUUD` бэлэн).

**Оролт:**

- 1-р мөр: алдааны мөр — `<Төрөл>: <мессеж>`. Мессеж дотор `: ` дахин орж
  болно, тиймээс **эхний** `: ` хүртэлх нь төрөл.
- 2-р мөр (байхгүй ч байж болно): stack-ийн эхний мөр —
  `    at <функц> (<файл>:<мөр>:<багана>)`, эсвэл функцийн нэргүй
  `    at <файл>:<мөр>:<багана>`. Түүнээс хойших мөрүүдийг (хэн дуудсан) үл
  тооно.

**Гаралт:**

```text
Төрөл: <төрөл>
Мессеж: <мессеж>
Функц: <функц>
Байршил: <файл>, <мөр>-р мөр, <багана>-р багана
Зөвлөгөө: <зөвлөгөө>
```

- Функцийн нэргүй stack мөрөнд: `Функц: (дээд түвшин)`.
- 2-р мөр байхгүй (`prompt()` нь `null`) эсвэл хоосон бол `Функц` мөрийг
  хэвлэхгүй, `Байршил: тодорхойгүй` гэж хэвлэнэ.
- Зөвлөгөө нь `ZUVLUGUUNUUD`-ийн дарааллаар мессежид **орсон** эхний хэсгийнх;
  аль нь ч ороогүй бол `Мессежийг бүтнээр нь хайж үзээрэй`.
- Эхлэл кодын `console.log({ … })` шалгах мөрийг эцэст нь устга.
""",
                tests=(
                    TestCaseSpec(
                        stdin="TypeError: Cannot read properties of undefined (reading 'ner')\n    at haruulah (app.js:14:22)\n    at HTMLButtonElement.<anonymous> (app.js:31:5)\n",
                        expected_output="Төрөл: TypeError\nМессеж: Cannot read properties of undefined (reading 'ner')\nФункц: haruulah\nБайршил: app.js, 14-р мөр, 22-р багана\nЗөвлөгөө: Объект байхгүй (undefined/null) байхад дотор нь орсон\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="ReferenceError: hereglegch is not defined\n    at app.js:7:13\n",
                        expected_output="Төрөл: ReferenceError\nМессеж: hereglegch is not defined\nФункц: (дээд түвшин)\nБайршил: app.js, 7-р мөр, 13-р багана\nЗөвлөгөө: Бичиглэлийн алдаа, эсвэл хамрах хүрээнээс гадуур\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="TypeError: ur.map is not a function\n    at zurah (jagsaalt.js:22:8)\n",
                        expected_output="Төрөл: TypeError\nМессеж: ur.map is not a function\nФункц: zurah\nБайршил: jagsaalt.js, 22-р мөр, 8-р багана\nЗөвлөгөө: Нэрээ андуурсан, эсвэл утга нь функц биш\n",
                    ),
                    TestCaseSpec(
                        stdin="SyntaxError: Unexpected token '}'\n",
                        expected_output="Төрөл: SyntaxError\nМессеж: Unexpected token '}'\nБайршил: тодорхойгүй\nЗөвлөгөө: Хаалт, хашилт дутуу\n",
                    ),
                    TestCaseSpec(
                        stdin="ReferenceError: Cannot access 'too' before initialization\n    at tooloh (tooluur.js:3:15)\n",
                        expected_output="Төрөл: ReferenceError\nМессеж: Cannot access 'too' before initialization\nФункц: tooloh\nБайршил: tooluur.js, 3-р мөр, 15-р багана\nЗөвлөгөө: let/const-ыг зарлахаас өмнө ашигласан\n",
                    ),
                    TestCaseSpec(
                        stdin="Error: HTTP алдаа: 503\n    at achaalah (api.js:40:11)\n",
                        expected_output="Төрөл: Error\nМессеж: HTTP алдаа: 503\nФункц: achaalah\nБайршил: api.js, 40-р мөр, 11-р багана\nЗөвлөгөө: Мессежийг бүтнээр нь хайж үзээрэй\n",
                    ),
                    TestCaseSpec(
                        stdin="RangeError: Invalid array length\n    at uusgeh (massiv.js:2:9)\n",
                        expected_output="Төрөл: RangeError\nМессеж: Invalid array length\nФункц: uusgeh\nБайршил: massiv.js, 2-р мөр, 9-р багана\nЗөвлөгөө: Мессежийг бүтнээр нь хайж үзээрэй\n",
                    ),
                ),
                solution="""\
const ZUVLUGUUNUUD = [
  ["Cannot read properties of", "Объект байхгүй (undefined/null) байхад дотор нь орсон"],
  ["is not a function", "Нэрээ андуурсан, эсвэл утга нь функц биш"],
  ["is not defined", "Бичиглэлийн алдаа, эсвэл хамрах хүрээнээс гадуур"],
  ["Unexpected token", "Хаалт, хашилт дутуу"],
  ["before initialization", "let/const-ыг зарлахаас өмнө ашигласан"],
];

const aldaaMur = prompt();
const stackMur = prompt(); // байхгүй бол null

// 1. "TypeError: мессеж" — эхний ": " хүртэлх нь төрөл, үлдсэн нь мессеж
const zaag = aldaaMur.indexOf(": ");
const turul = aldaaMur.slice(0, zaag);
const messej = aldaaMur.slice(zaag + 2);

console.log(`Төрөл: ${turul}`);
console.log(`Мессеж: ${messej}`);

// 2. "    at haruulah (app.js:14:22)" эсвэл "    at app.js:31:5"
if (stackMur === null || stackMur.trim() === "") {
  console.log("Байршил: тодорхойгүй");
} else {
  const at = stackMur.trim().slice(3);
  let funkts = "(дээд түвшин)";
  let bairshil = at;

  if (at.includes(" (")) {
    funkts = at.slice(0, at.indexOf(" ("));
    bairshil = at.slice(at.indexOf(" (") + 2, -1);
  }

  const [fail, mur, bagana] = bairshil.split(":");
  console.log(`Функц: ${funkts}`);
  console.log(`Байршил: ${fail}, ${mur}-р мөр, ${bagana}-р багана`);
}

// 3. Мессежид аль хэсэг нь орсныг хүснэгтээс хайна
const olson = ZUVLUGUUNUUD.find(([hesseg]) => messej.includes(hesseg));
console.log(`Зөвлөгөө: ${olson ? olson[1] : "Мессежийг бүтнээр нь хайж үзээрэй"}`);
""",
                tips="""\
- `indexOf(": ")` нь **эхний** байрлалыг өгнө: `slice(0, i)` нь төрөл,
  `slice(i + 2)` нь мессеж. `split(": ")` хэрэглэвэл `HTTP алдаа: 503` гэх
  мэт мессеж хуваагдаж тасарна.
- Stack мөрийн урдах зайг `trim()`-ээр хасаад `"at "`-ийг `slice(3)`-аар.
- `" ("` байвал функцийн нэр нь түүний өмнө, байршил нь хаалтан дотор —
  сүүлийн `)`-ийг `slice(…, -1)` хасна.
- `"app.js:14:22".split(":")` → `["app.js", "14", "22"]` — массив задлалтаар
  шууд нэрлэж болно.
- `find` нь нөхцөл биелсэн эхний элементийг, олдохгүй бол `undefined`
  буцаана. Элемент бүр `[хэсэг, зөвлөгөө]` хос.
- `console.log({ aldaaMur })` нь хөгжүүлэх үед маш хэрэгтэй, гэхдээ гаралтад
  орно — тест илгээхээсээ өмнө устга.
""",
            ),
        ),
        LessonSpec(
            title="Breakpoint ба debugger",
            slug="breakpoint-ba-debugger",
            description="Кодыг зогсоож, алхам алхмаар шалгах.",
            duration=450,
            content="""\
`console.log` нь хурдан ч хязгаартай. Breakpoint нь кодыг **зогсоож**,
тэр агшны бүх хувьсагчийг харуулна.

### Breakpoint тавих

DevTools → **Sources** таб → файлаа нээ → мөрийн дугаар дээр дар.

Код тэр мөрөнд хүрэхэд зогсоно. Дараа нь:

- **Scope** самбарт бүх хувьсагчийн утга харагдана
- **Call Stack** самбарт энэ функц хэрхэн дуудагдсан нь харагдана
- Console дээр тэр агшны хүрээнд код бичиж ажиллуулж болно

Сүүлийнх нь хамгийн хүчтэй нь: `console.log` нь урьдчилан бодсон зүйлээ
л харуулдаг бол breakpoint дээр **юу ч** асууж болно.

### `debugger` түлхүүр үг

```javascript
function bodoh(a, b) {
  debugger; // DevTools нээлттэй бол энд зогсоно
  return a + b;
}
```

Хэрэгтэй боловч **commit хийхээсээ өмнө устгаарай**.

### Алхмын товчнууд

| Товч | Үйлдэл |
|---|---|
| Resume | Дараагийн breakpoint хүртэл үргэлжлүүлнэ |
| Step over | Дараагийн мөр рүү — функц дотор ОРОХГҮЙ |
| Step into | Дуудагдаж буй функц дотор орно |
| Step out | Одоогийн функцээс гарна |

Ихэнх үед `step over` хангалттай. Танихгүй функц рүү орж төөрөхөөс
болгоомжил.

### Нөхцөлт breakpoint

Мөрийн дугаар дээр баруун товшоод "Add conditional breakpoint" сонгоно:

```javascript
i === 42
```

1000 давталтын 42 дахь нь л сонирхолтой бол энэ нь цагийг маш их хэмнэнэ.

### Алдааг системтэй олох

1. **Давтан үүсгэ** — алдаа хэзээ гарч байгааг тодорхойл
2. **Нарийсга** — хамгийн бага кодоор давтан гаргаж үз
3. **Таамаглал дэвшүүл** — юу болж байж болох вэ
4. **Шалга** — нэг л зүйл өөрчлөөд үзнэ
5. **Засаад баталгаажуул** — зөвхөн засвар ажиллаж байгааг бус, өөр юу ч
   эвдрээгүйг шалга

Санамсаргүй кодоо өөрчлөх нь хамгийн удаан арга. Нэг удаад **нэг** зүйл
өөрчил.

Даалгаварт ажилладаг ч буруу хариу өгдөг програм байна — дээрх алхмуудаар
алдаануудыг нь нэг нэгээр нь олж засна.
""",
            initial_code="""\
// Энэ програм 4 алдаатай. Синтакс алдаа биш — код ажиллана, гэхдээ буруу
// хариу гаргана. Алдаа бүрийг олж, НЭГ удаад нэгийг засаарай.
//
// Туслах хэвлэлтийг console.info-гоор хийсэн: console дээр харагдана, гэхдээ
// гаралтад (тестэд) тооцогдохгүй. Хүсвэл өөрөө нэмээрэй.
// debugger; гэж бичвэл DevTools нээлттэй үед тэр мөрөнд зогсоно.

// Оролт: мөр бүр "<нэр> <дүн>"
const suralcagchid = [];
let mur = prompt();
while (mur !== null) {
  const [ner, dun] = mur.split(" ");
  suralcagchid.push({ ner, dun });
  mur = prompt();
}

console.info({ suralcagchid }); // юу уншигдсаныг харъя

function dundaj(jagsaalt) {
  let niit = 0;
  for (let i = 1; i < jagsaalt.length; i++) {
    niit += jagsaalt[i].dun;
  }
  return niit / jagsaalt.length;
}

function hamgiinUndur(jagsaalt) {
  let hamgiin = jagsaalt[0];
  for (const suralcagch of jagsaalt) {
    console.info(`шалгаж байна: ${suralcagch.ner} (${suralcagch.dun}) | одоогийн: ${hamgiin.ner}`);
    if (suralcagch.dun < hamgiin.dun) {
      hamgiin = suralcagch;
    }
  }
  return hamgiin;
}

function tentsegguinuud(jagsaalt) {
  return jagsaalt.filter((s) => s.dun <= 60).map((s) => s.ner);
}

const ur = hamgiinUndur(suralcagchid);
const unaasan = tentsegguinuud(suralcagchid);

console.log(`Суралцагч: ${suralcagchid.length}`);
console.log(`Дундаж: ${dundaj(suralcagchid).toFixed(2)}`);
console.log(`Хамгийн өндөр: ${ur.ner} (${ur.dun})`);
console.log(`Тэнцээгүй: ${unaasan.length > 0 ? unaasan.join(", ") : "байхгүй"}`);
""",
            exercise=ExerciseSpec(
                statement="""\
Эхлэл кодын програм суралцагчдын дүнгийн тайлан гаргадаг ч **4 алдаатай**.
Синтакс алдаа биш — код ажиллаад **буруу хариу** өгнө. Хичээлийн аргаар ол:
давтан үүсгэ, нарийсга, таамагла, шалга. Нэг удаад нэг л зүйл өөрчил.
Туслах хэвлэлтийг `console.info`-гоор хий — console дээр харагдана, гэхдээ
гаралтад тооцогдохгүй.

Зөв ажиллах програм:

- Оролтын мөр бүрээс нэр, дүнг уншина. Дүн нь **тоо**.
- Дундаж нь **бүх** суралцагчийн дүнгийн дундаж, 2 оронтой бутархайгаар.
- Хамгийн өндөр дүнтэйг олно; тэнцвэл жагсаалтад түрүүлж орсон нь.
- 60-аас **доош** дүнтэй нь тэнцээгүй — яг 60 бол тэнцсэн.

**Оролт:** мөр бүр `<нэр> <дүн>`, оролт дуустал (дор хаяж нэг мөр).

**Гаралт:**

```text
Суралцагч: <тоо>
Дундаж: <дундаж, 2 орон>
Хамгийн өндөр: <нэр> (<дүн>)
Тэнцээгүй: <нэрс ", "-ээр тусгаарлан, эсвэл байхгүй>
```

Тэнцээгүй нэрс оролтын дарааллаар; нэг ч байхгүй бол `Тэнцээгүй: байхгүй`.
""",
                tests=(
                    TestCaseSpec(
                        stdin="Бат 75\nСараа 92\nДорж 58\nОюун 88\n",
                        expected_output="Суралцагч: 4\nДундаж: 78.25\nХамгийн өндөр: Сараа (92)\nТэнцээгүй: Дорж\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="Анар 100\nБилгүүн 95\nЦэцэг 60\n",
                        expected_output="Суралцагч: 3\nДундаж: 85.00\nХамгийн өндөр: Анар (100)\nТэнцээгүй: байхгүй\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="Тэмүүлэн 45\n",
                        expected_output="Суралцагч: 1\nДундаж: 45.00\nХамгийн өндөр: Тэмүүлэн (45)\nТэнцээгүй: Тэмүүлэн\n",
                    ),
                    TestCaseSpec(
                        stdin="Сарнай 99\nОргил 70\nБат 59\nНомин 30\n",
                        expected_output="Суралцагч: 4\nДундаж: 64.50\nХамгийн өндөр: Сарнай (99)\nТэнцээгүй: Бат, Номин\n",
                    ),
                    TestCaseSpec(
                        stdin="Мөнх 80\nГэрэл 80\nЗаяа 61\n",
                        expected_output="Суралцагч: 3\nДундаж: 73.67\nХамгийн өндөр: Мөнх (80)\nТэнцээгүй: байхгүй\n",
                    ),
                ),
                solution="""\
const suralcagchid = [];
let mur = prompt();
while (mur !== null) {
  const [ner, dun] = mur.split(" ");
  // Алдаа 1: prompt() текст буцаана — тоо болгохгүй бол "75" + "92" = "7592"
  suralcagchid.push({ ner, dun: Number(dun) });
  mur = prompt();
}

function dundaj(jagsaalt) {
  let niit = 0;
  // Алдаа 2: индекс 0-ээс эхэлнэ — i = 1 бол эхний суралцагч алгасагдана
  for (let i = 0; i < jagsaalt.length; i++) {
    niit += jagsaalt[i].dun;
  }
  return niit / jagsaalt.length;
}

function hamgiinUndur(jagsaalt) {
  let hamgiin = jagsaalt[0];
  for (const suralcagch of jagsaalt) {
    // Алдаа 3: хамгийн ӨНДРИЙГ хайж байгаа тул >
    if (suralcagch.dun > hamgiin.dun) {
      hamgiin = suralcagch;
    }
  }
  return hamgiin;
}

function tentsegguinuud(jagsaalt) {
  // Алдаа 4: 60 оноо тэнцсэнд тооцогдоно — зөвхөн 60-аас доош нь унана
  return jagsaalt.filter((s) => s.dun < 60).map((s) => s.ner);
}

const ur = hamgiinUndur(suralcagchid);
const unaasan = tentsegguinuud(suralcagchid);

console.log(`Суралцагч: ${suralcagchid.length}`);
console.log(`Дундаж: ${dundaj(suralcagchid).toFixed(2)}`);
console.log(`Хамгийн өндөр: ${ur.ner} (${ur.dun})`);
console.log(`Тэнцээгүй: ${unaasan.length > 0 ? unaasan.join(", ") : "байхгүй"}`);
""",
                tips="""\
- Эхлээд жишээ тестийг ажиллуулж, аль мөр нь зөрж байгааг хар — тэндээс эхэл.
- `console.info({ suralcagchid })`-ийн гаралтыг хар: `dun` хашилттай
  (`"75"`) байна уу? `prompt()` үргэлж текст буцаадаг. `"75" + "92"` нь
  `"7592"`, `"100" < "95"` нь `true` (текстийг тэмдэгт тэмдэгтээр харьцуулна).
  Уншихдаа нэг удаа хөрвүүлбэл бусад функц бүгд засагдана.
- Давталт хаанаас эхэлж байна? Массивын эхний индекс хэд вэ?
- Харьцуулалтын чиглэл: хамгийн **их**-ийг хайж байхад `<` зөв үү? Тэнцвэл
  эхнийх нь үлдэх ёстой — `>` ба `>=`-ийн ялгааг бод.
- Хилийн утгыг шалга: яг 60 оноотой суралцагч тэнцэх үү?
- Засаад дууссаны дараа туслах хэвлэлт, `debugger`-ээ устга.
""",
            ),
        ),
    ],
)

TOOLING_MODULES = [MODULES, DEBUGGING]
