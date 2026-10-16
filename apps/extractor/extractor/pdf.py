"""PDF-ээс текст задлах — зөвхөн pypdfium2 (PDFium, Apache-2.0 / BSD-3).

PyMuPDF нь AGPL тул БҮҮ хэрэглэ. Энэ модулийг зөвхөн `extractor.worker`
(хязгаартай дэд процесс) импортлоно.
"""

from typing import Any

import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c

from extractor.document import ExtractError, Page, build_result, normalize
from extractor.settings import Settings

PDF_MAGIC = b"%PDF-"
# Header-ийн өмнө хог байж болно (PDFium үүнийг зөвшөөрдөг), гэхдээ эхний 1 KB-д.
MAGIC_WINDOW = 1024
# Нууц үгтэй (эсвэл PDFium-ийн дэмждэггүй хамгаалалттай) PDF.
_PASSWORD_ERRORS = frozenset({pdfium_c.FPDF_ERR_PASSWORD, pdfium_c.FPDF_ERR_SECURITY})


def _page_text(document: pdfium.PdfDocument, index: int) -> str:
    try:
        page = document[index]
    except pdfium.PdfiumError:
        return ""
    try:
        textpage = page.get_textpage()
        try:
            return textpage.get_text_range()
        finally:
            textpage.close()
    except pdfium.PdfiumError:
        # Эвдэрсэн ганц хуудас баримтыг бүхэлд нь унагаахгүй.
        return ""
    finally:
        page.close()


def extract_pdf(path: str, settings: Settings) -> dict[str, Any]:
    with open(path, "rb") as file:
        head = file.read(MAGIC_WINDOW)
    if PDF_MAGIC not in head:
        raise ExtractError("corrupt", detail="magic")

    try:
        # Нууц үггүйгээр нээнэ. Зөвхөн эзэмшигчийн нууц үгтэй (хэвлэх, хуулах
        # хориотой) PDF нээгдэнэ — унших нууц үгтэй нь PASSWORD алдаа өгнө.
        document = pdfium.PdfDocument(path, password=None)
    except pdfium.PdfiumError as error:
        if error.err_code in _PASSWORD_ERRORS:
            raise ExtractError("encrypted") from None
        raise ExtractError("corrupt", detail=f"pdfium_{error.err_code}") from None

    try:
        count = len(document)
        if count > settings.max_pages:
            raise ExtractError("too_many_pages", page_count=count)

        pages: list[Page] = []
        remaining = settings.max_text_chars
        truncated = False
        for index in range(count):
            if remaining <= 0:
                # Нийт хязгаарт хүрсэн — үлдсэн хуудсыг ачаалж цаг үрэхгүй.
                pages.append(Page(None, ""))
                truncated = True
                continue
            text = normalize(_page_text(document, index))
            remaining -= len(text)
            pages.append(Page(None, text))
        return build_result("pdf", pages, settings.max_text_chars, truncated)
    finally:
        document.close()
