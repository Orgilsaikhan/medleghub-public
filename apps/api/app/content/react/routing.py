"""Модул 8 — Routing.

react-router-оор олон хуудастай SPA: `BrowserRouter`, `Routes`, `Route`,
`Link`/`NavLink`, замын параметр, `useNavigate`, үүрлэсэн route ба
`Outlet`, 404 ба query параметр. Төгсгөлд нь «Сургалтын платформ» төсөл.

Sandbox-д `BrowserRouter` нь санах ойн router болж, одоогийн зам «Хөтөч»-ийн
хаягийн мөрөнд харагдана. Тестэд `setPath("/courses/2")`-оор эхлэх замыг
өгнө. 2 дахь хичээлээс эхлэн `BrowserRouter` нь 🔒 `main.jsx`-д байх тул
тест `runMain()`-ээр ажиллана.
"""

from app.content.react.common import files, solution, test, vite
from app.content.types import ExerciseSpec, LessonSpec, ModuleSpec
from app.models.enums import LessonLanguage

JSX = LessonLanguage.JSX

ROUTER_MAIN = """\
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router";
import App from "./App";
import "./styles.css";

createRoot(document.getElementById("root")).render(
  <BrowserRouter>
    <App />
  </BrowserRouter>,
);
"""

ROUTER_CSS = """\
body {
  margin: 0;
  font-family: system-ui, sans-serif;
  background: #f6f8fa;
  color: #1f2328;
}

header {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding: 10px 16px;
  background: #1f2328;
  color: #fff;
}

nav {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  padding: 8px 16px;
  background: #1f2328;
}

header nav {
  padding: 0;
}

nav a {
  padding: 6px 12px;
  border-radius: 6px;
  color: #d0d7de;
  text-decoration: none;
}

nav a:hover {
  color: #fff;
}

nav a.active {
  background: #2da44e;
  color: #fff;
}

main {
  max-width: 640px;
  margin: 0 auto;
  padding: 16px;
}

footer {
  padding: 16px;
  text-align: center;
  color: #57606a;
}

.filters {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.filters button {
  padding: 6px 12px;
  border: 1px solid #d0d7de;
  border-radius: 999px;
  background: #fff;
  cursor: pointer;
}

.filters button[aria-pressed="true"] {
  border-color: #2da44e;
  background: #2da44e;
  color: #fff;
}
"""

COURSES_DATA = """\
export const courses = [
  { id: 1, title: "HTML & CSS үндэс", level: "Анхан", lessons: 60 },
  { id: 2, title: "JavaScript үндэс", level: "Анхан", lessons: 90 },
  { id: 3, title: "React-ээр апп бүтээх", level: "Дунд", lessons: 80 },
  { id: 4, title: "SQL өгөгдлийн сан", level: "Дунд", lessons: 50 },
];
"""

# --- Төсөл: Сургалтын платформ ---------------------------------------------------

PLATFORM_DATA = """\
export const courses = [
  { id: 1, title: "HTML & CSS үндэс", level: "Анхан", emoji: "🎨" },
  { id: 2, title: "JavaScript үндэс", level: "Анхан", emoji: "⚡" },
  { id: 3, title: "React-ээр апп бүтээх", level: "Дунд", emoji: "⚛️" },
];

export const lessons = [
  { id: 101, courseId: 1, title: "HTML гэж юу вэ", minutes: 8, body: "Вэб хуудасны бүтцийг шошгоор тодорхойлно." },
  { id: 102, courseId: 1, title: "CSS сонгогч", minutes: 10, body: "Класс, id, шошгоор элементийг сонгож загварчилна." },
  { id: 201, courseId: 2, title: "Хувьсагч ба төрөл", minutes: 9, body: "let, const, тоо, текст, boolean." },
  { id: 202, courseId: 2, title: "Функц", minutes: 12, body: "Кодыг дахин ашиглагдах хэсэг болгоно." },
  { id: 301, courseId: 3, title: "JSX", minutes: 10, body: "JavaScript дотор HTML шиг бичих синтакс." },
  { id: 302, courseId: 3, title: "Props", minutes: 11, body: "Component-д өгөгдөл дамжуулах арга." },
  { id: 303, courseId: 3, title: "State", minutes: 14, body: "Цаг хугацаанд өөрчлөгдөх өгөгдөл." },
];

export const user = {
  name: "Ану Бат",
  email: "anu@example.mn",
  city: "Улаанбаатар",
  completed: 5,
};
"""

PLATFORM_CSS = """\
body {
  margin: 0;
  font-family: system-ui, sans-serif;
  background: #f6f8fa;
  color: #1f2328;
}

.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.topbar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding: 10px 16px;
  background: #1f2328;
}

.topbar a {
  padding: 6px 12px;
  border-radius: 6px;
  color: #d0d7de;
  text-decoration: none;
}

.topbar a.active {
  background: #2da44e;
  color: #fff;
}

.topbar .brand {
  font-weight: 700;
  color: #fff;
}

.topbar .brand.active {
  background: none;
}

.content {
  flex: 1;
  width: 100%;
  max-width: 720px;
  margin: 0 auto;
  padding: 16px;
  box-sizing: border-box;
}

.card {
  padding: 16px;
  margin-bottom: 12px;
  border: 1px solid #d0d7de;
  border-radius: 12px;
  background: #fff;
}

.course-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 12px;
  padding: 0;
  list-style: none;
}

.muted {
  color: #57606a;
}

.footer {
  padding: 16px;
  text-align: center;
  color: #57606a;
}
"""

PLATFORM_LAYOUT = """\
import { NavLink, Outlet } from "react-router";

export default function Layout() {
  return (
    <div className="app">
      <header className="topbar">
        <NavLink to="/" className="brand">
          📚 Medleghub
        </NavLink>
        <nav>
          <NavLink to="/courses">Сургалтууд</NavLink>
          <NavLink to="/profile">Профайл</NavLink>
          <NavLink to="/settings">Тохиргоо</NavLink>
        </nav>
      </header>
      <main className="content">
        <Outlet />
      </main>
      <footer className="footer">© 2026 Medleghub</footer>
    </div>
  );
}
"""

PLATFORM_HOME = """\
import { Link } from "react-router";
import { user } from "../data";

export default function Home() {
  return (
    <section className="card">
      <h1>Сайн уу, {user.name}!</h1>
      <p className="muted">Өнөөдөр юу сурах вэ?</p>
      <Link to="/courses">Сургалтуудыг үзэх →</Link>
    </section>
  );
}
"""

PLATFORM_PROFILE = """\
import { user } from "../data";

export default function Profile() {
  return (
    <section className="card">
      <h1>Профайл</h1>
      <p>👩‍💻 {user.name}</p>
      <p className="muted">
        {user.email} · {user.city}
      </p>
      <p>Дуусгасан хичээл: {user.completed}</p>
    </section>
  );
}
"""

PLATFORM_SETTINGS = """\
import { useState } from "react";

export default function Settings() {
  const [emails, setEmails] = useState(true);

  return (
    <section className="card">
      <h1>Тохиргоо</h1>
      <label>
        <input type="checkbox" checked={emails} onChange={(event) => setEmails(event.target.checked)} />
        Имэйлээр мэдэгдэл авах
      </label>
    </section>
  );
}
"""

ROUTING = ModuleSpec(
    title="Модул 8 — Routing",
    description="react-router-оор олон хуудастай SPA: зам, холбоос, параметр, layout, 404.",
    lessons=[
        # ------------------------------------------------------------------ 8.1
        LessonSpec(
            title="Client-side routing гэж юу вэ",
            slug="client-routing",
            description="SPA-ийн санаа ба BrowserRouter, Routes, Route-оор хуудсыг замтай холбох.",
            duration=900,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Уламжлалт олон хуудастай сайт ба SPA-ийн ялгааг ойлгох
- Client-side routing хэрхэн ажилладгийг мэдэх
- `BrowserRouter`, `Routes`, `Route`-оор зам бүрт хуудас холбох

### Яагаад чухал вэ

Бодит апп бараг үргэлж олон «хуудастай»: нүүр, сургалтууд, профайл,
тохиргоо. Хэрэглэгч хаягийн мөрөнд `/courses` гэж бичээд шууд тэр хуудсанд
очих, холбоосыг найздаа илгээх, «Буцах» сумаар өмнөх хуудас руу буцахыг
хүлээдэг.

Хуудсаа `useState`-ээр сольж болох ч тэгвэл хаяг өөрчлөгдөхгүй: дахин
ачаалахад нүүр хуудас руу үсэрнэ, холбоосоор хуваалцах боломжгүй, «Буцах»
сум бүр сайтаас гаргана. Routing эдгээрийг бүгдийг шийднэ.

### Уламжлалт сайт ба SPA

Уламжлалт сайтад холбоос дарах бүрт хөтөч серверээс **шинэ HTML** татаж,
хуудсыг бүхэлд нь дахин ачаална. SPA (single-page application)-д HTML ба
JavaScript **нэг л удаа** ачаалагдана. Дараа нь холбоос дарахад:

1. JavaScript дарлтыг барьж, хуудас дахин ачаалагдахыг зогсооно;
2. History API-аар (`history.pushState`) хаягийн мөрийг өөрчилнө;
3. React шинэ хаягт тохирох component-ийг render хийнэ.

Сервер рүү шинэ хуудасны хүсэлт явахгүй, state алдагдахгүй, шилжилт
агшин зуур. Үүнийг **client-side routing** гэнэ. React өөрөө router-гүй
тул ихэвчлэн **React Router** санг ашигладаг.

### Суулгах

Vite төсөлд:

```bash
npm install react-router
```

Энэ засварлагчид сан бэлэн суусан — шууд `import` хийнэ.

React Router-ийн v6 болон түүнээс өмнөх хувилбартай төслүүд
`react-router-dom` багцаас импортолдог. v7-д бүх зүйл `react-router`-т
нэгдэж, v8-д `react-router-dom` бүр хасагдсан. Хуучин код, заавар дээр
`react-router-dom` харвал багцын нэр л өөр, санаа нь ижил. Харин `<Switch>`,
`component={Home}` гэсэн бичлэг бол v5-ынх — одоо ашиглагдахгүй.

### Анхны route-ууд

```jsx
import { BrowserRouter, Route, Routes } from "react-router";

function Home() {
  return <h1>Нүүр хуудас</h1>;
}

function Courses() {
  return <h1>Сургалтууд</h1>;
}

export default function App() {
  return (
    <BrowserRouter>
      <header>📚 Medleghub</header>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/courses" element={<Courses />} />
      </Routes>
    </BrowserRouter>
  );
}
```

- **`BrowserRouter`** — хаягийн мөрийг ажиглаж, доторх бүх component-д
  «одоо ямар зам дээр байна» гэдгийг мэдээлнэ. Аппад **нэг л удаа**, хамгийн
  дээд түвшинд бичнэ.
- **`Routes`** — одоогийн замд хамгийн сайн таарах **нэг** `Route`-ийг
  сонгож render хийнэ. Дарааллаас үл хамааран хамгийн тодорхой зам нь
  сонгогдоно.
- **`Route`** — `path` (зам) ба `element` (тэр замд харуулах JSX)-ийн хос.

`Routes`-ийн гадна байгаа зүйл (дээрх `header`) бүх хуудсанд харагдана,
`Routes`-ийн доторх хэсэг л зам бүрт солигдоно.

`element`-д JSX өгдгийг анхаар: `element={<Home />}`. `element={Home}` гэж
component-ийг өөрийг нь өгвөл юу ч харагдахгүй, React анхааруулга өгнө.

### Таарах route байхгүй бол

`/pricing` гэх мэт бүртгэлгүй зам дээр `Routes` юу ч render хийхгүй,
Console-д `No routes matched location "/pricing"` гэсэн анхааруулга гарна.
Ойлгомжтой «Хуудас олдсонгүй» хуудсыг энэ модулийн 6 дахь хичээлд хийнэ.

### Энэ засварлагч дахь хаягийн мөр

«Хөтөч» tab-ийн дээд талд хаягийн мөр бий — одоогийн зам (`/`,
`/courses`) тэнд харагдана. Тэнд `/courses` гэж бичээд Enter дарвал тэр
хуудас нээгдэнэ, ← → сумнууд жинхэнэ хөтөч шиг ажиллана. Дотроо
`BrowserRouter` санах ойн router болж ажилладаг ч таны бичих код бодит
төсөлтэй яг ижил.

```quiz
Зөвхөн `/` ба `/courses` route-тай апп `/pricing` зам дээр юу харуулах вэ?
- [ ] Нүүр хуудас — бүх зам `/`-ээр эхэлдэг
- [x] `Routes`-ийн оронд юу ч харагдахгүй, Console-д анхааруулга гарна
- [ ] Алдааны overlay гарч апп зогсоно
> `Routes` таарах route олохгүй бол хоосон үлдэнэ. `/` нь зөвхөн яг `/` замд таарна.
```

```quiz
`<Route path="/courses" element={Courses} />` — энэ мөрөнд юу буруу вэ?
- [ ] `path` нь `/`-ээр эхлэх ёсгүй
- [x] `element`-д component биш JSX (`<Courses />`) өгөх ёстой
- [ ] `Route`-ийг `BrowserRouter`-ийн гадна бичих ёстой
> `element` нь «юуг render хийх» — бэлэн JSX элемент хүлээнэ.
```

### Дүгнэлт

SPA нэг удаа ачаалагдаад, хаягийг JavaScript-ээр сольж хуудас солино.
`BrowserRouter` хаягийг ажиглана, `Routes` таарах `Route`-ийг сонгоно,
`Route` зам ба JSX-ийг холбоно. Дараагийн хичээлд хаягийн мөрөнд бичихийн
оронд холбоосоор шилжинэ.
""",
            initial_code=vite(
                """\
// TODO: react-router-оос BrowserRouter, Routes, Route-ийг импортол

function Home() {
  return (
    <main>
      <h1>Нүүр хуудас</h1>
      <p>Medleghub-д тавтай морил! Хаягийн мөрөнд /courses гэж бичээд үзээрэй.</p>
    </main>
  );
}

function Courses() {
  return (
    <main>
      <h1>Сургалтууд</h1>
      <ul>
        <li>HTML & CSS үндэс</li>
        <li>JavaScript үндэс</li>
        <li>React-ээр апп бүтээх</li>
      </ul>
    </main>
  );
}

function About() {
  return (
    <main>
      <h1>Бидний тухай</h1>
      <p>Medleghub бол монгол хэл дээрх програмчлалын сургалтын платформ.</p>
    </main>
  );
}

export default function App() {
  return (
    <>
      <header>📚 Medleghub</header>
      {/* TODO: BrowserRouter > Routes > гурван Route ("/", "/courses", "/about") */}
      <Home />
    </>
  );
}
""",
                css=ROUTER_CSS,
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐ · 8 минут

`App.jsx`-д гурван хуудас бэлэн байгаа ч одоогоор үргэлж `Home` л
харагдаж байна. `BrowserRouter`, `Routes`, `Route` ашиглан `/`, `/courses`,
`/about` зам бүрт харгалзах хуудсыг холбо. Дараа нь «Хөтөч»-ийн хаягийн
мөрөнд `/courses`, `/about` гэж бичиж шалгаарай.
""",
                tests=(
                    test(
                        "«/» зам дээр «Нүүр хуудас» харагдана",
                        """
setPath("/");
render(<App />);
expect(screen.getByRole("heading", { name: "Нүүр хуудас" })).toBeInTheDocument();
""",
                    ),
                    test(
                        "«/courses» зам дээр зөвхөн «Сургалтууд» хуудас харагдана",
                        """
setPath("/courses");
render(<App />);
expect(screen.getByRole("heading", { name: "Сургалтууд" })).toBeInTheDocument();
expect(screen.queryByRole("heading", { name: "Нүүр хуудас" })).toBeNull();
""",
                    ),
                    test(
                        "«/about» зам дээр «Бидний тухай» хуудас харагдана",
                        """
setPath("/about");
render(<App />);
expect(screen.getByRole("heading", { name: "Бидний тухай" })).toBeInTheDocument();
expect(screen.queryByRole("heading", { name: "Нүүр хуудас" })).toBeNull();
""",
                    ),
                    test(
                        "Бүртгэлгүй зам дээр гурван хуудасны аль нь ч харагдахгүй",
                        """
setPath("/pricing");
render(<App />);
for (const name of ["Нүүр хуудас", "Сургалтууд", "Бидний тухай"]) {
  expect(screen.queryByRole("heading", { name })).toBeNull();
}
""",
                    ),
                ),
                tips="""\
- Импорт: `import { BrowserRouter, Route, Routes } from "react-router";`
- Бүтэц: `BrowserRouter` → `Routes` → гурван `Route`. `header`-ийг
  `BrowserRouter` дотор, `Routes`-ийн гадна үлдээж болно.
- `element={<Courses />}` — JSX. `element={Courses}` гэвэл юу ч харагдахгүй.
- Хуучин `<Home />` мөрийг устгахаа бүү март — эс бөгөөс бүх зам дээр нүүр
  хуудас харагдана.
""",
                solution=solution(
                    App_jsx="""\
import { BrowserRouter, Route, Routes } from "react-router";

function Home() {
  return (
    <main>
      <h1>Нүүр хуудас</h1>
      <p>Medleghub-д тавтай морил! Хаягийн мөрөнд /courses гэж бичээд үзээрэй.</p>
    </main>
  );
}

function Courses() {
  return (
    <main>
      <h1>Сургалтууд</h1>
      <ul>
        <li>HTML & CSS үндэс</li>
        <li>JavaScript үндэс</li>
        <li>React-ээр апп бүтээх</li>
      </ul>
    </main>
  );
}

function About() {
  return (
    <main>
      <h1>Бидний тухай</h1>
      <p>Medleghub бол монгол хэл дээрх програмчлалын сургалтын платформ.</p>
    </main>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <header>📚 Medleghub</header>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/courses" element={<Courses />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </BrowserRouter>
  );
}
"""
                ),
            ),
        ),
        # ------------------------------------------------------------------ 8.2
        LessonSpec(
            title="Link ба NavLink",
            slug="link-navlink",
            description="Хуудсыг дахин ачаалахгүй холбоос ба идэвхтэй цэсийг тодруулах NavLink.",
            duration=900,
            language=JSX,
            content="""\
### Энэ хичээлээр

- `<a href>` SPA-д яагаад тохирохгүйг ойлгох
- `Link`-ээр хуудас хооронд шилжих
- `NavLink`-ээр идэвхтэй цэсийг тодруулах (`active` класс, `aria-current`)
- `BrowserRouter`-ийг `main.jsx`-д байрлуулах

### Яагаад чухал вэ

Хэрэглэгч хаягийн мөрөнд бичдэггүй — цэс, холбоос дарж шилждэг. Энгийн
`<a href="/courses">` дарахад хөтөч серверээс хуудсыг шинээр татаж,
JavaScript бүхэлдээ дахин ачаалагдаж, state (сагс, бөглөж буй форм)
устана. SPA-ийн давуу тал алга болно. Бас хэрэглэгч аль хуудсан дээрээ
байгаагаа цэснээс харах ёстой.

### Link

```jsx
import { Link } from "react-router";

<Link to="/courses">Сургалтууд</Link>
```

`Link` нь DOM-д энгийн `<a href="/courses">` болж render хийгдэнэ —
тиймээс хүртээмжтэй: дэлгэц уншигч «холбоос» гэж уншина, баруун товчоор
«шинэ tab-д нээх», `Ctrl` + дарах ажиллана. Харин энгийн дарахад `Link`
дарлтыг барьж (`preventDefault`), хуудсыг дахин ачаалалгүйгээр зөвхөн
замыг сольдог.

Энэ засварлагчид энгийн `<a href>` дарахад шилжихгүй, Console-д «react-router-ийн
`<Link>` ашиглана» гэсэн сануулга гарна.

Гадаад сайт руу (`https://…`) энгийн `<a href>` хэрэглэнэ — `Link` зөвхөн
апп доторх замд.

### NavLink — идэвхтэй цэс

`NavLink` нь `Link` шиг ажиллаад, одоогийн зам таарвал:

- `active` класс нэмнэ;
- `aria-current="page"` attribute нэмнэ — дэлгэц уншигч «одоогийн хуудас»
  гэж уншина.

```jsx
<nav>
  <NavLink to="/">Нүүр</NavLink>
  <NavLink to="/courses">Сургалтууд</NavLink>
</nav>
```

```css
nav a.active {
  background: #2da44e;
  color: white;
}
```

Өөр класс хэрэгтэй бол `className`-д функц өгнө:

```jsx
<NavLink to="/courses" className={({ isActive }) => (isActive ? "tab tab-selected" : "tab")}>
  Сургалтууд
</NavLink>
```

### `end` — хэзээ идэвхтэй вэ

`<NavLink to="/courses">` нь `/courses`-д төдийгүй `/courses/3` гэх мэт
доод замд ч идэвхтэй. Ихэвчлэн энэ нь зөв: сургалтын дэлгэрэнгүй дээр
«Сургалтууд» цэс тодорно. Зөвхөн яг таарахад идэвхтэй болгох бол `end`:

```jsx
<NavLink to="/courses" end>
  Бүх сургалт
</NavLink>
```

`to="/"` бол онцгой: бүх зам `/`-ээр эхэлдэг тул React Router түүнийг
автоматаар зөвхөн яг `/` дээр идэвхтэй болгодог.

```quiz
Хаяг `/courses/3` үед аль нь идэвхтэй (`active`) вэ?
- [ ] `<NavLink to="/">`
- [x] `<NavLink to="/courses">`
- [ ] `<NavLink to="/courses" end>`
> `end`-гүй NavLink доод замд ч идэвхтэй. `/` нь зөвхөн яг `/` дээр идэвхтэй.
```

### BrowserRouter-ийг main.jsx-д

Бодит төсөлд `BrowserRouter`-ийг ихэвчлэн `main.jsx`-д `App`-ийг ороож
бичдэг:

```jsx
createRoot(document.getElementById("root")).render(
  <BrowserRouter>
    <App />
  </BrowserRouter>,
);
```

Ингэснээр `App` доторх бүх component `Link`, router-ийн hook-уудыг
чөлөөтэй ашиглана. Энэ хичээлээс эхлэн 🔒 `main.jsx` ийм болсон тул
`App.jsx`-д зөвхөн `Routes` үлдэнэ.

### Түгээмэл алдаа

- `<Link href="/courses">` — `Link`-ийн prop нь `to`.
- `Link`-ийг router-ийн гадна хэрэглэх → `useHref() may be used only in the
  context of a <Router> component` алдаа.
- Энгийн шилжилтийг `<button onClick>`-оор хийх. Холбоос бол холбоос —
  `Link` ашигла. Үйлдлийн дараах шилжилтийг дараагийн хичээлд үзнэ.

```quiz
SPA-ийн цэсэнд `<a href="/courses">` бичвэл бодит хөтөчид юу болох вэ?
- [ ] `Link`-тэй яг адилхан ажиллана
- [x] Хуудас бүхэлдээ дахин ачаалагдаж, React-ийн state алдагдана
- [ ] Холбоос огт ажиллахгүй
> `<a>` нь хөтчийн жинхэнэ шилжилт хийдэг. `Link` дарлтыг барьж, зөвхөн React-ийн хэсгийг солино.
```

### Дүгнэлт

Апп доторх шилжилтэд `Link`, цэсэнд `NavLink` хэрэглэнэ. `NavLink`
идэвхтэй үедээ `active` класс ба `aria-current="page"`-г өөрөө нэмдэг.
`BrowserRouter` бодит төсөлд `main.jsx`-д байрладаг.
""",
            initial_code=vite(
                """\
import { Route, Routes } from "react-router";

function Home() {
  return <h1>Нүүр хуудас</h1>;
}

function Courses() {
  return <h1>Сургалтууд</h1>;
}

function About() {
  return <h1>Бидний тухай</h1>;
}

export default function App() {
  return (
    <>
      <nav>
        {/* TODO: <a>-г NavLink болго */}
        <a href="/">Нүүр</a>
        <a href="/courses">Сургалтууд</a>
        <a href="/about">Бидний тухай</a>
      </nav>
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/courses" element={<Courses />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </main>
    </>
  );
}
""",
                css=ROUTER_CSS,
                main=ROUTER_MAIN,
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 8 минут

Цэс одоогоор энгийн `<a>` холбоостой тул дарахад хуудас солигдохгүй
(Console-оос сануулгыг хар). Холбоосуудыг `NavLink` болгож, идэвхтэй цэс
ногооноор тодрохыг «Хөтөч» дээр шалга. Загвар 🔒 `styles.css`-д бэлэн —
`active` классыг `NavLink` өөрөө нэмнэ.
""",
                tests=(
                    test(
                        "«Сургалтууд» холбоос дарахад сургалтын хуудас нээгдэнэ",
                        """
await runMain();
await user.click(screen.getByRole("link", { name: "Сургалтууд" }));
expect(await screen.findByRole("heading", { name: "Сургалтууд" })).toBeInTheDocument();
""",
                    ),
                    test(
                        "Цэсээр хэд хэдэн хуудас дамжин шилжинэ",
                        """
await runMain();
await user.click(screen.getByRole("link", { name: "Бидний тухай" }));
expect(await screen.findByRole("heading", { name: "Бидний тухай" })).toBeInTheDocument();
await user.click(screen.getByRole("link", { name: "Нүүр" }));
expect(await screen.findByRole("heading", { name: "Нүүр хуудас" })).toBeInTheDocument();
""",
                    ),
                    test(
                        'Идэвхтэй цэс aria-current="page" тэмдэгтэй, бусад нь үгүй',
                        """
setPath("/courses");
await runMain();
expect(screen.getByRole("link", { name: "Сургалтууд" })).toHaveAttribute("aria-current", "page");
expect(screen.getByRole("link", { name: "Нүүр" })).not.toHaveAttribute("aria-current");
""",
                    ),
                    test(
                        "Идэвхтэй цэс «active» класстай",
                        """
setPath("/about");
await runMain();
expect(screen.getByRole("link", { name: "Бидний тухай" })).toHaveClass("active");
expect(screen.getByRole("link", { name: "Нүүр" })).not.toHaveClass("active");
""",
                    ),
                ),
                tips="""\
- `import { NavLink, Route, Routes } from "react-router";`
- `<a href="/courses">` → `<NavLink to="/courses">`. `href` биш `to`.
- `active` класс, `aria-current`-ийг өөрөө бичих шаардлагагүй — `NavLink`
  одоогийн замыг хараад нэмнэ.
- «Нүүр» (`to="/"`) бусад хуудсан дээр идэвхтэй болохгүй — `/` онцгой
  тохиолдол.
""",
                solution=solution(
                    App_jsx="""\
import { NavLink, Route, Routes } from "react-router";

function Home() {
  return <h1>Нүүр хуудас</h1>;
}

function Courses() {
  return <h1>Сургалтууд</h1>;
}

function About() {
  return <h1>Бидний тухай</h1>;
}

export default function App() {
  return (
    <>
      <nav>
        <NavLink to="/">Нүүр</NavLink>
        <NavLink to="/courses">Сургалтууд</NavLink>
        <NavLink to="/about">Бидний тухай</NavLink>
      </nav>
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/courses" element={<Courses />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </main>
    </>
  );
}
"""
                ),
            ),
        ),
        # ------------------------------------------------------------------ 8.3
        LessonSpec(
            title="Замын параметр: useParams",
            slug="useparams",
            description="`/courses/:id` шиг динамик зам, параметрээр өгөгдөл олох, олдоогүй үеийг харуулах.",
            duration=960,
            language=JSX,
            content="""\
### Энэ хичээлээр

- `:id` гэх мэт динамик сегменттэй route бичих
- `useParams()`-аар замын параметрийг унших
- Параметрээр өгөгдлөөс бичлэг олж, олдоогүй үед мэдэгдэл харуулах

### Яагаад чухал вэ

100 сургалт байлаа гэж бодъё. Сургалт бүрт тусдаа `Route` бичих боломжгүй.
Бүх дэлгэрэнгүй хуудас ижил загвартай — ялгаа нь зөвхөн аль сургалтыг
харуулах. Замд `id` оруулбал нэг component бүгдэд үйлчилнэ: `/courses/1`,
`/courses/2`… Ийм хаягийг хуваалцах, хадгалах, дахин ачаалахад ч зөв
сургалт нээгдэнэ.

### Динамик сегмент

```jsx
<Route path="/courses/:id" element={<CourseDetail />} />
```

`:`-ээр эхэлсэн хэсэг нь **параметр**. `/courses/2`, `/courses/react`
хоёулаа таарна. Харин `/courses` (параметргүй) эсвэл `/courses/2/edit`
(илүү сегменттэй) таарахгүй.

### useParams

```jsx
import { useParams } from "react-router";

function CourseDetail() {
  const { id } = useParams(); // /courses/2 → { id: "2" }
  return <h1>Сургалт №{id}</h1>;
}
```

Параметрийн нэр route-ийн нэртэй таарна: `path="/users/:userId"` бол
`const { userId } = useParams()`.

### Анхаар: параметр үргэлж string

URL бол текст. `useParams()`-ийн утга үргэлж **string**. Өгөгдлийн `id`
тоо бол шууд харьцуулахад олдохгүй:

```jsx
const course = courses.find((c) => c.id === id);         // ❌ 2 === "2" → false
const course = courses.find((c) => c.id === Number(id)); // ✅
```

Энэ бол routing-ийн хамгийн түгээмэл алдаа.

```quiz
Хаяг `/courses/3`, route нь `/courses/:id`. `console.log(typeof id, id === 3)` юу хэвлэх вэ?
- [ ] `number true`
- [x] `string false`
- [ ] `string true`
> URL-ээс ирсэн утга үргэлж текст. Тоотой харьцуулахаас өмнө `Number(id)`.
```

### Олдоогүй үед

Хэрэглэгч `/courses/999` гэж бичиж болно, эсвэл сургалт устгагдсан байж
болно. `find` `undefined` буцаана — шалгахгүй бол `course.title` дээр апп
унана:

```jsx
function CourseDetail() {
  const { id } = useParams();
  const course = courses.find((c) => c.id === Number(id));

  if (!course) {
    return (
      <main>
        <h1>Сургалт олдсонгүй</h1>
        <Link to="/">Бүх сургалт руу буцах</Link>
      </main>
    );
  }

  return (
    <main>
      <h1>{course.title}</h1>
      <p>Түвшин: {course.level}</p>
    </main>
  );
}
```

Эрт буцаалт (early return)-ын ачаар доорх кодыг «`course` заавал байгаа»
гэж итгэлтэй бичнэ.

### Жагсаалтаас холбох

```jsx
{courses.map((course) => (
  <li key={course.id}>
    <Link to={`/courses/${course.id}`}>{course.title}</Link>
  </li>
))}
```

### Олон параметр

```jsx
<Route path="/courses/:courseId/lessons/:lessonId" element={<Lesson />} />
// /courses/3/lessons/12 → { courseId: "3", lessonId: "12" }
```

Бодит аппад дэлгэрэнгүй хуудас нь ихэвчлэн `id`-аар серверээс
(`/api/courses/3`) татдаг — Модул 9-д үзнэ. Санаа нь ижил: параметр →
өгөгдөл → олдсон эсэхийг шалгах.

```jsx
<Route path="/users/:userId" element={<Profile />} />

function Profile() {
  const { id } = useParams();
  return <h1>Хэрэглэгч №{id}</h1>;
}
```

```quiz
Дээрх `Profile` `/users/7` дээр юу харуулах вэ?
- [ ] «Хэрэглэгч №7»
- [x] «Хэрэглэгч №» — `id` нь `undefined`
- [ ] Алдаа гарна
> Параметрийн нэр `userId` тул `const { userId } = useParams()` гэж унших ёстой.
```

### Дүгнэлт

`:id` бүхий нэг route олон хуудсанд үйлчилнэ. `useParams()` параметрийг
**string**-ээр өгнө — тоотой харьцуулахдаа `Number()`. Олдоогүй тохиолдлыг
үргэлж тусад нь харуул.
""",
            initial_code=vite(
                """\
import { Link, Route, Routes } from "react-router";
import { courses } from "./data";

function CourseList() {
  return (
    <main>
      <h1>Сургалтууд</h1>
      <ul>
        {courses.map((course) => (
          <li key={course.id}>
            <Link to={`/courses/${course.id}`}>{course.title}</Link>
          </li>
        ))}
      </ul>
    </main>
  );
}

function CourseDetail() {
  // TODO: useParams-аар id-г аваад courses-оос сургалтыг ол.
  // Олдвол: h1 (нэр), «Түвшин: …», «Хичээл: …», «← Бүх сургалт» холбоос (/).
  // Олдохгүй бол: «Сургалт олдсонгүй».
  return null;
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<CourseList />} />
      {/* TODO: /courses/:id → CourseDetail */}
    </Routes>
  );
}
""",
                locked={"data.js": COURSES_DATA},
                css=ROUTER_CSS,
                main=ROUTER_MAIN,
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 12 минут

Жагсаалтын холбоос бүр `/courses/1`, `/courses/2` гэх мэт зам руу заадаг ч
тэр зам бүртгэгдээгүй байна. `/courses/:id` route нэмж, `CourseDetail`
дээр `useParams`-аар сургалтыг олж нэр (h1), түвшин, хичээлийн тоог
харуул. Байхгүй сургалтад «Сургалт олдсонгүй» гэж бич.
""",
                tests=(
                    test(
                        "«/courses/2» дээр «JavaScript үндэс» гарчиг харагдана",
                        """
setPath("/courses/2");
await runMain();
expect(screen.getByRole("heading", { name: "JavaScript үндэс" })).toBeInTheDocument();
""",
                    ),
                    test(
                        "Дэлгэрэнгүй хуудас түвшин ба хичээлийн тоог харуулна",
                        """
setPath("/courses/3");
await runMain();
expect(screen.getByRole("heading", { name: "React-ээр апп бүтээх" })).toBeInTheDocument();
expect(screen.text()).toContain("Дунд");
expect(screen.text()).toContain("80");
""",
                    ),
                    test(
                        "Жагсаалтын холбоос дарахад тухайн сургалтын хуудас нээгдэнэ",
                        """
setPath("/");
await runMain();
await user.click(screen.getByRole("link", { name: "SQL өгөгдлийн сан" }));
expect(await screen.findByRole("heading", { name: "SQL өгөгдлийн сан" })).toBeInTheDocument();
expect(screen.queryByRole("heading", { name: "Сургалтууд" })).toBeNull();
""",
                    ),
                    test(
                        "Байхгүй сургалтад «Сургалт олдсонгүй» гэж харуулна",
                        """
setPath("/courses/99");
await runMain();
expect(screen.text()).toContain("Сургалт олдсонгүй");
""",
                    ),
                ),
                tips="""\
- Route: `<Route path="/courses/:id" element={<CourseDetail />} />`.
- `const { id } = useParams();` — `id` нь текст (`"2"`). Хайхдаа
  `courses.find((course) => course.id === Number(id))`.
- `find` олохгүй бол `undefined` — `if (!course) return …` гэж эрт буцаа.
  Эс бөгөөс `course.title` дээр апп унана.
- «Хөтөч» дээр жагсаалтаас сургалт сонгоод хаягийн мөрийг ажигла. Мөн
  `/courses/99` гэж бичиж үз.
""",
                solution=solution(
                    App_jsx="""\
import { Link, Route, Routes, useParams } from "react-router";
import { courses } from "./data";

function CourseList() {
  return (
    <main>
      <h1>Сургалтууд</h1>
      <ul>
        {courses.map((course) => (
          <li key={course.id}>
            <Link to={`/courses/${course.id}`}>{course.title}</Link>
          </li>
        ))}
      </ul>
    </main>
  );
}

function CourseDetail() {
  const { id } = useParams();
  const course = courses.find((item) => item.id === Number(id));

  if (!course) {
    return (
      <main>
        <h1>Сургалт олдсонгүй</h1>
        <Link to="/">← Бүх сургалт</Link>
      </main>
    );
  }

  return (
    <main>
      <h1>{course.title}</h1>
      <p>Түвшин: {course.level}</p>
      <p>Хичээл: {course.lessons}</p>
      <Link to="/">← Бүх сургалт</Link>
    </main>
  );
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<CourseList />} />
      <Route path="/courses/:id" element={<CourseDetail />} />
    </Routes>
  );
}
"""
                ),
            ),
        ),
        # ------------------------------------------------------------------ 8.4
        LessonSpec(
            title="useNavigate: кодоор шилжих",
            slug="usenavigate",
            description="Форм илгээсний дараа шилжих, navigate(-1)-ээр буцах, Navigate-ээр чиглүүлэх.",
            duration=960,
            language=JSX,
            content="""\
### Энэ хичээлээр

- `useNavigate()`-ээр үйлдлийн дараа өөр хуудас руу шилжих
- `navigate(-1)`-ээр түүхээр буцах, `replace`-ийн утгыг ойлгох
- `<Navigate>` component-оор render үед чиглүүлэх
- `Link` ба `navigate`-ийн алийг хэзээ хэрэглэхийг ялгах

### Яагаад чухал вэ

Зарим шилжилт холбоос дарснаас биш, **үйлдлийн үр дүнд** болдог:
нэвтэрсний дараа самбар руу, шинэ сургалт хадгалсны дараа жагсаалт руу,
устгасны дараа өмнөх хуудас руу. Энд `Link` тохирохгүй — шилжихээсээ өмнө
баталгаажуулалт, хадгалалт зэрэг кодоо ажиллуулах хэрэгтэй.

### useNavigate

```jsx
import { useNavigate } from "react-router";

function NewCourse({ onCreate }) {
  const [title, setTitle] = useState("");
  const navigate = useNavigate();

  function handleSubmit(event) {
    event.preventDefault();
    if (!title.trim()) return; // хоосон бол шилжихгүй
    onCreate(title.trim());
    navigate("/courses"); // хадгалсны ДАРАА шилжинэ
  }
  // …
}
```

`useNavigate()` нь hook — component-ийн дээд түвшинд дуудаж, буцаасан
`navigate` функцээ event handler дотор хэрэглэнэ.

### Түүхээр буцах

```jsx
<button type="button" onClick={() => navigate(-1)}>
  ← Буцах
</button>
```

`navigate(-1)` хөтчийн «Буцах» сумтай ижил, `navigate(1)` — урагш. Энэ
засварлагчид «Хөтөч»-ийн сумнууд ч мөн адил ажиллана.

Анхаар: хэрэглэгч хуудсанд холбоосоор биш, шууд хаягаар орсон бол түүх
хоосон — `navigate(-1)` бодит хөтөчид сайтаас гаргаж мэднэ. Чухал газарт
тодорхой зам (`navigate("/courses")`) илүү найдвартай.

### replace ба state

```jsx
navigate("/dashboard", { replace: true });
```

`replace` нь түүхэнд шинэ бичлэг нэмэхийн оронд одоогийнхыг **солино**.
Нэвтэрсний дараа хэрэглэгч «Буцах» дарахад нэвтрэх форм руу дахин орохгүй.

Шилжихдээ жижиг өгөгдөл дамжуулж болно — **navigation state**:

```jsx
navigate("/courses", { state: { message: "Сургалт нэмэгдлээ" } });

// /courses хуудсанд:
const location = useLocation();
location.state?.message; // "Сургалт нэмэгдлээ"
```

State нь URL-д харагдахгүй тул хаягийг хуваалцахад алдагдана — зөвхөн
«амжилттай хадгаллаа» гэх мэт нэмэлт мэдээлэлд хэрэглэ.

### Navigate — render үед чиглүүлэх

`navigate()`-ийг render хийх явцад шууд дуудаж болохгүй — React Router
`You should call navigate() in a React.useEffect()…` гэж анхааруулна.
Render үед «энд биш, тэнд оч» гэх бол `<Navigate>` component:

```jsx
function Profile({ user }) {
  if (!user) return <Navigate to="/login" replace />;
  return <h1>{user.name}</h1>;
}

<Route path="/" element={<Navigate to="/courses" replace />} />
```

```jsx
function Saved() {
  const navigate = useNavigate();
  navigate("/courses");
  return <p>Хадгаллаа</p>;
}
```

```quiz
Дээрх `Saved` component-д юу буруу вэ?
- [ ] `useNavigate`-ийг `react`-оос импортлох ёстой
- [x] `navigate`-ийг render үед дуудсан — `<Navigate to="/courses" />` эсвэл event handler хэрэглэнэ
- [ ] `navigate`-д зам биш тоо өгөх ёстой
> Render нь цэвэр байх ёстой. Шилжилт бол гаж нөлөө — handler-т, эсвэл `<Navigate>`-ээр.
```

### Link уу, navigate уу?

| Нөхцөл | Хэрэглэх |
|---|---|
| Хэрэглэгч дарж өөр хуудас руу очих (цэс, жагсаалт) | `Link`, `NavLink` |
| Форм илгээсний, хадгалсны, устгасны дараа | `navigate()` |
| Нөхцөл биелэхгүй бол чиглүүлэх (нэвтрээгүй) | `<Navigate>` |

`Link` бол жинхэнэ холбоос: шинэ tab-д нээх, хаягийг хуулах, дэлгэц уншигч
бүгд ажиллана. `<button onClick={() => navigate("/courses")}>` эдгээрийг
алддаг — энгийн шилжилтэд бүү хэрэглэ.

```quiz
Нэвтэрсний дараа «Буцах» дарахад нэвтрэх хуудас руу дахин орохгүй байлгах аль нь вэ?
- [ ] `navigate(-1)`
- [ ] `navigate("/dashboard")`
- [x] `navigate("/dashboard", { replace: true })`
> `replace` нь нэвтрэх хуудасны бичлэгийг түүхээс шинэ хуудсаар солино.
```

### Дүгнэлт

`useNavigate()` үйлдлийн дараа кодоор шилжинэ, `navigate(-1)` буцна,
`replace` түүхийг солино. Render үеийн чиглүүлэлтэд `<Navigate>`, энгийн
холбоост `Link` хэрэглэнэ.
""",
            initial_code=vite(
                """\
import { useState } from "react";
import { Link, Navigate, Route, Routes, useNavigate } from "react-router";

function CourseList({ courses }) {
  return (
    <main>
      <h1>Сургалтууд</h1>
      <ul>
        {courses.map((course) => (
          <li key={course.id}>{course.title}</li>
        ))}
      </ul>
      <Link to="/new">Шинэ сургалт нэмэх</Link>
    </main>
  );
}

function NewCourse({ onCreate }) {
  const [title, setTitle] = useState("");
  // TODO: const navigate = useNavigate();

  function handleSubmit(event) {
    event.preventDefault();
    // TODO: Нэр хоосон бол зогс. Үгүй бол onCreate(нэр) дуудаж, /courses руу шилж.
  }

  return (
    <main>
      <h1>Шинэ сургалт</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Сургалтын нэр{" "}
          <input value={title} onChange={(event) => setTitle(event.target.value)} />
        </label>{" "}
        <button type="submit">Хадгалах</button>
      </form>
      {/* TODO: дарахад өмнөх хуудас руу буцна */}
      <button type="button">← Буцах</button>
    </main>
  );
}

export default function App() {
  const [courses, setCourses] = useState([
    { id: 1, title: "HTML & CSS үндэс" },
    { id: 2, title: "JavaScript үндэс" },
  ]);

  function addCourse(title) {
    setCourses([...courses, { id: Date.now(), title }]);
  }

  return (
    <Routes>
      <Route path="/" element={<Navigate to="/courses" replace />} />
      <Route path="/courses" element={<CourseList courses={courses} />} />
      <Route path="/new" element={<NewCourse onCreate={addCourse} />} />
    </Routes>
  );
}
""",
                css=ROUTER_CSS,
                main=ROUTER_MAIN,
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 12 минут

«Шинэ сургалт» хуудасны форм ба «Буцах» товч одоогоор юу ч хийхгүй байна.
Форм илгээхэд сургалтыг нэмээд жагсаалт руу, «Буцах» дарахад өмнөх хуудас
руу шилжүүл. Нэр хоосон бол юу ч хийхгүй. «Хөтөч» дээр хаягийн мөр ба
сумнуудыг ажиглаарай.
""",
                tests=(
                    test(
                        "Форм илгээхэд «Сургалтууд» хуудас руу шилжинэ",
                        """
setPath("/new");
await runMain();
await user.type(screen.getByLabelText("Сургалтын нэр"), "Vue үндэс");
await user.click(screen.getByRole("button", { name: "Хадгалах" }));
expect(await screen.findByRole("heading", { name: "Сургалтууд" })).toBeInTheDocument();
""",
                    ),
                    test(
                        "Шинэ сургалт жагсаалтад нэмэгдэнэ",
                        """
setPath("/new");
await runMain();
await user.type(screen.getByLabelText("Сургалтын нэр"), "Vue үндэс");
await user.click(screen.getByRole("button", { name: "Хадгалах" }));
await screen.findByRole("heading", { name: "Сургалтууд" });
expect(screen.getByText("Vue үндэс")).toBeInTheDocument();
""",
                    ),
                    test(
                        "Нэр хоосон бол шилжихгүй",
                        """
setPath("/new");
await runMain();
await user.click(screen.getByRole("button", { name: "Хадгалах" }));
await sleep(50);
expect(screen.getByRole("heading", { name: "Шинэ сургалт" })).toBeInTheDocument();
""",
                    ),
                    test(
                        "«Буцах» товч өмнөх хуудас руу буцаана",
                        """
setPath("/courses");
await runMain();
await user.click(screen.getByRole("link", { name: "Шинэ сургалт нэмэх" }));
await screen.findByRole("heading", { name: "Шинэ сургалт" });
await user.click(screen.getByRole("button", { name: /Буцах/ }));
expect(await screen.findByRole("heading", { name: "Сургалтууд" })).toBeInTheDocument();
""",
                    ),
                ),
                tips="""\
- `const navigate = useNavigate();` — component-ийн дээд түвшинд, handler
  дотор биш.
- `handleSubmit`: `const name = title.trim(); if (!name) return;` дараа нь
  `onCreate(name)` ба `navigate("/courses")`.
- «Буцах»: `onClick={() => navigate(-1)}`.
- `onCreate`-ийг дуудахаа мартвал хуудас солигдох ч жагсаалтад шинэ
  сургалт харагдахгүй.
""",
                solution=solution(
                    App_jsx="""\
import { useState } from "react";
import { Link, Navigate, Route, Routes, useNavigate } from "react-router";

function CourseList({ courses }) {
  return (
    <main>
      <h1>Сургалтууд</h1>
      <ul>
        {courses.map((course) => (
          <li key={course.id}>{course.title}</li>
        ))}
      </ul>
      <Link to="/new">Шинэ сургалт нэмэх</Link>
    </main>
  );
}

function NewCourse({ onCreate }) {
  const [title, setTitle] = useState("");
  const navigate = useNavigate();

  function handleSubmit(event) {
    event.preventDefault();
    const name = title.trim();
    if (!name) return;
    onCreate(name);
    navigate("/courses");
  }

  return (
    <main>
      <h1>Шинэ сургалт</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Сургалтын нэр{" "}
          <input value={title} onChange={(event) => setTitle(event.target.value)} />
        </label>{" "}
        <button type="submit">Хадгалах</button>
      </form>
      <button type="button" onClick={() => navigate(-1)}>
        ← Буцах
      </button>
    </main>
  );
}

export default function App() {
  const [courses, setCourses] = useState([
    { id: 1, title: "HTML & CSS үндэс" },
    { id: 2, title: "JavaScript үндэс" },
  ]);

  function addCourse(title) {
    setCourses([...courses, { id: Date.now(), title }]);
  }

  return (
    <Routes>
      <Route path="/" element={<Navigate to="/courses" replace />} />
      <Route path="/courses" element={<CourseList courses={courses} />} />
      <Route path="/new" element={<NewCourse onCreate={addCourse} />} />
    </Routes>
  );
}
"""
                ),
            ),
        ),
        # ------------------------------------------------------------------ 8.5
        LessonSpec(
            title="Үүрлэсэн route ба Outlet",
            slug="nested-routes",
            description="Толгой, цэс бүхий layout route, Outlet ба index route.",
            duration=960,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Бүх хуудсанд давтагдах толгой, цэс, хөлийг нэг **layout route**-д гаргах
- `<Outlet />`-оор хүүхэд route-ийн байрлалыг заах
- `index` route ба харьцангуй (relative) замыг ойлгох

### Яагаад чухал вэ

Өмнөх хичээлүүдэд цэсийг `Routes`-ийн гадна бичсэн. Бодит аппад хэсэг
бүр өөрийн layout-тай: нүүр, сургалтууд нэг цэстэй; тохиргооны хуудсууд
хажуугийн tab-тай; нэвтрэх хуудас огт цэсгүй. Хуудас бүрт `<Header />`-ийг
хуулж бичвэл нэг өөрчлөлтийг арван газар хийх болно. Үүнийг шийддэг нь
үүрлэсэн route.

### Layout route ба Outlet

```jsx
import { NavLink, Outlet, Route, Routes } from "react-router";

function Layout() {
  return (
    <>
      <header>
        <nav>
          <NavLink to="/">Нүүр</NavLink>
          <NavLink to="/courses">Сургалтууд</NavLink>
        </nav>
      </header>
      <main>
        <Outlet /> {/* хүүхэд route энд render болно */}
      </main>
      <footer>© Medleghub</footer>
    </>
  );
}

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="courses" element={<Courses />} />
        <Route path="about" element={<About />} />
      </Route>
    </Routes>
  );
}
```

- `path`-гүй гадна `Route` нь **layout route**: замд юу ч нэмэхгүй, зөвхөн
  хүүхдүүдээ `Layout`-аар ороож өгнө.
- `/courses` руу ороход React Router эхлээд `Layout`-ийг, дараа нь түүний
  `<Outlet />`-ийн байрлалд `Courses`-ийг render хийнэ.
- Хуудас солигдоход `Layout` дахин үүсэхгүй — зөвхөн `Outlet`-ийн доторх
  хэсэг солигдоно. `Layout` доторх state (жишээ нь нээлттэй цэс) хадгалагдана.

### index route

`<Route index element={<Home />} />` нь эцэг route-ийн **яг өөрийн** зам
(энд `/`) дээр `Outlet`-д харагдана — «хүүхэд сонгогдоогүй үеийн анхдагч
хүүхэд». `index` route-д `path` өгдөггүй.

### Харьцангуй зам

Хүүхэд route-ийн `path` `/`-ээр эхлээгүй бол эцгийн зам дээр нэмэгдэнэ:

```jsx
<Route path="/courses" element={<CoursesLayout />}>
  <Route index element={<CourseList />} />        {/* /courses */}
  <Route path=":id" element={<CourseDetail />} /> {/* /courses/:id */}
</Route>
```

`CoursesLayout` нь зөвхөн сургалтын хэсэгт хамаатай зүйлийг (хажуугийн
шүүлтүүр гэх мэт) агуулж, мөн `<Outlet />`-той байна. Ингэж layout-ууд
олон давхар үүрлэж болно.

```quiz
Дээрх route-уудтай апп `/courses` хаяг дээр юу харуулах вэ?
- [ ] Зөвхөн `CourseList`
- [x] `CoursesLayout`, түүний `Outlet`-ийн байрлалд `CourseList`
- [ ] `CoursesLayout` ба `CourseDetail`
> Эцэг route үргэлж render болно. `Outlet`-д яг `/courses` замд таарах `index` хүүхэд орно.
```

### Түгээмэл алдаа

- **`<Outlet />`-ийг мартах.** Алдаа гарахгүй, зүгээр л хүүхэд хуудас
  харагдахгүй — хамгийн их цаг алддаг алдаа.
- **Хүүхдэд эцгээсээ өөр абсолют зам өгөх.** `/courses` дотор
  `path="/lessons"` гэвэл React Router `Absolute route path "/lessons" nested
  under path "/courses" is not valid` алдаа шиднэ. Хүүхдийн замыг
  харьцангуй (`lessons`) бич.
- Layout дотор `Routes`-ийг дахин бичих — хэрэггүй, `<Outlet />` хангалттай.

```jsx
function Layout() {
  return (
    <>
      <nav>…</nav>
      <main />
    </>
  );
}
```

```quiz
Дээрх `Layout`-тай апп цэс дарахад юу болох вэ?
- [ ] Хуудас бүр `main` дотор харагдана
- [x] Хаяг солигдох ч хуудасны агуулга хэзээ ч харагдахгүй
- [ ] React «Outlet алга» гэсэн алдаа шиднэ
> Хүүхэд route хаана render болохыг зөвхөн `<Outlet />` заана. Түүнгүйгээр алдаагүй, гэхдээ хоосон.
```

### Дүгнэлт

Layout route хуудсуудын нийтлэг хэсгийг нэг газар хадгална, `<Outlet />`
хүүхэд хаана харагдахыг заана. `index` route нь эцгийн яг өөрийн замд,
харьцангуй `path` нь эцгийн зам дээр нэмэгдэнэ.
""",
            initial_code=vite(
                """\
import { Route, Routes } from "react-router";
import Layout from "./components/Layout";
import { About, Courses, Home } from "./pages";

export default function App() {
  return (
    <Routes>
      {/* TODO: Эдгээрийг <Route element={<Layout />}> дотор үүрлэж, "/"-г index route болго */}
      <Route path="/" element={<Home />} />
      <Route path="/courses" element={<Courses />} />
      <Route path="/about" element={<About />} />
    </Routes>
  );
}
""",
                extra={
                    "components/Layout.jsx": """\
import { NavLink } from "react-router";

export default function Layout() {
  return (
    <>
      <header>
        <strong>📚 Medleghub</strong>
        <nav>
          <NavLink to="/">Нүүр</NavLink>
          <NavLink to="/courses">Сургалтууд</NavLink>
          <NavLink to="/about">Бидний тухай</NavLink>
        </nav>
      </header>
      <main>{/* TODO: хүүхэд route энд харагдана */}</main>
      <footer>© 2026 Medleghub</footer>
    </>
  );
}
""",
                },
                locked={
                    "pages.jsx": """\
export function Home() {
  return (
    <>
      <h1>Нүүр хуудас</h1>
      <p>Монгол хэл дээр програмчлал сур.</p>
    </>
  );
}

export function Courses() {
  return (
    <>
      <h1>Сургалтууд</h1>
      <ul>
        <li>HTML & CSS үндэс</li>
        <li>JavaScript үндэс</li>
        <li>React-ээр апп бүтээх</li>
      </ul>
    </>
  );
}

export function About() {
  return (
    <>
      <h1>Бидний тухай</h1>
      <p>Medleghub бол монгол хэл дээрх програмчлалын сургалтын платформ.</p>
    </>
  );
}
""",
                },
                css=ROUTER_CSS,
                main=ROUTER_MAIN,
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐ · 12 минут

Гурван хуудас одоогоор тусдаа route бөгөөд цэс, хөл аль нь ч харагдахгүй.
`components/Layout.jsx` бэлэн боловч хүүхэд хуудас харуулах газаргүй.
Route-уудыг `Layout` дотор үүрлэж, нүүр хуудсыг `index` route болгоод,
`Layout`-ийн `main` дотор `<Outlet />` нэм.
""",
                tests=(
                    test(
                        "Нүүр хуудас «/» дээр цэстэйгээ харагдана",
                        """
setPath("/");
await runMain();
expect(screen.getByRole("navigation")).toBeInTheDocument();
expect(screen.getByRole("heading", { name: "Нүүр хуудас" })).toBeInTheDocument();
""",
                    ),
                    test(
                        "Хуудас бүр Layout-ийн <main> дотор харагдана",
                        """
setPath("/courses");
await runMain();
const main = screen.getByRole("main");
expect(within(main).getByRole("heading", { name: "Сургалтууд" })).toBeInTheDocument();
""",
                    ),
                    test(
                        "Цэсээр шилжихэд толгой, хөл хэвээр, зөвхөн агуулга солигдоно",
                        """
setPath("/");
await runMain();
await user.click(screen.getByRole("link", { name: "Бидний тухай" }));
expect(await screen.findByRole("heading", { name: "Бидний тухай" })).toBeInTheDocument();
expect(screen.queryByRole("heading", { name: "Нүүр хуудас" })).toBeNull();
expect(screen.getByRole("navigation")).toBeInTheDocument();
expect(screen.getByRole("contentinfo")).toHaveTextContent("Medleghub");
""",
                    ),
                ),
                tips="""\
- `App.jsx`: `<Route element={<Layout />}>` гэсэн path-гүй route дотор
  `<Route index element={<Home />} />`, `path="courses"`, `path="about"`.
- Хүүхдийн замыг `/`-гүй (харьцангуй) бичиж болно — `/courses` ч ажиллана,
  учир нь эцэг нь `/`.
- `Layout.jsx`: `import { NavLink, Outlet } from "react-router";`, дараа нь
  `<main><Outlet /></main>`.
- Route-уудыг үүрлэсэн ч хуудас харагдахгүй байвал `Outlet`-ээ шалга.
""",
                solution=files(
                    (
                        "App.jsx",
                        """\
import { Route, Routes } from "react-router";
import Layout from "./components/Layout";
import { About, Courses, Home } from "./pages";

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="courses" element={<Courses />} />
        <Route path="about" element={<About />} />
      </Route>
    </Routes>
  );
}
""",
                    ),
                    (
                        "components/Layout.jsx",
                        """\
import { NavLink, Outlet } from "react-router";

export default function Layout() {
  return (
    <>
      <header>
        <strong>📚 Medleghub</strong>
        <nav>
          <NavLink to="/">Нүүр</NavLink>
          <NavLink to="/courses">Сургалтууд</NavLink>
          <NavLink to="/about">Бидний тухай</NavLink>
        </nav>
      </header>
      <main>
        <Outlet />
      </main>
      <footer>© 2026 Medleghub</footer>
    </>
  );
}
""",
                    ),
                ),
            ),
        ),
        # ------------------------------------------------------------------ 8.6
        LessonSpec(
            title="404 хуудас ба query параметр",
            slug="not-found-search-params",
            description='`path="*"`-ээр олдоогүй хуудас, useSearchParams-аар URL дахь шүүлтүүр.',
            duration=1020,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Бүртгэлгүй бүх замд зориулсан 404 хуудас хийх (`path="*"`)
- URL-ийн query хэсгийг (`?level=beginner`) `useSearchParams`-аар унших,
  өөрчлөх
- Шүүлтүүрийг state-д биш URL-д хадгалах шалтгааныг ойлгох

### Яагаад чухал вэ

Хэрэглэгч хаягийг буруу бичих, хуучирсан холбоос дарах нь элбэг. Хоосон
цагаан дэлгэц «апп эвдэрсэн» мэт санагдана — ойлгомжтой 404 хуудас, нүүр
рүү буцах холбоос хэрэгтэй.

Мөн «Анхан түвшний сургалтууд» гэж шүүсэн жагсаалтын хаягийг найздаа
илгээхэд тэр хүн ч мөн шүүлттэй жагсаалтыг харах ёстой. Шүүлтүүр
`useState`-д байвал хаягт ороогүй тул алдагдана.

### 404: path="*"

```jsx
<Route element={<Layout />}>
  <Route index element={<Home />} />
  <Route path="courses" element={<Courses />} />
  <Route path="*" element={<NotFound />} />
</Route>
```

`*` бүх замд таардаг ч React Router хамгийн **тодорхой** route-ийг
сонгодог тул бусад нь таараагүй үед л ажиллана. Жагсаалтын хаана ч бичиж
болох ч уншихад ойлгомжтой байлгах үүднээс сүүлд нь бичдэг. Layout дотор
байрлуулбал 404 хуудас ч цэстэйгээ харагдана.

```jsx
function NotFound() {
  return (
    <>
      <h1>Хуудас олдсонгүй</h1>
      <p>Таны хайсан хуудас байхгүй эсвэл зөөгдсөн байна.</p>
      <Link to="/">Нүүр хуудас руу буцах</Link>
    </>
  );
}
```

Бодит төслийг байршуулахдаа (Netlify, Vercel, Cloudflare) бүх замыг
`index.html` руу чиглүүлэх «SPA fallback» тохиргоо хийдэг. Эс бөгөөс
`/courses`-ийг шууд нээхэд сервер өөрөө 404 буцааж, React хэзээ ч
ачаалагдахгүй.

```quiz
`<Route path="*">`-ийг бусад route-уудаас ӨМНӨ бичвэл `/courses` дээр юу харагдах вэ?
- [ ] 404 хуудас — эхний таарсан route сонгогдоно
- [x] `Courses` — React Router хамгийн тодорхой route-ийг сонгоно
- [ ] Хоёулаа зэрэг
> React Router route-уудыг дарааллаар биш, тодорхой байдлаар нь эрэмбэлдэг.
```

### Query параметр

URL-ийн `?`-ээс хойших хэсэг: `/courses?level=beginner&q=react`. Замын
параметр (`:id`) «аль бичлэг» гэдгийг заадаг бол query параметр ихэвчлэн
шүүлтүүр, хайлт, эрэмбэ, хуудаслалтад хэрэглэгдэнэ.

```jsx
import { useSearchParams } from "react-router";

function Courses() {
  const [searchParams, setSearchParams] = useSearchParams();
  const level = searchParams.get("level"); // "beginner" эсвэл null

  const visible = level ? courses.filter((c) => c.level === level) : courses;

  return (
    <>
      <button onClick={() => setSearchParams({})}>Бүгд</button>
      <button onClick={() => setSearchParams({ level: "beginner" })}>Анхан</button>
      {/* … visible-ийг жагсаана */}
    </>
  );
}
```

- `searchParams` нь хөтчийн `URLSearchParams` объект: `get`, `has`,
  `getAll`.
- `get` утга байхгүй бол `null`, байвал үргэлж **string** буцаана
  (`?page=2` → `"2"`).
- `setSearchParams` нь `useState`-ийн setter шиг: URL-ийг сольж,
  component-ийг дахин render хийнэ. Түүхэнд шинэ бичлэг нэмэгдэх тул
  «Буцах» сум өмнөх шүүлтүүр рүү буцна.

Бусад параметрийг хадгалж, нэгийг л өөрчлөх бол функцээр:

```jsx
setSearchParams((prev) => {
  const next = new URLSearchParams(prev);
  next.set("level", "beginner"); // ?q=… хэвээр үлдэнэ
  return next;
});
```

```quiz
Хаяг `/courses?page=2`. `searchParams.get("page") + 1` юу болох вэ?
- [ ] `3`
- [x] `"21"`
- [ ] `null`
> Query-ийн утга string. Тоо болгох бол `Number(searchParams.get("page"))`.
```

### URL уу, state уу?

| URL-д (query) | State-д |
|---|---|
| Шүүлтүүр, хайлт, эрэмбэ, хуудасны дугаар | Модал нээлттэй эсэх, бичиж буй текст |
| Хуваалцах, дахин ачаалахад үлдэх ёстой | Түр зуурын, зөвхөн энэ дэлгэцэнд |

Асуух зүйл: «Хаягийг хуваалцахад нөгөө хүн яг ижил зүйл харах ёстой юу?»
Тийм бол URL-д.

Энэ засварлагчид «Хөтөч»-ийн хаягийн мөрөнд `?level=…` хэрхэн өөрчлөгдөхийг
харж, ← сумаар өмнөх шүүлтүүр рүү буцаж болно.

### Дүгнэлт

`path="*"` бусад route таараагүй бүх замыг барина — ойлгомжтой 404 хуудас,
буцах холбоостой байлга. Хуваалцах ёстой шүүлтүүр, хайлтыг `useSearchParams`-
аар URL-д хадгал; утга нь үргэлж string.
""",
            initial_code=vite(
                """\
import { NavLink, Outlet, Route, Routes } from "react-router";
import Courses from "./Courses";
import NotFound from "./NotFound";

function Layout() {
  return (
    <>
      <nav>
        <NavLink to="/">Нүүр</NavLink>
        <NavLink to="/courses">Сургалтууд</NavLink>
      </nav>
      <main>
        <Outlet />
      </main>
    </>
  );
}

function Home() {
  return <h1>Нүүр хуудас</h1>;
}

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="courses" element={<Courses />} />
        {/* TODO: бусад бүх замд NotFound */}
      </Route>
    </Routes>
  );
}
""",
                extra={
                    "Courses.jsx": """\
import { useState } from "react";
import { courses, LEVELS } from "./data";

export default function Courses() {
  // TODO: useState-ийн оронд useSearchParams — ?level=beginner
  const [level, setLevel] = useState(null);
  const visible = level ? courses.filter((course) => course.level === level) : courses;

  return (
    <>
      <h1>Сургалтууд</h1>
      <div className="filters">
        <button type="button" aria-pressed={level === null} onClick={() => setLevel(null)}>
          Бүгд
        </button>
        {Object.entries(LEVELS).map(([value, label]) => (
          <button
            key={value}
            type="button"
            aria-pressed={level === value}
            onClick={() => setLevel(value)}
          >
            {label}
          </button>
        ))}
      </div>
      <ul>
        {visible.map((course) => (
          <li key={course.id}>
            {course.title} <small>({LEVELS[course.level]})</small>
          </li>
        ))}
      </ul>
    </>
  );
}
""",
                    "NotFound.jsx": """\
import { Link } from "react-router";

export default function NotFound() {
  // TODO: h1 «Хуудас олдсонгүй», тайлбар, «Нүүр хуудас руу буцах» холбоос (/)
  return null;
}
""",
                },
                locked={
                    "data.js": """\
export const LEVELS = { beginner: "Анхан", intermediate: "Дунд" };

export const courses = [
  { id: 1, title: "HTML & CSS үндэс", level: "beginner" },
  { id: 2, title: "JavaScript үндэс", level: "beginner" },
  { id: 3, title: "React-ээр апп бүтээх", level: "intermediate" },
  { id: 4, title: "SQL өгөгдлийн сан", level: "intermediate" },
];
""",
                },
                css=ROUTER_CSS,
                main=ROUTER_MAIN,
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐ · 15 минут

Хоёр ажил. Нэгдүгээрт, бүртгэлгүй бүх замд `NotFound` хуудас Layout
дотор харагддаг болгож, хуудсаа гүйцээ. Хоёрдугаарт, сургалтын шүүлтүүр
одоо `useState`-д байгаа тул `/courses?level=intermediate` хаягаар ороход
шүүлт ажиллахгүй. Үүнийг `useSearchParams` болгож, шүүлтүүрийг URL-д
хадгал. Шүүх бүртээ «Хөтөч»-ийн хаягийн мөрийг ажиглаарай.
""",
                tests=(
                    test(
                        "Бүртгэлгүй замд «Хуудас олдсонгүй» цэстэйгээ харагдана",
                        """
setPath("/pricing/2026");
await runMain();
expect(screen.text()).toContain("Хуудас олдсонгүй");
expect(screen.getByRole("navigation")).toBeInTheDocument();
""",
                    ),
                    test(
                        "«Нүүр хуудас руу буцах» холбоос нүүр хуудсыг нээнэ",
                        """
setPath("/abc");
await runMain();
await user.click(screen.getByRole("link", { name: "Нүүр хуудас руу буцах" }));
expect(await screen.findByRole("heading", { name: "Нүүр хуудас" })).toBeInTheDocument();
""",
                    ),
                    test(
                        "«?level=intermediate» хаягаар ороход зөвхөн дунд түвшний сургалт харагдана",
                        """
setPath("/courses?level=intermediate");
await runMain();
expect(screen.text()).toContain("React-ээр апп бүтээх");
expect(screen.text()).toContain("SQL өгөгдлийн сан");
expect(screen.text()).not.toContain("HTML & CSS үндэс");
""",
                    ),
                    test(
                        "Шүүлтүүрийн товч дарахад жагсаалт шүүгдэнэ",
                        """
setPath("/courses");
await runMain();
await user.click(screen.getByRole("button", { name: "Анхан" }));
await waitFor(() => expect(screen.text()).not.toContain("React-ээр апп бүтээх"));
expect(screen.text()).toContain("JavaScript үндэс");
""",
                    ),
                    test(
                        "«Бүгд» дарахад URL-ийн шүүлтүүр арилна",
                        """
setPath("/courses?level=beginner");
await runMain();
expect(screen.text()).not.toContain("SQL өгөгдлийн сан");
await user.click(screen.getByRole("button", { name: "Бүгд" }));
await waitFor(() => expect(screen.text()).toContain("SQL өгөгдлийн сан"));
expect(screen.text()).toContain("HTML & CSS үндэс");
""",
                    ),
                ),
                tips="""\
- 404: Layout доторх route-уудын төгсгөлд `<Route path="*" element={<NotFound />} />`.
- `NotFound`: `<h1>Хуудас олдсонгүй</h1>` ба `<Link to="/">Нүүр хуудас руу буцах</Link>`.
- `Courses`: `const [searchParams, setSearchParams] = useSearchParams();`,
  `const level = searchParams.get("level");` — байхгүй бол `null`.
- Товч: `setSearchParams({ level: value })`, «Бүгд»: `setSearchParams({})`.
- `useState`-ийг үлдээвэл товчнууд ажиллах ч хаягаас ирсэн шүүлтүүрийг
  анзаарахгүй — `useState` URL-ийг мэддэггүй.
""",
                solution=solution(
                    App_jsx="""\
import { NavLink, Outlet, Route, Routes } from "react-router";
import Courses from "./Courses";
import NotFound from "./NotFound";

function Layout() {
  return (
    <>
      <nav>
        <NavLink to="/">Нүүр</NavLink>
        <NavLink to="/courses">Сургалтууд</NavLink>
      </nav>
      <main>
        <Outlet />
      </main>
    </>
  );
}

function Home() {
  return <h1>Нүүр хуудас</h1>;
}

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="courses" element={<Courses />} />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}
""",
                    Courses_jsx="""\
import { useSearchParams } from "react-router";
import { courses, LEVELS } from "./data";

export default function Courses() {
  const [searchParams, setSearchParams] = useSearchParams();
  const level = searchParams.get("level");
  const visible = level ? courses.filter((course) => course.level === level) : courses;

  return (
    <>
      <h1>Сургалтууд</h1>
      <div className="filters">
        <button type="button" aria-pressed={level === null} onClick={() => setSearchParams({})}>
          Бүгд
        </button>
        {Object.entries(LEVELS).map(([value, label]) => (
          <button
            key={value}
            type="button"
            aria-pressed={level === value}
            onClick={() => setSearchParams({ level: value })}
          >
            {label}
          </button>
        ))}
      </div>
      <ul>
        {visible.map((course) => (
          <li key={course.id}>
            {course.title} <small>({LEVELS[course.level]})</small>
          </li>
        ))}
      </ul>
    </>
  );
}
""",
                    NotFound_jsx="""\
import { Link } from "react-router";

export default function NotFound() {
  return (
    <>
      <h1>Хуудас олдсонгүй</h1>
      <p>Таны хайсан хуудас байхгүй эсвэл зөөгдсөн байна.</p>
      <Link to="/">Нүүр хуудас руу буцах</Link>
    </>
  );
}
""",
                ),
            ),
        ),
        # ------------------------------------------------------------------ 8.7
        LessonSpec(
            title="Төсөл: Сургалтын платформ",
            slug="tusul-surgaltyn-platform",
            description="Нүүр, сургалтууд, сургалт, хичээл, профайл, тохиргоо бүхий олон хуудастай SPA.",
            duration=2400,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Модул 8-д сурсан бүхнээ нэг олон хуудастай апп болгон нэгтгэх
- Route-уудын бүтцийг төлөвлөж, хуудсуудыг файлуудад хуваах
- Динамик зам, layout route, 404-ийг хамтад нь хэрэглэх

### Яагаад чухал вэ

Бодит апп дан ганц route биш — хэдэн арван хуудас, тэдгээрийн хоорондох
холбоос, алга болсон өгөгдөл, буруу хаяг бүгд зэрэг байдаг. Хуудас бүрийг
зөв файлд, зөв замд байрлуулж чадвал апп томрох тусам ч ойлгомжтой хэвээр
үлдэнэ.

### Юу бүтээх вэ

Medleghub шиг жижиг сургалтын платформ:

```text
/                 Нүүр хуудас (бэлэн)
/courses          Бүх сургалт
/courses/:id      Нэг сургалт ба түүний хичээлүүд
/lessons/:id      Нэг хичээл
/profile          Профайл (бэлэн)
/settings         Тохиргоо (бэлэн)
*                 404
```

### Файлын бүтэц

```text
App.jsx                 ← route-ууд
components/Layout.jsx   ← толгой, цэс, Outlet (бэлэн)
pages/Home.jsx          ← бэлэн
pages/Courses.jsx       ← TODO
pages/CourseDetail.jsx  ← TODO
pages/Lesson.jsx        ← TODO
pages/Profile.jsx       ← бэлэн
pages/Settings.jsx      ← бэлэн
pages/NotFound.jsx      ← TODO
data.js 🔒              ← сургалт, хичээл, хэрэглэгч
styles.css              ← загвар (хүссэнээрээ өөрчил)
```

Бодит төсөлд хуудсуудыг `pages/` (эсвэл `routes/`) хавтсанд, дахин
ашиглагдах хэсгүүдийг `components/`-д хийдэг. Хавтас доторх файлаас
`data.js`-ийг `../data` гэж импортолно.

### Өгөгдөл

- `courses` — `{ id, title, level, emoji }`
- `lessons` — `{ id, courseId, title, minutes, body }`. Хичээл бүр
  `courseId`-аар сургалтдаа холбогдоно.

### Шаардлага

1. **App.jsx** — бүх route `Layout` дотор. `/` нь `index`, бусад нь
   харьцангуй зам. Сүүлд нь `*` → `NotFound`.
2. **Courses** — h1 «Сургалтууд», сургалт бүр `/courses/:id` руу `Link`
   (холбоосын текст нь сургалтын нэр).
3. **CourseDetail** — h1 нь сургалтын нэр, түвшин, хичээлүүдийн жагсаалт.
   Хичээл бүр `/lessons/:id` руу холбоос. Олдохгүй бол «Сургалт олдсонгүй».
4. **Lesson** — h1 нь хичээлийн нэр, хугацаа (минут), агуулга, хамаарах
   сургалт руу буцах холбоос (`/courses/:courseId`). Олдохгүй бол
   «Хичээл олдсонгүй».
5. **NotFound** — «Хуудас олдсонгүй», нүүр рүү буцах холбоос.

### Зөвлөмж

- `useParams`-ийн утга string — `Number(id)`.
- Сургалтын хичээлүүд: `lessons.filter((lesson) => lesson.courseId === course.id)`.
- Хичээлийн хуудас сургалтаа `lesson.courseId`-аар олно.
- Нэг хэсгийг дуусгах бүрт «Хөтөч» дээр цэс, холбоосоор шилжиж, хаягийн
  мөрөнд `/courses/99`, `/lessons/1`, `/abc` гэж бичиж шалга.

```quiz
`/courses` route дотор хүүхэд болгон `path="lessons/:id"` гэж бичвэл хичээлийн хаяг ямар болох вэ?
- [ ] `/lessons/:id`
- [x] `/courses/lessons/:id`
- [ ] Алдаа гарна
> Харьцангуй зам эцгийн зам дээр нэмэгддэг. Энэ төсөлд хичээл `/lessons/:id` тул Layout-ийн шууд хүүхэд байна.
```

```quiz
Хаяг `/courses/2` үед цэсний «Сургалтууд» (`<NavLink to="/courses">`) яагаад тодорч байна вэ?
- [x] `end`-гүй NavLink доод замд ч идэвхтэй байдаг
- [ ] `Layout` дахин render болсон
- [ ] `index` route-ийн нөлөө
> Энэ бол хүссэн зан төлөв: сургалтын дэлгэрэнгүй «Сургалтууд» хэсгийн нэг хэсэг.
```

### Дүгнэлт

Layout route, `index`, динамик `:id`, `Link`/`NavLink`, 404 — бүгдийг нэг
апп-д хэрэглэлээ. Дараагийн модульд өгөгдлийг `data.js`-ээс биш,
серверийн API-аас татна.
""",
            initial_code=vite(
                """\
import { Route, Routes } from "react-router";
import Layout from "./components/Layout";
import Home from "./pages/Home";
import Profile from "./pages/Profile";
import Settings from "./pages/Settings";
// TODO: Courses, CourseDetail, Lesson, NotFound-ийг импортол

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="profile" element={<Profile />} />
        <Route path="settings" element={<Settings />} />
        {/* TODO: courses, courses/:id, lessons/:id, * */}
      </Route>
    </Routes>
  );
}
""",
                extra={
                    "components/Layout.jsx": PLATFORM_LAYOUT,
                    "pages/Home.jsx": PLATFORM_HOME,
                    "pages/Courses.jsx": """\
import { Link } from "react-router";
import { courses } from "../data";

export default function Courses() {
  // TODO: сургалт бүрийг /courses/:id руу Link-ээр (текст нь нэр)
  return (
    <>
      <h1>Сургалтууд</h1>
    </>
  );
}
""",
                    "pages/CourseDetail.jsx": """\
import { Link, useParams } from "react-router";
import { courses, lessons } from "../data";

export default function CourseDetail() {
  // TODO: useParams → сургалтыг ол. Олдохгүй бол «Сургалт олдсонгүй».
  // h1 (нэр), түвшин, хичээлүүд — хичээл бүр /lessons/:id руу Link.
  return <p>TODO: сургалтын дэлгэрэнгүй</p>;
}
""",
                    "pages/Lesson.jsx": """\
import { Link, useParams } from "react-router";
import { courses, lessons } from "../data";

export default function Lesson() {
  // TODO: useParams → хичээлийг ол. Олдохгүй бол «Хичээл олдсонгүй».
  // h1 (нэр), хугацаа, агуулга, /courses/:courseId руу буцах Link.
  return <p>TODO: хичээл</p>;
}
""",
                    "pages/Profile.jsx": PLATFORM_PROFILE,
                    "pages/Settings.jsx": PLATFORM_SETTINGS,
                    "pages/NotFound.jsx": """\
import { Link } from "react-router";

export default function NotFound() {
  // TODO: «Хуудас олдсонгүй» ба нүүр рүү буцах холбоос
  return null;
}
""",
                },
                locked={"data.js": PLATFORM_DATA},
                css=PLATFORM_CSS,
                css_locked=False,
                main=ROUTER_MAIN,
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐ · 40 минут

Хичээлийн «Шаардлага»-ыг дагаж `App.jsx`-д route-уудаа бүртгээд, TODO
бүхий хуудсуудыг гүйцээ. Хэсэг бүрийг дуусгах бүртээ «Хөтөч» дээр цэс,
холбоосоор шилжиж шалгаарай. Файлуудын хооронд tab-аар шилжинэ.
""",
                tests=(
                    test(
                        "Цэсээр Сургалтууд, Профайл, Тохиргоо хуудсууд нээгдэнэ",
                        """
await runMain();
await user.click(screen.getByRole("link", { name: "Сургалтууд" }));
expect(await screen.findByRole("heading", { name: "Сургалтууд" })).toBeInTheDocument();
await user.click(screen.getByRole("link", { name: "Профайл" }));
expect(await screen.findByRole("heading", { name: "Профайл" })).toBeInTheDocument();
await user.click(screen.getByRole("link", { name: "Тохиргоо" }));
expect(await screen.findByRole("heading", { name: "Тохиргоо" })).toBeInTheDocument();
""",
                    ),
                    test(
                        "Сургалтуудаас сургалт руу, тэндээс хичээл рүү шилжинэ",
                        """
setPath("/courses");
await runMain();
await user.click(screen.getByRole("link", { name: /React-ээр апп бүтээх/ }));
expect(await screen.findByRole("heading", { name: /React-ээр апп бүтээх/ })).toBeInTheDocument();
await user.click(screen.getByRole("link", { name: /Props/ }));
expect(await screen.findByRole("heading", { name: /Props/ })).toBeInTheDocument();
expect(screen.text()).toContain("Component-д өгөгдөл дамжуулах арга.");
""",
                    ),
                    test(
                        "Хичээлийн хуудас хамаарах сургалт руу буцах холбоостой",
                        """
setPath("/lessons/201");
await runMain();
expect(screen.getByRole("heading", { name: /Хувьсагч ба төрөл/ })).toBeInTheDocument();
const back = screen.getAllByRole("link").find((link) => link.getAttribute("href") === "/courses/2");
expect(back).toBeTruthy();
await user.click(back);
expect(await screen.findByRole("heading", { name: /JavaScript үндэс/ })).toBeInTheDocument();
""",
                    ),
                    test(
                        "Байхгүй сургалтад «Сургалт олдсонгүй» гэж харуулна",
                        """
setPath("/courses/99");
await runMain();
expect(screen.text()).toContain("Сургалт олдсонгүй");
""",
                    ),
                    test(
                        "Бүртгэлгүй замд 404 хуудас цэстэйгээ харагдана",
                        """
setPath("/hello/world");
await runMain();
expect(screen.text()).toContain("Хуудас олдсонгүй");
expect(screen.getByRole("navigation")).toBeInTheDocument();
""",
                    ),
                ),
                tips="""\
- `App.jsx`: `<Route path="courses" …>`, `<Route path="courses/:id" …>`,
  `<Route path="lessons/:id" …>`, `<Route path="*" …>` — бүгд `Layout`
  доторх route-уудын дунд.
- `pages/` доторх файлаас: `import { courses, lessons } from "../data";`
- `CourseDetail`: `courses.find((c) => c.id === Number(id))`, хичээлүүд нь
  `lessons.filter((l) => l.courseId === course.id)`.
- `Lesson`: хичээлээ олсны дараа `courses.find((c) => c.id === lesson.courseId)`
  — буцах холбоос `` `/courses/${lesson.courseId}` ``.
- Олдохгүй тохиолдлыг эрт буцаалтаар (`if (!course) return …`) шийд.
""",
                solution=files(
                    (
                        "App.jsx",
                        """\
import { Route, Routes } from "react-router";
import Layout from "./components/Layout";
import CourseDetail from "./pages/CourseDetail";
import Courses from "./pages/Courses";
import Home from "./pages/Home";
import Lesson from "./pages/Lesson";
import NotFound from "./pages/NotFound";
import Profile from "./pages/Profile";
import Settings from "./pages/Settings";

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="courses" element={<Courses />} />
        <Route path="courses/:id" element={<CourseDetail />} />
        <Route path="lessons/:id" element={<Lesson />} />
        <Route path="profile" element={<Profile />} />
        <Route path="settings" element={<Settings />} />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}
""",
                    ),
                    (
                        "pages/Courses.jsx",
                        """\
import { Link } from "react-router";
import { courses } from "../data";

export default function Courses() {
  return (
    <>
      <h1>Сургалтууд</h1>
      <ul className="course-list">
        {courses.map((course) => (
          <li key={course.id} className="card">
            <div>{course.emoji}</div>
            <Link to={`/courses/${course.id}`}>{course.title}</Link>
            <p className="muted">{course.level}</p>
          </li>
        ))}
      </ul>
    </>
  );
}
""",
                    ),
                    (
                        "pages/CourseDetail.jsx",
                        """\
import { Link, useParams } from "react-router";
import { courses, lessons } from "../data";

export default function CourseDetail() {
  const { id } = useParams();
  const course = courses.find((item) => item.id === Number(id));

  if (!course) {
    return (
      <section className="card">
        <h1>Сургалт олдсонгүй</h1>
        <Link to="/courses">← Бүх сургалт</Link>
      </section>
    );
  }

  const courseLessons = lessons.filter((lesson) => lesson.courseId === course.id);

  return (
    <section className="card">
      <Link to="/courses">← Бүх сургалт</Link>
      <h1>
        {course.emoji} {course.title}
      </h1>
      <p className="muted">Түвшин: {course.level}</p>
      <h2>Хичээлүүд</h2>
      <ol>
        {courseLessons.map((lesson) => (
          <li key={lesson.id}>
            <Link to={`/lessons/${lesson.id}`}>{lesson.title}</Link>{" "}
            <span className="muted">· {lesson.minutes} мин</span>
          </li>
        ))}
      </ol>
    </section>
  );
}
""",
                    ),
                    (
                        "pages/Lesson.jsx",
                        """\
import { Link, useParams } from "react-router";
import { courses, lessons } from "../data";

export default function Lesson() {
  const { id } = useParams();
  const lesson = lessons.find((item) => item.id === Number(id));

  if (!lesson) {
    return (
      <section className="card">
        <h1>Хичээл олдсонгүй</h1>
        <Link to="/courses">← Бүх сургалт</Link>
      </section>
    );
  }

  const course = courses.find((item) => item.id === lesson.courseId);

  return (
    <article className="card">
      <Link to={`/courses/${lesson.courseId}`}>← {course.title}</Link>
      <h1>{lesson.title}</h1>
      <p className="muted">⏱ {lesson.minutes} минут</p>
      <p>{lesson.body}</p>
    </article>
  );
}
""",
                    ),
                    (
                        "pages/NotFound.jsx",
                        """\
import { Link } from "react-router";

export default function NotFound() {
  return (
    <section className="card">
      <h1>Хуудас олдсонгүй</h1>
      <p className="muted">Таны хайсан хуудас байхгүй эсвэл зөөгдсөн байна.</p>
      <Link to="/">Нүүр хуудас руу буцах</Link>
    </section>
  );
}
""",
                    ),
                ),
            ),
        ),
    ],
)
