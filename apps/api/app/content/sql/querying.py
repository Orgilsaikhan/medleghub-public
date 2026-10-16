"""Модул 2-5 — SELECT, WHERE шүүлт, суурь функц, бүлэглэл.

Анхан шатны асуулгууд. Бүх жишээ Модул 1-д үүсгэсэн `delguur` сан дээр
ажиллах бөгөөд өгөгдлийг зөвхөн уншина — юу ч өөрчлөхгүй.
"""

from app.content.types import LessonSpec, ModuleSpec
from app.models.enums import LessonLanguage

MY = LessonLanguage.MYSQL

SELECT_BASICS = ModuleSpec(
    title="Модул 2 — SELECT-ийн үндэс",
    description="Багана сонгох, нэр өгөх, эрэмбэлэх, хуудаслах.",
    lessons=[
        LessonSpec(
            title="SELECT ба FROM",
            slug="select-ba-from",
            description="Хүснэгтээс хэрэгтэй баганаа сонгож унших.",
            duration=420,
            language=MY,
            content="""\
`SELECT` бол SQL-ийн хамгийн их хэрэглэгддэг тушаал — хүснэгтээс өгөгдөл
**уншина**. Юу ч өөрчлөхгүй тул айхгүйгээр туршиж болно.

### Хамгийн энгийн хэлбэр

```sql
SELECT ner, une
FROM baraa;
```

- `SELECT` — **ямар багана** авах вэ
- `FROM` — **аль хүснэгтээс** авах вэ
- `;` — тушаалын төгсгөл

Үр дүн нь өөрөө хүснэгт хэлбэртэй — 12 мөр, 2 багана:

| ner | une |
|---|---|
| Ухаалаг утас | 1250000.00 |
| Зөөврийн компьютер | 3200000.00 |
| Чихэвч | 89000.00 |
| … | … |

### Эхлээд санг сонгох

Нэг сервер дээр олон өгөгдлийн сан байдаг. Аль нь дээр ажиллахаа заана:

```sql
USE delguur;
```

Эсвэл хүснэгтийн нэрийг сангийн нэртэй нь бүтнээр бичнэ: `delguur.baraa`.
Ингэвэл `USE`-гүйгээр ч аль сангийн хүснэгт болох нь тодорхой.

> Энэ сайт дээр ажиллуулалт бүр **ямар ч сан сонгоогүй** эхэлдэг. Тиймээс
> хичээлийн код бүр `USE delguur;`-ээр эхэлнэ.

### Бичих дүрэм

- Түлхүүр үг том жижиг үсэг ялгахгүй: `select` = `SELECT`. Заншлаар том
  үсгээр бичнэ.
- Мөр шилжүүлэх, зай тавих нь утгад нөлөөлөхгүй — уншихад амар хуваа.
- **Хүснэгтийн нэр** MySQL дээр Linux сервер дээр том жижиг үсэг ялгана
  (`Baraa` ≠ `baraa`), Windows дээр ялгахгүй. Тиймээс нэрийг үргэлж жижиг
  үсгээр бич.

### Тусгай нэрийг ишлэх

Нэр нь түлхүүр үгтэй давхцвал эсвэл зай агуулвал ишлэлд хийнэ:

```sql
SELECT `order` FROM `minii husnegt`;
```

MySQL нэрийг **backtick**-ээр (`` ` ``, гарын зүүн дээд буланд) хашдаг.
SQL стандартын `"order"` хэлбэр MySQL-д зөвхөн `ANSI_QUOTES` горим
асаалттай үед ажиллана. Хамгийн зөв нь ийм нэр огт хэрэглэхгүй байх.

### `SELECT *`

```sql
SELECT * FROM baraa;
```

Бүх баганыг авна. Өгөгдлийг **судлахад** тохиромжтой, гэхдээ програмын
кодод бүү хэрэглэ:

| Асуудал | Тайлбар |
|---|---|
| Илүү өгөгдөл | Хэрэггүй баганыг сүлжээгээр зөөнө |
| Эмзэг код | Хүснэгтэд багана нэмэгдэхэд үр дүн өөрчлөгдөнө |
| Index ашиглахгүй | Covering index (Модул 13) ажиллахаа болино |
| Ойлгомж муу | Ямар өгөгдөл хэрэгтэй нь кодоос харагдахгүй |

> **Дүрэм:** хэрэгтэй баганаа нэрээр нь жагсаа.

### FROM-гүй SELECT

```sql
SELECT 2 + 3;
```

MySQL-д `FROM`-гүй `SELECT` ажиллана — тооцоолуур шиг хэрэглэж болно.

### Тайлбар бичих

| Хэлбэр | Тайлбар |
|---|---|
| `-- мөр` | Стандарт. `--`-ийн дараа **зай** заавал |
| `# мөр` | Зөвхөн MySQL-д ажиллана |
| `/* олон мөр */` | Хэд хэдэн мөр хамарна |
""",
            initial_code="""\
-- Дэлгүүрийн сан руу шилжинэ
USE delguur;

-- 1. Бүх багана — зөвхөн өгөгдөлтэй танилцахад
SELECT * FROM baraa;

-- 2. Хэрэгтэй баганаа нэрээр нь жагсаана
SELECT ner, une, uldegdel
FROM baraa;

-- 3. Өөр хүснэгтээс
SELECT ovog, ner, hot
FROM hereglegch;

-- 4. Бүтэн нэрээр хандах
SELECT ner, alban_tushaal
FROM delguur.ajiltan;

-- 5. FROM-гүй SELECT — тооцоолуур
SELECT 2 + 3;

-- Даалгавар: zahialga хүснэгтээс zahialsan_ognoo, tuluv баганыг ав
""",
        ),
        LessonSpec(
            title="Alias ба тооцоолсон багана",
            slug="alias-ba-tootsoolson-bagana",
            description="AS-аар нэр өгөх, баганаар тооцоо хийх.",
            duration=420,
            language=MY,
            content="""\
### Тооцоолсон багана

`SELECT` дотор зөвхөн багана биш **илэрхийлэл** бичиж болно. Бараа бүрийн
агуулахад байгаа нийт үнэ:

```sql
SELECT ner, une * uldegdel
FROM baraa;
```

Үр дүнгийн баганын нэр нь `une * uldegdel` гэж гарна — муухай бөгөөд
програмаас хандахад төвөгтэй.

### AS — нэр өгөх

```sql
SELECT ner, une * uldegdel AS niit_une
FROM baraa;
```

| ner | niit_une |
|---|---|
| Ухаалаг утас | 18750000.00 |
| Зөөврийн компьютер | 19200000.00 |
| Чихэвч | 3560000.00 |
| … | … |

`AS` нь заавал биш: `une * uldegdel niit_une` ч ажиллана. Гэхдээ `AS`-тай
бичих нь илүү ойлгомжтой.

### Таслал мартах занга

```sql
SELECT ner une
FROM baraa;
```

Алдаа **гарахгүй**! `ner` баганыг `une` гэсэн нэртэйгээр харуулна. Үнэ
огт гарахгүй ч SQL үүнийг зөв гэж үзнэ. `AS` бичдэг зуршил энэ алдааг
харагдахуйц болгодог.

### Зай бүхий нэр

Зай бүхий нэрийг backtick-ээр хашина: `` AS `Нийт үнэ` ``. MySQL
`AS 'Нийт үнэ'` гэж дан ишлэлийг ч зөвшөөрдөг ч тэмдэгт мөртэй андуурагдана
— зайлсхий. Хамгийн сайн нь зайгүй нэр: `niit_une`.

### Арифметик оператор

| Оператор | Утга | Жишээ |
|---|---|---|
| `+` | Нэмэх | `une + 5000` |
| `-` | Хасах | `une - 10000` |
| `*` | Үржих | `une * 0.9` |
| `/` | Хуваах | `une / 1000` |
| `%` | Хуваалтын үлдэгдэл | `uldegdel % 10` |

> **Анхаар:** MySQL-д `/` бүхэл тоог хуваахад ч бутархай үр дүн өгнө:
> `7 / 2` = `3.5000`. Бүхэл хуваалт, тоймлолтыг Модул 4-т дэлгэрэнгүй
> үзнэ.

10%-ийн хямдралтай үнэ:

```sql
SELECT ner, une, une * 0.9 AS hyamdarsan_une
FROM baraa;
```

Илэрхийлэлд `NULL` орвол үр дүн нь бас `NULL` болно — Модул 3-т үзнэ.

### Хүснэгтийн alias

Хүснэгтэд ч товч нэр өгч болно:

```sql
SELECT b.ner, b.une
FROM baraa AS b;
```

Одоохондоо ач холбогдолгүй мэт боловч олон хүснэгт холбоход (Модул 9)
заавал хэрэгтэй болно.

### Alias-ыг хаана ашиглах вэ

Баганын alias нь үр дүнгийн баганын **нэр** болно. Дараагийн хичээлийн
`ORDER BY` (эрэмбэлэх) дотор түүнийг ашиглаж болно. Харин Модул 3-ын
`WHERE` (шүүлт) дотор ашиглаж болдоггүй — шалтгааныг тэнд үзнэ.
""",
            initial_code="""\
USE delguur;

-- 1. Тооцоолсон багана, нэр өгөөгүй
SELECT ner, une * uldegdel
FROM baraa;

-- 2. AS-аар ойлгомжтой нэр өгнө
SELECT ner, une * uldegdel AS niit_une
FROM baraa;

-- 3. Хямдралтай үнэ ба 10 ширхэгийн үнэ
SELECT ner,
       une,
       une * 0.9 AS hyamdarsan_une,
       une * 10 AS arvan_shirheg
FROM baraa;

-- 4. Таслал мартвал: ner багана une нэртэй гарна
SELECT ner une
FROM baraa;

-- 5. Хүснэгтийн alias
SELECT b.ner, b.une
FROM baraa AS b;

-- 6. Нэрийг backtick-д хийвэл зай бүхий нэр өгч болно
SELECT ner, une * uldegdel AS `Нийт үнэ`
FROM baraa;

-- Даалгавар: ajiltan хүснэгтээс ner болон жилийн цалин (tsalin * 12)
-- баганыг jiliin_tsalin нэртэйгээр ав
""",
        ),
        LessonSpec(
            title="ORDER BY ба DISTINCT",
            slug="order-by-ba-distinct",
            description="Үр дүнг эрэмбэлэх, давхардлыг арилгах.",
            duration=480,
            language=MY,
            content="""\
### Эрэмбэгүй бол дараалал баталгаагүй

`ORDER BY` бичээгүй бол мөрүүд **ямар ч** дарааллаар ирж болно. Өнөөдөр
`baraa_id`-аар гарч байгаа нь маргааш ч тэгнэ гэсэн баталгаа биш.

> **Дүрэм:** дараалал чухал бол заавал `ORDER BY` бич.

### ASC ба DESC

```sql
SELECT ner, une
FROM baraa
ORDER BY une DESC;
```

| ner | une |
|---|---|
| Зөөврийн компьютер | 3200000.00 |
| Ухаалаг утас | 1250000.00 |
| Тоос сорогч | 560000.00 |
| … | … |

- `ASC` — өсөхөөр (анхдагч, бичихгүй байж болно)
- `DESC` — буурахаар

### Олон баганаар

```sql
SELECT angilal_id, ner, une
FROM baraa
ORDER BY angilal_id ASC, une DESC;
```

Эхлээд ангиллаар, **ангилал адил** бол үнээр буурахаар. Чиглэл нь багана
бүрт тусдаа хамаарна.

Эрэмбэлэх утга тэнцүү мөрүүдийн дараалал бас баталгаагүй. Тогтвортой
дараалал хэрэгтэй бол давтагдашгүй багана нэм: `ORDER BY une DESC, baraa_id`.

### Alias ба илэрхийллээр

```sql
SELECT ner, une * uldegdel AS niit_une
FROM baraa
ORDER BY niit_une DESC;
```

`ORDER BY 2` гэж баганын дугаараар бичиж болох ч багана нэмэхэд чимээгүй
эвдэрдэг — зайлсхий.

### NULL хаана орох вэ

MySQL `NULL`-ийг **хамгийн бага** утга гэж үзнэ:

| `ASC` | `DESC` |
|---|---|
| `NULL` эхэнд | `NULL` төгсгөлд |

```sql
SELECT ner, hot FROM hereglegch ORDER BY hot;
```

Хот нь `NULL` байгаа Хулан **хамгийн эхэнд** гарна, дараа нь Дархан,
Улаанбаатар, Эрдэнэт.

MySQL-д PostgreSQL-ийн `NULLS LAST` бичлэг байхгүй. `NULL`-ийг төгсгөлд
гаргах арга:

```sql
SELECT ner, hot FROM hereglegch ORDER BY hot IS NULL, hot;
```

`hot IS NULL` нь «хот нь хоосон (`NULL`) юу?» гэсэн шалгалт: хоосон бол
`1`, үгүй бол `0` болно. Эхлээд энэ 0/1-ээр эрэмбэлэхэд хоттой мөрүүд (0)
түрүүлж, `NULL` мөр (1) төгсгөлд гарна. Дараа нь `hot`-оор эрэмбэлнэ.
`IS NULL`-ийг Модул 3-т нарийн үзнэ.

### Текстийн эрэмбэ

Текст **collation**-ы дүрмээр эрэмбэлэгдэнэ. Кирилл үсэг цагаан толгойн
дарааллаар гарна. Том жижиг үсгийг анхдагчаар ялгахгүй.

### DISTINCT — давхардлыг арилгах

```sql
SELECT DISTINCT hot
FROM hereglegch;
```

8 хэрэглэгчээс 4 мөр гарна: Улаанбаатар, Дархан, Эрдэнэт болон `NULL`.
`DISTINCT` нь бүх `NULL`-ийг **нэг** утга гэж үзнэ.

### DISTINCT нь бүх мөрөнд хамаарна

```sql
SELECT DISTINCT hereglegch_id, tuluv
FROM zahialga;
```

**Хослол** нь давтагдахгүй. 10 захиалгаас 9 мөр гарна — 1-р хэрэглэгчийн
хоёр «Хүргэгдсэн» захиалга нэг мөр болно.

`DISTINCT` бол функц биш. `SELECT DISTINCT(hot), ner` гэж бичсэн ч хаалт
нь юу ч хийхгүй — хоёр баганын хослолыг шүүнэ.

### DISTINCT ба ORDER BY

`DISTINCT`-тэй үед `ORDER BY` дахь багана `SELECT` жагсаалтад заавал
байх ёстой. Үгүй бол MySQL алдаа (3065) өгнө:

```sql
-- Алдаа: ner нь SELECT жагсаалтад байхгүй
SELECT DISTINCT hot FROM hereglegch ORDER BY ner;
```
""",
            initial_code="""\
USE delguur;

-- 1. Хамгийн үнэтэйгээс нь эхлэн
SELECT ner, une
FROM baraa
ORDER BY une DESC;

-- 2. Ангиллаар, дотроо үнээр буурахаар
SELECT angilal_id, ner, une
FROM baraa
ORDER BY angilal_id ASC, une DESC;

-- 3. Alias-аар эрэмбэлэх, тэнцвэл id-аар
SELECT baraa_id, ner, une * uldegdel AS niit_une
FROM baraa
ORDER BY niit_une DESC, baraa_id;

-- 4. NULL эхэнд гарна
SELECT ner, hot
FROM hereglegch
ORDER BY hot;

-- 5. NULL-ийг төгсгөлд: hot IS NULL нь хоосон бол 1, үгүй бол 0
SELECT ner, hot
FROM hereglegch
ORDER BY hot IS NULL, hot;

-- 6. Давтагдахгүй хотууд
SELECT DISTINCT hot
FROM hereglegch
ORDER BY hot;

-- 7. Давтагдахгүй хослол
SELECT DISTINCT hereglegch_id, tuluv
FROM zahialga
ORDER BY hereglegch_id;

-- Даалгавар: ajiltan хүснэгтийг цалингаар буурахаар эрэмбэл
""",
        ),
        LessonSpec(
            title="LIMIT ба OFFSET",
            slug="limit-top-offset-fetch",
            description="Эхний хэдэн мөрийг авах, хуудаслах.",
            duration=480,
            language=MY,
            content="""\
Хүснэгтэд мянга мянган мөр байхад бүгдийг нь авах нь ховор. «Хамгийн
үнэтэй 3 бараа», «хайлтын үр дүнгийн 2-р хуудас» гэх мэт хэсгийг л авна.
MySQL-д үүнийг `LIMIT` хийнэ.

### LIMIT — эхний n мөр

```sql
SELECT ner, une
FROM baraa
ORDER BY une DESC
LIMIT 3;
```

Хамгийн үнэтэй 3 бараа: Зөөврийн компьютер, Ухаалаг утас, Тоос сорогч.

- `LIMIT` асуулгын **хамгийн төгсгөлд**, `ORDER BY`-ийн дараа бичигдэнэ.
- Эхлээд `ORDER BY` эрэмбэлж, дараа нь `LIMIT` эхний 3-ыг таслана.

### OFFSET — алгасах

```sql
SELECT baraa_id, ner, une
FROM baraa
ORDER BY baraa_id
LIMIT 5 OFFSET 5;
```

Эхний 5-ыг алгасаад дараагийн 5-ыг авна — `baraa_id` 6–10.

MySQL-д товч хэлбэр бас бий: `LIMIT 5, 5` — **эхлээд алгасах тоо**,
дараа нь авах тоо. Дараалал нь `LIMIT 5 OFFSET 5`-аас эсрэг тул андуурахад
амар. Уншихад ойлгомжтой `OFFSET` хэлбэрийг хэрэглэ.

### Хуудасны томьёо

`OFFSET = (хуудас - 1) * хэмжээ`

| Хуудас (5 мөрөөр) | Бичлэг |
|---|---|
| 1 | `LIMIT 5 OFFSET 0` (эсвэл зүгээр `LIMIT 5`) |
| 2 | `LIMIT 5 OFFSET 5` |
| 3 | `LIMIT 5 OFFSET 10` |

`LIMIT`, `OFFSET`-д зөвхөн **тогтмол тоо** бичнэ: `LIMIT 5 OFFSET (3 - 1) * 5`
гэвэл синтакс алдаа. Бодит програмд хуудасны дугаар хэрэглэгчээс ирэх тул
тооцооллыг програмын кодод хийж, тоог нь параметрээр дамжуулна
(параметртэй асуулгыг Модул 18-д үзнэ).

### Тэнцсэн мөрүүд

Хамгийн бага үлдэгдэлтэй бараа аль вэ?

```sql
SELECT ner, uldegdel
FROM baraa
ORDER BY uldegdel
LIMIT 1;
```

Гутал, Сүүтэй цай хоёулаа үлдэгдэл 0 — гэвч `LIMIT 1` нь **зөвхөн нэгийг**
өгнө, аль нь болох нь ч тодорхойгүй. `LIMIT` тэнцсэн мөрүүдийг тоохгүй
таслана. Тэнцсэн бүгдийг авах аргыг Модул 10-ын дэд асуулга, Модул 15-ын
`RANK` функцээр үзнэ.

### Хоёр түгээмэл алдаа

**1. ORDER BY-гүй LIMIT.** MySQL зөвшөөрнө, гэхдээ «эхний 5» гэдэг нь
санамсаргүй 5 мөр болно.

**2. Тогтворгүй эрэмбэ.** `ORDER BY une` дээр хуудаслахад ижил үнэтэй
мөрүүд хуудас хооронд давхардаж эсвэл алга болж болно. Давтагдашгүй
багана нэм: `ORDER BY une, baraa_id`.

> **Гүйцэтгэл:** `OFFSET 100000` нь 100 000 мөрийг уншаад хаядаг. Том
> хүснэгтэд «сүүлийн харсан id-аас хойшхийг ав» гэсэн keyset хуудаслалт
> хурдан — үүнийг Модул 3-ын `WHERE` шүүлтээр хийнэ.

> `LIMIT` нь SQL стандарт биш, MySQL (мөн PostgreSQL, SQLite)-ийн бичлэг.
> Бусад DBMS мөр хязгаарлахыг өөрөөр бичдэг.
""",
            initial_code="""\
USE delguur;

-- 1. Хамгийн үнэтэй 3 бараа
SELECT ner, une
FROM baraa
ORDER BY une DESC
LIMIT 3;

-- 2. Хамгийн бага үлдэгдэлтэй 1 бараа: тэнцсэн хоёроос зөвхөн нэг нь гарна
SELECT ner, uldegdel
FROM baraa
ORDER BY uldegdel, baraa_id
LIMIT 1;

-- 3. Илүү мөр авбал тэнцсэн нь харагдана: эхний хоёр нь үлдэгдэл 0
SELECT ner, uldegdel
FROM baraa
ORDER BY uldegdel, baraa_id
LIMIT 3;

-- 4. Эхний 5-ыг алгасаад дараагийн 5
SELECT baraa_id, ner, une
FROM baraa
ORDER BY baraa_id
LIMIT 5 OFFSET 5;

-- 5. Товч хэлбэр: LIMIT алгасах, авах — дээрхтэй ижил үр дүн
SELECT baraa_id, ner, une
FROM baraa
ORDER BY baraa_id
LIMIT 5, 5;

-- 6. Хуудасны томьёо: 3-р хуудас, 5 мөрөөр -> OFFSET (3 - 1) * 5 = 10
SELECT baraa_id, ner
FROM baraa
ORDER BY baraa_id
LIMIT 5 OFFSET 10;

-- 7. Тогтвортой эрэмбэ: үнэ тэнцвэл id-аар
SELECT baraa_id, ner, une
FROM baraa
ORDER BY une, baraa_id
LIMIT 4;

-- Даалгавар: хамгийн өндөр цалинтай 2 ажилтныг ajiltan хүснэгтээс ав
""",
        ),
    ],
)

WHERE_FILTERING = ModuleSpec(
    title="Модул 3 — WHERE шүүлт",
    description="Нөхцөлөөр мөр шүүх, NULL-тай зөв ажиллах.",
    lessons=[
        LessonSpec(
            title="Харьцуулах ба логик оператор",
            slug="haritsuulah-ba-logik-operator",
            description="=, <>, <, > болон AND, OR, NOT-ийн эрэмбэ.",
            duration=480,
            language=MY,
            content="""\
### WHERE

`WHERE` нь нөхцөл **үнэн** болсон мөрүүдийг л үлдээнэ:

```sql
SELECT ner, une
FROM baraa
WHERE une > 1000000;
```

Үр дүн: Ухаалаг утас, Зөөврийн компьютер.

### Харьцуулах оператор

| Оператор | Утга |
|---|---|
| `=` | Тэнцүү |
| `<>` эсвэл `!=` | Тэнцүү биш |
| `<`, `>` | Бага, их |
| `<=`, `>=` | Бага буюу тэнцүү, их буюу тэнцүү |

`!=` ба `<>` хоёулаа ажиллана, `<>` нь стандарт.

SQL-д тэнцүүг шалгахдаа **нэг** `=` бичнэ — програмчлалын хэлний `==` биш.

### Текст ба огноо

Тэмдэгт мөр, огноог **дан ишлэлд** бичнэ:

```sql
SELECT ovog, ner FROM hereglegch WHERE hot = 'Дархан';

SELECT ovog, ner FROM hereglegch WHERE burtgesen_ognoo >= '2024-03-01';
```

Эхнийх нь Тэмүүлэн, Энх хоёрыг, хоёр дахь нь 4 хэрэглэгчийг өгнө.

| Бичлэг | MySQL-д утга |
|---|---|
| `'текст'` | Тэмдэгт мөр |
| `"текст"` | Тэмдэгт мөр (анхдагчаар) — гэхдээ стандарт SQL-д **нэр** |
| `` `текст` `` | Хүснэгт, баганын **нэр** |

Кирилл текстийг ямар ч угтваргүй `'Дархан'` гэж бичнэ — сан ба холболт
`utf8mb4` бол (Модул 1) үсэг бүр зөв хадгалагдана.

> **Дүрэм:** тэмдэгт мөрийг үргэлж дан ишлэлд бич.

### Далд хөрвүүлэлтийн занга

Төрөл таарахгүй үед MySQL алдаа өгөхийн оронд утгыг **өөрөө хөрвүүлдэг**:

```sql
SELECT 'abc' = 0;   -- 1 (үнэн!), анхааруулгатай
SELECT '10' = 10;   -- 1
```

MySQL нь тоо биш текстийг `0` болгож харьцуулдаг. Бусад зарим DBMS ийм
үед алдаа өгдөг — MySQL-ийн энэ «эелдэг» зан алдааг нууж болно.

`utas` нь текст багана тул тоогоор биш текстээр харьцуул:
`WHERE utas = '99112233'`.

### Alias WHERE дотор ажиллахгүй

Модул 2-т `AS`-аар өгсөн баганын нэрийг `ORDER BY`-д ашигласан. `WHERE`-д
бол болохгүй:

```sql
-- Алдаа: niit_une нь WHERE ажиллах үед хараахан байхгүй
SELECT ner, une * uldegdel AS niit_une
FROM baraa
WHERE niit_une > 5000000;

-- Зөв: илэрхийллийг давтан бичнэ
SELECT ner, une * uldegdel AS niit_une
FROM baraa
WHERE une * uldegdel > 5000000;
```

Яагаад гэвэл `WHERE` нь `SELECT`-ээс **өмнө** биелдэг: эхлээд мөрүүдийг
шүүж, дараа нь л баганыг тооцоолж нэр өгнө. `ORDER BY` хамгийн сүүлд
биелдэг тул alias-ыг мэддэг. Энэ дарааллыг Модул 5-д бүрэн үзнэ.

### AND, OR, NOT

| Оператор | Үр дүн үнэн байх нөхцөл |
|---|---|
| `A AND B` | Хоёулаа үнэн |
| `A OR B` | Ядаж нэг нь үнэн |
| `NOT A` | `A` худал |

```sql
SELECT ner, une, uldegdel
FROM baraa
WHERE une < 100000 AND uldegdel > 50;
```

### Эрэмбэ: NOT → AND → OR

Энэ нь хамгийн түгээмэл логик алдааны эх үүсвэр. Даалгавар: «1 эсвэл
4-р ангиллын, 100 000-аас хямд бараа».

```sql
-- БУРУУ
SELECT ner, angilal_id, une
FROM baraa
WHERE angilal_id = 1 OR angilal_id = 4 AND une < 100000;
```

`AND` түрүүлж биелэх тул энэ нь `angilal_id = 1 OR (angilal_id = 4 AND
une < 100000)` гэсэн утгатай. 1-р ангиллын **бүх** бараа гарна: Ухаалаг
утас, Зөөврийн компьютер, Чихэвч, Цайны аяга — 4 мөр.

```sql
-- ЗӨВ
SELECT ner, angilal_id, une
FROM baraa
WHERE (angilal_id = 1 OR angilal_id = 4) AND une < 100000;
```

Одоо зөвхөн Чихэвч, Цайны аяга.

> **Дүрэм:** `AND` ба `OR` холилдвол заавал хаалт тавь.

### NOT

```sql
SELECT ner FROM baraa WHERE NOT (angilal_id = 1);
```

Энэ нь `angilal_id <> 1`-тэй ижил. `NOT`-ийг ихэвчлэн `IN`, `LIKE`,
`BETWEEN`-тэй хамт хэрэглэнэ.

MySQL нь `AND`-ийн оронд `&&`, `OR`-ийн оронд `||` гэж бичихийг
зөвшөөрдөг ч стандарт биш бөгөөд `&&` нь хуучирсан. Үгээр бич.
""",
            initial_code="""\
USE delguur;

-- 1. Нэг сая төгрөгөөс үнэтэй бараа
SELECT ner, une
FROM baraa
WHERE une > 1000000;

-- 2. Үлдэгдэлгүй бараа
SELECT ner, uldegdel
FROM baraa
WHERE uldegdel = 0;

-- 3. Текст ба огноогоор
SELECT ovog, ner, hot
FROM hereglegch
WHERE hot = 'Дархан';

SELECT ovog, ner, burtgesen_ognoo
FROM hereglegch
WHERE burtgesen_ognoo >= '2024-03-01';

-- 4. MySQL-ийн далд хөрвүүлэлт: хоёулаа 1 буцаана
SELECT 'abc' = 0 AS gaihaltai, '10' = 10 AS bas_unen;

-- 5. Хаалтгүй — буруу үр дүн (4 мөр)
SELECT ner, angilal_id, une
FROM baraa
WHERE angilal_id = 1 OR angilal_id = 4 AND une < 100000;

-- 6. Хаалттай — зөв үр дүн (2 мөр)
SELECT ner, angilal_id, une
FROM baraa
WHERE (angilal_id = 1 OR angilal_id = 4) AND une < 100000;

-- 7. NOT
SELECT ner, angilal_id
FROM baraa
WHERE NOT (angilal_id = 1);

-- 8. Alias WHERE дотор ажиллахгүй тул илэрхийллийг давтана
SELECT ner, une * uldegdel AS niit_une
FROM baraa
WHERE une * uldegdel > 5000000;

-- Даалгавар: цалин нь 2 500 000-аас их, 2021 оноос өмнө ажилд орсон
-- ажилтнуудыг ol (ajild_orson < 2021-01-01)
""",
        ),
        LessonSpec(
            title="IN, BETWEEN ба LIKE",
            slug="in-between-like",
            description="Жагсаалт, завсар, загвараар шүүх ба огнооны занга.",
            duration=600,
            language=MY,
            content="""\
Энэ гурван оператор урт `OR`, `AND` нөхцөлийг товч, уншигдахуйц болгоно.

### IN — жагсаалтын аль нэг

```sql
SELECT ner, angilal_id
FROM baraa
WHERE angilal_id IN (2, 3);
```

Ноосон цамц, Гутал, Монгол түүх, SQL сурах бичиг. Энэ нь
`angilal_id = 2 OR angilal_id = 3`-тай яг ижил, гэхдээ товч.

```sql
SELECT ovog, ner, hot
FROM hereglegch
WHERE hot IN ('Дархан', 'Эрдэнэт');
```

`NOT IN` нь эсрэгээр ажиллана — гэхдээ жагсаалтад `NULL` орвол аюултай.
Дараагийн хичээлд үзнэ.

### BETWEEN — хоёр хил **хамаарна**

```sql
SELECT ner, une
FROM baraa
WHERE une BETWEEN 35000 AND 145000;
```

Чихэвч, Ноосон цамц (145 000), Монгол түүх (35 000), SQL сурах бичиг.
Хилийн утгууд **орно**: `une >= 35000 AND une <= 145000`.

- Бага утгыг эхэнд бич. `BETWEEN 145000 AND 35000` нь юу ч олохгүй.
- `NOT BETWEEN` — завсраас гадна.

### Огнооны занга

`zahialsan_ognoo` нь **цагтай** (`DATETIME`) багана. 2-р сарын 1-ээс
14-ний хоорондох захиалга:

```sql
SELECT zahialga_id, zahialsan_ognoo
FROM zahialga
WHERE zahialsan_ognoo BETWEEN '2024-02-01' AND '2024-02-14';
```

Зөвхөн 1-р захиалга гарна! 2-р захиалга `2024-02-14 18:40`-д хийгдсэн.
`'2024-02-14'` нь `2024-02-14 00:00:00` гэсэн утгатай тул тэр өдрийн
шөнө дундаас хойшхи бүх зүйл хасагдана.

```sql
-- ЗӨВ: хагас нээлттэй завсар
SELECT zahialga_id, zahialsan_ognoo
FROM zahialga
WHERE zahialsan_ognoo >= '2024-02-01'
  AND zahialsan_ognoo <  '2024-02-15';
```

Одоо 1, 2-р захиалга хоёулаа.

> **Дүрэм:** цагтай баганад `BETWEEN` бүү хэрэглэ — `>=` ба дараагийн
> өдрийн `<`. `'23:59:59'` гэж бичих нь секундын бутархайг алддаг.

Огноог үргэлж `'YYYY-MM-DD'` (эсвэл `'YYYY-MM-DD hh:mm:ss'`) хэлбэрээр
бич — MySQL үүнийг найдвартай таньдаг.

### LIKE — загвараар хайх

| Тэмдэг | Утга |
|---|---|
| `%` | Дурын тооны тэмдэгт (0 ч байж болно) |
| `_` | Яг **нэг** тэмдэгт |

```sql
-- С үсгээр эхэлсэн нэр — Сараа
SELECT ner FROM hereglegch WHERE ner LIKE 'С%';

-- ын-ээр төгссөн овог — Батын, Ганбаатарын
SELECT ovog FROM hereglegch WHERE ovog LIKE '%ын';

-- Яг 4 үсэгтэй нэр — Болд, Анар, Мөнх
SELECT ner FROM hereglegch WHERE ner LIKE '____';

-- Нэрэнд утас гэж орсон бараа
SELECT ner FROM baraa WHERE ner LIKE '%утас%';
```

`_` нь байт биш **тэмдэгт** тоолно — кирилл үсэг ч нэг `_`.

### Том жижиг үсэг

MySQL 8-ийн анхдагч collation `utf8mb4_0900_ai_ci` нь **case-insensitive**
(`ci`): `LIKE 'с%'` гэж жижиг үсгээр хайсан ч Сараа олдоно.

Том жижгийг ялгах шаардлагатай бол collation-ыг тухайн илэрхийлэлд заана:

```sql
WHERE ner LIKE 'с%' COLLATE utf8mb4_0900_as_cs
```

`as_cs` — accent-sensitive, case-sensitive. Одоо жижиг `с`-ээр эхэлсэн
нэр л олдоно.

### `%` эсвэл `_`-ийг өөрийг нь хайх

```sql
-- ESCAPE: ! тэмдгийн дараах _ нь жирийн тэмдэгт
WHERE email LIKE '%!_%' ESCAPE '!'

-- MySQL-ийн анхдагч escape тэмдэг: \\
WHERE email LIKE '%\\_%'
```

### REGEXP — илүү хүчтэй загвар

`LIKE`-д «Б эсвэл С үсгээр эхэлсэн» гэж бичих арга байхгүй. MySQL-ийн
`REGEXP` (энгийн илэрхийлэл, regular expression) үүнийг хийнэ:

```sql
-- Б эсвэл С үсгээр эхэлсэн — Болд, Сараа
SELECT ner FROM hereglegch WHERE ner REGEXP '^[БС]';
```

| Загвар | Утга |
|---|---|
| `^` | Текстийн эхлэл |
| `$` | Текстийн төгсгөл |
| `[БС]` | Б эсвэл С |
| `[^БС]` | Б, С-ээс бусад |

> **Гүйцэтгэл:** `LIKE '%утас'` шиг `%`-аар **эхэлсэн** загвар, мөн
> `REGEXP` нь index ашиглаж чадахгүй тул бүх мөрийг шалгана.
""",
            initial_code="""\
USE delguur;

-- 1. IN — жагсаалтын аль нэг ангилал
SELECT ner, angilal_id
FROM baraa
WHERE angilal_id IN (2, 3);

-- 2. IN — текстийн жагсаалт
SELECT ovog, ner, hot
FROM hereglegch
WHERE hot IN ('Дархан', 'Эрдэнэт');

-- 3. BETWEEN хилийн утгуудыг оруулна
SELECT ner, une
FROM baraa
WHERE une BETWEEN 35000 AND 145000;

-- 4. Огнооны занга: 2-р захиалга алга болно
SELECT zahialga_id, zahialsan_ognoo
FROM zahialga
WHERE zahialsan_ognoo BETWEEN '2024-02-01' AND '2024-02-14';

-- 5. Зөв арга: дараагийн өдрөөс бага
SELECT zahialga_id, zahialsan_ognoo
FROM zahialga
WHERE zahialsan_ognoo >= '2024-02-01'
  AND zahialsan_ognoo < '2024-02-15';

-- 6. LIKE загварууд
SELECT ner FROM hereglegch WHERE ner LIKE 'С%';
SELECT ovog FROM hereglegch WHERE ovog LIKE '%ын';
SELECT ner FROM hereglegch WHERE ner LIKE '____';
SELECT ner FROM baraa WHERE ner LIKE '%утас%';

-- 7. Жижиг үсгээр хайсан ч олдоно (case-insensitive)
SELECT ner FROM hereglegch WHERE ner LIKE 'с%';

-- 8. Том жижгийг ялгавал олдохгүй
SELECT ner FROM hereglegch WHERE ner LIKE 'с%' COLLATE utf8mb4_0900_as_cs;

-- 9. REGEXP: Б эсвэл С үсгээр эхэлсэн
SELECT ner FROM hereglegch WHERE ner REGEXP '^[БС]';

-- Даалгавар: 2024 оны 4-р сард хийгдсэн захиалгуудыг зөв аргаар ол
""",
        ),
        LessonSpec(
            title="NULL ба гурван утгат логик",
            slug="null-ba-gurvan-utgat-logik",
            description="IS NULL, = NULL яагаад ажилладаггүй, NOT IN-ийн занга.",
            duration=540,
            language=MY,
            content="""\
### NULL гэж юу вэ

`NULL` нь «утга **мэдэгдэхгүй** эсвэл байхгүй» гэсэн тэмдэглэгээ. Энэ нь:

- `0` биш
- хоосон текст `''` биш
- «худал» биш

Сараа, Хулан хоёрын утасны дугаар мэдэгдэхгүй тул `utas` нь `NULL`.

### `= NULL` хэзээ ч ажиллахгүй

```sql
SELECT ovog, ner FROM hereglegch WHERE utas = NULL;
```

**Нэг ч мөр** гарахгүй — алдаа ч өгөхгүй. Учир нь «мэдэгдэхгүй утга
мэдэгдэхгүй утгатай тэнцүү юу?» гэдгийн хариу нь мөн **мэдэгдэхгүй**.

```sql
SELECT NULL = NULL;   -- MySQL: NULL
SELECT NULL <> 5;     -- MySQL: NULL
SELECT NULL + 100;    -- NULL
```

### IS NULL ба IS NOT NULL

```sql
SELECT ovog, ner FROM hereglegch WHERE utas IS NULL;      -- Сараа, Хулан
SELECT ovog, ner FROM hereglegch WHERE utas IS NOT NULL;  -- бусад 6
```

`NULL`-ийг шалгах стандарт, **найдвартай** арга.

### Гурван утгат логик

SQL-ийн нөхцөл `TRUE`, `FALSE`-оос гадна `UNKNOWN` байж болно.
`WHERE` нь зөвхөн `TRUE` мөрийг үлдээнэ — `UNKNOWN` ч хасагдана.

| AND | TRUE | FALSE | UNKNOWN |
|---|---|---|---|
| **TRUE** | TRUE | FALSE | UNKNOWN |
| **FALSE** | FALSE | FALSE | FALSE |
| **UNKNOWN** | UNKNOWN | FALSE | UNKNOWN |

| OR | TRUE | FALSE | UNKNOWN |
|---|---|---|---|
| **TRUE** | TRUE | TRUE | TRUE |
| **FALSE** | TRUE | FALSE | UNKNOWN |
| **UNKNOWN** | TRUE | UNKNOWN | UNKNOWN |

`NOT UNKNOWN` нь `UNKNOWN` хэвээр.

### «Тэнцүү биш» ч NULL-ийг алдана

Улаанбаатараас **бусад** хотын хэрэглэгч:

```sql
SELECT ner, hot FROM hereglegch WHERE hot <> 'Улаанбаатар';
```

Тэмүүлэн, Номин, Энх — гурав. Хот нь `NULL` Хулан **ороогүй**:
`NULL <> 'Улаанбаатар'` нь `UNKNOWN`. Хулан-г оруулах бол илт бич:

```sql
SELECT ner, hot FROM hereglegch
WHERE hot <> 'Улаанбаатар' OR hot IS NULL;
```

### NOT IN-ийн занга

`ajiltan` хүснэгтэд захирал Батбаярын `menejer_id` нь `NULL`.

```sql
SELECT ner FROM ajiltan WHERE menejer_id NOT IN (2, 3);
```

Оюунаа, Ганзориг хоёр л гарна. Батбаяр алга — `NULL`-ийг 2-той харьцуулах
боломжгүй.

Жагсаалт дотор `NULL` орвол бүр ч муу:

```sql
SELECT ner FROM ajiltan WHERE ajiltan_id NOT IN (4, 5, NULL);
```

**Нэг ч мөр** гарахгүй. Задалбал:

```text
ajiltan_id <> 4 AND ajiltan_id <> 5 AND ajiltan_id <> NULL
                                        └── үргэлж UNKNOWN
```

`AND` дотор нэг `UNKNOWN` байхад үр дүн хэзээ ч `TRUE` болохгүй.
`IN (4, NULL)` харин 4-ийг олно — `OR` дотор нэг `TRUE` хангалттай.

> **Анхаар:** энэ асуудал ихэвчлэн `NOT IN (SELECT ...)` хэлбэрээр
> гардаг — дэд асуулга ганц `NULL` буцаахад бүх үр дүн алга болно.
> Модул 10-т `NOT EXISTS`-ээр засна.

### NULL-тэй тэнцүү гэж харьцуулах

MySQL-ийн `<=>` оператор нь **NULL-safe тэнцүү**: хоёулаа `NULL` бол
`1`, нэг нь л `NULL` бол `0` — хэзээ ч `NULL` буцаахгүй.

| Илэрхийлэл | Үр дүн |
|---|---|
| `NULL <=> NULL` | 1 |
| `5 <=> NULL` | 0 |
| `NOT (a <=> b)` | NULL-safe «тэнцүү биш» |

```sql
-- Батбаярыг олно
SELECT ner FROM ajiltan WHERE menejer_id <=> NULL;
```

### Бусад анхаарах зүйл

- `''` (хоосон текст) ба `NULL` өөр утга: `'' IS NULL` нь 0.
- MySQL-д нөхцөл нь `1`/`0`/`NULL` тоо тул `SELECT NULL = NULL` гэж шууд
  харж болно.
- `NULL`-ийг өөр утгаар орлуулах `COALESCE`-ийг Модул 11-д үзнэ.
""",
            initial_code="""\
USE delguur;

-- 1. = NULL — нэг ч мөр гарахгүй
SELECT ovog, ner, utas
FROM hereglegch
WHERE utas = NULL;

-- 2. IS NULL — Сараа, Хулан
SELECT ovog, ner, utas
FROM hereglegch
WHERE utas IS NULL;

-- 3. NULL-тэй харьцуулалт, тооцоо бүгд NULL
SELECT NULL = NULL AS tentsuu, NULL <> 5 AS tentsuu_bish, NULL + 100 AS niilber;

-- 4. Тэнцүү биш нь NULL мөрийг алдана (3 мөр)
SELECT ner, hot
FROM hereglegch
WHERE hot <> 'Улаанбаатар';

-- 5. NULL-ийг илт оруулна (4 мөр)
SELECT ner, hot
FROM hereglegch
WHERE hot <> 'Улаанбаатар' OR hot IS NULL;

-- 6. NOT IN — захирал Батбаяр алга
SELECT ner, menejer_id
FROM ajiltan
WHERE menejer_id NOT IN (2, 3);

-- 7. Жагсаалтад NULL байвал нэг ч мөр гарахгүй
SELECT ner
FROM ajiltan
WHERE ajiltan_id NOT IN (4, 5, NULL);

-- 8. IN дотор NULL байх нь хор хөнөөлгүй
SELECT ner
FROM ajiltan
WHERE ajiltan_id IN (4, NULL);

-- 9. NULL-safe тэнцүү
SELECT ner
FROM ajiltan
WHERE menejer_id <=> NULL;

-- Даалгавар: хот эсвэл утасны аль нэг нь бүртгэлгүй хэрэглэгчдийг ол
""",
        ),
    ],
)

BUILTIN_FUNCTIONS = ModuleSpec(
    title="Модул 4 — Суурь функцууд",
    description="Текст, тоо, огнооны функц ба төрөл хөрвүүлэх.",
    lessons=[
        LessonSpec(
            title="Текстийн функцууд",
            slug="tekstiin-funkts",
            description="CONCAT, урт, SUBSTRING, REPLACE, TRIM ба кирилл текстийн онцлог.",
            duration=600,
            language=MY,
            content="""\
### Товч жагсаалт

| Үйлдэл | Функц |
|---|---|
| Нийлүүлэх | `CONCAT`, `CONCAT_WS` |
| Тэмдэгтийн тоо | `CHAR_LENGTH` |
| Байтын тоо | `LENGTH` |
| Байрлал хайх | `LOCATE(хайх, мөр)` |
| Хэсэг авах | `SUBSTRING`, `LEFT`, `RIGHT`, `SUBSTRING_INDEX` |
| Солих | `REPLACE` |
| Зай арилгах | `TRIM`, `LTRIM`, `RTRIM` |
| Том, жижиг үсэг | `UPPER`, `LOWER` |

### CONCAT — нийлүүлэх

```sql
SELECT CONCAT(ovog, ' ', ner) AS buten_ner
FROM hereglegch;
```

Батын Болд, Доржийн Сараа, …

**NULL-тай үед анхаар:**

```sql
SELECT CONCAT(ner, ': ', utas) FROM hereglegch;
```

Сараагийн `utas` нь `NULL` тул үр дүн нь бүхэлдээ `NULL` — нэг `NULL`
бүгдийг `NULL` болгоно.

`CONCAT_WS(тусгаарлагч, ...)` (With Separator) нь `NULL`-ийг **алгасна**:

```sql
SELECT CONCAT_WS(', ', hot, utas) FROM hereglegch;
```

Сараа → `Улаанбаатар`, Хулан → хоосон текст.

### `+` текст нийлүүлдэггүй

MySQL-д `+` нь **зөвхөн тоо** нэмнэ. Текстийг тоо болгох гэж оролдоно:

```sql
SELECT '10' + '5';         -- 15.0
SELECT 'Болд' + 'Сараа';   -- 0.0, анхааруулгатай
```

Алдаа ч гарахгүй, буруу үр дүн л гарна. Текстийг үргэлж `CONCAT`-аар
нийлүүл.

### Урт: тэмдэгт үү, байт уу

`utf8mb4`-д латин үсэг 1 байт, **кирилл үсэг 2 байт**:

```sql
SELECT CHAR_LENGTH('Ухаалаг утас');  -- 12 тэмдэгт
SELECT LENGTH('Ухаалаг утас');       -- 23 байт
```

`LENGTH`-ээр «нэр 10 тэмдэгтээс урт уу» гэж шалгавал кирилл нэр хоёр
дахин урт мэт харагдана. Тэмдэгт тоолоход үргэлж `CHAR_LENGTH`.
Төгсгөлийн зай ч тоологдоно: `CHAR_LENGTH('abc   ')` нь `6`.

### UPPER, LOWER

```sql
SELECT UPPER(ner), LOWER(email) FROM hereglegch;
```

Кирилл үсэгт ч зөв ажиллана: `Болд` → `БОЛД`.

### SUBSTRING, LEFT, RIGHT

Байрлал **1-ээс** эхэлнэ.

```sql
SELECT SUBSTRING('Ухаалаг утас', 9, 4);  -- утас
SELECT LEFT(ovog, 1), RIGHT(utas, 4) FROM hereglegch;
```

| Бичлэг | Үр дүн |
|---|---|
| `SUBSTRING(s, 9, 4)` | 9-р тэмдэгтээс 4 тэмдэгт |
| `SUBSTRING(s, 9)` | 9-р тэмдэгтээс төгсгөл хүртэл |
| `SUBSTRING(s, -4)` | Сүүлийн 4 тэмдэгт |

Имэйлийн `@`-ээс өмнөх хэсэг — хоёр арга:

```sql
SELECT SUBSTRING(email, 1, LOCATE('@', email) - 1) FROM hereglegch;
SELECT SUBSTRING_INDEX(email, '@', 1) FROM hereglegch;
```

`LOCATE('@', email)` нь `@`-ийн байрлалыг (олдохгүй бол 0) өгнө.
`SUBSTRING_INDEX(s, тэмдэгт, n)` нь тэмдэгтийн n дахь тохиолдлоос өмнөх
хэсгийг өгнө — MySQL-ийн тохиромжтой функц.

### REPLACE

```sql
SELECT REPLACE(email, '@example.mn', '@mail.mn') FROM hereglegch;
```

`REPLACE` нь том жижиг үсгийг **үргэлж ялгана** — collation
case-insensitive байсан ч: `REPLACE('Болд болд', 'болд', 'X')` →
`Болд X`.

### TRIM

```sql
SELECT TRIM('   Болд   ');              -- Болд
-- Зайнаас өөр тэмдэгт арилгах
SELECT TRIM(BOTH '.' FROM '..Болд..');   -- Болд
SELECT TRIM(LEADING '0' FROM '00123');   -- 123
```

`LTRIM`, `RTRIM` нь зөвхөн зүүн, баруун талын зайг арилгана.

> **Гүйцэтгэл:** `WHERE UPPER(ner) = 'БОЛД'` шиг баганыг функцэд хийвэл
> index ашиглагдахгүй. Collation аль хэдийн case-insensitive тул
> `WHERE ner = 'Болд'` хангалттай.
""",
            initial_code="""\
USE delguur;

-- 1. Овог нэрийг нийлүүлэх
SELECT CONCAT(ovog, ' ', ner) AS buten_ner
FROM hereglegch;

-- 2. CONCAT: utas NULL бол бүхэлдээ NULL
SELECT ner, CONCAT(ner, ': ', utas) AS kontakt
FROM hereglegch;

-- 3. CONCAT_WS нь NULL-ийг алгасна
SELECT ner, CONCAT_WS(', ', hot, utas) AS medeelel
FROM hereglegch;

-- 4. Тэмдэгт ба байт: кирилл үсэг 2 байт
SELECT ner,
       CHAR_LENGTH(ner) AS temdegt,
       LENGTH(ner) AS bait
FROM baraa;

-- 5. Том үсэг, товчилсон нэр
SELECT UPPER(ner) AS tom,
       CONCAT(LEFT(ovog, 1), '. ', ner) AS tovch_ner
FROM hereglegch;

-- 6. Имэйлийн нэвтрэх нэр
SELECT email,
       SUBSTRING(email, 1, LOCATE('@', email) - 1) AS login1,
       SUBSTRING_INDEX(email, '@', 1) AS login2
FROM hereglegch;

-- 7. Сүүлийн 4 тэмдэгт — сөрөг эхлэл
SELECT ner, SUBSTRING(ner, -4) AS suuliin4
FROM baraa;

-- 8. Солих ба зай арилгах
SELECT REPLACE(email, '@example.mn', '@mail.mn') AS shine_email
FROM hereglegch;

SELECT CONCAT('[', TRIM('   Болд   '), ']') AS tseverlesen;

-- 9. + нь текст нийлүүлдэггүй: 15.0 ба 0.0 (анхааруулгатай)
SELECT '10' + '5' AS too_bolson, 'Болд' + 'Сараа' AS buruu;

-- Даалгавар: бараа бүрийг «НЭР (үнэ)» хэлбэрээр, нэрийг том үсгээр гарга
""",
        ),
        LessonSpec(
            title="Тоон функц ба хуваалт",
            slug="toon-funkts-ba-huvaalt",
            description="ROUND, TRUNCATE, FLOOR, CEILING, `/` ба `DIV` хуваалт.",
            duration=540,
            language=MY,
            content="""\
Үнэ, хувь, тоо ширхэгтэй ажиллахад тоон функц хэрэгтэй.

### Товч жагсаалт

| Үйлдэл | Функц | Жишээ → үр дүн |
|---|---|---|
| Тоймлох | `ROUND(x)`, `ROUND(x, d)` | `ROUND(2.567, 2)` → `2.57` |
| Таслах | `TRUNCATE(x, d)` | `TRUNCATE(2.567, 2)` → `2.56` |
| Доош, дээш | `FLOOR`, `CEILING` (`CEIL`) | `FLOOR(2.7)` → `2` |
| Бүхэл хуваалт | `DIV` | `7 DIV 2` → `3` |
| Үлдэгдэл | `%`, `MOD(a, b)` | `7 % 2` → `1` |
| Бусад | `ABS`, `POWER`, `SQRT`, `SIGN` | `POWER(2, 10)` → `1024` |

### ROUND ба TRUNCATE

```sql
SELECT ROUND(2.567, 2);     -- 2.57
SELECT ROUND(2.567);        -- 3 — d бичээгүй бол бүхэл хүртэл
SELECT ROUND(12345, -2);    -- 12300 — сөрөг d нь аравт, зуут руу
SELECT TRUNCATE(2.567, 2);  -- 2.56 — тоймлохгүй, таслана
```

> `TRUNCATE(x, d)` функцийг хүснэгт хоослох `TRUNCATE TABLE`-тэй
> (Модул 7) андуурч болохгүй — нэр л адилхан.

### Нарийн ба ойролцоо тоо

```sql
SELECT ROUND(2.5);    -- 3
SELECT ROUND(2.5e0);  -- 2
```

`2.5` бол **нарийн** (`DECIMAL`) тоо — `.5`-ыг үргэлж тэгээс холдуулж
тоймлоно. `2.5e0` бол **ойролцоо** (`DOUBLE`) тоо — хамгийн ойрын
**тэгш** тоо руу тоймлоно. Мөнгийг `FLOAT`, `DOUBLE` биш `DECIMAL`-аар
хадгалдгийн нэг шалтгаан энэ (Модул 6).

### FLOOR ба CEILING

```sql
SELECT FLOOR(2.7), CEILING(2.1);    -- 2, 3
SELECT FLOOR(-2.5), CEILING(-2.5);  -- -3, -2
```

`FLOOR` нь үргэлж **доош** (сөрөг тоонд тэгээс холдоно), `CEILING` үргэлж
**дээш**.

### Хуваалт: `/` ба `DIV`

```sql
SELECT 7 / 2;     -- 3.5000
SELECT 7 DIV 2;   -- 3
SELECT 1 / 3;     -- 0.3333
```

- `/` нь бүхэл тоог бүхэл тоонд хуваахад ч **бутархай** буцаана.
- Үр дүнгийн бутархай орон анхдагчаар 4-өөр нэмэгдэнэ
  (`div_precision_increment` тохиргоо). Хэрэгтэй оронд нь `ROUND`-оор
  тоймло.
- Бүхэл хуваалт хэрэгтэй бол `DIV` — бутархайг **хаяна** (`-7 DIV 2` → `-3`).

> Бусад зарим DBMS-д бүхэл тоог бүхэл тоонд `/`-ээр хуваахад бутархай
> хэсэг хаягддаг. Өөр сан руу шилжихдээ үүнийг анхаар.

### Бодит жишээ: хайрцгийн тоо

Нэг хайрцагт 12 ширхэг багтана. Бараа бүрт хэдэн хайрцаг хэрэгтэй вэ?

```sql
SELECT ner, uldegdel,
       CEILING(uldegdel / 12)   AS zuv,
       CEILING(uldegdel DIV 12) AS buruu
FROM baraa;
```

Ухаалаг утас (15 ширхэг): `zuv` = 2, `buruu` = 1. `15 DIV 12` нь аль
хэдийн `1` болчихсон тул `CEILING` дээш тоймлох зүйлгүй.

### Хувь тооцоолох

Бүх барааны нийт үлдэгдэл 471. Ухаалаг утасны эзлэх хувь:

```sql
SELECT ROUND(15 * 100 / 471, 2);  -- 3.18
```

### Үлдэгдэл

```sql
SELECT 7 % 2, MOD(7, 2);  -- 1, 1
```

Тэгш тоонд үлдэгдэл `0` — тэгш, сондгойг ялгахад хэрэглэнэ.

### Тэгд хуваах

```sql
SELECT 1 / 0;  -- NULL + анхааруулга 1365 Division by 0
```

MySQL алдаа өгөхгүй, чимээгүй `NULL` өгнө. Энэ нь алдааг нууж болно —
тэгд хуваахаас сэргийлэх `NULLIF`-ийг Модул 11-д үзнэ.
""",
            initial_code="""\
USE delguur;

-- 1. ROUND, TRUNCATE: 2.57, 3, 2.56, 12300
SELECT ROUND(2.567, 2) AS toimlson,
       ROUND(2.567) AS buhel,
       TRUNCATE(2.567, 2) AS taslsan,
       ROUND(12345, -2) AS zuut;

-- 2. Нарийн (DECIMAL) ба ойролцоо (DOUBLE) тоо: 3 ба 2
SELECT ROUND(2.5) AS nariin, ROUND(2.5e0) AS oirolts;

-- 3. FLOOR ба CEILING, сөрөг тоо
SELECT FLOOR(2.7) AS a, CEILING(2.1) AS b,
       FLOOR(-2.5) AS c, CEILING(-2.5) AS d;

-- 4. Хуваалт: / бутархай, DIV бүхэл
SELECT 7 / 2 AS butarhai, 7 DIV 2 AS buhel, 1 / 3 AS gurvanii_neg;

-- 5. Хайрцгийн тоо (12 ширхэгээр): / зөв, DIV буруу
SELECT ner, uldegdel,
       CEILING(uldegdel / 12) AS zuv,
       CEILING(uldegdel DIV 12) AS buruu
FROM baraa;

-- 6. Үлдэгдлийн хувь — нийт 471
SELECT ner, uldegdel,
       ROUND(uldegdel * 100 / 471, 2) AS huvi
FROM baraa;

-- 7. Үлдэгдэл: тэгш эсвэл сондгой id
SELECT baraa_id, baraa_id % 2 AS sondgoi, MOD(baraa_id, 2) AS mod_funkts
FROM baraa;

-- 8. Үнийг мянгат руу тоймлох
SELECT ner, une, ROUND(une, -3) AS toimog_une
FROM baraa;

-- 9. Тэгд хуваах: алдаа биш, NULL + анхааруулга
SELECT 1 / 0 AS teg;

-- Даалгавар: ажилтан бүрийн цалинг 30 хоногт хувааж өдрийн цалинг
-- 2 оронтой бутархайгаар гарга
""",
        ),
        LessonSpec(
            title="Огноо цагийн функцууд",
            slug="ognoo-tsagiin-funkts",
            description="Одоогийн цаг, нэмэх, хасах, зөрүү тооцох, формат.",
            duration=660,
            language=MY,
            content="""\
Захиалгын огноо, хүргэх хугацаа, ажилласан жил — огноо цагтай ажиллах нь
өдөр тутмын ажил.

### Товч жагсаалт

| Үйлдэл | Функц |
|---|---|
| Одоо (огноо, цаг) | `NOW()` |
| Өнөөдөр | `CURDATE()` |
| Он, сар, өдөр | `YEAR(d)`, `MONTH(d)`, `DAY(d)` |
| Цаг, минут | `HOUR(d)`, `MINUTE(d)` |
| Нэмэх | `DATE_ADD(d, INTERVAL 3 DAY)` |
| Хасах | `DATE_SUB(d, INTERVAL 3 DAY)` |
| Өдрийн зөрүү | `DATEDIFF(төгсгөл, эхлэл)` |
| Бусад нэгжээр зөрүү | `TIMESTAMPDIFF(MONTH, эхлэл, төгсгөл)` |
| Сарын сүүлийн өдөр | `LAST_DAY(d)` |
| Огноо хэсгийг авах | `DATE(d)` |
| Формат | `DATE_FORMAT(d, '%Y-%m-%d')` |

### Одоогийн цаг

| Функц | Утга |
|---|---|
| `NOW()` (= `CURRENT_TIMESTAMP`) | Тушаал **эхэлсэн** агшин, `DATETIME` |
| `SYSDATE()` | Функц **дуудагдсан** агшин |
| `CURDATE()` (= `CURRENT_DATE`) | Өнөөдрийн огноо, `DATE` |
| `UTC_TIMESTAMP()` | UTC цаг |

`NOW()` нь **серверийн** цагийн бүсээр буцаана. Монголын цаг UTC+8 тул
сервер өөр бүсэд байвал `UTC_TIMESTAMP()` хэрэглэж, програмд хөрвүүлэх нь
найдвартай.

### Хэсэг задлах

```sql
SELECT zahialga_id,
       YEAR(zahialsan_ognoo)  AS zah_on,
       MONTH(zahialsan_ognoo) AS sar,
       HOUR(zahialsan_ognoo)  AS tsag
FROM zahialga;
```

Мөн `DAYNAME(d)` (гарагийн нэр), `QUARTER(d)` (улирал) зэрэг функц бий.

### Нэмэх, хасах

```sql
-- Хүргэх хугацаа 3 хоног
SELECT zahialga_id, DATE_ADD(zahialsan_ognoo, INTERVAL 3 DAY) FROM zahialga;
SELECT zahialsan_ognoo + INTERVAL 1 MONTH FROM zahialga;  -- товч хэлбэр
SELECT DATE_SUB('2024-03-01', INTERVAL 1 DAY);            -- 2024-02-29
```

`INTERVAL`-ийн нэгж: `SECOND`, `MINUTE`, `HOUR`, `DAY`, `WEEK`, `MONTH`,
`YEAR`.

Сарын төгсгөл зөв тооцогдоно: 2024-01-31 дээр 1 сар нэмэхэд **2024-02-29**.

### DATEDIFF — аргументын дараалал

```sql
-- (төгсгөл, эхлэл), зөвхөн өдрөөр
SELECT DATEDIFF('2024-06-12', '2024-02-03');   -- 130
SELECT DATEDIFF('2024-02-03', '2024-06-12');   -- -130
```

Дарааллыг сольчихвол сөрөг тоо гарна. `DATEDIFF` цагийг тооцохгүй:
`2024-02-03 23:59`-аас `2024-02-04 00:01` хүртэл `1` өдөр.

### TIMESTAMPDIFF — бүтэн нэгж

```sql
SELECT TIMESTAMPDIFF(YEAR, '2023-12-31', '2024-01-01');   -- 0
SELECT TIMESTAMPDIFF(MONTH, '2024-02-03', '2024-06-12');  -- 4
SELECT TIMESTAMPDIFF(HOUR, '2024-02-03 10:15', '2024-02-04 09:00');  -- 22
```

Энд дараалал нь **эсрэг**: `(нэгж, эхлэл, төгсгөл)`. `TIMESTAMPDIFF` нь
**бүтэн** нэгжийг тоолно — 1 өдрийн зөрүүтэй ч 0 жил. Ажилласан жил, нас
тооцоолоход яг хэрэгтэй зүйл.

### Формат

```sql
SELECT DATE_FORMAT(zahialsan_ognoo, '%Y-%m-%d %H:%i') FROM zahialga;
-- 2024-02-03 10:15
```

| Код | Утга |
|---|---|
| `%Y` | Он (4 орон) |
| `%m` | Сар (01–12) |
| `%d` | Өдөр (01–31) |
| `%H` | Цаг (00–23) |
| `%i` | **Минут** |
| `%s` | Секунд |

Хамгийн их алддаг нь **минут**: `%i`. `%m` бол сар — `'%H:%m'` гэж
бичвэл `10:02` гэсэн утгагүй «цаг» гарна.

### WHERE дотор функц

```sql
-- Ажиллана, гэхдээ index ашиглахгүй
WHERE YEAR(zahialsan_ognoo) = 2024 AND MONTH(zahialsan_ognoo) = 3

-- Илүү сайн: завсар
WHERE zahialsan_ognoo >= '2024-03-01' AND zahialsan_ognoo < '2024-04-01'
```

Хоёулаа 3, 4-р захиалгыг олно.
""",
            initial_code="""\
USE delguur;

-- 1. Одоогийн огноо цаг
SELECT NOW() AS odoo, CURDATE() AS unuudur, UTC_TIMESTAMP() AS utc;

-- 2. Огнооны хэсгүүд
SELECT zahialga_id,
       YEAR(zahialsan_ognoo) AS zah_on,
       MONTH(zahialsan_ognoo) AS sar,
       DAY(zahialsan_ognoo) AS udur,
       HOUR(zahialsan_ognoo) AS tsag,
       DATE(zahialsan_ognoo) AS zuvhun_ognoo
FROM zahialga;

-- 3. Хүргэх хугацаа: 3 хоногийн дараа
SELECT zahialga_id,
       zahialsan_ognoo,
       DATE_ADD(zahialsan_ognoo, INTERVAL 3 DAY) AS hurgeh_ognoo
FROM zahialga;

-- 4. Сарын төгсгөл: 2024-02-29
SELECT DATE_ADD('2024-01-31', INTERVAL 1 MONTH) AS nemsen,
       LAST_DAY('2024-02-10') AS saryn_suul;

-- 5. DATEDIFF (төгсгөл, эхлэл): 130
SELECT DATEDIFF('2024-06-12', '2024-02-03') AS honog;

-- 6. Бүтэн нэгжээр: 0 жил, 4 сар
SELECT TIMESTAMPDIFF(YEAR, '2023-12-31', '2024-01-01') AS jil,
       TIMESTAMPDIFF(MONTH, '2024-02-03', '2024-06-12') AS sar;

-- 7. Ажилтан бүрийн ажилласан бүтэн жил
SELECT ner, ajild_orson,
       TIMESTAMPDIFF(YEAR, ajild_orson, CURDATE()) AS ajilsan_jil
FROM ajiltan;

-- 8. Формат: %i нь минут
SELECT zahialga_id,
       DATE_FORMAT(zahialsan_ognoo, '%Y-%m-%d %H:%i') AS formatlasan,
       DATE_FORMAT(zahialsan_ognoo, '%d/%m/%Y') AS udur_ehend
FROM zahialga;

-- 9. 3-р сарын захиалга — завсраар
SELECT zahialga_id, zahialsan_ognoo
FROM zahialga
WHERE zahialsan_ognoo >= '2024-03-01'
  AND zahialsan_ognoo < '2024-04-01';

-- Даалгавар: хэрэглэгч бүр бүртгүүлснээс хойш хэдэн хоног өнгөрснийг ол
""",
        ),
        LessonSpec(
            title="CAST ба CONVERT",
            slug="cast-ba-convert",
            description="Төрөл хөрвүүлэх, текст ба огноо, бүтэлгүй хөрвүүлэлт.",
            duration=540,
            language=MY,
            content="""\
### Далд ба илт хөрвүүлэлт

Сервер төрлийг өөрөө хөрвүүлэхийг **далд** хөрвүүлэлт гэнэ. Энэ нь
заримдаа санаснаар, заримдаа үгүй ажилладаг — өмнөх хичээлүүдэд `'abc' = 0`
үнэн болж, `'Болд' + 'Сараа'` нь `0` болсныг харсан. Төрлийг **илт** заах
нь найдвартай.

### CAST — стандарт

```sql
SELECT CAST(une AS SIGNED) FROM baraa;                -- 1250000
SELECT CAST(zahialsan_ognoo AS DATE) FROM zahialga;   -- 2024-02-03
SELECT CAST(uldegdel AS CHAR) FROM baraa;             -- '15'
```

`CAST(утга AS төрөл)`-ийн зорилтот төрөл MySQL-д хүснэгтийн баганын
төрлөөс арай өөр нэртэй:

| Зорилт | `CAST`-д бичих | Жишээ |
|---|---|---|
| Бүхэл тоо | `SIGNED`, `UNSIGNED` | `CAST('42' AS SIGNED)` |
| Бутархай | `DECIMAL(p,s)`, `DOUBLE` | `CAST('3.14' AS DECIMAL(5,2))` |
| Текст | `CHAR`, `CHAR(n)` | `CAST(15 AS CHAR)` |
| Огноо, цаг | `DATE`, `DATETIME`, `TIME` | `CAST('2024-02-03' AS DATE)` |

> `CAST(x AS INT)`, `CAST(x AS VARCHAR(10))` гэж бичвэл MySQL-д
> **синтакс алдаа** (1064). Бүхэл тоонд `SIGNED`, текстэд `CHAR`.

### CONVERT

```sql
SELECT CONVERT(uldegdel, CHAR) FROM baraa;   -- CAST(uldegdel AS CHAR)-тай ижил
SELECT CONVERT('текст' USING utf8mb4);       -- тэмдэгтийн багц солих
```

`CONVERT(утга, төрөл)` нь `CAST`-ын өөр бичлэг. `USING` хэлбэр нь
текстийн кодчиллыг солино. Стандарт тул `CAST`-ыг илүүд үз.

### Огноо ↔ текст

Огноог текст болгохдоо өмнөх хичээлийн `DATE_FORMAT`, текстээс огноо
гаргахдаа түүний эсрэг `STR_TO_DATE`-ийг хэрэглэнэ. Хэлбэрийн код нь
адилхан:

```sql
SELECT DATE_FORMAT('2024-02-03', '%d/%m/%Y');   -- 03/02/2024
SELECT STR_TO_DATE('03/02/2024', '%d/%m/%Y');   -- 2024-02-03
SELECT STR_TO_DATE('2024-13-45', '%Y-%m-%d');   -- NULL + анхааруулга
```

Хэрэглэгч, Excel-ээс ирсэн `03.02.2024` гэх мэт текстийг огноо болгоход
`STR_TO_DATE` хэрэгтэй.

### Мөнгөний формат

```sql
SELECT FORMAT(une, 2) FROM baraa;   -- 1,250,000.00
SELECT FORMAT(une, 0) FROM baraa;   -- 1,250,000
```

`FORMAT` **текст** буцаана — харуулахад л хэрэглэ. Үр дүнгээр нь тооцоо
хийх, эрэмбэлэх гэвэл текстээр харьцуулагдана.

### Хөрвүүлэлт бүтэлгүйтвэл

| Илэрхийлэл | Үр дүн |
|---|---|
| `CAST('123' AS SIGNED)` | `123` |
| `CAST('abc' AS SIGNED)` | `0` + анхааруулга |
| `CAST('12abc' AS SIGNED)` | `12` + анхааруулга |

MySQL `SELECT` дотор буруу текстэд **алдаа өгөхгүй** — эхний тоо биш
тэмдэгт хүртэлх хэсгийг авч, анхааруулга (1292 `Truncated incorrect ...`)
үлдээнэ. Энэ сайтын console анхааруулгыг шууд харуулна. `mysql` CLI
дээр `SHOW WARNINGS;` гэж харна.

> Харин хүснэгтэд мөр **нэмэх, засах** үед буруу утга алдаа өгнө
> (strict горим — Модул 6).

### Бутархайг бүхэл болгох

```sql
SELECT CAST(2.9 AS SIGNED);    -- 3 — тоо тоймлогдоно
SELECT CAST('2.9' AS SIGNED);  -- 2 — текст таслагдана
```

Ижил утга өөр үр дүн өгч байна! Санаагаа илт бич: `ROUND`, `FLOOR`,
`TRUNCATE`.

### Урт, нарийвчлалыг заавал бич

| Бичсэн | Үр дүн |
|---|---|
| `CAST(2.567 AS DECIMAL)` | `3` — `DECIMAL(10,0)` гэж ойлгоно |
| `CAST(2.567 AS DECIMAL(10,2))` | `2.57` |
| `CAST('Ухаалаг утас' AS CHAR(3))` | `Уха` + анхааруулга |

`CAST` нь урт текстийг таслана, нарийвчлалгүй `DECIMAL` бутархайгаа
алдана. Үргэлж `DECIMAL(12,2)` гэх мэтээр бүтэн заа.
""",
            initial_code="""\
USE delguur;

-- 1. CAST: DECIMAL-ийг бүхэл тоо, DATETIME-ийг DATE, TIME болгох
SELECT ner, une, CAST(une AS SIGNED) AS buhel_une
FROM baraa;

SELECT zahialga_id,
       CAST(zahialsan_ognoo AS DATE) AS ognoo,
       CAST(zahialsan_ognoo AS TIME) AS tsag
FROM zahialga;

-- 2. Тоог текст болгож нийлүүлэх
SELECT CONCAT('Үлдэгдэл: ', CAST(uldegdel AS CHAR)) AS medeelel
FROM baraa;

-- 3. CONVERT(утга, төрөл) — CAST-тай ижил
SELECT CONVERT(42, CHAR) AS tekst, CONVERT('42', SIGNED) AS too;

-- 4. Текстээс огноо: STR_TO_DATE
SELECT STR_TO_DATE('03/02/2024', '%d/%m/%Y') AS ognoo,
       STR_TO_DATE('03.02.2024 10:15', '%d.%m.%Y %H:%i') AS ognoo_tsag;

-- 5. Огноог текст болгох: DATE_FORMAT
SELECT ner, DATE_FORMAT(ajild_orson, '%d.%m.%Y') AS ognoo_tekst
FROM ajiltan;

-- 6. Мөнгөний формат: мянгатын таслал
SELECT ner, une, FORMAT(une, 2) AS une_tekst
FROM baraa;

-- 7. Бүтэлгүй хөрвүүлэлт: алдаа биш, 0 ба 12 + анхааруулга
SELECT CAST('123' AS SIGNED) AS zuv,
       CAST('abc' AS SIGNED) AS buruu,
       CAST('12abc' AS SIGNED) AS holimog;

-- 8. Бутархай -> бүхэл: тоо тоймлогдоно (3), текст таслагдана (2)
SELECT CAST(2.9 AS SIGNED) AS toonoos,
       CAST('2.9' AS SIGNED) AS tekstees,
       FLOOR(2.9) AS floor_ilt;

-- 9. Нарийвчлалгүй DECIMAL бутархайгаа алдана
SELECT CAST(2.567 AS DECIMAL) AS nariivchlalgui,
       CAST(2.567 AS DECIMAL(10,2)) AS nariivchlaltai;

-- Даалгавар: ажилтан бүрийн цалинг мянгатын таслалтай, бутархай оронгүй
-- текстээр гарга
""",
        ),
    ],
)

AGGREGATION = ModuleSpec(
    title="Модул 5 — Бүлэглэл",
    description="Нэгтгэх функц, GROUP BY, HAVING ба асуулгын логик дараалал.",
    lessons=[
        LessonSpec(
            title="COUNT, SUM, AVG, MIN, MAX",
            slug="count-sum-avg-min-max",
            description="Олон мөрийг нэг утга болгох ба NULL-ийн занга.",
            duration=540,
            language=MY,
            content="""\
Нэгтгэх (aggregate) функц нь **олон мөрийг нэг утга** болгоно: «хэдэн
хэрэглэгч байна», «нийт борлуулалт хэд», «хамгийн үнэтэй бараа хэд вэ».

### Таван үндсэн функц

| Функц | Утга | NULL |
|---|---|---|
| `COUNT(*)` | Мөрийн тоо | Тоолно |
| `COUNT(багана)` | `NULL` биш утгын тоо | Алгасна |
| `COUNT(DISTINCT багана)` | Давтагдахгүй утгын тоо | Алгасна |
| `SUM(багана)` | Нийлбэр | Алгасна |
| `AVG(багана)` | Дундаж | Алгасна |
| `MIN`, `MAX` | Хамгийн бага, их | Алгасна |

### COUNT-ийн гурван хэлбэр

```sql
SELECT COUNT(*)            AS niit,
       COUNT(hot)          AS hottoi,
       COUNT(DISTINCT hot) AS hotyn_too,
       COUNT(utas)         AS utastai
FROM hereglegch;
```

| niit | hottoi | hotyn_too | utastai |
|---|---|---|---|
| 8 | 7 | 3 | 6 |

- 8 хэрэглэгч бий.
- Хулан-гийн хот `NULL` тул `COUNT(hot)` = 7.
- Давтагдахгүй хот: Улаанбаатар, Дархан, Эрдэнэт = 3.
- Сараа, Хулан хоёрын утас `NULL` тул 6.

MySQL-д `COUNT(DISTINCT a, b)` нь хоёр баганын давтагдахгүй **хослолыг**
тоолно: `COUNT(DISTINCT hereglegch_id, tuluv)` = 9.

### SUM, MIN, MAX

```sql
SELECT SUM(uldegdel) AS niit_uldegdel,  -- 471
       MIN(une)      AS hamgiin_hyamd,  -- 3500.00
       MAX(une)      AS hamgiin_unetei  -- 3200000.00
FROM baraa;
```

`MIN`, `MAX` нь текст, огноонд ч ажиллана:

```sql
SELECT MIN(zahialsan_ognoo), MAX(zahialsan_ognoo) FROM zahialga;
-- 2024-02-03 10:15:00, 2024-06-12 19:30:00

SELECT MIN(ner), MAX(ner) FROM baraa;
-- SQL сурах бичиг, Чихэвч — collation-ы дарааллаар
```

Текстийг collation-ы дүрмээр харьцуулна: латин үсэг кирилл үсгээс өмнө
ордог тул `SQL сурах бичиг` хамгийн «бага» болов.

Илэрхийллийг ч нэгтгэж болно — нийт борлуулалт:

```sql
SELECT SUM(too * negj_une) AS niit_dun FROM zahialgiin_mur;  -- 11191000.00
```

(Цуцлагдсан 4-р захиалга ч орсон — шүүхийг JOIN-ы дараа үзнэ.)

### AVG

```sql
SELECT AVG(uldegdel) FROM baraa;   -- 39.2500
```

`471 / 12 = 39.25`. MySQL-ийн `AVG` бүхэл баганаас ч **бутархай** дундаж
буцаана (4 нэмэлт оронтой). Харуулахдаа `ROUND(AVG(uldegdel), 1)`.

`AVG(багана)` нь `NULL` мөрүүдийг **тоолохгүй**: нийлбэрийг `NULL` биш
утгын тоонд хуваана. Тиймээс `SUM(багана) / COUNT(*)`-аас ялгаатай байж
болно — `NULL`-ийг 0 гэж тооцох ёстой эсэхийг бодоорой.

### NULL ба хоосон үр дүн

```sql
SELECT COUNT(*) AS too, SUM(uldegdel) AS niilber
FROM baraa
WHERE une > 99999999;
```

Нэг ч мөр таарахгүй: `COUNT(*)` = **0**, харин `SUM` = **NULL** (0 биш).
`NULL`-ийг 0 болгох `COALESCE`-ийг Модул 11-д үзнэ.

### Нэгтгэх функцтэй хамт энгийн багана

```sql
SELECT ner, MAX(une) FROM baraa;  -- АЛДАА 1140
```

«Аль барааны нэр?» гэдэг тодорхойгүй тул MySQL 8 анхдагчаар алдаа өгнө.
Шийдлийг дараагийн хичээлд (`GROUP BY`) үзнэ. Нэгтгэх функцыг `WHERE`
дотор бичиж **болохгүй** — `HAVING`-ийг гуравдахь хичээлд үзнэ.
""",
            initial_code="""\
USE delguur;

-- 1. COUNT-ийн гурван хэлбэр: 8, 7, 3, 6
SELECT COUNT(*) AS niit,
       COUNT(hot) AS hottoi,
       COUNT(DISTINCT hot) AS hotyn_too,
       COUNT(utas) AS utastai
FROM hereglegch;

-- 2. Хоёр баганын давтагдахгүй хослол: 9
SELECT COUNT(DISTINCT hereglegch_id, tuluv) AS hoslol
FROM zahialga;

-- 3. SUM, MIN, MAX
SELECT SUM(uldegdel) AS niit_uldegdel,
       MIN(une) AS hamgiin_hyamd,
       MAX(une) AS hamgiin_unetei
FROM baraa;

-- 4. Огноо ба текстэнд MIN, MAX
SELECT MIN(zahialsan_ognoo) AS ehnii,
       MAX(zahialsan_ognoo) AS suuliin
FROM zahialga;

SELECT MIN(ner) AS ehnii_ner, MAX(ner) AS suuliin_ner
FROM baraa;

-- 5. Илэрхийллийн нийлбэр — нийт борлуулалт
SELECT SUM(too * negj_une) AS niit_dun
FROM zahialgiin_mur;

-- 6. AVG бүхэл баганаас бутархай дундаж: 39.2500
SELECT AVG(uldegdel) AS dundaj,
       ROUND(AVG(uldegdel), 1) AS toimlson
FROM baraa;

-- 7. Хоосон үр дүн: COUNT 0, SUM NULL
SELECT COUNT(*) AS too, SUM(uldegdel) AS niilber
FROM baraa
WHERE une > 99999999;

-- 8. NULL-ийг алгасна: 6 ба 5
SELECT COUNT(*) AS ajiltan, COUNT(menejer_id) AS menejertei
FROM ajiltan;

-- 9. Алдаа 1140 — туршихдаа тайлбарыг арилга
-- SELECT ner, MAX(une) FROM baraa;

-- Даалгавар: ajiltan хүснэгтийн дундаж, хамгийн бага, хамгийн их цалинг ол
""",
        ),
        LessonSpec(
            title="GROUP BY",
            slug="group-by-buleglel",
            description="Мөрүүдийг бүлэглэж бүлэг бүрт нэгтгэх, ONLY_FULL_GROUP_BY.",
            duration=600,
            language=MY,
            content="""\
Өмнөх хичээлд бүх хүснэгтийг **нэг** утга болгосон. `GROUP BY` нь
мөрүүдийг бүлэгт хувааж, **бүлэг бүрт** нэг мөр гаргана.

### Анхны жишээ

```sql
SELECT angilal_id,
       COUNT(*)            AS baraa_too,
       SUM(uldegdel)       AS niit_uldegdel,
       ROUND(AVG(une), 2)  AS dundaj_une
FROM baraa
GROUP BY angilal_id;
```

| angilal_id | baraa_too | niit_uldegdel | dundaj_une |
|---|---|---|---|
| 1 | 3 | 61 | 1513000.00 |
| 2 | 2 | 25 | 177500.00 |
| 3 | 2 | 72 | 41500.00 |
| 4 | 3 | 113 | 254333.33 |
| 5 | 2 | 200 | 7750.00 |

Хэрхэн ажилладаг вэ:

```text
12 мөр  →  angilal_id-аар 5 овоо  →  овоо бүрийг нэг мөр болгоно
```

### Олон баганаар

```sql
SELECT hereglegch_id, tuluv, COUNT(*) AS too
FROM zahialga
GROUP BY hereglegch_id, tuluv;
```

**Хослол** бүр нэг бүлэг — 9 мөр. 1-р хэрэглэгч: «Хүргэгдсэн» 2,
«Хүлээгдэж буй» 1.

### NULL нэг бүлэг болно

```sql
SELECT hot, COUNT(*) AS too
FROM hereglegch
GROUP BY hot;
```

Улаанбаатар 4, Дархан 2, Эрдэнэт 1, `NULL` 1. `WHERE`-д `NULL = NULL`
үнэн биш байсан ч `GROUP BY`, `DISTINCT` нь бүх `NULL`-ийг нэг бүлэгт
оруулна.

### Алтан дүрэм

> `SELECT`-д байгаа, нэгтгэх функц **доторх биш** багана бүр `GROUP BY`-д
> байх ёстой.

```sql
SELECT angilal_id, ner, COUNT(*)
FROM baraa
GROUP BY angilal_id;
```

1-р ангилалд 3 бараа бий — аль `ner`-ийг харуулах вэ? Хариулт тодорхойгүй.

| Горим | Үр дүн |
|---|---|
| MySQL 5.7.5+, анхдагч | Алдаа 1055: «... this is incompatible with sql_mode=only_full_group_by» |
| `ONLY_FULL_GROUP_BY` унтраалттай | Алдаагүй, **санамсаргүй** нэг нэр — хамгийн аюултай |

### ONLY_FULL_GROUP_BY

MySQL 5.7.5-аас хойш анхдагчаар асаалттай горим. Шалгах:

```sql
SELECT @@sql_mode;
```

Хуучин код «ажиллахгүй болсон» гэж энэ горимыг унтраадаг хүмүүс бий —
**бүү унтраа**. Алдаа нь асуулга чинь буруу гэдгийг хэлж байна.

Аль ч утга хамаагүй гэдгээ илт хэлэх бол MySQL-д `ANY_VALUE(ner)`.

MySQL нэг зүйлд ухаалаг: `GROUP BY`-д **primary key** байвал тэр
хүснэгтийн бусад баганыг `SELECT`-д бичихийг зөвшөөрнө (functional
dependency) — id тодорхой бол нэр нь ч тодорхой.

### Илэрхийллээр бүлэглэх

Сар бүрийн захиалгын тоо:

```sql
SELECT YEAR(zahialsan_ognoo) AS zah_on, MONTH(zahialsan_ognoo) AS sar,
       COUNT(*) AS too
FROM zahialga
GROUP BY zah_on, sar
ORDER BY zah_on, sar;
```

2-оос 6-р сар хүртэл сар бүр 2 захиалга. MySQL `GROUP BY`-д `SELECT`-ийн
alias-ыг зөвшөөрдөг. Стандарт SQL-д энэ нь ажиллахгүй тул илэрхийллийг
давтаж бичих нь бас түгээмэл: `GROUP BY YEAR(zahialsan_ognoo),
MONTH(zahialsan_ognoo)`.

### Бүлэглэл эрэмбэлэхгүй

MySQL 5.7 хүртэл `GROUP BY` үр дүнг эрэмбэлдэг байсан — MySQL 8-д
**больсон**. Дараалал хэрэгтэй бол `ORDER BY` бич.

### Захиалга бүрийн дүн

```sql
SELECT zahialga_id, SUM(too * negj_une) AS dun
FROM zahialgiin_mur
GROUP BY zahialga_id
ORDER BY dun DESC;
```

Хамгийн том нь 10-р захиалга (3 289 000), дараа нь 4-р (3 200 000).
""",
            initial_code="""\
USE delguur;

-- 1. Ангилал бүрийн барааны тоо, үлдэгдэл, дундаж үнэ
SELECT angilal_id,
       COUNT(*) AS baraa_too,
       SUM(uldegdel) AS niit_uldegdel,
       ROUND(AVG(une), 2) AS dundaj_une
FROM baraa
GROUP BY angilal_id
ORDER BY angilal_id;

-- 2. Хот бүрийн хэрэглэгч — NULL нэг бүлэг
SELECT hot, COUNT(*) AS too
FROM hereglegch
GROUP BY hot
ORDER BY too DESC;

-- 3. Хэрэглэгч ба төлөвийн хослол
SELECT hereglegch_id, tuluv, COUNT(*) AS too
FROM zahialga
GROUP BY hereglegch_id, tuluv
ORDER BY hereglegch_id, tuluv;

-- 4. Сар бүрийн захиалга — alias-аар бүлэглэж болно
SELECT YEAR(zahialsan_ognoo) AS zah_on,
       MONTH(zahialsan_ognoo) AS sar,
       COUNT(*) AS too
FROM zahialga
GROUP BY zah_on, sar
ORDER BY zah_on, sar;

-- 5. Захиалга бүрийн нийт дүн
SELECT zahialga_id,
       COUNT(*) AS mur_too,
       SUM(too * negj_une) AS dun
FROM zahialgiin_mur
GROUP BY zahialga_id
ORDER BY dun DESC;

-- 6. Бараа бүр нийт хэдэн ширхэг зарагдсан
SELECT baraa_id, SUM(too) AS zaragdsan
FROM zahialgiin_mur
GROUP BY baraa_id
ORDER BY zaragdsan DESC;

-- 7. Алдаа 1055 — туршихдаа тайлбарыг арилга
-- SELECT angilal_id, ner, COUNT(*) FROM baraa GROUP BY angilal_id;

-- 8. ANY_VALUE: аль ч нэр хамаагүй гэдгээ илт хэлнэ
SELECT angilal_id, ANY_VALUE(ner) AS jishee_baraa, COUNT(*) AS too
FROM baraa
GROUP BY angilal_id;

-- Даалгавар: ajiltan хүснэгтийг alban_tushaal-аар бүлэглэж
-- албан тушаал бүрийн хүний тоо, дундаж цалинг ол
""",
        ),
        LessonSpec(
            title="HAVING ба асуулгын логик дараалал",
            slug="having-ba-logik-daraalal",
            description="Бүлгийг шүүх, WHERE-ээс ялгах, SQL хэрхэн биелдэг вэ.",
            duration=600,
            language=MY,
            content="""\
### HAVING — бүлгийг шүүх

2 ба түүнээс олон захиалга хийсэн хэрэглэгч:

```sql
SELECT hereglegch_id, COUNT(*) AS zahialga_too
FROM zahialga
GROUP BY hereglegch_id
HAVING COUNT(*) >= 2;
```

| hereglegch_id | zahialga_too |
|---|---|
| 1 | 3 |
| 2 | 2 |

`WHERE COUNT(*) >= 2` гэж бичвэл MySQL алдаа 1111 «Invalid use of group
function» өгнө: `WHERE` ажиллах үед бүлэг хараахан үүсээгүй.

### WHERE ба HAVING

| | `WHERE` | `HAVING` |
|---|---|---|
| Юуг шүүх | **Мөр** | **Бүлэг** |
| Хэзээ | Бүлэглэхээс **өмнө** | Бүлэглэсний **дараа** |
| Нэгтгэх функц | Үгүй | Тийм |

Хоёуланг нь хамт:

```sql
SELECT hereglegch_id, COUNT(*) AS hurgegdsen
FROM zahialga
WHERE tuluv = 'Хүргэгдсэн'
GROUP BY hereglegch_id
HAVING COUNT(*) >= 2;
```

Одоо зөвхөн 1-р хэрэглэгч (2 захиалга). 2-р хэрэглэгчийн нэг захиалга
«Хүлээгдэж буй» тул `WHERE` түүнийг **бүлэглэхээс өмнө** хасч, 1 л үлдсэн.

> **Дүрэм:** нэгтгэх функцгүй нөхцлийг `HAVING` биш `WHERE`-д бич — мөрийг
> эрт хасах тул хурдан.

### Том захиалгууд

```sql
SELECT zahialga_id, SUM(too * negj_une) AS dun
FROM zahialgiin_mur
GROUP BY zahialga_id
HAVING SUM(too * negj_une) > 1000000
ORDER BY dun DESC;
```

10-р (3 289 000), 4-р (3 200 000), 6-р (1 620 000), 1-р (1 428 000).

### Логик дараалал

SQL-ийг **бичих** дараалал ба **биелэх** дараалал өөр:

| Бичих | Биелэх |
|---|---|
| 1. `SELECT` | 1. `FROM` — хүснэгт |
| 2. `FROM` | 2. `WHERE` — мөр шүүх |
| 3. `WHERE` | 3. `GROUP BY` — бүлэглэх |
| 4. `GROUP BY` | 4. `HAVING` — бүлэг шүүх |
| 5. `HAVING` | 5. `SELECT` — багана, alias тооцох |
| 6. `ORDER BY` | 6. `DISTINCT` |
| 7. `LIMIT` | 7. `ORDER BY` — эрэмбэлэх |
| | 8. `LIMIT` — мөр таслах |

### Алхам алхмаар

Зөөврийн компьютер (`baraa_id = 2`)-оос бусад бараагаар 200 000-аас их
дүнтэй захиалгуудын хамгийн том 3:

```sql
SELECT zahialga_id, SUM(too * negj_une) AS dun   -- 5
FROM zahialgiin_mur                              -- 1
WHERE baraa_id <> 2                              -- 2
GROUP BY zahialga_id                             -- 3
HAVING SUM(too * negj_une) > 200000              -- 4
ORDER BY dun DESC                                -- 6
LIMIT 3;                                         -- 7
```

| Алхам | Үлдсэн |
|---|---|
| 1. `FROM` | 19 мөр |
| 2. `WHERE` | 17 мөр — 4, 10-р захиалгын компьютер хасагдав |
| 3. `GROUP BY` | 9 бүлэг — 4-р захиалга бүхэлдээ алга |
| 4. `HAVING` | 6 бүлэг |
| 5. `SELECT` | `dun` тооцоологдов |
| 6. `ORDER BY` | 6, 1, 5, 8, 2, 9 |
| 7. `LIMIT` | 6 (1 620 000), 1 (1 428 000), 5 (680 000) |

### Дарааллын үр дагавар: alias хаана ажиллах вэ

| Хэсэг | MySQL-д alias ажиллах уу |
|---|---|
| `WHERE` | Үгүй |
| `GROUP BY` | Тийм (MySQL өргөтгөл) |
| `HAVING` | Тийм (MySQL өргөтгөл) |
| `ORDER BY` | Тийм |

Стандартаар alias зөвхөн `ORDER BY`-д ажиллана — `SELECT`-ийн дараа
биелдэг цорын ганц хэсэг. MySQL өргөтгөл болгож `GROUP BY`, `HAVING`-д
зөвшөөрдөг:

```sql
SELECT hereglegch_id, COUNT(*) AS zahialga_too
FROM zahialga
GROUP BY hereglegch_id
HAVING zahialga_too >= 2;
```

Бусад DBMS-д ч ажиллах код бичих бол `HAVING`-д функцыг давтан бич.

> **Логик ≠ физик.** Энэ бол үр дүнг **тодорхойлох** дараалал. Серверийн
> optimizer бодит гүйцэтгэлийг өөрөөр зохион байгуулж болох ч үр дүн
> энэ дараалалтай ижил байна.
""",
            initial_code="""\
USE delguur;

-- 1. 2 ба түүнээс олон захиалгатай хэрэглэгч
SELECT hereglegch_id, COUNT(*) AS zahialga_too
FROM zahialga
GROUP BY hereglegch_id
HAVING COUNT(*) >= 2;

-- 2. WHERE мөрийг, HAVING бүлгийг шүүнэ — зөвхөн 1-р хэрэглэгч
SELECT hereglegch_id, COUNT(*) AS hurgegdsen
FROM zahialga
WHERE tuluv = 'Хүргэгдсэн'
GROUP BY hereglegch_id
HAVING COUNT(*) >= 2;

-- 3. Нэг саяас их дүнтэй захиалга
SELECT zahialga_id, SUM(too * negj_une) AS dun
FROM zahialgiin_mur
GROUP BY zahialga_id
HAVING SUM(too * negj_une) > 1000000
ORDER BY dun DESC;

-- 4. Бүх алхамтай асуулга: 6, 1, 5-р захиалга
SELECT zahialga_id, SUM(too * negj_une) AS dun
FROM zahialgiin_mur
WHERE baraa_id <> 2
GROUP BY zahialga_id
HAVING SUM(too * negj_une) > 200000
ORDER BY dun DESC
LIMIT 3;

-- 5. MySQL өргөтгөл: HAVING дотор alias
SELECT hereglegch_id, COUNT(*) AS zahialga_too
FROM zahialga
GROUP BY hereglegch_id
HAVING zahialga_too >= 2;

-- 6. Ангилал бүрийн нийт үлдэгдэл 100-аас их
SELECT angilal_id, SUM(uldegdel) AS niit_uldegdel
FROM baraa
GROUP BY angilal_id
HAVING SUM(uldegdel) > 100
ORDER BY niit_uldegdel DESC;

-- 7. Алдаа: WHERE дотор нэгтгэх функц — туршихдаа тайлбарыг арилга
-- SELECT hereglegch_id FROM zahialga WHERE COUNT(*) >= 2 GROUP BY hereglegch_id;

-- Даалгавар: нийт 3-аас олон ширхэг зарагдсан барааны baraa_id,
-- зарагдсан тоог ихээс бага руу эрэмбэлж гарга
""",
        ),
    ],
)

SQL_QUERY_MODULES = [SELECT_BASICS, WHERE_FILTERING, BUILTIN_FUNCTIONS, AGGREGATION]
