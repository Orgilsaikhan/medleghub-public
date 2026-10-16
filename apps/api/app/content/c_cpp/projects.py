"""Модул 20-21 — C ба C++ төслүүд.

Хичээлүүдэд үзсэнээ нэгтгэсэн бүтэн програмууд. Тус бүр нь хуулж
хөрвүүлээд шууд ажиллана.
"""

from app.content.types import ExerciseSpec, LessonSpec, ModuleSpec, TestCaseSpec
from app.models.enums import LessonLanguage

C = LessonLanguage.C
CPP = LessonLanguage.CPP

C_PROJECTS = ModuleSpec(
    title="Модул 20 — C төслүүд",
    description="C-ийн мэдлэгээ нэгтгэсэн дөрвөн програм.",
    lessons=[
        LessonSpec(
            title="Төсөл — Тооцоолуур",
            slug="c-tootsooluur",
            description="Цэс, switch, оролт шалгалт.",
            duration=660,
            language=C,
            content="""\
Дөрвөн үйлдлийн тооцоолуур. Хэрэглэх зүйлс: `switch`, функц, `scanf`-ийн
шалгалт, `do while` цэс.

### Бүтэц

Нэг том `main` бичихийн оронд ажлыг хуваа:

```c
double bodoh(double a, char uildel, double b, int *amjilttai);
void tses_haruulah(void);
int too_unshih(const char *asuult, double *ur);
```

### Оролтыг үргэлж шалга

```c
if (scanf("%lf", &a) != 1) {
    printf("Тоо оруулна уу\\n");
    return 0;
}
```

`scanf` нь **амжилттай уншсан утгын тоог** буцаана: `"%lf"` бол 1,
`"%lf %c %lf"` бол 3. Хэрэглэгч тооны оронд үг бичвэл түүнээс бага тоо
буцаана — тэгэхээр хувьсагчид хог утга үлдсэн гэсэн үг.

`double` уншихад `%lf`, хэвлэхэд `%f` гэдгийг анхаар — энэ ялгаа
`scanf`-д л байдаг.

### Тэгд хуваах

C нь бүхэл тоог тэгд хуваахад програмыг **унагаана**. Бутархайд
`inf` эсвэл `nan` өгнө. Аль ч тохиолдолд өөрөө шалгах хэрэгтэй.

### Амжилтыг тусад нь буцаах

```c
double bodoh(double a, char uildel, double b, int *amjilttai) {
    *amjilttai = 1;

    switch (uildel) {
        case '/':
            if (b == 0) {
                *amjilttai = 0;
                return 0;
            }
            return a / b;
    }
}
```

Буцаах утга нь **үр дүн**, заагч нь **амжилт эсэх**. Модул 9-д үзсэн
загвар.

### Нэмэлт сорилт

1. Зэрэг дэвшүүлэх үйлдэл нэмээрэй (`<math.h>`-ийн `pow`).
2. Сүүлийн үр дүнг санаж, дараагийн тооцоололд ашиглаарай.
3. Үлдэгдэл (`%`) үйлдлийг бүхэл тоонд нэмээрэй.

### Жишээ програм

```c
#include <stdio.h>

double bodoh(double a, char uildel, double b, int *amjilttai);
void tses_haruulah(void);

int main(void) {
    double a;
    double b;
    char uildel;
    char ur_tsag;

    do {
        tses_haruulah();

        printf("Эхний тоо: ");
        if (scanf("%lf", &a) != 1) {
            printf("Тоо оруулна уу.\\n");
            return 1;
        }

        printf("Үйлдэл (+ - * /): ");
        if (scanf(" %c", &uildel) != 1) {
            printf("Үйлдэл оруулна уу.\\n");
            return 1;
        }

        printf("Хоёр дахь тоо: ");
        if (scanf("%lf", &b) != 1) {
            printf("Тоо оруулна уу.\\n");
            return 1;
        }

        int amjilttai;
        double ur = bodoh(a, uildel, b, &amjilttai);

        if (amjilttai) {
            printf("\\n%.2f %c %.2f = %.2f\\n", a, uildel, b, ur);
        } else {
            printf("\\nБодож чадсангүй. Тэгд хуваах, эсвэл танихгүй үйлдэл.\\n");
        }

        printf("\\nДахин бодох уу? (t/u): ");
        scanf(" %c", &ur_tsag);

    } while (ur_tsag == 't' || ur_tsag == 'T');

    printf("Баяртай.\\n");
    return 0;
}

/* Буцаах утга нь үр дүн, заагч нь амжилт эсэх */
double bodoh(double a, char uildel, double b, int *amjilttai) {
    *amjilttai = 1;

    switch (uildel) {
        case '+':
            return a + b;
        case '-':
            return a - b;
        case '*':
            return a * b;
        case '/':
            if (b == 0) {
                *amjilttai = 0;
                return 0;
            }
            return a / b;
        default:
            *amjilttai = 0;
            return 0;
    }
}

void tses_haruulah(void) {
    printf("\\n=== Тооцоолуур ===\\n");
}
```
""",
            initial_code="""\
#include <stdio.h>

#define AMJILTTAI 0
#define TEGD_HUVAAH 1
#define TANIHGUI 2

/* a uildel b-г бодно. Амжилттай бол хариуг *ur-д бичээд AMJILTTAI буцаана.
   Тэгд хуваах бол TEGD_HUVAAH, танихгүй үйлдэл бол TANIHGUI буцаана. */
int bodoh(double a, char uildel, double b, double *ur) {
    /* TODO: switch ашиглан + - * / үйлдлийг гүйцэтгэ */
    return TANIHGUI;
}

int main(void) {
    int n;
    if (scanf("%d", &n) != 1) {
        printf("Оролт буруу.\\n");
        return 1;
    }

    int amjilttai = 0;

    for (int i = 0; i < n; i++) {
        double a;
        double b;
        char uildel;

        /* TODO: «a uildel b»-г нэг scanf-аар уншиж, амжилттай эсэхийг шалга */

        /* TODO: bodoh-г дуудаж, хариу эсвэл алдааны мөрийг хэвлэ */
    }

    /* TODO: «Амжилттай: K / N» мөрийг хэвлэ */

    return 0;
}
""",
            exercise=ExerciseSpec(
                statement="""\
Тооцоолуурыг шалгагдах хэлбэрт оруулъя: програм эхлээд хэдэн илэрхийлэл
бодохоо уншаад, тус бүрийг бодож хариуг хэвлэнэ.

**Оролт:** эхний мөрөнд илэрхийллийн тоо `N` (0 ≤ N ≤ 20). Дараагийн `N`
мөр бүрт `<a> <үйлдэл> <b>` — `a`, `b` нь бодит тоо, үйлдэл нь нэг тэмдэгт.

**Гаралт:** илэрхийлэл бүрт нэг мөр:

- `+`, `-`, `*`, `/` бол `<a> <үйлдэл> <b> = <хариу>` — гурван тоог бүгдийг
  `%.2f` форматаар, жишээ нь `12.00 + 8.00 = 20.00`.
- Тэгд хуваах бол `Алдаа: тэгд хуваах боломжгүй`.
- Өөр тэмдэгт бол `Алдаа: танихгүй үйлдэл <тэмдэгт>`.
- Илэрхийллийг уншиж чадахгүй бол (жишээ нь тооны оронд үг) `Оролт буруу.`
  гэж хэвлээд програмыг **шууд** дуусгана.

Бүх илэрхийллийг бодсоны дараа сүүлийн мөрөнд `Амжилттай: <K> / <N>` —
`K` нь хариу гарсан илэрхийллийн тоо.

Цэс, «Эхний тоо:» гэх мэт асуулт **бүү хэвлэ** — шалгагч зөвхөн гаралтыг
харьцуулна.
""",
                tests=(
                    TestCaseSpec(
                        stdin="4\n12 + 8\n50 - 17.5\n10 / 4\n5 / 0\n",
                        expected_output=(
                            "12.00 + 8.00 = 20.00\n"
                            "50.00 - 17.50 = 32.50\n"
                            "10.00 / 4.00 = 2.50\n"
                            "Алдаа: тэгд хуваах боломжгүй\n"
                            "Амжилттай: 3 / 4\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="0\n",
                        expected_output="Амжилттай: 0 / 0\n",
                    ),
                    TestCaseSpec(
                        stdin="4\n-4.5 * 2\n2 ^ 3\n-9 / -3\n7 % 2\n",
                        expected_output=(
                            "-4.50 * 2.00 = -9.00\n"
                            "Алдаа: танихгүй үйлдэл ^\n"
                            "-9.00 / -3.00 = 3.00\n"
                            "Алдаа: танихгүй үйлдэл %\n"
                            "Амжилттай: 2 / 4\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="3\n2 + 2\nхоёр * 3\n1 + 1\n",
                        expected_output="2.00 + 2.00 = 4.00\nОролт буруу.\n",
                    ),
                    TestCaseSpec(
                        stdin="3\n1 / 3\n0 / 0\n6 * 7\n",
                        expected_output=(
                            "1.00 / 3.00 = 0.33\n"
                            "Алдаа: тэгд хуваах боломжгүй\n"
                            "6.00 * 7.00 = 42.00\n"
                            "Амжилттай: 2 / 3\n"
                        ),
                    ),
                ),
                solution="""\
#include <stdio.h>

/* bodoh() функцийн буцаах төлөвийн кодууд */
#define AMJILTTAI 0
#define TEGD_HUVAAH 1
#define TANIHGUI 2

/* Нэг илэрхийллийг бодно: хариуг *ur-д бичиж, төлөвийн код буцаана */
int bodoh(double a, char uildel, double b, double *ur) {
    switch (uildel) {
        case '+':
            *ur = a + b;
            return AMJILTTAI;
        case '-':
            *ur = a - b;
            return AMJILTTAI;
        case '*':
            *ur = a * b;
            return AMJILTTAI;
        case '/':
            /* Хуваахаас ӨМНӨ тэгийг шалгана (0 / 0 ч мөн адил) */
            if (b == 0) {
                return TEGD_HUVAAH;
            }
            *ur = a / b;
            return AMJILTTAI;
        default:
            /* + - * / биш бүх тэмдэгт */
            return TANIHGUI;
    }
}

int main(void) {
    /* Эхлээд хэдэн илэрхийлэл бодохыг уншина */
    int n;
    if (scanf("%d", &n) != 1) {
        printf("Оролт буруу.\\n");
        return 1;
    }

    int amjilttai = 0; /* хариу гарсан илэрхийллийн тоо (K) */

    for (int i = 0; i < n; i++) {
        double a;
        double b;
        char uildel;

        /* «a uildel b»-г нэг scanf-аар уншина: 3 утга авч чадаагүй бол
           оролт буруу — нэгтгэл хэвлэлгүй шууд дуусна */
        if (scanf("%lf %c %lf", &a, &uildel, &b) != 3) {
            printf("Оролт буруу.\\n");
            return 1;
        }

        double ur = 0.0;
        int tuluv = bodoh(a, uildel, b, &ur);

        /* Төлөвөөс хамаарч хариу эсвэл алдааны мөр хэвлэнэ */
        if (tuluv == AMJILTTAI) {
            printf("%.2f %c %.2f = %.2f\\n", a, uildel, b, ur);
            amjilttai++;
        } else if (tuluv == TEGD_HUVAAH) {
            printf("Алдаа: тэгд хуваах боломжгүй\\n");
        } else {
            printf("Алдаа: танихгүй үйлдэл %c\\n", uildel);
        }
    }

    /* Бүх илэрхийллийн дараа нэгтгэл — N = 0 үед ч хэвлэнэ */
    printf("Амжилттай: %d / %d\\n", amjilttai, n);
    return 0;
}
""",
                tips="""\
- Эхлээд `N`-ийг уншаад `for` давталтаар яг `N` удаа эргэ. Илэрхийлэл бүрийг
  нэг `scanf("%lf %c %lf", &a, &uildel, &b)`-аар уншаад буцаах утга нь `3`
  эсэхийг шалга.
- Бодох ажлыг тусдаа функцэд гарга: хариуг заагчаар (`double *ur`) буцааж,
  функцийн буцаах утгаар төлөвийг (амжилттай / тэгд хуваах / танихгүй)
  илэрхийл. `switch`-ийн `default` нь `+ - * /`-ээс бусад бүх тэмдэгтийг барина.
- `/` үйлдэлд хуваахаас **өмнө** `b == 0` эсэхийг шалга — хуваагдагч нь бас 0
  байсан ч тэгд хуваалт хэвээр.
- Оролт буруу бол `Оролт буруу.` гэж хэвлээд `return`-ээр шууд гар — энэ үед
  `Амжилттай: ...` мөр **хэвлэгдэхгүй**, харин өмнө нь бодсон мөрүүд үлдэнэ.
- `K`-г зөвхөн хариу гарсан үед нэмэгдүүл. `N = 0` байсан ч сүүлийн мөр
  хэвлэгдэнэ. Сөрөг тоо, бутархай хариуг `%.2f` өөрөө зөв дугуйлна.
""",
            ),
        ),
        LessonSpec(
            title="Төсөл — Тоо таах тоглоом",
            slug="c-too-taah-togloom",
            description="Санамсаргүй тоо, давталт, сануулга.",
            duration=660,
            language=C,
            content="""\
Компьютер 1-100 хооронд тоо санана. Хэрэглэгч таана.

### Санамсаргүй тоо

```c
#include <stdlib.h>
#include <time.h>

srand((unsigned) time(NULL));
int nuuts = rand() % 100 + 1;
```

`srand` нь генераторын үр (seed) тавина. **Нэг л удаа**, програмын эхэнд
дуудна. Давталт дотор дуудвал ижил тоо гарсаар байна.

`time(NULL)` нь одоогийн секунд — тиймээс ажиллуулах бүрд өөр үр.

> `rand() % 100` нь жигд бус хуваарилалт өгдөг сул талтай. Тоглоомд
> хангалттай, харин криптографт **хэзээ ч** бүү ашигла.

### Давталт

```c
while (oroldlogo < MAX_OROLDLOGO) {
    /* таалт авах */
    if (taalt == nuuts) break;
    /* сануулга өгөх */
}
```

### Оролт шалгах

`scanf` нь амжилттай уншсан утгын тоог буцаана. Хэрэглэгч тоо биш зүйл
бичвэл `scanf` нь **0** буцаана, оролт бүр дууссан бол тусгай утга **`EOF`**
(`<stdio.h>`-д тодорхойлсон, ихэвчлэн −1) буцаана.

Амжилтгүй болсон үг буферт **үлддэг** — дараагийн `scanf` ч тэр үгэн дээр
дахин бүтэлгүйтэнэ. Тиймээс мөрийн үлдсэнийг алгасна:

```c
if (scanf("%d", &taalt) != 1) {
    int c;
    while ((c = getchar()) != '\\n' && c != EOF) { }
    continue;
}
```

`getchar()` нь оролтоос **нэг тэмдэгт** уншиж буцаана (оролт дууссан бол
`EOF`). `(c = getchar()) != '\\n'` нь эхлээд тэмдэгтийг `c`-д хадгалаад,
дараа нь мөр таслал мөн эсэхийг шалгана. Ингэж мөр таслал эсвэл оролтын
төгсгөл хүртэл нэг нэгээр нь уншиж хаяна. `c`-г `char` биш `int` болгосон нь
`EOF`-ийг жирийн тэмдэгтээс ялгахын тулд.

Энэ мөрийг орхивол програм хариу өгөхөө болино — сургалтын явцад олон
хүн энэ асуудалтай тулгардаг.

### Нэмэлт сорилт

1. Хэцүү байдлын түвшин нэмээрэй (муж болон оролдлогын тоог өөрчилнө).
2. Хамгийн бага оролдлогын дүнг файлд хадгалаарай.
3. Хэрэглэгчийн өмнөх таалтуудыг хэвлээрэй.

### Жишээ програм

```c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define DEED_HYAZGAAR 100
#define MAX_OROLDLOGO 7

int main(void) {
    /* Үр НЭГ л удаа тавина */
    srand((unsigned) time(NULL));
    int nuuts = rand() % DEED_HYAZGAAR + 1;

    int oroldlogo = 0;
    int taalt = 0;
    int oldson = 0;

    printf("=== Тоо таах тоглоом ===\\n");
    printf("1-ээс %d хооронд тоо санав.\\n", DEED_HYAZGAAR);
    printf("Танд %d оролдлого байна.\\n\\n", MAX_OROLDLOGO);

    while (oroldlogo < MAX_OROLDLOGO) {
        printf("%d дэх таалт: ", oroldlogo + 1);

        if (scanf("%d", &taalt) != 1) {
            printf("Тоо оруулна уу.\\n");

            /* Буферийг цэвэрлэхгүй бол давталт мөнхөд эргэнэ */
            int c;
            while ((c = getchar()) != '\\n' && c != EOF) {
            }
            continue;
        }

        oroldlogo++;

        if (taalt == nuuts) {
            oldson = 1;
            break;
        }

        if (taalt < nuuts) {
            printf("  Илүү ИХ тоо.\\n");
        } else {
            printf("  Илүү БАГА тоо.\\n");
        }

        printf("  Үлдсэн оролдлого: %d\\n\\n", MAX_OROLDLOGO - oroldlogo);
    }

    printf("\\n");
    if (oldson) {
        printf("Зөв! Нууц тоо %d байлаа. %d оролдлогод оллоо.\\n", nuuts, oroldlogo);
    } else {
        printf("Оролдлого дууслаа. Нууц тоо %d байсан.\\n", nuuts);
    }

    return 0;
}
```
""",
            initial_code="""\
#include <stdio.h>

#define DOOD 1
#define DEED 100
#define MAX_OROLDLOGO 7

int main(void) {
    int nuuts;
    if (scanf("%d", &nuuts) != 1) {
        return 1;
    }

    int oroldlogo = 0;

    while (oroldlogo < MAX_OROLDLOGO) {
        int taalt;
        int unshsan = scanf("%d", &taalt);

        if (unshsan == EOF) {
            return 0;   /* оролт дууслаа */
        }

        /* TODO: тоо биш бол сануулаад мөрийн үлдсэнийг getchar-аар алгас.
           Алгасахгүй бол scanf дахин дахин бүтэлгүйтэж давталт мөнхөд эргэнэ. */

        /* TODO: 1-100-аас гадуур бол сануул — оролдлогод тооцохгүй */

        /* TODO: оролдлогыг тоолж, зөв бол дуусга, эс бөгөөс их/бага гэж хэл */
    }

    /* TODO: 7 оролдлого дууссан бол нууц тоог хэлнэ */

    return 0;
}
""",
            exercise=ExerciseSpec(
                statement="""\
Тоо таах тоглоомыг шалгагдах хэлбэрт оруулъя. Санамсаргүй тооны оронд нууц
тоог оролтоос уншина — ингэснээр тест бүр ижил үр дүн өгнө.

**Оролт:** эхний мөрөнд нууц тоо `S` (1 ≤ S ≤ 100). Дараагийн мөр бүрт
тоглогчийн нэг таалт. Тоглоом дуустал хангалттай мөр үргэлж байна.

**Гаралт:** таалт бүрт нэг мөр:

- Тоо биш бол `Тоо оруулна уу.` — тэр мөрийн үлдсэн хэсгийг алгасна.
- 1–100-аас гадуур бол `1-100 хооронд тоо оруулна уу.`
- `S`-ээс бага бол `Илүү их. Үлдсэн оролдлого: <R>`, их бол
  `Илүү бага. Үлдсэн оролдлого: <R>`.
- Зөв бол `Зөв! <K> оролдлогод оллоо.` гэж хэвлээд програм дуусна — үлдсэн
  мөрүүдийг уншихгүй.

Эхний хоёр тохиолдол оролдлогод **тооцогдохгүй**. Нийт **7** оролдлого
байна: `R` нь энэ таалтын дараа үлдсэн оролдлого, `K` нь зөв таасан
оролдлогын дугаар. 7 дахь оролдлого ч буруу бол сүүлийн сануулгын дараа
`Оролдлого дууслаа. Нууц тоо <S> байсан.` гэж хэвлэнэ.

«1 дэх таалт:» гэх мэт асуулт **бүү хэвлэ** — шалгагч зөвхөн гаралтыг
харьцуулна.
""",
                tests=(
                    TestCaseSpec(
                        stdin="42\n50\n25\n42\n",
                        expected_output=(
                            "Илүү бага. Үлдсэн оролдлого: 6\n"
                            "Илүү их. Үлдсэн оролдлого: 5\n"
                            "Зөв! 3 оролдлогод оллоо.\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="15\nарав\n150\n10\n15\n",
                        expected_output=(
                            "Тоо оруулна уу.\n"
                            "1-100 хооронд тоо оруулна уу.\n"
                            "Илүү их. Үлдсэн оролдлого: 6\n"
                            "Зөв! 2 оролдлогод оллоо.\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="77\n10\n20\n30\n40\n50\n60\n70\n",
                        expected_output=(
                            "Илүү их. Үлдсэн оролдлого: 6\n"
                            "Илүү их. Үлдсэн оролдлого: 5\n"
                            "Илүү их. Үлдсэн оролдлого: 4\n"
                            "Илүү их. Үлдсэн оролдлого: 3\n"
                            "Илүү их. Үлдсэн оролдлого: 2\n"
                            "Илүү их. Үлдсэн оролдлого: 1\n"
                            "Илүү их. Үлдсэн оролдлого: 0\n"
                            "Оролдлого дууслаа. Нууц тоо 77 байсан.\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="64\n50\n75\n62\n68\n65\n63\n64\n",
                        expected_output=(
                            "Илүү их. Үлдсэн оролдлого: 6\n"
                            "Илүү бага. Үлдсэн оролдлого: 5\n"
                            "Илүү их. Үлдсэн оролдлого: 4\n"
                            "Илүү бага. Үлдсэн оролдлого: 3\n"
                            "Илүү бага. Үлдсэн оролдлого: 2\n"
                            "Илүү их. Үлдсэн оролдлого: 1\n"
                            "Зөв! 7 оролдлогод оллоо.\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="7\n7\n8\n9\n",
                        expected_output="Зөв! 1 оролдлогод оллоо.\n",
                    ),
                    TestCaseSpec(
                        stdin="100\n1\nзуу\n101\n0\n99\n100\n",
                        expected_output=(
                            "Илүү их. Үлдсэн оролдлого: 6\n"
                            "Тоо оруулна уу.\n"
                            "1-100 хооронд тоо оруулна уу.\n"
                            "1-100 хооронд тоо оруулна уу.\n"
                            "Илүү их. Үлдсэн оролдлого: 5\n"
                            "Зөв! 3 оролдлогод оллоо.\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="1\n2\n-5\n3\n4\nx\n5\n6\n7\n8\n",
                        expected_output=(
                            "Илүү бага. Үлдсэн оролдлого: 6\n"
                            "1-100 хооронд тоо оруулна уу.\n"
                            "Илүү бага. Үлдсэн оролдлого: 5\n"
                            "Илүү бага. Үлдсэн оролдлого: 4\n"
                            "Тоо оруулна уу.\n"
                            "Илүү бага. Үлдсэн оролдлого: 3\n"
                            "Илүү бага. Үлдсэн оролдлого: 2\n"
                            "Илүү бага. Үлдсэн оролдлого: 1\n"
                            "Илүү бага. Үлдсэн оролдлого: 0\n"
                            "Оролдлого дууслаа. Нууц тоо 1 байсан.\n"
                        ),
                    ),
                ),
                solution="""\
#include <stdio.h>

/* Хүчинтэй муж ба оролдлогын дээд хэмжээ */
#define DOOD 1
#define DEED 100
#define MAX_OROLDLOGO 7

int main(void) {
    /* Эхний мөр — нууц тоо (санамсаргүй тооны оронд) */
    int nuuts;
    if (scanf("%d", &nuuts) != 1) {
        return 1;
    }

    int oroldlogo = 0; /* зөвхөн хүчинтэй таалтыг тоолно */

    while (oroldlogo < MAX_OROLDLOGO) {
        int taalt;
        /* scanf: 1 = тоо уншсан, 0 = тоо биш, EOF = оролт дууссан */
        int unshsan = scanf("%d", &taalt);

        if (unshsan == EOF) {
            return 0;
        }

        /* 1) Тоо биш — оролдлогод тооцохгүй */
        if (unshsan != 1) {
            printf("Тоо оруулна уу.\\n");
            /* Буферийг цэвэрлэхгүй бол давталт мөнхөд эргэнэ */
            int c;
            while ((c = getchar()) != '\\n' && c != EOF) {
            }
            continue;
        }

        /* 2) Мужаас гадуур — мөн оролдлогод тооцохгүй */
        if (taalt < DOOD || taalt > DEED) {
            printf("%d-%d хооронд тоо оруулна уу.\\n", DOOD, DEED);
            continue;
        }

        /* Хүчинтэй таалт — одоо л оролдлогыг тоолно */
        oroldlogo++;

        /* 3) Зөв бол шууд дуусгана, үлдсэн мөрийг уншихгүй */
        if (taalt == nuuts) {
            printf("Зөв! %d оролдлогод оллоо.\\n", oroldlogo);
            return 0;
        }

        /* 4) Их/бага сануулга ба үлдсэн оролдлого */
        if (taalt < nuuts) {
            printf("Илүү их. ");
        } else {
            printf("Илүү бага. ");
        }
        printf("Үлдсэн оролдлого: %d\\n", MAX_OROLDLOGO - oroldlogo);
    }

    /* 7 оролдлого бүгд буруу байсан */
    printf("Оролдлого дууслаа. Нууц тоо %d байсан.\\n", nuuts);
    return 0;
}
""",
                tips="""\
- Эхний тоо нь нууц тоо. Дараа нь `while (oroldlogo < 7)` давталтаар таалт
  унш. `scanf`-ийн буцаах утгыг хувьсагчид хадгалж, `1` (тоо), `0` (тоо биш),
  `EOF` (оролт дууссан) гэсэн гурван тохиолдлыг ялга.
- Шалгах дараалал: тоо эсэх → 1–100 мужид эсэх → **зөвхөн дараа нь**
  оролдлогыг нэмэгдүүл → зөв эсэх → их/бага. Эхний хоёр алдаа оролдлого
  «иддэггүй» тул `continue` хий.
- Тоо биш үед мөрийн үлдсэнийг `getchar()`-аар `'\\n'` хүртэл алгас. Эс бөгөөс
  `scanf` ижил үгэн дээр дахин дахин бүтэлгүйтэж, давталт мөнхөд эргэнэ.
- Зөв таасан бол мөрөө хэвлээд шууд `return 0` — дараагийн мөрүүдийг
  уншихгүй. 7 дахь оролдлогод таасан ч `Зөв!` гарах ёстой.
- `R` нь оролдлогыг нэмэгдүүлсний **дараах** `7 - oroldlogo`. Мужийн хил
  (`1`, `100`) хүчинтэй, `0` болон сөрөг тоо хүчингүй гэдгийг анхаар.
""",
            ),
        ),
        LessonSpec(
            title="Төсөл — Дүнгийн тооцоолуур",
            slug="c-dungiin-tootsooluur",
            description="Бүтэц, массив, статистик.",
            duration=720,
            language=C,
            content="""\
Оюутнуудын дүнг уншиж, статистик гаргах програм.

### Өгөгдлийн бүтэц

```c
typedef struct {
    char ner[50];
    double dun[HICHEEL];
    double dundaj;
    char unelgee;
} Oyutan;
```

Дундаж болон үнэлгээг **хадгалах** уу, эсвэл **шаардлагатай үед
тооцоолох** уу?

| Арга | Давуу тал | Сул тал |
|---|---|---|
| Хадгалах | Хурдан | Дүн өөрчлөгдөхөд шинэчлэх ёстой |
| Тооцоолох | Үргэлж зөв | Давтан тооцоолно |

Жижиг програмд тооцоолох нь аюулгүй. Энд хадгалах хувилбарыг үзүүлэв —
гэхдээ `dundaj_shinechleh` функцээр төвлөрүүлсэн.

### Статистик

```c
double dundaj(const double dun[], int too);
char unelgee_oloh(double dundaj);
```

Функц бүр **нэг** ажил хийнэ. Ингэснээр тус бүрийг тусад нь шалгаж
болно.

### Эрэмбэлэх

```c
#include <stdlib.h>

int hartsuulah(const void *a, const void *b) {
    const Oyutan *x = a;
    const Oyutan *y = b;

    if (x->dundaj < y->dundaj) return 1;    /* буурахаар */
    if (x->dundaj > y->dundaj) return -1;
    return 0;
}

qsort(angi, too, sizeof(Oyutan), hartsuulah);
```

`qsort` нь `void *` авдаг тул өөрийн төрөл рүү хөрвүүлнэ.

### Нэмэлт сорилт

1. Хичээл тус бүрийн дундажийг гаргаарай.
2. Дүнг файлаас уншдаг болгоорой (`fopen`, `fscanf`).
3. Босгоос доош дүнтэй оюутныг тусад нь жагсаагаарай.

### Жишээ програм

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define HICHEEL 3
#define OYUTAN 4

typedef struct {
    char ner[50];
    double dun[HICHEEL];
    double dundaj;
    char unelgee;
} Oyutan;

double dundaj_bodoh(const double dun[], int too);
char unelgee_oloh(double dundaj);
void dundaj_shinechleh(Oyutan *o);
int hartsuulah(const void *a, const void *b);
void husnegt_hevleh(const Oyutan angi[], int too);

int main(void) {
    Oyutan angi[OYUTAN] = {
        {"Бат",   {85, 92, 78}, 0, ' '},
        {"Сараа", {70, 65, 80}, 0, ' '},
        {"Дорж",  {95, 89, 91}, 0, ' '},
        {"Оюун",  {55, 62, 48}, 0, ' '}
    };

    for (int i = 0; i < OYUTAN; i++) {
        dundaj_shinechleh(&angi[i]);
    }

    printf("=== Анхны жагсаалт ===\\n");
    husnegt_hevleh(angi, OYUTAN);

    /* Дунджаар буурахаар эрэмбэлнэ */
    qsort(angi, OYUTAN, sizeof(Oyutan), hartsuulah);

    printf("\\n=== Дунджаар эрэмбэлсэн ===\\n");
    husnegt_hevleh(angi, OYUTAN);

    /* Ангийн статистик */
    double niit = 0.0;
    int tentssen = 0;

    for (int i = 0; i < OYUTAN; i++) {
        niit += angi[i].dundaj;
        if (angi[i].dundaj >= 60.0) {
            tentssen++;
        }
    }

    printf("\\nАнгийн дундаж: %.2f\\n", niit / OYUTAN);
    printf("Тэнцсэн: %d / %d\\n", tentssen, OYUTAN);
    printf("Тэргүүлэгч: %s (%.2f)\\n", angi[0].ner, angi[0].dundaj);

    return 0;
}

double dundaj_bodoh(const double dun[], int too) {
    if (too <= 0) {
        return 0.0;
    }

    double niilber = 0.0;
    for (int i = 0; i < too; i++) {
        niilber += dun[i];
    }
    return niilber / too;
}

char unelgee_oloh(double dundaj) {
    if (dundaj >= 90.0) return 'A';
    if (dundaj >= 80.0) return 'B';
    if (dundaj >= 70.0) return 'C';
    if (dundaj >= 60.0) return 'D';
    return 'F';
}

/* Дундаж ба үнэлгээг НЭГ газраас шинэчилнэ */
void dundaj_shinechleh(Oyutan *o) {
    o->dundaj = dundaj_bodoh(o->dun, HICHEEL);
    o->unelgee = unelgee_oloh(o->dundaj);
}

int hartsuulah(const void *a, const void *b) {
    const Oyutan *x = a;
    const Oyutan *y = b;

    if (x->dundaj < y->dundaj) return 1;
    if (x->dundaj > y->dundaj) return -1;
    return 0;
}

void husnegt_hevleh(const Oyutan angi[], int too) {
    printf("%-8s", "Нэр");
    for (int h = 0; h < HICHEEL; h++) {
        printf("%7d", h + 1);
    }
    printf("%9s%4s\\n", "Дундаж", "Үнэ");

    for (int i = 0; i < too; i++) {
        printf("%-8s", angi[i].ner);
        for (int h = 0; h < HICHEEL; h++) {
            printf("%7.0f", angi[i].dun[h]);
        }
        printf("%9.2f%4c\\n", angi[i].dundaj, angi[i].unelgee);
    }
}
```
""",
            initial_code="""\
#include <stdio.h>

#define HICHEEL 3
#define MAX_OYUTAN 50

typedef struct {
    char ner[50];
    int dun[HICHEEL];
    double dundaj;
} Oyutan;

/* dun массивын дундажийг буцаана. Бүхэл хуваалтаас болгоомжил! */
double dundaj_bodoh(const int dun[], int too) {
    /* TODO */
    return 0.0;
}

/* 90+ A, 80+ B, 70+ C, 60+ D, бусад нь F */
char unelgee_oloh(double dundaj) {
    /* TODO */
    return 'F';
}

int main(void) {
    Oyutan angi[MAX_OYUTAN];
    int n;

    if (scanf("%d", &n) != 1 || n < 0 || n > MAX_OYUTAN) {
        return 1;
    }

    /* TODO: n == 0 бол «Оюутан алга.» гэж хэвлээд дуусга */

    for (int i = 0; i < n; i++) {
        /* TODO: нэр ба гурван дүнг angi[i]-д уншиж, дундажийг бод */
    }

    /* TODO: оюутан бүрийн мөр, дараа нь ангийн дундаж, тэнцсэн тоо,
       тэргүүлэгчийг хэвлэ */

    return 0;
}
""",
            exercise=ExerciseSpec(
                statement="""\
Ангийн дүнгийн тайлан гаргадаг програм бич. Оюутан бүр гурван хичээлийн
дүнтэй.

**Оролт:** эхний мөрөнд оюутны тоо `N` (0 ≤ N ≤ 50). Дараагийн `N` мөр
бүрт `<нэр> <д1> <д2> <д3>` — нэр нь зайгүй нэг үг, дүн нь 0–100 хоорондох
бүхэл тоо.

**Гаралт:** `N = 0` бол зөвхөн `Оюутан алга.` Эс бөгөөс:

1. Оюутан бүрт оролтын дарааллаар `<нэр>: <дундаж> <үнэлгээ>`, жишээ нь
   `Бат: 85.00 B`.
2. `Ангийн дундаж: <X>` — оюутнуудын дунджийн дундаж.
3. `Тэнцсэн: <K> / <N>` — дундаж нь 60 ба түүнээс дээш оюутны тоо.
4. `Тэргүүлэгч: <нэр> (<дундаж>)` — хамгийн өндөр дундажтай оюутан. Хэд
   хэдэн оюутан тэнцвэл оролтод хамгийн түрүүнд орсон нь.

Бүх бутархай тоог `%.2f` форматаар хэвлэнэ. Үнэлгээ: дундаж 90 ба түүнээс
дээш бол `A`, 80+ `B`, 70+ `C`, 60+ `D`, бусад нь `F`.

«Оюутны тоо:» гэх мэт асуулт **бүү хэвлэ** — шалгагч зөвхөн гаралтыг
харьцуулна.
""",
                tests=(
                    TestCaseSpec(
                        stdin="3\nБат 85 92 78\nСараа 70 65 80\nОюун 55 62 48\n",
                        expected_output=(
                            "Бат: 85.00 B\n"
                            "Сараа: 71.67 C\n"
                            "Оюун: 55.00 F\n"
                            "Ангийн дундаж: 70.56\n"
                            "Тэнцсэн: 2 / 3\n"
                            "Тэргүүлэгч: Бат (85.00)\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="0\n",
                        expected_output="Оюутан алга.\n",
                    ),
                    TestCaseSpec(
                        stdin="4\nАнар 90 90 90\nБолд 90 89 90\nДулмаа 60 60 60\nЭнх 60 59 60\n",
                        expected_output=(
                            "Анар: 90.00 A\n"
                            "Болд: 89.67 B\n"
                            "Дулмаа: 60.00 D\n"
                            "Энх: 59.67 F\n"
                            "Ангийн дундаж: 74.83\n"
                            "Тэнцсэн: 3 / 4\n"
                            "Тэргүүлэгч: Анар (90.00)\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="3\nТөмөр 80 80 80\nЗаяа 70 90 80\nНомин 100 100 40\n",
                        expected_output=(
                            "Төмөр: 80.00 B\n"
                            "Заяа: 80.00 B\n"
                            "Номин: 80.00 B\n"
                            "Ангийн дундаж: 80.00\n"
                            "Тэнцсэн: 3 / 3\n"
                            "Тэргүүлэгч: Төмөр (80.00)\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="1\nBold 0 0 0\n",
                        expected_output=(
                            "Bold: 0.00 F\n"
                            "Ангийн дундаж: 0.00\n"
                            "Тэнцсэн: 0 / 1\n"
                            "Тэргүүлэгч: Bold (0.00)\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="2\nАну 59 60 61\nЭнхээ 100 99 98\n",
                        expected_output=(
                            "Ану: 60.00 D\n"
                            "Энхээ: 99.00 A\n"
                            "Ангийн дундаж: 79.50\n"
                            "Тэнцсэн: 2 / 2\n"
                            "Тэргүүлэгч: Энхээ (99.00)\n"
                        ),
                    ),
                ),
                solution="""\
#include <stdio.h>

#define HICHEEL 3
#define MAX_OYUTAN 50

/* Нэг оюутны өгөгдөл: нэр, гурван дүн, бодсон дундаж */
typedef struct {
    char ner[50];
    int dun[HICHEEL];
    double dundaj;
} Oyutan;

/* Бүхэл нийлбэрийг double болгож хуваана — бүхэл хуваалт бутархайг хаяна */
double dundaj_bodoh(const int dun[], int too) {
    int niilber = 0;
    for (int i = 0; i < too; i++) {
        niilber += dun[i];
    }
    return (double) niilber / too;
}

/* Дээрээс доош шалгана: эхний таарсан босго үнэлгээг өгнө */
char unelgee_oloh(double dundaj) {
    if (dundaj >= 90.0) return 'A';
    if (dundaj >= 80.0) return 'B';
    if (dundaj >= 70.0) return 'C';
    if (dundaj >= 60.0) return 'D';
    return 'F';
}

int main(void) {
    Oyutan angi[MAX_OYUTAN];
    int n;

    if (scanf("%d", &n) != 1 || n < 0 || n > MAX_OYUTAN) {
        return 1;
    }

    /* Хоосон анги — өөр юу ч хэвлэхгүй (доор n-д хуваахаас сэргийлнэ) */
    if (n == 0) {
        printf("Оюутан алга.\\n");
        return 0;
    }

    /* 1-р шат: бүх оюутныг уншиж, дунджийг нь бодно */
    for (int i = 0; i < n; i++) {
        Oyutan *o = &angi[i];
        /* %49s — ner[50]-ээс хэтрэхгүй */
        if (scanf("%49s %d %d %d", o->ner, &o->dun[0], &o->dun[1], &o->dun[2]) != 4) {
            return 1;
        }
        o->dundaj = dundaj_bodoh(o->dun, HICHEEL);
    }

    double niit = 0.0;   /* дунджуудын нийлбэр */
    int tentssen = 0;    /* дундаж >= 60 оюутны тоо */
    int terguulegch = 0; /* тэргүүлэгчийн индекс */

    /* 2-р шат: мөр бүрийг хэвлэхийн зэрэгцээ статистик цуглуулна */
    for (int i = 0; i < n; i++) {
        printf("%s: %.2f %c\\n", angi[i].ner, angi[i].dundaj, unelgee_oloh(angi[i].dundaj));

        niit += angi[i].dundaj;
        if (angi[i].dundaj >= 60.0) {
            tentssen++;
        }
        /* Хатуу «>» — тэнцвэл түрүүлж орсон нь үлдэнэ */
        if (angi[i].dundaj > angi[terguulegch].dundaj) {
            terguulegch = i;
        }
    }

    /* Нэгтгэл */
    printf("Ангийн дундаж: %.2f\\n", niit / n);
    printf("Тэнцсэн: %d / %d\\n", tentssen, n);
    printf("Тэргүүлэгч: %s (%.2f)\\n", angi[terguulegch].ner, angi[terguulegch].dundaj);
    return 0;
}
""",
                tips="""\
- Оюутан бүрийг `struct`-д (нэр, `dun[3]`, `dundaj`) хадгалж, `Oyutan angi[50]`
  массивт унш. Нэрийг `%49s`-ээр уншвал `ner[50]`-ээс хэтрэхгүй.
- `N = 0`-ийг хамгийн түрүүнд шалга: `Оюутан алга.` хэвлээд шууд дуусга —
  ангийн дундажийг `N`-д хуваах гэж оролдохоос сэргийлнэ.
- Дундажийг `(double) niilber / 3` гэж бод. `niilber / 3` гэвэл бүхэл хуваалт
  болж бутархай хэсэг алга болно.
- Үнэлгээг дээрээс доош `>=`-ээр шалга (90 → 80 → 70 → 60). Яг босго дээрх
  дундаж дээд үнэлгээ авна, босгоос арай доогуур нь (жишээ нь `89.67`) авахгүй.
- Тэргүүлэгчийн **индексийг** хадгалж, **хатуу** `>`-ээр харьцуул — хэд хэдэн
  оюутан тэнцвэл түрүүлж орсон нь үлдэнэ. Нэг оюутантай анги ч зөв ажиллах
  ёстой.
""",
            ),
        ),
        LessonSpec(
            title="Төсөл — Холбоо барих програм",
            slug="c-holbogdoh-programm",
            description="Бүтцийн массив, хайх, нэмэх, устгах.",
            duration=720,
            language=C,
            content="""\
Утасны дэвтэр. Нэмэх, хайх, устгах, жагсаах.

### Бүтэц

```c
typedef struct {
    char ner[50];
    char utas[20];
} Holboo;

typedef struct {
    Holboo jagsaalt[MAX];
    int too;
} Devter;
```

Массив ба түүний уртыг **нэг бүтцэд** оруулсныг анхаар. Ингэснээр хоёр
параметр дамжуулах шаардлагагүй бөгөөд хоёулаа үргэлж зэрэгцэнэ.

### Устгах арга

Дундаас нь устгахад хоёр сонголт:

**1. Үлдсэнийг зөөх** — дараалал хадгалагдана, удаан:

```c
for (int i = baiirlal; i < d->too - 1; i++) {
    d->jagsaalt[i] = d->jagsaalt[i + 1];
}
d->too--;
```

**2. Сүүлчийнхийг нүхэнд нь тавих** — хурдан, дараалал алдагдана:

```c
d->jagsaalt[baiirlal] = d->jagsaalt[d->too - 1];
d->too--;
```

Дараалал чухал бол эхнийхийг сонго.

### Дүүрсэн эсэхийг шалга

```c
if (d->too >= MAX) {
    return 0;
}
```

Шалгахгүй бол массиваас гадуур бичиж, санах ойг эвдэнэ. C нь таныг
зогсоохгүй.

### Хайлт

Том жижиг үсэг ялгахгүй хайлт нь илүү тав тухтай. `strcasecmp` нь
стандарт биш тул гараар бичих, эсвэл `tolower`-оор тэгшитгэх хэрэгтэй.

### Нэмэлт сорилт

1. Хайлтыг том жижиг үсэг ялгахгүй болгоорой.
2. Нэрээр эрэмбэлж хэвлээрэй.
3. Файлд хадгалж, эхлэхэд уншдаг болгоорой.

### Жишээ програм

```c
#include <stdio.h>
#include <string.h>

#define MAX_HOLBOO 50

typedef struct {
    char ner[50];
    char utas[20];
} Holboo;

typedef struct {
    Holboo jagsaalt[MAX_HOLBOO];
    int too;
} Devter;

int nemeh(Devter *d, const char *ner, const char *utas);
int oloh(const Devter *d, const char *ner);
int ustgah(Devter *d, const char *ner);
void jagsaah(const Devter *d);

int main(void) {
    Devter devter = {.too = 0};

    nemeh(&devter, "Бат", "9911-2233");
    nemeh(&devter, "Сараа", "8844-5566");
    nemeh(&devter, "Дорж", "9977-8899");
    nemeh(&devter, "Оюун", "9955-4433");

    jagsaah(&devter);

    /* Хайх */
    const char *haih = "Дорж";
    int baiirlal = oloh(&devter, haih);

    printf("\\n--- Хайлт ---\\n");
    if (baiirlal >= 0) {
        printf("%s: %s\\n", devter.jagsaalt[baiirlal].ner,
               devter.jagsaalt[baiirlal].utas);
    } else {
        printf("«%s» олдсонгүй\\n", haih);
    }

    /* Устгах */
    printf("\\n--- Сарааг устгав ---\\n");
    if (ustgah(&devter, "Сараа")) {
        jagsaah(&devter);
    }

    /* Байхгүйг устгах */
    if (!ustgah(&devter, "Болд")) {
        printf("\\n«Болд» байхгүй тул устгасангүй\\n");
    }

    return 0;
}

int nemeh(Devter *d, const char *ner, const char *utas) {
    if (d->too >= MAX_HOLBOO) {
        return 0;   /* дүүрсэн */
    }

    /* snprintf нь хэмжээг хүндэтгэж, тэглэх тэмдэгтийг өөрөө тавина */
    snprintf(d->jagsaalt[d->too].ner, sizeof(d->jagsaalt[d->too].ner), "%s", ner);
    snprintf(d->jagsaalt[d->too].utas, sizeof(d->jagsaalt[d->too].utas), "%s", utas);
    d->too++;

    return 1;
}

int oloh(const Devter *d, const char *ner) {
    for (int i = 0; i < d->too; i++) {
        if (strcmp(d->jagsaalt[i].ner, ner) == 0) {
            return i;
        }
    }
    return -1;
}

int ustgah(Devter *d, const char *ner) {
    int baiirlal = oloh(d, ner);
    if (baiirlal < 0) {
        return 0;
    }

    /* Үлдсэнийг зөөнө — дараалал хадгалагдана */
    for (int i = baiirlal; i < d->too - 1; i++) {
        d->jagsaalt[i] = d->jagsaalt[i + 1];
    }
    d->too--;

    return 1;
}

void jagsaah(const Devter *d) {
    printf("\\n=== Утасны дэвтэр (%d) ===\\n", d->too);
    for (int i = 0; i < d->too; i++) {
        printf("%2d. %-8s %s\\n", i + 1, d->jagsaalt[i].ner, d->jagsaalt[i].utas);
    }
}
```
""",
            initial_code="""\
#include <stdio.h>
#include <string.h>

#define MAX_HOLBOO 5

typedef struct {
    char ner[50];
    char utas[20];
} Holboo;

typedef struct {
    Holboo jagsaalt[MAX_HOLBOO];
    int too;
} Devter;

/* Нэрээр хайж байрлалыг буцаана, олдохгүй бол -1 */
int oloh(const Devter *d, const char *ner) {
    /* TODO */
    return -1;
}

int main(void) {
    Devter devter = {.too = 0};
    char tushaal[20];
    char ner[50];
    char utas[20];

    while (scanf("%19s", tushaal) == 1) {
        if (strcmp(tushaal, "QUIT") == 0) {
            break;
        } else if (strcmp(tushaal, "ADD") == 0) {
            if (scanf("%49s %19s", ner, utas) != 2) {
                break;
            }
            /* TODO: давхардал, дараа нь дүүрсэн эсэхийг шалгаад devter-т нэм */
        } else if (strcmp(tushaal, "FIND") == 0) {
            if (scanf("%49s", ner) != 1) {
                break;
            }
            /* TODO */
        } else if (strcmp(tushaal, "DEL") == 0) {
            if (scanf("%49s", ner) != 1) {
                break;
            }
            /* TODO: устгаад араас нь байгааг нэг байр урагш зөө */
        } else if (strcmp(tushaal, "LIST") == 0) {
            /* TODO */
        } else {
            printf("Танихгүй тушаал: %s\\n", tushaal);
        }
    }

    return 0;
}
""",
            exercise=ExerciseSpec(
                statement="""\
Утасны дэвтрийг тушаалаар удирддаг програм бич. Дэвтэрт хамгийн ихдээ
**5** харилцагч багтана.

**Оролт:** мөр бүрт нэг тушаал. Нэр ба утас нь зайгүй нэг үг.

- `ADD <нэр> <утас>` — харилцагч нэмнэ.
- `FIND <нэр>` — утсыг нь хайна.
- `DEL <нэр>` — харилцагчийг устгана.
- `LIST` — бүх харилцагчийг жагсаана.
- `QUIT` — програмыг дуусгана. Оролт дуусахад ч мөн адил.

**Гаралт:**

- `ADD`: нэр аль хэдийн байвал `<нэр> аль хэдийн байна.`, дэвтэр дүүрсэн
  бол `Дэвтэр дүүрсэн.`, эс бөгөөс `<нэр> нэмэгдлээ.` Давхардлыг дүүрсэн
  эсэхээс **өмнө** шалгана.
- `FIND`: `<нэр>: <утас>` эсвэл `<нэр> олдсонгүй.`
- `DEL`: `<нэр> устгагдлаа.` эсвэл `<нэр> олдсонгүй.`
- `LIST`: хоосон бол `Дэвтэр хоосон.`, эс бөгөөс харилцагч бүрт
  `<i>. <нэр>: <утас>` (`i` нь 1-ээс эхэлнэ). Харилцагчид **нэмсэн
  дарааллаараа** байна — устгахад үлдсэнийх нь дараалал өөрчлөгдөхгүй.
- Танихгүй тушаал (мөрөнд ганцаараа ирнэ): `Танихгүй тушаал: <тушаал>`.

Цэс, асуулт **бүү хэвлэ** — шалгагч зөвхөн гаралтыг харьцуулна.
""",
                tests=(
                    TestCaseSpec(
                        stdin=(
                            "ADD Бат 9911-2233\n"
                            "ADD Сараа 8844-5566\n"
                            "ADD Дорж 9977-8899\n"
                            "FIND Сараа\n"
                            "DEL Сараа\n"
                            "LIST\n"
                            "QUIT\n"
                        ),
                        expected_output=(
                            "Бат нэмэгдлээ.\n"
                            "Сараа нэмэгдлээ.\n"
                            "Дорж нэмэгдлээ.\n"
                            "Сараа: 8844-5566\n"
                            "Сараа устгагдлаа.\n"
                            "1. Бат: 9911-2233\n"
                            "2. Дорж: 9977-8899\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="LIST\nFIND Бат\nDEL Бат\nQUIT\n",
                        expected_output="Дэвтэр хоосон.\nБат олдсонгүй.\nБат олдсонгүй.\n",
                    ),
                    TestCaseSpec(
                        stdin=(
                            "ADD Анар 9900-0001\n"
                            "ADD Болд 9900-0002\n"
                            "ADD Ганаа 9900-0003\n"
                            "ADD Анар 9900-0004\n"
                            "ADD Дулмаа 9900-0005\n"
                            "ADD Энхээ 9900-0006\n"
                            "ADD Жаргал 9900-0007\n"
                            "ADD Болд 9900-0008\n"
                            "LIST\n"
                            "QUIT\n"
                        ),
                        expected_output=(
                            "Анар нэмэгдлээ.\n"
                            "Болд нэмэгдлээ.\n"
                            "Ганаа нэмэгдлээ.\n"
                            "Анар аль хэдийн байна.\n"
                            "Дулмаа нэмэгдлээ.\n"
                            "Энхээ нэмэгдлээ.\n"
                            "Дэвтэр дүүрсэн.\n"
                            "Болд аль хэдийн байна.\n"
                            "1. Анар: 9900-0001\n"
                            "2. Болд: 9900-0002\n"
                            "3. Ганаа: 9900-0003\n"
                            "4. Дулмаа: 9900-0005\n"
                            "5. Энхээ: 9900-0006\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin=(
                            "ADD Бат 9911-2233\n"
                            "ADD Сараа 8844-5566\n"
                            "ADD Дорж 9977-8899\n"
                            "DEL Бат\n"
                            "ADD Оюун 9955-4433\n"
                            "LIST\n"
                            "FIND Бат\n"
                            "QUIT\n"
                        ),
                        expected_output=(
                            "Бат нэмэгдлээ.\n"
                            "Сараа нэмэгдлээ.\n"
                            "Дорж нэмэгдлээ.\n"
                            "Бат устгагдлаа.\n"
                            "Оюун нэмэгдлээ.\n"
                            "1. Сараа: 8844-5566\n"
                            "2. Дорж: 9977-8899\n"
                            "3. Оюун: 9955-4433\n"
                            "Бат олдсонгүй.\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="ADD Болд 8800-1122\nEDIT\nLIST\nQUIT\nLIST\n",
                        expected_output=(
                            "Болд нэмэгдлээ.\nТанихгүй тушаал: EDIT\n1. Болд: 8800-1122\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="ADD Анар 9900-0000\nFIND Анар\nDEL Анар\nLIST\n",
                        expected_output=(
                            "Анар нэмэгдлээ.\nАнар: 9900-0000\nАнар устгагдлаа.\nДэвтэр хоосон.\n"
                        ),
                    ),
                ),
                solution="""\
#include <stdio.h>
#include <string.h>

#define MAX_HOLBOO 5

/* Нэг харилцагч */
typedef struct {
    char ner[50];
    char utas[20];
} Holboo;

/* Дэвтэр: тогтмол хэмжээтэй массив + одоо хэдэн харилцагч байгаа */
typedef struct {
    Holboo jagsaalt[MAX_HOLBOO];
    int too;
} Devter;

/* Нэрээр хайна: олдвол индекс, эс бөгөөс -1. ADD, FIND, DEL бүгд ашиглана */
int oloh(const Devter *d, const char *ner) {
    for (int i = 0; i < d->too; i++) {
        if (strcmp(d->jagsaalt[i].ner, ner) == 0) {
            return i;
        }
    }
    return -1;
}

/* ADD — давхардлыг дүүрсэн эсэхээс ӨМНӨ шалгана */
void nemeh(Devter *d, const char *ner, const char *utas) {
    if (oloh(d, ner) >= 0) {
        printf("%s аль хэдийн байна.\\n", ner);
        return;
    }
    if (d->too >= MAX_HOLBOO) {
        printf("Дэвтэр дүүрсэн.\\n");
        return;
    }

    /* Шинэ харилцагчийг массивын төгсгөлд нэмнэ */
    strcpy(d->jagsaalt[d->too].ner, ner);
    strcpy(d->jagsaalt[d->too].utas, utas);
    d->too++;
    printf("%s нэмэгдлээ.\\n", ner);
}

/* DEL */
void ustgah(Devter *d, const char *ner) {
    int baiirlal = oloh(d, ner);
    if (baiirlal < 0) {
        printf("%s олдсонгүй.\\n", ner);
        return;
    }

    /* Үлдсэнийг зөөнө — дараалал хадгалагдана */
    for (int i = baiirlal; i < d->too - 1; i++) {
        d->jagsaalt[i] = d->jagsaalt[i + 1];
    }
    d->too--;
    printf("%s устгагдлаа.\\n", ner);
}

/* LIST — дугаар 1-ээс эхэлнэ */
void jagsaah(const Devter *d) {
    if (d->too == 0) {
        printf("Дэвтэр хоосон.\\n");
        return;
    }
    for (int i = 0; i < d->too; i++) {
        printf("%d. %s: %s\\n", i + 1, d->jagsaalt[i].ner, d->jagsaalt[i].utas);
    }
}

int main(void) {
    Devter devter = {.too = 0};
    char tushaal[20];
    char ner[50];
    char utas[20];

    /* Тушаал уншиж чадсаар байх хооронд эргэнэ — оролт дуусвал зогсоно */
    while (scanf("%19s", tushaal) == 1) {
        /* Тэмдэгт мөрийг == биш strcmp-ээр харьцуулна */
        if (strcmp(tushaal, "QUIT") == 0) {
            break;
        } else if (strcmp(tushaal, "ADD") == 0) {
            if (scanf("%49s %19s", ner, utas) != 2) {
                break;
            }
            nemeh(&devter, ner, utas);
        } else if (strcmp(tushaal, "FIND") == 0) {
            if (scanf("%49s", ner) != 1) {
                break;
            }
            int baiirlal = oloh(&devter, ner);
            if (baiirlal >= 0) {
                printf("%s: %s\\n", ner, devter.jagsaalt[baiirlal].utas);
            } else {
                printf("%s олдсонгүй.\\n", ner);
            }
        } else if (strcmp(tushaal, "DEL") == 0) {
            if (scanf("%49s", ner) != 1) {
                break;
            }
            ustgah(&devter, ner);
        } else if (strcmp(tushaal, "LIST") == 0) {
            jagsaah(&devter);
        } else {
            /* Танихгүй тушаал — аргумент уншихгүй */
            printf("Танихгүй тушаал: %s\\n", tushaal);
        }
    }

    return 0;
}
""",
                tips="""\
- Бүтэц: `Holboo` (нэр, утас) ба `Devter` (`Holboo jagsaalt[5]` + `int too`).
  `while (scanf("%19s", tushaal) == 1)` давталтаар тушаал уншиж, `strcmp`-ээр
  салаал — C-д тэмдэгт мөрийг `==`-ээр харьцуулж болохгүй.
- Нэрээр хайдаг `oloh()` функц бич (олдвол индекс, эс бөгөөс `-1`). `ADD`,
  `FIND`, `DEL` гурвуулаа түүнийг ашиглана. Тушаал бүрийг тусдаа функцэд гарга.
- `ADD` дээр давхардлыг дүүрсэн эсэхээс **өмнө** шалга: дэвтэр дүүрсэн үед
  аль хэдийн байгаа нэр ирвэл `Дэвтэр дүүрсэн.` биш `аль хэдийн байна.` гарна.
- `DEL` хийхдээ араас нь байгаа бүх элементийг нэг байр урагш зөөгөөд `too`-г
  хасна. Сүүлийн элементээр нөхөх нь нэмсэн дарааллыг эвддэг. Устгасны дараа
  чөлөөлөгдсөн байранд шинэ харилцагч нэмэгдэх ёстой.
- `QUIT`-ийн дараах мөрүүдийг уншихгүй, `QUIT` ирээгүй ч оролт дуусахад
  програм зөв гарна. Хоосон дэвтрийн `LIST`, байхгүй нэрийн `FIND`/`DEL`-ийг
  мартуузай.
""",
            ),
        ),
    ],
)

CPP_PROJECTS = ModuleSpec(
    title="Модул 21 — C++ төслүүд",
    description="Класс, вектор, std::string ашигласан төслүүд.",
    lessons=[
        LessonSpec(
            title="Төсөл — C++ тооцоолуур",
            slug="cpp-tootsooluur",
            description="Түүх хадгалдаг классан дээр суурилсан тооцоолуур.",
            duration=660,
            language=CPP,
            content="""\
Модул 20-ийн тооцоолуурыг C++ маягаар дахин бичнэ.

### Юу өөрчлөгдөх вэ

| C | C++ |
|---|---|
| `scanf` шалгалт | `std::cin` төлөв шалгах |
| `char massiv[]` | `std::string` |
| Заагчаар амжилт буцаах | Онцгой байдал эсвэл `optional` |
| Глобал массив | Классын гишүүн `std::vector` |

### Класс болгох давуу тал

Түүх, тохиргоо зэрэг төлөвийг классын дотор нууна:

```cpp
class Tootsooluur {
public:
    double bodoh(double a, char uildel, double b);
    void tuuh_hevleh() const;

private:
    std::vector<std::string> tuuh_;
};
```

Глобал хувьсагч ашиглах шаардлагагүй болно.

### Алдааг онцгой байдлаар

Энэ төслийн шинэ хэрэгсэл бол **онцгой байдал** (exception). Функц
ажлаа хийж чадахгүй бол алдааг **шиднэ** (`throw`):

```cpp
#include <stdexcept>

if (b == 0) {
    throw std::invalid_argument("Тэгд хуваах боломжгүй");
}
```

`throw` хийгдмэгц функц тэр дороо зогсоно — доорх мөрүүд ажиллахгүй,
`return` ч хийгдэхгүй. `std::invalid_argument` нь «аргумент буруу» гэсэн
бэлэн алдааны төрөл, хаалтанд алдааны мессежийг өгнө.

Дуудсан тал нь алдааг **барина** (`try` / `catch`):

```cpp
try {
    double ur = t.bodoh(a, uildel, b);
    std::cout << ur << "\\n";            // алдаа гарвал энэ мөр алгасагдана
} catch (const std::invalid_argument &aldaa) {
    std::cout << aldaa.what() << "\\n";  // шидсэн мессеж
}
```

- `try { ... }` блок дотор алдаа шидэгдвэл үлдсэн мөрүүд алгасагдаж, шууд
  `catch` блок руу үсэрнэ. Алдаа гараагүй бол `catch` огт ажиллахгүй.
- `catch (const std::invalid_argument &aldaa)` нь тэр төрлийн алдааг барина,
  `aldaa.what()` нь `throw` хийхдээ өгсөн мессежийг буцаана.
- `std::exception` гэж бичвэл бүх стандарт алдааг нэг дор барина.
- Алдааг хэн ч бариагүй бол програм алдаа заагаад зогсоно.

Заагчаар амжилт буцаахаас илүү тодорхой: амжилтын зам нь цэвэр үлдэнэ.

### Түүхийг мөр болгох

```cpp
std::ostringstream ss;
ss << a << " " << uildel << " " << b << " = " << ur;
tuuh_.push_back(ss.str());
```

`std::ostringstream` (`<sstream>`) нь Модул 16-ийн `std::stringstream`-ийн
зөвхөн **бичдэг** хувилбар: `std::cout` руу бичдэг шигээ бичээд, `ss.str()`-ээр
нэг `std::string` болгож авна. `std::fixed << std::setprecision(2)` ч энд
адилхан ажиллана.

### Нэмэлт сорилт

1. Сүүлийн үр дүнг санаж, `ans` гэж ашиглах боломж нэмээрэй.
2. Түүхийг цэвэрлэх метод нэмээрэй.
3. Зэрэг дэвшүүлэх үйлдэл нэмээрэй.

### Жишээ програм

```cpp
#include <iomanip>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

class Tootsooluur {
public:
    double bodoh(double a, char uildel, double b) {
        double ur = 0.0;

        switch (uildel) {
            case '+': ur = a + b; break;
            case '-': ur = a - b; break;
            case '*': ur = a * b; break;
            case '/':
                if (b == 0) {
                    throw std::invalid_argument("Тэгд хуваах боломжгүй");
                }
                ur = a / b;
                break;
            default:
                throw std::invalid_argument("Танихгүй үйлдэл");
        }

        tuuh_temdegleh(a, uildel, b, ur);
        return ur;
    }

    void tuuh_hevleh() const {
        if (tuuh_.empty()) {
            std::cout << "Түүх хоосон байна.\\n";
            return;
        }

        std::cout << "\\n=== Түүх (" << tuuh_.size() << ") ===\\n";
        for (std::size_t i = 0; i < tuuh_.size(); i++) {
            std::cout << "  " << i + 1 << ". " << tuuh_[i] << "\\n";
        }
    }

    std::size_t tuuhiin_too() const { return tuuh_.size(); }

private:
    void tuuh_temdegleh(double a, char uildel, double b, double ur) {
        std::ostringstream ss;
        ss << std::fixed << std::setprecision(2);
        ss << a << " " << uildel << " " << b << " = " << ur;
        tuuh_.push_back(ss.str());
    }

    std::vector<std::string> tuuh_;
};

int main() {
    Tootsooluur t;

    std::cout << std::fixed << std::setprecision(2);

    // Амжилттай тооцоолол
    struct Bodlogo {
        double a;
        char uildel;
        double b;
    };

    const std::vector<Bodlogo> bodloguud = {
        {12, '+', 8}, {50, '-', 17}, {6, '*', 7}, {10, '/', 4}, {5, '/', 0}
    };

    for (const auto &bodlogo : bodloguud) {
        try {
            double ur = t.bodoh(bodlogo.a, bodlogo.uildel, bodlogo.b);
            std::cout << "OK:    " << bodlogo.a << " " << bodlogo.uildel
                      << " " << bodlogo.b << " = " << ur << "\\n";
        } catch (const std::exception &aldaa) {
            std::cout << "Алдаа: " << aldaa.what() << "\\n";
        }
    }

    t.tuuh_hevleh();

    return 0;
}
```
""",
            initial_code="""\
#include <iomanip>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

class Tootsooluur {
public:
    // Бодоод «a uildel b = ur» мөрийг түүхэнд нэмж, түүнийгээ буцаана.
    // Тэгд хуваах, танихгүй үйлдэл бол std::invalid_argument шиднэ.
    std::string bodoh(double a, char uildel, double b) {
        // TODO: switch, тэгд хуваах шалгалт, std::ostringstream
        return "";
    }

    void tuuh_hevleh() const {
        // TODO: хоосон бол «Түүх хоосон.», эс бөгөөс дугаарласан мөрүүд
    }

    void tseverleh() { tuuh_.clear(); }

private:
    std::vector<std::string> tuuh_;
};

int main() {
    Tootsooluur t;
    std::string tushaal;

    while (std::cin >> tushaal && tushaal != "QUIT") {
        if (tushaal == "CALC") {
            double a;
            double b;
            char uildel;
            if (!(std::cin >> a >> uildel >> b)) {
                break;
            }
            // TODO: t.bodoh-г try/catch дотор дуудаж, хариу эсвэл алдааг хэвлэ
        } else if (tushaal == "HISTORY") {
            t.tuuh_hevleh();
        } else if (tushaal == "CLEAR") {
            // TODO
        } else {
            std::cout << "Танихгүй тушаал: " << tushaal << "\\n";
        }
    }

    return 0;
}
""",
            exercise=ExerciseSpec(
                statement="""\
Түүх хадгалдаг тооцоолуурыг `Tootsooluur` класс ашиглан бич. Тооцоолуур
тушаалаар ажиллана.

**Оролт:** мөр бүрт нэг тушаал:

- `CALC <a> <үйлдэл> <b>` — `a`, `b` нь бодит тоо, үйлдэл нь нэг тэмдэгт.
- `HISTORY` — амжилттай бодсон бүх тооцооллыг харуулна.
- `CLEAR` — түүхийг цэвэрлэнэ.
- `QUIT` — програмыг дуусгана. Оролт дуусахад ч мөн адил.

**Гаралт:**

- `CALC`: `+`, `-`, `*`, `/` бол `<a> <үйлдэл> <b> = <хариу>`, жишээ нь
  `12.00 + 8.00 = 20.00`, мөн энэ мөр түүхэнд нэмэгдэнэ. Тэгд хуваавал
  `Алдаа: тэгд хуваах боломжгүй`, өөр үйлдэл бол `Алдаа: танихгүй үйлдэл`.
  Алдаатай тооцоолол түүхэнд **орохгүй**.
- `HISTORY`: хоосон бол `Түүх хоосон.`, эс бөгөөс тооцоолол бүрт
  `<i>. <тооцоолол>` (`i` нь 1-ээс эхэлнэ).
- `CLEAR`: `Түүх цэвэрлэгдлээ.`
- Танихгүй тушаал (мөрөнд ганцаараа ирнэ): `Танихгүй тушаал: <тушаал>`.

Бүх тоог `std::fixed << std::setprecision(2)` форматаар хэвлэнэ. Цэс,
асуулт **бүү хэвлэ** — шалгагч зөвхөн гаралтыг харьцуулна.
""",
                tests=(
                    TestCaseSpec(
                        stdin="CALC 12 + 8\nCALC 10 / 4\nCALC 5 / 0\nHISTORY\nQUIT\n",
                        expected_output=(
                            "12.00 + 8.00 = 20.00\n"
                            "10.00 / 4.00 = 2.50\n"
                            "Алдаа: тэгд хуваах боломжгүй\n"
                            "1. 12.00 + 8.00 = 20.00\n"
                            "2. 10.00 / 4.00 = 2.50\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="HISTORY\nQUIT\n",
                        expected_output="Түүх хоосон.\n",
                    ),
                    TestCaseSpec(
                        stdin="CALC 2 ^ 3\nCALC 6 * 7\nCLEAR\nHISTORY\nCALC 1 - 3.5\nHISTORY\n",
                        expected_output=(
                            "Алдаа: танихгүй үйлдэл\n"
                            "6.00 * 7.00 = 42.00\n"
                            "Түүх цэвэрлэгдлээ.\n"
                            "Түүх хоосон.\n"
                            "1.00 - 3.50 = -2.50\n"
                            "1. 1.00 - 3.50 = -2.50\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="CALC -1.5 * 4\nPRINT\nQUIT\nHISTORY\n",
                        expected_output="-1.50 * 4.00 = -6.00\nТанихгүй тушаал: PRINT\n",
                    ),
                    TestCaseSpec(
                        stdin="CALC 1 / 3\nCALC 2 / 3\nCALC 0 / 0\nCALC 100 - 0.25\nHISTORY\nQUIT\n",
                        expected_output=(
                            "1.00 / 3.00 = 0.33\n"
                            "2.00 / 3.00 = 0.67\n"
                            "Алдаа: тэгд хуваах боломжгүй\n"
                            "100.00 - 0.25 = 99.75\n"
                            "1. 1.00 / 3.00 = 0.33\n"
                            "2. 2.00 / 3.00 = 0.67\n"
                            "3. 100.00 - 0.25 = 99.75\n"
                        ),
                    ),
                ),
                solution="""\
#include <iomanip>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

class Tootsooluur {
public:
    // Бодоод бэлэн мөрийг түүхэнд нэмж буцаана; алдаа бол exception шиднэ
    std::string bodoh(double a, char uildel, double b) {
        double ur = 0.0;

        switch (uildel) {
            case '+': ur = a + b; break;
            case '-': ur = a - b; break;
            case '*': ur = a * b; break;
            case '/':
                // Хуваахаас ӨМНӨ тэгийг шалгана
                if (b == 0) {
                    throw std::invalid_argument("тэгд хуваах боломжгүй");
                }
                ur = a / b;
                break;
            default:
                throw std::invalid_argument("танихгүй үйлдэл");
        }

        // Энд хүрсэн бол амжилттай: мөрийг нэг удаа бүрдүүлж түүхэнд хадгална.
        // throw нь push_back-аас өмнө тул алдаатай тооцоолол түүхэнд орохгүй.
        std::ostringstream ss;
        ss << std::fixed << std::setprecision(2);
        ss << a << " " << uildel << " " << b << " = " << ur;
        tuuh_.push_back(ss.str());
        return tuuh_.back();
    }

    // HISTORY — дугаар 1-ээс эхэлнэ
    void tuuh_hevleh() const {
        if (tuuh_.empty()) {
            std::cout << "Түүх хоосон.\\n";
            return;
        }
        for (std::size_t i = 0; i < tuuh_.size(); i++) {
            std::cout << i + 1 << ". " << tuuh_[i] << "\\n";
        }
    }

    // CLEAR
    void tseverleh() { tuuh_.clear(); }

private:
    std::vector<std::string> tuuh_; // амжилттай тооцооллын мөрүүд
};

int main() {
    Tootsooluur t;
    std::string tushaal;

    // Оролт дуусах эсвэл QUIT ирэх хүртэл тушаал уншина
    while (std::cin >> tushaal && tushaal != "QUIT") {
        if (tushaal == "CALC") {
            double a;
            double b;
            char uildel;
            if (!(std::cin >> a >> uildel >> b)) {
                break;
            }
            // Алдааг класс шиднэ, main барьж хэвлэнэ
            try {
                std::cout << t.bodoh(a, uildel, b) << "\\n";
            } catch (const std::invalid_argument &aldaa) {
                std::cout << "Алдаа: " << aldaa.what() << "\\n";
            }
        } else if (tushaal == "HISTORY") {
            t.tuuh_hevleh();
        } else if (tushaal == "CLEAR") {
            t.tseverleh();
            std::cout << "Түүх цэвэрлэгдлээ.\\n";
        } else {
            std::cout << "Танихгүй тушаал: " << tushaal << "\\n";
        }
    }

    return 0;
}
""",
                tips="""\
- `Tootsooluur` классын дотор `std::vector<std::string> tuuh_` хадгалж,
  `bodoh`, `tuuh_hevleh`, `tseverleh` гишүүн функцүүд бич. `main` нь
  `while (std::cin >> tushaal && tushaal != "QUIT")` давталтаар тушаал уншина.
- Алдаа гарвал `bodoh` дотор `throw std::invalid_argument("...")` шидэж, `main`
  дотор `try/catch`-аар барьж `aldaa.what()`-ийг хэвлэ. `throw` нь
  `push_back`-аас **өмнө** байвал алдаатай тооцоолол түүхэнд орохгүй.
- Мөрийг `std::ostringstream` дээр `std::fixed << std::setprecision(2)`-оор
  нэг удаа бүрдүүл — дэлгэц болон түүхэнд яг ижил мөр очно.
- `/`-д хуваахаас өмнө `b == 0`-г шалга (хуваагдагч нь 0 байсан ч). Танихгүй
  үйлдлийн мессежид тэмдэгт **ордоггүй** — C хувилбараас ялгаатай.
- `CLEAR`-ийн дараа дугаарлалт дахин 1-ээс эхэлнэ. `QUIT`-ийн дараах
  тушаалуудыг гүйцэтгэхгүй. Сөрөг, бутархай тоо ч зөв уншигдах ёстой.
""",
            ),
        ),
        LessonSpec(
            title="Төсөл — Оюутны удирдлага",
            slug="cpp-oyutan-udirdlaga",
            description="Класс, вектор, эрэмбэлэлт, хайлт.",
            duration=720,
            language=CPP,
            content="""\
Оюутны бүртгэлийг удирдах програм.

### Хоёр класс

```cpp
class Oyutan { … };        // нэг оюутан
class Angi { … };          // оюутнуудын цуглуулга
```

Нэг класс нэг зүйлийг хариуцна. `Oyutan` нь өөрийн дүнг мэднэ,
`Angi` нь бүлгийг удирдана.

### `Oyutan`

```cpp
class Oyutan {
public:
    Oyutan(std::string ner, std::vector<double> dun);

    const std::string &ner() const;
    double dundaj() const;
    char unelgee() const;

private:
    std::string ner_;
    std::vector<double> dun_;
};
```

`dundaj()` нь **тооцоолно**, хадгалахгүй. Ингэснээр дүн өөрчлөгдөхөд
хуучирсан утга үлдэх боломжгүй.

### `Angi`

```cpp
class Angi {
public:
    void nemeh(const Oyutan &o);
    const Oyutan *oloh(const std::string &ner) const;
    double angiin_dundaj() const;
    void erembeleh();

private:
    std::vector<Oyutan> oyutnuud_;
};
```

### Эрэмбэлэх

```cpp
#include <algorithm>

std::sort(oyutnuud_.begin(), oyutnuud_.end(),
          [](const Oyutan &a, const Oyutan &b) {
              return a.dundaj() > b.dundaj();
          });
```

Дөрвөлжин хаалтаар эхэлсэн хэсгийг **лямбда** гэнэ — нэр өгөхгүйгээр
тэр дор нь бичсэн функц. `[]`-ийн дараа энгийн функц шиг параметр, дараа нь
`{ }` дотор бие бичнэ. C-ийн `qsort`-ийн харьцуулах функцээс хамаагүй товч
бөгөөд `void *` хөрвүүлэлт шаардахгүй.

`std::sort` (Модул 19) нь гуравдахь аргументаа хоёр элементийг харьцуулахад
дуудна: `a` нь `b`-гээс **өмнө** байх ёстой бол `true` буцаана. Энд `>`
ашигласан тул дундаж нь их оюутан эхэнд — буурах дараалал. Гуравдахь
аргументгүй бол `std::sort` `<`-ээр өсөхөөр эрэмбэлдэг.

### Олдохгүй тохиолдол

```cpp
const Oyutan *oloh(const std::string &ner) const;
```

Олдохгүй бол `nullptr`. C++17-д `std::optional` илүү тод хувилбар.

### Нэмэлт сорилт

1. Оюутан устгах метод нэмээрэй.
2. Дүнгээр шүүх метод нэмээрэй (босгоос дээш).
3. Нэрээр эрэмбэлэх сонголт нэмээрэй.

### Жишээ програм

```cpp
#include <algorithm>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <string>
#include <vector>

class Oyutan {
public:
    Oyutan(std::string ner, std::vector<double> dun)
        : ner_(ner), dun_(dun) {
    }

    const std::string &ner() const { return ner_; }

    // Хадгалахгүй ТООЦООЛНО — хуучирсан утга үлдэх боломжгүй
    double dundaj() const {
        if (dun_.empty()) {
            return 0.0;
        }
        return std::accumulate(dun_.begin(), dun_.end(), 0.0) / dun_.size();
    }

    char unelgee() const {
        const double d = dundaj();
        if (d >= 90.0) return 'A';
        if (d >= 80.0) return 'B';
        if (d >= 70.0) return 'C';
        if (d >= 60.0) return 'D';
        return 'F';
    }

    bool tentssen() const { return dundaj() >= 60.0; }

private:
    std::string ner_;
    std::vector<double> dun_;
};

class Angi {
public:
    void nemeh(const Oyutan &o) { oyutnuud_.push_back(o); }

    const Oyutan *oloh(const std::string &ner) const {
        for (const auto &o : oyutnuud_) {
            if (o.ner() == ner) {
                return &o;
            }
        }
        return nullptr;
    }

    double angiin_dundaj() const {
        if (oyutnuud_.empty()) {
            return 0.0;
        }

        double niit = 0.0;
        for (const auto &o : oyutnuud_) {
            niit += o.dundaj();
        }
        return niit / oyutnuud_.size();
    }

    // Лямбда — нэр өгөхгүйгээр тэр дор нь бичсэн функц
    void dundajaar_erembeleh() {
        std::sort(oyutnuud_.begin(), oyutnuud_.end(),
                  [](const Oyutan &a, const Oyutan &b) {
                      return a.dundaj() > b.dundaj();
                  });
    }

    void hevleh() const {
        std::cout << std::left << std::setw(10) << "Нэр"
                  << std::right << std::setw(9) << "Дундаж"
                  << std::setw(5) << "Үнэ" << "\\n";

        for (const auto &o : oyutnuud_) {
            std::cout << std::left << std::setw(10) << o.ner()
                      << std::right << std::setw(9) << std::fixed
                      << std::setprecision(2) << o.dundaj()
                      << std::setw(5) << o.unelgee() << "\\n";
        }
    }

    std::size_t hemjee() const { return oyutnuud_.size(); }

private:
    std::vector<Oyutan> oyutnuud_;
};

int main() {
    Angi angi;

    angi.nemeh(Oyutan("Бат", {85, 92, 78}));
    angi.nemeh(Oyutan("Сараа", {70, 65, 80}));
    angi.nemeh(Oyutan("Дорж", {95, 89, 91}));
    angi.nemeh(Oyutan("Оюун", {55, 62, 48}));

    std::cout << "=== Анхны жагсаалт ===\\n";
    angi.hevleh();

    angi.dundajaar_erembeleh();
    std::cout << "\\n=== Дунджаар эрэмбэлсэн ===\\n";
    angi.hevleh();

    std::cout << "\\nАнгийн дундаж: " << std::fixed << std::setprecision(2)
              << angi.angiin_dundaj() << "\\n";

    // Хайх — олдохгүй бол nullptr
    const Oyutan *oldson = angi.oloh("Дорж");
    if (oldson != nullptr) {
        std::cout << "Дорж: " << oldson->dundaj() << " (" << oldson->unelgee() << ")\\n";
    }

    if (angi.oloh("Болд") == nullptr) {
        std::cout << "«Болд» олдсонгүй\\n";
    }

    return 0;
}
```
""",
            initial_code="""\
#include <algorithm>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

class Oyutan {
public:
    Oyutan(std::string ner, std::vector<int> dun)
        : ner_(ner), dun_(dun) {
    }

    const std::string &ner() const { return ner_; }

    // Хадгалахгүй ТООЦООЛНО. Бүхэл хуваалтаас болгоомжил!
    double dundaj() const {
        // TODO
        return 0.0;
    }

    // 90+ A, 80+ B, 70+ C, 60+ D, бусад нь F
    char unelgee() const {
        // TODO
        return 'F';
    }

private:
    std::string ner_;
    std::vector<int> dun_;
};

class Angi {
public:
    // Нэр давхардвал нэмэхгүйгээр false буцаана
    bool nemeh(const Oyutan &o) {
        // TODO: эхлээд oloh-оор шалга
        oyutnuud_.push_back(o);
        return true;
    }

    // Олдохгүй бол nullptr
    const Oyutan *oloh(const std::string &ner) const {
        // TODO
        return nullptr;
    }

    // Олдохгүй бол false
    bool hasah(const std::string &ner) {
        // TODO: oyutnuud_.erase
        return false;
    }

    void jagsaah() const {
        // TODO: хоосон бол «Бүртгэл хоосон.», эс бөгөөс хуулбарыг
        // std::sort + лямбдагаар дунджаар буурахаар эрэмбэлж хэвлэ
    }

private:
    std::vector<Oyutan> oyutnuud_;
};

int main() {
    Angi angi;
    std::string tushaal;

    std::cout << std::fixed << std::setprecision(2);

    while (std::cin >> tushaal && tushaal != "QUIT") {
        if (tushaal == "ADD") {
            std::string ner;
            int k;
            std::cin >> ner >> k;
            // TODO: k ширхэг дүнг std::vector<int>-д уншаад angi.nemeh-г дууд
        } else if (tushaal == "FIND") {
            // TODO
        } else if (tushaal == "REMOVE") {
            // TODO
        } else if (tushaal == "LIST") {
            angi.jagsaah();
        } else {
            std::cout << "Танихгүй тушаал: " << tushaal << "\\n";
        }
    }

    return 0;
}
""",
            exercise=ExerciseSpec(
                statement="""\
Оюутны бүртгэлийг хоёр класс — `Oyutan` (нэг оюутан) ба `Angi`
(оюутнуудын цуглуулга) — ашиглан удирдах програм бич.

**Оролт:** мөр бүрт нэг тушаал. Нэр нь зайгүй нэг үг.

- `ADD <нэр> <k> <д1> ... <дk>` — `k` ширхэг дүнтэй оюутан нэмнэ.
- `FIND <нэр>` — оюутны дундаж ба үнэлгээг харуулна.
- `REMOVE <нэр>` — оюутныг хасна.
- `LIST` — бүх оюутныг **дунджаар нь буурахаар** жагсаана.
- `QUIT` — програмыг дуусгана. Оролт дуусахад ч мөн адил.

**Гаралт:**

- `ADD`: `<нэр> нэмэгдлээ.`, нэр аль хэдийн байвал `<нэр> аль хэдийн байна.`
  Энэ үед ч тушаалын бүх дүнг уншиж дуусгана.
- `FIND`: `<нэр>: <дундаж> <үнэлгээ>`, жишээ нь `Бат: 85.00 B`; байхгүй бол
  `<нэр> олдсонгүй.`
- `REMOVE`: `<нэр> хасагдлаа.` эсвэл `<нэр> олдсонгүй.`
- `LIST`: хоосон бол `Бүртгэл хоосон.`, эс бөгөөс оюутан бүрт
  `<i>. <нэр> <дундаж> <үнэлгээ>` (`i` нь 1-ээс эхэлнэ).
- Танихгүй тушаал (мөрөнд ганцаараа ирнэ): `Танихгүй тушаал: <тушаал>`.

Дунджийг `std::fixed << std::setprecision(2)` форматаар хэвлэнэ. Үнэлгээ:
дундаж 90 ба түүнээс дээш бол `A`, 80+ `B`, 70+ `C`, 60+ `D`, бусад нь `F`.

**Хязгаарлалт:** 1 ≤ k ≤ 5, дүн нь 0–100 хоорондох бүхэл тоо. Бүртгэлд
зэрэг байгаа хоёр оюутны дундаж хэзээ ч тэнцэхгүй.
""",
                tests=(
                    TestCaseSpec(
                        stdin=(
                            "ADD Бат 3 85 92 78\n"
                            "ADD Сараа 2 70 65\n"
                            "ADD Дорж 4 95 89 91 90\n"
                            "FIND Сараа\n"
                            "LIST\n"
                            "QUIT\n"
                        ),
                        expected_output=(
                            "Бат нэмэгдлээ.\n"
                            "Сараа нэмэгдлээ.\n"
                            "Дорж нэмэгдлээ.\n"
                            "Сараа: 67.50 D\n"
                            "1. Дорж 91.25 A\n"
                            "2. Бат 85.00 B\n"
                            "3. Сараа 67.50 D\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="LIST\nFIND Бат\nREMOVE Бат\n",
                        expected_output="Бүртгэл хоосон.\nБат олдсонгүй.\nБат олдсонгүй.\n",
                    ),
                    TestCaseSpec(
                        stdin="ADD Анар 2 80 90\nADD Анар 3 10 20 30\nLIST\nQUIT\n",
                        expected_output="Анар нэмэгдлээ.\nАнар аль хэдийн байна.\n1. Анар 85.00 B\n",
                    ),
                    TestCaseSpec(
                        stdin=(
                            "ADD Бат 1 50\n"
                            "ADD Болд 1 60\n"
                            "ADD Ганаа 3 70 71 72\n"
                            "REMOVE Болд\n"
                            "SHOW\n"
                            "LIST\n"
                            "FIND Болд\n"
                            "QUIT\n"
                            "LIST\n"
                        ),
                        expected_output=(
                            "Бат нэмэгдлээ.\n"
                            "Болд нэмэгдлээ.\n"
                            "Ганаа нэмэгдлээ.\n"
                            "Болд хасагдлаа.\n"
                            "Танихгүй тушаал: SHOW\n"
                            "1. Ганаа 71.00 C\n"
                            "2. Бат 50.00 F\n"
                            "Болд олдсонгүй.\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin=(
                            "ADD Номин 2 90 90\n"
                            "ADD Тэмүүлэн 2 59 60\n"
                            "ADD Хулан 1 60\n"
                            "ADD Золбоо 5 79 80 81 80 80\n"
                            "FIND Тэмүүлэн\n"
                            "LIST\n"
                        ),
                        expected_output=(
                            "Номин нэмэгдлээ.\n"
                            "Тэмүүлэн нэмэгдлээ.\n"
                            "Хулан нэмэгдлээ.\n"
                            "Золбоо нэмэгдлээ.\n"
                            "Тэмүүлэн: 59.50 F\n"
                            "1. Номин 90.00 A\n"
                            "2. Золбоо 80.00 B\n"
                            "3. Хулан 60.00 D\n"
                            "4. Тэмүүлэн 59.50 F\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="ADD Оюун 1 70\nREMOVE Оюун\nADD Оюун 2 100 99\nLIST\nQUIT\n",
                        expected_output=(
                            "Оюун нэмэгдлээ.\nОюун хасагдлаа.\nОюун нэмэгдлээ.\n1. Оюун 99.50 A\n"
                        ),
                    ),
                ),
                solution="""\
#include <algorithm>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

// Нэг оюутан: нэр ба дүнгүүд. Дундаж, үнэлгээг хадгалахгүй — тооцоолно
class Oyutan {
public:
    Oyutan(std::string ner, std::vector<int> dun)
        : ner_(ner), dun_(dun) {
    }

    const std::string &ner() const { return ner_; }

    // double руу хөрвүүлж хуваана — бүхэл хуваалт бутархайг хаяна
    double dundaj() const {
        int niit = 0;
        for (int d : dun_) {
            niit += d;
        }
        return static_cast<double>(niit) / dun_.size();
    }

    // Дээрээс доош: эхний таарсан босго үнэлгээг өгнө
    char unelgee() const {
        const double d = dundaj();
        if (d >= 90.0) return 'A';
        if (d >= 80.0) return 'B';
        if (d >= 70.0) return 'C';
        if (d >= 60.0) return 'D';
        return 'F';
    }

private:
    std::string ner_;
    std::vector<int> dun_;
};

// Оюутнуудын цуглуулга — тушаал бүрт нэг гишүүн функц
class Angi {
public:
    // ADD — нэр давхардвал нэмэхгүй
    bool nemeh(const Oyutan &o) {
        if (oloh(o.ner()) != nullptr) {
            return false;
        }
        oyutnuud_.push_back(o);
        return true;
    }

    // FIND — олдохгүй бол nullptr
    const Oyutan *oloh(const std::string &ner) const {
        for (const auto &o : oyutnuud_) {
            if (o.ner() == ner) {
                return &o;
            }
        }
        return nullptr;
    }

    // REMOVE — индексээр нь erase хийнэ
    bool hasah(const std::string &ner) {
        for (std::size_t i = 0; i < oyutnuud_.size(); i++) {
            if (oyutnuud_[i].ner() == ner) {
                oyutnuud_.erase(oyutnuud_.begin() + i);
                return true;
            }
        }
        return false;
    }

    // LIST — хуулбарыг дунджаар буурахаар эрэмбэлнэ, эх дараалал хэвээр
    void jagsaah() const {
        if (oyutnuud_.empty()) {
            std::cout << "Бүртгэл хоосон.\\n";
            return;
        }

        std::vector<Oyutan> erembelsen = oyutnuud_;
        std::sort(erembelsen.begin(), erembelsen.end(),
                  [](const Oyutan &a, const Oyutan &b) {
                      return a.dundaj() > b.dundaj();
                  });

        for (std::size_t i = 0; i < erembelsen.size(); i++) {
            const Oyutan &o = erembelsen[i];
            std::cout << i + 1 << ". " << o.ner() << " " << o.dundaj() << " "
                      << o.unelgee() << "\\n";
        }
    }

private:
    std::vector<Oyutan> oyutnuud_;
};

int main() {
    Angi angi;
    std::string tushaal;

    // Бүх бутархай тоог 2 оронтой хэвлэх тохиргоо — нэг удаа
    std::cout << std::fixed << std::setprecision(2);

    while (std::cin >> tushaal && tushaal != "QUIT") {
        if (tushaal == "ADD") {
            std::string ner;
            int k;
            std::cin >> ner >> k;

            // Нэр давхардсан ч k дүнг бүгдийг уншина — эс бөгөөс
            // үлдсэн дүнгүүд дараагийн тушаал мэт уншигдана
            std::vector<int> dun(k, 0);
            for (int &d : dun) {
                std::cin >> d;
            }

            if (angi.nemeh(Oyutan(ner, dun))) {
                std::cout << ner << " нэмэгдлээ.\\n";
            } else {
                std::cout << ner << " аль хэдийн байна.\\n";
            }
        } else if (tushaal == "FIND") {
            std::string ner;
            std::cin >> ner;
            // Заагчийг ашиглахаас өмнө nullptr эсэхийг шалгана
            const Oyutan *o = angi.oloh(ner);
            if (o != nullptr) {
                std::cout << ner << ": " << o->dundaj() << " " << o->unelgee() << "\\n";
            } else {
                std::cout << ner << " олдсонгүй.\\n";
            }
        } else if (tushaal == "REMOVE") {
            std::string ner;
            std::cin >> ner;
            if (angi.hasah(ner)) {
                std::cout << ner << " хасагдлаа.\\n";
            } else {
                std::cout << ner << " олдсонгүй.\\n";
            }
        } else if (tushaal == "LIST") {
            angi.jagsaah();
        } else {
            std::cout << "Танихгүй тушаал: " << tushaal << "\\n";
        }
    }

    return 0;
}
""",
                tips="""\
- Хоёр класс: `Oyutan` (нэр + `std::vector<int>` дүн; `dundaj()`, `unelgee()`
  нь утгыг хадгалахгүй, тооцоолж буцаана) ба `Angi` (`std::vector<Oyutan>`;
  `nemeh`, `oloh`, `hasah`, `jagsaah`). `main` зөвхөн тушаал уншиж, `Angi`-ийн
  функцийг дуудна.
- `ADD` дээр `k`-г уншаад `k` ширхэг дүнг **заавал бүгдийг** унш — нэр
  давхардсан үед ч. Эс бөгөөс үлдсэн дүнгүүд дараагийн тушаал мэт уншигдана.
- `oloh` нь олдохгүй бол `nullptr` буцаадаг бол `nemeh` доторх давхардлын
  шалгалт болон `FIND` хоёулаа түүнийг ашиглана. `hasah`-д
  `erase(oyutnuud_.begin() + i)` хэрэглэ.
- Дундажийг `static_cast<double>(niit) / dun_.size()` гэж бод — бүхэл хуваалт
  бутархайг хаяна. Үнэлгээний босгыг `>=`-ээр дээрээс доош шалга, яг 60 бол
  `D`.
- `LIST` нь **хуулбарыг** `std::sort` + лямбдагаар (`a.dundaj() > b.dundaj()`)
  эрэмбэлнэ. `std::fixed << std::setprecision(2)`-г `main`-ийн эхэнд нэг удаа
  тохируул. Хассан оюутныг дахин нэмж болно.
""",
            ),
        ),
        LessonSpec(
            title="Төсөл — Банкны програм",
            slug="cpp-bank-programm",
            description="Инкапсуляци, гүйлгээний түүх, алдаа боловсруулалт.",
            duration=720,
            language=CPP,
            content="""\
Дансны үйл ажиллагааг загварчилсан програм. Модул 18-ийн инкапсуляцийг
бүрэн ашиглана.

### Яагаад инкапсуляци чухал вэ

Банкны үлдэгдэл бол **хамгийн сайн жишээ**. Хэн ч гаднаас нь шууд
өөрчилж болохгүй:

```cpp
dans.uldegdel_ = 1000000;    // private тул ХӨРВҮҮЛЭХГҮЙ
```

Бүх өөрчлөлт `nemeh` эсвэл `hasah`-аар дамжина. Тэнд шалгалт болон
түүхийн бичилт хийгдэнэ.

### Гүйлгээний бүтэц

```cpp
struct Guilgee {
    std::string turul;
    double dun;
    double uldegdel_daraa;
};
```

Гүйлгээ бүрийн дараах үлдэгдлийг хадгалах нь дараа нь шалгахад тусална.

Шинэ гүйлгээг түүхэнд нэмэхдээ бүтцийн утгуудыг `{...}` дотор талбаруудын
дарааллаар нь бичиж болно — Модул 10-ын `struct` эхлүүлэлттэй ижил:

```cpp
Guilgee g = {"Орлого", 500, 1500};
tuuh_.push_back(g);

tuuh_.push_back({"Орлого", 500, 1500});   // ижил зүйл, товчхон
```

### Мөнгө ба бутархай

> Бодит банкны системд мөнгийг **бүхэл тоогоор** (жижиг нэгжээр)
> хадгална. `double` нь тооцооллын алдаа хуримтлуулдаг тул мөнгөнд
> тохиромжгүй.

Энэ сургалтын төсөлд `double` ашиглав — гэхдээ бодит системд `long long`
эсвэл тусгай төрөл сонго.

`long long` нь `int`-ийн том ах: 8 байт, ойролцоогоор ±9·10¹⁸ хүртэлх бүхэл
тоо багтана (`int` нь ±2.1·10⁹ хүртэл). `std::cin`, `std::cout` түүнийг
`int`-тэй адил уншиж, хэвлэнэ.

### Алдааг хэрхэн мэдэгдэх вэ

Хоёр арга:

```cpp
bool hasah(double dun);                 // амжилт эсэхийг буцаана
void hasah(double dun);                 // амжилтгүй бол онцгой байдал
```

Үлдэгдэл хүрэлцэхгүй нь **хүлээгдэж буй** тохиолдол тул `bool` илүү
тохиромжтой. Онцгой байдлыг үнэхээр гэнэтийн зүйлд үлдээ.

### Нэмэлт сорилт

1. Дансны хооронд шилжүүлэх метод нэмээрэй.
2. Хүүгийн тооцоолол нэмээрэй.
3. Гүйлгээнд огноо нэмээрэй (`<chrono>`).

### Жишээ програм

```cpp
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

struct Guilgee {
    std::string turul;
    double dun;
    double uldegdel_daraa;
};

class Dans {
public:
    Dans(std::string ezen, double ehleliin = 0.0)
        : ezen_(ezen), uldegdel_(ehleliin < 0 ? 0 : ehleliin) {
        if (uldegdel_ > 0) {
            tuuh_.push_back({"Нээлт", uldegdel_, uldegdel_});
        }
    }

    bool nemeh(double dun) {
        if (dun <= 0) {
            return false;
        }
        uldegdel_ += dun;
        tuuh_.push_back({"Орлого", dun, uldegdel_});
        return true;
    }

    bool hasah(double dun) {
        if (dun <= 0 || dun > uldegdel_) {
            return false;
        }
        uldegdel_ -= dun;
        tuuh_.push_back({"Зарлага", -dun, uldegdel_});
        return true;
    }

    double uldegdel() const { return uldegdel_; }
    const std::string &ezen() const { return ezen_; }

    void hurangui() const {
        std::cout << ezen_ << ": " << std::fixed << std::setprecision(2)
                  << uldegdel_ << "₮ (" << tuuh_.size() << " гүйлгээ)\\n";
    }

    void tuuh_hevleh() const {
        std::cout << "\\n=== " << ezen_ << " ===\\n";
        std::cout << std::left << std::setw(10) << "Төрөл"
                  << std::right << std::setw(12) << "Дүн"
                  << std::setw(14) << "Үлдэгдэл" << "\\n";

        for (const auto &g : tuuh_) {
            std::cout << std::left << std::setw(10) << g.turul
                      << std::right << std::setw(12) << std::fixed
                      << std::setprecision(2) << g.dun
                      << std::setw(14) << g.uldegdel_daraa << "\\n";
        }
    }

private:
    std::string ezen_;
    double uldegdel_;
    std::vector<Guilgee> tuuh_;
};

int main() {
    Dans bat("Бат", 1000);
    Dans saraa("Сараа");

    bat.nemeh(500);
    bat.hasah(200);

    saraa.nemeh(3000);
    saraa.hasah(500);

    std::cout << "=== Дансны хураангуй ===\\n";
    bat.hurangui();
    saraa.hurangui();

    // Хүлээгдэж буй алдаа — bool-оор мэдэгдэнэ
    if (!bat.hasah(99999)) {
        std::cout << "\\nБатын үлдэгдэл хүрэлцэхгүй\\n";
    }

    if (!bat.nemeh(-100)) {
        std::cout << "Сөрөг дүн нэмэх боломжгүй\\n";
    }

    bat.tuuh_hevleh();
    saraa.tuuh_hevleh();

    return 0;
}
```
""",
            initial_code="""\
#include <iostream>
#include <string>
#include <vector>

struct Guilgee {
    std::string turul;          // "Орлого" эсвэл "Зарлага"
    long long dun;
    long long uldegdel_daraa;   // гүйлгээний дараах үлдэгдэл
};

class Dans {
public:
    Dans(std::string ezen, long long ehleliin)
        : ezen_(ezen), uldegdel_(ehleliin) {
    }

    void nemeh(long long dun) {
        // TODO: үлдэгдлийг нэмээд түүхэнд бич
    }

    // Үлдэгдэл хүрэлцэхгүй бол юу ч өөрчлөхгүйгээр false буцаана
    bool hasah(long long dun) {
        // TODO
        return false;
    }

    long long uldegdel() const { return uldegdel_; }
    const std::string &ezen() const { return ezen_; }

    void tuuh_hevleh() const {
        // TODO: «Гүйлгээ алга.» эсвэл дугаарласан мөрүүд
    }

private:
    std::string ezen_;
    long long uldegdel_;
    std::vector<Guilgee> tuuh_;
};

int main() {
    std::string ezen;
    long long ehleliin;
    if (!(std::cin >> ezen >> ehleliin)) {
        return 1;
    }

    Dans dans(ezen, ehleliin);
    std::string tushaal;

    while (std::cin >> tushaal && tushaal != "QUIT") {
        if (tushaal == "DEPOSIT" || tushaal == "WITHDRAW") {
            long long dun;
            if (!(std::cin >> dun)) {
                break;
            }
            // TODO: эерэг эсэхийг шалгаад dans.nemeh эсвэл dans.hasah-г дууд
        } else if (tushaal == "BALANCE") {
            std::cout << dans.ezen() << ": " << dans.uldegdel() << "\\n";
        } else if (tushaal == "HISTORY") {
            dans.tuuh_hevleh();
        } else {
            std::cout << "Танихгүй тушаал: " << tushaal << "\\n";
        }
    }

    return 0;
}
""",
            exercise=ExerciseSpec(
                statement="""\
Нэг банкны дансыг удирдах програм бич. Үлдэгдлийг зөвхөн `Dans` классын
методоор өөрчилнө — `private` талбарт гаднаас шууд хандахгүй.

**Оролт:** эхний мөрөнд дансны эзний нэр (зайгүй нэг үг) ба эхний үлдэгдэл.
Дараагийн мөр бүрт нэг тушаал:

- `DEPOSIT <дүн>` — данс руу мөнгө хийнэ.
- `WITHDRAW <дүн>` — данснаас мөнгө авна.
- `BALANCE` — үлдэгдлийг харуулна.
- `HISTORY` — амжилттай гүйлгээнүүдийг харуулна.
- `QUIT` — програмыг дуусгана. Оролт дуусахад ч мөн адил.

**Гаралт:**

- `DEPOSIT`: `Орлого: <дүн>. Үлдэгдэл: <үлдэгдэл>`
- `WITHDRAW`: `Зарлага: <дүн>. Үлдэгдэл: <үлдэгдэл>`, үлдэгдэл хүрэлцэхгүй
  бол `Алдаа: үлдэгдэл хүрэлцэхгүй.`
- `DEPOSIT` ба `WITHDRAW`-ийн дүн 0 эсвэл сөрөг бол
  `Алдаа: дүн эерэг байх ёстой.` Үүнийг үлдэгдлээс **өмнө** шалгана.
- `BALANCE`: `<эзэн>: <үлдэгдэл>`
- `HISTORY`: гүйлгээ байхгүй бол `Гүйлгээ алга.`, эс бөгөөс гүйлгээ бүрт
  `<i>. Орлого <дүн> -> <үлдэгдэл>` эсвэл `<i>. Зарлага <дүн> -> <үлдэгдэл>`
  (`i` нь 1-ээс эхэлнэ, үлдэгдэл нь тэр гүйлгээний дараах). Амжилтгүй
  гүйлгээ түүхэнд **орохгүй**.
- Танихгүй тушаал (мөрөнд ганцаараа ирнэ): `Танихгүй тушаал: <тушаал>`.

**Хязгаарлалт:** бүх дүн бүхэл тоо, үлдэгдэл 0-ээс 10^12 хооронд байна.
Энэ нь `int`-д багтахгүй тул `long long` ашигла.
""",
                tests=(
                    TestCaseSpec(
                        stdin=(
                            "Бат 1000\n"
                            "DEPOSIT 500\n"
                            "WITHDRAW 200\n"
                            "WITHDRAW 5000\n"
                            "BALANCE\n"
                            "HISTORY\n"
                            "QUIT\n"
                        ),
                        expected_output=(
                            "Орлого: 500. Үлдэгдэл: 1500\n"
                            "Зарлага: 200. Үлдэгдэл: 1300\n"
                            "Алдаа: үлдэгдэл хүрэлцэхгүй.\n"
                            "Бат: 1300\n"
                            "1. Орлого 500 -> 1500\n"
                            "2. Зарлага 200 -> 1300\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin=(
                            "Сараа 0\n"
                            "HISTORY\n"
                            "WITHDRAW 1\n"
                            "WITHDRAW -5\n"
                            "DEPOSIT 0\n"
                            "DEPOSIT -50\n"
                            "BALANCE\n"
                        ),
                        expected_output=(
                            "Гүйлгээ алга.\n"
                            "Алдаа: үлдэгдэл хүрэлцэхгүй.\n"
                            "Алдаа: дүн эерэг байх ёстой.\n"
                            "Алдаа: дүн эерэг байх ёстой.\n"
                            "Алдаа: дүн эерэг байх ёстой.\n"
                            "Сараа: 0\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="Дорж 300\nWITHDRAW 300\nBALANCE\nWITHDRAW 1\nHISTORY\nQUIT\nDEPOSIT 5\n",
                        expected_output=(
                            "Зарлага: 300. Үлдэгдэл: 0\n"
                            "Дорж: 0\n"
                            "Алдаа: үлдэгдэл хүрэлцэхгүй.\n"
                            "1. Зарлага 300 -> 0\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin=(
                            "Оюун 2000000000\n"
                            "DEPOSIT 2000000000\n"
                            "TRANSFER\n"
                            "WITHDRAW 3999999999\n"
                            "BALANCE\n"
                            "HISTORY\n"
                        ),
                        expected_output=(
                            "Орлого: 2000000000. Үлдэгдэл: 4000000000\n"
                            "Танихгүй тушаал: TRANSFER\n"
                            "Зарлага: 3999999999. Үлдэгдэл: 1\n"
                            "Оюун: 1\n"
                            "1. Орлого 2000000000 -> 4000000000\n"
                            "2. Зарлага 3999999999 -> 1\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin=(
                            "Анар 50\n"
                            "DEPOSIT 25\n"
                            "DEPOSIT 25\n"
                            "WITHDRAW 100\n"
                            "WITHDRAW 1\n"
                            "HISTORY\n"
                            "BALANCE\n"
                            "QUIT\n"
                        ),
                        expected_output=(
                            "Орлого: 25. Үлдэгдэл: 75\n"
                            "Орлого: 25. Үлдэгдэл: 100\n"
                            "Зарлага: 100. Үлдэгдэл: 0\n"
                            "Алдаа: үлдэгдэл хүрэлцэхгүй.\n"
                            "1. Орлого 25 -> 75\n"
                            "2. Орлого 25 -> 100\n"
                            "3. Зарлага 100 -> 0\n"
                            "Анар: 0\n"
                        ),
                    ),
                ),
                solution="""\
#include <iostream>
#include <string>
#include <vector>

// Нэг амжилттай гүйлгээний бичлэг
struct Guilgee {
    std::string turul;          // "Орлого" эсвэл "Зарлага"
    long long dun;
    long long uldegdel_daraa;   // гүйлгээний дараах үлдэгдэл
};

// Үлдэгдэл private — зөвхөн nemeh/hasah методоор өөрчлөгдөнө
class Dans {
public:
    Dans(std::string ezen, long long ehleliin)
        : ezen_(ezen), uldegdel_(ehleliin) {
    }

    // DEPOSIT — дүн эерэг гэдгийг main аль хэдийн шалгасан
    void nemeh(long long dun) {
        uldegdel_ += dun;
        tuuh_.push_back({"Орлого", dun, uldegdel_});
    }

    // WITHDRAW — хүрэлцэхгүй бол юу ч өөрчлөхгүй, түүхэнд ч бичихгүй
    bool hasah(long long dun) {
        if (dun > uldegdel_) {
            return false;
        }
        uldegdel_ -= dun;
        tuuh_.push_back({"Зарлага", dun, uldegdel_});
        return true;
    }

    long long uldegdel() const { return uldegdel_; }
    const std::string &ezen() const { return ezen_; }

    // HISTORY — дугаар 1-ээс эхэлнэ
    void tuuh_hevleh() const {
        if (tuuh_.empty()) {
            std::cout << "Гүйлгээ алга.\\n";
            return;
        }
        for (std::size_t i = 0; i < tuuh_.size(); i++) {
            const Guilgee &g = tuuh_[i];
            std::cout << i + 1 << ". " << g.turul << " " << g.dun << " -> "
                      << g.uldegdel_daraa << "\\n";
        }
    }

private:
    std::string ezen_;
    long long uldegdel_;          // int-д багтахгүй дүн ирж болно
    std::vector<Guilgee> tuuh_;
};

int main() {
    // Эхний мөр — эзний нэр ба эхний үлдэгдэл
    std::string ezen;
    long long ehleliin;
    if (!(std::cin >> ezen >> ehleliin)) {
        return 1;
    }

    Dans dans(ezen, ehleliin);
    std::string tushaal;

    while (std::cin >> tushaal && tushaal != "QUIT") {
        if (tushaal == "DEPOSIT" || tushaal == "WITHDRAW") {
            long long dun;
            if (!(std::cin >> dun)) {
                break;
            }

            // Дараалал: эхлээд дүн эерэг эсэх, дараа нь үлдэгдэл хүрэлцэх эсэх
            if (dun <= 0) {
                std::cout << "Алдаа: дүн эерэг байх ёстой.\\n";
            } else if (tushaal == "DEPOSIT") {
                dans.nemeh(dun);
                std::cout << "Орлого: " << dun << ". Үлдэгдэл: " << dans.uldegdel() << "\\n";
            } else if (dans.hasah(dun)) {
                std::cout << "Зарлага: " << dun << ". Үлдэгдэл: " << dans.uldegdel() << "\\n";
            } else {
                std::cout << "Алдаа: үлдэгдэл хүрэлцэхгүй.\\n";
            }
        } else if (tushaal == "BALANCE") {
            std::cout << dans.ezen() << ": " << dans.uldegdel() << "\\n";
        } else if (tushaal == "HISTORY") {
            dans.tuuh_hevleh();
        } else {
            std::cout << "Танихгүй тушаал: " << tushaal << "\\n";
        }
    }

    return 0;
}
""",
                tips="""\
- `Dans` класст `private` талбарууд (`ezen_`, `uldegdel_`,
  `std::vector<Guilgee> tuuh_`) байлга. Үлдэгдлийг зөвхөн `nemeh` / `hasah`
  методоор өөрчил. `Guilgee` struct нь төрөл, дүн, гүйлгээний **дараах**
  үлдэгдлийг хадгална.
- Эхлээд эзэн ба эхний үлдэгдлийг уншаад дансаа үүсгэ, дараа нь
  `while (std::cin >> tushaal && tushaal != "QUIT")` давталтаар тушаал унш.
- Шалгах дараалал: дүн `<= 0` эсэх → (`WITHDRAW` бол) үлдэгдэл хүрэлцэх эсэх
  → гүйлгээ. Сөрөг дүнтэй `WITHDRAW` нь «хүрэлцэхгүй» биш «эерэг байх ёстой»
  гэсэн алдаа өгнө.
- `hasah` нь хүрэлцэхгүй үед юу ч өөрчлөхгүйгээр `false` буцаана — амжилтгүй
  гүйлгээ түүхэнд орохгүй. Үлдэгдлээ **бүгдийг нь** авах (`dun == uldegdel_`)
  зөвшөөрөгдөнө.
- Бүх мөнгөн дүнг `long long`-оор унш, хадгал — `int`-д багтахгүй том тоо
  ирнэ. Эхний үлдэгдэл түүхэнд гүйлгээ болж **орохгүй**.
""",
            ),
        ),
        LessonSpec(
            title="Төсөл — Номын сангийн систем",
            slug="cpp-oop-tusul",
            description="Хэд хэдэн класс хамтран ажиллах.",
            duration=780,
            language=CPP,
            content="""\
Эцсийн төсөл: ном зээлдүүлэх систем. Хэд хэдэн класс хамтран ажиллана.

### Классуудын үүрэг

| Класс | Хариуцах зүйл |
|---|---|
| `Nom` | Нэг номын мэдээлэл, төлөв |
| `Nomiin_san` | Номын цуглуулга, зээлдүүлэх логик |

Ганц класс бүгдийг хийхийг **бүү** зөвшөөр. Класс бүр нэг сэдэвтэй
байх ёстой.

### Төлөв удирдах

```cpp
class Nom {
public:
    bool zeeldueleh();
    bool butsaah();
    bool bolomjtoi() const { return bolomjtoi_; }

private:
    bool bolomjtoi_ = true;
};
```

Төлөв өөрчлөх логик нь **тэр объектын дотор** байна. Гаднаас
`nom.bolomjtoi_ = false` гэж бичих боломжгүй.

### Хоёр дахин зээлдүүлэхээс сэргийлэх

```cpp
bool Nom::zeeldueleh() {
    if (!bolomjtoi_) {
        return false;
    }
    bolomjtoi_ = false;
    return true;
}
```

Метод нь өөрөө шалгадаг тул дуудсан тал мартах боломжгүй. Энэ бол
инкапсуляцийн бодит ашиг.

### Заагч буцаах

```cpp
Nom *oloh(const std::string &garchig);
```

`Nom_san` доторх бодит объект руу заана — хуулбар биш. Тиймээс түүнийг
өөрчилвөл эх өгөгдөл өөрчлөгдөнө.

> Вектор дотор элемент **нэмэхэд** хуучин заагч хүчингүй болж болзошгүй
> (вектор өсөхдөө санах ойгоо зөөдөг). Заагчийг удаан бүү хадгал.

### Гишүүн эхлүүлэгч

```cpp
private:
    bool bolomjtoi_ = true;
```

C++11-ээс хойш талбарт анхдагч утгыг шууд өгч болно. Конструктор бүрт
давтах шаардлагагүй.

### Нэмэлт сорилт

1. Зээлдэгчийн нэрийг хадгалаарай.
2. Зохиогчоор хайх метод нэмээрэй.
3. Зээлсэн бүх номыг жагсаах метод нэмээрэй.
4. Номын ангилал нэмж, ангиллаар шүүгээрэй.

### Жишээ програм

```cpp
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

class Nom {
public:
    Nom(std::string garchig, std::string zohiogch, int jil)
        : garchig_(garchig), zohiogch_(zohiogch), jil_(jil) {
    }

    const std::string &garchig() const { return garchig_; }
    const std::string &zohiogch() const { return zohiogch_; }
    int jil() const { return jil_; }
    bool bolomjtoi() const { return bolomjtoi_; }

    // Шалгалт нь методын ДОТОР — дуудсан тал мартах боломжгүй
    bool zeeldueleh() {
        if (!bolomjtoi_) {
            return false;
        }
        bolomjtoi_ = false;
        zeelsen_too_++;
        return true;
    }

    bool butsaah() {
        if (bolomjtoi_) {
            return false;   // аль хэдийн санд байна
        }
        bolomjtoi_ = true;
        return true;
    }

    int zeelsen_too() const { return zeelsen_too_; }

private:
    std::string garchig_;
    std::string zohiogch_;
    int jil_;
    bool bolomjtoi_ = true;   // C++11 гишүүн эхлүүлэгч
    int zeelsen_too_ = 0;
};

class Nomiin_san {
public:
    void nemeh(const Nom &nom) { nomuud_.push_back(nom); }

    Nom *oloh(const std::string &garchig) {
        for (auto &nom : nomuud_) {
            if (nom.garchig() == garchig) {
                return &nom;
            }
        }
        return nullptr;
    }

    int bolomjtoin_too() const {
        int too = 0;
        for (const auto &nom : nomuud_) {
            if (nom.bolomjtoi()) {
                too++;
            }
        }
        return too;
    }

    void hevleh() const {
        std::cout << std::left << std::setw(22) << "Гарчиг"
                  << std::setw(16) << "Зохиогч"
                  << std::right << std::setw(6) << "Он"
                  << std::setw(12) << "Төлөв" << "\\n";

        for (const auto &nom : nomuud_) {
            std::cout << std::left << std::setw(22) << nom.garchig()
                      << std::setw(16) << nom.zohiogch()
                      << std::right << std::setw(6) << nom.jil()
                      << std::setw(12) << (nom.bolomjtoi() ? "Санд" : "Зээлсэн")
                      << "\\n";
        }
    }

private:
    std::vector<Nom> nomuud_;
};

int main() {
    Nomiin_san san;

    san.nemeh(Nom("Цагаан хэрэм", "Б. Ринчен", 1971));
    san.nemeh(Nom("Тунгалаг Тамир", "Ч. Лодойдамба", 1962));
    san.nemeh(Nom("Clean Code", "R. Martin", 2008));

    std::cout << "=== Номын сан ===\\n";
    san.hevleh();

    // Зээлдүүлэх
    std::cout << "\\n--- Зээлдүүлэх ---\\n";
    Nom *nom = san.oloh("Clean Code");
    if (nom != nullptr) {
        if (nom->zeeldueleh()) {
            std::cout << "«" << nom->garchig() << "» зээллээ\\n";
        }

        // Хоёр дахин зээлдүүлэхийг метод өөрөө хориглоно
        if (!nom->zeeldueleh()) {
            std::cout << "«" << nom->garchig() << "» аль хэдийн зээлэгдсэн\\n";
        }
    }

    if (san.oloh("Байхгүй ном") == nullptr) {
        std::cout << "«Байхгүй ном» олдсонгүй\\n";
    }

    san.hevleh();
    std::cout << "\\nБоломжтой: " << san.bolomjtoin_too() << " ном\\n";

    // Буцаах
    std::cout << "\\n--- Буцаах ---\\n";
    nom = san.oloh("Clean Code");
    if (nom != nullptr) {
        if (nom->butsaah()) {
            std::cout << "«" << nom->garchig() << "» буцаалаа ("
                      << nom->zeelsen_too() << " удаа зээлэгдсэн)\\n";
        }
    }

    std::cout << "Боломжтой: " << san.bolomjtoin_too() << " ном\\n";

    return 0;
}
```
""",
            initial_code="""\
#include <iostream>
#include <string>
#include <vector>

class Nom {
public:
    Nom(std::string garchig) : garchig_(garchig) {
    }

    const std::string &garchig() const { return garchig_; }
    const std::string &zeeldegch() const { return zeeldegch_; }
    bool bolomjtoi() const { return zeeldegch_.empty(); }

    // Аль хэдийн зээлэгдсэн бол false
    bool zeeldeh(const std::string &ner) {
        // TODO
        return false;
    }

    // Ном санд байгаа бол false
    bool butsaah() {
        // TODO
        return false;
    }

private:
    std::string garchig_;
    std::string zeeldegch_;   // хоосон бол ном санд байна
};

class Nomiin_san {
public:
    // Гарчиг давхардвал false
    bool nemeh(const std::string &garchig) {
        // TODO
        return false;
    }

    // Олдохгүй бол nullptr
    Nom *oloh(const std::string &garchig) {
        // TODO
        return nullptr;
    }

    void jagsaah() const {
        // TODO: «Номын сан хоосон.» эсвэл дугаарласан мөрүүд
    }

private:
    std::vector<Nom> nomuud_;
};

int main() {
    Nomiin_san san;
    std::string tushaal;

    while (std::cin >> tushaal && tushaal != "QUIT") {
        if (tushaal == "ADD") {
            std::string garchig;
            std::cin >> garchig;
            // TODO
        } else if (tushaal == "BORROW") {
            std::string garchig;
            std::string ner;
            std::cin >> garchig >> ner;
            // TODO: san.oloh-оор хайгаад nom->zeeldeh-г дууд
        } else if (tushaal == "RETURN") {
            std::string garchig;
            std::cin >> garchig;
            // TODO
        } else if (tushaal == "LIST") {
            san.jagsaah();
        } else {
            std::cout << "Танихгүй тушаал: " << tushaal << "\\n";
        }
    }

    return 0;
}
""",
            exercise=ExerciseSpec(
                statement="""\
Номын сангийн зээлийн системийг хоёр класс — `Nom` (нэг ном) ба
`Nomiin_san` (номын цуглуулга) — ашиглан бич. Ном бүр хэн зээлснийг санана.

**Оролт:** мөр бүрт нэг тушаал. Гарчиг ба зээлдэгчийн нэр нь зайгүй нэг үг
(гарчигт зайны оронд `_` ашиглана).

- `ADD <гарчиг>` — ном нэмнэ.
- `BORROW <гарчиг> <нэр>` — номыг зээлдүүлнэ.
- `RETURN <гарчиг>` — номыг буцааж авна.
- `LIST` — бүх номыг нэмсэн дарааллаар жагсаана.
- `QUIT` — програмыг дуусгана. Оролт дуусахад ч мөн адил.

**Гаралт:**

- `ADD`: `<гарчиг> нэмэгдлээ.`, давхардвал `<гарчиг> аль хэдийн байна.`
- `BORROW`: `Зээллээ: <гарчиг> -> <нэр>`; ном аль хэдийн зээлэгдсэн бол
  `<гарчиг> аль хэдийн зээлэгдсэн (<зээлдэгч>).`
- `RETURN`: `Буцаалаа: <гарчиг>`; ном санд байвал `<гарчиг> санд байна.`
- `BORROW`, `RETURN`-д ийм ном байхгүй бол `<гарчиг> олдсонгүй.`
- `LIST`: хоосон бол `Номын сан хоосон.`, эс бөгөөс ном бүрт
  `<i>. <гарчиг>: санд` эсвэл `<i>. <гарчиг>: <зээлдэгч> зээлсэн` (`i` нь
  1-ээс эхэлнэ).
- Танихгүй тушаал (мөрөнд ганцаараа ирнэ): `Танихгүй тушаал: <тушаал>`.

Цэс, асуулт **бүү хэвлэ** — шалгагч зөвхөн гаралтыг харьцуулна.
""",
                tests=(
                    TestCaseSpec(
                        stdin=(
                            "ADD Clean_Code\n"
                            "ADD Цагаан_хэрэм\n"
                            "BORROW Clean_Code Бат\n"
                            "BORROW Clean_Code Сараа\n"
                            "LIST\n"
                            "RETURN Clean_Code\n"
                            "QUIT\n"
                        ),
                        expected_output=(
                            "Clean_Code нэмэгдлээ.\n"
                            "Цагаан_хэрэм нэмэгдлээ.\n"
                            "Зээллээ: Clean_Code -> Бат\n"
                            "Clean_Code аль хэдийн зээлэгдсэн (Бат).\n"
                            "1. Clean_Code: Бат зээлсэн\n"
                            "2. Цагаан_хэрэм: санд\n"
                            "Буцаалаа: Clean_Code\n"
                        ),
                        sample=True,
                    ),
                    TestCaseSpec(
                        stdin="LIST\nBORROW Дуу Бат\nRETURN Дуу\n",
                        expected_output="Номын сан хоосон.\nДуу олдсонгүй.\nДуу олдсонгүй.\n",
                    ),
                    TestCaseSpec(
                        stdin=(
                            "ADD Тунгалаг_Тамир\n"
                            "ADD Тунгалаг_Тамир\n"
                            "RETURN Тунгалаг_Тамир\n"
                            "READ\n"
                            "LIST\n"
                            "QUIT\n"
                        ),
                        expected_output=(
                            "Тунгалаг_Тамир нэмэгдлээ.\n"
                            "Тунгалаг_Тамир аль хэдийн байна.\n"
                            "Тунгалаг_Тамир санд байна.\n"
                            "Танихгүй тушаал: READ\n"
                            "1. Тунгалаг_Тамир: санд\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin=(
                            "ADD Цагаан_хэрэм\n"
                            "ADD Clean_Code\n"
                            "BORROW Clean_Code Анар\n"
                            "RETURN Clean_Code\n"
                            "BORROW Clean_Code Болд\n"
                            "BORROW Цагаан_хэрэм Болд\n"
                            "BORROW Цагаан_хэрэм Анар\n"
                            "LIST\n"
                            "QUIT\n"
                            "LIST\n"
                        ),
                        expected_output=(
                            "Цагаан_хэрэм нэмэгдлээ.\n"
                            "Clean_Code нэмэгдлээ.\n"
                            "Зээллээ: Clean_Code -> Анар\n"
                            "Буцаалаа: Clean_Code\n"
                            "Зээллээ: Clean_Code -> Болд\n"
                            "Зээллээ: Цагаан_хэрэм -> Болд\n"
                            "Цагаан_хэрэм аль хэдийн зээлэгдсэн (Болд).\n"
                            "1. Цагаан_хэрэм: Болд зээлсэн\n"
                            "2. Clean_Code: Болд зээлсэн\n"
                        ),
                    ),
                    TestCaseSpec(
                        stdin="ADD Дуу\nBORROW Шүлэг Бат\nBORROW Дуу Сараа\nRETURN Дуу\nRETURN Дуу\nLIST\n",
                        expected_output=(
                            "Дуу нэмэгдлээ.\n"
                            "Шүлэг олдсонгүй.\n"
                            "Зээллээ: Дуу -> Сараа\n"
                            "Буцаалаа: Дуу\n"
                            "Дуу санд байна.\n"
                            "1. Дуу: санд\n"
                        ),
                    ),
                ),
                solution="""\
#include <iostream>
#include <string>
#include <vector>

// Нэг ном: зээлдэгчийн нэр хоосон бол ном санд байна
class Nom {
public:
    Nom(std::string garchig) : garchig_(garchig) {
    }

    const std::string &garchig() const { return garchig_; }
    const std::string &zeeldegch() const { return zeeldegch_; }
    // Тусдаа bool хадгалахгүй — зээлдэгчээс төлөвийг гаргана
    bool bolomjtoi() const { return zeeldegch_.empty(); }

    // Аль хэдийн зээлэгдсэн бол төлөвийг өөрчлөхгүйгээр false
    bool zeeldeh(const std::string &ner) {
        if (!bolomjtoi()) {
            return false;
        }
        zeeldegch_ = ner;
        return true;
    }

    // Ном санд байгаа бол false
    bool butsaah() {
        if (bolomjtoi()) {
            return false;
        }
        zeeldegch_.clear();
        return true;
    }

private:
    std::string garchig_;
    std::string zeeldegch_;
};

// Номын цуглуулга — нэмсэн дарааллаа хадгална
class Nomiin_san {
public:
    // ADD — гарчиг давхардвал нэмэхгүй
    bool nemeh(const std::string &garchig) {
        if (oloh(garchig) != nullptr) {
            return false;
        }
        nomuud_.push_back(Nom(garchig));
        return true;
    }

    // const биш заагч буцаана — дуудсан тал номыг өөрчилж чадна.
    // Олдохгүй бол nullptr
    Nom *oloh(const std::string &garchig) {
        for (auto &nom : nomuud_) {
            if (nom.garchig() == garchig) {
                return &nom;
            }
        }
        return nullptr;
    }

    // LIST
    void jagsaah() const {
        if (nomuud_.empty()) {
            std::cout << "Номын сан хоосон.\\n";
            return;
        }
        for (std::size_t i = 0; i < nomuud_.size(); i++) {
            const Nom &nom = nomuud_[i];
            std::cout << i + 1 << ". " << nom.garchig() << ": ";
            if (nom.bolomjtoi()) {
                std::cout << "санд\\n";
            } else {
                std::cout << nom.zeeldegch() << " зээлсэн\\n";
            }
        }
    }

private:
    std::vector<Nom> nomuud_;
};

int main() {
    Nomiin_san san;
    std::string tushaal;

    while (std::cin >> tushaal && tushaal != "QUIT") {
        if (tushaal == "ADD") {
            std::string garchig;
            std::cin >> garchig;
            if (san.nemeh(garchig)) {
                std::cout << garchig << " нэмэгдлээ.\\n";
            } else {
                std::cout << garchig << " аль хэдийн байна.\\n";
            }
        } else if (tushaal == "BORROW") {
            // Ном олдсон эсэхээс үл хамааран хоёр үгийг бүгдийг уншина
            std::string garchig;
            std::string ner;
            std::cin >> garchig >> ner;

            // Дараалал: ном байгаа эсэх → зээлж болох эсэх
            Nom *nom = san.oloh(garchig);
            if (nom == nullptr) {
                std::cout << garchig << " олдсонгүй.\\n";
            } else if (nom->zeeldeh(ner)) {
                std::cout << "Зээллээ: " << garchig << " -> " << ner << "\\n";
            } else {
                std::cout << garchig << " аль хэдийн зээлэгдсэн (" << nom->zeeldegch() << ").\\n";
            }
        } else if (tushaal == "RETURN") {
            std::string garchig;
            std::cin >> garchig;

            // Дараалал: ном байгаа эсэх → буцааж болох эсэх
            Nom *nom = san.oloh(garchig);
            if (nom == nullptr) {
                std::cout << garchig << " олдсонгүй.\\n";
            } else if (nom->butsaah()) {
                std::cout << "Буцаалаа: " << garchig << "\\n";
            } else {
                std::cout << garchig << " санд байна.\\n";
            }
        } else if (tushaal == "LIST") {
            san.jagsaah();
        } else {
            std::cout << "Танихгүй тушаал: " << tushaal << "\\n";
        }
    }

    return 0;
}
""",
                tips="""\
- Хоёр класс: `Nom` (гарчиг + зээлдэгчийн нэр) ба `Nomiin_san`
  (`std::vector<Nom>`). Тусдаа `bool` төлөв хадгалахын оронд «зээлдэгч
  хоосон бол санд байна» (`zeeldegch_.empty()`) гэж тооцвол хоёр утга хэзээ ч
  зөрөхгүй.
- `oloh` нь **const биш** `Nom *` буцаавал `BORROW` / `RETURN` олдсон номыг
  шууд өөрчилнө; олдохгүй бол `nullptr`. Буцаасан заагчийг удаан хадгалж
  болохгүй — `push_back` хийхэд вектор шилжиж, заагч хүчингүй болж болно.
- `BORROW`, `RETURN`-ийн шалгах дараалал: ном байгаа эсэх → төлөв (зээлэгдсэн
  эсвэл санд) → үйлдэл. `BORROW`-д ном олдоогүй ч гарчиг ба нэрийг хоёуланг
  нь уншиж дуусга.
- `zeeldeh` / `butsaah` амжилтгүй бол төлөвийг өөрчлөхгүйгээр `false` буцаана.
  «аль хэдийн зээлэгдсэн» мессежид **одоогийн** зээлдэгчийн нэрийг хэвлэ.
- Буцаасан номыг дахин (өөр хүн ч) зээлж болно, нэг хүн хэд хэдэн ном зээлж
  болно. `LIST` нь нэмсэн дарааллаар — эрэмбэлэхгүй.
""",
            ),
        ),
    ],
)

PROJECT_MODULES = [C_PROJECTS, CPP_PROJECTS]
