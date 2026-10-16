"""Модул 15-17 — Дадлагын төслүүд.

Сурсан бүх зүйлийг эхнээс нь эцэс хүртэл нэг урсгалаар давтана. Хичээл
бүр нь дарааллаар нь ажиллуулах бүрэн тушаалын жагсаалт.
"""

from app.content.types import LessonSpec, ModuleSpec
from app.models.enums import LessonLanguage

SH = LessonLanguage.SHELL

PERSONAL = ModuleSpec(
    title="Модул 15 — Хувийн төсөл",
    description="Агуулах үүсгэхээс release хүртэл.",
    lessons=[
        LessonSpec(
            title="Дадлага — Хувийн төсөл",
            slug="huviin-tusul",
            description="init, commit, push, tag, release.",
            duration=720,
            language=SH,
            content="""\
Бүх зүйлийг эхнээс нь өөрөө хийнэ. Хуулж тавихын оронд **бичиж**
үзээрэй — гарын дасгал нь санахад тусална.

### Зорилго

1. Локал агуулах үүсгэх
2. Хэд хэдэн утга учиртай commit хийх
3. GitHub дээр нийтлэх
4. Хувилбар тэмдэглэж release гаргах

### Алхам 1 — Төсөл бэлдэх

Ямар ч жижиг төсөл болно: скрипт, тэмдэглэл, дасгалын код. Гол нь
**хэдэн файлтай** байх.

### Алхам 2 — Эхний commit

`.gitignore`-ыг **эхний** commit-д оруул. Дараа нь нэмбэл хэрэггүй
файлууд аль хэдийн түүхэнд орсон байна.

### Алхам 3 — Утга учиртай commit-ууд

Бүх ажлыг нэг commit болгож бүү хий. Гурав дөрөв болгож хуваа:

```text
«Төслийн бүтэц үүсгэв»
«Дүн тооцоолох функц нэмэв»
«Хэрэглэх зааврыг README-д нэмэв»
```

### Алхам 4 — GitHub

Агуулах нэрийг локал хавтасныхаа нэртэй ижил байлга — төөрөгдөл
багасна.

### Алхам 5 — Release

```bash
git tag -a v1.0.0 -m "Анхны хувилбар"
git push --tags
gh release create v1.0.0 --generate-notes
```

### Шалгах жагсаалт

- `git log --oneline` нь ойлгомжтой түүх харуулж байна уу
- README нь суулгах, ашиглах зааврыг агуулж байна уу
- `.gitignore` нь хэрэггүй файлыг хааж байна уу
- Нууц үг, түлхүүр түүхэнд ороогүй эсэх
- GitHub дээрх release харагдаж байна уу

### Дараа нь

Энэ агуулахыг портфолио болгон ашиглаж болно. Ажил горилоход GitHub
профайл тань кодын жишээ болно — цэвэрхэн түүх, сайн README нь
мэргэжлийн байдлыг харуулна.
""",
            initial_code="""\
# ===== 1. Төсөл бэлдэх =====
mkdir dun-tootsooluur
cd dun-tootsooluur
git init

# ===== 2. .gitignore-ыг ЭХНИЙ commit-д =====
cat > .gitignore << 'EOF'
.env
node_modules/
*.log
.DS_Store
EOF

cat > README.md << 'EOF'
# Дүн тооцоолуур

Оюутны дүнгээс дундаж болон үнэлгээ гаргадаг скрипт.
EOF

git add .gitignore README.md
git commit -m "Төслийн бүтэц үүсгэв"

# ===== 3. Утга учиртай commit-ууд =====
cat > tootsooluur.py << 'EOF'
def dundaj(dunguud):
    if not dunguud:
        return 0.0
    return sum(dunguud) / len(dunguud)
EOF

git add tootsooluur.py
git commit -m "Дундаж тооцоолох функц нэмэв"

cat >> tootsooluur.py << 'EOF'


def unelgee(dundaj):
    if dundaj >= 90:
        return "A"
    if dundaj >= 80:
        return "B"
    if dundaj >= 60:
        return "D"
    return "F"
EOF

git add tootsooluur.py
git commit -m "Үнэлгээ гаргах функц нэмэв"

# ===== 4. GitHub дээр нийтлэх =====
gh repo create dun-tootsooluur --public --source=. --remote=origin
git push -u origin main

# CLI байхгүй бол GitHub дээр гараар үүсгээд:
# git remote add origin https://github.com/hereglegch/dun-tootsooluur.git
# git branch -M main
# git push -u origin main

# ===== 5. Release =====
git tag -a v1.0.0 -m "Анхны хувилбар"
git push --tags
gh release create v1.0.0 --generate-notes

# ===== 6. Шалгах =====
git log --oneline
git status
gh repo view --web
""",
        ),
    ],
)

COLLAB_PROJECT = ModuleSpec(
    title="Модул 16 — Хамтын ажиллагааны төсөл",
    description="Салаа, PR, код хянал, нэгтгэл.",
    lessons=[
        LessonSpec(
            title="Дадлага — Хамтын ажиллагаа",
            slug="hamtiin-tusul",
            description="Салаанаас нэгтгэл хүртэлх бүтэн зам.",
            duration=780,
            language=SH,
            content="""\
Энэ дадлагыг **хоёр хүн** хамтран хийвэл хамгийн үр дүнтэй. Ганцаараа
бол хоёр хавтсанд clone хийж, хоёр хүнийг дуурайж болно.

### Зорилго

1. Салаа гаргах
2. Ажиллаж commit хийх
3. PR нээх
4. Хянал авах, санал тусгах
5. Нэгтгэж цэвэрлэх

### Бэлтгэл

Нэг хүн агуулах үүсгээд нөгөөг нь хамтрагч болгон нэмнэ:

```bash
gh repo create bagiin-tusul --public --clone
gh api repos/{owner}/bagiin-tusul/collaborators/{ner} -X PUT
```

### Алхам 1 — Салаа

**Хоёулаа** өөр өөр салаа гаргана. Ижил файлын ижил мөрийг зориуд
засвал зөрчил үүсэхийг үзэж болно.

### Алхам 2 — PR

```bash
gh pr create --fill
```

`--fill` нь commit мессежээс гарчиг, тайлбарыг авна.

### Алхам 3 — Хянал

Нөгөө хүн PR-ыг хянана:

```bash
gh pr checkout 1
npm test
gh pr review 1 --comment --body "Null шалгалт нэмэх үү?"
```

### Алхам 4 — Санал тусгах

```bash
git commit -am "Хяналтын дагуу null шалгалт нэмэв"
git push
```

PR автоматаар шинэчлэгдэнэ.

### Алхам 5 — Нэгтгэх

```bash
gh pr merge 1 --squash --delete-branch
```

`--squash` нь салааны бүх commit-ыг нэг болгоно. `--delete-branch` нь
алсын салааг устгана.

### Алхам 6 — Цэвэрлэх

```bash
git switch main
git pull
git fetch --prune
git branch -d bolomj/miniy-ajil
```

### Зөрчил үүсгэж үзэх

Хоёулаа README-ийн **ижил мөрийг** өөрөөр засаад хоёуланг нь нэгтгэхийг
оролдоорой. Эхнийх нь амархан орно, хоёр дахь нь зөрчилдөнө.

Энэ бол **зориуд хийх дасгал** — жинхэнэ төсөл дээр биш, тайван орчинд
зөрчил шийдэж сурна.

### Шалгах жагсаалт

- PR-ийн тайлбар нь юу, яагаад хийснийг тайлбарлаж байна уу
- Хянагч дор хаяж нэг санал бичсэн үү
- Санал тусгагдсаны дараа PR шинэчлэгдсэн үү
- Нэгтгэсний дараа салаа устсан уу
- `main` дээрх түүх ойлгомжтой байна уу
""",
            initial_code="""\
# ===== БЭЛТГЭЛ (нэг хүн) =====
gh repo create bagiin-tusul --public --clone
cd bagiin-tusul

echo "# Багийн төсөл" > README.md
git add README.md
git commit -m "Анхны commit"
git push -u origin main

# Хамтрагч нэмэх: GitHub -> Settings -> Collaborators

# ===== НӨГӨӨ ХҮН =====
git clone https://github.com/ner/bagiin-tusul.git
cd bagiin-tusul

# ===== 1. Салаа гаргах (хоёулаа өөр өөрийнхийг) =====
git switch main
git pull
git switch -c bolomj/tanilzuulga

# ===== 2. Ажиллаж commit хийх =====
cat >> README.md << 'EOF'

## Тухай

Git сурах зорилготой дадлагын төсөл.
EOF

git add README.md
git commit -m "Танилцуулга хэсэг нэмэв"
git push -u origin bolomj/tanilzuulga

# ===== 3. PR нээх =====
gh pr create --fill

# ===== 4. Нөгөө хүн хянана =====
gh pr list
gh pr checkout 1
gh pr diff 1
gh pr review 1 --comment --body "Суулгах зааврыг ч нэмэх үү?"

# ===== 5. Санал тусгах =====
git switch bolomj/tanilzuulga
cat >> README.md << 'EOF'

## Суулгах

```bash
git clone <хаяг>
```
EOF

git commit -am "Хяналтын дагуу суулгах заавар нэмэв"
git push

# ===== 6. Зөвшөөрч нэгтгэх =====
gh pr review 1 --approve
gh pr merge 1 --squash --delete-branch

# ===== 7. Цэвэрлэх =====
git switch main
git pull
git fetch --prune
git branch -d bolomj/tanilzuulga

git log --oneline --graph --all
""",
        ),
    ],
)

REAL_WORLD = ModuleSpec(
    title="Модул 17 — Бодит ажлын урсгал",
    description="Clone, салаа, зөрчил, нэгтгэл — бүрэн мөчлөг.",
    lessons=[
        LessonSpec(
            title="Дадлага — Бодит ажлын урсгал",
            slug="bodit-urgats",
            description="Зөрчил шийдэх хүртэлх бүрэн зам.",
            duration=840,
            language=SH,
            content="""\
Эцсийн дадлага. Бодит ажилд тохиолддог бүх алхмыг дамжина — зөрчил
шийдэх ч дотроо.

### Бүтэн мөчлөг

```text
1.  Clone
2.  main-ийг шинэчлэх
3.  Боломжийн салаа гаргах
4.  Хэд хэдэн commit
5.  Push
6.  PR нээх
7.  Энэ хооронд main урагшилсан
8.  main-ийг салаандаа нэгтгэх
9.  Зөрчил шийдэх
10. Тест ажиллуулах
11. Push — PR шинэчлэгдэнэ
12. Хянал, нэгтгэл
13. Цэвэрлэх
```

Долоо дахь алхам бол **бодит байдал**. Таны ажиллах хугацаанд
багийнхан ажиллаж, `main` урагшилсан байна.

### Яагаад 8 дахь алхам чухал вэ

Зөрчлийг **өөрийн салаан дээр** шийдвэл:

- `main` эвдрэхгүй
- Тайван шалгах цаг байна
- PR нь цэвэр нэгтгэгдэнэ

`main` дээр шийдэх гэж оролдвол бүх багийг хааж магадгүй.

### Урт ажилд тогтмол нэгтгэ

```bash
git fetch origin
git merge origin/main
```

Өдөр бүр эсвэл хоёр өдөр тутам. Зөрчил бага багаар шийдэгдэнэ.

### Тест ажиллуулахаа бүү мартаарай

> Зөрчлийн тэмдэглэгээг арилгасан нь код ажиллаж байна гэсэн үг **биш**.
> Хоёр талын логик зөрчилдсөн байж болно. Нэгтгэсний дараа тест
> ажиллуулах нь заавал.

### Хэрэв бүх зүйл эвдэрвэл

```bash
git merge --abort            # нэгтгэлтийг цуцлана
git reflog                   # хаана байсныг олно
git reset --hard HEAD@{3}    # буцаана
```

Git-д бараг бүх зүйл сэргээгддэг. Сандрахаасаа өмнө `git reflog`
ажиллуул.

### Шалгах жагсаалт

- Салаа нь `main`-ээс гарсан, хуучин commit-оос биш
- Commit мессежүүд нь юу хийснийг тайлбарлаж байна
- Зөрчил зөв шийдэгдсэн — хоёр талын ажил хоёулаа үлдсэн
- Тест өнгөрсөн
- PR-ийн тайлбар бүрэн
- Нэгтгэсний дараа салаанууд цэвэрлэгдсэн

### Дараагийн алхам

Энэ сургалт Git-ийн өдөр тутмын 95 хувийг хамарлаа. Цааш сурах зүйлс:

| Сэдэв | Юунд |
|---|---|
| `git rebase -i` | Түүхийг цэгцлэх |
| `git cherry-pick` | Нэг commit-ыг өөр салаа руу |
| `git worktree` | Хэд хэдэн салааг зэрэг нээх |
| GitHub Actions | Автомат тест, байршуулалт |
| Git hooks | Commit-ийн өмнө автомат шалгалт |

Эдгээрийг **хэрэгцээ гарах үед** сур. Одоо мэдэж байгаа зүйл тань
ажлын ихэнхэд хангалттай.
""",
            initial_code="""\
# ===== 1-2. Clone ба шинэчлэх =====
git clone https://github.com/baig/tusul.git
cd tusul
git switch main
git pull

# ===== 3. Боломжийн салаа =====
git switch -c bolomj/hereglegchiin-profil

# ===== 4. Хэд хэдэн commit =====
# ... ажиллана ...
git add src/profil.js
git commit -m "Профайлын хуудасны бүтэц нэмэв"

git add src/profil.js
git commit -m "Профайл засах маягт нэмэв"

git add tests/profil.test.js
git commit -m "Профайлын тест нэмэв"

# ===== 5-6. Push ба PR =====
git push -u origin bolomj/hereglegchiin-profil
gh pr create --fill

# ===== 7. Энэ хооронд main урагшилсан =====
git fetch origin
git log HEAD..origin/main --oneline     # юу нэмэгдсэнийг хар

# ===== 8. main-ийг ӨӨРИЙН салаандаа нэгтгэх =====
git merge origin/main

# CONFLICT (content): Merge conflict in src/profil.js

# ===== 9. Зөрчил шийдэх =====
git status
git diff --name-only --diff-filter=U

# Файлыг нээж <<<<<<< ======= >>>>>>> мөрүүдийг арилгана.
# Хоёр талын ажил ХОЁУЛАА үлдэх ёстой эсэхийг бод.

git add src/profil.js
git diff --check                        # үлдсэн тэмдэглэгээ байна уу
git commit                              # мессежийг Git бэлдэнэ

# ===== 10. ЗААВАЛ тест =====
npm test

# ===== 11. Push — PR автоматаар шинэчлэгдэнэ =====
git push

# ===== 12. Хянал ба нэгтгэл =====
gh pr view --web
gh pr merge --squash --delete-branch

# ===== 13. Цэвэрлэх =====
git switch main
git pull
git fetch --prune
git branch -d bolomj/hereglegchiin-profil

# ===== Бүх зүйл эвдэрвэл =====
git merge --abort
git reflog
git reset --hard HEAD@{3}
""",
        ),
    ],
)

GIT_PRACTICE_MODULES = [PERSONAL, COLLAB_PROJECT, REAL_WORLD]
