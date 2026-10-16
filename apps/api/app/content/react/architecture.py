"""Модул 7 — State-ийн архитектур.

State-ийг хаана байрлуулахаа шийдэх: дээш өргөх, нэг үнэн эх сурвалж,
prop drilling ба composition, Context, provider component, `useReducer`,
reducer + Context. Төгсгөлд нь theme ба хэрэглэгчийн тохиргооны апп бүтээнэ.
"""

from app.content.react.common import solution, test, vite
from app.content.types import ExerciseSpec, LessonSpec, ModuleSpec
from app.models.enums import LessonLanguage

JSX = LessonLanguage.JSX

# Модулийн хичээлүүдэд нийтлэг, түгжигдсэн энгийн загвар.
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
"""

# --- 1. State-ийг дээш өргөх ---------------------------------------------------

FAQ_CSS = (
    BASE_CSS
    + """
.panel {
  max-width: 520px;
  margin: 8px 0;
  border: 1px solid #d0d7de;
  border-radius: 10px;
  background: #fff;
}

.panel h2 {
  margin: 0;
  font-size: 1rem;
}

.panel button {
  width: 100%;
  padding: 12px 14px;
  border: 0;
  background: none;
  font-weight: 600;
  text-align: left;
}

.panel p {
  margin: 0;
  padding: 0 14px 12px;
  color: #55624f;
}
"""
)

FAQ_APP_START = """\
import Panel from "./Panel";

const faqs = [
  { title: "Хүргэлт", answer: "Улаанбаатар хотод захиалгыг 24 цагийн дотор хүргэнэ." },
  { title: "Төлбөр", answer: "QPay, банкны карт эсвэл бэлнээр төлж болно." },
  { title: "Буцаалт", answer: "Гэмтэлтэй барааг 3 хоногийн дотор сольж өгнө." },
];

export default function App() {
  // TODO 1: Аль панель нээлттэйг индексээр нь хадгалах state (эхэндээ 0)

  return (
    <main>
      <h1>❓ Түгээмэл асуулт</h1>
      {faqs.map((faq) => (
        // TODO 2: Panel-д isOpen, onToggle-ийг дамжуул
        <Panel key={faq.title} title={faq.title}>
          {faq.answer}
        </Panel>
      ))}
      {/* TODO 3: <p>Нээлттэй: Хүргэлт</p> — бүгд хаалттай бол «Нээлттэй: —» */}
    </main>
  );
}
"""

FAQ_PANEL_START = """\
import { useState } from "react";

// TODO: Өөрийн state-ийг хасаад isOpen, onToggle-ийг props-оос ав.
export default function Panel({ title, children }) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <section className="panel">
      <h2>
        <button onClick={() => setIsOpen(!isOpen)} aria-expanded={isOpen}>
          <span aria-hidden="true">{isOpen ? "▾" : "▸"}</span> {title}
        </button>
      </h2>
      {isOpen && <p>{children}</p>}
    </section>
  );
}
"""

# --- 2. Нэг үнэн эх сурвалж ------------------------------------------------------

CART_ROWS_CSS = (
    BASE_CSS
    + """
.rows {
  max-width: 420px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 6px 0;
  padding: 8px 12px;
  border: 1px solid #dfe6da;
  border-radius: 10px;
  background: #fff;
}

.row.selected {
  border-color: #15803d;
  box-shadow: 0 0 0 1px #15803d;
}

.row .name {
  flex: 1;
  border: 0;
  background: none;
  text-align: left;
  font-weight: 600;
}

.row .qty {
  min-width: 24px;
  text-align: center;
}

.details {
  max-width: 420px;
  margin-top: 16px;
  padding: 12px 16px;
  border-radius: 12px;
  background: #e8f3e3;
}

.details h2 {
  margin: 0 0 4px;
  font-size: 1.1rem;
}

.details p {
  margin: 4px 0;
}
"""
)

CART_ROWS_APP_START = """\
import { useState } from "react";

const initialItems = [
  { id: 1, name: "Алим", emoji: "🍎", price: 2800, qty: 1 },
  { id: 2, name: "Сүү", emoji: "🥛", price: 3200, qty: 2 },
  { id: 3, name: "Талх", emoji: "🍞", price: 2500, qty: 1 },
];

export default function App() {
  const [items, setItems] = useState(initialItems);
  // ❌ Сонгосон барааны ХУУЛБАР — items өөрчлөгдөхөд хуучирна
  const [selected, setSelected] = useState(initialItems[0]);
  // ❌ items-ээс тооцож болох утгыг тусад нь хадгалж байна
  const [totalQty, setTotalQty] = useState(4);

  function changeQty(id, delta) {
    setItems(
      items.map((item) =>
        item.id === id ? { ...item, qty: Math.max(0, item.qty + delta) } : item,
      ),
    );
    setTotalQty(totalQty + delta);
  }

  return (
    <main>
      <h1>🛒 Сагс</h1>
      <ul className="rows">
        {items.map((item) => (
          <li key={item.id} className={item.id === selected.id ? "row selected" : "row"}>
            <span>{item.emoji}</span>
            <button className="name" onClick={() => setSelected(item)}>
              {item.name}
            </button>
            <button aria-label={`${item.name} хасах`} onClick={() => changeQty(item.id, -1)}>
              −
            </button>
            <span className="qty">{item.qty}</span>
            <button aria-label={`${item.name} нэмэх`} onClick={() => changeQty(item.id, 1)}>
              +
            </button>
          </li>
        ))}
      </ul>
      <section className="details">
        <h2>Сонгосон: {selected.name}</h2>
        <p>Тоо: {selected.qty}</p>
        <p>Дүн: {selected.price * selected.qty}₮</p>
      </section>
      <p>Нийт ширхэг: {totalQty}</p>
    </main>
  );
}
"""

CART_ROWS_APP_SOLUTION = """\
import { useState } from "react";

const initialItems = [
  { id: 1, name: "Алим", emoji: "🍎", price: 2800, qty: 1 },
  { id: 2, name: "Сүү", emoji: "🥛", price: 3200, qty: 2 },
  { id: 3, name: "Талх", emoji: "🍞", price: 2500, qty: 1 },
];

export default function App() {
  const [items, setItems] = useState(initialItems);
  const [selectedId, setSelectedId] = useState(initialItems[0].id);

  // Хадгалахгүй — render бүрт items-ээс тооцно
  const selected = items.find((item) => item.id === selectedId);
  const totalQty = items.reduce((sum, item) => sum + item.qty, 0);

  function changeQty(id, delta) {
    setItems(
      items.map((item) =>
        item.id === id ? { ...item, qty: Math.max(0, item.qty + delta) } : item,
      ),
    );
  }

  return (
    <main>
      <h1>🛒 Сагс</h1>
      <ul className="rows">
        {items.map((item) => (
          <li key={item.id} className={item.id === selectedId ? "row selected" : "row"}>
            <span>{item.emoji}</span>
            <button className="name" onClick={() => setSelectedId(item.id)}>
              {item.name}
            </button>
            <button aria-label={`${item.name} хасах`} onClick={() => changeQty(item.id, -1)}>
              −
            </button>
            <span className="qty">{item.qty}</span>
            <button aria-label={`${item.name} нэмэх`} onClick={() => changeQty(item.id, 1)}>
              +
            </button>
          </li>
        ))}
      </ul>
      <section className="details">
        <h2>Сонгосон: {selected.name}</h2>
        <p>Тоо: {selected.qty}</p>
        <p>Дүн: {selected.price * selected.qty}₮</p>
      </section>
      <p>Нийт ширхэг: {totalQty}</p>
    </main>
  );
}
"""

# --- 3. Prop drilling --------------------------------------------------------------

DASHBOARD_CSS = (
    BASE_CSS
    + """
body {
  padding: 0;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 24px;
  background: #1f2a1c;
  color: #fff;
}

.badge {
  padding: 4px 10px;
  border-radius: 999px;
  background: #3f5a36;
}

main {
  padding: 24px;
}

.card {
  max-width: 360px;
  padding: 16px;
  border: 1px solid #dfe6da;
  border-radius: 12px;
  background: #fff;
}

.card h2 {
  margin: 0 0 8px;
  font-size: 1.1rem;
}

.card button {
  padding: 8px 16px;
  border: 0;
  border-radius: 8px;
  background: #15803d;
  color: #fff;
}
"""
)

DASHBOARD_APP_START = """\
import { useState } from "react";
import Layout from "./Layout";

export default function App() {
  const [user, setUser] = useState({ name: "Сараа", avatar: "👩‍🎓", plan: "Үнэгүй" });

  function upgrade() {
    setUser({ ...user, plan: "Standard" });
  }

  // TODO: Layout-д header ба children өгч, UserBadge, PlanCard-ийг энд шууд render хий.
  return <Layout user={user} onUpgrade={upgrade} />;
}
"""

DASHBOARD_LAYOUT_START = """\
import Header from "./Header";
import PlanCard from "./PlanCard";

// Layout нь user, onUpgrade-ийг огт ашигладаггүй — зөвхөн доош дамжуулж байна.
// TODO: { header, children } авч, header-ийг дээр, children-ийг <main> дотор харуул.
export default function Layout({ user, onUpgrade }) {
  return (
    <div className="layout">
      <Header user={user} />
      <main>
        <h1>Хяналтын самбар</h1>
        <PlanCard user={user} onUpgrade={onUpgrade} />
      </main>
    </div>
  );
}
"""

DASHBOARD_HEADER_START = """\
import UserBadge from "./UserBadge";

// Header ч user-ийг ашигладаггүй — зөвхөн UserBadge руу дамжуулна.
// TODO: { children } авч, лого-ийн хажууд харуул.
export default function Header({ user }) {
  return (
    <header className="header">
      <strong>🎓 MedlegHub</strong>
      <UserBadge user={user} />
    </header>
  );
}
"""

DASHBOARD_USER_BADGE = """\
export default function UserBadge({ user }) {
  return (
    <span className="badge">
      {user.avatar} {user.name} · {user.plan}
    </span>
  );
}
"""

DASHBOARD_PLAN_CARD = """\
export default function PlanCard({ user, onUpgrade }) {
  return (
    <section className="card">
      <h2>Таны багц: {user.plan}</h2>
      {user.plan === "Standard" ? (
        <p>Бүх хичээл нээлттэй 🎉</p>
      ) : (
        <button onClick={onUpgrade}>Standard авах</button>
      )}
    </section>
  );
}
"""

# --- 4. Context ба useContext ------------------------------------------------------

SHOP_CSS = (
    BASE_CSS
    + """
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 12px;
  max-width: 560px;
  margin: 16px 0 0;
  padding: 0;
  list-style: none;
}

.card {
  padding: 14px;
  border: 1px solid #dfe6da;
  border-radius: 12px;
  background: #fff;
  text-align: center;
}

.card .emoji {
  font-size: 32px;
}

.card h2 {
  margin: 6px 0 2px;
  font-size: 1rem;
}

.card p {
  margin: 0 0 8px;
  color: #55624f;
}

.cart-button,
.lang {
  padding: 6px 12px;
  border: 0;
  border-radius: 8px;
  background: #15803d;
  color: #fff;
}

.lang {
  float: right;
  background: #1f2a1c;
}
"""
)

LANGUAGE_TRANSLATIONS = """\
export const translations = {
  mn: {
    greeting: "Сайн байна уу! Өнөөдөр юу авах вэ?",
    addToCart: "Сагсанд нэмэх",
    switchLanguage: "English",
  },
  en: {
    greeting: "Hello! What would you like today?",
    addToCart: "Add to cart",
    switchLanguage: "Монгол",
  },
};
"""

LANGUAGE_PAGE = """\
import CartButton from "./CartButton";
import Greeting from "./Greeting";

// Page ба ProductCard хэлний тухай юу ч мэдэхгүй — props-оор юу ч дамжуулахгүй.
function ProductCard({ emoji, name, price }) {
  return (
    <li className="card">
      <span className="emoji">{emoji}</span>
      <h2>{name}</h2>
      <p>{price}₮</p>
      <CartButton />
    </li>
  );
}

export default function Page() {
  return (
    <div>
      <Greeting />
      <ul className="grid">
        <ProductCard emoji="🍎" name="Алим" price={2800} />
        <ProductCard emoji="🥛" name="Сүү" price={3200} />
      </ul>
    </div>
  );
}
"""

LANGUAGE_APP_START = """\
import { useState } from "react";
import Page from "./Page";
import { translations } from "./translations";

export default function App() {
  const [language, setLanguage] = useState("mn");

  function toggleLanguage() {
    setLanguage(language === "mn" ? "en" : "mn");
  }

  // TODO: Page-ийг LanguageContext-оор ороож, language-ийг value болгож өг.
  return (
    <main>
      <button className="lang" onClick={toggleLanguage}>
        🌐 {translations[language].switchLanguage}
      </button>
      <Page />
    </main>
  );
}
"""

LANGUAGE_CONTEXT_START = """\
// TODO: react-ийн createContext-оор LanguageContext үүсгэж, нэртэй export хий.
// Анхдагч утга нь "mn".
export const LanguageContext = null;
"""

LANGUAGE_GREETING_START = """\
import { translations } from "./translations";

export default function Greeting() {
  // TODO: хэлийг LanguageContext-оос унш
  const language = "mn";
  return <h1>{translations[language].greeting}</h1>;
}
"""

LANGUAGE_BUTTON_START = """\
import { translations } from "./translations";

export default function CartButton() {
  // TODO: хэлийг LanguageContext-оос унш
  const language = "mn";
  return <button className="cart-button">{translations[language].addToCart}</button>;
}
"""

# --- 5. Context + state: provider component ------------------------------------

AUTH_CSS = (
    BASE_CSS
    + """
body {
  padding: 0;
}

.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 24px;
  background: #1f2a1c;
  color: #fff;
}

.navbar button {
  margin-left: 8px;
  padding: 4px 10px;
  border: 0;
  border-radius: 6px;
}

main {
  padding: 24px;
}

.card {
  max-width: 360px;
  padding: 16px;
  border: 1px solid #dfe6da;
  border-radius: 12px;
  background: #fff;
}

.card h2 {
  margin: 0 0 8px;
  font-size: 1.1rem;
}

.card label {
  display: block;
  margin-bottom: 8px;
}

.card input {
  margin-left: 8px;
  padding: 6px 8px;
}

.card button {
  padding: 8px 16px;
  border: 0;
  border-radius: 8px;
  background: #15803d;
  color: #fff;
}
"""
)

AUTH_CONTEXT_START = """\
import { createContext, useContext, useState } from "react";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  // TODO 1: user state (эхэндээ null)
  // TODO 2: login(name) → user = { name }, logout() → user = null
  // TODO 3: { user, login, logout }-ийг AuthContext-оор children-д хүргэ
  return children;
}

export function useAuth() {
  // TODO 4: AuthContext-ийг уншиж буцаа. Provider-гүй (null) бол алдаа шид.
  return { user: null, login() {}, logout() {} };
}
"""

AUTH_CONTEXT_SOLUTION = """\
import { createContext, useContext, useState } from "react";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);

  function login(name) {
    setUser({ name });
  }

  function logout() {
    setUser(null);
  }

  return <AuthContext value={{ user, login, logout }}>{children}</AuthContext>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === null) {
    throw new Error("useAuth-ийг AuthProvider дотор ашиглана уу");
  }
  return context;
}
"""

AUTH_APP_START = """\
import Dashboard from "./Dashboard";
import Navbar from "./Navbar";

// TODO: Бүх апп-ыг AuthProvider-оор ороо.
export default function App() {
  return (
    <>
      <Navbar />
      <main>
        <Dashboard />
      </main>
    </>
  );
}
"""

AUTH_NAVBAR = """\
import { useAuth } from "./AuthContext";

export default function Navbar() {
  const { user, logout } = useAuth();

  return (
    <header className="navbar">
      <strong>🥬 Ногоон сагс</strong>
      {user ? (
        <span>
          👤 {user.name}
          <button onClick={logout}>Гарах</button>
        </span>
      ) : (
        <span>Зочин</span>
      )}
    </header>
  );
}
"""

AUTH_DASHBOARD = """\
import { useState } from "react";
import { useAuth } from "./AuthContext";

function LoginForm() {
  const { login } = useAuth();
  const [name, setName] = useState("");

  function handleSubmit(event) {
    event.preventDefault();
    if (name.trim()) login(name.trim());
  }

  return (
    <form onSubmit={handleSubmit} className="card">
      <h2>Нэвтрэх</h2>
      <label>
        Нэр
        <input value={name} onChange={(event) => setName(event.target.value)} />
      </label>
      <button>Нэвтрэх</button>
    </form>
  );
}

export default function Dashboard() {
  const { user } = useAuth();

  if (!user) return <LoginForm />;

  return (
    <section className="card">
      <h2>Тавтай морил, {user.name}!</h2>
      <p>Таны захиалгууд энд харагдана.</p>
    </section>
  );
}
"""

# --- 6. useReducer --------------------------------------------------------------------

TASKS_CSS = (
    BASE_CSS
    + """
main {
  max-width: 440px;
}

form {
  display: flex;
  gap: 8px;
  align-items: end;
}

form label {
  flex: 1;
  font-weight: 600;
}

form input {
  display: block;
  box-sizing: border-box;
  width: 100%;
  margin-top: 4px;
  padding: 8px 10px;
  border: 1px solid #c4c9d0;
  border-radius: 8px;
  font: inherit;
}

.tasks {
  margin: 16px 0;
  padding: 0;
  list-style: none;
}

.tasks li {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 6px 0;
  padding: 8px 12px;
  border: 1px solid #dfe6da;
  border-radius: 10px;
  background: #fff;
}

.tasks .done {
  color: #8a9486;
  text-decoration: line-through;
}

.tasks li button {
  border: 0;
  background: none;
}

.primary {
  padding: 8px 16px;
  border: 0;
  border-radius: 8px;
  background: #15803d;
  color: #fff;
}
"""
)

TASKS_REDUCER_START = """\
export const initialTasks = [
  { id: 1, text: "React хичээл үзэх", done: true },
  { id: 2, text: "Дасгал хийх", done: false },
  { id: 3, text: "Тест бичих", done: false },
];

// (tasks, action) => шинэ tasks. Анхны массивыг ӨӨРЧЛӨХГҮЙ.
export function tasksReducer(tasks, action) {
  switch (action.type) {
    // TODO 1: "added"   → { id: action.id, text: action.text, done: false }-г төгсгөлд нь нэм
    // TODO 2: "toggled" → action.id-тай даалгаврын done-ийг эсрэгээр нь соль
    // TODO 3: "deleted" → action.id-тай даалгаврыг хас
    // TODO 4: "cleared" → дууссан (done: true) даалгавруудыг бүгдийг нь хас
    default:
      throw new Error("Үл мэдэгдэх үйлдэл: " + action.type);
  }
}
"""

TASKS_REDUCER_SOLUTION = """\
export const initialTasks = [
  { id: 1, text: "React хичээл үзэх", done: true },
  { id: 2, text: "Дасгал хийх", done: false },
  { id: 3, text: "Тест бичих", done: false },
];

export function tasksReducer(tasks, action) {
  switch (action.type) {
    case "added":
      return [...tasks, { id: action.id, text: action.text, done: false }];
    case "toggled":
      return tasks.map((task) =>
        task.id === action.id ? { ...task, done: !task.done } : task,
      );
    case "deleted":
      return tasks.filter((task) => task.id !== action.id);
    case "cleared":
      return tasks.filter((task) => !task.done);
    default:
      throw new Error("Үл мэдэгдэх үйлдэл: " + action.type);
  }
}
"""

TASKS_APP_START = """\
import { useReducer, useState } from "react";
import { initialTasks, tasksReducer } from "./reducer";

let nextId = 4;

export default function App() {
  const [tasks, dispatch] = useReducer(tasksReducer, initialTasks);
  const [text, setText] = useState("");

  function handleSubmit(event) {
    event.preventDefault();
    if (!text.trim()) return;
    dispatch({ type: "added", id: nextId++, text: text.trim() });
    setText("");
  }

  const left = tasks.filter((task) => !task.done).length;

  return (
    <main>
      <h1>📝 Даалгаврууд</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Шинэ даалгавар
          <input value={text} onChange={(event) => setText(event.target.value)} />
        </label>
        <button className="primary">Нэмэх</button>
      </form>
      <ul className="tasks">
        {tasks.map((task) => (
          <li key={task.id}>
            <label>
              <input
                type="checkbox"
                checked={task.done}
                onChange={() => dispatch({ type: "toggled", id: task.id })}
              />
              <span className={task.done ? "done" : ""}>{task.text}</span>
            </label>
            <button
              aria-label={`${task.text} устгах`}
              onClick={() => dispatch({ type: "deleted", id: task.id })}
            >
              🗑️
            </button>
          </li>
        ))}
      </ul>
      <p>Үлдсэн: {left}</p>
      {/* TODO: «Дууссаныг цэвэрлэх» товч — { type: "cleared" } илгээнэ */}
    </main>
  );
}
"""

TASKS_APP_SOLUTION = """\
import { useReducer, useState } from "react";
import { initialTasks, tasksReducer } from "./reducer";

let nextId = 4;

export default function App() {
  const [tasks, dispatch] = useReducer(tasksReducer, initialTasks);
  const [text, setText] = useState("");

  function handleSubmit(event) {
    event.preventDefault();
    if (!text.trim()) return;
    dispatch({ type: "added", id: nextId++, text: text.trim() });
    setText("");
  }

  const left = tasks.filter((task) => !task.done).length;

  return (
    <main>
      <h1>📝 Даалгаврууд</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Шинэ даалгавар
          <input value={text} onChange={(event) => setText(event.target.value)} />
        </label>
        <button className="primary">Нэмэх</button>
      </form>
      <ul className="tasks">
        {tasks.map((task) => (
          <li key={task.id}>
            <label>
              <input
                type="checkbox"
                checked={task.done}
                onChange={() => dispatch({ type: "toggled", id: task.id })}
              />
              <span className={task.done ? "done" : ""}>{task.text}</span>
            </label>
            <button
              aria-label={`${task.text} устгах`}
              onClick={() => dispatch({ type: "deleted", id: task.id })}
            >
              🗑️
            </button>
          </li>
        ))}
      </ul>
      <p>Үлдсэн: {left}</p>
      <button className="primary" onClick={() => dispatch({ type: "cleared" })}>
        Дууссаныг цэвэрлэх
      </button>
    </main>
  );
}
"""

# --- 7. Reducer + Context ---------------------------------------------------------

CART_CSS = (
    SHOP_CSS
    + """
body {
  padding: 0;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 24px;
  background: #1f2a1c;
  color: #fff;
}

.cart-badge {
  padding: 4px 10px;
  border-radius: 999px;
  background: #3f5a36;
}

.shop {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
  padding: 24px;
}

.shop .grid {
  flex: 1;
  margin: 0;
}

.cart {
  width: 240px;
  padding: 16px;
  border-radius: 12px;
  background: #e8f3e3;
}

.cart h2 {
  margin: 0 0 8px;
  font-size: 1.1rem;
}

.cart ul {
  margin: 0;
  padding: 0;
  list-style: none;
}

.cart li {
  display: flex;
  justify-content: space-between;
  margin: 4px 0;
}

.cart li button {
  border: 0;
  background: none;
}

.total {
  font-weight: 700;
}
"""
)

CART_PRODUCTS = """\
export const products = [
  { id: 1, name: "Алим", emoji: "🍎", price: 2800 },
  { id: 2, name: "Сүү", emoji: "🥛", price: 3200 },
  { id: 3, name: "Талх", emoji: "🍞", price: 2500 },
];
"""

CART_CONTEXT_START = """\
import { createContext, useContext, useReducer } from "react";

const CartContext = createContext(null);
const CartDispatchContext = createContext(null);

// (items, action) => шинэ items. Анхны массив, объектыг ӨӨРЧЛӨХГҮЙ.
export function cartReducer(items, action) {
  switch (action.type) {
    // TODO 1: "added" → action.product сагсанд байвал qty-г нь 1-ээр нэм,
    //         байхгүй бол { ...action.product, qty: 1 }-ийг төгсгөлд нь нэм
    // TODO 2: "removed" → action.id-тай барааг хас
    default:
      throw new Error("Үл мэдэгдэх үйлдэл: " + action.type);
  }
}

export function CartProvider({ children }) {
  // TODO 3: useReducer(cartReducer, []). items-ийг CartContext-оор,
  //         dispatch-ийг CartDispatchContext-оор children-д хүргэ.
  return children;
}

export function useCart() {
  // TODO 4: CartContext-ийг уншиж буцаа
  return [];
}

export function useCartDispatch() {
  // TODO 5: CartDispatchContext-ийг уншиж буцаа
  return () => {};
}
"""

CART_CONTEXT_SOLUTION = """\
import { createContext, useContext, useReducer } from "react";

const CartContext = createContext(null);
const CartDispatchContext = createContext(null);

export function cartReducer(items, action) {
  switch (action.type) {
    case "added": {
      const exists = items.some((item) => item.id === action.product.id);
      if (exists) {
        return items.map((item) =>
          item.id === action.product.id ? { ...item, qty: item.qty + 1 } : item,
        );
      }
      return [...items, { ...action.product, qty: 1 }];
    }
    case "removed":
      return items.filter((item) => item.id !== action.id);
    default:
      throw new Error("Үл мэдэгдэх үйлдэл: " + action.type);
  }
}

export function CartProvider({ children }) {
  const [items, dispatch] = useReducer(cartReducer, []);

  return (
    <CartContext value={items}>
      <CartDispatchContext value={dispatch}>{children}</CartDispatchContext>
    </CartContext>
  );
}

export function useCart() {
  const items = useContext(CartContext);
  if (items === null) {
    throw new Error("useCart-ийг CartProvider дотор ашиглана уу");
  }
  return items;
}

export function useCartDispatch() {
  const dispatch = useContext(CartDispatchContext);
  if (dispatch === null) {
    throw new Error("useCartDispatch-ийг CartProvider дотор ашиглана уу");
  }
  return dispatch;
}
"""

CART_APP_START = """\
import Cart from "./Cart";
import CartBadge from "./CartBadge";
import ProductCard from "./ProductCard";
import { products } from "./products";

// TODO: Бүх апп-ыг CartProvider-оор ороо.
export default function App() {
  return (
    <>
      <header className="header">
        <strong>🥬 Ногоон сагс</strong>
        <CartBadge />
      </header>
      <main className="shop">
        <ul className="grid">
          {products.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </ul>
        <Cart />
      </main>
    </>
  );
}
"""

CART_APP_SOLUTION = """\
import Cart from "./Cart";
import CartBadge from "./CartBadge";
import { CartProvider } from "./CartContext";
import ProductCard from "./ProductCard";
import { products } from "./products";

export default function App() {
  return (
    <CartProvider>
      <header className="header">
        <strong>🥬 Ногоон сагс</strong>
        <CartBadge />
      </header>
      <main className="shop">
        <ul className="grid">
          {products.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </ul>
        <Cart />
      </main>
    </CartProvider>
  );
}
"""

CART_PRODUCT_CARD_START = """\
export default function ProductCard({ product }) {
  // TODO: useCartDispatch()-аар { type: "added", product } илгээ
  return (
    <li className="card">
      <span className="emoji">{product.emoji}</span>
      <h2>{product.name}</h2>
      <p>{product.price}₮</p>
      <button className="cart-button" aria-label={`Сагсанд нэмэх: ${product.name}`}>
        Сагсанд нэмэх
      </button>
    </li>
  );
}
"""

CART_PRODUCT_CARD_SOLUTION = """\
import { useCartDispatch } from "./CartContext";

export default function ProductCard({ product }) {
  const dispatch = useCartDispatch();

  return (
    <li className="card">
      <span className="emoji">{product.emoji}</span>
      <h2>{product.name}</h2>
      <p>{product.price}₮</p>
      <button
        className="cart-button"
        aria-label={`Сагсанд нэмэх: ${product.name}`}
        onClick={() => dispatch({ type: "added", product })}
      >
        Сагсанд нэмэх
      </button>
    </li>
  );
}
"""

CART_BADGE_START = """\
export default function CartBadge() {
  // TODO: useCart()-аас бараануудыг авч нийт ширхгийг (qty-ийн нийлбэр) тооцоол
  const count = 0;
  return <span className="cart-badge">🛒 Сагс: {count}</span>;
}
"""

CART_BADGE_SOLUTION = """\
import { useCart } from "./CartContext";

export default function CartBadge() {
  const items = useCart();
  const count = items.reduce((sum, item) => sum + item.qty, 0);
  return <span className="cart-badge">🛒 Сагс: {count}</span>;
}
"""

CART_VIEW = """\
import { useCart, useCartDispatch } from "./CartContext";

export default function Cart() {
  const items = useCart();
  const dispatch = useCartDispatch();
  const total = items.reduce((sum, item) => sum + item.price * item.qty, 0);

  return (
    <aside className="cart">
      <h2>Таны сагс</h2>
      {items.length === 0 ? (
        <p>Сагс хоосон байна</p>
      ) : (
        <ul>
          {items.map((item) => (
            <li key={item.id}>
              {item.emoji} {item.name} × {item.qty}
              <button
                aria-label={`${item.name} хасах`}
                onClick={() => dispatch({ type: "removed", id: item.id })}
              >
                ✕
              </button>
            </li>
          ))}
        </ul>
      )}
      <p className="total">Нийт: {total}₮</p>
    </aside>
  );
}
"""

# --- 8. Төсөл: Theme ба хэрэглэгчийн тохиргоо ----------------------------------

SETTINGS_CSS = """\
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

.columns {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 24px;
  max-width: 760px;
}

fieldset {
  margin: 0 0 16px;
  padding: 12px 16px;
  border: 1px solid #d0d7de;
  border-radius: 12px;
  background: #fff;
}

legend {
  padding: 0 6px;
  font-weight: 700;
}

fieldset label {
  display: block;
  margin: 8px 0;
}

fieldset select,
fieldset input:not([type="checkbox"]) {
  display: block;
  box-sizing: border-box;
  width: 100%;
  margin-top: 4px;
  padding: 8px 10px;
  border: 1px solid #c4c9d0;
  border-radius: 8px;
  font: inherit;
}

fieldset button {
  padding: 8px 14px;
  border: 1px solid #b42318;
  border-radius: 8px;
  background: #fff;
  color: #b42318;
  font: inherit;
  cursor: pointer;
}

/* Урьдчилан харах: className = "preview <theme> <fontSize>" */
.preview {
  padding: 20px;
  border: 1px solid #d0d7de;
  border-radius: 16px;
  transition:
    background 0.2s,
    color 0.2s;
}

.preview.light {
  background: #fff;
  color: #1f2a1c;
}

.preview.dark {
  border-color: #374151;
  background: #111827;
  color: #f9fafb;
}

.preview.small {
  font-size: 14px;
}

.preview.medium {
  font-size: 16px;
}

.preview.large {
  font-size: 20px;
}

.preview h2 {
  margin-top: 0;
  font-size: 1.4em;
}

.preview button {
  padding: 0.5em 1em;
  border: 0;
  border-radius: 8px;
  background: #15803d;
  color: #fff;
  font: inherit;
}

.preview.dark button {
  background: #22c55e;
  color: #052e16;
}
"""

SETTINGS_APP_START = """\
import Preview from "./Preview";
import ThemeSettings from "./ThemeSettings";
import UserSettings from "./UserSettings";

// TODO: Бүгдийг SettingsProvider-оор ороо.
export default function App() {
  return (
    <main>
      <h1>⚙️ Тохиргоо</h1>
      <div className="columns">
        <div>
          <ThemeSettings />
          <UserSettings />
        </div>
        <Preview />
      </div>
    </main>
  );
}
"""

SETTINGS_APP_SOLUTION = """\
import Preview from "./Preview";
import { SettingsProvider } from "./SettingsContext";
import ThemeSettings from "./ThemeSettings";
import UserSettings from "./UserSettings";

export default function App() {
  return (
    <SettingsProvider>
      <main>
        <h1>⚙️ Тохиргоо</h1>
        <div className="columns">
          <div>
            <ThemeSettings />
            <UserSettings />
          </div>
          <Preview />
        </div>
      </main>
    </SettingsProvider>
  );
}
"""

SETTINGS_CONTEXT_START = """\
import { createContext, useContext, useEffect, useReducer } from "react";

export const initialSettings = { theme: "light", fontSize: "medium", name: "" };

const SettingsContext = createContext(null);

// (settings, action) => шинэ settings
export function settingsReducer(settings, action) {
  switch (action.type) {
    // TODO 1: "themeToggled", "fontSizeChanged", "nameChanged", "reset"
    default:
      throw new Error("Үл мэдэгдэх үйлдэл: " + action.type);
  }
}

// useReducer-ийн 3 дахь аргумент: анхны state-ийг localStorage-оос сэргээнэ.
function loadSettings(initial) {
  // TODO 5: localStorage.getItem("settings")-ийг JSON.parse хийж,
  // { ...initial, ...saved } буцаа. Хадгалсан зүйлгүй эсвэл алдаа гарвал initial.
  return initial;
}

export function SettingsProvider({ children }) {
  // TODO 2: useReducer(settingsReducer, initialSettings, loadSettings)
  // TODO 3: { settings, dispatch }-ийг SettingsContext-оор children-д хүргэ
  // TODO 5: settings өөрчлөгдөх бүрт localStorage-д хадгал (useEffect)
  return children;
}

export function useSettings() {
  // TODO 4: context-ийг буцаа. SettingsProvider-гүй бол алдаа шид.
  return { settings: initialSettings, dispatch: () => {} };
}
"""

SETTINGS_CONTEXT_SOLUTION = """\
import { createContext, useContext, useEffect, useReducer } from "react";

export const initialSettings = { theme: "light", fontSize: "medium", name: "" };

const SettingsContext = createContext(null);

export function settingsReducer(settings, action) {
  switch (action.type) {
    case "themeToggled":
      return { ...settings, theme: settings.theme === "light" ? "dark" : "light" };
    case "fontSizeChanged":
      return { ...settings, fontSize: action.fontSize };
    case "nameChanged":
      return { ...settings, name: action.name };
    case "reset":
      return initialSettings;
    default:
      throw new Error("Үл мэдэгдэх үйлдэл: " + action.type);
  }
}

function loadSettings(initial) {
  try {
    const saved = JSON.parse(localStorage.getItem("settings"));
    return saved ? { ...initial, ...saved } : initial;
  } catch {
    return initial;
  }
}

export function SettingsProvider({ children }) {
  const [settings, dispatch] = useReducer(settingsReducer, initialSettings, loadSettings);

  useEffect(() => {
    localStorage.setItem("settings", JSON.stringify(settings));
  }, [settings]);

  return <SettingsContext value={{ settings, dispatch }}>{children}</SettingsContext>;
}

export function useSettings() {
  const context = useContext(SettingsContext);
  if (context === null) {
    throw new Error("useSettings-ийг SettingsProvider дотор ашиглана уу");
  }
  return context;
}
"""

SETTINGS_THEME_START = """\
// TODO: useSettings()-ээс settings, dispatch-ийг авч, хоёр талбарыг
// удирдлагатай (controlled) болго.
export default function ThemeSettings() {
  return (
    <fieldset>
      <legend>Харагдац</legend>
      <label>
        <input type="checkbox" /> Харанхуй горим
      </label>
      <label>
        Үсгийн хэмжээ
        <select defaultValue="medium">
          <option value="small">Жижиг</option>
          <option value="medium">Дунд</option>
          <option value="large">Том</option>
        </select>
      </label>
    </fieldset>
  );
}
"""

SETTINGS_THEME_SOLUTION = """\
import { useSettings } from "./SettingsContext";

export default function ThemeSettings() {
  const { settings, dispatch } = useSettings();

  return (
    <fieldset>
      <legend>Харагдац</legend>
      <label>
        <input
          type="checkbox"
          checked={settings.theme === "dark"}
          onChange={() => dispatch({ type: "themeToggled" })}
        />{" "}
        Харанхуй горим
      </label>
      <label>
        Үсгийн хэмжээ
        <select
          value={settings.fontSize}
          onChange={(event) =>
            dispatch({ type: "fontSizeChanged", fontSize: event.target.value })
          }
        >
          <option value="small">Жижиг</option>
          <option value="medium">Дунд</option>
          <option value="large">Том</option>
        </select>
      </label>
    </fieldset>
  );
}
"""

SETTINGS_USER_START = """\
// TODO: useSettings()-ээс settings, dispatch-ийг авч, нэрийг удирдлагатай
// болго. «Анхны тохиргоо» товч бүх тохиргоог буцаана.
export default function UserSettings() {
  return (
    <fieldset>
      <legend>Хэрэглэгч</legend>
      <label>
        Нэр
        <input placeholder="Таны нэр" />
      </label>
      <button type="button">Анхны тохиргоо</button>
    </fieldset>
  );
}
"""

SETTINGS_USER_SOLUTION = """\
import { useSettings } from "./SettingsContext";

export default function UserSettings() {
  const { settings, dispatch } = useSettings();

  return (
    <fieldset>
      <legend>Хэрэглэгч</legend>
      <label>
        Нэр
        <input
          placeholder="Таны нэр"
          value={settings.name}
          onChange={(event) => dispatch({ type: "nameChanged", name: event.target.value })}
        />
      </label>
      <button type="button" onClick={() => dispatch({ type: "reset" })}>
        Анхны тохиргоо
      </button>
    </fieldset>
  );
}
"""

SETTINGS_PREVIEW_START = """\
// TODO: useSettings()-ээс тохиргоог уншиж, текст болон className-ийг түүнээс гарга.
export default function Preview() {
  return (
    <section aria-label="Урьдчилан харах" className="preview light medium">
      <h2>Сайн уу, Зочин!</h2>
      <p>Горим: Цайвар</p>
      <p>Үсэг: Дунд</p>
      <button type="button">Жишээ товч</button>
    </section>
  );
}
"""

SETTINGS_PREVIEW_SOLUTION = """\
import { useSettings } from "./SettingsContext";

const sizeLabels = { small: "Жижиг", medium: "Дунд", large: "Том" };

export default function Preview() {
  const { settings } = useSettings();
  const name = settings.name.trim() || "Зочин";

  return (
    <section
      aria-label="Урьдчилан харах"
      className={`preview ${settings.theme} ${settings.fontSize}`}
    >
      <h2>Сайн уу, {name}!</h2>
      <p>Горим: {settings.theme === "dark" ? "Харанхуй" : "Цайвар"}</p>
      <p>Үсэг: {sizeLabels[settings.fontSize]}</p>
      <button type="button">Жишээ товч</button>
    </section>
  );
}
"""

ARCHITECTURE = ModuleSpec(
    title="Модул 7 — State-ийн архитектур",
    description=(
        "State-ийг хаана байрлуулахаа шийдэж, дээш өргөх, Context, useReducer-ээр "
        "апп-ын state-ийг цэгцтэй зохион байгуулна."
    ),
    lessons=[
        # ------------------------------------------------------------------
        LessonSpec(
            title="State-ийг дээш өргөх",
            slug="state-deesh-urgeh",
            description="Хоёр component нэг state хуваалцах үед түүнийг нийтлэг эцэгт нь шилжүүлэх.",
            duration=840,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Хэд хэдэн component нэг state хуваалцах хэрэгтэй үеийг таних
- State-ийг хамгийн ойрын нийтлэг эцэг рүү өргөх гурван алхмыг хийх
- Хүүхдэд утга ба түүнийг өөрчлөх функцийг (`isOpen` + `onToggle`) props-оор өгөх

### Яагаад чухал вэ

Түгээмэл асуултын (FAQ) хэсгийг бодъё. Панель бүр өөрийн `isOpen`
state-тэй. Гэтэл «нэгийг нээхэд бусад нь хаагдах ёстой» гэсэн шаардлага
ирэв. Панель бүр зөвхөн өөрийгөө мэднэ: хөршийнхөө state-ийг уншиж ч,
өөрчилж ч чадахгүй.

React-д өгөгдөл зөвхөн **дээрээс доош** урсдаг. Хоёр component нэг
өгөгдлийг хуваалцах бол тэр өгөгдөл тэдний **нийтлэг эцэгт** байх ёстой.
Үүнийг **state-ийг дээш өргөх** (lifting state up) гэдэг. Энэ бол React
апп-ын архитектурын хамгийн түгээмэл алхам: табууд, шүүлтүүр, хайлтын
талбар ба үр дүнгийн жагсаалт — бүгд ийм.

### Эхлэл: панель бүр өөрийн state-тэй

```jsx
function Panel({ title, children }) {
  const [isOpen, setIsOpen] = useState(false);
  return (
    <section>
      <h2>
        <button onClick={() => setIsOpen(!isOpen)}>{title}</button>
      </h2>
      {isOpen && <p>{children}</p>}
    </section>
  );
}

export default function Faq() {
  return (
    <>
      <Panel title="Хүргэлт">24 цагийн дотор хүргэнэ.</Panel>
      <Panel title="Төлбөр">QPay эсвэл картаар төлнө.</Panel>
    </>
  );
}
```

Хоёр панель зэрэг нээгдэнэ: тус бүрийн state бие даасан. `Faq` аль нь
нээлттэйг ч мэдэхгүй.

### Алхам 1: хүүхдээс state-ийг хас

`useState`-ийг `Panel`-оос устгаад, `isOpen`-ийг prop болгож авна:

```jsx
function Panel({ title, isOpen, children }) {
  // useState алга — нээлттэй эсэхийг эцэг нь шийднэ
}
```

### Алхам 2: эцгээс утгаа дамжуул

Эхлээд гараар бичиж туршина:

```jsx
<Panel title="Хүргэлт" isOpen={true}>…</Panel>
<Panel title="Төлбөр" isOpen={false}>…</Panel>
```

### Алхам 3: эцэгт state нэм

Аль панель нээлттэйг **нэг тоогоор** — индексээр хадгална. Хүүхэд
өөрчлөлт хүсэхдээ эцгийн өгсөн функцийг дуудна:

```jsx
export default function Faq() {
  const [activeIndex, setActiveIndex] = useState(0);
  return (
    <>
      <Panel title="Хүргэлт" isOpen={activeIndex === 0} onShow={() => setActiveIndex(0)}>
        24 цагийн дотор хүргэнэ.
      </Panel>
      <Panel title="Төлбөр" isOpen={activeIndex === 1} onShow={() => setActiveIndex(1)}>
        QPay эсвэл картаар төлнө.
      </Panel>
    </>
  );
}

function Panel({ title, isOpen, onShow, children }) {
  return (
    <section>
      <h2>
        <button onClick={onShow}>{title}</button>
      </h2>
      {isOpen && <p>{children}</p>}
    </section>
  );
}
```

Яагаад хоёр `boolean` биш, нэг индекс вэ? Хоёр `boolean` зэрэг `true` байж
болно. Индекс бол «нэг л панель нээлттэй» гэсэн дүрмийг state-ийн
**хэлбэрт нь** шингээдэг: буруу төлөв үүсэх боломжгүй. Энэ санааг дараагийн
хичээлд үргэлжлүүлнэ.

### Өгөгдөл доош, үйл явдал дээш

```text
Faq  (activeIndex)
 ├── Panel  isOpen={activeIndex === 0}  onShow={() => setActiveIndex(0)}
 └── Panel  isOpen={activeIndex === 1}  onShow={() => setActiveIndex(1)}
```

Утга props-оор доош урсана. Хүүхэд өөрчлөлтийг **callback** дуудаж дээш
«мэдэгдэнэ». `Panel` setter-ийг огт мэдэхгүй — зөвхөн «намайг нээ» гэж
хэлнэ, яаж нээхийг эцэг нь шийднэ. Ийм props-ийг `on` + үйл явдлаар
нэрлэдэг: `onToggle`, `onSelect`, `onChange`.

### State-ийг хаана байрлуулах вэ

1. Тухайн state-ийг **ашигладаг** бүх component-ийг ол.
2. Тэдний хамгийн ойрын **нийтлэг эцгийг** ол.
3. State-ийг тэнд байрлуул.

Хэт дээш бүү өргө. Зөвхөн нэг component хэрэглэдэг state (жишээ нь
бичиж буй текст) өөр дээрээ үлдэнэ. Дээш өргөх тусам props-оор дамжуулах
замаа уртасна — энэ асуудлыг 3-р хичээлд үзнэ.

### Түгээмэл алдаа

- `onShow={setActiveIndex(1)}` — функц биш, **дуудалтын үр дүнг** өгсөн.
  Render бүрт state өөрчлөгдөж, `Too many re-renders` алдаа гарна.
  Зөв нь: `onShow={() => setActiveIndex(1)}`.
- Хүүхэд дотор `useState`-ийг үлдээх — хүүхэд prop-оо үл тоож, өөрийн
  state-ээ харуулсаар байна.

```quiz
Хоёр `Panel` тус бүр `useState(false)`-тэй. Нэгийг нь нээхэд нөгөө нь яах вэ?
- [ ] Автоматаар хаагдана
- [x] Юу ч болохгүй — state бүр бие даасан
- [ ] React алдаа шиднэ
> Component бүрийн state тусдаа. Хамтдаа ажиллуулах бол state-ийг нийтлэг эцэгт нь өргөнө.
```

```quiz
Энэ кодын алдаа юу вэ?

`<Panel isOpen={activeIndex === 1} onShow={setActiveIndex(1)} />`
- [ ] Алдаагүй, товч дарахад панель нээгдэнэ
- [x] `setActiveIndex(1)` render хийх үед шууд дуудагдаж, төгсгөлгүй render үүснэ
- [ ] `isOpen`-д харьцуулалт бичиж болохгүй
> `onShow`-д функц өгөх ёстой: `() => setActiveIndex(1)`.
```

### Дүгнэлт

Хэд хэдэн component нэг өгөгдөл хуваалцах бол state-ийг тэдний хамгийн
ойрын нийтлэг эцэгт байрлуулна. Эцэг нь утгыг props-оор доош өгч, хүүхэд
нь өөрчлөлтийг callback-аар дээш мэдэгдэнэ.
""",
            initial_code=vite(
                FAQ_APP_START,
                extra={"Panel.jsx": FAQ_PANEL_START},
                css=FAQ_CSS,
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 12 минут

«Хөтөч» дээр панелиудыг дарж үз — хэд хэдэн панель зэрэг нээгддэг.
`Panel`-ийн state-ийг `App` руу өргөж, нэг удаад зөвхөн нэг панель
нээлттэй байхаар болго. `Panel` нь `isOpen`, `onToggle` props авна.
Эхэндээ «Хүргэлт» нээлттэй байна. Нээлттэй панелийн товчийг дахин дарвал
хаагдана. Жагсаалтын доор аль панель нээлттэйг «Нээлттэй: Хүргэлт» гэж
харуул (бүгд хаалттай бол «Нээлттэй: —»).
""",
                tests=(
                    test(
                        "Эхэндээ зөвхөн «Хүргэлт» нээлттэй байна",
                        """
render(<App />);
expect(screen.text()).toContain("24 цагийн дотор");
expect(screen.text()).not.toContain("QPay");
expect(screen.text()).not.toContain("3 хоногийн");
""",
                    ),
                    test(
                        "Өөр панель нээхэд өмнөх нь хаагдана",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: /Төлбөр/ }));
expect(screen.text()).toContain("QPay");
expect(screen.text()).not.toContain("24 цагийн дотор");
await user.click(screen.getByRole("button", { name: /Буцаалт/ }));
expect(screen.text()).toContain("3 хоногийн");
expect(screen.text()).not.toContain("QPay");
""",
                    ),
                    test(
                        "Нээлттэй панелийн товчийг дахин дарвал хаагдана",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: /Төлбөр/ }));
await user.click(screen.getByRole("button", { name: /Төлбөр/ }));
expect(screen.text()).not.toContain("QPay");
expect(screen.text()).not.toContain("24 цагийн дотор");
""",
                    ),
                    test(
                        "Доор нь нээлттэй панелийн нэр харагдана",
                        """
render(<App />);
expect(screen.text()).toContain("Нээлттэй: Хүргэлт");
await user.click(screen.getByRole("button", { name: /Буцаалт/ }));
expect(screen.text()).toContain("Нээлттэй: Буцаалт");
await user.click(screen.getByRole("button", { name: /Буцаалт/ }));
expect(screen.text()).not.toContain("Нээлттэй: Буцаалт");
""",
                    ),
                    test(
                        "Panel нь isOpen-оор харагдаж, дарахад onToggle-ийг дуудна",
                        """
const Panel = mod("./Panel").default;
const onToggle = fn();
const { rerender } = render(
  <Panel title="Туршилт" isOpen={false} onToggle={onToggle}>
    Нууц хариулт
  </Panel>
);
expect(screen.queryByText("Нууц хариулт")).toBeNull();
await user.click(screen.getByRole("button", { name: /Туршилт/ }));
expect(onToggle).toHaveBeenCalledTimes(1);
expect(screen.queryByText("Нууц хариулт")).toBeNull();
rerender(
  <Panel title="Туршилт" isOpen={true} onToggle={onToggle}>
    Нууц хариулт
  </Panel>
);
expect(screen.getByText("Нууц хариулт")).toBeInTheDocument();
""",
                    ),
                ),
                tips="""\
- `Panel`-оос `useState`-ийг бүхэлд нь устга. Товч нь `onToggle`-ийг л
  дуудна — нээх, хаахыг `App` шийднэ.
- `App`-д `const [activeIndex, setActiveIndex] = useState(0);`. Хаалттай
  төлөвийг `null`-оор илэрхийлж болно.
- `map`-ийн хоёр дахь аргумент нь индекс: `faqs.map((faq, index) => …)`.
  `isOpen={activeIndex === index}`.
- Toggle: дарсан панель аль хэдийн нээлттэй бол `null`, эс бөгөөс тэр
  индекс.
- `onToggle={() => handleToggle(index)}` — arrow функцээр ороо. `onToggle={handleToggle(index)}`
  гэвэл render хийх үед шууд дуудагдана.
- Доорх мөрийн нэрийг `faqs[activeIndex].title`-ээс ав — тусдаа state
  хэрэггүй.
""",
                solution=solution(
                    App_jsx="""\
import { useState } from "react";
import Panel from "./Panel";

const faqs = [
  { title: "Хүргэлт", answer: "Улаанбаатар хотод захиалгыг 24 цагийн дотор хүргэнэ." },
  { title: "Төлбөр", answer: "QPay, банкны карт эсвэл бэлнээр төлж болно." },
  { title: "Буцаалт", answer: "Гэмтэлтэй барааг 3 хоногийн дотор сольж өгнө." },
];

export default function App() {
  const [activeIndex, setActiveIndex] = useState(0);

  function handleToggle(index) {
    setActiveIndex(activeIndex === index ? null : index);
  }

  const active = activeIndex === null ? null : faqs[activeIndex];

  return (
    <main>
      <h1>❓ Түгээмэл асуулт</h1>
      {faqs.map((faq, index) => (
        <Panel
          key={faq.title}
          title={faq.title}
          isOpen={activeIndex === index}
          onToggle={() => handleToggle(index)}
        >
          {faq.answer}
        </Panel>
      ))}
      <p>Нээлттэй: {active ? active.title : "—"}</p>
    </main>
  );
}
""",
                    Panel_jsx="""\
export default function Panel({ title, isOpen, onToggle, children }) {
  return (
    <section className="panel">
      <h2>
        <button onClick={onToggle} aria-expanded={isOpen}>
          <span aria-hidden="true">{isOpen ? "▾" : "▸"}</span> {title}
        </button>
      </h2>
      {isOpen && <p>{children}</p>}
    </section>
  );
}
""",
                ),
            ),
        ),
        # ------------------------------------------------------------------
        LessonSpec(
            title="Нэг үнэн эх сурвалж",
            slug="neg-unen-survalj",
            description="Давхардсан, зөрчилдөх state-ээс зайлсхийж, controlled ба uncontrolled component-ийг ялгах.",
            duration=900,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Давхардсан болон хоорондоо зөрчилдөх state-ийг таньж засах
- Объектын хуулбарын оронд `id` хадгалж, бусдыг нь тооцоолох
- Props-ийг state-д хуулахын аюулыг ойлгох
- Controlled ба uncontrolled component-ийн ялгааг мэдэх

### Яагаад чухал вэ

Нэг өгөгдөл хоёр газар хадгалагдвал эрт орой хэзээ нэгэн цагт зөрнө.
Модул 0-ийн DOM тоологчийг санаарай: нэг газрыг шинэчлээд нөгөөг нь
мартвал дэлгэц худлаа хэлдэг. React-д ч адил: хоёр state нэг зүйлийг
илэрхийлвэл нэгийг нь шинэчлэх бүрт нөгөөг нь бас шинэчлэхээ санах хэрэгтэй.

Зарчим нь энгийн: мэдээлэл бүр **нэг л газар** хадгалагдана. Үүнийг **нэг
үнэн эх сурвалж** (single source of truth) гэдэг. Бусад бүхнийг тэндээс
тооцоолно.

### Давхардал 1: объектын хуулбар

```jsx
const [items, setItems] = useState(initialItems);
const [selected, setSelected] = useState(initialItems[0]); // ❌ хуулбар
```

`selected` нь `items` доторх объектын **хоёр дахь хуулбар**. Барааны тоог
нэмэхэд `items`-д шинэ объект үүснэ (immutable шинэчлэл), харин `selected`
хуучин объектыг заасаар үлдэнэ. Дэлгэрэнгүй хэсэг хуучин тоог харуулна.

Засвар: зөвхөн `id`-г хадгалж, объектыг render бүрт олно:

```jsx
const [selectedId, setSelectedId] = useState(initialItems[0].id); // ✅
const selected = items.find((item) => item.id === selectedId);
```

`id` өөрчлөгддөггүй тул хэзээ ч хуучрахгүй.

### Давхардал 2: тооцож болох утга

```jsx
const [totalQty, setTotalQty] = useState(4); // ❌
```

Модул 3-т үзсэн уламжлагдсан утга (derived value): `items`-ээс тооцоолж
болох бүхнийг state-д хийхгүй.

```jsx
const totalQty = items.reduce((sum, item) => sum + item.qty, 0); // ✅
```

`firstName`, `lastName`-ээс `fullName`, жагсаалт ба хайлтын үгээс
шүүсэн жагсаалт — бүгд ийм.

### Зөрчилдөх state

```jsx
const [isSending, setIsSending] = useState(false);
const [isSent, setIsSent] = useState(false);
```

Хоёулаа `true` байх боломжтой — «илгээж байгаа, бас илгээсэн» гэсэн
утгагүй төлөв. Оронд нь нэг `status`:

```jsx
const [status, setStatus] = useState("typing"); // "typing" | "sending" | "sent"
const isSending = status === "sending";
```

Буруу төлөв state-ийн хэлбэрээрээ боломжгүй болно.

### Props-ийг state-д бүү хуулбарла

```jsx
function Price({ amount }) {
  const [value, setValue] = useState(amount); // ❌
  return <p>{value}₮</p>;
}
```

`useState(amount)`-ийн анхны утга зөвхөн **эхний** render-т ашиглагдана.
Эцэг нь `amount`-ийг өөрчилбөл `value` хуучин хэвээр үлдэнэ. Prop-оо шууд
ашигла: `<p>{amount}₮</p>`. Зориуд анхны утга л хэрэгтэй бол нэрийг нь
`initialAmount` гэж өгч, уншигчид тодорхой болго.

### Controlled ба uncontrolled component

Өмнөх хичээлийн хоёр `Panel`-ийг харьцуулъя:

| | Өөрийн `useState`-тэй | `isOpen` + `onToggle` props-той |
|---|---|---|
| Нэр | **uncontrolled** | **controlled** |
| Хэн шийдэх | Component өөрөө | Эцэг нь |
| Давуу тал | Хэрэглэхэд амар, props цөөн | Бусадтай уялдуулж болно |
| Сул тал | Гаднаас удирдах боломжгүй | Эцэг нь state-ээ хадгална |

Модул 4-ийн input-тэй яг ижил санаа: `value` + `onChange` өгвөл
controlled, `defaultValue` өгвөл uncontrolled — утгыг DOM өөрөө хадгална.

Component бичихдээ «энэ мэдээллийг гаднаас удирдах хэрэгтэй юу?» гэж асуу.
Хэрэгтэй бол controlled болго. Бэлэн UI сангууд (жишээ нь Radix, MUI)
ихэвчлэн хоёуланг нь дэмждэг: `open` өгвөл controlled, `defaultOpen`
өгвөл uncontrolled.

### State нэмэхийн өмнө өөрөөсөө асуу

1. Үүнийг өөр state эсвэл props-оос **тооцож** болох уу? → state биш.
2. Энэ нь өөр state-ийн **хуулбар** уу? → `id` хадгал.
3. Хоёр state **зэрэг** үнэн байж болохгүй юу? → нэг `status` болго.

```quiz
Сагсанд `items` state байна. Нийт үнийг хаана байлгах вэ?
- [ ] Тусдаа `useState`-д, бараа нэмэх бүрт шинэчилнэ
- [x] State-д хадгалахгүй — render бүрт `items`-ээс тооцно
- [ ] `useRef`-д
> Тооцож болох утгыг хадгалбал хоёр эх сурвалж үүсч, эрт орой хэзээ нэгэн цагт зөрнө.
```

```quiz
`const [selected, setSelected] = useState(items[0]);` гэж бичсэн. Хэрэглэгч сонгосон барааныхаа тоог жагсаалтаас нэмэхэд дэлгэрэнгүй хэсэгт юу харагдах вэ?
- [x] Хуучин тоо — `selected` нь хуучин объектыг заасаар байна
- [ ] Шинэ тоо — React өөрөө шинэчилнэ
- [ ] Алдаа гарна
> Immutable шинэчлэл шинэ объект үүсгэдэг. `selectedId` хадгалаад объектыг `find`-аар олбол үргэлж шинэ утгыг харна.
```

```quiz
`<Tabs active={tab} onChange={setTab} />` — энэ `Tabs` ямар component вэ?
- [x] Controlled — идэвхтэй табыг эцэг нь удирдана
- [ ] Uncontrolled — таб өөрийн state-тэй
- [ ] Аль нь ч биш
> Гол мэдээлэл нь (идэвхтэй таб) props-оор ирж, өөрчлөлтийг callback-аар мэдэгдэж байна.
```

### Дүгнэлт

Мэдээлэл бүрийг нэг л газар хадгал. Объектын хуулбарын оронд `id`,
тооцож болох утгын оронд тооцоолол, зөрчилдөх `boolean`-уудын оронд нэг
`status`. Controlled component-ийг эцэг нь удирддаг, uncontrolled нь
өөрөө.
""",
            initial_code=vite(CART_ROWS_APP_START, css=CART_ROWS_CSS),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 12 минут

Сагсанд хоёр алдаа бий. «Хөтөч» дээр «Алим»-ын «+» товчийг дарж үз:
жагсаалт дахь тоо өөрчлөгдөх ч «Сонгосон» хэсэг хуучин тоогоо харуулна.
«Талх»-ын «−»-ийг хэд хэдэн удаа дарвал «Нийт ширхэг» буруу болно.
Давхардсан хоёр state-ийг устгаад, `selectedId` хадгалж, сонгосон бараа
болон нийт ширхэгийг `items`-ээс тооцоол.
""",
                tests=(
                    test(
                        "Сонгосон барааны тоо, дүн жагсаалттай үргэлж ижил байна",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: "Алим нэмэх" }));
await user.click(screen.getByRole("button", { name: "Алим нэмэх" }));
expect(screen.text()).toContain("Тоо: 3");
expect(screen.text()).toContain("Дүн: 8400₮");
""",
                    ),
                    test(
                        "Өөр бараа сонгоод тоог өөрчлөхөд дэлгэрэнгүй шинэчлэгдэнэ",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: "Сүү" }));
expect(screen.text()).toContain("Сонгосон: Сүү");
expect(screen.text()).toContain("Тоо: 2");
await user.click(screen.getByRole("button", { name: "Сүү нэмэх" }));
expect(screen.text()).toContain("Тоо: 3");
expect(screen.text()).toContain("Дүн: 9600₮");
""",
                    ),
                    test(
                        "Нийт ширхэг нь барааны тоонуудын нийлбэртэй үргэлж тэнцүү",
                        """
render(<App />);
expect(screen.text()).toContain("Нийт ширхэг: 4");
await user.click(screen.getByRole("button", { name: "Талх хасах" }));
await user.click(screen.getByRole("button", { name: "Талх хасах" }));
await user.click(screen.getByRole("button", { name: "Талх хасах" }));
expect(screen.text()).toContain("Нийт ширхэг: 3");
await user.click(screen.getByRole("button", { name: "Алим нэмэх" }));
expect(screen.text()).toContain("Нийт ширхэг: 4");
""",
                    ),
                ),
                tips="""\
- `selected`-ийн оронд `const [selectedId, setSelectedId] = useState(1);`
  гэж зөвхөн id хадгал. Сонгох товч `setSelectedId(item.id)` дуудна.
- Объектыг render бүрт ол: `const selected = items.find((item) => item.id === selectedId);`
- `totalQty` state-ийг бүр устгаад `reduce`-ээр тооцоол. Тэгвэл `changeQty`
  дотор `setTotalQty` хэрэггүй болно.
- `changeQty` дотор `setSelected`-ийг бас дуудаж хоёр state-ийг «синк»
  хийх нь ажиллана, гэхдээ энэ бол асуудлыг нууж буй хэрэг. Хуулбарыг бүр
  устга.
""",
                solution=solution(App_jsx=CART_ROWS_APP_SOLUTION),
            ),
        ),
        # ------------------------------------------------------------------
        LessonSpec(
            title="Prop drilling",
            slug="prop-drilling",
            description="Props-ийг олон давхар дамжуулах асуудал ба composition-оор шийдэх нь.",
            duration=900,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Prop drilling гэж юу болох, хэзээ асуудал болдгийг таних
- Props-оор шууд дамжуулах нь хэзээ зүгээр, бүр зөв болохыг мэдэх
- Composition (`children`, элемент prop)-оор завсрын component-уудыг
  хамааралгүй props-оос чөлөөлөх

### Яагаад чухал вэ

State-ийг дээш өргөх тусам түүнийг хэрэглэдэг component хүртэлх зам
урт болно. Завсрын component-ууд өөрсдөө огт ашигладаггүй prop-ийг
зөвхөн «цааш нь дамжуулахын тулд» авч эхэлнэ. Үүнийг **prop drilling**
(props-оор өрөмдөх) гэдэг. Жижиг апп-д анзаарагдахгүй ч апп томрох тусам
prop нэмэх, нэр солих бүрт таван файл засах болно.

### Асуудал

```jsx
export default function App() {
  const [user, setUser] = useState({ name: "Сараа", plan: "Үнэгүй" });
  return <Layout user={user} />;
}

function Layout({ user }) {       // user-ийг ашигладаггүй
  return (
    <div>
      <Header user={user} />
      <main>…</main>
    </div>
  );
}

function Header({ user }) {       // энэ ч ашигладаггүй
  return (
    <header>
      <Logo />
      <UserBadge user={user} />
    </header>
  );
}

function UserBadge({ user }) {    // ганцхан энэ л ашиглана
  return <span>{user.name}</span>;
}
```

Сул тал нь:

- `Layout`, `Header` хамааралгүй props-оор дүүрнэ. `user`-ийн хажууд
  `onLogout` нэмэхэд бүх давхрыг засна.
- `Layout`-ийг өөр хуудсанд дахин ашиглахад заавал `user` өгөх хэрэгтэй
  болно.
- Өгөгдөл хаанаас ирснийг мөшгихийн тулд олон файл ухна.

### Хэзээ зүгээр вэ

Prop drilling бол «муу» зүйл биш. Хоёр, гурван давхар, завсрын component
ч тэр prop-ийг ашигладаг бол props бол хамгийн энгийн, ил тод шийдэл:
өгөгдлийн урсгал харагдаж, component бүр юунаас хамаарахаа props-оороо
зарлана. Асуудал нь давхар олон, завсрынхан огт ашигладаггүй, олон prop
бөөнөөрөө дамжиж эхлэх үед л гарна.

### Шийдэл 1: composition ба `children`

Завсрын component юу харуулахаа заавал мэдэх албагүй. Тэр «хайрцаг» болж,
агуулгаа `children`-оор авна (Модул 2):

```jsx
function Header({ children }) {
  return (
    <header>
      <Logo />
      {children}
    </header>
  );
}

// App дотор:
<Header>
  <UserBadge user={user} />
</Header>
```

Одоо `UserBadge`-ийг `App` өөрөө үүсгэж, `user`-ийг шууд өгнө. `Header`
`user`-ийн тухай юу ч мэдэхгүй.

### Шийдэл 2: элемент prop («slot»)

Component-д хэд хэдэн «нүх» хэрэгтэй бол `children`-оос гадна элементийг
ердийн prop-оор дамжуулна. JSX элемент бол энгийн JavaScript утга тул
хувьсагчид хадгалж, prop болгож болно:

```jsx
function Layout({ header, children }) {
  return (
    <div className="layout">
      {header}
      <main>{children}</main>
    </div>
  );
}

export default function App() {
  const [user, setUser] = useState({ name: "Сараа", plan: "Үнэгүй" });
  return (
    <Layout
      header={
        <Header>
          <UserBadge user={user} />
        </Header>
      }
    >
      <PlanCard user={user} onUpgrade={() => setUser({ ...user, plan: "Standard" })} />
    </Layout>
  );
}
```

Component-уудын мод өмнөхтэй ижил — `Layout` дотор `Header`, түүний дотор
`UserBadge`. Өөрчлөгдсөн нь props-ийн зам: бүх өгөгдөл `App`-д байж,
хэрэгтэй component-д нь **шууд** очно.

### Composition эсвэл Context?

Composition бол эхний сонголт: энгийн, ил тод, нэмэлт API шаардахгүй.
Харин theme, нэвтэрсэн хэрэглэгч, хэл гэх мэт апп-ын өнцөг булан бүрт,
олон гүн газар хэрэгтэй өгөгдөлд дараагийн хичээлийн **Context**
тохиромжтой. React-ийн баримт бичиг ч «Context-оос өмнө props-оор
дамжуулах эсвэл `children`-оор задлахыг оролд» гэж зөвлөдөг.

### Бодит төсөлд

UI сангуудын `Card`, `Dialog`, `PageLayout` гэх мэт component-ууд
ихэвчлэн `children` болон `header`, `footer`, `actions` гэх мэт элемент
prop-оор ажилладаг. Тэд доторх агуулгынхаа өгөгдлийг мэдэх шаардлагагүй
тул хаана ч дахин ашиглагдана.

```quiz
Prop drilling гэж юу вэ?
- [ ] Props-ийг state-д хуулах
- [x] Өгөгдлийг, түүнийг ашигладаггүй завсрын component-уудаар дамжуулж гүн рүү хүргэх
- [ ] Нэг component-д хэт олон props өгөх
> Асуудал нь props өөрөө биш, ашигладаггүй component-уудаар «дамжин өнгөрөх» зам.
```

```quiz
`<Header><UserBadge user={user} /></Header>` гэж бичсэн бол `Header`-т `user` prop хэрэгтэй юу?
- [ ] Тийм — `UserBadge` түүний дотор харагддаг
- [x] Үгүй — `UserBadge`-ийг `App` үүсгэдэг, `Header` зөвхөн `children`-оо харуулна
- [ ] Тийм, эс бөгөөс алдаа гарна
> Элемент хаана үүссэн нь чухал: `user`-ийг `App` шууд өгсөн тул `Header` дамжуулах шаардлагагүй.
```

```quiz
Аль тохиолдолд props-оор шууд дамжуулах нь хамгийн зөв вэ?
- [x] Хоёр давхар, завсрын component ч тэр prop-ийг ашигладаг
- [ ] Хаана ч — Context үргэлж илүү
- [ ] Хэзээ ч — prop drilling үргэлж алдаа
> Цөөн давхар props бол хамгийн ил тод шийдэл. Composition, Context-ийг асуудал гарсан үед хэрэглэнэ.
```

### Дүгнэлт

Prop drilling бол ашигладаггүй component-уудаар props дамжуулах зам. Цөөн
давхар бол хэвийн. Урт болбол эхлээд composition-оор (`children`,
элемент prop) завсрын component-уудыг «хайрцаг» болго. Апп даяар хэрэгтэй
өгөгдөлд Context-ийг дараагийн хичээлд үзнэ.
""",
            initial_code=vite(
                DASHBOARD_APP_START,
                extra={
                    "Layout.jsx": DASHBOARD_LAYOUT_START,
                    "Header.jsx": DASHBOARD_HEADER_START,
                },
                locked={
                    "UserBadge.jsx": DASHBOARD_USER_BADGE,
                    "PlanCard.jsx": DASHBOARD_PLAN_CARD,
                },
                css=DASHBOARD_CSS,
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐ · 15 минут

`user` ба `onUpgrade` нь `App → Layout → Header → UserBadge`,
`App → Layout → PlanCard` гэж дамжиж байна. `Layout`, `Header` хоёр
тэдгээрийг огт ашигладаггүй. Composition-оор хоёуланг нь эдгээр props-оос
чөлөөл: `Layout` нь `header` ба `children` prop авч, `children`-оо
`<main>` дотор харуулна; `Header` нь `children`-оо лого-ийн хажууд
харуулна. `UserBadge`, `PlanCard`-ийг `App` өөрөө render хийнэ. Апп өмнөх
шигээ ажиллах ёстой.
""",
                tests=(
                    test(
                        "Layout нь header-ийг, children-ийг <main> дотор харуулна",
                        """
const Layout = mod("./Layout").default;
render(
  <Layout header={<p>Толгой хэсэг</p>}>
    <p>Үндсэн агуулга</p>
  </Layout>
);
expect(screen.getByText("Толгой хэсэг")).toBeInTheDocument();
expect(within(screen.getByRole("main")).getByText("Үндсэн агуулга")).toBeInTheDocument();
""",
                    ),
                    test(
                        "Header нь лого-той хамт children-оо харуулна",
                        """
const Header = mod("./Header").default;
render(
  <Header>
    <span>Хүүхэд элемент</span>
  </Header>
);
const banner = screen.getByRole("banner");
expect(banner).toHaveTextContent("MedlegHub");
expect(banner).toHaveTextContent("Хүүхэд элемент");
""",
                    ),
                    test(
                        "Толгой хэсэгт хэрэглэгчийн нэр, багц, доор нь самбарын гарчиг харагдана",
                        """
render(<App />);
const banner = screen.getByRole("banner");
expect(banner).toHaveTextContent("Сараа");
expect(banner).toHaveTextContent("Үнэгүй");
expect(screen.getByRole("heading", { name: "Хяналтын самбар" })).toBeInTheDocument();
""",
                    ),
                    test(
                        "«Standard авах» дарахад толгой хэсэг ба карт хоёулаа шинэчлэгдэнэ",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: "Standard авах" }));
expect(screen.getByRole("banner")).toHaveTextContent("Standard");
expect(screen.getByRole("main")).toHaveTextContent("Таны багц: Standard");
""",
                    ),
                ),
                tips="""\
- `Layout({ header, children })` нь `{header}`-ийг дээр, `<main>{children}</main>`-ийг
  доор нь буцаана. `Header`, `PlanCard`-ийн import-ууд `Layout.jsx`-д
  хэрэггүй болно.
- `Header({ children })` нь лого-ийн дараа `{children}`-оо харуулна.
- `App`-д `<Layout header={<Header><UserBadge user={user} /></Header>}>`, дотор
  нь гарчиг ба `<PlanCard user={user} onUpgrade={upgrade} />`.
- «Cannot read properties of undefined (reading 'avatar')» гэвэл `Header`
  `UserBadge`-ийг `user`-гүйгээр render хийсээр байна.
""",
                solution=solution(
                    App_jsx="""\
import { useState } from "react";
import Header from "./Header";
import Layout from "./Layout";
import PlanCard from "./PlanCard";
import UserBadge from "./UserBadge";

export default function App() {
  const [user, setUser] = useState({ name: "Сараа", avatar: "👩‍🎓", plan: "Үнэгүй" });

  function upgrade() {
    setUser({ ...user, plan: "Standard" });
  }

  return (
    <Layout
      header={
        <Header>
          <UserBadge user={user} />
        </Header>
      }
    >
      <h1>Хяналтын самбар</h1>
      <PlanCard user={user} onUpgrade={upgrade} />
    </Layout>
  );
}
""",
                    Layout_jsx="""\
export default function Layout({ header, children }) {
  return (
    <div className="layout">
      {header}
      <main>{children}</main>
    </div>
  );
}
""",
                    Header_jsx="""\
export default function Header({ children }) {
  return (
    <header className="header">
      <strong>🎓 MedlegHub</strong>
      {children}
    </header>
  );
}
""",
                ),
            ),
        ),
        # ------------------------------------------------------------------
        LessonSpec(
            title="Context ба useContext",
            slug="context",
            description="createContext, provider, useContext-оор утгыг props-гүйгээр гүн рүү хүргэх.",
            duration=960,
            language=JSX,
            content="""\
### Энэ хичээлээр

- `createContext`-оор context үүсгэж, анхдагч утга өгөх
- Утгыг `<ThemeContext value={…}>`-оор доош нь «цацах»
- `useContext`-оор хамгийн ойрын provider-ийн утгыг унших
- Context хэзээ тохирох, хэзээ тохирохгүйг мэдэх

### Яагаад чухал вэ

Зарим өгөгдөл апп-ын бараг бүх хэсэгт хэрэгтэй: theme (цайвар эсвэл
харанхуй), хэл, нэвтэрсэн хэрэглэгч. Үүнийг хуудас бүр, товч бүр хүртэл
props-оор дамжуулах нь өмнөх хичээлийн prop drilling-ийн хамгийн муу
хувилбар. **Context** нь утгыг модны дээд хэсэгт нэг удаа тавьж, доорх
ямар ч component хэдэн давхар гүнд байсан props-гүйгээр шууд уншдаг
болгоно.

### Алхам 1: үүсгэх

```jsx
// ThemeContext.js
import { createContext } from "react";

export const ThemeContext = createContext("light");
```

`"light"` бол **анхдагч утга** — дээр нь provider байхгүй үед ашиглагдана.
Context-ийг тусдаа файлд үүсгэж export хийдэг нь хэвшил: түүнийг хангах
component болон унших component хоёулаа импортлоно.

### Алхам 2: хангах (provide)

```jsx
import { useState } from "react";
import { ThemeContext } from "./ThemeContext";

export default function App() {
  const [theme, setTheme] = useState("dark");
  return (
    <ThemeContext value={theme}>
      <Page />
    </ThemeContext>
  );
}
```

`ThemeContext`-ийг component шиг бичээд `value`-д утгаа өгнө. Доторх бүх
мод тэр утгыг «харна».

### Алхам 3: унших

```jsx
import { useContext } from "react";
import { ThemeContext } from "./ThemeContext";

function Button({ children }) {
  const theme = useContext(ThemeContext);
  return <button className={`btn btn-${theme}`}>{children}</button>;
}
```

`Page` болон түүний доторх component-ууд theme-ийн тухай юу ч мэдэхгүй.
`Button` өөрт хэрэгтэй утгаа өөрөө уншина. `useContext` бол hook тул
дүрэм нь ижил: component-ийн дээд түвшинд дуудна.

### `.Provider` — хуучин бичлэг

React 19-өөс өмнө context-ийг `.Provider`-оор хангадаг байсан:

```jsx
<ThemeContext.Provider value={theme}>
  <Page />
</ThemeContext.Provider>
```

Энэ бичлэг React 19-д ч ажилладаг бөгөөд интернэт дэх жишээ, хуучин
төслүүдэд байнга таарна. Утга нь яг ижил. Гэхдээ цаашид хуучирсан
(deprecated) гэж зарлагдах тул шинэ кодод `<ThemeContext value={…}>`-ийг
бич.

### Хамгийн ойрын provider ялна

`useContext` дуудсан component-оос **дээш** чиглэн хамгийн ойрын
provider-ийг хайна:

```jsx
<ThemeContext value="dark">
  <Toolbar />               {/* dark */}
  <ThemeContext value="light">
    <Sidebar />             {/* light */}
  </ThemeContext>
</ThemeContext>
```

Хуудсын нэг хэсгийг өөр өнгөөр харуулах гэх мэтэд ашиглана. Provider нь
уншиж буй component-оос **дээр** байх ёстой: нэг component өөрөө
provider-ийг буцаагаад, мөн өөрөө `useContext` дуудвал тэр provider-ийг
харахгүй.

```jsx
const ColorContext = createContext("улаан");

function Label() {
  return <p>{useContext(ColorContext)}</p>;
}

export default function App() {
  return (
    <>
      <Label />
      <ColorContext value="ногоон">
        <Label />
      </ColorContext>
    </>
  );
}
```

```quiz
Дээрх `App` дэлгэцэнд юу харуулах вэ?
- [ ] «ногоон», «ногоон»
- [x] «улаан», «ногоон»
- [ ] «улаан», «улаан»
> Эхний `Label`-ийн дээр provider алга тул анхдагч утга «улаан» ирнэ. Хоёр дахь нь provider дотор байна.
```

### Анхдагч утга ба өөрчлөлт

Provider олдохгүй бол `createContext`-д өгсөн утга ирнэ. Энэ нь
component-ийг тусад нь турших, харуулахад хэрэгтэй. Анхдагч утга
**хэзээ ч өөрчлөгдөхгүй** — state биш. Утгыг өөрчлөх бол provider-ийн
`value`-г state-тэй холбоно (дээрх `App` шиг).

Provider-ийн `value` өөрчлөгдөхөд тэр context-ийг уншдаг **бүх**
component дахин render хийнэ, завсрын component-ууд юу ч дамжуулаагүй
байсан ч.

### Хэзээ хэрэглэх вэ

| Тохиромжтой | Тохиромжгүй |
|---|---|
| Theme, хэл, нэвтэрсэн хэрэглэгч, сагс | Нэг хоёр давхар дамжих өгөгдөл |
| Апп даяар нэг утгатай өгөгдөл | Зөвхөн нэг хэсэгт хэрэгтэй state |
| Олон газар, гүнд уншигддаг | Composition-оор шийдэгдэх асуудал |

Context-ийг хэт их хэрэглэвэл component хаанаас өгөгдөл авснаа нууж,
тусад нь дахин ашиглахад хэцүү болно. Эхлээд props, composition — дараа нь
Context.

### Бодит төсөлд

Context-ийг ихэвчлэн `src/contexts/` хавтаст хадгална. react-router,
TanStack Query зэрэг сангууд ч дотроо context ашигладаг: Модул 9-ийн
`<QueryClientProvider>` бол яг ийм provider. React 19-д context-ийг
`use(ThemeContext)`-оор ч уншиж болно — `useContext`-оос ялгаатай нь
нөхцөл дотор дуудаж болно (Модул 11).

```quiz
Энэ кодод `theme` ямар утгатай вэ? (`createContext("light")`)

`function App() { const theme = useContext(ThemeContext); return <ThemeContext value="dark"><p>{theme}</p></ThemeContext>; }`
- [ ] `"dark"`
- [x] `"light"`
- [ ] `undefined`
> Provider нь `App`-ын **доор** байна. `useContext` зөвхөн дээрх provider-ийг хардаг тул анхдагч утга ирнэ.
```

### Дүгнэлт

`createContext(анхдагч)` → `<Context value={…}>` → `useContext(Context)`.
Уншиж буй component-оос дээрх хамгийн ойрын provider-ийн утга ирнэ,
provider алга бол анхдагч утга. Хуучин кодод `.Provider` гэж бичсэн
байдаг. Context-ийг апп даяар хэрэгтэй өгөгдөлд хэрэглэ.
""",
            initial_code=vite(
                LANGUAGE_APP_START,
                extra={
                    "LanguageContext.js": LANGUAGE_CONTEXT_START,
                    "Greeting.jsx": LANGUAGE_GREETING_START,
                    "CartButton.jsx": LANGUAGE_BUTTON_START,
                },
                locked={"Page.jsx": LANGUAGE_PAGE, "translations.js": LANGUAGE_TRANSLATIONS},
                css=SHOP_CSS,
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 12 минут

«🌐 English» товч `App`-ын state-ийг өөрчилдөг ч `Greeting`, `CartButton`
хоёр үргэлж монголоор бичигдэнэ. `LanguageContext.js`-д анхдагч утга нь
`"mn"` байх `LanguageContext` үүсгэж (нэртэй export), `App`-д `Page`-ийг
түүгээр ороо. `Greeting`, `CartButton` хэлээ context-оос уншина.
`Page.jsx`-ийг өөрчлөх шаардлагагүй — props-оор юу ч дамжуулахгүй.
""",
                tests=(
                    test(
                        "LanguageContext-ийн анхдагч утга нь «mn»",
                        """
const m = mod("./LanguageContext");
const LanguageContext = m.LanguageContext ?? m.default;
function Probe() {
  const language = React.useContext(LanguageContext);
  return <p>Хэл: {language}</p>;
}
render(<Probe />);
expect(screen.text()).toContain("Хэл: mn");
""",
                    ),
                    test(
                        "Greeting нь хэлээ context-оос уншина",
                        """
const m = mod("./LanguageContext");
const LanguageContext = m.LanguageContext ?? m.default;
const Greeting = mod("./Greeting").default;
render(
  <LanguageContext value="en">
    <Greeting />
  </LanguageContext>
);
expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent("Hello!");
""",
                    ),
                    test(
                        "CartButton нь context-оос уншиж, provider-гүй бол монголоор бичигдэнэ",
                        """
const m = mod("./LanguageContext");
const LanguageContext = m.LanguageContext ?? m.default;
const CartButton = mod("./CartButton").default;
const english = render(
  <LanguageContext value="en">
    <CartButton />
  </LanguageContext>
).container;
const fallback = render(<CartButton />).container;
expect(within(english).getByRole("button")).toHaveTextContent("Add to cart");
expect(within(fallback).getByRole("button")).toHaveTextContent("Сагсанд нэмэх");
""",
                    ),
                    test(
                        "Хэл солих товч гарчиг ба бүх товчны текстийг солино",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: /English/ }));
expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent("Hello!");
expect(screen.getAllByRole("button", { name: "Add to cart" })).toHaveLength(2);
await user.click(screen.getByRole("button", { name: /Монгол/ }));
expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent("Сайн байна уу!");
expect(screen.getAllByRole("button", { name: "Сагсанд нэмэх" })).toHaveLength(2);
""",
                    ),
                ),
                tips="""\
- `LanguageContext.js`: `import { createContext } from "react";` дараа нь
  `export const LanguageContext = createContext("mn");`
- `App`: `<LanguageContext value={language}><Page /></LanguageContext>`. Хэл
  солих товч provider-ийн гадна байж болно — `App` state-ээ шууд мэднэ.
- `Greeting`, `CartButton`: `const language = useContext(LanguageContext);`
  — `useContext`-ийг `react`-ээс, `LanguageContext`-ийг `./LanguageContext`-оос
  импортло.
- `createContext`-д өгсөн утга зөвхөн provider байхгүй үед ирнэ. Provider
  тавиагүй бол товч дарахад юу ч өөрчлөгдөхгүй.
""",
                solution=solution(
                    App_jsx="""\
import { useState } from "react";
import { LanguageContext } from "./LanguageContext";
import Page from "./Page";
import { translations } from "./translations";

export default function App() {
  const [language, setLanguage] = useState("mn");

  function toggleLanguage() {
    setLanguage(language === "mn" ? "en" : "mn");
  }

  return (
    <main>
      <button className="lang" onClick={toggleLanguage}>
        🌐 {translations[language].switchLanguage}
      </button>
      <LanguageContext value={language}>
        <Page />
      </LanguageContext>
    </main>
  );
}
""",
                    LanguageContext_js="""\
import { createContext } from "react";

export const LanguageContext = createContext("mn");
""",
                    Greeting_jsx="""\
import { useContext } from "react";
import { LanguageContext } from "./LanguageContext";
import { translations } from "./translations";

export default function Greeting() {
  const language = useContext(LanguageContext);
  return <h1>{translations[language].greeting}</h1>;
}
""",
                    CartButton_jsx="""\
import { useContext } from "react";
import { LanguageContext } from "./LanguageContext";
import { translations } from "./translations";

export default function CartButton() {
  const language = useContext(LanguageContext);
  return <button className="cart-button">{translations[language].addToCart}</button>;
}
""",
                ),
            ),
        ),
        # ------------------------------------------------------------------
        LessonSpec(
            title="Context + state: provider component",
            slug="context-provider",
            description="State ба үйлдлүүдийг AuthProvider-т нууж, useAuth hook-оор хэрэглэх.",
            duration=960,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Context-оор state ба түүнийг өөрчлөх функцүүдийг хамт дамжуулах
- Бүх логикийг нэг **provider component** (`AuthProvider`)-д нууж цэгцлэх
- Provider-гүй үед ойлгомжтой алдаа шиддэг `useAuth()` hook бичих

### Яагаад чухал вэ

Өмнөх хичээлд context-ийн утга `App`-ын state байсан — state, setter,
логик бүгд `App` дотор үлдсэн. Нэвтрэлт шиг бодит өгөгдөлд `login`,
`logout`, дараа нь серверийн хүсэлт, токен хадгалах гэх мэт нэмэгдэнэ.
Энэ бүгдийг `App`-д бичвэл `App` хэт томорч, хэн юуг өөрчилж болохыг
хянахад хэцүү болно.

Шийдэл: context-ийн бүх логикийг нэг **provider component**-д нууж,
гадагш зөвхөн цэвэрхэн API — `useAuth()` hook гаргана. Бодит React төсөлд
хамгийн их таардаг хэв маяг энэ.

### State + функцүүд → value

```jsx
// AuthContext.jsx
import { createContext, useContext, useState } from "react";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);

  function login(name) {
    setUser({ name });
  }

  function logout() {
    setUser(null);
  }

  return <AuthContext value={{ user, login, logout }}>{children}</AuthContext>;
}
```

- `value` нь объект: state (`user`) ба түүнийг өөрчлөх **утга учиртай**
  үйлдлүүд. Consumer-ууд `setUser`-ийг огт мэдэхгүй — зөвхөн `login`,
  `logout`-ийг. Дотоод бүтцийг хожим өөрчилсөн ч тэд хөндөгдөхгүй.
- `children`: `AuthProvider` доторх бүх апп-ыг composition-оор хүлээж
  авна (3-р хичээл).
- `AuthContext` өөрөө export хийгдэхгүй — гаднаас зөвхөн provider ба hook-оор
  хандана.

### Custom hook: `useAuth`

```jsx
export function useAuth() {
  const context = useContext(AuthContext);
  if (context === null) {
    throw new Error("useAuth-ийг AuthProvider дотор ашиглана уу");
  }
  return context;
}
```

Энэ жижиг hook хоёр ашигтай:

- Consumer бүр `useContext`, `AuthContext` хоёрыг импортлохгүй — ганцхан
  `const { user, logout } = useAuth();`.
- Анхдагч утга `null` тул provider-ээ мартвал `Cannot read properties of
  null` гэсэн ойлгомжгүй алдааны оронд юу буруу болсныг шууд хэлнэ.

Модул 6-ийн custom hook-ийн санаа: hook дотор өөр hook (`useContext`)
дуудаж болно.

### Ашиглах

```jsx
// App.jsx
export default function App() {
  return (
    <AuthProvider>
      <Navbar />
      <Dashboard />
    </AuthProvider>
  );
}

// Navbar.jsx
export default function Navbar() {
  const { user, logout } = useAuth();
  return user ? <button onClick={logout}>Гарах ({user.name})</button> : <span>Зочин</span>;
}
```

`Navbar`, `Dashboard` хоёр нэг `user`-ийг хуваалцана: нэгд нь нэвтрэхэд
нөгөө нь шууд шинэчлэгдэнэ. State provider-т «дээш өргөгдсөн», харин
props-оор биш, context-оор хүрнэ.

```jsx
export default function App() {
  const { user } = useAuth();
  return (
    <AuthProvider>
      <p>{user?.name}</p>
    </AuthProvider>
  );
}
```

```quiz
Дээрх `App`-д юу болох вэ?
- [ ] `user`-ийн нэр харагдана
- [x] `useAuth` нь `AuthProvider`-ээс **дээр** дуудагдсан тул алдаа шиднэ
- [ ] Хоосон `<p>` харагдана
> Context зөвхөн provider-ийн доторх component-д хүрнэ. `<p>`-г тусдаа component болгож provider дотор тавь.
```

### Файлын бүтэц

```text
src/
├── contexts/
│   └── AuthContext.jsx   ← AuthProvider, useAuth
├── components/
│   ├── Navbar.jsx        ← useAuth()
│   └── Dashboard.jsx     ← useAuth()
└── main.jsx              ← <AuthProvider><App /></AuthProvider>
```

Provider-ийг `main.jsx`-д `App`-ыг бүхэлд нь ороож тавих нь түгээмэл.
Vite-ийн ESLint тохиргоо component ба hook-ийг нэг файлаас export хийхэд
`react-refresh/only-export-components` анхааруулга өгдөг: кодоо хадгалахад
хуудас дахин ачаалагдахгүй шинэчлэгддэг Fast Refresh тэр файлд бүрэн
ажиллахгүй гэсэн үг. Тиймээс зарим төсөл `useAuth`-ийг тусдаа файлд
гаргадаг.

### Бодит сангуудад

Ихэнх React сан яг ийм хэв маягтай: `<QueryClientProvider>` +
`useQueryClient()` (TanStack Query), `<BrowserRouter>` + `useNavigate()`
(react-router). Тэдгээрийг provider-ийн гадна дуудахад ч ийм ойлгомжтой
алдаа гардаг.

### Анхаарах зүйл

`value={{ user, login, logout }}` нь render бүрт шинэ объект үүсгэнэ.
`AuthProvider` дахин render хийх бүрт бүх consumer дахин render хийнэ
гэсэн үг. Жижиг апп-д асуудалгүй. Хэрэгтэй бол `useMemo`,
`useCallback`-оор тогтворжуулна (Модул 12).

```quiz
`useAuth` доторх `if (context === null) throw …` шалгалт юунд хэрэгтэй вэ?
- [ ] Хэрэглэгч нэвтрээгүй үед алдаа шидэхэд
- [x] Provider-ээ мартсан программистад юу буруу болсныг шууд хэлэхэд
- [ ] Context-ийг хурдан ажиллуулахад
> Нэвтрээгүй хэрэглэгч бол `user === null` — энэ хэвийн төлөв. Харин `context === null` нь дээр нь provider алга гэсэн үг.
```

### Дүгнэлт

Provider component нь context-ийн state ба үйлдлүүдийг нэг газар нуудаг.
Гадагш `useAuth()` шиг custom hook гаргаж, provider-гүй үед ойлгомжтой
алдаа шид. Consumer-ууд юу хийж болохыг (`login`, `logout`) мэдэх ба яаж
хийгдэхийг мэдэхгүй.
""",
            initial_code=vite(
                AUTH_APP_START,
                extra={"AuthContext.jsx": AUTH_CONTEXT_START},
                locked={"Navbar.jsx": AUTH_NAVBAR, "Dashboard.jsx": AUTH_DASHBOARD},
                css=AUTH_CSS,
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐ · 15 минут

`Navbar`, `Dashboard` хоёр `useAuth()`-аар нэвтрэлтийн мэдээллийг уншдаг
ч одоогоор `useAuth` хуурамч утга буцааж байна. `AuthContext.jsx`-д
`AuthProvider`-ийг гүйцээ: `user` state эхэндээ `null`, `login(name)`
нь `user`-ийг `{ name }` болгоно, `logout()` нь `null` болгоно. `useAuth()`
context-ийг буцааж, `AuthProvider`-ийн гадна дуудвал «AuthProvider» гэсэн
үг орсон алдаа шиднэ. Эцэст нь `App`-ыг `AuthProvider`-оор ороо.
""",
                tests=(
                    test(
                        "Нэрээ оруулж нэвтрэхэд толгой хэсэг ба самбар хоёулаа шинэчлэгдэнэ",
                        """
render(<App />);
await user.type(screen.getByLabelText("Нэр"), "Бат");
await user.click(screen.getByRole("button", { name: "Нэвтрэх" }));
expect(screen.getByRole("banner")).toHaveTextContent("Бат");
expect(screen.getByRole("heading", { name: "Тавтай морил, Бат!" })).toBeInTheDocument();
""",
                    ),
                    test(
                        "«Гарах» дарахад зочин болж, нэвтрэх форм буцаж гарна",
                        """
render(<App />);
await user.type(screen.getByLabelText("Нэр"), "Бат");
await user.click(screen.getByRole("button", { name: "Нэвтрэх" }));
await user.click(screen.getByRole("button", { name: "Гарах" }));
expect(screen.getByRole("banner")).toHaveTextContent("Зочин");
expect(screen.getByLabelText("Нэр")).toBeInTheDocument();
""",
                    ),
                    test(
                        "useAuth нь AuthProvider-ийн user, login, logout-ийг өгнө",
                        """
const { AuthProvider, useAuth } = mod("./AuthContext");
function Probe() {
  const { user, login, logout } = useAuth();
  return (
    <div>
      <p>Хэрэглэгч: {user ? user.name : "байхгүй"}</p>
      <button onClick={() => login("Сараа")}>нэвтрүүлэх</button>
      <button onClick={logout}>гаргах</button>
    </div>
  );
}
render(
  <AuthProvider>
    <Probe />
  </AuthProvider>
);
expect(screen.text()).toContain("Хэрэглэгч: байхгүй");
await user.click(screen.getByRole("button", { name: "нэвтрүүлэх" }));
expect(screen.text()).toContain("Хэрэглэгч: Сараа");
await user.click(screen.getByRole("button", { name: "гаргах" }));
expect(screen.text()).toContain("Хэрэглэгч: байхгүй");
""",
                    ),
                    test(
                        "AuthProvider-ийн гадна дуудахад useAuth ойлгомжтой алдаа шиднэ",
                        """
const { useAuth } = mod("./AuthContext");
class Boundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { message: null };
  }
  static getDerivedStateFromError(error) {
    return { message: error.message };
  }
  render() {
    if (this.state.message !== null) return <p>Алдаа: {this.state.message}</p>;
    return this.props.children;
  }
}
function Probe() {
  const auth = useAuth();
  return <p>Хэрэглэгч: {auth.user ? auth.user.name : "байхгүй"}</p>;
}
render(
  <Boundary>
    <Probe />
  </Boundary>
);
expect(screen.text()).toMatch(/Алдаа:.*AuthProvider/);
""",
                    ),
                ),
                tips="""\
- `AuthProvider` дотор нэг `useState(null)` ба хоёр жижиг функц. Буцаахдаа
  `children`-ийг `<AuthContext value={…}>`-оор ороо — `value` нь `user`,
  `login`, `logout` гурвыг агуулсан объект.
- `useAuth` дотор эхлээд `useContext(AuthContext)`. Утга нь `null` бол
  provider алга гэсэн үг — `throw new Error("…AuthProvider…")`. Эс бөгөөс
  утгаа буцаа.
- «Хэрэглэгч нэвтрээгүй» (`user === null`) ба «provider алга»
  (`context === null`)-г андуурч болохгүй — эхнийх нь хэвийн төлөв.
- `App`-д `<AuthProvider>`-ийг `Navbar`, `main` хоёуланг нь ороохоор тавь —
  аль нэгийг нь гадна үлдээвэл тэр хэсэг алдаа шиднэ.
""",
                solution=solution(
                    App_jsx="""\
import { AuthProvider } from "./AuthContext";
import Dashboard from "./Dashboard";
import Navbar from "./Navbar";

export default function App() {
  return (
    <AuthProvider>
      <Navbar />
      <main>
        <Dashboard />
      </main>
    </AuthProvider>
  );
}
""",
                    AuthContext_jsx=AUTH_CONTEXT_SOLUTION,
                ),
            ),
        ),
        # ------------------------------------------------------------------
        LessonSpec(
            title="useReducer",
            slug="usereducer",
            description="State-ийн бүх шилжилтийг нэг reducer функцэд цуглуулж, action-оор удирдах.",
            duration=1020,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Reducer функц `(state, action) => шинэ state`-ийг бичих
- `useReducer`, `dispatch`, action объектыг ашиглах
- `useState`-ээс `useReducer` руу шилжих, аль нь хэзээ тохирохыг мэдэх

### Яагаад чухал вэ

Даалгаврын жагсаалтыг бодъё: нэмэх, чагтлах, устгах, засах, дууссаныг
цэвэрлэх. Handler бүр дотроо `setTasks(…)`-ийн өөр өөр логиктой бөгөөд
component даяар тарсан. Логик олшрох тусам «state яг яаж өөрчлөгддөг
вэ?» гэдгийг ойлгохын тулд бүх component-ийг нүдлэх болно.

**Reducer** нь бүх шилжилтийг **нэг функцэд** цуглуулна. Component «юу
болсныг» хэлнэ (action), reducer «state яаж өөрчлөгдөхийг» шийднэ.

### Эхлэл: useState-тэй хувилбар

```jsx
function handleAdd(text) {
  setTasks([...tasks, { id: nextId++, text, done: false }]);
}

function handleToggle(id) {
  setTasks(tasks.map((t) => (t.id === id ? { ...t, done: !t.done } : t)));
}

function handleDelete(id) {
  setTasks(tasks.filter((t) => t.id !== id));
}
```

### Алхам 1: state тохируулахын оронд action илгээ

```jsx
function handleAdd(text) {
  dispatch({ type: "added", id: nextId++, text });
}

function handleToggle(id) {
  dispatch({ type: "toggled", id });
}

function handleDelete(id) {
  dispatch({ type: "deleted", id });
}
```

**Action** бол «юу болсон» гэсэн энгийн объект: `type` заавал байна,
бусад талбарт шаардлагатай мэдээллээ хийнэ. Нэрийг «хэрэглэгч юу хийсэн»
гэдгээр өгдөг: `added`, `toggled`, `deleted` (Redux маягаар `ADD_TASK`
гэж бичдэг төсөл ч бий).

### Алхам 2: reducer бич

```jsx
function tasksReducer(tasks, action) {
  switch (action.type) {
    case "added":
      return [...tasks, { id: action.id, text: action.text, done: false }];
    case "toggled":
      return tasks.map((t) => (t.id === action.id ? { ...t, done: !t.done } : t));
    case "deleted":
      return tasks.filter((t) => t.id !== action.id);
    default:
      throw new Error("Үл мэдэгдэх үйлдэл: " + action.type);
  }
}
```

Reducer нь одоогийн state ба action аваад **шинэ** state буцаана. Нэр нь
массивын `reduce`-ээс гаралтай (Модул 0): `reduce` нь
`(хураангуй, элемент) => шинэ хураангуй`, reducer нь
`(state, action) => шинэ state`.

### Алхам 3: component-д холбо

```jsx
import { useReducer } from "react";

const [tasks, dispatch] = useReducer(tasksReducer, initialTasks);
```

`useReducer` нь reducer ба анхны state-ийг аваад одоогийн state болон
`dispatch` функцийг буцаана. `dispatch(action)` дуудахад React reducer-ийг
ажиллуулж, буцаасан утгаар дахин render хийнэ. `setState` шиг шинэ утга
**дараагийн** render-т л харагдана (Модул 3-ын snapshot).

### Reducer-ийн дүрэм

- **Цэвэр (pure) байна.** Ижил оролтод ижил гаралт, гаж нөлөөгүй: дотор
  нь `fetch`, `setTimeout`, `Math.random()`, `Date.now()` бичихгүй. Шинэ
  `id` хэрэгтэй бол action-д хийж ир (`id: nextId++`) — reducer өөрөө
  үүсгэхгүй. StrictMode-д React reducer-ийг хоёр удаа дуудаж үүнийг
  шалгадаг.
- **Immutable.** `tasks.push(…)`, `task.done = true` бичихгүй — шинэ
  массив, шинэ объект буцаана. Эс бөгөөс React өөрчлөлтийг анзаарахгүй.
- **Үргэлж буцаана.** `case` бүр `return`-тэй. Мартвал state `undefined`
  болно.
- **`default`-д алдаа шид.** `type`-ийн үсгийн алдаа (`"toggeld"`) шууд
  илэрнэ.

```jsx
case "added":
  tasks.push({ id: action.id, text: action.text, done: false });
  return tasks;
```

```quiz
Дээрх `case`-ийн алдаа юу вэ?
- [ ] Алдаагүй — шинэ даалгавар нэмэгдэнэ
- [x] Анхны массивыг өөрчилж, ижил массивыг буцаасан тул React шинэчлэлтийг алгасаж магадгүй
- [ ] `push` reducer дотор ажилладаггүй
> React хуучин, шинэ state-ийг `Object.is`-ээр харьцуулдаг. Ижил массив буцвал «өөрчлөгдөөгүй» гэж үзнэ. `[...tasks, шинэ]` буцаа.
```

### Reducer-ийг тусад нь тестлэх

Reducer бол React-гүй энгийн функц. Тиймээс component render хийхгүйгээр
шууд шалгана:

```jsx
const before = [{ id: 1, text: "Ном унших", done: false }];
const after = tasksReducer(before, { type: "toggled", id: 1 });
// after[0].done === true, before[0].done === false хэвээр
```

Модул 13-т ийм тестийг Vitest-ээр бичнэ.

### useState эсвэл useReducer?

| | `useState` | `useReducer` |
|---|---|---|
| Энгийн утга (тоо, текст, boolean) | ✅ Тохиромжтой | Хэт их код |
| Хоорондоо холбоотой олон шинэчлэл | Handler-уудад тархана | ✅ Нэг газар |
| Тестлэх | Component-оор | ✅ Функцээр шууд |
| Алдаа мөшгих | Хаанаас ч өөрчилж болно | ✅ Бүх шилжилт reducer-т |

Хоёулаа ижил боломжтой — логикийг хаана бичих л ялгаатай. Нэг component-д
хоёуланг нь хэрэглэж болно: input-ийн текст `useState`-д, жагсаалт
`useReducer`-т.

### Бодит төсөлд

Redux (Redux Toolkit) бол reducer, action дээр суурилсан хамгийн алдартай
state-ийн сан. `useReducer`-ийг ойлговол Redux-ийн гол санааг аль хэдийн
мэдэж байна гэсэн үг. `useReducer(reducer, initialArg, init)` гэсэн гурав
дахь аргумент нь анхны state-ийг функцээр тооцоолно (жишээ нь
localStorage-оос унших) — модулийн төсөлд хэрэглэнэ.

```quiz
Аль нь reducer дотор бичихэд зөв вэ?
- [ ] `fetch("/api/tasks", { method: "POST" })`
- [ ] `{ id: Date.now(), text: action.text }`
- [x] `[...tasks, { id: action.id, text: action.text, done: false }]`
> Reducer цэвэр байх ёстой: сүлжээний хүсэлт, цаг, санамсаргүй тоо бол гаж нөлөө. `id`-г action-д хийж ир.
```

### Дүгнэлт

`useReducer` нь state-ийн бүх шилжилтийг нэг цэвэр функцэд цуглуулна.
Component `dispatch({ type, … })`-ээр юу болсныг хэлж, reducer шинэ
state-ийг буцаана. Логик олон, хоорондоо холбоотой үед `useReducer`,
энгийн утгад `useState`.
""",
            initial_code=vite(
                TASKS_APP_START,
                extra={"reducer.js": TASKS_REDUCER_START},
                css=TASKS_CSS,
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐ · 18 минут

`App.jsx` аль хэдийн `useReducer`-ээр `added`, `toggled`, `deleted`
action-уудыг илгээдэг ч `reducer.js` доторх `tasksReducer` хоосон —
«Хөтөч» дээр даалгавар чагтлахад «Үл мэдэгдэх үйлдэл» алдаа гарна. Гурван
action-ийг reducer-т бич. Дараа нь дууссан даалгавруудыг хасдаг `cleared`
action нэмж, `App`-д түүнийг илгээх «Дууссаныг цэвэрлэх» товч тавь.
Reducer анхны массив, объектыг өөрчлөхгүй.
""",
                tests=(
                    test(
                        "added нь шинэ даалгаврыг төгсгөлд нь нэмж, анхны массивыг өөрчлөхгүй",
                        """
const { tasksReducer } = mod("./reducer");
const before = [{ id: 1, text: "Ном унших", done: false }];
const after = tasksReducer(before, { type: "added", id: 7, text: "Гүйх" });
expect(after).toEqual([
  { id: 1, text: "Ном унших", done: false },
  { id: 7, text: "Гүйх", done: false },
]);
expect(before).toHaveLength(1);
""",
                    ),
                    test(
                        "toggled ба deleted нь зөвхөн тухайн id-тай даалгаварт нөлөөлнө",
                        """
const { tasksReducer } = mod("./reducer");
const before = [
  { id: 1, text: "А", done: false },
  { id: 2, text: "Б", done: false },
];
const toggled = tasksReducer(before, { type: "toggled", id: 2 });
expect(toggled).toEqual([
  { id: 1, text: "А", done: false },
  { id: 2, text: "Б", done: true },
]);
expect(before[1].done).toBe(false);
expect(tasksReducer(toggled, { type: "toggled", id: 2 })[1].done).toBe(false);
expect(tasksReducer(before, { type: "deleted", id: 1 })).toEqual([{ id: 2, text: "Б", done: false }]);
""",
                    ),
                    test(
                        "cleared нь дууссан даалгавруудыг хасаж, үл мэдэгдэх action-д алдаа шиднэ",
                        """
const { tasksReducer } = mod("./reducer");
const tasks = [
  { id: 1, text: "А", done: true },
  { id: 2, text: "Б", done: false },
  { id: 3, text: "В", done: true },
];
expect(tasksReducer(tasks, { type: "cleared" })).toEqual([{ id: 2, text: "Б", done: false }]);
expect(tasks).toHaveLength(3);
expect(() => tasksReducer(tasks, { type: "renamed" })).toThrow();
""",
                    ),
                    test(
                        "Нэмэх, чагтлах, устгах нь дэлгэц дээр ажиллана",
                        """
render(<App />);
await user.type(screen.getByLabelText("Шинэ даалгавар"), "Гүйлтээр хичээллэх");
await user.click(screen.getByRole("button", { name: "Нэмэх" }));
expect(screen.getByRole("checkbox", { name: "Гүйлтээр хичээллэх" })).not.toBeChecked();
await user.click(screen.getByRole("checkbox", { name: "Дасгал хийх" }));
expect(screen.getByRole("checkbox", { name: "Дасгал хийх" })).toBeChecked();
await user.click(screen.getByRole("button", { name: "React хичээл үзэх устгах" }));
expect(screen.queryByText("React хичээл үзэх")).toBeNull();
expect(screen.getAllByRole("listitem")).toHaveLength(3);
""",
                    ),
                    test(
                        "«Дууссаныг цэвэрлэх» товч дууссан даалгавруудыг хасна",
                        """
render(<App />);
await user.click(screen.getByRole("checkbox", { name: "Дасгал хийх" }));
await user.click(screen.getByRole("button", { name: "Дууссаныг цэвэрлэх" }));
expect(screen.getAllByRole("listitem")).toHaveLength(1);
expect(screen.getByRole("checkbox", { name: "Тест бичих" })).not.toBeChecked();
""",
                    ),
                ),
                tips="""\
- `case "added":` — spread-ээр шинэ массив: хуучин бүх даалгавар + шинэ
  объект. `id`, `text` хоёрыг action-оос ав.
- `toggled` → `map`: таарсан даалгаварт `{ ...task, done: !task.done }`,
  бусдыг хэвээр нь буцаа.
- `deleted`, `cleared` → `filter`. Нэг нь `id`-аар, нөгөө нь `done`-оор
  шүүнэ.
- `case` бүр `return`-тэй байх ёстой. `return`-гүй `case` дараагийн
  `case` руу «унана» эсвэл `undefined` буцаана.
- `push`, `task.done = …` бичвэл тест анхны массив өөрчлөгдсөнийг
  илрүүлнэ.
- Товч: `onClick={() => dispatch({ type: "cleared" })}`.
""",
                solution=solution(App_jsx=TASKS_APP_SOLUTION, reducer_js=TASKS_REDUCER_SOLUTION),
            ),
        ),
        # ------------------------------------------------------------------
        LessonSpec(
            title="Reducer + Context хослуулах",
            slug="reducer-context",
            description="useReducer-ийн state ба dispatch-ийг context-оор апп даяар хуваалцах.",
            duration=1080,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Reducer ба context-ийг хослуулж, апп даяар хуваалцах state удирдах
- State ба `dispatch`-ийг хоёр тусдаа context-оор дамжуулах
- `CartProvider`, `useCart()`, `useCartDispatch()` бүтцийг бичих

### Яагаад чухал вэ

Сагс бол онлайн дэлгүүрийн хамгийн «төвлөрсөн» state: барааны карт
бараа нэмнэ, толгой хэсэг тоог нь харуулна, сагсны хэсэг жагсаалт ба
нийт дүнг харуулж, бараа хасна. Эдгээр component модны өөр өөр мөчир дээр
байрладаг.

Өмнөх хичээлүүдэд хоёр хэрэгсэл сурсан: **reducer** бүх шилжилтийг нэг
газар цуглуулдаг, **context** утгыг props-гүйгээр гүн рүү хүргэдэг.
Хоёуланг нь хослуулбал жижиг «state-ийн сан» бүтээнэ — Redux-ийн санаа
яг ийм.

### Бүтэц

```text
CartProvider   ← useReducer(cartReducer, [])
 ├─ CartContext          → items
 └─ CartDispatchContext  → dispatch
     ├── CartBadge    ← useCart()           тоо харуулна
     ├── ProductCard  ← useCartDispatch()   бараа нэмнэ
     └── Cart         ← хоёуланг нь         жагсаалт, хасах
```

### Алхам 1: reducer

```jsx
export function cartReducer(items, action) {
  switch (action.type) {
    case "added": {
      const exists = items.some((item) => item.id === action.product.id);
      if (exists) {
        return items.map((item) =>
          item.id === action.product.id ? { ...item, qty: item.qty + 1 } : item,
        );
      }
      return [...items, { ...action.product, qty: 1 }];
    }
    case "removed":
      return items.filter((item) => item.id !== action.id);
    default:
      throw new Error("Үл мэдэгдэх үйлдэл: " + action.type);
  }
}
```

`case "added": { … }` дахь угалзан хаалт нь `const`-ийн хүрээг тухайн
`case` дотор хязгаарлана — эс бөгөөс өөр `case`-д ижил нэртэй хувьсагч
зарлахад алдаа гарна.

### Алхам 2: provider

```jsx
const CartContext = createContext(null);
const CartDispatchContext = createContext(null);

export function CartProvider({ children }) {
  const [items, dispatch] = useReducer(cartReducer, []);
  return (
    <CartContext value={items}>
      <CartDispatchContext value={dispatch}>{children}</CartDispatchContext>
    </CartContext>
  );
}
```

### Алхам 3: hook-ууд

```jsx
export function useCart() {
  return useContext(CartContext);
}

export function useCartDispatch() {
  return useContext(CartDispatchContext);
}
```

Өмнөх хичээлийнх шиг `null` шалгаж, provider-гүй үед ойлгомжтой алдаа
шидэхийг бүү мартаарай.

### Яагаад хоёр context вэ?

`dispatch` функц **хэзээ ч өөрчлөгддөггүй** — React түүнийг render
бүрт ижил байлгадаг. Иймд зөвхөн `dispatch` хэрэгтэй component (жишээ нь
«Сагсанд нэмэх» товч) сагс өөрчлөгдөх бүрт context-ийн улмаас дахин
render хийхгүй. Хэрэв нэг context-д `{ items, dispatch }` хийвэл бүх
consumer `items` өөрчлөгдөх бүрт дахин render хийнэ. Жижиг апп-д ялгаа
анзаарагдахгүй ч энэ бол React-ийн баримт бичгийн санал болгодог хэв
маяг.

### Хэрэглэх

```jsx
function ProductCard({ product }) {
  const dispatch = useCartDispatch();
  return (
    <button onClick={() => dispatch({ type: "added", product })}>Сагсанд нэмэх</button>
  );
}

function CartBadge() {
  const items = useCart();
  const count = items.reduce((sum, item) => sum + item.qty, 0);
  return <span>🛒 {count}</span>;
}
```

Нийт ширхэг, нийт дүн зэрэг утгыг consumer дотор `items`-ээс
**тооцоолно** — reducer-ийн state-д тусад нь хадгалахгүй (2-р хичээл).
`App` зөвхөн `<CartProvider>`-оор ороож, props дамжуулахгүй.

```quiz
`cartReducer([{ id: 1, name: "Алим", qty: 2 }], { type: "added", product: { id: 1, name: "Алим" } })` юу буцаах вэ?
- [ ] `[{ id: 1, name: "Алим", qty: 2 }, { id: 1, name: "Алим", qty: 1 }]`
- [x] `[{ id: 1, name: "Алим", qty: 3 }]`
- [ ] `[{ id: 1, name: "Алим", qty: 1 }]`
> Бараа сагсанд байгаа тул шинэ мөр нэмэхгүй, `qty`-г нь нэмэгдүүлнэ.
```

### dispatch эсвэл функцүүд?

Зарим баг `dispatch`-ийн оронд `addToCart(product)`, `removeFromCart(id)`
гэсэн функцүүдийг context-оор гаргадаг — `AuthProvider`-ийн `login`,
`logout` шиг. Энэ нь action-ийн бүтцийг нууна. `dispatch` нь API-г жижиг
байлгадаг. Аль аль нь зөв — төсөл дотроо нэгийг нь сонгоод тууштай
хэрэглэ.

### Бодит төсөлд

Энэ хэв маяг дунд хэмжээний апп-д хангалттай. Маш том апп-д Redux
Toolkit, Zustand зэрэг сан хэрэглэдэг бөгөөд тэдгээрийн санаа яг
reducer + context. Харин серверээс ирэх өгөгдлийг (барааны жагсаалт)
context-д биш, TanStack Query-д хадгална (Модул 9).

```quiz
`dispatch`-ийг яагаад тусдаа context-оор дамжуулдаг вэ?
- [ ] `dispatch` render бүрт өөрчлөгддөг тул
- [x] `dispatch` өөрчлөгддөггүй тул зөвхөн түүнийг уншдаг component сагс өөрчлөгдөхөд дахин render хийхгүй
- [ ] Context-д функц хийж болдоггүй
> Зөвхөн үйлдэл илгээдэг component-ууд state-ийн өөрчлөлтөөс хамааралгүй болно.
```

### Дүгнэлт

`useReducer`-ийг provider component-д байрлуулж, state-ийг нэг context-оор,
`dispatch`-ийг нөгөөгөөр дамжуулна. `useCart()`, `useCartDispatch()` гэсэн
hook-ууд гаднаас хэрэглэхийг хялбар болгоно. Ингэснээр гүн дэх ямар ч
component state-ийг уншиж, action илгээж чадна.
""",
            initial_code=vite(
                CART_APP_START,
                extra={
                    "CartContext.jsx": CART_CONTEXT_START,
                    "ProductCard.jsx": CART_PRODUCT_CARD_START,
                    "CartBadge.jsx": CART_BADGE_START,
                },
                locked={"Cart.jsx": CART_VIEW, "products.js": CART_PRODUCTS},
                css=CART_CSS,
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐⭐ · 20 минут

«Ногоон сагс»-ын сагсыг reducer + context-оор бүтээ. `CartContext.jsx`-д
`cartReducer`-ийн `added`, `removed` action-уудыг бичиж, `CartProvider`
нь `useReducer`-ийн `items`-ийг `CartContext`-оор, `dispatch`-ийг
`CartDispatchContext`-оор дамжуулна. `useCart()` бараануудыг,
`useCartDispatch()` нь `dispatch`-ийг буцаана. Дараа нь `App`-ыг
`CartProvider`-оор ороож, `ProductCard`-ийн товчоор
`{ type: "added", product }` илгээ, `CartBadge`-д нийт ширхгийг харуул.
`Cart.jsx` бэлэн — хэрхэн хэрэглэснийг нь хараарай.
""",
                tests=(
                    test(
                        "cartReducer: added шинэ барааг qty 1-тэй нэмж, давтвал qty-г нэмэгдүүлнэ",
                        """
const { cartReducer } = mod("./CartContext");
const apple = { id: 1, name: "Алим", emoji: "🍎", price: 2800 };
const once = cartReducer([], { type: "added", product: apple });
expect(once).toEqual([{ ...apple, qty: 1 }]);
const twice = cartReducer(once, { type: "added", product: apple });
expect(twice).toEqual([{ ...apple, qty: 2 }]);
expect(once[0].qty).toBe(1);
""",
                    ),
                    test(
                        "cartReducer: removed барааг сагснаас хасна",
                        """
const { cartReducer } = mod("./CartContext");
const items = [
  { id: 1, name: "Алим", price: 2800, qty: 2 },
  { id: 2, name: "Сүү", price: 3200, qty: 1 },
];
expect(cartReducer(items, { type: "removed", id: 1 })).toEqual([
  { id: 2, name: "Сүү", price: 3200, qty: 1 },
]);
expect(items).toHaveLength(2);
""",
                    ),
                    test(
                        "useCart, useCartDispatch нь CartProvider доторх нэг сагсыг хуваалцана",
                        """
const { CartProvider, useCart, useCartDispatch } = mod("./CartContext");
function AddButton() {
  const dispatch = useCartDispatch();
  const cheese = { id: 9, name: "Бяслаг", price: 9000 };
  return <button onClick={() => dispatch({ type: "added", product: cheese })}>нэм</button>;
}
function Count() {
  const items = useCart();
  return <p>Мөр: {items.length}</p>;
}
render(
  <CartProvider>
    <AddButton />
    <Count />
  </CartProvider>
);
expect(screen.text()).toContain("Мөр: 0");
await user.click(screen.getByRole("button", { name: "нэм" }));
expect(screen.text()).toContain("Мөр: 1");
""",
                    ),
                    test(
                        "«Сагсанд нэмэх» дарахад толгойн тоо, сагсны жагсаалт, нийт дүн шинэчлэгдэнэ",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: "Сагсанд нэмэх: Алим" }));
await user.click(screen.getByRole("button", { name: "Сагсанд нэмэх: Алим" }));
await user.click(screen.getByRole("button", { name: "Сагсанд нэмэх: Сүү" }));
expect(screen.getByRole("banner")).toHaveTextContent("Сагс: 3");
const cart = screen.getByRole("complementary");
expect(within(cart).getAllByRole("listitem")).toHaveLength(2);
expect(cart).toHaveTextContent("Алим × 2");
expect(cart).toHaveTextContent("Нийт: 8800₮");
""",
                    ),
                    test(
                        "Сагснаас хасахад толгойн тоо ба нийт дүн шинэчлэгдэнэ",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: "Сагсанд нэмэх: Талх" }));
await user.click(screen.getByRole("button", { name: "Сагсанд нэмэх: Сүү" }));
await user.click(screen.getByRole("button", { name: "Талх хасах" }));
expect(screen.getByRole("banner")).toHaveTextContent("Сагс: 1");
const cart = screen.getByRole("complementary");
expect(cart).not.toHaveTextContent("Талх");
expect(cart).toHaveTextContent("Нийт: 3200₮");
""",
                    ),
                ),
                tips="""\
- `added`: эхлээд `some`-оор бараа сагсанд байгаа эсэхийг шалга. Байвал
  `map`-аар тэр мөрийн `qty`-г нэм, байхгүй бол `[...items, { ...action.product, qty: 1 }]`.
- `case` дотор `const` зарлах бол `case "added": { … }` гэж угалзан хаалтаар ороо.
- `CartProvider`: `useReducer(cartReducer, [])`, дараа нь хоёр provider-ийг
  нэг нэгнийх нь дотор хийж, хамгийн дотор нь `children`.
- `useCart`, `useCartDispatch` — тус бүр өөрийн context-ийг `useContext`-оор
  уншина.
- `ProductCard`, `CartBadge` хоёрт hook-уудыг `./CartContext`-оос импортло.
  Ширхэг бол мөрийн тоо биш, `qty`-уудын нийлбэр.
- `App`-д `CartProvider` нь `header`, `main` хоёуланг нь ороох ёстой.
""",
                solution=solution(
                    App_jsx=CART_APP_SOLUTION,
                    CartContext_jsx=CART_CONTEXT_SOLUTION,
                    ProductCard_jsx=CART_PRODUCT_CARD_SOLUTION,
                    CartBadge_jsx=CART_BADGE_SOLUTION,
                ),
            ),
        ),
        # ------------------------------------------------------------------
        LessonSpec(
            title="Төсөл: Theme ба хэрэглэгчийн тохиргоо",
            slug="tusul-tohirgoo",
            description="SettingsContext, reducer, localStorage-оор харагдац ба хэрэглэгчийн тохиргооны апп бүтээх.",
            duration=2400,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Модулийн санаануудыг нэг апп-д нэгтгэх: reducer + context + provider +
  custom hook
- Нэг тохиргооны state-ийг гурван өөр component-оос уншиж, өөрчлөх
- `useReducer`-ийн гурав дахь аргументаар localStorage-оос анхны state
  сэргээх

### Яагаад чухал вэ

Бараг бүх апп-д «Тохиргоо» хэсэг бий: харанхуй горим, үсгийн хэмжээ,
хэрэглэгчийн нэр. Эдгээр нь апп-ын өөр өөр хэсэгт хэрэгтэй бөгөөд
хэрэглэгч дахин ороход хадгалагдсан байх ёстой. Энэ бол Context +
`useReducer`-ийн сонгодог хэрэглээ.

### Юу бүтээх вэ

- **Харагдац** (`ThemeSettings`): «Харанхуй горим» checkbox, «Үсгийн
  хэмжээ» select (Жижиг / Дунд / Том).
- **Хэрэглэгч** (`UserSettings`): «Нэр» талбар, «Анхны тохиргоо» товч.
- **Урьдчилан харах** (`Preview`): тохиргоо бүрийг шууд тусгасан карт.
- Тохиргоо хадгалагдаж, апп-ыг дахин нээхэд сэргэнэ.

### Component-уудын мод

```text
App
└── SettingsProvider   ← SettingsContext: useReducer + localStorage
    ├── ThemeSettings  ← useSettings(): theme, fontSize
    ├── UserSettings   ← useSettings(): name, reset
    └── Preview        ← useSettings(): бүгдийг харуулна
```

Гурван component бие биеийнхээ тухай мэдэхгүй, хоорондоо props
дамжуулахгүй — бүгд `useSettings()`-ээр **нэг эх сурвалжаас** уншина.

### State ба action-ууд

```jsx
export const initialSettings = { theme: "light", fontSize: "medium", name: "" };
```

| Action | Юу хийх |
|---|---|
| `{ type: "themeToggled" }` | `theme`: `"light"` ↔ `"dark"` |
| `{ type: "fontSizeChanged", fontSize }` | `"small"`, `"medium"`, `"large"` |
| `{ type: "nameChanged", name }` | Нэрийг солино |
| `{ type: "reset" }` | `initialSettings` руу буцна |
| бусад | алдаа шиднэ |

### `SettingsContext.jsx`-ийн API

| Export | Юу вэ |
|---|---|
| `initialSettings` | Анхны тохиргоо (бэлэн) |
| `settingsReducer(settings, action)` | Дээрх action-ууд, анхны объектыг өөрчлөхгүй |
| `SettingsProvider` | `useReducer` + localStorage; `{ settings, dispatch }`-ийг context-оор |
| `useSettings()` | `{ settings, dispatch }`; provider-гүй бол алдаа шиднэ |

Энэ удаа нэг context-д `{ settings, dispatch }`-ийг хамт хийнэ —
тохиргоо ховор өөрчлөгддөг тул хоёр context болгох шаардлагагүй.

### Урьдчилан харах хэсгийн шаардлага

- Гадна элемент нь `<section aria-label="Урьдчилан харах">`. `className`
  нь `preview`, theme (`light` / `dark`), үсгийн хэмжээ (`small` /
  `medium` / `large`) гурвыг агуулна: `"preview dark large"`. `styles.css`
  эдгээр классаар өнгө, хэмжээг аль хэдийн тохируулсан.
- Гарчиг: «Сайн уу, Бат!», нэр хоосон бол «Сайн уу, Зочин!».
- «Горим: Цайвар» эсвэл «Горим: Харанхуй»; «Үсэг: Жижиг / Дунд / Том».

### localStorage-д хадгалах

Хоёр хэсэгтэй:

1. **Хадгалах** — `settings` өөрчлөгдөх бүрт effect-ээр бичнэ (Модул 5):
   `localStorage.setItem("settings", JSON.stringify(settings))`.
2. **Сэргээх** — `useReducer(settingsReducer, initialSettings, loadSettings)`.
   React `loadSettings(initialSettings)`-ийг зөвхөн **эхний** render-т нэг
   удаа дуудна — `useState(() => …)`-ийн залхуу анхны утгатай адил
   (Модул 6).

```jsx
function loadSettings(initial) {
  try {
    const saved = JSON.parse(localStorage.getItem("settings"));
    return saved ? { ...initial, ...saved } : initial;
  } catch {
    return initial;
  }
}
```

`{ ...initial, ...saved }` — хуучин хувилбарт хадгалсан тохиргоонд шинэ
талбар дутуу байсан ч анхдагч утга нь орно. `try`/`catch` нь эвдэрсэн
JSON-оос хамгаална.

### Алхамууд

1. `settingsReducer`-ийг бичээд эхний тестээр шалга.
2. `SettingsProvider`, `useSettings`-ийг бичиж, `App`-ыг ороо.
3. `Preview`-ийг `useSettings()`-ээс уншдаг болго.
4. `ThemeSettings`, `UserSettings`-ийн талбаруудыг **controlled** болгож
   (`checked`, `value` нь `settings`-ээс), өөрчлөлт бүрт `dispatch` хий.
   Uncontrolled `defaultValue`-г устга — эс бөгөөс «Анхны тохиргоо» дарахад
   талбар хуучин утгаа харуулсаар байна (2-р хичээл).
5. localStorage-д хадгалж, сэргээ. «Хөтөч»-ийн «Дахин ачаалах»-аар шалга.

```quiz
`useReducer(settingsReducer, initialSettings, loadSettings)` бичсэн бол `loadSettings` хэдэн удаа дуудагдах вэ?
- [ ] Render бүрт
- [x] Зөвхөн эхний render-т нэг удаа
- [ ] `dispatch` дуудах бүрт
> Гурав дахь аргумент нь залхуу анхны утга: localStorage-ийг render бүрт дэмий уншихгүй.
```

```quiz
Checkbox-т `checked={settings.theme === "dark"}` бичээд `onChange` бичихээ мартвал юу болох вэ?
- [ ] Checkbox хэвийн ажиллана
- [x] Дарахад өөрчлөгдөхгүй, React console-д анхааруулга гаргана
- [ ] Апп унана
> Controlled талбарын утгыг зөвхөн state өөрчилнө. `onChange`-гүй бол state хэзээ ч өөрчлөгдөхгүй тул талбар «гацна».
```

### Нэмэлт сорилт

Тест шаардахгүй ч оролдоод үзээрэй:

- Theme-ийг зөвхөн `Preview` биш, бүх хуудсанд хэрэглэ — жишээ нь
  provider доторх wrapper `div`-д класс өгөх.
- «Өнгө» (accent) тохиргоо нэмж, reducer-т шинэ action бич.
- `SettingsContext`-ийг state ба `dispatch` гэсэн хоёр context болго
  (өмнөх хичээл).

### Дүгнэлт

Тохиргооны апп бол модулийн бүх санааны нэгдэл: нэг үнэн эх сурвалж
(reducer), түүнийг гүн рүү хүргэх context, логикийг нуусан provider,
хэрэглэхэд хялбар `useSettings()` hook. Гурван component props дамжуулалгүй
нэг state-ийг хуваалцаж, localStorage нь түүнийг хуудас хооронд хадгална.
""",
            initial_code=vite(
                SETTINGS_APP_START,
                extra={
                    "SettingsContext.jsx": SETTINGS_CONTEXT_START,
                    "ThemeSettings.jsx": SETTINGS_THEME_START,
                    "UserSettings.jsx": SETTINGS_USER_START,
                    "Preview.jsx": SETTINGS_PREVIEW_START,
                },
                css=SETTINGS_CSS,
                css_locked=False,
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐⭐ · 40 минут

«Заавар» дахь шаардлага, API-г дагаж тохиргооны апп-ыг бүтээ.
`SettingsContext.jsx`-д reducer, provider, hook-ийг бичээд `ThemeSettings`,
`UserSettings`, `Preview` гурвыг `useSettings()`-ээр холбо. Тохиргоо
localStorage-д хадгалагдаж, апп-ыг дахин нээхэд сэргэх ёстой. `styles.css`
бэлэн — хүсвэл өөрийнхөөрөө чимэглээрэй.
""",
                tests=(
                    test(
                        "settingsReducer нь тохиргоог өөрчилж, reset-ээр анхны утгад буцаана",
                        """
const { settingsReducer, initialSettings } = mod("./SettingsContext");
let state = settingsReducer(initialSettings, { type: "themeToggled" });
expect(state.theme).toBe("dark");
state = settingsReducer(state, { type: "fontSizeChanged", fontSize: "large" });
state = settingsReducer(state, { type: "nameChanged", name: "Бат" });
expect(state).toEqual({ theme: "dark", fontSize: "large", name: "Бат" });
expect(initialSettings).toEqual({ theme: "light", fontSize: "medium", name: "" });
expect(settingsReducer(state, { type: "themeToggled" }).theme).toBe("light");
expect(settingsReducer(state, { type: "reset" })).toEqual(initialSettings);
expect(() => settingsReducer(state, { type: "unknown" })).toThrow();
""",
                    ),
                    test(
                        "«Харанхуй горим» чагтлахад урьдчилан харах хэсэг харанхуй болно",
                        """
render(<App />);
const preview = () => screen.getByRole("region", { name: "Урьдчилан харах" });
expect(preview()).toHaveClass("light");
await user.click(screen.getByRole("checkbox", { name: "Харанхуй горим" }));
expect(preview()).toHaveClass("dark");
expect(preview()).not.toHaveClass("light");
expect(preview()).toHaveTextContent("Горим: Харанхуй");
expect(screen.getByRole("checkbox", { name: "Харанхуй горим" })).toBeChecked();
""",
                    ),
                    test(
                        "Нэр ба үсгийн хэмжээ урьдчилан харах хэсэгт шууд харагдана",
                        """
render(<App />);
await user.type(screen.getByLabelText("Нэр"), "Бат");
await user.selectOptions(screen.getByLabelText("Үсгийн хэмжээ"), "large");
const preview = screen.getByRole("region", { name: "Урьдчилан харах" });
expect(preview).toHaveTextContent("Сайн уу, Бат!");
expect(preview).toHaveTextContent("Үсэг: Том");
expect(preview).toHaveClass("large");
""",
                    ),
                    test(
                        "«Анхны тохиргоо» бүх тохиргоо ба талбаруудыг буцаана",
                        """
render(<App />);
await user.click(screen.getByRole("checkbox", { name: "Харанхуй горим" }));
await user.type(screen.getByLabelText("Нэр"), "Бат");
await user.selectOptions(screen.getByLabelText("Үсгийн хэмжээ"), "small");
await user.click(screen.getByRole("button", { name: "Анхны тохиргоо" }));
const preview = screen.getByRole("region", { name: "Урьдчилан харах" });
expect(preview).toHaveTextContent("Сайн уу, Зочин!");
expect(preview).toHaveClass("light");
expect(preview).toHaveClass("medium");
expect(screen.getByRole("checkbox", { name: "Харанхуй горим" })).not.toBeChecked();
expect(screen.getByLabelText("Нэр")).toHaveValue("");
expect(screen.getByLabelText("Үсгийн хэмжээ")).toHaveValue("medium");
""",
                    ),
                    test(
                        "Тохиргоо хадгалагдаж, апп-ыг дахин нээхэд сэргэнэ",
                        """
const first = render(<App />);
await user.click(screen.getByRole("checkbox", { name: "Харанхуй горим" }));
await user.type(screen.getByLabelText("Нэр"), "Сараа");
first.unmount();
render(<App />);
const preview = screen.getByRole("region", { name: "Урьдчилан харах" });
expect(preview).toHaveClass("dark");
expect(preview).toHaveTextContent("Сайн уу, Сараа!");
expect(screen.getByLabelText("Нэр")).toHaveValue("Сараа");
""",
                    ),
                ),
                tips="""\
- Эхлээд reducer: `case` бүр `{ ...settings, … }` шинэ объект буцаана,
  `reset` нь `initialSettings`-ийг. Эхний тест зөвхөн reducer-ийг шалгадаг
  тул эндээс эхэл.
- `SettingsProvider`: `useReducer`-ийн 3 дахь аргумент нь `loadSettings`.
  `value`-д `{ settings, dispatch }` объектыг өг.
- Component бүрт `const { settings, dispatch } = useSettings();`.
- Checkbox: `checked` нь `settings.theme === "dark"`, `onChange` нь
  `themeToggled` илгээнэ. Select: `value={settings.fontSize}`,
  `onChange` дотор `event.target.value`-г action-д хий. `defaultValue`-г устга.
- Preview-ийн класс: template string `` `preview ${…} ${…}` ``. Үсгийн
  хэмжээний монгол нэрийг `{ small: "Жижиг", … }` объектоос ав.
- Сэргэхгүй байвал: effect-ийн dependency-д `settings` байгаа эсэх,
  `loadSettings` хадгалсан утгыг буцааж байгаа эсэхийг шалга. Тест бүр
  цэвэр localStorage-оос эхэлдэг.
""",
                solution=solution(
                    App_jsx=SETTINGS_APP_SOLUTION,
                    SettingsContext_jsx=SETTINGS_CONTEXT_SOLUTION,
                    ThemeSettings_jsx=SETTINGS_THEME_SOLUTION,
                    UserSettings_jsx=SETTINGS_USER_SOLUTION,
                    Preview_jsx=SETTINGS_PREVIEW_SOLUTION,
                ),
            ),
        ),
    ],
)
