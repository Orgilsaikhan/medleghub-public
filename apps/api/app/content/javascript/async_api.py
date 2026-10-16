"""Модул 18-19 — Асинхрон JavaScript ба API.

АНХААР: Код ажиллуулагч нь сүлжээний хандалтыг бүрэн хаадаг (`fetch`,
`XMLHttpRequest` зэргийг устгасан). Тиймээс API-ийн хичээлүүдийн анхны код
нь `setTimeout` дээр суурилсан ХУУРАМЧ сервер ашиглана — хүсэлтийн хэлбэр,
алдаа боловсруулалт нь жинхэнэтэй яг адилхан.
"""

from app.content.types import ExerciseSpec, LessonSpec, ModuleSpec, TestCaseSpec

ASYNC = ModuleSpec(
    title="Модул 18 — Асинхрон JavaScript",
    description="Хүлээх шаардлагатай ажлыг зогсонгүй гүйцэтгэх.",
    lessons=[
        LessonSpec(
            title="Синхрон ба асинхрон",
            slug="sinhron-ba-asinhron",
            description="Нэг урсгал, callback, үйл явдлын гогцоо.",
            duration=450,
            content="""\
JavaScript нь **нэг урсгалтай** — нэг агшинд нэг л зүйл хийнэ.

### Синхрон код

Мөр бүр өмнөхөө дуусахыг хүлээнэ:

```javascript
console.log("нэг");
console.log("хоёр");
console.log("гурав");
// нэг, хоёр, гурав
```

Хэрэв нэг мөр удаан бол **бүх зүйл зогсоно** — товч дарагдахгүй, хуудас
гүйлгэгдэхгүй. Үүнийг "хөтөч царцлаа" гэж хэрэглэгч мэдэрнэ.

### Асинхрон код

Удаан ажлыг хүлээлгүйгээр цааш үргэлжилнэ:

```javascript
console.log("нэг");

setTimeout(() => {
  console.log("хоёр");
}, 1000);

console.log("гурав");
// нэг, гурав, хоёр
```

### Үйл явдлын гогцоо (event loop)

Асинхрон ажил бэлэн болоход түүний функц **дараалалд** орно. JavaScript
одоогийн ажлаа дуусгасны дараа дараалалаас дараагийнхыг авна.

```text
Үндсэн ажил дуусна
  → микро даалгавар (Promise)
  → макро даалгавар (setTimeout)
```

Тиймээс `setTimeout(fn, 0)` ч гэсэн **шууд** ажиллахгүй — одоогийн код
дуусахыг хүлээнэ.

### Callback

Асинхрон ажлын дараа юу хийхээ функцээр дамжуулна:

```javascript
function ugugdulAvah(butsaah) {
  setTimeout(() => {
    butsaah({ ner: "Бат" });
  }, 500);
}

ugugdulAvah((ugugdul) => {
  console.log(ugugdul.ner);
});
```

### Callback-ийн там

Хэд хэдэн ажлыг дараалуулбал код баруун тийш гүйнэ:

```javascript
a((ur1) => {
  b(ur1, (ur2) => {
    c(ur2, (ur3) => {
      // алдаа боловсруулалт нь хаана ч байхгүй
    });
  });
});
```

Үүнийг шийдэхийн тулд Promise зохиогдсон — дараагийн хичээл.

### Энэ сайт дээр ажиллуулахад

Энд код ажиллуулагч таны код дуусмагц зогсдог — түүнээс хойш ажиллах
`setTimeout`-ийн гаралт харагдахгүй. Хүлээлгэх аргыг «async / await»
хичээлд үзнэ. Даалгаварт `setTimeout`-ийн дарааллыг жижиг «гогцоо»
бичиж өөрсдөө дуурайна.
""",
            initial_code="""\
// setTimeout-ийн оронд ажлуудыг хадгалах дараалал
const daraalal = [];

// setTimeout(fn, ms)-тэй адил: fn-ийг ОДОО дуудахгүй, дараалалд хадгална.
function hojim(fn, ms) {
  // TODO: { fn, ms } объектыг daraalal-д нэм
}

// Үндсэн код дууссаны дараа дараалал дахь ажлуудыг ажиллуулна.
function gogtsoo() {
  // TODO: daraalal-ыг ms-ээр нь өсөхөөр эрэмбэл
  // TODO: ажил бүрийн fn-ийг дууд
}

const n = Number(prompt());

for (let i = 0; i < n; i++) {
  const hesguud = prompt().split(" ");

  if (hesguud[0] === "log") {
    console.log(hesguud.slice(1).join(" "));
  } else {
    const ms = Number(hesguud[1]);
    const tekst = hesguud.slice(2).join(" ");
    // TODO: tekst-ийг хэвлэдэг функцийг (callback) ms-тэй хамт hojim-д дамжуул
  }
}

// Үндсэн код дууслаа — одоо «гогцоо» дараалал руу орно.
gogtsoo();
""",
            exercise=ExerciseSpec(
                statement="""\
`setTimeout`-ийн дарааллыг ойлгохын тулд үйл явдлын гогцоог **өөрсдөө
дуурайя**. Эхлэл кодод `daraalal` массив бий. Хоёр функц бич:

- `hojim(fn, ms)` — `setTimeout(fn, ms)`-ийн орлуулга. `fn`-ийг **одоо
  дуудахгүй**, `{ fn, ms }` объект болгож `daraalal`-д нэмнэ.
- `gogtsoo()` — үндсэн код дууссаны дараа нэг удаа дуудагдана. Дараалал
  дахь ажлуудыг `ms`-ээр нь өсөх дарааллаар эрэмбэлж (ижил `ms`-тэй бол
  нэмсэн дарааллаараа), `fn` бүрийг дуудна.

Командуудыг уншдаг давталт бэлэн: `log` команд текстээ шууд хэвлэнэ.
`timeout` командын хувьд текстийг хэвлэдэг **callback** функцийг `hojim`-д
дамжуул.

**Оролт:** эхний мөрөнд командын тоо `n`, дараагийн `n` мөрөнд нэг нэг
команд. Текст нь зайтай байж болно:

```text
log <текст>
timeout <ms> <текст>
```

**Гаралт:** жинхэнэ JavaScript хэвлэх дарааллаар текстүүд, мөр бүрд нэг:
эхлээд бүх `log` оролтын дарааллаараа, дараа нь `timeout`-ууд хугацааныхаа
дарааллаар. `timeout 0` ч гэсэн синхрон кодын **дараа** гарна.
""",
                tests=(
                    TestCaseSpec(
                        stdin="4\nlog нэг\ntimeout 100 хоёр\nlog гурав\ntimeout 0 дөрөв\n",
                        expected_output="нэг\nгурав\nдөрөв\nхоёр\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="5\ntimeout 50 эхний\ntimeout 10 хурдан\nlog шууд\ntimeout 50 дараагийн\ntimeout 10 бас хурдан\n",
                        expected_output="шууд\nхурдан\nбас хурдан\nэхний\nдараагийн\n",
                    ),
                    TestCaseSpec(
                        stdin="3\ntimeout 300 C\ntimeout 200 B\ntimeout 100 A\n",
                        expected_output="A\nB\nC\n",
                    ),
                    TestCaseSpec(
                        stdin="4\ntimeout 0 setTimeout 0\nlog Эхлэл\ntimeout 0 бас 0\nlog Төгсгөл\n",
                        expected_output="Эхлэл\nТөгсгөл\nsetTimeout 0\nбас 0\n",
                    ),
                    TestCaseSpec(
                        stdin="3\nlog А\nlog Б\nlog В\n",
                        expected_output="А\nБ\nВ\n",
                    ),
                    TestCaseSpec(
                        stdin="1\ntimeout 1000 Ганцаараа хүлээлээ\n",
                        expected_output="Ганцаараа хүлээлээ\n",
                    ),
                ),
                solution="""\
const daraalal = [];

function hojim(fn, ms) {
  daraalal.push({ fn, ms });
}

function gogtsoo() {
  // sort нь ижил ms-тэй ажлуудын дарааллыг хадгална
  daraalal.sort((a, b) => a.ms - b.ms);
  for (const ajil of daraalal) {
    ajil.fn();
  }
}

const n = Number(prompt());

for (let i = 0; i < n; i++) {
  const hesguud = prompt().split(" ");

  if (hesguud[0] === "log") {
    console.log(hesguud.slice(1).join(" "));
  } else {
    const ms = Number(hesguud[1]);
    const tekst = hesguud.slice(2).join(" ");
    // Функцийг одоо биш, хожим дуудуулахаар дамжуулна
    hojim(() => console.log(tekst), ms);
  }
}

gogtsoo();
""",
                tips="""\
- **Callback** гэдэг нь «дараа нь дуудаарай» гэж дамжуулсан функц.
  `hojim(() => console.log(tekst), ms)` — `console.log(tekst)`-ийг шууд биш,
  сум функцэд ороож дамжуулна. `hojim(console.log(tekst), ms)` гэж бичвэл
  тэр дороо хэвлээд `undefined`-ийг дамжуулна.
- `hojim` дотор `fn`-ийг бүү дууд — зөвхөн `daraalal.push(...)`.
- `gogtsoo` дотор `sort((a, b) => a.ms - b.ms)` — тоогоор өсөхөөр. `sort`
  нь ижил утгатай элементүүдийн анхны дарааллыг хадгалдаг тул ижил `ms`
  асуудалгүй.
- Эрэмбэлсний дараа `for…of`-оор ажил бүрийн `fn()`-ийг дууд.
- `timeout 0` ч гэсэн синхрон код бүхэлдээ дууссаны дараа л ажилладаг —
  жинхэнэ `setTimeout(fn, 0)` яг ийм.
""",
            ),
        ),
        LessonSpec(
            title="Promise",
            slug="promise",
            description="Ирээдүйд ирэх утгыг илэрхийлэх объект.",
            duration=480,
            content="""\
**Promise** нь "хожим утга ирнэ" гэсэн амлалт.

### Гурван төлөв

| Төлөв | Утга |
|---|---|
| pending | Хүлээгдэж байна |
| fulfilled | Амжилттай дууссан |
| rejected | Амжилтгүй болсон |

Нэг удаа шийдэгдсэн Promise дахин өөрчлөгдөхгүй.

### Үүсгэх

```javascript
const amlalt = new Promise((resolve, reject) => {
  setTimeout(() => {
    resolve("бэлэн боллоо");
  }, 1000);
});
```

- `resolve(utga)` — амжилттай дуусгана
- `reject(aldaa)` — алдаатай дуусгана

### Хэрэглэх

```javascript
amlalt
  .then((utga) => console.log(utga))
  .catch((aldaa) => console.log("Алдаа:", aldaa.message))
  .finally(() => console.log("Дууслаа"));
```

### Гинжлэх

`then` нь шинэ Promise буцаадаг тул дараалуулж болно. Callback-ийн
тамаас ялгаатай нь код **доошоо** уншигдана:

```javascript
hereglegchAvah(1)
  .then((hereglegch) => zahialgaAvah(hereglegch.id))
  .then((zahialguud) => console.log(zahialguud.length))
  .catch((aldaa) => console.log("Хаана ч алдаа гарсан энд баригдана"));
```

Ганц `catch` нь гинжин хэлхээний **бүх** алдааг барина.

### Зэрэг ажиллуулах

`Promise.all` нь хэд хэдэн Promise-ийг зэрэг хүлээж, үр дүнгүүдийг нь
ижил дараалалтай массиваар өгнө:

```javascript
Promise.all([negAvah(), hoyorAvah()]).then(([a, b]) => {
  console.log(a, b);
});
```

| Метод | Зан төлөв |
|---|---|
| `Promise.all` | Бүгд амжилттай бол үр дүн. Нэг нь унавал шууд унана |
| `Promise.allSettled` | Бүгдийг хүлээнэ, тус бүрийн төлөвийг өгнө |
| `Promise.race` | Хамгийн түрүүнд дууссаных |
| `Promise.any` | Хамгийн түрүүнд **амжилттай** дууссаных |

Хоорондоо хамааралгүй хүсэлтүүдийг `Promise.all`-оор зэрэг явуулбал
хамаагүй хурдан болно.

### Энэ сайт дээр ажиллуулахад

Код ажиллуулагч таны кодыг функц дотор ажиллуулж, код дуусмагц зогсдог.
Хүлээгдэж буй Promise-ийн гаралт алдагдахгүйн тулд гинжээ хамгийн сүүлд
`return` хий:

```javascript
return amlalt.then((utga) => console.log(utga));
```

Энэ нь зөвхөн энэ сайтын онцлог — жинхэнэ файлд `return`-ийг функц дотор
л бичнэ. Дараагийн хичээлийн `await` үүнийг илүү энгийн болгоно.
""",
            initial_code="""\
// «Серверийн» өгөгдөл: id → нэр
const hereglegchid = {
  1: "Бат",
  2: "Сараа",
  3: "Дорж",
  4: "Оюун",
  5: "Тэмүүжин",
  6: "Номин",
};

// id-тай хэрэглэгчийн нэрийг хэсэг хүлээгээд өгдөг Promise буцаана.
function hereglegchAvah(id) {
  // TODO: new Promise((resolve, reject) => { ... }) буцаа.
  //   setTimeout-аар id * 3 мс хүлээгээд:
  //   - hereglegchid[id] байвал resolve(нэр)
  //   - байхгүй бол reject(new Error(`Хэрэглэгч ${id} олдсонгүй`))
}

const idnuud = prompt().split(" ").map(Number);

// TODO: Promise.all-оор бүх хэрэглэгчийг ЗЭРЭГ ав:
//   .then    — id бүрд "<id>. <нэр>", төгсгөлд "Нийт: <тоо> хэрэглэгч"
//   .catch   — "Алдаа: <мессеж>"
//   .finally — "Дууслаа"
// Код ажиллуулагч код дуусмагц зогсдог тул гинжээ return хий:
//   return Promise.all(...).then(...).catch(...).finally(...);
""",
            exercise=ExerciseSpec(
                statement="""\
Хэрэглэгчдийн нэрийг «серверээс» **зэрэг** татна.

1. `hereglegchAvah(id)`-г бич. Тэр нь `new Promise(...)` буцааж,
   `setTimeout`-аар бага зэрэг (`id * 3` мс) хүлээгээд:
   - `hereglegchid`-д `id` байвал нэрийг нь `resolve` хийнэ;
   - байхгүй бол `Хэрэглэгч <id> олдсонгүй` мессежтэй `Error`-оор
     `reject` хийнэ.
2. Оролтын бүх `id`-г `Promise.all`-оор зэрэг ав. Үр дүнг `.then`,
   алдааг `.catch`, төгсгөлийг `.finally`-аар хэвлэ.

Хүлээх хугацаа өөр өөр тул жижиг `id` түрүүлж ирнэ. Гэхдээ `Promise.all`-ийн
үр дүн **оролтын дарааллаараа** байдаг.

Код ажиллуулагч таны кодыг функц дотор ажиллуулж, код дуусмагц зогсдог.
Тиймээс гинжээ `return Promise.all(...)...` гэж **return** хий — тэгвэл
гинж дуустал хүлээнэ. (Дараагийн хичээлийн `await` үүнийг хялбар болгоно.)

**Оролт:** нэг мөрөнд зайгаар тусгаарласан `id`-ууд. Олдохгүй `id` нэгээс
олон байхгүй.

**Гаралт:** бүгд олдвол оролтын дарааллаар `<id>. <нэр>` мөрүүд, дараа нь
`Нийт: <тоо> хэрэглэгч`. Аль нэг нь олдохгүй бол зөвхөн `Алдаа: <мессеж>`.
Аль ч тохиолдолд хамгийн сүүлд `Дууслаа`:

```text
<id>. <нэр>
Нийт: <тоо> хэрэглэгч
Дууслаа
```
""",
                tests=(
                    TestCaseSpec(
                        stdin="1 3\n",
                        expected_output="1. Бат\n3. Дорж\nНийт: 2 хэрэглэгч\nДууслаа\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="2 7 4\n",
                        expected_output="Алдаа: Хэрэглэгч 7 олдсонгүй\nДууслаа\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="6 5 4 3 2 1\n",
                        expected_output="6. Номин\n5. Тэмүүжин\n4. Оюун\n3. Дорж\n2. Сараа\n1. Бат\nНийт: 6 хэрэглэгч\nДууслаа\n",
                    ),
                    TestCaseSpec(
                        stdin="4\n",
                        expected_output="4. Оюун\nНийт: 1 хэрэглэгч\nДууслаа\n",
                    ),
                    TestCaseSpec(
                        stdin="5 1 9\n",
                        expected_output="Алдаа: Хэрэглэгч 9 олдсонгүй\nДууслаа\n",
                    ),
                ),
                solution="""\
const hereglegchid = {
  1: "Бат",
  2: "Сараа",
  3: "Дорж",
  4: "Оюун",
  5: "Тэмүүжин",
  6: "Номин",
};

function hereglegchAvah(id) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const ner = hereglegchid[id];
      if (ner === undefined) {
        reject(new Error(`Хэрэглэгч ${id} олдсонгүй`));
      } else {
        resolve(ner);
      }
    }, id * 3);
  });
}

const idnuud = prompt().split(" ").map(Number);

// return — код ажиллуулагч гинж дуустал хүлээнэ
return Promise.all(idnuud.map((id) => hereglegchAvah(id)))
  .then((nernuud) => {
    // Promise.all-ийн үр дүн оролтын дарааллаар байна
    nernuud.forEach((ner, i) => {
      console.log(`${idnuud[i]}. ${ner}`);
    });
    console.log(`Нийт: ${nernuud.length} хэрэглэгч`);
  })
  .catch((aldaa) => {
    console.log(`Алдаа: ${aldaa.message}`);
  })
  .finally(() => {
    console.log("Дууслаа");
  });
""",
                tips="""\
- `new Promise((resolve, reject) => { ... })` дотор `setTimeout`-ыг дууд.
  Хугацаа дуусахад `resolve(ner)` эсвэл `reject(new Error(...))`-ийн **аль
  нэгийг** л дуудна.
- Нэр байхгүй эсэхийг `hereglegchid[id] === undefined`-ээр шалга.
- `idnuud.map((id) => hereglegchAvah(id))` нь Promise-уудын массив өгнө —
  түүнийг `Promise.all`-д өг.
- `.then((nernuud) => ...)` дахь `nernuud` нь оролтын дарааллаар байна —
  `forEach((ner, i) => ...)`-ийн `i`-гээр `idnuud[i]`-г ол.
- Нэг нь `reject` болбол `Promise.all` бүхэлдээ унаж, шууд `.catch` руу
  орно — `.then` огт ажиллахгүй.
- `.finally` нь амжилт, алдаанаас үл хамааран ажиллана.
- `return`-ийг мартвал код ажиллуулагч Promise дуусахыг хүлээлгүй зогсож,
  юу ч хэвлэгдэхгүй.
""",
            ),
        ),
        LessonSpec(
            title="async / await",
            slug="async-await",
            description="Асинхрон кодыг синхрон мэт бичих.",
            duration=480,
            content="""\
`async/await` нь Promise-ийн дээрх илүү уншигдахуйц бичлэг.

### `async` функц

`async` гэж тэмдэглэсэн функц нь **үргэлж Promise буцаана**:

```javascript
async function ner() {
  return "Бат";
}

ner().then((utga) => console.log(utga)); // "Бат"
```

### `await`

Promise шийдэгдэхийг хүлээгээд **утгыг нь** гаргаж авна:

```javascript
async function achaalah() {
  const hereglegch = await hereglegchAvah(1);
  const zahialguud = await zahialgaAvah(hereglegch.id);

  console.log(zahialguud.length);
}
```

Энэ нь `then` гинжтэй яг ижил ажиллана. Ялгаа нь зөвхөн уншигдац.

### Харьцуулалт

```javascript
// then
hereglegchAvah(1)
  .then((h) => zahialgaAvah(h.id))
  .then((z) => console.log(z.length));

// await
const h = await hereglegchAvah(1);
const z = await zahialgaAvah(h.id);
console.log(z.length);
```

### `await` хаана бичиж болох вэ

`async` функц дотор. Орчин үеийн модулиудад дээд түвшинд ч бичиж болно
(top-level await).

### Хэрэггүй хүлээлтээс сэргийл

Хоорондоо хамааралгүй ажлыг дараалуулж хүлээх нь цаг үрнэ:

```javascript
// Удаан — 600 ms
const a = await huleeh(200);
const b = await huleeh(200);
const c = await huleeh(200);

// Хурдан — 200 ms
const [a, b, c] = await Promise.all([huleeh(200), huleeh(200), huleeh(200)]);
```

Дараагийн ажил нь өмнөхийн үр дүнгээс **хамаарч байвал** л дараалуул.

### Давталт дотор

```javascript
// Ажиллана — дараалан
for (const id of idnuud) {
  const ugugdul = await avah(id);
}

// АЖИЛЛАХГҮЙ — forEach нь хүлээхгүй
idnuud.forEach(async (id) => {
  const ugugdul = await avah(id);
});
```

`forEach` нь буцаасан Promise-ийг үл тоомсорлодог тул давталт нь бүх
ажил дуусахаас өмнө "дуусна".
""",
            initial_code="""\
function huleeh(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// «Серверийн» өгөгдөл
const zahialguud = {
  101: { hereglegchId: 1, dun: 25000 },
  102: { hereglegchId: 2, dun: 12000 },
  103: { hereglegchId: 1, dun: 8500 },
  104: { hereglegchId: 3, dun: 40000 },
  105: { hereglegchId: 2, dun: 3000 },
  106: { hereglegchId: 4, dun: 15500 },
};
const hereglegchid = { 1: "Бат", 2: "Сараа", 3: "Дорж", 4: "Оюун" };

// Захиалга бүр өөр хугацаанд ирнэ — бүү өөрчил.
async function zahialgaAvah(id) {
  await huleeh((id % 4) * 5);
  return { id, ...zahialguud[id] };
}

async function hereglegchAvah(id) {
  await huleeh(3);
  return { id, ner: hereglegchid[id] };
}

// TODO: захиалгыг, дараа нь түүний hereglegchId-аар хэрэглэгчийг await-тэй ав.
//       { id, ner, dun } объект буцаа.
async function medeeAvah(id) {
  return { id, ner: "?", dun: 0 };
}

const idnuud = prompt().split(" ").map(Number);

// TODO: бүх захиалгыг Promise.all-оор ЗЭРЭГ ачаал (await), дараа нь хэвлэ:
//   #<id> <нэр>: <дүн>₮   (захиалга бүрд)
//   Нийт: <дүн>₮
""",
            exercise=ExerciseSpec(
                statement="""\
Захиалгуудын мэдээллийг `async/await`-оор ачаал. Эхлэл кодод хоёр
«серверийн» функц бэлэн, хоёулаа `async` тул `await`-тэй дуудна:

- `zahialgaAvah(id)` — `{ id, hereglegchId, dun }`;
- `hereglegchAvah(id)` — `{ id, ner }`.

1. `medeeAvah(id)`-г бөглө: эхлээд захиалгыг, дараа нь түүний
   `hereglegchId`-аар хэрэглэгчийг ав. Хоёр дахь хүсэлт нь эхнийхээс
   **хамаардаг** тул дараалуулна. `{ id, ner, dun }` объект буцаа.
2. Захиалгууд хоорондоо хамааралгүй тул бүгдийг `Promise.all`-оор **зэрэг**
   ачаал. Захиалга бүр өөр хугацаанд ирдэг ч үр дүнг **оролтын дарааллаар**
   хэвлэ.
3. Төгсгөлд бүх захиалгын нийт дүнг хэвлэ.

`forEach(async ...)` бүү ашигла — тэр нь хүлээдэггүй тул код ажиллуулагч
үр дүнг хэвлэхээс өмнө зогсоно.

**Оролт:** нэг мөрөнд зайгаар тусгаарласан захиалгын дугаарууд (бүгд
байгаа).

**Гаралт:** захиалга бүрд нэг мөр, төгсгөлд нийт дүн:

```text
#<id> <нэр>: <дүн>₮
Нийт: <дүн>₮
```
""",
                tests=(
                    TestCaseSpec(
                        stdin="101 102\n",
                        expected_output="#101 Бат: 25000₮\n#102 Сараа: 12000₮\nНийт: 37000₮\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="104\n",
                        expected_output="#104 Дорж: 40000₮\nНийт: 40000₮\n",
                    ),
                    TestCaseSpec(
                        stdin="106 105 104 103 102 101\n",
                        expected_output="#106 Оюун: 15500₮\n#105 Сараа: 3000₮\n#104 Дорж: 40000₮\n#103 Бат: 8500₮\n#102 Сараа: 12000₮\n#101 Бат: 25000₮\nНийт: 104000₮\n",
                    ),
                    TestCaseSpec(
                        stdin="103 101\n",
                        expected_output="#103 Бат: 8500₮\n#101 Бат: 25000₮\nНийт: 33500₮\n",
                    ),
                    TestCaseSpec(
                        stdin="105 106 102\n",
                        expected_output="#105 Сараа: 3000₮\n#106 Оюун: 15500₮\n#102 Сараа: 12000₮\nНийт: 30500₮\n",
                    ),
                ),
                solution="""\
function huleeh(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

const zahialguud = {
  101: { hereglegchId: 1, dun: 25000 },
  102: { hereglegchId: 2, dun: 12000 },
  103: { hereglegchId: 1, dun: 8500 },
  104: { hereglegchId: 3, dun: 40000 },
  105: { hereglegchId: 2, dun: 3000 },
  106: { hereglegchId: 4, dun: 15500 },
};
const hereglegchid = { 1: "Бат", 2: "Сараа", 3: "Дорж", 4: "Оюун" };

async function zahialgaAvah(id) {
  await huleeh((id % 4) * 5);
  return { id, ...zahialguud[id] };
}

async function hereglegchAvah(id) {
  await huleeh(3);
  return { id, ner: hereglegchid[id] };
}

async function medeeAvah(id) {
  // Хамааралтай: хэрэглэгчийн id-г захиалгаас л мэднэ
  const zahialga = await zahialgaAvah(id);
  const hereglegch = await hereglegchAvah(zahialga.hereglegchId);
  return { id: zahialga.id, ner: hereglegch.ner, dun: zahialga.dun };
}

const idnuud = prompt().split(" ").map(Number);

// Хамааралгүй: бүгдийг зэрэг явуулж, бүгд ирэхийг хүлээнэ
const medeenuud = await Promise.all(idnuud.map((id) => medeeAvah(id)));

for (const medee of medeenuud) {
  console.log(`#${medee.id} ${medee.ner}: ${medee.dun}₮`);
}

const niit = medeenuud.reduce((niilber, medee) => niilber + medee.dun, 0);
console.log(`Нийт: ${niit}₮`);
""",
                tips="""\
- `medeeAvah` дотор хоёр `await` дараалан: `const zahialga = await
  zahialgaAvah(id);`, дараа нь `zahialga.hereglegchId`-аар хэрэглэгчийг ав.
- `async` функц үргэлж Promise буцаадаг — `medeeAvah(5)`-ийн үр дүнг ч
  `await` хийж байж объект болно.
- `idnuud.map((id) => medeeAvah(id))` нь Promise-уудын массив.
  `await Promise.all(...)` нь бүгдийг зэрэг хүлээж, үр дүнг **оролтын
  дарааллаар** өгнө.
- Хэвлэхээ `Promise.all`-ийн дараа хий. `medeeAvah` дотроо хэвлэвэл хурдан
  ирсэн нь түрүүлж, дараалал алдагдана.
- Нийт дүнг `reduce`-ээр эсвэл давталтаар нэм.
""",
            ),
        ),
        LessonSpec(
            title="Асинхрон алдаа боловсруулах",
            slug="asinhron-aldaa",
            description="try/catch, барьж аваагүй promise, дахин оролдлого.",
            duration=480,
            content="""\
### `await` дээр `try/catch`

`await`-тай хамт энгийн `try/catch` ажиллана:

```javascript
async function achaalah() {
  try {
    const ugugdul = await avah();
    return ugugdul;
  } catch (aldaa) {
    console.log("Ачаалж чадсангүй:", aldaa.message);
    return null;
  }
}
```

Синхрон кодтой ижил харагдаж байгаа нь `async/await`-ийн гол давуу тал.

### Барьж аваагүй promise

`catch` байхгүй бол алдаа чимээгүй алга болно:

```javascript
avah(); // алдаа гарвал хаана ч харагдахгүй
```

Хөтөч үүнийг `unhandledrejection` болгож бүртгэдэг ч энэ нь сүүлчийн
хамгаалалт. Promise бүр `catch`-тай эсвэл `await`-тай байх ёстой.

### Хаана барих вэ

Алдааг **юу хийхээ мэддэг** газарт барь:

```javascript
// Доод давхарга — зөвхөн дамжуулна
async function avah(id) {
  const hariult = await huselt(`/api/hereglegch/${id}`);
  if (!hariult.ok) {
    throw new Error(`Хэрэглэгч ${id} олдсонгүй`);
  }
  return hariult.ugugdul;
}

// Дээд давхарга — хэрэглэгчид мэдэгдэнэ
try {
  const hereglegch = await avah(42);
  haruulah(hereglegch);
} catch (aldaa) {
  aldaaHaruulah(aldaa.message);
}
```

### Дахин оролдох

Сүлжээний алдаа түр зуурынх байдаг. Хэсэг хүлээгээд дахин оролдох нь
олон асуудлыг шийднэ:

```javascript
async function davtaj(ajil, oroldlogo = 3) {
  for (let i = 1; i <= oroldlogo; i++) {
    try {
      return await ajil();
    } catch (aldaa) {
      if (i === oroldlogo) throw aldaa;
      await huleeh(100 * 2 ** i); // тутамд хоёр дахин удаан хүлээнэ
    }
  }
}
```

Хүлээх хугацааг тутамд нэмэгдүүлэхийг *exponential backoff* гэнэ. Ингэж
хийхгүй бол унасан сервер рүү олон хүсэлт нэгэн зэрэг цохиж, байдлыг
улам дордуулна.

### Дахин оролдож болохгүй тохиолдол

Зөвхөн **түр зуурын** алдаанд дахин оролдоно. Буруу нууц үг, олдоогүй
хуудас зэрэг нь дахиад ч ижил үр дүн өгнө.
""",
            initial_code="""\
function huleeh(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// Түр зуурын (дахин оролдож болох) алдааны төрөл
class TurAldaa extends Error {
  constructor(messej) {
    super(messej);
    this.name = "TurAldaa";
  }
}

const hariunuud = prompt().split(" ");
const oroldlogo = Number(prompt());
let duudsanToo = 0;

// Тогтворгүй сервер: дуудах бүрд hariunuud-аас дараагийн хариуг өгнө — бүү өөрчил.
async function serverDuudah() {
  const hariu = hariunuud[duudsanToo] ?? "ok";
  duudsanToo++;
  await huleeh(2);
  if (hariu === "сүлжээ") {
    throw new TurAldaa("Сүлжээний алдаа");
  }
  if (hariu === "нууц") {
    throw new Error("Нууц үг буруу");
  }
  return "Өгөгдөл ирлээ";
}

// TODO: ajil-ийг дээд тал нь oroldlogo удаа оролдож дууд:
//   - амжилттай бол үр дүнг буцаа
//   - алдаа бүрд "Оролдлого <i>: <мессеж>" хэвлэ
//   - TurAldaa биш, эсвэл сүүлийн оролдлого бол алдааг дахин шид
//   - үгүй бол бага зэрэг хүлээгээд (await huleeh(5)) дахин оролд
async function davtaj(ajil, oroldlogo) {
  return await ajil();
}

// TODO: try/catch/finally:
//   амжилттай бол "Амжилттай: <үр дүн>", алдаа бол "Бүтэлгүйтлээ: <мессеж>",
//   finally дотор "Нийт дуудалт: <duudsanToo>"
const ur = await davtaj(serverDuudah, oroldlogo);
console.log(`Амжилттай: ${ur}`);
""",
            exercise=ExerciseSpec(
                statement="""\
Тогтворгүй сервер рүү **дахин оролдлоготой** хүсэлт явуул. Эхлэл кодод
`serverDuudah()` бэлэн — дуудах бүрд оролтод өгсөн дарааллаар хариулна:

| Хариу | Юу болох | Дахин оролдох уу |
|---|---|---|
| `сүлжээ` | `TurAldaa("Сүлжээний алдаа")` шиднэ | Тийм — түр зуурынх |
| `нууц` | `Error("Нууц үг буруу")` шиднэ | Үгүй — дахиад ч ижил |
| `ok` | `"Өгөгдөл ирлээ"` буцаана | — |

`async function davtaj(ajil, oroldlogo)`-г бөглө:

1. `ajil()`-ийг `await`-тэй дууд. Амжилттай бол үр дүнг буцаа.
2. Алдаа гарвал `Оролдлого <i>: <мессеж>` хэвлэ (`i` нь 1-ээс).
3. Алдаа нь `TurAldaa` биш, эсвэл энэ нь сүүлийн оролдлого бол алдааг
   дахин шид. Үгүй бол бага зэрэг хүлээгээд дахин оролд.

Дээд түвшинд `try/catch/finally`: амжилттай бол `Амжилттай: <үр дүн>`,
эцэст нь алдаа гарвал `Бүтэлгүйтлээ: <мессеж>`, үргэлж хамгийн сүүлд
`Нийт дуудалт: <тоо>` (`duudsanToo`).

**Оролт:** эхний мөрөнд серверийн хариунууд зайгаар тусгаарлагдсан, хоёр
дахь мөрөнд дээд тал нь хэдэн удаа оролдох тоо `oroldlogo` (1 ба түүнээс
их).

**Гаралт:**

```text
Оролдлого <i>: <мессеж>
Амжилттай: <үр дүн>
Нийт дуудалт: <тоо>
```

Эхний мөр нь алдаа бүрд давтагдана. Эцэст нь бүтэлгүйтвэл
`Амжилттай: ...`-ийн оронд `Бүтэлгүйтлээ: <мессеж>`.
""",
                tests=(
                    TestCaseSpec(
                        stdin="сүлжээ сүлжээ ok\n3\n",
                        expected_output="Оролдлого 1: Сүлжээний алдаа\nОролдлого 2: Сүлжээний алдаа\nАмжилттай: Өгөгдөл ирлээ\nНийт дуудалт: 3\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="нууц ok\n3\n",
                        expected_output="Оролдлого 1: Нууц үг буруу\nБүтэлгүйтлээ: Нууц үг буруу\nНийт дуудалт: 1\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="ok\n1\n",
                        expected_output="Амжилттай: Өгөгдөл ирлээ\nНийт дуудалт: 1\n",
                    ),
                    TestCaseSpec(
                        stdin="сүлжээ сүлжээ сүлжээ ok\n3\n",
                        expected_output="Оролдлого 1: Сүлжээний алдаа\nОролдлого 2: Сүлжээний алдаа\nОролдлого 3: Сүлжээний алдаа\nБүтэлгүйтлээ: Сүлжээний алдаа\nНийт дуудалт: 3\n",
                    ),
                    TestCaseSpec(
                        stdin="сүлжээ нууц ok\n5\n",
                        expected_output="Оролдлого 1: Сүлжээний алдаа\nОролдлого 2: Нууц үг буруу\nБүтэлгүйтлээ: Нууц үг буруу\nНийт дуудалт: 2\n",
                    ),
                    TestCaseSpec(
                        stdin="сүлжээ сүлжээ сүлжээ сүлжээ ok\n5\n",
                        expected_output="Оролдлого 1: Сүлжээний алдаа\nОролдлого 2: Сүлжээний алдаа\nОролдлого 3: Сүлжээний алдаа\nОролдлого 4: Сүлжээний алдаа\nАмжилттай: Өгөгдөл ирлээ\nНийт дуудалт: 5\n",
                    ),
                ),
                solution="""\
function huleeh(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

class TurAldaa extends Error {
  constructor(messej) {
    super(messej);
    this.name = "TurAldaa";
  }
}

const hariunuud = prompt().split(" ");
const oroldlogo = Number(prompt());
let duudsanToo = 0;

async function serverDuudah() {
  const hariu = hariunuud[duudsanToo] ?? "ok";
  duudsanToo++;
  await huleeh(2);
  if (hariu === "сүлжээ") {
    throw new TurAldaa("Сүлжээний алдаа");
  }
  if (hariu === "нууц") {
    throw new Error("Нууц үг буруу");
  }
  return "Өгөгдөл ирлээ";
}

async function davtaj(ajil, oroldlogo) {
  for (let i = 1; i <= oroldlogo; i++) {
    try {
      return await ajil();
    } catch (aldaa) {
      console.log(`Оролдлого ${i}: ${aldaa.message}`);
      // Байнгын алдаа эсвэл оролдлого дууссан — дээш нь дамжуулна
      if (!(aldaa instanceof TurAldaa) || i === oroldlogo) {
        throw aldaa;
      }
      // Тутамд арай удаан хүлээнэ
      await huleeh(2 * i);
    }
  }
}

try {
  const ur = await davtaj(serverDuudah, oroldlogo);
  console.log(`Амжилттай: ${ur}`);
} catch (aldaa) {
  console.log(`Бүтэлгүйтлээ: ${aldaa.message}`);
} finally {
  console.log(`Нийт дуудалт: ${duudsanToo}`);
}
""",
                tips="""\
- `for (let i = 1; i <= oroldlogo; i++)` дотор `try { return await ajil(); }`.
  `return` нь амжилттай болмогц давталтаас шууд гаргана.
- `return ajil();` гэж `await`-гүй бичвэл алдаа `try` дотор **баригдахгүй**
  — Promise нь функцээс гарсны дараа л унана.
- `catch (aldaa)` дотор эхлээд мессежийг хэвлэ, дараа нь шийд:
  `!(aldaa instanceof TurAldaa) || i === oroldlogo` бол `throw aldaa;`.
- Хүлээлтийг жижиг байлга (`await huleeh(2 * i)`) — тест хурдан дуусна.
- Дээд түвшний `finally` нь амжилт, алдаанаас үл хамааран ажилладаг тул
  «Нийт дуудалт»-ыг тэнд хэвлэ.
""",
            ),
        ),
    ],
)

APIS = ModuleSpec(
    title="Модул 19 — API ба HTTP",
    description="Сервертэй өгөгдөл солилцох.",
    lessons=[
        LessonSpec(
            title="API гэж юу вэ",
            slug="api-gej-yu-ve",
            description="HTTP-ийн үндэс, метод, статус код.",
            duration=450,
            content="""\
**API** (Application Programming Interface) нь хоёр програм хоорондоо
ярилцах гэрээ. Вэб дээр энэ нь ихэвчлэн HTTP хаягуудын цуглуулга.

```text
GET https://api.medleghub.mn/v1/courses
```

Хөтөч энэ хаяг руу хүсэлт явуулж, сервер JSON буцаана.

### HTTP хүсэлтийн бүтэц

| Хэсэг | Жишээ |
|---|---|
| Метод | `GET` |
| Хаяг | `/api/v1/courses` |
| Толгой (header) | `Content-Type: application/json` |
| Бие (body) | Зөвхөн `POST`, `PUT`, `PATCH`-д |

### Методууд

| Метод | Үйлдэл | Бие байх уу |
|---|---|---|
| `GET` | Унших | Үгүй |
| `POST` | Шинээр үүсгэх | Тийм |
| `PUT` | Бүтнээр солих | Тийм |
| `PATCH` | Хэсэгчлэн засах | Тийм |
| `DELETE` | Устгах | Үгүй |

`GET` нь юу ч **өөрчлөхгүй** байх ёстой. Энэ дүрмийг зөрчвөл хөтөч эсвэл
cache таны өгөгдлийг санамсаргүй өөрчилж болзошгүй.

### Статус код

Эхний цифр нь ангиллыг хэлнэ:

| Муж | Утга | Түгээмэл жишээ |
|---|---|---|
| 2xx | Амжилттай | 200 OK, 201 Created |
| 3xx | Шилжсэн | 301, 304 Not Modified |
| 4xx | **Client**-ийн алдаа | 400, 401, 403, 404 |
| 5xx | **Server**-ийн алдаа | 500, 503 |

4xx бол таны хүсэлт буруу. 5xx бол сервер эвдэрсэн — дахин оролдох нь
утга учиртай.

| Код | Утга |
|---|---|
| 400 | Хүсэлтийн өгөгдөл буруу |
| 401 | Нэвтрээгүй |
| 403 | Нэвтэрсэн ч эрх байхгүй |
| 404 | Олдсонгүй |
| 429 | Хэт олон хүсэлт |

401 ба 403-ын ялгааг сайн санаарай: эхнийх нь "чи хэн бэ?", хоёр дахь нь
"чамайг мэднэ, гэхдээ болохгүй".
""",
            initial_code="""\
// TODO: статус кодыг ангил (даалгаврын хүснэгтийг үз)
function angilah(status) {
  return "Тодорхойгүй";
}

const n = Number(prompt());
let amjilttai = 0;
let dahinOroldoh = 0;

for (let i = 0; i < n; i++) {
  const [method, hayag, statusText] = prompt().split(" ");
  const status = Number(statusText);
  const angilal = angilah(status);
  console.log(`${method} ${hayag}: ${status} ${angilal}`);
  // TODO: амжилттай (2xx) болон дахин оролдох (5xx) хүсэлтийг тоол
}

console.log(`Амжилттай: ${amjilttai}`);
console.log(`Дахин оролдох: ${dahinOroldoh}`);
""",
            exercise=ExerciseSpec(
                statement="""\
Серверийн хүсэлтийн бүртгэлийг (log) шинжил. Мөр бүрд метод, хаяг, статус
код байна. `angilah(status)` функцийг бичиж, статус бүрийг ангил:

| Статус | Ангилал |
|---|---|
| 200–299 | Амжилттай |
| 300–399 | Шилжсэн |
| 400–499 | Хүсэлтийн алдаа |
| 500–599 | Серверийн алдаа |
| бусад | Тодорхойгүй |

Мөн амжилттай хүсэлт болон **дахин оролдох** хүсэлтийг тоол. Серверийн алдаа
(5xx) түр зуурынх байж болох тул дахин оролдоно. Хүсэлтийн алдааг (4xx)
дахин оролдох утгагүй — хүсэлт өөрөө буруу.

**Оролт:** эхний мөрөнд хүсэлтийн тоо `n`, дараагийн `n` мөрөнд
`<метод> <хаяг> <статус>`.

**Гаралт:** хүсэлт бүрд нэг мөр, төгсгөлд хоёр тоо:

```text
<метод> <хаяг>: <статус> <ангилал>
Амжилттай: <тоо>
Дахин оролдох: <тоо>
```
""",
                tests=(
                    TestCaseSpec(
                        stdin="4\nGET /api/v1/courses 200\nPOST /api/v1/courses 201\nGET /api/v1/courses/99 404\nDELETE /api/v1/courses/1 503\n",
                        expected_output="GET /api/v1/courses: 200 Амжилттай\nPOST /api/v1/courses: 201 Амжилттай\nGET /api/v1/courses/99: 404 Хүсэлтийн алдаа\nDELETE /api/v1/courses/1: 503 Серверийн алдаа\nАмжилттай: 2\nДахин оролдох: 1\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="3\nGET /huuchin 301\nGET /logo.png 304\nPATCH /api/v1/me 401\n",
                        expected_output="GET /huuchin: 301 Шилжсэн\nGET /logo.png: 304 Шилжсэн\nPATCH /api/v1/me: 401 Хүсэлтийн алдаа\nАмжилттай: 0\nДахин оролдох: 0\n",
                    ),
                    TestCaseSpec(
                        stdin="5\nGET /api/v1/stats 500\nGET /api/v1/stats 502\nGET /api/v1/stats 200\nPUT /api/v1/courses/3 403\nPOST /api/v1/login 429\n",
                        expected_output="GET /api/v1/stats: 500 Серверийн алдаа\nGET /api/v1/stats: 502 Серверийн алдаа\nGET /api/v1/stats: 200 Амжилттай\nPUT /api/v1/courses/3: 403 Хүсэлтийн алдаа\nPOST /api/v1/login: 429 Хүсэлтийн алдаа\nАмжилттай: 1\nДахин оролдох: 2\n",
                    ),
                    TestCaseSpec(
                        stdin="3\nGET /api/v1/health 299\nGET /api/v1/ping 600\nHEAD /api/v1 399\n",
                        expected_output="GET /api/v1/health: 299 Амжилттай\nGET /api/v1/ping: 600 Тодорхойгүй\nHEAD /api/v1: 399 Шилжсэн\nАмжилттай: 1\nДахин оролдох: 0\n",
                    ),
                    TestCaseSpec(
                        stdin="1\nDELETE /api/v1/courses/7 599\n",
                        expected_output="DELETE /api/v1/courses/7: 599 Серверийн алдаа\nАмжилттай: 0\nДахин оролдох: 1\n",
                    ),
                ),
                solution="""\
function angilah(status) {
  if (status >= 200 && status <= 299) return "Амжилттай";
  if (status >= 300 && status <= 399) return "Шилжсэн";
  if (status >= 400 && status <= 499) return "Хүсэлтийн алдаа";
  if (status >= 500 && status <= 599) return "Серверийн алдаа";
  return "Тодорхойгүй";
}

const n = Number(prompt());
let amjilttai = 0;
let dahinOroldoh = 0;

for (let i = 0; i < n; i++) {
  const [method, hayag, statusText] = prompt().split(" ");
  const status = Number(statusText);
  const angilal = angilah(status);
  console.log(`${method} ${hayag}: ${status} ${angilal}`);

  if (angilal === "Амжилттай") amjilttai++;
  // Зөвхөн серверийн алдаа түр зуурынх байж болно
  if (angilal === "Серверийн алдаа") dahinOroldoh++;
}

console.log(`Амжилттай: ${amjilttai}`);
console.log(`Дахин оролдох: ${dahinOroldoh}`);
""",
                tips="""\
- Муж бүрийг `status >= 200 && status <= 299` гэх мэтээр шалгаад шууд
  `return` хий. Аль ч мужид ороогүй бол сүүлд нь `"Тодорхойгүй"`.
- Эхний цифр нь ангиллыг хэлдэг: 2 — амжилт, 3 — шилжсэн, 4 — таны
  (client) алдаа, 5 — серверийн алдаа.
- 429 (хэт олон хүсэлт) нь 4xx — энэ даалгаварт дахин оролдохгүй.
- Тоологчдыг давталт дотор `angilah`-ийн үр дүнгээр нэмэгдүүл.
""",
            ),
        ),
        LessonSpec(
            title="fetch ба GET хүсэлт",
            slug="fetch-ba-get",
            description="Сервер рүү хүсэлт явуулж, хариуг унших.",
            duration=480,
            content="""\
`fetch` нь хөтчийн суурьт HTTP хүсэлт явуулах функц. Promise буцаана.

```javascript
const hariult = await fetch("https://api.medleghub.mn/v1/courses");
const ugugdul = await hariult.json();

console.log(ugugdul);
```

### Хоёр удаа `await` хийх нь яагаад вэ

1. Эхнийх нь **толгой** ирэхийг хүлээнэ
2. Дараагийнх нь **бие** бүрэн татагдаж, JSON болж хөрвөхийг хүлээнэ

### `ok`-ийг ЗААВАЛ шалга

Энэ бол хамгийн олон давтагддаг алдаа:

> `fetch` нь 404 эсвэл 500 хариу ирэхэд **алдаа шидэхгүй**. Сервер хариу
> өгсөн тул хүсэлт нь "амжилттай" гэж тооцогдоно.

```javascript
const hariult = await fetch(hayag);

if (!hariult.ok) {
  throw new Error(`Хүсэлт амжилтгүй: ${hariult.status}`);
}

const ugugdul = await hariult.json();
```

`fetch` нь зөвхөн сүлжээ **огт** холбогдоогүй үед л алдаа шиднэ.

### Хайлтын параметр

Гараар мөр нийлүүлэхийн оронд:

```javascript
const parametr = new URLSearchParams({ haih: "js", huudas: 2 });
const hariult = await fetch(`/api/v1/courses?${parametr}`);
```

Ингэснээр тусгай тэмдэгтүүд зөв кодлогдоно.

### Толгой нэмэх

```javascript
const hariult = await fetch(hayag, {
  headers: { Authorization: `Bearer ${token}` },
});
```

### CORS

Өөр домэйн рүү хүсэлт явуулахад сервер зөвшөөрөл өгөх ёстой. Зөвшөөрөөгүй
бол хөтөч хариуг **хааж**, console дээр CORS алдаа гарна.

Энэ нь таны кодын алдаа биш — серверийн тохиргоо. Сервер тал дээр
`Access-Control-Allow-Origin` толгойг нэмж засна.
""",
            initial_code="""\
// Сүлжээ хаалттай тул хуурамч сервер бичье — бүү өөрчил. Хэлбэр нь жинхэнэ
// fetch-тэй адил: ok, status, json() бүхий хариу объект буцаана.
const surgaltuud = [
  { id: 1, ner: "JavaScript үндэс", hicheel: 71 },
  { id: 2, ner: "Python-оор програмчлал", hicheel: 44 },
  { id: 3, ner: "HTML ба CSS", hicheel: 30 },
  { id: 4, ner: "Өгөгдлийн сан", hicheel: 87 },
];

function hariuUusgeh(status, bie) {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: async () => JSON.parse(JSON.stringify(bie)),
  };
}

async function fetch(hayag) {
  await new Promise((resolve) => setTimeout(resolve, 2));
  const id = hayag.replace("/api/v1/courses/", "");
  // 5-р сургалт дээр сервер «эвдэрсэн»
  if (id === "5") {
    return hariuUusgeh(500, { message: "Серверийн алдаа" });
  }
  const surgalt = surgaltuud.find((s) => String(s.id) === id);
  if (surgalt === undefined) {
    return hariuUusgeh(404, { message: "Олдсонгүй" });
  }
  return hariuUusgeh(200, surgalt);
}

// TODO: hariult.ok биш бол `Хүсэлт амжилтгүй: <status>` мессежтэй алдаа шид.
//       ok-ийг шалгахгүй бол 404-ийг ч амжилт гэж ойлгоно!
async function avah(hayag) {
  const hariult = await fetch(hayag);
  return hariult.json();
}

const idnuud = prompt().split(" ");
let amjilttai = 0;

for (const id of idnuud) {
  // TODO: try/catch дотор avah(`/api/v1/courses/${id}`)-ийг await-тэй дууд:
  //   амжилттай бол "<id>. <нэр>: <тоо> хичээл" хэвлээд amjilttai-г нэм,
  //   алдаа бол "Алдаа (<id>): <мессеж>" хэвлэ.
}

console.log(`Амжилттай: ${amjilttai} / ${idnuud.length}`);
""",
            exercise=ExerciseSpec(
                statement="""\
Сургалтуудын дэлгэрэнгүйг `fetch`-ээр татна. Эхлэл кодод хуурамч `fetch`
бэлэн: `/api/v1/courses/<id>` хаягаар `ok`, `status`, `json()` бүхий хариу
өгнө. Олдоогүй сургалтад `404`, 5-р сургалтад `500` буцаана.

1. `avah(hayag)`-г засаж, `hariult.ok` худал бол
   `Хүсэлт амжилтгүй: <status>` мессежтэй алдаа шид. Үгүй бол
   `hariult.json()`-ийг буцаа.
2. Оролтын `id` бүрээр **дарааллаар** `avah`-ийг дуудаж, үр дүн эсвэл
   алдааг хэвлэ.
3. Төгсгөлд хэдэн хүсэлт амжилттай болсныг хэвлэ.

`fetch` нь 404, 500 хариунд алдаа **шидэхгүй** — `ok`-ийг өөрөө шалгана.

**Оролт:** нэг мөрөнд зайгаар тусгаарласан сургалтын `id`-ууд.

**Гаралт:** `id` бүрд нэг мөр, төгсгөлд дүн:

```text
<id>. <нэр>: <хичээлийн тоо> хичээл
Алдаа (<id>): Хүсэлт амжилтгүй: <status>
Амжилттай: <тоо> / <нийт>
```
""",
                tests=(
                    TestCaseSpec(
                        stdin="1 3\n",
                        expected_output="1. JavaScript үндэс: 71 хичээл\n3. HTML ба CSS: 30 хичээл\nАмжилттай: 2 / 2\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="2 9\n",
                        expected_output="2. Python-оор програмчлал: 44 хичээл\nАлдаа (9): Хүсэлт амжилтгүй: 404\nАмжилттай: 1 / 2\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="5 4\n",
                        expected_output="Алдаа (5): Хүсэлт амжилтгүй: 500\n4. Өгөгдлийн сан: 87 хичээл\nАмжилттай: 1 / 2\n",
                    ),
                    TestCaseSpec(
                        stdin="abc\n",
                        expected_output="Алдаа (abc): Хүсэлт амжилтгүй: 404\nАмжилттай: 0 / 1\n",
                    ),
                    TestCaseSpec(
                        stdin="4 3 2 1\n",
                        expected_output="4. Өгөгдлийн сан: 87 хичээл\n3. HTML ба CSS: 30 хичээл\n2. Python-оор програмчлал: 44 хичээл\n1. JavaScript үндэс: 71 хичээл\nАмжилттай: 4 / 4\n",
                    ),
                    TestCaseSpec(
                        stdin="0 1 5 12\n",
                        expected_output="Алдаа (0): Хүсэлт амжилтгүй: 404\n1. JavaScript үндэс: 71 хичээл\nАлдаа (5): Хүсэлт амжилтгүй: 500\nАлдаа (12): Хүсэлт амжилтгүй: 404\nАмжилттай: 1 / 4\n",
                    ),
                ),
                solution="""\
const surgaltuud = [
  { id: 1, ner: "JavaScript үндэс", hicheel: 71 },
  { id: 2, ner: "Python-оор програмчлал", hicheel: 44 },
  { id: 3, ner: "HTML ба CSS", hicheel: 30 },
  { id: 4, ner: "Өгөгдлийн сан", hicheel: 87 },
];

function hariuUusgeh(status, bie) {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: async () => JSON.parse(JSON.stringify(bie)),
  };
}

async function fetch(hayag) {
  await new Promise((resolve) => setTimeout(resolve, 2));
  const id = hayag.replace("/api/v1/courses/", "");
  if (id === "5") {
    return hariuUusgeh(500, { message: "Серверийн алдаа" });
  }
  const surgalt = surgaltuud.find((s) => String(s.id) === id);
  if (surgalt === undefined) {
    return hariuUusgeh(404, { message: "Олдсонгүй" });
  }
  return hariuUusgeh(200, surgalt);
}

async function avah(hayag) {
  // 1-р await — хариуны толгой
  const hariult = await fetch(hayag);

  // fetch нь 404/500-д алдаа шидэхгүй — өөрсдөө шалгана
  if (!hariult.ok) {
    throw new Error(`Хүсэлт амжилтгүй: ${hariult.status}`);
  }

  // 2-р await — бие (JSON)
  return await hariult.json();
}

const idnuud = prompt().split(" ");
let amjilttai = 0;

for (const id of idnuud) {
  try {
    const surgalt = await avah(`/api/v1/courses/${id}`);
    console.log(`${surgalt.id}. ${surgalt.ner}: ${surgalt.hicheel} хичээл`);
    amjilttai++;
  } catch (aldaa) {
    console.log(`Алдаа (${id}): ${aldaa.message}`);
  }
}

console.log(`Амжилттай: ${amjilttai} / ${idnuud.length}`);
""",
                tips="""\
- `avah` дотор `fetch`-ийн дараа, `json()`-оос **өмнө**
  `if (!hariult.ok) throw new Error(...)` бич. Мессежид
  `hariult.status`-ыг оруул.
- `ok`-ийг шалгахгүй бол 404-ийн хариу `{ message: "Олдсонгүй" }` нь
  сургалт мэт хэвлэгдэж, `undefined. undefined` гарна.
- Хоёр `await`: эхнийх нь `fetch`-ийг, хоёр дахь нь `hariult.json()`-ийг
  хүлээнэ.
- `for…of` дотор `try/catch` бичвэл нэг хүсэлт унасан ч дараагийнх нь
  үргэлжилнэ.
- `id` нь текст хэвээр байж болно — хаягт `${id}`-ээр оруулна.
""",
            ),
        ),
        LessonSpec(
            title="POST хүсэлт ба JSON",
            slug="post-husel-ba-json",
            description="Сервер рүү өгөгдөл илгээх.",
            duration=480,
            content="""\
### POST хүсэлт

```javascript
const hariult = await fetch("/api/v1/courses", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ ner: "Шинэ сургалт" }),
});

const uussen = await hariult.json();
```

Гурван зүйлийг бүү мартаарай:

1. `method: "POST"`
2. `Content-Type` толгой — эс бөгөөс сервер биеийг JSON гэж танихгүй
3. `JSON.stringify` — объектыг шууд өгвөл `[object Object]` болно

### JSON гэдэг нь юу вэ

Сүлжээгээр зөвхөн **текст** дамждаг. JSON бол объектыг текст болгох
стандарт арга:

```javascript
JSON.stringify({ ner: "Бат" }); // '{"ner":"Бат"}'
JSON.parse('{"ner":"Бат"}');    // { ner: "Бат" }
```

`hariult.json()` нь үнэндээ текстийг татаад `JSON.parse` хийж байгаа хэрэг.

### Хариуны статус

Амжилттай үүсгэсэн бол сервер `201 Created` буцаах ёстой. `200` ч
тааралдана — хоёулаа амжилт.

### Форм илгээх бүтэн жишээ

```javascript
form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const ugugdul = Object.fromEntries(new FormData(form));

  try {
    const hariult = await fetch("/api/v1/burtgel", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(ugugdul),
    });

    if (!hariult.ok) {
      const aldaa = await hariult.json();
      throw new Error(aldaa.message);
    }

    console.log("Амжилттай");
  } catch (aldaa) {
    aldaaHaruulah(aldaa.message);
  }
});
```

### Давхар илгээхээс сэргийл

Хэрэглэгч товчийг хоёр удаа дарвал хоёр бичлэг үүснэ. Хүсэлт явж байх
хугацаанд товчийг унтраа:

```javascript
tovch.disabled = true;
try {
  await ilgeeh();
} finally {
  tovch.disabled = false;
}
```

`finally` дотор буцааж асаах нь чухал — алдаа гарсан ч товч гацахгүй.
""",
            initial_code="""\
// Хуурамч сервер: POST-ийг жинхэнэ API шиг шалгаад хадгална — бүү өөрчил.
const suuri = [];
let daraagiinId = 1;

function hariuUusgeh(status, bie) {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: async () => JSON.parse(JSON.stringify(bie)),
  };
}

async function fetch(hayag, tohirgoo = {}) {
  await new Promise((resolve) => setTimeout(resolve, 2));
  if (hayag !== "/api/v1/courses") {
    return hariuUusgeh(404, { message: "Олдсонгүй" });
  }
  const method = (tohirgoo.method ?? "GET").toUpperCase();
  if (method === "GET") {
    return hariuUusgeh(200, suuri);
  }
  if (method !== "POST") {
    return hariuUusgeh(405, { message: "Зөвшөөрөгдөөгүй метод" });
  }
  const headers = tohirgoo.headers ?? {};
  const turul = Object.keys(headers).find((ner) => ner.toLowerCase() === "content-type");
  if (turul === undefined || headers[turul] !== "application/json") {
    return hariuUusgeh(415, { message: "Content-Type нь application/json байх ёстой" });
  }
  let ugugdul;
  try {
    ugugdul = JSON.parse(tohirgoo.body);
  } catch (aldaa) {
    return hariuUusgeh(400, { message: "Бие нь JSON биш" });
  }
  if (typeof ugugdul?.ner !== "string" || ugugdul.ner.trim() === "") {
    return hariuUusgeh(400, { message: "Нэр заавал шаардлагатай" });
  }
  if (typeof ugugdul.une !== "number" || ugugdul.une < 0) {
    return hariuUusgeh(400, { message: "Үнэ буруу" });
  }
  const uussen = { id: daraagiinId++, ner: ugugdul.ner.trim(), une: ugugdul.une };
  suuri.push(uussen);
  return hariuUusgeh(201, uussen);
}

// TODO: method, headers ("Content-Type": "application/json"), body-г зөв өг.
//       Хариуны JSON-ийг уншаад ok биш бол `<status>: <message>` мессежтэй
//       алдаа шид, үгүй бол үүссэн сургалтыг буцаа.
async function surgaltUusgeh(ner, une) {
  const hariult = await fetch("/api/v1/courses", {
    method: "POST",
    body: { ner, une },
  });
  return hariult.json();
}

const n = Number(prompt());

for (let i = 0; i < n; i++) {
  const [ner, uneText] = prompt().split(";");
  // TODO: try/catch дотор surgaltUusgeh(ner, Number(uneText))-ийг await-тэй дууд:
  //   амжилттай бол "Үүслээ: #<id> <нэр> (<үнэ>₮)", алдаа бол "Алдаа <мессеж>"
}

// TODO: GET хүсэлтээр бүх сургалтыг аваад "Санд <тоо> сургалт байна" хэвлэ
""",
            exercise=ExerciseSpec(
                statement="""\
Шинэ сургалтуудыг сервер рүү `POST` хүсэлтээр илгээ. Эхлэл кодод хуурамч
`fetch` бэлэн — жинхэнэ API шиг шалгана:

| Нөхцөл | Хариу |
|---|---|
| `Content-Type: application/json` толгой алга | `415` |
| Бие нь JSON текст биш (`JSON.stringify` мартсан) | `400` «Бие нь JSON биш» |
| Нэр хоосон | `400` «Нэр заавал шаардлагатай» |
| Үнэ тоо биш эсвэл сөрөг | `400` «Үнэ буруу» |
| Бүх зүйл зөв | `201` + үүссэн сургалт `{ id, ner, une }` |

Алдааны үед хариуны JSON нь `{ message }` байна. Сервер нэрийн хоёр талын
зайг өөрөө тайрна.

1. `surgaltUusgeh(ner, une)`-г зас: `method: "POST"`, `Content-Type`
   толгой, `JSON.stringify`-аар хөрвүүлсэн `{ ner, une }` бие. Хариу `ok`
   биш бол `<status>: <message>` мессежтэй алдаа шид.
2. Оролтын мөр бүрээр сургалт үүсгэж, үр дүн эсвэл алдааг хэвлэ. Үнийг
   `Number()`-ээр тоо болго.
3. Төгсгөлд `GET` хүсэлтээр (`fetch("/api/v1/courses")`) санд хэдэн
   сургалт байгааг хэвлэ.

**Оролт:** эхний мөрөнд тоо `n`, дараагийн `n` мөрөнд `<нэр>;<үнэ>`.

**Гаралт:** мөр бүрд нэг мөр, төгсгөлд нийт тоо:

```text
Үүслээ: #<id> <нэр> (<үнэ>₮)
Алдаа <status>: <message>
Санд <тоо> сургалт байна
```
""",
                tests=(
                    TestCaseSpec(
                        stdin="3\nReact;25000\n;5000\nTypeScript;30000\n",
                        expected_output="Үүслээ: #1 React (25000₮)\nАлдаа 400: Нэр заавал шаардлагатай\nҮүслээ: #2 TypeScript (30000₮)\nСанд 2 сургалт байна\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="1\nNode.js;0\n",
                        expected_output="Үүслээ: #1 Node.js (0₮)\nСанд 1 сургалт байна\n",
                    ),
                    TestCaseSpec(
                        stdin="2\nVue;үнэгүй\nSvelte;-100\n",
                        expected_output="Алдаа 400: Үнэ буруу\nАлдаа 400: Үнэ буруу\nСанд 0 сургалт байна\n",
                    ),
                    TestCaseSpec(
                        stdin="4\nHTML ба CSS;15000\n   ;100\nPython;19900\nGit;9900\n",
                        expected_output="Үүслээ: #1 HTML ба CSS (15000₮)\nАлдаа 400: Нэр заавал шаардлагатай\nҮүслээ: #2 Python (19900₮)\nҮүслээ: #3 Git (9900₮)\nСанд 3 сургалт байна\n",
                    ),
                    TestCaseSpec(
                        stdin="2\n  Angular  ;12000\nJava\n",
                        expected_output="Үүслээ: #1 Angular (12000₮)\nАлдаа 400: Үнэ буруу\nСанд 1 сургалт байна\n",
                    ),
                ),
                solution="""\
const suuri = [];
let daraagiinId = 1;

function hariuUusgeh(status, bie) {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: async () => JSON.parse(JSON.stringify(bie)),
  };
}

async function fetch(hayag, tohirgoo = {}) {
  await new Promise((resolve) => setTimeout(resolve, 2));
  if (hayag !== "/api/v1/courses") {
    return hariuUusgeh(404, { message: "Олдсонгүй" });
  }
  const method = (tohirgoo.method ?? "GET").toUpperCase();
  if (method === "GET") {
    return hariuUusgeh(200, suuri);
  }
  if (method !== "POST") {
    return hariuUusgeh(405, { message: "Зөвшөөрөгдөөгүй метод" });
  }
  const headers = tohirgoo.headers ?? {};
  const turul = Object.keys(headers).find((ner) => ner.toLowerCase() === "content-type");
  if (turul === undefined || headers[turul] !== "application/json") {
    return hariuUusgeh(415, { message: "Content-Type нь application/json байх ёстой" });
  }
  let ugugdul;
  try {
    ugugdul = JSON.parse(tohirgoo.body);
  } catch (aldaa) {
    return hariuUusgeh(400, { message: "Бие нь JSON биш" });
  }
  if (typeof ugugdul?.ner !== "string" || ugugdul.ner.trim() === "") {
    return hariuUusgeh(400, { message: "Нэр заавал шаардлагатай" });
  }
  if (typeof ugugdul.une !== "number" || ugugdul.une < 0) {
    return hariuUusgeh(400, { message: "Үнэ буруу" });
  }
  const uussen = { id: daraagiinId++, ner: ugugdul.ner.trim(), une: ugugdul.une };
  suuri.push(uussen);
  return hariuUusgeh(201, uussen);
}

async function surgaltUusgeh(ner, une) {
  const hariult = await fetch("/api/v1/courses", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ner, une }),
  });

  const ugugdul = await hariult.json();
  if (!hariult.ok) {
    throw new Error(`${hariult.status}: ${ugugdul.message}`);
  }
  return ugugdul;
}

const n = Number(prompt());

for (let i = 0; i < n; i++) {
  const [ner, uneText] = prompt().split(";");
  try {
    const surgalt = await surgaltUusgeh(ner, Number(uneText));
    console.log(`Үүслээ: #${surgalt.id} ${surgalt.ner} (${surgalt.une}₮)`);
  } catch (aldaa) {
    console.log(`Алдаа ${aldaa.message}`);
  }
}

const hariult = await fetch("/api/v1/courses");
const buh = await hariult.json();
console.log(`Санд ${buh.length} сургалт байна`);
""",
                tips="""\
- `fetch`-ийн хоёр дахь аргумент: `{ method: "POST", headers: {
  "Content-Type": "application/json" }, body: JSON.stringify({ ner, une }) }`.
- Объектыг `body`-д шууд өгвөл `[object Object]` текст болж, сервер JSON
  гэж танихгүй.
- Алдааны хариунд ч JSON бие байдаг — эхлээд `await hariult.json()`
  уншаад, дараа нь `ok`-ийг шалгаж `message`-ийг алдаанд оруул.
- `Number("үнэгүй")` нь `NaN`, харин `JSON.stringify` нь `NaN`-ийг `null`
  болгодог — сервер «Үнэ буруу» гэж хариулна. Үүнийг өөрөө шалгах
  шаардлагагүй.
- Хэвлэхдээ оролтын биш, **серверийн буцаасан** нэр, `id`-г ашигла.
- Сүүлийн `GET`-д тохиргоо хэрэггүй — `method` өгөөгүй бол `GET`.
""",
            ),
        ),
        LessonSpec(
            title="API-ийн алдаа боловсруулах",
            slug="api-aldaa-bolovsruulah",
            description="Ачаалж буй, алдаатай, хоосон гурван төлөв.",
            duration=480,
            content="""\
Сервертэй ажиллах код нь зөвхөн амжилтын зам биш **дөрвөн төлөвийг**
бүгдийг нь зохицуулах ёстой.

| Төлөв | Хэрэглэгч юу харах вэ |
|---|---|
| Ачаалж байна | Эргэлдэгч тэмдэг эсвэл араг яс |
| Алдаа гарсан | Ойлгомжтой мессеж, дахин оролдох товч |
| Хоосон ирсэн | "Одоогоор бичлэг алга" |
| Өгөгдөлтэй | Жинхэнэ агуулга |

Ихэнх шинэ хөгжүүлэгч зөвхөн сүүлчийнхийг бичдэг. Үлдсэн гурав нь
хэрэглэгчийн бодит амьдралд илүү олон тааралдана.

### Төлөвийг ил болгох

```javascript
let tuluv = "achaalj"; // "achaalj" | "aldaa" | "beleen"
let ugugdul = null;
let aldaa = null;

async function achaalah() {
  tuluv = "achaalj";
  zurah();

  try {
    ugugdul = await avah("/api/v1/courses");
    tuluv = "beleen";
  } catch (aldaanii) {
    aldaa = aldaanii.message;
    tuluv = "aldaa";
  }

  zurah();
}
```

### Хугацаа хэтрэх

`fetch` нь өөрөө хугацаа хязгаарладаггүй — сервер хариу өгөхгүй бол
мөнхөд хүлээнэ. `AbortController` ашиглана:

```javascript
const hyanagch = new AbortController();
setTimeout(() => hyanagch.abort(), 5000);

const hariult = await fetch(hayag, { signal: hyanagch.signal });
```

### Алдааг хэрэглэгчийн хэлээр

Техникийн мессежийг шууд бүү харуул:

| Дотоод | Хэрэглэгчид |
|---|---|
| `500 Internal Server Error` | "Сервер түр ажиллахгүй байна. Хэсэг хүлээгээд дахин оролдоно уу." |
| `401 Unauthorized` | "Нэвтрэх хугацаа дууслаа. Дахин нэвтэрнэ үү." |
| `Failed to fetch` | "Интернэт холболтоо шалгана уу." |

Дэлгэрэнгүйг console-д бүртгэ, хэрэглэгчид ойлгомжтойг харуул.

### Дахин оролдох товч

Алдааны мессежтэй хамт үйлдэл санал болго. "Алдаа гарлаа" гэсэн ганц
мөр нь хэрэглэгчийг гарцгүй болгоно.
""",
            initial_code="""\
function huleeh(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// Хуурамч сервер — бүү өөрчил. Оролтын мөр бүр нэг хүсэлтийн хариу:
//   "200 Бат Сараа" — амжилттай (нэргүй бол хоосон жагсаалт)
//   "401", "503" … — тухайн статустай алдааны хариу
//   "холболтгүй"   — fetch өөрөө TypeError шиднэ
//   "удаан"        — сервер 300 мс хариулахгүй (signal-аар тасалж болно)
const serveriinHariunuud = [];
let muur = prompt();
while (muur !== null) {
  serveriinHariunuud.push(muur);
  muur = prompt();
}
let dugaar = 0;

function hariuUusgeh(status, bie) {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: async () => JSON.parse(JSON.stringify(bie)),
  };
}

async function fetch(hayag, tohirgoo = {}) {
  const [kod, ...nernuud] = serveriinHariunuud[dugaar].split(" ");
  dugaar++;
  if (kod === "холболтгүй") {
    await huleeh(2);
    throw new TypeError("Failed to fetch");
  }
  await new Promise((resolve, reject) => {
    const tsag = setTimeout(resolve, kod === "удаан" ? 300 : 2);
    tohirgoo.signal?.addEventListener("abort", () => {
      clearTimeout(tsag);
      const aldaa = new Error("The operation was aborted.");
      aldaa.name = "AbortError";
      reject(aldaa);
    });
  });
  if (kod === "удаан") {
    return hariuUusgeh(200, [{ id: 1, ner: "Удаан" }]);
  }
  const status = Number(kod);
  if (status === 200) {
    return hariuUusgeh(200, nernuud.map((ner, i) => ({ id: i + 1, ner })));
  }
  return hariuUusgeh(status, { message: `HTTP ${status}` });
}

// TODO: алдааг хэрэглэгчид ойлгомжтой мессеж болго (даалгаврын хүснэгтийг үз)
function hereglegchiinMessej(aldaa) {
  return "Өгөгдөл ачаалахад алдаа гарлаа.";
}

async function achaalah() {
  console.log("Ачаалж байна...");
  // TODO: AbortController үүсгэж, 50 мс-ийн дараа abort() дууд
  // TODO: try/catch дотор:
  //   - fetch-д { signal } дамжуул
  //   - hariult.ok биш бол status-тай алдаа шид
  //   - хоосон жагсаалт бол "Хоосон: Одоогоор бичлэг алга"
  //   - эс бөгөөс "Амжилттай: <тоо> бичлэг (<нэр>, <нэр>)"
  //   - catch дотор "Алдаа: <hereglegchiinMessej(aldaa)>"
  const hariult = await fetch("/api/v1/courses");
  const bichlegud = await hariult.json();
  console.log(`Амжилттай: ${bichlegud.length} бичлэг`);
}

// Оролтын мөр бүрд нэг удаа ачаална — бүү өөрчил.
for (let i = 0; i < serveriinHariunuud.length; i++) {
  await achaalah();
}
""",
            exercise=ExerciseSpec(
                statement="""\
Сервертэй ажиллах код **бүх төлөвийг** зохицуулах ёстой: ачаалж байна,
алдаа, хоосон, өгөгдөлтэй. Эхлэл кодод хуурамч `fetch` бэлэн — оролтын
мөр бүр дараагийн хүсэлтийн хариуг тодорхойлно.

`achaalah()`-г бөглө:

1. Эхэнд `Ачаалж байна...` хэвлэ (бэлэн).
2. `AbortController` үүсгэж, **50 мс**-ийн дараа `abort()` дууд.
   `signal`-ыг `fetch`-д дамжуул.
3. Хариу `ok` биш бол статустай алдаа шид (жишээ нь `aldaa.status`).
4. Жагсаалт хоосон бол `Хоосон: Одоогоор бичлэг алга`, үгүй бол
   `Амжилттай: <тоо> бичлэг (<нэрс>)` — нэрсийг `, `-аар холбоно.
5. Ямар ч алдааг барьж, `Алдаа: <мессеж>` хэвлэ. Мессежийг
   `hereglegchiinMessej(aldaa)` өгнө — түүнийг бөглө:

| Нөхцөл | Мессеж |
|---|---|
| Хугацаа хэтэрсэн (`aldaa.name === "AbortError"`) | Сервер хариу өгөхгүй байна. Дахин оролдоно уу. |
| Холболтгүй (`fetch` `TypeError` шидсэн) | Интернэт холболтоо шалгана уу. |
| 401 | Нэвтрэх хугацаа дууслаа. Дахин нэвтэрнэ үү. |
| 404 | Хайсан зүйл олдсонгүй. |
| 500–599 | Сервер түр ажиллахгүй байна. Хэсэг хүлээгээд дахин оролдоно уу. |
| Бусад | Өгөгдөл ачаалахад алдаа гарлаа. |

Техникийн мессежийг (`aldaa.message`) хэрэглэгчид бүү харуул.
`console.error`-оор бүртгэж болно — гаралтад тооцогдохгүй.

**Оролт:** мөр бүр нэг ачаалалтын серверийн хариу: `200 <нэр> <нэр> ...`
(нэргүй бол хоосон), `401`, `503` гэх мэт статус, `холболтгүй` эсвэл
`удаан` (300 мс хариулахгүй).

**Гаралт:** ачаалалт бүрд хоёр мөр:

```text
Ачаалж байна...
Амжилттай: <тоо> бичлэг (<нэр>, <нэр>)
```

Хоёр дахь мөр нь `Хоосон: Одоогоор бичлэг алга` эсвэл
`Алдаа: <мессеж>` байж болно.
""",
                tests=(
                    TestCaseSpec(
                        stdin="200 Бат Сараа Дорж\n200\n401\n",
                        expected_output="Ачаалж байна...\nАмжилттай: 3 бичлэг (Бат, Сараа, Дорж)\nАчаалж байна...\nХоосон: Одоогоор бичлэг алга\nАчаалж байна...\nАлдаа: Нэвтрэх хугацаа дууслаа. Дахин нэвтэрнэ үү.\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="503\nхолболтгүй\nудаан\n",
                        expected_output="Ачаалж байна...\nАлдаа: Сервер түр ажиллахгүй байна. Хэсэг хүлээгээд дахин оролдоно уу.\nАчаалж байна...\nАлдаа: Интернэт холболтоо шалгана уу.\nАчаалж байна...\nАлдаа: Сервер хариу өгөхгүй байна. Дахин оролдоно уу.\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="404\n200 Оюун\n",
                        expected_output="Ачаалж байна...\nАлдаа: Хайсан зүйл олдсонгүй.\nАчаалж байна...\nАмжилттай: 1 бичлэг (Оюун)\n",
                    ),
                    TestCaseSpec(
                        stdin="400\n500\n200\n",
                        expected_output="Ачаалж байна...\nАлдаа: Өгөгдөл ачаалахад алдаа гарлаа.\nАчаалж байна...\nАлдаа: Сервер түр ажиллахгүй байна. Хэсэг хүлээгээд дахин оролдоно уу.\nАчаалж байна...\nХоосон: Одоогоор бичлэг алга\n",
                    ),
                    TestCaseSpec(
                        stdin="удаан\n200 Номин Тэмүүжин\n",
                        expected_output="Ачаалж байна...\nАлдаа: Сервер хариу өгөхгүй байна. Дахин оролдоно уу.\nАчаалж байна...\nАмжилттай: 2 бичлэг (Номин, Тэмүүжин)\n",
                    ),
                    TestCaseSpec(
                        stdin="429\n",
                        expected_output="Ачаалж байна...\nАлдаа: Өгөгдөл ачаалахад алдаа гарлаа.\n",
                    ),
                ),
                solution="""\
function huleeh(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

const serveriinHariunuud = [];
let muur = prompt();
while (muur !== null) {
  serveriinHariunuud.push(muur);
  muur = prompt();
}
let dugaar = 0;

function hariuUusgeh(status, bie) {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: async () => JSON.parse(JSON.stringify(bie)),
  };
}

async function fetch(hayag, tohirgoo = {}) {
  const [kod, ...nernuud] = serveriinHariunuud[dugaar].split(" ");
  dugaar++;
  if (kod === "холболтгүй") {
    await huleeh(2);
    throw new TypeError("Failed to fetch");
  }
  await new Promise((resolve, reject) => {
    const tsag = setTimeout(resolve, kod === "удаан" ? 300 : 2);
    tohirgoo.signal?.addEventListener("abort", () => {
      clearTimeout(tsag);
      const aldaa = new Error("The operation was aborted.");
      aldaa.name = "AbortError";
      reject(aldaa);
    });
  });
  if (kod === "удаан") {
    return hariuUusgeh(200, [{ id: 1, ner: "Удаан" }]);
  }
  const status = Number(kod);
  if (status === 200) {
    return hariuUusgeh(200, nernuud.map((ner, i) => ({ id: i + 1, ner })));
  }
  return hariuUusgeh(status, { message: `HTTP ${status}` });
}

function hereglegchiinMessej(aldaa) {
  if (aldaa.name === "AbortError") return "Сервер хариу өгөхгүй байна. Дахин оролдоно уу.";
  if (aldaa.name === "TypeError") return "Интернэт холболтоо шалгана уу.";
  if (aldaa.status === 401) return "Нэвтрэх хугацаа дууслаа. Дахин нэвтэрнэ үү.";
  if (aldaa.status === 404) return "Хайсан зүйл олдсонгүй.";
  if (aldaa.status >= 500 && aldaa.status <= 599) {
    return "Сервер түр ажиллахгүй байна. Хэсэг хүлээгээд дахин оролдоно уу.";
  }
  return "Өгөгдөл ачаалахад алдаа гарлаа.";
}

async function achaalah() {
  console.log("Ачаалж байна...");

  // Хугацаа хэтэрвэл хүсэлтийг таслана
  const hyanagch = new AbortController();
  const tsag = setTimeout(() => hyanagch.abort(), 50);

  try {
    const hariult = await fetch("/api/v1/courses", { signal: hyanagch.signal });

    if (!hariult.ok) {
      const aldaa = new Error(`HTTP ${hariult.status}`);
      aldaa.status = hariult.status;
      throw aldaa;
    }

    const bichlegud = await hariult.json();

    if (bichlegud.length === 0) {
      console.log("Хоосон: Одоогоор бичлэг алга");
    } else {
      const jagsaalt = bichlegud.map((bichleg) => bichleg.ner).join(", ");
      console.log(`Амжилттай: ${bichlegud.length} бичлэг (${jagsaalt})`);
    }
  } catch (aldaa) {
    // Дэлгэрэнгүйг console-д, хэрэглэгчид ойлгомжтойг
    console.error(aldaa.message);
    console.log(`Алдаа: ${hereglegchiinMessej(aldaa)}`);
  } finally {
    clearTimeout(tsag);
  }
}

for (let i = 0; i < serveriinHariunuud.length; i++) {
  await achaalah();
}
""",
                tips="""\
- `const hyanagch = new AbortController();`, дараа нь
  `setTimeout(() => hyanagch.abort(), 50)`. `fetch`-д
  `{ signal: hyanagch.signal }` дамжуул.
- Хүсэлт амжилттай дууссан бол `finally` дотор `clearTimeout(...)`-аар
  таслах цагийг цуцал.
- `fetch` нь 4xx/5xx-д алдаа шидэхгүй. `new Error(...)` үүсгээд
  `aldaa.status = hariult.status` гэж статусаа хадгалаад шид — тэгвэл
  `hereglegchiinMessej` дотор `aldaa.status`-аар ялгана.
- `hereglegchiinMessej` дотор эхлээд `aldaa.name`-ийг (`AbortError`,
  `TypeError`), дараа нь `aldaa.status`-ыг шалга.
- Хоосон эсэхийг `bichlegud.length === 0`-оор. Нэрсийг `map` + `join(", ")`.
""",
            ),
        ),
    ],
)

ASYNC_API_MODULES = [ASYNC, APIS]
