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
