"""Модул 12-14 — Өгөгдлийн сангийн дизайн, view ба index, transaction ба түгжээ.

Хүснэгтийг зөв хувааж холбох, асуулгыг хурдасгах, олон хэрэглэгч зэрэг
ажиллахад өгөгдлийг бүрэн бүтэн хадгалах сэдвүүд.
"""

from app.content.types import LessonSpec, ModuleSpec
from app.models.enums import LessonLanguage

MY = LessonLanguage.MYSQL

DESIGN = ModuleSpec(
    title="Модул 12 — Өгөгдлийн сангийн дизайн",
    description="Хамаарал, нормчлол, түлхүүр ба нэрлэлтийн дүрэм.",
    lessons=[
        LessonSpec(
            title="Хамаарал: 1:1, 1:N, N:M",
            slug="hamaaral-1-1-1-n-n-m",
            description="Хүснэгтүүдийг гадаад түлхүүрээр хэрхэн холбох вэ.",
            duration=540,
            language=MY,
            content="""\
Өгөгдлийн сангийн дизайны гол асуулт: **нэг зүйл нөгөөтэйгөө хэдэн
удаа холбогдох вэ?** Хариулт нь гадаад түлхүүрийг (FOREIGN KEY) хаана
тавихыг шийднэ.

### Гурван төрөл

| Төрөл | Утга | `delguur` дахь жишээ | FK хаана байх вэ |
|---|---|---|---|
| 1:1 | Нэг мөр яг нэг мөртэй | хэрэглэгч ба түүний профайл | Аль нэг талд, `UNIQUE`-тэй |
| 1:N | Нэг мөр олон мөртэй | `angilal` → `baraa` | «Олон» талд |
| N:M | Олон мөр олон мөртэй | `zahialga` ↔ `baraa` | Тусдаа холбох хүснэгтэд |

### 1:N — хамгийн түгээмэл

Нэг ангилалд олон бараа байна, харин бараа бүр яг нэг ангилалтай:

```text
angilal (1) ────────< (N) baraa
   angilal_id  <────────  angilal_id  (FK)
```

FK нь **«олон»** талын хүснэгтэд байна. Эсрэгээр нь `angilal` дотор
«бараануудын жагсаалт» багана хийх нь буруу — нэг нүдэнд олон утга
хадгалах болно.

Өөр жишээ: `hereglegch` → `zahialga`, мөн `ajiltan.menejer_id` нь өөрөө
өөртэйгээ холбогдсон 1:N (нэг менежер олон ажилтантай).

### 1:1

Нэг хэрэглэгч нэг л профайлтай. FK баганыг `UNIQUE` (эсвэл шууд
`PRIMARY KEY`) болговол давхардал үүсэхгүй:

```sql
CREATE TABLE hereglegch_profile (
    hereglegch_id INT PRIMARY KEY,          -- PK нь FK ч мөн
    tursun_ognoo  DATE NULL,
    FOREIGN KEY (hereglegch_id) REFERENCES hereglegch (hereglegch_id)
);
```

> 1:1-ийг ихэвчлэн ховор хэрэглэгддэг, том эсвэл нууц баганыг
> салгахад ашиглана. Үгүй бол нэг хүснэгтэд байлгах нь энгийн.

### N:M — холбох хүснэгт (junction table)

Нэг захиалгад олон бараа, нэг бараа олон захиалгад орно. Хоёр хүснэгтийн
аль алинд нь FK тавьж чадахгүй тул **гурав дахь** хүснэгт хэрэгтэй.
`delguur`-д энэ нь `zahialgiin_mur`:

```text
hereglegch (1)──<(N) zahialga (1)──<(N) zahialgiin_mur (N)>──(1) baraa
                                                                   │
                                                          (N)>──(1) angilal
```

```sql
CREATE TABLE zahialgiin_mur (
    zahialga_id INT NOT NULL,
    baraa_id    INT NOT NULL,
    too         INT NOT NULL,
    negj_une    DECIMAL(12,2) NOT NULL,
    PRIMARY KEY (zahialga_id, baraa_id),    -- давхар мөр орохгүй
    FOREIGN KEY (zahialga_id) REFERENCES zahialga (zahialga_id),
    FOREIGN KEY (baraa_id)    REFERENCES baraa (baraa_id)
);
```

Холбох хүснэгт нь зөвхөн хоёр ID биш, **холбоосны өөрийн шинж чанарыг**
(`too`, `negj_une`) хадгалж болно.

### ER диаграмыг текстээр

Crow's foot тэмдэглэгээнд `<` нь «олон», `|` нь «яг нэг» гэсэн утгатай.
Цаасан дээр эсвэл MySQL Workbench-ийн **EER Diagram** хэрэгслээр зурж
болно: Database → Reverse Engineer нь байгаа сангаас диаграмыг өөрөө
зурна.

### MySQL-д санах зүйл

- FOREIGN KEY зөвхөн **InnoDB** хүснэгтэд ажиллана (MySQL 8-ийн анхдагч).
- FK баганад index байхгүй бол MySQL түүнийг автоматаар үүсгэнэ.
- Эцэг мөрийг устгах, өөрчлөх үеийн үйлдлийг (`CASCADE`, `SET NULL`,
  `RESTRICT`) Модул 8-д үзсэн.
""",
            initial_code="""\
USE delguur;

-- Өмнө нь ажиллуулсан бол цэвэрлэнэ (хүүхэд хүснэгтээс эхэлж устгана)
DROP TABLE IF EXISTS tur_burtgel;
DROP TABLE IF EXISTS tur_oyutan;
DROP TABLE IF EXISTS tur_hicheel;

-- 1. Оюутан ба хичээл: N:M хамаарал
CREATE TABLE tur_oyutan (
    oyutan_id INT AUTO_INCREMENT PRIMARY KEY,
    ner       VARCHAR(50) NOT NULL
);

CREATE TABLE tur_hicheel (
    hicheel_id INT AUTO_INCREMENT PRIMARY KEY,
    ner        VARCHAR(50) NOT NULL
);

-- 2. Холбох хүснэгт: нийлмэл PK нь давхар бүртгэлээс сэргийлнэ
CREATE TABLE tur_burtgel (
    oyutan_id  INT NOT NULL,
    hicheel_id INT NOT NULL,
    unelgee    CHAR(1) NULL,
    PRIMARY KEY (oyutan_id, hicheel_id),
    FOREIGN KEY (oyutan_id)  REFERENCES tur_oyutan (oyutan_id),
    FOREIGN KEY (hicheel_id) REFERENCES tur_hicheel (hicheel_id)
);

INSERT INTO tur_oyutan (ner) VALUES ('Болд'), ('Сараа'), ('Анар');
INSERT INTO tur_hicheel (ner) VALUES ('SQL'), ('Python'), ('Англи хэл');

INSERT INTO tur_burtgel (oyutan_id, hicheel_id, unelgee) VALUES
    (1, 1, 'A'), (1, 2, 'B'),
    (2, 1, NULL),
    (3, 2, 'A'), (3, 3, 'C');

-- 3. Хэн ямар хичээл үзэж байна вэ
SELECT o.ner AS oyutan, h.ner AS hicheel, b.unelgee
FROM tur_burtgel AS b
JOIN tur_oyutan  AS o ON o.oyutan_id  = b.oyutan_id
JOIN tur_hicheel AS h ON h.hicheel_id = b.hicheel_id
ORDER BY o.ner, h.ner;

-- 4. Хичээл тус бүрд хэдэн оюутан
SELECT h.ner, COUNT(b.oyutan_id) AS oyutny_too
FROM tur_hicheel AS h
LEFT JOIN tur_burtgel AS b ON b.hicheel_id = h.hicheel_id
GROUP BY h.hicheel_id, h.ner;

-- 5. Дараах мөр алдаа өгнө: давхар бүртгэл (Duplicate entry)
-- INSERT INTO tur_burtgel (oyutan_id, hicheel_id) VALUES (1, 1);

-- 6. delguur дахь бодит N:M: захиалга бүрийн бараанууд
SELECT m.zahialga_id, b.ner, m.too
FROM zahialgiin_mur AS m
JOIN baraa AS b ON b.baraa_id = m.baraa_id
WHERE m.zahialga_id IN (1, 7);

-- 7. Цэвэрлэгээ
DROP TABLE IF EXISTS tur_burtgel;
DROP TABLE IF EXISTS tur_oyutan;
DROP TABLE IF EXISTS tur_hicheel;
""",
        ),
        LessonSpec(
            title="Нормчлол: 1NF, 2NF, 3NF",
            slug="normalchlal-1nf-2nf-3nf",
            description="Муу хүснэгтийг алхам алхмаар зөв хувааж, аномалиас сэргийлэх.",
            duration=660,
            language=MY,
            content="""\
**Нормчлол** (normalization) гэдэг нь нэг баримтыг **нэг л газар**
хадгалахаар хүснэгтүүдийг хуваах арга. Зорилго нь давхардал ба
зөрчилтэй өгөгдлөөс сэргийлэх.

### Эхлэл: муу хүснэгт

Бүх зүйлийг нэг хүснэгтэд хийсэн гэж бодъё:

| zahialga_id | hereglegch | email | hot | baraanuud |
|---|---|---|---|---|
| 1 | Болд | bold@example.mn | Улаанбаатар | Ухаалаг утас, Чихэвч |
| 2 | Сараа | saraa@example.mn | Улаанбаатар | Ноосон цамц, Цайны аяга |
| 3 | Болд | bold@example.mn | Улаанбаатар | Монгол түүх, SQL сурах бичиг |

Энгийн харагдах ч гурван **аномали** (зөрчил) нуугдаж байна.

### Гурван аномали

| Аномали | Юу болох вэ |
|---|---|
| **Шинэчлэх** (update) | Болд Дархан руу нүүвэл 1 ба 3-р мөрийг хоёуланг нь засна. Нэгийг мартвал өгөгдөл зөрнө |
| **Нэмэх** (insert) | Захиалгагүй шинэ хэрэглэгчийг (жишээ нь Мөнх) оруулах газар алга — `zahialga_id` заавал хэрэгтэй |
| **Устгах** (delete) | Сараагийн цорын ганц захиалгыг устгавал түүний email, хот хамт алга болно |

Мөн `baraanuud` багана дахь таслалаар тусгаарласан жагсаалтыг тоолох,
JOIN хийх, index-лэх боломжгүй. `LIKE '%Чихэвч%'` гэж хайх нь удаан бөгөөд
«Чихэвч» гэдэг үгийг агуулсан өөр барааг ч барина. MySQL-ийн
`FIND_IN_SET('Чихэвч', baraanuud)` функц таслалтай жагсаалтаас яг тэр
элементийг олж чадах ч мөн index ашиглаж чадахгүй.

### 1NF — нүд бүр атомар

**Дүрэм:** нүд бүрт нэг л утга, давтагдах бүлэг байхгүй, мөр бүр PK-тай.

Жагсаалтыг задалж, **бараа бүрийг тусдаа мөр** болгоно:

| zahialga_id | baraa | une | hereglegch | email | hot |
|---|---|---|---|---|---|
| 1 | Ухаалаг утас | 1250000 | Болд | bold@example.mn | Улаанбаатар |
| 1 | Чихэвч | 89000 | Болд | bold@example.mn | Улаанбаатар |
| ... | | | | | |

PK = `(zahialga_id, baraa)`. Жагсаалтын асуудал шийдэгдсэн ч давхардал
бүр ч нэмэгдлээ.

### 2NF — нийлмэл түлхүүрийн **хэсгээс** хамаарахгүй

**Дүрэм:** 1NF + түлхүүр биш багана бүр **бүтэн** PK-аас хамаарна.

- `hereglegch`, `email`, `hot` нь зөвхөн `zahialga_id`-аас хамаарна
- `une` нь зөвхөн `baraa`-аас хамаарна

Тиймээс салгана:

```text
zahialga       (zahialga_id PK, hereglegch, email, hot)
baraa          (baraa_id PK, ner, une)
zahialgiin_mur (zahialga_id, baraa_id, too)   PK = хоёулаа
```

### 3NF — дамжсан хамаарал байхгүй

**Дүрэм:** 2NF + түлхүүр биш багана өөр түлхүүр биш баганаас хамаарахгүй.

`zahialga` дотор: `zahialga_id → email → hot`. Хот нь захиалгын биш,
**хэрэглэгчийн** шинж. Дахин салгана:

```text
hereglegch (hereglegch_id PK, ner, email UNIQUE, hot)
zahialga   (zahialga_id PK, hereglegch_id FK, zahialsan_ognoo)
```

Одоо Болдын хот **нэг л мөрөнд** байна. Энэ нь яг `delguur`-ийн бүтэц.

Хуваасан хүснэгтүүдээс анхны «жагсаалттай» харагдах байдлыг `JOIN` ба
`GROUP_CONCAT`-аар сэргээж болно. `GROUP_CONCAT(b.ner ORDER BY b.baraa_id
SEPARATOR ', ')` нь бүлэг доторх утгуудыг нэг текст болгон нийлүүлдэг
MySQL-ийн агрегат функц — **харуулахад** тохиромжтой, хадгалахад биш.

> Санах хэллэг: «Түлхүүрээс, бүтэн түлхүүрээс, зөвхөн түлхүүрээс
> хамаар» (the key, the whole key, and nothing but the key).

### `negj_une` давхардал биш үү?

`zahialgiin_mur.negj_une` нь `baraa.une`-тэй адилхан санагдана. Гэхдээ
энэ бол **захиалсан үеийн** үнэ — өөр баримт. Бараа үнэ өөрчлөгдөхөд
хуучин захиалгын дүн өөрчлөгдөх ёсгүй тул тусад нь хадгална.

### Хэзээ санаатай денормчлох вэ

- **Тайлан, аналитик** — сая сая мөр JOIN хийхээс нэг өргөн хүснэгт хурдан
- **Кэш утга** — захиалгын нийт дүнг баганад хадгалах (trigger эсвэл
  програмаар шинэчилнэ)
- **Түүхэн хормын хувилбар** — дээрх `negj_une` шиг

> Эхлээд 3NF хүртэл нормчил. Хэмжиж, удаан байгааг нотолсны дараа л
> денормчил — тэгэхдээ давхар утгыг хэрхэн синк хийхээ заавал шийд.
""",
            initial_code="""\
USE delguur;

DROP TABLE IF EXISTS tur_n_zahialgiin_mur;
DROP TABLE IF EXISTS tur_n_zahialga;
DROP TABLE IF EXISTS tur_n_baraa;
DROP TABLE IF EXISTS tur_n_hereglegch;
DROP TABLE IF EXISTS tur_zahialga_muu;

-- 1. Нормчлоогүй муу хүснэгт
CREATE TABLE tur_zahialga_muu (
    zahialga_id INT PRIMARY KEY,
    hereglegch  VARCHAR(50),
    email       VARCHAR(100),
    hot         VARCHAR(50),
    baraanuud   VARCHAR(255)
);

INSERT INTO tur_zahialga_muu VALUES
    (1, 'Болд',  'bold@example.mn',  'Улаанбаатар', 'Ухаалаг утас,Чихэвч'),
    (2, 'Сараа', 'saraa@example.mn', 'Улаанбаатар', 'Ноосон цамц,Цайны аяга'),
    (3, 'Болд',  'bold@example.mn',  'Улаанбаатар', 'Монгол түүх,SQL сурах бичиг');

-- 2. Жагсаалтаас хайх нь эвгүй: FIND_IN_SET нь index ашиглаж чадахгүй
SELECT zahialga_id FROM tur_zahialga_muu
WHERE FIND_IN_SET('Чихэвч', baraanuud) > 0;

-- 3. Шинэчлэх аномали: нэг мөрийг л зассан тул Болд хоёр хоттой боллоо
UPDATE tur_zahialga_muu SET hot = 'Дархан' WHERE zahialga_id = 1;
SELECT DISTINCT hereglegch, hot FROM tur_zahialga_muu WHERE hereglegch = 'Болд';

-- 4. 3NF бүтэц
CREATE TABLE tur_n_hereglegch (
    hereglegch_id INT AUTO_INCREMENT PRIMARY KEY,
    ner   VARCHAR(50)  NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    hot   VARCHAR(50)  NULL
);

CREATE TABLE tur_n_baraa (
    baraa_id INT AUTO_INCREMENT PRIMARY KEY,
    ner      VARCHAR(100) NOT NULL,
    une      DECIMAL(12,2) NOT NULL
);

CREATE TABLE tur_n_zahialga (
    zahialga_id   INT PRIMARY KEY,
    hereglegch_id INT NOT NULL,
    FOREIGN KEY (hereglegch_id) REFERENCES tur_n_hereglegch (hereglegch_id)
);

CREATE TABLE tur_n_zahialgiin_mur (
    zahialga_id INT NOT NULL,
    baraa_id    INT NOT NULL,
    too         INT NOT NULL DEFAULT 1,
    PRIMARY KEY (zahialga_id, baraa_id),
    FOREIGN KEY (zahialga_id) REFERENCES tur_n_zahialga (zahialga_id),
    FOREIGN KEY (baraa_id)    REFERENCES tur_n_baraa (baraa_id)
);

INSERT INTO tur_n_hereglegch (ner, email, hot) VALUES
    ('Болд',  'bold@example.mn',  'Улаанбаатар'),
    ('Сараа', 'saraa@example.mn', 'Улаанбаатар'),
    ('Мөнх',  'munh@example.mn',  'Улаанбаатар');  -- захиалгагүй ч орно

INSERT INTO tur_n_baraa (ner, une) VALUES
    ('Ухаалаг утас', 1250000), ('Чихэвч', 89000), ('Ноосон цамц', 145000),
    ('Цайны аяга', 18000), ('Монгол түүх', 35000), ('SQL сурах бичиг', 48000);

INSERT INTO tur_n_zahialga (zahialga_id, hereglegch_id) VALUES (1, 1), (2, 2), (3, 1);

INSERT INTO tur_n_zahialgiin_mur (zahialga_id, baraa_id) VALUES
    (1, 1), (1, 2), (2, 3), (2, 4), (3, 5), (3, 6);

-- 5. Хот одоо нэг л газар: нэг мөр засахад хангалттай
UPDATE tur_n_hereglegch SET hot = 'Дархан' WHERE hereglegch_id = 1;

-- 6. Анхны харагдах байдлыг JOIN ба GROUP_CONCAT-аар сэргээх
SELECT z.zahialga_id, h.ner, h.hot,
       GROUP_CONCAT(b.ner ORDER BY b.baraa_id SEPARATOR ', ') AS baraanuud
FROM tur_n_zahialga AS z
JOIN tur_n_hereglegch     AS h ON h.hereglegch_id = z.hereglegch_id
JOIN tur_n_zahialgiin_mur AS m ON m.zahialga_id = z.zahialga_id
JOIN tur_n_baraa          AS b ON b.baraa_id = m.baraa_id
GROUP BY z.zahialga_id, h.ner, h.hot;

-- 7. Цэвэрлэгээ
DROP TABLE IF EXISTS tur_n_zahialgiin_mur;
DROP TABLE IF EXISTS tur_n_zahialga;
DROP TABLE IF EXISTS tur_n_baraa;
DROP TABLE IF EXISTS tur_n_hereglegch;
DROP TABLE IF EXISTS tur_zahialga_muu;
""",
        ),
        LessonSpec(
            title="Түлхүүр ба нэрлэлтийн дүрэм",
            slug="tulhuur-nerlelt-quoting",
            description="Байгалийн ба орлуулагч түлхүүр, нэрлэлт, нөөц үгийг backtick-ээр хашилтлах.",
            duration=600,
            language=MY,
            content="""\
### Байгалийн ба орлуулагч түлхүүр

| | Байгалийн (natural) | Орлуулагч (surrogate) |
|---|---|---|
| Жишээ | email, регистрийн дугаар, ISO улсын код `MN` | `hereglegch_id` = 1, 2, 3... |
| Утга | Бодит ертөнцөд утгатай | Утгагүй, зөвхөн ялгах зорилготой |
| Өөрчлөгдөх үү | Өөрчлөгдөж болно (email солих) | Хэзээ ч өөрчлөгдөхгүй |
| Хэмжээ | Урт байж болно | Жижиг (`INT` = 4 байт) |

Практикт түгээмэл шийдэл: **орлуулагч PK + байгалийн түлхүүрт `UNIQUE`**.
`delguur`-ийн `hereglegch` яг ийм: `hereglegch_id` нь PK, `email` нь `UNIQUE`.

> Өөрчлөгдөж болох утгыг PK болговол түүнийг заасан бүх FK-г хамт
> шинэчлэх шаардлага гарна.

Үргэлж богино, хэзээ ч өөрчлөгдөхгүй байгалийн түлхүүр (ISO улсын код
`MN`, `JP`) бол PK болгож болно.

### Орлуулагч түлхүүр үүсгэх

| Хэрэгцээ | MySQL |
|---|---|
| Автомат тоо | `INT AUTO_INCREMENT PRIMARY KEY` |
| Сүүлд үүссэн ID | `LAST_INSERT_ID()` |
| UUID | `UUID()` → `CHAR(36)` эсвэл `BINARY(16)` |
| Дараалсан UUID | `UUID_TO_BIN(UUID(), 1)` |

UUID нь серверээс асуулгүйгээр (гар утас, өөр систем дээр) давтагдашгүй
ID үүсгэх боломж өгнө. Гэхдээ 16 байт — `INT`-ээс 4 дахин том.

> InnoDB хүснэгт PK-ийн дарааллаар хадгалагддаг (Модул 13). Санамсаргүй
> UUID-г PK болговол шинэ мөр хүснэгтийн дунд орж, хуудас хуваагдах
> (page split) тул бичих үйлдэл удаашрана. `UUID_TO_BIN(UUID(), 1)`-ийн
> `1` нь цагийн хэсгийг урагш зөөж, UUID-г өсөх дараалалтай болгоно.

### Нийлмэл түлхүүр

Хэд хэдэн баганаас бүтсэн PK. Холбох хүснэгтэд байгалийн сонголт:

```sql
PRIMARY KEY (zahialga_id, baraa_id)
```

Баганын **дараалал чухал** — энэ нь index-ийн дараалал болно (Модул 13).

### Нэрлэлтийн дүрэм

| Дүрэм | Сайн | Муу |
|---|---|---|
| `snake_case`, жижиг үсэг | `zahialgiin_mur` | `ZahialgiinMur`, `zahialgiin mur` |
| PK нь `<хүснэгт>_id` | `baraa_id` | `id`, `BaraaID` |
| FK нь заасан PK-тай ижил нэр | `zahialga.hereglegch_id` | `zahialga.user` |
| Нөөц үг бүү ашигла | `zahialsan_ognoo` | `date`, `order` |
| Constraint-д угтвар | `fk_`, `uq_`, `ck_`, `ix_` | MySQL-ийн өгдөг `tur_baraa_ibfk_1`, `tur_baraa_chk_1` |

**Ганц эсвэл олон тоо?** `baraa` эсвэл `baraanuud` — аль алиныг нь
хэрэглэдэг. Гол нь **нэг төсөлд нэгийг** сонгож тууштай баримтлах.
Энэ сургалт ганц тоо ашигладаг.

**Том жижиг үсэг:** MySQL-д хүснэгтийн нэр файлын системээс хамаарна
(`lower_case_table_names`: Linux дээр 0 — ялгана, Windows дээр 1, macOS
дээр 2). Тиймээс **үргэлж жижиг үсгээр** нэрлэвэл аль ч серверт ажиллана.

### Нөөц үг ба хашилт

`order`, `group`, `key`, `rank` зэрэг нөөц үгийг нэр болгож заавал
хэрэглэх бол **backtick**-ээр хашина:

```sql
SELECT `order`, `group` FROM tur_nerlelt;
```

| Бичлэг | MySQL-д утга |
|---|---|
| `` `order` `` | Нэр (хүснэгт, багана) |
| `'order'` | Тэмдэгт мөр |
| `"order"` | Анхдагчаар **тэмдэгт мөр**, `ANSI_QUOTES` горимд нэр |

SQL стандартад давхар хашилт нь нэр. MySQL-ийг стандартын дагуу болгох
`ANSI_QUOTES` горимыг session-д асааж болно:

```sql
SET SESSION sql_mode = CONCAT(@@SESSION.sql_mode, ',ANSI_QUOTES');
SELECT "order" FROM tur_nerlelt;   -- одоо баганын утга гарна
```

`@@SESSION.sql_mode` нь одоогийн горим, `CONCAT` түүн дээр `ANSI_QUOTES`
нэмнэ. Тохиргоо зөвхөн энэ холболтод хамаарна. (`SET`, `@@` хувьсагчийг
Модул 16-д нарийн үзнэ.)

> Хувилбар шинэчлэхэд шинэ нөөц үг нэмэгддэг. Жишээ нь MySQL 8.0-оос
> `rank` нөөц үг болсон (window функц). Жагсаалтыг
> `information_schema.KEYWORDS`-оос харж болно.
""",
            initial_code="""\
USE delguur;

-- Хүүхэд хүснэгтээс эхэлж цэвэрлэнэ
DROP TABLE IF EXISTS tur_hereglegch_erh;
DROP TABLE IF EXISTS tur_erh;
DROP TABLE IF EXISTS tur_uls;
DROP TABLE IF EXISTS tur_nerlelt;

-- 1. Байгалийн түлхүүр: ISO улсын код
CREATE TABLE tur_uls (
    uls_kod CHAR(2)     NOT NULL,
    ner     VARCHAR(50) NOT NULL,
    CONSTRAINT pk_tur_uls PRIMARY KEY (uls_kod)
);

INSERT INTO tur_uls (uls_kod, ner)
VALUES ('MN', 'Монгол'), ('JP', 'Япон'), ('KR', 'Солонгос');

-- 2. Орлуулагч түлхүүр + байгалийн түлхүүрт UNIQUE
CREATE TABLE tur_erh (
    erh_id INT AUTO_INCREMENT,
    kod    VARCHAR(20) NOT NULL,
    ner    VARCHAR(50) NOT NULL,
    CONSTRAINT pk_tur_erh PRIMARY KEY (erh_id),
    CONSTRAINT uq_tur_erh_kod UNIQUE (kod)
);

INSERT INTO tur_erh (kod, ner) VALUES ('admin', 'Админ');
SELECT LAST_INSERT_ID() AS suuliin_id;   -- 1

INSERT INTO tur_erh (kod, ner) VALUES ('editor', 'Засварлагч');
SELECT LAST_INSERT_ID() AS suuliin_id;   -- 2

-- 3. Нийлмэл түлхүүр ба нэртэй constraint-ууд
CREATE TABLE tur_hereglegch_erh (
    hereglegch_id INT NOT NULL,
    erh_id        INT NOT NULL,
    CONSTRAINT pk_tur_hereglegch_erh PRIMARY KEY (hereglegch_id, erh_id),
    CONSTRAINT fk_tur_hereglegch_erh_hereglegch
        FOREIGN KEY (hereglegch_id) REFERENCES hereglegch (hereglegch_id),
    CONSTRAINT fk_tur_hereglegch_erh_erh
        FOREIGN KEY (erh_id) REFERENCES tur_erh (erh_id)
);

INSERT INTO tur_hereglegch_erh (hereglegch_id, erh_id)
VALUES (1, 1), (1, 2), (2, 2);

SELECT h.ner, e.kod
FROM tur_hereglegch_erh AS he
JOIN hereglegch AS h ON h.hereglegch_id = he.hereglegch_id
JOIN tur_erh    AS e ON e.erh_id = he.erh_id;

-- Constraint-ын нэрс ойлгомжтой (PRIMARY KEY-ийнх үргэлж PRIMARY)
SELECT CONSTRAINT_NAME, CONSTRAINT_TYPE
FROM information_schema.TABLE_CONSTRAINTS
WHERE TABLE_SCHEMA = 'delguur' AND TABLE_NAME = 'tur_hereglegch_erh';

-- 4. UUID: 36 тэмдэгт текст, BINARY(16) болгоход 16 байт
SELECT UUID() AS uuid_tekst,
       LENGTH(UUID_TO_BIN(UUID(), 1)) AS bait;

-- 5. Нөөц үгтэй багана: backtick хашилт
CREATE TABLE tur_nerlelt (
    tur_nerlelt_id INT AUTO_INCREMENT PRIMARY KEY,
    `order`        INT         NOT NULL,
    `group`        VARCHAR(20) NOT NULL,
    `rank`         INT         NULL
);

INSERT INTO tur_nerlelt (`order`, `group`, `rank`)
VALUES (1, 'А', 10), (2, 'Б', NULL);

SELECT `order`, `group`, `rank`
FROM tur_nerlelt
ORDER BY `order`;

-- 6. Давхар хашилт анхдагчаар ТЕКСТ: баганын утга биш order гэсэн үг гарна
SELECT "order" AS davhar_hashilt, `order` AS backtick
FROM tur_nerlelt;

-- 7. ANSI_QUOTES горимд давхар хашилт нэр болно (зөвхөн энэ холболтод)
SET SESSION sql_mode = CONCAT(@@SESSION.sql_mode, ',ANSI_QUOTES');
SELECT "order" AS davhar_hashilt FROM tur_nerlelt;

-- 8. Нөөц үг эсэхийг шалгах: RESERVED = 1 бол заавал хашина
SELECT WORD, RESERVED
FROM information_schema.KEYWORDS
WHERE WORD IN ('ORDER', 'GROUP', 'RANK', 'KEY', 'USER');

-- 9. Цэвэрлэгээ
DROP TABLE IF EXISTS tur_hereglegch_erh;
DROP TABLE IF EXISTS tur_erh;
DROP TABLE IF EXISTS tur_uls;
DROP TABLE IF EXISTS tur_nerlelt;
""",
        ),
    ],
)

VIEWS_INDEXES = ModuleSpec(
    title="Модул 13 — View ба Index",
    description="Хадгалсан асуулга, index-ийн бүтэц, гүйцэтгэлийн төлөвлөгөө унших.",
    lessons=[
        LessonSpec(
            title="View — хадгалсан асуулга",
            slug="view-uusgeh-mysql-tsql",
            description="CREATE OR REPLACE VIEW, шинэчлэх боломжтой view, WITH CHECK OPTION.",
            duration=600,
            language=MY,
            content="""\
**View** гэдэг нь нэртэй хадгалсан `SELECT`. Хүснэгт шиг асуулга
хийнэ, гэхдээ **өөрөө өгөгдөл хадгалдаггүй** — дуудах бүрт доторх
асуулга дахин ажиллана.

### Яагаад хэрэгтэй вэ

- Олон удаа бичдэг төвөгтэй JOIN, GROUP BY-г нэг нэрэнд нуух
- Хэрэглэгчид зөвхөн зарим багана, мөрийг харуулах (эрхийн хяналт)
- Хүснэгтийн бүтэц өөрчлөгдсөн ч програмд ижил интерфейс үлдээх

### Үүсгэх

```sql
CREATE OR REPLACE VIEW v_zahialgiin_dun AS
SELECT z.zahialga_id, z.hereglegch_id, z.tuluv,
       SUM(m.too * m.negj_une) AS niit_dun
FROM zahialga AS z
JOIN zahialgiin_mur AS m ON m.zahialga_id = z.zahialga_id
GROUP BY z.zahialga_id, z.hereglegch_id, z.tuluv;
```

`OR REPLACE` нь view байвал шинэ тодорхойлолтоор солино — скриптийг дахин
ажиллуулахад алдаа гарахгүй.

Ашиглах нь хүснэгттэй яг адил:

```sql
SELECT * FROM v_zahialgiin_dun WHERE niit_dun > 1000000;
```

| zahialga_id | niit_dun |
|---|---|
| 1 | 1428000.00 |
| 4 | 3200000.00 |
| 6 | 1620000.00 |
| 10 | 3289000.00 |

### Удирдах

| Үйлдэл | MySQL |
|---|---|
| Үүсгэх эсвэл солих | `CREATE OR REPLACE VIEW v AS SELECT …` |
| Устгах | `DROP VIEW IF EXISTS v` |
| Тодорхойлолт харах | `SHOW CREATE VIEW v;` |
| Бүх view | `information_schema.VIEWS` |

View дотор `ORDER BY` бичиж болох ч дуудах асуулга өөрөөр эрэмбэлбэл
түүнийх давамгайлна. Эрэмбийг view-г дуудах асуулгад бич.

### View өгөгдөл хадгалдаггүй

`baraa.une` өөрчлөгдвөл view-ийн үр дүн тэр даруй өөрчлөгдөнө. View нь
хурдасгадаггүй — доторх асуулга удаан бол view ч удаан. MySQL-д үр дүнг
хадгалдаг (materialized) view байхгүй. Үр дүнг бодитоор хадгалах бол
тусдаа тайлангийн хүснэгт үүсгэж, үе үе шинэчилнэ.

### Шинэчлэх боломжтой view

Энгийн view-ээр `UPDATE`, `INSERT`, `DELETE` хийж болно — өөрчлөлт
**суурь хүснэгтэд** очно. Нөхцөл:

- Өөрчлөлт **нэг** суурь хүснэгтэд хамаарах
- `GROUP BY`, `DISTINCT`, агрегат функц (`SUM`, `COUNT`), `UNION` байхгүй
- Өөрчлөх багана нь тооцоолсон (`too * negj_une`) биш, энгийн багана

Тиймээс `v_zahialgiin_dun` шинэчлэгдэхгүй (MySQL: алдаа 1288).

`WITH CHECK OPTION` нь view-ийн `WHERE`-ээс гадуур гарах өөрчлөлтийг
хориглоно:

```sql
CREATE OR REPLACE VIEW v_tur_uldegdel_baga AS
SELECT baraa_id, ner, uldegdel FROM baraa WHERE uldegdel < 10
WITH CHECK OPTION;

UPDATE v_tur_uldegdel_baga SET uldegdel = 50 WHERE baraa_id = 9;
-- ERROR 1369: CHECK OPTION failed
```

50 нь `uldegdel < 10` нөхцлөөс гарах тул view-ээр дамжуулж хийхийг
хориглоно — мөр view-ээс «алга болох» өөрчлөлтийг хаана.
""",
            initial_code="""\
USE delguur;

-- 1. Захиалга бүрийн нийт дүн (дахин ажиллуулж болно)
CREATE OR REPLACE VIEW v_zahialgiin_dun AS
SELECT z.zahialga_id,
       z.hereglegch_id,
       z.zahialsan_ognoo,
       z.tuluv,
       SUM(m.too * m.negj_une) AS niit_dun
FROM zahialga AS z
JOIN zahialgiin_mur AS m ON m.zahialga_id = z.zahialga_id
GROUP BY z.zahialga_id, z.hereglegch_id, z.zahialsan_ognoo, z.tuluv;

-- 2. View-г хүснэгт шиг ашиглах
SELECT zahialga_id, tuluv, niit_dun
FROM v_zahialgiin_dun
ORDER BY niit_dun DESC;

-- 3. View-г өөр хүснэгттэй JOIN хийх: цуцлагдаагүй захиалгын хэрэглэгч тус бүрийн дүн
SELECT h.ner, COUNT(*) AS zahialgyn_too, SUM(v.niit_dun) AS niit
FROM v_zahialgiin_dun AS v
JOIN hereglegch AS h ON h.hereglegch_id = v.hereglegch_id
WHERE v.tuluv <> 'Цуцлагдсан'
GROUP BY h.hereglegch_id, h.ner
ORDER BY niit DESC;

-- 4. Тодорхойлолтыг харах
SHOW CREATE VIEW v_zahialgiin_dun;

SELECT TABLE_NAME, IS_UPDATABLE
FROM information_schema.VIEWS
WHERE TABLE_SCHEMA = 'delguur';

-- 5. Шинэчлэх боломжтой энгийн view + CHECK OPTION
CREATE OR REPLACE VIEW v_tur_uldegdel_baga AS
SELECT baraa_id, ner, uldegdel
FROM baraa
WHERE uldegdel < 10
WITH CHECK OPTION;

SELECT * FROM v_tur_uldegdel_baga;

-- Өөрчлөлтийг transaction дотор хийж, дараа нь буцаана
START TRANSACTION;

UPDATE v_tur_uldegdel_baga SET uldegdel = uldegdel + 1 WHERE baraa_id = 9;
SELECT baraa_id, uldegdel FROM baraa WHERE baraa_id = 9;   -- 5: суурь хүснэгт өөрчлөгдлөө

-- Дараах мөрүүд алдаа өгнө (тайлбараас гаргаж туршаарай):
-- UPDATE v_tur_uldegdel_baga SET uldegdel = 50 WHERE baraa_id = 9;   -- 1369 CHECK OPTION
-- UPDATE v_zahialgiin_dun SET tuluv = tuluv WHERE zahialga_id = 1;   -- 1288 not updatable

ROLLBACK;

SELECT baraa_id, uldegdel FROM baraa WHERE baraa_id = 9;   -- дахин 4

-- 6. Туршилтын view-г устгана (v_zahialgiin_dun үлдэнэ)
DROP VIEW IF EXISTS v_tur_uldegdel_baga;
""",
        ),
        LessonSpec(
            title="Index: B-tree, clustered ба secondary",
            slug="index-btree-clustered",
            description="Index хэрхэн ажилладаг, нийлмэл ба бүрхэх index, бичих зардал.",
            duration=720,
            language=MY,
            content="""\
### Утасны лавлах

Утасны лавлахад «Батын Болд»-ыг хайхдаа эхнээс нь нэг нэгээр нь
уншдаггүй — **цагаан толгойн дарааллаар** шууд Б үсэг рүү очно.
Index яг ийм: баганын утгуудыг **эрэмбэлсэн** тусдаа бүтэц.

- Index-гүй: бүх мөрийг шалгана — **full scan**, O(n)
- Index-тэй: модоор доош бууна — **seek**, O(log n)

### B-tree (B+tree)

```text
                 [ 40 | 80 ]                ← root
          /           |           \\
   [10|20|30]    [50|60|70]    [90|95]      ← дотоод түвшин
      ...           ...          ...
   навч: утга + мөр рүү заагч               ← leaf
```

Сая мөртэй хүснэгтэд ч 3–4 түвшин л байдаг. MySQL InnoDB B+tree
ашиглана. Навчнууд хоорондоо холбоотой тул `BETWEEN`,
`>`, `ORDER BY` зэрэг **муж** хайлтад ч тохирно.

### Clustered ба secondary

**Clustered index** — хүснэгтийн мөрүүд **өөрөө** энэ дарааллаар
хадгалагдана. Тиймээс хүснэгт бүрт **ганц** байна.

**Secondary index** (өөр нэр нь nonclustered) — тусдаа бүтэц, навчиндаа
мөр рүү заагч хадгална. Олон байж болно.

| Асуулт | MySQL InnoDB |
|---|---|
| Clustered index хаана | **Үргэлж** PK дээр |
| PK байхгүй бол | Эхний `UNIQUE NOT NULL` index, эс бөгөөс далд 6 байт row ID |
| Өөр баганыг clustered болгох | Боломжгүй |
| Secondary index-ийн заагч | PK-ийн утга |

Secondary index-ээр мөр олсны дараа MySQL PK-ийн утгаар clustered
index-ээс бүтэн мөрийг дахин хайна.

> InnoDB-д secondary index нь PK-г агуулдаг тул урт PK (жишээ нь
> `CHAR(36)` UUID) бүх index-ийг томруулна.

### Нийлмэл index ба зүүн угтварын дүрэм

```sql
CREATE INDEX ix_baraa_angilal_une ON baraa (angilal_id, une);
```

Утасны лавлах «овог, нэр»-ээр эрэмбэлэгдсэн бол зөвхөн нэрээр хайж
чадахгүй. Үүнтэй адил:

| WHERE | Index ашиглах уу |
|---|---|
| `angilal_id = 1` | Тийм |
| `angilal_id = 1 AND une > 100000` | Тийм, хоёр багана |
| `une > 100000` | Ихэвчлэн **үгүй** — зүүн багана алга |

Тиймээс **тэнцүүгээр** шүүдэг баганыг эхэнд, мужаар шүүдгийг ард нь тавь.

### Бүрхэх (covering) index

Асуулгад хэрэгтэй **бүх** багана index-д байвал хүснэгт рүү огт
очихгүй — хамгийн хурдан.

```sql
-- Хэрэгтэй баганыг index-ийн төгсгөлд нэмнэ. EXPLAIN-д "Using index" гарна
CREATE INDEX ix_baraa_angilal_une_ner ON baraa (angilal_id, une, ner);
```

InnoDB-ийн secondary index PK-г аль хэдийн агуулдаг тул `baraa_id`-г
нэмэх шаардлагагүй — `SELECT baraa_id, une … WHERE angilal_id = 1` ч
бүрхэгдэнэ.

### Синтакс

| Үйлдэл | MySQL |
|---|---|
| Үүсгэх | `CREATE [UNIQUE] INDEX ix ON t (c);` |
| Өөр хэлбэр | `ALTER TABLE t ADD INDEX ix (c);` |
| Устгах | `DROP INDEX ix ON t;` |
| Өөр хэлбэр | `ALTER TABLE t DROP INDEX ix;` |
| Жагсаах | `SHOW INDEX FROM t;` |

> MySQL-д `DROP INDEX IF EXISTS` **байхгүй** (MariaDB-д бий) — байхгүй
> index-ийг устгавал алдаа. Мөн MySQL FK баганад index-ийг автоматаар
> үүсгэдэг (Модул 8).

### Үнэгүй биш

- `INSERT`, `DELETE` бүр **бүх** index-ийг шинэчилнэ; `UPDATE` нь өөрчлөгдсөн
  баганатай index-ийг шинэчилнэ
- Диск, санах ой эзэлнэ
- Сонголт тааруу index-ийг optimizer ашиглахгүй ч зардал нь үлдэнэ

**Index тавих нь зүйтэй:** `WHERE`, `JOIN ... ON`, `ORDER BY`-д байнга
орж, олон ялгаатай утгатай багана. **Эргэлзээтэй:** цөөн утгатай
(`tuluv` шиг) багана дангаараа, байнга бичигддэг жижиг хүснэгт.
""",
            initial_code="""\
USE delguur;

DROP TABLE IF EXISTS tur_baraa;

-- 1. baraa-г хуулна. CREATE TABLE ... AS SELECT нь PK, index-ийг хуулдаггүй
CREATE TABLE tur_baraa AS SELECT * FROM baraa;
SHOW INDEX FROM tur_baraa;              -- хоосон

-- 2. PK нэмэхэд InnoDB түүн дээр clustered index үүсгэнэ
ALTER TABLE tur_baraa ADD PRIMARY KEY (baraa_id);
SHOW INDEX FROM tur_baraa;              -- Key_name = PRIMARY

-- Анхны хүснэгтэд FK багана angilal_id дээр автомат index бий
SHOW INDEX FROM baraa;

-- 3. Index-гүй: type = ALL (бүх мөрийг уншина)
EXPLAIN SELECT * FROM tur_baraa WHERE angilal_id = 1;

-- 4. Нийлмэл index
CREATE INDEX ix_tur_baraa_angilal_une ON tur_baraa (angilal_id, une);

-- type = ref эсвэл range болно
-- (12 мөртэй жижиг хүснэгтэд optimizer заримдаа ALL-ыг сонгож болно)
EXPLAIN SELECT * FROM tur_baraa WHERE angilal_id = 1;
EXPLAIN SELECT * FROM tur_baraa WHERE angilal_id = 1 AND une > 100000;

-- 5. Зүүн угтварын дүрэм: зөвхөн une-ээр шүүвэл index-ийн түлхүүрээр хайж чадахгүй
EXPLAIN SELECT * FROM tur_baraa WHERE une > 100000;

-- 6. Бүрхэх index: хэрэгтэй бүх багана index-д байна
-- Extra баганад Using index гэж гарна
EXPLAIN SELECT angilal_id, une FROM tur_baraa WHERE angilal_id = 1;

-- 7. Устгах хоёр арга
DROP INDEX ix_tur_baraa_angilal_une ON tur_baraa;

ALTER TABLE tur_baraa ADD INDEX ix_tur_baraa_ner (ner);
ALTER TABLE tur_baraa DROP INDEX ix_tur_baraa_ner;

SHOW INDEX FROM tur_baraa;

-- 8. Цэвэрлэгээ
DROP TABLE IF EXISTS tur_baraa;
""",
        ),
        LessonSpec(
            title="EXPLAIN — гүйцэтгэлийн төлөвлөгөө",
            slug="explain-execution-plan",
            description="Асуулга index ашиглаж байгаа эсэхийг EXPLAIN-ээр шалгах, sargable нөхцөл.",
            duration=720,
            language=MY,
            content="""\
Асуулга удаан байвал таамаглах биш **серверээс асуу**: «Энэ асуулгыг
яаж гүйцэтгэх гэж байна?» Хариулт нь **гүйцэтгэлийн төлөвлөгөө**
(execution plan). MySQL-д үүнийг `EXPLAIN` харуулна.

### EXPLAIN

```sql
EXPLAIN SELECT * FROM zahialga WHERE hereglegch_id = 1;
```

Асуулгын өмнө `EXPLAIN` гэж бичихэд асуулга **ажиллахгүй** — зөвхөн
төлөвлөгөөг хүснэгтээр буцаана. Хамгийн чухал баганууд:

| Багана | Утга |
|---|---|
| `type` | Хандах арга (доорх хүснэгт) |
| `possible_keys` | Ашиглаж болох index-үүд |
| `key` | Сонгосон index (`NULL` = index-гүй) |
| `rows` | Шалгах гэж буй мөрийн **тооцоолол** |
| `Extra` | `Using index` (бүрхэх), `Using filesort` (нэмэлт эрэмбэлэлт), `Using temporary` (түр хүснэгт) |

`type`-ийн утгууд, **сайнаас муу руу**:

| type | Утга |
|---|---|
| `const` | PK/UNIQUE-ээр яг нэг мөр |
| `eq_ref` | JOIN-д мөр бүрт UNIQUE-ээр нэг мөр |
| `ref` | Index-ээр тэнцүү утга хайх (олон мөр байж болно) |
| `range` | Index-ээр муж (`BETWEEN`, `>`, `IN`) |
| `index` | Бүтэн index-ийг уншина |
| `ALL` | Бүтэн хүснэгтийг уншина — том хүснэгтэд аюул |

### FORMAT=TREE ба EXPLAIN ANALYZE

```sql
-- MySQL 8.0.16+: модон хэлбэр — дотроосоо гадагш уншина
EXPLAIN FORMAT=TREE SELECT * FROM zahialga WHERE hereglegch_id = 1;

-- MySQL 8.0.18+: асуулгыг БОДИТООР ажиллуулж, бодит хугацаа ба мөрийн тоог харуулна
EXPLAIN ANALYZE SELECT * FROM zahialga WHERE hereglegch_id = 1;
```

Модон хэлбэрийн мөр бүрт `cost` (тооцоолсон зардал) ба `rows` байна.
`EXPLAIN ANALYZE` нэмээд `actual time` ба бодит `rows`-ыг харуулна.
Тооцоолсон ба бодит мөрийн тоо их зөрвөл статистик хуучирсан байж
магадгүй.

> `EXPLAIN ANALYZE` асуулгыг үнэхээр гүйцэтгэдэг тул удаан асуулгад
> удаан л ажиллана.

### Статистик ба ANALYZE TABLE

Optimizer аль замыг сонгохоо хүснэгтийн **статистикаар** (хэдэн мөр,
утга хэр олон янз) шийднэ. Их хэмжээний өгөгдөл нэг дор оруулсны дараа
статистик хоцрох тул:

```sql
ANALYZE TABLE tur_zahialga;
```

Энэ нь өгөгдлийг өөрчлөхгүй, зөвхөн статистикийг шинэчилнэ.

### Sargable нөхцөл

**Sargable** (Search ARGument ABLE) — index-ээр **хайж** (`range`, `ref`)
болох нөхцөл. Гол дүрэм: **баганыг функц, тооцоонд бүү ороо**.

| Муу (бүтэн уншина) | Сайн (index-ээр хайна) |
|---|---|
| `YEAR(zahialsan_ognoo) = 2024` | `zahialsan_ognoo >= '2024-01-01' AND zahialsan_ognoo < '2025-01-01'` |
| `une * 1.1 > 110000` | `une > 100000` |
| `ner LIKE '%цамц'` | `ner LIKE 'Ноосон%'` |
| `UPPER(email) = 'BOLD@EXAMPLE.MN'` | `email = 'bold@example.mn'` (collation нь том жижиг үсэг ялгахгүй тул) |

Index нь **баганын утгаар** эрэмбэлэгдсэн. `YEAR(zahialsan_ognoo)`-ийн
утга index-д байхгүй тул MySQL мөр бүрт функцийг тооцоолох хэрэгтэй
болно.

Мөн **төрөл зөрүүлэхээс** болгоомжил: `VARCHAR` баганыг тоотой
харьцуулбал (`utas = 99112233`) мөр бүрийн текстийг тоо болгох тул index
ашиглагдахгүй — `utas = '99112233'` гэж бич.

> Функцээр шүүх зайлшгүй бол MySQL 8.0.13+ **функцэн index**:
> `CREATE INDEX ix ON zahialga ((DATE(zahialsan_ognoo)));` — давхар хаалт
> заавал. Одоо `WHERE DATE(zahialsan_ognoo) = '2024-03-09'` index ашиглана.

### Энэ хичээлийн код

`delguur`-ийн 10 захиалга хэтэрхий цөөн — ийм жижиг хүснэгтэд optimizer
index байсан ч бүтэн уншихыг сонгодог (хямд зам). Тиймээс код эхлээд
`zahialga`-г `CROSS JOIN`-оор (Модул 9) өөртэй нь хоёр удаа үржүүлж
**1 000 мөртэй** туршилтын хүснэгт үүсгэнэ. Огноо давхцахгүйн тулд мөр
бүрт өөр өдөр нэмнэ (`+ INTERVAL … DAY`, Модул 4).
""",
            initial_code="""\
USE delguur;

-- 0. Туршилтын хүснэгт: zahialga-г 1 000 мөртэй болгоно
DROP TABLE IF EXISTS tur_zahialga;

CREATE TABLE tur_zahialga (
    zahialga_id     INT AUTO_INCREMENT PRIMARY KEY,
    hereglegch_id   INT NOT NULL,
    zahialsan_ognoo DATETIME NOT NULL,
    tuluv           VARCHAR(20) NOT NULL
);

-- 10 x 10 x 10 = 1000 мөр: CROSS JOIN-оор олшруулж, огноог өдрөөр тараана
INSERT INTO tur_zahialga (hereglegch_id, zahialsan_ognoo, tuluv)
SELECT a.hereglegch_id,
       a.zahialsan_ognoo + INTERVAL (b.zahialga_id * 10 + c.zahialga_id) DAY,
       a.tuluv
FROM zahialga AS a
CROSS JOIN zahialga AS b
CROSS JOIN zahialga AS c;

-- Optimizer-ийн статистикийг шинэчилнэ
ANALYZE TABLE tur_zahialga;

-- 1. Index-гүй: type = ALL, rows = 1000 (бүх мөрийг уншина)
EXPLAIN SELECT zahialga_id, zahialsan_ognoo
FROM tur_zahialga
WHERE zahialsan_ognoo >= '2024-03-01' AND zahialsan_ognoo < '2024-04-01';

-- 2. Огноон дээр index
CREATE INDEX ix_tur_zahialga_ognoo ON tur_zahialga (zahialsan_ognoo);

-- 3. Sargable муж: type = range, key = ix_tur_zahialga_ognoo, rows = 74
EXPLAIN SELECT zahialga_id, zahialsan_ognoo
FROM tur_zahialga
WHERE zahialsan_ognoo >= '2024-03-01' AND zahialsan_ognoo < '2024-04-01';

-- 4. Sargable биш: баганыг функцэд оруулсан тул type = index,
--    rows = 1000 — index-ийг бүтнээр нь уншина
EXPLAIN SELECT zahialga_id, zahialsan_ognoo
FROM tur_zahialga
WHERE YEAR(zahialsan_ognoo) = 2024 AND MONTH(zahialsan_ognoo) = 3;

-- 5. PK-ээр: type = const, rows = 1
EXPLAIN SELECT * FROM tur_zahialga WHERE zahialga_id = 5;

-- 6. Index-гүй баганаар: type = ALL
EXPLAIN SELECT zahialga_id FROM tur_zahialga WHERE hereglegch_id = 1;

-- 7. Модон хэлбэр
EXPLAIN FORMAT=TREE
SELECT zahialga_id FROM tur_zahialga
WHERE zahialsan_ognoo >= '2024-03-01' AND zahialsan_ognoo < '2024-04-01';

-- 8. EXPLAIN ANALYZE: бодитоор ажиллуулж, actual time ба rows-ыг харуулна
EXPLAIN ANALYZE
SELECT COUNT(*) FROM tur_zahialga
WHERE zahialsan_ognoo >= '2024-03-01' AND zahialsan_ognoo < '2024-04-01';

-- 9. Функцэн index: DATE(...) дээр index тавибал type = ref болно
CREATE INDEX ix_tur_zahialga_udur ON tur_zahialga ((DATE(zahialsan_ognoo)));
EXPLAIN SELECT zahialga_id FROM tur_zahialga WHERE DATE(zahialsan_ognoo) = '2024-03-09';

-- 10. Цэвэрлэгээ
DROP TABLE IF EXISTS tur_zahialga;
""",
        ),
    ],
)

TRANSACTIONS = ModuleSpec(
    title="Модул 14 — Transaction ба түгжээ",
    description="ACID, тусгаарлалтын түвшин, түгжээ ба deadlock.",
    lessons=[
        LessonSpec(
            title="Transaction: ACID, COMMIT, ROLLBACK",
            slug="transaction-acid-savepoint",
            description="Олон өөрчлөлтийг нэг бүхэл үйлдэл болгох, savepoint, далд COMMIT.",
            duration=660,
            language=MY,
            content="""\
**Transaction** гэдэг нь «бүгд амжилттай, эсвэл юу ч болоогүй» гэж
үзэх SQL мэдэгдлүүдийн бүлэг.

Жишээ: агуулахын засвараар 1-р бараанаас 5 ширхгийг хасч, 3-р бараанд
нэмэх. Хасалт амжаад нэмэлт нь алдаа өгвөл 5 ширхэг «алга болно».
Transaction үүнээс сэргийлнэ.

### ACID

| Үсэг | Нэр | Утга |
|---|---|---|
| **A** | Atomicity | Бүх мэдэгдэл хэрэгжинэ, эсвэл бүгд буцна |
| **C** | Consistency | PK, FK, CHECK зэрэг дүрэм хэзээ ч зөрчигдөхгүй |
| **I** | Isolation | Зэрэг ажиллаж буй transaction-ууд бие биедээ саад болохгүй |
| **D** | Durability | `COMMIT` хийсэн өөрчлөлт сервер унасан ч үлдэнэ (log-д бичигдсэн) |

MySQL-д transaction-ийг **InnoDB** хүснэгт дэмжинэ (8.0-ийн анхдагч).

### Синтакс

| Үйлдэл | MySQL |
|---|---|
| Эхлүүлэх | `START TRANSACTION;` (эсвэл `BEGIN;`) |
| Батлах | `COMMIT;` |
| Бүгдийг буцаах | `ROLLBACK;` |
| Savepoint тавих | `SAVEPOINT sp1;` |
| Savepoint хүртэл буцаах | `ROLLBACK TO SAVEPOINT sp1;` |
| Savepoint чөлөөлөх | `RELEASE SAVEPOINT sp1;` |

```sql
START TRANSACTION;
UPDATE baraa SET uldegdel = uldegdel - 5 WHERE baraa_id = 1;
UPDATE baraa SET uldegdel = uldegdel + 5 WHERE baraa_id = 3;
COMMIT;
```

### Autocommit

MySQL анхдагчаар **autocommit** горимд ажиллана: мэдэгдэл бүр өөрийн
transaction болж, дуусмагц автоматаар батлагдана. `START TRANSACTION`
энэ горимыг тухайн transaction дуустал түр зогсооно.

| | |
|---|---|
| Одоогийн утга | `SELECT @@autocommit;` → `1` |
| Унтраах | `SET autocommit = 0;` |
| Унтраасны дараа | Эхний мэдэгдэл transaction нээж, `COMMIT`/`ROLLBACK` хүртэл нээлттэй |

`@@autocommit` нь серверийн **тохиргооны хувьсагч**, `SET` түүнийг энэ
холболтод өөрчилнө (хувьсагчийг Модул 16-д нарийн үзнэ).

> Autocommit унтраагаад `COMMIT`-оо мартвал түгжээ удаан барьж, холболт
> тасрахад бүх ажил **буцна**.

### Далд COMMIT — MySQL-ийн гол урхи

Дараах мэдэгдлүүд нээлттэй transaction-ийг **автоматаар COMMIT** хийнэ —
өмнөх өөрчлөлтүүд батлагдаж, `ROLLBACK` тэднийг буцааж чадахгүй:

- DDL: `CREATE TABLE`, `ALTER TABLE`, `DROP TABLE`, `TRUNCATE TABLE`
  (Модул 7), `CREATE INDEX`
- Шинэ `START TRANSACTION` (эсвэл `BEGIN`)
- `SET autocommit = 1`

MySQL-д **үүрлэсэн transaction байхгүй**: transaction дотор дахин
`START TRANSACTION` бичвэл эхнийх нь батлагдаад шинэ transaction эхэлнэ.
Хэсэгчлэн буцаах хэрэгтэй бол savepoint ашигла.

### Алдаа гарвал

Ихэнх алдаа (жишээ нь CHECK зөрчил, давхардсан түлхүүр) зөвхөн **тухайн
мэдэгдлийг** буцааж, transaction нээлттэй үлдэнэ. Юу хийхийг — `COMMIT`
эсвэл `ROLLBACK` — та (эсвэл програм) шийднэ. Deadlock (энэ модулийн
сүүлийн хичээл) бол эсрэгээрээ transaction-ийг **бүхэлд нь** буцаадаг.

> Энэ сайт дээр алдаа гармагц скрипт зогсоно. Ажиллуулалт бүр шинэ
> холболтоор эхэлдэг тул нээлттэй үлдсэн transaction дараагийн
> ажиллуулалтад нөлөөлөхгүй.

### Savepoint — хэсэгчлэн буцаах

```text
START ─ UPDATE 1 ─ UPDATE 3 ─ SAVEPOINT sp ─ UPDATE 8 ─ ROLLBACK TO sp ─ ROLLBACK
                                             └──── энэ л буцна ────┘
```

Savepoint нь transaction-ийг **дуусгадаггүй** — эцэст нь `COMMIT` эсвэл
`ROLLBACK` заавал хэрэгтэй.
""",
            initial_code="""\
USE delguur;

-- 1. Эхний төлөв: 15, 40, 100
SELECT baraa_id, ner, uldegdel FROM baraa WHERE baraa_id IN (1, 3, 8);
SELECT @@autocommit AS autocommit;                             -- 1

-- 2. Үлдэгдэл шилжүүлэх transaction
START TRANSACTION;

UPDATE baraa SET uldegdel = uldegdel - 5 WHERE baraa_id = 1;
UPDATE baraa SET uldegdel = uldegdel + 5 WHERE baraa_id = 3;

SELECT baraa_id, uldegdel FROM baraa WHERE baraa_id IN (1, 3, 8);   -- 10, 45, 100

-- 3. Savepoint тавиад дахин өөрчлөх
SAVEPOINT sp_aguulah;

UPDATE baraa SET uldegdel = 0 WHERE baraa_id = 8;
SELECT baraa_id, uldegdel FROM baraa WHERE baraa_id IN (1, 3, 8);   -- 10, 45, 0

-- 4. Зөвхөн savepoint-оос хойшхийг буцаана — transaction нээлттэй хэвээр
ROLLBACK TO SAVEPOINT sp_aguulah;
SELECT baraa_id, uldegdel FROM baraa WHERE baraa_id IN (1, 3, 8);   -- 10, 45, 100

-- 5. Бүгдийг буцаана: өгөгдөл анхны байдалдаа орно
ROLLBACK;
SELECT baraa_id, uldegdel FROM baraa WHERE baraa_id IN (1, 3, 8);   -- 15, 40, 100

-- 6. Үүрлэсэн transaction байхгүй: хоёр дахь START TRANSACTION эхнийхийг батална
START TRANSACTION;
UPDATE baraa SET uldegdel = uldegdel + 1 WHERE baraa_id = 8;   -- 101
START TRANSACTION;                                             -- далд COMMIT!
ROLLBACK;                                                      -- юу ч буцаахгүй
SELECT uldegdel FROM baraa WHERE baraa_id = 8;                 -- 101

-- 7. DDL-ийн далд COMMIT: CREATE TABLE өмнөх өөрчлөлтийг батална
START TRANSACTION;
UPDATE baraa SET uldegdel = uldegdel - 1 WHERE baraa_id = 8;   -- 100
CREATE TABLE tur_ddl (id INT);                                 -- далд COMMIT!
ROLLBACK;
SELECT uldegdel FROM baraa WHERE baraa_id = 8;                 -- 100: буцаагүй
DROP TABLE tur_ddl;

-- 8. autocommit = 0: эхний мэдэгдэл өөрөө transaction нээнэ
SET autocommit = 0;
UPDATE baraa SET uldegdel = uldegdel + 1 WHERE baraa_id = 8;   -- 101
ROLLBACK;                                                      -- буцна
SET autocommit = 1;

SELECT baraa_id, uldegdel FROM baraa WHERE baraa_id IN (1, 3, 8);   -- 15, 40, 100
""",
        ),
        LessonSpec(
            title="Тусгаарлалтын түвшин ба аномали",
            slug="isolation-level-anomali",
            description="Dirty read, non-repeatable read, phantom ба тэдгээрээс сэргийлэх түвшин.",
            duration=720,
            language=MY,
            content="""\
Олон хэрэглэгч зэрэг ажиллахад нэг transaction нөгөөгийнхөө
өөрчлөлтийг **хэзээ** харах вэ? Үүнийг **isolation level** тодорхойлно.

### Гурван аномали

| Аномали | Юу болох вэ |
|---|---|
| **Dirty read** | B-гийн **батлаагүй** өөрчлөлтийг A уншина. B `ROLLBACK` хийвэл A байхгүй өгөгдөл харсан болно |
| **Non-repeatable read** | A нэг мөрийг хоёр уншихад дунд нь B **батлаад** өөрчилсөн тул утга өөр |
| **Phantom read** | A ижил нөхцөлөөр хоёр уншихад дунд нь B мөр нэмсэн/өөрчилсөн тул **мөрийн тоо** өөр |

### Дөрвөн түвшин (SQL стандарт)

| Түвшин | Dirty | Non-repeatable | Phantom |
|---|---|---|---|
| `READ UNCOMMITTED` | Болно | Болно | Болно |
| `READ COMMITTED` | Үгүй | Болно | Болно |
| `REPEATABLE READ` | Үгүй | Үгүй | Болно |
| `SERIALIZABLE` | Үгүй | Үгүй | Үгүй |

Түвшин өндөр байх тусам аюулгүй, гэхдээ түгжээ/хүлээлт ихэснэ.

### MySQL InnoDB-ийн хэрэгжүүлэлт

| | MySQL (InnoDB) |
|---|---|
| Анхдагч түвшин | **REPEATABLE READ** |
| Энгийн `SELECT` | MVCC snapshot — бичигчийг **хүлээхгүй** |
| Одоогийн түвшин | `SELECT @@transaction_isolation;` эсвэл `SHOW VARIABLES LIKE 'transaction_isolation';` |

**MVCC** (multi-version concurrency control): InnoDB өөрчлөгдсөн мөрийн
хуучин хувилбарыг түр хадгалдаг. Уншигч батлагдаагүй өөрчлөлтийг хүлээх
биш, өөрт харагдах ёстой **хувилбарыг** уншина.

InnoDB-ийн онцлог: `REPEATABLE READ`-д энгийн `SELECT` нь transaction-ийн
**эхний уншилтын үеийн snapshot**-ыг хардаг тул phantom ч харагдахгүй.
`FOR UPDATE` зэрэг түгжих уншилтад (дараагийн хичээл) next-key lock
ашиглана.

### Түвшин тохируулах

```sql
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;          -- ЗӨВХӨН дараагийн transaction
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;  -- сессийн турш
SET GLOBAL TRANSACTION ISOLATION LEVEL READ COMMITTED;   -- шинэ холболтуудад
```

`GLOBAL`-д серверийн админы эрх хэрэгтэй.

> MySQL-д нээлттэй transaction дотор түвшин солих гэвэл 1568 алдаа
> гарна. `START TRANSACTION`-оос **өмнө** тохируул.

### Дасгал: хоёр сесс

Хоёр **тусдаа холболт** нээ (хоёр `mysql` цонх, эсвэл Workbench-д
холболтыг хоёр удаа нээх).

> Энэ сайтын «Код ажиллуулах» нэг л холболт нээдэг тул хоёр сессийн
> дасгалыг өөрийн компьютер дээрх MySQL-д (Модул 1) хий. Анхны кодыг энд
> ажиллуулбал зөвхөн сесс A-гийн тал харагдана.

**Туршилт 1 — dirty read**

| Алхам | Сесс A | Сесс B |
|---|---|---|
| 1 | `SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;` `START TRANSACTION;` | |
| 2 | | `START TRANSACTION;` `UPDATE baraa SET uldegdel = 0 WHERE baraa_id = 3;` |
| 3 | `SELECT uldegdel FROM baraa WHERE baraa_id = 3;` → **0** (бохир!) | |
| 4 | | `ROLLBACK;` |
| 5 | Дахин `SELECT` → **40**. `COMMIT;` | |

`READ COMMITTED`-ээр давтвал 3-р алхамд MySQL шууд **40** буцаана — B-г
хүлээхгүй, батлагдсан сүүлийн хувилбарыг уншина (MVCC).

**Туршилт 2 — non-repeatable read**

| Алхам | Сесс A | Сесс B |
|---|---|---|
| 1 | `READ COMMITTED` тохируулаад `START TRANSACTION;` `SELECT` → 40 | |
| 2 | | `UPDATE baraa SET uldegdel = uldegdel + 10 WHERE baraa_id = 3;` |
| 3 | `SELECT` → **50** (өөрчлөгдлөө). `COMMIT;` | |
| 4 | | Буцаах: `UPDATE baraa SET uldegdel = uldegdel - 10 WHERE baraa_id = 3;` |

`REPEATABLE READ`-ээр давтвал 3-р алхамд A хуучин утгаа харна.

**Туршилт 3 — phantom:** A нь `SELECT COUNT(*) FROM baraa WHERE uldegdel = 0;`
(2) гэж уншина; B нь `UPDATE baraa SET uldegdel = 0 WHERE baraa_id = 12;`
хийнэ; A дахин тоолно. `READ COMMITTED` → 3, InnoDB `REPEATABLE READ` → 2.
Эцэст нь B-д `UPDATE baraa SET uldegdel = 9 WHERE baraa_id = 12;` гэж буцаа.
""",
            initial_code="""\
USE delguur;

-- Энэ скрипт бол СЕСС A. Тайлбарт СЕСС B гэж бичсэн мөрийг
-- өөр холболтод ажиллуул. B байхгүй бол зүгээр л ижил утга харагдана.

-- 1. Одоогийн түвшин (анхдагч REPEATABLE-READ)
SHOW VARIABLES LIKE 'transaction_isolation';

-- 2. READ COMMITTED: батлагдсан шинэ утгыг transaction дундуур харна
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
SHOW VARIABLES LIKE 'transaction_isolation';

START TRANSACTION;
SELECT baraa_id, uldegdel FROM baraa WHERE baraa_id = 3;     -- 40

-- СЕСС B: UPDATE baraa SET uldegdel = uldegdel + 10 WHERE baraa_id = 3;

SELECT baraa_id, uldegdel FROM baraa WHERE baraa_id = 3;     -- 50 (non-repeatable read)
COMMIT;

-- 3. REPEATABLE READ: transaction дотор snapshot тогтмол
SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;

START TRANSACTION;
SELECT baraa_id, uldegdel FROM baraa WHERE baraa_id = 3;     -- 50

-- СЕСС B (буцаах): UPDATE baraa SET uldegdel = uldegdel - 10 WHERE baraa_id = 3;

SELECT baraa_id, uldegdel FROM baraa WHERE baraa_id = 3;     -- 50 хэвээр
COMMIT;

SELECT baraa_id, uldegdel FROM baraa WHERE baraa_id = 3;     -- 40: шинэ transaction

-- 4. Phantom-ийг InnoDB REPEATABLE READ харуулахгүй
START TRANSACTION;
SELECT COUNT(*) AS uldegdelgui FROM baraa WHERE uldegdel = 0;   -- 2

-- СЕСС B: UPDATE baraa SET uldegdel = 0 WHERE baraa_id = 12;

SELECT COUNT(*) AS uldegdelgui FROM baraa WHERE uldegdel = 0;   -- 2 хэвээр
COMMIT;

-- СЕСС B (буцаах): UPDATE baraa SET uldegdel = 9 WHERE baraa_id = 12;

-- 5. Зөвхөн ДАРААГИЙН нэг transaction-д түвшин өгөх
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
START TRANSACTION READ ONLY;
SELECT COUNT(*) AS niit_baraa FROM baraa;
COMMIT;

-- 6. Анхдагч руу буцаах
SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SHOW VARIABLES LIKE 'transaction_isolation';
""",
        ),
        LessonSpec(
            title="Түгжээ ба deadlock",
            slug="lock-ba-deadlock",
            description="Мөрийн түгжээ, FOR UPDATE, NOWAIT, SKIP LOCKED, deadlock үүсэх ба сэргийлэх.",
            duration=720,
            language=MY,
            content="""\
Transaction-ууд нэг мөрийг зэрэг өөрчлөхгүйн тулд сервер **түгжээ**
(lock) ашиглана.

> Deadlock, хүлээлтийн дасгалд хоёр холболт хэрэгтэй — өөрийн компьютер
> дээрх MySQL-д (Модул 1) хий. Анхны кодыг энд ажиллуулбал нэг сессийн
> түгжээг `performance_schema.data_locks`-оос харна.

### Хоёр үндсэн түгжээ

| Түгжээ | Хэзээ | Бусад S авах | Бусад X авах |
|---|---|---|---|
| **Shared (S)** | Унших | Болно | Хүлээнэ |
| **Exclusive (X)** | `UPDATE`, `DELETE`, `INSERT` | Хүлээнэ | Хүлээнэ |

X түгжээ transaction **дуустал** (`COMMIT`/`ROLLBACK`) барина. Тиймээс
урт transaction = бусдыг удаан хүлээлгэх.

### Түгжээний хэмжээ

| | MySQL InnoDB |
|---|---|
| Нэгж | Мөр (index-ийн бичлэг), завсар (gap) |
| Хүснэгтийн түвшинд | Мөр түгжихээс өмнө хүснэгтэд «санаа» түгжээ (`IX`, `IS`) тавина |
| Index-гүй `WHERE` | Уншсан **бүх** мөрийг түгжинэ |
| Энгийн `SELECT` | Түгжихгүй (snapshot, өмнөх хичээл) |

> `WHERE` дахь баганад index байхгүй бол InnoDB бүх хүснэгтийг бараг
> түгжсэнтэй адил болно. Index нь зөвхөн хурд биш, **зэрэгцээ ажил**-д ч чухал.

### «Уншаад дараа нь бичих» асуудал

Хоёр худалдан авагч сүүлийн ширхэгийг зэрэг авах гэж байна:
хоёулаа `uldegdel = 1` гэж уншаад, хоёулаа хасвал `-1` болно.
Шийдэл: уншихдаа **бичих зорилготой түгжих**.

```sql
START TRANSACTION;
SELECT uldegdel FROM baraa WHERE baraa_id = 9 FOR UPDATE;
UPDATE baraa SET uldegdel = uldegdel - 1 WHERE baraa_id = 9;
COMMIT;
```

`FOR UPDATE` нь уншсан мөрт X түгжээ тавина — өөр transaction тэр мөрийг
`FOR UPDATE`-ээр унших, өөрчлөх гэвэл бидний `COMMIT`-ийг хүлээнэ.

| Хэрэгцээ | MySQL 8 |
|---|---|
| Бичихээр түгжиж унших | `SELECT ... FOR UPDATE` |
| Дуустал shared түгжих | `SELECT ... FOR SHARE` |
| Хүлээхгүй, шууд алдаа | `FOR UPDATE NOWAIT` (алдаа 3572) |
| Түгжигдсэн мөрийг алгасах | `FOR UPDATE SKIP LOCKED` — ажлын дараалалд тохиромжтой |
| Хүлээх хугацаа | `innodb_lock_wait_timeout` = 50 сек |
| Хугацаа хэтэрвэл | Алдаа **1205** |
| Түгжээ харах | `performance_schema.data_locks` |

> `FOR UPDATE` зөвхөн transaction дотор утгатай. Autocommit горимд
> мэдэгдэл дуусмагц түгжээ суларна.

### Deadlock

Хоёр transaction бие биенийхээ түгжээг хүлээж, хэн нь ч урагшлахгүй:

| Алхам | Сесс A | Сесс B |
|---|---|---|
| 1 | `START TRANSACTION;` `UPDATE baraa SET uldegdel = uldegdel - 1 WHERE baraa_id = 1;` | |
| 2 | | `START TRANSACTION;` `UPDATE baraa SET uldegdel = uldegdel - 1 WHERE baraa_id = 3;` |
| 3 | `UPDATE baraa ... WHERE baraa_id = 3;` → B-г **хүлээнэ** | |
| 4 | | `UPDATE baraa ... WHERE baraa_id = 1;` → **DEADLOCK** |
| 5 | Үргэлжилнэ → `ROLLBACK;` | Алдаа авч, transaction бүхэлдээ буцсан |

```text
ERROR 1213 (40001): Deadlock found when trying to get lock;
try restarting transaction
```

InnoDB тойргийг өөрөө илрүүлж, нэгийг нь **хохирогч** (victim) болгон
буцаана — ихэвчлэн цөөн мөр өөрчилсөн, буцаахад хямд transaction-ийг.

> **Хоёр алдааг ялга:** **1205** — lock wait timeout: зөвхөн тухайн
> мэдэгдэл буцна, transaction нээлттэй. **1213** — deadlock: transaction
> **бүхэлдээ** буцсан.

Шинжлэх: `SHOW ENGINE INNODB STATUS;`-ийн `LATEST DETECTED DEADLOCK` хэсэг
хамгийн сүүлийн deadlock-ийн хоёр transaction, түгжээг харуулна.

### Сэргийлэх

1. **Тогтмол дараалал** — мөрүүдийг үргэлж ижил дарааллаар түгж
   (жишээ нь `baraa_id` өсөхөөр). Дээрх жишээнд B ч 1-ээс эхэлсэн бол
   deadlock болохгүй, зүгээр л хүлээнэ.
2. **Богино transaction** — дотор нь хэрэглэгчийн оролт, API дуудлага
   бүү хүлээ.
3. **Index** — цөөн мөр түгжигдэнэ.
4. **Дахин оролдох** — 1213 / 1205 авбал програм transaction-ийг бүхлээр
   нь дахин ажиллуулна. Deadlock-ийг бүрэн арилгах боломжгүй.
""",
            initial_code="""\
USE delguur;

-- 1. Түгжээний тохиргоо
SHOW VARIABLES LIKE 'innodb_lock_wait_timeout';     -- анхдагч 50

-- 2. Deadlock дасгал (хоёр холболт нээж алхам алхмаар):
--   A: START TRANSACTION;
--   A: UPDATE baraa SET uldegdel = uldegdel - 1 WHERE baraa_id = 1;
--   B: START TRANSACTION;
--   B: UPDATE baraa SET uldegdel = uldegdel - 1 WHERE baraa_id = 3;
--   A: UPDATE baraa SET uldegdel = uldegdel + 1 WHERE baraa_id = 3;   -- хүлээнэ
--   B: UPDATE baraa SET uldegdel = uldegdel + 1 WHERE baraa_id = 1;   -- ERROR 1213
--   A: ROLLBACK;
-- Дараа нь: SHOW ENGINE INNODB STATUS;  -- LATEST DETECTED DEADLOCK хэсэг

-- 3. Тогтмол дарааллаар түгжих (deadlock-оос сэргийлнэ)
START TRANSACTION;

SELECT baraa_id, ner, uldegdel
FROM baraa
WHERE baraa_id IN (1, 3)
ORDER BY baraa_id
FOR UPDATE;

-- Одоо барьж буй түгжээнүүд: хүснэгтэд IX, мөр бүрт X
SELECT OBJECT_NAME, INDEX_NAME, LOCK_TYPE, LOCK_MODE, LOCK_STATUS, LOCK_DATA
FROM performance_schema.data_locks
WHERE OBJECT_SCHEMA = 'delguur';

-- Энэ үед СЕСС B-д туршаарай:
--   SELECT uldegdel FROM baraa WHERE baraa_id = 1;                           -- шууд: snapshot
--   SELECT uldegdel FROM baraa WHERE baraa_id = 1 FOR UPDATE;                -- хүлээнэ
--   SELECT uldegdel FROM baraa WHERE baraa_id = 1 FOR UPDATE NOWAIT;         -- ERROR 3572
--   SELECT baraa_id FROM baraa WHERE baraa_id IN (1, 2, 3) FOR UPDATE SKIP LOCKED;   -- зөвхөн 2

-- Үлдэгдэл шилжүүлэх
UPDATE baraa SET uldegdel = uldegdel - 1 WHERE baraa_id = 1;
UPDATE baraa SET uldegdel = uldegdel + 1 WHERE baraa_id = 3;
SELECT baraa_id, uldegdel FROM baraa WHERE baraa_id IN (1, 3);   -- 14, 41

-- 4. Жишээ өгөгдлийг хэвээр үлдээхийн тулд буцаана; түгжээ суларна
ROLLBACK;
""",
        ),
    ],
)

SQL_DESIGN_MODULES = [DESIGN, VIEWS_INDEXES, TRANSACTIONS]
