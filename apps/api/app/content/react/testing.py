"""Модул 13 — Тест.

Сурагч өөрөө `App.test.jsx` бичнэ; тестлэх component нь түгжигдсэн
(`App.jsx` 🔒). Импорт нь бодит төсөлтэй ижил (`vitest`,
`@testing-library/react`, `@testing-library/user-event`) бөгөөд sandbox-ийн
runtime руу холбогдоно (`react-runtime/test-file.ts`). Тест файл байхад
«Хөтөч» апп биш Vitest шиг тайлан харуулна.

Дасгалын шалгалт: `runTestFile()` нь сурагчийн тестийг жинхэнэ component
дээр ажиллуулж бүгд давахыг, дараа нь зориуд эвдэрсэн хувилбар бүр дээр
(`runTestFile(undefined, {"App.jsx": BUGGY})`) дор хаяж нэг нь унахыг
шаардана. Эвдэрсэн хувилбарыг зөв кодоос `_bug()`-оор үүсгэдэг тул хоёр нь
үргэлж зэрэгцэн шинэчлэгдэнэ.
"""

import json

from app.content.react.common import HTML, files, test
from app.content.types import ExerciseSpec, LessonSpec, ModuleSpec, ReactTestSpec
from app.models.enums import LessonLanguage

JSX = LessonLanguage.JSX


def _bug(source: str, old: str, new: str) -> str:
    """Зөв кодын нэг хэсгийг солиж алдаатай хувилбар үүсгэнэ."""
    assert source.count(old) == 1, f"«{old}» яг нэг удаа байх ёстой"
    return source.replace(old, new)


def _lesson_files(test_file: str, *locked: tuple[str, str]) -> str:
    """`App.test.jsx` (сурагч бичнэ) + түгжигдсэн файлууд + `index.html`."""
    return files(
        ("App.test.jsx", test_file),
        *((name, code, True) for name, code in locked),
        ("index.html", HTML, True),
    )


def _all_pass(name: str, minimum: int) -> ReactTestSpec:
    code = """
const results = await runTestFile();
for (const r of results) expect(r.passed ? "" : "✗ " + r.name + " — " + r.message).toBe("");
expect(results.length >= __MIN__ ? "" : "Дор хаяж __MIN__ тест бичнэ үү — одоо " + results.length + ".").toBe("");
"""
    return test(name, code.replace("__MIN__", str(minimum)))


def _catches(name: str, buggy: str, file: str = "App.jsx") -> ReactTestSpec:
    code = """
const results = await runTestFile(undefined, { __FILE__: __CODE__ });
expect(results.some((r) => !r.passed) ? "" : "Энэ алдаатай хувилбар дээр таны бүх тест давлаа — алдааг барих тест нэм.").toBe("");
"""
    return test(
        name,
        code.replace("__FILE__", json.dumps(file)).replace(
            "__CODE__", json.dumps(buggy, ensure_ascii=False)
        ),
    )


def _solution(test_file: str) -> str:
    return files(("App.test.jsx", test_file))


# --- 1. yagaad-test -----------------------------------------------------------------

UTILS = """\
export function formatPrice(amount) {
  return amount.toLocaleString("en-US") + "₮";
}

export function cartTotal(items) {
  return items.reduce((sum, item) => sum + item.price * item.qty, 0);
}
"""

UTILS_NO_QTY = _bug(UTILS, "sum + item.price * item.qty", "sum + item.price")
UTILS_NO_COMMA = _bug(UTILS, 'amount.toLocaleString("en-US") + "₮"', 'String(amount) + "₮"')

PRICE_TAG = """\
import { formatPrice } from "./utils";

export default function PriceTag({ amount }) {
  return <p>Үнэ: {formatPrice(amount)}</p>;
}
"""

WHY_STARTER = """\
import { describe, expect, test } from "vitest";
import { render, screen } from "@testing-library/react";
import PriceTag from "./App";
import { cartTotal, formatPrice } from "./utils";

// Жишээ: component-ийн тест (дараагийн хичээлд дэлгэрэнгүй үзнэ)
test("PriceTag үнийг ₮ тэмдэгтэй харуулна", () => {
  render(<PriceTag amount={500} />);
  expect(screen.getByText("Үнэ: 500₮")).toBeInTheDocument();
});

describe("formatPrice", () => {
  test("мянгатыг таслалаар тусгаарлана", () => {
    // TODO: formatPrice(12500) нь "12,500₮" болохыг шалга
  });
});

describe("cartTotal", () => {
  test("үнийг тоо ширхэгээр үржүүлж нэмнэ", () => {
    // TODO: тоо ширхэг нь 1-ээс их бараатай сагсны нийт дүнг шалга
  });

  test("хоосон сагсны дүн 0", () => {
    // TODO
  });
});
"""

WHY_SOLUTION = """\
import { describe, expect, test } from "vitest";
import { render, screen } from "@testing-library/react";
import PriceTag from "./App";
import { cartTotal, formatPrice } from "./utils";

test("PriceTag үнийг ₮ тэмдэгтэй харуулна", () => {
  render(<PriceTag amount={500} />);
  expect(screen.getByText("Үнэ: 500₮")).toBeInTheDocument();
});

describe("formatPrice", () => {
  test("мянгатыг таслалаар тусгаарлана", () => {
    expect(formatPrice(12500)).toBe("12,500₮");
    expect(formatPrice(1000000)).toBe("1,000,000₮");
  });
});

describe("cartTotal", () => {
  test("үнийг тоо ширхэгээр үржүүлж нэмнэ", () => {
    const items = [
      { price: 3500, qty: 2 },
      { price: 2800, qty: 1 },
    ];
    expect(cartTotal(items)).toBe(9800);
  });

  test("хоосон сагсны дүн 0", () => {
    expect(cartTotal([])).toBe(0);
  });
});
"""

# --- 2. anhny-test ------------------------------------------------------------------

PRODUCT_CARD = """\
export default function ProductCard({ product, onAdd }) {
  const soldOut = product.stock === 0;

  return (
    <article>
      <h2>
        <span aria-hidden="true">{product.emoji}</span> {product.name}
      </h2>
      <p>{product.price.toLocaleString("en-US")}₮</p>
      {soldOut && <p>Дууссан</p>}
      <button disabled={soldOut} onClick={() => onAdd?.(product)}>
        Сагсанд нэмэх
      </button>
    </article>
  );
}
"""

CARD_ALWAYS_ENABLED = _bug(PRODUCT_CARD, "disabled={soldOut}", "disabled={false}")
CARD_ALWAYS_SOLD_OUT = _bug(
    PRODUCT_CARD, "{soldOut && <p>Дууссан</p>}", "{product.stock >= 0 && <p>Дууссан</p>}"
)

FIRST_STARTER = """\
import { expect, test } from "vitest";
import { render, screen } from "@testing-library/react";
import ProductCard from "./App";

const banana = { id: 1, name: "Банана", price: 3500, emoji: "🍌", stock: 24 };
const broccoli = { id: 6, name: "Брокколи", price: 5200, emoji: "🥦", stock: 0 };

test("барааны нэрийг гарчиг болгож харуулна", () => {
  render(<ProductCard product={banana} />);
  expect(screen.getByRole("heading", { name: "Банана" })).toBeInTheDocument();
});

test("үнийг харуулна", () => {
  // TODO: render хийгээд "3,500₮" текст байгааг шалга
});

test("үлдэгдэлтэй бараанд «Дууссан» гэж бичигдэхгүй, товч идэвхтэй", () => {
  // TODO: queryByText ба toBeEnabled
});

test("дууссан бараанд «Дууссан» гэж бичигдэж, товч идэвхгүй", () => {
  // TODO: broccoli-г render хий — getByText ба toBeDisabled
});
"""

FIRST_SOLUTION = """\
import { expect, test } from "vitest";
import { render, screen } from "@testing-library/react";
import ProductCard from "./App";

const banana = { id: 1, name: "Банана", price: 3500, emoji: "🍌", stock: 24 };
const broccoli = { id: 6, name: "Брокколи", price: 5200, emoji: "🥦", stock: 0 };

test("барааны нэрийг гарчиг болгож харуулна", () => {
  render(<ProductCard product={banana} />);
  expect(screen.getByRole("heading", { name: "Банана" })).toBeInTheDocument();
});

test("үнийг харуулна", () => {
  render(<ProductCard product={banana} />);
  expect(screen.getByText("3,500₮")).toBeInTheDocument();
});

test("үлдэгдэлтэй бараанд «Дууссан» гэж бичигдэхгүй, товч идэвхтэй", () => {
  render(<ProductCard product={banana} />);
  expect(screen.queryByText("Дууссан")).not.toBeInTheDocument();
  expect(screen.getByRole("button", { name: "Сагсанд нэмэх" })).toBeEnabled();
});

test("дууссан бараанд «Дууссан» гэж бичигдэж, товч идэвхгүй", () => {
  render(<ProductCard product={broccoli} />);
  expect(screen.getByText("Дууссан")).toBeInTheDocument();
  expect(screen.getByRole("button", { name: "Сагсанд нэмэх" })).toBeDisabled();
});
"""

# --- 3. uildel-test -----------------------------------------------------------------

TODO_APP = """\
import { useState } from "react";

let nextId = 1;

export default function TodoApp() {
  const [todos, setTodos] = useState([]);
  const [text, setText] = useState("");

  function handleSubmit(event) {
    event.preventDefault();
    const title = text.trim();
    if (!title) return;
    setTodos([...todos, { id: nextId++, title }]);
    setText("");
  }

  function remove(id) {
    setTodos(todos.filter((todo) => todo.id !== id));
  }

  return (
    <main>
      <h1>Хийх ажлууд</h1>
      <form onSubmit={handleSubmit}>
        <label htmlFor="new-todo">Шинэ ажил</label>{" "}
        <input id="new-todo" value={text} onChange={(e) => setText(e.target.value)} />{" "}
        <button type="submit">Нэмэх</button>
      </form>
      <p>Нийт: {todos.length}</p>
      <ul>
        {todos.map((todo) => (
          <li key={todo.id}>
            {todo.title}{" "}
            <button onClick={() => remove(todo.id)} aria-label={`${todo.title} устгах`}>
              ✕
            </button>
          </li>
        ))}
      </ul>
    </main>
  );
}
"""

TODO_ADDS_EMPTY = _bug(TODO_APP, "    if (!title) return;\n", "")
TODO_WRONG_DELETE = _bug(
    TODO_APP,
    "setTodos(todos.filter((todo) => todo.id !== id));",
    "setTodos(todos.slice(1));",
)
TODO_KEEPS_TEXT = _bug(TODO_APP, '    setText("");\n', "")

ACTION_STARTER = """\
import { expect, test } from "vitest";
import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import TodoApp from "./App";

test("бичээд «Нэмэх» дарахад жагсаалтад нэмэгдэнэ", async () => {
  const user = userEvent.setup();
  render(<TodoApp />);

  await user.type(screen.getByLabelText("Шинэ ажил"), "Сүү авах");
  await user.click(screen.getByRole("button", { name: "Нэмэх" }));

  expect(screen.getByRole("listitem")).toHaveTextContent("Сүү авах");
});

test("нэмсний дараа талбар хоосорно", async () => {
  // TODO: бичээд {Enter} дар → талбарын утга "" (toHaveValue)
});

test("хоосон бол нэмэгдэхгүй", async () => {
  // TODO: зөвхөн хоосон зай бичээд «Нэмэх» дар → listitem байхгүй
});

test("✕ дарахад зөвхөн тэр ажил устна", async () => {
  // TODO: хоёр ажил нэмээд ХОЁР ДАХЬ-ийг нь устга (within)
});
"""

ACTION_SOLUTION = """\
import { expect, test } from "vitest";
import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import TodoApp from "./App";

test("бичээд «Нэмэх» дарахад жагсаалтад нэмэгдэнэ", async () => {
  const user = userEvent.setup();
  render(<TodoApp />);

  await user.type(screen.getByLabelText("Шинэ ажил"), "Сүү авах");
  await user.click(screen.getByRole("button", { name: "Нэмэх" }));

  expect(screen.getByRole("listitem")).toHaveTextContent("Сүү авах");
});

test("нэмсний дараа талбар хоосорно", async () => {
  const user = userEvent.setup();
  render(<TodoApp />);
  const input = screen.getByLabelText("Шинэ ажил");

  await user.type(input, "Ном унших{Enter}");

  expect(input).toHaveValue("");
  expect(screen.getByText("Нийт: 1")).toBeInTheDocument();
});

test("хоосон бол нэмэгдэхгүй", async () => {
  const user = userEvent.setup();
  render(<TodoApp />);

  await user.type(screen.getByLabelText("Шинэ ажил"), "   ");
  await user.click(screen.getByRole("button", { name: "Нэмэх" }));

  expect(screen.queryAllByRole("listitem")).toHaveLength(0);
  expect(screen.getByText("Нийт: 0")).toBeInTheDocument();
});

test("✕ дарахад зөвхөн тэр ажил устна", async () => {
  const user = userEvent.setup();
  render(<TodoApp />);
  const input = screen.getByLabelText("Шинэ ажил");
  await user.type(input, "Сүү авах{Enter}");
  await user.type(input, "Ном унших{Enter}");

  const items = screen.getAllByRole("listitem");
  await user.click(within(items[1]).getByRole("button", { name: /устгах/ }));

  const left = screen.getAllByRole("listitem");
  expect(left).toHaveLength(1);
  expect(left[0]).toHaveTextContent("Сүү авах");
});
"""

# --- 4. form-test -------------------------------------------------------------------

SIGNUP_FORM = """\
import { useState } from "react";

export default function SignupForm({ onSubmit }) {
  const [values, setValues] = useState({ name: "", email: "", password: "" });
  const [errors, setErrors] = useState({});

  function handleChange(event) {
    setValues({ ...values, [event.target.name]: event.target.value });
  }

  function handleSubmit(event) {
    event.preventDefault();
    const next = {};
    if (!values.name.trim()) next.name = "Нэрээ оруулна уу";
    if (!values.email.includes("@")) next.email = "Имэйл буруу байна";
    if (values.password.length < 6) next.password = "Нууц үг дор хаяж 6 тэмдэгт байна";
    setErrors(next);
    if (Object.keys(next).length > 0) return;
    onSubmit({ name: values.name.trim(), email: values.email, password: values.password });
  }

  return (
    <form onSubmit={handleSubmit} noValidate>
      <h2>Шинэ хэрэглэгч</h2>
      <p>
        <label htmlFor="name">Нэр</label>{" "}
        <input id="name" name="name" value={values.name} onChange={handleChange} />
      </p>
      {errors.name && <p role="alert">{errors.name}</p>}
      <p>
        <label htmlFor="email">Имэйл</label>{" "}
        <input id="email" name="email" type="email" value={values.email} onChange={handleChange} />
      </p>
      {errors.email && <p role="alert">{errors.email}</p>}
      <p>
        <label htmlFor="password">Нууц үг</label>{" "}
        <input
          id="password"
          name="password"
          type="password"
          value={values.password}
          onChange={handleChange}
        />
      </p>
      {errors.password && <p role="alert">{errors.password}</p>}
      <button type="submit">Бүртгүүлэх</button>
    </form>
  );
}
"""

FORM_SUBMITS_INVALID = _bug(SIGNUP_FORM, "    if (Object.keys(next).length > 0) return;\n", "")
FORM_DROPS_PASSWORD = _bug(
    SIGNUP_FORM,
    "onSubmit({ name: values.name.trim(), email: values.email, password: values.password });",
    "onSubmit({ name: values.name.trim(), email: values.email });",
)
FORM_OFF_BY_ONE = _bug(SIGNUP_FORM, "values.password.length < 6", "values.password.length < 5")

FORM_HELPER = """\
import { expect, test, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import SignupForm from "./App";

// Туслах: хоосон утга ("") өгсөн талбарыг бөглөхгүй орхино.
async function fillForm(user, { name = "Бат", email = "bat@example.mn", password = "secret1" } = {}) {
  if (name) await user.type(screen.getByLabelText("Нэр"), name);
  if (email) await user.type(screen.getByLabelText("Имэйл"), email);
  if (password) await user.type(screen.getByLabelText("Нууц үг"), password);
}

test("хоосон илгээхэд нэрийн алдаа гарна", async () => {
  const user = userEvent.setup();
  render(<SignupForm onSubmit={vi.fn()} />);

  await user.click(screen.getByRole("button", { name: "Бүртгүүлэх" }));

  expect(screen.getByText("Нэрээ оруулна уу")).toBeInTheDocument();
});
"""

FORM_STARTER = (
    FORM_HELPER
    + """
test("зөв бөглөөд илгээхэд onSubmit-ийг өгөгдөлтэй нь дуудна", async () => {
  // TODO: const handleSubmit = vi.fn(); … await fillForm(user); … toHaveBeenCalledWith
});

test("алдаатай үед onSubmit дуудагдахгүй", async () => {
  // TODO: жишээ нь имэйлгүй бөглөөд илгээ → not.toHaveBeenCalled()
});

test("имэйлд @ байхгүй бол алдаа гарна", async () => {
  // TODO: await fillForm(user, { email: "bat.example.mn" });
});

test("нууц үг 6-аас богино бол алдаа гарна", async () => {
  // TODO: хилийн утга — яг 5 тэмдэгт
});
"""
)

FORM_SOLUTION = (
    FORM_HELPER
    + """
test("зөв бөглөөд илгээхэд onSubmit-ийг өгөгдөлтэй нь дуудна", async () => {
  const handleSubmit = vi.fn();
  const user = userEvent.setup();
  render(<SignupForm onSubmit={handleSubmit} />);

  await fillForm(user);
  await user.click(screen.getByRole("button", { name: "Бүртгүүлэх" }));

  expect(handleSubmit).toHaveBeenCalledTimes(1);
  expect(handleSubmit).toHaveBeenCalledWith({
    name: "Бат",
    email: "bat@example.mn",
    password: "secret1",
  });
});

test("алдаатай үед onSubmit дуудагдахгүй", async () => {
  const handleSubmit = vi.fn();
  const user = userEvent.setup();
  render(<SignupForm onSubmit={handleSubmit} />);

  await fillForm(user, { email: "" });
  await user.click(screen.getByRole("button", { name: "Бүртгүүлэх" }));

  expect(screen.getByText("Имэйл буруу байна")).toBeInTheDocument();
  expect(handleSubmit).not.toHaveBeenCalled();
});

test("имэйлд @ байхгүй бол алдаа гарна", async () => {
  const user = userEvent.setup();
  render(<SignupForm onSubmit={vi.fn()} />);

  await fillForm(user, { email: "bat.example.mn" });
  await user.click(screen.getByRole("button", { name: "Бүртгүүлэх" }));

  expect(screen.getByText("Имэйл буруу байна")).toBeInTheDocument();
});

test("нууц үг 6-аас богино бол алдаа гарна", async () => {
  const handleSubmit = vi.fn();
  const user = userEvent.setup();
  render(<SignupForm onSubmit={handleSubmit} />);

  await fillForm(user, { password: "12345" });
  await user.click(screen.getByRole("button", { name: "Бүртгүүлэх" }));

  expect(screen.getByText("Нууц үг дор хаяж 6 тэмдэгт байна")).toBeInTheDocument();
  expect(handleSubmit).not.toHaveBeenCalled();
});

test("яг 6 тэмдэгттэй нууц үгийг зөвшөөрнө", async () => {
  const handleSubmit = vi.fn();
  const user = userEvent.setup();
  render(<SignupForm onSubmit={handleSubmit} />);

  await fillForm(user, { password: "123456" });
  await user.click(screen.getByRole("button", { name: "Бүртгүүлэх" }));

  expect(handleSubmit).toHaveBeenCalledTimes(1);
});
"""
)

# --- 5. async-mock-test -------------------------------------------------------------

USER_LIST = """\
import { useEffect, useState } from "react";

export async function fetchUsers() {
  const response = await fetch("/api/users");
  if (!response.ok) throw new Error("Сервер алдаа буцаалаа");
  return response.json();
}

// loadUsers: өгөгдөл татах функц — тестэд хуурамчаар сольж болно.
export default function UserList({ loadUsers = fetchUsers, onSelect }) {
  const [users, setUsers] = useState([]);
  const [status, setStatus] = useState("loading");
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    let ignore = false;
    setStatus("loading");
    Promise.resolve()
      .then(() => loadUsers())
      .then((data) => {
        if (ignore) return;
        setUsers(data);
        setStatus("done");
      })
      .catch(() => {
        if (!ignore) setStatus("error");
      });
    return () => {
      ignore = true;
    };
  }, [loadUsers, attempt]);

  if (status === "loading") return <p>Ачаалж байна…</p>;

  if (status === "error") {
    return (
      <div role="alert">
        <p>Хэрэглэгчдийг ачаалж чадсангүй.</p>
        <button onClick={() => setAttempt(attempt + 1)}>Дахин оролдох</button>
      </div>
    );
  }

  if (users.length === 0) return <p>Хэрэглэгч алга.</p>;

  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>
          <button onClick={() => onSelect?.(user)}>{user.name}</button>
        </li>
      ))}
    </ul>
  );
}
"""

USERS_HIDE_ERROR = _bug(
    USER_LIST, 'if (!ignore) setStatus("error");', 'if (!ignore) setStatus("done");'
)
USERS_NO_RETRY = _bug(USER_LIST, "}, [loadUsers, attempt]);", "}, [loadUsers]);")
USERS_SELECT_ID = _bug(USER_LIST, "onSelect?.(user)", "onSelect?.(user.id)")

ASYNC_HEAD = """\
import { expect, test, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import UserList from "./App";

test("эхлээд ачаалж, дараа нь API-ийн хэрэглэгчдийг харуулна", async () => {
  render(<UserList />);

  expect(screen.getByText("Ачаалж байна…")).toBeInTheDocument();
  expect(await screen.findByText("Бат")).toBeInTheDocument();
  expect(screen.getAllByRole("listitem")).toHaveLength(4);
});
"""

ASYNC_STARTER = (
    ASYNC_HEAD
    + """
test("алдаа гарвал мэдэгдэл харуулна", async () => {
  const loadUsers = vi.fn(async () => {
    throw new Error("Сервер унтарсан");
  });
  // TODO: render(<UserList loadUsers={loadUsers} />) → await findByRole("alert")
});

test("«Дахин оролдох» дарахад дахин ачаална", async () => {
  // TODO: эхний дуудалт алдаа шиддэг, хоёр дахь нь хэрэглэгч буцаадаг mock бич
});

test("хэрэглэгч дээр дарахад onSelect-ийг тэр хэрэглэгчээр дуудна", async () => {
  // TODO: onSelect = vi.fn() … toHaveBeenCalledWith(хэрэглэгчийн объект)
});
"""
)

ASYNC_SOLUTION = (
    ASYNC_HEAD
    + """
test("алдаа гарвал мэдэгдэл харуулна", async () => {
  const loadUsers = vi.fn(async () => {
    throw new Error("Сервер унтарсан");
  });
  render(<UserList loadUsers={loadUsers} />);

  expect(await screen.findByRole("alert")).toHaveTextContent("ачаалж чадсангүй");
  expect(loadUsers).toHaveBeenCalledTimes(1);
});

test("«Дахин оролдох» дарахад дахин ачаална", async () => {
  let calls = 0;
  const loadUsers = vi.fn(async () => {
    calls += 1;
    if (calls === 1) throw new Error("Түр алдаа");
    return [{ id: 1, name: "Сараа" }];
  });
  const user = userEvent.setup();
  render(<UserList loadUsers={loadUsers} />);

  await user.click(await screen.findByRole("button", { name: "Дахин оролдох" }));

  expect(await screen.findByText("Сараа")).toBeInTheDocument();
  expect(loadUsers).toHaveBeenCalledTimes(2);
});

test("хоосон жагсаалтад «Хэрэглэгч алга» гэнэ", async () => {
  render(<UserList loadUsers={vi.fn(async () => [])} />);

  expect(await screen.findByText("Хэрэглэгч алга.")).toBeInTheDocument();
});

test("хэрэглэгч дээр дарахад onSelect-ийг тэр хэрэглэгчээр дуудна", async () => {
  const saraa = { id: 2, name: "Сараа" };
  const loadUsers = vi.fn(async () => [{ id: 1, name: "Бат" }, saraa]);
  const onSelect = vi.fn();
  const user = userEvent.setup();
  render(<UserList loadUsers={loadUsers} onSelect={onSelect} />);

  await user.click(await screen.findByRole("button", { name: "Сараа" }));

  expect(onSelect).toHaveBeenCalledWith(saraa);
});
"""
)

# --- 6. tusul-test-nemeh ------------------------------------------------------------

SHOP_PRODUCTS = """\
export const products = [
  { id: 1, name: "Банана", price: 3500, emoji: "🍌" },
  { id: 2, name: "Алим", price: 2800, emoji: "🍎" },
  { id: 3, name: "Сүү", price: 3200, emoji: "🥛" },
];
"""

SHOP_APP = """\
import { useState } from "react";
import { products } from "./products";

export default function App() {
  const [cart, setCart] = useState([]);
  const [code, setCode] = useState("");
  const [discount, setDiscount] = useState(0);
  const [message, setMessage] = useState("");

  function add(product) {
    const existing = cart.find((line) => line.id === product.id);
    if (existing) {
      setCart(cart.map((line) => (line.id === product.id ? { ...line, qty: line.qty + 1 } : line)));
    } else {
      setCart([...cart, { ...product, qty: 1 }]);
    }
  }

  function decrease(id) {
    setCart(
      cart
        .map((line) => (line.id === id ? { ...line, qty: line.qty - 1 } : line))
        .filter((line) => line.qty > 0),
    );
  }

  function remove(id) {
    setCart(cart.filter((line) => line.id !== id));
  }

  function applyCode(event) {
    event.preventDefault();
    if (code.trim().toUpperCase() === "SALE10") {
      setDiscount(10);
      setMessage("10% хямдрал идэвхжлээ");
    } else {
      setDiscount(0);
      setMessage("Код буруу байна");
    }
  }

  const subtotal = cart.reduce((sum, line) => sum + line.price * line.qty, 0);
  const total = Math.round((subtotal * (100 - discount)) / 100);

  return (
    <main>
      <h1>Ногоон сагс</h1>
      <section aria-label="Бараа">
        <ul>
          {products.map((product) => (
            <li key={product.id}>
              {product.emoji} {product.name} — {product.price}₮{" "}
              <button onClick={() => add(product)} aria-label={`${product.name} нэмэх`}>
                Нэмэх
              </button>
            </li>
          ))}
        </ul>
      </section>
      <section aria-label="Сагс">
        <h2>Сагс</h2>
        {cart.length === 0 ? (
          <p>Сагс хоосон байна</p>
        ) : (
          <ul>
            {cart.map((line) => (
              <li key={line.id}>
                {line.name} × {line.qty} = {line.price * line.qty}₮{" "}
                <button onClick={() => decrease(line.id)} aria-label={`${line.name} хасах`}>
                  −
                </button>{" "}
                <button onClick={() => remove(line.id)} aria-label={`${line.name} устгах`}>
                  ✕
                </button>
              </li>
            ))}
          </ul>
        )}
        <form onSubmit={applyCode}>
          <label htmlFor="code">Хямдралын код</label>{" "}
          <input id="code" value={code} onChange={(e) => setCode(e.target.value)} />{" "}
          <button type="submit">Хэрэглэх</button>
        </form>
        {message && <p role="status">{message}</p>}
        <p>Нийт: {total}₮</p>
      </section>
    </main>
  );
}
"""

SHOP_TOTAL_NO_QTY = _bug(SHOP_APP, "sum + line.price * line.qty", "sum + line.price")
SHOP_DUPLICATES = _bug(
    SHOP_APP,
    "cart.find((line) => line.id === product.id)",
    "cart.find((line) => line.id === product)",
)
SHOP_KEEPS_ZERO = _bug(
    SHOP_APP, ".filter((line) => line.qty > 0)", ".filter((line) => line.qty >= 0)"
)
SHOP_FLAT_DISCOUNT = _bug(
    SHOP_APP, "Math.round((subtotal * (100 - discount)) / 100)", "subtotal - discount"
)

SHOP_HEAD = """\
import { describe, expect, test } from "vitest";
import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import App from "./App";

// «Банана» бараа ба сагс хоёуланд нь гардаг тул сагсны хэсэг дотор хайна.
function renderApp() {
  const user = userEvent.setup();
  render(<App />);
  const cart = screen.getByRole("region", { name: "Сагс" });
  return { user, cart };
}
"""

SHOP_STARTER = (
    SHOP_HEAD
    + """
describe("Ногоон сагс", () => {
  test("эхлэхэд сагс хоосон, нийт 0₮", () => {
    const { cart } = renderApp();
    expect(within(cart).getByText("Сагс хоосон байна")).toBeInTheDocument();
    expect(within(cart).getByText("Нийт: 0₮")).toBeInTheDocument();
  });

  // TODO: дор хаяж 4 тест нэм. App.jsx-ийг уншиж, хэрэглэгчийн хийж чадах
  //       бүх зүйлийг (нэмэх, хасах, устгах, хямдралын код) шалга.
});
"""
)

SHOP_SOLUTION = (
    SHOP_HEAD
    + """
describe("Ногоон сагс", () => {
  test("эхлэхэд сагс хоосон, нийт 0₮", () => {
    const { cart } = renderApp();
    expect(within(cart).getByText("Сагс хоосон байна")).toBeInTheDocument();
    expect(within(cart).getByText("Нийт: 0₮")).toBeInTheDocument();
  });

  test("бараа нэмэхэд сагсанд гарч, нийт шинэчлэгдэнэ", async () => {
    const { user, cart } = renderApp();
    await user.click(screen.getByRole("button", { name: "Алим нэмэх" }));

    expect(within(cart).getByText(/Алим × 1/)).toBeInTheDocument();
    expect(within(cart).getByText("Нийт: 2800₮")).toBeInTheDocument();
    expect(within(cart).queryByText("Сагс хоосон байна")).not.toBeInTheDocument();
  });

  test("ижил барааг хоёр нэмэхэд нэг мөрөнд тоо ширхэг нь 2 болно", async () => {
    const { user, cart } = renderApp();
    const addBanana = screen.getByRole("button", { name: "Банана нэмэх" });
    await user.click(addBanana);
    await user.click(addBanana);

    expect(within(cart).getAllByRole("listitem")).toHaveLength(1);
    expect(within(cart).getByText(/Банана × 2/)).toBeInTheDocument();
    expect(within(cart).getByText("Нийт: 7000₮")).toBeInTheDocument();
  });

  test("«−» дарахад тоо буурч, 1 байхад мөр устна", async () => {
    const { user, cart } = renderApp();
    const addMilk = screen.getByRole("button", { name: "Сүү нэмэх" });
    await user.click(addMilk);
    await user.click(addMilk);

    await user.click(within(cart).getByRole("button", { name: "Сүү хасах" }));
    expect(within(cart).getByText(/Сүү × 1/)).toBeInTheDocument();

    await user.click(within(cart).getByRole("button", { name: "Сүү хасах" }));
    expect(within(cart).getByText("Сагс хоосон байна")).toBeInTheDocument();
  });

  test("✕ дарахад зөвхөн тэр мөр устна", async () => {
    const { user, cart } = renderApp();
    await user.click(screen.getByRole("button", { name: "Банана нэмэх" }));
    await user.click(screen.getByRole("button", { name: "Алим нэмэх" }));

    await user.click(within(cart).getByRole("button", { name: "Банана устгах" }));

    expect(within(cart).getAllByRole("listitem")).toHaveLength(1);
    expect(within(cart).getByText(/Алим × 1/)).toBeInTheDocument();
    expect(within(cart).getByText("Нийт: 2800₮")).toBeInTheDocument();
  });

  test("SALE10 код нийт дүнг 10% хямдруулна", async () => {
    const { user, cart } = renderApp();
    const addBanana = screen.getByRole("button", { name: "Банана нэмэх" });
    await user.click(addBanana);
    await user.click(addBanana);

    await user.type(within(cart).getByLabelText("Хямдралын код"), "sale10{Enter}");

    expect(within(cart).getByRole("status")).toHaveTextContent("10% хямдрал идэвхжлээ");
    expect(within(cart).getByText("Нийт: 6300₮")).toBeInTheDocument();
  });

  test("буруу код хямдрал өгөхгүй", async () => {
    const { user, cart } = renderApp();
    await user.click(screen.getByRole("button", { name: "Сүү нэмэх" }));

    await user.type(within(cart).getByLabelText("Хямдралын код"), "FREE{Enter}");

    expect(within(cart).getByRole("status")).toHaveTextContent("Код буруу байна");
    expect(within(cart).getByText("Нийт: 3200₮")).toBeInTheDocument();
  });
});
"""
)

TESTING = ModuleSpec(
    title="Модул 13 — Тест",
    description=(
        "Vitest ба Testing Library-ийн аргаар component-ийн зан төлөвийг тестлэж, "
        "бэлэн аппад тест нэмнэ."
    ),
    lessons=[
        LessonSpec(
            title="Яагаад тест бичдэг вэ",
            slug="yagaad-test",
            description="Тестийн төрлүүд, Vitest + Testing Library, анхны test ба expect.",
            duration=840,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Автомат тест яагаад хэрэгтэйг ойлгох
- Unit, component, end-to-end тестийн ялгааг мэдэх
- Vitest + React Testing Library-г бодит төсөлд суулгах
- Анхны `test`, `expect`-ээ бичих

### Яагаад чухал вэ

Апп томрох тусам нэг газар засахад өөр газар эвдэрдэг (regression).
Бүх товчийг гараар дарж шалгах нь удаан бөгөөд ямар нэг зүйл заавал
мартагдана. Автомат тест хэдхэн секундэд бүгдийг шалгаж, «энэ өөрчлөлт
юуг ч эвдээгүй» гэсэн итгэлийг өгнө. Ингэснээр кодоо зоригтой refactor
хийж, багаараа ажиллахад хялбар болно. Тест бол бас ажилладаг баримт
бичиг: шинэ хөгжүүлэгч тестийг уншаад component юу хийдгийг ойлгоно.

Энэ сургалтын хичээл бүрийн тест ч яг ийм — таны кодыг автоматаар
шалгадаг. Одоо та өөрөө тест бичих болно.

### Тестийн төрлүүд

| Төрөл | Юуг шалгах | Хэрэгсэл | Хурд |
|---|---|---|---|
| Unit | Нэг функц (`formatPrice`) | Vitest | ⚡ мс |
| Component | Component-ийг хэрэглэгч шиг ашиглах | Vitest + React Testing Library | ⚡ мс |
| End-to-end (e2e) | Бүтэн апп жинхэнэ хөтөч дээр: нэвтрэх → сагс → төлбөр | Playwright, Cypress | 🐢 секунд |

React төсөлд ихэнх тест нь **component** түвшинд байдаг: хурдан ажиллаад
хэрэглэгчийн туршлагад ойр. Цөөн тооны e2e тест хамгийн чухал урсгалыг
(төлбөр төлөх) хамгаална.

### Бодит төсөлд суулгах

Vite төсөлд:

```bash
npm install -D vitest jsdom @testing-library/react @testing-library/dom @testing-library/user-event @testing-library/jest-dom
```

`vite.config.js`:

```jsx
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom", // Node дотор хуурамч DOM
    globals: true, // тест бүрийн дараа DOM-ыг автоматаар цэвэрлэнэ
    setupFiles: "./src/setupTests.js",
  },
});
```

`src/setupTests.js`:

```jsx
import "@testing-library/jest-dom/vitest"; // toBeInTheDocument гэх мэт
```

`package.json`-ийн `scripts`-д `"test": "vitest"` нэмээд `npm test`
ажиллуулна. Vitest файл хадгалах бүрт тестийг дахин ажиллуулдаг.
Тестийн файлыг component-ийнхээ хажууд `Button.test.jsx` гэж нэрлэнэ.

Энэ засварлагчид бүгд бэлэн: `App.test.jsx` файл байвал «Хөтөч» tab апп
биш **тестийн тайлан** харуулна. Импортууд нь бодит төсөлтэй яг ижил.

### Тестийн бүтэц

```jsx
import { describe, expect, test } from "vitest";
import { cartTotal } from "./utils";

describe("cartTotal", () => {
  test("үнийг тоо ширхэгээр үржүүлж нэмнэ", () => {
    // Бэлтгэх (Arrange)
    const items = [{ price: 1000, qty: 2 }, { price: 500, qty: 1 }];
    // Үйлдэл (Act)
    const total = cartTotal(items);
    // Шалгах (Assert)
    expect(total).toBe(2500);
  });
});
```

- `test(нэр, функц)` (эсвэл `it`) — нэг тест. Нэр нь юуг шалгахыг
  өгүүлбэрээр хэлнэ — унахад яг энэ нэр харагдана.
- `describe` — холбоотой тестүүдийг бүлэглэнэ.
- `expect(утга).toBe(хүлээгдэж буй)` — таарахгүй бол тест унана. Бусад:
  `toEqual` (объект, массивыг агуулгаар нь), `toContain`,
  `toBeGreaterThan`, үгүйсгэл `.not.toBe(…)`.

### Зан төлөвийг тестлэ, дотоод бүтцийг биш

Сайн тест хэрэглэгчид харагдах **үр дүнг** шалгана: «Нэмэх дарахад
сагсанд 1 бараа харагдана». Муу тест дотоод нарийн ширийнийг шалгана:
«state-ийн `items` массивын урт 1», «`handleAdd` функц дуудагдсан».

Дотоод бүтцийг өөрчлөхөд (`useState`-ийг `useReducer` болгох гэх мэт)
муу тест унана — апп зөв ажилласаар байхад. Ийм тест хамгаалалт биш,
саад болдог. Testing Library яг энэ зарчмаар бүтээгдсэн.

### Сайн тест алдааг барьдаг

Тест бичээд ногоон болсон нь хангалтгүй. Кодыг зориуд эвдэхэд
(жишээ нь `*`-ийг `+` болгоход) тест **улаан** болох ёстой. Үргэлж давдаг
тест бол хоосон тест. Энэ модулийн дасгалууд таны тестийг зориуд
эвдэрсэн хувилбарууд дээр ажиллуулж шалгана.

```quiz
Аль нь зан төлөвийн (behaviour) тест вэ?
- [x] «Нэмэх» дарахад «Сагс: 1» гэж харагдана
- [ ] `useState` хоёр удаа дуудагдсан
- [ ] Component 3 ширхэг `div` буцаадаг
- [ ] `handleAdd` функцийн нэр зөв
> Хэрэглэгч `useState`, `div`-ийн тоог хардаггүй. Тест ч мөн адил харах ёсгүй.
```

```quiz
`expect([1, 2]).toBe([1, 2])` юу болох вэ?
- [ ] Давна
- [x] Унана — `toBe` хаягаар нь харьцуулдаг тул `toEqual` хэрэгтэй
- [ ] Синтакс алдаа гарна
> Хоёр массив агуулгаараа ижил ч өөр хоёр объект. `toBe` нь `Object.is`, `toEqual` нь агуулгыг харьцуулна.
```

### Дүгнэлт

Автомат тест regression-оос хамгаалж, refactor хийх итгэл өгнө. Vitest
тестийг ажиллуулж, Testing Library component-ийг хэрэглэгч шиг ашиглана.
Тест нь зан төлөвийг шалгаж, эвдэрсэн кодон дээр унах ёстой.
""",
            initial_code=_lesson_files(WHY_STARTER, ("App.jsx", PRICE_TAG), ("utils.js", UTILS)),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐ · 10 минут

`utils.js` (🔒)-ийн хоёр функцэд тест бич: `App.test.jsx` дахь TODO
тестүүдийг гүйцээ. Үр дүнг «Хөтөч» tab-ийн тестийн тайлангаас хар. Таны
тестийг зөв код дээр, мөн зориуд эвдэрсэн хувилбарууд дээр ажиллуулна —
сайн тест эвдэрсэн кодон дээр унах ёстой.
""",
                tests=(
                    _all_pass("Таны бүх тест зөв код дээр амжилттай (дор хаяж 4 тест)", 4),
                    _catches(
                        "Тест cartTotal-ийн алдааг (тоо ширхэгийг тооцоогүй) барина",
                        UTILS_NO_QTY,
                        "utils.js",
                    ),
                    _catches(
                        "Тест formatPrice-ийн алдааг (мянгатын таслалгүй) барина",
                        UTILS_NO_COMMA,
                        "utils.js",
                    ),
                ),
                tips="""\
- `expect(formatPrice(12500)).toBe("12,500₮")`. 500 шиг жижиг тоо
  таслалын алдааг илрүүлэхгүй — яагаад гэдгийг бод.
- `cartTotal`-д тоо ширхэг нь 1-ээс их бараа хэрэгтэй: `qty: 1` бол
  үржүүлээгүй код ч зөв хариу өгнө.
- Хоосон TODO тест үргэлж давдаг — ийм тест юуг ч хамгаалдаггүй.
""",
                solution=_solution(WHY_SOLUTION),
            ),
        ),
        LessonSpec(
            title="Анхны component тест",
            slug="anhny-test",
            description="render, screen, expect ба хайлтын эрэмбэ: getByRole-оос getByTestId хүртэл.",
            duration=900,
            language=JSX,
            content="""\
### Энэ хичээлээр

- `render`, `screen`, `expect`-ээр component тестлэх
- Хайлтын эрэмбэ: `getByRole` → `getByLabelText` → `getByText` →
  `getByTestId`
- `getBy`, `queryBy`, `findBy`-ийн ялгаа
- DOM matcher-ууд: `toBeInTheDocument`, `toHaveTextContent`, `toBeDisabled`

### Яагаад чухал вэ

Хэрэглэгч class, id мэдэхгүй — гарчиг, товчны текст, талбарын шошгыг
хардаг. Testing Library-ийн хайлтууд үүнийг дуурайдаг тул дизайн,
бүтэц өөрчлөгдөхөд тест эвддэггүй. Дээр нь хүртээмжгүй UI-г (шошгогүй
input, `div` товч) илрүүлдэг: тест олж чадахгүй бол дэлгэц уншигч ч
олохгүй.

### render ба screen

```jsx
import { expect, test } from "vitest";
import { render, screen } from "@testing-library/react";
import Greeting from "./Greeting";

test("нэрээр мэндэлнэ", () => {
  render(<Greeting name="Сараа" />);
  expect(screen.getByRole("heading", { name: "Сайн уу, Сараа!" })).toBeInTheDocument();
});
```

`render` нь component-ийг тестийн DOM-д зурна; `screen` нь хуудас
даяар хайна. Тест бүр өөрийн `render`-тэй — тестийн дараа DOM
цэвэрлэгдэнэ.

### Аль хайлтыг сонгох вэ

Testing Library-ийн зөвлөдөг дараалал:

1. `getByRole("button", { name: "Хадгалах" })` — хамгийн сайн. Товч,
   гарчиг, холбоос, checkbox — дэлгэц уншигч ч ингэж хардаг.
2. `getByLabelText("Имэйл")` — формын талбар.
3. `getByPlaceholderText`, `getByText("Дууссан")` — энгийн текст.
4. `getByDisplayValue`, `getByAltText`, `getByTitle`.
5. `getByTestId("cart-total")` — `data-testid`. Бусад нь боломжгүй үед
   л.

Түгээмэл role: `button`, `heading` (`{ level: 2 }`), `link`, `textbox`,
`checkbox`, `listitem`, `img`, `alert`. `type="password"` input-д role
байхгүй — `getByLabelText` хэрэглэнэ.

`name` нь яг таарах текст эсвэл regex: `{ name: /сагс/i }`.
`getByText("Нийт", { exact: false })` нь текстийн хэсгээр хайна.

### getBy, queryBy, findBy

| | Олдвол | Олдохгүй бол | Хэзээ |
|---|---|---|---|
| `getBy…` | элемент | алдаа шиднэ | байх ёстой зүйлд |
| `queryBy…` | элемент | `null` | **байх ёсгүй** зүйлд |
| `findBy…` | Promise → элемент | хүлээгээд алдаа | асинхрон (13.5-р хичээл) |

Олон элемент: `getAllBy…`, `queryAllBy…`, `findAllBy…` → массив.
`getBy…` нэгээс олныг олбол ч алдаа шиднэ.

```jsx
expect(screen.queryByText("Дууссан")).not.toBeInTheDocument();
```

Түгээмэл алдаа:
`expect(screen.getByText("Дууссан")).not.toBeInTheDocument()` —
`getBy…` олдохгүй үед шууд алдаа шиддэг тул `.not` хүртэл очихгүй.

### DOM matcher-ууд

`@testing-library/jest-dom`-ийн matcher-ууд:

```jsx
expect(button).toBeInTheDocument();
expect(price).toHaveTextContent("3,500₮");
expect(button).toBeDisabled(); // эсвэл toBeEnabled()
expect(input).toHaveValue("Бат");
expect(checkbox).toBeChecked();
expect(link).toHaveAttribute("href", "/cart");
```

### Props-оор өөр өөр тохиолдол

Нэг component-ийг өөр props-оор хэд хэдэн удаа тестлэнэ: үлдэгдэлтэй
ба дууссан бараа, хоосон ба дүүрэн сагс. Тестийн өгөгдлийг файлын
эхэнд тогтмол болгож зарлавал давтагдахгүй.

```quiz
Дууссан бараанд «Сагсанд нэмэх» товч идэвхгүйг шалгах хамгийн зөв мөр аль вэ?
- [x] `expect(screen.getByRole("button", { name: "Сагсанд нэмэх" })).toBeDisabled()`
- [ ] `expect(screen.getByTestId("add-button").disabled).toBe(true)`
- [ ] `expect(container.querySelector("button").className).toContain("disabled")`
> Role ба нэрээр хайх нь хэрэглэгч товчийг хэрхэн хардагтай ижил. Class нь дизайн өөрчлөгдөхөд эвдэрнэ.
```

```quiz
`expect(screen.getByText("Алдаа")).not.toBeInTheDocument()` — «Алдаа» текст хуудсанд байхгүй үед юу болох вэ?
- [ ] Тест давна
- [x] Тест унана — `getByText` олдохгүй бол өөрөө алдаа шиднэ
- [ ] `null` буцаана
> Байхгүйг шалгахдаа `queryByText` хэрэглэнэ: олдохгүй бол `null` буцаадаг.
```

### Дүгнэлт

`render` зурж, `screen` хайж, `expect` шалгана. Хэрэглэгч шиг хай:
эхлээд `getByRole`, дараа нь `getByLabelText`, `getByText`. Байх ёсгүй
зүйлийг `queryBy…`-гаар шалгана.
""",
            initial_code=_lesson_files(FIRST_STARTER, ("App.jsx", PRODUCT_CARD)),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 12 минут

`App.jsx` (🔒) дахь `ProductCard`-д тест бич. Үлдэгдэлтэй (`banana`) ба
дууссан (`broccoli`) хоёр тохиолдлыг хоёуланг нь шалга. Эхний тест
бэлэн — түүнийг жишээ болгоод TODO-гуудыг гүйцээ.
""",
                tests=(
                    _all_pass("Таны бүх тест зөв component дээр амжилттай (дор хаяж 4 тест)", 4),
                    _catches(
                        "Тест дууссан бараанд товч идэвхтэй үлддэг алдааг барина",
                        CARD_ALWAYS_ENABLED,
                    ),
                    _catches(
                        "Тест үлдэгдэлтэй бараанд ч «Дууссан» гардаг алдааг барина",
                        CARD_ALWAYS_SOLD_OUT,
                    ),
                ),
                tips="""\
- Тест бүр өөрөө `render(<ProductCard product={…} />)` хийнэ.
- Байх ёсгүй текст: `expect(screen.queryByText("Дууссан")).not.toBeInTheDocument()`.
- Товч: `screen.getByRole("button", { name: "Сагсанд нэмэх" })`, дараа нь
  `toBeEnabled()` эсвэл `toBeDisabled()`.
- Үнэ `toLocaleString`-оор форматлагддаг: `"3,500₮"`.
""",
                solution=_solution(FIRST_SOLUTION),
            ),
        ),
        LessonSpec(
            title="Хэрэглэгчийн үйлдлийг тестлэх",
            slug="uildel-test",
            description="userEvent.setup()-ээр дарах, бичих үйлдлийг дуурайж үр дүнг шалгах.",
            duration=900,
            language=JSX,
            content="""\
### Энэ хичээлээр

- `userEvent.setup()`-ээр хэрэглэгчийн үйлдлийг дуурайх
- `click`, `type`, `clear`, `keyboard`-ийг хэрэглэх
- Үйлдлийн дараах UI-г шалгах; `within`-ээр хэсэг дотор хайх

### Яагаад чухал вэ

Ихэнх алдаа үйлдлийн дараа гардаг: товч дарахад юу ч болохгүй, буруу
мөр устана, талбар цэвэрлэгдэхгүй. `user-event` нь жинхэнэ хэрэглэгч
шиг focus, keydown, input, click зэрэг үйл явдлуудыг дарааллаар нь
үүсгэдэг тул тест бодит хэрэглээтэй ойр.

### setup ба await

```jsx
import userEvent from "@testing-library/user-event";

test("тоологч нэмэгдэнэ", async () => {
  const user = userEvent.setup(); // render-ээс ӨМНӨ
  render(<Counter />);

  await user.click(screen.getByRole("button", { name: "+" }));

  expect(screen.getByText("Тоо: 1")).toBeInTheDocument();
});
```

- Тестийн функц `async`, үйлдэл бүрийн өмнө `await`. user-event-ийн
  бүх функц Promise буцаадаг. `await`-ийг мартвал шалгалт үйлдлээс өмнө
  ажиллаж, тест санамсаргүй унана.
- React-ийн шинэчлэлийг Testing Library өөрөө `act`-оор ороодог — гараар
  `act` бичих шаардлагагүй.

### Үндсэн үйлдлүүд

```jsx
await user.click(button);
await user.dblClick(item);
await user.type(input, "Сүү авах");        // үсэг үсгээр
await user.type(input, "Сүү авах{Enter}"); // Enter дарж форм илгээнэ
await user.clear(input);
await user.keyboard("{Escape}");
await user.selectOptions(select, "Жимс");
await user.hover(card);
```

### fireEvent-ээс ялгаа

Хуучин код `fireEvent.click(button)` ашигладаг. Энэ нь ганцхан үйл
явдал илгээнэ. `user.type` бол үсэг бүрт keydown → input → keyup,
`user.click` бол pointer, mouse, focus → click. Идэвхгүй (`disabled`)
товчийг `user.click` дарахгүй — яг хэрэглэгч шиг. Тиймээс `userEvent`-ийг
илүүд үзнэ.

### within — хэсэг дотор хайх

Жагсаалтын мөр бүр ижил «Устгах» товчтой бол аль нэгийг нь хэрхэн
сонгох вэ? `within` нь хайлтыг нэг элементийн дотор хязгаарлана:

```jsx
const items = screen.getAllByRole("listitem");
await user.click(within(items[1]).getByRole("button", { name: /устгах/ }));
```

### Нэг тест — нэг зан төлөв

Тест бүр өөрийн `render`-тэй, бусдаасаа хамааралгүй байна. Бүгдийг нэг
том тестэд шалгавал эхний шалгалт унахад үлдсэн нь ажиллахгүй, юу
эвдэрснийг олоход хэцүү. Тестийн нэр нь «Хэрэглэгч X хийхэд Y болно»
гэсэн өгүүлбэр байхад хамгийн тодорхой.

### Онцгой тохиолдлыг мартахгүй

Зөвхөн «аз жаргалтай замыг» бүү шалга. Хэрэглэгч хоосон талбартай
«Нэмэх» дарна, хоёр дахь мөрийг устгана, Enter дарна. Алдаа ихэвчлэн
эдгээр газарт нуугддаг. Жишээ нь нэг мөр нэмээд түүнийгээ устгавал
«эхний мөрийг л устгадаг» алдаа илрэхгүй — хоёр мөр нэмээд хоёр
дахийг нь устга.

```jsx
test("нэмэгдэнэ", () => {
  const user = userEvent.setup();
  render(<Counter />);
  user.click(screen.getByRole("button", { name: "+" }));
  expect(screen.getByText("Тоо: 1")).toBeInTheDocument();
});
```

```quiz
Дээрх тест яагаад унадаг вэ?
- [ ] `userEvent.setup()` хэрэггүй
- [x] `await` байхгүй — click дуусахаас өмнө шалгаж байна (функц нь `async` ч биш)
- [ ] `getByText` биш `getByRole` хэрэглэх ёстой
- [ ] `render`-ийг `await` хийх ёстой
> `user.click` Promise буцаадаг. Функцийг `async` болгоод `await user.click(...)` гэж бичнэ.
```

```quiz
Хоёр мөртэй жагсаалтын ХОЁР ДАХЬ мөрийн «Устгах» товчийг хэрхэн олох вэ?
- [ ] `screen.getByRole("button", { name: "Устгах" })`
- [x] `within(screen.getAllByRole("listitem")[1]).getByRole("button", { name: "Устгах" })`
- [ ] `screen.getByTestId("delete-2")`
> Эхнийх нь хоёр товч олоод алдаа шиднэ. `within` нь хайлтыг тухайн мөрөөр хязгаарлана.
```

### Дүгнэлт

`const user = userEvent.setup()` → `render` → `await user.…` → `expect`.
Үйлдэл бүрийг `await` хий. Онцгой тохиолдлыг (хоосон утга, олон мөр)
тусад нь тестлэж, `within`-ээр тодорхой хэсэг дотор хай.
""",
            initial_code=_lesson_files(ACTION_STARTER, ("App.jsx", TODO_APP)),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐ · 15 минут

`App.jsx` (🔒) бол хийх ажлын жагсаалт. Хэрэглэгч шиг — бичиж, дарж —
нэмэх, талбар цэвэрлэгдэх, хоосон утга, устгах үйлдлүүдийг тестлэ.
Эхний тест бэлэн. Таны тестийг гурван өөр алдаатай хувилбар дээр
ажиллуулна.
""",
                tests=(
                    _all_pass("Таны бүх тест зөв апп дээр амжилттай (дор хаяж 4 тест)", 4),
                    _catches("Тест хоосон ажил нэмэгддэг алдааг барина", TODO_ADDS_EMPTY),
                    _catches("Тест буруу ажлыг устгадаг алдааг барина", TODO_WRONG_DELETE),
                    _catches(
                        "Тест нэмсний дараа талбар цэвэрлэгддэггүй алдааг барина", TODO_KEEPS_TEXT
                    ),
                ),
                tips="""\
- Талбар: `const input = screen.getByLabelText("Шинэ ажил");`, дараа нь
  `expect(input).toHaveValue("")`.
- `await user.type(input, "Ном унших{Enter}")` — Enter форм илгээнэ.
- Байхгүйг шалгах: `expect(screen.queryAllByRole("listitem")).toHaveLength(0)`.
- Устгах тестэд ХОЁР ажил нэмээд хоёр дахийг нь устга: нэг ажилтай бол
  «эхнийхийг устгадаг» алдаа илрэхгүй.
""",
                solution=_solution(ACTION_SOLUTION),
            ),
        ),
        LessonSpec(
            title="Формыг тестлэх",
            slug="form-test",
            description="Форм бөглөх, илгээх, алдааны мессеж ба vi.fn()-ээр onSubmit-ийг шалгах.",
            duration=1020,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Формыг бөглөж илгээхийг тестлэх
- Баталгаажуулалтын алдааны мессежийг шалгах
- `vi.fn()`-ээр `onSubmit` prop-ийг «тагнах»
- Хилийн утгаар (boundary) тестлэх

### Яагаад чухал вэ

Форм бол апп-ын хамгийн их алдаатай хэсгийн нэг: хоосон талбар
илгээгдэх, буруу өгөгдөл сервер рүү явах, алдааны мессеж гарахгүй байх.
Бүртгэл, төлбөрийн форм эвдэрвэл хэрэглэгч шууд алдагдана.

### vi.fn — хуурамч функц

Форм ихэвчлэн өгөгдлөө `onSubmit` prop-оор эцэгтээ өгдөг. Тестэд
жинхэнэ сервер хэрэггүй — оронд нь **mock** функц дамжуулж, хэрхэн
дуудагдсаныг шалгана:

```jsx
import { expect, test, vi } from "vitest";

test("илгээхэд өгөгдлийг дамжуулна", async () => {
  const handleSubmit = vi.fn();
  const user = userEvent.setup();
  render(<LoginForm onSubmit={handleSubmit} />);

  await user.type(screen.getByLabelText("Имэйл"), "bat@example.mn");
  await user.type(screen.getByLabelText("Нууц үг"), "secret123");
  await user.click(screen.getByRole("button", { name: "Нэвтрэх" }));

  expect(handleSubmit).toHaveBeenCalledTimes(1);
  expect(handleSubmit).toHaveBeenCalledWith({
    email: "bat@example.mn",
    password: "secret123",
  });
});
```

Mock-ийн matcher-ууд:

- `toHaveBeenCalled()`, `.not.toHaveBeenCalled()`
- `toHaveBeenCalledTimes(n)`
- `toHaveBeenCalledWith(...аргументууд)` — дор хаяж нэг дуудалт яг ийм
  аргументтай (объектыг агуулгаар нь харьцуулна)
- `toHaveBeenLastCalledWith(...)`
- `handleSubmit.mock.calls` — бүх дуудалтын аргументууд:
  `handleSubmit.mock.calls[0][0]` нь эхний дуудалтын эхний аргумент

`vi.fn(() => 42)` эсвэл `vi.fn().mockReturnValue(42)` нь утга буцаадаг
mock үүсгэнэ.

### Баталгаажуулалтыг тестлэх

```jsx
test("хоосон имэйлд алдаа гарч, илгээгдэхгүй", async () => {
  const handleSubmit = vi.fn();
  const user = userEvent.setup();
  render(<LoginForm onSubmit={handleSubmit} />);

  await user.click(screen.getByRole("button", { name: "Нэвтрэх" }));

  expect(screen.getByText("Имэйлээ оруулна уу")).toBeInTheDocument();
  expect(handleSubmit).not.toHaveBeenCalled();
});
```

Алдааны мессеж гарсныг шалгахаас гадна **илгээгдээгүйг** заавал шалга.
Мессеж харагдаад өгөгдөл явчихсан бол энэ бас алдаа.

### Хилийн утга

«Нууц үг дор хаяж 6 тэмдэгт» гэсэн дүрмийн хамгийн эмзэг газар нь хил:
5 (алдаа) ба 6 (зөв). `"123"` эсвэл `"12345678"`-аар шалгавал `< 6`-г
`< 5` гэж андуурсан алдаа илрэхгүй. Тоон хязгаар бүрт хилийн хоёр талыг
шалгах нь тестийн хамгийн хүчтэй аргуудын нэг.

### Туслах функц

Олон тест формыг бөглөдөг бол давталтыг туслах функцэд гарга:

```jsx
async function fillForm(user, { email = "bat@example.mn", password = "secret123" } = {}) {
  if (email) await user.type(screen.getByLabelText("Имэйл"), email);
  if (password) await user.type(screen.getByLabelText("Нууц үг"), password);
}

await fillForm(user, { password: "12345" }); // зөвхөн нэг утгыг өөрчилнө
```

### Хүртээмж ба тест

`getByLabelText("Имэйл")` ажиллахгүй байвал ихэвчлэн `<label htmlFor>`
дутуу — тест хүртээмжийн алдааг олсон гэсэн үг (Модул 4). Шошгыг
засахад тест ч, дэлгэц уншигч хэрэглэгч ч баярлана.

```quiz
«Нууц үг 8-аас дээш тэмдэгт» шаардлагыг аль утгуудаар тестлэх нь хамгийн үр дүнтэй вэ?
- [ ] 1 ба 100
- [x] 7 ба 8
- [ ] Зөвхөн 8
- [ ] Хоосон мөр
> Хилийн хоёр тал: 7 (алдаа) ба 8 (зөв). Хэтэрхий жижиг, том утга хилийн алдааг илрүүлэхгүй.
```

```quiz
`onSubmit` нь `{ name: "Бат", email: "b@x.mn" }`-ээр дуудагдсан. `expect(onSubmit).toHaveBeenCalledWith({ name: "Бат" })` юу болох вэ?
- [ ] Давна — `name` таарч байна
- [x] Унана — аргументыг бүтнээр нь харьцуулдаг
> `toHaveBeenCalledWith` нь `toEqual` шиг бүх талбарыг харьцуулна. Илүү талбар байвал таарахгүй.
```

### Дүгнэлт

Формыг хэрэглэгч шиг бөглөж илгээнэ. `onSubmit`-д `vi.fn()` өгч юугаар,
хэдэн удаа дуудагдсаныг шалгана. Алдаатай үед мессеж гарахаас гадна
илгээгдэхгүй байхыг, тоон хязгаарыг хилийн утгаар шалга.
""",
            initial_code=_lesson_files(FORM_STARTER, ("App.jsx", SIGNUP_FORM)),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐ · 18 минут

`App.jsx` (🔒) дахь бүртгэлийн формд тест бич: зөв бөглөөд илгээх,
талбар тус бүрийн алдаа, алдаатай үед илгээгдэхгүй байх. `onSubmit`-д
`vi.fn()` дамжуулна. `fillForm` туслах функц бэлэн — ашигла.
""",
                tests=(
                    _all_pass("Таны бүх тест зөв форм дээр амжилттай (дор хаяж 5 тест)", 5),
                    _catches("Тест алдаатай байхад ч илгээдэг алдааг барина", FORM_SUBMITS_INVALID),
                    _catches(
                        "Тест илгээх өгөгдлийн алдааг (нууц үг дутуу) барина", FORM_DROPS_PASSWORD
                    ),
                    _catches(
                        "Тест нууц үгийн хилийн алдааг (5 тэмдэгт зөвшөөрдөг) барина",
                        FORM_OFF_BY_ONE,
                    ),
                ),
                tips="""\
- `const handleSubmit = vi.fn();` → `render(<SignupForm onSubmit={handleSubmit} />)`.
- Бүх талбарыг шалга: `toHaveBeenCalledWith({ name, email, password })`.
  Зөвхөн «дуудагдсан» гэж шалгавал дутуу өгөгдөл илрэхгүй.
- Алдаатай тохиолдолд мессежээс гадна `expect(handleSubmit).not.toHaveBeenCalled()`.
- Нууц үгийн хил: яг 5 тэмдэгт (`"12345"`) — алдаа гарах ёстой.
""",
                solution=_solution(FORM_SOLUTION),
            ),
        ),
        LessonSpec(
            title="Асинхрон UI ба mock",
            slug="async-mock-test",
            description="findBy, waitFor-оор ачаалах, алдааны төлвийг тестлэж, өгөгдлийг mock хийх.",
            duration=1080,
            language=JSX,
            content="""\
### Энэ хичээлээр

- `findBy…`, `waitFor`-оор асинхрон UI-г хүлээх
- Ачаалж буй, алдаа, хоосон төлвийг тестлэх
- Өгөгдөл татах функцийг `vi.fn()`-ээр орлуулах
- Бодит төсөлд MSW-ээр сүлжээг mock хийх

### Яагаад чухал вэ

Серверээс өгөгдөл татдаг component-ийн хамгийн эмзэг хэсэг нь «аз
жаргалтай зам» биш: сервер унтарсан, удаан хариулсан, хоосон жагсаалт
буцаасан үе (Модул 9). Эдгээрийг гараар шалгахын тулд серверээ унтраах
хэрэгтэй болно — тестэд бол хэдхэн мөр.

### findBy ба waitFor

Өгөгдөл ирэхээс өмнө `getByText("Бат")` шууд унана. `findBy…` нь
элемент гарч иртэл давтан хайдаг Promise буцаана (бодит Testing
Library-д анхдагчаар 1 секунд, энэ засварлагчид 2 секунд):

```jsx
render(<UserList />);

expect(screen.getByText("Ачаалж байна…")).toBeInTheDocument();
expect(await screen.findByText("Бат")).toBeInTheDocument();
expect(screen.queryByText("Ачаалж байна…")).not.toBeInTheDocument();
```

`waitFor` нь дурын шалгалтыг давж иртэл давтана:

```jsx
await waitFor(() => {
  expect(screen.getAllByRole("listitem")).toHaveLength(4);
});
```

Түгээмэл алдаа:

- `findBy…`-г `await`-гүй бичих — Promise үргэлж «үнэн».
- `waitFor` дотор үйлдэл (click) хийх — давтах бүрт дахин дарна.
- `await sleep(1000)` — удаан бөгөөд найдваргүй. Нөхцөлийг хүлээ,
  хугацааг биш.

### Өгөгдөл татах функцийг mock хийх

Component нь өгөгдлийг хаанаас авахаа prop-оор хүлээн авбал тестэд
хуурамчаар солиход амархан (dependency injection):

```jsx
export default function UserList({ loadUsers = fetchUsers }) { /* … */ }
```

```jsx
test("алдаа гарвал мэдэгдэнэ", async () => {
  const loadUsers = vi.fn(async () => {
    throw new Error("Сервер унтарсан");
  });
  render(<UserList loadUsers={loadUsers} />);

  expect(await screen.findByRole("alert")).toHaveTextContent("ачаалж чадсангүй");
  expect(loadUsers).toHaveBeenCalledTimes(1);
});
```

Дуудалт бүрт өөр хариу — эхлээд алдаа, дараа нь амжилт:

```jsx
let calls = 0;
const loadUsers = vi.fn(async () => {
  calls += 1;
  if (calls === 1) throw new Error("Түр алдаа");
  return [{ id: 1, name: "Сараа" }];
});
```

Бодит Vitest-д үүнийг
`vi.fn().mockRejectedValueOnce(new Error()).mockResolvedValueOnce([…])`
гэж товчилж болно. Энэ засварлагчид `vi.fn(async () => …)` хэлбэрийг
ашиглана.

### Callback prop-ийг шалгах

Хэрэглэгч дээр дарахад эцэгт мэдэгддэг `onSelect` мэт callback-д
`vi.fn()` өгч, **юугаар** дуудагдсаныг шалгана:

```jsx
const onSelect = vi.fn();
render(<UserList loadUsers={loadUsers} onSelect={onSelect} />);
await user.click(await screen.findByRole("button", { name: "Сараа" }));
expect(onSelect).toHaveBeenCalledWith({ id: 2, name: "Сараа" });
```

### Бодит төсөлд: MSW

Бодит кодод component `fetch`-ийг шууд дууддаг нь элбэг. Тэгвэл **Mock
Service Worker (MSW)** сүлжээний хүсэлтийг өөрөө барьж хуурамч хариу
өгдөг — component-ийн код огт өөрчлөгдөхгүй:

```jsx
import { http, HttpResponse } from "msw";
import { setupServer } from "msw/node";

const server = setupServer(
  http.get("/api/users", () => HttpResponse.json([{ id: 1, name: "Бат" }])),
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

test("серверийн алдаа", async () => {
  server.use(http.get("/api/users", () => new HttpResponse(null, { status: 500 })));
  render(<UserList />);
  expect(await screen.findByRole("alert")).toBeInTheDocument();
});
```

Бодит Vitest-д мөн `vi.mock("./api")` (модулийг бүхэлд нь орлуулах),
`vi.spyOn` байдаг. Энэ засварлагчид тэдгээр байхгүй; харин дадлагын API
(`/api/users`) тестэд жинхэнэ ажилладаг (20 мс хоцролттой).

```jsx
test("хэрэглэгчдийг харуулна", () => {
  render(<UserList />);
  expect(screen.getByText("Бат")).toBeInTheDocument();
});
```

```quiz
Дээрх тест яагаад унадаг вэ?
- [ ] `UserList`-д `loadUsers` prop заавал хэрэгтэй
- [x] Өгөгдөл ирэхээс өмнө шалгаж байна — `await screen.findByText("Бат")` хэрэгтэй
- [ ] `getByText` нь товч доторх текстийг олдоггүй
> Эхний render-т зөвхөн «Ачаалж байна…» харагдана. `findBy…` өгөгдөл ирэхийг хүлээнэ.
```

```quiz
`const fn = vi.fn(); fn("a", 1); fn("b");` — `fn.mock.calls` юу вэ?
- [ ] `["a", 1, "b"]`
- [x] `[["a", 1], ["b"]]`
- [ ] `2`
> Дуудалт бүрийн аргументуудын массив. Дуудалтын тоо нь `fn.mock.calls.length`.
```

### Дүгнэлт

Асинхрон UI-г `findBy…`, `waitFor`-оор хүлээнэ — `sleep`-ээр биш.
Өгөгдлийн эх үүсвэрийг prop эсвэл MSW-ээр хуурамчаар сольж, ачаалах,
алдаа, хоосон, дахин оролдох төлөв бүрийг тусад нь тестлэнэ.
""",
            initial_code=_lesson_files(ASYNC_STARTER, ("App.jsx", USER_LIST)),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐ · 18 минут

`App.jsx` (🔒)-ийн `UserList` хэрэглэгчдийг татдаг. Эхний тест жинхэнэ
дадлагын API-г ашигладаг — бэлэн. `loadUsers` prop-оор хуурамч функц
өгч алдааны төлөв, «Дахин оролдох», хэрэглэгч сонгох (`onSelect`)-ыг
тестлэ.
""",
                tests=(
                    _all_pass("Таны бүх тест зөв component дээр амжилттай (дор хаяж 4 тест)", 4),
                    _catches(
                        "Тест алдааг нуудаг (мэдэгдэл харуулдаггүй) алдааг барина",
                        USERS_HIDE_ERROR,
                    ),
                    _catches("Тест «Дахин оролдох» ажилладаггүй алдааг барина", USERS_NO_RETRY),
                    _catches(
                        "Тест onSelect-ийг буруу утгаар дууддаг алдааг барина", USERS_SELECT_ID
                    ),
                ),
                tips="""\
- Алдааны мэдэгдэл `role="alert"`-тай: `await screen.findByRole("alert")`.
- Дахин оролдох: эхний дуудалтад `throw`, хоёр дахьд массив буцаадаг
  mock бич. Товчийг ч `findByRole`-оор хүлээ — алдаа ирсний дараа л
  гарна.
- `onSelect`: `toHaveBeenCalledWith(хэрэглэгчийн объект)` — зөвхөн
  «дуудагдсан» гэж шалгавал буруу утгаар дуудсан алдаа илрэхгүй.
- Бүх `findBy…`-ийн өмнө `await`.
""",
                solution=_solution(ASYNC_SOLUTION),
            ),
        ),
        LessonSpec(
            title="Төсөл: Бэлэн аппад тест нэмэх",
            slug="tusul-test-nemeh",
            description="Тестгүй сагсны аппыг уншиж, гол зан төлөвийг хамарсан тестийн иж бүрдэл бичнэ.",
            duration=2400,
            language=JSX,
            content="""\
### Энэ хичээлээр

- Бусдын бичсэн аппын кодыг уншиж, тестлэх зан төлөвийг жагсаах
- Тестийн иж бүрдлийг (test suite) `describe`, туслах функцээр цэгцтэй
  бичих
- Тест бүр алдааг барьж чадах эсэхийг шалгах

### Яагаад чухал вэ

Ажилд ороход ихэвчлэн шинэ апп биш, аль хэдийн ажиллаж буй, тестгүй код
өгдөг. Түүнийг өөрчлөхийн өмнө одоогийн зан төлөвийг тестээр
«түгжих» нь хамгийн аюулгүй арга: дараа нь юу ч эвдэрвэл тест шууд
хэлнэ.

### 1. Кодыг уншиж, зан төлөвийг жагсаа

`App.jsx` (🔒)-ийг уншаад хэрэглэгчийн хийж чадах зүйлсийг өгүүлбэрээр
бич. Жишээ нь:

- Бараа нэмэхэд сагсанд гарч, нийт дүн шинэчлэгдэнэ
- Ижил барааг дахин нэмэхэд …
- «−» дарахад …, 1 ширхэгтэй бол …
- «✕» дарахад …
- Хямдралын код зөв бол …, буруу бол …

Жагсаалтын мөр бүр нэг тест болно. **Мөнгө**-тэй холбоотой хэсэг (нийт
дүн, хямдрал) хамгийн чухал — алдаа нь хамгийн үнэтэй.

### 2. Туслах функц ба within

«Банана» гэсэн текст барааны жагсаалтад ч, сагсанд ч гардаг. Сагсны
хэсгийг `aria-label`-аар нь олоод дотор нь хайна:

```jsx
function renderApp() {
  const user = userEvent.setup();
  render(<App />);
  const cart = screen.getByRole("region", { name: "Сагс" });
  return { user, cart };
}

test("…", async () => {
  const { user, cart } = renderApp();
  await user.click(screen.getByRole("button", { name: "Банана нэмэх" }));
  expect(within(cart).getByText(/Банана × 1/)).toBeInTheDocument();
});
```

Тест бүр `renderApp()`-аар эхэлж, бусдаасаа хамааралгүй байна.

### 3. Хил ба онцгой тохиолдол

Нэг ширхэг бараа нэмэхэд `price * qty` ба `price` ижил үр дүн өгнө —
үржүүлэхээ мартсан алдаа илрэхгүй. Тиймээс:

- тоо ширхэгийг 2 ба түүнээс дээш болго;
- «−»-г 1 ширхэгтэй мөр дээр дар;
- хямдралыг 10₮ ба 10%-ийн ялгаа харагдах дүн дээр шалга;
- буруу кодыг ч шалга.

### 4. Тест алдааг барьж чадах уу?

Тест бүрийг бичсэний дараа өөрөөсөө асуу: «Кодыг хаана нь эвдвэл энэ
тест улаан болох вэ?» Хариулж чадахгүй бол тест юуг ч хамгаалахгүй
байж магадгүй. Бодит төсөлд **mutation testing** хэрэгсэл (жишээ нь
Stryker) кодыг автоматаар мянга мянган жижиг байдлаар эвдэж, аль
өөрчлөлтийг тест барьсангүйг харуулдаг. Энэ хичээлийн шалгалт ч яг
тийм — таны тестийг дөрвөн эвдэрсэн хувилбар дээр ажиллуулна.

### Coverage

`npx vitest run --coverage` (`@vitest/coverage-v8` багц) нь кодын хэдэн
хувь тестээр ажилласныг харуулна. Тестлэгдээгүй хэсгийг олоход тустай.
Гэхдээ 100% coverage нь сайн тест гэсэн үг биш: мөр ажилласан ч үр
дүнг нь шалгаагүй байж болно.

```quiz
Сагсны нийт дүнд `price * qty`-ийн оронд `price` гэж бичсэн алдааг аль тест илрүүлэх вэ?
- [ ] Нэг бараа нэг удаа нэмээд нийтийг шалгах
- [x] Нэг барааг 2 удаа нэмээд нийтийг шалгах
- [ ] Сагс хоосон үед нийт 0₮ эсэхийг шалгах
> `qty = 1` бол хоёр томьёо ижил хариу өгнө. Ялгаа гарах өгөгдлөөр тестлэнэ.
```

```quiz
Coverage 100% болсон. Энэ юу гэсэн үг вэ?
- [ ] Апп-д алдаа байхгүй
- [x] Кодын мөр бүр тестийн үеэр ажилласан, гэхдээ үр дүн нь шалгагдсан гэсэн баталгаа байхгүй
- [ ] Цаашид тест бичих шаардлагагүй
> Coverage нь юу АЖИЛЛАСНЫГ хэмждэг, юу ШАЛГАГДСАНЫГ биш.
```

### Дүгнэлт

Бэлэн кодод тест нэмэхдээ эхлээд зан төлөвийг жагсааж, хамгийн чухал
(мөнгө) хэсгээс эхэлнэ. Туслах функц, `within`-ээр тестийг цэгцтэй
байлгаж, хил ба онцгой тохиолдлыг заавал хамруулна. Сайн тест бол
эвдэрсэн кодыг барьдаг тест.
""",
            initial_code=_lesson_files(
                SHOP_STARTER, ("App.jsx", SHOP_APP), ("products.js", SHOP_PRODUCTS)
            ),
            exercise=ExerciseSpec(
                statement="""\
**Түвшин:** ⭐⭐⭐⭐ · 35 минут

«Ногоон сагс»-ын жижиг хувилбар (`App.jsx` 🔒) огт тестгүй. Кодыг уншиж,
хэрэглэгчийн хийж чадах зүйлсийг жагсаагаад `App.test.jsx`-д тестийн иж
бүрдэл бич. `renderApp` туслах функц ба эхний тест бэлэн. Таны тестийг
дөрвөн өөр алдаатай хувилбар дээр ажиллуулна — бүгдийг нь барих ёстой.
""",
                tests=(
                    _all_pass("Таны бүх тест зөв апп дээр амжилттай (дор хаяж 5 тест)", 5),
                    _catches(
                        "Тест нийт дүнгийн алдааг (тоо ширхэгийг тооцоогүй) барина",
                        SHOP_TOTAL_NO_QTY,
                    ),
                    _catches("Тест ижил бараа давхар мөр болдог алдааг барина", SHOP_DUPLICATES),
                    _catches(
                        "Тест «−» товчны алдааг (0 ширхэгтэй мөр үлддэг) барина", SHOP_KEEPS_ZERO
                    ),
                    _catches(
                        "Тест хямдралын алдааг (10% биш 10₮ хасдаг) барина", SHOP_FLAT_DISCOUNT
                    ),
                ),
                tips="""\
- Товчнууд `aria-label`-тай: `"Банана нэмэх"`, `"Сүү хасах"`, `"Алим устгах"`.
- Сагсны мөр: `within(cart).getByText(/Банана × 2/)`; мөрийн тоо:
  `within(cart).getAllByRole("listitem")`.
- Нийт дүн: `within(cart).getByText("Нийт: 7000₮")`.
- Код: `await user.type(within(cart).getByLabelText("Хямдралын код"), "SALE10{Enter}")`,
  мессеж нь `role="status"`-тай.
- Нэг барааг ДОР ХАЯЖ хоёр удаа нэмсэн тест хэрэгтэй — эс бөгөөс тоо
  ширхэгийн алдаа нуугдана.
""",
                solution=_solution(SHOP_SOLUTION),
            ),
        ),
    ],
)
