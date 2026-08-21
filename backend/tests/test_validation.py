"""Tests for file validation logic."""

import pytest
from app.utils.validation import detect_file_signature, validate_file_upload


def test_detect_file_signature():
    """Verify magic bytes detection for supported formats."""
    assert detect_file_signature(b"%PDF-1.4 sample") == "pdf"
    assert detect_file_signature(b"\x89PNG\r\n\x1a\n\x00\x00") == "png"
    assert detect_file_signature(b"\xff\xd8\xff\xe0\x00") == "jpeg"
    assert detect_file_signature(b"RIFF\x00\x00\x00\x00WEBPVP8") == "webp"
    assert detect_file_signature(b"plain text content") == "unknown"


def test_validate_valid_pdf():
    """Verify successful validation of PDF file."""
    content = b"%PDF-1.5 test document"
    cat, name = validate_file_upload("my_post.pdf", content)
    assert cat == "pdf"
    assert name == "my_post.pdf"


def test_validate_valid_image():
    """Verify successful validation of PNG image."""
    content = b"\x89PNG\r\n\x1a\n\x00\x00\x00"
    cat, name = validate_file_upload("screenshot.png", content)
    assert cat == "image"
    assert name == "screenshot.png"


def test_validate_empty_file():
    """Verify empty file raises ValueError."""
    with pytest.raises(ValueError, match="empty"):
        validate_file_upload("empty.pdf", b"")


def test_validate_oversized_file():
    """Verify oversized file raises ValueError."""
    large_bytes = b"%PDF" + b"0" * (11 * 1024 * 1024)
    with pytest.raises(ValueError, match="exceeds maximum allowed limit"):
        validate_file_upload("huge.pdf", large_bytes, max_size_bytes=10 * 1024 * 1024)


def test_validate_unsupported_extension():
    """Verify unsupported extension raises ValueError."""
    with pytest.raises(ValueError, match="Unsupported file format"):
        validate_file_upload("document.docx", b"PK\x03\x04test")


def test_validate_mismatched_extension_and_content():
    """Verify spoofed extension is caught by signature check."""
    # File named .pdf but actually plain text
    with pytest.raises(ValueError, match="File content signature could not be verified"):
        validate_file_upload("fake.pdf", b"This is not a binary PDF")
