# syntax=docker/dockerfile:1

# Emscripten-ийн хувилбарыг ТОГТООНО. Шинэчлэхдээ `test` target-ийг ажиллуулж
# хөтөчийн worker хангадаггүй импорт нэмэгдээгүйг шалгана.
FROM emscripten/emsdk:6.0.9 AS runtime

ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Ubuntu 24.04-ийн Python нь «externally managed». Энэ image нь ганц
# зориулалттай тул системийн сан руу шууд суулгана.
COPY requirements.txt ./
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

COPY compiler ./compiler

# Emscripten-ийн кэш, туслах объект, PCH, Python bytecode-ийг бэлдэж, жишээ
# програмуудыг runtime-тай ижил замаар хөрвүүлж шалгана. Амжилтгүй бол build
# зогсоно. PYTHONDONTWRITEBYTECODE-г ЗОРИУД дараа нь тавьсан: bytecode энд
# бичигдэхгүй бол emcc дуудлага бүр Python эх кодоо дахин задална.
RUN python3 -m compiler.prewarm

RUN useradd --system --uid 10001 --no-create-home --shell /usr/sbin/nologin compiler

# АНХААР: upstream emsdk image нь хөрвүүлэгч болон кэшийг хэн ч бичих эрхтэй
# (777) ирүүлдэг. Контейнерийг ЗААВАЛ read-only root filesystem-тэй
# ажиллуулна (`docker run --read-only --tmpfs /tmp`, compose-д
# `read_only: true`). Эс бөгөөс эвдэрсэн хөрвүүлэлт дараагийн сурагчдын
# хөрвүүлэгчийг өөрчилж чадна. Үйлчилгээ эхлэхдээ үүнийг шалгаж анхааруулна.
#
# Runtime-д кэш зөвхөн уншигдана. Sanity check нь кэшид бичдэг тул алгасна.
ENV EM_FROZEN_CACHE=1 \
    EMCC_SKIP_SANITY_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    HOME=/tmp \
    COMPILER_WORK_DIR=/tmp

USER compiler
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s \
    CMD ["python3", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health', timeout=2)"]

CMD ["python3", "-m", "uvicorn", "compiler.main:app", "--host", "0.0.0.0", "--port", "8080", "--no-server-header", "--no-access-log"]


# --- Тест ---------------------------------------------------------------------
#   docker build --target test -t medleghub-compiler-test apps/compiler
#   docker run --rm --read-only --tmpfs /tmp medleghub-compiler-test
FROM runtime AS test

USER root
COPY requirements-dev.txt ./
RUN pip3 install --no-cache-dir --break-system-packages -r requirements-dev.txt
COPY pyproject.toml ./
COPY tests ./tests
USER compiler

CMD ["python3", "-m", "pytest", "-q", "-p", "no:cacheprovider"]
