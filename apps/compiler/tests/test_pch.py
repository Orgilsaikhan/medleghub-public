"""PCH сонголт — emcc шаардахгүй, хаана ч ажиллана."""

import pytest

from compiler import pch
from compiler.pch import header_name, header_text, leading_system_headers, select

LESSON = """\
// Оюутны бүртгэл
#include <iostream>
#include <string>
#include <vector>

using namespace std;

#include <algorithm>

int main() {}
"""


def test_reads_only_the_leading_include_block() -> None:
    """Кодын дундах `#include <algorithm>` нь PCH сонголтод орохгүй."""
    assert leading_system_headers(LESSON) == {"iostream", "string", "vector"}


def test_comments_and_blank_lines_do_not_end_the_block() -> None:
    source = "/* Тайлбар\n   олон мөр */\n\n#include <iostream> // гаралт\n#  include<string>\n"

    assert leading_system_headers(source) == {"iostream", "string"}


def test_define_before_includes_disables_pch() -> None:
    """Макро нь толгой файлын агуулгыг өөрчилж болзошгүй."""
    source = "#define _USE_MATH_DEFINES\n#include <iostream>\n"

    assert leading_system_headers(source) == frozenset()
    assert select(leading_system_headers(source)) is None


def test_quoted_include_ends_the_block() -> None:
    source = '#include <iostream>\n#include "mine.h"\n#include <vector>\n'

    assert leading_system_headers(source) == {"iostream"}


def test_lessons_with_iostream_get_the_pch() -> None:
    assert select(frozenset({"iostream", "string", "vector"})) == {"iostream"}


def test_no_pch_without_iostream() -> None:
    assert select(frozenset({"vector", "string"})) is None
    assert select(frozenset()) is None


def test_selection_is_always_fully_included(monkeypatch: pytest.MonkeyPatch) -> None:
    """Олон олонлогтой байсан ч сурагчийн include хийгээгүй толгой файл сонгогдохгүй."""
    monkeypatch.setattr(
        pch,
        "PCH_SETS",
        (
            frozenset({"iostream"}),
            frozenset({"iostream", "vector"}),
            frozenset({"algorithm", "iostream", "vector"}),
        ),
    )

    assert select(frozenset({"iostream", "string"})) == {"iostream"}
    assert select(frozenset({"iostream", "string", "vector"})) == {"iostream", "vector"}
    assert select(frozenset({"algorithm", "iostream", "vector"})) == {
        "algorithm",
        "iostream",
        "vector",
    }


def test_names_are_stable() -> None:
    assert header_name(frozenset({"iostream"})) == "iostream.h"
    assert header_name(frozenset({"string", "iostream"})) == "iostream-string.h"
    assert header_text(frozenset({"string", "iostream"})) == (
        "#include <iostream>\n#include <string>\n"
    )
