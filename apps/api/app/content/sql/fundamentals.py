"""Модул 0-1 — Өгөгдлийн сангийн үндэс ба жишээ сан.

Эхний хоёр модул нь SQL бичихээс өмнөх суурийг тавина: өгөгдлийн сан гэж юу
вэ, SQL ба MySQL гэж юу вэ. Модул 1-ийн `delguur` үүсгэх скриптийг бусад бүх
хичээл ашиглана. Код бүр сайт дээр ажилладаг тул MySQL суулгах хичээл
байхгүй (эзэмшигчийн шийдвэр, 2026-09-29).
"""

from app.content.types import LessonSpec, ModuleSpec
from app.models.enums import LessonLanguage

MY = LessonLanguage.MYSQL

DB_FUNDAMENTALS = ModuleSpec(
    title="Модул 0 — Өгөгдлийн сангийн үндэс",
    description="Өгөгдлийн сан, хамааралтай загвар, SQL ба MySQL-тэй танилцана.",
    lessons=[
        LessonSpec(
            title="Өгөгдлийн сан гэж юу вэ",
            slug="ugugdliin-san-gej-yu-ve",
            description="Өгөгдлийн сан, DBMS гэж юу вэ, хүснэгт файлаас юугаараа давуу вэ.",
            duration=420,
            language=MY,
            content="""\
**Өгөгдлийн сан** (database) гэдэг нь зохион байгуулалттай хадгалагдсан,
хайж, шинэчилж, хамгаалахад зориулсан өгөгдлийн цуглуулга юм.

Онлайн дэлгүүрийг бодоод үзье: бараа, хэрэглэгч, захиалга, үнэ, үлдэгдэл.
Энэ бүгдийг хаа нэгтээ найдвартай хадгалах ёстой. Тэр газар нь өгөгдлийн сан.

### Excel файл яагаад хүрэлцэхгүй вэ

Жижиг жагсаалтад Excel хангалттай. Гэхдээ өгөгдөл өсөж, олон хүн зэрэг
ажиллах үед асуудал гарна:

| Асуудал | Хүснэгт файл (Excel, CSV) | Өгөгдлийн сан |
|---|---|---|
| Олон хүн зэрэг засах | Бие биеийнхээ өөрчлөлтийг дарж бичнэ | Гүйлгээ, түгжээгээр зохицуулна |
| Хэмжээ | Excel нэг хуудсанд 1 048 576 мөр | Тэрбум мөр ч боломжтой |
| Буруу өгөгдөл | Үнийн нүдэнд «мэдэхгүй» гэж бичиж болно | Төрөл, хязгаарлалт шалгана |
| Давхардал | Хэрэглэгчийн хаягийг олон газар хуулна | Нэг газар хадгалж, холбоно |
| Хайлт | Гараар шүүнэ | SQL асуулга, индекс |
| Эрх | Файлыг нээсэн хүн бүгдийг харна | Хэрэглэгч бүрт тусдаа эрх |
| Сэргээх | Файл эвдэрвэл өгөгдөл алга | Нөөц хуулбар, гүйлгээний лог |

### DBMS — өгөгдлийн сангийн удирдлагын систем

Өгөгдлийн сан өөрөө диск дээрх файлууд. Тэдгээрийг удирддаг програмыг
**DBMS** (Database Management System) гэнэ. Бид DBMS-тэй SQL хэлээр ярина.

```text
Апп / вэб сайт  --- SQL асуулга --->  DBMS сервер  --->  диск дээрх файлууд
                <--- үр дүн ---------
```

Та файлыг шууд нээхгүй. «Улаанбаатарын хэрэглэгчдийг өг» гэж асуухад DBMS
өөрөө файлаас хайж, үр дүнг буцаана.

| DBMS | Эзэмшигч | Онцлог |
|---|---|---|
| **MySQL** | Oracle | Нээлттэй эх, вэбд хамгийн түгээмэл |
| **SQL Server** | Microsoft | Корпораци, .NET орчинд түгээмэл |
| PostgreSQL | Нээлттэй эх нийгэмлэг | Стандартад ойр, өргөтгөл ихтэй |
| Oracle Database | Oracle | Том банк, байгууллага |
| SQLite | Нээлттэй эх | Сервергүй, гар утасны апп дотор |

Энэ сургалт **MySQL**-ийг заана. Хамааралтай DBMS-ийн SQL хоорондоо маш
төстэй тул нэгийг нь сайн сурвал бусад руу амархан шилжинэ.

### Хамааралтай ба NoSQL

- **Хамааралтай** (relational) сан нь өгөгдлийг хүснэгтэд хадгалж, SQL
  ашиглана. MySQL, SQL Server, PostgreSQL бүгд ийм.
- **NoSQL** сан нь баримт (MongoDB), түлхүүр-утга (Redis) зэрэг өөр
  бүтэцтэй. Тусгай хэрэгцээнд ашиглагдана.

Санхүү, захиалга, бүртгэл зэрэг нарийн холбоотой өгөгдөлд хамааралтай сан
давамгайлсан хэвээр байна.

### Хаана хэрэглэгддэг вэ

- **Банк** — данс, гүйлгээ, зээл
- **Цахим худалдаа** — бараа, сагс, захиалга
- **Эмнэлэг, сургууль** — өвчтөн, сурагч, дүнгийн бүртгэл
- **Гар утасны апп** — хэрэглэгчийн профайл, мессеж
- **Энэ платформ** — хичээл, таны ахиц өгөгдлийн санд хадгалагдаж байна

### SQL нь «юу» гэж асуудаг

SQL-д **хэрхэн** хайхыг биш **юу** хэрэгтэйг бичнэ:

```sql
SELECT ner, hot
FROM hereglegch
WHERE hot = 'Дархан';
```

Файлыг яаж унших, аль индекс ашиглахыг DBMS өөрөө шийднэ.

Энэ жишээ нь зөвхөн SQL ямар харагддагийг үзүүлж байна: `SELECT`-ийг
Модул 2-т, `WHERE`-ийг Модул 3-т нарийн үзнэ.

> Энэ хичээлийн код ямар ч хүснэгт шаардахгүй. **«Код ажиллуулах»**
> товчоор энэ сайт дээр шууд ажиллуулна — юу ч суулгах шаардлагагүй.
> Үр дүнг нь хараарай — мөр бүрийг одоо ойлгох шаардлагагүй.
""",
            initial_code="""\
-- Энэ хичээлийн код ямар ч хүснэгт шаардахгүй.
-- «Код ажиллуулах» товчоор энд шууд ажиллуулна.
-- Танилцуулга: ажиллуулж үр дүнг хар. SELECT, AS-ийг Модул 2-т үзнэ.

-- Кирилл үсэг зөв дамжихын тулд холболтыг utf8mb4 болгоно
SET NAMES utf8mb4;

-- 1. Сервер хариу өгч байгааг шалгах
SELECT 'Сайн байна уу, өгөгдлийн сан!' AS mendchilgee;

-- 2. DBMS тооцоолол хийж чадна
SELECT 2 + 3 AS niilber, 10 * 4 AS urjver;

-- 3. Үр дүн үргэлж мөр, баганатай хүснэгт хэлбэртэй
--    (UNION ALL нь хэд хэдэн SELECT-ийн мөрийг нэг үр дүнд залгана —
--    Модул 11-д үзнэ)
SELECT 1 AS id, 'Болд' AS ner, 'Улаанбаатар' AS hot
UNION ALL
SELECT 2, 'Сараа', 'Улаанбаатар'
UNION ALL
SELECT 3, 'Тэмүүлэн', 'Дархан';

-- 4. Серверийн өнөөдрийн огноо ба цаг
SELECT CURRENT_DATE AS unuudur, CURRENT_TIME AS tsag;
""",
        ),
        LessonSpec(
            title="Хамааралтай загвар",
            slug="hamaaraltai-zagvar",
            description="Хүснэгт, мөр, багана, анхдагч ба гадаад түлхүүр, холбоосууд.",
            duration=600,
            language=MY,
            content="""\
**Хамааралтай загварыг** (relational model) 1970 онд IBM-ийн Эдгар Кодд
санал болгосон. Санаа нь энгийн: бүх өгөгдөл **хүснэгтэд** хадгалагдана.

### Хүснэгт, мөр, багана

| Нэр томьёо | Өөр нэр | Утга |
|---|---|---|
| Хүснэгт (table) | relation | Нэг төрлийн зүйлсийн цуглуулга: бараа |
| Мөр (row) | record, tuple | Нэг зүйл: «Чихэвч» |
| Багана (column) | field, attribute | Нэг шинж: үнэ |

`baraa` хүснэгтийн хэсэг:

| baraa_id | ner | angilal_id | une | uldegdel |
|---|---|---|---|---|
| 1 | Ухаалаг утас | 1 | 1250000.00 | 15 |
| 3 | Чихэвч | 1 | 89000.00 | 40 |
| 6 | Монгол түүх | 3 | 35000.00 | 60 |

Багана бүр **нэг төрөлтэй**: `une` нь зөвхөн тоо, `ner` нь зөвхөн текст.
Утга байхгүй нүдийг **NULL** гэнэ — энэ нь 0 ч биш, хоосон текст ч биш.

### Анхдагч түлхүүр (PRIMARY KEY)

Мөр бүрийг **давтагдашгүй** ялгах багана. `baraa_id = 3` гэвэл яг нэг
бараа олдоно.

- Давхардахгүй
- NULL байж болохгүй
- Өөрчлөгддөггүй байх нь зүйтэй

Нэр эсвэл имэйлийг түлхүүр болгож болох ч тэд өөрчлөгддөг. Тиймээс ихэвчлэн
утгагүй тоон `..._id` баганыг автоматаар дугаарлуулна.

### Гадаад түлхүүр (FOREIGN KEY)

Өөр хүснэгтийн анхдагч түлхүүр рүү **заадаг** багана. `baraa.angilal_id = 1`
нь «энэ бараа `angilal` хүснэгтийн 1 дүгээр мөрөнд хамаарна» гэсэн үг.

DBMS нь байхгүй ангилал (жишээ нь 42) руу заахыг **хориглоно**. Үүнийг
лавлагааны бүрэн бүтэн байдал (referential integrity) гэнэ.

### Холбоосын төрлүүд

| Төрөл | Утга | `delguur` дахь жишээ |
|---|---|---|
| 1:N | Нэг нь олонтой | Нэг ангилалд олон бараа |
| N:M | Олон нь олонтой | Нэг захиалгад олон бараа, нэг бараа олон захиалгад |
| Өөрийгөө заах | Хүснэгт өөр рүүгээ | Ажилтны менежер нь бас ажилтан |

N:M холбоосыг шууд хадгалах боломжгүй тул **завсрын хүснэгт** хэрэглэнэ:
`zahialgiin_mur`.

### `delguur` жишээ сангийн бүтэц

Энэ сургалтын бүх жишээ `delguur` (онлайн дэлгүүр) сан дээр ажиллана:

```text
angilal                        hereglegch
  PK angilal_id                  PK hereglegch_id
     ner                            ovog, ner, email, hot,
      |                             utas, burtgesen_ognoo
      | 1:N                          |
      v                              | 1:N
baraa                                v
  PK baraa_id                  zahialga
  FK angilal_id                  PK zahialga_id
     ner, une, uldegdel,         FK hereglegch_id
     nemsen_ognoo                   zahialsan_ognoo, tuluv
      |                              |
      | 1:N                          | 1:N
      |                              |
      +------> zahialgiin_mur <------+
                 PK, FK zahialga_id
                 PK, FK baraa_id
                    too, negj_une

ajiltan
  PK ajiltan_id
  FK menejer_id  --> ajiltan.ajiltan_id
     ner, alban_tushaal, tsalin, ajild_orson
```

### Нэг захиалгыг мөрдөж үзье

1. `zahialga` дахь 1 дүгээр захиалга: `hereglegch_id = 1`, огноо 2024-02-03
2. `hereglegch` дахь 1 дүгээр мөр: **Батын Болд**, Улаанбаатар
3. `zahialgiin_mur` дотор `zahialga_id = 1` мөрүүд:
   - `baraa_id = 1` (Ухаалаг утас), 1 ширхэг × 1 250 000
   - `baraa_id = 3` (Чихэвч), 2 ширхэг × 89 000
4. Нийт дүн: 1 250 000 + 178 000 = **1 428 000** ₮

`zahialgiin_mur`-ийн анхдагч түлхүүр нь **хоёр баганаас** бүтнэ:
`(zahialga_id, baraa_id)`. Нэг захиалгад нэг бараа нэг л удаа орно.

> `negj_une` нь `baraa.une`-г давтсан мэт харагдана. Гэхдээ үнэ дараа нь
> өөрчлөгдөж болно — захиалга хийсэн **тухайн үеийн** үнийг хадгалах ёстой.

### Энэ хичээлийн код

Код нь `tur_zagvar` түр сан үүсгэж, анхдагч ба гадаад түлхүүр алдаатай
мөрийг хэрхэн хаадгийг харуулаад, төгсгөлд нь сангаа устгана.

Энэ бол **урьдчилан харах** скрипт: ажиллуулаад үр дүнг нь хар, мөр бүрийг
одоо цээжлэх шаардлагагүй. Тушаал бүрийг дараа нь нарийн үзнэ:

| Тушаал | Юу хийдэг вэ | Хаана үзэх |
|---|---|---|
| `CREATE TABLE` | Хүснэгт үүсгэнэ | Модул 6 |
| `INSERT INTO … VALUES` | Мөр нэмнэ | Модул 7 |
| `JOIN … ON` | Хоёр хүснэгтийг түлхүүрээр холбож харуулна | Модул 9 |

Алдаатай хоёр мөрийг `INSERT IGNORE`-оор нэмнэ. `IGNORE` нь алдааг
**анхааруулга** (warning) болгож, тэр мөрийг алгасна — скрипт зогсохгүй,
харин алдааны мессеж console дээр анхааруулга болж харагдана. `IGNORE`-гүй бол
MySQL алдаа өгөөд скриптийг тэр мөрөнд зогсооно.
""",
            initial_code="""\
-- tur_zagvar түр санг үүсгээд төгсгөлд устгана.
-- Урьдчилан харах скрипт: ажиллуулаад үр дүнг хар. CREATE TABLE (Модул 6),
-- INSERT (Модул 7), JOIN (Модул 9)-г дараа нь үзнэ.

SET NAMES utf8mb4;

-- 1. Түр сан үүсгэх
DROP DATABASE IF EXISTS tur_zagvar;
CREATE DATABASE tur_zagvar;
USE tur_zagvar;

-- 2. Эх хүснэгт: angilal_id нь анхдагч түлхүүр
CREATE TABLE tur_angilal (
    angilal_id INT         NOT NULL PRIMARY KEY,
    ner        VARCHAR(50) NOT NULL
);

-- 3. Хүүхэд хүснэгт: angilal_id нь гадаад түлхүүр
CREATE TABLE tur_baraa (
    baraa_id   INT          NOT NULL PRIMARY KEY,
    ner        VARCHAR(100) NOT NULL,
    angilal_id INT          NOT NULL,
    FOREIGN KEY (angilal_id) REFERENCES tur_angilal (angilal_id)
);

-- 4. Мөр нэмэх: эхлээд эх, дараа нь хүүхэд
INSERT INTO tur_angilal (angilal_id, ner)
VALUES (1, 'Электроник'), (3, 'Ном');

INSERT INTO tur_baraa (baraa_id, ner, angilal_id)
VALUES (1, 'Ухаалаг утас', 1),
       (3, 'Чихэвч', 1),
       (6, 'Монгол түүх', 3);

-- 5. Хоёр хүснэгтийг түлхүүрээр нь холбож харах
SELECT b.baraa_id, b.ner AS baraa, a.ner AS angilal
FROM tur_baraa AS b
JOIN tur_angilal AS a ON a.angilal_id = b.angilal_id;

-- 6. Анхдагч түлхүүр давхардахыг хориглоно
--    Анхааруулга: 1062 Duplicate entry '1' for key 'tur_angilal.PRIMARY'
INSERT IGNORE INTO tur_angilal (angilal_id, ner) VALUES (1, 'Давхар');

-- 7. Байхгүй ангилал руу заахыг гадаад түлхүүр хориглоно
--    Анхааруулга: 1452 Cannot add or update a child row: a foreign key
--    constraint fails
INSERT IGNORE INTO tur_baraa (baraa_id, ner, angilal_id) VALUES (99, 'Эзэнгүй бараа', 42);

-- 8. Хүснэгтэд алдаатай мөр ороогүйг шалгах: 3 мөр л байна
SELECT * FROM tur_baraa;
SELECT * FROM tur_angilal;

-- 9. Цэвэрлэх
DROP DATABASE IF EXISTS tur_zagvar;
""",
        ),
        LessonSpec(
            title="SQL ба MySQL",
            slug="sql-ba-ayalguu-mysql-sql-server",
            description="SQL стандарт ба аялгуу, тушаалын ангилал, MySQL-ийн онцлог бичлэг.",
            duration=600,
            language=MY,
            content="""\
**SQL** (Structured Query Language) нь хамааралтай өгөгдлийн сантай ярих хэл.
1970-аад онд IBM-д бүтээгдэж, 1986 онд ANSI, 1987 онд ISO стандарт болсон.

### Стандарт ба аялгуу

Стандарт хэд хэдэн удаа шинэчлэгдсэн: SQL-92, SQL:1999, SQL:2003 (цонхны
функц), SQL:2011, SQL:2016 (JSON), SQL:2023. Гэвч DBMS бүр стандартыг
**бүрэн биш** хэрэгжүүлж, өөрийн нэмэлтийг оруулдаг. Үүнийг **аялгуу**
(dialect) гэнэ.

| DBMS | Аялгууны нэр |
|---|---|
| MySQL | MySQL SQL |
| SQL Server | T-SQL (Transact-SQL) |
| Oracle | PL/SQL |
| PostgreSQL | PL/pgSQL (процедурын хэсэг) |

`SELECT`, `WHERE`, `JOIN`, `GROUP BY` зэрэг цөм нь бүгдэд адилхан. Ялгаа
нь функц, төрөл, процедурын бичлэгт гарна. Энэ сургалт **MySQL 8.4**-ийн
аялгуугаар заана.

### Тушаалын ангилал

| Ангилал | Утга | Тушаалууд |
|---|---|---|
| **DDL** — Data Definition | Бүтэц үүсгэх, өөрчлөх | `CREATE`, `ALTER`, `DROP`, `TRUNCATE` |
| **DML** — Data Manipulation | Өгөгдөл унших, өөрчлөх | `SELECT`, `INSERT`, `UPDATE`, `DELETE` |
| **DCL** — Data Control | Эрх олгох, хасах | `GRANT`, `REVOKE` |
| **TCL** — Transaction Control | Гүйлгээ удирдах | `START TRANSACTION`, `COMMIT`, `ROLLBACK`, `SAVEPOINT` |

> Зарим эх сурвалж `SELECT`-ийг тусад нь **DQL** (Data Query Language)
> гэж ангилдаг.

### MySQL

| | |
|---|---|
| Эзэмшигч | Oracle |
| Лиценз | Community: нээлттэй эх (GPLv2), Enterprise: төлбөртэй |
| Платформ | Windows, Linux, macOS, Docker |
| GUI хэрэгсэл | MySQL Workbench |
| Тушаалын мөр | `mysql` |
| Түгээмэл орчин | Вэб сайт, WordPress, PHP, стартап, SaaS |

MySQL-ийн «ах дүү» **MariaDB** нь MySQL-ээс салбарласан тул бичлэг нь
бараг адилхан.

### MySQL-ийн онцлог бичлэг

Дараах бичлэгүүд MySQL-д байдаг. Бусад DBMS-д заримыг нь өөрөөр бичдэг
тул өөр сан руу шилжихдээ түүний баримт бичгийг хараарай.

| Зорилго | MySQL | Хаана үзэх |
|---|---|---|
| Эхний 5 мөр | `SELECT ... LIMIT 5` | Модул 2 |
| Хуудаслалт | `LIMIT 10 OFFSET 20` | Модул 2 |
| Одоогийн огноо цаг | `NOW()` | Модул 4 |
| Текстийн урт | `CHAR_LENGTH(s)` | Модул 4 |
| Автомат дугаар | `INT AUTO_INCREMENT` | Модул 6, 8 |
| Кирилл текст | `VARCHAR` + `utf8mb4` | Модул 1, 6 |
| Логик төрөл | `BOOLEAN` (= `TINYINT(1)`) | Модул 6 |
| NULL-ийг орлуулах | `IFNULL(a, b)` | Модул 11 |
| Нэр хашилт | `` `order` `` | Модул 12 |
| Гүйлгээ эхлэх | `START TRANSACTION` | Модул 14 |
| Процедурын тусгаарлагч | `DELIMITER $$` | Модул 16 |

Стандарт SQL-ийн олон зүйл MySQL-д ч бий: `CONCAT`, `COALESCE`,
`CURRENT_TIMESTAMP`, `CASE`, `DROP TABLE IF EXISTS`.

Жишээ — хамгийн үнэтэй 3 бараа:

```sql
SELECT ner, une FROM baraa ORDER BY une DESC LIMIT 3;
```

### Анхаарах урхиуд

- MySQL-ийн `ISNULL(x)` функц **нэг** аргументтай бөгөөд 1 эсвэл 0
  буцаана. NULL-ийг орлуулахад `IFNULL(a, b)` эсвэл `COALESCE(a, b)`.
- MySQL нь `"текст"` давхар хашилтыг анхдагчаар текст гэж ойлгоно. Харин
  SQL стандартад давхар хашилт нь **нэр** хашилт. Текстэд үргэлж `'...'`
  хэрэглэ.
- `DELIMITER` нь SQL тушаал **биш** — `mysql` клиент, Workbench-ийн
  тушаал. Сервер рүү илгээгддэггүй. Модул 16-д үзнэ.

### Энэ сургалтын журам

- Бүх хичээлийн код **MySQL 8.4** дээр ажиллана.
- **«Код ажиллуулах»** товч кодыг манай тусгаарлагдсан MySQL сервер дээр
  ажиллуулж, үр дүнг `mysql` CLI шиг хүснэгтээр харуулна.
- Ажиллуулалт бүр `delguur`, `nomiin_san` жишээ сангууд **анхны төлөвтэй**
  серверээс эхэлнэ. Өгөгдлийг устгасан ч дараагийн ажиллуулалтад сэргэнэ —
  айлгүй туршаарай.
- Ижил кодыг өөрийн компьютер дээрх MySQL-д (Workbench эсвэл `mysql` CLI)
  ч хуулж ажиллуулж болно.

Доорх код ямар ч хүснэгт шаардахгүй. Энэ бол **тойм**: дээрх хүснэгтийн
хэдэн мөрийг ажиллуулж харуулна. Функц бүрийг дараагийн модулиудад нарийн
үзнэ — `NOW`, `CONCAT`, `CHAR_LENGTH`-ийг Модул 4-т, `IFNULL`, `COALESCE`-ийг
Модул 11-д.
""",
            initial_code="""\
-- Хүснэгт шаардахгүй, шууд ажиллуулж болно.
-- Тойм: ажиллуулж үр дүнг хар. Функц бүрийг Модул 4, 11-д нарийн үзнэ.

-- Кирилл үсэг зөв дамжихын тулд холболтыг utf8mb4 болгоно
SET NAMES utf8mb4;

-- 1. Одоогийн огноо ба цаг
SELECT NOW() AS odoo;

-- 2. NULL утгыг өөр утгаар орлуулах
SELECT IFNULL(NULL, 'утасгүй') AS utas;

-- 3. SQL стандартын ижил үүрэгтэй функц
SELECT COALESCE(NULL, 'утасгүй') AS utas;

-- 4. Нөөц үгийг нэр болгох: backtick хашилт
SELECT 'Хүргэгдсэн' AS `order`;

-- 5. Текст нийлүүлэх
SELECT CONCAT('Батын', ' ', 'Болд') AS buten_ner;

-- 6. Кирилл текстийн урт: тэмдэгтээр ба байтаар
SELECT CHAR_LENGTH('Монгол') AS temdegt, LENGTH('Монгол') AS bait;

-- LIMIT-ийг Модул 2-т delguur сан дээр ажиллуулж үзнэ.
""",
        ),
    ],
)

ENVIRONMENT = ModuleSpec(
    title="Модул 1 — Жишээ сан",
    description="Бүх хичээлийн ашиглах delguur жишээ сантай танилцана.",
    lessons=[
        LessonSpec(
            title="Жишээ сан — delguur",
            slug="delguur-san-mysql",
            description="delguur онлайн дэлгүүрийн санг MySQL дээр үүсгэж, хүснэгт бүрийг танина.",
            duration=720,
            language=MY,
            content="""\
Энэ сургалтын бараг бүх хичээл **`delguur`** (онлайн дэлгүүр) сан дээр
ажиллана. Доорх анхны код нь санг **бүтнээр нь** үүсгэнэ.

Энэ сайт дээр `delguur` сан **аль хэдийн бэлэн**: ажиллуулалт бүр анхны
төлөвтэй сангаас эхэлдэг. Энэ скриптийг «Код ажиллуулах»-аар ажиллуулбал
санг дахин үүсгээд мөрийн тоог шалгана.

> Скрипт нь эхэндээ `DROP DATABASE IF EXISTS delguur` хийдэг. Дахин
> ажиллуулахад таны бүх өөрчлөлт **устаж**, анхны өгөгдөл сэргэнэ. Санг
> эвдэрчихвэл энэ скриптийг л дахин ажиллуул.

### Скриптийн бүтэц

1. `SET NAMES utf8mb4` — клиент ба серверийн хооронд кирилл зөв дамжина
2. Санг `utf8mb4`, `utf8mb4_0900_ai_ci`-тэй шинээр үүсгэнэ
3. Хүснэгтүүдийг **гадаад түлхүүрийн дарааллаар** үүсгэнэ: эх хүснэгт
   (`angilal`, `hereglegch`) эхэлж, түүн рүү заадаг хүснэгт дараа нь
4. Өгөгдлийг мөн адил дарааллаар оруулна
5. Хүснэгт бүрийн мөрийн тоог шалгана

`id`-г `INSERT`-д шууд бичсэн тул дугаар яг таарна. `AUTO_INCREMENT` багана
руу утга шууд бичихэд тоолуур хамгийн их утгаас үргэлжилнэ: дараагийн
бараа 13 дугаартай болно.

> Энэ бол **бэлдэх скрипт** — одоо ажиллуулахад л хангалттай. Доторх
> тушаалуудыг дараа нь нэг бүрчлэн үзнэ: `CREATE TABLE`-ийг Модул 6-д,
> `INSERT`-ийг Модул 7-д, хязгаарлалтуудыг (`FOREIGN KEY`, `CHECK`) Модул
> 8-д. Төгсгөлийн мөр тоолох шалгалт `COUNT(*)`-ыг Модул 5-д үзнэ.

### `angilal` — барааны ангилал

| Багана | Төрөл | Тайлбар |
|---|---|---|
| `angilal_id` | `INT AUTO_INCREMENT` | Анхдагч түлхүүр |
| `ner` | `VARCHAR(50)` | Ангиллын нэр, давтагдашгүй (`UNIQUE`) |

### `baraa` — бараа

| Багана | Төрөл | Тайлбар |
|---|---|---|
| `baraa_id` | `INT AUTO_INCREMENT` | Анхдагч түлхүүр |
| `ner` | `VARCHAR(100)` | Барааны нэр |
| `angilal_id` | `INT` | → `angilal.angilal_id` |
| `une` | `DECIMAL(12,2)` | Үнэ, ₮. `CHECK (une >= 0)` |
| `uldegdel` | `INT` | Агуулахын үлдэгдэл, анхдагч 0 |
| `nemsen_ognoo` | `DATE` | Дэлгүүрт нэмэгдсэн огноо |

Мөнгийг `FLOAT` биш **`DECIMAL`**-аар хадгална — `FLOAT` нь бутархайг
яг хадгалж чаддаггүй.

### `hereglegch` — хэрэглэгч

| Багана | Төрөл | Тайлбар |
|---|---|---|
| `hereglegch_id` | `INT AUTO_INCREMENT` | Анхдагч түлхүүр |
| `ovog`, `ner` | `VARCHAR(50)` | Овог, нэр |
| `email` | `VARCHAR(100)` | Имэйл, давтагдашгүй |
| `hot` | `VARCHAR(50)` NULL | Хот — мэдэгдэхгүй бол NULL |
| `utas` | `VARCHAR(20)` NULL | Утас — тоо биш текст: `0`-ээр эхэлж, тооцоо хийхгүй |
| `burtgesen_ognoo` | `DATE` | Бүртгүүлсэн огноо |

### `zahialga` — захиалга

| Багана | Төрөл | Тайлбар |
|---|---|---|
| `zahialga_id` | `INT AUTO_INCREMENT` | Анхдагч түлхүүр |
| `hereglegch_id` | `INT` | → `hereglegch.hereglegch_id` |
| `zahialsan_ognoo` | `DATETIME` | Огноо ба цаг |
| `tuluv` | `VARCHAR(20)` | `Хүлээгдэж буй` (анхдагч), `Хүргэгдсэн`, `Цуцлагдсан` |

### `zahialgiin_mur` — захиалгын мөр

| Багана | Төрөл | Тайлбар |
|---|---|---|
| `zahialga_id` | `INT` | PK-ийн хэсэг, → `zahialga` |
| `baraa_id` | `INT` | PK-ийн хэсэг, → `baraa` |
| `too` | `INT` | Тоо ширхэг, `CHECK (too > 0)` |
| `negj_une` | `DECIMAL(12,2)` | Захиалах үеийн нэгж үнэ |

Мөрийн дүн = `too * negj_une`. Захиалгын нийт дүн нь мөрүүдийн нийлбэр.

### `ajiltan` — ажилтан

| Багана | Төрөл | Тайлбар |
|---|---|---|
| `ajiltan_id` | `INT AUTO_INCREMENT` | Анхдагч түлхүүр |
| `ner` | `VARCHAR(100)` | Нэр |
| `alban_tushaal` | `VARCHAR(50)` | Албан тушаал |
| `menejer_id` | `INT` NULL | → `ajiltan.ajiltan_id`. Захирал NULL |
| `tsalin` | `DECIMAL(12,2)` | Сарын цалин |
| `ajild_orson` | `DATE` | Ажилд орсон огноо |

### Дасгалд хэрэг болох баримтууд

- 5 дугаар бараа **Гутал** хэзээ ч захиалагдаагүй
- 8 дугаар хэрэглэгч **Мөнх** захиалга хийгээгүй
- 5, 11 дүгээр барааны үлдэгдэл 0
- 2, 6 дугаар хэрэглэгчийн утас NULL, 6 дугаарынх хот нь бас NULL
- 4 дүгээр захиалга цуцлагдсан

### Хүлээгдэж буй үр дүн

Скриптийн төгсгөлийн шалгалт:

| husnegt | mur_too |
|---|---|
| angilal | 5 |
| baraa | 12 |
| hereglegch | 8 |
| zahialga | 10 |
| zahialgiin_mur | 19 |
| ajiltan | 6 |

> MySQL 8.0.16-аас өмнө `CHECK` хязгаарлалт бичигдэх боловч **шалгагддаггүй**
> байсан. 8.0.16+ дээр бүрэн ажиллана.
""",
            initial_code="""\
-- delguur жишээ сан: MySQL 8.0 болон түүнээс шинэ хувилбарт.
-- Дахин ажиллуулж болно: хуучин сан устаж, анхны өгөгдөл сэргэнэ.

SET NAMES utf8mb4;

-- 1. Санг шинээр үүсгэх
DROP DATABASE IF EXISTS delguur;
CREATE DATABASE delguur CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE delguur;

-- 2. Хүснэгтүүд: эх хүснэгт эхэлж, түүн рүү заадаг нь дараа нь
CREATE TABLE angilal (
    angilal_id INT AUTO_INCREMENT PRIMARY KEY,
    ner        VARCHAR(50) NOT NULL,
    CONSTRAINT uq_angilal_ner UNIQUE (ner)
);

CREATE TABLE baraa (
    baraa_id     INT AUTO_INCREMENT PRIMARY KEY,
    ner          VARCHAR(100)  NOT NULL,
    angilal_id   INT           NOT NULL,
    une          DECIMAL(12,2) NOT NULL,
    uldegdel     INT           NOT NULL DEFAULT 0,
    nemsen_ognoo DATE          NOT NULL,
    CONSTRAINT fk_baraa_angilal FOREIGN KEY (angilal_id)
        REFERENCES angilal (angilal_id),
    CONSTRAINT ck_baraa_une CHECK (une >= 0)
);

CREATE TABLE hereglegch (
    hereglegch_id   INT AUTO_INCREMENT PRIMARY KEY,
    ovog            VARCHAR(50)  NOT NULL,
    ner             VARCHAR(50)  NOT NULL,
    email           VARCHAR(100) NOT NULL,
    hot             VARCHAR(50)  NULL,
    utas            VARCHAR(20)  NULL,
    burtgesen_ognoo DATE         NOT NULL,
    CONSTRAINT uq_hereglegch_email UNIQUE (email)
);

CREATE TABLE zahialga (
    zahialga_id     INT AUTO_INCREMENT PRIMARY KEY,
    hereglegch_id   INT         NOT NULL,
    zahialsan_ognoo DATETIME    NOT NULL,
    tuluv           VARCHAR(20) NOT NULL DEFAULT 'Хүлээгдэж буй',
    CONSTRAINT fk_zahialga_hereglegch FOREIGN KEY (hereglegch_id)
        REFERENCES hereglegch (hereglegch_id)
);

CREATE TABLE zahialgiin_mur (
    zahialga_id INT           NOT NULL,
    baraa_id    INT           NOT NULL,
    too         INT           NOT NULL,
    negj_une    DECIMAL(12,2) NOT NULL,
    PRIMARY KEY (zahialga_id, baraa_id),
    CONSTRAINT fk_mur_zahialga FOREIGN KEY (zahialga_id)
        REFERENCES zahialga (zahialga_id),
    CONSTRAINT fk_mur_baraa FOREIGN KEY (baraa_id)
        REFERENCES baraa (baraa_id),
    CONSTRAINT ck_mur_too CHECK (too > 0)
);

CREATE TABLE ajiltan (
    ajiltan_id    INT AUTO_INCREMENT PRIMARY KEY,
    ner           VARCHAR(100)  NOT NULL,
    alban_tushaal VARCHAR(50)   NOT NULL,
    menejer_id    INT           NULL,
    tsalin        DECIMAL(12,2) NOT NULL,
    ajild_orson   DATE          NOT NULL,
    CONSTRAINT fk_ajiltan_menejer FOREIGN KEY (menejer_id)
        REFERENCES ajiltan (ajiltan_id)
);

-- 3. Өгөгдөл оруулах
INSERT INTO angilal (angilal_id, ner) VALUES
    (1, 'Электроник'),
    (2, 'Хувцас'),
    (3, 'Ном'),
    (4, 'Гэр ахуй'),
    (5, 'Хүнс');

INSERT INTO baraa (baraa_id, ner, angilal_id, une, uldegdel, nemsen_ognoo) VALUES
    (1,  'Ухаалаг утас',       1, 1250000.00,  15, '2024-01-10'),
    (2,  'Зөөврийн компьютер', 1, 3200000.00,   6, '2024-01-15'),
    (3,  'Чихэвч',             1,   89000.00,  40, '2024-02-01'),
    (4,  'Ноосон цамц',        2,  145000.00,  25, '2024-02-10'),
    (5,  'Гутал',              2,  210000.00,   0, '2024-03-05'),
    (6,  'Монгол түүх',        3,   35000.00,  60, '2024-01-20'),
    (7,  'SQL сурах бичиг',    3,   48000.00,  12, '2024-04-01'),
    (8,  'Цайны аяга',         4,   18000.00, 100, '2024-02-25'),
    (9,  'Тоос сорогч',        4,  560000.00,   4, '2024-03-18'),
    (10, 'Ааруул',             5,   12000.00, 200, '2024-04-10'),
    (11, 'Сүүтэй цай',         5,    3500.00,   0, '2024-04-12'),
    (12, 'Хөнжил',             4,  185000.00,   9, '2024-05-02');

INSERT INTO hereglegch (hereglegch_id, ovog, ner, email, hot, utas, burtgesen_ognoo) VALUES
    (1, 'Батын',       'Болд',     'bold@example.mn',     'Улаанбаатар', '99112233', '2023-11-02'),
    (2, 'Доржийн',     'Сараа',    'saraa@example.mn',    'Улаанбаатар', NULL,       '2023-12-15'),
    (3, 'Ганбаатарын', 'Тэмүүлэн', 'temuulen@example.mn', 'Дархан',      '88001122', '2024-01-08'),
    (4, 'Цэрэнгийн',   'Номин',    'nomin@example.mn',    'Эрдэнэт',     '95554433', '2024-02-20'),
    (5, 'Эрдэнийн',    'Анар',     'anar@example.mn',     'Улаанбаатар', '99887766', '2024-03-01'),
    (6, 'Мөнхийн',     'Хулан',    'hulan@example.mn',    NULL,          NULL,       '2024-03-22'),
    (7, 'Отгоны',      'Энх',      'enh@example.mn',      'Дархан',      '80112244', '2024-04-05'),
    (8, 'Сүхийн',      'Мөнх',     'munh@example.mn',     'Улаанбаатар', '91234567', '2024-05-11');

INSERT INTO zahialga (zahialga_id, hereglegch_id, zahialsan_ognoo, tuluv) VALUES
    (1,  1, '2024-02-03 10:15:00', 'Хүргэгдсэн'),
    (2,  2, '2024-02-14 18:40:00', 'Хүргэгдсэн'),
    (3,  1, '2024-03-09 09:05:00', 'Хүргэгдсэн'),
    (4,  3, '2024-03-21 14:30:00', 'Цуцлагдсан'),
    (5,  4, '2024-04-02 11:00:00', 'Хүргэгдсэн'),
    (6,  5, '2024-04-18 20:10:00', 'Хүргэгдсэн'),
    (7,  2, '2024-05-06 13:25:00', 'Хүлээгдэж буй'),
    (8,  6, '2024-05-20 16:45:00', 'Хүргэгдсэн'),
    (9,  7, '2024-06-01 08:50:00', 'Хүлээгдэж буй'),
    (10, 1, '2024-06-12 19:30:00', 'Хүлээгдэж буй');

INSERT INTO zahialgiin_mur (zahialga_id, baraa_id, too, negj_une) VALUES
    (1,  1,  1, 1250000.00),
    (1,  3,  2,   89000.00),
    (2,  4,  1,  145000.00),
    (2,  8,  4,   18000.00),
    (3,  6,  2,   35000.00),
    (3,  7,  1,   48000.00),
    (4,  2,  1, 3200000.00),
    (5,  9,  1,  560000.00),
    (5,  10, 10,  12000.00),
    (6,  1,  1, 1250000.00),
    (6,  12, 2,  185000.00),
    (7,  3,  1,   89000.00),
    (7,  6,  1,   35000.00),
    (7,  11, 6,    3500.00),
    (8,  4,  2,  145000.00),
    (9,  7,  3,   48000.00),
    (9,  10, 5,   12000.00),
    (10, 2,  1, 3200000.00),
    (10, 3,  1,   89000.00);

INSERT INTO ajiltan (ajiltan_id, ner, alban_tushaal, menejer_id, tsalin, ajild_orson) VALUES
    (1, 'Батбаяр',  'Захирал',              NULL, 6500000.00, '2019-03-01'),
    (2, 'Оюунаа',   'Борлуулалтын менежер', 1,    4200000.00, '2020-06-15'),
    (3, 'Ганзориг', 'Агуулахын менежер',    1,    3900000.00, '2020-09-01'),
    (4, 'Солонго',  'Борлуулагч',           2,    2400000.00, '2022-01-10'),
    (5, 'Тэмүүжин', 'Борлуулагч',           2,    2300000.00, '2023-04-03'),
    (6, 'Цэцэг',    'Нярав',                3,    2100000.00, '2021-11-20');

-- 4. Шалгах: 5, 12, 8, 10, 19, 6 мөр гарах ёстой
SELECT 'angilal' AS husnegt, COUNT(*) AS mur_too FROM angilal
UNION ALL SELECT 'baraa', COUNT(*) FROM baraa
UNION ALL SELECT 'hereglegch', COUNT(*) FROM hereglegch
UNION ALL SELECT 'zahialga', COUNT(*) FROM zahialga
UNION ALL SELECT 'zahialgiin_mur', COUNT(*) FROM zahialgiin_mur
UNION ALL SELECT 'ajiltan', COUNT(*) FROM ajiltan;
""",
        ),
    ],
)

SQL_FUNDAMENTAL_MODULES = [DB_FUNDAMENTALS, ENVIRONMENT]
