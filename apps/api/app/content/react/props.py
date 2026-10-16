"""Модул 2 — Props ба component.

Props-оор component-д өгөгдөл дамжуулж, нэг component-ийг олон газар
ашиглана: задлалт ба анхдагч утга, `children`, нөхцөлт render, `map`-аар
жагсаалт, `key`, дахин ашиглагдах component-ийн props API. Төгсгөлд нь
олон файлтай барааны каталог бүтээнэ. State хараахан ороогүй — бүх UI
props-оос л хамаарна.
"""

from app.content.react.common import HTML, MAIN_WITH_CSS, files, solution, test, vite
from app.content.types import ExerciseSpec, LessonSpec, ModuleSpec
from app.models.enums import LessonLanguage

JSX = LessonLanguage.JSX

BASE_CSS = """\
body {
  margin: 0;
  padding: 24px;
  font-family: system-ui, sans-serif;
  background: #f6f8f5;
  color: #1f2a1c;
}

h1 {
  margin-top: 0;
}

button {
  font: inherit;
  cursor: pointer;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.card {
  background: #fff;
  border: 1px solid #dfe6da;
  border-radius: 12px;
  padding: 16px;
}

.card h2 {
  margin: 4px 0 8px;
  font-size: 1.1rem;
}

.card p {
  margin: 4px 0;
  color: #55624f;
}
"""

# --- Төсөл: Барааны каталог ---------------------------------------------------

CATALOG_PRODUCTS = """\
export const products = [
  { id: 1, name: "Банана", price: 3500, category: "Жимс", emoji: "🍌", stock: 24 },
  { id: 2, name: "Алим", price: 2800, category: "Жимс", emoji: "🍎", stock: 40 },
  { id: 3, name: "Жүрж", price: 4200, category: "Жимс", emoji: "🍊", stock: 15 },
  { id: 4, name: "Лууван", price: 1900, category: "Ногоо", emoji: "🥕", stock: 30 },
  { id: 5, name: "Брокколи", price: 5200, category: "Ногоо", emoji: "🥦", stock: 0 },
  { id: 6, name: "Сүү", price: 3200, category: "Сүүн бүтээгдэхүүн", emoji: "🥛", stock: 18 },
  { id: 7, name: "Бяслаг", price: 12500, category: "Сүүн бүтээгдэхүүн", emoji: "🧀", stock: 0 },
  { id: 8, name: "Талх", price: 2500, category: "Гурил", emoji: "🍞", stock: 12 },
];
"""

CATALOG_CSS = """\
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: system-ui, sans-serif;
  background: #f4f7f2;
  color: #1f2a1c;
}

.page {
  max-width: 960px;
  margin: 0 auto;
  padding: 0 16px 16px;
}

.header {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  justify-content: space-between;
  gap: 8px;
  padding: 20px 0;
  border-bottom: 2px solid #cfe3c4;
}

.header h1 {
  margin: 0;
  color: #2f6b1f;
  font-size: 1.6rem;
}

.header p {
  margin: 0;
  color: #5b6b55;
}

.grid {
  list-style: none;
  margin: 24px 0;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 16px;
}

.card {
  position: relative;
  background: #fff;
  border: 1px solid #dfe8da;
  border-radius: 14px;
  padding: 16px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
}

.card-emoji {
  font-size: 2.5rem;
}

.card h2 {
  margin: 8px 0 2px;
  font-size: 1.1rem;
}

.category {
  margin: 0;
  color: #6b7a65;
  font-size: 0.85rem;
}

.price {
  margin: 8px 0 4px;
  font-size: 1.2rem;
  font-weight: 700;
  color: #2f6b1f;
}

.stock {
  margin: 0;
  font-size: 0.85rem;
  color: #5b6b55;
}

.badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 600;
}

.sold-out {
  position: absolute;
  top: 12px;
  right: 12px;
  background: #fde2e1;
  color: #a3261f;
}

.footer {
  padding: 16px 0;
  border-top: 1px solid #dfe8da;
  color: #6b7a65;
  font-size: 0.85rem;
  text-align: center;
}
"""

CATALOG_APP_START = """\
import Footer from "./components/Footer";
import Header from "./components/Header";
import ProductList from "./components/ProductList";
import { products } from "./products";

// Алхам 5: Header, ProductList, Footer-ийг энд угсар.
export default function App() {
  return (
    <div className="page">
      <p>Каталог удахгүй нээгдэнэ…</p>
    </div>
  );
}
"""

CATALOG_FORMAT_START = """\
// Алхам 1: 3500 → "3,500₮"
export function formatPrice(price) {
  // TODO: price.toLocaleString("en-US") ашиглаж, төгсгөлд нь "₮" залга
  return price + "₮";
}
"""

CATALOG_HEADER_START = """\
// Алхам 4
export default function Header({ count }) {
  return (
    <header className="header">
      <h1>🥬 Ногоон сагс</h1>
      {/* TODO: count-ийг «8 бараа» хэлбэрээр <p>-д харуул */}
    </header>
  );
}
"""

CATALOG_LIST_START = """\
import ProductCard from "./ProductCard";

// Алхам 3
export default function ProductList({ products }) {
  // TODO: products.map(...)-ээр бараа бүрт ProductCard үүсгэ (key-ээ мартуузай!)
  return <ul className="grid"></ul>;
}
"""

CATALOG_CARD_START = """\
import { formatPrice } from "../format";

// Алхам 2
export default function ProductCard({ product }) {
  // TODO: product-оос name, emoji, category, price, stock-ийг задал
  return (
    <li className="card">
      <div className="card-emoji">❓</div>
      <h2>Барааны нэр</h2>
      {/* TODO: ангилал, formatPrice(price), үлдэгдэл эсвэл «Дууссан» шошго */}
    </li>
  );
}
"""

CATALOG_FOOTER_START = """\
// Алхам 4
export default function Footer() {
  // TODO: <footer className="footer"> дотор «© 2026 Ногоон сагс» гэж харуул
  return null;
}
"""

PROPS = ModuleSpec(
    title="Модул 2 — Props ба component",
    description="Props-оор өгөгдөл дамжуулж, дахин ашиглагдах component, жагсаалт, нөхцөлт UI бүтээнэ.",
    lessons=[
        # --- 1 ------------------------------------------------------------------
        LessonSpec(
            title="Props дамжуулах",
            slug="props-damjuulah",
            description="Component-д өгөгдөл дамжуулж, нэг component-ийг олон янзаар ашиглах.",
            duration=900,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Component-д props дамжуулах: текст, тоо, boolean, объект, массив, функц
- Component дотор `props` объектыг уншиж харуулах
- Props яагаад зөвхөн уншигддаг (read-only) болохыг ойлгох

### Яагаад чухал вэ

Модул 1-д бичсэн component-ууд үргэлж ижил зүйл харуулдаг байсан:
`<ProfileCard />` бүр ижил нэр, ижил зурагтай. Гэтэл онлайн дэлгүүрт 100
бараа байвал 100 өөр component бичихгүй — **нэг** `ProductCard` бичээд,
бараа бүрийн мэдээллийг түүнд **дамжуулна**. Ийнхүү дамжуулж буй өгөгдлийг
**props** (properties — шинж чанарууд) гэдэг.

Props бол component-ийн **параметр**. Функцэд аргумент өгдөг шиг
component-д props өгнө.

### Props дамжуулах, унших

```jsx
function Greeting(props) {
  return <p>Сайн уу, {props.name}!</p>;
}

export default function App() {
  return (
    <>
      <Greeting name="Бат" />
      <Greeting name="Сараа" />
    </>
  );
}
```

`<Greeting name="Бат" />` гэж бичихэд React нь `Greeting` функцийг
`{ name: "Бат" }` объекттой дуудна. Энэ объект нь component-ийн эхний
параметр бөгөөд заншлаар `props` гэж нэрлэдэг. JSX-ийн attribute бүр
объектын нэг талбар болно:

```jsx
<Greeting name="Бат" age={17} />
// props = { name: "Бат", age: 17 }
```

Дамжуулаагүй prop нь `undefined` байх бөгөөд `{undefined}` дэлгэцэнд юу ч
гаргахгүй. Нэрийн том, жижиг үсэг ялгаатай: `props.Name`, `props.name` хоёр
өөр талбар.

### Ямар утга дамжуулж болох вэ

Ямар ч JavaScript утга дамжуулж болно. Текстийг хашилтад, бусад бүгдийг
`{}` дотор бичнэ:

```jsx
<ProductCard
  name="Алим"
  price={2800}
  inStock={true}
  featured
  product={{ name: "Алим", emoji: "🍎" }}
  tags={["жимс", "шинэ"]}
  onBuy={handleBuy}
/>
```

| Prop | Төрөл | Тайлбар |
|---|---|---|
| `name="Алим"` | текст | Хашилтад бичнэ |
| `price={2800}` | тоо | `{}` дотор — `"2800"` бол текст болно |
| `inStock={true}` | boolean | |
| `featured` | boolean | Утгагүй бичвэл `true` |
| `product={{ … }}` | объект | Гадна `{}` — JS илэрхийлэл, дотор `{}` — объект |
| `tags={[…]}` | массив | |
| `onBuy={handleBuy}` | функц | Модул 3-т үйл явдалд хэрэглэнэ |

Хамгийн түгээмэл алдаа нь тоог хашилтад бичих:

```jsx
function Price(props) {
  return <p>Хүргэлттэй: {props.price + 5000}₮</p>;
}

<Price price="2800" />  // «28005000₮» 😬 — текстүүд залгагдлаа
<Price price={2800} />  // «7800₮» ✅
```

### Props зөвхөн уншигдана

Component нь өөрт ирсэн props-ийг **өөрчилж болохгүй**:

```jsx
function Price(props) {
  props.price = props.price * 0.9; // ❌ TypeError: Cannot assign to read only property
  return <p>{props.price}₮</p>;
}
```

React хөгжүүлэлтийн (development) горимд props объектыг «хөлдөөдөг»
(`Object.freeze`) тул энэ мөр алдаа өгнө. Өөр утга хэрэгтэй бол **шинэ
хувьсагч** үүсгэ:

```jsx
function Price(props) {
  const discounted = props.price * 0.9; // ✅
  return <p>{discounted}₮</p>;
}
```

Яагаад ийм дүрэмтэй вэ? Props-ийг **эцэг** component өгдөг — өгөгдөл
эцгээс хүүхэд рүү **нэг чиглэлд** урсана. Хүүхэд нь props-оо өөрчилбөл эцэг
нь мэдэхгүй, дэлгэц өгөгдлөөсөө зөрнө. Тиймээс component нь **цэвэр функц**
шиг байх ёстой: ижил props → ижил үр дүн. Цаг хугацааны явцад өөрчлөгддөг
өгөгдөлд **state** хэрэглэдэг — Модул 3-т үзнэ.

### Бодит төсөлд

Vite, Next.js зэрэг бүх React төсөлд props яг ийм байдлаар ажиллана. UI
сан (MUI, shadcn/ui гэх мэт) ашиглахад ч `<Button variant="contained"
disabled>` гэж props дамжуулна — одоо цаана нь юу болж байгааг ойлгож
байна.

```quiz
`<Price price="2800" />` гэж дамжуулбал component дотор `props.price + 5000` юу болох вэ?
- [ ] `7800`
- [x] `"28005000"`
- [ ] Алдаа гарна
> `"2800"` бол текст тул `+` нь текстүүдийг залгана. Тоо дамжуулахдаа `price={2800}` гэж бич.
```

```quiz
Component дотор ирсэн гарчгийг өөрчилж харуулах зөв арга аль вэ?
- [ ] `props.title = props.title.toUpperCase()`
- [ ] `props = { title: "Шинэ" }`
- [x] `const title = props.title.toUpperCase()` гэж шинэ хувьсагч үүсгэх
> Props-ийг эцэг component удирддаг. Хүүхэд нь зөвхөн уншиж, шаардлагатай бол шинэ утга тооцоолно.
```

### Дүгнэлт

Props нь component-ийн параметр: `<Card title="…" count={3} />` →
`props.title`, `props.count`. Текстээс бусад утгыг `{}`-д бичнэ. Props
зөвхөн уншигдана — өгөгдөл эцгээс хүүхэд рүү урсана.
""",
            initial_code=vite(
                """\
import CourseCard from "./CourseCard";

export default function App() {
  return (
    <main>
      <h1>Манай сургалтууд</h1>
      <div className="grid">
        <CourseCard title="HTML & CSS үндэс" level="Анхан" lessons={60} emoji="🎨" />
        {/* TODO: «JavaScript үндэс», «React-ээр апп бүтээх» сургалтын картыг нэм */}
      </div>
    </main>
  );
}
""",
                extra={
                    "CourseCard.jsx": """\
// TODO: тогтмол утгуудын оронд props.emoji, props.title,
//       props.level, props.lessons-ийг харуул.
export default function CourseCard(props) {
  return (
    <article className="card">
      <div className="emoji">📘</div>
      <h2>Сургалтын нэр</h2>
      <p>Түвшин: ?</p>
      <p>? хичээл</p>
    </article>
  );
}
"""
                },
                css=BASE_CSS
                + """
.emoji {
  font-size: 2rem;
}
""",
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐ · 8 минут

`CourseCard.jsx` одоо ямар ч props өгсөн ижил зүйл харуулж байна. Түүнийг
`props`-оос `emoji`, `title`, `level`, `lessons`-ийг уншдаг болго. Дараа нь
`App.jsx`-д дахиад хоёр карт нэм:

| title | level | lessons | emoji |
|---|---|---|---|
| JavaScript үндэс | Анхан | 90 | 🟨 |
| React-ээр апп бүтээх | Дунд | 111 | ⚛️ |
""",
                tests=(
                    test(
                        "CourseCard нь дамжуулсан гарчгийг харуулна",
                        """
const CourseCard = mod("./CourseCard").default;
render(<CourseCard title="SQL өгөгдлийн сан" level="Дунд" lessons={50} emoji="🗄️" />);
expect(screen.getByRole("heading", { name: /SQL өгөгдлийн сан/ })).toBeInTheDocument();
""",
                    ),
                    test(
                        "CourseCard нь emoji, түвшин, хичээлийн тоог харуулна",
                        """
const CourseCard = mod("./CourseCard").default;
render(<CourseCard title="SQL өгөгдлийн сан" level="Дунд" lessons={50} emoji="🗄️" />);
expect(screen.text()).toContain("🗄️");
expect(screen.text()).toContain("Дунд");
expect(screen.text()).toContain("50 хичээл");
""",
                    ),
                    test(
                        "App нь гурван сургалтын картыг харуулна",
                        """
render(<App />);
expect(screen.getAllByRole("heading", { level: 2 })).toHaveLength(3);
expect(screen.getByRole("heading", { name: /HTML & CSS үндэс/ })).toBeInTheDocument();
expect(screen.getByRole("heading", { name: /JavaScript үндэс/ })).toBeInTheDocument();
expect(screen.getByRole("heading", { name: /React-ээр апп бүтээх/ })).toBeInTheDocument();
""",
                    ),
                    test(
                        "Карт бүр өөрийн түвшин, хичээлийн тоотой",
                        """
render(<App />);
const text = screen.text();
expect(text).toContain("60 хичээл");
expect(text).toContain("90 хичээл");
expect(text).toContain("111 хичээл");
expect(text).toContain("Түвшин: Дунд");
""",
                    ),
                ),
                tips="""\
- `props` бол энгийн объект: `props.title`, `props.lessons` гэж уншина.
- JSX дотор утгыг `{}`-д бичнэ: `<h2>{props.title}</h2>`.
- `App.jsx`-д байгаа `<CourseCard … />` мөрийг хуулж, утгуудыг нь соль.
  Тоог `lessons={90}` гэж `{}`-д бичихээ бүү март.
""",
                solution=solution(
                    App_jsx="""\
import CourseCard from "./CourseCard";

export default function App() {
  return (
    <main>
      <h1>Манай сургалтууд</h1>
      <div className="grid">
        <CourseCard title="HTML & CSS үндэс" level="Анхан" lessons={60} emoji="🎨" />
        <CourseCard title="JavaScript үндэс" level="Анхан" lessons={90} emoji="🟨" />
        <CourseCard title="React-ээр апп бүтээх" level="Дунд" lessons={111} emoji="⚛️" />
      </div>
    </main>
  );
}
""",
                    CourseCard_jsx="""\
export default function CourseCard(props) {
  return (
    <article className="card">
      <div className="emoji">{props.emoji}</div>
      <h2>{props.title}</h2>
      <p>Түвшин: {props.level}</p>
      <p>{props.lessons} хичээл</p>
    </article>
  );
}
""",
                ),
            ),
        ),
        # --- 2 ------------------------------------------------------------------
        LessonSpec(
            title="Props задлах ба анхдагч утга",
            slug="props-zadlah",
            description="Props-ийг параметр дотор задалж, анхдагч утга өгөх, үлдсэнийг нь дамжуулах.",
            duration=900,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Props-ийг параметр дотор нь задлах (destructuring)
- Дамжуулаагүй prop-д анхдагч утга өгөх
- Үлдсэн props-ийг `...rest`-ээр цуглуулж, дотоод элемент рүү дамжуулах
- Объектын бүх талбарыг `{...obj}`-оор props болгох

### Яагаад чухал вэ

`props.title`, `props.price`, `props.emoji`… гэж давтах нь урт бөгөөд
component ямар props хүлээж авдгийг харахад хэцүү. Бодит төслүүдийн бараг
бүх component props-оо **параметр дотор нь задалдаг** — функцийн эхний
мөрийг хармагц юу хэрэгтэйг нь мэднэ.

### Параметр дотор задлах

Модул 0-д үзсэн объект задлалтыг шууд параметрт хэрэглэнэ:

```jsx
// Өмнө нь
function Avatar(props) {
  return <span title={props.name}>{props.emoji}</span>;
}

// Одоо
function Avatar({ name, emoji }) {
  return <span title={name}>{emoji}</span>;
}
```

Хоёулаа яг ижил ажиллана. `{ name, emoji }` нь «props объектоос `name`,
`emoji` талбарыг ав» гэсэн үг.

Түгээмэл алдаа — угалзан хаалтаа мартах:

```jsx
function Avatar(name) {       // ❌ name = бүхэл props объект
  return <span>{name}</span>; // Objects are not valid as a React child
}
```

### Анхдагч утга

```jsx
function Avatar({ name, emoji = "🙂", size = 32 }) {
  return (
    <span title={name} style={{ fontSize: size }}>
      {emoji}
    </span>
  );
}

<Avatar name="Бат" />                         // 🙂, 32px
<Avatar name="Сараа" emoji="🦊" size={48} />  // 🦊, 48px
```

Анхдагч утга зөвхөн prop **`undefined`** үед хэрэглэгдэнэ. `null`, `0`,
`""` дамжуулбал анхдагч утга ажиллахгүй:

```jsx
<Avatar name="Бат" emoji={null} /> // emoji = null → юу ч харагдахгүй
```

### Үлдсэн props: ...rest

Component заримдаа хэдэн props-оо өөрөө хэрэглээд, **бусдыг** нь дотоод
HTML элемент рүү дамжуулах хэрэгтэй. Жишээ нь товч: `disabled`, `title`,
`aria-label`, `className`… бүгдийг нэг бүрчлэн бичихгүй:

```jsx
function PrimaryButton({ label, ...rest }) {
  return (
    <button type="button" {...rest}>
      {label}
    </button>
  );
}

<PrimaryButton label="Илгээх" disabled title="Эхлээд формоо бөглө" />
// rest = { disabled: true, title: "Эхлээд формоо бөглө" }
```

`...rest` нь задалсны дараа **үлдсэн** бүх талбарыг нэг объектод
цуглуулна. JSX дахь `{...rest}` нь тэр объектын талбар бүрийг attribute
болгон тавина. Дараалал чухал: `{...rest}`-ийн **ард** бичсэн attribute
давуу эрхтэй, өмнө нь бичсэнийг rest дарж бичиж болно.

### Объектыг props болгон дэлгэх

```jsx
const course = { title: "SQL өгөгдлийн сан", level: "Дунд", lessons: 50 };

<CourseCard {...course} />
// <CourseCard title="SQL өгөгдлийн сан" level="Дунд" lessons={50} />-тэй ижил
```

Товч боловч болгоомжтой хэрэглэ: хэрэггүй талбар ч дамжиж, ямар props
очиж байгаа нь кодоос харагдахгүй болно. Цөөн props бол нэг бүрчлэн бичих
нь ойлгомжтой.

### Бодит төсөлд

UI сангуудын component бараг бүгд `({ variant, size, ...props })` хэлбэртэй:
өөрийн props-оо авч, үлдсэнийг нь HTML элемент рүү дамжуулдаг. Ингэснээр
`<Button onClick={…} aria-label="…">` гэх мэт жирийн attribute бүр
ажиллана.

```quiz
`function Badge({ color = "green" })` component-д `<Badge color={null} />` дамжуулбал `color` юу болох вэ?
- [ ] `"green"`
- [x] `null`
- [ ] `undefined`
> Анхдагч утга зөвхөн `undefined` үед ажиллана. `null` бол «зориуд хоосон» гэсэн утга.
```

```jsx
function Title(text) {
  return <h2>{text}</h2>;
}

<Title text="Сайн уу" />;
```

```quiz
Дээрх код яагаад алдаа өгөх вэ?
- [ ] `text` prop дамжаагүй
- [x] Параметр нь бүхэл props объект тул `<h2>` дотор объект render хийх гэж байна
- [ ] `<h2>` дотор хувьсагч бичиж болохгүй
> `function Title({ text })` гэж угалзан хаалтаар задлах ёстой.
```

### Дүгнэлт

`function Card({ title, count = 0, ...rest })` — нэг мөрөнд задлалт,
анхдагч утга, үлдсэн props. Анхдагч утга зөвхөн `undefined`-д ажиллана.
`{...rest}`-ээр үлдсэн props-ийг HTML элемент рүү дамжуулна.
""",
            initial_code=vite(
                """\
import IconButton from "./IconButton";

export default function App() {
  return (
    <main>
      <h1>Товчнууд</h1>
      <div className="row">
        <IconButton label="Дэлгэрэнгүй" />
        <IconButton icon="🛒" label="Сагсанд нэмэх" className="primary" />
        <IconButton icon="🗑️" label="Устгах" disabled title="Одоогоор устгах боломжгүй" />
      </div>
    </main>
  );
}
""",
                extra={
                    "IconButton.jsx": """\
// TODO 1: props-оо параметр дотор задал: { icon, label, ...rest }
// TODO 2: icon өгөөгүй үед "👉" байхаар анхдагч утга өг
// TODO 3: ...rest-ийг <button> руу дэлгэж дамжуул
export default function IconButton(props) {
  return (
    <button type="button">
      {props.icon} {props.label}
    </button>
  );
}
"""
                },
                css=BASE_CSS
                + """
.row {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.row button {
  padding: 8px 16px;
  border: 1px solid #cfd8ca;
  border-radius: 8px;
  background: #fff;
}

.row button.primary {
  border-color: #2f6b1f;
  background: #2f6b1f;
  color: #fff;
}

.row button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
""",
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 10 минут

`IconButton.jsx`-ийг дахин ашиглагдахуйц болго: props-оо параметр дотор
задал, `icon` өгөөгүй үед `👉` харуул, бусад бүх props (`disabled`,
`title`, `className`…) `<button>` руу дамжина. `App.jsx` бэлэн — «Хөтөч»
дээрх гурван товч хэрхэн өөрчлөгдөхийг хараарай.
""",
                tests=(
                    test(
                        "icon өгөөгүй бол анхдагч «👉» харагдана",
                        """
const IconButton = mod("./IconButton").default;
render(<IconButton label="Дэлгэрэнгүй" />);
expect(screen.getByRole("button", { name: /Дэлгэрэнгүй/ })).toHaveTextContent("👉");
""",
                    ),
                    test(
                        "icon өгвөл анхдагчийн оронд түүнийг харуулна",
                        """
const IconButton = mod("./IconButton").default;
render(<IconButton icon="🛒" label="Сагслах" />);
const button = screen.getByRole("button", { name: /Сагслах/ });
expect(button).toHaveTextContent("🛒");
expect(button).not.toHaveTextContent("👉");
""",
                    ),
                    test(
                        "disabled, title зэрэг бусад props товч руу дамжина",
                        """
const IconButton = mod("./IconButton").default;
render(<IconButton label="Устгах" disabled title="Эрх хүрэхгүй" />);
const button = screen.getByRole("button", { name: /Устгах/ });
expect(button).toBeDisabled();
expect(button).toHaveAttribute("title", "Эрх хүрэхгүй");
""",
                    ),
                    test(
                        "className prop товчны класс болно",
                        """
const IconButton = mod("./IconButton").default;
render(<IconButton label="Хадгалах" className="primary" />);
expect(screen.getByRole("button", { name: /Хадгалах/ })).toHaveClass("primary");
""",
                    ),
                ),
                tips="""\
- Задлалт, анхдагч утга, rest гурвыг нэг мөрөнд бичиж болно:
  `function IconButton({ icon = "👉", label, ...rest })`.
- `rest` нь `icon`, `label`-ээс бусад бүх props-ийг агуулсан объект. Түүнийг
  `<button type="button" {...rest}>` гэж дэлгэнэ.
- `className`-ийг тусад нь бичих шаардлагагүй — `rest` дотор ирнэ.
- Задалсны дараа `props` гэсэн хувьсагч байхгүй: `props.icon`-ийг `icon`
  болгож солихоо бүү март.
""",
                solution=solution(
                    IconButton_jsx="""\
export default function IconButton({ icon = "👉", label, ...rest }) {
  return (
    <button type="button" {...rest}>
      {icon} {label}
    </button>
  );
}
"""
                ),
            ),
        ),
        # --- 3 ------------------------------------------------------------------
        LessonSpec(
            title="children prop",
            slug="children",
            description="Tag-уудын хооронд бичсэн агуулгыг хүлээн авдаг wrapper component бүтээх.",
            duration=840,
            language=JSX,
            content="""\
### Энэ хичээлээр

- `children` prop гэж юу болохыг ойлгох
- Card, Panel зэрэг «хүрээ» (wrapper) component бичих
- JSX-ийг props болгон дамжуулж, хэд хэдэн «үүр»-тэй component бүтээх

### Яагаад чухал вэ

Сайт бүрт ижил хүрээтэй хайрцгууд байдаг: цагаан дэвсгэр, хүрээ, гарчиг.
Харин **дотор нь** өөр өөр зүйл: нэг нь текст, нөгөө нь жагсаалт, гурав
дахь нь товч. Ийм агуулгыг текст prop болгож дамжуулж чадахгүй — дотор нь
бүтэн JSX байна. Үүнд `children` хэрэглэнэ.

### children гэж юу вэ

HTML-д `<div>` дотор юу ч бичиж болдог шиг өөрийн component-ийн нээх, хаах
tag-ийн хооронд JSX бичиж болно. React тэр агуулгыг `children` нэртэй prop
болгож дамжуулна:

```jsx
function Card({ children }) {
  return <div className="card">{children}</div>;
}

export default function App() {
  return (
    <Card>
      <h2>Сайн уу!</h2>
      <p>Энэ бол картын агуулга.</p>
    </Card>
  );
}
```

`Card` дотор нь юу байгааг мэдэх шаардлагагүй — хаана байрлуулахаа л
шийднэ. `children` нь текст, нэг элемент, олон элемент, бүр өөр component
ч байж болно.

### Гарчигтай хүрээ: props + children

```jsx
function Panel({ title, children }) {
  return (
    <section className="panel">
      <h2>{title}</h2>
      <div className="panel-body">{children}</div>
    </section>
  );
}

<Panel title="Мэдээ">
  <p>Шинэ хичээл нэмэгдлээ!</p>
</Panel>

<Panel title="Ур чадвар">
  <ul>
    <li>HTML</li>
    <li>React</li>
  </ul>
</Panel>
```

Нэг `Panel`, хоёр өөр агуулга. Энэ бол **composition** (угсралт) — жижиг
component-уудыг бие биеийнхээ дотор хийж том UI бүтээх арга. Модул 1-д
component-уудаа угсарч байсан; одоо угсралтын «нүх»-ийг өөрөө үлдээж
сурлаа.

### Түгээмэл алдаа

```jsx
function Card({ title }) {
  return (
    <div className="card">
      <h2>{title}</h2> {/* ❌ children-ийг мартжээ */}
    </div>
  );
}

<Card title="Мэдээ">
  <p>Энэ текст харагдахгүй!</p>
</Card>
```

React алдаа ч, анхааруулга ч өгөхгүй — агуулга зүгээр л алга болно.
`children`-ийг задалж, JSX дотроо байрлуулахаа бүү март. Мөн `<Card />`
гэж өөрөө хаагдсан tag-д `children` байхгүй (`undefined`).

### JSX-ийг бусад props-оор дамжуулах

`children` бол ганц «үүр». Хэд хэдэн газар агуулга оруулах бол JSX-ийг
энгийн prop-оор дамжуулж болно:

```jsx
function Layout({ header, sidebar, children }) {
  return (
    <div className="layout">
      <header>{header}</header>
      <aside>{sidebar}</aside>
      <main>{children}</main>
    </div>
  );
}

<Layout header={<h1>Ногоон сагс</h1>} sidebar={<p>Ангилал</p>}>
  <p>Бараанууд энд</p>
</Layout>
```

JSX бол энгийн JavaScript утга — хувьсагчид хадгалж, props-оор дамжуулж
болно.

### Бодит төсөлд

`Modal`, `Layout`, `Tooltip`, `Button` — бараг бүх UI сан `children`-оор
ажилладаг: `<Button><Icon /> Хадгалах</Button>`. React Router-ийн layout
хуудас ч мөн ийм зарчимтай (Модул 8).

```jsx
function Box({ children }) {
  return <div className="box">{children}</div>;
}

<Box>
  <b>А</b>
  <i>Б</i>
</Box>;
```

```quiz
Дээрх кодод `Box` юу харуулах вэ?
- [ ] Зөвхөн «А»
- [x] «А», «Б» хоёулаа `div.box` дотор
- [ ] Юу ч харуулахгүй — `children` prop дамжуулаагүй
> Tag-уудын хооронд бичсэн бүх зүйл `children` болж ирнэ — хоёр элемент ч гэсэн.
```

```quiz
`<Card title="Мэдээ"><p>Текст</p></Card>` гэж бичсэн ч «Текст» харагдахгүй байна. Шалтгаан нь юу байх магадлалтай вэ?
- [x] `Card` component `{children}`-ийг JSX дотроо байрлуулаагүй
- [ ] `<p>`-г component дотор бичиж болохгүй
- [ ] `title` ба `children`-ийг зэрэг дамжуулж болохгүй
> React ирсэн `children`-ийг автоматаар харуулдаггүй — component өөрөө хаана байрлуулахаа заана.
```

### Дүгнэлт

Tag-уудын хооронд бичсэн JSX `children` prop болж ирнэ. Wrapper component
нь хүрээгээ зурж, `{children}`-ийг дотроо байрлуулна. Олон үүр хэрэгтэй
бол JSX-ийг энгийн props-оор дамжуулна.
""",
            initial_code=vite(
                """\
import Card from "./Card";

export default function App() {
  return (
    <main className="grid">
      <Card title="Миний тухай">
        <p>Намайг Сараа гэдэг. Би React сурч байна.</p>
      </Card>

      <Card title="Ур чадвар">
        <ul>
          <li>HTML & CSS</li>
          <li>JavaScript</li>
          <li>React</li>
        </ul>
      </Card>

      <Card title="Холбоо барих" footer={<button type="button">Мессеж бичих</button>}>
        <p>📧 saraa@example.mn</p>
      </Card>
    </main>
  );
}
""",
                extra={
                    "Card.jsx": """\
export default function Card({ title }) {
  return (
    <section className="card">
      <h2>{title}</h2>
      {/* TODO 1: Card-ын tag-уудын хооронд бичсэн агуулгыг (children) энд харуул */}
      {/* TODO 2: footer prop-ийг <footer className="card-footer"> дотор харуул */}
    </section>
  );
}
"""
                },
                css=BASE_CSS
                + """
.card ul {
  margin: 0;
  padding-left: 20px;
}

.card-footer {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #e6ece2;
}

.card-footer:empty {
  display: none;
}

.card-footer button {
  padding: 6px 12px;
  border: 0;
  border-radius: 8px;
  background: #2f6b1f;
  color: #fff;
}
""",
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 8 минут

`App.jsx` нь `Card`-ыг гурван өөр агуулгатай ашиглаж байгаа ч «Хөтөч»
дээр зөвхөн гарчгууд харагдаж байна. `Card.jsx`-ийг засаж tag-уудын
хоорондох агуулгыг харуул. Мөн `footer` prop-оор ирсэн JSX-ийг картын доод
хэсэгт `<footer>` элемент дотор харуул.
""",
                tests=(
                    test(
                        "Card нь tag-уудын хоорондох агуулгыг (children) харуулна",
                        """
const Card = mod("./Card").default;
render(
  <Card title="Туршилт">
    <p>Дотор текст</p>
  </Card>
);
expect(screen.getByRole("heading", { name: "Туршилт" })).toBeInTheDocument();
expect(screen.getByText("Дотор текст")).toBeInTheDocument();
""",
                    ),
                    test(
                        "Олон элементтэй children-ийг бүгдийг нь харуулна",
                        """
const Card = mod("./Card").default;
render(
  <Card title="Жагсаалт">
    <ul>
      <li>Нэг</li>
      <li>Хоёр</li>
    </ul>
    <button type="button">Дар</button>
  </Card>
);
expect(screen.getAllByRole("listitem")).toHaveLength(2);
expect(screen.getByRole("button", { name: "Дар" })).toBeInTheDocument();
""",
                    ),
                    test(
                        "footer prop-оор ирсэн JSX картын <footer> дотор харагдана",
                        """
const Card = mod("./Card").default;
const { container } = render(
  <Card title="А" footer={<button type="button">Дэлгэрэнгүй</button>}>
    <p>Бие</p>
  </Card>
);
const footer = container.querySelector("footer");
expect(footer).toBeInTheDocument();
expect(footer).toHaveTextContent("Дэлгэрэнгүй");
""",
                    ),
                    test(
                        "App дээр гурван картын агуулга бүгд харагдана",
                        """
render(<App />);
expect(screen.text()).toContain("Намайг Сараа гэдэг");
expect(screen.getAllByRole("listitem")).toHaveLength(3);
expect(screen.text()).toContain("saraa@example.mn");
expect(screen.getByRole("button", { name: "Мессеж бичих" })).toBeInTheDocument();
""",
                    ),
                ),
                tips="""\
- `children` бусад props-той адилхан: `function Card({ title, footer, children })`.
- JSX дотор `{children}` гэж байрлуулна, жишээ нь
  `<div className="card-body">{children}</div>`.
- `footer`-т JSX ирнэ, түүнийг мөн `{footer}` гэж харуулна. CSS нь хоосон
  `.card-footer`-ийг нуудаг тул footer-гүй картад ч асуудалгүй.
""",
                solution=solution(
                    Card_jsx="""\
export default function Card({ title, footer, children }) {
  return (
    <section className="card">
      <h2>{title}</h2>
      <div className="card-body">{children}</div>
      <footer className="card-footer">{footer}</footer>
    </section>
  );
}
"""
                ),
            ),
        ),
        # --- 4 ------------------------------------------------------------------
        LessonSpec(
            title="Нөхцөлт render",
            slug="nohtsolt-render",
            description="if, тернар оператор, && ашиглан нөхцөлөөс хамаарч өөр UI харуулах.",
            duration=960,
            language=JSX,
            content="""\
### Энэ хичээлээр

- `if` ба эрт буцаалт (early return)-аар өөр JSX буцаах
- JSX дотор тернар (`? :`), `&&` ашиглах
- `0 &&` алдаанаас сэргийлэх
- `null` буцааж юу ч харуулахгүй байх

### Яагаад чухал вэ

Бодит UI үргэлж нөхцөлтэй: нэвтэрсэн хэрэглэгчид профайл, нэвтрээгүйд
«Нэвтрэх» товч; бараа дууссан бол «Дууссан» шошго; жагсаалт хоосон бол
«Юу ч олдсонгүй». React-д үүнд тусгай синтакс байхгүй — энгийн
JavaScript-ийн `if`, `? :`, `&&`-ийг хэрэглэнэ.

### if ба эрт буцаалт

JSX-ийн `{}` дотор `if` бичиж болохгүй — тэнд зөвхөн утга буцаадаг
**илэрхийлэл** орно. Харин component-ийн биед `if` чөлөөтэй бичнэ:

```jsx
function Greeting({ user }) {
  if (!user) {
    return <p>Нэвтэрнэ үү.</p>;
  }
  return <p>Сайн уу, {user.name}!</p>;
}
```

Эхэнд нь «онцгой тохиолдлыг» шалгаад буцаавал доорх код `user` байгаа
гэдэгт итгэлтэй ажиллана. Үүнийг **early return** гэдэг.

### Юу ч харуулахгүй: null

```jsx
function Warning({ message }) {
  if (!message) return null;
  return <p className="warning">⚠️ {message}</p>;
}
```

`null` буцаасан component дэлгэцэнд юу ч гаргахгүй.

### Тернар: A эсвэл B

JSX дотор хоёр хувилбараас нэгийг сонгоход:

```jsx
<p>{product.stock > 0 ? "Байгаа" : "Дууссан"}</p>

{isLoggedIn ? <ProfileMenu /> : <LoginButton />}
```

Урт JSX-ийг хаалтад хийж олон мөрөнд бичнэ:

```jsx
{messages.length === 0 ? (
  <p>Мэдэгдэл алга</p>
) : (
  <p>{messages.length} шинэ мэдэгдэл</p>
)}
```

### &&: байвал харуул, үгүй бол юу ч үгүй

```jsx
{isNew && <span className="badge">Шинэ</span>}
```

`isNew` үнэн бол шошго гарна, худал бол юу ч гарахгүй. React `false`,
`null`, `undefined`, `true`-г дэлгэцэнд харуулдаггүй.

### 0 && — хамгийн түгээмэл алдаа

```jsx
{messages.length && <span className="badge">{messages.length}</span>}
```

Мэдэгдэлгүй үед дэлгэцэнд **«0»** гарч ирнэ! `0 && …` нь `0`-ийг
буцаадаг, харин React тоог (тэр дундаа 0-ийг) харуулдаг. `&&`-ийн зүүн
талд үргэлж **boolean** байлга:

```jsx
{messages.length > 0 && <span className="badge">{messages.length}</span>} // ✅
```

### Хувьсагчид JSX бэлдэх

Нөхцөл олон бол JSX-ээ `return`-ээс өмнө хувьсагчид бэлдэж болно:

```jsx
let status;
if (stock === 0) {
  status = <span className="red">Дууссан</span>;
} else if (stock < 5) {
  status = <span className="orange">Цөөн үлдсэн</span>;
} else {
  status = <span className="green">Байгаа</span>;
}

return <div>{status}</div>;
```

Гурав, түүнээс олон хувилбартай үед тернарыг давхарлаж
(`a ? x : b ? y : z`) бичихээс ийм `if` илүү уншигдана.

```quiz
`const count = 0;` бол `<div>{count && <b>Шинэ</b>}</div>` дэлгэцэнд юу харуулах вэ?
- [ ] Юу ч харуулахгүй
- [x] `0`
- [ ] «Шинэ»
> `0 && x` нь `0`-ийг буцаадаг, React тоог харуулна. `count > 0 && …` гэж бич.
```

```quiz
Аль нь JSX дотор ажиллахгүй вэ?
- [x] `{if (isNew) { <b>Шинэ</b> }}`
- [ ] `{isNew && <b>Шинэ</b>}`
- [ ] `{isNew ? <b>Шинэ</b> : null}`
> JSX-ийн `{}` дотор зөвхөн илэрхийлэл бичнэ. `if` бол statement — component-ийн биед бичнэ.
```

### Дүгнэлт

Component-ийн биед `if` ба early return, JSX дотор тернар ба `&&`.
Юу ч харуулахгүй бол `null` буцаа. `&&`-ийн зүүн талд тоо биш boolean
байлга — эс бөгөөс «0» гарч ирнэ.
""",
            initial_code=vite(
                """\
import Inbox from "./Inbox";

const messages = ["Шинэ хичээл нэмэгдлээ", "Даалгавар шалгагдлаа", "Төслийн хугацаа ойртлоо"];

export default function App() {
  return (
    <main className="grid">
      <Inbox user={null} messages={[]} />
      <Inbox user={{ name: "Бат", isAdmin: false }} messages={[]} />
      <Inbox user={{ name: "Сараа", isAdmin: true }} messages={messages} />
    </main>
  );
}
""",
                extra={
                    "Inbox.jsx": """\
export default function Inbox({ user, messages }) {
  // TODO 1: user нь null бол «Мэдэгдлээ харахын тулд нэвтэрнэ үү.» гэсэн
  //         <p>-г шууд буцаа (early return).

  return (
    <section className="card">
      <h2>
        Мэдэгдэл
        {/* TODO 2: мэдэгдэл байвал л тоог нь <span className="badge">-д харуул.
            Анхаар: messages.length && … гэж бичвэл 0 гарч ирнэ! */}
      </h2>

      {/* TODO 3: мэдэгдэлгүй бол «Шинэ мэдэгдэл алга 🎉»,
          байвал «N шинэ мэдэгдэл байна.» гэж харуул (тернар). */}

      {/* TODO 4: user.isAdmin үнэн бол «Бүгдийг цэвэрлэх» товч харуул (&&). */}
    </section>
  );
}
"""
                },
                css=BASE_CSS
                + """
.badge {
  display: inline-block;
  margin-left: 8px;
  padding: 0 8px;
  border-radius: 999px;
  background: #c62828;
  color: #fff;
  font-size: 0.85rem;
}

.card button {
  margin-top: 8px;
  padding: 6px 12px;
  border: 1px solid #c62828;
  border-radius: 8px;
  background: #fff;
  color: #c62828;
}
""",
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 12 минут

`Inbox.jsx` хэрэглэгчийн мэдэгдлийг харуулдаг ч одоо ямар ч нөхцөлгүй
тул бүх тохиолдолд ижил харагдаж байна. `App.jsx` гурван өөр тохиолдлыг
зэрэг харуулдаг — TODO-г дагаж нөхцөлт render нэм: нэвтрээгүй хэрэглэгч,
мэдэгдэлгүй, мэдэгдэлтэй, админ.
""",
                tests=(
                    test(
                        "Нэвтрээгүй (user = null) үед зөвхөн нэвтрэх санал харагдана",
                        """
const Inbox = mod("./Inbox").default;
render(<Inbox user={null} messages={[]} />);
expect(screen.text()).toContain("нэвтэрнэ үү");
expect(screen.queryByRole("heading")).toBeNull();
""",
                    ),
                    test(
                        "Мэдэгдэлгүй үед «Шинэ мэдэгдэл алга» гарч, «0» харагдахгүй",
                        """
const Inbox = mod("./Inbox").default;
render(<Inbox user={{ name: "Бат", isAdmin: false }} messages={[]} />);
expect(screen.text()).toContain("Шинэ мэдэгдэл алга");
expect(screen.text()).not.toContain("0");
""",
                    ),
                    test(
                        "Мэдэгдэлтэй үед тоо нь гарчигт, «3 шинэ мэдэгдэл байна» текстэд харагдана",
                        """
const Inbox = mod("./Inbox").default;
render(<Inbox user={{ name: "Бат", isAdmin: false }} messages={["А", "Б", "В"]} />);
expect(screen.getByRole("heading")).toHaveTextContent("3");
expect(screen.text()).toContain("3 шинэ мэдэгдэл байна");
expect(screen.text()).not.toContain("Шинэ мэдэгдэл алга");
""",
                    ),
                    test(
                        "Зөвхөн админд «Бүгдийг цэвэрлэх» товч харагдана",
                        """
const Inbox = mod("./Inbox").default;
const { unmount } = render(<Inbox user={{ name: "Бат", isAdmin: false }} messages={[]} />);
expect(screen.queryByRole("button", { name: /Бүгдийг цэвэрлэх/ })).toBeNull();
unmount();
render(<Inbox user={{ name: "Сараа", isAdmin: true }} messages={[]} />);
expect(screen.getByRole("button", { name: /Бүгдийг цэвэрлэх/ })).toBeInTheDocument();
""",
                    ),
                ),
                tips="""\
- TODO 1: `if (!user) { return <p>…</p>; }` — `return (...)`-ээс **өмнө**.
  Үүний дараа `user` заавал байгаа тул `user.isAdmin`-ийг айхгүй уншина.
- TODO 2: `{messages.length > 0 && <span className="badge">…</span>}` —
  `> 0`-гүй бол мэдэгдэлгүй үед «0» гарна.
- TODO 3: `{messages.length === 0 ? (<p>…</p>) : (<p>…</p>)}`.
- TODO 4: `{user.isAdmin && <button type="button">Бүгдийг цэвэрлэх</button>}`.
""",
                solution=solution(
                    Inbox_jsx="""\
export default function Inbox({ user, messages }) {
  if (!user) {
    return <p className="card">Мэдэгдлээ харахын тулд нэвтэрнэ үү.</p>;
  }

  return (
    <section className="card">
      <h2>
        Мэдэгдэл
        {messages.length > 0 && <span className="badge">{messages.length}</span>}
      </h2>

      {messages.length === 0 ? (
        <p>Шинэ мэдэгдэл алга 🎉</p>
      ) : (
        <p>{messages.length} шинэ мэдэгдэл байна.</p>
      )}

      {user.isAdmin && <button type="button">Бүгдийг цэвэрлэх</button>}
    </section>
  );
}
"""
                ),
            ),
        ),
        # --- 5 ------------------------------------------------------------------
        LessonSpec(
            title="Жагсаалт: map",
            slug="jagsaalt-map",
            description="Массив, объектын массивыг map-аар JSX болгож, filter-ээр шүүж харуулах.",
            duration=900,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Массивыг `map`-аар JSX элементүүдийн массив болгох
- Объектын массивыг component-оор харуулах
- Эхлээд `filter`, дараа нь `map` — шүүж харуулах
- Хоосон жагсаалтын төлвийг харуулах

### Яагаад чухал вэ

Бараа, сургалт, сэтгэгдэл, мэдэгдэл — өгөгдөл бараг үргэлж **массив**
хэлбэрээр, ихэвчлэн серверээс ирдэг. Хэдэн бараа байхыг урьдчилж мэдэхгүй
тул `<li>`-г гараар бичихгүй — массиваас **үүсгэнэ**.

### JSX массивыг харуулдаг

JSX-ийн `{}` дотор элементүүдийн массив тавибал React бүгдийг дарааллаар
нь харуулна:

```jsx
const items = [<li key="a">Алим</li>, <li key="b">Банана</li>];
return <ul>{items}</ul>;
```

Гараар ингэж бичих утгагүй — Модул 0-д үзсэн `map` энэ массивыг бидний
өмнөөс үүсгэнэ:

```jsx
const fruits = ["Алим", "Банана", "Жүрж"];

function FruitList() {
  return (
    <ul>
      {fruits.map((fruit) => (
        <li key={fruit}>{fruit}</li>
      ))}
    </ul>
  );
}
```

`key`-ийн тухай дараагийн хичээлд дэлгэрэнгүй үзнэ. Одоохондоо:
`map`-аас буцаах элемент бүрт давтагдашгүй `key` өг — үгүй бол Console-д
анхааруулга гарна.

### Объектын массив

```jsx
const products = [
  { id: 1, name: "Банана", price: 3500 },
  { id: 2, name: "Алим", price: 2800 },
];

<ul>
  {products.map((product) => (
    <li key={product.id}>
      {product.name} — {product.price}₮
    </li>
  ))}
</ul>;
```

Мөр томорвол тусдаа component болго — жагсаалт нь «юу» харуулахаа, мөр нь
«яаж» харуулахаа мэднэ:

```jsx
function ProductRow({ product }) {
  return (
    <li>
      {product.name} — {product.price}₮
    </li>
  );
}

<ul>
  {products.map((product) => (
    <ProductRow key={product.id} product={product} />
  ))}
</ul>;
```

### Шүүгээд харуулах

```jsx
const cheap = products.filter((product) => product.price < 3000);

<ul>
  {cheap.map((product) => (
    <ProductRow key={product.id} product={product} />
  ))}
</ul>;
```

`filter` → `map`-ийг нэг мөрөнд гинжлэн бичиж болох ч шүүсэн үр дүнд нэр
өгвөл код илүү уншигдана.

### Хоосон жагсаалт

```jsx
if (products.length === 0) {
  return <p>Бараа олдсонгүй</p>;
}
```

Хоосон үед юу ч харуулахгүй байх нь хэрэглэгчийг «эвдэрсэн үү?» гэж
эргэлзүүлдэг — үргэлж ойлгомжтой мессеж үлдээ.

### Түгээмэл алдаа: return мартах

```jsx
{products.map((product) => {
  <li key={product.id}>{product.name}</li>; // ❌ {} биетэй — return алга
})}

{products.map((product) => (
  <li key={product.id}>{product.name}</li> // ✅ () — шууд буцаана
))}
```

Эхнийх нь `undefined`-ийн массив буцааж, юу ч харуулахгүй. `forEach` ч
мөн адил — юу ч буцаадаггүй. JSX-д үргэлж `map`.

```jsx
const names = ["Бат", "Сараа"];

<ul>
  {names.map((name) => {
    <li key={name}>{name}</li>;
  })}
</ul>;
```

```quiz
Дээрх код дэлгэцэнд юу харуулах вэ?
- [ ] «Бат», «Сараа» гэсэн хоёр мөр
- [x] Хоосон жагсаалт
- [ ] Алдаа гарна
> `{}` биетэй arrow функц `return`-гүй бол `undefined` буцаана. `(name) => (<li>…</li>)` эсвэл `return <li>…</li>;` гэж бич.
```

```quiz
Зөвхөн үлдэгдэлтэй барааг харуулах зөв код аль вэ?
- [x] `products.filter((p) => p.stock > 0).map((p) => <Card key={p.id} product={p} />)`
- [ ] `products.map((p) => <Card key={p.id} product={p} />).filter((p) => p.stock > 0)`
- [ ] `products.forEach((p) => <Card key={p.id} product={p} />)`
> Эхлээд өгөгдлийг шүүж, дараа нь JSX болгоно. JSX элементэд `stock` талбар байхгүй, `forEach` юу ч буцаадаггүй.
```

### Дүгнэлт

`{array.map((item) => <li key={item.id}>…</li>)}` — массив бүрийг JSX
болгох үндсэн хэлбэр. Шүүхдээ эхлээд `filter`, дараа нь `map`. Хоосон
жагсаалтад ойлгомжтой мессеж харуул.
""",
            initial_code=vite(
                """\
import CourseList from "./CourseList";
import { courses } from "./courses";

export default function App() {
  // TODO 3: filter ашиглаж зөвхөн level === "Анхан" сургалтуудыг ав

  return (
    <main>
      <h1>Сургалтууд</h1>

      <h2>Бүх сургалт</h2>
      <CourseList courses={courses} />

      <h2>Анхан шатны сургалтууд</h2>
      {/* TODO 4: анхан шатны сургалтуудыг CourseList-ээр харуул */}
    </main>
  );
}
""",
                extra={
                    "CourseList.jsx": """\
export default function CourseList({ courses }) {
  // TODO 1: courses хоосон бол <p>Сургалт олдсонгүй</p> буцаа
  // TODO 2: courses.map ашиглаж сургалт бүрийг <li> болго:
  //         «🎨 HTML & CSS үндэс — 60 хичээл»  (key={course.id})
  return <ul className="list"></ul>;
}
"""
                },
                locked={
                    "courses.js": """\
export const courses = [
  { id: 1, title: "HTML & CSS үндэс", level: "Анхан", lessons: 60, emoji: "🎨" },
  { id: 2, title: "JavaScript үндэс", level: "Анхан", lessons: 90, emoji: "🟨" },
  { id: 3, title: "React-ээр апп бүтээх", level: "Дунд", lessons: 111, emoji: "⚛️" },
  { id: 4, title: "Python програмчлал", level: "Анхан", lessons: 110, emoji: "🐍" },
  { id: 5, title: "SQL өгөгдлийн сан", level: "Дунд", lessons: 50, emoji: "🗄️" },
];
"""
                },
                css=BASE_CSS
                + """
.list {
  margin: 0 0 24px;
  padding: 0;
  list-style: none;
}

.list li {
  margin-bottom: 8px;
  padding: 10px 14px;
  border: 1px solid #dfe6da;
  border-radius: 10px;
  background: #fff;
}
""",
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 12 минут

`courses.js`-д таван сургалт бий. `CourseList.jsx`-д `courses` prop-ийн
сургалт бүрийг `<li>` болгож харуул (жишээ нь «🎨 HTML & CSS үндэс — 60
хичээл»), хоосон массив ирвэл «Сургалт олдсонгүй» гэж харуул. Дараа нь
`App.jsx`-д зөвхөн «Анхан» түвшний сургалтуудыг шүүж, хоёр дахь
жагсаалтаар харуул.
""",
                tests=(
                    test(
                        "CourseList нь сургалт бүрийг <li> болгон харуулна",
                        """
const CourseList = mod("./CourseList").default;
const sample = [
  { id: 1, title: "Тест А", level: "Анхан", lessons: 3, emoji: "🅰️" },
  { id: 2, title: "Тест Б", level: "Дунд", lessons: 7, emoji: "🅱️" },
];
render(<CourseList courses={sample} />);
const items = screen.getAllByRole("listitem");
expect(items).toHaveLength(2);
expect(items[0]).toHaveTextContent("Тест А");
expect(items[1]).toHaveTextContent("Тест Б");
""",
                    ),
                    test(
                        "Мөр бүрт emoji, хичээлийн тоо харагдана",
                        """
const CourseList = mod("./CourseList").default;
const sample = [
  { id: 1, title: "Тест А", level: "Анхан", lessons: 3, emoji: "🅰️" },
  { id: 2, title: "Тест Б", level: "Дунд", lessons: 7, emoji: "🅱️" },
];
render(<CourseList courses={sample} />);
const items = screen.getAllByRole("listitem");
expect(items[0]).toHaveTextContent("🅰️");
expect(items[0]).toHaveTextContent("3 хичээл");
expect(items[1]).toHaveTextContent("7 хичээл");
""",
                    ),
                    test(
                        "Хоосон массив өгвөл «Сургалт олдсонгүй» гэж харуулна",
                        """
const CourseList = mod("./CourseList").default;
render(<CourseList courses={[]} />);
expect(screen.text()).toContain("Сургалт олдсонгүй");
expect(screen.queryAllByRole("listitem")).toHaveLength(0);
""",
                    ),
                    test(
                        "App нь бүх (5) ба анхан шатны (3) сургалтын хоёр жагсаалт харуулна",
                        """
render(<App />);
const lists = screen.getAllByRole("list");
expect(lists).toHaveLength(2);
expect(within(lists[0]).getAllByRole("listitem")).toHaveLength(5);
const beginner = within(lists[1]).getAllByRole("listitem");
expect(beginner).toHaveLength(3);
const text = lists[1].textContent;
expect(text).toContain("HTML & CSS үндэс");
expect(text).toContain("Python програмчлал");
expect(text).not.toContain("SQL");
""",
                    ),
                ),
                tips="""\
- `CourseList`: хоосон эсэхийг `return`-ээс өмнө шалга —
  `if (courses.length === 0) return <p>…</p>;`
- `{courses.map((course) => (<li key={course.id}>…</li>))}` — `()` хаалттай
  arrow функц JSX-ийг шууд буцаана. `{}` хэрэглэвэл `return` заавал бич.
- Мөрийн текст: `{course.emoji} {course.title} — {course.lessons} хичээл`.
- `App`: `const beginner = courses.filter((course) => course.level === "Анхан");`
  дараа нь `<CourseList courses={beginner} />`.
""",
                solution=solution(
                    App_jsx="""\
import CourseList from "./CourseList";
import { courses } from "./courses";

export default function App() {
  const beginner = courses.filter((course) => course.level === "Анхан");

  return (
    <main>
      <h1>Сургалтууд</h1>

      <h2>Бүх сургалт</h2>
      <CourseList courses={courses} />

      <h2>Анхан шатны сургалтууд</h2>
      <CourseList courses={beginner} />
    </main>
  );
}
""",
                    CourseList_jsx="""\
export default function CourseList({ courses }) {
  if (courses.length === 0) {
    return <p>Сургалт олдсонгүй</p>;
  }

  return (
    <ul className="list">
      {courses.map((course) => (
        <li key={course.id}>
          {course.emoji} {course.title} — {course.lessons} хичээл
        </li>
      ))}
    </ul>
  );
}
""",
                ),
            ),
        ),
        # --- 6 ------------------------------------------------------------------
        LessonSpec(
            title="key",
            slug="key",
            description="Жагсаалтын мөр бүрт тогтвортой key өгч, index-ийг key болгох алдаанаас сэргийлэх.",
            duration=960,
            language=JSX,
            content="""\
### Энэ хичээлээр

- React-д `key` юунд хэрэгтэйг ойлгох
- Зөв key сонгох: давтагдашгүй, тогтвортой id
- Index-ийг key болгох нь хэзээ алдаа үүсгэдгийг өөрийн нүдээр харах
- Console дахь key анхааруулгыг уншиж засах

### Яагаад чухал вэ

Жагсаалт өөрчлөгдөхөд (мөр нэмэгдэх, устах, дараалал солигдох) React аль
мөр аль нь болохыг `key`-ээр таньдаг. Буруу key бол зүгээр нэг
анхааруулга биш — бичсэн текст өөр мөрөнд шилжих, checkbox буруу мөрөнд
үлдэх зэрэг **жинхэнэ алдаа** үүсгэнэ.

### Key юунд хэрэгтэй вэ

Өгөгдөл өөрчлөгдөхөд React шинэ JSX-ийг хуучинтай нь харьцуулж, DOM-д
зөвхөн ялгааг нь шинэчилнэ. Жагсаалтын хувьд «хуучин 2-р мөр шинэ
жагсаалтын аль нь вэ?» гэдгийг React өөрөө мэдэхгүй. `key` бол мөр бүрийн
**нэрийн хуудас**:

```jsx
<ul>
  {products.map((product) => (
    <li key={product.id}>{product.name}</li>
  ))}
</ul>
```

Key-гүй бол React мөрүүдийг **байрлалаар** (0, 1, 2…) тааруулна.
Жагсаалтын эхэнд мөр нэмэхэд бүх мөрийг «өөрчлөгдсөн» гэж үзэж, мөр доторх
төлвийг (input-д бичсэн текст, checkbox) байрлалд нь үлдээнэ.

### Анхааруулга

Key мартвал Console-д ийм мессеж гарна:

```text
Each child in a list should have a unique "key" prop.
Check the render method of `ProductList`.
```

«Жагсаалтын хүүхэд бүр давтагдашгүй key-тэй байх ёстой. `ProductList`-ийн
render-ийг шалга» — аль component-д байгааг ч хэлж байна.

### Зөв key сонгох

| Key | Зөв үү? | Яагаад |
|---|---|---|
| `product.id` | ✅ | Өгөгдлийн давтагдашгүй, тогтвортой id |
| `user.email` | ✅ | Давтагдашгүй бол ямар ч талбар болно |
| `index` | ⚠️ | Жагсаалт хэзээ ч өөрчлөгдөхгүй бол л |
| `product.name` | ⚠️ | Ижил нэртэй хоёр бараа байж болно |
| `Math.random()` | ❌ | Render бүрт өөр — React мөр бүрийг устгаад шинээр үүсгэнэ |

Дүрэм: key нь **ах дүүсийн дунд** давтагдашгүй (өөр жагсаалтад ижил key
байж болно), render бүрт **ижил** байх ёстой. Id-г өгөгдөл **үүсэх** үед
нэг удаа олгоно (сервер эсвэл нэмэх үйлдэл), render дотор биш.

### Index-ийг key болгох асуудал

```jsx
{items.map((item, index) => (
  <li key={index}>
    {item.name} <input placeholder="Тэмдэглэл" />
  </li>
))}
```

«Сүү»-ийн тэмдэглэлд «2 литр» гэж бичээд дарааллыг эргүүлбэл «2 литр»
**хуучин байрлалдаа** үлдэнэ — одоо тэнд өөр бараа байгаа. React «key=2
хэвээр, зөвхөн нэр нь өөрчлөгдсөн» гэж бодсон тул input-ийг хөдөлгөөгүй.
Даалгаврын «Хөтөч» дээр өөрөө туршиж үзээрэй.

### Key-г хаана тавих вэ

Key нь `map`-аас **шууд буцаж буй** элементэд тавигдана:

```jsx
// ❌ key дотор талын элементэд
{products.map((product) => (
  <div className="row">
    <ProductCard key={product.id} product={product} />
  </div>
))}

// ✅ гадна талын элементэд
{products.map((product) => (
  <div className="row" key={product.id}>
    <ProductCard product={product} />
  </div>
))}
```

`key` бол props биш: `ProductCard` дотор `props.key` гэж унших боломжгүй
(`undefined`). Id хэрэгтэй бол тусад нь `id={product.id}` гэж дамжуул.

Хэд хэдэн элемент буцаах бол `<>` биш, key авдаг `<Fragment key={…}>`
хэрэглэнэ:

```jsx
import { Fragment } from "react";

{terms.map((term) => (
  <Fragment key={term.id}>
    <dt>{term.word}</dt>
    <dd>{term.meaning}</dd>
  </Fragment>
))}
```

```quiz
Хийх ажлын жагсаалтад аль key хамгийн тохиромжтой вэ?
- [ ] `key={Math.random()}`
- [ ] `key={index}`
- [x] `key={todo.id}`
- [ ] Key хэрэггүй
> Id нь давтагдашгүй, render бүрт ижил. `Math.random()` render бүрт өөр тул React мөр бүрийг устгаж, шинээр үүсгэнэ.
```

```jsx
function ProductCard({ key, name }) {
  return <li data-id={key}>{name}</li>;
}
```

```quiz
Дээрх кодод юу буруу вэ?
- [x] `key` бол props биш — component дотор `undefined` байна
- [ ] `data-id` attribute ашиглаж болохгүй
- [ ] Алдаа байхгүй
> React `key`-г өөрөө ашиглаад component руу дамжуулдаггүй. `id={product.id}` гэж тусад нь дамжуул.
```

### Дүгнэлт

`key` нь React-д жагсаалтын мөрүүдийг render хооронд таних боломж олгоно.
Өгөгдлийн тогтвортой id-г `map`-аас буцах гадна талын элементэд тавь.
Index-ийг зөвхөн хэзээ ч өөрчлөгдөхгүй жагсаалтад хэрэглэ.
""",
            initial_code=files(
                (
                    "ShoppingList.jsx",
                    """\
export default function ShoppingList({ items }) {
  return (
    <ul className="list">
      {/* TODO: map-аас буцаж буй элементэд тогтвортой, давтагдашгүй key өг */}
      {items.map((item) => (
        <li>
          <label>
            <span>
              {item.emoji} {item.name}
            </span>
            <input placeholder="Тэмдэглэл" />
          </label>
        </li>
      ))}
    </ul>
  );
}
""",
                ),
                (
                    "App.jsx",
                    """\
// Энэ файл товч дарахад (onClick) жагсаалтыг өөрчлөхийн тулд useState
// ашигладаг — хоёуланг нь Модул 3-т үзнэ. Одоохондоо «товч дарахад
// жагсаалтын дараалал өөрчлөгдөнө» гэдгийг мэдэхэд хангалттай. Та зөвхөн
// ShoppingList.jsx-ийг засна — түүнд useState хэрэггүй.
import { useState } from "react";
import ShoppingList from "./ShoppingList";

const initialItems = [
  { id: 1, name: "Банана", emoji: "🍌" },
  { id: 2, name: "Алим", emoji: "🍎" },
  { id: 3, name: "Сүү", emoji: "🥛" },
  { id: 4, name: "Өндөг", emoji: "🥚" },
];

export default function App() {
  const [items, setItems] = useState(initialItems);

  return (
    <main>
      <h1>Худалдан авах жагсаалт</h1>
      <div className="row">
        <button type="button" onClick={() => setItems([...items].reverse())}>
          🔃 Дарааллыг эргүүлэх
        </button>
        <button
          type="button"
          onClick={() => setItems([{ id: Date.now(), name: "Талх", emoji: "🍞" }, ...items])}
        >
          ➕ Эхэнд «Талх» нэмэх
        </button>
      </div>
      <ShoppingList items={items} />
    </main>
  );
}
""",
                    True,
                ),
                (
                    "styles.css",
                    BASE_CSS
                    + """
.row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}

.row button {
  padding: 8px 14px;
  border: 1px solid #cfd8ca;
  border-radius: 8px;
  background: #fff;
}

.list {
  margin: 0;
  padding: 0;
  list-style: none;
}

.list li {
  margin-bottom: 8px;
  padding: 10px 14px;
  border: 1px solid #dfe6da;
  border-radius: 10px;
  background: #fff;
}

.list label {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.list input {
  padding: 6px 8px;
  border: 1px solid #cfd8ca;
  border-radius: 6px;
}
""",
                    True,
                ),
                ("main.jsx", MAIN_WITH_CSS, True),
                ("index.html", HTML, True),
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 10 минут

«Хөтөч» дээр «Сүү»-ийн тэмдэглэлд «2 литр» гэж бичээд «Дарааллыг
эргүүлэх» дар — тэмдэглэл өөр бараанд шилжинэ. Console дахь key
анхааруулгыг ч хараарай. `ShoppingList.jsx`-д зөв `key` нэмж хоёр асуудлыг
хоёуланг нь зас. Дараа нь `key={index}` гэж туршаад юу болохыг
харьцуулаарай.
""",
                tests=(
                    test(
                        "Console-д «unique key» анхааруулга гарахгүй",
                        """
render(<App />);
expect(logs.some((entry) => entry.text.includes('unique "key"'))).toBe(false);
""",
                    ),
                    test(
                        "Дараалал эргэхэд тэмдэглэл бараагаа дагаж шилжинэ",
                        """
render(<App />);
await user.type(screen.getByLabelText(/Сүү/), "2 литр");
await user.click(screen.getByRole("button", { name: /Дарааллыг эргүүлэх/ }));
expect(screen.getByLabelText(/Сүү/)).toHaveValue("2 литр");
expect(screen.getByLabelText(/Банана/)).toHaveValue("");
""",
                    ),
                    test(
                        "Эхэнд бараа нэмэхэд тэмдэглэлүүд бараагаа дагана",
                        """
render(<App />);
await user.type(screen.getByLabelText(/Банана/), "шар өнгөтэй");
await user.click(screen.getByRole("button", { name: /Талх/ }));
expect(screen.getByLabelText(/Талх/)).toHaveValue("");
expect(screen.getByLabelText(/Банана/)).toHaveValue("шар өнгөтэй");
""",
                    ),
                ),
                tips="""\
- Key нь `map`-аас **шууд** буцаж буй элементэд буюу `<li>`-д тавигдана,
  `<label>` эсвэл `<span>`-д биш.
- Бараа бүр `id`-тай — `key={item.id}`.
- `key={index}` бол анхааруулга алга болох ч дараалал солигдоход
  тэмдэглэл байрлалдаа үлдсээр байна. Яг энэ нь тестээр баригдана.
""",
                solution=solution(
                    ShoppingList_jsx="""\
export default function ShoppingList({ items }) {
  return (
    <ul className="list">
      {items.map((item) => (
        <li key={item.id}>
          <label>
            <span>
              {item.emoji} {item.name}
            </span>
            <input placeholder="Тэмдэглэл" />
          </label>
        </li>
      ))}
    </ul>
  );
}
"""
                ),
            ),
        ),
        # --- 7 ------------------------------------------------------------------
        LessonSpec(
            title="Дахин ашиглагдах component",
            slug="dahin-ashiglagdah-component",
            description="Ойлгомжтой props API-тай Button, Badge бүтээж, тусдаа файлд хуваах.",
            duration=1020,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Component-ийн props API-г төлөвлөх: `variant`, `size`, анхдагч утга
- Олон boolean prop-ийн оронд нэг утгатай prop ашиглах
- «Тохиргоо»-ноос илүү «угсралт» (composition over configuration)
- Component-уудыг `components/` хавтсанд хуваах

### Яагаад чухал вэ

Апп томрох тусам товч, шошго, карт зэрэг жижиг component-ууд хэдэн арван
газар ашиглагдана. Тэдгээрийн props ойлгомжгүй бол хүн бүр өөр өөрөөр
ашиглаж, загвар замбараагүй болно. Сайн component-ийг **харахад л хэрхэн
ашиглахыг** нь мэддэг.

### Props API төлөвлөх

Товч бодъё. Эхний санаа ихэвчлэн ийм байдаг:

```jsx
<Button blue big />
<Button red small outline />
```

`blue`, `red` хоёуланг нь өгвөл яах вэ? Boolean-ууд хоорондоо зөрчилдөж
болно. Оронд нь **утгаар** сонгуул:

```jsx
<Button variant="primary" size="lg">Хадгалах</Button>
<Button variant="danger" size="sm">Устгах</Button>
```

- `variant`: `"primary"`, `"secondary"`, `"danger"` — өнгө биш **утга
  санаа** илэрхийлнэ. `"danger"` нь «аюултай үйлдэл», өнгө нь CSS-д.
- `size`: `"sm"`, `"md"`, `"lg"`.
- Хамгийн түгээмэл хэрэглээг **анхдагч** болго: ихэнх товч `primary`, `md`.

```jsx
export default function Button({ variant = "primary", size = "md", children, ...rest }) {
  return (
    <button type="button" className={`btn btn-${variant} btn-${size}`} {...rest}>
      {children}
    </button>
  );
}
```

`children` нь товчны текст (эсвэл дүрс + текст), `...rest` нь `disabled`,
`onClick`, `aria-label` гэх мэтийг дамжуулна — `Button` жирийн `<button>`
шиг ашиглагдана. Класс нэрийг template string-ээр угсарч, загварыг CSS-д
үлдээнэ.

### Composition over configuration

Component-ийг бүх тохиолдолд тааруулах гэж олон props нэмэх нь уруу
татдаг:

```jsx
<ProductCard
  title="Банана"
  subtitle="Жимс"
  showBadge
  badgeText="Шинэ"
  showButton
  buttonText="Сагслах"
/>
```

Шинэ хэрэгцээ гарах бүрт шинэ prop нэмэгдэж, component дотроо `if`-ээр
дүүрнэ. Оронд нь жижиг component-уудыг **угсар**:

```jsx
<Card>
  <h3>
    Банана <Badge tone="green">Шинэ</Badge>
  </h3>
  <p>Жимс</p>
  <Button size="sm">Сагслах</Button>
</Card>
```

`Card` зөвхөн хүрээгээ, `Badge`, `Button` өөр өөрийн ажлыг хийнэ. Шинэ
зүйл хэрэгтэй бол `Card`-ыг өөрчлөхгүйгээр дотор нь нэмнэ.

### Файлд хуваах

Бодит Vite төсөлд дахин ашиглагдах component-уудыг тусад нь хадгалдаг:

```text
src/
├── App.jsx
├── main.jsx
└── components/
    ├── Badge.jsx
    ├── Button.jsx
    └── Card.jsx
```

```jsx
// App.jsx
import Badge from "./components/Badge";
import Button from "./components/Button";
```

Файл бүрт нэг component, файлын нэр нь component-ийн нэртэй ижил
(`Button.jsx` → `Button`). Энэ засварлагч ч хавтас дэмждэг — даалгаврын
`components/` хавтсыг хараарай.

### Бодит төсөлд

shadcn/ui, MUI, Chakra зэрэг сангуудын `Button` бараг бүгд ийм API-тай:
`variant`, `size`, `children`, үлдсэн props нь `<button>` руу. Өөрийн
component-оо ижил зарчмаар бичвэл багийнхан тань зааваргүйгээр ойлгоно.

```quiz
Товчны props API-д аль нь хамгийн тохиромжтой вэ?
- [ ] `<Button red big />`
- [x] `<Button variant="danger" size="lg" />`
- [ ] `<Button color="#d00" fontSize={20} />`
> Нэг утгатай `variant`, `size` хоорондоо зөрчилдөхгүй, өнгө, хэмжээний нарийн ширийн CSS-д үлдэнэ.
```

```quiz
`Badge` нь `badge badge-${tone}` класс өгдөг, `tone`-ийн анхдагч утга `"gray"`. `<Badge>Ноорог</Badge>` ямар класстай болох вэ?
- [x] `badge badge-gray`
- [ ] `badge badge-undefined`
- [ ] `badge`
> `tone` дамжуулаагүй буюу `undefined` тул анхдагч `"gray"` хэрэглэгдэнэ.
```

### Дүгнэлт

Сайн component-ийн props нь цөөн, утга санаатай (`variant`, `size`),
түгээмэл хэрэглээнд анхдагч утгатай байна. Олон тохиргооны props-оос
`children`-оор угсрах нь уян хатан. Дахин ашиглагдах component-уудыг
`components/` хавтсанд тус тусын файлд хадгал.
""",
            initial_code=vite(
                """\
import Badge from "./components/Badge";
import Button from "./components/Button";

export default function App() {
  return (
    <main>
      <h1>Component-ийн цуглуулга</h1>

      <section>
        <h2>Товчнууд</h2>
        <div className="row">
          <Button>Хадгалах</Button>
          <Button variant="secondary">Цуцлах</Button>
          <Button variant="danger" size="sm">
            Устгах
          </Button>
          <Button size="lg">Том товч</Button>
          <Button disabled>Идэвхгүй</Button>
        </div>
      </section>

      <section>
        <h2>Шошго</h2>
        <div className="row">
          <Badge tone="green">Шинэ</Badge>
          <Badge tone="red">Дууссан</Badge>
          <Badge>Ноорог</Badge>
        </div>
      </section>

      <section className="card product">
        <h2>
          🍌 Банана <Badge tone="green">Шинэ</Badge>
        </h2>
        <p>3,500₮</p>
        <Button size="sm">Сагсанд нэмэх</Button>
      </section>
    </main>
  );
}
""",
                extra={
                    "components/Button.jsx": """\
// TODO: props-оо задал: variant (анхдагч "primary"), size (анхдагч "md"),
//       children, ...rest
// TODO: className нь "btn btn-<variant> btn-<size>" байна,
//       ...rest-ийг <button> руу дамжуул.
export default function Button(props) {
  return <button type="button">{props.children}</button>;
}
""",
                    "components/Badge.jsx": """\
// TODO: props-оо задал: tone (анхдагч "gray"), children
// TODO: className нь "badge badge-<tone>" байна.
export default function Badge(props) {
  return <span>{props.children}</span>;
}
""",
                },
                css=BASE_CSS
                + """
section {
  margin-bottom: 24px;
}

.row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 10px;
}

.btn {
  border: 1px solid transparent;
  border-radius: 8px;
}

.btn-sm {
  padding: 4px 10px;
  font-size: 0.85rem;
}

.btn-md {
  padding: 8px 16px;
}

.btn-lg {
  padding: 12px 22px;
  font-size: 1.15rem;
}

.btn-primary {
  background: #2f6b1f;
  color: #fff;
}

.btn-secondary {
  border-color: #b9c6b2;
  background: #fff;
  color: #1f2a1c;
}

.btn-danger {
  background: #c62828;
  color: #fff;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.badge {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 999px;
  font-size: 0.8rem;
  font-weight: 600;
  vertical-align: middle;
}

.badge-green {
  background: #dcefd3;
  color: #2f6b1f;
}

.badge-red {
  background: #fde2e1;
  color: #a3261f;
}

.badge-gray {
  background: #eceeea;
  color: #55624f;
}

.product {
  max-width: 280px;
}
""",
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 12 минут

`components/` хавтсан дахь `Button`, `Badge`-ийг дахин ашиглагдахуйц
болго. `Button` нь `variant`, `size` props-оос `btn btn-<variant>
btn-<size>` класс үүсгэж, бусад props-ийг `<button>` руу дамжуулна.
`Badge` нь `tone` prop-оос `badge badge-<tone>` класс авна. CSS бэлэн —
`App.jsx` дахь загварууд «Хөтөч» дээр гарч ирэх ёстой.
""",
                tests=(
                    test(
                        "Button нь анхдагчаар btn, btn-primary, btn-md класстай",
                        """
const Button = mod("./components/Button").default;
render(<Button>Хадгалах</Button>);
expect(screen.getByRole("button", { name: "Хадгалах" })).toHaveClass("btn", "btn-primary", "btn-md");
""",
                    ),
                    test(
                        "variant, size props-оор класс солигдоно",
                        """
const Button = mod("./components/Button").default;
render(
  <Button variant="danger" size="sm">
    Устгах
  </Button>
);
const button = screen.getByRole("button", { name: "Устгах" });
expect(button).toHaveClass("btn", "btn-danger", "btn-sm");
expect(button).not.toHaveClass("btn-primary");
expect(button).not.toHaveClass("btn-md");
""",
                    ),
                    test(
                        "Button нь бусад props-ийг <button> руу дамжуулна",
                        """
const Button = mod("./components/Button").default;
render(
  <Button disabled aria-label="Захиалга илгээх">
    Илгээх
  </Button>
);
expect(screen.getByRole("button", { name: "Захиалга илгээх" })).toBeDisabled();
""",
                    ),
                    test(
                        "Badge нь badge, badge-<tone> класстай, анхдагч tone нь gray",
                        """
const Badge = mod("./components/Badge").default;
render(
  <div>
    <Badge tone="green">Шинэ</Badge>
    <Badge>Ноорог</Badge>
  </div>
);
expect(screen.getByText("Шинэ")).toHaveClass("badge", "badge-green");
expect(screen.getByText("Ноорог")).toHaveClass("badge", "badge-gray");
""",
                    ),
                ),
                tips="""\
- `function Button({ variant = "primary", size = "md", children, ...rest })`.
- Класс нэрийг template string-ээр угсар:
  `` className={`btn btn-${variant} btn-${size}`} ``.
- `{...rest}`-ийг `<button>`-д тавь — `disabled`, `aria-label`, `onClick`
  бүгд тэгж дамжина.
- `Badge` ч ижил зарчмаар: `` className={`badge badge-${tone}`} ``.
""",
                solution=files(
                    (
                        "components/Button.jsx",
                        """\
export default function Button({ variant = "primary", size = "md", children, ...rest }) {
  return (
    <button type="button" className={`btn btn-${variant} btn-${size}`} {...rest}>
      {children}
    </button>
  );
}
""",
                    ),
                    (
                        "components/Badge.jsx",
                        """\
export default function Badge({ tone = "gray", children }) {
  return <span className={`badge badge-${tone}`}>{children}</span>;
}
""",
                    ),
                ),
            ),
        ),
        # --- 8 ------------------------------------------------------------------
        LessonSpec(
            title="Төсөл: Барааны каталог",
            slug="tusul-baraany-katalog",
            description="Props, жагсаалт, нөхцөлт render-ээр олон файлтай барааны каталог бүтээх.",
            duration=2400,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Модул 2-т сурсан бүхнээ нэг апп-д нэгтгэх
- UI-г component-уудын мод болгон задлах
- Олон файлтай төслийг алхам алхмаар угсрах

### Яагаад чухал вэ

Бодит апп-ыг нэг дор бичдэггүй: эхлээд дизайныг component-ууд болгон
хуваагаад, жижгээс нь эхэлж бүтээнэ. Энэ төсөл бол сургалтын төгсгөлд
бүтээх «Ногоон сагс» дэлгүүрийн анхны хувилбар — дараагийн модулиудад
түүнд сагс, хайлт, серверийн өгөгдөл нэмнэ.

### Юу бүтээх вэ

«Ногоон сагс»-ын барааны каталог:

- **Толгой хэсэг:** дэлгүүрийн нэр, барааны тоо («8 бараа»).
- **Барааны тор (grid):** карт бүрт emoji, нэр, ангилал, үнэ (`3,500₮`),
  үлдэгдэл. Дууссан бараанд **«Дууссан»** шошго.
- **Доод хэсэг (footer):** «© 2026 Ногоон сагс».

### Component-уудын мод

```text
App
├── Header          ← дэлгүүрийн нэр, барааны тоо
├── ProductList     ← products.map(...)
│   ├── ProductCard
│   ├── ProductCard
│   └── ProductCard …
└── Footer
```

Өгөгдөл дээрээс доош props-оор урсана: `App` нь `products`-ийг импортлоод
`ProductList`-д, `ProductList` нь бараа бүрийг `ProductCard`-д өгнө.
`Header` зөвхөн тоог нь авна — бүх барааг мэдэх шаардлагагүй.

### Файлын бүтэц

```text
App.jsx
products.js 🔒      ← 8 барааны өгөгдөл
format.js           ← formatPrice()
styles.css          ← тор, картын загвар (бэлэн)
components/
├── Header.jsx
├── ProductList.jsx
├── ProductCard.jsx
└── Footer.jsx
```

Файл бүрт TODO бий. Доорх дарааллаар ажиллавал алхам бүрийн дараа
«Хөтөч» дээр ахиц харагдана.

### Алхам 1 — Үнийг форматлах

`format.js` дахь `formatPrice(price)` нь `3500`-г `"3,500₮"` болгоно.
`toLocaleString` тоог мянгатаар нь таслалаар хуваана:

```jsx
(12500).toLocaleString("en-US"); // "12,500"
```

Ард нь `"₮"`-г залгана. Ийм жижиг **цэвэр функцийг** component-оос тусад
нь бичвэл хаана ч дахин ашиглаж, тестлэхэд амар.

### Алхам 2 — ProductCard

`product` prop-оос талбаруудаа задалж харуул:

```jsx
export default function ProductCard({ product }) {
  const { name, emoji, category, price, stock } = product;
  return <li className="card">{/* … */}</li>;
}
```

- `<div className="card-emoji">`-д emoji, `<h2>`-д нэр.
- `<p className="category">`-д ангилал, `<p className="price">`-д
  `formatPrice(price)`.
- `stock === 0` бол `<span className="badge sold-out">Дууссан</span>`,
  эс бөгөөс `<p className="stock">Үлдэгдэл: 24</p>` (тернар).

### Алхам 3 — ProductList

`<ul className="grid">` дотор `products.map(...)`-ээр бараа бүрт
`<ProductCard … />` үүсгэ. Key-г `ProductCard`-д тавина уу, эсвэл
`ProductCard` доторх `<li>`-д үү? `map`-аас **шууд** буцаж буй элемент нь
`<ProductCard>` — key тэнд.

### Алхам 4 — Header ба Footer

- `Header` нь `count` prop авч, гарчгийн доор `<p>{count} бараа</p>`
  харуулна. Гадна элемент нь `<header>`.
- `Footer` нь `<footer className="footer">© 2026 Ногоон сагс</footer>`
  буцаана.

### Алхам 5 — App-д угсрах

```jsx
<div className="page">
  <Header count={products.length} />
  <ProductList products={products} />
  <Footer />
</div>
```

Барааны тоог `products.length`-ээс ав. Гараар «8» гэж бичвэл бараа
нэмэгдэхэд дэлгэц өгөгдлөөсөө зөрнө.

### Шалгах

«Ажиллуулах» дарахаас өмнө «Хөтөч» дээр:

- 8 карт тор болж харагдаж байна уу? Цонхыг нарийсгахад багана цөөрч байна уу?
- «Брокколи», «Бяслаг» дээр «Дууссан» шошго байна уу?
- Console-д `key`-ийн анхааруулга алга уу?

### Нэмэлт сорилт

Тест шаардахгүй ч оролдоод үзээрэй:

- 3,000₮-өөс хямд бараанд `Badge`-тэй адил «Хямд» шошго нэм.
- `ProductList`-д `title` prop нэмж, «Жимс», «Ногоо»-г тус тусад нь
  (`filter`) харуул.

```quiz
`Header`-т барааны тоог дамжуулах хамгийн зөв арга аль вэ?
- [ ] `<Header count="8" />`
- [x] `<Header count={products.length} />`
- [ ] `Header` дотор `products`-ийг дахин импортлож тоолох
> Тоо өгөгдлөөс гарах ёстой — бараа нэмэгдэхэд автоматаар шинэчлэгдэнэ. Импортлох нь ажиллах ч `Header`-ийг тодорхой өгөгдөлтэй холбож, дахин ашиглах боломжийг хаана.
```

```quiz
`ProductList` дотор `products.map((p) => <ProductCard product={p} />)` гэж бичсэн. Key-г хаана тавих вэ?
- [x] `<ProductCard key={p.id} product={p} />`
- [ ] `ProductCard` доторх `<li key={product.id}>`
- [ ] `<ul key="grid">`
> Key нь `map`-аас шууд буцаж буй элементэд тавигдана. `ProductCard` доторх `<li>` жагсаалтын «хүүхэд» биш.
```

### Дүгнэлт

Том UI-г component-уудын мод болгон задалж, өгөгдлийг props-оор доош
дамжуулсан. `map` ба `key`-ээр жагсаалт, тернараар «Дууссан» шошго,
тусдаа файлд цэвэр функц. Дараагийн модульд энэ каталогт state нэмж
сагстай болгоно.
""",
            initial_code=vite(
                CATALOG_APP_START,
                extra={
                    "format.js": CATALOG_FORMAT_START,
                    "components/Header.jsx": CATALOG_HEADER_START,
                    "components/ProductList.jsx": CATALOG_LIST_START,
                    "components/ProductCard.jsx": CATALOG_CARD_START,
                    "components/Footer.jsx": CATALOG_FOOTER_START,
                },
                locked={"products.js": CATALOG_PRODUCTS},
                css=CATALOG_CSS,
                css_locked=False,
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐ · 35 минут

«Заавар» дахь алхмуудыг дагаж «Ногоон сагс»-ын барааны каталогийг угсар.
Файл бүрт TODO бий; `products.js`-ийг өөрчлөх шаардлагагүй. `styles.css`
торыг бэлдчихсэн — хүсвэл өөрийнхөөрөө чимэглээрэй.
""",
                tests=(
                    test(
                        "formatPrice нь үнийг мянгатын таслалтай, ₮ тэмдэгтэй болгоно",
                        """
const { formatPrice } = mod("./format");
expect(formatPrice(3500)).toBe("3,500₮");
expect(formatPrice(12500)).toBe("12,500₮");
expect(formatPrice(900)).toBe("900₮");
""",
                    ),
                    test(
                        "ProductCard нь emoji, нэр, ангилал, үнийг харуулна",
                        """
const ProductCard = mod("./components/ProductCard").default;
render(
  <ul>
    <ProductCard product={{ id: 1, name: "Банана", price: 3500, category: "Жимс", emoji: "🍌", stock: 24 }} />
  </ul>
);
expect(screen.getByRole("heading", { name: "Банана" })).toBeInTheDocument();
const text = screen.text();
expect(text).toContain("🍌");
expect(text).toContain("Жимс");
expect(text).toContain("3,500₮");
""",
                    ),
                    test(
                        "Үлдэгдэл 0 бол «Дууссан» шошго харагдана, бусад үед харагдахгүй",
                        """
const ProductCard = mod("./components/ProductCard").default;
const soldOut = render(
  <ul>
    <ProductCard product={{ id: 5, name: "Брокколи", price: 5200, category: "Ногоо", emoji: "🥦", stock: 0 }} />
  </ul>
).container;
const inStock = render(
  <ul>
    <ProductCard product={{ id: 4, name: "Лууван", price: 1900, category: "Ногоо", emoji: "🥕", stock: 30 }} />
  </ul>
).container;
expect(within(soldOut).text()).toContain("Дууссан");
expect(within(inStock).text()).not.toContain("Дууссан");
""",
                    ),
                    test(
                        "App нь бүх 8 барааг key-тэй жагсаалтаар харуулна",
                        """
render(<App />);
expect(screen.getAllByRole("listitem")).toHaveLength(8);
for (const name of ["Банана", "Брокколи", "Бяслаг", "Талх"]) {
  expect(screen.getByRole("heading", { name })).toBeInTheDocument();
}
expect(logs.some((entry) => entry.text.includes('unique "key"'))).toBe(false);
""",
                    ),
                    test(
                        "Header-т барааны тоо, footer-т дэлгүүрийн нэр харагдана",
                        """
render(<App />);
expect(screen.getByRole("banner")).toHaveTextContent("8 бараа");
expect(screen.getByRole("contentinfo")).toHaveTextContent("Ногоон сагс");
""",
                    ),
                ),
                tips="""\
- `formatPrice`: `return price.toLocaleString("en-US") + "₮";`
- `ProductCard`: `const { name, emoji, category, price, stock } = product;`
  дараа нь `{stock === 0 ? (<span …>Дууссан</span>) : (<p …>Үлдэгдэл: {stock}</p>)}`.
- `ProductList`: `{products.map((product) => (<ProductCard key={product.id} product={product} />))}`
  — `()` хаалттай arrow функц, `key` нь `ProductCard` дээр.
- `Header`: `<p>{count} бараа</p>`; `Footer`: `null`-ийн оронд `<footer>` буцаа.
- `App`: `Header`, `ProductList`, `Footer`-ийг `.page` дотор угсар, тоог
  `products.length`-ээс ав.
""",
                solution=files(
                    (
                        "App.jsx",
                        """\
import Footer from "./components/Footer";
import Header from "./components/Header";
import ProductList from "./components/ProductList";
import { products } from "./products";

export default function App() {
  return (
    <div className="page">
      <Header count={products.length} />
      <ProductList products={products} />
      <Footer />
    </div>
  );
}
""",
                    ),
                    (
                        "format.js",
                        """\
export function formatPrice(price) {
  return price.toLocaleString("en-US") + "₮";
}
""",
                    ),
                    (
                        "components/Header.jsx",
                        """\
export default function Header({ count }) {
  return (
    <header className="header">
      <h1>🥬 Ногоон сагс</h1>
      <p>{count} бараа</p>
    </header>
  );
}
""",
                    ),
                    (
                        "components/ProductList.jsx",
                        """\
import ProductCard from "./ProductCard";

export default function ProductList({ products }) {
  return (
    <ul className="grid">
      {products.map((product) => (
        <ProductCard key={product.id} product={product} />
      ))}
    </ul>
  );
}
""",
                    ),
                    (
                        "components/ProductCard.jsx",
                        """\
import { formatPrice } from "../format";

export default function ProductCard({ product }) {
  const { name, emoji, category, price, stock } = product;

  return (
    <li className="card">
      <div className="card-emoji">{emoji}</div>
      <h2>{name}</h2>
      <p className="category">{category}</p>
      <p className="price">{formatPrice(price)}</p>
      {stock === 0 ? (
        <span className="badge sold-out">Дууссан</span>
      ) : (
        <p className="stock">Үлдэгдэл: {stock}</p>
      )}
    </li>
  );
}
""",
                    ),
                    (
                        "components/Footer.jsx",
                        """\
export default function Footer() {
  return <footer className="footer">© 2026 Ногоон сагс</footer>;
}
""",
                    ),
                ),
            ),
        ),
    ],
)
