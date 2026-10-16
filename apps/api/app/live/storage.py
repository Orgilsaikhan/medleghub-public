"""Эх файлын сан — Cloudflare R2-ийн хувийн bucket эсвэл (dev, тест) локал хавтас.

Файл хэзээ ч нийтэд ил URL-гүй: зөвхөн API уншина. Түлхүүр нь санамсаргүй
(`materials/<uuid>/original`), хэрэглэгчийн файлын нэрээс гаргахгүй.

R2 нь S3-тай нийцтэй тул хүсэлтийг AWS Signature V4-өөр гарын үсэглэнэ
(`sign_v4`). boto3 (~15 MB) нэмэхгүйн тулд httpx-ээр шууд.
"""

import asyncio
import hashlib
import hmac
from datetime import UTC, datetime
from pathlib import Path
from typing import Protocol
from urllib.parse import quote

import httpx

from app.core.config import settings


class StorageError(Exception):
    pass


class BlobStorage(Protocol):
    async def put(self, key: str, data: bytes, content_type: str) -> None: ...

    async def get(self, key: str) -> bytes: ...

    async def delete(self, key: str) -> None:
        """Байхгүй файлыг устгах нь алдаа биш."""
        ...


def _check_key(key: str) -> str:
    parts = key.split("/")
    if not key or key.startswith("/") or any(part in {"", ".", ".."} for part in parts):
        raise StorageError(f"bad key {key!r}")
    return key


class LocalBlobStorage:
    """Хөгжүүлэлт, тестэд. Production-д ашиглахгүй (контейнер солигдоход алга болно)."""

    def __init__(self, root: str | Path) -> None:
        self._root = Path(root).resolve()

    def _path(self, key: str) -> Path:
        return self._root / _check_key(key)

    async def put(self, key: str, data: bytes, content_type: str) -> None:
        path = self._path(key)

        def write() -> None:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)

        await asyncio.to_thread(write)

    async def get(self, key: str) -> bytes:
        path = self._path(key)
        try:
            return await asyncio.to_thread(path.read_bytes)
        except FileNotFoundError as exc:
            raise StorageError(f"missing {key}") from exc

    async def delete(self, key: str) -> None:
        await asyncio.to_thread(self._path(key).unlink, missing_ok=True)


def _hmac(key: bytes, message: str) -> bytes:
    return hmac.new(key, message.encode(), hashlib.sha256).digest()


def sign_v4(
    *,
    method: str,
    host: str,
    path: str,
    headers: dict[str, str],
    payload_hash: str,
    access_key_id: str,
    secret_access_key: str,
    region: str,
    service: str,
    now: datetime,
) -> str:
    """AWS Signature V4-ийн `Authorization` толгой. `headers` нь `host`-ыг оруулаад
    гарын үсэг зурах бүх толгой (жижиг үсгээр). Query string ашиглахгүй."""
    amz_date = now.strftime("%Y%m%dT%H%M%SZ")
    datestamp = now.strftime("%Y%m%d")
    names = sorted(headers)
    canonical_headers = "".join(f"{name}:{headers[name].strip()}\n" for name in names)
    signed_headers = ";".join(names)
    canonical_request = "\n".join(
        [method, path, "", canonical_headers, signed_headers, payload_hash]
    )
    scope = f"{datestamp}/{region}/{service}/aws4_request"
    string_to_sign = "\n".join(
        [
            "AWS4-HMAC-SHA256",
            amz_date,
            scope,
            hashlib.sha256(canonical_request.encode()).hexdigest(),
        ]
    )
    key = _hmac(f"AWS4{secret_access_key}".encode(), datestamp)
    key = _hmac(key, region)
    key = _hmac(key, service)
    key = _hmac(key, "aws4_request")
    signature = hmac.new(key, string_to_sign.encode(), hashlib.sha256).hexdigest()
    return (
        f"AWS4-HMAC-SHA256 Credential={access_key_id}/{scope}, "
        f"SignedHeaders={signed_headers}, Signature={signature}"
    )


class R2BlobStorage:
    def __init__(
        self,
        account_id: str,
        access_key_id: str,
        secret_access_key: str,
        bucket: str,
        *,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self._host = f"{account_id}.r2.cloudflarestorage.com"
        self._access_key_id = access_key_id
        self._secret_access_key = secret_access_key
        self._bucket = bucket
        self._client = client or httpx.AsyncClient(timeout=settings.live_r2_timeout_seconds)

    async def aclose(self) -> None:
        await self._client.aclose()

    async def _request(
        self, method: str, key: str, body: bytes = b"", content_type: str | None = None
    ) -> httpx.Response:
        path = f"/{self._bucket}/{quote(_check_key(key), safe='/-_.~')}"
        now = datetime.now(UTC)
        payload_hash = hashlib.sha256(body).hexdigest()
        headers = {
            "host": self._host,
            "x-amz-content-sha256": payload_hash,
            "x-amz-date": now.strftime("%Y%m%dT%H%M%SZ"),
        }
        if content_type:
            headers["content-type"] = content_type
        authorization = sign_v4(
            method=method,
            host=self._host,
            path=path,
            headers=headers,
            payload_hash=payload_hash,
            access_key_id=self._access_key_id,
            secret_access_key=self._secret_access_key,
            region="auto",
            service="s3",
            now=now,
        )
        try:
            return await self._client.request(
                method,
                f"https://{self._host}{path}",
                content=body or None,
                headers={**headers, "authorization": authorization},
            )
        except httpx.HTTPError as exc:
            raise StorageError(f"R2 {method} {type(exc).__name__}") from exc

    async def put(self, key: str, data: bytes, content_type: str) -> None:
        response = await self._request("PUT", key, data, content_type)
        if response.status_code != 200:
            raise StorageError(f"R2 PUT → {response.status_code}")

    async def get(self, key: str) -> bytes:
        response = await self._request("GET", key)
        if response.status_code != 200:
            raise StorageError(f"R2 GET → {response.status_code}")
        return response.content

    async def delete(self, key: str) -> None:
        response = await self._request("DELETE", key)
        if response.status_code not in (200, 204, 404):
            raise StorageError(f"R2 DELETE → {response.status_code}")


def r2_configured() -> bool:
    return all(
        (
            settings.live_r2_account_id,
            settings.live_r2_access_key_id,
            settings.live_r2_secret_access_key,
            settings.live_r2_bucket,
        )
    )


def storage_configured() -> bool:
    """Production-д зөвхөн R2; бусад орчинд локал хавтас хүрэлцэнэ."""
    return r2_configured() or not settings.is_production


_storage: BlobStorage | None = None


def get_storage() -> BlobStorage:
    """Процесст нэг. Тохиргоогүй production-д дуудахаас өмнө `storage_configured()`."""
    global _storage
    if _storage is None:
        if r2_configured():
            _storage = R2BlobStorage(
                settings.live_r2_account_id,
                settings.live_r2_access_key_id,
                settings.live_r2_secret_access_key,
                settings.live_r2_bucket,
            )
        else:
            _storage = LocalBlobStorage(settings.live_storage_dir)
    return _storage
