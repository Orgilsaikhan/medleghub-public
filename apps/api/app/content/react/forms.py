"""Модул 4 — Форм.

Удирдлагатай (controlled) input-ээс эхлээд олон талбартай форм, сонголтын
талбарууд, илгээлт, баталгаажуулалт, хүртээмжтэй алдааны мэдэгдэл хүртэл
алхам алхмаар үзэж, төгсгөлд нь бүртгэлийн форм бүтээнэ.
"""

from app.content.react.common import solution, test, vite
from app.content.types import ExerciseSpec, LessonSpec, ModuleSpec
from app.models.enums import LessonLanguage

JSX = LessonLanguage.JSX

# Модулийн бүх хичээлд ижил, түгжигдсэн загвар — формууд цэвэрхэн харагдана.
FORM_CSS = """\
main,
form {
  max-width: 440px;
}
label {
  display: block;
  margin: 14px 0 4px;
  font-weight: 600;
}
input:not([type="checkbox"]):not([type="radio"]),
select,
textarea {
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
[aria-invalid="true"] {
  border-color: #b42318 !important;
}
fieldset {
  margin: 14px 0;
  border: 1px solid #d0d7de;
  border-radius: 8px;
}
fieldset label,
label:has(> input[type="checkbox"]) {
  font-weight: 400;
}
button {
  margin: 14px 8px 0 0;
  padding: 8px 16px;
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
.error {
  margin: 4px 0 0;
  color: #b42318;
  font-size: 14px;
  font-weight: 400;
}
.card {
  margin-top: 20px;
  padding: 16px;
  border: 1px solid #d0d7de;
  border-radius: 12px;
  background: #f6f8fa;
}
"""

FORMS = ModuleSpec(
    title="Модул 4 — Форм",
    description="Удирдлагатай форм, баталгаажуулалт, хүртээмжтэй алдааны мэдэгдэл бичнэ.",
    lessons=[
        # --- 1 ------------------------------------------------------------------
        LessonSpec(
            title="Удирдлагатай (controlled) input",
            slug="controlled-input",
            description="Input-ийн утгыг state-ээр удирдаж, бичсэн текстийг шууд харуулна.",
            duration=720,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Input-ийн утгыг state-д хадгалж, `value` ба `onChange`-ээр холбох
- `e.target.value`-ээр хэрэглэгчийн бичсэн текстийг авах
- Бичих явцад UI-г шууд шинэчлэх (live preview)
- Удирдлагагүй (uncontrolled) input ба `defaultValue`-тэй танилцах

### Яагаад чухал вэ

Нэвтрэх, бүртгүүлэх, хайх, сэтгэгдэл бичих — бараг бүх апп форм ашигладаг.
Хэрэглэгч юу бичиж байгааг апп тань тухай бүрд нь мэдэх хэрэгтэй: тэмдэгт
тоолох, товчийг идэвхгүй болгох, алдаа харуулах, бичих явцад хайх.

HTML-ийн `<input>` утгаа DOM дотроо өөрөө хадгалдаг. React-д бид тэр утгыг
**state**-д хадгалж, «үнэний ганц эх сурвалж» болгоно. Ингэснээр дэлгэц ба
өгөгдөл хэзээ ч зөрөхгүй — Модул 0-ийн DOM тоологчийн асуудлыг санаарай.

### value + onChange

```jsx
import { useState } from "react";

export default function App() {
  const [name, setName] = useState("");

  return (
    <label>
      Нэр
      <input value={name} onChange={(e) => setName(e.target.value)} />
    </label>
  );
}
```

Энд хоёр чиглэлтэй холбоо үүсч байна:

1. `value={name}` — input нь state-ийн утгыг харуулна.
2. Хэрэглэгч үсэг бичихэд `onChange` ажиллаж, `e.target.value` буюу
   input-ийн **шинэ** утгыг state-д бичнэ.
3. State өөрчлөгдөхөд component дахин render хийж, input шинэ утгаа
   харуулна.

Утгыг нь React удирддаг ийм input-ийг **удирдлагатай (controlled) input**
гэнэ. `e.target` нь event болсон элемент (энд input), `.value` нь түүний
одоогийн бүтэн текст.

React-ийн `onChange` нь HTML-ийн `change` event-ээс ялгаатай: талбараас
гарахыг хүлээлгүй **үсэг бүрт** ажиллана.

### Бичих явцад шууд харуулах

Утга state-д байгаа тул JSX-ийн хаана ч ашиглаж болно:

```jsx
<p>Сайн уу, {name || "зочин"}!</p>
<p>{name.length} / 20 тэмдэгт</p>
```

Эсрэгээр нь state-ийг өөрчилбөл input өөрөө дагаж шинэчлэгдэнэ. Жишээ нь
талбарыг цэвэрлэх товч:

```jsx
<button onClick={() => setName("")}>Цэвэрлэх</button>
```

Утгыг state-д бичихээсээ өмнө өөрчилж ч болно:
`setName(e.target.value.toUpperCase())` — бичсэн бүхэн том үсэг болно.
Энэ бүхэн controlled input-ийн давуу тал.

### Түгээмэл алдаа

- **`onChange`-гүй `value`.** Input «хөлдөж», юу ч бичигдэхгүй. React
  Console-д «You provided a `value` prop to a form field without an
  `onChange` handler» гэж анхааруулна.
- **Анхны утга `undefined`.** `useState()` гэж хоосон эхлүүлбэл input эхлээд
  uncontrolled, үсэг бичсний дараа controlled болж, React анхааруулга
  өгнө. Текстийн анхны утга үргэлж `""`.
- **`onChange={setName}`.** Ингэвэл state-д текст биш event объект орно.
  `e.target.value`-г авахаа бүү мартаарай.

```quiz
Энэ кодын алдааг ол: `<input value={name} />` (`name` нь state)
- [ ] Бичсэн текст state-д автоматаар орно, алдаа байхгүй
- [x] Input-д юу ч бичигдэхгүй — state-ийг шинэчлэх `onChange` алга
- [ ] Апп алдаа шидэж зогсоно
> `value` өгсөн бол input үргэлж тэр утгыг харуулна. `onChange`-ээр state-ийг шинэчлэхгүй бол утга хэзээ ч өөрчлөгдөхгүй.
```

### Удирдлагагүй (uncontrolled) input

Заримдаа утгыг бичих явцад мэдэх шаардлагагүй — зөвхөн илгээх үед л
хэрэгтэй. Тэгвэл утгыг DOM-д үлдээж, зөвхөн анхны утгыг `defaultValue`-ээр
өгнө:

```jsx
<input name="city" defaultValue="Улаанбаатар" />
```

`defaultValue` нь зөвхөн эхлэлийн утга — дараа нь React оролцохгүй. Утгыг
илгээх үед `FormData`-аар (Модул 11-ийн form action) эсвэл ref-ээр
(Модул 6) уншина.

| | Controlled | Uncontrolled |
|---|---|---|
| Утга хаана хадгалагдах | state | DOM |
| Prop | `value` + `onChange` | `defaultValue` |
| Бичих явцад харуулах, шалгах | Амархан | Хэцүү |

Бичих явцад UI шинэчлэх, шалгах шаардлагатай бол controlled input сонго.
Энэ модульд бүх талбарыг controlled хэлбэрээр бичнэ.

```quiz
Талбарт «Ба» гэж бичсэн байхад хэрэглэгч «т» дарав. `onChange` дотор `e.target.value` юу байх вэ?
- [ ] "Ба" — өмнөх утга
- [x] "Бат" — шинэчлэгдсэн бүтэн утга
- [ ] "т" — зөвхөн дарсан үсэг
> `e.target.value` нь input-ийн одоогийн бүтэн текст. Тэр л шинэ state болно.
```

### Дүгнэлт

Controlled input = `value={state}` + `onChange` дотор
`setState(e.target.value)`. Утга state-д байгаа тул хаана ч харуулж,
өөрчилж, цэвэрлэж болно. Uncontrolled input утгаа DOM-д хадгалж,
`defaultValue`-ээр эхэлнэ.
""",
            initial_code=vite(
                """\
import { useState } from "react";

export default function App() {
  const [name, setName] = useState("");

  // TODO 1: input-ийг name state-тэй холбо (value + onChange)
  // TODO 2: картад бичсэн нэр, тэмдэгтийн тоог харуул
  // TODO 3: «Цэвэрлэх» товч name-ийг хоосон болгоно

  return (
    <main>
      <h1>Нэрийн хуудас</h1>
      <label>
        Нэр
        <input maxLength={20} />
      </label>
      <button>Цэвэрлэх</button>

      <section className="card">
        <p>Сайн уу, зочин!</p>
        <p>0 / 20 тэмдэгт</p>
      </section>
    </main>
  );
}
""",
                css=FORM_CSS,
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐ · 8 минут

«Нэр» талбарыг `name` state-тэй холбож нэрийн хуудсыг «амьд» болго:
бичсэн нэр картад шууд гарч, тэмдэгтийн тоо шинэчлэгдэнэ. Нэр хоосон үед
картад «Сайн уу, зочин!» гэж харагдана. «Цэвэрлэх» товч талбарыг хоосолно.
""",
                tests=(
                    test(
                        "Бичсэн нэр картад шууд харагдана",
                        """
render(<App />);
await user.type(screen.getByLabelText("Нэр"), "Сараа");
expect(screen.text()).toContain("Сайн уу, Сараа!");
""",
                    ),
                    test(
                        "Тэмдэгтийн тоо бичих явцад шинэчлэгдэнэ",
                        """
render(<App />);
await user.type(screen.getByLabelText("Нэр"), "Бат");
expect(screen.text()).toContain("3 / 20");
""",
                    ),
                    test(
                        "«Цэвэрлэх» товч талбар ба картыг анхны байдалд нь оруулна",
                        """
render(<App />);
const input = screen.getByLabelText("Нэр");
await user.type(input, "Бат");
await user.click(screen.getByRole("button", { name: "Цэвэрлэх" }));
expect(input).toHaveValue("");
expect(screen.text()).toContain("Сайн уу, зочин!");
expect(screen.text()).toContain("0 / 20");
""",
                    ),
                ),
                tips="""\
- Input-д хоёулаа хэрэгтэй: `value={name}` ба
  `onChange={(e) => setName(e.target.value)}`.
- Картын текстэд `{name || "зочин"}` — хоосон мөр худал (falsy) тул
  «зочин» гарна.
- Тэмдэгтийн тоо: `{name.length}`.
- «Цэвэрлэх» нь input-д шууд хүрэхгүй, зөвхөн state-ийг `""` болгоно —
  controlled input өөрөө дагаж хоосорно. `value`-гүй бол ингэж цэвэрлэх
  боломжгүй.
""",
                solution=solution(
                    App_jsx="""\
import { useState } from "react";

export default function App() {
  const [name, setName] = useState("");

  return (
    <main>
      <h1>Нэрийн хуудас</h1>
      <label>
        Нэр
        <input maxLength={20} value={name} onChange={(e) => setName(e.target.value)} />
      </label>
      <button onClick={() => setName("")}>Цэвэрлэх</button>

      <section className="card">
        <p>Сайн уу, {name || "зочин"}!</p>
        <p>{name.length} / 20 тэмдэгт</p>
      </section>
    </main>
  );
}
"""
                ),
            ),
        ),
        # --- 2 ------------------------------------------------------------------
        LessonSpec(
            title="Олон талбартай форм",
            slug="olon-talbartai-form",
            description="Олон талбарыг нэг state объект, name attribute, нэг handleChange-ээр удирдана.",
            duration=840,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Формын бүх утгыг нэг state объектод хадгалах
- `name` attribute-аар талбарыг таних
- `[e.target.name]` тооцоолсон түлхүүрээр нэг `handleChange` бичих
- `textarea`-г controlled болгох

### Яагаад чухал вэ

Бүртгэл, профайл, хүргэлтийн хаяг — бодит форм 5–10 талбартай. Талбар бүрт
тусдаа `useState`, тусдаа `onChange` бичвэл код хурдан давтагдана:

```jsx
const [firstName, setFirstName] = useState("");
const [lastName, setLastName] = useState("");
const [email, setEmail] = useState("");

<input value={firstName} onChange={(e) => setFirstName(e.target.value)} />
<input value={lastName} onChange={(e) => setLastName(e.target.value)} />
<input value={email} onChange={(e) => setEmail(e.target.value)} />
```

Талбар нэмэх бүрт гурван газар засна, илгээхдээ бүх утгыг гараар нэг
объект болгож цуглуулна. Илүү цэвэрхэн арга бий.

### Нэг объект, нэг handler

```jsx
const [form, setForm] = useState({ firstName: "", lastName: "", email: "" });

function handleChange(e) {
  const { name, value } = e.target;
  setForm({ ...form, [name]: value });
}

return (
  <>
    <input name="firstName" value={form.firstName} onChange={handleChange} />
    <input name="lastName" value={form.lastName} onChange={handleChange} />
    <input name="email" value={form.email} onChange={handleChange} />
  </>
);
```

Гурван талбар нэг функцийг хуваалцана. Аль талбар өөрчлөгдсөнийг функц
`e.target.name`-ээс мэднэ. Тиймээс input бүрийн `name` нь state-ийн
түлхүүртэй **яг ижил** байх ёстой.

### Тооцоолсон түлхүүр `[name]`

```jsx
const key = "email";
const a = { key: "bat@example.mn" };   // { key: "bat@example.mn" }
const b = { [key]: "bat@example.mn" }; // { email: "bat@example.mn" }
```

Дөрвөлжин хаалт доторх илэрхийллийн **утга** түлхүүр болно (computed
property name). Тэгэхээр `{ ...form, [name]: value }` гэдэг нь «form-ийн
бүх талбарыг хуулж, `name` нэртэй талбарыг шинэ утгаар дар» гэсэн үг.

Дараалал чухал: эхлээд spread, дараа нь шинэ утга.
`{ [name]: value, ...form }` гэж бичвэл хуучин утга шинийг дарчихна.

### Функционал шинэчлэлт

Модул 3-т үзсэн шиг өмнөх state-ээс тооцох хэлбэр ч ажиллана:

```jsx
function handleChange(e) {
  const { name, value } = e.target;
  setForm((prev) => ({ ...prev, [name]: value }));
}
```

`name`, `value`-г callback-аас гадна урьдчилж задалж авсан нь цэвэрхэн:
callback хожим ажиллах тул тэр үед event объектод найдах шаардлагагүй.

### textarea

HTML-д `<textarea>` утгаа хүүхэд текстээр авдаг бол React-д `value`
prop-оор, яг input шиг:

```jsx
<textarea name="bio" value={form.bio} onChange={handleChange} />
```

`<select>`, checkbox, radio-г дараагийн хичээлд үзнэ.

### Түгээмэл алдаа

- **Spread мартах.** `setForm({ [name]: value })` — шинэ объектод ганц
  талбар үлдэж, бусад нь `undefined` болно. Бусад input хоосорч, React
  uncontrolled анхааруулга өгнө.
- **`name` таарахгүй.** `name="first_name"` гэвэл state-д `first_name`
  гэсэн шинэ түлхүүр үүсэж, `form.firstName` өөрчлөгдөхгүй — талбар
  «хөлдөнө».
- **Анхны объектод талбар мартах.** `useState({ firstName: "" })` дотор
  `email` байхгүй бол `value={form.email}` нь `undefined` болно.

```quiz
`setForm({ [e.target.name]: e.target.value })` гэж бичжээ. «Нэр»-д бичээд дараа нь «Овог»-т бичихэд юу болох вэ?
- [ ] Хоёр талбар хоёулаа зөв хадгалагдана
- [x] «Нэр» талбарын утга арилна
- [ ] React алдаа шидэж зогсоно
> Шинэ объектод зөвхөн нэг түлхүүр бий. Бусад талбарыг `...form`-оор хуулах ёстой.
```

```quiz
`const field = "city"; const user = { [field]: "Дархан" };` — `user` юу болох вэ?
- [x] `{ city: "Дархан" }`
- [ ] `{ field: "Дархан" }`
- [ ] `{ "[field]": "Дархан" }`
> Дөрвөлжин хаалт нь хувьсагчийн утгыг түлхүүр болгоно.
```

### Дүгнэлт

Олон талбартай формд нэг state объект, нэг `handleChange` хэрэглэнэ. Input
бүрийн `name` нь state-ийн түлхүүртэй ижил, шинэчлэхдээ
`{ ...form, [name]: value }`. Spread-ийг мартвал бусад талбар алга болно.
""",
            initial_code=vite(
                """\
import { useState } from "react";

export default function App() {
  const [form, setForm] = useState({
    firstName: "",
    lastName: "",
    email: "",
    bio: "",
  });

  function handleChange(e) {
    // TODO: e.target.name-ээс аль талбар болохыг мэдэж form-ийг шинэчил.
    //       Бусад талбарын утгыг алдахгүй байхаа мартваа.
  }

  const fullName = `${form.firstName} ${form.lastName}`.trim();

  // TODO: талбар бүрт state-ийн түлхүүртэй ижил name attribute нэм
  return (
    <main>
      <form>
        <h1>Профайл засах</h1>
        <label>
          Нэр
          <input value={form.firstName} onChange={handleChange} />
        </label>
        <label>
          Овог
          <input value={form.lastName} onChange={handleChange} />
        </label>
        <label>
          Имэйл
          <input type="email" value={form.email} onChange={handleChange} />
        </label>
        <label>
          Танилцуулга
          <textarea rows={3} value={form.bio} onChange={handleChange} />
        </label>
      </form>

      <section className="card">
        <h2>👤 {fullName || "Нэргүй хэрэглэгч"}</h2>
        <p>{form.email || "Имэйл оруулаагүй"}</p>
        <p>{form.bio}</p>
      </section>
    </main>
  );
}
""",
                css=FORM_CSS,
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 10 минут

Профайл засах формын дөрвөн талбар бүгд нэг `form` объектод хадгалагдана,
гэвч одоогоор юу ч бичигдэхгүй байна. Талбар бүрт тохирох `name` attribute
нэмж, ганц `handleChange` функцээр `form`-ийг шинэчил. Доорх карт бичих
явцад шинэчлэгдэнэ.
""",
                tests=(
                    test(
                        "Нэр, овог картад харагдана",
                        """
render(<App />);
await user.type(screen.getByLabelText("Нэр"), "Бат");
await user.type(screen.getByLabelText("Овог"), "Дорж");
expect(screen.getByRole("heading", { level: 2 })).toHaveTextContent("Бат Дорж");
""",
                    ),
                    test(
                        "Имэйл, танилцуулга картад харагдана",
                        """
render(<App />);
await user.type(screen.getByLabelText("Имэйл"), "bat@example.mn");
await user.type(screen.getByLabelText("Танилцуулга"), "React сурч байна");
expect(screen.text()).toContain("bat@example.mn");
expect(screen.text()).toContain("React сурч байна");
""",
                    ),
                    test(
                        "Нэг талбарт бичихэд бусад талбарын утга хэвээр үлдэнэ",
                        """
render(<App />);
await user.type(screen.getByLabelText("Нэр"), "Сараа");
await user.type(screen.getByLabelText("Имэйл"), "saraa@example.mn");
await user.type(screen.getByLabelText("Овог"), "Мөнх");
expect(screen.getByLabelText("Нэр")).toHaveValue("Сараа");
expect(screen.getByLabelText("Имэйл")).toHaveValue("saraa@example.mn");
expect(screen.getByLabelText("Овог")).toHaveValue("Мөнх");
""",
                    ),
                ),
                tips="""\
- `name` нь state-ийн түлхүүртэй яг ижил: `firstName`, `lastName`,
  `email`, `bio`. `textarea`-д ч мөн `name` хэрэгтэй.
- `handleChange` дотор эхлээд `const { name, value } = e.target;`, дараа нь
  `setForm({ ...form, [name]: value })`.
- `...form`-ийг мартвал нэг талбарт бичихэд бусад нь арилна — гурав дахь
  тест яг үүнийг шалгана.
""",
                solution=solution(
                    App_jsx="""\
import { useState } from "react";

export default function App() {
  const [form, setForm] = useState({
    firstName: "",
    lastName: "",
    email: "",
    bio: "",
  });

  function handleChange(e) {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
  }

  const fullName = `${form.firstName} ${form.lastName}`.trim();

  return (
    <main>
      <form>
        <h1>Профайл засах</h1>
        <label>
          Нэр
          <input name="firstName" value={form.firstName} onChange={handleChange} />
        </label>
        <label>
          Овог
          <input name="lastName" value={form.lastName} onChange={handleChange} />
        </label>
        <label>
          Имэйл
          <input type="email" name="email" value={form.email} onChange={handleChange} />
        </label>
        <label>
          Танилцуулга
          <textarea rows={3} name="bio" value={form.bio} onChange={handleChange} />
        </label>
      </form>

      <section className="card">
        <h2>👤 {fullName || "Нэргүй хэрэглэгч"}</h2>
        <p>{form.email || "Имэйл оруулаагүй"}</p>
        <p>{form.bio}</p>
      </section>
    </main>
  );
}
"""
                ),
            ),
        ),
        # --- 3 ------------------------------------------------------------------
        LessonSpec(
            title="select, checkbox, radio",
            slug="select-checkbox-radio",
            description="Сонголтын талбаруудыг удирдах: select-ийн value, checkbox-ийн checked, radio бүлэг.",
            duration=840,
            language=JSX,
            content="""\
### Энэ хичээлээр

- `<select>`-ийг `value`-ээр удирдах
- Checkbox-ийг `checked` ба `e.target.checked`-ээр удирдах
- Radio бүлгийг нэг state-ээр удирдах
- Бүх төрлийн талбарт нэг `handleChange` бичих

### Яагаад чухал вэ

Кофены хэмжээ, хүргэлтийн арга, «Үйлчилгээний нөхцөлийг зөвшөөрч байна» —
бүгд сонголтын талбар. Эдгээр нь текстийн талбараас нэг чухал зүйлээрээ
ялгаатай: checkbox, radio-гийн төлвийг `value` биш **`checked`** хэлдэг.
Үүнийг андуурах нь формын хамгийн түгээмэл алдааны нэг.

### select

```jsx
const [size, setSize] = useState("M");

<select value={size} onChange={(e) => setSize(e.target.value)}>
  <option value="S">Жижиг</option>
  <option value="M">Дунд</option>
  <option value="L">Том</option>
</select>
```

HTML-д сонгогдсон сонголтыг `<option selected>`-ээр тэмдэглэдэг бол
React-д `<select value>`-ээр. Бүх зүйл text input-тэй адилхан:
`value` + `onChange` + `e.target.value`. `<option>`-д `value` өгөөгүй бол
түүний текст нь утга болно.

### checkbox — value биш checked

```jsx
const [agree, setAgree] = useState(false);

<label>
  <input
    type="checkbox"
    checked={agree}
    onChange={(e) => setAgree(e.target.checked)}
  />
  Нөхцөлийг зөвшөөрч байна
</label>
```

Checkbox-ийн `value` чагтласан ч, чагтлаагүй ч өөрчлөгддөггүй (анхдагч нь
`"on"`). Чагтлагдсан эсэхийг `e.target.checked` (`true`/`false`) хэлнэ.
Тиймээс state нь boolean, prop нь `checked`.

### radio — нэг бүлэг, нэг state

```jsx
const [delivery, setDelivery] = useState("courier");

<label>
  <input
    type="radio"
    name="delivery"
    value="courier"
    checked={delivery === "courier"}
    onChange={(e) => setDelivery(e.target.value)}
  />
  Хүргэлтээр
</label>
<label>
  <input
    type="radio"
    name="delivery"
    value="pickup"
    checked={delivery === "pickup"}
    onChange={(e) => setDelivery(e.target.value)}
  />
  Очиж авна
</label>
```

Radio-д `value` нь тухайн сонголтын утга, `checked` нь «энэ сонгогдсон уу»
гэсэн асуулт. Ижил `name` нь тэднийг нэг бүлэг болгоно: нэгийг сонгоход
нөгөө нь автоматаар цуцлагдана, сумтай товчоор шилжинэ.

Сонголт олон бол массиваас `map`-аар үүсгэвэл давталтгүй:

```jsx
const OPTIONS = [
  { value: "courier", label: "Хүргэлтээр" },
  { value: "pickup", label: "Очиж авна" },
];

{OPTIONS.map((option) => (
  <label key={option.value}>
    <input
      type="radio"
      name="delivery"
      value={option.value}
      checked={delivery === option.value}
      onChange={(e) => setDelivery(e.target.value)}
    />
    {option.label}
  </label>
))}
```

### Нэг handleChange бүх төрөлд

Өмнөх хичээлийн handler-ийг checkbox-д зориулж жаахан өргөтгөнө:

```jsx
function handleChange(e) {
  const { name, value, type, checked } = e.target;
  setForm({ ...form, [name]: type === "checkbox" ? checked : value });
}
```

Одоо text, select, radio, checkbox бүгд нэг функц хуваалцана.

### Түгээмэл алдаа

- Checkbox-оос `e.target.value` унших — үргэлж `"on"`.
- Radio-д `checked`-ийн оронд `value={delivery}` бичих — бүх radio ижил
  утгатай болж, сонголт ажиллахгүй.
- `checked` өгөөд `onChange` мартах — checkbox дарахад өөрчлөгдөхгүй.
- `<option selected>` бичих — React Console-д `value`-г `<select>`-д өг
  гэж анхааруулна.

```quiz
Энэ кодын дараа checkbox дарахад `agree` юу болох вэ? `<input type="checkbox" checked={agree} onChange={(e) => setAgree(e.target.value)} />`
- [ ] `true`, дахин дарахад `false`
- [x] `"on"` гэсэн текст — дахин дарсан ч өөрчлөгдөхгүй
- [ ] `undefined`
> Checkbox-ийн төлөвийг `e.target.checked` хэлнэ. `value` нь тогтмол `"on"`.
```

```quiz
Radio бүлэгт аль radio сонгогдсоныг React-д юугаар заах вэ?
- [ ] Бүх radio-д ижил `value={state}` өгнө
- [x] Radio бүрт `checked={state === тэр radio-гийн утга}`
- [ ] `<fieldset value={state}>`
> Radio бүр өөрийн тогтмол `value`-тэй, харин `checked` нь state-тэй харьцуулж тооцогдоно.
```

### Дүгнэлт

`<select>` нь text input шиг `value`-ээр удирдагдана. Checkbox-ийн төлөв
`checked` ба `e.target.checked`. Radio бүлэг нэг state хуваалцаж, radio
бүрийн `checked` нь `state === value`.
""",
            initial_code=vite(
                """\
import { useState } from "react";

const SIZES = [
  { value: "Жижиг", price: 4000 },
  { value: "Дунд", price: 5000 },
  { value: "Том", price: 6000 },
];

const MILKS = [
  { value: "Энгийн сүү", price: 0 },
  { value: "Овъёосны сүү", price: 800 },
  { value: "Сүүгүй", price: 0 },
];

const SHOT_PRICE = 1000;

export default function App() {
  const [order, setOrder] = useState({
    size: "Дунд",
    milk: "Энгийн сүү",
    extraShot: false,
  });

  function handleChange(e) {
    // TODO: select, radio-д e.target.value, checkbox-д e.target.checked-ийг
    //       order-ийн [e.target.name] талбарт хадгал
  }

  const total =
    SIZES.find((size) => size.value === order.size).price +
    MILKS.find((milk) => milk.value === order.milk).price +
    (order.extraShot ? SHOT_PRICE : 0);

  // TODO: select-д value, radio болон checkbox-д checked, бүгдэд onChange өг
  return (
    <main>
      <h1>☕ Кофе захиалга</h1>

      <label>
        Хэмжээ
        <select name="size">
          {SIZES.map((size) => (
            <option key={size.value} value={size.value}>
              {size.value}
            </option>
          ))}
        </select>
      </label>

      <fieldset>
        <legend>Сүү</legend>
        {MILKS.map((milk) => (
          <label key={milk.value}>
            <input type="radio" name="milk" value={milk.value} />
            {milk.value}
          </label>
        ))}
      </fieldset>

      <label>
        <input type="checkbox" name="extraShot" />
        Нэмэлт шот (+1000₮)
      </label>

      <section className="card">
        <p>
          Таны захиалга: {order.size}, {order.milk}
          {order.extraShot ? ", нэмэлт шоттой" : ""}
        </p>
        <p>Нийт: {total}₮</p>
      </section>
    </main>
  );
}
""",
                css=FORM_CSS,
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 10 минут

Кофе захиалгын формын талбарууд `order` state-тэй холбогдоогүй тул
захиалга, үнэ өөрчлөгдөхгүй байна. Хэмжээний `select`, сүүний radio бүлэг,
«Нэмэлт шот» checkbox-ийг `order`-оор удирдаж, нэг `handleChange` бич.
Нийт үнийг аль хэдийн state-ээс тооцоолж байгаа.
""",
                tests=(
                    test(
                        "Эхлэхэд «Дунд», «Энгийн сүү» сонгогдсон байна",
                        """
render(<App />);
expect(screen.getByLabelText("Хэмжээ")).toHaveValue("Дунд");
expect(screen.getByRole("radio", { name: "Энгийн сүү" })).toBeChecked();
expect(screen.getByRole("checkbox", { name: /Нэмэлт шот/ })).not.toBeChecked();
""",
                    ),
                    test(
                        "Хэмжээ сонгоход захиалга, үнэ шинэчлэгдэнэ",
                        """
render(<App />);
await user.selectOptions(screen.getByLabelText("Хэмжээ"), "Том");
expect(screen.text()).toContain("Таны захиалга: Том");
expect(screen.text()).toContain("Нийт: 6000₮");
""",
                    ),
                    test(
                        "Сүүний төрлийг radio-гоор сонгоно, нэг л radio сонгогдоно",
                        """
render(<App />);
await user.click(screen.getByRole("radio", { name: "Овъёосны сүү" }));
expect(screen.getByRole("radio", { name: "Овъёосны сүү" })).toBeChecked();
expect(screen.getByRole("radio", { name: "Энгийн сүү" })).not.toBeChecked();
expect(screen.text()).toContain("Овъёосны сүү");
expect(screen.text()).toContain("Нийт: 5800₮");
""",
                    ),
                    test(
                        "«Нэмэлт шот» checkbox үнэд нэмэгдэж, дахин дарахад хасагдана",
                        """
render(<App />);
const shot = screen.getByRole("checkbox", { name: /Нэмэлт шот/ });
await user.click(shot);
expect(shot).toBeChecked();
expect(screen.text()).toContain("нэмэлт шоттой");
expect(screen.text()).toContain("Нийт: 6000₮");
await user.click(shot);
expect(shot).not.toBeChecked();
expect(screen.text()).toContain("Нийт: 5000₮");
""",
                    ),
                ),
                tips="""\
- `handleChange` дотор `const { name, value, type, checked } = e.target;`,
  дараа нь `[name]: type === "checkbox" ? checked : value`.
- `<select name="size" value={order.size} onChange={handleChange}>`.
- Radio бүрт `checked={order.milk === milk.value}` — `value={order.milk}`
  биш. Radio-гийн `value` нь өөрийн тогтмол утга хэвээр үлдэнэ.
- Checkbox-д `checked={order.extraShot}`.
""",
                solution=solution(
                    App_jsx="""\
import { useState } from "react";

const SIZES = [
  { value: "Жижиг", price: 4000 },
  { value: "Дунд", price: 5000 },
  { value: "Том", price: 6000 },
];

const MILKS = [
  { value: "Энгийн сүү", price: 0 },
  { value: "Овъёосны сүү", price: 800 },
  { value: "Сүүгүй", price: 0 },
];

const SHOT_PRICE = 1000;

export default function App() {
  const [order, setOrder] = useState({
    size: "Дунд",
    milk: "Энгийн сүү",
    extraShot: false,
  });

  function handleChange(e) {
    const { name, value, type, checked } = e.target;
    setOrder({ ...order, [name]: type === "checkbox" ? checked : value });
  }

  const total =
    SIZES.find((size) => size.value === order.size).price +
    MILKS.find((milk) => milk.value === order.milk).price +
    (order.extraShot ? SHOT_PRICE : 0);

  return (
    <main>
      <h1>☕ Кофе захиалга</h1>

      <label>
        Хэмжээ
        <select name="size" value={order.size} onChange={handleChange}>
          {SIZES.map((size) => (
            <option key={size.value} value={size.value}>
              {size.value}
            </option>
          ))}
        </select>
      </label>

      <fieldset>
        <legend>Сүү</legend>
        {MILKS.map((milk) => (
          <label key={milk.value}>
            <input
              type="radio"
              name="milk"
              value={milk.value}
              checked={order.milk === milk.value}
              onChange={handleChange}
            />
            {milk.value}
          </label>
        ))}
      </fieldset>

      <label>
        <input
          type="checkbox"
          name="extraShot"
          checked={order.extraShot}
          onChange={handleChange}
        />
        Нэмэлт шот (+1000₮)
      </label>

      <section className="card">
        <p>
          Таны захиалга: {order.size}, {order.milk}
          {order.extraShot ? ", нэмэлт шоттой" : ""}
        </p>
        <p>Нийт: {total}₮</p>
      </section>
    </main>
  );
}
"""
                ),
            ),
        ),
        # --- 4 ------------------------------------------------------------------
        LessonSpec(
            title="Форм илгээх",
            slug="form-ilgeeh",
            description="onSubmit, preventDefault, илгээсний дараа цэвэрлэх ба идэвхгүй товч.",
            duration=840,
            language=JSX,
            content="""\
### Энэ хичээлээр

- `<form onSubmit>`-оор илгээлтийг барих
- `e.preventDefault()` яагаад хэрэгтэйг ойлгох
- Илгээсний дараа талбаруудыг цэвэрлэх
- Бөглөөгүй үед илгээх товчийг идэвхгүй болгох

### Яагаад чухал вэ

Хэрэглэгч формыг хоёр янзаар илгээдэг: товч дарах, эсвэл талбарт Enter
дарах. Хоёуланг нь, мөн дэлгэц уншигч, гарын товчлол зэргийг зөв дэмжих
хамгийн хялбар арга бол HTML-ийн `<form>` элемент ба түүний **submit**
event. Товч бүрийн `onClick`-ээр «гараар» барих гэж оролдвол Enter ажиллахгүй
болох зэрэг жижиг алдаа олон гарна.

### onSubmit, onClick биш

```jsx
function handleSubmit(e) {
  e.preventDefault();
  addComment(text);
  setText("");
}

return (
  <form onSubmit={handleSubmit}>
    <input value={text} onChange={(e) => setText(e.target.value)} />
    <button type="submit">Нэмэх</button>
  </form>
);
```

`onSubmit` нь `<form>` дээр байна. Товч дарах ч, талбарт Enter дарах ч
ижил `handleSubmit` ажиллана.

`<form>` доторх `<button>` анхдагчаар `type="submit"`. Тиймээс форм доторх
өөр үйлдэлтэй товчинд (жишээ нь «Цуцлах») `type="button"` заавал бичнэ —
эс бөгөөс тэр товч ч формыг илгээнэ.

### e.preventDefault()

Хөтөч формыг илгээхдээ анхдагчаар **хуудсыг дахин ачаална** (эсвэл
`action` хаяг руу шилжинэ). Энэ нь 1990-ээд оны, сервер бүх хуудсыг
шинээр буцаадаг вэбийн зан үйл. React апп-д хуудас дахин ачаалагдвал бүх
state алга болно. `e.preventDefault()` энэ анхдагч үйлдлийг зогсоож, бид
өгөгдлийг өөрсдөө боловсруулна.

Энэ sandbox хуудсыг дахин ачаалахгүй, харин Console-д «Форм илгээгдэж
хуудас дахин ачаалагдах гэлээ — onSubmit дотор e.preventDefault()
дуудаагүй байна.» гэсэн анхааруулга гарна. Жинхэнэ хөтөч дээр бол хуудас
анивчиж, бичсэн бүхэн алга болно.

React 19 нь `<form action={fn}>` гэсэн шинэ арга нэмсэн (Модул 11). Одоохондоо
`onSubmit` + `preventDefault` — хамгийн өргөн хэрэглэгддэг, үндсэн хэлбэр.

### Илгээсний дараа цэвэрлэх

Input controlled тул state-ийг хоосон болгоход л хангалттай:
`setText("")`. Олон талбартай бол анхны утгыг component-оос гадна тогтмол
болгож хадгалаад, түүнийгээ буцааж онооно:

```jsx
const INITIAL = { name: "", email: "" };

// handleSubmit дотор
setForm(INITIAL);
```

### Идэвхгүй товч

```jsx
const isEmpty = text.trim() === "";

<button type="submit" disabled={isEmpty}>Нэмэх</button>
```

`disabled`-ийн утгыг state-ээс тооцоолно — тусдаа state хэрэггүй (Модул
3-ын derived value). `trim()` нь зөвхөн зайнаас тогтсон текстийг хоосонд
тооцно. Найдвартай байхын тулд `handleSubmit` дотор ч
`if (isEmpty) return;` гэж шалгах нь зүгээр.

### Түгээмэл алдаа

- `<form>`-гүй, товчны `onClick` — Enter дарахад юу ч болохгүй.
- `e.preventDefault()`-ийг мартах — жинхэнэ хөтөч дээр хуудас дахин
  ачаалагдана.
- `onSubmit={handleSubmit()}` — функцийг дамжуулахын оронд render үед нь
  дуудчихна.
- Форм доторх «Цуцлах» товчинд `type="button"` бичихээ мартах.

```quiz
Форм дотор `<button onClick={() => setOpen(false)}>Цуцлах</button>` байна. Үүнийг дарахад юу болох вэ?
- [ ] Зөвхөн `setOpen(false)` ажиллана
- [x] `setOpen(false)`-ийн дараа форм бас илгээгдэнэ
- [ ] Юу ч болохгүй
> Форм доторх `type`-гүй товч бол submit товч. `type="button"` бичих ёстой.
```

```quiz
`handleSubmit` дотор `e.preventDefault()` байхгүй бол жинхэнэ хөтөч дээр юу болох вэ?
- [ ] Юу ч болохгүй, React өөрөө зогсооно
- [x] Хуудас дахин ачаалагдаж, state бүхэлдээ алга болно
- [ ] React алдаа шидэнэ
> Формын анхдагч үйлдэл нь хуудсыг илгээж дахин ачаалах. React үүнийг өөрөө зогсоодоггүй.
```

### Дүгнэлт

Формыг `<form onSubmit>`-оор барьж, эхний мөрөнд `e.preventDefault()`
дуудна. Илгээсний дараа state-ийг анхны утгаар нь солиход талбарууд
цэвэрлэгдэнэ. Товчны `disabled`-ийг state-ээс тооцоолно.
""",
            initial_code=vite(
                """\
import { useState } from "react";

let nextId = 2;

export default function App() {
  const [comments, setComments] = useState([
    { id: 1, text: "Маш ойлгомжтой хичээл байлаа!" },
  ]);
  const [text, setText] = useState("");

  // TODO 1: handleSubmit — preventDefault, сэтгэгдэл нэмэх, талбарыг цэвэрлэх
  // TODO 2: <div>-ийг <form onSubmit={…}> болго
  // TODO 3: талбар хоосон (эсвэл зөвхөн зай) үед «Нэмэх» товч идэвхгүй

  return (
    <main>
      <h1>💬 Сэтгэгдэл</h1>
      <ul>
        {comments.map((comment) => (
          <li key={comment.id}>{comment.text}</li>
        ))}
      </ul>

      <div>
        <label>
          Сэтгэгдэл
          <input value={text} onChange={(e) => setText(e.target.value)} />
        </label>
        <button>Нэмэх</button>
      </div>
    </main>
  );
}
""",
                css=FORM_CSS,
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 10 минут

Сэтгэгдэл нэмэх хэсгийг жинхэнэ форм болго: илгээхэд шинэ сэтгэгдэл
жагсаалтын төгсгөлд нэмэгдэж, талбар цэвэрлэгдэнэ. Талбар хоосон (эсвэл
зөвхөн зайтай) үед «Нэмэх» товч идэвхгүй байна. Илгээхэд Console-д
`preventDefault`-ийн анхааруулга гарах ёсгүй.
""",
                tests=(
                    test(
                        "«Нэмэх» дарахад сэтгэгдэл жагсаалтад нэмэгдэнэ",
                        """
render(<App />);
await user.type(screen.getByLabelText("Сэтгэгдэл"), "Гоё хичээл");
await user.click(screen.getByRole("button", { name: "Нэмэх" }));
const items = screen.getAllByRole("listitem");
expect(items).toHaveLength(2);
expect(items[1]).toHaveTextContent("Гоё хичээл");
""",
                    ),
                    test(
                        "Талбарт Enter дарахад ч илгээгдэнэ",
                        """
render(<App />);
await user.type(screen.getByLabelText("Сэтгэгдэл"), "Enter-ээр илгээв{enter}");
expect(screen.text()).toContain("Enter-ээр илгээв");
expect(screen.getAllByRole("listitem")).toHaveLength(2);
""",
                    ),
                    test(
                        "Илгээсний дараа талбар хоосорно",
                        """
render(<App />);
const input = screen.getByLabelText("Сэтгэгдэл");
await user.type(input, "Баярлалаа");
await user.click(screen.getByRole("button", { name: "Нэмэх" }));
expect(screen.text()).toContain("Баярлалаа");
expect(input).toHaveValue("");
""",
                    ),
                    test(
                        "Талбар хоосон эсвэл зөвхөн зайтай үед «Нэмэх» идэвхгүй",
                        """
render(<App />);
const button = screen.getByRole("button", { name: "Нэмэх" });
expect(button).toBeDisabled();
await user.type(screen.getByLabelText("Сэтгэгдэл"), "   ");
expect(button).toBeDisabled();
await user.type(screen.getByLabelText("Сэтгэгдэл"), "а");
expect(button).toBeEnabled();
""",
                    ),
                    test(
                        "Илгээхэд хуудас дахин ачаалагдахгүй (preventDefault)",
                        """
render(<App />);
await user.type(screen.getByLabelText("Сэтгэгдэл"), "Туршилт");
await user.click(screen.getByRole("button", { name: "Нэмэх" }));
expect(screen.text()).toContain("Туршилт");
const warned = logs.some((entry) => entry.text.includes("preventDefault"));
expect(warned).toBe(false);
""",
                    ),
                ),
                tips="""\
- `<div>`-ийг `<form onSubmit={handleSubmit}>` болгосноор Enter автоматаар
  ажиллана. Товчинд `onClick` хэрэггүй, `type="submit"` хангалттай.
- `handleSubmit`-ийн эхний мөр: `e.preventDefault();`.
- Шинэ сэтгэгдэл: `setComments([...comments, { id: nextId++, text }])`,
  дараа нь `setText("")`.
- Хоосон эсэхийг тооцоол: `const isEmpty = text.trim() === "";` →
  `disabled={isEmpty}`. `trim()`-гүй бол зай бичихэд товч идэвхжинэ.
""",
                solution=solution(
                    App_jsx="""\
import { useState } from "react";

let nextId = 2;

export default function App() {
  const [comments, setComments] = useState([
    { id: 1, text: "Маш ойлгомжтой хичээл байлаа!" },
  ]);
  const [text, setText] = useState("");

  const isEmpty = text.trim() === "";

  function handleSubmit(e) {
    e.preventDefault();
    if (isEmpty) return;
    setComments([...comments, { id: nextId++, text: text.trim() }]);
    setText("");
  }

  return (
    <main>
      <h1>💬 Сэтгэгдэл</h1>
      <ul>
        {comments.map((comment) => (
          <li key={comment.id}>{comment.text}</li>
        ))}
      </ul>

      <form onSubmit={handleSubmit}>
        <label>
          Сэтгэгдэл
          <input value={text} onChange={(e) => setText(e.target.value)} />
        </label>
        <button type="submit" disabled={isEmpty}>
          Нэмэх
        </button>
      </form>
    </main>
  );
}
"""
                ),
            ),
        ),
        # --- 5 ------------------------------------------------------------------
        LessonSpec(
            title="Баталгаажуулалт ба алдааны төлөв",
            slug="form-batalgaajuulalt",
            description="validate функц, errors объект, touched төлвөөр алдааг зөв үед нь харуулна.",
            duration=960,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Формын дүрмүүдийг нэг `validate(values)` функцэд бичих
- Алдааг `errors` объектоор илэрхийлэх
- Алдааг илгээх үед болон талбараас гарах (blur) үед харуулах
- `touched` төлвөөр хэрэглэгчийг хэт эрт «загнахгүй» байх

### Яагаад чухал вэ

Буруу утасны дугаар, хоосон нэр сервер рүү очихоос өмнө хэрэглэгчид хурдан,
ойлгомжтой хариу өгөх хэрэгтэй. Гэхдээ хэрэглэгч бичиж амжаагүй байхад
бүх талбарын доор улаан алдаа гаргах нь муу туршлага. Тэгэхээр хоёр асуулт
бий: **юу алдаа вэ** (дүрэм), **хэзээ харуулах вэ** (UX).

Анхаар: хөтөч дээрх шалгалт нь хэрэглэгчид туслах зорилготой. Хэн ч
хөтчийг тойрч сервер рүү шууд хүсэлт илгээж чадна — сервер өөрөө бас
шалгах ёстой.

### validate — цэвэр функц

```jsx
function validate(values) {
  const errors = {};
  if (values.name.trim() === "") {
    errors.name = "Нэрээ оруулна уу";
  }
  if (!/^[0-9]{8}$/.test(values.phone)) {
    errors.phone = "Утасны дугаар 8 оронтой байна";
  }
  return errors;
}
```

- Оролт нь утгууд, гаралт нь алдааны объект. Side effect-гүй тул
  component-оос гадна бичиж, дангаар нь тестэлж болно.
- Алдаагүй бол хоосон объект: `Object.keys(errors).length === 0`.
- `/^[0-9]{8}$/` — эхнээс төгсгөл хүртэл яг 8 цифр.

### errors-ийг state-д хадгалах уу?

Үгүй. Алдаа нь утгуудаас бүрэн **тооцоолж болох** зүйл (Модул 3-ын
derived value). Render бүрт шинээр тооцвол утга, алдаа хэзээ ч зөрөхгүй:

```jsx
const [values, setValues] = useState({ name: "", phone: "" });
const [touched, setTouched] = useState({});
const [submitted, setSubmitted] = useState(false);

const errors = validate(values);
```

State-д зөвхөн «хэзээ харуулах» мэдээлэл үлдэнэ: аль талбарт хүрсэн
(`touched`), илгээх гэж оролдсон эсэх (`submitted`).

### Blur — талбараас гарах үед

```jsx
function handleBlur(e) {
  setTouched({ ...touched, [e.target.name]: true });
}

function showError(field) {
  return (touched[field] || submitted) && errors[field];
}

<input name="phone" value={values.phone} onChange={handleChange} onBlur={handleBlur} />
{showError("phone") && <p className="error">{errors.phone}</p>}
```

`onBlur` нь фокус талбараас гарахад ажиллана: хэрэглэгч бичиж дуусаад
дараагийн талбар руу шилжсэн гэсэн үг. Алдаа нэг харагдсаны дараа
`errors` render бүрт шинээр тооцогддог тул хэрэглэгч засах мөчид алга
болно.

### Илгээх үед

```jsx
function handleSubmit(e) {
  e.preventDefault();
  setSubmitted(true);
  if (Object.keys(errors).length > 0) return;
  // алдаагүй — илгээнэ
}
```

`submitted` нь хэрэглэгчийн хүрээгүй талбаруудын алдааг ч харуулна.
`errors`-ийг state биш тооцоолсон хувьсагч болгосон тул энд хамгийн сүүлийн
утгыг шууд уншиж болно.

### Хэзээ харуулах вэ

| Хэзээ | Давуу тал | Сул тал |
|---|---|---|
| Үсэг бүрт | Хамгийн хурдан хариу | Эхний үсгээс л улаан алдаа |
| Blur | Бичиж дууссаны дараа | Нэг алхам хоцорно |
| Илгээх үед | Тайван | Хэт хоцорсон, олон алдаа нэг дор |

Түгээмэл сонголт: **blur + илгээх**, алдаа гарсны дараа үсэг бүрт
шинэчлэгдэнэ. Бодит төсөлд React Hook Form, Formik зэрэг сан, Zod зэрэг
schema ашигладаг ч дотор нь яг энэ санаа.

### Түгээмэл алдаа

- `errors`-ийг state-д хадгалж, утга өөрчлөгдөхөд шинэчлэхээ мартах.
- `setSubmitted(true)`-ийн дараа шууд `submitted`-ийг унших — snapshot
  тул хуучин утга (`false`) хэвээр байна.
- Эхний render-ээс бүх алдааг харуулах.

```quiz
`validate({ name: "", phone: "99112233" })` юу буцаах вэ?
- [ ] `{}`
- [x] `{ name: "Нэрээ оруулна уу" }`
- [ ] `{ name: "Нэрээ оруулна уу", phone: "Утасны дугаар 8 оронтой байна" }`
> Утас яг 8 цифр тул зөвхөн нэрийн алдаа үлдэнэ.
```

```quiz
Хэрэглэгч «Нэр» дээр дараад, юу ч бичилгүй «Утас» руу шилжив. Ямар алдаа харагдах вэ?
- [x] Зөвхөн «Нэрээ оруулна уу»
- [ ] Хоёр алдаа хоёулаа
- [ ] Ямар ч алдаа харагдахгүй
> «Нэр» touched болсон, «Утас»-т хүрээгүй хэвээр. Form илгээгээгүй тул `submitted` худал.
```

### Дүгнэлт

Дүрмийг цэвэр `validate` функцэд бичиж, `errors`-ийг render бүрт
тооцоолно. State-д зөвхөн `touched`, `submitted` хадгалж, алдааг
«хүрсэн эсвэл илгээсэн» үед л харуулна.
""",
            initial_code=vite(
                """\
import { useState } from "react";

export function validate(values) {
  const errors = {};
  // TODO: нэр хоосон (зөвхөн зай ч гэсэн) бол errors.name = "Нэрээ оруулна уу"
  // TODO: утас яг 8 цифр биш бол errors.phone = "Утасны дугаар 8 оронтой байна"
  return errors;
}

export default function App() {
  const [values, setValues] = useState({ name: "", phone: "" });
  const [touched, setTouched] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const [sent, setSent] = useState(false);

  const errors = validate(values);

  function handleChange(e) {
    setValues({ ...values, [e.target.name]: e.target.value });
  }

  // TODO: handleBlur — тухайн талбарыг touched болго

  function handleSubmit(e) {
    e.preventDefault();
    // TODO: submitted-ийг true болго; алдаагүй бол sent-ийг true болго
  }

  // TODO: талбар touched эсвэл submitted, мөн алдаатай үед л алдааг харуул

  if (sent) {
    return <p className="card">✅ Захиалга амжилттай илгээгдлээ!</p>;
  }

  return (
    <form onSubmit={handleSubmit} noValidate>
      <h1>🚚 Хүргэлтийн мэдээлэл</h1>

      <label>
        Нэр
        <input name="name" value={values.name} onChange={handleChange} />
      </label>

      <label>
        Утас
        <input name="phone" type="tel" value={values.phone} onChange={handleChange} />
      </label>

      <button type="submit">Илгээх</button>
    </form>
  );
}
""",
                css=FORM_CSS,
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐ · 15 минут

Хүргэлтийн формд баталгаажуулалт нэм. Эхлээд `validate` функцийг
сэтгэгдэлд бичсэн дүрэм, мессежээр гүйцээ. Дараа нь алдааг зөв үед нь
харуул: хэрэглэгч талбараас гарсны (blur) дараа, эсвэл илгээх гэж
оролдсон үед. Алдаагүй бол илгээхэд амжилтын мэдэгдэл гарна.
""",
                tests=(
                    test(
                        "validate нь дүрэм зөрчсөн талбар бүрт алдаа буцаана",
                        """
const { validate } = mod("./App");
expect(validate({ name: "", phone: "123" })).toEqual({
  name: "Нэрээ оруулна уу",
  phone: "Утасны дугаар 8 оронтой байна",
});
expect(validate({ name: "   ", phone: "9911223a" })).toEqual({
  name: "Нэрээ оруулна уу",
  phone: "Утасны дугаар 8 оронтой байна",
});
expect(validate({ name: "Бат", phone: "99112233" })).toEqual({});
""",
                    ),
                    test(
                        "Эхлээд алдаа харагдахгүй, хоосон илгээхэд хоёр алдаа хоёулаа гарна",
                        """
render(<App />);
expect(screen.text()).not.toContain("Нэрээ оруулна уу");
expect(screen.text()).not.toContain("8 оронтой");
await user.click(screen.getByRole("button", { name: "Илгээх" }));
expect(screen.text()).toContain("Нэрээ оруулна уу");
expect(screen.text()).toContain("Утасны дугаар 8 оронтой байна");
expect(screen.text()).not.toMatch(/амжилттай/i);
""",
                    ),
                    test(
                        "Талбараас гарахад (blur) зөвхөн тэр талбарын алдаа харагдана",
                        """
render(<App />);
const name = screen.getByLabelText("Нэр");
await user.click(name);
await act(async () => {
  name.dispatchEvent(new FocusEvent("focusout", { bubbles: true }));
});
expect(screen.text()).toContain("Нэрээ оруулна уу");
expect(screen.text()).not.toContain("8 оронтой");
""",
                    ),
                    test(
                        "Алдааг зассан даруйд тэр алдаа алга болно",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: "Илгээх" }));
await user.type(screen.getByLabelText("Нэр"), "Бат");
expect(screen.text()).not.toContain("Нэрээ оруулна уу");
expect(screen.text()).toContain("Утасны дугаар 8 оронтой байна");
""",
                    ),
                    test(
                        "Зөв бөглөж илгээхэд амжилтын мэдэгдэл гарна",
                        """
render(<App />);
await user.type(screen.getByLabelText("Нэр"), "Бат");
await user.type(screen.getByLabelText("Утас"), "99112233");
await user.click(screen.getByRole("button", { name: "Илгээх" }));
expect(screen.text()).toMatch(/амжилттай/i);
""",
                    ),
                ),
                tips="""\
- `validate`: `values.name.trim() === ""`, утсанд `/^[0-9]{8}$/.test(values.phone)`.
  Мессежийг яг сэтгэгдэлд бичсэнээр нь хуул.
- `handleBlur`: `setTouched({ ...touched, [e.target.name]: true })`, input
  бүрт `onBlur={handleBlur}`.
- Харуулах нөхцөл: `(touched.name || submitted) && errors.name`.
- `handleSubmit` дотор `errors` нь аль хэдийн тооцоологдсон — state биш тул
  хуучирдаггүй: `if (Object.keys(errors).length === 0) setSent(true);`
- `errors`-ийг state болгох шаардлагагүй — утгаас render бүрт тооцоологдоно.
""",
                solution=solution(
                    App_jsx="""\
import { useState } from "react";

export function validate(values) {
  const errors = {};
  if (values.name.trim() === "") {
    errors.name = "Нэрээ оруулна уу";
  }
  if (!/^[0-9]{8}$/.test(values.phone)) {
    errors.phone = "Утасны дугаар 8 оронтой байна";
  }
  return errors;
}

export default function App() {
  const [values, setValues] = useState({ name: "", phone: "" });
  const [touched, setTouched] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const [sent, setSent] = useState(false);

  const errors = validate(values);

  function handleChange(e) {
    setValues({ ...values, [e.target.name]: e.target.value });
  }

  function handleBlur(e) {
    setTouched({ ...touched, [e.target.name]: true });
  }

  function handleSubmit(e) {
    e.preventDefault();
    setSubmitted(true);
    if (Object.keys(errors).length === 0) {
      setSent(true);
    }
  }

  function showError(field) {
    return (touched[field] || submitted) && errors[field];
  }

  if (sent) {
    return <p className="card">✅ Захиалга амжилттай илгээгдлээ!</p>;
  }

  return (
    <form onSubmit={handleSubmit} noValidate>
      <h1>🚚 Хүргэлтийн мэдээлэл</h1>

      <label>
        Нэр
        <input name="name" value={values.name} onChange={handleChange} onBlur={handleBlur} />
      </label>
      {showError("name") && <p className="error">{errors.name}</p>}

      <label>
        Утас
        <input
          name="phone"
          type="tel"
          value={values.phone}
          onChange={handleChange}
          onBlur={handleBlur}
        />
      </label>
      {showError("phone") && <p className="error">{errors.phone}</p>}

      <button type="submit">Илгээх</button>
    </form>
  );
}
"""
                ),
            ),
        ),
        # --- 6 ------------------------------------------------------------------
        LessonSpec(
            title="Формын хүртээмж",
            slug="form-hurteemj",
            description="label, required, aria-invalid, aria-describedby ба role=alert-оор хүн бүрт ойлгомжтой форм бүтээнэ.",
            duration=900,
            language=JSX,
            content="""\
### Энэ хичээлээр

- `<label>`-ийг `htmlFor`-оор талбартай холбох
- `required`, `aria-invalid`-ээр талбарын төлвийг илэрхийлэх
- `aria-describedby`-гаар алдааны текстийг талбартай холбох
- `role="alert"`-оор алдааг дэлгэц уншигчид мэдэгдэх

### Яагаад чухал вэ

Хараагүй, харааны бэрхшээлтэй хүмүүс **дэлгэц уншигч** (screen reader:
NVDA, VoiceOver, TalkBack) ашиглана. Label-гүй, алдааг зөвхөн улаан өнгөөр
харуулсан форм тэдэнд «засварлах талбар, хоосон» гэж л сонсогдоно — юу
бичих, юу буруу байгааг мэдэх боломжгүй.

Хүртээмж бүгдэд ашигтай: label дээр дарахад талбар идэвхждэг тул утсан
дээр жижиг checkbox дарахад хялбар, гараар (Tab) бүх талбарыг тойрч
болно. Бас нэг давуу тал: Testing Library талбарыг хэрэглэгч шиг
**label-аар нь** хайдаг (`getByLabelText`). Хүртээмжтэй форм тестлэхэд ч
хялбар.

### label ба htmlFor

Өмнөх хичээлүүдэд input-ийг label дотор бичсэн — энэ нь холбох нэг арга.
Нөгөө арга нь `id`-аар холбох:

```jsx
<label htmlFor="email">Имэйл</label>
<input id="email" name="email" type="email" />
```

JSX-д `for` биш **`htmlFor`** гэж бичнэ, учир нь `for` нь JavaScript-ийн
түлхүүр үг (`class` → `className`-тэй адил шалтгаан).

`id` хуудсанд давхцах ёсгүй. Нэг component хуудсанд хэд хэд гарвал
React-ийн `useId()` hook давтагдашгүй id үүсгэнэ:

```jsx
const id = useId();

<label htmlFor={id}>Имэйл</label>
<input id={id} />
```

**Placeholder нь label биш.** Бичиж эхлэхэд алга болж, ихэвчлэн бүдэг
өнгөтэй, дэлгэц уншигч заримдаа уншдаггүй. Placeholder-ийг зөвхөн жишээ
(«bat@example.mn») өгөхөд хэрэглэ.

### required ба noValidate

`required` нь талбарыг заавал бөглөх ёстой гэж хөтөч, дэлгэц уншигчид
хэлнэ («Имэйл, шаардлагатай, засварлах талбар»).

Анхаар: `required`, `type="email"` нь хөтчийн өөрийн шалгалтыг
идэвхжүүлнэ. Талбар буруу бол хөтөч өөрийн бөмбөлгийг гаргаж, **`onSubmit`
огт ажиллахгүй**. Өөрсдийн алдааны мэдэгдлийг харуулах бол формд
`noValidate` нэмнэ — хөтчийн шалгалт унтарч, `required`-ийн утга
хадгалагдана:

```jsx
<form onSubmit={handleSubmit} noValidate>
```

### aria-invalid ба aria-describedby

```jsx
<label htmlFor="email">Имэйл</label>
<input
  id="email"
  type="email"
  required
  aria-invalid={error ? true : undefined}
  aria-describedby={error ? "email-error" : undefined}
/>
{error && (
  <p id="email-error" className="error" role="alert">
    {error}
  </p>
)}
```

- `aria-invalid="true"` — «энэ талбар алдаатай» гэж мэдэгдэнэ.
- `aria-describedby` — алдааны элементийн `id`-г заана. Талбар дээр фокус
  очиход дэлгэц уншигч нэрийн дараа тайлбарыг уншина: «Имэйл, алдаатай,
  Имэйлээ зөв оруулна уу».
- `role="alert"` — элемент гарч ирэхэд дэлгэц уншигч бусдыг таслаад шууд
  уншина.
- Алдааг зөвхөн өнгөөр биш, **текстээр** илэрхийл — өнгө ялгадаггүй хүмүүс
  бий.

Алдаагүй үед `undefined` өгвөл React тэр attribute-ийг огт бичихгүй.

### Шалгах арга

- Хулгана хэрэглэхгүйгээр зөвхөн Tab, Enter-ээр формоо бөглөж үз.
- Хөтчийн DevTools → Accessibility хэсэгт талбар бүрийн нэр (name),
  тайлбарыг (description) хар.
- Lighthouse, axe зэрэг хэрэгсэл label-гүй талбарыг автоматаар илрүүлнэ.

Илгээхэд алдаа гарвал эхний алдаатай талбар руу фокус шилжүүлэх нь бас
сайн туршлага — үүнийг `useRef`-ээр хийхийг Модул 6-д үзнэ.

```quiz
Аль нь JSX-д label-ийг input-тэй зөв холбох вэ?
- [ ] `<label for="name">`
- [x] `<label htmlFor="name">`
- [ ] `<label forName="name">`
> JSX-д `for` нь `htmlFor`, `class` нь `className` болдог.
```

```quiz
Энэ кодын хүртээмжийн алдааг ол: `<input placeholder="Имэйл" />` ба доор нь `<p style={{ color: "red" }}>Буруу имэйл</p>`
- [ ] Алдаа байхгүй — placeholder нь label болно
- [x] Label алга, алдааны текст талбартай холбогдоогүй тул дэлгэц уншигч тэр хоёрыг холбож чадахгүй
- [ ] Улаан өнгө хангалттай
> Label (`htmlFor`), `aria-invalid`, `aria-describedby`, `role="alert"` хэрэгтэй.
```

### Дүгнэлт

Талбар бүр `htmlFor`-оор холбогдсон label-тай. Алдаатай талбар
`aria-invalid="true"` бөгөөд `aria-describedby`-гаар алдааны текстээ заана,
алдаа нь `role="alert"`. Өөрийн мессежийг харуулахын тулд формд
`noValidate`.
""",
            initial_code=vite(
                """\
import { useState } from "react";

function validate(values) {
  const errors = {};
  if (values.name.trim() === "") {
    errors.name = "Нэрээ оруулна уу";
  }
  if (!/^[^@ ]+@[^@ ]+[.][^@ ]+$/.test(values.email)) {
    errors.email = "Имэйлээ зөв оруулна уу";
  }
  return errors;
}

export default function App() {
  const [values, setValues] = useState({ name: "", email: "" });
  const [submitted, setSubmitted] = useState(false);
  const [done, setDone] = useState(false);

  const errors = submitted ? validate(values) : {};

  function handleChange(e) {
    setValues({ ...values, [e.target.name]: e.target.value });
  }

  function handleSubmit(e) {
    e.preventDefault();
    setSubmitted(true);
    if (Object.keys(validate(values)).length === 0) {
      setDone(true);
    }
  }

  if (done) {
    return <p className="card">🎉 Бүртгэгдлээ! Баярлалаа, {values.name}.</p>;
  }

  // TODO: label-уудыг htmlFor-оор холбо, талбаруудыг required болго,
  //       алдаатай талбарт aria-invalid, aria-describedby нэм,
  //       алдааны мэдэгдлийг role="alert" болго. Формд noValidate хэрэгтэй.
  return (
    <form onSubmit={handleSubmit}>
      <h1>📰 Мэдээллийн товхимол</h1>

      <label>Нэр</label>
      <input id="name" name="name" value={values.name} onChange={handleChange} />
      {errors.name && <p className="error">{errors.name}</p>}

      <label>Имэйл</label>
      <input
        id="email"
        name="email"
        type="email"
        value={values.email}
        onChange={handleChange}
      />
      {errors.email && <p className="error">{errors.email}</p>}

      <button type="submit">Бүртгүүлэх</button>
    </form>
  );
}
""",
                css=FORM_CSS,
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐ · 12 минут

Товхимлын бүртгэлийн форм ажиллаж байгаа ч дэлгэц уншигч хэрэглэгчид
ойлгомжгүй: label нь талбартайгаа холбогдоогүй, алдаа зөвхөн улаан
текстээр харагдана. Хичээлд үзсэн attribute-уудаар формыг хүртээмжтэй
болго. Баталгаажуулалтын логик бэлэн — зөвхөн JSX-ийг засна.
""",
                tests=(
                    test(
                        "Талбарууд label-аараа олдоно (htmlFor)",
                        """
render(<App />);
expect(screen.getByLabelText("Нэр")).toHaveAttribute("name", "name");
expect(screen.getByLabelText("Имэйл")).toHaveAttribute("name", "email");
""",
                    ),
                    test(
                        "Хоёр талбар хоёулаа заавал бөглөх (required) гэж тэмдэглэгдсэн",
                        """
render(<App />);
for (const label of ["Нэр", "Имэйл"]) {
  const input = screen.getByLabelText(label);
  const required = input.required || input.getAttribute("aria-required") === "true";
  expect(required).toBe(true);
}
""",
                    ),
                    test(
                        'Алдаатай талбар aria-invalid="true" болж, aria-describedby-гаар алдааны текстээ заана',
                        """
render(<App />);
await user.type(screen.getByLabelText("Имэйл"), "bat.example.mn");
await user.click(screen.getByRole("button", { name: "Бүртгүүлэх" }));
const described = (input) =>
  (input.getAttribute("aria-describedby") ?? "")
    .split(" ")
    .map((id) => document.getElementById(id)?.textContent ?? "")
    .join(" ");
const name = screen.getByLabelText("Нэр");
const email = screen.getByLabelText("Имэйл");
expect(name).toHaveAttribute("aria-invalid", "true");
expect(email).toHaveAttribute("aria-invalid", "true");
expect(described(name)).toContain("Нэрээ оруулна уу");
expect(described(email)).toContain("Имэйлээ зөв оруулна уу");
""",
                    ),
                    test(
                        'Алдааны мэдэгдэл role="alert"-оор зарлагдана',
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: "Бүртгүүлэх" }));
const alerts = screen
  .getAllByRole("alert")
  .map((element) => element.textContent)
  .join(" ");
expect(alerts).toContain("Нэрээ оруулна уу");
expect(alerts).toContain("Имэйлээ зөв оруулна уу");
""",
                    ),
                    test(
                        "Зассан талбарын aria-invalid арилж, зөв бөглөхөд бүртгэгдэнэ",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: "Бүртгүүлэх" }));
await user.type(screen.getByLabelText("Нэр"), "Сараа");
expect(screen.getByLabelText("Нэр").getAttribute("aria-invalid")).not.toBe("true");
await user.type(screen.getByLabelText("Имэйл"), "saraa@example.mn");
await user.click(screen.getByRole("button", { name: "Бүртгүүлэх" }));
expect(screen.text()).toContain("Бүртгэгдлээ");
""",
                    ),
                ),
                tips="""\
- `<label htmlFor="name">` ба `<input id="name">` — `htmlFor` нь input-ийн
  `id`-тай яг ижил.
- `required` нэмсний дараа формд `noValidate` нэмэхээ бүү мартаарай. Эс
  бөгөөс буруу имэйлтэй үед хөтөч өөрөө илгээлтийг зогсоож, таны мессеж
  огт гарахгүй.
- Алдаатай үед: `aria-invalid={errors.email ? true : undefined}`,
  `aria-describedby={errors.email ? "email-error" : undefined}`.
- Алдааны `<p>`-д `id="email-error"` ба `role="alert"`.
""",
                solution=solution(
                    App_jsx="""\
import { useState } from "react";

function validate(values) {
  const errors = {};
  if (values.name.trim() === "") {
    errors.name = "Нэрээ оруулна уу";
  }
  if (!/^[^@ ]+@[^@ ]+[.][^@ ]+$/.test(values.email)) {
    errors.email = "Имэйлээ зөв оруулна уу";
  }
  return errors;
}

export default function App() {
  const [values, setValues] = useState({ name: "", email: "" });
  const [submitted, setSubmitted] = useState(false);
  const [done, setDone] = useState(false);

  const errors = submitted ? validate(values) : {};

  function handleChange(e) {
    setValues({ ...values, [e.target.name]: e.target.value });
  }

  function handleSubmit(e) {
    e.preventDefault();
    setSubmitted(true);
    if (Object.keys(validate(values)).length === 0) {
      setDone(true);
    }
  }

  if (done) {
    return <p className="card">🎉 Бүртгэгдлээ! Баярлалаа, {values.name}.</p>;
  }

  return (
    <form onSubmit={handleSubmit} noValidate>
      <h1>📰 Мэдээллийн товхимол</h1>

      <label htmlFor="name">Нэр</label>
      <input
        id="name"
        name="name"
        required
        value={values.name}
        onChange={handleChange}
        aria-invalid={errors.name ? true : undefined}
        aria-describedby={errors.name ? "name-error" : undefined}
      />
      {errors.name && (
        <p id="name-error" className="error" role="alert">
          {errors.name}
        </p>
      )}

      <label htmlFor="email">Имэйл</label>
      <input
        id="email"
        name="email"
        type="email"
        required
        value={values.email}
        onChange={handleChange}
        aria-invalid={errors.email ? true : undefined}
        aria-describedby={errors.email ? "email-error" : undefined}
      />
      {errors.email && (
        <p id="email-error" className="error" role="alert">
          {errors.email}
        </p>
      )}

      <button type="submit">Бүртгүүлэх</button>
    </form>
  );
}
"""
                ),
            ),
        ),
        # --- 7 ------------------------------------------------------------------
        LessonSpec(
            title="Төсөл: Бүртгэлийн форм",
            slug="tusul-burtgeliin-form",
            description="Хэрэглэгчийн нэр, имэйл, нууц үг ба давталттай, баталгаажуулалт, алдаа, амжилтын төлөвтэй бүрэн форм бүтээнэ.",
            duration=2100,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Модул 4-т сурсан бүхнээ нэг бүрэн форм болгон нэгтгэх
- Хоёр талбараас хамаарсан дүрэм (нууц үг давтах) бичих
- Дахин ашиглагдах `Field` component-оор давталтыг арилгах
- Хүртээмжтэй алдаа, амжилтын төлөв бүтээх

### Яагаад чухал вэ

Бүртгэлийн форм бол хэрэглэгч таны апптай хийх анхны харилцаа. Ойлгомжгүй
алдаа, хэт эрт гарах улаан мессеж, Enter дарахад ажилладаггүй товч —
хэрэглэгч бүртгүүлэлгүй гарч явах хамгийн түгээмэл шалтгаанууд. Энэ
төсөлд controlled input, олон талбар, илгээлт, баталгаажуулалт, хүртээмж
гэсэн бүх хичээлээ нэг дор хэрэглэнэ.

### Шаардлага

| Label | `name` | Дүрэм | Алдааны мессеж |
|---|---|---|---|
| Хэрэглэгчийн нэр | `username` | Зайг хассаны дараа 3-аас доошгүй тэмдэгт | Хэрэглэгчийн нэр дор хаяж 3 тэмдэгт байна |
| Имэйл | `email` | `нэр@домэйн.mn` хэлбэртэй | Имэйлээ зөв оруулна уу |
| Нууц үг | `password` | 8-аас доошгүй тэмдэгт | Нууц үг дор хаяж 8 тэмдэгт байна |
| Нууц үг давтах | `confirm` | Хоосон биш | Нууц үгээ давтан оруулна уу |
| | | Нууц үгтэй ижил | Нууц үг таарахгүй байна |

- Label-ийн текст хүснэгтэд байгаагаар яг ижил, `htmlFor`-оор холбогдсон.
  Нууц үгийн хоёр талбар `type="password"`.
- Алдаа тухайн талбараас гарах (blur) эсвэл илгээх үед л харагдана, зассан
  даруйд алга болно. Хүрээгүй талбарын алдааг хэт эрт бүү харуул.
- Алдаатай талбар `aria-invalid="true"`, `aria-describedby`-гаар алдаагаа
  заана, алдааны мессеж `role="alert"`.
- «Бүртгүүлэх» товч эсвэл Enter илгээнэ, хуудас дахин ачаалагдахгүй.
- Бүх талбар зөв бол форм алга болж «Бүртгэл амжилттай! Тавтай морил,
  {хэрэглэгчийн нэр}.» гэсэн мэдэгдэл гарна.

### Дизайн

```
┌ Шинэ бүртгэл ───────────────────┐
│ Хэрэглэгчийн нэр                │
│ [ sa                          ] │
│ Хэрэглэгчийн нэр дор хаяж 3 ... │  ← улаан, role="alert"
│ Имэйл                           │
│ [                             ] │
│ Нууц үг                         │
│ [ ••••••••                    ] │
│ Нууц үг давтах                  │
│ [ •••••••                     ] │
│ Нууц үг таарахгүй байна         │
│ [ Бүртгүүлэх ]                  │
└─────────────────────────────────┘
```

Эхлэл кодод гурван файл бий:

| Файл | Үүрэг |
|---|---|
| `validate.js` | `validate(values)` → `errors` объект. Цэвэр функц. |
| `Field.jsx` | Нэг талбар: label, input, алдаа ба бүх aria холбоос. Дөрвөн удаа дахин ашиглагдана. |
| `App.jsx` | State (`values`, `touched`, `submitted`, амжилт), handler-ууд, форм. |

`Field`-ийн props: `label`, `name`, `type`, `value`, `error`, `onChange`,
`onBlur`. `error` нь харуулах ёстой алдаа (эсвэл `undefined`) — хэзээ
харуулахыг `App` шийднэ, `Field` зөвхөн зурна.

### Хоёр талбараас хамаарсан дүрэм

`validate` бүх утгыг нэг дор хүлээн авдаг тул талбаруудыг хооронд нь
харьцуулахад хялбар:

```jsx
if (values.confirm === "") {
  errors.confirm = "Нууц үгээ давтан оруулна уу";
} else if (values.confirm !== values.password) {
  errors.confirm = "Нууц үг таарахгүй байна";
}
```

`errors`-ийг render бүрт тооцдог тул хэрэглэгч эхний нууц үгээ засахад
давталтын алдаа ч автоматаар шинэчлэгдэнэ.

### Алхмууд

1. `validate.js`-ийг хүснэгтийн дагуу гүйцээ. Имэйлд
   `/^[^@ ]+@[^@ ]+[.][^@ ]+$/` хангалттай.
2. `Field.jsx`-т label-ийг `htmlFor`-оор холбож, алдаатай үед
   `aria-invalid`, `aria-describedby` болон `role="alert"`-тэй мессеж нэм.
   Алдааны `id`-г `name`-ээс үүсгэж болно: `` `${name}-error` ``.
3. `App.jsx`-т `touched`, `submitted`, амжилтын state нэмж, `handleBlur`,
   `handleSubmit` бич. Үлдсэн гурван талбарыг `Field`-ээр нэм.
4. Амжилтын төлөвт формын оронд мэдэгдлийг буцаа.

### Нэмэлт сорилт

- Нууц үгийн хүчийг харуулах: сул / дунд / хүчтэй (урт, тоо, том үсэг).
- «Нууц үгийг харуулах» checkbox — `type`-ийг `"password"` ба `"text"`
  хооронд солих.
- `Field` дотор `id`-г `useId()`-аар үүсгэх.

```quiz
Нууц үг «nuuts1234», давталт «nuuts123» үед `validate` `confirm`-д юу буцаах вэ?
- [ ] Юу ч үгүй — хоёулаа 8-аас урт
- [ ] «Нууц үгээ давтан оруулна уу»
- [x] «Нууц үг таарахгүй байна»
> Давталт хоосон биш ч нууц үгтэй таарахгүй байна.
```

### Дүгнэлт

Бодит форм нь олон жижиг санаанаас бүрдэнэ: нэг state объект, цэвэр
`validate`, `touched` + `submitted`-ээр алдаа харуулах цаг, хүртээмжтэй
`Field` component, `preventDefault`-тай илгээлт. Энэ бүтцийг дараа нь
React Hook Form зэрэг сан руу шилжүүлэхэд ч ижил санаа хэвээр үлдэнэ.
""",
            initial_code=vite(
                """\
import { useState } from "react";
import Field from "./Field";
import { validate } from "./validate";

const INITIAL = { username: "", email: "", password: "", confirm: "" };

export default function App() {
  const [values, setValues] = useState(INITIAL);
  // TODO: touched, submitted, амжилтын state

  function handleChange(e) {
    setValues({ ...values, [e.target.name]: e.target.value });
  }

  // TODO: handleBlur, handleSubmit (preventDefault!)
  // TODO: амжилттай бол формын оронд мэдэгдэл буцаа

  return (
    <form noValidate>
      <h1>Шинэ бүртгэл</h1>
      <Field
        label="Хэрэглэгчийн нэр"
        name="username"
        value={values.username}
        onChange={handleChange}
      />
      {/* TODO: Имэйл, Нууц үг, Нууц үг давтах талбарууд */}
      <button type="submit">Бүртгүүлэх</button>
    </form>
  );
}
""",
                extra={
                    "Field.jsx": """\
export default function Field({ label, name, type = "text", value, error, onChange, onBlur }) {
  // TODO: label-ийг input-тэй htmlFor/id-аар холбо.
  // TODO: error байвал aria-invalid, aria-describedby ба role="alert"-тэй мессеж.
  return (
    <div className="field">
      <label>{label}</label>
      <input name={name} type={type} value={value} onChange={onChange} onBlur={onBlur} />
    </div>
  );
}
""",
                    "validate.js": """\
export function validate(values) {
  const errors = {};
  // TODO: «Заавар»-ын хүснэгтийн дүрэм, мессежүүд
  return errors;
}
""",
                },
                css=FORM_CSS,
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐⭐ · 35 минут

«Заавар» дахь шаардлага, дизайны дагуу бүртгэлийн формыг бүтээ.
`validate.js`, `Field.jsx`, `App.jsx` гурвыг гүйцээнэ. Тестүүд дууссан
формын хүлээн авах шалгуурыг жагсааж байгаа.
""",
                tests=(
                    test(
                        "Дөрвөн талбар label-аараа олдож, нууц үгнүүд нуугдмал",
                        """
render(<App />);
expect(screen.getByLabelText("Хэрэглэгчийн нэр")).toBeInTheDocument();
expect(screen.getByLabelText("Имэйл")).toBeInTheDocument();
expect(screen.getByLabelText("Нууц үг")).toHaveAttribute("type", "password");
expect(screen.getByLabelText("Нууц үг давтах")).toHaveAttribute("type", "password");
""",
                    ),
                    test(
                        "Хоосон илгээхэд талбар бүрийн алдаа харагдана",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: "Бүртгүүлэх" }));
const text = screen.text();
expect(text).toContain("Хэрэглэгчийн нэр дор хаяж 3 тэмдэгт байна");
expect(text).toContain("Имэйлээ зөв оруулна уу");
expect(text).toContain("Нууц үг дор хаяж 8 тэмдэгт байна");
expect(text).toContain("Нууц үгээ давтан оруулна уу");
""",
                    ),
                    test(
                        "Нууц үг таарахгүй бол талбараас гарахад алдаа гарна, хүрээгүй талбар загнахгүй",
                        """
render(<App />);
await user.type(screen.getByLabelText("Нууц үг"), "nuuts1234");
const confirm = screen.getByLabelText("Нууц үг давтах");
await user.type(confirm, "nuuts123");
await act(async () => {
  confirm.dispatchEvent(new FocusEvent("focusout", { bubbles: true }));
});
expect(screen.text()).toContain("Нууц үг таарахгүй байна");
expect(screen.text()).not.toContain("Хэрэглэгчийн нэр дор хаяж");
""",
                    ),
                    test(
                        'Алдаатай талбар бүр aria-invalid="true", aria-describedby-тай, алдаа нь role="alert"',
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: "Бүртгүүлэх" }));
for (const label of ["Хэрэглэгчийн нэр", "Имэйл", "Нууц үг", "Нууц үг давтах"]) {
  const input = screen.getByLabelText(label);
  expect(input).toHaveAttribute("aria-invalid", "true");
  const ids = (input.getAttribute("aria-describedby") ?? "").split(" ").filter(Boolean);
  const described = ids.map((id) => document.getElementById(id)?.textContent ?? "").join(" ");
  expect(described.trim().length).toBeGreaterThan(0);
}
expect(screen.getAllByRole("alert").length).toBeGreaterThanOrEqual(4);
""",
                    ),
                    test(
                        "Зөв бөглөж илгээхэд форм алга болж амжилтын мэдэгдэл гарна",
                        """
render(<App />);
await user.type(screen.getByLabelText("Хэрэглэгчийн нэр"), "saraa");
await user.type(screen.getByLabelText("Имэйл"), "saraa@example.mn");
await user.type(screen.getByLabelText("Нууц үг"), "nuuts1234");
await user.type(screen.getByLabelText("Нууц үг давтах"), "nuuts1234{enter}");
expect(screen.text()).toContain("Бүртгэл амжилттай");
expect(screen.text()).toContain("saraa");
expect(screen.queryByLabelText("Имэйл")).toBeNull();
expect(logs.some((entry) => entry.text.includes("preventDefault"))).toBe(false);
""",
                    ),
                ),
                tips="""\
- `Field`: `<label htmlFor={name}>` ба `<input id={name} …>`. Алдааны
  элементийн `id` нь жишээ нь `` `${name}-error` ``, input-ийн
  `aria-describedby` мөн түүнийг заана.
- `App`: `const errors = validate(values);` — render бүрт тооцоол. Харуулах
  алдаа: `touched[name] || submitted ? errors[name] : undefined`.
- `handleSubmit`: `e.preventDefault()`, `setSubmitted(true)`, алдаагүй бол
  амжилтын state-ийг тохируул. Формд `onSubmit={handleSubmit}` өгөхөө бүү
  мартаарай — тэгвэл Enter ч ажиллана.
- Амжилтын дараа `if (…) return <p>…</p>;` — форм бүхэлдээ алга болно.
- «Нууц үг» label-ийг хайхад «Нууц үг давтах» андуурагдахгүйн тулд label-ийн
  текстийг яг хүснэгтэд байгаагаар бич.
""",
                solution=solution(
                    App_jsx="""\
import { useState } from "react";
import Field from "./Field";
import { validate } from "./validate";

const INITIAL = { username: "", email: "", password: "", confirm: "" };

export default function App() {
  const [values, setValues] = useState(INITIAL);
  const [touched, setTouched] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const [registered, setRegistered] = useState(null);

  const errors = validate(values);

  function handleChange(e) {
    setValues({ ...values, [e.target.name]: e.target.value });
  }

  function handleBlur(e) {
    setTouched({ ...touched, [e.target.name]: true });
  }

  function handleSubmit(e) {
    e.preventDefault();
    setSubmitted(true);
    if (Object.keys(errors).length === 0) {
      setRegistered(values.username.trim());
    }
  }

  function fieldProps(name) {
    return {
      name,
      value: values[name],
      error: touched[name] || submitted ? errors[name] : undefined,
      onChange: handleChange,
      onBlur: handleBlur,
    };
  }

  if (registered) {
    return (
      <p className="card" role="status">
        🎉 Бүртгэл амжилттай! Тавтай морил, {registered}.
      </p>
    );
  }

  return (
    <form onSubmit={handleSubmit} noValidate>
      <h1>Шинэ бүртгэл</h1>
      <Field label="Хэрэглэгчийн нэр" {...fieldProps("username")} />
      <Field label="Имэйл" type="email" {...fieldProps("email")} />
      <Field label="Нууц үг" type="password" {...fieldProps("password")} />
      <Field label="Нууц үг давтах" type="password" {...fieldProps("confirm")} />
      <button type="submit">Бүртгүүлэх</button>
    </form>
  );
}
""",
                    Field_jsx="""\
export default function Field({ label, name, type = "text", value, error, onChange, onBlur }) {
  const errorId = `${name}-error`;
  return (
    <div className="field">
      <label htmlFor={name}>{label}</label>
      <input
        id={name}
        name={name}
        type={type}
        value={value}
        required
        onChange={onChange}
        onBlur={onBlur}
        aria-invalid={error ? true : undefined}
        aria-describedby={error ? errorId : undefined}
      />
      {error && (
        <p id={errorId} className="error" role="alert">
          {error}
        </p>
      )}
    </div>
  );
}
""",
                    validate_js="""\
export function validate(values) {
  const errors = {};
  if (values.username.trim().length < 3) {
    errors.username = "Хэрэглэгчийн нэр дор хаяж 3 тэмдэгт байна";
  }
  if (!/^[^@ ]+@[^@ ]+[.][^@ ]+$/.test(values.email)) {
    errors.email = "Имэйлээ зөв оруулна уу";
  }
  if (values.password.length < 8) {
    errors.password = "Нууц үг дор хаяж 8 тэмдэгт байна";
  }
  if (values.confirm === "") {
    errors.confirm = "Нууц үгээ давтан оруулна уу";
  } else if (values.confirm !== values.password) {
    errors.confirm = "Нууц үг таарахгүй байна";
  }
  return errors;
}
""",
                ),
            ),
        ),
    ],
)
