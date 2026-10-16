"""Модул 22-25 — Төгсгөлийн төслүүд.

Курсийн бүх сэдвийг нэгтгэсэн дөрвөн апп. Хичээлийн текст нь жинхэнэ
хөтөчид ажиллах бүтэн шийдлийг харуулна. Даалгавар нь сүлжээ, DOM-гүй
орчинд ажиллах хувилбар — оролтоос тушаал уншиж, хуурамч API-тай ажиллана.
Логик, бүтэц нь яг адилхан.
"""

from app.content.types import ExerciseSpec, LessonSpec, ModuleSpec, TestCaseSpec

WEATHER = ModuleSpec(
    title="Модул 22 — Цаг агаарын апп",
    description="API-аас өгөгдөл татаж, ачаалалт ба алдааг зохицуулна.",
    lessons=[
        LessonSpec(
            title="Төсөл — Цаг агаарын апп",
            slug="tsag-agaariin-app",
            description="fetch, async/await, дөрвөн төлөв, кэш.",
            duration=900,
            content="""\
Хот хайж цаг агаарыг нь харуулах апп. Модул 18-19-ийн бүх зүйлийг
нэгтгэнэ.

### Юу үзүүлэх вэ

1. Хэрэглэгч хотын нэр бичнэ
2. Апп API руу хүсэлт явуулна
3. Ачаалж байх хугацаанд тэмдэглэгээ харуулна
4. Ирсэн өгөгдлийг зурна, эсвэл алдааг ойлгомжтой харуулна

### Бүтэц

```javascript
const tuluv = {
  tuluv: "hooson",  // hooson | achaalj | beleen | aldaa
  ugugdul: null,
  aldaa: null,
};

async function haih(hot) {
  tuluv.tuluv = "achaalj";
  zurah();

  try {
    tuluv.ugugdul = await tsagAgaarAvah(hot);
    tuluv.tuluv = "beleen";
  } catch (aldaa) {
    tuluv.aldaa = hereglegchiinMessej(aldaa);
    tuluv.tuluv = "aldaa";
  }

  zurah();
}
```

Төлөвийг **нэг объектод** төвлөрүүлэх нь чухал. Тархсан хувьсагч нь
хоорондоо зөрөх эрсдэлтэй.

### API дуудлага

```javascript
async function tsagAgaarAvah(hot) {
  const parametr = new URLSearchParams({ q: hot, units: "metric" });
  const hariult = await fetch(`${SUURI}/weather?${parametr}`);

  if (hariult.status === 404) {
    throw new Error("Хот олдсонгүй");
  }

  if (!hariult.ok) {
    throw new Error(`Сервер алдаа: ${hariult.status}`);
  }

  return hariult.json();
}
```

### Кэш

Нэг хотыг дахин дахин асуух нь утгагүй. Хариуг хотын нэрээр объектод
хадгалж, хугацаа дуусаагүй бол дахин ашиглана:

```javascript
const kesh = {}; // хотын нэр → { ugugdul, tsag }
const HUCHINTEI_HUGATSAA = 10 * 60 * 1000; // 10 минут

function keshees(hot) {
  const olson = kesh[hot];
  if (!olson) {
    return null;
  }
  if (Date.now() - olson.tsag > HUCHINTEI_HUGATSAA) {
    return null; // хэтэрхий хуучин
  }
  return olson.ugugdul;
}

// Хадгалахдаа: kesh[hot] = { ugugdul, tsag: Date.now() };
```

### API түлхүүр хаана байх вэ

> API түлхүүрийг хөтчийн кодод **хэзээ ч** бүү бич. Хэн ч түүнийг харж,
> таны нэрийн өмнөөс ашиглах боломжтой. Түлхүүр шаардсан API-г өөрийн
> сервер дамжуулан дуудна.

### Нэмэлт сорилт

Үндсэн даалгавраа давсны дараа:

1. Хайлтын түүхийг `localStorage`-д хадгалж, хуудас дахин ачаалахад
   сэргээгээрэй.
2. Хугацаа нь дууссан кэшийн бичлэгүүдийг цэвэрлэдэг функц бичээрэй.
3. Хугацаа хэтрэх хамгаалалт нэмээрэй (`AbortController`).
""",
            initial_code="""\
// --- Хуурамч API (бүү өөрчил) -------------------------------------------
const SUURI = "https://api.tsag-agaar.mn";

const SERVER_UGUGDUL = {
  "улаанбаатар": { hot: "Улаанбаатар", temp: -12, tailbar: "Цэлмэг", chiigshil: 45 },
  "дархан": { hot: "Дархан", temp: -9, tailbar: "Үүлшинэ", chiigshil: 52 },
  "эрдэнэт": { hot: "Эрдэнэт", temp: -10, tailbar: "Цас", chiigshil: 61 },
  "чойбалсан": { hot: "Чойбалсан", temp: -15, tailbar: "Салхитай", chiigshil: 38 },
  "ховд": { hot: "Ховд", temp: 3, tailbar: "Нартай", chiigshil: 30 },
  "мөрөн": { hot: "Мөрөн", temp: -20, tailbar: "Хүйтэн", chiigshil: 55 },
};

let serverAjillaj = true;
let husultiinToo = 0;

// fetch(`${SUURI}/weather?q=${tulhuur}`) — жинхэнэ fetch-ийн хариутай ижил хэлбэр
async function fetch(url) {
  husultiinToo++;
  await new Promise((resolve) => setTimeout(resolve, 5));

  if (!serverAjillaj) {
    return { ok: false, status: 503, json: async () => ({ message: "Service Unavailable" }) };
  }

  const olson = SERVER_UGUGDUL[url.split("q=")[1]];
  if (olson === undefined) {
    return { ok: false, status: 404, json: async () => ({ message: "Not found" }) };
  }
  return { ok: true, status: 200, json: async () => ({ ...olson }) };
}

// --- Апп-ын төлөв -------------------------------------------------------
const tuluv = { negj: "C", tuuh: [] }; // negj: "C" | "F", tuuh: сүүлд хайсан хотууд
const kesh = {}; // түлхүүр → { ugugdul, tsag }
const HUCHINTEI = 10 * 60 * 1000; // 10 минут

function keshees(tulhuur) {
  const olson = kesh[tulhuur];
  if (!olson || Date.now() - olson.tsag > HUCHINTEI) {
    return null;
  }
  return olson.ugugdul;
}

async function tsagAgaarAvah(tulhuur, ner) {
  const hariult = await fetch(`${SUURI}/weather?q=${tulhuur}`);
  // TODO 1: status 404 бол Error("«<ner>» хот олдсонгүй") шид.
  //         Бусад ok биш хариунд Error("Сервер түр ажиллахгүй байна (<status>)").
  return hariult.json();
}

function temperatur(c) {
  // TODO 2: tuluv.negj нь "F" бол Math.round(c * 9 / 5 + 32) + "°F" буцаа.
  return `${c}°C`;
}

function zurah(ugugdul, haanaas) {
  console.log(
    `${ugugdul.hot}: ${temperatur(ugugdul.temp)}, ${ugugdul.tailbar}, чийгшил ${ugugdul.chiigshil}% (${haanaas})`,
  );
}

async function haih(ner) {
  const tulhuur = ner.toLowerCase();

  // TODO 3: keshees(tulhuur) олдвол zurah(..., "кэш") — хүсэлт явуулахгүй.
  //         Эс бөгөөс "Ачаалж байна..." хэвлээд tsagAgaarAvah-г try/catch-аар дууд:
  //           амжилттай → kesh-д хадгалж zurah(..., "сервер");
  //           алдаа     → "✗ <мессеж>".
  //         Амжилттай хайлт бүр (кэшээс ч) хотыг tuluv.tuuh-ийн ЭХЭНД
  //         шилжүүлнэ: давхардуулахгүй, хамгийн ихдээ 5.
  const ugugdul = await tsagAgaarAvah(tulhuur, ner);
  zurah(ugugdul, "сервер");
}

// --- Тушаал унших -------------------------------------------------------
let mur = prompt();
while (mur !== null) {
  const [komand, ...uldsen] = mur.trim().split(" ");
  const utga = uldsen.join(" ").trim();

  if (komand === "хайх") {
    await haih(utga);
  } else {
    // TODO 4: "нэгж F" / "нэгж C", "сервер унтраах", "сервер асаах", "түүх",
    //         бусад бүх мөрөнд "Тушаал танигдсангүй: <мөр>".
  }

  mur = prompt();
}

console.log(`Нийт хүсэлт: ${husultiinToo}`);
""",
            exercise=ExerciseSpec(
                statement="""\
Цаг агаарын аппыг **тушаалаар** ажилладаг хувилбараар бүтээ. Хуурамч API
эхлэл кодод бэлэн: `fetch(url)` нь жинхэнэ `fetch` шиг `{ ok, status, json() }`
буцаана — хот олдохгүй бол 404, сервер унтарсан бол 503. `husultiinToo` нь
сервер рүү явсан хүсэлтийг тоолно.

**Оролт:** мөр бүр нэг тушаал, оролт дуустал:

| Тушаал | Үйлдэл |
|---|---|
| `хайх <хот>` | Хотын цаг агаарыг харуулна |
| `нэгж F`, `нэгж C` | Температурын нэгжийг солино |
| `сервер унтраах`, `сервер асаах` | Хуурамч серверийг унтрааж, асаана |
| `түүх` | Сүүлд хайсан хотуудыг харуулна |

**Гаралт:** тушаал бүрийн хариу, эцэст нь `Нийт хүсэлт: <husultiinToo>` (бэлэн).

`хайх <хот>`:

- Хотын нэрийг `trim()`, `toLowerCase()` хийсэн **түлхүүр** нь кэшэд ч, URL-д
  ч орно.
- Кэшэд байвал хүсэлт явуулахгүй:
  `<Хот>: <темп>, <тайлбар>, чийгшил <чийгшил>% (кэш)`
- Эс бөгөөс эхлээд `Ачаалж байна...`, дараа нь:
  - амжилттай — кэшэд хадгалаад ижил мөрийг `(сервер)`-ээр;
  - 404 — `✗ «<оруулсан нэр>» хот олдсонгүй`;
  - бусад алдаа — `✗ Сервер түр ажиллахгүй байна (<status>)`.
  Алдаатай хариуг кэшлэхгүй.
- Температур `°C` үед `-12°C`; `°F` үед `Math.round(c * 9 / 5 + 32)` — `10°F`.
  Кэшэд Цельсээр хадгалж, **харуулахдаа** хөрвүүл.
- Амжилттай хайлт бүр (кэшээс ч) хотын нэрийг (`ugugdul.hot`) түүхийн
  **эхэнд** шилжүүлнэ: давхардуулахгүй, хамгийн ихдээ 5.

Бусад тушаалын хариу:

```text
Нэгж: °F
Сервер унтарлаа
Сервер асалаа
Түүх: Дархан, Улаанбаатар
Тушаал танигдсангүй: <мөр>
```

Түүх хоосон бол `Түүх: хоосон`.
""",
                tests=(
                    TestCaseSpec(
                        stdin="хайх Улаанбаатар\nхайх улаанбаатар\nхайх Токио\nтүүх\n",
                        expected_output="Ачаалж байна...\nУлаанбаатар: -12°C, Цэлмэг, чийгшил 45% (сервер)\nУлаанбаатар: -12°C, Цэлмэг, чийгшил 45% (кэш)\nАчаалж байна...\n✗ «Токио» хот олдсонгүй\nТүүх: Улаанбаатар\nНийт хүсэлт: 2\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="нэгж F\nхайх Дархан\nсервер унтраах\nхайх Дархан\nхайх Эрдэнэт\nсервер асаах\nхайх Эрдэнэт\n",
                        expected_output="Нэгж: °F\nАчаалж байна...\nДархан: 16°F, Үүлшинэ, чийгшил 52% (сервер)\nСервер унтарлаа\nДархан: 16°F, Үүлшинэ, чийгшил 52% (кэш)\nАчаалж байна...\n✗ Сервер түр ажиллахгүй байна (503)\nСервер асалаа\nАчаалж байна...\nЭрдэнэт: 14°F, Цас, чийгшил 61% (сервер)\nНийт хүсэлт: 3\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="хайх Ховд\nхайх Дархан\nхайх Эрдэнэт\nхайх Чойбалсан\nхайх Улаанбаатар\nхайх Мөрөн\nхайх ДАРХАН\nтүүх\n",
                        expected_output="Ачаалж байна...\nХовд: 3°C, Нартай, чийгшил 30% (сервер)\nАчаалж байна...\nДархан: -9°C, Үүлшинэ, чийгшил 52% (сервер)\nАчаалж байна...\nЭрдэнэт: -10°C, Цас, чийгшил 61% (сервер)\nАчаалж байна...\nЧойбалсан: -15°C, Салхитай, чийгшил 38% (сервер)\nАчаалж байна...\nУлаанбаатар: -12°C, Цэлмэг, чийгшил 45% (сервер)\nАчаалж байна...\nМөрөн: -20°C, Хүйтэн, чийгшил 55% (сервер)\nДархан: -9°C, Үүлшинэ, чийгшил 52% (кэш)\nТүүх: Дархан, Мөрөн, Улаанбаатар, Чойбалсан, Эрдэнэт\nНийт хүсэлт: 6\n",
                    ),
                    TestCaseSpec(
                        stdin="түүх\nцаг\nсервер унтраах\nхайх Ховд\nсервер асаах\nхайх Ховд\nхайх   Ховд\n",
                        expected_output="Түүх: хоосон\nТушаал танигдсангүй: цаг\nСервер унтарлаа\nАчаалж байна...\n✗ Сервер түр ажиллахгүй байна (503)\nСервер асалаа\nАчаалж байна...\nХовд: 3°C, Нартай, чийгшил 30% (сервер)\nХовд: 3°C, Нартай, чийгшил 30% (кэш)\nНийт хүсэлт: 2\n",
                    ),
                    TestCaseSpec(
                        stdin="нэгж F\nхайх Мөрөн\nнэгж C\nхайх мөрөн\nхайх Чойбалсан\nхайх Сэлэнгэ\n",
                        expected_output="Нэгж: °F\nАчаалж байна...\nМөрөн: -4°F, Хүйтэн, чийгшил 55% (сервер)\nНэгж: °C\nМөрөн: -20°C, Хүйтэн, чийгшил 55% (кэш)\nАчаалж байна...\nЧойбалсан: -15°C, Салхитай, чийгшил 38% (сервер)\nАчаалж байна...\n✗ «Сэлэнгэ» хот олдсонгүй\nНийт хүсэлт: 3\n",
                    ),
                ),
                solution="""\
// --- Хуурамч API (бүү өөрчил) -------------------------------------------
const SUURI = "https://api.tsag-agaar.mn";

const SERVER_UGUGDUL = {
  "улаанбаатар": { hot: "Улаанбаатар", temp: -12, tailbar: "Цэлмэг", chiigshil: 45 },
  "дархан": { hot: "Дархан", temp: -9, tailbar: "Үүлшинэ", chiigshil: 52 },
  "эрдэнэт": { hot: "Эрдэнэт", temp: -10, tailbar: "Цас", chiigshil: 61 },
  "чойбалсан": { hot: "Чойбалсан", temp: -15, tailbar: "Салхитай", chiigshil: 38 },
  "ховд": { hot: "Ховд", temp: 3, tailbar: "Нартай", chiigshil: 30 },
  "мөрөн": { hot: "Мөрөн", temp: -20, tailbar: "Хүйтэн", chiigshil: 55 },
};

let serverAjillaj = true;
let husultiinToo = 0;

async function fetch(url) {
  husultiinToo++;
  await new Promise((resolve) => setTimeout(resolve, 5));

  if (!serverAjillaj) {
    return { ok: false, status: 503, json: async () => ({ message: "Service Unavailable" }) };
  }

  const olson = SERVER_UGUGDUL[url.split("q=")[1]];
  if (olson === undefined) {
    return { ok: false, status: 404, json: async () => ({ message: "Not found" }) };
  }
  return { ok: true, status: 200, json: async () => ({ ...olson }) };
}

// --- Апп-ын төлөв -------------------------------------------------------
const tuluv = { negj: "C", tuuh: [] };
const kesh = {}; // түлхүүр → { ugugdul, tsag }
const HUCHINTEI = 10 * 60 * 1000;

function keshees(tulhuur) {
  const olson = kesh[tulhuur];
  if (!olson || Date.now() - olson.tsag > HUCHINTEI) {
    return null;
  }
  return olson.ugugdul;
}

async function tsagAgaarAvah(tulhuur, ner) {
  const hariult = await fetch(`${SUURI}/weather?q=${tulhuur}`);

  if (hariult.status === 404) {
    throw new Error(`«${ner}» хот олдсонгүй`);
  }
  if (!hariult.ok) {
    throw new Error(`Сервер түр ажиллахгүй байна (${hariult.status})`);
  }
  return hariult.json();
}

function temperatur(c) {
  if (tuluv.negj === "F") {
    return `${Math.round((c * 9) / 5 + 32)}°F`;
  }
  return `${c}°C`;
}

function zurah(ugugdul, haanaas) {
  console.log(
    `${ugugdul.hot}: ${temperatur(ugugdul.temp)}, ${ugugdul.tailbar}, чийгшил ${ugugdul.chiigshil}% (${haanaas})`,
  );
}

function tuuhedNemeh(hot) {
  // Хуучин байрыг нь хасаад эхэнд нэмнэ, 5-аас хэтрүүлэхгүй
  tuluv.tuuh = [hot, ...tuluv.tuuh.filter((h) => h !== hot)].slice(0, 5);
}

async function haih(ner) {
  const tulhuur = ner.toLowerCase();

  const keshtei = keshees(tulhuur);
  if (keshtei) {
    zurah(keshtei, "кэш");
    tuuhedNemeh(keshtei.hot);
    return;
  }

  console.log("Ачаалж байна...");
  try {
    const ugugdul = await tsagAgaarAvah(tulhuur, ner);
    kesh[tulhuur] = { ugugdul, tsag: Date.now() };
    zurah(ugugdul, "сервер");
    tuuhedNemeh(ugugdul.hot);
  } catch (aldaa) {
    console.log(`✗ ${aldaa.message}`);
  }
}

// --- Тушаал унших -------------------------------------------------------
let mur = prompt();
while (mur !== null) {
  const [komand, ...uldsen] = mur.trim().split(" ");
  const utga = uldsen.join(" ").trim();

  if (komand === "хайх") {
    await haih(utga);
  } else if (komand === "нэгж") {
    tuluv.negj = utga;
    console.log(`Нэгж: °${utga}`);
  } else if (komand === "сервер" && utga === "унтраах") {
    serverAjillaj = false;
    console.log("Сервер унтарлаа");
  } else if (komand === "сервер" && utga === "асаах") {
    serverAjillaj = true;
    console.log("Сервер асалаа");
  } else if (komand === "түүх") {
    console.log(`Түүх: ${tuluv.tuuh.length > 0 ? tuluv.tuuh.join(", ") : "хоосон"}`);
  } else {
    console.log(`Тушаал танигдсангүй: ${mur}`);
  }

  mur = prompt();
}

console.log(`Нийт хүсэлт: ${husultiinToo}`);
""",
                tips="""\
- Төлөвийг нэг газар төвлөрүүл: `tuluv.negj`, `tuluv.tuuh`, `kesh`. Тархсан
  хувьсагчид хоорондоо зөрдөг.
- `tsagAgaarAvah` дотор `status`-ыг шалгаж `throw new Error(…)`, `haih`
  дотор `try/catch` — алдааг нэг газар хэрэглэгчийн мессеж болгоно.
- Кэшийг хүсэлтээс **өмнө** шалга — тэгвэл «Ачаалж байна...» ч хэвлэгдэхгүй,
  `husultiinToo` ч өсөхгүй.
- °F-ийг кэшэд бүү хадгал: нэгж солигдсоны дараа ч кэшийн өгөгдөл хэрэглэгдэнэ.
- Түүх: хуучин байрыг нь `filter`-ээр хасаад эхэнд нэм, дараа нь `slice(0, 5)`.
- `await haih(…)` — хүлээхгүй бол гаралтын дараалал холилдож, код дуусахад
  worker зогсоод хариу алдагдана.
""",
            ),
        ),
    ],
)

MOVIES = ModuleSpec(
    title="Модул 23 — Кино хайх апп",
    description="Хайлт, debounce, хуудаслалт, хоосон төлөв.",
    lessons=[
        LessonSpec(
            title="Төсөл — Кино хайх апп",
            slug="kino-haih-app",
            description="Бичих бүрт хайх, илүүц хүсэлт хасах, үр дүн хуудаслах.",
            duration=900,
            content="""\
Бичих бүрт хайдаг апп. Гол бэрхшээл нь **хэт олон хүсэлт** явуулахгүй
байх.

### Debounce

Хэрэглэгч "матрица" гэж бичвэл 7 хүсэлт явна. Хэрэгтэй нь зөвхөн
сүүлчийнх:

```javascript
let tsag;

talbar.addEventListener("input", (event) => {
  clearTimeout(tsag);
  tsag = setTimeout(() => haih(event.target.value), 300);
});
```

300 мс нь тав тухтай утга. Богино бол илүүц хүсэлт явна, урт бол
хэрэглэгч удаан гэж мэдэрнэ.

### Хоцорсон хариу

Debounce хийсэн ч хоёр хүсэлт зэрэг явж болно. Эхнийх нь **сүүлд** ирвэл
хуучин үр дүн шинийг дарж бичнэ:

```text
"мат"    → хүсэлт A явлаа
"матриц" → хүсэлт B явлаа
         → B ирлээ (зөв)
         → A ирлээ (хуучин — дэлгэцийг эвдлээ)
```

Шийдэл нь хамгийн сүүлийн хүсэлтийг тэмдэглэх:

```javascript
let suuliinHusult = 0;

async function haih(ug) {
  const eniiDugaar = ++suuliinHusult;
  const urDun = await avah(ug);

  if (eniiDugaar !== suuliinHusult) return; // хоцорсон — хая

  zurah(urDun);
}
```

Энэ бол бодит аппуудад байнга тохиолддог алдаа. `AbortController`-оор ч
шийдэж болно.

### Хоосон төлөв

| Нөхцөл | Харуулах зүйл |
|---|---|
| Юу ч бичээгүй | "Кино хайхын тулд нэр бичнэ үү" |
| Хайсан ч олдоогүй | "«матриц» гэсэн үр дүн олдсонгүй" |
| Алдаа гарсан | Мессеж + дахин оролдох товч |

Хайсан үгийг мессежид оруулах нь хэрэглэгчид үсгийн алдаагаа олоход
тусална.

### Хуудаслалт

```javascript
const nEgHuudsand = 5;
const huudasniiToo = Math.ceil(urDun.length / nEgHuudsand);
const haragdah = urDun.slice((huudas - 1) * nEgHuudsand, huudas * nEgHuudsand);
```

`Math.ceil` нь дээш бүхэлчилнэ: 12 кино 5-аар бол `12 / 5 = 2.4` → 3 хуудас.

### Нэмэлт сорилт

Үндсэн даалгавраа давсны дараа:

1. Оноогоос гадна он, нэрээр эрэмбэлэх сонголт нэмээрэй.
2. Дуртай кинонуудыг `localStorage`-д хадгалаарай.
3. Жинхэнэ `setTimeout`-той хувилбарт хоцорсон хариуг хаядаг
   хамгаалалтыг (`suuliinHusult`) нэмээрэй.
""",
            initial_code="""\
// --- Хуурамч кино API (бүү өөрчил) ----------------------------------------
const KINONUUD = [
  { ner: "Матрица", jil: 1999, onoo: 8.7 },
  { ner: "Матрица 2", jil: 2003, onoo: 7.2 },
  { ner: "Матрица 3", jil: 2003, onoo: 6.8 },
  { ner: "Матрица 4", jil: 2021, onoo: 5.7 },
  { ner: "Эхлэл", jil: 2010, onoo: 8.8 },
  { ner: "Од хоорондын аялал", jil: 2014, onoo: 8.6 },
  { ner: "Эргэлт", jil: 2020, onoo: 7.3 },
  { ner: "Харанхуй баатар", jil: 2008, onoo: 9.0 },
  { ner: "Аватар", jil: 2009, onoo: 7.9 },
  { ner: "Аватар 2", jil: 2022, onoo: 7.6 },
  { ner: "Титаник", jil: 1997, onoo: 7.8 },
];

let husultiinToo = 0;

// Нэрэнд ug орсон кинонууд (том жижиг үсэг хамаарахгүй)
async function avah(ug) {
  husultiinToo++;
  await new Promise((resolve) => setTimeout(resolve, 2));
  return KINONUUD.filter((k) => k.ner.toLowerCase().includes(ug.toLowerCase()));
}

const DEBOUNCE = 300;
const NEG_HUUDSAND = 3;

// --- Оролт (бэлэн) --------------------------------------------------------
const huudas = Number(prompt());
const uildluud = []; // { tsag, utga } — талбарын утга өөрчлөгдсөн агшин бүр
let mur = prompt();
while (mur !== null) {
  const [tsag, ...uges] = mur.split(" ");
  uildluud.push({ tsag: Number(tsag), utga: uges.join(" ") });
  mur = prompt();
}

// --- Хайлт ----------------------------------------------------------------
let suuliinUrDun = []; // дэлгэцэн дээр харагдах — хамгийн сүүлийн хайлтынх

async function haih(utga) {
  const ug = utga.trim();
  // TODO 2: хоосон бол "Кино хайхын тулд нэр бичнэ үү",
  //         2-оос богино бол "«<ug>» — дор хаяж 2 тэмдэгт бичнэ үү" —
  //         аль алинд нь хүсэлт явуулахгүй. Олдоогүй бол
  //         "«<ug>» гэсэн үр дүн олдсонгүй".
  //         suuliinUrDun-д оноогоор БУУРАХ дарааллаар эрэмбэлсэн хуулбар хадгал
  //         (үр дүнгүй хайлтын дараа хоосон).
  const urDun = await avah(ug);
  console.log(`«${ug}» — ${urDun.length} үр дүн`);
}

// TODO 1: Одоо бичих БҮРТ хайж байна. Debounce нэм: дараагийн өөрчлөлт
//         DEBOUNCE мс хүрэхгүй хугацаанд ирвэл энэ утгаар хайхгүй.
for (const uildel of uildluud) {
  await haih(uildel.utga);
}

console.log(`Нийт хүсэлт: ${husultiinToo}`);

// TODO 3: suuliinUrDun хоосон биш бол huudas-ыг харуул (NEG_HUUDSAND кино):
//         "Хуудас <huudas>/<нийт>:" ба мөр бүр
//         "<дугаар>. <нэр> (<он>) ★ <оноо.toFixed(1)>".
//         Ийм хуудас байхгүй бол "Хуудас <huudas> алга (нийт <нийт>)".
""",
            exercise=ExerciseSpec(
                statement="""\
Кино хайх аппын гол хоёр асуудлыг шийд: **debounce** ба **хуудаслалт**.
Жинхэнэ цаг хүлээхийн оронд хугацааг оролтоор өгнө: мөр бүр «тэр агшинд
хайлтын талбарт юу бичигдсэн байв» гэдгийг хэлнэ (оролтыг эхлэл код
`uildluud` болгон уншсан). Хуурамч API `avah(ug)` нь нэрэнд `ug` орсон
кинонуудыг буцааж, `husultiinToo`-г нэмэгдүүлнэ.

**Debounce (300 мс):** талбарын утга өөрчлөгдсөний дараа **дараагийн**
өөрчлөлт 300 мс-ээс бага хугацаанд ирвэл тэр утгаар хайхгүй. 300 мс ба
түүнээс удаан бол, эсвэл сүүлийн мөр бол тэр утгаар хайлт ажиллана.

Хайлт ажиллах бүрт (`ug` нь утгыг `trim()` хийсэн):

- хоосон — `Кино хайхын тулд нэр бичнэ үү`, хүсэлт явахгүй;
- 2-оос богино — `«<ug>» — дор хаяж 2 тэмдэгт бичнэ үү`, хүсэлт явахгүй;
- олдоогүй — `«<ug>» гэсэн үр дүн олдсонгүй`;
- олдсон — `«<ug>» — <тоо> үр дүн`.

Дараа нь `Нийт хүсэлт: <husultiinToo>` (бэлэн). Хамгийн **сүүлийн** хайлт
үр дүнтэй байсан бол түүний өгөгдсөн хуудсыг харуул: кинонууд **оноогоор
буурах** дарааллаар, нэг хуудсанд 3.

**Оролт:** 1-р мөр — харах хуудасны дугаар (1-ээс). Үлдсэн мөр бүр
`<мс> <талбарын утга>`, хугацаа өсөх дарааллаар; талбар хоосон бол зөвхөн
`<мс>`.

**Гаралт** (хуудасны хэсэг):

```text
Хуудас <дугаар>/<нийт хуудас>:
<дугаар>. <нэр> (<он>) ★ <оноо, 1 орон>
```

Кинонуудыг бүх үр дүн дундах дугаараар нь дугаарла — 2-р хуудас `4.`-өөс
эхэлнэ. Ийм хуудас байхгүй бол: `Хуудас <дугаар> алга (нийт <нийт хуудас>)`.
""",
                tests=(
                    TestCaseSpec(
                        stdin="1\n0 м\n120 ма\n250 мат\n900 матр\n1000 матри\n",
                        expected_output="«мат» — 4 үр дүн\n«матри» — 4 үр дүн\nНийт хүсэлт: 2\nХуудас 1/2:\n1. Матрица (1999) ★ 8.7\n2. Матрица 2 (2003) ★ 7.2\n3. Матрица 3 (2003) ★ 6.8\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="1\n0 а\n500 ав\n600 ава\n700 аватар\n1500 аватарх\n",
                        expected_output="«а» — дор хаяж 2 тэмдэгт бичнэ үү\n«аватар» — 2 үр дүн\n«аватарх» гэсэн үр дүн олдсонгүй\nНийт хүсэлт: 2\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="2\n0 мат\n50 матр\n",
                        expected_output="«матр» — 4 үр дүн\nНийт хүсэлт: 1\nХуудас 2/2:\n4. Матрица 4 (2021) ★ 5.7\n",
                    ),
                    TestCaseSpec(
                        stdin="3\n0 ОД\n400 од хоор\n",
                        expected_output="«ОД» — 1 үр дүн\n«од хоор» — 1 үр дүн\nНийт хүсэлт: 2\nХуудас 3 алга (нийт 1)\n",
                    ),
                    TestCaseSpec(
                        stdin="1\n0 А\n200 Ар\n",
                        expected_output="«Ар» — 3 үр дүн\nНийт хүсэлт: 1\nХуудас 1/1:\n1. Харанхуй баатар (2008) ★ 9.0\n2. Аватар (2009) ★ 7.9\n3. Аватар 2 (2022) ★ 7.6\n",
                    ),
                    TestCaseSpec(
                        stdin="2\n0 т\n100 ти\n400 та\n450 т\n700\n1000 э\n1200 эр\n",
                        expected_output="«ти» — 1 үр дүн\nКино хайхын тулд нэр бичнэ үү\n«эр» — 1 үр дүн\nНийт хүсэлт: 2\nХуудас 2 алга (нийт 1)\n",
                    ),
                ),
                solution="""\
// --- Хуурамч кино API ------------------------------------------------------
const KINONUUD = [
  { ner: "Матрица", jil: 1999, onoo: 8.7 },
  { ner: "Матрица 2", jil: 2003, onoo: 7.2 },
  { ner: "Матрица 3", jil: 2003, onoo: 6.8 },
  { ner: "Матрица 4", jil: 2021, onoo: 5.7 },
  { ner: "Эхлэл", jil: 2010, onoo: 8.8 },
  { ner: "Од хоорондын аялал", jil: 2014, onoo: 8.6 },
  { ner: "Эргэлт", jil: 2020, onoo: 7.3 },
  { ner: "Харанхуй баатар", jil: 2008, onoo: 9.0 },
  { ner: "Аватар", jil: 2009, onoo: 7.9 },
  { ner: "Аватар 2", jil: 2022, onoo: 7.6 },
  { ner: "Титаник", jil: 1997, onoo: 7.8 },
];

let husultiinToo = 0;

async function avah(ug) {
  husultiinToo++;
  await new Promise((resolve) => setTimeout(resolve, 2));
  return KINONUUD.filter((k) => k.ner.toLowerCase().includes(ug.toLowerCase()));
}

const DEBOUNCE = 300;
const NEG_HUUDSAND = 3;

// --- Оролт ----------------------------------------------------------------
const huudas = Number(prompt());
const uildluud = [];
let mur = prompt();
while (mur !== null) {
  const [tsag, ...uges] = mur.split(" ");
  uildluud.push({ tsag: Number(tsag), utga: uges.join(" ") });
  mur = prompt();
}

// --- Хайлт ----------------------------------------------------------------
let suuliinUrDun = [];

async function haih(utga) {
  const ug = utga.trim();
  suuliinUrDun = [];

  if (ug.length === 0) {
    console.log("Кино хайхын тулд нэр бичнэ үү");
    return;
  }
  if (ug.length < 2) {
    console.log(`«${ug}» — дор хаяж 2 тэмдэгт бичнэ үү`);
    return;
  }

  const urDun = await avah(ug);
  if (urDun.length === 0) {
    console.log(`«${ug}» гэсэн үр дүн олдсонгүй`);
    return;
  }

  console.log(`«${ug}» — ${urDun.length} үр дүн`);
  suuliinUrDun = [...urDun].sort((a, b) => b.onoo - a.onoo);
}

// Debounce: дараагийн өөрчлөлт 300 мс дотор ирвэл энэ утгаар хайхгүй
for (let i = 0; i < uildluud.length; i++) {
  const daraah = uildluud[i + 1];
  if (daraah === undefined || daraah.tsag - uildluud[i].tsag >= DEBOUNCE) {
    await haih(uildluud[i].utga);
  }
}

console.log(`Нийт хүсэлт: ${husultiinToo}`);

// --- Хуудаслалт -----------------------------------------------------------
if (suuliinUrDun.length > 0) {
  const niitHuudas = Math.ceil(suuliinUrDun.length / NEG_HUUDSAND);

  if (!Number.isInteger(huudas) || huudas < 1 || huudas > niitHuudas) {
    console.log(`Хуудас ${huudas} алга (нийт ${niitHuudas})`);
  } else {
    console.log(`Хуудас ${huudas}/${niitHuudas}:`);
    const ehlel = (huudas - 1) * NEG_HUUDSAND;
    suuliinUrDun.slice(ehlel, ehlel + NEG_HUUDSAND).forEach((k, i) => {
      console.log(`${ehlel + i + 1}. ${k.ner} (${k.jil}) ★ ${k.onoo.toFixed(1)}`);
    });
  }
}
""",
                tips="""\
- Debounce-ийн шийдвэр зөвхөн **дараагийн** мөрөөс хамаарна:
  `uildluud[i + 1]` байхгүй, эсвэл хугацааны зөрүү нь 300-аас багагүй бол
  хай. Тиймээс `for…of` биш индекстэй `for` хэрэгтэй.
- Хайлт бүрийг `await` хийж дараалуулж байгаа тул хоцорсон хариу энд гарахгүй.
  Жинхэнэ `setTimeout`-той хувилбарт хичээлийн `suuliinHusult` заль хэрэгтэй.
- Эрэмбэлэхдээ хуулбар дээр: `[...urDun].sort(…)`; `b.onoo - a.onoo` нь
  буурах дараалал.
- `Math.ceil(urt / 3)` — 4 кино бол 2 хуудас. Хуудасны эхний индекс
  `(huudas - 1) * 3`, дугаар нь индекс + 1.
- `(9).toFixed(1)` нь `"9.0"` — шууд хэвлэвэл `9` гарна.
- Хайлт бүр `suuliinUrDun`-ийг шинэчилнэ: сүүлийн хайлт хоосон, богино,
  олдоогүй бол хуудас хэвлэхгүй.
""",
            ),
        ),
    ],
)

EXPENSES = ModuleSpec(
    title="Модул 24 — Зарлагын бүртгэл",
    description="CRUD, хадгалалт, нэгтгэсэн үзүүлэлт.",
    lessons=[
        LessonSpec(
            title="Төсөл — Зарлагын бүртгэл",
            slug="zarlagiin-burtgel",
            description="Нэмэх, засах, устгах, шүүх, хадгалах.",
            duration=900,
            content="""\
Орлого зарлагыг бүртгэж, үлдэгдлийг тооцоолох апп. Бүрэн CRUD
(Create, Read, Update, Delete) хийх анхны төсөл.

### Өгөгдлийн бүтэц

```javascript
const gishuun = {
  id: 1,
  tailbar: "Хоол",
  dun: -23000,       // хасах нь зарлага, нэмэх нь орлого
  angilal: "Хоол",
  ognoo: "2026-09-12",
};
```

Тэмдгээр орлого зарлагыг ялгах нь тусдаа талбар нэмэхээс хялбар — нийт
дүнг шууд нэмэхэд л болно.

### Мөнгө хадгалах

> Мөнгийг бутархай тоогоор хадгалах нь удаан хугацаанд алдаа хуримтлуулна
> (`0.1 + 0.2` асуудлыг санаарай). Хамгийн жижиг нэгжээр **бүхэл тоогоор**
> хадгалж, харуулахдаа л хуваана.

### Үндсэн үйлдлүүд

```javascript
function nemeh(gishuun) {
  gishuud.push({ id: daraaghiinId++, ...gishuun });
  hadgalah();
}

function zasah(id, uurchlult) {
  const gishuun = gishuud.find((g) => g.id === id);
  if (!gishuun) return false;
  Object.assign(gishuun, uurchlult);
  hadgalah();
  return true;
}

function ustgah(id) {
  const umnuh = gishuud.length;
  gishuud = gishuud.filter((g) => g.id !== id);
  hadgalah();
  return gishuud.length < umnuh;
}
```

`Object.assign(gishuun, uurchlult)` нь `uurchlult` объектын талбаруудыг
`gishuun` руу хуулж, байгаа утгыг нь дарж бичнэ — жишээ нь `{ dun: -25000 }`
өгвөл зөвхөн `dun` солигдоно.

Үйлдэл бүр **амжилттай эсэхээ буцаах** нь чухал. Байхгүй бичлэгийг
устгах гэж оролдвол хэрэглэгчид мэдэгдэх ёстой.

### Нэгтгэсэн үзүүлэлт

```javascript
const orlogo = gishuud.filter((g) => g.dun > 0).reduce((d, g) => d + g.dun, 0);
const zarlaga = gishuud.filter((g) => g.dun < 0).reduce((d, g) => d + g.dun, 0);
const uldegdel = orlogo + zarlaga;
```

### Устгахаас өмнө батал

Устгах нь буцаах боломжгүй үйлдэл. Дор хаяж "буцаах" боломж 5 секунд
өгөх нь орчин үеийн зөв шийдэл — баталгааны цонхноос илүү тав тухтай.

### Нэмэлт сорилт

Үндсэн даалгавраа давсны дараа:

1. Огноо (`ognoo`) талбар нэмж, сараар шүүх боломж нэмээрэй.
2. Устгасан бичлэгийг хэсэг хугацаанд буцаах («undo») боломж нэмээрэй.
3. Жагсаалтаа `localStorage`-д JSON-оор хадгалж, дахин ачаалахад
   сэргээгээрэй.
""",
            initial_code="""\
// Мөнгийг бүхэл төгрөгөөр хадгалж, харуулахдаа л хэлбэржүүлнэ (бэлэн):
// 1500000 → "1,500,000₮", -30000 → "-30,000₮"
function mungu(dun) {
  let tsifr = String(Math.abs(dun));
  let ur = "";
  while (tsifr.length > 3) {
    ur = `,${tsifr.slice(-3)}${ur}`;
    tsifr = tsifr.slice(0, -3);
  }
  return `${dun < 0 ? "-" : ""}${tsifr}${ur}₮`;
}

let gishuud = []; // { id, dun, angilal, tailbar } — dun < 0 бол зарлага
let daraagiinId = 1;
let tusuv = 0; // 0 бол төсөв тогтоогоогүй

function nemeh(dun, angilal, tailbar) {
  const gishuun = { id: daraagiinId++, dun, angilal, tailbar };
  gishuud.push(gishuun);
  return gishuun;
}

// TODO 1: zasah(id, dun) — олдвол дүнг солиод true, олдохгүй бол false.
// TODO 2: ustgah(id) — устгасан бол true, олдохгүй бол false.
// TODO 3: tusuvShalgah() — төсөв тогтоосон ба нийт зарлага түүнээс их бол
//         "⚠ Төсөв хэтэрлээ: <зарлага> / <төсөв>".
// TODO 4: tailan() — Орлого, Зарлага, Үлдэгдэл ба ангилал бүрийн зарлага, хувь.

let mur = prompt();
while (mur !== null) {
  const [komand, ...uges] = mur.trim().split(" ");

  if (komand === "нэмэх") {
    const dun = Number(uges[0]);
    const angilal = uges[1];
    const tailbar = uges.slice(2).join(" ") || angilal;
    // TODO 5: дүн 0-ээс ялгаатай бүхэл тоо биш бол "✗ Дүн буруу байна".
    //         Нэмсний дараа төсвөө шалга.
    const g = nemeh(dun, angilal, tailbar);
    console.log(`✓ #${g.id} ${g.tailbar} ${mungu(g.dun)} [${g.angilal}]`);
  } else {
    // TODO 6: засах, устгах, төсөв, тайлан ба танихгүй тушаал.
  }

  mur = prompt();
}
""",
            exercise=ExerciseSpec(
                statement="""\
Зарлагын бүртгэлийг тушаалаар ажиллуул — бүрэн CRUD. Мөнгийг **бүхэл**
төгрөгөөр хадгална: эерэг нь орлого, сөрөг нь зарлага. Харуулахдаа эхлэл
кодын `mungu()`-г ашигла (`-230000` → `-230,000₮`).

**Оролт:** мөр бүр нэг тушаал, оролт дуустал:

| Тушаал | Хариу |
|---|---|
| `нэмэх <дүн> <ангилал> [тайлбар…]` | `✓ #<id> <тайлбар> <дүн> [<ангилал>]` |
| `засах <id> <дүн>` | `✓ #<id> засагдлаа: <дүн>` |
| `устгах <id>` | `✓ #<id> устгагдлаа` |
| `төсөв <дүн>` | `Төсөв: <дүн>` |
| `тайлан` | доорх тайлан |

- Тайлбар хэдэн ч үгтэй байж болно; байхгүй бол ангиллын нэр.
- `id` нь 1-ээс эхэлж, нэмэх бүрт 1-ээр өснө — устгасан `id`-г дахин
  ашиглахгүй.
- `нэмэх`, `засах`-ын дүн 0-ээс ялгаатай бүхэл тоо биш бол:
  `✗ Дүн буруу байна`.
- `засах`, `устгах`-д ийм `id` байхгүй бол: `✗ #<id> олдсонгүй`.
- Танихгүй тушаал: `✗ Тушаал танигдсангүй: <тушаал>`.
- Төсөв тогтоосон үед амжилттай `нэмэх`, `засах`, мөн `төсөв`-ийн дараа нийт
  зарлага төсвөөс **их** бол: `⚠ Төсөв хэтэрлээ: <нийт зарлага> / <төсөв>`.

**Гаралт** (`тайлан`):

```text
Орлого: 1,500,000₮
Зарлага: -860,000₮
Үлдэгдэл: 640,000₮
  Байр: 600,000₮ (70%)
  Хоол: 230,000₮ (27%)
```

Доод мөрүүд нь ангилал бүрийн зарлага (эерэг тоогоор) ба нийт зарлагад
эзлэх хувь (`Math.round`), дүнгээр нь **буурах** дарааллаар (тэнцвэл түрүүлж
орсон нь эхэнд). Зарлага байхгүй бол зөвхөн эхний гурван мөр.
""",
                tests=(
                    TestCaseSpec(
                        stdin="нэмэх 1500000 Орлого Цалин\nнэмэх -600000 Байр Түрээс\nнэмэх -230000 Хоол\nнэмэх -30000 Тээвэр Автобусны карт\nтайлан\n",
                        expected_output="✓ #1 Цалин 1,500,000₮ [Орлого]\n✓ #2 Түрээс -600,000₮ [Байр]\n✓ #3 Хоол -230,000₮ [Хоол]\n✓ #4 Автобусны карт -30,000₮ [Тээвэр]\nОрлого: 1,500,000₮\nЗарлага: -860,000₮\nҮлдэгдэл: 640,000₮\n  Байр: 600,000₮ (70%)\n  Хоол: 230,000₮ (27%)\n  Тээвэр: 30,000₮ (3%)\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="төсөв 500000\nнэмэх -300000 Байр\nнэмэх -150000 Хоол\nнэмэх -80000 Хоол Ресторан\nзасах 3 -20000\nтайлан\n",
                        expected_output="Төсөв: 500,000₮\n✓ #1 Байр -300,000₮ [Байр]\n✓ #2 Хоол -150,000₮ [Хоол]\n✓ #3 Ресторан -80,000₮ [Хоол]\n⚠ Төсөв хэтэрлээ: 530,000₮ / 500,000₮\n✓ #3 засагдлаа: -20,000₮\nОрлого: 0₮\nЗарлага: -470,000₮\nҮлдэгдэл: -470,000₮\n  Байр: 300,000₮ (64%)\n  Хоол: 170,000₮ (36%)\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="нэмэх 800000 Орлого Цалин\nнэмэх -50000 Хоол Өглөөний цай\nзасах 2 -65000\nзасах 9 -1000\nустгах 5\nнэмэх abc Хоол\nтайлан\n",
                        expected_output="✓ #1 Цалин 800,000₮ [Орлого]\n✓ #2 Өглөөний цай -50,000₮ [Хоол]\n✓ #2 засагдлаа: -65,000₮\n✗ #9 олдсонгүй\n✗ #5 олдсонгүй\n✗ Дүн буруу байна\nОрлого: 800,000₮\nЗарлага: -65,000₮\nҮлдэгдэл: 735,000₮\n  Хоол: 65,000₮ (100%)\n",
                    ),
                    TestCaseSpec(
                        stdin="нэмэх -20000 Тээвэр\nнэмэх -45000 Хоол\nнэмэх -35000 Тээвэр Такси\nустгах 2\nнэмэх 100000 Орлого Бэлэг\nхэвлэх\nтайлан\n",
                        expected_output="✓ #1 Тээвэр -20,000₮ [Тээвэр]\n✓ #2 Хоол -45,000₮ [Хоол]\n✓ #3 Такси -35,000₮ [Тээвэр]\n✓ #2 устгагдлаа\n✓ #4 Бэлэг 100,000₮ [Орлого]\n✗ Тушаал танигдсангүй: хэвлэх\nОрлого: 100,000₮\nЗарлага: -55,000₮\nҮлдэгдэл: 45,000₮\n  Тээвэр: 55,000₮ (100%)\n",
                    ),
                    TestCaseSpec(
                        stdin="нэмэх 250000 Орлого\nтайлан\nустгах 1\nустгах 1\nтайлан\n",
                        expected_output="✓ #1 Орлого 250,000₮ [Орлого]\nОрлого: 250,000₮\nЗарлага: 0₮\nҮлдэгдэл: 250,000₮\n✓ #1 устгагдлаа\n✗ #1 олдсонгүй\nОрлого: 0₮\nЗарлага: 0₮\nҮлдэгдэл: 0₮\n",
                    ),
                    TestCaseSpec(
                        stdin="нэмэх -90000 Хоол\nтөсөв 50000\nнэмэх 0 Хоол\nнэмэх 1.5 Хоол\nзасах 1 -40000\nтайлан\n",
                        expected_output="✓ #1 Хоол -90,000₮ [Хоол]\nТөсөв: 50,000₮\n⚠ Төсөв хэтэрлээ: 90,000₮ / 50,000₮\n✗ Дүн буруу байна\n✗ Дүн буруу байна\n✓ #1 засагдлаа: -40,000₮\nОрлого: 0₮\nЗарлага: -40,000₮\nҮлдэгдэл: -40,000₮\n  Хоол: 40,000₮ (100%)\n",
                    ),
                ),
                solution="""\
function mungu(dun) {
  let tsifr = String(Math.abs(dun));
  let ur = "";
  while (tsifr.length > 3) {
    ur = `,${tsifr.slice(-3)}${ur}`;
    tsifr = tsifr.slice(0, -3);
  }
  return `${dun < 0 ? "-" : ""}${tsifr}${ur}₮`;
}

let gishuud = [];
let daraagiinId = 1;
let tusuv = 0;

function nemeh(dun, angilal, tailbar) {
  const gishuun = { id: daraagiinId++, dun, angilal, tailbar };
  gishuud.push(gishuun);
  return gishuun;
}

function zasah(id, dun) {
  const gishuun = gishuud.find((g) => g.id === id);
  if (!gishuun) {
    return false;
  }
  gishuun.dun = dun;
  return true;
}

function ustgah(id) {
  const umnuh = gishuud.length;
  gishuud = gishuud.filter((g) => g.id !== id);
  return gishuud.length < umnuh;
}

// Нийт зарлага — эерэг тоогоор
function niitZarlaga() {
  return gishuud.filter((g) => g.dun < 0).reduce((d, g) => d - g.dun, 0);
}

function tusuvShalgah() {
  const zarlaga = niitZarlaga();
  if (tusuv > 0 && zarlaga > tusuv) {
    console.log(`⚠ Төсөв хэтэрлээ: ${mungu(zarlaga)} / ${mungu(tusuv)}`);
  }
}

function dunZuv(dun) {
  return Number.isInteger(dun) && dun !== 0;
}

function tailan() {
  const orlogo = gishuud.filter((g) => g.dun > 0).reduce((d, g) => d + g.dun, 0);
  const zarlaga = niitZarlaga();
  console.log(`Орлого: ${mungu(orlogo)}`);
  console.log(`Зарлага: ${mungu(-zarlaga)}`);
  console.log(`Үлдэгдэл: ${mungu(orlogo - zarlaga)}`);

  const angilalaar = gishuud
    .filter((g) => g.dun < 0)
    .reduce((dun, g) => {
      dun[g.angilal] = (dun[g.angilal] ?? 0) - g.dun;
      return dun;
    }, {});

  const erembelsen = Object.entries(angilalaar).sort((a, b) => b[1] - a[1]);
  for (const [angilal, dun] of erembelsen) {
    console.log(`  ${angilal}: ${mungu(dun)} (${Math.round((dun / zarlaga) * 100)}%)`);
  }
}

let mur = prompt();
while (mur !== null) {
  const [komand, ...uges] = mur.trim().split(" ");

  if (komand === "нэмэх") {
    const dun = Number(uges[0]);
    const angilal = uges[1];
    const tailbar = uges.slice(2).join(" ") || angilal;
    if (!dunZuv(dun)) {
      console.log("✗ Дүн буруу байна");
    } else {
      const g = nemeh(dun, angilal, tailbar);
      console.log(`✓ #${g.id} ${g.tailbar} ${mungu(g.dun)} [${g.angilal}]`);
      tusuvShalgah();
    }
  } else if (komand === "засах") {
    const id = Number(uges[0]);
    const dun = Number(uges[1]);
    if (!dunZuv(dun)) {
      console.log("✗ Дүн буруу байна");
    } else if (zasah(id, dun)) {
      console.log(`✓ #${id} засагдлаа: ${mungu(dun)}`);
      tusuvShalgah();
    } else {
      console.log(`✗ #${id} олдсонгүй`);
    }
  } else if (komand === "устгах") {
    const id = Number(uges[0]);
    console.log(ustgah(id) ? `✓ #${id} устгагдлаа` : `✗ #${id} олдсонгүй`);
  } else if (komand === "төсөв") {
    tusuv = Number(uges[0]);
    console.log(`Төсөв: ${mungu(tusuv)}`);
    tusuvShalgah();
  } else if (komand === "тайлан") {
    tailan();
  } else {
    console.log(`✗ Тушаал танигдсангүй: ${komand}`);
  }

  mur = prompt();
}
""",
                tips="""\
- `mur.trim().split(" ")` → эхний үг нь тушаал, үлдсэн нь аргументууд.
  Олон үгтэй тайлбарыг `slice(2).join(" ")`-оор нийлүүл.
- `Number("abc")` нь `NaN`, `Number.isInteger(NaN)` нь `false` — нэг
  шалгалтаар үсэг, бутархай хоёуланг нь барина.
- CRUD функц бүр амжилттай эсэхээ `true`/`false`-аар буцаавал тушаалын хэсэг
  мессежээ сонгоход амархан.
- `find`-аар олсон объектыг өөрчлөхөд массив доторх нь өөрчлөгдөнө;
  устгахдаа `filter`.
- Ангиллаар бүлэглэхэд `reduce` + `??`, эрэмбэлэхэд
  `Object.entries(…).sort(…)`.
- Нийт зарлагыг эерэг тоогоор тооцвол төсөвтэй харьцуулах, хувь бодоход
  хялбар; `Зарлага:` мөрөнд хасах тэмдэгтэй харуулна.
""",
            ),
        ),
    ],
)

QUIZ = ModuleSpec(
    title="Модул 25 — Шалгалтын апп",
    description="Төлөвт машин, таймер, үр дүнгийн дүн шинжилгээ.",
    lessons=[
        LessonSpec(
            title="Төсөл — Шалгалтын апп",
            slug="shalgaltiin-app",
            description="Асуултаар алхах, хугацаа хэмжих, үр дүн шинжлэх.",
            duration=900,
            content="""\
Курсийн эцсийн төсөл. Модул 9-ийн энгийн шалгалтыг бүрэн апп болгоно.

### Төлөвт машин

Апп нь тодорхой **төлөвүүдтэй** бөгөөд тэдгээрийн хооронд л шилжинэ:

```text
эхлэх → асуулт → (дараагийн асуулт) → үр дүн → эхлэх
```

```javascript
const tuluv = {
  ueshat: "ehleh",     // ehleh | asuult | urdun
  odoogiinIndex: 0,
  hariultuud: [],
  ehelsenTsag: null,
};
```

Төлөвт машин нь "хэрэглэгч буцах товч дарвал яах вэ" гэх мэт асуултуудыг
урьдчилан бодоход тусална. Зөвшөөрөгдөөгүй шилжилтийг хориглоно.

### Хариултыг хадгалах

Оноог тэр дор нь нэмэхийн оронд **хариулт бүрийг** хадгална:

```javascript
tuluv.hariultuud.push({
  asuultId: asuult.id,
  songoson: index,
  zuv: index === asuult.zuv,
  hugatsaa: Date.now() - asuultEhelsen,
});
```

Ингэснээр эцэст нь илүү баялаг дүн шинжилгээ хийж чадна: аль асуулт
хүндэрсэн, хаана удаан бодсон гэх мэт. Зөвхөн оноо хадгалсан бол энэ
мэдээлэл алдагдана.

### Таймер

`setInterval(функц, 1000)` нь `setTimeout`-тай төстэй ч функцийг ганц
удаа биш, **секунд тутам** дахин дахин дуудна. `clearInterval` нь зогсооно:

```javascript
const tsag = setInterval(() => {
  uldsen--;
  zurah();
  if (uldsen <= 0) {
    clearInterval(tsag);
    daraagiinAsuult();
  }
}, 1000);
```

`clearInterval`-ийг **бүү мартаарай**. Цэвэрлээгүй таймер нь хуудас
солигдсон ч ажилласаар байж, хачирхалтай алдаа үүсгэнэ.

### Санамсаргүй дараалал

```javascript
function holih(jagsaalt) {
  const huulbar = [...jagsaalt];
  for (let i = huulbar.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [huulbar[i], huulbar[j]] = [huulbar[j], huulbar[i]];
  }
  return huulbar;
}
```

Энэ бол Fisher-Yates алгоритм. `sort(() => Math.random() - 0.5)` гэдэг
өргөн тархсан заль мэх нь **жигд биш** үр дүн өгдөг тул ашиглаж болохгүй.

### Хариултыг нуух

Зөв хариултыг client талын кодод хадгалбал хэрэглэгч DevTools нээгээд
харна. Бодит шалгалтад хариултыг **сервер** дээр шалгах ёстой.

### Нэмэлт сорилт

Үндсэн даалгавраа давсны дараа:

1. Асуулт бүрт тайлбар нэмж, буруу хариултын дараа харуулаарай.
2. Хамгийн сайн оноог `localStorage`-д хадгалаарай.
3. Асуулт бүрт `setInterval` таймер нэмж, хугацаа дуусвал буруу гэж
   тооцоорой.
""",
            initial_code="""\
const ASUULTUUD = [
  {
    id: 1,
    asuult: "Аль түлхүүр үг нь блокийн хүрээтэй вэ?",
    songoltuud: ["var", "let", "function"],
    zuv: 1,
  },
  {
    id: 2,
    asuult: "Promise-ийн гурван төлөв аль нь вэ?",
    songoltuud: ["pending, fulfilled, rejected", "start, run, end", "open, close, done"],
    zuv: 0,
  },
  {
    id: 3,
    asuult: "fetch нь 404 хариу ирэхэд юу хийх вэ?",
    songoltuud: ["Алдаа шиднэ", "Алдаа шидэхгүй — ok нь false болно", "null буцаана"],
    zuv: 1,
  },
  {
    id: 4,
    asuult: "?? оператор юуг орлуулах вэ?",
    songoltuud: ["Бүх falsy утга", "Зөвхөн null ба undefined", "Зөвхөн 0"],
    zuv: 1,
  },
];

// ueshat: "ehleh" | "asuult" | "urdun"
// jagsaalt: энэ оролдлогын асуултууд, index: одоогийн асуулт,
// hariultuud: { asuult, zuv, hugatsaa } — хариулт бүрийг хадгална
const tuluv = { ueshat: "ehleh", jagsaalt: [], index: 0, hariultuud: [] };

// Одоогийн асуултыг хэвлэнэ (бэлэн)
function asuultHevleh() {
  const asuult = tuluv.jagsaalt[tuluv.index];
  console.log(`${tuluv.index + 1}/${tuluv.jagsaalt.length}. ${asuult.asuult}`);
  const songoltuud = asuult.songoltuud.map((s, i) => `${i + 1}) ${s}`);
  console.log(`   ${songoltuud.join(" | ")}`);
}

function ehluuleh(jagsaalt) {
  tuluv.ueshat = "asuult";
  tuluv.jagsaalt = jagsaalt;
  tuluv.index = 0;
  tuluv.hariultuud = [];
  asuultHevleh();
}

// TODO 1: hariulah(songolt, hugatsaa) — сонголтыг шалгаж, хариултыг хадгалаад
//         "✓ Зөв" / "✗ Буруу — зөв нь: …" хэвлэ. Дараагийн асуулт эсвэл urdun().
// TODO 2: urdun() — "=== Үр дүн ===" ба оноо, хугацаа, үнэлгээ, хамгийн удаан,
//         буруу асуултууд.

let mur = prompt();
while (mur !== null) {
  const komand = mur.trim();

  if (komand === "эхлэх") {
    // TODO 3: шалгалт явж байхад "Шалгалт аль хэдийн явж байна".
    console.log(`Шалгалт эхэллээ — ${ASUULTUUD.length} асуулт`);
    ehluuleh(ASUULTUUD);
  } else {
    // TODO 4: "давтах", буруу төлөвт ирсэн хариулт, "<сонголт> <секунд>".
  }

  mur = prompt();
}

// TODO 5: оролт дуусахад шалгалт дуусаагүй бол "Шалгалт дуусаагүй: <хариулсан>/<асуулт>".
""",
            exercise=ExerciseSpec(
                statement="""\
Шалгалтын аппыг **төлөвт машин** болгож бүтээ. Төлөв (`tuluv.ueshat`):
`ehleh` → `asuult` → `urdun`. Асуултууд ба `asuultHevleh()` эхлэл кодод
бэлэн. Асуултын дарааллыг холихгүй — тест бүр ижил дарааллыг хүлээнэ.

**Оролт:** мөр бүр нэг тушаал, оролт дуустал:

| Мөр | Зөвшөөрөгдөх төлөв | Үйлдэл |
|---|---|---|
| `эхлэх` | `ehleh`, `urdun` | `Шалгалт эхэллээ — 4 асуулт`, эхний асуулт |
| `<сонголт> <секунд>` | `asuult` | Одоогийн асуултад хариулна |
| `давтах` | `urdun` | Сүүлийн оролдлогын буруу асуултуудаар дахин |

Хариулт `2 7` нь «2-р сонголт, 7 секунд бодсон» гэсэн үг.

- Зөв бол `✓ Зөв`, буруу бол `✗ Буруу — зөв нь: <зөв сонголтын текст>`.
  Дараа нь дараагийн асуулт, сүүлийнх бол үр дүн.
- Сонголт нь 1-ээс сонголтын тоо хүртэлх бүхэл тоо биш бол:
  `Сонголт 1–<сонголтын тоо> хооронд байх ёстой` — асуулт хэвээр үлдэнэ.
- `давтах` нь `Давтлага — <тоо> асуулт` гэж эхэлнэ, асуултууд анхны
  дарааллаараа.

Буруу төлөвт ирсэн тушаал:

| Тушаал | Хэзээ | Хариу |
|---|---|---|
| `эхлэх` | шалгалтын дундуур | `Шалгалт аль хэдийн явж байна` |
| `давтах` | үр дүнгээс өөр үед | `Одоо давтах боломжгүй` |
| `давтах` | бүгд зөв байсан бол | `Давтах асуулт алга` |
| хариулт | шалгалт явахгүй үед | `Шалгалт эхлээгүй байна` |

**Гаралт** (оролдлого дуусахад):

```text
=== Үр дүн ===
Оноо: <зөв> / <асуулт> (<хувь>%)
Хугацаа: <нийт секунд> сек
Үнэлгээ: <Онц | Тэнцсэн | Дахин үзээрэй>
Хамгийн удаан: <id>-р асуулт (<секунд> сек)
Буруу: <id-ууд ", "-ээр тусгаарлан, эсвэл байхгүй>
```

Хувь нь `Math.round`; 80 ба түүнээс дээш бол «Онц», 60 ба түүнээс дээш бол
«Тэнцсэн». Хамгийн удаан нь тэнцвэл эрт хариулсан нь; `id` нь асуултын
`id`. Оролт дуусахад шалгалт дуусаагүй бол:
`Шалгалт дуусаагүй: <хариулсан>/<асуулт>`.
""",
                tests=(
                    TestCaseSpec(
                        stdin="эхлэх\n2 4\n1 12\n2 7\n3 3\n",
                        expected_output="Шалгалт эхэллээ — 4 асуулт\n1/4. Аль түлхүүр үг нь блокийн хүрээтэй вэ?\n   1) var | 2) let | 3) function\n✓ Зөв\n2/4. Promise-ийн гурван төлөв аль нь вэ?\n   1) pending, fulfilled, rejected | 2) start, run, end | 3) open, close, done\n✓ Зөв\n3/4. fetch нь 404 хариу ирэхэд юу хийх вэ?\n   1) Алдаа шиднэ | 2) Алдаа шидэхгүй — ok нь false болно | 3) null буцаана\n✓ Зөв\n4/4. ?? оператор юуг орлуулах вэ?\n   1) Бүх falsy утга | 2) Зөвхөн null ба undefined | 3) Зөвхөн 0\n✗ Буруу — зөв нь: Зөвхөн null ба undefined\n=== Үр дүн ===\nОноо: 3 / 4 (75%)\nХугацаа: 26 сек\nҮнэлгээ: Тэнцсэн\nХамгийн удаан: 2-р асуулт (12 сек)\nБуруу: 4\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="1 5\nэхлэх\n1 3\n4 2\n2 6\nэхлэх\n2 8\n2 2\nдавтах\n2 4\n1 5\n",
                        expected_output="Шалгалт эхлээгүй байна\nШалгалт эхэллээ — 4 асуулт\n1/4. Аль түлхүүр үг нь блокийн хүрээтэй вэ?\n   1) var | 2) let | 3) function\n✗ Буруу — зөв нь: let\n2/4. Promise-ийн гурван төлөв аль нь вэ?\n   1) pending, fulfilled, rejected | 2) start, run, end | 3) open, close, done\nСонголт 1–3 хооронд байх ёстой\n✗ Буруу — зөв нь: pending, fulfilled, rejected\n3/4. fetch нь 404 хариу ирэхэд юу хийх вэ?\n   1) Алдаа шиднэ | 2) Алдаа шидэхгүй — ok нь false болно | 3) null буцаана\nШалгалт аль хэдийн явж байна\n✓ Зөв\n4/4. ?? оператор юуг орлуулах вэ?\n   1) Бүх falsy утга | 2) Зөвхөн null ба undefined | 3) Зөвхөн 0\n✓ Зөв\n=== Үр дүн ===\nОноо: 2 / 4 (50%)\nХугацаа: 19 сек\nҮнэлгээ: Дахин үзээрэй\nХамгийн удаан: 3-р асуулт (8 сек)\nБуруу: 1, 2\nДавтлага — 2 асуулт\n1/2. Аль түлхүүр үг нь блокийн хүрээтэй вэ?\n   1) var | 2) let | 3) function\n✓ Зөв\n2/2. Promise-ийн гурван төлөв аль нь вэ?\n   1) pending, fulfilled, rejected | 2) start, run, end | 3) open, close, done\n✓ Зөв\n=== Үр дүн ===\nОноо: 2 / 2 (100%)\nХугацаа: 9 сек\nҮнэлгээ: Онц\nХамгийн удаан: 2-р асуулт (5 сек)\nБуруу: байхгүй\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="давтах\nэхлэх\n2 3\n1 3\n2 3\n2 3\nдавтах\n",
                        expected_output="Одоо давтах боломжгүй\nШалгалт эхэллээ — 4 асуулт\n1/4. Аль түлхүүр үг нь блокийн хүрээтэй вэ?\n   1) var | 2) let | 3) function\n✓ Зөв\n2/4. Promise-ийн гурван төлөв аль нь вэ?\n   1) pending, fulfilled, rejected | 2) start, run, end | 3) open, close, done\n✓ Зөв\n3/4. fetch нь 404 хариу ирэхэд юу хийх вэ?\n   1) Алдаа шиднэ | 2) Алдаа шидэхгүй — ok нь false болно | 3) null буцаана\n✓ Зөв\n4/4. ?? оператор юуг орлуулах вэ?\n   1) Бүх falsy утга | 2) Зөвхөн null ба undefined | 3) Зөвхөн 0\n✓ Зөв\n=== Үр дүн ===\nОноо: 4 / 4 (100%)\nХугацаа: 12 сек\nҮнэлгээ: Онц\nХамгийн удаан: 1-р асуулт (3 сек)\nБуруу: байхгүй\nДавтах асуулт алга\n",
                    ),
                    TestCaseSpec(
                        stdin="эхлэх\n3 10\n0 1\nabc\n2 15\n2 9\n1 20\nдавтах\n2 6\n2 5\n1 7\n",
                        expected_output="Шалгалт эхэллээ — 4 асуулт\n1/4. Аль түлхүүр үг нь блокийн хүрээтэй вэ?\n   1) var | 2) let | 3) function\n✗ Буруу — зөв нь: let\n2/4. Promise-ийн гурван төлөв аль нь вэ?\n   1) pending, fulfilled, rejected | 2) start, run, end | 3) open, close, done\nСонголт 1–3 хооронд байх ёстой\nСонголт 1–3 хооронд байх ёстой\n✗ Буруу — зөв нь: pending, fulfilled, rejected\n3/4. fetch нь 404 хариу ирэхэд юу хийх вэ?\n   1) Алдаа шиднэ | 2) Алдаа шидэхгүй — ok нь false болно | 3) null буцаана\n✓ Зөв\n4/4. ?? оператор юуг орлуулах вэ?\n   1) Бүх falsy утга | 2) Зөвхөн null ба undefined | 3) Зөвхөн 0\n✗ Буруу — зөв нь: Зөвхөн null ба undefined\n=== Үр дүн ===\nОноо: 1 / 4 (25%)\nХугацаа: 54 сек\nҮнэлгээ: Дахин үзээрэй\nХамгийн удаан: 4-р асуулт (20 сек)\nБуруу: 1, 2, 4\nДавтлага — 3 асуулт\n1/3. Аль түлхүүр үг нь блокийн хүрээтэй вэ?\n   1) var | 2) let | 3) function\n✓ Зөв\n2/3. Promise-ийн гурван төлөв аль нь вэ?\n   1) pending, fulfilled, rejected | 2) start, run, end | 3) open, close, done\n✗ Буруу — зөв нь: pending, fulfilled, rejected\n3/3. ?? оператор юуг орлуулах вэ?\n   1) Бүх falsy утга | 2) Зөвхөн null ба undefined | 3) Зөвхөн 0\n✗ Буруу — зөв нь: Зөвхөн null ба undefined\n=== Үр дүн ===\nОноо: 1 / 3 (33%)\nХугацаа: 18 сек\nҮнэлгээ: Дахин үзээрэй\nХамгийн удаан: 4-р асуулт (7 сек)\nБуруу: 2, 4\n",
                    ),
                    TestCaseSpec(
                        stdin="эхлэх\n2 5\n1 4\n2 3\n2 6\nэхлэх\n3 2\n",
                        expected_output="Шалгалт эхэллээ — 4 асуулт\n1/4. Аль түлхүүр үг нь блокийн хүрээтэй вэ?\n   1) var | 2) let | 3) function\n✓ Зөв\n2/4. Promise-ийн гурван төлөв аль нь вэ?\n   1) pending, fulfilled, rejected | 2) start, run, end | 3) open, close, done\n✓ Зөв\n3/4. fetch нь 404 хариу ирэхэд юу хийх вэ?\n   1) Алдаа шиднэ | 2) Алдаа шидэхгүй — ok нь false болно | 3) null буцаана\n✓ Зөв\n4/4. ?? оператор юуг орлуулах вэ?\n   1) Бүх falsy утга | 2) Зөвхөн null ба undefined | 3) Зөвхөн 0\n✓ Зөв\n=== Үр дүн ===\nОноо: 4 / 4 (100%)\nХугацаа: 18 сек\nҮнэлгээ: Онц\nХамгийн удаан: 4-р асуулт (6 сек)\nБуруу: байхгүй\nШалгалт эхэллээ — 4 асуулт\n1/4. Аль түлхүүр үг нь блокийн хүрээтэй вэ?\n   1) var | 2) let | 3) function\n✗ Буруу — зөв нь: let\n2/4. Promise-ийн гурван төлөв аль нь вэ?\n   1) pending, fulfilled, rejected | 2) start, run, end | 3) open, close, done\nШалгалт дуусаагүй: 1/4\n",
                    ),
                ),
                solution="""\
const ASUULTUUD = [
  {
    id: 1,
    asuult: "Аль түлхүүр үг нь блокийн хүрээтэй вэ?",
    songoltuud: ["var", "let", "function"],
    zuv: 1,
  },
  {
    id: 2,
    asuult: "Promise-ийн гурван төлөв аль нь вэ?",
    songoltuud: ["pending, fulfilled, rejected", "start, run, end", "open, close, done"],
    zuv: 0,
  },
  {
    id: 3,
    asuult: "fetch нь 404 хариу ирэхэд юу хийх вэ?",
    songoltuud: ["Алдаа шиднэ", "Алдаа шидэхгүй — ok нь false болно", "null буцаана"],
    zuv: 1,
  },
  {
    id: 4,
    asuult: "?? оператор юуг орлуулах вэ?",
    songoltuud: ["Бүх falsy утга", "Зөвхөн null ба undefined", "Зөвхөн 0"],
    zuv: 1,
  },
];

const tuluv = { ueshat: "ehleh", jagsaalt: [], index: 0, hariultuud: [] };

function asuultHevleh() {
  const asuult = tuluv.jagsaalt[tuluv.index];
  console.log(`${tuluv.index + 1}/${tuluv.jagsaalt.length}. ${asuult.asuult}`);
  const songoltuud = asuult.songoltuud.map((s, i) => `${i + 1}) ${s}`);
  console.log(`   ${songoltuud.join(" | ")}`);
}

function ehluuleh(jagsaalt) {
  tuluv.ueshat = "asuult";
  tuluv.jagsaalt = jagsaalt;
  tuluv.index = 0;
  tuluv.hariultuud = [];
  asuultHevleh();
}

function hariulah(songolt, hugatsaa) {
  const asuult = tuluv.jagsaalt[tuluv.index];
  const n = asuult.songoltuud.length;

  if (!Number.isInteger(songolt) || songolt < 1 || songolt > n) {
    console.log(`Сонголт 1–${n} хооронд байх ёстой`);
    return;
  }

  // Сонголт 1-ээс, zuv индекс 0-ээс эхэлнэ
  const zuv = songolt - 1 === asuult.zuv;
  tuluv.hariultuud.push({ asuult, zuv, hugatsaa });
  console.log(zuv ? "✓ Зөв" : `✗ Буруу — зөв нь: ${asuult.songoltuud[asuult.zuv]}`);

  tuluv.index++;
  if (tuluv.index < tuluv.jagsaalt.length) {
    asuultHevleh();
  } else {
    urdun();
  }
}

function urdun() {
  tuluv.ueshat = "urdun";
  const hariultuud = tuluv.hariultuud;
  const zuvToo = hariultuud.filter((h) => h.zuv).length;
  const huvi = Math.round((zuvToo / hariultuud.length) * 100);
  const niitHugatsaa = hariultuud.reduce((d, h) => d + h.hugatsaa, 0);
  const unelgee = huvi >= 80 ? "Онц" : huvi >= 60 ? "Тэнцсэн" : "Дахин үзээрэй";

  let udaan = hariultuud[0];
  for (const h of hariultuud) {
    if (h.hugatsaa > udaan.hugatsaa) {
      udaan = h;
    }
  }

  const buruu = hariultuud.filter((h) => !h.zuv).map((h) => h.asuult.id);

  console.log("=== Үр дүн ===");
  console.log(`Оноо: ${zuvToo} / ${hariultuud.length} (${huvi}%)`);
  console.log(`Хугацаа: ${niitHugatsaa} сек`);
  console.log(`Үнэлгээ: ${unelgee}`);
  console.log(`Хамгийн удаан: ${udaan.asuult.id}-р асуулт (${udaan.hugatsaa} сек)`);
  console.log(`Буруу: ${buruu.length > 0 ? buruu.join(", ") : "байхгүй"}`);
}

let mur = prompt();
while (mur !== null) {
  const komand = mur.trim();

  if (komand === "эхлэх") {
    if (tuluv.ueshat === "asuult") {
      console.log("Шалгалт аль хэдийн явж байна");
    } else {
      console.log(`Шалгалт эхэллээ — ${ASUULTUUD.length} асуулт`);
      ehluuleh(ASUULTUUD);
    }
  } else if (komand === "давтах") {
    if (tuluv.ueshat !== "urdun") {
      console.log("Одоо давтах боломжгүй");
    } else {
      const buruunuud = tuluv.hariultuud.filter((h) => !h.zuv).map((h) => h.asuult);
      if (buruunuud.length === 0) {
        console.log("Давтах асуулт алга");
      } else {
        console.log(`Давтлага — ${buruunuud.length} асуулт`);
        ehluuleh(buruunuud);
      }
    }
  } else if (tuluv.ueshat !== "asuult") {
    console.log("Шалгалт эхлээгүй байна");
  } else {
    const [songolt, hugatsaa] = komand.split(" ").map(Number);
    hariulah(songolt, hugatsaa);
  }

  mur = prompt();
}

if (tuluv.ueshat === "asuult") {
  console.log(`Шалгалт дуусаагүй: ${tuluv.hariultuud.length}/${tuluv.jagsaalt.length}`);
}
""",
                tips="""\
- Тушаал бүрийн өмнө `tuluv.ueshat`-ыг шалга — төлөвт машины гол санаа нь
  зөвшөөрөгдөөгүй шилжилтийг хориглох.
- Оноог тэр дор нь нэмэхийн оронд хариулт бүрийг `{ asuult, zuv, hugatsaa }`
  болгож хадгал — оноо, хугацаа, хамгийн удаан, буруу асуултууд бүгд үүнээс
  гарна.
- Сонголт 1-ээс, `zuv` индекс 0-ээс эхэлдэг: `songolt - 1 === asuult.zuv`.
- `"abc".split(" ").map(Number)` → `[NaN]`; `Number.isInteger`-ээр шалгавал
  `0`, `4`, `abc` бүгд баригдана.
- `давтах` нь сүүлийн оролдлогын буруу асуултуудаас шинэ жагсаалт үүсгээд
  ижил `ehluuleh()`-ээр эхэлнэ — жагсаалт солигдоход л хангалттай.
- Хамгийн удааныг олохдоо `>` (хатуу) — тэнцвэл эхнийх нь үлдэнэ.
""",
            ),
        ),
    ],
)

FINAL_PROJECT_MODULES = [WEATHER, MOVIES, EXPENSES, QUIZ]
