"""Git ба GitHub сургалт.

Модул 0-ээс 17 хүртэл — үндэс, үндсэн тушаал, салаа, хамтын ажиллагаа, дунд
шатны сэдэв, дадлага.

АНХААР: Хичээлүүдийн код нь ТЕРМИНАЛЫН ТУШААЛ (`shell`) тул хөтөч дотор
ажиллахгүй. «Код ажиллуулах» товч идэвхгүй байна. Анхны код бүр нь
суралцагч өөрийн терминал дээрээ дарааллаар нь ажиллуулж болох бүрэн
тушаалын жагсаалт байхаар бичигдсэн.

Зарим жишээ нь `gh` (GitHub CLI) ашиглана — тэр нь заавал биш, ижил
ажлыг вэб интерфэйсээс хийж болно.
"""

from app.content.git_github.basics import GIT_BASIC_MODULES
from app.content.git_github.branching import GIT_BRANCHING_MODULES
from app.content.git_github.fundamentals import GIT_FUNDAMENTAL_MODULES
from app.content.git_github.intermediate import GIT_INTERMEDIATE_MODULES
from app.content.git_github.practice import GIT_PRACTICE_MODULES
from app.content.types import CourseSpec
from app.models.enums import Category, Difficulty

GIT_COURSE = CourseSpec(
    title="Git ба GitHub",
    slug="git-github",
    description=(
        "Кодын хувилбарыг хянаж, багаар ажиллаж сурна. Commit, салаа, "
        "нэгтгэлтээс эхлээд pull request, код хянал, зөрчил шийдэх хүртэл. "
        "Төгсгөлд нь бодит ажлын урсгалыг эхнээс нь эцэс хүртэл давтана. "
        "Өмнөх мэдлэг шаардахгүй."
    ),
    difficulty=Difficulty.BEGINNER,
    category=Category.GIT,
    modules=[
        *GIT_FUNDAMENTAL_MODULES,
        *GIT_BASIC_MODULES,
        *GIT_BRANCHING_MODULES,
        *GIT_INTERMEDIATE_MODULES,
        *GIT_PRACTICE_MODULES,
    ],
    # Үнэгүй хэсэг: «Модул 4 — GitHub-ийн үндэс» дуустал. Үлдсэн нь Standard багц.
    is_free=False,
    free_lessons=13,
)
