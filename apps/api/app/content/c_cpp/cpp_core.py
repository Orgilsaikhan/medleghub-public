"""Модул 16-19 — Мөр, лавлагаа, OOP, цуглуулга.

C++ -ийн жинхэнэ давуу талууд. Энд сурсан зүйлс нь C дээр гараар хийх
шаардлагатай байсан ажлыг бүрэн орлоно.
"""

from app.content.types import ExerciseSpec, LessonSpec, ModuleSpec, TestCaseSpec
from app.models.enums import LessonLanguage

CPP = LessonLanguage.CPP

STRINGS = ModuleSpec(
    title="Модул 16 — Мөр (std::string)",
    description="Санах ойн зовлонгүй текст боловсруулалт.",
    lessons=[
        LessonSpec(
            title="C-ийн мөр ба std::string",
            slug="c-mur-ba-std-string",
            description="Хоёрын ялгаа, яагаад std::string сонгох вэ.",
            duration=420,
            language=CPP,
            content="""\
### C-ийн мөрийн бэрхшээл

```c
char ner[50];
strcpy(ner, "Бат");
strcat(ner, " Болд");
```

Асуудлууд:

- Хэмжээг **урьдчилан** таах шаардлагатай
- Хэтэрвэл санах ой халина — аюулгүй байдлын цоорхой
- Урт олох нь `O(n)` — тэглэх тэмдэгтийг хайна
- Харьцуулахад `strcmp` хэрэгтэй

### `std::string`

Модул 12-т `std::string`-ийг текст хадгалах, унших, хэвлэхэд ашигласан.
Одоо түүний бусад боломжийг дэлгэрэнгүй үзье.

```cpp
#include <string>

std::string ner = "Бат";
ner += " Болд";          // төгсгөлд нь залгана
```

- Хэмжээгээ **өөрөө** удирдана
- Санах ой халих боломжгүй
- `size()` нь `O(1)`
- `==`, `<`, `+` операторууд ажиллана

```cpp
if (ner == "Бат Болд") {        // strcmp хэрэггүй
    std::cout << "Тэнцүү\\n";
}
```

### Үүсгэх

```cpp
std::string a;                   // хоосон
std::string b = "текст";
std::string c(5, 'x');           // "xxxxx"
std::string d = b;               // хуулбар
```

### Урт ба хоосон эсэх

```cpp
ner.size();      // тэмдэгтийн тоо
ner.length();    // ЯГ ижил зүйл
ner.empty();     // хоосон эсэх
```

`size() == 0`-ийн оронд `empty()` бич — зорилго нь тодорхой.

### Хандах

```cpp
ner[0];           // хязгаар ШАЛГАХГҮЙ
ner.at(0);        // хязгаараас хэтэрвэл онцгой байдал шиднэ
ner.front();
ner.back();
```

### C-ийн функцтэй холбох

Хуучин C API нь `const char *` шаарддаг:

```cpp
std::string ner = "Бат";
printf("%s\\n", ner.c_str());
```

`c_str()` нь тэглэх тэмдэгттэй C мөр буцаана.

> `c_str()`-ийн буцаасан заагчийг **удаан бүү хадгал**. `std::string`
> өөрчлөгдвөл тэр заагч хүчингүй болно.

### Кирилл үсэг ба `size()`

```cpp
std::string ner = "Бат";
std::cout << ner.size();     // 3 БИШ — 6
```

UTF-8-д кирилл үсэг тус бүр **2 байт** эзэлнэ. `size()` нь **байтын**
тоог өгдөг, тэмдэгтийн тоог биш. Тэмдэгтээр тоолох нь илүү нарийн ажил
шаардана.

### Жишээ програм

```cpp
#include <iostream>
#include <string>
#include <cstdio>

int main() {
    // C-ийн мөр — хэмжээг урьдчилан таах ёстой
    char c_ner[50] = "Бат";

    // std::string — хэмжээгээ өөрөө удирдана
    std::string ner = "Бат";
    ner += " Болд";
    ner += ", Улаанбаатар";

    std::cout << "Нэр: " << ner << "\\n";
    std::cout << "Байт: " << ner.size() << "\\n";
    std::cout << "Хоосон эсэх: " << (ner.empty() ? "тийм" : "үгүй") << "\\n\\n";

    // Операторууд шууд ажиллана — strcmp хэрэггүй
    std::string a = "Бат";
    std::string b = "Бат";

    if (a == b) {
        std::cout << "a ба b тэнцүү\\n";
    }

    // Нэмэх нь шинэ мөр үүсгэнэ
    std::string buten = a + " " + "Болд";
    std::cout << "Нийлүүлсэн: " << buten << "\\n\\n";

    // Хандах
    std::string text = "MedlegHub";
    std::cout << "Эхний:   " << text.front() << "\\n";
    std::cout << "Сүүлчийн: " << text.back() << "\\n";
    std::cout << "at(2):   " << text.at(2) << "\\n\\n";

    // C API-тай холбох
    printf("c_str(): %s\\n", ner.c_str());
    printf("C мөр:   %s\\n", c_ner);

    return 0;
}
```
""",
            initial_code="""\
#include <iostream>
#include <string>

int main() {
    std::string nuuts_ug;
    std::string davtan;

    // 1. Хоёр мөрийг std::getline-аар уншина (зай агуулж болно)

    // 2. Дүрмүүдийг дарааллаар нь шалгана:
    //    хоосон эсэх -> 8-аас богино эсэх -> хоёр мөр ижил эсэх

    // 3. Эхний таарсан дүрмийн мессежийг хэвлэнэ

    return 0;
}
""",
            exercise=ExerciseSpec(
                statement="""\
Бүртгэлийн хуудас шинэ нууц үгийг **хоёр удаа** оруулуулдаг. Хоёр мөрийг
уншаад нууц үгийг хадгалж болох эсэхийг шалгадаг програм бич. C-ийн
`strcmp`, `strlen`-ийн оронд `std::string`-ийн `==`, `size()`, `empty()`-г
ашигла.

**Оролт:** хоёр мөр — нууц үг ба түүнийг давтсан нь. Мөр нь латин үсэг,
тоо, тэмдэгт, **зай** агуулж болно.

**Гаралт:** дараах дүрмийг **дарааллаар нь** шалгаж, эхний таарсан
мессежийг ганц мөрөөр хэвлэ (`N` — эхний мөрийн тэмдэгтийн тоо):

1. Эхний мөр хоосон бол `Нууц үг хоосон байна.`
2. 8-аас богино бол `Хэт богино: N тэмдэгт, дор хаяж 8 хэрэгтэй.`
3. Хоёр мөр ялгаатай бол `Нууц үгнүүд таарахгүй байна.`
4. Бусад үед `Амжилттай! Нууц үг N тэмдэгттэй.`

«Нууц үгээ оруулна уу:» гэх мэт асуулт **бүү хэвлэ** — шалгагч зөвхөн
гаралтыг харьцуулна.

Зөвлөгөө: зай агуулсан мөрийг `std::cin >>` биш `std::getline` уншина.
Том, жижиг үсэг ялгаатай — `abc` ба `ABC` өөр нууц үг.
""",
                tests=(
                    TestCaseSpec(
                        stdin="medleghub2026\nmedleghub2026\n",
                        expected_output="Амжилттай! Нууц үг 13 тэмдэгттэй.\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="abc12\nabc12\n",
                        expected_output="Хэт богино: 5 тэмдэгт, дор хаяж 8 хэрэгтэй.\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="Password1\npassword1\n",
                        expected_output="Нууц үгнүүд таарахгүй байна.\n",
                    ),
                    TestCaseSpec(
                        stdin="\n\n",
                        expected_output="Нууц үг хоосон байна.\n",
                    ),
                    TestCaseSpec(
                        stdin="12345678\n12345678\n",
                        expected_output="Амжилттай! Нууц үг 8 тэмдэгттэй.\n",
                    ),
                    TestCaseSpec(
                        stdin="my secret pass\nmy secret pass\n",
                        expected_output="Амжилттай! Нууц үг 14 тэмдэгттэй.\n",
                    ),
                    TestCaseSpec(
                        stdin="my secret pass\nmy secret\n",
                        expected_output="Нууц үгнүүд таарахгүй байна.\n",
                    ),
                    TestCaseSpec(
                        stdin="short\nlonger text\n",
                        expected_output="Хэт богино: 5 тэмдэгт, дор хаяж 8 хэрэгтэй.\n",
                    ),
                ),
                solution="""\
#include <iostream>
#include <string>

int main() {
    std::string nuuts_ug;
    std::string davtan;
    // getline нь мөрийг зайтай нь бүтнээр уншина (cin >> зай дээр зогсоно)
    std::getline(std::cin, nuuts_ug);
    std::getline(std::cin, davtan);

    // Дүрмүүдийг дарааллаар нь шалгана — зөвхөн эхний таарсан нь хэвлэгдэнэ.
    // Хоосон мөр ч бас 8-аас богино тул empty() хамгийн түрүүнд байна.
    if (nuuts_ug.empty()) {
        std::cout << "Нууц үг хоосон байна.\\n";
    } else if (nuuts_ug.size() < 8) {
        // size() нь уртыг шууд өгнө — strlen шиг тоолж гүйхгүй
        std::cout << "Хэт богино: " << nuuts_ug.size() << " тэмдэгт, дор хаяж 8 хэрэгтэй.\\n";
    } else if (nuuts_ug != davtan) {
        // std::string-ийг == / != -ээр шууд харьцуулна, strcmp хэрэггүй
        std::cout << "Нууц үгнүүд таарахгүй байна.\\n";
    } else {
        std::cout << "Амжилттай! Нууц үг " << nuuts_ug.size() << " тэмдэгттэй.\\n";
    }

    return 0;
}
""",
                tips="""\
- Хоёр мөрийг `std::getline(std::cin, s)`-ээр унш. `std::cin >>` нь эхний
  зай дээр зогсдог тул зай агуулсан нууц үгийг тасалчихна.
- Дүрмүүдийг `if / else if / else` гинжээр **яг өгөгдсөн дарааллаар** шалга:
  хоосон → богино → ялгаатай → амжилттай. Жишээ нь богино **бөгөөд**
  таарахгүй нууц үгэнд зөвхөн «Хэт богино» мессеж гарна.
- `std::string`-ийн хэрэгслүүдийг ашигла: хоосон эсэхийг `empty()`, уртыг
  `size()`, тэнцүү эсэхийг `==` / `!=`. `strlen`, `strcmp` хэрэггүй.
- Хязгаарын тохиолдлуудыг анхаар: хоосон мөр, яг 8 тэмдэгттэй нууц үг
  (хүчинтэй — `< 8` гэж шалга), зөвхөн том жижиг үсгээр ялгаатай мөрүүд
  (`==` тэднийг өөр гэж үзнэ).
- Мессежийг цэг, таслал, зайтай нь яг хуулж бич, «Нууц үгээ оруулна уу»
  гэх мэт асуулт бүү хэвлэ.
""",
            ),
        ),
        LessonSpec(
            title="Мөрийн үйлдлүүд",
            slug="string-uildluud",
            description="Хайх, тасдах, солих, хуваах.",
            duration=450,
            language=CPP,
            content="""\
### Хайх

```cpp
std::string text = "Сайн байна уу";

std::size_t bairlal = text.find("байна");

if (bairlal != std::string::npos) {
    std::cout << "Олдлоо: " << bairlal << "\\n";
}
```

`find` нь олдсон байрлалыг (эхлэх индексийг) `std::size_t` төрлөөр буцаана —
энэ нь C-ийн `sizeof`-оос танил `size_t`: хэмжээ, байрлалд зориулсан
**тэмдэггүй** (сөрөг болдоггүй) бүхэл төрөл.

Олдохгүй бол `std::string::npos` буцаана — энэ нь **маш том тэмдэггүй
тоо**, `-1` биш. Тиймээс:

```cpp
if (text.find("x") != std::string::npos) { }    // зөв
if (text.find("x") >= 0) { }                    // ҮРГЭЛЖ ҮНЭН — буруу
```

### Хэсэг тасдах

```cpp
std::string heseg = text.substr(5, 5);     // 5 дахь тэмдэгтээс 5 ширхэг
std::string tugsgul = text.substr(5);      // 5-аас төгсгөл хүртэл
```

### Өөрчлөх

```cpp
text.insert(0, "Өө, ");        // 0 дэх байрлалд оруулна
text.erase(0, 4);              // 0-ээс эхлэх 4 тэмдэгтийг устгана
text.replace(0, 4, "Шинэ");    // 0-ээс эхлэх 4 тэмдэгтийг сольно
text.clear();                  // хоосон болгоно
```

### Хуваах

C++ -д бэлэн `split` **байхгүй**. `std::stringstream` ашиглан хэсэг хэсгээр
нь уншина:

```cpp
#include <sstream>

std::string jagsaalt = "алим,гадил,интоор";
std::stringstream urgats(jagsaalt);
std::string heseg;

while (std::getline(urgats, heseg, ',')) {
    std::cout << heseg << "\\n";
}
```

`std::stringstream` нь мөрийг `std::cin` шиг **урсгал** болгож уншуулна.
`std::getline`-ийн гурав дахь параметр нь мөр таслалын оронд зогсох тэмдэгт —
энд `,`. Хэсгүүдийг хадгалах шаардлагатай бол Модул 19-д үзэх `std::vector`
руу нэмнэ.

### Нийлүүлэх

```cpp
std::stringstream ss;
ss << "Нас: " << 20 << ", дундаж: " << 87.5;
std::string ur = ss.str();
```

`ss`-т `std::cout` руу бичдэг шигээ бичээд, `ss.str()`-ээр бүгдийг нэг
`std::string` болгож авна. Тоог текст болгоход тохиромжтой.

### Том жижиг үсэг

```cpp
#include <cctype>

for (char &c : text) {
    c = std::toupper(static_cast<unsigned char>(c));
}
```

`std::toupper` нь нэг латин жижиг үсгийг том болгоно (`std::tolower` —
эсрэгээр). `char &c` тул мөр доторх тэмдэгт өөрөө өөрчлөгдөнө (Модул 14).

> Энэ нь зөвхөн **ASCII** дээр ажиллана. Кирилл үсэгт ажиллахгүй —
> UTF-8 дэх олон байтын тэмдэгтийг байт тус бүрээр нь боловсруулж
> болохгүй.

### Хоёр талын зайг авах

```cpp
std::string tseverleh(std::string s) {
    const std::size_t ehlel = s.find_first_not_of(" \\t");
    if (ehlel == std::string::npos) return "";

    const std::size_t tugsgul = s.find_last_not_of(" \\t");
    return s.substr(ehlel, tugsgul - ehlel + 1);
}
```

`find_first_not_of(" \\t")` нь зай, таб **биш** эхний тэмдэгтийн байрлалыг,
`find_last_not_of` нь сүүлчийнхийг олно. Тэдгээрийн хоорондох хэсэг нь
цэвэрлэсэн текст.

### Жишээ програм

```cpp
#include <cctype>
#include <iostream>
#include <sstream>
#include <string>

int main() {
    std::string text = "Сайн байна уу, MedlegHub";

    // Хайх — олдохгүй бол npos, -1 БИШ
    std::size_t bairlal = text.find("MedlegHub");
    if (bairlal != std::string::npos) {
        std::cout << "«MedlegHub» " << bairlal << " дэх байтаас эхэлж байна\\n";
    }

    if (text.find("Python") == std::string::npos) {
        std::cout << "«Python» олдсонгүй\\n\\n";
    }

    // Тасдах
    std::cout << "substr(0, 8): " << text.substr(0, 8) << "\\n";

    // Солих — эх мөрийг өөрчилнө
    std::string huulbar = text;
    huulbar.replace(0, 8, "Мэндчилгээ");
    std::cout << "Сольсон:      " << huulbar << "\\n\\n";

    // Хуваах — C++ -д бэлэн split байхгүй
    std::string jagsaalt = "алим,гадил,интоор,усан үзэм";
    std::stringstream urgats(jagsaalt);
    std::string jims;
    int too = 0;

    std::cout << "Жимснүүд:\\n";
    while (std::getline(urgats, jims, ',')) {
        std::cout << "  - " << jims << "\\n";
        too++;
    }
    std::cout << "Нийт " << too << " жимс\\n";

    // stringstream-ээр нийлүүлэх — тоог текст болгоно
    std::stringstream ss;
    ss << "Нас: " << 20 << ", дундаж: " << 87.5;
    std::cout << "\\nНийлүүлсэн: " << ss.str() << "\\n";

    // Том үсэг — зөвхөн латин үсэгт ажиллана
    std::string ner = "MedlegHub";
    for (char &c : ner) {
        c = std::toupper(static_cast<unsigned char>(c));
    }
    std::cout << "Том үсгээр:   " << ner << "\\n";

    return 0;
}
```
""",
            initial_code="""\
#include <iostream>
#include <string>

int main() {
    std::string text;
    std::string hai;
    std::string shine;
    std::getline(std::cin, text);
    std::getline(std::cin, hai);
    std::getline(std::cin, shine);

    int too = 0;

    // TODO: text.find(hai, bairlal)-аар дараагийн тохиолдлыг хайна.
    //       Олдвол replace()-ээр сольж, too-г нэмээд хайлтыг
    //       шинэ үгийн АРДААС үргэлжлүүлнэ.
    //       std::string::npos буцаавал давталт дуусна.

    std::cout << text << "\\n";
    std::cout << "Сольсон: " << too << "\\n";
    return 0;
}
""",
            exercise=ExerciseSpec(
                statement="""\
Текст засварлагчийн «Бүгдийг солих» (Replace All) үйлдлийг хэрэгжүүл.
Текстэн дэх **хайх үгийн бүх** тохиолдлыг шинэ үгээр сольж, үр дүн ба
хэдэн удаа сольсныг хэвлэ.

**Оролт:** гурван мөр — текст, хайх үг (хоосон биш), шинэ үг. Шинэ үг
хоосон байж болно — тэгвэл хайх үгийг устгана. Мөр бүр зай агуулж болно.

**Гаралт:** хоёр мөр — сольсны дараах текст, дараа нь `Сольсон: N`.

Тохиолдлуудыг зүүнээс баруун тийш, давхцуулалгүй тоолно: `aaaa` дотор
`aa` хоёр удаа олдоно.

Зөвлөгөө: `text.find(hai, ehlel)`-ийн хоёр дахь параметр нь хайж эхлэх
байрлал. Сольсныхоо дараа хайлтыг **шинэ үгийн ардаас** үргэлжлүүл — эс
бөгөөс `C`-г `C++`-ээр солиход давталт хэзээ ч дуусахгүй.
""",
                tests=(
                    TestCaseSpec(
                        stdin="муур муур хоёр тоглож байна\nмуур\nнохой\n",
                        expected_output="нохой нохой хоёр тоглож байна\nСольсон: 2\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="I like C. C is fast.\nC\nC++\n",
                        expected_output="I like C++. C++ is fast.\nСольсон: 2\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="Сайн байна уу\nPython\nC++\n",
                        expected_output="Сайн байна уу\nСольсон: 0\n",
                    ),
                    TestCaseSpec(
                        stdin="a-b-c-d\n-\n\n",
                        expected_output="abcd\nСольсон: 3\n",
                    ),
                    TestCaseSpec(
                        stdin="aaaa\naa\nb\n",
                        expected_output="bb\nСольсон: 2\n",
                    ),
                    TestCaseSpec(
                        stdin="abab\nab\nabab\n",
                        expected_output="abababab\nСольсон: 2\n",
                    ),
                    TestCaseSpec(
                        stdin="2025 он, 2025 жил\n2025\n2026\n",
                        expected_output="2026 он, 2026 жил\nСольсон: 2\n",
                    ),
                ),
                solution="""\
#include <iostream>
#include <string>

int main() {
    std::string text;
    std::string hai;
    std::string shine;
    std::getline(std::cin, text);
    std::getline(std::cin, hai);
    std::getline(std::cin, shine);

    int too = 0;

    // Хоосон үгийг find() үргэлж «олох» тул давталт төгсөхгүй — урьдчилан хамгаална
    if (!hai.empty()) {
        // Эхний тохиолдлыг олно; олдохгүй бол npos буцна (-1 биш)
        std::size_t bairlal = text.find(hai);
        while (bairlal != std::string::npos) {
            // bairlal-аас эхлэх hai.size() тэмдэгтийг shine-ээр солино
            text.replace(bairlal, hai.size(), shine);
            too++;
            // Шинэ үгийн доторх тохиолдлыг дахин солихгүйн тулд ардаас нь хайна
            bairlal = text.find(hai, bairlal + shine.size());
        }
    }

    std::cout << text << "\\n";
    std::cout << "Сольсон: " << too << "\\n";
    return 0;
}
""",
                tips="""\
- Эхлээд `text.find(hai)`-ээр эхний тохиолдлыг ол, дараа нь
  `while (bairlal != std::string::npos)` давталтаар үргэлжлүүл. Олдохгүй үед
  `npos` буцдаг, `-1` биш — `>= 0` гэж шалгавал үргэлж үнэн гарна.
- Олдсон байрлалд `text.replace(bairlal, hai.size(), shine)` хий — хэдэн
  тэмдэгт солихыг **хайх үгийн** уртаар өгнө, шинэ үгийнхээр биш.
- Гол занга: дараагийн хайлтыг `text.find(hai, bairlal + shine.size())` гэж
  **шинэ үгийн ардаас** эхлүүл. `bairlal`-аас эхлүүлбэл шинэ үг дотор хайх
  үг байх үед давталт хэзээ ч дуусахгүй, эсвэл нэг газрыг олон удаа солино.
- Шалгагч огт олдохгүй байх (`Сольсон: 0`), шинэ үг хоосон байх (устгах),
  давхцаж болох тохиолдлууд, шинэ үг нь хайх үгийг агуулсан тохиолдлыг
  шалгана. Тоологчоо `replace` бүрт нэмэхээ бүү мартаарай.
""",
            ),
        ),
    ],
)

REFERENCES = ModuleSpec(
    title="Модул 17 — Лавлагаа (References)",
    description="Заагчийн илүү аюулгүй хувилбар.",
    lessons=[
        LessonSpec(
            title="Лавлагаа",
            slug="lavlagaa",
            description="Хувьсагчийн өөр нэр үүсгэх.",
            duration=400,
            language=CPP,
            content="""\
Лавлагаа нь одоо байгаа хувьсагчийн **өөр нэр**:

```cpp
int too = 42;
int &lavlagaa = too;

lavlagaa = 100;
std::cout << too;      // 100 — ижил хувьсагч
```

Шинэ санах ой үүсэхгүй. `lavlagaa` ба `too` нь **яг нэг зүйл**.

### Гурван дүрэм

**1. Зарлахдаа заавал эхлүүлнэ**

```cpp
int &a;           // АЛДАА — юуг заасан нь тодорхойгүй
int &b = too;     // зөв
```

**2. Дараа нь өөр зүйл рүү заалгаж болохгүй**

```cpp
int a = 1, b = 2;
int &lav = a;
lav = b;          // a-д b-гийн УТГЫГ оноолоо, заалтыг сольсонгүй
```

**3. `nullptr` байж болохгүй**

Тиймээс лавлагаа нь заагчаас **аюулгүй** — хоосон эсэхийг шалгах
шаардлагагүй.

### Гол хэрэглээ — функцийн параметр

```cpp
void hoyor_dahin(int &too) {
    too *= 2;
}

int a = 5;
hoyor_dahin(a);       // & бичих шаардлагагүй
std::cout << a;       // 10
```

C-ийн заагчтай харьцуулбал:

```c
void hoyor_dahin(int *too) { *too *= 2; }
hoyor_dahin(&a);
```

Лавлагаа нь дуудалтын талд ямар ч нэмэлт тэмдэг шаардахгүй.

### `const` лавлагаа

```cpp
void hevleh(const std::string &text) {
    std::cout << text << "\\n";
}
```

Хуулбар үүсэхгүй **бөгөөд** өөрчлөхгүй. Том объектыг унших стандарт
хэлбэр.

### Далд байдлаар хуулбар үүсэх занга

```cpp
std::string jagsaalt[] = {"урт текст", "бас урт"};

for (auto ner : jagsaalt) { }          // давталт бүрт ХУУЛБАР
for (const auto &ner : jagsaalt) { }   // хуулбаргүй
```

Муж дээрх `for`-ийн `&` (Модул 14) нь мөн лавлагаа. `const auto &` нь
«хуулбар үүсгэхгүй, гэхдээ өөрчлөхгүй» гэсэн утгатай. Жижиг жагсаалтад
мэдэгдэхгүй ч том өгөгдөл дээр ялгаа нь мэдэгдэхүйц.

### Лавлагаа буцаах нь аюултай

```cpp
int &muu() {
    int locale = 42;
    return locale;       // функц дуусахад locale УСТАНА
}
```

Устсан хувьсагч руу заасан лавлагаа. Хөрвүүлэгч анхааруулж магадгүй ч
зогсоохгүй. Локал хувьсагчийг **утгаар** буцаа.

### Жишээ програм

```cpp
#include <iostream>
#include <string>

void hoyor_dahin(int &too);
void hevleh(const std::string &text);
void solih(int &a, int &b);

int main() {
    int too = 42;
    int &lavlagaa = too;

    // Ижил хувьсагч — шинэ санах ой үүсэхгүй
    lavlagaa = 100;
    std::cout << "too       = " << too << "\\n";
    std::cout << "lavlagaa  = " << lavlagaa << "\\n";
    std::cout << "Хаяг ижил: " << (&too == &lavlagaa ? "тийм" : "үгүй") << "\\n\\n";

    // Функцийн параметр — дуудахдаа & шаардлагагүй
    int a = 5;
    hoyor_dahin(a);
    std::cout << "Хоёр дахин: " << a << "\\n";

    int x = 1;
    int y = 2;
    solih(x, y);
    std::cout << "Сольсон: x = " << x << ", y = " << y << "\\n\\n";

    hevleh("const лавлагаа — хуулбаргүй, өөрчлөхгүй");

    // Давталт дахь хуулбар
    std::string nershuud[] = {"Бат", "Сараа", "Дорж"};

    std::cout << "\\nconst auto & ашиглавал хуулбар үүсэхгүй:\\n";
    for (const auto &ner : nershuud) {
        std::cout << "  " << ner << "\\n";
    }

    return 0;
}

void hoyor_dahin(int &too) {
    too *= 2;
}

void hevleh(const std::string &text) {
    std::cout << text << "\\n";
}

void solih(int &a, int &b) {
    int tur = a;
    a = b;
    b = tur;
}
```
""",
            initial_code="""\
#include <iostream>

// a ба b-гийн утгыг солино
void solih(int &a, int &b) {
    // TODO
}

// solih()-ийг ашиглан a <= b <= c болгоно
void erembeleh(int &a, int &b, int &c) {
    // TODO
}

int main() {
    int a = 0;
    int b = 0;
    int c = 0;
    std::cin >> a >> b >> c;

    // Дуудахдаа & бичихгүй — лавлагаа өөрөө холбогдоно
    erembeleh(a, b, c);

    std::cout << a << " " << b << " " << c << "\\n";
    return 0;
}
""",
            exercise=ExerciseSpec(
                statement="""\
Лавлагаа ашиглан гурван хувьсагчийг **байранд нь** өсөх дарааллаар
эрэмбэл. `solih(a, b)` нь хоёр хувьсагчийн утгыг солино. `erembeleh(a, b, c)`
нь `solih`-ийг дуудаж `a <= b <= c` болгоно. `main` бэлэн — гурван тоо
уншиж, `erembeleh`-ийг дуудаад үр дүнг хэвлэнэ. Чи хоёр функцийн биеийг
бичнэ.

**Оролт:** гурван бүхэл тоо `a b c`.

**Гаралт:** эрэмбэлсэн гурван тоо, нэг мөрөнд, нэг зайгаар тусгаарлана.

**Хязгаарлалт:** тоо бүр `int`-ийн мужид багтана, сөрөг ба ижил тоо байж
болно.

Зөвлөгөө: гурван харьцуулалт хангалттай — `a > b` бол сол, `b > c` бол
сол, дахин `a > b` бол сол.
""",
                tests=(
                    TestCaseSpec(stdin="3 1 2\n", expected_output="1 2 3\n", sample=True),
                    TestCaseSpec(stdin="-5 10 0\n", expected_output="-5 0 10\n", sample=True),
                    TestCaseSpec(stdin="9 5 1\n", expected_output="1 5 9\n"),
                    TestCaseSpec(stdin="7 7 7\n", expected_output="7 7 7\n"),
                    TestCaseSpec(stdin="4 4 -1\n", expected_output="-1 4 4\n"),
                    TestCaseSpec(stdin="1 3 2\n", expected_output="1 2 3\n"),
                    TestCaseSpec(
                        stdin="2 -2147483648 2147483647\n",
                        expected_output="-2147483648 2 2147483647\n",
                    ),
                ),
                solution="""\
#include <iostream>

// int & — лавлагаа: дуудагчийн хувьсагчтай ШУУД ажиллана, хуулбар биш
void solih(int &a, int &b) {
    // a-гийн утгыг түр хадгалж байж солино, эс бөгөөс алдагдана
    int tur = a;
    a = b;
    b = tur;
}

void erembeleh(int &a, int &b, int &c) {
    // 1. Эхний хоёрыг зөв дараалалд оруулна
    if (a > b) {
        solih(a, b);
    }
    // 2. Хамгийн их утга c-д очно
    if (b > c) {
        solih(b, c);
    }
    // 3. c-ээс ирсэн бага утга a-гаас бага байж болох тул дахин шалгана
    if (a > b) {
        solih(a, b);
    }
}

int main() {
    int a = 0;
    int b = 0;
    int c = 0;
    std::cin >> a >> b >> c;

    // Дуудахдаа & бичихгүй — лавлагаа өөрөө холбогдоно
    erembeleh(a, b, c);

    std::cout << a << " " << b << " " << c << "\\n";
    return 0;
}
""",
                tips="""\
- Параметрийг `int &a` гэж **лавлагаагаар** ав. `int a` гэж утгаар авбал
  функц зөвхөн хуулбарыг солиод `main` дахь хувьсагч өөрчлөгдөхгүй.
- `solih` дотор түр хувьсагч ашигла: эхлээд `a`-г хадгал, дараа нь `a = b`,
  эцэст нь хадгалсан утгыг `b`-д өг. Шууд `a = b; b = a;` гэвэл хоёулаа
  ижил утгатай болно.
- `erembeleh`-д гурван харьцуулалт хангалттай: `a > b`, `b > c`, дахин
  `a > b`. Сүүлчийн шалгалтыг мартвал хамгийн бага тоо сүүлд ирсэн үед
  дунд нь гацна.
- Шалгагч ижил тоо, сөрөг тоо, `int`-ийн хамгийн их ба бага утгыг шалгана.
  Нэмэх/хасах аргаар солих (`a = a + b` гэх мэт) халилт үүсгэдэг тул түр
  хувьсагчтай аргыг хэрэглэ.
""",
            ),
        ),
        LessonSpec(
            title="Лавлагаа ба заагч",
            slug="lavlagaa-ba-zaagch",
            description="Хоёрын ялгаа, алийг нь хэзээ сонгох вэ.",
            duration=420,
            language=CPP,
            content="""\
### Харьцуулалт

| | Лавлагаа `&` | Заагч `*` |
|---|---|---|
| Эхлүүлэх | **Заавал** | Заавал биш |
| Дараа нь солих | Болохгүй | Болно |
| `nullptr` байж болох уу | **Үгүй** | Тийм |
| Синтакс | `too` | `*too` |
| Арифметик | Үгүй | Тийм (`z + 1`) |

### Алийг нь сонгох вэ

> **Анхдагчаар лавлагаа сонго.** Заагчийг зөвхөн лавлагаа хийж
> чадахгүй зүйлд ашигла.

Заагч хэрэгтэй гурван тохиолдол:

**1. «Утга байхгүй» гэдгийг илэрхийлэх**

```cpp
Hereglegch *oloh(int id);     // олдохгүй бол nullptr
```

Лавлагаа нь хоосон байж чадахгүй тул энд заагч хэрэгтэй. C++17-д
`std::optional` нь илүү тод хувилбар.

**2. Заалтыг өөрчлөх**

```cpp
int *odoo = &a;
odoo = &b;          // одоо b руу заана
```

**3. Массив дамжих**

```cpp
for (int *z = massiv; z < massiv + urt; z++) { }
```

### Функцийн гарын үсгээс уншигдах

```cpp
void ajil(const Oyutan &o);    // заавал байна, өөрчлөхгүй
void ajil(Oyutan &o);          // заавал байна, өөрчилнө
void ajil(const Oyutan *o);    // байхгүй ч байж болно
```

Уншигч гарын үсгийг хараад л дуудахдаа юу өгөхөө мэднэ. Энэ бол
лавлагааны далд боловч чухал давуу тал.

### Заагчийг задлахын өмнө шалга

```cpp
void ajil(Oyutan *o) {
    if (o == nullptr) {
        return;
    }
    std::cout << o->ner << "\\n";
}
```

Лавлагаатай бол энэ шалгалт **шаардлагагүй** — хоосон байх боломжгүй.

### Дүгнэлт

C-ээс шилжиж ирсэн хүн бүх зүйлд заагч ашиглах хандлагатай байдаг.
C++ -д ихэнх тохиолдолд лавлагаа илүү тохиромжтой: код нь цэвэрхэн,
хоосон заагчийн алдаа гарах боломжгүй.

### Жишээ програм

```cpp
#include <iostream>
#include <string>

struct Oyutan {
    std::string ner;
    int nas;
};

// Лавлагаа — заавал байна, өөрчлөхгүй
void hevleh(const Oyutan &o);

// Лавлагаа — заавал байна, ӨӨРЧИЛНӨ
void nas_nemeh(Oyutan &o);

// Заагч — олдохгүй бол nullptr буцаана
Oyutan *oloh(Oyutan angi[], int urt, const std::string &ner);

int main() {
    Oyutan angi[] = {
        {"Бат", 20},
        {"Сараа", 22},
        {"Дорж", 19}
    };

    for (const auto &o : angi) {
        hevleh(o);
    }

    // Лавлагаа — хоосон байх боломжгүй тул шалгах шаардлагагүй
    nas_nemeh(angi[0]);
    std::cout << "\\nНас нэмсний дараа: ";
    hevleh(angi[0]);

    // Заагч — задлахын өмнө ЗААВАЛ шалгана
    std::cout << "\\n";
    Oyutan *oldson = oloh(angi, 3, "Сараа");
    if (oldson != nullptr) {
        std::cout << "Олдлоо: " << oldson->ner << "\\n";
    }

    Oyutan *baihgui = oloh(angi, 3, "Болд");
    if (baihgui == nullptr) {
        std::cout << "«Болд» олдсонгүй\\n";
    }

    return 0;
}

void hevleh(const Oyutan &o) {
    std::cout << o.ner << " — " << o.nas << " настай\\n";
}

void nas_nemeh(Oyutan &o) {
    o.nas++;
}

Oyutan *oloh(Oyutan angi[], int urt, const std::string &ner) {
    for (int i = 0; i < urt; i++) {
        if (angi[i].ner == ner) {
            return &angi[i];   // массив доторх жинхэнэ элементийн хаяг
        }
    }
    return nullptr;
}
```
""",
            initial_code="""\
#include <iostream>
#include <string>

struct Baraa {
    std::string ner;
    int uldegdel;
};

// Заагч — нэрээр хайна. Олдвол тэр барааны хаяг, олдохгүй бол nullptr.
Baraa *oloh(Baraa baraanuud[], int n, const std::string &ner) {
    // TODO
    return nullptr;
}

// Лавлагаа — бараа заавал байгаа. Хүрэлцэх бол үлдэгдлийг хасаад true,
// хүрэлцэхгүй бол юу ч өөрчлөхгүй false.
bool zarah(Baraa &baraa, int too) {
    // TODO
    return false;
}

int main() {
    Baraa baraanuud[100];
    int n = 0;
    std::cin >> n;
    for (int i = 0; i < n; i++) {
        std::cin >> baraanuud[i].ner >> baraanuud[i].uldegdel;
    }

    int m = 0;
    std::cin >> m;
    for (int i = 0; i < m; i++) {
        std::string ner;
        int too = 0;
        std::cin >> ner >> too;

        // TODO: oloh()-оор хайж, nullptr эсэхийг ЗААВАЛ шалгана.
        //       Олдвол zarah(*baraa, too)-г дуудаж, үр дүнгээр нь
        //       тохирох мөрийг хэвлэнэ.
    }

    return 0;
}
""",
            exercise=ExerciseSpec(
                statement="""\
Дэлгүүрийн агуулахын захиалга боловсруулдаг програм бич. Барааг нэрээр нь
хайдаг `oloh` нь **заагч** буцаана — олдохгүй бол `nullptr`. Барааг зардаг
`zarah` нь барааг **лавлагаагаар** авна, учир нь түүнийг дуудах үед бараа
заавал байгаа.

**Оролт:**

- эхний мөрөнд барааны тоо `N`, дараагийн `N` мөрөнд `нэр үлдэгдэл`;
- дараа нь захиалгын тоо `M`, дараагийн `M` мөрөнд `нэр тоо_ширхэг`.

Нэр нь зайгүй нэг үг, том жижиг үсэг ялгаатай.

**Гаралт:** захиалга бүрт нэг мөр:

- бараа байхгүй бол `<нэр>: олдсонгүй`
- үлдэгдэл хүрэлцэхгүй бол `<нэр>: хүрэлцэхгүй (үлдэгдэл <үлдэгдэл>)`
- эс бөгөөс үлдэгдлээс хасаад `<нэр>: зарагдлаа, үлдэгдэл <шинэ үлдэгдэл>`

**Хязгаарлалт:** `1 ≤ N ≤ 100`, `1 ≤ M ≤ 100`, нэрс давхардахгүй,
үлдэгдэл `≥ 0`, захиалах тоо `≥ 1`.

Зөвлөгөө: массивын `i` дэх элементийн хаяг нь `&baraanuud[i]`. Заагчаар
талбарт хандахдаа `baraa->uldegdel`.
""",
                tests=(
                    TestCaseSpec(
                        stdin="3\nалим 10\nгадил 5\nинтоор 0\n4\nалим 3\nтарвас 1\nгадил 6\nалим 7\n",
                        expected_output=(
                            "алим: зарагдлаа, үлдэгдэл 7\n"
                            "тарвас: олдсонгүй\n"
                            "гадил: хүрэлцэхгүй (үлдэгдэл 5)\n"
                            "алим: зарагдлаа, үлдэгдэл 0\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="2\nсүү 1\nталх 0\n4\nталх 1\nсүү 1\nсүү 1\nСүү 1\n",
                        expected_output=(
                            "талх: хүрэлцэхгүй (үлдэгдэл 0)\n"
                            "сүү: зарагдлаа, үлдэгдэл 0\n"
                            "сүү: хүрэлцэхгүй (үлдэгдэл 0)\n"
                            "Сүү: олдсонгүй\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="1\npen 100\n3\nbook 1\npencil 2\npe 1\n",
                        expected_output="book: олдсонгүй\npencil: олдсонгүй\npe: олдсонгүй\n",
                    ),
                    TestCaseSpec(
                        stdin="5\na 1\nb 2\nc 3\nd 4\ne 5\n2\ne 5\ne 1\n",
                        expected_output="e: зарагдлаа, үлдэгдэл 0\ne: хүрэлцэхгүй (үлдэгдэл 0)\n",
                    ),
                    TestCaseSpec(
                        stdin="2\nном 20\nдэвтэр 50\n3\nдэвтэр 49\nном 1\nдэвтэр 2\n",
                        expected_output=(
                            "дэвтэр: зарагдлаа, үлдэгдэл 1\n"
                            "ном: зарагдлаа, үлдэгдэл 19\n"
                            "дэвтэр: хүрэлцэхгүй (үлдэгдэл 1)\n"
                        ),
                    ),
                ),
                solution="""\
#include <iostream>
#include <string>

struct Baraa {
    std::string ner;
    int uldegdel;
};

// Заагч буцаана — «олдсонгүй» гэдгийг nullptr-ээр илэрхийлж чадна
Baraa *oloh(Baraa baraanuud[], int n, const std::string &ner) {
    for (int i = 0; i < n; i++) {
        if (baraanuud[i].ner == ner) {
            // Хуулбарын биш, массив доторх ЖИНХЭНЭ элементийн хаяг
            return &baraanuud[i];
        }
    }
    return nullptr;
}

// Лавлагаа — бараа заавал байгаа тул nullptr шалгах шаардлагагүй
bool zarah(Baraa &baraa, int too) {
    // Хүрэлцэхгүй бол юу ч өөрчлөхгүйгээр false
    if (too > baraa.uldegdel) {
        return false;
    }
    // Лавлагаагаар ирсэн тул массив дахь барааны үлдэгдэл шууд хасагдана
    baraa.uldegdel -= too;
    return true;
}

int main() {
    Baraa baraanuud[100];
    int n = 0;
    std::cin >> n;
    for (int i = 0; i < n; i++) {
        std::cin >> baraanuud[i].ner >> baraanuud[i].uldegdel;
    }

    int m = 0;
    std::cin >> m;
    for (int i = 0; i < m; i++) {
        std::string ner;
        int too = 0;
        std::cin >> ner >> too;

        Baraa *baraa = oloh(baraanuud, n, ner);
        // Заагчийг задлахаас (*, ->) өмнө ЗААВАЛ nullptr эсэхийг шалгана.
        // *baraa нь заагчийг задалж zarah()-ийн лавлагаа параметрт өгнө.
        if (baraa == nullptr) {
            std::cout << ner << ": олдсонгүй\\n";
        } else if (zarah(*baraa, too)) {
            std::cout << ner << ": зарагдлаа, үлдэгдэл " << baraa->uldegdel << "\\n";
        } else {
            std::cout << ner << ": хүрэлцэхгүй (үлдэгдэл " << baraa->uldegdel << ")\\n";
        }
    }

    return 0;
}
""",
                tips="""\
- `oloh` дотор массивыг гүйж, нэр нь `==`-ээр таарвал `&baraanuud[i]`
  буцаа; давталт дуустал олдоогүй бол `nullptr`. Массив доторх элементийн
  хаягийг буцаах нь чухал — хуулбарынх бол үлдэгдлийн өөрчлөлт хадгалагдахгүй.
- `main`-д заагчийг ашиглахаас өмнө `baraa == nullptr` эсэхийг **заавал**
  шалга. Олдсон бол `zarah(*baraa, too)` — `*`-ээр задлаад лавлагаа
  параметрт өгнө. Талбарыг заагчаар уншихдаа `baraa->uldegdel`.
- `zarah`-д үлдэгдэл хүрэлцэхгүй бол юу ч өөрчлөхгүйгээр `false` буцаа.
  Захиалах тоо үлдэгдэлтэй **яг тэнцүү** бол зарагдана (үлдэгдэл `0`).
- Шалгагч нэг барааг олон удаа захиалах (өмнөх борлуулалт хадгалагдсан байх
  ёстой), үлдэгдэл нь `0` бараа, зөвхөн том жижиг үсгээр ялгаатай эсвэл
  хэсэгчлэн таарсан нэрийг шалгана — ийм нэр **олдсонгүй** гэж тооцогдоно.
""",
            ),
        ),
    ],
)

OOP = ModuleSpec(
    title="Модул 18 — Объект хандлагат програмчлалын үндэс",
    description="Класс, объект, конструктор, нэвтрэх эрх.",
    lessons=[
        LessonSpec(
            title="Класс ба объект",
            slug="angi-ba-obyekt",
            description="Өгөгдөл ба түүн дээрх үйлдлийг нэгтгэх.",
            duration=450,
            language=CPP,
            content="""\
`struct` нь өгөгдлийг багцалдаг. **Класс** нь өгөгдөл дээрх
**үйлдлийг** ч хамт багцална.

```cpp
class Dans {
public:
    std::string ezen;
    double uldegdel;

    void nemeh(double dun) {
        uldegdel += dun;
    }

    void hevleh() const {
        std::cout << ezen << ": " << uldegdel << "\\n";
    }
};
```

Хаалтын дараах **цэг таслалыг** бүү мартаарай.

### Объект үүсгэх

```cpp
Dans dans;
dans.ezen = "Бат";
dans.uldegdel = 1000;

dans.nemeh(500);
dans.hevleh();
```

**Класс** нь загвар, **объект** нь түүнээс үүсгэсэн бодит зүйл. Нэг
класснаас хэдэн ч объект үүсгэж болно, тус бүр өөрийн өгөгдөлтэй.

### Метод

Класс доторх функцийг **метод** гэнэ. Тэдгээр нь объектын талбарт
шууд хандана — `this->` бичих шаардлагагүй.

### `const` метод

```cpp
void hevleh() const {
    std::cout << uldegdel << "\\n";
}
```

`const` нь «энэ метод объектыг **өөрчлөхгүй**» гэдгийг батална.
Өөрчлөх гэвэл хөрвүүлэгч алдаа заана.

`const` объект дээр зөвхөн `const` метод дуудагдана:

```cpp
void hevleh(const Dans &d) {
    d.hevleh();      // const метод тул ажиллана
    d.nemeh(100);    // АЛДАА
}
```

> Объектыг өөрчлөхгүй метод бүрд `const` бич. Энэ нь зуршил болох ёстой.

### `class` ба `struct`

Техникийн хувьд ганц ялгаа:

| | Анхдагч эрх |
|---|---|
| `struct` | `public` |
| `class` | `private` |

Уламжлал:

- Зөвхөн өгөгдөл багцалж байвал `struct`
- Өгөгдөл ба зан төлөв хамт байвал `class`

### Тодорхойлолтыг тусад нь

Том класст методын биеийг гадна нь бичих нь уншихад хялбар:

```cpp
class Dans {
public:
    void nemeh(double dun);
};

void Dans::nemeh(double dun) {
    uldegdel += dun;
}
```

`Dans::` нь «энэ метод `Dans` классынх» гэсэн утгатай.

### Жишээ програм

```cpp
#include <iostream>
#include <string>

class Dans {
public:
    std::string ezen;
    double uldegdel;

    void nemeh(double dun) {
        if (dun <= 0) {
            std::cout << "Дүн эерэг байх ёстой\\n";
            return;
        }
        uldegdel += dun;
    }

    bool hasah(double dun) {
        if (dun > uldegdel) {
            return false;
        }
        uldegdel -= dun;
        return true;
    }

    // const — энэ метод объектыг ӨӨРЧЛӨХГҮЙ
    void hevleh() const {
        std::cout << ezen << ": " << uldegdel << "₮\\n";
    }
};

void tailan(const Dans &d);

int main() {
    Dans bat;
    bat.ezen = "Бат";
    bat.uldegdel = 1000;

    Dans saraa;
    saraa.ezen = "Сараа";
    saraa.uldegdel = 5000;

    // Объект бүр өөрийн өгөгдөлтэй
    bat.nemeh(500);
    saraa.hasah(2000);

    bat.hevleh();
    saraa.hevleh();

    // Хүрэлцэхгүй үед
    if (!bat.hasah(99999)) {
        std::cout << "\\nҮлдэгдэл хүрэлцэхгүй\\n";
    }

    tailan(bat);

    return 0;
}

// const объект дээр зөвхөн const метод дуудагдана
void tailan(const Dans &d) {
    std::cout << "\\n--- Тайлан ---\\n";
    d.hevleh();
    // d.nemeh(100);  <- энэ мөр ХӨРВҮҮЛЭХГҮЙ
}
```
""",
            initial_code="""\
#include <iostream>
#include <string>

class Baatar {
public:
    std::string ner;
    int ami;   // 0-100

    // ami-г huch-аар бууруулна. 0-ээс доош орохгүй.
    void tsohih(int huch) {
        // TODO
    }

    // ami-г hemjee-гээр нэмнэ. 100-аас дээш гарахгүй.
    // Ялагдсан (ami нь 0) баатар эдгэрэхгүй.
    void edgeh(int hemjee) {
        // TODO
    }

    // ami 0-ээс их бол true
    bool amid() const {
        // TODO
        return false;
    }

    // «<нэр>: <ами>/100», ялагдсан бол ард нь « (ялагдсан)»
    void hevleh() const {
        // TODO
    }
};

void tailan(const Baatar &b);

// main бэлэн — оролт уншиж, методуудыг дуудна
int main() {
    Baatar baatar;
    std::cin >> baatar.ner >> baatar.ami;

    std::string komand;
    int utga = 0;
    while (std::cin >> komand) {
        if (komand == "tsohih") {
            std::cin >> utga;
            baatar.tsohih(utga);
        } else if (komand == "edgeh") {
            std::cin >> utga;
            baatar.edgeh(utga);
        } else if (komand == "hevleh") {
            tailan(baatar);
        }
    }

    return 0;
}

// const объект дээр зөвхөн const метод дуудагдана
void tailan(const Baatar &b) {
    b.hevleh();
}
""",
            exercise=ExerciseSpec(
                statement="""\
Тоглоомын баатрыг `Baatar` классаар загварчил. Классын араг болон оролт
уншдаг `main` бэлэн — чи дөрвөн методын биеийг бичнэ:

- `tsohih(huch)` — амийг `huch`-аар бууруулна, `0`-ээс доош орохгүй.
- `edgeh(hemjee)` — амийг `hemjee`-гээр нэмнэ, `100`-аас дээш гарахгүй.
  Ялагдсан (амь нь `0`) баатар эдгэрэхгүй.
- `amid()` — амь `0`-ээс их бол `true`. Объектыг өөрчлөхгүй тул `const`.
- `hevleh()` — `<нэр>: <амь>/100` гэж хэвлэнэ, ялагдсан бол ард нь
  ` (ялагдсан)` нэмнэ. Мөн `const`.

**Оролт:** эхний мөрөнд баатрын нэр (нэг үг) ба эхний амь (`1`–`100`).
Дараа нь файлын төгсгөл хүртэл тушаалууд: `tsohih X`, `edgeh X` эсвэл
`hevleh` (`X` — эерэг бүхэл тоо).

**Гаралт:** `hevleh` тушаал бүрт нэг мөр.

Зөвлөгөө: `hevleh()` дотроос `amid()`-ийг дуудаж болно.
""",
                tests=(
                    TestCaseSpec(
                        stdin="Сараа 80\ntsohih 25\nhevleh\nedgeh 10\nhevleh\n",
                        expected_output="Сараа: 55/100\nСараа: 65/100\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="Бат 40\ntsohih 55\nhevleh\n",
                        expected_output="Бат: 0/100 (ялагдсан)\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="Дорж 90\nedgeh 50\nhevleh\ntsohih 1\nhevleh\n",
                        expected_output="Дорж: 100/100\nДорж: 99/100\n",
                    ),
                    TestCaseSpec(
                        stdin="Anu 30\ntsohih 30\nhevleh\nedgeh 40\nhevleh\n",
                        expected_output="Anu: 0/100 (ялагдсан)\nAnu: 0/100 (ялагдсан)\n",
                    ),
                    TestCaseSpec(
                        stdin="Тэмүүлэн 1\nhevleh\ntsohih 1\ntsohih 5\nedgeh 100\nhevleh\n",
                        expected_output="Тэмүүлэн: 1/100\nТэмүүлэн: 0/100 (ялагдсан)\n",
                    ),
                    TestCaseSpec(
                        stdin="Болд 100\nhevleh\nedgeh 1\nhevleh\ntsohih 99\nedgeh 50\nhevleh\n",
                        expected_output="Болд: 100/100\nБолд: 100/100\nБолд: 51/100\n",
                    ),
                ),
                solution="""\
#include <iostream>
#include <string>

class Baatar {
public:
    std::string ner;
    int ami;

    // Метод дотроос талбарт шууд нэрээр нь хандана (ami, ner).
    // Эхлээд хасаад, 0-ээс доош орсон бол 0 болгоно.
    void tsohih(int huch) {
        ami -= huch;
        if (ami < 0) {
            ami = 0;
        }
    }

    void edgeh(int hemjee) {
        // Ялагдсан баатар эдгэрэхгүй — өөрийн amid() методыг дуудаж шалгана
        if (!amid()) {
            return;
        }
        // Нэмээд 100-аас хэтэрвэл 100 болгоно
        ami += hemjee;
        if (ami > 100) {
            ami = 100;
        }
    }

    // const — энэ метод объектыг өөрчлөхгүй гэдгийг хөрвүүлэгчид амлана
    bool amid() const {
        return ami > 0;
    }

    // tailan() дотор const объект дээр дуудагддаг тул мөн const байх ёстой
    void hevleh() const {
        std::cout << ner << ": " << ami << "/100";
        if (!amid()) {
            std::cout << " (ялагдсан)";
        }
        std::cout << "\\n";
    }
};

void tailan(const Baatar &b);

int main() {
    Baatar baatar;
    std::cin >> baatar.ner >> baatar.ami;

    // Файлын төгсгөл хүртэл тушаал уншиж, тохирох методыг дуудна
    std::string komand;
    int utga = 0;
    while (std::cin >> komand) {
        if (komand == "tsohih") {
            std::cin >> utga;
            baatar.tsohih(utga);
        } else if (komand == "edgeh") {
            std::cin >> utga;
            baatar.edgeh(utga);
        } else if (komand == "hevleh") {
            tailan(baatar);
        }
    }

    return 0;
}

// const объект дээр зөвхөн const метод дуудагдана
void tailan(const Baatar &b) {
    b.hevleh();
}
""",
                tips="""\
- Метод дотроос талбарт шууд нэрээр нь хандана (`ami`, `ner`) —
  `baatar.ami` гэж бичих шаардлагагүй, аль объект дээр дуудагдсан нь
  өөрөө тодорхой.
- `tsohih`: эхлээд хас, дараа нь `0`-ээс бага болсон бол `0` болго.
  `edgeh`: **эхлээд** амьд эсэхийг шалга, дараа нь нэмээд `100`-аас
  хэтэрвэл `100` болго.
- `amid()`, `hevleh()`-ийн `const`-ийг бүү устга — `tailan` нь
  `const Baatar &` авдаг тул `const` биш методыг дуудвал хөрвүүлэлтийн
  алдаа гарна. `hevleh()` дотроос `amid()`-ийг дуудаж болно.
- Шалгагч амь яг `0` хүрэх, `0`-ээс доош унах, аль хэдийн `100` байхад
  эдгээх, ялагдсаны дараа эдгээх зэрэг хязгаарын тохиолдлыг шалгана.
  ` (ялагдсан)`-ын өмнөх зайг мартуузай.
""",
            ),
        ),
        LessonSpec(
            title="Конструктор",
            slug="konstruktor",
            description="Объектыг үүсэх мөчид нь зөв төлөвт оруулах.",
            duration=450,
            language=CPP,
            content="""\
Өмнөх хичээлд объект үүсгээд талбар бүрийг гараар оноосон. Мартвал
хог утга үлдэнэ:

```cpp
Dans dans;
dans.ezen = "Бат";
// uldegdel оноогоогүй — хог утга
```

**Конструктор** нь үүсэх мөчид нь ажиллаж, энэ асуудлыг шийднэ.

```cpp
class Dans {
public:
    Dans(std::string ezen, double ehleliin)
        : ezen_(ezen), uldegdel_(ehleliin) {
    }

private:
    std::string ezen_;
    double uldegdel_;
};
```

Ашиглах:

```cpp
Dans bat("Бат", 1000);
```

Одоо **эхлүүлээгүй объект үүсгэх боломжгүй**.

### Эхлүүлэгчийн жагсаалт

```cpp
Dans(std::string ezen, double ehleliin)
    : ezen_(ezen), uldegdel_(ehleliin) {
}
```

Хоёр цэгийн дараах хэсгийг *эхлүүлэгчийн жагсаалт* гэнэ. Энэ нь биен
дотор оноохоос **илүү**:

```cpp
Dans(std::string ezen) {
    ezen_ = ezen;      // эхлээд хоосон үүсээд дараа нь оноолоо
}
```

Биен дотор оноовол талбар эхлээд анхдагчаар үүсээд дараа нь дахин
онооно — хоёр удаагийн ажил. `const` талбар болон лавлагааг зөвхөн
жагсаалтаар л эхлүүлж чадна.

### Давхардсан конструктор

```cpp
Dans(std::string ezen, double ehleliin);
Dans(std::string ezen);            // үлдэгдэл 0
Dans();                            // бүх зүйл анхдагч
```

Эсвэл анхдагч параметр:

```cpp
Dans(std::string ezen, double ehleliin = 0.0);
```

### Анхдагч конструктор

Конструктор **огт бичихгүй** бол хөрвүүлэгч хоосон нэгийг өөрөө үүсгэнэ.
Гэхдээ нэгийг нь бичмэгц тэр автомат нь **алга болно**:

```cpp
Dans(std::string ezen, double dun);

Dans hooson;     // АЛДАА — анхдагч конструктор байхгүй болсон
```

Хэрэгтэй бол тодорхой зарла:

```cpp
Dans() = default;
```

### Деструктор

Объект устахад ажиллана:

```cpp
~Dans() {
    std::cout << "Данс хаагдлаа\\n";
}
```

Файл, сүлжээний холболт, санах ой чөлөөлөхөд хэрэгтэй. Энгийн класст
ихэвчлэн шаардлагагүй — `std::string`, `std::vector` нь өөрсдийгөө
цэвэрлэнэ.

### Жишээ програм

```cpp
#include <iostream>
#include <string>

class Dans {
public:
    // Эхлүүлэгчийн жагсаалт — биен дотор оноохоос илүү
    Dans(std::string ezen, double ehleliin = 0.0)
        : ezen_(ezen), uldegdel_(ehleliin) {
        std::cout << "Данс нээгдлээ: " << ezen_ << "\\n";
    }

    ~Dans() {
        std::cout << "Данс хаагдлаа: " << ezen_ << "\\n";
    }

    void nemeh(double dun) {
        if (dun > 0) {
            uldegdel_ += dun;
        }
    }

    bool hasah(double dun) {
        if (dun <= 0 || dun > uldegdel_) {
            return false;
        }
        uldegdel_ -= dun;
        return true;
    }

    void hevleh() const {
        std::cout << "  " << ezen_ << ": " << uldegdel_ << "₮\\n";
    }

private:
    std::string ezen_;
    double uldegdel_;
};

int main() {
    // Эхлүүлээгүй объект үүсгэх БОЛОМЖГҮЙ болсон
    Dans bat("Бат", 1000);
    Dans saraa("Сараа");   // анхдагч утга — 0

    std::cout << "\\n";
    bat.nemeh(500);
    saraa.nemeh(3000);

    bat.hevleh();
    saraa.hevleh();

    if (!saraa.hasah(99999)) {
        std::cout << "\\nСараагийн үлдэгдэл хүрэлцэхгүй\\n\\n";
    }

    // main дуусахад деструктор УРВУУ дарааллаар ажиллана
    return 0;
}
```
""",
            initial_code="""\
#include <iomanip>
#include <iostream>

// Хэдэн ч минутыг 0-1439 мужид оруулна: 1500 -> 60, -30 -> 1410
int hevend_oruulah(int minut) {
    // TODO
    return minut;
}

class Tsag {
public:
    // TODO: эхлүүлэгчийн жагсаалтаар niit_minut_-ийг
    //       hevend_oruulah(tsag * 60 + minut)-ээр эхлүүлнэ
    Tsag(int tsag, int minut) : niit_minut_(0) {
    }

    // TODO: minut-ийг нэмнэ (сөрөг бол хасна), үр дүн мөн мужид орно
    void nemeh(int minut) {
    }

    // TODO: одоогоор минутыг шууд хэвлэж байна.
    //       ЦЦ:ММ хэлбэрээр, хоёр оронтой хэвлэ — жишээ нь 09:05
    void hevleh() const {
        std::cout << niit_minut_ << "\\n";
    }

private:
    int niit_minut_;   // шөнө дундаас хойшхи минут, 0-1439
};

// main бэлэн
int main() {
    int tsag = 0;
    int minut = 0;
    int nemelt = 0;
    std::cin >> tsag >> minut >> nemelt;

    Tsag t(tsag, minut);
    t.hevleh();

    t.nemeh(nemelt);
    t.hevleh();

    return 0;
}
""",
            exercise=ExerciseSpec(
                statement="""\
Цагийг хадгалдаг `Tsag` класс бич. Дотроо шөнө дундаас хойшхи минутыг
`0`–`1439` мужид хадгална. Конструктор нь ямар ч цаг, минутаас объектыг
**үүсэх мөчид нь** зөв төлөвт оруулна — буруу төлөвтэй `Tsag` байх
боломжгүй.

- `Tsag(tsag, minut)` — `tsag * 60 + minut`-ийг мужид оруулна. Жишээ нь
  `Tsag(25, 70)` нь `02:10`, `Tsag(0, -30)` нь `23:30`.
- `nemeh(minut)` — минут нэмнэ (сөрөг бол хасна), үр дүн мөн мужид орно.
- `hevleh()` — `ЦЦ:ММ` хэлбэрээр, тус бүрийг хоёр оронтой хэвлэнэ (`09:05`).

`main` бэлэн: гурван тоо уншаад объект үүсгэж хэвлэнэ, дараа нь минут
нэмээд дахин хэвлэнэ.

**Оролт:** гурван бүхэл тоо — цаг, минут, нэмэх минут. Аль нь ч сөрөг
байж болно.

**Гаралт:** хоёр мөр — эхний цаг ба нэмсний дараах цаг, `ЦЦ:ММ` хэлбэрээр.

**Хязгаарлалт:** тоо бүрийн абсолют утга `1 000 000`-аас хэтрэхгүй.

Зөвлөгөө: C++ -д `-30 % 1440` нь `-30` гарна — сөрөг үлдэгдэлд `1440`
нэм. Урд нь тэг нэмэхэд `std::setfill('0') << std::setw(2)` (`<iomanip>`)
эсвэл `if (x < 10)` хэрэглэж болно. `std::setfill('0')` нь `setw`-ийн
дүүргэх хоосон зайн оронд `0` тавина: `5` → `05`.
""",
                tests=(
                    TestCaseSpec(stdin="9 45 30\n", expected_output="09:45\n10:15\n", sample=True),
                    TestCaseSpec(stdin="23 50 20\n", expected_output="23:50\n00:10\n", sample=True),
                    TestCaseSpec(stdin="25 70 0\n", expected_output="02:10\n02:10\n"),
                    TestCaseSpec(stdin="0 0 -1\n", expected_output="00:00\n23:59\n"),
                    TestCaseSpec(stdin="10 -90 -600\n", expected_output="08:30\n22:30\n"),
                    TestCaseSpec(stdin="-1 0 1440\n", expected_output="23:00\n23:00\n"),
                    TestCaseSpec(stdin="12 0 100000\n", expected_output="12:00\n22:40\n"),
                    TestCaseSpec(
                        stdin="0 -1000000 -1000000\n",
                        expected_output="13:20\n02:40\n",
                    ),
                ),
                solution="""\
#include <iomanip>
#include <iostream>

// Ямар ч минутыг 0-1439 мужид оруулна
int hevend_oruulah(int minut) {
    const int odor = 24 * 60;
    int ur = minut % odor;
    // C++ -д сөрөг тооны % нь сөрөг гарна (-30 % 1440 == -30) — нэг өдөр нэмж засна
    if (ur < 0) {
        ur += odor;
    }
    return ur;
}

class Tsag {
public:
    // Эхлүүлэгчийн жагсаалт — объект үүсэх мөчөөсөө зөв төлөвтэй байна
    Tsag(int tsag, int minut) : niit_minut_(hevend_oruulah(tsag * 60 + minut)) {
    }

    // Нэмсний дараа дахин мужид оруулна — төлөв хэзээ ч буруу болохгүй
    void nemeh(int minut) {
        niit_minut_ = hevend_oruulah(niit_minut_ + minut);
    }

    // Цаг = минут / 60, минут = минут % 60.
    // setfill('0') хадгалагдана, харин setw(2) зөвхөн дараагийн утгад үйлчилнэ.
    void hevleh() const {
        std::cout << std::setfill('0') << std::setw(2) << niit_minut_ / 60 << ":"
                  << std::setw(2) << niit_minut_ % 60 << "\\n";
    }

private:
    // Шөнө дундаас хойшхи минут — цаг, минутыг тусад нь хадгалахаас хялбар
    int niit_minut_;
};

int main() {
    int tsag = 0;
    int minut = 0;
    int nemelt = 0;
    std::cin >> tsag >> minut >> nemelt;

    Tsag t(tsag, minut);
    t.hevleh();

    t.nemeh(nemelt);
    t.hevleh();

    return 0;
}
""",
                tips="""\
- Эхлээд `hevend_oruulah`-г бич: `minut % 1440`-ийг ав, үр дүн сөрөг бол
  `1440` нэм. C++ -д `%` нь сөрөг тоонд сөрөг үлдэгдэл өгдөг — энэ бол
  хамгийн түгээмэл алдаа.
- Конструкторын биед оноохын оронд **эхлүүлэгчийн жагсаалтад**
  `: niit_minut_(hevend_oruulah(...))` гэж эхлүүл. `nemeh` ч үр дүнгээ мөн
  энэ функцээр дахин мужид оруулна.
- Хэвлэхдээ цаг нь `niit_minut_ / 60`, минут нь `niit_minut_ % 60`. Хоёр
  оронтой болгоход `std::setfill('0') << std::setw(2)` — `setw` зөвхөн
  дараагийн нэг утгад үйлчилдэг тул минутын өмнө дахин бич.
- Шалгагч 24-өөс их цаг, 59-өөс их минут, сөрөг цаг ба минут, олон хоногоор
  нэмэх ба хасах тохиолдлыг шалгана. Бүгдийг нэг «нийт минут» болгож
  хадгалбал ийм тохиолдол бүр ижилхэн шийдэгдэнэ.
""",
            ),
        ),
        LessonSpec(
            title="public ба private",
            slug="public-private",
            description="Дотоод төлөвийг хамгаалах.",
            duration=450,
            language=CPP,
            content="""\
### Асуудал

Талбарууд `public` бол хэн ч, юу ч хийж чадна:

```cpp
Dans dans("Бат", 1000);
dans.uldegdel = -99999;      // сөрөг үлдэгдэл!
```

Класс дотор шалгалт бичсэн ч утгагүй — тойрч гарах боломжтой.

### `private`

```cpp
class Dans {
public:
    void nemeh(double dun);
    double uldegdel() const;

private:
    double uldegdel_;      // гаднаас ХҮРЭХГҮЙ
};
```

Одоо `uldegdel_`-ийг зөвхөн классын өөрийн метод өөрчилнө. Бүх
өөрчлөлт таны шалгалтаар дамжина.

Үүнийг **инкапсуляци** (нуулт) гэнэ — OOP-ийн үндсэн санаа.

### Нэрлэх уламжлал

Хувийн талбарыг ялгахын тулд дагавар эсвэл угтвар өгнө:

```cpp
double uldegdel_;      // дагавар — түгээмэл
double m_uldegdel;     // угтвар — бас түгээмэл
```

Аль нь ч болно. Төсөл дотроо тууштай байх нь чухал.

### Getter ба setter

```cpp
double uldegdel() const {        // getter
    return uldegdel_;
}

void uldegdel_tavih(double dun) { // setter
    if (dun >= 0) {
        uldegdel_ = dun;
    }
}
```

Текст зэрэг том талбарын getter нь ихэвчлэн `const` лавлагаа буцаадаг:

```cpp
const std::string &ezen() const {
    return ezen_;
}
```

Хуулбар үүсэхгүй, `const` тул дуудсан тал өөрчилж чадахгүй. Модул 17-д
локал хувьсагч руу лавлагаа буцаах нь аюултай гэж үзсэн — функц дуусахад
тэр устдаг. Харин талбар нь объекттой хамт амьдардаг тул түүн рүү лавлагаа
буцаах нь аюулгүй.

> Талбар бүрт автоматаар getter/setter бүү бич. Тэгвэл `public` болгосонтой
> адил болно. **Зөвхөн үнэхээр хэрэгтэйг** нь гарга.

Сайн класс нь өгөгдлөө гаргахын оронд **утга учиртай үйлдэл** санал
болгоно:

```cpp
// Муу — дотоод бүтэц ил гарлаа
dans.uldegdel_tavih(dans.uldegdel() - 500);

// Сайн — зорилго нь тодорхой, шалгалт дотроо
dans.hasah(500);
```

### `protected`

Гурав дахь эрх. Удамшсан класст харагдана, гаднаас харагдахгүй.
Удамшил нь энэ сургалтын хүрээнээс гадуур.

### Ерөнхий дүрэм

> Талбарыг **анхдагчаар `private`** болго. Зөвхөн шаардлагатайг нь
> `public` болго.

Дараа нь `private`-ийг `public` болгох нь амархан. Эсрэгээрээ хийх нь
тэр классыг ашигласан бүх кодыг эвдэнэ.

### Жишээ програм

```cpp
#include <iostream>
#include <string>

class Dans {
public:
    Dans(std::string ezen, double ehleliin = 0.0)
        : ezen_(ezen), uldegdel_(ehleliin < 0 ? 0 : ehleliin), guilgee_too_(0) {
    }

    // Утга учиртай үйлдэл — шалгалт нь дотроо
    void nemeh(double dun) {
        if (dun <= 0) {
            return;
        }
        uldegdel_ += dun;
        guilgee_too_++;
    }

    bool hasah(double dun) {
        if (dun <= 0 || dun > uldegdel_) {
            return false;
        }
        uldegdel_ -= dun;
        guilgee_too_++;
        return true;
    }

    // Зөвхөн унших getter
    double uldegdel() const { return uldegdel_; }
    const std::string &ezen() const { return ezen_; }
    int guilgeenii_too() const { return guilgee_too_; }

    void hevleh() const {
        std::cout << ezen_ << ": " << uldegdel_ << "₮ ("
                  << guilgee_too_ << " гүйлгээ)\\n";
    }

private:
    std::string ezen_;
    double uldegdel_;
    int guilgee_too_;   // амжилттай гүйлгээний тоо
};

int main() {
    Dans bat("Бат", 1000);

    bat.nemeh(500);
    bat.nemeh(-100);    // шалгалтаар хаагдана
    bat.hasah(200);
    bat.hasah(99999);   // хүрэлцэхгүй тул хаагдана

    bat.hevleh();

    // bat.uldegdel_ = -99999;  <- private тул ХӨРВҮҮЛЭХГҮЙ
    std::cout << "Үлдэгдэл: " << bat.uldegdel() << "₮\\n";
    std::cout << "Эзэн: " << bat.ezen() << "\\n";

    // Сөрөг эхлэлийг конструктор засна
    Dans burugu("Тест", -500);
    std::cout << "\\nСөрөг эхлэл -> " << burugu.uldegdel() << "₮\\n";

    return 0;
}
```
""",
            initial_code="""\
#include <iostream>

class Lift {
public:
    // TODO: davhar_too-г хадгална. Лифт 1 давхраас эхэлнэ, туулсан зам 0.
    Lift(int davhar_too) : odoo_(0), zam_(0) {
    }

    // TODO: davhar нь 1..davhar_too мужид байвал тэнд очиж, туулсан
    //       давхрын тоог zam_-д нэмээд true. Мужаас гадуур бол юу ч
    //       өөрчлөхгүй false.
    bool yavah(int davhar) {
        return false;
    }

    // Зөвхөн унших getter-ууд — талбарыг гаднаас өөрчлөх боломжгүй
    int odoo() const { return odoo_; }
    int zam() const { return zam_; }

private:
    // TODO: байшингийн давхрын тоог хадгалах талбар нэм
    int odoo_;   // одоогийн давхар
    int zam_;    // нийт туулсан давхар
};

// main бэлэн — Lift-ийн дотоод талбарт хүрэхгүй, зөвхөн методоор ажиллана
int main() {
    int n = 0;
    std::cin >> n;
    Lift lift(n);

    int davhar = 0;
    while (std::cin >> davhar) {
        if (lift.yavah(davhar)) {
            std::cout << davhar << " давхарт ирлээ\\n";
        } else {
            std::cout << "Алдаа: " << davhar << " давхар байхгүй\\n";
        }
    }

    // lift.odoo_ = 5;  <- private тул ХӨРВҮҮЛЭХГҮЙ
    std::cout << "Нийт " << lift.zam() << " давхар туулсан, одоо "
              << lift.odoo() << " давхарт байна.\\n";
    return 0;
}
""",
            exercise=ExerciseSpec(
                statement="""\
Байшингийн лифтийг `Lift` классаар загварчил. Давхрын тоо, одоогийн
давхар, туулсан замыг `private` талбарт хадгалж, зөвхөн `yavah()`
үйлдлээр өөрчилдөг болго — тэгвэл лифт хэзээ ч байхгүй давхарт очихгүй.
`main` ба `const` getter-ууд (`odoo()`, `zam()`) бэлэн, чи дараахийг
бичнэ:

- давхрын тоог хадгалах `private` талбар;
- `Lift(davhar_too)` — давхрын тоог хадгална, лифт **1-р давхраас**
  эхэлнэ, туулсан зам `0`;
- `yavah(davhar)` — `davhar` нь `1`–`davhar_too` мужид байвал тэнд очиж,
  туулсан давхрын тоог (хуучин ба шинэ давхрын зөрүүний абсолют утга)
  замд нэмээд `true` буцаана. Мужаас гадуур бол юу ч өөрчлөхгүй, `false`.

**Оролт:** эхний мөрөнд байшингийн давхрын тоо `N`, дараа нь файлын
төгсгөл хүртэл очих давхрууд (бүхэл тоо, `0` ба сөрөг байж болно).

**Гаралт:** хүсэлт бүрт `<d> давхарт ирлээ` эсвэл `Алдаа: <d> давхар
байхгүй`, төгсгөлд нь `Нийт <зам> давхар туулсан, одоо <давхар> давхарт
байна.` — энэ хэвлэлтийг `main` хийнэ.

**Хязгаарлалт:** `1 ≤ N ≤ 100`.
""",
                tests=(
                    TestCaseSpec(
                        stdin="10\n5\n3\n12\n3\n",
                        expected_output=(
                            "5 давхарт ирлээ\n"
                            "3 давхарт ирлээ\n"
                            "Алдаа: 12 давхар байхгүй\n"
                            "3 давхарт ирлээ\n"
                            "Нийт 6 давхар туулсан, одоо 3 давхарт байна.\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="5\n0\n-2\n6\n",
                        expected_output=(
                            "Алдаа: 0 давхар байхгүй\n"
                            "Алдаа: -2 давхар байхгүй\n"
                            "Алдаа: 6 давхар байхгүй\n"
                            "Нийт 0 давхар туулсан, одоо 1 давхарт байна.\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="1\n1\n2\n",
                        expected_output=(
                            "1 давхарт ирлээ\n"
                            "Алдаа: 2 давхар байхгүй\n"
                            "Нийт 0 давхар туулсан, одоо 1 давхарт байна.\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="100\n100\n1\n50\n",
                        expected_output=(
                            "100 давхарт ирлээ\n"
                            "1 давхарт ирлээ\n"
                            "50 давхарт ирлээ\n"
                            "Нийт 247 давхар туулсан, одоо 50 давхарт байна.\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="20\n",
                        expected_output="Нийт 0 давхар туулсан, одоо 1 давхарт байна.\n",
                    ),
                    TestCaseSpec(
                        stdin="12 7 13 2 7\n",
                        expected_output=(
                            "7 давхарт ирлээ\n"
                            "Алдаа: 13 давхар байхгүй\n"
                            "2 давхарт ирлээ\n"
                            "7 давхарт ирлээ\n"
                            "Нийт 16 давхар туулсан, одоо 7 давхарт байна.\n"
                        ),
                    ),
                ),
                solution="""\
#include <iostream>

class Lift {
public:
    // Лифт 1-р давхраас, туулсан зам 0-ээс эхэлнэ.
    // Жагсаалтын дараалал нь талбарыг зарласан дараалалтай ижил байна.
    Lift(int davhar_too) : davhar_too_(davhar_too), odoo_(1), zam_(0) {
    }

    bool yavah(int davhar) {
        // Мужаас гадуур бол төлөвт огт хүрэлгүй false
        if (davhar < 1 || davhar > davhar_too_) {
            return false;
        }
        // Туулсан давхар = зөрүүний абсолют утга (доош явахад ч эерэг)
        zam_ += davhar > odoo_ ? davhar - odoo_ : odoo_ - davhar;
        // Замыг тооцсоны ДАРАА л одоогийн давхрыг шинэчилнэ
        odoo_ = davhar;
        return true;
    }

    // Getter-ууд — гаднаас унших боломжтой ч өөрчлөх боломжгүй
    int odoo() const { return odoo_; }
    int zam() const { return zam_; }

private:
    // Дотоод төлөв — зөвхөн конструктор ба yavah() өөрчилнө
    int davhar_too_;
    int odoo_;
    int zam_;
};

int main() {
    int n = 0;
    std::cin >> n;
    Lift lift(n);

    int davhar = 0;
    while (std::cin >> davhar) {
        if (lift.yavah(davhar)) {
            std::cout << davhar << " давхарт ирлээ\\n";
        } else {
            std::cout << "Алдаа: " << davhar << " давхар байхгүй\\n";
        }
    }

    std::cout << "Нийт " << lift.zam() << " давхар туулсан, одоо "
              << lift.odoo() << " давхарт байна.\\n";
    return 0;
}
""",
                tips="""\
- `private:` хэсэгт давхрын тоог хадгалах талбар нэм (жишээ нь
  `davhar_too_`) ба конструкторын эхлүүлэгчийн жагсаалтад эхлүүл. Лифт
  `1`-р давхраас эхэлнэ — `0` биш.
- Эхлүүлэгчийн жагсаалтад талбаруудыг **зарласан дарааллаар нь** бич —
  эс бөгөөс хөрвүүлэгч анхааруулга (`-Wreorder`) өгнө.
- `yavah` дотор **эхлээд** мужийг шалга (`davhar < 1 || davhar > davhar_too_`),
  буруу бол юу ч өөрчлөлгүй `false`. Зөв бол эхлээд замд нэм, **дараа нь**
  одоогийн давхрыг шинэчил — эсрэгээр хийвэл зөрүү үргэлж `0` гарна.
- Зам нь хуучин ба шинэ давхрын зөрүүний **абсолют утга**. Шалгагч `0`,
  сөрөг, давхрын тооноос их давхар, одоогийн давхар руугаа дахин явах
  (зам нэмэгдэхгүй), нэг ч хүсэлтгүй оролтыг шалгана.
""",
            ),
        ),
    ],
)

COLLECTIONS = ModuleSpec(
    title="Модул 19 — C++ цуглуулга",
    description="std::array ба std::vector.",
    lessons=[
        LessonSpec(
            title="std::array",
            slug="std-array",
            description="Тогтмол хэмжээтэй аюулгүй массив.",
            duration=400,
            language=CPP,
            content="""\
C-ийн массивын асуудлууд: хэмжээгээ мэддэггүй, хязгаараа шалгадаггүй,
функцэд орохдоо заагч болдог.

`std::array` нь эдгээрийг бүгдийг шийднэ.

```cpp
#include <array>

std::array<int, 5> dunguud = {75, 82, 58, 91, 64};
```

`<int, 5>` нь «5 ширхэг `int`». Хэмжээ нь **төрлийн нэг хэсэг** тул
хөрвүүлэх үед мэдэгдэнэ.

### Давуу талууд

```cpp
dunguud.size();        // 5 — өөрөө мэднэ
dunguud.at(10);        // алдаа заагаад зогсоно (онцгой байдал шиднэ)
dunguud[10];           // хязгаар шалгахгүй — C-тэй ижил
```

`at()` нь аюулгүй, `[]` нь хурдан. Индекс нь найдвартай биш үед `at()`
ашигла.

### Функцэд дамжуулах

```cpp
void hevleh(const std::array<int, 5> &a) {
    std::cout << a.size() << "\\n";     // ажиллана!
}
```

Заагч болж хувирахгүй тул урт нь хадгалагдана. Уртыг тусдаа параметрээр
дамжуулах шаардлагагүй.

### Хуулагдана

```cpp
std::array<int, 3> a = {1, 2, 3};
std::array<int, 3> b = a;      // бүтэн хуулбар
```

C-ийн массив оноож болдоггүй байсан.

### Муж дээрх `for`

```cpp
for (int dun : dunguud) {
    std::cout << dun << " ";
}
```

### Ашигтай методууд

```cpp
a.front();     // эхний
a.back();      // сүүлчийн
a.fill(0);     // бүгдийг тэгээр
a.empty();     // хоосон эсэх
```

### Итератор: `begin()` ба `end()`

```cpp
auto it = dunguud.begin();   // эхний элемент рүү заана
std::cout << *it;            // 75 — заагч шиг * -ээр утгыг авна
it++;                        // дараагийн элемент рүү шилжинэ
```

`begin()` нь эхний элемент рүү, `end()` нь сүүлчийн элементийн **дараах**
байрлал руу заадаг **итератор** буцаана. Итератор нь Модул 9-ийн заагчтай
төстэй: `*it` нь утгыг өгнө, `it - dunguud.begin()` нь индексийг өгнө.
`end()` элемент рүү заадаггүй тул `*dunguud.end()` гэж бүү бич.

### Алгоритмуудтай ажиллана

`<algorithm>`, `<numeric>`-ийн бэлэн функцүүд нь `(begin(), end())` хосоор
«аль хэсэг дээр ажиллах»-ыг авна:

```cpp
#include <algorithm>
#include <numeric>

std::sort(a.begin(), a.end());                          // өсөхөөр эрэмбэлнэ
int niilber = std::accumulate(a.begin(), a.end(), 0);   // 0-ээс эхлэн нэмнэ
auto it = std::max_element(a.begin(), a.end());         // хамгийн их рүү заасан итератор
int ih = *it;                                           // утга
int indeks = it - a.begin();                            // байрлал
```

`std::max_element`, `std::min_element` нь утга биш **итератор** буцаана —
тэнцүү утга хэд байвал эхнийх рүү нь заана. Эдгээрийг гараар бичих
шаардлагагүй болсон.

### Хэзээ `array`, хэзээ `vector`

| Нөхцөл | Сонголт |
|---|---|
| Хэмжээ хөрвүүлэх үед тодорхой | `std::array` |
| Хэмжээ өөрчлөгдөнө | `std::vector` |

`std::array` нь стек дээр байрлана — хуваарилалт хийхгүй тул хурдан.

### Жишээ програм

```cpp
#include <algorithm>
#include <array>
#include <iostream>
#include <numeric>

void hevleh(const std::array<int, 5> &a);

int main() {
    std::array<int, 5> dunguud = {75, 82, 58, 91, 64};

    // Хэмжээгээ ӨӨРӨӨ мэднэ
    std::cout << "Хэмжээ: " << dunguud.size() << "\\n";
    std::cout << "Эхний:  " << dunguud.front() << "\\n";
    std::cout << "Сүүлчийн: " << dunguud.back() << "\\n\\n";

    hevleh(dunguud);

    // Алгоритмууд — гараар бичих шаардлагагүй
    int niilber = std::accumulate(dunguud.begin(), dunguud.end(), 0);
    auto ih = *std::max_element(dunguud.begin(), dunguud.end());
    auto bag = *std::min_element(dunguud.begin(), dunguud.end());

    std::cout << "\\nНийлбэр: " << niilber << "\\n";
    std::cout << "Дундаж:  " << static_cast<double>(niilber) / dunguud.size() << "\\n";
    std::cout << "Их: " << ih << ", бага: " << bag << "\\n";

    // Эрэмбэлэх
    std::sort(dunguud.begin(), dunguud.end());
    std::cout << "\\nЭрэмбэлсэн: ";
    for (int dun : dunguud) {
        std::cout << dun << " ";
    }
    std::cout << "\\n";

    // at() нь хязгаарыг шалгана: dunguud.at(10) гэвэл програм алдаа
    // заагаад зогсоно, харин dunguud[10] чимээгүй хог утга уншина
    std::cout << "at(4):  " << dunguud.at(4) << "\\n";

    return 0;
}

// Заагч болж хувирахгүй тул size() ажиллана
void hevleh(const std::array<int, 5> &a) {
    std::cout << "Функц дотор " << a.size() << " элемент харагдаж байна\\n";
}
```
""",
            initial_code="""\
#include <algorithm>
#include <array>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <string>

const std::array<std::string, 7> GARAG = {
    "Даваа", "Мягмар", "Лхагва", "Пүрэв", "Баасан", "Бямба", "Ням"
};

// Заагч болж хувирахгүй тул a.size() функц дотор ч ажиллана
double dundaj(const std::array<int, 7> &a) {
    // TODO: std::accumulate-аар нийлбэрийг олоод a.size()-д хуваана
    return 0.0;
}

int main() {
    std::array<int, 7> hem;
    for (int &t : hem) {
        std::cin >> t;
    }

    // TODO: 1. Дундаж — 2 оронтой (std::fixed, std::setprecision)

    // TODO: 2. Хамгийн дулаан ба хүйтэн өдөр — std::max_element,
    //          std::min_element. Индекс нь (it - hem.begin()).

    // TODO: 3. Дунджаас дулаан өдрийн тоо

    return 0;
}
""",
            exercise=ExerciseSpec(
                statement="""\
Долоо хоногийн өдөр бүрийн агаарын температурыг `std::array<int, 7>`-д
хадгалаад товч тайлан гарга. Өдрийн нэрс `GARAG` массивт бэлэн.

**Оролт:** Даваагаас Ням хүртэлх 7 бүхэл тоо (сөрөг байж болно), зай
эсвэл мөр таслалаар тусгаарлагдсан.

**Гаралт:** яг 4 мөр:

```text
Дундаж: <дундаж>
Хамгийн дулаан: <өдөр> (<температур>)
Хамгийн хүйтэн: <өдөр> (<температур>)
Дунджаас дулаан: <тоо> өдөр
```

- Дунджийг `std::fixed << std::setprecision(2)`-оор 2 оронтой хэвлэ.
- Хамгийн дулаан (хүйтэн) өдөр хэд байвал **хамгийн эхнийхийг** нь сонго —
  `std::max_element`, `std::min_element` яг ингэж ажилладаг.
- «Дунджаас дулаан» гэдэг нь температур нь дунджаас **хатуу их** өдөр.

Зөвлөгөө: итераторыг индекс болгохдоо `it - hem.begin()`.
""",
                tests=(
                    TestCaseSpec(
                        stdin="-5 0 3 7 12 4 3\n",
                        expected_output=(
                            "Дундаж: 3.43\n"
                            "Хамгийн дулаан: Баасан (12)\n"
                            "Хамгийн хүйтэн: Даваа (-5)\n"
                            "Дунджаас дулаан: 3 өдөр\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="20\n21\n22\n23\n24\n25\n26\n",
                        expected_output=(
                            "Дундаж: 23.00\n"
                            "Хамгийн дулаан: Ням (26)\n"
                            "Хамгийн хүйтэн: Даваа (20)\n"
                            "Дунджаас дулаан: 3 өдөр\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="5 5 5 5 5 5 5\n",
                        expected_output=(
                            "Дундаж: 5.00\n"
                            "Хамгийн дулаан: Даваа (5)\n"
                            "Хамгийн хүйтэн: Даваа (5)\n"
                            "Дунджаас дулаан: 0 өдөр\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="-10 -3 -15 -3 -8 -1 -20\n",
                        expected_output=(
                            "Дундаж: -8.57\n"
                            "Хамгийн дулаан: Бямба (-1)\n"
                            "Хамгийн хүйтэн: Ням (-20)\n"
                            "Дунджаас дулаан: 4 өдөр\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="1 9 3 9 0 -2 -2\n",
                        expected_output=(
                            "Дундаж: 2.57\n"
                            "Хамгийн дулаан: Мягмар (9)\n"
                            "Хамгийн хүйтэн: Бямба (-2)\n"
                            "Дунджаас дулаан: 3 өдөр\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="3 -4 0 0 0 0 0\n",
                        expected_output=(
                            "Дундаж: -0.14\n"
                            "Хамгийн дулаан: Даваа (3)\n"
                            "Хамгийн хүйтэн: Мягмар (-4)\n"
                            "Дунджаас дулаан: 6 өдөр\n"
                        ),
                    ),
                ),
                solution="""\
#include <algorithm>
#include <array>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <string>

const std::array<std::string, 7> GARAG = {
    "Даваа", "Мягмар", "Лхагва", "Пүрэв", "Баасан", "Бямба", "Ням"
};

// const лавлагаа — хуулбаргүй; std::array заагч болж хувирахгүй тул size() ажиллана
double dundaj(const std::array<int, 7> &a) {
    int niilber = std::accumulate(a.begin(), a.end(), 0);
    // Бүхэл хуваалт болохгүйн тулд double руу хөрвүүлж байж хуваана
    return static_cast<double>(niilber) / a.size();
}

int main() {
    std::array<int, 7> hem;
    // int &t — лавлагаа тул массив дахь элемент руу шууд уншина
    for (int &t : hem) {
        std::cin >> t;
    }

    double dun = dundaj(hem);
    // Утга биш ИТЕРАТОР буцаана; тэнцүү утгууд байвал эхнийхийг нь өгнө
    auto ih = std::max_element(hem.begin(), hem.end());
    auto bag = std::min_element(hem.begin(), hem.end());

    // Дунджаас ХАТУУ их өдрүүдийг тоолно
    int dulaan = 0;
    for (int t : hem) {
        if (t > dun) {
            dulaan++;
        }
    }

    std::cout << std::fixed << std::setprecision(2);
    std::cout << "Дундаж: " << dun << "\\n";
    // it - hem.begin() нь индекс (GARAG-д хэрэглэнэ), *it нь температур
    std::cout << "Хамгийн дулаан: " << GARAG[ih - hem.begin()] << " (" << *ih << ")\\n";
    std::cout << "Хамгийн хүйтэн: " << GARAG[bag - hem.begin()] << " (" << *bag << ")\\n";
    std::cout << "Дунджаас дулаан: " << dulaan << " өдөр\\n";
    return 0;
}
""",
                tips="""\
- Уншихдаа `for (int &t : hem)` гэж **лавлагаагаар** гүй — `&`-гүй бол
  хуулбар руу уншаад массив дахь утгууд хог хэвээр үлдэнэ.
- Дунджийг `std::accumulate(a.begin(), a.end(), 0)`-оор нийлбэр олоод
  `double` руу хөрвүүлж `a.size()`-д хуваа — бүхэл тоог бүхэлд хуваавал
  бутархай хэсэг алга болно. Хэвлэхээс өмнө `std::fixed << std::setprecision(2)`.
- `std::max_element` / `std::min_element` нь **итератор** буцаана: утга нь
  `*it`, индекс нь `it - hem.begin()`, өдрийн нэр нь `GARAG[индекс]`.
  Тэнцүү утгатай өдрүүд байвал эдгээр функц эхнийхийг нь автоматаар өгнө.
- «Дунджаас дулаан» нь `t > dundaj` — **хатуу** их. Шалгагч бүх өдөр ижил
  температуртай (хариу `0` өдөр), бүгд сөрөг, дундаж нь `0`-ээс арай бага
  сөрөг тоо гарах тохиолдлыг шалгана.
""",
            ),
        ),
        LessonSpec(
            title="std::vector",
            slug="std-vector",
            description="Хэмжээ нь өөрчлөгддөг цуглуулга.",
            duration=450,
            language=CPP,
            content="""\
`std::vector` нь хэмжээгээ **ажиллах үед** өөрчилж чадна. C++ -д хамгийн
их хэрэглэгддэг цуглуулга.

```cpp
#include <vector>

std::vector<int> toonuud;          // хоосон
std::vector<int> a = {1, 2, 3};
std::vector<int> b(10, 0);         // 10 ширхэг тэг
```

### Нэмэх ба хасах

```cpp
toonuud.push_back(42);
toonuud.pop_back();
toonuud.clear();
```

`push_back` нь зай хүрэхгүй бол **автоматаар** илүү том санах ой аваад
хуулна. Та юу ч хийх шаардлагагүй.

### Хэмжээ ба багтаамж

```cpp
v.size();       // хэдэн элемент байгаа
v.capacity();   // хэдэн элемент багтах зай авсан
v.reserve(100); // урьдчилан зай авна
```

Хэдэн элемент нэмэхээ мэдэж байвал `reserve` хийвэл дахин хуулах ажлыг
бүрэн арилгана. Том давталтад мэдэгдэхүйц хурдан болгоно.

### Хандах

```cpp
v[0];          // хязгаар шалгахгүй
v.at(0);       // шалгана, онцгой байдал шиднэ
v.front();
v.back();
```

### Хоосон вектор

```cpp
std::vector<int> v;
std::cout << v[0];        // ТОДОРХОЙГҮЙ ЗАН ТӨЛӨВ
std::cout << v.front();   // мөн адил
```

Ашиглахын өмнө `empty()`-ээр шалга.

### Дундаас хасах

```cpp
v.erase(v.begin() + 2);              // 2 дахь элементийг
v.insert(v.begin(), 0);              // эхэнд оруулах
```

Эдгээр нь үлдсэн элементийг **зөөдөг** тул удаан. Төгсгөлд нэмэх,
хасах нь хурдан.

### Итератор хүчингүй болох

```cpp
for (auto it = v.begin(); it != v.end(); ++it) {
    if (*it == 3) {
        v.erase(it);      // it одоо ХҮЧИНГҮЙ — цааш ашиглаж болохгүй
    }
}
```

`erase` нь шинэ итератор буцаадаг:

```cpp
for (auto it = v.begin(); it != v.end(); ) {
    if (*it == 3) {
        it = v.erase(it);
    } else {
        ++it;
    }
}
```

Энэ бол C++ -ийн сонгодог занга. Илүү энгийн шийдэл:

```cpp
v.erase(std::remove(v.begin(), v.end(), 3), v.end());
```

`std::remove` (`<algorithm>`) нь 3-тай тэнцүү **биш** элементүүдийг урагш
шахаж, шинэ төгсгөлийн итераторыг буцаана. `erase` нь тэр байрлалаас `end()`
хүртэлх илүү хэсгийг устгана.

### Хоёр хэмжээст

```cpp
std::vector<std::vector<int>> husnegt(3, std::vector<int>(4, 0));
```

3 мөр, 4 багана, бүгд тэг.

### Жишээ програм

```cpp
#include <algorithm>
#include <iostream>
#include <numeric>
#include <string>
#include <vector>

int main() {
    std::vector<int> toonuud;

    // Хэмжээ нь өөрчлөгдөнө — зай хүрэхгүй бол автоматаар өснө
    for (int i = 1; i <= 5; i++) {
        toonuud.push_back(i * 10);
    }

    std::cout << "Хэмжээ: " << toonuud.size() << "\\n";
    std::cout << "Элементүүд: ";
    for (int too : toonuud) {
        std::cout << too << " ";
    }
    std::cout << "\\n\\n";

    // Ашиглахын өмнө хоосон эсэхийг шалга
    if (!toonuud.empty()) {
        std::cout << "Эхний: " << toonuud.front() << "\\n";
        std::cout << "Сүүлчийн: " << toonuud.back() << "\\n\\n";
    }

    // Утга хасах — remove + erase хослол
    toonuud.push_back(30);
    std::cout << "30 нэмсний дараа: " << toonuud.size() << " элемент\\n";

    toonuud.erase(std::remove(toonuud.begin(), toonuud.end(), 30), toonuud.end());
    std::cout << "Бүх 30-г хассны дараа: " << toonuud.size() << " элемент\\n\\n";

    // Алгоритмууд
    int niilber = std::accumulate(toonuud.begin(), toonuud.end(), 0);
    std::cout << "Нийлбэр: " << niilber << "\\n";

    // Объектын вектор
    std::vector<std::string> nershuud = {"Дорж", "Бат", "Сараа"};
    std::sort(nershuud.begin(), nershuud.end());

    std::cout << "\\nЭрэмбэлсэн нэрс:\\n";
    for (const auto &ner : nershuud) {
        std::cout << "  " << ner << "\\n";
    }

    // Хоёр хэмжээст
    std::vector<std::vector<int>> husnegt(3, std::vector<int>(4, 0));
    husnegt[1][2] = 7;

    std::cout << "\\nХүснэгт:\\n";
    for (const auto &mur : husnegt) {
        for (int nudd : mur) {
            std::cout << nudd << " ";
        }
        std::cout << "\\n";
    }

    return 0;
}
```
""",
            initial_code="""\
#include <algorithm>
#include <iomanip>
#include <iostream>
#include <vector>

int main() {
    std::vector<int> toonuud;

    // TODO: 1. Файлын төгсгөл хүртэл тоо уншиж push_back хийнэ
    //          while (std::cin >> too) { ... }

    // TODO: 2. Хоосон бол «Тоо алга.» гэж хэвлээд дуусна

    // TODO: 3. std::sort-оор эрэмбэлээд тоо ширхэг, эрэмбэлсэн
    //          жагсаалт, медианыг хэвлэнэ

    return 0;
}
""",
            exercise=ExerciseSpec(
                statement="""\
Хэдэн тоо ирэхийг урьдчилан мэдэхгүй — `std::vector` яг үүнд зориулагдсан.
Файлын төгсгөл хүртэл бүхэл тоонуудыг уншаад эрэмбэлж, **медианыг** ол.

Медиан нь эрэмбэлсэн жагсаалтын голын утга. Тоо ширхэг тэгш бол голын
хоёр утгын дундаж.

**Оролт:** зай эсвэл мөр таслалаар тусгаарласан бүхэл тоонууд. Тоо огт
байхгүй байж болно.

**Гаралт:** тоо байхгүй бол ганц мөр `Тоо алга.`, эс бөгөөс гурван мөр:

```text
Тоо: <ширхэг>
Эрэмбэлсэн: <тоонууд нэг зайгаар>
Медиан: <медиан>
```

Медианыг `std::fixed << std::setprecision(1)`-ээр 1 оронтой хэвлэ.

**Хязгаарлалт:** тоо бүрийн абсолют утга `1 000 000`-аас хэтрэхгүй.

Зөвлөгөө: хоосон вектор дээр `[]`, `front()` дуудах нь тодорхойгүй зан
төлөв — эхлээд `empty()`-ээр шалга. Бүхэл тоог `2.0`-д хуваавал бутархай
гарна.
""",
                tests=(
                    TestCaseSpec(
                        stdin="5 3 9 1 8 2 9\n",
                        expected_output="Тоо: 7\nЭрэмбэлсэн: 1 2 3 5 8 9 9\nМедиан: 5.0\n",
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="4 1 3 2\n",
                        expected_output="Тоо: 4\nЭрэмбэлсэн: 1 2 3 4\nМедиан: 2.5\n",
                        sample=True,
                    ),
                    TestCaseSpec(stdin="\n", expected_output="Тоо алга.\n"),
                    TestCaseSpec(
                        stdin="42\n",
                        expected_output="Тоо: 1\nЭрэмбэлсэн: 42\nМедиан: 42.0\n",
                    ),
                    TestCaseSpec(
                        stdin="-3\n-1\n-2\n-10\n",
                        expected_output="Тоо: 4\nЭрэмбэлсэн: -10 -3 -2 -1\nМедиан: -2.5\n",
                    ),
                    TestCaseSpec(
                        stdin="1000000 -1000000\n",
                        expected_output="Тоо: 2\nЭрэмбэлсэн: -1000000 1000000\nМедиан: 0.0\n",
                    ),
                    TestCaseSpec(
                        stdin="7 7 7 7 7 7 7 7 7 7 1\n",
                        expected_output="Тоо: 11\nЭрэмбэлсэн: 1 7 7 7 7 7 7 7 7 7 7\nМедиан: 7.0\n",
                    ),
                ),
                solution="""\
#include <algorithm>
#include <iomanip>
#include <iostream>
#include <vector>

int main() {
    std::vector<int> toonuud;
    int too = 0;
    // Уншилт бүтэлгүйтэх (файлын төгсгөл) хүртэл — вектор өөрөө томорно
    while (std::cin >> too) {
        toonuud.push_back(too);
    }

    // Хоосон вектор дээр [] ашиглах нь тодорхойгүй зан төлөв — эхлээд шалгана
    if (toonuud.empty()) {
        std::cout << "Тоо алга.\\n";
        return 0;
    }

    std::sort(toonuud.begin(), toonuud.end());

    std::cout << "Тоо: " << toonuud.size() << "\\n";
    // Тоо бүрийн ӨМНӨ зай хэвлэснээр мөрийн төгсгөлд илүү зай үлдэхгүй
    std::cout << "Эрэмбэлсэн:";
    for (int t : toonuud) {
        std::cout << " " << t;
    }
    std::cout << "\\n";

    std::size_t n = toonuud.size();
    double median = 0.0;
    if (n % 2 == 1) {
        // Сондгой тоо: яг голын элемент
        median = toonuud[n / 2];
    } else {
        // Тэгш тоо: голын хоёрын дундаж — 2.0-д хуваавал бутархай хадгалагдана
        median = (toonuud[n / 2 - 1] + toonuud[n / 2]) / 2.0;
    }

    std::cout << std::fixed << std::setprecision(1);
    std::cout << "Медиан: " << median << "\\n";
    return 0;
}
""",
                tips="""\
- `while (std::cin >> too)` давталтаар файлын төгсгөл хүртэл уншиж
  `push_back` хий — хэдэн тоо ирэхийг урьдчилан мэдэх шаардлагагүй.
- Юуны өмнө `empty()`-ээр шалга: тоо огт байхгүй бол `Тоо алга.` хэвлээд
  дуусга. Хоосон вектор дээр `[]` дуудах нь тодорхойгүй зан төлөв.
- `std::sort(toonuud.begin(), toonuud.end())`-оор эрэмбэлээд `n = size()`
  ол: сондгой бол `toonuud[n / 2]`, тэгш бол `toonuud[n / 2 - 1]` ба
  `toonuud[n / 2]`-ийн дундаж. `2`-т хуваавал бүхэл хуваалт болж `.5`
  алга болно — `2.0`-д хуваа.
- Шалгагч ганц тоо, сөрөг тоонууд (медиан нь сөрөг бутархай), давхардсан
  тоо, олон мөрөнд тархсан оролтыг шалгана. Медианыг
  `std::fixed << std::setprecision(1)`-ээр хэвлэж, эрэмбэлсэн тоонуудын
  хооронд яг нэг зай тавь.
""",
            ),
        ),
    ],
)

CPP_CORE_MODULES = [STRINGS, REFERENCES, OOP, COLLECTIONS]
