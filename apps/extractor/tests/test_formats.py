"""Задлагчийн дүрмүүд — дэд процессгүй, шууд функцээр."""

from pathlib import Path

import pypdfium2 as pdfium
import pytest

from extractor.document import ExtractError, Page, build_result, normalize
from extractor.ooxml import _split_long, extract_docx, extract_pptx
from extractor.pdf import extract_pdf
from extractor.settings import Settings
from tests import builders


@pytest.fixture
def config() -> Settings:
    return Settings()


def write(tmp_path: Path, name: str, data: bytes) -> str:
    path = tmp_path / name
    path.write_bytes(data)
    return str(path)


# --- Текст ------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("  Сайн   байна\tуу  ", "Сайн байна уу"),
        ("мөр 1\r\nмөр 2\rмөр 3", "мөр 1\nмөр 2\nмөр 3"),
        ("\n\nнэг\n\n\n\nхоёр\n \n\t\nгурав\n\n", "нэг\n\nхоёр\n\nгурав"),
        ("NUL\x00 тэмдэгт\x07", "NUL тэмдэгт"),
        ("өргөн зай　энд", "өргөн зай энд"),
        ("ганц\ud800surrogate", "ганцsurrogate"),
        (" шинэ\x0bмөр\x0c", "шинэ\nмөр"),
        ("", ""),
    ],
)
def test_normalize(raw: str, expected: str) -> None:
    assert normalize(raw) == expected


def test_build_result_caps_total_text() -> None:
    pages = [Page(None, "абвгд"), Page("Гарчиг", "еёжзи"), Page(None, "йклмн")]
    assert build_result("docx", pages, 7) == {
        "kind": "docx",
        "page_count": 3,
        "pages": [
            {"number": 1, "title": None, "text": "абвгд"},
            {"number": 2, "title": "Гарчиг", "text": "её"},
            {"number": 3, "title": None, "text": ""},
        ],
        "truncated": True,
    }
    assert build_result("docx", pages, 15)["truncated"] is False


def test_split_long_breaks_at_spaces() -> None:
    text = " ".join(["үг"] * 100)  # 299 тэмдэгт
    pieces = list(_split_long(text, 50))
    assert all(len(piece) <= 50 for piece in pieces)
    assert " ".join(pieces) == text


def test_split_long_without_spaces() -> None:
    assert list(_split_long("а" * 120, 50)) == ["а" * 50, "а" * 50, "а" * 20]


# --- PDF ----------------------------------------------------------------------------


def test_encrypted_fixture_is_a_real_encrypted_pdf(tmp_path: Path, config: Settings) -> None:
    """Тестийн нууцалсан PDF зөв нууц үгээр нээгддэг — зүгээр эвдэрхий файл биш."""
    data = builders.make_pdf([["Нууц хуудас"]], user_password="nuuts")
    document = pdfium.PdfDocument(data, password="nuuts")
    assert document[0].get_textpage().get_text_range() == "Нууц хуудас"
    with pytest.raises(ExtractError) as error:
        extract_pdf(write(tmp_path, "secret.pdf", data), config)
    assert error.value.code == "encrypted"


def test_pdf_skips_pages_after_text_cap(tmp_path: Path, config: Settings) -> None:
    config.max_text_chars = 5
    path = write(tmp_path, "a.pdf", builders.make_pdf([["Нэгдүгээр"], ["Хоёр"], ["Гурав"]]))
    result = extract_pdf(path, config)
    assert [page["text"] for page in result["pages"]] == ["Нэгдү", "", ""]
    assert result["truncated"] is True


# --- PPTX -----------------------------------------------------------------------------


def test_pptx_line_break_and_alternate_content(tmp_path: Path, config: Settings) -> None:
    slide = (
        '<p:sp><p:nvSpPr><p:cNvPr id="3" name="Text"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
        "<p:spPr/><p:txBody><a:bodyPr/>"
        "<a:p><a:r><a:t>Нэгдүгээр</a:t></a:r><a:br/><a:r><a:t>мөр</a:t></a:r></a:p>"
        "</p:txBody></p:sp>"
        '<mc:AlternateContent><mc:Choice Requires="a14">'
        + builders.shape("Томьёо")
        + "</mc:Choice><mc:Fallback>"
        + builders.shape("Томьёо")
        + "</mc:Fallback></mc:AlternateContent>"
    )
    path = write(tmp_path, "a.pptx", builders.make_pptx([[slide]]))
    assert extract_pptx(path, config)["pages"][0]["text"] == "Нэгдүгээр\nмөр\nТомьёо"


def test_pptx_notes_only_slide(tmp_path: Path, config: Settings) -> None:
    path = write(tmp_path, "a.pptx", builders.make_pptx([[]], notes={0: ["Зөвхөн тэмдэглэл"]}))
    page = extract_pptx(path, config)["pages"][0]
    assert page == {"number": 1, "title": None, "text": "Тэмдэглэл: Зөвхөн тэмдэглэл"}


def test_pptx_missing_slide_part_is_empty(tmp_path: Path, config: Settings) -> None:
    data = builders.make_pptx(
        [[builders.shape("Байгаа")]],
        extra_files={
            "ppt/_rels/presentation.xml.rels": builders._rels(
                [("rId101", builders.REL_SLIDE, "slides/slide1.xml")]
            ),
            "ppt/presentation.xml": (
                f'<p:presentation xmlns:p="{builders.NS_P}" xmlns:r="{builders.NS_REL}">'
                '<p:sldIdLst><p:sldId id="256" r:id="rId101"/><p:sldId id="257" r:id="rId999"/>'
                "</p:sldIdLst></p:presentation>"
            ),
        },
    )
    result = extract_pptx(write(tmp_path, "a.pptx", data), config)
    assert [page["text"] for page in result["pages"]] == ["Байгаа", ""]


def test_pptx_relationship_cannot_escape_package(tmp_path: Path, config: Settings) -> None:
    data = builders.make_pptx(
        [[builders.shape("Байгаа")]],
        extra_files={
            "ppt/_rels/presentation.xml.rels": builders._rels(
                [("rId101", builders.REL_SLIDE, "../../../../etc/passwd")]
            ),
        },
    )
    result = extract_pptx(write(tmp_path, "a.pptx", data), config)
    assert result["pages"] == [{"number": 1, "title": None, "text": ""}]


def test_pptx_long_title_is_trimmed(tmp_path: Path, config: Settings) -> None:
    title = "Гарчиг " * 100
    path = write(
        tmp_path, "a.pptx", builders.make_pptx([[builders.shape(title, placeholder="title")]])
    )
    page = extract_pptx(path, config)["pages"][0]
    assert len(page["title"]) == 300
    assert page["text"] == title.strip()


# --- DOCX -----------------------------------------------------------------------------


def test_docx_runs_tabs_breaks_and_tracked_changes(tmp_path: Path, config: Settings) -> None:
    body = [
        "<w:p><w:r><w:t>Нэр</w:t></w:r><w:r><w:tab/><w:t>Оноо</w:t></w:r>"
        "<w:r><w:br/><w:t>Дараагийн мөр</w:t></w:r></w:p>",
        '<w:p><w:r><w:t xml:space="preserve">Хадгалсан </w:t></w:r>'
        "<w:del><w:r><w:delText>устгасан</w:delText></w:r></w:del>"
        "<w:ins><w:r><w:t>нэмсэн</w:t></w:r></w:ins>"
        "<w:moveFrom><w:r><w:t>зөөсөн</w:t></w:r></w:moveFrom></w:p>",
        '<w:p><w:r><w:fldChar w:fldCharType="begin"/></w:r>'
        "<w:r><w:instrText>PAGE</w:instrText></w:r><w:r><w:t>5</w:t></w:r></w:p>",
        "<w:p><w:hyperlink><w:r><w:t>Холбоос</w:t></w:r></w:hyperlink></w:p>",
    ]
    path = write(tmp_path, "a.docx", builders.make_docx(body))
    assert extract_docx(path, config)["pages"][0]["text"] == (
        "Нэр Оноо\nДараагийн мөр\nХадгалсан нэмсэн\n5\nХолбоос"
    )


def test_docx_textbox_is_read_once(tmp_path: Path, config: Settings) -> None:
    textbox = "<w:txbxContent>" + builders.para("Текст хайрцаг") + "</w:txbxContent>"
    body = [
        "<w:p><w:r><w:t>Өмнө</w:t></w:r><w:r><mc:AlternateContent>"
        f'<mc:Choice Requires="wps"><w:drawing>{textbox}</w:drawing></mc:Choice>'
        f"<mc:Fallback><w:pict>{textbox}</w:pict></mc:Fallback>"
        "</mc:AlternateContent></w:r></w:p>",
        builders.para("Дараа"),
    ]
    path = write(tmp_path, "a.docx", builders.make_docx(body))
    assert extract_docx(path, config)["pages"][0]["text"] == "Өмнө\nТекст хайрцаг\nДараа"


def test_docx_content_controls_and_nested_tables(tmp_path: Path, config: Settings) -> None:
    inner = builders.word_table([["Дотоод"]])
    body = [
        "<w:sdt><w:sdtPr/><w:sdtContent>" + builders.para("Удирдлага") + "</w:sdtContent></w:sdt>",
        f"<w:tbl><w:tr><w:tc>{builders.para('Гадна')}{inner}</w:tc></w:tr></w:tbl>",
    ]
    path = write(tmp_path, "a.docx", builders.make_docx(body))
    assert extract_docx(path, config)["pages"][0]["text"] == "Удирдлага\nГадна\nДотоод"


def test_docx_outline_level_and_missing_styles(tmp_path: Path, config: Settings) -> None:
    body = [
        builders.para("Өмнөх"),
        '<w:p><w:pPr><w:outlineLvl w:val="1"/></w:pPr><w:r><w:t>Шууд түвшин</w:t></w:r></w:p>',
        builders.para("Дараах"),
    ]
    path = write(tmp_path, "a.docx", builders.make_docx(body, styles=None))
    pages = extract_docx(path, config)["pages"]
    assert [(page["title"], page["text"]) for page in pages] == [
        (None, "Өмнөх"),
        ("Шууд түвшин", "Шууд түвшин\nДараах"),
    ]


def test_docx_heading_only_section_keeps_following_long_paragraph(
    tmp_path: Path, config: Settings
) -> None:
    config.section_chars = 100
    body = [builders.para("Гарчиг", "Heading1"), builders.para("үг " * 30)]
    path = write(tmp_path, "a.docx", builders.make_docx(body))
    pages = extract_docx(path, config)["pages"]
    assert pages[0]["title"] == "Гарчиг"
    assert pages[0]["text"].startswith("Гарчиг\nүг үг")


def test_docx_template_is_accepted(tmp_path: Path, config: Settings) -> None:
    template = "application/vnd.openxmlformats-officedocument.wordprocessingml.template.main+xml"
    path = write(
        tmp_path, "a.dotx", builders.make_docx([builders.para("Загвар")], main_type=template)
    )
    assert extract_docx(path, config)["pages"][0]["text"] == "Загвар"
