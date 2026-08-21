"""Tests for PyMuPDF PDF extractor service."""

import pytest
from app.services.pdf_extractor import PDFExtractionError, extract_text_from_pdf


def test_extract_valid_pdf(sample_pdf_bytes: bytes):
    """Verify extracting text from a valid PDF."""
    res = extract_text_from_pdf(sample_pdf_bytes)
    assert res["page_count"] == 1
    assert "Are you still writing social media posts" in res["text"]
    assert "#ContentStrategy" in res["text"]
    assert res["method"] == "PyMuPDF Text Extraction"


def test_extract_empty_pdf(sample_empty_pdf_bytes: bytes):
    """Verify empty/scanned PDF raises appropriate PDFExtractionError."""
    with pytest.raises(PDFExtractionError, match="no selectable text"):
        extract_text_from_pdf(sample_empty_pdf_bytes)


def test_extract_corrupted_pdf_bytes():
    """Verify corrupted PDF bytes raise PDFExtractionError."""
    with pytest.raises(PDFExtractionError, match="Could not open or parse PDF document"):
        extract_text_from_pdf(b"%PDF-invalid-bytes-12345")
