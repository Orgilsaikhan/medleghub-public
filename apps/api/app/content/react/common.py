"""React хичээлийн олон файлтай кодыг бүтээх туслахууд.

Хичээлийн `initial_code` нь `// @file <нэр>` мөрөөр файлуудад хуваагдана
(`apps/web/src/lib/sandbox/react/files.ts`). Эдгээр функц нь Vite-ийн
стандарт бүтцийг давтагдалгүй үүсгэнэ:

    App.jsx            ← сурагч бичнэ
    main.jsx   🔒      ← createRoot(...).render(<App />)
    index.html 🔒      ← <div id="root"></div>
"""

from app.content.types import ReactTestSpec

HTML = '<div id="root"></div>\n'

MAIN = """\
import { createRoot } from "react-dom/client";
import App from "./App";

createRoot(document.getElementById("root")).render(<App />);
"""

MAIN_WITH_CSS = """\
import { createRoot } from "react-dom/client";
import App from "./App";
import "./styles.css";

createRoot(document.getElementById("root")).render(<App />);
"""

File = tuple[str, str] | tuple[str, str, bool]


def files(*entries: File) -> str:
    """`("App.jsx", код)` эсвэл `("main.jsx", код, True)` — сүүлийнх нь түгжигдсэн."""
    parts: list[str] = []
    for entry in entries:
        name, code = entry[0], entry[1]
        locked = len(entry) == 3 and entry[2]  # type: ignore[misc]
        parts.append(f"// @file {name}{' locked' if locked else ''}\n{code.strip()}\n")
    return "".join(parts)


def vite(
    app: str,
    *,
    extra: dict[str, str] | None = None,
    locked: dict[str, str] | None = None,
    css: str | None = None,
    css_locked: bool = True,
    main: str | None = None,
    main_locked: bool = True,
    html: str = HTML,
) -> str:
    """Vite-ийн стандарт бүтэц. `extra` — засварлагдах бусад файл (`Card.jsx`),
    `locked` — түгжигдсэн нэмэлт файл (өгөгдөл, туслах)."""
    entries: list[File] = [("App.jsx", app)]
    entries += [(name, code) for name, code in (extra or {}).items()]
    entries += [(name, code, True) for name, code in (locked or {}).items()]
    if css is not None:
        entries.append(("styles.css", css, css_locked))
    entries.append(("main.jsx", main or (MAIN_WITH_CSS if css is not None else MAIN), main_locked))
    entries.append(("index.html", html, True))
    return files(*entries)


def solution(**changed: str) -> str:
    """Жишиг шийдэл — зөвхөн өөрчлөгдсөн файлууд: `solution(App_jsx=...)`.

    Python-ы нэрэнд цэг орохгүй тул `App_jsx` → `App.jsx`, `styles_css` →
    `styles.css` болгоно.
    """
    return files(*((_filename(name), code) for name, code in changed.items()))


def _filename(key: str) -> str:
    """`App_jsx` → `App.jsx`, `use_counter_js` → `use_counter.js`."""
    stem, _, extension = key.rpartition("_")
    return f"{stem}.{extension}"


def test(name: str, code: str) -> ReactTestSpec:
    return ReactTestSpec(name=name, code=code.strip())
