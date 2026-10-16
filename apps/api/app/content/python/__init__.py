"""Python сургалт.

Ахисан шат (Async, FastAPI, Django, Data Science гэх мэт) нь одоогоор
орхигдсон.

Код хөтөч дотор Pyodide (WebAssembly дээрх CPython)-оор ажиллана.

ХИЧЭЭЛ БҮР HACKERRANK МАЯГИЙН ДАСГАЛТАЙ (C/C++ сургалттай ижил)
───────────────────────────────────────────────────────────────
- `content` нь тайлбар бөгөөд төгсгөлдөө «Жишээ програм»-тай.
- `initial_code` нь дасгалын эхлэл код, `exercise` нь даалгавар, жишээ ба
  нууц тестүүд, жишиг шийдэл, «Тусламж»-ийн зөвлөгөө.
- Тест бүр цэвэр нэрийн талбарт ажиллаж, `input()`-ийн асуулт гаралтад
  тооцогдохгүй.
- Pyodide-д БАЙХГҮЙ: `requests`, `sqlalchemy`, `venv`, `pip` — дасгал
  тэдгээрийг ашиглаж болохгүй. `sqlite3`, `json`, `unittest`, `logging`
  зэрэг стандарт сан бүгд ажиллана.

Тестүүд зөв эсэхийг шалгах:

    python -m app.content.exercises | node ../web/scripts/verify-exercises.mjs
"""

from app.content.python.beginner_applied import APPLIED_MODULES
from app.content.python.beginner_core import CORE_MODULES
from app.content.python.fundamentals import FUNDAMENTALS
from app.content.python.intermediate import INTERMEDIATE_MODULES
from app.content.types import CourseSpec
from app.models.enums import Category, Difficulty

PYTHON_COURSE = CourseSpec(
    title="Python Программчлал",
    slug="python-programchlal",
    description=(
        "Програмчлалын үндсээс эхлээд бодит төсөл бичих хүртэл. Хувьсагч, "
        "давталт, функцээс эхэлж, объект хандлагат програмчлал, тест, "
        "өгөгдлийн сан, API хүртэл алхам алхмаар сурна. Өмнөх мэдлэг шаардахгүй."
    ),
    difficulty=Difficulty.BEGINNER,
    category=Category.PYTHON,
    modules=[FUNDAMENTALS, *CORE_MODULES, *APPLIED_MODULES, *INTERMEDIATE_MODULES],
    # Үнэгүй хэсэг: «Модул 4 — Жагсаалт» дуустал. Үлдсэн нь Standard багц.
    is_free=False,
    free_lessons=13,
)
