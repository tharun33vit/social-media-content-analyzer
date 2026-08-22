"""Test configuration and shared fixtures for backend testing."""

import io
from typing import Any, Dict
import fitz  # PyMuPDF
import pytest
from fastapi.testclient import TestClient
from PIL import Image, ImageDraw

from app.main import app


@pytest.fixture
def client() -> TestClient:
    """FastAPI TestClient fixture."""
    return TestClient(app)


@pytest.fixture
def sample_pdf_bytes() -> bytes:
    """Generate a valid single-page PDF with realistic social media text."""
    doc = fitz.open()
    page = doc.new_page()
    text = (
        "Are you still writing social media posts without a clear hook?\n\n"
        "Here are 3 simple principles to improve engagement today:\n"
        "1. Write for busy scrollers: keep the first line under 80 characters.\n"
        "2. Ask a specific question at the end to encourage authentic comments.\n"
        "3. Include a single, direct call-to-action.\n\n"
        "What strategy has worked best for your team? Share your thoughts below!\n\n"
        "#ContentStrategy #SocialMediaTips #Marketing"
    )
    page.insert_text((50, 72), text, fontsize=12)
    pdf_data = doc.write()
    doc.close()
    return pdf_data


@pytest.fixture
def sample_empty_pdf_bytes() -> bytes:
    """Generate a PDF with no text."""
    doc = fitz.open()
    doc.new_page()
    pdf_data = doc.write()
    doc.close()
    return pdf_data


@pytest.fixture
def sample_image_png_bytes() -> bytes:
    """Generate a valid PNG image with text rendered on canvas."""
    img = Image.new("RGB", (600, 250), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    d.text((20, 30), "How to scale your engineering team in 2026.", fill=(0, 0, 0))
    d.text((20, 70), "Focus on mentorship, clear metrics, and quality.", fill=(0, 0, 0))
    d.text((20, 110), "What is your biggest leadership lesson? Comment below.", fill=(0, 0, 0))
    d.text((20, 150), "#Engineering #Leadership #Tech", fill=(0, 0, 0))
    
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


@pytest.fixture
def sample_analysis_payload() -> Dict[str, Any]:
    """Sample full analysis response data for report generation tests."""
    return {
        "file_info": {
            "filename": "demo_post.pdf",
            "file_type": "pdf",
            "size_bytes": 10240,
            "extraction_method": "PyMuPDF Text Extraction",
            "page_count": 1,
            "char_count": 340,
        },
        "extracted_text": "Sample social media post text for testing reports.",
        "metrics": {
            "word_count": 52,
            "character_count": 340,
            "sentence_count": 5,
            "paragraph_count": 3,
            "hashtag_count": 3,
            "hashtags": ["#ContentStrategy", "#SocialMediaTips", "#Marketing"],
            "mention_count": 0,
            "mentions": [],
            "url_count": 0,
            "urls": [],
            "question_count": 2,
            "has_question": True,
            "cta_count": 1,
            "has_cta": True,
            "detected_ctas": ["share your thoughts"],
            "first_line": "Are you still writing social media posts without a clear hook?",
            "first_line_length": 62,
            "average_sentence_length": 10.4,
            "readability_score": 74.5,
            "readability_grade": "Easy / Conversational",
        },
        "score": {
            "total_score": 88,
            "verdict": "High engagement readiness with a compelling hook, balanced structure, and clear action path.",
            "breakdown": {
                "hook_opening": {"score": 18, "max": 20, "label": "Hook & Opening"},
                "clarity_readability": {"score": 19, "max": 20, "label": "Clarity & Readability"},
                "engagement_potential": {"score": 18, "max": 20, "label": "Engagement Potential"},
                "call_to_action": {"score": 13, "max": 15, "label": "Call-to-Action"},
                "content_structure": {"score": 9, "max": 10, "label": "Content Structure"},
                "hashtag_strategy": {"score": 5, "max": 5, "label": "Hashtag Strategy"},
                "audience_format": {"score": 6, "max": 10, "label": "Audience & Format Fit"},
            },
            "disclaimer": "This score is an analytical heuristic for engagement readiness, not a guarantee of impressions, reach, or likes.",
        },
        "ai_review": {
            "ai_status": "success",
            "ai_model": "gemini-3.6-flash",
            "overall_assessment": "The post has an intriguing opening question and clean numbered formatting that encourages reading.",
            "strengths": [
                "Intriguing question hook that immediately challenges the reader.",
                "Numbered structure that makes key takeaways easy to scan.",
                "Direct conversation prompt at the end.",
            ],
            "areas_for_improvement": [
                "Could specify a tangible example for principle #1.",
                "Consider spacing hashtags onto their own line.",
            ],
            "hook_analysis": "Strong question hook that stimulates curiosity.",
            "clarity_analysis": "Clear, concise sentences with ideal cadence.",
            "engagement_analysis": "High conversational potential with the closing question.",
            "cta_analysis": "Explicit comment prompt included.",
            "audience_analysis": "Targeted well at social media content creators.",
            "tone": "Professional & Educational",
            "suggestions": [
                {
                    "title": "Add Concrete Example",
                    "issue": "Principles are theoretical without an applied sample.",
                    "recommendation": "Include a 1-line before/after example.",
                    "reason": "Examples make abstract advice immediately actionable.",
                },
                {
                    "title": "Format Hashtag Footer",
                    "issue": "Hashtags are tightly packed.",
                    "recommendation": "Place 2 line breaks before tags.",
                    "reason": "Improves visual cleanliness on mobile screens.",
                },
            ],
            "improved_post": (
                "Are you still writing social media posts without a clear hook?\n\n"
                "Here are 3 simple principles to improve engagement today:\n\n"
                "1. Keep your opening line under 80 characters for fast scanning\n"
                "2. Ask a specific question to spark comments\n"
                "3. Give a single, obvious next step\n\n"
                "Which of these 3 made the biggest difference in your recent posts? Let me know below ðŸ‘‡\n\n"
                "#ContentStrategy #SocialMediaTips"
            ),
        },
    }
