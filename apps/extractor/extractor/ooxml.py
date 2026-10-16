"""PPTX, DOCX (Office Open XML)-ээс текст задлах.

Файл нь ZIP багц. Оролтод итгэхгүй тул:
  • ZIP-ийн бичлэгийн тоо, задарсан нийт хэмжээ, хэрэгтэй XML хэсэг бүрийн
    хэмжээг хязгаарлана (zip bomb). Толгойн хэмжээнд сохроор итгэхгүй —
    хэсэгчлэн уншиж, хязгаарт хүрмэгц зогсооно.
  • XML-ийг зөвхөн defusedxml-ээр задална: DTD, entity хориотой.
  • Зөвхөн хэрэгтэй хэсгүүдийг уншина (толгой, хөл, тайлбар, зураг — үгүй).
  • Макротой багц (`.pptm`, `.docm`, `vbaProject.bin`) татгалзана.

Элементийг namespace-гүй, зөвхөн локал нэрээр нь таньдаг — ISO «Strict»
OOXML (өөр namespace) ч ижил задарна.
"""

import posixpath
import struct
import zipfile
from collections.abc import Iterator
from typing import Any
from urllib.parse import unquote
from xml.etree.ElementTree import Element, ParseError

from defusedxml import DefusedXmlException
from defusedxml.ElementTree import fromstring

from extractor.document import ExtractError, Page, build_result, normalize, title_of
from extractor.settings import Settings

# OLE compound file (хуучин .doc/.ppt болон нууц үгтэй Office файлын сав).
OLE_MAGIC = bytes.fromhex("D0CF11E0A1B11AE1")
ZIP_MAGIC = b"PK\x03\x04"

_PML = "application/vnd.openxmlformats-officedocument.presentationml"
_WML = "application/vnd.openxmlformats-officedocument.wordprocessingml"
MAIN_CONTENT_TYPES = {
    "pptx": frozenset(
        {
            f"{_PML}.presentation.main+xml",
            f"{_PML}.slideshow.main+xml",  # .ppsx
            f"{_PML}.template.main+xml",  # .potx
        }
    ),
    "docx": frozenset(
        {
            f"{_WML}.document.main+xml",
            f"{_WML}.template.main+xml",  # .dotx
        }
    ),
}

NOTES_PREFIX = "Тэмдэглэл: "
_TITLE_PLACEHOLDERS = frozenset({"title", "ctrTitle"})
# Догол мөр, run-ийн тохиргоо (таб зогсоол гэх мэт); засвар хянах горимд устгасан,
# зөөсөн текст (эцсийн хувилбарт байхгүй); талбарын код; `mc:Fallback` (Choice-г уншсан).
_WORD_SKIP = frozenset({"pPr", "rPr", "del", "moveFrom", "instrText", "delText", "Fallback"})


def _local(tag: object) -> str:
    return tag.rsplit("}", 1)[-1] if isinstance(tag, str) else ""


def _children(element: Element, name: str) -> Iterator[Element]:
    return (child for child in element if _local(child.tag) == name)


def _first(element: Element, *path: str) -> Element | None:
    current: Element | None = element
    for name in path:
        if current is None:
            return None
        current = next(_children(current, name), None)
    return current


def _attr(element: Element, name: str) -> str | None:
    """Namespace-тэй атрибут (`w:val`, `r:id`) — локал нэрээр нь."""
    for key, value in element.attrib.items():
        if key.startswith("{") and _local(key) == name:
            return value
    return None


# --- OLE --------------------------------------------------------------------

_MAXREGSECT = 0xFFFFFFFA


def _ole_entry_names(data: bytes) -> set[str]:
    """OLE (MS-CFB) файлын directory-ийн бүх stream, storage-ийн нэр (жижиг үсгээр).

    Мод бүтцийг дагалгүй directory-ийн sector-уудыг дараалан уншина.
    Бүтэц эвдэрсэн бол ValueError, struct.error.
    """
    shift = struct.unpack_from("<H", data, 30)[0]
    if shift not in (9, 12):
        raise ValueError("sector size")
    size = 1 << shift
    total_sectors = max(0, len(data) // size - 1)

    def sector(index: int) -> bytes:
        if index >= total_sectors:
            raise ValueError("sector out of range")
        start = (index + 1) * size
        return data[start : start + size]

    fat_count, first_dir = struct.unpack_from("<II", data, 44)
    next_difat, difat_count = struct.unpack_from("<II", data, 68)
    fat_sectors = list(struct.unpack_from("<109I", data, 76))
    per_sector = size // 4
    seen: set[int] = set()
    while next_difat <= _MAXREGSECT and difat_count > 0 and next_difat not in seen:
        seen.add(next_difat)
        block = struct.unpack(f"<{per_sector}I", sector(next_difat))
        fat_sectors.extend(block[:-1])
        next_difat = block[-1]
        difat_count -= 1
    fat: list[int] = []
    for index in [s for s in fat_sectors if s <= _MAXREGSECT][:fat_count]:
        fat.extend(struct.unpack(f"<{per_sector}I", sector(index)))

    names: set[str] = set()
    current = first_dir
    visited: set[int] = set()
    while current <= _MAXREGSECT and current not in visited:
        visited.add(current)
        block = sector(current)
        for offset in range(0, size, 128):
            length = struct.unpack_from("<H", block, offset + 64)[0]
            kind = block[offset + 66]
            if kind in (1, 2, 5) and 2 <= length <= 64:
                raw = block[offset : offset + length - 2]
                names.add(raw.decode("utf-16-le", errors="replace").lower())
        current = fat[current] if current < len(fat) else _MAXREGSECT + 1
    return names


def ole_error(path: str) -> str:
    """OLE файл: нууц үгтэй OOXML бол `encrypted`, бусад нь (.doc/.ppt) `legacy_format`.

    Нууц үгтэй Office файл нь OLE сав дотор `EncryptionInfo` ба
    `EncryptedPackage` stream-тэй байдаг (MS-OFFCRYPTO). Directory-г уншиж
    чадахгүй бол `legacy_format`.
    """
    with open(path, "rb") as file:
        data = file.read()
    try:
        names = _ole_entry_names(data)
    except (ValueError, struct.error, IndexError):
        return "legacy_format"
    if {"encryptedpackage", "encryptioninfo"} <= names:
        return "encrypted"
    return "legacy_format"


# --- ZIP багц -----------------------------------------------------------------


class Package:
    """Хязгаартай уншдаг OOXML багц."""

    def __init__(self, path: str, settings: Settings) -> None:
        with open(path, "rb") as file:
            head = file.read(len(OLE_MAGIC))
        if head == OLE_MAGIC:
            raise ExtractError(ole_error(path))
        if not head.startswith(ZIP_MAGIC):
            raise ExtractError("corrupt", detail="magic")
        try:
            self._zip = zipfile.ZipFile(path)
        except (zipfile.BadZipFile, zipfile.LargeZipFile, ValueError, EOFError, OSError):
            raise ExtractError("corrupt", detail="zip") from None
        try:
            infos = self._zip.infolist()
            if len(infos) > settings.max_zip_entries:
                raise ExtractError("corrupt", detail="zip_entries")
            if sum(info.file_size for info in infos) > settings.max_zip_bytes:
                raise ExtractError("corrupt", detail="zip_size")
        except BaseException:
            self._zip.close()
            raise
        # OPC-ийн хэсгийн нэр том жижиг үсэг ялгадаггүй.
        self._parts: dict[str, zipfile.ZipInfo] = {}
        for info in infos:
            self._parts.setdefault(info.filename.lower(), info)
        self._settings = settings
        self._read_bytes = 0
        self._content_types: tuple[dict[str, str], dict[str, str]] | None = None

    def __enter__(self) -> "Package":
        return self

    def __exit__(self, *_: object) -> None:
        self._zip.close()

    def names(self) -> Iterator[str]:
        return iter(self._parts)

    def read(self, name: str) -> bytes | None:
        """Хэсгийг хязгаартай уншина. Байхгүй бол None."""
        info = self._parts.get(name.lower())
        if info is None:
            return None
        limit = self._settings.max_part_bytes
        if info.file_size > limit:
            raise ExtractError("corrupt", detail="part_size")
        chunks: list[bytes] = []
        size = 0
        try:
            with self._zip.open(info) as stream:
                while chunk := stream.read(64 * 1024):
                    size += len(chunk)
                    if size > limit or self._read_bytes + size > self._settings.max_zip_bytes:
                        raise ExtractError("corrupt", detail="part_size")
                    chunks.append(chunk)
        except ExtractError:
            raise
        except (zipfile.BadZipFile, RuntimeError, NotImplementedError, EOFError, OSError):
            # CRC алдаа, ZIP-ийн нууц үг, дэмжигдээгүй шахалт гэх мэт.
            raise ExtractError("corrupt", detail="zip_entry") from None
        self._read_bytes += size
        return b"".join(chunks)

    def xml(self, name: str) -> Element | None:
        data = self.read(name)
        if data is None:
            return None
        try:
            return fromstring(data, forbid_dtd=True, forbid_entities=True, forbid_external=True)
        except (ParseError, DefusedXmlException, ValueError):
            raise ExtractError("corrupt", detail="xml") from None

    def relationships(self, part: str) -> list[tuple[str, str, str]]:
        """`part`-ийн дотоод холбоосууд: (Id, Type, зорилтот хэсэг)."""
        base, name = posixpath.split(part)
        root = self.xml(posixpath.join(base, "_rels", f"{name}.rels"))
        if root is None:
            return []
        found = []
        for rel in _children(root, "Relationship"):
            if (rel.get("TargetMode") or "").lower() == "external":
                continue
            target = _resolve(base, rel.get("Target") or "")
            if target:
                found.append((rel.get("Id") or "", rel.get("Type") or "", target))
        return found

    def content_type(self, part: str) -> str:
        if self._content_types is None:
            root = self.xml("[Content_Types].xml")
            if root is None:
                raise ExtractError("corrupt", detail="content_types")
            overrides, defaults = {}, {}
            for item in root:
                if _local(item.tag) == "Override":
                    overrides[(item.get("PartName") or "").lstrip("/").lower()] = (
                        item.get("ContentType") or ""
                    )
                elif _local(item.tag) == "Default":
                    defaults[(item.get("Extension") or "").lower()] = item.get("ContentType") or ""
            self._content_types = (overrides, defaults)
        overrides, defaults = self._content_types
        if part.lower() in overrides:
            return overrides[part.lower()]
        return defaults.get(posixpath.splitext(part)[1].lstrip(".").lower(), "")

    def main_part(self, kind: str) -> str:
        """Үндсэн хэсэг (`ppt/presentation.xml`, `word/document.xml`)-ийг шалгаж буцаана."""
        if any(name.endswith("vbaproject.bin") for name in self.names()):
            raise ExtractError("macro_enabled")
        main = next(
            (
                target
                for _, rel_type, target in self.relationships("")
                if rel_type.endswith("/officeDocument")
            ),
            None,
        )
        if main is None:
            raise ExtractError("corrupt", detail="no_main_part")
        content_type = self.content_type(main)
        if "macroenabled" in content_type.lower():
            raise ExtractError("macro_enabled")
        if content_type not in MAIN_CONTENT_TYPES[kind]:
            raise ExtractError("corrupt", detail="content_type")
        return main


def _resolve(base: str, target: str) -> str | None:
    target = unquote(target.split("#", 1)[0])
    if not target:
        return None
    path = target.lstrip("/") if target.startswith("/") else posixpath.join(base, target)
    path = posixpath.normpath(path)
    if path == "." or path == ".." or path.startswith("../"):
        return None
    return path


# --- PPTX -----------------------------------------------------------------------


def _placeholder_type(shape: Element) -> str | None:
    """`p:nvSpPr/p:nvPr/p:ph`-ийн төрөл. Төрөлгүй placeholder нь `obj`."""
    placeholder = _first(shape, "nvSpPr", "nvPr", "ph")
    return None if placeholder is None else placeholder.get("type", "obj")


def _drawing_text(element: Element, parts: list[str]) -> None:
    for child in element:
        name = _local(child.tag)
        if name == "Fallback":
            # `mc:AlternateContent`-ийн Choice-г (жишээ нь томьёо) аль хэдийн уншсан.
            continue
        if name == "t":
            parts.append(child.text or "")
        elif name == "br":
            parts.append("\n")
        else:
            _drawing_text(child, parts)


def _drawing_paragraphs(element: Element, in_title: bool = False) -> Iterator[tuple[bool, str]]:
    """Слайдын `a:p` бүр баримтын дарааллаар: хэлбэр, бүлэг, хүснэгтийн нүд."""
    for child in element:
        name = _local(child.tag)
        if name == "Fallback":
            continue
        if name == "sp":
            yield from _drawing_paragraphs(
                child, in_title or _placeholder_type(child) in _TITLE_PLACEHOLDERS
            )
        elif name == "p":
            parts: list[str] = []
            _drawing_text(child, parts)
            yield in_title, "".join(parts)
        else:
            yield from _drawing_paragraphs(child, in_title)


def _notes_text(package: Package, slide_part: str) -> str:
    for _, rel_type, target in package.relationships(slide_part):
        if not rel_type.endswith("/notesSlide"):
            continue
        root = package.xml(target)
        if root is None:
            return ""
        lines = []
        # Зөвхөн тэмдэглэлийн body — слайдын зураг, дугаар, огноо, толгой биш.
        for shape in root.iter():
            if _local(shape.tag) == "sp" and _placeholder_type(shape) == "body":
                lines.extend(text for _, text in _drawing_paragraphs(shape))
        return normalize("\n".join(lines))
    return ""


def _slide(package: Package, part: str | None) -> Page:
    root = package.xml(part) if part else None
    if root is None:
        return Page(None, "")
    tree = _first(root, "cSld", "spTree")
    lines: list[str] = []
    title_lines: list[str] = []
    for in_title, text in _drawing_paragraphs(tree) if tree is not None else ():
        lines.append(text)
        if in_title:
            title_lines.append(text)
    text = normalize("\n".join(lines))
    notes = _notes_text(package, part) if part else ""
    if notes:
        text = f"{text}\n{NOTES_PREFIX}{notes}" if text else f"{NOTES_PREFIX}{notes}"
    return Page(title_of(normalize("\n".join(title_lines))), text)


def extract_pptx(path: str, settings: Settings) -> dict[str, Any]:
    with Package(path, settings) as package:
        main = package.main_part("pptx")
        presentation = package.xml(main)
        if presentation is None:
            raise ExtractError("corrupt", detail="no_main_part")
        targets = {rel_id: target for rel_id, _, target in package.relationships(main)}
        slide_list = _first(presentation, "sldIdLst")
        # Файлын нэрээр биш, илтгэлийн дарааллаар (`p:sldIdLst`).
        slides = [
            targets.get(_attr(item, "id") or "")
            for item in (_children(slide_list, "sldId") if slide_list is not None else ())
        ]
        if len(slides) > settings.max_pages:
            raise ExtractError("too_many_pages", page_count=len(slides))
        pages = [_slide(package, part) for part in slides]
    return build_result("pptx", pages, settings.max_text_chars)


# --- DOCX -----------------------------------------------------------------------


def _heading_styles(package: Package, main: str) -> set[str]:
    """Гарчгийн загварын id-ууд `styles.xml`-ээс.

    Орос, монгол Word-д загварын id нь `Heading1` биш (`1`, `a3` гэх мэт),
    харин нэр нь үргэлж англиар («heading 1»). Outline level 0–1 ч гарчиг.
    """
    styles_part = next(
        (
            target
            for _, rel_type, target in package.relationships(main)
            if rel_type.endswith("/styles")
        ),
        None,
    )
    root = package.xml(styles_part) if styles_part else None
    if root is None:
        return set()
    found = set()
    for style in _children(root, "style"):
        style_id = _attr(style, "styleId")
        if not style_id or _attr(style, "type") not in (None, "paragraph"):
            continue
        name_element = _first(style, "name")
        name = (_attr(name_element, "val") or "").lower() if name_element is not None else ""
        outline = _first(style, "pPr", "outlineLvl")
        level = _attr(outline, "val") if outline is not None else None
        if name in ("heading 1", "heading 2", "title") or level in ("0", "1"):
            found.add(style_id)
    return found


def _word_text(element: Element, parts: list[str], nested: list[Element]) -> None:
    for child in element:
        name = _local(child.tag)
        if name in _WORD_SKIP:
            continue
        if name == "t":
            parts.append(child.text or "")
        elif name == "tab":
            parts.append("\t")
        elif name in ("br", "cr"):
            parts.append("\n")
        elif name == "noBreakHyphen":
            parts.append("-")
        elif name in ("txbxContent", "p"):
            # Текст хайрцгийн доторх догол мөрүүд — энэ догол мөрийн дараа тусад нь.
            nested.append(child)
        else:
            _word_text(child, parts, nested)


def _word_paragraph(paragraph: Element) -> Iterator[tuple[str | None, str | None, str]]:
    style = outline = None
    properties = _first(paragraph, "pPr")
    if properties is not None:
        style_element = _first(properties, "pStyle")
        style = _attr(style_element, "val") if style_element is not None else None
        outline_element = _first(properties, "outlineLvl")
        outline = _attr(outline_element, "val") if outline_element is not None else None
    parts: list[str] = []
    nested: list[Element] = []
    _word_text(paragraph, parts, nested)
    yield style, outline, "".join(parts)
    for inner in nested:
        if _local(inner.tag) == "p":
            yield from _word_paragraph(inner)
        else:
            yield from _word_paragraphs(inner)


def _word_paragraphs(element: Element) -> Iterator[tuple[str | None, str | None, str]]:
    """Биеийн догол мөр бүр баримтын дарааллаар: хүснэгтийн нүд, content control."""
    for child in element:
        name = _local(child.tag)
        if name in ("Fallback", "sectPr"):
            continue
        if name == "p":
            yield from _word_paragraph(child)
        else:
            yield from _word_paragraphs(child)


def _split_long(text: str, limit: int) -> Iterator[str]:
    """Хэт урт догол мөрийг зайгаар нь ~`limit` тэмдэгтийн хэсгүүдэд хуваана."""
    while len(text) > limit:
        cut = max(text.rfind(" ", 0, limit), text.rfind("\n", 0, limit))
        if cut < limit // 2:
            cut = limit
        yield text[:cut].rstrip()
        text = text[cut:].lstrip()
    if text:
        yield text


def _is_heading(style: str | None, outline: str | None, heading_styles: set[str]) -> bool:
    if style and (
        style.startswith(("Heading1", "Heading2")) or style == "Title" or style in heading_styles
    ):
        return True
    return outline in ("0", "1")


def extract_docx(path: str, settings: Settings) -> dict[str, Any]:
    with Package(path, settings) as package:
        main = package.main_part("docx")
        document = package.xml(main)
        body = _first(document, "body") if document is not None else None
        if body is None:
            raise ExtractError("corrupt", detail="no_body")
        heading_styles = _heading_styles(package, main)

        pages: list[Page] = []
        title: str | None = None
        lines: list[str] = []
        length = 0

        def flush() -> None:
            if lines:
                pages.append(Page(title, normalize("\n".join(lines))))

        for style, outline, raw in _word_paragraphs(body):
            text = normalize(raw)
            if not text:
                continue
            if _is_heading(style, outline, heading_styles):
                flush()
                title = title_of(text)
                lines, length = [text], len(text)
                continue
            for piece in _split_long(text, settings.section_chars):
                has_body = len(lines) > (1 if title else 0)
                if has_body and length + len(piece) > settings.section_chars:
                    flush()
                    title, lines, length = None, [], 0
                lines.append(piece)
                length += len(piece) + 1
        flush()

    if len(pages) > settings.max_pages:
        raise ExtractError("too_many_pages", page_count=len(pages))
    return build_result("docx", pages, settings.max_text_chars)
