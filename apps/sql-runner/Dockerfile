# syntax=docker/dockerfile:1

# MySQL-ийн хувилбарыг ТОГТООНО. Шинэчлэхдээ `test` target-ийг ажиллуулж
# сурагчийн эрхийн хязгаарлалт хэвээр эсэхийг шалгана (`tests/test_sandbox.py`).
# Oracle Linux 9 суурьтай, `arm64` хувилбартай — Oracle Ampere VM дээр эмуляцигүй.
FROM mysql:8.4.11 AS runtime

ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN microdnf -y install python3.12 python3.12-pip \
    && microdnf clean all

WORKDIR /app

COPY requirements.txt ./
RUN python3.12 -m pip install --no-cache-dir -r requirements.txt

COPY sqlrunner ./sqlrunner
COPY sandbox ./sandbox
RUN python3.12 -m compileall -q sqlrunner \
    && mkdir -p build \
    && chown mysql:mysql build

ENV SQLRUNNER_TEMPLATE_DIR=/app/build/template \
    SQLRUNNER_WORK_DIR=/tmp

# Upstream-ийн entrypoint нь root-оор эхэлж `/var/lib/mysql`-д сервер
# бэлддэг — энд хэрэггүй. Бүх зүйл `mysql` хэрэглэгчээр, root-гүй ажиллана.
USER mysql

# Цэвэр datadir загвар: хоосон сервер + `student` данс + жишээ сангууд.
# Амжилтгүй бол build зогсоно. Runtime-д slot бүр үүнийг /tmp руу хуулна.
RUN python3.12 -m sqlrunner.prewarm

# ЗААВАЛ: контейнерийг read-only root filesystem-тэй, /tmp-г tmpfs болгож
# ажиллуулна (`docker run --read-only --tmpfs /tmp`, compose-д `read_only: true`).
# Datadir бүхэлдээ /tmp-д байх тул tmpfs-ийн хэмжээ = slot × ~400 MB.
ENV PYTHONDONTWRITEBYTECODE=1

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=60s \
    CMD ["python3.12", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health', timeout=2)"]

ENTRYPOINT []
CMD ["python3.12", "-m", "uvicorn", "sqlrunner.main:app", "--host", "0.0.0.0", "--port", "8080", "--no-server-header", "--no-access-log"]


# --- Тест ---------------------------------------------------------------------
#   docker build --target test -t medleghub-sql-runner-test apps/sql-runner
#   docker run --rm --read-only --tmpfs /tmp:size=2g medleghub-sql-runner-test
FROM runtime AS test

USER root
COPY requirements-dev.txt ./
RUN python3.12 -m pip install --no-cache-dir -r requirements-dev.txt
COPY pyproject.toml ./
COPY tests ./tests
USER mysql

CMD ["python3.12", "-m", "pytest", "-q", "-p", "no:cacheprovider"]
