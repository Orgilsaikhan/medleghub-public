"""React-ээр апп бүтээх сургалт.

Энэ сургалтын хичээлүүд `jsx` хэлтэй: код нь олон файл (`// @file App.jsx`)
бөгөөд react-tutorial.app маягийн засварлагч дээр ажиллана — файлууд tab-аар,
баруун талд «Заавар / Хөтөч», доор нь тест ба console. Дасгалын тест нь
`ReactTestSpec` (DOM тест) бөгөөд «Ажиллуулах» дарахад бүгд шалгагдана.

Шалгах:

    cd apps/web && npm run verify:react
"""

from app.content.react.advanced import ADVANCED
from app.content.react.architecture import ARCHITECTURE
from app.content.react.capstone import CAPSTONE
from app.content.react.effects import EFFECTS
from app.content.react.forms import FORMS
from app.content.react.fundamentals import FUNDAMENTALS
from app.content.react.hooks import HOOKS
from app.content.react.modern import MODERN
from app.content.react.performance import PERFORMANCE
from app.content.react.prerequisites import PREREQUISITES
from app.content.react.props import PROPS
from app.content.react.routing import ROUTING
from app.content.react.server_data import SERVER_DATA
from app.content.react.state import STATE
from app.content.react.testing import TESTING
from app.content.types import CourseSpec
from app.models.enums import Category, Difficulty

REACT_COURSE = CourseSpec(
    title="React-ээр апп бүтээх",
    slug="react-app-buteeh",
    description=(
        "Component, props, state, hook ашиглан орчин үеийн вэб апп бүтээнэ. "
        "Форм, effect, routing, серверийн өгөгдөл, React 19, гүйцэтгэл, тест "
        "хүртэл алхам алхмаар үзэж, хичээл бүрт кодоо шууд бичээд автомат "
        "тестээр шалгуулна. Төгсгөлд нь бүтэн онлайн дэлгүүр бүтээнэ. "
        "JavaScript, HTML & CSS-ийн үндсийг мэдэх шаардлагатай."
    ),
    difficulty=Difficulty.INTERMEDIATE,
    category=Category.REACT,
    modules=[
        PREREQUISITES,
        FUNDAMENTALS,
        PROPS,
        STATE,
        FORMS,
        EFFECTS,
        HOOKS,
        ARCHITECTURE,
        ROUTING,
        SERVER_DATA,
        ADVANCED,
        MODERN,
        PERFORMANCE,
        TESTING,
        CAPSTONE,
    ],
    # Үнэгүй хэсэг: «Модул 1 — React-ийн үндэс» дуустал. Үлдсэн нь Standard багц.
    is_free=False,
    free_lessons=16,
)
