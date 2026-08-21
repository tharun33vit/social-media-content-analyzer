"""Tests for health check endpoint."""

from fastapi.testclient import TestClient


def test_health_endpoint(client: TestClient):
    """Verify /health returns 200 and expected status fields."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "Social Media Content Analyzer" in data["service"]
    assert "version" in data
    assert "gemini_configured" in data
    assert "tesseract_available" in data
