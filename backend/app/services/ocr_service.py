"""Image OCR service using Pillow and Tesseract."""

import io
import shutil
from typing import Any, Dict
from PIL import Image, ImageOps, UnidentifiedImageError
import pytesseract
from app.config import get_settings


class OCRError(Exception):
    """Raised when OCR extraction encounters an error."""
    pass


def configure_tesseract() -> None:
    """Configure Tesseract binary path from settings or system defaults."""
    settings = get_settings()
    if settings.TESSERACT_CMD:
        pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD
    elif shutil.which("tesseract"):
        # Auto-discovered in PATH
        pass
    else:
        # Standard default Windows location check
        default_win_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        if shutil.which(default_win_path):
            pytesseract.pytesseract.tesseract_cmd = default_win_path


def extract_text_from_image(image_bytes: bytes) -> Dict[str, Any]:
    """
    Extract readable text from image bytes using Pillow and Tesseract OCR.

    Args:
        image_bytes: Raw binary bytes of uploaded image.

    Returns:
        Dict containing:
            - text: Cleaned extracted text
            - method: Extraction engine name
            - width: Image width
            - height: Image height
            - format: Image format (PNG, JPEG, etc.)

    Raises:
        OCRError: If Tesseract is unavailable, image is corrupted, or no text found.
    """
    if not image_bytes or len(image_bytes) == 0:
        raise OCRError("Image file is empty.")

    configure_tesseract()

    try:
        image = Image.open(io.BytesIO(image_bytes))
        image.load()  # Validate integrity
    except (UnidentifiedImageError, OSError):
        raise OCRError("The uploaded image could not be identified or is corrupted.")
    except Exception as e:
        raise OCRError(f"The uploaded image could not be identified or is corrupted: {str(e)}")

    img_format = image.format or "IMAGE"
    width, height = image.size

    # Preprocessing: convert to grayscale and normalize contrast
    try:
        if image.mode not in ("L", "RGB"):
            processed_img = image.convert("RGB")
        else:
            processed_img = image

        # Convert to grayscale for consistent character contrast
        gray_img = ImageOps.grayscale(processed_img)
        # Gentle auto-contrast to enhance text edges
        enhanced_img = ImageOps.autocontrast(gray_img)
    except Exception:
        enhanced_img = image

    # Run OCR with pytesseract
    try:
        raw_text = pytesseract.image_to_string(enhanced_img, config="--psm 3")
    except pytesseract.TesseractNotFoundError:
        raise OCRError(
            "OCR is currently unavailable. Please install/configure Tesseract OCR on the server."
        )
    except Exception as e:
        error_msg = str(e).lower()
        if "tesseract is not installed" in error_msg or "not found" in error_msg:
            raise OCRError(
                "OCR is currently unavailable. Please install/configure Tesseract OCR."
            )
        raise OCRError(f"OCR processing encountered an unexpected issue: {str(e)}")

    # Clean up text lines
    cleaned_lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
    cleaned_text = "\n".join(cleaned_lines)

    if not cleaned_text or len(cleaned_text.strip()) < 3:
        raise OCRError(
            "No readable text could be recognized from the image. "
            "Please ensure the image contains clear, high-contrast text and try again."
        )

    return {
        "text": cleaned_text.strip(),
        "method": "Tesseract OCR",
        "format": img_format,
        "width": width,
        "height": height,
        "char_count": len(cleaned_text.strip()),
    }
