"""Модул 10-14 — Буцаах, stash, түүх, тэмдэг, төслийн удирдлага.

Алдаа гаргасан үед юу хийх вэ гэсэн асуултад хариулна. Git-д бараг бүх
зүйлийг буцаах боломжтой — аль тушаалыг хэзээ ашиглахаа мэдэх нь чухал.
"""

from app.content.types import LessonSpec, ModuleSpec
from app.models.enums import LessonLanguage

SH = LessonLanguage.SHELL

UNDOING = ModuleSpec(
    title="Модул 10 — Өөрчлөлтийг буцаах",
    description="restore, revert, reset болон аль нь хэзээ.",
    lessons=[
        LessonSpec(
            title="git restore",
            slug="git-restore",
            description="Commit хийгээгүй өөрчлөлтийг буцаах.",
            duration=400,
            language=SH,
            content="""\
`git restore` нь **commit хийгээгүй** өөрчлөлтийг л буцаана.

### Ажлын хавтсын өөрчлөлтийг устгах

```bash
git restore main.c          # нэг файл
git restore .               # бүгд
```

> Энэ нь өөрчлөлтийг **бүрмөсөн устгана**. Commit хийгээгүй ажил
> **буцаж ирэхгүй**. Эргэлзвэл `git stash` ашигла — түр хадгална
> (Модул 11-д үзнэ).

### Бэлтгэснийг буцаах

```bash
git restore --staged main.c
```

`git add` хийснийг буцаана. **Өөрчлөлт нь үлдэнэ** — зөвхөн бэлтгэх
талбараас гарна.

### Хоёрыг нэг дор

```bash
git restore --staged --worktree main.c
```

Бэлтгэснийг ч, өөрчлөлтийг ч бүгдийг буцаана.

### Тодорхой commit-оос сэргээх

```bash
git restore --source HEAD~3 main.c
git restore --source a1b2c3d main.c
```

Файлыг тэр үеийн байдал руу буцаана. Бусад файлд хүрэхгүй.

### Хуучин тушаалууд

| Хуучин | Шинэ |
|---|---|
| `git checkout -- file` | `git restore file` |
| `git reset HEAD file` | `git restore --staged file` |

`git checkout` нь салаа солих, файл сэргээх, commit руу үсрэх гурван
өөр ажил хийдэг тул эхлэгчид төөрөгддөг байв. Git 2.23-аас хойш
`switch` ба `restore` гэж **хуваасан**.

Шинэ кодод хуваасан хувилбарыг сонго.

### Устгасан файлыг сэргээх

```bash
git restore ustgasan.c
```

Commit хийсэн файлыг санамсаргүй устгасан бол ингэж сэргээнэ.

### Аль нь хэзээ

```text
Commit хийгээгүй    ->  git restore
Commit хийсэн       ->  git revert (нийтэд) эсвэл git reset (локал)
```

Энэ ялгааг сайн санаарай — дараагийн хоёр хичээл тэр тухай.
""",
            initial_code="""\
# --- Ажлын хавтсын өөрчлөлтийг УСТГАХ ---
git restore main.c              # нэг файл
git restore .                   # бүгд

# АНХААР: commit хийгээгүй ажил буцаж ирэхгүй.
# Эргэлзвэл эхлээд: git stash — түр хадгална (Модул 11)

# --- Бэлтгэснийг буцаах (өөрчлөлт ҮЛДЭНЭ) ---
git restore --staged main.c
git status

# --- Хоёуланг нь ---
git restore --staged --worktree main.c

# --- Тодорхой commit-оос сэргээх ---
git restore --source HEAD~3 main.c
git restore --source a1b2c3d src/tohirgoo.c

# --- Устгасан файлыг сэргээх ---
rm main.c
git restore main.c

# --- Хуучин тушаалуудтай харьцуулах ---
# git checkout -- main.c     ->  git restore main.c
# git reset HEAD main.c      ->  git restore --staged main.c

# --- Юу өөрчлөгдөхийг УРЬДЧИЛАН харах ---
git diff                        # ажлын хавтас
git diff --staged               # бэлтгэх талбар
""",
        ),
        LessonSpec(
            title="git revert",
            slug="git-revert",
            description="Commit-ийг аюулгүйгээр буцаах.",
            duration=420,
            language=SH,
            content="""\
`git revert` нь commit-ийн өөрчлөлтийг **эсрэгээр** хийсэн **шинэ
commit** үүсгэнэ.

```bash
git revert a1b2c3d
```

```text
Өмнө:  A ─── B ─── C
Дараа: A ─── B ─── C ─── C'
```

`C'` нь `C`-ийн үйлдлийг буцаана. `C` нь **түүхэнд үлдэнэ**.

### Яагаад энэ нь аюулгүй вэ

Түүхийг **өөрчлөхгүй** — зөвхөн нэмнэ. Тиймээс:

- Push хийсэн commit дээр ашиглаж болно
- Багийнхны ажил эвдрэхгүй
- Юу болсон нь түүхэнд харагдана

> **Дүрэм: нийтэд push хийсэн зүйлийг буцаахдаа `revert` ашигла.**
> `reset` нь түүхийг өөрчилдөг тул бусдын агуулахтай зөрчилдөнө.

### Хэд хэдэн commit

```bash
git revert a1b2c3d 9f8e7d6            # хоёрыг
git revert HEAD~3..HEAD               # мужаар
```

### Нэгтгэх commit-ыг буцаах

```bash
git revert -m 1 a1b2c3d
```

Нэгтгэх commit нь хоёр эцэгтэй тул аль нь «үндсэн» болохыг заана.
`-m 1` нь ихэвчлэн зөв — нэгтгэлт хийсэн салаа.

### Commit үүсгэхгүй

```bash
git revert --no-commit a1b2c3d
```

Өөрчлөлтийг бэлтгэх талбарт тавиад зогсоно. Хэд хэдэн revert-ыг нэг
commit болгоход тохиромжтой.

### Зөрчил гарвал

Тэр кодыг хожим өөрчилсөн бол зөрчил үүснэ:

```bash
git revert a1b2c3d
# зөрчлийг зас
git add .
git revert --continue

# эсвэл цуцлах
git revert --abort
```

### Revert-ийг revert хийж болно

```bash
git revert <revert-ийн commit>
```

Санамсаргүй буцаасан бол буцаалтыг нь буцаана. Түүх нь бага зэрэг
төвөгтэй харагдах ч бүх зүйл хадгалагдана.

### Дадлага

Production дээр алдаа гарвал:

1. `git revert` — тэр дор нь буцаана
2. Тайван засвар хий
3. Дахин нэгтгэ

Алдааг «хурдан засах» гэж яарснаас **эхлээд буцаах** нь үргэлж
аюулгүй.
""",
            initial_code="""\
# --- Нэг commit буцаах ---
git revert a1b2c3d

# Шинэ commit үүснэ. Хуучин commit түүхэнд ҮЛДЭНЭ.
git log --oneline -3

# --- Сүүлийн commit-ыг ---
git revert HEAD

# --- Хэд хэдэн ---
git revert a1b2c3d 9f8e7d6
git revert HEAD~3..HEAD

# --- Нэгтгэх commit ---
git revert -m 1 a1b2c3d
# -m 1 нь аль эцгийг «үндсэн» гэж үзэхийг заана

# --- Commit үүсгэхгүй, зөвхөн бэлтгэх ---
git revert --no-commit a1b2c3d
git revert --no-commit 9f8e7d6
git commit -m "Хоёр өөрчлөлтийг буцаав"

# --- Зөрчил гарвал ---
git revert a1b2c3d
# зөрчлийг зас
git add .
git revert --continue
# эсвэл
git revert --abort

# --- Production дээр алдаа гарвал ---
git revert <алдаатай commit>
git push                       # тэр дор нь буцаана
# Дараа нь тайван засвар хийнэ
""",
        ),
        LessonSpec(
            title="git reset",
            slug="git-reset",
            description="Түүхийг өөрчлөх — болгоомжтой.",
            duration=450,
            language=SH,
            content="""\
`git reset` нь салааны заагчийг **өмнөх commit руу зөөнө**. Түүхийг
өөрчилдөг тул болгоомжтой ашиглана.

### Гурван горим

```bash
git reset --soft HEAD~1
git reset --mixed HEAD~1     # анхдагч
git reset --hard HEAD~1
```

| Горим | Commit | Бэлтгэх талбар | Ажлын хавтас |
|---|---|---|---|
| `--soft` | Буцаана | **Хэвээр** | **Хэвээр** |
| `--mixed` | Буцаана | Цэвэрлэнэ | **Хэвээр** |
| `--hard` | Буцаана | Цэвэрлэнэ | **УСТГАНА** |

### `--soft` — хамгийн аюулгүй

```bash
git reset --soft HEAD~1
```

Commit-ыг задлана, өөрчлөлт нь бэлтгэгдсэн хэвээр үлдэнэ. Commit
мессежийг засах, хэд хэдэн commit нэгтгэхэд тохиромжтой.

### `--mixed` — анхдагч

```bash
git reset HEAD~1
```

Commit болон бэлтгэлийг задлана. Өөрчлөлт файлд үлдэнэ. Дахин
бэлтгэж, өөр байдлаар commit хийж болно.

### `--hard` — АЮУЛТАЙ

```bash
git reset --hard HEAD~1
```

> Бүх зүйлийг **устгана**. Commit хийгээгүй ажил бүрмөсөн алга болно.
> Ажиллуулахын өмнө `git status` хийж, юу алдахаа мэдэж бай.

### `revert` уу, `reset` үү

| Нөхцөл | Тушаал |
|---|---|
| Push хийсэн | `git revert` — **заавал** |
| Зөвхөн локал | `git reset` — болно |
| Commit хийгээгүй | `git restore` |

> Push хийсэн commit дээр `reset` ашиглавал таны түүх багийнхнаас
> зөрнө. Дараагийн push татгалзана, force push хийвэл бусдын ажлыг
> устгана.

### Түгээмэл хэрэглээ

**Сүүлийн commit-ыг задлах:**

```bash
git reset --soft HEAD~1
```

**Гурван commit-ыг нэг болгох:**

```bash
git reset --soft HEAD~3
git commit -m "Нэвтрэх маягтыг бүрэн хийв"
```

**Санамсаргүй `git add`-ыг буцаах:**

```bash
git reset                     # эсвэл git restore --staged .
```

### Алдсан бол `reflog`

```bash
git reflog
# a1b2c3d HEAD@{0}: reset: moving to HEAD~1
# 9f8e7d6 HEAD@{1}: commit: Чухал ажил

git reset --hard 9f8e7d6
```

`reflog` нь `HEAD` хаана явснаа **бүгдийг** бүртгэдэг. `--hard`-аар
алдсан commit-ыг ч ихэвчлэн сэргээж болно — хэдэн долоо хоногийн
дотор.

Энэ бол Git-ийн аврах олс. Сандрахаасаа өмнө `git reflog` ажиллуул.
""",
            initial_code="""\
# --- Гурван горим ---
git reset --soft HEAD~1        # commit задална, бэлтгэл ҮЛДЭНЭ
git reset --mixed HEAD~1       # commit ба бэлтгэл задална (анхдагч)
git reset --hard HEAD~1        # БҮГДИЙГ устгана

# --- Сүүлийн commit-ийн мессежийг засах ---
git reset --soft HEAD~1
git commit -m "Зассан мессеж"
# эсвэл богино:
git commit --amend -m "Зассан мессеж"

# --- Гурван commit-ыг нэг болгох ---
git reset --soft HEAD~3
git commit -m "Нэвтрэх маягтыг бүрэн хийв"

# --- Санамсаргүй add-ыг буцаах ---
git reset
git restore --staged .         # ижил үр дүн

# --- --hard хийхийн ӨМНӨ ---
git status                     # юу алдахаа мэд
git stash                      # эсвэл түр хадгал (Модул 11)

# --- Алдсан бол reflog ---
git reflog
git reset --hard 9f8e7d6       # сэргээнэ

# --- Push хийсэн бол reset БИШ revert ---
git revert a1b2c3d
""",
        ),
    ],
)

STASHING = ModuleSpec(
    title="Модул 11 — Stash",
    description="Дуусаагүй ажлыг түр хадгалах.",
    lessons=[
        LessonSpec(
            title="git stash",
            slug="git-stash",
            description="Ажлаа тавиад өөр зүйл рүү шилжих.",
            duration=420,
            language=SH,
            content="""\
### Асуудал

Ажил дунд байхад яаралтай засвар хийх шаардлага гарлаа. Одоогийн ажил
дуусаагүй тул commit хийхийг хүсэхгүй байна.

```bash
git switch main
# error: Your local changes would be overwritten
```

### Шийдэл

```bash
git stash
```

Commit хийгээгүй бүх өөрчлөлтийг **тавиур** дээр хадгалж, ажлын хавтсыг
цэвэрлэнэ.

```bash
git stash                     # хадгална
git switch main               # чөлөөтэй шилжинэ
# яаралтай засварыг хийнэ
git switch bolomj/ajil
git stash pop                 # буцааж авна
```

### `pop` ба `apply`

| Тушаал | Тавиураас устгах уу |
|---|---|
| `git stash pop` | Тийм |
| `git stash apply` | Үгүй — үлдэнэ |

Хэд хэдэн салаанд ижил өөрчлөлт хэрэглэх бол `apply`.

### Тайлбар бич

```bash
git stash push -m "Нэвтрэх маягт хийгдэж байна"
```

Тайлбаргүй stash нь хэдхэн хоногийн дараа танигдахаа болино.

### Жагсаах ба харах

```bash
git stash list
# stash@{0}: On bolomj: Нэвтрэх маягт хийгдэж байна
# stash@{1}: WIP on main: a1b2c3d Өмнөх ажил

git stash show stash@{0}         # хураангуй
git stash show -p stash@{0}      # бүтэн ялгаа
```

### Тодорхой нэгийг

```bash
git stash pop stash@{1}
git stash drop stash@{0}         # устгана
git stash clear                  # БҮГДИЙГ устгана
```

### Хянагдаагүй файл

```bash
git stash                        # untracked файлыг АВАХГҮЙ
git stash -u                     # untracked-ыг ч авна
git stash -a                     # ignored-ыг ч авна
```

`-u` мартвал шинэ файлууд ажлын хавтсанд үлдэнэ. Энэ нь ихэвчлэн
төөрөгдөл үүсгэдэг.

### Stash-аас салаа гаргах

```bash
git stash branch bolomj/shine stash@{0}
```

Шинэ салаа үүсгээд stash-ыг тэнд хэрэглэнэ. Ажил нь урт болж
хувирвал тохиромжтой.

### Болгоомжлох зүйл

> Stash нь **түр зуурынх**. Хэдэн долоо хоног хадгалах бол салаа
> гаргаж commit хий. Stash нь салаанд харьяалагдахгүй тул мартагдвал
> олоход хэцүү.

`git stash clear` нь **буцаах боломжгүй**. Ашиглахын өмнө `list`-ээр
шалга.
""",
            initial_code="""\
# --- Ажлаа түр хадгалах ---
git stash
git stash push -m "Нэвтрэх маягт хийгдэж байна"

# --- Чөлөөтэй шилжих ---
git switch main
git pull
# яаралтай засварыг хийнэ
git commit -am "Яаралтай засвар"
git push

# --- Ажлаа буцааж авах ---
git switch bolomj/nevtreh-maygt
git stash pop

# --- Жагсаах ба харах ---
git stash list
git stash show stash@{0}
git stash show -p stash@{0}       # бүтэн ялгаа

# --- pop ба apply ---
git stash pop                     # авч, тавиураас УСТГАНА
git stash apply                   # авч, тавиурт ҮЛДЭЭНЭ

# --- Хянагдаагүй файлыг ч авах ---
git stash -u                      # untracked
git stash -a                      # ignored-ыг ч

# --- Тодорхой нэгийг ---
git stash pop stash@{1}
git stash drop stash@{0}

# --- Stash-аас салаа гаргах ---
git stash branch bolomj/shine stash@{0}

# --- БҮГДИЙГ устгах (буцаах боломжгүй) ---
git stash list                    # эхлээд шалга
git stash clear
""",
        ),
    ],
)

HISTORY = ModuleSpec(
    title="Модул 12 — Git-ийн түүх",
    description="Өнгөрсөнд юу болсныг олох.",
    lessons=[
        LessonSpec(
            title="Түүхийг харах",
            slug="tuuh-harah",
            description="log, show болон шүүлтүүрүүд.",
            duration=420,
            language=SH,
            content="""\
### Хэрэгтэй `log` хувилбарууд

```bash
git log --oneline                     # нэг мөр
git log --oneline --graph --all       # салаатай зураг
git log --stat                        # өөрчлөгдсөн файлууд
git log -p                            # бүрэн ялгаатай
git log -5                            # сүүлийн 5
```

### Шүүх

```bash
git log --author="Бат"
git log --since="2026-09-01"
git log --until="1 week ago"
git log --grep="нэвтрэх"              # мессежээр хайна
git log -S"parseUser"                 # КОД дотроос хайна
```

`-S` нь онцгой хүчтэй: тэр текстийг **нэмсэн эсвэл хассан** commit-ыг
олно. «Энэ функц хэзээ алга болсон бэ» гэсэн асуултад хариулна.

### Файлын түүх

```bash
git log --oneline -- src/main.c
git log --follow -- src/main.c        # нэр солигдсоныг ч дагана
```

`--follow` нь файл нэр солигдсон ч түүхийг үргэлжлүүлнэ.

### `git show`

```bash
git show a1b2c3d                      # commit-ийн бүх мэдээлэл
git show HEAD                         # сүүлийнх
git show HEAD~2                       # хоёр өмнөх
git show a1b2c3d:src/main.c           # тэр үеийн файлын АГУУЛГА
```

Сүүлийнх нь маш хэрэгтэй — сэргээхгүйгээр хуучин хувилбарыг харна.

### `git blame`

```bash
git blame src/main.c
git blame -L 40,60 src/main.c         # зөвхөн 40-60 мөр
```

Мөр бүрийг хэн, хэзээ, аль commit дээр бичсэнийг харуулна.

> Нэр нь сөрөг сонсогдох ч зорилго нь **буруутгах биш**. Тэр мөрийг
> яагаад ингэж бичсэнийг олж, тухайн commit-ийн мессежээс шалтгааныг
> уншина.

### Хугацааны цэгүүд

| Бичлэг | Утга |
|---|---|
| `HEAD` | Одоогийн commit |
| `HEAD~1` | Нэг өмнөх |
| `HEAD~3` | Гурван өмнөх |
| `main@{yesterday}` | Өчигдрийн main |

### Хоёр цэгийн ялгаа

```bash
git diff main..bolomj                 # хоёрын ялгаа
git log main..bolomj                  # bolomj дээр байгаа, main дээр байхгүй
git log origin/main..HEAD             # push хийгээгүй commit-ууд
```

Сүүлийнх нь push хийхийн өмнө шалгахад хэрэгтэй.

### Статистик

```bash
git shortlog -sn                      # хэн хэдэн commit хийсэн
git log --oneline | wc -l             # нийт commit
```
""",
            initial_code="""\
# --- Үндсэн хувилбарууд ---
git log --oneline
git log --oneline --graph --all --decorate
git log --stat                        # өөрчлөгдсөн файлууд
git log -p -3                         # сүүлийн 3-ын бүтэн ялгаа

# --- Шүүх ---
git log --author="Бат"
git log --since="2026-09-01" --until="2026-09-13"
git log --grep="нэвтрэх"              # мессежээр
git log -S"parseUser"                 # КОД дотроос — хэзээ нэмэгдэж/хасагдсаныг олно

# --- Файлын түүх ---
git log --oneline -- src/main.c
git log --follow -- src/main.c        # нэр солигдсоныг ч дагана

# --- Нэг commit ---
git show HEAD
git show a1b2c3d
git show a1b2c3d --stat
git show a1b2c3d:src/main.c           # тэр үеийн файлын агуулга

# --- Мөр бүрийг хэн бичсэн ---
git blame src/main.c
git blame -L 40,60 src/main.c

# --- Хоёр цэгийн ялгаа ---
git diff main..bolomj
git log main..bolomj --oneline
git log origin/main..HEAD --oneline   # push хийгээгүй commit-ууд

# --- Статистик ---
git shortlog -sn
""",
        ),
        LessonSpec(
            title="Өмнөх commit-ыг олох",
            slug="umnuh-commit-oloh",
            description="Алдаа хэзээ орсныг олох, хуучин хувилбар руу очих.",
            duration=420,
            language=SH,
            content="""\
### Хуучин commit руу очих

```bash
git switch --detach a1b2c3d
```

Тэр үеийн бүх файлыг харна. Энэ нь *detached HEAD* төлөв — салаан дээр
биш, тодорхой commit дээр зогсож байна.

```bash
git switch -                          # буцах
```

> Detached төлөвт commit хийвэл тэр commit **аль ч салаанд
> харьяалагдахгүй**. Хадгалах бол салаа гарга:
> `git switch -c shine-salaa`

### `git bisect` — алдааг хоёртын хайлтаар олох

«Энэ алдаа хэзээ орсон бэ?» Хэдэн зуун commit байвал гараар шалгах
боломжгүй. `bisect` нь хоёртын хайлт хийнэ.

```bash
git bisect start
git bisect bad                        # одоо алдаатай
git bisect good v1.0                  # энэ хувилбарт зөв байсан
```

Git дунд нь байгаа commit руу аваачна. Шалгаад хэлнэ:

```bash
git bisect good                       # эсвэл
git bisect bad
```

Дуусахад:

```bash
git bisect reset
```

1000 commit-оос **10 алхамд** олно. Гараар бол 1000 удаа шалгах байсан.

### Автоматжуулах

```bash
git bisect start HEAD v1.0
git bisect run npm test
```

Git тестийг өөрөө ажиллуулж, алдааны эх үүсвэрийг **өөрөө** олно. Энэ
бол Git-ийн хамгийн дутуу үнэлэгдсэн боломжуудын нэг.

### Устсан commit олох

```bash
git reflog
```

`HEAD` хаана явснаа бүгдийг бүртгэнэ — reset, checkout, merge бүгд.
Алдсан ажлыг олох хамгийн найдвартай арга.

```bash
git reflog
# 9f8e7d6 HEAD@{5}: commit: Чухал ажил

git switch -c sergeesen 9f8e7d6
```

### Устсан салаа

```bash
git reflog | grep "checkout: moving from bolomj"
git switch -c bolomj-sergeesen a1b2c3d
```

### Файлын хуучин хувилбар

```bash
git show HEAD~5:src/main.c > huuchin.c
git restore --source HEAD~5 src/main.c
```

Эхнийх нь тусад нь файл болгоно, хоёр дахь нь оронд нь тавина.

### Хэзээ устдаг вэ

Аль ч салаанд харьяалагдахгүй commit нь **ойролцоогоор 30 хоногийн
дараа** цэвэрлэгдэнэ. Тэр хүртэл `reflog`-оор олж болно.

Тиймээс алдсан ажлаа **тэр дор нь** хай.
""",
            initial_code="""\
# --- Хуучин commit руу очих ---
git switch --detach a1b2c3d
# ... шалгана ...
git switch -                          # буцах

# Detached төлөвт хийсэн ажлыг хадгалах бол:
git switch -c shine-salaa

# --- Алдаа хэзээ орсныг олох ---
git bisect start
git bisect bad                        # одоо алдаатай
git bisect good v1.0                  # энд зөв байсан

# Git дунд руу аваачна. Шалгаад хэл:
git bisect good
git bisect bad

# Дуусахад
git bisect reset

# --- Автоматаар ---
git bisect start HEAD v1.0
git bisect run npm test
# Git тестийг өөрөө ажиллуулж эх үүсвэрийг олно

# --- Алдсан ажлыг олох ---
git reflog
git switch -c sergeesen 9f8e7d6

# --- Устсан салааг сэргээх ---
git reflog | grep "checkout: moving from bolomj"
git switch -c bolomj-sergeesen a1b2c3d

# --- Файлын хуучин хувилбар ---
git show HEAD~5:src/main.c > huuchin.c
git restore --source HEAD~5 src/main.c
""",
        ),
    ],
)

TAGS = ModuleSpec(
    title="Модул 13 — Тэмдэг ба хувилбар",
    description="Хувилбар тэмдэглэх, release гаргах.",
    lessons=[
        LessonSpec(
            title="git tag",
            slug="git-tag",
            description="Тодорхой commit-ыг нэрлэх.",
            duration=400,
            language=SH,
            content="""\
**Тэмдэг** нь тодорхой commit-д өгсөн байнгын нэр. Ихэвчлэн хувилбар
тэмдэглэхэд ашиглана.

```bash
git tag v1.0.0
```

### Хоёр төрөл

```bash
git tag v1.0.0                              # хөнгөн
git tag -a v1.0.0 -m "Анхны хувилбар"       # тайлбартай
```

| | Хөнгөн | Тайлбартай |
|---|---|---|
| Агуулах | Зөвхөн заагч | Зохиогч, огноо, мессеж |
| Хэзээ | Түр зуурын тэмдэглэгээ | **Нийтэлсэн хувилбар** |

> Нийтлэх хувилбарт **үргэлж** `-a` ашигла. Хэн, хэзээ гаргасан нь
> тэмдэглэгдэнэ.

### Хуучин commit-д тэмдэг

```bash
git tag -a v0.9.0 a1b2c3d -m "Бета хувилбар"
```

### Жагсаах ба харах

```bash
git tag                                # бүгд
git tag -l "v1.*"                      # шүүх
git show v1.0.0                        # дэлгэрэнгүй
```

### Push хийх — мартагддаг алхам

```bash
git push origin v1.0.0                 # нэгийг
git push --tags                        # бүгдийг
```

> Тэмдэг нь `git push`-аар **автоматаар явдаггүй**. Тусад нь илгээнэ.
> Энэ бол хамгийн олон мартагддаг алхмуудын нэг.

### Устгах

```bash
git tag -d v1.0.0                      # локал
git push origin --delete v1.0.0        # алсын
```

### Семантик хувилбарлалт

```text
v2.4.1
 │ │ │
 │ │ └── Patch  — алдааны засвар
 │ └──── Minor  — шинэ боломж, хуучинтай нийцнэ
 └────── Major  — нийцгүй өөрчлөлт
```

| Өөрчлөлт | Аль тоог нэмэх |
|---|---|
| Алдаа зассан | Patch: `2.4.1` → `2.4.2` |
| Шинэ боломж нэмсэн | Minor: `2.4.1` → `2.5.0` |
| Хуучин API эвдсэн | Major: `2.4.1` → `3.0.0` |

`1.0.0`-аас өмнөх хувилбар нь тогтворгүй гэсэн утгатай — хэзээ ч
эвдэрч болно.

### Тэмдгээс салаа

```bash
git switch -c zasvar/v1.0.1 v1.0.0
```

Гаргасан хувилбарт яаралтай засвар хийхэд тэр цэгээс эхэлнэ.

### Хэзээ тэмдэглэх вэ

Нийтэд гаргах бүрд. Ингэснээр:

- Хэрэглэгч аль хувилбарыг ашиглаж байгаагаа мэднэ
- Алдаа мэдээлэхэд хувилбар нь тодорхой
- Тэр цэг рүү үргэлж буцаж болно
""",
            initial_code="""\
# --- Тэмдэг үүсгэх ---
git tag v1.0.0                              # хөнгөн
git tag -a v1.0.0 -m "Анхны тогтвортой хувилбар"   # тайлбартай

# Нийтлэх хувилбарт ҮРГЭЛЖ -a ашигла

# --- Хуучин commit-д ---
git tag -a v0.9.0 a1b2c3d -m "Бета хувилбар"

# --- Жагсаах ба харах ---
git tag
git tag -l "v1.*"
git show v1.0.0

# --- Push хийх (АВТОМАТААР ЯВДАГГҮЙ) ---
git push origin v1.0.0
git push --tags

# --- Устгах ---
git tag -d v1.0.0
git push origin --delete v1.0.0

# --- Хувилбар хоорондын өөрчлөлт ---
git log v1.0.0..v1.1.0 --oneline
git diff v1.0.0 v1.1.0 --stat

# --- Тэмдгээс салаа гаргах (яаралтай засварт) ---
git switch -c zasvar/v1.0.1 v1.0.0

# --- Сүүлийн тэмдгээс хойшхи commit-ууд ---
git log $(git describe --tags --abbrev=0)..HEAD --oneline
""",
        ),
        LessonSpec(
            title="GitHub Release",
            slug="github-release",
            description="Хувилбарыг нийтэд гаргах.",
            duration=400,
            language=SH,
            content="""\
**Release** нь GitHub дээрх тэмдгийн дээр нэмэгдсэн давхарга: тайлбар,
татах файл, өөрчлөлтийн жагсаалт.

### Тэмдэг ба release

| | Тэмдэг | Release |
|---|---|---|
| Хаана | Git дотор | GitHub дээр |
| Агуулах | Commit заагч | Тайлбар, файл, тэмдэглэл |

Release нь тэмдэг дээр **суурилна** — эхлээд тэмдэг хэрэгтэй.

### Үүсгэх

GitHub → Releases → Draft a new release. Эсвэл CLI-аар:

```bash
gh release create v1.0.0 --title "v1.0.0" --notes "Анхны хувилбар"
```

Өөрчлөлтийн жагсаалтыг автоматаар:

```bash
gh release create v1.0.0 --generate-notes
```

Сүүлийн release-ээс хойшхи PR-уудаас жагсаалт гаргана.

### Сайн release тэмдэглэл

```markdown
## Шинэ боломж
- Тайланг CSV болгож экспортлох (#58)
- Харанхуй горим (#61)

## Засвар
- Нэвтрэхэд хоосон нууц үг зөвшөөрч байсныг зассан (#42)

## Эвдэрсэн өөрчлөлт
- `/api/v1/users` устсан. `/api/v2/users` ашиглана уу.
```

**Эвдэрсэн өөрчлөлт** хэсгийг хэзээ ч бүү орхи. Хэрэглэгч шинэчлэхийн
өмнө юу эвдрэхийг мэдэх ёстой.

### Файл хавсаргах

```bash
gh release create v1.0.0 ./dist/programm.exe ./dist/programm-linux
```

Хөрвүүлсэн файл хавсаргавал хэрэглэгч эх кодыг хөрвүүлэхгүйгээр
ашиглана.

### Урьдчилсан хувилбар

```bash
gh release create v2.0.0-beta.1 --prerelease
```

«Тогтворгүй» гэж тэмдэглэнэ. Хэрэглэгч санамсаргүй суулгахгүй.

### Ноорог

```bash
gh release create v1.0.0 --draft
```

Бэлдээд дараа нь нийтэлнэ.

### Автоматжуулах

```yaml
on:
  push:
    tags: ['v*']

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm run build
      - uses: softprops/action-gh-release@v2
        with:
          files: dist/*
```

Тэмдэг push хийхэд release **өөрөө** үүснэ. Гараар хийх алхам
багасах тусам алдаа багасна.

### Release-ийн мөчлөг

```bash
# 1. main дээр бүх ажил нэгтгэгдсэн, тест ногоон
git switch main
git pull

# 2. Хувилбар дугаарыг файлд шинэчил
# 3. Тэмдэг
git tag -a v1.2.0 -m "v1.2.0"
git push --tags

# 4. Release үүсгэ
gh release create v1.2.0 --generate-notes
```
""",
            initial_code="""\
# --- Release-ийн бүрэн мөчлөг ---

# 1. main цэвэр, тест ногоон эсэхийг шалга
git switch main
git pull
npm test

# 2. Тэмдэг үүсгэж илгээх
git tag -a v1.2.0 -m "v1.2.0 — тайлан экспорт, харанхуй горим"
git push --tags

# 3. Release үүсгэх
gh release create v1.2.0 --generate-notes

# --- Гараар тэмдэглэл бичих ---
gh release create v1.2.0 --title "v1.2.0" --notes "$(cat << 'EOF'
## Шинэ боломж
- Тайланг CSV болгож экспортлох (#58)
- Харанхуй горим (#61)

## Засвар
- Нэвтрэхэд хоосон нууц үг зөвшөөрч байсныг зассан (#42)

## Эвдэрсэн өөрчлөлт
- /api/v1/users устсан. /api/v2/users ашиглана уу.
EOF
)"

# --- Файл хавсаргах ---
gh release create v1.2.0 ./dist/programm.exe ./dist/programm-linux

# --- Урьдчилсан хувилбар ---
gh release create v2.0.0-beta.1 --prerelease --generate-notes

# --- Ноорог ---
gh release create v1.2.0 --draft

# --- Жагсаах ба харах ---
gh release list
gh release view v1.2.0

# --- Сүүлийн release-ээс хойшхи өөрчлөлт ---
git log $(git describe --tags --abbrev=0)..HEAD --oneline
""",
        ),
    ],
)

PROJECT_MANAGEMENT = ModuleSpec(
    title="Модул 14 — GitHub төслийн удирдлага",
    description="Issue, шошго, үе шат, самбар.",
    lessons=[
        LessonSpec(
            title="Шошго, үе шат, хариуцагч",
            slug="issue-label-milestone",
            description="Ажлыг ангилж, эрэмбэлэх.",
            duration=400,
            language=SH,
            content="""\
Issue цөөхөн байхад жагсаалт хангалттай. Хэдэн арав болоход ангилал
хэрэгтэй болно.

### Шошго (label)

Гурван бүлэг шошго ашиглах нь түгээмэл:

| Бүлэг | Жишээ |
|---|---|
| Төрөл | `bug`, `enhancement`, `documentation` |
| Тэргүүлэх ач холбогдол | `p0-yaaraltai`, `p1-uden`, `p2-hojim` |
| Төлөв | `blocked`, `needs-info`, `ready` |

Өнгөөр нь бүлгийг ялгавал жагсаалт харахад ойлгомжтой.

```bash
gh label create "p0-yaaraltai" --color FF0000 --description "Тэр дор нь засах"
gh issue edit 42 --add-label "bug,p0-yaaraltai"
```

### Хэт олон шошго бүү үүсгэ

10-15 шошго хангалттай. Илүү олон болвол хэн ч зөв шошгыг олохгүй
бөгөөд ашиглахаа болино.

### Үе шат (milestone)

Холбоотой issue-г нэг зорилгын дор цуглуулна:

```bash
gh issue edit 42 --milestone "v1.2.0"
```

Ихэвчлэн хувилбартай уялдуулна. GitHub нь хэдэн хувь дууссаныг
автоматаар харуулна.

Хугацаа тавьж болно — гэхдээ хугацаа хэтэрсэн үе шат нь урам хугалдаг
тул бодитой байлга.

### Хариуцагч

```bash
gh issue edit 42 --add-assignee "bat"
```

> Нэг issue-д **нэг** хариуцагч. Хоёр хүн хариуцвал хэн ч хариуцахгүй
> болдог.

Хариуцагчгүй issue нь «хэн ч авч болно» гэсэн утгатай.

### Ажил эхлэхийн өмнө

```bash
gh issue list --assignee "@me"
gh issue edit 42 --add-assignee "@me"
```

Өөрийгөө хариуцагч болгох нь багийнхандаа «би үүн дээр ажиллаж байна»
гэж хэлэх арга. Хоёр хүн ижил ажил давхардуулахаас сэргийлнэ.

### Issue-г PR-тай холбох

```bash
gh pr create --title "Нэвтрэх алдааг зассан" --body "Closes #42"
```

Нэгтгэхэд issue автоматаар хаагдана.

### Шүүх

```bash
gh issue list --label bug --state open
gh issue list --milestone "v1.2.0"
gh issue list --assignee "@me" --state open
gh issue list --search "нэвтрэх in:title"
```

### Хаагдсан issue-г шалгах

Долоо хоног бүр нээлттэй issue-г хараарай. Хуучирсан, ач холбогдолгүй
болсныг хаах нь жагсаалтыг ашиглагдахуйц байлгана.

Хэдэн зуун нээлттэй issue бүхий төсөлд хэн ч шинийг нэмэх сонирхолгүй
болдог.
""",
            initial_code="""\
# --- Шошго үүсгэх ---
gh label create "p0-yaaraltai" --color FF0000 --description "Тэр дор нь засах"
gh label create "p1-uden" --color FFA500
gh label create "needs-info" --color CCCCCC --description "Нэмэлт мэдээлэл хэрэгтэй"

gh label list

# 10-15 шошго хангалттай. Илүү олон бол хэн ч зөвийг нь олохгүй.

# --- Issue-д шошго нэмэх ---
gh issue edit 42 --add-label "bug,p0-yaaraltai"
gh issue edit 42 --remove-label "needs-info"

# --- Үе шат ---
gh issue edit 42 --milestone "v1.2.0"

# --- Хариуцагч (нэг issue — НЭГ хариуцагч) ---
gh issue edit 42 --add-assignee "@me"

# --- Ажил эхлэхийн өмнө ---
gh issue list --assignee "@me" --state open
gh issue view 42

# --- Шүүх ---
gh issue list --label bug --state open
gh issue list --milestone "v1.2.0"
gh issue list --search "нэвтрэх in:title"

# --- PR-тай холбох ---
gh pr create --title "Нэвтрэх алдааг зассан" --body "Closes #42"

# --- Хуучирсныг хаах ---
gh issue close 17 --comment "Хуучирсан тул хаав"
""",
        ),
        LessonSpec(
            title="Төслийн самбар",
            slug="project-board",
            description="Ажлын урсгалыг нүдээр харах.",
            duration=400,
            language=SH,
            content="""\
**Project** нь issue болон PR-ыг багана болгон харуулна.

### Ердийн баганууд

```text
┌─────────┬──────────┬─────────┬─────────┐
│ Todo    │ In       │ In      │ Done    │
│         │ Progress │ Review  │         │
├─────────┼──────────┼─────────┼─────────┤
│ #58     │ #42      │ #37     │ #30     │
│ #61     │          │         │ #33     │
└─────────┴──────────┴─────────┴─────────┘
```

Issue нь баганаас баганад шилжих нь ажлын явцыг харуулна.

### Хэт олон багана бүү үүсгэ

4-5 багана хангалттай. 10 багана бүхий самбарыг хэн ч шинэчлэхгүй.

### Автоматжуулалт

GitHub Projects нь дүрэм тохируулах боломжтой:

| Үйл явдал | Үйлдэл |
|---|---|
| Issue нээгдэв | Todo руу |
| PR нээгдэв | In Review руу |
| PR нэгтгэгдэв | Done руу |
| Issue хаагдав | Done руу |

Автоматжуулбал самбар нь **өөрөө** шинэчлэгдэнэ. Гараар зөөх
шаардлагагүй — хүн мартдаг, автомат мартдаггүй.

### Харагдац

| Харагдац | Хэзээ |
|---|---|
| Board | Өдөр тутмын ажлын явц |
| Table | Олон талбараар шүүх, эрэмбэлэх |
| Roadmap | Хугацааны төлөвлөгөө |

### Өөрийн талбар

Issue-д нэмэлт мэдээлэл өгч болно:

- Хүндрэлийн оноо (1, 2, 3, 5, 8)
- Давтамж (Sprint 12)
- Баг (Backend, Frontend)

Эдгээрээр шүүж, бүлэглэж болно.

### WIP хязгаар

> Нэг хүн нэг зэрэг **нэг** ажил хийх нь хамгийн үр дүнтэй. Таван
> ажлыг зэрэг эхлүүлээд аль нь ч дуусахгүй байх нь түгээмэл алдаа.

«In Progress» баганад хэт олон карт хуримтлагдвал энэ нь дохио.

### Жижиг багт

Гурваас цөөн хүнтэй бол самбар илүүц байж болно. Issue-ийн жагсаалт
болон шошго хангалттай.

Хэрэгсэл нь ажлыг хөнгөвчлөх ёстой, нэмэлт ажил үүсгэх ёсгүй.

### CLI

```bash
gh project list --owner baigaa-ner
gh project item-list 1 --owner baigaa-ner
```

Projects-ийн CLI дэмжлэг хязгаарлагдмал тул вэб интерфэйс илүү
тохиромжтой.
""",
            initial_code="""\
# --- Project жагсаах ---
gh project list --owner baiguullaga
gh project view 1 --owner baiguullaga

# --- Доторх зүйлсийг харах ---
gh project item-list 1 --owner baiguullaga

# --- Issue нэмэх ---
gh project item-add 1 --owner baiguullaga --url https://github.com/ner/tusul/issues/42

# --- Ихэнх ажлыг вэб интерфэйсээс хийнэ ---
# Settings -> Workflows дотор автоматжуулалт тохируулна:
#   Issue нээгдэв      -> Todo
#   PR нээгдэв         -> In Review
#   PR нэгтгэгдэв      -> Done
#   Issue хаагдав      -> Done

# --- Өдөр тутмын ажлын урсгал ---
gh issue list --assignee "@me" --state open   # миний ажил
gh pr status                                   # миний PR-ууд
gh pr list --search "review-requested:@me"     # хянах хүсэлт

# --- Ажил эхлэх ---
gh issue edit 42 --add-assignee "@me"
git switch -c bolomj/42-nevtreh-maygt

# --- Ажил дуусгах ---
gh pr create --title "Нэвтрэх маягт" --body "Closes #42"
# Нэгтгэхэд issue хаагдаж, самбар дээр Done руу автоматаар шилжинэ
""",
        ),
    ],
)

GIT_INTERMEDIATE_MODULES = [UNDOING, STASHING, HISTORY, TAGS, PROJECT_MANAGEMENT]
