# syntax=docker/dockerfile:1

# Жижиг Debian суурь. PDFium нь pypdfium2-ийн wheel дотор ирдэг тул системийн
# сан нэмж суулгахгүй. Шинэчлэхдээ `test` target-ийг ажиллуулна.
FROM python:3.13-slim AS runtime

ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY extractor ./extractor
RUN python -m compileall -q extractor

RUN useradd --system --uid 10003 --no-create-home --shell /usr/sbin/nologin extractor

# ЗААВАЛ: контейнерийг read-only root filesystem-тэй, /tmp-г tmpfs болгож
# ажиллуулна (`docker run --read-only --tmpfs /tmp`, compose-д `read_only: true`).
# Хүсэлтийн түр файл зөвхөн /tmp-д бичигдэнэ. Нууц мэдээлэл ЭНД БҮҮ ӨГ —
# итгэж болохгүй файл энэ контейнерт задарна.
ENV PYTHONDONTWRITEBYTECODE=1 \
    HOME=/tmp \
    EXTRACTOR_WORK_DIR=/tmp

USER extractor
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health', timeout=2)"]

CMD ["python", "-m", "uvicorn", "extractor.main:app", "--host", "0.0.0.0", "--port", "8080", "--no-server-header", "--no-access-log"]


# --- Тест ---------------------------------------------------------------------
#   docker build --target test -t medleghub-extractor-test apps/extractor
#   docker run --rm --read-only --tmpfs /tmp:size=256m,mode=1777 medleghub-extractor-test
FROM runtime AS test

USER root
COPY requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt
COPY pyproject.toml ./
COPY tests ./tests
USER extractor

CMD ["python", "-m", "pytest", "-q", "-p", "no:cacheprovider"]
