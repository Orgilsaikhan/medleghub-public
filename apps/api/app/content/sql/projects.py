"""Модул 19-20 — Төсөл: дэлгүүрийн тайлан, номын сангийн систем.

Өмнөх бүх модулийн мэдлэгийг нэгтгэх хоёр том даалгавар. Хичээл бүр
эхлээд шаардлагыг тавьж, зөвлөгөө өгөөд, дараа нь шийдлийг алхам алхмаар тайлбарлана.
"""

from app.content.types import LessonSpec, ModuleSpec
from app.models.enums import LessonLanguage

MY = LessonLanguage.MYSQL

SHOP_REPORT = ModuleSpec(
    title="Модул 19 — Төсөл: Дэлгүүрийн борлуулалтын тайлан",
    description="delguur сан дээр удирдлагад зориулсан бодит тайлан бэлдэнэ.",
    lessons=[
        LessonSpec(
            title="Шаардлага ба үндсэн үзүүлэлт",
            slug="delguur-tailan-undsen-uzuulelt",
            description="Орлого, ангиллын хувь, шилдэг хэрэглэгчийг тооцоолох.",
            duration=660,
            language=MY,
            content="""\
Энэ модулиас эхлэн шинэ зүйл үзэхгүй. Удирдлагаас ирсэн **бодит хүсэлтийг**
өмнө сурсан JOIN, GROUP BY, CASE, CTE, цонхон функцээр шийднэ.

### Даалгавар

Дэлгүүрийн захирал Батбаяр дараах тоонуудыг хүсчээ:

1. **Нийт орлого**, захиалгын тоо, нэг захиалгын дундаж дүн
2. Орлого **захиалгын төлөвөөр** (хүргэгдсэн / хүлээгдэж буй / цуцлагдсан)
3. **Ангилал бүрийн орлого** ба нийт орлогод эзлэх хувь — борлуулалтгүй
   ангилал ч жагсаалтад харагдах ёстой
4. Орлогоороо **шилдэг 3 хэрэглэгч** — тэнцсэн бол бүгдийг нь харуулна

> **Бизнесийн тодорхойлолт:** «Орлого» = цуцлагдсанаас бусад захиалгын
> `too * negj_une`-ийн нийлбэр. Тайлан эхлэхээс өмнө ийм тодорхойлолтыг
> заавал тохиролцоорой — «зөвхөн хүргэгдсэн» гэж тооцвол тоо өөр гарна.

### Зөвлөгөө

- Мөрийн дүн `zahialgiin_mur`-т, төлөв `zahialga`-д байгаа тул JOIN хэрэгтэй.
- Дундаж захиалгыг шууд `AVG(too * negj_une)` гэвэл **мөрийн** дундаж гарна.
  Эхлээд захиалга бүрийн дүнг дэд асуулгаар гаргаад дараа нь `AVG` ав.
- Ангилал бүрийг харуулахын тулд `angilal`-аас эхэлж `LEFT JOIN` хий, цуцлалтын
  шүүлтүүрийг CTE дотор хий — `WHERE` дээр тавьбал `LEFT JOIN` нь `INNER` болно.
- «Тэнцсэнийг нь ч харуул» гэдэг нь `RANK()`-ийн ажил.

### Шийдэл 1 — нийт үзүүлэлт

```sql
SELECT COUNT(*) AS zahialga_too, SUM(dun) AS niit_orlogo,
       ROUND(AVG(dun), 2) AS dundaj_zahialga
FROM (SELECT z.zahialga_id, SUM(zm.too * zm.negj_une) AS dun
      FROM zahialga AS z
      JOIN zahialgiin_mur AS zm ON zm.zahialga_id = z.zahialga_id
      WHERE z.tuluv <> 'Цуцлагдсан'
      GROUP BY z.zahialga_id) AS t;
```

| zahialga_too | niit_orlogo | dundaj_zahialga |
|---|---|---|
| 9 | 7991000.00 | 887888.89 |

Төлөвөөр задлахдаа `SUM(CASE WHEN ... THEN dun END)` хэлбэрийн **нөхцөлт
нэгтгэл** хэрэглэнэ: хүргэгдсэн 4 353 000, хүлээгдэж буй 3 638 000,
цуцлагдсан 3 200 000. Эхний хоёрын нийлбэр 7 991 000 — тоо таарч байна.

### Шийдэл 2 — ангиллын орлого

`SUM(SUM(dun)) OVER ()` нь «бүлэглэсний дараах бүх мөрийн нийлбэр» — өөрөөр
хэлбэл нийт орлого. Түүнд хувааж хувийг олно.

| angilal | orlogo | huvi |
|---|---|---|
| Электроник | 6056000.00 | 75.79 |
| Гэр ахуй | 1002000.00 | 12.54 |
| Хувцас | 435000.00 | 5.44 |
| Ном | 297000.00 | 3.72 |
| Хүнс | 201000.00 | 2.52 |

> **Шалгах дадал:** ангиллын орлогын нийлбэр нийт орлоготой (7 991 000)
> тэнцэх ёстой. Тайлан бүрт ийм «хяналтын нийлбэр» тавь.

### Шийдэл 3 — шилдэг хэрэглэгч, тэнцэлтэй

`ORDER BY orlogo DESC LIMIT 3` нь тэнцсэн мөрүүдийг тоохгүй таслана
(Модул 2). Оронд нь `RANK()`-ээр байр тооцоод `WHERE bair <= 3` гэж
шүүнэ:

| Хэрэгцээ | MySQL |
|---|---|
| Яг N мөр | `ORDER BY … LIMIT 3` |
| Тэнцсэнийг оруулах | `RANK()` + `WHERE bair <= 3` |

Орлогоор тэнцсэн хэрэглэгч манай өгөгдөлд алга. Харин **захиалгын тоогоор**
эрэмбэлэхэд Номин, Анар, Хулан, Энх бүгд 1 захиалгатай тул хамтдаа 3-р байр
эзэлнэ — `RANK()` 6 мөр буцаана, `ROW_NUMBER()` бол дурын 3-ыг нь сонгож
бусдыг нь шударга бусаар хасна.

| hereglegch | zahialga_too | orlogo | orlogo_bair |
|---|---|---|---|
| Батын Болд | 3 | 4835000.00 | 1 |
| Эрдэнийн Анар | 1 | 1620000.00 | 2 |
| Цэрэнгийн Номин | 1 | 680000.00 | 3 |

> Тэмүүлэнгийн цорын ганц захиалга цуцлагдсан, Мөнх захиалга хийгээгүй тул
> энэ жагсаалтад орохгүй — `JOIN` тэднийг хасна.
""",
            initial_code="""\
USE delguur;

-- ===== 1. Нийт үзүүлэлт (цуцлагдсан захиалгыг тооцохгүй) =====
-- Эхлээд захиалга бүрийн дүн, дараа нь түүн дээрээ COUNT, SUM, AVG
SELECT COUNT(*)            AS zahialga_too,
       SUM(dun)            AS niit_orlogo,
       ROUND(AVG(dun), 2)  AS dundaj_zahialga
FROM (
    SELECT z.zahialga_id, SUM(zm.too * zm.negj_une) AS dun
    FROM zahialga AS z
    JOIN zahialgiin_mur AS zm ON zm.zahialga_id = z.zahialga_id
    WHERE z.tuluv <> 'Цуцлагдсан'
    GROUP BY z.zahialga_id
) AS t;

-- ===== 2. Төлөвөөр задалсан орлого (нөхцөлт нэгтгэл) =====
SELECT
    SUM(CASE WHEN z.tuluv = 'Хүргэгдсэн' THEN zm.too * zm.negj_une ELSE 0 END)
        AS hurgegdsen,
    SUM(CASE WHEN z.tuluv = 'Хүлээгдэж буй' THEN zm.too * zm.negj_une ELSE 0 END)
        AS huleegdej_bui,
    SUM(CASE WHEN z.tuluv = 'Цуцлагдсан' THEN zm.too * zm.negj_une ELSE 0 END)
        AS tsutslagdsan
FROM zahialga AS z
JOIN zahialgiin_mur AS zm ON zm.zahialga_id = z.zahialga_id;

-- ===== 3. Ангилал бүрийн орлого ба эзлэх хувь =====
-- Шүүлтүүрийг CTE дотор хийснээр LEFT JOIN бүх ангиллыг хадгална
WITH mur_orlogo AS (
    SELECT zm.baraa_id, zm.too, zm.too * zm.negj_une AS dun
    FROM zahialgiin_mur AS zm
    JOIN zahialga AS z ON z.zahialga_id = zm.zahialga_id
    WHERE z.tuluv <> 'Цуцлагдсан'
)
SELECT a.ner                                   AS angilal,
       COALESCE(SUM(mo.too), 0)                AS zarsan_too,
       COALESCE(SUM(mo.dun), 0)                AS orlogo,
       -- SUM(SUM(...)) OVER () = бүх ангиллын нийлбэр буюу нийт орлого
       ROUND(COALESCE(SUM(mo.dun), 0) * 100 / SUM(SUM(mo.dun)) OVER (), 2) AS huvi
FROM angilal AS a
LEFT JOIN baraa AS b       ON b.angilal_id = a.angilal_id
LEFT JOIN mur_orlogo AS mo ON mo.baraa_id = b.baraa_id
GROUP BY a.angilal_id, a.ner
ORDER BY orlogo DESC;

-- ===== 4. Шилдэг хэрэглэгч (тэнцсэнийг нь ч оруулна) =====
WITH hereglegch_orlogo AS (
    SELECT h.hereglegch_id,
           CONCAT(h.ovog, ' ', h.ner)      AS hereglegch,
           COUNT(DISTINCT z.zahialga_id)   AS zahialga_too,
           SUM(zm.too * zm.negj_une)       AS orlogo
    FROM hereglegch AS h
    JOIN zahialga AS z        ON z.hereglegch_id = h.hereglegch_id
    JOIN zahialgiin_mur AS zm ON zm.zahialga_id = z.zahialga_id
    WHERE z.tuluv <> 'Цуцлагдсан'
    GROUP BY h.hereglegch_id, h.ovog, h.ner
),
bairlal AS (
    SELECT ho.*,
           RANK() OVER (ORDER BY ho.orlogo DESC)       AS orlogo_bair,
           RANK() OVER (ORDER BY ho.zahialga_too DESC) AS zahialga_bair
    FROM hereglegch_orlogo AS ho
)
SELECT hereglegch, zahialga_too, orlogo, orlogo_bair
FROM bairlal
WHERE orlogo_bair <= 3
ORDER BY orlogo_bair;

-- ===== 5. Захиалгын тоогоор — энд тэнцэл гарна =====
-- RANK: 1, 2, 3, 3, 3, 3 (6 мөр). ROW_NUMBER бол 3-ыг л авна.
WITH hereglegch_too AS (
    SELECT h.hereglegch_id,
           CONCAT(h.ovog, ' ', h.ner)    AS hereglegch,
           COUNT(*)                      AS zahialga_too
    FROM hereglegch AS h
    JOIN zahialga AS z ON z.hereglegch_id = h.hereglegch_id
    WHERE z.tuluv <> 'Цуцлагдсан'
    GROUP BY h.hereglegch_id, h.ovog, h.ner
)
SELECT *
FROM (
    SELECT ht.hereglegch, ht.zahialga_too,
           RANK()       OVER (ORDER BY ht.zahialga_too DESC) AS bair,
           ROW_NUMBER() OVER (ORDER BY ht.zahialga_too DESC) AS dugaar
    FROM hereglegch_too AS ht
) AS r
WHERE r.bair <= 3
ORDER BY r.bair, r.hereglegch;
""",
        ),
        LessonSpec(
            title="Сарын чиг хандлага",
            slug="delguur-sariin-chig-handlaga",
            description="Сарын орлого, хуримтлал, өсөлтийн хувь, сарын шилдэг бараа, тайлангийн процедур.",
            duration=720,
            language=MY,
            content="""\
### Даалгавар

Санхүүгийн менежер Оюунаа сар бүрийн тайлан хүсэв:

1. Сар бүрийн **захиалгын тоо ба орлого** (цуцлагдсаныг хасна)
2. Оны эхнээс **хуримтлагдсан орлого** (running total)
3. Өмнөх сартай харьцуулсан **өсөлтийн хувь** (month-over-month)
4. Сар бүрийн **хамгийн их зарагдсан бараа** (тоо ширхгээр, тэнцвэл орлогоор)
5. Дээрхийг огнооны мужаар дуудаж болох **процедур** болгох

### Зөвлөгөө

- Сарыг `DATE_FORMAT(ognoo, '%Y-%m')` гэж `'2024-03'` хэлбэрт шилжүүл.
  Энэ мөр цагаан толгойн дарааллаар эрэмбэлэхэд он сарын дараалалтай ижил.
- Эхлээд сарын нэгтгэлийг CTE-д гарга, цонхон функцийг дараа нь хэрэглэ.
- `LAG(orlogo) OVER (ORDER BY sar)` өмнөх сарын орлогыг өгнө.
- Тэгээр хуваахаас `NULLIF(..., 0)`-оор сэргийл.
- Бүлэг бүрээс нэг мөр авах = `ROW_NUMBER() OVER (PARTITION BY ...)` + `WHERE mur = 1`.
- Процедурын параметрийг шалгаад буруу бол `SIGNAL`-аар алдаа өг (Модул 17).

### Шийдэл 1 — сарын нэгтгэл, хуримтлал, өсөлт

```sql
SUM(orlogo) OVER (ORDER BY sar ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
```

`ROWS ...` хэсгийг заавал бич: `ORDER BY`-тай `OVER`-ийн анхдагч хүрээ нь
`RANGE` бөгөөд ижил утгатай мөрүүдийг нэг дор нэмдэг (Модул 15).

| sar | zahialga_too | orlogo | hurimtlal | osolt_huvi |
|---|---|---|---|---|
| 2024-02 | 2 | 1645000.00 | 1645000.00 | NULL |
| 2024-03 | 1 | 118000.00 | 1763000.00 | -92.83 |
| 2024-04 | 2 | 2300000.00 | 4063000.00 | 1849.15 |
| 2024-05 | 2 | 435000.00 | 4498000.00 | -81.09 |
| 2024-06 | 2 | 3493000.00 | 7991000.00 | 702.99 |

Эхний сард өмнөх сар байхгүй тул `LAG` нь `NULL`, хувь ч `NULL` — энэ зөв.

### Шийдэл 2 — сарын шилдэг бараа

| sar | baraa | too | orlogo |
|---|---|---|---|
| 2024-02 | Цайны аяга | 4 | 72000.00 |
| 2024-03 | Монгол түүх | 2 | 70000.00 |
| 2024-04 | Ааруул | 10 | 120000.00 |
| 2024-05 | Сүүтэй цай | 6 | 21000.00 |
| 2024-06 | Ааруул | 5 | 60000.00 |

> Тоогоор тэнцсэн бараа гарвал `ROW_NUMBER` нэгийг л сонгоно — тиймээс
> `ORDER BY too DESC, orlogo DESC` гэж хоёр дахь шалгуурыг тодорхой өгөв.
> Тэнцсэн бүгдийг харуулах бол `RANK()` хэрэглэ.

### Шийдэл 3 — процедур

`sp_sariin_tailan(p_ehlel, p_tugsgul)` нь эхлэх огноо дуусахаас хойш бол
`SIGNAL`-аар алдаа өгч, эс бөгөөс мужийн сарын тайланг буцаана:

```sql
CALL sp_sariin_tailan('2024-04-01', '2024-06-30');
```

Процедур зөвхөн мужийн доторх өгөгдлийг хардаг тул хуримтлал 4-р сараас
эхэлж (2 300 000 → 2 735 000 → 6 228 000), 4-р сарын өсөлт `NULL` гарна.

Дуусах өдрийг бүтнээр нь оруулахын тулд `zahialsan_ognoo < p_tugsgul +
INTERVAL 1 DAY` гэж шүүнэ — `DATETIME` багана дээр `<= '2024-06-30'` бол
тэр өдрийн 00:00-оос хойшхи захиалга хасагдана (Модул 3).

> Захиалгагүй сар байвал тэр сар тайланд огт гарахгүй. Бодит тайланд
> рекурсив CTE-ээр бүх сарыг үүсгээд `LEFT JOIN` хийдэг (Модул 15).
""",
            initial_code="""\
USE delguur;

-- ===== 1. Сарын орлого, хуримтлал, өмнөх сартай харьцуулалт =====
WITH sariin_orlogo AS (
    SELECT DATE_FORMAT(z.zahialsan_ognoo, '%Y-%m') AS sar,
           COUNT(DISTINCT z.zahialga_id)            AS zahialga_too,
           SUM(zm.too * zm.negj_une)                AS orlogo
    FROM zahialga AS z
    JOIN zahialgiin_mur AS zm ON zm.zahialga_id = z.zahialga_id
    WHERE z.tuluv <> 'Цуцлагдсан'
    GROUP BY DATE_FORMAT(z.zahialsan_ognoo, '%Y-%m')
)
SELECT sar,
       zahialga_too,
       orlogo,
       -- Хуримтлагдсан орлого
       SUM(orlogo) OVER (ORDER BY sar
                         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS hurimtlal,
       -- Өмнөх сарын орлого
       LAG(orlogo) OVER (ORDER BY sar) AS omnoh_sar,
       -- Өсөлтийн хувь; эхний сард NULL
       ROUND((orlogo - LAG(orlogo) OVER (ORDER BY sar)) * 100
             / NULLIF(LAG(orlogo) OVER (ORDER BY sar), 0), 2) AS osolt_huvi
FROM sariin_orlogo
ORDER BY sar;

-- ===== 2. Сар бүрийн хамгийн их зарагдсан бараа =====
WITH sariin_baraa AS (
    SELECT DATE_FORMAT(z.zahialsan_ognoo, '%Y-%m') AS sar,
           b.ner                                    AS baraa,
           SUM(zm.too)                              AS too,
           SUM(zm.too * zm.negj_une)                AS orlogo
    FROM zahialga AS z
    JOIN zahialgiin_mur AS zm ON zm.zahialga_id = z.zahialga_id
    JOIN baraa AS b           ON b.baraa_id = zm.baraa_id
    WHERE z.tuluv <> 'Цуцлагдсан'
    GROUP BY DATE_FORMAT(z.zahialsan_ognoo, '%Y-%m'), b.baraa_id, b.ner
),
dugaarlasan AS (
    SELECT sb.*,
           ROW_NUMBER() OVER (PARTITION BY sb.sar
                              ORDER BY sb.too DESC, sb.orlogo DESC) AS mur
    FROM sariin_baraa AS sb
)
SELECT sar, baraa, too, orlogo
FROM dugaarlasan
WHERE mur = 1
ORDER BY sar;

-- ===== 3. Огнооны мужаар дууддаг процедур =====
DROP PROCEDURE IF EXISTS sp_sariin_tailan;

DELIMITER $$
CREATE PROCEDURE sp_sariin_tailan(
    IN p_ehlel   DATE,
    IN p_tugsgul DATE
)
BEGIN
    IF p_ehlel > p_tugsgul THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Эхлэх огноо дуусах огнооноос хойш байна.',
                MYSQL_ERRNO = 5001;
    END IF;

    WITH sariin_orlogo AS (
        SELECT DATE_FORMAT(z.zahialsan_ognoo, '%Y-%m') AS sar,
               COUNT(DISTINCT z.zahialga_id)            AS zahialga_too,
               SUM(zm.too * zm.negj_une)                AS orlogo
        FROM zahialga AS z
        JOIN zahialgiin_mur AS zm ON zm.zahialga_id = z.zahialga_id
        WHERE z.tuluv <> 'Цуцлагдсан'
          -- Сүүлийн өдрийг бүтнээр нь оруулахын тулд дараагийн өдрөөс бага
          AND z.zahialsan_ognoo >= p_ehlel
          AND z.zahialsan_ognoo <  p_tugsgul + INTERVAL 1 DAY
        GROUP BY DATE_FORMAT(z.zahialsan_ognoo, '%Y-%m')
    )
    SELECT sar,
           zahialga_too,
           orlogo,
           SUM(orlogo) OVER (ORDER BY sar
                             ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS hurimtlal,
           ROUND((orlogo - LAG(orlogo) OVER (ORDER BY sar)) * 100
                 / NULLIF(LAG(orlogo) OVER (ORDER BY sar), 0), 2) AS osolt_huvi
    FROM sariin_orlogo
    ORDER BY sar;
END$$
DELIMITER ;

-- ===== 4. Процедурыг турших =====
CALL sp_sariin_tailan('2024-04-01', '2024-06-30');

-- Буруу муж: ERROR 5001 (45000) — туршихдаа тайлбарыг арилга
-- CALL sp_sariin_tailan('2024-06-30', '2024-01-01');
""",
        ),
        LessonSpec(
            title="Үйл ажиллагааны хяналтын самбар",
            slug="delguur-hyanaltiin-samber",
            description="Нөөцийн анхааруулга, идэвхгүй хэрэглэгч, бүгдийг view болгох.",
            duration=660,
            language=MY,
            content="""\
Тайлан бүрийг өдөр бүр гараар бичих нь алдаа гаргана. Энэ хичээлд
асуулгуудыг **view** болгож, хяналтын самбар (dashboard) програм нэг
`SELECT`-ээр авдаг болгоно.

### Даалгавар

Агуулахын менежер Ганзориг болон маркетингийн баг дараахыг хүсэв:

1. **Нөөцийн анхааруулга:** үлдэгдэл 10-аас бага бараа. Дууссан (0) бол
   «Дууссан», бусад нь «Бага» гэж тэмдэглэ. Хэр их зарагддагийг нь харуулж
   захиалах эрэмбийг тогтооход тусал.
2. **Идэвхгүй хэрэглэгч:** сүүлийн **60 хоногт** (цуцлагдаагүй) захиалга
   хийгээгүй хэрэглэгч — огт захиалгагүй хүмүүсийг ч оруул.
3. Ангиллын орлого (энэ модулийн эхний хичээлийнх)
4. Бүх гол тоог **нэг мөрөөр** буцаах самбарын view

### Тогтмол лавлах огноо

«Сүүлийн 60 хоног» нь өнөөдрөөс хамаарна. Жишээ өгөгдөл 2024 оных тул
`CURDATE()` хэрэглэвэл хэн нэгэн хэзээ ажиллуулахаас хамаарч үр дүн өөр
гарна. Тиймээс **лавлах огноог `2024-06-30`** гэж тогтооно:

```sql
-- Сургалтад
DATE '2024-06-30' - INTERVAL 60 DAY      -- 2024-05-01
-- Бодит системд
CURDATE() - INTERVAL 60 DAY
```

> MySQL-ийн view дотор `@huvisagch` хэрэглэж **болохгүй** (алдаа 1351).
> Тиймээс огноог view дотор шууд бичнэ. Параметртэй тайлан хэрэгтэй бол
> процедур эсвэл програмын талаас `WHERE` нэмнэ.

### Зөвлөгөө

- Анхааруулгад борлуулалтын тоог `LEFT JOIN (дэд асуулга)`-аар нэм —
  Гутал хэзээ ч зарагдаагүй ч жагсаалтад гарах ёстой.
- Идэвхгүй хэрэглэгчид `LEFT JOIN` + `GROUP BY` + `HAVING MAX(...) IS NULL OR ...`.
  Цуцлалтын нөхцөлийг `ON` дотор тавь.
- View бусад view-ээс уншиж болно — самбар нь бусад view дээр тулгуурлана.

### Шийдэл — хүлээгдэж буй үр дүн

`v_baraa_anhaaruulga`:

| baraa | uldegdel | zarsan_too | tuluv |
|---|---|---|---|
| Сүүтэй цай | 0 | 6 | Дууссан |
| Гутал | 0 | 0 | Дууссан |
| Тоос сорогч | 4 | 1 | Бага |
| Зөөврийн компьютер | 6 | 1 | Бага |
| Хөнжил | 9 | 2 | Бага |

`v_idevhgui_hereglegch`: Цэрэнгийн Номин (89 хоног), Эрдэнийн Анар (73 хоног),
Ганбаатарын Тэмүүлэн, Сүхийн Мөнх (`NULL` — цуцлагдаагүй захиалга байхгүй).

`v_hyanaltiin_samber`:

| niit_orlogo | huleegdej_bui | anhaaruulga_baraa | idevhgui_hereglegch |
|---|---|---|---|
| 7991000.00 | 3 | 5 | 4 |

### View-ийн давуу ба анхаарах зүйл

| Давуу тал | Анхаарах зүйл |
|---|---|
| Логик нэг газар — «орлого»-ын тодорхойлолт өөрчлөгдвөл нэг view засна | View нь өгөгдөл хадгалдаггүй, дуудах бүрт асуулга дахин ажиллана |
| Програм, BI хэрэгсэлд энгийн хүснэгт шиг харагдана | View дээр view давхарлах тусам гүйцэтгэлийг `EXPLAIN`-аар шалга |
| Эрхийг view-ээр хязгаарлаж болно | View дотор `ORDER BY` тавихгүй — уншихдаа эрэмбэл |

| Хэрэгцээ | MySQL |
|---|---|
| Дахин ажиллуулж болох | `CREATE OR REPLACE VIEW` |
| Тогтмол огноо | `DATE '2024-06-30' - INTERVAL 60 DAY` |
| Хоногийн зөрүү | `DATEDIFF(ихэс, бага)` |

> `DATEDIFF`-ийн аргументын дараалал `(төгсгөл, эхлэл)`, харин
> `TIMESTAMPDIFF`-ийнх `(нэгж, эхлэл, төгсгөл)` — эсрэг (Модул 4).
> Хамгийн түгээмэл алдааны нэг.
""",
            initial_code="""\
USE delguur;

-- ===== 1. Нөөцийн анхааруулга =====
CREATE OR REPLACE VIEW v_baraa_anhaaruulga AS
SELECT b.baraa_id,
       b.ner                      AS baraa,
       a.ner                      AS angilal,
       b.uldegdel,
       COALESCE(s.zarsan_too, 0)  AS zarsan_too,
       CASE WHEN b.uldegdel = 0 THEN 'Дууссан' ELSE 'Бага' END AS tuluv
FROM baraa AS b
JOIN angilal AS a ON a.angilal_id = b.angilal_id
-- Цуцлагдаагүй захиалгаар зарагдсан тоо; хэзээ ч зарагдаагүй бол NULL
LEFT JOIN (
    SELECT zm.baraa_id, SUM(zm.too) AS zarsan_too
    FROM zahialgiin_mur AS zm
    JOIN zahialga AS z ON z.zahialga_id = zm.zahialga_id
    WHERE z.tuluv <> 'Цуцлагдсан'
    GROUP BY zm.baraa_id
) AS s ON s.baraa_id = b.baraa_id
WHERE b.uldegdel < 10;

-- Дууссаныг эхэнд, дотроо их зарагддагийг нь эхэнд
SELECT baraa, angilal, uldegdel, zarsan_too, tuluv
FROM v_baraa_anhaaruulga
ORDER BY uldegdel, zarsan_too DESC;

-- ===== 2. Идэвхгүй хэрэглэгч (лавлах огноо 2024-06-30, 60 хоног) =====
CREATE OR REPLACE VIEW v_idevhgui_hereglegch AS
SELECT h.hereglegch_id,
       CONCAT(h.ovog, ' ', h.ner)                     AS hereglegch,
       h.email,
       h.hot,
       MAX(z.zahialsan_ognoo)                         AS suuliin_zahialga,
       DATEDIFF(DATE '2024-06-30', MAX(z.zahialsan_ognoo)) AS honog
FROM hereglegch AS h
-- Цуцлалтын нөхцөл ON дотор: захиалгагүй хэрэглэгч хасагдахгүй
LEFT JOIN zahialga AS z
       ON z.hereglegch_id = h.hereglegch_id
      AND z.tuluv <> 'Цуцлагдсан'
GROUP BY h.hereglegch_id, h.ovog, h.ner, h.email, h.hot
HAVING MAX(z.zahialsan_ognoo) IS NULL
    OR MAX(z.zahialsan_ognoo) < DATE '2024-06-30' - INTERVAL 60 DAY;

SELECT hereglegch, email, hot, suuliin_zahialga, honog
FROM v_idevhgui_hereglegch
ORDER BY honog DESC;

-- ===== 3. Ангиллын орлого =====
CREATE OR REPLACE VIEW v_angilal_orlogo AS
SELECT a.angilal_id,
       a.ner                                AS angilal,
       COALESCE(SUM(mo.dun), 0)             AS orlogo
FROM angilal AS a
LEFT JOIN baraa AS b ON b.angilal_id = a.angilal_id
LEFT JOIN (
    SELECT zm.baraa_id, zm.too * zm.negj_une AS dun
    FROM zahialgiin_mur AS zm
    JOIN zahialga AS z ON z.zahialga_id = zm.zahialga_id
    WHERE z.tuluv <> 'Цуцлагдсан'
) AS mo ON mo.baraa_id = b.baraa_id
GROUP BY a.angilal_id, a.ner;

SELECT angilal, orlogo
FROM v_angilal_orlogo
ORDER BY orlogo DESC;

-- ===== 4. Хяналтын самбар — бүх гол тоо нэг мөрөнд =====
-- Бусад view-ээс уншина, тиймээс хамгийн сүүлд үүсгэнэ
CREATE OR REPLACE VIEW v_hyanaltiin_samber AS
SELECT
    (SELECT SUM(orlogo) FROM v_angilal_orlogo)                   AS niit_orlogo,
    (SELECT COUNT(*) FROM zahialga WHERE tuluv = 'Хүлээгдэж буй') AS huleegdej_bui,
    (SELECT COUNT(*) FROM v_baraa_anhaaruulga)                   AS anhaaruulga_baraa,
    (SELECT COUNT(*) FROM v_idevhgui_hereglegch)                 AS idevhgui_hereglegch;

SELECT * FROM v_hyanaltiin_samber;

-- ===== 5. Үүссэн view-үүдийг шалгах =====
SELECT table_name AS view_ner
FROM information_schema.views
WHERE table_schema = 'delguur'
  AND table_name IN ('v_baraa_anhaaruulga', 'v_idevhgui_hereglegch',
                     'v_angilal_orlogo', 'v_hyanaltiin_samber');
""",
        ),
    ],
)

LIBRARY_SYSTEM = ModuleSpec(
    title="Модул 20 — Төсөл: Номын сангийн систем эхнээс нь",
    description="Шаардлагаас эхлээд загвар, өгөгдөл, логик, тайланг бүрэн бүтээнэ.",
    lessons=[
        LessonSpec(
            title="Шаардлага ба загвар",
            slug="nomiin-san-zagvar-mysql",
            description="Нэгжүүд, нормчлол, ER диаграм, хязгаарлалттай хүснэгтүүд.",
            duration=720,
            language=MY,
            content="""\
Сүүлийн төсөлд бэлэн сан байхгүй — **хоосон хуудаснаас** эхэлнэ. Энэ
хичээлд `nomiin_san` санг бүтээж, дараагийн хичээлд зээлийн логикийг
процедур, триггерээр, сүүлийнх нь тайлан ба индексийг нэмнэ.

> Энэ сайт дээр `nomiin_san` сан аль хэдийн бэлэн — ажиллуулалт бүр
> анхны төлөвөөс эхэлнэ. Доорх скриптийг ажиллуулбал санг дахин үүсгэнэ.

### Шаардлага

Сумын номын сангаас:

- Ном бүрийн нэр, ISBN, хэвлэлийн он, **хэдэн хувь** байгааг хадгална.
- Нэг ном **олон зохиогчтой**, нэг зохиогч олон номтой байж болно.
- Гишүүн бүртгэлтэй, гишүүн бүр **зэрэг зээлэх дээд хязгаартай** (анхдагч 3).
- Зээл бүр: авсан, буцаах ёстой, бодитоор буцаасан огноо. Түүх устахгүй.
- Нэг гишүүн **нэг номыг давхар** (буцаалгүйгээр дахин) зээлж болохгүй.

### Нэгжүүд ба холбоос

```text
zohiogch 1 ──< nom_zohiogch >── 1 nom 1 ──< zeel >── 1 gishuun
             (олон-олон холбоос)          (зээл бүр нэг ном, нэг гишүүн)
```

| Хүснэгт | Үүрэг | Түлхүүр |
|---|---|---|
| `zohiogch` | Зохиогч | `zohiogch_id` |
| `nom` | Ном (гарчиг) ба нийт хувь | `nom_id`, `isbn` UNIQUE |
| `nom_zohiogch` | N:M холбоос | `(nom_id, zohiogch_id)` |
| `gishuun` | Гишүүн, зээлийн хязгаар | `gishuun_id`, `email` UNIQUE |
| `zeel` | Зээлийн түүх | `zeel_id`, FK → `nom`, `gishuun` |

### Нормчлолын шийдвэрүүд

- **Зохиогчийг `nom` дотор багана болгохгүй.** «Ганбат, Уянга» гэж нэг нүдэнд
  бичвэл 1NF зөрчинө; `zohiogch1`, `zohiogch2` гэвэл давтагдах бүлэг болно.
  Тиймээс `nom_zohiogch` холбоос хүснэгт.
- **«Боломжит хувь»-ийг хадгалахгүй.** Энэ нь `niit_too` − буцаагаагүй зээлийн
  тоо гэж **тооцоологддог** өгөгдөл. Хадгалбал хоёр газар зөрөх эрсдэлтэй.
- **Зээлийг `nom`-ын багана болгохгүй** (`zeelsen_gishuun_id` гэх мэт) —
  түүх алдагдана, олон хувьтай номыг илэрхийлж чадахгүй.
- **Торгуулийг хадгалахгүй** — хоцорсон хоногоос тооцоолно.

### Хязгаарлалт — өгөгдлийн хамгаалалт

| Дүрэм | Хэрэгжүүлэлт |
|---|---|
| Он боломжийн мужид | `CHECK (hevlesen_on BETWEEN 1450 AND 2100)` |
| Хувь сөрөг биш | `CHECK (niit_too >= 0)` |
| Буцаах огноо авснаас хойш | `CHECK (duusah_ognoo >= avsan_ognoo)` |
| Давхар зээлгүй | Үүсгэсэн багана + `UNIQUE` (доор) |

### Давхар зээлийг MySQL-д хориглох

«Зөвхөн буцаагаагүй мөрүүдийн дунд давтагдахгүй» гэсэн дүрмийг `UNIQUE`
шууд илэрхийлж чадахгүй: түүх дотор ижил гишүүн-ном хос олон удаа байж
болно. Зарим DBMS-д үүнд шүүлттэй (filtered) index байдаг, MySQL-д
байхгүй. Оронд нь **үүсгэсэн багана** (generated column) ашиглана:

```sql
idevhtei_gishuun_id INT GENERATED ALWAYS AS
    (CASE WHEN butsaasan_ognoo IS NULL THEN gishuun_id END) STORED,
UNIQUE KEY ux_zeel_idevhtei (nom_id, idevhtei_gishuun_id)
```

`GENERATED ALWAYS AS (илэрхийлэл) STORED` нь баганын утгыг бусад баганаас
**автоматаар** тооцоолж хадгална — гараар бичих боломжгүй. Буцаагаагүй
зээлд утга нь `gishuun_id`, буцаасан зээлд `NULL`. `UNIQUE` индекс олон
`NULL`-ийг зөвшөөрдөг (Модул 8) тул түүх хэдэн ч мөр байж болох ч
**идэвхтэй** зээл нэг гишүүн-номд нэгээс илүү байж чадахгүй.

> `CHECK` дотор `CURDATE()` зэрэг тогтмол бус функц хэрэглэж болохгүй.
> «Он ирээдүйд биш» гэх дүрмийг триггер эсвэл програмаар шалгана.

### Жишээ өгөгдөл

Лавлах огноо **2024-06-30**. Зээлийн хугацаа 14 хоног. Энэ өдрийн байдлаар
3 зээл хугацаа хэтэрсэн, «Хонгор зул» ба «SQL дасгал ажил» (тус бүр 1 хувь)
зээлд гарсан, Дөлгөөн (хязгаар 1) хязгаартаа хүрсэн — дараагийн хичээлүүдийн
шалгалтад эдгээр нөхцөл хэрэгтэй.

> Скрипт `DROP DATABASE IF EXISTS`-ээр эхэлдэг тул хэдэн ч удаа ажиллуулж
> болно — сан анхны төлөвтөө буцна.
""",
            initial_code="""\
-- ===== 0. Санг шинээр үүсгэх =====
DROP DATABASE IF EXISTS nomiin_san;
CREATE DATABASE nomiin_san
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_0900_ai_ci;
USE nomiin_san;

-- ===== 1. Зохиогч =====
CREATE TABLE zohiogch (
    zohiogch_id  INT AUTO_INCREMENT PRIMARY KEY,
    ovog         VARCHAR(50)  NOT NULL,
    ner          VARCHAR(50)  NOT NULL,
    tursun_on    SMALLINT     NULL
);

-- ===== 2. Ном =====
CREATE TABLE nom (
    nom_id       INT AUTO_INCREMENT PRIMARY KEY,
    ner          VARCHAR(150) NOT NULL,
    isbn         VARCHAR(17)  NOT NULL,
    hevlesen_on  SMALLINT     NOT NULL,
    niit_too     INT          NOT NULL DEFAULT 1,
    CONSTRAINT uq_nom_isbn UNIQUE (isbn),
    CONSTRAINT ck_nom_on   CHECK (hevlesen_on BETWEEN 1450 AND 2100),
    CONSTRAINT ck_nom_too  CHECK (niit_too >= 0)
);

-- ===== 3. Ном-зохиогч (олон-олон) =====
CREATE TABLE nom_zohiogch (
    nom_id       INT NOT NULL,
    zohiogch_id  INT NOT NULL,
    PRIMARY KEY (nom_id, zohiogch_id),
    -- Ном устгавал холбоос нь хамт устна
    CONSTRAINT fk_nz_nom FOREIGN KEY (nom_id)
        REFERENCES nom (nom_id) ON DELETE CASCADE,
    -- Номтой зохиогчийг устгахыг хориглоно
    CONSTRAINT fk_nz_zohiogch FOREIGN KEY (zohiogch_id)
        REFERENCES zohiogch (zohiogch_id)
);

-- ===== 4. Гишүүн =====
CREATE TABLE gishuun (
    gishuun_id        INT AUTO_INCREMENT PRIMARY KEY,
    ovog              VARCHAR(50)  NOT NULL,
    ner               VARCHAR(50)  NOT NULL,
    email             VARCHAR(100) NOT NULL,
    utas              VARCHAR(20)  NULL,
    burtgesen_ognoo   DATE         NOT NULL DEFAULT (CURRENT_DATE),
    zeeliin_hyazgaar  TINYINT      NOT NULL DEFAULT 3,
    CONSTRAINT uq_gishuun_email     UNIQUE (email),
    CONSTRAINT ck_gishuun_email     CHECK (email LIKE '%_@_%'),
    CONSTRAINT ck_gishuun_hyazgaar  CHECK (zeeliin_hyazgaar BETWEEN 1 AND 10)
);

-- ===== 5. Зээл =====
CREATE TABLE zeel (
    zeel_id          INT AUTO_INCREMENT PRIMARY KEY,
    nom_id           INT  NOT NULL,
    gishuun_id       INT  NOT NULL,
    avsan_ognoo      DATE NOT NULL DEFAULT (CURRENT_DATE),
    duusah_ognoo     DATE NOT NULL,
    butsaasan_ognoo  DATE NULL,
    -- Буцаагаагүй бол gishuun_id, буцаасан бол NULL
    idevhtei_gishuun_id INT GENERATED ALWAYS AS
        (CASE WHEN butsaasan_ognoo IS NULL THEN gishuun_id END) STORED,
    CONSTRAINT fk_zeel_nom FOREIGN KEY (nom_id) REFERENCES nom (nom_id),
    CONSTRAINT fk_zeel_gishuun FOREIGN KEY (gishuun_id) REFERENCES gishuun (gishuun_id),
    CONSTRAINT ck_zeel_hugatsaa CHECK (duusah_ognoo >= avsan_ognoo),
    CONSTRAINT ck_zeel_butsaasan
        CHECK (butsaasan_ognoo IS NULL OR butsaasan_ognoo >= avsan_ognoo),
    -- Нэг гишүүн нэг номыг зэрэг хоёр удаа зээлэхгүй
    CONSTRAINT ux_zeel_idevhtei UNIQUE (nom_id, idevhtei_gishuun_id)
);

-- ===== 6. Жишээ өгөгдөл (шинэ сан тул ID 1-ээс дараална) =====
INSERT INTO zohiogch (ovog, ner, tursun_on) VALUES
    ('Дашдоржийн',  'Нацагдорж',  1906),   -- 1
    ('Чадраабалын', 'Лодойдамба', 1917),   -- 2
    ('Бямбын',      'Ринчен',     1905),   -- 3
    ('Сэнгийн',     'Эрдэнэ',     1929),   -- 4
    ('Батын',       'Ганбат',     1980),   -- 5
    ('Доржийн',     'Уянга',      1985);   -- 6

INSERT INTO nom (ner, isbn, hevlesen_on, niit_too) VALUES
    ('Тунгалаг Тамир',            '978-99978-01-001', 2015, 3),  -- 1
    ('Үүрийн туяа',               '978-99978-01-002', 2016, 2),  -- 2
    ('Миний нутаг',               '978-99978-01-003', 2018, 2),  -- 3
    ('Хонгор зул',                '978-99978-01-004', 2017, 1),  -- 4
    ('Өгөгдлийн сангийн үндэс',   '978-99978-01-005', 2022, 2),  -- 5
    ('SQL дасгал ажил',           '978-99978-01-006', 2023, 1),  -- 6
    ('Програмчлалын үндэс',       '978-99978-01-007', 2021, 2);  -- 7

INSERT INTO nom_zohiogch (nom_id, zohiogch_id) VALUES
    (1, 2), (2, 3), (3, 1), (4, 4),
    (5, 5), (5, 6),                 -- хоёр зохиогчтой ном
    (6, 6), (7, 5);

INSERT INTO gishuun (ovog, ner, email, utas, burtgesen_ognoo, zeeliin_hyazgaar) VALUES
    ('Батын',      'Болор',    'bolor@example.mn',    '99001122', '2023-09-01', 3),  -- 1
    ('Гантулгын',  'Мишээл',   'misheel@example.mn',  NULL,       '2023-10-15', 3),  -- 2
    ('Энхбаярын',  'Тэмүүлэн', 'temuulen@example.mn', '88112233', '2024-01-20', 2),  -- 3
    ('Сувдын',     'Оюу',      'oyu@example.mn',      '95123456', '2024-02-05', 5),  -- 4
    ('Нямын',      'Дөлгөөн',  'dulguun@example.mn',  NULL,       '2024-03-10', 1);  -- 5

INSERT INTO zeel (nom_id, gishuun_id, avsan_ognoo, duusah_ognoo, butsaasan_ognoo) VALUES
    (1, 1, '2024-04-01', '2024-04-15', '2024-04-12'),  -- 1 хугацаандаа
    (5, 1, '2024-04-20', '2024-05-04', '2024-05-10'),  -- 2 хоцорч буцаасан
    (2, 2, '2024-05-02', '2024-05-16', '2024-05-15'),  -- 3
    (1, 3, '2024-05-10', '2024-05-24', '2024-05-20'),  -- 4
    (5, 4, '2024-05-15', '2024-05-29', '2024-06-01'),  -- 5 хоцорч буцаасан
    (3, 4, '2024-06-01', '2024-06-15', NULL),          -- 6 хугацаа хэтэрсэн
    (1, 2, '2024-06-05', '2024-06-19', NULL),          -- 7 хугацаа хэтэрсэн
    (5, 3, '2024-06-10', '2024-06-24', NULL),          -- 8 хугацаа хэтэрсэн
    (6, 1, '2024-06-18', '2024-07-02', NULL),          -- 9
    (1, 4, '2024-06-20', '2024-07-04', NULL),          -- 10
    (4, 5, '2024-06-25', '2024-07-09', NULL),          -- 11
    (2, 4, '2024-06-22', '2024-07-06', NULL);          -- 12

-- ===== 7. Шалгалт =====
SELECT 'zohiogch' AS husnegt, COUNT(*) AS mur FROM zohiogch
UNION ALL SELECT 'nom', COUNT(*) FROM nom
UNION ALL SELECT 'nom_zohiogch', COUNT(*) FROM nom_zohiogch
UNION ALL SELECT 'gishuun', COUNT(*) FROM gishuun
UNION ALL SELECT 'zeel', COUNT(*) FROM zeel;

-- Номын боломжит хувь = нийт хувь - буцаагаагүй зээл
SELECT n.nom_id, n.ner, n.niit_too,
       COUNT(z.zeel_id)              AS zeeld_bui,
       n.niit_too - COUNT(z.zeel_id) AS bolomjit
FROM nom AS n
LEFT JOIN zeel AS z ON z.nom_id = n.nom_id AND z.butsaasan_ognoo IS NULL
GROUP BY n.nom_id, n.ner, n.niit_too
ORDER BY n.nom_id;

-- Давхар зээлийн хамгаалалтыг турших: Мишээл 1-р номыг буцаагаагүй байна.
-- Доорх мөрийн тайлбарыг авбал алдаа 1062 (Duplicate entry) гарна.
-- INSERT INTO zeel (nom_id, gishuun_id, avsan_ognoo, duusah_ognoo)
-- VALUES (1, 2, DATE '2024-06-30', DATE '2024-07-14');
""",
        ),
        LessonSpec(
            title="Зээлийн логик: процедур ба триггер",
            slug="nomiin-san-tsql-bizness-logik",
            description="Ном зээлүүлэх, буцаах процедур, хувийн тоог хамгаалах триггер, тайлангийн процедур.",
            duration=720,
            language=MY,
            content="""\
**Урьдчилсан нөхцөл:** өмнөх хичээлийн скриптээр `nomiin_san`-г үүсгэсэн
байх. Энэ сайт дээр сан аль хэдийн бэлэн бөгөөд ажиллуулалт бүр анхны
төлөвөөс эхэлнэ. Өөрийн компьютер дээр дараалал эвдэрсэн бол тэр
скриптийг дахин ажиллуулж өгөгдлийг анхны төлөвт нь оруул.

### Даалгавар

1. **`sp_nom_zeelduuleh`** — ном зээлүүлэх процедур. Дараахыг шалгана:
   - Ном ба гишүүн бүртгэлтэй эсэх
   - Номын **чөлөөт хувь** байгаа эсэх
   - Гишүүн **зээлийн хязгаартаа** хүрээгүй эсэх
   - Ижил номыг **давхар** зээлээгүй эсэх
   - Бүгд transaction дотор, алдаа гарвал `ROLLBACK` + `RESIGNAL`
2. **`sp_nom_butsaah`** — буцаах процедур, хоцорсон хоног ба торгуулийг (өдөрт
   500₮) буцаана.
3. **Триггер** — хэн нэгэн процедурыг тойрч шууд `INSERT` хийсэн ч номын
   хувиас илүү зээл үүсэхгүй.
4. **`sp_hotsorson_zeel`** — огноо параметртэй хугацаа хэтэрсэн зээлийн тайлан.

### Зөвлөгөө

- `DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK; RESIGNAL; END;` —
  ямар ч алдаа transaction-ийг бүхэлд нь буцааж, анхны алдааг дуудагч руу
  дамжуулна (Модул 17).
- Хоёр ажилтан сүүлийн нэг хувийг **зэрэг** зээлүүлэхээс сэргийлж номын
  мөрийг `SELECT … FOR UPDATE`-ээр түгжинэ (Модул 14). Хоёр дахь нь
  эхнийхийг дуусахыг хүлээгээд, шинэчлэгдсэн тоог уншина.
- `SIGNAL`-ийн `MESSAGE_TEXT`-д илэрхийлэл бичиж болохгүй — эхлээд
  `v_msg` хувьсагчид `CONCAT`-аар угсар.
- MySQL-ийн процедурын параметр **анхдагч утгагүй**. Огноог `NULL`-ээр
  дамжуулбал биеийн эхэнд `COALESCE(p_ognoo, CURDATE())` гэж өнөөдрөөр
  орлуулна.
- MySQL-ийн функц хүснэгт буцааж чаддаггүй (Модул 16) тул тайланг
  **процедур** болгоно.

### Хамгаалалтын давхарга

| Давхарга | Юуг барина | Алдаа |
|---|---|---|
| Процедур | Бүх бизнесийн дүрэм | Ойлгомжтой, дугаартай (5001–5005) |
| Триггер | Хувиас илүү зээл — ямар ч замаар орсон | 5010 |
| Үүсгэсэн багана + `UNIQUE` | Давхар зээл | Системийн 1062 |
| `CHECK` | Огнооны дараалал | Системийн 3819 |

Процедур хэрэглэгчид ээлтэй алдаа өгдөг, харин триггер ба хязгаарлалт нь
«эцсийн хаалга» — програмд алдаа байсан ч өгөгдөл эвдрэхгүй.

### Шийдлийн тайлбар

**Зээлүүлэх:** transaction эхлүүлээд номын `niit_too`-г `FOR UPDATE`-ээр
түгжиж уншина. Олдохгүй бол 5001. Гишүүний хязгаарыг уншина (5002).
Идэвхтэй зээлийн тоо ≥ хувь бол 5003, гишүүний идэвхтэй зээл ≥ хязгаар
бол 5004, ижил ном буцаагаагүй бол 5005. Бүгд давбал `INSERT`,
`LAST_INSERT_ID()`-ээр шинэ дугаарыг `OUT` параметрт аваад `COMMIT`.

**Триггер** `BEFORE INSERT … FOR EACH ROW`: шинэ мөр (`NEW`) буцаагаагүй
зээл бол тухайн номын идэвхтэй зээлийг тоолж, `niit_too`-д хүрсэн бол
`SIGNAL`. MySQL-ийн триггер мөр бүрт ажилладаг тул олон мөрийн `INSERT`-д
ч мөр бүрийг шалгана.

**Турших:** энгийн скриптэд алдаа барих арга байхгүй — эхний алдаа
скриптийг зогсооно. Тиймээс туршилтын туслах процедур
`tur_zeel_turshih` алдааг `EXIT HANDLER`-ээр барьж, кодыг нь
`GET DIAGNOSTICS`-ээр аваад мөр болгон харуулна.

### Турших сценари (лавлах огноо 2024-06-30)

| Дуудлага | Үр дүн |
|---|---|
| Ном 7 → Болор | Амжилттай (шалгаад мөрийг устгана) |
| Ном 4 «Хонгор зул» → Болор | 5003: чөлөөт хувь алга |
| Ном 7 → Дөлгөөн | 5004: хязгаар 1, аль хэдийн 1 зээлтэй |
| Ном 1 → Мишээл | 5005: буцаагаагүй байна |
| Шууд `INSERT` ном 6 | Триггер 5010 |
| Зээл 6-г буцаах | 15 хоног хоцорсон, 7 500₮ |

Хугацаа хэтэрсэн тайлан: Оюу — «Миний нутаг» 15 хоног, Мишээл — «Тунгалаг
Тамир» 11 хоног, Тэмүүлэн — «Өгөгдлийн сангийн үндэс» 6 хоног.

> Процедур өөрөө `COMMIT` хийдэг тул гаднаас `START TRANSACTION … ROLLBACK`
> хийж буцааж чадахгүй — MySQL-д үүрлэсэн transaction байхгүй (Модул 14).
> Тиймээс амжилттай туршилтын дараа мөрийг гараар устгаж, буцаасан зээлийг
> дахин нээнэ. `AUTO_INCREMENT` буцдаггүй тул дараагийн шинэ зээл 13 биш 14
> дугаар авна — энэ хэвийн.
""",
            initial_code="""\
-- Урьдчилсан нөхцөл: өмнөх хичээлийн nomiin_san скрипт ажилласан байх
USE nomiin_san;

DROP PROCEDURE IF EXISTS sp_nom_zeelduuleh;
DROP PROCEDURE IF EXISTS sp_nom_butsaah;
DROP PROCEDURE IF EXISTS sp_hotsorson_zeel;
DROP PROCEDURE IF EXISTS tur_zeel_turshih;
DROP TRIGGER IF EXISTS trg_zeel_huvi_shalgah;

DELIMITER $$

-- ===== 1. Ном зээлүүлэх процедур =====
CREATE PROCEDURE sp_nom_zeelduuleh(
    IN  p_nom_id     INT,
    IN  p_gishuun_id INT,
    IN  p_ognoo      DATE,   -- NULL бол өнөөдөр
    IN  p_honog      INT,
    OUT p_zeel_id    INT
)
BEGIN
    DECLARE v_ognoo DATE DEFAULT COALESCE(p_ognoo, CURDATE());
    DECLARE v_niit_too INT;
    DECLARE v_hyazgaar INT;
    DECLARE v_zeeld_bui INT;
    DECLARE v_gishuun_zeel INT;
    DECLARE v_msg VARCHAR(255);

    -- Ямар ч алдаа: буцаагаад анхны алдааг дуудагч руу дамжуулна
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    -- Номын мөрийг түгжинэ: зэрэг зээлүүлэлт дараалалд орно
    SELECT niit_too INTO v_niit_too
    FROM nom
    WHERE nom_id = p_nom_id
    FOR UPDATE;

    IF v_niit_too IS NULL THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Ийм ном бүртгэлгүй байна.', MYSQL_ERRNO = 5001;
    END IF;

    SELECT zeeliin_hyazgaar INTO v_hyazgaar
    FROM gishuun
    WHERE gishuun_id = p_gishuun_id
    FOR UPDATE;

    IF v_hyazgaar IS NULL THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Ийм гишүүн бүртгэлгүй байна.', MYSQL_ERRNO = 5002;
    END IF;

    -- Чөлөөт хувь
    SELECT COUNT(*) INTO v_zeeld_bui
    FROM zeel
    WHERE nom_id = p_nom_id AND butsaasan_ognoo IS NULL;

    IF v_zeeld_bui >= v_niit_too THEN
        SET v_msg = CONCAT('Чөлөөт хувь алга: ', v_niit_too, ' хувиас ',
                           v_zeeld_bui, ' нь зээлд байна.');
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = v_msg, MYSQL_ERRNO = 5003;
    END IF;

    -- Гишүүний хязгаар
    SELECT COUNT(*) INTO v_gishuun_zeel
    FROM zeel
    WHERE gishuun_id = p_gishuun_id AND butsaasan_ognoo IS NULL;

    IF v_gishuun_zeel >= v_hyazgaar THEN
        SET v_msg = CONCAT('Зээлийн хязгаар хүрсэн: ', v_gishuun_zeel, '/', v_hyazgaar);
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = v_msg, MYSQL_ERRNO = 5004;
    END IF;

    -- Давхар зээл
    IF EXISTS (SELECT 1 FROM zeel
               WHERE nom_id = p_nom_id AND gishuun_id = p_gishuun_id
                 AND butsaasan_ognoo IS NULL) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Гишүүн энэ номыг буцаагаагүй байна.', MYSQL_ERRNO = 5005;
    END IF;

    INSERT INTO zeel (nom_id, gishuun_id, avsan_ognoo, duusah_ognoo)
    VALUES (p_nom_id, p_gishuun_id, v_ognoo, v_ognoo + INTERVAL p_honog DAY);

    SET p_zeel_id = LAST_INSERT_ID();

    COMMIT;
END$$

-- ===== 2. Ном буцаах процедур =====
CREATE PROCEDURE sp_nom_butsaah(
    IN p_zeel_id INT,
    IN p_ognoo   DATE    -- NULL бол өнөөдөр
)
BEGIN
    DECLARE v_ognoo DATE DEFAULT COALESCE(p_ognoo, CURDATE());
    DECLARE v_avsan DATE;
    DECLARE v_duusah DATE;
    DECLARE v_butsaasan DATE;
    DECLARE v_hotsorson INT;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    SELECT avsan_ognoo, duusah_ognoo, butsaasan_ognoo
    INTO v_avsan, v_duusah, v_butsaasan
    FROM zeel
    WHERE zeel_id = p_zeel_id
    FOR UPDATE;

    IF v_avsan IS NULL THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Ийм зээл олдсонгүй.', MYSQL_ERRNO = 5011;
    END IF;

    IF v_butsaasan IS NOT NULL THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Энэ ном аль хэдийн буцаагдсан.', MYSQL_ERRNO = 5012;
    END IF;

    UPDATE zeel
    SET butsaasan_ognoo = v_ognoo
    WHERE zeel_id = p_zeel_id;

    COMMIT;

    -- GREATEST(a, b) нь ихийг нь өгнө: хугацаандаа буцаасан бол 0
    SET v_hotsorson = GREATEST(DATEDIFF(v_ognoo, v_duusah), 0);

    SELECT p_zeel_id AS zeel_id, v_ognoo AS butsaasan_ognoo,
           v_hotsorson AS hotsorson_honog, v_hotsorson * 500 AS torguuli;
END$$

-- ===== 3. Триггер: номын хувиас илүү идэвхтэй зээл үүсгэхгүй =====
CREATE TRIGGER trg_zeel_huvi_shalgah
BEFORE INSERT ON zeel
FOR EACH ROW
BEGIN
    DECLARE v_niit_too INT;
    DECLARE v_zeeld_bui INT;

    IF NEW.butsaasan_ognoo IS NULL THEN
        SELECT niit_too INTO v_niit_too FROM nom WHERE nom_id = NEW.nom_id;

        SELECT COUNT(*) INTO v_zeeld_bui
        FROM zeel
        WHERE nom_id = NEW.nom_id AND butsaasan_ognoo IS NULL;

        IF v_zeeld_bui >= v_niit_too THEN
            SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Номын хувиас илүү идэвхтэй зээл үүсэх гэж байна.',
                    MYSQL_ERRNO = 5010;
        END IF;
    END IF;
END$$

-- ===== 4. Хугацаа хэтэрсэн зээл — огноо параметртэй тайлан =====
CREATE PROCEDURE sp_hotsorson_zeel(IN p_ognoo DATE)
BEGIN
    SELECT z.zeel_id,
           n.ner                                     AS nom,
           CONCAT(g.ovog, ' ', g.ner)                AS gishuun,
           g.utas,
           z.duusah_ognoo,
           DATEDIFF(p_ognoo, z.duusah_ognoo)         AS hotsorson_honog,
           DATEDIFF(p_ognoo, z.duusah_ognoo) * 500   AS torguuli
    FROM zeel AS z
    JOIN nom AS n     ON n.nom_id = z.nom_id
    JOIN gishuun AS g ON g.gishuun_id = z.gishuun_id
    WHERE z.butsaasan_ognoo IS NULL
      AND z.duusah_ognoo < p_ognoo
    ORDER BY hotsorson_honog DESC;
END$$

-- ===== 5. Туршилтын туслах: алдааг барьж мөр болгон харуулна =====
-- p_shuud = TRUE бол процедурыг тойрч шууд INSERT хийнэ (триггерийг турших)
CREATE PROCEDURE tur_zeel_turshih(IN p_nom_id INT, IN p_gishuun_id INT, IN p_shuud BOOLEAN)
BEGIN
    DECLARE v_kod INT;
    DECLARE v_msg VARCHAR(255);

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        GET DIAGNOSTICS CONDITION 1 v_kod = MYSQL_ERRNO, v_msg = MESSAGE_TEXT;
        SELECT p_nom_id AS nom_id, p_gishuun_id AS gishuun_id,
               v_kod AS aldaa_kod, v_msg AS aldaa;
    END;

    IF p_shuud THEN
        INSERT INTO zeel (nom_id, gishuun_id, avsan_ognoo, duusah_ognoo)
        VALUES (p_nom_id, p_gishuun_id, '2024-06-30', '2024-07-14');
    ELSE
        CALL sp_nom_zeelduuleh(p_nom_id, p_gishuun_id, '2024-06-30', 14, @zeel_id);
    END IF;

    SELECT p_nom_id AS nom_id, p_gishuun_id AS gishuun_id,
           'Амжилттай' AS ur_dun, LAST_INSERT_ID() AS shine_zeel_id;
END$$

DELIMITER ;

-- ===== 6. Турших =====
-- 6.1 Амжилттай зээл: шалгаад мөрийг устгана
CALL sp_nom_zeelduuleh(7, 1, '2024-06-30', 14, @zeel_id);
SELECT zeel_id, nom_id, gishuun_id, avsan_ognoo, duusah_ognoo
FROM zeel WHERE zeel_id = @zeel_id;
DELETE FROM zeel WHERE zeel_id = @zeel_id;

-- 6.2 Чөлөөт хувь алга (5003)
CALL tur_zeel_turshih(4, 1, FALSE);

-- 6.3 Гишүүний хязгаар (5004)
CALL tur_zeel_turshih(7, 5, FALSE);

-- 6.4 Давхар зээл (5005)
CALL tur_zeel_turshih(1, 2, FALSE);

-- 6.5 Процедурыг тойрсон шууд INSERT: триггер барина (5010)
CALL tur_zeel_turshih(6, 2, TRUE);

-- 6.6 Хоцорсон номыг буцаах: 15 хоног, 7500 төгрөг. Дараа нь дахин нээнэ.
CALL sp_nom_butsaah(6, '2024-06-30');
UPDATE zeel SET butsaasan_ognoo = NULL WHERE zeel_id = 6;

-- 6.7 Хугацаа хэтэрсэн зээлийн тайлан
CALL sp_hotsorson_zeel('2024-06-30');

-- Өгөгдөл хэвээрээ: 12 зээл, 7 нь буцаагаагүй
SELECT COUNT(*) AS niit_zeel,
       SUM(CASE WHEN butsaasan_ognoo IS NULL THEN 1 ELSE 0 END) AS butsaagaagui
FROM zeel;
""",
        ),
        LessonSpec(
            title="Тайлан ба индекс",
            slug="nomiin-san-mysql-tailan-indeks",
            description="Хугацаа хэтэрсэн зээл, эрэлттэй ном, гишүүний түүх, EXPLAIN.",
            duration=720,
            language=MY,
            content="""\
**Урьдчилсан нөхцөл:** энэ модулийн эхний хичээлийн скриптийг ажиллуулсан
байх (энэ сайт дээр `nomiin_san` бэлэн). Энэ хичээл өгөгдлийг өөрчлөхгүй,
зөвхөн уншиж, индекс нэмнэ.

### Даалгавар

Номын санч дараах тайланг долоо хоног бүр авахыг хүсэв (лавлах огноо
**2024-06-30**):

1. **Хугацаа хэтэрсэн зээл** — гишүүн, утас, хэдэн хоног, торгууль (500₮/хоног)
2. **Эрэлттэй ном** — зээлийн тоогоор байр, хэзээ ч зээлэгдээгүй ном ч гарна
3. **Эрэлттэй зохиогч** — тэнцсэн бол ижил байр
4. **Гишүүний түүх** — нэг гишүүний бүх зээл төлөвтэй нь, мөн гишүүн бүрийн
   товч нэгтгэл
5. Эдгээр асуулгад тохирох **индекс** сонгож `EXPLAIN`-аар шалгах

### Зөвлөгөө

- Лавлах огноог `SET @lavlah_ognoo = '2024-06-30';` гэж нэг удаа тодорхойл.
- «Хэзээ ч зээлэгдээгүй ном ч гарна» = `nom`-оос `LEFT JOIN zeel`, `COUNT(z.zeel_id)`.
  `COUNT(*)` бичвэл зээлгүй ном 0 биш 1 гэж тоологдоно.
- Байр: `RANK() OVER (ORDER BY COUNT(z.zeel_id) DESC)` — нэгтгэл дээр шууд.
- Зээлийн төлөвийг `CASE`-ээр: хугацаа хэтэрсэн / зээлд байгаа / хоцорч
  буцаасан / хугацаандаа буцаасан. **Нөхцөлийн дараалал чухал.**

### Хүлээгдэж буй үр дүн

Хугацаа хэтэрсэн: Сувдын Оюу 15 хоног (7 500₮), Гантулгын Мишээл 11 (5 500₮),
Энхбаярын Тэмүүлэн 6 (3 000₮).

| nom | zeel_too | bair |
|---|---|---|
| Тунгалаг Тамир | 4 | 1 |
| Өгөгдлийн сангийн үндэс | 3 | 2 |
| Үүрийн туяа | 2 | 3 |
| Миний нутаг, Хонгор зул, SQL дасгал ажил | 1 | 4 |
| Програмчлалын үндэс | 0 | 7 |

Зохиогч: Лодойдамба ба Уянга 4 зээлээр **хамт 1-р байр**, Ганбат 3 (3-р байр —
`RANK` 2-ыг алгасна), Ринчен 2, Нацагдорж ба Эрдэнэ 1.

Гишүүн Оюугийн (id 4) түүх: «Өгөгдлийн сангийн үндэс» хоцорч буцаасан (3 хоног),
«Миний нутаг» хугацаа хэтэрсэн, «Тунгалаг Тамир» ба «Үүрийн туяа» зээлд байгаа.

### Индекс сонголт

Асуулга бүрийн `WHERE`, `JOIN`, `ORDER BY`-г хараад шийднэ:

| Асуулга | Шүүлт | Индекс |
|---|---|---|
| Хугацаа хэтэрсэн | `butsaasan_ognoo IS NULL AND duusah_ognoo < ?` | `(butsaasan_ognoo, duusah_ognoo)` |
| Гишүүний түүх | `gishuun_id = ? ORDER BY avsan_ognoo` | `(gishuun_id, avsan_ognoo)` |
| Эрэлттэй ном | `JOIN ON nom_id` | `ux_zeel_idevhtei`-ийн эхний багана `nom_id` — хангалттай |

- Нийлмэл индексийн **тэнцүү нөхцөлтэй баганыг эхэнд**, мужийн (`<`) баганыг
  дараа нь тавина.
- MySQL гадаад түлхүүрийн баганад индекс автоматаар үүсгэдэг. `(gishuun_id,
  avsan_ognoo)` үүсгэхэд `fk_zeel_gishuun`-ийн автомат индексийг MySQL өөрөө
  устгаж болно — шинэ индекс түүний үүргийг гүйцэтгэнэ.

### Дахин ажиллуулж болох индекс

MySQL-д `CREATE INDEX IF NOT EXISTS` **байхгүй**, `DROP INDEX IF EXISTS`
ч байхгүй (MariaDB-д бий). Тиймээс `information_schema.statistics`-оос
шалгаад, бэлтгэсэн тушаал (`PREPARE`, Модул 18) ажиллуулна:

- `SELECT IF(COUNT(*) = 0, 'CREATE INDEX …', 'SELECT …')` нь индекс
  байхгүй бол үүсгэх, байвал мэдээлэл хэвлэх **SQL текстийг** сонгоно.
- `PREPARE tushaal FROM @sql; EXECUTE tushaal;` тэр текстийг ажиллуулна.

### EXPLAIN-ийг уншихад

- `type`: `ALL` = бүтэн хүснэгт уншсан, `ref`/`range` = индекс ашигласан.
- `key`: сонгосон индексийн нэр. `rows`: уншина гэж тооцоолсон мөр.
- `EXPLAIN ANALYZE` (8.0.18+) асуулгыг **бодитоор ажиллуулж** хугацааг хэмжинэ.

> 12 мөртэй хүснэгтэд оновчлогч индексийг үл тоож `ALL` сонгож магадгүй —
> бүгдийг уншсан нь хурдан. Энэ алдаа биш. Индексийн ач холбогдол мянга,
> сая мөрөнд л харагдана.
""",
            initial_code="""\
-- Урьдчилсан нөхцөл: энэ модулийн эхний хичээлийн MySQL скрипт ажилласан байх
USE nomiin_san;

SET @lavlah_ognoo = '2024-06-30';

-- ===== 1. Хугацаа хэтэрсэн зээл =====
SELECT z.zeel_id,
       CONCAT(g.ovog, ' ', g.ner)                    AS gishuun,
       g.utas,
       n.ner                                         AS nom,
       z.duusah_ognoo,
       DATEDIFF(@lavlah_ognoo, z.duusah_ognoo)       AS hotsorson_honog,
       DATEDIFF(@lavlah_ognoo, z.duusah_ognoo) * 500 AS torguuli
FROM zeel AS z
JOIN gishuun AS g ON g.gishuun_id = z.gishuun_id
JOIN nom AS n     ON n.nom_id = z.nom_id
WHERE z.butsaasan_ognoo IS NULL
  AND z.duusah_ognoo < @lavlah_ognoo
ORDER BY hotsorson_honog DESC;

-- ===== 2. Эрэлттэй ном (зээлээгүй ном ч гарна) =====
SELECT n.ner                                        AS nom,
       COUNT(z.zeel_id)                             AS zeel_too,
       RANK() OVER (ORDER BY COUNT(z.zeel_id) DESC) AS bair
FROM nom AS n
LEFT JOIN zeel AS z ON z.nom_id = n.nom_id
GROUP BY n.nom_id, n.ner
ORDER BY bair, nom;

-- ===== 3. Эрэлттэй зохиогч (тэнцвэл ижил байр) =====
SELECT CONCAT(zo.ovog, ' ', zo.ner)                 AS zohiogch,
       GROUP_CONCAT(DISTINCT n.ner ORDER BY n.ner SEPARATOR ', ') AS nomuud,
       COUNT(z.zeel_id)                             AS zeel_too,
       RANK() OVER (ORDER BY COUNT(z.zeel_id) DESC) AS bair
FROM zohiogch AS zo
JOIN nom_zohiogch AS nz ON nz.zohiogch_id = zo.zohiogch_id
JOIN nom AS n           ON n.nom_id = nz.nom_id
LEFT JOIN zeel AS z     ON z.nom_id = nz.nom_id
GROUP BY zo.zohiogch_id, zo.ovog, zo.ner
ORDER BY bair, zohiogch;

-- ===== 4. Нэг гишүүний түүх =====
SET @gishuun_id = 4;

SELECT n.ner AS nom,
       z.avsan_ognoo,
       z.duusah_ognoo,
       z.butsaasan_ognoo,
       -- Дараалал чухал: эхлээд буцаагаагүйг, дараа нь буцаасныг ангилна
       CASE
           WHEN z.butsaasan_ognoo IS NULL AND z.duusah_ognoo < @lavlah_ognoo
               THEN 'Хугацаа хэтэрсэн'
           WHEN z.butsaasan_ognoo IS NULL
               THEN 'Зээлд байгаа'
           WHEN z.butsaasan_ognoo > z.duusah_ognoo
               THEN 'Хоцорч буцаасан'
           ELSE 'Хугацаандаа буцаасан'
       END AS tuluv,
       GREATEST(DATEDIFF(COALESCE(z.butsaasan_ognoo, @lavlah_ognoo), z.duusah_ognoo), 0)
           AS hotsorson_honog
FROM zeel AS z
JOIN nom AS n ON n.nom_id = z.nom_id
WHERE z.gishuun_id = @gishuun_id
ORDER BY z.avsan_ognoo;

-- ===== 5. Гишүүн бүрийн товч нэгтгэл =====
SELECT CONCAT(g.ovog, ' ', g.ner) AS gishuun,
       g.zeeliin_hyazgaar,
       COUNT(z.zeel_id)           AS niit_zeel,
       SUM(CASE WHEN z.zeel_id IS NOT NULL AND z.butsaasan_ognoo IS NULL
                THEN 1 ELSE 0 END) AS idevhtei,
       SUM(CASE WHEN z.butsaasan_ognoo IS NULL AND z.duusah_ognoo < @lavlah_ognoo
                THEN 1 ELSE 0 END) AS hetersen
FROM gishuun AS g
LEFT JOIN zeel AS z ON z.gishuun_id = g.gishuun_id
GROUP BY g.gishuun_id, g.ovog, g.ner, g.zeeliin_hyazgaar
ORDER BY hetersen DESC, idevhtei DESC;

-- ===== 6. Индекс — байхгүй бол л үүсгэнэ =====
-- 6.1 Хугацаа хэтэрсэн зээлд: тэнцүү нөхцөл эхэнд, муж дараа нь
SET @sql = (
    SELECT IF(COUNT(*) = 0,
              'CREATE INDEX ix_zeel_butsaasan_duusah ON zeel (butsaasan_ognoo, duusah_ognoo)',
              'SELECT ''ix_zeel_butsaasan_duusah аль хэдийн байна'' AS medeelel')
    FROM information_schema.statistics
    WHERE table_schema = DATABASE()
      AND table_name = 'zeel'
      AND index_name = 'ix_zeel_butsaasan_duusah'
);
PREPARE tushaal FROM @sql;
EXECUTE tushaal;
DEALLOCATE PREPARE tushaal;

-- 6.2 Гишүүний түүхэд
SET @sql = (
    SELECT IF(COUNT(*) = 0,
              'CREATE INDEX ix_zeel_gishuun_avsan ON zeel (gishuun_id, avsan_ognoo)',
              'SELECT ''ix_zeel_gishuun_avsan аль хэдийн байна'' AS medeelel')
    FROM information_schema.statistics
    WHERE table_schema = DATABASE()
      AND table_name = 'zeel'
      AND index_name = 'ix_zeel_gishuun_avsan'
);
PREPARE tushaal FROM @sql;
EXECUTE tushaal;
DEALLOCATE PREPARE tushaal;

-- Хүснэгтийн индексүүд
SHOW INDEX FROM zeel;

-- ===== 7. Төлөвлөгөөг шалгах =====
-- Уламжлалт хүснэгт хэлбэр: type, key, rows баганыг хар
EXPLAIN
SELECT z.zeel_id, z.duusah_ognoo
FROM zeel AS z
WHERE z.butsaasan_ognoo IS NULL
  AND z.duusah_ognoo < '2024-06-30';

-- Мод хэлбэр (8.0.16+)
EXPLAIN FORMAT=TREE
SELECT z.avsan_ognoo, z.nom_id
FROM zeel AS z
WHERE z.gishuun_id = 4
ORDER BY z.avsan_ognoo;

-- Бодитоор ажиллуулж хэмжинэ (8.0.18+)
EXPLAIN ANALYZE
SELECT n.ner, COUNT(z.zeel_id) AS zeel_too
FROM nom AS n
LEFT JOIN zeel AS z ON z.nom_id = n.nom_id
GROUP BY n.nom_id, n.ner;
""",
        ),
    ],
)

SQL_PROJECT_MODULES = [SHOP_REPORT, LIBRARY_SYSTEM]
