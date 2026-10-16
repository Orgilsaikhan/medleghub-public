"""JavaScript сургалт — MVP-ийн туг сургалт.

Модул 0-ээс 25 хүртэл, үндсээс эхлээд төгсгөлийн төслүүд хүртэл.

Энэ бол хөтөч дотор код нь БҮРЭН ажилладаг сургалт. Тиймээс хичээл бүрийн
`initial_code` нь sandbox дотор алдаагүй ажиллах ёстой. Sandbox нь Web
Worker тул дараах зүйлс БАЙХГҮЙ:

    • `document`, `window`, `localStorage` — DOM огт байхгүй
    • `fetch`, `XMLHttpRequest` — сүлжээг зориуд хаасан

Хөтчийн сэдэвтэй модулиуд (10-14, 19, 22-25) нь тиймээс ижил нэр, ижил
хэлбэртэй ЖИЖИГ ЗАГВАРЫГ анхны кодондоо өөрсдөө үүсгэнэ. Хичээлийн
markdown доторх жишээ нь жинхэнэ хөтөчид ажиллах бодит код бөгөөд
суралцагч түүнийг өөрийн файлд хуулж ашиглана.
"""

from app.content.javascript.async_api import ASYNC_API_MODULES
from app.content.javascript.basics import BASICS_MODULES
from app.content.javascript.beginner_projects import BEGINNER_PROJECTS
from app.content.javascript.browser import BROWSER_MODULES
from app.content.javascript.browser_projects import BROWSER_PROJECTS
from app.content.javascript.functions_data import FUNCTION_DATA_MODULES
from app.content.javascript.fundamentals import FUNDAMENTALS
from app.content.javascript.modern import MODERN_MODULES
from app.content.javascript.projects import FINAL_PROJECT_MODULES
from app.content.javascript.tooling import TOOLING_MODULES
from app.content.types import CourseSpec
from app.models.enums import Category, Difficulty

JS_COURSE = CourseSpec(
    title="JavaScript үндэс",
    slug="javascript-undes",
    description=(
        "JavaScript-ийг эхнээс нь бүрэн сурна. Хувьсагч, давталт, функцээс "
        "эхэлж, DOM, үйл явдал, асинхрон код, API хүртэл алхам алхмаар үзнэ. "
        "Хичээл бүрт кодоо шууд бичиж ажиллуулж үзэх бөгөөд төгсгөлд нь бодит "
        "дөрвөн төсөл хийнэ. Өмнөх мэдлэг шаардахгүй."
    ),
    difficulty=Difficulty.BEGINNER,
    category=Category.JAVASCRIPT,
    modules=[
        FUNDAMENTALS,
        *BASICS_MODULES,
        *FUNCTION_DATA_MODULES,
        BEGINNER_PROJECTS,
        *BROWSER_MODULES,
        BROWSER_PROJECTS,
        *MODERN_MODULES,
        *ASYNC_API_MODULES,
        *TOOLING_MODULES,
        *FINAL_PROJECT_MODULES,
    ],
    # Үнэгүй хэсэг: «Модул 4 — Давталт» дуустал. Үлдсэн нь Standard багц.
    is_free=False,
    free_lessons=15,
)
