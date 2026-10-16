# Medleghub

Монгол хэл дээрх интерактив програмчлалын сургалтын платформ
([medleghub.com](https://medleghub.com)). Хэрэглэгч хичээл уншиж, кодоо хөтөч
дотор бичиж, ажиллуулж, автомат тестээр шалгуулна.

Архитектур, аюулгүй байдлын шийдвэрүүд:
[`apps/web/docs/ARCHITECTURE.md`](apps/web/docs/ARCHITECTURE.md).

## Бүтэц

```
apps/api         FastAPI + SQLAlchemy + PostgreSQL (alembic migration, seed, сургалтын агуулга)
apps/web         Next.js 16 + TypeScript + Tailwind; production-д Cloudflare Workers (OpenNext)
apps/compiler    C/C++ хөрвүүлэгч — Emscripten → WebAssembly, тусдаа контейнер
apps/sql-runner  MySQL 8.4 sandbox, тусдаа контейнер
apps/extractor   Medleghub Live-ийн файл задлагч (PDF, PPTX, DOCX → текст), тусдаа контейнер
```

Сургалтын агуулга бүхэлдээ кодонд байна: `apps/api/app/content/`. Seed нь
өгөгдлийн санг түүнтэй тэнцүү болгоно.

## Шаардлага

| Хэрэгсэл | Хувилбар |
|---|---|
| Node.js | 20+ |
| Python | 3.11+ |
| Docker | PostgreSQL, хөрвүүлэгч, MySQL sandbox, файл задлагчид |

## Локал дээр ажиллуулах

### 1. Өгөгдлийн сан ба контейнерүүд

```bash
docker compose up -d
```

| Үйлчилгээ | Хаяг | Тайлбар |
|---|---|---|
| PostgreSQL 16 | `localhost:5432` | `suralts / suralts / suralts` (хэрэглэгч / нууц үг / DB) |
| C/C++ хөрвүүлэгч | `127.0.0.1:8090` | Анхны build удаан: Emscripten image (3.4 GB) |
| MySQL sandbox | `127.0.0.1:8091` | Анхны build ~2 мин |
| Файл задлагч | `127.0.0.1:8092` | Зөвхөн Medleghub Live-д |

C/C++, SQL хичээл дээр ажиллахгүй бол зөвхөн өгөгдлийн санг асааж болно:
`docker compose up -d db`.

### 2. Backend

```bash
cd apps/api
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
cp .env.example .env
alembic upgrade head
python -m app.seed                 # сургалтууд ба жишээ хэрэглэгчид
uvicorn app.main:app --reload --port 8000
```

API: http://localhost:8000 · Swagger: http://localhost:8000/docs ·
Health: http://localhost:8000/health

### 3. Frontend

```bash
cd apps/web
npm install
cp .env.example .env.local
npm run dev
```

Сайт: http://localhost:3000

### Жишээ хэрэглэгчид

| Үүрэг | Имэйл | Нууц үг |
|---|---|---|
| Админ | `admin@suralts.mn` | `Admin12345` |
| Сурагч | `suragch@suralts.mn` | `Suragch12345` |
| Standard багцтай сурагч | `standard@suralts.mn` | `Standard12345` |

Зөвхөн хөгжүүлэлтэд. Production дээр `SEED_ADMIN_*` заавал өгнө (анхдагч нууц
үгийг seed татгалзана).

Локалд `SUPABASE_URL` хоосон бол бүртгүүлэхэд код асуухгүй, шууд нэвтэрнэ.
`WIRE_SECRET_KEY` хоосон бол төлбөр 503 буцаана. Medleghub Live-ийг AI
түлхүүргүй турших бол `apps/api/.env`-д `LIVE_ACCESS=all`, `AI_MODELS=fake:local`.

## Тушаалууд

### Backend (`apps/api`)

| Тушаал | Үүрэг |
|---|---|
| `alembic revision --autogenerate -m "..."` | Шинэ migration |
| `alembic upgrade head` | Migration хэрэглэх |
| `python -m app.seed` | Агуулгыг `app/content/`-той тэнцүү болгох (ахиц хэвээр) |
| `python -m app.seed --reset` | Бүгдийг устгаад шинээр үүсгэх (зөвхөн локалд) |
| `ruff check app tests` · `ruff format app tests` | Lint · format |
| `pytest` | Тест |
| `python -m app.content.verify_sql_cases` | SQL мөрдөгчийн хэргүүдийн хариултыг sandbox дээр шалгах |

### Контейнерүүд (`apps/compiler`, `apps/sql-runner`, `apps/extractor`)

Тус бүр ижил хэлбэртэй (`<pkg>` = `compiler`, `sqlrunner`, `extractor`):

| Тушаал | Үүрэг |
|---|---|
| `docker compose up -d --build <үйлчилгээ>` | Бүтээж асаах (repo-ийн үндсэн хавтаснаас) |
| `ruff check <pkg> tests` | Lint |
| `pytest` | Docker шаардахгүй тестүүд |
| `docker build --target test -t <нэр>-test .` | Бүх тесттэй image |
| `docker run --rm --read-only --tmpfs /tmp <нэр>-test` | Production шиг зөвхөн уншигдах файлын системтэй тест (sql-runner: `--tmpfs /tmp:size=2g`) |

### Frontend (`apps/web`)

| Тушаал | Үүрэг |
|---|---|
| `npm run dev` · `npm run build` · `npm run start` | Dev server · production build · production server |
| `npm run lint` · `npm run typecheck` · `npm run format` | ESLint · TypeScript · Prettier |
| `npm run test:unit` · `npm run test:worker` | Node-ийн unit тест (Flowgorithm, React sandbox, Worker) |
| `npm run verify:exercises` | C/C++, Python, JavaScript дасгал бүрийн жишиг шийдэл тестийг давж, эхлэл код давахгүйг шалгана |
| `npm run verify:react` | React хичээл бүрийг хөтөч дотор шалгана |
| `npm run e2e` | Бүх E2E тест (Playwright) |
| `npm run e2e:<нэр>` | Нэг spec — `package.json`-ийг үз |
| `npm run cf:build` · `npm run cf:preview` · `npm run cf:deploy` | Cloudflare Workers-д build · локал preview · байршуулах |

**E2E.** Хөрвүүлэгч, SQL sandbox, backend, frontend асаалттай, өгөгдлийн сан
seed хийгдсэн байх ёстой. Тестүүд seed-ийн хэрэглэгч, сургалтууд дээр
тулгуурлаж, шинэ өгөгдөл үүсгээд цэвэрлэдэггүй — дараа нь
`python -m app.seed --reset`. Локал API нэг IP-ээс минутад 10 нэвтрэлт
зөвшөөрдөг тул бүтэн ажиллагаанд API-г `RATE_LIMIT_ENABLED=false`-оор асаа.
`npm run e2e:live` нь `LIVE_ACCESS=all`, `AI_MODELS=fake:local` болон файл
задлагч шаардана.

### CI

[`.github/workflows/ci.yml`](.github/workflows/ci.yml): API (ruff, migration,
pytest), хөрвүүлэгч ба SQL sandbox (Docker image дотор бүх тест), web (ESLint,
TypeScript, Prettier, build, `npm audit`), e2e (production build дээр
Playwright). [`images.yml`](.github/workflows/images.yml) нь `main`, `test`
салбарт backend-ийн image-уудыг `ghcr.io/<repo-ийн эзэн>/medleghub-*` руу
түлхэнэ.

## Сургалтууд

| Сургалт | Модул | Хичээл | Код хаана ажиллах |
|---|---|---|---|
| Flowgorithm — програмчлалын анхны алхам | 8 | 24 | Хөтөч — сайт доторх блок схем |
| JavaScript үндэс | 26 | 71 | Хөтөч — Web Worker (`prompt()`-оор оролт) |
| Python Программчлал | 29 | 44 | Хөтөч — Pyodide |
| HTML & CSS үндэс | 20 | 54 | Хөтөч — шууд шинэчлэгдэх preview |
| C ба C++ үндэс | 21 | 52 | Серверт хөрвүүлж, хөтөчид WebAssembly-ээр |
| Git ба GitHub | 18 | 39 | Үгүй — терминалын тушаал |
| Өгөгдлийн Сангийн Үндэс (MySQL) | 22 | 87 | Серверийн MySQL sandbox; 23 мөрдөгчийн хэрэг |
| React-ээр апп бүтээх | 15 | 111 | Хөтөч доторх sandbox iframe |

**Хичээл нэмэх.** Тухайн модулын файлд `LessonSpec` нэмээд `python -m app.seed`.
Seed нь хичээлийг `slug`-аар тааруулдаг тул суралцагчийн ахиц алдагдахгүй;
`app/content`-оос хассан хичээлийг ахицтай нь устгана. Дасгал бүр оролт уншиж,
дор хаяж 4 тесттэй (нэг нь нууц), 2-оос олон өөр гаралттай байна
(`tests/test_content.py`). Хичээл зөвхөн өмнө заасан синтакс ашиглана
(`tests/test_concept_order.py`).

**Тэмдэг (badges).** Нөхцөл, нэр нь `apps/api/app/content/badges.py`-д. Дүрсийг
тэмдгийн түлхүүрээр нэрлээд `apps/web/public/badges/`-д хийнэ (SVG, PNG, WebP);
`npm run dev`/`build` өөрөө бүртгэнэ.

**Лого.** Ангиллын түлхүүрээр нэрлэсэн файлыг `apps/web/public/logos/`-д хийнэ —
[`README`](apps/web/public/logos/README.md)-ийг үз.

## Аюулгүй байдал

Хэрэглэгчийн JavaScript, Python, C/C++ код **зөвхөн хөтчийн Web Worker sandbox**
дотор ажиллана: сүлжээний API, DOM, cookie, localStorage байхгүй, 3 секундын
дараа албадан зогсоно. Python-д Pyodide ачаалж дууссаны дараа сүлжээний API
устгагдана (`e2e/python-sandbox.spec.mjs` шалгадаг).

C/C++-ийн эх код зөвхөн хөрвүүлэгдэхээр API-д ирж, **ажиллуулагдахгүй,
хадгалагдахгүй**. Хөрвүүлэгч контейнер нь нууцгүй, өгөгдлийн сангүй,
сүлжээгүй, зөвхөн уншигдах файлын системтэй, эрхгүй хэрэглэгчээр,
хугацаа/санах ой/процессын хязгаартай ажиллана. Upstream Emscripten image нь
хөрвүүлэгчийг хэн ч бичих эрхтэй ирүүлдэг тул **заавал** `read_only`-оор
ажиллуул — эс бөгөөс нэг сурагчийн хөрвүүлэлт дараагийнхных нь хөрвүүлэгчийг
өөрчилж чадна.

MySQL код серверт ажиллана, гэхдээ API-ийн сантай холбоогүй, сүлжээгүй, нууцгүй
тусдаа контейнерт, `SYSTEM_USER`/`FILE`/`SUPER` эрхгүй данстай, ажиллагаа
бүрийн дараа цэвэрлэгддэг MySQL дээр.

Бусад нь (нууц үгийн hash, httpOnly cookie доторх JWT, эрхийн хяналт, хүсэлтийн
хязгаар, CSP) — `ARCHITECTURE.md` §8.

## Байршуулах (self-host)

medleghub.com ийм бүтэцтэй ажилладаг байсан:

```
хөтөч ──► <домэйн> (Cloudflare Worker, apps/web)
            │  /api/v1/* → API_PROXY_TARGET (build-ийн үед тогтоно)
            ▼
         api.<домэйн> (DNS only) ──► VM: Caddy :443 ──► api :8000
                                                     ├─► compiler   (дотоод сүлжээ, интернэтгүй)
                                                     ├─► sql-runner (дотоод сүлжээ, интернэтгүй)
                                                     ├─► extractor  (Live; дотоод сүлжээ, интернэтгүй)
                                                     └─► PostgreSQL (Supabase эсвэл өөр)
```

### 1. Өгөгдлийн сан ба Supabase Auth

Ямар ч PostgreSQL 16 болно. `DATABASE_URL` =
`postgresql+asyncpg://хэрэглэгч:нууц@хост:5432/сан?ssl=require` (нууц үг дэх `$`
нь `%24` болно). API контейнер эхлэхдээ `alembic upgrade head` ажиллуулна.
Supabase ашиглавал IPv4-тэй **session pooler**-ийн хаягийг ав (direct host
нь зөвхөн IPv6), Data API-г унтраа. Шинэ хүснэгтийн migration бүр
`ENABLE ROW LEVEL SECURITY` хийнэ.

Бүртгэл баталгаажуулах, нууц үг сэргээх, имэйл солих нэг удаагийн кодыг
**Supabase Auth** илгээдэг (`apps/api/app/services/email_otp.py`); нэвтрэлт,
бүртгэл Medleghub-ийн API-д үлдэнэ. Production дээр `SUPABASE_URL`,
`SUPABASE_ANON_KEY`-гүй бол API эхлэхгүй.

- **Authentication → Email Templates:** «Confirm signup» ба «Magic Link» хоёуланд
  нь ижил загвар тавина. Загварт холбоос биш, зөвхөн `{{ .Token }}` код байна
  (`ConfirmationURL`-ийг API ашигладаггүй).
- **Sign In / Providers → Email:** provider асаалттай, шинэ хэрэглэгч бүртгэхийг
  зөвшөөрнө, OTP expiration **600** секунд (имэйлд «10 минут» гэж бичнэ), OTP
  урт **6**.
- **Rate Limits:** имэйл илгээх хязгаарыг нэмнэ. Supabase бүх хүсэлтийг API
  серверийн нэг IP-ээс хардаг; API өөрөө имэйл бүрт хязгаар тавьдаг.
- **API Keys:** `SUPABASE_URL`, `SUPABASE_ANON_KEY` (publishable),
  `SUPABASE_SERVICE_ROLE_KEY` (secret; бүртгэл устахад Supabase Auth-ийн
  бичлэгийг устгахад л хэрэглэнэ, хөтөчид хэзээ ч бүү өг).

### 2. Backend VM

1. x86-64 Ubuntu + Docker compose. Зөвхөн 22, 80, 443 портыг нээнэ.
   1 vCPU / 2 GB хангалттай (`.env.prod`-д `COMPILER_MAX_CONCURRENCY=1`,
   `COMPILER_CPUS=1`, `SQLRUNNER_SLOTS=2`, мөн 1 GB swap).
2. `docker-compose.prod.yml`, `Caddyfile`, `.env.prod.example`-ийг серверт хуулна.
   Image-уудыг fork-ийнхоо `images.yml`-ээр бүтээгээд `docker-compose.prod.yml`
   дахь `ghcr.io/orgilsaikhan/...`-ийг өөрийнхөөрөө солино (эсвэл серверт
   `docker build`). Хувийн GHCR багц бол `read:packages` эрхтэй PAT-аар
   `docker login ghcr.io`.
3. `.env.prod.example`-ийг `.env.prod` болгож бөглөнө: `API_HOST`, `ACME_EMAIL`,
   `CORS_ORIGINS`, `DATABASE_URL`, `JWT_SECRET` (32+ тэмдэгт), `SUPABASE_*`,
   `CLIENT_IP_SECRET` (32+ тэмдэгт, Worker-ийнхтэй ижил), `IMAGE_TAG`, `SITE_URL`.
   Файл доторх тайлбар хувьсагч бүрийг тайлбарласан.
4. `api.<домэйн>`-ийн `A` бичлэгийг серверийн IP руу **DNS only** (саарал үүл)
   заана — Caddy өөрөө Let's Encrypt сертификат авна.
5. Асаах, дараа нь seed:

   ```bash
   docker compose -f docker-compose.prod.yml --env-file .env.prod pull
   docker compose -f docker-compose.prod.yml --env-file .env.prod up -d
   docker compose -f docker-compose.prod.yml --env-file .env.prod exec \
     -e SEED_ADMIN_EMAIL=you@example.com -e SEED_ADMIN_PASSWORD='…' api python -m app.seed
   ```

   `pull` + `up -d` нь migration хийдэг ч шинэ хичээлийг seed хийдэггүй —
   агуулга өөрчлөгдөх бүрд seed-ийг дахин ажиллуул. Production-д `--reset`
   хэзээ ч бүү хэрэглэ. SQL хэргүүдийн `medleg_hot` сантай sql-runner seed-ээс
   өмнө асаалттай байна.

### 3. Вэб (Cloudflare Workers)

1. Өөрийн домэйноор солино:
   - `apps/web/wrangler.jsonc` — `name`, `services[].service`,
     `vars.API_INTERNAL_URL`, `routes`;
   - `apps/web/scripts/cloudflare-build.mjs` — `NEXT_PUBLIC_SITE_URL`,
     `API_PROXY_TARGET` (эсвэл shell-ээс орчны хувьсагчаар өгнө).
2. `npx wrangler secret put CLIENT_IP_SECRET` — `.env.prod`-ийнхтэй ижил утга.
3. `cd apps/web && npm run cf:deploy`. `git push` вэбийг шинэчлэхгүй, байршуулах
   бүрд энэ тушаал.

Нэг хуудас үзэлт prefetch-тэйгээ 8–14 Worker хүсэлт болдог; Workers Free-ийн
өдрийн хязгаарт хүрвэл Workers Paid руу шилж.

### 4. Нэмэлт боломжууд (заавал биш)

- **Төлбөр (Wire / QPay).** `WIRE_SECRET_KEY`, `WIRE_WEBHOOK_SECRET`,
  `SITE_URL`. `Caddyfile` webhook-ийг зөвхөн Wire-ийн IP-ээс хүлээн авдаг
  (TCP хаягаар шалгадаг тул `api.<домэйн>` DNS only байх ёстой). Хоосон бол
  төлбөр унтраалттай.
- **Medleghub Live** (материал оруулаад AI-аар заалгах). `LIVE_ACCESS=all`,
  `OPENROUTER_API_KEY` эсвэл `GEMINI_API_KEY`, хувийн R2 bucket-ийн `LIVE_R2_*`,
  `extractor` контейнер. AI зардлын хязгаар `.env.prod.example`-д. Анхдагчаар
  унтраалттай (`LIVE_ACCESS=off`).

### 5. Medleghub-д тусгайлан бичигдсэн зүйлс

Өөрийн сайт болгохдоо эдгээрийг солино:

| Хаана | Юу |
|---|---|
| `apps/web/src/content/legal/` | Нууцлалын бодлого, Үйлчилгээний нөхцөл — Medleghub-ийн баримт бичиг. Өөрийнхөөрөө солино. |
| `apps/web/public/main_logo.png`, `badges/`, `videos/`; `apps/web/src/app/favicon.ico` | Medleghub-ийн лого, тэмдгийн зураг, демо видео — лицензээр нээгдээгүй (доорх «Лиценз»). Өөрийнхөөрөө солино. |
| `apps/web/src/lib/seo.ts` | `SITE_URL`, `CONTACT_EMAIL`, `FACEBOOK_URL` |
| `apps/web/src/components/layout/site-footer.tsx` | Холбоо барих имэйл, утас |
| `apps/web/src/lib/i18n/mn.ts` | Төлбөрийн алдааны мессеж дэх имэйл |
| `apps/web/src/components/layout/chat-widget.tsx` | Flux-Core чатбот — зөвхөн `SITE_URL`-ийн хост дээр ачаалагдана; хэрэггүй бол хас (CSP нь `next.config.ts`-д) |
| `apps/web/public/og.png`, `scripts/generate-og-image.mjs`, `scripts/indexnow.mjs` | Домэйн, OG зураг |
| `apps/api/app/content/promo_codes.py` | Seed-ийн нэмдэг промо код |

### Анхаарах зүйлс

- `apps/web/open-next.config.ts`-ийн `enableCacheInterception`-ийг **хэзээ ч
  асааж болохгүй** — Next 16.3-ийн `prefetchInlining`-тэй хамт эцэсгүй prefetch
  давталт үүсгэж, Worker-ийн хязгаарыг дуусгадаг.
- API-д ирсэн `X-Forwarded-For`/`X-Real-IP`-д итгэхгүй. Зочны IP-г Worker
  гарын үсэгтэй `X-MedlegHub-Client-IP` толгойгоор дамжуулдаг
  (`apps/web/worker/client-ip.mjs`, `apps/api/app/core/rate_limit.py`).
  Cloudflare-ийн IP-г Caddy-ийн `trusted_proxies`-д **бүү нэм** — бусад
  Cloudflare хэрэглэгчийн Worker толгойг хуурамчаар бичиж чадна.
- `wrangler dev`-ийг `cf:build`-ийн дараа шууд ажиллуулбал `/privacy`, `/terms`
  500 өгнө — `npm run cf:preview` ашигла.
- Cloudflare-ийн proxy ~100 секундэд тасардаг тул удаан ажлыг background job
  болго.

## Лиценз

| Юу | Лиценз |
|---|---|
| Код — доор дурдаагүй бүх файл | [AGPL-3.0-or-later](LICENSE) |
| Сургалтын агуулга — `apps/api/app/content/` доторх сургалт бүрийн хавтас (`c_cpp`, `flowgorithm`, `git_github`, `html_css`, `javascript`, `python`, `react`, `sql`), `apps/sql-runner/sandbox/*.sql` | [CC BY-SA 4.0](LICENSES/CC-BY-SA-4.0.txt) |
| Medleghub нэр, лого, favicon, OG зураг, тэмдгийн зураг, демо видео | Бүх эрх хуулиар хамгаалагдсан ([тайлбар](LICENSES/LicenseRef-Medleghub-Reserved.txt)) |
| Нууцлалын бодлого, Үйлчилгээний нөхцөл (`apps/web/src/content/legal/`) | Бүх эрх хуулиар хамгаалагдсан |
| `apps/web/public/logos/` дахь технологийн лого | Эзэмшигчдийнх ([тайлбар](LICENSES/LicenseRef-Third-Party-Logos.txt)) |

Файл бүрийн яг лицензийг [`REUSE.toml`](REUSE.toml) заана; `pipx run reuse lint`
шалгана.

- **AGPL-3.0:** өөрчилсөн хувилбарыг сервер дээр ажиллуулж бусдад үйлчилбэл
  түүний эх кодыг тэдгээр хэрэглэгчдэд нээлттэй болгоно.
- **CC BY-SA 4.0:** хичээлийг ашиглах, өөрчлөхдөө «Medleghub»-ийг эх сурвалж
  гэж дурдаж, өөрчилсөн хувилбараа мөн CC BY-SA 4.0-оор түгээнэ.
- Өөрийн сайт ажиллуулбал Medleghub-ийн нэр, лого, брэндийн файл, хууль эрх
  зүйн баримт бичгийг өөрийнхөөрөө солино («Medleghub-д тусгайлан бичигдсэн
  зүйлс»-ийг үз).
