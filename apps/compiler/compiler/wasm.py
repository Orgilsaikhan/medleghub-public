"""WebAssembly модульд хөрвүүлэгчийн анхааруулгыг хавсаргана.

Амжилттай хөрвүүлэлтийн хариу нь `application/wasm` байт. Анхааруулгыг
(`-Wall`) header-т хийвэл reverse proxy-ийн header-ийн хэмжээний хязгаарт
тулна, JSON+base64 болговол модуль 33% томорно. Тиймээс модуль дотор нь
**custom section** болгон хийнэ.

Custom section бол WebAssembly-ийн стандарт механизм (`name`, `producers`
section-ууд ч мөн адил). Модулийг ажиллуулахад огт нөлөөлөхгүй, browser нь
`WebAssembly.Module.customSections(module, WARNINGS_SECTION)`-ээр уншина.
"""

WARNINGS_SECTION = "medleghub.warnings"

_CUSTOM_SECTION_ID = b"\x00"


def _uleb128(value: int) -> bytes:
    """WebAssembly-ийн хэмжээ бичих хувьсах урттай кодчилол."""
    if value < 0:
        raise ValueError("uleb128 нь сөрөг тоо кодлохгүй")
    out = bytearray()
    while True:
        byte = value & 0x7F
        value >>= 7
        if value:
            out.append(byte | 0x80)
        else:
            out.append(byte)
            return bytes(out)


def append_custom_section(module: bytes, name: str, payload: bytes) -> bytes:
    """Модулийн төгсгөлд custom section нэмнэ.

    Стандартын дагуу custom section нь модулийн аль ч хэсэгт, тэр дундаа
    хамгийн төгсгөлд байж болно — бусад section-ийг задлах шаардлагагүй.
    """
    encoded_name = name.encode("utf-8")
    body = _uleb128(len(encoded_name)) + encoded_name + payload
    return module + _CUSTOM_SECTION_ID + _uleb128(len(body)) + body
