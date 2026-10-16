"""Модул 6-9 — Салаа, нэгтгэлт, GitHub дээрх хамтын ажиллагаа.

Git-ийн хамгийн хүчтэй боломж нь салаа. Энэ нь олон хүн нэг төсөл дээр
бие биенээ эвдэлгүй ажиллах боломж олгоно.
"""

from app.content.types import LessonSpec, ModuleSpec
from app.models.enums import LessonLanguage

SH = LessonLanguage.SHELL

BRANCHES = ModuleSpec(
    title="Модул 6 — Салаа (Branches)",
    description="Үндсэн кодыг эвдэлгүй туршиж ажиллах.",
    lessons=[
        LessonSpec(
            title="Салаа гэж юу вэ?",
            slug="salaa-gej-yu-ve",
            description="Тусдаа ажлын шугам.",
            duration=400,
            language=SH,
            content="""\
**Салаа** нь тусдаа ажлын шугам. Үндсэн кодыг эвдэлгүй шинэ зүйл
туршиж болно.

```text
main      A───B───C───────F
                   \\     /
bolomj              D───E
```

`D` ба `E` нь `bolomj` салаан дээр хийгдсэн. `F` нь тэдгээрийг `main`
руу нэгтгэсэн.

### Яагаад хэрэгтэй вэ

- Дуусаагүй ажил үндсэн кодод нөлөөлөхгүй
- Хэд хэдэн хүн зэрэг өөр зүйл дээр ажиллана
- Туршилт амжилтгүй бол зүгээр л салааг устгана
- Код хянуулах боломж үүснэ (pull request)

### Git-д салаа хямд

Салаа нь зүгээр л **нэг commit руу заасан заагч**. Шинэ салаа үүсгэх
нь файл хуулахгүй — 41 байтын файл үүсгэнэ. Тиймээс хором зуурт болно.

Бусад системд салаа нь бүх файлыг хуулдаг байсан тул хүмүүс салаанаас
зайлсхийдэг байв.

### `HEAD`

`HEAD` нь «би одоо хаана байна» гэсэн заагч. Ихэвчлэн салаа руу заана:

```text
HEAD -> main -> C
```

### Салаа харах

```bash
git branch                # локал
git branch -r             # алсын
git branch -a             # бүгд
git branch -v             # сүүлийн commit-тай хамт
```

Одоогийн салаа `*` тэмдэгтэй харагдана.

### Салаа солих

```bash
git switch bolomj         # шинэ тушаал — тодорхой
git checkout bolomj       # хуучин — олон үүрэгтэй
```

`git switch` нь зөвхөн салаа солино. `git checkout` нь файл сэргээх,
commit руу үсрэх зэрэг олон ажил хийдэг тул эхлэгчид төөрөгддөг.
**Шинэ кодод `switch` сонго.**

### Салаа солиход юу болох вэ

Ажлын хавтас дахь файлууд **тэр салааны байдал руу** солигдоно. Тиймээс
commit хийгээгүй өөрчлөлт байвал Git анхааруулна.

```bash
git stash        # өөрчлөлтийг түр нууж хадгална (Модул 11-д үзнэ)
git switch main
```

### Салааны нэр

```text
bolomj/nevtreh-maygt
zasvar/hooson-nuuts-ug
tailan/2026-09
```

Урьдчилсан угтвар нь жагсаалтыг эмхэлнэ. Багийн журмыг дага.
""",
            initial_code="""\
# --- Салаа харах ---
git branch                    # локал, одоогийнх нь * тэмдэгтэй
git branch -v                 # сүүлийн commit-тай хамт
git branch -a                 # алсынхыг ч харуулна

# --- Салаа солих ---
git switch bolomj             # шинэ тушаал — зөвхөн салаа солино
git switch main

# git checkout bolomj         # хуучин хувилбар, олон үүрэгтэй

# --- Өмнөх салаа руу буцах ---
git switch -

# --- Одоо хаана байгааг харах ---
git status
git branch --show-current

# --- Салааны түүхийг зурагтай харах ---
git log --oneline --graph --all --decorate

# --- Commit хийгээгүй өөрчлөлттэй үед солих ---
git stash                     # түр нууж хадгална (Модул 11-д үзнэ)
git switch main
git stash pop                 # буцааж авна
""",
        ),
        LessonSpec(
            title="Салаа үүсгэх ба устгах",
            slug="salaa-uusgeh-ustgah",
            description="branch, switch -c, устгах.",
            duration=400,
            language=SH,
            content="""\
### Үүсгэх

```bash
git branch bolomj/nevtreh          # үүсгэнэ, ШИЛЖИХГҮЙ
git switch bolomj/nevtreh          # шилжинэ
```

Хоёрыг нэг дор:

```bash
git switch -c bolomj/nevtreh       # үүсгээд шилжинэ
git checkout -b bolomj/nevtreh     # хуучин хувилбар
```

`-c` нь *create*. Энэ хэлбэр хамгийн түгээмэл.

### Хаанаас эхлэх вэ

Шинэ салаа нь **одоогийн байрлалаас** үүснэ. Тиймээс эхлэхийн өмнө
зөв газраа байгаа эсэхээ шалга:

```bash
git switch main
git pull
git switch -c bolomj/nevtreh
```

Хуучирсан `main` дээрээс салаа гаргавал дараа нь илүү зөрчил үүснэ.

Тодорхой цэгээс:

```bash
git switch -c zasvar a1b2c3d       # commit-оос
git switch -c zasvar v1.0          # тэмдгээс
```

### Нэр солих

```bash
git branch -m shine-ner            # одоогийнхыг
git branch -m huuchin shine        # тодорхойг
```

### Устгах

```bash
git branch -d bolomj/nevtreh       # аюулгүй — нэгтгээгүй бол татгалзана
git branch -D bolomj/nevtreh       # албадан — АНХААРУУЛГАГҮЙ устгана
```

> `-d` ашигла. Татгалзвал тэр салаанд нэгтгээгүй ажил байна гэсэн үг —
> Git тань ажлаа алдахаас хамгаалж байна.

### Алсынхыг устгах

```bash
git push origin --delete bolomj/nevtreh
```

Локал ба алсын салаа нь **тусдаа**. Нэгийг устгахад нөгөө нь үлдэнэ.

### Нэгтгэсэн салааг цэвэрлэх

```bash
git branch --merged main           # нэгтгэгдсэн салаанууд
git branch --no-merged main        # нэгтгээгүй
```

Нэгтгэсэн салааг устгах нь зүйтэй — жагсаалт цэвэрхэн болно.

### Санамсаргүй устгасан бол

```bash
git reflog
git switch -c sergeesen a1b2c3d
```

`reflog` нь `HEAD` хаана явснаа бүртгэдэг. Устсан салааны commit нь
хэсэг хугацаанд үлддэг тул сэргээж болно. Модул 10-д дэлгэрэнгүй.
""",
            initial_code="""\
# --- Зөв газраасаа эхлэх ---
git switch main
git pull
git switch -c bolomj/nevtreh-maygt

# -c нь create — үүсгээд шилжинэ

# --- Ажиллаад commit хийх ---
# ... файлаа засна ...
git add .
git commit -m "Нэвтрэх маягтын шалгалт нэмэв"

# --- Алсад илгээх ---
git push -u origin bolomj/nevtreh-maygt

# --- Тодорхой цэгээс салаа гаргах ---
git switch -c zasvar a1b2c3d       # commit-оос
git switch -c zasvar v1.0          # тэмдгээс

# --- Нэр солих ---
git branch -m bolomj/shine-ner

# --- Нэгтгэсний дараа цэвэрлэх ---
git switch main
git pull
git branch --merged main           # нэгтгэгдсэнийг харуулна
git branch -d bolomj/nevtreh-maygt # аюулгүй устгал

# Алсынхыг тусад нь
git push origin --delete bolomj/nevtreh-maygt

# --- Санамсаргүй устгасан бол ---
git reflog
git switch -c sergeesen a1b2c3d
""",
        ),
    ],
)

MERGING = ModuleSpec(
    title="Модул 7 — Нэгтгэх (Merging)",
    description="Салаануудыг буцааж нийлүүлэх.",
    lessons=[
        LessonSpec(
            title="git merge",
            slug="git-merge",
            description="Салааны ажлыг үндсэн кодтой нийлүүлэх.",
            duration=420,
            language=SH,
            content="""\
### Үндсэн урсгал

```bash
git switch main            # хүлээн авах салаа руу
git pull                   # шинэчил
git merge bolomj/nevtreh   # нэгтгэнэ
```

> Чиглэлийг санаарай: **хүлээн авах** салаан дээр зогсоод, **өгөх**
> салааг нэрлэнэ.

### Хоёр төрлийн нэгтгэлт

**1. Fast-forward** — `main` дээр шинэ commit байхгүй:

```text
Өмнө:  main ─── A ─── B
                      \\
       bolomj          C ─── D

Дараа: main ─── A ─── B ─── C ─── D
```

Git зүгээр л заагчийг урагшлуулна. Шинэ commit үүсэхгүй.

**2. Гурван талт нэгтгэлт** — хоёулаа урагшилсан:

```text
main ─── A ─── B ─── E ─── M
                \\         /
bolomj           C ─── D
```

`M` нь **нэгтгэх commit** — хоёр эцэгтэй.

### Түүхийг хадгалах

```bash
git merge --no-ff bolomj/nevtreh
```

Fast-forward боломжтой ч нэгтгэх commit **заавал** үүсгэнэ. Давуу тал:
тэр салаанд ямар ажил хийгдсэн нь түүхэнд харагдана.

Олон баг үүнийг шаарддаг.

### Нэгтгэхийн өмнө

```bash
git status                 # цэвэр байх ёстой
git switch main
git pull                   # хуучирсан main дээр нэгтгэхгүй
```

Commit хийгээгүй өөрчлөлттэй бол Git татгалзана.

### Нэгтгэлтийг цуцлах

```bash
git merge --abort
```

Зөрчил гарч, шийдэхийг хүсэхгүй бол бүгдийг буцаана.

### Нэгтгэсний дараа

```bash
git push
git branch -d bolomj/nevtreh
git push origin --delete bolomj/nevtreh
```

### Merge ба rebase

```bash
git rebase main            # салааны commit-уудыг main-ий дээр дахин тавина
```

| | `merge` | `rebase` |
|---|---|---|
| Түүх | Бодит, салаатай | Шулуун, цэвэр |
| Аюулгүй | Тийм | Түүхийг өөрчилнө |

> Push хийсэн, бусад хүн ашиглаж байгаа салааг **хэзээ ч** бүү rebase
> хий. Зөвхөн өөрийн локал салаанд.
""",
            initial_code="""\
# --- Нэгтгэхийн өмнө ---
git status                      # цэвэр байх ёстой
git switch main
git pull                        # хуучирсан main дээр нэгтгэхгүй

# --- Нэгтгэх ---
git merge bolomj/nevtreh

# Чиглэл: ХҮЛЭЭН АВАХ салаан дээр зогсоод ӨГӨХ салааг нэрлэнэ

# --- Түүхэнд салаа харагдуулах ---
git merge --no-ff bolomj/nevtreh

# --- Үр дүнг харах ---
git log --oneline --graph --all

# --- Илгээж, цэвэрлэх ---
git push
git branch -d bolomj/nevtreh
git push origin --delete bolomj/nevtreh

# --- Зөрчил гарч, шийдэхийг хүсэхгүй бол ---
git merge --abort

# --- Rebase хувилбар (ЗӨВХӨН өөрийн локал салаанд) ---
git switch bolomj/nevtreh
git rebase main
# зөрчил гарвал шийдээд:
git rebase --continue
# эсвэл цуцлах:
git rebase --abort
""",
        ),
        LessonSpec(
            title="Нэгтгэлтийн зөрчил",
            slug="zorchil",
            description="Хэзээ, яагаад үүсдэг вэ.",
            duration=420,
            language=SH,
            content="""\
### Хэзээ үүсдэг вэ

Хоёр салаа **нэг файлын нэг мөрийг** өөр өөрөөр өөрчилсөн үед. Git аль
нь зөв болохыг мэдэх аргагүй тул таныг шийдэхийг хүснэ.

> Зөрчил бол **алдаа биш**. Хоёр хүн зэрэг ажиллахад хэвийн үзэгдэл.

### Юу зөрчил үүсгэдэггүй вэ

- Өөр өөр файл засах
- Нэг файлын **өөр өөр хэсэг** засах

Git эдгээрийг өөрөө нэгтгэнэ.

### Зөрчлийн тэмдэглэгээ

```text
<<<<<<< HEAD
const dээд = 100;
=======
const dээд = 200;
>>>>>>> bolomj/hyazgaar
```

| Хэсэг | Утга |
|---|---|
| `<<<<<<< HEAD` | Таны одоогийн салааны хувилбар эхэлнэ |
| `=======` | Тусгаарлагч |
| `>>>>>>> salaa` | Нөгөө салааны хувилбар дуусна |

### Аль файл зөрчилдсөнийг олох

```bash
git status
```

```text
Unmerged paths:
        both modified:   src/tohirgoo.c
```

```bash
git diff --name-only --diff-filter=U    # зөвхөн зөрчилтэй файл
```

### Зөрчлөөс сэргийлэх

| Арга | Тайлбар |
|---|---|
| Тогтмол `git pull` | Хуучирсан код дээр ажиллахгүй |
| Жижиг салаа | Удаан амьдарсан салаа их зөрчилддөг |
| Хурдан нэгтгэх | Долоо хоног хүлээхгүй |
| Ажлаа хуваарилах | Нэг файл дээр хоёр хүн зэрэг ажиллахгүй |

Хамгийн үр дүнтэй нь **жижиг, богино настай салаа**.

### Автомат форматлагч

Багийнхан өөр өөр форматлагч ашиглавал бүх мөр өөрчлөгдөж, зөрчил
хэмжээлшгүй болно. Нэг тохиргоог төсөлд хадгал (`.editorconfig`,
`.prettierrc`).

### Хоёртын файл

Зураг, `.docx` зэрэг файлыг Git нэгтгэж **чадахгүй**. Зөвхөн аль нэгийг
нь сонгоно:

```bash
git checkout --ours zurag.png
git checkout --theirs zurag.png
```

### Цуцлах

```bash
git merge --abort
```

Зөрчлөөс айх шаардлагагүй — `--abort` нь үргэлж байна. Тайван шийд.
""",
            initial_code="""\
# --- Нэгтгэх үед зөрчил гарлаа ---
git merge bolomj/hyazgaar

# Auto-merging src/tohirgoo.c
# CONFLICT (content): Merge conflict in src/tohirgoo.c
# Automatic merge failed; fix conflicts and then commit the result.

# --- Аль файл зөрчилдсөнийг олох ---
git status
git diff --name-only --diff-filter=U

# --- Файлыг нээхэд ийм байна ---
# <<<<<<< HEAD
# const deed = 100;
# =======
# const deed = 200;
# >>>>>>> bolomj/hyazgaar

# --- Хоёртын файлд аль нэгийг нь сонгох ---
git checkout --ours zurag.png      # миний хувилбар
git checkout --theirs zurag.png    # нөгөө салааных

# --- Цуцлах ---
git merge --abort

# --- Зөрчлөөс сэргийлэх ---
git pull                           # тогтмол шинэчил
# Салаагаа жижиг байлга, хурдан нэгтгэ
""",
        ),
        LessonSpec(
            title="Зөрчлийг шийдэх",
            slug="zorchil-shiideh",
            description="Алхам алхмаар шийдэх дараалал.",
            duration=450,
            language=SH,
            content="""\
### Таван алхам

```bash
# 1. Аль файл зөрчилдсөнийг олох
git status

# 2. Файлыг нээж, зөрчлийг ЗАСАХ
#    Бүх <<<<<<< ======= >>>>>>> мөрийг УСТГАНА

# 3. Зассан файлыг бэлтгэх
git add src/tohirgoo.c

# 4. Бүгдийг шийдсэн эсэхийг шалгах
git status

# 5. Нэгтгэлтийг дуусгах
git commit
```

Сүүлийн `git commit` нь мессежийг өөрөө бэлдэнэ — засах шаардлагагүй.

### Зөв шийдэл гэж юу вэ

Зөрчлийн тэмдэглэгээг арилгах нь **хангалтгүй**. Гурван сонголтыг бод:

| Сонголт | Хэзээ |
|---|---|
| Миний хувилбар | Нөгөөх нь хуучирсан |
| Тэдний хувилбар | Миний нь хуучирсан |
| **Хоёуланг нь нэгтгэсэн шинэ код** | Ихэвчлэн зөв хариулт |

Гурав дахийг мартах нь түгээмэл алдаа. Хоёр хүн хоёулаа хэрэгтэй зүйл
нэмсэн байж болно.

### Эргэлзвэл асуу

Тэр мөрийг хэн бичсэнийг олох:

```bash
git log -p --follow src/tohirgoo.c   # файлын өөрчлөлт бүр, хэн хийснийх нь хамт
git blame src/tohirgoo.c             # мөр бүрийг хэн, аль commit-д бичсэн (Модул 12)
```

Тэр хүнээс асуух нь таамаглахаас хамаагүй хурдан.

### Шийдсэний дараа ЗААВАЛ шалга

```bash
# Хөрвүүлэгдэж байна уу
make

# Тест өнгөрч байна уу
npm test
```

> Зөрчлийг «арилгасан» ч код нь ажиллахгүй байх нь **маш түгээмэл**.
> Хоёр талын логик зөрчилдсөн байж болно. Тест ажиллуулахгүйгээр
> commit хийж болохгүй.

### Тэмдэглэгээ үлдээгүй эсэх

```bash
git diff --check
grep -rn "<<<<<<<" src/
```

Санамсаргүй үлдсэн `<<<<<<<` нь ажиллахгүй код руу хүргэнэ.

### Хэрэгсэл ашиглах

```bash
git mergetool
```

VS Code нь зөрчлийг харуулж, «Accept Current / Accept Incoming / Accept
Both» товч санал болгоно. Гараар засахаас хурдан бөгөөд тэмдэглэгээ
үлдээхгүй.

### Дахин зөрчилдөхөөс сэргийлэх

```bash
git config --global rerere.enabled true
```

*Reuse recorded resolution* — ижил зөрчил дахин гарвал Git өмнөх
шийдлийг тань автоматаар хэрэглэнэ. Удаан үргэлжилсэн rebase-д
маш хэрэгтэй.
""",
            initial_code="""\
# --- 1. Аль файл зөрчилдсөн бэ ---
git status
git diff --name-only --diff-filter=U

# --- 2. Файлыг засах ---
# Бүх <<<<<<< ======= >>>>>>> мөрийг УСТГАНА
# Гурван сонголтыг бод:
#   - миний хувилбар
#   - тэдний хувилбар
#   - ХОЁУЛАНГ нь нэгтгэсэн шинэ код  <- ихэвчлэн зөв хариулт

# Хэн бичсэнийг олох: мөр бүрийн зохиогч (blame-ийг Модул 12-т үзнэ)
git blame src/tohirgoo.c
git log -p --follow src/tohirgoo.c

# --- 3. Зассаныг бэлтгэх ---
git add src/tohirgoo.c

# --- 4. Шалгах ---
git status
git diff --check                   # үлдсэн тэмдэглэгээ байна уу
grep -rn "<<<<<<<" src/

# --- 5. ЗААВАЛ тест ажиллуул ---
npm test

# --- 6. Дуусгах ---
git commit                         # мессежийг Git өөрөө бэлдэнэ

# --- Хэрэгсэл ашиглах ---
git mergetool

# --- Ижил зөрчлийг дахин шийдэхгүй байх ---
git config --global rerere.enabled true
""",
        ),
    ],
)

COLLABORATION = ModuleSpec(
    title="Модул 8 — GitHub дээрх хамтын ажиллагаа",
    description="Fork, pull request, код хянах, issue.",
    lessons=[
        LessonSpec(
            title="Fork ба pull request",
            slug="fork-ba-pull-request",
            description="Өөрийн эрхгүй төсөлд хувь нэмэр оруулах.",
            duration=450,
            language=SH,
            content="""\
### Fork

**Fork** нь өөр хүний агуулахын **өөрийн хуулбар** GitHub дээр үүсгэнэ.
Бичих эрхгүй төсөлд хувь нэмэр оруулах арга.

```text
ehiin/tusul  ──fork──>  bi/tusul  ──clone──>  миний компьютер
```

### Бүтэн урсгал

```bash
# 1. GitHub дээр Fork товч дарна

# 2. Өөрийн fork-ыг татна
git clone git@github.com:bi/tusul.git
cd tusul

# 3. Эх төслийг upstream болгон нэмнэ
git remote add upstream https://github.com/ehiin/tusul.git

# 4. Салаа гаргана
git switch -c zasvar/hooson-nuuts-ug

# 5. Ажиллаж commit хийнэ
git commit -am "Хоосон нууц үг зөвшөөрч байсныг зассан"

# 6. ӨӨРИЙН fork руу push хийнэ
git push -u origin zasvar/hooson-nuuts-ug

# 7. GitHub дээр Pull Request нээнэ
```

### Fork-оо шинэчлэх

Эх төсөл урагшилсан бол:

```bash
git switch main
git fetch upstream
git merge upstream/main
git push
```

Салаа гаргахын өмнө үргэлж энийг хий — эс бөгөөс хуучирсан код дээр
ажиллана.

### Pull request

PR нь «миний өөрчлөлтийг авна уу» гэсэн хүсэлт. Түүнд:

- Өөрчлөлтийн жагсаалт
- Хэлэлцүүлэг
- Автомат тестийн үр дүн
- Код хянах тэмдэглэл

### Сайн PR

| Шинж | Тайлбар |
|---|---|
| Жижиг | 400 мөрөөс бага. Том PR хянагдахгүй удна |
| Нэг зорилго | Засвар **ба** шинэ боломж хамт бүү оруул |
| Тайлбартай | Юуг яагаад өөрчилснийг бич |
| Тесттэй | Шинэ код тесттэй ирэх ёстой |
| Ногоон | Автомат шалгалт өнгөрсөн байх |

### PR-ийн тайлбар

```markdown
## Юу өөрчлөгдсөн
Нэвтрэх маягт хоосон нууц үг зөвшөөрч байсныг зассан.

## Яагаад
#42 асуудал. Хоосон нууц үгээр данс үүсгэх боломжтой байсан.

## Хэрхэн шалгах
1. /burtgel хуудас руу орно
2. Нууц үгийг хоосон орхино
3. Алдааны мессеж гарах ёстой

Closes #42
```

`Closes #42` нь нэгтгэхэд тэр issue-г **автоматаар хаана**.

### Санал авсны дараа

```bash
git commit -am "Хяналтын саналыг тусгав"
git push
```

PR нь **автоматаар шинэчлэгдэнэ** — шинэ PR нээх шаардлагагүй.
""",
            initial_code="""\
# --- 1. GitHub дээр Fork товч дарна ---

# --- 2. Өөрийн fork-ыг татах ---
git clone git@github.com:bi/tusul.git
cd tusul

# --- 3. Эх төслийг upstream болгон нэмэх ---
git remote add upstream https://github.com/ehiin/tusul.git
git remote -v
# origin    git@github.com:bi/tusul.git         (миний fork)
# upstream  https://github.com/ehiin/tusul.git  (эх төсөл)

# --- 4. Fork-оо шинэчлэх (салаа гаргахын ӨМНӨ) ---
git switch main
git fetch upstream
git merge upstream/main
git push

# --- 5. Салаа гаргаж ажиллах ---
git switch -c zasvar/hooson-nuuts-ug
# ... засварлана ...
git commit -am "Хоосон нууц үг зөвшөөрч байсныг зассан"

# --- 6. ӨӨРИЙН fork руу push ---
git push -u origin zasvar/hooson-nuuts-ug

# --- 7. GitHub дээр Pull Request нээнэ ---

# --- 8. Хяналтын саналыг тусгах ---
git commit -am "Хяналтын саналыг тусгав"
git push
# PR автоматаар шинэчлэгдэнэ — шинэ PR нээх шаардлагагүй
""",
        ),
        LessonSpec(
            title="Код хянах",
            slug="code-review",
            description="Бусдын кодыг хянах, санал хүлээж авах.",
            duration=450,
            language=SH,
            content="""\
Код хянах нь алдаа барихаас илүү: мэдлэг түгээх, стандарт тогтоох,
хамтын хариуцлага бий болгох.

### Хянагчийн үүрэг

Юу шалгах вэ:

| Асуулт | Яагаад |
|---|---|
| Зөв ажиллах уу | Захын тохиолдол, алдааны зам |
| Ойлгомжтой юу | Хагас жилийн дараа уншиж чадах уу |
| Тесттэй юу | Шинэ зан төлөвт тест бий юу |
| Аюулгүй юу | Нууц үг, оролтын шалгалт |
| Хэрэгтэй юу | Илүүц төвөгтэй байдал байна уу |

### Сайн сэтгэгдэл

| Муу | Сайн |
|---|---|
| «Энэ буруу» | «Хэрэглэгч хоосон нэр оруулбал энд унана. Шалгалт нэмэх үү?» |
| «Муу нэр» | «`d` гэхийн оронд `dundaj` гэвэл уншихад хялбар болох уу?» |
| «Яагаад ингэсэн юм бэ» | «Энэ хэсгийг ойлгосонгүй. Тайлбарлаж өгөх үү?» |

Дүрмүүд:

- **Кодыг** шүүмжил, хүнийг биш
- Асуулт хэлбэрээр бич
- Сайн зүйлийг ч дурд
- Заавал биш саналыг тэмдэглэ: «nit:» эсвэл «санал:»

### Заавал ба сонголт

```text
Заавал: Энд null шалгалт хэрэгтэй — унах эрсдэлтэй.
nit: Хоосон мөр илүүц байна.
Санал: Энийг функц болговол дахин ашиглаж болно.
```

Ингэснээр зохиогч аль нь заавал болохыг мэднэ.

### Зохиогчийн үүрэг

- PR-ээ **жижиг** байлга
- Тайлбар бич — хянагчийн цагийг хэмнэнэ
- Хариулт өг, санал бүрийг үл тоомсорлож болохгүй
- Санал зөв бол зас, зөвшөөрөхгүй бол **шалтгаанаа тайлбарла**
- Хувь хүн рүү бүү ав

### GitHub дээрх хэрэгслүүд

| Боломж | Юунд |
|---|---|
| Inline comment | Тодорхой мөрөнд |
| Suggestion | Засварыг шууд санал болгох — зохиогч нэг товчоор хүлээн авна |
| Approve | Зөвшөөрөх |
| Request changes | Засвар шаардах |
| Draft PR | Дуусаагүй ажлыг эрт харуулах |

### Хурдан хариул

24 цагийн дотор хариулах нь сайн журам. PR удаан хүлээвэл зөрчил
үүсэх, зохиогч контекстээ мартах эрсдэлтэй.

### Автомат шалгалт

Форматлалт, lint зэргийг **хүн бүү хяна**. CI-д даатга:

```yaml
- run: npm run lint
- run: npm test
```

Хүн зөвхөн логик, архитектур дээр анхаарна.
""",
            initial_code="""\
# --- PR-ийг локал дээр шалгах ---
git fetch origin pull/42/head:pr-42
git switch pr-42

# Ажиллуулж үзэх
npm install
npm test
npm start

# --- Юу өөрчлөгдсөнийг харах ---
git diff main...pr-42
git diff main...pr-42 --stat        # файлын жагсаалт

# --- Шалгасны дараа буцах ---
git switch main
git branch -D pr-42

# --- GitHub CLI ашиглавал илүү хялбар ---
gh pr checkout 42
gh pr diff 42
gh pr review 42 --approve
gh pr review 42 --request-changes --body "Null шалгалт нэмнэ үү"

# --- Зохиогч: саналыг тусгах ---
git commit -am "Хяналтын дагуу null шалгалт нэмэв"
git push

# --- Хэн бичсэнийг олох: мөр бүрийн зохиогч (Модул 12-т үзнэ) ---
git blame src/nevtreh.c
git log -p --follow src/nevtreh.c
""",
        ),
        LessonSpec(
            title="Issue ба хэлэлцүүлэг",
            slug="issues-ba-discussions",
            description="Алдаа, санал бүртгэх, асуулт асуух.",
            duration=400,
            language=SH,
            content="""\
### Issue гэж юу вэ

Хийх ажил, алдаа, санал бүртгэх нэгж. Дугаартай (`#42`) бөгөөд commit,
PR-тай холбогдоно.

### Сайн алдааны мэдээлэл

```markdown
## Юу болсон
Нэвтрэх товч дарахад хуудас цагаан болно.

## Хэрхэн давтан гаргах
1. /nevtreh хуудас руу орно
2. Зөв имэйл, нууц үг оруулна
3. «Нэвтрэх» дарна

## Хүлээж байсан
Хяналтын самбар руу шилжинэ.

## Гарсан
Цагаан хуудас. Console дээр:
TypeError: Cannot read properties of undefined (reading 'id')

## Орчин
- Chrome 130, Windows 11
- Хувилбар v2.3.1
```

**Давтан гаргах алхам** нь хамгийн чухал хэсэг. Үүнгүй бол засварлагч
асуудлыг олж чадахгүй.

### Issue-г commit-той холбох

```bash
git commit -m "Нэвтрэхэд хоосон хариу боловсруулав

Closes #42"
```

Түлхүүр үгс: `Closes`, `Fixes`, `Resolves`. Нэгтгэхэд issue
**автоматаар хаагдана**.

Зөвхөн дурдах бол дугаарыг нь бич — холбоос үүснэ, хаагдахгүй:

```text
#42-тэй холбоотой
```

### Шошго (label)

| Шошго | Утга |
|---|---|
| `bug` | Алдаа |
| `enhancement` | Шинэ боломж |
| `documentation` | Баримт бичиг |
| `good first issue` | Шинэ хүнд тохиромжтой |
| `help wanted` | Тусламж хэрэгтэй |

`good first issue` нь шинэ хувь нэмэр оруулагчдыг татах хамгийн үр
дүнтэй арга.

### Загвар

`.github/ISSUE_TEMPLATE/` дотор загвар үүсгэвэл GitHub нь issue нээхэд
автоматаар санал болгоно. Мэдээлэл дутуу ирэхээс сэргийлнэ.

### Issue ба Discussion

| | Issue | Discussion |
|---|---|---|
| Юунд | Тодорхой ажил | Нээлттэй яриа |
| Хаагдах уу | Тийм | Үгүй |
| Жишээ | «Нэвтрэх алдаатай» | «Ямар өгөгдлийн сан сонгох вэ?» |

Асуулт, санаа бол Discussion. Хийх ажил бол Issue.

### Хувь нэмэр оруулж эхлэх

Нээлттэй эх төсөлд оролцох хамгийн хялбар зам:

1. `good first issue` шошготой асуудал хай
2. Сэтгэгдэл бичиж «би хийж үзье» гэж хэл
3. Fork хийж, зас, PR нээ

Эхний PR нь баримт бичгийн үсгийн алдаа ч байж болно — эхлэх нь чухал.
""",
            initial_code="""\
# --- Issue-г commit-той холбох ---
git commit -m "Нэвтрэхэд хоосон хариу боловсруулав

Хэрэглэгчийн мэдээлэл ирээгүй үед хуудас цагаан болж байсан.
Одоо алдааны мессеж харуулна.

Closes #42"

# Түлхүүр үг: Closes, Fixes, Resolves — нэгтгэхэд issue автоматаар хаагдана
# Зөвхөн дурдахад: «#42-тэй холбоотой» — холбоос үүснэ, хаагдахгүй

# --- GitHub CLI-аар issue удирдах ---
gh issue list
gh issue list --label "good first issue"
gh issue view 42
gh issue create --title "Нэвтрэх товч ажиллахгүй" --body "..."
gh issue close 42

# --- Өөрт оноогдсон ажил ---
gh issue list --assignee "@me"

# --- PR-ийг issue-тэй холбох ---
gh pr create --title "Нэвтрэх алдааг зассан" --body "Closes #42"

# --- Issue загвар үүсгэх ---
mkdir -p .github/ISSUE_TEMPLATE
# .github/ISSUE_TEMPLATE/bug_report.md файл нэмвэл
# GitHub issue нээхэд автоматаар санал болгоно
""",
        ),
    ],
)

TEAM = ModuleSpec(
    title="Модул 9 — Багийн ажлын урсгал",
    description="Олон хүн нэг төсөл дээр эмх цэгцтэй ажиллах.",
    lessons=[
        LessonSpec(
            title="Боломжийн салаа",
            slug="bolomjiin-salaa",
            description="Ажил бүрд тусдаа салаа.",
            duration=420,
            language=SH,
            content="""\
### Үндсэн санаа

> `main` салаан дээр **шууд бүү ажилла**. Ажил бүрд салаа гарга.

`main` нь үргэлж **ажиллах төлөвт** байх ёстой. Хэзээ ч түүнээс
байршуулж болдог байх.

### Нэрлэх журам

```text
bolomj/nevtreh-maygt        шинэ боломж
zasvar/hooson-nuuts-ug      алдааны засвар
yaaraltai/tulbur-unasan     яаралтай засвар
barimt/suulgah-zaavar       баримт бичиг
```

Угтвар нь жагсаалтыг эмхэлж, ажлын төрлийг шууд харуулна.

Зарим баг issue дугаар нэмдэг: `bolomj/42-nevtreh-maygt`.

### Салааг богино насттай байлга

| Хугацаа | Эрсдэл |
|---|---|
| 1-2 өдөр | Бага — зөрчил бараг гарахгүй |
| 1 долоо хоног | Дунд |
| 2+ долоо хоног | Өндөр — нэгтгэхэд хэцүү болно |

Том ажлыг **жижиг хэсэгт хуваа**. Тус бүрийг тусад нь нэгтгэ.

### Ердийн мөчлөг

```bash
git switch main
git pull
git switch -c bolomj/nevtreh-maygt

# ажиллана, хэд хэдэн удаа commit хийнэ
git commit -am "Маягтын бүтэц нэмэв"
git commit -am "Шалгалт нэмэв"

git push -u origin bolomj/nevtreh-maygt
# GitHub дээр PR нээнэ
```

### Урт салааг шинэчлэх

Ажил удаан үргэлжилвэл `main`-ийг тогтмол татаж ав:

```bash
git switch bolomj/nevtreh-maygt
git fetch origin
git merge origin/main
```

Ингэснээр зөрчил **бага багаар** шийдэгдэнэ. Эцэст нь нэг дор шийдэхээс
хамаагүй хялбар.

### `main`-ийг хамгаалах

GitHub → Settings → Branches → Add rule:

| Дүрэм | Үр дүн |
|---|---|
| Require pull request | Шууд push хийх боломжгүй |
| Require approvals | Дор хаяж нэг хүн зөвшөөрнө |
| Require status checks | Тест өнгөрсөн байх ёстой |

Эдгээрийг тохируулбал журам нь **автоматаар** хэрэгжинэ.

### Яаралтай засвар

```bash
git switch main
git pull
git switch -c yaaraltai/tulbur-unasan
# зас
git push -u origin yaaraltai/tulbur-unasan
# PR нээж, хурдан хянуулж, нэгтгэнэ
```

Яаралтай ч гэсэн PR-ээр дамжина. Шууд `main` руу push хийх нь хожим
илүү асуудал үүсгэдэг.
""",
            initial_code="""\
# --- Шинэ ажил эхлэх ---
git switch main
git pull                                  # ҮРГЭЛЖ эхлээд татна
git switch -c bolomj/nevtreh-maygt

# --- Ажиллаж, жижиг commit хийх ---
git commit -am "Маягтын бүтэц нэмэв"
git commit -am "Оролтын шалгалт нэмэв"
git commit -am "Алдааны мессеж нэмэв"

# --- Илгээж, PR нээх ---
git push -u origin bolomj/nevtreh-maygt
gh pr create --fill

# --- Урт салааг тогтмол шинэчлэх ---
git fetch origin
git merge origin/main
# Зөрчлийг бага багаар шийдэх нь эцэст нь нэг дор шийдэхээс хялбар

# --- Нэгтгэсний дараа цэвэрлэх ---
git switch main
git pull
git branch -d bolomj/nevtreh-maygt
git fetch --prune

# --- Яаралтай засвар ---
git switch main
git pull
git switch -c yaaraltai/tulbur-unasan
# зас, тест ажиллуул
git push -u origin yaaraltai/tulbur-unasan
""",
        ),
        LessonSpec(
            title="Багийн бүрэн урсгал",
            slug="bagiin-urgats",
            description="Pull, ажил, commit, push, PR, хянал, нэгтгэл.",
            duration=450,
            language=SH,
            content="""\
### Бүтэн мөчлөг

```text
1. git pull                 сүүлийн ажлыг ав
2. git switch -c bolomj/…   салаа гарга
3. ажил хий, commit хий
4. git push                 илгээ
5. PR нээ
6. автомат тест ажиллана
7. багийнхан хянана
8. саналыг тусга
9. нэгтгэнэ
10. салааг устга
```

### Өдрийн эхэнд

```bash
git switch main
git pull
git fetch --prune          # устсан салааг цэвэрлэ
```

### Өдрийн эцэст

```bash
git status                 # орхигдсон зүйл байна уу
git push                   # ажлаа хадгал
```

Commit хийсэн ч push хийгээгүй ажил нь зөвхөн таны компьютер дээр байна.

### Нэгтгэх гурван арга

GitHub PR дээр гурван товч байна:

| Арга | Түүх | Хэзээ |
|---|---|---|
| Merge commit | Бүх commit + нэгтгэх commit | Түүхийг бүтнээр хадгалах |
| Squash and merge | **Нэг** commit болгоно | Хамгийн түгээмэл |
| Rebase and merge | Commit-ууд шулуунаар | Цэвэр түүх хүсвэл |

**Squash** нь ихэнх багийн сонголт: салаан дахь «үсгийн алдаа зассан»
маягийн commit-ууд алга болж, `main` дээр нэг утга учиртай commit
үлдэнэ.

### Хэн юу хийж байгааг мэдэх

```bash
git fetch
git branch -r                          # алсын салаанууд
git log --oneline --all --graph -20
```

```bash
gh pr list                             # нээлттэй PR-ууд
gh pr status                           # надад хамаатай нь
```

### Түгээмэл асуудлууд

| Асуудал | Шийдэл |
|---|---|
| Push татгалзсан | `git pull` хийгээд дахин |
| Буруу салаан дээр commit хийсэн | `git reset --soft HEAD~1` (Модул 10), зөв салаа руу шилж |
| `main` дээр шууд ажилласан | `git switch -c bolomj/…` — commit нь дагаж ирнэ |
| Хэрэггүй файл commit хийсэн | `git rm --cached`, `.gitignore`-д нэм |

### Багийн гэрээ

Эдгээрийг **бичгээр** тогтоо:

- Салааны нэрлэх журам
- Commit мессежийн хэлбэр
- Хэдэн хүн зөвшөөрөх ёстой
- Squash уу, merge үү
- `main` хамгаалалттай юу

Бичээгүй журам нь маргаан үүсгэдэг. `CONTRIBUTING.md`-д бич.
""",
            initial_code="""\
# --- Өдрийн эхэнд ---
git switch main
git pull
git fetch --prune

# --- Шинэ ажил ---
git switch -c bolomj/tailan-eksport

# ... ажиллана ...
git add .
git commit -m "Тайланг CSV болгож экспортлох боломж нэмэв"

git push -u origin bolomj/tailan-eksport
gh pr create --fill

# --- Хяналтын санал ирлээ ---
git commit -am "Хяналтын дагуу алдааны боловсруулалт нэмэв"
git push

# --- Нэгтгэсний дараа ---
git switch main
git pull
git branch -d bolomj/tailan-eksport
git fetch --prune

# --- Юу болж байгааг харах ---
gh pr list
gh pr status
git log --oneline --all --graph -20

# --- Буруу салаан дээр commit хийсэн бол ---
git reset --soft HEAD~1        # commit-ыг буцаана, өөрчлөлт үлдэнэ (Модул 10)
git stash                      # өөрчлөлтийг түр нууна (Модул 11)
git switch zuv-salaa
git stash pop                  # нуусан өөрчлөлтөө буцааж авна
git commit -m "Зөв салаан дээр"

# --- Өдрийн эцэст ---
git status
git push
""",
        ),
    ],
)

GIT_BRANCHING_MODULES = [BRANCHES, MERGING, COLLABORATION, TEAM]
