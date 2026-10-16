"""Модул 1 — React-ийн үндэс.

React гэж юу вэ, төслийн бүтэц, элемент, createRoot, JSX, component ба
тэдгээрийг нийлүүлэх. Төгсгөлд нь «Хувийн профайл» төсөл.
"""

from app.content.react.common import HTML, files, solution, test, vite
from app.content.types import ExerciseSpec, LessonSpec, ModuleSpec
from app.models.enums import LessonLanguage

JSX = LessonLanguage.JSX

PROFILE_CSS = """\
body {
  margin: 0;
  background: #f4f6f8;
  color: #1f2328;
}

.page {
  max-width: 560px;
  margin: 0 auto;
  padding: 24px 16px;
}

header h1 {
  margin: 0;
  font-size: 28px;
}

header p {
  margin: 4px 0 0;
  color: #57606a;
}

.card {
  margin-top: 16px;
  padding: 16px;
  border-radius: 12px;
  background: #fff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.avatar {
  display: grid;
  place-items: center;
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: #dcfce7;
  font-size: 32px;
}

.skills {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 0;
  list-style: none;
}

.skills li {
  padding: 4px 12px;
  border-radius: 999px;
  background: #e0f2fe;
}

footer {
  margin-top: 24px;
  color: #57606a;
  font-size: 14px;
  text-align: center;
}
"""

FUNDAMENTALS = ModuleSpec(
    title="Модул 1 — React-ийн үндэс",
    description="React элемент, JSX, component, тэдгээрийг нийлүүлэн UI бүтээх.",
    lessons=[
        LessonSpec(
            title="React гэж юу вэ",
            slug="react-gej-yu-ve",
            description="Сан ба framework, declarative UI, component, SPA.",
            duration=600,
            language=JSX,
            content="""\
### Энэ хичээлээр

- React гэж юу болохыг, яагаад ийм түгээмэл болсныг ойлгох
- Сан (library) ба framework-ийн ялгааг мэдэх
- Component, declarative UI, SPA гэсэн гол ойлголтуудтай танилцах

### Яагаад чухал вэ

Өмнөх хичээлд DOM-оор тоологч бичихэд өгөгдөл өөрчлөгдөх бүрт холбоотой
бүх газрыг гараар шинэчлэх хэрэгтэй байсан. Facebook-ийн инженерүүд
2013 онд яг энэ асуудлыг шийдэх гэж **React**-ийг бүтээсэн. Өнөөдөр
Facebook, Instagram, Netflix, Airbnb, Discord зэрэг олон мянган компани
ашигладаг бөгөөд вэб хөгжүүлэгчийн ажлын зарын ихэнх нь React шаарддаг.

### Сан уу, framework уу?

**Сан (library)** — таны код түүнийг дууддаг. Та аппын бүтцээ өөрөө
шийднэ, сан нэг ажлыг сайн хийнэ. React зөвхөн **UI** бүтээдэг сан.

**Framework** — framework таны кодыг дууддаг: хавтас, routing, өгөгдөл
татах бүгдийн дүрэмтэй. Жишээ нь Next.js бол React дээр суурилсан
framework.

| | React (сан) | Next.js (framework) |
|---|---|---|
| Юу хийдэг | UI-г component-оор бүтээнэ | UI + routing + сервер + build |
| Бүтэц | Та өөрөө сонгоно | Framework-ийн дүрэмтэй |
| Хэзээ | Бүх React апп-ын суурь | Том, SEO чухал сайт |

Энэ сургалт React-ийг өөрийг нь заана. Сурсан бүхэн тань Next.js зэрэг
framework-т шууд хэрэг болно.

### Component — UI-ын тоосго

React апп жижиг, дахин ашиглагдах хэсгүүдээс — **component**-оос —
бүрдэнэ. Товч, карт, толгой хэсэг бүр нь component. Тэдгээрийг LEGO
шиг нийлүүлж хуудас болгоно:

```jsx
function App() {
  return (
    <div>
      <Header />
      <ProductList />
      <Footer />
    </div>
  );
}
```

### Declarative: юу харагдахыг л хэлнэ

React-д «товч дарахад span-ийн текстийг өөрчил» гэж бичихгүй.
Оронд нь «тоо ийм байхад дэлгэц ийм харагдана» гэж бичнэ. Өгөгдөл
өөрчлөгдөхөд React DOM-ыг **өөрөө** шинэчилнэ. Үүнийг `UI = f(state)`
гэж томьёолдог.

React шинэчлэхийн өмнө шинэ UI-г санах ойд байгуулж, хуучинтай нь
харьцуулаад **зөвхөн өөрчлөгдсөн** DOM-ыг шинэчилдэг (үүнийг «virtual
DOM» гэж нэрлэдэг, Модул 10-т дэлгэрэнгүй).

### SPA — нэг хуудастай апп

Уламжлалт сайтад холбоос дарах бүрт сервер шинэ HTML хуудас явуулна.
React-ийн ихэнх апп **SPA (single page application)**: хөтөч нэг л HTML
ачаална, дараа нь JavaScript хуудсыг солино. Шилжилт хурдан, апп шиг
мэдрэмжтэй. Модул 8-д React-д хуудсууд хэрхэн солигддогийг үзнэ.

### Одоо «Хөтөч»-өөс үз

Баруун талын «Хөтөч» tab-д 0.5-р хичээлийн тоологчийг React-ээр бичсэн
хувилбар ажиллаж байна. `App.jsx`-ийг уншаад, товчийг дарж үзээрэй.
Ганц ч `document.getElementById` алга, гэхдээ хоёр газар зэрэг
шинэчлэгдэнэ. Кодыг одоо бүрэн ойлгох шаардлагагүй.

```quiz
React бол юу вэ?
- [ ] Бүрэн framework — сервер, өгөгдлийн сан, routing бүгдийг агуулна
- [x] UI бүтээх JavaScript сан
- [ ] HTML-ийн шинэ хувилбар
- [ ] Зөвхөн Facebook дотор ашиглагддаг хэрэгсэл
> React зөвхөн UI бүтээх ажлыг хийнэ. Routing, өгөгдөл татах зэрэгт өөр сан эсвэл framework ашиглана.
```

```quiz
«Declarative» UI гэдэг нь…
- [x] Өгөгдөл тухайн мөчид ямар харагдахыг бичиж, DOM-ыг шинэчлэх ажлыг React-д даатгах
- [ ] DOM-ын элемент бүрийг гараар олж шинэчлэх
- [ ] CSS-гүй бичих
> Imperative аргад «хэрхэн», declarative аргад «юу» гэдгийг бичнэ.
```

### Дүгнэлт

React бол component-оор UI бүтээх, declarative сан. Та өгөгдлөөс хамаарч
UI ямар харагдахыг бичнэ, React DOM-ыг өөрөө шинэчилнэ. Дараагийн
хичээлд React төсөл ямар файлуудаас бүрддэгийг үзнэ.
""",
            initial_code=vite(
                """\
// Урьдчилан харах жишээ: useState-ийг Модул 3-т үзнэ — одоо ойлгох
// шаардлагагүй. Товчийг дараад хоёр мөр зэрэг шинэчлэгдэхийг л ажигла.
import { useState } from "react";

export default function App() {
  const [count, setCount] = useState(0);

  return (
    <main>
      <h1>React тоологч</h1>
      <p>Дарсан: {count}</p>
      <p>{count % 2 === 0 ? "Тэгш" : "Сондгой"}</p>
      <button onClick={() => setCount(count + 1)}>+1</button>
      <button onClick={() => setCount(0)}>Тэглэх</button>
    </main>
  );
}
"""
            ),
        ),
        LessonSpec(
            title="React төслийн бүтэц: Vite",
            slug="react-tosliin-butets",
            description="index.html, main.jsx, App.jsx — React апп хэрхэн эхэлдэг.",
            duration=720,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Бодит React төслийг Vite-ээр хэрхэн үүсгэдгийг мэдэх
- `index.html`, `main.jsx`, `App.jsx` файлуудын үүргийг ойлгох
- React апп хөтөч дээр хэрхэн «асдаг»-ийг дагах

### Яагаад чухал вэ

Энэ засварлагч дахь файлууд нь бодит React төслийн файлуудтай ижил.
Бүтцийг ойлговол өөрийн компьютер дээр төсөл эхлүүлэхэд төөрөхгүй.

### Төсөл үүсгэх

React төслийг ихэвчлэн **Vite** хэрэгслээр үүсгэдэг. Node.js суулгасан
компьютерт:

```jsx
// Терминалд:
// npm create vite@latest my-app -- --template react
// cd my-app
// npm install
// npm run dev    →  http://localhost:5173
```

`npm run dev` нь хөгжүүлэлтийн сервер асаана: кодоо хадгалах бүрт хөтөч
шууд шинэчлэгдэнэ. Бэлэн болсон аппаа `npm run build`-ээр жижигрүүлж
`dist/` хавтаст гаргаад сервер дээр байршуулна.

### Файлууд

```jsx
my-app/
├── index.html        ← хөтчийн ачаалах цорын ганц HTML
├── package.json      ← react, react-dom зэрэг сангууд
└── src/
    ├── main.jsx      ← эхлэх цэг: React-ийг #root-д холбоно
    └── App.jsx       ← үндсэн component
```

**index.html** нь бараг хоосон: ганц `<div id="root"></div>` болон
`main.jsx`-ийг ачаалах `<script>`. Бүх UI-г React энэ div дотор
байгуулна.

**main.jsx** нь React-ийг HTML-тэй холбоно:

```jsx
import { createRoot } from "react-dom/client";
import App from "./App";

createRoot(document.getElementById("root")).render(<App />);
```

- `react-dom/client` — React-ийг хөтчийн DOM-той ажиллуулах хэсэг.
- `createRoot(элемент)` — React-ийн удирдах «үндэс»-ийг үүсгэнэ.
- `.render(<App />)` — `App` component-ийг тэнд харуулна.

**App.jsx** — таны аппын үндсэн component. Ихэнх цагаа энд болон
түүний импортолсон бусад файлд зарцуулна.

### Хэрхэн асдаг вэ

1. Хөтөч `index.html`-ийг ачаална — хоосон `#root`.
2. `main.jsx` ажиллаж `createRoot`-оор `#root`-ийг React-д өгнө.
3. React `App`-ийг дуудаж, буцаасан UI-г `#root` дотор DOM болгоно.

Энэ засварлагчийн 🔒 `main.jsx`, 🔒 `index.html` яг энэ хоёр файл. Энэ
хичээлд `main.jsx`-ийн түгжээг авсан — доорх даалгаврыг хар.

```quiz
`index.html` доторх `<div id="root"></div>`-ийн үүрэг юу вэ?
- [ ] Хуудасны гарчгийг харуулна
- [x] React бүх UI-гаа байгуулах байр
- [ ] CSS-ийг ачаална
> `createRoot(document.getElementById("root"))` нь яг энэ div-ийг React-д өгнө.
```

### Дүгнэлт

Vite төсөлд `index.html` нь хоосон `#root`-той, `main.jsx` нь React-ийг
тэнд холбоно, `App.jsx` нь UI-гаа агуулна. Дараагийн хичээлүүдэд эдгээр
алхам бүрийг дэлгэрэнгүй үзнэ.
""",
            initial_code=files(
                (
                    "main.jsx",
                    """\
import { createRoot } from "react-dom/client";
import App from "./App";

// TODO: #root элементэд createRoot үүсгэж, <App />-ийг render хий.
""",
                ),
                (
                    "App.jsx",
                    """\
export default function App() {
  return (
    <main>
      <h1>Миний анхны React апп</h1>
      <p>main.jsx намайг #root дотор харуулна.</p>
    </main>
  );
}
""",
                    True,
                ),
                ("index.html", HTML, True),
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐ · 5 минут

Энэ удаа `main.jsx` засварлагдана. Одоогоор «Хөтөч» хоосон — `App`-ийг
хэн ч render хийгээгүй. `createRoot`, `render`-ийг ашиглан `App`-ийг
`#root` дотор харуул.
""",
                tests=(
                    test(
                        "main.jsx нь App-ийг #root дотор харуулна",
                        """
const root = await runMain();
expect(root).toHaveTextContent("Миний анхны React апп");
""",
                    ),
                    test(
                        "Гарчиг h1 хэлбэрээр харагдана",
                        """
await runMain();
expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent("Миний анхны React апп");
""",
                    ),
                ),
                tips="""\
Хичээлийн текст дэх `main.jsx`-ийн гурван мөрийг санаарай:
`createRoot(...)`-д `document.getElementById("root")`-ийг өгч, буцаасан
root дээр `.render(<App />)` дууд. `import` мөрүүд аль хэдийн бичигдсэн.
""",
                solution=solution(
                    main_jsx="""\
import { createRoot } from "react-dom/client";
import App from "./App";

createRoot(document.getElementById("root")).render(<App />);
"""
                ),
            ),
        ),
        LessonSpec(
            title="React элемент ба createElement",
            slug="react-element",
            description="JSX-гүйгээр React элемент үүсгэж, түүний бүтцийг харах.",
            duration=720,
            language=JSX,
            content="""\
### Энэ хичээлээр

- React элемент гэж юу болохыг ойлгох
- `createElement(төрөл, props, ...хүүхдүүд)`-ийг ашиглах
- Элементүүдийг үүрлүүлж мод бүтэц үүсгэх

### Яагаад чухал вэ

Дараагийн хичээлээс JSX бичнэ. JSX нь үнэндээ `createElement`-ийн
дуудлага болж хувирдаг. Доор нь юу болж байгааг мэдвэл JSX-ийн дүрэм,
алдааны мессежүүд ойлгомжтой болно.

### React элемент — UI-ын тайлбар

React элемент бол DOM элемент **биш**. Энэ бол «энд ийм зүйл харагдана»
гэсэн энгийн JavaScript объект:

```jsx
import { createElement } from "react";

const title = createElement("h1", { className: "title" }, "Сайн уу!");
console.log(title);
// { type: "h1", props: { className: "title", children: "Сайн уу!" }, … }
```

`createElement`-ийн аргументууд:

1. **type** — HTML шошгын нэр (`"h1"`, `"div"`) эсвэл component.
2. **props** — attribute-уудын объект (`null` байж болно).
3. **children** — дотор нь байх текст эсвэл бусад элементүүд.

Анхаар: HTML-ийн `class`-ийн оронд `className` гэж бичнэ, учир нь
`class` нь JavaScript-ийн нөөц үг.

### Үүрлэсэн элемент

```jsx
const card = createElement(
  "div",
  { className: "card" },
  createElement("h2", null, "React"),
  createElement("p", null, "UI бүтээх сан"),
);
```

Энэ нь дараах HTML-тэй ижил бүтэц:

```jsx
<div class="card">
  <h2>React</h2>
  <p>UI бүтээх сан</p>
</div>
```

Элемент нь зүгээр л тайлбар. `render` дуудахад React түүнийг уншиж жинхэнэ
DOM үүсгэнэ.

### Элемент өөрчлөгддөггүй

React элементийг үүсгэсний дараа өөрчилдөггүй — «зураг» шиг. UI
шинэчлэгдэхэд React **шинэ** элемент үүсгэж, хуучинтай нь харьцуулдаг.

```quiz
`createElement("p", null, "Сайн уу")` юу буцаах вэ?
- [ ] Хуудсан дээр шууд гарсан `<p>` DOM элемент
- [x] `type`, `props`-той энгийн JavaScript объект
- [ ] HTML текст `"<p>Сайн уу</p>"`
> React элемент бол тайлбар. DOM-ыг `render` үед React өөрөө үүсгэнэ.
```

### Дүгнэлт

`createElement(төрөл, props, ...хүүхдүүд)` нь UI-г тайлбарласан объект
буцаана. JSX нь яг ийм дуудлагыг товч бичих арга — дараагийн хичээлүүдэд
үүнийг ашиглана.
""",
            initial_code=files(
                (
                    "elements.js",
                    """\
import { createElement } from "react";

export function createCard(title, text) {
  // TODO: <div className="card"><h2>{title}</h2><p>{text}</p></div>
  // бүтэцтэй элементийг createElement ашиглан буцаа.
  return createElement("div", { className: "card" });
}
""",
                ),
                (
                    "App.jsx",
                    """\
import { createCard } from "./elements";

export default function App() {
  const card = createCard("React", "UI бүтээх сан");
  console.log("Элементийн төрөл:", card.type);
  console.log("Props:", card.props);
  return card;
}
""",
                    True,
                ),
                (
                    "main.jsx",
                    """\
import { createRoot } from "react-dom/client";
import App from "./App";

createRoot(document.getElementById("root")).render(<App />);
""",
                    True,
                ),
                ("index.html", HTML, True),
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 8 минут

`elements.js` доторх `createCard` функцийг гүйцээ. Энэ нь `card`
класстай `div` дотор `h2` гарчиг (`title`), `p` текст (`text`) бүхий
элемент буцаах ёстой. JSX бүү ашигла — энэ хичээлийн зорилго
`createElement`.
""",
                tests=(
                    test(
                        "div элемент, className нь card",
                        """
const card = mod("./elements").createCard("React", "UI сан");
expect(card.type).toBe("div");
expect(card.props.className).toBe("card");
""",
                    ),
                    test(
                        "Дотор нь title-тай h2 харагдана",
                        """
render(mod("./elements").createCard("Hooks", "Функц"));
expect(screen.getByRole("heading", { level: 2 })).toHaveTextContent("Hooks");
""",
                    ),
                    test(
                        "Дотор нь text-тэй p харагдана",
                        """
const { container } = render(mod("./elements").createCard("A", "Энгийн текст"));
const paragraph = container.querySelector(".card > p");
expect(paragraph).toHaveTextContent("Энгийн текст");
""",
                    ),
                ),
                tips="""\
`createElement`-ийн гурав дахь аргументаас хойш хэдэн ч хүүхэд өгч болно:

`createElement("div", { className: "card" }, хүүхэд1, хүүхэд2)`

Хүүхэд бүр өөрөө `createElement("h2", null, title)` гэх мэт элемент.
""",
                solution=solution(
                    elements_js="""\
import { createElement } from "react";

export function createCard(title, text) {
  return createElement(
    "div",
    { className: "card" },
    createElement("h2", null, title),
    createElement("p", null, text),
  );
}
"""
                ),
            ),
        ),
        LessonSpec(
            title="createRoot ба render",
            slug="createroot-render",
            description="React-ийг DOM-д холбож, дахин render хийхэд юу болдгийг харах.",
            duration=720,
            language=JSX,
            content="""\
### Энэ хичээлээр

- `createRoot`, `root.render`-ийг өөрөө бичих
- Дахин `render` хийхэд React зөвхөн өөрчлөгдсөн хэсгийг шинэчилдгийг харах

### Яагаад чухал вэ

Энэ бол React аппын эхлэл. Бодит төсөлд үүнийг нэг л удаа бичдэг ч
React яаж ажилладгийг ойлгох хамгийн сайн цонх.

### Үндэс үүсгэх

```jsx
import { createRoot } from "react-dom/client";

const root = createRoot(document.getElementById("root"));
root.render(createElement("h1", null, "Сайн уу!"));
```

`createRoot`-ийг нэг DOM элемент дээр **нэг** удаа дуудна. Цаашид
тэр элемент доторх бүх зүйлийг React удирдана — тэнд гараар
`innerHTML` өөрчлөхгүй.

### Дахин render

`root.render`-ийг дахин дуудвал React шинэ элементийг хуучинтай нь
харьцуулж, **зөвхөн өөрчлөгдсөн** DOM-ыг шинэчилнэ:

```jsx
function tick() {
  const time = new Date().toLocaleTimeString("mn-MN");
  root.render(
    createElement("div", null,
      createElement("h1", null, "Цаг"),
      createElement("p", null, time),
    ),
  );
}

setInterval(tick, 1000);
```

Секунд тутамд бүх модыг шинээр тайлбарлаж байгаа ч React зөвхөн `p`-ийн
текстийг шинэчилнэ. Даалгавраа дуусгасны дараа энэ жишээг `main.jsx`-д
хуулж ажиллуулаад үзээрэй — `h1` хэвээр, зөвхөн цаг солигдоно.

Бодит апп дээр `root.render`-ийг гараар давтан дууддаггүй — Модул 3-т
**state** өөрчлөгдөхөд React өөрөө дахин render хийнэ. Гэхдээ доор яг
ийм харьцуулалт явагддаг.

```quiz
`root.render(...)`-ийг хоёр дахь удаа дуудахад юу болох вэ?
- [ ] Хуудас бүхэлдээ дахин ачаалагдана
- [ ] Алдаа гарна — render зөвхөн нэг удаа
- [x] React шинэ элементийг хуучинтай харьцуулж, өөрчлөгдсөн DOM-ыг л шинэчилнэ
> Энэ харьцуулалтыг reconciliation гэдэг — Модул 10-т дэлгэрэнгүй.
```

### Дүгнэлт

`createRoot(элемент)` нэг удаа, `root.render(ui)` UI-г харуулна. Дахин
render хийхэд React зөвхөн ялгааг DOM-д хэрэглэнэ.
""",
            initial_code=files(
                (
                    "main.jsx",
                    """\
import { createElement } from "react";
import { createRoot } from "react-dom/client";

// TODO 1: #root элемент дээр root үүсгэ.
// TODO 2: <h1>Миний анхны React апп</h1> болон
//         <p>createElement-ээр бүтээв</p>-ийг агуулсан div-ийг render хий.
//         (JSX-ийг дараагийн хичээлд үзнэ — одоохондоо createElement.)
""",
                ),
                ("index.html", HTML, True),
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐ · 6 минут

`main.jsx`-д `createRoot`-оор үндэс үүсгэж, `h1` гарчиг ба `p` текст
бүхий `div`-ийг `createElement`-ээр render хий. Текстүүд даалгаврын
TODO-д бичигдсэн.
""",
                tests=(
                    test(
                        "#root дотор «Миний анхны React апп» гарчиг харагдана",
                        """
await runMain();
expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent("Миний анхны React апп");
""",
                    ),
                    test(
                        "«createElement-ээр бүтээв» текст харагдана",
                        """
const root = await runMain();
expect(root.querySelector("p")).toHaveTextContent("createElement-ээр бүтээв");
""",
                    ),
                ),
                tips="""\
1. `const root = createRoot(document.getElementById("root"));`
2. `root.render(createElement("div", null, …))` — `div`-ийн хүүхдүүдэд
   `h1`, `p` элементүүдээ `createElement`-ээр өгнө.
""",
                solution=solution(
                    main_jsx="""\
import { createElement } from "react";
import { createRoot } from "react-dom/client";

const root = createRoot(document.getElementById("root"));

root.render(
  createElement(
    "div",
    null,
    createElement("h1", null, "Миний анхны React апп"),
    createElement("p", null, "createElement-ээр бүтээв"),
  ),
);
"""
                ),
            ),
        ),
        LessonSpec(
            title="JSX: HTML-ээс JSX рүү",
            slug="jsx",
            description="JSX-ийн дүрэм: нэг эх элемент, хаах шошго, className, htmlFor.",
            duration=900,
            language=JSX,
            content="""\
### Энэ хичээлээр

- JSX гэж юу болохыг, `createElement`-тэй хэрхэн холбогддогийг ойлгох
- JSX-ийн гол дүрмүүдийг сурах
- HTML-ийг JSX болгож хөрвүүлэх

### Яагаад чухал вэ

`createElement`-ээр том UI бичих нь хэцүү, уншихад төвөгтэй. **JSX** нь
HTML шиг харагддаг ч JavaScript доторх бичлэг. React-ийн бараг бүх код
JSX-ээр бичигддэг.

### JSX → createElement

```jsx
const title = <h1 className="title">Сайн уу!</h1>;

// Хөрвүүлэгч (Vite) үүнийг дараах болгоно:
const same = createElement("h1", { className: "title" }, "Сайн уу!");
```

Тиймээс JSX нь HTML **биш** — JavaScript. Үүнээс хэдэн дүрэм гарна.

### Дүрэм 1: ганц эх элемент

Функц нэг л утга буцаадаг тул JSX ч нэг л эх элементтэй байна:

```jsx
// ❌ Алдаа: Adjacent JSX elements must be wrapped in an enclosing tag
return (
  <h1>Гарчиг</h1>
  <p>Текст</p>
);

// ✅
return (
  <div>
    <h1>Гарчиг</h1>
    <p>Текст</p>
  </div>
);
```

### Дүрэм 2: бүх шошгыг хаана

HTML-д `<br>`, `<img>`, `<input>`-ийг хаахгүй байж болдог. JSX-д бүх
шошго хаагдах ёстой: `<br />`, `<img />`, `<input />`.

### Дүрэм 3: зарим attribute өөр нэртэй

| HTML | JSX | Шалтгаан |
|---|---|---|
| `class` | `className` | `class` нь JavaScript-ийн нөөц үг |
| `for` | `htmlFor` | `for` нь давталтын нөөц үг |
| `onclick` | `onClick` | camelCase |
| `tabindex` | `tabIndex` | camelCase |

`aria-label`, `data-id` зэрэг зураастай attribute хэвээр үлдэнэ.

### Дүрэм 4: тайлбар ба олон мөр

```jsx
return (
  <div>
    {/* JSX доторх тайлбар ингэж бичигдэнэ */}
    <p>Олон мөрт JSX-ийг хаалтанд () хийнэ.</p>
  </div>
);
```

### Алдааны мессежийг унш

Энэ засварлагч синтакс алдааг «Хөтөч» дээр мөрийн дугаартай харуулна:
«&lt;div&gt; шошгыг зөв хаагаагүй», «JSX нэг л эх элемент буцаана…».
Эх англи мессеж нь хаалтанд байгаа — бодит төсөлд ч яг ийм мессеж харна.

```quiz
Аль нь зөв JSX вэ?
- [ ] `<label for="email">Имэйл</label>`
- [ ] `<img src="logo.png">`
- [x] `<input className="field" />`
- [ ] `<div class="card"></div>`
> JSX-д `htmlFor`, `className` гэж бичиж, бүх шошгыг хаана.
```

### Дүгнэлт

JSX нь `createElement`-ийг товч бичих арга. Нэг эх элемент, бүх шошгыг
хаах, `className`, `htmlFor`, camelCase attribute — эдгээрийг сана.
""",
            initial_code=vite(
                """\
/*
  Доорх HTML-ийг JSX болгож App дотор буцаа:

  <section class="card">
    <h2>React-ийн мэдээллийн хуудас</h2>
    <p>Шинэ хичээлийн мэдээ авахыг хүсвэл имэйлээ үлдээнэ үү.<br>Спам илгээхгүй.</p>
    <label for="email">Имэйл</label>
    <input id="email" type="email" placeholder="bat@example.mn">
    <hr>
    <button type="button" tabindex="0">Бүртгүүлэх</button>
  </section>
*/

export default function App() {
  return (
    <section>
      {/* TODO: дээрх HTML-ийг JSX болгож энд бич */}
    </section>
  );
}
""",
                css="""\
.card {
  max-width: 420px;
  padding: 20px;
  border: 1px solid #d0d7de;
  border-radius: 12px;
}

.card input {
  display: block;
  width: 100%;
  margin: 6px 0 12px;
  padding: 8px;
  box-sizing: border-box;
}
""",
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 10 минут

`App.jsx`-ийн тайлбар дахь HTML-ийг JSX болгож `App` дотор буцаа. JSX-ийн
дүрмүүдийг бүгдийг нь хэрэглэх хэрэгтэй: `className`, `htmlFor`, хаасан
шошго, camelCase attribute. Синтакс алдаа гарвал «Хөтөч» дээрх мессежийг
унш.
""",
                tests=(
                    test(
                        "section нь card класстай",
                        """
const { container } = render(<App />);
expect(container.querySelector("section.card")).toBeInTheDocument();
""",
                    ),
                    test(
                        "Гарчиг, текст хоёулаа харагдана",
                        """
render(<App />);
expect(screen.getByRole("heading", { level: 2 })).toHaveTextContent("React-ийн мэдээллийн хуудас");
expect(screen.text()).toContain("Спам илгээхгүй.");
""",
                    ),
                    test(
                        "«Имэйл» label нь имэйлийн талбартай холбогдсон",
                        """
render(<App />);
const input = screen.getByLabelText("Имэйл");
expect(input).toHaveAttribute("type", "email");
expect(input).toHaveAttribute("placeholder", "bat@example.mn");
""",
                    ),
                    test(
                        "«Бүртгүүлэх» товч ба хэвтээ зураас байна",
                        """
const { container } = render(<App />);
expect(screen.getByRole("button", { name: "Бүртгүүлэх" })).toBeInTheDocument();
expect(container.querySelector("hr")).toBeInTheDocument();
""",
                    ),
                ),
                tips="""\
- `class` → `className`, `for` → `htmlFor`, `tabindex` → `tabIndex`.
- `<br>`, `<input …>`, `<hr>`-ийг `<br />`, `<input … />`, `<hr />` гэж хаа.
- HTML-ийн `<section class="card">`-ийг гадна талын `<section>`-ийн оронд
  ашигла — хоёр section үүрлэх шаардлагагүй.
""",
                solution=solution(
                    App_jsx="""\
export default function App() {
  return (
    <section className="card">
      <h2>React-ийн мэдээллийн хуудас</h2>
      <p>
        Шинэ хичээлийн мэдээ авахыг хүсвэл имэйлээ үлдээнэ үү.
        <br />
        Спам илгээхгүй.
      </p>
      <label htmlFor="email">Имэйл</label>
      <input id="email" type="email" placeholder="bat@example.mn" />
      <hr />
      <button type="button" tabIndex={0}>
        Бүртгүүлэх
      </button>
    </section>
  );
}
"""
                ),
            ),
        ),
        LessonSpec(
            title="JSX дахь JavaScript: {} илэрхийлэл",
            slug="jsx-ilerhiilel",
            description="Хувьсагч, тооцоо, функцийн дуудлагыг JSX дотор харуулах.",
            duration=840,
            language=JSX,
            content="""\
### Энэ хичээлээр

- `{}` дотор JavaScript илэрхийлэл бичих
- Илэрхийлэл ба statement-ийн ялгааг ойлгох
- Юуг render хийж болох, юуг болохгүйг мэдэх

### Яагаад чухал вэ

UI бараг үргэлж өгөгдлөөс хамаарна: хэрэглэгчийн нэр, барааны үнэ,
сагсны тоо. JSX-д өгөгдлийг `{}`-оор оруулна.

### {} — JavaScript руу «цонх»

```jsx
const user = { name: "Сараа", points: 1250 };

return (
  <div>
    <h1>Сайн уу, {user.name}!</h1>
    <p>Оноо: {user.points}</p>
    <p>Дараагийн түвшин хүртэл: {2000 - user.points}</p>
    <p>{user.name.toUpperCase()}</p>
  </div>
);
```

`{}` дотор утга буцаадаг **дурын илэрхийлэл** бичиж болно: хувьсагч,
тооцоо, функцийн дуудлага, template string, тернар оператор.

### Statement болохгүй

`if`, `for`, `const x = …` бол statement — утга буцаадаггүй. Тэдгээрийг
`{}` дотор бичих боломжгүй, JSX-ийн **гадна** бичнэ:

```jsx
// ❌ <p>{if (points > 1000) { "VIP" }}</p>

// ✅ Тернар — илэрхийлэл
<p>{user.points > 1000 ? "VIP гишүүн" : "Энгийн гишүүн"}</p>

// ✅ Эсвэл return-ийн өмнө тооцоол
const level = user.points > 1000 ? "VIP" : "Энгийн";
```

### Юуг render хийж болох вэ

| Утга | Юу харагдах |
|---|---|
| Текст, тоо | Шууд харагдана |
| `true`, `false`, `null`, `undefined` | Юу ч харагдахгүй |
| Массив | Элемент бүр дараалан |
| Объект `{ name: "Бат" }` | **Алдаа:** Objects are not valid as a React child |

Объектын оронд талбарыг нь харуулна: `{user.name}`.

### Тоог форматлах

```jsx
<p>Үнэ: {price.toLocaleString("mn-MN")}₮</p>   {/* 12500 → 12,500₮ */}
```

```quiz
`<p>{user}</p>` гэж бичвэл (`user` нь объект) юу болох вэ?
- [ ] `[object Object]` гэж харагдана
- [x] React алдаа заана: объектыг шууд render хийх боломжгүй
- [ ] Юу ч харагдахгүй
> Объектын талбарыг сонгож харуулна: `{user.name}`.
```

### Дүгнэлт

`{}` дотор илэрхийлэл бичнэ. Statement-ийг JSX-ийн гадна бичнэ. Текст,
тоо, массивыг render хийж болно, объектыг болохгүй.
""",
            initial_code=vite(
                """\
const student = {
  name: "Тэмүүлэн",
  birthYear: 2008,
  city: "Эрдэнэт",
  skills: ["HTML", "CSS", "JavaScript"],
  points: 1250,
};

const currentYear = new Date().getFullYear();

export default function App() {
  return (
    <main>
      {/* TODO 1: «Сайн уу, Тэмүүлэн!» гарчгийг student-ээс харуул */}
      <h1>Сайн уу!</h1>
      {/* TODO 2: «Нас: …» — currentYear болон birthYear-ээс тооцоол */}
      {/* TODO 3: «Хот: Эрдэнэт» */}
      {/* TODO 4: «3 ур чадвартай» — skills-ийн уртаас */}
      {/* TODO 5: points 1000-аас их бол «VIP гишүүн», эс бөгөөс «Энгийн гишүүн» */}
    </main>
  );
}
"""
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 10 минут

`student` объектын өгөгдлийг `{}` ашиглан харуул. Текстийг гараар бүү
бич — утга бүрийг объектоос эсвэл тооцооллоос ав. Тест өөр өгөгдлөөр
шалгахгүй ч «Хөтөч» дээр `student`-ийг өөрчилж үзээд бүх текст дагаж
өөрчлөгдөж буйг шалгаарай.
""",
                tests=(
                    test(
                        "Гарчиг «Сайн уу, Тэмүүлэн!» гэж харагдана",
                        """
render(<App />);
expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent("Сайн уу, Тэмүүлэн!");
""",
                    ),
                    test(
                        "Нас нь одоогийн оноос тооцоологдоно",
                        """
render(<App />);
const age = new Date().getFullYear() - 2008;
expect(screen.text()).toContain("Нас: " + age);
""",
                    ),
                    test(
                        "Хот ба ур чадварын тоо харагдана",
                        """
render(<App />);
expect(screen.text()).toContain("Хот: Эрдэнэт");
expect(screen.text()).toContain("3 ур чадвартай");
""",
                    ),
                    test(
                        "1250 оноотой тул «VIP гишүүн» харагдана",
                        """
render(<App />);
expect(screen.text()).toContain("VIP гишүүн");
expect(screen.text()).not.toContain("Энгийн гишүүн");
""",
                    ),
                ),
                tips="""\
- `<h1>Сайн уу, {student.name}!</h1>`
- Нас: `{currentYear - student.birthYear}` — тооцоо ч илэрхийлэл.
- Уртыг `student.skills.length`-ээр авна.
- Нөхцөлд тернар: `{student.points > 1000 ? "VIP гишүүн" : "Энгийн гишүүн"}`.
""",
                solution=solution(
                    App_jsx="""\
const student = {
  name: "Тэмүүлэн",
  birthYear: 2008,
  city: "Эрдэнэт",
  skills: ["HTML", "CSS", "JavaScript"],
  points: 1250,
};

const currentYear = new Date().getFullYear();

export default function App() {
  return (
    <main>
      <h1>Сайн уу, {student.name}!</h1>
      <p>Нас: {currentYear - student.birthYear}</p>
      <p>Хот: {student.city}</p>
      <p>{student.skills.length} ур чадвартай</p>
      <p>{student.points > 1000 ? "VIP гишүүн" : "Энгийн гишүүн"}</p>
    </main>
  );
}
"""
                ),
            ),
        ),
        LessonSpec(
            title="Attribute, style ба className",
            slug="jsx-attribute-style",
            description="Attribute-д утга дамжуулах, style объект, нөхцөлт класс.",
            duration=840,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Attribute-д `{}`-оор утга өгөх
- `style`-ийг объектоор бичих
- Нөхцөлөөс хамаарч `className` солих
- Boolean attribute (`disabled`, `checked`)

### Яагаад чухал вэ

Товч идэвхгүй болох, алдаатай талбар улаан болох, сонгосон таб
тодрох — бүгд attribute, класс, загварыг өгөгдлөөс хамааруулахад
тулгуурладаг.

### Attribute-д утга

```jsx
const product = { name: "Алим", emoji: "🍎", url: "/products/2" };

<a href={product.url} title={product.name}>
  {product.emoji} {product.name}
</a>
```

Хашилт `"..."` нь тогтмол текст, `{...}` нь JavaScript илэрхийлэл.
Хоёуланг нь хамт бичихгүй: `href="{product.url}"` гэвэл яг ийм текст
болно.

### style — объект

HTML-д `style="color: red; font-size: 18px"` гэж бичдэг. JSX-д `style`
нь **объект** авна, шинж чанарууд camelCase:

```jsx
<p style={{ color: "#16a34a", fontSize: 18, backgroundColor: "#dcfce7" }}>
  Хадгалагдлаа
</p>
```

- Гадна `{}` — JavaScript руу орох, дотор `{}` — объект.
- `font-size` → `fontSize`, `background-color` → `backgroundColor`.
- Тоо өгвөл `px` гэж ойлгоно: `fontSize: 18` → `18px`.

Ихэнх загварыг CSS файлд бичиж `className` ашиглах нь дээр. `style`-ийг
утга нь өгөгдлөөс хамаарах үед (өнгө, өргөн) хэрэглэнэ.

### Нөхцөлт класс

```jsx
const isActive = true;

<button className={isActive ? "tab active" : "tab"}>Нүүр</button>

// Template string-ээр:
<button className={`tab ${isActive ? "active" : ""}`}>Нүүр</button>
```

### Boolean attribute

```jsx
const outOfStock = true;

<button disabled={outOfStock}>Сагсанд нэмэх</button>
<input type="checkbox" checked={true} readOnly />
```

`disabled={false}` бол attribute огт гарахгүй — товч идэвхтэй.

```quiz
`<div style="color: red">` гэж JSX-д бичвэл юу болох вэ?
- [ ] Текст улаан болно
- [x] React алдаа заана — style объект байх ёстой
- [ ] Юу ч болохгүй
> Зөв нь `style={{ color: "red" }}`.
```

### Дүгнэлт

Attribute-д `{}`-оор утга өгнө. `style` нь camelCase объект. Классыг
нөхцөлөөс хамааруулж тооцоолно. `disabled={true/false}` шиг boolean
attribute-ууд өгөгдлөөс шууд хамаарна.
""",
            initial_code=vite(
                """\
const product = {
  name: "Брокколи",
  emoji: "🥦",
  stock: 0,
  color: "#16a34a",
};

export default function App() {
  const outOfStock = product.stock === 0;

  return (
    <article className="product">
      {/* TODO 1: h2-ийн текстийн өнгийг product.color болго (style) */}
      <h2>
        {product.emoji} {product.name}
      </h2>
      {/* TODO 2: outOfStock бол p-ийн className "badge sold-out",
                  эс бөгөөс "badge". Текст: «Дууссан» эсвэл «Байгаа» */}
      <p className="badge">Байгаа</p>
      {/* TODO 3: outOfStock бол товч идэвхгүй (disabled) */}
      <button>Сагсанд нэмэх</button>
    </article>
  );
}
""",
                css="""\
.product {
  max-width: 320px;
  padding: 16px;
  border: 1px solid #d0d7de;
  border-radius: 12px;
}

.badge {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 999px;
  background: #dcfce7;
}

.badge.sold-out {
  background: #fee2e2;
  color: #b42318;
}
""",
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 10 минут

`product`-ийн өгөгдлөөс хамааруулж гарчгийн өнгө, шошгын класс,
текст, товчны `disabled`-ийг тохируул. Брокколи дууссан (`stock: 0`)
тул «Хөтөч» дээр улаан «Дууссан» шошго, идэвхгүй товч харагдах ёстой.
""",
                tests=(
                    test(
                        "Гарчгийн өнгө product.color-оос авна",
                        """
render(<App />);
expect(screen.getByRole("heading", { level: 2 })).toHaveStyle({ color: "#16a34a" });
""",
                    ),
                    test(
                        "Дууссан барааны шошго «Дууссан», sold-out класстай",
                        """
render(<App />);
const badge = screen.getByText("Дууссан");
expect(badge).toHaveClass("badge", "sold-out");
""",
                    ),
                    test(
                        "Дууссан бараанд «Сагсанд нэмэх» товч идэвхгүй",
                        """
render(<App />);
expect(screen.getByRole("button", { name: "Сагсанд нэмэх" })).toBeDisabled();
""",
                    ),
                ),
                tips="""\
- `style={{ color: product.color }}` — гадна хаалт JavaScript, дотор нь объект.
- `className={outOfStock ? "badge sold-out" : "badge"}`
- Текстийг ч мөн тернараар: `{outOfStock ? "Дууссан" : "Байгаа"}`.
- `disabled={outOfStock}`
""",
                solution=solution(
                    App_jsx="""\
const product = {
  name: "Брокколи",
  emoji: "🥦",
  stock: 0,
  color: "#16a34a",
};

export default function App() {
  const outOfStock = product.stock === 0;

  return (
    <article className="product">
      <h2 style={{ color: product.color }}>
        {product.emoji} {product.name}
      </h2>
      <p className={outOfStock ? "badge sold-out" : "badge"}>
        {outOfStock ? "Дууссан" : "Байгаа"}
      </p>
      <button disabled={outOfStock}>Сагсанд нэмэх</button>
    </article>
  );
}
"""
                ),
            ),
        ),
        LessonSpec(
            title="Fragment",
            slug="fragment",
            description="Илүү div нэмэлгүйгээр олон элемент буцаах.",
            duration=600,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Нэг эх элементийн дүрмийг `div`-гүйгээр биелүүлэх
- `<>…</>` ба `<Fragment>`-ийг хэрэглэх
- Илүү `div` хэзээ асуудал үүсгэдгийг мэдэх

### Яагаад чухал вэ

JSX нэг л эх элемент буцаадаг. Бүгдийг `div`-ээр ороох нь хялбар ч
заримдаа HTML-ийн бүтцийг эвддэг: хүснэгт, жагсаалт, flex/grid layout.

### Асуудал

```jsx
function Rows() {
  return (
    <div>
      <tr><td>Алим</td></tr>
      <tr><td>Сүү</td></tr>
    </div>
  );
}

<table>
  <tbody>
    <Rows />   {/* ❌ tbody дотор div байж болохгүй */}
  </tbody>
</table>
```

Хөтөч ийм HTML-ийг «засах» гээд хүснэгтийг эвддэг, React console-д
анхааруулга гаргана.

### Fragment

**Fragment** нь DOM-д юу ч нэмэхгүйгээр хүүхдүүдийг бүлэглэнэ:

```jsx
function Rows() {
  return (
    <>
      <tr><td>Алим</td></tr>
      <tr><td>Сүү</td></tr>
    </>
  );
}
```

`<>…</>` бол `<Fragment>…</Fragment>`-ийн товч бичлэг. Жагсаалтад
`key` өгөх шаардлагатай үед бүтэн хэлбэрийг хэрэглэнэ (Модул 2):

```jsx
import { Fragment } from "react";

<Fragment key={item.id}>…</Fragment>
```

### Хэзээ хэрэглэх вэ

- `table`, `ul`, `ol`, `dl` дотор олон мөр/элемент буцаах үед.
- Flex, grid эцэгт хүүхдүүд шууд хүүхэд байх ёстой үед.
- Илүү `div` зүгээр л шаардлагагүй үед.

```quiz
`<>…</>` DOM-д юу нэмэх вэ?
- [ ] Хоосон `<div>`
- [ ] `<fragment>` шошго
- [x] Юу ч нэмэхгүй — зөвхөн хүүхдүүд нь үлдэнэ
> Fragment нь зөвхөн JSX-ийн «нэг эх элемент» дүрмийг биелүүлэх хэрэгсэл.
```

### Дүгнэлт

Илүү `div` бүтцийг эвдэж болно. `<>…</>` нь DOM-д ул мөргүйгээр олон
элементийг бүлэглэнэ.
""",
            initial_code=vite(
                """\
function PriceRows() {
  // TODO: div-ийг Fragment болго — tbody дотор шууд tr байх ёстой.
  return (
    <div>
      <tr>
        <td>🍎 Алим</td>
        <td>2,800₮</td>
      </tr>
      <tr>
        <td>🥛 Сүү</td>
        <td>3,200₮</td>
      </tr>
    </div>
  );
}

export default function App() {
  return (
    <table>
      <thead>
        <tr>
          <th>Бараа</th>
          <th>Үнэ</th>
        </tr>
      </thead>
      <tbody>
        <PriceRows />
      </tbody>
    </table>
  );
}
"""
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐ · 5 минут

`PriceRows` нь `div` буцааж байгаа тул хүснэгтийн бүтэц эвдэрч, Console-д
React анхааруулга гарч байна. `div`-ийг Fragment болгож засаарай.
""",
                tests=(
                    test(
                        "Хүснэгтэд 3 мөр (гарчиг + 2 бараа) байна",
                        """
render(<App />);
expect(screen.getAllByRole("row")).toHaveLength(3);
""",
                    ),
                    test(
                        "tbody дотор div байхгүй",
                        """
const { container } = render(<App />);
expect(container.querySelector("tbody > div")).toBeNull();
expect(container.querySelectorAll("tbody > tr")).toHaveLength(2);
""",
                    ),
                    test(
                        "Console-д HTML бүтцийн анхааруулга гарахгүй",
                        """
render(<App />);
expect(logs.some((entry) => /cannot (be a child|appear as a child)/i.test(entry.text))).toBe(false);
""",
                    ),
                ),
                tips="""\
`<div>`-ийг `<>`, `</div>`-ийг `</>` болгоход хангалттай. Fragment нь
DOM-д юу ч нэмэхгүй тул `tr`-ууд шууд `tbody`-ийн хүүхэд болно.
""",
                solution=solution(
                    App_jsx="""\
function PriceRows() {
  return (
    <>
      <tr>
        <td>🍎 Алим</td>
        <td>2,800₮</td>
      </tr>
      <tr>
        <td>🥛 Сүү</td>
        <td>3,200₮</td>
      </tr>
    </>
  );
}

export default function App() {
  return (
    <table>
      <thead>
        <tr>
          <th>Бараа</th>
          <th>Үнэ</th>
        </tr>
      </thead>
      <tbody>
        <PriceRows />
      </tbody>
    </table>
  );
}
"""
                ),
            ),
        ),
        LessonSpec(
            title="Анхны component",
            slug="anhny-component",
            description="JSX буцаадаг функц — component бичих, дахин ашиглах.",
            duration=840,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Component бичих, ашиглах
- Нэрийг том үсгээр эхлүүлэх дүрмийг ойлгох
- `export default` ба нэртэй export-ийн ялгааг давтах

### Яагаад чухал вэ

Component бол React-ийн гол нэгж. Том UI-г жижиг, ойлгомжтой, дахин
ашиглагдах хэсгүүдэд хуваах нь бүх React төслийн үндэс.

### Component = JSX буцаадаг функц

```jsx
function Greeting() {
  return <p>Сайн уу! Бид React сурч байна.</p>;
}
```

Ашиглахдаа HTML шошго шиг бичнэ:

```jsx
export default function App() {
  return (
    <main>
      <Greeting />
      <Greeting />
    </main>
  );
}
```

Нэг component-ийг хэдэн ч удаа ашиглаж болно.

### Нэр том үсгээр

React жижиг үсгээр эхэлсэн шошгыг HTML гэж, **том** үсгээр эхэлсэнийг
component гэж ойлгоно:

```jsx
function greeting() { … }
<greeting />   // ❌ React үүнийг HTML-ийн <greeting> шошго гэж ойлгоно
```

Console-д «The tag &lt;greeting&gt; is unrecognized in this browser»
анхааруулга гарна. Component-ийн нэрийг үргэлж **PascalCase**-ээр
бичнэ: `Greeting`, `ProductCard`, `UserAvatar`.

### Component-ийг дээд түвшинд тодорхойл

```jsx
// ❌ Component дотор component тодорхойлохгүй
function App() {
  function Button() { … }
  return <Button />;
}

// ✅ Файлын дээд түвшинд
function Button() { … }
function App() {
  return <Button />;
}
```

Дотор нь тодорхойлбол render бүрт шинэ component үүсэж, удаан ажиллаж,
төлөвөө алддаг.

### Export

```jsx
export function Greeting() { … }           // нэртэй — import { Greeting }
export default function App() { … }        // default — import App
```

```quiz
Аль нь component-ийн зөв нэр вэ?
- [ ] `productCard`
- [x] `ProductCard`
- [ ] `product-card`
- [ ] `PRODUCTcard()`
> Том үсгээр эхэлсэн нэрийг React component гэж танина.
```

### Дүгнэлт

Component бол том үсгээр эхэлсэн, JSX буцаадаг функц. Файлын дээд
түвшинд тодорхойлж, хэдэн ч удаа дахин ашиглана.
""",
            initial_code=vite(
                """\
// TODO 1: «Сайн уу! Бид React сурч байна.» гэсэн <p> буцаадаг
//         Greeting component бичиж, нэрээр нь export хий.

// TODO 2: 👋 эможитой, «avatar» класстай <span> буцаадаг
//         Avatar component бичиж, нэрээр нь export хий.

export default function App() {
  return (
    <main>
      <h1>Component-ууд</h1>
      {/* TODO 3: Avatar-ийг нэг, Greeting-ийг хоёр удаа харуул */}
    </main>
  );
}
"""
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐ · 8 минут

`Greeting`, `Avatar` гэсэн хоёр component бичиж, `export function …`-ээр
гаргаад `App` дотор ашигла.
""",
                tests=(
                    test(
                        "Greeting component бичигдэж export хийгдсэн",
                        """
const { Greeting } = mod("./App");
expect(typeof Greeting).toBe("function");
render(<Greeting />);
expect(screen.getByText("Сайн уу! Бид React сурч байна.")).toBeInTheDocument();
""",
                    ),
                    test(
                        "Avatar нь avatar класстай, 👋-тэй span буцаана",
                        """
const { Avatar } = mod("./App");
expect(typeof Avatar).toBe("function");
const { container } = render(<Avatar />);
const span = container.querySelector("span.avatar");
expect(span).toHaveTextContent("👋");
""",
                    ),
                    test(
                        "App нь Greeting-ийг хоёр удаа харуулна",
                        """
render(<App />);
expect(screen.getAllByText("Сайн уу! Бид React сурч байна.")).toHaveLength(2);
""",
                    ),
                    test(
                        "App нь Avatar-ийг харуулна",
                        """
const { container } = render(<App />);
expect(container.querySelectorAll(".avatar")).toHaveLength(1);
""",
                    ),
                ),
                tips="""\
- `export function Greeting() { return <p>…</p>; }`
- Нэрийг том үсгээр эхлүүл — `greeting` гэвэл React HTML шошго гэж ойлгоно.
- `App` дотор `<Avatar />`, `<Greeting />`, `<Greeting />`.
""",
                solution=solution(
                    App_jsx="""\
export function Greeting() {
  return <p>Сайн уу! Бид React сурч байна.</p>;
}

export function Avatar() {
  return <span className="avatar">👋</span>;
}

export default function App() {
  return (
    <main>
      <h1>Component-ууд</h1>
      <Avatar />
      <Greeting />
      <Greeting />
    </main>
  );
}
"""
                ),
            ),
        ),
        LessonSpec(
            title="Component нийлүүлэх ба файлд хуваах",
            slug="component-niiluuleh",
            description="Component tree, файл бүрт нэг component, import/export.",
            duration=900,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Component-уудыг нийлүүлж мод (tree) бүтээх
- Component бүрийг тусдаа файлд хуваах
- Семантик шошго (`header`, `main`, `footer`) ашиглах

### Яагаад чухал вэ

Бодит апп хэдэн зуун component-той. Бүгдийг нэг файлд бичвэл уншиж,
засахад хэцүү. Ихэнх төсөл **нэг файлд нэг component** зарчмыг баримталдаг.

### Component tree

```jsx
App
├── Header
├── main
│   ├── Post
│   └── Post
└── Footer
```

`App` нь `Header`, `Footer`-ийг агуулна — **эцэг** ба **хүүхэд**
component. Хүүхэд нь бас өөрийн хүүхэдтэй байж болно.

### Файлд хуваах

```jsx
// Header.jsx
export default function Header() {
  return (
    <header>
      <h1>Миний блог</h1>
    </header>
  );
}
```

```jsx
// App.jsx
import Header from "./Header";
import Footer from "./Footer";

export default function App() {
  return (
    <>
      <Header />
      <main>…</main>
      <Footer />
    </>
  );
}
```

- `./` — одоогийн хавтас. Файлын өргөтгөл (`.jsx`)-ийг бичихгүй байж болно.
- Default export-ийг дурын нэрээр импортолж болох ч файлын нэртэй ижил
  нэр өгөх нь ойлгомжтой.
- Том төсөлд `components/Header.jsx` гэх мэт хавтас ашиглана:
  `import Header from "./components/Header";`

### Семантик HTML

`header`, `main`, `footer`, `nav` зэрэг шошго нь дэлгэц уншигч
(screen reader) болон хайлтын системд хуудасны бүтцийг ойлгуулна.
Бүгдийг `div`-ээр бичихээс илүү дээр.

```quiz
`Header.jsx`-ийн `export default function Header()`-ийг `App.jsx`-д хэрхэн импортлох вэ?
- [x] `import Header from "./Header";`
- [ ] `import { Header } from "./Header";`
- [ ] `import "./Header";`
> Хаалт `{}` нь нэртэй export-д зориулагдсан. Default export-ийг хаалтгүй импортолно.
```

### Дүгнэлт

Том UI-г component tree болгон задална. Component бүр өөрийн файлтай,
`export default`-оор гарч, `import`-оор ашиглагдана.
""",
            initial_code=vite(
                """\
import Footer from "./Footer";
import Header from "./Header";

export default function App() {
  return (
    <>
      <Header />
      <main>
        <h2>Анхны нийтлэл</h2>
        <p>Өнөөдөр component-уудыг файлд хувааж сурлаа.</p>
      </main>
      <Footer />
    </>
  );
}
""",
                extra={
                    "Header.jsx": """\
// TODO: <header> дотор «Миний блог» гэсэн <h1> буцаа.
export default function Header() {
  return null;
}
""",
                    "Footer.jsx": """\
// TODO: <footer> дотор «© 2026 Миний блог» гэсэн <p> буцаа.
export default function Footer() {
  return null;
}
""",
                },
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 8 минут

`App.jsx` аль хэдийн `Header`, `Footer`-ийг импортолж байгаа ч тэдгээр
одоохондоо `null` буцааж байна. `Header.jsx`, `Footer.jsx` файлуудыг
гүйцээ — файлуудын tab-ыг дарж солиорой.
""",
                tests=(
                    test(
                        "Header нь <header> дотор «Миний блог» гарчигтай",
                        """
render(<App />);
const header = screen.getByRole("banner");
expect(within(header).getByRole("heading", { level: 1 })).toHaveTextContent("Миний блог");
""",
                    ),
                    test(
                        "Footer нь <footer> дотор «© 2026 Миний блог» текстэй",
                        """
render(<App />);
expect(screen.getByRole("contentinfo")).toHaveTextContent("© 2026 Миний блог");
""",
                    ),
                    test(
                        "Header, Footer нь тусдаа файлаас default export хийгдсэн",
                        """
expect(typeof mod("./Header").default).toBe("function");
expect(typeof mod("./Footer").default).toBe("function");
render(React.createElement(mod("./Header").default));
expect(screen.getByRole("banner")).toBeInTheDocument();
""",
                    ),
                ),
                tips="""\
`Header.jsx`:

- `return (<header><h1>…</h1></header>);`

`Footer.jsx` мөн адил, `footer` ба `p`-тэй. `©` тэмдгийг хуулж тавьж болно.
`App.jsx`-ийг өөрчлөх шаардлагагүй.
""",
                solution=solution(
                    Header_jsx="""\
export default function Header() {
  return (
    <header>
      <h1>Миний блог</h1>
    </header>
  );
}
""",
                    Footer_jsx="""\
export default function Footer() {
  return (
    <footer>
      <p>© 2026 Миний блог</p>
    </footer>
  );
}
""",
                ),
            ),
        ),
        LessonSpec(
            title="Төсөл: Хувийн профайл",
            slug="tusul-huviin-profile",
            description="Header, Profile, Skills, Footer — дөрвөн component-оос профайл хуудас.",
            duration=1800,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Модул 1-д сурсан бүхнээ нэг төсөлд хэрэглэх
- Өгөгдлийг тусдаа файлаас импортолж харуулах
- Component tree-г файлууд болгон зохион байгуулах

### Төслийн бүтэц

```jsx
App
├── Header     — нэр, мэргэжил
├── Profile    — аватар, танилцуулга, хот
├── Skills     — ур чадварын жагсаалт
└── Footer     — холбоо барих
```

Өгөгдөл нь 🔒 `profile.js`-д бэлэн байна. Загвар 🔒 `styles.css`-д
бичигдсэн — классуудыг л зөв ашиглахад хангалттай.

### Алхмууд

**1. Header.jsx** — `<header>` дотор `h1`-д `profile.name`, доор нь `p`-д
`profile.role`.

**2. Profile.jsx** — `card` класстай `section`. `avatar` класстай `div`-д
`profile.emoji`, дараа нь `profile.bio`, `Хот: …`.

**3. Skills.jsx** — `card` класстай `section`, `h2` «Ур чадвар», `skills`
класстай `ul` дотор гурван `li` (`profile.skills[0]`, `[1]`, `[2]`).
Массивыг `map`-аар автоматаар харуулахыг Модул 2-т сурна — одоохондоо
индексээр гаргана.

**4. Footer.jsx** — `<footer>` дотор `profile.email`.

**5. App.jsx** — `page` класстай `div` дотор дөрвөн component-ийг дарааллаар
нь.

### Шалгах зүйлс

- Файл бүр `export default`-той юу?
- `className`, хаасан шошго, нэг эх элемент — JSX-ийн дүрмүүд.
- Өгөгдлийг гараар бичихгүй, `profile`-оос авна.

```quiz
`profile.js`-ийн `export const profile = …`-ийг хэрхэн импортлох вэ?
- [ ] `import profile from "./profile";`
- [x] `import { profile } from "./profile";`
- [ ] `import * from "./profile";`
> Нэртэй export-ийг хаалтанд импортолно.
```

### Дүгнэлт

Энэ төслөөр элемент, JSX, component, файлд хуваах, өгөгдөл харуулах
гэсэн Модул 1-ийн бүх ойлголтыг хэрэглэлээ. Дараагийн модульд
component-уудад **props** дамжуулж, илүү уян хатан болгоно.
""",
            initial_code=vite(
                """\
import Footer from "./Footer";
import Header from "./Header";
import Profile from "./Profile";
import Skills from "./Skills";

export default function App() {
  // TODO: page класстай div дотор Header, Profile, Skills, Footer
  return <div className="page"></div>;
}
""",
                extra={
                    "Header.jsx": """\
import { profile } from "./profile";

export default function Header() {
  // TODO: <header> — h1: profile.name, p: profile.role
  return null;
}
""",
                    "Profile.jsx": """\
import { profile } from "./profile";

export default function Profile() {
  // TODO: <section className="card"> — .avatar div (profile.emoji), bio, «Хот: …»
  return null;
}
""",
                    "Skills.jsx": """\
import { profile } from "./profile";

export default function Skills() {
  // TODO: <section className="card"> — h2 «Ур чадвар», ul.skills дотор 3 li
  return null;
}
""",
                    "Footer.jsx": """\
import { profile } from "./profile";

export default function Footer() {
  // TODO: <footer> дотор profile.email
  return null;
}
""",
                },
                locked={
                    "profile.js": """\
export const profile = {
  name: "Ану Бат",
  role: "Frontend хөгжүүлэгч болохоор суралцаж байна",
  emoji: "👩‍💻",
  bio: "Вэб сайт бүтээх дуртай. Одоо React сурч байна.",
  city: "Улаанбаатар",
  skills: ["HTML", "CSS", "JavaScript"],
  email: "anu@example.mn",
};
""",
                },
                css=PROFILE_CSS,
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 25 минут

Хичээлийн «Алхмууд»-ыг дагаж дөрвөн component-ийг гүйцээж, `App`-д
нийлүүл. Файлуудын хооронд tab-аар шилжинэ. Бүх өгөгдлийг `profile.js`-ээс
ав.
""",
                tests=(
                    test(
                        "Header нь нэр (h1) ба мэргэжлийг харуулна",
                        """
render(<App />);
const header = screen.getByRole("banner");
expect(within(header).getByRole("heading", { level: 1 })).toHaveTextContent("Ану Бат");
expect(header).toHaveTextContent("Frontend хөгжүүлэгч");
""",
                    ),
                    test(
                        "Profile нь аватар, танилцуулга, хотыг харуулна",
                        """
render(<App />);
expect(screen.text()).toContain("👩‍💻");
expect(screen.text()).toContain("Вэб сайт бүтээх дуртай");
expect(screen.text()).toContain("Хот: Улаанбаатар");
""",
                    ),
                    test(
                        "Skills нь «Ур чадвар» гарчиг ба 3 ур чадварын жагсаалттай",
                        """
render(<App />);
expect(screen.getByRole("heading", { name: "Ур чадвар" })).toBeInTheDocument();
const items = screen.getAllByRole("listitem");
expect(items.map((item) => item.textContent.trim())).toEqual(["HTML", "CSS", "JavaScript"]);
""",
                    ),
                    test(
                        "Footer нь имэйлийг харуулна",
                        """
render(<App />);
expect(screen.getByRole("contentinfo")).toHaveTextContent("anu@example.mn");
""",
                    ),
                    test(
                        "Component бүр өөрийн файлд",
                        """
for (const name of ["./Header", "./Profile", "./Skills", "./Footer"]) {
  expect(typeof mod(name).default).toBe("function");
}
const { container } = render(React.createElement(mod("./Skills").default));
expect(container.querySelector("ul")).toBeInTheDocument();
""",
                    ),
                ),
                tips="""\
- Component бүр `profile`-ийг өөрөө импортолсон байгаа — `profile.name` гэх
  мэтээр хэрэглэ.
- `Skills` дотор: `<li>{profile.skills[0]}</li>` гэх мэт гурван мөр.
- `App`: `<div className="page"><Header /><Profile /><Skills /><Footer /></div>`.
- «Хөтөч» хоосон бол аль component `null` буцааж байгааг шалга.
""",
                solution=solution(
                    App_jsx="""\
import Footer from "./Footer";
import Header from "./Header";
import Profile from "./Profile";
import Skills from "./Skills";

export default function App() {
  return (
    <div className="page">
      <Header />
      <Profile />
      <Skills />
      <Footer />
    </div>
  );
}
""",
                    Header_jsx="""\
import { profile } from "./profile";

export default function Header() {
  return (
    <header>
      <h1>{profile.name}</h1>
      <p>{profile.role}</p>
    </header>
  );
}
""",
                    Profile_jsx="""\
import { profile } from "./profile";

export default function Profile() {
  return (
    <section className="card">
      <div className="avatar">{profile.emoji}</div>
      <p>{profile.bio}</p>
      <p>Хот: {profile.city}</p>
    </section>
  );
}
""",
                    Skills_jsx="""\
import { profile } from "./profile";

export default function Skills() {
  return (
    <section className="card">
      <h2>Ур чадвар</h2>
      <ul className="skills">
        <li>{profile.skills[0]}</li>
        <li>{profile.skills[1]}</li>
        <li>{profile.skills[2]}</li>
      </ul>
    </section>
  );
}
""",
                    Footer_jsx="""\
import { profile } from "./profile";

export default function Footer() {
  return (
    <footer>
      <p>Холбоо барих: {profile.email}</p>
    </footer>
  );
}
""",
                ),
            ),
        ),
    ],
)
