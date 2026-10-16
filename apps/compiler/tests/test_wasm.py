"""Анхааруулгын custom section — emcc шаардахгүй, хаана ч ажиллана."""

from compiler.wasm import WARNINGS_SECTION, append_custom_section
from tests.wasm_helpers import MAGIC, custom_sections, read_uleb128, sections


def test_section_is_readable_after_appending() -> None:
    text = b"main.c:4:20: warning: variable 'nas' is uninitialized"

    module = append_custom_section(MAGIC, WARNINGS_SECTION, text)

    assert custom_sections(module, WARNINGS_SECTION) == [text]


def test_large_payload_uses_a_multibyte_size() -> None:
    """127 байтаас их бол хэмжээ нь олон байттай LEB128 болно."""
    payload = "анхааруулга\n".encode() * 100

    module = append_custom_section(MAGIC, WARNINGS_SECTION, payload)

    assert custom_sections(module, WARNINGS_SECTION) == [payload]
    assert len(sections(module)) == 1
    size, _ = read_uleb128(module, 9)
    assert size > 127


def test_existing_sections_are_left_untouched() -> None:
    first = append_custom_section(MAGIC, "producers", b"clang")

    module = append_custom_section(first, WARNINGS_SECTION, b"warning")

    assert module.startswith(first)
    assert custom_sections(module, "producers") == [b"clang"]
    assert custom_sections(module, WARNINGS_SECTION) == [b"warning"]
