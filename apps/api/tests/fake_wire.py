"""Олон төлбөртэй тестэд зориулсан Wire-ийн загвар.

`test_billing.wire_api` нь үргэлж нэг `pi_1` буцаадаг. Энд нэхэмжлэх бүр өөр
intent (`pi_1`, `pi_2`, …) авч, Wire руу илгээсэн дүнгээ санадаг — хөнгөлөлттэй
дүн ч таарна. Төлбөрийн төлөвийг `status`-аар удирдана.
"""

import json
from collections.abc import AsyncGenerator
from dataclasses import dataclass, field

import httpx
import pytest

from app.core.config import settings
from app.main import app
from app.services.wire import get_wire_client


@dataclass
class FakeWire:
    # Шалгахад Wire-ийн хэлэх төлөв: `succeeded`, `canceled`, `requires_payment_method`.
    status: str = "succeeded"
    # intent id -> Wire руу илгээсэн дүн.
    amounts: dict[str, int] = field(default_factory=dict)
    descriptions: dict[str, str] = field(default_factory=dict)

    def handle(self, request: httpx.Request) -> httpx.Response:
        path = request.url.path
        if request.method == "POST" and path == "/v1/payment_intents":
            body = json.loads(request.content)
            intent_id = f"pi_{len(self.amounts) + 1}"
            self.amounts[intent_id] = body["amount"]
            self.descriptions[intent_id] = body["description"]
            return httpx.Response(
                200,
                json={
                    "id": intent_id,
                    "status": "requires_payment_method",
                    "amount": body["amount"],
                },
            )
        if request.method == "POST" and path == "/v1/checkout/sessions":
            intent_id = json.loads(request.content)["payment_intent"]
            return httpx.Response(
                200,
                json={
                    "id": f"cs_{intent_id}",
                    "url": "https://pay.wire.mn/c/tok",
                    "payment_intent": intent_id,
                },
            )
        if request.method == "GET" and path.startswith("/v1/payment_intents/"):
            intent_id = path.rsplit("/", 1)[1]
            return httpx.Response(
                200,
                json={
                    "id": intent_id,
                    "status": self.status,
                    "amount": self.amounts[intent_id],
                    "currency": "MNT",
                },
            )
        return httpx.Response(404, json={"error": {"code": "not_found"}})

    @property
    def last_amount(self) -> int:
        return list(self.amounts.values())[-1]


def install_fake_wire(monkeypatch: pytest.MonkeyPatch) -> FakeWire:
    monkeypatch.setattr(settings, "wire_secret_key", "sk_test_123")
    monkeypatch.setattr(settings, "wire_webhook_secret", "whsec_test")
    monkeypatch.setattr(settings, "wire_allowed_operators", ["sandbox"])
    monkeypatch.setattr(settings, "site_url", "https://medleghub.com")
    fake = FakeWire()

    async def override() -> AsyncGenerator[httpx.AsyncClient, None]:
        async with httpx.AsyncClient(
            transport=httpx.MockTransport(fake.handle), base_url="https://api.wire.test"
        ) as client:
            yield client

    app.dependency_overrides[get_wire_client] = override
    return fake


async def checkout(
    client: httpx.AsyncClient, api: str, months: int = 1, promo_code: str | None = None
) -> str:
    body: dict[str, object] = {"months": months}
    if promo_code is not None:
        body["promo_code"] = promo_code
    response = await client.post(f"{api}/billing/checkout", json=body)
    assert response.status_code == 200, response.text
    return response.json()["payment_id"]


async def pay(client: httpx.AsyncClient, api: str, payment_id: str) -> dict:
    """Буцах хуудас шиг төлөвийг шалгана — Wire `succeeded` бол багц сунгагдана."""
    response = await client.get(f"{api}/billing/payments/{payment_id}")
    assert response.status_code == 200, response.text
    return response.json()
