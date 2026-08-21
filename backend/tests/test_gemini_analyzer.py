"""Tests for Gemini LLM analysis service with mocks and fallback tests."""

import json
from unittest.mock import MagicMock, patch
import pytest

from app.services.gemini_analyzer import (
    StructuredGeminiAnalysis,
    analyze_with_gemini,
    generate_rule_based_fallback,
)


def test_rule_based_fallback_generation():
    """Verify rule-based fallback produces complete structured analysis."""
    text = "Are you struggling to gain traction? Follow these simple rules. What do you think?"
    metrics = {
        "word_count": 14,
        "character_count": 83,
        "sentence_count": 3,
        "paragraph_count": 1,
        "hashtag_count": 0,
        "hashtags": [],
        "has_cta": False,
        "has_question": True,
        "first_line": "Are you struggling to gain traction?",
        "readability_grade": "Easy / Conversational",
        "average_sentence_length": 4.7,
        "detected_ctas": [],
    }
    score_data = {"total_score": 75, "verdict": "Good foundation."}

    fallback = generate_rule_based_fallback(text, metrics, score_data)

    assert "overall_assessment" in fallback
    assert len(fallback["strengths"]) >= 2
    assert len(fallback["areas_for_improvement"]) >= 2
    assert len(fallback["suggestions"]) >= 3
    assert "improved_post" in fallback
    assert "hook_analysis" in fallback
    assert "clarity_analysis" in fallback
    assert "engagement_analysis" in fallback
    assert "cta_analysis" in fallback


def test_gemini_missing_api_key_uses_fallback():
    """Verify fallback is returned cleanly when GEMINI_API_KEY is not set."""
    with patch("app.services.gemini_analyzer.get_settings") as mock_settings:
        mock_settings.return_value.GEMINI_API_KEY = None
        mock_settings.return_value.GEMINI_MODEL = "gemini-2.5-flash"

        metrics = {"word_count": 20, "has_cta": True, "has_question": True, "hashtags": []}
        score_data = {"total_score": 80}

        result = analyze_with_gemini("Sample text", metrics, score_data)
        assert result["ai_status"] == "fallback"
        assert "AI analysis is currently unavailable" in result["ai_notice"]
        assert len(result["strengths"]) >= 2


def test_gemini_successful_mocked_response():
    """Verify Gemini analyzer successfully parses structured JSON response when mocked."""
    mock_payload = {
        "overall_assessment": "The post has strong potential with a crisp message and good readability.",
        "strengths": ["Strong opening curiosity hook", "Clear scannable takeaways"],
        "areas_for_improvement": ["Add more specific call-to-action", "Add 2-3 relevant hashtags"],
        "hook_analysis": "Opens with an attention-grabbing hook.",
        "clarity_analysis": "Sentence cadence is natural.",
        "engagement_analysis": "Encourages reader interaction.",
        "cta_analysis": "CTA is clear.",
        "audience_analysis": "Well targeted.",
        "tone": "Professional",
        "suggestions": [
            {
                "title": "Sharpen Hook",
                "issue": "First line could be shorter.",
                "recommendation": "Cut filler words.",
                "reason": "Faster stop-scroll rate.",
            },
            {
                "title": "Add CTA",
                "issue": "Missing next step.",
                "recommendation": "Add comment question.",
                "reason": "Boosts comments.",
            },
            {
                "title": "Format Spacing",
                "issue": "Dense text.",
                "recommendation": "Use line breaks.",
                "reason": "Mobile readability.",
            },
        ],
        "improved_post": "Rewritten high-impact post text here.",
    }

    mock_response = MagicMock()
    mock_response.text = json.dumps(mock_payload)

    with patch("app.services.gemini_analyzer.get_settings") as mock_settings, \
         patch("google.genai.Client") as mock_genai_client:

        mock_settings.return_value.GEMINI_API_KEY = "test_fake_api_key"
        mock_settings.return_value.GEMINI_MODEL = "gemini-2.5-flash"

        client_instance = MagicMock()
        client_instance.models.generate_content.return_value = mock_response
        mock_genai_client.return_value = client_instance

        metrics = {"word_count": 30, "has_cta": True, "has_question": True, "hashtags": []}
        score_data = {"total_score": 85}

        result = analyze_with_gemini("Sample text", metrics, score_data)
        assert result["ai_status"] == "success"
        assert result["overall_assessment"] == mock_payload["overall_assessment"]
        assert len(result["suggestions"]) == 3
        assert result["improved_post"] == "Rewritten high-impact post text here."


def test_gemini_api_failure_falls_back_gracefully():
    """Verify network error or API timeout gracefully triggers fallback without crashing."""
    with patch("app.services.gemini_analyzer.get_settings") as mock_settings, \
         patch("google.genai.Client") as mock_genai_client:

        mock_settings.return_value.GEMINI_API_KEY = "test_fake_api_key"
        mock_settings.return_value.GEMINI_MODEL = "gemini-2.5-flash"

        client_instance = MagicMock()
        client_instance.models.generate_content.side_effect = Exception("503 Service Unavailable / Rate limit exceeded")
        mock_genai_client.return_value = client_instance

        metrics = {"word_count": 30, "has_cta": True, "has_question": True, "hashtags": []}
        score_data = {"total_score": 85}

        result = analyze_with_gemini("Sample text", metrics, score_data)
        assert result["ai_status"] == "fallback"
        assert "AI analysis is currently unavailable" in result["ai_notice"]
        assert "strengths" in result
