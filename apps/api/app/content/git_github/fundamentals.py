"""Модул 0-1 — Хувилбарын хяналтын үндэс ба Git тохируулах.

Тушаал бичихээс өмнө Git юу хийдгийг ойлгуулна.
"""

from app.content.types import LessonSpec, ModuleSpec
from app.models.enums import LessonLanguage

SH = LessonLanguage.SHELL

FUNDAMENTALS = ModuleSpec(
    title="Модул 0 — Хувилбарын хяналтын үндэс",
    description="Git юу шийддэг вэ, яагаад хэрэгтэй вэ.",
    lessons=[
        LessonSpec(
            title="Хувилбарын хяналт гэж юу вэ?",
            slug="hyanaltiin-undes",
            description="Файлын түүхийг хадгалах систем.",
            duration=360,
            language=SH,
            content="""\
Танд танил санагдах уу:

```text
tailan.docx
tailan_shine.docx
tailan_shine_etses.docx
tailan_shine_etses_ULAAN.docx
tailan_etsesiin_etses.docx
```

Энэ бол **гараар хийсэн хувилбарын хяналт**. Асуудлууд нь:

- Аль нь хамгийн сүүлийнх вэ
- Юу өөрчлөгдсөнийг мэдэхгүй
- Хоёр хүн зэрэг ажиллаж чадахгүй
- Хуучин хувилбар руу буцахад аль нь болохыг таахгүй

### Хувилбарын хяналтын систем

**Өөрчлөлт бүрийг** түүх болгон хадгална. Git танд дараах зүйлийг өгнө:

| Боломж | Утга |
|---|---|
| Түүх | Хэн, хэзээ, юуг, **яагаад** өөрчилсөн |
| Буцаах | Ямар ч цэг рүү буцаж болно |
| Салаалах | Үндсэн кодыг эвдэлгүй туршиж болно |
| Хамтын ажиллагаа | Олон хүн зэрэг ажиллана |

### Яагаад Git вэ

Git-ээс өмнө ч систем байсан (SVN, CVS). Git-ийн давуу тал:

- **Тархсан** — хүн бүрт бүтэн түүх байна, сервер унасан ч ажиллана
- **Хурдан** — ихэнх үйлдэл локал дээр болно, сүлжээ шаардахгүй
- **Салаа хямд** — шинэ салаа үүсгэх нь бараг үнэгүй
- **Стандарт** — өнөөдөр бараг бүх төсөл Git ашигладаг

Git-ийг Linux-ийн цөмийг удирдахын тулд Linus Torvalds 2005 онд
бүтээсэн.

### Commit гэж юу вэ

**Commit** нь тухайн агшин дахь төслийн **бүрэн агшин зураг**. Commit
бүрт:

- Юу өөрчлөгдсөн
- Хэн өөрчилсөн
- Хэзээ
- **Яагаад** — таны бичсэн мессеж

Сүүлийнх нь хамгийн үнэ цэнэтэй. Код нь юу хийж байгааг харуулдаг ч
**яагаад** ингэж хийснийг зөвхөн commit мессеж хэлнэ.

### Зөвхөн код биш

Git нь текст файл бүрт тохирно: баримт бичиг, тохиргоо, судалгааны
тэмдэглэл. Зураг, видео зэрэг хоёртын файлыг ч хадгална — гэхдээ
өөрчлөлтийг нь харуулж чадахгүй.
""",
            initial_code="""\
# Урьдчилан харах: Git-ийг Модул 1-д суулгаж, эдгээр тушаалыг Модул 2-т
# нэг бүрчлэн үзнэ. Одоо зөвхөн ажлын дарааллыг ажигла.

# Git суулгасан эсэхээ шалгах
git --version

# Аль ч төсөлд эхлэх гурван тушаал
git init                 # шинэ агуулах үүсгэнэ
git add .                # бүх файлыг бэлтгэнэ
git commit -m "Анхны commit"

# Түүхийг харах
git log --oneline

# Одоогийн төлөв
git status
""",
        ),
        LessonSpec(
            title="Git ба GitHub",
            slug="git-ba-github",
            description="Хоёр өөр зүйл. Аль нь юу хийдэг вэ.",
            duration=360,
            language=SH,
            content="""\
Энэ хоёрыг андуурах нь маш түгээмэл.

| | Git | GitHub |
|---|---|---|
| Юу вэ | **Хөтөлбөр** | **Вэбсайт** |
| Хаана ажиллана | Таны компьютер дээр | Интернэтэд |
| Хэн бүтээсэн | Linus Torvalds, 2005 | GitHub Inc., 2008 |
| Хэрэгтэй юу | Тийм | Үгүй — сонголт |

### Git нь дангаараа бүрэн ажиллана

Интернэт огт байхгүй ч Git бүх ажлаа хийнэ: commit, салаа, түүх,
буцаалт. GitHub нь зөвхөн **хуваалцахад** хэрэгтэй.

### GitHub юу нэмдэг вэ

- Кодыг интернэтэд хадгална — компьютер эвдэрсэн ч аюулгүй
- Бусадтай хуваалцана
- Pull request — код хянах урсгал
- Issues — алдаа, санал бүртгэх
- Actions — автомат тест ажиллуулах

### Өөр хувилбарууд

GitHub нь цорын ганц биш:

| Үйлчилгээ | Онцлог |
|---|---|
| GitHub | Хамгийн том, нээлттэй эхэд түгээмэл |
| GitLab | Өөрийн сервер дээр суулгаж болно |
| Bitbucket | Atlassian-ы бүтээгдэхүүнтэй холбогдоно |

Гурвуулаа **ижил Git**-ийг ашиглана. Тиймээс Git сурвал хаана ч
ажиллана.

### Ердийн урсгал

```text
Таны компьютер              GitHub
─────────────              ──────
өөрчлөлт хийнэ
git add
git commit        ──push──>  хадгалагдана
                  <──pull──  багийнхны өөрчлөлт
```

`push` нь дээш илгээх, `pull` нь доош татах.

> Git-ийг сурахад **эхлээд локал** дээр дадлагажаарай. GitHub-ийг дараа
> нь нэмэх нь хамаагүй хялбар.
""",
            initial_code="""\
# Урьдчилан харах: тушаал бүрийг Модул 2–7-д нэг бүрчлэн үзнэ. Одоо
# зөвхөн аль нь локал, аль нь GitHub-тай ажилладгийг ажигла.

# --- Git: локал, интернэт шаардахгүй ---
git init
git add .
git commit -m "Анхны commit"
git log
git branch bolomj
git checkout bolomj

# Дээрх бүгд интернэтгүйгээр ажиллана.

# --- GitHub: алсын хуулбартай холбох ---
git remote add origin https://github.com/hereglegch/tusul.git
git push -u origin main

# Багийнхны өөрчлөлтийг татах
git pull

# Алсын жагсаалт
git remote -v
""",
        ),
        LessonSpec(
            title="Локал ба алсын агуулах",
            slug="lokal-ba-alsiin",
            description="Хоёр хуулбар хэрхэн зэрэгцэн оршдог вэ.",
            duration=400,
            language=SH,
            content="""\
### Агуулах (repository)

**Агуулах** нь төслийн файлууд **болон** түүний бүтэн түүх. Git нь
түүхийг `.git` гэсэн далд хавтсанд хадгална.

```bash
ls -a
# .git  README.md  main.c
```

> `.git` хавтсыг **гараар бүү засвар**. Устгавал бүх түүх алга болно —
> файлууд үлдэнэ ч түүх сэргэхгүй.

### Локал ба алсын

| | Локал | Алсын (remote) |
|---|---|---|
| Хаана | Таны компьютер | GitHub сервер |
| Хэн хандана | Зөвхөн та | Эрх бүхий хүн бүр |
| Хурд | Шууд | Сүлжээнээс хамаарна |

**Хоёулаа бүтэн түүхтэй.** Энэ нь Git-ийн тархсан шинж — алсын хуулбар
нь «эх» биш, зүгээр л нэг хуулбар.

### `origin`

Алсын агуулахын анхдагч нэр нь `origin`. Энэ бол зүгээр л нэр — өөрчилж
болно, хэд хэдэн алсыг нэмж болно.

```bash
git remote -v
# origin  https://github.com/ner/tusul.git (fetch)
# origin  https://github.com/ner/tusul.git (push)
```

### Гурван үндсэн үйлдэл

```bash
git clone <хаяг>    # алсын хуулбарыг бүтнээр нь татаж авна
git push            # локал commit-уудыг дээш илгээнэ
git pull            # алсын өөрчлөлтийг доош татна
```

### Ажлын урсгал

```text
1. git pull          багийнхны сүүлийн ажлыг ав
2. өөрчлөлт хий
3. git add           бэлтгэ
4. git commit        түүхэнд тэмдэглэ
5. git push          бусадтай хуваалц
```

Энэ таван алхам нь өдөр тутмын ажлын 90 хувийг эзэлнэ.

### Яагаад эхлээд `pull` вэ

Бусад хүн ажиллаж байсан бол таны `push` **татгалзагдана**. Эхлээд
татвал энэ асуудал гарахгүй бөгөөд зөрчлийг эрт олно.
""",
            initial_code="""\
# Урьдчилан харах: clone, remote, pull, push-ийг Модул 5-д нарийн үзнэ.
# Одоо зөвхөн локал ба алсын хооронд юу шилждэгийг ажигла.

# --- Одоо байгаа төслийг татаж авах ---
git clone https://github.com/hereglegch/tusul.git
cd tusul

# clone нь БҮТЭН түүхийг татна — зөвхөн файлыг биш
git log --oneline | head -20

# --- Алсын тохиргоог харах ---
git remote -v
git remote show origin

# --- Өдөр тутмын урсгал ---
git pull                          # 1. багийнхны ажлыг ав
# ... файлаа засна ...
git add README.md                 # 3. бэлтгэ
git commit -m "Танилцуулга нэмэв" # 4. тэмдэглэ
git push                          # 5. хуваалц

# --- Локал ба алсын ялгааг харах ---
git status
git log origin/main..HEAD --oneline   # илгээгээгүй commit-ууд
""",
        ),
    ],
)

SETUP = ModuleSpec(
    title="Модул 1 — Git тохируулах",
    description="Суулгах, нэр имэйл тохируулах.",
    lessons=[
        LessonSpec(
            title="Git суулгах ба терминал",
            slug="git-suulgah",
            description="Windows, macOS, Linux дээр суулгах.",
            duration=360,
            language=SH,
            content="""\
### Суулгах

| Систем | Арга |
|---|---|
| Windows | [git-scm.com](https://git-scm.com) — Git Bash хамт ирнэ |
| macOS | `brew install git` эсвэл Xcode хэрэгсэл |
| Linux | `sudo apt install git` (Debian/Ubuntu) |

Шалгах:

```bash
git --version
# git version 2.43.0
```

### Windows дээрх Git Bash

Windows-ийн `cmd` нь Unix тушаалуудыг мэдэхгүй. Git суулгахад **Git
Bash** хамт ирнэ — энэ нь Linux/macOS-тай ижил орчин өгнө.

Сургалтын бүх тушаал Git Bash дээр ажиллана.

### Хэрэгтэй терминалын тушаалууд

```bash
pwd                  # одоо хаана байгаа вэ
ls                   # файлуудыг харуулна
ls -a                # далд файлыг ч харуулна (.git гэх мэт)
cd tusul             # хавтас руу орно
cd ..                # нэг шат дээш
mkdir shine          # хавтас үүсгэнэ
```

`cd` дараа **Tab** дарвал нэрийг автоматаар гүйцээнэ. Урт нэр бичихээс
хэмнэнэ.

### Мөр таслалтын анхааруулга

Windows нь мөрийг `CRLF`, Unix нь `LF` -ээр таслана. Хольсон баг дээр
энэ нь хуурамч өөрчлөлт үүсгэнэ:

```bash
# Windows дээр
git config --global core.autocrlf true

# macOS / Linux дээр
git config --global core.autocrlf input
```

Илүү найдвартай арга нь төсөлд `.gitattributes` файл нэмэх:

```text
* text=auto eol=lf
```

Ингэснээр хүн бүрийн тохиргооноос үл хамааран агуулахад `LF` хадгалагдана.

### Засварлагч

Git заримдаа засварлагч нээнэ (урт commit мессеж, rebase). Анхдагч нь
`vim` — танил биш бол солиорой:

```bash
git config --global core.editor "code --wait"    # VS Code
git config --global core.editor "nano"           # энгийн
```

> `vim` дотор гацвал: `Esc` дараад `:q!` бичээд Enter. Энэ нь «хадгалахгүй
> гарах» гэсэн утгатай.
""",
            initial_code="""\
# --- Суулгасан эсэхээ шалгах ---
git --version

# --- Терминалын үндсэн тушаалууд ---
pwd                    # одоо хаана байна вэ
ls -a                  # далд файлыг ч харуулна
cd tusul               # хавтас руу орох
cd ..                  # нэг шат дээш
mkdir shine-tusul      # хавтас үүсгэх

# --- Мөр таслалт (Windows дээр заавал) ---
git config --global core.autocrlf true

# macOS / Linux дээр:
# git config --global core.autocrlf input

# --- Засварлагчийг солих ---
git config --global core.editor "code --wait"

# vim дотор гацвал: Esc дараад :q! бичээд Enter

# --- Тусламж ---
git help commit
git commit --help
""",
        ),
        LessonSpec(
            title="git config",
            slug="git-config",
            description="Нэр, имэйл болон бусад тохиргоо.",
            duration=400,
            language=SH,
            content="""\
### Нэр ба имэйл — заавал

Commit бүрт зохиогчийн нэр, имэйл бичигдэнэ. Тохируулаагүй бол Git
commit хийхийг зөвшөөрөхгүй.

```bash
git config --global user.name "Бат Болд"
git config --global user.email "bat@jishee.mn"
```

> GitHub дээр ашигладаг имэйлээ бич — эс бөгөөс commit тань таны
> бүртгэлтэй холбогдохгүй бөгөөд профайл дээр харагдахгүй.

### Гурван түвшин

| Түвшин | Тушаал | Хаана хадгалагдана |
|---|---|---|
| Систем | `--system` | Бүх хэрэглэгчид |
| Хэрэглэгч | `--global` | `~/.gitconfig` |
| Төсөл | (туггүй) | `.git/config` |

Доод түвшин нь дээдийг **дарж бичнэ**. Ажлын төсөлд өөр имэйл
хэрэгтэй бол:

```bash
cd ~/ajil/tusul
git config user.email "bat@kompani.mn"
```

Энэ нь зөвхөн тэр төсөлд хамаарна.

### Харах

```bash
git config --list                    # бүгд
git config user.name                 # нэг утга
git config --list --show-origin      # аль файлаас ирснийг харуулна
```

Сүүлийнх нь «яагаад энэ утга ийм байна вэ» гэсэн асуултад хариулна.

### Үндсэн салааны нэр

```bash
git config --global init.defaultBranch main
```

Git-ийн хуучин анхдагч нэр нь `master` байсан. Өнөөдөр ихэнх төсөл
`main` ашигладаг тул шинэ агуулах бүрт гараар солихгүйн тулд энэ
тохиргоог хий.

### Товчлол (alias)

Байнга бичдэг тушаалыг богиносгоно:

```bash
git config --global alias.st status
git config --global alias.lg "log --oneline --graph --all"
```

Одоо `git st` нь `git status`-тай ижил.

### Тохиргоог шалгах

```bash
git config user.name
git config user.email
```

Шинэ компьютер дээр эхлэхэд хамгийн түрүүнд эдгээрийг хий. Мартвал
commit-ууд тань буруу нэрээр бүртгэгдэнэ.
""",
            initial_code="""\
# --- Заавал хийх хоёр тохиргоо ---
git config --global user.name "Бат Болд"
git config --global user.email "bat@jishee.mn"

# GitHub-д ашигладаг имэйлээ бич — эс бөгөөс commit тань
# таны профайлтай холбогдохгүй.

# --- Зөвлөмжтэй тохиргоо ---
git config --global init.defaultBranch main
git config --global core.editor "code --wait"
git config --global pull.rebase false

# --- Товчлол ---
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.lg "log --oneline --graph --all --decorate"

# --- Шалгах ---
git config --list
git config user.name
git config user.email

# Аль файлаас ирснийг харуулна — «яагаад ийм утгатай вэ» гэдгийг хэлнэ
git config --list --show-origin

# --- Зөвхөн энэ төсөлд өөр имэйл ---
cd ~/ajil/tusul
git config user.email "bat@kompani.mn"
""",
        ),
    ],
)

GIT_FUNDAMENTAL_MODULES = [FUNDAMENTALS, SETUP]
