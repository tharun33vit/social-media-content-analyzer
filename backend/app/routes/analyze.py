"""Analysis API routes for PDF and Image content processing."""

import logging
from typing import Any, Dict
from fastapi import APIRouter, File, HTTPException, UploadFile, status
from pydantic import BaseModel

from app.config import get_settings
from app.services.content_analyzer import analyze_deterministic_metrics, calculate_engagement_score
from app.services.gemini_analyzer import analyze_with_gemini
from app.services.ocr_service import OCRError, extract_text_from_image
from app.services.pdf_extractor import PDFExtractionError, extract_text_from_pdf
from app.utils.validation import validate_file_upload

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["Analysis"])


@router.post("/analyze")
async def analyze_content(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Process an uploaded social media content document or image.
    Extracts text, runs deterministic metrics and scoring, and adds Gemini qualitative analysis.
    """
    settings = get_settings()

    if not file or not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file was provided in the upload request.",
        )

    try:
        content = await file.read()
    except Exception as e:
        logger.error("Failed to read uploaded file: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to read the uploaded file data.",
        )

    # 1. Validation (File size, extension, magic-byte signatures)
    try:
        file_category, clean_filename = validate_file_upload(
            filename=file.filename,
            content=content,
            max_size_bytes=settings.max_upload_size_bytes,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    # 2. Text Extraction
    extraction_result: Dict[str, Any] = {}
    try:
        if file_category == "pdf":
            extraction_result = extract_text_from_pdf(content)
        elif file_category == "image":
            extraction_result = extract_text_from_image(content)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file category: '{file_category}'",
            )
    except PDFExtractionError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    except OCRError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    except Exception as e:
        logger.error("Unexpected extraction error: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while extracting text from the document.",
        )

    extracted_text = extraction_result.get("text", "").strip()
    if not extracted_text:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No extractable text was found in the document.",
        )

    # 3. Deterministic Content Analysis & Scoring
    metrics = analyze_deterministic_metrics(extracted_text)
    score_data = calculate_engagement_score(metrics, extracted_text)

    # 4. Gemini Qualitative Analysis (with seamless rule-based fallback)
    ai_review = analyze_with_gemini(extracted_text, metrics, score_data)

    # 5. Assemble File Information
    file_info = {
        "filename": clean_filename,
        "file_type": file_category,
        "size_bytes": len(content),
        "extraction_method": extraction_result.get("method", "Standard Extraction"),
        "page_count": extraction_result.get("page_count", 1 if file_category == "image" else 0),
        "char_count": len(extracted_text),
    }

    return {
        "file_info": file_info,
        "extracted_text": extracted_text,
        "metrics": metrics,
        "score": score_data,
        "ai_review": ai_review,
    }
