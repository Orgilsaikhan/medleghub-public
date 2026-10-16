"""Тестийн файлуудыг кодоор бүтээнэ — repo-д хоёртын fixture байхгүй.

• PDF: гараар бичсэн, Type0 фонт + ToUnicode CMap-тай (кирилл текст
  фонтын файлгүйгээр зөв задарна). Хүсвэл RC4 40 битээр нууцална.
• PPTX, DOCX: `zipfile` + хамгийн бага XML.
• OLE: MS-CFB-ийн хамгийн бага сав (толгой, FAT, directory).
"""

import hashlib
import io
import struct
import zipfile
from xml.sax.saxutils import escape

# --- PDF ------------------------------------------------------------------------

_PAD = bytes.fromhex("28BF4E5E4E758A4164004E56FFFA01082E2E00B6D0683E802F0CA9FE6453697A")


def _rc4(key: bytes, data: bytes) -> bytes:
    state = list(range(256))
    j = 0
    for i in range(256):
        j = (j + state[i] + key[i % len(key)]) % 256
        state[i], state[j] = state[j], state[i]
    out = bytearray()
    i = j = 0
    for byte in data:
        i = (i + 1) % 256
        j = (j + state[i]) % 256
        state[i], state[j] = state[j], state[i]
        out.append(byte ^ state[(state[i] + state[j]) % 256])
    return bytes(out)


def _to_unicode_cmap(codes: dict[str, int]) -> bytes:
    lines = [
        "/CIDInit /ProcSet findresource begin",
        "12 dict begin",
        "begincmap",
        "/CMapName /MedlegTest def",
        "/CMapType 2 def",
        "1 begincodespacerange",
        "<0000> <FFFF>",
        "endcodespacerange",
    ]
    items = list(codes.items())
    for start in range(0, len(items), 100):
        chunk = items[start : start + 100]
        lines.append(f"{len(chunk)} beginbfchar")
        lines.extend(
            f"<{code:04X}> <{char.encode('utf-16-be').hex().upper()}>" for char, code in chunk
        )
        lines.append("endbfchar")
    lines += ["endcmap", "CMapName currentdict /CMap defineresource pop", "end", "end"]
    return "\n".join(lines).encode()


def make_pdf(pages: list[list[str]], user_password: str | None = None) -> bytes:
    """Хуудас бүр мөрүүдийн жагсаалт. `user_password` өгвөл унших нууц үгтэй."""
    chars = sorted({char for page in pages for line in page for char in line})
    codes = {char: index + 1 for index, char in enumerate(chars)}
    objects: dict[int, bytes | tuple[bytes]] = {}
    kids = [7 + 2 * index for index in range(len(pages))]
    objects[1] = b"<< /Type /Catalog /Pages 2 0 R >>"
    objects[2] = b"<< /Type /Pages /Kids [%s] /Count %d >>" % (
        b" ".join(b"%d 0 R" % kid for kid in kids),
        len(pages),
    )
    objects[3] = (
        b"<< /Type /Font /Subtype /Type0 /BaseFont /MedlegTest /Encoding /Identity-H"
        b" /DescendantFonts [4 0 R] /ToUnicode 5 0 R >>"
    )
    objects[4] = (
        b"<< /Type /Font /Subtype /CIDFontType2 /BaseFont /MedlegTest"
        b" /CIDSystemInfo << /Registry (Adobe) /Ordering (Identity) /Supplement 0 >>"
        b" /FontDescriptor 6 0 R /DW 600 /CIDToGIDMap /Identity >>"
    )
    objects[5] = (_to_unicode_cmap(codes),)
    objects[6] = (
        b"<< /Type /FontDescriptor /FontName /MedlegTest /Flags 32"
        b" /FontBBox [0 -200 1000 900] /ItalicAngle 0 /Ascent 900 /Descent -200"
        b" /CapHeight 700 /StemV 80 >>"
    )
    for index, lines in enumerate(pages):
        page_id, content_id = 7 + 2 * index, 8 + 2 * index
        objects[page_id] = (
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792]"
            b" /Resources << /Font << /F1 3 0 R >> >> /Contents %d 0 R >>" % content_id
        )
        operators = [b"BT", b"/F1 12 Tf", b"14 TL", b"50 740 Td"]
        for line in lines:
            hexed = "".join(f"{codes[char]:04X}" for char in line).encode()
            operators.append(b"<%s> Tj T*" % hexed)
        operators.append(b"ET")
        objects[content_id] = (b"\n".join(operators),)

    file_id = hashlib.md5(b"medleghub-extractor-test").digest()
    key = None
    encrypt_id = None
    if user_password is not None:
        # PDF 1.4-ийн Standard security handler, V1 R2 (RC4, 40 бит).
        permissions = -44
        owner_key = hashlib.md5((b"owner" + _PAD)[:32]).digest()[:5]
        owner = _rc4(owner_key, (user_password.encode() + _PAD)[:32])
        key = hashlib.md5(
            (user_password.encode() + _PAD)[:32] + owner + struct.pack("<i", permissions) + file_id
        ).digest()[:5]
        user = _rc4(key, _PAD)
        encrypt_id = max(objects) + 1
        objects[encrypt_id] = b"<< /Filter /Standard /V 1 /R 2 /O <%s> /U <%s> /P %d >>" % (
            owner.hex().encode(),
            user.hex().encode(),
            permissions,
        )

    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = {}
    for number in sorted(objects):
        offsets[number] = len(out)
        body = objects[number]
        out += b"%d 0 obj\n" % number
        if isinstance(body, tuple):
            data = body[0]
            if key is not None:
                object_key = hashlib.md5(key + struct.pack("<I", number)[:3] + b"\0\0").digest()
                data = _rc4(object_key[:10], data)
            out += b"<< /Length %d >>\nstream\n%s\nendstream" % (len(data), data)
        else:
            out += body
        out += b"\nendobj\n"
    xref = len(out)
    size = max(objects) + 1
    out += b"xref\n0 %d\n0000000000 65535 f \n" % size
    for number in range(1, size):
        out += b"%010d 00000 n \n" % offsets[number]
    trailer = b"<< /Size %d /Root 1 0 R /ID [<%s> <%s>]" % (
        size,
        file_id.hex().encode(),
        file_id.hex().encode(),
    )
    if encrypt_id is not None:
        trailer += b" /Encrypt %d 0 R" % encrypt_id
    out += b"trailer\n%s >>\nstartxref\n%d\n%%%%EOF\n" % (trailer, xref)
    return bytes(out)


# --- OOXML ----------------------------------------------------------------------

NS_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_PKG_REL = "http://schemas.openxmlformats.org/package/2006/relationships"
NS_A = "http://schemas.openxmlformats.org/drawingml/2006/main"
NS_P = "http://schemas.openxmlformats.org/presentationml/2006/main"
NS_W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS_MC = "http://schemas.openxmlformats.org/markup-compatibility/2006"

PPTX_MAIN = "application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"
PPTM_MAIN = "application/vnd.ms-powerpoint.presentation.macroEnabled.main+xml"
DOCX_MAIN = "application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"
DOCM_MAIN = "application/vnd.ms-word.document.macroEnabled.main+xml"

REL_OFFICE = f"{NS_REL}/officeDocument"
REL_SLIDE = f"{NS_REL}/slide"
REL_NOTES = f"{NS_REL}/notesSlide"
REL_STYLES = f"{NS_REL}/styles"


def _content_types(overrides: dict[str, str]) -> str:
    items = "".join(
        f'<Override PartName="{name}" ContentType="{kind}"/>' for name, kind in overrides.items()
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" '
        'ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        f"{items}</Types>"
    )


def _rels(items: list[tuple[str, str, str]]) -> str:
    body = "".join(
        f'<Relationship Id="{rid}" Type="{kind}" Target="{target}"/>' for rid, kind, target in items
    )
    return (
        f'<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="{NS_PKG_REL}">'
        f"{body}</Relationships>"
    )


def zip_bytes(files: dict[str, str | bytes], extra_entries: int = 0) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, content in files.items():
            archive.writestr(name, content.encode() if isinstance(content, str) else content)
        for index in range(extra_entries):
            archive.writestr(f"customXml/item{index}.xml", "<x/>")
    return buffer.getvalue()


def set_declared_size(data: bytes, name: str, size: int) -> bytes:
    """ZIP-ийн central directory-д `name`-ийн задарсан хэмжээг худлаа бичнэ."""
    out = bytearray(data)
    target = name.encode()
    offset = out.find(b"PK\x01\x02")
    while offset != -1:
        name_length = struct.unpack_from("<H", out, offset + 28)[0]
        if bytes(out[offset + 46 : offset + 46 + name_length]) == target:
            struct.pack_into("<I", out, offset + 24, size)
            return bytes(out)
        offset = out.find(b"PK\x01\x02", offset + 46)
    raise KeyError(name)


# PPTX: shape-ууд


def run_text(text: str) -> str:
    return f'<a:r><a:rPr lang="mn-MN"/><a:t>{escape(text)}</a:t></a:r>'


def paragraphs(*lines: str, split: bool = False) -> str:
    """`split` бол үг бүр тусдаа run (PowerPoint ингэж хадгалдаг)."""
    out = []
    for line in lines:
        words = line.split(" ") if split else [line]
        runs = "".join(
            run_text(word + (" " if index < len(words) - 1 else ""))
            for index, word in enumerate(words)
        )
        out.append(f"<a:p>{runs}</a:p>")
    return "".join(out)


def shape(*lines: str, placeholder: str | None = None, split: bool = False) -> str:
    ph = f'<p:ph type="{placeholder}"/>' if placeholder else ""
    return (
        '<p:sp><p:nvSpPr><p:cNvPr id="2" name="Shape"/><p:cNvSpPr/>'
        f"<p:nvPr>{ph}</p:nvPr></p:nvSpPr>"
        f"<p:spPr/><p:txBody><a:bodyPr/><a:lstStyle/>{paragraphs(*lines, split=split)}"
        "</p:txBody></p:sp>"
    )


def group(*shapes: str) -> str:
    return (
        '<p:grpSp><p:nvGrpSpPr><p:cNvPr id="9" name="Group"/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
        f"<p:grpSpPr/>{''.join(shapes)}</p:grpSp>"
    )


def table(rows: list[list[str]]) -> str:
    cells = "".join(
        '<a:tr h="370840">'
        + "".join(
            f"<a:tc><a:txBody><a:bodyPr/>{paragraphs(cell)}</a:txBody></a:tc>" for cell in row
        )
        + "</a:tr>"
        for row in rows
    )
    return (
        '<p:graphicFrame><p:nvGraphicFramePr><p:cNvPr id="5" name="Table"/><p:cNvGraphicFramePr/>'
        "<p:nvPr/></p:nvGraphicFramePr><p:xfrm/><a:graphic>"
        '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/table">'
        f"<a:tbl><a:tblGrid/>{cells}</a:tbl></a:graphicData></a:graphic></p:graphicFrame>"
    )


def _slide_xml(shapes: list[str]) -> str:
    return (
        f'<?xml version="1.0" encoding="UTF-8"?><p:sld xmlns:a="{NS_A}" xmlns:p="{NS_P}" '
        f'xmlns:r="{NS_REL}" xmlns:mc="{NS_MC}"><p:cSld><p:spTree>'
        '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/>'
        f"{''.join(shapes)}</p:spTree></p:cSld></p:sld>"
    )


def _notes_xml(lines: list[str]) -> str:
    return (
        f'<?xml version="1.0" encoding="UTF-8"?><p:notes xmlns:a="{NS_A}" xmlns:p="{NS_P}" '
        f'xmlns:r="{NS_REL}"><p:cSld><p:spTree>'
        '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/>'
        f"{shape(placeholder='sldImg')}{shape(*lines, placeholder='body')}"
        f"{shape('7', placeholder='sldNum')}</p:spTree></p:cSld></p:notes>"
    )


def make_pptx(
    slides: list[list[str]],
    *,
    notes: dict[int, list[str]] | None = None,
    order: list[int] | None = None,
    main_type: str = PPTX_MAIN,
    extra_files: dict[str, str | bytes] | None = None,
    extra_entries: int = 0,
) -> bytes:
    """`slides[i]` нь `slideN.xml` (N = i + 1)-ийн shape-ууд. `order` нь илтгэлийн дараалал."""
    notes = notes or {}
    order = order if order is not None else list(range(len(slides)))
    overrides = {"/ppt/presentation.xml": main_type}
    files: dict[str, str | bytes] = {
        "_rels/.rels": _rels([("rId1", REL_OFFICE, "ppt/presentation.xml")]),
    }
    presentation_rels = []
    for index, shapes in enumerate(slides):
        number = index + 1
        files[f"ppt/slides/slide{number}.xml"] = _slide_xml(shapes)
        overrides[f"/ppt/slides/slide{number}.xml"] = (
            "application/vnd.openxmlformats-officedocument.presentationml.slide+xml"
        )
        presentation_rels.append((f"rId{100 + number}", REL_SLIDE, f"slides/slide{number}.xml"))
        if index in notes:
            files[f"ppt/notesSlides/notesSlide{number}.xml"] = _notes_xml(notes[index])
            files[f"ppt/slides/_rels/slide{number}.xml.rels"] = _rels(
                [("rId2", REL_NOTES, f"../notesSlides/notesSlide{number}.xml")]
            )
    ids = "".join(
        f'<p:sldId id="{256 + i}" r:id="rId{100 + index + 1}"/>' for i, index in enumerate(order)
    )
    files["ppt/presentation.xml"] = (
        f'<?xml version="1.0" encoding="UTF-8"?><p:presentation xmlns:a="{NS_A}" xmlns:p="{NS_P}" '
        f'xmlns:r="{NS_REL}"><p:sldIdLst>{ids}</p:sldIdLst></p:presentation>'
    )
    files["ppt/_rels/presentation.xml.rels"] = _rels(presentation_rels)
    files["[Content_Types].xml"] = _content_types(overrides)
    files.update(extra_files or {})
    return zip_bytes(files, extra_entries)


# DOCX


def para(text: str, style: str | None = None, *, split: bool = False) -> str:
    """Догол мөр. `split` бол үг бүр тусдаа run (Word ингэж хадгалдаг)."""
    properties = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ""
    words = text.split(" ") if split else [text]
    runs = "".join(
        f'<w:r><w:rPr><w:lang w:val="mn-MN"/></w:rPr><w:t xml:space="preserve">'
        f"{escape(word)}{' ' if split and i < len(words) - 1 else ''}</w:t></w:r>"
        for i, word in enumerate(words)
    )
    return f"<w:p>{properties}{runs}</w:p>"


def word_table(rows: list[list[str]]) -> str:
    return (
        "<w:tbl><w:tblPr/>"
        + "".join(
            "<w:tr>" + "".join(f"<w:tc>{para(cell)}</w:tc>" for cell in row) + "</w:tr>"
            for row in rows
        )
        + "</w:tbl>"
    )


DEFAULT_STYLES = (
    f'<?xml version="1.0" encoding="UTF-8"?><w:styles xmlns:w="{NS_W}">'
    # Орос/монгол Word: id нь «1», нэр нь «heading 1».
    '<w:style w:type="paragraph" w:styleId="1"><w:name w:val="heading 1"/>'
    '<w:pPr><w:outlineLvl w:val="0"/></w:pPr></w:style>'
    '<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/>'
    '<w:pPr><w:outlineLvl w:val="2"/></w:pPr></w:style>'
    "</w:styles>"
)


def make_docx(
    body: list[str],
    *,
    main_type: str = DOCX_MAIN,
    styles: str | None = DEFAULT_STYLES,
    extra_files: dict[str, str | bytes] | None = None,
    extra_entries: int = 0,
) -> bytes:
    overrides = {"/word/document.xml": main_type}
    files: dict[str, str | bytes] = {
        "_rels/.rels": _rels([("rId1", REL_OFFICE, "word/document.xml")]),
        "word/document.xml": (
            f'<?xml version="1.0" encoding="UTF-8"?><w:document xmlns:w="{NS_W}" '
            f'xmlns:r="{NS_REL}" xmlns:mc="{NS_MC}"><w:body>{"".join(body)}'
            "<w:sectPr/></w:body></w:document>"
        ),
    }
    if styles is not None:
        files["word/styles.xml"] = styles
        files["word/_rels/document.xml.rels"] = _rels([("rId1", REL_STYLES, "styles.xml")])
        overrides["/word/styles.xml"] = (
            "application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"
        )
    files["[Content_Types].xml"] = _content_types(overrides)
    files.update(extra_files or {})
    return zip_bytes(files, extra_entries)


# --- OLE (MS-CFB) ------------------------------------------------------------------

OLE_MAGIC = bytes.fromhex("D0CF11E0A1B11AE1")
_FREE, _END, _FATSECT, _NOSTREAM = 0xFFFFFFFF, 0xFFFFFFFE, 0xFFFFFFFD, 0xFFFFFFFF


def _directory_entry(name: str, kind: int) -> bytes:
    entry = bytearray(128)
    encoded = name.encode("utf-16-le") + b"\0\0"
    entry[: len(encoded)] = encoded
    struct.pack_into("<HBB", entry, 64, len(encoded), kind, 1)
    struct.pack_into("<III", entry, 68, _NOSTREAM, _NOSTREAM, _NOSTREAM)
    struct.pack_into("<I", entry, 116, _END)
    return bytes(entry)


def make_ole(stream_names: list[str]) -> bytes:
    """Хоосон stream-үүдтэй хамгийн бага OLE файл (512 байтын sector, v3)."""
    assert len(stream_names) <= 3
    header = bytearray(512)
    header[:8] = OLE_MAGIC
    struct.pack_into("<HHHHH", header, 24, 0x3E, 3, 0xFFFE, 9, 6)
    struct.pack_into("<IIII", header, 44, 1, 1, 0, 4096)  # FAT sector-ийн тоо, directory, …
    struct.pack_into("<IIII", header, 60, _END, 0, _END, 0)
    struct.pack_into("<109I", header, 76, 0, *([_FREE] * 108))
    fat = struct.pack("<128I", _FATSECT, _END, *([_FREE] * 126))
    directory = _directory_entry("Root Entry", 5) + b"".join(
        _directory_entry(name, 2) for name in stream_names
    )
    return bytes(header) + fat + directory.ljust(512, b"\0")
