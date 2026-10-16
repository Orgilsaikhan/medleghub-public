"""Модул 7-14 — Функц, мөр, файл, алдаа, модул, төслүүд."""

from app.content.types import ExerciseSpec, LessonSpec, ModuleSpec, TestCaseSpec
from app.models.enums import LessonLanguage

PY = LessonLanguage.PYTHON

FUNCTIONS = ModuleSpec(
    title="Модул 7 — Функц (Functions)",
    description="Кодоо дахин ашиглагдах хэсгүүдэд хуваах.",
    lessons=[
        LessonSpec(
            title="Функц зарлах ба буцаах",
            slug="funkts-zarlah",
            description="def, параметр, return.",
            duration=420,
            language=PY,
            content="""\
Функц нь давтагдах кодыг нэг нэрийн дор багцлана.

```python
def mendchileh(ner):
    return f"Сайн байна уу, {ner}!"

print(mendchileh("Бат"))
```

### return vs print

Энэ хоёрыг андуурах нь маш түгээмэл:

```python
def nemeh_print(a, b):
    print(a + b)        # зөвхөн харуулна

def nemeh_return(a, b):
    return a + b        # утга БУЦААНА

dun = nemeh_return(2, 3)
print(dun * 10)         # 50 — утгыг цааш ашиглаж болно

dun2 = nemeh_print(2, 3)
print(dun2)             # None — юу ч буцаагаагүй
```

`return` байхгүй функц `None` буцаана. `None` бол «утга байхгүй» гэсэн
тусгай утга. Утга `None` эсэхийг `==` биш `is`-ээр шалгадаг:

```python
if dun2 is None:
    print("Функц юу ч буцаагаагүй")
```

Эсрэгээр нь `is not None` гэж бичнэ.

### Функц олон утга буцаах

`return`-ийн ард таслалаар бичвэл tuple буцаана — дуудсан газар нь задална:

```python
def ehnii_ba_suuliin(ug):
    return ug[0], ug[-1]

ehnii, suuliin = ehnii_ba_suuliin("Python")   # "P", "n"
```

### Анхдагч утга

```python
def mendchileh(ner="зочин"):
    return f"Сайн байна уу, {ner}!"

print(mendchileh())          # Сайн байна уу, зочин!
print(mendchileh("Бат"))     # Сайн байна уу, Бат!
```

### Нэрээр дамжуулах

```python
def hereglegch_uusgeh(ner, nas, hot="Улаанбаатар"):
    print(ner, nas, hot)

hereglegch_uusgeh(ner="Бат", nas=20)
hereglegch_uusgeh("Бат", 20, hot="Дархан")
```

Нэрээр дамжуулсан нь уншихад хамаагүй ойлгомжтой — ялангуяа параметр олонтой үед.

### Жишээ програм

```python
def mendchileh(ner="зочин"):
    return f"Сайн байна уу, {ner}!"

print(mendchileh())
print(mendchileh("Бат"))


def dundaj_bodoh(toonuud):
    if not toonuud:
        return 0
    return sum(toonuud) / len(toonuud)


print(dundaj_bodoh([90, 85, 78]))
print(dundaj_bodoh([]))
```
""",
            initial_code="""\
def hyamdraltai_une(une, huvi=10):
    # TODO: хямдралын дараах үнийг return хийнэ (print биш!)
    #       томьёо: une * (100 - huvi) // 100
    pass  # «юу ч хийхгүй» гэсэн түр орлуулагч — өөрийн кодоор солино


# 1. Барааны тоо n-ийг уншина

# 2. n удаа: мөрийг split() хийж үнэ (байвал хувийг ч) int() болгоно

# 3. Хувь байвал hyamdraltai_une(une, huvi), үгүй бол hyamdraltai_une(une)
#    гэж дуудаад үр дүнг хэвлэнэ
""",
            exercise=ExerciseSpec(
                statement="""\
Дэлгүүрт хямдралтай үнэ боддог функц хэрэгтэй боллоо.
`hyamdraltai_une(une, huvi=10)` функцийг бич: хямдралын дараах үнийг
`une * (100 - huvi) // 100` томьёогоор **буцаана** (`return`). Хувь
өгөгдөөгүй бол анхдагч **10%** хямдрал үйлчилнэ.

**Оролт:** эхний мөрөнд барааны тоо `n`. Дараагийн `n` мөр бүрт зөвхөн үнэ,
эсвэл зайгаар тусгаарласан үнэ ба хямдралын хувь (бүхэл тоонууд).

**Гаралт:** бараа бүрийн хямдарсан үнийг тус тусад нь мөрөнд хэвлэнэ.

**Хязгаарлалт:** `0 ≤ хувь ≤ 100`. Функц дотор `print` бүү хий — утгыг
буцааж, хэвлэхийг үндсэн хэсэгт үлдээ.
""",
                tests=(
                    TestCaseSpec(
                        stdin="3\n10000\n25000 20\n999 50\n",
                        expected_output="9000\n20000\n499\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="2\n5000 0\n5000 100\n",
                        expected_output="5000\n0\n",
                    ),
                    TestCaseSpec(
                        stdin="1\n7\n",
                        expected_output="6\n",
                    ),
                    TestCaseSpec(
                        stdin="4\n120000\n120000 15\n1 10\n35500 35\n",
                        expected_output="108000\n102000\n0\n23075\n",
                    ),
                ),
                solution="""\
def hyamdraltai_une(une, huvi=10):
    # Хямдралын дараах үнийг БУЦААНА — хэвлэхгүй
    return une * (100 - huvi) // 100


n = int(input())
# _ — давталтын хувьсагчийн утгыг ашиглахгүй гэсэн тохиролцоот нэр
for _ in range(n):
    hesguud = input().split()
    une = int(hesguud[0])
    if len(hesguud) == 2:
        # Хувь өгөгдсөн — хоёр аргументтай дуудна
        print(hyamdraltai_une(une, int(hesguud[1])))
    else:
        # Хувь өгөгдөөгүй — анхдагч 10% үйлчилнэ
        print(hyamdraltai_une(une))
""",
                tips="""\
- Функц утгыг `return`-ээр **буцаана**. Дотроо `print` хийдэг функц `None`
  буцаадаг тул `print(hyamdraltai_une(...))` нь `None` гэж хэвлэнэ.
- `huvi=10` гэсэн анхдагч утгатай тул `hyamdraltai_une(une)` гэж ганц
  аргументаар дуудахад `huvi` автоматаар 10 болно.
- Мөрийг `split()` хийхэд жагсаалтын урт 1 эсвэл 2 болно — `len(...)`-ээр аль
  тохиолдол болохыг шалга.
- `//` бол бүхэл хуваалт. `/` хэрэглэвэл `9000.0` гэх мэт бутархай гарна.
- Хувь 0 ба 100 байх хилийн тохиолдлыг бод.
""",
            ),
        ),
        LessonSpec(
            title="Хамрах хүрээ (Scope)",
            slug="hamrah-huree",
            description="Хувьсагч хаана амьдардаг вэ.",
            duration=360,
            language=PY,
            content="""\
Функц дотор үүссэн хувьсагч зөвхөн тэр функц дотор амьдарна.

```python
def tootsoolol():
    dotood = 10
    print(dotood)      # ажиллана

tootsoolol()
print(dotood)          # NameError — гадна харагдахгүй
```

### Гадаад хувьсагчийг унших

```python
NIIT = 100

def hariu():
    return NIIT * 2    # уншиж болно

print(hariu())         # 200
```

### Гэхдээ өөрчилж болохгүй

```python
too = 0

def nemeh():
    too = too + 1      # UnboundLocalError!

nemeh()
```

Python `too` -г функцийн дотоод хувьсагч гэж үзээд, утга оноохоос
өмнө уншсан гэж алдаа заана.

### Зөв шийдэл: утга буцаах

```python
def nemeh(too):
    return too + 1

too = nemeh(too)
```

`global` түлхүүр үг байдаг ч **түүнээс зайлсхийх** нь зөв. Функц нь
оролтоо аваад гаралтаа буцаах нь ойлгомжтой, тестлэхэд амархан байдаг.

### Жишээ програм

```python
NIIT_DUN = 100


def huvi_bodoh(hesgiin_dun):
    # Гадаад тогтмолыг уншиж болно
    return hesgiin_dun / NIIT_DUN * 100


print(f"{huvi_bodoh(85):.0f}%")   # :.0f — бутархайгүй, бүхэлд дугуйрхайлна


# Зөв хэв маяг: оролт → гаралт
def toolol_nemeh(odoogiin):
    return odoogiin + 1


toolol = 0
toolol = toolol_nemeh(toolol)
toolol = toolol_nemeh(toolol)
print("Тоолол:", toolol)
```
""",
            initial_code="""\
HURAAMJ = 100  # зарлага бүрийн шимтгэл — гадаад тогтмол


def shinechleh(uldegdel, temdeg, dun):
    # TODO: "+" бол uldegdel + dun-г буцаана
    # TODO: "-" бол dun + HURAAMJ-г хасна; хүрэлцэхгүй бол uldegdel-ийг
    #       хэвээр нь буцаана
    return uldegdel


# 1. Эхний үлдэгдэл ба гүйлгээний тоо n-ийг уншина

# 2. n удаа: "+ 5000" мөрийг split() хийж тэмдэг, дүнг салгана

# 3. uldegdel = shinechleh(...) гэж шинэчлээд (global биш!) үлдэгдлийг хэвлэнэ
""",
            exercise=ExerciseSpec(
                statement="""\
Хэтэвчний үлдэгдлийг гүйлгээ бүрийн дараа хэвлэдэг програм бич. Шинэ
үлдэгдлийг `shinechleh(uldegdel, temdeg, dun)` функц **буцаадаг** байх ёстой —
`global` ашиглахгүй. Зарлага бүрт `HURAAMJ = 100` төгрөгийн шимтгэл нэмж
хасагдана.

- `+ dun` — орлого: үлдэгдэл дээр `dun` нэмэгдэнэ.
- `- dun` — зарлага: `dun + HURAAMJ` хасагдана. Үлдэгдэл хүрэлцэхгүй бол
  гүйлгээ **цуцлагдаж**, үлдэгдэл өөрчлөгдөхгүй.

**Оролт:** эхний мөрөнд эхний үлдэгдэл, хоёр дахь мөрөнд гүйлгээний тоо `n`.
Дараагийн `n` мөр бүрт `+` эсвэл `-` тэмдэг ба дүн (зайгаар тусгаарласан).

**Гаралт:** гүйлгээ бүрийн дараах үлдэгдлийг тус тусад нь мөрөнд хэвлэнэ.

**Хязгаарлалт:** бүх тоо сөрөг биш бүхэл тоо, `dun ≥ 1`.
""",
                tests=(
                    TestCaseSpec(
                        stdin="10000\n4\n+ 5000\n- 3000\n- 20000\n+ 100\n",
                        expected_output="15000\n11900\n11900\n12000\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="500\n2\n- 400\n- 1\n",
                        expected_output="0\n0\n",
                    ),
                    TestCaseSpec(
                        stdin="0\n3\n- 1\n+ 250\n- 150\n",
                        expected_output="0\n250\n0\n",
                    ),
                    TestCaseSpec(
                        stdin="1000000\n5\n- 999900\n+ 1\n+ 2\n- 3\n- 1\n",
                        expected_output="0\n1\n3\n3\n3\n",
                    ),
                ),
                solution="""\
HURAAMJ = 100  # зарлага бүрийн шимтгэл — гадаад тогтмол


def shinechleh(uldegdel, temdeg, dun):
    # Гадаад тогтмолыг зөвхөн уншина — өөрчлөхгүй
    if temdeg == "+":
        return uldegdel + dun
    zarlaga = dun + HURAAMJ
    if zarlaga > uldegdel:
        # Хүрэлцэхгүй — үлдэгдэл хэвээрээ
        return uldegdel
    return uldegdel - zarlaga


uldegdel = int(input())
n = int(input())
for _ in range(n):
    temdeg, dun = input().split()
    # global-гүйгээр: буцаасан утгаар хувьсагчаа шинэчилнэ
    uldegdel = shinechleh(uldegdel, temdeg, int(dun))
    print(uldegdel)
""",
                tips="""\
- Функц доторх `uldegdel` бол **дотоод** хувьсагч — түүнийг өөрчлөх нь гаднах
  хувьсагчид нөлөөлөхгүй. Тиймээс шинэ утгыг `return` хийгээд гадна нь
  `uldegdel = shinechleh(...)` гэж хадгал.
- `HURAAMJ` зэрэг гадаад тогтмолыг функц дотроос **уншиж** болно, харин
  утга оноох гэвэл `UnboundLocalError` гарна.
- Зарлагыг шалгахдаа шимтгэлтэй нийт дүнг (`dun + HURAAMJ`) үлдэгдэлтэй
  харьцуул. Яг тэнцүү бол гүйлгээ хийгдэж үлдэгдэл 0 болно.
- `input().split()` нь `["+", "5000"]` буцаана — дүнг `int()` болгохоо бүү март.
""",
            ),
        ),
    ],
)

STRINGS = ModuleSpec(
    title="Модул 8 — Мөр (Strings)",
    description="Текст боловсруулах.",
    lessons=[
        LessonSpec(
            title="Мөрийн үндсэн үйлдлүүд",
            slug="muriin-uildluud",
            description="upper, strip, replace, split.",
            duration=420,
            language=PY,
            content="""\
Мөр нь маш олон бэлэн боломжтой.

```python
mur = "  Сайн байна уу  "

print(mur.strip())            # хоёр талын зайг арилгана
print(mur.upper())            # ТОМ ҮСЭГ
print(mur.lower())            # жижиг үсэг
print(mur.replace("Сайн", "Муу"))
```

### split ба join

```python
ugs = "алим,лийр,гүзээлзгэнэ".split(",")
print(ugs)          # ['алим', 'лийр', 'гүзээлзгэнэ']

niilsen = ", ".join(ugs)
print(niilsen)      # алим, лийр, гүзээлзгэнэ
```

Эдгээр нь хосолсон үйлдэл — файл, CSV боловсруулахад байнга хэрэглэгдэнэ.

### Хайх ба шалгах

```python
mur = "medleghub@example.com"

print("@" in mur)               # True
print(mur.startswith("med"))    # True
print(mur.endswith(".com"))     # True
print(mur.find("@"))            # 9  (индекс)
```

### Мөр өөрчлөгддөггүй

```python
mur = "Бат"
mur[0] = "П"        # TypeError!
```

Бүх мөрийн метод нь **шинэ мөр буцаана**, эхнийхийг өөрчлөхгүй:

```python
mur = "бат"
mur.upper()          # үр дүн хаяглагдаагүй тул алга болно
mur = mur.upper()    # зөв нь ингэж хадгална
```

### Жишээ програм

```python
mur = "  Сайн байна уу, MedlegHub  "

print(f"[{mur.strip()}]")
print(mur.strip().upper())
print(mur.replace("MedlegHub", "Монгол"))

# split ба join
jagsaalt_mur = "алим,лийр,гүзээлзгэнэ"
jimsnuud = jagsaalt_mur.split(",")
print(jimsnuud)
print(" | ".join(jimsnuud))

# Имэйл шалгах (энгийн хувилбар)
imeil = "bat@medleghub.mn"
zuv = "@" in imeil and "." in imeil.split("@")[-1]
print("Имэйл зөв эсэх:", zuv)
```
""",
            initial_code="""\
mur = input()

# 1. mur-г "," тэмдгээр split() хийж шошгонуудыг салгана

# 2. Шошго бүрийг strip() ба lower() хийнэ, хоосон бол алгасна

# 3. Доторх зайг replace()-ээр "_" болгож, урд нь "#" залгана

# 4. Давхардсаныг алгасаад " ".join(...)-ээр нэг мөрөнд хэвлэнэ
#    (нэг ч шошго үлдээгүй бол «Шошго алга»)
""",
            exercise=ExerciseSpec(
                statement="""\
Нийтлэлийн шошгуудыг таслалаар тусгаарласан нэг мөрөөр өгнө. Тэдгээрийг
цэвэрлэж **hashtag** болгон хэвлэ:

- шошго бүрийн хоёр талын зайг арилгаж, жижиг үсэг болгоно;
- шошго доторх зайг `_` тэмдэгтээр солиод урд нь `#` залгана;
- хоосон шошгыг алгасна;
- давхардсан шошгыг (жижиг үсэг болгосны дараа) анх гарсан байранд нь зөвхөн
  нэг удаа үлдээнэ.

**Оролт:** нэг мөр — таслалаар тусгаарласан шошгууд. Шошго доторх үгс яг
нэг зайгаар тусгаарлагдсан.

**Гаралт:** hashtag-уудыг нэг зайгаар тусгаарлан нэг мөрөнд хэвлэнэ. Нэг ч
шошго үлдээгүй бол `Шошго алга` гэж хэвлэнэ.
""",
                tests=(
                    TestCaseSpec(
                        stdin="  Python , Вэб хөгжүүлэлт,python,  ДАТА \n",
                        expected_output="#python #вэб_хөгжүүлэлт #дата\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin=",, ,\n",
                        expected_output="Шошго алга\n",
                    ),
                    TestCaseSpec(
                        stdin="AI\n",
                        expected_output="#ai\n",
                    ),
                    TestCaseSpec(
                        stdin="Монгол хэл, монгол ХЭЛ ,Код, ,код,Нээлттэй эх сурвалж,\n",
                        expected_output="#монгол_хэл #код #нээлттэй_эх_сурвалж\n",
                    ),
                ),
                solution="""\
mur = input()

hashtaguud = []
for shoshgo in mur.split(","):
    # Хоёр талын зайг арилгаад жижиг үсэг болгоно
    shoshgo = shoshgo.strip().lower()
    if shoshgo == "":
        continue  # хоосон шошгыг алгасна
    # Доторх зайг доогуур зураас болгоод урд нь # залгана
    tag = "#" + shoshgo.replace(" ", "_")
    if tag not in hashtaguud:
        hashtaguud.append(tag)

if hashtaguud:
    print(" ".join(hashtaguud))
else:
    print("Шошго алга")
""",
                tips="""\
- `split(",")` нь мөрийг таслал бүр дээр хуваана — хэсгүүдийн хоёр талд зай,
  эсвэл бүр хоосон хэсэг үлдэж болно. Тиймээс хэсэг бүрт `strip()` хий.
- Мөрийн метод **шинэ мөр буцаадаг**: `shoshgo.lower()` гэж дуудаад
  орхивол юу ч өөрчлөгдөхгүй — `shoshgo = shoshgo.strip().lower()` гэж хадгал.
- Давхардлыг `in` оператороор шалга: `if tag not in hashtaguud`. Жижиг үсэг
  болгосны **дараа** шалгавал `Python`, `python` хоёр нэг шошго болно.
- Эцэст нь `" ".join(...)`-аар нэгтгэнэ. Жагсаалт хоосон үед тусгай мөр
  хэвлэхээ бүү март.
""",
            ),
        ),
        LessonSpec(
            title="f-string ба форматлалт",
            slug="f-string-format",
            description="Тоо, огноог гоё харуулах.",
            duration=360,
            language=PY,
            content="""\
f-string нь мөр дотор утга шигтгэх хамгийн орчин үеийн арга.

```python
ner = "Бат"
dun = 87.5678

print(f"{ner}: {dun}")            # Бат: 87.5678
print(f"{ner}: {dun:.2f}")        # Бат: 87.57
```

### Тоон форматлалт

| Формат | Үр дүн |
|---|---|
| `{dun:.1f}` | `87.6` |
| `{dun:.0f}` | `88` |
| `{1234567:,}` | `1,234,567` |
| `{0.256:.1%}` | `25.6%` |

### Байрлал ба өргөн

Хүснэгт хэвлэхэд хэрэгтэй:

```python
for ner, dun in [("Бат", 90), ("Цэцэг", 100)]:
    print(f"{ner:<10} {dun:>5}")
```

```text
Бат           90
Цэцэг        100
```

- `<` зүүн тийш
- `>` баруун тийш
- `^` голлуулна

### Дибаг хийхэд хэрэгтэй заль

```python
too = 42
print(f"{too=}")      # too=42
```

Хувьсагчийн нэр, утгыг хамт хэвлэнэ — `print("too =", too)` бичихээс хурдан.

### Жишээ програм

```python
oyutnuud = [("Бат", 87.5678), ("Цэцэг", 95.2), ("Болд", 72.0)]

print(f"{'Нэр':<10} {'Дүн':>8}")
print("-" * 19)   # мөрийг тоогоор үржүүлбэл давтана: "-" 19 удаа
for ner, dun in oyutnuud:
    print(f"{ner:<10} {dun:>8.1f}")

print()

# Тоон форматууд
une = 1234567
print(f"Үнэ: {une:,}₮")

huvi = 0.2567
print(f"Хувь: {huvi:.1%}")

# Дибаг
too = 42
print(f"{too=}")
```
""",
            initial_code="""\
n = int(input())

# 1. Толгой мөр: «Бараа» 10 өргөнд зүүн тийш, «Тоо» 5, «Дүн» 12 өргөнд
#    баруун тийш — f"{'Бараа':<10}..." хэлбэрээр

# 2. 27 ширхэг «-»

# 3. n мөр уншиж, бараа бүрийн мөрийг дүнгийн хамт (тоо × үнэ, мянгатын
#    таслалтай) хэвлэнэ

# 4. Дахин 27 «-», дараа нь «Нийт» ба «Дундаж» мөрүүд
""",
            exercise=ExerciseSpec(
                statement="""\
Дэлгүүрийн баримтыг хүснэгт хэлбэрээр хэвлэ. Бараа бүрийн дүн нь
**тоо ширхэг × нэгжийн үнэ**.

**Оролт:** эхний мөрөнд барааны тоо `n` (`n ≥ 1`). Дараагийн `n` мөр бүрт
барааны нэр (зайгүй, 10-аас ихгүй тэмдэгт), тоо ширхэг, нэгжийн үнэ.

**Гаралт:** баганын өргөнийг яг дагаж хэвлэнэ:

- толгой мөр: `Бараа` — 10 тэмдэгтийн өргөнд зүүн тийш, `Тоо` — 5 өргөнд
  баруун тийш, `Дүн` — 12 өргөнд баруун тийш;
- 27 ширхэг `-` тэмдэгт;
- бараа бүр: нэр (10, зүүн), тоо ширхэг (5, баруун), дүн (12, баруун,
  мянгатын таслалтай);
- дахин 27 ширхэг `-`;
- `Нийт` (10, зүүн) ба нийт дүн (17, баруун, мянгатын таслалтай);
- `Дундаж: <нийт / n>` — мянгатын таслалтай, таслалаас хойш 2 оронтой.
""",
                tests=(
                    TestCaseSpec(
                        stdin="3\nТалх 2 2500\nСүү 3 3200\nБяслаг 1 18500\n",
                        expected_output=(
                            "Бараа       Тоо         Дүн\n"
                            "---------------------------\n"
                            "Талх          2       5,000\n"
                            "Сүү           3       9,600\n"
                            "Бяслаг        1      18,500\n"
                            "---------------------------\n"
                            "Нийт                 33,100\n"
                            "Дундаж: 11,033.33\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="1\nЗурагт 2 1899000\n",
                        expected_output=(
                            "Бараа       Тоо         Дүн\n"
                            "---------------------------\n"
                            "Зурагт        2   3,798,000\n"
                            "---------------------------\n"
                            "Нийт              3,798,000\n"
                            "Дундаж: 3,798,000.00\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="4\nАлим 12 450\nХарандаа 100 150\nЦүнх 1 125000\nДэвтэр 0 900\n",
                        expected_output=(
                            "Бараа       Тоо         Дүн\n"
                            "---------------------------\n"
                            "Алим         12       5,400\n"
                            "Харандаа    100      15,000\n"
                            "Цүнх          1     125,000\n"
                            "Дэвтэр        0           0\n"
                            "---------------------------\n"
                            "Нийт                145,400\n"
                            "Дундаж: 36,350.00\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="5\nКофе 3 7500\nЦай 10 1200\nЖүүс 6 3300\nУс 24 800\nШоколад 7 2999\n",
                        expected_output=(
                            "Бараа       Тоо         Дүн\n"
                            "---------------------------\n"
                            "Кофе          3      22,500\n"
                            "Цай          10      12,000\n"
                            "Жүүс          6      19,800\n"
                            "Ус           24      19,200\n"
                            "Шоколад       7      20,993\n"
                            "---------------------------\n"
                            "Нийт                 94,493\n"
                            "Дундаж: 18,898.60\n"
                        ),
                    ),
                ),
                solution="""\
n = int(input())

print(f"{'Бараа':<10}{'Тоо':>5}{'Дүн':>12}")
print("-" * 27)

niit = 0
for _ in range(n):
    ner, too, une = input().split()
    dun = int(too) * int(une)
    niit += dun
    # < зүүн, > баруун тийш шахна; «,» нь мянгатын таслал
    print(f"{ner:<10}{too:>5}{dun:>12,}")

print("-" * 27)
print(f"{'Нийт':<10}{niit:>17,}")
# .2f — таслалаас хойш яг 2 орон
print(f"Дундаж: {niit / n:,.2f}")
""",
                tips="""\
- `f"{ner:<10}"` нь 10 тэмдэгтийн өргөнд зүүн тийш, `f"{too:>5}"` нь 5
  өргөнд баруун тийш шахна. Толгой мөрөнд ч ижил өргөн хэрэглэ:
  `f"{'Бараа':<10}"`.
- Мянгатын таслал: `f"{dun:>12,}"`; бутархайтай бол `f"{x:,.2f}"`.
- `split()` нь текст буцаана — дүнг бодохын өмнө тоо ширхэг, үнийг `int()`
  болго.
- Мөрийн төгсгөлийн зай тооцогдохгүй, харин **эхний ба дундах** зай яг
  таарах ёстой — нэг ч зайгаар зөрвөл тест унана.
""",
            ),
        ),
    ],
)

FILES = ModuleSpec(
    title="Модул 9 — Файл (Files)",
    description="Диск дээрх өгөгдөл унших, бичих.",
    lessons=[
        LessonSpec(
            title="Файл унших",
            slug="fail-unshih",
            description="with open, кодчилол.",
            duration=420,
            language=PY,
            content="""\
Файл уншихдаа `with open(...)` хэрэглэнэ.

```python
with open("medee.txt", encoding="utf-8") as f:
    aguulga = f.read()

print(aguulga)
```

### Яагаад `with` вэ?

`with` блок дуусмагц файлыг **автоматаар хаана**. Алдаа гарсан ч хаагдана.

```python
# Ингэж бичвэл алдаа гарахад файл нээлттэй үлдэнэ
f = open("medee.txt")
aguulga = f.read()
f.close()
```

### Кодчилол (encoding)

Монгол үсэгтэй файл уншихдаа `encoding="utf-8"` **заавал** бичнэ.
Эс бөгөөс Windows дээр үсэг эвдэрч, `UnicodeDecodeError` гарч болно.

### Мөр мөрөөр унших

```python
with open("medee.txt", encoding="utf-8") as f:
    for mur in f:
        print(mur.strip())
```

Энэ нь `read()`-ээс **санах ойд хэмнэлттэй**. Том файл уншихад
`read()` нь бүхэлд нь санах ойд ачаалдаг.

| Метод | Буцаах утга |
|---|---|
| `f.read()` | Бүх агуулга нэг мөр болгож |
| `f.readlines()` | Мөрүүдийн жагсаалт |
| `for mur in f` | Мөр бүрийг ээлжлэн |

### Жишээ програм

```python
# Эхлээд унших файлаа үүсгэе (бичихийг дараагийн хичээлд дэлгэрэнгүй үзнэ)
with open("medee.txt", "w", encoding="utf-8") as f:
    f.write("эхний мөр\\nхоёр дахь мөр\\nгурав дахь мөр\\n")

# Бүхэлд нь унших
with open("medee.txt", encoding="utf-8") as f:
    aguulga = f.read()
print(aguulga)

# Мөр мөрөөр унших (том файлд тохиромжтой)
with open("medee.txt", encoding="utf-8") as f:
    for i, mur in enumerate(f, start=1):
        print(f"{i}: {mur.strip()}")
```

Байхгүй файлыг нээх гэвэл `FileNotFoundError` алдаа гарч програм зогсоно.
Ийм алдааг барьж авахыг Модул 11-д үзнэ.
""",
            initial_code="""\
# Бэлтгэл: оролтын мөрүүдийг "onoo.txt" файлд хадгална (энэ хэсгийг бүү өөрчил)
n = int(input())
with open("onoo.txt", "w", encoding="utf-8") as f:
    for _ in range(n):
        f.write(input() + "\\n")

# 1. "onoo.txt"-г with open(..., encoding="utf-8")-ээр нээнэ

# 2. for mur in f: — мөр бүрийг strip() хийж, хоосон бол алгасна

# 3. "нэр,оноо"-г split(",")-ээр салгаж, тоо, нийлбэр, шилдгийг хөтөлнө

# 4. «Сурагч», «Шилдэг», «Дундаж» гэсэн гурван мөр хэвлэнэ
""",
            exercise=ExerciseSpec(
                statement="""\
Сурагчдын оноо `onoo.txt` файлд `нэр,оноо` хэлбэрээр мөр бүрт бичигдсэн.
Эхлэл кодын бэлтгэл хэсэг оролтыг тэр файлд хадгална — чиний ажил бол
**файлыг мөр мөрөөр уншиж** сурагчийн тоо, шилдэг сурагч, дундаж оноог олох.

**Оролт:** эхний мөрөнд `n`, дараагийн `n` мөр нь файлын агуулга. Хоосон
(эсвэл зөвхөн зайтай) мөр байж болно — түүнийг алгасна. Таслалын хоёр талд
зай байж болно. Хоосон биш мөр дор хаяж нэг бий.

**Гаралт:**

```text
Сурагч: <хоосон биш мөрийн тоо>
Шилдэг: <нэр> (<оноо>)
Дундаж: <дундаж оноо, таслалаас хойш 2 оронтой>
```

Хамгийн өндөр оноотой хэд байвал файлд **түрүүлж** бичигдсэнийг нь сонго.
""",
                tests=(
                    TestCaseSpec(
                        stdin="4\nБат,85\nЦэцэг,98\nБолд,72\nСараа,90\n",
                        expected_output="Сурагч: 4\nШилдэг: Цэцэг (98)\nДундаж: 86.25\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="4\nНомин,70\n\nГанаа,95\nЭнх,64\n",
                        expected_output="Сурагч: 3\nШилдэг: Ганаа (95)\nДундаж: 76.33\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="5\n\nДорж, 60\n  \nОюун ,60\nТөмөр,59\n",
                        expected_output="Сурагч: 3\nШилдэг: Дорж (60)\nДундаж: 59.67\n",
                    ),
                    TestCaseSpec(
                        stdin="1\nАнар,100\n",
                        expected_output="Сурагч: 1\nШилдэг: Анар (100)\nДундаж: 100.00\n",
                    ),
                    TestCaseSpec(
                        stdin="6\nНомин,0\nГанаа,0\nЭнх,1\nДорж,0\nБат,0\nОюун,0\n",
                        expected_output="Сурагч: 6\nШилдэг: Энх (1)\nДундаж: 0.17\n",
                    ),
                ),
                solution="""\
# Бэлтгэл: оролтын мөрүүдийг "onoo.txt" файлд хадгална
n = int(input())
with open("onoo.txt", "w", encoding="utf-8") as f:
    for _ in range(n):
        f.write(input() + "\\n")

too = 0
niilber = 0
shildeg_ner = ""
shildeg_onoo = -1

# Мөр мөрөөр уншина — with блок дуусахад файл автоматаар хаагдана
with open("onoo.txt", encoding="utf-8") as f:
    for mur in f:
        mur = mur.strip()
        if not mur:
            continue  # хоосон мөрийг алгасна
        ner, onoo = mur.split(",")
        onoo = int(onoo)
        too += 1
        niilber += onoo
        # Зөвхөн ИЛҮҮ оноо шинэчилнэ — тэнцвэл эхнийх нь үлдэнэ
        if onoo > shildeg_onoo:
            shildeg_ner = ner.strip()
            shildeg_onoo = onoo

print(f"Сурагч: {too}")
print(f"Шилдэг: {shildeg_ner} ({shildeg_onoo})")
print(f"Дундаж: {niilber / too:.2f}")
""",
                tips="""\
- `with open("onoo.txt", encoding="utf-8") as f:` дотор `for mur in f:` гэж
  мөр бүрийг ээлжлэн уншина. Мөр бүр төгсгөлдөө `\\n`-тэй ирдэг тул
  `strip()` хий.
- `strip()`-ийн дараа хоосон мөр `""` болно — `if not mur: continue`.
- `split(",")`-ийн хэсгүүдэд ч зай үлдэж болно: нэрийг `strip()` хий.
  `int()` харин хоёр талын зайг өөрөө тэвчдэг.
- Шилдгийг шинэчлэхдээ `>` ашигла (`>=` биш) — тэгвэл тэнцүү оноотой үед
  эхнийх нь үлдэнэ.
""",
            ),
        ),
        LessonSpec(
            title="Файл бичих",
            slug="fail-bichih",
            description="Бичих ба нэмэх горим.",
            duration=360,
            language=PY,
            content="""\
### Горимууд

| Горим | Утга | Анхаар |
|---|---|---|
| `"r"` | унших (анхдагч) | Файл байхгүй бол алдаа |
| `"w"` | бичих | **Хуучин агуулгыг устгана** |
| `"a"` | нэмэх | Төгсгөлд нь залгана |
| `"x"` | шинээр үүсгэх | Байвал алдаа |

```python
with open("tailan.txt", "w", encoding="utf-8") as f:
    f.write("Эхний мөр\\n")
    f.write("Хоёр дахь мөр\\n")
```

> `"w"` горим нь файлыг **шууд цэвэрлэдэг**. Log бичихэд `"a"` хэрэглэнэ.

### Мөр таслалт

`write()` нь автоматаар мөр таслахгүй. `\\n` -г өөрөө бичнэ.
`print()`-ээс ялгаатай.

```python
murnuud = ["нэг", "хоёр", "гурав"]

with open("jagsaalt.txt", "w", encoding="utf-8") as f:
    for mur in murnuud:
        f.write(mur + "\\n")
```

### print-ээс ялгаа

| | `print(x)` | `f.write(x)` |
|---|---|---|
| Хаашаа | Дэлгэц | Файл |
| Мөр таслах | Өөрөө | `\\n`-г өөрөө бичнэ |
| Утгын төрөл | Юу ч байж болно | Зөвхөн мөр — тоог `f"{x}"` болго |

Файлын замтай найдвартай ажиллах стандарт `pathlib` модулийг `import`-ийн
хамт Модул 12-т үзнэ.

### Жишээ програм

```python
# Бичих — хуучин агуулга устана
with open("tailan.txt", "w", encoding="utf-8") as f:
    f.write("Тайлан\\n")
    f.write("=" * 20 + "\\n")

# Нэмэх — төгсгөлд залгана
oyutnuud = [("Бат", 90), ("Цэцэг", 95)]
with open("tailan.txt", "a", encoding="utf-8") as f:
    for ner, dun in oyutnuud:
        f.write(f"{ner},{dun}\\n")

# Бичсэнээ буцааж уншиж шалгана
with open("tailan.txt", encoding="utf-8") as f:
    print(f.read())

# Мөрүүдийн жагсаалт болгож унших
with open("tailan.txt", encoding="utf-8") as f:
    murnuud = f.readlines()
print("Мөрийн тоо:", len(murnuud))
```
""",
            initial_code="""\
ognoo = input()
n = int(input())

# 1. "tailan.txt"-г "w" горимоор нээж «Тайлан: <огноо>» мөрийг бичнэ
#    (write() мөр таслахгүй — төгсгөлд нь "\\n"-г өөрөө нэмнэ)

# 2. "a" горимоор нээж, n барааг «- <нэр>: <дүн>₮» гэж нэмээд
#    эцэст нь «Нийт: <нийлбэр>₮» мөрийг нэмнэ

# 3. Файлыг уншиж агуулгыг нь хэвлээд, «Мөр: <мөрийн тоо>» хэвлэнэ
""",
            exercise=ExerciseSpec(
                statement="""\
Өдрийн борлуулалтын тайланг `tailan.txt` файлд бичээд, дараа нь файлаа
буцааж уншиж хэвлэ.

1. `"w"` горимоор `Тайлан: <огноо>` мөрийг бичнэ.
2. `"a"` горимоор бараа бүрийг `- <нэр>: <дүн>₮` гэж нэмээд, эцэст нь
   `Нийт: <нийлбэр>₮` мөрийг нэмнэ.
3. Файлыг уншиж агуулгыг нь яг хэвээр хэвлээд, сүүлд нь
   `Мөр: <файлын мөрийн тоо>` хэвлэнэ.

**Оролт:** эхний мөрөнд огноо, хоёр дахь мөрөнд барааны тоо `n` (`n ≥ 0`).
Дараагийн `n` мөр бүрт `нэр,дүн` (нэр зайтай байж болно, дүн бүхэл тоо).

**Гаралт:** дээр тайлбарласан файлын агуулга ба `Мөр: ...` мөр.

Файл програм дууссаны дараа ч үлддэг — «Код ажиллуулах»-ыг хоёр удаа
дараад үзээрэй. Эхний бичилтийг `"w"` горимоор хийхгүй бол ажиллуулах бүрд
тайлан давхарлана.
""",
                tests=(
                    TestCaseSpec(
                        stdin="2024-05-01\n3\nТалх,5000\nСүү,9600\nБяслаг,18500\n",
                        expected_output=(
                            "Тайлан: 2024-05-01\n"
                            "- Талх: 5000₮\n"
                            "- Сүү: 9600₮\n"
                            "- Бяслаг: 18500₮\n"
                            "Нийт: 33100₮\n"
                            "Мөр: 5\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="2024-12-31\n0\n",
                        expected_output="Тайлан: 2024-12-31\nНийт: 0₮\nМөр: 2\n",
                    ),
                    TestCaseSpec(
                        stdin="2025-01-15\n1\nУлаан алим,4500\n",
                        expected_output=(
                            "Тайлан: 2025-01-15\n- Улаан алим: 4500₮\nНийт: 4500₮\nМөр: 3\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="2025-02-28\n4\nКофе,22500\nЦай,12000\nНоос бээлий,35000\nУс,800\n",
                        expected_output=(
                            "Тайлан: 2025-02-28\n"
                            "- Кофе: 22500₮\n"
                            "- Цай: 12000₮\n"
                            "- Ноос бээлий: 35000₮\n"
                            "- Ус: 800₮\n"
                            "Нийт: 70300₮\n"
                            "Мөр: 6\n"
                        ),
                    ),
                ),
                solution="""\
ognoo = input()
n = int(input())

# "w" — файлыг шинээр эхлүүлнэ, өмнөх агуулга устана
with open("tailan.txt", "w", encoding="utf-8") as f:
    f.write(f"Тайлан: {ognoo}\\n")

niit = 0
# "a" — файлын төгсгөлд залгана
with open("tailan.txt", "a", encoding="utf-8") as f:
    for _ in range(n):
        ner, dun = input().split(",")
        dun = int(dun)
        niit += dun
        # write() мөр таслахгүй тул \\n-г өөрсдөө нэмнэ
        f.write(f"- {ner}: {dun}₮\\n")
    f.write(f"Нийт: {niit}₮\\n")

# Бичсэнээ буцааж уншиж шалгана
with open("tailan.txt", encoding="utf-8") as f:
    murnuud = f.readlines()

for mur in murnuud:
    print(mur, end="")
print(f"Мөр: {len(murnuud)}")
""",
                tips="""\
- `"w"` нь файлыг **цэвэрлээд** эхэлнэ, `"a"` нь төгсгөлд нь **залгана**.
  Эхний мөрийг `"a"`-гаар бичвэл өмнөх ажиллуулалтын агуулга үлдэж, тайлан
  давхарлана.
- `write()` мөр таслахгүй — мөр бүрийн төгсгөлд `"\\n"`-г өөрөө нэм.
- `split(",")`-ээр нэр, дүнг салгаад дүнг `int()` болгож нийлбэрт нэм.
- `f.readlines()` мөрүүдийн жагсаалт буцаана — `len(...)` нь мөрийн тоо.
  Мөр бүр `\\n`-тэй ирдэг тул `print(mur, end="")` эсвэл `mur.strip()` хэрэглэ.
""",
            ),
        ),
    ],
)

JSON_MODULE = ModuleSpec(
    title="Модул 10 — JSON",
    description="Програмууд хоорондоо өгөгдөл солилцох формат.",
    lessons=[
        LessonSpec(
            title="JSON унших ба бичих",
            slug="json-unshih-bichih",
            description="dumps, loads, dump, load.",
            duration=420,
            language=PY,
            content="""\
JSON бол програмууд хоорондоо өгөгдөл солилцох хамгийн түгээмэл формат.
Вэб API бараг бүгд JSON ашигладаг.

```python
import json

oyutan = {"ner": "Бат", "nas": 20, "dunguud": [90, 85]}

mur = json.dumps(oyutan, ensure_ascii=False)
print(mur)
```

Эхний мөрийн `import json` нь Python-д бэлэн ирдэг `json` **модулийг**
ачаална. Үүний дараа түүний функцуудыг модулийн нэрээр нь — `json.dumps(...)`
гэж — дуудна. Модул, `import`-ийн тухай Модул 12-т дэлгэрэнгүй үзнэ.

### Дөрвөн функц

| Функц | Юунаас юу руу |
|---|---|
| `json.dumps(obj)` | Python → мөр |
| `json.loads(mur)` | мөр → Python |
| `json.dump(obj, f)` | Python → файл |
| `json.load(f)` | файл → Python |

`s` үсэг нь **string** гэсэн үг. `s`-гүй нь файлтай ажиллана.

### Монгол үсэг

```python
json.dumps({"ner": "Бат"})                      # {"ner": "\\u0411\\u0430\\u0442"}
json.dumps({"ner": "Бат"}, ensure_ascii=False)  # {"ner": "Бат"}
```

`ensure_ascii=False` бичихгүй бол кирилл үсэг escape болно. Техникийн
хувьд зөв ч уншихад тохиромжгүй.

### Уншихад тохиромжтой хэлбэр

```python
json.dumps(data, ensure_ascii=False, indent=2)
```

### Төрлийн харгалзаа

| Python | JSON |
|---|---|
| `dict` | object |
| `list` | array |
| `str` | string |
| `True` / `False` | `true` / `false` |
| `None` | `null` |

### Жишээ програм

```python
import json

oyutan = {
    "ner": "Бат",
    "nas": 20,
    "dunguud": [90, 85, 78],
    "tugssun": False,
}

# Python → JSON мөр
mur = json.dumps(oyutan, ensure_ascii=False, indent=2)
print(mur)

print("---")

# JSON мөр → Python
buts = json.loads(mur)
print(buts["ner"], "→", sum(buts["dunguud"]) / len(buts["dunguud"]))
```
""",
            initial_code="""\
import json

mur = input()

# 1. json.loads(mur)-ээр текстийг толь бичиг болгоно

# 2. "baraa" жагсаалтаар гүйж une × too-г нэмээд нийт дүнг олно

# 3. «Хэрэглэгч», «Барааны төрөл», «Нийт» мөрүүдийг хэвлэнэ

# 4. {"hereglegch": ..., "niit": ..., "unegui_hurgelt": ...} толь бичгийг
#    json.dumps(..., ensure_ascii=False)-ээр хэвлэнэ
""",
            exercise=ExerciseSpec(
                statement="""\
Онлайн дэлгүүрийн захиалга JSON текст хэлбэрээр ирнэ. Түүнийг `json`
модулиар задалж, захиалгын дүнг бодоод, товч хураангуйг буцаад JSON болгон
хэвлэ.

**Оролт:** нэг мөр — JSON объект. `"hereglegch"` нь хэрэглэгчийн нэр (текст),
`"baraa"` нь барааны жагсаалт; бараа бүр `"ner"`, `"une"`, `"too"` талбартай.
Түлхүүрүүдийн дараалал өөр байж, илүү талбар ч байж болно.

**Гаралт:** дөрвөн мөр:

```text
Хэрэглэгч: <нэр>
Барааны төрөл: <жагсаалтын урт>
Нийт: <une × too-ийн нийлбэр>₮
{"hereglegch": "<нэр>", "niit": <нийт>, "unegui_hurgelt": <true/false>}
```

`unegui_hurgelt` нь нийт дүн **50000-аас багагүй** бол `true`. Сүүлийн мөрийг
`json.dumps(..., ensure_ascii=False)`-ээр, түлхүүрүүдийг яг энэ дарааллаар
хэвлэ.
""",
                tests=(
                    TestCaseSpec(
                        stdin='{"hereglegch": "Бат", "baraa": [{"ner": "Талх", "une": 2500, "too": 2}, {"ner": "Сүү", "une": 3200, "too": 3}, {"ner": "Бяслаг", "une": 18500, "too": 1}]}\n',
                        expected_output=(
                            "Хэрэглэгч: Бат\n"
                            "Барааны төрөл: 3\n"
                            "Нийт: 33100₮\n"
                            '{"hereglegch": "Бат", "niit": 33100, "unegui_hurgelt": false}\n'
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin='{"hereglegch": "Сараа", "baraa": [{"ner": "Гутал", "une": 89000, "too": 1}]}\n',
                        expected_output=(
                            "Хэрэглэгч: Сараа\n"
                            "Барааны төрөл: 1\n"
                            "Нийт: 89000₮\n"
                            '{"hereglegch": "Сараа", "niit": 89000, "unegui_hurgelt": true}\n'
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin='{"hereglegch": "Болд", "baraa": []}\n',
                        expected_output=(
                            "Хэрэглэгч: Болд\n"
                            "Барааны төрөл: 0\n"
                            "Нийт: 0₮\n"
                            '{"hereglegch": "Болд", "niit": 0, "unegui_hurgelt": false}\n'
                        ),
                    ),
                    TestCaseSpec(
                        stdin='{"baraa": [{"ner": "Ном", "une": 25000, "too": 2}], "hereglegch": "\\u041d\\u043e\\u043c\\u0438\\u043d"}\n',
                        expected_output=(
                            "Хэрэглэгч: Номин\n"
                            "Барааны төрөл: 1\n"
                            "Нийт: 50000₮\n"
                            '{"hereglegch": "Номин", "niit": 50000, "unegui_hurgelt": true}\n'
                        ),
                    ),
                    TestCaseSpec(
                        stdin='{"baraa":[{"too":4,"une":1500,"ner":"Алим"},{"ner":"Ус","une":800,"too":6}],"hereglegch":"Дорж","utas":"99112233"}\n',
                        expected_output=(
                            "Хэрэглэгч: Дорж\n"
                            "Барааны төрөл: 2\n"
                            "Нийт: 10800₮\n"
                            '{"hereglegch": "Дорж", "niit": 10800, "unegui_hurgelt": false}\n'
                        ),
                    ),
                ),
                solution="""\
import json

# JSON текстээс Python толь бичиг рүү
zahialga = json.loads(input())

niit = 0
for baraa in zahialga["baraa"]:
    niit += baraa["une"] * baraa["too"]

print(f"Хэрэглэгч: {zahialga['hereglegch']}")
print(f"Барааны төрөл: {len(zahialga['baraa'])}")
print(f"Нийт: {niit}₮")

huraangui = {
    "hereglegch": zahialga["hereglegch"],
    "niit": niit,
    "unegui_hurgelt": niit >= 50000,  # Python-ий True → JSON-ий true
}
# ensure_ascii=False — кирилл үсэг \\u0411 гэх мэтээр хувирахгүй
print(json.dumps(huraangui, ensure_ascii=False))
""",
                tips="""\
- `json.loads(mur)` нь JSON текстийг Python толь бичиг болгоно — дараа нь
  `zahialga["baraa"]` гэж энгийн жагсаалт шиг хандана.
- Python-ий `True`/`False` нь `json.dumps`-аар `true`/`false` болно — JSON
  текстийг гараар угсрах шаардлагагүй.
- `ensure_ascii=False` бичихгүй бол кирилл нэр `\\u0411...` болж хувирна.
  Оролтод escape хэлбэрээр ирсэн текстийг ч `loads` жинхэнэ үсэг болгоно.
- `dumps` толь бичгийн түлхүүрийг оруулсан дарааллаар нь хэвлэдэг —
  `hereglegch`, `niit`, `unegui_hurgelt` дарааллаар үүсгэ.
- Хоосон жагсаалт болон яг 50000 гэсэн хилийн утгыг бод.
""",
            ),
        ),
    ],
)

ERRORS = ModuleSpec(
    title="Модул 11 — Алдаа боловсруулах",
    description="Програм гэнэт унахаас сэргийлэх.",
    lessons=[
        LessonSpec(
            title="try, except, finally",
            slug="try-except",
            description="Алдааг барьж авах.",
            duration=420,
            language=PY,
            content="""\
```python
try:
    too = int("энэ тоо биш")
except ValueError:
    print("Тоо руу хөрвүүлж чадсангүй")
```

### Тодорхой алдааг барь

```python
try:
    hariu = 10 / 0
except ZeroDivisionError:
    print("Тэгд хувааж болохгүй")
except ValueError:
    print("Утга буруу")
```

### Бүх алдааг барих нь муу дадал

```python
try:
    too = int(input())
except:                    # МУУ — бүх алдааг нууна
    pass                   # pass — «юу ч хийхгүй»
```

Ингэвэл жинхэнэ асуудал нуугдаж, дибаг хийхэд туйлын хэцүү болно.
Ямар алдаа хүлээж байгаагаа **тодорхой бич**.

### else ба finally

```python
try:
    f = open("medee.txt", encoding="utf-8")
except FileNotFoundError:
    print("Файл олдсонгүй")
else:
    print("Амжилттай нээлээ")     # алдаа гараагүй бол
    f.close()
finally:
    print("Энэ мөр ҮРГЭЛЖ ажиллана")
```

### Өөрийн алдаа үүсгэх

```python
def nas_shalgah(nas):
    if nas < 0:
        raise ValueError("Нас сөрөг байж болохгүй")
    return nas
```

Буруу өгөгдлийг **эрт зогсоох** нь дараа нь ойлгомжгүй алдаа гарахаас дээр.

### Жишээ програм

```python
def too_ruu_hurvuuleh(mur):
    try:
        return int(mur)
    except ValueError:
        print(f"'{mur}' нь тоо биш байна")
        return None


print(too_ruu_hurvuuleh("42"))
print(too_ruu_hurvuuleh("бат"))

print("---")


def hovoh(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None
    finally:
        print(f"{a} / {b} хийж үзлээ")


print(hovoh(10, 2))
print(hovoh(10, 0))

print("---")


def nas_shalgah(nas):
    if nas < 0:
        raise ValueError("Нас сөрөг байж болохгүй")
    return nas


try:
    nas_shalgah(-5)
except ValueError as aldaa:
    print("Алдаа:", aldaa)
```
""",
            initial_code="""\
def onoo_shalgah(mur):
    # TODO: int(mur)-ээр тоо болгоно (тоо биш бол ValueError өөрөө гарна)
    # TODO: 0-100 хооронд биш бол raise ValueError(...) хийнэ
    # TODO: зөв оноог return хийнэ
    return int(mur)


n = int(input())
onoonuud = []

# 1. n мөр уншиж, мөр бүрийг strip() хийнэ

# 2. try: onoo_shalgah(...) — амжилттай бол жагсаалтад нэмнэ
#    except ValueError: «Алгаслаа: <мөр>» хэвлэнэ

# 3. try: дунджийг бодно; except ZeroDivisionError: «Хүчинтэй оноо алга»;
#    else: «Дундаж: <2 оронтой>» хэвлэнэ
""",
            exercise=ExerciseSpec(
                statement="""\
Шалгалтын оноог гараар оруулсан тул дунд нь алдаатай мөр байж болно. Буруу
мөрүүдийг `try`/`except`-ээр барьж алгасаад, зөв оноонуудын дунджийг ол.

Хүчинтэй оноо бол `int()`-ээр хөрвөх, **0-ээс 100** хүртэлх бүхэл тоо. Хөрвөхгүй
бол `int()` өөрөө `ValueError` шиднэ; хязгаараас гадуур бол `onoo_shalgah`
функц дотроо `raise ValueError(...)` хийнэ.

**Оролт:** эхний мөрөнд `n`, дараагийн `n` мөр бүрт нэг оноо (буруу байж болно).

**Гаралт:**

- буруу мөр бүрт (хоёр талын зайг арилгаад) `Алгаслаа: <мөр>`;
- эцэст нь `Дундаж: <дундаж>` — таслалаас хойш 2 оронтой. Хүчинтэй оноо огт
  байхгүй бол дундаж бодоход гарах `ZeroDivisionError`-ыг барьж
  `Хүчинтэй оноо алга` гэж хэвлэнэ.
""",
                tests=(
                    TestCaseSpec(
                        stdin="5\n90\nхорин\n75\n-5\n100\n",
                        expected_output="Алгаслаа: хорин\nАлгаслаа: -5\nДундаж: 88.33\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="3\n101\n12.5\nарав\n",
                        expected_output=(
                            "Алгаслаа: 101\nАлгаслаа: 12.5\nАлгаслаа: арав\nХүчинтэй оноо алга\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="4\n 0 \n100\n+50\n7\n",
                        expected_output="Дундаж: 39.25\n",
                    ),
                    TestCaseSpec(
                        stdin="3\n\n55\n1e2\n",
                        expected_output="Алгаслаа:\nАлгаслаа: 1e2\nДундаж: 55.00\n",
                    ),
                    TestCaseSpec(
                        stdin="6\n60\n61\n62\n63\n64\n65\n",
                        expected_output="Дундаж: 62.50\n",
                    ),
                ),
                solution="""\
def onoo_shalgah(mur):
    # int() нь тоо биш текст дээр ValueError өөрөө шиднэ
    onoo = int(mur)
    if onoo < 0 or onoo > 100:
        # Тоо мөн ч хязгаараас гадуур — алдааг өөрсдөө үүсгэнэ
        raise ValueError("Оноо 0-100 хооронд байх ёстой")
    return onoo


n = int(input())
onoonuud = []
for _ in range(n):
    mur = input().strip()
    try:
        onoonuud.append(onoo_shalgah(mur))
    except ValueError:
        print(f"Алгаслаа: {mur}")

try:
    dundaj = sum(onoonuud) / len(onoonuud)
except ZeroDivisionError:
    # Жагсаалт хоосон — 0-д хуваах гэж оролдлоо
    print("Хүчинтэй оноо алга")
else:
    print(f"Дундаж: {dundaj:.2f}")
""",
                tips="""\
- Алдаа гарч болох кодоо `try:` блокт, алдаа гарсан үед хийх зүйлээ
  `except ValueError:` блокт бич. Програм унахгүй, дараагийн мөр рүү шилжинэ.
- `raise ValueError("...")` нь `int()`-ийн алдаатай ижил төрлийнх тул ганц
  `except ValueError` хоёуланг нь барина.
- Хоосон жагсаалт дээр `sum(x) / len(x)` нь `ZeroDivisionError` өгнө —
  `except ZeroDivisionError:` ба `else:` хэсгийг ашигла.
- `int()` бутархай, үсэг, хоосон мөрийг хүлээж авдаггүй; харин хоёр талын зай
  ба `+`/`-` тэмдгийг зөвшөөрдөг. `-5` бол тоо мөн ч хязгаараас гадуур.
""",
            ),
        ),
    ],
)

MODULES = ModuleSpec(
    title="Модул 12 — Модул ба багц",
    description="Кодоо олон файлд хуваах.",
    lessons=[
        LessonSpec(
            title="import хийх",
            slug="import-hiih",
            description="Стандарт сан болон өөрийн файл.",
            duration=420,
            language=PY,
            content="""\
Python-д маш баялаг **стандарт сан** бэлэн ирдэг.

```python
import math
print(math.sqrt(16))       # 4.0

from datetime import date
print(date.today())

import random
print(random.choice(["алим", "лийр"]))
```

### import -ийн хэлбэрүүд

```python
import math                      # math.sqrt(16)
from math import sqrt            # sqrt(16)
from math import sqrt as ug      # ug(16)
from math import *               # ЗАЙЛСХИЙ — юу орж ирснийг мэдэхгүй
```

### Өөрийн модул

`tootsoolol.py` файл үүсгээд:

```python
def nemeh(a, b):
    return a + b
```

`main.py` дотор:

```python
from tootsoolol import nemeh
print(nemeh(2, 3))
```

### `if __name__ == "__main__"`

```python
def nemeh(a, b):
    return a + b

if __name__ == "__main__":
    print(nemeh(2, 3))     # зөвхөн шууд ажиллуулахад
```

Энэ файлыг **import хийхэд** доорх блок ажиллахгүй. Тиймээс модул нь
функцээ санал болгохын зэрэгцээ бие даан ч ажиллаж чадна.

### Хэрэгтэй стандарт модулууд

| Модул | Зориулалт |
|---|---|
| `math` | Математик |
| `random` | Санамсаргүй утга |
| `datetime` | Огноо, цаг |
| `json` | JSON |
| `pathlib` | Файлын зам |
| `collections` | Нэмэлт бүтцүүд |

### pathlib — файлын зам

```python
from pathlib import Path

zam = Path("data") / "tailan.txt"               # data/tailan.txt
zam.parent.mkdir(parents=True, exist_ok=True)   # data хавтсыг (байхгүй бол) үүсгэнэ
zam.write_text("агуулга", encoding="utf-8")
print(zam.read_text(encoding="utf-8"))
```

`pathlib` нь Windows болон Linux дээр ижил ажиллана. Мөрөөр зам барихаас
(`"data/" + ner`) илүү найдвартай.

### Жишээ програм

```python
import math
import random
from datetime import date

print("Квадрат язгуур:", math.sqrt(16))
print("Дугуйлах:", math.ceil(4.1), math.floor(4.9))   # дээш 5, доош 4
print("Пи:", round(math.pi, 4))   # round(x, 4) — 4 орон хүртэл дугуйрхайлна

print("---")

random.seed(42)  # ижил үр дүн гарахын тулд
print("Санамсаргүй сонголт:", random.choice(["алим", "лийр", "гүзээлзгэнэ"]))
print("1-100 хооронд:", random.randint(1, 100))

print("---")

print("Өнөөдөр:", date.today())
```
""",
            initial_code="""\
# 1. math модулийг, datetime-ээс date-г import хийнэ

GARAGUUD = ["Даваа", "Мягмар", "Лхагва", "Пүрэв", "Баасан", "Бямба", "Ням"]


def main():
    # 2. Хоёр огноог уншиж date.fromisoformat(...)-ээр date болгоно

    # 3. (tugsgul - ehlel).days — хоёр огнооны зөрүү өдрөөр

    # 4. «Өдөр», «Долоо хоног» (math.ceil), «Гараг» мөрүүдийг хэвлэнэ
    pass


if __name__ == "__main__":
    main()
""",
            exercise=ExerciseSpec(
                statement="""\
Хоёр огнооны хооронд хэдэн өдөр байгааг, дуусах өдөр нь гарагийн аль өдөр
болохыг олох програм бич. `datetime` модулийн `date` ба `math` модулийг
**import** хийж ашигла.

**Оролт:** хоёр мөр — эхлэх ба дуусах огноо, `YYYY-MM-DD` хэлбэртэй. Дуусах
огноо эхлэхээсээ өмнө биш.

**Гаралт:**

```text
Өдөр: <хоёр огнооны зөрүү өдрөөр>
Долоо хоног: <өдөр / 7-г дээш бүхэлчилсэн>
Гараг: <дуусах огнооны гараг>
```

Гарагийн нэрс: `Даваа`, `Мягмар`, `Лхагва`, `Пүрэв`, `Баасан`, `Бямба`, `Ням`.

**Туслах:** `date.fromisoformat("2024-05-01")` нь текстээс огноо үүсгэнэ;
`(b - a).days` нь хоёр огнооны зөрүүг өдрөөр өгнө; `d.weekday()` нь Даваа
гарагт `0`, Ням гарагт `6` буцаана; `math.ceil(x)` нь дээш бүхэлчилнэ.
""",
                tests=(
                    TestCaseSpec(
                        stdin="2024-03-01\n2024-12-25\n",
                        expected_output="Өдөр: 299\nДолоо хоног: 43\nГараг: Лхагва\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="2024-02-28\n2024-03-01\n",
                        expected_output="Өдөр: 2\nДолоо хоног: 1\nГараг: Баасан\n",
                    ),
                    TestCaseSpec(
                        stdin="2025-06-10\n2025-06-10\n",
                        expected_output="Өдөр: 0\nДолоо хоног: 0\nГараг: Мягмар\n",
                    ),
                    TestCaseSpec(
                        stdin="2023-12-25\n2024-01-01\n",
                        expected_output="Өдөр: 7\nДолоо хоног: 1\nГараг: Даваа\n",
                    ),
                    TestCaseSpec(
                        stdin="2000-01-01\n2026-09-27\n",
                        expected_output="Өдөр: 9766\nДолоо хоног: 1396\nГараг: Ням\n",
                    ),
                ),
                solution="""\
import math
from datetime import date

GARAGUUD = ["Даваа", "Мягмар", "Лхагва", "Пүрэв", "Баасан", "Бямба", "Ням"]


def main():
    ehlel = date.fromisoformat(input().strip())
    tugsgul = date.fromisoformat(input().strip())

    # Хоёр огноог хасахад timedelta гарна — .days нь өдрийн тоо
    udur = (tugsgul - ehlel).days
    print(f"Өдөр: {udur}")
    # math.ceil — дутуу долоо хоногийг бүтэнд тооцно
    print(f"Долоо хоног: {math.ceil(udur / 7)}")
    # weekday(): Даваа = 0, ..., Ням = 6
    print(f"Гараг: {GARAGUUD[tugsgul.weekday()]}")


if __name__ == "__main__":
    main()
""",
                tips="""\
- Файлын эхэнд `import math` ба `from datetime import date` гэж бич. Эхнийх нь
  `math.ceil(...)` гэж модулийн нэрээр, хоёр дахь нь шууд `date` гэж
  хэрэглэгдэнэ.
- `input()` текст буцаадаг — `date.fromisoformat(...)`-ээр огноо болгосны
  дараа л хасах боломжтой.
- Гарагийн нэрсийг жагсаалтад хадгалаад `weekday()`-ийн утгаар индексжүүл.
- Өндөр жил, оны заагийг `date` өөрөө зөв тооцдог — өдрийг гараар бүү бод.
  Хоёр огноо ижил байх тохиолдлыг ч бод.
- `if __name__ == "__main__":` блок нь файлыг шууд ажиллуулахад `main()`-г
  дуудна.
""",
            ),
        ),
    ],
)

COMPREHENSIONS = ModuleSpec(
    title="Модул 13 — Comprehension",
    description="Жагсаалт үүсгэх товч бичлэг.",
    lessons=[
        LessonSpec(
            title="List, dict, set comprehension",
            slug="comprehension",
            description="Давталтыг нэг мөрөнд.",
            duration=420,
            language=PY,
            content="""\
Comprehension нь давталтыг товч бичих Python-ийн онцлог арга.

### Өмнө нь

```python
kvadratuud = []
for too in range(5):
    kvadratuud.append(too ** 2)
```

### Comprehension-оор

```python
kvadratuud = [too ** 2 for too in range(5)]
# [0, 1, 4, 9, 16]
```

### Шүүлттэй

```python
tegsh = [too for too in range(10) if too % 2 == 0]
# [0, 2, 4, 6, 8]
```

Бүтэц нь: `[илэрхийлэл for элемент in дараалал if нөхцөл]`

### Dict ба set дээр

```python
urt = {ug: len(ug) for ug in ["алим", "лийр"]}
# {'алим': 4, 'лийр': 4}

ehnii_useg = {ug[0] for ug in ["алим", "арц", "лийр"]}
# {'а', 'л'}
```

### Хэзээ хэрэглэхгүй вэ?

Уншихад хэцүү болвол энгийн давталт бич:

```python
# Хэт нарийн — уншихад хэцүү
ur = [x * y for x in range(10) for y in range(10) if x != y and x + y > 5]
```

Богино нь үргэлж дээр гэсэн үг биш. **Уншигдах** нь чухал.

### Жишээ програм

```python
# Энгийн
kvadratuud = [too ** 2 for too in range(1, 6)]
print(kvadratuud)

# Шүүлттэй
tegsh = [too for too in range(20) if too % 2 == 0]
print(tegsh)

# Мөр боловсруулах — capitalize() нь эхний үсгийг том, бусдыг жижиг болгоно
ners = ["  бат ", "ЦЭЦЭГ", " Болд"]
tseverlesen = [ner.strip().capitalize() for ner in ners]
print(tseverlesen)

# Dict comprehension
urt = {ug: len(ug) for ug in ["алим", "гүзээлзгэнэ", "лийр"]}
print(urt)

# Set comprehension
ehnii_useg = {ug[0] for ug in ["алим", "арц", "лийр", "лууван"]}
print(ehnii_useg)
```
""",
            initial_code="""\
n = int(input())

# 1. List comprehension-оор n мөрийг уншиж split() хийнэ:
#    muruud = [... for _ in range(n)]

# 2. Dict comprehension: {нэр: int(оноо) ...}

# 3. List comprehension + if: 60 ба түүнээс дээш оноотой нэрс

# 4. Dict comprehension: оноо + 5 (100-аас хэтрэхгүй — min() ашигла)

# 5. Set comprehension: нэрсийн эхний үсэг — sorted() хийж хэвлэнэ
""",
            exercise=ExerciseSpec(
                statement="""\
Сурагчдын нэр, оноог уншаад comprehension ашиглан гурван мөр тайлан гарга.
List, dict, set comprehension-ийг тус бүр дор хаяж нэг удаа хэрэглээрэй.

**Оролт:** эхний мөрөнд `n` (`n ≥ 1`), дараагийн `n` мөр бүрт нэр (зайгүй,
давтагдахгүй) ба оноо (0-100 бүхэл тоо).

**Гаралт:**

```text
Тэнцсэн (<тоо>): <60 ба түүнээс дээш оноотой нэрс>
Бонустай: <нэр>=<оноо + 5, гэхдээ 100-аас ихгүй>, ...
Эхний үсэг: <нэрсийн давхардалгүй эхний үсгүүд>
```

Нэрсийг оролтын дарааллаар нь `", "`-ээр тусгаарлана. Эхний үсгүүдийг
`sorted()`-ийн дарааллаар эрэмбэлнэ. Тэнцсэн хүн байхгүй бол хоёр цэгийн
араас юу ч бичихгүй.
""",
                tests=(
                    TestCaseSpec(
                        stdin="4\nБат 85\nЦэцэг 58\nБолд 97\nДорж 60\n",
                        expected_output=(
                            "Тэнцсэн (3): Бат, Болд, Дорж\n"
                            "Бонустай: Бат=90, Цэцэг=63, Болд=100, Дорж=65\n"
                            "Эхний үсэг: Б, Д, Ц\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="2\nОюун 10\nӨлзий 59\n",
                        expected_output=(
                            "Тэнцсэн (0):\nБонустай: Оюун=15, Өлзий=64\nЭхний үсэг: О, Ө\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="1\nАнар 100\n",
                        expected_output="Тэнцсэн (1): Анар\nБонустай: Анар=100\nЭхний үсэг: А\n",
                    ),
                    TestCaseSpec(
                        stdin="5\nТөмөр 96\nТуяа 45\nҮүрцайх 60\nСарнай 59\nСүхээ 99\n",
                        expected_output=(
                            "Тэнцсэн (3): Төмөр, Үүрцайх, Сүхээ\n"
                            "Бонустай: Төмөр=100, Туяа=50, Үүрцайх=65, Сарнай=64, Сүхээ=100\n"
                            "Эхний үсэг: С, Т, Ү\n"
                        ),
                    ),
                ),
                solution="""\
n = int(input())

# List comprehension — n мөрийг нэг дор уншиж хуваана
muruud = [input().split() for _ in range(n)]

# Dict comprehension — нэр → оноо
onoo = {ner: int(o) for ner, o in muruud}

# Шүүлттэй list comprehension — оролтын дараалал хадгалагдана
tentssen = [ner for ner, o in onoo.items() if o >= 60]

# Dict comprehension — +5 оноо, гэхдээ 100-аас хэтрэхгүй
bonustai = {ner: min(o + 5, 100) for ner, o in onoo.items()}

# Set comprehension — давхардалгүй эхний үсгүүд
ehnii_useg = sorted({ner[0] for ner in onoo})

print(f"Тэнцсэн ({len(tentssen)}): {', '.join(tentssen)}")
print("Бонустай: " + ", ".join([f"{ner}={o}" for ner, o in bonustai.items()]))
print(f"Эхний үсэг: {', '.join(ehnii_useg)}")
""",
                tips="""\
- `[input().split() for _ in range(n)]` нь `n` мөрийг нэг мөр кодоор уншина.
- Шүүлт: `[... for ner, o in onoo.items() if o >= 60]`. Толь бичиг оруулсан
  дарааллаа хадгалдаг тул нэрсийн дараалал оролтынхтой ижил үлдэнэ.
- `min(o + 5, 100)` нь оноог 100-аас хэтрүүлэхгүй.
- Set-ийн дараалал тогтворгүй — хэвлэхийн өмнө заавал `sorted(...)` хий.
- `", ".join(...)` зөвхөн текстийн жагсаалт авна — `f"{ner}={o}"` гэж
  хөрвүүлсэн comprehension дамжуул.
""",
            ),
        ),
    ],
)

BEGINNER_PROJECTS = ModuleSpec(
    title="Модул 14 — Анхан шатны төслүүд",
    description="Үзсэнээ нэгтгэн бодит жижиг програм бичих.",
    lessons=[
        LessonSpec(
            title="Төсөл — Хийх зүйлсийн жагсаалт",
            slug="tusul-todo",
            description="Жагсаалт, толь бичиг, функцийг нэгтгэнэ.",
            duration=720,
            language=PY,
            content="""\
Одоо хүртэл үзсэн бүхнийг нэг дор ашиглая.

### Шаардлага

1. Даалгавар нэмэх
2. Дууссан гэж тэмдэглэх
3. Бүх даалгаврыг харуулах
4. Статистик харуулах

### Бүтцийн шийдвэр

Даалгавар бүрийг толь бичгээр илэрхийлнэ:

```python
{"id": 1, "garchig": "Python сурах", "duussan": False}
```

Тэдгээрийг жагсаалтад хадгална. Энэ бол **өгөгдлийн загвар** —
код бичихээс өмнө үүнийг шийдэх нь чухал.

### Функц бүр нэг ажил хийнэ

| Функц | Үүрэг |
|---|---|
| `daalgavar_nemeh` | Шинээр нэмнэ |
| `duusgah` | Тэмдэглэнэ |
| `haruulah` | Хэвлэнэ |
| `statistik` | Тоолно |

Ингэж хуваавал алдаа хайхад амархан, дараа нь өөрчлөхөд хялбар болно.

### Жишээ програм

Функцүүд `global` ашиглахгүй (Модул 7): жагсаалтыг параметрээр авч, шинэ
утгыг `return`-ээр буцаана. Жагсаалтад `append` хийвэл дуудсан газрын
жагсаалт өөрөө өөрчлөгдөнө — `b = a` хуулбар биш байсантай адил (Модул 4).

```python
def daalgavar_nemeh(daalgavruud, dugaar, garchig):
    daalgavruud.append({"id": dugaar, "garchig": garchig, "duussan": False})
    return dugaar + 1  # дараагийн дугаар


def duusgah(daalgavruud, daalgavar_id):
    for daalgavar in daalgavruud:
        if daalgavar["id"] == daalgavar_id:
            daalgavar["duussan"] = True
            return True
    return False


def haruulah(daalgavruud):
    if not daalgavruud:
        print("Даалгавар байхгүй байна.")
        return  # утгагүй return — функцээс шууд гарна
    for daalgavar in daalgavruud:
        temdeg = "✓" if daalgavar["duussan"] else "○"
        print(f"{temdeg} [{daalgavar['id']}] {daalgavar['garchig']}")


def statistik(daalgavruud):
    niit = len(daalgavruud)
    duussan = len([d for d in daalgavruud if d["duussan"]])
    huvi = duussan / niit * 100 if niit > 0 else 0
    print(f"{duussan}/{niit} дууссан ({huvi:.0f}%)")


daalgavruud = []
daraagiin_id = 1

daraagiin_id = daalgavar_nemeh(daalgavruud, daraagiin_id, "Python сурах")
daraagiin_id = daalgavar_nemeh(daalgavruud, daraagiin_id, "Дасгал хийх")
daraagiin_id = daalgavar_nemeh(daalgavruud, daraagiin_id, "Төсөл бичих")

duusgah(daalgavruud, 1)

haruulah(daalgavruud)
print("---")
statistik(daalgavruud)
```
""",
            initial_code="""\
def olokh(daalgavruud, dugaar):
    # TODO: id нь dugaar-тай тэнцүү даалгаврыг (толь бичиг) буцаана,
    #       олдохгүй бол None
    return None


def haruulah(daalgavruud):
    # TODO: хоосон бол «Жагсаалт хоосон», эс бөгөөс мөр бүрийг
    #       «[x] #1 ...» эсвэл «[ ] #1 ...» хэлбэрээр хэвлэнэ
    pass


def main():
    daalgavruud = []  # {"id": 1, "garchig": "...", "duussan": False}
    daraagiin_id = 1

    while True:
        mur = input().strip()
        # TODO: мөрийг команд ба утга болгон салгана — mur.split(" ", 1)
        # TODO: QUIT → «Баяртай!» хэвлээд break
        # TODO: ADD, DONE, DEL, LIST, STATS командуудыг гүйцэтгэнэ
        # TODO: бусад үед «Үл мэдэгдэх команд: ...»
        break


if __name__ == "__main__":
    main()
""",
            exercise=ExerciseSpec(
                statement="""\
Командаар удирддаг «Хийх зүйлсийн жагсаалт» програм бич. Даалгавар бүр
дугаартай: 1-ээс эхэлж, шинээр нэмэх бүрд 1-ээр өснө; устгасан дугаар дахин
ашиглагдахгүй. Мөр бүрт нэг команд ирнэ:

- `ADD <текст>` → шинэ даалгавар нэмээд `Нэмэгдлээ: #<дугаар> <текст>`
- `DONE <дугаар>` → дууссан гэж тэмдэглээд `Дууслаа: #<дугаар>`; аль хэдийн
  дууссан бол `Аль хэдийн дууссан: #<дугаар>`
- `DEL <дугаар>` → устгаад `Устлаа: #<дугаар>`
- `LIST` → даалгавар бүрийг нэмсэн дарааллаар `[x] #<дугаар> <текст>`
  (дууссан) эсвэл `[ ] #<дугаар> <текст>`; хоосон бол `Жагсаалт хоосон`
- `STATS` → `<дууссан>/<нийт> дууссан`
- `QUIT` → `Баяртай!` хэвлээд програм дуусна (цаашдын мөрийг уншихгүй)

`DONE`, `DEL`-ийн дугаар бүхэл тоо биш бол `Буруу дугаар: <утга>`, ийм
дугаартай даалгавар байхгүй бол `Олдсонгүй: #<дугаар>` гэж хэвлэнэ. Өөр
команд ирвэл `Үл мэдэгдэх команд: <команд>` (том, жижиг үсгийг ялгана).

**Оролт:** нэг мөрөнд нэг команд. Оролтод `QUIT` заавал байна.

**Гаралт:** команд бүрийн хариуг дээрх форматаар хэвлэнэ.
""",
                tests=(
                    TestCaseSpec(
                        stdin="ADD Талх авах\nADD Python дасгал хийх\nDONE 1\nLIST\nSTATS\nQUIT\n",
                        expected_output=(
                            "Нэмэгдлээ: #1 Талх авах\n"
                            "Нэмэгдлээ: #2 Python дасгал хийх\n"
                            "Дууслаа: #1\n"
                            "[x] #1 Талх авах\n"
                            "[ ] #2 Python дасгал хийх\n"
                            "1/2 дууссан\n"
                            "Баяртай!\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="LIST\nDONE 5\nADD Ном унших\nDEL 1\nLIST\nQUIT\n",
                        expected_output=(
                            "Жагсаалт хоосон\n"
                            "Олдсонгүй: #5\n"
                            "Нэмэгдлээ: #1 Ном унших\n"
                            "Устлаа: #1\n"
                            "Жагсаалт хоосон\n"
                            "Баяртай!\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin=(
                            "STATS\n"
                            "ADD Цэвэрлэгээ хийх\n"
                            "ADD Эмээ рүү залгах\n"
                            "ADD Гэрийн даалгавар\n"
                            "DEL 2\n"
                            "ADD Спорт заал\n"
                            "DONE 3\n"
                            "DONE 3\n"
                            "DONE abc\n"
                            "LIST\n"
                            "STATS\n"
                            "remove 1\n"
                            "QUIT\n"
                        ),
                        expected_output=(
                            "0/0 дууссан\n"
                            "Нэмэгдлээ: #1 Цэвэрлэгээ хийх\n"
                            "Нэмэгдлээ: #2 Эмээ рүү залгах\n"
                            "Нэмэгдлээ: #3 Гэрийн даалгавар\n"
                            "Устлаа: #2\n"
                            "Нэмэгдлээ: #4 Спорт заал\n"
                            "Дууслаа: #3\n"
                            "Аль хэдийн дууссан: #3\n"
                            "Буруу дугаар: abc\n"
                            "[ ] #1 Цэвэрлэгээ хийх\n"
                            "[x] #3 Гэрийн даалгавар\n"
                            "[ ] #4 Спорт заал\n"
                            "1/3 дууссан\n"
                            "Үл мэдэгдэх команд: remove\n"
                            "Баяртай!\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="QUIT\nADD Энэ мөр уншигдахгүй\nLIST\n",
                        expected_output="Баяртай!\n",
                    ),
                    TestCaseSpec(
                        stdin=(
                            "ADD 3 ном унших\n"
                            "ADD Кино үзэх\n"
                            "DONE 1\n"
                            "DEL 1\n"
                            "DONE 1\n"
                            "DEL 1\n"
                            "DEL 2\n"
                            "ADD Алхах\n"
                            "LIST\n"
                            "STATS\n"
                            "QUIT\n"
                        ),
                        expected_output=(
                            "Нэмэгдлээ: #1 3 ном унших\n"
                            "Нэмэгдлээ: #2 Кино үзэх\n"
                            "Дууслаа: #1\n"
                            "Устлаа: #1\n"
                            "Олдсонгүй: #1\n"
                            "Олдсонгүй: #1\n"
                            "Устлаа: #2\n"
                            "Нэмэгдлээ: #3 Алхах\n"
                            "[ ] #3 Алхах\n"
                            "0/1 дууссан\n"
                            "Баяртай!\n"
                        ),
                    ),
                ),
                solution="""\
def olokh(daalgavruud, dugaar):
    # Дугаараар нь хайна — олдохгүй бол None
    for daalgavar in daalgavruud:
        if daalgavar["id"] == dugaar:
            return daalgavar
    return None


def haruulah(daalgavruud):
    if not daalgavruud:
        print("Жагсаалт хоосон")
        return
    for daalgavar in daalgavruud:
        temdeg = "x" if daalgavar["duussan"] else " "
        print(f"[{temdeg}] #{daalgavar['id']} {daalgavar['garchig']}")


def main():
    daalgavruud = []
    daraagiin_id = 1  # устгасан дугаарыг дахин ашиглахгүй

    while True:
        # Эхний үгийг команд, үлдсэнийг утга болгон салгана
        hesguud = input().strip().split(" ", 1)
        komand = hesguud[0]
        utga = hesguud[1] if len(hesguud) > 1 else ""

        if komand == "QUIT":
            print("Баяртай!")
            break
        elif komand == "ADD":
            daalgavruud.append({"id": daraagiin_id, "garchig": utga, "duussan": False})
            print(f"Нэмэгдлээ: #{daraagiin_id} {utga}")
            daraagiin_id += 1
        elif komand == "LIST":
            haruulah(daalgavruud)
        elif komand == "STATS":
            duussan = len([d for d in daalgavruud if d["duussan"]])
            print(f"{duussan}/{len(daalgavruud)} дууссан")
        elif komand == "DONE" or komand == "DEL":
            # Дугаар тоо биш бол програм унахгүй — алдааг барина
            try:
                dugaar = int(utga)
            except ValueError:
                print(f"Буруу дугаар: {utga}")
                continue
            daalgavar = olokh(daalgavruud, dugaar)
            if daalgavar is None:
                print(f"Олдсонгүй: #{dugaar}")
            elif komand == "DEL":
                daalgavruud.remove(daalgavar)
                print(f"Устлаа: #{dugaar}")
            elif daalgavar["duussan"]:
                print(f"Аль хэдийн дууссан: #{dugaar}")
            else:
                daalgavar["duussan"] = True
                print(f"Дууслаа: #{dugaar}")
        else:
            print(f"Үл мэдэгдэх команд: {komand}")


if __name__ == "__main__":
    main()
""",
                tips="""\
- Өгөгдлийн загвараа эхлээд шийд: даалгавар бүр
  `{"id": 1, "garchig": "...", "duussan": False}` толь бичиг, бүгд нэг жагсаалтад.
- `mur.split(" ", 1)` нь зөвхөн эхний зай дээр хуваана — командыг текстээс нь
  салгахад тохиромжтой, текст доторх зай хадгалагдана.
- `while True:` давталтаас `QUIT` дээр `break` хий. Дугаарыг `int()` болгохдоо
  `try`/`except ValueError` ашигла.
- Хайх, хэвлэх ажлыг тусдаа функцэд гарга — `global`-ын оронд жагсаалтыг
  параметрээр дамжуул.
- Дараагийн дугаарыг тусдаа тоолуураар хөтөл: `len(daalgavruud) + 1` гэж
  бодвол устгасны дараа дугаар давхардана.
""",
            ),
        ),
        LessonSpec(
            title="Төсөл — Текстийн шинжилгээ",
            slug="tusul-tekst-shinjilgee",
            description="Мөр, толь бичиг, эрэмбэлэлтийг хослуулна.",
            duration=720,
            language=PY,
            content="""\
Текстээс үг тоолж, хамгийн их давтагдсаныг олно.

### Алхмууд

1. Текстийг жижиг үсэг болгоно
2. Цэг таслалыг арилгана
3. Үгээр хуваана
4. Үг бүрийг тоолно
5. Эрэмбэлж хэвлэнэ

### Тоолох хоёр арга

Гараар:

```python
toolol = {}
for ug in ugs:
    toolol[ug] = toolol.get(ug, 0) + 1
```

`get(ug, 0)` нь түлхүүр байхгүй бол 0 буцаана — `KeyError`-оос хамгаална.

Эсвэл бэлэн хэрэгслээр:

```python
from collections import Counter
toolol = Counter(ugs)
print(toolol.most_common(3))
```

`Counter` нь яг энэ ажилд зориулагдсан. Стандарт санг мэдэх нь
кодыг богиносгодог.

### Эрэмбэлэх

`sorted()`-ийн `key=` параметрт **функцийн нэрийг** (хаалтгүй) өгнө.
`sorted` элемент бүрийг тэр функцэд дамжуулж, буцаасан утгаар нь жишнэ:

```python
def toogoor(hos):
    return hos[1]      # ("python", 3) хосын тоо

erembelsen = sorted(toolol.items(), key=toogoor, reverse=True)
```

Функц tuple буцаавал эхний утгаар нь, тэнцвэл дараагийнхаар нь жишинэ:

```python
def erembe(hos):
    # Тоогоор буурах (хасах тэмдэг их тоог түрүүлүүлнэ), тэнцвэл үгээр өсөх
    return (-hos[1], hos[0])

erembelsen = sorted(toolol.items(), key=erembe)
```

Ийм богино функцийг `lambda`-аар нэг мөрөнд бичихийг Модул 17-д үзнэ.

### Жишээ програм

```python
from collections import Counter

tekst = \"\"\"
Python бол сурахад хялбар хэл. Python дээр вэб сайт хийж болно.
Python нь өгөгдлийн шинжилгээнд ч ашиглагддаг. Хялбар бөгөөд хүчирхэг.
\"\"\"

# 1-3. Цэвэрлээд үгээр хуваах
tseverlesen = tekst.lower()
for temdeg in ".,!?":
    tseverlesen = tseverlesen.replace(temdeg, " ")
ugs = tseverlesen.split()

print("Нийт үг:", len(ugs))
print("Өвөрмөц үг:", len(set(ugs)))

print("---")

# 4-5. Тоолж эрэмбэлэх
toolol = Counter(ugs)
for ug, too in toolol.most_common(5):
    print(f"{ug:<15} {'█' * too} {too}")
```
""",
            initial_code="""\
TSEG_TASLAL = ".,!?;:"


def ugs_salgah(mur):
    # TODO: lower() хийж, TSEG_TASLAL-ын тэмдэгт бүрийг зайгаар replace()
    #       хийгээд split()-ийн үр дүнг буцаана
    return []


def erembe(hos):
    # TODO: (үг, тоо) хосоос эрэмбийн түлхүүр буцаана — тоогоор буурах,
    #       тэнцвэл үгээр өсөх: (-тоо, үг)
    return hos


def main():
    n = int(input())
    muruud = [input() for _ in range(n)]

    # 1. Мөр бүрийн үгсийг ugs_salgah()-аар нэг жагсаалтад цуглуулна

    # 2. Үг бүрийг толь бичгээр тоолно: toolol.get(ug, 0) + 1

    # 3. «Мөр», «Үг», «Өвөрмөц үг», «Хамгийн урт үг» мөрүүдийг хэвлэнэ

    # 4. «Топ 3:» — sorted(toolol.items(), key=erembe)[:3]


if __name__ == "__main__":
    main()
""",
            exercise=ExerciseSpec(
                statement="""\
Өгөгдсөн текстэд энгийн шинжилгээ хий: мөр, үгийг тоолж, хамгийн их
давтагдсан үгсийг ол.

Үгийг ялгахдаа текстийг **жижиг үсэг** болгож, `. , ! ? ; :` тэмдэгтүүдийг
зайгаар солиод `split()` хийнэ.

**Оролт:** эхний мөрөнд `n`, дараагийн `n` мөр нь текст. Хоосон мөр байж
болно. Нийт текстэд дор хаяж нэг үг бий.

**Гаралт:**

```text
Мөр: <хоосон биш мөрийн тоо>
Үг: <нийт үгийн тоо>
Өвөрмөц үг: <давхардалгүй үгийн тоо>
Хамгийн урт үг: <хамгийн урт үг>
Топ 3:
<үг> <тоо>
...
```

- Хамгийн урт үг хэд байвал текстэд **түрүүлж** гарсныг нь сонгоно.
- «Топ 3» нь давтамжаар нь буурахаар, давтамж тэнцвэл үгийг өөрийг нь
  өсөхөөр (`sorted()`-ийн анхдагч дарааллаар) эрэмбэлсэн эхний 3 үг.
  Өвөрмөц үг 3-аас цөөн бол байгаа хэрээр нь хэвлэнэ.
""",
                tests=(
                    TestCaseSpec(
                        stdin=(
                            "3\n"
                            "Python бол сурахад хялбар хэл.\n"
                            "Python дээр вэб сайт хийж болно!\n"
                            "Python бол хүчирхэг, хялбар.\n"
                        ),
                        expected_output=(
                            "Мөр: 3\n"
                            "Үг: 15\n"
                            "Өвөрмөц үг: 11\n"
                            "Хамгийн урт үг: хүчирхэг\n"
                            "Топ 3:\n"
                            "python 3\n"
                            "бол 2\n"
                            "хялбар 2\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="4\n\nСайн байна уу?\n   \nсайн, САЙН!\n",
                        expected_output=(
                            "Мөр: 2\n"
                            "Үг: 5\n"
                            "Өвөрмөц үг: 3\n"
                            "Хамгийн урт үг: байна\n"
                            "Топ 3:\n"
                            "сайн 3\n"
                            "байна 1\n"
                            "уу 1\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="1\nМедлег\n",
                        expected_output=(
                            "Мөр: 1\nҮг: 1\nӨвөрмөц үг: 1\nХамгийн урт үг: медлег\nТоп 3:\nмедлег 1\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="2\nнэг хоёр гурав дөрөв\nтав долоо найм ес\n",
                        expected_output=(
                            "Мөр: 2\n"
                            "Үг: 8\n"
                            "Өвөрмөц үг: 8\n"
                            "Хамгийн урт үг: гурав\n"
                            "Топ 3:\n"
                            "гурав 1\n"
                            "долоо 1\n"
                            "дөрөв 1\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="2\nТийм; тийм: ҮГҮЙ!\nүгүй?? тийм... магадгүй\n",
                        expected_output=(
                            "Мөр: 2\n"
                            "Үг: 6\n"
                            "Өвөрмөц үг: 3\n"
                            "Хамгийн урт үг: магадгүй\n"
                            "Топ 3:\n"
                            "тийм 3\n"
                            "үгүй 2\n"
                            "магадгүй 1\n"
                        ),
                    ),
                ),
                solution="""\
TSEG_TASLAL = ".,!?;:"


def ugs_salgah(mur):
    # Жижиг үсэг болгож, цэг таслалыг зайгаар солиод үгээр хуваана
    mur = mur.lower()
    for temdeg in TSEG_TASLAL:
        mur = mur.replace(temdeg, " ")
    return mur.split()


def erembe(hos):
    # Тоогоор буурах (хасах тэмдгээр), тэнцвэл үгээр өсөх
    return (-hos[1], hos[0])


def main():
    n = int(input())
    muruud = [input() for _ in range(n)]

    ugs = []
    for mur in muruud:
        ugs.extend(ugs_salgah(mur))

    # Үг бүрийг тоолно — get(ug, 0) нь KeyError-оос хамгаална
    toolol = {}
    for ug in ugs:
        toolol[ug] = toolol.get(ug, 0) + 1

    # Хамгийн урт үг — тэнцвэл түрүүлж гарсан нь үлдэнэ
    urt = ugs[0]
    for ug in ugs:
        if len(ug) > len(urt):
            urt = ug

    print(f"Мөр: {len([m for m in muruud if m.strip()])}")
    print(f"Үг: {len(ugs)}")
    print(f"Өвөрмөц үг: {len(toolol)}")
    print(f"Хамгийн урт үг: {urt}")
    print("Топ 3:")
    # key=erembe — функцийн нэрийг хаалтгүй дамжуулна
    erembelsen = sorted(toolol.items(), key=erembe)
    for ug, too in erembelsen[:3]:
        print(f"{ug} {too}")


if __name__ == "__main__":
    main()
""",
                tips="""\
- Ажлаа жижиг функцэд хуваа: нэг мөрийг цэвэрлээд үгсийн жагсаалт буцаадаг
  функц бичвэл үндсэн хэсэг богино, ойлгомжтой болно.
- Тоолохдоо `toolol[ug] = toolol.get(ug, 0) + 1` — шинэ үг дээр `KeyError`
  гарахгүй.
- Хоёр түвшний эрэмбэ: `erembe` функц `(-hos[1], hos[0])` tuple буцаавал
  `sorted(..., key=erembe)` эхлээд тоогоор буурахаар, тэнцвэл үгээр өсөхөөр
  эрэмбэлнэ. `Counter.most_common()` тэнцүү үед оролтын дарааллыг хадгалдаг
  тул энд шууд тохирохгүй.
- Хамгийн уртыг олохдоо `>` ашигла (`>=` биш) — тэгвэл тэнцүү урттай үед
  эхнийх нь үлдэнэ.
- «Мөр»-ийг тоолохдоо зөвхөн зайтай мөрийг ч хоосонд тооц — `mur.strip()`.
""",
            ),
        ),
    ],
)

APPLIED_MODULES = [
    FUNCTIONS,
    STRINGS,
    FILES,
    JSON_MODULE,
    ERRORS,
    MODULES,
    COMPREHENSIONS,
    BEGINNER_PROJECTS,
]
