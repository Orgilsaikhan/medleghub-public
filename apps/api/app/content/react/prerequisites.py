"""Модул 0 — Эхлэхийн өмнө.

Засварлагчтай танилцаж, React-д хамгийн их хэрэглэгддэг JavaScript-ийг
(задлалт, spread, массивын аргууд, модуль, async) хурдан сэргээнэ. Сүүлийн
хичээл нь DOM-оор UI бичих хүндрэлийг мэдрүүлж, React яагаад хэрэгтэйг
харуулна.
"""

from app.content.react.common import files, solution, test, vite
from app.content.types import ExerciseSpec, LessonSpec, ModuleSpec
from app.models.enums import LessonLanguage

JSX = LessonLanguage.JSX

CONSOLE_PAGE = "<p>Энэ хичээлийн үр дүн доорх Console-д гарна.</p>\n"

PREREQUISITES = ModuleSpec(
    title="Модул 0 — Эхлэхийн өмнө",
    description="Засварлагчтай танилцаж, React-д хэрэгтэй JavaScript-ийг сэргээнэ.",
    lessons=[
        LessonSpec(
            title="Сургалтад тавтай морил",
            slug="tavtai-moril",
            description="Юу сурах, засварлагч хэрхэн ажилладаг, анхны өөрчлөлт.",
            duration=420,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Сургалтын бүтэц, эцэст нь юу бүтээхээ мэдэх
- Засварлагчийн хэсгүүдтэй танилцах: файлууд, «Заавар», «Хөтөч», тест, console
- Анхны кодоо өөрчилж «Ажиллуулах» дарах

### Урьдчилсан мэдлэг

React бол JavaScript-ийн сан. Тиймээс энэ сургалт JavaScript-ийн үндэс
(функц, объект, массив, `import`/`export`, Promise) болон HTML & CSS-ийг
мэддэг гэж үзнэ. Мэдэхгүй бол эхлээд
[JavaScript үндэс](/courses/javascript-undes),
[HTML & CSS үндэс](/courses/html-css-undes) сургалтуудыг үзээрэй.

Мэддэг бол шууд үргэлжлүүл. Модул 0 нь React-д хамгийн их хэрэглэгддэг
JavaScript-ийг хурдан сэргээнэ.

### Юу сурах вэ

| Шат | Сэдэв |
|---|---|
| Үндэс | JSX, component, props, жагсаалт |
| Харилцан үйлдэл | state, үйл явдал, форм |
| Гадаад ертөнц | effect, hook, API, routing |
| Ахисан | архитектур, React 19, гүйцэтгэл, тест |

Сургалтын төгсгөлд **«Ногоон сагс»** нэртэй онлайн хүнсний дэлгүүр бүтээнэ:
барааны каталог, хайлт, сагс, төлбөр тооцоо, нэвтрэлт, админ хэсэг.

### Засварлагч хэрхэн ажилладаг вэ

- **Файлууд** зүүн талд tab-аар байна. Кодоо `App.jsx` дээр бичнэ. 🔒
  тэмдэгтэй файл (`main.jsx`, `index.html`) түгжигдсэн: жинхэнэ React
  төсөлд байдаг файлууд боловч одоохондоо өөрчлөх шаардлагагүй.
- **«Заавар»** tab-д одоо уншиж буй энэ текст байна.
- **«Хөтөч»** tab-д таны апп жинхэнэ хөтөч дээрх шиг харагдана.
- **«Ажиллуулах»** (эсвэл `Ctrl + Enter`) нь кодыг дахин ачаалж, зэрэг
  **тестүүдийг** шалгана. Бүх тест давбал хичээл дуусна.
- **Console** хэсэгт `console.log`-ийн гаралт, React-ийн анхааруулга, алдаа
  гарна.
- Гацвал **«Тусламж»** дарж зөвлөгөө, жишиг шийдлийг харна.

### Хэрхэн сурах вэ

Хичээл бүрт эхлээд уншиж, жишээ кодыг өөрчилж ажиллуулж үзнэ. Дараа нь
шалгах асуултад хариулж, даалгавраа хийнэ. Тест унавал мессежийг нь
анхааралтай уншаарай — яг юу дутуу байгааг хэлдэг. Алдаа гаргах нь
сурахын нэг хэсэг.

### Нэршил

React-ийн баримт бичиг болон бодит төслүүд англи нэр хэрэглэдэг. Тиймээс
component, хувьсагчийн нэрийг англиар бичнэ (`ProductCard`, `count`),
харин дэлгэцэнд гарах текстийг монголоор.

```quiz
«Ажиллуулах» товч юу хийдэг вэ?
- [ ] Кодыг хадгалж, дараагийн хичээл рүү шилжинэ
- [x] Кодыг «Хөтөч» дээр дахин ачаалж, бүх тестийг шалгана
- [ ] Кодыг багшид илгээж шалгуулна
> Тестүүд таны кодыг автоматаар шалгаж, аль шаардлага биелээгүйг хэлнэ.
```

### Дүгнэлт

Засварлагчийн зүүн тал нь код ба тест, баруун тал нь заавар, хөтөч ба
console. Одоо доорх даалгавраар анхны өөрчлөлтөө хийцгээе.
""",
            initial_code=vite(
                """\
export default function App() {
  return <h1>Hello!</h1>;
}
"""
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐ · 2 минут

`App.jsx` доторх гарчгийг **Сайн уу, React!** болгож өөрчлөөд
«Ажиллуулах» дар. Дараа нь «Хөтөч» tab-аас үр дүнгээ хар.
""",
                tests=(
                    test(
                        "Гарчиг «Сайн уу, React!» гэж бичигдсэн",
                        """
render(<App />);
expect(screen.getByRole("heading", { level: 1 }).textContent.trim()).toBe("Сайн уу, React!");
""",
                    ),
                    test(
                        "Гарчиг нь <h1> хэвээр байна",
                        """
render(<App />);
expect(screen.getByRole("heading", { level: 1 })).toBeInTheDocument();
""",
                    ),
                ),
                tips="""\
Зөвхөн `<h1>` ба `</h1>`-ийн хоорондох текстийг солино. Таслал, анхаарлын
тэмдэг хүртэл яг таарах ёстой: `Сайн уу, React!`.
""",
                solution=solution(
                    App_jsx="""\
export default function App() {
  return <h1>Сайн уу, React!</h1>;
}
"""
                ),
            ),
        ),
        LessonSpec(
            title="JavaScript сэргээх: функц, объект, задлалт",
            slug="js-funkts-obekt",
            description="Arrow функц, destructuring, spread ба immutability.",
            duration=720,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Arrow функц, template string-ийг сэргээх
- Объект, массивыг задлах (destructuring)
- Spread (`...`)-ээр хуулбар үүсгэх
- Өгөгдлийг өөрчлөхгүйгээр (immutable) шинэчлэх

### Яагаад чухал вэ

React-ийн код бараг бүхэлдээ эдгээр бичлэгээс бүрдэнэ. Жишээ нь нэг мөр:

```jsx
const [count, setCount] = useState(0);
```

энэ бол массив задлалт. `function Card({ title })` нь объект задлалт.
State шинэчлэх бүрт spread хэрэглэнэ. Эдгээрийг сайн мэдэхгүй бол React
«ид шид» шиг санагдана.

### Arrow функц ба template string

```jsx
function double(n) {
  return n * 2;
}

// Ижил утгатай arrow функц — нэг илэрхийлэл бол return шаардахгүй
const doubleArrow = (n) => n * 2;

const greet = (name) => `Сайн уу, ${name}!`;
```

### Задлалт (destructuring)

```jsx
const user = { name: "Бат", city: "Улаанбаатар", age: 17 };

const { name, city } = user;          // объектоос
const [first, second] = ["a", "b"];   // массиваас

// Функцийн параметрт шууд задлах — React-д маш түгээмэл
function describe({ name, age = 18 }) {
  return `${name} (${age})`;
}
```

`age = 18` нь анхдагч утга: объектод `age` байхгүй бол 18 болно.

### Spread — хуулбар үүсгэх

```jsx
const product = { name: "Алим", price: 2800 };

const cheaper = { ...product, price: 2500 };   // шинэ объект
const tags = ["жимс"];
const moreTags = [...tags, "шинэ"];            // шинэ массив
```

`...product` нь бүх талбарыг хуулна, дараа бичсэн `price` нь дарж бичнэ.

### Immutability — өөрчлөхгүй, шинээр үүсгэх

```jsx
// ❌ Анхны объектыг өөрчилнө (mutation)
product.price = 2500;
tags.push("шинэ");

// ✅ Хуучныг хэвээр үлдээж, шинийг үүсгэнэ
const updated = { ...product, price: 2500 };
const added = [...tags, "шинэ"];
```

React нь state өөрчлөгдсөн эсэхийг **хуучин ба шинэ утга нь өөр объект
эсэхээр** шалгадаг. Объектыг дотроос нь өөрчилбөл React өөрчлөлтийг
анзаарахгүй, дэлгэц шинэчлэгдэхгүй. Тиймээс Модул 3-аас эхлэн үргэлж
шинэ объект, шинэ массив үүсгэнэ.

```quiz
Дараах кодын дараа `a.price` хэд вэ?

`const a = { price: 100 }; const b = { ...a, price: 50 };`
- [x] 100
- [ ] 50
- [ ] undefined
> Spread нь шинэ объект үүсгэдэг тул `b`-г өөрчлөх нь `a`-д нөлөөлөхгүй.
```

### Дүгнэлт

Задлалт нь өгөгдлийг хялбар авах, spread нь хуулбар үүсгэх арга. React-д
өгөгдлийг хэзээ ч дотроос нь өөрчлөхгүй — үргэлж шинээр үүсгэнэ.
""",
            initial_code=files(
                (
                    "utils.js",
                    """\
// Гурван функцийг гүйцээ. index.js нь тэдгээрийг ажиллуулж Console-д хэвлэнэ.

export function fullName(user) {
  // TODO: user-ээс firstName, lastName-ийг задалж "Бат Дорж" хэлбэрээр буцаа
}

export function withDiscount(product, percent) {
  // TODO: үнийг percent хувиар хямдруулсан ШИНЭ объект буцаа
}

export function addTag(tags, tag) {
  // TODO: tag-ийг төгсгөлд нь нэмсэн ШИНЭ массив буцаа (push хэрэглэхгүй)
}
""",
                ),
                (
                    "index.js",
                    """\
import { addTag, fullName, withDiscount } from "./utils";

const user = { firstName: "Бат", lastName: "Дорж" };
console.log("Нэр:", fullName(user));

const book = { name: "React ном", price: 30000 };
console.log("Хямдарсан:", withDiscount(book, 20));
console.log("Анхны ном:", book);

const tags = ["react"];
console.log("Шинэ шошгууд:", addTag(tags, "javascript"));
console.log("Анхны шошгууд:", tags);
""",
                    True,
                ),
                ("index.html", CONSOLE_PAGE, True),
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐ · 8 минут

`utils.js` доторх гурван функцийг гүйцээ. Хоёр дахь, гурав дахь функц
анхны объект, массивыг **өөрчлөхгүй**, шинээр үүсгэж буцаах ёстой.
Console-оос `index.js`-ийн хэвлэсэн утгыг шалгаарай.
""",
                tests=(
                    test(
                        "fullName нь нэр, овгийг нэг мөр болгоно",
                        """
const { fullName } = mod("./utils");
expect(fullName({ firstName: "Бат", lastName: "Дорж" })).toBe("Бат Дорж");
expect(fullName({ firstName: "Сараа", lastName: "Мөнх" })).toBe("Сараа Мөнх");
""",
                    ),
                    test(
                        "withDiscount нь хямдарсан шинэ объект буцаана",
                        """
const { withDiscount } = mod("./utils");
expect(withDiscount({ name: "Ном", price: 10000 }, 20)).toEqual({ name: "Ном", price: 8000 });
""",
                    ),
                    test(
                        "withDiscount нь анхны объектыг өөрчлөхгүй",
                        """
const { withDiscount } = mod("./utils");
const book = { name: "Ном", price: 10000 };
const result = withDiscount(book, 50);
expect(book.price).toBe(10000);
expect(result).not.toBe(book);
""",
                    ),
                    test(
                        "addTag нь анхны массивыг өөрчлөхгүйгээр шинэ массив буцаана",
                        """
const { addTag } = mod("./utils");
const tags = ["react"];
const result = addTag(tags, "js");
expect(result).toEqual(["react", "js"]);
expect(tags).toEqual(["react"]);
""",
                    ),
                ),
                tips="""\
- `fullName`: параметрт шууд задалж болно — `function fullName({ firstName, lastName })`,
  дараа нь template string: `` `${firstName} ${lastName}` ``.
- `withDiscount`: `{ ...product, price: … }` — spread нь бусад талбарыг
  хуулж, `price`-ийг шинэ утгаар дарна. Хямдарсан үнэ = `price * (100 - percent) / 100`.
- `addTag`: `push` анхны массивыг өөрчилдөг. Оронд нь `[...tags, tag]`.
""",
                solution=solution(
                    utils_js="""\
export function fullName({ firstName, lastName }) {
  return `${firstName} ${lastName}`;
}

export function withDiscount(product, percent) {
  return { ...product, price: (product.price * (100 - percent)) / 100 };
}

export function addTag(tags, tag) {
  return [...tags, tag];
}
"""
                ),
            ),
        ),
        LessonSpec(
            title="Массивын аргууд: map, filter, find, reduce",
            slug="js-massivyn-arguud",
            description="Жагсаалтыг хувиргах, шүүх, хайх, нэгтгэх.",
            duration=720,
            language=JSX,
            content="""\
### Энэ хичээлээр

- `map`-аар массивыг хувиргах
- `filter`, `find`, `some`-оор шүүх, хайх
- `reduce`-ээр нийлбэр тооцох
- Аргуудыг гинжлэн хэрэглэх

### Яагаад чухал вэ

React-д жагсаалтыг **`map`-аар** render хийнэ, хайлт шүүлтүүрийг
**`filter`-ээр**, сагсны нийт үнийг **`reduce`-ээр** тооцно. Эдгээр арга
бүгд **шинэ** массив (эсвэл утга) буцаадаг, анхныхыг өөрчлөхгүй — яг
React-ийн хүсдэг зүйл.

### map — хувиргах

```jsx
const prices = [1000, 2500, 400];
const withTax = prices.map((price) => price * 1.1);
// [1100, 2750, 440]

const products = [{ name: "Алим" }, { name: "Сүү" }];
const names = products.map((product) => product.name);
// ["Алим", "Сүү"]
```

### filter, find, some — шүүх, хайх

```jsx
const cheap = products.filter((p) => p.price < 3000); // нөхцөл биелсэн БҮГД
const apple = products.find((p) => p.id === 2);       // эхний ОЛДСОН нэг (эсвэл undefined)
const anyEmpty = products.some((p) => p.stock === 0); // ядаж нэг нь биелсэн эсэх
```

### reduce — нэг утга болгох

```jsx
const cart = [
  { price: 2000, qty: 2 },
  { price: 500, qty: 3 },
];

const total = cart.reduce((sum, item) => sum + item.price * item.qty, 0);
// 5500
```

`reduce` нь эхний утга (`0`)-аас эхэлж, элемент бүрийг «хураангуй» руу
нэмнэ.

### Гинжлэх

```jsx
const names = products
  .filter((p) => p.stock > 0)
  .map((p) => p.name);
```

### Эрэмбэлэх — хуулбар дээр

`sort()` нь анхны массивыг өөрчилдөг. Хуулбар дээр эрэмбэл:

```jsx
const sorted = [...products].sort((a, b) => a.price - b.price);
// эсвэл шинэ арга: products.toSorted((a, b) => a.price - b.price)
```

```quiz
Олдохгүй бол `find` юу буцаах вэ?
- [ ] Хоосон массив `[]`
- [x] `undefined`
- [ ] `null`
- [ ] `-1`
> `-1`-ийг `findIndex` буцаадаг, хоосон массивыг `filter` буцаадаг.
```

### Дүгнэлт

`map` хувиргана, `filter` шүүнэ, `find` нэгийг олно, `reduce` нэгтгэнэ.
Бүгд шинэ утга буцааж, анхны массивыг хэвээр үлдээнэ.
""",
            initial_code=files(
                (
                    "utils.js",
                    """\
export function productNames(products) {
  // TODO: барааны нэрсийн массив буцаа
  return [];
}

export function inStock(products) {
  // TODO: stock нь 0-ээс их бараануудыг буцаа
  return [];
}

export function findById(products, id) {
  // TODO: id-тай таарах барааг буцаа
}

export function totalPrice(cart) {
  // TODO: price * qty-ийн нийлбэрийг буцаа
  return 0;
}
""",
                ),
                (
                    "products.js",
                    """\
export const products = [
  { id: 1, name: "Банана", price: 3500, stock: 24 },
  { id: 2, name: "Алим", price: 2800, stock: 40 },
  { id: 3, name: "Брокколи", price: 5200, stock: 0 },
  { id: 4, name: "Сүү", price: 3200, stock: 18 },
];

export const cart = [
  { name: "Банана", price: 3500, qty: 2 },
  { name: "Сүү", price: 3200, qty: 1 },
];
""",
                    True,
                ),
                (
                    "index.js",
                    """\
import { cart, products } from "./products";
import { findById, inStock, productNames, totalPrice } from "./utils";

console.log("Нэрс:", productNames(products));
console.log("Үлдэгдэлтэй:", inStock(products).map((p) => p.name));
console.log("id = 2:", findById(products, 2));
console.log("Сагсны нийт үнэ:", totalPrice(cart));
""",
                    True,
                ),
                ("index.html", CONSOLE_PAGE, True),
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 10 минут

`utils.js` доторх дөрвөн функцийг массивын аргуудаар гүйцээ. `for`
давталт бичих шаардлагагүй — `map`, `filter`, `find`, `reduce` хангалттай.
""",
                tests=(
                    test(
                        "productNames нь нэрсийн массив буцаана",
                        """
const { productNames } = mod("./utils");
const { products } = mod("./products");
expect(productNames(products)).toEqual(["Банана", "Алим", "Брокколи", "Сүү"]);
expect(productNames([])).toEqual([]);
""",
                    ),
                    test(
                        "inStock нь үлдэгдэлтэй бараануудыг л буцаана",
                        """
const { inStock } = mod("./utils");
const { products } = mod("./products");
expect(inStock(products).map((p) => p.id)).toEqual([1, 2, 4]);
""",
                    ),
                    test(
                        "findById нь таарах барааг, эс бөгөөс undefined буцаана",
                        """
const { findById } = mod("./utils");
const { products } = mod("./products");
expect(findById(products, 3).name).toBe("Брокколи");
expect(findById(products, 99)).toBeUndefined();
""",
                    ),
                    test(
                        "totalPrice нь price × qty-ийн нийлбэрийг тооцно",
                        """
const { totalPrice } = mod("./utils");
expect(totalPrice(mod("./products").cart)).toBe(10200);
expect(totalPrice([])).toBe(0);
""",
                    ),
                ),
                tips="""\
- `products.map((p) => p.name)`
- `products.filter((p) => p.stock > 0)`
- `products.find((p) => p.id === id)` — олдохгүй бол өөрөө `undefined` буцаана.
- `cart.reduce((sum, item) => sum + item.price * item.qty, 0)` — `0` эхлэл
  утгыг мартвал хоосон сагсанд алдаа гарна.
""",
                solution=solution(
                    utils_js="""\
export function productNames(products) {
  return products.map((product) => product.name);
}

export function inStock(products) {
  return products.filter((product) => product.stock > 0);
}

export function findById(products, id) {
  return products.find((product) => product.id === id);
}

export function totalPrice(cart) {
  return cart.reduce((sum, item) => sum + item.price * item.qty, 0);
}
"""
                ),
            ),
        ),
        LessonSpec(
            title="Модуль, Promise ба async/await",
            slug="js-module-async",
            description="import/export, fetch, async/await ба алдаа барих.",
            duration=840,
            language=JSX,
            content="""\
### Энэ хичээлээр

- `export`, `import`-оор кодыг файлуудад хуваах
- Promise, `async`/`await`-ийг сэргээх
- `fetch`-ээр өгөгдөл татах, `response.ok`-ийг шалгах
- Энэ сургалтын **дадлагын API**-тай танилцах

### Модуль: export ба import

```jsx
// math.js
export function sum(a, b) {        // нэртэй (named) export
  return a + b;
}
export default function double(n) { // файл бүрт нэг default export
  return n * 2;
}

// app.js
import double, { sum } from "./math";
```

React төсөлд component бүр ихэвчлэн өөрийн файлтай бөгөөд
`export default`-оор гаргадаг.

### Promise ба async/await

Сүлжээний хүсэлт шууд хариу өгдөггүй — **Promise** буцаана. `await` нь
Promise биелэхийг хүлээнэ, зөвхөн `async` функц дотор ажиллана:

```jsx
async function loadUsers() {
  const response = await fetch("/api/users");
  const users = await response.json();
  return users;
}
```

`async` функц өөрөө үргэлж Promise буцаадаг — дуудагч нь бас `await`
хийнэ.

### Алдааг зөв барих

`fetch` нь сервер `404`, `500` буцаасан ч **алдаа шидэхгүй**. Тиймээс
`response.ok`-ийг өөрөө шалгана:

```jsx
async function loadUser(id) {
  const response = await fetch(`/api/users/${id}`);
  if (!response.ok) {
    throw new Error("Хэрэглэгч олдсонгүй");
  }
  return response.json();
}

try {
  const user = await loadUser(99);
} catch (error) {
  console.log(error.message); // "Хэрэглэгч олдсонгүй"
}
```

### Дадлагын API

Энэ засварлагч интернетгүй, хамгаалагдсан орчинд ажилладаг. Оронд нь
бодит сервер шиг ажилладаг **дадлагын API** бий:

| Хаяг | Юу буцаах |
|---|---|
| `GET /api/products` | 10 хүнсний бараа (`id`, `name`, `price`, `category`, `emoji`, `stock`) |
| `GET /api/products/2` | Нэг бараа, байхгүй бол `404` |
| `GET /api/users`, `/api/courses`, `/api/todos`, `/api/posts` | Бусад жишээ өгөгдөл |
| `?q=алим` | Хайлт |
| `?_delay=2000` | Хариуг 2 секунд хоцрооно |
| `?_status=500` | Серверийн алдааг дуурайна |

`POST`, `PATCH`, `DELETE` ч ажиллана — Модул 9-д ашиглана.

```quiz
Сервер `404` буцаахад `await fetch(url)` юу хийх вэ?
- [ ] Алдаа шиднэ
- [x] Ердийн Response буцаана, `response.ok` нь `false` байна
- [ ] `null` буцаана
> Зөвхөн сүлжээ тасрах зэрэгт `fetch` алдаа шиддэг. HTTP алдааг `response.ok`-оор шалгана.
```

### Дүгнэлт

Модуль нь кодыг файлуудад хуваана. `async`/`await` нь асинхрон кодыг
дараалсан мэт бичих боломж олгоно. `fetch`-ийн дараа `response.ok`-ийг
заавал шалга.
""",
            initial_code=files(
                (
                    "api.js",
                    """\
export async function loadProductNames() {
  // TODO: "/api/products"-ээс бараануудыг татаж, нэрсийн массив буцаа
  return [];
}

export async function loadProduct(id) {
  // TODO: `/api/products/${id}`-ээс нэг барааг татаж буцаа.
  // Хариу амжилтгүй бол new Error("Бараа олдсонгүй") шид.
}
""",
                ),
                (
                    "index.js",
                    """\
import { loadProduct, loadProductNames } from "./api";

async function main() {
  console.log("Бараанууд:", await loadProductNames());
  console.log("id = 2:", await loadProduct(2));
  try {
    await loadProduct(999);
  } catch (error) {
    console.log("Алдаа:", error.message);
  }
}

main();
""",
                    True,
                ),
                ("index.html", CONSOLE_PAGE, True),
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 10 минут

`api.js` доторх хоёр функцийг дадлагын API ашиглан гүйцээ. Хариу ирэхэд
0.4 секунд зарцуулагдана — Console-д үр дүн жаахан хоцорч гарна.
""",
                tests=(
                    test(
                        "loadProductNames нь бүх барааны нэрийг буцаана",
                        """
const names = await mod("./api").loadProductNames();
expect(names).toHaveLength(10);
expect(names).toContain("Банана");
""",
                    ),
                    test(
                        "loadProductNames нь /api/products руу хүсэлт илгээнэ",
                        """
await mod("./api").loadProductNames();
expect(api.requests.some((request) => request.path.startsWith("/api/products"))).toBe(true);
""",
                    ),
                    test(
                        "loadProduct нь нэг барааг буцаана",
                        """
const product = await mod("./api").loadProduct(2);
expect(product.name).toBe("Алим");
""",
                    ),
                    test(
                        "Байхгүй бараанд «Бараа олдсонгүй» алдаа шиднэ",
                        """
let error;
try {
  await mod("./api").loadProduct(999);
} catch (caught) {
  error = caught;
}
expect(error && error.message).toBe("Бараа олдсонгүй");
""",
                    ),
                ),
                tips="""\
- `const response = await fetch("/api/products");` дараа нь
  `const products = await response.json();`
- Нэрсийг `products.map((product) => product.name)`-ээр гаргана.
- `loadProduct` дотор `if (!response.ok) throw new Error("Бараа олдсонгүй");`
  — энэ шалгалтгүй бол `404`-ийн хариу `{ error: "Олдсонгүй" }` объект болж
  буцна, алдаа шидэгдэхгүй.
""",
                solution=solution(
                    api_js="""\
export async function loadProductNames() {
  const response = await fetch("/api/products");
  const products = await response.json();
  return products.map((product) => product.name);
}

export async function loadProduct(id) {
  const response = await fetch(`/api/products/${id}`);
  if (!response.ok) {
    throw new Error("Бараа олдсонгүй");
  }
  return response.json();
}
"""
                ),
            ),
        ),
        LessonSpec(
            title="DOM-оор UI бүтээх нь яагаад хэцүү вэ",
            slug="dom-yagaad-hetsuu",
            description="Энгийн JavaScript-ээр тоологч бичиж, React-ийн хэрэгцээг мэдрэх.",
            duration=720,
            language=JSX,
            content="""\
### Энэ хичээлээр

- React-гүйгээр, зөвхөн DOM-оор жижиг UI бичих
- Өгөгдөл (state) ба дэлгэц хоорондоо яаж зөрдгийг мэдрэх
- «Юуг» биш «яаж» гэж бичих (imperative) аргын сул талыг ойлгох

### DOM-оор бичих нь

Тоологч бодъё: тоо, «+1» товч. Энгийн JavaScript-ээр:

```jsx
const countEl = document.getElementById("count");
let count = 0;

document.getElementById("plus").addEventListener("click", () => {
  count = count + 1;
  countEl.textContent = count; // дэлгэцийг ӨӨРӨӨ шинэчилнэ
});
```

Энэ нь **imperative** буюу «хэрхэн» хийхийг алхам алхмаар хэлэх арга:
элементийг ол, утгыг өөрчил, текстийг шинэчил.

### Асуудал: бүх газрыг санах

Одоо «тэгш/сондгой» гэсэн шошго, «тэглэх» товч нэмье. Тоо өөрчлөгдөх
бүрт **хоёр** газрыг шинэчлэх ёстой болно. Товч нэмэгдэх бүрт, өгөгдөл
өөрчлөгдөх газар бүрт бүх холбоотой DOM-оо санаж шинэчилнэ. Нэгийг
мартвал дэлгэц ба өгөгдөл **зөрнө** — хамгийн түгээмэл алдаа.

Том апп (сагс, шүүлтүүр, нэвтрэлт) дээр энэ нь хэдэн зуун газар болно.

### React-ийн шийдэл: UI = f(state)

React-д дэлгэц хэрхэн шинэчлэгдэхийг бичихгүй. Өгөгдөл тухайн мөчид
**ямар харагдахыг** л тодорхойлно — **declarative**:

```jsx
function Counter() {
  const [count, setCount] = useState(0);
  return (
    <>
      <p>Дарсан: {count}</p>
      <p>{count % 2 === 0 ? "Тэгш" : "Сондгой"}</p>
      <button onClick={() => setCount(count + 1)}>+1</button>
    </>
  );
}
```

`count` өөрчлөгдөхөд React бүх холбоотой газрыг өөрөө шинэчилнэ. Энэ
кодыг одоо ойлгох шаардлагагүй — Модул 3-т дэлгэрэнгүй үзнэ. Эхлээд доорх
даалгавраар DOM-оор бичиж, ялгааг өөрөө мэдэр.

```quiz
Imperative ба declarative аргын ялгаа аль нь вэ?
- [x] Imperative нь «хэрхэн» шинэчлэхийг, declarative нь «ямар харагдахыг» бичнэ
- [ ] Declarative нь үргэлж удаан ажилладаг
- [ ] Imperative код бичихэд JavaScript хэрэггүй
> React дэлгэцийг өгөгдлийн функц болгож, DOM-ын шинэчлэлийг өөрөө хийнэ.
```

### Дүгнэлт

DOM-оор бичихэд өгөгдөл өөрчлөгдөх бүрт бүх холбоотой газрыг гараар
шинэчилнэ. React энэ ажлыг хийж, бид зөвхөн «ямар харагдахыг» бичнэ.
""",
            initial_code=files(
                (
                    "index.js",
                    """\
const countEl = document.getElementById("count");
const parityEl = document.getElementById("parity");
const plusButton = document.getElementById("plus");
const resetButton = document.getElementById("reset");

let count = 0;

// TODO 1: «+1» товч дарахад count-ийг нэмэгдүүлж, #count-ийг шинэчил.
// TODO 2: «Тэглэх» товч count-ийг 0 болгоно.
// TODO 3: count өөрчлөгдөх бүрт #parity-д "Тэгш" эсвэл "Сондгой" гэж бич.
""",
                ),
                (
                    "index.html",
                    """\
<main>
  <h1>DOM тоологч</h1>
  <p>Дарсан: <span id="count">0</span></p>
  <p id="parity">Тэгш</p>
  <button id="plus">+1</button>
  <button id="reset">Тэглэх</button>
</main>
""",
                    True,
                ),
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 12 минут

`index.js`-д товчнуудын үйлдлийг бич. Тоо өөрчлөгдөх бүрт **хоёр**
газрыг — `#count` ба `#parity`-г — шинэчлэхээ бүү март. Шинэчлэлийн кодыг
нэг `render()` функцэд цуглуулбал аль ч товчноос дуудаж болно.
""",
                tests=(
                    test(
                        "«+1» товч тоог 1-ээр нэмэгдүүлнэ",
                        """
await runMain();
await user.click(screen.getByRole("button", { name: "+1" }));
await user.click(screen.getByRole("button", { name: "+1" }));
expect(document.getElementById("count")).toHaveTextContent("2");
""",
                    ),
                    test(
                        "«Тэглэх» товч тоог 0 болгоно",
                        """
await runMain();
await user.click(screen.getByRole("button", { name: "+1" }));
await user.click(screen.getByRole("button", { name: "Тэглэх" }));
expect(document.getElementById("count").textContent.trim()).toBe("0");
""",
                    ),
                    test(
                        "Тэгш, сондгойг зөв харуулна",
                        """
await runMain();
await user.click(screen.getByRole("button", { name: "+1" }));
expect(document.getElementById("parity").textContent.trim()).toBe("Сондгой");
await user.click(screen.getByRole("button", { name: "+1" }));
expect(document.getElementById("parity").textContent.trim()).toBe("Тэгш");
""",
                    ),
                    test(
                        "Тэглэхэд «Тэгш» болно",
                        """
await runMain();
await user.click(screen.getByRole("button", { name: "+1" }));
await user.click(screen.getByRole("button", { name: "Тэглэх" }));
expect(document.getElementById("parity").textContent.trim()).toBe("Тэгш");
""",
                    ),
                ),
                tips="""\
Нэг `render()` функц бичээд, товч бүрийн `addEventListener` дотор `count`-оо
өөрчилсний дараа түүнийг дууд:

- `countEl.textContent = count;`
- `parityEl.textContent = count % 2 === 0 ? "Тэгш" : "Сондгой";`

«Тэглэх» дээр `#parity`-г шинэчлэхээ мартах нь яг энэ хичээлийн
харуулах гэсэн алдаа.
""",
                solution=solution(
                    index_js="""\
const countEl = document.getElementById("count");
const parityEl = document.getElementById("parity");
const plusButton = document.getElementById("plus");
const resetButton = document.getElementById("reset");

let count = 0;

function render() {
  countEl.textContent = count;
  parityEl.textContent = count % 2 === 0 ? "Тэгш" : "Сондгой";
}

plusButton.addEventListener("click", () => {
  count = count + 1;
  render();
});

resetButton.addEventListener("click", () => {
  count = 0;
  render();
});
"""
                ),
            ),
        ),
    ],
)
