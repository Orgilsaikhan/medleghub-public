"""Модул 6-8 — Хүснэгт үүсгэх, өгөгдөл өөрчлөх, хязгаарлалт.

SELECT-ээс цааш: хүснэгтийн бүтцийг өөрөө тодорхойлж, мөр нэмэх, засах,
устгах, буруу өгөгдлөөс хязгаарлалтаар хамгаалах.
"""

from app.content.types import LessonSpec, ModuleSpec
from app.models.enums import LessonLanguage

MY = LessonLanguage.MYSQL

CREATING_TABLES = ModuleSpec(
    title="Модул 6 — Хүснэгт үүсгэх",
    description="Өгөгдлийн төрөл, CREATE, ALTER, DROP.",
    lessons=[
        LessonSpec(
            title="Өгөгдлийн төрлүүд",
            slug="sql-ogogdliin-turluud",
            description="Тоо, текст, огноо, логик төрлийг зөв сонгох, strict горим.",
            duration=660,
            language=MY,
            content="""\
Багана бүр **төрөлтэй**. Төрөл нь юу хадгалах, хэдэн байт эзлэх, ямар
утгыг хүлээж авахгүйг тодорхойлно. Мөр олширсон хойно төрөл солих нь
хэцүү тул эхнээс нь зөв сонго.

### Үндсэн төрлүүд

| Хэрэглээ | MySQL төрөл | Тайлбар |
|---|---|---|
| Бүхэл тоо | `INT` | 4 байт, ±2.1 тэрбум |
| Том бүхэл тоо | `BIGINT` | 8 байт |
| Жижиг бүхэл | `TINYINT`, `SMALLINT` | 1 байт (−128…127), 2 байт |
| Сөрөггүй тоо | `INT UNSIGNED` | 0…4.2 тэрбум |
| Мөнгө, яг тоо | `DECIMAL(p,s)` | p ≤ 65 орон |
| Ойролцоо тоо | `FLOAT`, `DOUBLE` | Шинжлэх ухааны тооцоо |
| Текст | `VARCHAR(n)` | n тэмдэгт хүртэл |
| Урт текст | `TEXT`, `MEDIUMTEXT`, `LONGTEXT` | 64 КБ, 16 МБ, 4 ГБ |
| Тогтмол урт | `CHAR(n)` | Үргэлж n тэмдэгт |
| Огноо | `DATE` | `2024-02-03` |
| Огноо + цаг | `DATETIME`, `TIMESTAMP` | `2024-02-03 10:15:00` |
| Тийм / Үгүй | `BOOLEAN` | `TINYINT(1)`-ийн өөр нэр |
| JSON баримт | `JSON` | Бүтэцтэй өгөгдөл |

### INT ба BIGINT

`INT`-ийн дээд хязгаар 2 147 483 647 (≈2.1 тэрбум) — ихэнх id-д хангалттай.
Лог, үзэлт гэх мэт тэрбумаар өсөх хүснэгтэд `BIGINT`.

> MySQL-ийн `INT(11)` дахь тоо нь зөвхөн **харуулах өргөн** бөгөөд 8.0.17-оос
> хуучирсан (deprecated). Хадгалах хүрээнд огт нөлөөлдөггүй.

### Мөнгөнд DECIMAL, FLOAT биш

`DECIMAL(12,2)` — нийт 12 орон, үүнээс 2 нь бутархай. Утгыг **яг**
хадгална. `FLOAT`/`DOUBLE` нь хоёртын бутархай тул 0.1 яг хадгалагддаггүй:

```sql
-- 0.1e0 бичиглэл DOUBLE, 0.1 бичиглэл DECIMAL
SELECT 0.1e0 + 0.2e0 = 0.3e0;   -- 0 (тэнцүү биш)
SELECT 0.1 + 0.2 = 0.3;         -- 1 (тэнцүү)
```

`DECIMAL(12,2)` баганад `19.999` өгвөл `20.00` болж дугуйлагдана.

### VARCHAR — кирилл үсэг

`VARCHAR(50)` = 50 **тэмдэгт** (байт биш). Кодчилол нь хүснэгтийн
charset-ээс хамаарна. MySQL 8.0-ийн анхдагч `utf8mb4` дээр латин үсэг 1
байт, кирилл үсэг 2 байт, emoji 4 байт эзэлнэ.

> MySQL-ийн `utf8` нь үнэндээ `utf8mb3` (3 байт хүртэл) — хуучирсан, emoji
> хадгалж чаддаггүй. Үргэлж `utf8mb4` бич.

| Шалгах | Функц | `'Сараа'` |
|---|---|---|
| Тэмдэгтийн тоо | `CHAR_LENGTH` | 5 |
| Байтын тоо | `LENGTH` | 10 |

### TEXT ба VARCHAR

| Төрөл | Дээд хэмжээ |
|---|---|
| `TEXT` | 64 КБ |
| `MEDIUMTEXT` | 16 МБ |
| `LONGTEXT` | 4 ГБ |

`TEXT` баганад `DEFAULT` утга өгөхөд хаалттай илэрхийлэл хэрэгтэй, индекс
хийхэд угтварын урт заах шаардлагатай. Тиймээс нэр, имэйл зэрэг богино
утганд `VARCHAR`, нийтлэл, тайлбар зэрэг урт текстэд `TEXT`.

### Огноо ба цаг

| Төрөл | Хүрээ | Онцлог |
|---|---|---|
| `DATE` | 1000–9999 он | Зөвхөн огноо |
| `DATETIME` | 1000–9999 он | Бичсэнээрээ хадгална |
| `DATETIME(6)` | — | Микросекунд хүртэл |
| `TIMESTAMP` | 1970–2038 он | UTC болгож хадгалаад холболтын цагийн бүсээр харуулна |

`TIMESTAMP`-ийн 2038 оны хязгаар нь төрсөн огноо, гэрээний дуусах огноо
зэрэгт тохиромжгүй — ихэнх тохиолдолд `DATETIME` сонго.
`ON UPDATE CURRENT_TIMESTAMP` нь мөр засагдах бүрт баганыг автоматаар
шинэчилнэ — «сүүлд засагдсан» баганад тохиромжтой.

### BOOLEAN

`BOOLEAN` нь `TINYINT(1)`-ийн синоним. `TRUE` = 1, `FALSE` = 0.
`WHERE idevhtei` гэж шууд бичиж болно. `DESCRIBE` хийхэд `tinyint(1)`
гэж харагдана.

### CHAR ба VARCHAR

`CHAR(n)` тогтмол урттай — богино утгыг хоосон зайгаар дүүргэнэ. Улсын код
(`'MN'`) гэх мэт **үргэлж ижил урттай** утганд. Бусад бүх текстэд `VARCHAR`.

### Strict горим

MySQL 8-ийн анхдагч `sql_mode`-д `STRICT_TRANS_TABLES` орсон. Энэ горимд
баганад **багтахгүй** утга (хэт том тоо, хэт урт текст, буруу огноо)
оруулахад MySQL алдаа өгч, мөрийг хүлээж авахгүй:

| Зөрчил | Алдаа |
|---|---|
| `INT` баганад 3 000 000 000 | 1264 `Out of range value` |
| `VARCHAR(5)` баганад 10 тэмдэгт | 1406 `Data too long` |
| `DATE` баганад `'2024-02-30'` | 1292 `Incorrect date value` |

Горимыг `SELECT @@sql_mode;`-оор шалгана. Хуучин системд strict горим
унтраалттай бол MySQL утгыг чимээгүй таслаж, анхааруулга л үлдээдэг —
өгөгдөл эвдрэх шалтгаан болно. **Бүү унтраа.**

> JSON хадгалах: MySQL-д `JSON` төрөл бий — утгыг хүчинтэй JSON эсэхийг
> шалгаж хадгална.
""",
            initial_code="""\
USE delguur;

-- 1. DECIMAL ба DOUBLE: 0.1 + 0.2 яг 0.3 болох уу
SELECT 0.1 + 0.2 = 0.3       AS decimal_tentsuu,   -- 1
       0.1e0 + 0.2e0 = 0.3e0 AS double_tentsuu;    -- 0

-- 2. Кирилл: тэмдэгт ба байт (utf8mb4)
SELECT CHAR_LENGTH('Сараа') AS temdegt,   -- 5
       LENGTH('Сараа')      AS bait;      -- 10

-- 3. Олон төрөлтэй түр хүснэгт
DROP TABLE IF EXISTS tur_turul;

CREATE TABLE tur_turul (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    too_shirheg   INT NOT NULL,                  -- 2.1 тэрбум хүртэл
    tom_too       BIGINT NOT NULL,               -- маш том тоо
    une           DECIMAL(12,2) NOT NULL,        -- мөнгө: яг утга
    oiroltsoo     DOUBLE NOT NULL,               -- ойролцоо утга
    ner           VARCHAR(50) NOT NULL,          -- 50 тэмдэгт
    ulsiin_kod    CHAR(2) NOT NULL,              -- үргэлж 2 тэмдэгт
    tailbar       TEXT NULL,                     -- урт текст
    tursun_udur   DATE NULL,
    uussen        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    shinechilsen  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                  ON UPDATE CURRENT_TIMESTAMP,   -- засах бүрд шинэчлэгдэнэ
    idevhtei      BOOLEAN NOT NULL DEFAULT TRUE  -- TINYINT(1) болно
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- INSERT INTO хүснэгт (баганууд) VALUES (утгууд) нь шинэ мөр нэмнэ.
-- Төрөл хэрхэн ажиллахыг харахад л хэрэглэж байна — Модул 7-д нарийн үзнэ.
INSERT INTO tur_turul
    (too_shirheg, tom_too, une, oiroltsoo, ner, ulsiin_kod, tailbar, tursun_udur)
VALUES
    (15, 9000000000, 1250000.00, 0.1, 'Ухаалаг утас', 'MN',
     'Урт тайлбар энд орно', '2000-05-17');

SELECT * FROM tur_turul;

-- 4. BOOLEAN нь TINYINT(1) болсныг харах
DESCRIBE tur_turul;

-- 5. DECIMAL(12,2)-т 3 бутархай орон өгвөл дугуйлна
INSERT INTO tur_turul
    (too_shirheg, tom_too, une, oiroltsoo, ner, ulsiin_kod)
VALUES
    (1, 1, 19.999, 0.1, 'Дугуйралт', 'MN');
SHOW WARNINGS;
SELECT id, une FROM tur_turul;

-- 6. Хүрээнээс хэтэрвэл strict mode алдаа өгнө (тайлбарыг арилгаж үз):
-- INSERT INTO tur_turul (too_shirheg, tom_too, une, oiroltsoo, ner, ulsiin_kod)
-- VALUES (3000000000, 1, 1, 1, 'Хэт том', 'MN');
-- ERROR 1264: Out of range value

-- 7. Цэвэрлэх
DROP TABLE IF EXISTS tur_turul;
""",
        ),
        LessonSpec(
            title="CREATE DATABASE ба CREATE TABLE",
            slug="mysql-create-database-table",
            description="MySQL дээр сан, хүснэгт үүсгэж бүтцийг нь шалгах.",
            duration=540,
            language=MY,
            content="""\
### CREATE DATABASE

```sql
CREATE DATABASE IF NOT EXISTS tur_dadlaga
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_0900_ai_ci;

SHOW DATABASES;
USE tur_dadlaga;
SELECT DATABASE();          -- одоо аль сан дээр байгаа вэ
DROP DATABASE IF EXISTS tur_dadlaga;
```

- `IF NOT EXISTS` — байгаа бол алдаа биш, зөвхөн сануулга (note).
- `CHARACTER SET utf8mb4` — кирилл, emoji бүгдийг хадгална. MySQL 8.0-д
  анхдагч нь аль хэдийн `utf8mb4`, гэхдээ тодорхой бичих нь найдвартай.
- `ai_ci` — accent-insensitive, case-insensitive: `'bold' = 'BOLD'` үнэн.

> MySQL-д `DATABASE` ба `SCHEMA` нь **ижил зүйл** (`CREATE SCHEMA` гэж ч
> бичиж болно). Бусад зарим DBMS-д schema нь сан доторх нэрсийн орон зай —
> өөр ойлголт.

### CREATE TABLE

```sql
CREATE TABLE tur_hereglegch (
    hereglegch_id INT AUTO_INCREMENT PRIMARY KEY,
    ovog          VARCHAR(50)  NOT NULL,
    ner           VARCHAR(50)  NOT NULL,
    email         VARCHAR(100) NOT NULL UNIQUE,
    idevhtei      BOOLEAN      NOT NULL DEFAULT TRUE,
    burtgesen     DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
```

Бүтэц: `багана төрөл [хязгаарлалт]`, таслалаар тусгаарлана. Сүүлийн
баганын дараа таслал **тавихгүй** — хамгийн түгээмэл синтакс алдаа.

| Хэсэг | Утга |
|---|---|
| `AUTO_INCREMENT` | Шинэ мөр бүрт 1, 2, 3… автоматаар |
| `PRIMARY KEY` | Мөрийг давтагдашгүй тодорхойлно |
| `NOT NULL` | Хоосон байж болохгүй |
| `UNIQUE` | Давтагдах ёсгүй |
| `DEFAULT` | Утга өгөөгүй үед |
| `ENGINE = InnoDB` | Transaction, FOREIGN KEY дэмжинэ (8.0-ийн анхдагч) |

Хязгаарлалтыг Модул 8-д дэлгэрэнгүй үзнэ.

### Бүтцийг шалгах

```sql
SHOW TABLES;
DESCRIBE tur_hereglegch;          -- багана, төрөл, NULL, түлхүүр
SHOW CREATE TABLE tur_hereglegch; -- бүрэн CREATE тушаал
```

`SHOW CREATE TABLE` нь MySQL өөрөө нэмсэн анхдагч утгыг (collation гэх
мэт) бүгдийг харуулдаг тул хүснэгтийг өөр серверт хуулахад хэрэгтэй.

### Байгаа хүснэгтээс үүсгэх

```sql
-- Бүтцийг л хуулна (индекс, AUTO_INCREMENT орно; өгөгдөл, FOREIGN KEY орохгүй)
CREATE TABLE tur_baraa_huulbar LIKE baraa;

-- SELECT-ийн үр дүнгээр (өгөгдөл орно, PRIMARY KEY орохгүй)
CREATE TABLE tur_elektronik AS
SELECT baraa_id, ner, une FROM baraa WHERE angilal_id = 1;
```

> `CREATE TABLE … AS SELECT` нь зөвхөн багана, төрлийг авна — PRIMARY KEY,
> AUTO_INCREMENT, индекс алга болно. Хуулбарыг байнгын хүснэгт болгох бол
> дараа нь түлхүүрийг нэмэх ёстой.

### Нэрлэх зөвлөмж

- Жижиг үсэг, доогуур зураас: `zahialgiin_mur`. Linux дээрх MySQL-д
  хүснэгтийн нэр **том жижиг үсэг ялгадаг**, Windows дээр ялгадаггүй —
  жижиг үсгээр бичвэл хоёуланд нь ажиллана.
- Нөөц үгийг (`order`, `group`, `key`) нэр болгохгүй. Заавал бол
  `` `order` `` гэж backtick-ээр хашина (Модул 12).
""",
            initial_code="""\
USE delguur;

-- 1. Шинэ өгөгдлийн сан үүсгэх
CREATE DATABASE IF NOT EXISTS tur_dadlaga
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_0900_ai_ci;

SHOW DATABASES LIKE 'tur%';
SHOW CREATE DATABASE tur_dadlaga;

-- Шинэ сан руу шилжээд буцах
USE tur_dadlaga;
SELECT DATABASE() AS odoogiin_san;

USE delguur;
DROP DATABASE IF EXISTS tur_dadlaga;

-- 2. delguur дотор түр хүснэгт үүсгэх
DROP TABLE IF EXISTS tur_hereglegch;

CREATE TABLE tur_hereglegch (
    hereglegch_id INT AUTO_INCREMENT PRIMARY KEY,
    ovog          VARCHAR(50)  NOT NULL,
    ner           VARCHAR(50)  NOT NULL,
    email         VARCHAR(100) NOT NULL UNIQUE,
    idevhtei      BOOLEAN      NOT NULL DEFAULT TRUE,
    burtgesen     DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- 3. Мөр нэмж шалгах (id, idevhtei, burtgesen автоматаар)
--    INSERT нь шинэ мөр нэмнэ — Модул 7-д нарийн үзнэ
INSERT INTO tur_hereglegch (ovog, ner, email)
VALUES ('Батын', 'Болд', 'bold@example.mn'),
       ('Доржийн', 'Сараа', 'saraa@example.mn');

SELECT * FROM tur_hereglegch;

-- 4. Бүтцийг харах
SHOW TABLES LIKE 'tur%';
DESCRIBE tur_hereglegch;
SHOW CREATE TABLE tur_hereglegch;

-- 5. Байгаа бол алдаа биш, сануулга
CREATE TABLE IF NOT EXISTS tur_hereglegch (id INT);
SHOW WARNINGS;

-- 6. SELECT-ийн үр дүнгээр хүснэгт үүсгэх
DROP TABLE IF EXISTS tur_elektronik;

CREATE TABLE tur_elektronik AS
SELECT baraa_id, ner, une
FROM baraa
WHERE angilal_id = 1;

SELECT * FROM tur_elektronik;
DESCRIBE tur_elektronik;   -- Key баганад PRI байхгүйг анзаар

-- 7. Цэвэрлэх
DROP TABLE IF EXISTS tur_elektronik, tur_hereglegch;
""",
        ),
        LessonSpec(
            title="ALTER TABLE ба DROP",
            slug="alter-table-ba-drop-table",
            description="Багана нэмэх, өөрчлөх, нэр солих, устгах.",
            duration=600,
            language=MY,
            content="""\
Хүснэгт үүссэний дараа шаардлага өөрчлөгддөг. `ALTER TABLE` нь өгөгдлийг
алдалгүй бүтцийг өөрчилнө.

### Тушаалууд

| Үйлдэл | MySQL |
|---|---|
| Багана нэмэх | `ADD COLUMN c INT` |
| Байрлал заах | `AFTER x`, `FIRST` |
| Төрөл өөрчлөх | `MODIFY COLUMN c …` |
| Нэр солих | `RENAME COLUMN a TO b` (8.0+) |
| Нэр + төрөл | `CHANGE COLUMN a b …` |
| Багана устгах | `DROP COLUMN c` |
| Хүснэгтийн нэр | `RENAME TABLE a TO b` |
| Бүтэц харах | `DESCRIBE t`, `SHOW CREATE TABLE t` |

### Багана нэмэх

```sql
ALTER TABLE tur_hamtragch ADD COLUMN email VARCHAR(100) NULL AFTER ner;
```

`AFTER ner` нь баганыг `ner`-ийн ард байрлуулна, `FIRST` — хамгийн эхэнд.
Бичээгүй бол төгсгөлд нэмэгдэнэ.

Мөртэй хүснэгтэд `NOT NULL` багана нэмэхэд `DEFAULT` өгсөн бол байгаа
мөрүүдэд тэр утга бөглөгдөнө. `DEFAULT` өгөөгүй бол MySQL далд анхдагч
утга (тоонд `0`, текстэд `''`) бөглөнө — санамсаргүй утга орохоос
сэргийлж `DEFAULT`-ийг үргэлж илт бич.

Нэг `ALTER TABLE` дотор хэд хэдэн өөрчлөлтийг таслалаар бичиж болно.

### Төрөл өөрчлөх — нуугдмал хавх

```sql
-- MODIFY нь баганыг БҮТНЭЭР нь дахин тодорхойлно
ALTER TABLE tur_hamtragch MODIFY COLUMN ner VARCHAR(100) NOT NULL;
```

> `MODIFY`-д `NOT NULL`, `DEFAULT`-ийг дахин бичихгүй бол **алга
> болно**. `MODIFY COLUMN uldegdel INT;` гэвэл `NOT NULL DEFAULT 0`
> устаж, багана `NULL` зөвшөөрдөг болно.

Урт текстийг богиносгох, тоог жижиг төрөл болгоход байгаа өгөгдөл
багтахгүй бол strict горим алдаа өгнө.

### Нэр солих

```sql
ALTER TABLE tur_hamtragch RENAME COLUMN utas TO utasnii_dugaar;
RENAME TABLE tur_hamtragch TO tur_niiluulegch;
```

`CHANGE COLUMN хуучин шинэ төрөл` нь нэр ба төрлийг зэрэг солино — гэхдээ
`MODIFY`-тэй адил баганыг бүтнээр нь дахин тодорхойлно.

View, procedure доторх хуучин нэр **автоматаар солигдохгүй** — нэр солихоос
өмнө түүнийг хаана ашигладгийг шалга.

### Багана устгах

```sql
ALTER TABLE tur_hamtragch DROP COLUMN idevhtei;
```

Баганатай хамт түүн дээрх индекс, `CHECK` хязгаарлалт устана. Гадаад
түлхүүрт оролцож буй баганыг эхлээд түлхүүрийг нь устгаж байж устгана
(Модул 8).

### DROP TABLE

```sql
DROP TABLE IF EXISTS tur_niiluulegch;
```

`IF EXISTS` — хүснэгт байхгүй бол алдааны оронд сануулга (note) өгнө.
Скриптийг дахин ажиллуулах боломжтой болгодог.

> `DROP TABLE` нь бүтэц, өгөгдөл, индекс, trigger бүгдийг устгана.
> MySQL-д DDL нь transaction-ийг автоматаар commit хийдэг тул **буцаах
> боломжгүй**. Нөөц хуулбаргүйгээр жинхэнэ хүснэгтийг бүү устга.

### information_schema

Хүснэгтийн бүтцийг SQL асуулгаар унших стандарт арга:

```sql
SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = 'delguur' AND TABLE_NAME = 'baraa'
ORDER BY ORDINAL_POSITION;
```

MySQL-д `TABLE_SCHEMA` нь сангийн нэр. `DESCRIBE`-ээс ялгаатай нь үр
дүнг шүүж, эрэмбэлж, бусад асуулгад ашиглаж болно.
""",
            initial_code="""\
USE delguur;

-- 1. Түр хүснэгт бэлдэх
DROP TABLE IF EXISTS tur_niiluulegch;
DROP TABLE IF EXISTS tur_hamtragch;

CREATE TABLE tur_hamtragch (
    hamtragch_id INT AUTO_INCREMENT PRIMARY KEY,
    ner          VARCHAR(50) NOT NULL,
    utas         VARCHAR(20) NULL
);

-- Туршилтын мөрүүд (INSERT-ийг Модул 7-д нарийн үзнэ)
INSERT INTO tur_hamtragch (ner, utas)
VALUES ('Номин ХХК', '77001122'),
       ('Говь ХК', NULL);

-- 2. Багана нэмэх: байрлал заах боломжтой
ALTER TABLE tur_hamtragch ADD COLUMN email VARCHAR(100) NULL AFTER ner;

-- NOT NULL + DEFAULT: байгаа мөрүүдэд TRUE бөглөнө
ALTER TABLE tur_hamtragch ADD COLUMN idevhtei BOOLEAN NOT NULL DEFAULT TRUE;

-- Нэг тушаалаар хэд хэдэн өөрчлөлт
ALTER TABLE tur_hamtragch
    ADD COLUMN hot VARCHAR(50) NULL,
    ADD COLUMN geree_ognoo DATE NULL;

SELECT * FROM tur_hamtragch;

-- 3. Төрөл өөрчлөх: NOT NULL-ыг заавал дахин бичнэ
ALTER TABLE tur_hamtragch MODIFY COLUMN ner VARCHAR(100) NOT NULL;
DESCRIBE tur_hamtragch;

-- 4. Нэр солих (MySQL 8.0+)
ALTER TABLE tur_hamtragch RENAME COLUMN utas TO utasnii_dugaar;

-- CHANGE: нэр ба төрлийг зэрэг солино
ALTER TABLE tur_hamtragch CHANGE COLUMN utasnii_dugaar utas VARCHAR(30) NULL;

-- 5. Багана устгах
ALTER TABLE tur_hamtragch DROP COLUMN idevhtei;

-- 6. Хүснэгтийн нэр солих
RENAME TABLE tur_hamtragch TO tur_niiluulegch;

-- 7. Эцсийн бүтцийг хоёр аргаар харах
DESCRIBE tur_niiluulegch;

SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, IS_NULLABLE, COLUMN_DEFAULT
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = 'delguur'
  AND TABLE_NAME = 'tur_niiluulegch'
ORDER BY ORDINAL_POSITION;

SELECT * FROM tur_niiluulegch;

-- 8. Устгах
DROP TABLE IF EXISTS tur_niiluulegch;
SHOW TABLES LIKE 'tur%';
""",
        ),
    ],
)

MODIFYING_DATA = ModuleSpec(
    title="Модул 7 — Өгөгдөл өөрчлөх",
    description="INSERT, UPDATE, DELETE ба TRUNCATE-ийг аюулгүй ашиглах.",
    lessons=[
        LessonSpec(
            title="INSERT — мөр нэмэх",
            slug="insert-ba-last-insert-id",
            description="Нэг ба олон мөр, INSERT…SELECT, шинэ id-г авах.",
            duration=540,
            language=MY,
            content="""\
### Нэг мөр

```sql
INSERT INTO tur_baraa (ner, angilal_id, une, uldegdel)
VALUES ('Ухаалаг цаг', 1, 690000.00, 8);
```

Баганын жагсаалтыг **үргэлж** бич. Жагсаалтгүй хэлбэр ажилладаг ч:

```sql
INSERT INTO tur_baraa VALUES (NULL, 'Ухаалаг цаг', 1, 690000.00, 8, '2024-06-01');
```

- Бүх баганын утгыг **яг дарааллаар** нь өгөх ёстой.
- Хэн нэгэн багана нэмбэл энэ тушаал эвдэрнэ.

### Олон мөр нэг дор

```sql
INSERT INTO tur_baraa (ner, angilal_id, une)
VALUES ('Ширээний чийдэн', 4, 75000.00),
       ('Ногоон цай',      5,  9000.00),
       ('Шатар',           4, 42000.00);
```

Нэг тушаал нь гурван тусдаа `INSERT`-ээс хамаагүй хурдан.

### Анхдагч утга

Жагсаалтаас орхигдсон багана `DEFAULT` утгаа авна. Утгын байранд
`DEFAULT` гэж шууд бичиж ч болно:

```sql
INSERT INTO tur_baraa (ner, angilal_id, une, uldegdel)
VALUES ('Аяга', 4, 18000.00, DEFAULT);
```

`DEFAULT`-гүй `NOT NULL` баганыг орхивол MySQL-ийн strict mode (8.0-ийн
анхдагч) алдаа өгнө: `ERROR 1364: Field 'ner' doesn't have a default value`.

### INSERT … SELECT

Өөр хүснэгтээс сонгосон мөрүүдийг оруулна. `VALUES` бичихгүй:

```sql
INSERT INTO tur_baraa (ner, angilal_id, une, uldegdel)
SELECT ner, angilal_id, une, uldegdel
FROM baraa
WHERE angilal_id = 3;
```

Баганын **тоо, дараалал, төрөл** таарах ёстой — нэр нь таарах
шаардлагагүй.

### Шинэ id-г авах

```sql
INSERT INTO tur_baraa (ner, angilal_id, une) VALUES ('Хөтөч', 1, 30000.00);
SELECT LAST_INSERT_ID();
```

`LAST_INSERT_ID()`-ийн дүрэм:

- **Холболт бүрт тусдаа** — өөр хүн зэрэг мөр нэмсэн ч таны id зөв.
- Олон мөрийн `INSERT`-ийн дараа **эхний** мөрийн id-г буцаана.
- `AUTO_INCREMENT` баганад утгыг гараар өгвөл өөрчлөгдөхгүй.

`SELECT MAX(baraa_id)` гэж **бүү** ав — өөр холболт тэр хооронд мөр
нэмсэн байж болно.

### Хэдэн мөр нэмэгдсэн бэ

`ROW_COUNT()` нь сүүлийн `INSERT`, `UPDATE`, `DELETE` хэдэн мөрт
нөлөөлснийг өгнө. `INSERT … SELECT`-ийн дараа хэдэн мөр хуулагдсаныг
шалгахад тохиромжтой.

> Хүснэгтийг өгөгдөлтэй нь хуулах бол Модул 6-ийн
> `CREATE TABLE … AS SELECT`. MySQL-д `SELECT … INTO` нь хүснэгт
> үүсгэдэггүй — утгыг хувьсагч руу бичдэг (Модул 16).

### Түгээмэл алдаа

| Код | Шалтгаан |
|---|---|
| 1062 `Duplicate entry` | `PRIMARY KEY` / `UNIQUE` давхардсан |
| 1048 `Column cannot be null` | `NOT NULL` баганад `NULL` |
| 1364 `doesn't have a default value` | `NOT NULL` баганыг орхисон |
| 1406 `Data too long` | Текст баганын уртаас хэтэрсэн |
| 1452 `foreign key constraint fails` | Байхгүй эцэг мөрийг заасан |
""",
            initial_code="""\
USE delguur;

-- 0. baraa-тай ижил бүтэцтэй түр хүснэгт
DROP TABLE IF EXISTS tur_baraa;

CREATE TABLE tur_baraa (
    baraa_id     INT AUTO_INCREMENT PRIMARY KEY,
    ner          VARCHAR(100) NOT NULL,
    angilal_id   INT NOT NULL,
    une          DECIMAL(12,2) NOT NULL,
    uldegdel     INT NOT NULL DEFAULT 0,
    nemsen_ognoo DATE NOT NULL DEFAULT (CURRENT_DATE)   -- MySQL 8.0.13+
);

-- 1. Нэг мөр, баганын жагсаалттай
INSERT INTO tur_baraa (ner, angilal_id, une, uldegdel)
VALUES ('Ухаалаг цаг', 1, 690000.00, 8);

SELECT LAST_INSERT_ID() AS shine_id;   -- 1

-- 2. Олон мөр: uldegdel, nemsen_ognoo анхдагч утгаа авна
INSERT INTO tur_baraa (ner, angilal_id, une)
VALUES ('Ширээний чийдэн', 4, 75000.00),
       ('Ногоон цай',      5,  9000.00),
       ('Шатар',           4, 42000.00);

-- Олон мөрийн дараа ЭХНИЙ мөрийн id
SELECT LAST_INSERT_ID() AS ehnii_id;   -- 2

-- 3. DEFAULT түлхүүр үг
INSERT INTO tur_baraa (ner, angilal_id, une, uldegdel, nemsen_ognoo)
VALUES ('Цайны аяга', 4, 18000.00, DEFAULT, DEFAULT);

-- 4. INSERT ... SELECT: жинхэнэ baraa-аас номнуудыг хуулах
INSERT INTO tur_baraa (ner, angilal_id, une, uldegdel, nemsen_ognoo)
SELECT ner, angilal_id, une, uldegdel, nemsen_ognoo
FROM baraa
WHERE angilal_id = 3;

SELECT ROW_COUNT() AS nemegdsen_mur;   -- 2

-- 5. id-г гараар өгч болно, дараагийнх нь түүнээс үргэлжилнэ
INSERT INTO tur_baraa (baraa_id, ner, angilal_id, une)
VALUES (100, 'Гараар id өгсөн', 5, 1000.00);

INSERT INTO tur_baraa (ner, angilal_id, une)
VALUES ('Дараагийн мөр', 5, 2000.00);

SELECT * FROM tur_baraa ORDER BY baraa_id;   -- сүүлийнх нь 101

-- 6. Алдааг харах бол тайлбарыг арилгаж тусад нь ажиллуул:
-- INSERT INTO tur_baraa (angilal_id, une) VALUES (1, 5000.00);
-- ERROR 1364: ner баганад анхдагч утга байхгүй

-- 7. Цэвэрлэх
DROP TABLE IF EXISTS tur_baraa;
""",
        ),
        LessonSpec(
            title="UPDATE — өгөгдөл засах",
            slug="update-ba-join-update",
            description="WHERE-тэй аюулгүй UPDATE, ROLLBACK-аар хамгаалах, safe update mode.",
            duration=600,
            language=MY,
            content="""\
```sql
UPDATE baraa
SET une = 52000.00
WHERE baraa_id = 7;
```

### WHERE-гүй UPDATE — хамгийн аюултай алдаа

```sql
UPDATE baraa SET une = 0;   -- БҮХ бараа үнэгүй боллоо
```

`WHERE` мартвал **бүх мөр** өөрчлөгдөнө. Сануулга, асуулт байхгүй.

Аюулгүй дадал:

1. Эхлээд ижил `WHERE`-тэй **`SELECT`** бичиж, аль мөрүүд өөрчлөгдөхийг хар.
2. `SELECT … FROM` хэсгийг `UPDATE … SET` болгож соль, `WHERE`-г хэвээр үлдээ.
3. Чухал өгөгдөл дээр **transaction** дотор ажиллуулж, шалгаад
   `COMMIT` эсвэл `ROLLBACK`.

```sql
SELECT baraa_id, ner, une FROM baraa WHERE angilal_id = 3;   -- 1. шалгах

START TRANSACTION;                                           -- 2. хамгаалах
UPDATE baraa SET une = une * 1.1 WHERE angilal_id = 3;
SELECT baraa_id, ner, une FROM baraa WHERE angilal_id = 3;   -- 3. үр дүн
ROLLBACK;                                                    -- эсвэл COMMIT
```

- `START TRANSACTION` — «одооноос хийх өөрчлөлтийг хараахан бүү
  баталгаажуул» гэсэн тэмдэг.
- `ROLLBACK` — түүнээс хойш хийсэн **бүх** өөрчлөлтийг буцаана.
- `COMMIT` — өөрчлөлтийг баталгаажуулж, үүрд хадгална.

Энэ сургалтын жишээнүүд `delguur`-ийн өгөгдлийг эвдэхгүйн тулд ингэж
төгсгөлд нь `ROLLBACK` хийнэ. (Энэ сайт дээр ажиллуулалт бүр анхны
сангаас эхэлдэг ч жинхэнэ сервер дээр ийм хамгаалалт байхгүй — дадлаа
одооноос суулга.) Transaction-ийг Модул 14-т нарийн үзнэ.

### MySQL Workbench-ийн safe update mode

Workbench анхдагчаар `SQL_SAFE_UPDATES = 1` тохиргоотой. Энэ үед
`WHERE`-д **түлхүүр (индекстэй) багана** ашиглаагүй бөгөөд `LIMIT`-гүй
`UPDATE`/`DELETE` татгалзагдана:

```text
Error Code: 1175. You are using safe update mode and you tried to update
a table without a WHERE that uses a KEY column.
```

Энэ бол **хамгаалалт**, алдаа биш. Унтраах арга:

```sql
SET SQL_SAFE_UPDATES = 0;   -- зөвхөн энэ session-д
```

эсвэл Edit → Preferences → SQL Editor → «Safe Updates». Унтраах бүрдээ
`WHERE`-ээ хоёр дахин шалга. `mysql` CLI-д анхдагчаар унтраалттай
(`--safe-updates` гэж асаана).

### Олон багана, тооцоолол

```sql
UPDATE hereglegch
SET hot  = 'Улаанбаатар',
    utas = '99001122'
WHERE hereglegch_id = 6;

UPDATE baraa SET uldegdel = uldegdel + 20 WHERE baraa_id = 5;
```

> **Нарийн зүйл:** `SET a = a + 1, b = a` гэвэл MySQL-ийн нэг хүснэгтийн
> `UPDATE` зүүнээс баруун тийш үнэлж `b`-д **шинэ** `a`-г өгнө. SQL
> стандарт болон бусад ихэнх DBMS бүх илэрхийллийг **хуучин** утгаар
> үнэлдэг — MySQL-ийн онцлог.

### Өөр хүснэгтийн утгаар засах

Захиалга 9 хүргэгдлээ — түүний мөрүүдээр барааны үлдэгдлийг хасъя. Эхлээд
захиалгын мөрүүдийг харна:

```sql
SELECT baraa_id, too FROM zahialgiin_mur WHERE zahialga_id = 9;
```

| baraa_id | too |
|---|---|
| 7 | 3 |
| 10 | 5 |

Дараа нь бараа бүрийг тус тусад нь засна:

```sql
UPDATE baraa SET uldegdel = uldegdel - 3 WHERE baraa_id = 7;    -- SQL сурах бичиг: 12 → 9
UPDATE baraa SET uldegdel = uldegdel - 5 WHERE baraa_id = 10;   -- Ааруул: 200 → 195
```

Мөр цөөн үед ингэж болно. Олон мөртэй бол хоёр хүснэгтийг нэг `UPDATE`
дотор холбож засдаг — **JOIN-той UPDATE**. Хүснэгт холбох `JOIN`-ийг
Модул 9-д үзэхдээ энэ жишээг нэг тушаалаар бичнэ.

### Хэрэгтэй нэмэлтүүд

| Зорилго | MySQL |
|---|---|
| Хэдэн мөр өөрчлөгдсөн | `SELECT ROW_COUNT();` |
| Зөвхөн эхний N мөрийг засах | `UPDATE … ORDER BY … LIMIT n` |

`ROW_COUNT()` нь утга нь **өөрчлөгдсөн** мөрийг тоолно: `une`-г ижил
утгаар нь «засвал» 0 гэж гарна.
""",
            initial_code="""\
USE delguur;

-- Бүх өөрчлөлт transaction дотор, төгсгөлд нь ROLLBACK
-- WHERE нь PRIMARY KEY ашигладаг тул Workbench safe mode-д ч ажиллана

-- 1. Эхлээд SELECT-ээр шалгах
SELECT baraa_id, ner, une
FROM baraa
WHERE baraa_id IN (6, 7);

START TRANSACTION;

-- 2. Нэг баганыг засах
UPDATE baraa
SET une = 52000.00
WHERE baraa_id = 7;

-- 3. Тооцоолол: 10 хувийн хөнгөлөлт
UPDATE baraa
SET une = une * 0.9
WHERE baraa_id IN (6, 7);

SELECT ROW_COUNT() AS uurchlugdsun;   -- 2

SELECT baraa_id, ner, une
FROM baraa
WHERE baraa_id IN (6, 7);             -- 31500.00, 46800.00

-- 4. Олон багана зэрэг
UPDATE hereglegch
SET hot  = 'Улаанбаатар',
    utas = '99001122'
WHERE hereglegch_id = 6;

SELECT hereglegch_id, ner, hot, utas FROM hereglegch WHERE hereglegch_id = 6;

-- 5. Захиалга 9-ийн мөрүүдээр үлдэгдэл хасах
--    Эхлээд захиалгын мөрүүдийг харна: 7-р бараа 3, 10-р бараа 5 ширхэг
SELECT baraa_id, too
FROM zahialgiin_mur
WHERE zahialga_id = 9;

UPDATE baraa SET uldegdel = uldegdel - 3 WHERE baraa_id = 7;
UPDATE baraa SET uldegdel = uldegdel - 5 WHERE baraa_id = 10;

UPDATE zahialga
SET tuluv = 'Хүргэгдсэн'
WHERE zahialga_id = 9;

SELECT baraa_id, ner, uldegdel FROM baraa WHERE baraa_id IN (7, 10);   -- 9, 195
SELECT zahialga_id, tuluv FROM zahialga WHERE zahialga_id = 9;

-- 6. Бүгдийг буцаах
ROLLBACK;

-- 7. Анхны утгууд эргэж ирсэн эсэх
SELECT baraa_id, ner, une, uldegdel FROM baraa WHERE baraa_id IN (6, 7, 10);
SELECT zahialga_id, tuluv FROM zahialga WHERE zahialga_id = 9;

-- АЮУЛТАЙ: WHERE-гүй UPDATE бүх мөрийг өөрчилнө. Бүү ажиллуул:
-- UPDATE baraa SET une = 0;
""",
        ),
        LessonSpec(
            title="DELETE, TRUNCATE ба DROP",
            slug="delete-truncate-drop",
            description="Мөр устгах гурван арга: ROLLBACK, AUTO_INCREMENT, FOREIGN KEY.",
            duration=600,
            language=MY,
            content="""\
Гурвуулаа «устгадаг» ч огт өөр түвшинд ажилладаг.

```sql
DELETE FROM tur_log WHERE log_id = 2;   -- сонгосон мөрүүд
DELETE FROM tur_log;                    -- бүх мөр, нэг нэгээр
TRUNCATE TABLE tur_log;                 -- бүх мөр, нэг дор
DROP TABLE tur_log;                     -- хүснэгт бүтнээрээ
```

### Харьцуулалт

| | `DELETE` | `TRUNCATE TABLE` | `DROP TABLE` |
|---|---|---|---|
| Юу устгах | Мөрүүд | Бүх мөр | Бүтэц + өгөгдөл |
| `WHERE` | Тийм | Үгүй | Үгүй |
| Ангилал (Модул 0) | DML | DDL | DDL |
| Хурд (сая мөр) | Удаан — мөр бүрийг | Маш хурдан | Маш хурдан |
| `DELETE` trigger | Ажиллана | Ажиллахгүй | Ажиллахгүй |
| `AUTO_INCREMENT` | Үргэлжилнэ | **1-ээс эхэлнэ** | — |
| FK-ээр заагдсан хүснэгт | Хүүхэд мөргүй бол OK | **Алдаа** | **Алдаа** |
| `ROLLBACK`-оор буцаах | Тийм | **Үгүй** | **Үгүй** |

`TRUNCATE` мөрүүдийг нэг нэгээр устгадаггүй — хүснэгтийг хоосноор нь
дахин үүсгэдэг. Тиймээс хурдан ч trigger ажиллахгүй, тоолуур эхэлнэ.

### TRUNCATE, DROP-ийг буцаах боломжгүй

MySQL-д DDL (`CREATE`, `ALTER`, `DROP`) болон `TRUNCATE` нь **далд commit**
хийдэг:

```sql
START TRANSACTION;
TRUNCATE TABLE tur_log;   -- өмнөх ажлыг ч commit хийгээд хүснэгтийг цэвэрлэнэ
ROLLBACK;                 -- юу ч буцаахгүй
```

Transaction дотор байсан ч `TRUNCATE`, `DROP`-ийг буцааж **чадахгүй**.
Түүнээс өмнө хийсэн, хараахан commit хийгээгүй өөрчлөлт ч зэрэг
баталгаажчихна. Ажиллуулахаасаа өмнө нөөц хуулбар бэлд (Модул 18).

### AUTO_INCREMENT дугаар

`DELETE` нь тоолуурыг хөндөхгүй: 1, 2, 3-ыг устгаад шинэ мөр нэмбэл 4.
`TRUNCATE` нь 1 рүү буцаана.

```sql
ALTER TABLE tur_log AUTO_INCREMENT = 100;   -- дараагийн мөр 100 дугаартай
```

> Тоолуурыг одоо байгаа хамгийн их id-ээс бага болгож чадахгүй — `MAX + 1`
> болж тохируулагдана. Устгасан id дахин ашиглагддаггүй тул дугаарт
> «цоорхой» гарах нь хэвийн.

### FOREIGN KEY-ийн хязгаар

Өөр хүснэгтийн FK заадаг хүснэгтийг (жишээ нь `angilal`):

- `TRUNCATE` хийж **болохгүй** — хүүхэд хүснэгт хоосон байсан ч:
  `ERROR 1701 Cannot truncate a table referenced in a foreign key constraint`.
- `DROP` хийж болохгүй — эхлээд хүүхэд хүснэгт эсвэл FK-г устгана:
  `ERROR 3730`.
- `DELETE` хийж болно — гэхдээ заагдсан мөрийг устгавал FK алдаа
  (Модул 8).

### WHERE-гүй DELETE

```sql
DELETE FROM tur_log;   -- бүх мөр!
```

`UPDATE`-ийн адил эхлээд `SELECT`, дараа нь transaction. MySQL Workbench-ийн
safe update mode нь түлхүүр баганагүй `DELETE`-ийг хаадаг.

MySQL-д `DELETE … ORDER BY uussen LIMIT 1000` гэж **хэсэгчлэн** устгаж
болно — том хүснэгтийг багцаар цэвэрлэхэд серверийг удаан түгжихгүй.

### Хэзээ алийг нь

| Нөхцөл | Сонголт |
|---|---|
| Зарим мөрийг устгах | `DELETE … WHERE` |
| Түр/ачааллын хүснэгтийг бүрэн хоослох | `TRUNCATE TABLE` |
| Хүснэгт хэрэггүй болсон | `DROP TABLE` |
| Устгасан түүхийг хадгалах | Устгахгүй — `idevhtei = 0` багана («soft delete») |

> Бодит системд хэрэглэгч, захиалгыг ихэвчлэн **устгадаггүй**: тайлан,
> санхүүгийн түүх эвдэрнэ. `idevhtei` эсвэл `ustgasan_ognoo` багана
> нэмж шүүдэг.
""",
            initial_code="""\
USE delguur;

-- 0. Түр хүснэгтүүд (хүүхдийг эхэлж устгана)
DROP TABLE IF EXISTS tur_log_delgerengui;
DROP TABLE IF EXISTS tur_log;

CREATE TABLE tur_log (
    log_id        INT AUTO_INCREMENT PRIMARY KEY,
    uil_ajillagaa VARCHAR(100) NOT NULL,
    uussen        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO tur_log (uil_ajillagaa)
VALUES ('Нэвтэрсэн'), ('Захиалга үүсгэсэн'), ('Гарсан');

SELECT * FROM tur_log;

-- 1. DELETE ... WHERE: сонгосон мөр
DELETE FROM tur_log WHERE log_id = 2;
SELECT ROW_COUNT() AS ustgasan;                    -- 1

-- 2. WHERE-гүй DELETE-ийг transaction дотор туршиж буцаах
START TRANSACTION;
DELETE FROM tur_log;
SELECT COUNT(*) AS tran_dotor FROM tur_log;        -- 0
ROLLBACK;
SELECT COUNT(*) AS rollback_daraa FROM tur_log;    -- 2

-- 3. DELETE нь AUTO_INCREMENT-ийг эхлүүлэхгүй
DELETE FROM tur_log;
INSERT INTO tur_log (uil_ajillagaa) VALUES ('DELETE-ийн дараа');
SELECT LAST_INSERT_ID() AS shine_id;               -- 4

-- 4. TRUNCATE нь AUTO_INCREMENT-ийг 1 рүү буцаана
TRUNCATE TABLE tur_log;
INSERT INTO tur_log (uil_ajillagaa) VALUES ('TRUNCATE-ийн дараа');
SELECT LAST_INSERT_ID() AS shine_id;               -- 1

-- 5. TRUNCATE-ийг ROLLBACK буцаахгүй: далд COMMIT
START TRANSACTION;
TRUNCATE TABLE tur_log;
ROLLBACK;
SELECT COUNT(*) AS rollback_daraa FROM tur_log;    -- 0 — буцаагүй!

-- 6. FOREIGN KEY-ээр заагдсан хүснэгт: log_id нь tur_log руу заана
--    (FOREIGN KEY-ийн бичиглэлийг дараагийн модульд үзнэ)
INSERT INTO tur_log (uil_ajillagaa) VALUES ('Шинэ мөр');

CREATE TABLE tur_log_delgerengui (
    delgerengui_id INT AUTO_INCREMENT PRIMARY KEY,
    log_id         INT NOT NULL,
    tailbar        VARCHAR(200) NULL,
    CONSTRAINT fk_tur_log_delgerengui_log
        FOREIGN KEY (log_id) REFERENCES tur_log (log_id)
);

-- Хүүхэд хүснэгт хоосон ч TRUNCATE, DROP татгалзана.
-- Тайлбарыг НЭГ НЭГЭЭР арилгаж тусад нь ажиллуул:
-- TRUNCATE TABLE tur_log;   -- ERROR 1701
-- DROP TABLE tur_log;       -- ERROR 3730

-- DELETE болно: заагдсан мөр байхгүй
DELETE FROM tur_log;
SELECT COUNT(*) AS uldsen FROM tur_log;            -- 0

-- 7. Цэвэрлэх: эхлээд хүүхэд, дараа нь эцэг
DROP TABLE IF EXISTS tur_log_delgerengui;
DROP TABLE IF EXISTS tur_log;
""",
        ),
    ],
)

CONSTRAINTS = ModuleSpec(
    title="Модул 8 — Хязгаарлалт",
    description="NOT NULL, DEFAULT, UNIQUE, CHECK, PRIMARY KEY, FOREIGN KEY.",
    lessons=[
        LessonSpec(
            title="NOT NULL, DEFAULT, UNIQUE, CHECK",
            slug="not-null-default-unique-check",
            description="Буруу өгөгдлийг өгөгдлийн сан өөрөө хүлээж авахгүй болгох.",
            duration=600,
            language=MY,
            content="""\
Хязгаарлалт (constraint) нь **дүрмийг өгөгдлийн сан дотор** бичнэ. Аль ч
програм, аль ч хүн мөр нэмсэн дүрэм зөрчигдөхгүй — зөвхөн вэб апп-ын
шалгалтад найдахаас хамаагүй найдвартай.

### Дөрвөн үндсэн хязгаарлалт

| Хязгаарлалт | Утга | Жишээ |
|---|---|---|
| `NOT NULL` | Утга заавал байна | `ner VARCHAR(100) NOT NULL` |
| `DEFAULT` | Утга өгөөгүй үед | `uldegdel INT NOT NULL DEFAULT 0` |
| `UNIQUE` | Давхардахгүй | `email VARCHAR(100) UNIQUE` |
| `CHECK` | Нөхцөл үнэн байх | `CHECK (une >= 0)` |

### Нэртэй хязгаарлалт

```sql
CREATE TABLE tur_ajiltan (
    ajiltan_id INT AUTO_INCREMENT PRIMARY KEY,
    ner        VARCHAR(100)  NOT NULL,
    email      VARCHAR(100)  NOT NULL,
    tsalin     DECIMAL(12,2) NOT NULL DEFAULT 1000000.00,
    tuluv      VARCHAR(20)   NOT NULL DEFAULT 'Идэвхтэй',
    CONSTRAINT uq_tur_ajiltan_email  UNIQUE (email),
    CONSTRAINT ck_tur_ajiltan_tsalin CHECK (tsalin > 0),
    CONSTRAINT ck_tur_ajiltan_tuluv
        CHECK (tuluv IN ('Идэвхтэй', 'Чөлөөтэй', 'Гарсан'))
);
```

Нэр өгөөгүй бол сервер өөрөө нэр зохионо (жишээ нь `tur_ajiltan_chk_1`).
Алдааны мессежид нэр нь гардаг тул **ойлгомжтой нэр** өг: `ck_` CHECK,
`uq_` UNIQUE, `pk_` PRIMARY KEY, `fk_` FOREIGN KEY.

> MySQL-д CHECK-ийн нэр **сан дотор давтагдашгүй** байх ёстой.
> Хүснэгтийн нэрийг хязгаарлалтын нэрэнд оруулбал давхцахгүй.

### CHECK — MySQL-ийн хувилбарт анхаар

> MySQL **8.0.16-аас өмнө** `CHECK`-ийг уншаад **чимээгүй үл тоомсорлодог**
> байсан. Хуучин сервер дээр `CHECK (une >= 0)` бичсэн ч сөрөг үнэ орно.
> `SELECT VERSION();` гэж шалгаарай.

CHECK-ийн дүрмүүд:

- `NULL` нь CHECK-ийг **давна** — нөхцөл «үл мэдэгдэх» бол зөрчил биш.
  `CHECK (tsalin > 0)` байхад `tsalin = NULL` орно. Хэрэггүй бол `NOT NULL` нэм.
- Дэд асуулга (subquery, Модул 10) ашиглаж болохгүй.
- MySQL-д `CURRENT_DATE`, `NOW()` зэрэг тогтворгүй функц хориотой.

### UNIQUE ба NULL

MySQL-д `UNIQUE` баганад **олон `NULL`** зөвшөөрнө. `NULL` нь «үл
мэдэгдэх» утга тул хоёр `NULL` бие биетэйгээ тэнцүү биш гэж үзнэ (Модул
3). Утасгүй олон ажилтан байж болно, харин бөглөсөн утас давтагдахгүй —
яг хэрэгтэй дүрэм.

`UNIQUE` нь ард нь индекс үүсгэдэг — индексийг Модул 13-т нарийн үзнэ.

### DEFAULT

| Зорилго | Бичлэг |
|---|---|
| Тогтмол утга | `DEFAULT 0` |
| Одоогийн цаг | `DEFAULT CURRENT_TIMESTAMP` |
| Өнөөдрийн огноо | `DEFAULT (CURRENT_DATE)` (8.0.13+) |
| Дараа нь солих | `ALTER TABLE t ALTER COLUMN c SET DEFAULT 0` |

Функц, илэрхийллийг анхдагч утга болгоход **хаалтанд** бичнэ:
`DEFAULT (CURRENT_DATE)`. `CURRENT_TIMESTAMP` л хаалтгүй бичигдэх
онцгой тохиолдол.

### Байгаа хүснэгтэд нэмэх, хасах

```sql
ALTER TABLE tur_ajiltan ADD CONSTRAINT ck_tur_ajiltan_email CHECK (email LIKE '%@%');
```

| Хасах | Бичлэг |
|---|---|
| CHECK | `ALTER TABLE t DROP CHECK ck_x` |
| UNIQUE | `ALTER TABLE t DROP INDEX uq_x` |
| Аль ч төрөл | `ALTER TABLE t DROP CONSTRAINT x` (8.0.19+) |

Байгаа өгөгдөл шинэ дүрмийг зөрчиж байвал `ADD CONSTRAINT` алдаа өгнө.

### Алдааны мессежүүд

| Зөрчил | MySQL-ийн алдаа |
|---|---|
| `NOT NULL` | 1048 `Column 'ner' cannot be null` |
| `NOT NULL`, утга өгөөгүй | 1364 `Field 'ner' doesn't have a default value` |
| `UNIQUE` | 1062 `Duplicate entry` |
| `CHECK` | 3819 `Check constraint '…' is violated` |
""",
            initial_code="""\
USE delguur;

-- MySQL 8.0.16+ байх ёстой (түүнээс өмнө CHECK ажилладаггүй)
SELECT VERSION();

-- 1. Нэртэй хязгаарлалттай хүснэгт
DROP TABLE IF EXISTS tur_ajiltan;

CREATE TABLE tur_ajiltan (
    ajiltan_id  INT AUTO_INCREMENT PRIMARY KEY,
    ner         VARCHAR(100)  NOT NULL,
    email       VARCHAR(100)  NOT NULL,
    utas        VARCHAR(20)   NULL,
    tsalin      DECIMAL(12,2) NOT NULL DEFAULT 1000000.00,
    ajild_orson DATE          NOT NULL DEFAULT (CURRENT_DATE),
    tuluv       VARCHAR(20)   NOT NULL DEFAULT 'Идэвхтэй',
    CONSTRAINT uq_tur_ajiltan_email  UNIQUE (email),
    CONSTRAINT uq_tur_ajiltan_utas   UNIQUE (utas),
    CONSTRAINT ck_tur_ajiltan_tsalin CHECK (tsalin > 0),
    CONSTRAINT ck_tur_ajiltan_tuluv
        CHECK (tuluv IN ('Идэвхтэй', 'Чөлөөтэй', 'Гарсан'))
);

-- 2. Зөв мөрүүд: DEFAULT утгууд бөглөгдөнө
INSERT INTO tur_ajiltan (ner, email)
VALUES ('Солонго', 'solongo@example.mn');

INSERT INTO tur_ajiltan (ner, email, utas, tsalin)
VALUES ('Тэмүүжин', 'temuujin@example.mn', NULL, 2300000.00);

-- UNIQUE баганад олон NULL болно
INSERT INTO tur_ajiltan (ner, email, utas, tuluv)
VALUES ('Цэцэг', 'tsetseg@example.mn', NULL, 'Чөлөөтэй');

SELECT * FROM tur_ajiltan;

-- 3. Зөрчлүүд. Тайлбарыг НЭГ НЭГЭЭР арилгаж тусад нь ажиллуул:

-- NOT NULL -> ERROR 1048
-- INSERT INTO tur_ajiltan (ner, email) VALUES (NULL, 'hooson@example.mn');

-- UNIQUE -> ERROR 1062
-- INSERT INTO tur_ajiltan (ner, email) VALUES ('Давхар', 'solongo@example.mn');

-- CHECK tsalin > 0 -> ERROR 3819
-- INSERT INTO tur_ajiltan (ner, email, tsalin) VALUES ('Сөрөг', 'sorog@example.mn', -5);

-- CHECK tuluv IN (...) -> ERROR 3819
-- INSERT INTO tur_ajiltan (ner, email, tuluv) VALUES ('Буруу', 'buruu@example.mn', 'Амралт');

-- DEFAULT-гүй NOT NULL баганыг орхисон -> ERROR 1364
-- INSERT INTO tur_ajiltan (email) VALUES ('nergui@example.mn');

-- 4. NULL нь CHECK-ийг давдаг: урамшууллын баганад NULL орно
ALTER TABLE tur_ajiltan ADD COLUMN uramshuulal DECIMAL(12,2) NULL;
ALTER TABLE tur_ajiltan
    ADD CONSTRAINT ck_tur_ajiltan_uramshuulal CHECK (uramshuulal >= 0);

UPDATE tur_ajiltan SET uramshuulal = NULL WHERE ajiltan_id = 1;   -- алдаа биш
SELECT ajiltan_id, ner, uramshuulal FROM tur_ajiltan;

-- 5. Байгаа хүснэгтэд хязгаарлалт нэмэх
ALTER TABLE tur_ajiltan
    ADD CONSTRAINT ck_tur_ajiltan_email CHECK (email LIKE '%@%');

-- 6. Хязгаарлалтуудыг харах
SELECT CONSTRAINT_NAME, CONSTRAINT_TYPE
FROM information_schema.TABLE_CONSTRAINTS
WHERE TABLE_SCHEMA = 'delguur' AND TABLE_NAME = 'tur_ajiltan';

SELECT CONSTRAINT_NAME, CHECK_CLAUSE
FROM information_schema.CHECK_CONSTRAINTS
WHERE CONSTRAINT_SCHEMA = 'delguur' AND CONSTRAINT_NAME LIKE 'ck_tur_ajiltan%';

-- 7. Хасах, DEFAULT солих
ALTER TABLE tur_ajiltan DROP CHECK ck_tur_ajiltan_email;
ALTER TABLE tur_ajiltan ALTER COLUMN tuluv SET DEFAULT 'Чөлөөтэй';
SHOW CREATE TABLE tur_ajiltan;

-- 8. Цэвэрлэх
DROP TABLE IF EXISTS tur_ajiltan;
""",
        ),
        LessonSpec(
            title="PRIMARY KEY ба AUTO_INCREMENT",
            slug="primary-key-auto-increment-identity",
            description="Үндсэн түлхүүр, автомат дугаар, нийлмэл түлхүүр, суррогат түлхүүр.",
            duration=600,
            language=MY,
            content="""\
**PRIMARY KEY** нь мөр бүрийг давтагдашгүй тодорхойлно.

- Утга нь **давтагдахгүй** (`UNIQUE`)
- **`NULL` байж болохгүй** — автоматаар `NOT NULL`
- Хүснэгтэд **нэг л** PRIMARY KEY (нэг эсвэл хэд хэдэн баганаас)

### Бичих хоёр арга

```sql
-- Баганын дэргэд
baraa_id INT AUTO_INCREMENT PRIMARY KEY

-- Хүснэгтийн төгсгөлд
CONSTRAINT pk_tur_tasalbar PRIMARY KEY (tasalbar_id)
```

> MySQL-д PRIMARY KEY-ийн нэр **үргэлж `PRIMARY`** — `CONSTRAINT pk_…`
> гэж өгсөн нэрийг үл тоомсорлоно. `SHOW INDEX`-ээр харвал `PRIMARY`
> гэж гарна.

### AUTO_INCREMENT

```sql
CREATE TABLE tur_tasalbar (
    tasalbar_id INT AUTO_INCREMENT PRIMARY KEY,
    garchig     VARCHAR(100) NOT NULL
) AUTO_INCREMENT = 100;
```

| Асуулт | MySQL `AUTO_INCREMENT` |
|---|---|
| Эхлэл | Хүснэгтийн сонголт `AUTO_INCREMENT = 100` (анхдагч 1) |
| Алхам | Серверийн `auto_increment_increment` тохиргоо (анхдагч 1) — хүснэгт бүрт биш |
| Гараар утга өгөх | Шууд болно — тоолуур түүнээс үргэлжилнэ |
| `NULL` эсвэл `0` өгвөл | Дараагийн дугаар автоматаар үүснэ |
| Хүснэгтэд хэд | Нэг л, түлхүүр (индекс)-тэй байх ёстой |
| Сүүлийн утга | `LAST_INSERT_ID()` (Модул 7) |
| Одоогийн тоолуур | `SHOW CREATE TABLE`-ийн `AUTO_INCREMENT=…` |

### Цоорхой гарах нь хэвийн

- `ROLLBACK` хийсэн `INSERT` дугаараа **буцааж өгөхгүй**.
- Алдаагаар бүтэлгүйтсэн `INSERT` ч дугаар «идэнэ».
- Устгасан мөрийн дугаар дахин ашиглагдахгүй.

Тиймээс id-г **дараалсан тоо** гэж бүү найд — зөвхөн давтагдашгүй тэмдэг.
«Нэхэмжлэх №» гэх мэт цоорхойгүй дугаар хэрэгтэй бол тусад нь үүсгэнэ.

### Нийлмэл түлхүүр

`zahialgiin_mur` хүснэгтэд нэг захиалгад нэг бараа нэг л мөрөөр орно:

```sql
CONSTRAINT pk_zahialgiin_mur PRIMARY KEY (zahialga_id, baraa_id)
```

- `(1, 1)` ба `(1, 3)` — болно
- `(1, 3)` дахин — **зөрчил**
- Баганын дараалал чухал: индекс `zahialga_id`-аар эхэлж эрэмбэлэгдэнэ.

### Суррогат ба натурал түлхүүр

| | Суррогат | Натурал |
|---|---|---|
| Жишээ | `hereglegch_id` (1, 2, 3…) | `email`, регистрийн дугаар |
| Утга | Бизнесийн утгагүй | Бодит ертөнцийн утга |
| Өөрчлөгдөх үү | Хэзээ ч | Өөрчлөгдөж болно (email солих) |
| Хэмжээ | 4 байт | Урт текст |

Практикт: **суррогат түлхүүрийг PRIMARY KEY**, натурал түлхүүрийг
`UNIQUE` болго. `delguur` сан яг ийм: `hereglegch_id` PK, `email` UNIQUE.

> Өөр системтэй нэгтгэх, офлайн үүсгэх шаардлагатай бол UUID:
> `BINARY(16)` багана + `UUID_TO_BIN(UUID())`. Том, удаан тул шаардлагагүй
> бол `INT`.

### Кластерлагдсан индекс

MySQL-ийн InnoDB хүснэгт **үргэлж** PRIMARY KEY-ээрээ кластерлагдана:
мөрүүд дискэн дээр түлхүүрийн дарааллаар хадгалагдана (Модул 13). Иймээс
богино, өсөх дараалалтай `INT AUTO_INCREMENT` id нь хамгийн тохиромжтой —
шинэ мөр үргэлж төгсгөлд нэмэгдэнэ.

### Зөрчлийн мессеж

```text
ERROR 1062 (23000): Duplicate entry '1-3' for key 'tur_zahialgiin_mur.PRIMARY'
```

Нийлмэл түлхүүрийн утгууд `-`-ээр холбогдож харагдана: `'1-3'`.
""",
            initial_code="""\
USE delguur;

-- 0. Түр хүснэгтүүд
DROP TABLE IF EXISTS tur_zahialgiin_mur;
DROP TABLE IF EXISTS tur_tasalbar;

-- 1. AUTO_INCREMENT = 100: 100-аас эхэлнэ
CREATE TABLE tur_tasalbar (
    tasalbar_id INT AUTO_INCREMENT,
    garchig     VARCHAR(100) NOT NULL,
    CONSTRAINT pk_tur_tasalbar PRIMARY KEY (tasalbar_id)
) AUTO_INCREMENT = 100;

INSERT INTO tur_tasalbar (garchig)
VALUES ('Хүргэлт хоцорсон'), ('Бараа буцаах');     -- 100, 101

SELECT * FROM tur_tasalbar;

-- 2. ROLLBACK хийсэн INSERT дугаараа буцааж өгөхгүй
START TRANSACTION;
INSERT INTO tur_tasalbar (garchig) VALUES ('Буцаагдах мөр');   -- 102
ROLLBACK;

INSERT INTO tur_tasalbar (garchig) VALUES ('Цоорхойн дараах');
SELECT LAST_INSERT_ID() AS shine_id;               -- 103: 102 алга

-- 3. Гараар дугаар өгөх: шууд болно
INSERT INTO tur_tasalbar (tasalbar_id, garchig) VALUES (500, 'Гараар дугаарласан');

-- NULL өгвөл дараагийн дугаар автоматаар: 501
INSERT INTO tur_tasalbar (tasalbar_id, garchig) VALUES (NULL, 'Дараагийнх');

SELECT * FROM tur_tasalbar ORDER BY tasalbar_id;

-- 4. PRIMARY KEY-ийн нэр үргэлж PRIMARY (pk_tur_tasalbar биш)
SHOW INDEX FROM tur_tasalbar;

-- 5. Нийлмэл түлхүүр
CREATE TABLE tur_zahialgiin_mur (
    zahialga_id INT NOT NULL,
    baraa_id    INT NOT NULL,
    too         INT NOT NULL,
    CONSTRAINT pk_tur_zahialgiin_mur PRIMARY KEY (zahialga_id, baraa_id)
);

INSERT INTO tur_zahialgiin_mur (zahialga_id, baraa_id, too)
VALUES (1, 1, 1), (1, 3, 2), (2, 3, 1);   -- хос бүр өөр тул болно

SELECT * FROM tur_zahialgiin_mur;

-- 6. Давхардал. Тайлбарыг НЭГ НЭГЭЭР арилгаж тусад нь ажиллуул:

-- (1, 3) аль хэдийн байна -> ERROR 1062 Duplicate entry '1-3'
-- INSERT INTO tur_zahialgiin_mur (zahialga_id, baraa_id, too) VALUES (1, 3, 5);

-- 100 дугаартай тасалбар байна -> ERROR 1062 Duplicate entry '100'
-- INSERT INTO tur_tasalbar (tasalbar_id, garchig) VALUES (100, 'Давхар');

-- 7. Тоолуурын одоогийн утга: AUTO_INCREMENT=502
SHOW CREATE TABLE tur_tasalbar;

-- 8. Цэвэрлэх
DROP TABLE IF EXISTS tur_zahialgiin_mur;
DROP TABLE IF EXISTS tur_tasalbar;
""",
        ),
        LessonSpec(
            title="FOREIGN KEY ба холбоосын үйлдлүүд",
            slug="foreign-key-cascade-set-null",
            description="Хүснэгтийг холбох, CASCADE, SET NULL, RESTRICT, FK алдаа.",
            duration=660,
            language=MY,
            content="""\
**FOREIGN KEY** нь нэг хүснэгтийн багана нөгөө хүснэгтийн **байгаа**
мөрийг заахыг баталгаажуулна. `baraa.angilal_id` нь `angilal`-д байхгүй
ангиллыг заах боломжгүй.

```text
angilal (эцэг)            baraa (хүүхэд)
angilal_id  PK  <───────  angilal_id  FK
```

### Бичиглэл

```sql
CREATE TABLE tur_baraa (
    baraa_id   INT AUTO_INCREMENT PRIMARY KEY,
    ner        VARCHAR(100) NOT NULL,
    angilal_id INT NULL,
    CONSTRAINT fk_tur_baraa_angilal
        FOREIGN KEY (angilal_id)
        REFERENCES tur_angilal (angilal_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE = InnoDB;
```

Шаардлага:

- Эцгийн багана `PRIMARY KEY` эсвэл `UNIQUE` байх.
- Хоёр багана **ижил төрөлтэй** (`INT` ↔ `INT`; MySQL-д `INT` ↔
  `INT UNSIGNED` ч таарахгүй).
- Хүүхэд мөр нэмэхээс өмнө эцгийн мөр байх.

### MySQL-ийн онцлог

> **InnoDB шаардлагатай.** MyISAM зэрэг хөдөлгүүр FOREIGN KEY-г уншаад
> **үл тоомсорлодог** — алдаа ч өгөхгүй. MySQL 8.0-ийн анхдагч InnoDB,
> гэхдээ хуучин хүснэгтийг `SHOW TABLE STATUS`-аар шалга.

> **Баганын дэргэдэх `REFERENCES`** (`angilal_id INT REFERENCES
> angilal(angilal_id)`) нь MySQL 8.0/8.4 дээр мөн **үл тоомсорлогддог**.
> Үргэлж хүснэгтийн төгсгөлд `FOREIGN KEY (…) REFERENCES …` гэж бич.

- FK баганад индекс байхгүй бол MySQL түүнийг **автоматаар** үүсгэнэ —
  JOIN болон эцэг мөр устгах шалгалт хурдан байна.
- `SET FOREIGN_KEY_CHECKS = 0;` нь FK шалгалтыг тухайн session-д түр
  унтраана. Их хэмжээний өгөгдөл ачаалахад л хэрэглэж, дараа нь заавал
  `= 1` болго — унтраалттай үед орсон буруу мөрийг дараа нь хэн ч
  шалгахгүй.

### Холбоосын үйлдлүүд

Эцгийн мөрийг **устгах** (`ON DELETE`) эсвэл түлхүүрийг нь **өөрчлөх**
(`ON UPDATE`) үед хүүхэд мөрүүдэд юу болох вэ:

| Үйлдэл | Утга | InnoDB |
|---|---|---|
| `NO ACTION` | Хүүхэд байвал татгалзана | Тийм (анхдагч) |
| `RESTRICT` | Мөн адил татгалзана | Тийм |
| `CASCADE` | Хүүхдийг хамт устгана/өөрчилнө | Тийм |
| `SET NULL` | Хүүхдийн FK-г `NULL` болгоно | Тийм |
| `SET DEFAULT` | Анхдагч утга болгоно | **Татгалзана** |

- InnoDB-д `RESTRICT` ба `NO ACTION` яг ижил — тэр дор нь шалгана.
  `ON DELETE` бичээгүй бол ийм байна.
- `SET NULL`-д FK багана `NULL` зөвшөөрдөг байх ёстой.

### Хэзээ алийг нь

| Холбоо | Сонголт | Шалтгаан |
|---|---|---|
| `zahialga` → `zahialgiin_mur` | `CASCADE` | Мөр захиалгагүйгээр утгагүй |
| `angilal` → `baraa` | `RESTRICT` / `NO ACTION` | Бараатай ангиллыг андуурч устгахгүй |
| `ajiltan` → `menejer_id` | `SET NULL` | Менежер гарсан ч ажилтан үлдэнэ |
| `hereglegch` → `zahialga` | `NO ACTION` | Санхүүгийн түүх хадгалагдана |

> `CASCADE` хүчтэй ч **аюултай**: нэг `DELETE` олон хүснэгтийн мянган мөрийг
> чимээгүй устгаж болно.

### FK зөрчлийн алдаа

```text
-- MySQL: байхгүй эцгийг заах
ERROR 1452 (23000): Cannot add or update a child row: a foreign key constraint
fails (`delguur`.`tur_baraa`, CONSTRAINT `fk_tur_baraa_angilal` FOREIGN KEY
(`angilal_id`) REFERENCES `tur_angilal` (`angilal_id`) ...)

-- MySQL: хүүхэдтэй эцгийг устгах
ERROR 1451 (23000): Cannot delete or update a parent row: a foreign key
constraint fails (...)
```

### Хүснэгт үүсгэх, устгах дараалал

- **Үүсгэх:** эцэг → хүүхэд (`angilal`, дараа нь `baraa`)
- **Устгах:** хүүхэд → эцэг (`baraa`, дараа нь `angilal`)

Эсрэгээр нь хийвэл FK алдаа өгнө.
""",
            initial_code="""\
USE delguur;

-- 0. Өмнөх ажиллуулалтаас үлдсэнийг цэвэрлэх: хүүхэд -> эцэг
DROP TABLE IF EXISTS tur_setgegdel;
DROP TABLE IF EXISTS tur_baraa_zurag;
DROP TABLE IF EXISTS tur_baraa;
DROP TABLE IF EXISTS tur_angilal;

-- 1. Эцэг хүснэгт
CREATE TABLE tur_angilal (
    angilal_id INT AUTO_INCREMENT PRIMARY KEY,
    ner        VARCHAR(50) NOT NULL UNIQUE
) ENGINE = InnoDB;

-- 2. Бараа: ангилал устгавал NULL, ангиллын id солигдвол дагаж солигдоно
CREATE TABLE tur_baraa (
    baraa_id   INT AUTO_INCREMENT PRIMARY KEY,
    ner        VARCHAR(100) NOT NULL,
    angilal_id INT NULL,                        -- SET NULL тул NULL зөвшөөрнө
    CONSTRAINT fk_tur_baraa_angilal
        FOREIGN KEY (angilal_id)
        REFERENCES tur_angilal (angilal_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE = InnoDB;

-- 3. Зураг: бараа устгавал зураг нь хамт устана
CREATE TABLE tur_baraa_zurag (
    zurag_id INT AUTO_INCREMENT PRIMARY KEY,
    baraa_id INT NOT NULL,
    zam      VARCHAR(200) NOT NULL,
    CONSTRAINT fk_tur_baraa_zurag_baraa
        FOREIGN KEY (baraa_id)
        REFERENCES tur_baraa (baraa_id)
        ON DELETE CASCADE
) ENGINE = InnoDB;

-- 4. Сэтгэгдэл: сэтгэгдэлтэй барааг устгахыг хориглоно
CREATE TABLE tur_setgegdel (
    setgegdel_id  INT AUTO_INCREMENT PRIMARY KEY,
    baraa_id      INT NOT NULL,
    hereglegch_id INT NOT NULL,
    tekst         VARCHAR(500) NOT NULL,
    CONSTRAINT fk_tur_setgegdel_baraa
        FOREIGN KEY (baraa_id)
        REFERENCES tur_baraa (baraa_id)
        ON DELETE RESTRICT,
    CONSTRAINT fk_tur_setgegdel_hereglegch       -- жишээ сангийн hereglegch
        FOREIGN KEY (hereglegch_id)
        REFERENCES hereglegch (hereglegch_id)
) ENGINE = InnoDB;

-- 5. Өгөгдөл: эцэг -> хүүхэд дарааллаар
INSERT INTO tur_angilal (ner) VALUES ('Электроник'), ('Ном');       -- 1, 2

INSERT INTO tur_baraa (ner, angilal_id)
VALUES ('Чихэвч', 1), ('Ухаалаг утас', 1), ('SQL сурах бичиг', 2); -- 1, 2, 3

INSERT INTO tur_baraa_zurag (baraa_id, zam)
VALUES (1, 'zurag/chihevch-1.jpg'),
       (1, 'zurag/chihevch-2.jpg'),
       (2, 'zurag/utas.jpg');

INSERT INTO tur_setgegdel (baraa_id, hereglegch_id, tekst)
VALUES (3, 1, 'Маш ойлгомжтой ном');

-- 6. FK баганад индекс автоматаар үүссэн
SHOW INDEX FROM tur_baraa_zurag;

-- 7. FK зөрчил. Тайлбарыг НЭГ НЭГЭЭР арилгаж тусад нь ажиллуул:

-- Байхгүй ангилал 99 -> ERROR 1452
-- INSERT INTO tur_baraa (ner, angilal_id) VALUES ('Сүнс бараа', 99);

-- Байхгүй хэрэглэгч 99 -> ERROR 1452
-- INSERT INTO tur_setgegdel (baraa_id, hereglegch_id, tekst) VALUES (1, 99, 'Тест');

-- Сэтгэгдэлтэй бараа, RESTRICT -> ERROR 1451
-- DELETE FROM tur_baraa WHERE baraa_id = 3;

-- Жишээ сан: бараатай ангилал 3 -> ERROR 1451
-- DELETE FROM angilal WHERE angilal_id = 3;

-- Хүүхэдтэй эцэг хүснэгтийг устгах -> ERROR 3730
-- DROP TABLE tur_angilal;

-- 8. ON UPDATE CASCADE: ангиллын id 1 -> 10
UPDATE tur_angilal SET angilal_id = 10 WHERE angilal_id = 1;
SELECT * FROM tur_baraa;             -- Чихэвч, Ухаалаг утас: angilal_id = 10

-- 9. ON DELETE CASCADE: Чихэвч устахад 2 зураг нь хамт устана
DELETE FROM tur_baraa WHERE baraa_id = 1;
SELECT * FROM tur_baraa_zurag;       -- зөвхөн utas.jpg үлдэнэ

-- 10. ON DELETE SET NULL: Электроник устахад Ухаалаг утас ангилалгүй болно
DELETE FROM tur_angilal WHERE angilal_id = 10;
SELECT * FROM tur_baraa;             -- Ухаалаг утас: angilal_id = NULL

-- 11. FK-уудын дүрмийг харах
SELECT CONSTRAINT_NAME, TABLE_NAME, REFERENCED_TABLE_NAME, UPDATE_RULE, DELETE_RULE
FROM information_schema.REFERENTIAL_CONSTRAINTS
WHERE CONSTRAINT_SCHEMA = 'delguur' AND TABLE_NAME LIKE 'tur%';

-- 12. Цэвэрлэх: хүүхэд -> эцэг
DROP TABLE IF EXISTS tur_setgegdel;
DROP TABLE IF EXISTS tur_baraa_zurag;
DROP TABLE IF EXISTS tur_baraa;
DROP TABLE IF EXISTS tur_angilal;
""",
        ),
    ],
)

SQL_DEFINITION_MODULES = [CREATING_TABLES, MODIFYING_DATA, CONSTRAINTS]
