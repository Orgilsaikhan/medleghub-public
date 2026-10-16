"""Модул 12 — Гүйцэтгэл.

Шаардлагагүй render-ийг хэмжиж илрүүлээд, state-ийг доош зөөх, `memo`,
`useMemo`, `useCallback`, code splitting, урт жагсаалтын аргуудаар аппыг
хурдасгана. Sandbox-д StrictMode байхгүй тул component доторх `console.log`
нь render-ийг яг тоолно — тестүүд `logs`-оос тоолж шалгана.
"""

from app.content.react.common import files, solution, test, vite
from app.content.types import ExerciseSpec, LessonSpec, ModuleSpec
from app.models.enums import LessonLanguage

JSX = LessonLanguage.JSX

SLOW_JS = """\
// Хүнд тооцоог дуурайна: ms миллисекунд процессорыг завгүй байлгана.
export function slowDown(ms) {
  const start = performance.now();
  while (performance.now() - start < ms) {
    // зориуд хоосон давталт
  }
}
"""

# --- 1. render-hemjih ---------------------------------------------------------------

MEASURE_PRODUCT_LIST = """\
import { slowDown } from "./slow";

const products = [
  { id: 1, name: "Банана", price: 3500, emoji: "🍌" },
  { id: 2, name: "Алим", price: 2800, emoji: "🍎" },
  { id: 3, name: "Жүрж", price: 4200, emoji: "🍊" },
  { id: 4, name: "Сүү", price: 3200, emoji: "🥛" },
  { id: 5, name: "Талх", price: 2500, emoji: "🍞" },
];

// «Удаан» component: бодит аппад 500 мөртэй хүснэгт, график гэх мэт.
export default function ProductList() {
  console.log("render: ProductList");
  slowDown(5);

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

MEASURE_APP = """\
import { Profiler, useState } from "react";
import ProductList from "./ProductList";

// TODO 1: onRender функц бичиж, ProductList-ийг
//         <Profiler id="ProductList" onRender={onRender}>-оор орооно.
// TODO 2: Санал хүсэлтийн талбар, түүний state-ийг тусдаа FeedbackBox
//         component руу зөөнө.

export default function App() {
  const [feedback, setFeedback] = useState("");

  return (
    <main>
      <h1>Ногоон сагс</h1>
      <label>
        Санал хүсэлт{" "}
        <input value={feedback} onChange={(e) => setFeedback(e.target.value)} />
      </label>
      <p>{feedback.length} тэмдэгт</p>
      <ProductList />
    </main>
  );
}
"""

MEASURE_SOLUTION = """\
import { Profiler, useState } from "react";
import ProductList from "./ProductList";

function onRender(id, phase, actualDuration) {
  console.log(`${id} ${phase} ${actualDuration.toFixed(1)}ms`);
}

function FeedbackBox() {
  const [feedback, setFeedback] = useState("");

  return (
    <section>
      <label>
        Санал хүсэлт{" "}
        <input value={feedback} onChange={(e) => setFeedback(e.target.value)} />
      </label>
      <p>{feedback.length} тэмдэгт</p>
    </section>
  );
}

export default function App() {
  return (
    <main>
      <h1>Ногоон сагс</h1>
      <FeedbackBox />
      <Profiler id="ProductList" onRender={onRender}>
        <ProductList />
      </Profiler>
    </main>
  );
}
"""

# --- 2. memo ------------------------------------------------------------------------

MEMO_APP = """\
import { useState } from "react";
import ProductCard from "./ProductCard";

const initialProducts = [
  { id: 1, name: "Банана", price: 3500, emoji: "🍌" },
  { id: 2, name: "Алим", price: 2800, emoji: "🍎" },
  { id: 3, name: "Жүрж", price: 4200, emoji: "🍊" },
  { id: 4, name: "Сүү", price: 3200, emoji: "🥛" },
];

export default function App() {
  const [dark, setDark] = useState(false);
  const [products, setProducts] = useState(initialProducts);

  function discountBanana() {
    setProducts(products.map((p) => (p.id === 1 ? { ...p, price: p.price - 500 } : p)));
  }

  return (
    <main
      style={{
        padding: 16,
        background: dark ? "#1f2937" : "#ffffff",
        color: dark ? "#f9fafb" : "#111827",
      }}
    >
      <button onClick={() => setDark(!dark)}>Горим солих</button>{" "}
      <button onClick={discountBanana}>Бананыг хямдруулах</button>
      <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginTop: 12 }}>
        {products.map((p) => (
          <ProductCard key={p.id} name={p.name} price={p.price} emoji={p.emoji} />
        ))}
      </div>
    </main>
  );
}
"""

MEMO_CARD = """\
// TODO: ProductCard-ийг memo-оор ороож экспортло.

export default function ProductCard({ name, price, emoji }) {
  console.log(`render: ${name}`);

  return (
    <article style={{ minWidth: 120, padding: 12, border: "1px solid #d1d5db", borderRadius: 8 }}>
      <div style={{ fontSize: 32 }}>{emoji}</div>
      <h2 style={{ margin: "4px 0", fontSize: 16 }}>{name}</h2>
      <p style={{ margin: 0 }}>{price}₮</p>
    </article>
  );
}
"""

MEMO_CARD_SOLUTION = """\
import { memo } from "react";

function ProductCard({ name, price, emoji }) {
  console.log(`render: ${name}`);

  return (
    <article style={{ minWidth: 120, padding: 12, border: "1px solid #d1d5db", borderRadius: 8 }}>
      <div style={{ fontSize: 32 }}>{emoji}</div>
      <h2 style={{ margin: "4px 0", fontSize: 16 }}>{name}</h2>
      <p style={{ margin: 0 }}>{price}₮</p>
    </article>
  );
}

export default memo(ProductCard);
"""

COUNT_RENDERS = 'const count = (name) => logs.filter((l) => l.text === "render: " + name).length;'

# --- 3. memo-hamt -------------------------------------------------------------------

TOGETHER_DATA = """\
export const products = [
  { id: 1, name: "Банана", price: 3500, emoji: "🍌" },
  { id: 2, name: "Алим", price: 2800, emoji: "🍎" },
  { id: 3, name: "Жүрж", price: 4200, emoji: "🍊" },
  { id: 4, name: "Лууван", price: 1900, emoji: "🥕" },
  { id: 5, name: "Төмс", price: 1500, emoji: "🥔" },
  { id: 6, name: "Сүү", price: 3200, emoji: "🥛" },
];
"""

TOGETHER_LIST = """\
import { memo } from "react";

function ProductList({ products, onAdd }) {
  console.log("render: ProductList");

  return (
    <ul>
      {products.map((product) => (
        <li key={product.id}>
          {product.emoji} {product.name} — {product.price}₮{" "}
          <button onClick={() => onAdd(product.id)}>Нэмэх</button>
        </li>
      ))}
    </ul>
  );
}

// memo аль хэдийн байгаа — гэвч App-аас ирэх props тогтвортой биш.
export default memo(ProductList);
"""

TOGETHER_APP = """\
import { useState } from "react";
import { products } from "./data";
import ProductList from "./ProductList";

export default function App() {
  const [query, setQuery] = useState("");
  const [dark, setDark] = useState(false);
  const [cart, setCart] = useState([]);

  // TODO: Доорх хоёр утга render бүрт ШИНЭ болж, ProductList-ийн memo-г эвдэж байна.
  const visible = products.filter((p) => p.name.toLowerCase().includes(query.toLowerCase()));

  function handleAdd(id) {
    setCart([...cart, id]);
  }

  return (
    <main style={{ padding: 16, background: dark ? "#1f2937" : "#ffffff", color: dark ? "#f9fafb" : "#111827" }}>
      <header>
        <h1>Дэлгүүр</h1>
        <p>Сагс: {cart.length}</p>
        <button onClick={() => setDark(!dark)}>Горим солих</button>
      </header>
      <label>
        Хайх <input value={query} onChange={(e) => setQuery(e.target.value)} />
      </label>
      <ProductList products={visible} onAdd={handleAdd} />
    </main>
  );
}
"""

TOGETHER_SOLUTION = """\
import { useCallback, useMemo, useState } from "react";
import { products } from "./data";
import ProductList from "./ProductList";

export default function App() {
  const [query, setQuery] = useState("");
  const [dark, setDark] = useState(false);
  const [cart, setCart] = useState([]);

  const visible = useMemo(
    () => products.filter((p) => p.name.toLowerCase().includes(query.toLowerCase())),
    [query],
  );

  const handleAdd = useCallback((id) => {
    setCart((current) => [...current, id]);
  }, []);

  return (
    <main style={{ padding: 16, background: dark ? "#1f2937" : "#ffffff", color: dark ? "#f9fafb" : "#111827" }}>
      <header>
        <h1>Дэлгүүр</h1>
        <p>Сагс: {cart.length}</p>
        <button onClick={() => setDark(!dark)}>Горим солих</button>
      </header>
      <label>
        Хайх <input value={query} onChange={(e) => setQuery(e.target.value)} />
      </label>
      <ProductList products={visible} onAdd={handleAdd} />
    </main>
  );
}
"""

# --- 4. code-splitting --------------------------------------------------------------

SPLIT_REPORTS = """\
// «Хүнд» модуль: бодит төсөлд график, хүснэгтийн сан (~300 KB) импортолдог.
console.log("📦 Reports модуль ачааллаа");

const sales = [
  { month: "1-р сар", total: 1250000 },
  { month: "2-р сар", total: 980000 },
  { month: "3-р сар", total: 1540000 },
];

export default function Reports() {
  return (
    <section>
      <h2>Борлуулалтын тайлан</h2>
      <ul>
        {sales.map((row) => (
          <li key={row.month}>
            {row.month}: {row.total.toLocaleString("en-US")}₮
          </li>
        ))}
      </ul>
    </section>
  );
}
"""

SPLIT_HELP = """\
console.log("📦 Help модуль ачааллаа");

export default function Help() {
  return (
    <section>
      <h2>Тусламж</h2>
      <p>Асуулт байвал info@medleghub.com хаягаар бичээрэй.</p>
    </section>
  );
}
"""

SPLIT_NETWORK = """\
// Sandbox-д import() шууд биелдэг. Сүлжээгээр файл татаж буйг дуурайхын тулд
// хүлээлт нэмнэ. Бодит төсөлд зүгээр л: lazy(() => import("./Reports"))
export function withDelay(load, ms = 600) {
  return new Promise((resolve) => setTimeout(resolve, ms)).then(load);
}
"""

SPLIT_APP = """\
import { lazy, Suspense, useState } from "react";
import { withDelay } from "./network";
// TODO: Reports-ийг Help шиг lazy болго — энэ static import-ийг устга.
import Reports from "./Reports";

// Жишээ: Help нь «Тусламж» дарах үед л татагдана.
const Help = lazy(() => withDelay(() => import("./Help")));

export default function App() {
  const [tab, setTab] = useState("home");

  return (
    <main>
      <nav>
        <button onClick={() => setTab("home")}>Нүүр</button>{" "}
        <button onClick={() => setTab("reports")}>Тайлан</button>{" "}
        <button onClick={() => setTab("help")}>Тусламж</button>
      </nav>
      {tab === "home" && <h2>Тавтай морил!</h2>}
      {tab === "reports" && <Reports />}
      <Suspense fallback={<p>Ачаалж байна…</p>}>{tab === "help" && <Help />}</Suspense>
    </main>
  );
}
"""

SPLIT_SOLUTION = """\
import { lazy, Suspense, useState } from "react";
import { withDelay } from "./network";

const Help = lazy(() => withDelay(() => import("./Help")));
const Reports = lazy(() => withDelay(() => import("./Reports")));

export default function App() {
  const [tab, setTab] = useState("home");

  return (
    <main>
      <nav>
        <button onClick={() => setTab("home")}>Нүүр</button>{" "}
        <button onClick={() => setTab("reports")}>Тайлан</button>{" "}
        <button onClick={() => setTab("help")}>Тусламж</button>
      </nav>
      {tab === "home" && <h2>Тавтай морил!</h2>}
      <Suspense fallback={<p>Ачаалж байна…</p>}>
        {tab === "reports" && <Reports />}
        {tab === "help" && <Help />}
      </Suspense>
    </main>
  );
}
"""

# --- 5. urt-jagsaalt ----------------------------------------------------------------

LIST_DATA = """\
// 1000 захиалга — бодит аппад серверээс ирнэ.
export const orders = Array.from({ length: 1000 }, (_, index) => ({
  id: index + 1,
  title: `Захиалга #${index + 1}`,
  total: (((index * 7919) % 90) + 10) * 1000,
}));
"""

LIST_APP = """\
import { orders } from "./data";

const PAGE_SIZE = 20;

export default function App() {
  // TODO: page state нэмж, зөвхөн тухайн хуудасны PAGE_SIZE захиалгыг харуул.
  //       Доор нь «Өмнөх», «Хуудас 1 / 50», «Дараах».

  return (
    <main>
      <h1>Захиалгууд ({orders.length})</h1>
      <ul>
        {orders.map((order) => (
          <li key={order.id}>
            {order.title} — {order.total.toLocaleString("en-US")}₮
          </li>
        ))}
      </ul>
    </main>
  );
}
"""

LIST_SOLUTION = """\
import { useState } from "react";
import { orders } from "./data";

const PAGE_SIZE = 20;

export default function App() {
  const [page, setPage] = useState(1);
  const pageCount = Math.ceil(orders.length / PAGE_SIZE);
  const visible = orders.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE);

  return (
    <main>
      <h1>Захиалгууд ({orders.length})</h1>
      <ul>
        {visible.map((order) => (
          <li key={order.id}>
            {order.title} — {order.total.toLocaleString("en-US")}₮
          </li>
        ))}
      </ul>
      <nav>
        <button onClick={() => setPage(page - 1)} disabled={page === 1}>
          Өмнөх
        </button>{" "}
        <span>
          Хуудас {page} / {pageCount}
        </span>{" "}
        <button onClick={() => setPage(page + 1)} disabled={page === pageCount}>
          Дараах
        </button>
      </nav>
    </main>
  );
}
"""

# --- 6. tusul-hurdasgah -------------------------------------------------------------

PROJECT_DATA = """\
const base = [
  { name: "Банана", price: 3500, emoji: "🍌" },
  { name: "Алим", price: 2800, emoji: "🍎" },
  { name: "Жүрж", price: 4200, emoji: "🍊" },
  { name: "Лууван", price: 1900, emoji: "🥕" },
  { name: "Төмс", price: 1500, emoji: "🥔" },
  { name: "Брокколи", price: 5200, emoji: "🥦" },
  { name: "Сүү", price: 3200, emoji: "🥛" },
  { name: "Бяслаг", price: 12500, emoji: "🧀" },
  { name: "Талх", price: 2500, emoji: "🍞" },
  { name: "Өндөг", price: 6500, emoji: "🥚" },
];

// 200 бараа: «Банана 1», «Алим 1», … «Өндөг 20».
export const products = Array.from({ length: 200 }, (_, index) => {
  const item = base[index % base.length];
  const batch = Math.floor(index / base.length) + 1;
  return {
    id: index + 1,
    name: `${item.name} ${batch}`,
    price: item.price + batch * 100,
    emoji: item.emoji,
    stock: (index * 7) % 50,
  };
});
"""

PROJECT_STATS = """\
import { slowDown } from "./slow";

// Хүнд тооцоо — бодит аппад олон мянган мөрийн статистик.
export function computeStats(products) {
  console.log("computeStats");
  slowDown(15);
  const totalPrice = products.reduce((sum, p) => sum + p.price, 0);
  return {
    count: products.length,
    avgPrice: Math.round(totalPrice / products.length),
    totalStock: products.reduce((sum, p) => sum + p.stock, 0),
  };
}
"""

PROJECT_TABLE = """\
import { slowDown } from "./slow";

export default function ProductTable({ products, favorites, onToggle }) {
  console.log("render: ProductTable");
  slowDown(10);

  return (
    <table>
      <thead>
        <tr>
          <th>Бараа</th>
          <th>Үнэ</th>
          <th>Дуртай</th>
        </tr>
      </thead>
      <tbody>
        {products.map((product) => (
          <tr key={product.id}>
            <td>
              {product.emoji} {product.name}
            </td>
            <td>{product.price}₮</td>
            <td>
              <button onClick={() => onToggle(product.id)} aria-label={`${product.name} — дуртай`}>
                {favorites.includes(product.id) ? "★" : "☆"}
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
"""

_TABLE_HEAD = 'import { slowDown } from "./slow";\n\nexport default function ProductTable('
assert PROJECT_TABLE.count(_TABLE_HEAD) == 1
PROJECT_TABLE_SOLUTION = (
    PROJECT_TABLE.replace(
        _TABLE_HEAD,
        'import { memo } from "react";\nimport { slowDown } from "./slow";\n\nfunction ProductTable(',
    )
    + "\nexport default memo(ProductTable);\n"
)

PROJECT_APP = """\
import { Profiler, useState } from "react";
import { products } from "./data";
import ProductTable from "./ProductTable";
import { computeStats } from "./stats";

function onRender(id, phase, actualDuration) {
  console.log(`⏱ ${id} ${phase}: ${actualDuration.toFixed(1)}ms`);
}

export default function App() {
  const [query, setQuery] = useState("");
  const [note, setNote] = useState("");
  const [favorites, setFavorites] = useState([]);

  const stats = computeStats(products);
  const visible = products.filter((p) => p.name.toLowerCase().includes(query.toLowerCase()));

  function toggleFavorite(id) {
    setFavorites(favorites.includes(id) ? favorites.filter((f) => f !== id) : [...favorites, id]);
  }

  return (
    <main>
      <h1>Барааны самбар</h1>
      <p>
        Нийт {stats.count} бараа · Дундаж үнэ {stats.avgPrice}₮ · Үлдэгдэл {stats.totalStock} ·
        Дуртай: {favorites.length}
      </p>
      <p>
        <label>
          Хайх <input value={query} onChange={(e) => setQuery(e.target.value)} />
        </label>{" "}
        <label>
          Тэмдэглэл <input value={note} onChange={(e) => setNote(e.target.value)} />
        </label>
      </p>
      <Profiler id="ProductTable" onRender={onRender}>
        <ProductTable products={visible} favorites={favorites} onToggle={toggleFavorite} />
      </Profiler>
    </main>
  );
}
"""

PROJECT_SOLUTION = """\
import { Profiler, useCallback, useMemo, useState } from "react";
import { products } from "./data";
import ProductTable from "./ProductTable";
import { computeStats } from "./stats";

function onRender(id, phase, actualDuration) {
  console.log(`⏱ ${id} ${phase}: ${actualDuration.toFixed(1)}ms`);
}

export default function App() {
  const [query, setQuery] = useState("");
  const [note, setNote] = useState("");
  const [favorites, setFavorites] = useState([]);

  // products нь файлын түвшний тогтмол — нэг л удаа тооцно.
  const stats = useMemo(() => computeStats(products), []);
  const visible = useMemo(
    () => products.filter((p) => p.name.toLowerCase().includes(query.toLowerCase())),
    [query],
  );

  const toggleFavorite = useCallback((id) => {
    setFavorites((current) =>
      current.includes(id) ? current.filter((f) => f !== id) : [...current, id],
    );
  }, []);

  return (
    <main>
      <h1>Барааны самбар</h1>
      <p>
        Нийт {stats.count} бараа · Дундаж үнэ {stats.avgPrice}₮ · Үлдэгдэл {stats.totalStock} ·
        Дуртай: {favorites.length}
      </p>
      <p>
        <label>
          Хайх <input value={query} onChange={(e) => setQuery(e.target.value)} />
        </label>{" "}
        <label>
          Тэмдэглэл <input value={note} onChange={(e) => setNote(e.target.value)} />
        </label>
      </p>
      <Profiler id="ProductTable" onRender={onRender}>
        <ProductTable products={visible} favorites={favorites} onToggle={toggleFavorite} />
      </Profiler>
    </main>
  );
}
"""

PERFORMANCE = ModuleSpec(
    title="Модул 12 — Гүйцэтгэл",
    description=(
        "Render-ийг хэмжиж, memo, useMemo, useCallback, code splitting, урт "
        "жагсаалтын аргуудаар аппыг хурдасгана."
    ),
    lessons=[
        LessonSpec(
            title="Шаардлагагүй render-ийг илрүүлэх",
            slug="render-hemjih",
            description="Render-ийг console.log, React DevTools Profiler, <Profiler>-оор хэмжиж, state-ийг доош зөөнө.",
            duration=900,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Component хэзээ, яагаад дахин render хийдгийг сэргээх
- `console.log`-оор render тоолох
- React DevTools Profiler болон `<Profiler>` API-аар хэмжих
- State-ийг доош зөөж шаардлагагүй render-ийг арилгах

### Яагаад чухал вэ

Жижиг апп дээр render хэдэн удаа болох нь хамаагүй — React маш хурдан.
Харин 500 мөртэй хүснэгт, график зэрэг «хүнд» component input-д үсэг
бичих бүрт дахин render хийгдвэл бичих нь гацаж эхэлнэ.

Гүйцэтгэлийг сайжруулахын өмнөх хамгийн эхний алхам бол **хэмжих**. Юу,
хэдэн удаа, хэр удаан render хийгдэж байгааг мэдэхгүйгээр «хурдасгах» нь
зүгээр л таамаг. Мэргэжлийн хөгжүүлэгчид «хэмж → шалтгааныг ол → засаад →
дахин хэмж» гэсэн дарааллыг баримталдаг.

### Render хэзээ болдог вэ

Модул 10-т үзсэнээр component гурван шалтгаанаар дахин render хийнэ:

1. Өөрийн **state** өөрчлөгдөх
2. **Эцэг component** render хийх — props нь өөрчлөгдөөгүй байсан ч!
3. Хэрэглэж буй **context**-ийн утга өөрчлөгдөх

Хоёр дахь нь хамгийн их гайхшруулдаг:

```jsx
function App() {
  const [text, setText] = useState("");
  return (
    <>
      <input value={text} onChange={(e) => setText(e.target.value)} />
      <ProductList /> {/* props авдаггүй ч үсэг бүрт render хийнэ */}
    </>
  );
}
```

Render хийсэн нь DOM өөрчлөгдсөн гэсэн үг биш. React шинэ JSX-ийг
хуучинтай харьцуулаад ялгаагүй бол DOM-д хүрэхгүй. Гэвч component-ийн
функц өөрөө **ажилласан** — дотор нь хүнд тооцоо байвал цаг зарцуулсан.

### console.log-оор тоолох

Хамгийн энгийн хэмжүүр:

```jsx
function ProductList() {
  console.log("render: ProductList");
  // ...
}
```

Энэ засварлагчид `StrictMode` байхгүй тул Console-ийн нэг мөр = нэг
render. Бодит Vite төсөлд `main.jsx` дотор `<StrictMode>` байдаг бөгөөд
development үед component-ийг зориуд **хоёр удаа** render хийдэг. Лог
давхар гарвал айх хэрэггүй — production build-д нэг л удаа.

### React DevTools Profiler

Бодит төсөлд хамгийн хүчтэй хэрэгсэл бол **React DevTools** (Chrome,
Firefox, Edge-ийн өргөтгөл). Энэ засварлагч хамгаалагдсан iframe дотор
ажилладаг тул DevTools энд харагдахгүй — өөрийн Vite төсөл дээр туршаарай:

1. Өргөтгөлийг суулгаад апп-аа `npm run dev`-ээр нээнэ.
2. DevTools → **Profiler** tab → ⚙ тохиргооноос «Record why each
   component rendered while profiling»-ийг асаана.
3. ⏺ дараад апп дээр үйлдэл хийнэ (жишээ нь input-д бичнэ), дараа нь
   зогсооно.
4. **Flamegraph** нь commit бүрт аль component хэдэн мс зарцуулсныг,
   **Ranked** нь хамгийн удааныг эхэнд нь харуулна. Component дээр дарвал
   «Why did this render?» хэсэгт шалтгаан гарна: «The parent component
   rendered», «Hook 1 changed» гэх мэт.

⚙ → General → «Highlight updates when components render»-ийг асаавал
render хийсэн component бүр дэлгэц дээр хүрээгээр гялсхийнэ — шаардлагагүй
render нүдэнд шууд харагдана.

### `<Profiler>` API

Кодоор хэмжих бол React-ийн `Profiler` component бий:

```jsx
import { Profiler } from "react";

function onRender(id, phase, actualDuration, baseDuration) {
  console.log(`${id} ${phase} ${actualDuration.toFixed(1)}ms`);
}

<Profiler id="ProductList" onRender={onRender}>
  <ProductList />
</Profiler>
```

- `id` — аль хэсэг болохыг ялгах нэр
- `phase` — `"mount"` (анх), `"update"` (дахин render), `"nested-update"`
- `actualDuration` — энэ commit-д дотор нь render хийсэн component-уудад
  зарцуулсан хугацаа (мс)
- `baseDuration` — бүх дэд модыг memo-гүйгээр render хийвэл зарцуулах
  тооцоолсон хугацаа

`Profiler` нь development build-д ажиллана; production-д анхдагчаар
унтраалттай. Development build өөрөө удаан тул абсолют тоо биш,
**өмнө ба дараах** харьцуулалт чухал.

### Засах арга: state-ийг доош зөө

`memo`-г дараагийн хичээлд үзнэ. Гэхдээ хамгийн энгийн, үнэгүй арга нь
state-ийг түүнийг ашигладаг component руу нь ойртуулах:

```jsx
function FeedbackBox() {
  const [text, setText] = useState("");
  return <input value={text} onChange={(e) => setText(e.target.value)} />;
}

function App() {
  return (
    <>
      <FeedbackBox /> {/* state энд — зөвхөн энэ render хийнэ */}
      <ProductList /> {/* App render хийхгүй тул энэ ч хийхгүй */}
    </>
  );
}
```

Одоо үсэг бичихэд зөвхөн `FeedbackBox` render хийнэ.

```jsx
function Child() {
  console.log("Child");
  return <p>Би хүүхэд</p>;
}

function Parent() {
  const [n, setN] = useState(0);
  return (
    <>
      <button onClick={() => setN(n + 1)}>{n}</button>
      <Child />
    </>
  );
}
```

```quiz
Дээрх `Parent`-ийн товчийг 3 удаа дарвал Console-д нийт хэдэн «Child» гарах вэ? (StrictMode-гүй)
- [ ] 1
- [ ] 3
- [x] 4
- [ ] 6
> Анх mount хийхэд 1, дараа нь `Parent` render хийх бүрт `Child` ч дахин render хийнэ: 1 + 3 = 4. Props өөрчлөгдөөгүй ч хамаагүй.
```

```quiz
Удаан апп-ыг хурдасгах зөв дараалал аль вэ?
- [ ] Бүх component-д `memo` нэмээд дараа нь хэмжих
- [x] Хэмжих → шалтгааныг олох → засах → дахин хэмжих
- [ ] Production build хийгээд л болно
> Хэмжилтгүйгээр оновчлол нь таамаг. Засварын дараа дахин хэмжиж үр дүн гарсан эсэхийг баталгаажуулна.
```

### Дүгнэлт

Эцэг render хийхэд хүүхдүүд нь props-оос үл хамааран render хийнэ.
`console.log`, React DevTools Profiler, `<Profiler>`-оор юу, хэдэн удаа
render хийж байгааг хэмжинэ. Хамгийн энгийн засвар бол state-ийг түүнийг
ашигладаг газар руу нь доош зөөх.
""",
            initial_code=vite(
                MEASURE_APP,
                locked={"ProductList.jsx": MEASURE_PRODUCT_LIST, "slow.js": SLOW_JS},
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 12 минут

«Санал хүсэлт» талбарт үсэг бичих бүрт «удаан» `ProductList` (🔒) дахин
render хийж байна — Console-оос `render: ProductList` мөрийг тоолж хар.

Эхлээд **хэмж**: `onRender` функц бичиж, `ProductList`-ийг
`<Profiler id="ProductList" onRender={onRender}>`-оор ороо. `onRender` нь
Console-д `ProductList mount 5.2ms` хэлбэрээр (`id`, `phase`,
`actualDuration`) бичнэ. Дараа нь **зас**: талбар, түүний state, «N
тэмдэгт» мөрийг тусдаа `FeedbackBox` component руу зөө.
""",
                tests=(
                    test(
                        "Санал хүсэлт бичихэд тэмдэгтийн тоо харагдана",
                        """
render(<App />);
await user.type(screen.getByRole("textbox"), "Сайн");
expect(screen.text()).toContain("4 тэмдэгт");
""",
                    ),
                    test(
                        "Санал хүсэлт бичихэд ProductList дахин render хийгдэхгүй",
                        """
render(<App />);
await user.type(screen.getByRole("textbox"), "Сайн байна уу");
expect(logs.filter((l) => l.text === "render: ProductList").length).toBe(1);
""",
                    ),
                    test(
                        "Profiler нь «ProductList mount …ms» гэж Console-д бичнэ",
                        """
render(<App />);
const lines = logs.map((l) => l.text).join(" | ");
expect(lines).toMatch(/ProductList mount [0-9.]+ms/);
""",
                    ),
                ),
                tips="""\
- `Profiler`-ийг `react`-оос импортолно — эхлэл кодод аль хэдийн бий.
- `onRender`-ийн эхний гурван параметр нь `id`, `phase`, `actualDuration`.
  Template string: `` `${id} ${phase} ${actualDuration.toFixed(1)}ms` ``.
- `FeedbackBox`-д `feedback` state, `<input>`, «N тэмдэгт» мөр гурвуулаа
  орно. State `App`-д үлдвэл `App` бүхэлдээ render хийсээр байна.
- `FeedbackBox`-ийг `App`-ийн **дотор** функц болгож бүү зарла — render
  бүрт шинэ component болж, input фокусаа алдана. Файлын түвшинд зарла.
""",
                solution=solution(App_jsx=MEASURE_SOLUTION),
            ),
        ),
        LessonSpec(
            title="memo: ижил props-той үед render алгасах",
            slug="memo",
            description="memo нь props-ыг хэрхэн харьцуулж, хэзээ render-ийг алгасдаг вэ.",
            duration=840,
            language=JSX,
            content="""\
### Энэ хичээлээр

- `memo` юу хийдэг, props-ыг хэрхэн харьцуулдгийг ойлгох
- `memo` хэзээ тусалж, хэзээ дэмий болохыг ялгах
- Жагсаалтын картуудыг `memo`-оор хурдасгах

### Яагаад чухал вэ

Өмнөх хичээлд state-ийг доош зөөж render-ийг багасгасан. Гэвч заримдаа
state эцэгтээ байх ёстой (горим, сагс, шүүлтүүр), тэгээд эцэг render
хийхэд 50 карт бүгд дахин render хийнэ — props нь огт өөрчлөгдөөгүй
байхад. `memo` нь React-д «props адилхан бол энэ component-ийг алгас»
гэж хэлнэ.

### memo хэрхэн ажилладаг вэ

```jsx
import { memo } from "react";

function ProductCard({ name, price }) {
  console.log("render:", name);
  return <p>{name} — {price}₮</p>;
}

export default memo(ProductCard);
```

`memo(Component)` нь шинэ component буцаана. Эцэг render хийхэд React
шинэ props-ыг хуучинтай нь **prop тус бүрээр** `Object.is`-ээр
харьцуулна (shallow comparison). Бүгд ижил бол өмнөх үр дүнг дахин
ашиглаж, `ProductCard` функц огт ажиллахгүй.

| Prop | Өмнө | Одоо | Ижил үү? |
|---|---|---|---|
| `price` | `3500` | `3500` | ✅ |
| `name` | `"Алим"` | `"Алим"` | ✅ |
| `product` | `{…}` | `{…}` — шинээр үүсгэсэн | ❌ |
| `onAdd` | `() => …` | `() => …` — шинэ функц | ❌ |

Тоо, текст, boolean утгаараа харьцуулагдана. Объект, массив, функц
**хаягаараа** харьцуулагдана: агуулга нь ижил ч render бүрт шинээр
үүсгэсэн бол «өөр». Энэ асуудлыг дараагийн хичээлд `useMemo`,
`useCallback`-аар шийднэ.

### Immutable шинэчлэлийн бонус

```jsx
setProducts(products.map((p) => (p.id === 1 ? { ...p, price: 3000 } : p)));
```

`map` нь зөвхөн Бананын объектыг шинээр үүсгэж, бусдыг нь **хэвээр**
буцаана. Тиймээс `product={p}` гэж объектоор нь дамжуулсан ч бусад карт
memo-той бол render хийхгүй. Хэрэв `products.map((p) => ({ ...p }))` гэж
бүгдийг хуулбал бүх карт «шинэ» болно.

### memo юуг зогсоодоггүй вэ

- Component-ийн **өөрийн state** өөрчлөгдөх
- Хэрэглэж буй **context** өөрчлөгдөх
- `children` зэрэг JSX prop: `<Card><p>…</p></Card>` дахь `<p>` нь render
  бүрт шинэ объект тул `Card`-ийн memo ажиллахгүй

### Хэзээ хэрэглэх вэ

`memo` үнэгүй биш: props-ыг харьцуулахад цаг орж, код төвөгтэй болно.
Хэрэглэх нь зүйтэй:

- Component нь мэдэгдэхүйц удаан render хийдэг (Profiler-оор хэмжсэн!)
- Ижил props-тойгоор ойр ойрхон дахин render хийгддэг
- Жагсаалтын мөр, карт гэх мэт олон хувьтай

Хэрэггүй: props нь бараг үргэлж өөрчлөгддөг, эсвэл component маш хөнгөн.

Хоёр дахь аргументаар өөрийн харьцуулалтыг өгч болно:
`memo(Chart, (prev, next) => prev.data === next.data)`. Энэ нь ховор
хэрэглэгддэг бөгөөд аюултай — шинэ функц prop-ийг харьцуулахаа мартвал
хуучирсан callback дуудагдана.

### React Compiler

Модул 11-д үзсэн **React Compiler** нь build үед `memo`, `useMemo`,
`useCallback`-ийг автоматаар нэмдэг. Compiler асаасан төсөлд гараар
`memo` бичих нь ховор болно. Гэвч олон төсөл compiler-гүй хэвээр бөгөөд
ойлголт нь ижил — render яагаад болдгийг мэдэхгүй бол compiler юу хийж
байгааг ч ойлгохгүй.

```jsx
const Card = memo(function Card({ product, onSelect }) {
  return <button onClick={onSelect}>{product.name}</button>;
});

function List({ products }) {
  const [selected, setSelected] = useState(null);
  return products.map((p) => (
    <Card key={p.id} product={p} onSelect={() => setSelected(p.id)} />
  ));
}
```

```quiz
Дээрх кодод `selected` өөрчлөгдөхөд бүх `Card` дахин render хийсээр байна. Яагаад?
- [ ] `memo` зөвхөн class component-д ажилладаг
- [ ] `product` объект render бүрт шинээр үүсдэг
- [x] `onSelect` нь render бүрт шинэ функц
- [ ] `key` буруу сонгосон
> `() => setSelected(p.id)` нь `List` render хийх бүрт шинээр үүснэ. `product` нь `products` массивын хуучин объект тул ижил.
```

```quiz
`memo`-той component аль тохиолдолд render ХИЙХГҮЙ вэ?
- [ ] Өөрийн state нь өөрчлөгдсөн
- [ ] Хэрэглэж буй context нь өөрчлөгдсөн
- [x] Эцэг нь render хийсэн боловч бүх props нь өмнөхтэйгөө ижил
> `memo` зөвхөн props-ын харьцуулалтаар эцгээс ирэх render-ийг алгасна.
```

### Дүгнэлт

`memo` нь props-ыг prop тус бүрээр `Object.is`-ээр харьцуулж, ижил бол
render-ийг алгасна. Тоо, текст props-той картад шууд ажиллана; объект,
функц props-той бол тэдгээрийг тогтвортой байлгах хэрэгтэй. Хэмжээгүй
байж хаа сайгүй `memo` бүү нэм.
""",
            initial_code=vite(MEMO_APP, extra={"ProductCard.jsx": MEMO_CARD}),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 8 минут

«Горим солих» дарахад дөрвөн карт бүгд дахин render хийж байна —
Console-оос хар. `ProductCard.jsx`-ийг `memo`-оор ороож, props нь
өөрчлөгдөөгүй карт render хийхгүй болго. `console.log` мөрийг
устгахгүй — тестүүд түүгээр тоолно.
""",
                tests=(
                    test(
                        "«Горим солих» дарахад картууд дахин render хийгдэхгүй",
                        """
render(<App />);
const toggle = screen.getByRole("button", { name: "Горим солих" });
await user.click(toggle);
await user.click(toggle);
"""
                        + COUNT_RENDERS
                        + """
expect(count("Банана")).toBe(1);
expect(count("Сүү")).toBe(1);
""",
                    ),
                    test(
                        "Банана хямдрахад зөвхөн Бананын карт дахин render хийгдэнэ",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: "Бананыг хямдруулах" }));
"""
                        + COUNT_RENDERS
                        + """
expect(count("Банана")).toBe(2);
expect(count("Алим")).toBe(1);
expect(count("Жүрж")).toBe(1);
""",
                    ),
                    test(
                        "Хямдарсан үнэ картад харагдана",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: "Бананыг хямдруулах" }));
expect(screen.text()).toContain("3000₮");
""",
                    ),
                ),
                tips="""\
- `import { memo } from "react";`
- Хамгийн энгийн нь файлын төгсгөлд: `export default memo(ProductCard);`
  (`export default`-ийг функцийн өмнөөс авна).
- `App` дахь `products.map(...)` нь зөвхөн Бананын объектыг шинээр
  үүсгэдэг тул бусад картын props өмнөхтэйгөө ижил хэвээр.
- `console.log`-ийг memo-гийн гадна (жишээ нь `App` дотор) зөөвөл тоо
  буруу гарна — component-ийн бие дотор үлдээ.
""",
                solution=solution(ProductCard_jsx=MEMO_CARD_SOLUTION),
            ),
        ),
        LessonSpec(
            title="memo, useMemo, useCallback хамтдаа",
            slug="memo-hamt",
            description="Шинэ объект, функц props нь memo-г эвддэг — тогтвортой утгаар засна.",
            duration=960,
            language=JSX,
            content="""\
### Энэ хичээлээр

- `memo`-г «эвддэг» шинэ объект, массив, функц props-ыг таних
- `useMemo`, `useCallback`-ийг `memo`-той хослуулах
- Функциональ шинэчлэлээр callback-ийг тогтвортой байлгах

### Яагаад чухал вэ

«`memo` нэмсэн ч ажиллахгүй байна» гэдэг бол хамгийн түгээмэл гомдол.
Шалтгаан нь бараг үргэлж нэг: эцэг component render бүрт шинэ объект,
массив эсвэл функц үүсгэж дамжуулдаг. Модул 6-д `useMemo`,
`useCallback`-ийг тус тусад нь үзсэн — тэдгээрийн жинхэнэ хэрэглээ нь
`memo`-той хамт.

### Асуудал

```jsx
const ProductList = memo(function ProductList({ products, onAdd }) { /* … */ });

function App() {
  const [query, setQuery] = useState("");
  const [dark, setDark] = useState(false);
  const [cart, setCart] = useState([]);

  const visible = products.filter((p) => p.name.includes(query)); // шинэ массив
  const handleAdd = (id) => setCart([...cart, id]);               // шинэ функц

  return <ProductList products={visible} onAdd={handleAdd} />;
}
```

`dark` өөрчлөгдөхөд `visible`-ийн агуулга ижил, гэвч `filter` үргэлж
**шинэ** массив буцаадаг. `Object.is(хуучин, шинэ)` нь `false` → `memo`
дэмий. `handleAdd` ч мөн адил.

### Шийдэл

```jsx
const visible = useMemo(
  () => products.filter((p) => p.name.includes(query)),
  [query],
);

const handleAdd = useCallback((id) => {
  setCart((current) => [...current, id]);
}, []);
```

- `useMemo` — dependency өөрчлөгдөөгүй бол өмнөх массивыг (ижил хаягтай)
  буцаана.
- `useCallback(fn, deps)` нь `useMemo(() => fn, deps)`-тэй ижил — функцийг
  өөрийг нь хадгална.

### Функциональ шинэчлэл — хоосон dependency-ийн түлхүүр

`handleAdd` дотор `cart` хэрэглэвэл хоёр муу сонголт үлдэнэ:

- `useCallback(() => setCart([...cart, id]), [cart])` — зөв ажиллана,
  гэвч `cart` өөрчлөгдөх бүрт шинэ функц → «Нэмэх» бүрт жагсаалт бүхэлдээ
  render хийнэ.
- `useCallback(() => setCart([...cart, id]), [])` — функц тогтвортой,
  гэвч эхний render-ийн **хуучирсан** (stale) `cart = []`-ийг барьж
  үлдэнэ: хэдэн удаа дарсан ч сагсанд 1 л бараа.

`setCart((current) => [...current, id])` гэвэл React одоогийн утгыг
өөрөө өгдөг тул `cart`-ийг dependency-д оруулах шаардлагагүй. `setState`
функц өөрөө үргэлж тогтвортой.

### Бусад «далд» шинэ утга

| Бичлэг | Асуудал | Шийдэл |
|---|---|---|
| `style={{ color: "red" }}` | Render бүрт шинэ объект | Component-ийн гадна тогтмол |
| `options={["S", "M", "L"]}` | Шинэ массив | Component-ийн гадна тогтмол |
| `onClick={() => …}` | Шинэ функц | `useCallback` |
| `<Card>…</Card>` | `children` шинэ JSX | Ихэвчлэн memo хэрэггүй |

Өөрчлөгддөггүй утгыг component-ийн **гадна** зарлах нь хамгийн энгийн
бөгөөд hook шаардахгүй.

### Хэтэрхий бүү ашигла

Бүх утгыг `useMemo`, бүх функцийг `useCallback`-аар ороох нь кодыг
уншихад хэцүү болгоод ихэнхдээ ямар ч ашиггүй: хүлээн авагч нь
`memo`-гүй бол тогтвортой хаяг юу ч өгөхгүй. Дүрэм: **memo-той
component-д дамжуулдаг** эсвэл effect-ийн dependency болдог утгад л
хэрэглэ. React Compiler асаасан төсөлд энэ бүгдийг compiler өөрөө хийнэ.

```jsx
const Child = memo(function Child({ config }) {
  console.log("Child");
  return null;
});

function Parent() {
  const [n, setN] = useState(0);
  const config = useMemo(() => ({ theme: "dark" }), [n]);
  return (
    <>
      <button onClick={() => setN(n + 1)}>{n}</button>
      <Child config={config} />
    </>
  );
}
```

```quiz
Дээрх `Parent`-ийн товчийг 2 удаа дарвал «Child» нийт хэдэн удаа хэвлэгдэх вэ?
- [ ] 1
- [x] 3
- [ ] 2
> `useMemo`-гийн dependency нь `n` — дарах бүрт шинэ `config` үүснэ: 1 + 2 = 3. Dependency-г `[]` болговол (эсвэл объектыг гадна зарлавал) 1 болно.
```

```quiz
`memo`-той хүүхдэд дамжуулахад render бүрт ИЖИЛ хэвээр үлдэх утгууд аль нь вэ? (олон хариулт)
- [x] `useState`-ийн `setCount` функц
- [x] Component-ийн гадна зарласан `const SIZES = ["S", "M"]`
- [ ] `() => setCount(0)`
- [ ] `{ ...user }`
> React `setState` функцийг тогтвортой байлгадаг. Гадна зарласан тогтмол нэг л удаа үүснэ. Arrow функц, spread нь render бүрт шинэ.
```

### Дүгнэлт

`memo` зөвхөн props нь тогтвортой үед ажиллана. Шүүсэн массив,
тооцоолсон объектод `useMemo`, callback-д `useCallback`, state-ийн
шинэчлэлд функциональ хэлбэрийг хэрэглэнэ. Өөрчлөгддөггүй утгыг
component-ийн гадна зарла.
""",
            initial_code=vite(
                TOGETHER_APP,
                locked={"ProductList.jsx": TOGETHER_LIST, "data.js": TOGETHER_DATA},
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐ · 15 минут

`ProductList` (🔒) аль хэдийн `memo`-той. Гэвч «Горим солих» эсвэл
«Нэмэх» дарахад Console-д `render: ProductList` дахин дахин гарч байна.
`App.jsx` дахь шүүсэн жагсаалт ба `handleAdd`-ийг тогтвортой болгож
`memo`-г ажиллуул. Хайлт, сагс хэвийн ажилласаар байх ёстой.
""",
                tests=(
                    test(
                        "«Горим солих» дарахад ProductList дахин render хийгдэхгүй",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: "Горим солих" }));
await user.click(screen.getByRole("button", { name: "Горим солих" }));
expect(logs.filter((l) => l.text === "render: ProductList").length).toBe(1);
""",
                    ),
                    test(
                        "«Нэмэх» дарахад сагсны тоо зөв нэмэгдэнэ",
                        """
render(<App />);
const buttons = screen.getAllByRole("button", { name: "Нэмэх" });
await user.click(buttons[0]);
await user.click(buttons[1]);
expect(screen.text()).toContain("Сагс: 2");
""",
                    ),
                    test(
                        "«Нэмэх» дарахад ProductList дахин render хийгдэхгүй",
                        """
render(<App />);
const buttons = screen.getAllByRole("button", { name: "Нэмэх" });
await user.click(buttons[0]);
await user.click(buttons[1]);
expect(logs.filter((l) => l.text === "render: ProductList").length).toBe(1);
""",
                    ),
                    test(
                        "Хайлтаар жагсаалт шүүгдсээр байна",
                        """
render(<App />);
await user.type(screen.getByRole("textbox"), "ал");
const items = screen.getAllByRole("listitem");
expect(items).toHaveLength(1);
expect(items[0]).toHaveTextContent("Алим");
""",
                    ),
                ),
                tips="""\
- `useMemo(() => products.filter(...), [query])` — `products` файлын
  гаднаас ирдэг тогтмол тул dependency-д зөвхөн `query`.
- `useCallback((id) => setCart((current) => [...current, id]), [])`.
- Функциональ шинэчлэлгүйгээр `[]` бичвэл «Сагс» 1-ээс өсөхгүй —
  хуучирсан `cart`.
- `[cart]` dependency бичвэл тоо зөв боловч «Нэмэх» бүрт жагсаалт дахин
  render хийнэ.
""",
                solution=solution(App_jsx=TOGETHER_SOLUTION),
            ),
        ),
        LessonSpec(
            title="Code splitting ба bundle-ийн хэмжээ",
            slug="code-splitting",
            description="lazy, dynamic import-оор кодыг хувааж, bundle, зураг, кэшийг оновчлох.",
            duration=960,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Bundle гэж юу вэ, том bundle яагаад удаан ачаалагддагийг ойлгох
- `import()`, `lazy`, `Suspense`-ээр кодыг хэсэгчлэн ачаалах
- Bundle-ийг шинжлэх, сүлжээний гүйцэтгэлийг (зураг, кэш) сайжруулах

### Яагаад чухал вэ

Vite `npm run build` хийхэд таны бүх код болон сангууд цөөн хэдэн JS
файл — **bundle** болно. Хэрэглэгч эхний хуудсыг харахын өмнө энэ файлыг
бүхэлд нь татаж, задлан ажиллуулна. Админ хуудас, график, PDF үүсгэгч
зэрэг ховор хэрэглэгддэг хэсэг ч эхний ачааллад орвол гар утасны удаан
сүлжээнд апп хэдэн секунд цагаан дэлгэцтэй байна. Code splitting нь
кодыг хэрэгтэй үед нь татна.

### Dynamic `import()`

Энгийн `import` файлын эхэнд ажилладаг. `import()` бол функц: модулийг
**дуудсан үед** татаж, Promise буцаана:

```jsx
async function exportPdf() {
  const { jsPDF } = await import("jspdf"); // товч дарах үед л татагдана
  const doc = new jsPDF();
  doc.text("Тайлан", 10, 10);
  doc.save("tailan.pdf");
}
```

Vite `import()` бүрийг тусдаа файл (chunk) болгож хуваадаг.

### `lazy` ба `Suspense`

Component-ийг хэсэгчлэн ачаалах бол `lazy` (Модул 10):

```jsx
import { lazy, Suspense } from "react";

const AdminPage = lazy(() => import("./AdminPage"));

function App() {
  return (
    <Suspense fallback={<p>Ачаалж байна…</p>}>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/admin" element={<AdminPage />} />
      </Routes>
    </Suspense>
  );
}
```

- `lazy`-г **файлын түвшинд** зарлана. Component дотор зарлавал render
  бүрт шинэ component болж, state нь алдагдана.
- Модуль `export default`-той байх ёстой. Нэртэй export бол:
  `lazy(() => import("./Charts").then((m) => ({ default: m.SalesChart })))`.
- Хамгийн ашигтай хуваалт бол **route**-оор: хэрэглэгч аль хуудсанд
  орсон, тэр хуудасны код л татагдана.

Урьдчилан татах: хэрэглэгч товч дээр хулганаа авчрахад
`onMouseEnter={() => import("./AdminPage")}` гэж дуудвал дарах үед файл
бэлэн болсон байна. `import()` нэг модулийг хоёр дахь удаа татдаггүй.

### Bundle-ийг шинжлэх

- `npm run build`-ийн гаралт chunk бүрийн хэмжээг харуулна. 500 kB-аас
  том бол Vite анхааруулдаг.
- `rollup-plugin-visualizer` нь аль сан хэдий хэмжээ эзэлж байгааг
  өнгөт зургаар харуулна.
- Том сангийн оронд жижгийг сонго: `moment` (~300 kB)-ийн оронд `Intl`
  эсвэл `date-fns`; бүх `lodash`-ийн оронд тусдаа функц.

### Сүлжээний гүйцэтгэл

JavaScript-ээс гадна:

- **Зураг** — ихэнх хуудасны хамгийн том хэсэг. WebP/AVIF формат,
  тохирох хэмжээ (`srcset`), харагдах хүртэл ачаалахгүй
  `loading="lazy"`. `width`, `height`-ийг заавал өг — эс бөгөөс ачаалагдах
  үед хуудас «үсэрнэ».
- **Кэш** — Vite файлын нэрэнд hash нэмдэг (`index-a1b2c3.js`). Иймд
  `assets/`-ийг `Cache-Control: max-age=31536000, immutable`-ээр жил
  кэшлэж, харин `index.html`-ийг кэшлэхгүй. Шинэ хувилбар гарахад нэр нь
  өөрчлөгдөж, хэрэглэгч шинийг авна.
- **Шахалт** — gzip/brotli-г CDN (Cloudflare гэх мэт) ихэвчлэн өөрөө
  хийнэ.

### Энэ засварлагчид

Баруун талын «Хөтөч» дээр «Тусламж» дарж үз: `Help` модуль хэрэгтэй үед
л татагдаж, Console-д «📦 Help модуль ачааллаа» гарна. Sandbox-д
`import()` шууд биелдэг тул `withDelay` (🔒) сүлжээний хүлээлтийг
дуурайна — бодит төсөлд үүнийг бичихгүй.

```quiz
Дараах кодын алдаа юу вэ?

`function App() { const Admin = lazy(() => import("./Admin")); return <Suspense fallback="…"><Admin /></Suspense>; }`
- [ ] `lazy` нь зөвхөн route дээр ажилладаг
- [x] `lazy` component дотор зарлагдсан тул render бүрт шинэ component болно
- [ ] `fallback` нь JSX биш текст байж болохгүй
> `lazy`-г файлын түвшинд зарлана. `fallback` нь текст ч байж болно.
```

```quiz
Vite-ийн `assets/index-a1b2c3.js` мэт hash-тай файлыг яагаад удаан хугацаагаар кэшлэж болдог вэ?
- [x] Агуулга өөрчлөгдөхөд файлын нэр өөрчлөгддөг
- [ ] Хөтөч JS файлыг хэзээ ч шинэчилдэггүй
- [ ] Hash нь файлыг шахдаг
> Шинэ build өөр нэртэй файл үүсгэж, шинэ `index.html` түүнийг зааж өгнө.
```

### Дүгнэлт

Эхний ачааллыг жижиг байлга: ховор хэрэглэгдэх хуудас, том санг
`lazy`/`import()`-оор хэрэгтэй үед нь татна. Bundle-ийг шинжилж том
сангуудыг ол; зураг, кэшийг зөв тохируул.
""",
            initial_code=vite(
                SPLIT_APP,
                locked={
                    "Reports.jsx": SPLIT_REPORTS,
                    "Help.jsx": SPLIT_HELP,
                    "network.js": SPLIT_NETWORK,
                },
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 10 минут

«Тайлан» хуудас (`Reports.jsx` 🔒) нь «хүнд». Одоо static import-оор
холбогдсон тул апп эхлэхэд л татагдаж байна — Console-д «📦 Reports
модуль ачааллаа» шууд гарна. `Help`-ийн жишээг дагаж `Reports`-ийг
`lazy` болго: «Тайлан» дарах үед л татагдаж, хүлээх хооронд «Ачаалж
байна…» харагдана.
""",
                tests=(
                    test(
                        "Апп эхлэхэд Reports модуль ачаалагдахгүй",
                        """
render(<App />);
expect(logs.some((l) => l.text.includes("Reports модуль ачааллаа"))).toBe(false);
""",
                    ),
                    test(
                        "«Тайлан» дарахад эхлээд «Ачаалж байна…» харагдана",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: "Тайлан" }));
expect(screen.text()).toContain("Ачаалж байна");
""",
                    ),
                    test(
                        "Дараа нь «Борлуулалтын тайлан» гарч ирнэ",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: "Тайлан" }));
expect(await screen.findByRole("heading", { name: "Борлуулалтын тайлан" })).toBeInTheDocument();
expect(logs.some((l) => l.text.includes("Reports модуль ачааллаа"))).toBe(true);
""",
                    ),
                ),
                tips="""\
- `import Reports from "./Reports";` мөрийг устгаж, оронд нь
  `const Reports = lazy(() => withDelay(() => import("./Reports")));`
- `<Reports />`-ийг `<Suspense fallback={…}>` дотор оруул — `Help`-тэй
  нэг `Suspense`-д ч болно.
- Static import нэг ч газар үлдвэл модуль эхэнд нь татагдсаар байна.
""",
                solution=solution(App_jsx=SPLIT_SOLUTION),
            ),
        ),
        LessonSpec(
            title="Урт жагсаалт",
            slug="urt-jagsaalt",
            description="Мянга мянган мөрийг хуудаслалт, «Цааш үзэх», windowing-оор харуулах.",
            duration=900,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Олон мянган мөр render хийх нь яагаад удаан байдгийг ойлгох
- Хуудаслалт (pagination) ба «Цааш үзэх» (load more) бичих
- Windowing (virtualization)-ийн санаа, `react-window`-той танилцах

### Яагаад чухал вэ

Захиалгын түүх, бүтээгдэхүүний каталог, чат — жагсаалт хурдан томордог.
10 000 мөр = 10 000+ DOM элемент: эхний render удаан, санах ой их
зарцуулж, жагсаалтын дээрх input-д бичих бүрт React бүгдийг дахин
харьцуулна. Хэрэглэгч нэг дор 20–30 мөрөөс илүүг хардаггүй — бусдыг
render хийх нь дэмий.

### 1. Хуудаслалт

Хамгийн энгийн, найдвартай арга:

```jsx
const PAGE_SIZE = 20;

function OrderList({ orders }) {
  const [page, setPage] = useState(1);
  const pageCount = Math.ceil(orders.length / PAGE_SIZE);
  const visible = orders.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE);

  return (
    <>
      <ul>{visible.map((o) => <li key={o.id}>{o.title}</li>)}</ul>
      <button disabled={page === 1} onClick={() => setPage(page - 1)}>Өмнөх</button>
      <button disabled={page === pageCount} onClick={() => setPage(page + 1)}>Дараах</button>
    </>
  );
}
```

Бодит аппад өгөгдлийг ч хуудсаар нь серверээс авна:
`GET /api/orders?page=2&limit=20` — 10 000 мөрийг нэг дор татах нь
render-ээс ч удаан.

### 2. «Цааш үзэх»

Нийгмийн сүлжээ, онлайн дэлгүүрт түгээмэл:

```jsx
const [count, setCount] = useState(20);
const visible = items.slice(0, count);
// …
<button onClick={() => setCount(count + 20)}>Цааш үзэх</button>
```

Товч дарахын оронд жагсаалтын төгсгөл харагдах үед автоматаар ачаалбал
**infinite scroll** болно (`IntersectionObserver`; TanStack Query-ийн
`useInfiniteQuery`). Сул тал: мөр нэмэгдэх тусам DOM томорсоор байна.

### 3. Windowing

Бүх мөрийг гүйлгэх (scroll) боломжтой байлгаад зөвхөн **харагдаж буй**
мөрүүдийг render хийнэ. Гүйлгэх бүрт аль мөрүүд харагдахыг тооцоолно:

```jsx
const ROW_HEIGHT = 32;
const VIEW_HEIGHT = 320;

function VirtualList({ items }) {
  const [scrollTop, setScrollTop] = useState(0);
  const start = Math.floor(scrollTop / ROW_HEIGHT);
  const visible = items.slice(start, start + VIEW_HEIGHT / ROW_HEIGHT + 1);

  return (
    <div
      style={{ height: VIEW_HEIGHT, overflowY: "auto" }}
      onScroll={(e) => setScrollTop(e.currentTarget.scrollTop)}
    >
      <div style={{ height: items.length * ROW_HEIGHT, position: "relative" }}>
        {visible.map((item, i) => (
          <div
            key={item.id}
            style={{ position: "absolute", top: (start + i) * ROW_HEIGHT, height: ROW_HEIGHT }}
          >
            {item.title}
          </div>
        ))}
      </div>
    </div>
  );
}
```

Гадна `div` нь 320px өндөртэй гүйлгэгч, дотор нь бүх мөрийн нийт
өндөртэй «хоосон» `div` (scrollbar зөв харагдахын тулд). 10 000 мөрөөс
~11-ийг л render хийнэ.

Бодит төсөлд үүнийг гараар бичихгүй — өөр өөр өндөртэй мөр, дэлгэцийн
хэмжээ өөрчлөгдөх зэргийг сангууд шийддэг:

```jsx
import { List } from "react-window";

function Row({ index, style, orders }) {
  return <div style={style}>{orders[index].title}</div>;
}

<List rowComponent={Row} rowCount={orders.length} rowHeight={32} rowProps={{ orders }} />
```

Мөн `@tanstack/react-virtual`-ийн `useVirtualizer` түгээмэл. Сул тал:
хөтчийн «Ctrl + F» хайлт render хийгдээгүй мөрийг олохгүй.

### Аль нь вэ?

| Арга | Хэзээ |
|---|---|
| Хуудаслалт | Хүснэгт, админ самбар, хайлтын үр дүн |
| «Цааш үзэх» | Мэдээний урсгал, каталог — хэдэн зуун мөр |
| Windowing | Мянга мянган мөрийг нэг дор гүйлгэх (лог, чат) |

Аль ч аргад `key`-г `id`-аар өг (index биш), мөрийн component-ийг
`memo`-оор ороовол шүүлтүүр өөрчлөгдөхөд хуучин мөрүүд render хийхгүй.

```quiz
1000 мөртэй жагсаалтыг хуудас бүрт 20-оор харуулна. 3-р хуудсанд `slice`-ийн аргументууд юу байх вэ? (`page` 1-ээс эхэлнэ)
- [ ] `slice(60, 80)`
- [x] `slice(40, 60)`
- [ ] `slice(3, 23)`
> `(page - 1) * 20 = 40`-өөс `page * 20 = 60` хүртэл. `slice`-ийн төгсгөл нь орохгүй.
```

```quiz
Windowing-ийн гол санаа аль вэ?
- [ ] Бүх мөрийг render хийгээд CSS-ээр нуух
- [x] Зөвхөн харагдаж буй мөрүүдийг render хийж, гүйлгэх үед солих
- [ ] Мөр бүрийг тусдаа хуудсанд харуулах
> DOM-д цөөн мөр л байх тул жагсаалт хэчнээн урт байсан ч хурдан.
```

### Дүгнэлт

Хэрэглэгчийн харахгүй мөрийг render хийх хэрэггүй. Ихэнх тохиолдолд
хуудаслалт эсвэл «Цааш үзэх» хангалттай; олон мянган мөрийг нэг дор
гүйлгэх бол windowing сан ашиглана.
""",
            initial_code=vite(LIST_APP, locked={"data.js": LIST_DATA}),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 12 минут

1000 захиалга бүгд нэг дор render хийгдэж байна. Хуудаслалт нэм:
хуудас бүрт 20 захиалга, доор нь «Өмнөх», `Хуудас 1 / 50` гэсэн текст,
«Дараах» товч. Эхний хуудсанд «Өмнөх», сүүлийн хуудсанд «Дараах» идэвхгүй
(`disabled`) байна.
""",
                tests=(
                    test(
                        "Эхний хуудсанд эхний 20 захиалга л харагдана",
                        """
render(<App />);
const items = screen.getAllByRole("listitem");
expect(items).toHaveLength(20);
expect(items[0]).toHaveTextContent("Захиалга #1");
expect(items[19]).toHaveTextContent("Захиалга #20");
""",
                    ),
                    test(
                        "«Дараах» дарахад дараагийн 20 захиалга гарна",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: "Дараах" }));
const items = screen.getAllByRole("listitem");
expect(items).toHaveLength(20);
expect(items[0]).toHaveTextContent("Захиалга #21");
expect(screen.text()).toContain("Хуудас 2 / 50");
""",
                    ),
                    test(
                        "«Өмнөх» дарахад өмнөх хуудас руу буцна",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: "Дараах" }));
await user.click(screen.getByRole("button", { name: "Дараах" }));
await user.click(screen.getByRole("button", { name: "Өмнөх" }));
expect(screen.getAllByRole("listitem")[0]).toHaveTextContent("Захиалга #21");
expect(screen.text()).toContain("Хуудас 2 / 50");
""",
                    ),
                    test(
                        "Эхний хуудсанд «Өмнөх», сүүлийнхэд «Дараах» идэвхгүй",
                        """
render(<App />);
expect(screen.getByRole("button", { name: "Өмнөх" })).toBeDisabled();
const next = screen.getByRole("button", { name: "Дараах" });
for (let i = 0; i < 49; i++) await user.click(next);
expect(screen.text()).toContain("Хуудас 50 / 50");
expect(screen.getAllByRole("listitem")[0]).toHaveTextContent("Захиалга #981");
expect(screen.getByRole("button", { name: "Дараах" })).toBeDisabled();
""",
                    ),
                ),
                tips="""\
- `const [page, setPage] = useState(1);`
- Хуудасны тоо: `Math.ceil(orders.length / PAGE_SIZE)`.
- Харагдах хэсэг: `orders.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE)`
  — `map`-ийг `orders` биш, үүн дээр хий.
- `disabled={page === 1}`, `disabled={page === pageCount}` — идэвхгүй
  товч дарагдахгүй тул `page` 0 эсвэл 51 болохгүй.
""",
                solution=solution(App_jsx=LIST_SOLUTION),
            ),
        ),
        LessonSpec(
            title="Төсөл: Удаан аппыг хурдасгах",
            slug="tusul-hurdasgah",
            description="Удаан самбарыг хэмжиж, гацааг олж, оновчлоод дахин хэмжинэ.",
            duration=2100,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Бодит гүйцэтгэлийн асуудлыг эхнээс нь дуустал шийдэх
- «Хэмж → шалтгааныг ол → оновчил → дахин хэмж» аргачлалыг хэрэглэх
- `useMemo`, `useCallback`, `memo`-г зөвхөн хэрэгтэй газар нь хэрэглэх

### Яагаад чухал вэ

Бодит ажил дээр «апп удаан байна» гэсэн гомдол ирэхэд хэн ч аль мөр
буруу байгааг хэлж өгөхгүй. Хөгжүүлэгч өөрөө хэмжиж, гацааг олж,
засвараа батлах ёстой. Энэ төсөл бол яг тийм даалгавар.

### Апп

«Барааны самбар» нь 200 бараатай хүснэгт, хайлт, тэмдэглэл бичих талбар,
дуртай бараа тэмдэглэх ☆ товчтой. Дээр нь статистик (нийт, дундаж үнэ,
үлдэгдэл) харуулна.

| Файл | Юу вэ |
|---|---|
| `App.jsx` | Самбар — state, тооцоо, `Profiler` |
| `ProductTable.jsx` | Хүснэгт — «удаан» (render бүрт ~10 мс) |
| `stats.js` 🔒 | `computeStats` — «хүнд» тооцоо (~15 мс) |
| `data.js` 🔒, `slow.js` 🔒 | Өгөгдөл, удаашруулагч |

### 1. Хэмж

«Хөтөч» дээр «Тэмдэглэл» талбарт хурдан бичиж үз — үсэг бүр хоцорно.
Console-оос тоол:

- `computeStats` — хэдэн удаа дуудагдсан бэ?
- `render: ProductTable` — хүснэгт хэдэн удаа render хийсэн бэ?
- `⏱ ProductTable update: 10.3ms` — `Profiler`-ийн хэмжсэн хугацаа

5 үсэг бичихэд 5 удаа хүнд тооцоо, 5 удаа хүснэгт — нэг ч нь тэмдэглэлтэй
холбоогүй.

### 2. Шалтгааныг ол

Өөрөөсөө асуу:

- `computeStats(products)`-ийн үр дүн `note` өөрчлөгдөхөд өөрчлөгдөх үү?
- `visible` массив render бүрт шинэ үү?
- `toggleFavorite` render бүрт шинэ үү?
- `ProductTable` ижил props авсан ч render хийх үү?

### 3. Оновчил

Өмнөх хичээлүүдийн хэрэгслүүд:

```jsx
const value = useMemo(() => heavy(a), [a]);        // тооцоог хадгалах
const handler = useCallback((id) => {
  setList((current) => /* … */ current);           // функциональ шинэчлэл
}, []);
export default memo(Component);                    // render алгасах
```

Хайлтын талбарт бичихэд хүснэгт render хийх нь **зөв** — харагдах мөрүүд
өөрчлөгдсөн. Мөн ☆ дарахад хүснэгт render хийх ёстой — од нь солигдоно.
Зөвхөн хамааралгүй өөрчлөлтөөс (тэмдэглэл) хамгаалах хэрэгтэй.

### 4. Дахин хэмж

Засварын дараа «Тэмдэглэл»-д бичихэд Console-д `computeStats`,
`render: ProductTable` гарахгүй, `⏱ ProductTable update` хугацаа ~0 мс
болсон байх ёстой. `Profiler` өөрөө `App`-тай хамт render хийдэг ч дотор
нь `memo`-той хүснэгт алгасагдсан тул хугацаа бараг тэг.

### Цаашид юу хийж болох вэ

- 200 биш 20 000 мөр бол: хуудаслалт эсвэл windowing (өмнөх хичээл)
- Хайлтын талбарт `useDeferredValue` (Модул 10): бичих нь шууд, хүснэгт
  хоцорч шинэчлэгдэнэ
- React Compiler асаавал `useMemo`, `useCallback`, `memo` автоматаар

```quiz
Хайлтын талбарт «ал» гэж бичихэд `ProductTable` дахин render хийх нь зөв үү?
- [x] Тийм — `visible` өөрчлөгдсөн тул хүснэгт шинэчлэгдэх ёстой
- [ ] Үгүй — `memo` байгаа бол хэзээ ч render хийх ёсгүй
> Оновчлолын зорилго нь render-ийг бүрмөсөн болиулах биш, ШААРДЛАГАГҮЙ render-ийг арилгах.
```

### Дүгнэлт

Гүйцэтгэлийн ажил хэмжилтээр эхэлж, хэмжилтээр дуусна. Хамааралгүй
state-ийн өөрчлөлтөөс хүнд тооцоог `useMemo`-оор, хүнд component-ийг
`memo` + тогтвортой props-оор хамгаална.
""",
            initial_code=vite(
                PROJECT_APP,
                extra={"ProductTable.jsx": PROJECT_TABLE},
                locked={"stats.js": PROJECT_STATS, "data.js": PROJECT_DATA, "slow.js": SLOW_JS},
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐⭐ · 30 минут

«Барааны самбар»-ын «Тэмдэглэл» талбарт бичихэд үсэг бүр хоцорч байна.
Заавар дахь дөрвөн алхмаар хурдасга: Console-оос хэмж, шалтгааныг ол,
`App.jsx`, `ProductTable.jsx`-ийг оновчил, дахин хэмж. UI, текст, 🔒
файлуудыг өөрчлөхгүй — апп яг өмнөх шигээ ажиллах ёстой, зөвхөн хурдан.
""",
                tests=(
                    test(
                        "«Хайх», «Тэмдэглэл»-д бичихэд computeStats дахин дуудагдахгүй",
                        """
render(<App />);
await user.type(screen.getByLabelText("Тэмдэглэл"), "сайн");
await user.type(screen.getByLabelText("Хайх"), "ал");
expect(logs.filter((l) => l.text === "computeStats").length).toBe(1);
""",
                    ),
                    test(
                        "«Тэмдэглэл»-д бичихэд ProductTable дахин render хийгдэхгүй",
                        """
render(<App />);
await user.type(screen.getByLabelText("Тэмдэглэл"), "сайн байна");
expect(logs.filter((l) => l.text === "render: ProductTable").length).toBe(1);
""",
                    ),
                    test(
                        "Хайлт хүснэгтийг шүүсээр байна",
                        """
render(<App />);
await user.type(screen.getByLabelText("Хайх"), "алим");
expect(screen.getAllByRole("button", { name: /дуртай/ })).toHaveLength(20);
expect(screen.getAllByRole("button", { name: /Алим/ })).toHaveLength(20);
""",
                    ),
                    test(
                        "Хоёр бараанд ☆ дарахад «Дуртай: 2» болно",
                        """
render(<App />);
const stars = screen.getAllByRole("button", { name: /дуртай/ });
await user.click(stars[0]);
await user.click(stars[1]);
expect(screen.getByText(/Дуртай:/)).toHaveTextContent("Дуртай: 2");
expect(screen.getAllByRole("button", { name: /дуртай/ })[0]).toHaveTextContent("★");
""",
                    ),
                ),
                tips="""\
- `computeStats(products)` нь зөвхөн `products`-оос хамаарна, `products`
  нь файлын түвшний тогтмол — `useMemo(() => computeStats(products), [])`.
- `visible`-д `useMemo`, dependency нь `[query]`.
- `toggleFavorite`-ийг `useCallback`-аар ороохдоо функциональ шинэчлэл
  хэрэглэ — эс бөгөөс хоёр дахь ☆ эхнийхийг «мартана».
- `ProductTable.jsx`-ийн төгсгөлд `export default memo(ProductTable);`
- Засвар бүрийн дараа «Хөтөч» дээр бичиж, Console-оос дахин хэмж.
""",
                solution=files(
                    ("App.jsx", PROJECT_SOLUTION),
                    ("ProductTable.jsx", PROJECT_TABLE_SOLUTION),
                ),
            ),
        ),
    ],
)
