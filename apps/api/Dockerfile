# syntax=docker/dockerfile:1

# --- Build -------------------------------------------------------------------
# asyncpg, bcrypt зэрэг нь ARM дээр бэлэн wheel байхгүй бол эх кодоос
# хөрвүүлэгддэг. Хөрвүүлэгчийг ЗӨВХӨН энд суулгаж, runtime image-ыг цэвэр
# үлдээнэ.
FROM python:3.13-slim AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /build
COPY pyproject.toml ./
COPY app ./app
RUN pip install .


# --- Runtime -----------------------------------------------------------------
FROM python:3.13-slim AS runtime

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH"

COPY --from=builder /opt/venv /opt/venv

WORKDIR /app
# Миграц нь runtime-д ажилладаг тул alembic-ийг ЗААВАЛ хамт хуулна.
COPY alembic.ini ./
COPY alembic ./alembic
COPY app ./app
COPY docker-entrypoint.sh ./docker-entrypoint.sh

RUN useradd --system --uid 10002 --no-create-home --shell /usr/sbin/nologin api
USER api

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=30s \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)"]

# `sh`-ээр шууд дуудна — Windows дээр git нь exec bit-ийг хадгалдаггүй.
ENTRYPOINT ["sh", "./docker-entrypoint.sh"]
CMD ["python", "-m", "uvicorn", "app.main:app", \
     "--host", "0.0.0.0", "--port", "8000", \
     "--proxy-headers", "--forwarded-allow-ips", "*", \
     "--no-server-header"]
