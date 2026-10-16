# MedlegHub — System Architecture (MVP)

Монгол хэл дээрх интерактив програмчлалын сургалтын платформ.

Энэ баримт нь MVP-ийн эцсийн архитектур. Phase бүрийн өмнө үүнтэй нийцэж
байгааг шалгана.

---

## 1. Final system architecture

```
                    ┌────────────────────────────┐
                    │        Browser             │
                    │                            │
                    │  Next.js 16 (App Router)   │
                    │  ├─ RSC: public pages      │
                    │  ├─ Client: lesson player  │
                    │  │   ├─ Monaco Editor      │
                    │  │   ├─ Video.js (HLS)     │
                    │  │   └─ Sandbox Web Worker │ ← JS, Python, C/C++ энд ажиллана
                    │  └─ TanStack Query cache   │
                    └───────────┬────────────────┘
                                │ HTTPS + httpOnly cookie (JWT), JSON/REST
                    ┌───────────▼────────────────┐
                    │  FastAPI (Python 3.11+)    │  C/C++ эх код   ┌────────────────────────┐
                    │  ├─ api/v1 routers         │ ──────────────▶ │ Compiler (дотоод)      │
                    │  ├─ services (business)    │ ◀────────────── │ Emscripten → .wasm     │
                    │  ├─ schemas (Pydantic v2)  │   WebAssembly   │ read-only, нууцгүй     │
                    │  ├─ models (SQLAlchemy 2)  │                 └────────────────────────┘
                    │  └─ core (auth/config/rl)  │  MySQL код      ┌────────────────────────┐
                    │                            │ ──────────────▶ │ SQL runner (дотоод)    │
                    │                            │ ◀────────────── │ MySQL 8.4 sandbox      │
                    │                            │  хүснэгт (JSON) │ read-only, нууцгүй     │
                    └───────────┬────────────────┘                 └────────────────────────┘
                                │ asyncpg
                    ┌───────────▼────────────────┐
                    │       PostgreSQL 16        │
                    └────────────────────────────┘

  Static/video assets → Cloudflare R2 (S3-compatible) → CDN → Browser
```

### Хилүүд (boundaries)

| Хил | Шийдвэр |
|---|---|
| Frontend ↔ Backend | Зөвхөн REST/JSON. Next.js нь DB-д шууд хандахгүй. |
| User code ↔ Server | JavaScript, Python, C/C++ код сервер дээр АЖИЛЛАХГҮЙ — зөвхөн browser Web Worker дотор. JavaScript, Python код сервер рүү огт очихгүй. C/C++-ийн эх код хөрвүүлэгдэхээр очих ч хадгалагдахгүй. **Үл хамаарах зүйл нь MySQL:** өгөгдлийн сан хөтөчид ажилладаггүй тул тусгаарлагдсан SQL runner дээр ажиллана (§8). |
| API ↔ Compiler | Дотоод HTTP. Хөрвүүлэгч нь нууц мэдээлэлгүй, өгөгдлийн сангүй, зөвхөн уншигдах файлын системтэй тусдаа контейнер (§8). |
| API ↔ SQL runner | Дотоод HTTP. Нууц мэдээлэлгүй, API-ийн PostgreSQL-тэй холбоогүй, гадагш сүлжээгүй тусдаа контейнер. Ажиллагаа бүрийн дараа MySQL цэвэрлэгдэж шалгагдана (§8). |
| Video | Backend нь зөвхөн `video_url` хадгална. Stream нь CDN-ээс шууд ирнэ. |

### Технологийн сонголт

| Давхарга | Технологи | Шалтгаан |
|---|---|---|
| Frontend | Next.js 16 App Router, TypeScript strict | RSC-ээр public хуудсууд хурдан, SEO сайн |
| Styling | Tailwind CSS v4 + shadcn/ui | Vendored component, гадаад dependency бага |
| Server state | TanStack Query v5 | Cache + dedupe — lesson хуудсан дээрх давхардсан дуудлагыг арилгана |
| Editor | Monaco, lazy | Спекээр шаардсан |
| Video | Video.js + HLS, lazy | Спекээр шаардсан |
| Backend | FastAPI + SQLAlchemy 2.0 async + asyncpg | Async I/O, ORM-оор SQL injection-оос хамгаална |
| Migrations | Alembic | Схемийн өөрчлөлт бүр migration-тай |
| DB | PostgreSQL 16 | Спекээр шаардсан |

---

## 2. Database ERD

```
┌──────────────────┐             ┌──────────────────────┐
│ users            │             │ courses              │
├──────────────────┤             ├──────────────────────┤
│ id          PK   │             │ id              PK   │
│ email       UQ   │             │ title                │
│ password_hash    │             │ slug            UQ   │
│ name             │             │ description          │
│ role  enum       │             │ thumbnail_url        │
│ created_at       │             │ difficulty  enum     │
└───┬──────────┬───┘             │ category    enum     │
    │          │                 │ is_free     bool     │
    │          │                 │ published   bool     │
    │          │                 │ created_at           │
    │          │                 │ updated_at           │
    │          │                 └──────┬───────────────┘
    │          │                        │ 1:N
    │          │                 ┌──────▼───────────────┐
    │          │                 │ modules              │
    │          │                 ├──────────────────────┤
    │          │                 │ id              PK   │
    │          │                 │ course_id       FK   │
    │          │                 │ title                │
    │          │                 │ description          │
    │          │                 │ position  int        │
    │          │                 └──────┬───────────────┘
    │          │                        │ 1:N
    │          │                 ┌──────▼───────────────┐
    │          │                 │ lessons              │
    │          │                 ├──────────────────────┤
    │          │                 │ id              PK   │
    │          │                 │ module_id       FK   │
    │          │                 │ title                │
    │          │                 │ slug                 │
    │          │                 │ description          │
    │          │                 │ video_url            │
    │          │                 │ duration  int (sec)  │
    │          │                 │ content   markdown   │
    │          │                 │ initial_code  text   │
    │          │                 │ language             │
    │          │                 │ position  int        │
    │          │                 │ published bool       │
    │          │                 │ exercise  jsonb      │
    │          │                 └──────┬───────────────┘
    │          │                        │
    │ 1:N      │ 1:N                    │ 1:N
┌───▼──────────▼──────┐          ┌──────▼───────────────┐
│ enrollments         │          │ lesson_progress      │
├─────────────────────┤          ├──────────────────────┤
│ id             PK   │          │ id              PK   │
│ user_id        FK   │          │ user_id         FK   │
│ course_id      FK   │          │ lesson_id       FK   │
│ created_at          │          │ completed  bool      │
│ UQ(user_id,course)  │          │ completed_at         │
└─────────────────────┘          │ UQ(user_id,lesson)   │
                                 └──────────────────────┘

users 1:N
┌───────────────────────┐
│ user_badges           │   Тэмдгийн тодорхойлолт кодод:
├───────────────────────┤   `app/content/badges.py`
│ id               PK   │
│ user_id          FK   │
│ badge_key             │
│ awarded_at            │
│ showcase_position     │   онцлох байр 1–5, NULL
│ UQ(user_id,badge_key) │
│ UQ(user_id,showcase_  │
│    position)          │
└───────────────────────┘
```

### Индексүүд

| Хүснэгт | Индекс | Зорилго |
|---|---|---|
| users | UNIQUE(email) | Login lookup |
| courses | UNIQUE(slug); INDEX(published, category, difficulty) | Catalog filter |
| modules | INDEX(course_id, position) | Curriculum ordering |
| lessons | INDEX(module_id, position); UNIQUE(module_id, slug) | Ordering, slug lookup |
| enrollments | UNIQUE(user_id, course_id) | Давхар enrollment-аас хамгаална |
| lesson_progress | UNIQUE(user_id, lesson_id); INDEX(user_id) | Upsert, dashboard |

### Enum-ууд

- `role`: `student`, `admin`
- `difficulty`: `beginner`, `intermediate`, `advanced`
- `category`: `html_css`, `javascript`, `python`, `c`, `csharp`, `java`, `react`, `backend`, `database`, `git`

Enum-уудыг PostgreSQL native enum биш **VARCHAR + CHECK** байдлаар хадгална —
шинэ category нэмэхэд migration хялбар болно.

### Cascade

`course` устгахад modules → lessons → lesson_progress бүгд `ON DELETE CASCADE`.
`user` устгахад enrollments болон lesson_progress cascade.

---

## 3. API architecture

Бүх route `/api/v1` prefix дор. Frontend `NEXT_PUBLIC_API_URL`-ээр заана.

| Method | Path | Auth | Тайлбар |
|---|---|---|---|
| POST | `/auth/register` | — | Бүртгүүлэх, cookie тавина |
| POST | `/auth/login` | — | Нэвтрэх, cookie тавина |
| POST | `/auth/logout` | user | Cookie устгана |
| GET | `/auth/me` | user | Одоогийн хэрэглэгч |
| GET | `/courses` | optional | `?q=&category=&difficulty=&page=&page_size=` |
| GET | `/courses/{slug}` | optional | Detail + curriculum + progress |
| POST | `/courses` | admin | Үүсгэх |
| PATCH | `/courses/{id}` | admin | Засах / publish toggle |
| DELETE | `/courses/{id}` | admin | Устгах |
| POST | `/courses/{id}/modules` | admin | Module үүсгэх |
| PATCH | `/modules/{id}` | admin | Module засах / position |
| DELETE | `/modules/{id}` | admin | Module устгах |
| GET | `/lessons/{id}` | user | Lesson дэлгэрэнгүй |
| POST | `/modules/{id}/lessons` | admin | Lesson үүсгэх |
| PATCH | `/lessons/{id}` | admin | Lesson засах |
| DELETE | `/lessons/{id}` | admin | Lesson устгах |
| POST | `/courses/{id}/enroll` | user | Enroll (idempotent) |
| GET | `/me/courses` | user | Миний сургалтууд + progress |
| GET | `/me/profile` | user | Профайл: статистик ба тэмдгүүд (ховор байдал, онцлох байртай). Хангасан ч олгоогүй тэмдгийг олгоно |
| PUT | `/me/showcase` | user | Нэрийн хажууд онцлох 0–5 авсан тэмдэг, дарааллаар |
| GET | `/lessons/{id}/help` | user | Дасгалын зөвлөгөө ба жишиг шийдэл («Тусламж») |
| POST | `/lessons/{id}/complete` | user | Хичээл дуусгах (idempotent) |
| GET | `/courses/{id}/progress` | user | Course progress |

### Нэмэлт route

| Method | Path | Auth | Шалтгаан |
|---|---|---|---|
| GET | `/courses/{slug}/lessons/{lessonSlug}` | user | Lesson player нэг дуудлагаар lesson + curriculum + progress авна (Performance §22). |
| GET | `/admin/courses/{id}` | admin | Админ засварын дэлгэцэд нийтлэгдээгүй модул/хичээл ч харагдах ёстой. Нийтийн `/courses/{slug}` нь тэдгээрийг шүүдэг. |
| POST | `/compile` | user | C/C++ → WebAssembly (`application/wasm`). Хэрэглэгч бүрт минутад 60, эх код 64 KB хүртэл. |
| POST | `/sql/run` | user | MySQL кодыг тусгаарлагдсан MySQL 8.4 дээр ажиллуулж үр дүнг JSON-оор буцаана. Хэрэглэгч бүрт минутад 60, код 64 KB хүртэл. |

Эхнийх нь §18-ийн `GET /lessons/{id}`-ийн slug хувилбар бөгөөд §19-д заасан
`/learn/[courseSlug]/[lessonSlug]` route-ыг ажиллуулахад шаардлагатай. Хоёр дахь
нь §15-д заасан админы CRUD-ыг ажиллуулахад шаардлагатай. Гурав дахь нь C/C++
хичээлийн кодыг хөтөч дотор ажиллуулахад шаардлагатай (§8). Дөрөв дэх нь MySQL
хичээлийн кодыг серверийн sandbox дээр ажиллуулна (§8).

### Алдааны формат

```json
{ "detail": { "code": "COURSE_NOT_FOUND", "message": "Сургалт олдсонгүй." } }
```

`POST /compile`-ийн хөрвүүлэлтийн алдаа (422, `COMPILE_ERROR`) нь хөрвүүлэгчийн
мессежийг `diagnostics` талбарт нэмж өгнө — сурагч аль мөрөнд алдсанаа харах
ёстой. Амжилттай хариу JSON биш, WebAssembly байт; `-Wall` анхааруулга нь
модулийн `medleghub.warnings` custom section дотор ирнэ.

`POST /sql/run`-д сурагчийн SQL алдаа HTTP алдаа БИШ — 200 хариуны `error`
талбарт `line`, `code`, `sqlstate`-тэй ирнэ (`ERROR 1146 (42S02)`).
`SQL_RUNNER_BUSY` (503), `SQL_RUNNER_UNAVAILABLE` (503), `SQL_RUN_TIMEOUT` (504)
нь үйлчилгээний алдаа.

---

## 4. Frontend route structure

```
app/
├── (public)/
│   ├── page.tsx                              /
│   ├── courses/page.tsx                      /courses
│   └── courses/[slug]/page.tsx               /courses/[slug]
├── (auth)/
│   ├── login/page.tsx                        /login
│   └── register/page.tsx                     /register
├── (app)/
│   └── dashboard/page.tsx                    /dashboard        [protected]
├── learn/
│   └── [courseSlug]/[lessonSlug]/page.tsx    /learn/...        [protected]
└── admin/
    ├── page.tsx                              /admin            [admin]
    ├── courses/page.tsx                      /admin/courses
    ├── courses/new/page.tsx                  /admin/courses/new
    ├── courses/[id]/page.tsx                 /admin/courses/[id]
    ├── courses/[id]/modules/page.tsx         /admin/courses/[id]/modules
    ├── lessons/new/page.tsx                  /admin/lessons/new?module=&course=
    └── lessons/[id]/page.tsx                 /admin/lessons/[id]
```

`/admin/lessons/new` нь §19-д тусгайлан заагаагүй боловч §15-ийн «Lessons —
Create» боломжийг хэрэгжүүлэхэд шаардлагатай.

`/learn` нь бүтэн дэлгэцийн өөрийн layout ашиглана (site header/footer-гүй).

---

## 5. Component architecture

```
components/
├── ui/              shadcn primitives (button, input, card, dialog, ...)
├── layout/          SiteHeader, SiteFooter, ThemeToggle, UserMenu
├── marketing/       Hero, FeaturedCourses, HowItWorks, InteractiveDemo,
│                    WhyLearnHere, CtaSection
├── courses/         CourseCard, CourseGrid, CourseFilters, CourseSearch,
│                    CurriculumList, LessonRow, ProgressBar, EnrollButton
├── learn/           LessonLayout, CurriculumSidebar, VideoPlayer,
│                    LessonContent, CodeEditor, ConsoleOutput,
│                    ResizableSplit, LessonNav, CompleteButton
├── dashboard/       ContinueLearningCard, MyCoursesList
├── admin/           AdminShell, CourseForm, ModuleForm, LessonForm,
│                    PositionControls, PublishToggle
└── common/          Skeletons, EmptyState, ErrorState, Pagination
```

```
lib/
├── api/             client.ts, auth.ts, courses.ts, lessons.ts,
│                    progress.ts, admin.ts, compile.ts, sql.ts
├── hooks/           useAuth, useCourses, useCourse, useLesson, useProgress
├── sandbox/         runner.ts + worker-source.ts        (JavaScript)
│                    python-runner.ts + python-worker-source.ts (Python)
│                    native-runner.ts + native-worker-source.ts (C/C++)
│                    sql-runner.ts                       (MySQL — сервер дээр)
├── types/           api.ts
└── i18n/            mn.ts (бүх UI текст нэг газар)
```

Дүрэм: нэг component нэг файл, ~200 мөрөөс богино. Бизнес логик component
дотор биш `lib/hooks` дотор.

---

## 6. Folder structure

```
Suralts/
├── apps/
│   ├── api/                 FastAPI
│   │   ├── alembic/
│   │   ├── app/
│   │   │   ├── api/v1/      routers
│   │   │   ├── content/     хичээлийн агуулга (код биш, өгөгдөл)
│   │   │   ├── core/        config, security, deps, rate limit, errors
│   │   │   ├── db/          engine, session, Base
│   │   │   ├── models/      SQLAlchemy models
│   │   │   ├── schemas/     Pydantic schemas
│   │   │   ├── services/    business logic
│   │   │   └── main.py
│   │   ├── tests/
│   │   └── pyproject.toml
│   ├── compiler/            C/C++ хөрвүүлэгч (тусдаа контейнер)
│   │   ├── compiler/        HTTP үйлчилгээ, emcc ажиллуулагч, PCH, кэш
│   │   ├── tests/
│   │   └── Dockerfile       emscripten/emsdk:6.0.9 + prewarm
│   ├── sql-runner/          MySQL sandbox (тусдаа контейнер)
│   │   ├── sqlrunner/       HTTP үйлчилгээ, mysqld slot, цэвэрлэгээ, statement хуваагч
│   │   ├── sandbox/         delguur.sql, nomiin_san.sql — хичээлийн жишээ сангууд
│   │   ├── tests/
│   │   └── Dockerfile       mysql:8.4.11 + prewarm (цэвэр datadir загвар)
│   └── web/                 Next.js
│       ├── src/app/
│       ├── src/components/
│       ├── src/lib/
│       └── package.json
├── docs/ARCHITECTURE.md
├── docker-compose.yml       PostgreSQL + C/C++ хөрвүүлэгч + MySQL sandbox (dev)
└── README.md
```

---

## 7. MVP development roadmap

| Phase | Агуулга | Дуусах шалгуур |
|---|---|---|
| 1 | Project setup | Postgres контейнер, API `/health` 200, web dev server |
| 2 | DB + backend | Бүх model, migration, §18-ийн endpoint, seed data |
| 3 | Public frontend | Landing, catalog (search/filter), course detail |
| 4 | Auth UI | Register/login/logout, protected route guard |
| 5 | Lesson player | Video, markdown, Monaco, Worker sandbox, console, reset |
| 6 | Progress | Enroll, complete, course progress, dashboard |
| 7 | Admin | Course/module/lesson CRUD + publish |
| 8 | Polish | Responsive, loading/empty/error, perf, security review |

---

## 8. Key security decisions

1. **User code isolation.** Сурагчийн код ЗӨВХӨН Web Worker дотор ажиллана.
   Worker-т DOM, cookie, localStorage байхгүй. Сүлжээний API-г (`fetch`,
   `XMLHttpRequest`, `WebSocket`, `EventSource`, `importScripts`, `indexedDB`,
   `caches`, `Worker`, `BroadcastChannel`) устгана. 3 секундын timeout, дараа
   нь `worker.terminate()` — infinite loop таслагдана. Backend нь сурагчийн
   кодыг хэзээ ч ажиллуулахгүй, хадгалахгүй. C/C++-ийн эх код
   нь зөвхөн хөрвүүлэгдэхээр сервер рүү очно — доорх «C/C++»-ийг үз.

   Гурван хэл, гурван worker:

   | | JavaScript | Python | C/C++ |
   |---|---|---|---|
   | Ажиллуулагч | `AsyncFunction` | Pyodide (CPython → WebAssembly) | Серверт хөрвүүлсэн WebAssembly + WASI shim |
   | Worker төрөл | classic (`blob:`) | module (`blob:`, Pyodide нь ESM) | classic (`blob:`) |
   | Хамгаалалтын дараалал | эхлэнгүүт хаана | **ачаалсны дараа хаана** | эхлэнгүүт хаана |
   | Дахин ашиглалт | ажиллуулах бүрд шинэ | хадгална (ачаалалт удаан) | ажиллуулах бүрд шинэ |

   **Дараалал урвуу байгаа нь зориудынх.** Pyodide өөрийн WebAssembly болон
   стандарт санг татахад `fetch` хэрэгтэй. Тиймээс: (1) ачаална,
   (2) сүлжээний API-г устгана, (3) ДАРАА НЬ сурагчийн кодыг хүлээж авна.
   Энэ дараалал буруу бол сүлжээ нээлттэй үлдэнэ — `e2e/python-sandbox.spec.mjs`
   нь устсан эсэхийг Python талаас нь шалгадаг.

   Багц суулгах боломжгүй: стандарт сан бүхэлдээ `python_stdlib.zip` дотор
   ирдэг тул сүлжээ хаасны дараа ч math, json, dataclasses, collections,
   pathlib бүгд ажиллана. `requests`, `sqlalchemy` зэрэг гуравдагч сан
   ТАТАГДАХГҮЙ — сурагчийн код сүлжээнд хандах ёсгүй.

   **Хугацаа хэтрэлт.** SharedArrayBuffer (тэгснээр Pyodide-ийн
   `setInterruptBuffer`) нь cross-origin isolation шаарддаг бөгөөд тэр нь
   гадаад thumbnail-уудыг эвдэнэ. Тиймээс зогсоох арга нь `terminate()` —
   дараагийн ажиллуулалт Pyodide-ийг шинээр ачаална. Үүнээс болж `input()`
   нь гараас хүлээж чадахгүй тул мөрүүдийг урьдчилан өгдөг оролтын талбартай.

   **C/C++ — серверт хөрвүүлж, хөтөч дотор ажиллуулна.** Хөтөч дотор clang
   татах нь хэдэн арван MB тул хөрвүүлэлтийг сервер хийнэ. Сервер кодыг
   АЖИЛЛУУЛАХГҮЙ — зөвхөн WebAssembly модуль гаргаж, сурагчийн хөтөч доторх
   worker ажиллуулна. Гэхдээ clang нь итгэлгүй оролт боловсруулдаг том програм
   тул хамгаалалт давхраатай:

   - **API:** зөвхөн нэвтэрсэн хэрэглэгч, хэрэглэгчээр минутад 60 (IP-гаар
     биш — нэг ангийн сурагчид нэг IP-ийн ард байдаг), эх код 64 KB.
   - **Контейнер:** нууц мэдээлэлгүй, өгөгдлийн сангүй, **read-only root
     filesystem** (зөвхөн `/tmp` бичигдэнэ), эрхгүй хэрэглэгч, `cap_drop: ALL`,
     `no-new-privileges`, 2 GB санах ой, 128 процесс. Upstream emsdk image нь
     хөрвүүлэгчийг хэн ч бичих эрхтэй (777) ирүүлдэг тул read-only нь ЗААВАЛ —
     эс бөгөөс эвдэрсэн хөрвүүлэлт дараагийн сурагчдын хөрвүүлэгчийг өөрчилж
     чадна. Үйлчилгээ эхлэхдээ шалгаж анхааруулдаг, CI нь `--read-only`-оор
     тестэлдэг. Production-д API-тай нэг дотоод сүлжээнд, гадагш сүлжээгүй.
   - **Хүсэлт бүр:** өөрийн түр хавтас, 15 с хугацаа (clang, wasm-ld-ийн
     процессын бүлгийг бүхэлд нь устгана), `prlimit` (CPU, файлын хэмжээ,
     2 GB хаягийн зай), stdin хаалттай, мессеж 1 MB-аас хэтэрвэл зогсооно.
   - **Тугууд** зөвхөн сервер талд — сурагчийн кодоос юу ч нэмэгдэхгүй.
   - `#include "/etc/passwd"` зэргээр контейнер доторх файлыг мессежээр харж
     болохыг хүлээн зөвшөөрсөн. Тиймээс контейнерт нууц мэдээлэл хэзээ ч бүү өг.

   Worker нь модульд зөвхөн WASI (`wasi_snapshot_preview1`) импорт өгнө:
   stdout/stderr, stdin (урьдчилан бэлдсэн мөрүүд — терминал шиг нэг удаад нэг
   мөр, асуултын ард харагдана), цаг, санамсаргүй тоо, гарах. Файлын систем,
   сүлжээ байхгүй. Шинэ туг worker хангадаггүй импорт нэмбэл
   `apps/compiler/tests/test_service.py` баригдана.

   `main`-аас гарсан C++ exception нь g++-тэй ижил «terminate called after
   throwing an instance of …» мессеж хэвлээд abort болно. Emscripten-ийн
   `_start` нь `main` биш `__main_void`-ийг дууддаг тул хөрвүүлэгч түүнийг
   ороодог (`apps/compiler/compiler/toolchain.py`).

   **MySQL — серверийн sandbox дээр ажиллана.** Өгөгдлийн сан хөтөчид
   ажилладаггүй тул энэ нь сурагчийн код СЕРВЕР ДЭЭР ажилладаг цорын ганц
   тохиолдол. Хөтөч дотор SQLite ажиллуулах хувилбарыг хэмжиж үзсэн: 73
   хичээлийн нэг нь ч бүтэн ажиллаагүй (`USE`, `DELIMITER`, `SHOW`, `GRANT`,
   T-SQL), бүтэн ажилласан ч MySQL-ээс өөр дүрмээр (төрөл, гадаад түлхүүр)
   ажилладаг тул татгалзсан. SQL Server-ийн контейнер зөвхөн x86-64 тул ARM
   VM дээр ажиллахгүй — T-SQL хичээлд товч идэвхгүй.

   - **API:** зөвхөн нэвтэрсэн хэрэглэгч, хэрэглэгчээр минутад 60, код 64 KB.
     Ажиллуулагчийн хариуг Pydantic-аар шалгаж байж хөтөч рүү дамжуулна.
   - **Контейнер:** хөрвүүлэгчтэй ижил — нууцгүй, read-only root, эрхгүй
     хэрэглэгч, `cap_drop: ALL`, `no-new-privileges`, 1.5 GB санах ой, 256
     процесс, `internal: true` сүлжээ. MySQL нь `skip-networking` (зөвхөн unix
     socket), `secure_file_priv=NULL`, `local_infile=OFF`.
   - **Slot:** `SQLRUNNER_SLOTS` тооны тусдаа `mysqld`, datadir нь tmpfs дээр.
     Нэг slot-д нэг л ажиллагаа; бусад нь дараалалд хүлээж, 10 с дараа 503.
   - **Эрх:** сурагч `student` данстай. Хичээлд хэрэгтэй сан, хэрэглэгч, role
     үүсгэх, GRANT хийх эрхтэй боловч `SYSTEM_USER`, `FILE`, `SUPER`,
     `SYSTEM_VARIABLES_ADMIN`, `SET_ANY_DEFINER`-гүй, `mysql` схемийг зөвхөн
     уншина (partial revoke). Тиймээс root-ийг өөрчлөх, root-ийг role болгох,
     эрхийн хүснэгт засах, файл унших/бичих, глобал тохиргоо өөрчлөх боломжгүй —
     `apps/sql-runner/tests/test_sandbox.py` бүгдийг жинхэнэ MySQL дээр шалгана.
   - **Хүсэлт бүр:** 10 с (хэтэрвэл админ холболтоос `KILL`), нэг үр дүнд 200
     мөр харуулж 100 000 хүртэл тоолно, гаралт 200 000 тэмдэгт, 500 statement.
     Үр дүнг unbuffered уншдаг тул асар том хүснэгт санах ойд ачаалагдахгүй.
   - **Цэвэрлэгээ:** ажиллагаа бүрийн дараа холболт, XA transaction (холболт
     тасарсны дараа ч түгжээ барьдаг), сан, хэрэглэгчийг устгаж, `student`-ийг
     дахин үүсгээд жишээ сангуудыг (`delguur`, `nomiin_san`) ачаалж ШАЛГАНА
     (~0.2 с). Шалгалт тэнцэхгүй,
     процесс унасан эсвэл 200 ажиллагааны дараа datadir-ийг image доторх цэвэр
     загвараас хуулж дахин эхлүүлнэ (~1 с).
   - `SET SESSION sort_buffer_size` зэрэг сессийн буферийг MySQL хязгаарладаггүй.
     Санах ой хэтэрвэл контейнерийн хязгаар бусад үйлчилгээг хамгаална: унасан
     `mysqld`-г pool дахин эхлүүлж, ажиллуулагч өөрөө унавал Docker эхлүүлнэ.
2. **Нууц үг.** `bcrypt` шууд, cost 12.
3. **JWT + httpOnly cookie.** Token localStorage-д хадгалахгүй (XSS эрсдэл).
   HS256, 7 хоног, `httpOnly`, `Secure` (prod), `SameSite` env-ээр тохируулна.
   Logout cookie-г устгана.
4. **CSRF.** `SameSite=Lax` cookie, бүх state-changing хүсэлт
   `Content-Type: application/json` (CORS preflight шаардагдана).
5. **Role-based authorization.** `require_admin` dependency. Эрхийг зөвхөн
   backend олгоно; frontend-ийн нуулт нь UX-ийн зорилготой.
6. **Progress-д итгэхгүй.** `complete` нь enrollment болон published эсэхийг
   backend дээр шалгана.
7. **Input validation.** Pydantic v2 дээр `max_length`, slug regex, position
   bounds. Бүх DB хандалт ORM/bound parameter-ээр.
8. **Rate limiting.** Sliding-window: `/auth/login`, `/auth/register` дээр
   IP-ээр 10 req/min. Backend interface дараа Redis руу солигдохоор.
9. **Markdown.** `react-markdown`, raw HTML идэвхгүй.
10. **Secrets.** Бүгд env-д. `.env` git-д орохгүй, зөвхөн `.env.example`.

---

## 9. Key performance decisions

1. **Lesson хуудас 1 API дуудлага** — lesson + curriculum + progress нэг response.
   E2E тестээр баталгаажсан (`e2e/student-journey.spec.mjs`).
2. **TanStack Query** `staleTime`: catalog 60s, lesson 30s. Сервер дээр
   render хийгдсэн хариу нь `initialDataUpdatedAt: 0`-тэй — нэвтэрсэн
   хэрэглэгчийн ахиц нэмэгдэж ирнэ.
3. **Monaco lazy** — `next/dynamic` + `ssr: false`. Нийтийн хуудсууд дээр
   огт татагдахгүй.
4. **Video.js lazy** — зөвхөн `video_url` байгаа үед import.
5. **RSC** — landing болон catalog server дээр render.
6. **Индексүүд** — §2-ийн бүгд migration-д.
7. **Pagination** — `/courses` анхдагч 12 мөр.
8. **N+1-ээс зайлсхийх** — curriculum `selectinload`, progress нэг `IN` query.
9. **Skeleton states** бүх жагсаалт/detail хуудсанд.
10. **Monaco өөрөө хостлогдоно** (`public/monaco`) — гуравдагч CDN руу хүсэлт
    явахгүй. Файлууд нэрэндээ hash-тай тул `immutable` cache-тэй.
11. **Pyodide өөрөө хостлогдоно** (`public/pyodide`, 12.9 MB) — мөн
    `immutable` cache-тэй. Зөвхөн Python хичээл дээр татагдана.
12. **Pyodide урьдчилан ачаалагдана** — хичээл нээгдэнгүүт эхэлнэ, сурагч
    тайлбараа уншиж байх зуур бэлэн болно. Хэмжилтээр "Ажиллуулах" дарахад
    гаралт 52 мс дотор гарсан.
13. **Python worker хадгалагдана** — ажиллуулах бүрд дахин ачаалахгүй.
    Зөвхөн timeout болсон үед л шинээр үүснэ.
14. **C/C++ хөрвүүлэлт ~0.2–0.5 с** (emsdk 6.0.9, `-O1`). C++-ийн хугацааны
    ихэнхийг стандарт толгой файл задлах эзэлдэг тул `<iostream>`-ийн PCH
    ашиглана: хичээлийн C++ ~0.9 с → ~0.3 с. PCH нь сурагч өөрөө
    `#include <iostream>` бичсэн үед л хэрэглэгдэнэ — мартсан `#include`
    алдаа хэвээр гарна (`apps/compiler/compiler/pch.py`).
15. **Хоёр түвшний кэш.** Сервер ижил кодын үр дүнг (хөрвүүлэлтийн алдааг ч)
    sha256-аар 128 MB хүртэл санана, ангийн сурагчид зэрэг дарсан ч
    хөрвүүлэлт нэг л удаа болно. Хөтөч сүүлийн 8 үр дүнг хадгалдаг тул
    зөвхөн «Оролт» өөрчлөхөд сервер рүү огт хандахгүй.
16. **C/C++-ийн анхны код урьдчилан хөрвүүлэгдэнэ** — Pyodide шиг хичээл
    нээгдэнгүүт эхэлнэ.
17. **WebAssembly модуль gzip-ээр** — C++ модуль ~200 KB → ~70 KB.

### Хэмжсэн үзүүлэлт (production build, gzip)

| Хуудас | JS (сүлжээгээр) | Тайлбар |
|---|---|---|
| Нийтийн хуудсууд | ~330 KB | React 19 + Query + Radix |
| Хичээлийн хуудас (анх) | +2.7 MB | Monaco (үүнээс 1.5 MB нь TS worker) |
| Хичээлийн хуудас (дараа) | 0 KB | `immutable` cache-аас уншина |
| Python хичээл (анх) | +12.9 MB | Pyodide; шахагдсан байдлаар ~5 MB |
| Python хичээл (дараа) | 0 KB | `immutable` cache-аас уншина |
| C/C++ «Ажиллуулах» | C ~15 KB, C++ ~70 KB | Серверт хөрвүүлсэн модуль, gzip |

Monaco-ийн TypeScript worker нь засварлагч дотор шууд syntax алдаа харуулахад
хэрэгтэй — шинэ суралцагчид үнэ цэнэтэй. Зөвхөн нэг удаа татагдана.

---

## 11. Хүртээмж (accessibility)

Бүх хуудас axe-core-ийн WCAG 2.1 A/AA шалгуурыг гэрэл, харанхуй горим
хоёуланд нь давдаг (`e2e/a11y.spec.mjs`).

Шийдвэрлэсэн гол зүйлс:

- Брэндийн өнгөний гэрэлтлийг (L) 4.5:1 харьцаа хангахаар сонгосон:
  гэрэл горимд `oklch(0.5 0.13 195)` → 5.16:1, харанхуйд 8.21:1.
- Хичээлийн уншлагын хэсэг нь гүйлгэгддэг тул `tabIndex={0}`-тэй —
  гарын түлхүүрээр хандах боломжтой (WCAG 2.1.1).
- Хэмжээ өөрчлөх зурвас нь `role="separator"`, `aria-valuenow`-тэй бөгөөд
  сум товчоор ажиллана — хулганагүйгээр хэмжээг өөрчилж болно (WCAG 2.1.1).
- Эвхэгдсэн хөтөлбөр нь `inert` — харагдахгүй байхдаа фокус авахгүй.
- Формын талбар бүр `aria-invalid`, `aria-describedby`-аар алдаатай холбогдсон.
- Хэвтээ гүйлт 320px-ээс эхлэн ямар ч хуудсанд байхгүй.

---

## 10. Assumptions

1. §18-ийн path-ууд `/api/v1` prefix дор байрлана.
2. Lesson slug course дотор давтагдахгүй.
3. `duration` секундээр. Course duration нь lesson-уудын нийлбэр, тооцоологдоно.
4. Course duration/lesson count DB-д хадгалагдахгүй, query-д тооцогдоно.
5. "Locked" статус зөвхөн визуал; sequential lock хийхгүй.
6. Premium course enroll хийх боломжгүй, "Тун удахгүй" гэж харуулна.
7. Бүх PK нь UUID v4.
8. Video нь гадаад URL (R2/CDN эсвэл HLS manifest). Upload UI байхгүй.
9. Email verification / forgot password — model түвшинд орон зай үлдээнэ,
   MVP-д implement хийхгүй.
10. Бүх UI монгол. Техник нэр томъёо англиар хаалтанд.

---

## 12. Сургалтын агуулга

Агуулга нь `apps/api/app/content/` дотор `CourseSpec` / `ModuleSpec` /
`LessonSpec` dataclass хэлбэрээр байрлана. Seed нь зөвхөн өгөгдлийн санд
бичих ажлыг гүйцэтгэнэ.

```
app/content/
├── types.py           CourseSpec, ModuleSpec, LessonSpec
├── placeholders.py    React — агуулгагүй
├── c_cpp/             C ба C++ үндэс (21 модул, 52 хичээл)
│   ├── c_basics.py           Модул 1-5
│   ├── c_core.py             Модул 6-10
│   ├── cpp_basics.py         Модул 11-15
│   ├── cpp_core.py           Модул 16-19
│   └── projects.py           Модул 20-21
├── git_github/        Git ба GitHub (18 модул, 39 хичээл)
│   ├── fundamentals.py       Модул 0-1
│   ├── basics.py             Модул 2-5
│   ├── branching.py          Модул 6-9
│   ├── intermediate.py       Модул 10-14
│   └── practice.py           Модул 15-17
├── html_css/          HTML & CSS үндэс (20 модул, 54 хичээл)
│   ├── fundamentals.py       Модул 0
│   ├── html_basics.py        Модул 1-3
│   ├── html_structure.py     Модул 4-6
│   ├── css_basics.py         Модул 7-9
│   ├── css_layout.py         Модул 10-13
│   ├── responsive.py         Модул 14-15
│   └── projects.py           Модул 16-19
├── javascript/        JavaScript үндэс (26 модул, 71 хичээл)
│   ├── fundamentals.py       Модул 0
│   ├── basics.py             Модул 1-4
│   ├── functions_data.py     Модул 5-8
│   ├── beginner_projects.py  Модул 9
│   ├── browser.py            Модул 10-13
│   ├── browser_projects.py   Модул 14
│   ├── modern.py             Модул 15-17
│   ├── async_api.py          Модул 18-19
│   ├── tooling.py            Модул 20-21
│   └── projects.py           Модул 22-25
├── python/            Python (29 модул, 44 хичээл)
│   ├── fundamentals.py     Модул 0
│   ├── beginner_core.py    Модул 1-6
│   ├── beginner_applied.py Модул 7-14
│   └── intermediate.py     Модул 15-28
└── sql/               Өгөгдлийн Сангийн Үндэс (MySQL) (22 модул, 87 хичээл, 23 мөрдөгчийн хэрэг)
    ├── fundamentals.py       Модул 0-1
    ├── querying.py           Модул 2-5
    ├── data_definition.py    Модул 6-8
    ├── joins.py              Модул 9-11
    ├── design.py             Модул 12-14
    ├── advanced.py           Модул 15-18
    └── projects.py           Модул 19-20
```

«Өгөгдлийн Сангийн Үндэс (MySQL)» сургалтад хичээлийн `language` нь
анхны кодын аялгууг заана: `mysql` эсвэл `sql`
(SQL Server / T-SQL). Ихэнх хичээл Модул 1-ийн `delguur` жишээ санг
ашиглах бөгөөд анхны код нь түүний өгөгдлийг байнгын өөрчлөхгүй — `tur_`
хүснэгт үүсгээд устгах, эсвэл ROLLBACK хийнэ.

JavaScript сургалтын хөтчийн сэдэвтэй модулиуд (DOM, форм, хадгалалт, API) нь
sandbox дотор `document`, `localStorage`, `fetch` байхгүйг харгалзан анхны
кодондоо ижил хэлбэртэй загварыг өөрсдөө зарладаг — хичээлийн markdown дахь
жишээ нь жинхэнэ хөтөчид ажиллах бодит код.

HTML & CSS сургалтын хичээлийн `language` нь юуг заахаас шалтгаална: бүтцийн хичээлүүд `html`,
загварын хичээлүүд `css`. Хөтөч дотор ажиллуулах боломжгүй тул анхны код
нь суралцагч өөрийн файлдаа **хуулж шууд ашиглаж болох бүтэн жишээ**
байхаар бичигдсэн.

`tests/test_content.py` нь агуулга бүрийг шалгана: slug давхардаагүй,
хугацаа боломжтой, гарчиг давтагдаагүй, **Python-ийн анхны код бүр
синтаксийн хувьд зөв**, **JavaScript-ийн анхны код нь sandbox дотор
байхгүй global-уудыг зарлалгүй ашиглаагүй**, мөн **HTML-ийн шошго болон
CSS-ийн хаалт тэнцүү**, **C/C++ -ийн хаалт тэнцүү**, **shell-ийн
heredoc хаагдсан**, мөн **SQL-ийн хаалт, ишлэл тэнцүү бөгөөд анхны код нь
хичээлийн шошгосон аялгуунаас (MySQL / SQL Server) өөр бичиглэл
агуулаагүй** эсэх.

### Хэл бүрийн ажиллах чадвар

| Хэл | `LessonLanguage` | Syntax highlight | Хөтөч дотор ажиллах |
|---|---|---|---|
| JavaScript | `javascript` | Тийм | **Тийм** — Web Worker sandbox |
| React (JSX) | `jsx` | Тийм (`.jsx` model) | **Тийм** — sandbox iframe, «Хөтөч» + DOM тест |
| Python | `python` | Тийм | **Тийм** — Pyodide |
| HTML / CSS | `html`, `css` | Тийм | **Тийм** — sandbox iframe, шууд шинэчлэгдэх «Хөтөч» |
| C / C++ | `c`, `cpp` | Тийм | **Тийм** — серверт хөрвүүлж (Emscripten), Web Worker дотор |
| Терминал | `shell` | Тийм | Үгүй |
| MySQL / SQL Server | `mysql`, `sql` | Тийм | Үгүй — сервер дээрх өгөгдлийн сан шаардана |

`LessonLanguage`-ийн утга бүр нь **Monaco-ийн хэлний ID-тай яг таарна** —
`code-editor.tsx` нь утгыг шууд Monaco руу дамжуулдаг. Цорын ганц үл
хамаарах нь `jsx`: засварлагч үүнийг `javascript` болгож, файлын `.jsx`
замаар JSX-ийг таниулна. Шинэ утга нэмэхэд
дөрвөн газар засна: enum, `lessons.language`-ийн CHECK (migration),
frontend-ийн `LessonLanguage` төрөл, `languageLabels`. Энэ жагсаалтыг
`app/models/enums.py` дотор тайлбарласан бөгөөд `test_content.py` нь enum
ба Monaco ID-ийн жагсаалт зөрөхөөс сэргийлнэ.

Ажиллахгүй хэл дээр «Код ажиллуулах» товч идэвхгүй байх ба console хэсэгт
шалтгааныг монголоор тайлбарлана. Энэ нь эвдэрсэн төлөв биш — `CodePlayground`
дотор зориудаар зохицуулагдсан.

Python-ийг хөтөч дотор ажиллуулах бол **Pyodide** (CPython → WebAssembly) нь
одоо байгаа архитектурт тохирно: ижил Worker тусгаарлалтыг ашиглах бөгөөд
`runner.ts`-ийн интерфейс өөрчлөгдөхгүй. Зардал нь ~10 MB WASM татах явдал.

### Дасгал ба тест (C/C++, Python)

C/C++ болон Python хичээл бүр HackerRank маягийн дасгалтай. Хичээлийн `initial_code` нь
эхлэл код (араг), `lessons.exercise` (JSONB) нь даалгавар болон тестүүд:

```json
{ "statement": "Markdown", "tests": [{ "stdin": "…", "expected_output": "…", "sample": true }] }
```

| Товч | Юуг ажиллуулна | Харагдах зүйл |
|---|---|---|
| «Код ажиллуулах» | Сурагчийн «Оролт» (эхний жишээгээр бөглөгдсөн) | Терминал шиг гаралт, оролт давтагдана |
| «Тест ажиллуулах» | Зөвхөн `sample` тестүүд | Оролт / таны гаралт / хүлээгдэж буй гаралт, зөрсөн мөр |
| «Илгээх» | Бүх тест (нууцыг оролцуулан) | Нууц тестийн зөвхөн дүн. Бүгд давбал `POST /lessons/{id}/complete` |

**Шалгалт хөтөч дотор явагдана.** C/C++: код нэг удаа хөрвүүлэгдэж
(кэштэй), модуль тест бүрд шинэ worker-т `echoStdin: false` горимоор
ажиллана. Python: Pyodide-ийн worker хадгалагдана (ачаалалт удаан), тест
бүр `mode: "test"` горимоор ЦЭВЭР нэрийн талбарт (`__name__ == "__main__"`)
ажиллаж, `input()`-ийн асуулт гаралтад бичигдэхгүй — сурагч
`input("Нэр: ")` гэж бичсэнээр унах ёсгүй. Тест бүр мөн шинэ хоосон
хавтаст ажиллаж (өмнөх тестийн файл үлдэхгүй), `logging`-ийн тохиргоо
анхны төлөвтөө буцна (Pyodide нь `logging`-ийг өөрөө ачаалдаг тул
`basicConfig` өмнөх ажиллуулалтаас үлддэг байв). Оролтын төгсгөлийн «Enter»
илүү хоосон мөр болохгүй — `for line in sys.stdin` жинхэнэ CPython-той ижил. Python-ий stdout нь байт
хэлбэрээр уншигдаж, ажиллуулалт бүрийн төгсгөлд хоослогддог тул шинэ мөргүй
төгссөн гаралт (`print(x, end="")`) ч харагдана (өмнө нь алга болдог байв).
`grader.ts` нь зөвхөн stdout-ийг, мөрийн төгсгөлийн зай болон төгсгөлийн
хоосон мөрийг үл тоон харьцуулна. `main`-ийн буцаах код дүгнэлтэд орохгүй —
хичээлүүд буруу оролтод `return 1` хийхийг заадаг.

**Итгэлийн загвар.** Сервер сурагчийн кодыг ажиллуулдаггүй (§8) тул
`/complete` нь өмнөх шигээ client-ийн хүсэлтэд итгэнэ, нууц тестийн
хүлээгдэж буй гаралт ч хөтөч рүү очно. UI нь тэдгээрийг харуулахгүй ч
сүлжээний хүсэлтээс харж болно. Ахиц нь гэрчилгээ биш — хуурах сурагч
зөвхөн өөрийгөө хохироодог. Жинхэнэ нууц тест, серверийн баталгаа хэрэгтэй
болбол модулийг хөрвүүлэгчийн тусгаарлагдсан контейнер дотор WASI
runtime-аар ажиллуулж дүгнэх нь дараагийн алхам.

**«Тусламж».** Дасгал бүр зөвлөгөө (`tips`) болон тайлбартай жишиг
шийдэлтэй. Тэдгээр нь `lessons.exercise`-д хадгалагдах ч хичээлийн хариунд
ОРОХГҮЙ (`LessonExercise` схем нь зөвхөн даалгавар, тест). Сурагч «Тусламж»
дарахад «шууд хариу өгнө» гэсэн анхааруулга ГАРЧ, зөвшөөрсний дараа л
`GET /lessons/{id}/help` дуудагдана. «Дахиж анхааруулах хэрэггүй» сонголт
нь тухайн хөтөчийн `localStorage`-д (бүх хичээлд) хадгалагдана. Тусламж
харсан эсэх ахицад нөлөөлөхгүй.

`npm run verify:exercises` нь дасгал бүрийн шийдэл бүх тестийг давж, эхлэл
код давахгүйг жинхэнэ хөрвүүлэгч болон хөтөчийн worker-ийн ижил эх кодоор
шалгадаг — CI-ийн `e2e` job-д ажиллана.

### React хичээл (`jsx`)

React сургалтын засварлагч react-tutorial.app-ийн байршилтай
(`components/learn/react/`): зүүн талд файлууд tab-аар (`App.jsx`,
🔒 `main.jsx`, 🔒 `index.html`) ба «Тестүүд (x / n)», баруун талд «Заавар /
Хөтөч» tab ба Console. Нарийн дэлгэцэнд «Заавар / Код / Хөтөч». Хичээл
нээгдэхэд код автоматаар ажиллаж, «Ажиллуулах» (Ctrl + Enter) нь «Хөтөч»-ийг
дахин ачаалж, бүх тестийг зэрэг шалгана. Бүгд давбал хичээл дуусна.

**Олон файл нэг баганад.** `initial_code` нь `// @file App.jsx`,
`// @file main.jsx locked` мөрөөр файлуудад хуваагдана (`lib/sandbox/react/files.ts`)
— шинэ хүснэгт, багана шаардаагүй. Жишиг шийдэл мөн ийм хэлбэртэй, зөвхөн
өөрчлөгдсөн файлуудыг агуулна.

**Тусгаарлалт.** Код `sandbox="allow-scripts allow-forms"` iframe-ийн
`srcdoc` дотор ажиллана. `allow-same-origin` байхгүй тул iframe нь opaque
origin-той: MedlegHub-ийн cookie, `localStorage`, DOM-д хүрэхгүй, манай
API руу CORS-оос болж хүсэлт илгээж чадахгүй. `srcdoc` нь хуудасны CSP-ийг
өвлөнө — `connect-src 'self'` тул гадаад сүлжээ хаалттай. Хуудас ба iframe
зөвхөн `postMessage`-ээр харилцана; хуудас мессежийг тухайн iframe-ийн
`contentWindow`, тухайн ажиллуулалтын `runId`-аар шүүнэ.

**Runtime.** `lib/sandbox/react-runtime/` → `npm run sandbox:react`
(`predev`/`prebuild` өөрөө дууддаг) → `public/sandbox/react-runtime.js`
(~1.1 MB, gzip ~330 KB, git-д ордоггүй). React 19 **development** хувилбар
(`key` анхааруулга, тестийн `act`), react-router, TanStack Query, Sucrase
(JSX → JS), Acorn (синтакс шалгалт + давталтын хамгаалалт). Iframe нь
runtime-ийг URL-аар ачаалж хөтчийн кэшд хадгална; зарим хөтөч sandbox
iframe-д `'self'`-ийг зөвшөөрөхгүй бол текстийг нь `srcdoc` дотор оруулна.
Runtime нь `localStorage` (санах ойд), `alert`, дадлагын REST API
(`fetch("/api/products")`), `BrowserRouter` (санах ойн router + хаягийн мөр),
2 секундээс удаан гацсан давталтыг таслах зэргийг хангана.

**Тест.** `lessons.exercise.tests` нь `{ "name", "code", "sample" }` —
`name` нь шаардлага болж харагдана, `code` нь нуугдмал iframe-д тест бүрт
шинэ модулиудтай ажиллана. API нь Testing Library + Jest-тэй ижил нэртэй
(`render`, `screen.getByRole`, `user.click`, `expect(...).toHaveTextContent`),
алдааны мессеж монголоор. «Модул 13 — Тест»-д сурагч өөрөө `App.test.jsx`
бичиж (`vitest`, `@testing-library/*` импорт ажиллана), дасгал түүнийг зөв
болон зориуд эвдэрсэн component дээр ажиллуулж дүгнэнэ. Итгэлийн загвар
C/C++, Python-той ижил.

`npm run verify:react` нь React хичээл бүрийг Playwright Chromium дотор
(сайтын CSP-тэй хуудсанд, ижил `runner.ts`-ээр) шалгана: эхлэл код алдаагүй
render хийгдэнэ, жишиг шийдэл бүх тестийг давна, эхлэл код давахгүй.

### HTML & CSS хичээл (`html`, `css`)

React-ийн байршилтай (`components/learn/html/`): зүүн талд файлууд tab-аар,
баруун талд «Заавар / Хөтөч». «Ажиллуулах» товчгүй — «Хөтөч» код бичих зуур
өөрөө шинэчлэгдэнэ (HTML засвар 400 мс-ийн дараа дахин ачаална, гүйлгэсэн
байрлал хадгалагдана; CSS засвар `<style>`-ийг `postMessage`-ээр шууд
сольно). Тест, шалгагч байхгүй — «Хичээл дууссан» товчоор дуусна.

**Файлууд.** `initial_code` нь React-ийн `// @file` хэлбэр (`files.ts`,
API талд `app/content/html_css/common.py`). Тэмдэггүй код нь `index.html`
(HTML хичээл) эсвэл `style.css` (CSS хичээл). CSS хичээл бүр `index.html` +
`style.css` (`css_page()`); `tests/test_content.py` нь `index.html` нь
`style.css`-ийг холбож, загварын бүх класс, id-г агуулахыг шалгана.

**Хөтөч** (`lib/sandbox/html/preview.ts`). Хуудас нь
`sandbox="allow-scripts allow-forms"` iframe-ийн `srcdoc` — React-тай ижил
тусгаарлалт (`allow-same-origin` үгүй, хуудасны CSP-г өвлөнө).
`<link rel="stylesheet">` нь хичээлийн CSS файлыг `<style>` болгон оруулна;
холбоогүй бол CSS нөлөөлөхгүй (жинхэнэ хөтөч шиг). `srcdoc`-ийн үндсэн хаяг
нь MedlegHub-ийн хуудас тул iframe дотор оруулсан жижиг script холбоос,
формыг барина: `#id` хуудас дотроо гүйлгэнэ, `tuhai.html` тэр файлыг
нээнэ (буцах/урагшлах, хаягийн мөр), гадаад / байхгүй / `mailto:`
холбоос, форм илгээлт, `alert()` нь «Хөтөч»-ийн доод талд мэдэгдэл болно.
Утас (375px) / таблет (768px) өргөн, одоогийн өргөн пикселээр — хариуцлагатай
дизайны хичээлд.

## 13. Тэмдэг (badges)

Тэмдэг бүрийн нэр, нөхцөл, хэлбэр `app/content/badges.py`-д, олгох логик
`app/services/badge_service.py`-д. Олгосон тэмдэг `user_badges`-д хадгалагдаж
**хэзээ ч хасагдахгүй** — агуулга өөрчлөгдсөн, ахиц устсан ч хэрэглэгч
алдахгүй.

- **Хэзээ олгох вэ.** Хичээл дуусгах бүрд (`POST /lessons/{id}/complete`
  хариуны `new_badges` → UI «Шинэ тэмдэг» мэдэгдэл) ба профайл нээхэд
  (`GET /me/profile` — энэ системээс өмнөх ахицыг гүйцээж олгоно). Зэрэг
  ирсэн хүсэлт `ON CONFLICT DO NOTHING`-оор давхардахгүй.
- **Юуг тоолох вэ.** Зөвхөн нийтлэгдсэн сургалтын нийтлэгдсэн хичээл. Цагийн
  нөхцөл (Night Owl, Early Bird) нь Улаанбаатарын цагаар (UTC+8, зуны цаггүй).
- **«Тун удахгүй».** `tracked=False` тэмдгүүдэд шаардлагатай өгөгдлийг
  (илгээлтийн оролдлого, тусламж ашигласан эсэх, зарцуулсан хугацаа, кодын
  чанар, нийгэмлэг) одоогоор бүртгэдэггүй. Өгөгдлийг нь бүртгэж эхлээд
  `RULES`-д нөхцөл нэмэхэд л идэвхжинэ.
- **Дүрс.** `apps/web/public/badges/<түлхүүр>.svg|png|webp` — build хийх
  үед `scripts/generate-badge-manifest.mjs` бүртгэнэ. Файлгүй тэмдэг
  хэлбэрээрээ (дугуй, бамбай, зургаан өнцөгт) хоосон харагдана.
- **Ховор байдал.** Тэмдэг бүр `earned_percent` — «Нийт хэрэглэгчдийн X% нь
  авсан». Имэйлээ баталгаажуулсан, профайлаа нуугаагүй суралцагчдаас тооцно
  (админ, нуусан профайл орохгүй — Нууцлалын бодлого §4.1). Профайл нээх бүрд
  хоёр aggregate query; хэрэглэгч ихсэвэл богино хугацаагаар кэшлэнэ.
- **Онцлох амжилт.** Эзэн авсан тэмдгүүдээсээ 5 хүртэлхийг сонгож
  (`PUT /me/showcase`) нэрийнхээ хажууд харуулна —
  `user_badges.showcase_position`. Дээд тоо `app.models.badge.SHOWCASE_MAX`,
  DB-ийн CHECK ба вэбийн `BADGE_SHOWCASE_MAX`-тай хамт өөрчилнө.
