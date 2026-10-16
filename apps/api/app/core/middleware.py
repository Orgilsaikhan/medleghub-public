"""API-ийн аюулгүй байдлын header-ууд."""

from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

# API нь зөвхөн JSON буцаадаг тул хамгаалалт нь энгийн бөгөөд хатуу.
SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
    "Cross-Origin-Resource-Policy": "same-site",
    # JSON API нь ямар ч нөөц ачаалах шаардлагагүй.
    "Content-Security-Policy": "default-src 'none'; frame-ancestors 'none'",
}


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        response = await call_next(request)

        for key, value in SECURITY_HEADERS.items():
            # Swagger UI нь өөрийн CSS/JS ачаалдаг тул CSP-г алгасана.
            if key == "Content-Security-Policy" and request.url.path in {"/docs", "/openapi.json"}:
                continue
            response.headers.setdefault(key, value)

        return response
