"""Модул 5 — Effect.

Component-ийг React-ийн гаднах системтэй (хөтчийн гарчиг, гарын товчлуур,
timer, сервер) синхрончлох `useEffect`, хамаарлын массив, цэвэрлэгээ,
өгөгдөл татах, уралдааны нөхцөлийг үзэж, effect хэрэггүй тохиолдлыг
таньж сурна. Төгсгөлд нь хайлтын апп бүтээнэ.
"""

from app.content.react.common import solution, test, vite
from app.content.types import ExerciseSpec, LessonSpec, ModuleSpec
from app.models.enums import LessonLanguage

JSX = LessonLanguage.JSX

# Модулийн бүх хичээлд ижил, түгжигдсэн загвар.
EFFECT_CSS = """\
body {
  font-family: system-ui, sans-serif;
  color: #1f2328;
}
main {
  max-width: 560px;
}
button {
  margin: 4px 8px 4px 0;
  padding: 8px 14px;
  border: 0;
  border-radius: 8px;
  background: #15803d;
  color: #fff;
  font: inherit;
  cursor: pointer;
}
button:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}
button[aria-pressed="true"] {
  background: #14532d;
  outline: 2px solid #86efac;
}
label {
  display: block;
  margin: 12px 0 4px;
  font-weight: 600;
}
label:has(> input[type="checkbox"]) {
  font-weight: 400;
}
input:not([type="checkbox"]),
select {
  display: block;
  box-sizing: border-box;
  width: 100%;
  margin-top: 4px;
  padding: 8px 10px;
  border: 1px solid #c4c9d0;
  border-radius: 8px;
  font: inherit;
  font-weight: 400;
}
ul {
  padding-left: 20px;
}
li {
  margin: 4px 0;
}
.muted {
  color: #57606a;
}
.error {
  color: #b42318;
}
.card {
  margin-top: 12px;
  padding: 12px 16px;
  border: 1px solid #d0d7de;
  border-radius: 12px;
  background: #f6f8fa;
}
.big {
  display: block;
  font-size: 48px;
  line-height: 1.2;
}
.display {
  font-size: 40px;
  font-variant-numeric: tabular-nums;
  margin: 12px 0;
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 10px;
}
.tile {
  margin: 0;
  padding: 12px;
  border: 1px solid #d0d7de;
  background: #fff;
  color: #1f2328;
}
.lightbox {
  position: fixed;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(15, 23, 42, 0.92);
  color: #fff;
}
.lightbox .big {
  font-size: 96px;
}
"""

EFFECTS = ModuleSpec(
    title="Модул 5 — Effect",
    description="Effect-ээр гадаад системтэй синхрончилж, timer, listener, өгөгдөл татах, цэвэрлэгээг зөв бичнэ.",
    lessons=[
        # --- 1 ------------------------------------------------------------------
        LessonSpec(
            title="useEffect: гадаад системтэй синхрончлох",
            slug="useeffect",
            description="Render-ийн дараа ажилладаг effect-ээр хөтчийн tab-ийн гарчгийг state-тэй синхрончилно.",
            duration=840,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Effect гэж юу болох, render-ээс юугаараа ялгаатайг ойлгох
- `useEffect`-ийг бичиж, render-ийн **дараа** ажилладгийг ажиглах
- Хөтчийн tab-ийн гарчиг `document.title`-ийг state-тэй синхрончлох

### Яагаад чухал вэ

Одоог хүртэл component-ууд зөвхөн props, state-ээс JSX тооцоолж ирлээ.
Гэвч бодит апп React-ийн удирддаггүй зүйлстэй харилцах шаардлагатай:
хөтчийн tab-ийн гарчиг, timer, гарын товчлуурын event, серверийн API,
`localStorage`, газрын зураг, видео тоглуулагч. Эдгээрийг **гадаад
систем** гэнэ.

Component-ийн render **цэвэр** байх ёстой (Модул 2): ижил props, state →
ижил JSX, гадаад ертөнцөд хүрэхгүй. Тэгвэл гадаад ертөнцийг өөрчлөх кодоо
хаана бичих вэ? Хоёр газар бий:

- **Event handler** — хэрэглэгчийн тодорхой үйлдлээс болж ажиллах код.
  «Захиалах» дарахад захиалга илгээх.
- **Effect** — component дэлгэцэд харагдаж байгаагаас болж ажиллах код.
  «Уншаагүй 3 мессеж харагдаж байгаа бол tab-ийн гарчиг "(3) Мессеж" байх
  ёстой».

Facebook, Gmail яг ингэж уншаагүй мессежийн тоогоо tab-ийн гарчигт
харуулдаг.

### useEffect

```jsx
import { useEffect, useState } from "react";

export default function App() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    document.title = `Дарсан: ${count}`;
  });

  return <button onClick={() => setCount(count + 1)}>Дарсан: {count}</button>;
}
```

- `useEffect(setup)` — эхний аргумент нь функц. React түүнийг render
  дуусч, DOM шинэчлэгдсэний **дараа** дуудна.
- Бусад hook шиг component-ийн дээд түвшинд л дуудна — `if`, давталт
  дотор биш.
- Хоёр дахь аргумент буюу хамаарлын массивыг дараагийн хичээлд үзнэ.
  Түүнгүй бол effect **render бүрийн дараа** ажиллана.

### Хэзээ ажилладаг вэ

```jsx
function App() {
  console.log("1. render эхэллээ");

  useEffect(() => {
    console.log("3. effect");
  });

  console.log("2. JSX буцаах гэж байна");
  return <p>Сайн уу</p>;
}
```

Console-д 1, 2, 3 гэсэн дарааллаар гарна. `useEffect` мөр 1, 2-ын хооронд
бичигдсэн ч доторх функц нь эхлээд зөвхөн «хадгалагдаж», дараа нь
ажиллана:

1. React `App`-ийг дуудна — **render**.
2. React DOM-ыг шинэчилнэ — **commit**.
3. React effect-үүдийг ажиллуулна.

Тиймээс effect ажиллах үед дэлгэцэнд харагдаж буй зүйл state-тэй аль
хэдийн таарч байна.

### document.title — хөтчийн tab-ийн гарчиг

`document.title` нь хуудасны `<title>` буюу хөтчийн tab дээр бичигдсэн
текст. Энэ засварлагчид «Хөтөч»-ийн дээд мөрөнд, хаягийн баруун талд
харагдана (өргөн дэлгэц дээр). Одоо тэнд «React App» гэж байгаа.
Даалгаврыг хийсний дараа товч дарах бүрт тэр текст өөрчлөгдөхийг
ажиглаарай.

Яагаад render дотор шууд бичиж болохгүй вэ?

```jsx
function App() {
  const [count, setCount] = useState(0);
  document.title = `Дарсан: ${count}`; // ❌ render-ийн үеэр гадаад ертөнцийг өөрчилнө
  // ...
}
```

Энд ажиллаж байгаа мэт харагдах ч React render-ийг хэд хэдэн удаа, эсвэл
дэлгэцэнд гаргахгүйгээр дуудаж болно (StrictMode, transition — хожим
үзнэ). Render үеийн гадаад өөрчлөлт урьдчилан таамаглашгүй болно. Effect
харин зөвхөн дэлгэцэнд үнэхээр гарсны дараа ажилладаг.

### Effect бол «синхрончлол»

Effect-ийг «X болоход Y хий» гэж бус, «гадаад системийг одоогийн
state-тэй **ижил байлга**» гэж бод. Гарчиг = f(count). `count` өөрчлөгдөж
component дахин render хийх бүрт effect дахин ажиллаж, гарчгийг state-тэй
тааруулна.

Бодит Vite төсөлд ч яг ижил: `import { useEffect } from "react"`. React
19-д `<title>`-ийг component дотроо шууд render хийж болдог — React
түүнийг `<head>` руу зөөнө. Гэхдээ effect-ийн зарчим timer, listener,
сүлжээний хүсэлт гээд бүх гадаад системд ижил тул энэ хичээлд
`document.title`-аар дадлага хийнэ.

### Түгээмэл алдаа

- **`import`-оо мартах.** `useEffect is not defined` алдаа гарна.
- **Нөхцөл дотор дуудах.** `if (count > 0) useEffect(…)` нь hook-ийн
  дүрмийг зөрчинө. Нөхцөлийг effect-ийн **дотор** бич.
- **Effect дотор state өөрчлөх.** Хамаарлын массивгүй effect дотор
  `setCount` дуудвал render → effect → render … гэж төгсгөлгүй
  давтагдана. Дараагийн хичээлүүдэд дэлгэрэнгүй үзнэ.

Өөрийгөө шалга — дараах component-ийг ажигла:

```jsx
function App() {
  console.log("A");
  useEffect(() => {
    console.log("B");
  });
  console.log("C");
  return null;
}
```

```quiz
Дээрх `App` анх render хийхэд Console-д ямар дарааллаар гарах вэ?
- [ ] A, B, C
- [x] A, C, B
- [ ] B, A, C
> Effect-ийн функц render дуусч, DOM шинэчлэгдсэний дараа л ажиллана.
```

```quiz
Аль нь effect-ийн ажил вэ?
- [ ] Сагсан дахь барааны нийт үнийг тооцох
- [ ] «Захиалах» товч дарахад захиалга илгээх
- [x] Уншаагүй мессежийн тоог tab-ийн гарчигт байнга харуулж байх
> Нийт үнийг render дотор тооцно, товчны үйлдэл event handler-т бичигдэнэ. Гарчгийг state-тэй ижил байлгах нь гадаад системтэй синхрончлох ажил.
```

### Дүгнэлт

Effect нь component-ийг React-ийн гаднах систем (хөтчийн гарчиг, timer,
сервер)-тэй синхрончилно. `useEffect(() => { … })` доторх код render,
commit дууссаны дараа ажиллана. Render-ийг цэвэр байлгаж, гадаад
өөрчлөлтийг effect-д шилжүүл.
""",
            initial_code=vite(
                """\
import { useState } from "react";

export default function App() {
  const [unread, setUnread] = useState(0);

  // TODO: useEffect ашиглан document.title-ийг unread-тэй синхрончил:
  //   unread > 0 бол "(3) Мессеж", 0 бол "Мессеж"

  return (
    <main>
      <h1>📨 Мессеж</h1>
      <p>Уншаагүй: {unread}</p>
      <button onClick={() => setUnread((n) => n + 1)}>Шинэ мессеж ирэх</button>
      <button onClick={() => setUnread(0)}>Бүгдийг уншсан</button>
    </main>
  );
}
""",
                css=EFFECT_CSS,
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐ · 8 минут

Мессежийн апп уншаагүй мессежийн тоог дэлгэцэнд харуулж байгаа ч
хөтчийн tab-ийн гарчиг «React App» хэвээр байна. `useEffect` ашиглан
`document.title`-ийг `unread`-тэй синхрончил: уншаагүй мессеж байвал
«(3) Мессеж», байхгүй бол «Мессеж». «Хөтөч»-ийн дээд мөрөнд гарчиг
хэрхэн өөрчлөгдөхийг хараарай.
""",
                tests=(
                    test(
                        "Эхлэхэд хуудасны гарчиг «Мессеж» байна",
                        """
render(<App />);
expect(document.title).toBe("Мессеж");
""",
                    ),
                    test(
                        "Шинэ мессеж ирэхэд гарчиг «(N) Мессеж» болно",
                        """
render(<App />);
const button = screen.getByRole("button", { name: "Шинэ мессеж ирэх" });
await user.click(button);
expect(document.title).toBe("(1) Мессеж");
await user.click(button);
expect(document.title).toBe("(2) Мессеж");
""",
                    ),
                    test(
                        "«Бүгдийг уншсан» дарахад гарчиг «Мессеж» болж буцна",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: "Шинэ мессеж ирэх" }));
await user.click(screen.getByRole("button", { name: "Бүгдийг уншсан" }));
expect(document.title).toBe("Мессеж");
expect(screen.text()).toContain("Уншаагүй: 0");
""",
                    ),
                ),
                tips="""\
- `useEffect`-ийг `useState`-ийн хажууд `react`-аас импортол.
- Effect дотор гарчгийг нөхцөлөөр тооцоол: `unread > 0` бол
  `` `(${unread}) Мессеж` ``, эс бөгөөс `"Мессеж"`. Хаалтны дараа нэг зай
  байна.
- `document.title = …`-ийг render дотор шууд бичвэл тест давж магадгүй ч
  энэ нь буруу зуршил. Гадаад системд хүрэх кодыг effect дотор бич.
""",
                solution=solution(
                    App_jsx="""\
import { useEffect, useState } from "react";

export default function App() {
  const [unread, setUnread] = useState(0);

  useEffect(() => {
    document.title = unread > 0 ? `(${unread}) Мессеж` : "Мессеж";
  });

  return (
    <main>
      <h1>📨 Мессеж</h1>
      <p>Уншаагүй: {unread}</p>
      <button onClick={() => setUnread((n) => n + 1)}>Шинэ мессеж ирэх</button>
      <button onClick={() => setUnread(0)}>Бүгдийг уншсан</button>
    </main>
  );
}
"""
                ),
            ),
        ),
        # --- 2 ------------------------------------------------------------------
        LessonSpec(
            title="Хамаарлын массив",
            slug="effect-hamaaral",
            description="Effect хэзээ дахин ажиллахыг хамаарлын массиваар удирдана: массивгүй, [] ба [утгууд].",
            duration=900,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Effect-ийн хоёр дахь аргумент — хамаарлын массивыг (dependency array)
  ойлгох
- Массивгүй, `[]`, `[page]` гурвын ялгааг мэдэх
- Effect дотор уншсан бүх reactive утгыг массивт бичих дүрмийг сурах
- Объект, функц хамаарлын хавхыг таних

### Яагаад чухал вэ

Массивгүй effect render бүрийн дараа ажиллана. Input-д үсэг бичих бүрт
component дахин render хийдэг тул effect ч үсэг бүрт ажиллана. Гарчиг
солиход энэ нь асуудалгүй. Харин сервер рүү хүсэлт илгээх, статистикийн
event бүртгэх, чат руу холбогдох effect бол «алим» гэж бичихэд 4 хүсэлт,
4 event болно. Хэрэглэгч хэдэн хуудас үзснийг тоолох статистик худлаа
гарна.

### Гурван хэлбэр

```jsx
useEffect(() => {
  // 1. render бүрийн дараа
});

useEffect(() => {
  // 2. зөвхөн анх дэлгэцэнд гарахад (mount) нэг удаа
}, []);

useEffect(() => {
  // 3. анх гарахад + page өөрчлөгдөх бүрт
}, [page]);
```

| Бичлэг | Хэзээ ажиллах | Жишээ |
|---|---|---|
| массивгүй | Render бүрийн дараа | Ховор хэрэгтэй |
| `[]` | Зөвхөн mount үед нэг удаа | Апп нээгдсэнийг бүртгэх, listener нэмэх |
| `[a, b]` | Mount + `a` эсвэл `b` өөрчлөгдөхөд | Сонгосон хуудас, хайлтын үгээр өгөгдөл татах |

**Mount** гэдэг нь component анх удаа дэлгэцэнд гарахыг, **unmount** нь
дэлгэцээс алга болохыг хэлнэ.

### React хэрхэн шалгадаг вэ

Render бүрийн дараа React массивын утга бүрийг өмнөх render-ийнхтэй
`Object.is`-ээр (бараг `===`) харьцуулна. Бүгд ижил бол effect-ийг
алгасна, ядаж нэг нь өөр бол ажиллуулна.

```jsx
const [page, setPage] = useState("Нүүр");
const [query, setQuery] = useState("");

useEffect(() => {
  console.log("Хуудас үзэв:", page);
}, [page]);
```

- Хайлтад бичих → render → `page` ижил → effect алгасагдана.
- «Бараа» tab дарах → render → `page` өөр → effect ажиллана.

### Дүрэм: effect дотор уншсан бүхнийг бич

Хамаарлыг бид дураараа «сонгодоггүй» — код өөрөө тодорхойлно. Effect
дотор уншсан **reactive утга** бүр массивт байх ёстой. Reactive утга гэдэг
нь render бүрт өөр байж болох бүхэн: props, state, component дотор
зарласан хувьсагч, функц.

```jsx
function Greeting({ name }) {
  const [lang, setLang] = useState("mn");

  useEffect(() => {
    document.title = lang === "mn" ? `Сайн уу, ${name}` : `Hello, ${name}`;
  }, [lang]); // ❌ name дутуу — name өөрчлөгдөхөд гарчиг хуучирна
  // ...
}
```

Зөв нь `[lang, name]`. Массивт бичих шаардлагагүй зүйлс:

- Component-ийн **гадна** зарласан тогтмол, импорт (`PAGES`, `track`);
- `useState`-ийн `setX` функц — React түүнийг үргэлж ижил байлгадаг.

Бодит Vite төсөлд `eslint-plugin-react-hooks`-ийн `exhaustive-deps` дүрэм
дутуу хамаарлыг засварлагч дээр шууд сануулдаг. Энэ засварлагчид ESLint
байхгүй тул өөрөө нягтлаарай.

### Хуучирсан утга (stale closure)

```jsx
useEffect(() => {
  console.log("Хуудас:", page);
}, []); // ❌ Үргэлж эхний page-ийг хэвлэнэ
```

Effect өөрийг нь үүсгэсэн render-ийн утгуудыг «хардаг» — Модул 3-ын
snapshot-ийг санаарай. `[]` бол effect дахин үүсэхгүй тул зөвхөн эхний
render-ийн `page`-ийг мэднэ. Массивыг `[page]` болговол хуудас солигдох
бүрт шинэ утгатай effect үүснэ.

### Объект ба функц хамаарал

```jsx
function Weather({ city }) {
  const options = { city, units: "C" }; // render бүрт ШИНЭ объект

  useEffect(() => {
    console.log("Цаг агаар татах:", options.city);
  }, [options]); // ❌ render бүрт ажиллана
  // ...
}
```

`Object.is({}, {})` нь `false` — агуулга ижил ч хоёр өөр объект. Тиймээс
хамаарал «үргэлж өөрчлөгдсөн» гэж тооцогдоно. Засахдаа энгийн утгыг
хамаарал болго (`[city]`), эсвэл объектоо effect-ийн **дотор** үүсгэ.
Component дотор зарласан функц ч мөн render бүрт шинэ. Энэ талаар
«Танд effect хэрэггүй байж магадгүй» хичээл болон Модул 6-гийн `useMemo`,
`useCallback`-д дэлгэрэнгүй үзнэ.

Өөрийгөө шалга — дараах component-ийг ажигла:

```jsx
const [text, setText] = useState("");
const [count, setCount] = useState(0);

useEffect(() => {
  console.log("effect");
}, [count]);
```

```quiz
Дээрх component гарч ирсний дараа хэрэглэгч input-д 3 үсэг бичиж, `count`-ийг нэг удаа нэмэгдүүлэв. Console-д нийт хэдэн «effect» хэвлэгдэх вэ?
- [ ] 1
- [x] 2
- [ ] 5
> Mount үед нэг, `count` өөрчлөгдөхөд нэг. Текст бичих нь `count`-ийг өөрчлөхгүй тул effect алгасагдана.
```

```jsx
useEffect(() => {
  document.title = `${user.name} — ${tab}`;
}, [tab]);
```

```quiz
Дээрх effect-ийн алдааг ол.
- [ ] Алдаагүй, зөв бичигдсэн
- [x] `user.name` хамааралд алга — хэрэглэгч солигдоход гарчиг хуучирна
- [ ] Массив нь `[]` байх ёстой
> Effect дотор уншсан reactive утга бүр массивт байх ёстой: `[user.name, tab]`.
```

### Дүгнэлт

Массивгүй effect render бүрт, `[]` нь mount үед нэг удаа, `[a, b]` нь `a`
эсвэл `b` өөрчлөгдөхөд ажиллана. Хамаарлыг код тодорхойлно: effect дотор
уншсан props, state бүрийг бич. Объект, функц render бүрт шинэ тул
боломжтой бол энгийн утгыг хамаарал болго.
""",
            initial_code=vite(
                """\
import { useEffect, useState } from "react";
import { track } from "./analytics";

const PAGES = ["Нүүр", "Бараа", "Сагс"];

export default function App() {
  const [page, setPage] = useState("Нүүр");
  const [query, setQuery] = useState("");

  // TODO 1: «Апп нээгдлээ» нь зөвхөн нэг удаа бүртгэгдэнэ
  useEffect(() => {
    track("Апп нээгдлээ");
  });

  // TODO 2: «Хуудас: …» нь хуудас солигдох бүрт л бүртгэгдэнэ
  useEffect(() => {
    track(`Хуудас: ${page}`);
  });

  return (
    <main>
      <nav>
        {PAGES.map((name) => (
          <button key={name} aria-pressed={page === name} onClick={() => setPage(name)}>
            {name}
          </button>
        ))}
      </nav>
      <h1>{page}</h1>
      <label>
        Хайх
        <input value={query} onChange={(e) => setQuery(e.target.value)} />
      </label>
      <p className="muted">Хайлт: {query || "—"}</p>
    </main>
  );
}
""",
                locked={
                    "analytics.js": """\
// Бодит төсөлд энэ функц Google Analytics зэрэг үйлчилгээ рүү event илгээнэ.
// Энд зөвхөн жагсаалтад нэмж, Console-д хэвлэнэ.
export const events = [];

export function track(name) {
  events.push(name);
  console.log("📊", name);
}
""",
                },
                css=EFFECT_CSS,
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 10 минут

«Ногоон сагс» апп хэрэглэгчийн үйлдлийг `track()`-оор бүртгэдэг. Одоогийн
хоёр effect хамаарлын массивгүй тул хайлтад үсэг бичих бүрт хоёр event
бүртгэгдэж байна — Console-оос хар. Хамаарлын массив нэмж, «Апп
нээгдлээ» нэг л удаа, «Хуудас: …» хуудас солигдох бүрт л бүртгэгддэг
болго.
""",
                tests=(
                    test(
                        "Апп нээгдэхэд «Апп нээгдлээ», «Хуудас: Нүүр» тус бүр нэг удаа бүртгэгдэнэ",
                        """
render(<App />);
const { events } = mod("./analytics");
expect(events.filter((name) => name === "Апп нээгдлээ")).toHaveLength(1);
expect(events.filter((name) => name === "Хуудас: Нүүр")).toHaveLength(1);
expect(events).toHaveLength(2);
""",
                    ),
                    test(
                        "Хайлтад бичихэд шинэ event бүртгэгдэхгүй",
                        """
render(<App />);
const { events } = mod("./analytics");
await user.type(screen.getByLabelText("Хайх"), "алим");
expect(screen.text()).toContain("Хайлт: алим");
expect(events).toHaveLength(2);
""",
                    ),
                    test(
                        "Хуудас солиход шинэ хуудас нэг удаа бүртгэгдэж, «Апп нээгдлээ» давтагдахгүй",
                        """
render(<App />);
const { events } = mod("./analytics");
await user.click(screen.getByRole("button", { name: "Бараа" }));
await user.click(screen.getByRole("button", { name: "Сагс" }));
expect(events.filter((name) => name === "Апп нээгдлээ")).toHaveLength(1);
expect(events.filter((name) => name === "Хуудас: Бараа")).toHaveLength(1);
expect(events.filter((name) => name === "Хуудас: Сагс")).toHaveLength(1);
expect(events).toHaveLength(4);
""",
                    ),
                ),
                tips="""\
- Effect бүрт «энэ код юунаас хамаарч дахин ажиллах ёстой вэ?» гэж асуу.
- «Апп нээгдлээ» нь юу ч уншдаггүй → хоосон массив `[]`.
- «Хуудас: …» нь `page`-ийг уншдаг → `[page]`. `query`-г бичвэл хайлтад
  бичих бүрт дахин бүртгэнэ.
- `track` нь component-ийн гадна импортлогдсон тул массивт бичих
  шаардлагагүй.
""",
                solution=solution(
                    App_jsx="""\
import { useEffect, useState } from "react";
import { track } from "./analytics";

const PAGES = ["Нүүр", "Бараа", "Сагс"];

export default function App() {
  const [page, setPage] = useState("Нүүр");
  const [query, setQuery] = useState("");

  useEffect(() => {
    track("Апп нээгдлээ");
  }, []);

  useEffect(() => {
    track(`Хуудас: ${page}`);
  }, [page]);

  return (
    <main>
      <nav>
        {PAGES.map((name) => (
          <button key={name} aria-pressed={page === name} onClick={() => setPage(name)}>
            {name}
          </button>
        ))}
      </nav>
      <h1>{page}</h1>
      <label>
        Хайх
        <input value={query} onChange={(e) => setQuery(e.target.value)} />
      </label>
      <p className="muted">Хайлт: {query || "—"}</p>
    </main>
  );
}
"""
                ),
            ),
        ),
        # --- 3 ------------------------------------------------------------------
        LessonSpec(
            title="Цэвэрлэгээ (cleanup)",
            slug="effect-tseverlegee",
            description="Effect-ийн буцаасан функцээр listener-ийг хасч, unmount болон дахин ажиллахын өмнө цэвэрлэнэ.",
            duration=960,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Effect-ээс цэвэрлэгээний (cleanup) функц буцаах
- `addEventListener`, `removeEventListener`-ийг хосоор нь бичих
  (`keydown`, `resize`)
- Цэвэрлэгээ хэзээ ажилладгийг мэдэх: unmount үед ба effect дахин
  ажиллахын өмнө
- StrictMode яагаад хөгжүүлэлтийн үед effect-ийг хоёр удаа ажиллуулдгийг
  ойлгох

### Яагаад чухал вэ

Гадаад системд «холбогддог» effect (listener, timer, чат, WebSocket)
«салах»-аа ч мэдэх ёстой. Эс бөгөөс цонх хаагдсан ч Escape товчийг
«сонссоор» байна. Цонх нээх бүрт дахиад нэг listener нэмэгдэж, нэг товч
дарахад handler 2, 3, 10 удаа ажиллана. Хэрэггүй listener, timer санах
ойд хуримтлагдана — үүнийг **санах ойн алдагдал** (memory leak) гэдэг.

### Цэвэрлэгээний функц

```jsx
useEffect(() => {
  function handleKeyDown(e) {
    if (e.key === "Escape") onClose();
  }
  window.addEventListener("keydown", handleKeyDown);

  return () => {
    window.removeEventListener("keydown", handleKeyDown);
  };
}, [onClose]);
```

Effect-ийн **буцаасан функц** бол цэвэрлэгээ. React түүнийг хадгалж,
хожим дуудна. Setup юу нэмсэн бол цэвэрлэгээ яг түүнийгээ буцааж авна:

| Setup | Цэвэрлэгээ |
|---|---|
| `addEventListener` | `removeEventListener` |
| `setInterval` | `clearInterval` |
| `connect()` | `disconnect()` |

`removeEventListener`-д **яг тэр функцийг** өгөх ёстой. Тиймээс
handler-ийг нэртэй (`handleKeyDown`) зарлана.
`removeEventListener("keydown", () => …)` гэж шинэ функц өгвөл юу ч
хасагдахгүй.

`e.key` нь дарсан товчны нэр: `"Escape"`, `"Enter"`, `"ArrowLeft"`,
`"ArrowRight"`, `"a"`.

### Хэзээ ажилладаг вэ

```jsx
function ChatRoom({ room }) {
  useEffect(() => {
    console.log("✅ Холбогдлоо:", room);
    return () => console.log("❌ Саллаа:", room);
  }, [room]);
  // ...
}
```

`room` «Ерөнхий»-өөс «React» болж, дараа нь component алга болбол Console:

```jsx
// ✅ Холбогдлоо: Ерөнхий   ← mount
// ❌ Саллаа: Ерөнхий       ← room өөрчлөгдлөө: эхлээд хуучныг цэвэрлэнэ,
// ✅ Холбогдлоо: React     ←                   дараа нь шинээр холбогдоно
// ❌ Саллаа: React         ← unmount
```

1. **Mount** — setup ажиллана.
2. **Хамаарал өөрчлөгдөхөд** — эхлээд өмнөх effect-ийн цэвэрлэгээ
   (хуучин утгуудаараа), дараа нь шинэ setup.
3. **Unmount** — сүүлийн цэвэрлэгээ.

Ингэснээр нэг мөчид ганц л «холболт» байна.

### resize — цонхны хэмжээ

```jsx
function WindowWidth() {
  const [width, setWidth] = useState(window.innerWidth);

  useEffect(() => {
    function handleResize() {
      setWidth(window.innerWidth);
    }
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return <p>Цонхны өргөн: {width}px</p>;
}
```

Энэ хичээлийн 🔒 `WindowWidth.jsx` яг ийм. Хөтчийнхөө цонхны хэмжээг
өөрчилж «Хөтөч»-ийн доод талын тоог ажигла.

Handler нь `[]`-тэй effect дотор байгаа ч `setWidth`-д шинэ утгыг шууд
өгдөг тул хуучирсан утгын асуудалгүй. Харин handler state уншдаг бол
(`index + 1`) функционал шинэчлэлт `setIndex((i) => i + 1)` хэрэглэ —
тэгвэл handler хуучирсан `index`-ийг уншихгүй.

### StrictMode — хөгжүүлэлтийн үед хоёр удаа

Бодит Vite төслийн `main.jsx` иймэрхүү байдаг:

```jsx
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
```

Хөгжүүлэлтийн (`npm run dev`) үед StrictMode component бүрийг mount
хийсний дараа шууд unmount, дахин mount хийдэг: setup → цэвэрлэгээ →
setup. Console-д «✅ Холбогдлоо» хоёр удаа гарна. Энэ бол алдаа биш —
цэвэрлэгээ дутуу эсэхийг эрт илрүүлэх зориуд хийсэн шалгалт. Цэвэрлэгээ
зөв бол хэрэглэгчид ялгаа мэдэгдэхгүй, дутуу бол хоёр listener үүсэж,
алдаа тэр дороо ил гарна. Production build-д effect нэг л удаа ажиллана.

Энэ засварлагч StrictMode ашигладаггүй — render, effect-ийн тоо
ойлгомжтой байхын тулд. Тиймээс мартсан цэвэрлэгээг энд автоматаар
анзаарахгүй, өөрөө анхаараарай. Давхар ажиллахыг «засах» гэж StrictMode-ийг
устгах, эсвэл «аль хэдийн ажилласан» гэж тэмдэглэх хэрэггүй —
цэвэрлэгээгээ зөв бич.

### Бодит төсөлд

Escape-ээр хаагддаг цонхыг бодит төсөлд ихэвчлэн HTML-ийн `<dialog>`
элемент эсвэл Radix UI, Headless UI зэрэг сангаар хийдэг — тэд Escape,
фокусыг өөрсдөө зохицуулдаг. Гэвч тэдний дотор яг энэ хичээлийн
listener + цэвэрлэгээ ажиллаж байгаа.

### Түгээмэл алдаа

- **Цэвэрлэгээ мартах.** Listener хуримтлагдаж, handler олон удаа
  ажиллана.
- **Өөр функц хасах.** `removeEventListener`-д шинэ arrow функц өгвөл юу
  ч хасагдахгүй.
- **Цэвэрлэгээг функц биш, шууд дуудах.** Дараах кодыг ажигла:

```jsx
useEffect(() => {
  window.addEventListener("keydown", handleKey);
  return window.removeEventListener("keydown", handleKey);
}, []);
```

```quiz
Дээрх кодын алдааг ол.
- [ ] Алдаагүй, зөв бичигдсэн
- [x] Listener тэр дороо хасагдана — цэвэрлэгээ нь функц байх ёстой: `return () => window.removeEventListener(…)`
- [ ] Listener-ийг `window` биш `document` дээр нэмэх ёстой
> `return`-ийн араас бичсэн илэрхийлэл шууд ажиллаж, түүний үр дүн (`undefined`) буцна. Цэвэрлэгээ нь хожим дуудагдах **функц** байх ёстой.
```

```quiz
`ChatRoom`-ийн `room` «А»-аас «Б» болоход Console-д юу гарах вэ?
- [ ] Зөвхөн «✅ Холбогдлоо: Б»
- [x] «❌ Саллаа: А», дараа нь «✅ Холбогдлоо: Б»
- [ ] «✅ Холбогдлоо: Б», дараа нь «❌ Саллаа: А»
> Хамаарал өөрчлөгдөхөд React эхлээд хуучин effect-ийг хуучин утгаар нь цэвэрлээд, дараа нь шинийг ажиллуулна.
```

```quiz
StrictMode-той Vite төсөлд `npm run dev` үед `ChatRoom` mount болоход Console-д юу гарах вэ?
- [ ] «✅ Холбогдлоо: А» нэг удаа
- [x] «✅ Холбогдлоо: А», «❌ Саллаа: А», «✅ Холбогдлоо: А»
- [ ] Юу ч гарахгүй
> Хөгжүүлэлтийн үед StrictMode setup → цэвэрлэгээ → setup хийж, цэвэрлэгээг шалгадаг. Production-д нэг удаа.
```

### Дүгнэлт

Effect-ийн буцаасан функц бол цэвэрлэгээ: setup-ийн нэмсэн бүхнийг
буцааж авна. React цэвэрлэгээг effect дахин ажиллахын өмнө болон unmount
үед дууддаг. StrictMode хөгжүүлэлтийн үед effect-ийг хоёр удаа
ажиллуулж, мартсан цэвэрлэгээг ил гаргадаг.
""",
            initial_code=vite(
                """\
import { useState } from "react";
import Lightbox from "./Lightbox";
import WindowWidth from "./WindowWidth";

const PRODUCTS = [
  { id: 1, name: "Банана", emoji: "🍌" },
  { id: 2, name: "Алим", emoji: "🍎" },
  { id: 3, name: "Жүрж", emoji: "🍊" },
  { id: 4, name: "Лууван", emoji: "🥕" },
  { id: 5, name: "Сүү", emoji: "🥛" },
  { id: 6, name: "Талх", emoji: "🍞" },
];

export default function App() {
  const [openIndex, setOpenIndex] = useState(null);

  return (
    <main>
      <h1>Барааны цомог</h1>
      <p className="muted">Бараа дээр дарж томоор хар. ← → товчоор гүйлгэж, Esc-ээр хаа.</p>
      <div className="grid">
        {PRODUCTS.map((product, index) => (
          <button key={product.id} className="tile" onClick={() => setOpenIndex(index)}>
            <span className="big">{product.emoji}</span>
            {product.name}
          </button>
        ))}
      </div>
      {openIndex !== null && (
        <Lightbox products={PRODUCTS} startIndex={openIndex} onClose={() => setOpenIndex(null)} />
      )}
      <WindowWidth />
    </main>
  );
}
""",
                extra={
                    "Lightbox.jsx": """\
import { useState } from "react";

export default function Lightbox({ products, startIndex, onClose }) {
  const [index, setIndex] = useState(startIndex);
  const count = products.length;
  const product = products[index];

  function showPrevious() {
    setIndex((i) => (i - 1 + count) % count);
  }

  function showNext() {
    setIndex((i) => (i + 1) % count);
  }

  // TODO: useEffect — window дээр "keydown" listener нэм:
  //   ArrowLeft → өмнөх, ArrowRight → дараах, Escape → onClose()
  // TODO: цэвэрлэгээнд listener-ээ заавал хас

  return (
    <div className="lightbox" role="dialog" aria-modal="true" aria-label="Бараа томоор харах">
      <span className="big">{product.emoji}</span>
      <h2>{product.name}</h2>
      <p>
        {index + 1} / {count}
      </p>
      <div>
        <button onClick={showPrevious}>← Өмнөх</button>
        <button onClick={showNext}>Дараах →</button>
        <button onClick={onClose}>Хаах ✕</button>
      </div>
    </div>
  );
}
""",
                },
                locked={
                    "WindowWidth.jsx": """\
import { useEffect, useState } from "react";

// Жишээ: resize listener ба түүний цэвэрлэгээ.
export default function WindowWidth() {
  const [width, setWidth] = useState(window.innerWidth);

  useEffect(() => {
    function handleResize() {
      setWidth(window.innerWidth);
    }
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return <p className="muted">«Хөтөч»-ийн өргөн: {width}px</p>;
}
""",
                },
                css=EFFECT_CSS,
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐ · 12 минут

Цомогт бараа дарахад `Lightbox` цонх нээгдэнэ, гэвч одоогоор зөвхөн
товчоор удирдагдана. `Lightbox.jsx`-д `window` дээр `keydown` listener
нэмж ← → товчоор бараа гүйлгэж, Escape-ээр хаадаг болго. Цонх хаагдахад
listener-ээ заавал хас — эс бөгөөс хаагдсан цонх товчлуурыг «сонссоор»
үлдэнэ.
""",
                tests=(
                    test(
                        "→ ба ← товчлуураар бараа солигдоно",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: /Банана/ }));
const dialog = screen.getByRole("dialog");
await user.keyboard("{ArrowRight}");
expect(within(dialog).getByRole("heading")).toHaveTextContent("Алим");
await user.keyboard("{ArrowRight}");
expect(within(dialog).getByRole("heading")).toHaveTextContent("Жүрж");
await user.keyboard("{ArrowLeft}");
expect(within(dialog).getByRole("heading")).toHaveTextContent("Алим");
""",
                    ),
                    test(
                        "Escape дарахад цонх хаагдана",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: /Алим/ }));
expect(screen.getByRole("dialog")).toBeInTheDocument();
await user.keyboard("{Escape}");
expect(screen.queryByRole("dialog")).toBeNull();
""",
                    ),
                    test(
                        "Цонх хаагдсаны (unmount) дараа keydown listener үлдэхгүй",
                        """
const Lightbox = mod("./Lightbox").default;
const products = [
  { id: 1, name: "Банана", emoji: "🍌" },
  { id: 2, name: "Алим", emoji: "🍎" },
];
const onClose = fn();
const { unmount } = render(<Lightbox products={products} startIndex={0} onClose={onClose} />);
await user.keyboard("{Escape}");
expect(onClose).toHaveBeenCalledTimes(1);
unmount();
await user.keyboard("{Escape}");
await user.keyboard("{Escape}");
expect(onClose).toHaveBeenCalledTimes(1);
""",
                    ),
                    test(
                        "onClose солигдоход хуучин listener цэвэрлэгдэж, шинэ onClose л дуудагдана",
                        """
const Lightbox = mod("./Lightbox").default;
const products = [{ id: 1, name: "Банана", emoji: "🍌" }];
const first = fn();
const second = fn();
const { rerender } = render(<Lightbox products={products} startIndex={0} onClose={first} />);
rerender(<Lightbox products={products} startIndex={0} onClose={second} />);
await user.keyboard("{Escape}");
expect(second).toHaveBeenCalledTimes(1);
expect(first).toHaveBeenCalledTimes(0);
""",
                    ),
                ),
                tips="""\
- Handler-ийг effect-ийн **дотор** нэртэй функцээр зарла
  (`function handleKeyDown(e) { … }`), `e.key`-ээр аль товч дарагдсаныг
  шалга.
- Индексийг функционал шинэчлэлтээр өөрчил: `setIndex((i) => …)`.
  `setIndex(index + 1)` гэвэл handler хуучирсан `index`-ийг уншиж, хоёр
  дахь товчноос хойш бараа солигдохгүй.
- Handler нь `onClose`, `count`-ийг уншдаг тул хамааралд бич. Тэгвэл
  `onClose` солигдоход React хуучин listener-ийг цэвэрлэж, шинийг нэмнэ.
- Цэвэрлэгээ нь **функц** буцаана: `return () => …removeEventListener(…)`.
  `removeEventListener`-д яг `addEventListener`-т өгсөн функцээ өг.
""",
                solution=solution(
                    Lightbox_jsx="""\
import { useEffect, useState } from "react";

export default function Lightbox({ products, startIndex, onClose }) {
  const [index, setIndex] = useState(startIndex);
  const count = products.length;
  const product = products[index];

  function showPrevious() {
    setIndex((i) => (i - 1 + count) % count);
  }

  function showNext() {
    setIndex((i) => (i + 1) % count);
  }

  useEffect(() => {
    function handleKeyDown(e) {
      if (e.key === "ArrowLeft") setIndex((i) => (i - 1 + count) % count);
      if (e.key === "ArrowRight") setIndex((i) => (i + 1) % count);
      if (e.key === "Escape") onClose();
    }
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [count, onClose]);

  return (
    <div className="lightbox" role="dialog" aria-modal="true" aria-label="Бараа томоор харах">
      <span className="big">{product.emoji}</span>
      <h2>{product.name}</h2>
      <p>
        {index + 1} / {count}
      </p>
      <div>
        <button onClick={showPrevious}>← Өмнөх</button>
        <button onClick={showNext}>Дараах →</button>
        <button onClick={onClose}>Хаах ✕</button>
      </div>
    </div>
  );
}
"""
                ),
            ),
        ),
        # --- 4 ------------------------------------------------------------------
        LessonSpec(
            title="Timer: setInterval ба цэвэрлэгээ",
            slug="effect-timer",
            description="setInterval-ийг effect-ээр эхлүүлж, цэвэрлэгээгээр зогсоож, функционал шинэчлэлтээр хуучирсан утгаас сэргийлнэ.",
            duration=900,
            language=JSX,
            content="""\
### Энэ хичээлээр

- `setInterval`-ийг effect дотор эхлүүлж, `clearInterval`-ээр цэвэрлэх
- Interval доторх хуучирсан утгын хавхыг ойлгох
- Функционал шинэчлэлт `setSeconds((s) => s + 1)`-ээр засах
- Timer-ийг boolean state-ээр асааж, унтраах

### Яагаад чухал вэ

«Кодыг 60 секундын дараа дахин илгээх боломжтой» гэсэн тоолуур,
секундомер, шалгалтын үлдсэн хугацаа, слайд шоу, хэдэн секунд тутам шинэ
мэдээ шалгах — бүгд timer. Timer бол хөтчийн, өөрөөр хэлбэл гадаад
системийн зүйл: React түүнийг мэдэхгүй. `clearInterval` хийхгүй бол
component алга болсон ч timer ажилласаар, дахин mount болох бүрт нэг timer
нэмэгдэж, цаг 2, 3 дахин хурдан гүйнэ.

### Цаг

```jsx
function Clock() {
  const [now, setNow] = useState(() => new Date());

  useEffect(() => {
    const id = setInterval(() => {
      setNow(new Date());
    }, 1000);
    return () => clearInterval(id);
  }, []);

  return <p>{now.toLocaleTimeString()}</p>;
}
```

- `setInterval(fn, 1000)` нь `fn`-ийг секунд тутам дуудаж, timer-ийн
  **id** буцаана.
- Цэвэрлэгээ тэр id-гаар timer-ийг зогсооно.
- `[]` — mount үед нэг удаа эхэлж, unmount үед зогсоно.

### Хуучирсан утгын хавх

```jsx
const [seconds, setSeconds] = useState(0);

useEffect(() => {
  const id = setInterval(() => {
    setSeconds(seconds + 1); // ❌ seconds үргэлж 0
  }, 1000);
  return () => clearInterval(id);
}, []);
```

Дэлгэцэнд 1 гарч, тэгээд хөдлөхөө болино. Яагаад? Interval-ийн функц
эхний render дээр үүссэн бөгөөд тэр render-ийн `seconds` нь 0 (Модул 3-ын
snapshot). `[]` тул effect дахин үүсэхгүй — функц үүрд 0-ийг харж, секунд
тутам `setSeconds(0 + 1)` дуудна.

Хоёр засвар бий:

1. ✅ **Функционал шинэчлэлт** — `setSeconds((s) => s + 1)`. React хамгийн
   сүүлийн утгыг `s`-ээр өгнө. Функц `seconds`-ийг огт уншихгүй тул
   хамаарал `[]` хэвээр үлдэнэ.
2. `seconds`-ийг хамааралд нэмэх — ажиллана, гэхдээ секунд тутам interval
   устаж, шинээр үүснэ. Функционал шинэчлэлт илүү цэвэрхэн.

### Асаах, унтраах

```jsx
const [seconds, setSeconds] = useState(0);
const [running, setRunning] = useState(false);

useEffect(() => {
  if (!running) return; // зогссон үед timer хэрэггүй

  const id = setInterval(() => {
    setSeconds((s) => s + 1);
  }, 1000);
  return () => clearInterval(id);
}, [running]);
```

- `running` нь `true` болоход effect interval эхлүүлнэ.
- `running` нь `false` болоход React эхлээд өмнөх цэвэрлэгээг ажиллуулж
  interval-ийг зогсооно. Шинэ setup нь шууд `return` хийж, юу ч
  эхлүүлэхгүй — юу ч эхлүүлээгүй бол цэвэрлэх зүйл ч алга.
- «Эхлүүлэх»-ийг хэд дарсан ч interval давхардахгүй: `running` аль хэдийн
  `true` бол хамаарал өөрчлөгдөхгүй.

Timer-ийн id-г state-д хадгалах хэрэггүй — цэвэрлэгээ түүнийг өөрийн
хаалтаас (closure) авна. Event handler-ээс timer зогсоох шаардлагатай бол
Модул 6-гийн `useRef` хэрэг болно.

### setTimeout ч адилхан

```jsx
useEffect(() => {
  if (!message) return;
  const id = setTimeout(() => setMessage(""), 3000);
  return () => clearTimeout(id);
}, [message]);
```

Мэдэгдэл 3 секундын дараа алга болно. Хугацаа дуусахаас өмнө шинэ мессеж
ирвэл хуучин timer цэвэрлэгдэж, тоолол шинээр эхэлнэ.

### Түгээмэл алдаа

- **Цэвэрлэгээ мартах.** StrictMode-той Vite төсөлд хөгжүүлэлтийн үед
  timer хоёр болж, тоо секундэд 2-оор нэмэгдэнэ.
- **`setInterval(tick(), 1000)`.** `tick`-ийг тэр дороо дуудаж, үр дүнг
  нь өгнө. Функцээ өөрийг нь өг: `setInterval(tick, 1000)`.
- **onClick дотор `setInterval`.** Товч дарах бүрт шинэ interval үүсэж,
  хуучин нь зогсохгүй. Timer-ийг state-ээр удирдаж, effect-д эхлүүл.

```quiz
«Хуучирсан утгын хавх» хэсгийн кодыг 5 секунд ажиллуулбал дэлгэцэнд ямар тоо харагдах вэ?
- [ ] 5
- [x] 1
- [ ] 0
> Interval-ийн функц эхний render-ийн `seconds` (0)-ийг л хардаг тул секунд тутам `setSeconds(1)` дуудна.
```

```quiz
`[running]`-тэй секундомерт «Зогсоох» дарахад interval-ийг яг юу зогсоох вэ?
- [ ] Interval өөрөө зогсоно
- [x] `running` өөрчлөгдсөн тул React-ийн ажиллуулсан цэвэрлэгээ (`clearInterval`)
- [ ] Шинэ setup дотор `clearInterval` дуудах ёстой
> Хамаарал өөрчлөгдөхөд React эхлээд өмнөх effect-ийн цэвэрлэгээг дуудна. Шинэ setup `running` худал тул юу ч эхлүүлэхгүй.
```

### Дүгнэлт

`setInterval` ↔ `clearInterval` хосыг effect дотор бич. Interval-ийн
функц үүссэн render-ийнхээ утгыг хардаг тул state-ийг `setX((prev) => …)`
функционал шинэчлэлтээр өөрчил. Timer-ийг асааж унтраахдаа boolean
state-ийг хамаарал болго.
""",
            initial_code=vite(
                """\
import { useState } from "react";

export default function App() {
  const [tenths, setTenths] = useState(0); // секундийн аравны нэгээр
  const [running, setRunning] = useState(false);

  // TODO 1: running үнэн үед 100 мс тутамд tenths-ийг 1-ээр нэмэгдүүл.
  //         Функционал шинэчлэлт, цэвэрлэгээ хоёроо бүү мартаарай.

  function reset() {
    // TODO 2: секундомерыг зогсоож, 0 болго
  }

  return (
    <main>
      <h1>⏱️ Секундомер</h1>
      <p className="display">{(tenths / 10).toFixed(1)} сек</p>
      <button onClick={() => setRunning(true)} disabled={running}>
        Эхлүүлэх
      </button>
      <button onClick={() => setRunning(false)} disabled={!running}>
        Зогсоох
      </button>
      <button onClick={reset}>Тэглэх</button>
    </main>
  );
}
""",
                css=EFFECT_CSS,
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 10 минут

Секундомерын товчнууд `running` state-ийг сольж байгаа ч тоо хөдлөхгүй
байна. `running` үнэн үед 100 мс тутамд `tenths`-ийг нэмэгдүүлдэг
interval-ийг effect-ээр эхлүүл, зогсоход болон component устахад
цэвэрлэ. «Тэглэх» товч секундомерыг зогсоож, 0.0 болгоно.
""",
                tests=(
                    test(
                        "«Эхлүүлэх» дарахад хугацаа тасралтгүй нэмэгдэнэ",
                        """
const read = () => {
  const match = screen.text().match(/([0-9]+[.][0-9]) сек/);
  expect(match).toBeTruthy();
  return Number(match[1]);
};
render(<App />);
expect(read()).toBe(0);
await user.click(screen.getByRole("button", { name: "Эхлүүлэх" }));
await waitFor(() => expect(read()).toBeGreaterThanOrEqual(0.5));
""",
                    ),
                    test(
                        "«Зогсоох» дарахад хугацаа зогсоно",
                        """
const read = () => {
  const match = screen.text().match(/([0-9]+[.][0-9]) сек/);
  expect(match).toBeTruthy();
  return Number(match[1]);
};
render(<App />);
await user.click(screen.getByRole("button", { name: "Эхлүүлэх" }));
await waitFor(() => expect(read()).toBeGreaterThanOrEqual(0.2));
await user.click(screen.getByRole("button", { name: "Зогсоох" }));
const stopped = read();
await act(async () => {
  await sleep(350);
});
expect(read()).toBe(stopped);
""",
                    ),
                    test(
                        "«Тэглэх» дарахад 0.0 болж, дахин нэмэгдэхгүй",
                        """
const read = () => {
  const match = screen.text().match(/([0-9]+[.][0-9]) сек/);
  expect(match).toBeTruthy();
  return Number(match[1]);
};
render(<App />);
await user.click(screen.getByRole("button", { name: "Эхлүүлэх" }));
await waitFor(() => expect(read()).toBeGreaterThanOrEqual(0.2));
await user.click(screen.getByRole("button", { name: "Тэглэх" }));
expect(read()).toBe(0);
await act(async () => {
  await sleep(300);
});
expect(read()).toBe(0);
""",
                    ),
                    test(
                        "Component устахад (unmount) interval цэвэрлэгдэнэ",
                        """
const active = new Set();
const realSetInterval = window.setInterval;
const realClearInterval = window.clearInterval;
window.setInterval = (...args) => {
  const id = realSetInterval(...args);
  active.add(id);
  return id;
};
window.clearInterval = (id) => {
  active.delete(id);
  realClearInterval(id);
};
try {
  const { unmount } = render(<App />);
  await user.click(screen.getByRole("button", { name: "Эхлүүлэх" }));
  expect(active.size).toBeGreaterThan(0);
  unmount();
  expect(active.size).toBe(0);
} finally {
  window.setInterval = realSetInterval;
  window.clearInterval = realClearInterval;
}
""",
                    ),
                ),
                tips="""\
- Effect-ийн хамаарал нь `[running]`. `running` худал бол шууд `return` —
  timer эхлүүлэхгүй.
- Interval дотор `setTenths(tenths + 1)` гэвэл функц эхний render-ийн
  `tenths` (0)-ийг л харж, 0.1 дээр зогсоно. `setTenths((t) => t + 1)`
  хэрэглэ.
- `setInterval`-ийн буцаасан id-г хадгалж, цэвэрлэгээнд
  `clearInterval(id)` дууд. `running` өөрчлөгдөх болон unmount үед React
  түүнийг өөрөө дуудна.
- «Тэглэх»: `setRunning(false)` ба `setTenths(0)` — interval-ийг
  цэвэрлэгээ зогсооно.
""",
                solution=solution(
                    App_jsx="""\
import { useEffect, useState } from "react";

export default function App() {
  const [tenths, setTenths] = useState(0); // секундийн аравны нэгээр
  const [running, setRunning] = useState(false);

  useEffect(() => {
    if (!running) return;

    const id = setInterval(() => {
      setTenths((t) => t + 1);
    }, 100);
    return () => clearInterval(id);
  }, [running]);

  function reset() {
    setRunning(false);
    setTenths(0);
  }

  return (
    <main>
      <h1>⏱️ Секундомер</h1>
      <p className="display">{(tenths / 10).toFixed(1)} сек</p>
      <button onClick={() => setRunning(true)} disabled={running}>
        Эхлүүлэх
      </button>
      <button onClick={() => setRunning(false)} disabled={!running}>
        Зогсоох
      </button>
      <button onClick={reset}>Тэглэх</button>
    </main>
  );
}
"""
                ),
            ),
        ),
        # --- 5 ------------------------------------------------------------------
        LessonSpec(
            title="Effect дотор өгөгдөл татах",
            slug="effect-fetch",
            description="API-гаас өгөгдөл татаж ачаалах, алдаа, өгөгдлийн төлөвийг харуулж, уралдааны нөхцөлөөс сэргийлнэ.",
            duration=1080,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Effect дотор `fetch` хийж, API-гаас өгөгдөл татах
- Ачаалж буй, алдаа, өгөгдөл гэсэн гурван төлөвийг харуулах
- Хамаарал өөрчлөгдөхөд өгөгдлийг дахин татах
- `ignore` тэмдэглэл эсвэл `AbortController`-оор уралдааны нөхцөлөөс
  (race condition) сэргийлэх

### Яагаад чухал вэ

Бараг бүх апп серверийн өгөгдөл харуулдаг: бараа, хэрэглэгч, захиалга.
Сервер бол гадаад систем: хариу нь хэсэг хугацааны дараа ирнэ, заримдаа
алдаа буцаана, хариу ирэхээс өмнө хэрэглэгч шүүлтүүрээ сольчихсон байж
болно. Эдгээрийг бодоогүй апп хоосон дэлгэц, дуусдаггүй «ачаалж байна»,
эсвэл буруу өгөгдөл харуулна.

### Хамгийн энгийн хувилбар

```jsx
function UserList() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    fetch("/api/users")
      .then((response) => response.json())
      .then((data) => setUsers(data));
  }, []);

  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

Mount үед нэг удаа татна (`[]`). Ажиллана, гэхдээ дутуу: хариу ирэх
хүртэл (энд 0.4 сек) дэлгэц хоосон, алдааг огт харуулахгүй,
`response.ok`-ийг шалгаагүй.

Effect-ийн функц өөрөө `async` байж болохгүй: `useEffect(async () => …)`
нь Promise буцаадаг, харин React цэвэрлэгээний функц эсвэл юу ч үгүйг
хүлээдэг. Оронд нь effect дотор `async` функц зарлаад дууд.

### Гурван төлөв

```jsx
function UserList() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function load() {
      try {
        const response = await fetch("/api/users");
        if (!response.ok) throw new Error(`Сервер ${response.status} алдаа буцаалаа`);
        setUsers(await response.json());
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) return <p>Ачаалж байна…</p>;
  if (error) return <p role="alert">Алдаа гарлаа: {error}</p>;
  return <ul>{/* … */}</ul>;
}
```

- `loading` нь `true`-ээс эхэлнэ — хэрэглэгч эхний render-ээс л ямар нэг
  зүйл болж байгааг харна.
- `fetch` нь 404, 500-д алдаа шиддэггүй (Модул 0) — `response.ok`-ийг
  өөрөө шалгаж, алдаа шид.
- `finally` нь амжилт, алдаа аль алинд ажиллаж ачааллыг дуусгана.
- Алдааны мэдэгдэлд `role="alert"` — дэлгэц уншигч түүнийг шууд уншина
  (Модул 4).

Дадлагын API-д хаягийн ард `?_status=500` нэмбэл алдаа буцаана,
`?_delay=3000` нь хариуг 3 секунд хоцрооно — төлөв бүрийг «Хөтөч» дээр
туршиж үзээрэй.

### Хамаарал өөрчлөгдөхөд дахин татах

```jsx
const [city, setCity] = useState("");
const url = city ? `/api/users?city=${city}` : "/api/users";

useEffect(() => {
  setLoading(true);
  setError(null);
  // … fetch(url) …
}, [url]);
```

Хот солигдох бүрт `url` өөрчлөгдөж, effect дахин ажиллана. Шинэ хүсэлтийн
өмнө ачааллыг асааж, өмнөх алдааг арилгана.

### Уралдааны нөхцөл (race condition)

Хэрэглэгч «Дархан»-ыг сонгоод, тэр дороо «Эрдэнэт»-ийг сонгов. Хоёр хүсэлт
зэрэг явж байна. Хариунууд илгээсэн дарааллаараа ирнэ гэсэн баталгаа
сүлжээнд байхгүй. «Дархан»-ы хариу хоцорч ирвэл сонголтод «Эрдэнэт»,
жагсаалтад Дарханы хэрэглэгчид харагдана — дэлгэц state-ээсээ зөрнө.

```jsx
// Цаг хугацаа →
// «Дархан» хүсэлт  ──────────────────────► хариу (хожуу) ❌ шинийг дарна
// «Эрдэнэт» хүсэлт     ─────► хариу ✅
```

**Засвар 1 — `ignore` тэмдэглэл:**

```jsx
useEffect(() => {
  let ignore = false;

  async function load() {
    const response = await fetch(url);
    const data = await response.json();
    if (!ignore) setUsers(data); // хуучирсан бол хаяна
  }
  load();

  return () => {
    ignore = true;
  };
}, [url]);
```

Effect ажиллах бүрт өөрийн гэсэн `ignore` хувьсагч үүснэ. `url`
өөрчлөгдөхөд React өмнөх effect-ийн цэвэрлэгээг ажиллуулж, **тэр**
effect-ийн `ignore`-ийг `true` болгоно. Хуучин хариу ирэхэд `if (!ignore)`
түүнийг хаяна.

**Засвар 2 — `AbortController`** нь хүсэлтийг өөрийг нь цуцална:

```jsx
useEffect(() => {
  const controller = new AbortController();

  fetch(url, { signal: controller.signal })
    .then((response) => response.json())
    .then((data) => setUsers(data))
    .catch((err) => {
      if (err.name === "AbortError") return; // бид өөрсдөө цуцалсан
      setError(err.message);
    });

  return () => controller.abort();
}, [url]);
```

Цуцлагдсан `fetch` нь `AbortError` шиднэ. Энэ бол жинхэнэ алдаа биш —
хэрэглэгчид харуулахгүй. Давуу тал нь сүлжээ, серверийн ачаалал
багасна. Хоёр арга хоёулаа зөв: `ignore` ойлгоход хялбар,
`AbortController` хүсэлтийг бодитоор зогсооно.

### Бодит төсөлд

Effect дотор өгөгдөл татах нь ажилладаг ч бодит төсөлд дутагдалтай: кэш
байхгүй (хуудас руу буцах бүрт дахин татна), код давтагдана, олон
component ижил өгөгдлийг тус тусдаа татна. Тиймээс ихэнх баг **TanStack
Query** (Модул 9) эсвэл React Router, Next.js зэрэг framework-ийн өгөгдөл
татах аргыг хэрэглэдэг. Тэд цаанаа яг энэ хичээлийн гурван төлөв,
уралдааны хамгаалалтыг хийдэг тул үүнийг ойлгох нь чухал.

Өөрийгөө шалга — дараах кодыг ажигла:

```jsx
useEffect(async () => {
  const response = await fetch(url);
  setData(await response.json());
}, [url]);
```

```quiz
Дээрх кодын асуудал юу вэ?
- [ ] Алдаагүй, зөв бичигдсэн
- [x] Effect Promise буцааж байна — React цэвэрлэгээний функц хүлээдэг тул `async` функцийг effect дотор зарлаж дуудах ёстой
- [ ] `[url]` биш `[]` байх ёстой
> `async` функц үргэлж Promise буцаадаг. React түүнийг цэвэрлэгээ гэж ойлгохгүй, Console-д анхааруулга гаргана.
```

```quiz
`ignore` тэмдэглэлгүй кодонд хэрэглэгч А хотыг сонгоод, дараа нь Б хотыг сонгов. А-гийн хариу хамгийн сүүлд ирвэл дэлгэцэнд юу харагдах вэ?
- [ ] Б хотын хэрэглэгчид
- [x] А хотын хэрэглэгчид, харин сонголтод Б
- [ ] Алдааны мэдэгдэл
> Сүүлд ирсэн хариу state-ийг дарж бичнэ. `ignore` эсвэл `AbortController` хуучин хариуг хаяна.
```

```quiz
`AbortController`-оор цуцалсан хүсэлтийн `AbortError`-ийг яах вэ?
- [ ] Алдааны мэдэгдлээр харуулна
- [x] Үл тооно — бид өөрсдөө цуцалсан
- [ ] Хүсэлтийг дахин илгээнэ
> Цуцлах нь хамаарал өөрчлөгдсөн эсвэл component устсаны шинж. Хэрэглэгчид алдаа биш.
```

### Дүгнэлт

Өгөгдөл татах effect гурван төлөвтэй: ачаалж буй, алдаа, өгөгдөл.
`response.ok`-ийг шалгаж, `finally`-д ачааллыг дуусга. Хамаарал
өөрчлөгдөхөд дахин татаж, хуучирсан хариуг цэвэрлэгээнд `ignore = true`
эсвэл `controller.abort()`-оор хая.
""",
            initial_code=vite(
                """\
import { useEffect, useState } from "react";

const CITIES = ["Улаанбаатар", "Дархан", "Эрдэнэт"];

export default function App() {
  const [city, setCity] = useState("");
  const [users, setUsers] = useState([]);
  // TODO 1: loading, error state

  const url = city ? `/api/users?city=${city}` : "/api/users";

  // TODO 2: url өөрчлөгдөх бүрт fetch хий, response.ok-ийг шалга
  // TODO 3: хуучирсан хариуг ignore эсвэл AbortController-оор хая

  return (
    <main>
      <h1>👥 Хэрэглэгчид</h1>
      <label>
        Хот
        <select value={city} onChange={(e) => setCity(e.target.value)}>
          <option value="">Бүх хот</option>
          {CITIES.map((name) => (
            <option key={name} value={name}>
              {name}
            </option>
          ))}
        </select>
      </label>

      {/* TODO 4: ачаалж байхад «Ачаалж байна…»,
          алдаа гарвал role="alert"-тэй «Алдаа гарлаа: …» */}
      <ul>
        {users.map((user) => (
          <li key={user.id}>
            <strong>{user.name}</strong> — {user.city} · {user.email}
          </li>
        ))}
      </ul>
    </main>
  );
}
""",
                css=EFFECT_CSS,
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐ · 15 минут

Хэрэглэгчдийн жагсаалтыг дадлагын API-гаас (`/api/users`) татаж харуул.
«Хот» сонгоход `url` өөрчлөгдөж, тухайн хотын хэрэглэгчид ачаалагдана.
Хариу ирэх хүртэл «Ачаалж байна…», алдаа гарвал `role="alert"`-тэй
«Алдаа гарлаа: …» мэдэгдэл харуул. Хотыг хурдан солиход хожуу ирсэн хуучин
хариу шинэ жагсаалтыг дарж болохгүй.
""",
                tests=(
                    test(
                        "Эхлээд «Ачаалж байна…», дараа нь бүх хэрэглэгч харагдана",
                        """
render(<App />);
expect(screen.text()).toMatch(/Ачаалж байна/);
await screen.findByText(/Тэмүүлэн/);
const text = screen.text();
for (const name of ["Бат", "Сараа", "Ану"]) {
  expect(text).toContain(name);
}
expect(text).not.toMatch(/Ачаалж байна/);
""",
                    ),
                    test(
                        "Хот сонгоход тухайн хотын хэрэглэгчид л ачаалагдана",
                        """
render(<App />);
await screen.findByText(/Тэмүүлэн/);
await user.selectOptions(screen.getByLabelText("Хот"), "Дархан");
await waitFor(() => {
  expect(screen.text()).toContain("Сараа");
  expect(screen.text()).not.toContain("Тэмүүлэн");
});
const asked = api.requests.some((request) => decodeURIComponent(request.path).includes("city=Дархан"));
expect(asked).toBe(true);
""",
                    ),
                    test(
                        'Серверийн алдаа гарвал role="alert"-тэй «Алдаа гарлаа» мэдэгдэл харагдана',
                        """
api.fail("/api/users", 500);
render(<App />);
const alert = await screen.findByRole("alert");
expect(alert).toHaveTextContent(/Алдаа гарлаа/);
expect(screen.text()).not.toMatch(/Ачаалж байна/);
""",
                    ),
                    test(
                        "Хожуу ирсэн хуучин хариу шинэ сонголтын жагсаалтыг дарахгүй",
                        """
const realFetch = window.fetch;
window.fetch = async (input, init) => {
  if (decodeURIComponent(String(input)).includes("Дархан")) {
    await sleep(300);
    if (init && init.signal && init.signal.aborted) {
      throw new DOMException("The operation was aborted.", "AbortError");
    }
  }
  return realFetch(input, init);
};
try {
  render(<App />);
  await screen.findByText(/Тэмүүлэн/);
  const select = screen.getByLabelText("Хот");
  await user.selectOptions(select, "Дархан");
  await user.selectOptions(select, "Эрдэнэт");
  await waitFor(() => {
    expect(screen.text()).toContain("Тэмүүлэн");
    expect(screen.text()).not.toContain("Ану");
  });
  await act(async () => {
    await sleep(400);
  });
  expect(screen.text()).toContain("Тэмүүлэн");
  expect(screen.text()).not.toContain("Сараа");
  expect(screen.text()).not.toMatch(/Алдаа гарлаа/);
} finally {
  window.fetch = realFetch;
}
""",
                    ),
                ),
                tips="""\
- `loading`-ийг `true`-ээс, `error`-ийг `null`-оос эхлүүл. Effect-ийн
  эхэнд `setLoading(true)`, `setError(null)` — хот солигдох бүрт шинэ
  хүсэлт эхэлнэ.
- Хамаарал нь `[url]`. Effect-ийн функцийг `async` болгож болохгүй —
  дотор нь `async function load() { … }` зарлаад дууд.
- `if (!response.ok) throw new Error(…)` — эс бөгөөс 500-ийн хариу
  өгөгдөл мэт харагдана.
- Уралдаан: `let ignore = false;`, цэвэрлэгээнд `ignore = true`, state
  шинэчлэх бүрийн өмнө `if (!ignore)`. `AbortController` сонговол
  `AbortError`-ийг алдаа гэж бүү харуул.
""",
                solution=solution(
                    App_jsx="""\
import { useEffect, useState } from "react";

const CITIES = ["Улаанбаатар", "Дархан", "Эрдэнэт"];

export default function App() {
  const [city, setCity] = useState("");
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const url = city ? `/api/users?city=${city}` : "/api/users";

  useEffect(() => {
    let ignore = false;
    setLoading(true);
    setError(null);

    async function load() {
      try {
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error(`Сервер ${response.status} алдаа буцаалаа`);
        }
        const data = await response.json();
        if (!ignore) setUsers(data);
      } catch (err) {
        if (!ignore) setError(err.message);
      } finally {
        if (!ignore) setLoading(false);
      }
    }

    load();
    return () => {
      ignore = true;
    };
  }, [url]);

  return (
    <main>
      <h1>👥 Хэрэглэгчид</h1>
      <label>
        Хот
        <select value={city} onChange={(e) => setCity(e.target.value)}>
          <option value="">Бүх хот</option>
          {CITIES.map((name) => (
            <option key={name} value={name}>
              {name}
            </option>
          ))}
        </select>
      </label>

      {loading && <p className="muted">Ачаалж байна…</p>}
      {error && (
        <p className="error" role="alert">
          Алдаа гарлаа: {error}
        </p>
      )}
      {!loading && !error && (
        <ul>
          {users.map((user) => (
            <li key={user.id}>
              <strong>{user.name}</strong> — {user.city} · {user.email}
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}
"""
                ),
            ),
        ),
        # --- 6 ------------------------------------------------------------------
        LessonSpec(
            title="Танд effect хэрэггүй байж магадгүй",
            slug="effect-heregtei-yu",
            description="Тооцоолж болох утга, хэрэглэгчийн үйлдлийг effect-ээс салгаж, effect-ийн түгээмэл алдаанаас зайлсхийнэ.",
            duration=1020,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Props, state-ээс тооцоолж болох утгыг effect-гүйгээр render дотор тооцох
- Хэрэглэгчийн үйлдлийн логикийг effect биш event handler-т бичих
- Хамаарал дутуу, төгсгөлгүй давталт, объект хамаарал гэсэн түгээмэл
  алдааг таних
- «Энэ код яагаад ажиллах ёстой вэ?» гэсэн асуултаар effect хэрэгтэй
  эсэхийг шийдэх

### Яагаад чухал вэ

`useEffect`-ийг сурсны дараа түүнийг хаа сайгүй хэрэглэх хүсэл төрдөг.
Гэвч effect бол React-ийн «гарц» (escape hatch) — зөвхөн гадаад системтэй
синхрончлоход зориулагдсан. Шаардлагагүй effect:

- **илүү render** хийлгэж аппыг удаашруулна;
- нэг агшин **буруу утга** харуулна;
- хамаарал мартвал **хуучирсан өгөгдөл** үлдээнэ;
- кодыг дагаж ойлгоход хэцүү болгоно.

React-ийн албан ёсны баримт бичигт «You Might Not Need an Effect» гэсэн
бүтэн хуудас бий — бодит төслүүдэд хамгийн түгээмэл алдааны нэг.

### 1. Тооцоолж болох утга — state биш

```jsx
// ❌ Effect-ээр state-ийг «толин тусгал» болгох
const [firstName, setFirstName] = useState("Бат");
const [lastName, setLastName] = useState("Дорж");
const [fullName, setFullName] = useState("");

useEffect(() => {
  setFullName(`${firstName} ${lastName}`);
}, [firstName, lastName]);
```

`firstName` өөрчлөгдөхөд:

1. Render — `fullName` **хуучин** утгаараа.
2. Commit — дэлгэцэнд хуучин нэр.
3. Effect → `setFullName` → **дахин** render, commit.

Нэг өөрчлөлтөд хоёр render, дунд нь буруу утга.

```jsx
// ✅ Render дотор тооцоол
const fullName = `${firstName} ${lastName}`;
```

Дүрэм (Модул 3-ын уламжлагдсан утга): props, state-ээс тооцож болох
утгыг state-д **хадгалахгүй**. Шүүсэн жагсаалт, нийт үнэ, тоо ширхэг —
бүгд render дотор. Тооцоолол үнэхээр удаан бол `useMemo` (Модул 6).

### 2. Хэрэглэгчийн үйлдэл — event handler-т

```jsx
// ❌
useEffect(() => {
  if (cart.length > 0) {
    showToast("Сагсанд нэмэгдлээ!");
  }
}, [cart]);
```

Сагс `localStorage`-оос сэргээгдэхэд (хуудас ачаалахад) ч, бараа хасахад
ч «нэмэгдлээ» гарна. Effect сагс **яагаад** өөрчлөгдснийг мэдэхгүй.

```jsx
// ✅
function handleAdd(product) {
  setCart([...cart, product]);
  showToast(`${product.name} сагсанд нэмэгдлээ!`);
}
```

Форм илгээх POST хүсэлт ч мөн адил — `submitted` state-ийг ажиглах effect
биш, `handleSubmit` дотор бичнэ. Өөрөөсөө асуу: **«Энэ код яагаад ажиллах
ёстой вэ?»**

- Component дэлгэцэд харагдаж байгаа учраас → effect.
- Хэрэглэгч ямар нэг зүйл хийсэн учраас → event handler.

### 3. Prop солигдоход state-ийг шинэчлэх — key

```jsx
// ❌ Profile дотор
useEffect(() => {
  setComment("");
}, [userId]);

// ✅ Эцэг component дээр
<Profile key={userId} userId={userId} />
```

`key` өөрчлөгдөхөд React хуучин component-ийг устгаж, шинийг хоосон
state-тэйгээр үүсгэнэ (Модул 2-ын `key`).

### Түгээмэл алдаа

**Хамаарал дутуу.** Effect хуучирсан утгыг харна (энэ модулийн 2-р
хичээл). Засахдаа хамаарлыг нэм — эсвэл тэр effect ерөөсөө хэрэгтэй
эсэхийг эргэж бод.

**Төгсгөлгүй давталт.**

```jsx
const [count, setCount] = useState(0);

useEffect(() => {
  setCount(count + 1); // ❌ render → effect → setCount → render → …
});
```

Массивгүй effect render бүрийн дараа ажиллаж, state өөрчлөн шинэ render
үүсгэнэ. `[count]` бичсэн ч ялгаагүй — `count` өөрчлөгдөх бүрт дахин
ажиллана. Апп гацаж, React Console-д «Maximum update depth exceeded» гэж
анхааруулна. Effect дотор state өөрчилж байвал «энэ утгыг render дотор
тооцож болох уу?» гэж эхлээд асуу.

**Объект хамаарал + setState.**

```jsx
const filters = { city, minAge }; // render бүрт шинэ объект

useEffect(() => {
  fetch(`/api/users?city=${filters.city}`)
    .then((response) => response.json())
    .then((data) => setUsers(data)); // → render → шинэ filters → effect → …
}, [filters]);
```

`filters` render бүрт шинэ тул effect render бүрт ажиллаж, `setUsers` нь
дахиад render үүсгэнэ — хүсэлт тасралтгүй явна. Энгийн утгуудыг хамаарал
болго: `[city, minAge]`.

### Шийдэх хүснэгт

| Нөхцөл | Хаана бичих |
|---|---|
| Утгыг props, state-ээс тооцож болно | Render дотор |
| Товч дарах, илгээх зэрэг үйлдлийн хариу | Event handler |
| Prop солигдоход state-ийг бүхэлд нь шинэчлэх | `key` |
| Гадаад системтэй синхрон байлгах (гарчиг, timer, listener, сүлжээ) | `useEffect` |

Өөрийгөө шалга — дараах кодыг ажигла:

```jsx
const [price, setPrice] = useState(1000);
const [qty, setQty] = useState(1);
const [total, setTotal] = useState(1000);

useEffect(() => {
  setTotal(price * qty);
}, [price]);
```

```quiz
Дээрх кодонд `qty`-г 3 болговол дэлгэцэн дээрх `total` хэд байх вэ?
- [ ] 3000
- [x] 1000
- [ ] 0
> `qty` хамааралд алга тул effect ажиллахгүй. Хамгийн зөв засвар нь effect, `total` state-ийг устгаж, `const total = price * qty;` гэж render дотор тооцох.
```

```quiz
Аль нь effect шаарддаг вэ?
- [ ] Хайлтын үгээр жагсаалтыг шүүх
- [ ] «Худалдаж авах» дарахад баярын мэдэгдэл харуулах
- [x] Чатын өрөөнд холбогдож, өрөө солигдоход дахин холбогдох
> Шүүлт нь render дотор, мэдэгдэл нь event handler-т бичигдэнэ. Чатын сервертэй холболт бол гадаад систем.
```

```quiz
Аль код төгсгөлгүй давталт үүсгэх вэ?
- [x] `useEffect(() => { setItems([...items]); });`
- [ ] `useEffect(() => { document.title = title; }, [title]);`
- [ ] `const done = items.filter((item) => item.done);`
> Массивгүй effect render бүрт state-ийг шинэ массиваар сольж, дахин render үүсгэнэ: render → effect → render …
```

### Дүгнэлт

Effect-ийг зөвхөн гадаад системтэй синхрончлоход хэрэглэ. Тооцоолж болох
утгыг render дотор, хэрэглэгчийн үйлдлийг event handler-т бич. Effect
дотор `setState` харагдвал сэрэмжил: илүү render, хуучирсан утга,
төгсгөлгүй давталтын эх үүсвэр байж болно.
""",
            initial_code=vite(
                """\
import { useEffect, useState } from "react";
import { products } from "./products";

export default function App() {
  const [query, setQuery] = useState("");
  const [inStockOnly, setInStockOnly] = useState(false);
  const [visible, setVisible] = useState([]);
  const [count, setCount] = useState(0);

  // TODO: Доорх хоёр effect props, state-ээс тооцож болох утгыг state-д
  //       хуулж байна. visible, count-ийн state, effect-үүдийг устгаж,
  //       хоёуланг нь render дотор тооцоол.
  useEffect(() => {
    setVisible(
      products.filter(
        (product) =>
          product.name.toLowerCase().includes(query.toLowerCase()) &&
          (!inStockOnly || product.stock > 0),
      ),
    );
  }, [query]);

  useEffect(() => {
    setCount(visible.length);
  }, [visible]);

  return (
    <main>
      <h1>🔎 Бараа шүүх</h1>
      <label>
        Хайх
        <input value={query} onChange={(e) => setQuery(e.target.value)} />
      </label>
      <label>
        <input
          type="checkbox"
          checked={inStockOnly}
          onChange={(e) => setInStockOnly(e.target.checked)}
        />
        Зөвхөн үлдэгдэлтэй
      </label>
      <p>Олдсон: {count}</p>
      <ul>
        {visible.map((product) => (
          <li key={product.id}>
            {product.emoji} {product.name} —{" "}
            {product.stock > 0 ? `${product.stock} ширхэг` : "Дууссан"}
          </li>
        ))}
      </ul>
    </main>
  );
}
""",
                locked={
                    "products.js": """\
export const products = [
  { id: 1, name: "Банана", emoji: "🍌", stock: 24 },
  { id: 2, name: "Алим", emoji: "🍎", stock: 40 },
  { id: 3, name: "Жүрж", emoji: "🍊", stock: 15 },
  { id: 4, name: "Лууван", emoji: "🥕", stock: 30 },
  { id: 5, name: "Төмс", emoji: "🥔", stock: 60 },
  { id: 6, name: "Брокколи", emoji: "🥦", stock: 0 },
  { id: 7, name: "Сүү", emoji: "🥛", stock: 18 },
  { id: 8, name: "Бяслаг", emoji: "🧀", stock: 7 },
  { id: 9, name: "Талх", emoji: "🍞", stock: 12 },
  { id: 10, name: "Өндөг (10ш)", emoji: "🥚", stock: 20 },
];
""",
                },
                css=EFFECT_CSS,
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐ · 12 минут

Барааны шүүлтүүрийн өмнөх хөгжүүлэгч шүүсэн жагсаалт `visible`, олдсон
тоо `count`-ийг state-д хадгалж, effect-ээр «толин тусгал» хийжээ. Үр
дүнд нь «Зөвхөн үлдэгдэлтэй» checkbox ажиллахгүй, үсэг бүрт апп гурван
удаа render хийж байна. Илүү state, effect-үүдийг устгаж, хоёр утгыг
render дотор тооцоол.
""",
                tests=(
                    test(
                        "Хайлтаар бараа шүүгдэж, олдсон тоо шинэчлэгдэнэ",
                        """
render(<App />);
await user.type(screen.getByLabelText("Хайх"), "ал");
const text = screen.text();
expect(text).toContain("Алим");
expect(text).toContain("Талх");
expect(text).not.toContain("Банана");
expect(text).toContain("Олдсон: 2");
""",
                    ),
                    test(
                        "«Зөвхөн үлдэгдэлтэй» чагтлахад дууссан бараа алга болно",
                        """
render(<App />);
expect(screen.text()).toContain("Брокколи");
await user.click(screen.getByLabelText("Зөвхөн үлдэгдэлтэй"));
expect(screen.text()).not.toContain("Брокколи");
expect(screen.text()).toContain("Олдсон: 9");
""",
                    ),
                    test(
                        "Анх нээгдэхэд апп ганц л удаа render хийнэ",
                        """
const onRender = fn();
render(
  <React.Profiler id="app" onRender={onRender}>
    <App />
  </React.Profiler>,
);
expect(onRender).toHaveBeenCalledTimes(1);
""",
                    ),
                    test(
                        "Хайлтад нэг үсэг бичихэд ганц л render хийгдэнэ",
                        """
const onRender = fn();
render(
  <React.Profiler id="app" onRender={onRender}>
    <App />
  </React.Profiler>,
);
const before = onRender.mock.calls.length;
await user.type(screen.getByLabelText("Хайх"), "а");
expect(onRender.mock.calls.length - before).toBe(1);
""",
                    ),
                ),
                tips="""\
- `visible`, `count`-ийн `useState` ба хоёр `useEffect`-ийг бүхэлд нь
  устга.
- Эхний effect доторх `products.filter(…)` томьёог render дотор
  `const visible = …` болгон шилжүүл — одоо `inStockOnly` өөрчлөгдөхөд ч
  автоматаар дахин тооцогдоно.
- `count` бол зүгээр л `visible.length`.
- Тест render-ийг `<Profiler>`-оор (Модул 12) тоолно: effect доторх
  `setState` бүр нэмэлт render үүсгэдэг.
""",
                solution=solution(
                    App_jsx="""\
import { useState } from "react";
import { products } from "./products";

export default function App() {
  const [query, setQuery] = useState("");
  const [inStockOnly, setInStockOnly] = useState(false);

  const visible = products.filter(
    (product) =>
      product.name.toLowerCase().includes(query.toLowerCase()) &&
      (!inStockOnly || product.stock > 0),
  );
  const count = visible.length;

  return (
    <main>
      <h1>🔎 Бараа шүүх</h1>
      <label>
        Хайх
        <input value={query} onChange={(e) => setQuery(e.target.value)} />
      </label>
      <label>
        <input
          type="checkbox"
          checked={inStockOnly}
          onChange={(e) => setInStockOnly(e.target.checked)}
        />
        Зөвхөн үлдэгдэлтэй
      </label>
      <p>Олдсон: {count}</p>
      <ul>
        {visible.map((product) => (
          <li key={product.id}>
            {product.emoji} {product.name} —{" "}
            {product.stock > 0 ? `${product.stock} ширхэг` : "Дууссан"}
          </li>
        ))}
      </ul>
    </main>
  );
}
"""
                ),
            ),
        ),
        # --- 7 ------------------------------------------------------------------
        LessonSpec(
            title="Төсөл: Хайлтын апп",
            slug="tusul-hailtyn-app",
            description="Бичих явцад /api/products-оос хайж, ачаалах, алдаа, хоосон, үр дүнгийн төлөвтэй, хоцорсон хариунаас хамгаалалттай хайлтын апп бүтээнэ.",
            duration=2400,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Модул 5-д сурсан effect, хамаарал, цэвэрлэгээ, өгөгдөл татахыг нэг апп
  болгон нэгтгэх
- Хайлтын үгээр серверээс өгөгдөл татах
- Ачаалж буй, алдаа, хоосон, үр дүн гэсэн дөрвөн төлөвийг харуулах
- Хоцорсон хариу, илүүдэл хүсэлтээс (debounce) хамгаалах

### Яагаад чухал вэ

Хайлт бол онлайн дэлгүүр, мэдээний сайт, сургалтын платформ бүрт байдаг.
Хэрэглэгч бичих явцад үр дүн гарч ирэхийг хүлээдэг. Харин ард нь үсэг
бүрийн хүсэлт, хариунуудын уралдаан, удаан сүлжээ, серверийн алдаа гээд
энэ модулийн бүх асуудал нэг дор тулгарна. Энэ төсөл бол «Ногоон
сагс»-ын хайлтын анхны хувилбар — Модул 14-ийн дэлгүүрт дахин
хэрэглэгдэнэ.

### Шаардлага

| Төлөв | Хэзээ | Юу харагдах |
|---|---|---|
| Ачаалж буй | Хүсэлт явж байхад, эхний render-ээс эхлэн | «Ачаалж байна…» |
| Алдаа | Сервер алдаа буцаавал | `role="alert"`-тэй «Алдаа гарлаа. Дахин оролдоно уу.» |
| Хоосон | Хариу хоосон массив бол | «пицца» гэсэн хайлтад бараа олдсонгүй. |
| Үр дүн | Бараа олдвол | «3 бараа олдлоо» ба `ProductCard`-ийн жагсаалт |

- «Хайх» label-тэй input (`type="search"`).
- Хайлтын үг өөрчлөгдөх бүрт `GET /api/products?q=<үг>` хүсэлт явна.
  Хоосон үгэнд бүх бараа ирнэ.
- `response.ok`-ийг шалгана — 500-ийн хариу бараа мэт харагдах ёсгүй.
- Хуучин хүсэлтийн хожуу ирсэн хариу шинэ үр дүнг дарахгүй.
- Хоосон төлөв зөвхөн ачаалал дуусч, алдаагүй үед харагдана.

### Дизайн

```
┌ 🛒 Ногоон сагс — хайлт ─────────────┐
│ Хайх                                │
│ [ алим                            ] │
│ 1 бараа олдлоо                      │
│ ┌────────────┐                      │
│ │ 🍎 Алим    │                      │
│ │ Жимс       │                      │
│ │ 2,800₮     │                      │
│ └────────────┘                      │
└─────────────────────────────────────┘
```

### API

| Хүсэлт | Хариу |
|---|---|
| `GET /api/products` | 10 бараа: `id`, `name`, `price`, `category`, `emoji`, `stock` |
| `GET /api/products?q=алим` | Нэр, ангилал зэрэг текст талбарт «алим» орсон бараа (том, жижиг үсэг хамаагүй) |
| `…&_delay=2000` | Хариуг 2 секунд хоцрооно — ачааллын төлөвийг харах |
| `…&_status=500` | Серверийн алдаа — алдааны төлөвийг харах |

Кирилл үсгийг URL-д `encodeURIComponent`-оор кодлох нь зөв зуршил:
`` `/api/products?q=${encodeURIComponent(query)}` ``.

Эхлэл кодод хоёр файл бий:

| Файл | Үүрэг |
|---|---|
| `App.jsx` | Хайлтын state, effect, дөрвөн төлөв — чиний бичих хэсэг |
| 🔒 `ProductCard.jsx` | Нэг барааны карт, `product` prop авна |

### Алхмууд

1. `products`, `loading`, `error` state нэм. `loading`-ийг `true`-ээс
   эхлүүл.
2. `query`-ээс хамаарсан effect бич: эхэнд нь `setLoading(true)`,
   `setError(null)`, дараа нь `fetch`, `response.ok`-ийн шалгалт.
3. Цэвэрлэгээнд `ignore = true` (эсвэл `controller.abort()`).
4. Дөрвөн төлөвийг нөхцөлт render-ээр харуул (Модул 2): ачаалж байна →
   алдаа → хоосон → үр дүн.
5. «Хөтөч» дээр туршиж үз: хурдан бич, URL-даа түр `&_delay=2000`,
   `&_status=500` нэмж төлөв бүрийг хар, дараа нь буцааж ав.

### Нэмэлт: debounce

Одоо «алим» гэж бичихэд 4 хүсэлт явна: «а», «ал», «али», «алим».
Хэрэглэгч бичиж дуустал 300 мс хүлээвэл ганц хүсэлт хангалттай — үүнийг
**debounce** гэдэг. Timer ба цэвэрлэгээгээр хийнэ:

```jsx
useEffect(() => {
  let ignore = false;
  setLoading(true);

  const timer = setTimeout(() => {
    // энд fetch хийж, if (!ignore) … гэж state-ээ шинэчилнэ
  }, 300);

  return () => {
    ignore = true;
    clearTimeout(timer); // дараагийн үсэг өмнөх timer-ийг цуцална
  };
}, [query]);
```

Шинэ үсэг бичигдэх бүрт цэвэрлэгээ өмнөх timer-ийг цуцална. Зөвхөн
сүүлийн үсгийн дараах timer дуусч, хүсэлт явна. `setLoading(true)` нь
timer-ээс гадна байгаа тул хүлээх хооронд ч «Ачаалж байна…» харагдана.
Модул 6-д үүнийг `useDebounce` hook болгоно.

### Нэмэлт сорилт

- Ангиллаар шүүх `<select>` нэмэх — API нь `&category=Жимс`-ийг ойлгодог.
- Алдааны үед «Дахин оролдох» товч — дарахад тоолуур state нэмэгдэж,
  түүнийг хамаарал болгосон effect дахин ажиллана.
- Хайлтын үгийг барааны нэрэнд `<mark>`-аар тодруулах.

```quiz
Хэрэглэгч «ал» гэж бичээд хүлээлгүй «алим» болгов. «ал»-ын хариу хамгийн сүүлд ирвэл `ignore`-той апп юу харуулах вэ?
- [ ] «ал»-ын үр дүн (Алим, Талх)
- [x] «алим»-ын үр дүн (Алим)
- [ ] Хоосон жагсаалт
> «ал»-ын effect-ийн цэвэрлэгээ `ignore`-ийг `true` болгосон тул түүний хариу хаягдана.
```

```quiz
«Олдсонгүй» мэдэгдлийг хэзээ харуулах вэ?
- [ ] `products.length === 0` үед үргэлж
- [x] Ачаалал дууссан, алдаагүй, массив хоосон үед
- [ ] Хайлтын үг хоосон үед
> Эс бөгөөс хариу ирэхээс өмнө, эсвэл алдааны үед «олдсонгүй» гэж худлаа хэлнэ.
```

### Дүгнэлт

Хайлтын апп effect-ийн бүх санааг нэгтгэдэг: хамаарал (`query`), өгөгдөл
татах, дөрвөн төлөв, цэвэрлэгээгээр хуучин хариу ба timer-ийг цуцлах.
Бодит төсөлд энэ логикийг TanStack Query (Модул 9), `useDebounce` зэрэг
hook-оор (Модул 6) товчилдог — тэд цаанаа яг энэ ажлыг хийдэг.
""",
            initial_code=vite(
                """\
import { useEffect, useState } from "react";
import ProductCard from "./ProductCard";

export default function App() {
  const [query, setQuery] = useState("");
  // TODO 1: products, loading, error state

  // TODO 2: query өөрчлөгдөх бүрт `/api/products?q=…`-ээс бараа татах effect.
  //         response.ok-ийг шалгаж, хуучирсан хариуг хая.
  // Нэмэлт: 300 мс debounce (setTimeout + цэвэрлэгээнд clearTimeout)

  return (
    <main>
      <h1>🛒 Ногоон сагс — хайлт</h1>
      <label>
        Хайх
        <input
          type="search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Жишээ нь: алим, жимс"
        />
      </label>

      {/* TODO 3: ачаалж буй, алдаа, хоосон, үр дүн гэсэн дөрвөн төлөв */}
    </main>
  );
}
""",
                locked={
                    "ProductCard.jsx": """\
export default function ProductCard({ product }) {
  return (
    <article className="card">
      <h2>
        {product.emoji} {product.name}
      </h2>
      <p className="muted">{product.category}</p>
      <p>{product.price.toLocaleString("en-US")}₮</p>
    </article>
  );
}
""",
                },
                css=EFFECT_CSS,
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐⭐ · 40 минут

«Заавар» дахь шаардлага, дизайн, API-гийн дагуу «Ногоон сагс»-ын хайлтын
аппыг бүтээ. Хайлтын үг өөрчлөгдөх бүрт серверээс бараа татаж, ачаалж
буй, алдаа, хоосон, үр дүн гэсэн дөрвөн төлөвийг харуулна. Тестүүд
дууссан аппын хүлээн авах шалгуурыг жагсааж байгаа.
""",
                tests=(
                    test(
                        "Хариу ирэх хүртэл «Ачаалж байна…», дараа нь бүх бараа харагдана",
                        """
render(<App />);
expect(screen.text()).toMatch(/Ачаалж байна/);
await screen.findByText(/Банана/);
const text = screen.text();
for (const name of ["Алим", "Бяслаг", "Талх"]) {
  expect(text).toContain(name);
}
expect(text).not.toMatch(/Ачаалж байна/);
""",
                    ),
                    test(
                        "Бичсэн үгээр /api/products?q=… хүсэлт явж, тохирох бараа л харагдана",
                        """
render(<App />);
await screen.findByText(/Банана/);
await user.type(screen.getByLabelText("Хайх"), "алим");
await waitFor(() => {
  expect(screen.text()).toContain("Алим");
  expect(screen.text()).not.toContain("Банана");
});
const searched = api.requests.some((request) => {
  const url = new URL(request.path, "http://localhost");
  return url.pathname === "/api/products" && url.searchParams.get("q") === "алим";
});
expect(searched).toBe(true);
""",
                    ),
                    test(
                        "Илэрц олдохгүй бол «… олдсонгүй» мэдэгдэл харагдана",
                        """
render(<App />);
await screen.findByText(/Банана/);
await user.type(screen.getByLabelText("Хайх"), "пицца");
await screen.findByText(/олдсонгүй/);
expect(screen.text()).not.toContain("Банана");
expect(screen.text()).not.toMatch(/Ачаалж байна/);
""",
                    ),
                    test(
                        'Серверийн алдаа гарвал role="alert"-тэй «Алдаа гарлаа» мэдэгдэл харагдана',
                        """
api.fail("/api/products", 500);
render(<App />);
const alert = await screen.findByRole("alert");
expect(alert).toHaveTextContent(/Алдаа гарлаа/);
expect(screen.text()).not.toMatch(/Ачаалж байна/);
expect(screen.text()).not.toMatch(/олдсонгүй/);
""",
                    ),
                    test(
                        "Хожуу ирсэн хуучин хариу шинэ үр дүнг дарахгүй",
                        """
const realFetch = window.fetch;
const asked = [];
window.fetch = async (input, init) => {
  const q = new URL(String(input), "http://localhost").searchParams.get("q");
  asked.push(q);
  if (q === "а") {
    await sleep(500);
    if (init && init.signal && init.signal.aborted) {
      throw new DOMException("The operation was aborted.", "AbortError");
    }
  }
  return realFetch(input, init);
};
try {
  render(<App />);
  await screen.findByText(/Банана/);
  const input = screen.getByLabelText("Хайх");
  await user.type(input, "а");
  await waitFor(() => expect(asked).toContain("а"));
  await user.type(input, "лим");
  await waitFor(() => {
    expect(screen.text()).toContain("Алим");
    expect(screen.text()).not.toContain("Банана");
  });
  await act(async () => {
    await sleep(700);
  });
  expect(screen.text()).toContain("Алим");
  expect(screen.text()).not.toContain("Банана");
} finally {
  window.fetch = realFetch;
}
""",
                    ),
                ),
                tips="""\
- `loading`-ийг `true`-ээс эхлүүл — эхний render-ээс «Ачаалж байна…»
  харагдана. Effect-ийн эхэнд `setLoading(true)`, `setError(null)`.
- Хамаарал нь `[query]`. URL:
  `` `/api/products?q=${encodeURIComponent(query)}` `` — хоосон `q` бүх
  барааг буцаана.
- Төлөвүүдийг дарааллаар нь шалга: ачаалж байна → алдаа → хоосон → үр
  дүн. Хоосон төлөвийг зөвхөн ачаалал дуусч, алдаагүй үед харуул.
- Хуучин хариу: `ignore` тэмдэглэл эсвэл `AbortController`. Debounce
  хийвэл цэвэрлэгээнд `clearTimeout`-ийг ч бүү мартаарай.
""",
                solution=solution(
                    App_jsx="""\
import { useEffect, useState } from "react";
import ProductCard from "./ProductCard";

export default function App() {
  const [query, setQuery] = useState("");
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let ignore = false;
    setLoading(true);
    setError(null);

    // Debounce: бичиж дуустал 300 мс хүлээнэ.
    const timer = setTimeout(async () => {
      try {
        const response = await fetch(`/api/products?q=${encodeURIComponent(query.trim())}`);
        if (!response.ok) {
          throw new Error(`Сервер ${response.status} алдаа буцаалаа`);
        }
        const data = await response.json();
        if (!ignore) setProducts(data);
      } catch (err) {
        if (!ignore) setError(err.message);
      } finally {
        if (!ignore) setLoading(false);
      }
    }, 300);

    return () => {
      ignore = true;
      clearTimeout(timer);
    };
  }, [query]);

  return (
    <main>
      <h1>🛒 Ногоон сагс — хайлт</h1>
      <label>
        Хайх
        <input
          type="search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Жишээ нь: алим, жимс"
        />
      </label>

      {loading ? (
        <p className="muted">Ачаалж байна…</p>
      ) : error ? (
        <p className="error" role="alert">
          Алдаа гарлаа. Дахин оролдоно уу.
        </p>
      ) : products.length === 0 ? (
        <p>«{query.trim()}» гэсэн хайлтад бараа олдсонгүй.</p>
      ) : (
        <>
          <p className="muted">{products.length} бараа олдлоо</p>
          <div className="grid">
            {products.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        </>
      )}
    </main>
  );
}
"""
                ),
            ),
        ),
    ],
)
