"""Integration tests for /api/analyze and /api/report endpoints."""

from typing import Any, Dict
from fastapi.testclient import TestClient


def test_api_analyze_pdf_success(client: TestClient, sample_pdf_bytes: bytes):
    """Verify POST /api/analyze with valid PDF upload."""
    files = {"file": ("my_content.pdf", sample_pdf_bytes, "application/pdf")}
    response = client.post("/api/analyze", files=files)
    assert response.status_code == 200
    data = response.json()

    assert "file_info" in data
    assert data["file_info"]["filename"] == "my_content.pdf"
    assert data["file_info"]["file_type"] == "pdf"

    assert "metrics" in data
    assert data["metrics"]["word_count"] > 0

    assert "score" in data
    assert 0 <= data["score"]["total_score"] <= 100
    assert "breakdown" in data["score"]

    assert "ai_review" in data
    assert "overall_assessment" in data["ai_review"]
    assert "improved_post" in data["ai_review"]


def test_api_analyze_invalid_extension(client: TestClient):
    """Verify POST /api/analyze with unsupported file type returns 400."""
    files = {"file": ("spreadsheet.xlsx", b"PK\x03\x04fakexlsx", "application/octet-stream")}
    response = client.post("/api/analyze", files=files)
    assert response.status_code == 400
    assert "Unsupported file format" in response.json()["detail"]


def test_api_analyze_empty_file(client: TestClient):
    """Verify POST /api/analyze with empty file returns 400."""
    files = {"file": ("empty.pdf", b"", "application/pdf")}
    response = client.post("/api/analyze", files=files)
    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()


def test_api_report_pdf_download(client: TestClient, sample_analysis_payload: Dict[str, Any]):
    """Verify POST /api/report/pdf downloads a valid PDF."""
    response = client.post("/api/report/pdf", json=sample_analysis_payload)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert "attachment; filename=" in response.headers.get("content-disposition", "")
    assert len(response.content) > 500


def test_api_report_docx_download(client: TestClient, sample_analysis_payload: Dict[str, Any]):
    """Verify POST /api/report/docx downloads a valid Word doc."""
    response = client.post("/api/report/docx", json=sample_analysis_payload)
    assert response.status_code == 200
    assert "wordprocessingml" in response.headers["content-type"]
    assert "attachment; filename=" in response.headers.get("content-disposition", "")
    assert len(response.content) > 500
