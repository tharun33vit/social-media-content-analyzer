"""File upload and request validation utilities."""

import os
from typing import Tuple

SUPPORTED_EXTENSIONS = {
    ".pdf": "pdf",
    ".png": "image",
    ".jpg": "image",
    ".jpeg": "image",
    ".webp": "image",
}


def detect_file_signature(content: bytes) -> str:
    """Detect file format based on magic bytes / file signatures."""
    if len(content) < 4:
        return "unknown"

    # PDF signature
    if content.startswith(b"%PDF"):
        return "pdf"

    # PNG signature: 89 50 4E 47 0D 0A 1A 0A
    if content.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"

    # JPEG signature: FF D8 FF
    if content.startswith(b"\xff\xd8\xff"):
        return "jpeg"

    # WEBP signature: RIFF....WEBP
    if content.startswith(b"RIFF") and len(content) >= 12 and content[8:12] == b"WEBP":
        return "webp"

    return "unknown"


def validate_file_upload(
    filename: str,
    content: bytes,
    max_size_bytes: int = 10 * 1024 * 1024,
) -> Tuple[str, str]:
    """
    Validate uploaded file for size, allowed extension, and authentic file signature.

    Returns:
        Tuple[file_type, clean_filename]: e.g. ("pdf", "sample.pdf") or ("image", "sample.png")

    Raises:
        ValueError: If validation fails with human-readable error explanation.
    """
    if not filename or not filename.strip():
        raise ValueError("Filename cannot be empty.")

    clean_filename = os.path.basename(filename.strip())

    # Empty file check
    if not content or len(content) == 0:
        raise ValueError("The uploaded file is empty. Please select a valid document or image.")

    # Size limit check
    if len(content) > max_size_bytes:
        file_size_mb = len(content) / (1024 * 1024)
        max_size_mb = max_size_bytes / (1024 * 1024)
        raise ValueError(
            f"File size ({file_size_mb:.2f} MB) exceeds maximum allowed limit of {max_size_mb:.0f} MB."
        )

    # Extension check
    _, ext = os.path.splitext(clean_filename.lower())
    if ext not in SUPPORTED_EXTENSIONS:
        supported = ", ".join(sorted(SUPPORTED_EXTENSIONS.keys()))
        raise ValueError(
            f"Unsupported file format '{ext}'. Supported formats are: {supported}."
        )

    expected_category = SUPPORTED_EXTENSIONS[ext]

    # Magic byte validation
    signature = detect_file_signature(content)
    if signature == "unknown":
        raise ValueError(
            "File content signature could not be verified or is corrupted. "
            "Please ensure the file is a valid PDF or standard image."
        )

    # Match extension category to signature
    if expected_category == "pdf" and signature != "pdf":
        raise ValueError(
            "File has .pdf extension but the binary content is not a valid PDF document."
        )

    if expected_category == "image" and signature not in {"png", "jpeg", "webp"}:
        raise ValueError(
            f"File has image extension '{ext}' but binary content does not match standard image format."
        )

    return expected_category, clean_filename
