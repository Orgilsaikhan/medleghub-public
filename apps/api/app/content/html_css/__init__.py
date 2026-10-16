"""HTML & CSS сургалт.

Модул 0-ээс 19 хүртэл — вэбийн үндэс, HTML, CSS, хариуцлагатай дизайн, төслүүд.

Хичээлийн засварлагч нь файлуудыг tab-аар харуулж, баруун талын «Хөтөч»
нь сурагчийн хуудсыг код бичих зуур шууд харуулна
(`apps/web/src/components/learn/html/`). Анхны код нь суралцагч өөрийн
файлдаа хуулж шууд ашиглаж болох БҮТЭН, ажиллах жишээ.

Хичээлийн `language` нь тухайн хичээл юуг заахаас шалтгаална: бүтцийн
хичээлүүд `html`, загварын хичээлүүд `css`. Олон файлтай код нь
`// @file` мөрөөр хуваагдана (`common.py`): CSS хичээл бүр `index.html` +
`style.css` (`css_page()`) тул сурагч бичсэн загвараа хуудас дээр харна.
Модул 16-18-ийн төслүүд нь `<style>` агуулсан нэг HTML, Модул 19 нь олон
файлтай сайт.
"""

from app.content.html_css.css_basics import CSS_BASIC_MODULES
from app.content.html_css.css_layout import CSS_LAYOUT_MODULES
from app.content.html_css.fundamentals import FUNDAMENTALS
from app.content.html_css.html_basics import HTML_BASIC_MODULES
from app.content.html_css.html_structure import HTML_STRUCTURE_MODULES
from app.content.html_css.projects import PROJECT_MODULES
from app.content.html_css.responsive import RESPONSIVE_MODULES
from app.content.types import CourseSpec
from app.models.enums import Category, Difficulty

HTML_COURSE = CourseSpec(
    title="HTML & CSS үндэс",
    slug="html-css-undes",
    description=(
        "Вэб хуудасны бүтэц болон загварыг эхнээс нь сурна. Семантик HTML, "
        "форм, сонгогч, хайрцгийн загвараас эхлээд Flexbox, Grid, "
        "хариуцлагатай дизайн хүртэл. Төгсгөлд нь портфолио, нүүр хуудас, "
        "блог зэрэг бүтэн төсөл бичнэ. Өмнөх мэдлэг шаардахгүй."
    ),
    difficulty=Difficulty.BEGINNER,
    category=Category.HTML_CSS,
    modules=[
        FUNDAMENTALS,
        *HTML_BASIC_MODULES,
        *HTML_STRUCTURE_MODULES,
        *CSS_BASIC_MODULES,
        *CSS_LAYOUT_MODULES,
        *RESPONSIVE_MODULES,
        *PROJECT_MODULES,
    ],
    # Үнэгүй хэсэг: «Модул 3 — HTML шинж чанар» дуустал. Үлдсэн нь Standard багц.
    is_free=False,
    free_lessons=13,
)
