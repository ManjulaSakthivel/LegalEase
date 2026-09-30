from services.document_formatter import format_docx, format_pdf
from utils.text_utils import sanitize_text, terms_from_text


def test_sanitize_text():
    text = "Hello “world” — test…"
    result = sanitize_text(text)
    assert result == 'Hello "world" - test...'


def test_terms():
    assert terms_from_text("A; B; ; C") == ["A", "B", "C"]


def test_docx_export():
    result = format_docx("1. PARTIES\n\nAlice and Bob", "NDA")
    assert result[:2] == b"PK"


def test_pdf_export():
    result = format_pdf("1. PARTIES\n\nAlice and Bob", "NDA")
    assert result.startswith(b"%PDF")
