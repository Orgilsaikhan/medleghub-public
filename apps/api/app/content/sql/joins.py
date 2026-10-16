"""Модул 9-11 — JOIN, дэд асуулга, олонлогийн үйлдэл ба нөхцөлт илэрхийлэл.

Бодит өгөгдөл олон хүснэгтэд тархсан байдаг. Эдгээр модулиар хүснэгтүүдийг
холбож, асуулга дотор асуулга бичиж, үр дүнг нэгтгэж сурна.
"""

from app.content.types import LessonSpec, ModuleSpec
from app.models.enums import LessonLanguage

MY = LessonLanguage.MYSQL

JOINS = ModuleSpec(
    title="Модул 9 — JOIN",
    description="Хоёр ба түүнээс олон хүснэгтийг холбох.",
    lessons=[
        LessonSpec(
            title="INNER JOIN",
            slug="inner-join",
            description="Хоёр хүснэгтийн тохирох мөрүүдийг холбох.",
            duration=540,
            language=MY,
            content="""\
`zahialga` хүснэгтэд зөвхөн `hereglegch_id` хадгалагддаг. Захиалагчийн
**нэрийг** харахын тулд `hereglegch` хүснэгттэй **холбох** хэрэгтэй.

### Үндсэн бичлэг

```sql
SELECT z.zahialga_id, h.ner, z.zahialsan_ognoo, z.tuluv
FROM zahialga AS z
INNER JOIN hereglegch AS h
    ON z.hereglegch_id = h.hereglegch_id
ORDER BY z.zahialga_id;
```

| zahialga_id | ner | zahialsan_ognoo | tuluv |
|---|---|---|---|
| 1 | Болд | 2024-02-03 10:15:00 | Хүргэгдсэн |
| 2 | Сараа | 2024-02-14 18:40:00 | Хүргэгдсэн |
| 3 | Болд | 2024-03-09 09:05:00 | Хүргэгдсэн |
| 4 | Тэмүүлэн | 2024-03-21 14:30:00 | Цуцлагдсан |
| … | … | … | … |

Нийт 10 мөр гарна. `ON` нөхцөл нь «аль мөр аль мөртэй тохирох вэ» гэдгийг
заана — ихэвчлэн гадаад түлхүүр = үндсэн түлхүүр.

### INNER JOIN юу буцаадаг вэ

**Хоёр талд хоёуланд нь** тохирол олдсон мөрүүдийг л буцаана. Мөнх
(`hereglegch_id = 8`) захиалгагүй тул энэ үр дүнд **огт гарахгүй**.
Тохиролгүй мөрийг хадгалах бол `LEFT JOIN` хэрэгтэй (дараагийн хичээл).

`JOIN` гэж товч бичвэл `INNER JOIN`-тэй яг адилхан.

### Товч нэр (alias)

`AS z`, `AS h` нь хүснэгтийн товч нэр. `AS` үгийг орхиж болно:
`FROM zahialga z`. Товч нэр өгсний дараа **хүснэгтийн бүтэн нэрээр**
хандаж болохгүй — `zahialga.tuluv` гэж бичвэл алдаа гарна.

### Ижил нэртэй багана

`baraa` ба `angilal` хоёуланд нь `ner` багана бий. Аль хүснэгтийнхийг
заахгүй бол алдаа өгнө: `ERROR 1052: Column 'ner' in field list is ambiguous`.

```sql
SELECT b.ner AS baraa, a.ner AS angilal, b.une
FROM baraa AS b
JOIN angilal AS a ON b.angilal_id = a.angilal_id;
```

> Олон хүснэгттэй асуулгад **бүх** баганад товч нэрээ бич. Дараа нь хүснэгт
> нэмэхэд санаандгүй давхцал үүсэхээс сэргийлнэ.

### Нэмэлт шүүлт

Холбосны дараа `WHERE` нь аль ч хүснэгтийн баганаар шүүж чадна:

```sql
SELECT z.zahialga_id, h.ner, h.hot
FROM zahialga AS z
JOIN hereglegch AS h ON z.hereglegch_id = h.hereglegch_id
WHERE h.hot = 'Улаанбаатар'
  AND z.tuluv = 'Хүргэгдсэн';
```

Улаанбаатарын хэрэглэгчдийн хүргэгдсэн 4 захиалга (1, 2, 3, 6) гарна.

### Хуучин «таслалтай» бичлэг

```sql
SELECT z.zahialga_id, h.ner
FROM zahialga z, hereglegch h
WHERE z.hereglegch_id = h.hereglegch_id;
```

Ажиллана, үр дүн нь ижил. Гэхдээ **бүү ашигла**:

- Холбох нөхцөл ба шүүлт `WHERE` дотор холилдож, уншихад хэцүү.
- `WHERE`-ээ мартвал алдаа гарахгүй — **10 × 8 = 80** мөр (декартын
  үржвэр) чимээгүй буцна.
- `LEFT JOIN` рүү шилжүүлэхэд бүхэлд нь дахин бичих хэрэгтэй.

### USING, NATURAL JOIN ба ON-гүй JOIN

| Бичлэг | Утга |
|---|---|
| `JOIN h USING (hereglegch_id)` | `ON z.hereglegch_id = h.hereglegch_id`-ийн товчлол |
| `NATURAL JOIN` | **Ижил нэртэй бүх** баганаар өөрөө холбоно |
| `ON`-гүй `JOIN` | MySQL алдаа өгөхгүй — CROSS JOIN болно |

`USING` нь хоёр хүснэгтэд багана **ижил нэртэй** үед л ажиллана.
`NATURAL JOIN` аюултай: `baraa`, `angilal` хоёуланд `ner` багана байгаа
тул түүгээр ч холбож, юу ч олдохгүй. `ON`-оо мартвал алдааны оронд
80 мөрийн үржвэр гарна. Хамгийн ойлгомжтой нь үргэлж `ON` бичих.

### JOIN-той UPDATE

Модул 7-д захиалга 9-ийн мөрүүдээр барааны үлдэгдлийг хасахдаа бараа
бүрт тусдаа `UPDATE` бичсэн. `JOIN` мэддэг болсон тул одоо нэг тушаалаар
бичнэ — `zahialgiin_mur`-ийн `too`-г шууд авч хасна:

```sql
UPDATE baraa AS b
JOIN zahialgiin_mur AS zm ON zm.baraa_id = b.baraa_id
SET b.uldegdel = b.uldegdel - zm.too
WHERE zm.zahialga_id = 9;
```

Бүтэц нь `UPDATE a JOIN b ON … SET … WHERE …` — `SELECT`-ийн `FROM … JOIN`
хэсэг `UPDATE`-ийн ард шууд орно. Энэ бол MySQL-ийн бичлэг; бусад DBMS-д
JOIN-той UPDATE өөрөөр бичигддэг.

Үр дүн нь өмнөхтэй ижил: SQL сурах бичиг 12 → 9, Ааруул 200 → 195.
Өөрчлөхөөсөө өмнө ижил `JOIN`, `WHERE`-тэй `SELECT` бичиж шалгаад,
`START TRANSACTION` … `ROLLBACK` дотор турш.

> Нэг бараа нэг захиалгад **хоёр** мөрөөр орсон бол JOIN-той UPDATE тэр
> барааг нэг л удаа өөрчилдөг — нийлбэрийг хасахгүй. `zahialgiin_mur`-ийн
> PRIMARY KEY (zahialga_id, baraa_id) нь ийм давхардлаас сэргийлдэг.
""",
            initial_code="""\
USE delguur;

-- 1. Захиалга бүрийг захиалагчийн нэртэй нь харуулах
SELECT z.zahialga_id, h.ner, z.zahialsan_ognoo, z.tuluv
FROM zahialga AS z
INNER JOIN hereglegch AS h
    ON z.hereglegch_id = h.hereglegch_id
ORDER BY z.zahialga_id;

-- 2. Бараа ба ангиллын нэр (ner багана хоёуланд байгаа тул товч нэр заавал)
SELECT b.ner AS baraa, a.ner AS angilal, b.une
FROM baraa AS b
JOIN angilal AS a ON b.angilal_id = a.angilal_id
ORDER BY a.ner, b.une DESC;

-- 3. Холбосны дараа шүүх: Улаанбаатарын хүргэгдсэн захиалгууд
SELECT z.zahialga_id, h.ner, h.hot, z.tuluv
FROM zahialga AS z
JOIN hereglegch AS h ON z.hereglegch_id = h.hereglegch_id
WHERE h.hot = 'Улаанбаатар'
  AND z.tuluv = 'Хүргэгдсэн';

-- 4. USING товчлол: хоёр хүснэгтэд ижил нэртэй багана
SELECT z.zahialga_id, h.ner
FROM zahialga AS z
JOIN hereglegch AS h USING (hereglegch_id);

-- 5. Хуучин таслалтай бичлэг: ажиллана, гэхдээ бүү хэрэглэ
SELECT z.zahialga_id, h.ner
FROM zahialga AS z, hereglegch AS h
WHERE z.hereglegch_id = h.hereglegch_id;

-- 6. WHERE мартвал юу болох вэ: 10 x 8 = 80 мөр
SELECT COUNT(*) AS mur_too
FROM zahialga AS z, hereglegch AS h;

-- 7. JOIN-той UPDATE: захиалга 9-ийн мөрүүдээр үлдэгдэл хасах
--    Эхлээд ижил JOIN-той SELECT-ээр шалгана
SELECT b.baraa_id, b.ner, b.uldegdel, zm.too,
       b.uldegdel - zm.too AS shine_uldegdel
FROM baraa AS b
JOIN zahialgiin_mur AS zm ON zm.baraa_id = b.baraa_id
WHERE zm.zahialga_id = 9;

START TRANSACTION;

UPDATE baraa AS b
JOIN zahialgiin_mur AS zm ON zm.baraa_id = b.baraa_id
SET b.uldegdel = b.uldegdel - zm.too
WHERE zm.zahialga_id = 9;

SELECT baraa_id, ner, uldegdel FROM baraa WHERE baraa_id IN (7, 10);   -- 9, 195

ROLLBACK;   -- delguur-ийн өгөгдлийг анхны байдалд нь буцаана
""",
        ),
        LessonSpec(
            title="LEFT ба RIGHT JOIN",
            slug="left-right-join",
            description="Тохиролгүй мөрүүдийг хадгалах гадаад холболт.",
            duration=600,
            language=MY,
            content="""\
`INNER JOIN` нь тохиролгүй мөрийг хаядаг. Харин «захиалга **хийгээгүй**
хэрэглэгч хэн бэ» гэсэн асуултад яг тэр хаягдсан мөрүүд хэрэгтэй.

### LEFT JOIN

**Зүүн** хүснэгтийн (`FROM` дээрх) **бүх** мөрийг хадгална. Баруун талд
тохирол олдоогүй бол баруун хүснэгтийн баганууд `NULL` болно.

```sql
SELECT h.hereglegch_id, h.ner, z.zahialga_id
FROM hereglegch AS h
LEFT JOIN zahialga AS z
    ON z.hereglegch_id = h.hereglegch_id
ORDER BY h.hereglegch_id;
```

| hereglegch_id | ner | zahialga_id |
|---|---|---|
| 1 | Болд | 1 |
| 1 | Болд | 3 |
| 1 | Болд | 10 |
| … | … | … |
| 7 | Энх | 9 |
| 8 | Мөнх | NULL |

`LEFT JOIN` ба `LEFT OUTER JOIN` нь нэг зүйл.

### Тохиролгүй мөрийг олох: `IS NULL` загвар

```sql
SELECT h.hereglegch_id, h.ner
FROM hereglegch AS h
LEFT JOIN zahialga AS z ON z.hereglegch_id = h.hereglegch_id
WHERE z.zahialga_id IS NULL;
```

Үр дүн: **Мөнх** (8). Шалгахдаа баруун хүснэгтийн `NOT NULL` багана
(ихэвчлэн үндсэн түлхүүр) ашигла — жинхэнэ `NULL` утгатай баганаар
шалгавал буруу үр дүн гарна.

Хэзээ ч захиалагдаагүй бараа:

```sql
SELECT b.baraa_id, b.ner
FROM baraa AS b
LEFT JOIN zahialgiin_mur AS m ON m.baraa_id = b.baraa_id
WHERE m.baraa_id IS NULL;
```

Үр дүн: **Гутал** (5).

### COUNT(*) ба COUNT(багана)

```sql
SELECT h.ner, COUNT(*) AS buruu, COUNT(z.zahialga_id) AS zuv
FROM hereglegch AS h
LEFT JOIN zahialga AS z ON z.hereglegch_id = h.hereglegch_id
GROUP BY h.hereglegch_id, h.ner;
```

Мөнхийн хувьд `COUNT(*)` = **1** (NULL-тай мөрийг тоолно), харин
`COUNT(z.zahialga_id)` = **0**. Гадаад холболтын дараа баганаар тоол.

### Нөхцөл `ON` дотор уу, `WHERE` дотор уу

INNER JOIN-д ялгаагүй. LEFT JOIN-д **огт өөр** үр дүн өгнө:

```sql
-- A: нөхцөл ON дотор
SELECT h.ner, COUNT(z.zahialga_id) AS hurgegdsen
FROM hereglegch AS h
LEFT JOIN zahialga AS z
    ON z.hereglegch_id = h.hereglegch_id
   AND z.tuluv = 'Хүргэгдсэн'
GROUP BY h.hereglegch_id, h.ner;

-- B: нөхцөл WHERE дотор
SELECT h.ner, COUNT(z.zahialga_id) AS hurgegdsen
FROM hereglegch AS h
LEFT JOIN zahialga AS z ON z.hereglegch_id = h.hereglegch_id
WHERE z.tuluv = 'Хүргэгдсэн'
GROUP BY h.hereglegch_id, h.ner;
```

| | Мөрийн тоо | Тэмүүлэн, Энх, Мөнх |
|---|---|---|
| A (`ON`) | 8 | 0 гэж гарна |
| B (`WHERE`) | 5 | **алга болно** |

`ON` нь «аль мөрийг **холбох** вэ» гэдгийг, `WHERE` нь «холбосны дараа
аль мөрийг **үлдээх** вэ» гэдгийг шийднэ. B хувилбарт `z.tuluv` нь NULL
мөрүүд `WHERE`-ээр шүүгдэж, LEFT JOIN нь INNER JOIN болж хувирдаг.

> Дүрэм: LEFT JOIN-ийн **баруун** хүснэгтийн шүүлтийг `ON` дотор, **зүүн**
> хүснэгтийн шүүлтийг `WHERE` дотор бич.

### RIGHT JOIN

**Баруун** хүснэгтийн бүх мөрийг хадгална:

```sql
SELECT b.ner, m.zahialga_id
FROM zahialgiin_mur AS m
RIGHT JOIN baraa AS b ON m.baraa_id = b.baraa_id;
```

Энэ нь хүснэгтийн байрыг сольсон `baraa LEFT JOIN zahialgiin_mur`-тэй
яг адил. Ихэнх баг зөвхөн `LEFT JOIN` бичдэг — «үндсэн хүснэгт зүүн талд»
гэсэн нэг загвар уншихад хялбар.

`LEFT` ба `RIGHT JOIN`-ийг нэгтгэвэл хоёр талын бүх мөрийг авч болно —
MySQL-д шууд байхгүй `FULL OUTER JOIN`-ийг дараагийн хичээлд ингэж
дуурайна.
""",
            initial_code="""\
USE delguur;

-- 1. Бүх хэрэглэгч, захиалгатай нь (захиалгагүй бол NULL)
SELECT h.hereglegch_id, h.ner, z.zahialga_id, z.tuluv
FROM hereglegch AS h
LEFT JOIN zahialga AS z
    ON z.hereglegch_id = h.hereglegch_id
ORDER BY h.hereglegch_id, z.zahialga_id;

-- 2. Захиалга хийгээгүй хэрэглэгч (Мөнх гарна)
SELECT h.hereglegch_id, h.ner
FROM hereglegch AS h
LEFT JOIN zahialga AS z ON z.hereglegch_id = h.hereglegch_id
WHERE z.zahialga_id IS NULL;

-- 3. Хэзээ ч захиалагдаагүй бараа (Гутал гарна)
SELECT b.baraa_id, b.ner
FROM baraa AS b
LEFT JOIN zahialgiin_mur AS m ON m.baraa_id = b.baraa_id
WHERE m.baraa_id IS NULL;

-- 4. COUNT(*) нь NULL мөрийг тоолдог тул Мөнхөд 1 гэж гарна
SELECT h.ner,
       COUNT(*) AS buruu_too,
       COUNT(z.zahialga_id) AS zuv_too
FROM hereglegch AS h
LEFT JOIN zahialga AS z ON z.hereglegch_id = h.hereglegch_id
GROUP BY h.hereglegch_id, h.ner
ORDER BY h.hereglegch_id;

-- 5A. Нөхцөл ON дотор: 8 хэрэглэгч бүгд үлдэнэ
SELECT h.ner, COUNT(z.zahialga_id) AS hurgegdsen
FROM hereglegch AS h
LEFT JOIN zahialga AS z
    ON z.hereglegch_id = h.hereglegch_id
   AND z.tuluv = 'Хүргэгдсэн'
GROUP BY h.hereglegch_id, h.ner
ORDER BY h.hereglegch_id;

-- 5B. Нөхцөл WHERE дотор: 5 мөр л үлдэнэ (INNER JOIN болж хувирав)
SELECT h.ner, COUNT(z.zahialga_id) AS hurgegdsen
FROM hereglegch AS h
LEFT JOIN zahialga AS z ON z.hereglegch_id = h.hereglegch_id
WHERE z.tuluv = 'Хүргэгдсэн'
GROUP BY h.hereglegch_id, h.ner
ORDER BY h.hereglegch_id;

-- 6. RIGHT JOIN ба түүнтэй адил LEFT JOIN
SELECT b.ner, m.zahialga_id
FROM zahialgiin_mur AS m
RIGHT JOIN baraa AS b ON m.baraa_id = b.baraa_id
ORDER BY b.baraa_id;

SELECT b.ner, m.zahialga_id
FROM baraa AS b
LEFT JOIN zahialgiin_mur AS m ON m.baraa_id = b.baraa_id
ORDER BY b.baraa_id;
""",
        ),
        LessonSpec(
            title="FULL OUTER (дуурайх), SELF ба CROSS JOIN",
            slug="full-self-cross-join",
            description="Хоёр талын бүх мөр, хүснэгтийг өөртэй нь холбох, декартын үржвэр.",
            duration=660,
            language=MY,
            content="""\
### FULL OUTER JOIN — MySQL-д байхгүй

`FULL OUTER JOIN` нь **хоёр** талын бүх мөрийг хадгалдаг: тохирсон мөрүүд
нийлж, аль нэг талд тохиролгүй мөрийн нөгөө талын баганууд `NULL` болно.
SQL стандартад байдаг ч **MySQL үүнийг дэмждэггүй** — бичвэл синтакс алдаа
(1064). Оронд нь `LEFT JOIN` ба `RIGHT JOIN` хоёрын үр дүнг нэгтгэж
**дуурайна**.

Жишээ: 2024 оны 1-р улиралд (4-р сараас өмнө) болон 2-р улиралд захиалга
хийсэн хэрэглэгчдийг харьцуулъя. Эхлээд улирал бүрийн захиалагчдыг
Модул 6-ийн `CREATE TABLE … AS SELECT`-ээр хоёр түр хүснэгтэд хуулна:

```sql
CREATE TABLE tur_uliral1 AS
SELECT DISTINCT hereglegch_id FROM zahialga
WHERE zahialsan_ognoo < '2024-04-01';    -- 1, 2, 3

CREATE TABLE tur_uliral2 AS
SELECT DISTINCT hereglegch_id FROM zahialga
WHERE zahialsan_ognoo >= '2024-04-01';   -- 1, 2, 4, 5, 6, 7
```

### UNION ALL — хоёр үр дүнг залгах

Дуурайлтад хоёр `SELECT`-ийн мөрүүдийг **нэг үр дүнд** залгах хэрэгтэй.
Үүнийг `UNION ALL` хийнэ (Модул 11-д нарийн үзнэ):

```sql
SELECT 'А' AS useg
UNION ALL
SELECT 'Б';
```

- Эхний `SELECT`-ийн мөрүүдийн **доор** хоёр дахийнх нь залгагдана.
- Хоёр `SELECT`-ийн **баганын тоо** ижил байх ёстой.
- Баганын нэрийг **эхний** `SELECT`-ээс авна.
- `ALL`-гүй `UNION` нь давхардсан мөрийг арилгана.

### Дуурайлт: LEFT JOIN + UNION ALL + RIGHT JOIN

```sql
SELECT u1.hereglegch_id AS uliral1, u2.hereglegch_id AS uliral2
FROM tur_uliral1 AS u1
LEFT JOIN tur_uliral2 AS u2 ON u1.hereglegch_id = u2.hereglegch_id
UNION ALL
SELECT u1.hereglegch_id, u2.hereglegch_id
FROM tur_uliral1 AS u1
RIGHT JOIN tur_uliral2 AS u2 ON u1.hereglegch_id = u2.hereglegch_id
WHERE u1.hereglegch_id IS NULL;
```

| uliral1 | uliral2 |
|---|---|
| 1 | 1 |
| 2 | 2 |
| 3 | NULL |
| NULL | 4 |
| NULL | 5 |
| NULL | 6 |
| NULL | 7 |

- Эхний хэсэг (`LEFT JOIN`) хоёр улиралд байгаа болон зөвхөн 1-р улиралд
  байгааг өгнө.
- Хоёр дахь хэсэг (`RIGHT JOIN`) дотроос `WHERE u1… IS NULL` нь зөвхөн 2-р
  улиралд байгааг л үлдээнэ — үгүй бол хоёуланд байгаа Болд, Сараа хоёр
  **давхар** гарна.

Болд, Сараа хоёр улиралд хоёуланд нь; Тэмүүлэн зөвхөн 1-р улиралд; 4–7
зөвхөн 2-р улиралд захиалсан.

> `WHERE`-гүйгээр `UNION` (ALL-гүй) бичиж давхардлыг арилгах арга ч
> түгээмэл. Гэхдээ `UNION` нь жинхэнэ давхардсан мөрийг ч нийлүүлдэг тул
> `UNION ALL` + `IS NULL` нь илүү нарийн.

Зөвхөн **нэг** улиралд захиалсан хэрэглэгчид: хэсэг бүрт нөгөө талыг нь
`IS NULL`-оор шүүнэ:

```sql
SELECT u1.hereglegch_id AS uliral1, u2.hereglegch_id AS uliral2
FROM tur_uliral1 AS u1
LEFT JOIN tur_uliral2 AS u2 ON u1.hereglegch_id = u2.hereglegch_id
WHERE u2.hereglegch_id IS NULL
UNION ALL
SELECT u1.hereglegch_id, u2.hereglegch_id
FROM tur_uliral1 AS u1
RIGHT JOIN tur_uliral2 AS u2 ON u1.hereglegch_id = u2.hereglegch_id
WHERE u1.hereglegch_id IS NULL;
```

### SELF JOIN — хүснэгтийг өөртэй нь

`ajiltan.menejer_id` нь **мөн л** `ajiltan` хүснэгтийг заана. Нэг
хүснэгтийг хоёр өөр товч нэрээр холбоно:

```sql
SELECT a.ner AS ajiltan,
       a.alban_tushaal,
       m.ner AS menejer
FROM ajiltan AS a
LEFT JOIN ajiltan AS m ON a.menejer_id = m.ajiltan_id;
```

| ajiltan | menejer |
|---|---|
| Батбаяр | NULL |
| Оюунаа | Батбаяр |
| Ганзориг | Батбаяр |
| Солонго | Оюунаа |
| Тэмүүжин | Оюунаа |
| Цэцэг | Ганзориг |

Захирал `menejer_id = NULL` тул `INNER JOIN` бичвэл тэр алга болно —
`LEFT JOIN` ашигласан шалтгаан нь энэ. Товч нэр **заавал** — өөрөөр
аль «хувилбар» гэдгийг ялгах боломжгүй.

Ижил албан тушаалтай хос ажилтан (`<` нь хос бүрийг нэг удаа гаргана):

```sql
SELECT x.ner, y.ner, x.alban_tushaal
FROM ajiltan AS x
JOIN ajiltan AS y
  ON x.alban_tushaal = y.alban_tushaal
 AND x.ajiltan_id < y.ajiltan_id;
```

Үр дүн: Солонго — Тэмүүжин (Борлуулагч).

### CROSS JOIN — декартын үржвэр

Зүүн талын **мөр бүрийг** баруун талын **мөр бүртэй** хослуулна.
`ON` байхгүй.

```sql
CREATE TABLE tur_hot AS
SELECT DISTINCT hot FROM hereglegch
WHERE hot IS NOT NULL;                   -- 3 хот

SELECT a.ner AS angilal, h.hot
FROM angilal AS a
CROSS JOIN tur_hot AS h;
```

5 ангилал × 3 хот = **15** мөр. Тайланд «хоосон нүд» ч гэсэн бүх
хослолыг гаргах, огноо × бараа гэх мэт хүснэгт үүсгэхэд хэрэглэнэ.

> CROSS JOIN-ийн мөрийн тоо хурдан өсдөг: 10 000 × 10 000 = 100 сая.
> Санаатай үед л хэрэглэ.
""",
            initial_code="""\
USE delguur;

-- 0. Улирал бүрийн захиалагчид, хотуудыг түр хүснэгтэд хуулах
--    (CREATE TABLE … AS SELECT — Модул 6)
DROP TABLE IF EXISTS tur_uliral1, tur_uliral2, tur_hot;

CREATE TABLE tur_uliral1 AS
SELECT DISTINCT hereglegch_id FROM zahialga
WHERE zahialsan_ognoo < '2024-04-01';

CREATE TABLE tur_uliral2 AS
SELECT DISTINCT hereglegch_id FROM zahialga
WHERE zahialsan_ognoo >= '2024-04-01';

CREATE TABLE tur_hot AS
SELECT DISTINCT hot FROM hereglegch
WHERE hot IS NOT NULL;

-- 1. UNION ALL: хоёр SELECT-ийн мөрийг нэг үр дүнд залгана
SELECT 'А' AS useg
UNION ALL
SELECT 'Б';

-- 2. FULL OUTER JOIN-ийг дуурайх: LEFT JOIN + UNION ALL + RIGHT JOIN
SELECT u1.hereglegch_id AS uliral1, u2.hereglegch_id AS uliral2
FROM tur_uliral1 AS u1
LEFT JOIN tur_uliral2 AS u2 ON u1.hereglegch_id = u2.hereglegch_id
UNION ALL
SELECT u1.hereglegch_id, u2.hereglegch_id
FROM tur_uliral1 AS u1
RIGHT JOIN tur_uliral2 AS u2 ON u1.hereglegch_id = u2.hereglegch_id
WHERE u1.hereglegch_id IS NULL;

-- 3. Зөвхөн нэг улиралд захиалсан хэрэглэгчид
SELECT u1.hereglegch_id AS uliral1, u2.hereglegch_id AS uliral2
FROM tur_uliral1 AS u1
LEFT JOIN tur_uliral2 AS u2 ON u1.hereglegch_id = u2.hereglegch_id
WHERE u2.hereglegch_id IS NULL
UNION ALL
SELECT u1.hereglegch_id, u2.hereglegch_id
FROM tur_uliral1 AS u1
RIGHT JOIN tur_uliral2 AS u2 ON u1.hereglegch_id = u2.hereglegch_id
WHERE u1.hereglegch_id IS NULL;

-- 4. SELF JOIN: ажилтан ба түүний менежер (захирлынх NULL)
SELECT a.ner AS ajiltan,
       a.alban_tushaal,
       m.ner AS menejer
FROM ajiltan AS a
LEFT JOIN ajiltan AS m ON a.menejer_id = m.ajiltan_id
ORDER BY a.ajiltan_id;

-- 5. Хоёр шат дээш: менежерийн менежер
SELECT a.ner AS ajiltan, m.ner AS menejer, mm.ner AS deed_menejer
FROM ajiltan AS a
LEFT JOIN ajiltan AS m  ON a.menejer_id = m.ajiltan_id
LEFT JOIN ajiltan AS mm ON m.menejer_id = mm.ajiltan_id
ORDER BY a.ajiltan_id;

-- 6. Ижил албан тушаалтай хос ажилтан
SELECT x.ner AS ajiltan1, y.ner AS ajiltan2, x.alban_tushaal
FROM ajiltan AS x
JOIN ajiltan AS y
  ON x.alban_tushaal = y.alban_tushaal
 AND x.ajiltan_id < y.ajiltan_id;

-- 7. CROSS JOIN: ангилал бүр x хот бүр = 15 мөр
SELECT a.ner AS angilal, h.hot
FROM angilal AS a
CROSS JOIN tur_hot AS h
ORDER BY a.ner, h.hot;

-- 8. Цэвэрлэх
DROP TABLE IF EXISTS tur_uliral1, tur_uliral2, tur_hot;
""",
        ),
        LessonSpec(
            title="Олон хүснэгт холбох",
            slug="olon-husnegt-join",
            description="Захиалга, мөр, бараа, ангиллыг нэг асуулгад холбож дүн гаргах.",
            duration=660,
            language=MY,
            content="""\
Нэг захиалгын бүрэн мэдээлэл дөрвөн хүснэгтэд тархсан:

```text
hereglegch ──< zahialga ──< zahialgiin_mur >── baraa >── angilal
```

`JOIN` бүр өмнөх үр дүн дээр **нэг** хүснэгт нэмнэ. Дараалал нь гинж
шиг — хүснэгт бүр аль хэдийн холбогдсон хүснэгттэй `ON`-оор холбогдоно.

### Захиалгын дэлгэрэнгүй

```sql
SELECT z.zahialga_id, h.ner AS hereglegch,
       b.ner AS baraa, a.ner AS angilal,
       m.too, m.negj_une,
       m.too * m.negj_une AS dun
FROM zahialga AS z
JOIN hereglegch     AS h ON h.hereglegch_id = z.hereglegch_id
JOIN zahialgiin_mur AS m ON m.zahialga_id   = z.zahialga_id
JOIN baraa          AS b ON b.baraa_id      = m.baraa_id
JOIN angilal        AS a ON a.angilal_id    = b.angilal_id
ORDER BY z.zahialga_id;
```

Захиалгын мөр бүр нэг мөр болно — нийт 19 мөр.

> `negj_une`-г `baraa.une`-ээс биш `zahialgiin_mur`-ээс ав. Барааны үнэ
> өөрчлөгдөж болно, харин захиалгын мөрд **худалдан авсан үеийн** үнэ
> хадгалагдана.

### Захиалга бүрийн нийт дүн

```sql
SELECT z.zahialga_id, h.ner,
       SUM(m.too * m.negj_une) AS niit
FROM zahialga AS z
JOIN hereglegch     AS h ON h.hereglegch_id = z.hereglegch_id
JOIN zahialgiin_mur AS m ON m.zahialga_id   = z.zahialga_id
GROUP BY z.zahialga_id, h.ner
ORDER BY z.zahialga_id;
```

| zahialga_id | ner | niit |
|---|---|---|
| 1 | Болд | 1428000.00 |
| 2 | Сараа | 217000.00 |
| 3 | Болд | 118000.00 |
| 4 | Тэмүүлэн | 3200000.00 |
| 5 | Номин | 680000.00 |
| 6 | Анар | 1620000.00 |
| 7 | Сараа | 145000.00 |
| 8 | Хулан | 290000.00 |
| 9 | Энх | 204000.00 |
| 10 | Болд | 3289000.00 |

### Хамгийн том 3 захиалга

Өмнөх асуулгын төгсгөлд `ORDER BY niit DESC LIMIT 3` гэж нэмнэ. Үр дүн:
10 (3 289 000), 4 (3 200 000), 6 (1 620 000).

### Ангиллаар борлуулалт (цуцлагдсаныг хасаж)

```sql
SELECT a.ner AS angilal,
       SUM(m.too * m.negj_une) AS borluulalt
FROM angilal AS a
JOIN baraa          AS b ON b.angilal_id  = a.angilal_id
JOIN zahialgiin_mur AS m ON m.baraa_id    = b.baraa_id
JOIN zahialga       AS z ON z.zahialga_id = m.zahialga_id
WHERE z.tuluv <> 'Цуцлагдсан'
GROUP BY a.angilal_id, a.ner
ORDER BY borluulalt DESC;
```

Электроник 6 056 000-аар тэргүүлнэ (цуцлагдсан 4-р захиалгын
3 200 000 хасагдсан).

### LEFT ба INNER JOIN холилдох урхи

```sql
SELECT h.ner, m.baraa_id
FROM hereglegch AS h
LEFT JOIN zahialga  AS z ON z.hereglegch_id = h.hereglegch_id
JOIN zahialgiin_mur AS m ON m.zahialga_id   = z.zahialga_id;
```

Мөнхийн мөр `LEFT JOIN`-ээр хадгалагдсан ч `z.zahialga_id = NULL` тул
дараагийн **INNER** `JOIN` түүнийг хаяна. Гинжний дагуу тохиролгүй мөр
хадгалах бол **дараагийн холболтууд ч** `LEFT JOIN` байх ёстой.

### Холболтын тоо ба мөрийн тоо

- Нэг-олон холболт мөрийг **олшруулна**: 10 захиалга → 19 захиалгын мөр.
- `SUM`-ийг олшруулсан мөр дээр хийхдээ болгоомжтой: захиалга бүрт
  хоёр мөр байхад `zahialga`-ийн нэг утгыг нэмбэл хоёр удаа тоологдоно.
- Тоо сэжигтэй бол эхлээд `COUNT(*)`-аар мөрийн тоогоо шалга.
""",
            initial_code="""\
USE delguur;

-- 1. Захиалгын мөр бүрийг бүрэн мэдээлэлтэй нь (5 хүснэгт)
SELECT z.zahialga_id, h.ner AS hereglegch,
       b.ner AS baraa, a.ner AS angilal,
       m.too, m.negj_une,
       m.too * m.negj_une AS dun
FROM zahialga AS z
JOIN hereglegch     AS h ON h.hereglegch_id = z.hereglegch_id
JOIN zahialgiin_mur AS m ON m.zahialga_id   = z.zahialga_id
JOIN baraa          AS b ON b.baraa_id      = m.baraa_id
JOIN angilal        AS a ON a.angilal_id    = b.angilal_id
ORDER BY z.zahialga_id, b.baraa_id;

-- 2. Захиалга бүрийн нийт дүн
SELECT z.zahialga_id, h.ner,
       SUM(m.too * m.negj_une) AS niit
FROM zahialga AS z
JOIN hereglegch     AS h ON h.hereglegch_id = z.hereglegch_id
JOIN zahialgiin_mur AS m ON m.zahialga_id   = z.zahialga_id
GROUP BY z.zahialga_id, h.ner
ORDER BY z.zahialga_id;

-- 3. Хамгийн том 3 захиалга
SELECT z.zahialga_id, h.ner,
       SUM(m.too * m.negj_une) AS niit
FROM zahialga AS z
JOIN hereglegch     AS h ON h.hereglegch_id = z.hereglegch_id
JOIN zahialgiin_mur AS m ON m.zahialga_id   = z.zahialga_id
GROUP BY z.zahialga_id, h.ner
ORDER BY niit DESC
LIMIT 3;

-- 4. Ангиллаар борлуулалт, цуцлагдсан захиалгыг хасаж
SELECT a.ner AS angilal,
       SUM(m.too * m.negj_une) AS borluulalt
FROM angilal AS a
JOIN baraa          AS b ON b.angilal_id  = a.angilal_id
JOIN zahialgiin_mur AS m ON m.baraa_id    = b.baraa_id
JOIN zahialga       AS z ON z.zahialga_id = m.zahialga_id
WHERE z.tuluv <> 'Цуцлагдсан'
GROUP BY a.angilal_id, a.ner
ORDER BY borluulalt DESC;

-- 5. Хэрэглэгч бүрийн нийт худалдан авалт
--    Захиалгагүй Мөнх: zahialga_too 0, niit NULL (нэмэх мөр байхгүй)
SELECT h.ner,
       COUNT(DISTINCT z.zahialga_id) AS zahialga_too,
       SUM(m.too * m.negj_une) AS niit
FROM hereglegch AS h
LEFT JOIN zahialga       AS z ON z.hereglegch_id = h.hereglegch_id
LEFT JOIN zahialgiin_mur AS m ON m.zahialga_id   = z.zahialga_id
GROUP BY h.hereglegch_id, h.ner
ORDER BY niit DESC;

-- 6. Урхи: LEFT JOIN-ий дараах INNER JOIN нь Мөнхийг хаяна
SELECT h.ner, m.baraa_id
FROM hereglegch AS h
LEFT JOIN zahialga  AS z ON z.hereglegch_id = h.hereglegch_id
JOIN zahialgiin_mur AS m ON m.zahialga_id   = z.zahialga_id
ORDER BY h.hereglegch_id;
""",
        ),
    ],
)

SUBQUERIES = ModuleSpec(
    title="Модул 10 — Дэд асуулга",
    description="Асуулга дотор асуулга: WHERE, FROM, SELECT хэсэгт.",
    lessons=[
        LessonSpec(
            title="Скаляр ба IN дэд асуулга",
            slug="scalar-in-ded-asuulga",
            description="Нэг утга эсвэл жагсаалт буцаадаг дэд асуулга.",
            duration=600,
            language=MY,
            content="""\
**Дэд асуулга** (subquery) нь хаалтан доторх бүтэн `SELECT`. Гадаад асуулга
түүний үр дүнг утга, жагсаалт эсвэл хүснэгт мэт ашиглана.

### Скаляр дэд асуулга — нэг утга

«Дундаж үнээс үнэтэй бараа» — дундажийг урьдчилан мэдэхгүй:

```sql
SELECT baraa_id, ner, une
FROM baraa
WHERE une > (SELECT AVG(une) FROM baraa);
```

Дундаж үнэ = 5 755 500 / 12 = **479 625**. Үр дүн: Ухаалаг утас,
Зөөврийн компьютер, Тоос сорогч.

`WHERE` дотор `AVG(une)` шууд бичиж **болохгүй** — агрегат функц `WHERE`
дотор зөвшөөрөгдөхгүй. Дэд асуулга яг энэ асуудлыг шийднэ.

Скаляр дэд асуулгыг `SELECT` жагсаалтад ч хэрэглэж болно:

```sql
SELECT ner, une,
       une - (SELECT AVG(une) FROM baraa) AS dundjaas_zoruu
FROM baraa;
```

### Олон мөр буцаавал

Скаляр байх ёстой газарт дэд асуулга 2+ мөр буцаавал ажиллах үед алдаа:
`ERROR 1242: Subquery returns more than 1 row`.

0 мөр буцаавал алдаа биш — утга нь `NULL` болно.

### IN дэд асуулга — жагсаалт

Электроник (ангилал 1) бараа захиалсан хэрэглэгчид:

```sql
SELECT hereglegch_id, ner
FROM hereglegch
WHERE hereglegch_id IN (
    SELECT z.hereglegch_id
    FROM zahialga AS z
    JOIN zahialgiin_mur AS m ON m.zahialga_id = z.zahialga_id
    JOIN baraa AS b ON b.baraa_id = m.baraa_id
    WHERE b.angilal_id = 1
);
```

Үр дүн: Болд, Сараа, Тэмүүлэн, Анар. Дэд асуулга нэг хэрэглэгчийг хэд
хэдэн удаа буцаасан ч `IN` нь гадаад мөрийг **нэг л удаа** гаргана —
`JOIN`-оос ялгаатай нь давхардал үүсгэхгүй.

Дэд асуулга нэг баганатай байх ёстой.

### NOT IN

```sql
SELECT baraa_id, ner
FROM baraa
WHERE baraa_id NOT IN (SELECT baraa_id FROM zahialgiin_mur);
```

Үр дүн: Гутал. Энд `zahialgiin_mur.baraa_id` нь `NOT NULL` тул аюулгүй.

> Дэд асуулга **NULL** буцааж болох бол `NOT IN` хоосон үр дүн өгдөг.
> Энэ урхийг дараагийн хичээлд үзнэ.

### ANY ба ALL

```sql
-- Бүх номноос үнэтэй бараа
SELECT ner, une FROM baraa
WHERE une > ALL (SELECT une FROM baraa WHERE angilal_id = 3);
```

Номын хамгийн өндөр үнэ 48 000 — түүнээс үнэтэй 7 бараа гарна.
`> ANY (...)` нь «ядаж нэгээс их» гэсэн утгатай. `= ANY` нь `IN`-тэй адил.

### MySQL-ийн хоёр хязгаарлалт

- `IN (...)`, `ALL`, `ANY` дэд асуулга дотор `LIMIT` бичиж **болохгүй**:
  `ERROR 1235: This version of MySQL doesn't yet support 'LIMIT &
  IN/ALL/ANY/SOME subquery'`. Ийм үед дэд асуулгыг `FROM`-д (энэ модулийн
  3-р хичээл) эсвэл `JOIN` болгож бичнэ.
- Дэд асуулга доторх `LIMIT`-гүй `ORDER BY` ихэвчлэн **үл тоомсорлогдоно**
  — үр дүнгийн дараалал зөвхөн гадаад асуулгын `ORDER BY`-оос хамаарна.
""",
            initial_code="""\
USE delguur;

-- 1. Дундаж үнэ хэд вэ
SELECT AVG(une) AS dundaj FROM baraa;

-- 2. Дунджаас үнэтэй бараа (скаляр дэд асуулга)
SELECT baraa_id, ner, une
FROM baraa
WHERE une > (SELECT AVG(une) FROM baraa)
ORDER BY une DESC;

-- 3. Хамгийн үнэтэй бараа
SELECT ner, une
FROM baraa
WHERE une = (SELECT MAX(une) FROM baraa);

-- 4. Скаляр дэд асуулга SELECT жагсаалтад
SELECT ner, une,
       une - (SELECT AVG(une) FROM baraa) AS dundjaas_zoruu
FROM baraa
ORDER BY dundjaas_zoruu DESC;

-- 5. Электроник бараа захиалсан хэрэглэгчид (IN)
SELECT hereglegch_id, ner
FROM hereglegch
WHERE hereglegch_id IN (
    SELECT z.hereglegch_id
    FROM zahialga AS z
    JOIN zahialgiin_mur AS m ON m.zahialga_id = z.zahialga_id
    JOIN baraa AS b ON b.baraa_id = m.baraa_id
    WHERE b.angilal_id = 1
);

-- 6. Мөн адил, гэхдээ цуцлагдсан захиалгыг тооцохгүй (Тэмүүлэн хасагдана)
SELECT hereglegch_id, ner
FROM hereglegch
WHERE hereglegch_id IN (
    SELECT z.hereglegch_id
    FROM zahialga AS z
    JOIN zahialgiin_mur AS m ON m.zahialga_id = z.zahialga_id
    JOIN baraa AS b ON b.baraa_id = m.baraa_id
    WHERE b.angilal_id = 1
      AND z.tuluv <> 'Цуцлагдсан'
);

-- 7. Хэзээ ч захиалагдаагүй бараа (NOT IN, NULL байхгүй тул аюулгүй)
SELECT baraa_id, ner
FROM baraa
WHERE baraa_id NOT IN (SELECT baraa_id FROM zahialgiin_mur);

-- 8. Бүх номноос үнэтэй бараа (ALL)
SELECT ner, une
FROM baraa
WHERE une > ALL (SELECT une FROM baraa WHERE angilal_id = 3)
ORDER BY une;
""",
        ),
        LessonSpec(
            title="EXISTS ба хамааралт дэд асуулга",
            slug="exists-correlated-ded-asuulga",
            description="Гадаад мөр бүрт ажилладаг дэд асуулга, NOT IN-ий NULL урхи.",
            duration=660,
            language=MY,
            content="""\
### Хамааралт (correlated) дэд асуулга

Өмнөх хичээлийн дэд асуулгууд **бие даасан** байсан — тусад нь ажиллуулж
болно. **Хамааралт** дэд асуулга нь гадаад асуулгын баганыг ашигладаг
тул утгын хувьд гадаад **мөр бүрт** дахин үнэлэгдэнэ.

«Өөрийн ангиллын дунджаас үнэтэй бараа»:

```sql
SELECT b.ner, b.angilal_id, b.une
FROM baraa AS b
WHERE b.une > (
    SELECT AVG(b2.une)
    FROM baraa AS b2
    WHERE b2.angilal_id = b.angilal_id   -- гадаад мөрийг заана
);
```

| ner | angilal_id | une |
|---|---|---|
| Зөөврийн компьютер | 1 | 3200000.00 |
| Гутал | 2 | 210000.00 |
| SQL сурах бичиг | 3 | 48000.00 |
| Тоос сорогч | 4 | 560000.00 |
| Ааруул | 5 | 12000.00 |

Нэг хүснэгтийг дотор, гадна хоёуланд нь ашиглаж байгаа тул товч нэр
(`b`, `b2`) **заавал**.

### EXISTS

`EXISTS (дэд асуулга)` нь дэд асуулга **ядаж нэг мөр** буцаавал `TRUE`.
Буцаасан утга нь хамаагүй — тиймээс ихэвчлэн `SELECT 1` гэж бичдэг.

```sql
-- Ядаж нэг захиалга хийсэн хэрэглэгч
SELECT h.ner
FROM hereglegch AS h
WHERE EXISTS (
    SELECT 1 FROM zahialga AS z
    WHERE z.hereglegch_id = h.hereglegch_id
);
```

7 хэрэглэгч гарна. Анхны тохирол олдмогц хайлт зогсоно.

### NOT EXISTS

```sql
SELECT h.ner
FROM hereglegch AS h
WHERE NOT EXISTS (
    SELECT 1 FROM zahialga AS z
    WHERE z.hereglegch_id = h.hereglegch_id
);
```

Үр дүн: Мөнх. Энэ нь `LEFT JOIN ... WHERE ... IS NULL` загвартай ижил
утгатай.

### NOT IN ба NULL — хамгийн аюултай урхи

«Хэнийг ч удирддаггүй ажилтан»-ыг олъё. Менежерүүд нь `menejer_id`
баганад байгаа хүмүүс:

```sql
SELECT ner FROM ajiltan
WHERE ajiltan_id NOT IN (SELECT menejer_id FROM ajiltan);
```

Хүлээгдэж буй үр дүн: Солонго, Тэмүүжин, Цэцэг. Бодит үр дүн: **0 мөр!**

Шалтгаан: Батбаяр захирлын `menejer_id` нь `NULL`. Жишээ нь Солонгын
хувьд `4 NOT IN (1, 1, 2, 2, 3, NULL)` нь
`4 <> 1 AND ... AND 4 <> NULL` гэсэн утгатай. `4 <> NULL` нь `UNKNOWN`,
тиймээс бүх илэрхийлэл хэзээ ч `TRUE` болохгүй.

| Бичлэг | Дэд асуулгад NULL байвал |
|---|---|
| `NOT IN (...)` | **Хоосон үр дүн** |
| `NOT EXISTS (...)` | Зөв ажиллана |
| `IN (...)` / `EXISTS (...)` | Хоёулаа зөв |

Засах хоёр арга:

```sql
-- 1. NOT EXISTS (зөвлөмжтэй)
SELECT a.ner FROM ajiltan AS a
WHERE NOT EXISTS (
    SELECT 1 FROM ajiltan AS d
    WHERE d.menejer_id = a.ajiltan_id
);

-- 2. NULL-ийг шүүх
SELECT ner FROM ajiltan
WHERE ajiltan_id NOT IN (
    SELECT menejer_id FROM ajiltan WHERE menejer_id IS NOT NULL
);
```

> «Байхгүй» гэсэн асуултад `NOT EXISTS` хэрэглэх зуршил тогтоо. Өнөөдөр
> NULL байхгүй багана маргааш NULL-тэй болж, `NOT IN` чимээгүй эвдэрнэ.

### Хамааралт дэд асуулга ба гүйцэтгэл

Утгын хувьд «мөр бүрт нэг удаа» гэж ойлгож болно. Бодит байдал дээр
MySQL 8 `EXISTS` / `IN`-ийг ихэвчлэн **semi-join** болгож хувиргадаг тул
хурдан. Холбогдох баганад (`zahialga.hereglegch_id`) индекс байх нь хамгийн
чухал. MySQL асуулгыг яаж гүйцэтгэхийг `EXPLAIN`-ээр харна (Модул 13).
""",
            initial_code="""\
USE delguur;

-- 1. Хамааралт дэд асуулга: өөрийн ангиллын дунджаас үнэтэй бараа
SELECT b.ner, b.angilal_id, b.une
FROM baraa AS b
WHERE b.une > (
    SELECT AVG(b2.une)
    FROM baraa AS b2
    WHERE b2.angilal_id = b.angilal_id
)
ORDER BY b.angilal_id;

-- 2. Хэрэглэгч бүрийн хамгийн сүүлийн захиалга
SELECT z.hereglegch_id, z.zahialga_id, z.zahialsan_ognoo
FROM zahialga AS z
WHERE z.zahialsan_ognoo = (
    SELECT MAX(z2.zahialsan_ognoo)
    FROM zahialga AS z2
    WHERE z2.hereglegch_id = z.hereglegch_id
)
ORDER BY z.hereglegch_id;

-- 3. EXISTS: ядаж нэг захиалга хийсэн хэрэглэгч
SELECT h.ner
FROM hereglegch AS h
WHERE EXISTS (
    SELECT 1 FROM zahialga AS z
    WHERE z.hereglegch_id = h.hereglegch_id
);

-- 4. NOT EXISTS: захиалгагүй хэрэглэгч (Мөнх)
SELECT h.ner
FROM hereglegch AS h
WHERE NOT EXISTS (
    SELECT 1 FROM zahialga AS z
    WHERE z.hereglegch_id = h.hereglegch_id
);

-- 5. EXISTS олон нөхцөлтэй: хүлээгдэж буй захиалгатай хэрэглэгч
SELECT h.ner
FROM hereglegch AS h
WHERE EXISTS (
    SELECT 1 FROM zahialga AS z
    WHERE z.hereglegch_id = h.hereglegch_id
      AND z.tuluv = 'Хүлээгдэж буй'
);

-- 6. УРХИ: menejer_id дотор NULL байгаа тул 0 мөр гарна
SELECT ner FROM ajiltan
WHERE ajiltan_id NOT IN (SELECT menejer_id FROM ajiltan);

-- 7. Засвар 1: NOT EXISTS (Солонго, Тэмүүжин, Цэцэг)
SELECT a.ner FROM ajiltan AS a
WHERE NOT EXISTS (
    SELECT 1 FROM ajiltan AS d
    WHERE d.menejer_id = a.ajiltan_id
);

-- 8. Засвар 2: NULL-ийг дэд асуулгаас шүүх
SELECT ner FROM ajiltan
WHERE ajiltan_id NOT IN (
    SELECT menejer_id FROM ajiltan WHERE menejer_id IS NOT NULL
);
""",
        ),
        LessonSpec(
            title="FROM ба SELECT доторх дэд асуулга",
            slug="derived-table-ded-asuulga",
            description="Уламжилсан хүснэгт, SELECT жагсаалтын дэд асуулга, LATERAL.",
            duration=660,
            language=MY,
            content="""\
### Уламжилсан хүснэгт (derived table)

`FROM` дотор бичсэн дэд асуулга нь **түр хүснэгт** шиг ажиллана. Нэг
алхмаар гаргах боломжгүй «агрегатын агрегат»-д хэрэгтэй.

«Хэрэглэгч бүрийн захиалгын **дундаж** дүн» — эхлээд захиалга бүрийн
дүнг, дараа нь түүний дунджийг:

```sql
SELECT d.hereglegch_id, AVG(d.niit) AS dundaj_zahialga
FROM (
    SELECT z.zahialga_id, z.hereglegch_id,
           SUM(m.too * m.negj_une) AS niit
    FROM zahialga AS z
    JOIN zahialgiin_mur AS m ON m.zahialga_id = z.zahialga_id
    GROUP BY z.zahialga_id, z.hereglegch_id
) AS d
GROUP BY d.hereglegch_id;
```

Жишээ нь Сараа (2): (217 000 + 145 000) / 2 = **181 000**.

### Дүрмүүд

| Дүрэм | MySQL |
|---|---|
| Товч нэр (`AS d`) | **Заавал** — үгүй бол `ERROR 1248: Every derived table must have its own alias` |
| Тооцоолсон баганын нэр | Нэргүй бол илэрхийлэл өөрөө нэр болно: `` `SUM(m.too * m.negj_une)` `` |
| Дотор `ORDER BY` | Зөвшөөрнө, гэхдээ дараалал баталгаагүй |

Нэргүй баганад гадаад асуулгаас хандах бараг боломжгүй. Тиймээс хүснэгт
**ба** тооцоолсон багана бүрт нэр өг: `SUM(...) AS niit`.

### Дундаас их зарцуулсан хэрэглэгч

```sql
SELECT h.ner, t.zartsuulsan
FROM (
    SELECT z.hereglegch_id, SUM(m.too * m.negj_une) AS zartsuulsan
    FROM zahialga AS z
    JOIN zahialgiin_mur AS m ON m.zahialga_id = z.zahialga_id
    GROUP BY z.hereglegch_id
) AS t
JOIN hereglegch AS h ON h.hereglegch_id = t.hereglegch_id
WHERE t.zartsuulsan > (
    SELECT AVG(t2.zartsuulsan) FROM (
        SELECT SUM(m.too * m.negj_une) AS zartsuulsan
        FROM zahialga AS z
        JOIN zahialgiin_mur AS m ON m.zahialga_id = z.zahialga_id
        GROUP BY z.hereglegch_id
    ) AS t2
);
```

Үр дүн: Болд, Тэмүүлэн, Анар. Нэг дэд асуулгыг хоёр удаа бичих нь
төвөгтэй — Модул 15-ын **CTE** (`WITH`) үүнийг цэгцэлнэ.

### SELECT жагсаалт дахь дэд асуулга

```sql
SELECT h.ner,
       (SELECT COUNT(*) FROM zahialga AS z
        WHERE z.hereglegch_id = h.hereglegch_id) AS zahialga_too,
       (SELECT MAX(z.zahialsan_ognoo) FROM zahialga AS z
        WHERE z.hereglegch_id = h.hereglegch_id) AS suuliin
FROM hereglegch AS h;
```

Хамааралт, скаляр байх ёстой (нэг мөр, нэг багана). Мөнхөд `0` ба `NULL`.

Ижил үр дүнг `JOIN` + `GROUP BY`-оор:

```sql
SELECT h.ner, COUNT(z.zahialga_id) AS zahialga_too,
       MAX(z.zahialsan_ognoo) AS suuliin
FROM hereglegch AS h
LEFT JOIN zahialga AS z ON z.hereglegch_id = h.hereglegch_id
GROUP BY h.hereglegch_id, h.ner;
```

> **Гүйцэтгэл:** `SELECT` дотор хамааралт дэд асуулга олон болох тусам
> хүснэгтийг дахин дахин уншдаг төлөвлөгөө гарах магадлал өснө. Нэг
> хүснэгтээс хэд хэдэн утга авах бол `JOIN` + `GROUP BY` ихэвчлэн
> илүү цэвэр, хурдан. Эргэлзвэл төлөвлөгөөг `EXPLAIN`-ээр хар (Модул 13).

### Мөр бүрт «шилдэг N»: LATERAL

Энгийн уламжилсан хүснэгт гадаад хүснэгтийн баганыг **харж чаддаггүй**.
`LATERAL` (MySQL 8.0.14+) гэж бичвэл `FROM` доторх дэд асуулга өмнөх
хүснэгтийн мөр бүрт ажиллаж, **олон багана, олон мөр** буцааж чадна:

```sql
-- Хэрэглэгч бүрийн сүүлийн захиалга
SELECT h.ner, s.zahialga_id, s.zahialsan_ognoo
FROM hereglegch AS h
LEFT JOIN LATERAL (
    SELECT z.zahialga_id, z.zahialsan_ognoo
    FROM zahialga AS z
    WHERE z.hereglegch_id = h.hereglegch_id
    ORDER BY z.zahialsan_ognoo DESC
    LIMIT 1
) AS s ON TRUE;
```

| Бичлэг | Тохиролгүй мөр |
|---|---|
| `CROSS JOIN LATERAL (...) AS s` | Хаягдана |
| `LEFT JOIN LATERAL (...) AS s ON TRUE` | Хадгалагдана (`NULL`-тай) |

`ON TRUE` нь «нэмэлт холбох нөхцөлгүй» гэсэн үг — холбох нөхцөл аль хэдийн
дэд асуулгын `WHERE` дотор бий.
""",
            initial_code="""\
USE delguur;

-- 1. Уламжилсан хүснэгт: захиалга бүрийн дүн, дараа нь хэрэглэгчээр дундаж
SELECT d.hereglegch_id, AVG(d.niit) AS dundaj_zahialga
FROM (
    SELECT z.zahialga_id, z.hereglegch_id,
           SUM(m.too * m.negj_une) AS niit   -- баганад нэр өг
    FROM zahialga AS z
    JOIN zahialgiin_mur AS m ON m.zahialga_id = z.zahialga_id
    GROUP BY z.zahialga_id, z.hereglegch_id
) AS d                                        -- товч нэр заавал
GROUP BY d.hereglegch_id
ORDER BY d.hereglegch_id;

-- 2. Дундаас их зарцуулсан хэрэглэгчид (Болд, Тэмүүлэн, Анар)
SELECT h.ner, t.zartsuulsan
FROM (
    SELECT z.hereglegch_id, SUM(m.too * m.negj_une) AS zartsuulsan
    FROM zahialga AS z
    JOIN zahialgiin_mur AS m ON m.zahialga_id = z.zahialga_id
    GROUP BY z.hereglegch_id
) AS t
JOIN hereglegch AS h ON h.hereglegch_id = t.hereglegch_id
WHERE t.zartsuulsan > (
    SELECT AVG(t2.zartsuulsan) FROM (
        SELECT SUM(m.too * m.negj_une) AS zartsuulsan
        FROM zahialga AS z
        JOIN zahialgiin_mur AS m ON m.zahialga_id = z.zahialga_id
        GROUP BY z.hereglegch_id
    ) AS t2
)
ORDER BY t.zartsuulsan DESC;

-- 3. SELECT жагсаалт дахь хамааралт дэд асуулга
SELECT h.ner,
       (SELECT COUNT(*) FROM zahialga AS z
        WHERE z.hereglegch_id = h.hereglegch_id) AS zahialga_too,
       (SELECT MAX(z.zahialsan_ognoo) FROM zahialga AS z
        WHERE z.hereglegch_id = h.hereglegch_id) AS suuliin
FROM hereglegch AS h
ORDER BY h.hereglegch_id;

-- 4. Ижил үр дүн JOIN + GROUP BY-оор
SELECT h.ner,
       COUNT(z.zahialga_id) AS zahialga_too,
       MAX(z.zahialsan_ognoo) AS suuliin
FROM hereglegch AS h
LEFT JOIN zahialga AS z ON z.hereglegch_id = h.hereglegch_id
GROUP BY h.hereglegch_id, h.ner
ORDER BY h.hereglegch_id;

-- 5. LEFT JOIN LATERAL: хэрэглэгч бүрийн сүүлийн захиалга (Мөнхөд NULL)
SELECT h.ner, s.zahialga_id, s.zahialsan_ognoo
FROM hereglegch AS h
LEFT JOIN LATERAL (
    SELECT z.zahialga_id, z.zahialsan_ognoo
    FROM zahialga AS z
    WHERE z.hereglegch_id = h.hereglegch_id
    ORDER BY z.zahialsan_ognoo DESC
    LIMIT 1
) AS s ON TRUE
ORDER BY h.hereglegch_id;

-- 6. CROSS JOIN LATERAL: захиалга бүрийн хамгийн их дүнтэй мөр
SELECT z.zahialga_id, t.baraa_id, t.dun
FROM zahialga AS z
CROSS JOIN LATERAL (
    SELECT m.baraa_id, m.too * m.negj_une AS dun
    FROM zahialgiin_mur AS m
    WHERE m.zahialga_id = z.zahialga_id
    ORDER BY dun DESC
    LIMIT 1
) AS t
ORDER BY z.zahialga_id;
""",
        ),
    ],
)

SETS_AND_CASE = ModuleSpec(
    title="Модул 11 — Олонлог ба нөхцөлт илэрхийлэл",
    description="UNION, INTERSECT, EXCEPT, CASE ба NULL-тай ажиллах функцүүд.",
    lessons=[
        LessonSpec(
            title="UNION, INTERSECT, EXCEPT",
            slug="union-intersect-except",
            description="Хоёр асуулгын үр дүнг нэгтгэх, огтлох, хасах.",
            duration=600,
            language=MY,
            content="""\
Олонлогийн үйлдлүүд нь хоёр `SELECT`-ийн **үр дүнг** мөрөөр нь нийлүүлнэ.
`JOIN` нь багана нэмдэг бол эдгээр нь **мөр** нэмж/хасна. Модул 9-д
`FULL OUTER JOIN`-ийг дуурайхдаа `UNION ALL`-ийг товч үзсэн — одоо бүрэн
судална.

Жишээнд хоёр олонлог ашиглая:

- **Q1** — 4-р сараас өмнө захиалсан хэрэглэгч: `1, 2, 1, 3` (4 мөр)
- **Q2** — 4-р сараас хойш захиалсан: `4, 5, 2, 6, 7, 1` (6 мөр)

### UNION ба UNION ALL

```sql
SELECT hereglegch_id FROM zahialga WHERE zahialsan_ognoo <  '2024-04-01'
UNION
SELECT hereglegch_id FROM zahialga WHERE zahialsan_ognoo >= '2024-04-01';
```

| Үйлдэл | Утга | Мөр |
|---|---|---|
| `UNION` | Нэгтгээд **давхардлыг устгана** | 7 (1–7) |
| `UNION ALL` | Бүгдийг нь хадгална | 10 (4 + 6) |

`UNION` давхардал хайхын тулд эрэмбэлэх/хэш хийх нэмэлт ажил хийдэг.
Давхардал **гарахгүй** гэдгийг мэдэж байвал эсвэл хэрэгтэй бол
`UNION ALL` бич — хурдан.

Бодит жишээ — хэрэглэгч ба ажилтны нэгдсэн нэрсийн жагсаалт:

```sql
SELECT ner, 'Хэрэглэгч' AS turul FROM hereglegch
UNION ALL
SELECT ner, 'Ажилтан' FROM ajiltan
ORDER BY ner;
```

### Дүрмүүд

1. `SELECT` бүр **ижил тооны** баганатай байна.
2. Харгалзах баганын төрөл **нийцтэй** байна.
3. Үр дүнгийн баганын нэрийг **эхний** `SELECT` өгнө.
4. `ORDER BY` нь **хамгийн төгсгөлд** нэг удаа бичигдэж, бүх үр дүнд
   үйлчилнэ.

Төрөл нийцэхгүй үед MySQL алдаа өгөхгүй:

```sql
SELECT ner FROM baraa
UNION ALL
SELECT une FROM baraa;
```

Бүгдийг текст болгож нэг баганад хийнэ — утгагүй үр дүн чимээгүй гарна.
Бусад зарим DBMS ийм үед алдаа өгдөг. Төрлийг өөрөө тааруул:
`CAST(une AS CHAR)`.

Нэг хэсэгт тусдаа `ORDER BY` / `LIMIT` хэрэгтэй бол тэр хэсгийг
хаалтанд хийнэ: `(SELECT ... ORDER BY une DESC LIMIT 3) UNION ALL (...)`.

### INTERSECT ба EXCEPT

```sql
-- Хоёр улиралд хоёуланд нь захиалсан: 1, 2
SELECT hereglegch_id FROM zahialga WHERE zahialsan_ognoo <  '2024-04-01'
INTERSECT
SELECT hereglegch_id FROM zahialga WHERE zahialsan_ognoo >= '2024-04-01';

-- Зөвхөн 1-р улиралд захиалсан: 3
SELECT hereglegch_id FROM zahialga WHERE zahialsan_ognoo <  '2024-04-01'
EXCEPT
SELECT hereglegch_id FROM zahialga WHERE zahialsan_ognoo >= '2024-04-01';
```

| | MySQL |
|---|---|
| `INTERSECT`, `EXCEPT` | **8.0.31**-ээс хойш |
| `INTERSECT ALL`, `EXCEPT ALL` | Дэмжинэ — давхардлыг хадгална |
| Oracle-ийн `MINUS` | Дэмжихгүй — `EXCEPT` бич |
| Эрэмбэ | `INTERSECT` нь `UNION` / `EXCEPT`-ээс түрүүлж үнэлэгдэнэ |

`SELECT VERSION();`-оор MySQL-ийн хувилбараа шалга. Энэ сайтын сервер
8.4 тул бүгд ажиллана.

### Хуучин MySQL дээр

```sql
-- INTERSECT-ийн оронд: EXISTS
SELECT DISTINCT a.hereglegch_id
FROM zahialga AS a
WHERE a.zahialsan_ognoo < '2024-04-01'
  AND EXISTS (SELECT 1 FROM zahialga AS b
              WHERE b.hereglegch_id = a.hereglegch_id
                AND b.zahialsan_ognoo >= '2024-04-01');

-- EXCEPT-ийн оронд: NOT EXISTS
SELECT DISTINCT a.hereglegch_id
FROM zahialga AS a
WHERE a.zahialsan_ognoo < '2024-04-01'
  AND NOT EXISTS (SELECT 1 FROM zahialga AS b
                  WHERE b.hereglegch_id = a.hereglegch_id
                    AND b.zahialsan_ognoo >= '2024-04-01');
```

`DISTINCT` заавал — `INTERSECT` / `EXCEPT` нь давхардалгүй үр дүн өгдөг.

> Ялгаа: `INTERSECT` / `EXCEPT` нь `NULL`-ийг «ижил» гэж үзэж харьцуулдаг,
> харин `=` нөхцөлтэй `EXISTS` нь `NULL`-ийг хэзээ ч тэнцүү гэж үзэхгүй.
""",
            initial_code="""\
USE delguur;

-- 1. UNION: давхардалгүй, 7 мөр
SELECT hereglegch_id FROM zahialga WHERE zahialsan_ognoo <  '2024-04-01'
UNION
SELECT hereglegch_id FROM zahialga WHERE zahialsan_ognoo >= '2024-04-01'
ORDER BY hereglegch_id;

-- 2. UNION ALL: давхардалтай, 10 мөр
SELECT hereglegch_id FROM zahialga WHERE zahialsan_ognoo <  '2024-04-01'
UNION ALL
SELECT hereglegch_id FROM zahialga WHERE zahialsan_ognoo >= '2024-04-01'
ORDER BY hereglegch_id;

-- 3. Хэрэглэгч ба ажилтны нэгдсэн жагсаалт (баганын нэр эхний SELECT-ээс)
SELECT ner, 'Хэрэглэгч' AS turul FROM hereglegch
UNION ALL
SELECT ner, 'Ажилтан' FROM ajiltan
ORDER BY ner;

-- 4. Хэсэг тус бүрт LIMIT: хаалтанд хийнэ
(SELECT ner, une FROM baraa WHERE angilal_id = 1 ORDER BY une DESC LIMIT 1)
UNION ALL
(SELECT ner, une FROM baraa WHERE angilal_id = 4 ORDER BY une DESC LIMIT 1);

-- 5. Хуучин MySQL-д тохирох INTERSECT орлуулга (1, 2)
SELECT DISTINCT a.hereglegch_id
FROM zahialga AS a
WHERE a.zahialsan_ognoo < '2024-04-01'
  AND EXISTS (SELECT 1 FROM zahialga AS b
              WHERE b.hereglegch_id = a.hereglegch_id
                AND b.zahialsan_ognoo >= '2024-04-01');

-- 6. Хуучин MySQL-д тохирох EXCEPT орлуулга (3)
SELECT DISTINCT a.hereglegch_id
FROM zahialga AS a
WHERE a.zahialsan_ognoo < '2024-04-01'
  AND NOT EXISTS (SELECT 1 FROM zahialga AS b
                  WHERE b.hereglegch_id = a.hereglegch_id
                    AND b.zahialsan_ognoo >= '2024-04-01');

-- Хувилбараа шалгах: доорх 2 асуулга MySQL 8.0.31+ шаардана
SELECT VERSION();

-- 7. INTERSECT: хоёр улиралд хоёуланд нь (1, 2)
SELECT hereglegch_id FROM zahialga WHERE zahialsan_ognoo <  '2024-04-01'
INTERSECT
SELECT hereglegch_id FROM zahialga WHERE zahialsan_ognoo >= '2024-04-01';

-- 8. EXCEPT: зөвхөн 1-р улиралд (3)
SELECT hereglegch_id FROM zahialga WHERE zahialsan_ognoo <  '2024-04-01'
EXCEPT
SELECT hereglegch_id FROM zahialga WHERE zahialsan_ognoo >= '2024-04-01';
""",
        ),
        LessonSpec(
            title="CASE илэрхийлэл",
            slug="case-ilerhiilel",
            description="Нөхцөлөөс хамаарч утга сонгох, нөхцөлт агрегат.",
            duration=600,
            language=MY,
            content="""\
`CASE` нь SQL-ийн «if / else». Утга гарах **ямар ч** газар — `SELECT`,
`WHERE`, `ORDER BY`, `GROUP BY`, агрегат функц дотор бичиж болно.

### Энгийн (simple) CASE

Нэг илэрхийллийг хэд хэдэн утгатай **тэнцүүгээр** харьцуулна:

```sql
SELECT zahialga_id,
       CASE tuluv
           WHEN 'Хүргэгдсэн'    THEN 'Дууссан'
           WHEN 'Хүлээгдэж буй' THEN 'Явцад'
           WHEN 'Цуцлагдсан'    THEN 'Цуцалсан'
           ELSE 'Тодорхойгүй'
       END AS tuluv_tovch
FROM zahialga;
```

### Хайлтын (searched) CASE

`WHEN` бүр **дурын нөхцөл** агуулна — `<`, `BETWEEN`, `IS NULL`, `AND`:

```sql
SELECT ner, une,
       CASE
           WHEN une < 50000  THEN 'Хямд'
           WHEN une < 500000 THEN 'Дунд'
           ELSE 'Үнэтэй'
       END AS une_angilal
FROM baraa;
```

| une_angilal | Бараа |
|---|---|
| Хямд | Монгол түүх, SQL сурах бичиг, Цайны аяга, Ааруул, Сүүтэй цай |
| Дунд | Чихэвч, Ноосон цамц, Гутал, Хөнжил |
| Үнэтэй | Ухаалаг утас, Зөөврийн компьютер, Тоос сорогч |

### Чухал дүрмүүд

- `WHEN`-үүд **дээрээс доош** шалгагдаж, эхний үнэн нөхцөл дээр зогсоно.
  Тиймээс `< 50000`-ийг `< 500000`-ийн **өмнө** бичсэн.
- `ELSE` байхгүй бөгөөд нэг ч нөхцөл биелэхгүй бол үр дүн **NULL**.
- Энгийн CASE нь `=` ашигладаг тул `CASE hot WHEN NULL ...` хэзээ ч
  биелэхгүй. NULL шалгахад хайлтын CASE: `WHEN hot IS NULL`.
- `THEN`-үүдийн төрөл нийцтэй байх нь зүйтэй. Нэг `THEN` тоо, нөгөө нь
  текст бол MySQL бүгдийг текст болгодог — эрэмбэлэхэд `10` нь `9`-өөс
  өмнө орж болно.

### ORDER BY дотор

Төлөвийг цагаан толгойгоор биш **утгаар** эрэмбэлэх:

```sql
SELECT zahialga_id, tuluv
FROM zahialga
ORDER BY CASE tuluv
             WHEN 'Хүлээгдэж буй' THEN 1
             WHEN 'Хүргэгдсэн'    THEN 2
             ELSE 3
         END, zahialga_id;
```

### Нөхцөлт агрегат

`SUM(CASE WHEN ... THEN 1 ELSE 0 END)` нь нэг мөрөнд хэд хэдэн тоолуур
гаргана — «pivot» тайлангийн үндэс:

```sql
SELECT h.ner,
       SUM(CASE WHEN z.tuluv = 'Хүргэгдсэн'    THEN 1 ELSE 0 END) AS hurgegdsen,
       SUM(CASE WHEN z.tuluv = 'Хүлээгдэж буй' THEN 1 ELSE 0 END) AS huleegdej,
       SUM(CASE WHEN z.tuluv = 'Цуцлагдсан'    THEN 1 ELSE 0 END) AS tsutslagdsan
FROM hereglegch AS h
JOIN zahialga AS z ON z.hereglegch_id = h.hereglegch_id
GROUP BY h.hereglegch_id, h.ner;
```

| ner | hurgegdsen | huleegdej | tsutslagdsan |
|---|---|---|---|
| Болд | 2 | 1 | 0 |
| Сараа | 1 | 1 | 0 |
| Тэмүүлэн | 0 | 0 | 1 |
| Номин | 1 | 0 | 0 |
| … | … | … | … |

`COUNT(CASE WHEN ... THEN 1 END)` ч ажиллана — `ELSE`-гүй тул NULL
болж, `COUNT` тоолохгүй.

### IF() функц

Хоёр салаатай богино хэлбэр: `IF(нөхцөл, үнэн_бол, худал_бол)`.

```sql
SELECT ner, IF(uldegdel = 0, 'Дууссан', 'Бий') AS baigaa_eseh FROM baraa;
```

MySQL-д харьцуулалт нь `1` / `0` буцаадаг тул `SUM(tuluv = 'Хүргэгдсэн')`
гэж товч бичиж болно — үнэн мөр бүр 1 нэмнэ.

> `IF()` функц ба харьцуулалтыг тоо болгож нэмэх нь MySQL-ийн онцлог.
> Бусад DBMS-д ч ажиллах код бичих бол `CASE` ашигла — SQL стандарт.
> Мөн `IF()` **функцийг** stored procedure доторх `IF … THEN … END IF`
> **тушаалтай** (Модул 16) андуурч болохгүй.
""",
            initial_code="""\
USE delguur;

-- 1. Энгийн CASE: төлөвийг богино нэр болгох
SELECT zahialga_id, tuluv,
       CASE tuluv
           WHEN 'Хүргэгдсэн'    THEN 'Дууссан'
           WHEN 'Хүлээгдэж буй' THEN 'Явцад'
           WHEN 'Цуцлагдсан'    THEN 'Цуцалсан'
           ELSE 'Тодорхойгүй'
       END AS tuluv_tovch
FROM zahialga;

-- 2. Хайлтын CASE: үнийн ангилал (дараалал чухал)
SELECT ner, une,
       CASE
           WHEN une < 50000  THEN 'Хямд'
           WHEN une < 500000 THEN 'Дунд'
           ELSE 'Үнэтэй'
       END AS une_angilal
FROM baraa
ORDER BY une;

-- 3. Үлдэгдлийн төлөв
SELECT ner, uldegdel,
       CASE
           WHEN uldegdel = 0 THEN 'Дууссан'
           WHEN uldegdel < 10 THEN 'Цөөн'
           ELSE 'Хангалттай'
       END AS nuots
FROM baraa;

-- 4. Ангилал бүрт хэдэн бараа байгааг бүлэглэх
SELECT CASE
           WHEN une < 50000  THEN 'Хямд'
           WHEN une < 500000 THEN 'Дунд'
           ELSE 'Үнэтэй'
       END AS une_angilal,
       COUNT(*) AS too
FROM baraa
GROUP BY une_angilal;

-- 5. ORDER BY дотор CASE: хүлээгдэж буйг эхэнд
SELECT zahialga_id, tuluv
FROM zahialga
ORDER BY CASE tuluv
             WHEN 'Хүлээгдэж буй' THEN 1
             WHEN 'Хүргэгдсэн'    THEN 2
             ELSE 3
         END, zahialga_id;

-- 6. Нөхцөлт агрегат: хэрэглэгч бүрийн төлөвөөр захиалгын тоо
SELECT h.ner,
       SUM(CASE WHEN z.tuluv = 'Хүргэгдсэн'    THEN 1 ELSE 0 END) AS hurgegdsen,
       SUM(CASE WHEN z.tuluv = 'Хүлээгдэж буй' THEN 1 ELSE 0 END) AS huleegdej,
       SUM(CASE WHEN z.tuluv = 'Цуцлагдсан'    THEN 1 ELSE 0 END) AS tsutslagdsan
FROM hereglegch AS h
JOIN zahialga AS z ON z.hereglegch_id = h.hereglegch_id
GROUP BY h.hereglegch_id, h.ner
ORDER BY h.hereglegch_id;

-- 7. Нийт дүнгийн хэдэн хувь нь хүргэгдсэн бэ
SELECT SUM(CASE WHEN z.tuluv = 'Хүргэгдсэн'
                THEN m.too * m.negj_une ELSE 0 END) AS hurgegdsen_dun,
       SUM(m.too * m.negj_une) AS niit_dun
FROM zahialga AS z
JOIN zahialgiin_mur AS m ON m.zahialga_id = z.zahialga_id;

-- 8. MySQL-ийн IF() ба товч бичлэг
SELECT ner, IF(uldegdel = 0, 'Дууссан', 'Бий') AS baigaa_eseh
FROM baraa;

SELECT SUM(tuluv = 'Хүргэгдсэн') AS hurgegdsen_too
FROM zahialga;
""",
        ),
        LessonSpec(
            title="NULL-тай ажиллах функцүүд",
            slug="coalesce-nullif-isnull",
            description="COALESCE, IFNULL, NULLIF ба тэгээр хуваах.",
            duration=600,
            language=MY,
            content="""\
`NULL` нь «утга байхгүй / мэдэгдэхгүй». Тайланд `NULL` харуулахын оронд
ойлгомжтой утга тавих, эсвэл тэгээр хуваахаас сэргийлэхэд эдгээр функц
хэрэгтэй.

### COALESCE — стандарт

`COALESCE(a, b, c, ...)` нь **NULL биш анхны** утгыг буцаана:

```sql
SELECT ner,
       COALESCE(utas, 'Утасгүй') AS utas,
       COALESCE(hot, utas, 'Мэдээлэлгүй') AS holboo
FROM hereglegch;
```

Сараа (2) → `Утасгүй`; Хулан (6)-ийн хот ч, утас ч NULL → `Мэдээлэлгүй`.

Модул 5-д хоосон үр дүнгийн `SUM` нь `0` биш `NULL` болдгийг харсан.
`COALESCE(SUM(uldegdel), 0)` нь үүнийг 0 болгоно.

### IFNULL ба ISNULL

| Функц | Утга |
|---|---|
| `COALESCE(a, b, ...)` | NULL биш анхны утга — аргумент хэдэн ч байж болно |
| `IFNULL(a, b)` | `a` NULL бол `b`, үгүй бол `a` — яг **хоёр** аргумент |
| `ISNULL(a)` | `a` NULL бол `1`, үгүй бол `0` — шалгалт, **орлуулга биш** |

> **Урхи:** `ISNULL` гэдэг нэр төөрөгдүүлдэг. MySQL-ийн `ISNULL(utas)` нь
> `utas IS NULL`-тэй адил шалгалт. Орлуулах гэж хоёр аргумент өгвөл
> `ERROR 1582: Incorrect parameter count in the call to native function
> 'ISNULL'`. Орлуулгад `IFNULL` эсвэл стандарт `COALESCE`.

`IFNULL` товч, `COALESCE` нь SQL стандарт бөгөөд олон аргумент авдаг —
аль алиныг нь хэрэглэж болно.

### NULLIF — тэгээр хуваахаас сэргийлэх

`NULLIF(a, b)` нь `a = b` бол `NULL`, үгүй бол `a` буцаана.

Модул 4-т MySQL тэгээр хуваахад алдааны оронд `NULL` өгдгийг үзсэн. Гэхдээ
бүх газар тийм биш:

| Хаана | `10 / 0` |
|---|---|
| `SELECT` дотор | `NULL` + анхааруулга 1365 |
| `INSERT`, `UPDATE` дотор (strict горим) | **Алдаа** 1365 `Division by 0` |

Хуваагч 0 байж болох бол `NULLIF(хуваагч, 0)` гэж бич — 0-ийг `NULL`
болгож, `x / NULL = NULL` болно. Санаа нь кодоос тод харагдаж, анхааруулга
ч гарахгүй. Гутал (5), Сүүтэй цай (11)-ны үлдэгдэл 0:

```sql
SELECT b.ner, b.uldegdel,
       COALESCE(SUM(m.too), 0) AS zarsan,
       ROUND(COALESCE(SUM(m.too), 0) / NULLIF(b.uldegdel, 0), 2) AS ergelt
FROM baraa AS b
LEFT JOIN zahialgiin_mur AS m ON m.baraa_id = b.baraa_id
GROUP BY b.baraa_id, b.ner, b.uldegdel;
```

### NULL ба мөр холбох

| Бичлэг | Нэг нь NULL бол |
|---|---|
| `CONCAT(ovog, ' ', utas)` | Бүхэлдээ **NULL** |
| `CONCAT_WS(' ', ovog, ner, utas)` | NULL-ийг **алгасна** |
| `CONCAT(ovog, ' ', COALESCE(utas, '-'))` | NULL-ийн оронд `-` |

### Агрегат ба NULL

`COUNT(*)` = 8, `COUNT(utas)` = 6 — агрегат функцууд NULL-ийг алгасна.
`AVG(x)` ба `AVG(COALESCE(x, 0))` өөр үр дүн өгч болохыг санаарай: эхнийх
нь NULL мөрийг тоолохгүй, хоёр дахь нь 0 гэж тоолно.
""",
            initial_code="""\
USE delguur;

-- 1. COALESCE: NULL биш анхны утга
SELECT ner, utas, hot,
       COALESCE(utas, 'Утасгүй') AS utas_haruulah,
       COALESCE(hot, utas, 'Мэдээлэлгүй') AS holboo
FROM hereglegch;

-- 2. IFNULL: хоёр аргументтай товч хувилбар
SELECT ner, IFNULL(hot, 'Тодорхойгүй') AS hot
FROM hereglegch;

-- 3. Хоосон нийлбэрийг 0 болгох: NULL биш 0
SELECT SUM(uldegdel) AS niilber,
       COALESCE(SUM(uldegdel), 0) AS niilber_0
FROM baraa
WHERE une > 99999999;

-- 4. NULLIF: тэнцүү бол NULL
SELECT NULLIF(5, 5) AS tentsuu, NULLIF(5, 3) AS yalgaatai;

-- 5. Тэгээр хуваах: SELECT-д NULL + анхааруулга
SELECT 10 / 0 AS teg;

-- 6. NULLIF-ээр 0-ийг NULL болгоод хуваана — анхааруулгагүй
SELECT b.ner, b.uldegdel,
       COALESCE(SUM(m.too), 0) AS zarsan,
       ROUND(COALESCE(SUM(m.too), 0) / NULLIF(b.uldegdel, 0), 2) AS ergelt
FROM baraa AS b
LEFT JOIN zahialgiin_mur AS m ON m.baraa_id = b.baraa_id
GROUP BY b.baraa_id, b.ner, b.uldegdel
ORDER BY b.baraa_id;

-- 7. Мөр холбох: CONCAT нь NULL өгнө, CONCAT_WS NULL-ийг алгасна
SELECT ner,
       CONCAT(ovog, ' ', utas) AS concat_ur_dun,
       CONCAT_WS(' ', ovog, ner, utas) AS concat_ws_ur_dun,
       CONCAT(ovog, ' ', COALESCE(utas, '-')) AS coalesce_hamt
FROM hereglegch;

-- 8. Агрегат NULL-ийг алгасна: 8, 6, 7
SELECT COUNT(*) AS bugd, COUNT(utas) AS utastai, COUNT(hot) AS hottoi
FROM hereglegch;

-- 9. INSERT доторх тэгээр хуваалт strict горимд алдаа — туршихдаа
--    тайлбарыг арилга (ERROR 1365 Division by 0):
-- CREATE TABLE tur_huvaalt (x DECIMAL(10,2));
-- INSERT INTO tur_huvaalt VALUES (10 / 0);
""",
        ),
    ],
)

SQL_JOIN_MODULES = [JOINS, SUBQUERIES, SETS_AND_CASE]
