"""Хуурамч AI — түлхүүргүйгээр Live-ийг локал дээр, e2e-д бүтнээр нь турших.

`AI_*_MODEL=fake:local` үед идэвхжинэ (production-д тохиргоо хориглоно).
Материалын текстийн гарчиг, догол мөрөөс тодорхой (детерминист) хэсэг, сэдэв,
карт, заавар, тест, таамаг бүтээнэ. Агуулга нь утга учиртай биш — зөвхөн
бүтэц, UI, урсгалыг шалгахад.
"""

import asyncio
import json
import re
from typing import Any

from app.services.ai.types import ProviderRequest, ProviderResult, Usage

_HEADING = re.compile(r"^#{1,3}\s+(\S.*)$")
_PAGE_MARKER = re.compile(r"^---\s+\S+\s+(\d+)")


def _paragraphs(text: str) -> list[tuple[str, str, int]]:
    """`(гарчиг, дараах текст, хуудас)` — Markdown гарчиг эсвэл догол мөрөөр."""
    page = 1
    blocks: list[tuple[str, list[str], int]] = []
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("==="):
            # `=== МАТЕРИАЛ: … ===` толгой.
            continue
        if marker := _PAGE_MARKER.match(line):
            page = int(marker.group(1))
            continue
        if heading := _HEADING.match(line):
            blocks.append((heading.group(1).strip(), [], page))
        elif line and blocks:
            blocks[-1][1].append(line)
        elif line:
            blocks.append((line[:60], [line], page))
    return [(title, " ".join(body), page) for title, body, page in blocks]


def _sentences(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+", text) if len(part.strip()) > 8]


def _document(context: dict[str, Any]) -> dict[str, Any]:
    blocks = _paragraphs(context.get("source_text") or "")[:12]
    if not blocks:
        pages = max(1, int(context.get("page_count") or 1))
        blocks = [
            (f"Үндсэн ойлголт {index}", "Материалын энэ хэсгийн гол санаа.", min(index, pages))
            for index in range(1, 5)
        ]
    topics = []
    for index, (title, body, page) in enumerate(blocks, start=1):
        sentences = _sentences(body) or [body or title]
        topics.append(
            {
                "key": f"topic-{index}",
                "title": title,
                "summary": sentences[0][:200],
                "pages": [page],
                "cards": [
                    {"front": f"{title} — {number}", "back": sentence[:300], "page": page}
                    for number, sentence in enumerate(sentences[:3], start=1)
                ],
            }
        )
    sections = [
        {"title": f"{topics[start]['title']}", "topics": topics[start : start + 3]}
        for start in range(0, len(topics), 3)
    ]
    return {
        "title": context.get("title") or "Материал",
        "summary": "Хуурамч AI-ийн гаргасан товч агуулга (локал турших зориулалттай).",
        "language": "mn",
        "sections": sections,
    }


def _guide(context: dict[str, Any]) -> dict[str, Any]:
    title = context.get("topic_title", "Сэдэв")
    summary = context.get("topic_summary", "")
    pages = context.get("pages") or []
    markdown = "\n\n".join(
        [
            f"## Гол санаа\n\n{summary or title}",
            f"## Ойлгох ёстой зүйлс\n\n- **{title}** — энэ сэдвийн гол ойлголт.",
            "## Жишээ\n\n```\nprint('MedlegHub')\n```",
            "## Түгээмэл алдаа\n\n- Тодорхойлолтыг цээжлээд хэрэглээг нь орхих.",
            f"## Товч дүгнэлт\n\n- {title}\n- Давтаж, тест өгч бататга.",
            f"## Эх сурвалж\n\nх. {', '.join(str(page) for page in pages) or '—'}",
        ]
    )
    return {"markdown": markdown}


def _quiz(context: dict[str, Any]) -> dict[str, Any]:
    topics = context.get("topics") or [{"key": "topic-1", "title": "Сэдэв", "summary": ""}]
    count = int(context.get("count") or 5)
    questions = []
    for index in range(count):
        topic = topics[index % len(topics)]
        others = [other["title"] for other in topics if other["key"] != topic["key"]]
        distractors = (others + ["Өөр сэдэв А", "Өөр сэдэв Б", "Өөр сэдэв В"])[:3]
        questions.append(
            {
                "prompt": f"{index + 1}. «{topic['title']}» сэдэвтэй аль нь холбоотой вэ?",
                "options": [topic["title"], *distractors],
                "correct_index": 0,
                "explanation": f"Асуулт «{topic['title']}» сэдвийн тухай.",
                "topic_key": topic["key"],
                "page": 1,
            }
        )
    return {"questions": questions}


def _exam(context: dict[str, Any]) -> dict[str, Any]:
    topics = context.get("topics") or [{"key": "topic-1", "title": "Сэдэв", "summary": ""}]
    levels = ["high", "medium", "low"]
    return {
        "overview": "Хуурамч AI-ийн таамаг — локал турших зориулалттай.",
        "predictions": [
            {
                "topic_key": topic["key"],
                "title": topic["title"],
                "likelihood": levels[index % 3],
                "reason": "Материалд олон удаа гарсан.",
            }
            for index, topic in enumerate(topics[:6])
        ],
        "questions": [
            {
                "question": f"«{topic['title']}»-г тайлбарлаж, жишээ гарга.",
                "type": ["short", "long", "problem"][index % 3],
                "likelihood": levels[index % 3],
                "answer_outline": f"- {topic['title']}-ийн тодорхойлолт\n- Жишээ",
                "topic_key": topic["key"],
            }
            for index, topic in enumerate(topics[:8])
        ],
        "study_plan": ["Сэдвүүдийн заавар унш.", "Картаар давт.", "Бүтэн тест өг."],
    }


_BUILDERS = {
    "document": _document,
    "study_guide": _guide,
    "topic_quiz": _quiz,
    "full_quiz": _quiz,
    "exam": _exam,
}


class FakeProvider:
    name = "fake"

    async def aclose(self) -> None:
        return None

    async def generate(self, request: ProviderRequest) -> ProviderResult:
        # UI-ийн «бэлтгэж байна» төлөв харагдах хэмжээний саатал.
        await asyncio.sleep(0.3)
        output = json.dumps(_BUILDERS[request.capability](request.context), ensure_ascii=False)
        input_chars = sum(len(part.text or "") + len(part.data or b"") for part in request.parts)
        return ProviderResult(
            text=output,
            usage=Usage(input_tokens=input_chars // 4, output_tokens=len(output) // 4),
            request_id="fake",
        )
