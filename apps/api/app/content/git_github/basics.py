"""Модул 2-5 — Үндсэн тушаал, ажлын урсгал, GitHub, алсын агуулах.

Өдөр тутам хэрэглэгдэх тушаалууд. Эдгээрийг эзэмшвэл ажлын 90 хувийг
хийж чадна.
"""

from app.content.types import LessonSpec, ModuleSpec
from app.models.enums import LessonLanguage

SH = LessonLanguage.SHELL

BASICS = ModuleSpec(
    title="Модул 2 — Git-ийн үндсэн тушаалууд",
    description="init, status, add, commit, log, diff.",
    lessons=[
        LessonSpec(
            title="git init ба git status",
            slug="git-init-ba-status",
            description="Агуулах үүсгэх, төлөв харах.",
            duration=400,
            language=SH,
            content="""\
### `git init`

Одоогийн хавтсыг Git агуулах болгоно:

```bash
cd miniy-tusul
git init
```

`.git` далд хавтас үүснэ. Энэ дотор бүх түүх хадгалагдана.

> Аль хэдийн агуулах доторх хавтсанд `git init` **бүү** ажиллуул.
> Үүрлэсэн агуулах нь төөрөгдөл үүсгэнэ. `git status`-аар эхлээд шалга.

### `git status` — хамгийн их хэрэглэгдэх тушаал

```bash
git status
```

Гурван зүйлийг хэлнэ:

1. Аль салаан дээр байгаа
2. Ямар файл өөрчлөгдсөн
3. Юу нь бэлтгэгдсэн, юу нь үгүй

```text
On branch main

Changes to be committed:
        new file:   README.md

Changes not staged for commit:
        modified:   main.c

Untracked files:
        tur.txt
```

### Файлын гурван төлөв

| Төлөв | Утга |
|---|---|
| Untracked | Git энэ файлыг мэдэхгүй |
| Modified | Өөрчлөгдсөн, гэхдээ бэлтгэгдээгүй |
| Staged | Дараагийн commit-д орохоор бэлтгэгдсэн |

### Богино хэлбэр

```bash
git status -s
```

```text
A  README.md
 M main.c
?? tur.txt
```

Эхний багана нь бэлтгэсэн байдал, хоёр дахь нь ажлын хавтас дахь байдал.

### Эргэлзвэл `status`

Git сурах явцад **тушаал бүрийн дараа** `git status` ажиллуул. Тэр нь
юу болсныг хэлж, ихэвчлэн дараа нь юу хийхийг зөвлөнө:

```text
  (use "git restore --staged <file>..." to unstage)
```

Git-ийн зөвлөмжийг унших нь хамгийн хурдан сурах арга.

### Байгаа төсөлд `init` хэрэггүй

GitHub дээр байгаа төслийг компьютер руугаа татахад `git clone` гэсэн
тушаал ашигладаг. Тэр нь агуулахыг өөрөө бэлддэг тул `git init` хийх
шаардлагагүй. `clone`-ийг Модул 5-д үзнэ — одоохондоо өөрийн шинэ
төсөлд `git init` л хэрэгтэй.
""",
            initial_code="""\
# --- Шинэ агуулах ---
mkdir miniy-tusul
cd miniy-tusul
git init

# .git хавтас үүссэн эсэхийг харах
ls -a

# --- Төлөв харах ---
git status

# Файл үүсгээд дахин харах
echo "# Миний төсөл" > README.md
git status

# Untracked гэж гарна — Git энэ файлыг хараахан мэдэхгүй

# --- Богино хэлбэр ---
git status -s

# --- Энэ хавтас агуулах мөн эсэхийг шалгах ---
git rev-parse --is-inside-work-tree
""",
        ),
        LessonSpec(
            title="git add ба git commit",
            slug="git-add-ba-commit",
            description="Өөрчлөлтийг бэлтгэж түүхэнд тэмдэглэх.",
            duration=450,
            language=SH,
            content="""\
### `git add` — бэлтгэх

```bash
git add README.md          # нэг файл
git add src/               # бүтэн хавтас
git add .                  # бүх өөрчлөлт
```

`add` нь өөрчлөлтийг **бэлтгэх талбарт** (staging area) оруулна. Commit
хийх хүртэл түүхэнд ороогүй.

> `git add .` нь хурдан ч болгоомжтой. Санамсаргүй нууц үг, түр файл
> оруулж магадгүй. Эхлээд `git status`-аар шалга.

### `git commit` — тэмдэглэх

```bash
git commit -m "Танилцуулга нэмэв"
```

Бэлтгэгдсэн бүх зүйлийг **нэг** commit болгоно.

### Яагаад хоёр алхам вэ

Энэ нь ямар өөрчлөлтүүд **хамт** орохыг сонгох боломж өгнө:

```bash
# Хоёр өөр ажил хийсэн. Тусад нь commit хийе.
git add src/nevtreh.c
git commit -m "Нэвтрэх алдааг зассан"

git add README.md
git commit -m "Баримт бичиг шинэчлэв"
```

Нэг commit нэг санааг агуулах нь түүхийг уншигдахуйц болгоно. Буцаах
шаардлага гарвал зөвхөн хэрэгтэйг нь буцаана.

### Сайн commit мессеж

| Муу | Сайн |
|---|---|
| «засвар» | «Нэвтрэхэд хоосон нууц үг зөвшөөрч байсныг зассан» |
| «шинэчлэл» | «Хэрэглэгчийн жагсаалтад хуудаслалт нэмэв» |
| «ажиллаж байна» | «Тайлан татахад timeout нэмэв» |

Дүрмүүд:

- Эхний мөр 50 тэмдэгтээс богино
- **Юу** хийснийг биш **яагаад** хийснийг тайлбарла
- Тушаал хэлбэрээр бич: «нэмэв» биш «нэм» ч болно — төслийн журмыг дага

Урт тайлбар хэрэгтэй бол:

```bash
git commit
```

Засварлагч нээгдэнэ. Эхний мөр гарчиг, хоосон мөр, дараа нь дэлгэрэнгүй.

### Бүгдийг нэг дор

```bash
git commit -am "Мессеж"
```

`-a` нь **өөрчлөгдсөн** файлыг автоматаар бэлтгэнэ. Гэхдээ **шинэ**
файлыг оруулахгүй — тэдгээрт `git add` заавал хэрэгтэй.

### Сүүлийн commit-ыг засах

```bash
git commit --amend -m "Зассан мессеж"
```

`--amend` нь сүүлийн commit-ыг шинэ мессежтэй (мөн бэлтгэсэн өөрчлөлттэй)
нь **дахин** хийнэ.

> Зөвхөн GitHub руу **илгээгээгүй** (push хийгээгүй, Модул 5) commit дээр
> ашигла. Илгээсний дараа түүхийг өөрчлөх нь багийнхны ажлыг эвдэнэ.

### Бэлтгэснийг буцаах

Буруу файл `git add` хийчихвэл:

```bash
git restore --staged README.md
```

Файл бэлтгэх талбараас гарна, харин доторх өөрчлөлт нь хавтсандаа
**үлдэнэ**. `git status` өөрөө энэ тушаалыг зөвлөдөг. Бусад буцаах
аргуудыг Модул 10-д үзнэ.
""",
            initial_code="""\
# --- Бэлтгэх ---
git add README.md              # нэг файл
git add src/                   # хавтас
git add .                      # бүгд — эхлээд status-аар шалга

# Юу бэлтгэгдсэнийг харах
git status

# --- Тэмдэглэх ---
git commit -m "Танилцуулга нэмэв"

# --- Тусад нь commit хийх ---
git add src/nevtreh.c
git commit -m "Нэвтрэхэд хоосон нууц үг зөвшөөрч байсныг зассан"

git add README.md
git commit -m "Суулгах зааврыг шинэчлэв"

# --- Урт тайлбартай commit ---
git commit
# Засварлагч нээгдэнэ:
#   Эхний мөр — гарчиг (50 тэмдэгтээс богино)
#   Хоосон мөр
#   Дэлгэрэнгүй тайлбар

# --- Богино хэлбэр (ЗӨВХӨН өөрчлөгдсөн файлд) ---
git commit -am "Жижиг засвар"

# --- Сүүлийн commit-ыг засах (push хийгээгүй бол) ---
git commit --amend -m "Зассан мессеж"

# --- Бэлтгэснийг буцаах ---
git restore --staged README.md
""",
        ),
        LessonSpec(
            title="git log ба git diff",
            slug="git-log-ba-diff",
            description="Түүх болон өөрчлөлтийг харах.",
            duration=420,
            language=SH,
            content="""\
### `git log`

```bash
git log
```

```text
commit a1b2c3d4e5f6...
Author: Бат Болд <bat@jishee.mn>
Date:   Fri Sep 13 10:22:31 2026 +0800

    Нэвтрэх алдааг зассан
```

Дэлгэрэнгүй боловч урт. Илүү хэрэгтэй хэлбэрүүд:

```bash
git log --oneline              # нэг commit нэг мөр
git log --oneline --graph      # салааг зурна
git log -5                     # сүүлийн 5
git log --author="Бат"         # тодорхой хүний
git log --since="2 weeks ago"
git log -- src/main.c          # тодорхой файлын түүх
```

Хамгийн түгээмэл хослол:

```bash
git log --oneline --graph --all --decorate
```

Үүнийг товчлол болгож тохируулах нь зүйтэй (Модул 1).

### `git log` дотроос гарах

Урт гаралт нь хуудаслагчид орно. **`q`** дарж гарна. Энэ нь эхлэгчдийн
байнга гацдаг газар.

### `git diff` — өөрчлөлтийг харах

```bash
git diff                  # бэлтгээгүй өөрчлөлт
git diff --staged         # бэлтгэсэн өөрчлөлт
git diff HEAD             # хоёуланг нь
```

```text
-    if (nuuts == NULL) {
+    if (nuuts == NULL || strlen(nuuts) == 0) {
```

`-` нь хассан мөр, `+` нь нэмсэн.

### Аль нь аль нь вэ

| Тушаал | Юуг харуулах |
|---|---|
| `git diff` | Ажлын хавтас ↔ бэлтгэх талбар |
| `git diff --staged` | Бэлтгэх талбар ↔ сүүлийн commit |
| `git diff HEAD` | Ажлын хавтас ↔ сүүлийн commit |

`git add` хийсний дараа `git diff` нь **хоосон** гарна — энэ нь алдаа
биш. `--staged` ашигла.

### Commit хоорондын ялгаа

```bash
git diff a1b2c3d 9f8e7d6
git diff HEAD~3 HEAD           # сүүлийн 3 commit-ийн ялгаа
```

`HEAD` нь одоогийн commit, `HEAD~1` нь өмнөх нь. Хоёр салааны ялгааг ч
ингэж харж болно — салааг Модул 6-д үзнэ.

### Commit-ийн агуулгыг харах

```bash
git show a1b2c3d
git show HEAD
```

Мессеж болон бүх өөрчлөлтийг хамт харуулна.

### Commit хийхийн өмнө шалга

```bash
git add .
git diff --staged
git commit -m "…"
```

Энэ зуршил нь санамсаргүй өөрчлөлт, дибагийн `print`, нууц үг орохоос
сэргийлнэ.
""",
            initial_code="""\
# --- Түүх ---
git log                              # дэлгэрэнгүй
git log --oneline                    # нэг мөр
git log --oneline --graph --all      # салаатай
git log -5                           # сүүлийн 5

# Урт гаралтаас гарах: q дарна

# Шүүх
git log --author="Бат"
git log --since="2 weeks ago"
git log --oneline -- src/main.c      # тодорхой файлын түүх

# --- Ялгаа ---
git diff                             # бэлтгээгүй өөрчлөлт
git diff --staged                    # бэлтгэсэн өөрчлөлт
git diff HEAD                        # хоёуланг нь

# git add хийсний дараа git diff ХООСОН гарна — --staged ашигла

# --- Commit хоорондын ---
git diff HEAD~3 HEAD

# --- Нэг commit-ийн бүх мэдээлэл ---
git show HEAD
git show a1b2c3d

# --- Commit хийхийн ӨМНӨ шалгах зуршил ---
git add .
git diff --staged
git commit -m "Шалгасны дараа commit хийв"
""",
        ),
    ],
)

WORKFLOW = ModuleSpec(
    title="Модул 3 — Git-ийн ажлын урсгал",
    description="Гурван талбар хоорондоо хэрхэн ажилладаг вэ.",
    lessons=[
        LessonSpec(
            title="Гурван талбар",
            slug="gurvan-heseg",
            description="Ажлын хавтас, бэлтгэх талбар, агуулах.",
            duration=420,
            language=SH,
            content="""\
Git-ийг ойлгоход хамгийн чухал загвар:

```text
Ажлын хавтас        Бэлтгэх талбар        Агуулах
(working dir)       (staging area)        (.git)
     │                     │                  │
     │──── git add ───────>│                  │
     │                     │──── git commit ─>│
     │<─────────── git restore ───────────────│
```

### 1. Ажлын хавтас

Таны харж, засварлаж буй файлууд. Git энд юу ч хийхгүй — та л
өөрчилнө.

### 2. Бэлтгэх талбар

**Дараагийн commit-д юу орохыг** сонгох завсрын талбар. Энэ бол Git-ийн
өвөрмөц санаа — ихэнх систем үүнгүй.

Яагаад хэрэгтэй вэ: нэг удаад **олон зүйл** засварласан ч тэдгээрийг
**тусад нь** commit хийж чадна.

```bash
git add src/nevtreh.c        # зөвхөн энэ засварыг
git commit -m "Нэвтрэх зассан"

git add README.md            # дараа нь энэ нь
git commit -m "Баримт шинэчлэв"
```

### 3. Агуулах

`.git` доторх бүх түүх. Commit хийсний дараа өөрчлөлт энд **бүрмөсөн**
хадгалагдана.

### Хэсэгчилсэн бэлтгэл

Нэг файлын **зарим мөрийг** л бэлтгэж болно:

```bash
git add -p main.c
```

Git өөрчлөлтийг хэсэг хэсгээр асууна: `y` бэлтгэ, `n` алгас, `s` жижиг
хэсэгт хуваа.

Нэг файлд хоёр өөр ажил хийсэн үед энэ нь маш хэрэгтэй.

### Төлөв шалгах

```bash
git status                # ерөнхий
git diff                  # бэлтгээгүй өөрчлөлт
git diff --staged         # бэлтгэсэн өөрчлөлт
```

### Буцаах

```bash
git restore --staged file    # бэлтгэснийг буцаана (өөрчлөлт үлдэнэ)
git restore file             # өөрчлөлтийг УСТГАНА
```

> Хоёр дахийг болгоомжтой ашигла — commit хийгээгүй өөрчлөлт **буцаж
> ирэхгүй**. `git restore`-ийн бусад хэрэглээг Модул 10-д үзнэ.
""",
            initial_code="""\
# --- Гурван талбарыг ажиглах ---

# 1. Ажлын хавтас — файлаа засна
echo "шинэ мөр" >> README.md
git status                     # «not staged» гэж гарна

# 2. Бэлтгэх талбар
git add README.md
git status                     # «to be committed» болов

# 3. Агуулах
git commit -m "README шинэчлэв"
git status                     # цэвэр

# --- Хоёр ажлыг ТУСАД нь commit хийх ---
git add src/nevtreh.c
git commit -m "Нэвтрэх алдааг зассан"

git add README.md
git commit -m "Баримт бичиг шинэчлэв"

# --- Хэсэгчилсэн бэлтгэл ---
git add -p main.c
# y = бэлтгэ, n = алгас, s = жижиг хэсэгт хуваа, q = гарах

# --- Аль талбарт юу байгааг харах ---
git diff                       # ажлын хавтас ↔ бэлтгэх талбар
git diff --staged              # бэлтгэх талбар ↔ сүүлийн commit

# --- Буцаах ---
git restore --staged README.md   # бэлтгэснийг буцаана, өөрчлөлт үлдэнэ
# git restore README.md          # өөрчлөлтийг УСТГАНА — эргэж ирэхгүй
""",
        ),
        LessonSpec(
            title="Commit-ийн урсгал",
            slug="commit-urgats",
            description="Өдөр тутмын ажлын дараалал.",
            duration=400,
            language=SH,
            content="""\
### Өдөр тутмын мөчлөг

```text
1. өөрчлөлт хий
2. git status          юу өөрчлөгдснийг хар
3. git diff            агуулгыг нь шалга
4. git add             хэрэгтэйг нь бэлтгэ
5. git diff --staged   дахин шалга
6. git commit -m "…"   тэмдэглэ
```

Эхэндээ урт санагдана. Хэдэн өдрийн дараа автоматаар болно.

GitHub-тай ажиллаж эхлэхэд (Модул 5) энэ мөчлөгийн **эхэнд** багийнхны
ажлыг татах `git pull`, **төгсгөлд** өөрийнхөө ажлыг илгээх `git push`
нэмэгдэнэ.

### Хэр олон commit хийх вэ

> Нэг commit нь **нэг бүрэн санаа** байх ёстой. Ажиллахгүй код бүү
> commit хий, гэхдээ өдрийн эцэс хүртэл ч бүү хүлээ.

Сайн хэмжээ:

| Хэт жижиг | Зөв | Хэт том |
|---|---|---|
| «үсгийн алдаа зассан» × 20 | «Нэвтрэх маягтын шалгалт нэмэв» | «Долоо хоногийн ажил» |

### Юуг commit хийхгүй вэ

- Нууц үг, API түлхүүр — **хэзээ ч**
- `node_modules/`, `.venv/` — дахин үүсгэж болно
- Хөрвүүлсэн файл (`.exe`, `.o`, `dist/`)
- Засварлагчийн тохиргоо (`.vscode/`, `.idea/`)
- Үйлдлийн системийн хог (`.DS_Store`, `Thumbs.db`)

Эдгээрийг `.gitignore`-д бич (Модул 4).

### Нууц үг орсон бол

```bash
# Commit хийгээд GitHub руу хараахан ИЛГЭЭГЭЭГҮЙ бол
git reset --soft HEAD~1
```

`git reset --soft HEAD~1` нь сүүлийн commit-ыг буцаана, харин түүний
өөрчлөлтүүд бэлтгэх талбартаа **үлдэнэ**. Нууц үгээ файлаас авч, дахин
commit хийнэ. `reset`-ийг Модул 10-д нарийн үзнэ.

> GitHub руу илгээсэн (push хийсэн, Модул 5) бол түүнийг устгах нь
> хангалтгүй — түүхэнд үлдэнэ. Тэр түлхүүрийг **тэр дор нь хүчингүй
> болгож**, шинээр үүсгэ. Энэ бол цорын ганц найдвартай арга.

### Ажлаа тогтмол хадгал

Commit нь одоохондоо зөвхөн таны компьютер дээр хадгалагдана — диск
эвдэрвэл түүх ч алга. Модул 5-д `git push`-ээр GitHub руу илгээж сурна.
Тэр үеэс өдөр бүрийн эцэст push хийх зуршилтай бол.

### Юу болж байгааг мэдэхгүй бол

```bash
git status
git log --oneline -5
```

Энэ хоёр тушаал бараг бүх асуултад хариулна.
""",
            initial_code="""\
# --- Өдөр тутмын бүрэн мөчлөг ---

# 1. Өөрчлөлт хий
# ... файлаа засна ...

# 2-3. Юу өөрчлөгдснийг шалга
git status
git diff

# 4-5. Бэлтгээд дахин шалга
git add src/nevtreh.c
git diff --staged

# 6. Тэмдэглэ
git commit -m "Нэвтрэхэд хоосон нууц үг зөвшөөрч байсныг зассан"

# (Модул 5-аас хойш: эхэнд git pull, төгсгөлд git push нэмэгдэнэ)

# --- Өдрийн эцэст ---
git status                   # орхигдсон зүйл байна уу

# --- Санамсаргүй нууц үг commit хийсэн бол ---
# GitHub руу ИЛГЭЭГЭЭГҮЙ бол: сүүлийн commit-ыг буцаана,
# өөрчлөлт нь бэлтгэх талбартаа үлдэнэ (reset-ийг Модул 10-д үзнэ)
git reset --soft HEAD~1
# Файлаас нууц үгээ авч, .gitignore-д нэм, дахин commit хий

# ИЛГЭЭСЭН (push хийсэн) бол: тэр түлхүүрийг ТЭР ДОР НЬ хүчингүй болго.
# Түүхээс устгах нь хангалтгүй.

# --- Төөрвөл ---
git status
git log --oneline -5
""",
        ),
    ],
)

GITHUB_BASICS = ModuleSpec(
    title="Модул 4 — GitHub-ийн үндэс",
    description="Бүртгэл, агуулах, README, .gitignore.",
    lessons=[
        LessonSpec(
            title="Бүртгэл ба агуулах үүсгэх",
            slug="github-burtgel-ba-aguulah",
            description="Данс нээх, эхний агуулах, нээлттэй ба хаалттай.",
            duration=420,
            language=SH,
            content="""\
### Бүртгэл

[github.com](https://github.com) дээр үнэгүй данс нээнэ. Хэрэглэгчийн
нэр тань олон нийтэд харагдана — ажил мэргэжлийн хувьд тохиромжтойг
сонго.

### Хоёр хүчин зүйлийн баталгаажуулалт

GitHub нь 2FA шаарддаг. Утасны апп (Authy, Google Authenticator) эсвэл
аюулгүй байдлын түлхүүр ашиглана. Сэргээх кодоо **аюулгүй газар
хадгал**.

### Агуулах үүсгэх

**New repository** товч дарна:

| Талбар | Тайлбар |
|---|---|
| Нэр | Жижиг үсэг, зураас: `miniy-tusul` |
| Тайлбар | Нэг өгүүлбэрээр |
| Public / Private | Доор үзнэ |
| README нэмэх | Тийм — эхлэхэд хялбар |
| .gitignore | Хэлээ сонго |
| Лиценз | Нээлттэй бол хэрэгтэй |

### Нээлттэй ба хаалттай

| | Public | Private |
|---|---|---|
| Хэн харах вэ | Хүн бүр | Зөвхөн урьсан хүн |
| Үнэ | Үнэгүй | Үнэгүй (хязгаартай) |
| Хэзээ | Портфолио, нээлттэй эх | Хувийн, ажлын |

> Public агуулахад юу байгааг **сайн бод**. Түүхэнд орсон нууц үг нь
> файлыг устгасан ч үлдэнэ.

### Локал төслийг холбох

Аль хэдийн локал агуулахтай бол GitHub шинэ хоосон агуулахын хуудсан
дээрээ яг эдгээр гурван мөрийг хуулж ажиллуулахыг санал болгодог:

```bash
git remote add origin https://github.com/ner/tusul.git
git branch -M main
git push -u origin main
```

Одоохондоо товч утгыг нь мэдэхэд хангалттай — Модул 5, 6-д нарийн үзнэ:

- `git remote add origin <хаяг>` — GitHub дээрх агуулахыг `origin` гэсэн
  нэрээр бүртгэнэ.
- `git branch -M main` — одоогийн салааг `main` гэж нэрлэнэ (салаа —
  Модул 6).
- `git push -u origin main` — commit-уудаа GitHub руу **илгээнэ**. `-u`
  нь дараагийн удаа зүгээр `git push` гэж бичихэд хангалттай болгоно.

### Нэвтрэлт

GitHub нь нууц үгээр push хийхийг **зөвшөөрөхгүй**. Хоёр сонголт:

**1. Personal access token** — HTTPS ашиглана. Settings → Developer
settings → Tokens. Нууц үгийн оронд түүнийг бичнэ.

**2. SSH түлхүүр** — илүү тохиромжтой:

```bash
ssh-keygen -t ed25519 -C "bat@jishee.mn"
cat ~/.ssh/id_ed25519.pub
```

Гарсан текстийг GitHub → Settings → SSH keys рүү хуулна.

### Лиценз

Лицензгүй код нь **хуулбарлах эрхгүй** гэсэн үг — хэн ч ашиглаж
чадахгүй. Нээлттэй байлгах бол MIT эсвэл Apache 2.0 сонго.
""",
            initial_code="""\
# --- Локал төслийг GitHub-тай холбох ---
# GitHub шинэ агуулахын хуудсан дээр санал болгодог гурван мөр
# (Модул 5, 6-д нарийн үзнэ):
git remote add origin https://github.com/hereglegch/tusul.git   # хаягийг origin нэрээр бүртгэнэ
git branch -M main                                              # салааг main гэж нэрлэнэ
git push -u origin main                                         # commit-уудаа GitHub руу илгээнэ

# -u нь дараа нь зүгээр «git push» гэж бичихэд хангалттай болгоно

# --- Бүртгэсэн хаягийг шалгах ---
git remote -v

# --- SSH түлхүүр үүсгэх (зөвлөмжтэй) ---
ssh-keygen -t ed25519 -C "bat@jishee.mn"
cat ~/.ssh/id_ed25519.pub
# Гарсан текстийг GitHub -> Settings -> SSH keys рүү хуулна

# Холболтыг шалгах
ssh -T git@github.com

# --- HTTPS-ээс SSH рүү шилжих: origin-ий хаягийг SSH хаягаар солино ---
git remote set-url origin git@github.com:hereglegch/tusul.git

# GitHub дээр үүсгэсэн агуулахыг компьютер руугаа татах git clone-ийг
# Модул 5-д үзнэ.
""",
        ),
        LessonSpec(
            title="README.md",
            slug="readme",
            description="Төслийн нүүр хуудас.",
            duration=380,
            language=SH,
            content="""\
`README.md` нь агуулахын нүүр хуудсанд **автоматаар** харагдана. Энэ
бол таны төслийн анхны сэтгэгдэл.

### Юу бичих вэ

```markdown
# Төслийн нэр

Нэг өгүүлбэрээр юу хийдгийг тайлбарла.

## Суулгах

```bash
npm install
```

## Ашиглах

```bash
npm start
```

## Лиценз

MIT
```

### Уншигчийн гурван асуулт

Сайн README нь эхний дэлгэц дотор гурван зүйлд хариулна:

1. **Энэ юу вэ?**
2. **Надад хэрэгтэй юу?**
3. **Хэрхэн эхлэх вэ?**

Урт түүх, архитектурын тайлбар доор нь орно.

### Markdown-ийн үндэс

```markdown
# Гарчиг 1
## Гарчиг 2

**тод**  *налуу*  `код`

- жагсаалт
1. дугаарласан

[холбоос](https://jishee.mn)
![зураг](zurag.png)

> Иш татсан

| Багана | Багана |
|---|---|
| утга | утга |
```

### Кодын блок

Хэлийг заавал бич — өнгө ялгаж харагдана:

````markdown
```bash
git clone https://github.com/ner/tusul.git
```
````

### Түгээмэл алдаанууд

| Алдаа | Засвар |
|---|---|
| Суулгах заавар байхгүй | Эхлээд үүнийг бич |
| Хуучирсан тушаал | Заримдаа өөрөө дагаж үзэж шалга |
| Зөвхөн нэр, өөр юу ч алга | Дор хаяж нэг өгүүлбэр нэм |
| Дэлгэцийн зураг байхгүй | UI төсөлд зураг нь мянган үг |

### Бусад хэрэгтэй файл

| Файл | Зорилго |
|---|---|
| `LICENSE` | Хуулбарлах эрх |
| `CONTRIBUTING.md` | Хэрхэн хувь нэмэр оруулах |
| `CHANGELOG.md` | Хувилбар бүрийн өөрчлөлт |
| `.github/` | Загвар, автоматжуулалт |

### Дадлага

Өөрийн төслийн README-г **өөр хүний нүдээр** уншаарай. Тэр хүн энэ
төслийг огт мэдэхгүй. Эхлэх гэж оролдоход хаана гацах вэ?
""",
            initial_code="""\
# --- README үүсгэх ---
cat > README.md << 'EOF'
# Миний төсөл

Оюутны дүнг тооцоолж, тайлан гаргадаг командын мөрийн хэрэгсэл.

## Суулгах

```bash
git clone https://github.com/hereglegch/tusul.git
cd tusul
npm install
```

## Ашиглах

```bash
npm start -- --fail dun.csv
```

## Шаардлага

- Node.js 20+

## Лиценз

MIT
EOF

git add README.md
git commit -m "README нэмэв"

# Өмнөх хичээлд «git push -u origin main»-оор холбосон бол GitHub руу
# илгээхэд зүгээр «git push» хангалттай (Модул 5-д нарийн үзнэ)
git push

# --- Markdown-ийг локал дээр урьдчилан харах ---
# VS Code дотор: Ctrl+Shift+V

# --- Лиценз нэмэх ---
# GitHub -> Add file -> Create new file -> «LICENSE» гэж бичвэл
# GitHub загвар санал болгоно
""",
        ),
        LessonSpec(
            title=".gitignore",
            slug="gitignore",
            description="Аль файлыг Git-д оруулахгүй вэ.",
            duration=400,
            language=SH,
            content="""\
Зарим файлыг **хэзээ ч** commit хийж болохгүй. `.gitignore` нь Git-д
тэдгээрийг үл тоомсорлохыг хэлнэ.

### Жишээ

```text
# Нууц
.env
*.key
secrets.json

# Хамаарал — дахин суулгаж болно
node_modules/
.venv/
vendor/

# Хөрвүүлсэн файл
*.o
*.exe
dist/
build/

# Засварлагч ба ОС
.vscode/
.idea/
.DS_Store
Thumbs.db

# Лог
*.log
```

### Дүрмүүд

| Бичлэг | Утга |
|---|---|
| `*.log` | Бүх `.log` файл |
| `build/` | `build` хавтас бүхэлдээ |
| `/tur.txt` | Зөвхөн үндсэн хавтас дахь |
| `!chuhal.log` | Үл хамаарах зүйл — энийг оруул |
| `# тайлбар` | Тайлбар |

### Аль хэдийн хянагдаж байгаа файлд ажиллахгүй

Энэ бол хамгийн түгээмэл төөрөгдөл:

```bash
# Файлыг аль хэдийн commit хийсэн бол .gitignore нэмэх нь ХАНГАЛТГҮЙ
git rm --cached .env
git commit -m ".env-ийг хяналтаас гаргав"
```

`--cached` нь **Git-ээс** хасна, дискнээс устгахгүй.

### Бүтэн хавтсыг

```bash
git rm -r --cached node_modules/
```

### Яагаад ингэдэг вэ

`.gitignore` нь зөвхөн **хянагдаагүй** файлд хамаарна. Нэг удаа
commit хийсэн файлыг Git үргэлжлүүлэн хянана.

### Шалгах

```bash
git status --ignored          # үл тоомсорлож буй файлууд
git check-ignore -v tur.log   # аль дүрэм барьж байгааг харуулна
```

Сүүлийнх нь «яагаад энэ файл орохгүй байна вэ» гэсэн асуултад хариулна.

### Бэлэн загвар

[github.com/github/gitignore](https://github.com/github/gitignore) дээр
хэл бүрт бэлэн загвар бий. Шинэ агуулах үүсгэхэд GitHub санал болгоно.

### Нууц үг орчихсон бол

> `.gitignore` нэмэх нь **хожимдсон**. Түүхэнд үлдсэн байна. Тэр
> түлхүүрийг хүчингүй болгож, шинээр үүсгэ. Энэ бол цорын ганц
> найдвартай засвар.
""",
            initial_code="""\
# --- .gitignore үүсгэх ---
cat > .gitignore << 'EOF'
# Нууц
.env
*.key

# Хамаарал
node_modules/
.venv/

# Хөрвүүлсэн файл
*.o
*.exe
dist/

# Засварлагч ба ОС
.vscode/
.idea/
.DS_Store
Thumbs.db

# Лог
*.log
!chuhal.log
EOF

git add .gitignore
git commit -m ".gitignore нэмэв"

# --- Аль хэдийн commit хийсэн файлыг хяналтаас гаргах ---
# .gitignore нэмэх нь ХАНГАЛТГҮЙ
git rm --cached .env
git commit -m ".env-ийг хяналтаас гаргав"

# Бүтэн хавтас
git rm -r --cached node_modules/
git commit -m "node_modules-ийг хяналтаас гаргав"

# --- Шалгах ---
git status --ignored
git check-ignore -v tur.log      # аль дүрэм барьж байгааг харуулна

# --- Бэлэн загвар ---
# https://github.com/github/gitignore
""",
        ),
    ],
)

REMOTES = ModuleSpec(
    title="Модул 5 — Алсын агуулах",
    description="remote, clone, push, pull, fetch.",
    lessons=[
        LessonSpec(
            title="git remote ба git clone",
            slug="git-remote-ba-clone",
            description="Алсын хуулбартай холбогдох.",
            duration=400,
            language=SH,
            content="""\
### `git clone`

Алсын агуулахыг **бүтнээр нь** татаж авна — файл, түүх, салаа бүгд:

```bash
git clone https://github.com/ner/tusul.git
cd tusul
```

`clone` нь дараах зүйлийг автоматаар хийнэ:

1. Хавтас үүсгэнэ
2. `git init` хийнэ
3. `origin` алсыг нэмнэ
4. Бүх түүхийг татна
5. Үндсэн салааг гаргана

Өөр нэрээр:

```bash
git clone https://github.com/ner/tusul.git miniy-hevleh
```

### `git remote`

Алсуудыг удирдана:

```bash
git remote -v                              # жагсаах
git remote add origin <хаяг>               # нэмэх
git remote remove origin                   # хасах
git remote set-url origin <шинэ хаяг>      # хаяг солих
git remote rename origin upstream          # нэр солих
```

### Хэд хэдэн алсын агуулах

Fork хийсэн төсөл дээр ажиллахад хоёр алс хэрэгтэй:

```bash
git remote -v
# origin    https://github.com/bi/tusul.git       (миний fork)
# upstream  https://github.com/ehiin/tusul.git    (эх төсөл)
```

`origin` руу push хийнэ, `upstream`-аас шинэчлэлт татна. Модул 8-д
дэлгэрэнгүй.

### Гүехэн clone

Том төслийн бүтэн түүх нь гигабайт байж болно:

```bash
git clone --depth 1 https://github.com/том/tusul.git
```

Зөвхөн сүүлийн commit-ыг татна. Хурдан, гэхдээ түүх байхгүй тул
хязгаарлагдмал.

### HTTPS ба SSH

```text
https://github.com/ner/tusul.git      # нууц үг/token асууна
git@github.com:ner/tusul.git          # SSH түлхүүр ашиглана
```

SSH нь тохируулсны дараа илүү тохиромжтой — дахин дахин
баталгаажуулахгүй.

Шилжих:

```bash
git remote set-url origin git@github.com:ner/tusul.git
```

### Алсын салаанууд

`main` бол таны төслийн үндсэн түүх — Git үүнийг **салаа** (branch) гэж
нэрлэдэг. Салааг Модул 6-д нарийн үзнэ; одоохондоо алсын агуулахынх нь
хуулбарыг харахад хангалттай:

```bash
git branch -r          # алсын (remote) салаанууд: origin/main
git branch -a          # локал ба алсын бүгд
```

`origin/main` гэдэг нь «`origin` дээрх `main` салаа сүүлд харахад
ийм байсан» гэсэн утгатай.
""",
            initial_code="""\
# --- Татаж авах ---
git clone https://github.com/hereglegch/tusul.git
cd tusul

# Өөр нэрээр
git clone https://github.com/hereglegch/tusul.git miniy-hevleh

# Гүехэн — зөвхөн сүүлийн commit, том төсөлд хурдан
git clone --depth 1 https://github.com/tom/tusul.git

# --- Алсыг удирдах ---
git remote -v
git remote show origin

# Нэмэх
git remote add origin https://github.com/hereglegch/tusul.git

# HTTPS-ээс SSH рүү шилжих
git remote set-url origin git@github.com:hereglegch/tusul.git

# Хасах
git remote remove hoyordogch

# --- Fork дээр ажиллахад хоёр алс (fork-ийг Модул 8-д үзнэ) ---
git remote add upstream https://github.com/ehiin/tusul.git
git remote -v
# origin    миний fork    (push энд)
# upstream  эх төсөл      (pull эндээс)

# --- Алсын салаанууд (салааг Модул 6-д нарийн үзнэ) ---
git branch -r        # алсын салаанууд: origin/main
git branch -a        # локал ба алсын бүгд
""",
        ),
        LessonSpec(
            title="git push",
            slug="git-push",
            description="Локал commit-уудыг дээш илгээх.",
            duration=400,
            language=SH,
            content="""\
```bash
git push
```

Локал commit-уудыг алсын агуулах руу илгээнэ.

### Эхний удаа

Шинэ салаа push хийхэд Git аль алсын салаатай холбохоо мэдэхгүй:

```bash
git push -u origin bolomj/nevtreh
```

`-u` (upstream) нь холбоог тогтооно. Дараа нь зүгээр `git push`
хангалттай.

### Push татгалзвал

```text
! [rejected]  main -> main (fetch first)
```

Энэ нь **алсад таны мэдэхгүй commit байна** гэсэн утгатай. Хэн нэгэн
таны өмнө push хийжээ.

Шийдэл:

```bash
git pull
# зөрчил байвал шийднэ
git push
```

> Энэ үед `--force` **бүү ашигла**. Тэр нь бусдын ажлыг устгана.

### `--force` ба `--force-with-lease`

```bash
git push --force               # АЮУЛТАЙ
git push --force-with-lease    # илүү аюулгүй
```

`--force-with-lease` нь таны сүүлд харснаас хойш алсад өөрчлөлт орсон
бол **татгалзана**. Түүхийг өөрчилсний дараа (rebase, amend) push
хийхэд үүнийг ашигла.

Хамтарсан салаан дээр түүхийг **хэзээ ч** бүү өөрчил.

### Салаа устгах

```bash
git push origin --delete bolomj/nevtreh
```

### Тэмдэг илгээх

```bash
git push --tags
```

Тэмдэг нь автоматаар push хийгддэггүй (Модул 13).

### Push хийхийн өмнө

```bash
git status                     # орхигдсон файл байна уу
git log origin/main..HEAD      # юу илгээгдэх вэ
```

Хоёр дахь тушаал нь «локалд байгаа ч алсад байхгүй» commit-уудыг
харуулна.

### Хэзээ push хийх вэ

Өдөрт дор хаяж нэг удаа. Commit нь зөвхөн таны компьютер дээр байвал
дискний эвдрэл бүх ажлыг тань авч одно.
""",
            initial_code="""\
# --- Ердийн push ---
git push

# --- Шинэ салааны эхний push ---
git push -u origin bolomj/nevtreh

# -u нь холбоог тогтооно. Дараа нь зүгээр «git push» хангалттай.

# --- Push татгалзвал ---
# ! [rejected]  main -> main (fetch first)
# Энэ нь алсад таны мэдэхгүй commit байна гэсэн утга.

git pull                # татаж нэгтгэнэ
# зөрчил байвал шийднэ
git push

# --force БҮҮ ашигла — бусдын ажлыг устгана

# --- Түүх өөрчилсний дараа (зөвхөн ӨӨРИЙН салаан дээр) ---
git push --force-with-lease

# --- Илгээхийн өмнө шалгах ---
git status
git log origin/main..HEAD --oneline     # юу илгээгдэх вэ

# --- Салаа устгах ---
git push origin --delete bolomj/hoochin

# --- Тэмдэг илгээх (автоматаар явдаггүй) ---
git push --tags
""",
        ),
        LessonSpec(
            title="git pull ба git fetch",
            slug="git-pull-ba-fetch",
            description="Алсын өөрчлөлтийг татах хоёр арга.",
            duration=420,
            language=SH,
            content="""\
### Хоёрын ялгаа

| Тушаал | Юу хийдэг |
|---|---|
| `git fetch` | Татна, гэхдээ **нэгтгэхгүй** |
| `git pull` | Татна **ба** нэгтгэнэ |

```text
git pull = git fetch + git merge
```

`git merge` нь татаж авсан өөрчлөлтийг өөрийн ажилтай **нэгтгэнэ**.
Нэгтгэлтийг Модул 7-д нарийн үзнэ.

### `git fetch` — аюулгүй

```bash
git fetch
git log HEAD..origin/main --oneline    # юу ирснийг хар
git diff HEAD origin/main              # ялгааг хар
```

Таны ажлыг **огт хөндөхгүй**. Юу ирснийг эхлээд харах боломж өгнө.

> Эргэлзвэл `fetch` хий. `pull` нь нэгтгэлт эхлүүлдэг тул гэнэтийн
> зөрчил үүсгэж болно.

### `git pull` — хурдан

```bash
git pull
```

Ихэнх үед энэ нь хэрэгтэй зүйл. Ажил эхлэхийн өмнө үргэлж хий.

### Merge уу, rebase уу

```bash
git pull                    # merge (анхдагч)
git pull --rebase           # rebase
```

| | `merge` | `rebase` |
|---|---|---|
| Түүх | Нэгтгэх commit нэмнэ | Шулуун байна |
| Аюулгүй байдал | Илүү аюулгүй | Түүхийг өөрчилнө |
| Хэзээ | Анхдагч | Цэвэр түүх хүсвэл |

Хоёулаа таны commit-уудыг татсан өөрчлөлттэй нийлүүлнэ — ялгаа нь түүх
ямар харагдахад л. Эхлэгч бол анхдагч `merge`-ийг орхи.

Анхдагчийг тохируулах:

```bash
git config --global pull.rebase false    # merge
git config --global pull.rebase true     # rebase
```

Багийнхаа журмыг дага.

### Цэвэрлэх

Алсад устсан салаа локал дээр үлддэг:

```bash
git fetch --prune
```

Устсан алсын салаануудыг цэвэрлэнэ.

### Pull амжилтгүй болвол

```text
error: Your local changes would be overwritten by merge
```

Commit хийгээгүй өөрчлөлт зөрчилдөж байна. Гурван сонголт:

```bash
git stash          # өөрчлөлтийг түр нууж хадгална (Модул 11)
git pull
git stash pop      # нуусан өөрчлөлтөө буцааж авна

# эсвэл commit хий
git commit -am "Ажил хийгдэж байна"
git pull
```

### Ажил эхлэхийн өмнө

```bash
git pull
```

Энэ нэг тушаал нь нэгтгэлтийн зөрчлийн ихэнхийг **урьдчилан сэргийлнэ**.
Хуучирсан код дээр ажиллах нь дараа нь зөрчил үүсгэдэг.
""",
            initial_code="""\
# --- fetch: татна, гэхдээ НЭГТГЭХГҮЙ ---
git fetch

# Юу ирснийг эхлээд хар
git log HEAD..origin/main --oneline
git diff HEAD origin/main

# Тохирч байвал нэгтгэ — merge нь татсан өөрчлөлтийг өөрийн ажилтай
# нийлүүлнэ (Модул 7-д нарийн үзнэ)
git merge origin/main

# --- pull: татна БА нэгтгэнэ ---
git pull

# pull = fetch + merge

# --- rebase хувилбар ---
git pull --rebase

# Анхдагчийг тохируулах
git config --global pull.rebase false

# --- Устсан алсын салааг цэвэрлэх ---
git fetch --prune

# --- Commit хийгээгүй өөрчлөлттэй үед pull ---
# error: Your local changes would be overwritten by merge

# stash — commit хийгээгүй өөрчлөлтийг түр нууж хадгална (Модул 11-д үзнэ)
git stash            # түр хадгална
git pull
git stash pop        # буцааж авна

# эсвэл
git commit -am "Ажил хийгдэж байна"
git pull

# --- Ажил эхлэхийн өмнө ҮРГЭЛЖ ---
git pull
""",
        ),
    ],
)

GIT_BASIC_MODULES = [BASICS, WORKFLOW, GITHUB_BASICS, REMOTES]
