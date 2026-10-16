"""SQL скриптийг `mysql` CLI шиг statement болгон хуваана.

Сервер нэг хүсэлтэд нэг statement хүлээн авна (`MULTI_STATEMENTS` унтраалттай).
Тиймээс хуваах ажлыг `mysql` клиент хийдэгтэй адил энд хийнэ:

- `;` нь мөр, нэр (`'…'`, `"…"`, `` `…` ``) болон тайлбар дотор бол
  тусгаарлагч биш.
- `DELIMITER $$` бол SQL биш, КЛИЕНТИЙН тушаал. Процедур, trigger-ийн бие олон
  `;` агуулдаг тул хичээлүүд `DELIMITER $$ … END$$ DELIMITER ;` бичдэг.
  Сервер үүнийг ойлгохгүй тул энд задалж, тусгаарлагчийг хасаад илгээнэ.
- `-- ` нь араасаа зай эсвэл мөрийн төгсгөлтэй үед л тайлбар (MySQL-ийн дүрэм):
  `SELECT 5--2` нь `5 - (-2)`.
- `/*! … */`, `/*+ … */` нь серверт утгатай тул statement-д үлдэнэ.
"""

import bisect
import re
from dataclasses import dataclass

DEFAULT_DELIMITER = ";"

_DELIMITER_COMMAND = re.compile(r"delimiter[ \t]", re.IGNORECASE)


@dataclass(frozen=True)
class Statement:
    text: str
    # Statement-ийн эхний утгатай тэмдэгтийн мөр (1-ээс). Алдааны мессежид.
    line: int


class SplitError(ValueError):
    def __init__(self, line: int, message: str) -> None:
        super().__init__(message)
        self.line = line
        self.message = message


def _skip_quoted(source: str, start: int) -> int:
    """`start` дахь хашилтын хаагдах байрлалын ДАРААХ индексийг буцаана.

    `'` ба `"` дотор `\\` нь дараагийн тэмдэгтийг escape хийнэ, давхар хашилт
    нь өөрөө escape. `` ` `` дотор зөвхөн давхар `` `` `` escape. Хаагдаагүй бол
    текстийн төгсгөл — сервер синтакс алдааг өөрөө мэдэгдэнэ.
    """
    quote = source[start]
    i = start + 1
    length = len(source)
    while i < length:
        char = source[i]
        if char == "\\" and quote != "`":
            i += 2
            continue
        if char == quote:
            if i + 1 < length and source[i + 1] == quote:
                i += 2
                continue
            return i + 1
        i += 1
    return length


def _line_end(source: str, start: int) -> int:
    end = source.find("\n", start)
    return len(source) if end == -1 else end


def split_statements(source: str) -> list[Statement]:
    source = source.replace("\r\n", "\n").replace("\r", "\n")
    newlines = [index for index, char in enumerate(source) if char == "\n"]

    def line_of(index: int) -> int:
        return bisect.bisect_right(newlines, index - 1) + 1

    statements: list[Statement] = []
    delimiter = DEFAULT_DELIMITER
    # Одоогийн statement-ийн эхний утгатай тэмдэгт. None бол statement эхлээгүй.
    begin: int | None = None
    length = len(source)
    i = 0

    while i < length:
        char = source[i]

        if begin is None and _DELIMITER_COMMAND.match(source, i):
            end = _line_end(source, i)
            parts = source[i:end].split()
            if len(parts) < 2:
                raise SplitError(line_of(i), "DELIMITER-ийн араас шинэ тусгаарлагч бичнэ үү.")
            delimiter = parts[1]
            i = end
            continue

        if char in " \t\n":
            i += 1
            continue

        if source.startswith("--", i) and (i + 2 == length or source[i + 2] in " \t\n"):
            i = _line_end(source, i)
            continue

        if char == "#":
            i = _line_end(source, i)
            continue

        if source.startswith("/*", i):
            close = source.find("*/", i + 2)
            end = length if close == -1 else close + 2
            if source.startswith(("/*!", "/*+"), i) and begin is None:
                begin = i
            i = end
            continue

        if char in "'\"`":
            if begin is None:
                begin = i
            i = _skip_quoted(source, i)
            continue

        if source.startswith(delimiter, i):
            if begin is not None:
                text = source[begin:i].rstrip()
                statements.append(Statement(text=text, line=line_of(begin)))
                begin = None
            i += len(delimiter)
            continue

        if begin is None:
            begin = i
        i += 1

    if begin is not None:
        text = source[begin:].rstrip()
        statements.append(Statement(text=text, line=line_of(begin)))

    return statements
