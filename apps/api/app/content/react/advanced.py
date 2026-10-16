"""Модул 10 — Ахисан React.

React дэлгэцийг хэрхэн шинэчилдэг (trigger → render → commit), state яагаад
мод дахь байрлалдаа хадгалагддаг, render-ийн алдааг хэрхэн хашиж, кодыг
хэрэгтэй үед нь ачаалах, шинэчлэлтийг яаралтай ба яаралгүй гэж ялгах
(transition, deferred value) талаар гүнзгий ойлголт өгнө.
"""

from app.content.react.common import solution, test, vite
from app.content.types import ExerciseSpec, LessonSpec, ModuleSpec
from app.models.enums import LessonLanguage

JSX = LessonLanguage.JSX

# Sandbox-д файлууд санах ойд байгаа тул dynamic import() шууд биелнэ.
# Сүлжээгээр татаж буйг дуурайх туслах (lazy, transition хичээлүүдэд).
NETWORK_JS = """\
// Sandbox-д файлууд санах ойд байгаа тул import() шууд биелдэг.
// slow() нь сүлжээгээр татаж буй мэт Promise-ийг хоцрооно.
// Бодит төсөлд үүнийг бичихгүй: lazy(() => import("./Reports")).
export function slow(promise, ms = 800) {
  return new Promise((resolve) => setTimeout(() => resolve(promise), ms));
}
"""

ADVANCED = ModuleSpec(
    title="Модул 10 — Ахисан React",
    description=(
        "Render хийх загвар, reconciliation, error boundary, lazy ба Suspense, "
        "useTransition, useDeferredValue-г гүнзгий ойлгоно."
    ),
    lessons=[
        # ------------------------------------------------------------------
        LessonSpec(
            title="React хэрхэн render хийдэг",
            slug="render-model",
            description="Trigger → render → commit, virtual DOM, цэвэр component ба render-ийн ялгаа.",
            duration=900,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Дэлгэц шинэчлэгдэх гурван алхмыг ойлгох: trigger → render → commit
- Virtual DOM гэж юу болохыг мэдэх
- Render хийх нь DOM-ыг шинэчлэх гэсэн үг биш гэдгийг ойлгох
- Цэвэр (pure) component бичих, render дотор юу хийж болохгүйг мэдэх

### Яагаад чухал вэ

Одоог хүртэл `setCount` дуудахад дэлгэц «өөрөө» шинэчлэгдэж байлаа. Цаана
нь юу болдгийг мэдэхгүй бол тоо санаандгүй «үсрэх», жагсаалтын дараалал
гэнэт өөрчлөгдөх зэрэг хачин алдааг ойлгоход хэцүү. Энэ модулийн бусад
хичээл (reconciliation, Suspense, transition) бүгд энэ загвар дээр
суурилна.

### Гурван алхам

Ресторантай зүйрлэе: зочин захиалга өгнө (trigger), тогооч хоол хийнэ
(render), зөөгч ширээнд тавина (commit).

1. **Trigger** — render-ийг юу эхлүүлэв:
   - анхны render: `createRoot(...).render(<App />)`;
   - state шинэчлэгдэх: `setCount(...)`. Тухайн component болон түүний
     доторх бүх component дахин render болно.
2. **Render** — React таны component **функцийг дуудна**. Функц JSX
   буцаана. Дахин render үед React шинэ JSX-ийг өмнөхтэй харьцуулж, юу
   өөрчлөгдснийг тооцно. Энэ үед DOM-д огт хүрэхгүй.
3. **Commit** — React зөвхөн **өөрчлөгдсөн** хэсгийг DOM-д хэрэглэнэ.
   Үүний дараа хөтөч дэлгэцийг зурж (paint), effect-үүд ажиллана.

```jsx
function Clock({ time }) {
  return (
    <>
      <h1>{time}</h1>
      <input placeholder="Энд бичээд үз" />
    </>
  );
}
```

`time` секунд тутам өөрчлөгдөхөд `Clock` дахин render болно. Гэвч React
зөвхөн `<h1>`-ийн текстийг солино — `<input>`-д бичсэн текст, фокус
хэвээр үлдэнэ.

### Virtual DOM

JSX нь `{ type: "h1", props: { children: "12:00" } }` мэт энгийн
JavaScript объект (React element) үүсгэдэг. Эдгээр объектын модыг
**virtual DOM** гэж нэрлэдэг. Объект үүсгэх хямд, жинхэнэ DOM-ыг өөрчлөх
үнэтэй. Тиймээс React эхлээд хуучин, шинэ хоёр модыг харьцуулаад
(дараагийн хичээлийн reconciliation), DOM-д аль болох цөөн өөрчлөлт хийнэ.

### Render ≠ DOM-ын шинэчлэл

Component render болсон нь DOM өөрчлөгдөнө гэсэн үг биш. Эцэг
component-ийн state өөрчлөгдөхөд хүүхдүүд нь дахин render болно, гэхдээ
тэдний JSX өмнөхтэйгөө ижил бол React DOM-д хүрэхгүй. Render-ийг хэмжих,
илүүц render-ээс сэргийлэх нь Модул 12-ын сэдэв.

### Component цэвэр байх ёстой

Render нь математикийн функц шиг байх ёстой: **ижил props, state → ижил
JSX**, бас гадна юу ч өөрчлөхгүй. Учир нь React component-ийг хэдэн удаа,
ямар дарааллаар дуудахаа өөрөө шийднэ: зарим render-ийг хаяж дахин
эхлүүлдэг (transition), хөгжүүлэлтийн үед хоёр удаа дууддаг (StrictMode).

```jsx
let guest = 0;

function Cup() {
  guest = guest + 1; // ❌ render дотор гаднах хувьсагчийг өөрчилж байна
  return <h2>Аяга №{guest}</h2>;
}
```

`<Cup />`-ийг гурван удаа render хийвэл эхэндээ 1, 2, 3 гэж харагдана.
Эцэг нь дахин render болмогц 4, 5, 6 болно. Засвар — утгыг props-оор
дамжуулна:

```jsx
function Cup({ guest }) {
  return <h2>Аяга №{guest}</h2>;
}

// <Cup guest={1} />  <Cup guest={2} />  <Cup guest={3} />
```

Render дотор хийж **болохгүй** зүйлс:

- гаднах хувьсагч, объект, массивыг өөрчлөх (`list.push(...)`, `items.sort()`);
- props, state-ийг шууд өөрчлөх;
- `fetch`, `setTimeout`, `document.title = …` зэрэг гаж нөлөө (side
  effect) — эдгээр event handler эсвэл effect-д байрлана.

Харин render дотор **шинээр үүсгэсэн** утгаа өөрчлөх нь зүгээр:

```jsx
function CheapestFirst({ items }) {
  const sorted = [...items];                // ✅ шинэ массив
  sorted.sort((a, b) => a.price - b.price); // зөвхөн өөрийн хуулбараа өөрчилнө
  return <List items={sorted} />;
}
```

`sort()` анхны массивыг өөрчилдгийг Модул 0-д үзсэн. `items.toSorted(...)`
ч мөн шинэ массив буцаана.

### StrictMode

Vite төслийн `main.jsx`-д `<StrictMode>` байдаг. Хөгжүүлэлтийн үед тэр
component бүрийг **хоёр удаа** render хийж, цэвэр биш кодыг ил гаргадаг
(production-д нэг удаа). Энэ sandbox-д StrictMode байхгүй — тиймээс
алдааг өөрөө анзаарах хэрэгтэй.

```quiz
Гаднах `guest` хувьсагчтай `Cup`-ийг гурван удаа render хийв. Дараа нь эцэг component-ийн state өөрчлөгдөж бүгд дахин render болов. Одоо дэлгэц дээр ямар дугаар харагдах вэ?
- [ ] 1, 2, 3
- [x] 4, 5, 6
- [ ] 1, 1, 1
> `guest` component-ийн гадна байгаа тул render бүр түүнийг нэмэгдүүлсээр байна. Үр дүн нь хэдэн удаа render хийснээс хамаарч байна — цэвэр биш component-ийн шинж.
```

```quiz
Render алхамд юу болдог вэ?
- [ ] React DOM-ыг шууд өөрчилнө
- [x] React component функцийг дуудаж, шинэ JSX-ийг өмнөхтэй харьцуулна
- [ ] Хөтөч дэлгэцийг дахин зурна
> DOM-ыг өөрчлөх нь commit алхам. Render нь зөвхөн «юу харагдах ёстойг» тооцно.
```

### Дүгнэлт

Trigger (анхны render эсвэл state өөрчлөгдөх) → render (component
функцийг дуудаж харьцуулах) → commit (DOM-д зөвхөн ялгааг хэрэглэх).
Component цэвэр байх ёстой: ижил оролтод ижил JSX, гадна юу ч өөрчлөхгүй.
""",
            initial_code=vite(
                """\
import { useState } from "react";
import { products } from "./data";

let position = 0;

function ProductRow({ product }) {
  // ❌ Render бүрт гаднах хувьсагчийг өөрчилж байна
  position = position + 1;
  return (
    <li>
      {position}. {product.emoji} {product.name} — {product.price}₮
    </li>
  );
}

function CheapestFirst({ items }) {
  // ❌ sort() нь props-оор ирсэн анхны массивыг өөрчилнө
  const sorted = items.sort((a, b) => a.price - b.price);
  return (
    <ul>
      {sorted.map((product) => (
        <ProductRow key={product.id} product={product} />
      ))}
    </ul>
  );
}

export default function App() {
  const [dark, setDark] = useState(false);

  return (
    <main
      style={{
        padding: 16,
        background: dark ? "#1f2937" : "#ffffff",
        color: dark ? "#f9fafb" : "#111827",
      }}
    >
      <button onClick={() => setDark(!dark)}>Өнгө солих</button>
      <h2>Дэлгүүрийн дараалал</h2>
      <ul>
        {products.map((product) => (
          <ProductRow key={product.id} product={product} />
        ))}
      </ul>
      <h2>Хямдаас нь</h2>
      <CheapestFirst items={products} />
    </main>
  );
}
""",
                locked={
                    "data.js": """\
export const products = [
  { id: 1, name: "Банана", price: 3500, emoji: "🍌" },
  { id: 2, name: "Алим", price: 2800, emoji: "🍎" },
  { id: 3, name: "Сүү", price: 3200, emoji: "🥛" },
  { id: 4, name: "Талх", price: 2500, emoji: "🍞" },
];
"""
                },
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐ · 12 минут

`App.jsx`-д хоёр цэвэр биш component байна. «Хөтөч» дээр «Өнгө солих»-ийг
хэд дарж үз: дугаарууд өссөөр, дэлгүүрийн дараалал өөрчлөгдөнө.
`ProductRow`, `CheapestFirst`-ийг цэвэр болго: дугаар props-оор ирдэг,
эрэмбэлэхдээ анхны массивыг өөрчилдөггүй байх ёстой. Мөр бүр дугаараар
эхэлсэн хэвээр («1. 🍌 Банана — 3500₮»).
""",
                tests=(
                    test(
                        "Хоёр жагсаалт хоёулаа 1-ээс дугаарлагдана",
                        """
render(<App />);
const lists = screen.getAllByRole("list");
expect(lists).toHaveLength(2);
for (const list of lists) {
  const numbers = within(list)
    .getAllByRole("listitem")
    .map((item) => parseInt(item.textContent, 10));
  expect(numbers).toEqual([1, 2, 3, 4]);
}
""",
                    ),
                    test(
                        "Дахин render хийхэд дугаарууд өөрчлөгдөхгүй",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: "Өнгө солих" }));
await user.click(screen.getByRole("button", { name: "Өнгө солих" }));
for (const list of screen.getAllByRole("list")) {
  const numbers = within(list)
    .getAllByRole("listitem")
    .map((item) => parseInt(item.textContent, 10));
  expect(numbers).toEqual([1, 2, 3, 4]);
}
""",
                    ),
                    test(
                        "«Хямдаас нь» жагсаалт үнэ өсөх дарааллаар харагдана",
                        """
const names = ["Банана", "Алим", "Сүү", "Талх"];
const nameOf = (item) => names.find((name) => item.textContent.includes(name));
render(<App />);
const cheap = screen.getAllByRole("list")[1];
expect(within(cheap).getAllByRole("listitem").map(nameOf)).toEqual([
  "Талх",
  "Алим",
  "Сүү",
  "Банана",
]);
""",
                    ),
                    test(
                        "Дэлгүүрийн дараалал, анхны массив өөрчлөгдөхгүй",
                        """
const names = ["Банана", "Алим", "Сүү", "Талх"];
const nameOf = (item) => names.find((name) => item.textContent.includes(name));
render(<App />);
await user.click(screen.getByRole("button", { name: "Өнгө солих" }));
const shop = screen.getAllByRole("list")[0];
expect(within(shop).getAllByRole("listitem").map(nameOf)).toEqual(names);
expect(mod("./data").products.map((product) => product.name)).toEqual(names);
""",
                    ),
                ),
                tips="""\
- Дугаарыг `map`-ийн хоёр дахь аргумент `index`-ээс авч
  `position={index + 1}` гэж props-оор дамжуул. Тэгвэл `let position`
  хувьсагч огт хэрэггүй болно.
- `CheapestFirst` өөрийн жагсаалтыг бас 1-ээс дугаарлах ёстой — тэнд ч
  `index`-ийг ашигла.
- `items.sort(...)` биш `[...items].sort(...)` эсвэл `items.toSorted(...)`.
- Өөрийгөө шалгах арга: «Өнгө солих»-ийг хэд ч дарсан жагсаалтууд
  өөрчлөгдөх ёсгүй.
""",
                solution=solution(
                    App_jsx="""\
import { useState } from "react";
import { products } from "./data";

function ProductRow({ product, position }) {
  return (
    <li>
      {position}. {product.emoji} {product.name} — {product.price}₮
    </li>
  );
}

function CheapestFirst({ items }) {
  const sorted = [...items].sort((a, b) => a.price - b.price);
  return (
    <ul>
      {sorted.map((product, index) => (
        <ProductRow key={product.id} product={product} position={index + 1} />
      ))}
    </ul>
  );
}

export default function App() {
  const [dark, setDark] = useState(false);

  return (
    <main
      style={{
        padding: 16,
        background: dark ? "#1f2937" : "#ffffff",
        color: dark ? "#f9fafb" : "#111827",
      }}
    >
      <button onClick={() => setDark(!dark)}>Өнгө солих</button>
      <h2>Дэлгүүрийн дараалал</h2>
      <ul>
        {products.map((product, index) => (
          <ProductRow key={product.id} product={product} position={index + 1} />
        ))}
      </ul>
      <h2>Хямдаас нь</h2>
      <CheapestFirst items={products} />
    </main>
  );
}
"""
                ),
            ),
        ),
        # ------------------------------------------------------------------
        LessonSpec(
            title="Reconciliation ба component-ийн хувийн шинж",
            slug="reconciliation",
            description="State хаана хадгалагддаг, хэзээ үлдэж, хэзээ арилдаг вэ; key-ээр state-ийг шинэчлэх.",
            duration=1020,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Reconciliation буюу React хоёр модыг хэрхэн харьцуулдгийг ойлгох
- State нь component-ийн мод дахь **байрлалтай** холбоотойг мэдэх
- Ижил байрлал + ижил төрөл → state үлдэнэ, өөр төрөл → state арилна
- `key`-ээр state-ийг зориуд дахин эхлүүлэх

### Яагаад чухал вэ

Чат апп-д Батад мессеж бичиж байгаад илгээлгүй Сараа руу шилжлээ гэж
бодъё. Бичсэн текст тань Сараагийн чатад үлдсэн байвал буруу хүнд илгээх
аюултай. Эсвэл эсрэгээрээ, нэг checkbox дарахад формын бүх талбар гэнэт
хоосорно. Хоёулаа reconciliation-ийн дүрмийг мэдэхгүйгээс гардаг алдаа.

### Reconciliation

Render бүрийн дараа React шинэ element-ийн модыг өмнөхтэй нь харьцуулна.
Үүнийг **reconciliation** гэдэг. Хоёр үндсэн дүрэм:

1. Нэг байрлалд **ижил төрлийн** element байвал React хуучин component-оо
   (state, DOM-той нь) үлдээж, зөвхөн props-ыг шинэчилнэ.
2. **Өөр төрөл** гарч ирвэл хуучныг нь бүхэлд нь (state-тэй нь) устгаж,
   шинийг эхнээс нь үүсгэнэ.

State нь component функц дотор биш, React-ийн мод дахь **байрлалд**
хадгалагддаг.

### Ижил байрлал, ижил төрөл — state үлдэнэ

```jsx
function App() {
  const [fancy, setFancy] = useState(false);
  return (
    <div>
      {fancy ? <Counter color="gold" /> : <Counter color="gray" />}
      <label>
        <input type="checkbox" checked={fancy} onChange={(e) => setFancy(e.target.checked)} />
        Гоё загвар
      </label>
    </div>
  );
}
```

Хоёр салбар хоёулаа `<div>`-ийн эхний хүүхэд, хоёулаа `Counter`. React-ийн
хувьд энэ бол **нэг л** component — checkbox дарахад тоологчийн утга
хадгалагдана. Код дээр хоёр өөр мөр байгаа нь хамаагүй, React зөвхөн
буцаасан модыг хардаг.

### Өөр төрөл — state устна

```jsx
{isPaused ? <p>Түр зогссон</p> : <Counter />}
```

`Counter` нь `<p>`-ээр солигдоход Counter-ийн state устна. Буцаад гарч
ирэхэд 0-ээс эхэлнэ. Эцэг элемент нь өөр болоход ч (`<div>` → `<section>`)
доторх бүх мод шинээр үүснэ.

### Түгээмэл алдаа: component дотор component зарлах

```jsx
function Form() {
  const [text, setText] = useState("");

  function Field() { // ❌ render бүрт ШИНЭ функц үүснэ
    return <input value={text} onChange={(e) => setText(e.target.value)} />;
  }

  return <Field />;
}
```

Render бүрт `Field` шинэ функц болж үүсдэг тул React үүнийг «өөр төрөл» гэж
үзнэ: нэг үсэг бичих бүрт `<input>` устаж шинээр үүсэн, фокус алдагдана.
Component-ийг үргэлж файлын дээд түвшинд зарла.

### key-ээр state-ийг дахин эхлүүлэх

Заримдаа эсрэгээрээ ижил component-ийн state-ийг зориуд шинэчлэх
хэрэгтэй. Үүнд `key` ашиглана. `key` зөвхөн жагсаалтад биш, хаана ч
ажилладаг:

```jsx
<Chat key={contact.id} contact={contact} />
```

`key` өөрчлөгдөхөд React үүнийг **өөр** component гэж үзэж, хуучныг нь
устгаад шинийг эхнээс нь үүсгэнэ. Бүх state дахин эхэлнэ.

Ялангуяа props-оос анхны утга авдаг state-д хэрэгтэй:

```jsx
function Chat({ contact }) {
  const [to, setTo] = useState(contact.email); // зөвхөн АНХНЫ render-д
  // ...
}
```

`useState(contact.email)` нь анхны render-д л утга авна. Дараа нь `contact`
өөрчлөгдсөн ч `to` хуучнаараа үлдэнэ. `useEffect`-ээр state-ийг «хуулах»
шаардлагагүй — `key={contact.id}` нэмэхэд л хангалттай.

Жагсаалтын `key` ч ижил дүрмээр ажилладаг: `key={index}` бол мөр устгах,
эрэмбэлэхэд state буруу мөрөнд «наалддаг» (Модул 2).

```quiz
`{showA ? <Counter key="a" /> : <Counter key="b" />}` — `showA`-г солиход тоологчид юу болох вэ?
- [ ] Утга нь хадгалагдана — хоёулаа `Counter`
- [x] 0-ээс эхэлнэ — `key` өөр тул өөр component
- [ ] React алдаа заана
> `key` нь component-ийн хувийн шинжийн нэг хэсэг. Төрөл ижил ч `key` өөр бол React шинээр үүсгэнэ.
```

```quiz
Доорх кодын алдааг ол: `function List() { function Item() { … } return <Item />; }`
- [ ] `Item` нэр том үсгээр эхэлсэн
- [x] `Item` render бүрт шинээр үүсэж, state нь байнга устна
- [ ] `return` дотор хаалт дутуу
> Component-ийг өөр component дотор зарлахгүй — файлын дээд түвшинд гарга.
```

### Дүгнэлт

React state-ийг мод дахь байрлалаар нь хадгална. Ижил байрлалд ижил төрөл
байвал state үлдэнэ, төрөл эсвэл `key` өөрчлөгдвөл state шинээр эхэлнэ.
State-ийг зориуд шинэчлэх хамгийн энгийн арга бол `key`.
""",
            initial_code=vite(
                """\
import { useState } from "react";

const contacts = [
  { id: 1, name: "Бат", email: "bat@example.mn" },
  { id: 2, name: "Сараа", email: "saraa@example.mn" },
  { id: 3, name: "Ану", email: "anu@example.mn" },
];

function Chat({ contact }) {
  const [to, setTo] = useState(contact.email);
  const [text, setText] = useState("");

  function handleSubmit(event) {
    event.preventDefault();
    console.log(`${to} хаяг руу илгээв: ${text}`);
    setText("");
  }

  return (
    <form onSubmit={handleSubmit} style={{ display: "grid", gap: 8, minWidth: 260 }}>
      <h2>Чат: {contact.name}</h2>
      <label>
        Хэнд
        <input value={to} onChange={(event) => setTo(event.target.value)} />
      </label>
      <label>
        Мессеж
        <textarea value={text} onChange={(event) => setText(event.target.value)} />
      </label>
      <button>Илгээх</button>
    </form>
  );
}

export default function App() {
  const [selected, setSelected] = useState(contacts[0]);

  return (
    <main style={{ display: "flex", gap: 24 }}>
      <nav style={{ display: "grid", gap: 8, alignContent: "start" }}>
        {contacts.map((contact) => (
          <button
            key={contact.id}
            onClick={() => setSelected(contact)}
            aria-pressed={contact.id === selected.id}
          >
            {contact.name}
          </button>
        ))}
      </nav>
      {/* TODO: харилцагч солигдоход Chat эхнээс нь эхэлдэг болго */}
      <Chat contact={selected} />
    </main>
  );
}
"""
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐ · 10 минут

«Хөтөч» дээр «Бат»-д мессеж бичээд «Сараа» руу шилжиж үз: бичсэн текст,
«Хэнд» талбарын имэйл хоёулаа хуучнаараа үлдэнэ. Харилцагч солигдох бүрт
`Chat` эхнээс нь эхэлдэг болгож засаарай. `Chat`-ийн кодыг өөрчлөх
шаардлагагүй.
""",
                tests=(
                    test(
                        "Харилцагч солиход мессежийн талбар хоосорно",
                        """
render(<App />);
await user.type(screen.getByLabelText("Мессеж"), "Сайн уу");
await user.click(screen.getByRole("button", { name: "Сараа" }));
expect(screen.getByLabelText("Мессеж")).toHaveValue("");
""",
                    ),
                    test(
                        "Харилцагч солиход «Хэнд» талбарт шинэ харилцагчийн имэйл гарна",
                        """
render(<App />);
expect(screen.getByLabelText("Хэнд")).toHaveValue("bat@example.mn");
await user.click(screen.getByRole("button", { name: "Ану" }));
expect(screen.getByLabelText("Хэнд")).toHaveValue("anu@example.mn");
""",
                    ),
                    test(
                        "Нэг харилцагч дээр байх үед бичсэн текст хадгалагдана",
                        """
render(<App />);
await user.type(screen.getByLabelText("Мессеж"), "Маргааш уулзъя");
await user.click(screen.getByRole("button", { name: "Бат" }));
expect(screen.getByLabelText("Мессеж")).toHaveValue("Маргааш уулзъя");
expect(screen.getByRole("heading", { name: "Чат: Бат" })).toBeInTheDocument();
""",
                    ),
                ),
                tips="""\
- Асуудал нь `Chat` биш, түүнийг хэрхэн render хийж байгаад байна: React-ийн
  хувьд харилцагч солигдсон ч энэ бол ижил байрлал дахь ижил `Chat`.
- React-д «энэ өөр чат» гэж хэлэх нэг prop бий — харилцагч бүрт өөр байх
  утга өг (`id` тохиромжтой).
- `useEffect`-ээр `setTo(contact.email)`, `setText("")` дуудах шаардлагагүй
  — нэмэлт render хийж, анивчуулна.
""",
                solution=solution(
                    App_jsx="""\
import { useState } from "react";

const contacts = [
  { id: 1, name: "Бат", email: "bat@example.mn" },
  { id: 2, name: "Сараа", email: "saraa@example.mn" },
  { id: 3, name: "Ану", email: "anu@example.mn" },
];

function Chat({ contact }) {
  const [to, setTo] = useState(contact.email);
  const [text, setText] = useState("");

  function handleSubmit(event) {
    event.preventDefault();
    console.log(`${to} хаяг руу илгээв: ${text}`);
    setText("");
  }

  return (
    <form onSubmit={handleSubmit} style={{ display: "grid", gap: 8, minWidth: 260 }}>
      <h2>Чат: {contact.name}</h2>
      <label>
        Хэнд
        <input value={to} onChange={(event) => setTo(event.target.value)} />
      </label>
      <label>
        Мессеж
        <textarea value={text} onChange={(event) => setText(event.target.value)} />
      </label>
      <button>Илгээх</button>
    </form>
  );
}

export default function App() {
  const [selected, setSelected] = useState(contacts[0]);

  return (
    <main style={{ display: "flex", gap: 24 }}>
      <nav style={{ display: "grid", gap: 8, alignContent: "start" }}>
        {contacts.map((contact) => (
          <button
            key={contact.id}
            onClick={() => setSelected(contact)}
            aria-pressed={contact.id === selected.id}
          >
            {contact.name}
          </button>
        ))}
      </nav>
      <Chat key={selected.id} contact={selected} />
    </main>
  );
}
"""
                ),
            ),
        ),
        # ------------------------------------------------------------------
        LessonSpec(
            title="Error boundary: алдааг хашиж барих",
            slug="error-boundary",
            description="Render-ийн алдааг барьж бүх апп унахаас сэргийлэх, fallback UI, дахин эхлүүлэх.",
            duration=1080,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Render-ийн алдаа яагаад бүх апп-ыг хоосон дэлгэц болгодгийг ойлгох
- Class component-оор error boundary бичих
- Fallback UI харуулах, алдааг бүртгэх (log)
- Boundary-г дахин эхлүүлэх (reset)

### Яагаад чухал вэ

Render хийх үед барьж аваагүй алдаа гарвал React **бүх** модыг устгадаг —
хэрэглэгч хоосон цагаан хуудас харна. Буруу үнэтэй сагс гэх мэт эвдэрсэн
UI харуулснаас хоосон дэлгэц дээр гэж React үздэг. Гэвч нэг барааны
өгөгдөл дутуу ирснээс болж бүх дэлгүүр унах ёсгүй. Error boundary нь
алдааг тухайн хэсэгт нь хашиж, бусдыг хэвийн ажиллуулна.

### Error boundary бичих

Одоогоор hook-оор бичих арга байхгүй — class component хэрэгтэй. Энэ
сургалтад class бичих цорын ганц газар:

```jsx
import { Component } from "react";

class ErrorBoundary extends Component {
  state = { hasError: false };

  // 1. Доорх component алдаа шидмэгц state-ийг шинэчилнэ → fallback харагдана
  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  // 2. Алдааг бүртгэнэ — бодит апп-д Sentry гэх мэт үйлчилгээ рүү илгээнэ
  componentDidCatch(error, info) {
    console.error("Барьсан алдаа:", error.message, info.componentStack);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback;
    }
    return this.props.children;
  }
}
```

Хэрэглэх нь:

```jsx
<ErrorBoundary fallback={<p>Энэ хэсгийг харуулж чадсангүй.</p>}>
  <ProductDetails product={product} />
</ErrorBoundary>
```

`ProductDetails` (эсвэл түүний доторх аль нэг component) render хийх үед
алдаа шидвэл хамгийн ойрын boundary fallback-ийг харуулна. Boundary-гаас
гадуурх хэсэг хэвийн ажилласаар байна.

`getDerivedStateFromError` нь render алхамд ажилладаг тул цэвэр байх ёстой
— зөвхөн шинэ state буцаана. Гаж нөлөө (log илгээх) `componentDidCatch`-д.

### Юуг барьдаггүй вэ

Error boundary зөвхөн **render** болон effect-ийн үеийн алдааг барьдаг.
Барьдаггүй:

- event handler (`onClick`) доторх алдаа — `try/catch`-аар өөрөө барь;
- асинхрон код (`setTimeout`, `fetch`) — алдааг state-д хадгалж харуул;
- boundary өөр дээрээ гарсан алдаа — дээд талын boundary барина.

### Хаана тавих вэ

- Бүх апп-ыг нэг boundary-гаар ороож «Уучлаарай, алдаа гарлаа» хуудас
  харуулах — хамгийн доод хамгаалалт.
- Хуудас, томоохон виджет бүрийг тусад нь — нэг хэсэг унахад бусад нь
  ажилласаар.
- Жижиг товч, мөр бүрийг ороох нь илүүц.

### Дахин эхлүүлэх

`hasError: true` болсон boundary өөрөө буцахгүй. Хоёр арга:

1. **`key`** — өмнөх хичээлийн арга. `<ErrorBoundary key={product.id}>`
   бол өөр бараа сонгоход boundary шинээр үүсэж, алдаа арилна.
2. **«Дахин оролдох» товч** — state-ийг буцаана:

```jsx
render() {
  if (this.state.hasError) {
    return (
      <div role="alert">
        <p>Алдаа гарлаа.</p>
        <button onClick={() => this.setState({ hasError: false })}>Дахин оролдох</button>
      </div>
    );
  }
  return this.props.children;
}
```

### Бодит төсөлд

Ихэнх төсөл class бичихийн оронд `react-error-boundary` санг ашигладаг
(`npm install react-error-boundary`):

```jsx
import { ErrorBoundary } from "react-error-boundary";

<ErrorBoundary fallback={<p>Алдаа гарлаа</p>} resetKeys={[product.id]}>
  <ProductDetails product={product} />
</ErrorBoundary>
```

Next.js-д `error.jsx` файл тухайн хуудасны boundary болдог. Хөгжүүлэлтийн
үед React барьсан алдааг ч console-д бичдэг — энэ хэвийн.

```quiz
Товч дарахад `onClick` дотор алдаа шидэгдэв. Error boundary үүнийг барих уу?
- [ ] Тийм, boundary бүх алдааг барьдаг
- [x] Үгүй — event handler-ийн алдааг `try/catch`-аар өөрөө барина
> Boundary нь render (ба effect)-ийн үеийн алдааг л барина. Event handler render-ээс гадна ажилладаг.
```

```quiz
`getDerivedStateFromError`, `componentDidCatch` хоёрын ялгаа юу вэ?
- [x] Эхнийх нь fallback харуулах state буцаана, хоёр дахь нь алдааг бүртгэх газар
- [ ] Эхнийх нь алдааг бүртгэнэ, хоёр дахь нь fallback-ийг render хийнэ
- [ ] Ялгаагүй, аль нэгийг нь бичихэд хангалттай
> `getDerivedStateFromError` render алхамд ажилладаг тул цэвэр байх ёстой. Гаж нөлөө `componentDidCatch`-д.
```

### Дүгнэлт

Error boundary нь хүүхэд component-уудын render-ийн алдааг барьж, fallback
харуулна — апп бүхэлдээ унахгүй. Class-аар (`getDerivedStateFromError`,
`componentDidCatch`) эсвэл `react-error-boundary`-аар бичнэ. `key` эсвэл
state буцаах товчоор дахин эхлүүлнэ.
""",
            initial_code=vite(
                """\
import { useState } from "react";
import ErrorBoundary from "./ErrorBoundary";
import { products } from "./data";

function ProductDetails({ product }) {
  return (
    <section>
      <h2>
        {product.emoji} {product.name}
      </h2>
      <p>Үнэ: {product.price}₮</p>
      <p>Илчлэг: {product.nutrition.calories} ккал</p>
    </section>
  );
}

export default function App() {
  const [selectedId, setSelectedId] = useState(null);
  const selected = products.find((product) => product.id === selectedId);

  return (
    <main>
      <h1>Бараанууд</h1>
      <nav style={{ display: "flex", gap: 8 }}>
        {products.map((product) => (
          <button key={product.id} onClick={() => setSelectedId(product.id)}>
            {product.emoji} {product.name}
          </button>
        ))}
      </nav>
      {/* TODO: ProductDetails-ийг ErrorBoundary-гаар ороо */}
      {selected && <ProductDetails product={selected} />}
    </main>
  );
}
""",
                extra={
                    "ErrorBoundary.jsx": """\
import { Component } from "react";

export default class ErrorBoundary extends Component {
  // TODO 1: state = { hasError: false }

  // TODO 2: static getDerivedStateFromError() — { hasError: true } буцаа

  // TODO 3: componentDidCatch(error) — console.error-оор алдааг бүртгэ

  render() {
    // TODO 4: алдаа гарсан бол this.props.fallback-ийг буцаа
    return this.props.children;
  }
}
"""
                },
                locked={
                    "data.js": """\
export const products = [
  { id: 1, name: "Алим", emoji: "🍎", price: 2800, nutrition: { calories: 52 } },
  // Серверээс nutrition ирээгүй — эвдэрсэн өгөгдөл
  { id: 2, name: "Брокколи", emoji: "🥦", price: 5200 },
  { id: 3, name: "Банана", emoji: "🍌", price: 3500, nutrition: { calories: 89 } },
];
"""
                },
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐⭐ · 15 минут

«Хөтөч» дээр «🥦 Брокколи»-г дарж үз — өгөгдөл нь дутуу тул бүх апп унана.
`ErrorBoundary.jsx`-ийг гүйцээгээд `App.jsx`-д барааны дэлгэрэнгүйг
түүгээр ороо. Алдаа гарвал «Энэ барааны мэдээллийг харуулж чадсангүй.»
гэсэн fallback харагдаж, өөр бараа сонгоход boundary дахин эхлэх ёстой.
""",
                tests=(
                    test(
                        "ErrorBoundary нь хүүхдийн алдааг барьж fallback-ийг харуулна",
                        """
const ErrorBoundary = mod("./ErrorBoundary").default;
function Broken() {
  throw new Error("Туршилтын алдаа");
}
render(
  <ErrorBoundary fallback={<p>Нөөц UI</p>}>
    <Broken />
  </ErrorBoundary>,
);
expect(screen.getByText("Нөөц UI")).toBeInTheDocument();
""",
                    ),
                    test(
                        "Алдаагүй үед хүүхдүүдээ хэвийн харуулна",
                        """
const ErrorBoundary = mod("./ErrorBoundary").default;
render(
  <ErrorBoundary fallback={<p>Нөөц UI</p>}>
    <p>Бүх зүйл хэвийн</p>
  </ErrorBoundary>,
);
expect(screen.getByText("Бүх зүйл хэвийн")).toBeInTheDocument();
expect(screen.queryByText("Нөөц UI")).toBeNull();
""",
                    ),
                    test(
                        "Эвдэрсэн бараа сонгоход fallback гарч, бусад хэсэг ажилласаар байна",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: /Брокколи/ }));
expect(screen.getByText(/харуулж чадсангүй/i)).toBeInTheDocument();
expect(screen.getByRole("heading", { name: "Бараанууд" })).toBeInTheDocument();
expect(screen.getByRole("button", { name: /Алим/ })).toBeInTheDocument();
""",
                    ),
                    test(
                        "Өөр бараа сонгоход fallback арилж, тухайн барааны мэдээлэл харагдана",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: /Брокколи/ }));
await user.click(screen.getByRole("button", { name: /Алим/ }));
expect(screen.queryByText(/харуулж чадсангүй/i)).toBeNull();
expect(screen.getByText(/52 ккал/)).toBeInTheDocument();
""",
                    ),
                ),
                tips="""\
- `static getDerivedStateFromError()` нь `static` түлхүүр үгтэй, шинэ state-ийн
  объект буцаана. `this` ашиглахгүй.
- `render()` дотор `this.state.hasError`-оор fallback эсвэл
  `this.props.children`-ийн аль нэгийг буцаа.
- `App.jsx`-д `<ErrorBoundary fallback={…}>`-ийг `{selected && …}`-ийн эргэн
  тойронд тавь. Жагсаалтыг (товчнуудыг) дотор нь бүү хий — тэд ажилласаар
  байх ёстой.
- Нэг удаа алдаа барьсан boundary өөрөө буцахгүй. Өмнөх хичээлийн аргыг
  санаарай: сонгосон барааны `id`-г boundary-ийн `key` болговол бараа
  солигдох бүрт boundary шинээр эхэлнэ.
""",
                solution=solution(
                    App_jsx="""\
import { useState } from "react";
import ErrorBoundary from "./ErrorBoundary";
import { products } from "./data";

function ProductDetails({ product }) {
  return (
    <section>
      <h2>
        {product.emoji} {product.name}
      </h2>
      <p>Үнэ: {product.price}₮</p>
      <p>Илчлэг: {product.nutrition.calories} ккал</p>
    </section>
  );
}

export default function App() {
  const [selectedId, setSelectedId] = useState(null);
  const selected = products.find((product) => product.id === selectedId);

  return (
    <main>
      <h1>Бараанууд</h1>
      <nav style={{ display: "flex", gap: 8 }}>
        {products.map((product) => (
          <button key={product.id} onClick={() => setSelectedId(product.id)}>
            {product.emoji} {product.name}
          </button>
        ))}
      </nav>
      <ErrorBoundary
        key={selectedId}
        fallback={<p role="alert">Энэ барааны мэдээллийг харуулж чадсангүй.</p>}
      >
        {selected && <ProductDetails product={selected} />}
      </ErrorBoundary>
    </main>
  );
}
""",
                    ErrorBoundary_jsx="""\
import { Component } from "react";

export default class ErrorBoundary extends Component {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error) {
    console.error("ErrorBoundary барьлаа:", error.message);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback;
    }
    return this.props.children;
  }
}
""",
                ),
            ),
        ),
        # ------------------------------------------------------------------
        LessonSpec(
            title="lazy ба Suspense: хэрэгтэй үед нь ачаалах",
            slug="lazy-suspense",
            description="Component-ийг тусдаа хэсэг болгон хэрэгтэй үед нь ачаалж, Suspense-ээр ачааллыг харуулах.",
            duration=960,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Code splitting гэж юу болохыг ойлгох
- `lazy()` ба dynamic `import()`-оор component-ийг хойшлуулан ачаалах
- `<Suspense fallback>`-оор ачааллын төлөв харуулах
- `lazy`-ийн түгээмэл алдаанаас зайлсхийх

### Яагаад чухал вэ

Vite апп-ыг build хийхэд бүх код нэг том JavaScript файл болдог. Хэрэглэгч
нүүр хуудсыг үзэхийн тулд админ самбар, график, тайлангийн кодыг ч татна.
Удаан интернеттэй утсан дээр энэ нь хэдэн секундын хоцрол. **Code
splitting** нь кодыг хэсгүүдэд (chunk) хувааж, тухайн хэсэг хэрэгтэй болох
үед л татна.

### Dynamic import

`import` хоёр янз бичигддэг:

```jsx
import Reports from "./Reports";          // статик — апп эхлэхэд ачаалагдана
const module = await import("./Reports"); // dynamic — дуудах үед, Promise буцаана
```

Vite dynamic `import()`-ийг хараад тэр файлыг тусдаа chunk болгодог.

### lazy

```jsx
import { lazy, Suspense } from "react";

const Reports = lazy(() => import("./Reports"));
```

- `lazy` нь Promise буцаадаг функц авна. React `<Reports />`-ийг **анх
  render хийх үед** л функцийг дуудаж, файлыг татна.
- Файл нь **default export** хийсэн байх ёстой.
- `lazy`-г файлын дээд түвшинд, import-уудын доор зарла. Component дотор
  зарлавал render бүрт шинэ component үүсч, state нь байнга устна (өмнөх
  хичээлийн дүрэм).

### Suspense

Ачаалж байх хооронд юу харуулахыг `Suspense` заана:

```jsx
<Suspense fallback={<p>Ачаалж байна…</p>}>
  {page === "reports" && <Reports />}
</Suspense>
```

Доторх аль нэг component бэлэн биш байвал (**suspend** хийвэл) React
хамгийн ойрын `Suspense`-ийн `fallback`-ийг харуулна. Файл нэг удаа
ачаалагдсан бол дахин татахгүй — дараагийн удаа шууд харагдана.

Suspense нь зөвхөн `lazy`-д зориулагдаагүй: Модул 11-ийн `use()`, TanStack
Query-ийн `useSuspenseQuery` зэрэг өгөгдөл ачаалахад ч ажиллана.

### Хаана хэрэглэх вэ

Хамгийн түгээмэл нь route бүрийг lazy болгох — хэрэглэгч тухайн хуудас
руу орох үед л кодыг нь татна:

```jsx
const AdminPage = lazy(() => import("./pages/AdminPage"));

<Suspense fallback={<Spinner />}>
  <Routes>
    <Route path="/admin" element={<AdminPage />} />
  </Routes>
</Suspense>
```

Мөн цонх (modal), график, текст засварлагч гэх мэт том, заримдаа л
хэрэгтэй хэсэгт тохирно. Жижиг товч, картыг lazy болгох нь илүүц —
хүсэлтийн тоо нэмэгдэхээс өөр ашиггүй.

Сүлжээ тасарвал `import()` алдаа шиднэ. Тиймээс lazy хэсгийг өмнөх
хичээлийн error boundary-гаар ороох нь зөв.

### Энэ sandbox-д

Файлууд санах ойд байгаа тул `import()` шууд биелж, fallback харагдахгүй
өнгөрнө. Сүлжээг дуурайхын тулд 🔒 `network.js`-ийн `slow()` функцийг
ашиглана:

```jsx
const Reports = lazy(() => slow(import("./Reports")));
```

Бодит төсөлд `slow` бичихгүй. Chrome DevTools-ийн Network tab-аас
хуудас солих үед шинэ `.js` файл татагдаж байгааг харж болно.

```quiz
Доорх кодын алдааг ол: `function App() { const Chart = lazy(() => import("./Chart")); return <Chart />; }`
- [ ] `import("./Chart")` буруу бичигдсэн
- [x] `lazy`-г component дотор зарласан — render бүрт шинэ component үүснэ
- [ ] `lazy`-д async функц өгөх ёстой
> `lazy`-г файлын дээд түвшинд зарлана. Мөн `Suspense` дутуу байна.
```

```quiz
`Reports.jsx` нь `export function Reports()` гэж нэртэй export хийсэн. `lazy(() => import("./Reports"))` ажиллах уу?
- [ ] Тийм
- [x] Үгүй — `lazy` default export хүлээдэг
> Нэртэй export-ыг `import("./Reports").then((m) => ({ default: m.Reports }))` гэж хөрвүүлж болно.
```

### Дүгнэлт

`lazy(() => import("./X"))` нь component-ийн кодыг анх хэрэгтэй болох үед
татна. `Suspense` ачаалж байх хооронд fallback харуулна. `lazy`-г файлын
дээд түвшинд зарлаж, ихэвчлэн route, том виджетэд хэрэглэнэ.
""",
            initial_code=vite(
                """\
import { useState } from "react";
import { slow } from "./network";
import Reports from "./Reports";

// TODO: Reports-ийг lazy болго: lazy(() => slow(import("./Reports")))

export default function App() {
  const [page, setPage] = useState("home");

  return (
    <main>
      <nav style={{ display: "flex", gap: 8 }}>
        <button onClick={() => setPage("home")}>Нүүр</button>
        <button onClick={() => setPage("reports")}>Тайлан</button>
      </nav>
      {page === "home" && (
        <section>
          <h1>Нүүр</h1>
          <p>Өнөөдрийн захиалга: 12</p>
        </section>
      )}
      {/* TODO: Suspense-ээр ороож, «Тайлан ачаалж байна…» fallback харуул */}
      {page === "reports" && <Reports />}
    </main>
  );
}
""",
                locked={
                    "Reports.jsx": """\
console.log("📦 Reports.jsx ачаалагдлаа");

const months = [
  { name: "7-р сар", sales: 42 },
  { name: "8-р сар", sales: 58 },
  { name: "9-р сар", sales: 71 },
];

export default function Reports() {
  return (
    <section>
      <h1>Тайлан</h1>
      {months.map((month) => (
        <p key={month.name}>
          {month.name}: {"█".repeat(Math.round(month.sales / 5))} {month.sales}
        </p>
      ))}
    </section>
  );
}
""",
                    "network.js": NETWORK_JS,
                },
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐ · 10 минут

«Тайлан» хуудас том тул апп эхлэхэд ачаалах шаардлагагүй. Одоо `App.jsx`
үүнийг статикаар импортолж байгаа тул Console-д «📦 Reports.jsx
ачаалагдлаа» шууд гарна. `Reports`-ийг `lazy` болгож (`slow()`-оор ороож),
ачаалах хооронд «Тайлан ачаалж байна…» гэсэн fallback-тай `Suspense` нэм.
""",
                tests=(
                    test(
                        "Апп эхлэхэд Reports.jsx ачаалагдахгүй",
                        """
render(<App />);
expect(screen.getByRole("heading", { name: "Нүүр" })).toBeInTheDocument();
expect(logs.some((entry) => entry.text.includes("Reports.jsx"))).toBe(false);
""",
                    ),
                    test(
                        "«Тайлан» дарахад эхлээд «Тайлан ачаалж байна…» харагдана",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: "Тайлан" }));
expect(screen.getByText(/ачаалж байна/i)).toBeInTheDocument();
""",
                    ),
                    test(
                        "Ачаалж дуусахад тайлангийн хуудас гарч ирнэ",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: "Тайлан" }));
expect(await screen.findByRole("heading", { name: "Тайлан" })).toBeInTheDocument();
expect(screen.queryByText(/ачаалж байна/i)).toBeNull();
expect(logs.some((entry) => entry.text.includes("Reports.jsx"))).toBe(true);
""",
                    ),
                ),
                tips="""\
- `import Reports from "./Reports";` мөрийг устга — статик импорт үлдвэл
  файл эхлэхэд л ачаалагдана.
- `import { lazy, Suspense, useState } from "react";`
- `const Reports = lazy(() => slow(import("./Reports")));` — файлын дээд
  түвшинд, component-ийн гадна.
- `Suspense`-ийг `{page === "reports" && <Reports />}`-ийн эргэн тойронд тавиад
  `fallback={<p>Тайлан ачаалж байна…</p>}` өг.
""",
                solution=solution(
                    App_jsx="""\
import { lazy, Suspense, useState } from "react";
import { slow } from "./network";

const Reports = lazy(() => slow(import("./Reports")));

export default function App() {
  const [page, setPage] = useState("home");

  return (
    <main>
      <nav style={{ display: "flex", gap: 8 }}>
        <button onClick={() => setPage("home")}>Нүүр</button>
        <button onClick={() => setPage("reports")}>Тайлан</button>
      </nav>
      {page === "home" && (
        <section>
          <h1>Нүүр</h1>
          <p>Өнөөдрийн захиалга: 12</p>
        </section>
      )}
      <Suspense fallback={<p>Тайлан ачаалж байна…</p>}>
        {page === "reports" && <Reports />}
      </Suspense>
    </main>
  );
}
"""
                ),
            ),
        ),
        # ------------------------------------------------------------------
        LessonSpec(
            title="useTransition: яаралгүй шинэчлэлт",
            slug="usetransition",
            description="Шинэчлэлтийг transition болгож UI-г хариу үйлдэлтэй байлгах, isPending-ээр төлөв харуулах.",
            duration=1080,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Яаралтай ба яаралгүй шинэчлэлтийг ялгах
- `useTransition`-ээр шинэчлэлтийг transition болгох
- `isPending`-ээр «шилжиж байна» төлөв харуулах
- Transition нь Suspense-ийн fallback-аас хэрхэн сэргийлдгийг ойлгох

### Яагаад чухал вэ

Таб дарахад шинэ таб удаан render хийгддэг бол хуудас бүхэлдээ хөлдөнө —
өөр таб дарах, бичих боломжгүй. Эсвэл таб бүр lazy бол таб солих бүрт
одоогийн агуулга алга болж «Ачаалж байна…» анивчина. Хоёулаа муу
туршлага.

### Яаралтай ба яаралгүй

- **Яаралтай** (urgent): бичих, дарах, сонгох. Хэрэглэгч шууд хариу
  хүлээдэг — оролтын талбар 100 мс хоцорвол «эвдэрсэн» мэт санагдана.
- **Яаралгүй** (transition): нэг дэлгэцээс нөгөөд шилжих. Хэдэн зуун мс
  хүлээж болно, гэхдээ одоогийн дэлгэц хөлдөх ёсгүй.

Анхдагчаар бүх шинэчлэлт яаралтай. `useTransition` нь «энэ шинэчлэлт
яаралгүй» гэж React-д хэлнэ:

```jsx
import { useState, useTransition } from "react";

function TabContainer() {
  const [isPending, startTransition] = useTransition();
  const [tab, setTab] = useState("about");

  function selectTab(nextTab) {
    startTransition(() => {
      setTab(nextTab);
    });
  }
  // ...
}
```

### Юу өөрчлөгдөх вэ

1. **Render тасалдаж болно.** React transition-ийг хэсэг хэсгээр render
   хийж, хооронд нь хөтөчид амсхийх боломж өгнө. Энэ үед хэрэглэгч өөр
   таб дарвал React хуучин render-ийг хаяж, шинийг эхлүүлнэ. Ийм render-ийг
   **concurrent rendering** гэдэг.
2. **Хуучин UI үлдэнэ.** Transition-ы үед component suspend хийвэл (lazy,
   өгөгдөл) React аль хэдийн харагдаж буй агуулгыг fallback-аар солихгүй,
   шинэ дэлгэц бэлэн болтол хуучнаа үлдээнэ.
3. **`isPending`** — transition дуусаагүй байх хооронд `true`. Хэрэглэгчид
   «ажиллаж байна» гэж мэдэгдэнэ:

```jsx
<nav style={{ opacity: isPending ? 0.6 : 1 }}>…</nav>
{isPending && <p>Шилжиж байна…</p>}
```

### Удаан render

```jsx
function SlowItem({ index }) {
  const start = performance.now();
  while (performance.now() - start < 1) {
    // 1 мс «ажил»
  }
  return <li>Бараа №{index + 1}</li>;
}
```

250 ийм мөртэй таб яаралтай шинэчлэлтээр хуудсыг ¼ секунд хөлдөөнө.
Transition-оор бол React мөр бүрийн хооронд завсарлаж, хөтөч хариу
үйлдэлтэй хэвээр байна. Эхлэл кодын «Бүх бараа» табыг дараад шууд
«Тухай»-г дарж үз — засахаас өмнө ба дараа нь харьцуул.

### Анхаарах зүйлс

- Оролтын талбарын утгыг (`<input value>`) transition болгож болохгүй —
  бичих нь үргэлж яаралтай. Үүнд дараагийн хичээлийн `useDeferredValue`
  тохирно.
- React 19-д `startTransition`-д async функц өгч болно (**Action**). Энэ
  үед `await`-ийн дараах `setState`-ийг дахин `startTransition`-оор
  ороох шаардлагатай. Дэлгэрэнгүйг Модул 11-д.
- Component-ийн гадна `import { startTransition } from "react"` ашиглаж
  болно, гэхдээ тэр `isPending` өгөхгүй.
- react-router-ийн шилжилт, олон сан дотроо transition ашигладаг.

```quiz
Таб солихыг `startTransition`-оор ороосон. Шинэ таб lazy бөгөөд ачаалж байна. Дэлгэц дээр юу харагдах вэ?
- [ ] Suspense-ийн fallback «Ачаалж байна…»
- [x] Одоогийн таб хэвээр, `isPending` нь `true`
- [ ] Хоосон дэлгэц
> Transition-ы үед React харагдаж буй агуулгыг fallback-аар солихгүй, шинэ дэлгэц бэлэн болтол хүлээнэ.
```

```quiz
Аль шинэчлэлтийг transition болгох нь зөв бэ?
- [ ] Хайлтын талбарт үсэг бичих
- [x] Табын агуулгыг солих
- [ ] Checkbox-ийг чагтлах
> Хэрэглэгчийн оролтыг шууд харуулах нь яаралтай. Дэлгэц солих нь хүлээж болох ажил.
```

### Дүгнэлт

`useTransition` нь шинэчлэлтийг яаралгүй гэж тэмдэглэнэ: render тасалдаж
болно, харагдаж буй UI fallback-аар солигдохгүй, `isPending` нь
«шилжиж байна» төлвийг өгнө. Оролтын утга үргэлж яаралтай хэвээр.
""",
            initial_code=vite(
                """\
import { lazy, Suspense, useState } from "react";
import { slow } from "./network";
import SlowList from "./SlowList";

const Reviews = lazy(() => slow(import("./Reviews")));

const tabs = [
  { id: "about", label: "Тухай" },
  { id: "products", label: "Бүх бараа" },
  { id: "reviews", label: "Сэтгэгдэл" },
];

function About() {
  return (
    <section>
      <h2>Ногоон сагс</h2>
      <p>Шинэ, эрүүл хүнсийг гэрт тань хүргэнэ.</p>
    </section>
  );
}

export default function App() {
  const [tab, setTab] = useState("about");
  // TODO 1: useTransition()-оос [isPending, startTransition]-ийг ав

  function selectTab(nextTab) {
    // TODO 2: шинэчлэлтийг startTransition дотор хий
    setTab(nextTab);
  }

  return (
    <main>
      <nav style={{ display: "flex", gap: 8 }}>
        {tabs.map((item) => (
          <button
            key={item.id}
            onClick={() => selectTab(item.id)}
            aria-pressed={tab === item.id}
          >
            {item.label}
          </button>
        ))}
      </nav>
      {/* TODO 3: isPending үед «Шилжиж байна…» гэж харуул */}
      <Suspense fallback={<p>Ачаалж байна…</p>}>
        {tab === "about" && <About />}
        {tab === "products" && <SlowList />}
        {tab === "reviews" && <Reviews />}
      </Suspense>
    </main>
  );
}
""",
                locked={
                    "SlowList.jsx": """\
function SlowItem({ index }) {
  const start = performance.now();
  while (performance.now() - start < 1) {
    // Мөр бүр 1 мс «ажиллана» — удаан component-ийг дуурайна
  }
  return <li>Бараа №{index + 1}</li>;
}

export default function SlowList() {
  const items = Array.from({ length: 250 }, (_, index) => index);
  return (
    <ul>
      {items.map((index) => (
        <SlowItem key={index} index={index} />
      ))}
    </ul>
  );
}
""",
                    "Reviews.jsx": """\
const reviews = [
  { id: 1, author: "Сараа", text: "Хүргэлт маш хурдан байлаа!" },
  { id: 2, author: "Тэмүүлэн", text: "Жимс шинэхэн, үнэ боломжийн." },
];

export default function Reviews() {
  return (
    <section>
      <h2>Сэтгэгдэл</h2>
      <ul>
        {reviews.map((review) => (
          <li key={review.id}>
            <b>{review.author}:</b> {review.text}
          </li>
        ))}
      </ul>
    </section>
  );
}
""",
                    "network.js": NETWORK_JS,
                },
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐⭐ · 12 минут

Табтай хуудас: «Тухай», «Бүх бараа» (удаан render), «Сэтгэгдэл» (lazy,
0.8 секунд ачаална). Одоо «Сэтгэгдэл» дарахад одоогийн таб алга болж
«Ачаалж байна…» гарна. Таб солихыг transition болгож, шилжиж байх үед
табуудын доор «Шилжиж байна…» гэж харуул.
""",
                tests=(
                    test(
                        "«Сэтгэгдэл» дарахад одоогийн таб харагдсаар, fallback гарахгүй",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: "Сэтгэгдэл" }));
expect(screen.queryByText(/ачаалж байна/i)).toBeNull();
expect(screen.getByRole("heading", { name: "Ногоон сагс" })).toBeInTheDocument();
""",
                    ),
                    test(
                        "Шилжиж байх үед «Шилжиж байна…» харагдана",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: "Сэтгэгдэл" }));
expect(screen.getByText(/шилжиж байна/i)).toBeInTheDocument();
""",
                    ),
                    test(
                        "Ачаалж дуусахад сэтгэгдлүүд гарч, «Шилжиж байна…» алга болно",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: "Сэтгэгдэл" }));
expect(await screen.findByRole("heading", { name: "Сэтгэгдэл" })).toBeInTheDocument();
expect(screen.queryByText(/шилжиж байна/i)).toBeNull();
""",
                    ),
                ),
                tips="""\
- `import { lazy, Suspense, useState, useTransition } from "react";`
- `const [isPending, startTransition] = useTransition();` — hook тул
  component-ийн дээд хэсэгт.
- `startTransition(() => { setTab(nextTab); });` — функц дотор `setTab`-ийг
  дууд, `startTransition(setTab(nextTab))` гэж бичвэл `setTab` шууд
  (яаралтай) ажиллана.
- «Шилжиж байна…»-г `Suspense`-ийн **гадна** тавь — дотор нь байвал
  fallback-тай хамт нуугдана.
""",
                solution=solution(
                    App_jsx="""\
import { lazy, Suspense, useState, useTransition } from "react";
import { slow } from "./network";
import SlowList from "./SlowList";

const Reviews = lazy(() => slow(import("./Reviews")));

const tabs = [
  { id: "about", label: "Тухай" },
  { id: "products", label: "Бүх бараа" },
  { id: "reviews", label: "Сэтгэгдэл" },
];

function About() {
  return (
    <section>
      <h2>Ногоон сагс</h2>
      <p>Шинэ, эрүүл хүнсийг гэрт тань хүргэнэ.</p>
    </section>
  );
}

export default function App() {
  const [tab, setTab] = useState("about");
  const [isPending, startTransition] = useTransition();

  function selectTab(nextTab) {
    startTransition(() => {
      setTab(nextTab);
    });
  }

  return (
    <main>
      <nav style={{ display: "flex", gap: 8, opacity: isPending ? 0.6 : 1 }}>
        {tabs.map((item) => (
          <button
            key={item.id}
            onClick={() => selectTab(item.id)}
            aria-pressed={tab === item.id}
          >
            {item.label}
          </button>
        ))}
      </nav>
      {isPending && <p>Шилжиж байна…</p>}
      <Suspense fallback={<p>Ачаалж байна…</p>}>
        {tab === "about" && <About />}
        {tab === "products" && <SlowList />}
        {tab === "reviews" && <Reviews />}
      </Suspense>
    </main>
  );
}
"""
                ),
            ),
        ),
        # ------------------------------------------------------------------
        LessonSpec(
            title="useDeferredValue: хойшлуулсан утга",
            slug="usedeferredvalue",
            description="Оролтыг хурдан байлгаж, удаан хэсгийг хуучин утгаар түр харуулах; хуучирсан үр дүнг тэмдэглэх.",
            duration=1020,
            language=JSX,
            content="""\
### Энэ хичээлээр

- `useDeferredValue`-ээр утгын «хоцорсон» хувилбар авах
- Шинэ үр дүн ачаалах хооронд хуучнаа харуулах
- Хуучирсан (stale) үр дүнг тэмдэглэх
- `useTransition`, debounce хоёроос ялгах

### Яагаад чухал вэ

Хайлтын талбарт үсэг бичих бүрт үр дүн шинээр ачаалагдана. Хариу
хүлээх бүрт жагсаалт алга болж «Ачаалж байна…» анивчвал, эсвэл удаан
жагсаалтаас болж бичих нь гацвал хэрэглэгч бухимдана. Өмнөх хичээлийн
`startTransition` энд тохирохгүй: талбарын утга (`setQuery`) яаралтай
байх ёстой.

### useDeferredValue

```jsx
import { useDeferredValue, useState } from "react";

function Search() {
  const [query, setQuery] = useState("");
  const deferredQuery = useDeferredValue(query);

  return (
    <>
      <input value={query} onChange={(e) => setQuery(e.target.value)} />
      <SearchResults query={deferredQuery} />
    </>
  );
}
```

Үсэг бичихэд:

1. React эхлээд **яаралтай** render хийнэ: `query` шинэ, `deferredQuery`
   хуучнаараа. Талбар шууд шинэчлэгдэж, үр дүн хуучин утгаараа үлдэнэ.
2. Дараа нь **ард** (transition шиг) `deferredQuery`-г шинэ утгаар render
   хийнэ. Энэ render тасалдаж болно: хэрэглэгч дахин үсэг бичвэл React
   үүнийг хаяж, хамгийн сүүлийн утгаар дахин эхэлнэ.
3. Ард хийх render suspend хийвэл (өгөгдөл ачаалж байвал) хэрэглэгч
   fallback биш, **хуучин үр дүнг** харна.

### Хуучирсан үр дүнг тэмдэглэх

`query !== deferredQuery` бол дэлгэц дээрх үр дүн хоцорч байна гэсэн үг:

```jsx
const isStale = query !== deferredQuery;

<div style={{ opacity: isStale ? 0.5 : 1 }}>
  {isStale && <p>Шинэчилж байна…</p>}
  <SearchResults query={deferredQuery} />
</div>
```

### Удаан render ба memo

Үр дүн өгөгдөл ачаалдаггүй, зүгээр удаан render хийдэг бол `memo` хэрэгтэй:

```jsx
const SlowList = memo(function SlowList({ text }) {
  // ... удаан render
});

<SlowList text={deferredQuery} />
```

Яаралтай render-ийн үед `deferredQuery` өөрчлөгдөөгүй тул `memo` удаан
жагсаалтыг алгасна — бичих хурдан хэвээр. `memo`-гүй бол жагсаалт
яаралтай render бүрт дахин render болж, `useDeferredValue` ашиггүй болно.
`memo`-г Модул 12-т дэлгэрэнгүй үзнэ.

### Debounce-оос юугаараа ялгаатай вэ

Debounce (жишээ нь 300 мс хүлээх) нь хурдан компьютер дээр ч заавал
хүлээлгэнэ. `useDeferredValue` тогтмол хугацаа хүлээдэггүй: хурдан төхөөрөмж
дээр бараг шууд, удаан дээр боломжоороо шинэчилнэ. Харин сервер рүү явах
хүсэлтийн тоог багасгах бол debounce хэрэгтэй хэвээр — хоёрыг хамт
хэрэглэж болно.

| | `useTransition` | `useDeferredValue` |
|---|---|---|
| Юуг хойшлуулах | state шинэчлэх **үйлдлийг** | **утгыг** |
| Хэзээ | `setState`-ийг өөрөө дууддаг бол | утга props-оор ирдэг, `setState`-д хүрэхгүй бол |
| Төлөв | `isPending` | `value !== deferredValue` |

React 19-д анхны утга өгч болно: `useDeferredValue(query, "")` — анхны
render-д `""`-ээр, дараа нь ард жинхэнэ утгаар render хийнэ.

### Энэ хичээлийн код

🔒 `SearchResults.jsx` нь дадлагын API-аас үр дүнг 0.5 секундэд ачаалж,
ачаалах хооронд suspend хийдэг. Үүнд Модул 11-д үзэх `use()` ашигласан —
одоо дотор нь юу байгааг ойлгох шаардлагагүй.

```quiz
`const deferred = useDeferredValue(query)`. Өмнө нь хоёулаа `""` байв. Хэрэглэгч «а» гэж бичсэний дараах **эхний** render-д утгууд ямар байх вэ?
- [ ] `query = ""`, `deferred = "а"`
- [x] `query = "а"`, `deferred = ""`
- [ ] Хоёулаа `"а"`
> Эхлээд яаралтай render шинэ `query`, хуучин `deferred`-ээр хийгдэнэ. Дараагийн (ард хийгдэх) render-д `deferred` шинэчлэгдэнэ.
```

```quiz
Удаан жагсаалтад `deferredQuery` дамжуулсан ч бичих гацсаар байна. Хамгийн магадлалтай шалтгаан юу вэ?
- [ ] `useDeferredValue` зөвхөн Suspense-тэй ажилладаг
- [x] Жагсаалт `memo`-гоор ороогдоогүй тул яаралтай render бүрт дахин render болж байна
- [ ] `query`-г transition-д хийх ёстой
> Яаралтай render-ийн үед жагсаалтыг алгасахын тулд `memo` хэрэгтэй.
```

### Дүгнэлт

`useDeferredValue` нь утгын хоцорсон хувилбарыг өгнө: оролт шууд
шинэчлэгдэж, удаан эсвэл ачаалж буй хэсэг хуучин утгаараа үлдэнэ.
`value !== deferredValue` үед хуучирсан үр дүнг бүдгэрүүлж тэмдэглэнэ.
""",
            initial_code=vite(
                """\
import { Suspense, useState } from "react";
import SearchResults from "./SearchResults";

export default function App() {
  const [query, setQuery] = useState("");
  // TODO 1: useDeferredValue-ээр query-ийн хойшлуулсан хувилбарыг ав

  return (
    <main>
      <h1>Барааны хайлт</h1>
      <label>
        Хайх
        <input value={query} onChange={(event) => setQuery(event.target.value)} />
      </label>
      {/* TODO 2: хуучирсан үед «Шинэчилж байна…» гэж бичиж, үр дүнг бүдгэрүүл */}
      <Suspense fallback={<p>Ачаалж байна…</p>}>
        <SearchResults query={query} />
      </Suspense>
    </main>
  );
}
""",
                locked={
                    "SearchResults.jsx": """\
import { use } from "react";

// Хайлт бүрийн Promise-ийг хадгална — нэг үгийг дахин татахгүй.
// use() нь Promise биелэх хүртэл component-ийг «хүлээлгэнэ» (suspend).
// Модул 11-д дэлгэрэнгүй үзнэ.
const cache = new Map();

function searchProducts(query) {
  if (!cache.has(query)) {
    const url = `/api/products?q=${encodeURIComponent(query)}&_delay=500`;
    cache.set(query, fetch(url).then((response) => response.json()));
  }
  return cache.get(query);
}

export default function SearchResults({ query }) {
  const products = use(searchProducts(query));
  if (products.length === 0) {
    return <p>«{query}» олдсонгүй.</p>;
  }
  return (
    <ul>
      {products.map((product) => (
        <li key={product.id}>
          {product.emoji} {product.name} — {product.price}₮
        </li>
      ))}
    </ul>
  );
}
"""
                },
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐⭐ · 12 минут

Одоо хайлтад үсэг бичих бүрт жагсаалт алга болж «Ачаалж байна…» анивчина.
`useDeferredValue` ашиглан шинэ үр дүн ачаалах хооронд хуучнаа харуулдаг
болго. Үр дүн хуучирсан үед дээр нь «Шинэчилж байна…» гэж бичиж, үр
дүнг бүдгэрүүл (`opacity: 0.5`).
""",
                tests=(
                    test(
                        "Бичих үед «Ачаалж байна…» гарахгүй, хуучин үр дүн харагдсаар байна",
                        """
await runMain();
await screen.findByText(/Банана/);
await user.type(screen.getByLabelText("Хайх"), "алим");
expect(screen.getByLabelText("Хайх")).toHaveValue("алим");
expect(screen.queryByText(/ачаалж байна/i)).toBeNull();
expect(screen.getByText(/Банана/)).toBeVisible();
""",
                    ),
                    test(
                        "Үр дүн хуучирсан үед «Шинэчилж байна…» харагдана",
                        """
await runMain();
await screen.findByText(/Банана/);
await user.type(screen.getByLabelText("Хайх"), "алим");
expect(screen.getByText(/шинэчилж байна/i)).toBeInTheDocument();
""",
                    ),
                    test(
                        "Хуучирсан үр дүн бүдэг харагдана",
                        """
await runMain();
await screen.findByText(/Банана/);
await user.type(screen.getByLabelText("Хайх"), "алим");
let element = screen.getByText(/Банана/);
let opacity = 1;
while (element) {
  opacity = opacity * Number(getComputedStyle(element).opacity);
  element = element.parentElement;
}
expect(opacity).toBeLessThan(1);
""",
                    ),
                    test(
                        "Шинэ үр дүн ирэхэд зөвхөн тохирох бараа үлдэж, «Шинэчилж байна…» алга болно",
                        """
await runMain();
await screen.findByText(/Банана/);
await user.type(screen.getByLabelText("Хайх"), "алим");
await waitFor(() => expect(screen.queryByText(/Банана/)).toBeNull());
expect(screen.getByText(/Алим/)).toBeVisible();
expect(screen.queryByText(/шинэчилж байна/i)).toBeNull();
""",
                    ),
                ),
                tips="""\
- `const deferredQuery = useDeferredValue(query);` — талбарт `query`,
  `SearchResults`-д `deferredQuery`-г өг. Хоёуланг нь `deferredQuery`
  болговол бичих удаашрахгүй ч талбар хоцорно.
- `const isStale = query !== deferredQuery;`
- «Шинэчилж байна…» ба `opacity`-г `Suspense`-ийн гаднах элементэд тавь,
  жишээ нь үр дүнг ороосон `<div style={{ opacity: isStale ? 0.5 : 1 }}>`.
""",
                solution=solution(
                    App_jsx="""\
import { Suspense, useDeferredValue, useState } from "react";
import SearchResults from "./SearchResults";

export default function App() {
  const [query, setQuery] = useState("");
  const deferredQuery = useDeferredValue(query);
  const isStale = query !== deferredQuery;

  return (
    <main>
      <h1>Барааны хайлт</h1>
      <label>
        Хайх
        <input value={query} onChange={(event) => setQuery(event.target.value)} />
      </label>
      <div style={{ opacity: isStale ? 0.5 : 1 }}>
        {isStale && <p>Шинэчилж байна…</p>}
        <Suspense fallback={<p>Ачаалж байна…</p>}>
          <SearchResults query={deferredQuery} />
        </Suspense>
      </div>
    </main>
  );
}
"""
                ),
            ),
        ),
    ],
)
