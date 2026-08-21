"""PDF text extraction service using PyMuPDF (fitz)."""

from typing import Any, Dict, List
import fitz  # PyMuPDF


class PDFExtractionError(Exception):
    """Raised when PDF extraction encounters an unrecoverable error."""
    pass


def extract_text_from_pdf(pdf_bytes: bytes) -> Dict[str, Any]:
    """
    Extract readable text and layout structure from a PDF byte stream.

    Args:
        pdf_bytes: Raw bytes of the uploaded PDF file.

    Returns:
        Dict containing:
            - text: Combined normalized text
            - page_count: Total number of pages
            - method: Extraction engine name
            - pages: List of per-page text content
            - is_scanned_likely: Boolean indicating if document contains zero or negligible text

    Raises:
        PDFExtractionError: If file is corrupted or cannot be read.
    """
    if not pdf_bytes or len(pdf_bytes) == 0:
        raise PDFExtractionError("PDF document is empty.")

    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    except Exception as e:
        raise PDFExtractionError(f"Could not open or parse PDF document: {str(e)}")

    page_count = len(doc)
    if page_count == 0:
        doc.close()
        raise PDFExtractionError("The PDF document contains no pages.")

    pages_text: List[str] = []
    total_characters = 0

    try:
        for page_idx in range(page_count):
            page = doc.load_page(page_idx)
            text = page.get_text("text")
            # Clean up excessive blank lines while preserving logical paragraphs
            normalized = "\n".join([line.rstrip() for line in text.splitlines() if line.strip()])
            pages_text.append(normalized)
            total_characters += len(normalized)
    except Exception as e:
        doc.close()
        raise PDFExtractionError(f"Failed extracting text from PDF page: {str(e)}")
    finally:
        doc.close()

    # Determine if the PDF is likely scanned / image-only
    is_scanned_likely = (total_characters < 15)

    if is_scanned_likely:
        raise PDFExtractionError(
            "The uploaded PDF contains no selectable text. It appears to be a scanned image or empty document. "
            "Please upload an image file directly (PNG, JPG) to use OCR, or a PDF with selectable text."
        )

    # Combine text cleanly
    if page_count == 1:
        combined_text = pages_text[0]
    else:
        combined_sections = []
        for idx, p_text in enumerate(pages_text, start=1):
            if p_text.strip():
                combined_sections.append(f"--- Page {idx} ---\n{p_text}")
        combined_text = "\n\n".join(combined_sections)

    return {
        "text": combined_text.strip(),
        "page_count": page_count,
        "method": "PyMuPDF Text Extraction",
        "pages": pages_text,
        "is_scanned_likely": False,
        "char_count": total_characters,
    }
