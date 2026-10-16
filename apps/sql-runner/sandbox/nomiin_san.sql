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
