"""Урьдчилан хөрвүүлсэн толгой файл (PCH) — C++ хөрвүүлэлтийг ~3 дахин хурдасгана.

`<iostream>` зэрэг стандарт толгой файлыг задлах нь C++ хөрвүүлэлтийн
хугацааны ихэнхийг эзэлдэг. PCH нь тэдгээрийг урьдчилан задалсан хэлбэр.

ЗААВАЛ ДЭД ОЛОНЛОГ
──────────────────
Clang-ийн PCH нь кодын өмнө автоматаар «include» хийгддэг. PCH-д `<vector>`
байгаад сурагч `#include <vector>` бичихээ мартвал код алдаагүй
хөрвүүлэгдэнэ — өөрийн компьютер дээр л алдаа гарна. Энэ нь сурагчид буруу
зуршил заана.

Тиймээс PCH-г зөвхөн түүний БҮХ толгой файлыг сурагч өөрөө кодын эхэнд
`#include` хийсэн үед ашиглана. PCH нь сурагчийн харах ёсгүй зүйлийг хэзээ
ч харуулахгүй — зөвхөн хурдасгана.

`#include <...>` мөрүүдийн өмнө эсвэл дунд `#define` зэрэг өөр мөр байвал
(толгой файлын агуулгыг өөрчилж болзошгүй) PCH ашиглахгүй.

ЯАГААД ЗӨВХӨН `<iostream>`
───────────────────────────
libc++-ийн `<iostream>` нь `<string>`, `<vector>` зэрэг ихэнх толгой файлыг
дотроо оруулдаг. emsdk 6.0.9 дээрх хэмжилт (3 удаагийн хамгийн сайн):

    Хичээл            PCH-гүй   <iostream>   8 толгой файлтай PCH
    angi-ba-obyekt     873 мс     294 мс       295 мс
    std-vector        1077 мс     505 мс       497 мс

Том олонлог нэмэлт хурд өгөөгүй ч тус бүр image-д 13 MB нэмнэ. C++
хичээлүүд `<iostream>` оруулдаг — «C ба C++» (`c-ba-cpp`) л C-ийн толгой
файлтай тул PCH-гүйгээр хөрвөнө.
"""

import re
from pathlib import Path

PCH_SETS: tuple[frozenset[str], ...] = (frozenset({"iostream"}),)

_COMMENTS = re.compile(r"/\*.*?\*/|//[^\n]*", re.DOTALL)
_SYSTEM_INCLUDE = re.compile(r"#\s*include\s*<([A-Za-z0-9_./+-]+)>")


def leading_system_headers(source: str) -> frozenset[str]:
    """Кодын эхэнд, өөр ямар ч мөрөөс өмнө бичсэн `#include <...>` толгой файлууд."""
    headers: set[str] = set()
    for line in _COMMENTS.sub(" ", source).splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        match = _SYSTEM_INCLUDE.fullmatch(stripped)
        if match is None:
            break
        headers.add(match.group(1))
    return frozenset(headers)


def select(headers: frozenset[str]) -> frozenset[str] | None:
    """Сурагчийн толгой файлуудад БҮРЭН багтах хамгийн том PCH."""
    best: frozenset[str] | None = None
    for candidate in PCH_SETS:
        if candidate <= headers and (best is None or len(candidate) > len(best)):
            best = candidate
    return best


def header_name(headers: frozenset[str]) -> str:
    return "-".join(sorted(headers)) + ".h"


def header_text(headers: frozenset[str]) -> str:
    return "".join(f"#include <{header}>\n" for header in sorted(headers))


def pch_path(directory: Path, headers: frozenset[str]) -> Path:
    return directory / (header_name(headers) + ".pch")
