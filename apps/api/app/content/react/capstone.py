"""Модул 14 — Төгсгөлийн төсөл: «Ногоон сагс».

Сургалтын бүх сэдвийг нэг бодит апп болгон нэгтгэнэ: онлайн хүнсний дэлгүүр.
Хичээл бүрийн эхлэл код нь өмнөх хичээлийн дууссан төлөв дээр шинэ TODO
нэмсэн хэлбэр. Тиймээс файл бүрийн хувилбарыг (`APP_1`, `APP_3`, …) нэг удаа
тодорхойлж, хичээлүүд дахин ашиглана.

Дэмжлэг аажмаар багасна (roadmap §19): 1–3, 5-р хичээл бүрэн чиглүүлэгтэй,
4, 6, 7, 8 хагас чиглүүлэгтэй, 9-р хичээл бие даасан (зөвхөн хүлээн авах
шалгуур — тестүүд).

`BrowserRouter` ба `QueryClientProvider` нь 🔒 `main.jsx`-д байх тул тест
`setPath(...)`-ийн дараа `runMain()`-ээр ажиллана.
"""

from app.content.react.common import files, test
from app.content.types import ExerciseSpec, LessonSpec, ModuleSpec
from app.models.enums import LessonLanguage

JSX = LessonLanguage.JSX

HTML = '<div id="root"></div>\n'


def patch(source: str, *changes: tuple[str, str]) -> str:
    """Өмнөх хувилбар дээр TODO, шинэ мөр нэмэх. Хуучин хэсэг заавал олдоно."""
    for old, new in changes:
        assert old in source, f"patch: «{old.strip()[:60]}» олдсонгүй"
        source = source.replace(old, new, 1)
    return source


def project(editable: list[tuple[str, str]], locked: list[tuple[str, str]]) -> str:
    """Төслийн файлууд: эхлээд энэ хичээлд засах файлууд (эхнийх нь нээгдэнэ),
    дараа нь 🔒 файлууд, төгсгөлд нь загвар, `main.jsx`, `index.html`."""
    return files(
        *editable,
        *((name, code, True) for name, code in locked),
        ("styles.css", STYLES_CSS, True),
        ("main.jsx", MAIN_JSX, True),
        ("index.html", HTML, True),
    )


# --- Бүх хичээлд ижил 🔒 файлууд ---------------------------------------------------

MAIN_JSX = """\
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router";
import App from "./App";
import "./styles.css";

// Серверийн өгөгдлийн кэш: татсан өгөгдлийг 1 минут «шинэ» гэж үзнэ,
// алдаа гарвал автоматаар дахин оролдохгүй (хэрэглэгч өөрөө шийднэ).
const queryClient = new QueryClient({
  defaultOptions: {
    queries: { staleTime: 60 * 1000, retry: false },
  },
});

createRoot(document.getElementById("root")).render(
  <QueryClientProvider client={queryClient}>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </QueryClientProvider>,
);
"""

STYLES_CSS = """\
:root {
  --green: #1f7a3a;
  --green-dark: #155d2b;
  --green-soft: #e8f5ec;
  --text: #1f2328;
  --muted: #59636e;
  --border: #d8dee4;
  --bg: #f6f8f5;
  --danger: #b42318;
  --radius: 12px;
  font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
  color: var(--text);
  background: var(--bg);
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
}

:focus-visible {
  outline: 3px solid #f5b400;
  outline-offset: 2px;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  margin: -1px;
  padding: 0;
  overflow: hidden;
  clip: rect(0 0 0 0);
  white-space: nowrap;
  border: 0;
}

.skip-link {
  position: absolute;
  top: -48px;
  left: 8px;
  z-index: 10;
  padding: 8px 12px;
  border-radius: 8px;
  background: #fff;
  color: var(--green-dark);
}

.skip-link:focus {
  top: 8px;
}

/* --- Layout ------------------------------------------------------------ */

.app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.site-header {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px 16px;
  padding: 10px 16px;
  background: var(--green-dark);
  color: #fff;
}

.brand {
  margin-right: auto;
  color: #fff;
  font-size: 1.15rem;
  font-weight: 800;
  text-decoration: none;
}

.nav,
.header-actions {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 4px;
}

.site-header a:not(.brand),
.site-header .link-button {
  padding: 6px 10px;
  border-radius: 8px;
  color: #e3f2e7;
  text-decoration: none;
}

.site-header a:not(.brand):hover,
.site-header .link-button:hover {
  background: rgba(255, 255, 255, 0.14);
  color: #fff;
}

.site-header a.active {
  background: #fff;
  color: var(--green-dark);
  font-weight: 600;
}

.badge {
  display: inline-block;
  min-width: 1.6em;
  margin-left: 4px;
  padding: 0 6px;
  border-radius: 999px;
  background: #f5b400;
  color: #1f2328;
  font-size: 0.8rem;
  font-weight: 700;
  text-align: center;
}

.container {
  flex: 1;
  width: 100%;
  max-width: 1040px;
  margin: 0 auto;
  padding: 20px 16px 32px;
}

.container:focus {
  outline: none;
}

.site-footer {
  padding: 16px;
  border-top: 1px solid var(--border);
  background: #fff;
  color: var(--muted);
  font-size: 0.9rem;
  text-align: center;
}

/* --- Ерөнхий ------------------------------------------------------------ */

h1 {
  margin: 0 0 12px;
  font-size: 1.6rem;
}

h2 {
  margin: 0 0 8px;
  font-size: 1.15rem;
}

.muted {
  color: var(--muted);
}

.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 9px 16px;
  border: 0;
  border-radius: 10px;
  background: var(--green);
  color: #fff;
  font: inherit;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
}

.button:hover {
  background: var(--green-dark);
}

.button:disabled {
  background: #9aa59f;
  cursor: not-allowed;
}

.button.secondary {
  border: 1px solid var(--green);
  background: #fff;
  color: var(--green-dark);
}

.link-button {
  padding: 0;
  border: 0;
  background: none;
  color: var(--green-dark);
  font: inherit;
  text-decoration: underline;
  cursor: pointer;
}

.link-button.danger {
  color: var(--danger);
}

.panel,
.card {
  padding: 16px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: #fff;
}

.panel + .panel {
  margin-top: 16px;
}

.empty {
  text-align: center;
}

.narrow {
  max-width: 440px;
  margin: 0 auto;
}

.big-emoji {
  margin: 0;
  font-size: 3rem;
}

.status {
  color: var(--muted);
}

.alert {
  padding: 12px;
  border: 1px solid #f1aeb5;
  border-radius: 10px;
  background: #fff5f5;
  color: var(--danger);
}

.alert p {
  margin: 0 0 8px;
}

.notice {
  padding: 10px 12px;
  border-radius: 10px;
  background: var(--green-soft);
  color: var(--green-dark);
}

/* --- Нүүр --------------------------------------------------------------- */

.hero {
  padding: 40px 24px;
  border-radius: 20px;
  background: linear-gradient(135deg, #e8f5ec, #fff7d6);
  text-align: center;
}

.hero h1 {
  font-size: 2.2rem;
}

.eyebrow {
  margin: 0 0 4px;
  color: var(--green);
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.lead {
  max-width: 520px;
  margin: 0 auto 20px;
  font-size: 1.1rem;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
  margin: 20px 0 0;
  padding: 0;
  list-style: none;
}

.features p {
  margin: 0;
}

.feature-emoji {
  font-size: 2rem;
}

/* --- Каталог ------------------------------------------------------------ */

.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.filters .field {
  flex: 1 1 200px;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(170px, 1fr));
  gap: 14px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.product-card {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.product-card p {
  margin: 0;
}

.product-card .button {
  margin-top: auto;
}

.product-emoji {
  font-size: 2.6rem;
  line-height: 1.2;
}

.product-name {
  margin: 4px 0 0;
  font-size: 1.05rem;
}

.product-name a {
  color: inherit;
  text-decoration: none;
}

.product-name a:hover {
  text-decoration: underline;
}

.price {
  color: var(--green-dark);
  font-weight: 700;
}

.price.big {
  font-size: 1.5rem;
}

.tag {
  display: inline-block;
  width: fit-content;
  padding: 2px 8px;
  border-radius: 999px;
  background: #fdecea;
  color: var(--danger);
  font-size: 0.8rem;
}

.detail-body {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 24px;
  margin-top: 12px;
}

.detail-body p {
  margin: 0 0 8px;
}

.detail-emoji {
  padding: 16px;
  border-radius: 20px;
  background: var(--green-soft);
  font-size: 6rem;
  line-height: 1;
}

/* --- Форм --------------------------------------------------------------- */

.field {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-bottom: 12px;
}

.field label {
  font-weight: 600;
}

input,
select {
  padding: 9px 10px;
  border: 1px solid #8c959f;
  border-radius: 8px;
  background: #fff;
  font: inherit;
}

[aria-invalid="true"] {
  border-color: var(--danger);
  box-shadow: 0 0 0 1px var(--danger);
}

.error {
  margin: 0;
  color: var(--danger);
  font-size: 0.9rem;
}

.form-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

/* --- Сагс, тооцоо ------------------------------------------------------- */

.cart-list,
.summary-list,
.order-items {
  margin: 0;
  padding: 0;
  list-style: none;
}

.cart-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid var(--border);
}

.cart-emoji {
  font-size: 2rem;
}

.cart-info {
  flex: 1 1 140px;
}

.cart-info p {
  margin: 0;
}

.qty {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.qty button {
  width: 34px;
  height: 34px;
  border: 1px solid #8c959f;
  border-radius: 8px;
  background: #fff;
  font-size: 1.1rem;
  cursor: pointer;
}

.qty-value {
  min-width: 1.5em;
  font-weight: 700;
  text-align: center;
}

.cart-sum {
  min-width: 90px;
  margin: 0;
  font-weight: 700;
  text-align: right;
}

.summary {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-top: 16px;
}

.total {
  margin: 12px 0 0;
  font-size: 1.15rem;
}

.checkout-grid,
.admin-grid {
  display: grid;
  grid-template-columns: minmax(0, 3fr) minmax(0, 2fr);
  gap: 16px;
  align-items: start;
}

.summary-list li,
.order-items li {
  display: flex;
  justify-content: space-between;
  gap: 8px;
  padding: 6px 0;
  border-bottom: 1px dashed var(--border);
}

/* --- Захиалга, админ ---------------------------------------------------- */

.order-list {
  display: grid;
  gap: 12px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.order-head {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.order-head h2,
.order-head h3 {
  margin: 0;
}

.status-pill {
  padding: 2px 10px;
  border-radius: 999px;
  background: var(--green-soft);
  color: var(--green-dark);
  font-size: 0.85rem;
  font-weight: 600;
}

.table-wrap {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

caption {
  padding: 0 0 8px;
  font-weight: 700;
  text-align: left;
}

th,
td {
  padding: 8px 10px;
  border-bottom: 1px solid var(--border);
  text-align: left;
}

@media (max-width: 720px) {
  .checkout-grid,
  .admin-grid {
    grid-template-columns: 1fr;
  }

  .hero h1 {
    font-size: 1.7rem;
  }

  .cart-sum {
    text-align: left;
  }
}
"""

FORMAT_JS = """\
// Мөнгө, огноо, төлвийг нэг хэлбэрээр харуулах туслахууд.

/** 3500 → "3,500₮" */
export function formatPrice(value) {
  return `${Number(value).toLocaleString("en-US")}₮`;
}

/** "2026-09-28T10:00:00.000Z" → "2026-09-28" */
export function formatDate(iso) {
  return String(iso).slice(0, 10);
}

/** Захиалгын төлвийн код → дэлгэцэнд харагдах нэр. */
export const ORDER_STATUS = {
  new: "Шинэ",
  shipping: "Хүргэлтэд",
  delivered: "Хүргэгдсэн",
};
"""

# --- 1. Бүтэц -------------------------------------------------------------------

APP_1_START = """\
import { Route, Routes } from "react-router";
import Layout from "./components/Layout";
import Home from "./pages/Home";
// TODO 3: Products, NotFound хуудсуудыг импортол

export default function App() {
  return (
    <Routes>
      {/* TODO 3: Бүх route-ийг <Route element={<Layout />}> дотор хий:
          index → Home, "products" → Products, "*" → NotFound */}
      <Route path="/" element={<Home />} />
    </Routes>
  );
}
"""

APP_1 = """\
import { Route, Routes } from "react-router";
import Layout from "./components/Layout";
import Home from "./pages/Home";
import NotFound from "./pages/NotFound";
import Products from "./pages/Products";

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="products" element={<Products />} />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}
"""

HEADER_1_START = """\
import { Link } from "react-router";

export default function Header() {
  return (
    <header className="site-header">
      <Link to="/" className="brand">
        <span aria-hidden="true">🥬</span> Ногоон сагс
      </Link>
      {/* TODO 1: <nav aria-label="Үндсэн цэс" className="nav"> дотор
          «Нүүр» (/) ба «Бараа» (/products) гэсэн хоёр NavLink */}
    </header>
  );
}
"""

HEADER_1 = """\
import { Link, NavLink } from "react-router";

export default function Header() {
  return (
    <header className="site-header">
      <Link to="/" className="brand">
        <span aria-hidden="true">🥬</span> Ногоон сагс
      </Link>
      <nav aria-label="Үндсэн цэс" className="nav">
        <NavLink to="/">Нүүр</NavLink>
        <NavLink to="/products">Бараа</NavLink>
      </nav>
    </header>
  );
}
"""

LAYOUT_START = """\
import Header from "./Header";

export default function Layout() {
  // TODO 2: Header-ийн доор <main id="main" className="container" tabIndex={-1}>
  //         дотор <Outlet />, түүний доор <footer className="site-footer"> нэм.
  //         Outlet-ийг "react-router"-оос импортлоорой.
  return (
    <div className="app">
      <a href="#main" className="skip-link">
        Үндсэн агуулга руу алгасах
      </a>
      <Header />
    </div>
  );
}
"""

LAYOUT = """\
import { Outlet } from "react-router";
import Header from "./Header";

export default function Layout() {
  return (
    <div className="app">
      <a href="#main" className="skip-link">
        Үндсэн агуулга руу алгасах
      </a>
      <Header />
      <main id="main" className="container" tabIndex={-1}>
        <Outlet />
      </main>
      <footer className="site-footer">
        <p>© 2026 Ногоон сагс · Шинэхэн хүнс гэрт тань</p>
      </footer>
    </div>
  );
}
"""

HOME = """\
import { Link } from "react-router";

const FEATURES = [
  { emoji: "🚚", title: "Өдөрт нь хүргэнэ", text: "11 цагаас өмнө захиалбал өнөөдөртөө авна." },
  { emoji: "🥕", title: "Шинэхэн", text: "Жимс, ногоогоо өдөр бүр фермерээс шууд авдаг." },
  { emoji: "💳", title: "Хялбар төлбөр", text: "Картаар эсвэл хүргэлтийн үед бэлнээр." },
];

export default function Home() {
  return (
    <>
      <section className="hero">
        <p className="eyebrow">Онлайн хүнсний дэлгүүр</p>
        <h1>Ногоон сагс</h1>
        <p className="lead">Шинэ жимс, ногоо, сүүн бүтээгдэхүүнээ гэрээсээ захиалаарай.</p>
        <Link to="/products" className="button">
          Бараа үзэх
        </Link>
      </section>
      <ul className="features">
        {FEATURES.map((feature) => (
          <li key={feature.title} className="card">
            <span className="feature-emoji" aria-hidden="true">
              {feature.emoji}
            </span>
            <h2>{feature.title}</h2>
            <p className="muted">{feature.text}</p>
          </li>
        ))}
      </ul>
    </>
  );
}
"""

PRODUCTS_PLACEHOLDER = """\
export default function Products() {
  return (
    <section>
      <h1>Бараа</h1>
      <p className="muted">Каталогийг дараагийн хичээлд серверээс татаж бүтээнэ.</p>
    </section>
  );
}
"""

NOT_FOUND_START = """\
import { Link } from "react-router";

export default function NotFound() {
  // TODO 4: h1 «Хуудас олдсонгүй», тайлбар, нүүр рүү буцах Link
  return null;
}
"""

NOT_FOUND = """\
import { Link } from "react-router";

export default function NotFound() {
  return (
    <section className="panel empty">
      <p className="big-emoji" aria-hidden="true">
        🧺
      </p>
      <h1>Хуудас олдсонгүй</h1>
      <p className="muted">Таны хайсан хуудас байхгүй эсвэл зөөгдсөн байна.</p>
      <Link to="/" className="button">
        Нүүр хуудас руу буцах
      </Link>
    </section>
  );
}
"""

# --- 2. Каталог -----------------------------------------------------------------

API_BASE = """\
// «Ногоон сагс»-ийн сервертэй харилцах функцууд. Хуудсууд fetch-ийг шууд
// дуудахгүй — эндээс импортолно. Хаяг, алдааны шалгалт нэг газарт.

export class ApiError extends Error {
  constructor(status, message) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

export async function request(path, options = {}) {
  const response = await fetch(path, {
    ...options,
    headers: { "Content-Type": "application/json", ...options.headers },
  });
  if (!response.ok) {
    const message = response.status === 404 ? "Олдсонгүй" : "Сервертэй холбогдоход алдаа гарлаа";
    throw new ApiError(response.status, message);
  }
  return response.json();
}

/** GET /api/products → [{ id, name, price, category, emoji, stock }] */
export function getProducts() {
  return request("/api/products");
}
"""

API_2 = API_BASE

API_3 = (
    API_2
    + """
/** GET /api/products/:id → нэг бараа, байхгүй бол 404 (ApiError) */
export function getProduct(id) {
  return request(`/api/products/${id}`);
}
"""
)

PRODUCT_CARD_START = """\
import { Link } from "react-router";
import { formatPrice } from "../format";

export default function ProductCard({ product }) {
  // TODO 1: <li className="card product-card"> дотор:
  //   - emoji: <span className="product-emoji" aria-hidden="true">
  //   - <h2 className="product-name"> дотор /products/:id руу Link (текст нь нэр)
  //   - ангилал (className="muted"), үнэ formatPrice-ээр (className="price")
  //   - stock === 0 бол <p className="tag">Дууссан</p>
  return <li className="card product-card">{product.name}</li>;
}
"""

PRODUCT_CARD_2 = """\
import { Link } from "react-router";
import { formatPrice } from "../format";

export default function ProductCard({ product }) {
  return (
    <li className="card product-card">
      <span className="product-emoji" aria-hidden="true">
        {product.emoji}
      </span>
      <h2 className="product-name">
        <Link to={`/products/${product.id}`}>{product.name}</Link>
      </h2>
      <p className="muted">{product.category}</p>
      <p className="price">{formatPrice(product.price)}</p>
      {product.stock === 0 && <p className="tag">Дууссан</p>}
    </li>
  );
}
"""

PRODUCTS_2_START = """\
import { useQuery } from "@tanstack/react-query";
import { getProducts } from "../api";
import ProductCard from "../components/ProductCard";

export default function Products() {
  // TODO 2: useQuery({ queryKey: ["products"], queryFn: getProducts })-оос
  //         data, isPending, isError, refetch-ийг ав.

  return (
    <section>
      <h1>Бараа</h1>
      {/* TODO 3: isPending үед <p role="status" className="status">Ачаалж байна…</p> */}
      {/* TODO 4: isError үед <div className="alert"> дотор <p role="alert">
          мессеж ба refetch() дууддаг «Дахин оролдох» товч */}
      {/* TODO 5: бараа бүрийг <ul className="product-grid"> дотор <ProductCard>-аар */}
    </section>
  );
}
"""

PRODUCTS_2 = """\
import { useQuery } from "@tanstack/react-query";
import { getProducts } from "../api";
import ProductCard from "../components/ProductCard";

export default function Products() {
  const {
    data: products,
    isPending,
    isError,
    refetch,
  } = useQuery({ queryKey: ["products"], queryFn: getProducts });

  return (
    <section>
      <h1>Бараа</h1>
      {isPending && (
        <p role="status" className="status">
          Ачаалж байна…
        </p>
      )}
      {isError && (
        <div className="alert">
          <p role="alert">Бараа ачаалж чадсангүй. Холболтоо шалгаад дахин оролдоно уу.</p>
          <button type="button" className="button" onClick={() => refetch()}>
            Дахин оролдох
          </button>
        </div>
      )}
      {products && (
        <ul className="product-grid">
          {products.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </ul>
      )}
    </section>
  );
}
"""

# --- 3. Дэлгэрэнгүй -------------------------------------------------------------

APP_3_START = """\
import { Route, Routes } from "react-router";
import Layout from "./components/Layout";
import Home from "./pages/Home";
import NotFound from "./pages/NotFound";
import Products from "./pages/Products";
// TODO 1: ProductDetail-ийг импортол

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="products" element={<Products />} />
        {/* TODO 1: "products/:id" → ProductDetail */}
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}
"""

APP_3 = """\
import { Route, Routes } from "react-router";
import Layout from "./components/Layout";
import Home from "./pages/Home";
import NotFound from "./pages/NotFound";
import ProductDetail from "./pages/ProductDetail";
import Products from "./pages/Products";

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="products" element={<Products />} />
        <Route path="products/:id" element={<ProductDetail />} />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}
"""

DETAIL_3_START = """\
import { useQuery } from "@tanstack/react-query";
import { Link, useNavigate, useParams } from "react-router";
import { getProduct } from "../api";
import { formatPrice } from "../format";

export default function ProductDetail() {
  // TODO 2: useParams()-аас id-г ав.
  // TODO 3: useQuery({ queryKey: ["products", id], queryFn: () => getProduct(id) })
  // TODO 4: ачаалах үед role="status"; error.status === 404 бол «Бараа олдсонгүй»
  //         ба /products руу холбоос; бусад алдаанд role="alert".
  // TODO 5: <title>, «← Буцах» товч (navigate(-1)), emoji, ангилал, h1 нэр,
  //         үнэ, «Үлдэгдэл: N ширхэг» эсвэл «Дууссан».
  return <p className="muted">TODO: барааны дэлгэрэнгүй</p>;
}
"""

DETAIL_3 = """\
import { useQuery } from "@tanstack/react-query";
import { Link, useNavigate, useParams } from "react-router";
import { getProduct } from "../api";
import { formatPrice } from "../format";

export default function ProductDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const {
    data: product,
    isPending,
    error,
  } = useQuery({ queryKey: ["products", id], queryFn: () => getProduct(id) });

  if (isPending) {
    return (
      <p role="status" className="status">
        Ачаалж байна…
      </p>
    );
  }

  if (error?.status === 404) {
    return (
      <section className="panel empty">
        <title>Бараа олдсонгүй — Ногоон сагс</title>
        <h1>Бараа олдсонгүй</h1>
        <p className="muted">Ийм бараа манай дэлгүүрт байхгүй байна.</p>
        <Link to="/products" className="button">
          Бүх бараа
        </Link>
      </section>
    );
  }

  if (error) {
    return (
      <p role="alert" className="alert">
        Бараа ачаалж чадсангүй. Дахин оролдоно уу.
      </p>
    );
  }

  return (
    <article className="panel">
      <title>{`${product.name} — Ногоон сагс`}</title>
      <button type="button" className="link-button" onClick={() => navigate(-1)}>
        ← Буцах
      </button>
      <div className="detail-body">
        <span className="detail-emoji" aria-hidden="true">
          {product.emoji}
        </span>
        <div>
          <p className="muted">{product.category}</p>
          <h1>{product.name}</h1>
          <p className="price big">{formatPrice(product.price)}</p>
          <p>{product.stock === 0 ? "Дууссан" : `Үлдэгдэл: ${product.stock} ширхэг`}</p>
        </div>
      </div>
    </article>
  );
}
"""

# --- 4. Хайлт ба шүүлтүүр -------------------------------------------------------

PRODUCTS_4_START = patch(
    PRODUCTS_2,
    (
        'import ProductCard from "../components/ProductCard";\n',
        'import ProductCard from "../components/ProductCard";\n'
        "\n"
        "// TODO: «Заавар»-ын шаардлагын дагуу хайлт ба ангиллын шүүлтүүр нэм.\n"
        "//       Утгууд нь URL-д хадгалагдана: /products?q=алим&category=Жимс\n",
    ),
)

PRODUCTS_4 = """\
import { useQuery } from "@tanstack/react-query";
import { useSearchParams } from "react-router";
import { getProducts } from "../api";
import ProductCard from "../components/ProductCard";

export default function Products() {
  const [searchParams, setSearchParams] = useSearchParams();
  const query = searchParams.get("q") ?? "";
  const category = searchParams.get("category") ?? "";

  const {
    data: products,
    isPending,
    isError,
    refetch,
  } = useQuery({ queryKey: ["products"], queryFn: getProducts });

  function updateFilter(name, value) {
    const next = new URLSearchParams(searchParams);
    if (value) {
      next.set(name, value);
    } else {
      next.delete(name);
    }
    setSearchParams(next, { replace: true });
  }

  const categories = [...new Set((products ?? []).map((product) => product.category))];
  const needle = query.trim().toLowerCase();
  const visible = (products ?? []).filter(
    (product) =>
      product.name.toLowerCase().includes(needle) &&
      (category === "" || product.category === category),
  );

  return (
    <section>
      <title>Бараа — Ногоон сагс</title>
      <h1>Бараа</h1>
      <form role="search" className="filters" onSubmit={(event) => event.preventDefault()}>
        <div className="field">
          <label htmlFor="search">Хайх</label>
          <input
            id="search"
            type="search"
            placeholder="Жишээ нь: алим"
            value={query}
            onChange={(event) => updateFilter("q", event.target.value)}
          />
        </div>
        <div className="field">
          <label htmlFor="category">Ангилал</label>
          <select
            id="category"
            value={category}
            onChange={(event) => updateFilter("category", event.target.value)}
          >
            <option value="">Бүгд</option>
            {categories.map((name) => (
              <option key={name} value={name}>
                {name}
              </option>
            ))}
          </select>
        </div>
      </form>
      {isPending && (
        <p role="status" className="status">
          Ачаалж байна…
        </p>
      )}
      {isError && (
        <div className="alert">
          <p role="alert">Бараа ачаалж чадсангүй. Холболтоо шалгаад дахин оролдоно уу.</p>
          <button type="button" className="button" onClick={() => refetch()}>
            Дахин оролдох
          </button>
        </div>
      )}
      {products && (
        <>
          <p role="status" className="muted">
            {visible.length} бараа олдлоо
          </p>
          {visible.length === 0 ? (
            <p className="panel empty">Тохирох бараа олдсонгүй. Өөр үгээр хайгаад үзээрэй.</p>
          ) : (
            <ul className="product-grid">
              {visible.map((product) => (
                <ProductCard key={product.id} product={product} />
              ))}
            </ul>
          )}
        </>
      )}
    </section>
  );
}
"""

# --- 5. Сагс --------------------------------------------------------------------

CART_CONTEXT_START = """\
import { createContext, useContext, useReducer } from "react";

const CartContext = createContext(null);

// Сагсны нэг мөр: { id, name, price, emoji, quantity }
export function cartReducer(items, action) {
  switch (action.type) {
    case "add":
      // TODO 1: action.product сагсанд байвал quantity-г нь 1-ээр нэмэгдүүл,
      //         байхгүй бол { id, name, price, emoji, quantity: 1 }-ийг төгсгөлд
      //         нь нэм. Массив, объектыг ӨӨРЧЛӨХГҮЙ — шинээр үүсгэ.
      return items;
    case "remove":
      // TODO 2: action.id-тай мөрийг хас.
      return items;
    case "setQuantity":
      // TODO 3: action.id-тай мөрийн quantity-г action.quantity болго.
      //         0 буюу түүнээс бага бол мөрийг хас.
      return items;
    case "clear":
      return [];
    default:
      throw new Error(`Үл мэдэгдэх үйлдэл: ${action.type}`);
  }
}

export function CartProvider({ children }) {
  const [items, dispatch] = useReducer(cartReducer, []);

  // TODO 4: count — нийт ширхэг, total — нийт үнэ (price × quantity).
  //         Хоёуланг нь items-ээс reduce-ээр тооцоол.
  const count = 0;
  const total = 0;

  const value = {
    items,
    count,
    total,
    add: (product) => dispatch({ type: "add", product }),
    remove: (id) => dispatch({ type: "remove", id }),
    setQuantity: (id, quantity) => dispatch({ type: "setQuantity", id, quantity }),
    clear: () => dispatch({ type: "clear" }),
  };

  return <CartContext value={value}>{children}</CartContext>;
}

export function useCart() {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error("useCart-ийг <CartProvider> дотор дуудна уу.");
  }
  return context;
}
"""

CART_CONTEXT_5 = """\
import { createContext, useContext, useReducer } from "react";

const CartContext = createContext(null);

// Сагсны нэг мөр: { id, name, price, emoji, quantity }
export function cartReducer(items, action) {
  switch (action.type) {
    case "add": {
      const { id, name, price, emoji } = action.product;
      const existing = items.find((item) => item.id === id);
      if (existing) {
        return items.map((item) =>
          item.id === id ? { ...item, quantity: item.quantity + 1 } : item,
        );
      }
      return [...items, { id, name, price, emoji, quantity: 1 }];
    }
    case "remove":
      return items.filter((item) => item.id !== action.id);
    case "setQuantity":
      if (action.quantity <= 0) {
        return items.filter((item) => item.id !== action.id);
      }
      return items.map((item) =>
        item.id === action.id ? { ...item, quantity: action.quantity } : item,
      );
    case "clear":
      return [];
    default:
      throw new Error(`Үл мэдэгдэх үйлдэл: ${action.type}`);
  }
}

export function CartProvider({ children }) {
  const [items, dispatch] = useReducer(cartReducer, []);

  const count = items.reduce((sum, item) => sum + item.quantity, 0);
  const total = items.reduce((sum, item) => sum + item.price * item.quantity, 0);

  const value = {
    items,
    count,
    total,
    add: (product) => dispatch({ type: "add", product }),
    remove: (id) => dispatch({ type: "remove", id }),
    setQuantity: (id, quantity) => dispatch({ type: "setQuantity", id, quantity }),
    clear: () => dispatch({ type: "clear" }),
  };

  return <CartContext value={value}>{children}</CartContext>;
}

export function useCart() {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error("useCart-ийг <CartProvider> дотор дуудна уу.");
  }
  return context;
}
"""

APP_5_START = patch(
    APP_3,
    (
        'import Products from "./pages/Products";\n',
        'import Products from "./pages/Products";\n'
        "// TODO 5: CartProvider (./context/CartContext) ба Cart хуудсыг импортол\n",
    ),
    (
        "export default function App() {\n",
        "export default function App() {\n"
        '  // TODO 5: <Routes>-ийг <CartProvider>-оор ороож, "cart" → Cart route нэм.\n',
    ),
)

APP_5 = """\
import { Route, Routes } from "react-router";
import Layout from "./components/Layout";
import { CartProvider } from "./context/CartContext";
import Cart from "./pages/Cart";
import Home from "./pages/Home";
import NotFound from "./pages/NotFound";
import ProductDetail from "./pages/ProductDetail";
import Products from "./pages/Products";

export default function App() {
  return (
    <CartProvider>
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="products" element={<Products />} />
          <Route path="products/:id" element={<ProductDetail />} />
          <Route path="cart" element={<Cart />} />
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </CartProvider>
  );
}
"""

HEADER_5_START = patch(
    HEADER_1,
    (
        'import { Link, NavLink } from "react-router";\n',
        'import { Link, NavLink } from "react-router";\n// TODO 6: useCart-ийг импортол\n',
    ),
    (
        "export default function Header() {\n",
        "export default function Header() {\n  // TODO 6: const { count } = useCart();\n",
    ),
    (
        "      </nav>\n",
        "      </nav>\n"
        '      {/* TODO 6: <div className="header-actions"> дотор /cart руу NavLink:\n'
        '          <span aria-hidden="true">🛒</span> Сагс <span className="badge">{count}</span> */}\n',
    ),
)

HEADER_5 = """\
import { Link, NavLink } from "react-router";
import { useCart } from "../context/CartContext";

export default function Header() {
  const { count } = useCart();

  return (
    <header className="site-header">
      <Link to="/" className="brand">
        <span aria-hidden="true">🥬</span> Ногоон сагс
      </Link>
      <nav aria-label="Үндсэн цэс" className="nav">
        <NavLink to="/">Нүүр</NavLink>
        <NavLink to="/products">Бараа</NavLink>
      </nav>
      <div className="header-actions">
        <NavLink to="/cart">
          <span aria-hidden="true">🛒</span> Сагс <span className="badge">{count}</span>
          <span className="sr-only"> бараа</span>
        </NavLink>
      </div>
    </header>
  );
}
"""

PRODUCT_CARD_5_START = patch(
    PRODUCT_CARD_2,
    (
        'import { formatPrice } from "../format";\n',
        'import { formatPrice } from "../format";\n// TODO 7: useCart-ийг импортол\n',
    ),
    (
        "export default function ProductCard({ product }) {\n",
        "export default function ProductCard({ product }) {\n"
        "  // TODO 7: const { add } = useCart();\n",
    ),
    (
        '      {product.stock === 0 && <p className="tag">Дууссан</p>}\n',
        '      {product.stock === 0 && <p className="tag">Дууссан</p>}\n'
        '      {/* TODO 7: className="button" «Сагсанд нэмэх» товч: onClick={() => add(product)},\n'
        "          stock === 0 бол disabled, aria-label={`Сагсанд нэмэх: ${product.name}`} */}\n",
    ),
)

PRODUCT_CARD_5 = """\
import { Link } from "react-router";
import { useCart } from "../context/CartContext";
import { formatPrice } from "../format";

export default function ProductCard({ product }) {
  const { add } = useCart();
  const soldOut = product.stock === 0;

  return (
    <li className="card product-card">
      <span className="product-emoji" aria-hidden="true">
        {product.emoji}
      </span>
      <h2 className="product-name">
        <Link to={`/products/${product.id}`}>{product.name}</Link>
      </h2>
      <p className="muted">{product.category}</p>
      <p className="price">{formatPrice(product.price)}</p>
      {soldOut && <p className="tag">Дууссан</p>}
      <button
        type="button"
        className="button"
        disabled={soldOut}
        aria-label={`Сагсанд нэмэх: ${product.name}`}
        onClick={() => add(product)}
      >
        Сагсанд нэмэх
      </button>
    </li>
  );
}
"""

DETAIL_STOCK_LINE = (
    '          <p>{product.stock === 0 ? "Дууссан" : `Үлдэгдэл: ${product.stock} ширхэг`}</p>\n'
)

DETAIL_5_START = patch(
    DETAIL_3,
    (
        'import { formatPrice } from "../format";\n',
        'import { formatPrice } from "../format";\n// TODO 7: useCart-ийг импортол\n',
    ),
    (
        "  const navigate = useNavigate();\n",
        "  const navigate = useNavigate();\n"
        "  // TODO 7: const { add } = useCart(); — hook-ийг early return-оос ӨМНӨ дууд\n",
    ),
    (
        DETAIL_STOCK_LINE,
        DETAIL_STOCK_LINE
        + '          {/* TODO 7: className="button" «Сагсанд нэмэх» товч, stock 0 бол disabled */}\n',
    ),
)

DETAIL_5 = patch(
    DETAIL_3,
    (
        'import { getProduct } from "../api";\n',
        'import { getProduct } from "../api";\nimport { useCart } from "../context/CartContext";\n',
    ),
    (
        "  const navigate = useNavigate();\n",
        "  const navigate = useNavigate();\n  const { add } = useCart();\n",
    ),
    (
        DETAIL_STOCK_LINE,
        DETAIL_STOCK_LINE
        + """\
          <button
            type="button"
            className="button"
            disabled={product.stock === 0}
            onClick={() => add(product)}
          >
            Сагсанд нэмэх
          </button>
""",
    ),
)

CART_5_START = """\
import { Link } from "react-router";
import { formatPrice } from "../format";
// TODO 8: useCart-ийг импортол

export default function Cart() {
  // TODO 8: items, total, setQuantity, remove-ийг useCart()-аас ав
  //         (доорх хоёр мөрийг устга).
  const items = [];
  const total = 0;

  if (items.length === 0) {
    return (
      <section className="panel empty">
        <p className="big-emoji" aria-hidden="true">
          🛒
        </p>
        <h1>Сагс</h1>
        <p>Сагс хоосон байна.</p>
        <Link to="/products" className="button">
          Бараа үзэх
        </Link>
      </section>
    );
  }

  return (
    <section className="panel">
      <h1>Сагс</h1>
      <ul className="cart-list">
        {items.map((item) => (
          <li key={item.id} className="cart-row">
            <span className="cart-emoji" aria-hidden="true">
              {item.emoji}
            </span>
            <div className="cart-info">
              <p>{item.name}</p>
              <p className="muted">{formatPrice(item.price)} / ширхэг</p>
            </div>
            <div className="qty">
              {/* TODO 8: onClick — тоог 1-ээр хасах */}
              <button type="button" aria-label={`${item.name}: хасах`}>
                −
              </button>
              <span className="qty-value">{item.quantity}</span>
              {/* TODO 8: onClick — тоог 1-ээр нэмэх */}
              <button type="button" aria-label={`${item.name}: нэмэх`}>
                +
              </button>
            </div>
            <p className="cart-sum">{formatPrice(item.price * item.quantity)}</p>
            {/* TODO 8: onClick — мөрийг устгах */}
            <button type="button" className="link-button danger" aria-label={`${item.name}: устгах`}>
              Устгах
            </button>
          </li>
        ))}
      </ul>
      <div className="summary">
        <p className="total">
          Нийт: <strong>{formatPrice(total)}</strong>
        </p>
        <Link to="/checkout" className="button">
          Тооцоо хийх
        </Link>
      </div>
    </section>
  );
}
"""

CART_5 = """\
import { Link } from "react-router";
import { useCart } from "../context/CartContext";
import { formatPrice } from "../format";

export default function Cart() {
  const { items, total, setQuantity, remove } = useCart();

  if (items.length === 0) {
    return (
      <section className="panel empty">
        <title>Сагс — Ногоон сагс</title>
        <p className="big-emoji" aria-hidden="true">
          🛒
        </p>
        <h1>Сагс</h1>
        <p>Сагс хоосон байна.</p>
        <Link to="/products" className="button">
          Бараа үзэх
        </Link>
      </section>
    );
  }

  return (
    <section className="panel">
      <title>Сагс — Ногоон сагс</title>
      <h1>Сагс</h1>
      <ul className="cart-list">
        {items.map((item) => (
          <li key={item.id} className="cart-row">
            <span className="cart-emoji" aria-hidden="true">
              {item.emoji}
            </span>
            <div className="cart-info">
              <p>{item.name}</p>
              <p className="muted">{formatPrice(item.price)} / ширхэг</p>
            </div>
            <div className="qty">
              <button
                type="button"
                aria-label={`${item.name}: хасах`}
                onClick={() => setQuantity(item.id, item.quantity - 1)}
              >
                −
              </button>
              <span className="qty-value">{item.quantity}</span>
              <button
                type="button"
                aria-label={`${item.name}: нэмэх`}
                onClick={() => setQuantity(item.id, item.quantity + 1)}
              >
                +
              </button>
            </div>
            <p className="cart-sum">{formatPrice(item.price * item.quantity)}</p>
            <button
              type="button"
              className="link-button danger"
              aria-label={`${item.name}: устгах`}
              onClick={() => remove(item.id)}
            >
              Устгах
            </button>
          </li>
        ))}
      </ul>
      <div className="summary">
        <p className="total">
          Нийт: <strong>{formatPrice(total)}</strong>
        </p>
        <Link to="/checkout" className="button">
          Тооцоо хийх
        </Link>
      </div>
    </section>
  );
}
"""

# JS тестийн туслах: толгой дахь сагсны холбоос.
CART_LINK_JS = """\
const cartLink = () =>
  within(screen.getByRole("banner"))
    .getAllByRole("link")
    .find((link) => link.getAttribute("href") === "/cart");
"""

# --- 6. Төлбөр тооцоо -----------------------------------------------------------

API_6_START = (
    API_3
    + """
// TODO: createOrder(order) — POST /api/orders («Заавар»-ын «API» хэсгийг үз).
"""
)

API_6 = (
    API_3
    + """
/** POST /api/orders → 201 { id, ...order } */
export function createOrder(order) {
  return request("/api/orders", { method: "POST", body: JSON.stringify(order) });
}
"""
)

APP_6_START = patch(
    APP_5,
    (
        'import Products from "./pages/Products";\n',
        'import Products from "./pages/Products";\n'
        "// TODO: Checkout, OrderSuccess хуудсуудыг импортлож route-уудыг нь нэм\n",
    ),
)

APP_6 = """\
import { Route, Routes } from "react-router";
import Layout from "./components/Layout";
import { CartProvider } from "./context/CartContext";
import Cart from "./pages/Cart";
import Checkout from "./pages/Checkout";
import Home from "./pages/Home";
import NotFound from "./pages/NotFound";
import OrderSuccess from "./pages/OrderSuccess";
import ProductDetail from "./pages/ProductDetail";
import Products from "./pages/Products";

export default function App() {
  return (
    <CartProvider>
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="products" element={<Products />} />
          <Route path="products/:id" element={<ProductDetail />} />
          <Route path="cart" element={<Cart />} />
          <Route path="checkout" element={<Checkout />} />
          <Route path="checkout/success" element={<OrderSuccess />} />
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </CartProvider>
  );
}
"""

CHECKOUT_START = """\
// /checkout — «Заавар»-ын шаардлага, дизайн, API-ийн дагуу бүтээ.
// Хэрэгтэй зүйлс: useCart() (items, total, clear), createOrder (../api),
// useMutation, useQueryClient (@tanstack/react-query), useNavigate, formatPrice.

export default function Checkout() {
  return (
    <section>
      <h1>Тооцоо хийх</h1>
    </section>
  );
}
"""

CHECKOUT_6 = """\
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { Link, useNavigate } from "react-router";
import { createOrder } from "../api";
import { useCart } from "../context/CartContext";
import { formatPrice } from "../format";

const FIELDS = [
  { name: "name", label: "Нэр", type: "text", autoComplete: "name" },
  { name: "phone", label: "Утас", type: "tel", autoComplete: "tel" },
  { name: "email", label: "Имэйл", type: "email", autoComplete: "email" },
  { name: "address", label: "Хүргэлтийн хаяг", type: "text", autoComplete: "street-address" },
];

const EMPTY = { name: "", phone: "", email: "", address: "" };

function validate(values) {
  const errors = {};
  if (values.name.trim().length < 2) {
    errors.name = "Нэрээ оруулна уу";
  }
  if (!/^[0-9]{8}$/.test(values.phone.trim())) {
    errors.phone = "Утасны дугаар 8 оронтой тоо байна";
  }
  if (!/^[^@ ]+@[^@ ]+[.][^@ ]+$/.test(values.email.trim())) {
    errors.email = "Имэйлээ зөв оруулна уу";
  }
  if (values.address.trim().length < 5) {
    errors.address = "Хүргэлтийн хаягаа дэлгэрэнгүй бичнэ үү";
  }
  return errors;
}

export default function Checkout() {
  const { items, total, clear } = useCart();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [values, setValues] = useState(EMPTY);
  const [submitted, setSubmitted] = useState(false);
  const errors = validate(values);

  const placeOrder = useMutation({
    mutationFn: createOrder,
    onSuccess: (order) => {
      queryClient.invalidateQueries({ queryKey: ["orders"] });
      clear();
      navigate("/checkout/success", { replace: true, state: { orderId: order.id } });
    },
  });

  function handleChange(event) {
    setValues({ ...values, [event.target.name]: event.target.value });
  }

  function handleSubmit(event) {
    event.preventDefault();
    setSubmitted(true);
    const invalid = FIELDS.find((field) => errors[field.name]);
    if (invalid) {
      event.currentTarget.elements.namedItem(invalid.name).focus();
      return;
    }
    placeOrder.mutate({
      email: values.email.trim(),
      customer: {
        name: values.name.trim(),
        phone: values.phone.trim(),
        address: values.address.trim(),
      },
      items: items.map(({ id, name, price, emoji, quantity }) => ({
        productId: id,
        name,
        price,
        emoji,
        quantity,
      })),
      total,
      status: "new",
      createdAt: new Date().toISOString(),
    });
  }

  if (items.length === 0) {
    return (
      <section className="panel empty">
        <title>Тооцоо — Ногоон сагс</title>
        <h1>Тооцоо хийх</h1>
        <p>Сагс хоосон байна.</p>
        <Link to="/products" className="button">
          Бараа үзэх
        </Link>
      </section>
    );
  }

  return (
    <section>
      <title>Тооцоо — Ногоон сагс</title>
      <h1>Тооцоо хийх</h1>
      <div className="checkout-grid">
        <form className="panel" onSubmit={handleSubmit} noValidate aria-labelledby="delivery-title">
          <h2 id="delivery-title">Хүргэлтийн мэдээлэл</h2>
          {FIELDS.map((field) => {
            const id = `checkout-${field.name}`;
            const error = submitted ? errors[field.name] : undefined;
            return (
              <div className="field" key={field.name}>
                <label htmlFor={id}>{field.label}</label>
                <input
                  id={id}
                  name={field.name}
                  type={field.type}
                  autoComplete={field.autoComplete}
                  value={values[field.name]}
                  onChange={handleChange}
                  required
                  aria-invalid={error ? true : undefined}
                  aria-describedby={error ? `${id}-error` : undefined}
                />
                {error && (
                  <p id={`${id}-error`} className="error" role="alert">
                    {error}
                  </p>
                )}
              </div>
            );
          })}
          {placeOrder.isError && (
            <p className="alert" role="alert">
              Захиалга илгээж чадсангүй. Дахин оролдоно уу.
            </p>
          )}
          <button type="submit" className="button" disabled={placeOrder.isPending}>
            {placeOrder.isPending ? "Илгээж байна…" : "Захиалах"}
          </button>
        </form>
        <aside className="panel" aria-labelledby="summary-title">
          <h2 id="summary-title">Таны захиалга</h2>
          <ul className="summary-list">
            {items.map((item) => (
              <li key={item.id}>
                <span>
                  <span aria-hidden="true">{item.emoji}</span> {item.name} × {item.quantity}
                </span>
                <span>{formatPrice(item.price * item.quantity)}</span>
              </li>
            ))}
          </ul>
          <p className="total">
            Нийт: <strong>{formatPrice(total)}</strong>
          </p>
        </aside>
      </div>
    </section>
  );
}
"""

ORDER_SUCCESS_START = """\
// /checkout/success — захиалга амжилттай болсны дараах хуудас.

export default function OrderSuccess() {
  return (
    <section className="panel empty">
      <h1>Захиалга амжилттай!</h1>
    </section>
  );
}
"""

ORDER_SUCCESS_6 = """\
import { Link, useLocation } from "react-router";

export default function OrderSuccess() {
  const { state } = useLocation();

  return (
    <section className="panel empty">
      <title>Захиалга баталгаажлаа — Ногоон сагс</title>
      <p className="big-emoji" aria-hidden="true">
        🎉
      </p>
      <h1>Захиалга амжилттай!</h1>
      {state?.orderId && (
        <p>
          Захиалгын дугаар: <strong>#{state.orderId}</strong>
        </p>
      )}
      <p className="muted">Бид удахгүй тантай холбогдож хүргэлтийн цагийг тохирно.</p>
      <Link to="/products" className="button">
        Дэлгүүр хэсэх
      </Link>
    </section>
  );
}
"""

# JS тестийн туслахууд: Банана × 2-ыг сагсалж, тооцооны хуудас руу орно; формыг бөглөнө.
CHECKOUT_SETUP_JS = (
    CART_LINK_JS
    + """
setPath("/products/1");
await runMain();
const addButton = await screen.findByRole("button", { name: /Сагсанд нэмэх/ });
await user.click(addButton);
await user.click(addButton);
await user.click(cartLink());
await user.click(await screen.findByRole("link", { name: /Тооцоо хийх/ }));
"""
)

CHECKOUT_FILL_JS = """
await user.type(await screen.findByLabelText("Нэр"), "Сараа");
await user.type(screen.getByLabelText("Утас"), "99112233");
await user.type(screen.getByLabelText("Имэйл"), "saraa@example.mn");
await user.type(screen.getByLabelText("Хүргэлтийн хаяг"), "СБД, 1-р хороо, 5-р байр");
"""

# --- 7. Нэвтрэлт ----------------------------------------------------------------

API_7_START = (
    API_6
    + """
// TODO: getOrders(email) — GET /api/orders?email=… (имэйлийг encodeURIComponent-оор).
"""
)

API_7 = (
    API_6
    + """
/** GET /api/orders?email=… → тухайн хэрэглэгчийн захиалгууд */
export function getOrders(email) {
  return request(`/api/orders?email=${encodeURIComponent(email)}`);
}
"""
)

APP_7_START = patch(
    APP_6,
    (
        'import Products from "./pages/Products";\n',
        'import Products from "./pages/Products";\n'
        "// TODO: AuthProvider-оор ороож, /login ба хамгаалагдсан /profile route нэм\n",
    ),
)

APP_7 = """\
import { Route, Routes } from "react-router";
import Layout from "./components/Layout";
import ProtectedRoute from "./components/ProtectedRoute";
import { AuthProvider } from "./context/AuthContext";
import { CartProvider } from "./context/CartContext";
import Cart from "./pages/Cart";
import Checkout from "./pages/Checkout";
import Home from "./pages/Home";
import Login from "./pages/Login";
import NotFound from "./pages/NotFound";
import OrderSuccess from "./pages/OrderSuccess";
import ProductDetail from "./pages/ProductDetail";
import Products from "./pages/Products";
import Profile from "./pages/Profile";

export default function App() {
  return (
    <AuthProvider>
      <CartProvider>
        <Routes>
          <Route element={<Layout />}>
            <Route index element={<Home />} />
            <Route path="products" element={<Products />} />
            <Route path="products/:id" element={<ProductDetail />} />
            <Route path="cart" element={<Cart />} />
            <Route path="checkout" element={<Checkout />} />
            <Route path="checkout/success" element={<OrderSuccess />} />
            <Route path="login" element={<Login />} />
            <Route element={<ProtectedRoute />}>
              <Route path="profile" element={<Profile />} />
            </Route>
            <Route path="*" element={<NotFound />} />
          </Route>
        </Routes>
      </CartProvider>
    </AuthProvider>
  );
}
"""

HEADER_7_START = patch(
    HEADER_5,
    (
        "  const { count } = useCart();\n",
        "  const { count } = useCart();\n"
        "  // TODO: нэвтрээгүй бол «Нэвтрэх» холбоос, нэвтэрсэн бол «Профайл» холбоос\n"
        "  //       ба «Гарах» товч (header-actions дотор)\n",
    ),
)

HEADER_7 = """\
import { Link, NavLink } from "react-router";
import { useAuth } from "../context/AuthContext";
import { useCart } from "../context/CartContext";

export default function Header() {
  const { count } = useCart();
  const { user, logout } = useAuth();

  return (
    <header className="site-header">
      <Link to="/" className="brand">
        <span aria-hidden="true">🥬</span> Ногоон сагс
      </Link>
      <nav aria-label="Үндсэн цэс" className="nav">
        <NavLink to="/">Нүүр</NavLink>
        <NavLink to="/products">Бараа</NavLink>
      </nav>
      <div className="header-actions">
        <NavLink to="/cart">
          <span aria-hidden="true">🛒</span> Сагс <span className="badge">{count}</span>
          <span className="sr-only"> бараа</span>
        </NavLink>
        {user ? (
          <>
            <NavLink to="/profile">Профайл</NavLink>
            <button type="button" className="link-button" onClick={logout}>
              Гарах
            </button>
          </>
        ) : (
          <NavLink to="/login">Нэвтрэх</NavLink>
        )}
      </div>
    </header>
  );
}
"""

AUTH_CONTEXT_START = """\
// ⚠️ ДАДЛАГЫН, ХУУРАМЧ нэвтрэлт. Бодит апп нууц үгийг хөтөч дээр хэзээ ч
// шалгадаггүй — серверт илгээж, сервер session эсвэл токен буцаадаг.
export const DEMO_PASSWORD = "nogoon123";
export const ADMIN_EMAIL = "admin@nogoon.mn";

// TODO: AuthContext, AuthProvider, useAuth — «Заавар»-ын «AuthContext-ийн API»-г үз.
"""

AUTH_CONTEXT_7 = """\
import { createContext, useContext, useState } from "react";

// ⚠️ ДАДЛАГЫН, ХУУРАМЧ нэвтрэлт. Бодит апп нууц үгийг хөтөч дээр хэзээ ч
// шалгадаггүй — серверт илгээж, сервер session эсвэл токен буцаадаг.
export const DEMO_PASSWORD = "nogoon123";
export const ADMIN_EMAIL = "admin@nogoon.mn";

const STORAGE_KEY = "nogoon-user";
const AuthContext = createContext(null);

function loadUser() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY));
  } catch {
    return null;
  }
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(loadUser);

  function login(email, password) {
    const normalized = email.trim().toLowerCase();
    if (!/^[^@ ]+@[^@ ]+$/.test(normalized) || password !== DEMO_PASSWORD) {
      throw new Error("Имэйл эсвэл нууц үг буруу байна");
    }
    const nextUser = {
      email: normalized,
      name: normalized.split("@")[0],
      isAdmin: normalized === ADMIN_EMAIL,
    };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(nextUser));
    setUser(nextUser);
    return nextUser;
  }

  function logout() {
    localStorage.removeItem(STORAGE_KEY);
    setUser(null);
  }

  return <AuthContext value={{ user, login, logout }}>{children}</AuthContext>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth-ийг <AuthProvider> дотор дуудна уу.");
  }
  return context;
}
"""

PROTECTED_START = """\
// Нэвтрээгүй хэрэглэгчийг /login руу шилжүүлдэг layout route.
// Хэрэгтэй зүйлс: useAuth, Navigate, Outlet, useLocation.

export default function ProtectedRoute() {
  return null;
}
"""

PROTECTED_7 = """\
import { Navigate, Outlet, useLocation } from "react-router";
import { useAuth } from "../context/AuthContext";

export default function ProtectedRoute() {
  const { user } = useAuth();
  const location = useLocation();

  if (!user) {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />;
  }
  return <Outlet />;
}
"""

LOGIN_START = """\
// /login — «Заавар»-ын шаардлагын дагуу нэвтрэх форм.

export default function Login() {
  return (
    <section className="panel narrow">
      <h1>Нэвтрэх</h1>
    </section>
  );
}
"""

LOGIN_7 = """\
import { useState } from "react";
import { Navigate, useLocation, useNavigate } from "react-router";
import { ADMIN_EMAIL, DEMO_PASSWORD, useAuth } from "../context/AuthContext";

export default function Login() {
  const { user, login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const from = location.state?.from ?? "/profile";

  function handleSubmit(event) {
    event.preventDefault();
    try {
      login(email, password);
      navigate(from, { replace: true });
    } catch (loginError) {
      setError(loginError.message);
    }
  }

  // Аль хэдийн нэвтэрсэн бол форм хэрэггүй.
  if (user) {
    return <Navigate to={from} replace />;
  }

  const invalid = error ? true : undefined;
  const describedBy = error ? "login-error" : undefined;

  return (
    <section className="panel narrow">
      <title>Нэвтрэх — Ногоон сагс</title>
      <h1>Нэвтрэх</h1>
      <p className="notice">
        Дадлагын нэвтрэлт: дурын имэйл, нууц үг <strong>{DEMO_PASSWORD}</strong>. Админ:{" "}
        <strong>{ADMIN_EMAIL}</strong>
      </p>
      <form onSubmit={handleSubmit} noValidate>
        <div className="field">
          <label htmlFor="login-email">Имэйл</label>
          <input
            id="login-email"
            type="email"
            autoComplete="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            aria-invalid={invalid}
            aria-describedby={describedBy}
          />
        </div>
        <div className="field">
          <label htmlFor="login-password">Нууц үг</label>
          <input
            id="login-password"
            type="password"
            autoComplete="current-password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            aria-invalid={invalid}
            aria-describedby={describedBy}
          />
        </div>
        {error && (
          <p id="login-error" className="error" role="alert">
            {error}
          </p>
        )}
        <button type="submit" className="button">
          Нэвтрэх
        </button>
      </form>
    </section>
  );
}
"""

PROFILE_START = """\
// /profile — хэрэглэгчийн мэдээлэл ба «Миний захиалгууд» (зөвхөн нэвтэрсэн үед).

export default function Profile() {
  return (
    <section className="panel">
      <h1>Профайл</h1>
    </section>
  );
}
"""

PROFILE_7 = """\
import { useQuery } from "@tanstack/react-query";
import { getOrders } from "../api";
import { useAuth } from "../context/AuthContext";
import { formatDate, formatPrice, ORDER_STATUS } from "../format";

export default function Profile() {
  const { user } = useAuth();
  const {
    data: orders,
    isPending,
    isError,
  } = useQuery({ queryKey: ["orders", user.email], queryFn: () => getOrders(user.email) });

  return (
    <section className="panel">
      <title>Профайл — Ногоон сагс</title>
      <h1>Профайл</h1>
      <p>
        <span aria-hidden="true">👤</span> <strong>{user.name}</strong>
      </p>
      <p className="muted">{user.email}</p>
      <h2>Миний захиалгууд</h2>
      {isPending && (
        <p role="status" className="status">
          Ачаалж байна…
        </p>
      )}
      {isError && (
        <p role="alert" className="alert">
          Захиалгуудыг ачаалж чадсангүй.
        </p>
      )}
      {orders?.length === 0 && <p className="muted">Та одоогоор захиалга хийгээгүй байна.</p>}
      {orders?.length > 0 && (
        <div className="table-wrap">
          <table>
            <caption className="sr-only">Миний захиалгууд</caption>
            <thead>
              <tr>
                <th scope="col">Дугаар</th>
                <th scope="col">Огноо</th>
                <th scope="col">Төлөв</th>
                <th scope="col">Нийт</th>
              </tr>
            </thead>
            <tbody>
              {orders.map((order) => (
                <tr key={order.id}>
                  <td>#{order.id}</td>
                  <td>{formatDate(order.createdAt)}</td>
                  <td>
                    <span className="status-pill">
                      {ORDER_STATUS[order.status] ?? order.status}
                    </span>
                  </td>
                  <td>{formatPrice(order.total)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}
"""

# JS тестийн туслахууд: дадлагын захиалгууд ба нэвтрэх үйлдэл.
ORDERS_JS = """\
api.set("orders", [
  {
    id: 101,
    email: "bat@example.mn",
    customer: { name: "Бат", phone: "99112233", address: "СБД, 1-р хороо" },
    items: [{ productId: 1, name: "Банана", price: 3500, emoji: "🍌", quantity: 2 }],
    total: 7000,
    status: "delivered",
    createdAt: "2026-09-01T10:00:00.000Z",
  },
  {
    id: 102,
    email: "saraa@example.mn",
    customer: { name: "Сараа", phone: "88112233", address: "ХУД, 3-р хороо" },
    items: [{ productId: 8, name: "Бяслаг", price: 12500, emoji: "🧀", quantity: 1 }],
    total: 12500,
    status: "new",
    createdAt: "2026-09-10T09:30:00.000Z",
  },
  {
    id: 103,
    email: "bat@example.mn",
    customer: { name: "Бат", phone: "99112233", address: "СБД, 1-р хороо" },
    items: [
      { productId: 2, name: "Алим", price: 2800, emoji: "🍎", quantity: 1 },
      { productId: 7, name: "Сүү", price: 3200, emoji: "🥛", quantity: 2 },
    ],
    total: 9200,
    status: "shipping",
    createdAt: "2026-09-20T18:15:00.000Z",
  },
  {
    id: 104,
    email: "bat@example.mn",
    customer: { name: "Бат", phone: "99112233", address: "СБД, 1-р хороо" },
    items: [{ productId: 9, name: "Талх", price: 2500, emoji: "🍞", quantity: 3 }],
    total: 7500,
    status: "delivered",
    createdAt: "2026-09-25T08:00:00.000Z",
  },
]);
"""

LOG_IN_JS = """\
async function logIn(email) {
  await user.type(await screen.findByLabelText("Имэйл"), email);
  await user.type(screen.getByLabelText("Нууц үг"), "nogoon123");
  await user.click(screen.getByRole("button", { name: "Нэвтрэх" }));
}
"""

# --- 8. Админ -------------------------------------------------------------------

API_8_START = (
    API_7
    + """
// TODO: createProduct(product) — POST /api/products
// TODO: updateProduct(id, changes) — PATCH /api/products/:id
"""
)

API_8 = (
    API_7
    + """
/** POST /api/products → 201 { id, ...product } */
export function createProduct(product) {
  return request("/api/products", { method: "POST", body: JSON.stringify(product) });
}

/** PATCH /api/products/:id → шинэчлэгдсэн бүтэн бараа */
export function updateProduct(id, changes) {
  return request(`/api/products/${id}`, { method: "PATCH", body: JSON.stringify(changes) });
}
"""
)

APP_8_START = patch(
    APP_7,
    (
        'import Profile from "./pages/Profile";\n',
        'import Profile from "./pages/Profile";\n'
        "// TODO: Admin хуудсыг зөвхөн админд нээгдэх /admin route болгон нэм\n",
    ),
)

APP_8 = patch(
    APP_7,
    (
        'import Cart from "./pages/Cart";\n',
        'import Admin from "./pages/Admin";\nimport Cart from "./pages/Cart";\n',
    ),
    (
        '              <Route path="profile" element={<Profile />} />\n            </Route>\n',
        '              <Route path="profile" element={<Profile />} />\n'
        "            </Route>\n"
        "            <Route element={<ProtectedRoute adminOnly />}>\n"
        '              <Route path="admin" element={<Admin />} />\n'
        "            </Route>\n",
    ),
)

NAV_PRODUCTS_LINK = '        <NavLink to="/products">Бараа</NavLink>\n'

HEADER_8_START = patch(
    HEADER_7,
    (
        NAV_PRODUCTS_LINK,
        NAV_PRODUCTS_LINK + "        {/* TODO: зөвхөн админд «Админ» (/admin) холбоос */}\n",
    ),
)

HEADER_8 = patch(
    HEADER_7,
    (
        NAV_PRODUCTS_LINK,
        NAV_PRODUCTS_LINK + '        {user?.isAdmin && <NavLink to="/admin">Админ</NavLink>}\n',
    ),
)

PROTECTED_8_START = patch(
    PROTECTED_7,
    (
        "export default function ProtectedRoute() {\n",
        "// TODO: adminOnly prop — нэвтэрсэн ч админ биш бол «Хандах эрхгүй» хуудас\n"
        "export default function ProtectedRoute() {\n",
    ),
)

PROTECTED_8 = """\
import { Link, Navigate, Outlet, useLocation } from "react-router";
import { useAuth } from "../context/AuthContext";

export default function ProtectedRoute({ adminOnly = false }) {
  const { user } = useAuth();
  const location = useLocation();

  if (!user) {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />;
  }
  if (adminOnly && !user.isAdmin) {
    return (
      <section className="panel empty">
        <title>Хандах эрхгүй — Ногоон сагс</title>
        <h1>Хандах эрхгүй</h1>
        <p className="muted">Энэ хуудас зөвхөн админд зориулагдсан.</p>
        <Link to="/" className="button">
          Нүүр хуудас руу буцах
        </Link>
      </section>
    );
  }
  return <Outlet />;
}
"""

ADMIN_START = """\
// /admin — «Заавар»-ын шаардлага, дизайн, API-ийн дагуу бараа нэмэх, засах
// хуудас. Хэрэгтэй зүйлс: useQuery, useMutation, useQueryClient,
// getProducts, createProduct, updateProduct, formatPrice.

export default function Admin() {
  return (
    <section>
      <h1>Админ</h1>
    </section>
  );
}
"""

ADMIN_8 = """\
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { createProduct, getProducts, updateProduct } from "../api";
import { formatPrice } from "../format";

const CATEGORIES = ["Жимс", "Ногоо", "Сүүн бүтээгдэхүүн", "Гурил", "Бусад"];
const EMPTY = { name: "", price: "", category: "Жимс", emoji: "", stock: "" };

function isWholeNumber(value, min) {
  const number = Number(value);
  return String(value).trim() !== "" && Number.isInteger(number) && number >= min;
}

function validate(values) {
  const errors = {};
  if ("name" in values && values.name.trim() === "") {
    errors.name = "Нэрээ оруулна уу";
  }
  if (!isWholeNumber(values.price, 1)) {
    errors.price = "Үнэ 0-ээс их бүхэл тоо байна";
  }
  if (!isWholeNumber(values.stock, 0)) {
    errors.stock = "Үлдэгдэл 0 буюу түүнээс их бүхэл тоо байна";
  }
  return errors;
}

function Field({ id, label, error, ...inputProps }) {
  return (
    <div className="field">
      <label htmlFor={id}>{label}</label>
      <input
        id={id}
        aria-invalid={error ? true : undefined}
        aria-describedby={error ? `${id}-error` : undefined}
        {...inputProps}
      />
      {error && (
        <p id={`${id}-error`} className="error" role="alert">
          {error}
        </p>
      )}
    </div>
  );
}

export default function Admin() {
  const queryClient = useQueryClient();
  const {
    data: products,
    isPending,
    isError,
  } = useQuery({ queryKey: ["products"], queryFn: getProducts });

  const [draft, setDraft] = useState(EMPTY);
  const [draftSubmitted, setDraftSubmitted] = useState(false);
  const [editing, setEditing] = useState(null);
  const [editSubmitted, setEditSubmitted] = useState(false);
  const [message, setMessage] = useState("");

  const draftErrors = validate(draft);
  const editErrors = editing ? validate({ price: editing.price, stock: editing.stock }) : {};

  // Бараа өөрчлөгдсөн тул "products"-оор эхэлсэн бүх кэшийг (жагсаалт,
  // дэлгэрэнгүй) хуучирсан гэж тэмдэглэж, дахин татуулна.
  function refreshProducts() {
    queryClient.invalidateQueries({ queryKey: ["products"] });
  }

  const addProduct = useMutation({
    mutationFn: createProduct,
    onSuccess: (product) => {
      refreshProducts();
      setDraft(EMPTY);
      setDraftSubmitted(false);
      setMessage(`«${product.name}» нэмэгдлээ.`);
    },
  });

  const saveProduct = useMutation({
    mutationFn: ({ id, changes }) => updateProduct(id, changes),
    onSuccess: (product) => {
      refreshProducts();
      setEditing(null);
      setMessage(`«${product.name}» шинэчлэгдлээ.`);
    },
  });

  function handleAdd(event) {
    event.preventDefault();
    setDraftSubmitted(true);
    if (Object.keys(draftErrors).length > 0) return;
    addProduct.mutate({
      name: draft.name.trim(),
      price: Number(draft.price),
      category: draft.category,
      emoji: draft.emoji.trim() || "🛒",
      stock: Number(draft.stock),
    });
  }

  function handleSave(event) {
    event.preventDefault();
    setEditSubmitted(true);
    if (Object.keys(editErrors).length > 0) return;
    saveProduct.mutate({
      id: editing.id,
      changes: { price: Number(editing.price), stock: Number(editing.stock) },
    });
  }

  function startEditing(product) {
    setEditing({
      id: product.id,
      name: product.name,
      price: String(product.price),
      stock: String(product.stock),
    });
    setEditSubmitted(false);
    setMessage("");
  }

  function changeDraft(event) {
    setDraft({ ...draft, [event.target.name]: event.target.value });
  }

  function changeEditing(event) {
    setEditing({ ...editing, [event.target.name]: event.target.value });
  }

  const draftError = (name) => (draftSubmitted ? draftErrors[name] : undefined);
  const editError = (name) => (editSubmitted ? editErrors[name] : undefined);

  return (
    <section>
      <title>Админ — Ногоон сагс</title>
      <h1>Админ</h1>
      <p role="status" className={message ? "notice" : undefined}>
        {message}
      </p>
      <div className="admin-grid">
        <div>
          <form className="panel" onSubmit={handleAdd} noValidate aria-labelledby="new-product-title">
            <h2 id="new-product-title">Шинэ бараа</h2>
            <Field
              id="new-name"
              name="name"
              label="Нэр"
              value={draft.name}
              onChange={changeDraft}
              error={draftError("name")}
            />
            <Field
              id="new-price"
              name="price"
              label="Үнэ"
              type="number"
              min="1"
              value={draft.price}
              onChange={changeDraft}
              error={draftError("price")}
            />
            <div className="field">
              <label htmlFor="new-category">Ангилал</label>
              <select id="new-category" name="category" value={draft.category} onChange={changeDraft}>
                {CATEGORIES.map((category) => (
                  <option key={category}>{category}</option>
                ))}
              </select>
            </div>
            <Field id="new-emoji" name="emoji" label="Эмодзи" value={draft.emoji} onChange={changeDraft} />
            <Field
              id="new-stock"
              name="stock"
              label="Үлдэгдэл"
              type="number"
              min="0"
              value={draft.stock}
              onChange={changeDraft}
              error={draftError("stock")}
            />
            {addProduct.isError && (
              <p className="alert" role="alert">
                Бараа нэмж чадсангүй. Дахин оролдоно уу.
              </p>
            )}
            <button type="submit" className="button" disabled={addProduct.isPending}>
              {addProduct.isPending ? "Нэмж байна…" : "Нэмэх"}
            </button>
          </form>

          {editing && (
            <form
              key={editing.id}
              className="panel"
              onSubmit={handleSave}
              noValidate
              aria-labelledby="edit-title"
            >
              <h2 id="edit-title">Засах: {editing.name}</h2>
              <Field
                id="edit-price"
                name="price"
                label="Үнэ"
                type="number"
                min="1"
                autoFocus
                value={editing.price}
                onChange={changeEditing}
                error={editError("price")}
              />
              <Field
                id="edit-stock"
                name="stock"
                label="Үлдэгдэл"
                type="number"
                min="0"
                value={editing.stock}
                onChange={changeEditing}
                error={editError("stock")}
              />
              {saveProduct.isError && (
                <p className="alert" role="alert">
                  Хадгалж чадсангүй. Дахин оролдоно уу.
                </p>
              )}
              <div className="form-actions">
                <button type="submit" className="button" disabled={saveProduct.isPending}>
                  Хадгалах
                </button>
                <button type="button" className="button secondary" onClick={() => setEditing(null)}>
                  Болих
                </button>
              </div>
            </form>
          )}
        </div>

        <div className="panel table-wrap">
          {isPending && (
            <p role="status" className="status">
              Ачаалж байна…
            </p>
          )}
          {isError && (
            <p role="alert" className="alert">
              Бараа ачаалж чадсангүй.
            </p>
          )}
          {products && (
            <table>
              <caption>Бараанууд ({products.length})</caption>
              <thead>
                <tr>
                  <th scope="col">Бараа</th>
                  <th scope="col">Ангилал</th>
                  <th scope="col">Үнэ</th>
                  <th scope="col">Үлдэгдэл</th>
                  <th scope="col">
                    <span className="sr-only">Үйлдэл</span>
                  </th>
                </tr>
              </thead>
              <tbody>
                {products.map((product) => (
                  <tr key={product.id}>
                    <td>
                      <span aria-hidden="true">{product.emoji}</span> {product.name}
                    </td>
                    <td>{product.category}</td>
                    <td>{formatPrice(product.price)}</td>
                    <td>{product.stock}</td>
                    <td>
                      <button
                        type="button"
                        className="link-button"
                        aria-label={`Засах: ${product.name}`}
                        onClick={() => startEditing(product)}
                      >
                        Засах
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </section>
  );
}
"""

ADMIN_LOG_IN_JS = (
    LOG_IN_JS
    + """
setPath("/admin");
await runMain();
await logIn("admin@nogoon.mn");
"""
)

EDIT_BANANA_JS = """
await user.click(await screen.findByRole("button", { name: /Засах.*Банана|Банана.*засах/i }));
const editForm = await screen.findByRole("form", { name: /Засах/ });
const price = within(editForm).getByLabelText("Үнэ");
await user.clear(price);
await user.type(price, "3900");
"""

# --- 9. Бие даасан: захиалгын түүх ------------------------------------------------

ORDERS_START = """\
// /orders — «Захиалгын түүх». Хүлээн авах шалгуурыг «Заавар»-аас үз.

export default function Orders() {
  return (
    <section>
      <h1>Захиалгын түүх</h1>
    </section>
  );
}
"""

ORDERS_9 = """\
import { useQuery } from "@tanstack/react-query";
import { useNavigate, useSearchParams } from "react-router";
import { getOrders } from "../api";
import { useAuth } from "../context/AuthContext";
import { useCart } from "../context/CartContext";
import { formatDate, formatPrice, ORDER_STATUS } from "../format";

export default function Orders() {
  const { user } = useAuth();
  const { add } = useCart();
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  const status = searchParams.get("status") ?? "";

  const {
    data: orders,
    isPending,
    isError,
    refetch,
  } = useQuery({ queryKey: ["orders", user.email], queryFn: () => getOrders(user.email) });

  // Кэш дэх массивыг өөрчлөхгүйн тулд хуулбар дээр эрэмбэлнэ.
  const visible = [...(orders ?? [])]
    .filter((order) => status === "" || order.status === status)
    .sort((a, b) => b.createdAt.localeCompare(a.createdAt));

  function changeStatus(event) {
    const value = event.target.value;
    setSearchParams(value ? { status: value } : {}, { replace: true });
  }

  function reorder(order) {
    for (const item of order.items) {
      const { productId, name, price, emoji } = item;
      add({ id: productId, name, price, emoji }, item.quantity);
    }
    navigate("/cart");
  }

  return (
    <section>
      <title>Захиалгын түүх — Ногоон сагс</title>
      <h1>Захиалгын түүх</h1>
      <div className="filters">
        <div className="field">
          <label htmlFor="order-status">Төлөв</label>
          <select id="order-status" value={status} onChange={changeStatus}>
            <option value="">Бүгд</option>
            {Object.entries(ORDER_STATUS).map(([value, label]) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
          </select>
        </div>
      </div>

      {isPending && (
        <p role="status" className="status">
          Ачаалж байна…
        </p>
      )}
      {isError && (
        <div className="alert">
          <p role="alert">Захиалгуудыг ачаалж чадсангүй.</p>
          <button type="button" className="button" onClick={() => refetch()}>
            Дахин оролдох
          </button>
        </div>
      )}
      {orders && visible.length === 0 && <p className="panel empty">Захиалга олдсонгүй.</p>}

      {visible.length > 0 && (
        <ul className="order-list">
          {visible.map((order) => (
            <li key={order.id} className="card">
              <div className="order-head">
                <h2>Захиалга #{order.id}</h2>
                <span className="status-pill">{ORDER_STATUS[order.status] ?? order.status}</span>
              </div>
              <p className="muted">{formatDate(order.createdAt)}</p>
              <ul className="order-items">
                {order.items.map((item) => (
                  <li key={item.productId}>
                    <span>
                      <span aria-hidden="true">{item.emoji}</span> {item.name} × {item.quantity}
                    </span>
                    <span>{formatPrice(item.price * item.quantity)}</span>
                  </li>
                ))}
              </ul>
              <div className="summary">
                <p className="total">
                  Нийт: <strong>{formatPrice(order.total)}</strong>
                </p>
                <button
                  type="button"
                  className="button secondary"
                  aria-label={`Дахин захиалах: захиалга #${order.id}`}
                  onClick={() => reorder(order)}
                >
                  Дахин захиалах
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
"""

CART_CONTEXT_9 = patch(
    CART_CONTEXT_5,
    (
        "      const { id, name, price, emoji } = action.product;\n",
        "      const { id, name, price, emoji } = action.product;\n"
        "      const amount = action.quantity ?? 1;\n",
    ),
    (
        "{ ...item, quantity: item.quantity + 1 }",
        "{ ...item, quantity: item.quantity + amount }",
    ),
    (
        "{ id, name, price, emoji, quantity: 1 }",
        "{ id, name, price, emoji, quantity: amount }",
    ),
    (
        '    add: (product) => dispatch({ type: "add", product }),\n',
        '    add: (product, quantity = 1) => dispatch({ type: "add", product, quantity }),\n',
    ),
)

HEADER_9 = patch(
    HEADER_8,
    (
        NAV_PRODUCTS_LINK,
        NAV_PRODUCTS_LINK + '        {user && <NavLink to="/orders">Захиалгууд</NavLink>}\n',
    ),
)

APP_9 = patch(
    APP_8,
    (
        'import OrderSuccess from "./pages/OrderSuccess";\n',
        'import OrderSuccess from "./pages/OrderSuccess";\nimport Orders from "./pages/Orders";\n',
    ),
    (
        '              <Route path="profile" element={<Profile />} />\n',
        '              <Route path="profile" element={<Profile />} />\n'
        '              <Route path="orders" element={<Orders />} />\n',
    ),
)

ORDERS_LOG_IN_JS = (
    ORDERS_JS
    + LOG_IN_JS
    + """
setPath("/orders");
await runMain();
"""
)

# --- Модуль ---------------------------------------------------------------------

CAPSTONE = ModuleSpec(
    title="Модул 14 — Төгсгөлийн төсөл: «Ногоон сагс»",
    description="Сурсан бүхнээ нэгтгэж онлайн хүнсний дэлгүүрийг төлөвлөхөөс админ хэсэг хүртэл бүтээнэ.",
    lessons=[
        # ------------------------------------------------------------------ 14.1
        LessonSpec(
            title="Төлөвлөгөө ба бүтэц",
            slug="capstone-butets",
            description="Дэлгүүрийн хуудас, component-ийн мод, хавтсыг төлөвлөж, layout ба route-уудын араг ясыг бүтээнэ.",
            duration=1500,
            language=JSX,
            content="""\
### Энэ хичээлээр

- «Ногоон сагс» дэлгүүрийн хуудас, route-уудыг төлөвлөх
- Component-ийн мод, хавтасны бүтцийг зохиох
- Layout route, `NavLink`, 404 хуудастай апп-ын араг ясыг бүтээх

> **Дэмжлэг: бүрэн чиглүүлэгтэй.** Бүтэц, эхлэл код, алхам, зөвлөгөө
> бүгд өгөгдсөн. Модулийн туршид дэмжлэг аажмаар багасна: 1–3, 5-р хичээл
> бүрэн чиглүүлэгтэй, 4, 6, 7, 8-р хичээлд зөвхөн шаардлага, дизайн, API
> өгнө, 9-р хичээлийг бие дааж хийнэ.

### Яагаад чухал вэ

Том апп-ыг шууд кодлож эхэлбэл хэдхэн хоногийн дараа «энэ state хаана
байх ёстой вэ», «энэ файлыг хаанаас импортлох вэ» гэсэн асуултад
живдэг. Туршлагатай хөгжүүлэгч эхлээд **юу бүтээхээ** (хуудас, өгөгдөл),
дараа нь **хаана юу байхыг** (component, state, файл) төлөвлөдөг. Хэдэн
минутын төлөвлөгөө хэдэн цагийн засварыг хэмнэнэ.

### Юу бүтээх вэ

Энэ модульд бүтээх «Ногоон сагс» бол онлайн хүнсний дэлгүүр. Хичээл бүр
нэг боломж нэмнэ:

| Хичээл | Нэмэгдэх боломж | Хэрэглэх сэдэв |
|---|---|---|
| 1 | Араг яс: толгой, цэс, 404 | Routing, layout |
| 2 | Барааны каталог | API, TanStack Query |
| 3 | Барааны дэлгэрэнгүй | `useParams`, алдааны төлөв |
| 4 | Хайлт ба шүүлтүүр | `useSearchParams` |
| 5 | Сагс | Context, `useReducer` |
| 6 | Төлбөр тооцоо | Форм, баталгаажуулалт, `useMutation` |
| 7 | Нэвтрэлт, профайл | Auth context, хамгаалагдсан route |
| 8 | Админ | POST, PATCH, кэш шинэчлэх |
| 9 | Захиалгын түүх | Бие даасан ажил |

### Хуудас ба route

```text
/                 Нүүр
/products         Бараа (каталог, хайлт)
/products/:id     Барааны дэлгэрэнгүй
/cart             Сагс
/checkout         Төлбөр тооцоо
/login            Нэвтрэх
/profile          Профайл        (нэвтэрсэн хэрэглэгчид)
/orders           Захиалгын түүх (нэвтэрсэн хэрэглэгчид)
/admin            Админ          (зөвхөн админд)
*                 404
```

### Component-ийн мод ба state

```text
App
└── Layout              ← бүх хуудсанд: толгой, main, footer
    ├── Header          ← лого, цэс, (дараа нь) сагсны тоо
    └── <Outlet />      ← идэвхтэй хуудас
        ├── Home
        ├── Products → ProductCard × n
        ├── ProductDetail
        ├── Cart, Checkout, Login, Profile, Admin …
        └── NotFound
```

State-ийг төрлөөр нь ялгаж, тохирох газар нь байрлуулна:

| State | Хаана |
|---|---|
| Бараа, захиалга (серверийн өгөгдөл) | TanStack Query-ийн кэш |
| Хайлт, шүүлтүүр | URL (`?q=…&category=…`) |
| Сагс, нэвтэрсэн хэрэглэгч | Context (`CartContext`, `AuthContext`) |
| Формын утга | Тухайн component-ийн `useState` |

### Хавтасны бүтэц

```text
main.jsx 🔒        BrowserRouter, QueryClientProvider
App.jsx            бүх route
components/        Layout, Header, ProductCard …
pages/             хуудас бүр нэг файл
context/           CartContext, AuthContext (дараа)
api.js             сервертэй харилцах функцууд (дараа)
styles.css 🔒      бэлэн, responsive загвар
```

Бодит төсөлд үүнийг `npm create vite@latest nogoon-sags -- --template react`,
дараа нь `npm install react-router @tanstack/react-query`-ээр эхлүүлнэ.
Энд бүх зүйл бэлэн — файлуудын хооронд tab-аар шилжинэ.

### Layout route

Толгой, footer бүх хуудсанд ижил. Тиймээс тэдгээрийг нэг `Layout`
component-д хийж, хуудсуудыг түүний хүүхэд route болгоно. Хүүхэд route
`Layout` доторх `<Outlet />`-ийн байранд render хийгдэнэ:

```jsx
<Routes>
  <Route element={<Layout />}>
    <Route index element={<Home />} />
    <Route path="products" element={<Products />} />
    <Route path="*" element={<NotFound />} />
  </Route>
</Routes>
```

`path`-гүй `Layout` route нь хаягт юу ч нэмэхгүй — зөвхөн ороолт.
`path="*"` нь бусад ямар ч route таараагүй үед ажиллана.

### Хүртээмж ба responsive — эхнээсээ

- `<header>`, `<nav>`, `<main>`, `<footer>` нь дэлгэц уншигчид хуудсыг
  хэсгүүдэд хуваан харуулдаг **landmark**. `<nav aria-label="Үндсэн цэс">`
  нь цэсэнд нэр өгнө.
- `NavLink` идэвхтэй үедээ `class="active"` ба `aria-current="page"`-ийг
  **өөрөө** нэмнэ — харагдах ба дэлгэц уншигчид сонсогдох төлөв нэг дор.
- «Үндсэн агуулга руу алгасах» холбоос (skip link) нь гараар ажилладаг
  хэрэглэгчид цэсийг алгасах боломж олгоно. Tab дарахад л харагдана.
- `styles.css` нь утасны дэлгэцэнд ч эвдрэхгүй — «Хөтөч»-ийн өргөнийг
  багасгаж шалгаарай.

### Алхмууд

1. `components/Header.jsx` — лого дэргэд `<nav>` дотор «Нүүр» ба «Бараа»
   `NavLink`.
2. `components/Layout.jsx` — `<main id="main">` дотор `<Outlet />`, доор
   нь `<footer>`.
3. `App.jsx` — бүх route-ийг `Layout` дотор хийж, `products` ба `*`
   route нэм.
4. `pages/NotFound.jsx` — «Хуудас олдсонгүй», нүүр рүү буцах холбоос.

Дараа нь «Хөтөч»-ийн хаягийн мөрөнд `/products`, `/abc` гэж бичиж шалга.

```quiz
Сагсанд байгаа бараа толгойн тоо болон сагсны хуудас хоёуланд хэрэгтэй. Сагсны state-ийг хаана хадгалах нь зөв бэ?
- [ ] `Header` component-ийн `useState`-д
- [ ] URL-ийн `?cart=` параметрт
- [x] Хоёуланг нь агуулах түвшний Context-д
- [ ] `ProductCard` бүрийн `useState`-д
> Олон, алслагдсан component-д хэрэгтэй client state-ийг Context-д хадгална (5-р хичээл).
```

```quiz
Хаяг `/products` үед `<NavLink to="/">Нүүр</NavLink>` идэвхтэй (`aria-current="page"`) болох уу?
- [ ] Тийм — бүх зам `/`-ээр эхэлдэг
- [x] Үгүй — `/` холбоос зөвхөн яг `/` үед идэвхтэй
- [ ] Зөвхөн `end` prop өгвөл идэвхтэй болно
> react-router нь `/` холбоосыг онцгойлон авч үздэг: бусад замын эхлэл болгон тооцохгүй.
```

### Дүгнэлт

Төлөвлөгөөтэй болсноор хуудас, component, state бүр хаана байхыг мэдэж
байна. Layout route нь толгой, footer-ийг нэг удаа бичих боломж олгож,
`NavLink` нь идэвхтэй хуудсыг автоматаар тэмдэглэнэ. Дараагийн хичээлд
каталогийг серверээс татна.
""",
            initial_code=project(
                [
                    ("App.jsx", APP_1_START),
                    ("components/Header.jsx", HEADER_1_START),
                    ("components/Layout.jsx", LAYOUT_START),
                    ("pages/NotFound.jsx", NOT_FOUND_START),
                ],
                [
                    ("pages/Home.jsx", HOME),
                    ("pages/Products.jsx", PRODUCTS_PLACEHOLDER),
                ],
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 20 минут

«Заавар»-ын «Алхмууд»-ыг дагаж дэлгүүрийн араг ясыг бүтээ: толгойн цэс,
layout, route-ууд, 404 хуудас. TODO бүхий дөрвөн файлын хооронд tab-аар
шилжинэ.
""",
                tests=(
                    test(
                        "Толгойн цэсэнд «Нүүр», «Бараа» холбоосууд байна",
                        """
await runMain();
const nav = screen.getByRole("navigation");
expect(within(nav).getByRole("link", { name: "Нүүр" })).toHaveAttribute("href", "/");
expect(within(nav).getByRole("link", { name: "Бараа" })).toHaveAttribute("href", "/products");
""",
                    ),
                    test(
                        "«Бараа» дарахад каталог нээгдэж, цэсний холбоос идэвхтэй болно",
                        """
await runMain();
const nav = screen.getByRole("navigation");
await user.click(within(nav).getByRole("link", { name: "Бараа" }));
expect(await screen.findByRole("heading", { level: 1, name: "Бараа" })).toBeInTheDocument();
expect(within(nav).getByRole("link", { name: "Бараа" })).toHaveAttribute("aria-current", "page");
expect(within(nav).getByRole("link", { name: "Нүүр" })).not.toHaveAttribute("aria-current");
""",
                    ),
                    test(
                        "Хуудас бүр header, main, footer-тэй, лого нүүр рүү буцаана",
                        """
setPath("/products");
await runMain();
expect(screen.getByRole("banner")).toBeInTheDocument();
expect(screen.getByRole("main")).toBeInTheDocument();
expect(screen.getByRole("contentinfo")).toBeInTheDocument();
await user.click(screen.getByRole("link", { name: /Ногоон сагс/ }));
expect(await screen.findByRole("heading", { level: 1, name: "Ногоон сагс" })).toBeInTheDocument();
""",
                    ),
                    test(
                        "Бүртгэлгүй замд цэстэйгээ 404 хуудас, нүүр рүү буцах холбоос харагдана",
                        """
setPath("/baihgui-huudas");
await runMain();
expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent("Хуудас олдсонгүй");
expect(screen.getByRole("navigation")).toBeInTheDocument();
const back = within(screen.getByRole("main"))
  .getAllByRole("link")
  .find((link) => link.getAttribute("href") === "/");
expect(back).toBeTruthy();
await user.click(back);
expect(await screen.findByRole("heading", { level: 1, name: "Ногоон сагс" })).toBeInTheDocument();
""",
                    ),
                ),
                tips="""\
- `Header`: `import { Link, NavLink } from "react-router";` — `NavLink`-д
  класс, `aria-current`-ийг гараар өгөх шаардлагагүй.
- `Layout`: `<Outlet />` бол «хүүхэд route энд гарна» гэсэн байр. Түүнийг
  `<main>` дотор хийхээ бүү март, эс бөгөөс хуудсууд харагдахгүй.
- `App`: хүүхэд route-уудын `path` харьцангуй — `"products"` (`/`-гүй).
  Нүүр хуудас нь `index` route.
- `path="*"` route-ийг `Layout` ДОТОР хийвэл 404 хуудас цэстэйгээ гарна.
- `NotFound`-д `return null`-ийн оронд JSX буцаа.
""",
                solution=files(
                    ("App.jsx", APP_1),
                    ("components/Header.jsx", HEADER_1),
                    ("components/Layout.jsx", LAYOUT),
                    ("pages/NotFound.jsx", NOT_FOUND),
                ),
            ),
        ),
        # ------------------------------------------------------------------ 14.2
        LessonSpec(
            title="Барааны каталог",
            slug="capstone-katalog",
            description="Бараануудыг API-аас татаж, ачаалах ба алдааны төлөвтэй, картын grid болгон харуулна.",
            duration=1800,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Сервертэй харилцах кодыг `api.js`-д тусгаарлах
- TanStack Query-ийн `useQuery`-ээр барааны жагсаалт татах
- Ачаалах, алдаа, амжилттай гурван төлвийг хүртээмжтэйгээр харуулах
- `ProductCard` component-оор responsive grid бүтээх

> **Дэмжлэг: бүрэн чиглүүлэгтэй.** Эхлэл код, алхам, зөвлөгөө өгөгдсөн.

### Яагаад чухал вэ

Хэрэглэгчдийн ихэнх нь гар утсаар, заримдаа удаан интернэтээр ордог.
Хоосон цагаан дэлгэц харвал «эвдэрсэн» гэж бодоод гарна. Алдаа гарахад юу
ч хэлдэггүй апп итгэл алддаг. Тиймээс серверийн өгөгдөлтэй хуудас бүр
гурван төлөвтэй: **ачаалж байна**, **алдаа**, **өгөгдөл**.

### API

| Хүсэлт | Хариу |
|---|---|
| `GET /api/products` | 10 бараа: `[{ id, name, price, category, emoji, stock }]` |
| `GET /api/products/:id` | Нэг бараа, байхгүй бол `404` (дараагийн хичээлд) |

Дадлагын API хариугаа 0.4 секунд хоцроож өгдөг тул ачаалах төлөв «Хөтөч»
дээр харагдана.

### api.js — сервертэй ярих ганц газар

🔒 `api.js` бэлэн байгаа:

```jsx
export async function request(path, options = {}) {
  const response = await fetch(path, { ...options, headers: { … } });
  if (!response.ok) {
    throw new ApiError(response.status, "…");
  }
  return response.json();
}

export function getProducts() {
  return request("/api/products");
}
```

Хуудсууд `fetch`-ийг шууд дуудахгүй, `getProducts()`-ийг дуудна. Серверийн
хаяг солигдох, нэвтрэлтийн токен нэмэх үед ганц файл засна. `fetch` нь
`404`, `500`-д алдаа шиддэггүй тул `response.ok`-ийг энд нэг удаа шалгаж,
`status` талбартай `ApiError` шиднэ. Дараагийн хичээлд үүгээр «олдсонгүй»-г
бусад алдаанаас ялгана.

### useQuery

```jsx
const { data: products, isPending, isError, refetch } = useQuery({
  queryKey: ["products"],
  queryFn: getProducts,
});
```

- `queryKey` — кэшийн нэр. Өөр component ижил түлхүүрээр асуувал сервер
  рүү дахин явахгүй, кэшээс авна.
- `queryFn` — Promise буцаах функц. Функцийг **өөрийг нь** өгнө
  (`getProducts`), дуудаж (`getProducts()`) биш.
- 🔒 `main.jsx`-д `staleTime: 60 * 1000` (өгөгдлийг 1 минут шинэ гэж үзнэ)
  ба `retry: false` (алдааг шууд харуулна) гэж тохируулсан.

Үүнийг `useEffect` + `useState`-ээр ч бичиж болно (Модул 5), гэхдээ кэш,
давхар хүсэлт, хуучирсан хариуг өөрөө зохицуулах болно. Бодит төсөлд
серверийн өгөгдөлд тусгай сан хэрэглэдэг нь үүнээс.

### Гурван төлөв

```jsx
{isPending && <p role="status">Ачаалж байна…</p>}
{isError && (
  <div className="alert">
    <p role="alert">Бараа ачаалж чадсангүй.</p>
    <button type="button" onClick={() => refetch()}>Дахин оролдох</button>
  </div>
)}
```

- `role="status"` — дэлгэц уншигч одоогийн өгүүлбэрээ дуусгаад тайван
  уншина. Ачаалах мэдэгдэлд тохирно.
- `role="alert"` — яаралтай: шууд таслаад уншина. Алдаанд тохирно.
- «Дахин оролдох» нь хэрэглэгчид гарц үлдээнэ — хуудсыг бүхэлд нь дахин
  ачаалуулах хэрэггүй.

### ProductCard

```text
┌───────────────┐
│ 🍌            │  ← чимэглэл: aria-hidden="true"
│ Банана        │  ← <h2> доторх Link → /products/1
│ Жимс          │
│ 3,500₮        │  ← formatPrice(3500)
│ Дууссан       │  ← зөвхөн stock === 0 үед
└───────────────┘
```

- Emoji-ийн утгыг нэр нь аль хэдийн хэлж байгаа тул дэлгэц уншигчаас
  нууна (`aria-hidden="true"`). Бодит дэлгүүрт энэ нь зураг байх ба
  чимэглэлийн зураг `alt=""`, утга нэмдэг зураг л тайлбар `alt` авна.
- Бараа бүр `<li>` — дэлгэц уншигч «10 зүйлтэй жагсаалт» гэж хэлнэ.
- `.product-grid` загвар бэлэн: дэлгэц нарийсахад багана цөөрнө.
- Үнийг 🔒 `format.js`-ийн `formatPrice`-ээр: `3500` → `3,500₮`.

Нэрийн холбоос одоохондоо 404 рүү очно — дэлгэрэнгүй хуудсыг дараагийн
хичээлд хийнэ.

### Алхмууд

1. `components/ProductCard.jsx` — дизайны дагуу карт.
2. `pages/Products.jsx` — `useQuery`-ээр бараануудыг ав.
3. Ачаалах ба алдааны төлөв.
4. `<ul className="product-grid">` дотор бараа бүрт `ProductCard`.

Алдааны төлвийг «Хөтөч» дээр харахын тулд `queryFn`-ийг түр
`() => request("/api/products?_status=500")` болгоод (`request`-ийг
`../api`-аас импортолно) дараа нь буцаагаарай.

```quiz
Дараах кодын алдаа юу вэ?

`useQuery({ queryKey: ["products"], queryFn: getProducts() })`
- [ ] `queryKey` массив байх ёсгүй
- [x] `getProducts()` render бүрт шууд дуудагдаж, функцийн оронд Promise дамжина
- [ ] `useQuery`-г `useEffect` дотор дуудах ёстой
> `queryFn`-д функцийг өөрийг нь өгнө: `queryFn: getProducts`. Хэзээ дуудахыг TanStack Query шийднэ.
```

```quiz
Алдааны мессежид аль нь хамгийн тохиромжтой вэ?
- [ ] `role="status"`
- [x] `role="alert"`
- [ ] `aria-hidden="true"`
> `alert` яаралтай тул дэлгэц уншигч шууд уншина. `status` нь ачаалах мэт тайван мэдээлэлд.
```

### Дүгнэлт

Сервертэй харилцах код `api.js`-д, кэш ба төлөв TanStack Query-д, харагдах
байдал component-д — хэсэг бүр нэг л үүрэгтэй. Серверийн өгөгдөлтэй хуудас
бүрт ачаалах, алдаа, өгөгдөл гурван төлвийг бодолцож, `role`-оор дэлгэц
уншигчид мэдэгдэнэ.
""",
            initial_code=project(
                [
                    ("pages/Products.jsx", PRODUCTS_2_START),
                    ("components/ProductCard.jsx", PRODUCT_CARD_START),
                ],
                [
                    ("api.js", API_2),
                    ("format.js", FORMAT_JS),
                    ("App.jsx", APP_1),
                    ("components/Header.jsx", HEADER_1),
                    ("components/Layout.jsx", LAYOUT),
                    ("pages/Home.jsx", HOME),
                    ("pages/NotFound.jsx", NOT_FOUND),
                ],
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐ · 25 минут

`pages/Products.jsx`-д бараануудыг `useQuery`-ээр татаж, ачаалах ба
алдааны төлөвтэй харуул. `components/ProductCard.jsx`-д «Заавар»-ын
дизайны дагуу картаа бүтээ.
""",
                tests=(
                    test(
                        'Ачаалж байх үед role="status" бүхий «Ачаалж байна» мессеж харагдана',
                        """
api.delay = 300;
setPath("/products");
await runMain();
expect(screen.getByRole("status")).toHaveTextContent(/Ачаалж/);
await screen.findByRole("link", { name: "Банана" });
expect(screen.queryByRole("status")).toBeNull();
""",
                    ),
                    test(
                        "Бараа бүр нэр нь холбоос, ангилал, үнэтэй карт болж жагсаалтад харагдана",
                        """
setPath("/products");
await runMain();
expect(await screen.findByRole("link", { name: "Банана" })).toHaveAttribute("href", "/products/1");
const productLinks = screen
  .getAllByRole("link")
  .filter((link) => /^[/]products[/][0-9]+$/.test(link.getAttribute("href") ?? ""));
expect(productLinks).toHaveLength(10);
expect(screen.getAllByRole("listitem")).toHaveLength(10);
expect(screen.text()).toMatch(/3,500 ?₮/);
expect(screen.text()).toContain("Сүүн бүтээгдэхүүн");
""",
                    ),
                    test(
                        "Дууссан барааг «Дууссан» гэж тэмдэглэнэ",
                        """
setPath("/products");
await runMain();
await screen.findByRole("link", { name: "Брокколи" });
expect(screen.getAllByText(/Дууссан/)).toHaveLength(1);
""",
                    ),
                    test(
                        'Серверийн алдаанд role="alert" мессеж гарч, «Дахин оролдох» товч дахин ачаална',
                        """
api.fail("/api/products", 500);
setPath("/products");
await runMain();
expect(await screen.findByRole("alert")).toBeInTheDocument();
expect(screen.queryByRole("link", { name: "Банана" })).toBeNull();
api.reset();
await user.click(screen.getByRole("button", { name: "Дахин оролдох" }));
expect(await screen.findByRole("link", { name: "Банана" })).toBeInTheDocument();
""",
                    ),
                ),
                tips="""\
- `const { data: products, isPending, isError, refetch } = useQuery({ … });`
  — `data`-г `products` гэж нэрлэвэл уншихад хялбар.
- Эхний render-т `products` нь `undefined`. `products.map` бичихээс өмнө
  `{products && …}` гэж шалга, эс бөгөөс «Cannot read properties of
  undefined» алдаа гарна.
- `onClick={refetch}` биш `onClick={() => refetch()}` — эс бөгөөс click
  event нь `refetch`-ийн тохиргоо (options) болж дамжина.
- Картын холбоос: `` <Link to={`/products/${product.id}`}>{product.name}</Link> ``.
- `ProductCard`-д `key` өгөхгүй — `key`-г `map` доторх `<ProductCard key={product.id} …>`-д өгнө.
""",
                solution=files(
                    ("pages/Products.jsx", PRODUCTS_2),
                    ("components/ProductCard.jsx", PRODUCT_CARD_2),
                ),
            ),
        ),
        # ------------------------------------------------------------------ 14.3
        LessonSpec(
            title="Барааны дэлгэрэнгүй хуудас",
            slug="capstone-delgerengui",
            description="/products/:id хуудсанд нэг барааг татаж, «олдсонгүй» ба алдааны төлөвтэй харуулна.",
            duration=1800,
            language=JSX,
            content="""\
### Энэ хичээлээр

- `/products/:id` динамик route ба `useParams`
- Нэг барааг id-аар нь татах, `queryKey`-д id оруулах
- «Олдсонгүй» (`404`)-г бусад алдаанаас ялгах
- React 19-ийн `<title>`-ээр хөтчийн tab-ын гарчгийг солих

> **Дэмжлэг: бүрэн чиглүүлэгтэй.** Эхлэл код, алхам, зөвлөгөө өгөгдсөн.

### Яагаад чухал вэ

Хэрэглэгч барааны холбоосыг найздаа Messenger-ээр илгээнэ, хуучирсан
холбоосоор орно, хаягийг гараар бичнэ. Тиймээс дэлгэрэнгүй хуудас
каталогоор дамжилгүй **шууд** нээгдэх, устсан бараанд ойлгомжтой хариу
өгөх ёстой. «Олдсонгүй» ба «сервер унасан» хоёр өөр нөхцөл: эхнийхэд
хэрэглэгч өөр бараа хайна, хоёр дахьд дахин оролдоно.

### Route ба useParams

```jsx
<Route path="products/:id" element={<ProductDetail />} />
```

```jsx
const { id } = useParams(); // "/products/8" → "8" — string!
```

### Нэг барааг татах

🔒 `api.js`-д `getProduct(id)` нэмэгдсэн. Түүнийг `useQuery`-ээр дуудна:

```jsx
const { data: product, isPending, error } = useQuery({
  queryKey: ["products", id],
  queryFn: () => getProduct(id),
});
```

- `queryKey`-д **id заавал** орно. Бараа бүр кэшдээ өөрийн байртай болно.
- `queryFn` нь аргументтай функц дууддаг тул arrow функцээр ороосон.
- `["products", id]` нь `["products"]`-ээр эхэлдэг — 8-р хичээлд
  `["products"]`-ийг шинэчлэхэд дэлгэрэнгүй хуудсууд ч дагаад шинэчлэгдэнэ.

### Олдсонгүй ба бусад алдаа

Эрт буцаалтаар (early return) төлөв бүрийг дарааллаар нь шийднэ:

```jsx
if (isPending) return <p role="status">Ачаалж байна…</p>;

if (error?.status === 404) {
  return (
    <section>
      <h1>Бараа олдсонгүй</h1>
      <Link to="/products">Бүх бараа</Link>
    </section>
  );
}

if (error) return <p role="alert">Бараа ачаалж чадсангүй.</p>;

// Энд хүрвэл product заавал байна.
```

`ApiError`-ийн `status`-аар ялгана. `error?.status` дахь `?.` нь `error`
`null` үед алдаа шидэхээс сэргийлнэ.

### Хөтчийн гарчиг: `<title>`

React 19-д `<title>`-ийг component-ийн хаана ч бичиж болно — React өөрөө
`<head>` руу зөөнө:

```jsx
<title>{`${product.name} — Ногоон сагс`}</title>
```

`<title>`-ийн хүүхэд **нэг string** байх ёстой. `{product.name} — Ногоон сагс`
гэж бичвэл хэд хэдэн хүүхэд болж React анхааруулна — template string-ээр
нэгтгэ. React 19-өөс өмнө үүнийг `useEffect`-д `document.title = …` гэж
эсвэл `react-helmet` сангаар хийдэг байсан. Зөв гарчиг нь олон tab
нээдэг хэрэглэгч, дэлгэц уншигч, хайлтын системд тустай.

### Буцах товч

```jsx
const navigate = useNavigate();

<button type="button" onClick={() => navigate(-1)}>← Буцах</button>
```

`navigate(-1)` нь хөтчийн «буцах» сумтай ижил — хэрэглэгчийг яг өмнөх
хуудас руу нь (дараагийн хичээлд — хайлт, шүүлтүүртэй нь) буцаана.
`<Link to="/products">` бол үргэлж шүүлтүүргүй каталог руу очно.

### Дизайн

```text
← Буцах
┌─────────┐   Жимс
│   🍎    │   Алим                 ← h1
│         │   2,800₮
└─────────┘   Үлдэгдэл: 40 ширхэг  ← stock 0 бол «Дууссан»
```

### Алхмууд

1. `App.jsx` — `products/:id` route.
2. `pages/ProductDetail.jsx` — `useParams`, `useQuery`.
3. Ачаалах, «олдсонгүй», алдааны төлөв.
4. Үндсэн хэсэг: `<title>`, «← Буцах», emoji, ангилал, нэр, үнэ, үлдэгдэл.

«Хөтөч»-ийн хаягийн мөрөнд `/products/8`, `/products/999` гэж бичиж шалга.

### Нэмэлт сорилт

Хэрэглэгч холбоосоор шууд орсон бол «буцах» өмнөх хуудасгүй. Ийм үед
(`useLocation().key === "default"`) `/products` руу шилжүүл.

```quiz
`queryKey: ["product"]` (id-гүй) гэж бичвэл юу болох вэ?
- [ ] Алдаа шиднэ
- [x] Өөр бараа руу шилжихэд кэшээс өмнөх бараа харагдана
- [ ] Бараа бүрт шинэ хүсэлт явна, асуудалгүй
> Түлхүүр ижил тул TanStack Query «энэ өгөгдөл аль хэдийн бий» гэж үзнэ. Хүсэлтэд нөлөөлөх бүх утгыг түлхүүрт оруулна.
```

```quiz
`/products/8` хаягт `useParams().id === 8` юу буцаах вэ?
- [ ] `true`
- [x] `false`
> URL-ийн параметр үргэлж string: `"8" === 8` худал. Тоотой харьцуулахдаа `Number(id)` ашигла.
```

### Дүгнэлт

Динамик route + `useParams` + id-тай `queryKey` — дэлгэрэнгүй хуудсын
стандарт хослол. Эрт буцаалтаар ачаалах, «олдсонгүй», алдааны төлвийг
дарааллаар нь шийдэж, `<title>`-ээр хөтчийн гарчгийг шинэчилнэ.
""",
            initial_code=project(
                [
                    ("pages/ProductDetail.jsx", DETAIL_3_START),
                    ("App.jsx", APP_3_START),
                ],
                [
                    ("api.js", API_3),
                    ("format.js", FORMAT_JS),
                    ("components/Header.jsx", HEADER_1),
                    ("components/Layout.jsx", LAYOUT),
                    ("components/ProductCard.jsx", PRODUCT_CARD_2),
                    ("pages/Home.jsx", HOME),
                    ("pages/Products.jsx", PRODUCTS_2),
                    ("pages/NotFound.jsx", NOT_FOUND),
                ],
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐ · 25 минут

`App.jsx`-д дэлгэрэнгүй хуудсын route-ийг бүртгэж, `pages/ProductDetail.jsx`-д
нэг барааг татаж харуул. «Олдсонгүй» ба бусад алдааг ялгаж, хөтчийн
гарчгийг барааны нэрээр соль.
""",
                tests=(
                    test(
                        "Каталогт барааны нэр дээр дарахад дэлгэрэнгүй хуудас нээгдэнэ",
                        """
setPath("/products");
await runMain();
await user.click(await screen.findByRole("link", { name: "Алим" }));
expect(await screen.findByRole("heading", { level: 1, name: "Алим" })).toBeInTheDocument();
const text = screen.text();
expect(text).toMatch(/2,800 ?₮/);
expect(text).toContain("Жимс");
expect(text).toMatch(/Үлдэгдэл: ?40/);
""",
                    ),
                    test(
                        "Хаягаар шууд орж болох ба дууссан барааг «Дууссан» гэж харуулна",
                        """
setPath("/products/6");
await runMain();
expect(await screen.findByRole("heading", { level: 1, name: "Брокколи" })).toBeInTheDocument();
expect(screen.text()).toContain("Дууссан");
""",
                    ),
                    test(
                        "Байхгүй бараанд «Бараа олдсонгүй» ба бүх бараа руу холбоос харагдана",
                        """
setPath("/products/999");
await runMain();
expect(await screen.findByText(/Бараа олдсонгүй/)).toBeInTheDocument();
const link = within(screen.getByRole("main"))
  .getAllByRole("link")
  .find((a) => a.getAttribute("href") === "/products");
expect(link).toBeTruthy();
""",
                    ),
                    test(
                        "«← Буцах» товч өмнөх хуудас руу буцаана",
                        """
setPath("/products");
await runMain();
await user.click(await screen.findByRole("link", { name: "Жүрж" }));
await screen.findByRole("heading", { level: 1, name: "Жүрж" });
await user.click(screen.getByRole("button", { name: /Буцах/ }));
expect(await screen.findByRole("heading", { level: 1, name: "Бараа" })).toBeInTheDocument();
""",
                    ),
                    test(
                        "Хөтчийн tab-ын гарчиг барааны нэртэй болно",
                        """
setPath("/products/8");
await runMain();
await screen.findByRole("heading", { level: 1, name: "Бяслаг" });
expect(document.title).toContain("Бяслаг");
""",
                    ),
                ),
                tips="""\
- `App.jsx`: `<Route path="products/:id" element={<ProductDetail />} />` —
  `import ProductDetail from "./pages/ProductDetail";`-ийг мартуузай.
- `queryFn: () => getProduct(id)` — arrow функцгүйгээр `getProduct(id)`
  шууд дуудагдана.
- Төлвүүдийг `isPending` → `404` → бусад алдаа → үндсэн хэсэг дарааллаар
  эрт буцаалтаар шийд. `product.name`-ийг `isPending`-ийн шалгалтаас өмнө
  уншвал алдаа гарна.
- `<title>`-д template string: `` {`${product.name} — Ногоон сагс`} ``.
- «Буцах» нь холбоос биш товч: `<button type="button" onClick={() => navigate(-1)}>`.
""",
                solution=files(
                    ("pages/ProductDetail.jsx", DETAIL_3),
                    ("App.jsx", APP_3),
                ),
            ),
        ),
        # ------------------------------------------------------------------ 14.4
        LessonSpec(
            title="Хайлт ба шүүлтүүр",
            slug="capstone-hailt",
            description="Каталогт нэрээр хайх, ангиллаар шүүх боломжийг URL-д хадгалагдах байдлаар нэмнэ.",
            duration=1800,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Хайлт, шүүлтүүрийн утгыг URL-д хадгалах (`useSearchParams`)
- Шүүсэн жагсаалтыг state-гүйгээр, render үеэр тооцоолох
- Үр дүнгийн тоо, хоосон үр дүнг хүртээмжтэйгээр мэдэгдэх

> **Дэмжлэг: хагас чиглүүлэгтэй.** Шаардлага, дизайн, URL-ийн хэлбэр
> өгөгдөнө. Кодын бүтэц, state-ээ хэрхэн зохион байгуулахыг өөрөө шийднэ.

### Яагаад чухал вэ

Хэрэглэгч «Ногоо» ангиллаас «төмс» хайгаад, нэг бараа нээж үзээд буцлаа
гэж бодъё. Шүүлтүүр нь алга болсон бол дахин бичих болно — хэдэн удаа
давтагдвал бухимдана. Мөн «эдгээр ногоог хар» гэж холбоос илгээхэд найз нь
яг ижил үр дүнг харах ёстой. Шүүлтүүрийг **URL-д** хадгалбал хоёр асуудал
зэрэг шийдэгдэнэ: хаяг өөрөө state болно.

### Шаардлага

1. «Хайх» label-тэй хайлтын талбар — барааны **нэрээр** шүүнэ, том жижиг
   үсэг ялгахгүй («алим» → «Алим»).
2. «Ангилал» label-тэй `<select>` — эхний сонголт «Бүгд», дараа нь
   бараануудын ангиллууд давхардалгүй.
3. Хоёр шүүлтүүр зэрэг ажиллана.
4. Утгууд URL-д: `/products?q=алим&category=Жимс`. Хоосон утгыг URL-д
   бичихгүй. Ийм хаягаар шууд орход талбарууд бөглөгдөж, шүүлт хэрэгжинэ.
5. Үр дүнгийн тоо `role="status"`-тай («3 бараа олдлоо»). Тохирох бараа
   байхгүй бол «Тохирох бараа олдсонгүй».
6. Бараа нээгээд «← Буцах» дарахад хайлт, шүүлтүүр хэвээр үлдэнэ.

### Дизайн

```text
Бараа
┌ Хайх ───────────────────┐  ┌ Ангилал ────────┐
│ алим                    │  │ Бүгд          ▾ │
└─────────────────────────┘  └─────────────────┘
1 бараа олдлоо
┌──────────┐
│ 🍎 Алим  │
└──────────┘
```

`.filters`, `.field` загвар бэлэн: өргөн дэлгэцэнд хажуу хажуудаа, утсан
дээр доошоо байрлана. Талбаруудыг `<form role="search">`-оор ороовол
дэлгэц уншигчид «хайлт» landmark болж харагдана.

### URL бол state

```jsx
const [searchParams, setSearchParams] = useSearchParams();
const query = searchParams.get("q") ?? ""; // байхгүй бол null → ""
```

`setSearchParams` нь query string-ийг **бүхэлд нь** солино. Нэг
параметрийг өөрчлөхдөө бусдыг нь хадгал:

```jsx
function updateFilter(name, value) {
  const next = new URLSearchParams(searchParams);
  if (value) next.set(name, value);
  else next.delete(name);
  setSearchParams(next, { replace: true });
}
```

- `replace: true` — үсэг бүр түүхэнд шинэ мөр нэмэхгүй. Эс бөгөөс «буцах»
  сум өмнөх хуудас биш, өмнөх **үсэг** рүү очно.
- Талбарын `value`-г URL-аас ав. Тусдаа `useState` нэмбэл хоёр эх сурвалж
  болж зөрнө: URL «алим», талбар хоосон гэх мэт.

### Шүүлтийг render үеэр тооцоол

```jsx
const visible = products.filter(
  (product) =>
    product.name.toLowerCase().includes(query.trim().toLowerCase()) &&
    (category === "" || product.category === category),
);
```

Шүүсэн жагсаалтыг state-д хадгалах, `useEffect`-ээр шинэчлэх шаардлагагүй
(Модул 5, «Effect хэрэгтэй юу»). Бараа мянга мянгаараа болбол `useMemo`,
`useDeferredValue` (Модул 10, 12) эсвэл серверээр шүүх
(`/api/products?q=алим&category=Жимс`, `queryKey`-д шүүлтүүрээ оруулж)
аргад шилжинэ. Энд 10 бараа тул хөтөч дээр шүүх нь хамгийн энгийн.

```quiz
Хаяг `/products?category=Жимс` үед `setSearchParams({ q: "алим" })` дуудвал хаяг ямар болох вэ?
- [ ] `/products?category=Жимс&q=алим`
- [x] `/products?q=алим` — ангилал алга болно
- [ ] Алдаа гарна
> `setSearchParams` нь бүх query string-ийг солино. Бусад параметрийг хадгалахын тулд одоогийн `searchParams`-аас хуулж өөрчил.
```

```quiz
Шүүлтүүрийг URL-д хадгалахын давуу тал АЛЬ НЬ БИШ вэ?
- [ ] Холбоос хуваалцахад ижил үр дүн гарна
- [ ] «Буцах» дарахад шүүлтүүр сэргэнэ
- [x] Хуудас хурдан ачаалагдана
- [ ] Хуудсыг дахин ачаалахад шүүлтүүр хадгалагдана
> URL хурдад нөлөөлөхгүй. Харин state-ийг хуваалцах, сэргээх боломжтой болгодог.
```

### Дүгнэлт

Хайх, шүүх, эрэмбэлэх, хуудаслах зэрэг «хэрэглэгч юу харж байна» гэсэн
state-ийн гэр нь URL. `useSearchParams`-аас утгаа уншиж, шүүсэн жагсаалтыг
render бүрт тооцоолбол нэг л үнэн эх сурвалж үлдэнэ.
""",
            initial_code=project(
                [("pages/Products.jsx", PRODUCTS_4_START)],
                [
                    ("App.jsx", APP_3),
                    ("api.js", API_3),
                    ("format.js", FORMAT_JS),
                    ("components/Header.jsx", HEADER_1),
                    ("components/Layout.jsx", LAYOUT),
                    ("components/ProductCard.jsx", PRODUCT_CARD_2),
                    ("pages/Home.jsx", HOME),
                    ("pages/ProductDetail.jsx", DETAIL_3),
                    ("pages/NotFound.jsx", NOT_FOUND),
                ],
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐ · 30 минут

`pages/Products.jsx`-д «Заавар»-ын шаардлагын дагуу хайлт ба ангиллын
шүүлтүүр нэм. Утгууд URL-д хадгалагдана — «Хөтөч»-ийн хаягийн мөрийг
ажиглаарай.
""",
                tests=(
                    test(
                        "«Хайх» талбарт бичихэд бараа нэрээр нь шүүгдэнэ",
                        """
setPath("/products");
await runMain();
await screen.findByRole("link", { name: "Банана" });
await user.type(screen.getByLabelText("Хайх"), "алим");
await waitFor(() => expect(screen.queryByRole("link", { name: "Банана" })).toBeNull());
expect(await screen.findByRole("link", { name: "Алим" })).toBeInTheDocument();
""",
                    ),
                    test(
                        "«Ангилал» сонгоход зөвхөн тэр ангиллын бараа үлдэж, тоо нь харагдана",
                        """
setPath("/products");
await runMain();
await screen.findByRole("link", { name: "Банана" });
const select = screen.getByLabelText("Ангилал");
expect(within(select).getAllByRole("option")).toHaveLength(6);
expect(within(select).getAllByRole("option")[0]).toHaveTextContent("Бүгд");
await user.selectOptions(select, "Ногоо");
await waitFor(() => expect(screen.queryByRole("link", { name: "Банана" })).toBeNull());
for (const name of ["Лууван", "Төмс", "Брокколи"]) {
  expect(await screen.findByRole("link", { name })).toBeInTheDocument();
}
await waitFor(() => expect(screen.getByRole("status")).toHaveTextContent("3"));
""",
                    ),
                    test(
                        "Хаягийн ?q= ба ?category=-г уншиж, хоёр шүүлтүүрийг зэрэг хэрэглэнэ",
                        """
setPath("/products?q=ал&category=Жимс");
await runMain();
expect(await screen.findByRole("link", { name: "Алим" })).toBeInTheDocument();
expect(screen.queryByRole("link", { name: "Талх" })).toBeNull();
expect(screen.queryByRole("link", { name: "Банана" })).toBeNull();
expect(screen.getByLabelText("Хайх")).toHaveValue("ал");
expect(screen.getByLabelText("Ангилал")).toHaveValue("Жимс");
""",
                    ),
                    test(
                        "Тохирох бараа байхгүй бол «Тохирох бараа олдсонгүй» гэж харуулна",
                        """
setPath("/products");
await runMain();
await screen.findByRole("link", { name: "Банана" });
await user.type(screen.getByLabelText("Хайх"), "пицца");
expect(await screen.findByText(/Тохирох бараа олдсонгүй/)).toBeInTheDocument();
expect(screen.queryAllByRole("listitem")).toHaveLength(0);
""",
                    ),
                    test(
                        "Бараа үзээд «← Буцах» дарахад хайлт, шүүлтүүр хэвээр үлдэнэ",
                        """
setPath("/products");
await runMain();
await screen.findByRole("link", { name: "Банана" });
await user.selectOptions(screen.getByLabelText("Ангилал"), "Жимс");
await user.type(screen.getByLabelText("Хайх"), "алим");
await user.click(await screen.findByRole("link", { name: "Алим" }));
await screen.findByRole("heading", { level: 1, name: "Алим" });
await user.click(screen.getByRole("button", { name: /Буцах/ }));
expect(await screen.findByLabelText("Хайх")).toHaveValue("алим");
expect(screen.getByLabelText("Ангилал")).toHaveValue("Жимс");
expect(screen.queryByRole("link", { name: "Банана" })).toBeNull();
""",
                    ),
                ),
                tips="""\
- Утгуудыг `useState`-д биш URL-д хадгал: `searchParams.get("q") ?? ""`.
  `useState`-д хадгалбал хаягаар шууд орох, «Буцах» дарах үед шүүлтүүр
  алга болно — хуудас дахин mount болоход state арилдаг.
- Нэг параметрийг солихдоо `new URLSearchParams(searchParams)`-аар
  хуулбар үүсгэж `set`/`delete` хий, дараа нь `setSearchParams(next, { replace: true })`.
- Ангиллууд: `[...new Set(products.map((p) => p.category))]`.
- `select`-ийн хоосон утгатай «Бүгд» сонголт: `<option value="">Бүгд</option>`.
- Харьцуулахдаа хоёр талыг `toLowerCase()` болго.
""",
                solution=files(("pages/Products.jsx", PRODUCTS_4)),
            ),
        ),
        # ------------------------------------------------------------------ 14.5
        LessonSpec(
            title="Сагс",
            slug="capstone-sags",
            description="CartContext ба useReducer-ээр сагс бүтээж, толгойн тоо, «Сагсанд нэмэх» товч, сагсны хуудсыг холбоно.",
            duration=2700,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Сагсны дүрмүүдийг `useReducer`-ийн цэвэр функцэд төвлөрүүлэх
- `CartContext`-оор сагсыг апп даяар хуваалцах
- Толгойн тоо, «Сагсанд нэмэх» товч, сагсны хуудсыг нэг сагсанд холбох

> **Дэмжлэг: бүрэн чиглүүлэгтэй.** Файл бүрт дугаарласан TODO бий
> (`TODO 1` … `TODO 8`), доорх алхмууд тэдгээрийг дарааллаар нь тайлбарлана.

### Яагаад чухал вэ

Сагс бол дэлгүүрийн зүрх. Каталогийн карт, дэлгэрэнгүй хуудас, толгойн
тоо, сагсны хуудас, дараагийн хичээлийн тооцоо — таван өөр газар **нэг**
сагсыг уншиж, өөрчилнө. Хэсэг бүр өөрийн state-тэй бол тоонууд зөрнө.
Props-оор дамжуулбал `Layout`, `Outlet`-ийг дамжин олон давхарга нэвтэрнэ
(prop drilling). Context + reducer: нэг үнэн эх сурвалж, өөрчлөлтийн бүх
дүрэм нэг газарт.

### Өгөгдлийн хэлбэр

```jsx
// Сагсны нэг мөр
{ id: 1, name: "Банана", price: 3500, emoji: "🍌", quantity: 2 }
```

Зөвхөн хэрэгтэй талбаруудыг хуулна (`stock`, `category` хэрэггүй). Нийт
ширхэг (`count`), нийт үнэ (`total`)-ийг state-д **хадгалахгүй** — `items`-ээс
тооцоолно. Хадгалбал хэзээ нэгэн цагт зөрнө.

### Reducer — сагсны дүрмүүд

| Үйлдэл (action) | Үр дүн |
|---|---|
| `{ type: "add", product }` | Байхгүй бол нэмнэ, байвал тоо +1 |
| `{ type: "remove", id }` | Мөрийг хасна |
| `{ type: "setQuantity", id, quantity }` | Тоог солино, 0 бол хасна |
| `{ type: "clear" }` | Хоосолно (тооцооны дараа) |

```jsx
case "add": {
  const { id, name, price, emoji } = action.product;
  const existing = items.find((item) => item.id === id);
  if (existing) {
    return items.map((item) =>
      item.id === id ? { ...item, quantity: item.quantity + 1 } : item,
    );
  }
  return [...items, { id, name, price, emoji, quantity: 1 }];
}
```

`existing.quantity += 1; return items;` гэж бичвэл массив нь хуучин
reference хэвээр — React «өөрчлөгдөөгүй» гэж үзээд дэлгэцийг
шинэчлэхгүй. Reducer бол цэвэр функц тул UI-гүйгээр шууд тестлэгдэнэ
(эхний тест яг үүнийг хийнэ).

### Provider ба hook

`CartContext.jsx`-ийн доод хэсэг бэлэн байгаа:

```jsx
const value = {
  items, count, total,
  add: (product) => dispatch({ type: "add", product }),
  remove: (id) => dispatch({ type: "remove", id }),
  // …
};

return <CartContext value={value}>{children}</CartContext>;
```

- Component-ууд `dispatch`, action-ы хэлбэрийг мэдэхгүй — `add(product)`
  гэж л дууддаг. Reducer-ийг дараа нь өөрчилсөн ч тэд өөрчлөгдөхгүй.
- React 19-д context-ийг шууд provider болгон бичнэ: `<CartContext value>`.
  Хуучин кодод `<CartContext.Provider value>` гэж харна — ижил утгатай.
- `useCart()` нь provider-гүй газар дуудагдвал ойлгомжтой алдаа шиднэ.

`App.jsx`-д `<Routes>`-ийг бүхэлд нь `<CartProvider>`-оор ороовол бүх
хуудас, `Layout` доторх `Header` ч сагсанд хүрнэ. Хуудас хооронд шилжихэд
сагс хадгалагдана (хуудсыг дахин ачаалахад арилна — «Нэмэлт сорилт»-ыг үз).

### Холбох

```jsx
// Header
const { count } = useCart();
<NavLink to="/cart">
  <span aria-hidden="true">🛒</span> Сагс <span className="badge">{count}</span>
</NavLink>

// ProductCard, ProductDetail
const { add } = useCart();
<button onClick={() => add(product)} disabled={product.stock === 0}>
  Сагсанд нэмэх
</button>
```

- Каталогт арван «Сагсанд нэмэх» товч бий. Дэлгэц уншигчийн товчны
  жагсаалтад бүгд ижил сонсогдоно. `aria-label="Сагсанд нэмэх: Банана"`
  нь тэднийг ялгана. Харагдах текстээр эхэлж байгаа тул дуугаар
  удирддаг хэрэглэгч «Сагсанд нэмэх» гэж хэлэхэд ажиллана.
- `ProductDetail` дотор `useCart()`-ийг бусад hook-ийн хамт **early
  return-оос өмнө** дууд — hook-ийн дүрэм (Модул 6).

### Алхмууд

1. `context/CartContext.jsx` — TODO 1–3: `add`, `remove`, `setQuantity`.
2. TODO 4: `count`, `total`-ийг `reduce`-ээр.
3. `App.jsx` — TODO 5: `CartProvider`, `cart` route.
4. `components/Header.jsx` — TODO 6: сагсны холбоос ба тоо.
5. `components/ProductCard.jsx`, `pages/ProductDetail.jsx` — TODO 7:
   «Сагсанд нэмэх» товч.
6. `pages/Cart.jsx` — TODO 8: `useCart()`-ийг холбож, товчнуудад `onClick` өг.

«Тооцоо хийх» холбоос одоохондоо 404 рүү очно — дараагийн хичээлд.

### Нэмэлт сорилт

- Сагсыг `localStorage`-д хадгал: `useReducer(cartReducer, [], load)` —
  гурав дахь аргумент нь анхны утгыг уншина, `useEffect` нь өөрчлөлт бүрийг
  бичнэ.
- Тоо ширхэгийг үлдэгдлээс (`stock`) хэтрүүлэхгүй болго.

```quiz
Энэ reducer-ийн алдаа юу вэ?

`case "add": items.push({ ...action.product, quantity: 1 }); return items;`
- [ ] `push` нь зөвхөн тоо нэмдэг
- [x] Анхны массивыг өөрчилж, ижил reference буцаадаг тул React дахин render хийхгүй
- [ ] `return` шаардлагагүй
> Reducer үргэлж шинэ массив буцаана: `return [...items, newItem];`
```

```quiz
`count`-ийг тусдаа `useState`-д хадгалахын оронд `items`-ээс тооцоолох нь яагаад дээр вэ?
- [x] Хоёр state зөрөх боломжгүй — нэг үнэн эх сурвалж
- [ ] `useState` context дотор ажилладаггүй
- [ ] `reduce` нь `useState`-ээс хурдан
> Бусад state-ээс гаргаж болох утгыг render бүрт тооцоолно (Модул 3, «уламжлагдсан утга»).
```

### Дүгнэлт

Reducer нь сагсны бүх дүрмийг нэг цэвэр функцэд, context нь сагсыг апп
даяар хүргэнэ. Component-ууд `useCart()`-аас `add`, `count` зэрэг хэрэгтэй
зүйлээ л авна. `count`, `total` мэт уламжлагдсан утгыг тооцоолж, хэзээ ч
тусад нь хадгалахгүй.
""",
            initial_code=project(
                [
                    ("context/CartContext.jsx", CART_CONTEXT_START),
                    ("App.jsx", APP_5_START),
                    ("components/Header.jsx", HEADER_5_START),
                    ("components/ProductCard.jsx", PRODUCT_CARD_5_START),
                    ("pages/ProductDetail.jsx", DETAIL_5_START),
                    ("pages/Cart.jsx", CART_5_START),
                ],
                [
                    ("api.js", API_3),
                    ("format.js", FORMAT_JS),
                    ("components/Layout.jsx", LAYOUT),
                    ("pages/Home.jsx", HOME),
                    ("pages/Products.jsx", PRODUCTS_4),
                    ("pages/NotFound.jsx", NOT_FOUND),
                ],
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐⭐ · 40 минут

«Заавар»-ын алхмуудыг дагаж `TODO 1`–`TODO 8`-ийг дарааллаар нь гүйцээ:
эхлээд reducer, дараа нь provider, эцэст нь толгой, товчнууд, сагсны
хуудас. Алхам бүрийн дараа «Хөтөч» дээр бараа нэмж шалгаарай.
""",
                tests=(
                    test(
                        "cartReducer нь нэмэх, тоо солих, хасах үед шинэ массив буцаана",
                        """
const { cartReducer } = mod("./context/CartContext");
const banana = { id: 1, name: "Банана", price: 3500, emoji: "🍌", category: "Жимс", stock: 24 };
const apple = { id: 2, name: "Алим", price: 2800, emoji: "🍎", category: "Жимс", stock: 40 };
const empty = [];
let items = cartReducer(empty, { type: "add", product: banana });
expect(empty).toEqual([]);
items = cartReducer(items, { type: "add", product: banana });
items = cartReducer(items, { type: "add", product: apple });
expect(items.map((item) => [item.id, item.name, item.price, item.quantity])).toEqual([
  [1, "Банана", 3500, 2],
  [2, "Алим", 2800, 1],
]);
const before = items;
items = cartReducer(items, { type: "setQuantity", id: 2, quantity: 5 });
expect(before[1].quantity).toBe(1);
expect(items[1].quantity).toBe(5);
items = cartReducer(items, { type: "setQuantity", id: 2, quantity: 0 });
expect(items.map((item) => item.id)).toEqual([1]);
expect(cartReducer(items, { type: "remove", id: 1 })).toEqual([]);
""",
                    ),
                    test(
                        "Дэлгэрэнгүй хуудасны «Сагсанд нэмэх» толгой дахь сагсны тоог нэмэгдүүлнэ",
                        CART_LINK_JS
                        + """
setPath("/products/1");
await runMain();
const add = await screen.findByRole("button", { name: /Сагсанд нэмэх/ });
await user.click(add);
await user.click(add);
expect(cartLink()).toBeTruthy();
expect(cartLink()).toHaveTextContent("2");
""",
                    ),
                    test(
                        "Каталогийн карт бүр «Сагсанд нэмэх» товчтой, дууссан барааных идэвхгүй",
                        CART_LINK_JS
                        + """
setPath("/products");
await runMain();
await screen.findByRole("link", { name: "Банана" });
const buttons = screen.getAllByRole("button", { name: /Сагсанд нэмэх/ });
expect(buttons).toHaveLength(10);
expect(buttons[5]).toBeDisabled();
await user.click(buttons[0]);
await user.click(buttons[1]);
await user.click(buttons[1]);
expect(cartLink()).toHaveTextContent("3");
""",
                    ),
                    test(
                        "Сагсны хуудас нийт үнийг харуулж, нэмэх, хасах, устгах товчнууд ажиллана",
                        CART_LINK_JS
                        + """
setPath("/products");
await runMain();
await screen.findByRole("link", { name: "Банана" });
const buttons = screen.getAllByRole("button", { name: /Сагсанд нэмэх/ });
await user.click(buttons[0]);
await user.click(buttons[0]);
await user.click(buttons[1]);
await user.click(cartLink());
expect(await screen.findByRole("heading", { level: 1, name: "Сагс" })).toBeInTheDocument();
expect(screen.text()).toMatch(/Нийт:? ?9,800 ?₮/);
await user.click(screen.getByRole("button", { name: /Банана.*нэмэх/ }));
expect(screen.text()).toMatch(/Нийт:? ?13,300 ?₮/);
await user.click(screen.getByRole("button", { name: /Алим.*устгах/ }));
expect(screen.queryByText("Алим")).toBeNull();
expect(screen.text()).toMatch(/Нийт:? ?10,500 ?₮/);
for (let i = 0; i < 3; i += 1) {
  await user.click(screen.getByRole("button", { name: /Банана.*хасах/ }));
}
expect(screen.text()).toContain("Сагс хоосон байна");
""",
                    ),
                ),
                tips="""\
- `add`: эхлээд `items.find(...)`-ээр байгаа эсэхийг шалга. Байвал
  `items.map(...)` дотор тухайн мөрийг `{ ...item, quantity: item.quantity + 1 }`
  болго, байхгүй бол `[...items, шинэМөр]`.
- `remove` ба `quantity <= 0`: `items.filter((item) => item.id !== action.id)`.
- `count`: `items.reduce((sum, item) => sum + item.quantity, 0)` — эхний утга
  `0`-ийг мартвал хоосон сагсанд алдаа гарна.
- «useCart-ийг <CartProvider> дотор дуудна уу» алдаа гарвал `App.jsx`-д
  provider нэмээгүй эсвэл `Routes`-ийг ороогоогүй байна.
- `Cart.jsx`-д `setQuantity(item.id, item.quantity - 1)` — 1-ээс хасахад
  reducer мөрийг өөрөө устгана.
""",
                solution=files(
                    ("context/CartContext.jsx", CART_CONTEXT_5),
                    ("App.jsx", APP_5),
                    ("components/Header.jsx", HEADER_5),
                    ("components/ProductCard.jsx", PRODUCT_CARD_5),
                    ("pages/ProductDetail.jsx", DETAIL_5),
                    ("pages/Cart.jsx", CART_5),
                ),
            ),
        ),
        # ------------------------------------------------------------------ 14.6
        LessonSpec(
            title="Төлбөр тооцоо",
            slug="capstone-tootsoo",
            description="Хүргэлтийн формыг баталгаажуулж, захиалгыг POST /api/orders-оор илгээн, амжилтын хуудас руу шилжинэ.",
            duration=2400,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Хүргэлтийн формыг баталгаажуулалт, хүртээмжтэй алдаатай бүтээх
- `useMutation`-оор захиалгыг `POST /api/orders` руу илгээх
- Амжилтын дараа сагсыг хоослож, амжилтын хуудас руу шилжих

> **Дэмжлэг: хагас чиглүүлэгтэй.** Шаардлага, дизайн, API-ийн
> тодорхойлолт өгөгдөнө. Component, state, функцээ хэрхэн хуваахыг өөрөө
> шийднэ. Модул 4 (форм) ба Модул 9 (`useMutation`)-ийг эргэн саная.

### Яагаад чухал вэ

Тооцооны хуудас бол дэлгүүрийн хамгийн «үнэтэй» хуудас: хэрэглэгч энд
орхивол худалдан авалт алга. Ойлгомжгүй алдаа, давхар дарсан товчноос
үүссэн хоёр захиалга, амжилттай эсэхийг хэлдэггүй форм — бүгд шууд
алдагдал.

### Шаардлага

1. `/checkout` — h1 «Тооцоо хийх», хоёр хэсэг: хүргэлтийн форм ба
   «Таны захиалга» (бараа × тоо, мөрийн үнэ, нийт үнэ).
2. Сагс хоосон бол форм биш «Сагс хоосон байна» ба бараа руу холбоос.
3. Талбарууд (label яг ийм):

| Label | `name` | Дүрэм | Алдааны мессеж |
|---|---|---|---|
| Нэр | `name` | 2-оос доошгүй тэмдэгт | Нэрээ оруулна уу |
| Утас | `phone` | Яг 8 цифр | Утасны дугаар 8 оронтой тоо байна |
| Имэйл | `email` | `нэр@домэйн.mn` | Имэйлээ зөв оруулна уу |
| Хүргэлтийн хаяг | `address` | 5-аас доошгүй тэмдэгт | Хүргэлтийн хаягаа дэлгэрэнгүй бичнэ үү |

4. Алдаа илгээх үед харагдана: талбар `aria-invalid="true"`,
   `aria-describedby`-гаар мессежээ заана, мессеж `role="alert"`. Фокус
   **эхний алдаатай талбар** руу шилжинэ.
5. «Захиалах» товч — илгээж байх үед `disabled` ба «Илгээж байна…».
   Серверийн алдаанд `role="alert"` мессеж.
6. Амжилттай бол сагс хоосорч, `/checkout/success` хуудсанд «Захиалга
   амжилттай!» ба «Захиалгын дугаар: #1».

### API

```text
POST /api/orders
{
  "email": "saraa@example.mn",
  "customer": { "name": "Сараа", "phone": "99112233", "address": "СБД, 1-р хороо" },
  "items": [
    { "productId": 1, "name": "Банана", "price": 3500, "emoji": "🍌", "quantity": 2 }
  ],
  "total": 7000,
  "status": "new",
  "createdAt": "2026-09-28T10:00:00.000Z"
}
→ 201 { "id": 1, …илгээсэн талбарууд }
```

`api.js`-д `request`-ийг ашиглан `createOrder(order)` нэм. Бодит
дэлгүүрт `total`, `status`, `createdAt`-ийг **сервер** өөрөө тооцдог —
хөтчөөс ирсэн үнэд хэзээ ч итгэхгүй. Дадлагын API илгээснийг л
хадгалдаг тул энд бид бүрдүүлж илгээнэ.

### Дизайн

```text
Тооцоо хийх
┌ Хүргэлтийн мэдээлэл ──────────┐  ┌ Таны захиалга ──────────┐
│ Нэр              [          ] │  │ 🍌 Банана × 2    7,000₮ │
│ Утас             [          ] │  │ ──────────────────────  │
│ Имэйл            [          ] │  │ Нийт: 7,000₮            │
│ Хүргэлтийн хаяг  [          ] │  └─────────────────────────┘
│ [ Захиалах ]                  │
└───────────────────────────────┘
```

`.checkout-grid` загвар бэлэн: утсан дээр нэг багана болно. Хоёр хэсгийг
`<form aria-labelledby>`, `<aside aria-labelledby>`-аар гарчигтай нь холбо.

### useMutation-ийг санацгаая

```jsx
const placeOrder = useMutation({
  mutationFn: createOrder,
  onSuccess: (order) => {
    // сагс хоослох, амжилтын хуудас руу шилжих
  },
});

placeOrder.mutate(orderData);
placeOrder.isPending; // илгээж байна
placeOrder.isError;   // алдаа гарсан
```

- Дараагийн хуудас руу өгөгдөл дамжуулах: `navigate("/checkout/success",
  { state: { orderId: order.id } })`, тэнд `useLocation().state`.
- `queryClient.invalidateQueries({ queryKey: ["orders"] })` — дараагийн
  хичээлийн захиалгын жагсаалт шинэ захиалгаа харуулна.

### Хүртээмжийн жижиг зүйлс

- Эхний алдаатай талбар руу фокус: `event.currentTarget.elements.namedItem("phone").focus()`.
  Дэлгэц уншигч алдааг шууд уншиж, хэрэглэгч засахаа мэднэ.
- `autoComplete="name"`, `"tel"`, `"email"`, `"street-address"` —
  хөтөч автоматаар бөглөнө. `type="tel"` утсан дээр тоон гар нээнэ.
- Формд `noValidate` өг — хөтчийн өөрийн бөмбөлөг биш, өөрийн мессеж.

```quiz
«Захиалах» товчийг илгээж байх үед яагаад идэвхгүй болгох вэ?
- [ ] Товч гоё харагдана
- [x] Хэрэглэгч дахин дарж давхар захиалга үүсгэхээс сэргийлнэ
- [ ] `useMutation` үүнийг шаарддаг
> Удаан сүлжээнд хэрэглэгч «ажиллахгүй байна» гэж бодоод дахин дардаг. `isPending` үед `disabled` өг.
```

```quiz
Бодит дэлгүүрт захиалгын нийт үнийг юунаас тооцох ёстой вэ?
- [ ] Хөтчөөс ирсэн `total`-оос
- [x] Серверийн өгөгдлийн сангийн үнэ ба ирсэн тоо ширхэгээс
- [ ] `localStorage`-д хадгалсан сагснаас
> Хөтчөөс ирсэн бүхнийг хэрэглэгч өөрчилж чадна. Үнэ, төлвийг сервер өөрөө тооцно.
```

### Дүгнэлт

Тооцооны хуудас нь форм, баталгаажуулалт, хүртээмж, серверт бичих,
глобал state (сагс), навигацийг нэг дор хэрэглэдэг. `isPending`-ээр
давхар илгээлтээс сэргийлж, `onSuccess`-д сагсаа хоосолж, хэрэглэгчийг
тодорхой амжилтын хуудас руу аваачна.
""",
            initial_code=project(
                [
                    ("pages/Checkout.jsx", CHECKOUT_START),
                    ("pages/OrderSuccess.jsx", ORDER_SUCCESS_START),
                    ("App.jsx", APP_6_START),
                    ("api.js", API_6_START),
                ],
                [
                    ("context/CartContext.jsx", CART_CONTEXT_5),
                    ("format.js", FORMAT_JS),
                    ("components/Header.jsx", HEADER_5),
                    ("components/Layout.jsx", LAYOUT),
                    ("components/ProductCard.jsx", PRODUCT_CARD_5),
                    ("pages/Home.jsx", HOME),
                    ("pages/Products.jsx", PRODUCTS_4),
                    ("pages/ProductDetail.jsx", DETAIL_5),
                    ("pages/Cart.jsx", CART_5),
                    ("pages/NotFound.jsx", NOT_FOUND),
                ],
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐⭐ · 40 минут

«Заавар»-ын шаардлага, дизайн, API-ийн дагуу тооцооны хуудас ба амжилтын
хуудсыг бүтээ. `api.js`-д `createOrder` нэмж, `App.jsx`-д хоёр route-ийг
бүртгэ. Каталогоос бараа сагсалж «Хөтөч» дээр бүтэн урсгалыг шалга.
""",
                tests=(
                    test(
                        "Тооцооны хуудас сагсны бараа ба нийт үнийг харуулна",
                        CHECKOUT_SETUP_JS
                        + """
expect(await screen.findByRole("heading", { level: 1, name: /Тооцоо/ })).toBeInTheDocument();
expect(screen.text()).toContain("Банана");
expect(screen.text()).toMatch(/7,000 ?₮/);
""",
                    ),
                    test(
                        'Буруу утганд алдаа бүр role="alert", aria-invalid-тай харагдаж, фокус эхний алдаатай талбарт очно',
                        CHECKOUT_SETUP_JS
                        + """
await user.type(await screen.findByLabelText("Утас"), "9911");
await user.click(screen.getByRole("button", { name: "Захиалах" }));
expect(screen.getAllByRole("alert").length).toBeGreaterThanOrEqual(4);
for (const label of ["Нэр", "Утас", "Имэйл", "Хүргэлтийн хаяг"]) {
  const input = screen.getByLabelText(label);
  expect(input).toHaveAttribute("aria-invalid", "true");
  expect(input.getAttribute("aria-describedby")).toBeTruthy();
}
expect(screen.text()).toContain("Утасны дугаар 8 оронтой тоо байна");
expect(screen.getByLabelText("Нэр")).toHaveFocus();
expect(api.requests.some((request) => request.method === "POST")).toBe(false);
""",
                    ),
                    test(
                        "Зөв бөглөхөд захиалга POST /api/orders-оор API-ийн хэлбэрээр илгээгдэнэ",
                        CHECKOUT_SETUP_JS
                        + CHECKOUT_FILL_JS
                        + """
await user.click(screen.getByRole("button", { name: "Захиалах" }));
await waitFor(() => expect(api.get("orders")).toHaveLength(1));
const [order] = api.get("orders");
expect(order.email).toBe("saraa@example.mn");
expect(order.customer).toEqual({ name: "Сараа", phone: "99112233", address: "СБД, 1-р хороо, 5-р байр" });
expect(order.items).toHaveLength(1);
expect(order.items[0]).toHaveProperty("productId", 1);
expect(order.items[0]).toHaveProperty("price", 3500);
expect(order.items[0]).toHaveProperty("quantity", 2);
expect(order.total).toBe(7000);
expect(order.status).toBe("new");
expect(typeof order.createdAt).toBe("string");
""",
                    ),
                    test(
                        "Амжилттай бол захиалгын дугаартай амжилтын хуудас нээгдэж, сагс хоосорно",
                        CHECKOUT_SETUP_JS
                        + CHECKOUT_FILL_JS
                        + """
await user.click(screen.getByRole("button", { name: "Захиалах" }));
await waitFor(() => expect(screen.text()).toMatch(/амжилттай/i));
expect(screen.text()).toMatch(/# ?1/);
expect(cartLink()).toHaveTextContent("0");
""",
                    ),
                    test(
                        "Илгээж байх үед «Захиалах» товч идэвхгүй болж, давхар захиалга үүсэхгүй",
                        CHECKOUT_SETUP_JS
                        + CHECKOUT_FILL_JS
                        + """
api.delay = 300;
const submit = screen.getByRole("button", { name: "Захиалах" });
await user.click(submit);
expect(submit).toBeDisabled();
await user.click(submit);
await waitFor(() => expect(screen.text()).toMatch(/амжилттай/i));
expect(api.get("orders")).toHaveLength(1);
""",
                    ),
                ),
                tips="""\
- Формын бүтэц Модул 4-ийн төсөлтэй ижил: нэг `values` объект, render
  бүрт `validate(values)`, `submitted` үнэн үед л алдааг харуул.
- `useCart()` дотор `items`, `total`, `clear` бэлэн байгаа.
- Захиалгын `items`-д сагсны `id`-г `productId` болгож хувирга:
  `items.map(({ id, ...rest }) => ({ productId: id, ...rest }))`.
- Фокус: `handleSubmit` дотор алдаатай эхний талбарын `name`-ийг олоод
  `event.currentTarget.elements.namedItem(name).focus()`.
- Амжилтын дараа `clear()` ба `navigate(...)`-ийг `onSuccess`-д дууд —
  `mutate()`-ийн дараа шууд дуудвал хүсэлт дуусаагүй байхад сагс хоосорно.
- Амжилтын хуудас `state`-гүй (жишээ нь хаягаар шууд) нээгдэж болно:
  `state?.orderId`.
""",
                solution=files(
                    ("pages/Checkout.jsx", CHECKOUT_6),
                    ("pages/OrderSuccess.jsx", ORDER_SUCCESS_6),
                    ("App.jsx", APP_6),
                    ("api.js", API_6),
                ),
            ),
        ),
        # ------------------------------------------------------------------ 14.7
        LessonSpec(
            title="Нэвтрэх ба хамгаалагдсан хуудас",
            slug="capstone-nevtreh",
            description="AuthContext-оор дадлагын нэвтрэлт хийж, хамгаалагдсан route ба захиалгатай профайл хуудас бүтээнэ.",
            duration=2400,
            language=JSX,
            content="""\
### Энэ хичээлээр

- `AuthContext`-оор нэвтэрсэн хэрэглэгчийг апп даяар хуваалцах
- Хамгаалагдсан route: нэвтрээгүй бол `/login` руу шилжүүлж, нэвтэрсний
  дараа анх очих гэсэн хуудас руу нь буцаах
- Профайл хуудсанд хэрэглэгчийн захиалгуудыг API-аас татах

> **Дэмжлэг: хагас чиглүүлэгтэй.** Шаардлага, context-ийн API, серверийн
> API өгөгдөнө. Хуудас, component-ийн дотоод бүтцийг өөрөө шийднэ.

### ⚠️ Энэ нэвтрэлт хуурамч

Бидэнд жинхэнэ сервер байхгүй тул нэвтрэлтийг хөтөч дээр **дуурайна**:
дурын имэйл, нууц үг нь `nogoon123`. `admin@nogoon.mn` бол админ (дараагийн
хичээлд). Бодит апп-д:

- Нууц үгийг HTTPS-ээр серверт илгээж, сервер шалгана. Хөтөч дээрх кодыг
  хэрэглэгч бүр харж, өөрчилж чаддаг тул тэнд хийсэн шалгалт хамгаалалт биш.
- Сервер `httpOnly` cookie (session) эсвэл токен буцаана. Нууц үгийг
  `localStorage`-д хэзээ ч хадгалахгүй.
- Эрхийг (админ эсэх) сервер API бүр дээр шалгана. Frontend зөвхөн цэс,
  товчийг нууж харуулна.
- Ихэвчлэн бэлэн шийдэл хэрэглэдэг: Auth.js, Clerk, Supabase Auth, Firebase Auth.

Гэхдээ **React талын бүтэц** — context, хамгаалагдсан route, redirect —
бодит апп-тай яг ижил.

### Яагаад чухал вэ

Нэвтэрсэн хэрэглэгчийн мэдээллийг толгой, профайл, тооцоо, админ зэрэг
олон хэсэг хэрэглэнэ — тиймээс context. Хэрэглэгч «Профайл» дарахад
нэвтрэх хуудас гарч, нэвтэрсний дараа **профайл руугаа** буцах нь заавал
байх ёстой туршлага. Нүүр хуудас руу шидвэл хэрэглэгч замаа дахин хайна.

### Шаардлага

1. **`context/AuthContext.jsx`** — `useAuth()` нь `{ user, login, logout }`
   буцаана:
   - `user` — `null` эсвэл `{ email, name, isAdmin }`. `name` нь имэйлийн
     `@`-ийн өмнөх хэсэг, `isAdmin` нь `email === ADMIN_EMAIL`.
   - `login(email, password)` — нууц үг буруу бол
     `Error("Имэйл эсвэл нууц үг буруу байна")` шиднэ.
   - `logout()` — `user`-ийг `null` болгоно.
2. **`/login`** — h1 «Нэвтрэх», «Имэйл», «Нууц үг» (`type="password"`)
   label-тэй талбар, «Нэвтрэх» товч, дадлагын нууц үгийн тайлбар. Алдаа
   `role="alert"`. Амжилттай бол `location.state.from` эсвэл `/profile` руу.
3. **`components/ProtectedRoute.jsx`** — layout route: нэвтрээгүй бол
   `<Navigate to="/login" replace state={{ from: … }} />`, эс бөгөөс
   `<Outlet />`. `/profile` түүний дотор.
4. **Толгой** — нэвтрээгүй: «Нэвтрэх» холбоос. Нэвтэрсэн: «Профайл»
   холбоос ба «Гарах» товч.
5. **`/profile`** — h1 «Профайл», нэр, имэйл, h2 «Миний захиалгууд»:
   дугаар (`#101`), огноо, төлөв (`ORDER_STATUS`), нийт үнэ. Ачаалах,
   алдаа, хоосон («Та одоогоор захиалга хийгээгүй байна») төлөвтэй.

### API

```text
GET /api/orders?email=bat@example.mn   → тухайн имэйлийн захиалгууд
```

Дадлагын API query параметрийн талбараар шүүдэг. `api.js`-д
`getOrders(email)` нэм — `encodeURIComponent(email)`-ийг мартуузай (`@`,
`+` тэмдэгт). Бодит серверт `GET /api/me/orders` гэх мэт — сервер
хэрэглэгчийг токеноос нь таньдаг тул өөр хүний имэйл бичээд захиалгыг нь
харах боломжгүй.

### Хамгаалагдсан route

```jsx
<Route element={<ProtectedRoute />}>
  <Route path="profile" element={<Profile />} />
</Route>
```

```jsx
// ProtectedRoute
if (!user) {
  return <Navigate to="/login" replace state={{ from: location.pathname }} />;
}
return <Outlet />;
```

```jsx
// Login — амжилттай бол
navigate(location.state?.from ?? "/profile", { replace: true });
```

`replace` — `/profile` түүхэнд үлдэхгүй, «буцах» дарахад дахин `/login`
руу шидэгдэх гогцоо үүсэхгүй. Дараа нь `/admin`, `/orders` ч энэ route
дотор орно — нэг газар хамгаална.

### Нэмэлт сорилт

- Хуудсыг дахин ачаалахад нэвтэрсэн хэвээр үлдээ: `localStorage`-д хадгалж,
  `useState(() => …)`-ийн lazy анхны утгаар уншина.
- Тооцооны хуудсанд нэвтэрсэн хэрэглэгчийн имэйлийг урьдчилан бөглө.
- Гарахад `queryClient.removeQueries({ queryKey: ["orders"] })` — дараагийн
  хэрэглэгч өмнөхийн захиалгыг кэшээс харахгүй.

```quiz
`<Navigate to="/login" replace />`-д `replace` юунд хэрэгтэй вэ?
- [ ] Хуудас хурдан ачаална
- [x] «Буцах» дарахад хамгаалагдсан хуудас руу орж, дахин /login руу шидэгдэх гогцооноос сэргийлнэ
- [ ] `state` дамжуулахад заавал хэрэгтэй
> `replace` нь түүхийн одоогийн мөрийг солино — хамгаалагдсан хаяг түүхэнд үлдэхгүй.
```

```quiz
Админ цэсийг `user.isAdmin` үед л харуулдаг боллоо. Энэ нь админы API-г хамгаалах уу?
- [ ] Тийм — цэс харагдахгүй бол хэн ч хандахгүй
- [x] Үгүй — хүсэлтийг хэн ч шууд илгээж чадна, эрхийг сервер шалгах ёстой
> Frontend-ийн шалгалт нь зөвхөн хэрэглэгчийн туршлагад. Аюулгүй байдал үргэлж сервер дээр.
```

### Дүгнэлт

Нэвтрэлт нь context (хэн нэвтэрсэн), хамгаалагдсан layout route (хаана
хэн орох), redirect (`state.from`) гэсэн гурван хэсгээс бүрдэнэ. Энэ
бүтэц жинхэнэ auth сан ашиглахад ч өөрчлөгдөхгүй — зөвхөн `login` доторх
код сервер рүү явна.
""",
            initial_code=project(
                [
                    ("context/AuthContext.jsx", AUTH_CONTEXT_START),
                    ("components/ProtectedRoute.jsx", PROTECTED_START),
                    ("pages/Login.jsx", LOGIN_START),
                    ("pages/Profile.jsx", PROFILE_START),
                    ("App.jsx", APP_7_START),
                    ("components/Header.jsx", HEADER_7_START),
                    ("api.js", API_7_START),
                ],
                [
                    ("context/CartContext.jsx", CART_CONTEXT_5),
                    ("format.js", FORMAT_JS),
                    ("components/Layout.jsx", LAYOUT),
                    ("components/ProductCard.jsx", PRODUCT_CARD_5),
                    ("pages/Home.jsx", HOME),
                    ("pages/Products.jsx", PRODUCTS_4),
                    ("pages/ProductDetail.jsx", DETAIL_5),
                    ("pages/Cart.jsx", CART_5),
                    ("pages/Checkout.jsx", CHECKOUT_6),
                    ("pages/OrderSuccess.jsx", ORDER_SUCCESS_6),
                    ("pages/NotFound.jsx", NOT_FOUND),
                ],
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐⭐ · 40 минут

«Заавар»-ын шаардлагын дагуу `AuthContext`, нэвтрэх хуудас, хамгаалагдсан
route, профайл хуудсыг бүтээж, толгой ба `App.jsx`-д холбо. Дадлагын нууц
үг: `nogoon123`. Профайлд захиалга харахын тулд эхлээд тооцоогоор нэг
захиалга хий.
""",
                tests=(
                    test(
                        "Нэвтрээгүй үед /profile хаяг нэвтрэх хуудас руу шилжүүлнэ",
                        """
setPath("/profile");
await runMain();
expect(await screen.findByRole("heading", { level: 1, name: "Нэвтрэх" })).toBeInTheDocument();
expect(screen.getByLabelText("Имэйл")).toBeInTheDocument();
expect(screen.getByLabelText("Нууц үг")).toHaveAttribute("type", "password");
""",
                    ),
                    test(
                        'Буруу нууц үгэнд role="alert" алдаа гарч, нэвтрэхгүй',
                        """
setPath("/login");
await runMain();
await user.type(await screen.findByLabelText("Имэйл"), "bat@example.mn");
await user.type(screen.getByLabelText("Нууц үг"), "12345678");
await user.click(screen.getByRole("button", { name: "Нэвтрэх" }));
expect(await screen.findByRole("alert")).toHaveTextContent(/буруу/);
expect(within(screen.getByRole("banner")).getByRole("link", { name: "Нэвтрэх" })).toBeInTheDocument();
""",
                    ),
                    test(
                        "Зөв нэвтэрвэл профайл нээгдэж, толгойд «Профайл» ба «Гарах» харагдана",
                        LOG_IN_JS
                        + """
setPath("/profile");
await runMain();
await logIn("bat@example.mn");
expect(await screen.findByRole("heading", { level: 1, name: "Профайл" })).toBeInTheDocument();
expect(screen.text()).toContain("bat@example.mn");
const header = within(screen.getByRole("banner"));
expect(header.getByRole("link", { name: "Профайл" })).toBeInTheDocument();
expect(header.getByRole("button", { name: "Гарах" })).toBeInTheDocument();
expect(header.queryByRole("link", { name: "Нэвтрэх" })).toBeNull();
""",
                    ),
                    test(
                        "Профайл нь зөвхөн нэвтэрсэн хэрэглэгчийн захиалгуудыг API-аас татаж харуулна",
                        ORDERS_JS
                        + LOG_IN_JS
                        + """
setPath("/profile");
await runMain();
await logIn("bat@example.mn");
await screen.findByRole("heading", { level: 1, name: "Профайл" });
await waitFor(() => expect(screen.text()).toContain("#101"));
const text = screen.text();
expect(text).toContain("#103");
expect(text).toContain("#104");
expect(text).not.toContain("#102");
expect(text).toContain("Хүргэлтэд");
expect(text).toMatch(/9,200 ?₮/);
expect(api.requests.some((request) => request.method === "GET" && request.path.startsWith("/api/orders"))).toBe(true);
""",
                    ),
                    test(
                        "«Гарах» дарахад гарч, толгойд дахин «Нэвтрэх» харагдана",
                        LOG_IN_JS
                        + """
setPath("/profile");
await runMain();
await logIn("bat@example.mn");
await screen.findByRole("heading", { level: 1, name: "Профайл" });
await user.click(screen.getByRole("button", { name: "Гарах" }));
const header = within(screen.getByRole("banner"));
expect(await header.findByRole("link", { name: "Нэвтрэх" })).toBeInTheDocument();
expect(header.queryByRole("link", { name: "Профайл" })).toBeNull();
expect(screen.text()).not.toContain("bat@example.mn");
""",
                    ),
                ),
                tips="""\
- `AuthContext`-ийн бүтэц `CartContext`-тэй ижил: `createContext`,
  provider component, `useAuth` hook. Энд reducer хэрэггүй — `useState`
  хангалттай.
- `login` дотор алдаа **шид** (`throw new Error(...)`), `Login` хуудас нь
  `try/catch`-аар барьж state-д хадгална.
- `App.jsx`-д `AuthProvider` нь `Routes`-ийг бүхэлд нь ороох ёстой
  (`Header` ч `useAuth`-ийг дуудна). `CartProvider`-ын гадна ч, дотор ч болно.
- `ProtectedRoute` нь `Outlet` буцаадаг layout route: `<Route element={<ProtectedRoute />}>`
  дотор `profile` route.
- `Profile`: `queryKey`-д имэйлийг оруул (`["orders", user.email]`) —
  өөр хэрэглэгч нэвтрэхэд өөр кэш.
- `logout` хийхэд `/profile` дээр байсан бол `ProtectedRoute` өөрөө
  `/login` руу шилжүүлнэ.
- `Login`-д «аль хэдийн нэвтэрсэн бол шилжүүлэх» (`if (user) return <Navigate … />`)
  нэмбэл `from` руу чиглүүл — `"/profile"` гэж хатуу бичвэл нэвтэрсэн
  даруйд `navigate(from)`-ийг дарж, хэрэглэгчийг буруу хуудас руу аваачна.
""",
                solution=files(
                    ("context/AuthContext.jsx", AUTH_CONTEXT_7),
                    ("components/ProtectedRoute.jsx", PROTECTED_7),
                    ("pages/Login.jsx", LOGIN_7),
                    ("pages/Profile.jsx", PROFILE_7),
                    ("App.jsx", APP_7),
                    ("components/Header.jsx", HEADER_7),
                    ("api.js", API_7),
                ),
            ),
        ),
        # ------------------------------------------------------------------ 14.8
        LessonSpec(
            title="Админ: бараа нэмэх, засах",
            slug="capstone-admin",
            description="Зөвхөн админд нээгдэх хуудсанд бараа нэмэх (POST), засах (PATCH) ба кэшийг шинэчлэх боломж бүтээнэ.",
            duration=2400,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Зөвхөн админд нээгдэх route бүтээх
- `useMutation`-оор бараа нэмэх (`POST`), засах (`PATCH`)
- `invalidateQueries`-ээр кэшийг шинэчилж, бүх хуудсанд шинэ өгөгдөл харуулах

> **Дэмжлэг: хагас чиглүүлэгтэй.** Шаардлага, дизайн, API өгөгдөнө.
> Хуудсын component, state-ийн бүтцийг өөрөө шийднэ.

### Яагаад чухал вэ

Дэлгүүрийн эзэн бананы үнийг өөрчиллөө. Хэрэглэгч каталогт хуучин үнийг,
сагсанд шинэ үнийг харвал итгэл алдагдана. Серверийн өгөгдлийг өөрчилсний
дараа **хаана хаана** хуучин хуулбар (кэш) байгааг мэдэж, шинэчлэх нь
бодит апп-ын хамгийн түгээмэл алдааны эх үүсвэр.

### Шаардлага

1. **Хандалт.** `/admin` — нэвтрээгүй бол `/login`, нэвтэрсэн ч админ биш
   бол h1 «Хандах эрхгүй». `ProtectedRoute`-д `adminOnly` prop нэм. Толгойн
   цэсэнд «Админ» холбоос зөвхөн админд (`admin@nogoon.mn`).
2. **«Шинэ бараа» форм** — `aria-labelledby`-гаар «Шинэ бараа» гарчигтайгаа
   холбогдсон. Талбарууд: «Нэр», «Үнэ», «Ангилал» (select: Жимс, Ногоо,
   Сүүн бүтээгдэхүүн, Гурил, Бусад), «Эмодзи», «Үлдэгдэл»; «Нэмэх» товч.
   - Нэр хоосон биш; үнэ 1-ээс их буюу тэнцүү бүхэл тоо; үлдэгдэл 0-ээс их
     буюу тэнцүү бүхэл тоо.
   - Алдаатай бол `aria-invalid`, `role="alert"` мессеж, хүсэлт илгээхгүй.
3. **Хүснэгт** — `<table>`, `<caption>`, `<th scope="col">`: бараа, ангилал,
   үнэ, үлдэгдэл. Мөр бүрт «Засах» товч, `aria-label="Засах: Банана"`.
4. **Засах форм** — «Засах: Банана» гарчигтай (`aria-labelledby`): «Үнэ»,
   «Үлдэгдэл», «Хадгалах», «Болих». Нээгдэхэд фокус «Үнэ» талбарт.
5. **Амжилттай бол** хүснэгт шинэчлэгдэж, `role="status"` мессеж
   («…нэмэгдлээ», «…шинэчлэгдлээ») гарна. Каталог, дэлгэрэнгүй хуудас ч шинэ
   утгаа шууд харуулна.

### API

```text
POST  /api/products      { name, price, category, emoji, stock }  → 201 { id, … }
PATCH /api/products/:id  { price, stock }                         → 200 бүтэн бараа
```

`api.js`-д `createProduct(product)`, `updateProduct(id, changes)` нэм.
`price`, `stock` нь **тоо** байна (`8900`, `"8900"` биш). Input-ийн
`event.target.value` нь `type="number"` байсан ч үргэлж string —
илгээхийн өмнө `Number(...)`.

### Дизайн

```text
Админ
«Тарвас» нэмэгдлээ.                      ← role="status"
┌ Шинэ бараа ──────┐  ┌ Бараанууд (11) ───────────────────────┐
│ Нэр      [     ] │  │ Бараа      Ангилал  Үнэ     Үлд.      │
│ Үнэ      [     ] │  │ 🍌 Банана  Жимс     3,500₮  24  Засах │
│ Ангилал  [Жимс▾] │  │ 🍎 Алим    Жимс     2,800₮  40  Засах │
│ Эмодзи   [     ] │  │ …                                     │
│ Үлдэгдэл [     ] │  └───────────────────────────────────────┘
│ [ Нэмэх ]        │
└──────────────────┘
┌ Засах: Банана ───┐   ← «Засах» дарсны дараа
│ Үнэ      [3500 ] │
│ Үлдэгдэл [24   ] │
│ [Хадгалах] [Болих]│
└──────────────────┘
```

`.admin-grid`, `.table-wrap` загвар бэлэн: утсан дээр хүснэгт хөндлөн
гүйлгэгдэнэ.

### Кэшийг шинэчлэх

🔒 `main.jsx`-д `staleTime: 60 * 1000` тул TanStack Query татсан өгөгдлийг
1 минут «шинэ» гэж үзэж, дахин татахгүй. Сервер дээр өөрчлөлт хийснээ
түүнд **өөрөө** хэлнэ:

```jsx
const queryClient = useQueryClient();

const addProduct = useMutation({
  mutationFn: createProduct,
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ["products"] });
  },
});
```

`["products"]`-оор **эхэлсэн** бүх түлхүүр — жагсаалт ба `["products", id]`
дэлгэрэнгүй — хуучирсан гэж тэмдэглэгдэж, одоо харагдаж байгаа нь шууд
дахин татагдана. Өөр аргууд: хариуг `setQueryData`-гаар кэшэд шууд бичих,
эсвэл хариу ирэхээс өмнө UI-г шинэчлэх optimistic update (Модул 11).

### Хүртээмж

- Хоёр форм хоёулаа «Үнэ» label-тэй. `aria-labelledby`-гаар нэрлэсэн форм
  нь дэлгэц уншигчид тусдаа landmark болж ялгарна.
- Хүснэгтийн «Засах» товч бүр `aria-label`-даа барааны нэртэй.
- «Засах» дарахад форм хүснэгтээс хол гарч ирдэг тул фокусыг түүн рүү
  шилжүүл (`autoFocus`; өөр бараа сонгоход дахин mount болгохын тулд
  формд `key={editing.id}`).

```quiz
`<input type="number">`-ийн `event.target.value` ямар төрөлтэй вэ?
- [ ] number
- [x] string
- [ ] Хэрэглэгчийн оруулснаас хамаарна
> Формын бүх утга string. Серверт илгээхийн өмнө `Number(value)`-ээр хөрвүүл.
```

```quiz
Үнийг PATCH-ээр өөрчилсний дараа `invalidateQueries` дуудаагүй бол каталогт юу харагдах вэ? (`staleTime` 1 минут)
- [ ] Шинэ үнэ — React өөрөө шинэчилнэ
- [x] Кэш хуучирсан гэж тооцогдох хүртэл хуучин үнэ
- [ ] Алдаа
> TanStack Query сервер дээр юу өөрчлөгдснийг мэдэхгүй. Mutation-ы дараа холбогдох түлхүүрүүдийг invalidate хийнэ.
```

### Дүгнэлт

Бичих үйлдэл (mutation) бүрийн дараа «энэ өгөгдлийг өөр хаана
харуулдаг вэ?» гэж асуу. Кэшийн түлхүүрийг зөв төлөвлөсөн бол нэг
`invalidateQueries` бүх хуудсыг шинэчилнэ. Админы эрхийг frontend-д
зөвхөн UI-д шалгадаг — жинхэнэ хамгаалалт сервер дээр.
""",
            initial_code=project(
                [
                    ("pages/Admin.jsx", ADMIN_START),
                    ("components/ProtectedRoute.jsx", PROTECTED_8_START),
                    ("App.jsx", APP_8_START),
                    ("components/Header.jsx", HEADER_8_START),
                    ("api.js", API_8_START),
                ],
                [
                    ("context/AuthContext.jsx", AUTH_CONTEXT_7),
                    ("context/CartContext.jsx", CART_CONTEXT_5),
                    ("format.js", FORMAT_JS),
                    ("components/Layout.jsx", LAYOUT),
                    ("components/ProductCard.jsx", PRODUCT_CARD_5),
                    ("pages/Home.jsx", HOME),
                    ("pages/Products.jsx", PRODUCTS_4),
                    ("pages/ProductDetail.jsx", DETAIL_5),
                    ("pages/Cart.jsx", CART_5),
                    ("pages/Checkout.jsx", CHECKOUT_6),
                    ("pages/OrderSuccess.jsx", ORDER_SUCCESS_6),
                    ("pages/Login.jsx", LOGIN_7),
                    ("pages/Profile.jsx", PROFILE_7),
                    ("pages/NotFound.jsx", NOT_FOUND),
                ],
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐⭐ · 45 минут

«Заавар»-ын шаардлага, дизайн, API-ийн дагуу админ хуудсыг бүтээ:
хандалтын хамгаалалт, бараа нэмэх форм, хүснэгт, засах форм. `admin@nogoon.mn`
/ `nogoon123`-ээр нэвтэрч «Хөтөч» дээр шалга.
""",
                tests=(
                    test(
                        "Энгийн хэрэглэгч админ хуудсанд хандах эрхгүй, цэсэнд «Админ» харагдахгүй",
                        LOG_IN_JS
                        + """
setPath("/admin");
await runMain();
await logIn("bat@example.mn");
await waitFor(() => expect(screen.text()).toMatch(/Хандах эрхгүй/));
expect(screen.queryByRole("form", { name: /Шинэ бараа/ })).toBeNull();
expect(within(screen.getByRole("banner")).queryByRole("link", { name: "Админ" })).toBeNull();
""",
                    ),
                    test(
                        "Админ шинэ бараа нэмэхэд POST /api/products тоон утгуудтай илгээгдэж, хүснэгтэд гарна",
                        ADMIN_LOG_IN_JS
                        + """
const form = await screen.findByRole("form", { name: /Шинэ бараа/ });
await screen.findByRole("table");
expect(within(screen.getByRole("banner")).getByRole("link", { name: "Админ" })).toBeInTheDocument();
await user.type(within(form).getByLabelText("Нэр"), "Тарвас");
await user.type(within(form).getByLabelText("Үнэ"), "8900");
await user.selectOptions(within(form).getByLabelText("Ангилал"), "Жимс");
await user.type(within(form).getByLabelText("Эмодзи"), "🍉");
await user.type(within(form).getByLabelText("Үлдэгдэл"), "5");
await user.click(within(form).getByRole("button", { name: /Нэмэх/ }));
await waitFor(() => expect(api.get("products")).toHaveLength(11));
const created = api.get("products")[10];
expect(created).toHaveProperty("name", "Тарвас");
expect(created).toHaveProperty("price", 8900);
expect(created).toHaveProperty("category", "Жимс");
expect(created).toHaveProperty("stock", 5);
await waitFor(() => expect(screen.getByRole("table")).toHaveTextContent("Тарвас"));
""",
                    ),
                    test(
                        "Буруу утгатай бараа нэмэхэд алдаа харагдаж, хүсэлт илгээгдэхгүй",
                        ADMIN_LOG_IN_JS
                        + """
const form = await screen.findByRole("form", { name: /Шинэ бараа/ });
await user.type(within(form).getByLabelText("Үнэ"), "0");
await user.click(within(form).getByRole("button", { name: /Нэмэх/ }));
expect(within(form).getAllByRole("alert").length).toBeGreaterThanOrEqual(2);
expect(within(form).getByLabelText("Нэр")).toHaveAttribute("aria-invalid", "true");
expect(within(form).getByLabelText("Үнэ")).toHaveAttribute("aria-invalid", "true");
expect(api.requests.some((request) => request.method === "POST")).toBe(false);
""",
                    ),
                    test(
                        "«Засах»-аар үнэ, үлдэгдлийг өөрчлөхөд PATCH /api/products/:id илгээгдэж, хүснэгт шинэчлэгдэнэ",
                        ADMIN_LOG_IN_JS
                        + EDIT_BANANA_JS
                        + """
const stock = within(editForm).getByLabelText("Үлдэгдэл");
await user.clear(stock);
await user.type(stock, "30");
await user.click(within(editForm).getByRole("button", { name: /Хадгалах/ }));
await waitFor(() => expect(api.get("products")[0].price).toBe(3900));
const request = api.requests.find((item) => item.method === "PATCH");
expect(request.path).toBe("/api/products/1");
expect(request.body).toHaveProperty("price", 3900);
expect(request.body).toHaveProperty("stock", 30);
await waitFor(() => expect(screen.getByRole("table")).toHaveTextContent(/3,900 ?₮/));
""",
                    ),
                    test(
                        "Засварласан үнэ каталогийн хуудсанд шууд харагдана",
                        LOG_IN_JS
                        + """
setPath("/products");
await runMain();
await screen.findByRole("link", { name: "Банана" });
expect(screen.text()).toMatch(/3,500 ?₮/);
await user.click(within(screen.getByRole("banner")).getByRole("link", { name: "Нэвтрэх" }));
await logIn("admin@nogoon.mn");
await user.click(await within(screen.getByRole("banner")).findByRole("link", { name: "Админ" }));
"""
                        + EDIT_BANANA_JS
                        + """
await user.click(within(editForm).getByRole("button", { name: /Хадгалах/ }));
await waitFor(() => expect(api.get("products")[0].price).toBe(3900));
await user.click(within(screen.getByRole("navigation")).getByRole("link", { name: "Бараа" }));
await screen.findByRole("link", { name: "Банана" });
await waitFor(() => expect(screen.text()).toMatch(/3,900 ?₮/));
expect(screen.text()).not.toMatch(/3,500 ?₮/);
""",
                    ),
                ),
                tips="""\
- `ProtectedRoute({ adminOnly = false })` — `user` байхгүй бол `/login`,
  `adminOnly && !user.isAdmin` бол «Хандах эрхгүй», эс бөгөөс `<Outlet />`.
  `App.jsx`-д `<Route element={<ProtectedRoute adminOnly />}>`.
- Хоёр форм тус бүр өөрийн state, `submitted` төлөвтэй. Засварлах state-ийг
  `null` (форм хаалттай) эсвэл `{ id, name, price, stock }` гэж хадгалж болно.
- Хүснэгтийг `useQuery({ queryKey: ["products"], … })`-ээр ав — каталогтой
  ижил түлхүүр. Mutation-ы `onSuccess`-д `queryClient.invalidateQueries({ queryKey: ["products"] })`.
- Серверт `Number(price)` илгээ. Бүхэл тоо эсэхийг шалгахдаа
  `Number.isInteger(Number(value))`.
- PATCH-д зөвхөн өөрчлөгдсөн талбарууд: `{ price, stock }`.
- `api.js`-ийн `request(path, { method: "PATCH", body: JSON.stringify(changes) })`.
""",
                solution=files(
                    ("pages/Admin.jsx", ADMIN_8),
                    ("components/ProtectedRoute.jsx", PROTECTED_8),
                    ("App.jsx", APP_8),
                    ("components/Header.jsx", HEADER_8),
                    ("api.js", API_8),
                ),
            ),
        ),
        # ------------------------------------------------------------------ 14.9
        LessonSpec(
            title="Бие даасан даалгавар: Захиалгын түүх",
            slug="capstone-bie-daasan",
            description="Зөвхөн бүтээгдэхүүний шаардлага ба хүлээн авах шалгуураар захиалгын түүх, шүүлтүүр, «Дахин захиалах» боломжийг бие дааж бүтээнэ.",
            duration=2700,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Бүтээгдэхүүний шаардлагаас эхлээд шийдлээ бие дааж төлөвлөх
- Өмнөх хичээлүүдийн хэв маягийг (query, context, URL state) шинэ
  боломжид хэрэглэх
- Ажлаа хүлээн авах шалгуураар (тестээр) баталгаажуулах

> **Дэмжлэг: бие даасан.** Зөвхөн бүтээгдэхүүний шаардлага, хүлээн авах
> шалгуур, техникийн хязгаарлалт өгнө. Аль файлд юу бичих, ямар component,
> state хэрэгтэйг өөрөө шийднэ. Тестүүд бол хүлээн авах шалгуур.

### Яагаад чухал вэ

Ажил дээр хэн ч «энэ мөрөнд ийм hook бич» гэж хэлэхгүй. Бүтээгдэхүүний
менежер «хэрэглэгчид өмнөх захиалгаа давтах амар арга хэрэгтэй» гэж л
хэлнэ. Үүнийг жижиг хэсгүүдэд задалж, хаана юу байхыг шийдэж, кодлоод,
шалгуураар баталгаажуулах нь хөгжүүлэгчийн жинхэнэ ажил.

### Бүтээгдэхүүний шаардлага

> «Байнгын худалдан авагчийн хувьд өмнөх захиалгуудаа нэг дор харж,
> дуртай захиалгаа нэг товчоор дахин сагсалмаар байна.»

### Хүлээн авах шалгуур

1. Толгойн цэсэнд «Захиалгууд» (`/orders`) холбоос зөвхөн нэвтэрсэн үед
   харагдана. Нэвтрээгүй хэрэглэгч `/orders` руу орвол нэвтрэх хуудас руу
   шилжиж, нэвтэрсний дараа буцаж ирнэ.
2. Хуудас h1 «Захиалгын түүх»-тэй. Зөвхөн нэвтэрсэн хэрэглэгчийн
   захиалгууд, **шинээс нь хуучин руу** (`createdAt`) харагдана.
3. Захиалга бүр «Захиалга #103» гэсэн гарчигтай (heading), огноо, төлөв
   (Шинэ / Хүргэлтэд / Хүргэгдсэн), бараа × тоо ширхэг, нийт үнэтэй.
4. «Төлөв» label-тэй сонголтоор (Бүгд, Шинэ, Хүргэлтэд, Хүргэгдсэн)
   шүүнэ.
5. Харуулах захиалга байхгүй бол (захиалгагүй эсвэл шүүлтэд тохирохгүй)
   «Захиалга олдсонгүй» гэсэн мэдэгдэл.
6. Захиалга бүрийн «Дахин захиалах» товч тухайн захиалгын **бүх** барааг
   тоо ширхэгтэй нь сагсанд нэмнэ (сагсанд байсан бараа дээр нэмэгдэнэ).
7. Ачаалах, алдааны төлөв; хүртээмж — label, heading, товч бүр ялгагдах нэртэй.

### Техникийн хязгаарлалт

- Шинэ файл нэмэх боломжгүй. Засах файлууд: `pages/Orders.jsx`, `App.jsx`,
  `components/Header.jsx`, `context/CartContext.jsx`, `api.js`. Бусад нь 🔒.
- Захиалгыг 7-р хичээлийн `getOrders(email)`-ээр ав. `useAuth()`,
  `useCart()` бэлэн.
- 🔒 `format.js`: `formatPrice`, `formatDate`, `ORDER_STATUS`.

### Өгөгдөл

```jsx
{
  id: 103,
  email: "bat@example.mn",
  items: [
    { productId: 2, name: "Алим", price: 2800, emoji: "🍎", quantity: 1 },
    { productId: 7, name: "Сүү", price: 3200, emoji: "🥛", quantity: 2 },
  ],
  total: 9200,
  status: "shipping", // new | shipping | delivered
  createdAt: "2026-09-20T18:15:00.000Z",
}
```

Тестүүд `api.set("orders", …)`-оор ийм хэлбэрийн захиалгуудыг бэлдэнэ.
«Хөтөч» дээр шалгахын тулд эхлээд тооцоогоор хэдэн захиалга хий.

### Эхлэхийн өмнө бодох асуултууд

- Шүүлтийн утга хаана амьдрах вэ — component-ийн state үү, URL уу?
- Шүүх, эрэмбэлэхийг хаана тооцох вэ? Үр дүнг state-д хадгалах хэрэгтэй юу?
- «Дахин захиалах»: `add`-ийг олон удаа дуудах уу, эсвэл reducer-ийг
  тоо ширхэг хүлээн авдаг болгох уу? Аль нь ойлгомжтой вэ?
- Олон «Дахин захиалах» товчийг дэлгэц уншигч хэрхэн ялгах вэ?

```quiz
Шүүж, эрэмбэлсэн захиалгын жагсаалтыг хаана хадгалах нь зөв бэ?
- [ ] Тусдаа `useState`-д, `useEffect`-ээр шинэчилнэ
- [x] Хаана ч хадгалахгүй — render бүрт `orders` ба төлвөөс тооцоолно
- [ ] `localStorage`-д
> Уламжлагдсан өгөгдлийг state-д хуулбал эх өгөгдөлтэйгээ зөрөх эрсдэлтэй.
```

```quiz
TanStack Query-ийн `data` массив дээр шууд `orders.sort(...)` дуудвал юу болох вэ?
- [ ] Асуудалгүй
- [x] Кэш дэх массивыг өөрчилж, ижил өгөгдлийг хэрэглэдэг бусад component-д нөлөөлнө
- [ ] Алдаа шиднэ
> `sort` анхны массивыг өөрчилдөг. `[...orders].sort(...)` эсвэл `orders.toSorted(...)` ашигла.
```

### Дүгнэлт

Баяр хүргэе — «Ногоон сагс» бүрэн ажиллаж байна: каталог, хайлт, сагс,
тооцоо, нэвтрэлт, админ, захиалгын түүх. Жинхэнэ төсөл болгохын тулд
дараагийн алхмууд: Vite төслөө `npm run build`-ээр бүтээж Vercel, Netlify,
Cloudflare Pages-д байршуулах; жинхэнэ сервер ба нэвтрэлт холбох;
TypeScript нэмэх; Модул 13-ын адил Vitest-ээр тест бичих. Хамгийн чухал нь
— өөрийн санаагаар дараагийн апп-аа эхлүүл.
""",
            initial_code=project(
                [
                    ("pages/Orders.jsx", ORDERS_START),
                    ("App.jsx", APP_8),
                    ("components/Header.jsx", HEADER_8),
                    ("context/CartContext.jsx", CART_CONTEXT_5),
                    ("api.js", API_8),
                ],
                [
                    ("context/AuthContext.jsx", AUTH_CONTEXT_7),
                    ("format.js", FORMAT_JS),
                    ("components/Layout.jsx", LAYOUT),
                    ("components/ProtectedRoute.jsx", PROTECTED_8),
                    ("components/ProductCard.jsx", PRODUCT_CARD_5),
                    ("pages/Home.jsx", HOME),
                    ("pages/Products.jsx", PRODUCTS_4),
                    ("pages/ProductDetail.jsx", DETAIL_5),
                    ("pages/Cart.jsx", CART_5),
                    ("pages/Checkout.jsx", CHECKOUT_6),
                    ("pages/OrderSuccess.jsx", ORDER_SUCCESS_6),
                    ("pages/Login.jsx", LOGIN_7),
                    ("pages/Profile.jsx", PROFILE_7),
                    ("pages/Admin.jsx", ADMIN_8),
                    ("pages/NotFound.jsx", NOT_FOUND),
                ],
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐⭐⭐ · 45 минут

«Заавар»-ын хүлээн авах шалгуурын дагуу захиалгын түүхийн хуудсыг бие
дааж бүтээ. Доорх тестүүд бол шалгуурын жагсаалт — бүгд давбал «Ногоон
сагс» дуусна.
""",
                tests=(
                    test(
                        "«Захиалгууд» цэс нэвтэрсэн үед л харагдаж, /orders нь нэвтрэхийг шаардана",
                        ORDERS_LOG_IN_JS
                        + """
expect(within(screen.getByRole("banner")).queryByRole("link", { name: "Захиалгууд" })).toBeNull();
await logIn("bat@example.mn");
expect(await screen.findByRole("heading", { level: 1, name: /Захиалгын түүх/ })).toBeInTheDocument();
const link = within(screen.getByRole("banner")).getByRole("link", { name: "Захиалгууд" });
expect(link).toHaveAttribute("href", "/orders");
""",
                    ),
                    test(
                        "Зөвхөн өөрийн захиалгуудыг шинээс нь хуучин руу, бараа, төлөв, нийт үнэтэй харуулна",
                        ORDERS_LOG_IN_JS
                        + """
await logIn("bat@example.mn");
await screen.findByRole("heading", { name: /#104/ });
const numbers = screen
  .getAllByRole("heading")
  .map((heading) => heading.textContent.match(/#([0-9]+)/))
  .filter(Boolean)
  .map((match) => match[1]);
expect(numbers).toEqual(["104", "103", "101"]);
const text = screen.text();
expect(text).toContain("Хүргэлтэд");
expect(text).toContain("Сүү");
expect(text).toMatch(/9,200 ?₮/);
""",
                    ),
                    test(
                        "«Төлөв» сонголтоор шүүж, тохирох захиалга байхгүй бол «Захиалга олдсонгүй» гэнэ",
                        ORDERS_LOG_IN_JS
                        + """
await logIn("bat@example.mn");
await screen.findByRole("heading", { name: /#104/ });
await user.selectOptions(screen.getByLabelText("Төлөв"), "Хүргэгдсэн");
await waitFor(() => expect(screen.queryByRole("heading", { name: /#103/ })).toBeNull());
expect(screen.getByRole("heading", { name: /#101/ })).toBeInTheDocument();
expect(screen.getByRole("heading", { name: /#104/ })).toBeInTheDocument();
await user.selectOptions(screen.getByLabelText("Төлөв"), "Шинэ");
expect(await screen.findByText(/Захиалга олдсонгүй/)).toBeInTheDocument();
""",
                    ),
                    test(
                        "«Дахин захиалах» нь тухайн захиалгын барааг тоо ширхэгтэй нь сагсанд нэмнэ",
                        ORDERS_LOG_IN_JS
                        + CART_LINK_JS
                        + """
await logIn("bat@example.mn");
let card = await screen.findByRole("heading", { name: /#103/ });
while (card && within(card).queryAllByRole("button", { name: /Дахин захиалах/ }).length === 0) {
  card = card.parentElement;
}
expect(card).toBeTruthy();
await user.click(within(card).getByRole("button", { name: /Дахин захиалах/ }));
await waitFor(() => expect(cartLink()).toHaveTextContent("3"));
await user.click(cartLink());
await screen.findByRole("heading", { level: 1, name: "Сагс" });
expect(screen.text()).toContain("Сүү");
expect(screen.text()).toMatch(/Нийт:? ?9,200 ?₮/);
""",
                    ),
                    test(
                        "Захиалга хийгээгүй хэрэглэгчид «Захиалга олдсонгүй» гэж харуулна",
                        ORDERS_LOG_IN_JS
                        + """
await logIn("shine@example.mn");
await screen.findByRole("heading", { level: 1, name: /Захиалгын түүх/ });
expect(await screen.findByText(/Захиалга олдсонгүй/)).toBeInTheDocument();
expect(screen.queryByRole("heading", { name: /#10/ })).toBeNull();
""",
                    ),
                ),
                tips="""\
- Эхлээд шалгуур бүрийг жижиг алхам болгон жагсаа: route → цэс → татах →
  харуулах → шүүх → дахин захиалах. Нэг алхам дуусах бүрт «Ажиллуулах» дар.
- Хамгаалалт, `getOrders`, `ORDER_STATUS` бүгд бэлэн — 4, 7-р хичээлийн
  `Products` (URL-ийн шүүлтүүр), `Profile` (захиалга татах)-ийг жишээ
  болгон харж болно.
- Эрэмбэлэхээс өмнө массивыг хуул — кэш дэх өгөгдлийг бүү өөрчил.
- «Дахин захиалах» товч олон байгаа тул нэр бүрийг ялгаатай болго
  (`aria-label`-д захиалгын дугаар).
- Захиалгын барааны `productId`-г сагсны мөрийн `id` болгохоо бүү март.
""",
                solution=files(
                    ("pages/Orders.jsx", ORDERS_9),
                    ("App.jsx", APP_9),
                    ("components/Header.jsx", HEADER_9),
                    ("context/CartContext.jsx", CART_CONTEXT_9),
                ),
            ),
        ),
    ],
)
