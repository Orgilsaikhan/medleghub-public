"""WebAssembly модулийг тестэд задлах жижиг туслах функцүүд."""

MAGIC = b"\0asm\x01\0\0\0"

_CUSTOM, _IMPORT, _EXPORT = 0, 2, 7


def read_uleb128(data: bytes, offset: int) -> tuple[int, int]:
    result = shift = 0
    while True:
        byte = data[offset]
        offset += 1
        result |= (byte & 0x7F) << shift
        shift += 7
        if byte < 0x80:
            return result, offset


def sections(module: bytes) -> list[tuple[int, bytes]]:
    assert module[:8] == MAGIC, "WebAssembly толгой буруу"
    found: list[tuple[int, bytes]] = []
    offset = 8
    while offset < len(module):
        section_id = module[offset]
        size, offset = read_uleb128(module, offset + 1)
        found.append((section_id, module[offset : offset + size]))
        offset += size
    assert offset == len(module), "section-уудын хэмжээ файлын хэмжээтэй таарахгүй"
    return found


def _name(body: bytes, offset: int) -> tuple[str, int]:
    length, offset = read_uleb128(body, offset)
    return body[offset : offset + length].decode("utf-8"), offset + length


def custom_sections(module: bytes, name: str) -> list[bytes]:
    payloads = []
    for section_id, body in sections(module):
        if section_id == _CUSTOM:
            section_name, offset = _name(body, 0)
            if section_name == name:
                payloads.append(body[offset:])
    return payloads


def _skip_limits(body: bytes, offset: int) -> int:
    flags = body[offset]
    _, offset = read_uleb128(body, offset + 1)
    if flags & 1:
        _, offset = read_uleb128(body, offset)
    return offset


def imports(module: bytes) -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    for section_id, body in sections(module):
        if section_id != _IMPORT:
            continue
        count, offset = read_uleb128(body, 0)
        for _ in range(count):
            module_name, offset = _name(body, offset)
            field, offset = _name(body, offset)
            kind = body[offset]
            offset += 1
            if kind == 0:  # функц: төрлийн дугаар
                _, offset = read_uleb128(body, offset)
            elif kind == 1:  # хүснэгт: reftype + хязгаар
                offset = _skip_limits(body, offset + 1)
            elif kind == 2:  # санах ой: хязгаар
                offset = _skip_limits(body, offset)
            elif kind == 3:  # глобал: төрөл + өөрчлөгдөх эсэх
                offset += 2
            elif kind == 4:  # exception tag: шинж + төрлийн дугаар
                _, offset = read_uleb128(body, offset + 1)
            found.append((module_name, field))
    return found


def exports(module: bytes) -> list[str]:
    names: list[str] = []
    for section_id, body in sections(module):
        if section_id != _EXPORT:
            continue
        count, offset = read_uleb128(body, 0)
        for _ in range(count):
            name, offset = _name(body, offset)
            _, offset = read_uleb128(body, offset + 1)
            names.append(name)
    return names
