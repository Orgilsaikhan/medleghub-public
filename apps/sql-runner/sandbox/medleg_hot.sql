-- medleg_hot жишээ сан: «МедлегХот» хотын цагдаагийн бүртгэл. MySQL 8.0.31+.
-- «Өгөгдлийн Сангийн Үндэс (MySQL)» сургалтын мөрдөгчийн хэргүүд энэ сан
-- дээр ажиллана (apps/api/app/content/sql/cases.py). Хүн, дугаар, үйл явдал
-- бүгд зохиомол. Дахин ажиллуулж болно: хуучин сан устаж, анхны өгөгдөл сэргэнэ.
-- Ажиллуулалт бүрийн өмнө дахин ачаалагддаг тул жижиг байлгана.

SET NAMES utf8mb4;

-- 1. Санг шинээр үүсгэх
DROP DATABASE IF EXISTS medleg_hot;
CREATE DATABASE medleg_hot CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE medleg_hot;

-- 2. Хүснэгтүүд: эх хүснэгт эхэлж, түүн рүү заадаг нь дараа нь
CREATE TABLE irgen (
    irgen_id     INT AUTO_INCREMENT PRIMARY KEY,
    ovog         VARCHAR(50) NOT NULL,
    ner          VARCHAR(50) NOT NULL,
    tursun_ognoo DATE        NOT NULL,
    utas         VARCHAR(8)  NULL,
    duureg       VARCHAR(40) NOT NULL,
    ajil         VARCHAR(50) NOT NULL
);

CREATE TABLE tsagdaa (
    tsagdaa_id INT AUTO_INCREMENT PRIMARY KEY,
    irgen_id   INT         NOT NULL,
    tsol       VARCHAR(30) NOT NULL,
    alba       VARCHAR(40) NOT NULL,
    darga_id   INT         NULL,
    login      VARCHAR(30) NOT NULL,
    CONSTRAINT uq_tsagdaa_login UNIQUE (login),
    CONSTRAINT fk_tsagdaa_irgen FOREIGN KEY (irgen_id) REFERENCES irgen (irgen_id),
    CONSTRAINT fk_tsagdaa_darga FOREIGN KEY (darga_id) REFERENCES tsagdaa (tsagdaa_id)
);

-- 102 дугаарт ирсэн дуудлага
CREATE TABLE duudlaga (
    duudlaga_id INT AUTO_INCREMENT PRIMARY KEY,
    tsag        DATETIME     NOT NULL,
    utas        VARCHAR(8)   NOT NULL,
    medeelegch  VARCHAR(50)  NOT NULL,
    tailbar     VARCHAR(200) NOT NULL
);

-- Хотын музейн үзмэр
CREATE TABLE uzmer (
    uzmer_id  INT AUTO_INCREMENT PRIMARY KEY,
    ner       VARCHAR(60)  NOT NULL,
    tanhim    VARCHAR(40)  NOT NULL,
    jin_gramm INT          NOT NULL,
    une_saya  DECIMAL(8,1) NOT NULL
);

-- Даатгалын компанийн жагсаалт
CREATE TABLE daatgal (
    daatgal_id INT AUTO_INCREMENT PRIMARY KEY,
    uzmer_ner  VARCHAR(60)  NOT NULL,
    une_saya   DECIMAL(8,1) NULL
);

CREATE TABLE mashin (
    mashin_id INT AUTO_INCREMENT PRIMARY KEY,
    dugaar    VARCHAR(10) NOT NULL,
    marka     VARCHAR(40) NOT NULL,
    ungu      VARCHAR(20) NULL,
    uild_on   INT         NOT NULL,
    ezen_id   INT         NULL,
    CONSTRAINT uq_mashin_dugaar UNIQUE (dugaar),
    CONSTRAINT fk_mashin_ezen FOREIGN KEY (ezen_id) REFERENCES irgen (irgen_id)
);

-- Замын камер дугаарыг өөрөө уншиж бичдэг — бичлэг нь алдаатай байж болно
CREATE TABLE kamer_bichlag (
    bichlag_id INT AUTO_INCREMENT PRIMARY KEY,
    kamer      VARCHAR(40) NOT NULL,
    dugaar     VARCHAR(12) NOT NULL,
    tsag       DATETIME    NOT NULL
);

-- Банкны шилжүүлэг
CREATE TABLE guilgee (
    guilgee_id       INT AUTO_INCREMENT PRIMARY KEY,
    ilgeegch_id      INT           NOT NULL,
    huleen_avagch_id INT           NOT NULL,
    dun              DECIMAL(14,2) NOT NULL,
    tsag             DATETIME      NOT NULL,
    utga             VARCHAR(40)   NOT NULL,
    CONSTRAINT fk_guilgee_ilgeegch FOREIGN KEY (ilgeegch_id) REFERENCES irgen (irgen_id),
    CONSTRAINT fk_guilgee_huleen FOREIGN KEY (huleen_avagch_id) REFERENCES irgen (irgen_id),
    CONSTRAINT ck_guilgee_dun CHECK (dun > 0)
);

-- Банкнаас ирсэн CSV — бүх баганыг текстээр ачаалсан
CREATE TABLE belen_mungu (
    mur       INT PRIMARY KEY,
    dans_ezen VARCHAR(60) NOT NULL,
    atm       VARCHAR(60) NOT NULL,
    dun       VARCHAR(20) NOT NULL,
    ognoo     VARCHAR(20) NOT NULL
);

-- Хаалганы картын уншигч
CREATE TABLE nevtrelt (
    nevtrelt_id INT AUTO_INCREMENT PRIMARY KEY,
    irgen_id    INT         NOT NULL,
    barilga     VARCHAR(40) NOT NULL,
    haalga      VARCHAR(40) NOT NULL,
    tsag        DATETIME    NOT NULL,
    tailbar     VARCHAR(40) NULL,
    CONSTRAINT fk_nevtrelt_irgen FOREIGN KEY (irgen_id) REFERENCES irgen (irgen_id)
);

-- Нотлох баримтын бүртгэл — хуучин системээс шууд хуулсан, хязгаарлалтгүй
CREATE TABLE nb_burtgel (
    burtgel_id INT PRIMARY KEY,
    lats       VARCHAR(10)  NOT NULL,
    zuil       VARCHAR(100) NOT NULL,
    jin_gramm  INT          NOT NULL,
    burtgesen  DATETIME     NOT NULL,
    tsagdaa_id INT          NOT NULL
);

-- Утасны дуудлага. tsamhag — залгасан утсыг холбосон цамхаг (байршил)
CREATE TABLE yaria (
    yaria_id     INT AUTO_INCREMENT PRIMARY KEY,
    zalgasan     VARCHAR(8)  NOT NULL,
    avsan        VARCHAR(8)  NOT NULL,
    ehelsen      DATETIME    NOT NULL,
    hugatsaa_sec INT         NOT NULL,
    tsamhag      VARCHAR(40) NOT NULL
);

CREATE TABLE sim_kart (
    utas            VARCHAR(8) PRIMARY KEY,
    hudaldsan_ognoo DATE       NOT NULL,
    irgen_id        INT        NOT NULL,
    CONSTRAINT fk_sim_irgen FOREIGN KEY (irgen_id) REFERENCES irgen (irgen_id)
);

-- Хяналтын албаны тэмдэглэл: уулзалтад байсан утаснууд, таслалаар
CREATE TABLE ajiglalt (
    ajiglalt_id INT AUTO_INCREMENT PRIMARY KEY,
    tsag        DATETIME     NOT NULL,
    bairshil    VARCHAR(40)  NOT NULL,
    utasnuud    VARCHAR(100) NOT NULL
);

CREATE TABLE sejigten (
    sejigten_id INT AUTO_INCREMENT PRIMARY KEY,
    irgen_id    INT          NOT NULL,
    shaltgaan   VARCHAR(100) NOT NULL,
    nemsen      DATE         NOT NULL,
    CONSTRAINT fk_sejigten_irgen FOREIGN KEY (irgen_id) REFERENCES irgen (irgen_id)
);

-- Банк зогсоосон, хараахан хийгдээгүй шилжүүлэг
CREATE TABLE huleelgiin_guilgee (
    dugaar           INT PRIMARY KEY,
    ilgeegch_id      INT           NOT NULL,
    huleen_avagch_id INT           NOT NULL,
    dun              DECIMAL(14,2) NOT NULL,
    tsag             DATETIME      NOT NULL,
    CONSTRAINT fk_huleelgiin_ilgeegch FOREIGN KEY (ilgeegch_id) REFERENCES irgen (irgen_id),
    CONSTRAINT fk_huleelgiin_huleen FOREIGN KEY (huleen_avagch_id) REFERENCES irgen (irgen_id)
);

CREATE TABLE zurvas (
    zurvas_id     INT AUTO_INCREMENT PRIMARY KEY,
    ilgeegch      VARCHAR(8)  NOT NULL,
    huleen_avagch VARCHAR(8)  NOT NULL,
    tsag          DATETIME    NOT NULL,
    agualga       VARCHAR(60) NOT NULL
);

-- Гэрч хамгаалах хөтөлбөр
CREATE TABLE gerch_hamgaalalt (
    hamgaalalt_id INT AUTO_INCREMENT PRIMARY KEY,
    kod           VARCHAR(10) NOT NULL,
    irgen_id      INT         NOT NULL,
    shine_utas    VARCHAR(8)  NOT NULL,
    hayag         VARCHAR(60) NOT NULL,
    CONSTRAINT uq_hamgaalalt_kod UNIQUE (kod),
    CONSTRAINT fk_hamgaalalt_irgen FOREIGN KEY (irgen_id) REFERENCES irgen (irgen_id)
);

-- Цагдаагийн вэб програмын хайлтын лог: хайлтын нүдэнд бичсэн утга
CREATE TABLE app_log (
    log_id  INT AUTO_INCREMENT PRIMARY KEY,
    login   VARCHAR(30)  NOT NULL,
    tsag    DATETIME     NOT NULL,
    hailt   VARCHAR(100) NOT NULL,
    mur_too INT          NULL
);

-- «Хүрэл Антик» дэлгүүрийн бараа ба борлуулалт
CREATE TABLE antik_baraa (
    baraa_id           INT AUTO_INCREMENT PRIMARY KEY,
    ner                VARCHAR(60)   NOT NULL,
    niiluulegch_id     INT           NOT NULL,
    avsan_une          DECIMAL(14,2) NOT NULL,
    zarsan_une         DECIMAL(14,2) NULL,
    zarsan_ognoo       DATE          NULL,
    hudaldan_avagch_id INT           NULL,
    CONSTRAINT fk_antik_niiluulegch FOREIGN KEY (niiluulegch_id) REFERENCES irgen (irgen_id),
    CONSTRAINT fk_antik_avagch FOREIGN KEY (hudaldan_avagch_id) REFERENCES irgen (irgen_id)
);

-- Хотын номын сан
CREATE TABLE nom (
    nom_id      INT AUTO_INCREMENT PRIMARY KEY,
    ner         VARCHAR(80) NOT NULL,
    hevlesen_on INT         NOT NULL
);

CREATE TABLE zeel (
    zeel_id   INT AUTO_INCREMENT PRIMARY KEY,
    nom_id    INT  NOT NULL,
    irgen_id  INT  NOT NULL,
    avsan     DATE NOT NULL,
    duusah    DATE NOT NULL,
    butsaasan DATE NULL,
    CONSTRAINT fk_zeel_nom FOREIGN KEY (nom_id) REFERENCES nom (nom_id),
    CONSTRAINT fk_zeel_irgen FOREIGN KEY (irgen_id) REFERENCES irgen (irgen_id)
);

-- 3. Өгөгдөл
INSERT INTO irgen (irgen_id, ovog, ner, tursun_ognoo, utas, duureg, ajil) VALUES
    (1,  'Батын',        'Сарангэрэл',   '1986-05-14', '88112040', 'Нарны хороолол', 'Таксины жолооч'),
    (2,  'Доржийн',      'Мөнхбат',      '1961-11-02', '99018877', 'Голын эрэг',     'Музейн харуул'),
    (3,  'Ганбатын',     'Энхтуяа',      '1972-03-08', '99110505', 'Төв',            'Музейн захирал'),
    (4,  'Нямын',        'Оюунбилэг',    '1983-09-21', '95223311', 'Төв',            'Сэргээн засварлагч'),
    (5,  'Сүхийн',       'Хүрэлбаатар',  '1969-12-30', '99887711', 'Хуучин хот',     'Эртний эдлэлийн наймаачин'),
    (6,  'Батын',        'Ганхуяг',      '1990-07-07', '88990011', 'Шинэ хот',       'Жолооч'),
    (7,  'Лувсангийн',   'Төмөрбаатар',  '1975-02-11', '99334422', 'Хуучин хот',     'Алтны дархан'),
    (8,  'Цэрэнгийн',    'Батзориг',     '1980-06-18', '88776655', 'Шинэ хот',       'Зуучлагч'),
    (9,  'Баярсайханы',  'Уранчимэг',    '1999-01-25', '95551234', 'Уулын энгэр',    'Оюутан'),
    (10, 'Дамдины',      'Баярсайхан',   '1971-08-09', '99121314', 'Уулын энгэр',    'Цагдаа'),
    (11, 'Очирын',       'Ганбаатар',    '1979-04-04', '99151617', 'Төв',            'Цагдаа'),
    (12, 'Ганбатын',     'Энхболд',      '1968-10-10', '99202122', 'Хуучин хот',     'Бизнес эрхлэгч'),
    (13, 'Пүрэвийн',     'Долгор',       '1953-03-03', '88223344', 'Нарны хороолол', 'Тэтгэвэрт'),
    (14, 'Жамцын',       'Лхагва',       '1965-06-30', '99701234', 'Голын эрэг',     'Загасчин'),
    (15, 'Отгоны',       'Бямбаа',       '1992-12-12', '88445566', 'Шинэ хот',       'Техникч'),
    (16, 'Галын',        'Жаргалсайхан', '1981-05-05', '99556677', 'Хуучин хот',     'Алтны дархан'),
    (17, 'Энхийн',       'Энхбаяр',      '1988-08-08', '88667788', 'Нарны хороолол', 'Таксины жолооч'),
    (18, 'Дашийн',       'Нарангэрэл',   '1972-03-08', '99443355', 'Шинэ хот',       'Багш'),
    (19, 'Цогтын',       'Батбаяр',      '1977-01-15', '99443322', 'Уулын энгэр',    'Дэлгүүр эрхлэгч'),
    (20, 'Мөнхийн',      'Сувд',         '1985-04-22', '95112233', 'Төв',            'Нягтлан бодогч'),
    (21, 'Бямбын',       'Тэмүүлэн',     '1983-02-02', '88002211', 'Шинэ хот',       'Валют арилжаачин'),
    (22, 'Гомбын',       'Одбаяр',       '1990-10-10', '88003322', 'Шинэ хот',       'Валют арилжаачин'),
    (23, 'Лхамын',       'Цэцэг',        '1966-09-09', '99001234', 'Шинэ хот',       'Тогооч'),
    (24, 'Сэргэлэнгийн', 'Хонгорзул',    '1994-03-17', '95667788', 'Шинэ хот',       'Худалдагч'),
    (25, 'Балдангийн',   'Цогтбаяр',     '1979-07-19', '99554411', 'Төв',            'Барилгачин'),
    (26, 'Түвшингийн',   'Ууганаа',      '1995-11-30', '95443322', 'Нарны хороолол', 'Оюутан'),
    (27, 'Жамбын',       'Цогт',         '1966-02-14', '99100001', 'Төв',            'Цагдаа'),
    (28, 'Отгонбаярын',  'Гэрэлмаа',     '1980-12-01', '99100002', 'Төв',            'Цагдаа'),
    (29, 'Сандагийн',    'Төгөлдөр',     '1987-05-09', '99100003', 'Уулын энгэр',    'Цагдаа'),
    (30, 'Доржийн',      'Туяа',         '1965-04-04', '99018800', 'Голын эрэг',     'Эмч'),
    (31, 'Хонгорын',     'Одгэрэл',      '1998-06-06', '95117788', 'Уулын энгэр',    'Оюутан'),
    (32, 'Нямаагийн',    'Солонго',      '1989-09-19', '88124455', 'Уулын энгэр',    'Сувилагч'),
    (33, 'Мягмарын',     'Болор',        '1976-01-01', '99664433', 'Шинэ хот',       'Жолооч');

INSERT INTO tsagdaa (tsagdaa_id, irgen_id, tsol, alba, darga_id, login) VALUES
    (1, 27, 'Хурандаа',      'Удирдлага',     NULL, 'j.tsogt'),
    (2, 28, 'Хошууч',        'Мөрдөн шалгах', 1,    'o.gerelmaa'),
    (3, 29, 'Ахмад',         'Мөрдөн шалгах', 2,    's.tuguldur'),
    (4, 10, 'Ахлах дэслэгч', 'Нотлох баримт', 1,    'd.bayarsaikhan'),
    (5, 11, 'Дэслэгч',       'Нотлох баримт', 4,    'o.ganbaatar');

INSERT INTO duudlaga (duudlaga_id, tsag, utas, medeelegch, tailbar) VALUES
    (1, '2024-10-01 23:12:00', '99443322', 'Батбаяр',    'Хөрш айлд чанга хөгжим тоглож байна'),
    (2, '2024-10-02 00:47:00', '99443355', 'Нарангэрэл', 'Автобусны буудал дээр согтуу хүн унтаж байна'),
    (3, '2024-10-02 02:14:00', '88112040', 'Сарангэрэл', 'Музейн дохиолол дуугарч байна. Хоёр хүн гол руу гүйлээ'),
    (4, '2024-10-02 02:19:00', '99554411', 'Цогтбаяр',   'Музейн зогсоол дээр машины дохиолол дуугарав'),
    (5, '2024-10-02 03:30:00', '95117788', 'Одгэрэл',    'Муур модон дээр гацжээ'),
    (6, '2024-10-02 06:45:00', '99018877', 'Мөнхбат',    'Музейн харуул байна. Шөнө унтчихаж, сэрэхэд дохиолол асаалттай байв');

INSERT INTO uzmer (uzmer_id, ner, tanhim, jin_gramm, une_saya) VALUES
    (1, 'Хүрэл Будда',            'Шашны танхим',   48000,  1500.0),
    (2, 'Алтан тамга',            'Хаадын танхим',  812,    1200.0),
    (3, 'Мөнгөн аяга',            'Хаадын танхим',  380,    45.0),
    (4, 'Хүрэл толь',             'Эртний танхим',  1500,   60.0),
    (5, 'Торгон дээл',            'Хаадын танхим',  2100,   180.0),
    (6, 'Сувдан зүүлт',           'Хаадын танхим',  95,     120.0),
    (7, 'Цаасан мөнгөн дэвсгэрт', 'Түүхийн танхим', 2,      0.5),
    (8, 'Модон сийлбэр',          'Шашны танхим',   3400,   25.0),
    (9, 'Чулуун хөшөө',           'Эртний танхим',  250000, 700.0);

INSERT INTO daatgal (daatgal_id, uzmer_ner, une_saya) VALUES
    (1, 'Хүрэл Будда', 1500.0), (2, 'Алтан тамга', 1200.0), (3, 'Мөнгөн аяга', 45.0),
    (4, 'Хүрэл толь ', 60.0),   (5, 'Торгон дээл', 180.0),  (6, 'Сувдан зүүлт', 120.0),
    (7, 'Мөнгөн хөөрөг', 85.0), (8, 'Модон сийлбэр', NULL), (9, 'Чулуун хөшөө', 700.0);

INSERT INTO mashin (mashin_id, dugaar, marka, ungu, uild_on, ezen_id) VALUES
    (1,  '4527 УНА', 'Тоёота Приус',        NULL,       2011, NULL),
    (2,  '1245 УБН', 'Тоёота Приус',        'Цагаан',   2014, 19),
    (3,  '4581 УКА', 'Хюндай Соната',       'Цагаан',   2016, 20),
    (4,  '4530 ДАР', 'Тоёота Королла',      'Саарал',   2009, 25),
    (5,  '4519 УБЕ', 'Тоёота Ланд Круйзер', 'Хар',      2018, 12),
    (6,  '1702 УНБ', 'Тоёота Приус',        'Шар',      2013, 1),
    (7,  '6061 УББ', 'Тоёота Королла',      'Цэнхэр',   2008, 13),
    (8,  '3318 УБЕ', 'Хюндай Акцент',       'Мөнгөлөг', 2012, 2),
    (9,  '2201 УАА', 'Ниссан Патрол',       'Ногоон',   2005, 14),
    (10, '5050 УБД', 'Лексус RX',           'Хар',      2020, 3),
    (11, '0909 УНН', 'Лексус LX',           'Мөнгөлөг', 2021, 5),
    (12, '1234 УНД', 'Хонда Фит',           NULL,       2010, 26),
    (13, '3434 УКБ', 'Ниссан Лиф',          'Цагаан',   2019, 31),
    (14, '7788 УАБ', 'Тоёота Приус',        'Цагаан',   2015, 17);

INSERT INTO kamer_bichlag (bichlag_id, kamer, dugaar, tsag) VALUES
    (1,  'Музейн гудамж',  '4527 УНА',  '2024-10-02 01:12:00'),
    (2,  'Музейн гудамж',  '1702 УНБ',  '2024-10-02 01:58:00'),
    (3,  'Төв талбай',     '4527 уна',  '2024-10-02 02:18:00'),
    (4,  'Голын гүүр',     '4527УНА',   '2024-10-02 02:41:00'),
    (5,  'Хүрэл Антик',    ' 4527-УНА', '2024-10-02 03:05:00'),
    (6,  'Төв талбай',     '0909 УНН',  '2024-10-02 09:30:00'),
    (7,  'Нарны зах',      '4527 УНА',  '2024-10-05 10:20:00'),
    (8,  'Төв талбай',     '3434 УКБ',  '2024-10-16 08:10:00'),
    (9,  'Голын гүүр',     '3434 УКБ',  '2024-10-16 08:25:00'),
    (10, 'Нисэх',          '7788 УАБ',  '2024-10-16 12:00:00'),
    (11, 'Хүрэл Антик',    '7788 УАБ',  '2024-10-16 12:40:00'),
    (12, 'Нарны хороолол', '6061 УББ',  '2024-10-16 18:02:00'),
    (13, 'Нисэх',          '6061 УББ',  '2024-10-16 18:06:00'),
    (14, 'Төв талбай',     '1702 УНБ',  '2024-10-16 19:00:00'),
    (15, 'Төв талбай',     '1702 УНБ',  '2024-10-16 19:02:00'),
    (16, 'Такси парк',     '1702 УНБ',  '2024-10-19 20:05:00'),
    (17, 'Тээрмийн зам',   '2201 УАА',  '2024-10-19 21:50:00'),
    (18, 'Голын эрэг',     '3318 УБЕ',  '2024-10-19 22:09:00'),
    (19, 'Тээрмийн зам',   '2201 УАА',  '2024-10-19 22:20:00'),
    (20, 'Тээрмийн зам',   '6061 УББ',  '2024-10-19 22:24:00'),
    (21, 'Нарны хороолол', '6061 УББ',  '2024-10-19 22:27:00'),
    (22, 'Тээрмийн зам',   '3318 УБЕ',  '2024-10-19 22:31:00'),
    (23, 'Тээрмийн зам',   '6061 УББ',  '2024-10-19 22:58:00'),
    (24, 'Нарны хороолол', '6061 УББ',  '2024-10-19 23:15:00'),
    (25, 'Такси парк',     '6061 УББ',  '2024-10-19 23:18:00'),
    (26, 'Нарны хороолол', '1702 УНБ',  '2024-10-20 00:10:00');

INSERT INTO guilgee (guilgee_id, ilgeegch_id, huleen_avagch_id, dun, tsag, utga) VALUES
    (1,  5,  4,  10000000.00, '2024-09-01 11:00:00', 'Урьдчилгаа'),
    (2,  5,  7,  18000000.00, '2024-09-10 15:20:00', 'Захиалга'),
    (3,  5,  16,   800000.00, '2024-09-12 10:05:00', 'Бөгж засвар'),
    (4,  5,  7,   6000000.00, '2024-09-25 16:40:00', 'Үлдэгдэл'),
    (5,  19, 20,  4700000.00, '2024-09-28 12:00:00', 'Түрээс'),
    (6,  5,  1,   2000000.00, '2024-10-02 03:40:00', 'Такси'),
    (7,  5,  6,   4950000.00, '2024-10-02 09:10:00', 'Зээл'),
    (8,  19, 20,  4800000.00, '2024-10-02 12:30:00', 'Түрээс'),
    (9,  5,  6,   4900000.00, '2024-10-03 09:05:00', 'Зээл'),
    (10, 21, 22,  4900000.00, '2024-10-03 14:00:00', 'Валют'),
    (11, 5,  6,   4850000.00, '2024-10-04 09:20:00', 'Зээл'),
    (12, 21, 22,  4800000.00, '2024-10-05 14:10:00', 'Валют'),
    (13, 21, 22,  5000000.00, '2024-10-06 14:05:00', 'Валют'),
    (14, 19, 20,  4750000.00, '2024-10-07 11:00:00', 'Түрээс'),
    (15, 12, 9,   9500000.00, '2024-10-07 18:00:00', 'Сургалтын төлбөр'),
    (16, 5,  8,   3000000.00, '2024-10-08 13:00:00', 'Зуучлал'),
    (17, 23, 24,  1200000.00, '2024-10-09 10:00:00', 'Цалин'),
    (18, 25, 12,  3000000.00, '2024-10-18 16:00:00', 'Барилгын материал'),
    (19, 3,  12, 20000000.00, '2024-10-20 08:40:00', 'Зээл'),
    (20, 12, 1,  15000000.00, '2024-10-20 09:12:00', 'Машины төлбөр'),
    (21, 12, 9,   4000000.00, '2024-10-20 09:30:00', 'Сургалтын төлбөр');

INSERT INTO belen_mungu (mur, dans_ezen, atm, dun, ognoo) VALUES
    (1, 'Батын Ганхуяг', 'Шинэ хот салбар',    '600000',  '2024-10-03'),
    (2, 'Батын Ганхуяг', 'Нарны зах',          '980000',  '2024-10-03'),
    (3, 'Батын Ганхуяг', 'Голын гүүр',         '1200000', '2024-10-04'),
    (4, 'Батын Ганхуяг', 'Төв талбай',         '2500000', '2024-10-04'),
    (5, 'Батын Ганхуяг', 'Төмөр замын буудал', '4750000', '2024-10-05');

INSERT INTO nevtrelt (nevtrelt_id, irgen_id, barilga, haalga, tsag, tailbar) VALUES
    (1,  3,  'Музей',            'Гол хаалга',           '2024-10-01 08:45:00', NULL),
    (2,  4,  'Музей',            'Гол хаалга',           '2024-10-01 09:02:00', NULL),
    (3,  4,  'Музей',            'Арын хаалга',          '2024-10-01 09:15:00', NULL),
    (4,  15, 'Музей',            'Гол хаалга',           '2024-10-01 02:05:00', 'Туршилт'),
    (5,  2,  'Музей',            'Гол хаалга',           '2024-10-01 21:55:00', NULL),
    (6,  4,  'Музей',            'Арын хаалга',          '2024-10-01 17:40:00', NULL),
    (7,  15, 'Музей',            'Гол хаалга',           '2024-10-02 02:05:00', 'Туршилт'),
    (8,  3,  'Музей',            'Гол хаалга',           '2024-10-02 07:50:00', NULL),
    (9,  11, 'Цагдаагийн газар', 'Нотлох баримтын өрөө', '2024-10-05 15:20:00', NULL),
    (10, 28, 'Цагдаагийн газар', 'Нотлох баримтын өрөө', '2024-10-05 19:35:00', NULL),
    (11, 10, 'Цагдаагийн газар', 'Нотлох баримтын өрөө', '2024-10-06 22:47:00', NULL),
    (12, 10, 'Цагдаагийн газар', 'Гол хаалга',           '2024-10-19 19:55:00', NULL),
    (13, 29, 'Цагдаагийн газар', 'Гол хаалга',           '2024-10-19 21:10:00', NULL),
    (14, 17, 'Такси парк',       'Гараж',                '2024-10-19 19:30:00', NULL),
    (15, 1,  'Такси парк',       'Гараж',                '2024-10-19 20:07:00', NULL),
    (16, 2,  'Голын эрэг 12',    'Гол хаалга',           '2024-10-19 22:03:00', NULL),
    (17, 1,  'Такси парк',       'Гараж',                '2024-10-19 23:21:00', NULL),
    (18, 17, 'Такси парк',       'Гараж',                '2024-10-19 23:49:00', NULL),
    (19, 10, 'Цагдаагийн газар', 'Гол хаалга',           '2024-10-20 08:05:00', NULL);

INSERT INTO nb_burtgel (burtgel_id, lats, zuil, jin_gramm, burtgesen, tsagdaa_id) VALUES
    (1, 'Л-0451', 'Хуруу хээний хальс',           0,    '2024-10-02 10:10:00', 3),
    (2, 'Л-0452', 'Хаалганы түгжээний хэлтэрхий', 40,   '2024-10-02 11:30:00', 3),
    (3, 'Л-0453', 'Хар бээлий',                   60,   '2024-10-03 09:00:00', 3),
    (4, 'Л-0454', 'Бэлэн мөнгө',                  5200, '2024-10-05 19:40:00', 2),
    (5, 'Л-0455', 'Сэжигтний гар утас',           180,  '2024-10-05 19:45:00', 2),
    (6, 'Л-0456', 'Галт тэрэгний тасалбар',       3,    '2024-10-05 19:50:00', 2),
    (7, 'Л-0455', 'Гар утас — эзэнд нь буцаав',   180,  '2024-10-06 22:51:00', 5),
    (8, 'Л-0457', 'Музейн түлхүүрийн хуулбар',    25,   '2024-10-07 10:00:00', 3);

INSERT INTO yaria (yaria_id, zalgasan, avsan, ehelsen, hugatsaa_sec, tsamhag) VALUES
    (1,  '88990011', '95223311', '2024-10-02 01:38:00', 20,  'Төв'),
    (2,  '99001234', '88990011', '2024-10-02 01:48:00', 60,  'Шинэ хот'),
    (3,  '89001122', '88990011', '2024-10-02 02:16:00', 40,  'Хуучин хот'),
    (4,  '95667788', '88990011', '2024-10-02 02:20:00', 95,  'Шинэ хот'),
    (5,  '89001122', '88112040', '2024-10-02 02:22:00', 25,  'Хуучин хот'),
    (6,  '99887711', '99110505', '2024-10-02 07:30:00', 120, 'Хуучин хот'),
    (7,  '99018877', '102',      '2024-10-12 10:05:00', 180, 'Голын эрэг'),
    (8,  '99121314', '88104477', '2024-10-19 21:40:00', 75,  'Төв'),
    (9,  '88104477', '99018800', '2024-10-19 21:58:00', 140, 'Голын эрэг'),
    (10, '99701234', '99702345', '2024-10-19 22:12:00', 50,  'Хуучин тээрэм'),
    (11, '88104477', '102',      '2024-10-19 22:44:00', 0,   'Хуучин тээрэм'),
    (12, '88104477', '102',      '2024-10-19 23:10:00', 4,   'Төв талбай');

INSERT INTO sim_kart (utas, hudaldsan_ognoo, irgen_id) VALUES
    ('89001122', '2024-09-20', 5),
    ('89005566', '2024-09-21', 8);

INSERT INTO ajiglalt (ajiglalt_id, tsag, bairshil, utasnuud) VALUES
    (1, '2024-09-20 14:00:00', 'Хүрэл Антик',      '99887711, 88776655, 99334422'),
    (2, '2024-09-24 20:30:00', 'Хаан ресторан',    '99887711,88776655'),
    (3, '2024-09-27 11:15:00', 'Хуучин хотын зах', '88776655, 99887711, 95223311'),
    (4, '2024-09-30 19:00:00', 'Хаан ресторан',    '89001122, 88776655, 88990011'),
    (5, '2024-10-01 16:45:00', 'Хүрэл Антик',      '99887711, 88776655, 99110505');

INSERT INTO sejigten (sejigten_id, irgen_id, shaltgaan, nemsen) VALUES
    (1, 6,  'Зугтсан машины жолооч',                  '2024-10-05'),
    (2, 4,  'Шөнө музейд арын хаалгаар орсон',        '2024-10-07'),
    (3, 11, 'Хуурамч бүртгэл түүний нэрээр орсон',    '2024-10-08'),
    (4, 5,  'Нэргүй SIM картын эзэн',                 '2024-10-09'),
    (5, 7,  'Хуурамч тамга урласан',                  '2024-10-10'),
    (6, 3,  'Даатгалын жагсаалтын үзмэр алга болсон', '2024-10-11'),
    (7, 8,  'Нууц уулзалт бүрт оролцсон',             '2024-10-12');

INSERT INTO huleelgiin_guilgee (dugaar, ilgeegch_id, huleen_avagch_id, dun, tsag) VALUES
    (1, 5, 9,  11000000.00, '2024-10-12 23:55:00'),
    (2, 5, 8,  12000000.00, '2024-10-12 23:56:00'),
    (3, 5, 12,  4000000.00, '2024-10-12 23:57:00'),
    (4, 5, 17,  1500000.00, '2024-10-12 23:58:00');

INSERT INTO zurvas (zurvas_id, ilgeegch, huleen_avagch, tsag, agualga) VALUES
    (1, '89001122', '88776655', '2024-10-10 21:00:00', 'ЦГБӨШЭТҮЛЧДЭХЯНЗ'),
    (2, '89001122', '88776655', '2024-10-17 07:30:00', 'ХМОБАРЦЕГЖУИНТЛШ'),
    (3, '88776655', '89001122', '2024-10-17 07:41:00', 'ОЙЛГОЛОО');

INSERT INTO gerch_hamgaalalt (hamgaalalt_id, kod, irgen_id, shine_utas, hayag) VALUES
    (1, 'ГХ-101', 32, '88101122', 'Уулын энгэр, 3-р байр'),
    (2, 'ГХ-102', 33, '88102233', 'Гол гудамж, 40-р байр'),
    (3, 'ГХ-103', 20, '88103344', 'Хуучин хот, 7-р байр'),
    (4, 'ГХ-104', 2,  '88104477', 'Голын эрэг, 12-р байр');

INSERT INTO app_log (log_id, login, tsag, hailt, mur_too) VALUES
    (1, 'o.gerelmaa',  '2024-10-15 10:12:00', 'ГХ-102', 1),
    (2, 'j.tsogt',     '2024-10-16 14:30:00', 'ГХ-101', 1),
    (3, 'o.ganbaatar', '2024-10-18 23:05:00', 'ГХ-10', 0),
    (4, 'o.ganbaatar', '2024-10-18 23:07:00', '''', NULL),
    (5, 'o.ganbaatar', '2024-10-18 23:09:00', 'x'' OR hayag LIKE ''%Голын%', 1),
    (6, 's.tuguldur',  '2024-10-19 09:00:00', 'ГХ-103', 1);

INSERT INTO antik_baraa
    (baraa_id, ner, niiluulegch_id, avsan_une, zarsan_une, zarsan_ognoo, hudaldan_avagch_id) VALUES
    (1,  'Мөнгөн хөөрөг',     3,  2000000.00,   38000000.00,  '2023-11-20', 8),
    (2,  'Хүрэл бурхан',      19, 110000000.00, 150000000.00, '2024-08-14', 25),
    (3,  'Алтан ээмэг',       20, 18000000.00,  30000000.00,  '2024-08-18', 31),
    (4,  'Хуучин сэлэм',      19, 8000000.00,   12000000.00,  '2024-08-20', 26),
    (5,  'Мөнгөн тогоо',      16, 12000000.00,  20000000.00,  '2024-08-26', 33),
    (6,  'Мөнгөн бугуйвч',    16, 2000000.00,   3500000.00,   '2024-08-27', 24),
    (7,  'Модон авдар',       25, 1000000.00,   2200000.00,   '2024-09-05', 32),
    (8,  'Хөөрөгний хайрцаг', 3,  500000.00,    1100000.00,   '2024-09-18', 31),
    (9,  'Зэс тогоо',         25, 800000.00,    1500000.00,   '2024-10-03', 26),
    (10, 'Шатрын хөлөг',      19, 1200000.00,   2500000.00,   '2024-10-09', 24),
    (11, 'Лааны суурь',       5,  200000.00,    120000000.00, '2024-10-16', 8),
    (12, 'Торгон хадаг',      20, 300000.00,    NULL,         NULL,         NULL);

INSERT INTO nom (nom_id, ner, hevlesen_on) VALUES
    (1, 'Музейн үзмэрийн каталог',     1998),
    (2, 'Монгол тамга, тэмдэг',        2005),
    (3, 'Загас агнуурын гарын авлага', 2015),
    (4, 'Эртний алт, дархны урлал',    2010),
    (5, 'МедлегХотын түүх',            2019);

INSERT INTO zeel (zeel_id, nom_id, irgen_id, avsan, duusah, butsaasan) VALUES
    (1, 1, 3,  '2024-06-01', '2024-06-15', '2024-08-19'),
    (2, 3, 14, '2024-06-17', '2024-07-01', '2024-08-30'),
    (3, 1, 7,  '2024-08-20', '2024-09-03', NULL),
    (4, 4, 7,  '2024-08-20', '2024-09-03', '2024-09-02'),
    (5, 5, 26, '2024-09-10', '2024-09-24', NULL),
    (6, 3, 26, '2024-09-17', '2024-10-01', NULL),
    (7, 2, 3,  '2024-10-01', '2024-10-15', '2024-10-14'),
    (8, 2, 2,  '2024-10-14', '2024-10-28', NULL);

-- 4. Даргын самбарт харагддаг сэжигтнүүдийн жагсаалт
CREATE VIEW v_sejigten AS
SELECT s.sejigten_id, i.ovog, i.ner, s.shaltgaan, s.nemsen
FROM sejigten AS s
JOIN irgen AS i ON i.irgen_id = s.irgen_id
WHERE i.tursun_ognoo <> '1972-03-08';

-- 5. Серверээс олдсон, эзэн нь тодорхойгүй «шөнийн ажил»
DELIMITER $$
CREATE PROCEDURE shono_ajil()
BEGIN
    DECLARE v_orlon INT;
    SELECT irgen_id INTO v_orlon FROM tsagdaa WHERE login = 'o.ganbaatar';
    UPDATE nevtrelt
    SET irgen_id = v_orlon
    WHERE barilga = 'Цагдаагийн газар'
      AND haalga = 'Нотлох баримтын өрөө'
      AND tsag >= '2024-10-06 20:00:00' AND tsag < '2024-10-07 06:00:00';
END$$
DELIMITER ;

-- 6. Шалгах: 22 хүснэгт
SELECT 'medleg_hot' AS san, COUNT(*) AS husnegt_too
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = 'medleg_hot' AND TABLE_TYPE = 'BASE TABLE';
