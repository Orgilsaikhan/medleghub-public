"""Модул 14 — Хөтчийн төслүүд.

Модул 10-13-ын DOM, үйл явдал, форм, хадгалалтыг нэгтгэнэ. Хичээлийн текст
дэх код нь жинхэнэ хөтөчид ажиллах бодит хувилбар. Анхны код нь DOM-гүй
орчинд ажиллах загвар — логик нь яг адилхан.

Даалгаврууд DOM-ын оронд хэрэглэгчийн үйлдлийг оролтын мөрөөр (тушаал,
товч, формын талбар) авч, үр дүнг `console.log`-оор хэвлэнэ. `localStorage`
хэрэгтэй бол эхлэл код, жишиг шийдэл хоёулаа жижиг загвараа зарлана.
"""

from app.content.types import ExerciseSpec, LessonSpec, ModuleSpec, TestCaseSpec

BROWSER_PROJECTS = ModuleSpec(
    title="Модул 14 — Хөтчийн төслүүд",
    description="DOM, үйл явдал, хадгалалтыг нэгтгэсэн жижиг аппууд.",
    lessons=[
        LessonSpec(
            title="Төсөл — Интерактив to-do апп",
            slug="interaktiv-to-do-app",
            description="Ажил нэмэх, тэмдэглэх, устгах, хадгалах.",
            duration=720,
            content="""\
Модул 9-д бичсэн жагсаалтыг одоо дэлгэц дээр гаргана.

### Бүтэц

Аппыг гурван хэсэгт хуваа:

| Хэсэг | Үүрэг |
|---|---|
| Төлөв (state) | Ажлуудын массив |
| Үйлдэл | Нэмэх, тэмдэглэх, устгах |
| Зурах (render) | Төлөвийг DOM болгож харуулах |

Энэ хуваарилалт нь React зэрэг сангуудын үндсэн санаа. Одооноос
дасвал хожим хялбар болно.

### Нэг чиглэлт урсгал

```text
хэрэглэгчийн үйлдэл → төлөв өөрчлөгдөнө → дахин зурна
```

DOM-ыг **хэзээ ч** шууд бүү засварла. Зөвхөн төлөвөө өөрчилж, дараа нь
дахин зур. Ингэснээр дэлгэц ба өгөгдөл хоорондоо хэзээ ч зөрөхгүй.

### Зурах функц

```javascript
function zurah() {
  jagsaalt.replaceChildren();

  for (const ajil of ajluud) {
    const li = document.createElement("li");
    li.textContent = ajil.garchig;
    li.dataset.id = ajil.id;
    if (ajil.duussan) {
      li.classList.add("duussan");
    }
    jagsaalt.append(li);
  }
}
```

`li.dataset.id` нь элементийн `data-id` шинж чанарт утга хадгална. Дараа нь
аль мөр дээр дарсныг түүгээр нь танина.

### Төлөөлөгч сонсогч

Мөр бүрт сонсогч хавсаргах шаардлагагүй:

```javascript
jagsaalt.addEventListener("click", (event) => {
  const li = event.target.closest("li");
  if (!li) {
    return; // мөрөөс гадуур дарсан
  }

  duusgah(Number(li.dataset.id));
  zurah();
});
```

### Хадгалах

Өөрчлөлт бүрийн дараа `localStorage`-д бичнэ:

```javascript
function hadgalah() {
  localStorage.setItem("ajluud", JSON.stringify(ajluud));
}
```

### Нэмэлт сорилт

Доорх «Даалгавар»-т DOM-ын оронд хэрэглэгчийн үйлдэл оролтын мөрөөр
(тушаалаар) ирнэ — «үйлдэл → төлөв → зурах» урсгал яг адилхан. Түүнийг
дуусгасны дараа жинхэнэ хөтөчид:

1. Ажлыг засварлах боломж нэмээрэй.
2. "Бүгд", "Дууссан", "Үлдсэн" шүүлтүүрийг товчоор сонгодог болгоорой.
""",
            initial_code="""\
// Worker дотор жинхэнэ localStorage байхгүй — ижил методтой жижиг загвар.
const localStorage = {
  ugugdul: {},
  setItem(tulhuur, utga) {
    this.ugugdul[tulhuur] = String(utga);
  },
  getItem(tulhuur) {
    return tulhuur in this.ugugdul ? this.ugugdul[tulhuur] : null;
  },
};

// --- Төлөв ---------------------------------------------------------------
let ajluud = [];
let daraagiinId = 1;
let shuultuur = "бүгд"; // "бүгд", "дууссан" эсвэл "үлдсэн"

function hadgalah() {
  localStorage.setItem("ajluud", JSON.stringify(ajluud));
}

// --- Үйлдлүүд ------------------------------------------------------------
function nemeh(garchig) {
  if (!garchig.trim()) {
    return; // хоосон гарчиг нэмэхгүй
  }
  ajluud.push({ id: daraagiinId++, garchig: garchig.trim(), duussan: false });
  hadgalah();
}

function tumdeglah(id) {
  // TODO: id-тай ажлын duussan-ийг эсрэгээр нь соль, дараа нь хадгал
}

function ustgah(id) {
  // TODO: id-тай ажлыг жагсаалтаас хасаад хадгал
}

// --- Зурах ---------------------------------------------------------------
function zurah() {
  console.log(`--- Ажлууд (${shuultuur}) ---`);

  // TODO: shuultuur-т таарах ажлуудыг л харуул; нэг ч байхгүй бол "(хоосон)"
  for (const ajil of ajluud) {
    console.log(`${ajil.duussan ? "[x]" : "[ ]"} ${ajil.id}. ${ajil.garchig}`);
  }

  const uldsen = ajluud.filter((a) => !a.duussan).length;
  console.log(`Үлдсэн: ${uldsen} / ${ajluud.length}`);
}

// --- Тушаал унших (хэрэглэгчийн үйлдэл) ------------------------------------
let mur = prompt();
while (mur !== null) {
  const zai = mur.indexOf(" ");
  const tushaal = zai === -1 ? mur : mur.slice(0, zai);
  const utga = zai === -1 ? "" : mur.slice(zai + 1);

  if (tushaal === "нэмэх") {
    nemeh(utga);
  }
  // TODO: "тэмдэглэх", "устгах" (utga-г тоо болго), "шүүлтүүр" тушаалууд

  mur = prompt();
}

zurah();
console.log(`Хадгалсан: ${localStorage.getItem("ajluud") || "[]"}`);
""",
            exercise=ExerciseSpec(
                statement="""\
To-do аппын үйлдлүүдийг гүйцээ. DOM-ын оронд хэрэглэгчийн үйлдэл оролтын
мөрөөр (тушаалаар) ирнэ — «үйлдэл → төлөв → зурах» урсгал яг адилхан. Эхлэл
кодод `localStorage`-ийн загвар, `nemeh`, тушаал уншдаг давталт бэлэн.

**Оролт:** мөр бүрт нэг тушаал, оролт дуустал:

| Тушаал | Үйлдэл |
|---|---|
| `нэмэх <гарчиг>` | Шинэ ажил нэмнэ. Дугаар нь 1, 2, 3, … дараалан. Хоосон гарчгийг үл тооно. |
| `тэмдэглэх <дугаар>` | Ажлын дууссан эсэхийг эсрэгээр нь солино. |
| `устгах <дугаар>` | Ажлыг жагсаалтаас хасна. |
| `шүүлтүүр <бүгд/дууссан/үлдсэн>` | Аль ажлуудыг харуулахыг сонгоно (анхдагч нь `бүгд`). |

Байхгүй дугаартай тушаал юу ч өөрчлөхгүй. Устгасан ажлын дугаарыг дахин
ашиглахгүй.

**Гаралт:** бүх тушаалын дараа нэг удаа зурна:

```text
--- Ажлууд (<шүүлтүүр>) ---
[x] <дугаар>. <гарчиг>
[ ] <дугаар>. <гарчиг>
Үлдсэн: <дуусаагүй ажлын тоо> / <нийт ажлын тоо>
Хадгалсан: <localStorage-ийн "ajluud" утга>
```

- `[x]` — дууссан, `[ ]` — дуусаагүй ажил. Шүүлтүүрт таарах ажлуудыг
  нэмсэн дарааллаар нь харуулна; нэг ч байхгүй бол тэдгээрийн оронд
  `(хоосон)` гэсэн нэг мөр.
- `Үлдсэн` мөр шүүлтүүрээс үл хамааран **бүх** ажлыг тоолно.
- Өөрчлөлт бүрийн дараа `hadgalah()`-ыг дууд — сүүлийн мөр нь хадгалсан
  JSON-ыг хэвлэнэ (эхлэл кодод бэлэн).
""",
                tests=(
                    TestCaseSpec(
                        stdin="нэмэх Хичээл үзэх\nнэмэх Дасгал хийх\nнэмэх Ном унших\nтэмдэглэх 1\nустгах 2\n",
                        expected_output=(
                            "--- Ажлууд (бүгд) ---\n"
                            "[x] 1. Хичээл үзэх\n"
                            "[ ] 3. Ном унших\n"
                            "Үлдсэн: 1 / 2\n"
                            'Хадгалсан: [{"id":1,"garchig":"Хичээл үзэх","duussan":true},'
                            '{"id":3,"garchig":"Ном унших","duussan":false}]\n'
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="нэмэх Талх авах\nнэмэх Сүү авах\nтэмдэглэх 2\nшүүлтүүр дууссан\n",
                        expected_output=(
                            "--- Ажлууд (дууссан) ---\n"
                            "[x] 2. Сүү авах\n"
                            "Үлдсэн: 1 / 2\n"
                            'Хадгалсан: [{"id":1,"garchig":"Талх авах","duussan":false},'
                            '{"id":2,"garchig":"Сүү авах","duussan":true}]\n'
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin=(
                            "нэмэх    \nнэмэх Гүйх\nтэмдэглэх 1\nтэмдэглэх 1\n"
                            "нэмэх Унших\nтэмдэглэх 2\nшүүлтүүр үлдсэн\n"
                        ),
                        expected_output=(
                            "--- Ажлууд (үлдсэн) ---\n"
                            "[ ] 1. Гүйх\n"
                            "Үлдсэн: 1 / 2\n"
                            'Хадгалсан: [{"id":1,"garchig":"Гүйх","duussan":false},'
                            '{"id":2,"garchig":"Унших","duussan":true}]\n'
                        ),
                    ),
                    TestCaseSpec(
                        stdin="нэмэх А\nустгах 1\nустгах 5\n",
                        expected_output=(
                            "--- Ажлууд (бүгд) ---\n(хоосон)\nҮлдсэн: 0 / 0\nХадгалсан: []\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin=(
                            "нэмэх Нэг\nнэмэх Хоёр\nустгах 1\nнэмэх Гурав\nтэмдэглэх 3\n"
                            "тэмдэглэх 9\nшүүлтүүр дууссан\nшүүлтүүр бүгд\n"
                        ),
                        expected_output=(
                            "--- Ажлууд (бүгд) ---\n"
                            "[ ] 2. Хоёр\n"
                            "[x] 3. Гурав\n"
                            "Үлдсэн: 1 / 2\n"
                            'Хадгалсан: [{"id":2,"garchig":"Хоёр","duussan":false},'
                            '{"id":3,"garchig":"Гурав","duussan":true}]\n'
                        ),
                    ),
                    TestCaseSpec(
                        stdin="нэмэх Сорил\nтэмдэглэх 1\nшүүлтүүр үлдсэн\n",
                        expected_output=(
                            "--- Ажлууд (үлдсэн) ---\n"
                            "(хоосон)\n"
                            "Үлдсэн: 0 / 1\n"
                            'Хадгалсан: [{"id":1,"garchig":"Сорил","duussan":true}]\n'
                        ),
                    ),
                ),
                solution="""\
// Worker дотор жинхэнэ localStorage байхгүй — ижил методтой жижиг загвар.
const localStorage = {
  ugugdul: {},
  setItem(tulhuur, utga) {
    this.ugugdul[tulhuur] = String(utga);
  },
  getItem(tulhuur) {
    return tulhuur in this.ugugdul ? this.ugugdul[tulhuur] : null;
  },
};

// --- Төлөв ---------------------------------------------------------------
let ajluud = [];
let daraagiinId = 1;
let shuultuur = "бүгд"; // "бүгд", "дууссан" эсвэл "үлдсэн"

function hadgalah() {
  localStorage.setItem("ajluud", JSON.stringify(ajluud));
}

// --- Үйлдлүүд ------------------------------------------------------------
function nemeh(garchig) {
  if (!garchig.trim()) {
    return; // хоосон гарчиг нэмэхгүй
  }
  ajluud.push({ id: daraagiinId++, garchig: garchig.trim(), duussan: false });
  hadgalah();
}

function tumdeglah(id) {
  const ajil = ajluud.find((a) => a.id === id);
  if (ajil) {
    ajil.duussan = !ajil.duussan;
    hadgalah();
  }
}

function ustgah(id) {
  ajluud = ajluud.filter((a) => a.id !== id);
  hadgalah();
}

// --- Зурах ---------------------------------------------------------------
function zurah() {
  console.log(`--- Ажлууд (${shuultuur}) ---`);

  // Төлөвийг өөрчлөхгүй — харуулах ажлуудыг тусдаа массив болгоно.
  let haragdah = ajluud;
  if (shuultuur === "дууссан") {
    haragdah = ajluud.filter((a) => a.duussan);
  } else if (shuultuur === "үлдсэн") {
    haragdah = ajluud.filter((a) => !a.duussan);
  }

  if (haragdah.length === 0) {
    console.log("(хоосон)");
  }
  for (const ajil of haragdah) {
    console.log(`${ajil.duussan ? "[x]" : "[ ]"} ${ajil.id}. ${ajil.garchig}`);
  }

  // Үлдсэнийг шүүлтүүрээс үл хамааран бүх ажлаас тоолно.
  const uldsen = ajluud.filter((a) => !a.duussan).length;
  console.log(`Үлдсэн: ${uldsen} / ${ajluud.length}`);
}

// --- Тушаал унших (хэрэглэгчийн үйлдэл) ------------------------------------
let mur = prompt();
while (mur !== null) {
  const zai = mur.indexOf(" ");
  const tushaal = zai === -1 ? mur : mur.slice(0, zai);
  const utga = zai === -1 ? "" : mur.slice(zai + 1);

  if (tushaal === "нэмэх") {
    nemeh(utga);
  } else if (tushaal === "тэмдэглэх") {
    tumdeglah(Number(utga)); // id нь тоо — "1" === 1 биш
  } else if (tushaal === "устгах") {
    ustgah(Number(utga));
  } else if (tushaal === "шүүлтүүр") {
    shuultuur = utga;
  }

  mur = prompt();
}

zurah();
console.log(`Хадгалсан: ${localStorage.getItem("ajluud") || "[]"}`);
""",
                tips="""\
- Тушаал бүр зөвхөн **төлөвийг** (`ajluud`, `shuultuur`) өөрчилнө. Зурах нь
  хамгийн сүүлд нэг удаа — хичээлийн «нэг чиглэлт урсгал».
- `utga` нь текст. Дугаарыг `Number(utga)`-аар тоо болго — эс бөгөөс
  `a.id === "1"` хэзээ ч үнэн болохгүй.
- Тэмдэглэхдээ `find`-аар ажлаа олоод `duussan`-ийг `!`-ээр эргүүл. Устгахдаа
  `filter`-ээр тэр дугаараас бусдыг үлдээ. Байхгүй дугаарт `find` нь
  `undefined` буцаана — шалгаж байж хандаарай.
- Шүүлтүүрийг `ajluud`-ыг өөрчлөхгүйгээр, харуулах ажлуудыг `filter`-ээр
  тусад нь гаргаж хий. `Үлдсэн`-ийг бүх `ajluud`-аас тоол.
- `tumdeglah`, `ustgah` дотроо `hadgalah()`-ыг дууд. Мартвал сүүлийн мөр
  хуучин төлөвийг харуулна.
""",
            ),
        ),
        LessonSpec(
            title="Төсөл — Формын шалгагч",
            slug="formiin-shalgagch",
            description="Бүртгэлийн форм, талбар бүрийн алдааны мессеж.",
            duration=720,
            content="""\
Бүртгэлийн формыг бүрэн шалгах систем бичнэ.

### Дүрмийг өгөгдөл болгох

Талбар бүрт `if` бичихийн оронд дүрмүүдээ жагсаалт болго:

```javascript
const durmuud = {
  ner: [
    { shalgah: (u) => u.trim().length > 0, messej: "Нэрээ оруулна уу" },
    { shalgah: (u) => u.length <= 50, messej: "Нэр хэт урт байна" },
  ],
  email: [
    { shalgah: (u) => u.includes("@"), messej: "Имэйл хаяг буруу байна" },
  ],
};
```

Ингэснээр шинэ талбар нэмэхэд шалгах кодоо огт өөрчлөхгүй.

### Шалгах функц

```javascript
function shalgah(ugugdul) {
  const aldaanuud = {};

  for (const [talbar, talbariinDurmuud] of Object.entries(durmuud)) {
    for (const durem of talbariinDurmuud) {
      if (!durem.shalgah(ugugdul[talbar] || "")) {
        aldaanuud[talbar] = durem.messej;
        break; // эхний алдааг л харуулна
      }
    }
  }

  return aldaanuud;
}
```

### Алдааг харуулах

```javascript
function aldaaHaruulah(talbar, messej) {
  const oruulga = document.querySelector(`#${talbar}`);
  const hesegt = document.querySelector(`#${talbar}-aldaa`);

  oruulga.setAttribute("aria-invalid", messej ? "true" : "false");
  hesegt.textContent = messej || "";
}
```

`aria-invalid` нь дэлгэц уншигчид алдааг мэдэгдэнэ. Зөвхөн улаан хүрээ
хангалтгүй.

### Хэзээ шалгах вэ

- Талбараас гарахад (`blur`) — тэр талбарыг л
- Илгээхэд (`submit`) — бүгдийг

Бичиж байх үед шалгах нь хэрэглэгчийг залхаана.

### Нэмэлт сорилт

Доорх «Даалгавар»-т «нууц үг давтах» талбарын дүрмийг нэмнэ — формын
талбарууд оролтын мөрөөр ирнэ. Дараа нь жинхэнэ хөтөчид:

1. Нууц үгийн хүчийг (сул / дунд / хүчтэй) үнэлээрэй.
2. Бүх талбар зөв үед л илгээх товчийг идэвхжүүлээрэй.
""",
            initial_code="""\
// Дүрэм бүр: shalgah(утга) нь true бол зөв, false бол messej-ийг харуулна.
const durmuud = {
  ner: [
    { shalgah: (u) => u.trim().length > 0, messej: "Нэрээ оруулна уу" },
    { shalgah: (u) => u.trim().length <= 20, messej: "Нэр хэт урт байна" },
  ],
  email: [
    { shalgah: (u) => u.length > 0, messej: "Имэйлээ оруулна уу" },
    { shalgah: (u) => u.includes("@") && u.includes("."), messej: "Имэйл хаяг буруу байна" },
  ],
  nuuts: [
    { shalgah: (u) => u.length >= 8, messej: "Нууц үг дор хаяж 8 тэмдэгт байна" },
    {
      // Үсэг бүрийг шалгана: аль нэг нь цифр байна уу?
      shalgah: (u) => u.split("").some((t) => "0123456789".includes(t)),
      messej: "Нууц үгэнд дор хаяж нэг тоо байна",
    },
  ],
  // TODO: davtah талбарын хоёр дүрэм:
  //   1) хоосон бол "Нууц үгээ давтан оруулна уу"
  //   2) nuuts-тай таарахгүй бол "Нууц үг таарахгүй байна"
};

function shalgah(ugugdul) {
  const aldaanuud = {};

  for (const [talbar, talbariinDurmuud] of Object.entries(durmuud)) {
    for (const durem of talbariinDurmuud) {
      // TODO: davtah-ын дүрэм nuuts-ыг харах ёстой — бүх ugugdul-ыг ч дамжуул
      if (!durem.shalgah(ugugdul[talbar] || "")) {
        aldaanuud[talbar] = durem.messej;
        break; // эхний алдааг л харуулна
      }
    }
  }

  return aldaanuud;
}

// Формын дөрвөн талбар (бүү өөрчил).
const ugugdul = {
  ner: prompt() || "",
  email: prompt() || "",
  nuuts: prompt() || "",
  davtah: prompt() || "",
};

const aldaanuud = shalgah(ugugdul);

// TODO: алдаагүй бол "✓ <нэр> бүртгэгдлээ" (нэрийн захын зайг хасна),
//       алдаатай бол талбар бүрийг доорх шиг хэвлэнэ
for (const [talbar, messej] of Object.entries(aldaanuud)) {
  console.log(`✗ ${talbar}: ${messej}`);
}
""",
            exercise=ExerciseSpec(
                statement="""\
Бүртгэлийн формын шалгагчийг гүйцээ. Дүрмүүд өгөгдөл хэлбэрээр `durmuud`
объектод бий — «нууц үг давтах» (`davtah`) талбарын дүрмийг нэмж, үр дүнг
хэвлэ.

**Оролт:** дөрвөн мөр — нэр, имэйл, нууц үг, нууц үгийн давталт (уншдаг хэсэг
эхлэл кодод бэлэн). Мөр хоосон байж болно.

**Дүрмүүд.** Талбар бүрийн **эхний** зөрчигдсөн дүрмийн мессежийг л
харуулна:

| Талбар | Дүрэм | Мессеж |
|---|---|---|
| `ner` | Захын зайг хассаны дараа хоосон биш | `Нэрээ оруулна уу` |
| `ner` | Захын зайг хассаны дараа 20-оос ихгүй тэмдэгт | `Нэр хэт урт байна` |
| `email` | Хоосон биш | `Имэйлээ оруулна уу` |
| `email` | `@` ба `.` хоёуланг агуулна | `Имэйл хаяг буруу байна` |
| `nuuts` | Дор хаяж 8 тэмдэгт | `Нууц үг дор хаяж 8 тэмдэгт байна` |
| `nuuts` | Дор хаяж нэг цифр | `Нууц үгэнд дор хаяж нэг тоо байна` |
| `davtah` | Хоосон биш | `Нууц үгээ давтан оруулна уу` |
| `davtah` | `nuuts`-тай яг ижил | `Нууц үг таарахгүй байна` |

**Гаралт:**

- Алдаагүй бол нэг мөр: `✓ <нэр> бүртгэгдлээ` — нэрийн захын зайг хассан.
- Алдаатай бол алдаатай талбар бүрт нэг мөр, хүснэгтийн дарааллаар:
  `✗ <талбар>: <мессеж>`.
""",
                tests=(
                    TestCaseSpec(
                        stdin="Бат\nbat@medleghub.mn\nnuutsUg1\nnuutsUg1\n",
                        expected_output="✓ Бат бүртгэгдлээ\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="Дорж\ndorj@mail\nnuutsugaa\nnuutsugaa\n",
                        expected_output=(
                            "✗ email: Имэйл хаяг буруу байна\n"
                            "✗ nuuts: Нууц үгэнд дор хаяж нэг тоо байна\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="\nbat\nabc\nabd\n",
                        expected_output=(
                            "✗ ner: Нэрээ оруулна уу\n"
                            "✗ email: Имэйл хаяг буруу байна\n"
                            "✗ nuuts: Нууц үг дор хаяж 8 тэмдэгт байна\n"
                            "✗ davtah: Нууц үг таарахгүй байна\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="  Сараа  \nsaraa@mail.mn\nSaraa2026\nSaraa2026\n",
                        expected_output="✓ Сараа бүртгэгдлээ\n",
                    ),
                    TestCaseSpec(
                        stdin="Батбаярын Энхтүвшинжаргал\n\nparol2026\n\n",
                        expected_output=(
                            "✗ ner: Нэр хэт урт байна\n"
                            "✗ email: Имэйлээ оруулна уу\n"
                            "✗ davtah: Нууц үгээ давтан оруулна уу\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="Туяа\ntuyaa@mail.mn\nnuutsug\nnuutsug\n",
                        expected_output="✗ nuuts: Нууц үг дор хаяж 8 тэмдэгт байна\n",
                    ),
                ),
                solution="""\
// Дүрэм бүр: shalgah(утга, бүх өгөгдөл) нь true бол зөв.
const durmuud = {
  ner: [
    { shalgah: (u) => u.trim().length > 0, messej: "Нэрээ оруулна уу" },
    { shalgah: (u) => u.trim().length <= 20, messej: "Нэр хэт урт байна" },
  ],
  email: [
    { shalgah: (u) => u.length > 0, messej: "Имэйлээ оруулна уу" },
    { shalgah: (u) => u.includes("@") && u.includes("."), messej: "Имэйл хаяг буруу байна" },
  ],
  nuuts: [
    { shalgah: (u) => u.length >= 8, messej: "Нууц үг дор хаяж 8 тэмдэгт байна" },
    {
      shalgah: (u) => u.split("").some((t) => "0123456789".includes(t)),
      messej: "Нууц үгэнд дор хаяж нэг тоо байна",
    },
  ],
  davtah: [
    { shalgah: (u) => u.length > 0, messej: "Нууц үгээ давтан оруулна уу" },
    // Хоёр дахь аргумент — бүх форм, тэгэхээр өөр талбартай харьцуулж болно.
    { shalgah: (u, ugugdul) => u === ugugdul.nuuts, messej: "Нууц үг таарахгүй байна" },
  ],
};

function shalgah(ugugdul) {
  const aldaanuud = {};

  for (const [talbar, talbariinDurmuud] of Object.entries(durmuud)) {
    for (const durem of talbariinDurmuud) {
      // Нэг аргументтай дүрмүүд илүү аргументыг зүгээр үл тооно.
      if (!durem.shalgah(ugugdul[talbar] || "", ugugdul)) {
        aldaanuud[talbar] = durem.messej;
        break; // эхний алдааг л харуулна
      }
    }
  }

  return aldaanuud;
}

// Формын дөрвөн талбар (бүү өөрчил).
const ugugdul = {
  ner: prompt() || "",
  email: prompt() || "",
  nuuts: prompt() || "",
  davtah: prompt() || "",
};

const aldaanuud = shalgah(ugugdul);

if (Object.keys(aldaanuud).length === 0) {
  console.log(`✓ ${ugugdul.ner.trim()} бүртгэгдлээ`);
} else {
  for (const [talbar, messej] of Object.entries(aldaanuud)) {
    console.log(`✗ ${talbar}: ${messej}`);
  }
}
""",
                tips="""\
- `davtah`-ын хоёр дахь дүрэм өөр талбарыг (`nuuts`) харах ёстой. Дүрмийн
  функцэд бүх өгөгдлийг **хоёр дахь аргумент** болгож өг. Нэг параметртэй
  хуучин дүрмүүд илүү аргументыг зүгээр үл тооно.
- Шинэ талбар нэмэхэд `shalgah`-ын давталтыг өөрчлөх шаардлагагүй —
  `durmuud`-д жагсаалт нэмэхэд л болно. Энэ бол «дүрмийг өгөгдөл болгох»-ын
  давуу тал.
- `Object.entries` нь объектод нэмсэн дарааллаар гүйнэ — `davtah`-ыг
  `nuuts`-ийн дараа нэм.
- Алдаа байгаа эсэхийг `Object.keys(aldaanuud).length`-оор мэд.
- Амжилтын мөрөнд нэрийг `trim()`-ээр захын зайгүй болго.
""",
            ),
        ),
        LessonSpec(
            title="Төсөл — Тооцоолуур апп",
            slug="tootsooluur-app",
            description="Товчны сүлжээ, төлөв удирдах, алдаанаас сэргийлэх.",
            duration=720,
            content="""\
Модул 9-ийн тооцоолуурыг товчтой апп болгоно.

### Төлөв

Тооцоолуурт цөөн хэдэн зүйл санах хэрэгтэй:

```javascript
const tuluv = {
  odoo: "0",      // дэлгэц дээр харагдаж буй тоо
  umnuh: null,    // өмнөх тоо
  uildel: null,   // хүлээгдэж буй үйлдэл
};
```

### Товчийг нэг сонсогчоор

```html
<div id="tovchnuud">
  <button data-too="7">7</button>
  <button data-uildel="+">+</button>
</div>
```

```javascript
tovchnuud.addEventListener("click", (event) => {
  const tovch = event.target.closest("button");
  if (!tovch) {
    return;
  }

  if (tovch.dataset.too) {
    tooNemeh(tovch.dataset.too);
  }
  if (tovch.dataset.uildel) {
    uildelSongoh(tovch.dataset.uildel);
  }

  zurah();
});
```

`data-` шинж чанар нь HTML дотор жижиг мэдээлэл авч явах цэвэрхэн арга.

### Захын тохиолдлууд

Тооцоолуур нь энгийн харагддаг ч зөв бичих нь хэцүү:

| Тохиолдол | Хүлээгдэх зан төлөв |
|---|---|
| Эхлээд `0`, дараа нь `5` | `5` болно, `05` биш |
| Цэгийг хоёр удаа дарах | Нэг л цэг орно |
| Тэгд хуваах | Алдааны мессеж, апп унахгүй |
| Үйлдлийг дараалан дарах | Сүүлийнх нь солино |

Эдгээрийг тусад нь бодож үзэхгүй бол апп хачин ажиллана.

### Нэмэлт сорилт

Доорх «Даалгавар»-т `C`, `%` товч болон дараалан дарсан үйлдлийг нэмнэ —
дарсан товчнууд оролтын мөрөөр ирнэ. Дараа нь жинхэнэ хөтөчид:

1. Гараас тоо оруулах боломж нэмээрэй (`keydown` үйл явдал).
2. Сүүлийн 5 тооцооллыг түүх болгон харуулаарай.
""",
            initial_code="""\
// TODO: үйлдлийн дараа шинэ тоо бичсэн эсэхийг санах талбар нэм
const tuluv = { odoo: "0", umnuh: null, uildel: null };

// C товч — бүгдийг цэвэрлээд шинээр эхэлнэ
function tseverleh() {
  tuluv.odoo = "0";
  tuluv.umnuh = null;
  tuluv.uildel = null;
}

function tooNemeh(temdegt) {
  if (temdegt === "." && tuluv.odoo.includes(".")) {
    return; // хоёр цэг болохгүй
  }
  tuluv.odoo = tuluv.odoo === "0" && temdegt !== "." ? temdegt : tuluv.odoo + temdegt;
}

function uildelSongoh(uildel) {
  // TODO: тоо бичилгүй дараалан дарсан бол зөвхөн tuluv.uildel-ийг соль
  if (tuluv.uildel && tuluv.umnuh !== null) {
    bodoh();
  }
  tuluv.umnuh = Number(tuluv.odoo);
  tuluv.uildel = uildel;
  tuluv.odoo = "0";
}

function bodoh() {
  const a = tuluv.umnuh;
  const b = Number(tuluv.odoo);

  let ur;
  switch (tuluv.uildel) {
    case "+": ur = a + b; break;
    case "-": ur = a - b; break;
    case "*": ur = a * b; break;
    case "/": ur = b === 0 ? "Алдаа" : a / b; break;
    default: return;
  }

  tuluv.odoo = String(ur);
  tuluv.umnuh = null;
  tuluv.uildel = null;
}

// Мөрийн товч бүрийг тохирох функц руу илгээнэ: "12+8=" → 1, 2, +, 8, =
function darah(tovchnuud) {
  for (const t of tovchnuud.split("")) {
    if ("0123456789.".includes(t)) {
      tooNemeh(t);
    } else if (t === "=") {
      bodoh();
    } else {
      // TODO: "C" (цэвэрлэх), "%" (100-д хуваах) товчийг тусад нь боловсруул
      uildelSongoh(t);
    }
  }
}

// Мөр бүр — шинэ тооцоолол (бүү өөрчил).
let mur = prompt();
while (mur !== null) {
  tseverleh();
  darah(mur);
  console.log(`${mur} → ${tuluv.odoo}`);
  mur = prompt();
}
""",
            exercise=ExerciseSpec(
                statement="""\
Тооцоолуурын гурван дутууг нөх: `C` товч, `%` товч, дараалан дарсан үйлдэл.

**Оролт:** мөр бүрт дарсан товчнууд, хоорондоо зайгүй: `0`–`9`, `.`,
`+ - * /`, `=`, `C`, `%`. Мөр бүр шинэ тооцооллоор эхэлнэ (эхлэл кодод
бэлэн).

**Шинэ зан төлөв:**

- `C` — бүгдийг цэвэрлэж, `0`-ээс эхэлнэ: `99C12-2=` → `10`.
- `%` — дэлгэц дээрх тоог 100-д хуваана: `50%` → `0.5`,
  `200*15%=` → `30`.
- Тоо бичилгүй үйлдлийн товчийг дараалан дарвал **сүүлийнх нь** өмнөхийг
  солино: `5*+3=` → `8`. Харин `0` товч дарсан бол тэр нь жинхэнэ тоо:
  `3+5*0+1=` → `1`.

**Хэвээр үлдэх:** эхний `0`-ийг солино (`05` → `5`), хоёр дахь цэгийг үл
тооно (`3.1.4` → `3.14`), тэгд хуваавал `Алдаа`, үйлдлүүд зүүнээс баруун
тийш дарааллаар бодогдоно (`2+3*4=` → `20`).

**Гаралт:** мөр бүрт `<товчнууд> → <дэлгэц дээрх утга>` (эхлэл кодод бэлэн).
""",
                tests=(
                    TestCaseSpec(
                        stdin="12+8=\n7/0=\n200*15%=\n",
                        expected_output="12+8= → 20\n7/0= → Алдаа\n200*15%= → 30\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="5*+3=\n05\n3.1.4\n",
                        expected_output="5*+3= → 8\n05 → 5\n3.1.4 → 3.14\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="99C12-2=\n5+5C+1=\n2*+3=\n2+3*4=\n",
                        expected_output="99C12-2= → 10\n5+5C+1= → 1\n2*+3= → 5\n2+3*4= → 20\n",
                    ),
                    TestCaseSpec(
                        stdin="1.5*4=\n8-/2=\n50%\n",
                        expected_output="1.5*4= → 6\n8-/2= → 4\n50% → 0.5\n",
                    ),
                    TestCaseSpec(
                        stdin="3+5*0+1=\n10/4*2=\n-5+2=\n6/-1=\n0*5=\n",
                        expected_output=(
                            "3+5*0+1= → 1\n10/4*2= → 5\n-5+2= → -3\n6/-1= → 5\n0*5= → 0\n"
                        ),
                    ),
                ),
                solution="""\
// shine: үйлдлийн товч дарсны дараа шинэ тоо хараахан бичээгүй бол true.
const tuluv = { odoo: "0", umnuh: null, uildel: null, shine: false };

// C товч — бүгдийг цэвэрлээд шинээр эхэлнэ
function tseverleh() {
  tuluv.odoo = "0";
  tuluv.umnuh = null;
  tuluv.uildel = null;
  tuluv.shine = false;
}

function tooNemeh(temdegt) {
  tuluv.shine = false; // тоо бичиж эхэллээ
  if (temdegt === "." && tuluv.odoo.includes(".")) {
    return; // хоёр цэг болохгүй
  }
  tuluv.odoo = tuluv.odoo === "0" && temdegt !== "." ? temdegt : tuluv.odoo + temdegt;
}

function uildelSongoh(uildel) {
  if (tuluv.uildel && tuluv.shine) {
    tuluv.uildel = uildel; // дараалан дарсан — сүүлийнх нь солино
    return;
  }
  if (tuluv.uildel && tuluv.umnuh !== null) {
    bodoh();
  }
  tuluv.umnuh = Number(tuluv.odoo);
  tuluv.uildel = uildel;
  tuluv.odoo = "0";
  tuluv.shine = true;
}

function huvi() {
  tuluv.odoo = String(Number(tuluv.odoo) / 100);
}

function bodoh() {
  const a = tuluv.umnuh;
  const b = Number(tuluv.odoo);

  let ur;
  switch (tuluv.uildel) {
    case "+": ur = a + b; break;
    case "-": ur = a - b; break;
    case "*": ur = a * b; break;
    case "/": ur = b === 0 ? "Алдаа" : a / b; break;
    default: return;
  }

  tuluv.odoo = String(ur);
  tuluv.umnuh = null;
  tuluv.uildel = null;
  tuluv.shine = false;
}

// Мөрийн товч бүрийг тохирох функц руу илгээнэ: "12+8=" → 1, 2, +, 8, =
function darah(tovchnuud) {
  for (const t of tovchnuud.split("")) {
    if ("0123456789.".includes(t)) {
      tooNemeh(t);
    } else if (t === "=") {
      bodoh();
    } else if (t === "C") {
      tseverleh();
    } else if (t === "%") {
      huvi();
    } else {
      uildelSongoh(t);
    }
  }
}

// Мөр бүр — шинэ тооцоолол (бүү өөрчил).
let mur = prompt();
while (mur !== null) {
  tseverleh();
  darah(mur);
  console.log(`${mur} → ${tuluv.odoo}`);
  mur = prompt();
}
""",
                tips="""\
- `darah` нь товч бүрийг тохирох функц руу илгээдэг. `C`, `%`-д шинэ салаа
  нэмэхгүй бол тэд үйлдлийн товч гэж ойлгогдоно.
- `%` нь зөвхөн `tuluv.odoo`-г өөрчилнө. Тэр нь мөр тул тоо болгож хуваагаад
  `String(...)`-ээр буцааж мөр болго.
- «Тоо бичилгүй дараалан дарсан»-ыг `tuluv.odoo === "0"`-оор танивал
  `5*0+`-д хэрэглэгчийн бичсэн `0`-ийг андуурна. Төлөвт тусдаа тэмдэг нэм:
  үйлдэл сонгоход `true`, тоо бичихэд `false`, цэвэрлэх, бодоход `false`.
- Тэмдэг `true`, үйлдэл хүлээгдэж байгаа үед `bodoh()`-ыг дуудалгүй зөвхөн
  `tuluv.uildel`-ийг солиод функцээс гар.
""",
            ),
        ),
        LessonSpec(
            title="Төсөл — Энгийн самбар",
            slug="engiin-sambar",
            description="Өгөгдлийг нэгтгэж, шүүж, хүснэгтээр харуулах.",
            duration=720,
            content="""\
Борлуулалтын жижиг самбар бичнэ: нийт үзүүлэлт, шүүлтүүр, эрэмбэлэлт.

### Өгөгдлөөс үзүүлэлт рүү

Самбарын гол ажил бол **түүхий өгөгдлийг** ойлгомжтой тоо болгох:

```javascript
const niit = zahialguud.reduce((dun, z) => dun + z.dun, 0);
const dundaj = niit / zahialguud.length;
const hamgiinIh = zahialguud.reduce((ih, z) => (z.dun > ih ? z.dun : ih), 0);
```

### Бүлэглэх

`reduce` ашиглан ангилал тус бүрийн нийлбэрийг гаргана. Энд
хуримтлуулагч нь `{}` хоосон объектоос эхэлж, ангиллын нэр бүрт нэг
талбартай болно:

```javascript
const angilalaar = zahialguud.reduce((dun, z) => {
  // Энэ ангилал анх удаа тааралдвал 0-ээс эхэлнэ
  dun[z.angilal] = (dun[z.angilal] || 0) + z.dun;
  return dun;
}, {});
// { Сургалт: 165000, Хоол: 31500, Техник: 180000 }
```

### Эрэмбэлэх

`sort` нь **эх массивыг өөрчилдөг** тул эхлээд хуулбар ав:

```javascript
const erembelsen = [...zahialguud].sort((a, b) => b.dun - a.dun);
```

Тоо эрэмбэлэхэд харьцуулах функц **заавал** хэрэгтэй. Үгүй бол
JavaScript тоонуудыг мөр болгож эрэмбэлнэ:

```javascript
[10, 9, 100].sort();              // [10, 100, 9] — буруу!
[10, 9, 100].sort((a, b) => a - b); // [9, 10, 100]
```

### Хүснэгт зурах

```javascript
function zurah(muruud) {
  hussnegtiinBie.replaceChildren();

  for (const mur of muruud) {
    const tr = document.createElement("tr");
    tr.innerHTML = "";

    for (const utga of [mur.ner, mur.angilal, mur.dun]) {
      const td = document.createElement("td");
      td.textContent = utga;
      tr.append(td);
    }

    hussnegtiinBie.append(tr);
  }
}
```

### Нэмэлт сорилт

Доорх «Даалгавар»-т захиалгууд оролтын мөрөөр ирж, самбарын үзүүлэлт ба
хамгийн их дүнтэй 3 захиалгыг гаргана. Дараа нь жинхэнэ хөтөчид:

1. Ангилалаар шүүх сонголт нэмээрэй.
2. Багана дээр дарахад эрэмбэ солигддог болгоорой.
""",
            initial_code="""\
// Мөр бүр: нэр,ангилал,дүн — zahialguud массив болгон уншина (бүү өөрчил).
const zahialguud = [];
let mur = prompt();
while (mur !== null) {
  const [ner, angilal, dun] = mur.split(",");
  zahialguud.push({ ner, angilal, dun: Number(dun) });
  mur = prompt();
}

// --- Нийт үзүүлэлт -------------------------------------------------------
const niit = zahialguud.reduce((dun, z) => dun + z.dun, 0);

console.log(`Захиалга: ${zahialguud.length}`);
console.log(`Нийт: ${niit}₮`);
// TODO: "Дундаж: <дүн>₮" — бүхэл болгож тойруулна

// --- Ангилалаар бүлэглэх -------------------------------------------------
const angilalaar = zahialguud.reduce((dun, z) => {
  dun[z.angilal] = (dun[z.angilal] || 0) + z.dun;
  return dun;
}, {});

console.log("--- Ангилалаар ---");
// TODO: ангиллуудыг нийлбэрээр ихээс бага руу эрэмбэлж, хувийг нь нэм
for (const [angilal, dun] of Object.entries(angilalaar)) {
  console.log(`${angilal}: ${dun}₮`);
}

// --- Их дүнгээр ----------------------------------------------------------
console.log("--- Их дүнгээр ---");
// TODO: хуулбарыг дүнгээр эрэмбэлж, эхний 3-ыг "1. <нэр> — <дүн>₮" гэж хэвлэ

console.log(`Эхний бичлэг: ${zahialguud[0].ner}`);
""",
            exercise=ExerciseSpec(
                statement="""\
Борлуулалтын самбарыг оролтын өгөгдлөөс гарга: нийт үзүүлэлт, ангиллаар
бүлэглэсэн дүн, хамгийн их дүнтэй 3 захиалга.

**Оролт:** мөр бүрт нэг захиалга `нэр,ангилал,дүн` (дүн нь бүхэл тоо), дор
хаяж нэг мөр. Уншиж `zahialguud` массив болгох хэсэг эхлэл кодод бэлэн.

**Гаралт:**

```text
Захиалга: <захиалгын тоо>
Нийт: <нийлбэр>₮
Дундаж: <нийлбэр / тоо>₮
--- Ангилалаар ---
<ангилал>: <ангиллын нийлбэр>₮ (<хувь>%)
--- Их дүнгээр ---
1. <нэр> — <дүн>₮
2. <нэр> — <дүн>₮
3. <нэр> — <дүн>₮
Эхний бичлэг: <оролтын эхний захиалгын нэр>
```

- Дундаж ба хувийг `Math.round`-оор бүхэл болго. Хувь нь
  `ангиллын нийлбэр / нийт × 100`.
- Ангиллуудыг нийлбэрээр нь **ихээс бага руу** эрэмбэл.
- «Их дүнгээр» хэсэгт дүнгээр ихээс бага руу эрэмбэлсэн эхний 3 захиалга
  (3-аас цөөн бол байгааг нь бүгдийг). Дүн тэнцүү бол оролтын дарааллаар.
- Сүүлийн мөр нь **эх массив** өөрчлөгдөөгүйг харуулна — эрэмбэлэхдээ
  хуулбар ав.
- Тоог `toLocaleString`-гүй, шууд хэвлэ.
""",
                tests=(
                    TestCaseSpec(
                        stdin=(
                            "Ном,Сургалт,45000\nКурс,Сургалт,120000\nКофе,Хоол,8500\n"
                            "Хоол,Хоол,23000\nЧихэвч,Техник,180000\n"
                        ),
                        expected_output=(
                            "Захиалга: 5\n"
                            "Нийт: 376500₮\n"
                            "Дундаж: 75300₮\n"
                            "--- Ангилалаар ---\n"
                            "Техник: 180000₮ (48%)\n"
                            "Сургалт: 165000₮ (44%)\n"
                            "Хоол: 31500₮ (8%)\n"
                            "--- Их дүнгээр ---\n"
                            "1. Чихэвч — 180000₮\n"
                            "2. Курс — 120000₮\n"
                            "3. Ном — 45000₮\n"
                            "Эхний бичлэг: Ном\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="Дэвтэр,Бичиг,3000\nҮзэг,Бичиг,1500\n",
                        expected_output=(
                            "Захиалга: 2\n"
                            "Нийт: 4500₮\n"
                            "Дундаж: 2250₮\n"
                            "--- Ангилалаар ---\n"
                            "Бичиг: 4500₮ (100%)\n"
                            "--- Их дүнгээр ---\n"
                            "1. Дэвтэр — 3000₮\n"
                            "2. Үзэг — 1500₮\n"
                            "Эхний бичлэг: Дэвтэр\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin=(
                            "Алим,Жимс,9000\nБанана,Жимс,10000\nЗурагт,Техник,100000\n"
                            "Утас,Техник,100000\nГадил,Жимс,900\n"
                        ),
                        expected_output=(
                            "Захиалга: 5\n"
                            "Нийт: 219900₮\n"
                            "Дундаж: 43980₮\n"
                            "--- Ангилалаар ---\n"
                            "Техник: 200000₮ (91%)\n"
                            "Жимс: 19900₮ (9%)\n"
                            "--- Их дүнгээр ---\n"
                            "1. Зурагт — 100000₮\n"
                            "2. Утас — 100000₮\n"
                            "3. Банана — 10000₮\n"
                            "Эхний бичлэг: Алим\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="Цүнх,Хувцас,65000\n",
                        expected_output=(
                            "Захиалга: 1\n"
                            "Нийт: 65000₮\n"
                            "Дундаж: 65000₮\n"
                            "--- Ангилалаар ---\n"
                            "Хувцас: 65000₮ (100%)\n"
                            "--- Их дүнгээр ---\n"
                            "1. Цүнх — 65000₮\n"
                            "Эхний бичлэг: Цүнх\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="Бэх,Бичиг,1000\nАяга,Гэр,700\nТаваг,Гэр,300\nЦаас,Бичиг,1\n",
                        expected_output=(
                            "Захиалга: 4\n"
                            "Нийт: 2001₮\n"
                            "Дундаж: 500₮\n"
                            "--- Ангилалаар ---\n"
                            "Бичиг: 1001₮ (50%)\n"
                            "Гэр: 1000₮ (50%)\n"
                            "--- Их дүнгээр ---\n"
                            "1. Бэх — 1000₮\n"
                            "2. Аяга — 700₮\n"
                            "3. Таваг — 300₮\n"
                            "Эхний бичлэг: Бэх\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="Тоглоом,Хүүхэд,25\nНом,Сургалт,100\nБөмбөг,Хүүхэд,80\n",
                        expected_output=(
                            "Захиалга: 3\n"
                            "Нийт: 205₮\n"
                            "Дундаж: 68₮\n"
                            "--- Ангилалаар ---\n"
                            "Хүүхэд: 105₮ (51%)\n"
                            "Сургалт: 100₮ (49%)\n"
                            "--- Их дүнгээр ---\n"
                            "1. Ном — 100₮\n"
                            "2. Бөмбөг — 80₮\n"
                            "3. Тоглоом — 25₮\n"
                            "Эхний бичлэг: Тоглоом\n"
                        ),
                    ),
                ),
                solution="""\
// Мөр бүр: нэр,ангилал,дүн — zahialguud массив болгон уншина (бүү өөрчил).
const zahialguud = [];
let mur = prompt();
while (mur !== null) {
  const [ner, angilal, dun] = mur.split(",");
  zahialguud.push({ ner, angilal, dun: Number(dun) });
  mur = prompt();
}

// --- Нийт үзүүлэлт -------------------------------------------------------
const niit = zahialguud.reduce((dun, z) => dun + z.dun, 0);
const dundaj = Math.round(niit / zahialguud.length);

console.log(`Захиалга: ${zahialguud.length}`);
console.log(`Нийт: ${niit}₮`);
console.log(`Дундаж: ${dundaj}₮`);

// --- Ангилалаар бүлэглэх -------------------------------------------------
const angilalaar = zahialguud.reduce((dun, z) => {
  dun[z.angilal] = (dun[z.angilal] || 0) + z.dun;
  return dun;
}, {});

console.log("--- Ангилалаар ---");
// [ангилал, дүн] хосуудыг дүнгээр (индекс 1) нь ихээс бага руу
const angilaluud = Object.entries(angilalaar).sort((a, b) => b[1] - a[1]);
for (const [angilal, dun] of angilaluud) {
  const huvi = Math.round((dun / niit) * 100);
  console.log(`${angilal}: ${dun}₮ (${huvi}%)`);
}

// --- Их дүнгээр ----------------------------------------------------------
console.log("--- Их дүнгээр ---");
// sort эх массивыг өөрчилдөг тул хуулбарыг эрэмбэлнэ
const erembelsen = [...zahialguud].sort((a, b) => b.dun - a.dun);
erembelsen.slice(0, 3).forEach((z, i) => {
  console.log(`${i + 1}. ${z.ner} — ${z.dun}₮`);
});

console.log(`Эхний бичлэг: ${zahialguud[0].ner}`);
""",
                tips="""\
- Бүлэглэсэн объектыг `Object.entries(...)`-ээр `[ангилал, дүн]` хосуудын
  массив болгоод эрэмбэл. Хосын дүн нь `[1]` индекст.
- Тоогоор эрэмбэлэхэд харьцуулах функц заавал хэрэгтэй. Ихээс бага руу бол
  `b`-гээс `a`-г хас.
- `sort` эх массивыг өөрчилнө. `zahialguud`-ыг шууд эрэмбэлбэл «Эхний
  бичлэг» буруу гарна — `[...zahialguud]` хуулбараар эрэмбэл.
- Эхний 3-ыг `slice(0, 3)`-аар ав — 3-аас цөөн бол байгааг нь буцаана.
  Дугаарыг `forEach`-ийн хоёр дахь параметр (индекс) + 1-ээс ав.
- `sort` тэнцүү утгуудын дарааллыг хадгалдаг — тэнцүү дүнд тусад нь юу ч
  хийх шаардлагагүй.
""",
            ),
        ),
    ],
)
