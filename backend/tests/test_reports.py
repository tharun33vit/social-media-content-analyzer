"""Tests for PDF and DOCX report generation."""

import io
from typing import Any, Dict
import fitz  # PyMuPDF
from docx import Document
import pytest

from app.services.report_generator import generate_docx_report, generate_pdf_report


def test_generate_pdf_report(sample_analysis_payload: Dict[str, Any]):
    """Verify that ReportLab creates a valid, parseable PDF byte stream."""
    pdf_bytes = generate_pdf_report(sample_analysis_payload)
    assert len(pdf_bytes) > 1000
    assert pdf_bytes.startswith(b"%PDF")

    # Verify PyMuPDF can parse the generated PDF report
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    assert len(doc) >= 1
    page1_text = doc[0].get_text()
    assert "SOCIAL MEDIA CONTENT ANALYSIS REPORT" in page1_text
    assert "ENGAGEMENT SCORE" in page1_text
    assert "88" in page1_text
    doc.close()


def test_generate_docx_report(sample_analysis_payload: Dict[str, Any]):
    """Verify that python-docx creates a valid, parseable DOCX byte stream."""
    docx_bytes = generate_docx_report(sample_analysis_payload)
    assert len(docx_bytes) > 1000

    # Verify python-docx can load the generated stream
    buf = io.BytesIO(docx_bytes)
    doc = Document(buf)
    full_text = "\n".join([p.text for p in doc.paragraphs])
    assert "Social Media Content Analysis Report" in full_text
    assert "Content Metrics Snapshot" in full_text
