"""Pydantic загвараас AI-д илгээх энгийн JSON Schema.

Gemini нь JSON Schema-ийн дэд хэсгийг л дэмждэг (type, properties, required,
items, enum, min/max…); маш гүн, `$ref`-тэй схемийг татгалзаж болно. Тиймээс
`$defs`-ийг шигтгэж, `title`/`default`-ийг хасна. LLM-ийн схемд `Optional`
талбар бүү ашигла (`anyOf` дэмжигдэхгүй) — «мэдэхгүй» бол 0 эсвэл хоосон мөр.
"""

from typing import Any

from pydantic import BaseModel

_DROP = {"title", "default"}


def llm_schema(model: type[BaseModel]) -> dict[str, Any]:
    raw = model.model_json_schema()
    defs = raw.pop("$defs", {})

    def resolve(node: Any) -> Any:
        if isinstance(node, list):
            return [resolve(item) for item in node]
        if not isinstance(node, dict):
            return node
        if "$ref" in node:
            return resolve(defs[node["$ref"].rsplit("/", 1)[-1]])
        out: dict[str, Any] = {}
        for key, value in node.items():
            if key in _DROP:
                continue
            if key == "properties":
                # Энд түлхүүр нь талбарын нэр (`title` байж болно) — хасахгүй.
                out[key] = {name: resolve(prop) for name, prop in value.items()}
            else:
                out[key] = resolve(value)
        return out

    return resolve(raw)
