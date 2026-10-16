"""Модул 11 — Орчин үеийн React (19).

React 19-ийн шинэ боломжууд: Actions (`<form action>`, `useActionState`,
`useFormStatus`, `useOptimistic`), `use()`, Server Components ба Server
Actions-ийн ойлголт, React Compiler. Сурагч state, effect, context, серверийн
өгөгдлийг аль хэдийн мэддэг — энд тэдгээрийг бичих шинэ, богино аргыг үзнэ.

Server Components, Server Actions нь серверт ажилладаг тул sandbox-д
ажиллахгүй: тэдгээрийн кодыг Markdown-д үзүүлж, sandbox-д клиент талын
ижил санааг ажиллуулна.
"""

from app.content.react.common import HTML, MAIN, files, solution, test, vite
from app.content.types import ExerciseSpec, LessonSpec, ModuleSpec
from app.models.enums import LessonLanguage

JSX = LessonLanguage.JSX

MODERN = ModuleSpec(
    title="Модул 11 — Орчин үеийн React (19)",
    description=(
        "React 19-ийн Actions, useActionState, useFormStatus, useOptimistic, use(), "
        "Server Components, Server Actions ба React Compiler."
    ),
    lessons=[
        # ------------------------------------------------------------------
        LessonSpec(
            title="React 19-д юу шинэ вэ",
            slug="react-19-shineleg",
            description="React 19-ийн тойм: ref prop, Context provider, <title> ба ref-ийн цэвэрлэгээ.",
            duration=900,
            language=JSX,
            content="""\
### Энэ хичээлээр

- React 19-ийн гол шинэчлэлтүүдийг тоймлож, энэ модулийн замыг харах
- `<Context value>`-ийг provider болгон ашиглах
- Component дотроос `<title>`, `<meta>` render хийх
- Ref-ийг prop-оор дамжуулах, callback ref-ээс цэвэрлэгээ буцаах

### Яагаад чухал вэ

React 19 2024 оны 12-р сард гарсан бөгөөд `npm create vite@latest` одоо
шинэ төсөлд шууд React 19 суулгадаг. Гэвч интернэт дэх жишээ, сангууд,
ажлын байран дээрх код олон жил React 18-ийн хэлбэрээр бичигдсэн хэвээр
байна. Тиймээс хоёуланг нь таних хэрэгтэй: шинэ кодоо орчин үеийн
хэлбэрээр бичиж, хуучныг нь уншиж, шинэчилж чаддаг байх.

### Тойм

| Шинэчлэл | Юуг хөнгөвчлөх вэ | Хаана үзэх |
|---|---|---|
| `<form action>`, `useActionState` | Илгээх, хүлээх, алдааны төлөв | Хичээл 2 |
| `useFormStatus` | Формын төлвийг доторх component-оос мэдэх | Хичээл 3 |
| `useOptimistic` | Серверийн хариуг хүлээлгүй UI шинэчлэх | Хичээл 4 |
| `use()` | Promise, Context-ийг render дотор унших | Хичээл 5 |
| Server Components, Server Actions | Серверт ажиллах component, функц | Хичээл 6–7 |
| `ref` prop, `<Context>`, `<title>`, ref cleanup | Жижиг боловч өдөр бүр хэрэглэгдэнэ | Энэ хичээл |

React Compiler нь React 19-ийн нэг хэсэг биш, тусдаа build хэрэгсэл —
хичээл 7-д үзнэ.

### Ref — энгийн prop

Модул 6-д үзсэн: React 19-д function component `ref`-ийг бусад props-той
адил хүлээж авдаг:

```jsx
function SearchField({ label, ref }) {
  return (
    <label>
      {label} <input ref={ref} />
    </label>
  );
}
```

React 18-ийн код үүнийг `forwardRef(function SearchField(props, ref) { … })`
гэж бичдэг. Хуучин кодыг шинэчлэхдээ `forwardRef`-ийг авч хаяад `ref`-ийг
props-оос задлахад хангалттай.

### `<Context value>` — provider

React 18 хүртэл context-ийн утгыг `.Provider`-оор дамжуулдаг байлаа. React
19-д context өөрөө provider болно:

```jsx
const ThemeContext = createContext("light");

// React 18
<ThemeContext.Provider value={theme}>
  <Page />
</ThemeContext.Provider>

// React 19
<ThemeContext value={theme}>
  <Page />
</ThemeContext>
```

Хоёулаа ажиллана, гэхдээ `.Provider` ирээдүйн хувилбарт хуучирсан
(deprecated) болно. Утгыг унших тал өөрчлөгдөөгүй: `useContext(ThemeContext)`
(эсвэл хичээл 5-ын `use(ThemeContext)`).

### Document metadata: `<title>`, `<meta>`

Хөтчийн tab-ын гарчиг, хайлтын системд зориулсан тайлбар `<head>` дотор
байдаг. Харин React апп `<div id="root">` дотор ажилладаг. Өмнө нь
`useEffect`-ээр `document.title = …` гэж бичих эсвэл `react-helmet` сан
ашигладаг байв. React 19-д эдгээрийг component дотор шууд render хийхэд
React тэдгээрийг `<head>` руу зөөнө (hoist):

```jsx
function ProductPage({ product }) {
  return (
    <article>
      <title>{`${product.name} — Ногоон сагс`}</title>
      <meta name="description" content={product.description} />
      <h1>{product.name}</h1>
    </article>
  );
}
```

- Component дэлгэцээс устахад React түүний `<title>`-ийг `<head>`-ээс хасна.
- Нэг зэрэг хэд хэдэн `<title>` render хийвэл хөтөч эхнийхийг нь харуулна.
  Хуудас бүрт нэгийг тавь.
- `<title>`-ийн хүүхэд **нэг текст** байх ёстой. `<title>Сагс ({count})</title>`
  гэж бичвэл JSX үүнийг гурван хэсэгтэй массив болгодог тул гарчиг хоосон
  гарна. Template string ашигла: `` <title>{`Сагс (${count})`}</title> ``.

Энэ sandbox-д гарчиг «Хөтөч»-ийн дээд мөрөнд, хаягийн мөрийн баруун талд
харагдана (өргөн дэлгэцэнд). Next.js зэрэг framework өөрийн metadata
API-тай, харин энгийн Vite апп-д энэ арга хамгийн хялбар.

### Callback ref ба цэвэрлэгээ

`ref`-д объектын оронд функц өгч болно (**callback ref**). React элементийг
DOM-д нэмэхэд функцийг тэр элементтэй нь дуудна. React 19-д энэ функц
**цэвэрлэгээний функц** буцааж болно — элемент DOM-оос хасагдахад React
түүнийг дуудна. Яг effect-ийн цэвэрлэгээ шиг:

```jsx
function ProductCard({ product }) {
  return (
    <article
      ref={(node) => {
        const observer = new ResizeObserver(([entry]) => {
          console.log("Өргөн:", entry.contentRect.width);
        });
        observer.observe(node);
        return () => observer.disconnect(); // элемент хасагдахад
      }}
    >
      {product.name}
    </article>
  );
}
```

Өмнө нь React элемент хасагдахад функцийг `null`-оор дахин дууддаг байсан
тул `if (node) { … } else { … }` гэж бичдэг байв. Цэвэрлэгээ буцаавал React
`null`-оор дуудахаа больно. Observer, газрын зураг, график зэрэг DOM
элементтэй холбогддог сан ашиглахад тохиромжтой.

Анхаар: `ref={(node) => (inputNode = node)}` гэсэн arrow функц `node`-ийг
буцаадаг. TypeScript үүнийг алдаа гэж заана — хаалт ашигла:
`ref={(node) => { inputNode = node; }}`.

```quiz
Доорх кодын алдааг ол: `<title>Сагс ({count})</title>`
- [ ] `<title>`-ийг component дотор бичиж болохгүй
- [x] Хүүхэд нь нэг текст биш, массив болж байна — гарчиг хоосон гарна
- [ ] `count`-ийг хаалтгүй бичих ёстой
> JSX дахь `Сагс (`, `{count}`, `)` гурван тусдаа хүүхэд болно. `` {`Сагс (${count})`} `` гэж нэг текст болго.
```

```quiz
React 19-д callback ref цэвэрлэгээний функц буцаасан бол элемент DOM-оос хасагдахад юу болох вэ?
- [ ] React callback-ийг `null`-оор дуудна
- [x] React буцаасан цэвэрлэгээний функцийг дуудна
- [ ] Юу ч болохгүй — цэвэрлэгээг өөрөө дуудна
> Цэвэрлэгээ буцаавал React `null`-оор дуудахаа больж, цэвэрлэгээг дуудна — effect-тэй адил.
```

### Дүгнэлт

React 19-д `ref` бол энгийн prop, context өөрөө provider (`<ThemeContext
value>`), `<title>`, `<meta>`-г component дотроос render хийхэд `<head>`
руу очно, callback ref цэвэрлэгээ буцааж болно. Дараагийн хичээлээс
хамгийн том шинэчлэл болох Actions-ийг үзнэ.
""",
            initial_code=vite(
                """\
import { createContext, useContext, useRef, useState } from "react";
import SearchField from "./SearchField";
import { products } from "./data";

const ThemeContext = createContext("light");

function Header({ count }) {
  const theme = useContext(ThemeContext);
  return (
    <header>
      <h1>🛒 Ногоон сагс</h1>
      <p>
        Горим: {theme === "dark" ? "харанхуй" : "гэгээлэг"} · Сагсанд: {count}
      </p>
    </header>
  );
}

export default function App() {
  const [theme, setTheme] = useState("light");
  const [cart, setCart] = useState([]);
  const searchRef = useRef(null);

  // TODO 1: хөтчийн гарчиг «Сагс (N) — Ногоон сагс» байх ёстой (<title>)
  // TODO 2: theme-ийг ThemeContext-оор доош дамжуул (React 19 хэлбэрээр)
  return (
    <main
      style={{
        padding: 16,
        background: theme === "dark" ? "#1f2937" : "#ffffff",
        color: theme === "dark" ? "#f9fafb" : "#111827",
      }}
    >
      <Header count={cart.length} />
      <button onClick={() => setTheme(theme === "light" ? "dark" : "light")}>
        Горим солих
      </button>{" "}
      <SearchField label="Хайх" ref={searchRef} />{" "}
      <button onClick={() => searchRef.current?.focus()}>🔍 Хайлт руу</button>
      <ul>
        {products.map((product) => (
          <li key={product.id}>
            {product.emoji} {product.name} — {product.price}₮{" "}
            <button onClick={() => setCart([...cart, product.id])}>Нэмэх</button>
          </li>
        ))}
      </ul>
    </main>
  );
}
""",
                extra={
                    "SearchField.jsx": """\
// TODO 3: ref-ийг prop болгон авч <input>-д холбо
export default function SearchField({ label }) {
  return (
    <label>
      {label} <input type="search" placeholder="Бараа хайх…" />
    </label>
  );
}
"""
                },
                locked={
                    "data.js": """\
export const products = [
  { id: 1, name: "Банана", price: 3500, emoji: "🍌" },
  { id: 2, name: "Алим", price: 2800, emoji: "🍎" },
  { id: 3, name: "Сүү", price: 3200, emoji: "🥛" },
];
"""
                },
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 10 минут

«Ногоон сагс»-ын нүүр хуудсыг React 19-ийн боломжуудаар гүйцээ. Хөтчийн
гарчиг сагсан дахь барааны тоог харуулдаг байх ёстой (жишээ нь «Сагс (2) —
Ногоон сагс»). «Горим солих» дарахад `Header` context-оос шинэ горимыг
уншдаг, «🔍 Хайлт руу» товч `SearchField` доторх талбарт фокус өгдөг болго.
""",
                tests=(
                    test(
                        "Хөтчийн гарчиг «Сагс (0) — Ногоон сагс» байна",
                        """
render(<App />);
expect(document.title).toContain("Сагс (0)");
expect(document.title).toContain("Ногоон сагс");
""",
                    ),
                    test(
                        "Бараа нэмэхэд гарчиг дахь тоо шинэчлэгдэнэ",
                        """
render(<App />);
const buttons = screen.getAllByRole("button", { name: "Нэмэх" });
await user.click(buttons[0]);
await user.click(buttons[1]);
expect(document.title).toContain("Сагс (2)");
""",
                    ),
                    test(
                        "Горим солиход Header «харанхуй» гэж харуулна",
                        """
render(<App />);
expect(screen.getByRole("banner")).toHaveTextContent("Горим: гэгээлэг");
await user.click(screen.getByRole("button", { name: "Горим солих" }));
expect(screen.getByRole("banner")).toHaveTextContent("Горим: харанхуй");
""",
                    ),
                    test(
                        "«Хайлт руу» товч хайлтын талбарт фокус өгнө",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: /Хайлт руу/ }));
expect(screen.getByLabelText("Хайх")).toHaveFocus();
""",
                    ),
                ),
                tips="""\
- `<title>`-ийг `App`-ийн JSX-ийн аль ч хэсэгт бичиж болно — React түүнийг
  `<head>` руу зөөнө. Хүүхэд нь нэг текст байх ёстой тул template string
  ашигла: `` {`Сагс (${cart.length}) — Ногоон сагс`} ``.
- Горим солиход `main`-ийн өнгө өөрчлөгдөж байгаа ч `Header` context-оос
  уншдаг. Provider байхгүй бол context анхны утгаа (`"light"`) буцаана.
  Бүх JSX-ийг `<ThemeContext value={theme}>`-ээр ороо — `.Provider` хэрэггүй.
- `SearchField`-ийн параметрт `ref`-ийг `label`-тэй хамт задлаад
  `<input ref={ref} … />` болго. `forwardRef` React 19-д шаардлагагүй.
""",
                solution=solution(
                    App_jsx="""\
import { createContext, useContext, useRef, useState } from "react";
import SearchField from "./SearchField";
import { products } from "./data";

const ThemeContext = createContext("light");

function Header({ count }) {
  const theme = useContext(ThemeContext);
  return (
    <header>
      <h1>🛒 Ногоон сагс</h1>
      <p>
        Горим: {theme === "dark" ? "харанхуй" : "гэгээлэг"} · Сагсанд: {count}
      </p>
    </header>
  );
}

export default function App() {
  const [theme, setTheme] = useState("light");
  const [cart, setCart] = useState([]);
  const searchRef = useRef(null);

  return (
    <ThemeContext value={theme}>
      <main
        style={{
          padding: 16,
          background: theme === "dark" ? "#1f2937" : "#ffffff",
          color: theme === "dark" ? "#f9fafb" : "#111827",
        }}
      >
        <title>{`Сагс (${cart.length}) — Ногоон сагс`}</title>
        <Header count={cart.length} />
        <button onClick={() => setTheme(theme === "light" ? "dark" : "light")}>
          Горим солих
        </button>{" "}
        <SearchField label="Хайх" ref={searchRef} />{" "}
        <button onClick={() => searchRef.current?.focus()}>🔍 Хайлт руу</button>
        <ul>
          {products.map((product) => (
            <li key={product.id}>
              {product.emoji} {product.name} — {product.price}₮{" "}
              <button onClick={() => setCart([...cart, product.id])}>Нэмэх</button>
            </li>
          ))}
        </ul>
      </main>
    </ThemeContext>
  );
}
""",
                    SearchField_jsx="""\
export default function SearchField({ label, ref }) {
  return (
    <label>
      {label} <input ref={ref} type="search" placeholder="Бараа хайх…" />
    </label>
  );
}
""",
                ),
            ),
        ),
        # ------------------------------------------------------------------
        LessonSpec(
            title="Form action ба useActionState",
            slug="form-action",
            description="<form action={fn}>, FormData ба useActionState-ээр илгээх, хүлээх, алдааны төлвийг удирдах.",
            duration=1080,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Action гэж юу болохыг ойлгох, `startTransition`-д async функц өгөх
- `<form action={fn}>` ба `FormData`-аар талбаруудын утгыг унших
- `useActionState`-ээр үр дүн, алдаа, `isPending`-ийг удирдах
- Action-ийн түгээмэл алдаанаас зайлсхийх

### Яагаад чухал вэ

Модул 4-д форм илгээхдээ бараг ижил кодыг форм бүрт давтсан:

```jsx
const [email, setEmail] = useState("");
const [error, setError] = useState(null);
const [isPending, setIsPending] = useState(false);

async function handleSubmit(event) {
  event.preventDefault();
  setIsPending(true);
  try {
    await subscribe(email);
    setEmail("");
  } catch (err) {
    setError(err.message);
  } finally {
    setIsPending(false);
  }
}
```

`finally`-г мартвал товч үүрд идэвхгүй хоцорно, `preventDefault`-ийг
мартвал хуудас дахин ачаалагдана. React 19-ийн **Actions** энэ ажлын
ихэнхийг өөрөө хийнэ.

### Action гэж юу вэ

Transition дотор ажилладаг функцийг **Action** гэнэ. Модул 10-д
`startTransition`-д энгийн функц өгсөн. React 19-д async функц өгч болно:

```jsx
const [isPending, startTransition] = useTransition();

function handleSave() {
  startTransition(async () => {
    const saved = await saveQuantity(quantity);
    startTransition(() => {
      setQuantity(saved);
    });
  });
}
```

`isPending` нь async функц бүрэн дуустал `true` байна. Модул 10-д
дурдсан анхааруулга: `await`-ийн **дараах** `setState` автоматаар
transition-д орохгүй — React одоогоор `await`-ийн дараа контекстоо
алддаг. Тийм шинэчлэлтийг transition болгох бол дахин
`startTransition(() => …)`-оор ороо.

### `<form action={fn}>`

Формын `action` prop-д функц өгвөл React:

1. `preventDefault`-ийг өөрөө дуудна;
2. функцийг Action болгон дуудаж, формын бүх утгыг `FormData` объектоор
   өгнө;
3. функц дуусахад controlled бус талбаруудыг цэвэрлэнэ (reset).

```jsx
async function subscribe(formData) {
  const email = formData.get("email");
  await saveEmail(email);
}

<form action={subscribe}>
  <input name="email" type="email" />
  <button>Бүртгүүлэх</button>
</form>
```

Талбар бүр `name`-тэй байх ёстой — `FormData` утгуудыг нэрээр нь
цуглуулна. `value`, `onChange`, талбар бүрийн state хэрэггүй: талбарууд
uncontrolled (Модул 4).

```jsx
formData.get("email");         // "bat@example.mn" — үргэлж текст
Number(formData.get("qty"));   // тоо хэрэгтэй бол хөрвүүлнэ
formData.get("agree");         // checkbox: "on" эсвэл null
formData.getAll("tags");       // ижил нэртэй олон талбар → массив
Object.fromEntries(formData);  // { email: "…", qty: "2" }
```

### useActionState

`<form action>` дангаараа үр дүнг (алдаа, амжилт) харуулах арга өгдөггүй.
`useActionState` action-ийг ороож, түүний **буцаасан утгыг** state болгоно:

```jsx
import { useActionState } from "react";

async function subscribe(previousState, formData) {
  const email = formData.get("email");
  if (!email.includes("@")) {
    return { error: "Имэйл буруу байна." };
  }
  await saveEmail(email);
  return { error: null, done: true };
}

function Newsletter() {
  const [state, formAction, isPending] = useActionState(subscribe, { error: null });

  return (
    <form action={formAction}>
      <input name="email" />
      <button disabled={isPending}>
        {isPending ? "Илгээж байна…" : "Бүртгүүлэх"}
      </button>
      {state.error && <p role="alert">{state.error}</p>}
      {state.done && <p>Баярлалаа!</p>}
    </form>
  );
}
```

- `state` — action-ийн сүүлд буцаасан утга (эхэндээ `initialState`).
- `formAction` — `<form action>`-д өгөх шинэ функц.
- `isPending` — action ажиллаж байх үед `true`.
- Action-ийн **эхний** параметр нь өмнөх state, `formData` хоёр дахь нь.
- Товчийг хэд дарвал action-ууд дараалж, нэг нэгээр ажиллана.

Хуучин нийтлэлд `react-dom`-ийн `useFormState` таарч магадгүй — энэ нь
`useActionState`-ийн өмнөх нэр.

### Алдаа ба reset

- **Хүлээгдэж буй алдаа** (буруу имэйл, серверийн 500): action дотор
  шалгаж, `try/catch`-аар барьж, state болгон буцаа.
- Барьж аваагүй `throw` хамгийн ойрын error boundary руу очно (Модул 10).
  Boundary байхгүй бол бүх апп унана.
- Action дууссаны дараа React формыг цэвэрлэнэ — алдаа буцаасан ч гэсэн.
  Бичсэнийг нь үлдээх бол утгыг state-д буцааж `defaultValue`-д өг:

```jsx
return { error: "Сэтгэгдэл хэт богино байна.", message };
// ...
<textarea name="message" defaultValue={state.message} />
```

Хичээл 7-д үзэх Next.js-ийн Server Actions яг энэ `<form action>`,
`useActionState`-ээр ажилладаг. Бичих явцад шалгалт хийдэг том форм бол
React Hook Form (`npm install react-hook-form`) зэрэг сан түгээмэл.

```quiz
Доорх кодын алдааг ол: `async function save(formData) { const name = formData.get("name"); … }` ба `useActionState(save, null)`
- [ ] `useActionState`-д async функц өгч болохгүй
- [x] Эхний параметр нь өмнөх state — `formData.get` гэж дуудахад алдаа гарна
- [ ] `formData.get` нь Promise буцаадаг тул `await` хэрэгтэй
> `useActionState`-ийн action `(previousState, formData)` гэж дуудагдана. Эхний параметрийг алгасахгүй.
```

```quiz
Action «Имэйл буруу байна.» гэсэн алдааг state болгон буцаав. Талбар `defaultValue`-гүй. Хэрэглэгчийн бичсэн имэйлд юу болох вэ?
- [ ] Хэвээр үлдэнэ
- [x] Талбар хоосорно — action дууссаны дараа React формыг цэвэрлэдэг
- [ ] React алдаа заана
> Reset нь алдаа буцаасан ч хийгдэнэ. Утгыг хадгалах бол state-д буцааж `defaultValue`-д өг.
```

### Дүгнэлт

Action бол transition дотор ажилладаг (async байж болох) функц.
`<form action={fn}>` нь `preventDefault`, `FormData`, reset-ийг өөрөө
хийнэ. `useActionState(action, initialState)` нь үр дүн, `formAction`,
`isPending`-ийг өгнө — action `(previousState, formData)` авч шинэ state
буцаана.
""",
            initial_code=vite(
                """\
import { useActionState } from "react";
import { postFeedback } from "./api";

async function sendFeedback(previousState, formData) {
  // TODO 1: formData-аас name, message-ийг ав
  // TODO 2: сэтгэгдэл 5 тэмдэгтээс богино бол алдаа буцаа
  // TODO 3: postFeedback({ name, message })-ийг дууд. Амжилттай бол талархал,
  //         алдаа шидвэл «Илгээж чадсангүй…» гэсэн state буцаа
  return previousState;
}

export default function App() {
  // TODO 4: useActionState(sendFeedback, { error: null, success: null })

  return (
    <form style={{ display: "grid", gap: 8, maxWidth: 320 }}>
      <h1>Санал хүсэлт</h1>
      <label>
        Нэр
        <input name="name" />
      </label>
      <label>
        Сэтгэгдэл
        <textarea name="message" />
      </label>
      {/* TODO 5: илгээж байх үед товч идэвхгүй, «Илгээж байна…» гэсэн бичигтэй */}
      <button>Илгээх</button>
      {/* TODO 6: state.error-ийг role="alert"-тай, state.success-ийг <p>-д харуул */}
    </form>
  );
}
""",
                locked={
                    "api.js": """\
// Сэтгэгдлийг дадлагын API-д хадгална. Сервер алдаа буцаавал Error шиднэ.
export async function postFeedback({ name, message }) {
  const response = await fetch("/api/posts", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title: name, body: message }),
  });
  if (!response.ok) {
    throw new Error("Сервер алдаа буцаалаа");
  }
  return response.json();
}
"""
                },
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐ · 15 минут

Санал хүсэлтийн формыг React 19-ийн Actions-оор бич. `sendFeedback`-ийг
гүйцээгээд `useActionState`-ээр формд холбо. Сэтгэгдэл 5 тэмдэгтээс богино
бол «Сэтгэгдэл хэт богино байна.», сервер алдаа буцаавал «Илгээж чадсангүй.
Дахин оролдоно уу.» гэж харуул. Амжилттай бол «Баярлалаа, Бат!» гэж нэрээр
нь талархана. Илгээж байх хооронд товч идэвхгүй, «Илгээж байна…» гэсэн
бичигтэй байна. `useState`, `onSubmit` хэрэггүй.
""",
                tests=(
                    test(
                        "Богино сэтгэгдэлд «хэт богино» гэсэн алдаа гарч, сервер рүү хүсэлт явахгүй",
                        """
render(<App />);
await user.type(screen.getByLabelText("Нэр"), "Бат");
await user.type(screen.getByLabelText("Сэтгэгдэл"), "Гоё");
await user.click(screen.getByRole("button", { name: "Илгээх" }));
expect(await screen.findByRole("alert")).toHaveTextContent(/хэт богино/i);
expect(api.requests.filter((request) => request.method === "POST")).toHaveLength(0);
""",
                    ),
                    test(
                        "Илгээж байх үед товч идэвхгүй болж «Илгээж байна…» гэж бичигдэнэ",
                        """
render(<App />);
await user.type(screen.getByLabelText("Нэр"), "Бат");
await user.type(screen.getByLabelText("Сэтгэгдэл"), "Хүргэлт маш хурдан байлаа");
await user.click(screen.getByRole("button", { name: "Илгээх" }));
expect(screen.getByRole("button", { name: /Илгээж байна/ })).toBeDisabled();
await waitFor(() => expect(screen.getByRole("button", { name: "Илгээх" })).toBeEnabled());
""",
                    ),
                    test(
                        "Амжилттай илгээхэд «Баярлалаа, Бат!» гарч, сэтгэгдэл серверт хадгалагдана",
                        """
render(<App />);
await user.type(screen.getByLabelText("Нэр"), "Бат");
await user.type(screen.getByLabelText("Сэтгэгдэл"), "Хүргэлт маш хурдан байлаа");
await user.click(screen.getByRole("button", { name: "Илгээх" }));
expect(await screen.findByText(/Баярлалаа, Бат!/)).toBeInTheDocument();
expect(api.get("posts").some((post) => post.body === "Хүргэлт маш хурдан байлаа")).toBe(true);
expect(screen.getByRole("button", { name: "Илгээх" })).toBeEnabled();
""",
                    ),
                    test(
                        "Серверийн алдаа гарвал «Илгээж чадсангүй» гэсэн мэдэгдэл харагдана",
                        """
api.fail("/api/posts", 500);
render(<App />);
await user.type(screen.getByLabelText("Нэр"), "Бат");
await user.type(screen.getByLabelText("Сэтгэгдэл"), "Хүргэлт маш хурдан байлаа");
await user.click(screen.getByRole("button", { name: "Илгээх" }));
expect(await screen.findByRole("alert")).toHaveTextContent(/илгээж чадсангүй/i);
""",
                    ),
                ),
                tips="""\
- Action-ийн параметрүүдийн дараалал: `sendFeedback(previousState, formData)`.
- `formData.get("message")` текст буцаана — `.trim()` хийгээд уртыг нь шалга.
  Богино бол `postFeedback`-ийг дуудалгүй шууд
  `{ error: "Сэтгэгдэл хэт богино байна.", success: null }` буцаа.
- `postFeedback` алдаа шиддэг тул `try/catch`-д хий. `catch` дотор алдааг
  state болгон **буцаа** — дахин `throw` хийвэл апп бүхэлдээ унана.
- `const [state, formAction, isPending] = useActionState(sendFeedback, { error: null, success: null });`
  дараа нь `<form action={formAction}>`.
- Товчны бичиг, `disabled`-ийг `isPending`-ээс тооцно.
""",
                solution=solution(
                    App_jsx="""\
import { useActionState } from "react";
import { postFeedback } from "./api";

async function sendFeedback(previousState, formData) {
  const name = String(formData.get("name") ?? "").trim() || "зочин";
  const message = String(formData.get("message") ?? "").trim();

  if (message.length < 5) {
    return { error: "Сэтгэгдэл хэт богино байна.", success: null };
  }

  try {
    await postFeedback({ name, message });
    return { error: null, success: `Баярлалаа, ${name}!` };
  } catch (error) {
    return { error: "Илгээж чадсангүй. Дахин оролдоно уу.", success: null };
  }
}

export default function App() {
  const [state, formAction, isPending] = useActionState(sendFeedback, {
    error: null,
    success: null,
  });

  return (
    <form action={formAction} style={{ display: "grid", gap: 8, maxWidth: 320 }}>
      <h1>Санал хүсэлт</h1>
      <label>
        Нэр
        <input name="name" />
      </label>
      <label>
        Сэтгэгдэл
        <textarea name="message" />
      </label>
      <button disabled={isPending}>{isPending ? "Илгээж байна…" : "Илгээх"}</button>
      {state.error && <p role="alert">{state.error}</p>}
      {state.success && <p>{state.success}</p>}
    </form>
  );
}
"""
                ),
            ),
        ),
        # ------------------------------------------------------------------
        LessonSpec(
            title="useFormStatus: формын төлөв",
            slug="useformstatus",
            description="Формын доторх component-оос илгээлтийн төлвийг уншиж, дахин ашиглагдах SubmitButton бичих.",
            duration=900,
            language=JSX,
            content="""\
### Энэ хичээлээр

- `useFormStatus`-ээр формын илгээлтийн төлвийг доторх component-оос унших
- Олон форм дээр дахин ашиглагдах `SubmitButton` бичих
- `useFormStatus` яагаад формын **дотор** байх ёстойг ойлгох
- `data`-аар илгээж буй утгыг харуулах

### Яагаад чухал вэ

Апп-д олон форм бий: нэвтрэх, бүртгүүлэх, профайл, сэтгэгдэл. Илгээх товч
бүр хүсэлт явж байх хооронд идэвхгүй болж, «Хадгалж байна…» гэж бичих
ёстой — эс бөгөөс хэрэглэгч хоёр дарж, хоёр захиалга үүсгэнэ. Өмнөх
хичээлийн `isPending`-ийг товч руу prop-оор дамжуулж болох ч товч гүнзгий
байрласан (жишээ нь дизайн системийн component) бол prop drilling болно.
`useFormStatus` нь товчинд «намайг агуулж буй форм илгээгдэж байна уу?» гэж
шууд асуух боломж олгоно.

### useFormStatus

```jsx
import { useFormStatus } from "react-dom";

function SubmitButton({ children }) {
  const { pending } = useFormStatus();
  return (
    <button disabled={pending}>
      {pending ? "Хадгалж байна…" : children}
    </button>
  );
}

function ProfileForm() {
  return (
    <form action={saveProfile}>
      <input name="name" />
      <SubmitButton>Хадгалах</SubmitButton>
    </form>
  );
}
```

- Import нь `react` биш, **`react-dom`**-оос — DOM-ын `<form>`-той холбоотой
  тул.
- Буцаах объект: `pending` (илгээж байгаа эсэх), `data` (илгээж буй
  `FormData`, илгээгээгүй үед `null`), `method`, `action`.
- Hook нь эцэг `<form>`-оо context шиг хардаг. Хуудсан дээр хэд хэдэн форм
  байвал товч бүр зөвхөн өөрийн формын төлвийг мэднэ.
- `<form action={fn}>` хэлбэрийн формд ажиллана — `useActionState`-тэй ч,
  түүнгүй ч. `onSubmit`-оор илгээдэг формд ажиллахгүй.

### Хамгийн түгээмэл алдаа

```jsx
function ProfileForm() {
  const { pending } = useFormStatus(); // ❌ үргэлж false
  return (
    <form action={saveProfile}>
      <input name="name" />
      <button disabled={pending}>Хадгалах</button>
    </form>
  );
}
```

`useFormStatus` нь **өөрийг нь дуудсан component-ийг агуулж буй** формыг
хайдаг. Энд `<form>`-ийг `ProfileForm` өөрөө render хийж байгаа тул
`ProfileForm` формын дотор биш, гадна нь байна — `pending` үргэлж `false`.
Засвар нь формын дотор render хийгдэх тусдаа component (дээрх
`SubmitButton`). Формыг render хийж буй component-д төлөв хэрэгтэй бол
`useActionState`-ийн `isPending`-ийг ашигла.

### data — юу илгээж байгаа вэ

```jsx
function SavingNote() {
  const { pending, data } = useFormStatus();
  if (!pending) return null;
  return <p>«{data.get("name")}» нэрийг хадгалж байна…</p>;
}
```

`data` нь action-д очих `FormData`-тай ижил. Илгээж байх хооронд
хэрэглэгчид юу хадгалагдаж байгааг сануулахад тохиромжтой.

### isPending уу, useFormStatus уу

| | `isPending` (`useActionState`) | `useFormStatus` |
|---|---|---|
| Хаана ажиллах | Формыг render хийж буй component | Формын доторх аль ч component |
| Юу өгөх | Action-ийн төлөв, буцаасан state | Илгээлтийн төлөв, `data` |
| Тохирох газар | Нэг формын логик | Дахин ашиглагдах товч, spinner |

Хоёуланг нь нэг апп-д хамт хэрэглэх нь хэвийн. Бодит төслүүдэд
`SubmitButton` бараг үргэлж нэг удаа бичигдээд бүх формд ашиглагддаг.

```quiz
Доорх кодын алдааг ол: `function Form() { const { pending } = useFormStatus(); return <form action={save}><button disabled={pending}>OK</button></form>; }`
- [ ] `useFormStatus` зөвхөн `useActionState`-тэй ажилладаг
- [x] `Form` өөрөө `<form>`-ийг render хийж байгаа тул формын дотор биш — `pending` үргэлж `false`
- [ ] `disabled`-д boolean өгч болохгүй
> Hook-ийг формын дотор render хийгдэх component-д (жишээ нь `SubmitButton`) дууд.
```

```quiz
Хуудсан дээр хоёр форм байгаа бөгөөд хоёулаа `<SubmitButton>` ашигладаг. Эхний формыг илгээхэд аль товч идэвхгүй болох вэ?
- [x] Зөвхөн эхний формын товч
- [ ] Хоёр товч хоёулаа
- [ ] Аль нь ч биш — `useFormStatus` глобал төлөв хардаг
> `useFormStatus` нь хамгийн ойрын эцэг `<form>`-ийн төлвийг л өгнө.
```

```quiz
`useFormStatus`-ийг хаанаас import хийх вэ?
- [ ] `react`
- [x] `react-dom`
- [ ] `react-dom/client`
> `useActionState`, `useOptimistic` нь `react`-оос, харин формтой холбоотой `useFormStatus` нь `react-dom`-оос.
```

### Дүгнэлт

`useFormStatus()` нь хамгийн ойрын эцэг `<form>`-ийн илгээлтийн төлвийг
(`pending`, `data`) өгнө. Hook-ийг формын **дотор** render хийгдэх
component-д дуудна — ихэвчлэн дахин ашиглагдах `SubmitButton`. Формыг
render хийж буй component-д `isPending` хэрэглэнэ.
""",
            initial_code=vite(
                """\
import { useState } from "react";
import { useFormStatus } from "react-dom";
import SubmitButton from "./SubmitButton";
import { saveName, sendComment } from "./api";

export default function App() {
  const [name, setName] = useState("Зочин");
  const [comments, setComments] = useState([]);
  // ❌ «…нэрийг хадгалж байна…» мэдэгдэл хэзээ ч гарахгүй байна. Яагаад?
  const { pending, data } = useFormStatus();

  async function updateName(formData) {
    const next = formData.get("name");
    await saveName(next);
    setName(next);
  }

  async function addComment(formData) {
    const saved = await sendComment(formData.get("comment"));
    setComments((current) => [...current, saved]);
  }

  return (
    <main style={{ display: "grid", gap: 16, maxWidth: 360 }}>
      <h1>Сайн уу, {name}!</h1>
      <form action={updateName} style={{ display: "grid", gap: 8 }}>
        <label>
          Шинэ нэр <input name="name" />
        </label>
        {pending && <p>«{data.get("name")}» нэрийг хадгалж байна…</p>}
        <SubmitButton pendingText="Хадгалж байна…">Хадгалах</SubmitButton>
      </form>
      <form action={addComment} style={{ display: "grid", gap: 8 }}>
        <label>
          Сэтгэгдэл <input name="comment" />
        </label>
        <SubmitButton pendingText="Илгээж байна…">Илгээх</SubmitButton>
      </form>
      <ul>
        {comments.map((comment) => (
          <li key={comment.id}>{comment.body}</li>
        ))}
      </ul>
    </main>
  );
}
""",
                extra={
                    "SubmitButton.jsx": """\
// TODO: useFormStatus-оор эцэг форм илгээгдэж байгаа эсэхийг мэдэж,
// тэр үед товчийг идэвхгүй болгоод pendingText-ийг харуул
export default function SubmitButton({ children, pendingText }) {
  return <button>{children}</button>;
}
"""
                },
                locked={
                    "api.js": """\
// Дадлагын API руу хүсэлт илгээнэ. Хариу ирэхэд 0.4 секунд зарцуулагдана.
export async function saveName(name) {
  const response = await fetch("/api/users/1", {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name }),
  });
  if (!response.ok) throw new Error("Нэрийг хадгалж чадсангүй");
  return response.json();
}

export async function sendComment(text) {
  const response = await fetch("/api/posts", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title: "Сэтгэгдэл", body: text }),
  });
  if (!response.ok) throw new Error("Сэтгэгдэл илгээж чадсангүй");
  return response.json();
}
"""
                },
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐ · 12 минут

Профайл ба сэтгэгдлийн хоёр форм бэлэн. `SubmitButton.jsx`-ийг гүйцээ:
товч өөрийн форм илгээгдэж байх үед идэвхгүй болж, `pendingText`-ийг
харуулна. Мөн `App` дахь ««Бат» нэрийг хадгалж байна…» гэсэн мэдэгдэл
хэзээ ч гарахгүй байна — шалтгааныг олж засаарай.
""",
                tests=(
                    test(
                        "Нэр хадгалах үед «Хадгалах» товч идэвхгүй болж «Хадгалж байна…» гэж бичигдэнэ",
                        """
render(<App />);
await user.type(screen.getByLabelText("Шинэ нэр"), "Бат");
await user.click(screen.getByRole("button", { name: "Хадгалах" }));
expect(screen.getByRole("button", { name: /Хадгалж байна/ })).toBeDisabled();
await screen.findByRole("heading", { name: "Сайн уу, Бат!" });
await waitFor(() => expect(screen.getByRole("button", { name: "Хадгалах" })).toBeEnabled());
""",
                    ),
                    test(
                        "Нэг форм илгээгдэж байхад нөгөө формын товч идэвхтэй хэвээр байна",
                        """
render(<App />);
await user.type(screen.getByLabelText("Шинэ нэр"), "Бат");
await user.click(screen.getByRole("button", { name: "Хадгалах" }));
expect(screen.getByRole("button", { name: /Хадгалж байна/ })).toBeInTheDocument();
expect(screen.getByRole("button", { name: "Илгээх" })).toBeEnabled();
await waitFor(() => expect(screen.getByRole("button", { name: "Хадгалах" })).toBeEnabled());
""",
                    ),
                    test(
                        "Хадгалж байх үед «Бат» нэрийг хадгалж байгааг мэдэгдэнэ",
                        """
render(<App />);
await user.type(screen.getByLabelText("Шинэ нэр"), "Бат");
await user.click(screen.getByRole("button", { name: "Хадгалах" }));
expect(screen.getByText(/«Бат» нэрийг хадгалж байна/)).toBeInTheDocument();
await screen.findByRole("heading", { name: "Сайн уу, Бат!" });
await waitFor(() => expect(screen.queryByText(/нэрийг хадгалж байна/)).toBeNull());
""",
                    ),
                    test(
                        "Сэтгэгдэл илгээхэд товч түр идэвхгүй болж, сэтгэгдэл жагсаалтад нэмэгдэнэ",
                        """
render(<App />);
await user.type(screen.getByLabelText("Сэтгэгдэл"), "Гоё байна");
await user.click(screen.getByRole("button", { name: "Илгээх" }));
expect(screen.getByRole("button", { name: /Илгээж байна/ })).toBeDisabled();
expect(await screen.findByRole("listitem")).toHaveTextContent("Гоё байна");
await waitFor(() => expect(screen.getByRole("button", { name: "Илгээх" })).toBeEnabled());
""",
                    ),
                ),
                tips="""\
- `SubmitButton.jsx`-д `import { useFormStatus } from "react-dom";` — `react`
  биш.
- `const { pending } = useFormStatus();` дараа нь `disabled={pending}`, бичиг
  нь `pending ? pendingText : children`.
- `App` өөрөө `<form>`-ийг render хийдэг тул түүний дотор дуудсан
  `useFormStatus` формын гадна байна. Мэдэгдлийг тусдаа component болгож
  (жишээ нь `SavingNote`), профайлын `<form>` дотор render хий.
- `data` нь илгээгээгүй үед `null` — `pending` үнэн үед л `data.get(...)`
  дууд.
""",
                solution=solution(
                    App_jsx="""\
import { useState } from "react";
import { useFormStatus } from "react-dom";
import SubmitButton from "./SubmitButton";
import { saveName, sendComment } from "./api";

function SavingNote() {
  const { pending, data } = useFormStatus();
  if (!pending) return null;
  return <p>«{data.get("name")}» нэрийг хадгалж байна…</p>;
}

export default function App() {
  const [name, setName] = useState("Зочин");
  const [comments, setComments] = useState([]);

  async function updateName(formData) {
    const next = formData.get("name");
    await saveName(next);
    setName(next);
  }

  async function addComment(formData) {
    const saved = await sendComment(formData.get("comment"));
    setComments((current) => [...current, saved]);
  }

  return (
    <main style={{ display: "grid", gap: 16, maxWidth: 360 }}>
      <h1>Сайн уу, {name}!</h1>
      <form action={updateName} style={{ display: "grid", gap: 8 }}>
        <label>
          Шинэ нэр <input name="name" />
        </label>
        <SavingNote />
        <SubmitButton pendingText="Хадгалж байна…">Хадгалах</SubmitButton>
      </form>
      <form action={addComment} style={{ display: "grid", gap: 8 }}>
        <label>
          Сэтгэгдэл <input name="comment" />
        </label>
        <SubmitButton pendingText="Илгээж байна…">Илгээх</SubmitButton>
      </form>
      <ul>
        {comments.map((comment) => (
          <li key={comment.id}>{comment.body}</li>
        ))}
      </ul>
    </main>
  );
}
""",
                    SubmitButton_jsx="""\
import { useFormStatus } from "react-dom";

export default function SubmitButton({ children, pendingText }) {
  const { pending } = useFormStatus();
  return <button disabled={pending}>{pending ? pendingText : children}</button>;
}
""",
                ),
            ),
        ),
        # ------------------------------------------------------------------
        LessonSpec(
            title="useOptimistic: хүлээлгүй шинэчлэх",
            slug="useoptimistic",
            description="Серверийн хариуг хүлээлгүй UI шинэчилж, алдаа гарвал автоматаар буцаах (rollback).",
            duration=1080,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Optimistic UI гэж юу болох, хэзээ тохирохыг ойлгох
- `useOptimistic`-оор серверийн хариуг хүлээлгүй UI шинэчлэх
- Алдаа гарвал UI-г автоматаар буцаах (rollback), хэрэглэгчид мэдэгдэх
- «Хадгалж байна…» төлвийг тэмдэглэх

### Яагаад чухал вэ

Instagram-д зүрх дармагц улаан болдог — сервер хариулахыг хүлээдэггүй.
Чатад мессеж илгээмэгц жагсаалтад гарч, хажууд нь «илгээж байна» тэмдэг
байна. 400 мс хүлээж байж харуулбал апп удаан, гацсан мэт санагдана.
Ихэнх хүсэлт амжилттай болдог тул үр дүнг **урьдчилан таамаглаж**
(optimistic) харуулаад, ховор алдааны үед буцаах нь илүү сайн туршлага.

### useOptimistic

```jsx
const [optimisticState, addOptimistic] = useOptimistic(state, updateFn);
```

- `state` — жинхэнэ, серверээр баталгаажсан state.
- `updateFn(currentState, optimisticValue)` — optimistic утгыг хэрхэн
  нэмэхийг заах **цэвэр** функц, шинэ state буцаана.
- `optimisticState` — action ажиллаж байх хооронд `updateFn`-ийг хэрэглэсэн
  үр дүн, бусад үед `state`-тэй ижил.
- `addOptimistic(value)` — optimistic шинэчлэлт эхлүүлнэ.

```jsx
function LikeButton({ likes, onLike }) {
  const [optimisticLikes, addOptimisticLike] = useOptimistic(
    likes,
    (current, amount) => current + amount,
  );

  async function like() {
    addOptimisticLike(1);
    await onLike(); // сервер хадгалж, эцэг нь likes-ийг шинэчилнэ
  }

  return (
    <form action={like}>
      <button>❤️ {optimisticLikes}</button>
    </form>
  );
}
```

### Хэрхэн ажилладаг вэ

1. `addOptimistic(…)` дуудмагц React `optimisticState`-ийг шинэ утгаар
   render хийнэ.
2. Action хүлээж байх хооронд optimistic утга харагдсаар байна.
3. Action **дуусахад** React optimistic утгыг хаяж, жинхэнэ `state` руу
   буцна:
   - амжилттай бол та `state`-ийг шинэчилсэн тул шинэ утга үлдэнэ;
   - алдаа гарвал `state` өөрчлөгдөөгүй тул UI өөрөө **буцна** (rollback).

Rollback-ийг гараар бичихгүй — энэ бол `useOptimistic`-ийн гол давуу тал.

### Зөвхөн Action дотор

`addOptimistic`-ийг Action (form action эсвэл `startTransition`) дотор л
дуудна. Гадна нь дуудвал React «An optimistic state update occurred outside
a transition or action» гэж анхааруулаад утгыг шууд буцаана:

```jsx
// ❌ onClick-т шууд
<button onClick={() => addOptimisticLike(1)}>❤️</button>

// ✅ startTransition дотор
<button
  onClick={() =>
    startTransition(async () => {
      addOptimisticLike(1);
      await saveLike();
    })
  }
>
  ❤️
</button>
```

### Жагсаалтад нэмэх

```jsx
const [todos, setTodos] = useState(initialTodos);
const [optimisticTodos, addOptimisticTodo] = useOptimistic(
  todos,
  (current, newTodo) => [...current, { ...newTodo, sending: true }],
);

async function addTodo(formData) {
  const title = formData.get("title");
  addOptimisticTodo({ id: `temp-${Date.now()}`, title });
  try {
    const created = await createTodo(title);
    startTransition(() => {
      setTodos((current) => [...current, created]);
    });
  } catch (error) {
    setError("Хадгалж чадсангүй.");
  }
}
```

- `sending: true` тэмдгээр түр мөрийг бүдгэрүүлж, «(хадгалж байна…)» гэж
  бичнэ. Жагсаалтад `optimisticTodos`-ийг харуулна, `todos`-ийг биш.
- Түр `id`-г action дотор үүсгэж дамжуулна — `updateFn` цэвэр байх ёстой,
  React түүнийг хэд хэдэн удаа дуудаж болно.
- `await`-ийн дараах `setTodos`-ийг `startTransition`-оор ороосноор (хичээл
  2) шинэ мөр action-ийн төгсгөлтэй хамт гарч, түр мөртэй давхар
  харагдахгүй.
- Rollback-ийн дараа хэрэглэгчид **заавал мэдэгдэнэ**. Эс бөгөөс мөр
  чимээгүй алга болж, хэрэглэгч хадгалагдсан гэж бодно.

### Хэзээ хэрэглэх вэ

Тохирно: лайк, сагсанд нэмэх, чат, жагсаалтад нэмэх, checkbox — амжилттай
болох магадлал өндөр, буцаахад хялбар үйлдэл. Тохирохгүй: төлбөр төлөх,
захиалга баталгаажуулах зэрэг хэрэглэгч үр дүнд нь бүрэн итгэх ёстой
үйлдэл. Тэнд `isPending`-ээр хүлээлгэнэ.

TanStack Query-д (Модул 9) ижил санааг `useMutation`-ийн `onMutate`-ээр
бичдэг. `useOptimistic` нь React-ийн Actions-тэй шууд ажилладаг.

```quiz
`likes` нь 10. Action дотор `addOptimisticLike(1)` дуудаад сервер алдаа буцаав (`likes`-ийг шинэчлээгүй). Action дууссаны дараа товч дээр хэд харагдах вэ?
- [ ] 11
- [x] 10
- [ ] 0
> Action дуусахад optimistic утга хаягдаж, жинхэнэ `likes` (10) харагдана — rollback автоматаар.
```

```quiz
Доорх кодын алдааг ол: `<button onClick={() => addOptimisticLike(1)}>❤️</button>`
- [ ] `addOptimisticLike`-д тоо өгч болохгүй
- [x] Action эсвэл `startTransition`-ээс гадна дуудсан — React анхааруулаад утгыг шууд буцаана
- [ ] `onClick`-ийн оронд `onSubmit` бичих ёстой
> Optimistic шинэчлэлт нь action ажиллах хугацаанд л амьдардаг. Action байхгүй бол шууд дуусна.
```

```quiz
Аль үйлдэлд optimistic UI **тохирохгүй** вэ?
- [ ] Постод лайк дарах
- [ ] Чатад мессеж илгээх
- [x] Картаар төлбөр төлөх
> Төлбөр амжилттай болсон эсэхийг хэрэглэгч бодитоор мэдэх ёстой — серверийн хариуг хүлээнэ.
```

### Дүгнэлт

`useOptimistic(state, updateFn)` нь action ажиллаж байх хооронд таамагласан
үр дүнг харуулна. Action дуусахад жинхэнэ state руу буцдаг тул алдааны
үед rollback автоматаар хийгдэнэ. `addOptimistic`-ийг зөвхөн Action дотор
дуудаж, алдааг хэрэглэгчид заавал мэдэгдэнэ.
""",
            initial_code=vite(
                """\
import { startTransition, useOptimistic, useState } from "react";
import { createTodo } from "./api";
import { initialTodos } from "./data";

export default function App() {
  const [todos, setTodos] = useState(initialTodos);
  const [error, setError] = useState(null);
  const [simulateError, setSimulateError] = useState(false);
  // TODO 1: useOptimistic(todos, …)-оор optimisticTodos, addOptimisticTodo үүсгэ.
  //         Шинэ ажлыг { ...newTodo, done: false, sending: true } гэж нэм.

  async function addTodo(formData) {
    const title = String(formData.get("title") ?? "").trim();
    if (!title) return;
    setError(null);
    // TODO 2: хүлээхээс ӨМНӨ шинэ ажлыг optimistic-аар нэм
    // TODO 3: алдаа гарвал «Хадгалж чадсангүй. Дахин оролдоно уу.» гэж харуул
    const created = await createTodo(title, simulateError);
    startTransition(() => {
      setTodos((current) => [...current, created]);
    });
  }

  return (
    <main>
      <h1>Хийх ажил</h1>
      <form action={addTodo}>
        <label>
          Шинэ ажил <input name="title" />
        </label>{" "}
        <button>Нэмэх</button>
      </form>
      <label>
        <input
          type="checkbox"
          checked={simulateError}
          onChange={(event) => setSimulateError(event.target.checked)}
        />
        Серверийн алдааг дуурайх
      </label>
      {error && <p role="alert">{error}</p>}
      <ul>
        {/* TODO 4: todos-ийн оронд optimisticTodos-ийг харуул */}
        {todos.map((todo) => (
          <li key={todo.id} style={{ opacity: todo.sending ? 0.5 : 1 }}>
            {todo.done ? "✅" : "⬜"} {todo.title}
            {todo.sending && " (хадгалж байна…)"}
          </li>
        ))}
      </ul>
    </main>
  );
}
""",
                locked={
                    "api.js": """\
// Шинэ ажлыг дадлагын API-д хадгална. fail = true бол сервер 500 буцаана.
export async function createTodo(title, fail = false) {
  const response = await fetch(`/api/todos${fail ? "?_status=500" : ""}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, done: false }),
  });
  if (!response.ok) {
    throw new Error("Сервер алдаа буцаалаа");
  }
  return response.json();
}
""",
                    "data.js": """\
// Дадлагын API-ийн /api/todos-той ижил эхлэл өгөгдөл.
export const initialTodos = [
  { id: 1, title: "React хичээл үзэх", done: true },
  { id: 2, title: "useState дасгал хийх", done: false },
  { id: 3, title: "Төсөл эхлүүлэх", done: false },
];
""",
                },
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐⭐ · 15 минут

Шинэ ажил сервер хариулсны дараа л (0.4 секунд) жагсаалтад гарч байна.
`useOptimistic` ашиглан «Нэмэх» дармагц шинэ ажил «(хадгалж байна…)»
гэсэн тэмдэгтэй шууд гардаг болго. Сервер алдаа буцаавал ажил жагсаалтаас
алга болж, «Хадгалж чадсангүй. Дахин оролдоно уу.» гэсэн мэдэгдэл гарна.
«Серверийн алдааг дуурайх»-ийг чагтлаад алдааны тохиолдлыг «Хөтөч» дээр
туршаарай.
""",
                tests=(
                    test(
                        "«Нэмэх» дармагц шинэ ажил «(хадгалж байна…)» тэмдэгтэй шууд гарна",
                        """
render(<App />);
await user.type(screen.getByLabelText("Шинэ ажил"), "Дэлгүүр орох");
await user.click(screen.getByRole("button", { name: "Нэмэх" }));
const items = screen.getAllByRole("listitem");
expect(items).toHaveLength(4);
expect(items[3]).toHaveTextContent("Дэлгүүр орох");
expect(items[3]).toHaveTextContent(/хадгалж байна/);
await waitFor(() => expect(screen.queryByText(/хадгалж байна/)).toBeNull());
""",
                    ),
                    test(
                        "Сервер хариулсны дараа ажил жагсаалтад үлдэж, тэмдэг нь арилна",
                        """
render(<App />);
await user.type(screen.getByLabelText("Шинэ ажил"), "Дэлгүүр орох");
await user.click(screen.getByRole("button", { name: "Нэмэх" }));
await waitFor(() => expect(screen.queryByText(/хадгалж байна/)).toBeNull());
const items = screen.getAllByRole("listitem");
expect(items).toHaveLength(4);
expect(items[3]).toHaveTextContent("Дэлгүүр орох");
expect(api.get("todos").some((todo) => todo.title === "Дэлгүүр орох")).toBe(true);
""",
                    ),
                    test(
                        "Серверийн алдаа гарвал шинэ ажил алга болж, алдааны мэдэгдэл гарна",
                        """
api.fail("/api/todos", 500);
render(<App />);
await user.type(screen.getByLabelText("Шинэ ажил"), "Дэлгүүр орох");
await user.click(screen.getByRole("button", { name: "Нэмэх" }));
expect(screen.getAllByRole("listitem")).toHaveLength(4);
expect(await screen.findByRole("alert")).toHaveTextContent(/хадгалж чадсангүй/i);
await waitFor(() => expect(screen.getAllByRole("listitem")).toHaveLength(3));
expect(screen.text()).not.toContain("Дэлгүүр орох");
""",
                    ),
                ),
                tips="""\
- `const [optimisticTodos, addOptimisticTodo] = useOptimistic(todos, (current, newTodo) => …)`
  — `updateFn` нь `current` массивын төгсгөлд `sending: true`-тэй шинэ объект
  нэмсэн **шинэ** массив буцаана.
- Түр `id`-г action дотор үүсгээд дамжуул: `` { id: `temp-${Date.now()}`, title } ``.
- `addOptimisticTodo(...)`-г `await createTodo(...)`-оос **өмнө** дууд —
  эс бөгөөс optimistic утга хэтэрхий оройтож гарна.
- `await createTodo(...)`-г `try/catch`-д хий. `catch` дотор `setError(...)`
  дууд — жагсаалтыг гараар буцаах хэрэггүй, React өөрөө буцаана.
- JSX-д `todos.map` биш `optimisticTodos.map`.
""",
                solution=solution(
                    App_jsx="""\
import { startTransition, useOptimistic, useState } from "react";
import { createTodo } from "./api";
import { initialTodos } from "./data";

export default function App() {
  const [todos, setTodos] = useState(initialTodos);
  const [error, setError] = useState(null);
  const [simulateError, setSimulateError] = useState(false);
  const [optimisticTodos, addOptimisticTodo] = useOptimistic(todos, (current, newTodo) => [
    ...current,
    { ...newTodo, done: false, sending: true },
  ]);

  async function addTodo(formData) {
    const title = String(formData.get("title") ?? "").trim();
    if (!title) return;
    setError(null);
    addOptimisticTodo({ id: `temp-${Date.now()}`, title });
    try {
      const created = await createTodo(title, simulateError);
      startTransition(() => {
        setTodos((current) => [...current, created]);
      });
    } catch (error) {
      setError("Хадгалж чадсангүй. Дахин оролдоно уу.");
    }
  }

  return (
    <main>
      <h1>Хийх ажил</h1>
      <form action={addTodo}>
        <label>
          Шинэ ажил <input name="title" />
        </label>{" "}
        <button>Нэмэх</button>
      </form>
      <label>
        <input
          type="checkbox"
          checked={simulateError}
          onChange={(event) => setSimulateError(event.target.checked)}
        />
        Серверийн алдааг дуурайх
      </label>
      {error && <p role="alert">{error}</p>}
      <ul>
        {optimisticTodos.map((todo) => (
          <li key={todo.id} style={{ opacity: todo.sending ? 0.5 : 1 }}>
            {todo.done ? "✅" : "⬜"} {todo.title}
            {todo.sending && " (хадгалж байна…)"}
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
        # ------------------------------------------------------------------
        LessonSpec(
            title="use(): Promise ба Context",
            slug="use-hook",
            description="use()-ээр Promise-ийг Suspense-тэй уншиж, Promise-ийг зөв газар үүсгэх; use(Context)-ийг нөхцөл дотор.",
            duration=1020,
            language=JSX,
            content="""\
### Энэ хичээлээр

- `use()`-ээр Promise-ийн утгыг render дотор унших
- Suspense ба error boundary-тай хамт ашиглах
- Promise-ийг хаана үүсгэх ёстойг ойлгох — render дотор биш
- `use(Context)`-ийг нөхцөл дотор дуудах

### Яагаад чухал вэ

Модул 5, 9-д өгөгдлийг `useEffect` + `useState`-ээр татсан: ачаалал,
алдаа, өгөгдлийн гурван state, хариу холилдохоос сэргийлэх `ignore` туг.
React 19-ийн `use()` нь Promise-ийг шууд уншиж, ачааллын төлвийг
`Suspense`-д, алдааг error boundary-д даатгадаг. Модул 10-ийн
`SearchResults.jsx` яг үүнийг ашигласан — одоо дотор нь юу болдгийг үзье.

### use(promise)

```jsx
import { Suspense, use } from "react";

function UserName({ userPromise }) {
  const user = use(userPromise); // Promise биелэх хүртэл «хүлээнэ»
  return <p>{user.name}</p>;
}

<Suspense fallback={<p>Ачаалж байна…</p>}>
  <UserName userPromise={userPromise} />
</Suspense>
```

- Promise хүлээгдэж байвал component **suspend** хийнэ — хамгийн ойрын
  `Suspense`-ийн fallback харагдана.
- Биелэхэд React component-ийг дахин render хийж, `use` утгыг буцаана.
- Татгалзвал (reject) хамгийн ойрын error boundary алдааг барина.

### Алтан дүрэм: Promise-ийг render дотор үүсгэхгүй

```jsx
function UserName({ id }) {
  // ❌ render бүрт ШИНЭ Promise
  const user = use(fetch(`/api/users/${id}`).then((r) => r.json()));
  return <p>{user.name}</p>;
}
```

Promise биелэхэд React component-ийг дахин render хийнэ — тэр үед шинэ
`fetch` явж, дахин suspend хийнэ. Хүсэлт төгсгөлгүй давтагдаж, «Ачаалж
байна…» хэзээ ч арилахгүй. Console-д «A component was suspended by an
uncached promise» гэсэн анхааруулга гарна. Promise-ийг render-ээс гадна
үүсгэж, **хадгалах** гурван арга бий:

1. **Кэш** — ижил түлхүүрт үргэлж ижил Promise буцаана:

```jsx
const cache = new Map();

function getUser(id) {
  if (!cache.has(id)) {
    cache.set(id, fetch(`/api/users/${id}`).then((r) => r.json()));
  }
  return cache.get(id);
}

function UserName({ id }) {
  const user = use(getUser(id)); // ✅ ижил id → ижил Promise
  return <p>{user.name}</p>;
}
```

2. **Event handler дотор үүсгэж, state-д хадгалах:**

```jsx
const [userPromise, setUserPromise] = useState(() => getUser(1));
// ...
<button onClick={() => setUserPromise(getUser(2))}>Сараа</button>
```

3. **Framework, сангаас авах.** Next.js-ийн Server Component Promise-ийг
   props-оор дамжуулна (хичээл 6), TanStack Query-ийн `useSuspenseQuery`
   кэшээ өөрөө удирдана. Бодит төсөлд ихэвчлэн энэ арга.

Энгийн `Map` кэш хэзээ ч хоосордоггүй, алдааг ч хадгалж үлддэг —
ойлголтод тохиромжтой, production-д кэшийг сан удирдана.

### Шилжилт ба алдаа

Өөр хэрэглэгч сонгоход component дахин suspend хийж, fallback гарна.
Хуучин мэдээллийг үлдээх бол сонголтыг Модул 10-ийн `startTransition`-оор
ороо. Алдааг барихын тулд `Suspense`-ийг error boundary-гаар ороох ёстой:

```jsx
<ErrorBoundary fallback={<p>Ачаалж чадсангүй.</p>}>
  <Suspense fallback={<p>Ачаалж байна…</p>}>
    <UserName id={id} />
  </Suspense>
</ErrorBoundary>
```

`use`-ийг `try/catch` дотор дуудахгүй — алдааг boundary барина. Эсвэл
Promise-д өөрт нь `.catch(() => null)` хийгээд component дотор `null`-ийг
шалгана.

### use(Context)

`use(ThemeContext)` нь `useContext(ThemeContext)`-тэй ижил утга буцаана.
Ялгаа нь `use`-ийг нөхцөл, давталт дотор, эрт `return`-ийн дараа дуудаж
болно:

```jsx
function Badge({ show }) {
  if (!show) return null;
  const theme = use(ThemeContext); // ✅ useContext энд hook-ийн дүрэм зөрчинө
  return <span className={theme}>Шинэ</span>;
}
```

Энэ нь hook-ийн дүрмийн (Модул 6) цорын ганц үл хамаарах зүйл. Гэхдээ
`use` ч гэсэн зөвхөн component эсвэл hook дотор дуудагдана — энгийн функц,
event handler дотор биш.

```quiz
Доорх кодын алдааг ол: `function Product({ id }) { const p = use(fetch("/api/products/" + id).then((r) => r.json())); … }`
- [ ] `use`-ийг `await`-тэй бичих ёстой
- [x] Promise render бүрт шинээр үүсдэг — хүсэлт төгсгөлгүй давтагдана
- [ ] `use` зөвхөн Context уншдаг
> Promise-ийг render-ээс гадна үүсгэ: кэш, state эсвэл framework, сангаас.
```

```quiz
`use(promise)`-ийн Promise татгалзвал (reject) юу болох вэ?
- [ ] `use` нь `undefined` буцаана
- [ ] Suspense-ийн fallback үүрд харагдана
- [x] Хамгийн ойрын error boundary алдааг барина
> Ачааллыг `Suspense`, алдааг error boundary удирдана. Хоёуланг нь тавь.
```

```quiz
Аль нь нөхцөл (`if`) дотор дуудагдаж болох вэ?
- [ ] `useContext(ThemeContext)`
- [x] `use(ThemeContext)`
- [ ] `useState(0)`
> `use` бол нөхцөл, давталт дотор дуудаж болох цорын ганц hook маягийн API.
```

### Дүгнэлт

`use(promise)` нь Promise-ийн утгыг render дотор уншиж, хүлээх хооронд
`Suspense`-ийн fallback, алдаанд error boundary-г ашиглана. Promise-ийг
хэзээ ч render дотор үүсгэхгүй — кэш, state эсвэл framework-оос авна.
`use(Context)` нь `useContext` шиг боловч нөхцөл дотор дуудагдаж болно.
""",
            initial_code=vite(
                """\
import { Suspense, use, useState } from "react";
import { fetchUser } from "./api";

const users = [
  { id: 1, name: "Бат" },
  { id: 2, name: "Сараа" },
  { id: 3, name: "Тэмүүлэн" },
];

const cache = new Map();

function getUser(id) {
  // TODO 1: id бүрийн Promise-ийг cache-д хадгал. Дахин дуудахад шинээр
  //         татахгүй, хадгалсан Promise-ийг буцаа.
  return fetchUser(id);
}

function UserCard({ id }) {
  // TODO 2: use(getUser(id))-ээр хэрэглэгчийг уншаад нэр, имэйл, хотыг харуул
  return <p>Хэрэглэгч №{id}</p>;
}

export default function App() {
  const [selectedId, setSelectedId] = useState(1);

  return (
    <main>
      <h1>Хэрэглэгчид</h1>
      <nav style={{ display: "flex", gap: 8 }}>
        {users.map((user) => (
          <button
            key={user.id}
            onClick={() => setSelectedId(user.id)}
            aria-pressed={user.id === selectedId}
          >
            {user.name}
          </button>
        ))}
      </nav>
      {/* TODO 3: UserCard-ийг «Ачаалж байна…» fallback-тай Suspense-ээр ороо */}
      <UserCard id={selectedId} />
    </main>
  );
}
""",
                locked={
                    "api.js": """\
// Нэг хэрэглэгчийг дадлагын API-аас татна. Дуудах бүрт ШИНЭ хүсэлт явна.
export function fetchUser(id) {
  console.log(`🌐 /api/users/${id} татаж байна`);
  return fetch(`/api/users/${id}`).then((response) => {
    if (!response.ok) {
      throw new Error("Хэрэглэгч олдсонгүй");
    }
    return response.json();
  });
}
"""
                },
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐⭐ · 15 минут

Хэрэглэгч сонгоход түүний нэр, имэйл, хотыг харуулдаг болго. `UserCard`
нь өгөгдлийг `use()`-ээр уншиж, ачаалах хооронд «Ачаалж байна…» гэсэн
fallback харагдана. Нэг хэрэглэгчийг дахин сонгоход сервер рүү дахин
хүсэлт явах ёсгүй — Console-оос «🌐 … татаж байна» мөрийг ажиглаарай.
""",
                tests=(
                    test(
                        "Эхлээд «Ачаалж байна…» харагдаж, дараа нь Батын имэйл, хот гарна",
                        """
await runMain();
expect(screen.getByText(/ачаалж байна/i)).toBeInTheDocument();
expect(await screen.findByText(/bat@example.mn/)).toBeInTheDocument();
expect(screen.getByText(/Улаанбаатар/)).toBeInTheDocument();
expect(screen.queryByText(/ачаалж байна/i)).toBeNull();
""",
                    ),
                    test(
                        "Өөр хэрэглэгч сонгоход түүний мэдээлэл гарна",
                        """
await runMain();
await screen.findByText(/bat@example.mn/);
await user.click(screen.getByRole("button", { name: "Сараа" }));
expect(await screen.findByText(/saraa@example.mn/)).toBeInTheDocument();
expect(screen.getByText(/Дархан/)).toBeInTheDocument();
""",
                    ),
                    test(
                        "Нэг хэрэглэгчийг дахин сонгоход сервер рүү дахин хүсэлт явахгүй",
                        """
await runMain();
await screen.findByText(/bat@example.mn/);
await user.click(screen.getByRole("button", { name: "Сараа" }));
await screen.findByText(/saraa@example.mn/);
await user.click(screen.getByRole("button", { name: "Бат" }));
expect(await screen.findByText(/bat@example.mn/)).toBeInTheDocument();
const batRequests = api.requests.filter((request) => request.path === "/api/users/1");
expect(batRequests).toHaveLength(1);
""",
                    ),
                ),
                tips="""\
- `getUser` дотор: `cache.has(id)` биш бол `cache.set(id, fetchUser(id))`,
  дараа нь үргэлж `return cache.get(id);`.
- `UserCard` дотор `const user = use(getUser(id));` — `await` хэрэггүй.
  Дараа нь `user.name`, `user.email`, `user.city`-г харуул.
- `getUser`-ийг кэшгүй үлдээвэл render бүрт шинэ Promise үүсч, хүсэлт
  зогсохгүй — Console-д «🌐» мөр тасралтгүй нэмэгдэнэ.
- `<Suspense fallback={<p>Ачаалж байна…</p>}>`-ийг `UserCard`-ийн эргэн
  тойронд тавь. `Suspense`-ийг `UserCard`-ийн **дотор** тавибал ажиллахгүй
  — suspend хийж буй component-ийн дээр байх ёстой.
""",
                solution=solution(
                    App_jsx="""\
import { Suspense, use, useState } from "react";
import { fetchUser } from "./api";

const users = [
  { id: 1, name: "Бат" },
  { id: 2, name: "Сараа" },
  { id: 3, name: "Тэмүүлэн" },
];

const cache = new Map();

function getUser(id) {
  if (!cache.has(id)) {
    cache.set(id, fetchUser(id));
  }
  return cache.get(id);
}

function UserCard({ id }) {
  const user = use(getUser(id));
  return (
    <article>
      <h2>{user.name}</h2>
      <p>📧 {user.email}</p>
      <p>📍 {user.city}</p>
    </article>
  );
}

export default function App() {
  const [selectedId, setSelectedId] = useState(1);

  return (
    <main>
      <h1>Хэрэглэгчид</h1>
      <nav style={{ display: "flex", gap: 8 }}>
        {users.map((user) => (
          <button
            key={user.id}
            onClick={() => setSelectedId(user.id)}
            aria-pressed={user.id === selectedId}
          >
            {user.name}
          </button>
        ))}
      </nav>
      <Suspense fallback={<p>Ачаалж байна…</p>}>
        <UserCard id={selectedId} />
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
            title="Server ба Client Components",
            slug="server-components",
            description="Server Component, Client Component, «use client» хил, serializable props ба SSR-ээс ялгаа.",
            duration=1080,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Server Component ба Client Component-ийн ялгааг ойлгох
- Аль код хаана ажиллаж болох, болохгүйг мэдэх
- `"use client"` хил, serializable props, `children`-ээр холих
- Server Components-ийг SSR-ээс ялгах

### Яагаад чухал вэ

Одоогийн Vite апп-д бүх component хөтөч дээр ажилладаг. Хэрэглэгч эхлээд
хоосон `<div id="root">`-тэй HTML авч, дараа нь апп-ын бүх JavaScript-ийг
татаж, React ажиллаж, `useEffect` API руу хүсэлт илгээж, хариу ирсний
дараа л дэлгэц дүүрнэ. Энэ дараалал (waterfall) удаан интернетэд хэдэн
секунд үргэлжилнэ. Барааны тайлбарыг нэг удаа HTML болгох markdown сан ч
хэрэглэгч бүрийн хөтөч рүү татагдана. **React Server Components (RSC)**
нь зарим component-ийг серверт ажиллуулж, зөвхөн үр дүнг нь хөтөч рүү
илгээнэ.

### Server Component

```jsx
// app/products/[id]/page.jsx — Next.js App Router
import { db } from "@/lib/db";
import AddToCart from "./AddToCart";

export default async function ProductPage({ params }) {
  const { id } = await params;
  const product = await db.product.findUnique({ where: { id: Number(id) } });

  return (
    <article>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <AddToCart productId={product.id} price={product.price} />
    </article>
  );
}
```

- `async` component: өгөгдлийг `await`-ээр шууд авна — `useEffect`,
  ачааллын state хэрэггүй.
- Өгөгдлийн сан, файл, нууц түлхүүрт шууд хандана. Код хөтөч рүү
  очдоггүй тул нууц задрахгүй.
- Component-ийн JavaScript-ийг хэрэглэгч татахгүй — зөвхөн render-ийн үр
  дүн очно. Bundle жижгэрнэ.
- Build хийх үед эсвэл хүсэлт бүрт серверт ажиллана.

### Client Component

```jsx
// app/products/[id]/AddToCart.jsx
"use client";

import { useState } from "react";

export default function AddToCart({ productId, price }) {
  const [quantity, setQuantity] = useState(1);
  // ... товчнууд, onClick
}
```

Файлын хамгийн эхний `"use client"` нь **хил** зурна: энэ файл болон
түүний импортолсон бүх зүйл клиентийн кодод орно. Client component-ийг ч
эхний ачаалалд серверт HTML болгож (SSR), дараа нь хөтөч дээр «сэргээж»
(hydrate) интерактив болгодог.

### Юу хаана ажиллах вэ

| | Server Component | Client Component |
|---|---|---|
| `async`/`await`-ээр өгөгдөл авах | ✅ | ❌ |
| Өгөгдлийн сан, нууц түлхүүр, файл | ✅ | ❌ |
| `useState`, `useEffect`, `useReducer` | ❌ | ✅ |
| `onClick`, `onChange` | ❌ | ✅ |
| `window`, `localStorage` | ❌ | ✅ |
| Context унших | ❌ | ✅ |
| JavaScript нь хөтөч рүү очих | Үгүй | Тийм |

Next.js App Router-т бүх component анхдагчаар **Server Component**.
`"use client"`-ийг зөвхөн интерактив хэрэгтэй, аль болох жижиг навч
(leaf) component-д тавь. Хуудсыг бүхэлд нь client болговол RSC-ийн давуу
тал алга болно.

### Хилээр дамжих props

Server-ээс client рүү props сүлжээгээр дамждаг тул **serializable** байх
ёстой: текст, тоо, boolean, массив, энгийн объект, `Date`, Promise, JSX.
Функц (Server Action-аас бусад), class-ийн объект дамжихгүй:

```jsx
<AddToCart productId={product.id} price={product.price} /> // ✅
<AddToCart onAdd={() => saveToCart(product.id)} />         // ❌ функц
```

Promise дамжуулж болох нь хүчтэй: server component сэтгэгдлүүдийг
хүлээлгүй `db.review.findMany()`-ийн Promise-ийг дамжуулж, client component
түүнийг хичээл 5-ын `use()`-ээр уншина. Хуудас хурдан гарч, сэтгэгдлүүд
Suspense-ийн дараа ачаалагдана.

### children-ээр холих

Client component server component-ийг **import** хийж чадахгүй — import
хийсэн бүхэн client болно. Харин `children`-ээр авч чадна:

```jsx
// Tabs.jsx — "use client", state-тэй
// page.jsx — server component
<Tabs>
  <ProductReviews productId={id} /> {/* server component хэвээр */}
</Tabs>
```

### Түгээмэл төөрөгдөл

- **RSC ба SSR өөр.** SSR нь client component-ийг эхний удаа серверт HTML
  болгож, дараа нь хөтөч дээр hydrate хийдэг — код нь хөтөч рүү очно.
  Server Component-ийн код хэзээ ч очихгүй, hydrate хийгдэхгүй. Next.js
  хоёуланг нь хамт хэрэглэдэг.
- **`"use server"` нь Server Component-д зориулагдаагүй.** Server Component
  ямар ч directive шаарддаггүй. `"use server"` нь Server Action-ийн тэмдэг
  (дараагийн хичээл).
- Серверийн кодыг санамсаргүй клиентэд import хийхээс `server-only`
  пакет сэргийлнэ: файлын эхэнд `import "server-only";`.

### Энэ sandbox-д

Sandbox бүхэлдээ хөтөч дотор ажилладаг — сервер байхгүй тул Server
Components ажиллахгүй, `"use client"` мөрийг зүгээр алгасна. Гэхдээ
component-оо серверт **бэлэн** байдлаар хувааж сурч болно: hook-гүй,
өгөгдлийг props-оор авдаг хэсэг (server) ба state, event-тэй жижиг хэсэг
(client). Жинхэнэ төсөл эхлүүлэх: `npx create-next-app@latest`.

```quiz
Аль нь Server Component дотор хийж болох зүйл вэ?
- [ ] `useState`-ээр тоолуур хадгалах
- [x] `await db.product.findMany()`-ээр өгөгдөл унших
- [ ] `onClick`-ээр товч дарахыг сонсох
- [ ] `localStorage`-оос тохиргоо унших
> Server Component серверт нэг удаа ажиллаж, үр дүнгээ илгээнэ — state, event, хөтчийн API түүнд байхгүй.
```

```quiz
Server component `<AddToCart onAdd={() => save(id)} />` гэж render хийв. `AddToCart` нь `"use client"`. Юу болох вэ?
- [ ] Хэвийн ажиллана
- [x] Алдаа — функц serializable биш тул хилээр дамжихгүй
- [ ] `onAdd` серверт ажиллана
> Хилээр зөвхөн өгөгдөл (текст, тоо, объект, Promise, JSX) дамжина. Үйлдлийг client component дотор бич эсвэл Server Action ашигла.
```

```quiz
Next.js-д Server Component бичихдээ файлын эхэнд юу бичих вэ?
- [x] Юу ч бичихгүй — анхдагчаар Server Component
- [ ] `"use server"`
- [ ] `"use client"`
> `"use client"` нь client хил, `"use server"` нь Server Action. Server Component directive шаарддаггүй.
```

### Дүгнэлт

Server Component серверт ажиллаж, өгөгдлийг шууд уншдаг, кодоо хөтөч рүү
илгээдэггүй. Client Component (`"use client"`) state, event, хөтчийн
API-тай. Хилээр зөвхөн serializable props дамжина. `"use client"`-ийг аль
болох жижиг, интерактив хэсэгт тавь.
""",
            initial_code=files(
                (
                    "ProductPage.jsx",
                    """\
import { useState } from "react";

// Энэ component бүхэлдээ клиентэд ажиллах ёстой — дотор нь state, onClick
// бий. Гэтэл гарчиг, тайлбар, үнэ, мэдээлэл серверт render хийгдэж болно.
// TODO: state ба товчнуудыг AddToCart.jsx руу зөөж, энэ component-ийг
//       hook-гүй (server component болж чадах) болго.
export default function ProductPage({ product }) {
  const [quantity, setQuantity] = useState(1);
  const [added, setAdded] = useState(0);

  return (
    <article style={{ maxWidth: 380 }}>
      <h1>
        {product.emoji} {product.name}
      </h1>
      <p>{product.description}</p>
      <p>Үнэ: {product.price}₮</p>
      <ul>
        {product.facts.map((fact) => (
          <li key={fact}>{fact}</li>
        ))}
      </ul>
      <div>
        <button onClick={() => setQuantity(Math.max(1, quantity - 1))} aria-label="Хасах">
          −
        </button>
        <span> {quantity} </span>
        <button onClick={() => setQuantity(quantity + 1)} aria-label="Нэмэх">
          +
        </button>{" "}
        <button onClick={() => setAdded(added + quantity)}>Сагсанд нэмэх</button>
        {added > 0 && (
          <p role="status">
            Сагсанд {added} ширхэг байна — {added * product.price}₮.
          </p>
        )}
      </div>
    </article>
  );
}
""",
                ),
                (
                    "AddToCart.jsx",
                    """\
"use client";

// TODO: ProductPage-ийн тоо ширхэгийн state, «−», «+», «Сагсанд нэмэх»
//       товчнууд ба «Сагсанд N ширхэг байна — …₮.» мэдэгдлийг энд зөө.
//       Props-оор зөвхөн өгөгдөл авна: price (тоо). Функц биш.
export default function AddToCart({ price }) {
  return null;
}
""",
                ),
                (
                    "App.jsx",
                    """\
// «Сервер» тал. Бодит Next.js төсөлд энэ нь app/products/[id]/page.jsx —
// async server component: const product = await db.product.findUnique(…).
// Sandbox-д сервер байхгүй тул өгөгдлийг db.js-ээс шууд авна.
import ProductPage from "./ProductPage";
import { product } from "./db";

export default function App() {
  return <ProductPage product={product} />;
}
""",
                    True,
                ),
                (
                    "db.js",
                    """\
// Өгөгдлийн санг дуурайна. Бодит төсөлд энэ код зөвхөн СЕРВЕРТ ажиллаж,
// нууц түлхүүр, SQL асуулга агуулж болно — хөтөч рүү хэзээ ч очихгүй.
export const product = {
  id: 8,
  name: "Бяслаг",
  emoji: "🧀",
  price: 12500,
  description: "Орон нутгийн сүүгээр хийсэн, 6 сар боловсруулсан хатуу бяслаг.",
  facts: ["Жин: 500 г", "Хадгалах хугацаа: 60 хоног", "Гарал үүсэл: Сэлэнгэ аймаг"],
};
""",
                    True,
                ),
                ("main.jsx", MAIN, True),
                ("index.html", HTML, True),
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐ · 12 минут

Барааны хуудас нэг л component бөгөөд `useState` агуулдаг тул Next.js-д
бүхэлдээ client component болох ёстой. Үүнийг хуваа: тоо ширхэгийн
state, товчнууд, мэдэгдлийг `AddToCart.jsx` руу зөө. `ProductPage` нь
hook-гүй болж, `<AddToCart price={…} />`-ийг render хийнэ. Хуудас өмнөх
шигээ ажиллах ёстой.
""",
                tests=(
                    test(
                        "ProductPage нь hook ашигладаггүй — server component болж чадна",
                        """
const ProductPage = mod("./ProductPage").default;
const { product } = mod("./db");
try {
  ProductPage({ product });
} catch (error) {
  throw new Error(
    `ProductPage-ийг серверт ажиллуулж чадсангүй (${error.message}). Hook-уудыг AddToCart руу зөө.`,
  );
}
""",
                    ),
                    test(
                        "ProductPage нь AddToCart-д зөвхөн өгөгдөл дамжуулна, функц биш",
                        """
const ProductPage = mod("./ProductPage").default;
const AddToCart = mod("./AddToCart").default;
const { product } = mod("./db");
const found = [];
function walk(node) {
  if (Array.isArray(node)) {
    node.forEach(walk);
    return;
  }
  if (!node || typeof node !== "object") return;
  if (node.type === AddToCart) found.push(node);
  walk(node.props && node.props.children);
}
walk(ProductPage({ product }));
expect(found).toHaveLength(1);
const functionProps = Object.entries(found[0].props)
  .filter(([, value]) => typeof value === "function")
  .map(([name]) => name);
expect(functionProps).toEqual([]);
""",
                    ),
                    test(
                        "AddToCart дангаараа тоо ширхэгийг өөрчилж, сагсанд нэмнэ",
                        """
const AddToCart = mod("./AddToCart").default;
render(<AddToCart price={1000} />);
await user.click(screen.getByRole("button", { name: "Нэмэх" }));
await user.click(screen.getByRole("button", { name: "Сагсанд нэмэх" }));
expect(screen.getByText(/Сагсанд 2 ширхэг/)).toBeInTheDocument();
expect(screen.text()).toContain("2000₮");
""",
                    ),
                    test(
                        "Хуудас бүтнээрээ өмнөх шигээ ажиллана",
                        """
render(<App />);
expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent("Бяслаг");
expect(screen.text()).toContain("6 сар боловсруулсан");
await user.click(screen.getByRole("button", { name: "Нэмэх" }));
await user.click(screen.getByRole("button", { name: "Нэмэх" }));
await user.click(screen.getByRole("button", { name: "Хасах" }));
await user.click(screen.getByRole("button", { name: "Сагсанд нэмэх" }));
expect(screen.getByText(/Сагсанд 2 ширхэг/)).toBeInTheDocument();
expect(screen.text()).toContain("25000₮");
""",
                    ),
                ),
                tips="""\
- `import { useState } from "react";`, хоёр state, гурван товч, мэдэгдлийг
  бүгдийг нь `AddToCart.jsx` руу зөө. `ProductPage.jsx`-д `useState`
  огт үлдэх ёсгүй.
- Мэдэгдэлд нийт үнэ хэрэгтэй тул `AddToCart` `price`-ийг prop-оор авна:
  `<AddToCart price={product.price} />` — тоо бол serializable.
- `onAdd={() => …}` гэх мэт функц дамжуулахгүй. Server component-оос
  client руу функц дамжихгүй.
- `"use client"` мөр `AddToCart.jsx`-ийн хамгийн эхэнд үлдэнэ —
  sandbox үүнийг алгасдаг ч бодит Next.js төсөлд шаардлагатай.
""",
                solution=files(
                    (
                        "ProductPage.jsx",
                        """\
import AddToCart from "./AddToCart";

export default function ProductPage({ product }) {
  return (
    <article style={{ maxWidth: 380 }}>
      <h1>
        {product.emoji} {product.name}
      </h1>
      <p>{product.description}</p>
      <p>Үнэ: {product.price}₮</p>
      <ul>
        {product.facts.map((fact) => (
          <li key={fact}>{fact}</li>
        ))}
      </ul>
      <AddToCart price={product.price} />
    </article>
  );
}
""",
                    ),
                    (
                        "AddToCart.jsx",
                        """\
"use client";

import { useState } from "react";

export default function AddToCart({ price }) {
  const [quantity, setQuantity] = useState(1);
  const [added, setAdded] = useState(0);

  return (
    <div>
      <button onClick={() => setQuantity(Math.max(1, quantity - 1))} aria-label="Хасах">
        −
      </button>
      <span> {quantity} </span>
      <button onClick={() => setQuantity(quantity + 1)} aria-label="Нэмэх">
        +
      </button>{" "}
      <button onClick={() => setAdded(added + quantity)}>Сагсанд нэмэх</button>
      {added > 0 && (
        <p role="status">
          Сагсанд {added} ширхэг байна — {added * price}₮.
        </p>
      )}
    </div>
  );
}
""",
                    ),
                ),
            ),
        ),
        # ------------------------------------------------------------------
        LessonSpec(
            title="Server Actions ба React Compiler",
            slug="server-actions-compiler",
            description="«use server» функцийг формоос дуудах, bind-ээр аргумент дамжуулах; React Compiler-ийн автомат memoization.",
            duration=1140,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Server Action (`"use server"`) гэж юу болох, хэрхэн дуудагддагийг ойлгох
- Server Action-ийг `<form action>`, `useActionState`-тэй холбож, нэмэлт
  аргументыг `bind`-ээр дамжуулах
- Server Action-ийн аюулгүй байдлын дүрмийг мэдэх
- React Compiler юу хийдэг, `useMemo`, `useCallback`, `memo`-д юу гэсэн
  үг болохыг ойлгох

### Яагаад чухал вэ

Өмнөх хичээлд өгөгдлийг серверт **унших**-ыг үзсэн. Харин **өөрчлөх**
(сагсанд нэмэх, сэтгэгдэл бичих) яах вэ? Уламжлалт арга: API route
(`POST /api/cart`) бичиж, клиентээс `fetch`-ээр JSON илгээж, хариуны кодыг
шалгана. Server Action нь серверийн функцийг клиентээс энгийн async функц
шиг дуудах боломж олгоно — хүсэлт, хаягийг framework өөрөө үүсгэнэ.

### Server Action

```jsx
// app/actions.js
"use server";

import { db } from "@/lib/db";
import { revalidatePath } from "next/cache";

export async function addComment(previousState, formData) {
  const text = String(formData.get("text") ?? "").trim();
  if (text.length < 3) {
    return { error: "Сэтгэгдэл хэт богино байна." };
  }
  await db.comment.create({ data: { text } });
  revalidatePath("/products"); // хуудсын өгөгдлийг шинэчилнэ
  return { error: null };
}
```

- Файлын эхний `"use server"` нь тэр файлын бүх export-ийг Server Action
  (албан ёсоор Server Function) болгоно. Server Component дотор бол async
  функцийн биеийн эхэнд бичиж болно.
- Клиент талаас import хийхэд функцийн **код** биш, «серверийн энэ
  функцийг дууд» гэсэн **холбоос** очно. Дуудахад framework POST хүсэлт
  илгээж, буцаасан утгыг авчирна.
- Аргумент, буцаах утга serializable байна (өмнөх хичээл).

### Формоос дуудах

```jsx
"use client";

import { useActionState } from "react";
import { addComment } from "./actions";

export default function CommentForm() {
  const [state, formAction, isPending] = useActionState(addComment, { error: null });
  return (
    <form action={formAction}>
      <textarea name="text" />
      <button disabled={isPending}>Илгээх</button>
      {state.error && <p role="alert">{state.error}</p>}
    </form>
  );
}
```

Хичээл 2-той яг ижил — зөвхөн action серверт ажиллана. Server Component
дотор render хийсэн `<form action={serverAction}>` нь JavaScript ачаалагдаж
амжаагүй байхад ч ажилладаг (progressive enhancement): хөтөч формыг
энгийн POST хүсэлтээр илгээнэ.

### Нэмэлт аргумент: bind

Барааны `id` гэх мэт формд байхгүй утгыг `bind`-ээр урьдчилан өгнө:

```jsx
// actions.js
export async function addToCart(productId, formData) { … }

// component
<form action={addToCart.bind(null, product.id)}>
```

`addToCart.bind(null, 8)` нь эхний аргументыг 8 болгож тогтоосон шинэ
функц буцаана. `useActionState`-тэй хэрэглэвэл action
`(productId, previousState, formData)` гэж дуудагдана. Нууц биш утгыг
`<input type="hidden" name="productId" value={product.id} />`-ээр ч
дамжуулж болно.

### Аюулгүй байдал

Server Action бол интернэтэд нээлттэй **API endpoint**. Хэн ч түүнийг
өөрийн хүссэн өгөгдлөөр дуудаж чадна. Тиймээс:

- оролтыг серверт **дахин шалга** — клиентийн шалгалт хуурамчаар
  тойрогдоно;
- хэрэглэгч нэвтэрсэн, эрхтэй эсэхийг action бүрт шалга;
- үнэ зэрэг итгэлтэй утгыг клиентээс авахгүй, серверт өгөгдлийн сангаас
  унш.

### Серверийн өгөгдөл: бүтэн зураг

| Ажил | Уламжлалт SPA | Server Components + Actions |
|---|---|---|
| Унших | `useEffect`, TanStack Query + API route | Server Component дотор `await` |
| Өөрчлөх | `fetch("/api/…", { method: "POST" })` | Server Action |
| Дэлгэц шинэчлэх | Query-г invalidate хийх | `revalidatePath`, `redirect` |

TanStack Query хэрэггүй болохгүй: клиент талд байнга шинэчлэгддэг
өгөгдөл, infinite scroll, offline зэрэгт хэрэглэгдсээр байна.

### React Compiler

Модул 6-д `useMemo`, `useCallback`, Модул 12-т `memo`-гоор илүүц
тооцоолол, render-ээс сэргийлнэ. Гараар бичихэд dependency мартах, хаана
хэрэгтэйг мэдэхгүй байх, код бүдгэрэх зэрэг асуудал гардаг. **React
Compiler** нь build үед кодыг шинжилж, memoization-ийг **автоматаар**
нэмдэг хэрэгсэл (2025 оны 10-р сард 1.0 хувилбар гарсан). Та энгийн код
бичнэ:

```jsx
function ProductList({ products, query }) {
  const visible = products.filter((p) => p.name.includes(query));
  return <List items={visible} onSelect={(id) => console.log(id)} />;
}
```

Compiler үүнийг ойролцоогоор ийм болгоно (хялбарчилсан):

```jsx
import { c as _c } from "react/compiler-runtime";

function ProductList({ products, query }) {
  const $ = _c(3); // энэ component-ийн кэш
  let visible;
  if ($[0] !== products || $[1] !== query) {
    visible = products.filter((p) => p.name.includes(query));
    $[0] = products;
    $[1] = query;
    $[2] = visible;
  } else {
    visible = $[2];
  }
  // onSelect функц, <List> element-ийг ч мөн адил кэшилнэ…
}
```

`products`, `query` өөрчлөгдөөгүй бол шүүлт дахин хийгдэхгүй, `onSelect`
ижил функц хэвээр, `<List>` element ч ижил тул React түүнийг дахин render
хийлгүй алгасна — `useMemo`, `useCallback`, `memo`-г гараар бичсэнтэй
адил, гэхдээ илүү нарийн.

### Энэ нь юу гэсэн үг вэ

- Compiler асаасан төсөлд шинэ кодод `useMemo`, `useCallback`, `memo`-г
  ихэнхдээ бичихгүй.
- Байгаа `useMemo`, `useCallback`-ийг заавал устгах шаардлагагүй. Effect-ийн
  dependency-г нарийн удирдах мэт тохиолдолд гараар бичих нь «зугтах гарц»
  хэвээр.
- Compiler **React-ийн дүрмийг** (цэвэр render, props, state-ийг
  өөрчлөхгүй, hook-ийн дүрэм) дагасан код дээр л ажиллана. Дүрэм зөрчсөн
  component-ийг алгасна — кэшлэхгүй. `eslint-plugin-react-hooks`-ийн
  шинэ дүрмүүд ийм газрыг заана.
- Олон төсөл compiler-гүй хэвээр тул Модул 12-т memoization-ийг гараар
  үзнэ. Энэ нь compiler юу хийж байгааг ойлгоход ч хэрэгтэй.

Next.js-д `next.config`-т `reactCompiler: true`, Vite-д
`babel-plugin-react-compiler`-ийг суулгаж `vite.config.js`-д холбоно —
алхмыг react.dev/learn/react-compiler хуудаснаас хар.

### Энэ sandbox-д

Server Action серверт, Compiler build үед ажилладаг тул энд аль аль нь
ажиллахгүй. Дасгалын 🔒 `actions.js` нь `"use server"` файлыг дуурайна:
sandbox directive-ийг алгасаж функцийг хөтөчид ажиллуулдаг, «сервер» нь
дадлагын API. Жинхэнэ Next.js төсөлд таны component-ийн код яг ижил
байна.

```quiz
Файлын эхэнд `"use server"` гэж бичих нь юу гэсэн үг вэ?
- [ ] Энэ файлын component-ууд Server Component болно
- [x] Файлын export-ууд клиентээс дуудаж болох серверийн функц (Server Action) болно
- [ ] Файл зөвхөн build үед ажиллана
> Server Component directive шаарддаггүй. `"use server"` нь клиентээс дуудагдах серверийн функцийн тэмдэг.
```

```quiz
`addToCart` Server Action үнийг `formData.get("price")`-ээс авч захиалга үүсгэдэг. Юу нь буруу вэ?
- [ ] `formData` серверт хүрдэггүй
- [x] Хэн ч үнийг өөрчилж илгээж чадна — үнийг серверт өгөгдлийн сангаас унших ёстой
- [ ] `price` тоо биш текст тул алдаа гарна
> Server Action нь нээлттэй endpoint. Клиентээс ирсэн утгад итгэхгүй, серверт шалгана.
```

```quiz
React Compiler асаасан төсөлд шинэ component бичиж байна. `useCallback`-ийг яах вэ?
- [ ] Функц бүрийг заавал `useCallback`-аар ороох
- [x] Ихэнхдээ бичихгүй — compiler шаардлагатай газар өөрөө кэшилнэ
- [ ] `useCallback` compiler-тэй хамт ажиллахгүй тул хэзээ ч бичихгүй
> Compiler build үед memoization нэмдэг. Гараар бичсэн нь ажилласаар, гэхдээ ихэнхдээ илүүц.
```

### Дүгнэлт

Server Action (`"use server"`) нь клиентээс энгийн функц шиг дуудагдах
серверийн функц — `<form action>`, `useActionState`-тэй ажиллаж, `bind`-ээр
нэмэлт аргумент авна. Оролтыг үргэлж серверт шалгана. React Compiler нь
build үед memoization-ийг автоматаар нэмдэг тул цэвэр, дүрэмд нийцсэн код
бичих нь хамгийн чухал.
""",
            initial_code=vite(
                """\
import { useActionState } from "react";
import { addToCart } from "./actions";
import { products } from "./data";

function ProductCard({ product }) {
  // TODO 1: useActionState-д addToCart.bind(null, product.id)-г өг, анхны state: null

  return (
    <article style={{ border: "1px solid #d0d7de", borderRadius: 8, padding: 12 }}>
      <h2>
        {product.emoji} {product.name}
      </h2>
      <p>
        {product.price}₮ · үлдэгдэл {product.stock}
      </p>
      {/* TODO 2: формыг Server Action-тэй холбо */}
      <form>
        <label>
          Тоо ширхэг{" "}
          <input name="quantity" type="number" defaultValue={1} style={{ width: 56 }} />
        </label>{" "}
        {/* TODO 3: илгээж байх үед товч идэвхгүй */}
        <button>Сагсанд нэмэх</button>
      </form>
      {/* TODO 4: state.message-ийг харуул — алдаа (ok: false) бол role="alert" */}
    </article>
  );
}

export default function App() {
  return (
    <main style={{ display: "grid", gap: 12, maxWidth: 360 }}>
      <h1>🛒 Ногоон сагс</h1>
      {products.map((product) => (
        <ProductCard key={product.id} product={product} />
      ))}
    </main>
  );
}
""",
                locked={
                    "actions.js": """\
"use server";
// Бодит Next.js төсөлд энэ файл СЕРВЕРТ ажиллана: хөтөч зөвхөн «addToCart-ийг
// дууд» гэсэн хүсэлт илгээдэг. Sandbox-д серверийг дадлагын API-аар дуурайна.
import { products } from "./data";

export async function addToCart(productId, previousState, formData) {
  const quantity = Number(formData.get("quantity"));

  // Клиентээс ирсэн өгөгдөлд итгэхгүй — серверт дахин шалгана.
  if (!Number.isInteger(quantity) || quantity < 1) {
    return { ok: false, message: "Тоо ширхэг буруу байна." };
  }
  const product = products.find((item) => item.id === productId);
  if (!product) {
    return { ok: false, message: "Бараа олдсонгүй." };
  }
  if (quantity > product.stock) {
    return { ok: false, message: `Үлдэгдэл хүрэлцэхгүй байна (${product.stock} ширхэг).` };
  }

  const response = await fetch("/api/orders", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ productId, quantity, total: quantity * product.price }),
  });
  if (!response.ok) {
    return { ok: false, message: "Сагсанд нэмж чадсангүй." };
  }
  return { ok: true, message: `${quantity} ширхэг сагсанд нэмэгдлээ.` };
}
""",
                    "data.js": """\
export const products = [
  { id: 2, name: "Алим", emoji: "🍎", price: 2800, stock: 40 },
  { id: 8, name: "Бяслаг", emoji: "🧀", price: 12500, stock: 7 },
  { id: 9, name: "Талх", emoji: "🍞", price: 2500, stock: 12 },
];
""",
                },
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐⭐ · 15 минут

🔒 `actions.js` нь Next.js-ийн `"use server"` файлыг дуурайна:
`addToCart(productId, previousState, formData)` серверт тоо ширхэгийг
шалгаж, захиалга үүсгэнэ. `ProductCard` бүрийн формыг энэ Server Action-тэй
холбо — барааны `id`-г `bind`-ээр дамжуулж, `useActionState`-ээр үр дүнг
картын доор харуул (алдаа бол `role="alert"`). Илгээж байх хооронд
тухайн картын товч идэвхгүй байна.
""",
                tests=(
                    test(
                        "Карт бүрийн форм тухайн барааны id-тай захиалга үүсгэнэ",
                        """
const card = (name) =>
  screen.getAllByRole("article").find((item) => item.textContent.includes(name));
render(<App />);
const quantity = within(card("Бяслаг")).getByLabelText(/Тоо ширхэг/);
await user.clear(quantity);
await user.type(quantity, "2");
await user.click(within(card("Бяслаг")).getByRole("button", { name: /Сагсанд нэмэх/ }));
await waitFor(() => expect(api.get("orders")).toHaveLength(1));
expect(api.get("orders")[0]).toHaveProperty("productId", 8);
expect(api.get("orders")[0]).toHaveProperty("quantity", 2);
await within(card("Бяслаг")).findByText(/сагсанд нэмэгдлээ/);
""",
                    ),
                    test(
                        "Амжилттай бол зөвхөн тухайн картад «3 ширхэг сагсанд нэмэгдлээ» гарна",
                        """
const card = (name) =>
  screen.getAllByRole("article").find((item) => item.textContent.includes(name));
render(<App />);
const quantity = within(card("Алим")).getByLabelText(/Тоо ширхэг/);
await user.clear(quantity);
await user.type(quantity, "3");
await user.click(within(card("Алим")).getByRole("button", { name: /Сагсанд нэмэх/ }));
expect(await within(card("Алим")).findByText(/3 ширхэг сагсанд нэмэгдлээ/)).toBeInTheDocument();
expect(within(card("Талх")).queryByText(/сагсанд нэмэгдлээ/)).toBeNull();
""",
                    ),
                    test(
                        "Илгээж байх үед зөвхөн тухайн картын товч идэвхгүй болно",
                        """
const card = (name) =>
  screen.getAllByRole("article").find((item) => item.textContent.includes(name));
render(<App />);
await user.click(within(card("Алим")).getByRole("button", { name: /Сагсанд нэмэх/ }));
expect(within(card("Алим")).getByRole("button")).toBeDisabled();
expect(within(card("Талх")).getByRole("button")).toBeEnabled();
await within(card("Алим")).findByText(/сагсанд нэмэгдлээ/);
""",
                    ),
                    test(
                        "Үлдэгдлээс их тоо оруулахад серверийн алдаа гарч, захиалга үүсэхгүй",
                        """
const card = (name) =>
  screen.getAllByRole("article").find((item) => item.textContent.includes(name));
render(<App />);
const quantity = within(card("Бяслаг")).getByLabelText(/Тоо ширхэг/);
await user.clear(quantity);
await user.type(quantity, "10");
await user.click(within(card("Бяслаг")).getByRole("button", { name: /Сагсанд нэмэх/ }));
expect(await within(card("Бяслаг")).findByRole("alert")).toHaveTextContent(
  /үлдэгдэл хүрэлцэхгүй/i,
);
expect(api.get("orders")).toHaveLength(0);
""",
                    ),
                ),
                tips="""\
- `const [state, formAction, isPending] = useActionState(addToCart.bind(null, product.id), null);`
  — `bind` эхний аргументыг (`productId`) тогтооно, үлдсэн хоёрыг
  (`previousState`, `formData`) React өгнө.
- `<form action={formAction}>` — `onSubmit` хэрэггүй.
- Эхэндээ `state` нь `null` тул мэдэгдлийг `state && …` гэж шалгаж харуул.
  `state.ok` худал бол `<p role="alert">`.
- `useActionState` card бүрт тусдаа байгаа тул төлөв, мэдэгдэл нь бусад
  картад нөлөөлөхгүй.
""",
                solution=solution(
                    App_jsx="""\
import { useActionState } from "react";
import { addToCart } from "./actions";
import { products } from "./data";

function ProductCard({ product }) {
  const [state, formAction, isPending] = useActionState(addToCart.bind(null, product.id), null);

  return (
    <article style={{ border: "1px solid #d0d7de", borderRadius: 8, padding: 12 }}>
      <h2>
        {product.emoji} {product.name}
      </h2>
      <p>
        {product.price}₮ · үлдэгдэл {product.stock}
      </p>
      <form action={formAction}>
        <label>
          Тоо ширхэг{" "}
          <input name="quantity" type="number" defaultValue={1} style={{ width: 56 }} />
        </label>{" "}
        <button disabled={isPending}>{isPending ? "Нэмж байна…" : "Сагсанд нэмэх"}</button>
      </form>
      {state && (state.ok ? <p>✅ {state.message}</p> : <p role="alert">{state.message}</p>)}
    </article>
  );
}

export default function App() {
  return (
    <main style={{ display: "grid", gap: 12, maxWidth: 360 }}>
      <h1>🛒 Ногоон сагс</h1>
      {products.map((product) => (
        <ProductCard key={product.id} product={product} />
      ))}
    </main>
  );
}
"""
                ),
            ),
        ),
    ],
)
