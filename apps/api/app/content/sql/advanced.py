"""Модул 15-18 — CTE, window функц, процедур, trigger, аюулгүй байдал.

Ахисан түвшний хэсэг: нарийн асуулгыг алхамчлах, сервер дээр код
хадгалах, өгөгдлийн санг хамгаалах.
"""

from app.content.types import LessonSpec, ModuleSpec
from app.models.enums import LessonLanguage

MY = LessonLanguage.MYSQL

CTE_WINDOW = ModuleSpec(
    title="Модул 15 — CTE ба Window функц",
    description="WITH, рекурсив CTE, эрэмбэлэх функц, хуримтлагдсан дүн.",
    lessons=[
        LessonSpec(
            title="WITH — нийтлэг хүснэгтэн илэрхийлэл",
            slug="cte-with-uguulber",
            description="Нарийн query-г нэртэй алхмууд болгон задлах.",
            duration=480,
            language=MY,
            content="""\
**CTE** (Common Table Expression) нь нэг query дотор түр зуурын нэртэй
үр дүн үүсгэнэ. Дэд query-г `FROM (...)` дотор шигтгэхийн оронд эхэнд нь
нэр өгөөд бичнэ.

### Derived table ба CTE

```sql
-- Derived table: дотроос нь гадагшаа уншина
SELECT d.zahialga_id, d.dun
FROM (
    SELECT zahialga_id, SUM(too * negj_une) AS dun
    FROM zahialgiin_mur
    GROUP BY zahialga_id
) AS d
WHERE d.dun > 500000;

-- CTE: дээрээс доош уншина
WITH zahialgiin_dun AS (
    SELECT zahialga_id, SUM(too * negj_une) AS dun
    FROM zahialgiin_mur
    GROUP BY zahialga_id
)
SELECT zahialga_id, dun
FROM zahialgiin_dun
WHERE dun > 500000;
```

Үр дүн адилхан. Ялгаа нь **уншигдах байдал**: алхам бүр нэртэй болно.

### Олон CTE

Таслалаар зааглаж бичнэ. Дараагийн CTE өмнөхөө ашиглаж болно:

```sql
WITH hereglegchiin_dun AS (
    SELECT z.hereglegch_id, SUM(m.too * m.negj_une) AS niit
    FROM zahialga z
    JOIN zahialgiin_mur m ON m.zahialga_id = z.zahialga_id
    WHERE z.tuluv <> 'Цуцлагдсан'
    GROUP BY z.hereglegch_id
),
dundaj AS (
    SELECT AVG(niit) AS dundaj_dun FROM hereglegchiin_dun
)
SELECT h.ner, hd.niit
FROM hereglegchiin_dun hd
JOIN hereglegch h ON h.hereglegch_id = hd.hereglegch_id
CROSS JOIN dundaj d
WHERE hd.niit > d.dundaj_dun;
```

Цуцлагдаагүй захиалгатай 6 хэрэглэгчийн дундаж нь ойролцоогоор
1 331 833. Үүнээс их худалдан авалт хийсэн нь **Болд** (4 835 000) ба
**Анар** (1 620 000).

### CTE-ийн давуу тал

| | Derived table | CTE |
|---|---|---|
| Уншигдах байдал | Шигтгээ гүнзгийрэх тусам хэцүү | Алхам алхмаар |
| Нэг query-д дахин ашиглах | Дахин бичнэ | Нэрээр нь олон удаа |
| Рекурсив | Боломжгүй | Боломжтой (дараагийн хичээл) |
| Хүрээ | Тухайн `FROM` | Зөвхөн тухайн нэг statement |

> CTE нь **view биш**. Statement дуусмагц устана. Олон query-д хэрэгтэй
> бол view (Модул 13) эсвэл түр хүснэгт ашигла.

### MySQL-д

- CTE MySQL **8.0**-оос хойш дэмжигдэнэ.
- Optimizer CTE-г гадна асуулгад шигтгэж (merge), эсвэл нэг удаа
  тооцоолоод түр хүснэгтэд хадгалж (materialize) болно. Нэг CTE-г хоёр
  газар ашиглахад ихэвчлэн нэг л удаа тооцоологдоно.
- CTE-г `SELECT`-ээс гадна `INSERT … SELECT`, `UPDATE`, `DELETE`-ийн
  өмнө ч бичиж болно.
""",
            initial_code="""\
USE delguur;

-- 1. Нэг CTE: захиалга бүрийн нийт дүн
WITH zahialgiin_dun AS (
    SELECT zahialga_id, SUM(too * negj_une) AS dun
    FROM zahialgiin_mur
    GROUP BY zahialga_id
)
SELECT z.zahialga_id, h.ner, z.tuluv, d.dun
FROM zahialga z
JOIN hereglegch h ON h.hereglegch_id = z.hereglegch_id
JOIN zahialgiin_dun d ON d.zahialga_id = z.zahialga_id
ORDER BY d.dun DESC;

-- 2. Олон CTE: дунджаас их худалдан авалт хийсэн хэрэглэгч
WITH hereglegchiin_dun AS (
    SELECT z.hereglegch_id, SUM(m.too * m.negj_une) AS niit
    FROM zahialga z
    JOIN zahialgiin_mur m ON m.zahialga_id = z.zahialga_id
    WHERE z.tuluv <> 'Цуцлагдсан'
    GROUP BY z.hereglegch_id
),
dundaj AS (
    SELECT AVG(niit) AS dundaj_dun
    FROM hereglegchiin_dun
)
SELECT h.ner, hd.niit, ROUND(d.dundaj_dun, 0) AS dundaj
FROM hereglegchiin_dun hd
JOIN hereglegch h ON h.hereglegch_id = hd.hereglegch_id
CROSS JOIN dundaj d
WHERE hd.niit > d.dundaj_dun
ORDER BY hd.niit DESC;

-- 3. Нэг CTE-г хоёр удаа ашиглах: ангилал бүрийн дундаж үнээс үнэтэй бараа
WITH angilal_dundaj AS (
    SELECT angilal_id, AVG(une) AS dundaj_une
    FROM baraa
    GROUP BY angilal_id
)
SELECT b.ner, b.une, ROUND(ad.dundaj_une, 0) AS angilal_dundaj
FROM baraa b
JOIN angilal_dundaj ad ON ad.angilal_id = b.angilal_id
WHERE b.une > ad.dundaj_une
  AND ad.dundaj_une < (SELECT MAX(dundaj_une) FROM angilal_dundaj)
ORDER BY b.une DESC;
""",
        ),
        LessonSpec(
            title="Рекурсив CTE — шатлал",
            slug="recursive-cte",
            description="WITH RECURSIVE: ажилтны удирдлагын мод, дугаар ба огнооны цуваа.",
            duration=600,
            language=MY,
            content="""\
Рекурсив CTE нь **өөрийгөө** дууддаг. Менежер → ажилтан шиг мод бүтэцтэй
өгөгдлийг хэдэн түвшин гүн байхаас үл хамааран гаргана.

### Бүтэц

```text
WITH RECURSIVE нэр AS (
    зангуу хэсэг          -- эхлэх мөрүүд (нэг удаа)
    UNION ALL
    рекурсив хэсэг        -- өмнөх алхмын үр дүнтэй JOIN
)
SELECT ... FROM нэр;
```

- MySQL-д `RECURSIVE` түлхүүр үг **заавал**.
- `UNION ALL` (Модул 11) нь зангуу ба рекурсив хэсгийн мөрүүдийг залгана.
- Рекурсив хэсэг **өмнөх алхмын** мөрүүдтэй JOIN хийж шинэ мөр гаргана.
  Шинэ мөр гарахгүй болмогц зогсоно.

### Ажилтны шатлал

```sql
WITH RECURSIVE shatlal AS (
    SELECT ajiltan_id, ner, menejer_id,
           1 AS tuvshin,
           CAST(ner AS CHAR(500)) AS zam
    FROM ajiltan
    WHERE menejer_id IS NULL
    UNION ALL
    SELECT a.ajiltan_id, a.ner, a.menejer_id,
           s.tuvshin + 1,
           CONCAT(s.zam, ' > ', a.ner)
    FROM ajiltan a
    JOIN shatlal s ON a.menejer_id = s.ajiltan_id
)
SELECT tuvshin, ner, zam FROM shatlal ORDER BY zam;
```

Үр дүн:

| tuvshin | ner | zam |
|---|---|---|
| 1 | Батбаяр | Батбаяр |
| 2 | Ганзориг | Батбаяр > Ганзориг |
| 3 | Цэцэг | Батбаяр > Ганзориг > Цэцэг |
| 2 | Оюунаа | Батбаяр > Оюунаа |
| 3 | Солонго | Батбаяр > Оюунаа > Солонго |
| 3 | Тэмүүжин | Батбаяр > Оюунаа > Тэмүүжин |

Алхмаар: 1-р алхамд захирал (зангуу); 2-р алхамд түүний шууд доод
ажилтнууд Оюунаа, Ганзориг; 3-р алхамд тэдний доод ажилтнууд; 4-р алхамд
шинэ мөр гарахгүй тул зогсоно.

Анхны кодод модыг догол мөртэй харуулахдаа `REPEAT('    ', tuvshin - 1)`
хэрэглэнэ: `REPEAT(текст, n)` нь текстийг n удаа давтана.

### Яагаад `CAST(ner AS CHAR(500))` вэ

Баганын төрөл, урт **зангуу хэсгээс** тодорхойлогдоно. Зангуу дахь `ner`
нь `VARCHAR(100)` бол `zam` багана ч мөн 100 тэмдэгттэй болно. Зам
уртсахад strict горимд `ERROR 1406: Data too long for column 'zam'` гарна.
Тиймээс зангуунд `CAST(... AS CHAR(500))`-аар (Модул 4) урт болгож
өргөсгөнө.

### Хязгааргүй давталтаас хамгаалах

MySQL рекурсийг анхдагчаар **1000** алхмаар хязгаарладаг
(`cte_max_recursion_depth`). Хэтэрвэл алдаа 3636 өгнө. Илүү гүн рекурс
хэрэгтэй бол session-д өсгөнө:

```sql
SET SESSION cte_max_recursion_depth = 5000;
```

> Өгөгдөлд мөчлөг байвал (A-ийн менежер B, B-ийн менежер A) query хэзээ ч
> дуусахгүй — хязгаар хүрэхэд алдаа өгнө. Нэмэлт хамгаалалт болгож
> рекурсив хэсэгт `WHERE s.tuvshin < 20` нөхцөл тавь.

### Рекурсив хэсгийн хязгаарлалт

Рекурсив хэсэгт `GROUP BY`, aggregate функц, `DISTINCT`, window функц,
`ORDER BY` бичиж болохгүй (MySQL 8.0.19-өөс `LIMIT` зөвшөөрөгдсөн). Шүүлт,
эрэмбэлэлт, бүлэглэлийг гадна талын `SELECT`-д хий.

### Бусад хэрэглээ

- Ангиллын мод (эцэг ангилал → дэд ангилал)
- Дугаарын цуваа 1..N
- **Огнооны цуваа** — захиалгагүй сарыг ч тайланд харуулах (дараагийн
  хичээлд ашиглана)
""",
            initial_code="""\
USE delguur;

-- 1. Бүтэн шатлал: түвшин, зам, догол мөртэй харагдац
WITH RECURSIVE shatlal AS (
    -- Зангуу: менежергүй ажилтан буюу захирал
    SELECT ajiltan_id, ner, menejer_id,
           1 AS tuvshin,
           CAST(ner AS CHAR(500)) AS zam
    FROM ajiltan
    WHERE menejer_id IS NULL

    UNION ALL

    -- Рекурсив хэсэг: өмнөх түвшний хүмүүсийн шууд доод ажилтнууд
    SELECT a.ajiltan_id, a.ner, a.menejer_id,
           s.tuvshin + 1,
           CONCAT(s.zam, ' > ', a.ner)
    FROM ajiltan AS a
    JOIN shatlal AS s ON a.menejer_id = s.ajiltan_id
    WHERE s.tuvshin < 20              -- мөчлөгөөс хамгаалах
)
SELECT tuvshin,
       CONCAT(REPEAT('    ', tuvshin - 1), ner) AS mod_butets,
       zam
FROM shatlal
ORDER BY zam;

-- 2. Нэг менежерийн доорх бүх хүн (Оюунаа, ajiltan_id = 2)
WITH RECURSIVE doorh AS (
    SELECT ajiltan_id, ner, 0 AS gun
    FROM ajiltan
    WHERE ajiltan_id = 2

    UNION ALL

    SELECT a.ajiltan_id, a.ner, d.gun + 1
    FROM ajiltan AS a
    JOIN doorh AS d ON a.menejer_id = d.ajiltan_id
)
SELECT ajiltan_id, ner, gun
FROM doorh
WHERE gun > 0;

-- 3. Дээш чиглэсэн гинж: Цэцэг (6)-ээс захирал хүртэл
WITH RECURSIVE deesh AS (
    SELECT ajiltan_id, ner, menejer_id, 0 AS alham
    FROM ajiltan
    WHERE ajiltan_id = 6

    UNION ALL

    SELECT a.ajiltan_id, a.ner, a.menejer_id, d.alham + 1
    FROM ajiltan AS a
    JOIN deesh AS d ON a.ajiltan_id = d.menejer_id
)
SELECT alham, ner
FROM deesh
ORDER BY alham;

-- 4. Дугаарын цуваа 1..2000: анхдагч хязгаар 1000 тул session-д өсгөнө
SET SESSION cte_max_recursion_depth = 3000;

WITH RECURSIVE dugaaruud AS (
    SELECT 1 AS n
    UNION ALL
    SELECT n + 1 FROM dugaaruud WHERE n < 2000
)
SELECT COUNT(*) AS mur_too, MAX(n) AS hamgiin_ih
FROM dugaaruud;

-- 5. Огнооны цуваа: 2024 оны 1-7 сарын эхний өдрүүд
WITH RECURSIVE saruud AS (
    SELECT DATE('2024-01-01') AS sar_ehlel
    UNION ALL
    SELECT sar_ehlel + INTERVAL 1 MONTH
    FROM saruud
    WHERE sar_ehlel < '2024-07-01'
)
SELECT sar_ehlel, DATE_FORMAT(sar_ehlel, '%Y-%m') AS sar
FROM saruud;
""",
        ),
        LessonSpec(
            title="ROW_NUMBER, RANK, DENSE_RANK",
            slug="row-number-rank-dense-rank",
            description="Бүлэг доторх дугаарлалт ба бүлэг бүрийн эхний N мөр.",
            duration=600,
            language=MY,
            content="""\
**Window функц** нь `GROUP BY` шиг мөрүүдийг нэгтгэдэггүй. Мөр бүр
хэвээрээ үлдэж, хажууд нь «цонх» доторх тооцоолол нэмэгдэнэ.

```sql
функц() OVER (PARTITION BY бүлэглэх ORDER BY эрэмбэлэх)
```

- `PARTITION BY` — цонхыг бүлгүүдэд хуваана (заавал биш)
- `ORDER BY` — бүлэг доторх дараалал

MySQL 8.0-оос хойш дэмжигдэнэ. Бичлэг нь SQL стандартын дагуу.

### Гурван эрэмбэлэх функц

Хэрэглэгч бүрийн захиалгын тоо (цуцлагдсаныг оруулаад):

```sql
SELECT ner, zahialgiin_too,
       ROW_NUMBER() OVER (ORDER BY zahialgiin_too DESC, hereglegch_id) AS dugaar,
       RANK()       OVER (ORDER BY zahialgiin_too DESC) AS zereg,
       DENSE_RANK() OVER (ORDER BY zahialgiin_too DESC) AS nyagt_zereg
FROM ...;
```

| ner | zahialgiin_too | dugaar | zereg | nyagt_zereg |
|---|---|---|---|---|
| Болд | 3 | 1 | 1 | 1 |
| Сараа | 2 | 2 | 2 | 2 |
| Тэмүүлэн | 1 | 3 | 3 | 3 |
| Номин | 1 | 4 | 3 | 3 |
| Анар | 1 | 5 | 3 | 3 |
| Хулан | 1 | 6 | 3 | 3 |
| Энх | 1 | 7 | 3 | 3 |
| Мөнх | 0 | 8 | 8 | 4 |

| Функц | Тэнцсэн утга | Дараагийн дугаар |
|---|---|---|
| `ROW_NUMBER` | Өөр өөр дугаар (дараалал нь санамсаргүй) | Үргэлж +1 |
| `RANK` | Ижил дугаар | Цоорхой үлдээнэ (3, 3, 3, 3, 3, **8**) |
| `DENSE_RANK` | Ижил дугаар | Цоорхойгүй (3, 3, 3, 3, 3, **4**) |

> `ROW_NUMBER` тэнцсэн мөрүүдэд ямар дугаар өгөхийг баталгаажуулдаггүй.
> Тогтвортой үр дүн хэрэгтэй бол `ORDER BY`-д давтагдашгүй багана
> (`hereglegch_id`) нэм.

### Бүлэг бүрийн хамгийн үнэтэй бараа

```sql
SELECT a.ner AS angilal, b.ner, b.une,
       ROW_NUMBER() OVER (PARTITION BY b.angilal_id ORDER BY b.une DESC) AS dugaar
FROM baraa b
JOIN angilal a ON a.angilal_id = b.angilal_id;
```

`PARTITION BY` ангилал бүрт дугаарлалтыг 1-ээс дахин эхлүүлнэ.

### Window функцийг `WHERE`-д ашиглаж болохгүй

Window функц `WHERE`-ээс **хойно** тооцоологдоно. Тиймээс CTE эсвэл
derived table-д ороож, гадна талд шүүнэ:

```sql
WITH erembe AS (
    SELECT angilal_id, ner, une,
           ROW_NUMBER() OVER (PARTITION BY angilal_id ORDER BY une DESC) AS dugaar
    FROM baraa
)
SELECT * FROM erembe WHERE dugaar <= 2;   -- ангилал бүрийн top-2
```

Тэнцсэн үнэтэй барааг бүгдийг нь авах бол `ROW_NUMBER`-ийн оронд
`RANK` хэрэглэ.

Зарим DBMS-д window функцээр шүүх `QUALIFY` бичлэг бий, MySQL-д **байхгүй**
— CTE эсвэл derived table-д ороох нь цорын ганц арга.

Модул 2-т `LIMIT 1` нь тэнцсэн мөрүүдээс нэгийг л авдгийг харсан.
`RANK() … = 1` нь тэнцсэн **бүгдийг** авна:

```sql
WITH erembe AS (
    SELECT ner, uldegdel, RANK() OVER (ORDER BY uldegdel) AS zereg
    FROM baraa
)
SELECT ner, uldegdel FROM erembe WHERE zereg = 1;   -- Гутал, Сүүтэй цай
```

### Aggregate функцийг цонхоор

`SUM`, `AVG`, `COUNT`, `MIN`, `MAX` мөн `OVER`-тэй ажиллана:

```sql
SELECT ner, une,
       AVG(une) OVER (PARTITION BY angilal_id) AS angilal_dundaj,
       une - AVG(une) OVER (PARTITION BY angilal_id) AS zoruu
FROM baraa;
```

Мөр бүр хадгалагдаж, бүлгийн дундаж хажууд нь гарна — `GROUP BY`-гаар
үүнийг JOIN-гүйгээр хийх боломжгүй.

> MySQL 8.0-д `RANK`, `ROW_NUMBER` зэрэг нь **нөөц үг**. Багана эсвэл
> alias-д `rank` гэж нэр өгвөл алдаа гарна.
""",
            initial_code="""\
USE delguur;

-- 1. Ангилал бүр доторх үнийн дугаарлалт
SELECT a.ner AS angilal, b.ner AS baraa, b.une,
       ROW_NUMBER() OVER (PARTITION BY b.angilal_id ORDER BY b.une DESC) AS dugaar
FROM baraa b
JOIN angilal a ON a.angilal_id = b.angilal_id
ORDER BY b.angilal_id, dugaar;

-- 2. Ангилал бүрийн хамгийн үнэтэй бараа
WITH erembe AS (
    SELECT b.angilal_id, b.ner, b.une,
           ROW_NUMBER() OVER (PARTITION BY b.angilal_id ORDER BY b.une DESC) AS dugaar
    FROM baraa b
)
SELECT a.ner AS angilal, e.ner AS baraa, e.une
FROM erembe e
JOIN angilal a ON a.angilal_id = e.angilal_id
WHERE e.dugaar = 1
ORDER BY e.une DESC;

-- 3. Ангилал бүрийн top-2 бараа
WITH erembe AS (
    SELECT angilal_id, ner, une,
           ROW_NUMBER() OVER (PARTITION BY angilal_id ORDER BY une DESC) AS dugaar
    FROM baraa
)
SELECT angilal_id, dugaar, ner, une
FROM erembe
WHERE dugaar <= 2
ORDER BY angilal_id, dugaar;

-- 4. ROW_NUMBER, RANK, DENSE_RANK ялгаа: захиалгын тоогоор
WITH hereglegch_too AS (
    SELECT h.hereglegch_id, h.ner, COUNT(z.zahialga_id) AS zahialgiin_too
    FROM hereglegch h
    LEFT JOIN zahialga z ON z.hereglegch_id = h.hereglegch_id
    GROUP BY h.hereglegch_id, h.ner
)
SELECT ner, zahialgiin_too,
       ROW_NUMBER() OVER (ORDER BY zahialgiin_too DESC, hereglegch_id) AS dugaar,
       RANK()       OVER (ORDER BY zahialgiin_too DESC) AS zereg,
       DENSE_RANK() OVER (ORDER BY zahialgiin_too DESC) AS nyagt_zereg
FROM hereglegch_too
ORDER BY zahialgiin_too DESC, hereglegch_id;

-- 5. Цонхоор aggregate: бараа бүрийг ангиллын дундажтай харьцуулах
SELECT ner, angilal_id, une,
       ROUND(AVG(une) OVER (PARTITION BY angilal_id), 0) AS angilal_dundaj,
       COUNT(*) OVER (PARTITION BY angilal_id) AS angilal_baraa_too
FROM baraa
ORDER BY angilal_id, une DESC;

-- 6. Тэнцсэн бүгдийг авах: хамгийн бага үлдэгдэлтэй бараа (Гутал, Сүүтэй цай)
WITH erembe AS (
    SELECT ner, uldegdel, RANK() OVER (ORDER BY uldegdel) AS zereg
    FROM baraa
)
SELECT ner, uldegdel
FROM erembe
WHERE zereg = 1;
""",
        ),
        LessonSpec(
            title="Хуримтлагдсан дүн, LAG ба LEAD",
            slug="running-total-lag-lead",
            description="Сарын орлого, өсөлт бууралтыг window функцээр тооцох.",
            duration=660,
            language=MY,
            content="""\
Тайланд хамгийн их хэрэгтэй хоёр асуулт: «Одоог хүртэл нийт хэд болсон
бэ?» ба «Өмнөх сараас хэр өөрчлөгдсөн бэ?».

### Эхлээд сараар бүлэглэх

| Зорилго | MySQL |
|---|---|
| Сарын түлхүүр (текст) | `DATE_FORMAT(ognoo, '%Y-%m')` |
| Сарын сүүлийн өдөр | `LAST_DAY(ognoo)` |

`'2024-02'` хэлбэрийн текст цагаан толгойн дарааллаар ч **зөв**
эрэмбэлэгдэнэ — он, сар хоёр оронтой тул.

Цуцлагдаагүй захиалгын сарын орлого:

| sar | orlogo | huriimtlagdsan | uurchlult |
|---|---|---|---|
| 2024-02 | 1 645 000 | 1 645 000 | NULL |
| 2024-03 | 118 000 | 1 763 000 | −1 527 000 |
| 2024-04 | 2 300 000 | 4 063 000 | +2 182 000 |
| 2024-05 | 435 000 | 4 498 000 | −1 865 000 |
| 2024-06 | 3 493 000 | 7 991 000 | +3 058 000 |

### Хуримтлагдсан дүн

```sql
SUM(orlogo) OVER (ORDER BY sar
                  ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
```

`OVER` дотор `ORDER BY` байхад **frame** (цонхны хүрээ) утга учиртай:

| Frame | Утга |
|---|---|
| `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` | Эхнээс одоогийн мөр хүртэл |
| `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` | Сүүлийн 3 мөр (гулсах дундаж) |
| `ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING` | Одооноос төгсгөл хүртэл |

> Frame бичихгүй бол анхдагч нь
> `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`. `RANGE` нь ижил
> `ORDER BY` утгатай мөрүүдийг **хамт** оруулдаг тул давхардсан огноотой
> үед гэнэтийн үр дүн өгнө. `ROWS`-ийг тодорхой бич.

### LAG ба LEAD

```sql
LAG(orlogo)        OVER (ORDER BY sar)   -- өмнөх мөрийн утга
LEAD(orlogo)       OVER (ORDER BY sar)   -- дараагийн мөрийн утга
LAG(orlogo, 1, 0)  OVER (ORDER BY sar)   -- 1 мөр өмнөх, байхгүй бол 0
```

Сараас сарын өөрчлөлт ба хувь:

```sql
orlogo - LAG(orlogo) OVER (ORDER BY sar) AS uurchlult,
ROUND(100 * (orlogo - LAG(orlogo) OVER (ORDER BY sar))
      / NULLIF(LAG(orlogo) OVER (ORDER BY sar), 0), 1) AS huvi
```

`NULLIF(..., 0)` нь тэгд хуваахаас хамгаална (Модул 11).

### Нэрлэсэн цонх

Ижил `OVER (ORDER BY sar)`-ийг олон удаа бичихийн оронд `WINDOW`-оор
нэр өгч болно:

```sql
SELECT sar, orlogo,
       LAG(orlogo)  OVER w AS umnuh_sar,
       LEAD(orlogo) OVER w AS daraagiin_sar
FROM sariin_orlogo
WINDOW w AS (ORDER BY sar);
```

### Анхаарах: хоосон сар

Захиалгагүй сар үр дүнд **огт гарахгүй**. Тэгвэл `LAG` нь «өмнөх сар»
биш «өмнөх мөр»-ийг авна. Бүх сарыг харуулах бол өмнөх хичээлийн рекурсив
CTE-ээр сарын цуваа үүсгээд `LEFT JOIN` хий — анхны кодын 4-р жишээ.

### Бүлэг бүрт хуримтлуулах

```sql
SUM(dun) OVER (PARTITION BY hereglegch_id
               ORDER BY zahialsan_ognoo
               ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
```

Хэрэглэгч бүрийн хуримтлагдсан худалдан авалт тусдаа 0-ээс эхэлнэ.
""",
            initial_code="""\
USE delguur;

-- 1. Сарын орлого, хуримтлагдсан дүн, өмнөх ба дараагийн сартай харьцуулалт
WITH sariin_orlogo AS (
    -- Сар бүрээр бүлэглэнэ (цуцлагдсан захиалгыг хасна)
    SELECT DATE_FORMAT(z.zahialsan_ognoo, '%Y-%m') AS sar,
           SUM(m.too * m.negj_une) AS orlogo
    FROM zahialga AS z
    JOIN zahialgiin_mur AS m ON m.zahialga_id = z.zahialga_id
    WHERE z.tuluv <> 'Цуцлагдсан'
    GROUP BY DATE_FORMAT(z.zahialsan_ognoo, '%Y-%m')
)
SELECT sar,
       orlogo,
       SUM(orlogo) OVER (ORDER BY sar
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS huriimtlagdsan,
       LAG(orlogo) OVER (ORDER BY sar) AS umnuh_sar,
       orlogo - LAG(orlogo) OVER (ORDER BY sar) AS uurchlult,
       ROUND(100 * (orlogo - LAG(orlogo) OVER (ORDER BY sar))
             / NULLIF(LAG(orlogo) OVER (ORDER BY sar), 0), 1) AS huvi,
       LEAD(orlogo) OVER (ORDER BY sar) AS daraagiin_sar
FROM sariin_orlogo
ORDER BY sar;

-- 2. Гулсах дундаж: сүүлийн 3 сарын дундаж орлого
WITH sariin_orlogo AS (
    SELECT DATE_FORMAT(z.zahialsan_ognoo, '%Y-%m') AS sar,
           SUM(m.too * m.negj_une) AS orlogo
    FROM zahialga AS z
    JOIN zahialgiin_mur AS m ON m.zahialga_id = z.zahialga_id
    WHERE z.tuluv <> 'Цуцлагдсан'
    GROUP BY DATE_FORMAT(z.zahialsan_ognoo, '%Y-%m')
)
SELECT sar, orlogo,
       ROUND(AVG(orlogo) OVER (ORDER BY sar
           ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 0) AS gulsah_dundaj
FROM sariin_orlogo
ORDER BY sar;

-- 3. Хэрэглэгч бүрийн хуримтлагдсан худалдан авалт ба өмнөх захиалгын огноо
WITH zahialgiin_dun AS (
    SELECT z.zahialga_id, z.hereglegch_id, z.zahialsan_ognoo,
           SUM(m.too * m.negj_une) AS dun
    FROM zahialga AS z
    JOIN zahialgiin_mur AS m ON m.zahialga_id = z.zahialga_id
    WHERE z.tuluv <> 'Цуцлагдсан'
    GROUP BY z.zahialga_id, z.hereglegch_id, z.zahialsan_ognoo
)
SELECT hereglegch_id, zahialga_id, zahialsan_ognoo, dun,
       SUM(dun) OVER (PARTITION BY hereglegch_id ORDER BY zahialsan_ognoo
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS huriimtlagdsan,
       LAG(zahialsan_ognoo) OVER (PARTITION BY hereglegch_id
           ORDER BY zahialsan_ognoo) AS umnuh_zahialga
FROM zahialgiin_dun
ORDER BY hereglegch_id, zahialsan_ognoo;

-- 4. Хоосон сарыг ч харуулах: рекурсив CTE-ийн сарын цуваа + LEFT JOIN
--    (1, 7-р сард захиалга байхгүй — 0 гэж гарна)
WITH RECURSIVE saruud AS (
    SELECT DATE('2024-01-01') AS sar_ehlel
    UNION ALL
    SELECT sar_ehlel + INTERVAL 1 MONTH FROM saruud WHERE sar_ehlel < '2024-07-01'
),
sariin_orlogo AS (
    SELECT DATE_FORMAT(z.zahialsan_ognoo, '%Y-%m') AS sar,
           SUM(m.too * m.negj_une) AS orlogo
    FROM zahialga AS z
    JOIN zahialgiin_mur AS m ON m.zahialga_id = z.zahialga_id
    WHERE z.tuluv <> 'Цуцлагдсан'
    GROUP BY DATE_FORMAT(z.zahialsan_ognoo, '%Y-%m')
)
SELECT DATE_FORMAT(s.sar_ehlel, '%Y-%m') AS sar,
       COALESCE(o.orlogo, 0) AS orlogo,
       COALESCE(o.orlogo, 0) - LAG(COALESCE(o.orlogo, 0)) OVER w AS uurchlult
FROM saruud AS s
LEFT JOIN sariin_orlogo AS o ON o.sar = DATE_FORMAT(s.sar_ehlel, '%Y-%m')
WINDOW w AS (ORDER BY s.sar_ehlel)
ORDER BY s.sar_ehlel;
""",
        ),
    ],
)

PROCEDURES = ModuleSpec(
    title="Модул 16 — Stored procedure ба функц",
    description="Хувьсагч, удирдлагын урсгал, процедур, хэрэглэгчийн функц.",
    lessons=[
        LessonSpec(
            title="Хувьсагч ба нөхцөлт логик",
            slug="tsql-huvisagch-udirdlagyn-urgal",
            description="Хэрэглэгчийн хувьсагч (@x), SET ба SELECT … INTO, системийн хувьсагч, IF() ба CASE.",
            duration=540,
            language=MY,
            content="""\
SQL нь өгөгдлийг «юу хэрэгтэй вэ» гэж тайлбарладаг хэл. Гэхдээ нэг
асуулгын үр дүнг дараагийнх нь ашиглах, утгыг түр хадгалах хэрэг гарна.
Үүнд **хувьсагч** хэрэгтэй. Энэ хичээл энгийн скрипт дотор ажилладаг
хувьсагчийг үзнэ, дараагийнх нь процедур доторх `IF`, `WHILE`-ийг.

### Хэрэглэгчийн хувьсагч: `@нэр`

```sql
SET @dood_une = 100000;
SELECT ner, une FROM baraa WHERE une >= @dood_une;
```

| Шинж | Хэрэглэгчийн хувьсагч `@x` |
|---|---|
| Зарлах | Шаардлагагүй — `SET` хийхэд л үүснэ |
| Төрөл | Өгсөн утгаас хамаарна |
| Хүрээ | **Холболт** (session) — өөр холболт харахгүй |
| Амьдрах хугацаа | Холболт хаагдах хүртэл |
| Утга өгөөгүй бол | `NULL` |

Нэг `SET`-ээр хэд хэдэн хувьсагч: `SET @a = 1, @b = 'Болд';`

> Энэ сайт дээр ажиллуулалт бүр **шинэ холболт** тул өмнөх
> ажиллуулалтын хувьсагч үлдэхгүй — нэг скрипт дотроо л ашиглана.

### SELECT … INTO — асуулгын үр дүнг хувьсагчид

```sql
SELECT COUNT(*) INTO @too FROM baraa WHERE une >= @dood_une;

SELECT ner, uldegdel INTO @ner, @uldegdel
FROM baraa
WHERE baraa_id = 9;
```

Баганын тоо ба хувьсагчийн тоо таарна. Асуулга **яг нэг мөр** буцаах ёстой:

| Мөрийн тоо | Юу болох вэ |
|---|---|
| 1 | Хувьсагчид утга орно |
| 0 | Анхааруулга 1329 `No data`, хувьсагч **хуучин утгаа** хадгална |
| 2+ | Алдаа 1172 `Result consisted of more than one row` |

0 мөрийн тохиолдол хамгийн аюултай: алдаа гарахгүй, хувьсагчид өмнөх
утга үлдэнэ. Шалгах бол эхлээд `SET @ner = NULL;` гэж цэвэрлээд дараа нь
`@ner IS NULL`-ээр шалга.

> `SELECT @x := …` хэлбэрээр илэрхийлэл дотор утга оноох нь MySQL 8-д
> хуучирсан (deprecated). `SET` эсвэл `SELECT … INTO` хэрэглэ.

### Системийн хувьсагч: `@@нэр`

Хоёр `@` нь серверийн **тохиргоо**: `@@version`, `@@autocommit`
(Модул 14), `@@sql_mode` (Модул 5, 6), `@@transaction_isolation`.
`SET SESSION нэр = утга` нь зөвхөн энэ холболтын тохиргоог өөрчилнө.

### Нөхцөлт логик: IF() ба CASE

Энгийн скриптэд «хэрэв … бол» гэдгийг **илэрхийллээр** бичнэ (Модул 11):

```sql
SELECT CASE
           WHEN @uldegdel IS NULL THEN 'Бараа олдсонгүй'
           WHEN @uldegdel = 0     THEN 'Дууссан'
           WHEN @uldegdel < 10    THEN 'Цөөхөн үлдсэн'
           ELSE 'Хангалттай'
       END AS tuluv,
       IF(@uldegdel < 10, 'Захиалах', 'Хүлээх') AS zuvlumj;
```

### Процедур доторх хувьсагч ба удирдлага

`IF … THEN … END IF` **тушаал**, `WHILE` давталт, `DECLARE`-ээр зарласан
**локал** хувьсагч нь зөвхөн `BEGIN … END` блок дотор — процедур, функц,
trigger-т ажиллана. Энгийн скриптэд бичвэл синтакс алдаа. Эдгээрийг
дараагийн хичээлд үзнэ.

| | Хэрэглэгчийн `@x` | Локал `x` |
|---|---|---|
| Хаана | Хаана ч | Зөвхөн `BEGIN … END` дотор |
| Зарлах | Үгүй | `DECLARE x INT DEFAULT 0;` |
| Хүрээ | Холболтын турш | Тухайн блок |

### Давталтын оронд set-based

Энгийн скриптэд давталт байхгүй — бас хэрэггүй нь олонтаа. «Ангилал
бүрээр давтаж барааг тоолох» ажлыг нэг `GROUP BY` хийнэ; 1..N цуваа
хэрэгтэй бол рекурсив CTE (Модул 15). Мөр мөрөөр давтах нь олон мөрт нэг
асуулгаас хэдэн зуу дахин удаан байж болно.

> `LIMIT`-д хувьсагч бичиж болохгүй: `LIMIT @n` гэвэл синтакс алдаа.
> Ийм үед prepared statement хэрэгтэй (Модул 18).
""",
            initial_code="""\
USE delguur;

-- 1. Хэрэглэгчийн хувьсагч: зарлахгүй, SET-ээр утга өгнө
SET @dood_une = 100000;
SELECT @dood_une AS dood_une;

-- 2. Хувьсагчийг асуулгад ашиглах
SELECT ner, une
FROM baraa
WHERE une >= @dood_une
ORDER BY une;

-- 3. SELECT ... INTO: асуулгын үр дүнг хувьсагчид (яг нэг мөр)
SELECT COUNT(*) INTO @too FROM baraa WHERE une >= @dood_une;
SELECT @too AS unetei_baraa;

-- 4. Нэг мөрөөс хоёр хувьсагч
SET @baraa_id = 9;

SELECT ner, uldegdel INTO @ner, @uldegdel
FROM baraa
WHERE baraa_id = @baraa_id;

SELECT @ner AS ner, @uldegdel AS uldegdel;   -- Тоос сорогч, 4

-- 5. Нөхцөлт логик: CASE ба IF() илэрхийлэл
SELECT @ner AS ner,
       CASE
           WHEN @uldegdel IS NULL THEN 'Бараа олдсонгүй'
           WHEN @uldegdel = 0 THEN 'Дууссан'
           WHEN @uldegdel < 10 THEN 'Цөөхөн үлдсэн'
           ELSE 'Хангалттай'
       END AS tuluv,
       IF(@uldegdel < 10, 'Захиалах', 'Хүлээх') AS zuvlumj;

-- 6. Мөр олдохгүй бол хувьсагч ХУУЧИН утгаа хадгална (+ анхааруулга 1329)
SELECT ner INTO @ner FROM baraa WHERE baraa_id = 999;
SELECT @ner AS ner_hevees;   -- Тоос сорогч хэвээр!

-- Зөв арга: эхлээд цэвэрлээд дараа нь шалгана
SET @ner = NULL;
SELECT ner INTO @ner FROM baraa WHERE baraa_id = 999;
SELECT IF(@ner IS NULL, 'Олдсонгүй', @ner) AS shalgalt;

-- 7. Утга өгөөгүй хувьсагч NULL
SELECT @baihgui_huvisagch AS utga;

-- 8. Тооцооллыг хувьсагчид хадгалж дараагийн асуулгад ашиглах
SELECT AVG(une) INTO @dundaj FROM baraa;

SELECT ner, une, ROUND(une - @dundaj, 0) AS dundjaas_zoruu
FROM baraa
WHERE une > @dundaj
ORDER BY une DESC;

-- 9. Системийн хувьсагч: @@ хоёр тэмдэг
SELECT @@version AS huvilbar,
       @@autocommit AS autocommit,
       @@transaction_isolation AS tusgaarlalt;

-- 10. Давталтын оронд set-based: ангилал бүрийн барааны тоо нэг асуулгаар
SELECT a.angilal_id, a.ner, COUNT(b.baraa_id) AS baraa_too,
       IF(COUNT(b.baraa_id) >= 3, 'Олон', 'Цөөн') AS unelgee
FROM angilal AS a
LEFT JOIN baraa AS b ON b.angilal_id = a.angilal_id
GROUP BY a.angilal_id, a.ner
ORDER BY a.angilal_id;

-- Алдаа 1172 — туршихдаа тайлбарыг арилга (2+ мөр):
-- SELECT ner INTO @ner FROM baraa;
""",
        ),
        LessonSpec(
            title="Stored procedure",
            slug="mysql-stored-procedure",
            description="DELIMITER, IN/OUT параметр, CALL, локал хувьсагч, IF ба WHILE.",
            duration=660,
            language=MY,
            content="""\
**Stored procedure** нь сервер дээр нэрээр хадгалагдсан SQL блок. Програм
олон мөр SQL илгээхийн оронд `CALL нэр(...)` гэж дуудна.

### Яагаад хэрэглэх вэ

- Бизнесийн дүрмийг нэг газар төвлөрүүлнэ
- Сүлжээгээр нэг удаа дуудна
- Хэрэглэгчид хүснэгтэд шууд эрх өгөхгүйгээр зөвхөн процедурыг
  ажиллуулах эрх өгч болно (Модул 18)

### `DELIMITER` гэж юу вэ

Процедурын бие олон `;` агуулна. `mysql` клиент эхний `;`-ийг хараад
statement дууслаа гэж ойлгож, дутуу процедурыг сервер рүү илгээнэ.
Иймээс түр зуур тусгаарлагчийг солино:

```sql
DELIMITER $$
CREATE PROCEDURE ...
BEGIN
    ...;
    ...;
END$$
DELIMITER ;
```

> `DELIMITER` бол SQL биш — `mysql` CLI ба Workbench-ийн **клиентийн**
> тушаал. Python, Node.js зэрэг драйвераар процедур үүсгэхэд хэрэггүй,
> харин бичвэл синтакс алдаа өгнө.

### Параметрийн төрөл

| Төрөл | Утга |
|---|---|
| `IN` (анхдагч) | Дуудагч утга дамжуулна |
| `OUT` | Процедур утга буцаана |
| `INOUT` | Хоёулаа |

```sql
DELIMITER $$
CREATE PROCEDURE hereglegchiin_tuuh(
    IN  p_hereglegch_id INT,
    OUT p_niit DECIMAL(14,2)
)
BEGIN
    SELECT zahialga_id, zahialsan_ognoo, tuluv
    FROM zahialga
    WHERE hereglegch_id = p_hereglegch_id;

    SELECT COALESCE(SUM(m.too * m.negj_une), 0) INTO p_niit
    FROM zahialga z
    JOIN zahialgiin_mur m ON m.zahialga_id = z.zahialga_id
    WHERE z.hereglegch_id = p_hereglegch_id
      AND z.tuluv <> 'Цуцлагдсан';
END$$
DELIMITER ;

CALL hereglegchiin_tuuh(1, @niit);
SELECT @niit;   -- 4835000.00
```

`OUT` параметрт сессийн хувьсагч (`@niit`) дамжуулж, дараа нь уншина.
Процедур доторх `SELECT` нь дуудагч руу **үр дүнгийн олонлог** болж очно.

### Нэрлэх зуршил

> Параметр, локал хувьсагчид `p_`, `v_` угтвар өг. Хүснэгтийн баганатай
> ижил нэртэй хувьсагч (`hereglegch_id`) байвал MySQL **хувьсагчийг**
> сонгоно — `WHERE hereglegch_id = hereglegch_id` үргэлж үнэн болж, бүх
> мөр гарна.

### Локал хувьсагч, IF ба WHILE

`BEGIN … END` дотор л ажилладаг хэрэгслүүд (өмнөх хичээлийн `@x`-ээс
ялгаатай):

```sql
DECLARE v_too INT DEFAULT 0;          -- локал хувьсагч, блокийн ЭХЭНД
SET v_too = v_too + 1;                -- утга оноох
SELECT COUNT(*) INTO v_too FROM baraa;

IF v_too = 0 THEN
    SET v_unelgee = 'Хоосон';
ELSEIF v_too < 3 THEN
    SET v_unelgee = 'Цөөн';
ELSE
    SET v_unelgee = 'Олон';
END IF;

WHILE v_i <= 5 DO
    SET v_i = v_i + 1;
END WHILE;
```

| Бүтэц | Бичлэг |
|---|---|
| Нөхцөл | `IF … THEN … ELSEIF … ELSE … END IF;` |
| Нөхцөлт давталт | `WHILE нөхцөл DO … END WHILE;` |
| Доод нөхцөлтэй давталт | `REPEAT … UNTIL нөхцөл END REPEAT;` |
| Энгийн давталт | `шошго: LOOP … END LOOP шошго;` |
| Давталтаас гарах | `LEAVE шошго;` |
| Дараагийн алхам | `ITERATE шошго;` |

- `DECLARE` нь блокийн **хамгийн эхэнд**, бусад statement-ээс өмнө.
- `IF … END IF` **тушаал** нь Модул 11-ийн `IF(a, b, c)` **функцээс**
  өөр: тушаал нь аль statement-ийг ажиллуулахыг сонгоно, функц утга
  буцаана.
- Давталт хэрэгтэй юу гэдгийг эхлээд бод — ихэнх ажлыг нэг `UPDATE`,
  `GROUP BY` илүү хурдан хийнэ.

### Удирдах

| Үйлдэл | Тушаал |
|---|---|
| Устгах | `DROP PROCEDURE IF EXISTS нэр;` |
| Кодыг харах | `SHOW CREATE PROCEDURE нэр;` |
| Жагсаалт | `SHOW PROCEDURE STATUS WHERE Db = 'delguur';` |
| Өөрчлөх | Устгаад дахин үүсгэнэ (`ALTER PROCEDURE` зөвхөн шинж чанарыг өөрчилнө) |

MySQL-д `CREATE OR REPLACE PROCEDURE` **байхгүй** — `DROP ... IF EXISTS`
хийгээд дахин үүсгэнэ.

### Өгөгдөл өөрчилдөг процедурыг аюулгүй турших

Захиалга үүсгэх процедурыг транзакц дотор дуудаж, үр дүнг хараад
`ROLLBACK` хийвэл өгөгдөл өөрчлөгдөхгүй:

```sql
START TRANSACTION;
CALL zahialga_uusgeh(8, 3, 2, @shine_id);
SELECT * FROM zahialgiin_mur WHERE zahialga_id = @shine_id;
ROLLBACK;
```

> `ROLLBACK` мөрүүдийг буцаадаг ч `AUTO_INCREMENT` тоолуурыг буцаадаггүй.
> Дараагийн захиалгын дугаар алгасаж болно — энэ хэвийн үзэгдэл.

Процедур дотор `START TRANSACTION` / `COMMIT` бичиж болно. Алдааны үед
яаж буцаахыг Модул 17-д үзнэ.
""",
            initial_code="""\
USE delguur;

-- 1. Хэрэглэгчийн захиалгын түүх + нийт дүнг OUT параметрээр
DROP PROCEDURE IF EXISTS hereglegchiin_tuuh;

DELIMITER $$
CREATE PROCEDURE hereglegchiin_tuuh(
    IN  p_hereglegch_id INT,
    OUT p_niit DECIMAL(14,2)
)
BEGIN
    -- Үр дүнгийн олонлог: захиалга бүр ба дүн
    SELECT z.zahialga_id, z.zahialsan_ognoo, z.tuluv,
           SUM(m.too * m.negj_une) AS dun
    FROM zahialga z
    JOIN zahialgiin_mur m ON m.zahialga_id = z.zahialga_id
    WHERE z.hereglegch_id = p_hereglegch_id
    GROUP BY z.zahialga_id, z.zahialsan_ognoo, z.tuluv
    ORDER BY z.zahialsan_ognoo;

    -- OUT утга: цуцлагдаагүй захиалгын нийт дүн
    SELECT COALESCE(SUM(m.too * m.negj_une), 0) INTO p_niit
    FROM zahialga z
    JOIN zahialgiin_mur m ON m.zahialga_id = z.zahialga_id
    WHERE z.hereglegch_id = p_hereglegch_id
      AND z.tuluv <> 'Цуцлагдсан';
END$$
DELIMITER ;

CALL hereglegchiin_tuuh(1, @niit);
SELECT @niit AS bold_niit_dun;

CALL hereglegchiin_tuuh(8, @niit);
SELECT @niit AS munh_niit_dun;

-- 2. Захиалга үүсгэх процедур
DROP PROCEDURE IF EXISTS zahialga_uusgeh;

DELIMITER $$
CREATE PROCEDURE zahialga_uusgeh(
    IN  p_hereglegch_id INT,
    IN  p_baraa_id INT,
    IN  p_too INT,
    OUT p_zahialga_id INT
)
BEGIN
    DECLARE v_une DECIMAL(12,2);

    -- Одоогийн үнийг бараанаас авна
    SELECT une INTO v_une FROM baraa WHERE baraa_id = p_baraa_id;

    INSERT INTO zahialga (hereglegch_id, zahialsan_ognoo)
    VALUES (p_hereglegch_id, NOW());

    SET p_zahialga_id = LAST_INSERT_ID();

    INSERT INTO zahialgiin_mur (zahialga_id, baraa_id, too, negj_une)
    VALUES (p_zahialga_id, p_baraa_id, p_too, v_une);
END$$
DELIMITER ;

-- 3. Транзакц дотор туршаад буцаана: өгөгдөл өөрчлөгдөхгүй
START TRANSACTION;

CALL zahialga_uusgeh(8, 3, 2, @shine_id);

SELECT z.zahialga_id, z.hereglegch_id, z.tuluv, m.baraa_id, m.too, m.negj_une
FROM zahialga z
JOIN zahialgiin_mur m ON m.zahialga_id = z.zahialga_id
WHERE z.zahialga_id = @shine_id;

ROLLBACK;

-- Буцаагдсаныг шалгах: 0 байх ёстой
SELECT COUNT(*) AS uldsen_mur FROM zahialga WHERE zahialga_id = @shine_id;

-- 4. Локал хувьсагч, WHILE ба IF: ангилал бүрийн барааг тоолж үнэлэх
DROP PROCEDURE IF EXISTS angilal_tailan;

DELIMITER $$
CREATE PROCEDURE angilal_tailan()
BEGIN
    DECLARE v_angilal_id INT DEFAULT 1;
    DECLARE v_max_id INT;
    DECLARE v_too INT;
    DECLARE v_unelgee VARCHAR(20);
    DECLARE v_tailan VARCHAR(1000) DEFAULT '';

    SELECT MAX(angilal_id) INTO v_max_id FROM angilal;

    WHILE v_angilal_id <= v_max_id DO
        SELECT COUNT(*) INTO v_too FROM baraa WHERE angilal_id = v_angilal_id;

        IF v_too = 0 THEN
            SET v_unelgee = 'хоосон';
        ELSEIF v_too < 3 THEN
            SET v_unelgee = 'цөөн';
        ELSE
            SET v_unelgee = 'олон';
        END IF;

        SET v_tailan = CONCAT(v_tailan, 'Ангилал ', v_angilal_id, ': ',
                              v_too, ' бараа (', v_unelgee, '); ');
        SET v_angilal_id = v_angilal_id + 1;
    END WHILE;

    SELECT v_tailan AS tailan;
END$$
DELIMITER ;

CALL angilal_tailan();

-- 5. Процедурын жагсаалт
SHOW PROCEDURE STATUS WHERE Db = 'delguur';
""",
        ),
        LessonSpec(
            title="Хэрэглэгчийн функц (UDF)",
            slug="user-defined-function",
            description="Scalar функц, DETERMINISTIC ба READS SQL DATA, процедуртай харьцуулалт.",
            duration=630,
            language=MY,
            content="""\
**Функц** нь утга буцаадаг бөгөөд `SELECT`, `WHERE` зэрэг илэрхийлэл
дотор шууд дуудагдана. Процедурыг `CALL`-оор тусад нь дуудна.

### Scalar функц

```sql
DELIMITER $$
CREATE FUNCTION zahialgiin_dun(p_zahialga_id INT)
RETURNS DECIMAL(14,2)
READS SQL DATA
BEGIN
    DECLARE v_dun DECIMAL(14,2);
    SELECT COALESCE(SUM(too * negj_une), 0) INTO v_dun
    FROM zahialgiin_mur
    WHERE zahialga_id = p_zahialga_id;
    RETURN v_dun;
END$$
DELIMITER ;

SELECT zahialga_id, tuluv, zahialgiin_dun(zahialga_id) AS dun
FROM zahialga;
```

### Шинж чанар ба binary log

MySQL 8.0-д binary log анхдагчаар **асаалттай**. Энэ үед функц үүсгэхдээ
дараахын ядаж нэгийг заавал зарлана, үгүй бол алдаа 1418 гарна:

| Шинж чанар | Утга |
|---|---|
| `DETERMINISTIC` | Ижил оролтод үргэлж ижил үр дүн |
| `NO SQL` | SQL огт агуулахгүй |
| `READS SQL DATA` | Өгөгдөл уншина, өөрчлөхгүй |

> Админ `SET GLOBAL log_bin_trust_function_creators = 1;` гэж энэ
> шалгалтыг унтрааж болно. Гэхдээ шинж чанарыг **үнэнээр** зарлах нь
> зөв. Хүснэгт уншдаг функцийг `DETERMINISTIC` гэвэл replication дээр
> өөр үр дүн гарч болзошгүй.

### Функц хүснэгт буцааж чадахгүй

MySQL-ийн хэрэглэгчийн функц зөвхөн **нэг утга** (scalar) буцаана. Олон
мөр, багана хэрэгтэй бол:

- **View** (Модул 13) — параметргүй хадгалсан асуулга
- **Процедур** — дотор нь `SELECT` бичвэл үр дүнгийн олонлог буцаана
- **LATERAL** дэд асуулга (Модул 10) — мөр бүрт «параметртэй» асуулга

Функц дотор `IF … END IF`, `DECLARE` зэрэг өмнөх хичээлийн бүх хэрэгсэл
ажиллана — доорх 3-р жишээ.

### Функц ба процедур

| | Функц | Процедур |
|---|---|---|
| Дуудах | `SELECT`, `WHERE` дотор | `CALL` |
| Буцаах | Нэг утга | Үр дүнгийн олонлог, `OUT` параметр |
| Өгөгдөл өөрчлөх | Боломжтой ч зөвлөхгүй | Боломжтой |
| Транзакц удирдах | Боломжгүй | Боломжтой |
| Динамик SQL | Боломжгүй | Боломжтой |
| Үр дүнгийн олонлог буцаах | Боломжгүй | Боломжтой |

> Энгийн дүрэм: **тооцоолол** бол функц, **үйлдэл** (захиалга үүсгэх,
> төлөв өөрчлөх) бол процедур.

### Гүйцэтгэлийн анхааруулга

`WHERE zahialgiin_dun(zahialga_id) > 500000` нь мөр бүрт функц дуудаж,
index ашиглах боломжгүй болгоно. Их өгөгдөлтэй бол JOIN + `GROUP BY`
эсвэл CTE-ээр бич.
""",
            initial_code="""\
USE delguur;

-- 1. Энгийн тооцоолол: НӨАТ (10%) нэмсэн үнэ, SQL агуулахгүй
DROP FUNCTION IF EXISTS une_nuattai;

DELIMITER $$
CREATE FUNCTION une_nuattai(p_une DECIMAL(12,2))
RETURNS DECIMAL(14,2)
DETERMINISTIC
NO SQL
BEGIN
    RETURN ROUND(p_une * 1.10, 2);
END$$
DELIMITER ;

SELECT ner, une, une_nuattai(une) AS nuattai_une
FROM baraa
ORDER BY une DESC;

-- 2. Хүснэгт уншдаг функц: захиалгын нийт дүн
DROP FUNCTION IF EXISTS zahialgiin_dun;

DELIMITER $$
CREATE FUNCTION zahialgiin_dun(p_zahialga_id INT)
RETURNS DECIMAL(14,2)
READS SQL DATA
BEGIN
    DECLARE v_dun DECIMAL(14,2);

    SELECT COALESCE(SUM(too * negj_une), 0) INTO v_dun
    FROM zahialgiin_mur
    WHERE zahialga_id = p_zahialga_id;

    RETURN v_dun;
END$$
DELIMITER ;

SELECT zahialga_id, tuluv, zahialgiin_dun(zahialga_id) AS dun
FROM zahialga
ORDER BY zahialga_id;

-- 3. IF ба CASE ашигласан функц: хэрэглэгчийн зэрэглэл
DROP FUNCTION IF EXISTS hereglegchiin_zereglel;

DELIMITER $$
CREATE FUNCTION hereglegchiin_zereglel(p_hereglegch_id INT)
RETURNS VARCHAR(20)
READS SQL DATA
BEGIN
    DECLARE v_niit DECIMAL(14,2);

    SELECT COALESCE(SUM(m.too * m.negj_une), 0) INTO v_niit
    FROM zahialga z
    JOIN zahialgiin_mur m ON m.zahialga_id = z.zahialga_id
    WHERE z.hereglegch_id = p_hereglegch_id
      AND z.tuluv <> 'Цуцлагдсан';

    IF v_niit >= 1000000 THEN
        RETURN 'Алт';
    ELSEIF v_niit >= 300000 THEN
        RETURN 'Мөнгө';
    END IF;
    RETURN 'Энгийн';
END$$
DELIMITER ;

SELECT hereglegch_id, ner, hereglegchiin_zereglel(hereglegch_id) AS zereglel
FROM hereglegch
ORDER BY hereglegch_id;

-- 4. Үүссэн функцүүдийг харах
SHOW FUNCTION STATUS WHERE Db = 'delguur';
SHOW CREATE FUNCTION zahialgiin_dun;
""",
        ),
    ],
)

TRIGGERS_ERRORS = ModuleSpec(
    title="Модул 17 — Trigger ба алдаа боловсруулалт",
    description="Автомат үйлдэл ба алдааг зөв барьж, транзакцыг буцаах.",
    lessons=[
        LessonSpec(
            title="Trigger",
            slug="mysql-trigger",
            description="BEFORE/AFTER, FOR EACH ROW, NEW ба OLD — үлдэгдлийг автоматаар шинэчлэх.",
            duration=630,
            language=MY,
            content="""\
**Trigger** нь хүснэгтэд `INSERT`, `UPDATE`, `DELETE` болох үед
**автоматаар** ажилладаг код. Програм мартсан ч өгөгдлийн сан дүрмийг
өөрөө сахина.

### Бүтэц

```sql
DELIMITER $$
CREATE TRIGGER нэр
{BEFORE | AFTER} {INSERT | UPDATE | DELETE}
ON хүснэгт
FOR EACH ROW
BEGIN
    ...
END$$
DELIMITER ;
```

MySQL-ийн trigger үргэлж **мөр бүрт** (`FOR EACH ROW`) ажиллана: 3 мөр
нэмбэл 3 удаа.

### `NEW` ба `OLD`

| Үйлдэл | `OLD` | `NEW` |
|---|---|---|
| `INSERT` | Байхгүй | Шинэ мөр |
| `UPDATE` | Өөрчлөхөөс өмнөх | Өөрчилсний дараах |
| `DELETE` | Устгах мөр | Байхгүй |

`OLD` зөвхөн уншигдана. `BEFORE` trigger дотор `SET NEW.багана = ...`
гэж оруулах утгыг өөрчилж болно.

### BEFORE ба AFTER

| | `BEFORE` | `AFTER` |
|---|---|---|
| Хэрэглээ | Шалгах, `NEW` утгыг засах | Өөр хүснэгтийг шинэчлэх, лог бичих |
| Алдаа өгвөл | Мөр огт бичигдэхгүй | Statement бүхэлдээ буцаагдана |

### Жишээ: захиалга нэмэхэд үлдэгдэл хасах

```sql
CREATE TRIGGER zahialgiin_mur_ai_uldegdel
AFTER INSERT ON zahialgiin_mur
FOR EACH ROW
BEGIN
    UPDATE baraa
    SET uldegdel = uldegdel - NEW.too
    WHERE baraa_id = NEW.baraa_id;
END$$
```

Үлдэгдэл хүрэлцэхгүй бол `BEFORE INSERT` дотор `SIGNAL` ашиглан
statement-ийг зогсооно:

```sql
IF v_uldegdel < NEW.too THEN
    SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Үлдэгдэл хүрэлцэхгүй байна';
END IF;
```

InnoDB хүснэгтэд trigger алдаа өгвөл тухайн statement-ийн бүх өөрчлөлт
(trigger-ийн хийсэн `UPDATE` ч мөн) буцаагдана.

### UPDATE ба DELETE

```sql
-- Тоо ширхэг өөрчлөгдвөл зөрүүг тооцно
UPDATE baraa SET uldegdel = uldegdel + OLD.too - NEW.too
WHERE baraa_id = NEW.baraa_id;

-- Мөр устгавал үлдэгдлийг буцааж нэмнэ
UPDATE baraa SET uldegdel = uldegdel + OLD.too
WHERE baraa_id = OLD.baraa_id;
```

> `UPDATE` жишээ нь `baraa_id` өөрчлөгдөхгүй гэж үзсэн. Өөрчлөгдөж
> болох бол `OLD.baraa_id`-д нэмж, `NEW.baraa_id`-аас хас.

### Хязгаарлалт

- Trigger-ийг үүсгэсэн хүснэгтээ дотроос нь `UPDATE` хийж болохгүй
  (алдаа 1442). Оронд нь `BEFORE` дотор `SET NEW...` ашигла.
- Foreign key-ийн `ON DELETE CASCADE` зэрэг үйлдэл trigger асаадаггүй.
- `TRUNCATE TABLE` нь `DELETE` trigger асаахгүй.
- Үр дүнгийн олонлог буцааж (`SELECT` хэвлэх) болохгүй.
- Нэг үйлдэлд олон trigger байж болно, дарааллыг `FOLLOWS` / `PRECEDES`.

### Удирдах

```sql
SHOW TRIGGERS FROM delguur;
DROP TRIGGER IF EXISTS zahialgiin_mur_ai_uldegdel;
```

> Trigger нь «үл харагдах» код. Хэт олон бол алдааг хайхад хэцүү. Энгийн,
> баримтжуулсан, заавал хэрэгтэй дүрэмд л хэрэглэ.
""",
            initial_code="""\
USE delguur;

-- 0. Дахин ажиллуулж болохуйц: байвал эхлээд устгана
DROP TRIGGER IF EXISTS zahialgiin_mur_bi_shalgah;
DROP TRIGGER IF EXISTS zahialgiin_mur_ai_uldegdel;
DROP TRIGGER IF EXISTS zahialgiin_mur_ad_uldegdel;

DELIMITER $$

-- 1. BEFORE INSERT: үлдэгдэл хүрэлцэх эсэхийг шалгана
CREATE TRIGGER zahialgiin_mur_bi_shalgah
BEFORE INSERT ON zahialgiin_mur
FOR EACH ROW
BEGIN
    DECLARE v_uldegdel INT;

    SELECT uldegdel INTO v_uldegdel
    FROM baraa
    WHERE baraa_id = NEW.baraa_id;

    IF v_uldegdel < NEW.too THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Үлдэгдэл хүрэлцэхгүй байна';
    END IF;
END$$

-- 2. AFTER INSERT: үлдэгдлээс хасна
CREATE TRIGGER zahialgiin_mur_ai_uldegdel
AFTER INSERT ON zahialgiin_mur
FOR EACH ROW
BEGIN
    UPDATE baraa
    SET uldegdel = uldegdel - NEW.too
    WHERE baraa_id = NEW.baraa_id;
END$$

-- 3. AFTER DELETE: устгасан мөрийн тоог буцааж нэмнэ
CREATE TRIGGER zahialgiin_mur_ad_uldegdel
AFTER DELETE ON zahialgiin_mur
FOR EACH ROW
BEGIN
    UPDATE baraa
    SET uldegdel = uldegdel + OLD.too
    WHERE baraa_id = OLD.baraa_id;
END$$

DELIMITER ;

SHOW TRIGGERS FROM delguur;

-- 4. Транзакц дотор турших: төгсгөлд ROLLBACK
START TRANSACTION;

-- Эхний үлдэгдэл: Чихэвч 40, Цайны аяга 100
SELECT baraa_id, ner, uldegdel FROM baraa WHERE baraa_id IN (3, 8);

INSERT INTO zahialga (hereglegch_id, zahialsan_ognoo) VALUES (8, NOW());
SET @z = LAST_INSERT_ID();

-- Хоёр мөр нэмнэ: trigger мөр бүрт ажиллана
INSERT INTO zahialgiin_mur (zahialga_id, baraa_id, too, negj_une)
VALUES (@z, 3, 2, 89000.00),
       (@z, 8, 5, 18000.00);

-- Одоо: Чихэвч 38, Цайны аяга 95
SELECT baraa_id, ner, uldegdel FROM baraa WHERE baraa_id IN (3, 8);

-- Нэг мөрийг устгавал Цайны аяга 100 болж буцна
DELETE FROM zahialgiin_mur WHERE zahialga_id = @z AND baraa_id = 8;
SELECT baraa_id, ner, uldegdel FROM baraa WHERE baraa_id IN (3, 8);

-- Туршиж үзэх: Гутал (5) үлдэгдэл 0 тул доорх мөр алдаа 45000 өгнө
-- INSERT INTO zahialgiin_mur (zahialga_id, baraa_id, too, negj_une) VALUES (@z, 5, 1, 210000.00);

ROLLBACK;

-- Анхны утга сэргэсэн: Чихэвч 40, Цайны аяга 100
SELECT baraa_id, ner, uldegdel FROM baraa WHERE baraa_id IN (3, 8);

-- 5. Цэвэрлэх: дараагийн хичээлүүдэд нөлөөлөхгүйн тулд устгана
DROP TRIGGER IF EXISTS zahialgiin_mur_bi_shalgah;
DROP TRIGGER IF EXISTS zahialgiin_mur_ai_uldegdel;
DROP TRIGGER IF EXISTS zahialgiin_mur_ad_uldegdel;
""",
        ),
        LessonSpec(
            title="Алдаа боловсруулалт: HANDLER ба SIGNAL",
            slug="mysql-aldaa-handler-signal",
            description="DECLARE HANDLER, SIGNAL, RESIGNAL, GET DIAGNOSTICS ба ROLLBACK.",
            duration=630,
            language=MY,
            content="""\
Процедурын дунд алдаа гарвал хагас хийгдсэн өөрчлөлт үлдэж болно:
нэг данснаас мөнгө хасагдаад нөгөөд нь нэмэгдээгүй гэх мэт. Алдааг
барьж, транзакцыг **бүхэлд нь** буцаах хэрэгтэй.

### Handler

```sql
DECLARE {EXIT | CONTINUE} HANDLER FOR нөхцөл
    statement;
```

| Төрөл | Handler ажилласны дараа |
|---|---|
| `EXIT` | Одоогийн `BEGIN ... END` блокоос гарна |
| `CONTINUE` | Алдаа гарсан statement-ийн дараагаас үргэлжилнэ |

MySQL-д `UNDO` handler байхгүй.

| Нөхцөл | Юуг барина |
|---|---|
| `SQLEXCEPTION` | Бүх алдаа |
| `SQLWARNING` | Анхааруулга (`01` ангилал) |
| `NOT FOUND` | Мөр олдсонгүй (`02` ангилал, cursor, `SELECT INTO`) |
| `1062` | Тодорхой MySQL алдааны код (давхардсан түлхүүр) |
| `SQLSTATE '23000'` | Тодорхой SQLSTATE |

```sql
-- Давхардсан түлхүүр гарвал алгасаад үргэлжлэх
DECLARE CONTINUE HANDLER FOR 1062 SET v_davhardsan = 1;
```

> `DECLARE`-ийн дараалал заавал: эхлээд хувьсагч ба condition, дараа нь
> cursor, **хамгийн сүүлд** handler.

### Транзакцыг буцаах загвар

```sql
DECLARE EXIT HANDLER FOR SQLEXCEPTION
BEGIN
    ROLLBACK;
    RESIGNAL;      -- анхны алдааг дуудагч руу дамжуулна
END;

START TRANSACTION;
    ...
COMMIT;
```

`RESIGNAL`-гүй бол алдаа чимээгүй «залгигдана» — дуудагч амжилттай
болсон гэж бодно. Алдааг лог бичих, эсвэл `OUT` параметрт мессеж буцаах
бол `GET DIAGNOSTICS` ашигла:

```sql
DECLARE EXIT HANDLER FOR SQLEXCEPTION
BEGIN
    GET DIAGNOSTICS CONDITION 1
        v_sqlstate = RETURNED_SQLSTATE,
        v_msg = MESSAGE_TEXT;
    ROLLBACK;
    SET p_ur_dun = CONCAT('Алдаа ', v_sqlstate, ': ', v_msg);
END;
```

> `GET DIAGNOSTICS` handler-ийн **эхний** statement байх ёстой. Өмнө нь
> өөр statement ажиллавал алдааны мэдээлэл цэвэрлэгдэж болно.

### SIGNAL — өөрөө алдаа үүсгэх

```sql
IF p_dun <= 0 THEN
    SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Дүн эерэг байх ёстой',
            MYSQL_ERRNO = 5001;
END IF;
```

`'45000'` нь «хэрэглэгчийн тодорхойлсон, боловсруулаагүй алдаа» гэсэн
стандарт SQLSTATE. `SQLEXCEPTION` handler үүнийг мөн барина.

### Товч жагсаалт

| Зорилго | MySQL |
|---|---|
| Алдаа барих | `DECLARE ... HANDLER` |
| Алдаа үүсгэх | `SIGNAL SQLSTATE '45000'` |
| Дахин шидэх | `RESIGNAL;` |
| Мессеж авах | `GET DIAGNOSTICS` |
| Хаана ажиллах | Зөвхөн routine (процедур, функц, trigger) дотор |

Энгийн скриптэд алдаа барих арга байхгүй — алдаа гармагц скрипт
зогсоно. Тиймээс алдааг зохицуулах логикийг процедурт бичнэ.

### Бусад анхааруулга

- Handler-гүй процедурт алдаа гарвал `START TRANSACTION` нээлттэй үлдэнэ.
  Холболт хаагдах эсвэл дараагийн `COMMIT` хүртэл түгжээ барьж болно.
- `SELECT ... INTO` мөр олохгүй бол алдаа биш, `NOT FOUND` анхааруулга
  өгч хувьсагч өөрчлөгдөхгүй. `IS NULL`-ээр шалга.
- DDL (`CREATE TABLE` г.м.) далд `COMMIT` хийдэг тул транзакц дотор бүү
  хэрэглэ.
""",
            initial_code="""\
USE delguur;

-- 0. Туршилтын данс хүснэгт (tur_ угтвартай, төгсгөлд устгана)
DROP PROCEDURE IF EXISTS tur_shiljuuleg;
DROP TABLE IF EXISTS tur_dans;

CREATE TABLE tur_dans (
    dans_id INT PRIMARY KEY,
    ezemshigch VARCHAR(50) NOT NULL,
    uldegdel DECIMAL(12,2) NOT NULL CHECK (uldegdel >= 0)
);

INSERT INTO tur_dans (dans_id, ezemshigch, uldegdel)
VALUES (1, 'Болд', 100000.00),
       (2, 'Сараа', 50000.00);

-- 1. Мөнгө шилжүүлэх процедур: алдаа гарвал бүгдийг буцаана
DELIMITER $$
CREATE PROCEDURE tur_shiljuuleg(
    IN  p_ilgeegch INT,
    IN  p_huleen_avagch INT,
    IN  p_dun DECIMAL(12,2),
    OUT p_ur_dun VARCHAR(255)
)
BEGIN
    DECLARE v_uldegdel DECIMAL(12,2);
    DECLARE v_sqlstate CHAR(5) DEFAULT '00000';
    DECLARE v_msg VARCHAR(255) DEFAULT '';

    -- Ямар ч алдаа: мэдээллийг авч, буцааж, мессежээр хариулна
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        GET DIAGNOSTICS CONDITION 1
            v_sqlstate = RETURNED_SQLSTATE,
            v_msg = MESSAGE_TEXT;
        ROLLBACK;
        SET p_ur_dun = CONCAT('Буцаагдлаа (', v_sqlstate, '): ', v_msg);
    END;

    IF p_dun <= 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Дүн эерэг байх ёстой';
    END IF;

    START TRANSACTION;

    -- FOR UPDATE: шалгах ба хасах хооронд өөр хүн өөрчлөхгүй
    SELECT uldegdel INTO v_uldegdel
    FROM tur_dans
    WHERE dans_id = p_ilgeegch
    FOR UPDATE;

    IF v_uldegdel IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Илгээгч данс олдсонгүй';
    ELSEIF v_uldegdel < p_dun THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Үлдэгдэл хүрэлцэхгүй';
    END IF;

    UPDATE tur_dans SET uldegdel = uldegdel - p_dun WHERE dans_id = p_ilgeegch;
    UPDATE tur_dans SET uldegdel = uldegdel + p_dun WHERE dans_id = p_huleen_avagch;

    -- Хүлээн авагч байхгүй бол эхний UPDATE-ийг ч буцаах ёстой
    IF ROW_COUNT() = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Хүлээн авагч данс олдсонгүй';
    END IF;

    COMMIT;
    SET p_ur_dun = 'Амжилттай';
END$$
DELIMITER ;

-- 2. Амжилттай шилжүүлэг: 1 -> 2, 30000
CALL tur_shiljuuleg(1, 2, 30000, @ur);
SELECT @ur AS ur_dun;

-- 3. Үлдэгдэл хүрэлцэхгүй
CALL tur_shiljuuleg(1, 2, 500000, @ur);
SELECT @ur AS ur_dun;

-- 4. Хүлээн авагч байхгүй: хасагдсан мөнгө буцаж ирнэ
CALL tur_shiljuuleg(1, 99, 10000, @ur);
SELECT @ur AS ur_dun;

-- 5. Буруу дүн
CALL tur_shiljuuleg(1, 2, -5, @ur);
SELECT @ur AS ur_dun;

-- Зөвхөн эхний шилжүүлэг үлдсэн: Болд 70000, Сараа 80000
SELECT * FROM tur_dans;

-- 6. Цэвэрлэх
DROP PROCEDURE IF EXISTS tur_shiljuuleg;
DROP TABLE IF EXISTS tur_dans;
""",
        ),
    ],
)

SECURITY_ADMIN = ModuleSpec(
    title="Модул 18 — Аюулгүй байдал ба удирдлага",
    description="Хэрэглэгч ба эрх, SQL injection, нөөцлөлт ба сэргээлт.",
    lessons=[
        LessonSpec(
            title="Хэрэглэгч, роль, GRANT ба REVOKE",
            slug="hereglegch-erh-grant-revoke",
            description="Хамгийн бага эрхийн зарчмаар програмын хэрэглэгч үүсгэх.",
            duration=660,
            language=MY,
            content="""\
Програм өгөгдлийн сантай `root` эрхээр холбогдох нь хамгийн
түгээмэл бөгөөд аюултай алдаа. Нэг SQL injection гарвал халдагч бүх
өгөгдлийн санг устгах боломжтой болно.

### Хамгийн бага эрхийн зарчим

Хэрэглэгч бүрт **ажилдаа яг хэрэгтэй** эрхийг л өг:

| Хэрэглэгч | Хэрэгтэй эрх |
|---|---|
| Онлайн дэлгүүрийн програм | Бараа унших, захиалга нэмэх |
| Тайлангийн хэрэгсэл | Зөвхөн унших, хувийн мэдээлэлгүй |
| Миграци ажиллуулагч | DDL (`CREATE`, `ALTER`) |
| Хүн (DBA) | Бүгд, гэхдээ өөрийн нэрээр |

### MySQL: хэрэглэгч = нэр + хост

```sql
CREATE USER 'delguur_app'@'localhost' IDENTIFIED BY 'Jishee#NuutsUg2024';
```

`'delguur_app'@'localhost'` ба `'delguur_app'@'%'` нь **өөр** хэрэглэгч.
`'%'` нь аль ч хостоос холбогдохыг зөвшөөрнө — боломжтой бол програмын
серверийн IP-г тодорхой бич.

```sql
GRANT SELECT ON delguur.* TO 'delguur_app'@'localhost';        -- бүх хүснэгт
GRANT INSERT ON delguur.zahialga TO 'delguur_app'@'localhost'; -- нэг хүснэгт
GRANT SELECT (hereglegch_id, ner) ON delguur.hereglegch
    TO 'delguur_tailan'@'localhost';                            -- багана
GRANT EXECUTE ON PROCEDURE delguur.hereglegchiin_tuuh
    TO 'delguur_app'@'localhost';                               -- процедур
REVOKE INSERT ON delguur.zahialga FROM 'delguur_app'@'localhost';
SHOW GRANTS FOR 'delguur_app'@'localhost';
```

`GRANT` ашиглавал `FLUSH PRIVILEGES` хэрэггүй.

### MySQL 8.0 роль

```sql
CREATE ROLE 'delguur_unshigch';
GRANT SELECT ON delguur.* TO 'delguur_unshigch';
GRANT 'delguur_unshigch' TO 'delguur_app'@'localhost';
SET DEFAULT ROLE ALL TO 'delguur_app'@'localhost';
```

> Роль олгосон ч **идэвхжүүлэхгүй** бол ажиллахгүй. `SET DEFAULT ROLE`
> хий, эсвэл сервер дээр `activate_all_roles_on_login = ON` тохируул.

### Хувийн мэдээллийг хаах

MySQL-д «хориглох» тушаал байхгүй — хэрэглэгч зөвхөн **өгсөн** эрхтэй.
Тиймээс хувийн баганыг (`email`, `utas`) хаахын тулд:

- Хүснэгт бүтнээр биш, **зөвшөөрөгдсөн баганад** л эрх өг:
  `GRANT SELECT (hereglegch_id, ner, hot) ON delguur.hereglegch TO …`
- Эсвэл хувийн баганагүй **view** (Модул 13) үүсгээд эрхийг view дээр өг.

| Үйлдэл | MySQL |
|---|---|
| Хэрэглэгч үүсгэх | `CREATE USER 'u'@'host' IDENTIFIED BY '…'` |
| Эрх олгох | `GRANT … ON сан.хүснэгт TO …` |
| Эрх цуцлах | `REVOKE … ON … FROM …` |
| Роль гишүүн болгох | `GRANT 'role' TO 'u'@'host'` |
| Эрх харах | `SHOW GRANTS FOR 'u'@'host'` |
| Түгжих | `ALTER USER 'u'@'host' ACCOUNT LOCK` |

> Энэ хичээлийн нууц үгс **зөвхөн жишээ**. Бодит системд урт, санамсаргүй
> нууц үг үүсгэж, кодод биш орчны хувьсагч эсвэл нууц сан (secret
> manager)-д хадгал.

### Бусад сайн туршлага

- Хүн бүр өөрийн нэртэй хэрэглэгчтэй байх — хуваалцсан `root` байхгүй
- Ашиглахаа больсон хэрэглэгчийг `DROP USER` эсвэл түгжих
  (`ALTER USER ... ACCOUNT LOCK`)
- Хүснэгтэд шууд эрх өгөхийн оронд процедур дээр `EXECUTE` өгөх
- Эрхийг тогтмол шалгах: `SHOW GRANTS`
""",
            initial_code="""\
-- АНХААР: админ (root) эрхээр ажиллуулна.
-- Нууц үгс зөвхөн жишээ. Бодит системд хэзээ ч бүү ашигла.
USE delguur;

-- 0. Дахин ажиллуулж болохуйц: байвал устгана
DROP USER IF EXISTS 'delguur_app'@'localhost', 'delguur_tailan'@'localhost';
DROP ROLE IF EXISTS 'delguur_unshigch', 'delguur_bichigch';

-- 1. Роль үүсгэж эрх олгох
CREATE ROLE 'delguur_unshigch', 'delguur_bichigch';

GRANT SELECT ON delguur.* TO 'delguur_unshigch';

GRANT INSERT, UPDATE ON delguur.zahialga TO 'delguur_bichigch';
GRANT INSERT ON delguur.zahialgiin_mur TO 'delguur_bichigch';

-- 2. Хэрэглэгч үүсгэх
CREATE USER 'delguur_app'@'localhost' IDENTIFIED BY 'Jishee#NuutsUg2024';
CREATE USER 'delguur_tailan'@'localhost' IDENTIFIED BY 'Jishee#Tailan2024';

-- 3. Програмд хоёр роль, идэвхжүүлнэ
GRANT 'delguur_unshigch', 'delguur_bichigch' TO 'delguur_app'@'localhost';
SET DEFAULT ROLE ALL TO 'delguur_app'@'localhost';

-- 4. Тайлангийн хэрэглэгч: зөвхөн хэрэгтэй хүснэгт, хувийн багана хаалттай
GRANT SELECT ON delguur.zahialga TO 'delguur_tailan'@'localhost';
GRANT SELECT ON delguur.zahialgiin_mur TO 'delguur_tailan'@'localhost';
GRANT SELECT ON delguur.baraa TO 'delguur_tailan'@'localhost';
GRANT SELECT ON delguur.angilal TO 'delguur_tailan'@'localhost';
GRANT SELECT (hereglegch_id, ner, hot) ON delguur.hereglegch
    TO 'delguur_tailan'@'localhost';

-- 5. Эрхийг шалгах
SHOW GRANTS FOR 'delguur_app'@'localhost';
SHOW GRANTS FOR 'delguur_app'@'localhost' USING 'delguur_unshigch', 'delguur_bichigch';
SHOW GRANTS FOR 'delguur_tailan'@'localhost';

-- 6. Эрх цуцлах: роль дээрээс UPDATE-ийг авна
REVOKE UPDATE ON delguur.zahialga FROM 'delguur_bichigch';
SHOW GRANTS FOR 'delguur_app'@'localhost' USING 'delguur_bichigch';

-- 7. Хэрэглэгчдийн жагсаалт
SELECT user, host, account_locked
FROM mysql.user
WHERE user LIKE 'delguur%';

-- Туршиж үзэх: шинэ терминалаас  mysql -u delguur_tailan -p
-- Дараа нь  SELECT email FROM delguur.hereglegch;  гэвэл эрхгүй гэсэн алдаа гарна

-- 8. Цэвэрлэх
DROP USER IF EXISTS 'delguur_app'@'localhost', 'delguur_tailan'@'localhost';
DROP ROLE IF EXISTS 'delguur_unshigch', 'delguur_bichigch';
""",
        ),
        LessonSpec(
            title="SQL injection ба параметртэй query",
            slug="sql-injection-parameterized",
            description="Мөр залгаж query бичих аюул, параметр ба prepared statement.",
            duration=690,
            language=MY,
            content="""\
**SQL injection** нь хэрэглэгчийн оруулсан текст SQL кодын хэсэг болж
ажиллах халдлага. Олон жилийн турш вэб аппликейшний хамгийн аюултай
эмзэг байдлын жагсаалтын тэргүүн эгнээнд байсаар ирсэн.

### Эмзэг код

```python
email = request.args["email"]
sql = "SELECT * FROM hereglegch WHERE email = '" + email + "'"
cursor.execute(sql)
```

Хэрэглэгч `bold@example.mn` гэж оруулбал хэвийн. Харин
`' OR '1'='1` гэж оруулбал:

```sql
SELECT * FROM hereglegch WHERE email = '' OR '1'='1'
```

Нөхцөл үргэлж үнэн — **бүх хэрэглэгчийн** мэдээлэл гарна. Нэвтрэх
хуудсан дээр бол нууц үггүйгээр нэвтэрнэ. `UNION SELECT`-ээр өөр
хүснэгтийн өгөгдлийг ч хулгайлж болно.

```javascript
// JavaScript — мөн адил эмзэг
const sql = `SELECT * FROM hereglegch WHERE email = '${email}'`;
const [rows] = await pool.query(sql);
```

> MySQL-ийн драйверууд нэг дуудлагад олон statement
> (`'; DROP TABLE hereglegch; --`) ажиллуулахыг ихэвчлэн анхдагчаар
> хориглодог (жишээ нь Node.js `mysql2`-ийн `multipleStatements: false`).
> Гэхдээ дээрх `OR`, `UNION` халдлага бүрэн ажиллана.

### Зөв арга: параметр

Query-ийн **бүтэц** ба **утгыг** тусад нь илгээнэ. Сервер утгыг хэзээ ч
код гэж тайлбарлахгүй:

```python
# mysql-connector-python, PyMySQL: %s
cursor.execute(
    "SELECT * FROM hereglegch WHERE email = %s",
    (email,),
)
```

> Python-ий `%s` энд мөр форматлах оператор **биш** — драйверийн
> орлуулагч. `"... = %s" % email` эсвэл f-string бичвэл дахиад эмзэг болно.

```javascript
// Node.js (mysql2)
const [rows] = await pool.execute(
  "SELECT * FROM hereglegch WHERE email = ?",
  [email],
);
```

### Сервер талын prepared statement

MySQL өөрөө ч параметртэй асуулгыг SQL-ээр бэлдэж чадна:

```sql
PREPARE haih FROM 'SELECT * FROM hereglegch WHERE email = ?';
SET @email = 'bold@example.mn';
EXECUTE haih USING @email;
DEALLOCATE PREPARE haih;
```

| Тушаал | Утга |
|---|---|
| `PREPARE нэр FROM 'SQL'` | Асуулгыг задлан бэлдэнэ, `?` нь утгын орлуулагч |
| `EXECUTE нэр USING @a, @b` | `?`-үүдийг хэрэглэгчийн хувьсагчийн (Модул 16) утгаар ажиллуулна |
| `DEALLOCATE PREPARE нэр` | Чөлөөлнө |

`?` нь `LIMIT`, `OFFSET`-д ч ажиллана — Модул 2-ын хуудаслалтыг
хувьсагчаар хийх арга: `LIMIT ? OFFSET ?`.

### Динамик SQL — процедур ч эмзэг байж болно

```sql
-- БУРУУ: процедур дотор ч мөр залгаж байна
SET @sql = CONCAT('SELECT * FROM hereglegch WHERE email = ''', p_email, '''');
PREPARE s FROM @sql;
EXECUTE s;
```

Параметрээр **зөвхөн утга** дамжина. Хүснэгт, баганын нэр, `ASC`/`DESC`
параметр болж чадахгүй. Ийм үед:

| Арга | MySQL |
|---|---|
| Зөвшөөрөгдсөн жагсаалт | `CASE` — зөвхөн мэдэгдэж буй нэрсийн аль нэгийг сонгоно |
| Нэрийг хашилтад оруулах | Backtick, доторх `` ` ``-г давхарлах |
| Объект байгаа эсэх | `information_schema.COLUMNS` |

Зөвшөөрөгдсөн жагсаалтын жишээг анхны кодын 5-р хэсгээс хар.

### Хамгаалалтын давхарга

1. **Үргэлж** параметр ашигла (ORM-ийн raw query-д ч)
2. Нэрийг зөвшөөрөгдсөн жагсаалтаар шалга
3. Програмын хэрэглэгчид хамгийн бага эрх (өмнөх хичээл)
4. Өгөгдлийн сангийн алдааны мессежийг хэрэглэгчид бүү харуул

> «Тусгай тэмдэгтийг escape хийх» арга найдваргүй: кодчилол, тэмдэгт
> орхигдох зэргээс болж алдаа гардаг. Параметр бол цорын ганц найдвартай
> хамгаалалт.
""",
            initial_code="""\
USE delguur;

-- 1. Prepared statement: ? нь утгын орлуулагч
PREPARE hereglegch_haih FROM
    'SELECT hereglegch_id, ovog, ner, hot FROM hereglegch WHERE email = ?';

SET @email = 'bold@example.mn';
EXECUTE hereglegch_haih USING @email;

-- 2. Халдлагын текстийг оруулбал: зүгээр л утга, 0 мөр буцна
SET @email = ''' OR ''1''=''1';
SELECT @email AS oroltiin_utga;
EXECUTE hereglegch_haih USING @email;

DEALLOCATE PREPARE hereglegch_haih;

-- 3. Олон параметр: дараалал нь USING доторх дараалалтай таарна
PREPARE baraa_haih FROM
    'SELECT ner, une, uldegdel FROM baraa WHERE angilal_id = ? AND une <= ? ORDER BY une';

SET @angilal = 1;
SET @deed_une = 1500000;
EXECUTE baraa_haih USING @angilal, @deed_une;

DEALLOCATE PREPARE baraa_haih;

-- 4. Эмзэг жишээг харах: мөр залгавал ямар SQL үүсэхийг хэвлэнэ (ажиллуулахгүй)
SET @oroltoo = ''' OR ''1''=''1';
SELECT CONCAT('SELECT * FROM hereglegch WHERE email = ''', @oroltoo, '''') AS aiultai_sql;

-- 5. Баганын нэрийг параметр болгож болохгүй: зөвшөөрөгдсөн жагсаалтаас сонгоно
SET @erembe = 'une';
SET @sql = CONCAT(
    'SELECT ner, une, uldegdel FROM baraa ORDER BY ',
    CASE @erembe
        WHEN 'une' THEN 'une'
        WHEN 'ner' THEN 'ner'
        ELSE 'baraa_id'
    END,
    ' LIMIT 5'
);
SELECT @sql AS uusgesen_sql;

PREPARE dinamik FROM @sql;
EXECUTE dinamik;
DEALLOCATE PREPARE dinamik;

-- 6. LIMIT, OFFSET-д ч параметр: 2-р хуудас, 5 мөрөөр
PREPARE huudas FROM
    'SELECT baraa_id, ner FROM baraa ORDER BY baraa_id LIMIT ? OFFSET ?';

SET @hemjee = 5;
SET @alsah = (2 - 1) * @hemjee;
EXECUTE huudas USING @hemjee, @alsah;

DEALLOCATE PREPARE huudas;
""",
        ),
        LessonSpec(
            title="Нөөцлөлт ба сэргээлт",
            slug="backup-restore",
            description="mysqldump, сэргээлт, binary log, 3-2-1 дүрэм ба хүснэгтийн хуулбараар сэргээх.",
            duration=660,
            language=MY,
            content="""\
Диск эвдрэх, санамсаргүй `DELETE`, ransomware — нөөцгүй бол өгөгдөл
буцаж ирэхгүй. **Сэргээж үзээгүй нөөц бол нөөц биш.**

### Хоёр гол асуулт

| Ойлголт | Асуулт |
|---|---|
| **RPO** | Хамгийн ихдээ хэдэн минутын өгөгдөл алдаж болох вэ? |
| **RTO** | Хэдэн цагийн дотор ажиллагаа сэргэх ёстой вэ? |

Хариултаас хамаарч нөөцлөх давтамж, төрлийг сонгоно.

### `mysqldump` — логик нөөц

`mysqldump` бол SQL тушаал биш, **тушаалын мөрийн програм** — MySQL-тэй
хамт суудаг (Модул 1). Санг `CREATE TABLE`, `INSERT` бүхий SQL скрипт
болгон гаргана. Терминалд ажиллуулна:

```bash
mysqldump -u root -p --single-transaction --routines --events \\
    --databases delguur --result-file=delguur_2024-06-30.sql
```

| Сонголт | Утга |
|---|---|
| `--single-transaction` | InnoDB-г түгжихгүйгээр тогтвортой агшинд нөөцөлнө (Модул 14-ийн snapshot) |
| `--routines`, `--events` | Процедур, функц, event (анхдагчаар ордоггүй) |
| `--databases` | `CREATE DATABASE` ба `USE` мөрийг оруулна |
| `--result-file` | Файлд шууд бичнэ |

Trigger анхдагчаар ордог (`--triggers`). Гарсан файл нь Модул 1-ийн
`delguur` скрипттэй яг ижил төрлийн SQL — нээж уншиж болно.

### Сэргээх

```bash
# Шинэ нэртэй сан руу туршиж сэргээх (--databases-гүй хийсэн dump бол)
mysql -u root -p -e "CREATE DATABASE delguur_test"
mysql -u root -p delguur_test < delguur_2024-06-30.sql
```

`--databases`-тэй хийсэн dump өөрөө `USE delguur` агуулдаг тул **анхны
сан руу** сэргээнэ — туршихдаа болгоомжтой.

> **Windows PowerShell:** `<` оролтын чиглүүлэлт ажиллахгүй, `>` нь
> UTF-16 файл үүсгэж болно. `--result-file` ашигла, сэргээхдээ `mysql`
> клиент дотор `SOURCE delguur_2024-06-30.sql;` эсвэл `cmd /c "... < ..."`.

### Том сан ба цэг хугацаанд сэргээх

| Хэрэгсэл | Төрөл | Хэзээ |
|---|---|---|
| `mysqldump` | Логик (SQL) | Жижиг, дунд сан; өөр хувилбар руу шилжих |
| MySQL Shell `util.dumpInstance()` | Логик, зэрэгцээ | Том сан — олон урсгалаар хурдан |
| Percona XtraBackup | Физик (файл) | Маш том сан — файлыг шууд хуулна |
| Binary log + `mysqlbinlog` | Өөрчлөлтийн бүртгэл | Цэг хугацаанд сэргээх |

**Binary log** нь сервер дээр хийгдсэн өөрчлөлт бүрийг бичдэг (MySQL 8-д
анхдагчаар асаалттай). Шөнийн бүтэн нөөц + түүнээс хойшхи binary log
байвал алдаатай `DELETE`-ийн **яг өмнөх** агшин хүртэл сэргээж болно:

```bash
mysqlbinlog --stop-datetime="2024-06-30 14:25:00" binlog.000042 | mysql -u root -p
```

### Сэргээлтийг шалгах

- Нөөцийг **тестийн сервер** эсвэл өөр нэртэй сан руу бүрэн сэргээ.
- Хүснэгт бүрийн мөрийн тоо, гол дүнг (жишээ нь нийт борлуулалт)
  анхны сантай харьцуул.
- Процедур, trigger, хэрэглэгчийн эрх хамт сэргэсэн эсэхийг шалга.

### Сан доторх хурдан хуулбар

Эрсдэлтэй `UPDATE`, `DELETE`-ийн өмнө хүснэгтийн **хуулбар** авах нь
энгийн, хурдан хамгаалалт:

```sql
CREATE TABLE baraa_nuuts_20240630 AS SELECT * FROM baraa;
```

Алдаа гарвал хуулбараас `JOIN`-той `UPDATE` (Модул 9) эсвэл
`INSERT … SELECT`-ээр (Модул 7) сэргээнэ. Энэ бол **бүрэн нөөцийн орлуулга
биш**: нэг сервер дээр байгаа тул сервер эвдэрвэл хамт алга болно. Мөн
`CREATE TABLE … AS SELECT` түлхүүр, index-ийг хуулдаггүй — бүтцийг бүрэн
хуулах бол `CREATE TABLE … LIKE` + `INSERT … SELECT` (Модул 6).

Энэ хичээлийн код яг ийм «осол» ба сэргээлтийг дуурайна. (Энэ сайт дээр
ажиллуулалт бүр анхны сангаас эхэлдэг тул `delguur` эвдрэхгүй.)

### 3-2-1 дүрэм

- **3** хуулбар (үндсэн өгөгдөл + 2 нөөц)
- **2** өөр төрлийн хадгалалт (локал диск + объект сан г.м.)
- **1** хуулбар өөр байршилд (offsite / cloud)

Нэмээд: нөөцийг шифрлэ, хандах эрхийг хязгаарла, **сэргээлтийг тогтмол
турш** — сард ядаж нэг удаа.
""",
            initial_code="""\
USE delguur;

-- 1. Эрсдэлтэй өөрчлөлтийн өмнө хүснэгтийн хуулбар
DROP TABLE IF EXISTS baraa_nuuts_20240630;
CREATE TABLE baraa_nuuts_20240630 AS SELECT * FROM baraa;

SELECT COUNT(*) AS huulsan_mur FROM baraa_nuuts_20240630;    -- 12

-- 2. «Осол»: WHERE мартсан UPDATE бүх үнийг 0 болголоо
UPDATE baraa SET une = 0;
SELECT baraa_id, ner, une FROM baraa ORDER BY baraa_id LIMIT 3;

-- 3. Хуулбараас сэргээх: JOIN-той UPDATE
UPDATE baraa AS b
JOIN baraa_nuuts_20240630 AS n ON n.baraa_id = b.baraa_id
SET b.une = n.une;

-- 4. Шалгах: хуулбартай зөрөх мөр 0 байх ёстой
SELECT COUNT(*) AS zoruutei_mur
FROM baraa AS b
JOIN baraa_nuuts_20240630 AS n ON n.baraa_id = b.baraa_id
WHERE b.une <> n.une OR b.uldegdel <> n.uldegdel;

-- 5. Сэргээлтийг турших сан: өөр нэртэй сан руу хуулна
DROP DATABASE IF EXISTS delguur_test;
CREATE DATABASE delguur_test;

-- LIKE нь бүтцийг (PK, index) бүрэн хуулна, INSERT ... SELECT өгөгдлийг
CREATE TABLE delguur_test.angilal LIKE delguur.angilal;
INSERT INTO delguur_test.angilal SELECT * FROM delguur.angilal;

CREATE TABLE delguur_test.baraa LIKE delguur.baraa;
INSERT INTO delguur_test.baraa SELECT * FROM delguur.baraa;

-- 6. Анхны ба хуулбар сангийн мөрийн тоо, нийт үнийг харьцуулах
SELECT 'delguur' AS san, COUNT(*) AS mur, SUM(une) AS niit_une FROM delguur.baraa
UNION ALL
SELECT 'delguur_test', COUNT(*), SUM(une) FROM delguur_test.baraa;

-- PRIMARY KEY, index, CHECK хуулагдсан; FOREIGN KEY хуулагдахгүй
SHOW CREATE TABLE delguur_test.baraa;

-- 7. Цэвэрлэх
DROP DATABASE IF EXISTS delguur_test;
DROP TABLE IF EXISTS baraa_nuuts_20240630;

-- mysqldump, mysqlbinlog нь терминалын програм — энд биш, өөрийн компьютер
-- дээр ажиллуулна (тайлбарыг үз).
""",
        ),
    ],
)

SQL_ADVANCED_MODULES = [CTE_WINDOW, PROCEDURES, TRIGGERS_ERRORS, SECURITY_ADMIN]
