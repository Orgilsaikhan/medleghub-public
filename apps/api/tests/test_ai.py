"""AI давхарга: Gemini-ийн REST client, схем, үнэ, R2-ийн гарын үсэг, загварын нэрийн дүрэм."""

import json
import re
import uuid
from datetime import UTC, date, datetime
from decimal import Decimal
from pathlib import Path

import httpx
import pytest
from pydantic import BaseModel

from app.live.ai_outputs import DocumentAnalysis, QuizOutput, QuizQuestionOutput
from app.live.pipeline import normalize_quiz
from app.live.storage import sign_v4
from app.services.ai import prices
from app.services.ai.errors import AIError, AIIncompleteError
from app.services.ai.providers.gemini import GeminiProvider, build_body
from app.services.ai.providers.openrouter import OpenRouterProvider
from app.services.ai.providers.openrouter import build_body as openrouter_body
from app.services.ai.router import ModelHealth, cooldown
from app.services.ai.routing import ModelRoute
from app.services.ai.schema import llm_schema
from app.services.ai.types import Part, ProviderRequest, Usage

APP = Path(__file__).resolve().parents[1] / "app"


def request(**overrides: object) -> ProviderRequest:
    values: dict = {
        "capability": "document",
        "model": "gemini-3.8-flash",
        "system": "Чи багш.",
        "parts": [Part.of_document(b"%PDF-1.7", "application/pdf"), Part.of_text("задал")],
        "schema": {"type": "object"},
        "max_output_tokens": 1000,
        "thinking_level": "low",
        "timeout_seconds": 5.0,
    }
    values.update(overrides)
    return ProviderRequest(**values)


def completed(text: str, **usage: int) -> dict:
    return {
        "id": "interaction-1",
        "status": "completed",
        "steps": [
            {"type": "user_input", "content": [{"type": "text", "text": "…"}]},
            {"type": "model_output", "content": [{"type": "text", "text": text}]},
        ],
        "usage": {
            "total_input_tokens": 1200,
            "total_cached_tokens": 200,
            "total_output_tokens": 300,
            "total_thought_tokens": 50,
            **usage,
        },
    }


def provider(handler) -> GeminiProvider:
    client = httpx.AsyncClient(
        base_url="https://gemini.test", transport=httpx.MockTransport(handler)
    )
    return GeminiProvider("key-123", "https://gemini.test", client=client)


def test_body_never_stores_and_carries_the_schema() -> None:
    body = build_body(request())
    assert body["store"] is False
    assert body["model"] == "gemini-3.8-flash"
    assert body["system_instruction"] == "Чи багш."
    assert body["response_format"] == {
        "type": "text",
        "mime_type": "application/json",
        "schema": {"type": "object"},
    }
    assert body["generation_config"] == {"thinking_level": "low", "max_output_tokens": 1000}
    document, text = body["input"]
    assert document == {"type": "document", "data": "JVBERi0xLjc=", "mime_type": "application/pdf"}
    assert text == {"type": "text", "text": "задал"}


async def test_successful_interaction() -> None:
    seen: list[httpx.Request] = []

    def handler(req: httpx.Request) -> httpx.Response:
        seen.append(req)
        return httpx.Response(200, json=completed('{"ok": true}'))

    result = await provider(handler).generate(request())
    assert result.text == '{"ok": true}'
    assert result.request_id == "interaction-1"
    assert result.usage == Usage(1200, 200, 300, 50)
    assert seen[0].url.path == "/v1beta/interactions"
    assert seen[0].headers["x-goog-api-key"] == "key-123"
    assert json.loads(seen[0].content)["store"] is False


@pytest.mark.parametrize(
    ("status", "error", "retryable"),
    [
        (503, {"status": "UNAVAILABLE"}, True),
        (429, {"status": "RESOURCE_EXHAUSTED", "code": 429}, True),
        # Өдрийн квот загвар тутамд — router өөр загвар руу шилжинэ.
        (429, {"status": "quota_exceeded"}, True),
        (402, {"status": "payment_required"}, False),
        (400, {"status": "INVALID_ARGUMENT"}, False),
    ],
)
async def test_errors_are_classified(status: int, error: dict, retryable: bool) -> None:
    gemini = provider(lambda _: httpx.Response(status, json={"error": error}))
    with pytest.raises(AIError) as caught:
        await gemini.generate(request())
    assert caught.value.code == f"http_{status}"
    assert caught.value.retryable is retryable


async def test_retry_delay_is_read_from_header_or_body() -> None:
    with_header = provider(
        lambda _: httpx.Response(
            429, headers={"Retry-After": "17"}, json={"error": {"code": "rate_limit_exceeded"}}
        )
    )
    with pytest.raises(AIError) as caught:
        await with_header.generate(request())
    assert caught.value.retry_after == 17.0
    assert caught.value.detail == "rate_limit_exceeded"

    body = {
        "error": {
            "status": "RESOURCE_EXHAUSTED",
            "details": [{"@type": "type.googleapis.com/google.rpc.RetryInfo", "retryDelay": "32s"}],
        }
    }
    with pytest.raises(AIError) as caught:
        await provider(lambda _: httpx.Response(429, json=body)).generate(request())
    assert caught.value.retry_after == 32.0


def test_cooldowns_follow_the_error() -> None:
    limited = AIError("http_429", "rate_limit_exceeded", retryable=True)
    assert cooldown(limited, 1) == ("rate_limited", 60.0)
    quota = AIError("http_429", "quota_exceeded", retryable=True)
    assert cooldown(quota, 1) == ("quota", 3600.0)
    hinted = AIError("http_429", "resource_exhausted", retryable=True, retry_after=12.0)
    assert cooldown(hinted, 1) == ("rate_limited", 12.0)
    busy = AIError("http_503", "service_unavailable", retryable=True)
    assert [cooldown(busy, n)[1] for n in (1, 2, 3, 6, 9)] == [4.0, 8.0, 16.0, 120.0, 120.0]
    assert cooldown(AIError("timeout", retryable=True), 1) == ("timeout", 4.0)

    clock = [0.0]
    health = ModelHealth(clock=lambda: clock[0])
    assert health.remaining("gemini:a") == 0
    health.failure("gemini:a", busy)
    health.failure("gemini:a", busy)
    assert health.remaining("gemini:a") == 8.0
    assert health.get("gemini:a").reason == "overloaded"
    clock[0] = 8.0
    assert health.remaining("gemini:a") == 0
    health.success("gemini:a")
    assert health.get("gemini:a").failures == 0


async def test_timeouts_are_retryable() -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("slow")

    with pytest.raises(AIError) as caught:
        await provider(handler).generate(request())
    assert (caught.value.code, caught.value.retryable) == ("timeout", True)


async def test_incomplete_output_keeps_usage_for_billing() -> None:
    body = completed("{", total_output_tokens=1000)
    body["status"] = "incomplete"
    with pytest.raises(AIIncompleteError) as caught:
        await provider(lambda _: httpx.Response(200, json=body)).generate(request())
    assert caught.value.usage.output_tokens == 1000


def test_llm_schema_is_flat_and_keeps_title_fields() -> None:
    schema = llm_schema(DocumentAnalysis)
    text = json.dumps(schema)
    assert "$ref" not in text and "$defs" not in text and "anyOf" not in text
    assert "title" in schema["properties"]
    topic = schema["properties"]["sections"]["items"]["properties"]["topics"]["items"]
    assert set(topic["required"]) == {"key", "title", "summary", "pages", "cards"}
    assert "title" not in {key for key in topic if key != "properties"}
    assert schema["properties"]["language"]["enum"] == ["mn", "en", "mixed"]

    class Nested(BaseModel):
        title: str

    assert llm_schema(Nested) == {
        "properties": {"title": {"type": "string"}},
        "required": ["title"],
        "type": "object",
    }


def test_prices_follow_their_dates() -> None:
    route = ModelRoute("gemini", "gemini-3.8-flash")
    before = prices.price_for(route, date(2026, 12, 31))
    after = prices.price_for(route, date(2027, 1, 1))
    assert before is not None and after is not None
    assert after.input == 2 * before.input
    assert prices.price_for(route, date(2025, 12, 31)) is None
    assert prices.price_for(ModelRoute("gemini", "unknown"), date(2026, 10, 1)) is None
    assert prices.price_for(ModelRoute("fake", "x"), date(2026, 10, 1)) == prices.ZERO

    usage = Usage(
        input_tokens=1_000_000,
        cached_input_tokens=200_000,
        output_tokens=100_000,
        reasoning_tokens=100_000,
    )
    # 800k × 0.75 + 200k × 0.075 + 200k × 3.75 = 0.6 + 0.015 + 0.75
    assert prices.cost_usd(before, usage) == Decimal("1.365000")
    assert prices.worst_case_usd(before, 10_000, 32_768) == Decimal("0.130380")


def test_normalize_quiz_shuffles_but_keeps_the_answer() -> None:
    keys = {"sort": uuid.uuid4()}
    output = QuizOutput(
        questions=[
            QuizQuestionOutput(
                prompt=f"Асуулт {index}",
                options=["зөв", "буруу 1", "буруу 2", "буруу 3"],
                correct_index=0,
                explanation="тайлбар",
                topic_key="Sort",
                page=2,
            )
            for index in range(30)
        ]
        + [
            QuizQuestionOutput(
                prompt="Давхардсан хариулт",
                options=["а", "А", "б", "в"],
                correct_index=0,
                explanation="",
                topic_key="sort",
                page=0,
            ),
            QuizQuestionOutput(
                prompt="Гурван хариулт",
                options=["а", "б", "в"],
                correct_index=0,
                explanation="",
                topic_key="sort",
                page=0,
            ),
        ]
    )
    questions = normalize_quiz(output, keys, page_count=10, limit=40)
    assert len(questions) == 30
    assert all(q["options"][q["correct_index"]] == "зөв" for q in questions)
    assert len({q["correct_index"] for q in questions}) > 1
    assert all(q["topic_id"] == keys["sort"] and q["page"] == 2 for q in questions)
    assert len(normalize_quiz(output, keys, page_count=1, limit=5)) == 5
    assert normalize_quiz(output, keys, page_count=1, limit=5)[0]["page"] is None


def test_sigv4_matches_the_aws_example() -> None:
    """AWS S3 «Signature Version 4: GET Object» жишээ."""
    empty = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    authorization = sign_v4(
        method="GET",
        host="examplebucket.s3.amazonaws.com",
        path="/test.txt",
        headers={
            "host": "examplebucket.s3.amazonaws.com",
            "range": "bytes=0-9",
            "x-amz-content-sha256": empty,
            "x-amz-date": "20130524T000000Z",
        },
        payload_hash=empty,
        access_key_id="AKIAIOSFODNN7EXAMPLE",
        secret_access_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
        region="us-east-1",
        service="s3",
        now=datetime(2013, 5, 24, tzinfo=UTC),
    )
    assert authorization == (
        "AWS4-HMAC-SHA256 Credential=AKIAIOSFODNN7EXAMPLE/20130524/us-east-1/s3/aws4_request, "
        "SignedHeaders=host;range;x-amz-content-sha256;x-amz-date, "
        "Signature=f0e8bdb87c964420e857bd35b5d6ed310bd44f0170aba48dd91039c6036bdb41"
    )


def test_model_names_live_only_in_config_and_prices() -> None:
    """Загвар солиход код өөрчлөгдөхгүй: нэр нь зөвхөн тохиргоо, үнийн хүснэгтэд."""
    allowed = {APP / "core" / "config.py", APP / "services" / "ai" / "prices.py"}
    pattern = re.compile(r"""["'](?:gemini|gpt)-[0-9]""")
    offenders = [
        str(path.relative_to(APP))
        for path in APP.rglob("*.py")
        if path not in allowed and pattern.search(path.read_text(encoding="utf-8"))
    ]
    assert offenders == []


# --- OpenRouter ----------------------------------------------------------------


def openrouter(handler) -> OpenRouterProvider:
    client = httpx.AsyncClient(
        base_url="https://openrouter.test/api/v1", transport=httpx.MockTransport(handler)
    )
    return OpenRouterProvider("or-key", "https://openrouter.test/api/v1", client=client)


def completion(content: str, finish: str = "stop") -> dict:
    return {
        "id": "gen-1",
        "choices": [
            {"message": {"role": "assistant", "content": content}, "finish_reason": finish}
        ],
        "usage": {
            "prompt_tokens": 28000,
            "completion_tokens": 1500,
            "prompt_tokens_details": {"cached_tokens": 20000},
            "completion_tokens_details": {"reasoning_tokens": 500},
            "cost": 0.012345,
        },
    }


def test_openrouter_body_denies_training_and_reads_pdfs_natively() -> None:
    body = openrouter_body(request(model="google/gemini-3.8-flash", schema=llm_schema(QuizOutput)))
    assert body["model"] == "google/gemini-3.8-flash"
    assert body["provider"]["data_collection"] == "deny"
    assert body["provider"]["require_parameters"] is True
    assert "zdr" not in body["provider"]
    assert body["plugins"] == [{"id": "file-parser", "pdf": {"engine": "native"}}]
    assert body["reasoning"] == {"effort": "low", "exclude": True}
    assert body["max_tokens"] == 1000
    assert body["usage"] == {"include": True}
    system, user = body["messages"]
    assert system == {"role": "system", "content": "Чи багш."}
    document, text = user["content"]
    assert document == {
        "type": "file",
        "file": {
            "filename": "material.pdf",
            "file_data": "data:application/pdf;base64,JVBERi0xLjc=",
        },
    }
    assert text == {"type": "text", "text": "задал"}
    schema = body["response_format"]["json_schema"]
    assert schema["strict"] is True
    assert schema["schema"]["additionalProperties"] is False
    question = schema["schema"]["properties"]["questions"]["items"]
    assert question["additionalProperties"] is False
    image = openrouter_body(request(parts=[Part.of_image(b"\x89PNG", "image/png")]))
    assert image["messages"][1]["content"][0]["type"] == "image_url"


async def test_openrouter_success_uses_the_reported_cost() -> None:
    seen: list[httpx.Request] = []

    def handler(req: httpx.Request) -> httpx.Response:
        seen.append(req)
        return httpx.Response(200, json=completion('{"ok": true}'))

    result = await openrouter(handler).generate(request(model="google/gemini-3.8-flash"))
    assert result.text == '{"ok": true}'
    assert result.usage == Usage(28000, 20000, 1000, 500, Decimal("0.012345"))
    assert seen[0].url.path == "/api/v1/chat/completions"
    assert seen[0].headers["authorization"] == "Bearer or-key"
    route = ModelRoute("openrouter", "google/gemini-3.8-flash")
    price = prices.price_for(route, date(2026, 10, 1))
    assert price is not None and price.input == Decimal("0.75")
    assert prices.cost_usd(price, result.usage) == Decimal("0.012345")


@pytest.mark.parametrize(
    ("status", "message", "detail", "retryable"),
    [
        (402, "Insufficient credits", "payment_required", False),
        (429, "Rate limit exceeded", "rate_limit_exceeded", True),
        (503, "Provider overloaded", "503", True),
        (404, "No endpoints found matching your data policy", "no_endpoints", False),
    ],
)
async def test_openrouter_errors(status: int, message: str, detail: str, retryable: bool) -> None:
    provider = openrouter(
        lambda _: httpx.Response(status, json={"error": {"code": status, "message": message}})
    )
    with pytest.raises(AIError) as caught:
        await provider.generate(request())
    assert caught.value.code == f"http_{status}"
    assert caught.value.detail == detail
    assert caught.value.retryable is retryable


async def test_openrouter_truncated_or_upstream_errors() -> None:
    truncated = openrouter(lambda _: httpx.Response(200, json=completion("{", finish="length")))
    with pytest.raises(AIIncompleteError) as caught:
        await truncated.generate(request())
    assert caught.value.usage.cost_usd == Decimal("0.012345")
    upstream = openrouter(
        lambda _: httpx.Response(200, json={"error": {"code": 502, "message": "upstream"}})
    )
    with pytest.raises(AIError) as error:
        await upstream.generate(request())
    assert error.value.retryable is True


def test_free_models_cost_nothing_and_chains_follow_the_provider() -> None:
    free = ModelRoute("openrouter", "qwen/qwen3.8-27b:free")
    assert prices.price_for(free, date(2026, 10, 1)) == prices.ZERO
    assert prices.price_for(ModelRoute("openrouter", "unknown/model"), date(2026, 10, 1)) is None

    from app.core.config import Settings

    assert Settings(ai_provider="openrouter").ai_document_models[0] == (
        "openrouter:google/gemini-3.8-flash"
    )
    auto = Settings(ai_provider="auto", openrouter_api_key="k", ai_exam_models="")
    assert auto.ai_exam_models[0] == "openrouter:google/gemini-3.8-flash"
    assert Settings(ai_provider="auto", openrouter_api_key="").ai_exam_models[0] == (
        "gemini:gemini-3.8-flash"
    )
    assert Settings(ai_provider="gemini", ai_guide_models="").ai_guide_models[0] == (
        "gemini:gemini-3.5-flash-lite"
    )


def test_json_is_extracted_from_surrounding_text() -> None:
    from app.services.ai.service import _parse

    class Out(BaseModel):
        answer: str

    assert _parse(Out, '{"answer": "a"}').answer == "a"
    assert _parse(Out, '```json\n{"answer": "b"}\n```').answer == "b"
    assert _parse(Out, 'Here is the JSON requested:\n{"answer": "c"}\nDone.').answer == "c"
    with pytest.raises(ValueError):
        _parse(Out, "no json here")
