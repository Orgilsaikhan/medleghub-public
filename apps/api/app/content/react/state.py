"""Модул 3 — State ба харилцан үйлдэл.

Үйл явдал (event) ба handler-ээс эхэлж, `useState`-ээр component-д санах
ой өгнө: state бол render бүрийн агшин зураг, функцээр шинэчлэх, boolean,
объект, массив state-ийг immutable шинэчлэх, тооцоолж болох утгыг state-д
хадгалахгүй байх. Төгсгөлд нь «Ногоон сагс»-ын сагсыг бүтээнэ. Форм
(Модул 4), effect (Модул 5) хараахан ороогүй — бүх харилцан үйлдэл товчоор.
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
  padding: 6px 14px;
  border: 1px solid #b9c7b1;
  border-radius: 8px;
  background: #fff;
  font: inherit;
  cursor: pointer;
}

button:hover:not(:disabled) {
  background: #eef5ea;
}

button:disabled {
  color: #9aa596;
  cursor: not-allowed;
}

.grid {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
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
  margin: 4px 0 12px;
  color: #55624f;
}

.row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
}
"""

# --- Төсөл: Сагс --------------------------------------------------------------

CART_PRODUCTS = """\
export const products = [
  { id: 1, name: "Банана", price: 3500, category: "Жимс", emoji: "🍌" },
  { id: 2, name: "Алим", price: 2800, category: "Жимс", emoji: "🍎" },
  { id: 3, name: "Лууван", price: 1900, category: "Ногоо", emoji: "🥕" },
  { id: 4, name: "Сүү", price: 3200, category: "Сүүн бүтээгдэхүүн", emoji: "🥛" },
  { id: 5, name: "Бяслаг", price: 12500, category: "Сүүн бүтээгдэхүүн", emoji: "🧀" },
  { id: 6, name: "Талх", price: 2500, category: "Гурил", emoji: "🍞" },
];
"""

CART_FORMAT = """\
export function formatPrice(price) {
  return price.toLocaleString("en-US") + "₮";
}
"""

CART_CSS = """\
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: system-ui, sans-serif;
  background: #f4f7f2;
  color: #1f2a1c;
}

button {
  font: inherit;
  cursor: pointer;
}

.page {
  max-width: 1040px;
  margin: 0 auto;
  padding: 0 16px 24px;
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

.cart-count {
  margin: 0;
  font-weight: 600;
}

.layout {
  display: grid;
  grid-template-columns: 1fr;
  gap: 24px;
  margin-top: 20px;
}

@media (min-width: 720px) {
  .layout {
    grid-template-columns: 1fr 320px;
    align-items: start;
  }
}

.products h2,
.cart h2 {
  margin: 0 0 12px;
  font-size: 1.2rem;
}

.grid {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 12px;
}

.card {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 14px;
  border: 1px solid #dfe8da;
  border-radius: 14px;
  background: #fff;
}

.card-emoji {
  font-size: 2.2rem;
}

.card h3 {
  margin: 4px 0 0;
  font-size: 1rem;
}

.price {
  margin: 0 0 8px;
  font-weight: 700;
  color: #2f6b1f;
}

.add {
  margin-top: auto;
  padding: 8px;
  border: 0;
  border-radius: 8px;
  background: #2f6b1f;
  color: #fff;
}

.add:hover {
  background: #255716;
}

.cart {
  padding: 16px;
  border: 1px solid #dfe8da;
  border-radius: 14px;
  background: #fff;
}

.empty {
  margin: 8px 0;
  color: #6b7a65;
}

.cart-list {
  margin: 0;
  padding: 0;
  list-style: none;
}

.cart-item {
  display: grid;
  grid-template-columns: 1fr auto;
  align-items: center;
  gap: 6px 8px;
  padding: 10px 0;
  border-bottom: 1px solid #eef2eb;
}

.qty {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.qty button,
.remove {
  width: 30px;
  height: 30px;
  padding: 0;
  border: 1px solid #cfd8ca;
  border-radius: 8px;
  background: #fff;
}

.line-total {
  font-weight: 600;
}

.remove {
  justify-self: end;
  color: #a3261f;
}

.total {
  margin: 16px 0 12px;
  font-size: 1.2rem;
  font-weight: 700;
}

.clear {
  width: 100%;
  padding: 8px;
  border: 1px solid #e3b4b0;
  border-radius: 8px;
  background: #fff;
  color: #a3261f;
}
"""

CART_APP_START = """\
import { useState } from "react";
import { addToCart, cartCount, cartTotal, changeQuantity, removeFromCart } from "./cart";
import Cart from "./components/Cart";
import Header from "./components/Header";
import ProductList from "./components/ProductList";
import { products } from "./products";

export default function App() {
  // Алхам 2: энэ мөрийн оронд cart state үүсгэ (эхэндээ хоосон массив).
  const cart = [];

  // Алхам 2: handler бүр cart.js-ийн функцээр ШИНЭ сагс тооцоод state-д хийнэ.
  function handleAdd(product) {}
  function handleIncrease(id) {}
  function handleDecrease(id) {}
  function handleRemove(id) {}
  function handleClear() {}

  // Алхам 2: уламжлагдсан утгууд — state биш, cart-аас тооцоол.
  const count = 0;
  const total = 0;

  return (
    <div className="page">
      <Header count={count} />
      <main className="layout">
        <ProductList products={products} onAdd={handleAdd} />
        <Cart
          items={cart}
          total={total}
          onIncrease={handleIncrease}
          onDecrease={handleDecrease}
          onRemove={handleRemove}
          onClear={handleClear}
        />
      </main>
    </div>
  );
}
"""

CART_LOGIC_START = """\
// Сагсны бүх логик — React-гүй цэвэр функцууд. Функц бүр ХУУЧИН сагсыг
// өөрчлөхгүйгээр ШИНЭ массив (эсвэл тоо) буцаана.
//
// Сагсны мөр: { id, name, price, emoji, category, quantity }

// Алхам 1а: бараа сагсанд байхгүй бол quantity: 1-тэйгээр төгсгөлд нэм,
//           байгаа бол тэр мөрийн quantity-г 1-ээр нэмэгдүүл.
export function addToCart(cart, product) {
  return cart;
}

// Алхам 1б: id-тай мөрийн quantity-г delta-аар (+1 эсвэл -1) өөрчил.
//           0 болсон мөрийг сагснаас хас.
export function changeQuantity(cart, id, delta) {
  return cart;
}

// Алхам 1в: id-тай мөрийг хас.
export function removeFromCart(cart, id) {
  return cart;
}

// Алхам 1г: нийт дүн — price × quantity-ийн нийлбэр.
export function cartTotal(cart) {
  return 0;
}

// Алхам 1д: нийт ширхэг — quantity-ийн нийлбэр.
export function cartCount(cart) {
  return 0;
}
"""

CART_HEADER = """\
// Бэлэн — өөрчлөх шаардлагагүй.
export default function Header({ count }) {
  return (
    <header className="header">
      <h1>🥬 Ногоон сагс</h1>
      <p className="cart-count">🛒 Сагсанд: {count} ширхэг</p>
    </header>
  );
}
"""

CART_PRODUCT_LIST_START = """\
import { formatPrice } from "../format";

export default function ProductList({ products, onAdd }) {
  return (
    <section className="products" aria-label="Бараанууд">
      <h2>Бараанууд</h2>
      <ul className="grid">
        {products.map((product) => (
          <li key={product.id} className="card">
            <div className="card-emoji">{product.emoji}</div>
            <h3>{product.name}</h3>
            <p className="price">{formatPrice(product.price)}</p>
            {/* Алхам 3: дарахад onAdd(product)-ийг дууд */}
            <button type="button" className="add">
              Сагсанд нэмэх
            </button>
          </li>
        ))}
      </ul>
    </section>
  );
}
"""

CART_ITEM_START = """\
import { formatPrice } from "../format";

// Алхам 4: гурван товчинд onDecrease(item.id), onIncrease(item.id),
//          onRemove(item.id)-ийг холбо.
export default function CartItem({ item, onIncrease, onDecrease, onRemove }) {
  return (
    <li className="cart-item">
      <span>
        {item.emoji} {item.name}
      </span>
      <button type="button" className="remove" aria-label={`${item.name}: устгах`}>
        ✕
      </button>
      <div className="qty">
        <button type="button" aria-label={`${item.name}: нэгээр хасах`}>
          −
        </button>
        <span>{item.quantity}</span>
        <button type="button" aria-label={`${item.name}: нэгээр нэмэх`}>
          +
        </button>
      </div>
      <span className="line-total">{formatPrice(item.price * item.quantity)}</span>
    </li>
  );
}
"""

CART_START = """\
import { formatPrice } from "../format";
import CartItem from "./CartItem";

// Алхам 5
export default function Cart({ items, total, onIncrease, onDecrease, onRemove, onClear }) {
  return (
    <aside className="cart" aria-label="Сагс">
      <h2>Сагс</h2>
      {/* TODO: items хоосон бол «Сагс хоосон байна» гэж харуул. Эс бөгөөс:
          - <ul className="cart-list"> дотор мөр бүрт CartItem (key-ээ мартуузай!)
          - <p className="total">Нийт: …</p> — formatPrice(total)
          - «Сагсыг хоослох» товч → onClear */}
    </aside>
  );
}
"""

STATE = ModuleSpec(
    title="Модул 3 — State ба харилцан үйлдэл",
    description="Үйл явдал, useState-ээр хэрэглэгчтэй харилцаж, state-ийг immutable шинэчилнэ.",
    lessons=[
        # --- 1 ------------------------------------------------------------------
        LessonSpec(
            title="Үйл явдал ба handler",
            slug="uil-yavdal",
            description="onClick-т функц холбож, event объект ашиглан, handler-ийг props-оор дамжуулах.",
            duration=900,
            language=JSX,
            content="""\
### Энэ хичээлээр

- `onClick`-оор товчинд үйлдэл холбох
- Функцийг **дамжуулах** ба **дуудах** ялгааг ойлгох
- Event объектоос мэдээлэл авах, event-ийн хөөрөлтийг зогсоох
- Handler-ийг props-оор хүүхэд component-д дамжуулах, `handleX` / `onX` нэршил

### Яагаад чухал вэ

Одоог хүртэл бидний component-ууд зөвхөн **харуулдаг** байлаа. Гэтэл апп
гэдэг хэрэглэгчийн үйлдэлд хариу өгөх ёстой: товч дарах, цэс нээх,
сагсанд бараа нэмэх. Хөтөч эдгээр үйлдэл бүрийг **үйл явдал** (event)
болгон мэдээлдэг. React-д үйл явдалд хариу өгөх функц буюу **event
handler**-ийг JSX дээр шууд холбоно — `addEventListener` бичих
шаардлагагүй.

### onClick-т функц өгөх

```jsx
export default function App() {
  function handleClick() {
    alert("Та товч дарлаа!");
  }

  return <button onClick={handleClick}>Намайг дар</button>;
}
```

Гурван зүйлийг анхаар:

- Handler-ийг component-ийн **дотор** бичнэ — ингэснээр props-д хандаж чадна.
- Prop-ийн нэр camelCase: `onClick`, `onMouseEnter`, `onKeyDown`. HTML-ийн
  `onclick` биш.
- `{}` дотор **функц** өгнө. HTML шиг `onclick="handleClick()"` гэсэн текст
  биш.

Богино handler-ийг JSX дотор шууд arrow функцээр бичиж болно:

```jsx
<button onClick={() => alert("Та товч дарлаа!")}>Намайг дар</button>
```

### Дамжуулах ба дуудах — хамгийн түгээмэл алдаа

```jsx
<button onClick={handleClick}>   // ✅ функцийг дамжуулж байна
<button onClick={handleClick()}> // ❌ render хийх үед ШУУД дуудна
```

Хоёр дахь мөрөнд `handleClick()` нь component render хийгдэх мөчид
ажиллаж, түүний буцаасан утга (`undefined`) `onClick`-т очно. Үр дүнд нь
хуудас ачаалагдах бүрт alert гарч, товч дарахад юу ч болохгүй. Бидний
хэлэх ёстой зүйл: «энэ функцийг **дараа нь**, дарахад дуудаарай».

Аргумент дамжуулах шаардлагатай бол arrow функцэд боож өгнө:

```jsx
<button onClick={() => handleDelete(product.id)}>Устгах</button>
```

`() => handleDelete(product.id)` бол шинэ функц. Товч дарах хүртэл
`handleDelete` дуудагдахгүй.

### Event объект

React handler-т үйл явдлын мэдээлэлтэй **event объект** дамжуулна.
Заншлаар `e` эсвэл `event` гэж нэрлэнэ:

```jsx
function handleClick(e) {
  console.log(e.type);               // "click"
  console.log(e.target.textContent); // дарсан товчны текст
}
```

Энэ бол хөтчийн event-ийг ороосон React-ийн **SyntheticEvent** — бүх
хөтөч дээр ижил ажиллана. Хамгийн хэрэгтэй хоёр арга:

| Арга | Юу хийх | Хэзээ |
|---|---|---|
| `e.preventDefault()` | Хөтчийн анхдагч үйлдлийг зогсооно | Холбоос, форм илгээх (Модул 4) |
| `e.stopPropagation()` | Event-ийг эцэг элемент рүү «хөөрөхөөс» зогсооно | Карт доторх товч |

Event **хөөрдөг** (bubbling): товч дээр дарахад эхлээд товчны, дараа нь
түүнийг агуулсан элементүүдийн handler ажиллана:

```jsx
<div className="card" onClick={() => console.log("Карт нээгдлээ")}>
  <button
    onClick={(e) => {
      e.stopPropagation(); // картын onClick ажиллахгүй
      console.log("Сагсанд нэмлээ");
    }}
  >
    Сагсанд нэмэх
  </button>
</div>
```

### Нэршил: handleX ба onX

React-ийн нийтлэг заншил:

- Handler **функцийг** `handle` + үйл явдал гэж нэрлэнэ: `handleClick`,
  `handleAddToCart`, `handleDelete`.
- Handler хүлээж авдаг **prop**-ийг `on` + үйл явдал гэж нэрлэнэ:
  `onClick`, `onAdd`, `onSelect`.

### Handler-ийг props-оор дамжуулах

Ихэнхдээ товч нь хүүхэд component-д байдаг, харин юу хийхийг нь эцэг
мэддэг. Тэгвэл эцэг нь функцээ **prop болгон** дамжуулна (Модул 2-т `onBuy`
гэж дурдсан):

```jsx
function ProductCard({ product, onAdd }) {
  return (
    <li>
      {product.name}
      <button onClick={() => onAdd(product)}>Сагсанд нэмэх</button>
    </li>
  );
}

export default function App() {
  function handleAdd(product) {
    console.log("Сагсанд нэмлээ:", product.name);
  }

  return (
    <ul>
      <ProductCard product={{ id: 1, name: "Банана" }} onAdd={handleAdd} />
    </ul>
  );
}
```

`ProductCard` юу хийхээ мэдэхгүй — зөвхөн «товч дарлаа, энэ бараа» гэж
мэдээлнэ. Шийдвэр нь `App`-д. Ингэснээр нэг `ProductCard`-ыг өөр өөр
газар өөр үйлдэлтэй ашиглана.

Анхаар: `<ProductCard onClick={…} />` гэж **өөрийн** component-д өгсөн
`onClick` бол зүгээр л нэг prop. `ProductCard` түүнийгээ дотроо
`<button>`-д холбохгүй бол юу ч болохгүй.

### Бусад түгээмэл event

| Prop | Хэзээ ажиллах |
|---|---|
| `onClick` | Дарахад |
| `onDoubleClick` | Давхар дарахад |
| `onMouseEnter`, `onMouseLeave` | Хулгана дээгүүр нь орох, гарахад |
| `onKeyDown` | Гарын товч дарахад |
| `onChange`, `onSubmit` | Форм — Модул 4 |

### Одоохондоо дэлгэц өөрчлөгдөхгүй

Handler дотор хувьсагч өөрчилсөн ч дэлгэц шинэчлэгдэхгүй — үүнд **state**
хэрэгтэй, дараагийн хичээлийн сэдэв. Тиймээс энэ хичээлд үр дүнг Console-оос
харна. Бодит Vite төсөлд ч код яг ийм: React event-үүдийг root элемент
дээр төвлөрүүлэн хүлээж аваад (event delegation) зөв handler-т хүргэдэг.

```jsx
function App() {
  function greet(name) {
    alert("Сайн уу, " + name);
  }
  return <button onClick={greet("Бат")}>Мэндлэх</button>;
}
```

```quiz
Дээрх кодыг ажиллуулахад юу болох вэ?
- [ ] Товч дарахад «Сайн уу, Бат» гарна
- [x] Хуудас ачаалагдахад шууд alert гарч, товч дарахад юу ч болохгүй
- [ ] Синтакс алдаа гарна
> `greet("Бат")` нь render хийх үед дуудагдана. `onClick={() => greet("Бат")}` гэж arrow функцэд боож өг.
```

```quiz
Карт доторх товч дарахад товчны handler-ийн дараа картын `onClick` ч ажиллаж байна. Үүнийг юу зогсоох вэ?
- [ ] `e.preventDefault()`
- [x] `e.stopPropagation()`
- [ ] Handler-ээс `return false` буцаах
> `preventDefault` нь хөтчийн анхдагч үйлдлийг (холбоос нээх, форм илгээх) зогсооно, хөөрөлтийг биш. React-д `return false` ямар ч нөлөөгүй.
```

```quiz
`TodoItem` component-д устгах функц дамжуулах. Prop-ийг заншлаар юу гэж нэрлэх вэ?
- [ ] `<TodoItem handleDelete={handleDelete} />`
- [x] `<TodoItem onDelete={handleDelete} />`
- [ ] `<TodoItem delete={handleDelete()} />`
> Prop нь `on`-оор, эцэг дэх функц нь `handle`-ээр эхэлнэ. Сүүлийн хувилбар нь функцийг render үед дуудчихна.
```

### Дүгнэлт

`onClick={handleClick}` — функцийг дамжуул, бүү дууд. Аргументтай бол
`onClick={() => handleDelete(id)}`. Event объект нь `e.target`,
`e.stopPropagation()` зэргийг өгнө. Handler-ийг `handleX`, түүнийг хүлээж
авах prop-ийг `onX` гэж нэрлээд хүүхэд component-д дамжуулна.
""",
            initial_code=vite(
                """\
import ProductCard from "./ProductCard";

const products = [
  { id: 1, name: "Банана", price: 3500, emoji: "🍌" },
  { id: 2, name: "Алим", price: 2800, emoji: "🍎" },
  { id: 3, name: "Сүү", price: 3200, emoji: "🥛" },
];

export default function App() {
  // TODO 2: handleAdd(product) функц бичиж, Console-д
  //         "Сагсанд нэмлээ: Банана" хэлбэрээр хэвлэ.

  // TODO 3: ProductCard бүрт onAdd prop-оор handleAdd-ийг дамжуул.
  return (
    <main>
      <h1>🥬 Ногоон сагс</h1>
      <ul className="grid">
        {products.map((product) => (
          <ProductCard key={product.id} product={product} />
        ))}
      </ul>
    </main>
  );
}
""",
                extra={
                    "ProductCard.jsx": """\
export default function ProductCard({ product, onAdd }) {
  // TODO 1: «Сагсанд нэмэх» дарахад onAdd(product)-ийг дууд.
  //         Анхаар: onClick-т функц ӨГНӨ, render үед дуудахгүй!
  return (
    <li className="card">
      <div className="emoji">{product.emoji}</div>
      <h2>{product.name}</h2>
      <p>{product.price}₮</p>
      <button type="button">Сагсанд нэмэх</button>
    </li>
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
**Түвшин:** ⭐⭐ · 10 минут

«Ногоон сагс»-ын картууд дээрх «Сагсанд нэмэх» товч одоо юу ч хийхгүй
байна. `ProductCard.jsx`-д товчийг `onAdd` prop-той холбож, `App.jsx`-д
`handleAdd` функц бичээд картуудад дамжуул. Товч дарахад Console-д
`Сагсанд нэмлээ: Банана` гэж гарах ёстой — «Хөтөч» дээр дарж шалгаарай.
""",
                tests=(
                    test(
                        "«Сагсанд нэмэх» дарахад onAdd тухайн бараатайгаа дуудагдана",
                        """
const ProductCard = mod("./ProductCard").default;
const product = { id: 2, name: "Алим", price: 2800, emoji: "🍎" };
const onAdd = fn();
render(<ul><ProductCard product={product} onAdd={onAdd} /></ul>);
await user.click(screen.getByRole("button", { name: /Сагсанд нэмэх/ }));
expect(onAdd).toHaveBeenCalledWith(product);
""",
                    ),
                    test(
                        "onAdd render үед биш, зөвхөн товч дарахад дуудагдана",
                        """
const ProductCard = mod("./ProductCard").default;
const onAdd = fn();
render(<ul><ProductCard product={{ id: 1, name: "Банана", price: 3500, emoji: "🍌" }} onAdd={onAdd} /></ul>);
expect(onAdd).not.toHaveBeenCalled();
const button = screen.getByRole("button", { name: /Сагсанд нэмэх/ });
await user.click(button);
await user.click(button);
expect(onAdd).toHaveBeenCalledTimes(2);
""",
                    ),
                    test(
                        "App дээр «Алим»-ын товч дарахад Console-д «Сагсанд нэмлээ: Алим» гарна",
                        """
render(<App />);
const buttons = screen.getAllByRole("button", { name: /Сагсанд нэмэх/ });
expect(buttons).toHaveLength(3);
await user.click(buttons[1]);
expect(logs.some((entry) => entry.text.includes("Сагсанд нэмлээ: Алим"))).toBe(true);
expect(logs.some((entry) => entry.text.includes("Банана"))).toBe(false);
""",
                    ),
                ),
                tips="""\
- `ProductCard`-д товч нь аль бараа болохыг мэддэг тул arrow функцэд боож
  дамжуулна: `onClick={() => …}`. Хаалтгүй `onClick={onAdd(product)}` гэвэл
  render хийх бүрт дуудагдаж, товч ажиллахгүй.
- `App`-д `function handleAdd(product) { … }` дотор `console.log`-д хоёр
  аргумент өгч болно: `"Сагсанд нэмлээ:"` ба `product.name`.
- `<ProductCard … onAdd={handleAdd} />` — энд `handleAdd`-ийн ард хаалт
  бичихгүй: функцийг өөрийг нь дамжуулж байна.
""",
                solution=solution(
                    App_jsx="""\
import ProductCard from "./ProductCard";

const products = [
  { id: 1, name: "Банана", price: 3500, emoji: "🍌" },
  { id: 2, name: "Алим", price: 2800, emoji: "🍎" },
  { id: 3, name: "Сүү", price: 3200, emoji: "🥛" },
];

export default function App() {
  function handleAdd(product) {
    console.log("Сагсанд нэмлээ:", product.name);
  }

  return (
    <main>
      <h1>🥬 Ногоон сагс</h1>
      <ul className="grid">
        {products.map((product) => (
          <ProductCard key={product.id} product={product} onAdd={handleAdd} />
        ))}
      </ul>
    </main>
  );
}
""",
                    ProductCard_jsx="""\
export default function ProductCard({ product, onAdd }) {
  return (
    <li className="card">
      <div className="emoji">{product.emoji}</div>
      <h2>{product.name}</h2>
      <p>{product.price}₮</p>
      <button type="button" onClick={() => onAdd(product)}>
        Сагсанд нэмэх
      </button>
    </li>
  );
}
""",
                ),
            ),
        ),
        # --- 2 ------------------------------------------------------------------
        LessonSpec(
            title="State ба useState",
            slug="usestate",
            description="Энгийн хувьсагч яагаад хангалтгүйг ойлгож, useState-ээр тоологч бүтээх.",
            duration=960,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Энгийн хувьсагч яагаад дэлгэцийг шинэчилдэггүйг ойлгох
- `useState`-ээр component-д «санах ой» өгөх
- State шинэчлэхэд React дахин render хийдгийг мэдэх
- Hook-ийн дүрэм: зөвхөн component-ийн дээд түвшинд дуудах

### Яагаад чухал вэ

Тоологч, сагсны тоо, нээлттэй цэс, сонгосон tab — цаг хугацааны явцад
өөрчлөгдөж, дэлгэцэнд тусдаг өгөгдлийг **state** гэнэ. Модул 0-д DOM-оор
тоологч бичихдээ тоо өөрчлөгдөх бүрт дэлгэцийг гараар шинэчилж байсныг
санаарай. React-д state-ээ өөрчлөхөд л хангалттай — дэлгэцийг React өөрөө
шинэчилнэ.

### Энгийн хувьсагч яагаад ажиллахгүй вэ

```jsx
export default function Counter() {
  let count = 0;

  function handleClick() {
    count = count + 1;
    console.log(count); // 1, 2, 3…
  }

  return <button onClick={handleClick}>Дарсан: {count}</button>;
}
```

Console-д тоо өсөж байгаа ч дэлгэцэнд «Дарсан: 0» хэвээр. Хоёр шалтгаантай:

1. **Локал хувьсагч өөрчлөгдөхийг React мэдэхгүй.** Дахин render хийх
   шалтгаан алга.
2. **Дахин render хийсэн ч** `let count = 0` мөр дахин ажиллаж, тоо 0
   болно. Component функц дуудагдах бүрт локал хувьсагчид шинээр үүсдэг.

Бидэнд render хооронд **хадгалагдах** утга, мөн өөрчлөгдөхөд **дахин
render** хийлгэх арга хэрэгтэй. Энэ хоёрыг `useState` өгнө.

### useState

```jsx
import { useState } from "react";

export default function Counter() {
  const [count, setCount] = useState(0);

  function handleClick() {
    setCount(count + 1);
  }

  return <button onClick={handleClick}>Дарсан: {count}</button>;
}
```

- `useState(0)` нь state үүсгэнэ. `0` бол **анхны утга**.
- Хоёр элементтэй массив буцаана: `[одоогийн утга, шинэчлэх функц]`.
  Модул 0-ийн массив задлалтаар нэр өгнө.
- Нэршил: `[something, setSomething]` — `[isOpen, setIsOpen]`,
  `[items, setItems]`.
- Анхны утга зөвхөн **эхний** render-т хэрэглэгдэнэ. Дараагийн
  render-үүдэд React хадгалсан утгаа өгнө.

### Товч дарахад юу болдог вэ

1. Эхний render: `useState(0)` → `count = 0`. Дэлгэцэнд «Дарсан: 0».
2. Товч дарахад `setCount(1)` дуудагдана. React шинэ утгыг хадгалаад
   дахин render хийхээр төлөвлөнө.
3. React `Counter` функцийг **дахин дуудна**. Энэ удаа `useState(0)` нь
   `1` буцаана.
4. Шинэ JSX-ийг хуучинтай нь харьцуулж, DOM-д зөвхөн өөрчлөгдсөн текстийг
   шинэчилнэ (Модул 1-ийн `root.render`-ийг санаарай).

Томьёолбол **UI = f(state)**: бид state-ийг өөрчилнө, дэлгэцийг React
тааруулна.

### Хэд хэдэн state

```jsx
const [count, setCount] = useState(0);
const [step, setStep] = useState(1);
```

State бүр бие даасан. Ямар ч утга хадгалж болно: тоо, текст, boolean,
объект, массив — дараагийн хичээлүүдэд бүгдийг үзнэ.

### State нь component бүрт тусдаа

```jsx
<Counter />
<Counter />
```

Хоёр тоологч тус тусын `count`-той: нэгийг нь дарахад нөгөө нь
өөрчлөгдөхгүй. State нь функцэд биш, дэлгэц дээрх тухайн **хувь**
(instance)-д хамаарна. Эцэг component хүүхдийнхээ state-ийг харж чадахгүй —
хэрэгтэй бол state-ийг эцэгт нь байрлуулж, props-оор дамжуулна (Модул 7).

### Hook-ийн дүрэм

`use`-ээр эхэлсэн функцийг **hook** гэнэ. `useState` бол таны анхны hook.
Дүрэм нь:

- Зөвхөн component-ийн (эсвэл өөр hook-ийн) **дээд түвшинд** дуудна.
- `if`, давталт, handler дотор дуудахгүй.

```jsx
function Counter({ enabled }) {
  if (enabled) {
    const [count, setCount] = useState(0); // ❌ нөхцөл дотор
  }

  function handleClick() {
    const [x, setX] = useState(0); // ❌ handler дотор — Invalid hook call
  }
}
```

React state-үүдийг **дуудсан дарааллаар** нь таньдаг. Нөхцөлөөр дараалал
өөрчлөгдвөл аль state аль нь болохыг андуурна. Модул 6-д дэлгэрэнгүй
үзнэ.

### Түгээмэл алдаанууд

| Алдаа | Юу болох |
|---|---|
| `count = count + 1`, `count++` | `const` тул TypeError. `let` байсан ч дэлгэц шинэчлэгдэхгүй |
| `setCount(count + 1)`-ийн дараа шууд `count`-ийг унших | Хуучин утга гарна — дараагийн хичээлийн сэдэв |
| `import`-оо мартах | `useState is not defined` |
| `onClick={setCount(count + 1)}` | Render бүрт дуудагдаж, дахин render хийлгэнэ — «Too many re-renders» алдаа |

### Бодит төсөлд

Vite төсөлд ч яг ийм. Хөтчийн **React DevTools** өргөтгөлийн «Components»
tab дээр component бүрийн state-ийг харж, гараар өөрчилж болно — алдаа
хайхад их тус болдог.

```quiz
Дээрх `let count = 0` бүхий `Counter`-ийн товчийг 3 удаа дарахад дэлгэцэнд юу харагдах вэ?
- [x] «Дарсан: 0»
- [ ] «Дарсан: 3»
- [ ] «Дарсан: 1»
> Локал хувьсагч өөрчлөгдсөн ч React дахин render хийхгүй. Console-д 1, 2, 3 гарна, дэлгэц хэвээр.
```

```quiz
`const [count, setCount] = useState(10);` — `10` хэзээ хэрэглэгдэх вэ?
- [ ] Render бүрт `count` 10 болж эхэлнэ
- [x] Зөвхөн эхний render-т
- [ ] `setCount` дуудах бүрт
> Дараагийн render-үүдэд React хадгалсан утгаа буцаана, анхны утгыг үл тооно.
```

```jsx
function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={setCount(count + 1)}>{count}</button>;
}
```

```quiz
Дээрх код «Too many re-renders» алдаа өгнө. Яагаад?
- [ ] `useState`-ийг буруу импортолсон
- [x] `setCount(count + 1)` render бүрт дуудагдаж, дахин render хийлгэсээр байна
- [ ] Товч доторх `{count}` тоо биш
> `onClick`-т функц өгөх ёстой: `onClick={() => setCount(count + 1)}`.
```

### Дүгнэлт

Локал хувьсагч render хооронд хадгалагдахгүй, өөрчлөгдөхөд дэлгэц
шинэчлэгдэхгүй. `const [value, setValue] = useState(initial)` — утгыг
хадгалж, `setValue` нь дахин render хийлгэнэ. Hook-ийг зөвхөн
component-ийн дээд түвшинд дууд.
""",
            initial_code=vite(
                """\
// TODO 1: react-оос useState-ийг импортло.

export default function App() {
  // TODO 2: энэ мөрийн оронд count state үүсгэ (анхны утга 0).
  const count = 0;

  // TODO 3: гурван товчинд handler холбо: «+» нэмнэ, «−» хасна,
  //         «Тэглэх» 0 болгоно. Тоо 0 үед «−» идэвхгүй (disabled).
  return (
    <main className="counter">
      <h1>Тоологч</h1>
      <p className="value">Тоо: {count}</p>
      <div className="row">
        <button type="button">−</button>
        <button type="button">+</button>
        <button type="button">Тэглэх</button>
      </div>
    </main>
  );
}
""",
                css=BASE_CSS
                + """
.counter {
  max-width: 320px;
}

.value {
  font-size: 2rem;
  font-weight: 700;
}

.row button {
  min-width: 48px;
}
""",
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 10 минут

Тоологчийг ажилладаг болго: «+» тоог нэмнэ, «−» хасна, «Тэглэх» 0
болгоно. Тоо сөрөг болох ёсгүй — тоо 0 үед «−» товчийг идэвхгүй
(`disabled`) болго. Тоо өөрчлөгдөхөд дэлгэцийг гараар шинэчлэх нэг ч
мөр бичихгүй гэдгийг Модул 0-ийн DOM тоологчтой харьцуулаарай.
""",
                tests=(
                    test(
                        "«+» дарахад тоо 1-ээр нэмэгдэнэ",
                        """
render(<App />);
const plus = screen.getByRole("button", { name: "+" });
await user.click(plus);
await user.click(plus);
expect(screen.getByText(/Тоо:/)).toHaveTextContent(/Тоо: ?2$/);
""",
                    ),
                    test(
                        "«−» дарахад тоо 1-ээр хасагдана",
                        """
render(<App />);
const plus = screen.getByRole("button", { name: "+" });
await user.click(plus);
await user.click(plus);
await user.click(plus);
await user.click(screen.getByRole("button", { name: /^[−-]$/ }));
expect(screen.getByText(/Тоо:/)).toHaveTextContent(/Тоо: ?2$/);
""",
                    ),
                    test(
                        "«Тэглэх» дарахад тоо 0 болно",
                        """
render(<App />);
const plus = screen.getByRole("button", { name: "+" });
await user.click(plus);
await user.click(plus);
await user.click(screen.getByRole("button", { name: "Тэглэх" }));
expect(screen.getByText(/Тоо:/)).toHaveTextContent(/Тоо: ?0$/);
""",
                    ),
                    test(
                        "Тоо 0 үед «−» товч идэвхгүй, 0-ээс их үед идэвхтэй",
                        """
render(<App />);
const minus = screen.getByRole("button", { name: /^[−-]$/ });
expect(minus).toBeDisabled();
await user.click(screen.getByRole("button", { name: "+" }));
expect(minus).toBeEnabled();
await user.click(minus);
expect(minus).toBeDisabled();
expect(screen.getByText(/Тоо:/)).toHaveTextContent(/Тоо: ?0$/);
""",
                    ),
                ),
                tips="""\
- `import { useState } from "react";`, дараа нь `const count = 0;` мөрийг
  `const [count, setCount] = useState(0);` болго.
- Товч бүрт `onClick={() => setCount(…)}`. Arrow функцгүйгээр
  `onClick={setCount(count + 1)}` гэвэл «Too many re-renders» алдаа гарна.
- `disabled`-д state-ээс тооцсон boolean өг: `disabled={count === 0}`.
  Ингэвэл тоо 0 болох бүрт товч өөрөө идэвхгүй болно.
""",
                solution=solution(
                    App_jsx="""\
import { useState } from "react";

export default function App() {
  const [count, setCount] = useState(0);

  return (
    <main className="counter">
      <h1>Тоологч</h1>
      <p className="value">Тоо: {count}</p>
      <div className="row">
        <button type="button" onClick={() => setCount(count - 1)} disabled={count === 0}>
          −
        </button>
        <button type="button" onClick={() => setCount(count + 1)}>
          +
        </button>
        <button type="button" onClick={() => setCount(0)}>
          Тэглэх
        </button>
      </div>
    </main>
  );
}
"""
                ),
            ),
        ),
        # --- 3 ------------------------------------------------------------------
        LessonSpec(
            title="State бол агшин зураг",
            slug="state-snapshot",
            description="setState утгыг шууд биш дараагийн render-т өөрчилдөг, batching хэрхэн ажилладгийг ойлгох.",
            duration=960,
            language=JSX,
            content="""\
### Энэ хичээлээр

- State-ийг render бүрийн **агшин зураг** гэж ойлгох
- `setState` утгыг шууд биш, дараагийн render-т өөрчилдгийг мэдэх
- Batching: нэг handler доторх олон шинэчлэлт нэг render болдгийг ойлгох
- Шинэ утгыг handler дотор зөв ашиглах

### Яагаад чухал вэ

«`setCount` дуудсан, гэтэл `console.log(count)` хуучин утга хэвлэлээ!» —
React сурч буй хүн бүрийн гайхдаг зүйл. Үүнийг ойлгохгүй бол серверт
хуучин утга илгээх, эцэг component-д буруу тоо мэдээлэх зэрэг олоход хэцүү
алдаа гарна.

### Render бол агшин зураг

React component-ийг дуудах бүрт (render) тухайн мөчийн props, state-ээр
JSX-ийн **агшин зургийг** авдаг. Тэр render-т үүссэн handler-ууд ч мөн
тэр зургийн утгуудыг «санаж» үлдэнэ.

```jsx
const [count, setCount] = useState(0);

function handleClick() {
  setCount(count + 1);
  console.log(count); // 0 — хуучин агшин хэвээр
}
```

Энэ render-т `count` бол энгийн `const` тоо — `0`. `setCount` түүнийг
өөрчлөхгүй, харин React-д «дараагийн render-т `count`-ийг 1 болго» гэсэн
**хүсэлт** илгээнэ. Одоогийн handler хуучин зургаа харсаар дуусна.
Шинэ утга (`1`) зөвхөн **дараагийн** render, түүний шинэ handler-т ирнэ.

### Алхам алхмаар

1. Render 1: `count = 0`. Үүссэн `handleClick` нь `count = 0`-ийг санасан.
2. Товч дарахад handler ажиллана: `setCount(0 + 1)` → хүсэлт дараалалд орно.
3. `console.log(count)` → `0`.
4. Handler дуусна. React дахин render хийнэ: `count = 1`, шинэ
   `handleClick` үүснэ.

### Гурван удаа дуудвал?

```jsx
function handleClick() {
  setCount(count + 1);
  setCount(count + 1);
  setCount(count + 1);
}
```

Товч дарахад тоо **1**-ээр л нэмэгдэнэ. Гурван мөр бүгд ижил агшин
(`count = 0`)-аас тооцож, `setCount(1)`-ийг гурван удаа хэлж байна.
Үүнийг засах аргыг дараагийн хичээлд үзнэ.

### Batching — нэг удаа render

React handler доторх бүх код дуусахыг хүлээгээд, бүх state шинэчлэлтийг
**нэг** render-т нэгтгэдэг. Үүнийг **batching** гэнэ. Ресторанд зөөгч таны
хоол бүрийг сонсох тоолон гал тогоо руу гүйдэггүй — бүх захиалгыг
сонсоод нэг удаа очдогтой адил.

```jsx
function handleReset() {
  setCount(0);
  setStep(1);
  setMessage("Тэглэлээ");
  // Гурван state → НЭГ render
}
```

Ингэснээр хагас шинэчлэгдсэн дэлгэц хэзээ ч харагдахгүй бөгөөд илүү
хурдан. React 18-аас хойш `setTimeout`, `fetch`-ийн дараах шинэчлэлтүүд
ч мөн нэгтгэгддэг.

### Хожим ажиллах код ч хуучин агшинг харна

```jsx
function handleClick() {
  setCount(count + 5);
  setTimeout(() => {
    alert(count); // 0 — 3 секундийн дараа ч гэсэн
  }, 3000);
}
```

Alert гарах үед дэлгэцэнд аль хэдийн 5 харагдаж байгаа ч `alert` дарах
үеийн агшин (`0`)-ийг харна. Энэ бол алдаа биш: handler өөрийн render-ийн
утгуудтай гэрэл зураг шиг хадгалагддаг тул үр дүнг нь таамаглахад амар.

### Шинэ утга хэрэгтэй бол хувьсагчид тооцоол

```jsx
function handleClick() {
  const nextCount = count + 1;
  setCount(nextCount);
  console.log(nextCount); // 1 ✅
  onChange(nextCount);    // эцэгт ч шинэ утгыг мэдээлнэ ✅
}
```

Шинэ утгыг **нэг удаа** тооцоод, state-д ч, бусад газар ч тэр хувьсагчаа
ашигла.

Энд `onChange` бол эцэг component-ийн дамжуулсан **энгийн callback
prop** — өмнөх хичээлийн `onAdd`, `onSelect`-тэй адил `on` + үйл явдал
нэршилтэй. Input-ийн `onChange` event-тэй хамаагүй (түүнийг Модул 4-т
үзнэ).

### Бодит төсөлд

Ийм алдаа ихэвчлэн серверт хадгалах, аналитик руу илгээх, эцэг
component-ийн `onChange`-ийг дуудах үед гардаг. Жишээ нь сагсны тоо
өөрчлөгдөхөд `saveCart(items)` гэж хуучин массив илгээх. Санах дүрэм:
`setX(…)`-ийн дараах мөрүүдэд `x` **өөрчлөгдөөгүй** хэвээр.

```jsx
const [count, setCount] = useState(0);

function handleClick() {
  setCount(count + 1);
  setCount(count + 1);
  console.log(count);
}
```

```quiz
Дээрх товчийг нэг удаа дарахад Console-д юу гарч, дэлгэц дээр `count` хэд болох вэ?
- [ ] Console: 2, дэлгэц: 2
- [x] Console: 0, дэлгэц: 1
- [ ] Console: 1, дэлгэц: 2
- [ ] Console: 0, дэлгэц: 2
> Хоёр `setCount` хоёулаа `0 + 1`-ийг хүсэж байна. `console.log` нь энэ render-ийн агшин буюу 0-ийг хэвлэнэ.
```

```jsx
const [name, setName] = useState("Бат");

function handleClick() {
  setName("Сараа");
  setTimeout(() => console.log(name), 1000);
}
```

```quiz
Дээрх товчийг дарснаас 1 секундийн дараа Console-д юу гарах вэ?
- [x] «Бат»
- [ ] «Сараа»
- [ ] `undefined`
> Дэлгэцэнд «Сараа» гарсан ч `setTimeout`-ийн функц дарах үеийн агшинд үүссэн тул `name` нь «Бат».
```

```quiz
Нэг handler дотор гурван өөр state (`setCount`, `setStep`, `setMessage`) шинэчилбэл хэдэн удаа render хийгдэх вэ?
- [ ] 3 удаа — шинэчлэлт бүрт
- [x] 1 удаа — handler дууссаны дараа
- [ ] 0 удаа — дахин товч дарах хүртэл
> React шинэчлэлтүүдийг нэгтгэж (batching), handler дууссаны дараа нэг л удаа render хийнэ.
```

### Дүгнэлт

Render бүр өөрийн state-ийн агшин зурагтай, handler-ууд тэр зургийг
санана. `setState` одоогийн хувьсагчийг өөрчлөхгүй — дараагийн render-ийг
төлөвлөнө. React шинэчлэлтүүдийг нэгтгэж нэг удаа render хийнэ. Шинэ
утга хэрэгтэй бол эхлээд хувьсагчид тооцоол.
""",
            initial_code=files(
                (
                    "QuantityPicker.jsx",
                    """\
import { useState } from "react";

export default function QuantityPicker({ onChange }) {
  const [quantity, setQuantity] = useState(1);

  // 🐞 «+» дарахад энд 2 гарч байхад доорх «Сагсанд:» 1 хэвээр байна.
  //    Хоёр handler хоёулаа эцэгтээ ХУУЧИН тоог мэдээлж байна. Зас.
  function handleIncrease() {
    setQuantity(quantity + 1);
    onChange(quantity);
  }

  function handleDecrease() {
    // TODO: тоо 1-ээс доош буурах ёсгүй.
    setQuantity(quantity - 1);
    onChange(quantity);
  }

  return (
    <div className="picker">
      <button type="button" aria-label="Тоог хасах" onClick={handleDecrease}>
        −
      </button>
      <span className="quantity">{quantity}</span>
      <button type="button" aria-label="Тоог нэмэх" onClick={handleIncrease}>
        +
      </button>
    </div>
  );
}
""",
                ),
                (
                    "App.jsx",
                    """\
// Энэ файлыг өөрчлөх шаардлагагүй — алдаа нь QuantityPicker.jsx-д.
import { useState } from "react";
import QuantityPicker from "./QuantityPicker";

const PRICE = 12500;

export default function App() {
  // Picker-ийн мэдээлсэн тоог хадгална.
  const [quantity, setQuantity] = useState(1);

  function handleQuantityChange(next) {
    console.log("Picker мэдээллээ:", next);
    setQuantity(next);
  }

  return (
    <main className="card product">
      <div className="emoji">🧀</div>
      <h1>Бяслаг</h1>
      <p>Нэгжийн үнэ: 12,500₮</p>
      <QuantityPicker onChange={handleQuantityChange} />
      <p className="summary">
        Сагсанд: {quantity} ширхэг · Дүн: {(quantity * PRICE).toLocaleString("en-US")}₮
      </p>
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
.product {
  max-width: 320px;
}

.emoji {
  font-size: 3rem;
}

.picker {
  display: inline-flex;
  align-items: center;
  gap: 12px;
}

.picker button {
  width: 40px;
  height: 40px;
  padding: 0;
  font-size: 1.2rem;
}

.quantity {
  min-width: 24px;
  font-size: 1.3rem;
  font-weight: 700;
  text-align: center;
}

.summary {
  margin-top: 16px;
  font-weight: 600;
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

Бяслагны хуудсан дээр «+» дарахад тоо сонгогч 2 болж байхад доорх
«Сагсанд: 1 ширхэг» нэг алхмаар хоцорч байна. Console дахь «Picker
мэдээллээ» мөрүүдийг хараарай. `QuantityPicker.jsx`-ийн handler-ууд
эцэгтээ шинэ тоог мэдээлдэг болгож зас, мөн тоо 1-ээс доош буурахгүй
болго. `App.jsx` түгжигдсэн.
""",
                tests=(
                    test(
                        "«+» дарахад onChange шинэ тоогоор (2) дуудагдана",
                        """
const QuantityPicker = mod("./QuantityPicker").default;
const onChange = fn();
render(<QuantityPicker onChange={onChange} />);
await user.click(screen.getByRole("button", { name: /нэмэх/ }));
expect(onChange).toHaveBeenLastCalledWith(2);
""",
                    ),
                    test(
                        "Дараалан «+», «+», «−» дарахад onChange 2, 3, 2 гэж дуудагдана",
                        """
const QuantityPicker = mod("./QuantityPicker").default;
const onChange = fn();
render(<QuantityPicker onChange={onChange} />);
await user.click(screen.getByRole("button", { name: /нэмэх/ }));
await user.click(screen.getByRole("button", { name: /нэмэх/ }));
await user.click(screen.getByRole("button", { name: /хасах/ }));
expect(onChange.mock.calls).toEqual([[2], [3], [2]]);
""",
                    ),
                    test(
                        "Тоо 1-ээс доош буурахгүй",
                        """
const QuantityPicker = mod("./QuantityPicker").default;
const onChange = fn();
render(<QuantityPicker onChange={onChange} />);
const minus = screen.getByRole("button", { name: /хасах/ });
await user.click(minus);
expect(screen.text()).not.toContain("0");
await user.click(minus);
expect(screen.text()).toContain("1");
expect(onChange.mock.calls.every(([next]) => next >= 1)).toBe(true);
""",
                    ),
                    test(
                        "App дахь «Сагсанд» тоо ба дүн сонгогчтой таарна",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: /нэмэх/ }));
await user.click(screen.getByRole("button", { name: /нэмэх/ }));
expect(screen.text()).toContain("Сагсанд: 3 ширхэг");
expect(screen.text()).toContain("37,500₮");
""",
                    ),
                ),
                tips="""\
- `setQuantity(quantity + 1)`-ийн дараах мөрөнд `quantity` өөрчлөгдөөгүй —
  энэ нь одоогийн render-ийн агшин.
- Шинэ утгыг эхлээд хувьсагчид тооцоол: `const next = quantity + 1;`,
  дараа нь `setQuantity(next)` ба `onChange(next)`.
- 1-ээс доош буулгахгүйн тулд handler-ийн эхэнд `if (quantity === 1) return;`
  гэж шалга, эсвэл «−» товчинд `disabled={quantity === 1}` өг.
- Энд тоо хоёр газар (сонгогч ба `App`) хадгалагдаж байгаа нь өөрөө эрсдэлтэй.
  State-ийг нэг газар байлгах аргыг Модул 7-д үзнэ.
""",
                solution=solution(
                    QuantityPicker_jsx="""\
import { useState } from "react";

export default function QuantityPicker({ onChange }) {
  const [quantity, setQuantity] = useState(1);

  function handleIncrease() {
    const next = quantity + 1;
    setQuantity(next);
    onChange(next);
  }

  function handleDecrease() {
    if (quantity === 1) return;
    const next = quantity - 1;
    setQuantity(next);
    onChange(next);
  }

  return (
    <div className="picker">
      <button
        type="button"
        aria-label="Тоог хасах"
        onClick={handleDecrease}
        disabled={quantity === 1}
      >
        −
      </button>
      <span className="quantity">{quantity}</span>
      <button type="button" aria-label="Тоог нэмэх" onClick={handleIncrease}>
        +
      </button>
    </div>
  );
}
"""
                ),
            ),
        ),
        # --- 4 ------------------------------------------------------------------
        LessonSpec(
            title="Функцээр шинэчлэх",
            slug="funktsional-shinechlelt",
            description="setCount((c) => c + 1) — өмнөх утгаас тооцож, нэг handler-т олон удаа шинэчлэх.",
            duration=900,
            language=JSX,
            content="""\
### Энэ хичээлээр

- `setCount((c) => c + 1)` — өмнөх утгаас тооцох функц дамжуулах
- React шинэчлэлтийн дарааллыг (queue) хэрхэн боловсруулдгийг ойлгох
- Утгаар ба функцээр шинэчлэхийн алийг нь хэзээ хэрэглэхийг мэдэх
- Updater функцийн түгээмэл алдаанаас сэргийлэх

### Яагаад чухал вэ

Өмнөх хичээлд `setCount(count + 1)`-ийг гурван удаа дуудахад тоо 1-ээр
л нэмэгдсэн. Гэтэл нэг үйлдэл state-ийг хэд хэдэн удаа өөрчлөх, эсвэл
хожим ажиллах код (timer, серверийн хариу) state шинэчлэх нь бодит апп-д
байнга тохиолддог. Ийм үед агшны хуучин утгаас биш, **хамгийн сүүлийн**
утгаас тооцох хэрэгтэй.

### Updater функц

`setState`-д утгын оронд **функц** өгч болно:

```jsx
function handleClick() {
  setCount((c) => c + 1);
  setCount((c) => c + 1);
  setCount((c) => c + 1);
}
```

Одоо тоо 3-аар нэмэгдэнэ. `(c) => c + 1` бол «өмнөх утга юу ч байсан,
түүн дээр 1 нэм» гэсэн **заавар**. React үүнийг дараалалд хийгээд,
дараагийн render-ийн үеэр нэг нэгээр нь ажиллуулна. Ийм функцийг
**updater функц** гэнэ.

### React дарааллыг хэрхэн боловсруулдаг вэ

Handler ажиллах үед React бүх `setCount`-ийг дараалалд бичнэ. Дараагийн
render дээр тэдгээрийг эхнээс нь ажиллуулна:

| Дараалал | `c` (өмнөх) | Буцаах |
|---|---|---|
| `(c) => c + 1` | 0 | 1 |
| `(c) => c + 1` | 1 | 2 |
| `(c) => c + 1` | 2 | 3 |

Эцсийн утга 3-ыг React хадгалж, `useState` буцаана.

Утгаар дуудсан `setCount(5)` ч дараалалд ордог — «өмнөхийг үл тоон 5
болго» гэсэн заавар:

```jsx
setCount(count + 5);    // count = 0 → «5 болго»
setCount((c) => c + 1); // 5 → 6
```

Дарахад 6 болно. Харин эсрэг дарааллаар бол:

```jsx
setCount((c) => c + 1); // 0 → 1
setCount(42);           // → 42
```

Сүүлийн заавар «42 болго» тул үр дүн 42.

### Хожим ажиллах код

```jsx
function handleLikeLater() {
  setTimeout(() => {
    setLikes((l) => l + 1); // ✅ үргэлж сүүлийн утгаас
  }, 1000);
}
```

Товчийг секундэд гурав дарвал `setLikes(likes + 1)` хувилбарт гурван
timer бүгд дарах үеийн ижил агшнаас тооцож, лайк 1-ээр л нэмэгдэнэ.
Updater хувилбар 3 болно. Timer, серверийн хүсэлтийг Модул 5-д
дэлгэрэнгүй үзнэ.

### Хэзээ аль нь вэ

| Нөхцөл | Хэлбэр |
|---|---|
| Шинэ утга өмнөхөөсөө хамаарахгүй | `setCount(0)`, `setName("Бат")` |
| Нэг handler-т хэд хэдэн удаа шинэчлэх | `setCount((c) => c + 1)` |
| Timer, серверийн хариу гэх мэт хожим ажиллах код | `setCount((c) => c + 1)` |
| Өмнөхөөсөө хамаарах, ганц удаа | Аль нь ч болно. Олон баг updater-ийг илүүд үздэг |

Параметрийн нэрийг state-ийн эхний үсгээр (`c`, `s`), `prevCount` гэж,
эсвэл state-ийн нэрээр нь (`count => count + 1`) өгдөг. Гол нь уншихад
ойлгомжтой байх.

### Түгээмэл алдаанууд

```jsx
setCount((c) => c++);       // ❌ c++ хуучин утгаа буцаана — өөрчлөгдөхгүй
setCount((c) => { c + 1 }); // ❌ {} дотор return алга → undefined
setCount(() => count + 1);  // ❌ функц ч гэсэн хуучин агшны count-оос тооцож байна
```

Updater нь **цэвэр функц** байх ёстой: өмнөх утгаас шинийг тооцоод
буцаана, өөр юу ч хийхгүй. Дотор нь `console.log`, серверийн хүсэлт, өөр
`setState` бичихгүй. Хөгжүүлэлтийн горимд (StrictMode) React updater-ийг
зориуд хоёр удаа ажиллуулж, цэвэр эсэхийг шалгадаг.

### Бодит төсөлд

Бодит кодод updater маш түгээмэл: цэс нээх, хаах `setOpen((o) => !o)`,
жагсаалтад нэмэх `setItems((prev) => [...prev, item])`, секунд тоолох
`setSeconds((s) => s + 1)`. Дараагийн хичээлүүдэд boolean, объект,
массив state-д ч ийм хэлбэрийг ашиглана.

```jsx
const [score, setScore] = useState(1);

function handleClick() {
  setScore(score + 2);
  setScore((s) => s * 10);
}
```

```quiz
Дээрх товчийг нэг удаа дарахад `score` хэд болох вэ?
- [ ] 12
- [ ] 20
- [x] 30
- [ ] 3
> Эхний заавар «3 болго» (1 + 2), дараагийнх нь өмнөх 3-ыг 10 дахин ихэсгэнэ.
```

```quiz
`count` нь 0 үед `setCount((c) => c + 1); setCount(count + 1);` гэж дуудвал дараагийн render-т `count` хэд болох вэ?
- [x] 1
- [ ] 2
- [ ] 0
> Хоёр дахь нь агшны `count` (0)-оос тооцсон «1 болго» гэсэн заавар тул эхнийхийн үр дүнг дарж бичнэ.
```

```quiz
`setCount((c) => c++)` гэж бичсэн товч дарахад юу болох вэ?
- [ ] Тоо 1-ээр нэмэгдэнэ
- [x] Тоо өөрчлөгдөхгүй
- [ ] Алдаа гарна
> `c++` нь нэмэхээсээ өмнөх утгаа буцаадаг. Updater-ээс `c + 1` буцаа.
```

### Дүгнэлт

`setX((prev) => …)` нь өмнөх утгаас шинийг тооцох заавар — React
дарааллаар нь ажиллуулна. Нэг handler-т олон удаа, эсвэл хожим ажиллах
кодоос шинэчлэхдээ updater хэрэглэ. Updater цэвэр байх ёстой.
""",
            initial_code=vite(
                """\
import { useState } from "react";

export default function App() {
  const [score, setScore] = useState(0);

  // 🐞 «+2» дарахад оноо 1-ээр л нэмэгдэж байна.
  function addPoint() {
    setScore(score + 1);
  }

  function handleScore(points) {
    for (let i = 0; i < points; i++) {
      addPoint();
    }
  }

  // Хоёр онооны шидэлт + торгуулийн шидэлт: хоёр тусдаа үйлдэл.
  // Энэ функцийг өөрчлөхгүйгээр ажилладаг болгох нь гол сорилт.
  function handleAndOne() {
    handleScore(2);
    handleScore(1);
  }

  // TODO: «+2»-ын дараа «+3» товч нэм.
  return (
    <main className="scoreboard">
      <h1>🏀 Онооны самбар</h1>
      <p className="score">Оноо: {score}</p>
      <div className="row">
        <button type="button" onClick={() => handleScore(1)}>
          +1
        </button>
        <button type="button" onClick={() => handleScore(2)}>
          +2
        </button>
        <button type="button" onClick={handleAndOne}>
          +2 ба +1
        </button>
        <button type="button" onClick={() => setScore(0)}>
          Тэглэх
        </button>
      </div>
    </main>
  );
}
""",
                css=BASE_CSS
                + """
.scoreboard {
  max-width: 420px;
}

.score {
  font-size: 2.2rem;
  font-weight: 700;
}
""",
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 10 минут

Сагсан бөмбөгийн онооны самбар дээр «+2» дарахад оноо 1-ээр л нэмэгдэж
байна. `addPoint`-ийг функцээр шинэчилдэг болгож засаад, «+2»-ын дараа
«+3» товч нэм. «+2 ба +1» товчны `handleAndOne`-ийг өөрчлөхгүйгээр
ажилладаг болгож чадах уу?
""",
                tests=(
                    test(
                        "«+3» товч оноог 3-аар нэмэгдүүлнэ",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: "+3" }));
expect(screen.getByText(/Оноо:/)).toHaveTextContent(/Оноо: ?3$/);
""",
                    ),
                    test(
                        "«+2» товч оноог 2-оор нэмэгдүүлнэ",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: "+2" }));
expect(screen.getByText(/Оноо:/)).toHaveTextContent(/Оноо: ?2$/);
""",
                    ),
                    test(
                        "«+2 ба +1» товч оноог 3-аар нэмэгдүүлнэ",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: "+2 ба +1" }));
expect(screen.getByText(/Оноо:/)).toHaveTextContent(/Оноо: ?3$/);
""",
                    ),
                    test(
                        "Дараалан дарахад оноо хуримтлагдана: +3, +2, +1 → 6",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: "+3" }));
await user.click(screen.getByRole("button", { name: "+2" }));
await user.click(screen.getByRole("button", { name: "+1" }));
expect(screen.getByText(/Оноо:/)).toHaveTextContent(/Оноо: ?6$/);
""",
                    ),
                ),
                tips="""\
- `addPoint` давталтад хэд дуудагдсан ч бүгд ижил агшны `score`-оос тооцож
  байна. Утгын оронд updater өг: «өмнөх оноо дээр 1 нэм».
- `handleScore`-ийг `setScore(score + points)` болгож засвал «+3» ажиллах ч
  «+2 ба +1» ажиллахгүй хэвээр. Яагаад гэдгийг хүснэгтээр дарааллыг зурж
  бодоорой.
- «+3» товч бусадтайгаа адилхан: `onClick`-т `handleScore(3)`-ийг дуудах
  arrow функц өгнө.
""",
                solution=solution(
                    App_jsx="""\
import { useState } from "react";

export default function App() {
  const [score, setScore] = useState(0);

  function addPoint() {
    setScore((s) => s + 1);
  }

  function handleScore(points) {
    for (let i = 0; i < points; i++) {
      addPoint();
    }
  }

  function handleAndOne() {
    handleScore(2);
    handleScore(1);
  }

  return (
    <main className="scoreboard">
      <h1>🏀 Онооны самбар</h1>
      <p className="score">Оноо: {score}</p>
      <div className="row">
        <button type="button" onClick={() => handleScore(1)}>
          +1
        </button>
        <button type="button" onClick={() => handleScore(2)}>
          +2
        </button>
        <button type="button" onClick={() => handleScore(3)}>
          +3
        </button>
        <button type="button" onClick={handleAndOne}>
          +2 ба +1
        </button>
        <button type="button" onClick={() => setScore(0)}>
          Тэглэх
        </button>
      </div>
    </main>
  );
}
"""
                ),
            ),
        ),
        # --- 5 ------------------------------------------------------------------
        LessonSpec(
            title="Boolean state: харуулах/нуух",
            slug="boolean-state",
            description="Boolean state-ээр хэсэг нээж хааж, aria-expanded-аар хүртээмжтэй болгох.",
            duration=900,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Boolean state-ээр ямар нэг хэсгийг харуулах, нуух
- `setIsOpen((open) => !open)`-оор toggle хийх
- `aria-expanded`-аар дэлгэц уншигчид нээлттэй эсэхийг мэдэгдэх
- `&&`-ээр устгах ба `hidden`-ээр нуухын ялгааг мэдэх

### Яагаад чухал вэ

Цэс нээх, хаах, «Дэлгэрэнгүй» хэсэг, нууц үг харуулах, харанхуй горим,
модал цонх — UI-ийн маш олон хэсэг «тийм / үгүй» гэсэн хоёр төлөвтэй.
Эдгээрийг бүгдийг нь boolean state-ээр хийнэ.

### Toggle

```jsx
import { useState } from "react";

function Details() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <section>
      <button onClick={() => setIsOpen((open) => !open)}>
        {isOpen ? "Хураах" : "Дэлгэрэнгүй"}
      </button>
      {isOpen && <p>Улаанбаатар хотод 24 цагийн дотор хүргэнэ.</p>}
    </section>
  );
}
```

- `!open` нь эсрэг утгыг буцаана. `setIsOpen(!isOpen)` ч ажиллана, гэхдээ
  updater хэлбэр аюулгүй (өмнөх хичээл).
- Boolean-ийг `is`, `has`, `show` угтвартай нэрлэдэг: `isOpen`,
  `isVisible`, `hasError`, `showPassword`. Нэрнээс нь «тийм / үгүй» утга
  гэдэг шууд мэдэгдэнэ.
- Нэг boolean-оос олон зүйл тооцогдоно: товчны текст, сум, класс,
  `aria-expanded`. Тэдгээрийг тусад нь state-д хадгалахгүй.

### Нууц үг харуулах

```jsx
function PasswordField() {
  const [showPassword, setShowPassword] = useState(false);

  return (
    <div>
      <input type={showPassword ? "text" : "password"} aria-label="Нууц үг" />
      <button onClick={() => setShowPassword((show) => !show)}>
        {showPassword ? "🙈 Нуух" : "👁️ Харуулах"}
      </button>
    </div>
  );
}
```

Энд input-ийн **утгыг** React удирдахгүй — зөвхөн `type` attribute-ийг
сольж байна. Бичсэн текстийг state-ээр удирдахыг Модул 4-т үзнэ.

### Хүртээмж: aria-expanded

Харж буй хэрэглэгч хэсэг нээгдсэнийг нүдээрээ хардаг. Харин дэлгэц
уншигч (screen reader) ашигладаг хүнд товч нь хэсгийг **нээж хаадаг**
гэдгийг, одоо нээлттэй эсэхийг хэлж өгөх хэрэгтэй:

```jsx
<button
  aria-expanded={isOpen}
  aria-controls="delivery-info"
  onClick={() => setIsOpen((open) => !open)}
>
  <span aria-hidden="true">{isOpen ? "▾" : "▸"}</span> Хүргэлтийн нөхцөл
</button>
{isOpen && <p id="delivery-info">Улаанбаатар хотод 24 цагийн дотор.</p>}
```

- `aria-expanded={isOpen}` нь DOM-д `"true"` / `"false"` болж бичигдэнэ.
  Дэлгэц уншигч «Хүргэлтийн нөхцөл, товч, хураасан» гэж уншина.
- `aria-controls` нь аль хэсгийг удирддагийг заана.
- Сум зөвхөн нүдэнд зориулсан тул `aria-hidden="true"`-гаар дэлгэц
  уншигчаас нууна.
- Заавал `<button>` хэрэглэ. `<div onClick>`-д гарын Tab, Enter хүрэхгүй.

### && ба hidden

| Арга | DOM | Доторх state |
|---|---|---|
| `{isOpen && <Panel />}` | Хаахад DOM-оос устна | Хамт устна — дахин нээхэд шинээр эхэлнэ |
| `<div hidden={!isOpen}>…</div>` | DOM-д үлдэж, харагдахгүй | Хадгалагдана |

Ихэнх тохиолдолд `&&` хангалттай. Хаагдсан хэсгийн доторх төлөв (жишээ
нь бичсэн текст) хадгалагдах ёстой бол `hidden` хэрэглэнэ.

### Хэд хэдэн хэсэг

`FaqItem` бүр өөрийн `isOpen`-той бол тус тусдаа нээгдэнэ — state
component бүрт тусдаа. «Нэг удаад зөвхөн нэг нь нээлттэй» байх ёстой бол
state-ийг эцэгт нь шилжүүлж `openId` хадгална. Үүнийг Модул 7-д үзнэ.

### Олон boolean-оос болгоомжил

```jsx
const [isLoading, setIsLoading] = useState(false);
const [isError, setIsError] = useState(false);
const [isSuccess, setIsSuccess] = useState(false);
```

Гурвуулаа нэг зэрэг `true` байж болох уу? Үгүй ч код үүнийг зөвшөөрч
байна — «боломжгүй төлөв» үүсэх эрсдэлтэй. Бие биеэ үгүйсгэдэг төлөвүүдийг
нэг текст state-ээр илэрхийл: `useState("idle")` → `"loading"`,
`"error"`, `"success"`. Энэ хэв маягийг Модул 4, 5-д ашиглана.

```jsx
const [isOpen, setIsOpen] = useState(false);

function handleClick() {
  setIsOpen(!isOpen);
  setIsOpen(!isOpen);
}
```

```quiz
Дээрх товчийг нэг удаа дарахад `isOpen` юу болох вэ?
- [x] `true`
- [ ] `false`
- [ ] Алдаа гарна
> Хоёр мөр хоёулаа агшны `isOpen` (false)-оос тооцож «true болго» гэнэ. `setIsOpen((open) => !open)` хоёр удаа бол `false` болно.
```

```quiz
Хэсэг нээж хаадаг товчинд дэлгэц уншигчид зориулж юу нэмэх вэ?
- [ ] `title="нээх"`
- [x] `aria-expanded={isOpen}`
- [ ] `role="toggle"`
> `aria-expanded` нь товч хэсгийг удирддаг, одоо нээлттэй эсэхийг мэдэгдэнэ.
```

```quiz
`{isOpen && <Comment />}` доторх input-д текст бичээд хаагаад дахин нээвэл юу болох вэ?
- [ ] Текст хэвээр үлдэнэ
- [x] Текст арилна
- [ ] Алдаа гарна
> `&&` нь хаахад component-ийг DOM-оос, түүний state-ийг хамт устгана. Хадгалах бол `hidden` хэрэглэ.
```

### Дүгнэлт

`const [isOpen, setIsOpen] = useState(false)` ба
`setIsOpen((open) => !open)` — toggle-ийн үндэс. Нэг boolean-оос текст,
сум, `aria-expanded`-ийг тооцоол. `&&` устгадаг, `hidden` нуудаг.
Бие биеэ үгүйсгэдэг олон boolean-ыг нэг state болго.
""",
            initial_code=files(
                (
                    "FaqItem.jsx",
                    """\
// TODO 1: isOpen boolean state үүсгэ — эхэндээ хаалттай.
// TODO 2: товч дарахад нээж, дахин дарахад хаа (toggle).
//         Товчинд aria-expanded={isOpen} өг.
// TODO 3: хариултыг зөвхөн нээлттэй үед харуул, сумыг ▸ / ▾ болгож соль.
export default function FaqItem({ question, answer }) {
  return (
    <li className="faq-item">
      <h2>
        <button type="button" className="faq-question">
          <span aria-hidden="true">▸</span> {question}
        </button>
      </h2>
      <p className="faq-answer">{answer}</p>
    </li>
  );
}
""",
                ),
                (
                    "App.jsx",
                    """\
// Энэ файлыг өөрчлөх шаардлагагүй — FaqItem.jsx дээр ажиллана.
import FaqItem from "./FaqItem";

const faqs = [
  {
    id: 1,
    question: "Хүргэлт хэд хоног болох вэ?",
    answer: "Улаанбаатар хотод 24 цагийн дотор, орон нутагт 3–5 хоногт хүргэнэ.",
  },
  {
    id: 2,
    question: "Барааг буцааж болох уу?",
    answer: "Савлагааг нь задлаагүй бол 7 хоногийн дотор буцааж болно.",
  },
  {
    id: 3,
    question: "Ямар төлбөрийн хэлбэр байдаг вэ?",
    answer: "QPay, банкны карт, эсвэл хүргэлтийн үед бэлнээр төлнө.",
  },
];

export default function App() {
  return (
    <main className="faq">
      <h1>Түгээмэл асуулт</h1>
      <ul className="faq-list">
        {faqs.map((faq) => (
          <FaqItem key={faq.id} question={faq.question} answer={faq.answer} />
        ))}
      </ul>
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
.faq {
  max-width: 560px;
}

.faq-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.faq-item {
  margin-bottom: 8px;
  border: 1px solid #dfe6da;
  border-radius: 10px;
  background: #fff;
}

.faq-item h2 {
  margin: 0;
  font-size: 1rem;
}

.faq-question {
  width: 100%;
  padding: 12px 16px;
  border: 0;
  border-radius: 10px;
  background: none;
  text-align: left;
  font-weight: 600;
}

.faq-answer {
  margin: 0;
  padding: 0 16px 14px 36px;
  color: #55624f;
}
""",
                    True,
                ),
                ("main.jsx", MAIN_WITH_CSS, True),
                ("index.html", HTML, True),
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 12 минут

«Ногоон сагс»-ын түгээмэл асуултын хуудсан дээр бүх хариулт үргэлж
дэлгэгдсэн байна. `FaqItem.jsx`-ийг асуулт дээр дарахад хариулт нь нээгдэж,
дахин дарахад хаагддаг болго. Дэлгэц уншигч ашигладаг хүн ч нээлттэй
эсэхийг мэдэж байх ёстой.
""",
                tests=(
                    test(
                        "Эхэндээ хариулт харагдахгүй",
                        """
const FaqItem = mod("./FaqItem").default;
render(<ul><FaqItem question="Дэлгүүр хэдэд нээдэг вэ?" answer="Өдөр бүр 09:00–21:00 цагт." /></ul>);
expect(screen.getByRole("button", { name: /Дэлгүүр хэдэд нээдэг/ })).toBeInTheDocument();
const answer = screen.queryByText(/09:00/);
if (answer) expect(answer).not.toBeVisible();
""",
                    ),
                    test(
                        "Асуулт дээр дарахад хариулт гарч, дахин дарахад нуугдана",
                        """
const FaqItem = mod("./FaqItem").default;
render(<ul><FaqItem question="Дэлгүүр хэдэд нээдэг вэ?" answer="Өдөр бүр 09:00–21:00 цагт." /></ul>);
const button = screen.getByRole("button", { name: /Дэлгүүр хэдэд нээдэг/ });
await user.click(button);
expect(screen.getByText(/09:00/)).toBeVisible();
await user.click(button);
const answer = screen.queryByText(/09:00/);
if (answer) expect(answer).not.toBeVisible();
""",
                    ),
                    test(
                        "Товчны aria-expanded нь нээлттэй эсэхийг заана",
                        """
const FaqItem = mod("./FaqItem").default;
render(<ul><FaqItem question="Дэлгүүр хэдэд нээдэг вэ?" answer="Өдөр бүр 09:00–21:00 цагт." /></ul>);
const button = screen.getByRole("button", { name: /Дэлгүүр хэдэд нээдэг/ });
expect(button).toHaveAttribute("aria-expanded", "false");
await user.click(button);
expect(button).toHaveAttribute("aria-expanded", "true");
await user.click(button);
expect(button).toHaveAttribute("aria-expanded", "false");
""",
                    ),
                    test(
                        "Асуулт бүр бие даан нээгдэнэ",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: /буцааж болох/ }));
expect(screen.getByText(/7 хоногийн дотор/)).toBeVisible();
for (const text of [/24 цагийн дотор/, /QPay/]) {
  const other = screen.queryByText(text);
  if (other) expect(other).not.toBeVisible();
}
""",
                    ),
                ),
                tips="""\
- `import { useState } from "react";` ба
  `const [isOpen, setIsOpen] = useState(false);` — component-ийн эхэнд.
- Товчинд `onClick={() => setIsOpen((open) => !open)}` ба
  `aria-expanded={isOpen}`.
- Хариулт: `{isOpen && <p className="faq-answer">{answer}</p>}`. Сум:
  `{isOpen ? "▾" : "▸"}`.
- `FaqItem` бүр өөрийн state-тэй тул нэгийг нээхэд бусад нь хаалттай
  хэвээр — нэмэлт код хэрэггүй.
""",
                solution=solution(
                    FaqItem_jsx="""\
import { useState } from "react";

export default function FaqItem({ question, answer }) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <li className="faq-item">
      <h2>
        <button
          type="button"
          className="faq-question"
          aria-expanded={isOpen}
          onClick={() => setIsOpen((open) => !open)}
        >
          <span aria-hidden="true">{isOpen ? "▾" : "▸"}</span> {question}
        </button>
      </h2>
      {isOpen && <p className="faq-answer">{answer}</p>}
    </li>
  );
}
"""
                ),
            ),
        ),
        # --- 6 ------------------------------------------------------------------
        LessonSpec(
            title="Объект state ба immutability",
            slug="object-state",
            description="Объект state-ийг spread-ээр шинээр үүсгэж шинэчлэх, nested объект засах.",
            duration=1020,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Холбоотой утгуудыг нэг объект state-д хадгалах
- Объектыг дотроос нь өөрчлөх (mutation) яагаад ажиллахгүйг ойлгох
- Spread-ээр шинэ объект үүсгэж шинэчлэх
- Nested (давхар) объектыг түвшин бүрээр нь хуулж шинэчлэх

### Яагаад чухал вэ

Хэрэглэгчийн профайл, тохиргоо, захиалгын мэдээлэл — холбоотой олон утгыг
нэг объектод хадгалах нь тохиромжтой. Гэхдээ объект state бол хамгийн
түгээмэл алдааны эх үүсвэр: объектыг «засаад» `setState` дуудсан ч
дэлгэц өөрчлөгдөхгүй. Модул 0-д «React-д өгөгдлийг дотроос нь өөрчлөхгүй»
гэж хэлсний учрыг одоо харна.

### Объект state

```jsx
const [user, setUser] = useState({
  name: "Бат",
  city: "Улаанбаатар",
  level: 1,
});
```

### Mutation — ажиллахгүй

```jsx
function handleLevelUp() {
  user.level = user.level + 1; // ❌ хуучин объектыг өөрчиллөө
  setUser(user);               // ижил объект → React юу ч хийхгүй
}
```

React шинэ state-ийг хуучинтай нь `Object.is`-ээр харьцуулдаг. `user` нь
**ижил объект** (зөвхөн дотор нь өөрчлөгдсөн) тул React «өөрчлөлт алга»
гэж үзээд дахин render хийхгүй. Бүр муу нь: дараа нь өөр state
өөрчлөгдөж дахин render хийгдэхэд нууцаар өөрчилсөн утга гэнэт гарч
ирнэ. Ийм алдааг олоход маш хэцүү.

Тиймээс state дахь объект, массивыг props шиг **зөвхөн уншдаг** гэж үз.

### Spread-ээр шинэ объект

```jsx
function handleLevelUp() {
  setUser({ ...user, level: user.level + 1 }); // ✅ шинэ объект
}
```

`...user` бүх талбарыг хуулж, ард нь бичсэн `level` дарж бичнэ. Объект
шинэ тул React өөрчлөлтийг анзаарч дахин render хийнэ. Updater хэлбэрээр:

```jsx
setUser((prev) => ({ ...prev, level: prev.level + 1 }));
```

Arrow функцээс объект буцаахдаа **хаалтанд** хийнэ: `=> ({ … })`.
Хаалтгүй бол `{` нь функцийн бие гэж ойлгогдоод синтакс алдаа гарна.

### Spread-ээ мартвал

```jsx
setUser({ level: 2 }); // ❌ name, city алга боллоо
```

`useState`-ийн setter объектуудыг **нийлүүлдэггүй** — өгсөн объектоор
бүтнээр нь солино. (Хуучин class component-ийн `this.setState` нийлүүлдэг
байсан тул хуучин нийтлэлүүдэд андуурал бий.)

### Nested объект

```jsx
const [profile, setProfile] = useState({
  name: "Бат",
  settings: { theme: "Цайвар", notifications: true },
});

// ❌ гадна объект шинэ ч дотор талынхыг өөрчилсөн — mutation
profile.settings.theme = "Харанхуй";
setProfile({ ...profile });

// ✅ өөрчлөх замын дагуух объект бүрийг шинээр үүсгэнэ
setProfile({
  ...profile,
  settings: { ...profile.settings, theme: "Харанхуй" },
});
```

Spread нь **гүехэн** (shallow) хуулбар — зөвхөн нэг түвшин. `{ ...profile }`
доторх `settings` нь хуучин объект руу заасан хэвээр. Эхний хувилбар
дэлгэцэн дээр ажиллаж байгаа мэт харагдах ч анхны өгөгдлийг эвдэж,
хожим `memo` (Модул 12) зэрэгт олоход хэцүү алдаа үүсгэнэ.

Давхарлалт гүн байвал state-ээ хавтгай болгох, эсвэл хэд хэдэн state-д
хуваах талаар бод. Бодит төслүүдэд **Immer** (`use-immer`) сангаар
`draft.settings.theme = "Харанхуй"` гэж «өөрчилж» бичээд, цаана нь шинэ
объект үүсгүүлдэг.

### Нэг объект уу, олон state уу?

- Хамт өөрчлөгдөж, хамт хэрэглэгддэг утгууд (профайл, байрлал `{ x, y }`)
  → нэг объект.
- Бие биеэсээ хамааралгүй утгууд (`isOpen`, `count`) → тусдаа `useState`.

### Бодит төсөлд

Redux, Zustand, TanStack Query зэрэг бүх түгээмэл сан immutable
шинэчлэлт дээр суурилдаг: «шинэ объект = өөрчлөгдсөн». Энэ дүрмийг
одооноос дадал болговол тэдгээрийг сурахад амар.

```jsx
const [user, setUser] = useState({ name: "Бат", age: 17 });

function handleBirthday() {
  user.age = 18;
  setUser(user);
}
```

```quiz
Дээрх товчийг дарахад дэлгэцэнд нас юу болох вэ?
- [ ] 18
- [x] 17 хэвээр
- [ ] Алдаа гарна
> `setUser`-т ижил объект очсон тул React дахин render хийхгүй. `setUser({ ...user, age: 18 })` гэж бич.
```

```quiz
`user = { name: "Бат", age: 17 }` үед `setUser({ age: 18 })` дуудсаны дараа `user.name` юу болох вэ?
- [ ] «Бат»
- [x] `undefined`
- [ ] `null`
> `useState`-ийн setter нийлүүлдэггүй, бүтнээр нь солино. Spread-ээр бусад талбарыг хуул.
```

```quiz
`user = { name, address: { city, street } }` үед зөвхөн хотыг «Дархан» болгох зөв код аль вэ?
- [ ] `setUser({ ...user, city: "Дархан" })`
- [ ] `setUser({ ...user, address: { city: "Дархан" } })`
- [x] `setUser({ ...user, address: { ...user.address, city: "Дархан" } })`
> Эхнийх нь дээд түвшинд шинэ `city` нэмнэ, хоёр дахь нь `street`-ийг устгана.
```

### Дүгнэлт

State дахь объектыг хэзээ ч дотроос нь өөрчлөхгүй — `{ ...obj, key: value }`
гэж шинээр үүсгэнэ. Setter нийлүүлдэггүй тул spread-ээ бүү март. Nested
объектод өөрчлөх замын дагуух түвшин бүрийг хуулна.
""",
            initial_code=vite(
                """\
import { useState } from "react";
import { initialProfile } from "./profile";

const avatars = ["🦊", "🐼", "🐯", "🐸"];

export default function App() {
  const [profile, setProfile] = useState(initialProfile);

  // 🐞 Handler-ууд объектыг дотроос нь өөрчилж (mutation) байна — товч
  //    дарахад дэлгэц шинэчлэгдэхгүй. Spread-ээр ШИНЭ объект үүсгэж зас.
  function handleAvatar(avatar) {
    profile.avatar = avatar;
    setProfile(profile);
  }

  function handleLevelUp() {
    profile.level = profile.level + 1;
    setProfile(profile);
  }

  function handleTheme() {
    profile.settings.theme = profile.settings.theme === "Цайвар" ? "Харанхуй" : "Цайвар";
    setProfile(profile);
  }

  function handleNotifications() {
    profile.settings.notifications = !profile.settings.notifications;
    setProfile({ ...profile }); // дэлгэц шинэчлэгдэнэ… гэхдээ зөв үү? 🤔
  }

  const { settings } = profile;

  return (
    <main className={settings.theme === "Харанхуй" ? "profile dark" : "profile"}>
      <div className="avatar" role="img" aria-label="Профайлын зураг">
        {profile.avatar}
      </div>
      <h1>{profile.name}</h1>
      <p>Түвшин: {profile.level}</p>
      <p>Горим: {settings.theme}</p>
      <p>Мэдэгдэл: {settings.notifications ? "Асаалттай" : "Унтраалттай"}</p>

      <h2>Зураг сонгох</h2>
      <div className="row">
        {avatars.map((avatar) => (
          <button
            key={avatar}
            type="button"
            aria-pressed={profile.avatar === avatar}
            onClick={() => handleAvatar(avatar)}
          >
            {avatar}
          </button>
        ))}
      </div>

      <h2>Тохиргоо</h2>
      <div className="row">
        <button type="button" onClick={handleLevelUp}>
          ⬆️ Түвшин ахих
        </button>
        <button type="button" onClick={handleTheme}>
          🌓 Горим солих
        </button>
        <button type="button" onClick={handleNotifications}>
          🔔 Мэдэгдэл асаах/унтраах
        </button>
      </div>
    </main>
  );
}
""",
                locked={
                    "profile.js": """\
export const initialProfile = {
  name: "Бат",
  avatar: "🦊",
  level: 1,
  settings: {
    theme: "Цайвар",
    notifications: true,
  },
};
"""
                },
                css=BASE_CSS
                + """
.profile {
  max-width: 480px;
  padding: 20px;
  border-radius: 16px;
  background: #fff;
  border: 1px solid #dfe6da;
}

.profile.dark {
  background: #1f2a1c;
  color: #eef5ea;
}

.profile h2 {
  margin: 20px 0 8px;
  font-size: 1rem;
}

.profile p {
  margin: 4px 0;
}

.avatar {
  font-size: 3.5rem;
}

button[aria-pressed="true"] {
  border-color: #2f6b1f;
  background: #dff0d6;
}
""",
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐ · 15 минут

Профайл засварлагчийн товчнууд ажиллахгүй байна: зураг, түвшин, горим
солигдохгүй. Харин «Мэдэгдэл» дарахад өмнөх бүх өөрчлөлт гэнэт гарч
ирнэ — «Хөтөч» дээр туршаад учрыг нь бодоорой. Дөрвөн handler-ийг
объектыг дотроос нь өөрчлөхгүйгээр, шинэ объект үүсгэдэг болгож зас.
""",
                tests=(
                    test(
                        "Зураг сонгоход профайлын зураг солигдоно",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: "🐼" }));
expect(screen.getByRole("img", { name: "Профайлын зураг" })).toHaveTextContent("🐼");
""",
                    ),
                    test(
                        "«Түвшин ахих» түвшинг 1-ээр нэмж, бусад мэдээллийг хэвээр үлдээнэ",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: /Түвшин ахих/ }));
await user.click(screen.getByRole("button", { name: /Түвшин ахих/ }));
expect(screen.text()).toContain("Түвшин: 3");
expect(screen.getByRole("heading", { name: "Бат" })).toBeInTheDocument();
expect(screen.getByRole("img", { name: "Профайлын зураг" })).toHaveTextContent("🦊");
""",
                    ),
                    test(
                        "Горим, мэдэгдлийн тохиргоо бие биедээ нөлөөлөхгүй солигдоно",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: /Горим солих/ }));
expect(screen.text()).toContain("Горим: Харанхуй");
expect(screen.text()).toContain("Мэдэгдэл: Асаалттай");
await user.click(screen.getByRole("button", { name: /Мэдэгдэл/ }));
expect(screen.text()).toContain("Горим: Харанхуй");
expect(screen.text()).toContain("Мэдэгдэл: Унтраалттай");
""",
                    ),
                    test(
                        "Анхны initialProfile объект (settings-ийг оруулаад) өөрчлөгдөхгүй",
                        """
const { initialProfile } = mod("./profile");
const before = JSON.stringify(initialProfile);
render(<App />);
await user.click(screen.getByRole("button", { name: "🐯" }));
await user.click(screen.getByRole("button", { name: /Түвшин ахих/ }));
await user.click(screen.getByRole("button", { name: /Горим солих/ }));
await user.click(screen.getByRole("button", { name: /Мэдэгдэл/ }));
expect(JSON.stringify(initialProfile)).toBe(before);
""",
                    ),
                ),
                tips="""\
- `setProfile({ ...profile, avatar })` — эхлээд spread, дараа нь өөрчлөх
  талбар. `avatar: avatar`-ыг товчоор `avatar` гэж бичиж болно.
- Updater хэлбэрээр: `setProfile((prev) => ({ ...prev, level: prev.level + 1 }))`
  — буцаах объектыг хаалтанд хийхээ бүү март.
- `settings` доторх талбарыг өөрчлөхдөө хоёр түвшнийг хоёуланг нь хуулна:
  `settings: { ...profile.settings, theme: … }`.
- `setProfile({ ...profile })` гадна объектыг шинэчилсэн ч `settings`-ийг
  дотроос нь өөрчилсөн хэвээр — сүүлийн тест үүнийг барина.
""",
                solution=solution(
                    App_jsx="""\
import { useState } from "react";
import { initialProfile } from "./profile";

const avatars = ["🦊", "🐼", "🐯", "🐸"];

export default function App() {
  const [profile, setProfile] = useState(initialProfile);

  function handleAvatar(avatar) {
    setProfile({ ...profile, avatar });
  }

  function handleLevelUp() {
    setProfile((prev) => ({ ...prev, level: prev.level + 1 }));
  }

  function handleTheme() {
    setProfile({
      ...profile,
      settings: {
        ...profile.settings,
        theme: profile.settings.theme === "Цайвар" ? "Харанхуй" : "Цайвар",
      },
    });
  }

  function handleNotifications() {
    setProfile({
      ...profile,
      settings: {
        ...profile.settings,
        notifications: !profile.settings.notifications,
      },
    });
  }

  const { settings } = profile;

  return (
    <main className={settings.theme === "Харанхуй" ? "profile dark" : "profile"}>
      <div className="avatar" role="img" aria-label="Профайлын зураг">
        {profile.avatar}
      </div>
      <h1>{profile.name}</h1>
      <p>Түвшин: {profile.level}</p>
      <p>Горим: {settings.theme}</p>
      <p>Мэдэгдэл: {settings.notifications ? "Асаалттай" : "Унтраалттай"}</p>

      <h2>Зураг сонгох</h2>
      <div className="row">
        {avatars.map((avatar) => (
          <button
            key={avatar}
            type="button"
            aria-pressed={profile.avatar === avatar}
            onClick={() => handleAvatar(avatar)}
          >
            {avatar}
          </button>
        ))}
      </div>

      <h2>Тохиргоо</h2>
      <div className="row">
        <button type="button" onClick={handleLevelUp}>
          ⬆️ Түвшин ахих
        </button>
        <button type="button" onClick={handleTheme}>
          🌓 Горим солих
        </button>
        <button type="button" onClick={handleNotifications}>
          🔔 Мэдэгдэл асаах/унтраах
        </button>
      </div>
    </main>
  );
}
"""
                ),
            ),
        ),
        # --- 7 ------------------------------------------------------------------
        LessonSpec(
            title="Массив state: нэмэх, устгах, засах",
            slug="massiv-state",
            description="Массив state-д spread, filter, map-аар immutable байдлаар нэмэх, хасах, засах.",
            duration=1080,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Массив state-д зүйл нэмэх, хасах, засах
- Массивыг өөрчилдөг ба шинэ массив буцаадаг аргуудыг ялгах
- `map` + spread-ээр массив доторх нэг объектыг шинэчлэх
- Шинэ зүйлд давтагдашгүй id олгох

### Яагаад чухал вэ

Хийх ажлын жагсаалт, сагс, сэтгэгдэл, мэдэгдэл — бараг бүх апп
жагсаалттай бөгөөд хэрэглэгч түүнд нэмж, хасаж, засдаг. Массив ч бас
объект тул өмнөх хичээлийн дүрэм энд бүрэн хамаарна: дотроос нь
өөрчлөхгүй, шинээр үүсгэнэ.

### Өөрчилдөг ба шинээр үүсгэдэг аргууд

| Үйлдэл | ❌ Массивыг өөрчилнө | ✅ Шинэ массив буцаана |
|---|---|---|
| Нэмэх | `push`, `unshift` | `[...arr, x]`, `[x, ...arr]` |
| Хасах | `pop`, `shift`, `splice` | `filter`, `slice` |
| Солих | `arr[i] = x`, `splice` | `map` |
| Эрэмбэлэх | `sort`, `reverse` | `[...arr].sort()`, `toSorted()`, `toReversed()` |

`todos.push(x); setTodos(todos);` гэвэл ижил массив очих тул React
өөрчлөлтийг анзаарахгүй — объекттой яг адил.

### Нэмэх

```jsx
let nextId = 4; // component-оос ГАДНА

export default function TodoList() {
  const [todos, setTodos] = useState(initialTodos);

  function handleAdd(title) {
    setTodos([...todos, { id: nextId++, title, done: false }]); // төгсгөлд
    // эхэнд нэмэх бол: [{ … }, ...todos]
  }
  // …
}
```

### Давтагдашгүй id

Модул 2-т үзсэнээр жагсаалтын key тогтвортой, давтагдашгүй байх ёстой.
Id-г зүйл **үүсэх үед** нэг удаа олгоно:

- `nextId`-г component **дотор** бичвэл render бүрт 4-өөс эхэлж давтагдана.
- `todos.length + 1` — нэгийг устгаад шинийг нэмэхэд давхцана.
- `Date.now()` — нэг миллисекундэд хоёр удаа дуудвал давхцана.
- Бодит төсөлд id-г ихэвчлэн сервер өгдөг, эсвэл `crypto.randomUUID()`.

### Хасах: filter

```jsx
function handleDelete(id) {
  setTodos(todos.filter((todo) => todo.id !== id));
}
```

«Id нь энэ биш бүгдийг үлдээ» гэсэн утгатай. `filter` шинэ массив
буцаана.

### Засах: map

Массив доторх нэг объектыг өөрчлөхдөө `map`-аар бүх элементийг дамжиж,
**таарсныг нь шинэ объектоор** солиод бусдыг нь хэвээр үлдээнэ:

```jsx
function handleToggle(id) {
  setTodos(
    todos.map((todo) => (todo.id === id ? { ...todo, done: !todo.done } : todo)),
  );
}
```

Түгээмэл алдаа — шинэ массив үүсгэсэн ч доторх объектыг өөрчлөх:

```jsx
setTodos(
  todos.map((todo) => {
    if (todo.id === id) todo.done = !todo.done; // ❌ хуучин объектыг өөрчиллөө
    return todo;
  }),
);
```

Дэлгэц шинэчлэгдэх ч анхны өгөгдөл эвдэрнэ — өмнөх хичээлийн nested
объекттой ижил алдаа. Массив гадна, объектууд дотор нь — хоёр түвшин.

### Дунд нь оруулах, эрэмбэлэх

```jsx
// index байрлалд оруулах
setTodos([...todos.slice(0, index), newTodo, ...todos.slice(index)]);

// эрэмбэлэх — эхлээд хуулна
setTodos([...todos].sort((a, b) => a.title.localeCompare(b.title)));
// эсвэл: todos.toSorted((a, b) => a.title.localeCompare(b.title))
```

### Updater хэлбэр

Нэг handler-т хэд хэдэн удаа, эсвэл хожим шинэчлэх бол updater хэрэглэ:

```jsx
setTodos((prev) => [...prev, newTodo]);
setTodos((prev) => prev.filter((todo) => todo.id !== id));
```

### Checkbox-ийг state-ээр удирдах — товчхон

Даалгаварт checkbox-ийн чагтыг state-ээс авна:

```jsx
<input type="checkbox" checked={todo.done} onChange={() => handleToggle(todo.id)} />
```

`checked` нь юу харуулахыг state-ээс авна, `onChange` нь дарахад
дуудагдана. Ингэснээр checkbox state-ээ дагана — state өөрчлөгдөхгүй бол
чагт ч өөрчлөгдөхгүй. Форм элементийг state-ээр удирдахыг Модул 4-т
дэлгэрэнгүй үзнэ.

```quiz
Аль нь `todos` массивыг өөрчлөхгүй вэ?
- [ ] `todos.push(newTodo)`
- [ ] `todos.sort()`
- [x] `todos.filter((todo) => !todo.done)`
- [ ] `todos.splice(0, 1)`
> `filter`, `map`, `slice`, spread шинэ массив буцаадаг. `push`, `sort`, `splice` анхныхыг өөрчилнө.
```

```jsx
const [items, setItems] = useState(["А"]);

function handleClick() {
  setItems([...items, "Б"]);
  setItems([...items, "В"]);
}
```

```quiz
Дээрх товчийг дарсны дараа `items` юу болох вэ?
- [ ] `["А", "Б", "В"]`
- [x] `["А", "В"]`
- [ ] `["А", "Б"]`
> Хоёулаа агшны `["А"]`-аас тооцож, сүүлийнх нь ялна. `setItems((prev) => [...prev, "Б"])` гэвэл гурвуулаа үлдэнэ.
```

```quiz
`nextId`-г яагаад component-оос гадна зарладаг вэ?
- [ ] Component дотор `let` зарлаж болдоггүй
- [x] Component доторх хувьсагч render бүрт шинээр үүсч, анхны утгаасаа эхэлдэг
- [ ] Гадна зарласан хувьсагч илүү хурдан
> Локал хувьсагч render хооронд хадгалагдахгүй (useState хичээл). Модулийн хувьсагч апп ажиллах хооронд нэг л байна.
```

### Дүгнэлт

Нэмэх — `[...arr, x]`, хасах — `filter`, засах — `map` + `{ ...item }`.
`push`, `splice`, `sort`, `arr[i] =`-ийг state дээр хэрэглэхгүй. Шинэ
зүйлд давтагдашгүй id-г үүсэх үед нь олго.
""",
            initial_code=vite(
                """\
import { useState } from "react";
import { initialTodos, suggestions } from "./todos";

let nextId = 4;

export default function App() {
  const [todos, setTodos] = useState(initialTodos);

  function handleAdd(title) {
    // TODO 1: { id: nextId++, title, done: false }-ийг жагсаалтын ТӨГСГӨЛД нэм.
  }

  function handleDelete(id) {
    // TODO 2: id-тай ажлыг жагсаалтаас хас (filter).
  }

  function handleToggle(id) {
    // TODO 3: id-тай ажлын done-ийг эсрэгээр нь соль (map + spread).
  }

  function handleClearDone() {
    // TODO 4: дууссан бүх ажлыг хас.
  }

  return (
    <main className="todos">
      <h1>📝 Хийх ажил</h1>

      <p className="hint">Санал болгох:</p>
      <div className="row">
        {suggestions.map((title) => (
          <button key={title} type="button" onClick={() => handleAdd(title)}>
            + {title}
          </button>
        ))}
      </div>

      <ul className="todo-list">
        {todos.map((todo) => (
          <li key={todo.id} className={todo.done ? "done" : ""}>
            <label>
              <input
                type="checkbox"
                checked={todo.done}
                onChange={() => handleToggle(todo.id)}
              />
              {todo.title}
            </label>
            <button
              type="button"
              aria-label={`Устгах: ${todo.title}`}
              onClick={() => handleDelete(todo.id)}
            >
              🗑️
            </button>
          </li>
        ))}
      </ul>

      <button type="button" onClick={handleClearDone}>
        Дууссаныг цэвэрлэх
      </button>
    </main>
  );
}
""",
                locked={
                    "todos.js": """\
export const initialTodos = [
  { id: 1, title: "React хичээл үзэх", done: true },
  { id: 2, title: "useState дасгал хийх", done: false },
  { id: 3, title: "Төсөл эхлүүлэх", done: false },
];

export const suggestions = ["Талх авах", "Номын санд очих", "Гүйлтээр хичээллэх"];
"""
                },
                css=BASE_CSS
                + """
.todos {
  max-width: 520px;
}

.hint {
  margin: 0 0 8px;
  color: #55624f;
}

.todo-list {
  margin: 20px 0;
  padding: 0;
  list-style: none;
}

.todo-list li {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 8px;
  padding: 8px 12px;
  border: 1px solid #dfe6da;
  border-radius: 10px;
  background: #fff;
}

.todo-list label {
  display: flex;
  align-items: center;
  gap: 10px;
}

.todo-list li.done label {
  color: #8a9785;
  text-decoration: line-through;
}

.todo-list li button {
  border: 0;
  background: none;
}
""",
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐ · 15 минут

Хийх ажлын жагсаалтын markup бэлэн, харин дөрвөн handler хоосон байна.
Санал болгосон товчоор ажил нэмэх, 🗑️-ээр устгах, checkbox-оор
дууссан/дуусаагүй болгох, дууссан бүхнийг цэвэрлэх үйлдлийг массивыг
өөрчлөхгүйгээр бич. Нэг ажлыг хоёр удаа нэмээд Console-д key-ийн
анхааруулга гарахгүй эсэхийг шалгаарай.
""",
                tests=(
                    test(
                        "Санал болгосон товч шинэ ажлыг жагсаалтын төгсгөлд нэмнэ",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: "+ Талх авах" }));
const items = screen.getAllByRole("listitem");
expect(items).toHaveLength(4);
expect(items[3]).toHaveTextContent("Талх авах");
expect(screen.getByRole("checkbox", { name: /Талх авах/ })).not.toBeChecked();
""",
                    ),
                    test(
                        "Нэг ажлыг хоёр удаа нэмэхэд давтагдашгүй key-тэй хоёр мөр үүснэ",
                        """
render(<App />);
const add = screen.getByRole("button", { name: "+ Номын санд очих" });
await user.click(add);
await user.click(add);
expect(screen.getAllByRole("listitem")).toHaveLength(5);
expect(logs.some((entry) => entry.text.includes("same key") || entry.text.includes('unique "key"'))).toBe(false);
""",
                    ),
                    test(
                        "Устгах товч зөвхөн тухайн ажлыг хасна",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: "Устгах: useState дасгал хийх" }));
expect(screen.getAllByRole("listitem")).toHaveLength(2);
expect(screen.queryByText("useState дасгал хийх")).toBeNull();
expect(screen.text()).toContain("React хичээл үзэх");
expect(screen.text()).toContain("Төсөл эхлүүлэх");
""",
                    ),
                    test(
                        "Checkbox дарахад ажлын төлөв солигдож, анхны өгөгдөл өөрчлөгдөхгүй",
                        """
const { initialTodos } = mod("./todos");
render(<App />);
const box = screen.getByRole("checkbox", { name: /useState дасгал/ });
await user.click(box);
expect(box).toBeChecked();
expect(screen.getByRole("checkbox", { name: /React хичээл/ })).toBeChecked();
await user.click(box);
expect(box).not.toBeChecked();
await user.click(screen.getByRole("checkbox", { name: /Төсөл эхлүүлэх/ }));
expect(screen.getByRole("checkbox", { name: /Төсөл эхлүүлэх/ })).toBeChecked();
expect(initialTodos.map((todo) => todo.done)).toEqual([true, false, false]);
""",
                    ),
                    test(
                        "«Дууссаныг цэвэрлэх» зөвхөн дууссан ажлуудыг хасна",
                        """
render(<App />);
await user.click(screen.getByRole("checkbox", { name: /Төсөл эхлүүлэх/ }));
await user.click(screen.getByRole("button", { name: "Дууссаныг цэвэрлэх" }));
const items = screen.getAllByRole("listitem");
expect(items).toHaveLength(1);
expect(items[0]).toHaveTextContent("useState дасгал хийх");
""",
                    ),
                ),
                tips="""\
- Нэмэх: `setTodos([...todos, { … }])`. Id-д `nextId++` — одоогийн утгыг
  өгөөд дараагийнхыг нэгээр ахиулна.
- Устгах: `filter`-ийн нөхцөл «үлдэх» элементүүдийг сонгоно:
  `todo.id !== id`.
- Солих: `map` дотор таарсан элементэд `{ ...todo, done: !todo.done }`,
  бусдад нь `todo`-г өөрийг нь буцаа. `todo.done = …` гэж өөрчилбөл анхны
  өгөгдөл эвдэрч, тест унана.
- Цэвэрлэх: мөн л `filter` — «дуусаагүйг нь үлдээ».
""",
                solution=solution(
                    App_jsx="""\
import { useState } from "react";
import { initialTodos, suggestions } from "./todos";

let nextId = 4;

export default function App() {
  const [todos, setTodos] = useState(initialTodos);

  function handleAdd(title) {
    setTodos([...todos, { id: nextId++, title, done: false }]);
  }

  function handleDelete(id) {
    setTodos(todos.filter((todo) => todo.id !== id));
  }

  function handleToggle(id) {
    setTodos(todos.map((todo) => (todo.id === id ? { ...todo, done: !todo.done } : todo)));
  }

  function handleClearDone() {
    setTodos(todos.filter((todo) => !todo.done));
  }

  return (
    <main className="todos">
      <h1>📝 Хийх ажил</h1>

      <p className="hint">Санал болгох:</p>
      <div className="row">
        {suggestions.map((title) => (
          <button key={title} type="button" onClick={() => handleAdd(title)}>
            + {title}
          </button>
        ))}
      </div>

      <ul className="todo-list">
        {todos.map((todo) => (
          <li key={todo.id} className={todo.done ? "done" : ""}>
            <label>
              <input
                type="checkbox"
                checked={todo.done}
                onChange={() => handleToggle(todo.id)}
              />
              {todo.title}
            </label>
            <button
              type="button"
              aria-label={`Устгах: ${todo.title}`}
              onClick={() => handleDelete(todo.id)}
            >
              🗑️
            </button>
          </li>
        ))}
      </ul>

      <button type="button" onClick={handleClearDone}>
        Дууссаныг цэвэрлэх
      </button>
    </main>
  );
}
"""
                ),
            ),
        ),
        # --- 8 ------------------------------------------------------------------
        LessonSpec(
            title="Уламжлагдсан утга",
            slug="ulamjlagdsan-utga",
            description="Тооцоолж болох утгыг state-д хадгалахгүй, render үеэр state-ээс тооцоолох.",
            duration=960,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Тооцоолж болох утгыг state-д хадгалахгүй байх
- Render үеэр state, props-оос утга тооцоолох (derived value)
- Давхар хадгалсан state хэрхэн зөрдгийг таних
- Хамгийн бага state-ийг сонгох гурван асуулт

### Яагаад чухал вэ

Нэг өгөгдлийг хоёр газар хадгалбал эрт орой хэзээ нэгэн цагт **зөрнө**:
хэн нэгэн нэгийг нь шинэчлээд нөгөөг нь мартана. Модул 0-ийн DOM
тоологчид `#count`-ийг шинэчлээд `#parity`-г мартах нь яг ийм алдаа
байсан. React-д үүнээс сэргийлэх энгийн дүрэм бий: **тооцоолж болох
бүхнийг тооцоол, бүү хадгал.**

### Давхар state-ийн алдаа

```jsx
const [items, setItems] = useState(initialItems);
const [count, setCount] = useState(initialItems.length); // 🐞

function handleAdd(item) {
  setItems([...items, item]);
  setCount(count + 1);
}

function handleDelete(id) {
  setItems(items.filter((item) => item.id !== id));
  // setCount-ийг мартжээ → тоо буруу
}
```

`count` бол үнэндээ `items.length`. Тусад нь хадгалах шаардлагагүй:

```jsx
const [items, setItems] = useState(initialItems);
const count = items.length; // ✅ render бүрт шинээр тооцоологдоно
```

`items` өөрчлөгдөх бүрт component дахин render хийгдэж, `count` өөрөө зөв
гарна. Шинэчлэх код ч, мартах эрсдэл ч үгүй. Иймэрхүү утгыг
**уламжлагдсан утга** (derived value) гэнэ.

### Түгээмэл жишээнүүд

```jsx
// Бүтэн нэр
const fullName = firstName + " " + lastName;

// Сагсны нийт дүн, хоосон эсэх
const total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
const isEmpty = cart.length === 0;

// Шүүлтүүр — state-д зөвхөн шүүлтүүрийн НЭР
const [filter, setFilter] = useState("all");
const visibleTodos = todos.filter((todo) => {
  if (filter === "done") return todo.done;
  if (filter === "active") return !todo.done;
  return true;
});
```

Шүүлтүүрийн хувьд state-д шүүгдсэн массивыг биш, **шүүлтүүрийн нэрийг**
(`"all"`) хадгална. Шүүгдсэн жагсаалт нь `todos` ба `filter`-ээс
тооцоологдоно — аль нь ч өөрчлөгдсөн жагсаалт зөв гарна.

### State байх ёстой юу? — гурван асуулт

Утга бүрийн хувьд асуу:

1. **Цаг хугацааны явцад өөрчлөгддөг үү?** Үгүй бол энгийн тогтмол.
2. **Эцгээс props-оор ирдэг үү?** Тийм бол state биш.
3. **Одоо байгаа state, props-оос тооцоолж болох уу?** Тийм бол state
   биш — тооцоол.

Гурвуулаа «үгүй» бол л state болгоно. Жишээ нь дэлгүүрийн хуудсанд:
барааны жагсаалт — өгөгдөл; хайлтын үг, сонгосон ангилал — state;
шүүгдсэн бараанууд, олдсон барааны тоо — тооцоолно.

### Объектын хуулбарыг биш, id-г хадгал

```jsx
const [selectedProduct, setSelectedProduct] = useState(products[0]); // 🐞 хуулбар
```

Барааны үнэ, үлдэгдэл өөрчлөгдөхөд `selectedProduct` хуучин хуулбар
хэвээр үлдэнэ. Оронд нь:

```jsx
const [selectedId, setSelectedId] = useState(1);
const selectedProduct = products.find((product) => product.id === selectedId);
```

### Гүйцэтгэлд санаа зовох уу?

Ихэнх тооцоо (хэдэн зуун элементийн `filter`, `reduce`) микросекунд
зарцуулна — render бүрт тооцоход асуудалгүй. Үнэхээр удаан тооцоонд
`useMemo` (Модул 6) бий. Эхлээд энгийнээр тооцоол, хэмжээд удаан байвал
дараа нь хурдасга.

### Бодит төсөлд

Энэ дүрэм бүх түвшинд хамаарна: Модул 4-т формын алдааг утгуудаас нь
тооцоолно, Модул 5-д state-ийг `useEffect`-ээр «синк» хийх нь яагаад
буруу болохыг үзнэ. Code review-д «энэ state хэрэгтэй юу?» гэдэг асуулт
хамгийн их гардаг.

```quiz
Онлайн дэлгүүрийн хайлтын хуудсанд алийг нь state-д хадгалах вэ? (Хэд хэдэн зөв хариулттай)
- [x] Хайлтын үг
- [x] Сонгосон ангилал
- [ ] Хайлтад таарсан бараанууд
- [ ] Олдсон барааны тоо
> Таарсан бараанууд, тэдгээрийн тоо нь барааны жагсаалт, хайлтын үг, ангиллаас тооцоологдоно.
```

```jsx
const [cart, setCart] = useState([]);
const [total, setTotal] = useState(0);

function handleAdd(product) {
  setCart([...cart, product]);
  setTotal(total + product.price);
}

function handleClear() {
  setCart([]);
}
```

```quiz
Дээрх кодод ямар асуудал байна вэ?
- [ ] `setCart([])` хоосон массив өгч болохгүй
- [x] Сагсыг хоослоход `total` хуучин дүнгээрээ үлдэнэ — `total`-ийг `cart`-аас тооцоолох ёстой
- [ ] Асуудалгүй
> `const total = cart.reduce((sum, item) => sum + item.price, 0);` гэвэл хоосон сагсанд өөрөө 0 болно.
```

```quiz
Жагсаалтаас сонгосон барааг санахад юуг state-д хадгалах нь хамгийн зөв вэ?
- [ ] Барааны объектын хуулбар
- [x] Барааны `id`
- [ ] Барааны нэр ба үнэ
> Id-аар жагсаалтаас хайж олбол бараа шинэчлэгдэхэд сонголт ч үргэлж шинэ мэдээлэлтэй байна.
```

### Дүгнэлт

State-ийг хамгийн бага байлга. Тоо, нийлбэр, шүүгдсэн жагсаалт, бүтэн
нэр зэргийг render үеэр state-ээс тооцоол. Давхар хадгалсан state
хэзээ нэгэн цагт зөрнө. Объектын хуулбарын оронд id хадгал.
""",
            initial_code=vite(
                """\
import { useState } from "react";
import { formatPrice, initialItems } from "./data";

const filters = [
  { value: "all", label: "Бүгд" },
  { value: "todo", label: "Авах" },
  { value: "bought", label: "Авсан" },
];

export default function App() {
  const [items, setItems] = useState(initialItems);
  const [filter, setFilter] = useState("all");

  // 🐞 Дараах гурав нь items, filter-ээс ТООЦООЛЖ болох утгууд. Давхар
  //    хадгалсан тул хоорондоо зөрж байна. State-ээс хасаад энгийн
  //    хувьсагчаар тооцоол.
  const [boughtCount, setBoughtCount] = useState(1);
  const [remaining, setRemaining] = useState(25000);
  const [visibleItems, setVisibleItems] = useState(initialItems);

  function handleToggle(id) {
    setItems(items.map((item) => (item.id === id ? { ...item, bought: !item.bought } : item)));
    setBoughtCount(boughtCount + 1); // буцаахад ч нэмэгдэнэ 🐞
    // remaining, visibleItems-ийг шинэчлэхээ мартжээ 🐞
  }

  function handleFilter(nextFilter) {
    setFilter(nextFilter);
    if (nextFilter === "all") setVisibleItems(items);
    if (nextFilter === "todo") setVisibleItems(items.filter((item) => !item.bought));
    if (nextFilter === "bought") setVisibleItems(items.filter((item) => item.bought));
  }

  return (
    <main className="shopping">
      <h1>🛒 Худалдан авалт</h1>
      <p className="summary">
        {items.length} бараанаас {boughtCount} нь авсан · Үлдсэн: {formatPrice(remaining)}
      </p>

      <div className="row" role="group" aria-label="Шүүлтүүр">
        {filters.map((option) => (
          <button
            key={option.value}
            type="button"
            aria-pressed={filter === option.value}
            onClick={() => handleFilter(option.value)}
          >
            {option.label}
          </button>
        ))}
      </div>

      <ul className="list">
        {visibleItems.map((item) => (
          <li key={item.id} className={item.bought ? "bought" : ""}>
            <label>
              <input
                type="checkbox"
                checked={item.bought}
                onChange={() => handleToggle(item.id)}
              />
              {item.emoji} {item.name}
            </label>
            <span>{formatPrice(item.price)}</span>
          </li>
        ))}
      </ul>
    </main>
  );
}
""",
                locked={
                    "data.js": """\
export const initialItems = [
  { id: 1, name: "Талх", emoji: "🍞", price: 2500, bought: true },
  { id: 2, name: "Сүү", emoji: "🥛", price: 3200, bought: false },
  { id: 3, name: "Алим", emoji: "🍎", price: 2800, bought: false },
  { id: 4, name: "Өндөг", emoji: "🥚", price: 6500, bought: false },
  { id: 5, name: "Бяслаг", emoji: "🧀", price: 12500, bought: false },
];

export function formatPrice(price) {
  return price.toLocaleString("en-US") + "₮";
}
"""
                },
                css=BASE_CSS
                + """
.shopping {
  max-width: 480px;
}

.summary {
  font-weight: 600;
}

button[aria-pressed="true"] {
  border-color: #2f6b1f;
  background: #dff0d6;
}

.list {
  margin: 16px 0 0;
  padding: 0;
  list-style: none;
}

.list li {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
  padding: 8px 12px;
  border: 1px solid #dfe6da;
  border-radius: 10px;
  background: #fff;
}

.list label {
  display: flex;
  align-items: center;
  gap: 10px;
}

.list li.bought label {
  color: #8a9785;
  text-decoration: line-through;
}
""",
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐ · 15 минут

Худалдан авалтын жагсаалт дээр барааг «авсан» гэж тэмдэглэхэд чагт ч,
тоо ч, үлдсэн зардал ч зөв шинэчлэгдэхгүй байна. Учир нь `items`,
`filter`-ээс тооцоолж болох гурван утгыг state-д давхар хадгалсан.
Тэдгээрийг state-ээс хасаж, render бүрт тооцоолдог болго. Эцэст нь
component-д хоёр л `useState` үлдэх ёстой.
""",
                tests=(
                    test(
                        "Авсан барааны тоо «5 бараанаас N нь авсан» гэж зөв гарна",
                        """
render(<App />);
expect(screen.text()).toContain("5 бараанаас 1 нь авсан");
const milk = screen.getByRole("checkbox", { name: /Сүү/ });
await user.click(milk);
expect(milk).toBeChecked();
expect(screen.text()).toContain("5 бараанаас 2 нь авсан");
await user.click(milk);
expect(milk).not.toBeChecked();
expect(screen.text()).toContain("5 бараанаас 1 нь авсан");
""",
                    ),
                    test(
                        "Үлдсэн зардлыг авах бараануудын үнээр тооцно",
                        """
render(<App />);
expect(screen.text()).toContain("Үлдсэн: 25,000₮");
await user.click(screen.getByRole("checkbox", { name: /Бяслаг/ }));
expect(screen.text()).toContain("Үлдсэн: 12,500₮");
await user.click(screen.getByRole("checkbox", { name: /Талх/ }));
expect(screen.text()).toContain("Үлдсэн: 15,000₮");
""",
                    ),
                    test(
                        "«Авсан» шүүлтүүр зөвхөн авсан барааг харуулна",
                        """
render(<App />);
await user.click(screen.getByRole("checkbox", { name: /Алим/ }));
await user.click(screen.getByRole("button", { name: "Авсан" }));
expect(screen.getAllByRole("listitem")).toHaveLength(2);
expect(screen.text()).toContain("Алим");
expect(screen.text()).not.toContain("Сүү");
await user.click(screen.getByRole("button", { name: "Бүгд" }));
expect(screen.getAllByRole("listitem")).toHaveLength(5);
""",
                    ),
                    test(
                        "«Авах» шүүлтүүр дээр бараа авахад жагсаалтаас шууд алга болно",
                        """
render(<App />);
await user.click(screen.getByRole("button", { name: "Авах" }));
expect(screen.getAllByRole("listitem")).toHaveLength(4);
await user.click(screen.getByRole("checkbox", { name: /Сүү/ }));
expect(screen.getAllByRole("listitem")).toHaveLength(3);
expect(screen.queryByRole("checkbox", { name: /Сүү/ })).toBeNull();
""",
                    ),
                ),
                tips="""\
- `boughtCount`, `remaining`, `visibleItems`-ийн `useState` мөрүүд болон
  тэдгээрийг шинэчилдэг бүх `set…` дуудлагыг устга.
- Тоо: авсан бараануудыг `filter`-ээр шүүгээд `.length`.
- Үлдсэн зардал: `reduce` — зөвхөн авах бараануудын `price`-ийг нэм,
  эхлэл утга `0`.
- Харагдах жагсаалт: `filter`-ийн утгаас хамаарч `items.filter(…)`.
  Ингэвэл `handleFilter` зөвхөн `setFilter` дуудна, `handleToggle` зөвхөн
  `setItems`.
""",
                solution=solution(
                    App_jsx="""\
import { useState } from "react";
import { formatPrice, initialItems } from "./data";

const filters = [
  { value: "all", label: "Бүгд" },
  { value: "todo", label: "Авах" },
  { value: "bought", label: "Авсан" },
];

export default function App() {
  const [items, setItems] = useState(initialItems);
  const [filter, setFilter] = useState("all");

  const boughtCount = items.filter((item) => item.bought).length;
  const remaining = items
    .filter((item) => !item.bought)
    .reduce((sum, item) => sum + item.price, 0);
  const visibleItems = items.filter((item) => {
    if (filter === "todo") return !item.bought;
    if (filter === "bought") return item.bought;
    return true;
  });

  function handleToggle(id) {
    setItems(items.map((item) => (item.id === id ? { ...item, bought: !item.bought } : item)));
  }

  return (
    <main className="shopping">
      <h1>🛒 Худалдан авалт</h1>
      <p className="summary">
        {items.length} бараанаас {boughtCount} нь авсан · Үлдсэн: {formatPrice(remaining)}
      </p>

      <div className="row" role="group" aria-label="Шүүлтүүр">
        {filters.map((option) => (
          <button
            key={option.value}
            type="button"
            aria-pressed={filter === option.value}
            onClick={() => setFilter(option.value)}
          >
            {option.label}
          </button>
        ))}
      </div>

      <ul className="list">
        {visibleItems.map((item) => (
          <li key={item.id} className={item.bought ? "bought" : ""}>
            <label>
              <input
                type="checkbox"
                checked={item.bought}
                onChange={() => handleToggle(item.id)}
              />
              {item.emoji} {item.name}
            </label>
            <span>{formatPrice(item.price)}</span>
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
        # --- 9 ------------------------------------------------------------------
        LessonSpec(
            title="Төсөл: Сагс",
            slug="tusul-sags",
            description="State, үйл явдал, массив шинэчлэлт, уламжлагдсан утгаар «Ногоон сагс»-ын сагсыг бүтээх.",
            duration=2400,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Модул 3-т сурсан бүхнээ нэг апп-д нэгтгэх
- Сагсны логикийг React-гүй цэвэр функцэд салгах
- Массив state-ийг immutable шинэчилж, нийт дүнг тооцоолох
- Handler-уудыг props-оор component-уудад дамжуулах

### Яагаад чухал вэ

Сагс бол онлайн дэлгүүрийн зүрх: бараа нэмэх, тоог өөрчлөх, хасах, нийт
дүн. Модул 2-т бүтээсэн каталог одоо зөвхөн харуулдаг — энэ төслөөр түүнд
харилцан үйлдэл нэмнэ. Сургалтын төгсгөлд (Модул 14) энэ сагсыг Context,
reducer, серверийн өгөгдөлтэй болгож өргөтгөнө.

### Юу бүтээх вэ

- **Толгой хэсэг:** «🛒 Сагсанд: 3 ширхэг».
- **Барааны тор:** карт бүрт «Сагсанд нэмэх» товч.
- **Сагс:** мөр бүрт `−` / тоо / `+`, мөрийн дүн, ✕. Доор нь
  «Нийт: 10,200₮», «Сагсыг хоослох». Хоосон бол «Сагс хоосон байна».

### Component-уудын мод ба өгөгдлийн урсгал

```text
App                  ← cart state, handler-ууд, count, total
├── Header           ← count
└── main
    ├── ProductList  ← products, onAdd
    └── Cart         ← items, total, onIncrease, onDecrease, onRemove, onClear
        └── CartItem …
```

State **нэг** газар — `App`-д байна. Өгөгдөл props-оор доош, үйл явдал
handler-оор дээш урсана: `CartItem`-ийн «+» дарахад `onIncrease(id)` →
`App`-ийн `handleIncrease` → `setCart` → бүх мод дахин render хийгдэнэ.

### Файлын бүтэц

```text
App.jsx
cart.js             ← сагсны цэвэр функцууд
products.js 🔒      ← 6 бараа
format.js 🔒        ← formatPrice()
styles.css          ← бэлэн загвар
components/
├── Header.jsx      ← бэлэн
├── ProductList.jsx
├── Cart.jsx
└── CartItem.jsx
```

### Сагсны өгөгдлийн хэлбэр

```jsx
[
  { id: 1, name: "Банана", price: 3500, emoji: "🍌", category: "Жимс", quantity: 2 },
  { id: 4, name: "Сүү", price: 3200, emoji: "🥛", category: "Сүүн бүтээгдэхүүн", quantity: 1 },
]
```

Барааны мэдээллийг хуулаад `quantity` нэмнэ. Энэ төсөлд барааны мэдээлэл
өөрчлөгддөггүй тул хуулах нь хамгийн энгийн. Үнэ нь серверээс өөрчлөгддөг
бодит апп-д (Модул 9) өмнөх хичээлийн зөвлөснөөр зөвхөн `{ id, quantity }`
хадгалж, бусдыг нь барааны жагсаалтаас хайна.

### Алхам 1 — cart.js: цэвэр функцууд

Сагсны бүх логикийг React-гүй, энгийн функц болгон бичнэ: оролт нь хуучин
сагс, гаралт нь **шинэ** сагс. Ийм функцийг дангаар нь шалгахад амар
(эхний хоёр тест яг үүнийг хийнэ), Модул 7-ийн `useReducer`-т ч шууд
хэрэглэгдэнэ.

- `addToCart(cart, product)` — `find`-ээр сагсанд байгаа эсэхийг шалга.
  Байвал `map`-аар тэр мөрийн `quantity`-г +1, үгүй бол
  `[...cart, { ...product, quantity: 1 }]`.
- `changeQuantity(cart, id, delta)` — `map`-аар `quantity + delta`, дараа
  нь `filter`-ээр `quantity > 0` мөрүүдийг үлдээ.
- `removeFromCart(cart, id)` — `filter`.
- `cartTotal(cart)`, `cartCount(cart)` — `reduce`, эхлэл утга `0`.

### Алхам 2 — App: state ба handler

```jsx
const [cart, setCart] = useState([]);

function handleAdd(product) {
  setCart((prev) => addToCart(prev, product));
}
```

Updater хэлбэр хурдан дараалан дарахад ч зөв ажиллана (4-р хичээл).
Бусад handler-ыг ижил загвараар бич: `changeQuantity(prev, id, 1)`,
`changeQuantity(prev, id, -1)`, `removeFromCart(prev, id)`, хоослох нь
`setCart([])`. `count`, `total`-ийг state-д биш, `cartCount(cart)`,
`cartTotal(cart)`-аар тооцоол (8-р хичээл).

### Алхам 3 — ProductList

«Сагсанд нэмэх» товчинд `onClick={() => onAdd(product)}` (1-р хичээл).
Хаалтыг мартвал render бүрт бүх бараа сагсанд орох гэж оролдоно.

### Алхам 4 — CartItem

Гурван товчинд `onDecrease(item.id)`, `onIncrease(item.id)`,
`onRemove(item.id)`. Товчнууд `aria-label`-тай: «−» тэмдэгт дэлгэц
уншигчид юу ч хэлэхгүй, «Банана: нэгээр хасах» бол ойлгомжтой.

### Алхам 5 — Cart

- `items.length === 0` бол `<p className="empty">Сагс хоосон байна</p>`.
- Эс бөгөөс `<ul className="cart-list">` дотор `CartItem` (key!),
  `<p className="total">Нийт: {formatPrice(total)}</p>`, «Сагсыг
  хоослох» товч.
- Тернарын нэг салаанд олон элемент буцаахдаа `<>…</>`-д боо.
- `Cart` handler-уудыг өөрөө ашиглахгүй ч `CartItem`-д дамжуулна.

### Шалгах

«Ажиллуулах»-аас өмнө «Хөтөч» дээр:

- Нэг барааг гурав дарахад сагсанд нэг л мөр гарч, тоо нь 3 болж байна уу?
- `−`-ийг тоо 1 үед дарахад мөр алга болж байна уу?
- Толгой хэсгийн тоо, нийт дүн үргэлж сагстай таарч байна уу?
- Console-д `key`-ийн анхааруулга алга уу?

### Нэмэлт сорилт

Тест шаардахгүй ч оролдоод үзээрэй:

- 50,000₮-өөс дээш захиалгад «🚚 Үнэгүй хүргэлт» гэж харуул — бас л
  уламжлагдсан утга.
- Барааны карт дээр сагсанд байгаа тоог нь «Сагсанд: 2» гэж харуул.
- Нэг бараанаас 10-аас илүү нэмэгдэхгүй болго.

```quiz
Толгой хэсгийн «Сагсанд: N ширхэг»-ийн N-ийг хэрхэн гаргах нь зөв бэ?
- [ ] `const [count, setCount] = useState(0)` гээд нэмэх, хасах бүрт шинэчлэх
- [x] `App`-д `const count = cartCount(cart)` гэж тооцоолоод `Header`-т дамжуулах
- [ ] `Header` дотор тусдаа сагс хадгалах
> Тоо нь сагснаас тооцоологддог — тусад нь хадгалбал хэзээ нэгэн цагт зөрнө.
```

```quiz
`CartItem`-ийн «+» дарахад юу болох вэ?
- [ ] `CartItem` өөрийн `item.quantity`-г нэмнэ
- [x] `onIncrease(id)` → `App`-ийн `handleIncrease` → `setCart` → `App` ба бүх хүүхэд дахин render
- [ ] `Cart` өөрийн state-ийг шинэчилнэ
> State нь `App`-д. Хүүхэд нь props-оо өөрчилж чадахгүй — зөвхөн handler дуудаж мэдэгдэнэ.
```

```quiz
`addToCart` дотор `existing.quantity += 1; return cart;` гэж бичвэл юу болох вэ?
- [ ] Ажиллана — тоо нэмэгдсэн
- [x] Ижил массив буцаах тул React дахин render хийхгүй, анхны өгөгдөл ч эвдэрнэ
- [ ] Синтакс алдаа гарна
> Массив ба доторх объектыг хоёуланг нь шинээр үүсгэ: `map` + `{ ...item, quantity: item.quantity + 1 }`.
```

### Дүгнэлт

State нэг газар (`App`), логик нь цэвэр функцэд (`cart.js`), тооцоолж
болох бүхэн тооцоологдсон, өгөгдөл доош, үйл явдал дээш урсаж байна.
Дараагийн модульд форм нэмж хэрэглэгчээс мэдээлэл авна.
""",
            initial_code=vite(
                CART_APP_START,
                extra={
                    "cart.js": CART_LOGIC_START,
                    "components/Header.jsx": CART_HEADER,
                    "components/ProductList.jsx": CART_PRODUCT_LIST_START,
                    "components/Cart.jsx": CART_START,
                    "components/CartItem.jsx": CART_ITEM_START,
                },
                locked={"products.js": CART_PRODUCTS, "format.js": CART_FORMAT},
                css=CART_CSS,
                css_locked=False,
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐ · 40 минут

«Заавар» дахь алхмуудыг дагаж «Ногоон сагс»-т сагс нэм. Эхлээд `cart.js`-ийн
цэвэр функцуудыг бичээд (эхний хоёр тест), дараа нь `App`, `ProductList`,
`CartItem`, `Cart`-ыг холбо. `products.js`, `format.js` түгжигдсэн,
`styles.css` бэлэн — хүсвэл өөрийнхөөрөө чимэглээрэй.
""",
                tests=(
                    test(
                        "addToCart шинэ барааг нэмж, байгаа барааных нь тоог нэмэгдүүлнэ",
                        """
const { addToCart } = mod("./cart");
const banana = { id: 1, name: "Банана", price: 3500, emoji: "🍌" };
const milk = { id: 4, name: "Сүү", price: 3200, emoji: "🥛" };
const empty = [];
const one = addToCart(empty, banana);
expect(one).toEqual([{ ...banana, quantity: 1 }]);
expect(empty).toEqual([]);
const two = addToCart(one, banana);
expect(two).toEqual([{ ...banana, quantity: 2 }]);
expect(one[0].quantity).toBe(1);
expect(addToCart(two, milk)).toEqual([{ ...banana, quantity: 2 }, { ...milk, quantity: 1 }]);
""",
                    ),
                    test(
                        "changeQuantity тоог өөрчилж, 0 болсон мөрийг хасна",
                        """
const { changeQuantity } = mod("./cart");
const cart = [
  { id: 1, name: "Банана", price: 3500, emoji: "🍌", quantity: 2 },
  { id: 4, name: "Сүү", price: 3200, emoji: "🥛", quantity: 1 },
];
expect(changeQuantity(cart, 1, 1)[0].quantity).toBe(3);
expect(changeQuantity(cart, 1, -1)[0].quantity).toBe(1);
expect(changeQuantity(cart, 4, -1).map((item) => item.id)).toEqual([1]);
expect(cart[0].quantity).toBe(2);
expect(cart).toHaveLength(2);
""",
                    ),
                    test(
                        "Бараа нэмэхэд сагс, нийт дүн, толгой хэсгийн тоо шинэчлэгдэнэ",
                        """
render(<App />);
const cart = () => within(screen.getByLabelText("Сагс"));
const add = async (name) => {
  const card = within(screen.getByLabelText("Бараанууд")).getByRole("heading", { name }).closest("li");
  await user.click(within(card).getByRole("button", { name: /Сагсанд нэмэх/ }));
};
expect(cart().getByText(/Сагс хоосон байна/)).toBeInTheDocument();
await add("Банана");
await add("Банана");
await add("Сүү");
expect(cart().getAllByRole("listitem")).toHaveLength(2);
expect(cart().text()).toContain("Нийт: 10,200₮");
expect(screen.getByRole("banner")).toHaveTextContent("3 ширхэг");
expect(logs.some((entry) => entry.text.includes('unique "key"'))).toBe(false);
""",
                    ),
                    test(
                        "Сагсны «+», «−» товч тоог өөрчилж, ✕ товч барааг хасна",
                        """
render(<App />);
const cart = () => within(screen.getByLabelText("Сагс"));
const add = async (name) => {
  const card = within(screen.getByLabelText("Бараанууд")).getByRole("heading", { name }).closest("li");
  await user.click(within(card).getByRole("button", { name: /Сагсанд нэмэх/ }));
};
await add("Алим");
await user.click(cart().getByRole("button", { name: /Алим: нэгээр нэмэх/ }));
await user.click(cart().getByRole("button", { name: /Алим: нэгээр нэмэх/ }));
expect(cart().text()).toContain("Нийт: 8,400₮");
await user.click(cart().getByRole("button", { name: /Алим: нэгээр хасах/ }));
expect(cart().text()).toContain("Нийт: 5,600₮");
await add("Талх");
await user.click(cart().getByRole("button", { name: /Алим: устгах/ }));
expect(cart().queryByText(/Алим/)).toBeNull();
expect(cart().text()).toContain("Нийт: 2,500₮");
""",
                    ),
                    test(
                        "«Сагсыг хоослох» сагсыг хоосолж, «Сагс хоосон байна» гэж харуулна",
                        """
render(<App />);
const cart = () => within(screen.getByLabelText("Сагс"));
const add = async (name) => {
  const card = within(screen.getByLabelText("Бараанууд")).getByRole("heading", { name }).closest("li");
  await user.click(within(card).getByRole("button", { name: /Сагсанд нэмэх/ }));
};
await add("Банана");
await add("Бяслаг");
await user.click(cart().getByRole("button", { name: /Сагсыг хоослох/ }));
expect(cart().queryAllByRole("listitem")).toHaveLength(0);
expect(cart().getByText(/Сагс хоосон байна/)).toBeInTheDocument();
expect(screen.getByRole("banner")).toHaveTextContent("0 ширхэг");
""",
                    ),
                ),
                tips="""\
- `addToCart`: `cart.find((item) => item.id === product.id)` — олдвол
  `map`-аар тэр мөрийг `{ ...item, quantity: item.quantity + 1 }` болго,
  олдохгүй бол spread-ээр төгсгөлд нэм.
- `changeQuantity`: `map`-ийн араас `.filter((item) => item.quantity > 0)`
  гэж гинжилбэл 0 болсон мөр өөрөө хасагдана.
- `App`: `useState([])`, handler бүр `setCart((prev) => …(prev, …))`,
  `const total = cartTotal(cart);`.
- `Cart` handler-уудыг өөрөө хэрэглэхгүй ч `CartItem` бүрт дамжуулна.
  Хоосон эсэхийг `{items.length === 0 ? (…) : (<>…</>)}` гэж шалга.
""",
                solution=files(
                    (
                        "App.jsx",
                        """\
import { useState } from "react";
import { addToCart, cartCount, cartTotal, changeQuantity, removeFromCart } from "./cart";
import Cart from "./components/Cart";
import Header from "./components/Header";
import ProductList from "./components/ProductList";
import { products } from "./products";

export default function App() {
  const [cart, setCart] = useState([]);

  function handleAdd(product) {
    setCart((prev) => addToCart(prev, product));
  }

  function handleIncrease(id) {
    setCart((prev) => changeQuantity(prev, id, 1));
  }

  function handleDecrease(id) {
    setCart((prev) => changeQuantity(prev, id, -1));
  }

  function handleRemove(id) {
    setCart((prev) => removeFromCart(prev, id));
  }

  function handleClear() {
    setCart([]);
  }

  const count = cartCount(cart);
  const total = cartTotal(cart);

  return (
    <div className="page">
      <Header count={count} />
      <main className="layout">
        <ProductList products={products} onAdd={handleAdd} />
        <Cart
          items={cart}
          total={total}
          onIncrease={handleIncrease}
          onDecrease={handleDecrease}
          onRemove={handleRemove}
          onClear={handleClear}
        />
      </main>
    </div>
  );
}
""",
                    ),
                    (
                        "cart.js",
                        """\
export function addToCart(cart, product) {
  const existing = cart.find((item) => item.id === product.id);
  if (existing) {
    return cart.map((item) =>
      item.id === product.id ? { ...item, quantity: item.quantity + 1 } : item,
    );
  }
  return [...cart, { ...product, quantity: 1 }];
}

export function changeQuantity(cart, id, delta) {
  return cart
    .map((item) => (item.id === id ? { ...item, quantity: item.quantity + delta } : item))
    .filter((item) => item.quantity > 0);
}

export function removeFromCart(cart, id) {
  return cart.filter((item) => item.id !== id);
}

export function cartTotal(cart) {
  return cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

export function cartCount(cart) {
  return cart.reduce((sum, item) => sum + item.quantity, 0);
}
""",
                    ),
                    (
                        "components/ProductList.jsx",
                        """\
import { formatPrice } from "../format";

export default function ProductList({ products, onAdd }) {
  return (
    <section className="products" aria-label="Бараанууд">
      <h2>Бараанууд</h2>
      <ul className="grid">
        {products.map((product) => (
          <li key={product.id} className="card">
            <div className="card-emoji">{product.emoji}</div>
            <h3>{product.name}</h3>
            <p className="price">{formatPrice(product.price)}</p>
            <button type="button" className="add" onClick={() => onAdd(product)}>
              Сагсанд нэмэх
            </button>
          </li>
        ))}
      </ul>
    </section>
  );
}
""",
                    ),
                    (
                        "components/CartItem.jsx",
                        """\
import { formatPrice } from "../format";

export default function CartItem({ item, onIncrease, onDecrease, onRemove }) {
  return (
    <li className="cart-item">
      <span>
        {item.emoji} {item.name}
      </span>
      <button
        type="button"
        className="remove"
        aria-label={`${item.name}: устгах`}
        onClick={() => onRemove(item.id)}
      >
        ✕
      </button>
      <div className="qty">
        <button
          type="button"
          aria-label={`${item.name}: нэгээр хасах`}
          onClick={() => onDecrease(item.id)}
        >
          −
        </button>
        <span>{item.quantity}</span>
        <button
          type="button"
          aria-label={`${item.name}: нэгээр нэмэх`}
          onClick={() => onIncrease(item.id)}
        >
          +
        </button>
      </div>
      <span className="line-total">{formatPrice(item.price * item.quantity)}</span>
    </li>
  );
}
""",
                    ),
                    (
                        "components/Cart.jsx",
                        """\
import { formatPrice } from "../format";
import CartItem from "./CartItem";

export default function Cart({ items, total, onIncrease, onDecrease, onRemove, onClear }) {
  return (
    <aside className="cart" aria-label="Сагс">
      <h2>Сагс</h2>
      {items.length === 0 ? (
        <p className="empty">Сагс хоосон байна 🧺</p>
      ) : (
        <>
          <ul className="cart-list">
            {items.map((item) => (
              <CartItem
                key={item.id}
                item={item}
                onIncrease={onIncrease}
                onDecrease={onDecrease}
                onRemove={onRemove}
              />
            ))}
          </ul>
          <p className="total">Нийт: {formatPrice(total)}</p>
          <button type="button" className="clear" onClick={onClear}>
            Сагсыг хоослох
          </button>
        </>
      )}
    </aside>
  );
}
""",
                    ),
                ),
            ),
        ),
    ],
)
