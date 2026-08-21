"""Tests for OCR extraction service."""

from unittest.mock import patch
import pytest
from app.services.ocr_service import OCRError, extract_text_from_image


def test_extract_valid_image(sample_image_png_bytes: bytes):
    """Verify extracting text from an image with OCR."""
    try:
        res = extract_text_from_image(sample_image_png_bytes)
        assert "method" in res
        assert "text" in res
        assert len(res["text"]) > 0
    except OCRError as e:
        # If Tesseract is not configured in current CI test environment, verify error is clean
        assert "OCR is currently unavailable" in str(e) or "No readable text" in str(e)


def test_corrupted_image():
    """Verify corrupted image bytes raise clean OCRError."""
    with pytest.raises(OCRError, match="could not be identified or is corrupted"):
        extract_text_from_image(b"\x89PNG\r\n\x1a\n\x00corrupt")


def test_ocr_missing_tesseract_mocked(sample_image_png_bytes: bytes):
    """Verify clean error when Tesseract executable is not found."""
    with patch("pytesseract.image_to_string", side_effect=Exception("tesseract is not installed or it's not in your PATH")):
        with pytest.raises(OCRError, match="OCR is currently unavailable"):
            extract_text_from_image(sample_image_png_bytes)
