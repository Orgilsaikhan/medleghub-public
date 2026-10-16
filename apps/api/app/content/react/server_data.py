"""Модул 9 — API ба серверийн өгөгдөл.

HTTP ба REST-ийн үндэс, `POST`/`PATCH`/`DELETE`-ээр өгөгдөл илгээх,
ачаалах/алдаа/хоосон төлөв, серверийн state ба UI state-ийн ялгаа, TanStack
Query (`useQuery`, `useMutation`). Төгсгөлд нь «Сургалтын самбар» төсөл.

Бүх хичээл sandbox-ийн дадлагын API-г (`/api/...`,
`apps/web/src/lib/sandbox/react-runtime/api.ts`) ашиглана. Тестэд
`api.fail(path, 500)`, `api.set(collection, [...])`, `api.requests`,
`api.get(collection)`-оор серверийн төлөвийг удирдаж, шалгана. TanStack
Query-тэй хичээлүүдэд `QueryClient` нь 🔒 `main.jsx`-д (5 дахь хичээлд
сурагч өөрөө бичнэ) `retry: false`-тэй үүснэ — эс бөгөөс алдааны төлөв
7 секунд хүлээгдэж тестийн хугацаа хэтэрнэ. Тест бүрт модулиуд шинээр
ачаалагдах тул `QueryClient` (кэш) ч шинэ.
"""

from app.content.react.common import files, solution, test, vite
from app.content.types import ExerciseSpec, LessonSpec, ModuleSpec
from app.models.enums import LessonLanguage

JSX = LessonLanguage.JSX

DATA_CSS = """\
body {
  margin: 0;
  font-family: system-ui, sans-serif;
  background: #f6f8fa;
  color: #1f2328;
}

main {
  max-width: 560px;
  margin: 0 auto;
  padding: 16px;
}

ul {
  padding: 0;
  list-style: none;
}

li {
  padding: 10px 12px;
  margin-bottom: 8px;
  border: 1px solid #d0d7de;
  border-radius: 8px;
  background: #fff;
}

li h2 {
  margin: 0 0 4px;
  font-size: 16px;
}

li p {
  margin: 0;
  color: #57606a;
}

form {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
  margin-bottom: 12px;
}

input:not([type]),
input[type="text"] {
  padding: 6px 8px;
  border: 1px solid #d0d7de;
  border-radius: 6px;
}

button {
  padding: 6px 12px;
  border: 1px solid #d0d7de;
  border-radius: 6px;
  background: #fff;
  cursor: pointer;
}

button:disabled {
  opacity: 0.6;
  cursor: default;
}

[role="status"] {
  color: #57606a;
}

[role="alert"] {
  padding: 10px 12px;
  border: 1px solid #f1aeb5;
  border-radius: 8px;
  background: #fff5f5;
  color: #b42318;
}

header {
  padding: 10px 16px;
  background: #1f2328;
  color: #fff;
  font-weight: 600;
}
"""

SERVER_DATA = ModuleSpec(
    title="Модул 9 — API ба серверийн өгөгдөл",
    description="HTTP, REST, CRUD хүсэлт, ачаалах ба алдааны төлөв, TanStack Query-гээр серверийн өгөгдөл.",
    lessons=[
        # ------------------------------------------------------------------ 9.1
        LessonSpec(
            title="HTTP ба REST-ийн үндэс",
            slug="http-rest",
            description="Хүсэлт, хариу, method, статус код, REST-ийн замууд ба жагсаалт татах.",
            duration=960,
            language=JSX,
            content="""\
### Энэ хичээлээр

- HTTP хүсэлт ба хариуны бүтцийг ойлгох: method, зам, header, body, статус
- REST-ийн «resource» ба түүний замуудыг унших
- Статус кодоор юу болсныг таних
- Effect-ээр жагсаалт татаж, ачаалах, алдаа, хоосон төлвийг харуулах

### Яагаад чухал вэ

Одоог хүртэл өгөгдлөө `data.js`-д бичиж байлаа. Бодит апп-д бараа,
сургалт, хэрэглэгч, захиалга бүгд **сервер** дээр, өгөгдлийн санд
хадгалагддаг. Хөтөч дээрх React апп тэдгээрийг сүлжээгээр **HTTP** хүсэлт
илгээж авна. Хүсэлт яагаад амжилтгүй болсныг ойлгох, backend хөгжүүлэгч
«`PATCH /api/todos/3` руу илгээ» гэхэд юу хэлж байгааг мэдэхийн тулд
HTTP-ийн үндсийг мэдэх хэрэгтэй.

### Хүсэлт ба хариу

Хөтөч (client) **хүсэлт** илгээж, сервер **хариу** буцаана. Хоёулаа
энгийн текст:

```text
→ Хүсэлт
GET /api/users/2 HTTP/1.1
Accept: application/json

← Хариу
HTTP/1.1 200 OK
Content-Type: application/json

{"id": 2, "name": "Сараа", "city": "Дархан"}
```

Хүсэлт нь **method** (`GET`), **зам** (`/api/users/2`), **header**-ууд
(нэмэлт мэдээлэл), заримдаа **body** (илгээх өгөгдөл)-оос бүрдэнэ. Хариу нь
**статус код** (`200`), header-ууд ба body-той.

### Method — юу хийхийг хэлнэ

| Method | Утга | Body | Жишээ |
|---|---|---|---|
| `GET` | Унших | Үгүй | `GET /api/todos` |
| `POST` | Шинээр үүсгэх | Тийм | `POST /api/todos` |
| `PUT` | Бүтнээр нь солих | Тийм | `PUT /api/todos/3` |
| `PATCH` | Хэсэгчлэн засах | Тийм | `PATCH /api/todos/3` |
| `DELETE` | Устгах | Үгүй | `DELETE /api/todos/3` |

`GET` өгөгдлийг хэзээ ч өөрчлөх ёсгүй: хөтөч, кэш, хайлтын систем түүнийг
хэдэн ч удаа дахин илгээж болно гэж үздэг.

### Статус код — юу болсныг хэлнэ

| Код | Утга |
|---|---|
| `200 OK` | Амжилттай |
| `201 Created` | Шинэ бичлэг үүслээ (`POST`-ийн дараа) |
| `204 No Content` | Амжилттай, body хоосон (ихэвчлэн `DELETE`) |
| `400 Bad Request` | Хүсэлт буруу: талбар дутуу, JSON эвдэрхий |
| `401` / `403` | Нэвтрээгүй / эрх хүрэхгүй |
| `404 Not Found` | Ийм зүйл алга |
| `500 Internal Server Error` | Сервер дээр алдаа гарлаа |

Эхний цифр нь ангиллыг хэлнэ: **2xx** амжилт, **4xx** клиентийн алдаа
(хүсэлт буруу, дахин илгээгээд нэмэргүй), **5xx** серверийн алдаа (таны
буруу биш, хэсэг хугацааны дараа дахин оролдож болно).

### Header ба JSON

Header нь хүсэлт, хариуны тухай мэдээлэл: `Content-Type: application/json`
нь «body JSON форматтай» гэсэн үг, `Accept` нь ямар хариу хүлээж байгааг,
`Authorization: Bearer <token>` нь нэвтэрсэн хэрэглэгчийг хэлнэ. REST
API-ууд өгөгдлийг ихэвчлэн **JSON** хэлбэрээр солилцдог: хариуг
`response.json()`-оор уншиж, илгээхдээ `JSON.stringify()` хийнэ.

### REST — resource ба зам

REST бол API зохион байгуулах түгээмэл дүрэм. Өгөгдлийн төрөл бүр нэг
**resource** (нэр үг, олон тоогоор), үйлдлийг нь **method** хэлнэ:

```text
GET    /api/todos              бүх ажил
GET    /api/todos/3            id = 3 ажил
POST   /api/todos              шинэ ажил үүсгэх
PATCH  /api/todos/3            id = 3 ажлыг засах
DELETE /api/todos/3            id = 3 ажлыг устгах
GET    /api/todos?done=false   шүүх (query параметр)
```

Замд үйл үг бичдэггүй: `/api/getTodos`, `/api/deleteTodo?id=3` гэж биш.
Энэ засварлагчийн дадлагын API (`/api/products`, `/api/courses`,
`/api/users`, `/api/todos`, …) яг ийм дүрмээр ажилладаг.

### React-д жагсаалт татах

Модул 5-д үзсэн хэв маяг: effect дотор `fetch`, `response.ok`-ийн
шалгалт, цэвэрлэгээнд `AbortController`. Дараа нь **дөрвөн** төлвийг
харуулна:

```jsx
if (loading) return <p>Ачаалж байна…</p>;
if (error) return <p role="alert">Алдаа: {error.message}</p>;
if (products.length === 0) return <p>Бараа алга</p>;
return <ul>{products.map((p) => <li key={p.id}>{p.name}</li>)}</ul>;
```

Хоосон төлвийг мартах нь түгээмэл. Хоосон `<ul>` харсан хэрэглэгч «эвдэрсэн
үү, ачаалж байна уу?» гэж эргэлзэнэ.

### Статусаар алдааг ялгах

«Алдаа гарлаа» гэхээс илүү хэрэгтэй нь юу болсныг хэлэх. `Error`
объектод статус кодыг хавсаргавал UI нь 4xx, 5xx-ийг ялгаж чадна:

```jsx
const response = await fetch("/api/products", { signal: controller.signal });
if (!response.ok) {
  const error = new Error(`HTTP ${response.status}`);
  error.status = response.status;
  throw error;
}

function errorText(error) {
  if (!error.status) return "Сүлжээний алдаа. Интернэт холболтоо шалгана уу.";
  if (error.status >= 500) return `Серверийн алдаа (${error.status}). Дараа дахин оролдоорой.`;
  return `Хүсэлт буруу (${error.status}).`;
}
```

5xx үед «дахин оролдоорой» гэх нь утгатай, 4xx үед ижил хүсэлтийг дахин
илгээх нь нэмэргүй. Интернэт тасарвал `fetch` өөрөө `TypeError` шиддэг —
тэр алдаанд `status` байхгүй.

```jsx
const response = await fetch("/api/products");
const products = await response.json();
setProducts(products);
// render: products.map((p) => <li key={p.id}>{p.name}</li>)
```

```quiz
Дээрх кодтой үед сервер `500`, body нь `{ "error": "…" }` буцаавал юу болох вэ?
- [ ] `catch` ажиллаж, алдааны мэдэгдэл гарна
- [x] `products.map is not a function` алдаагаар апп унана
- [ ] Хоосон жагсаалт харагдана
> `fetch` нь 500-д алдаа шидэхгүй. Алдааны JSON объект state-д орж, `map` дуудахад унана. `response.ok`-ийг заавал шалга.
```

```quiz
Шинэ бичлэг амжилттай үүсэхэд сервер ихэвчлэн ямар статус буцаах вэ?
- [ ] `200 OK`
- [x] `201 Created`
- [ ] `204 No Content`
- [ ] `302 Found`
> `201` нь «шинэ зүйл үүслээ» гэсэн утгатай, body-д нь ихэвчлэн үүссэн бичлэг (id-тай нь) ирнэ.
```

```quiz
REST дүрмийн дагуу 5 дугаар барааг устгах хүсэлт аль нь вэ?
- [x] `DELETE /api/products/5`
- [ ] `POST /api/deleteProduct?id=5`
- [ ] `GET /api/products/5/delete`
> Зам нь resource-ийг (`/api/products/5`), method нь үйлдлийг (`DELETE`) заана.
```

### Хүсэлтээ харах

Бодит хөтөчид F12 → **Network** tab-д хүсэлт бүрийн method, статус,
header, body харагдана — API-тай ажиллахдаа хамгийн их нээдэг цонх. Энэ
засварлагчид түүний оронд `console.log(response.status)` хэвлээрэй. Замд
`?_delay=2000` нэмбэл хариу 2 секунд хоцорно, `?_status=500` нэмбэл
серверийн алдааг дуурайна.

### Дүгнэлт

HTTP хүсэлт нь method, зам, header, body-тай; хариу нь статус код ба
body-той. REST-д resource-ийг зам, үйлдлийг method заана. Өгөгдөл татахдаа
`response.ok`-ийг шалгаж, ачаалах, алдаа, хоосон, амжилттай гэсэн дөрвөн
төлвийг бүгдийг нь харуул. Алдааны мэдэгдэлд статусыг ашиглаж, хэрэглэгчид
юу хийхийг хэл.
""",
            initial_code=vite(
                """\
import { useEffect, useState } from "react";

// Алдааны текст — статус кодоор ялгана.
function errorText(error) {
  // TODO: 5xx → «Серверийн алдаа (503). Дараа дахин оролдоорой.»
  //       4xx → «Хүсэлт буруу (404).»
  //       status байхгүй (сүлжээ тасарсан) → «Сүлжээний алдаа…»
  return "Алдаа гарлаа";
}

export default function App() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // TODO: useEffect дотор GET /api/products хүсэлт илгээ.
  //  - response.ok биш бол status-тай алдаа шид (error.status = response.status)
  //  - амжилттай бол setProducts, дараа нь setLoading(false)
  //  - component устахад AbortController-оор хүсэлтийг цуцал

  return (
    <main>
      <h1>🛒 Бараанууд</h1>
      {/* TODO: ачаалж байхад «Ачаалж байна…»,
          алдаа гарвал role="alert" дотор errorText(error),
          бараа байхгүй бол «Бараа алга» */}
      <ul>
        {products.map((product) => (
          <li key={product.id}>
            {product.emoji} {product.name} — {product.price}₮
          </li>
        ))}
      </ul>
    </main>
  );
}
""",
                css=DATA_CSS,
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 12 минут

`/api/products`-ээс бараануудыг effect дотор татаж жагсаа. Хариу ирэх
хүртэл «Ачаалж байна…», бараа байхгүй бол «Бараа алга» гэж харуул. Алдаа
гарвал `role="alert"` мэдэгдэлд статус кодыг оруул: 5xx бол «Серверийн
алдаа (503)…», 4xx бол «Хүсэлт буруу (404)». «Хөтөч» дээр замыг түр
`/api/products?_status=503` эсвэл `?_status=404` болгож туршаарай.
""",
                tests=(
                    test(
                        "Хариу ирэх хүртэл «Ачаалж байна…», дараа нь 10 бараа харагдана",
                        """
render(<App />);
expect(screen.text()).toContain("Ачаалж байна");
await waitFor(() => expect(screen.getAllByRole("listitem")).toHaveLength(10));
expect(screen.getAllByRole("listitem")[0]).toHaveTextContent("Банана");
expect(screen.getAllByRole("listitem")[0]).toHaveTextContent("3500");
expect(screen.text()).not.toContain("Ачаалж байна");
""",
                    ),
                    test(
                        "/api/products руу GET хүсэлт ганц удаа илгээнэ",
                        """
render(<App />);
await waitFor(() => expect(screen.getAllByRole("listitem")).toHaveLength(10));
await sleep(100);
const requests = api.requests.filter((request) => request.path.startsWith("/api/products"));
expect(requests).toHaveLength(1);
expect(requests[0].method).toBe("GET");
""",
                    ),
                    test(
                        "5xx алдаанд «Серверийн алдаа» гэж статус кодтой нь харуулна",
                        """
api.fail("/api/products", 503);
render(<App />);
const alert = await screen.findByRole("alert");
expect(alert).toHaveTextContent("Серверийн алдаа");
expect(alert).toHaveTextContent("503");
expect(screen.text()).not.toContain("Ачаалж байна");
expect(screen.queryAllByRole("listitem")).toHaveLength(0);
""",
                    ),
                    test(
                        "4xx алдаанд «Хүсэлт буруу» гэж статус кодтой нь харуулна",
                        """
api.fail("/api/products", 404);
render(<App />);
const alert = await screen.findByRole("alert");
expect(alert).toHaveTextContent("Хүсэлт буруу");
expect(alert).toHaveTextContent("404");
expect(alert).not.toHaveTextContent("Серверийн алдаа");
""",
                    ),
                    test(
                        "Бараа байхгүй бол «Бараа алга» гэж харуулна",
                        """
api.set("products", []);
render(<App />);
expect(await screen.findByText(/Бараа алга/)).toBeInTheDocument();
expect(screen.text()).not.toContain("Ачаалж байна");
""",
                    ),
                ),
                tips="""\
- Effect-ийн dependency нь `[]` — бараануудыг нэг л удаа татна. Effect
  өөрөө `async` байж болохгүй тул дотор нь `async function load()` зарлаад
  шууд дууд.
- `fetch("/api/products", { signal: controller.signal })`, цэвэрлэгээнд
  `controller.abort()`. Цуцалсан хүсэлтийн `AbortError`-ийг алдаа гэж
  харуулахгүй.
- `const error = new Error(…); error.status = response.status; throw error;`
  — `catch` дотор `setError(caught)` хийвэл `errorText` статусыг уншина.
- `errorText`: эхлээд `!error.status`, дараа нь `error.status >= 500`,
  бусад нь 4xx.
- Алдаа гарсан ч `setLoading(false)` хийхээ бүү март, үгүй бол «Ачаалж
  байна…» үүрд үлдэнэ.
""",
                solution=solution(
                    App_jsx="""\
import { useEffect, useState } from "react";

// Алдааны текст — статус кодоор ялгана.
function errorText(error) {
  if (!error.status) return "Сүлжээний алдаа. Интернэт холболтоо шалгана уу.";
  if (error.status >= 500) {
    return `Серверийн алдаа (${error.status}). Дараа дахин оролдоорой.`;
  }
  return `Хүсэлт буруу (${error.status}).`;
}

export default function App() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const controller = new AbortController();

    async function load() {
      try {
        const response = await fetch("/api/products", { signal: controller.signal });
        if (!response.ok) {
          const failure = new Error(`HTTP ${response.status}`);
          failure.status = response.status;
          throw failure;
        }
        setProducts(await response.json());
        setLoading(false);
      } catch (caught) {
        if (caught.name === "AbortError") return;
        setError(caught);
        setLoading(false);
      }
    }

    load();
    return () => controller.abort();
  }, []);

  return (
    <main>
      <h1>🛒 Бараанууд</h1>
      {loading && <p role="status">Ачаалж байна…</p>}
      {error && <p role="alert">{errorText(error)}</p>}
      {!loading && !error && products.length === 0 && <p>Бараа алга</p>}
      {products.length > 0 && (
        <ul>
          {products.map((product) => (
            <li key={product.id}>
              {product.emoji} {product.name} — {product.price}₮
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}
"""
                ),
            ),
        ),
        # ------------------------------------------------------------------ 9.2
        LessonSpec(
            title="Өгөгдөл илгээх: POST, PATCH, DELETE",
            slug="post-patch-delete",
            description="JSON body, Content-Type header, серверийн хариугаар state шинэчлэх.",
            duration=1020,
            language=JSX,
            content="""\
### Энэ хичээлээр

- `POST`-оор шинэ бичлэг үүсгэж, JSON body илгээх
- `PATCH` ба `PUT`-ийн ялгааг мэдэж, `DELETE`-ээр устгах
- Серверийн хариугаар local state-ээ шинэчлэх
- Хүсэлт амжилтгүй болбол дэлгэцэнд худал өгөгдөл үлдээхгүй байх

### Яагаад чухал вэ

Ажил нэмэх, сагсанд хийх, профайл засах — хэрэглэгчийн хийсэн өөрчлөлт
бүр сервер дээр хадгалагдах ёстой. Эс бөгөөс хуудсыг дахин ачаалахад бүгд
алга болно. Хүсэлт буруу хэлбэртэй бол сервер ойлгохгүй, хариуг нь
тоохгүй бол дэлгэц ба сервер хоёр зөрнө.

### POST — шинэ бичлэг үүсгэх

```jsx
async function addTodo(title) {
  const response = await fetch("/api/todos", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, done: false }),
  });
  if (!response.ok) {
    throw new Error("Ажлыг хадгалж чадсангүй");
  }
  const created = await response.json(); // { id: 4, title, done: false }
  setTodos((current) => [...current, created]);
}
```

`fetch`-ийн хоёр дахь аргументад гурван зүйл бичнэ:

- **`method`** — анхдагч нь `GET`, тиймээс бусдыг заавал бичнэ.
- **`headers`** — `Content-Type: application/json` нь серверт «body JSON»
  гэж хэлнэ. Үүнгүйгээр олон сервер (Express, FastAPI) body-г уншихгүй,
  `400` эсвэл `422` буцаана.
- **`body`** — **текст** байх ёстой, тиймээс `JSON.stringify(…)`. Объектыг
  шууд өгвөл `"[object Object]"` гэсэн утгагүй текст илгээгдэнэ.

`id`-г **сервер** өгдөг. `{ id: Date.now(), title }` гэж өөрөө зохиохын
оронд серверийн буцаасан `created`-ийг state-д нэмнэ. Дараагийн `PATCH`,
`DELETE` яг тэр id-г ашиглана.

### PATCH ба PUT — засах

```jsx
async function toggleTodo(todo) {
  const response = await fetch(`/api/todos/${todo.id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ done: !todo.done }),
  });
  if (!response.ok) {
    throw new Error("Шинэчилж чадсангүй");
  }
  const updated = await response.json();
  setTodos((current) =>
    current.map((item) => (item.id === updated.id ? updated : item)),
  );
}
```

`PATCH` зөвхөн илгээсэн талбарыг өөрчилнө. `PUT` бол бичлэгийг **бүхэлд
нь солино**: илгээгээгүй талбар устна. Шинэчилсний дараа серверийн
буцаасан `updated`-ийг `map`-аар байранд нь тавина — сервер өөр талбарыг
(жишээ нь `updatedAt`) ч өөрчилсөн байж болно.

```quiz
Сервер дээр `{ id: 2, title: "useState дасгал хийх", done: false }` байна. `PUT /api/todos/2`-оор `{ done: true }` илгээвэл юу үлдэх вэ?
- [ ] `{ id: 2, title: "useState дасгал хийх", done: true }`
- [x] `{ id: 2, done: true }`
- [ ] Юу ч өөрчлөгдөхгүй
> `PUT` бичлэгийг бүхэлд нь сольдог — `title` илгээгээгүй тул устлаа. Нэг талбар өөрчлөхөд `PATCH` хэрэглэ.
```

### DELETE — устгах

```jsx
async function deleteTodo(id) {
  const response = await fetch(`/api/todos/${id}`, { method: "DELETE" });
  if (!response.ok) {
    throw new Error("Устгаж чадсангүй");
  }
  setTodos((current) => current.filter((item) => item.id !== id));
}
```

Олон API устгасны дараа `204 No Content` буцаадаг — body хоосон. Тэр үед
`response.json()` дуудвал `Unexpected end of JSON input` алдаа гарна.
Устгасан бичлэгийн id танд аль хэдийн байгаа тул хариуны body хэрэггүй.

### Серверийг хүлээх

Дээрх функц бүр серверийн хариуг **хүлээгээд** дараа нь state-ээ
өөрчилдөг. Үүнийг pessimistic update гэдэг: жаахан удаан ч найдвартай,
алдаа гарвал дэлгэц худал зүйл харуулахгүй. Хариуг хүлээлгүй шууд харуулж,
алдаа гарвал буцаадаг optimistic update-ийг Модул 11-д `useOptimistic`-оор
үзнэ.

Event handler дотор async функц алдаа шидвэл түүнийг хэн ч барихгүй —
Console-д `Uncaught (in promise)` гарна. Тиймээс handler дотор
`try`/`catch` хийж, хэрэглэгчид мэдэгдэл харуулна:

```jsx
async function handleAdd() {
  try {
    await addTodo(title);
    setTitle("");
  } catch (error) {
    setError(error.message);
  }
}
```

Бодит төсөлд `fetch`-ийг `api.js` доторх жижиг `request(url, options)`
функцэд боож, header, `response.ok`-ийн шалгалтыг нэг газар бичдэг —
component-ууд давхардсан кодгүй болно.

```quiz
`fetch("/api/todos", { method: "POST", body: { title: "Сүү авах" } })` — энэ мөрөнд юу дутуу вэ?
- [ ] `method` нь жижиг үсгээр байх ёстой
- [x] `body`-г `JSON.stringify`-аар текст болгож, `Content-Type` header нэмэх ёстой
- [ ] `POST` хүсэлтэд body илгээдэггүй
> Объект шууд илгээгдэхгүй — `"[object Object]"` болно. JSON текст ба түүнийг тайлбарлах header хоёулаа хэрэгтэй.
```

```quiz
Шинэ ажлыг state-д нэмэхдээ яагаад серверийн хариуг (`created`) ашигладаг вэ?
- [ ] Хариуг ашиглахгүй бол React анхааруулга өгнө
- [x] Сервер бичлэгт id өгдөг — дараагийн PATCH, DELETE тэр id-г хэрэглэнэ
- [ ] `fetch` хариугаа уншихгүй бол хүсэлт цуцлагдана
> Өөрөө зохиосон id сервер дээрхтэй таарахгүй тул дараа нь засах, устгах хүсэлт `404` авна.
```

### Дүгнэлт

`POST` үүсгэнэ, `PATCH` хэсэгчлэн засна, `PUT` бүхэлд нь солино, `DELETE`
устгана. Body илгээхдээ `JSON.stringify` ба `Content-Type` хоёулаа хэрэгтэй.
`response.ok`-ийг шалгаж, серверийн хариугаар state-ээ immutable
шинэчил.
""",
            initial_code=vite(
                """\
import { useEffect, useState } from "react";

export default function App() {
  const [todos, setTodos] = useState([]);
  const [title, setTitle] = useState("");
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("/api/todos")
      .then((response) => response.json())
      .then(setTodos);
  }, []);

  // Үйлдлийг ажиллуулж, алдаа шидвэл мэдэгдэл харуулна. Амжилттай бол true.
  async function run(action) {
    setError(null);
    try {
      await action();
      return true;
    } catch (caught) {
      setError(caught.message || "Алдаа гарлаа");
      return false;
    }
  }

  async function addTodo(text) {
    // TODO: POST /api/todos — body: { title: text, done: false }
    // response.ok биш бол алдаа шид. Серверийн буцаасан todo-г төгсгөлд нэм.
  }

  async function toggleTodo(todo) {
    // TODO: PATCH /api/todos/:id — body: { done: !todo.done }
    // Серверийн буцаасан todo-гоор жагсаалтад байгааг нь соль.
  }

  async function deleteTodo(id) {
    // TODO: DELETE /api/todos/:id, амжилттай бол жагсаалтаас хас.
  }

  async function handleSubmit(event) {
    event.preventDefault();
    const text = title.trim();
    if (!text) return;
    if (await run(() => addTodo(text))) setTitle("");
  }

  return (
    <main>
      <h1>✅ Ажлын жагсаалт</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Шинэ ажил <input value={title} onChange={(event) => setTitle(event.target.value)} />
        </label>
        <button type="submit">Нэмэх</button>
      </form>
      {error && <p role="alert">{error}</p>}
      <ul>
        {todos.map((todo) => (
          <li key={todo.id}>
            <label>
              <input type="checkbox" checked={todo.done} onChange={() => run(() => toggleTodo(todo))} />{" "}
              {todo.title}
            </label>{" "}
            <button onClick={() => run(() => deleteTodo(todo.id))}>Устгах</button>
          </li>
        ))}
      </ul>
    </main>
  );
}
""",
                css=DATA_CSS,
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐ · 15 минут

Жагсаалт татах, форм, товчнууд бэлэн. `addTodo`, `toggleTodo`,
`deleteTodo` гурван функцийг `/api/todos` руу зөв хүсэлт илгээдэг болгож,
серверийн хариугаар `todos` state-ийг шинэчил. Хариу `ok` биш бол алдаа
шид — бэлэн `run` функц түүнийг барьж мэдэгдэл харуулна.
""",
                tests=(
                    test(
                        "Шинэ ажил сервер дээр хадгалагдаж, жагсаалтын төгсгөлд нэмэгдэнэ",
                        """
render(<App />);
await screen.findByText("React хичээл үзэх");
await user.type(screen.getByLabelText("Шинэ ажил"), "Сүү авах{enter}");
await waitFor(() => expect(screen.getAllByRole("listitem")).toHaveLength(4));
expect(screen.getAllByRole("listitem")[3]).toHaveTextContent("Сүү авах");
const saved = api.get("todos").find((todo) => todo.title === "Сүү авах");
expect(saved).toBeTruthy();
expect(saved.done).toBe(false);
""",
                    ),
                    test(
                        "POST хүсэлт JSON body ба «Content-Type: application/json» header-тэй",
                        """
const realFetch = window.fetch;
const calls = [];
window.fetch = (input, init = {}) => {
  calls.push(init);
  return realFetch(input, init);
};
try {
  render(<App />);
  await screen.findByText("React хичээл үзэх");
  await user.type(screen.getByLabelText("Шинэ ажил"), "Сүү авах{enter}");
  const isPost = (init) => String(init.method || "").toUpperCase() === "POST";
  await waitFor(() => expect(calls.some(isPost)).toBe(true));
  const post = calls.find(isPost);
  expect(typeof post.body).toBe("string");
  expect(JSON.parse(post.body).title).toBe("Сүү авах");
  expect(new Headers(post.headers).get("Content-Type") || "").toContain("application/json");
} finally {
  window.fetch = realFetch;
}
""",
                    ),
                    test(
                        "Checkbox дарахад PATCH-аар done солигдож, гарчиг хэвээр үлдэнэ",
                        """
render(<App />);
const box = await screen.findByRole("checkbox", { name: "useState дасгал хийх" });
expect(box).not.toBeChecked();
await user.click(box);
await waitFor(() =>
  expect(screen.getByRole("checkbox", { name: "useState дасгал хийх" })).toBeChecked(),
);
expect(api.requests.some((r) => r.method === "PATCH" && r.path === "/api/todos/2")).toBe(true);
expect(api.get("todos").find((todo) => todo.id === 2)).toEqual({
  id: 2,
  title: "useState дасгал хийх",
  done: true,
});
""",
                    ),
                    test(
                        "«Устгах» товч DELETE хүсэлтээр ажлыг сервер болон жагсаалтаас хасна",
                        """
render(<App />);
const item = (await screen.findByText("Төсөл эхлүүлэх")).closest("li");
await user.click(within(item).getByRole("button", { name: /Устгах/ }));
await waitFor(() => expect(screen.queryByText("Төсөл эхлүүлэх")).toBeNull());
expect(api.requests.some((r) => r.method === "DELETE" && r.path === "/api/todos/3")).toBe(true);
expect(api.get("todos").map((todo) => todo.id)).toEqual([1, 2]);
""",
                    ),
                    test(
                        "Сервер алдаа буцаавал ажил нэмэгдэхгүй, алдааны мэдэгдэл харагдана",
                        """
render(<App />);
await screen.findByText("React хичээл үзэх");
api.fail("/api/todos", 500);
await user.type(screen.getByLabelText("Шинэ ажил"), "Сүү авах{enter}");
expect(await screen.findByRole("alert")).toBeInTheDocument();
expect(screen.getAllByRole("listitem")).toHaveLength(3);
expect(screen.queryByText("Сүү авах")).toBeNull();
""",
                    ),
                ),
                tips="""\
- Гурван функц ижил хэв маягтай: `fetch(url, { method, headers, body })` →
  `if (!response.ok) throw new Error(…)` → state шинэчлэх.
- `POST`, `PATCH`-д `headers: { "Content-Type": "application/json" }` ба
  `body: JSON.stringify(…)` хоёулаа хэрэгтэй.
- Зам: `` `/api/todos/${todo.id}` `` — id-г замд, өөрчлөлтийг body-д.
- State-ийг функцээр, immutable шинэчил: нэмэх `[...current, created]`,
  солих `current.map(…)`, хасах `current.filter(…)`.
- `response.ok`-ийг шалгахгүй бол 500-ийн хариу `{ error: "…" }` шинэ
  «ажил» болж жагсаалтад орно.
""",
                solution=solution(
                    App_jsx="""\
import { useEffect, useState } from "react";

export default function App() {
  const [todos, setTodos] = useState([]);
  const [title, setTitle] = useState("");
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("/api/todos")
      .then((response) => response.json())
      .then(setTodos);
  }, []);

  // Үйлдлийг ажиллуулж, алдаа шидвэл мэдэгдэл харуулна. Амжилттай бол true.
  async function run(action) {
    setError(null);
    try {
      await action();
      return true;
    } catch (caught) {
      setError(caught.message || "Алдаа гарлаа");
      return false;
    }
  }

  async function addTodo(text) {
    const response = await fetch("/api/todos", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: text, done: false }),
    });
    if (!response.ok) {
      throw new Error("Ажлыг хадгалж чадсангүй. Дахин оролдоно уу.");
    }
    const created = await response.json();
    setTodos((current) => [...current, created]);
  }

  async function toggleTodo(todo) {
    const response = await fetch(`/api/todos/${todo.id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ done: !todo.done }),
    });
    if (!response.ok) {
      throw new Error("Ажлыг шинэчилж чадсангүй.");
    }
    const updated = await response.json();
    setTodos((current) => current.map((item) => (item.id === updated.id ? updated : item)));
  }

  async function deleteTodo(id) {
    const response = await fetch(`/api/todos/${id}`, { method: "DELETE" });
    if (!response.ok) {
      throw new Error("Ажлыг устгаж чадсангүй.");
    }
    setTodos((current) => current.filter((item) => item.id !== id));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    const text = title.trim();
    if (!text) return;
    if (await run(() => addTodo(text))) setTitle("");
  }

  return (
    <main>
      <h1>✅ Ажлын жагсаалт</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Шинэ ажил <input value={title} onChange={(event) => setTitle(event.target.value)} />
        </label>
        <button type="submit">Нэмэх</button>
      </form>
      {error && <p role="alert">{error}</p>}
      <ul>
        {todos.map((todo) => (
          <li key={todo.id}>
            <label>
              <input type="checkbox" checked={todo.done} onChange={() => run(() => toggleTodo(todo))} />{" "}
              {todo.title}
            </label>{" "}
            <button onClick={() => run(() => deleteTodo(todo.id))}>Устгах</button>
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
        # ------------------------------------------------------------------ 9.3
        LessonSpec(
            title="Ачаалах, алдаа, хоосон төлөв",
            slug="achaalal-aldaa-hooson",
            description="Олон boolean-ы оронд нэг status, «Дахин оролдох» товч ба ойлгомжтой мэдэгдэл.",
            duration=960,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Асинхрон UI-ийн дөрвөн төлвийг (ачаалж буй, алдаа, хоосон, амжилттай)
  бүрэн харуулах
- Олон boolean-ы оронд нэг `status` хувьсагч (төлвийн машин) ашиглах
- «Дахин оролдох» товчоор хүсэлтийг дахин илгээх
- Хэрэглэгчид ойлгомжтой, хүртээмжтэй мэдэгдэл бичих

### Яагаад чухал вэ

Сүлжээ үргэлж хурдан, найдвартай байдаггүй: хөдөө орон нутгийн мобайл
интернет, лифт, сервер шинэчлэгдэж буй мөч. Хэрэглэгч хоосон цагаан дэлгэц
эсвэл үүрд эргэлдэх spinner харвал «апп эвдэрчээ» гэж бодоод гарна. Сайн
апп төлөв бүрт юу болж байгааг, одоо юу хийж болохыг хэлдэг.

### Boolean-уудын асуудал

```jsx
const [isLoading, setIsLoading] = useState(true);
const [isError, setIsError] = useState(false);
const [posts, setPosts] = useState([]);

async function load() {
  try {
    const response = await fetch("/api/posts");
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    setPosts(await response.json());
    setIsLoading(false);
  } catch {
    setIsError(true);
  }
}
```

Хоёр boolean дөрвөн хослол үүсгэнэ, гэтэл утгатай нь гурав: «ачаалж
байна», «алдаа», «бэлэн». `isLoading` ба `isError` зэрэг `true` байх нь
**боломжгүй төлөв** — гэвч код үүнийг зөвшөөрдөг. Нэг `set…`-ийг мартахад л
хангалттай.

```quiz
Дээрх кодтой үед сервер `500` буцаавал дэлгэцэд юу харагдах вэ (`isLoading` бол «Ачаалж байна…», `isError` бол алдааны мэдэгдэл)?
- [ ] Зөвхөн алдааны мэдэгдэл
- [x] «Ачаалж байна…» ба алдааны мэдэгдэл зэрэг, «Ачаалж байна…» хэзээ ч алга болохгүй
- [ ] Хоосон жагсаалт
> `catch` дотор `setIsLoading(false)` алга. Олон boolean-тай үед ийм алдаа амархан гардаг.
```

### Төлвийн машин: нэг status

Олон boolean-ы оронд боломжит төлвүүдийг **нэг** хувьсагчаар илэрхийлнэ:

```jsx
const [status, setStatus] = useState("loading"); // "loading" | "error" | "success"
const [posts, setPosts] = useState([]);
const [error, setError] = useState(null);
```

`status` нэг агшинд нэг л утгатай тул «ачаалж байгаа ба алдаатай» гэсэн
төлөв үүсэх боломжгүй. Шилжилтүүдийг зурж болно:

```text
loading ──амжилт──▶ success
   │
   └──алдаа──▶ error ──«Дахин оролдох»──▶ loading
```

«Хоосон» нь тусдаа status биш — амжилттай хариуны нэг хэлбэр. Үүнийг
өгөгдлөөс гаргаж авна (Модул 3-ын уламжлагдсан утга):

```jsx
let content;
if (status === "loading") {
  content = <p role="status">Ачаалж байна…</p>;
} else if (status === "error") {
  content = <p role="alert">Нийтлэлүүдийг ачаалж чадсангүй.</p>;
} else if (posts.length === 0) {
  content = <p>Нийтлэл алга. Эхнийхийг нь та бичээрэй!</p>;
} else {
  content = <ul>{/* … */}</ul>;
}

return (
  <main>
    <h1>Нийтлэлүүд</h1>
    {content}
  </main>
);
```

Гарчиг ямар ч төлөвт харагдсаар байна — зөвхөн агуулга солигдоно.

### Дахин оролдох

Effect-ийг дахин ажиллуулахын тулд dependency-г нь өөрчилнө. Хамгийн
энгийн арга нь тоолуур:

```jsx
const [attempt, setAttempt] = useState(0);

useEffect(() => {
  const controller = new AbortController();

  async function load() {
    try {
      const response = await fetch("/api/posts", { signal: controller.signal });
      if (!response.ok) throw new Error(`Сервер ${response.status} алдаа буцаалаа`);
      setPosts(await response.json());
      setStatus("success");
    } catch (caught) {
      if (caught.name === "AbortError") return;
      setError(caught);
      setStatus("error");
    }
  }

  load();
  return () => controller.abort();
}, [attempt]);

function retry() {
  setStatus("loading");
  setAttempt((count) => count + 1);
}
```

`retry` дарагдахад `status` шууд `"loading"` болж алдааны мэдэгдэл
нуугдана, `attempt` өөрчлөгдсөн тул effect дахин ажиллана. Өмнөх хүсэлт
дуусаагүй байсан ч цэвэрлэгээ түүнийг цуцална. 4xx алдаанд (хүсэлт өөрөө
буруу) дахин оролдох нь ихэвчлэн утгагүй — «Дахин оролдох»-ыг 5xx ба
сүлжээний алдаанд санал болгодог.

### Хэрэглэгчид ээлтэй мэдэгдэл

- Алдааны мессежид **юу болсон**, **юу хийж болохыг** бич: «Нийтлэлүүдийг
  ачаалж чадсангүй. Интернэт холболтоо шалгаад дахин оролдоно уу.»
  `TypeError: Failed to fetch` гэсэн техникийн текст биш.
- `role="status"` нь дэлгэц уншигчид «ачаалж байна»-г тайван уншуулна,
  `role="alert"` нь алдааг шууд зарлана (Модул 4).
- Ачаалах үед хуудасны бүтцийг хадгал. Бодит апп-д жагсаалтын хэлбэртэй
  саарал хайрцгууд (skeleton) түгээмэл — агуулга гарч ирэхэд хуудас
  «үсрэхгүй».
- Хоосон төлөвт дараагийн алхмыг санал болго: «Эхнийхийг нь та бичээрэй!»

```quiz
Яагаад «хоосон»-ыг `status`-ийн тусдаа утга болгодоггүй вэ?
- [ ] `useState` дөрвөөс олон утга хадгалж чаддаггүй
- [x] Хоосон жагсаалт бол амжилттай хариу — өгөгдлөөс (`posts.length === 0`) гаргаж авч болно
- [ ] Хоосон жагсаалтыг React render хийж чаддаггүй
> Өгөгдлөөс тооцож болох зүйлийг тусад нь хадгалбал хоёр утга зөрөх эрсдэлтэй.
```

### Дүгнэлт

Асинхрон UI дөрвөн төлөвтэй: ачаалж буй, алдаа, хоосон, амжилттай. Нэг
`status` хувьсагч боломжгүй төлвийг арилгана, хоосон төлвийг өгөгдлөөс
гаргана. Алдааны үед юу болсныг хэлж, «Дахин оролдох» боломж өг.
""",
            initial_code=vite(
                """\
import { useEffect, useState } from "react";

export default function App() {
  const [posts, setPosts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isError, setIsError] = useState(false);

  useEffect(() => {
    const controller = new AbortController();

    async function load() {
      try {
        const response = await fetch("/api/posts", { signal: controller.signal });
        if (!response.ok) throw new Error(`Сервер ${response.status} алдаа буцаалаа`);
        setPosts(await response.json());
        setIsLoading(false);
      } catch (caught) {
        if (caught.name !== "AbortError") setIsError(true);
      }
    }

    load();
    return () => controller.abort();
  }, []);

  // TODO: isLoading, isError-ийг нэг status ("loading" | "error" | "success") болго.
  // TODO: алдааны үед «Дахин оролдох» товч, нийтлэл байхгүй бол «Нийтлэл алга».
  return (
    <main>
      <h1>📝 Нийтлэлүүд</h1>
      {isLoading && <p role="status">Ачаалж байна…</p>}
      {isError && <p role="alert">Нийтлэлүүдийг ачаалж чадсангүй.</p>}
      <ul>
        {posts.map((post) => (
          <li key={post.id}>
            <h2>{post.title}</h2>
            <p>{post.body}</p>
          </li>
        ))}
      </ul>
    </main>
  );
}
""",
                css=DATA_CSS,
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐ · 15 минут

Энэ апп алдаа гарахад «Ачаалж байна…»-г үүрд харуулж, дахин оролдох
боломжгүй. `isLoading`, `isError` хоёрыг нэг `status` болгож засаад,
алдааны мэдэгдлийн доор «Дахин оролдох» товч нэм. Нийтлэл огт байхгүй бол
«Нийтлэл алга» гэж харуул. Алдааг «Хөтөч» дээр харахын тулд замыг түр
`/api/posts?_status=500` болгож үзээрэй.
""",
                tests=(
                    test(
                        "Ачаалж байхад «Ачаалж байна…», дараа нь нийтлэлүүд харагдана",
                        """
render(<App />);
expect(screen.text()).toContain("Ачаалж байна");
expect(await screen.findByText("Анхны component")).toBeInTheDocument();
expect(screen.getAllByRole("listitem")).toHaveLength(3);
expect(screen.text()).not.toContain("Ачаалж байна");
""",
                    ),
                    test(
                        "Алдаа гарвал «Ачаалж байна…» алга болж, зөвхөн алдааны мэдэгдэл харагдана",
                        """
api.fail("/api/posts", 500);
render(<App />);
expect(await screen.findByRole("alert")).toBeInTheDocument();
expect(screen.text()).not.toContain("Ачаалж байна");
""",
                    ),
                    test(
                        "«Дахин оролдох» дарахад алдааны мэдэгдэл нуугдаж, «Ачаалж байна…» дахин харагдана",
                        """
api.fail("/api/posts", 500);
render(<App />);
await user.click(await screen.findByRole("button", { name: /Дахин оролдох/ }));
expect(screen.text()).toContain("Ачаалж байна");
expect(screen.queryByRole("alert")).toBeNull();
""",
                    ),
                    test(
                        "Сервер сэргэсний дараа «Дахин оролдох» нийтлэлүүдийг ачаална",
                        """
api.fail("/api/posts", 500);
render(<App />);
const retry = await screen.findByRole("button", { name: /Дахин оролдох/ });
api.reset(); // сервер сэргэлээ
await user.click(retry);
expect(await screen.findByText("Анхны component")).toBeInTheDocument();
expect(screen.queryByRole("alert")).toBeNull();
const requests = api.requests.filter((request) => request.path.startsWith("/api/posts"));
expect(requests).toHaveLength(1);
""",
                    ),
                    test(
                        "Нийтлэл байхгүй бол «Нийтлэл алга» гэж харуулна",
                        """
api.set("posts", []);
render(<App />);
expect(await screen.findByText(/Нийтлэл алга/)).toBeInTheDocument();
expect(screen.text()).not.toContain("Ачаалж байна");
expect(screen.queryAllByRole("listitem")).toHaveLength(0);
""",
                    ),
                ),
                tips="""\
- `const [status, setStatus] = useState("loading");` — амжилттай бол
  `"success"`, алдаа гарвал `"error"`. `isLoading`, `isError`-ийг бүр устга.
- Дахин ажиллуулахын тулд `const [attempt, setAttempt] = useState(0);`-ийг
  effect-ийн dependency болго. Товч дарахад `setStatus("loading")` ба
  `setAttempt((count) => count + 1)`.
- Render-ийг `status`-аар салаал: `"loading"` → `role="status"`,
  `"error"` → `role="alert"` + товч, бусад үед хоосон эсэхийг
  `posts.length === 0`-аар шалга.
- Товчийг алдааны мэдэгдлийн доор, `role="alert"`-ийн гадна эсвэл дотор
  тавьж болно — аль нь ч болно.
""",
                solution=solution(
                    App_jsx="""\
import { useEffect, useState } from "react";

export default function App() {
  const [posts, setPosts] = useState([]);
  const [status, setStatus] = useState("loading");
  const [error, setError] = useState(null);
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    const controller = new AbortController();

    async function load() {
      try {
        const response = await fetch("/api/posts", { signal: controller.signal });
        if (!response.ok) throw new Error(`Сервер ${response.status} алдаа буцаалаа`);
        setPosts(await response.json());
        setStatus("success");
      } catch (caught) {
        if (caught.name === "AbortError") return;
        setError(caught);
        setStatus("error");
      }
    }

    load();
    return () => controller.abort();
  }, [attempt]);

  function retry() {
    setStatus("loading");
    setAttempt((count) => count + 1);
  }

  let content;
  if (status === "loading") {
    content = <p role="status">Ачаалж байна…</p>;
  } else if (status === "error") {
    content = (
      <>
        <p role="alert">
          Нийтлэлүүдийг ачаалж чадсангүй ({error.message}). Интернэт холболтоо шалгаад дахин
          оролдоно уу.
        </p>
        <button onClick={retry}>Дахин оролдох</button>
      </>
    );
  } else if (posts.length === 0) {
    content = <p>Нийтлэл алга. Эхнийхийг нь та бичээрэй!</p>;
  } else {
    content = (
      <ul>
        {posts.map((post) => (
          <li key={post.id}>
            <h2>{post.title}</h2>
            <p>{post.body}</p>
          </li>
        ))}
      </ul>
    );
  }

  return (
    <main>
      <h1>📝 Нийтлэлүүд</h1>
      {content}
    </main>
  );
}
"""
                ),
            ),
        ),
        # ------------------------------------------------------------------ 9.4
        LessonSpec(
            title="Серверийн state ба UI state",
            slug="server-state",
            description="Хоёр төрлийн state, кэш ба хуучирсан өгөгдөл, өгөгдлийн сангууд яагаад хэрэгтэй вэ.",
            duration=900,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Серверийн state ба UI state-ийг ялгах
- Кэш, «хуучирсан» (stale) өгөгдөл гэж юу болохыг ойлгох
- Нэг өгөгдлийг олон газар хуулж хадгалахын асуудлыг мэдрэх
- TanStack Query зэрэг өгөгдлийн сангууд яагаад бий болсныг ойлгох

### Яагаад чухал вэ

Өмнөх хичээлүүдэд component бүр өгөгдлөө өөрөө effect-ээр татсан. Жижиг
апп-д энэ хангалттай. Гэвч апп томрох тусам ижил жагсаалтыг таван газар
татаж, нэг газар шинэчлэхэд бусад нь хуучин тоо харуулж, хуудас солих бүрт
«Ачаалж байна…» гарна. Энэ бүхэн нэг л шалтгаантай: серверийн өгөгдлийг
энгийн state шиг харьцаж байна.

### Хоёр төрлийн state

| | UI state | Серверийн state |
|---|---|---|
| Жишээ | нээлттэй цонх, input-ийн текст, сонгосон tab | сургалтууд, захиалга, профайл |
| Эзэн | Таны апп | Сервер (өгөгдлийн сан) |
| Хандах | Шууд, синхрон | Сүлжээгээр, асинхрон |
| Хэн өөрчлөх | Зөвхөн таны код | Бусад хэрэглэгч, өөр төхөөрөмж ч |
| Үнэн эсэх | Үргэлж үнэн | Таны хуулбар хуучирч болно |

UI state-д `useState`, `useReducer`, context хангалттай. Харин серверийн
state бол сервер дээрх өгөгдлийн **хуулбар**, тодорхой агшны зураг
(snapshot). Таныг татсаны дараа өөр хэрэглэгч сургалт нэмж, үнэ өөрчилж
болно — таны хуулбар **хуучирна** (stale).

```quiz
Аль нь серверийн state вэ?
- [ ] Хайлтын input-д бичиж буй текст
- [ ] Цэс нээлттэй эсэх
- [x] Хэрэглэгчийн сервер дээр хадгалагдсан захиалгууд
- [ ] Сонгосон tab
> Захиалгын эзэн нь сервер. Апп зөвхөн түүний хуулбарыг харуулна — өөр төхөөрөмжөөс өөрчлөгдөж болно.
```

### Effect-ээр татахын асуудлууд

1. **Давхардал** — толгой хэсэг ба жагсаалт хоёулаа `/api/courses`-ийг
   татвал хоёр хүсэлт, хоёр хуулбар.
2. **Зөрөлдөөн** — нэг хуулбарыг шинэчлэхэд нөгөө нь мэдэхгүй: жагсаалтад
   6 сургалт, толгойд 5.
3. **Кэш алга** — хуудас руу буцаж ирэх бүрт дахин татаж, «Ачаалж байна…»
   дахин гарна.
4. **Давтагдах код** — loading, error, `AbortController`, дахин оролдох…
   component бүрт шинээр.
5. **Хуучралт** — хэрэглэгч tab-аа нээлттэй орхиод цагийн дараа эргэж
   ирэхэд өгөгдөл аль хэдийн хуучирсан.

Доорх даалгаврын эхлэл кодод эхний хоёр асуудал бий. Console-оос хоёр
хүсэлт явж байгааг хараад, «Git ба GitHub» нэмэх товч дарж толгойн тоо
өөрчлөгдөхгүйг ажигла.

### Кэш ба stale-while-revalidate

**Кэш** гэдэг нь түлхүүр → өгөгдөл (хэзээ татсан тэмдэглэлтэй) гэсэн
хадгалалт. `courses` түлхүүрээр нэг удаа татсан бол дараагийн component
шууд кэшээс авна, сүлжээ рүү дахин явахгүй.

**Stale-while-revalidate** стратеги: хуучирсан ч гэсэн кэштэй өгөгдлийг
**шууд** харуулж, ард нь шинийг татаад, ирэхэд дэлгэцийг шинэчилнэ:

```text
1. Анх нээхэд:    кэш хоосон → «Ачаалж байна…» → татна → кэшлэнэ → харуулна
2. Дахин нээхэд:  кэштэй → ШУУД харуулна → ард нь дахин татна → шинэчилнэ
3. Өөрчилсний дараа: кэшийг «хуучирсан» гэж тэмдэглэнэ → дахин татна
```

Хэрэглэгч хоосон дэлгэц биш, өгөгдөл хардаг — апп «хурдан» санагдана.

### Серверийн өгөгдлийг state-д бүү хуул

```jsx
// ❌ props-ийг state-д хуулсан — эцэг нь шинэ өгөгдөл өгөхөд шинэчлэгдэхгүй
function CourseTitle({ course }) {
  const [title] = useState(course.title);
  return <h2>{title}</h2>;
}

// ✅ Шууд хэрэглэ
function CourseTitle({ course }) {
  return <h2>{course.title}</h2>;
}
```

Хуулбар нэмэгдэх бүрт зөрөх боломж нэмэгдэнэ. Засварлах форм л онцгой:
хэрэглэгчийн бичиж буй ноорог бол UI state тул түүнийг state-д хадгална.

### Нэг эзэнтэй болгох

Одоохондоо шийдэл нь Модул 7-ийн «нэг үнэний эх сурвалж»: өгөгдлийг нэг
газар (эцэг component-д) татаж, хэрэгтэй газарт нь props-оор дамжуулна.
Даалгаврыг ингэж засна. Гэвч өөр route, өөр хуудас, кэш, ард нь
шинэчлэх, өөрчлөлтийн дараа дахин татах… бүгдийг гараар хийвэл та өөрөө
жижиг «өгөгдлийн сан» бичиж байгаатай адил.

### Өгөгдлийн сангууд

Тиймээс серверийн state-д зориулсан сангууд бий:

- **TanStack Query** (хуучин нэр нь React Query) — хамгийн түгээмэл,
  дараагийн хичээлээс үзнэ.
- **SWR** — Vercel-ийн, жижиг, энгийн.
- **RTK Query** — Redux ашигладаг төслүүдэд.

Бүгд ижил зүйлийг хийдэг: түлхүүрээр кэшлэх, зэрэг явсан ижил хүсэлтийг
нэгтгэх (dedupe), ард нь шинэчлэх, алдаанд дахин оролдох, өөрчлөлтийн
дараа кэшийг хүчингүй болгох (invalidate). Next.js, React Router зэрэг
framework-ууд өгөгдлийг сервер дээр татах өөрийн арга бий — Модул 11-д
Server Components-оор танилцана.

```quiz
Stale-while-revalidate стратегитай апп-д хэрэглэгч өмнө нь үзсэн хуудас руугаа буцвал юу харах вэ?
- [ ] Өгөгдөл ирэх хүртэл «Ачаалж байна…»
- [x] Кэштэй өгөгдлийг шууд, дараа нь ард татсан шинэ өгөгдлийг
- [ ] Үргэлж хуучин өгөгдлийг, дахин татахгүй
> Хуучирсан өгөгдлийг шууд харуулж (stale), ард нь шинэчилнэ (revalidate).
```

```quiz
`Header` ба `CourseList` хоёулаа `/api/courses`-ийг өөр өөрийн state-д татдаг. `CourseList` шинэ сургалт нэмж өөрийн state-ээ шинэчилбэл толгой хэд гэж харуулах вэ (өмнө нь 5)?
- [x] 5 — толгойн хуулбар өөрчлөлтийг мэдэхгүй
- [ ] 6 — React хоёр state-ийг автоматаар холбоно
- [ ] 0 — толгой дахин ачаална
> Хоёр тусдаа хуулбар бие биенээ мэдэхгүй. Энэ бол давхардсан серверийн state-ийн гол асуудал.
```

### Дүгнэлт

UI state таных, серверийн state серверийнх — апп зөвхөн хуулбарыг нь
барьдаг бөгөөд тэр нь хуучирдаг. Хуулбар олон байх тусам зөрөх эрсдэл
өснө. Кэш, dedupe, ард нь шинэчлэх, invalidation-ийг гараар бичихийн оронд
TanStack Query зэрэг сан ашигладаг.
""",
            initial_code=vite(
                """\
import { useEffect, useState } from "react";
import { createCourse, getCourses } from "./api";

function Header() {
  const [courses, setCourses] = useState([]);

  useEffect(() => {
    getCourses().then(setCourses);
  }, []);

  return <header>📚 Medleghub · Сургалт: {courses.length}</header>;
}

function CourseList() {
  const [courses, setCourses] = useState(null);

  useEffect(() => {
    getCourses().then(setCourses);
  }, []);

  async function handleAdd() {
    const created = await createCourse("Git ба GitHub");
    setCourses((current) => [...current, created]);
  }

  if (!courses) return <p role="status">Ачаалж байна…</p>;

  return (
    <section>
      <ul>
        {courses.map((course) => (
          <li key={course.id}>{course.title}</li>
        ))}
      </ul>
      <button onClick={handleAdd}>«Git ба GitHub» нэмэх</button>
    </section>
  );
}

// TODO: сургалтуудыг App-д ганц удаа татаж, Header, CourseList-д props-оор дамжуул.
// Нэмэх үйлдэл ч App-д байх ёстой — тэгвэл хоёулаа нэг л хуулбарыг харна.
export default function App() {
  return (
    <>
      <Header />
      <main>
        <CourseList />
      </main>
    </>
  );
}
""",
                locked={
                    "api.js": """\
// Хүсэлт бүрийг Console-д бичнэ — хэдэн удаа татаж байгааг ажигла.

export async function getCourses() {
  console.log("→ GET /api/courses");
  const response = await fetch("/api/courses");
  if (!response.ok) throw new Error(`Сервер ${response.status} алдаа буцаалаа`);
  return response.json();
}

export async function createCourse(title) {
  console.log("→ POST /api/courses");
  const response = await fetch("/api/courses", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, level: "Анхан", lessons: 0, category: "Вэб" }),
  });
  if (!response.ok) throw new Error(`Сервер ${response.status} алдаа буцаалаа`);
  return response.json();
}
"""
                },
                css=DATA_CSS,
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 10 минут

`Header` ба `CourseList` хоёулаа `/api/courses`-ийг тус тусдаа татаж,
өөр өөрийн хуулбарыг барьж байна. Console-оос хоёр хүсэлт явж байгааг,
«Git ба GitHub» нэмэх товч дарахад толгойн тоо өөрчлөгдөхгүйг хар. Дараа нь
сургалтуудыг `App`-д ганц удаа татаж, хоёр component-д props-оор дамжуулж
засаарай.
""",
                tests=(
                    test(
                        "Толгойд «Сургалт: 5», жагсаалтад 5 сургалт харагдана",
                        """
render(<App />);
await waitFor(() => expect(screen.getAllByRole("listitem")).toHaveLength(5));
await waitFor(() => expect(screen.text()).toContain("Сургалт: 5"));
""",
                    ),
                    test(
                        "/api/courses руу GET хүсэлт ганц л удаа явна",
                        """
render(<App />);
await waitFor(() => expect(screen.getAllByRole("listitem")).toHaveLength(5));
await sleep(100);
const gets = api.requests.filter(
  (request) => request.method === "GET" && request.path.startsWith("/api/courses"),
);
expect(gets).toHaveLength(1);
""",
                    ),
                    test(
                        "Сургалт нэмэхэд жагсаалт ба толгойн тоо хоёулаа шинэчлэгдэнэ",
                        """
render(<App />);
await user.click(await screen.findByRole("button", { name: /Git ба GitHub/ }));
expect(await screen.findByText("Git ба GitHub")).toBeInTheDocument();
expect(screen.getAllByRole("listitem")).toHaveLength(6);
await waitFor(() => expect(screen.text()).toContain("Сургалт: 6"));
""",
                    ),
                ),
                tips="""\
- `courses` state ба түүнийг татах `useEffect`-ийг `App` руу зөөж,
  `Header`, `CourseList` доторх хуулбаруудыг устга.
- `Header`-т зөвхөн тоо хэрэгтэй: `<Header count={courses?.length} />`.
  Ачаалж байх үед `courses` нь `null` тул `?.` хэрэглэ.
- `handleAdd`-ийг мөн `App`-д зөөж, `CourseList`-д `onAdd` prop болгон өг
  (Модул 7: state-ийг дээш өргөх).
- Шийдсэний дараа бодоод үз: хоёр өөр хуудас (route) ижил өгөгдөл
  хэрэглэвэл яах вэ? Дараагийн хичээлийн TanStack Query яг үүнийг шийднэ.
""",
                solution=solution(
                    App_jsx="""\
import { useEffect, useState } from "react";
import { createCourse, getCourses } from "./api";

function Header({ count }) {
  return <header>📚 Medleghub · Сургалт: {count ?? "…"}</header>;
}

function CourseList({ courses, onAdd }) {
  if (!courses) return <p role="status">Ачаалж байна…</p>;

  return (
    <section>
      <ul>
        {courses.map((course) => (
          <li key={course.id}>{course.title}</li>
        ))}
      </ul>
      <button onClick={onAdd}>«Git ба GitHub» нэмэх</button>
    </section>
  );
}

export default function App() {
  const [courses, setCourses] = useState(null);

  useEffect(() => {
    getCourses().then(setCourses);
  }, []);

  async function handleAdd() {
    const created = await createCourse("Git ба GitHub");
    setCourses((current) => [...current, created]);
  }

  return (
    <>
      <Header count={courses?.length} />
      <main>
        <CourseList courses={courses} onAdd={handleAdd} />
      </main>
    </>
  );
}
"""
                ),
            ),
        ),
        # ------------------------------------------------------------------ 9.5
        LessonSpec(
            title="TanStack Query: useQuery",
            slug="usequery",
            description="QueryClient, QueryClientProvider, queryKey, queryFn ба isPending, isError, data.",
            duration=1080,
            language=JSX,
            content="""\
### Энэ хичээлээр

- TanStack Query-г суулгаж, `QueryClient`, `QueryClientProvider`-оор
  тохируулах
- `useQuery`-ийн `queryKey`, `queryFn`-ийг ойлгох
- `isPending`, `isError`, `data`, `error`-оор төлөв харуулах
- Кэш, давхардсан хүсэлтийг нэгтгэх (dedupe), дахин оролдохыг (retry) мэдэх

### Яагаад чухал вэ

Өмнөх хичээлүүдэд ~25 мөр effect кодыг component бүрт бичсэн: loading,
error, `AbortController`, `response.ok`. TanStack Query үүнийг нэг hook
болгож, кэш, dedupe, ард нь шинэчлэх, дахин оролдохыг нэмэлт кодгүйгээр
өгнө. Орчин үеийн React төслүүдийн ихэнх нь серверийн өгөгдлийг ийм сангаар
удирддаг.

### Суулгах ба тохируулах

Vite төсөлд:

```bash
npm install @tanstack/react-query
```

Энэ засварлагчид сан бэлэн суусан. Аппын оройд нэг удаа тохируулна:

```jsx
// main.jsx
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { createRoot } from "react-dom/client";
import App from "./App";

const queryClient = new QueryClient();

createRoot(document.getElementById("root")).render(
  <QueryClientProvider client={queryClient}>
    <App />
  </QueryClientProvider>,
);
```

`QueryClient` бол кэш өөрөө. `QueryClientProvider` нь (Модул 7-ийн
context шиг) түүнийг доторх бүх component-д хүргэнэ. `QueryClient`-ийг
component-ийн **гадна** нэг удаа үүсгэ: component дотор `new QueryClient()`
бичвэл render бүрт шинэ, хоосон кэш үүснэ. Provider-гүй бол `useQuery`
«No QueryClient set» гэсэн алдаа шиднэ.

### useQuery

```jsx
import { useQuery } from "@tanstack/react-query";

async function fetchCourses() {
  const response = await fetch("/api/courses");
  if (!response.ok) {
    throw new Error(`Сервер ${response.status} алдаа буцаалаа`);
  }
  return response.json();
}

function CourseList() {
  const { data, isPending, isError, error } = useQuery({
    queryKey: ["courses"],
    queryFn: fetchCourses,
  });

  if (isPending) return <p role="status">Ачаалж байна…</p>;
  if (isError) return <p role="alert">{error.message}</p>;

  return (
    <ul>
      {data.map((course) => (
        <li key={course.id}>{course.title}</li>
      ))}
    </ul>
  );
}
```

- **`queryKey`** — кэшийн түлхүүр, үргэлж массив. Ижил түлхүүртэй бүх
  `useQuery` нэг кэш, нэг хүсэлтийг хуваалцана.
- **`queryFn`** — өгөгдлийг буцаах async функц. Алдаа гарвал **алдаа шидэх**
  ёстой: `fetch` 500-д алдаа шиддэггүй тул `response.ok`-ийг шалгахгүй бол
  TanStack Query алдааны JSON-ийг амжилттай өгөгдөл гэж хүлээж авна.
- **`isPending`** — өгөгдөл хараахан алга (анх ачаалж байна).
- **`isError`**, **`error`** — `queryFn` алдаа шидсэн.
- **`data`** — амжилттай бол өгөгдөл.
- **`isFetching`** — ард нь дахин татаж байна (кэштэй өгөгдөл харагдаж
  байхад ч `true` байж болно).
- **`refetch()`** — гараар дахин татах, «Дахин оролдох» товчинд тохиромжтой.

Effect, `useState` бичээгүйг анзаараарай. TanStack Query хариуг
түлхүүрээр нь кэшлэдэг тул хуучин хүсэлтийн хариу шинэ өгөгдлийг дарж
бичихгүй. Хүсэлтийг бодитоор цуцлах бол `queryFn`-д ирэх `signal`-ийг
`fetch`-д дамжуулна: `queryFn: ({ signal }) => fetch(url, { signal })…`.

TanStack Query-гийн v4 болон түүнээс өмнөх хувилбарын заавар дээр
`isLoading`, `useQuery(["courses"], fetchCourses)` гэсэн бичлэг харагдана.
v5-д `isPending` болж, `useQuery` зөвхөн объект хүлээн авдаг болсон.

### Параметртэй түлхүүр

```jsx
function CourseDetail({ id }) {
  const { data: course, isPending } = useQuery({
    queryKey: ["courses", id],
    queryFn: () => fetchJson(`/api/courses/${id}`),
  });
  // …
}
```

`id` өөрчлөгдөхөд түлхүүр өөрчлөгдөж шинэ хүсэлт автоматаар явна —
effect-ийн dependency-тэй ижил санаа. `queryFn`-д хэрэглэсэн хувьсагч бүр
түлхүүрт орох ёстой: `queryKey: ["course"]` гэж бичвэл бүх id-д нэг кэш
хэрэглэгдэж, өөр сургалт руу ороход хуучин сургалт харагдана.

### Кэш хэрхэн ажилладаг вэ

- Анхдагч `staleTime: 0` — татсан даруй «хуучирсан» гэж тооцно. Дараагийн
  удаа component mount болоход кэшээс **шууд** харуулж, ард нь дахин татна
  (stale-while-revalidate).
- `staleTime: 60 * 1000` өгвөл 1 минут «шинэ» гэж үзэж дахин татахгүй.
- `gcTime` (анхдагч 5 минут) — ямар ч component ашиглахаа больсон кэшийг
  хэдий хугацааны дараа устгах.
- Хэрэглэгч tab руугаа буцаж ирэхэд (`refetchOnWindowFocus`), интернет
  сэргэхэд хуучирсан query-г автоматаар дахин татна.

Бодит төсөлд `@tanstack/react-query-devtools` суулгаж `<ReactQueryDevtools />`
нэмбэл кэшид юу байгаа, аль query хуучирсныг харж болно.

### Retry ба тест

`queryFn` алдаа шидвэл TanStack Query анхдагчаар **3 удаа дахин** оролдоно
(1, 2, 4 секундын завсартай). Сүлжээ түр тасарсан үед энэ нь сайн. Гэвч
алдааны мэдэгдэл ~7 секундын дараа л гарна — тестэд хэтэрхий удаан.
Тиймээс тест болон энэ дасгалд:

```jsx
const queryClient = new QueryClient({
  defaultOptions: { queries: { retry: false } },
});
```

Бодит аппад анхдагчийг үлдээж, тестийн `QueryClient`-д л унтраадаг.

```quiz
`Header` ба `CourseList` хоёулаа `useQuery({ queryKey: ["courses"], queryFn: fetchCourses })` дуудвал хэдэн хүсэлт явах вэ?
- [ ] 2 — component бүр өөрийн хүсэлттэй
- [x] 1 — ижил түлхүүртэй query-ууд нэг хүсэлт, нэг кэшийг хуваалцана
- [ ] 0 — кэш хоосон тул юу ч татахгүй
> Энэ бол dedupe: зэрэг явах ижил хүсэлтүүд нэгддэг. Өмнөх хичээлийн давхардлын асуудал алга боллоо.
```

```quiz
`queryFn: () => fetch("/api/courses")` гэж бичвэл `data.map(…)` дээр юу болох вэ?
- [ ] Ажиллана — `fetch` JSON буцаадаг
- [x] `data.map is not a function` — `data` нь JSON биш, `Response` объект
- [ ] TanStack Query JSON-ийг автоматаар уншина
> `queryFn` буцаасан утга яг `data` болно. `response.json()`-ийг өөрөө дуудаж, `response.ok`-ийг шалга.
```

### Дүгнэлт

`QueryClient` (кэш)-ийг нэг удаа үүсгэж, `QueryClientProvider`-оор апп-д
өгнө. `useQuery({ queryKey, queryFn })` нь `isPending`, `isError`, `data`-г
буцааж, кэш, dedupe, ард нь шинэчлэхийг өөрөө хийнэ. `queryFn` алдаан дээр
заавал алдаа шидэх ёстой.
""",
            initial_code=vite(
                """\
// TODO: @tanstack/react-query-оос useQuery-г импортол

async function fetchCourses() {
  // TODO: GET /api/courses — response.ok биш бол алдаа шид, эс бөгөөс JSON буцаа
}

function CourseCount() {
  // TODO: App-тай ИЖИЛ queryKey-тэй useQuery. data ирсэн бол «Нийт: 5 сургалт».
  return <span>Нийт: … сургалт</span>;
}

export default function App() {
  // TODO: const { data, isPending, isError, error } = useQuery({ … });
  // isPending → «Ачаалж байна…», isError → role="alert" мэдэгдэл, эс бөгөөс жагсаалт

  return (
    <>
      <header>
        📚 Medleghub · <CourseCount />
      </header>
      <main>
        <h1>Сургалтууд</h1>
      </main>
    </>
  );
}
""",
                css=DATA_CSS,
                main="""\
import { createRoot } from "react-dom/client";
// TODO: @tanstack/react-query-оос QueryClient, QueryClientProvider-ийг импортол
import App from "./App";
import "./styles.css";

// TODO: queryClient үүсгэ. Энэ дасгалд алдааг шууд харахын тулд retry: false:
// new QueryClient({ defaultOptions: { queries: { retry: false } } })

createRoot(document.getElementById("root")).render(
  // TODO: <App />-ийг <QueryClientProvider client={queryClient}>-оор бүрх
  <App />,
);
""",
                main_locked=False,
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐ · 15 минут

Хоёр алхамтай. Эхлээд `main.jsx`-д `QueryClient` үүсгэж (энэ дасгалд
`retry: false`), `App`-ийг `QueryClientProvider`-оор бүрх. Дараа нь
`App.jsx`-д `fetchCourses`-ийг гүйцээж, `App` ба `CourseCount` хоёулаа
ижил `queryKey`-тэй `useQuery` ашигладаг болго. `App` ачаалж байхад
«Ачаалж байна…», алдаа гарвал `role="alert"` мэдэгдэл, амжилттай бол
сургалтуудын жагсаалтыг харуулна.
""",
                tests=(
                    test(
                        "Ачаалж байхад «Ачаалж байна…», дараа нь 5 сургалт жагсаалтад харагдана",
                        """
await runMain();
expect(screen.text()).toContain("Ачаалж байна");
await waitFor(() => expect(screen.getAllByRole("listitem")).toHaveLength(5));
expect(screen.getAllByRole("listitem")[2]).toHaveTextContent("React-ээр апп бүтээх");
expect(screen.text()).not.toContain("Ачаалж байна");
""",
                    ),
                    test(
                        "Хоёр component ижил queryKey ашиглаж, ганц GET хүсэлт илгээнэ",
                        """
await runMain();
await waitFor(() => expect(screen.getAllByRole("listitem")).toHaveLength(5));
await waitFor(() => expect(screen.text()).toContain("Нийт: 5 сургалт"));
const gets = api.requests.filter(
  (request) => request.method === "GET" && request.path.startsWith("/api/courses"),
);
expect(gets).toHaveLength(1);
""",
                    ),
                    test(
                        'Серверийн алдааг role="alert" мэдэгдлээр харуулна',
                        """
api.fail("/api/courses", 500);
await runMain();
const alerts = await screen.findAllByRole("alert");
expect(alerts.length).toBeGreaterThan(0);
expect(screen.queryAllByRole("listitem")).toHaveLength(0);
expect(screen.text()).not.toContain("Ачаалж байна");
""",
                    ),
                ),
                tips="""\
- `main.jsx`: `import { QueryClient, QueryClientProvider } from "@tanstack/react-query";`
  → `const queryClient = new QueryClient({ … })` component-ийн гадна →
  `render(<QueryClientProvider client={queryClient}><App /></QueryClientProvider>)`.
- «No QueryClient set» алдаа гарвал Provider дутуу байна.
- `fetchCourses`: `fetch` → `if (!response.ok) throw new Error(…)` →
  `return response.json()`.
- Хоёр component-д яг ижил `queryKey: ["courses"]`. Өөр түлхүүр
  (`["count"]`) өгвөл хоёр хүсэлт явна.
- Алдааны тест 2 секундээс удаан хүлээгдээд унавал `retry: false`-ийг
  мартсан байна.
""",
                solution=files(
                    (
                        "App.jsx",
                        """\
import { useQuery } from "@tanstack/react-query";

async function fetchCourses() {
  const response = await fetch("/api/courses");
  if (!response.ok) {
    throw new Error(`Сервер ${response.status} алдаа буцаалаа`);
  }
  return response.json();
}

function CourseCount() {
  const { data } = useQuery({ queryKey: ["courses"], queryFn: fetchCourses });
  return <span>Нийт: {data ? data.length : "…"} сургалт</span>;
}

export default function App() {
  const { data, isPending, isError, error } = useQuery({
    queryKey: ["courses"],
    queryFn: fetchCourses,
  });

  let content;
  if (isPending) {
    content = <p role="status">Ачаалж байна…</p>;
  } else if (isError) {
    content = <p role="alert">Сургалтуудыг ачаалж чадсангүй: {error.message}</p>;
  } else {
    content = (
      <ul>
        {data.map((course) => (
          <li key={course.id}>
            {course.title} · {course.level}
          </li>
        ))}
      </ul>
    );
  }

  return (
    <>
      <header>
        📚 Medleghub · <CourseCount />
      </header>
      <main>
        <h1>Сургалтууд</h1>
        {content}
      </main>
    </>
  );
}
""",
                    ),
                    (
                        "main.jsx",
                        """\
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { createRoot } from "react-dom/client";
import App from "./App";
import "./styles.css";

const queryClient = new QueryClient({
  defaultOptions: { queries: { retry: false } },
});

createRoot(document.getElementById("root")).render(
  <QueryClientProvider client={queryClient}>
    <App />
  </QueryClientProvider>,
);
""",
                    ),
                ),
            ),
        ),
        # ------------------------------------------------------------------ 9.6
        LessonSpec(
            title="useMutation ба кэш шинэчлэх",
            slug="usemutation",
            description="mutate, isPending, onSuccess дотор invalidateQueries ба setQueryData.",
            duration=1080,
            language=JSX,
            content="""\
### Энэ хичээлээр

- `useMutation`-оор өгөгдөл өөрчлөх хүсэлт илгээх
- `mutate`, `isPending`, `isError`-ийг UI-д ашиглах
- `onSuccess` дотор `invalidateQueries`-ээр кэшийг шинэчлүүлэх
- `setQueryData`-тай харьцуулж, аль нь хэзээ тохирохыг мэдэх

### Яагаад чухал вэ

`useQuery` зөвхөн уншихад зориулагдсан. Ажил нэмэх, тэмдэглэх, устгахад
сервер дээрх өгөгдөл өөрчлөгдөж, кэш дэх хуулбар хуучирна. Кэшид «чи
хуучирлаа» гэж хэн нэгэн хэлэхгүй бол дэлгэц өөрчлөлтийг харуулахгүй.
`useMutation` хүсэлтийн төлвийг (pending, error) удирдаж, амжилттай
болсны дараа кэшийг шинэчлэх газрыг өгнө.

### useMutation

```jsx
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { request } from "./api";

function AddTodo() {
  const queryClient = useQueryClient();

  const addTodo = useMutation({
    mutationFn: (title) =>
      request("/api/todos", {
        method: "POST",
        body: JSON.stringify({ title, done: false }),
      }),
    onSuccess: () => {
      return queryClient.invalidateQueries({ queryKey: ["todos"] });
    },
  });

  return (
    <button onClick={() => addTodo.mutate("Сүү авах")} disabled={addTodo.isPending}>
      {addTodo.isPending ? "Нэмж байна…" : "Нэмэх"}
    </button>
  );
}
```

- **`mutationFn`** — өөрчлөлтийг хийх async функц. `mutate(x)`-д өгсөн
  утгыг аргумент болгон авна. `queryFn`-ий адил алдаа гарвал **алдаа
  шидэх** ёстой.
- **`mutate(variables)`** — хүсэлтийг эхлүүлнэ. Render хийх үед биш, event
  handler дотор дуудна.
- **`isPending`**, **`isError`**, **`error`**, **`isSuccess`** — яг одоогийн
  хүсэлтийн төлөв.
- **`useQueryClient()`** — `QueryClientProvider`-т өгсөн кэшийг авна.

`useQuery`-ээс ялгаатай нь mutation өөрөө эхлэхгүй (та `mutate` дуудна),
кэшлэгдэхгүй, алдаанд дахин оролдохгүй (анхдагч `retry: 0`) — өөрчлөлтийг
санамсаргүй хоёр удаа илгээхгүйн тулд.

### invalidateQueries — «энэ кэш хуучирлаа»

`queryClient.invalidateQueries({ queryKey: ["todos"] })` нь `["todos"]`-ээр
**эхэлсэн** бүх query-г хуучирсан гэж тэмдэглээд, дэлгэцэд харагдаж
байгааг нь дахин татна: `["todos"]`, `["todos", 3]`,
`["todos", { done: false }]` бүгд хамаарна. Хамгийн энгийн, найдвартай
арга — хамгийн сүүлийн үнэнийг сервер өгнө.

`onSuccess`-ээс Promise буцаавал (`return queryClient.invalidateQueries(…)`)
жагсаалт дахин татагдаж дуустал mutation `isPending` хэвээр байна. Ингэснээр
«Нэмж байна…» шинэ жагсаалт гарах хүртэл харагдаж, товч эрт идэвхжихгүй.

### setQueryData — кэшийг гараар шинэчлэх

```jsx
onSuccess: (created) => {
  queryClient.setQueryData(["todos"], (old = []) => [...old, created]);
},
```

Серверийн хариугаар кэшийг шууд засна — нэмэлт хүсэлтгүй, хурдан. Гэхдээ
серверийн логикийг (эрэмбэ, шүүлтүүр, тоолуур) давтах шаардлага гардаг.
Кэш дэх өгөгдлийг ч immutable шинэчилнэ: `old.push(created)` бүү хий.
Эхлээд `invalidateQueries`, хурд чухал газар `setQueryData` гэж санаарай.

### Дуудалт бүрийн callback

```jsx
addTodo.mutate(title, {
  onSuccess: () => setTitle(""), // зөвхөн энэ дуудалтад
});
```

`useMutation`-ийн `onSuccess` нь «үргэлж хийх» ажилд (кэш шинэчлэх),
`mutate(…, { onSuccess })` нь тухайн component-ийн UI-д (input цэвэрлэх,
өөр хуудас руу шилжих) тохирно.

`mutateAsync` нь Promise буцаадаг тул `await` хийж болно, гэхдээ алдааг
өөрөө `try`/`catch`-аар барих ёстой. `mutate` алдааг өөрөө барьж
`isError` болгодог — ихэнх үед хангалттай.

### Түгээмэл алдаанууд

- **Буруу түлхүүр** — `["todo"]`-г хүчингүй болгосон ч query нь
  `["todos"]` → юу ч шинэчлэгдэхгүй.
- **`response.ok` шалгаагүй** — 500 ч «амжилттай» болж, `onSuccess` ажиллана.
- **Render дотор `mutate()`** — render бүрт хүсэлт явж, төгсгөлгүй давталт.

Хариуг хүлээлгүй шууд харуулах optimistic update-ийг Модул 11-д
`useOptimistic`-оор үзнэ. TanStack Query-д үүнийг `onMutate`-ээр хийдэг.

```quiz
`invalidateQueries({ queryKey: ["todos"] })` аль query-г хуучирсан болгох вэ?
- [ ] Зөвхөн яг `["todos"]`
- [x] `["todos"]` ба `["todos", 5]` хоёулаа
- [ ] Кэш дэх бүх query
> Түлхүүр угтвараар (prefix) тааруулагддаг. Нэг ажлын `["todos", 5]` ч жагсаалтын хамт шинэчлэгдэнэ.
```

```quiz
Mutation амжилттай болсон ч жагсаалт шинэчлэгдэхгүй байна. `onSuccess: () => queryClient.invalidateQueries({ queryKey: ["todo"] })`, жагсаалт нь `useQuery({ queryKey: ["todos"], … })`. Алдаа юу вэ?
- [ ] `onSuccess` дотор `await` бичээгүй
- [x] Түлхүүр таарахгүй: `["todo"]` нь `["todos"]`-ийн угтвар биш
- [ ] `useMutation` кэшийг шинэчилж чаддаггүй
> `invalidateQueries`-ийн түлхүүр query-ийн түлхүүрийн эхлэлтэй яг таарах ёстой.
```

### Дүгнэлт

`useMutation` өөрчлөлтийн хүсэлтийг илгээж, `isPending`, `isError`-ийг
өгнө. Амжилттай болсны дараа `invalidateQueries`-ээр холбогдох query-г
дахин татуулж, эсвэл `setQueryData`-гаар кэшийг шууд засна. Ингэснээр
дэлгэцийн бүх хэсэг нэг кэшээс шинэ өгөгдлийг харна.
""",
            initial_code=vite(
                """\
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { request } from "./api";

export default function App() {
  const [title, setTitle] = useState("");
  const todos = useQuery({
    queryKey: ["todos"],
    queryFn: () => request("/api/todos"),
  });

  // TODO 1: addTodo = useMutation — POST /api/todos, body { title, done: false }.
  //         Амжилттай бол ["todos"]-ийг invalidateQueries (Promise-ийг нь буцаа).
  // TODO 2: toggleTodo = useMutation — PATCH /api/todos/:id, body { done: !todo.done },
  //         мөн амжилттай бол invalidateQueries.

  function handleSubmit(event) {
    event.preventDefault();
    const text = title.trim();
    if (!text) return;
    // TODO: addTodo.mutate(text, { onSuccess: () => setTitle("") });
  }

  return (
    <main>
      <h1>✅ Ажлын жагсаалт</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Шинэ ажил <input value={title} onChange={(event) => setTitle(event.target.value)} />
        </label>
        {/* TODO: нэмж байх үед товчийг disabled болгож «Нэмж байна…» гэж бич */}
        <button type="submit">Нэмэх</button>
      </form>
      {/* TODO: addTodo алдаатай бол role="alert" мэдэгдэл */}

      {todos.isPending && <p role="status">Ачаалж байна…</p>}
      {todos.isError && <p role="alert">{todos.error.message}</p>}
      {todos.data && (
        <ul>
          {todos.data.map((todo) => (
            <li key={todo.id}>
              <label>
                <input
                  type="checkbox"
                  checked={todo.done}
                  onChange={() => {
                    // TODO: toggleTodo.mutate(todo);
                  }}
                />{" "}
                {todo.title}
              </label>
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}
""",
                locked={
                    "api.js": """\
// Бүх хүсэлт энэ функцээр явна: JSON header ба алдааны шалгалт нэг газар.
export async function request(url, options = {}) {
  const response = await fetch(url, {
    ...options,
    headers: { "Content-Type": "application/json", ...options.headers },
  });
  if (!response.ok) {
    throw new Error(`Сервер ${response.status} алдаа буцаалаа`);
  }
  return response.json();
}
"""
                },
                css=DATA_CSS,
                main="""\
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { createRoot } from "react-dom/client";
import App from "./App";
import "./styles.css";

// retry: false — алдааг дахин оролдолгүй шууд харуулна (тестэд хурдан).
const queryClient = new QueryClient({
  defaultOptions: { queries: { retry: false } },
});

createRoot(document.getElementById("root")).render(
  <QueryClientProvider client={queryClient}>
    <App />
  </QueryClientProvider>,
);
""",
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐ · 15 минут

Жагсаалт `useQuery`-ээр аль хэдийн татагдаж байна. `useMutation`-оор хоёр
өөрчлөлт нэм: формоор шинэ ажил үүсгэх (`POST`), checkbox-оор дууссан
эсэхийг солих (`PATCH`). Хоёулаа амжилттай болсны дараа `["todos"]`-ийг
`invalidateQueries`-ээр дахин татуулна. Нэмж байх үед товч идэвхгүй болж
«Нэмж байна…» гэж бичигдэх, нэмэхэд алдаа гарвал `role="alert"`
мэдэгдэл харагдах ёстой. `request` туслах функц 🔒 `api.js`-д бэлэн.
""",
                tests=(
                    test(
                        "Шинэ ажил POST-оор хадгалагдаж, жагсаалтад гарч, input цэвэрлэгдэнэ",
                        """
await runMain();
await screen.findByText("React хичээл үзэх");
await user.type(screen.getByLabelText("Шинэ ажил"), "Сүү авах{enter}");
expect(await screen.findByText("Сүү авах")).toBeInTheDocument();
const saved = api.get("todos").find((todo) => todo.title === "Сүү авах");
expect(saved && saved.done).toBe(false);
await waitFor(() => expect(screen.getByLabelText("Шинэ ажил")).toHaveValue(""));
""",
                    ),
                    test(
                        "Нэмсний дараа жагсаалтыг серверээс дахин татна (invalidateQueries)",
                        """
const todoGets = () =>
  api.requests.filter((request) => request.method === "GET" && request.path.startsWith("/api/todos"))
    .length;
await runMain();
await screen.findByText("React хичээл үзэх");
expect(todoGets()).toBe(1);
await user.type(screen.getByLabelText("Шинэ ажил"), "Сүү авах{enter}");
await screen.findByText("Сүү авах");
await waitFor(() => expect(todoGets()).toBeGreaterThan(1));
""",
                    ),
                    test(
                        "Нэмж байх үед товч идэвхгүй болж «Нэмж байна…» гэж бичигдэнэ",
                        """
await runMain();
await screen.findByText("React хичээл үзэх");
const realFetch = window.fetch;
window.fetch = async (input, init) => {
  await sleep(300);
  return realFetch(input, init);
};
try {
  await user.type(screen.getByLabelText("Шинэ ажил"), "Сүү авах{enter}");
  const pending = await screen.findByRole("button", { name: /Нэмж байна/ });
  expect(pending).toBeDisabled();
  await waitFor(() => expect(screen.getByRole("button", { name: "Нэмэх" })).toBeEnabled());
} finally {
  window.fetch = realFetch;
}
""",
                    ),
                    test(
                        "Checkbox дарахад PATCH-аар done солигдож, жагсаалт шинэчлэгдэнэ",
                        """
await runMain();
await user.click(await screen.findByRole("checkbox", { name: "useState дасгал хийх" }));
await waitFor(() =>
  expect(screen.getByRole("checkbox", { name: "useState дасгал хийх" })).toBeChecked(),
);
expect(api.requests.some((r) => r.method === "PATCH" && r.path === "/api/todos/2")).toBe(true);
expect(api.get("todos").find((todo) => todo.id === 2).done).toBe(true);
""",
                    ),
                    test(
                        'Нэмэх үед сервер алдаа буцаавал role="alert" мэдэгдэл харагдана',
                        """
await runMain();
await screen.findByText("React хичээл үзэх");
api.fail("/api/todos", 500);
await user.type(screen.getByLabelText("Шинэ ажил"), "Сүү авах{enter}");
expect(await screen.findByRole("alert")).toBeInTheDocument();
expect(screen.getAllByRole("listitem")).toHaveLength(3);
""",
                    ),
                ),
                tips="""\
- `const queryClient = useQueryClient();` — component дотор, hook-уудын
  дунд.
- `useMutation({ mutationFn: (text) => request("/api/todos", { method: "POST", body: JSON.stringify(…) }), onSuccess: () => queryClient.invalidateQueries({ queryKey: ["todos"] }) })`
- `toggleTodo`-ийн `mutationFn` нь `todo`-г бүтнээр нь авч, замд
  `todo.id`, body-д `{ done: !todo.done }` илгээнэ.
- Товч: `disabled={addTodo.isPending}`, текст нь
  `addTodo.isPending ? "Нэмж байна…" : "Нэмэх"`.
- Алдаа: `addTodo.isError && <p role="alert">{addTodo.error.message}</p>`.
- `mutate`-ийг render дотор биш, `handleSubmit`, `onChange` дотор дууд.
""",
                solution=solution(
                    App_jsx="""\
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { request } from "./api";

export default function App() {
  const [title, setTitle] = useState("");
  const queryClient = useQueryClient();
  const todos = useQuery({
    queryKey: ["todos"],
    queryFn: () => request("/api/todos"),
  });

  const addTodo = useMutation({
    mutationFn: (text) =>
      request("/api/todos", {
        method: "POST",
        body: JSON.stringify({ title: text, done: false }),
      }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["todos"] }),
  });

  const toggleTodo = useMutation({
    mutationFn: (todo) =>
      request(`/api/todos/${todo.id}`, {
        method: "PATCH",
        body: JSON.stringify({ done: !todo.done }),
      }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["todos"] }),
  });

  function handleSubmit(event) {
    event.preventDefault();
    const text = title.trim();
    if (!text) return;
    addTodo.mutate(text, { onSuccess: () => setTitle("") });
  }

  return (
    <main>
      <h1>✅ Ажлын жагсаалт</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Шинэ ажил <input value={title} onChange={(event) => setTitle(event.target.value)} />
        </label>
        <button type="submit" disabled={addTodo.isPending}>
          {addTodo.isPending ? "Нэмж байна…" : "Нэмэх"}
        </button>
      </form>
      {addTodo.isError && (
        <p role="alert">Ажлыг хадгалж чадсангүй: {addTodo.error.message}</p>
      )}

      {todos.isPending && <p role="status">Ачаалж байна…</p>}
      {todos.isError && <p role="alert">{todos.error.message}</p>}
      {todos.data && (
        <ul>
          {todos.data.map((todo) => (
            <li key={todo.id}>
              <label>
                <input
                  type="checkbox"
                  checked={todo.done}
                  disabled={toggleTodo.isPending}
                  onChange={() => toggleTodo.mutate(todo)}
                />{" "}
                {todo.title}
              </label>
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}
"""
                ),
            ),
        ),
        # ------------------------------------------------------------------ 9.7
        LessonSpec(
            title="Төсөл: Сургалтын самбар",
            slug="tusul-surgaltyn-samber",
            description="Сургалт татах, дэлгэрэнгүй, бүртгүүлэх, явц шинэчлэх — TanStack Query-тэй самбар.",
            duration=2700,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Модул 9-д сурсан бүхнээ нэг апп болгон нэгтгэх: REST API, `useQuery`,
  `useMutation`, кэш
- Серверийн өгөгдлийг `api.js` → `queries.js` → хуудас гэсэн давхаргад
  хуваах
- Ачаалах, алдаа, хоосон төлвийг хуудас бүрт зөв харуулах
- Өөрчлөлтийн дараа кэшийг шинэчилж, бүх хуудсыг нэг үнэнтэй байлгах

### Яагаад чухал вэ

Бодит апп-д нэг өгөгдлийг хэд хэдэн хуудас хэрэглэдэг: самбар таны
сургалтуудыг, сургалтын хуудас бүртгэл ба явцыг харуулна. Нэг газар
өөрчлөхөд бусад нь шууд шинэчлэгдэх ёстой. Энэ төсөл Medleghub-ийн
жинхэнэ самбарын жижиг хувилбар бөгөөд серверийн state-ийг TanStack
Query-гээр удирдах бүтэн хэв маягийг харуулна.

### Юу бүтээх вэ

```text
/               Самбар: «Миний сургалтууд» (явцтай) ба «Бүх сургалт»
/courses/:id    Сургалтын хуудас: мэдээлэл, «Бүртгүүлэх», явц, «Хичээл дуусгах»
*               404 (бэлэн)
```

### Файлын бүтэц

```text
App.jsx                      ← route-ууд ба layout (бэлэн)
api.js                       ← fetch функцууд (2 нь TODO)
queries.js                   ← TanStack Query hook-ууд (4 нь TODO)
pages/Dashboard.jsx          ← самбар («Миний сургалтууд» TODO)
pages/CourseDetail.jsx       ← сургалтын хуудас (TODO)
components/Status.jsx        ← <Loading />, <ErrorMessage /> (бэлэн)
components/ProgressBar.jsx   ← явцын мөр (бэлэн)
styles.css                   ← загвар (хүссэнээрээ өөрчил)
main.jsx 🔒                  ← QueryClientProvider, BrowserRouter
```

Бодит төсөлд ийм гурван давхарга түгээмэл: **`api.js`** зөвхөн HTTP
хүсэлт мэднэ, **`queries.js`** кэшийн түлхүүр ба invalidation-ийг нэг
газарт төвлөрүүлнэ, **хуудсууд** зөвхөн `useCourse(id)` гэх мэт hook
дуудна. Түлхүүрийг хуудас бүрт гараар бичихгүй тул `["enrollment"]`,
`["enrollments"]` гэж андуурах боломжгүй.

### API

| Хүсэлт | Хариу |
|---|---|
| `GET /api/courses` | `[{ id, title, level, lessons, category }]` — 5 сургалт |
| `GET /api/courses/:id` | Нэг сургалт, байхгүй бол `404` |
| `GET /api/enrollments` | `[{ id, courseId, completed }]` — эхэндээ хоосон |
| `POST /api/enrollments` | body `{ courseId, completed: 0 }` → үүссэн бүртгэл (`201`) |
| `PATCH /api/enrollments/:id` | body `{ completed }` → шинэчилсэн бүртгэл |

`completed` нь дуусгасан хичээлийн тоо, `lessons` нь нийт хичээл.

### Кэшийн тохиргоо

🔒 `main.jsx`-д:

```jsx
const queryClient = new QueryClient({
  defaultOptions: {
    queries: { staleTime: 30 * 1000, retry: false },
  },
});
```

`staleTime` 30 секунд гэдэг нь татсан өгөгдлийг хагас минут «шинэ» гэж
үзэж дахин татахгүй гэсэн үг. Самбар ба сургалтын хуудасны хооронд шилжихэд «Ачаалж
байна…» гарахгүй, кэшээс шууд харагдана. Гэхдээ энэ нь **өөрчлөлтийн
дараа кэшийг заавал хүчингүй болгох** ёстой гэсэн үг: `invalidateQueries`
хийхгүй бол бүртгүүлсэн сургалт 30 секундын турш хаана ч харагдахгүй.

### Шаардлага

1. **api.js** — `enroll(courseId)` нь `POST /api/enrollments`,
   `updateProgress(id, completed)` нь `PATCH /api/enrollments/:id`.
   Бэлэн `request` функцийг ашигла.
2. **queries.js** — `useCourse(id)` (түлхүүр `["courses", id]`),
   `useEnrollments()` (`["enrollments"]`), `useEnroll()`,
   `useUpdateProgress()`. Хоёр mutation амжилттай болсны дараа
   `["enrollments"]`-ийг invalidate хийнэ.
3. **CourseDetail** — ачаалж байхад `<Loading />`, алдаа гарвал
   `<ErrorMessage error={…} onRetry={…} />`. h1 нь сургалтын нэр, доор нь
   түвшин ба хичээлийн тоо. Бүртгэлгүй бол «Бүртгүүлэх» товч, бүртгэлтэй
   бол `<ProgressBar />` ба «Хичээл дуусгах» товч (+1 хичээл, бүгдийг
   дуусгасан бол идэвхгүй). Хүсэлт явж байхад товч идэвхгүй.
4. **Dashboard** — «Миний сургалтууд» хэсэгт бүртгэл бүрийн сургалтын нэр
   (сургалтын хуудас руу холбоос) ба `<ProgressBar />`. Бүртгэл байхгүй
   бол «Та одоогоор ямар ч сургалтад бүртгүүлээгүй байна.»

### Зөвлөмж

- Эхлээд `api.js`, дараа нь `queries.js`, тэгээд хуудсуудаа хий.
- `useParams`-ийн утга string — `Number(id)`. Үгүй бол `courseId: "2"`
  хадгалагдаж, `2 === "2"` худал болно.
- Бүртгэлээ `enrollments.data.find((item) => item.courseId === courseId)`-оор ол.
- Бүртгэлд сургалтын нэр, хичээлийн тоо байхгүй — тэдгээр нь `courses`-д
  бий. Самбарт бүртгэл бүрт тохирох сургалтыг `courseId`-аар ол.
- «Хөтөч» дээр алдааг турших: `/courses/99` (404) руу ор — «Дахин оролдох»
  харагдах ёстой.

```quiz
Бүртгүүлсний дараа `invalidateQueries`-ийг мартвал (`staleTime` 30 секунд) юу болох вэ?
- [ ] Самбар бүртгэлийг шууд харуулна — TanStack Query POST-ийг өөрөө мэддэг
- [x] Хуучин (хоосон) бүртгэлийн жагсаалт 30 секунд кэшээс харагдана
- [ ] Апп алдаа шиднэ
> TanStack Query ямар mutation ямар query-д нөлөөлөхийг мэдэхгүй — үүнийг `invalidateQueries`-ээр хэлж өгнө.
```

```quiz
Сургалтын хуудсанд `queryKey: ["course"]` (id-гүй) гэж бичвэл юу болох вэ?
- [ ] Ажиллана — `queryFn` дотор id бий
- [x] Эхэлж нээсэн сургалт бусад бүх сургалтын хуудсанд кэшээс харагдана
- [ ] TanStack Query id-г автоматаар нэмнэ
> Түлхүүр кэшийн «хаяг». `queryFn`-д хэрэглэсэн хувьсагч бүр түлхүүрт орох ёстой: `["courses", id]`.
```

### Дүгнэлт

REST API, `useQuery`, `useMutation`, invalidation, ачаалах ба алдааны
төлвийг нэг апп-д нэгтгэлээ. `api.js` → `queries.js` → хуудас гэсэн
давхарга нь түлхүүр ба хүсэлтийг нэг газар барьж, хуудсуудыг энгийн
үлдээнэ. Дараагийн модульд React хэрхэн render хийдгийг гүнзгий үзнэ.
""",
            initial_code=vite(
                """\
import { NavLink, Outlet, Route, Routes } from "react-router";
import CourseDetail from "./pages/CourseDetail";
import Dashboard from "./pages/Dashboard";

function Layout() {
  return (
    <div className="app">
      <header className="topbar">
        <strong>📊 Medleghub</strong>
        <nav>
          <NavLink to="/" end>
            Самбар
          </NavLink>
        </nav>
      </header>
      <main className="content">
        <Outlet />
      </main>
    </div>
  );
}

function NotFound() {
  return (
    <section className="card">
      <h1>Хуудас олдсонгүй</h1>
    </section>
  );
}

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="courses/:id" element={<CourseDetail />} />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}
""",
                extra={
                    "api.js": """\
// Бүх хүсэлт энэ функцээр явна: JSON header ба алдааны шалгалт нэг газар.
async function request(url, options = {}) {
  const response = await fetch(url, {
    ...options,
    headers: { "Content-Type": "application/json", ...options.headers },
  });
  if (!response.ok) {
    throw new Error(`Сервер ${response.status} алдаа буцаалаа`);
  }
  return response.json();
}

export const getCourses = () => request("/api/courses");
export const getCourse = (id) => request(`/api/courses/${id}`);
export const getEnrollments = () => request("/api/enrollments");

// TODO: POST /api/enrollments — body: { courseId, completed: 0 }
export function enroll(courseId) {}

// TODO: PATCH /api/enrollments/:id — body: { completed }
export function updateProgress(id, completed) {}
""",
                    "queries.js": """\
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { enroll, getCourse, getCourses, getEnrollments, updateProgress } from "./api";

// Жишээ: бүх сургалт. queryKey — кэшийн түлхүүр.
export function useCourses() {
  return useQuery({ queryKey: ["courses"], queryFn: getCourses });
}

// TODO: нэг сургалт — queryKey: ["courses", id]
export function useCourse(id) {}

// TODO: бүх бүртгэл — queryKey: ["enrollments"]
export function useEnrollments() {}

// TODO: бүртгүүлэх mutation — mutate(courseId).
// Амжилттай бол ["enrollments"]-ийг invalidate.
export function useEnroll() {}

// TODO: явц шинэчлэх mutation — mutate({ id, completed }).
// Амжилттай бол ["enrollments"]-ийг invalidate.
export function useUpdateProgress() {}
""",
                    "pages/Dashboard.jsx": """\
import { Link } from "react-router";
import ProgressBar from "../components/ProgressBar";
import { ErrorMessage, Loading } from "../components/Status";
import { useCourses } from "../queries";

export default function Dashboard() {
  const courses = useCourses();
  // TODO: useEnrollments()

  return (
    <>
      <h1>Сургалтын самбар</h1>

      <section className="card">
        <h2>Миний сургалтууд</h2>
        {/* TODO: бүртгэл бүрт сургалтын нэр (холбоос) ба <ProgressBar />.
            Бүртгэл байхгүй бол «Та одоогоор ямар ч сургалтад бүртгүүлээгүй байна.» */}
      </section>

      <section className="card">
        <h2>Бүх сургалт</h2>
        {courses.isPending && <Loading />}
        {courses.isError && <ErrorMessage error={courses.error} onRetry={courses.refetch} />}
        {courses.data && (
          <ul className="course-grid">
            {courses.data.map((course) => (
              <li key={course.id}>
                <Link to={`/courses/${course.id}`}>{course.title}</Link>
                <p className="muted">
                  {course.level} · {course.lessons} хичээл
                </p>
              </li>
            ))}
          </ul>
        )}
      </section>
    </>
  );
}
""",
                    "pages/CourseDetail.jsx": """\
import { Link, useParams } from "react-router";
import ProgressBar from "../components/ProgressBar";
import { ErrorMessage, Loading } from "../components/Status";
// TODO: queries.js-ээс хэрэгтэй hook-уудаа импортол

export default function CourseDetail() {
  const { id } = useParams();
  const courseId = Number(id);

  // TODO: useCourse(courseId), useEnrollments(), useEnroll(), useUpdateProgress()
  // 1. Ачаалж байхад <Loading />, алдаа гарвал <ErrorMessage error={…} onRetry={…} />
  // 2. h1 — сургалтын нэр, доор нь түвшин ба хичээлийн тоо
  // 3. Бүртгэлгүй бол «Бүртгүүлэх» товч (хүсэлт явж байхад идэвхгүй)
  // 4. Бүртгэлтэй бол <ProgressBar /> ба «Хичээл дуусгах» товч (+1)

  return (
    <section className="card">
      <Link to="/">← Самбар</Link>
      <p>TODO: сургалт #{courseId}</p>
    </section>
  );
}
""",
                    "components/ProgressBar.jsx": """\
export default function ProgressBar({ completed, total }) {
  const percent = total > 0 ? Math.round((completed / total) * 100) : 0;

  return (
    <div className="progress">
      <progress value={completed} max={total} aria-label="Явц" />
      <span>
        {completed} / {total} хичээл · {percent}%
      </span>
    </div>
  );
}
""",
                    "components/Status.jsx": """\
export function Loading() {
  return (
    <p role="status" className="muted">
      Ачаалж байна…
    </p>
  );
}

export function ErrorMessage({ error, onRetry }) {
  return (
    <div role="alert" className="error">
      <p>Алдаа гарлаа: {error.message}</p>
      {onRetry && <button onClick={() => onRetry()}>Дахин оролдох</button>}
    </div>
  );
}
""",
                },
                css="""\
body {
  margin: 0;
  font-family: system-ui, sans-serif;
  background: #f6f8fa;
  color: #1f2328;
}

.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding: 10px 16px;
  background: #1f2328;
  color: #fff;
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

.content {
  max-width: 720px;
  margin: 0 auto;
  padding: 16px;
}

.card {
  padding: 16px;
  margin-bottom: 12px;
  border: 1px solid #d0d7de;
  border-radius: 12px;
  background: #fff;
}

.card h2 {
  margin-top: 0;
  font-size: 18px;
}

.course-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 12px;
  padding: 0;
  list-style: none;
}

.course-grid li {
  padding: 12px;
  border: 1px solid #d0d7de;
  border-radius: 8px;
}

.my-courses {
  padding: 0;
  list-style: none;
}

.my-courses li {
  display: grid;
  gap: 4px;
  padding: 8px 0;
  border-bottom: 1px solid #eaeef2;
}

.progress {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 8px 0;
}

.progress progress {
  flex: 1;
  accent-color: #2da44e;
}

.muted {
  color: #57606a;
}

.error {
  padding: 10px 12px;
  border: 1px solid #f1aeb5;
  border-radius: 8px;
  background: #fff5f5;
  color: #b42318;
}

button {
  padding: 6px 12px;
  border: 1px solid #2da44e;
  border-radius: 6px;
  background: #2da44e;
  color: #fff;
  cursor: pointer;
}

button:disabled {
  opacity: 0.6;
  cursor: default;
}

.error button {
  border-color: #b42318;
  background: #fff;
  color: #b42318;
}
""",
                css_locked=False,
                main="""\
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router";
import App from "./App";
import "./styles.css";

// staleTime: татсан өгөгдлийг 30 секунд «шинэ» гэж үзэж, дахин татахгүй.
// retry: false — алдааг дахин оролдолгүй шууд харуулна (тестэд хурдан).
const queryClient = new QueryClient({
  defaultOptions: {
    queries: { staleTime: 30 * 1000, retry: false },
  },
});

createRoot(document.getElementById("root")).render(
  <QueryClientProvider client={queryClient}>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </QueryClientProvider>,
);
""",
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐⭐ · 45 минут

Хичээлийн «Шаардлага»-ыг дагаж `api.js`, `queries.js`-ийн TODO-г
гүйцээгээд, `CourseDetail` ба самбарын «Миний сургалтууд» хэсгийг бич.
Хэсэг бүрийг дуусгах бүрт «Хөтөч» дээр сургалт руу орж бүртгүүлээд,
хичээл дуусгаад, самбар руу буцаж шалгаарай.
""",
                tests=(
                    test(
                        "Сургалтын хуудас ачаалах төлвийн дараа нэр, түвшин, хичээлийн тоог харуулна",
                        """
setPath("/courses/3");
await runMain();
expect(screen.getAllByRole("status").length).toBeGreaterThan(0);
expect(await screen.findByRole("heading", { name: /React-ээр апп бүтээх/ })).toBeInTheDocument();
expect(screen.text()).toContain("Дунд");
expect(screen.text()).toContain("80");
expect(api.requests.some((r) => r.method === "GET" && r.path === "/api/courses/3")).toBe(true);
""",
                    ),
                    test(
                        "«Бүртгүүлэх» дарахад POST /api/enrollments илгээгдэж, явц харагдана",
                        """
setPath("/courses/2");
await runMain();
await user.click(await screen.findByRole("button", { name: "Бүртгүүлэх" }));
await waitFor(() => expect(screen.text()).toContain("0 / 90"));
const saved = api.get("enrollments");
expect(saved).toHaveLength(1);
expect(saved[0].courseId).toBe(2);
expect(saved[0].completed).toBe(0);
expect(screen.getByRole("button", { name: "Хичээл дуусгах" })).toBeEnabled();
""",
                    ),
                    test(
                        "«Хичээл дуусгах» дарахад PATCH-аар явц 1-ээр нэмэгдэнэ",
                        """
api.set("enrollments", [{ id: 1, courseId: 3, completed: 5 }]);
setPath("/courses/3");
await runMain();
await waitFor(() => expect(screen.text()).toContain("5 / 80"));
await user.click(screen.getByRole("button", { name: "Хичээл дуусгах" }));
await waitFor(() => expect(screen.text()).toContain("6 / 80"));
expect(api.get("enrollments")[0].completed).toBe(6);
expect(api.requests.some((r) => r.method === "PATCH" && r.path === "/api/enrollments/1")).toBe(
  true,
);
""",
                    ),
                    test(
                        "Самбар хоосон үед тайлбар, бүртгүүлсний дараа «Миний сургалтууд»-д явцтай нь харагдана",
                        """
await runMain();
expect(await screen.findByText(/бүртгүүлээгүй/)).toBeInTheDocument();
await user.click(screen.getByRole("link", { name: "JavaScript үндэс" }));
await user.click(await screen.findByRole("button", { name: "Бүртгүүлэх" }));
await waitFor(() => expect(screen.text()).toContain("0 / 90"));
await user.click(screen.getByRole("link", { name: "Самбар" }));
expect(screen.getByRole("heading", { name: "Миний сургалтууд" })).toBeInTheDocument();
await waitFor(() => expect(screen.text()).toContain("0 / 90"));
expect(screen.queryByText(/бүртгүүлээгүй/)).toBeNull();
""",
                    ),
                    test(
                        "Алдаа гарвал мэдэгдэл харагдаж, «Дахин оролдох» дарахад дахин ачаална",
                        """
api.fail("/api/courses/4", 500);
setPath("/courses/4");
await runMain();
const retry = await screen.findByRole("button", { name: "Дахин оролдох" });
expect(screen.getByRole("alert")).toBeInTheDocument();
api.reset(); // сервер сэргэлээ
await user.click(retry);
expect(await screen.findByRole("heading", { name: /Python програмчлал/ })).toBeInTheDocument();
expect(screen.queryByRole("alert")).toBeNull();
""",
                    ),
                ),
                tips="""\
- `api.js`: `request("/api/enrollments", { method: "POST", body: JSON.stringify({ courseId, completed: 0 }) })`
  — `request`-ийг `return` хийхээ бүү март.
- `queries.js`: mutation hook дотор `const queryClient = useQueryClient();`,
  `onSuccess: () => queryClient.invalidateQueries({ queryKey: ["enrollments"] })`.
  `useUpdateProgress`-ийн `mutationFn` нь `({ id, completed }) => updateProgress(id, completed)`.
- `CourseDetail`: `course` ба `enrollments` хоёулаа ачаалагдсаны дараа л
  товч харуул — эс бөгөөс бүртгэлтэй хэрэглэгчид «Бүртгүүлэх» түр
  харагдана.
- «Хичээл дуусгах»: `mutate({ id: enrollment.id, completed: enrollment.completed + 1 })`.
- «Дахин оролдох»: `onRetry={course.refetch}`.
- Самбар: `courses.data.find((course) => course.id === enrollment.courseId)`.
""",
                solution=files(
                    (
                        "api.js",
                        """\
// Бүх хүсэлт энэ функцээр явна: JSON header ба алдааны шалгалт нэг газар.
async function request(url, options = {}) {
  const response = await fetch(url, {
    ...options,
    headers: { "Content-Type": "application/json", ...options.headers },
  });
  if (!response.ok) {
    throw new Error(`Сервер ${response.status} алдаа буцаалаа`);
  }
  return response.json();
}

export const getCourses = () => request("/api/courses");
export const getCourse = (id) => request(`/api/courses/${id}`);
export const getEnrollments = () => request("/api/enrollments");

export function enroll(courseId) {
  return request("/api/enrollments", {
    method: "POST",
    body: JSON.stringify({ courseId, completed: 0 }),
  });
}

export function updateProgress(id, completed) {
  return request(`/api/enrollments/${id}`, {
    method: "PATCH",
    body: JSON.stringify({ completed }),
  });
}
""",
                    ),
                    (
                        "queries.js",
                        """\
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { enroll, getCourse, getCourses, getEnrollments, updateProgress } from "./api";

export function useCourses() {
  return useQuery({ queryKey: ["courses"], queryFn: getCourses });
}

export function useCourse(id) {
  return useQuery({ queryKey: ["courses", id], queryFn: () => getCourse(id) });
}

export function useEnrollments() {
  return useQuery({ queryKey: ["enrollments"], queryFn: getEnrollments });
}

export function useEnroll() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (courseId) => enroll(courseId),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["enrollments"] }),
  });
}

export function useUpdateProgress() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, completed }) => updateProgress(id, completed),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["enrollments"] }),
  });
}
""",
                    ),
                    (
                        "pages/Dashboard.jsx",
                        """\
import { Link } from "react-router";
import ProgressBar from "../components/ProgressBar";
import { ErrorMessage, Loading } from "../components/Status";
import { useCourses, useEnrollments } from "../queries";

function MyCourses({ courses, enrollments }) {
  if (enrollments.length === 0) {
    return <p className="muted">Та одоогоор ямар ч сургалтад бүртгүүлээгүй байна.</p>;
  }

  return (
    <ul className="my-courses">
      {enrollments.map((enrollment) => {
        const course = courses.find((item) => item.id === enrollment.courseId);
        if (!course) return null;
        return (
          <li key={enrollment.id}>
            <Link to={`/courses/${course.id}`}>{course.title}</Link>
            <ProgressBar completed={enrollment.completed} total={course.lessons} />
          </li>
        );
      })}
    </ul>
  );
}

export default function Dashboard() {
  const courses = useCourses();
  const enrollments = useEnrollments();

  return (
    <>
      <h1>Сургалтын самбар</h1>

      <section className="card">
        <h2>Миний сургалтууд</h2>
        {(courses.isPending || enrollments.isPending) && <Loading />}
        {enrollments.isError && (
          <ErrorMessage error={enrollments.error} onRetry={enrollments.refetch} />
        )}
        {courses.data && enrollments.data && (
          <MyCourses courses={courses.data} enrollments={enrollments.data} />
        )}
      </section>

      <section className="card">
        <h2>Бүх сургалт</h2>
        {courses.isPending && <Loading />}
        {courses.isError && <ErrorMessage error={courses.error} onRetry={courses.refetch} />}
        {courses.data && (
          <ul className="course-grid">
            {courses.data.map((course) => (
              <li key={course.id}>
                <Link to={`/courses/${course.id}`}>{course.title}</Link>
                <p className="muted">
                  {course.level} · {course.lessons} хичээл
                </p>
              </li>
            ))}
          </ul>
        )}
      </section>
    </>
  );
}
""",
                    ),
                    (
                        "pages/CourseDetail.jsx",
                        """\
import { Link, useParams } from "react-router";
import ProgressBar from "../components/ProgressBar";
import { ErrorMessage, Loading } from "../components/Status";
import { useCourse, useEnroll, useEnrollments, useUpdateProgress } from "../queries";

export default function CourseDetail() {
  const { id } = useParams();
  const courseId = Number(id);
  const course = useCourse(courseId);
  const enrollments = useEnrollments();
  const enroll = useEnroll();
  const updateProgress = useUpdateProgress();

  let body;
  if (course.isPending || enrollments.isPending) {
    body = <Loading />;
  } else if (course.isError) {
    body = <ErrorMessage error={course.error} onRetry={course.refetch} />;
  } else if (enrollments.isError) {
    body = <ErrorMessage error={enrollments.error} onRetry={enrollments.refetch} />;
  } else {
    const { title, level, lessons } = course.data;
    const enrollment = enrollments.data.find((item) => item.courseId === courseId);
    const failed = enroll.error ?? updateProgress.error;

    body = (
      <>
        <h1>{title}</h1>
        <p className="muted">
          Түвшин: {level} · {lessons} хичээл
        </p>

        {enrollment ? (
          <>
            <ProgressBar completed={enrollment.completed} total={lessons} />
            <button
              onClick={() =>
                updateProgress.mutate({ id: enrollment.id, completed: enrollment.completed + 1 })
              }
              disabled={updateProgress.isPending || enrollment.completed >= lessons}
            >
              Хичээл дуусгах
            </button>
            {enrollment.completed >= lessons && <p>🎉 Сургалтаа дуусгалаа!</p>}
          </>
        ) : (
          <button onClick={() => enroll.mutate(courseId)} disabled={enroll.isPending}>
            Бүртгүүлэх
          </button>
        )}

        {failed && (
          <p role="alert" className="error">
            Хадгалж чадсангүй: {failed.message}
          </p>
        )}
      </>
    );
  }

  return (
    <section className="card">
      <Link to="/">← Самбар</Link>
      {body}
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
