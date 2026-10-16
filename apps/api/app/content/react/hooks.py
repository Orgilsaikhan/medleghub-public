"""Модул 6 — Hook-ууд.

Hook-ийн дүрэм, `useRef` (DOM ба утга хадгалах), `useMemo`, `useCallback`,
өөрийн hook бичих, `useLocalStorage`. Төгсгөлд нь `useFetch`, `useDebounce`,
`useWindowSize`-ээс бүрдсэн hook-ийн сан бүтээнэ.
"""

from app.content.react.common import solution, test, vite
from app.content.types import ExerciseSpec, LessonSpec, ModuleSpec
from app.models.enums import LessonLanguage

JSX = LessonLanguage.JSX

HOOKS = ModuleSpec(
    title="Модул 6 — Hook-ууд",
    description=(
        "Hook-ийн дүрэм, useRef, useMemo, useCallback-ийг сурч, өөрийн hook бичин "
        "дахин ашиглагдах hook-ийн сан бүтээнэ."
    ),
    lessons=[
        # ------------------------------------------------------------------
        LessonSpec(
            title="Hook-ийн дүрэм",
            slug="hook-durem",
            description="Hook-ийг яагаад зөвхөн дээд түвшинд, ижил дарааллаар дууддаг вэ.",
            duration=720,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Hook-ийн хоёр дүрмийг мэдэх
- React hook-уудыг **дуудсан дарааллаар** нь таньдгийг ойлгох
- Нөхцөл дотор болон эрт `return`-ийн дараа бичсэн hook-ийн алдааг засах

### Яагаад чухал вэ

Hook-ийн дүрэм зөрчсөн код эхэндээ хэвийн ажиллаж байгаа мэт харагддаг.
Гэтэл хэрэглэгч товч дармагц апп бүхэлдээ унаж, Console-д
`Rendered more hooks than during the previous render` гэсэн алдаа гарна.
Энэ алдааны учрыг ойлговол засах нь нэг минутын ажил.

### Hook гэж юу вэ

Hook бол `use`-ээр эхэлсэн функц: `useState`, `useEffect`, `useRef`,
`useContext`… Тэд component-ийг React-ийн боломжуудтай «холбодог» (hook —
дэгээ): state хадгалах, effect ажиллуулах, DOM-д хандах. Энэ модульд шинэ
hook-уудыг сурч, эцэст нь өөрийн hook бичнэ. Гэхдээ эхлээд бүх hook-д
хамаатай хоёр дүрэм.

### Дүрэм 1: Зөвхөн дээд түвшинд дуудна

Hook-ийг component-ийн биеийн **хамгийн дээд түвшинд**, ямар ч `return`-оос
өмнө дуудна. Нөхцөл, давталт, дотоод функц дотор дуудахгүй:

```jsx
function Profile({ user }) {
  const [open, setOpen] = useState(false); // ✅ дээд түвшинд

  if (user.isAdmin) {
    const [logs, setLogs] = useState([]);  // ❌ нөхцөл дотор
  }

  for (const item of user.items) {
    useEffect(() => {});                    // ❌ давталт дотор
  }

  function handleClick() {
    const inputRef = useRef(null);          // ❌ event handler дотор
  }

  if (!user.name) return null;
  const [tab, setTab] = useState("info");  // ❌ эрт return-ийн дараа
  // ...
}
```

### Дүрэм 2: Зөвхөн React функц дотор дуудна

Hook-ийг зөвхөн **function component** эсвэл **өөрийн hook** (custom hook,
энэ модулийн 6-р хичээл) дотор дуудна. Энгийн JavaScript функц, class
component дотор дуудахгүй.

### Яагаад: React hook-уудыг дарааллаар нь таньдаг

`useState(0)`-д нэр байхгүй. Тэгвэл React аль state нь аль нь болохыг яаж
мэддэг вэ? Хариу нь **дуудсан дараалал**. React component бүрт hook-уудын
жагсаалт хадгалдаг:

```jsx
function Form() {
  const [name, setName] = useState("Бат"); // 1-р hook → "Бат"
  const [age, setAge] = useState(17);       // 2-р hook → 17
  useEffect(() => {                         // 3-р hook → effect
    document.title = name;
  });
  // ...
}
```

Render бүрт React «1-р дуудлага бол нэр, 2-р нь нас, 3-р нь effect» гэж
жагсаалтаасаа тааруулна. Хэрэв нэг render-т аль нэг hook нөхцөлөөр
алгасагдвал түүний дараах бүх hook нэг байрлал урагшилна: `age`-ийн оронд
effect ирнэ гэх мэт. React үүнийг илрүүлээд алдаа шиднэ:

- `Rendered more hooks than during the previous render` — өмнөхөөсөө олон hook дуудсан;
- `Rendered fewer hooks than expected` — цөөн дуудсан;
- Console-д `React has detected a change in the order of Hooks` анхааруулга.

### Засах арга: нөхцөлийг hook-ийн дотор оруул

Hook-ийг үргэлж дуудаад, нөхцөлийг **дотор нь** шалгана:

```jsx
// ❌
if (isOpen) {
  useEffect(() => {
    document.title = "Нээлттэй";
  });
}

// ✅
useEffect(() => {
  if (isOpen) {
    document.title = "Нээлттэй";
  }
}, [isOpen]);
```

Эрт `return` хийх бол бүх hook-оо түүнээс **өмнө** дуудна:

```jsx
function Cart({ items }) {
  const [coupon, setCoupon] = useState(""); // ✅ эхлээд hook-ууд

  if (items.length === 0) {
    return <p>Сагс хоосон</p>;             // дараа нь эрт return
  }
  // ...
}
```

Тухайн render-т state хэрэггүй байсан ч hook-ийг дуудах нь зүгээр. Утгыг нь
ашиглахгүй л бол ямар ч асуудалгүй.

### Бодит төсөлд

Vite-ийн React загвар `eslint-plugin-react-hooks`-ийг агуулдаг. Түүний
`rules-of-hooks` дүрэм эдгээр алдааг код бичих үед нь, апп ажиллуулахаас
өмнө улаанаар тэмдэглэнэ. Энэ засварлагчид ESLint байхгүй тул алдааг
ажиллуулж байж л харна.

```quiz
Энэ component-д ямар алдаа байна вэ?

`function Timer({ running }) { if (!running) return null; const [s, setS] = useState(0); … }`
- [ ] `null` буцааж болохгүй
- [x] `running` өөрчлөгдөхөд hook-уудын тоо өөрчлөгдөж, React алдаа шиднэ
- [ ] `useState`-ийг component-ийн гадна дуудах ёстой
> `useState` нь эрт `return`-ийн дараа байгаа тул `running === false` үед дуудагдахгүй. Hook-ийг `return`-оос өмнө шилжүүлнэ.
```

```quiz
Аль нь hook-ийн дүрмийг зөрчөөгүй вэ?
- [ ] `if (user) { useEffect(…); }`
- [ ] `items.map(() => useState(0))`
- [x] `useEffect(() => { if (user) { … } }, [user]);`
- [ ] `function onClick() { useRef(null); }`
> Нөхцөл нь effect-ийн дотор байгаа тул `useEffect` өөрөө render бүрт ижил байрлалд дуудагдана.
```

### Дүгнэлт

Hook-ийг component эсвэл өөрийн hook-ийн дээд түвшинд, ямар ч нөхцөл,
давталт, эрт `return`-оос өмнө дуудна. React hook-уудыг дарааллаар нь
таньдаг тул дараалал render бүрт ижил байх ёстой. Нөхцөлийг hook-ийн дотор
оруул.
""",
            initial_code=vite(
                """\
import { useEffect, useState } from "react";

export default function App() {
  const [showDetails, setShowDetails] = useState(false);

  // ❌ Hook нөхцөл дотор
  if (showDetails) {
    useEffect(() => {
      document.title = "Алим — дэлгэрэнгүй";
    });
  }

  if (!showDetails) {
    return (
      <main>
        <h1>🍎 Алим</h1>
        <button onClick={() => setShowDetails(true)}>Дэлгэрэнгүй</button>
      </main>
    );
  }

  // ❌ Эрт return-ийн дараах hook
  const [qty, setQty] = useState(1);

  return (
    <main>
      <h1>🍎 Алим</h1>
      <p>Үнэ: 2800₮</p>
      <p>Тоо: {qty}</p>
      <button onClick={() => setQty(qty + 1)}>+</button>
      <p>Нийт: {2800 * qty}₮</p>
      <button onClick={() => setShowDetails(false)}>Хураах</button>
    </main>
  );
}
"""
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 8 минут

`App.jsx` эхэндээ хэвийн харагдана. «Хөтөч» дээр «Дэлгэрэнгүй» товч дараад
үзээрэй — апп унана. Хоёр hook дүрэм зөрчсөн байна. Тэдгээрийг засаж, апп-ын
ажиллагааг хэвээр үлдээ: дэлгэрэнгүй нээхэд хуудасны гарчиг
«Алим — дэлгэрэнгүй» болдог хэвээр байна.
""",
                tests=(
                    test(
                        "«Дэлгэрэнгүй» дарахад үнэ, тоо алдаагүй харагдана",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: "Дэлгэрэнгүй" }));
expect(screen.text()).toContain("Үнэ: 2800₮");
expect(screen.text()).toContain("Тоо: 1");
""",
                    ),
                    test(
                        "«+» товч тоо болон нийт үнийг нэмэгдүүлнэ",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: "Дэлгэрэнгүй" }));
await user.click(screen.getByRole("button", { name: "+" }));
await user.click(screen.getByRole("button", { name: "+" }));
expect(screen.text()).toContain("Тоо: 3");
expect(screen.text()).toContain("Нийт: 8400₮");
""",
                    ),
                    test(
                        "Хураагаад дахин нээхэд алдаа гарахгүй",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: "Дэлгэрэнгүй" }));
await user.click(screen.getByRole("button", { name: "Хураах" }));
expect(screen.queryByText("Үнэ: 2800₮")).toBeNull();
await user.click(screen.getByRole("button", { name: "Дэлгэрэнгүй" }));
expect(screen.text()).toContain("Үнэ: 2800₮");
""",
                    ),
                    test(
                        "Дэлгэрэнгүй нээхэд хуудасны гарчиг «Алим — дэлгэрэнгүй» болно",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: "Дэлгэрэнгүй" }));
expect(document.title).toBe("Алим — дэлгэрэнгүй");
""",
                    ),
                ),
                tips="""\
- Бүх `useState`, `useEffect`-ийг component-ийн эхэнд, `if (!showDetails) return …`-оос
  **өмнө** шилжүүл.
- `if (showDetails) { useEffect(…) }`-ийг эргүүлж бич: `useEffect`-ийг үргэлж дууд,
  `if`-ийг effect-ийн дотор оруул. Dependency-д `showDetails`-ийг бич.
- `qty` state хураасан үед ч хадгалагдаж байх нь асуудалгүй — ашиглахгүй л бол
  зүгээр.
""",
                solution=solution(
                    App_jsx="""\
import { useEffect, useState } from "react";

export default function App() {
  const [showDetails, setShowDetails] = useState(false);
  const [qty, setQty] = useState(1);

  useEffect(() => {
    document.title = showDetails ? "Алим — дэлгэрэнгүй" : "Дэлгүүр";
  }, [showDetails]);

  if (!showDetails) {
    return (
      <main>
        <h1>🍎 Алим</h1>
        <button onClick={() => setShowDetails(true)}>Дэлгэрэнгүй</button>
      </main>
    );
  }

  return (
    <main>
      <h1>🍎 Алим</h1>
      <p>Үнэ: 2800₮</p>
      <p>Тоо: {qty}</p>
      <button onClick={() => setQty(qty + 1)}>+</button>
      <p>Нийт: {2800 * qty}₮</p>
      <button onClick={() => setShowDetails(false)}>Хураах</button>
    </main>
  );
}
"""
                ),
            ),
        ),
        # ------------------------------------------------------------------
        LessonSpec(
            title="useRef: DOM-д хандах",
            slug="useref-dom",
            description="Ref-ээр input-д фокус өгөх, элемент рүү гүйлгэх, хэмжээг хэмжих.",
            duration=840,
            language=JSX,
            content="""\
### Энэ хичээлээр

- `useRef`-ээр DOM элементийг «барьж авах»
- Input-д фокус өгөх, элемент рүү гүйлгэх, хэмжээг нь хэмжих
- React 19-д ref-ийг өөрийн component руу prop болгон дамжуулах

### Яагаад чухал вэ

React-д DOM-ыг ихэвчлэн гараар өөрчилдөггүй: state өөрчлөгдөхөд React
дэлгэцийг өөрөө шинэчилнэ. Гэхдээ зарим үйлдлийг state-ээр илэрхийлж
болдоггүй: input-д курсор оруулах, жагсаалтын төгсгөл рүү гүйлгэх,
элементийн өргөнийг хэмжих, видео тоглуулах. Эдгээрт хөтчийн DOM API
(`focus()`, `scrollIntoView()`, `getBoundingClientRect()`) хэрэгтэй, тэгэхээр
DOM элемент өөрөө хэрэгтэй.

### useRef ба `ref` attribute

```jsx
import { useRef } from "react";

export default function Search() {
  const inputRef = useRef(null);

  function handleClick() {
    inputRef.current.focus();
  }

  return (
    <>
      <input ref={inputRef} placeholder="Хайх…" />
      <button onClick={handleClick}>🔍 Хайлт руу</button>
    </>
  );
}
```

1. `useRef(null)` нь `{ current: null }` гэсэн объект буцаана. Энэ объект
   render-ийн хооронд нэг л хэвээр байна.
2. `ref={inputRef}` нь React-д «энэ `<input>`-ийн DOM элементийг
   `inputRef.current`-д хий» гэж хэлнэ.
3. Товч дарахад `inputRef.current` бол жинхэнэ `<input>` элемент тул түүний
   `focus()`-ийг дуудна.

Элемент дэлгэцээс устахад React `current`-ийг буцааж `null` болгоно.

### `current` хэзээ бэлэн байх вэ

Render хийх үед DOM хараахан үүсээгүй байна. Тиймээс `ref.current`-ийг
render дотор биш, **event handler эсвэл effect** дотор ашиглана:

```jsx
function Banner() {
  const boxRef = useRef(null);

  // ❌ Энд эхний render-т boxRef.current нь null
  // const width = boxRef.current.offsetWidth;

  useEffect(() => {
    // ✅ DOM бэлэн болсны дараа ажиллана
    const { width, height } = boxRef.current.getBoundingClientRect();
    console.log(`Хэмжээ: ${width} × ${height}`);
  }, []);

  return <div ref={boxRef}>Хямдрал 20%</div>;
}
```

### Элемент рүү гүйлгэх

Чат, урт жагсаалт, «Дээш буцах» товчинд элемент рүү гүйлгэдэг:

```jsx
function Chat({ messages }) {
  const endRef = useRef(null);

  function scrollToEnd() {
    endRef.current.scrollIntoView({ behavior: "smooth" });
  }

  return (
    <>
      <ul>
        {messages.map((message) => (
          <li key={message.id}>{message.text}</li>
        ))}
      </ul>
      <div ref={endRef} />
      <button onClick={scrollToEnd}>⬇️ Сүүлийнх рүү</button>
    </>
  );
}
```

### Өөрийн component руу ref дамжуулах (React 19)

Ref-ийг `<input>` шиг HTML элементэд шууд өгдөг. Харин өөрийн component-д
өгвөл яах вэ? React 19-д function component `ref`-ийг **энгийн prop** шиг
хүлээж аваад, дотроо HTML элементэд дамжуулна:

```jsx
function TextField({ label, ref }) {
  return (
    <label>
      {label} <input ref={ref} />
    </label>
  );
}

function SignupForm() {
  const nameRef = useRef(null);
  return (
    <>
      <TextField label="Нэр" ref={nameRef} />
      <button onClick={() => nameRef.current.focus()}>Нэр засах</button>
    </>
  );
}
```

React 18 болон түүнээс өмнөх кодод үүнийг
`forwardRef(function TextField(props, ref) { … })`-ээр бичдэг байсан. Хуучин
төсөл, сангуудад олонтаа таарна — React 19-д шаардлагагүй болсон.

### Ref-ийг хэтрүүлж хэрэглэхгүй

Ref бол «зугтах гарц» (escape hatch). Текст солих, класс нэмэх, элемент
харуулах, нуухыг ref-ээр биш **state**-ээр хийнэ. React-ийн үүсгэсэн DOM-ыг
гараар устгаж, өөрчилбөл React-ийн мэдэж байгаа зүйлтэй зөрж, алдаа гарна.

```quiz
Энэ кодыг ажиллуулахад юу болох вэ?

`function Title() { const ref = useRef(null); return <h1 ref={ref}>{ref.current.textContent}</h1>; }`
- [ ] Хоосон `<h1>` харуулна
- [x] Алдаа гарна: эхний render-т `ref.current` нь `null`
- [ ] `<h1>`-ийн текстийг хоёр удаа харуулна
> Render хийх үед DOM хараахан үүсээгүй. `ref.current`-ийг зөвхөн event handler эсвэл effect дотор уншина.
```

### Дүгнэлт

`useRef(null)` ба `ref={…}` нь DOM элементийг `ref.current`-д өгнө.
Түүнийг event handler эсвэл effect дотор `focus()`, `scrollIntoView()`,
`getBoundingClientRect()` зэрэгт ашиглана. React 19-д өөрийн component
`ref`-ийг энгийн prop шиг авдаг.
""",
            initial_code=vite(
                """\
import { useState } from "react";
import MessageInput from "./MessageInput";

export default function App() {
  const [messages, setMessages] = useState(["Сайн байна уу! 👋"]);
  const [text, setText] = useState("");
  // TODO 1: мессежийн талбарт зориулж ref үүсгэ

  function handleWrite() {
    // TODO 2: талбарт фокус өг
  }

  function handleSubmit(event) {
    event.preventDefault();
    if (!text.trim()) return;
    setMessages([...messages, text.trim()]);
    setText("");
    // TODO 3: илгээсний дараа фокусыг талбар руу буцаа
  }

  return (
    <main>
      <h1>💬 Чат</h1>
      <ul>
        {messages.map((message, index) => (
          <li key={index}>{message}</li>
        ))}
      </ul>
      <button onClick={handleWrite}>✏️ Мессеж бичих</button>
      <form onSubmit={handleSubmit}>
        <MessageInput value={text} onChange={(event) => setText(event.target.value)} />{" "}
        <button>Илгээх</button>
      </form>
    </main>
  );
}
""",
                extra={
                    "MessageInput.jsx": """\
// TODO 4: ref-ийг prop болгон авч <input>-д холбо (React 19)
export default function MessageInput({ value, onChange }) {
  return (
    <label>
      Мессеж <input value={value} onChange={onChange} placeholder="Энд бичнэ үү…" />
    </label>
  );
}
"""
                },
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 10 минут

Жижиг чат бэлэн байна. «✏️ Мессеж бичих» товч дарах болон мессеж илгээх үед
курсор мессежийн талбарт очдог болго. Талбар нь `MessageInput` component
дотор байгаа тул ref-ийг түүнд дамжуулах хэрэгтэй.
""",
                tests=(
                    test(
                        "«Мессеж бичих» товч дарахад талбар фокустай болно",
                        """
render(<App />);
const input = screen.getByLabelText("Мессеж");
await user.click(screen.getByRole("button", { name: /Мессеж бичих/ }));
expect(input).toHaveFocus();
""",
                    ),
                    test(
                        "Илгээхэд мессеж жагсаалтад нэмэгдэж, талбар хоосорно",
                        """
render(<App />);
const input = screen.getByLabelText("Мессеж");
await user.type(input, "Маргааш уулзъя");
await user.click(screen.getByRole("button", { name: "Илгээх" }));
expect(screen.getAllByRole("listitem").at(-1)).toHaveTextContent("Маргааш уулзъя");
expect(input).toHaveValue("");
""",
                    ),
                    test(
                        "Илгээсний дараа фокус талбар руу буцна",
                        """
render(<App />);
const input = screen.getByLabelText("Мессеж");
await user.type(input, "Сайн уу");
await user.click(screen.getByRole("button", { name: "Илгээх" }));
expect(input).toHaveFocus();
""",
                    ),
                ),
                tips="""\
- `App` дотор `const inputRef = useRef(null);` үүсгээд
  `<MessageInput ref={inputRef} … />` гэж дамжуул.
- `MessageInput`-ийн параметрт `ref`-ийг бусад props-той хамт задлаад
  `<input ref={ref} … />` болго.
- Фокус өгөх нь `inputRef.current.focus()`.
- Товч дарахад фокус товч руу шилждэг. Тиймээс илгээсний дараа фокусыг handler
  дотроос буцааж талбарт өгөх ёстой.
""",
                solution=solution(
                    App_jsx="""\
import { useRef, useState } from "react";
import MessageInput from "./MessageInput";

export default function App() {
  const [messages, setMessages] = useState(["Сайн байна уу! 👋"]);
  const [text, setText] = useState("");
  const inputRef = useRef(null);

  function handleWrite() {
    inputRef.current.focus();
  }

  function handleSubmit(event) {
    event.preventDefault();
    if (!text.trim()) return;
    setMessages([...messages, text.trim()]);
    setText("");
    inputRef.current.focus();
  }

  return (
    <main>
      <h1>💬 Чат</h1>
      <ul>
        {messages.map((message, index) => (
          <li key={index}>{message}</li>
        ))}
      </ul>
      <button onClick={handleWrite}>✏️ Мессеж бичих</button>
      <form onSubmit={handleSubmit}>
        <MessageInput
          ref={inputRef}
          value={text}
          onChange={(event) => setText(event.target.value)}
        />{" "}
        <button>Илгээх</button>
      </form>
    </main>
  );
}
""",
                    MessageInput_jsx="""\
export default function MessageInput({ value, onChange, ref }) {
  return (
    <label>
      Мессеж <input ref={ref} value={value} onChange={onChange} placeholder="Энд бичнэ үү…" />
    </label>
  );
}
""",
                ),
            ),
        ),
        # ------------------------------------------------------------------
        LessonSpec(
            title="useRef: render хийлгэхгүй утга хадгалах",
            slug="useref-utga",
            description="Timer-ийн id, өмнөх утгыг ref-д хадгалах; ref, state, хувьсагчийн ялгаа.",
            duration=900,
            language=JSX,
            content="""\
### Энэ хичээлээр

- `useRef`-ийг render-үүдийн хооронд утга хадгалах «хайрцаг» болгон ашиглах
- Ref, state, энгийн хувьсагчийн ялгааг ойлгох
- Interval-ийн id, өмнөх утгыг ref-д хадгалах

### Яагаад чухал вэ

Зарим утгыг component санах ёстой ч дэлгэцэнд харуулдаггүй:
`setInterval`-ийн id, өмнөх утга, хэдэн удаа дарсан гэх мэт. Үүнийг
state-д хийвэл өөрчлөх бүрт дэмий render болно. Энгийн `let` хувьсагчид
хийвэл дараагийн render-т мартагдана. Ref яг энэ хоёрын дунд байдаг.

### Гурван сонголт

| | Render-ийн хооронд хадгалагдах уу | Өөрчлөхөд render хийх үү |
|---|---|---|
| `let` хувьсагч | ❌ render бүрт шинээр үүснэ | ❌ |
| `useState` | ✅ | ✅ |
| `useRef` | ✅ | ❌ |

Ref бол React-ийн хянадаггүй `{ current: … }` хайрцаг. Утгыг нь шууд
өөрчилнө: `ref.current = 5`. `setState` шиг функц хэрэггүй.

### Ref өөрчлөгдөхөд render хийгдэхгүй

```jsx
function Clicker() {
  const clicks = useRef(0);

  function handleClick() {
    clicks.current = clicks.current + 1;
    console.log("Дарсан:", clicks.current);
  }

  return <button onClick={handleClick}>Дар ({clicks.current})</button>;
}
```

Гурван удаа дарахад Console-д 1, 2, 3 гарна, харин товч дээр `Дар (0)`
хэвээр. Ref өөрчлөгдсөнийг React мэдэхгүй тул дахин render хийхгүй.

**Дүрэм:** дэлгэцэнд харагдах утга бол state, харагдахгүй утга бол ref.
Render хийх үед `ref.current`-ийг уншиж, бичихгүй — зөвхөн event handler,
effect дотор.

### Interval-ийн id хадгалах

`setInterval` нь id буцаадаг бөгөөд зогсоохдоо `clearInterval(id)` хэрэгтэй.
Тэгэхээр id-г render-ийн хооронд санах ёстой:

```jsx
const [seconds, setSeconds] = useState(0);
const intervalRef = useRef(null);

function start() {
  if (intervalRef.current !== null) return; // аль хэдийн явж байна
  intervalRef.current = setInterval(() => {
    setSeconds((s) => s + 1);
  }, 1000);
}

function stop() {
  clearInterval(intervalRef.current);
  intervalRef.current = null;
}
```

`setSeconds((s) => s + 1)` — interval-ийн callback нэг л удаа үүсдэг тул
функцэн шинэчлэлт (Модул 3) хэрэгтэй. Эс бөгөөс `seconds` үргэлж эхний
утгаа харна.

Энгийн `let intervalId` яагаад болохгүй вэ? `setSeconds` дуудагдах бүрт
component функц дахин ажиллаж, `let intervalId = null` шинээр үүснэ.
Хамгийн сүүлийн render-ийн `stop` нь `null`-ийг цэвэрлэх гээд interval
зогсохгүй.

### Өмнөх утгыг санах

Event handler дотор «өөрчлөхийн өмнөх» утгыг ref-д хадгалж болно:

```jsx
function PriceEditor() {
  const [price, setPrice] = useState(2800);
  const previousRef = useRef(null);

  function changePrice(next) {
    previousRef.current = price; // хуучин үнийг санана
    setPrice(next);
  }

  function undo() {
    if (previousRef.current !== null) {
      setPrice(previousRef.current);
      previousRef.current = null;
    }
  }
  // ...
}
```

`previousRef` өөрчлөгдөхөд дэмий render хийгдэхгүй — «Буцаах» дарах хүртэл
дэлгэцэнд хэрэггүй утга.

### Цэвэрлэгээ

Component устахад timer явсаар байвал effect-ийн цэвэрлэгээнд (Модул 5)
зогсооно:

```jsx
useEffect(() => {
  return () => clearInterval(intervalRef.current);
}, []);
```

```quiz
`Clicker`-ийн товчийг 3 удаа дарахад товч дээр юу гарах вэ?
- [x] `Дар (0)`
- [ ] `Дар (3)`
- [ ] `Дар (1)`
> `clicks.current` өөрчлөгдсөн ч React дахин render хийгээгүй тул товчны текст хуучнаараа үлдэнэ.
```

```quiz
Аль утгыг ref-д хадгалах нь зөв бэ?
- [ ] Сагсан дахь барааны тоо
- [x] `setTimeout`-ийн id
- [ ] Input-д бичиж буй текст
> Барааны тоо, текст дэлгэцэнд харагддаг тул state. Timer-ийн id харагддаггүй, зөвхөн цэвэрлэхэд хэрэгтэй.
```

### Дүгнэлт

Ref бол render-ийн хооронд хадгалагддаг ч өөрчлөгдөхөд render
хийлгэдэггүй хайрцаг. Timer-ийн id, өмнөх утга зэрэг дэлгэцэнд харагддаггүй
утгыг ref-д, харагддагийг state-д хадгална.
""",
            initial_code=vite(
                """\
import { useState } from "react";

export default function App() {
  const [tenths, setTenths] = useState(0); // секундийн аравны нэгүүд
  let intervalId = null; // ❌ render бүрт дахин null болно

  function handleStart() {
    intervalId = setInterval(() => {
      setTenths((t) => t + 1);
    }, 100);
  }

  function handleStop() {
    clearInterval(intervalId);
  }

  function handleReset() {
    // TODO: зогсоогоод 0 болго
  }

  return (
    <main>
      <h1>⏱️ Секундомер</h1>
      <p>Хугацаа: {(tenths / 10).toFixed(1)} с</p>
      <button onClick={handleStart}>Эхлүүлэх</button>{" "}
      <button onClick={handleStop}>Зогсоох</button>{" "}
      <button onClick={handleReset}>Тэглэх</button>
    </main>
  );
}
"""
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐ · 12 минут

Секундомер эхэлдэг ч зогсдоггүй. Шалтгаан нь interval-ийн id-г энгийн `let`
хувьсагчид хадгалсан явдал. Id-г ref-д хадгалж «Зогсоох», «Тэглэх» товчийг
ажилладаг болго. «Эхлүүлэх»-ийг дахин дарахад хоёр дахь interval үүсэх ёсгүй.
""",
                tests=(
                    test(
                        "«Эхлүүлэх» дарахад хугацаа гүйнэ",
                        """
const seconds = () => Number((screen.text().match(/Хугацаа: ([0-9]+[.][0-9])/) || [])[1]);
render(<App />);
expect(seconds()).toBe(0);
await user.click(screen.getByRole("button", { name: "Эхлүүлэх" }));
await act(async () => { await sleep(450); });
expect(seconds()).toBeGreaterThan(0);
""",
                    ),
                    test(
                        "«Зогсоох» дарахад хугацаа зогсоно",
                        """
const seconds = () => Number((screen.text().match(/Хугацаа: ([0-9]+[.][0-9])/) || [])[1]);
render(<App />);
await user.click(screen.getByRole("button", { name: "Эхлүүлэх" }));
await act(async () => { await sleep(350); });
await user.click(screen.getByRole("button", { name: "Зогсоох" }));
const stopped = seconds();
expect(stopped).toBeGreaterThan(0);
await act(async () => { await sleep(350); });
expect(seconds()).toBe(stopped);
""",
                    ),
                    test(
                        "«Тэглэх» дарахад 0.0 болж, цаг зогсоно",
                        """
const seconds = () => Number((screen.text().match(/Хугацаа: ([0-9]+[.][0-9])/) || [])[1]);
render(<App />);
await user.click(screen.getByRole("button", { name: "Эхлүүлэх" }));
await act(async () => { await sleep(300); });
await user.click(screen.getByRole("button", { name: "Тэглэх" }));
expect(seconds()).toBe(0);
await act(async () => { await sleep(300); });
expect(seconds()).toBe(0);
""",
                    ),
                    test(
                        "«Эхлүүлэх»-ийг давхар дарахад цаг хоёр дахин хурдан гүйхгүй",
                        """
const seconds = () => Number((screen.text().match(/Хугацаа: ([0-9]+[.][0-9])/) || [])[1]);
render(<App />);
const start = screen.getByRole("button", { name: "Эхлүүлэх" });
await user.click(start);
await user.click(start);
await act(async () => { await sleep(600); });
await user.click(screen.getByRole("button", { name: "Зогсоох" }));
expect(seconds()).toBeGreaterThan(0);
expect(seconds()).toBeLessThanOrEqual(0.7);
""",
                    ),
                ),
                tips="""\
- `let intervalId = null;`-ийг `const intervalRef = useRef(null);` болго. Id-г
  `intervalRef.current`-д хадгал.
- `handleStart`-ийн эхэнд `intervalRef.current !== null` бол юу ч хийлгүй буц —
  эс бөгөөс хоёр interval зэрэг явж, цаг хоёр дахин хурдан гүйнэ.
- `handleStop`: `clearInterval(intervalRef.current)`, дараа нь
  `intervalRef.current = null` — ингэвэл дахин эхлүүлж болно.
- `handleReset`: эхлээд зогсоо, дараа нь `setTenths(0)`.
""",
                solution=solution(
                    App_jsx="""\
import { useEffect, useRef, useState } from "react";

export default function App() {
  const [tenths, setTenths] = useState(0);
  const intervalRef = useRef(null);

  function handleStart() {
    if (intervalRef.current !== null) return;
    intervalRef.current = setInterval(() => {
      setTenths((t) => t + 1);
    }, 100);
  }

  function handleStop() {
    clearInterval(intervalRef.current);
    intervalRef.current = null;
  }

  function handleReset() {
    handleStop();
    setTenths(0);
  }

  useEffect(() => {
    return () => clearInterval(intervalRef.current);
  }, []);

  return (
    <main>
      <h1>⏱️ Секундомер</h1>
      <p>Хугацаа: {(tenths / 10).toFixed(1)} с</p>
      <button onClick={handleStart}>Эхлүүлэх</button>{" "}
      <button onClick={handleStop}>Зогсоох</button>{" "}
      <button onClick={handleReset}>Тэглэх</button>
    </main>
  );
}
"""
                ),
            ),
        ),
        # ------------------------------------------------------------------
        LessonSpec(
            title="useMemo: тооцооллыг кэшлэх",
            slug="usememo",
            description="Үнэтэй тооцооллыг dependency өөрчлөгдөх үед л дахин хийх.",
            duration=900,
            language=JSX,
            content="""\
### Энэ хичээлээр

- `useMemo`-оор үнэтэй тооцооллын үр дүнг render-ийн хооронд кэшлэх
- Dependency массив хэзээ дахин тооцоолуулдгийг ойлгох
- `useMemo` хэзээ хэрэгтэй, хэзээ илүүц болохыг ялгах

### Яагаад чухал вэ

Component render хийх бүрт түүний бүх код дахин ажилладаг. 5000 барааг
шүүж, эрэмбэлэх тооцоо хайлтын үг өөрчлөгдөхөд ажиллах нь зөв. Гэтэл
өдөр/шөнийн горим солиход ч дахин ажиллавал дэмий — жагсаалт огт
өөрчлөгдөөгүй шүү дээ. Удаан тооцоо ингэж давтагдвал апп гацаж байгаа мэт
санагдана.

### useMemo

```jsx
import { useMemo, useState } from "react";

function ProductTable({ products }) {
  const [query, setQuery] = useState("");
  const [dark, setDark] = useState(false);

  const visible = useMemo(
    () => products.filter((p) => p.name.includes(query)),
    [products, query],
  );
  // ...
}
```

`useMemo(тооцоолох функц, dependency)`:

1. Эхний render-т функцийг ажиллуулж, үр дүнг хадгална.
2. Дараагийн render-т dependency бүрийг өмнөхтэй нь `Object.is`-ээр
   харьцуулна.
3. Бүгд ижил бол хадгалсан үр дүнг шууд буцаана. Аль нэг нь өөрчлөгдсөн бол
   функцийг дахин ажиллуулна.

Дээрх жишээнд `dark` өөрчлөгдөхөд шүүлт дахин ажиллахгүй.

### Dependency-г бүрэн бич

Тооцоонд ашигласан component-ийн **бүх** утгыг (props, state, тэднээс
гаргасан хувьсагч) dependency-д бичнэ. Мартвал хуучирсан үр дүн буцаана:

```jsx
// ❌ sortBy өөрчлөгдөхөд дахин эрэмбэлэхгүй
const sorted = useMemo(() => sortProducts(products, sortBy), [products]);

// ✅
const sorted = useMemo(() => sortProducts(products, sortBy), [products, sortBy]);
```

Бодит төсөлд ESLint-ийн `react-hooks/exhaustive-deps` дүрэм дутуу
dependency-г сануулна — Модул 5-ын `useEffect`-тэй яг адил.

### Эхлээд хэмж

`useMemo` бол гүйцэтгэлийн оновчлол. Тооцоо үнэхээр удаан эсэхийг эхлээд
хэмж:

```jsx
const started = performance.now();
const visible = filterProducts(products, query);
console.log("Шүүлт:", (performance.now() - started).toFixed(1), "мс");
```

Ойролцоогоор 1 мс-ээс удаан бол кэшлэх нь утгатай. Хоёр тоо нэмэх, 20
элементтэй массив шүүхэд `useMemo` хэрэггүй: hook өөрөө бага ч гэсэн
зардалтай, код уншихад хэцүү болно.

### Хэзээ хэрэглэх вэ

- Мэдэгдэхүйц удаан тооцоо: том жагсаалт шүүх, эрэмбэлэх, статистик.
- Үр дүнг `memo`-той хүүхэд component-д дамжуулах үед (дараагийн хичээл,
  Модул 12).
- Үр дүн өөр hook-ийн dependency болох үед (жишээ нь `useEffect`).

`useMemo` кодын **үр дүнг** өөрчлөх ёсгүй: түүнийг арилгахад апп удаан ч
гэсэн зөв ажиллах ёстой. React шаардлагатай үед кэшээ хаяж болно. React
Compiler (Модул 11) ийм кэшлэлтийг автоматаар хийж чаддаг ч `useMemo`-г
мэдэх хэрэгтэй — олон төсөл түүнийг ашигладаг.

```quiz
`const total = useMemo(() => sum(prices), []);` — `prices` шинэчлэгдэхэд `total` юу болох вэ?
- [ ] Шинэ `prices`-аар дахин тооцоологдоно
- [x] Хуучин утгаараа үлдэнэ
- [ ] Алдаа гарна
> Dependency массив хоосон тул React эхний үр дүнгээ үргэлж буцаана. `[prices]` гэж бичих ёстой.
```

```quiz
Аль тохиолдолд `useMemo` хамгийн их ашиг өгөх вэ?
- [ ] `const fullName = firstName + " " + lastName;`
- [x] 10 000 мөртэй хүснэгтийг шүүж, эрэмбэлэх
- [ ] `const isEmpty = items.length === 0;`
> Хурдан тооцоонд `useMemo` хэрэггүй. Том өгөгдөл шүүх, эрэмбэлэх нь кэшлэх үнэ цэнэтэй.
```

### Дүгнэлт

`useMemo` нь dependency өөрчлөгдөөгүй үед өмнөх тооцооны үр дүнг буцааж,
дэмий тооцоолохоос сэргийлнэ. Тооцоонд ашигласан бүх утгыг dependency-д
бич, удаан эсэхийг нь эхлээд хэмж.
""",
            initial_code=vite(
                """\
import { useState } from "react";
import { filterProducts, products } from "./products";

export default function App() {
  const [query, setQuery] = useState("");
  const [sortBy, setSortBy] = useState("default");
  const [dark, setDark] = useState(false);

  // TODO: зөвхөн query эсвэл sortBy өөрчлөгдөхөд дахин тооцоол
  const visible = filterProducts(products, query, sortBy);

  return (
    <main
      style={{
        padding: 16,
        background: dark ? "#1f2328" : "#ffffff",
        color: dark ? "#f0f3f6" : "#1f2328",
      }}
    >
      <h1>📦 Агуулах</h1>
      <button onClick={() => setDark(!dark)}>
        {dark ? "☀️ Өдрийн горим" : "🌙 Шөнийн горим"}
      </button>
      <p>
        <label>
          Хайх <input value={query} onChange={(event) => setQuery(event.target.value)} />
        </label>{" "}
        <label>
          Эрэмбэ{" "}
          <select value={sortBy} onChange={(event) => setSortBy(event.target.value)}>
            <option value="default">Анхны дарааллаар</option>
            <option value="price">Үнээр</option>
          </select>
        </label>
      </p>
      <p>Олдсон: {visible.length}</p>
      <ul>
        {visible.slice(0, 20).map((product) => (
          <li key={product.id}>
            {product.name} — {product.price}₮
          </li>
        ))}
      </ul>
    </main>
  );
}
""",
                locked={
                    "products.js": """\
const names = ["Алим", "Банана", "Жүрж", "Лууван", "Төмс", "Брокколи", "Сүү", "Бяслаг", "Талх", "Өндөг"];

// 5000 бараа — жинхэнэ дэлгүүрийн агуулах шиг
export const products = Array.from({ length: 5000 }, (_, index) => ({
  id: index + 1,
  name: `${names[index % names.length]} #${index + 1}`,
  price: 500 + ((index * 7919) % 20000),
}));

// Хэдэн удаа ажилласныг тоолно
export const stats = { calls: 0 };

export function filterProducts(list, query, sortBy) {
  stats.calls += 1;
  const started = performance.now();
  const text = query.trim().toLowerCase();
  let result = list.filter((product) => product.name.toLowerCase().includes(text));
  if (sortBy === "price") {
    result = [...result].sort((a, b) => a.price - b.price);
  }
  // Зориуд удаашруулна — «үнэтэй» тооцоо
  while (performance.now() - started < 15) {
    // хүлээнэ
  }
  console.log(`filterProducts ажиллалаа (${stats.calls}-р удаа)`);
  return result;
}
"""
                },
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 10 минут

Агуулахад 5000 бараа бий. `filterProducts` зориуд удаан бөгөөд ажиллах
бүртээ Console-д бичдэг. Одоо горим солих товч дарахад ч шүүлт дахин
ажиллаж байна — Console-оос хараарай. `useMemo`-оор шүүлтийг зөвхөн хайлт
эсвэл эрэмбэ өөрчлөгдөхөд ажилладаг болго.
""",
                tests=(
                    test(
                        "Горим солиход шүүлт дахин ажиллахгүй",
                        """
const { stats } = mod("./products");
render(<App />);
const before = stats.calls;
await user.click(screen.getByRole("button", { name: /горим/ }));
await user.click(screen.getByRole("button", { name: /горим/ }));
expect(stats.calls).toBe(before);
""",
                    ),
                    test(
                        "Хайлт өөрчлөгдөхөд жагсаалт дахин шүүгдэнэ",
                        """
const { stats } = mod("./products");
render(<App />);
const before = stats.calls;
await user.type(screen.getByLabelText("Хайх"), "Жүрж");
expect(stats.calls).toBeGreaterThan(before);
expect(screen.text()).toContain("Олдсон: 500");
const items = screen.getAllByRole("listitem");
expect(items.every((item) => item.textContent.includes("Жүрж"))).toBe(true);
""",
                    ),
                    test(
                        "Эрэмбэ өөрчлөгдөхөд жагсаалт үнээр эрэмбэлэгдэнэ",
                        """
const { products } = mod("./products");
const cheapest = products
  .filter((product) => product.name.includes("Сүү"))
  .sort((a, b) => a.price - b.price)[0];
render(<App />);
await user.type(screen.getByLabelText("Хайх"), "Сүү");
await user.selectOptions(screen.getByLabelText("Эрэмбэ"), "price");
expect(screen.getAllByRole("listitem")[0]).toHaveTextContent(`${cheapest.name} — ${cheapest.price}₮`);
""",
                    ),
                ),
                tips="""\
- `const visible = useMemo(() => filterProducts(products, query, sortBy), [...]);`
- Функц дотор ашигласан бүх утгыг dependency-д бич. `products` нь
  component-ийн гадна, модулийн түвшинд зарлагдсан тул хэзээ ч өөрчлөгдөхгүй —
  бичсэн ч, бичээгүй ч болно.
- `dark`-ийг dependency-д бичвэл горим солиход дахин тооцоолно — яг
  зайлсхийх гэсэн зүйл.
""",
                solution=solution(
                    App_jsx="""\
import { useMemo, useState } from "react";
import { filterProducts, products } from "./products";

export default function App() {
  const [query, setQuery] = useState("");
  const [sortBy, setSortBy] = useState("default");
  const [dark, setDark] = useState(false);

  const visible = useMemo(() => filterProducts(products, query, sortBy), [query, sortBy]);

  return (
    <main
      style={{
        padding: 16,
        background: dark ? "#1f2328" : "#ffffff",
        color: dark ? "#f0f3f6" : "#1f2328",
      }}
    >
      <h1>📦 Агуулах</h1>
      <button onClick={() => setDark(!dark)}>
        {dark ? "☀️ Өдрийн горим" : "🌙 Шөнийн горим"}
      </button>
      <p>
        <label>
          Хайх <input value={query} onChange={(event) => setQuery(event.target.value)} />
        </label>{" "}
        <label>
          Эрэмбэ{" "}
          <select value={sortBy} onChange={(event) => setSortBy(event.target.value)}>
            <option value="default">Анхны дарааллаар</option>
            <option value="price">Үнээр</option>
          </select>
        </label>
      </p>
      <p>Олдсон: {visible.length}</p>
      <ul>
        {visible.slice(0, 20).map((product) => (
          <li key={product.id}>
            {product.name} — {product.price}₮
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
            title="useCallback: функцийг тогтвортой байлгах",
            slug="usecallback",
            description="Функцийг render-ийн хооронд ижил байлгаж, memo хүүхдийн дэмий render-ийг арилгах.",
            duration=900,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Render бүрт функц шинээр үүсдгийг ойлгох
- `useCallback`-ээр функцийг render-ийн хооронд ижил байлгах
- `memo`-той хүүхэдтэй хамт хэрэглэж, dependency-г зөв бичих

### Яагаад чухал вэ

Том жагсаалттай хүүхэд component-ийг `memo`-оор ороовол props нь
өөрчлөгдөөгүй үед дахин render хийхгүй. Гэтэл эцэг нь түүнд функц
дамжуулдаг бол энэ оновчлол ажиллахаа больчихдог. Яагаад гэдгийг ойлгох нь
`useCallback`-ийн гол санаа.

### Функц render бүрт шинэ

```jsx
function App() {
  function handleAdd(product) {
    // ...
  } // render бүрт ШИНЭ функц

  return <ProductList onAdd={handleAdd} />;
}
```

JavaScript-д хоёр функц ижил кодтой байсан ч өөр объект:
`(() => {}) === (() => {})` нь `false`. `App` render хийх бүрт
`handleAdd` шинэ функц болно.

### memo товчхон

```jsx
import { memo } from "react";

const ProductList = memo(function ProductList({ products, onAdd }) {
  console.log("ProductList render");
  // ...
});
```

`memo` нь шинэ props-ийг өмнөхтэй нь нэг бүрчлэн (`Object.is`-ээр)
харьцуулж, бүгд ижил бол render-ийг алгасна. Дэлгэрэнгүйг Модул 12-т үзнэ.
Харин `onAdd` render бүрт шинэ функц бол «өөрчлөгдсөн» гэж тооцогдож, `memo`
дэмий болно.

### useCallback

```jsx
import { useCallback } from "react";

const handleAdd = useCallback((product) => {
  setCart((cart) => [...cart, product]);
}, []);
```

`useCallback(функц, dependency)` нь dependency өөрчлөгдөөгүй бол **өмнөх
яг тэр функцийг** буцаана. Одоо `ProductList` ижил `onAdd` авч, дахин
render хийхгүй. Үнэндээ `useCallback(fn, deps)` бол
`useMemo(() => fn, deps)`-тэй адил — тооцооны үр дүнгийн оронд функцийг
кэшлэдэг.

### Dependency ба хуучирсан утга

Функц дотор ашигласан state, props-ийг dependency-д бичнэ. Мартвал функц
эхний render-ийн утгыг үүрд «санаж» үлдэнэ (stale closure):

```jsx
// ❌ discount өөрчлөгдсөн ч хуучин хөнгөлөлтөөр тооцно
const handleAdd = useCallback((product) => {
  setCart((cart) => [...cart, { ...product, price: product.price - discount }]);
}, []);

// ✅
const handleAdd = useCallback((product) => {
  setCart((cart) => [...cart, { ...product, price: product.price - discount }]);
}, [discount]);
```

`setCart((cart) => …)` шиг функцэн шинэчлэлт хэрэглэвэл `cart`-ийг
dependency-д бичих шаардлагагүй. Dependency цөөн байх тусам функц илүү
тогтвортой. `useState`-ийн `setX` функцүүд өөрсдөө үргэлж ижил байдаг.

### Хэзээ хэрэгтэй вэ

- Функцийг `memo`-той хүүхэд component-д дамжуулах үед.
- Функц өөр hook-ийн dependency болох үед: `useEffect(…, [onLoad])`.
- Өөрийн hook-оос функц буцаах үед (дараагийн хичээл).

Бусад үед `useCallback` хурд нэмэхгүй: `memo`-гүй хүүхэд эцэгтэйгээ хамт
ямар ч байсан render хийнэ.

```quiz
Энэ кодод ямар алдаа байна вэ?

`const [qty, setQty] = useState(1); const add = useCallback((p) => addToCart(p, qty), []);`
- [ ] `useCallback`-д хоосон массив өгч болохгүй
- [x] `qty` dependency-д байхгүй тул `add` үргэлж `qty = 1`-ээр ажиллана
- [ ] Алдаа байхгүй
> Хоосон dependency-тэй функц эхний render-ийн `qty`-г «санана». `[qty]` гэж бичнэ.
```

### Дүгнэлт

Функц render бүрт шинээр үүсдэг тул `memo`-той хүүхдийн оновчлолыг
эвддэг. `useCallback` функцийг dependency өөрчлөгдөх хүртэл ижил
байлгана. Функц доторх бүх state, props-ийг dependency-д бич.
""",
            initial_code=vite(
                """\
import { useState } from "react";
import ProductList from "./ProductList";
import { products } from "./products";

export default function App() {
  const [cart, setCart] = useState([]);
  const [qty, setQty] = useState(1);
  const [note, setNote] = useState("");

  // TODO: useCallback-аар ороож, зөв dependency өг
  function handleAdd(product) {
    setCart((current) => [...current, { name: product.name, qty }]);
  }

  return (
    <main>
      <h1>🛍️ Дэлгүүр</h1>
      <label>
        Тоо ширхэг{" "}
        <select value={qty} onChange={(event) => setQty(Number(event.target.value))}>
          {[1, 2, 3, 4, 5].map((n) => (
            <option key={n} value={n}>
              {n}
            </option>
          ))}
        </select>
      </label>
      <ProductList products={products} onAdd={handleAdd} />
      <h2>Сагс</h2>
      <ul>
        {cart.map((item, index) => (
          <li key={index}>
            {item.name} × {item.qty}
          </li>
        ))}
      </ul>
      <label>
        Захиалгын тэмдэглэл{" "}
        <input value={note} onChange={(event) => setNote(event.target.value)} />
      </label>
    </main>
  );
}
""",
                locked={
                    "ProductList.jsx": """\
import { memo } from "react";

function ProductList({ products, onAdd }) {
  console.log("ProductList render");
  return (
    <ul>
      {products.map((product) => (
        <li key={product.id}>
          {product.emoji} {product.name} — {product.price}₮{" "}
          <button aria-label={`${product.name} нэмэх`} onClick={() => onAdd(product)}>
            Нэмэх
          </button>
        </li>
      ))}
    </ul>
  );
}

// memo: props өөрчлөгдөөгүй бол дахин render хийхгүй
export default memo(ProductList);
""",
                    "products.js": """\
export const products = [
  { id: 1, name: "Алим", price: 2800, emoji: "🍎" },
  { id: 2, name: "Банана", price: 3500, emoji: "🍌" },
  { id: 3, name: "Сүү", price: 3200, emoji: "🥛" },
  { id: 4, name: "Талх", price: 2500, emoji: "🍞" },
];
""",
                },
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐ · 12 минут

`ProductList` нь `memo`-той бөгөөд render хийх бүртээ Console-д бичдэг.
Захиалгын тэмдэглэл бичихэд үсэг бүрт `ProductList` дахин render хийж
байна — Console-оос хараарай. `handleAdd`-ийг `useCallback`-ээр засаж,
дэмий render-ийг арилга. Сонгосон тоо ширхэг зөв хэрэглэгдсээр байх ёстой.
""",
                tests=(
                    test(
                        "«Нэмэх» дарахад бараа сагсанд нэмэгдэнэ",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: "Алим нэмэх" }));
expect(screen.text()).toContain("Алим × 1");
""",
                    ),
                    test(
                        "Тэмдэглэл бичихэд ProductList дахин render хийхгүй",
                        """
const renders = () => logs.filter((entry) => entry.text.includes("ProductList render")).length;
render(<App />);
const before = renders();
await user.type(screen.getByLabelText("Захиалгын тэмдэглэл"), "Хурдан");
expect(renders()).toBe(before);
""",
                    ),
                    test(
                        "Тоо ширхэг өөрчилсний дараа шинэ тоогоор нэмнэ",
                        """
render(<App />);
await user.selectOptions(screen.getByLabelText("Тоо ширхэг"), "3");
await user.click(screen.getByRole("button", { name: "Сүү нэмэх" }));
expect(screen.text()).toContain("Сүү × 3");
""",
                    ),
                ),
                tips="""\
- `function handleAdd(product) {…}`-ийг
  `const handleAdd = useCallback((product) => {…}, [...]);` болго.
- Функц `qty`-г ашигладаг тул dependency-д бич. Тоо ширхэг өөрчлөгдөхөд
  `ProductList` дахин render хийх нь зөв, тэмдэглэл бичихэд — буруу.
- `cart`-ийг `setCart((current) => …)`-ээр шинэчилж байгаа тул dependency-д
  хэрэггүй.
""",
                solution=solution(
                    App_jsx="""\
import { useCallback, useState } from "react";
import ProductList from "./ProductList";
import { products } from "./products";

export default function App() {
  const [cart, setCart] = useState([]);
  const [qty, setQty] = useState(1);
  const [note, setNote] = useState("");

  const handleAdd = useCallback(
    (product) => {
      setCart((current) => [...current, { name: product.name, qty }]);
    },
    [qty],
  );

  return (
    <main>
      <h1>🛍️ Дэлгүүр</h1>
      <label>
        Тоо ширхэг{" "}
        <select value={qty} onChange={(event) => setQty(Number(event.target.value))}>
          {[1, 2, 3, 4, 5].map((n) => (
            <option key={n} value={n}>
              {n}
            </option>
          ))}
        </select>
      </label>
      <ProductList products={products} onAdd={handleAdd} />
      <h2>Сагс</h2>
      <ul>
        {cart.map((item, index) => (
          <li key={index}>
            {item.name} × {item.qty}
          </li>
        ))}
      </ul>
      <label>
        Захиалгын тэмдэглэл{" "}
        <input value={note} onChange={(event) => setNote(event.target.value)} />
      </label>
    </main>
  );
}
"""
                ),
            ),
        ),
        # ------------------------------------------------------------------
        LessonSpec(
            title="Өөрийн hook бичих",
            slug="custom-hook",
            description="Давтагдсан логикийг useToggle, useCounter шиг өөрийн hook болгон гаргах.",
            duration=900,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Давтагдсан hook-той логикийг өөрийн hook болгон салгах
- `use`-ээр эхэлдэг нэршлийн дүрэм, түүний учрыг ойлгох
- Custom hook **логик** хуваалцдаг, **state** биш гэдгийг мэдэх

### Яагаад чухал вэ

Олон component-д ижил `useState` ба handler давтагддаг: нээх/хаах,
тоологч, форм, өгөгдөл татах. Хуулж тавьсан кодыг засахдаа бүх газарт нь
засах хэрэгтэй болно. Давтагдсан кодыг функц болгон гаргадагтай адил,
hook-той логик давтагдвал **өөрийн hook** болгон гаргана.

### Жишээ: useToggle

```jsx
// useToggle.js
import { useState } from "react";

export function useToggle(initialValue = false) {
  const [on, setOn] = useState(initialValue);

  function toggle() {
    setOn((value) => !value);
  }

  return [on, toggle];
}
```

```jsx
// Faq.jsx
import { useToggle } from "./useToggle";

export default function Faq({ question, answer }) {
  const [open, toggleOpen] = useToggle();
  return (
    <div>
      <button onClick={toggleOpen}>{question}</button>
      {open && <p>{answer}</p>}
    </div>
  );
}
```

Custom hook бол **дотроо hook дууддаг энгийн функц**. Шинэ ид шид
байхгүй: `useToggle()` дуудахад түүний доторх `useState` яг `Faq`-ийн биед
бичсэн мэт ажиллана.

### Нэршил: `use`-ээр эхэлнэ

Hook-ийн нэр `use` + том үсэг: `useToggle`, `useCounter`, `useFetch`. Энэ
зүгээр нэг заншил биш:

- React болон ESLint нэрээр нь hook гэж таньж, hook-ийн дүрмийг шалгана.
- Уншигч `use…` гэж харвал дотор нь state, effect байж болохыг шууд мэднэ.

Эсрэгээр, hook дууддаггүй функцийг `use`-ээр нэрлэхгүй: `formatPrice`,
`getTotal` бол энгийн функц. Custom hook-д ч hook-ийн дүрэм үйлчилнэ:
түүнийг нөхцөл дотор дуудахгүй.

### Логик хуваалцана, state биш

```jsx
function Settings() {
  const [sound, toggleSound] = useToggle(true);
  const [dark, toggleDark] = useToggle(false);
  // sound, dark — хоорондоо хамааралгүй хоёр state
}
```

Hook-ийг дуудах бүр **шинэ, бие даасан** state үүсгэнэ — `useState`-ийг
хоёр удаа дуудсантай адил. Хоёр component нэг hook ашигладаг ч state-ээ
хуваалцахгүй. State хуваалцах бол түүнийг дээш өргөх эсвэл Context
хэрэглэнэ (Модул 7).

### Юу буцаах вэ

- **Массив** `[on, toggle]` — `useState` шиг, хоёр утгатай үед тохиромжтой.
  Хэрэглэгч нэрийг өөрөө өгнө: `const [sound, toggleSound] = useToggle()`.
- **Объект** `{ count, increment, reset }` — утга олон үед. Нэрээр нь авна:
  `counter.increment()`.

### Бодит төсөлд

Hook-уудыг ихэвчлэн `src/hooks/` хавтаст, файл бүрт нэгээр хадгална:
`src/hooks/useToggle.js`. Бэлэн hook-уудын сан ч бий (`usehooks-ts`,
`@uidotdev/usehooks`), гэхдээ эхлээд өөрөө бичиж сурах нь чухал.

```quiz
`Faq` component хуудсан дээр хоёр удаа гарсан. Нэгнийх нь товч дарахад нөгөө нь нээгдэх үү?
- [ ] Тийм — хоёулаа нэг `useToggle` ашигладаг
- [x] Үгүй — hook-ийг дуудах бүр бие даасан state үүсгэнэ
- [ ] Алдаа гарна
> Custom hook логикийг хуваалцдаг. State нь component бүрт тусдаа.
```

```quiz
Аль функцийг `use`-ээр нэрлэх ёстой вэ?
- [ ] `function getTotal(items) { return items.length; }`
- [x] `function useOnline() { const [online, setOnline] = useState(true); … }`
- [ ] `function formatPrice(n) { return n + "₮"; }`
> Дотроо hook дууддаг функц л hook. Бусад нь энгийн функц хэвээр.
```

### Дүгнэлт

Давтагдсан hook-той логикийг `use`-ээр эхэлсэн функц болгон гаргана.
Custom hook дотроо ямар ч hook дуудаж болох бөгөөд hook-ийн дүрэм түүнд ч
хамаатай. Дуудах бүр шинэ state үүсгэдэг: логик хуваалцагдана, state биш.
""",
            initial_code=vite(
                """\
import { useState } from "react";

// Хоёр тоологч яг ижил логиктой — давхардсан код.
export default function App() {
  const [adults, setAdults] = useState(1);
  const [kids, setKids] = useState(0);

  const total = adults * 15000 + kids * 8000;

  return (
    <main>
      <h1>🎟️ Кино тасалбар</h1>
      <p>
        Том хүн: {adults}{" "}
        <button onClick={() => setAdults(Math.max(0, adults - 1))}>Том хүн −</button>{" "}
        <button onClick={() => setAdults(adults + 1)}>Том хүн +</button>
      </p>
      <p>
        Хүүхэд: {kids}{" "}
        <button onClick={() => setKids(Math.max(0, kids - 1))}>Хүүхэд −</button>{" "}
        <button onClick={() => setKids(kids + 1)}>Хүүхэд +</button>
      </p>
      <p>Нийт: {total}₮</p>
      <button
        onClick={() => {
          setAdults(1);
          setKids(0);
        }}
      >
        Цэвэрлэх
      </button>
    </main>
  );
}
""",
                extra={
                    "useCounter.js": """\
import { useState } from "react";

// TODO: count state болон increment, decrement, reset функцүүдийг
// объект болгон буцаа. Тоо 0-ээс доош буухгүй.
export function useCounter(initialValue = 0) {
  return {
    count: initialValue,
    increment() {},
    decrement() {},
    reset() {},
  };
}
"""
                },
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 12 минут

`App.jsx`-д хоёр тоологч яг ижил логиктой давхардсан байна. `useCounter.js`-д
`useCounter(initialValue)` hook бич: `{ count, increment, decrement, reset }`
объект буцаана, тоо 0-ээс доош буухгүй. Дараа нь `App`-ыг энэ hook-оор дахин
бич — давхардал алга болно.
""",
                tests=(
                    test(
                        "useCounter анхны утгаас эхэлж, нэмж, хасна",
                        """
const m = mod("./useCounter");
const useCounter = m.useCounter ?? m.default;
function Probe() {
  const counter = useCounter(5);
  return (
    <div>
      <p>Утга: {counter.count}</p>
      <button onClick={() => counter.increment()}>нэмэх</button>
      <button onClick={() => counter.decrement()}>хасах</button>
    </div>
  );
}
render(<Probe />);
expect(screen.text()).toContain("Утга: 5");
await user.click(screen.getByRole("button", { name: "нэмэх" }));
expect(screen.text()).toContain("Утга: 6");
await user.click(screen.getByRole("button", { name: "хасах" }));
await user.click(screen.getByRole("button", { name: "хасах" }));
expect(screen.text()).toContain("Утга: 4");
""",
                    ),
                    test(
                        "reset анхны утга руу буцаана",
                        """
const m = mod("./useCounter");
const useCounter = m.useCounter ?? m.default;
function Probe() {
  const counter = useCounter(2);
  return (
    <div>
      <p>Утга: {counter.count}</p>
      <button onClick={() => counter.increment()}>нэмэх</button>
      <button onClick={() => counter.reset()}>тэглэх</button>
    </div>
  );
}
render(<Probe />);
await user.click(screen.getByRole("button", { name: "нэмэх" }));
await user.click(screen.getByRole("button", { name: "нэмэх" }));
expect(screen.text()).toContain("Утга: 4");
await user.click(screen.getByRole("button", { name: "тэглэх" }));
expect(screen.text()).toContain("Утга: 2");
""",
                    ),
                    test(
                        "Тоо 0-ээс доош буухгүй",
                        """
const m = mod("./useCounter");
const useCounter = m.useCounter ?? m.default;
function Probe() {
  const counter = useCounter(1);
  return (
    <div>
      <p>Утга: {counter.count}</p>
      <button onClick={() => counter.decrement()}>хасах</button>
    </div>
  );
}
render(<Probe />);
await user.click(screen.getByRole("button", { name: "хасах" }));
await user.click(screen.getByRole("button", { name: "хасах" }));
expect(screen.text()).toContain("Утга: 0");
""",
                    ),
                    test(
                        "Hook-ийг хоёр удаа дуудахад state нь тус тусдаа байна",
                        """
const m = mod("./useCounter");
const useCounter = m.useCounter ?? m.default;
function Probe() {
  const a = useCounter(1);
  const b = useCounter(1);
  return (
    <div>
      <p>A: {a.count}</p>
      <p>B: {b.count}</p>
      <button onClick={() => a.increment()}>A нэмэх</button>
    </div>
  );
}
render(<Probe />);
await user.click(screen.getByRole("button", { name: "A нэмэх" }));
expect(screen.text()).toContain("A: 2");
expect(screen.text()).toContain("B: 1");
""",
                    ),
                    test(
                        "Тасалбарын нийт үнэ зөв тооцогдоно",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: "Хүүхэд +" }));
await user.click(screen.getByRole("button", { name: "Том хүн +" }));
expect(screen.text()).toContain("Нийт: 38000₮");
await user.click(screen.getByRole("button", { name: "Цэвэрлэх" }));
expect(screen.text()).toContain("Нийт: 15000₮");
""",
                    ),
                ),
                tips="""\
- Hook дотор нэг `useState(initialValue)` хангалттай. Функцүүд нь зөвхөн
  `setCount`-ийг дуудна.
- `decrement`: `Math.max(0, value - 1)` — 0-ээс доош буухгүй.
- `reset`: `setCount(initialValue)`.
- `App`-д `const adults = useCounter(1); const kids = useCounter(0);` — тус
  бүр өөрийн state-тэй. Товчнууд `adults.increment` гэх мэтийг дуудна.
""",
                solution=solution(
                    App_jsx="""\
import { useCounter } from "./useCounter";

export default function App() {
  const adults = useCounter(1);
  const kids = useCounter(0);

  const total = adults.count * 15000 + kids.count * 8000;

  return (
    <main>
      <h1>🎟️ Кино тасалбар</h1>
      <p>
        Том хүн: {adults.count}{" "}
        <button onClick={adults.decrement}>Том хүн −</button>{" "}
        <button onClick={adults.increment}>Том хүн +</button>
      </p>
      <p>
        Хүүхэд: {kids.count}{" "}
        <button onClick={kids.decrement}>Хүүхэд −</button>{" "}
        <button onClick={kids.increment}>Хүүхэд +</button>
      </p>
      <p>Нийт: {total}₮</p>
      <button
        onClick={() => {
          adults.reset();
          kids.reset();
        }}
      >
        Цэвэрлэх
      </button>
    </main>
  );
}
""",
                    useCounter_js="""\
import { useState } from "react";

export function useCounter(initialValue = 0) {
  const [count, setCount] = useState(initialValue);

  function increment() {
    setCount((value) => value + 1);
  }

  function decrement() {
    setCount((value) => Math.max(0, value - 1));
  }

  function reset() {
    setCount(initialValue);
  }

  return { count, increment, decrement, reset };
}
""",
                ),
            ),
        ),
        # ------------------------------------------------------------------
        LessonSpec(
            title="useLocalStorage hook",
            slug="uselocalstorage",
            description="State-ийг localStorage-д хадгалж, дахин ачаалсны дараа сэргээх hook.",
            duration=960,
            language=JSX,
            content="""\
### Энэ хичээлээр

- `useState`-ийн lazy анхны утгаар localStorage-оос нэг л удаа унших
- Утга өөрчлөгдөх бүрт effect-ээр хадгалах
- JSON-оор тоо, объект, массив хадгалж, эвдэрсэн өгөгдлөөс хамгаалах

### Яагаад чухал вэ

State зөвхөн санах ойд амьдардаг: хуудсыг дахин ачаалахад алга болно.
Хэрэглэгчийн сонгосон theme, бичиж эхэлсэн ноорог, сагс дахин ачаалсны
дараа ч үлдэх ёстой. Хөтчийн `localStorage` үүнд тохирно. Ийм хэрэгцээ
олон газар гардаг тул нэг удаа hook болгож бичээд, `useState` шиг
хэрэглэнэ.

### localStorage товчхон

```jsx
localStorage.setItem("theme", "dark");
localStorage.getItem("theme");   // "dark"
localStorage.getItem("байхгүй"); // null
localStorage.removeItem("theme");
```

Зөвхөн **текст** хадгалагдана: `setItem("size", 16)` нь `"16"` болж буцна.
Тоо, объект, массивыг `JSON.stringify`-аар текст болгож хадгалаад,
`JSON.parse`-аар буцааж уншина:

```jsx
localStorage.setItem("cart", JSON.stringify([{ id: 1, qty: 2 }]));
const cart = JSON.parse(localStorage.getItem("cart")); // дахин массив
```

### Lazy анхны утга

```jsx
// ❌ localStorage-ийг render БҮРТ уншина
const [theme, setTheme] = useState(localStorage.getItem("theme") ?? "light");

// ✅ Функц өгвөл React түүнийг зөвхөн эхний render-т дуудна
const [theme, setTheme] = useState(() => localStorage.getItem("theme") ?? "light");
```

Эхний хувилбарт `useState` анхны утгыг хоёр дахь render-ээс эхлэн
ашиглахгүй ч аргумент нь render бүрт тооцоологдсоор байдаг. localStorage
уншиж, JSON задлах нь хурдан ажил биш. Функц өгснөөр React-д «хэрэгтэй
үед нь нэг удаа дууд» гэж хэлнэ.

### Хадгалах: effect

Утга өөрчлөгдөх бүрт хадгалах нь гадаад системтэй синхрончлох ажил тул
`useEffect`:

```jsx
useEffect(() => {
  localStorage.setItem("theme", theme);
}, [theme]);
```

### Эвдэрсэн өгөгдөл

localStorage-д апп-ын хуучин хувилбар эсвэл хэрэглэгч өөрөө буруу текст
хадгалсан байж болно. Тэгвэл `JSON.parse` алдаа шидэж, апп огт
нээгдэхгүй. `try`/`catch`-ээр хамгаалж, анхны утга руу буцна:

```jsx
function readJson(key, fallback) {
  try {
    const saved = localStorage.getItem(key);
    return saved === null ? fallback : JSON.parse(saved);
  } catch {
    return fallback;
  }
}
```

### Бодит төсөлд

- Next.js зэрэг сервер дээр render хийдэг орчинд `localStorage` байхгүй —
  `typeof window !== "undefined"` шалгалт хэрэгтэй. Vite апп-д асуудалгүй.
- Өөр tab дээр өөрчлөгдсөнийг `window`-ийн `storage` үйл явдлаар мэдэж
  болно.
- Нууц үгийг localStorage-д хэзээ ч хадгалахгүй — хуудсан дээрх ямар ч
  скрипт уншиж чадна.

Энэ засварлагчийн localStorage «Хөтөч»-ийг дахин ачаалсны дараа ч
хадгалагдана.

```quiz
`useState(JSON.parse(localStorage.getItem("cart")) ?? [])` кодын асуудал юу вэ?
- [x] localStorage-ийг render бүрт уншиж, JSON задална
- [ ] Анхны утга хэзээ ч ашиглагдахгүй
- [ ] `useState` массив хүлээж авдаггүй
> Функц өгвөл (`useState(() => …)`) React түүнийг зөвхөн эхний render-т дуудна.
```

### Дүгнэлт

localStorage-оос lazy анхны утгаар нэг удаа уншиж, effect-ээр хадгална.
Зөвхөн текст хадгалагддаг тул JSON хэрэглэж, `JSON.parse`-ийг
`try`/`catch`-ээр хамгаал. Үүнийг hook болговол `useState` шиг хялбар
хэрэглэнэ.
""",
            initial_code=vite(
                """\
import { useLocalStorage } from "./useLocalStorage";

export default function App() {
  const [note, setNote] = useLocalStorage("note", "");
  const [fontSize, setFontSize] = useLocalStorage("fontSize", 16);

  return (
    <main>
      <h1>📝 Тэмдэглэл</h1>
      <p>
        Үсгийн хэмжээ: {fontSize}px{" "}
        <button onClick={() => setFontSize(fontSize - 1)}>A−</button>{" "}
        <button onClick={() => setFontSize(fontSize + 1)}>A+</button>
      </p>
      <label>
        Тэмдэглэл
        <textarea
          value={note}
          onChange={(event) => setNote(event.target.value)}
          rows={6}
          style={{ display: "block", width: "100%", fontSize }}
        />
      </label>
      <p>{note.length} тэмдэгт</p>
    </main>
  );
}
""",
                extra={
                    "useLocalStorage.js": """\
import { useState } from "react";

export function useLocalStorage(key, initialValue) {
  // TODO 1: Эхний render-т л localStorage-оос key-ээр унш, JSON.parse хий.
  //         Байхгүй эсвэл эвдэрсэн бол initialValue.
  // TODO 2: value өөрчлөгдөх бүрт JSON.stringify хийж хадгал.
  const [value, setValue] = useState(initialValue);
  return [value, setValue];
}
"""
                },
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐ · 12 минут

`App` нь `useLocalStorage(key, initialValue)` hook-ийг `useState` шиг
ашигладаг ч hook одоогоор юу ч хадгалдаггүй. `useLocalStorage.js`-ийг
гүйцээ: эхний render-т утгыг localStorage-оос уншиж, өөрчлөгдөх бүрт JSON
болгож хадгална. Тэмдэглэл бичээд «Хөтөч»-ийг дахин ачаалж шалгаарай.
""",
                tests=(
                    test(
                        "Хадгалсан утгыг эхний render-т уншина",
                        """
localStorage.setItem("note", JSON.stringify("Маргааш 9 цагт"));
localStorage.setItem("fontSize", "20");
render(<App />);
expect(screen.getByLabelText("Тэмдэглэл")).toHaveValue("Маргааш 9 цагт");
expect(screen.text()).toContain("Үсгийн хэмжээ: 20px");
""",
                    ),
                    test(
                        "Өөрчлөлтийг localStorage-д JSON-оор хадгална",
                        """
render(<App />);
await user.type(screen.getByLabelText("Тэмдэглэл"), "Сайн");
expect(JSON.parse(localStorage.getItem("note"))).toBe("Сайн");
await user.click(screen.getByRole("button", { name: "A+" }));
expect(localStorage.getItem("fontSize")).toBe("17");
""",
                    ),
                    test(
                        "Утга байхгүй эсвэл эвдэрсэн бол анхны утгыг хэрэглэнэ",
                        """
localStorage.setItem("note", "{эвдэрсэн");
render(<App />);
expect(screen.getByLabelText("Тэмдэглэл")).toHaveValue("");
expect(screen.text()).toContain("Үсгийн хэмжээ: 16px");
""",
                    ),
                    test(
                        "localStorage-ийг render бүрт биш, нэг л удаа уншина",
                        """
const original = localStorage.getItem.bind(localStorage);
let reads = 0;
localStorage.getItem = (key) => {
  if (key === "note") reads += 1;
  return original(key);
};
render(<App />);
await user.type(screen.getByLabelText("Тэмдэглэл"), "абвгд");
expect(reads).toBe(1);
""",
                    ),
                ),
                tips="""\
- `useState(() => { … })` — функц дотор `localStorage.getItem(key)` уншаад,
  `null` бол `initialValue`, эс бөгөөс `JSON.parse`-ийн үр дүнг буцаа.
- `JSON.parse`-ийг `try`/`catch`-д хий — эвдэрсэн текст байвал `initialValue`.
- Хадгалах нь `useEffect` дотор: `JSON.stringify(value)`, dependency нь
  `[key, value]`.
- Hook `[value, setValue]` буцаана — яг `useState` шиг.
""",
                solution=solution(
                    useLocalStorage_js="""\
import { useEffect, useState } from "react";

export function useLocalStorage(key, initialValue) {
  const [value, setValue] = useState(() => {
    try {
      const saved = localStorage.getItem(key);
      return saved === null ? initialValue : JSON.parse(saved);
    } catch {
      return initialValue;
    }
  });

  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);

  return [value, setValue];
}
"""
                ),
            ),
        ),
        # ------------------------------------------------------------------
        LessonSpec(
            title="Төсөл: Hook-ийн сан",
            slug="tusul-hook-san",
            description="useFetch, useDebounce, useWindowSize-ээс бүрдсэн hook-ийн сан бүтээх.",
            duration=2100,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Модулийн hook-уудыг нэгтгэж, дахин ашиглагдах hook-ийн сан бүтээх
- `useFetch`, `useDebounce`, `useWindowSize`-ийг бичиж, жижиг апп-д хэрэглэх
- Hook бүрт effect-ийн цэвэрлэгээг зөв хийх

### Яагаад чухал вэ

Бодит төсөл бүрт «өгөгдөл татах», «хэрэглэгч бичиж дуусахыг хүлээх»,
«цонхны хэмжээг мэдэх» гэх мэт логик дахин дахин гарна. Үүнийг нэг удаа
сайн бичсэн hook болговол component-ууд богино, ойлгомжтой болж, алдаа нэг
л газар засагдана.

### Төслийн бүтэц

| Файл | Юу байх |
|---|---|
| `hooks.js` | Таны hook-ийн сан — энд бичнэ |
| `App.jsx` | Хэрэглэгч хайх апп — hook-уудыг аль хэдийн ашиглаж байгаа |

`App` нь хайлтын үгийг `useDebounce`-оор хоцрооно, `useFetch`-ээр
`/api/users?q=…`-ээс хэрэглэгчдийг татна, доод хэсэгт нь `useWindowSize`-ээр
цонхны хэмжээг харуулна. Hook-ууд ажиллахад апп ч ажиллана.

### Hook-уудын API

| Hook | Буцаах утга | Юу хийх |
|---|---|---|
| `useFetch(url)` | `{ data, loading, error }` | `url` өөрчлөгдөх бүрт `fetch` хийнэ; хариу `ok` биш бол `error` |
| `useDebounce(value, delay)` | хоцорсон `value` | `value` `delay` мс хөдлөхгүй байсны дараа л шинэчлэгдэнэ |
| `useWindowSize()` | `{ width, height }` | `window.innerWidth`, `innerHeight`; `resize` бүрт шинэчлэгдэнэ |

Гурвууланг нь `hooks.js`-ээс нэртэй export-оор гаргана.

### useFetch: анхаарах зүйлс

- `loading`-ийг `true`-ээс эхлүүлж, хариу ирэхэд `false` болго.
- `response.ok` биш бол алдаа шид (Модул 0) — `error`-т хадгал.
- Хэрэглэгч хурдан бичвэл хуучин хүсэлтийн хариу шинийхээс хойно ирж
  болно. Цэвэрлэгээнд `ignore` тэмдэглэл тавьж хуучин хариуг хая
  (Модул 5):

```jsx
useEffect(() => {
  let ignore = false;
  // fetch(url) … хариу ирэхэд:
  //   if (!ignore) setData(json);
  return () => {
    ignore = true;
  };
}, [url]);
```

### useDebounce: хэрхэн ажилладаг вэ

`value` өөрчлөгдөх бүрт `delay` мс-ийн timer эхлүүлнэ. Timer дуусахаас
өмнө `value` дахин өөрчлөгдвөл effect-ийн цэвэрлэгээ хуучин timer-ийг
цуцална. Ингэснээр хэрэглэгч бичиж байх хооронд хүсэлт явахгүй, зогссоны
дараа ганц хүсэлт явна. Хайлт, автоматаар хадгалах, шүүлтүүрт маш түгээмэл.

### useWindowSize: listener-ээ цэвэрлэ

`window.addEventListener("resize", …)`-ийг effect-д нэмээд, цэвэрлэгээнд
нь `removeEventListener`-ээр заавал хас. Эс бөгөөс component устсан ч
listener үлдэж, дэмий ажилласаар байна.

### Туршиж үзэх

«Хөтөч» дээр хайлтад хурдан бичээрэй: үр дүн үсэг бүрт биш, бичиж
зогссоны дараа шинэчлэгдэх ёстой. Хөтчийнхөө цонхны хэмжээг өөрчилж доод
талын тоог ажигла.

```quiz
`useDebounce(query, 300)` ашиглах үед хэрэглэгч 5 үсгийг хурдан бичээд зогсвол хэдэн хүсэлт явах вэ?
- [ ] 5
- [x] 1
- [ ] 0
> Үсэг бүр өмнөх timer-ийг цуцалдаг. Зөвхөн сүүлийн үсгийн дараах timer дуусаж, ганц хүсэлт явна.
```

```quiz
`useWindowSize`-ийн effect цэвэрлэгээгүй бол юу болох вэ?
- [ ] Цонхны хэмжээ огт шинэчлэгдэхгүй
- [x] Component устсаны дараа ч `resize` listener ажилласаар байна
- [ ] React алдаа шиднэ
> Цэвэрлэгээ нь effect-ийн нэмсэн бүхнийг буцааж авдаг. Үгүй бол listener хуримтлагдана.
```

### Дүгнэлт

Hook-ийн сан нь state, effect, цэвэрлэгээтэй нарийн логикийг нэг газар
төвлөрүүлж, component-уудыг энгийн болгодог. Hook бүр өөрийн timer,
listener, хүсэлтээ цэвэрлэх ёстой.
""",
            initial_code=vite(
                """\
import { useState } from "react";
import { useDebounce, useFetch, useWindowSize } from "./hooks";

export default function App() {
  const [query, setQuery] = useState("");
  const debouncedQuery = useDebounce(query, 300);
  const { data: users, loading, error } = useFetch(
    `/api/users?q=${encodeURIComponent(debouncedQuery)}`,
  );
  const { width, height } = useWindowSize();

  return (
    <main>
      <h1>👥 Хэрэглэгч хайх</h1>
      <label>
        Хайх <input value={query} onChange={(event) => setQuery(event.target.value)} />
      </label>
      {loading && <p>Ачаалж байна…</p>}
      {error && <p role="alert">Алдаа гарлаа</p>}
      {users &&
        (users.length === 0 ? (
          <p>Олдсонгүй</p>
        ) : (
          <ul>
            {users.map((user) => (
              <li key={user.id}>
                {user.name} — {user.city}
              </li>
            ))}
          </ul>
        ))}
      <footer>
        Цонх: {width} × {height}
      </footer>
    </main>
  );
}
""",
                extra={
                    "hooks.js": """\
import { useEffect, useState } from "react";

// useFetch(url) → { data, loading, error }
export function useFetch(url) {
  // TODO
  return { data: null, loading: false, error: null };
}

// useDebounce(value, delay) → value нь delay мс өөрчлөгдөөгүй байсны дараах утга
export function useDebounce(value, delay = 300) {
  // TODO
  return value;
}

// useWindowSize() → { width, height }
export function useWindowSize() {
  // TODO
  return { width: 0, height: 0 };
}
"""
                },
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐⭐ · 35 минут

`hooks.js`-д гурван hook-ийг дээрх API-ийн дагуу бич. `App.jsx` тэдгээрийг
аль хэдийн ашиглаж байгаа тул hook-ууд ажиллахад хайлтын апп ч ажиллана.
Тест бүр hook-ийг жижиг component дотор тусад нь шалгадаг — унасан тестийн
мессежээс аль hook-д юу дутуу байгааг унш.
""",
                tests=(
                    test(
                        "useFetch өгөгдөл татах үед loading, дараа нь data буцаана",
                        """
const { useFetch } = mod("./hooks");
function Probe() {
  const { data, loading, error } = useFetch("/api/products/2");
  if (loading) return <p>Ачаалж байна</p>;
  if (error) return <p>Алдаа</p>;
  return <p>Бараа: {data ? data.name : "—"}</p>;
}
render(<Probe />);
expect(screen.text()).toContain("Ачаалж байна");
expect(await screen.findByText("Бараа: Алим")).toBeInTheDocument();
""",
                    ),
                    test(
                        "useFetch серверийн алдааг error болгож буцаана",
                        """
const { useFetch } = mod("./hooks");
function Probe() {
  const { data, loading, error } = useFetch("/api/products?_status=500");
  if (loading) return <p>Ачаалж байна</p>;
  if (error) return <p>Алдаа гарлаа</p>;
  return <p>Өгөгдөл: {data ? data.length : "—"}</p>;
}
render(<Probe />);
expect(await screen.findByText("Алдаа гарлаа")).toBeInTheDocument();
""",
                    ),
                    test(
                        "useDebounce утгыг хоцроож шинэчилнэ",
                        """
const { useDebounce } = mod("./hooks");
function Probe() {
  const [text, setText] = React.useState("");
  const debounced = useDebounce(text, 200);
  return (
    <div>
      <label>
        Текст <input value={text} onChange={(event) => setText(event.target.value)} />
      </label>
      <p>Хоцорсон: [{debounced}]</p>
    </div>
  );
}
render(<Probe />);
await user.type(screen.getByLabelText("Текст"), "abc");
expect(screen.text()).toContain("Хоцорсон: []");
await waitFor(() => expect(screen.text()).toContain("Хоцорсон: [abc]"));
""",
                    ),
                    test(
                        "useWindowSize цонхны хэмжээ өөрчлөгдөхөд шинэчлэгдэнэ",
                        """
const { useWindowSize } = mod("./hooks");
function Probe() {
  const { width } = useWindowSize();
  return <p>Өргөн: {width}</p>;
}
const original = Object.getOwnPropertyDescriptor(window, "innerWidth");
try {
  render(<Probe />);
  expect(screen.text()).toContain(`Өргөн: ${window.innerWidth}`);
  Object.defineProperty(window, "innerWidth", { configurable: true, value: 555 });
  await act(async () => {
    window.dispatchEvent(new Event("resize"));
  });
  expect(screen.text()).toContain("Өргөн: 555");
} finally {
  if (original) Object.defineProperty(window, "innerWidth", original);
  else delete window.innerWidth;
}
""",
                    ),
                    test(
                        "Хайлт үсэг бүрт биш, бичиж зогссоны дараа нэг хүсэлт илгээнэ",
                        """
const userRequests = () => api.requests.filter((request) => request.path.startsWith("/api/users")).length;
render(<App />);
expect(await screen.findByText(/Бат/)).toBeInTheDocument();
const before = userRequests();
await user.type(screen.getByLabelText("Хайх"), "Сараа");
await waitFor(() => expect(screen.getAllByRole("listitem")).toHaveLength(1));
expect(screen.getByRole("listitem")).toHaveTextContent("Сараа");
expect(userRequests() - before).toBeLessThanOrEqual(2);
""",
                    ),
                ),
                tips="""\
- `useFetch`: гурван state (`data`, `loading`, `error`). `useEffect(…, [url])`
  дотор async функц зарлаж, шууд дууд. Шинэ `url` ирэхэд `loading`-ийг дахин
  `true`, `error`-ийг `null` болго. `!response.ok` бол `throw`.
- `useDebounce`: `const [debounced, setDebounced] = useState(value);` effect
  дотор `setTimeout(() => setDebounced(value), delay)`, цэвэрлэгээнд
  `clearTimeout`. Dependency: `[value, delay]`.
- `useWindowSize`: анхны утгыг `window.innerWidth`, `window.innerHeight`-ээс
  ав. `resize` listener-ийг effect-ийн цэвэрлэгээнд заавал хас.
""",
                solution=solution(
                    hooks_js="""\
import { useEffect, useState } from "react";

export function useFetch(url) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let ignore = false;
    setLoading(true);
    setError(null);

    async function load() {
      try {
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error(`Серверийн алдаа: ${response.status}`);
        }
        const json = await response.json();
        if (!ignore) setData(json);
      } catch (caught) {
        if (!ignore) setError(caught);
      } finally {
        if (!ignore) setLoading(false);
      }
    }

    load();
    return () => {
      ignore = true;
    };
  }, [url]);

  return { data, loading, error };
}

export function useDebounce(value, delay = 300) {
  const [debounced, setDebounced] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debounced;
}

export function useWindowSize() {
  const [size, setSize] = useState(() => ({
    width: window.innerWidth,
    height: window.innerHeight,
  }));

  useEffect(() => {
    function handleResize() {
      setSize({ width: window.innerWidth, height: window.innerHeight });
    }
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return size;
}
"""
                ),
            ),
        ),
    ],
)
