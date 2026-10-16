"""Модул 15-28 — Дунд шат.

OOP-оос эхлээд бодит төсөлд хэрэгтэй хэрэгслүүд хүртэл.
"""

from app.content.types import ExerciseSpec, LessonSpec, ModuleSpec, TestCaseSpec
from app.models.enums import LessonLanguage

PY = LessonLanguage.PYTHON

OOP = ModuleSpec(
    title="Модул 15 — Объект хандлагат програмчлал (OOP)",
    description="Класс, объект, өв залгамжлал.",
    lessons=[
        LessonSpec(
            title="Класс ба объект",
            slug="klass-ba-obekt",
            description="__init__, аттрибут, метод.",
            duration=480,
            language=PY,
            content="""\
Класс нь объект үүсгэх **загвар**.

```python
class Oyutan:
    def __init__(self, ner, nas):
        self.ner = ner
        self.nas = nas

    def tanilzuulah(self):
        return f"{self.ner}, {self.nas} настай"


bat = Oyutan("Бат", 20)
print(bat.tanilzuulah())
```

### self гэж юу вэ?

`self` нь **тухайн объект өөрөө**. Метод дуудахад Python түүнийг
автоматаар дамжуулна:

```python
bat.tanilzuulah()        # Python үүнийг Oyutan.tanilzuulah(bat) болгоно
```

Тиймээс метод бүрийн эхний параметр нь `self` байна.

### `__init__` — байгуулагч

Объект үүсэх үед автоматаар дуудагдана. Энд эхний утгуудыг тохируулна.

### Хэзээ класс хэрэглэх вэ?

| Нөхцөл | Сонголт |
|---|---|
| Зөвхөн өгөгдөл | `dict` эсвэл `dataclass` |
| Өгөгдөл + түүн дээрх үйлдэл | `class` |
| Зөвхөн үйлдэл | энгийн функц |

Класс нь **өгөгдөл ба түүнийг боловсруулах код хоёрыг нэг дор** барихад хэрэгтэй.

### `__str__` — уншигдахуйц харагдац

```python
class Oyutan:
    def __str__(self):
        return f"Oyutan({self.ner})"

print(bat)      # Oyutan(Бат)
```

Үгүй бол `<__main__.Oyutan object at 0x7f...>` гэж хэвлэгдэнэ.

### Жишээ програм

```python
class Oyutan:
    def __init__(self, ner, nas):
        self.ner = ner
        self.nas = nas
        self.dunguud = []

    def dun_nemeh(self, dun):
        self.dunguud.append(dun)

    def dundaj(self):
        if not self.dunguud:
            return 0
        return sum(self.dunguud) / len(self.dunguud)

    def __str__(self):
        return f"{self.ner} ({self.nas}) — дундаж {self.dundaj():.1f}"


bat = Oyutan("Бат", 20)
bat.dun_nemeh(90)
bat.dun_nemeh(85)

tsetseg = Oyutan("Цэцэг", 21)
tsetseg.dun_nemeh(95)

for oyutan in [bat, tsetseg]:
    print(oyutan)
```
""",
            initial_code="""\
class Dans:
    def __init__(self, ezen, uldegdel):
        # TODO: ezen, uldegdel-ийг объектын аттрибут болгон хадгал
        #       (self.ezen = ..., self.uldegdel = ...)
        pass

    def hiih(self, dun):
        # TODO: үлдэгдлийг dun-аар нэмэгдүүл
        pass

    def avah(self, dun):
        # TODO: үлдэгдэл хүрэлцэх бол dun-г хасаад True буцаа.
        #       Хүрэлцэхгүй бол юу ч өөрчлөхгүйгээр False буцаа.
        return False

    def __str__(self):
        # TODO: "Бат: 700₮" хэлбэрийн мөр буцаа
        return "Dans"


# Доорх хэсэг бэлэн — зөвхөн дээрх классыг гүйцээнэ.
n = int(input())
dansuud = {}
for _ in range(n):
    ezen, uldegdel = input().split()
    dansuud[ezen] = Dans(ezen, int(uldegdel))

m = int(input())
for _ in range(m):
    hesguud = input().split()
    uildel = hesguud[0]
    if uildel == "hiih":
        dansuud[hesguud[1]].hiih(int(hesguud[2]))
    elif uildel == "avah":
        if not dansuud[hesguud[1]].avah(int(hesguud[2])):
            print(f"Алдаа: үлдэгдэл хүрэлцэхгүй ({hesguud[1]})")
    elif uildel == "shiljuuleh":
        ilgeegch = dansuud[hesguud[1]]
        huleen_avagch = dansuud[hesguud[2]]
        dun = int(hesguud[3])
        if ilgeegch.avah(dun):
            huleen_avagch.hiih(dun)
        else:
            print(f"Алдаа: үлдэгдэл хүрэлцэхгүй ({hesguud[1]})")

for dans in dansuud.values():
    print(dans)
""",
            exercise=ExerciseSpec(
                statement="""\
Банкны данс бүрийг `Dans` классын **объект** болгоно. Объект бүр өөрийн
эзэн, үлдэгдэлтэй — нэг дансанд хийсэн өөрчлөлт нөгөөд нөлөөлөх ёсгүй.

Классын аргууд:

- `__init__(ezen, uldegdel)` — эзний нэр, эхний үлдэгдлийг хадгална.
- `hiih(dun)` — үлдэгдлийг `dun`-аар нэмнэ.
- `avah(dun)` — үлдэгдэл хүрэлцэх бол хасаад `True`, эс бөгөөс юу ч
  өөрчлөхгүйгээр `False` буцаана. Үлдэгдлээ бүтнээр нь авч болно.
- `__str__()` — `Бат: 700₮` хэлбэрийн мөр буцаана.

Оролт уншиж, командыг гүйцэтгэж, үр дүнг хэвлэх хэсэг эхлэл кодод бэлэн —
зөвхөн классыг гүйцээнэ.

**Оролт:** эхний мөрөнд дансны тоо `n`, дараагийн `n` мөрөнд
`<эзэн> <үлдэгдэл>`. Дараа нь командын тоо `m`, түүний дараа `m` команд:

```text
hiih <эзэн> <дүн>
avah <эзэн> <дүн>
shiljuuleh <илгээгч> <хүлээн авагч> <дүн>
```

**Гаралт:** `avah` эсвэл `shiljuuleh` амжилтгүй болох бүрт
`Алдаа: үлдэгдэл хүрэлцэхгүй (<эзэн>)` (шилжүүлэгт илгээгчийн нэр).
Төгсгөлд нь данс бүрийг оролтын дарааллаар `print(dans)`-аар хэвлэнэ.

**Хязгаарлалт:** нэр нь зайгүй нэг үг, бүх дүн эерэг бүхэл тоо.
""",
                tests=(
                    TestCaseSpec(
                        stdin=(
                            "2\nБат 1000\nСараа 500\n3\n"
                            "hiih Сараа 250\navah Бат 300\navah Сараа 1000\n"
                        ),
                        expected_output=(
                            "Алдаа: үлдэгдэл хүрэлцэхгүй (Сараа)\nБат: 700₮\nСараа: 750₮\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin=(
                            "3\nДорж 0\nБолд 2000\nГэрэл 100\n3\n"
                            "shiljuuleh Болд Дорж 1500\nshiljuuleh Гэрэл Болд 200\n"
                            "avah Дорж 1500\n"
                        ),
                        expected_output=(
                            "Алдаа: үлдэгдэл хүрэлцэхгүй (Гэрэл)\n"
                            "Дорж: 0₮\nБолд: 500₮\nГэрэл: 100₮\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(stdin="1\nАну 300\n0\n", expected_output="Ану: 300₮\n"),
                    TestCaseSpec(
                        stdin=(
                            "2\nТэмүүжин 100\nНомин 50\n6\n"
                            "avah Тэмүүжин 101\nhiih Тэмүүжин 1\navah Тэмүүжин 101\n"
                            "shiljuuleh Номин Тэмүүжин 50\nshiljuuleh Тэмүүжин Номин 51\n"
                            "avah Номин 52\n"
                        ),
                        expected_output=(
                            "Алдаа: үлдэгдэл хүрэлцэхгүй (Тэмүүжин)\n"
                            "Алдаа: үлдэгдэл хүрэлцэхгүй (Тэмүүжин)\n"
                            "Алдаа: үлдэгдэл хүрэлцэхгүй (Номин)\n"
                            "Тэмүүжин: 50₮\nНомин: 0₮\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="3\nА 500\nБ 500\nВ 500\n2\nhiih А 100\navah В 500\n",
                        expected_output="А: 600₮\nБ: 500₮\nВ: 0₮\n",
                    ),
                ),
                solution="""\
class Dans:
    def __init__(self, ezen, uldegdel):
        # Объект бүр өөрийн эзэн, үлдэгдэлтэй — self-д хадгална
        self.ezen = ezen
        self.uldegdel = uldegdel

    def hiih(self, dun):
        self.uldegdel += dun

    def avah(self, dun):
        # Хүрэлцэхгүй бол үлдэгдэлд огт хүрэхгүй. Тэнцүү бол авч болно.
        if dun > self.uldegdel:
            return False
        self.uldegdel -= dun
        return True

    def __str__(self):
        # print(dans) үүнийг автоматаар дуудна — хэвлэхгүй, буцаана
        return f"{self.ezen}: {self.uldegdel}₮"


n = int(input())
dansuud = {}
for _ in range(n):
    ezen, uldegdel = input().split()
    dansuud[ezen] = Dans(ezen, int(uldegdel))

m = int(input())
for _ in range(m):
    hesguud = input().split()
    uildel = hesguud[0]
    if uildel == "hiih":
        dansuud[hesguud[1]].hiih(int(hesguud[2]))
    elif uildel == "avah":
        if not dansuud[hesguud[1]].avah(int(hesguud[2])):
            print(f"Алдаа: үлдэгдэл хүрэлцэхгүй ({hesguud[1]})")
    elif uildel == "shiljuuleh":
        ilgeegch = dansuud[hesguud[1]]
        huleen_avagch = dansuud[hesguud[2]]
        dun = int(hesguud[3])
        # Эхлээд илгээгчээс авч чадвал л хүлээн авагчид хийнэ
        if ilgeegch.avah(dun):
            huleen_avagch.hiih(dun)
        else:
            print(f"Алдаа: үлдэгдэл хүрэлцэхгүй ({hesguud[1]})")

for dans in dansuud.values():
    print(dans)
""",
                tips="""\
- `self` бол тухайн объект өөрөө: `__init__` дотор `self.ezen = ezen` гэж
  хадгалсан утгыг бусад арга `self.ezen`-ээр уншина.
- Үлдэгдлийг **объектын** аттрибутад (`self.uldegdel`) хадгал. `class Dans:`-ийн
  шууд доор хувьсагч зарлавал бүх данс нэг утгыг хуваалцана.
- `avah` нь хүрэлцэхгүй үед үлдэгдэлд огт хүрэх ёсгүй — эхлээд шалгаад,
  дараа нь хас. Үлдэгдэлтэй яг тэнцүү дүнг авч болно (`>` ба `>=`-г андуурахгүй).
- `__str__` нь хэвлэхгүй, мөрийг **буцаана** (`return f"..."`) — `print(dans)`
  түүнийг өөрөө дуудна.
""",
            ),
        ),
        LessonSpec(
            title="Өв залгамжлал ба property",
            slug="uv-zalgamjlal",
            description="Классыг өргөтгөх, хандалтыг хянах.",
            duration=480,
            language=PY,
            content="""\
### Өв залгамжлал

```python
class Hun:
    def __init__(self, ner):
        self.ner = ner

    def mendleh(self):
        return f"Сайн байна уу, би {self.ner}"


class Bagsh(Hun):
    def __init__(self, ner, hicheel):
        super().__init__(ner)       # эцэг классын __init__
        self.hicheel = hicheel

    def mendleh(self):
        return f"{super().mendleh()}. Би {self.hicheel} заадаг."
```

`super()` нь эцэг классын хувилбарыг дуудна. Кодыг давтахгүй байхад хэрэгтэй.

### Өв залгамжлалыг хэтрүүлэхгүй байх

Гүн гүнзгий шатлал (A → B → C → D) нь ойлгоход хэцүү болгодог. Ихэнх
тохиолдолд **композиц** (объектыг аттрибут болгон агуулах) илүү уян хатан.

### property — тооцоологддог аттрибут

```python
class Tegsh_uld:
    def __init__(self, urt, urgun):
        self.urt = urt
        self.urgun = urgun

    @property
    def talbai(self):
        return self.urt * self.urgun


t = Tegsh_uld(3, 4)
print(t.talbai)        # 12 — хаалтгүй, аттрибут шиг
```

### Утгыг хамгаалах

```python
class Dans:
    def __init__(self):
        self._uldegdel = 0

    @property
    def uldegdel(self):
        return self._uldegdel

    @uldegdel.setter
    def uldegdel(self, utga):
        if utga < 0:
            raise ValueError("Үлдэгдэл сөрөг байж болохгүй")
        self._uldegdel = utga
```

Нэрний өмнөх `_` нь "дотоод хэрэглээ" гэсэн тохиролцоо. Python албадан
хаадаггүй ч хөгжүүлэгчид үүнийг хүндэтгэдэг.

### Жишээ програм

```python
class Hun:
    def __init__(self, ner):
        self.ner = ner

    def mendleh(self):
        return f"Сайн байна уу, би {self.ner}"


class Bagsh(Hun):
    def __init__(self, ner, hicheel):
        super().__init__(ner)
        self.hicheel = hicheel

    def mendleh(self):
        return f"{super().mendleh()}. Би {self.hicheel} заадаг."


class Oyutan(Hun):
    def __init__(self, ner, kurs):
        super().__init__(ner)
        self.kurs = kurs

    def mendleh(self):
        return f"{super().mendleh()}. Би {self.kurs}-р курс."


for hun in [Hun("Дорж"), Bagsh("Болд", "Python"), Oyutan("Бат", 2)]:
    print(hun.mendleh())

print("---")


class Tegsh_uld:
    def __init__(self, urt, urgun):
        self.urt = urt
        self.urgun = urgun

    @property
    def talbai(self):
        return self.urt * self.urgun


t = Tegsh_uld(3, 4)
print("Талбай:", t.talbai)
```
""",
            initial_code="""\
import math


class Durs:
    # Эцэг класс — бэлэн. Дүрс бүр нэртэй, талбайтай.
    def __init__(self, ner):
        self.ner = ner

    @property
    def talbai(self):
        return 0.0

    def __str__(self):
        return f"{self.ner}: {self.talbai:.2f}"


class TegshUntsugt(Durs):
    def __init__(self, urt, urgun, ner="Тэгш өнцөгт"):
        super().__init__(ner)
        # TODO: urt, urgun-ийг self-д хадгал

    # TODO: talbai property-г дахин тодорхойл — урт × өргөн


class Kvadrat(TegshUntsugt):
    def __init__(self, tal):
        # TODO: super()-ээр TegshUntsugt-ийг (tal, tal, "Квадрат")-аар дууд
        super().__init__(0, 0)


class Toirog(Durs):
    def __init__(self, radius):
        # TODO: super()-ээр "Тойрог" нэрийг дамжуулж, radius-ийг хадгал
        super().__init__("Тойрог")

    # TODO: talbai property — math.pi * r ** 2


# Доорх хэсэг бэлэн.
n = int(input())
dursuud = []
for _ in range(n):
    hesguud = input().split()
    toonuud = [float(x) for x in hesguud[1:]]
    if hesguud[0] == "tegsh":
        dursuud.append(TegshUntsugt(toonuud[0], toonuud[1]))
    elif hesguud[0] == "kvadrat":
        dursuud.append(Kvadrat(toonuud[0]))
    elif hesguud[0] == "toirog":
        dursuud.append(Toirog(toonuud[0]))

niit = 0.0
for durs in dursuud:
    print(durs)
    niit += durs.talbai
print(f"Нийт талбай: {niit:.2f}")
""",
            exercise=ExerciseSpec(
                statement="""\
Дүрсийн талбай тооцоолох классын шатлал бич. Эцэг класс `Durs` бэлэн:
нэртэй, `talbai` **property**-тэй (анхдагч нь `0.0`), `__str__` нь
`<нэр>: <талбай>`-г хоёр оронтой буцаана. Түүнээс удамшуулж:

- `TegshUntsugt(urt, urgun)` — нэр нь `Тэгш өнцөгт`, талбай нь `urt × urgun`.
- `Kvadrat(tal)` — `TegshUntsugt`-ээс удамшина, нэр нь `Квадрат`. Талбайг
  дахин бичихгүй — эцгийнхээ `talbai`-г ашиглана.
- `Toirog(radius)` — нэр нь `Тойрог`, талбай нь `math.pi × r²`.

Эцэг классын `__init__`-ийг `super()`-ээр дууд. Оролт уншиж хэвлэх хэсэг
эхлэл кодод бэлэн.

**Оролт:** эхний мөрөнд дүрсийн тоо `n` (1 ≤ n ≤ 20). Дараагийн `n` мөр бүрт
дараах хэлбэрийн аль нэг нь:

```text
tegsh <урт> <өргөн>
kvadrat <тал>
toirog <радиус>
```

Хэмжээ нь эерэг, бутархай байж болно.

**Гаралт:** дүрс бүрийг оролтын дарааллаар `<нэр>: <талбай>`, сүүлийн мөрөнд
`Нийт талбай: <нийлбэр>` — бүх тоо хоёр оронтой (`.2f`).
""",
                tests=(
                    TestCaseSpec(
                        stdin="3\ntegsh 3 4\nkvadrat 5\ntoirog 1\n",
                        expected_output=(
                            "Тэгш өнцөгт: 12.00\nКвадрат: 25.00\nТойрог: 3.14\nНийт талбай: 40.14\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="2\ntoirog 2\ntegsh 2.5 1.5\n",
                        expected_output="Тойрог: 12.57\nТэгш өнцөгт: 3.75\nНийт талбай: 16.32\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="1\nkvadrat 0.5\n",
                        expected_output="Квадрат: 0.25\nНийт талбай: 0.25\n",
                    ),
                    TestCaseSpec(
                        stdin="4\ntoirog 0.5\nkvadrat 1\ntegsh 10 0.1\ntoirog 10\n",
                        expected_output=(
                            "Тойрог: 0.79\nКвадрат: 1.00\nТэгш өнцөгт: 1.00\nТойрог: 314.16\n"
                            "Нийт талбай: 316.94\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="3\ntegsh 100 200\nkvadrat 12\ntoirog 3\n",
                        expected_output=(
                            "Тэгш өнцөгт: 20000.00\nКвадрат: 144.00\nТойрог: 28.27\n"
                            "Нийт талбай: 20172.27\n"
                        ),
                    ),
                ),
                solution="""\
import math


class Durs:
    def __init__(self, ner):
        self.ner = ner

    @property
    def talbai(self):
        return 0.0

    def __str__(self):
        # self.talbai нь тухайн объектын классын хувилбарыг автоматаар авна
        return f"{self.ner}: {self.talbai:.2f}"


class TegshUntsugt(Durs):
    def __init__(self, urt, urgun, ner="Тэгш өнцөгт"):
        super().__init__(ner)  # нэрийг эцэг класс хадгална
        self.urt = urt
        self.urgun = urgun

    @property
    def talbai(self):
        return self.urt * self.urgun


class Kvadrat(TegshUntsugt):
    def __init__(self, tal):
        # Квадрат бол талууд нь тэнцүү тэгш өнцөгт — talbai-г өвлөж авна
        super().__init__(tal, tal, "Квадрат")


class Toirog(Durs):
    def __init__(self, radius):
        super().__init__("Тойрог")
        self.radius = radius

    @property
    def talbai(self):
        return math.pi * self.radius**2


n = int(input())
dursuud = []
for _ in range(n):
    hesguud = input().split()
    toonuud = [float(x) for x in hesguud[1:]]
    if hesguud[0] == "tegsh":
        dursuud.append(TegshUntsugt(toonuud[0], toonuud[1]))
    elif hesguud[0] == "kvadrat":
        dursuud.append(Kvadrat(toonuud[0]))
    elif hesguud[0] == "toirog":
        dursuud.append(Toirog(toonuud[0]))

niit = 0.0
for durs in dursuud:
    print(durs)
    niit += durs.talbai
print(f"Нийт талбай: {niit:.2f}")
""",
                tips="""\
- `class Kvadrat(TegshUntsugt):` гэвэл `Kvadrat` эцгийнхээ бүх зүйлийг —
  `talbai`, `__str__`-г — өвлөнө. Зөвхөн ялгаатай хэсгийг л бич.
- Хүүхэд классын `__init__` эцгийнхийг өөрөө дуудахгүй — `super().__init__(...)`
  гэж заавал дууд, эс бөгөөс `self.ner` үүсэхгүй.
- Хүүхэд класст `@property def talbai` дахин тодорхойлоход `Durs.__str__`
  доторх `self.talbai` тухайн объектын хувилбарыг автоматаар авна.
- Property-г хаалтгүй уншина: `durs.talbai` (`durs.talbai()` биш).
""",
            ),
        ),
    ],
)

ITERATORS = ModuleSpec(
    title="Модул 16 — Iterator ба Generator",
    description="Санах ой хэмнэсэн дараалал.",
    lessons=[
        LessonSpec(
            title="Generator ба yield",
            slug="generator-yield",
            description="Утгыг нэг нэгээр нь үйлдвэрлэх.",
            duration=480,
            language=PY,
            content="""\
Generator нь утгыг **урьдчилж бэлдэхгүй**, шаардсан үед нь нэг нэгээр өгнө.

```python
def toonuud(hyazgaar):
    for i in range(hyazgaar):
        yield i
```

`return` нь функцийг зогсоодог бол `yield` нь **түр зогсоож**, дараа нь
яг тэр байрнаасаа үргэлжилнэ.

### Яагаад хэрэгтэй вэ?

```python
# Жагсаалт: 10 сая тоог САНАХ ОЙД бүгдийг нь хадгална
jagsaalt = [i for i in range(10_000_000)]

# Generator: нэг удаад нэг тоо л санах ойд байна
gen = (i for i in range(10_000_000))
```

Том файл, өгөгдлийн сангийн мөрүүдийг боловсруулахад энэ ялгаа шийдвэрлэх
ач холбогдолтой.

### Нэг удаа л дамжина

```python
gen = (i for i in range(3))
print(list(gen))     # [0, 1, 2]
print(list(gen))     # []  ← дууссан
```

Generator нь "хэрэглэгдэж дуусдаг". Дахин хэрэгтэй бол дахин үүсгэнэ.

### Практик жишээ: том файлыг шүүх

```python
def aldaatai_murnuud(zam):
    with open(zam, encoding="utf-8") as f:
        for mur in f:
            if "ERROR" in mur:
                yield mur.strip()
```

Файл хэчнээн том байсан ч санах ой дүүрэхгүй.

### Жишээ програм

```python
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b


print(list(fibonacci(10)))

print("---")


# Generator илэрхийлэл
kvadratuud = (too ** 2 for too in range(1, 6))
print("Нийлбэр:", sum(kvadratuud))

print("---")


# Шүүх generator
def zuvhun_tegsh(toonuud):
    for too in toonuud:
        if too % 2 == 0:
            yield too


print(list(zuvhun_tegsh(range(10))))
```
""",
            initial_code="""\
def collatz(n):
    # TODO: n != 1 байх хооронд n-г yield хийгээд дараагийн утга руу шилж
    #       (тэгш бол n // 2, сондгой бол 3 * n + 1).
    #       Төгсгөлд нь 1-ийг мөн yield хий.
    yield n


hesguud = input().split()
n = int(hesguud[0])
k = int(hesguud[1])

# TODO 1: for utga in collatz(n): ... — эхний k утгыг цуглуулаад нэг мөрөнд
#         зайгаар хэвлэ. k хүрмэгц break.

# TODO 2: collatz(n)-ийг ДАХИН дуудаж алхмын тоо (утгын тоо - 1) ба
#         хамгийн их утгыг ол. «Алхам: ...», «Хамгийн их: ...» гэж хэвлэ.
""",
            exercise=ExerciseSpec(
                statement="""\
Коллацын дараалал: `n` тэгш бол дараагийнх нь `n // 2`, сондгой бол
`3 * n + 1`. Ямар ч тооноос эхэлсэн эцэст нь `1`-д хүрдэг гэж үздэг.

Дарааллын утгыг `yield`-ээр нэг нэгээр нь өгдөг `collatz(n)` **generator**
бич — `n`-ээс эхэлж `1`-ээр дуусна (хоёулаа орно). Түүнийгээ ашиглан:

1. эхний `k` утгыг хэвлэ — `k`-д хүрмэгц зогсоно, үлдсэнийг нь тооцох
   шаардлагагүй;
2. алхмын тоо (утгын тоо − 1) ба хамгийн их утгыг ол.

**Оролт:** нэг мөрөнд `n k` (1 ≤ n ≤ 100 000, 1 ≤ k ≤ 1000).

**Гаралт:** гурван мөр:

```text
<эхний k утга, зайгаар тусгаарлагдсан>
Алхам: <тоо>
Хамгийн их: <утга>
```

Дараалал `k`-аас богино бол бүтнээр нь хэвлэнэ.
""",
                tests=(
                    TestCaseSpec(
                        stdin="6 5\n",
                        expected_output="6 3 10 5 16\nАлхам: 8\nХамгийн их: 16\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="7 100\n",
                        expected_output=(
                            "7 22 11 34 17 52 26 13 40 20 10 5 16 8 4 2 1\n"
                            "Алхам: 16\nХамгийн их: 52\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(stdin="1 3\n", expected_output="1\nАлхам: 0\nХамгийн их: 1\n"),
                    TestCaseSpec(
                        stdin="27 10\n",
                        expected_output=(
                            "27 82 41 124 62 31 94 47 142 71\nАлхам: 111\nХамгийн их: 9232\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="16 1\n",
                        expected_output="16\nАлхам: 4\nХамгийн их: 16\n",
                    ),
                ),
                solution="""\
def collatz(n):
    # return биш yield — утга бүрийн дараа функц түр зогсоод, дараа нь үргэлжилнэ
    while n != 1:
        yield n
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
    yield 1  # давталт 1 дээр зогсдог тул сүүлийн утгыг тусад нь өгнө


hesguud = input().split()
n = int(hesguud[0])
k = int(hesguud[1])

# 1. Эхний k утга — break хийсний дараах утгууд хэзээ ч тооцоологдохгүй
ehnii = []
for utga in collatz(n):
    if len(ehnii) == k:
        break
    ehnii.append(str(utga))
print(" ".join(ehnii))

# 2. Generator нэг л удаа дамжина — ШИНЭ generator үүсгэж нэг давталтаар тоолно
too = 0
hamgiin_ih = 0
for utga in collatz(n):
    too += 1
    hamgiin_ih = max(hamgiin_ih, utga)
print(f"Алхам: {too - 1}")
print(f"Хамгийн их: {hamgiin_ih}")
""",
                tips="""\
- `yield` нь утгыг гаргаж өгөөд функцийг **түр зогсооно**; дараагийн утга
  хэрэгтэй үед яг тэр байрнаасаа үргэлжилнэ.
- Сүүлийн `1`-ийг мартах нь түгээмэл: `while n != 1` давталт `1` дээр зогсдог
  тул `1`-ийг давталтын дараа тусад нь `yield` хий.
- Generator нэг л удаа дамжина. Эхний `k` утгыг аваад `break` хийсэн
  generator-оос дахин тоолж болохгүй — `collatz(n)`-ийг дахин дуудаж шинийг ав.
- Хуваахдаа `//` ашигла — `/` нь бутархай тоо (`5.0`) гаргана.
""",
            ),
        ),
    ],
)

FUNCTIONAL = ModuleSpec(
    title="Модул 17 — Функционал боломжууд",
    description="lambda, map, filter, sorted.",
    lessons=[
        LessonSpec(
            title="lambda ба дээд эрэмбийн функц",
            slug="lambda-map-filter",
            description="Функцийг утга болгон дамжуулах.",
            duration=420,
            language=PY,
            content="""\
### lambda — нэргүй богино функц

```python
nemeh = lambda a, b: a + b      # ингэж бичихээс
def nemeh(a, b): return a + b   # ингэж бичсэн нь дээр
```

lambda-г **хувьсагчид оноохгүй**. Түүний жинхэнэ зориулалт нь өөр функцэд
шууд дамжуулах:

```python
oyutnuud.sort(key=lambda o: o["dun"])
```

### sorted -ийн key

Модул 14-т `key=`-д `def`-ээр бичсэн функцийн нэрийг дамжуулсан. lambda нь
яг ийм жижиг функцийг дуудлага дотор нь шууд бичих боломж олгоно:

```python
oyutnuud = [
    {"ner": "Бат", "dun": 85},
    {"ner": "Цэцэг", "dun": 95},
]

eremblesen = sorted(oyutnuud, key=lambda o: o["dun"], reverse=True)
```

Энэ бол lambda-гийн хамгийн түгээмэл, хамгийн зөв хэрэглээ.

### map ба filter

```python
toonuud = [1, 2, 3, 4]

kvadrat = list(map(lambda x: x ** 2, toonuud))
tegsh = list(filter(lambda x: x % 2 == 0, toonuud))
```

Гэхдээ Python-д comprehension нь ихэвчлэн **илүү уншигдахуйц**:

```python
kvadrat = [x ** 2 for x in toonuud]
tegsh = [x for x in toonuud if x % 2 == 0]
```

Олон Python хөгжүүлэгч `map`/`filter`-ээс илүү comprehension-ыг сонгодог.

### Хэрэгтэй бэлэн функцууд

```python
print(any([False, True]))     # True — дор хаяж нэг нь
print(all([True, True]))      # True — бүгд
print(max(oyutnuud, key=lambda o: o["dun"]))
print(sum(o["dun"] for o in oyutnuud))
```

### Жишээ програм

```python
oyutnuud = [
    {"ner": "Бат", "dun": 85},
    {"ner": "Цэцэг", "dun": 95},
    {"ner": "Болд", "dun": 72},
]

# Эрэмбэлэх — lambda-гийн зөв хэрэглээ
eremblesen = sorted(oyutnuud, key=lambda o: o["dun"], reverse=True)
for i, o in enumerate(eremblesen, start=1):
    print(f"{i}. {o['ner']} — {o['dun']}")

print("---")

print("Хамгийн өндөр:", max(oyutnuud, key=lambda o: o["dun"])["ner"])
print("Дундаж:", sum(o["dun"] for o in oyutnuud) / len(oyutnuud))
print("Бүгд тэнцсэн үү?", all(o["dun"] >= 60 for o in oyutnuud))
print("Хэн нэг нь 90-ээс дээш үү?", any(o["dun"] > 90 for o in oyutnuud))
```
""",
            initial_code="""\
tusuv = int(input())
n = int(input())
baraanuud = []
for _ in range(n):
    ner, une, unelgee = input().split()
    baraanuud.append({"ner": ner, "une": int(une), "unelgee": int(unelgee)})

# TODO 1: sorted(baraanuud, key=lambda b: ...) — үнэлгээ буурах, үнэ өсөх,
#         нэр өсөх. Зөвлөгөө: key нь tuple буцааж болно.
eremblesen = baraanuud

for i, b in enumerate(eremblesen, start=1):
    print(f"{i}. {b['ner']} ({b['unelgee']} од) {b['une']}₮")

# TODO 2: filter(lambda b: ..., eremblesen) — үнэ нь төсөвт багтах бараа

# TODO 3: «Төсөвт багтах: ...» ба min(..., key=lambda b: ...)-ээр
#         «Хамгийн хямд: ...» хэвлэ. Багтах бараа байхгүй бол зөвхөн
#         «Төсөвт багтах: байхгүй» гэж хэвлэнэ.
""",
            exercise=ExerciseSpec(
                statement="""\
Онлайн дэлгүүрийн барааг эрэмбэлж, төсөвт багтахыг нь шүүнэ. `sorted`,
`filter`, `min`-д `key=lambda ...` дамжуулж бодоорой.

Эрэмбэ: **үнэлгээгээр буурах**, тэнцвэл **үнээр өсөх**, тэнцвэл **нэрээр**
(Python-ы мөр жиших дарааллаар).

**Оролт:** эхний мөрөнд төсөв (бүхэл тоо), дараагийн мөрөнд барааны тоо
`n` (1 ≤ n ≤ 20). Дараагийн `n` мөр бүрт `<нэр> <үнэ> <үнэлгээ>` — нэр нь
зайгүй нэг үг, үнэ ба үнэлгээ (1–5) нь бүхэл тоо.

**Гаралт:**

```text
1. <нэр> (<үнэлгээ> од) <үнэ>₮
2. ...
Төсөвт багтах: <нэр>, <нэр>, ...
Хамгийн хямд: <нэр>
```

«Төсөвт багтах» нь үнэ ≤ төсөв барааг **эрэмбэлсэн дарааллаар** нь
жагсаана. «Хамгийн хямд» нь тэдгээрээс хамгийн бага үнэтэй, тэнцвэл нэрээр
түрүүлэх нь. Нэг ч бараа багтахгүй бол `Төсөвт багтах: байхгүй` гэж хэвлээд
«Хамгийн хямд» мөрийг хэвлэхгүй.
""",
                tests=(
                    TestCaseSpec(
                        stdin="15000\n4\nНом 12000 5\nҮзэг 1500 4\nЦүнх 45000 5\nДэвтэр 1500 4\n",
                        expected_output=(
                            "1. Ном (5 од) 12000₮\n2. Цүнх (5 од) 45000₮\n"
                            "3. Дэвтэр (4 од) 1500₮\n4. Үзэг (4 од) 1500₮\n"
                            "Төсөвт багтах: Ном, Дэвтэр, Үзэг\nХамгийн хямд: Дэвтэр\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="1000\n2\nЦаг 250000 3\nУтас 900000 5\n",
                        expected_output=(
                            "1. Утас (5 од) 900000₮\n2. Цаг (3 од) 250000₮\n"
                            "Төсөвт багтах: байхгүй\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="5000\n3\nСүү 3000 4\nАаруул 3000 4\nБяслаг 3000 4\n",
                        expected_output=(
                            "1. Ааруул (4 од) 3000₮\n2. Бяслаг (4 од) 3000₮\n"
                            "3. Сүү (4 од) 3000₮\n"
                            "Төсөвт багтах: Ааруул, Бяслаг, Сүү\nХамгийн хямд: Ааруул\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="2500\n1\nТалх 2500 2\n",
                        expected_output=(
                            "1. Талх (2 од) 2500₮\nТөсөвт багтах: Талх\nХамгийн хямд: Талх\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin=(
                            "10000\n5\nАлим 800 3\nБанан 1200 5\nЖүрж 9999 5\n"
                            "Тарвас 10001 4\nЛийр 800 4\n"
                        ),
                        expected_output=(
                            "1. Банан (5 од) 1200₮\n2. Жүрж (5 од) 9999₮\n"
                            "3. Лийр (4 од) 800₮\n4. Тарвас (4 од) 10001₮\n"
                            "5. Алим (3 од) 800₮\n"
                            "Төсөвт багтах: Банан, Жүрж, Лийр, Алим\nХамгийн хямд: Алим\n"
                        ),
                    ),
                ),
                solution="""\
tusuv = int(input())
n = int(input())
baraanuud = []
for _ in range(n):
    ner, une, unelgee = input().split()
    baraanuud.append({"ner": ner, "une": int(une), "unelgee": int(unelgee)})

# tuple-ийг зүүнээс нь жишнэ. Зөвхөн үнэлгээг буурахаар — хасах тэмдгээр
eremblesen = sorted(baraanuud, key=lambda b: (-b["unelgee"], b["une"], b["ner"]))
for i, b in enumerate(eremblesen, start=1):
    print(f"{i}. {b['ner']} ({b['unelgee']} од) {b['une']}₮")

# filter нь эрэмбэлсэн дарааллыг хадгална
bagtah = list(filter(lambda b: b["une"] <= tusuv, eremblesen))
if bagtah:
    print("Төсөвт багтах: " + ", ".join(map(lambda b: b["ner"], bagtah)))
    hyamd = min(bagtah, key=lambda b: (b["une"], b["ner"]))
    print(f"Хамгийн хямд: {hyamd['ner']}")
else:
    print("Төсөвт багтах: байхгүй")
""",
                tips="""\
- `key=` нь элемент бүрээс жиших утгыг гаргадаг функц.
  `lambda b: (-b["unelgee"], b["une"], b["ner"])` гэвэл эхний утгаар, тэнцвэл
  дараагийнхаар нь жишинэ.
- `reverse=True` бүх түлхүүрийг зэрэг эргүүлж, нэрийг ч урвуулна. Зөвхөн
  үнэлгээг буурахаар эрэмбэлэхийн тулд тоог нь хасах болго.
- `filter`, `map` нь «залхуу» объект буцаана — `list(...)`-д хийх эсвэл
  `", ".join(...)`-д шууд өг.
- Төсөвтэй **яг тэнцүү** үнэтэй бараа багтана (`<=`). Хамгийн хямдыг олохдоо
  тэнцсэн үнэтэй бараанаас нэрээр түрүүлэхийг нь сонго.
""",
            ),
        ),
    ],
)

TYPE_HINTS = ModuleSpec(
    title="Модул 18 — Type hints",
    description="Кодоо өөрөө өөрийгөө тайлбарладаг болгох.",
    lessons=[
        LessonSpec(
            title="Төрлийн тэмдэглэгээ",
            slug="type-hints",
            description="Уншигдац ба хэрэгслийн дэмжлэг.",
            duration=420,
            language=PY,
            content="""\
```python
def mendchileh(ner: str) -> str:
    return f"Сайн байна уу, {ner}"
```

`: str` нь параметрийн төрөл, `-> str` нь буцаах утгын төрөл.

### Python үүнийг албадахгүй

```python
mendchileh(42)      # ажиллана! Python шалгахгүй
```

Тэгвэл юунд хэрэгтэй вэ?

1. **Кодыг уншигчид** ойлгомжтой болгоно
2. **Засварлагч** (VS Code) автомат нөхөлт, анхааруулга өгнө
3. **mypy** гэх хэрэгсэл алдааг ажиллуулахаас өмнө олно

### Түгээмэл тэмдэглэгээ

```python
toonuud: list[int] = [1, 2, 3]
tohirgoo: dict[str, str] = {"hel": "mn"}
hos: tuple[int, int] = (1, 2)
```

### None байж болох утга

```python
def hereglegch_oloh(id: int) -> User | None:
    ...
```

`| None` нь "энэ функц юу ч олохгүй байж магадгүй" гэдгийг **тодорхой хэлж**
байна. Дуудаж буй хүн шалгах ёстойгоо мэднэ.

### Хэзээ бичих вэ?

| Хаана | Зөвлөмж |
|---|---|
| Нийтийн функц, класс | Заавал |
| Багийн төсөл | Заавал |
| Богино скрипт | Сонголтоор |

Энэ платформын backend код бүхэлдээ type hint ашигладаг.

### Жишээ програм

```python
def mendchileh(ner: str) -> str:
    return f"Сайн байна уу, {ner}"


def dundaj(toonuud: list[float]) -> float:
    if not toonuud:
        return 0.0
    return sum(toonuud) / len(toonuud)


def oyutan_oloh(oyutnuud: list[dict], ner: str) -> dict | None:
    for oyutan in oyutnuud:
        if oyutan["ner"] == ner:
            return oyutan
    return None


print(mendchileh("Бат"))
print(dundaj([90.0, 85.5, 78.0]))

oyutnuud = [{"ner": "Бат", "dun": 85}]
oldson = oyutan_oloh(oyutnuud, "Цэцэг")
print("Олдсон эсэх:", oldson)
```
""",
            initial_code="""\
def mur_zadlah(mur: str) -> tuple[str, int] | None:
    # TODO: "Бат 85" -> ("Бат", 85).
    #       Яг хоёр хэсэггүй, эсвэл дүн нь 0-100 хоорондох бүхэл тоо биш бол None.
    return None


def dundaj(dunguud: list[int]) -> float | None:
    # TODO: хоосон бол None, эс бөгөөс арифметик дундаж
    return None


def shildeg(oyutnuud: list[tuple[str, int]]) -> str | None:
    # TODO: хамгийн өндөр дүнтэй оюутны нэр (тэнцвэл өмнө нь ирсэн нь).
    #       Хоосон бол None.
    return None


n = int(input())
oyutnuud: list[tuple[str, int]] = []
for _ in range(n):
    mur = input()
    zadalsan = mur_zadlah(mur)
    # TODO: None бол «Алгассан: <мөр>» хэвлэ, эс бөгөөс oyutnuud-д нэм

# TODO: «Хүчинтэй: ...», «Дундаж: ...», «Шилдэг: ...» хэвлэ.
#       Функц None буцаавал утгын оронд «байхгүй» гэж хэвлэнэ.
""",
            exercise=ExerciseSpec(
                statement="""\
Оюутны дүнгийн файлын мөрүүдийг шалгаж, тайлан гаргана. Функц бүр төрлийн
тэмдэглэгээтэй — `| None` нь «үр дүн байхгүй байж болно, шалгаж ашигла»
гэдгийг дуудаж буй кодод сануулна:

- `mur_zadlah(mur: str) -> tuple[str, int] | None` — `"Бат 85"`-г
  `("Бат", 85)` болгоно. Мөр яг хоёр хэсэггүй, эсвэл дүн нь 0–100 хоорондох
  бүхэл тоо биш бол `None`.
- `dundaj(dunguud: list[int]) -> float | None` — хоосон бол `None`.
- `shildeg(oyutnuud: list[tuple[str, int]]) -> str | None` — хамгийн өндөр
  дүнтэй оюутны нэр (тэнцвэл өмнө нь ирсэн нь), хоосон бол `None`.

**Оролт:** эхний мөрөнд мөрийн тоо `n` (0 ≤ n ≤ 30), дараагийн `n` мөр бүрт
`<нэр> <дүн>` байх ёстой ч буруу мөр ч орж ирж болно.

**Гаралт:** буруу мөр бүрт оролтын дарааллаар `Алгассан: <мөр>`, дараа нь:

```text
Хүчинтэй: <тоо>
Дундаж: <дундаж, .2f>
Шилдэг: <нэр>
```

Функц `None` буцаасан бол утгын оронд `байхгүй` гэж хэвлэнэ.
""",
                tests=(
                    TestCaseSpec(
                        stdin="4\nБат 85\nЦэцэг 95\nБолд абв\nДорж 73\n",
                        expected_output=(
                            "Алгассан: Болд абв\nХүчинтэй: 3\nДундаж: 84.33\nШилдэг: Цэцэг\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="2\nСараа 120\nАну\n",
                        expected_output=(
                            "Алгассан: Сараа 120\nАлгассан: Ану\n"
                            "Хүчинтэй: 0\nДундаж: байхгүй\nШилдэг: байхгүй\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin=(
                            "6\nГэрэл 100\nМөнх -5\nОюун 0\nТэмүүлэн 100\nНараа 50 60\nЗолоо 49\n"
                        ),
                        expected_output=(
                            "Алгассан: Мөнх -5\nАлгассан: Нараа 50 60\n"
                            "Хүчинтэй: 4\nДундаж: 62.25\nШилдэг: Гэрэл\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="3\nАлтан 7\nБүрэн 3.5\nЧимэг 8\n",
                        expected_output=(
                            "Алгассан: Бүрэн 3.5\nХүчинтэй: 2\nДундаж: 7.50\nШилдэг: Чимэг\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="2\nОюун 0\nБилгүүн 0\n",
                        expected_output="Хүчинтэй: 2\nДундаж: 0.00\nШилдэг: Оюун\n",
                    ),
                    TestCaseSpec(
                        stdin="0\n",
                        expected_output="Хүчинтэй: 0\nДундаж: байхгүй\nШилдэг: байхгүй\n",
                    ),
                ),
                solution="""\
def mur_zadlah(mur: str) -> tuple[str, int] | None:
    hesguud = mur.split()
    # isdigit нь "-5", "3.5", "абв" бүгдэд False — сөрөг биш бүхэл тоо л үлдэнэ
    if len(hesguud) != 2 or not hesguud[1].isdigit():
        return None
    dun = int(hesguud[1])
    if dun > 100:
        return None
    return hesguud[0], dun


def dundaj(dunguud: list[int]) -> float | None:
    if not dunguud:
        return None
    return sum(dunguud) / len(dunguud)


def shildeg(oyutnuud: list[tuple[str, int]]) -> str | None:
    if not oyutnuud:
        return None
    # max нь тэнцсэн үед эхэнд нь тааралдсаныг буцаана
    ner, _ = max(oyutnuud, key=lambda o: o[1])
    return ner


n = int(input())
oyutnuud: list[tuple[str, int]] = []
for _ in range(n):
    mur = input()
    zadalsan = mur_zadlah(mur)
    if zadalsan is None:
        print(f"Алгассан: {mur}")
    else:
        oyutnuud.append(zadalsan)

dun = dundaj([d for _, d in oyutnuud])
ner = shildeg(oyutnuud)
print(f"Хүчинтэй: {len(oyutnuud)}")
# "is None" — 0.0 дундаж ч хүчинтэй утга, "if not dun" гэвэл алдана
print("Дундаж: байхгүй" if dun is None else f"Дундаж: {dun:.2f}")
print("Шилдэг: байхгүй" if ner is None else f"Шилдэг: {ner}")
""",
                tips="""\
- Type hint-ийг Python өөрөө шалгадаггүй. Гэхдээ `-> float | None` гэж харсан
  хүн үр дүнг ашиглахаасаа өмнө `None` эсэхийг шалгах ёстойг шууд ойлгоно.
- `None` эсэхийг `is None`-оор шалга. `if not dun:` гэвэл `0.0` дундаж ч
  «байхгүй» болж хувирна.
- `"85".isdigit()` нь `True`, харин `"-5"`, `"3.5"`, `"абв"` бүгд `False` —
  `int()`-ийн өмнө ингэж шалгавал `ValueError`-оос сэргийлнэ. 0 ба 100 хоёулаа
  зөв дүн.
- `split()`-ийн дараа хэсгийн тоо яг 2 эсэхийг шалга — дүнгүй эсвэл илүү
  үгтэй мөр ч буруу.
""",
            ),
        ),
    ],
)

DATACLASSES = ModuleSpec(
    title="Модул 19 — Dataclass",
    description="Өгөгдөл хадгалах классыг товчхон бичих.",
    lessons=[
        LessonSpec(
            title="@dataclass",
            slug="dataclass",
            description="Боилерплэйт кодыг арилгах.",
            duration=420,
            language=PY,
            content="""\
### Гараар бичихэд

```python
class Tseg:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Tseg(x={self.x}, y={self.y})"

    def __eq__(self, busad):
        return self.x == busad.x and self.y == busad.y
```

### dataclass-аар

```python
from dataclasses import dataclass

@dataclass
class Tseg:
    x: int
    y: int
```

`__init__`, `__repr__`, `__eq__` бүгд автоматаар үүснэ.

```python
a = Tseg(1, 2)
print(a)              # Tseg(x=1, y=2)
print(a == Tseg(1, 2))  # True
```

### Анхдагч утга

```python
@dataclass
class Oyutan:
    ner: str
    nas: int = 18
    dunguud: list[int] = field(default_factory=list)
```

> Хувьсагч утгыг (`list`, `dict`) шууд анхдагчаар өгч **болохгүй**.
> `field(default_factory=list)` хэрэглэнэ. Эс бөгөөс бүх объект нэг
> жагсаалтыг хуваалцана — энэ нь маш төвөгтэй алдаа үүсгэдэг.

### Өөрчлөгдөхгүй болгох

```python
@dataclass(frozen=True)
class Tseg:
    x: int
    y: int
```

`frozen=True` нь өөрчлөлтөөс хамгаална. Энэ платформын агуулгын бүтэц
яг ийм байдлаар тодорхойлогдсон.

### Жишээ програм

```python
from dataclasses import dataclass, field


@dataclass
class Oyutan:
    ner: str
    nas: int = 18
    dunguud: list[int] = field(default_factory=list)

    def dundaj(self) -> float:
        return sum(self.dunguud) / len(self.dunguud) if self.dunguud else 0.0


bat = Oyutan("Бат", 20, [90, 85])
tsetseg = Oyutan("Цэцэг")

print(bat)
print(tsetseg)
print(f"Батын дундаж: {bat.dundaj():.1f}")

# Автомат харьцуулалт
print(Oyutan("Бат", 20, [90, 85]) == bat)


@dataclass(frozen=True)
class Tseg:
    x: int
    y: int


t = Tseg(1, 2)
print(t)
```
""",
            initial_code="""\
from dataclasses import dataclass


# TODO: @dataclass(frozen=True) нэмж, x: int ба y: int талбар зарла.
#       zai() нь abs(x) + abs(y)-г буцаана.
class Tseg:
    def zai(self) -> int:
        return 0


n = int(input())
tsegnuud = []
davhardsan = 0
for _ in range(n):
    x, y = input().split()
    # TODO: Tseg(int(x), int(y)) үүсгэ. Өмнө гарсан бол davhardsan-г
    #       нэмэгдүүл, үгүй бол tsegnuud-д нэм.

# TODO: цэг бүрийг print(tseg)-ээр хэвлэ
# TODO: «Давхардсан: ...» ба «Хамгийн ойр: ...» (min(..., key=lambda t: ...))
""",
            exercise=ExerciseSpec(
                statement="""\
Хавтгайн цэгүүдийг `@dataclass`-аар дүрсэлж, давхардлыг арилгана.

`Tseg` классыг `@dataclass(frozen=True)`-ээр зарла: `x: int`, `y: int`
талбартай, мөн эхээс хүрэх «хотын гудамжны» зайг буцаах `zai()` аргатай
(`|x| + |y|`). `__init__`, `__repr__`, `__eq__`-г dataclass өөрөө үүсгэнэ —
`print(tseg)` нь `Tseg(x=1, y=2)` гэж хэвлэнэ.

**Оролт:** эхний мөрөнд цэгийн тоо `n` (1 ≤ n ≤ 50), дараагийн `n` мөр бүрт
`<x> <y>` (бүхэл тоо).

**Гаралт:** давхардаагүй цэг бүрийг анх гарсан дарааллаар нь хэвлээд, дараа
нь:

```text
Давхардсан: <өмнө гарсан цэгийг дахин оруулсан тоо>
Хамгийн ойр: <zai() нь хамгийн бага цэг>
```

Хамгийн ойр цэг тэнцвэл өмнө нь гарсныг сонгоно.
""",
                tests=(
                    TestCaseSpec(
                        stdin="5\n1 2\n-3 0\n1 2\n0 0\n-3 0\n",
                        expected_output=(
                            "Tseg(x=1, y=2)\nTseg(x=-3, y=0)\nTseg(x=0, y=0)\n"
                            "Давхардсан: 2\nХамгийн ойр: Tseg(x=0, y=0)\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="3\n2 -2\n-1 3\n4 0\n",
                        expected_output=(
                            "Tseg(x=2, y=-2)\nTseg(x=-1, y=3)\nTseg(x=4, y=0)\n"
                            "Давхардсан: 0\nХамгийн ойр: Tseg(x=2, y=-2)\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="1\n7 -7\n",
                        expected_output=(
                            "Tseg(x=7, y=-7)\nДавхардсан: 0\nХамгийн ойр: Tseg(x=7, y=-7)\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="4\n5 5\n5 5\n5 5\n5 5\n",
                        expected_output=(
                            "Tseg(x=5, y=5)\nДавхардсан: 3\nХамгийн ойр: Tseg(x=5, y=5)\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="6\n10 -1\n1 2\n2 1\n-1 -2\n2 1\n0 -1\n",
                        expected_output=(
                            "Tseg(x=10, y=-1)\nTseg(x=1, y=2)\nTseg(x=2, y=1)\n"
                            "Tseg(x=-1, y=-2)\nTseg(x=0, y=-1)\n"
                            "Давхардсан: 1\nХамгийн ойр: Tseg(x=0, y=-1)\n"
                        ),
                    ),
                ),
                solution="""\
from dataclasses import dataclass


# frozen=True — өөрчлөгдөхгүй, тиймээс hash-тай: set-д хийж болно
@dataclass(frozen=True)
class Tseg:
    x: int
    y: int

    def zai(self) -> int:
        return abs(self.x) + abs(self.y)


n = int(input())
tsegnuud: list[Tseg] = []
harsan: set[Tseg] = set()
davhardsan = 0
for _ in range(n):
    x, y = input().split()
    tseg = Tseg(int(x), int(y))
    # == ба hash-ийг dataclass x, y талбараас автоматаар үүсгэсэн
    if tseg in harsan:
        davhardsan += 1
    else:
        harsan.add(tseg)
        tsegnuud.append(tseg)

for tseg in tsegnuud:
    print(tseg)  # автомат __repr__: Tseg(x=1, y=2)
print(f"Давхардсан: {davhardsan}")
# min нь тэнцсэн үед эхнийхийг нь буцаана
print(f"Хамгийн ойр: {min(tsegnuud, key=lambda t: t.zai())}")
""",
                tips="""\
- `@dataclass` нь талбарын жагсаалтаас `__init__`, `__repr__`, `__eq__`-г
  үүсгэнэ: `Tseg(1, 2) == Tseg(1, 2)` нь `True`, `print` нь `Tseg(x=1, y=2)`.
  Гараар `__str__` бичих шаардлагагүй.
- Энгийн `@dataclass`-ийг `set`-д хийвэл `TypeError: unhashable type` гарна.
  `frozen=True` нь объектыг өөрчлөгдөхгүй болгож, hash-тай болгодог.
- `Tseg(1, 2)` ба `Tseg(2, 1)` өөр цэг. Давхардлыг тоолохдоо анхных нь биш,
  **дахин** гарсныг нь л тоол.
- Хамгийн ойрыг `min(..., key=lambda t: t.zai())`-ээр ол — `min` тэнцсэн үед
  эхэнд нь тааралдсаныг буцаадаг.
""",
            ),
        ),
    ],
)

VENV = ModuleSpec(
    title="Модул 20 — Виртуал орчин",
    description="Төсөл бүрийг тусгаарлах.",
    lessons=[
        LessonSpec(
            title="venv ашиглах",
            slug="venv",
            description="Яагаад төсөл бүр өөрийн орчинтой байх ёстой вэ.",
            duration=420,
            language=PY,
            content="""\
### Асуудал

Төсөл А нь Django 3, төсөл Б нь Django 5 шаарддаг. Хоёуланг нь системд
суулгавал зөрчилдөнө.

### Шийдэл: виртуал орчин

Төсөл бүр өөрийн тусдаа сангийн багцтай болно.

```bash
python -m venv .venv
```

Идэвхжүүлэх:

```bash
# Windows
.venv\\Scripts\\activate

# macOS / Linux
source .venv/bin/activate
```

Идэвхжсэн үед тушаалын мөрөнд `(.venv)` гэж харагдана.

```bash
deactivate     # гарах
```

### Дүрэм

| Хийх | Хийхгүй |
|---|---|
| Төсөл бүрт `.venv` үүсгэх | Системийн Python руу суулгах |
| `.venv` -г `.gitignore` -д оруулах | `.venv` -г git-д хийх |
| `requirements.txt` -г git-д хийх | Багцуудыг гараар тоолж бичих |

`.venv` хавтас нь маш том бөгөөд платформ хамааралтай. Түүнийг git-д
оруулах нь хэзээ ч зөв биш.

### Энэ платформ дээр

`apps/api` хавтас яг ийм бүтэцтэй: `.venv` нь `.gitignore` дотор,
хамаарлууд нь `pyproject.toml` дотор тодорхойлогдсон.

### Жишээ програм

```python
# Виртуал орчин нь тушаалын мөрний ажил — Python код биш.
# Доорх нь ердийн урсгал:

# 1. Үүсгэх
#    python -m venv .venv

# 2. Идэвхжүүлэх
#    Windows:      .venv\\Scripts\\activate
#    macOS/Linux:  source .venv/bin/activate

# 3. Багц суулгах
#    pip install requests

# 4. Хадгалах
#    pip freeze > requirements.txt

# 5. Гарах
#    deactivate

import sys

print("Одоогийн Python:", sys.executable)
print("Хувилбар:", sys.version.split()[0])
```
""",
            initial_code="""\
# Бодит ажил дээр:
#   python -m venv .venv            # төсөл бүрт тусдаа орчин
#   pip freeze > requirements.txt   # суулгасан багцаа хадгалах
# Энд хоёр төслийн хамаарлыг оролтоос уншаад зөрчлийг олно.


def normchloh(ner: str) -> str:
    # TODO: зайг арилгаж, жижиг үсэг болгож, "_"-г "-" болго
    return ner


def unshih() -> dict[str, str]:
    # TODO: эхлээд тоог уншаад, тэр тооны "нэр==хувилбар" мөрийг
    #       {нормчилсон нэр: хувилбар} dict болгож буцаа
    return {}


a = unshih()
b = unshih()

# TODO: хоёуланд байгаа ч хувилбар нь өөр багцуудыг нэрээр эрэмбэлж ол
# TODO: «Зөрчилтэй багц: ...», мөр бүрт «  нэр: А / Б», дараа нь «Дүгнэлт: ...»
""",
            exercise=ExerciseSpec(
                statement="""\
Хоёр төсөл нэг Python орчныг хуваалцвал нэг багцын хоёр өөр хувилбар
зөрчилдөнө — яг ийм үед төсөл бүрт тусдаа `venv` үүсгэдэг. Бодит ажил дээр
хоёр орчны `pip freeze`-ийг харьцуулдаг; энд хоёр төслийн хамаарлыг
оролтоос уншаад зөрчлийг нь ол.

Багцын нэрийг pip-тэй адил **жижиг үсэг** болгож, `_`-г `-` болгож жишнэ:
`Typing_Extensions` ба `typing-extensions` нь нэг багц.

**Оролт:** эхний мөрөнд төсөл А-ийн багцын тоо, дараа нь тэр тооны
`<нэр>==<хувилбар>` мөр. Дараа нь төсөл Б-ийнх мөн адил. `==`-ийн хоёр талд
зай байж болно. Нэг төсөлд нэг багц давтагдахгүй.

**Гаралт:**

```text
Зөрчилтэй багц: <тоо>
  <нэр>: <А-ийн хувилбар> / <Б-ийн хувилбар>
Дүгнэлт: <...>
```

Зөрчилтэй багцыг (хоёуланд байгаа, хувилбар нь өөр) нормчилсон нэрээр
эрэмбэлж, мөр бүрийг хоёр зайгаар эхлүүлнэ. Дүгнэлт нь зөрчил байвал
`төсөл бүрт тусдаа venv хэрэгтэй`, үгүй бол `нэг орчинд багтана`.
""",
                tests=(
                    TestCaseSpec(
                        stdin=(
                            "3\nDjango==3.2\nrequests==2.31.0\nnumpy==1.26.4\n"
                            "2\ndjango==5.0\nrequests==2.31.0\n"
                        ),
                        expected_output=(
                            "Зөрчилтэй багц: 1\n  django: 3.2 / 5.0\n"
                            "Дүгнэлт: төсөл бүрт тусдаа venv хэрэгтэй\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="2\nflask==3.0.0\nrich==13.7.0\n1\npytest==8.0.0\n",
                        expected_output="Зөрчилтэй багц: 0\nДүгнэлт: нэг орчинд багтана\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin=(
                            "4\nTyping_Extensions==4.9.0\nPyYAML==6.0.1\nSQLAlchemy==2.0.25\n"
                            "attrs==23.2.0\n"
                            "4\nsqlalchemy==1.4.51\ntyping-extensions==4.12.2\npyyaml==6.0.1\n"
                            "Attrs==21.4.0\n"
                        ),
                        expected_output=(
                            "Зөрчилтэй багц: 3\n"
                            "  attrs: 23.2.0 / 21.4.0\n"
                            "  sqlalchemy: 2.0.25 / 1.4.51\n"
                            "  typing-extensions: 4.9.0 / 4.12.2\n"
                            "Дүгнэлт: төсөл бүрт тусдаа venv хэрэгтэй\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="0\n2\nfastapi==0.115.0\nuvicorn==0.30.0\n",
                        expected_output="Зөрчилтэй багц: 0\nДүгнэлт: нэг орчинд багтана\n",
                    ),
                    TestCaseSpec(
                        stdin=(
                            "2\nrequests == 2.28.0\nFlask==3.0.0\n"
                            "2\nflask == 3.0.0\nRequests==2.31.0\n"
                        ),
                        expected_output=(
                            "Зөрчилтэй багц: 1\n  requests: 2.28.0 / 2.31.0\n"
                            "Дүгнэлт: төсөл бүрт тусдаа venv хэрэгтэй\n"
                        ),
                    ),
                ),
                solution="""\
def normchloh(ner: str) -> str:
    # pip "Django" ба "django", "a_b" ба "a-b"-г нэг багц гэж үздэг
    return ner.strip().lower().replace("_", "-")


def unshih() -> dict[str, str]:
    bagtsuud = {}
    for _ in range(int(input())):
        ner, huvilbar = input().split("==")
        bagtsuud[normchloh(ner)] = huvilbar.strip()
    return bagtsuud


a = unshih()
b = unshih()

# Хоёуланд байгаа ч хувилбар нь өөр — нэг орчинд зэрэг суух боломжгүй
zorchil = sorted(ner for ner in a if ner in b and a[ner] != b[ner])
print(f"Зөрчилтэй багц: {len(zorchil)}")
for ner in zorchil:
    print(f"  {ner}: {a[ner]} / {b[ner]}")
if zorchil:
    print("Дүгнэлт: төсөл бүрт тусдаа venv хэрэгтэй")
else:
    print("Дүгнэлт: нэг орчинд багтана")
""",
                tips="""\
- Нэрийг dict-ийн түлхүүр болгохоосоо **өмнө** нормчил — тэгвэл `Django`,
  `django` хоёр нэг түлхүүр болж шууд жишигдэнэ.
- `"requests == 2.31.0".split("==")` хоёр хэсэг буцаана — хоёуланг нь
  `strip()` хий.
- Зөвхөн нэг төсөлд байгаа багц зөрчил биш. Хоёуланд байгаа ч хувилбар нь
  **ижил** бол мөн зөрчил биш.
- Зөрчил байхгүй үед ч `Зөрчилтэй багц: 0` мөрийг хэвлэ. Эхний төсөл огт
  багцгүй (`0`) байж болно.
""",
            ),
        ),
    ],
)

DEPENDENCIES = ModuleSpec(
    title="Модул 21 — Хамаарал (Dependencies)",
    description="Гадны сан суулгаж, удирдах.",
    lessons=[
        LessonSpec(
            title="pip ба requirements",
            slug="pip-requirements",
            description="Багц суулгах, хувилбар түгжих.",
            duration=420,
            language=PY,
            content="""\
```bash
pip install requests
pip install requests==2.31.0     # тодорхой хувилбар
pip uninstall requests
pip list                          # суулгасан бүгд
```

### requirements.txt

```text
requests==2.31.0
fastapi>=0.115
```

Суулгах:

```bash
pip install -r requirements.txt
```

### Хувилбарыг түгжих нь чухал

```text
requests           # МУУ — маргааш өөр хувилбар суух вий
requests==2.31.0   # САЙН — хэнд ч ижил ажиллана
```

Хувилбар түгжээгүй бол "миний машин дээр ажиллаж байсан" гэдэг асуудал үүснэ.

### pyproject.toml — орчин үеийн арга

```toml
[project]
name = "miny-tusul"
dependencies = [
    "requests>=2.31",
]
```

```bash
pip install -e .
```

Энэ платформын backend яг үүнийг ашигладаг.

### Аюулгүй байдал

```bash
pip audit        # мэдэгдэж буй эмзэг байдлыг шалгана
```

Гадны сан суулгах бүрт та тэдний кодыг итгэж байна гэсэн үг. Нэрийг
сайтар шалгах хэрэгтэй — "typosquatting" халдлага байдаг.

### Жишээ програм

```python
# pip нь тушаалын мөрний хэрэгсэл.

# Суулгах
#   pip install requests
#   pip install "fastapi>=0.115"

# Хадгалах
#   pip freeze > requirements.txt

# Сэргээх
#   pip install -r requirements.txt

# Эмзэг байдал шалгах
#   pip audit

# Суулгасан багцыг кодоос шалгах:
import json
import sys

print("Стандарт сангийн модул хэрэглэхэд суулгах шаардлагагүй.")
print("Жишээ:", json.dumps({"eh": "стандарт сан"}, ensure_ascii=False))
print("Python:", sys.version.split()[0])
```
""",
            initial_code="""\
# Бодит ажил дээр: pip install -r requirements.txt
# Энд файлын агуулгыг оролтоос уншаад түгжсэн/түгжээгүй багцыг ялгана.

TEMDEGUUD = ["==", ">=", "<=", "~="]


def normchloh(ner: str) -> str:
    # TODO: зайг арилгаж, жижиг үсэг болгож, "_"-г "-" болго
    return ner


def zadlah(mur: str) -> tuple[str, str, str]:
    # TODO: TEMDEGUUD-ээс мөрөнд байгаа тэмдгийг олж (нэр, тэмдэг, хувилбар)
    #       буцаа. Тэмдэг байхгүй бол (нэр, "", "").
    return normchloh(mur), "", ""


n = int(input())
tugjsen = []
tugjeegui = []
for _ in range(n):
    mur = input()
    # TODO: "#"-ээс хойшхийг хасаад strip() хий; хоосон бол алгас
    # TODO: zadlah-аар задалж, "==" бол tugjsen, бусад нь tugjeegui-д нэм

# TODO: «Түгжсэн: <тоо>», дараа нь нэрээр эрэмбэлсэн мөр бүр «  нэр==хувилбар»
# TODO: «Түгжээгүй: <тоо>» ба түүний мөрүүд
""",
            exercise=ExerciseSpec(
                statement="""\
`pip install -r requirements.txt`-ийн өмнө файлыг шалгадаг жижиг хэрэгсэл
бич: аль багц хувилбараа **түгжсэн** (`==`), аль нь түгжээгүйг ялга.

Мөр бүрийг ингэж боловсруулна:

- `#`-ээс хойшхи бүх зүйл тайлбар — хасна. Үлдсэн нь хоосон бол алгасна.
- Хувилбарын тэмдэг нь `==`, `>=`, `<=`, `~=`-ийн аль нэг, эсвэл огт
  байхгүй (`rich`). Тэмдгийн хоёр талд зай байж болно.
- Багцын нэрийг жижиг үсэг болгож, `_`-г `-` болгоно.
- `==` бол **түгжсэн**, бусад нь (тэмдэггүй ч) **түгжээгүй**.

**Оролт:** эхний мөрөнд файлын мөрийн тоо `n`, дараагийн `n` мөр нь файлын
агуулга (хоосон мөр, тайлбар орно). Багцын нэр давтагдахгүй.

**Гаралт:**

```text
Түгжсэн: <тоо>
  <нэр>==<хувилбар>
Түгжээгүй: <тоо>
  <нэр><тэмдэг><хувилбар>
```

Хэсэг бүрийн мөрүүдийг нормчилсон нэрээр эрэмбэлнэ. Мөр бүр хоёр зайгаар
эхэлж, дотроо зайгүй (`  numpy>=1.26`); тэмдэггүй багц зөвхөн нэрээрээ
(`  rich`) хэвлэгдэнэ. Хэсэг хоосон бол гарчиг нь `: 0`-тэй үлдэнэ.
""",
                tests=(
                    TestCaseSpec(
                        stdin=(
                            "6\n# Вэб сервер\nfastapi==0.115.0\nrequests==2.31.0\n\n"
                            "numpy>=1.26\nrich\n"
                        ),
                        expected_output=(
                            "Түгжсэн: 2\n  fastapi==0.115.0\n  requests==2.31.0\n"
                            "Түгжээгүй: 2\n  numpy>=1.26\n  rich\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="3\nFlask == 3.0.0   # вэб\npython_dotenv~=1.0\nJinja2\n",
                        expected_output=(
                            "Түгжсэн: 1\n  flask==3.0.0\n"
                            "Түгжээгүй: 2\n  jinja2\n  python-dotenv~=1.0\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="3\n# хоосон файл\n\n   # зөвхөн тайлбар\n",
                        expected_output="Түгжсэн: 0\nТүгжээгүй: 0\n",
                    ),
                    TestCaseSpec(
                        stdin=(
                            "5\nDjango<=5.0\ndjango-cors-headers==4.3.1\npytest==8.0.0  # test\n"
                            "black\nPillow>=10.0\n"
                        ),
                        expected_output=(
                            "Түгжсэн: 2\n  django-cors-headers==4.3.1\n  pytest==8.0.0\n"
                            "Түгжээгүй: 3\n  black\n  django<=5.0\n  pillow>=10.0\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="4\nWerkzeug == 3.0.1\naiohttp==3.9.1\n  NumPy >= 1.26  \nBabel\n",
                        expected_output=(
                            "Түгжсэн: 2\n  aiohttp==3.9.1\n  werkzeug==3.0.1\n"
                            "Түгжээгүй: 2\n  babel\n  numpy>=1.26\n"
                        ),
                    ),
                ),
                solution="""\
TEMDEGUUD = ["==", ">=", "<=", "~="]


def normchloh(ner: str) -> str:
    # pip "Flask" ба "flask", "a_b" ба "a-b"-г нэг багц гэж үздэг
    return ner.strip().lower().replace("_", "-")


def zadlah(mur: str) -> tuple[str, str, str]:
    # (нэр, тэмдэг, хувилбар) — тэмдэггүй бол сүүлийн хоёр нь хоосон
    for temdeg in TEMDEGUUD:
        if temdeg in mur:
            ner, huvilbar = mur.split(temdeg, 1)
            return normchloh(ner), temdeg, huvilbar.strip()
    return normchloh(mur), "", ""


n = int(input())
tugjsen = []
tugjeegui = []
for _ in range(n):
    mur = input().split("#")[0].strip()  # тайлбарыг хасна
    if not mur:
        continue
    ner, temdeg, huvilbar = zadlah(mur)
    bichleg = (ner, f"{ner}{temdeg}{huvilbar}")
    # Зөвхөн == нь хувилбарыг бүрэн түгжинэ — >= маргааш өөр хувилбар суулгаж болно
    if temdeg == "==":
        tugjsen.append(bichleg)
    else:
        tugjeegui.append(bichleg)

for garchig, jagsaalt in [("Түгжсэн", tugjsen), ("Түгжээгүй", tugjeegui)]:
    print(f"{garchig}: {len(jagsaalt)}")
    for _, bichleg in sorted(jagsaalt):  # tuple-ийн эхний утга — нэрээр
        print(f"  {bichleg}")
""",
                tips="""\
- `mur.split("#")[0]` нь тайлбарын өмнөх хэсгийг үлдээнэ — дараа нь `strip()`
  хийгээд хоосон эсэхийг шалга.
- `mur.split(temdeg, 1)` нь тэмдгийн хоёр талыг салгана; хоёр хэсгийг хоёуланг
  нь `strip()` хий.
- Нэрийг нормчилсны **дараа** эрэмбэл: `Flask`-ийн `F` том үсэг хэвээр бол
  жижиг үсэгтэй нэрсээс өмнө орчихно.
- `>=`, `~=` ч түгжээгүйд тооцогдоно — маргааш шинэ хувилбар суух боломжтой
  тул «миний машин дээр ажиллаж байсан» асуудал үүснэ.
""",
            ),
        ),
    ],
)

TESTING = ModuleSpec(
    title="Модул 22 — Тест бичих",
    description="Кодоо ажиллаж байгааг баталгаажуулах.",
    lessons=[
        LessonSpec(
            title="pytest -ийн үндэс",
            slug="pytest-undes",
            description="assert, тестийн бүтэц.",
            duration=480,
            language=PY,
            content="""\
Тест нь кодоо өөрчлөхөд юу ч эвдрээгүйг шалгах автомат арга.

```python
# tootsoolol.py
def nemeh(a, b):
    return a + b
```

```python
# test_tootsoolol.py
from tootsoolol import nemeh

def test_nemeh():
    assert nemeh(2, 3) == 5
```

```bash
pytest
```

### Дүрмүүд

| Юу | Дүрэм |
|---|---|
| Файлын нэр | `test_` -ээр эхэлнэ |
| Функцийн нэр | `test_` -ээр эхэлнэ |
| Шалгалт | `assert` |

### Захын тохиолдлыг шалга

```python
def test_hooson_jagsaalt():
    assert dundaj([]) == 0

def test_sorog_too():
    assert dundaj([-5, 5]) == 0
```

Алдаа ихэвчлэн **захын** тохиолдолд нуугддаг: хоосон, тэг, сөрөг, маш их.

### Алдаа гарахыг шалгах

```python
import pytest

def test_sorog_nas_aldaa():
    with pytest.raises(ValueError):
        nas_shalgah(-5)
```

### Сайн тестийн шинж

- Нэг тест нэг зүйл шалгана
- Нэр нь юу шалгаж буйг хэлнэ
- Бусад тестээс хамаарахгүй

Энэ платформ 51 backend тесттэй. Тэдгээр нь нэвтрэлт, эрх, ахиц зэргийг
өөрчлөлт бүрийн дараа шалгадаг.

### Жишээ програм

```python
# pytest нь тусдаа файлаас ажилладаг.
# Логикийг assert-ээр энд шалгаж үзье.


def dundaj(toonuud):
    if not toonuud:
        return 0
    return sum(toonuud) / len(toonuud)


def test_engiin():
    assert dundaj([2, 4, 6]) == 4


def test_hooson():
    assert dundaj([]) == 0


def test_neg_element():
    assert dundaj([5]) == 5


# Гараар ажиллуулж үзэх
for test in [test_engiin, test_hooson, test_neg_element]:
    try:
        test()
        print(f"PASS  {test.__name__}")
    except AssertionError:
        print(f"FAIL  {test.__name__}")
```
""",
            initial_code="""\
# Шалгагдаж буй код — ӨӨРЧЛӨХГҮЙ. Заримд нь алдаа нуугдсан.
def dundaj_a(toonuud):
    if not toonuud:
        return 0
    return sum(toonuud) / len(toonuud)


def dundaj_b(toonuud):
    return sum(toonuud) / len(toonuud)


def dundaj_c(toonuud):
    if not toonuud:
        return 0
    return sum(toonuud) // len(toonuud)


def dundaj_d(toonuud):
    if not toonuud:
        return 0
    return sorted(toonuud)[len(toonuud) // 2]


HEREGJUULELTUUD = [dundaj_a, dundaj_b, dundaj_c, dundaj_d]


def neg_test(funkts, toonuud, huleegdej_bui) -> bool:
    # TODO: assert funkts(toonuud) == huleegdej_bui
    #       Давбал True. AssertionError болон бусад ямар ч алдааг
    #       try/except-ээр барьж False буцаа — програм унах ёсгүй.
    return False


# Тохиолдлуудыг унших хэсэг бэлэн: [([2, 4, 6], 4.0), ([], 0.0), ...]
q = int(input())
tohioldluud = []
for _ in range(q):
    zuun, baruun = input().split("|")
    toonuud = [int(t) for t in zuun.split()]
    tohioldluud.append((toonuud, float(baruun)))

# TODO: HEREGJUULELTUUD-ийн функц бүрээр бүх тохиолдлыг neg_test-ээр шалгаж
#       «<нэр>: <P> passed, <F> failed» хэвлэ (нэр нь funkts.__name__)

# TODO: бүх тестийг давсан функцуудыг «Бүх тест давсан: ...» мөрөнд хэвлэ
""",
            exercise=ExerciseSpec(
                statement="""\
pytest нь `test_` функц бүрийг ажиллуулж, `assert` унавал — эсвэл тест
дотор ямар нэг алдаа гарвал — түүнийг **failed** гэж тэмдэглээд дараагийн
тест рүү үргэлжилдэг. Ийм жижиг «pytest»-ийг өөрөө бич.

Эхлэл кодод `dundaj` функцийн дөрвөн хэрэгжүүлэлт бий — заримд нь алдаа
нуугдсан. Оролтоос ирсэн тохиолдол бүрээр хэрэгжүүлэлт бүрийг шалгаж, аль
нь бүх тестийг давсныг ол. Хэрэгжүүлэлтүүдийг **өөрчлөхгүй**.

**Оролт:** эхний мөрөнд тохиолдлын тоо `q` (1 ≤ q ≤ 20). Дараагийн `q` мөр
бүрт `<тоонууд> | <хүлээгдэж буй>` — жишээ нь `2 4 6 | 4`. `|`-ийн зүүн тал
хоосон байж болно (хоосон жагсаалт). Хүлээгдэж буй утгыг `float` болгож
жишнэ — оролтыг уншдаг хэсэг эхлэл кодод бэлэн.

**Гаралт:** хэрэгжүүлэлт бүрт `dundaj_a`, `dundaj_b`, `dundaj_c`, `dundaj_d`
дарааллаар нэг мөр, сүүлд нь дүгнэлт:

```text
dundaj_a: <P> passed, <F> failed
...
Бүх тест давсан: <нэр>, <нэр>
```

Бүх тестийг давсан хэрэгжүүлэлт байхгүй бол `Бүх тест давсан: байхгүй`.
""",
                tests=(
                    TestCaseSpec(
                        stdin="3\n2 4 6 | 4\n1 2 | 1.5\n| 0\n",
                        expected_output=(
                            "dundaj_a: 3 passed, 0 failed\n"
                            "dundaj_b: 2 passed, 1 failed\n"
                            "dundaj_c: 2 passed, 1 failed\n"
                            "dundaj_d: 2 passed, 1 failed\n"
                            "Бүх тест давсан: dundaj_a\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="2\n5 | 5\n10 20 | 15\n",
                        expected_output=(
                            "dundaj_a: 2 passed, 0 failed\n"
                            "dundaj_b: 2 passed, 0 failed\n"
                            "dundaj_c: 2 passed, 0 failed\n"
                            "dundaj_d: 1 passed, 1 failed\n"
                            "Бүх тест давсан: dundaj_a, dundaj_b, dundaj_c\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="3\n-3 0 | -1.5\n-1 -2 -3 | -2\n7 | 7\n",
                        expected_output=(
                            "dundaj_a: 3 passed, 0 failed\n"
                            "dundaj_b: 3 passed, 0 failed\n"
                            "dundaj_c: 2 passed, 1 failed\n"
                            "dundaj_d: 2 passed, 1 failed\n"
                            "Бүх тест давсан: dundaj_a, dundaj_b\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="1\n1 1 | 2\n",
                        expected_output=(
                            "dundaj_a: 0 passed, 1 failed\n"
                            "dundaj_b: 0 passed, 1 failed\n"
                            "dundaj_c: 0 passed, 1 failed\n"
                            "dundaj_d: 0 passed, 1 failed\n"
                            "Бүх тест давсан: байхгүй\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="4\n1 2 3 4 | 2.5\n| 0\n100 | 100\n0 0 0 | 0\n",
                        expected_output=(
                            "dundaj_a: 4 passed, 0 failed\n"
                            "dundaj_b: 3 passed, 1 failed\n"
                            "dundaj_c: 3 passed, 1 failed\n"
                            "dundaj_d: 3 passed, 1 failed\n"
                            "Бүх тест давсан: dundaj_a\n"
                        ),
                    ),
                ),
                solution="""\
# Шалгагдаж буй код — өөрчлөхгүй
def dundaj_a(toonuud):
    if not toonuud:
        return 0
    return sum(toonuud) / len(toonuud)


def dundaj_b(toonuud):
    return sum(toonuud) / len(toonuud)


def dundaj_c(toonuud):
    if not toonuud:
        return 0
    return sum(toonuud) // len(toonuud)


def dundaj_d(toonuud):
    if not toonuud:
        return 0
    return sorted(toonuud)[len(toonuud) // 2]


HEREGJUULELTUUD = [dundaj_a, dundaj_b, dundaj_c, dundaj_d]


def neg_test(funkts, toonuud, huleegdej_bui) -> bool:
    try:
        assert funkts(toonuud) == huleegdej_bui
    except AssertionError:
        return False  # хариу буруу
    except Exception:
        return False  # тест дотор алдаа гарсан (ZeroDivisionError г.м.) — мөн failed
    return True


q = int(input())
tohioldluud = []
for _ in range(q):
    zuun, baruun = input().split("|")
    toonuud = [int(t) for t in zuun.split()]
    tohioldluud.append((toonuud, float(baruun)))

davsan = []
for funkts in HEREGJUULELTUUD:  # функц бол утга — жагсаалтаар давтаж болно
    passed = 0
    for toonuud, huleegdej_bui in tohioldluud:
        if neg_test(funkts, toonuud, huleegdej_bui):
            passed += 1
    failed = len(tohioldluud) - passed
    print(f"{funkts.__name__}: {passed} passed, {failed} failed")
    if failed == 0:
        davsan.append(funkts.__name__)

print("Бүх тест давсан: " + (", ".join(davsan) if davsan else "байхгүй"))
""",
                tips="""\
- `assert nohtsol` нь нөхцөл худал бол `AssertionError` үүсгэнэ.
  `try: ... except AssertionError:` нь pytest-ийн «failed»-ийг дуурайна.
- `dundaj_b([])` нь `ZeroDivisionError` өгнө — үүнийг ч барь, эс бөгөөс нэг
  муу тест бүх ажиллуулалтыг зогсооно. `except Exception:` энгийн бүх алдааг
  барина.
- Функц бол утга: `for funkts in HEREGJUULELTUUD:` гэж давтаад
  `funkts(toonuud)` гэж дуудна, нэрийг нь `funkts.__name__`-ээс авна.
- Жишээ 2-ыг анхаар: цөөн, хялбар тест алдаатай кодыг ч «давуулж» болно.
  Хоосон жагсаалт, бутархай дундаж, сөрөг тоо гэх мэт **захын** тохиолдол
  тестэд заавал байх ёстой.
""",
            ),
        ),
    ],
)

GIT = ModuleSpec(
    title="Модул 23 — Git",
    description="Кодын хувилбар хянах.",
    lessons=[
        LessonSpec(
            title="Git-ийн үндсэн урсгал",
            slug="git-undes",
            description="commit, branch, merge.",
            duration=480,
            language=PY,
            content="""\
Git нь кодын **өөрчлөлтийн түүх** хадгална. Буруу засвар хийвэл буцааж болно.

### Өдөр тутмын урсгал

```bash
git status                  # юу өөрчлөгдсөнийг харах
git add fail.py             # тодорхой файл нэмэх
git add .                   # бүгдийг
git commit -m "Тайлбар"     # түүхэнд бичих
```

### Сайн commit мессеж

```text
Хэрэглэгчийн нэвтрэлтэд хугацааны хязгаар нэмэв     ← САЙН
засвар                                              ← МУУ
```

Мессеж нь **юу өөрчилснийг** хэлэх ёстой. Хагас жилийн дараа өөрөө уншихад
хэрэгтэй болно.

### Салбар (branch)

```bash
git switch -c shine-bolomj    # шинэ салбар үүсгээд шилжих
# ... ажиллана, commit хийнэ ...
git switch main
git merge shine-bolomj
```

Салбар нь `main`-г тогтвортой байлгаж, шинэ ажлыг тусад нь хийх боломж өгнө.

### .gitignore

```text
.venv/
__pycache__/
.env
*.log
```

> `.env` файлыг **хэзээ ч** git-д оруулж болохгүй. Нууц үг, түлхүүр
> түүхэнд үлдэж, устгахад маш хэцүү болно.

### Түүхийг харах

```bash
git log --oneline
git diff
```

### Жишээ програм

```python
# Git нь тушаалын мөрний хэрэгсэл.

# Эхлэх
#   git init
#   git add .
#   git commit -m "Анхны commit"

# Өдөр тутам
#   git status
#   git add .
#   git commit -m "Юу өөрчилснөө тодорхой бич"

# Салбар
#   git switch -c shine-bolomj
#   git switch main
#   git merge shine-bolomj

# Түүх
#   git log --oneline
#   git diff

# .gitignore дотор заавал байх ёстой зүйлс:
gitignore_murnuud = [
    ".venv/",
    "__pycache__/",
    ".env",
    "*.log",
]

print(".gitignore:")
for mur in gitignore_murnuud:
    print(" ", mur)
```
""",
            initial_code="""\
# Бодит ажил дээр: git status --porcelain
# Энд түүний гаралтыг оролтоос уншиж хураангуйлна.

n = int(input())
staged = []  # (зам, төлөв)
unstaged = []  # (зам, төлөв)
untracked = []  # зам
for _ in range(n):
    mur = input()
    tolov = mur[:2]  # эхний хоёр тэмдэгт
    zam = mur[3:]  # зайны дараах зам
    # TODO: "??" бол untracked-д нэм
    # TODO: tolov[0] зай биш бол staged-д, tolov[1] зай биш бол unstaged-д нэм

# TODO: n == 0 бол «Ажлын хавтас цэвэр»
# TODO: үгүй бол гурван хэсгийг тоотой нь, мөрүүдийг замаар эрэмбэлж хэвлэ
# TODO: staged доторх .env файл бүрт «АНХААР: ...» мөр хэвлэ
""",
            exercise=ExerciseSpec(
                statement="""\
`git status --porcelain` нь өөрчлөлт бүрийг машинд уншигдах товч мөрөөр
гаргадаг: эхний хоёр тэмдэгт нь төлөв, дараа нь нэг зай, дараа нь файлын
зам.

- 1-р тэмдэгт — **staged** төлөв (`git add` хийгдсэн, commit-д орно): `M`
  өөрчилсөн, `A` нэмсэн, `D` устгасан, зай бол staged өөрчлөлтгүй.
- 2-р тэмдэгт — **add хийгээгүй** өөрчлөлт: `M`, `D`, эсвэл зай.
- `??` — git хянадаггүй шинэ файл.

`MM config.py` гэвэл нэг файл эхний хоёр хэсэгт хоёуланд нь орно. Энэ
гаралтыг уншиж `git status` шиг хураангуй хэвлэ.

**Оролт:** эхний мөрөнд мөрийн тоо `n` (0 ≤ n ≤ 30), дараагийн `n` мөр нь
porcelain мөрүүд. Зам нь зайгүй.

**Гаралт:** `n = 0` бол ганц мөр `Ажлын хавтас цэвэр`. Үгүй бол:

```text
Commit-д бэлэн: <тоо>
  <төлөв> <зам>
Add хийгээгүй: <тоо>
  <төлөв> <зам>
Хянагдаагүй: <тоо>
  <зам>
```

Хэсэг бүрийн мөрүүдийг замаар нь эрэмбэлнэ (`sorted`). Хамгийн төгсгөлд
staged хэсэгт байгаа `.env` нэртэй файл бүрт (ямар ч хавтас дотор байсан)
`АНХААР: .env файлыг commit хийх гэж байна (<зам>)` гэж хэвлэнэ.
""",
                tests=(
                    TestCaseSpec(
                        stdin="4\nM  app/main.py\n M README.md\nA  app/new.py\n?? notes.txt\n",
                        expected_output=(
                            "Commit-д бэлэн: 2\n  M app/main.py\n  A app/new.py\n"
                            "Add хийгээгүй: 1\n  M README.md\n"
                            "Хянагдаагүй: 1\n  notes.txt\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="3\nMM config.py\nA  .env\n?? .venv/\n",
                        expected_output=(
                            "Commit-д бэлэн: 2\n  A .env\n  M config.py\n"
                            "Add хийгээгүй: 1\n  M config.py\n"
                            "Хянагдаагүй: 1\n  .venv/\n"
                            "АНХААР: .env файлыг commit хийх гэж байна (.env)\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(stdin="0\n", expected_output="Ажлын хавтас цэвэр\n"),
                    TestCaseSpec(
                        stdin=(
                            "5\n D old.py\nD  legacy/util.py\n M src/app.py\nA  backend/.env\n"
                            "M  backend/.env.example\n"
                        ),
                        expected_output=(
                            "Commit-д бэлэн: 3\n  A backend/.env\n  M backend/.env.example\n"
                            "  D legacy/util.py\n"
                            "Add хийгээгүй: 2\n  D old.py\n  M src/app.py\n"
                            "Хянагдаагүй: 0\n"
                            "АНХААР: .env файлыг commit хийх гэж байна (backend/.env)\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="3\n?? zeta.txt\n?? Alpha.md\n?? docs/\n",
                        expected_output=(
                            "Commit-д бэлэн: 0\nAdd хийгээгүй: 0\n"
                            "Хянагдаагүй: 3\n  Alpha.md\n  docs/\n  zeta.txt\n"
                        ),
                    ),
                ),
                solution="""\
n = int(input())
staged = []
unstaged = []
untracked = []
for _ in range(n):
    mur = input()  # strip() хийхгүй — эхний зай нь утгатай
    tolov = mur[:2]
    zam = mur[3:]
    if tolov == "??":
        untracked.append(zam)
        continue
    # 1-р тэмдэгт — staged (index), 2-р тэмдэгт — ажлын хавтас. Хоёулаа байж болно.
    if tolov[0] != " ":
        staged.append((zam, tolov[0]))
    if tolov[1] != " ":
        unstaged.append((zam, tolov[1]))

if n == 0:
    print("Ажлын хавтас цэвэр")
else:
    print(f"Commit-д бэлэн: {len(staged)}")
    for zam, temdeg in sorted(staged):  # tuple-ийн эхний утга — замаар
        print(f"  {temdeg} {zam}")
    print(f"Add хийгээгүй: {len(unstaged)}")
    for zam, temdeg in sorted(unstaged):
        print(f"  {temdeg} {zam}")
    print(f"Хянагдаагүй: {len(untracked)}")
    for zam in sorted(untracked):
        print(f"  {zam}")
    # .env нь нууц үг агуулдаг — ямар ч хавтас дотор байсан commit-д орох ёсгүй
    for zam, _ in sorted(staged):
        if zam.split("/")[-1] == ".env":
            print(f"АНХААР: .env файлыг commit хийх гэж байна ({zam})")
""",
                tips="""\
- Мөрийн эхний зай утгатай: `" M README.md"` ба `"M  README.md"` өөр. Мөрийг
  `strip()` хийвэл энэ мэдээлэл алдагдана — `mur[:2]`, `mur[3:]`-ээр зүс.
- Нэг файл хоёр хэсэгт зэрэг орж болно (`MM`) — `if/elif` биш, хоёр тусдаа
  `if` хэрэглэ.
- `(зам, төлөв)` tuple-ийн жагсаалтыг `sorted()` хийхэд замаар эрэмбэлэгдэнэ.
  Том үсэг жижгээсээ өмнө ордог (`README.md` < `app.py`).
- Файлын нэрийг `zam.split("/")[-1]`-ээр ав: `backend/.env` мөн нууц файл,
  харин `.env.example` биш.
""",
            ),
        ),
    ],
)

HTTP_APIS = ModuleSpec(
    title="Модул 24 — HTTP ба API",
    description="Интернэтээс өгөгдөл авах.",
    lessons=[
        LessonSpec(
            title="requests-ээр API дуудах",
            slug="requests-api",
            description="GET, POST, статус код.",
            duration=480,
            language=PY,
            content="""\
```python
import requests

hariu = requests.get("https://api.example.com/oyutnuud")
print(hariu.status_code)
data = hariu.json()
```

### Статус кодууд

| Код | Утга |
|---|---|
| 200 | Амжилттай |
| 201 | Үүсгэлээ |
| 400 | Хүсэлт буруу |
| 401 | Нэвтрээгүй |
| 403 | Эрхгүй |
| 404 | Олдсонгүй |
| 500 | Серверийн алдаа |

Энэ платформын API яг эдгээрийг ашигладаг.

### Алдааг шалгах

```python
hariu = requests.get(url, timeout=10)
hariu.raise_for_status()      # 4xx/5xx бол алдаа үүсгэнэ
```

> `timeout` -г **үргэлж** заа. Эс бөгөөс сервер хариу өгөхгүй бол таны
> програм мөнхөд хүлээнэ.

### POST хүсэлт

```python
hariu = requests.post(
    "https://api.example.com/oyutnuud",
    json={"ner": "Бат", "nas": 20},
    timeout=10,
)
```

### Түлхүүрийг кодонд бичихгүй

```python
import os
tulhuur = os.environ["API_TULHUUR"]      # ЗӨВ

tulhuur = "sk-12345"                      # БУРУУ — git-д орно
```

### Алдаанаас хамгаалах

```python
try:
    hariu = requests.get(url, timeout=10)
    hariu.raise_for_status()
except requests.Timeout:
    print("Хугацаа хэтэрлээ")
except requests.RequestException as aldaa:
    print("Сүлжээний алдаа:", aldaa)
```

### Жишээ програм

```python
# requests нь гадны сан бөгөөд сүлжээ шаардана.
# Дуудалтын бүтцийг харуулав.

# import os
# import requests

# hariu = requests.get(
#     "https://api.example.com/oyutnuud",
#     headers={"Authorization": f"Bearer {os.environ['API_TULHUUR']}"},
#     timeout=10,
# )
# hariu.raise_for_status()
# oyutnuud = hariu.json()

# API-аас ирсэн өгөгдлийг боловсруулах логик:
import json

hariu_mur = '{"oyutnuud": [{"ner": "Бат", "dun": 85}, {"ner": "Цэцэг", "dun": 95}]}'
data = json.loads(hariu_mur)

for oyutan in data["oyutnuud"]:
    print(f"{oyutan['ner']}: {oyutan['dun']}")

dundaj = sum(o["dun"] for o in data["oyutnuud"]) / len(data["oyutnuud"])
print(f"Дундаж: {dundaj:.1f}")
```
""",
            initial_code="""\
import json


class Hariu:
    # requests-ийн хариуг дуурайсан жижиг класс — бэлэн
    def __init__(self, status_code: int, text: str) -> None:
        self.status_code = status_code
        self.text = text

    def json(self):
        # Жинхэнэ requests-тэй адил: JSON биш бол ValueError үүсгэнэ
        return json.loads(self.text)


def bolovsruulah(hariu: Hariu) -> tuple[str, bool]:
    # Буцаах утга: (хэвлэх мөр, амжилттай эсэх)
    # TODO: 404, бусад 4xx, 5xx статусыг эхлээд шалга
    # TODO: 200 бол hariu.json()-ийг try/except ValueError-оор уншиж үз
    # TODO: "hot", "temp" байгаа эсэхийг шалгаж, data.get("tolov", ...) ашигла
    return f"TODO {hariu.status_code}", False


# Доорх хэсэг бэлэн.
n = int(input())
amjilttai = 0
for _ in range(n):
    kod = int(input())
    bie = input()
    mur, amjilt = bolovsruulah(Hariu(kod, bie))
    print(mur)
    if amjilt:
        amjilttai += 1
print(f"Амжилттай: {amjilttai}/{n}")
""",
            exercise=ExerciseSpec(
                statement="""\
Бодит ажил дээр `hariu = requests.get(url, timeout=10)` гэж дуудаад
`hariu.status_code`, `hariu.json()`-ийг ашигладаг. Энд сүлжээ байхгүй тул
цаг агаарын API-ийн хариуг оролтоос уншина. Эхлэл кодын `Hariu` класс нь
`requests`-ийн хариуг дуурайна: `status_code`, `text`, `json()` — `json()`
нь JSON биш текст дээр `ValueError` үүсгэнэ.

Хариу бүрийг `bolovsruulah(hariu)` функцээр нэг мөр болгоно:

- `200`, JSON нь `hot` ба `temp` талбартай → `<hot>: <temp>°C, <tolov>` —
  `temp` нэг оронтой (`.1f`), `tolov` байхгүй бол `тодорхойгүй`.
- `200` боловч JSON биш → `Буруу JSON`.
- `200`, JSON боловч `hot` эсвэл `temp` дутуу → `Дутуу өгөгдөл`.
- `404` → `Олдсонгүй`.
- Бусад `4xx` → `Хүсэлтийн алдаа <код>`.
- `5xx` → `Серверийн алдаа <код>`.

Функц `(мөр, амжилттай эсэх)` буцаана — зөвхөн эхний дүрэм амжилттай.
Оролт уншиж хэвлэх хэсэг эхлэл кодод бэлэн.

**Оролт:** эхний мөрөнд хариуны тоо `n` (1 ≤ n ≤ 10). Хариу бүр хоёр мөр:
статус код, дараа нь хариуны бие (нэг мөр текст).

**Гаралт:** хариу бүрт нэг мөр, сүүлд нь `Амжилттай: <k>/<n>`.
""",
                tests=(
                    TestCaseSpec(
                        stdin=(
                            "3\n"
                            '200\n{"hot": "Улаанбаатар", "temp": -12.5, "tolov": "цастай"}\n'
                            '404\n{"error": "not found"}\n'
                            '200\n{"hot": "Дархан", "temp": 3}\n'
                        ),
                        expected_output=(
                            "Улаанбаатар: -12.5°C, цастай\nОлдсонгүй\n"
                            "Дархан: 3.0°C, тодорхойгүй\nАмжилттай: 2/3\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="2\n503\nService Unavailable\n200\n<html>Алдаа</html>\n",
                        expected_output="Серверийн алдаа 503\nБуруу JSON\nАмжилттай: 0/2\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin=(
                            "4\n"
                            '401\n{"error": "unauthorized"}\n'
                            '429\n{"error": "too many requests"}\n'
                            '200\n{"hot": "Эрдэнэт", "tolov": "бороотой"}\n'
                            "500\n{}\n"
                        ),
                        expected_output=(
                            "Хүсэлтийн алдаа 401\nХүсэлтийн алдаа 429\nДутуу өгөгдөл\n"
                            "Серверийн алдаа 500\nАмжилттай: 0/4\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin=(
                            "2\n"
                            '200\n{"temp": 25.34, "hot": "Ховд", "tolov": "нартай", "salhi": 5}\n'
                            '200\n{"hot": "Мөрөн", "temp": 0}\n'
                        ),
                        expected_output=(
                            "Ховд: 25.3°C, нартай\nМөрөн: 0.0°C, тодорхойгүй\nАмжилттай: 2/2\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="2\n200\n[]\n404\nNot Found\n",
                        expected_output="Дутуу өгөгдөл\nОлдсонгүй\nАмжилттай: 0/2\n",
                    ),
                ),
                solution="""\
import json


class Hariu:
    # requests-ийн хариуг дуурайсан жижиг класс
    def __init__(self, status_code: int, text: str) -> None:
        self.status_code = status_code
        self.text = text

    def json(self):
        return json.loads(self.text)


def bolovsruulah(hariu: Hariu) -> tuple[str, bool]:
    kod = hariu.status_code
    # 404-ийг бусад 4xx-ээс ӨМНӨ шалгана
    if kod == 404:
        return "Олдсонгүй", False
    if 400 <= kod < 500:
        return f"Хүсэлтийн алдаа {kod}", False
    if kod >= 500:
        return f"Серверийн алдаа {kod}", False

    try:
        data = hariu.json()
    except ValueError:  # json.JSONDecodeError нь ValueError-ийн дэд класс
        return "Буруу JSON", False

    # "in" шалгалт — temp нь 0 байсан ч зөв ажиллана
    if "hot" not in data or "temp" not in data:
        return "Дутуу өгөгдөл", False
    tolov = data.get("tolov", "тодорхойгүй")
    return f"{data['hot']}: {data['temp']:.1f}°C, {tolov}", True


n = int(input())
amjilttai = 0
for _ in range(n):
    kod = int(input())
    bie = input()
    mur, amjilt = bolovsruulah(Hariu(kod, bie))
    print(mur)
    if amjilt:
        amjilttai += 1
print(f"Амжилттай: {amjilttai}/{n}")
""",
                tips="""\
- Статус кодыг эхлээд шалга. `404`-ийг «бусад 4xx»-ээс **өмнө** шалгахгүй бол
  `Хүсэлтийн алдаа 404` гэж гарна.
- `hariu.json()` нь JSON биш текст дээр `json.JSONDecodeError` үүсгэнэ — энэ
  нь `ValueError`-ийн дэд класс тул `except ValueError:` барина. Жинхэнэ
  `requests` ч ижил.
- Байхгүй байж болох талбарыг `data.get("tolov", "тодорхойгүй")`-ээр ав.
  Харин `if not data.get("temp")` гэвэл `0` градус «дутуу» болно — `"temp" in
  data` ашигла.
- `f"{temp:.1f}"` нь бүхэл `3`-ыг ч `3.0` болгоно.
""",
            ),
        ),
    ],
)

SQL = ModuleSpec(
    title="Модул 25 — SQL ба өгөгдлийн сан",
    description="Өгөгдлийг байнга хадгалах.",
    lessons=[
        LessonSpec(
            title="SQL-ийн үндэс",
            slug="sql-undes",
            description="SELECT, INSERT, UPDATE, DELETE.",
            duration=480,
            language=PY,
            content="""\
Файл нь жижиг өгөгдөлд тохирно. Хэдэн мянган мөр болоход өгөгдлийн сан хэрэгтэй.

### Хүснэгт үүсгэх

```sql
CREATE TABLE oyutnuud (
    id INTEGER PRIMARY KEY,
    ner TEXT NOT NULL,
    nas INTEGER
);
```

### Үндсэн дөрвөн үйлдэл

```sql
INSERT INTO oyutnuud (ner, nas) VALUES ('Бат', 20);

SELECT * FROM oyutnuud;
SELECT ner FROM oyutnuud WHERE nas > 18 ORDER BY ner;

UPDATE oyutnuud SET nas = 21 WHERE ner = 'Бат';

DELETE FROM oyutnuud WHERE id = 1;
```

> `UPDATE` болон `DELETE` дээр `WHERE` бичихээ мартвал **бүх мөр** өөрчлөгдөнө.

### Python-оос ашиглах

```python
import sqlite3

holbolt = sqlite3.connect("surgalt.db")
kursor = holbolt.cursor()

kursor.execute("SELECT * FROM oyutnuud WHERE nas > ?", (18,))
```

### SQL injection — хамгийн чухал дүрэм

```python
# АЮУЛТАЙ — хэзээ ч ингэж бичиж болохгүй
kursor.execute(f"SELECT * FROM oyutnuud WHERE ner = '{ner}'")

# АЮУЛГҮЙ — параметр ашиглана
kursor.execute("SELECT * FROM oyutnuud WHERE ner = ?", (ner,))
```

Эхнийх дээр хэрэглэгч `'; DROP TABLE oyutnuud; --` гэж бичвэл хүснэгт устана.
Параметр ашиглавал утга нь зөвхөн **утга** хэвээр үлдэнэ.

### Жишээ програм

```python
import sqlite3

# Санах ойд түр сан үүсгэв
holbolt = sqlite3.connect(":memory:")
kursor = holbolt.cursor()

kursor.execute(\"\"\"
    CREATE TABLE oyutnuud (
        id INTEGER PRIMARY KEY,
        ner TEXT NOT NULL,
        dun INTEGER
    )
\"\"\")

# Параметртэй оруулалт — SQL injection-оос хамгаална
oyutnuud = [("Бат", 85), ("Цэцэг", 95), ("Болд", 72)]
kursor.executemany("INSERT INTO oyutnuud (ner, dun) VALUES (?, ?)", oyutnuud)
holbolt.commit()

# Унших
kursor.execute("SELECT ner, dun FROM oyutnuud WHERE dun > ? ORDER BY dun DESC", (80,))
for ner, dun in kursor.fetchall():
    print(f"{ner}: {dun}")

holbolt.close()
```
""",
            initial_code="""\
import sqlite3

holbolt = sqlite3.connect(":memory:")
kursor = holbolt.cursor()
kursor.execute(
    "CREATE TABLE suragchid (id INTEGER PRIMARY KEY, ner TEXT NOT NULL, dun INTEGER)"
)

n = int(input())
for _ in range(n):
    hesguud = input().split()
    komand = hesguud[0]
    if komand == "nemeh":
        # TODO: INSERT INTO suragchid (ner, dun) VALUES (?, ?)
        pass
    elif komand == "zasah":
        # TODO: UPDATE suragchid SET dun = ? WHERE ner = ?
        #       kursor.rowcount == 0 бол «Олдсонгүй: <нэр>»
        pass
    elif komand == "ustgah":
        # TODO: DELETE FROM suragchid WHERE ner = ?  (rowcount-г мөн шалга)
        pass
    elif komand == "harah":
        # TODO: SELECT ner, dun ... WHERE dun >= ? ORDER BY dun DESC, ner
        #       «>= <босго>: <тоо> сурагч», дараа нь мөр бүрт «  <нэр> <дүн>»
        pass

holbolt.close()
""",
            exercise=ExerciseSpec(
                statement="""\
Сурагчдын дүнг SQLite өгөгдлийн санд хадгалж, SQL-ийн дөрвөн үндсэн
үйлдлийг гүйцэтгэнэ. Сан санах ойд үүснэ (`sqlite3.connect(":memory:")`),
`suragchid` хүснэгт (`id`, `ner`, `dun`) эхлэл кодод бэлэн.

Командууд:

- `nemeh <нэр> <дүн>` — `INSERT`.
- `zasah <нэр> <дүн>` — `UPDATE`; ийм нэр байхгүй бол `Олдсонгүй: <нэр>`.
- `ustgah <нэр>` — `DELETE`; ийм нэр байхгүй бол `Олдсонгүй: <нэр>`.
- `harah <босго>` — `SELECT`: дүн ≥ босго сурагчид, дүнгээр буурах, тэнцвэл
  нэрээр. Эхлээд `>= <босго>: <тоо> сурагч`, дараа нь мөр бүрт
  `  <нэр> <дүн>` (хоёр зайгаар эхэлнэ).

Утгыг SQL мөрөнд f-string-ээр **бүү** оруул — `?` параметр ашигла. Нэрэнд
`'` тэмдэгт ч орж болно!

**Оролт:** эхний мөрөнд командын тоо `n` (1 ≤ n ≤ 30), дараагийн `n` мөрөнд
команд. Нэр нь зайгүй, санд давхардахгүй.

**Гаралт:** зөвхөн `harah`-ийн үр дүн ба `Олдсонгүй` мөрүүд.

Зөвлөгөө: `UPDATE`, `DELETE`-ийн дараа `kursor.rowcount` нь өөрчлөгдсөн
мөрийн тоог хэлнэ.
""",
                tests=(
                    TestCaseSpec(
                        stdin=(
                            "6\nnemeh Бат 85\nnemeh Цэцэг 95\nnemeh Болд 72\nharah 80\n"
                            "zasah Болд 88\nharah 80\n"
                        ),
                        expected_output=(
                            ">= 80: 2 сурагч\n  Цэцэг 95\n  Бат 85\n"
                            ">= 80: 3 сурагч\n  Цэцэг 95\n  Болд 88\n  Бат 85\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin=(
                            "5\nnemeh Дорж 60\nnemeh Сараа 59\nustgah Сараа\nustgah Сараа\n"
                            "harah 0\n"
                        ),
                        expected_output="Олдсонгүй: Сараа\n>= 0: 1 сурагч\n  Дорж 60\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin=(
                            "6\nnemeh О'Нил 77\nnemeh Ану 77\nnemeh Батаа 90\nzasah Хулан 50\n"
                            "harah 77\nharah 91\n"
                        ),
                        expected_output=(
                            "Олдсонгүй: Хулан\n"
                            ">= 77: 3 сурагч\n  Батаа 90\n  Ану 77\n  О'Нил 77\n"
                            ">= 91: 0 сурагч\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="4\nnemeh Мөнх 40\nzasah Мөнх 100\nustgah Мөнх\nharah 0\n",
                        expected_output=">= 0: 0 сурагч\n",
                    ),
                    TestCaseSpec(
                        stdin="2\nharah 50\nustgah Бат\n",
                        expected_output=">= 50: 0 сурагч\nОлдсонгүй: Бат\n",
                    ),
                ),
                solution="""\
import sqlite3

holbolt = sqlite3.connect(":memory:")
kursor = holbolt.cursor()
kursor.execute(
    "CREATE TABLE suragchid (id INTEGER PRIMARY KEY, ner TEXT NOT NULL, dun INTEGER)"
)

n = int(input())
for _ in range(n):
    hesguud = input().split()
    komand = hesguud[0]
    if komand == "nemeh":
        # ? параметр — нэрэнд ' байсан ч SQL эвдрэхгүй, утга нь утга хэвээр
        kursor.execute(
            "INSERT INTO suragchid (ner, dun) VALUES (?, ?)", (hesguud[1], int(hesguud[2]))
        )
    elif komand == "zasah":
        kursor.execute(
            "UPDATE suragchid SET dun = ? WHERE ner = ?", (int(hesguud[2]), hesguud[1])
        )
        if kursor.rowcount == 0:  # нэг ч мөр өөрчлөгдөөгүй — ийм сурагч алга
            print(f"Олдсонгүй: {hesguud[1]}")
    elif komand == "ustgah":
        kursor.execute("DELETE FROM suragchid WHERE ner = ?", (hesguud[1],))
        if kursor.rowcount == 0:
            print(f"Олдсонгүй: {hesguud[1]}")
    elif komand == "harah":
        bosgo = int(hesguud[1])
        kursor.execute(
            "SELECT ner, dun FROM suragchid WHERE dun >= ? ORDER BY dun DESC, ner",
            (bosgo,),
        )
        murnuud = kursor.fetchall()
        print(f">= {bosgo}: {len(murnuud)} сурагч")
        for ner, dun in murnuud:
            print(f"  {ner} {dun}")

holbolt.commit()
holbolt.close()
""",
                tips="""\
- Параметрийг tuple-ээр дамжуул: `kursor.execute("... WHERE ner = ?", (ner,))`
  — ганц утгатай tuple-д таслал заавал хэрэгтэй.
- `f"... WHERE ner = '{ner}'"` гэвэл `'` агуулсан нэр SQL-ийг эвдэнэ — SQL
  injection яг эндээс үүсдэг. `?` параметр үүнээс бүрэн хамгаална.
- Хоёр баганаар эрэмбэлэх: `ORDER BY dun DESC, ner` — эхлээд дүнгээр буурах,
  тэнцвэл нэрээр өсөх.
- `UPDATE`/`DELETE`-ийн дараа `kursor.rowcount` нь хэдэн мөр өөрчлөгдсөнийг
  хэлнэ: `0` бол ийм сурагч байхгүй. `SELECT`-ийн үр дүнг `fetchall()`-ээр
  жагсаалт болгож ав.
""",
            ),
        ),
    ],
)

SQLALCHEMY = ModuleSpec(
    title="Модул 26 — SQLAlchemy",
    description="Python объектоор өгөгдлийн сан удирдах.",
    lessons=[
        LessonSpec(
            title="ORM-ийн үндэс",
            slug="sqlalchemy-undes",
            description="Model, session, query.",
            duration=480,
            language=PY,
            content="""\
ORM (Object Relational Mapper) нь хүснэгтийг Python класс болгон харуулна.
SQL бичихийн оронд объекттой ажиллана.

### Model тодорхойлох

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Oyutan(Base):
    __tablename__ = "oyutnuud"

    id: Mapped[int] = mapped_column(primary_key=True)
    ner: Mapped[str] = mapped_column(String(120))
    dun: Mapped[int]
```

### Ашиглах

```python
with Session(engine) as session:
    bat = Oyutan(ner="Бат", dun=85)
    session.add(bat)
    session.commit()

    onts = session.scalars(
        select(Oyutan).where(Oyutan.dun > 80)
    ).all()
```

### Давуу тал

| SQL гараар | ORM-оор |
|---|---|
| Мөр бичнэ | Python объект |
| Injection-оос өөрөө болгоомжилно | Автоматаар хамгаална |
| Санг солиход дахин бичнэ | Ихэвчлэн ижил хэвээр |

### N+1 асуудал

```python
# МУУ — сургалт бүрт нэмэлт query явна
for surgalt in surgaltuud:
    print(surgalt.hicheeluud)

# САЙН — нэг удаа хамт ачаална
select(Surgalt).options(selectinload(Surgalt.hicheeluud))
```

Энэ бол ORM-ийн хамгийн түгээмэл гүйцэтгэлийн алдаа. Энэ платформын
backend `selectinload` ашиглан үүнээс зайлсхийсэн.

### Migration

Схем өөрчлөгдөхөд **Alembic** ашиглан хувилбар үүсгэнэ:

```bash
alembic revision --autogenerate -m "shine talbar"
alembic upgrade head
```

### Жишээ програм

```python
# SQLAlchemy нь гадны сан. Бүтцийг харуулав.

# from sqlalchemy import String, select
# from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

# class Base(DeclarativeBase):
#     pass

# class Oyutan(Base):
#     __tablename__ = "oyutnuud"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     ner: Mapped[str] = mapped_column(String(120))
#     dun: Mapped[int]

# with Session(engine) as session:
#     session.add(Oyutan(ner="Бат", dun=85))
#     session.commit()
#
#     onts = session.scalars(select(Oyutan).where(Oyutan.dun > 80)).all()

# Энэ платформын жинхэнэ model-ийн бүтэц:
model_talbaruud = {
    "courses": ["id", "title", "slug", "difficulty", "published"],
    "modules": ["id", "course_id", "title", "position"],
    "lessons": ["id", "module_id", "title", "slug", "content", "published"],
}

for hus, talbaruud in model_talbaruud.items():
    print(f"{hus}: {', '.join(talbaruud)}")
```
""",
            initial_code="""\
import sqlite3
from dataclasses import dataclass


@dataclass
class Oyutan:
    ner: str
    dun: int
    id: int | None = None  # сан руу хадгалсны дараа л id-тэй болно


class OyutanRepo:
    # SQL зөвхөн энэ класс дотор — бусад код Oyutan объекттой л ажиллана
    def __init__(self, holbolt: sqlite3.Connection) -> None:
        self.holbolt = holbolt
        self.holbolt.execute(
            "CREATE TABLE oyutnuud (id INTEGER PRIMARY KEY, ner TEXT NOT NULL, dun INTEGER)"
        )

    def nemeh(self, oyutan: Oyutan) -> Oyutan:
        # TODO: INSERT хийж, kursor.lastrowid-г oyutan.id-д оноогоод буцаа
        return oyutan

    def avah(self, oyutan_id: int) -> Oyutan | None:
        # TODO: SELECT id, ner, dun ... WHERE id = ? — мөр олдвол Oyutan болгож
        #       буцаа, олдохгүй бол None
        return None

    def shuuh(self, dood_dun: int) -> list[Oyutan]:
        # TODO: dun >= dood_dun, дүнгээр буурах, тэнцвэл id-ээр өсөх.
        #       Мөр бүрийг Oyutan объект болго.
        return []

    def ustgah(self, oyutan_id: int) -> bool:
        # TODO: DELETE ... WHERE id = ? — устгасан бол True (kursor.rowcount)
        return False


# Доорх хэсэг бэлэн — зөвхөн объекттой ажиллана, SQL огт харагдахгүй.
repo = OyutanRepo(sqlite3.connect(":memory:"))
n = int(input())
for _ in range(n):
    hesguud = input().split()
    komand = hesguud[0]
    if komand == "nemeh":
        oyutan = repo.nemeh(Oyutan(hesguud[1], int(hesguud[2])))
        print(f"Нэмэгдлээ: {oyutan}")
    elif komand == "avah":
        oyutan = repo.avah(int(hesguud[1]))
        print(oyutan if oyutan is not None else f"Олдсонгүй: {hesguud[1]}")
    elif komand == "shuuh":
        oldson = repo.shuuh(int(hesguud[1]))
        if not oldson:
            print("Хоосон")
        for oyutan in oldson:
            print(oyutan)
    elif komand == "ustgah":
        oyutan_id = int(hesguud[1])
        if repo.ustgah(oyutan_id):
            print(f"Устгалаа: {oyutan_id}")
        else:
            print(f"Олдсонгүй: {oyutan_id}")
""",
            exercise=ExerciseSpec(
                statement="""\
ORM-ийн гол санаа: SQL-ийг нэг газар нууж, бусад код зөвхөн Python
**объекттой** ажиллана. SQLAlchemy-д `session.add(oyutan)`,
`session.get(Oyutan, 1)`, `select(Oyutan).where(...)` гэж бичдэг. Хөтөчид
SQLAlchemy байхгүй тул тэр санааг `sqlite3` + `dataclass`-аар өөрөө
хэрэгжүүлье.

`Oyutan` dataclass ба командын давталт эхлэл кодод бэлэн. `OyutanRepo`
классын аргуудыг гүйцээ — тус бүр объектыг SQL мөр, SQL мөрийг объект
болгож хөрвүүлнэ:

- `nemeh(oyutan)` — `INSERT` хийж, сангийн өгсөн `id`-г (`kursor.lastrowid`)
  объектод оноогоод буцаана.
- `avah(oyutan_id)` — `Oyutan`, эсвэл олдохгүй бол `None`.
- `shuuh(dood_dun)` — дүн ≥ `dood_dun` оюутнуудын жагсаалт: дүнгээр буурах,
  тэнцвэл `id`-ээр өсөх.
- `ustgah(oyutan_id)` — устгасан бол `True`, ийм мөр байхгүй бол `False`.

**Оролт:** эхний мөрөнд командын тоо `n` (1 ≤ n ≤ 30), дараагийн `n` мөрөнд
`nemeh <нэр> <дүн>`, `avah <id>`, `shuuh <дүн>`, `ustgah <id>`-ийн аль нэг.

**Гаралт:** эхлэл кодын давталт хэвлэнэ, жишээ нь
`Нэмэгдлээ: Oyutan(ner='Бат', dun=85, id=1)`. Объектыг dataclass-ийн `repr`
хэлбэрээр хэвлэдэг тул талбаруудыг зөв бөглөсөн л бол гаралт зөв гарна.
""",
                tests=(
                    TestCaseSpec(
                        stdin="5\nnemeh Бат 85\nnemeh Цэцэг 95\navah 2\navah 7\nshuuh 80\n",
                        expected_output=(
                            "Нэмэгдлээ: Oyutan(ner='Бат', dun=85, id=1)\n"
                            "Нэмэгдлээ: Oyutan(ner='Цэцэг', dun=95, id=2)\n"
                            "Oyutan(ner='Цэцэг', dun=95, id=2)\n"
                            "Олдсонгүй: 7\n"
                            "Oyutan(ner='Цэцэг', dun=95, id=2)\n"
                            "Oyutan(ner='Бат', dun=85, id=1)\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="4\nnemeh Болд 70\nustgah 1\nustgah 1\nshuuh 0\n",
                        expected_output=(
                            "Нэмэгдлээ: Oyutan(ner='Болд', dun=70, id=1)\n"
                            "Устгалаа: 1\nОлдсонгүй: 1\nХоосон\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin=(
                            "6\nnemeh А 50\nnemeh Б 90\nnemeh В 90\nustgah 1\nnemeh Г 100\n"
                            "shuuh 90\n"
                        ),
                        expected_output=(
                            "Нэмэгдлээ: Oyutan(ner='А', dun=50, id=1)\n"
                            "Нэмэгдлээ: Oyutan(ner='Б', dun=90, id=2)\n"
                            "Нэмэгдлээ: Oyutan(ner='В', dun=90, id=3)\n"
                            "Устгалаа: 1\n"
                            "Нэмэгдлээ: Oyutan(ner='Г', dun=100, id=4)\n"
                            "Oyutan(ner='Г', dun=100, id=4)\n"
                            "Oyutan(ner='Б', dun=90, id=2)\n"
                            "Oyutan(ner='В', dun=90, id=3)\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="4\nnemeh О'Нил 60\navah 1\nustgah 1\navah 1\n",
                        expected_output=(
                            'Нэмэгдлээ: Oyutan(ner="О\'Нил", dun=60, id=1)\n'
                            'Oyutan(ner="О\'Нил", dun=60, id=1)\n'
                            "Устгалаа: 1\nОлдсонгүй: 1\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="3\nnemeh Сараа 59\nshuuh 60\navah 0\n",
                        expected_output=(
                            "Нэмэгдлээ: Oyutan(ner='Сараа', dun=59, id=1)\nХоосон\nОлдсонгүй: 0\n"
                        ),
                    ),
                ),
                solution="""\
import sqlite3
from dataclasses import dataclass


@dataclass
class Oyutan:
    ner: str
    dun: int
    id: int | None = None  # сан руу хадгалсны дараа л id-тэй болно


class OyutanRepo:
    # SQL зөвхөн энэ класс дотор — ORM-ийн session-ий үүрэг
    def __init__(self, holbolt: sqlite3.Connection) -> None:
        self.holbolt = holbolt
        self.holbolt.execute(
            "CREATE TABLE oyutnuud (id INTEGER PRIMARY KEY, ner TEXT NOT NULL, dun INTEGER)"
        )

    def nemeh(self, oyutan: Oyutan) -> Oyutan:
        # объект → мөр. session.add + commit-ийн дараа id бөглөгддөгтэй адил
        kursor = self.holbolt.execute(
            "INSERT INTO oyutnuud (ner, dun) VALUES (?, ?)", (oyutan.ner, oyutan.dun)
        )
        oyutan.id = kursor.lastrowid
        return oyutan

    def avah(self, oyutan_id: int) -> Oyutan | None:
        mur = self.holbolt.execute(
            "SELECT id, ner, dun FROM oyutnuud WHERE id = ?", (oyutan_id,)
        ).fetchone()
        if mur is None:
            return None
        # мөр → объект
        return Oyutan(ner=mur[1], dun=mur[2], id=mur[0])

    def shuuh(self, dood_dun: int) -> list[Oyutan]:
        murnuud = self.holbolt.execute(
            "SELECT id, ner, dun FROM oyutnuud WHERE dun >= ? ORDER BY dun DESC, id",
            (dood_dun,),
        ).fetchall()
        return [Oyutan(ner=ner, dun=dun, id=mur_id) for mur_id, ner, dun in murnuud]

    def ustgah(self, oyutan_id: int) -> bool:
        kursor = self.holbolt.execute("DELETE FROM oyutnuud WHERE id = ?", (oyutan_id,))
        return kursor.rowcount > 0


repo = OyutanRepo(sqlite3.connect(":memory:"))
n = int(input())
for _ in range(n):
    hesguud = input().split()
    komand = hesguud[0]
    if komand == "nemeh":
        oyutan = repo.nemeh(Oyutan(hesguud[1], int(hesguud[2])))
        print(f"Нэмэгдлээ: {oyutan}")
    elif komand == "avah":
        oyutan = repo.avah(int(hesguud[1]))
        print(oyutan if oyutan is not None else f"Олдсонгүй: {hesguud[1]}")
    elif komand == "shuuh":
        oldson = repo.shuuh(int(hesguud[1]))
        if not oldson:
            print("Хоосон")
        for oyutan in oldson:
            print(oyutan)
    elif komand == "ustgah":
        oyutan_id = int(hesguud[1])
        if repo.ustgah(oyutan_id):
            print(f"Устгалаа: {oyutan_id}")
        else:
            print(f"Олдсонгүй: {oyutan_id}")
""",
                tips="""\
- Мөр → объект: `fetchone()` нь `(1, 'Бат', 85)` tuple эсвэл `None` буцаана.
  `None` бол шууд `None` буцаа, эс бөгөөс `Oyutan(ner=..., dun=..., id=...)`
  болго. `fetchall()`-ийн мөр бүрийг comprehension-оор хөрвүүл.
- `INSERT`-ийн дараа `kursor.lastrowid` нь сангийн өгсөн шинэ `id`. Өөрөө
  тоолуур хөтлөх хэрэггүй — `id`-г сан хариуцна.
- `holbolt.execute(...)` нь шинэ курсор буцаадаг товчлол — `lastrowid`,
  `rowcount`, `fetchone()`-г түүнээс ав.
- Бүх утгыг `?` параметрээр дамжуул — нэрэнд `'` орж болно. ORM яг ингэж
  injection-оос автоматаар хамгаалдаг.
""",
            ),
        ),
    ],
)

LOGGING = ModuleSpec(
    title="Модул 27 — Logging",
    description="print-ийн оронд зохистой бүртгэл.",
    lessons=[
        LessonSpec(
            title="logging модул",
            slug="logging",
            description="Түвшин, формат, файлд бичих.",
            duration=420,
            language=PY,
            content="""\
### Яагаад print биш вэ?

| print | logging |
|---|---|
| Үргэлж хэвлэнэ | Түвшнээр шүүнэ |
| Зөвхөн дэлгэц рүү | Файл, сүлжээ рүү ч |
| Цаг хугацаа байхгүй | Автомат цагтай |
| Production дээр устгах хэрэгтэй | Тохиргоогоор унтраана |

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

logger = logging.getLogger(__name__)

logger.info("Сервер эхэллээ")
logger.warning("Санах ой 80%% хүрлээ")
logger.error("Өгөгдлийн санд холбогдож чадсангүй")
```

### Түвшнүүд

```text
DEBUG    → нарийн мэдээлэл, зөвхөн хөгжүүлэлтэд
INFO     → хэвийн үйл явдал
WARNING  → анхаарах зүйл
ERROR    → алдаа гарсан
CRITICAL → програм үргэлжлэх боломжгүй
```

`level=logging.INFO` бол `DEBUG` харагдахгүй. Production дээр `INFO`,
хөгжүүлэлтэд `DEBUG` тавих нь түгээмэл.

### Алдааг stack trace-тэй бичих

```python
try:
    ...
except Exception:
    logger.exception("Тооцоолол амжилтгүй боллоо")
```

`logger.exception` нь алдааны бүрэн замыг автоматаар нэмнэ.

### Нууц мэдээлэл бүртгэхгүй

```python
logger.info("Нэвтэрлээ: %s", imeil)              # зөв
logger.info("Нууц үг: %s", nuuts_ug)             # ХЭЗЭЭ Ч ҮГҮЙ
```

Log файл нь ихэвчлэн олон хүнд харагддаг, удаан хадгалагддаг.

### Жишээ програм

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)-8s %(message)s",
)

logger = logging.getLogger("surgalt")

logger.debug("Энэ харагдахгүй — түвшин INFO байна")
logger.info("Сургалт ачаалагдлаа")
logger.warning("Хичээл 10 нь видеогүй байна")
logger.error("Өгөгдлийн санд холбогдож чадсангүй")


def hovoh(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        logger.exception("Хуваах үед алдаа гарлаа")
        return None


hovoh(10, 0)
```
""",
            initial_code="""\
import logging
import sys

tuvshin = input().strip()  # DEBUG, INFO, WARNING эсвэл ERROR

# TODO: level=tuvshin ба format="%(levelname)s [%(name)s] %(message)s" нэм.
#       stream=sys.stdout — шалгагч зөвхөн stdout-ийг хардаг.
#       force=True — өмнөх ажиллуулалтын тохиргоог дарж бичнэ.
logging.basicConfig(stream=sys.stdout, force=True)

logger = logging.getLogger("sensor")

n = int(input())
for _ in range(n):
    mur = input().strip()
    # TODO: int(mur) — ValueError бол logger.error("Тоо биш: %s", mur)
    # TODO: 80-аас их бол logger.warning(...), бусад нь logger.debug(...)

# TODO: logger.info("Нийт %s хэмжилт: %s анхааруулга, %s алдаа", ...)
""",
            exercise=ExerciseSpec(
                statement="""\
Серверийн өрөөний температур мэдрэгчийн хэмжилтийг `logging`-оор бүртгэ.
`print` биш — түвшнээр шүүгддэг log бичнэ: оролтын эхний мөрөнд ирсэн
түвшнээс доогуур мессеж харагдахгүй.

`logging.basicConfig`-ийг ингэж тохируул:

- `stream=sys.stdout` — анхдагчаар log нь stderr рүү явдаг, харин шалгагч
  зөвхөн stdout-ийг хардаг.
- `level=<оролтын түвшин>` — `"INFO"` гэх мэт мөрийг шууд өгч болно.
- `format="%(levelname)s [%(name)s] %(message)s"` — цаггүй, тогтмол формат.
- `force=True` — өмнөх ажиллуулалтын тохиргоог дарж бичнэ.

Logger-ийн нэр нь `sensor`. Хэмжилт бүрт:

- бүхэл тоо биш → `ERROR`: `Тоо биш: <мөр>`
- 80-аас их → `WARNING`: `Хэт халсан: <утга>`
- бусад → `DEBUG`: `Хэвийн: <утга>`

Эцэст нь `INFO`: `Нийт <n> хэмжилт: <k> анхааруулга, <e> алдаа`.

**Оролт:** эхний мөрөнд түвшин (`DEBUG`, `INFO`, `WARNING`, `ERROR`),
дараагийн мөрөнд хэмжилтийн тоо `n` (0 ≤ n ≤ 30), дараагийн `n` мөрөнд
хэмжилт.

**Гаралт:** түвшнээр шүүгдэж үлдсэн log мөрүүд, жишээ нь
`WARNING [sensor] Хэт халсан: 85`.
""",
                tests=(
                    TestCaseSpec(
                        stdin="INFO\n4\n72\n85\nabc\n80\n",
                        expected_output=(
                            "WARNING [sensor] Хэт халсан: 85\n"
                            "ERROR [sensor] Тоо биш: abc\n"
                            "INFO [sensor] Нийт 4 хэмжилт: 1 анхааруулга, 1 алдаа\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="DEBUG\n2\n25\n90\n",
                        expected_output=(
                            "DEBUG [sensor] Хэвийн: 25\n"
                            "WARNING [sensor] Хэт халсан: 90\n"
                            "INFO [sensor] Нийт 2 хэмжилт: 1 анхааруулга, 0 алдаа\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="WARNING\n3\n81\n-5\n2.5\n",
                        expected_output=(
                            "WARNING [sensor] Хэт халсан: 81\nERROR [sensor] Тоо биш: 2.5\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="ERROR\n3\n100\nхорин\n50\n",
                        expected_output="ERROR [sensor] Тоо биш: хорин\n",
                    ),
                    TestCaseSpec(
                        stdin="DEBUG\n0\n",
                        expected_output="INFO [sensor] Нийт 0 хэмжилт: 0 анхааруулга, 0 алдаа\n",
                    ),
                ),
                solution="""\
import logging
import sys

tuvshin = input().strip()
logging.basicConfig(
    stream=sys.stdout,  # шалгагч зөвхөн stdout-ийг хардаг
    level=tuvshin,  # "INFO" гэх мэт нэрийг шууд хүлээж авна
    format="%(levelname)s [%(name)s] %(message)s",
    force=True,  # өмнө нь тохируулсан handler-ийг сольно
)
logger = logging.getLogger("sensor")

n = int(input())
anhaaruulga = 0
aldaa = 0
for _ in range(n):
    mur = input().strip()
    try:
        utga = int(mur)
    except ValueError:
        aldaa += 1
        logger.error("Тоо биш: %s", mur)
        continue
    if utga > 80:
        anhaaruulga += 1
        logger.warning("Хэт халсан: %s", utga)
    else:
        # Түвшин INFO ба түүнээс дээш бол энэ мөр огт хэвлэгдэхгүй
        logger.debug("Хэвийн: %s", utga)

# Тоолуурууд түвшнээс үл хамааран бүх хэмжилтийг тоолсон
logger.info("Нийт %s хэмжилт: %s анхааруулга, %s алдаа", n, anhaaruulga, aldaa)
""",
                tips="""\
- `basicConfig` нь root logger-ийг **нэг удаа** тохируулдаг — handler аль
  хэдийн байвал юу ч хийхгүй. `force=True` нь хуучныг нь сольж, код дахин
  ажиллах бүрт шинэ тохиргоо үйлчилнэ.
- Түвшний шүүлтийг өөрөө `if`-ээр бичих хэрэггүй: `level="WARNING"` бол
  `logger.debug`, `logger.info` дуудлага юу ч хэвлэхгүй — logging-ийн гол
  давуу тал энэ.
- Мессежийг `logger.error("Тоо биш: %s", mur)` гэж `%s`-ээр дамжуул — мөрийг
  зөвхөн хэвлэгдэх үед нь угсардаг.
- Анхааруулга, алдааг түвшин ямар ч байсан **тоол** — дүгнэлтийн мөр харагдах
  үед тоо нь зөв байх ёстой. `80` хэвийн, `81` хэт халсан.
""",
            ),
        ),
    ],
)

INTERMEDIATE_PROJECT = ModuleSpec(
    title="Модул 28 — Дунд шатны төсөл",
    description="Бүх мэдлэгээ нэгтгэсэн жинхэнэ програм.",
    lessons=[
        LessonSpec(
            title="Төсөл — Сургалтын бүртгэлийн систем",
            slug="tusul-burtgeliin-system",
            description="OOP, dataclass, type hints, алдаа боловсруулалтыг нэгтгэнэ.",
            duration=900,
            language=PY,
            content="""\
Энэ төсөл дунд шатанд үзсэн бүхнийг нэг дор ашиглана.

### Шаардлага

1. Оюутан, сургалт бүртгэх
2. Оюутныг сургалтад бүртгэх
3. Дүн оруулах
4. Тайлан гаргах

### Ашиглах зүйлс

| Ойлголт | Хаана |
|---|---|
| `dataclass` | Оюутан, Сургалт |
| Type hints | Функц бүр |
| `raise` | Буруу өгөгдөл зогсооно |
| Comprehension | Тайлан бэлдэх |
| `property` | Тооцоологддог утга |

### Бүтцийн зарчим

Класс бүр **нэг үүрэгтэй**:

- `Oyutan` — оюутны өгөгдөл
- `Surgalt` — сургалтын өгөгдөл
- `Burtgel` — хоёуланг холбож удирдана

Энэ нь "single responsibility" зарчим. Алдаа хайх, өөрчлөхөд хамаагүй амархан
болгодог.

### Дараагийн алхам

Энэ логикийг FastAPI-д залгавал жинхэнэ вэб API болно. Өгөгдлийг
SQLAlchemy-аар хадгалвал програм хаагдсан ч үлдэнэ. Эдгээрийг
ахисан шатанд үзнэ.

### Жишээ програм

```python
from dataclasses import dataclass, field


@dataclass
class Oyutan:
    id: int
    ner: str
    dunguud: dict[str, int] = field(default_factory=dict)

    @property
    def dundaj(self) -> float:
        return sum(self.dunguud.values()) / len(self.dunguud) if self.dunguud else 0.0


@dataclass
class Surgalt:
    kod: str
    ner: str
    kredit: int


class Burtgel:
    def __init__(self) -> None:
        self.oyutnuud: dict[int, Oyutan] = {}
        self.surgaltuud: dict[str, Surgalt] = {}

    def oyutan_nemeh(self, oyutan: Oyutan) -> None:
        if oyutan.id in self.oyutnuud:
            raise ValueError(f"ID {oyutan.id} аль хэдийн бүртгэлтэй")
        self.oyutnuud[oyutan.id] = oyutan

    def surgalt_nemeh(self, surgalt: Surgalt) -> None:
        self.surgaltuud[surgalt.kod] = surgalt

    def dun_oruulah(self, oyutan_id: int, kod: str, dun: int) -> None:
        if not 0 <= dun <= 100:
            raise ValueError("Дүн 0-100 хооронд байх ёстой")
        if kod not in self.surgaltuud:
            raise KeyError(f"Сургалт олдсонгүй: {kod}")
        self.oyutnuud[oyutan_id].dunguud[kod] = dun

    def tailan(self) -> list[str]:
        eremblesen = sorted(self.oyutnuud.values(), key=lambda o: o.dundaj, reverse=True)
        return [f"{o.ner:<10} {o.dundaj:>6.1f}" for o in eremblesen]


burtgel = Burtgel()
burtgel.surgalt_nemeh(Surgalt("PY101", "Python үндэс", 3))
burtgel.surgalt_nemeh(Surgalt("DB201", "Өгөгдлийн сан", 4))

burtgel.oyutan_nemeh(Oyutan(1, "Бат"))
burtgel.oyutan_nemeh(Oyutan(2, "Цэцэг"))

burtgel.dun_oruulah(1, "PY101", 85)
burtgel.dun_oruulah(1, "DB201", 78)
burtgel.dun_oruulah(2, "PY101", 95)

print(f"{'Нэр':<10} {'Дундаж':>6}")
print("-" * 17)
for mur in burtgel.tailan():
    print(mur)

print()
try:
    burtgel.dun_oruulah(1, "PY101", 150)
except ValueError as aldaa:
    print("Алдаа барьж авлаа:", aldaa)
```
""",
            initial_code="""\
from dataclasses import dataclass, field


class BurtgelAldaa(Exception):
    # Бүртгэлийн дүрэм зөрчигдөхөд үүсгэнэ: raise BurtgelAldaa("тайлбар")
    pass


@dataclass
class Surgalt:
    kod: str
    kredit: int


@dataclass
class Oyutan:
    id: int
    ner: str
    dunguud: dict[str, int] = field(default_factory=dict)  # {код: дүн}


class Burtgel:
    def __init__(self) -> None:
        self.surgaltuud: dict[str, Surgalt] = {}
        self.oyutnuud: dict[int, Oyutan] = {}

    def surgalt_nemeh(self, surgalt: Surgalt) -> None:
        # TODO: код давхардвал BurtgelAldaa("сургалт давхардсан: <код>")
        pass

    def oyutan_nemeh(self, oyutan: Oyutan) -> None:
        # TODO: id давхардвал BurtgelAldaa("ID <id> аль хэдийн бүртгэлтэй")
        pass

    def dun_oruulah(self, oyutan_id: int, kod: str, dun: int) -> None:
        # TODO: оюутан → сургалт → дүнгийн муж гэсэн дарааллаар шалгаж,
        #       бүгд зөв бол oyutan.dunguud[kod] = dun
        pass

    def tailan(self) -> list[str]:
        # TODO: кредитээр жигнэсэн дундаж (Σ дүн × кредит / Σ кредит)-аар
        #       буурах, тэнцвэл нэрээр эрэмбэлсэн мөрүүд + «Дүнгүй: ...» мөр.
        #       Оюутан огт байхгүй бол ["(хоосон)"].
        return []


burtgel = Burtgel()
n = int(input())
for _ in range(n):
    hesguud = input().split()
    komand = hesguud[0]
    # TODO: доорх хэсгийг try/except-д хий:
    #       except BurtgelAldaa as aldaa -> «Алдаа: <aldaa>»
    #       except ValueError -> «Алдаа: буруу тоо» (int() тоо биш текст авбал)
    if komand == "surgalt":
        burtgel.surgalt_nemeh(Surgalt(hesguud[1], int(hesguud[2])))
    elif komand == "tailan":
        print("Тайлан:")
        for mur in burtgel.tailan():
            print(mur)
    # TODO: oyutan, dun командууд; бусад нь BurtgelAldaa("үл мэдэх команд: ...")
""",
            exercise=ExerciseSpec(
                statement="""\
Дунд шатны мэдлэгээ нэгтгэсэн командын мөрийн бүртгэлийн систем бич:
`dataclass`, класс, өөрийн алдааны класс, type hints, эрэмбэлэлт.

```text
surgalt <код> <кредит>    сургалт нэмнэ
oyutan <id> <нэр>         оюутан нэмнэ
dun <id> <код> <дүн>      дүн оруулна (дахин оруулбал хуучныг солино)
tailan                    тайлан хэвлэнэ
```

Амжилттай команд юу ч хэвлэхгүй. Алдаа бол `Алдаа: <тайлбар>` хэвлээд
дараагийн команд руу үргэлжилнэ:

- тоо байх ёстой газар тоо биш → `буруу тоо` (бусад шалгалтаас өмнө)
- давхардсан сургалт → `сургалт давхардсан: <код>`
- давхардсан оюутан → `ID <id> аль хэдийн бүртгэлтэй`
- `dun`: эхлээд оюутан → `оюутан олдсонгүй: <id>`, дараа нь сургалт →
  `сургалт олдсонгүй: <код>`, дараа нь дүн 0–100 биш →
  `дүн 0-100 хооронд байх ёстой`
- танихгүй команд → `үл мэдэх команд: <команд>`

**Тайлан:** `Тайлан:` мөрийн дараа дүнтэй оюутнуудыг **кредитээр жигнэсэн
дундажаар** (Σ дүн × кредит / Σ кредит) буурах, тэнцвэл нэрээр эрэмбэлж
`<байр>. <нэр> <дундаж, .2f> (<кредитийн нийлбэр> кредит)` гэж хэвлэнэ.
Кредитийн нийлбэрт зөвхөн дүн авсан сургалтууд орно. Дүнгүй оюутан байвал
сүүлд нь `Дүнгүй: <нэр>, <нэр>` (нэрээр эрэмбэлсэн). Нэг ч оюутан байхгүй бол
`Тайлан:`-ийн дараа `(хоосон)`.

**Оролт:** эхний мөрөнд командын тоо `n` (1 ≤ n ≤ 40), дараагийн `n` мөрөнд
команд. Командын үгийн тоо үргэлж зөв; нэр ба код нь зайгүй.

**Гаралт:** алдааны мөрүүд ба тайлан, командын дарааллаар.
""",
                tests=(
                    TestCaseSpec(
                        stdin=(
                            "8\nsurgalt PY101 3\nsurgalt DB201 4\noyutan 1 Бат\noyutan 2 Цэцэг\n"
                            "dun 1 PY101 85\ndun 1 DB201 78\ndun 2 PY101 95\ntailan\n"
                        ),
                        expected_output=(
                            "Тайлан:\n1. Цэцэг 95.00 (3 кредит)\n2. Бат 81.00 (7 кредит)\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin=(
                            "7\nsurgalt PY101 3\noyutan 1 Бат\noyutan 1 Болд\ndun 2 PY101 90\n"
                            "dun 1 JS101 90\ndun 1 PY101 150\ntailan\n"
                        ),
                        expected_output=(
                            "Алдаа: ID 1 аль хэдийн бүртгэлтэй\n"
                            "Алдаа: оюутан олдсонгүй: 2\n"
                            "Алдаа: сургалт олдсонгүй: JS101\n"
                            "Алдаа: дүн 0-100 хооронд байх ёстой\n"
                            "Тайлан:\nДүнгүй: Бат\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin=(
                            "12\nsurgalt MATH 5\nsurgalt ART 1\noyutan 10 Сараа\noyutan 20 Ану\n"
                            "oyutan 30 Золбоо\ndun 10 MATH 70\ndun 10 MATH 90\ndun 20 MATH 90\n"
                            "dun 30 ART abc\nhevleh\nsurgalt ART 2\ntailan\n"
                        ),
                        expected_output=(
                            "Алдаа: буруу тоо\n"
                            "Алдаа: үл мэдэх команд: hevleh\n"
                            "Алдаа: сургалт давхардсан: ART\n"
                            "Тайлан:\n1. Ану 90.00 (5 кредит)\n2. Сараа 90.00 (5 кредит)\n"
                            "Дүнгүй: Золбоо\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin=(
                            "9\ntailan\nsurgalt A1 2\nsurgalt B2 3\nsurgalt C3 4\n"
                            "oyutan 5 Тэмүүлэн\ndun 5 A1 100\ndun 5 B2 0\ndun 5 C3 77\ntailan\n"
                        ),
                        expected_output=(
                            "Тайлан:\n(хоосон)\nТайлан:\n1. Тэмүүлэн 56.44 (9 кредит)\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin=(
                            "11\nsurgalt X 1\nsurgalt Y 2\noyutan 3 Гэрэл\noyutan 1 Дорж\n"
                            "oyutan 2 Батаа\noyutan x9 Нэр\ndun 3 X 60\ndun 1 Y 75\ndun 1 X 90\n"
                            "dun 2 Y -1\ntailan\n"
                        ),
                        expected_output=(
                            "Алдаа: буруу тоо\n"
                            "Алдаа: дүн 0-100 хооронд байх ёстой\n"
                            "Тайлан:\n1. Дорж 80.00 (3 кредит)\n2. Гэрэл 60.00 (1 кредит)\n"
                            "Дүнгүй: Батаа\n"
                        ),
                    ),
                ),
                solution="""\
from dataclasses import dataclass, field


class BurtgelAldaa(Exception):
    # Бүртгэлийн дүрэм зөрчигдөхөд үүсгэнэ — мессеж нь хэрэглэгчид харагдана
    pass


@dataclass
class Surgalt:
    kod: str
    kredit: int


@dataclass
class Oyutan:
    id: int
    ner: str
    dunguud: dict[str, int] = field(default_factory=dict)  # оюутан бүрт шинэ dict


class Burtgel:
    def __init__(self) -> None:
        self.surgaltuud: dict[str, Surgalt] = {}
        self.oyutnuud: dict[int, Oyutan] = {}

    def surgalt_nemeh(self, surgalt: Surgalt) -> None:
        if surgalt.kod in self.surgaltuud:
            raise BurtgelAldaa(f"сургалт давхардсан: {surgalt.kod}")
        self.surgaltuud[surgalt.kod] = surgalt

    def oyutan_nemeh(self, oyutan: Oyutan) -> None:
        if oyutan.id in self.oyutnuud:
            raise BurtgelAldaa(f"ID {oyutan.id} аль хэдийн бүртгэлтэй")
        self.oyutnuud[oyutan.id] = oyutan

    def dun_oruulah(self, oyutan_id: int, kod: str, dun: int) -> None:
        # Шалгах дараалал нь даалгаварт заасантай яг ижил
        if oyutan_id not in self.oyutnuud:
            raise BurtgelAldaa(f"оюутан олдсонгүй: {oyutan_id}")
        if kod not in self.surgaltuud:
            raise BurtgelAldaa(f"сургалт олдсонгүй: {kod}")
        if not 0 <= dun <= 100:
            raise BurtgelAldaa("дүн 0-100 хооронд байх ёстой")
        self.oyutnuud[oyutan_id].dunguud[kod] = dun

    def kredit(self, oyutan: Oyutan) -> int:
        # Зөвхөн дүн авсан сургалтын кредит
        return sum(self.surgaltuud[kod].kredit for kod in oyutan.dunguud)

    def dundaj(self, oyutan: Oyutan) -> float:
        # Жигнэсэн дундаж: Σ дүн × кредит / Σ кредит
        niilber = sum(dun * self.surgaltuud[kod].kredit for kod, dun in oyutan.dunguud.items())
        return niilber / self.kredit(oyutan)

    def tailan(self) -> list[str]:
        if not self.oyutnuud:
            return ["(хоосон)"]
        # Дүнгүй оюутныг тусад нь — тэдний кредит 0 тул дундаж тооцохгүй
        duntei = [o for o in self.oyutnuud.values() if o.dunguud]
        dungui = sorted(o.ner for o in self.oyutnuud.values() if not o.dunguud)
        duntei.sort(key=lambda o: (-self.dundaj(o), o.ner))
        murnuud = [
            f"{i}. {o.ner} {self.dundaj(o):.2f} ({self.kredit(o)} кредит)"
            for i, o in enumerate(duntei, start=1)
        ]
        if dungui:
            murnuud.append("Дүнгүй: " + ", ".join(dungui))
        return murnuud


burtgel = Burtgel()
n = int(input())
for _ in range(n):
    hesguud = input().split()
    komand = hesguud[0]
    # Бүх алдааг нэг газар барина — методууд print хийхгүй, raise хийнэ
    try:
        if komand == "surgalt":
            burtgel.surgalt_nemeh(Surgalt(hesguud[1], int(hesguud[2])))
        elif komand == "oyutan":
            burtgel.oyutan_nemeh(Oyutan(int(hesguud[1]), hesguud[2]))
        elif komand == "dun":
            burtgel.dun_oruulah(int(hesguud[1]), hesguud[2], int(hesguud[3]))
        elif komand == "tailan":
            print("Тайлан:")
            for mur in burtgel.tailan():
                print(mur)
        else:
            raise BurtgelAldaa(f"үл мэдэх команд: {komand}")
    except BurtgelAldaa as aldaa:
        print(f"Алдаа: {aldaa}")
    except ValueError:
        # int("abc") — метод дуудагдахаас өмнө гарна
        print("Алдаа: буруу тоо")
""",
                tips="""\
- Алдааг методын дотор `raise BurtgelAldaa("...")`-аар үүсгээд, командын
  давталтад **нэг** `try/except`-ээр барь — метод бүр өөрөө `print` хийх
  шаардлагагүй.
- `int("abc")` нь `ValueError` үүсгэнэ — метод дуудагдахаас өмнө гарах тул
  «буруу тоо» бусад шалгалтаас түрүүлнэ. `BurtgelAldaa`-г `Exception`-оос
  удамшуулбал `ValueError`-той андуурагдахгүй.
- Жигнэсэн дундаж: дүн бүрийг тухайн сургалтын кредитээр үржүүлж нэмээд нийт
  кредитэд хуваа. Дүнгүй оюутныг тусад нь ялга, эс бөгөөс тэгд хуваана.
- Олон түлхүүрээр эрэмбэлэх: `key=lambda o: (-dundaj, o.ner)`.
  `field(default_factory=dict)` нь оюутан бүрт тусдаа `dunguud` өгнө.
""",
            ),
        ),
    ],
)

INTERMEDIATE_MODULES = [
    OOP,
    ITERATORS,
    FUNCTIONAL,
    TYPE_HINTS,
    DATACLASSES,
    VENV,
    DEPENDENCIES,
    TESTING,
    GIT,
    HTTP_APIS,
    SQL,
    SQLALCHEMY,
    LOGGING,
    INTERMEDIATE_PROJECT,
]
