"""C ба C++ сургалт.

Модул 1-10 нь C, Модул 11-19 нь C++, Модул 20-21 нь төслүүд. Модул 0
байхгүй тул энэ сургалт 1-ээс эхэлнэ.

Код серверт хөрвүүлэгдээд (`apps/compiler`) хөтөч дотор ажиллана.

ХИЧЭЭЛ БҮР HACKERRANK МАЯГИЙН ДАСГАЛТАЙ
───────────────────────────────────────
- `content` нь тайлбар бөгөөд төгсгөлдөө «Жишээ програм» — сэдвийг бүтнээр
  нь харуулсан ажиллах програмтай.
- `initial_code` нь дасгалын эхлэл код (араг), `exercise` нь даалгавар,
  жишээ ба нууц тестүүд, жишиг шийдэл.
- Сурагч «Тест ажиллуулах»-аар жишээ тестүүдийг, «Илгээх»-ээр бүх тестийг
  ажиллуулна. Бүгдийг давбал хичээл дуусна.

Дасгал нэмэх, засахдаа тестүүд зөв эсэхийг шалгана (хөрвүүлэгч асаалттай):

    python -m app.content.exercises | node ../web/scripts/verify-exercises.mjs
"""

from app.content.c_cpp.c_basics import C_BASIC_MODULES
from app.content.c_cpp.c_core import C_CORE_MODULES
from app.content.c_cpp.cpp_basics import CPP_BASIC_MODULES
from app.content.c_cpp.cpp_core import CPP_CORE_MODULES
from app.content.c_cpp.projects import PROJECT_MODULES
from app.content.types import CourseSpec
from app.models.enums import Category, Difficulty

C_CPP_COURSE = CourseSpec(
    title="C ба C++ үндэс",
    slug="c-cpp-undes",
    description=(
        "Техник хангамжид хамгийн ойр хоёр хэлийг эхнээс нь сурна. C дээр "
        "хувьсагч, заагч, бүтэц зэрэг суурь ойлголтуудыг эзэмшээд, C++ рүү "
        "шилжин класс, вектор, std::string ашиглаж сурна. Төгсгөлд нь найман "
        "бүтэн програм бичнэ. Өмнөх мэдлэг шаардахгүй."
    ),
    difficulty=Difficulty.BEGINNER,
    category=Category.C,
    modules=[
        *C_BASIC_MODULES,
        *C_CORE_MODULES,
        *CPP_BASIC_MODULES,
        *CPP_CORE_MODULES,
        *PROJECT_MODULES,
    ],
    # Үнэгүй хэсэг: «Модул 6 — Давталт» дуустал. Үлдсэн нь Standard багц.
    is_free=False,
    free_lessons=15,
)
