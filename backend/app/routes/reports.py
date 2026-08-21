"""Report download routes for PDF and DOCX generation."""

import logging
from datetime import datetime
from typing import Any, Dict
from fastapi import APIRouter, HTTPException, Response, status
from fastapi.responses import Response

from app.services.report_generator import generate_docx_report, generate_pdf_report

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/report", tags=["Reports"])


@router.post("/pdf")
async def download_pdf_report(payload: Dict[str, Any]) -> Response:
    """
    Generate and download a professional PDF report from the analysis payload.
    """
    if not payload or not isinstance(payload, dict):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid analysis payload provided.",
        )

    try:
        pdf_bytes = generate_pdf_report(payload)
    except Exception as e:
        logger.error("PDF generation failed: %s", str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate PDF report: {str(e)}",
        )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Social_Media_Analysis_{timestamp}.pdf"

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )


@router.post("/docx")
async def download_docx_report(payload: Dict[str, Any]) -> Response:
    """
    Generate and download a professional Word (.docx) report from the analysis payload.
    """
    if not payload or not isinstance(payload, dict):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid analysis payload provided.",
        )

    try:
        docx_bytes = generate_docx_report(payload)
    except Exception as e:
        logger.error("DOCX generation failed: %s", str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate Word report: {str(e)}",
        )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Social_Media_Analysis_{timestamp}.docx"

    return Response(
        content=docx_bytes,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )
