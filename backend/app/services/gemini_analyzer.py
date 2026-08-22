"""Google Gemini LLM semantic analysis service with structured output and rule-based fallback."""

import logging
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

from app.config import get_settings

logger = logging.getLogger(__name__)


class SuggestionItem(BaseModel):
    """Specific actionable improvement item."""
    title: str = Field(description="Short title of the suggestion")
    issue: str = Field(description="What needs improvement in the content")
    recommendation: str = Field(description="Concrete recommendation on how to fix it")
    reason: str = Field(description="Strategic rationale for why this matters for social engagement")


class StructuredGeminiAnalysis(BaseModel):
    """Structured response schema for Gemini analysis."""
    overall_assessment: str = Field(
        description="A concise, professional 2-3 sentence assessment of the post's overall strengths and areas for refinement."
    )
    strengths: List[str] = Field(
        description="2 to 4 notable strengths of the content",
        min_length=2,
        max_length=4,
    )
    areas_for_improvement: List[str] = Field(
        description="2 to 4 key areas for improvement",
        min_length=2,
        max_length=4,
    )
    hook_analysis: str = Field(
        description="Detailed evaluation of whether the opening captures attention and stops the scroll."
    )
    clarity_analysis: str = Field(
        description="Evaluation of message clarity, sentence cadence, and readability."
    )
    engagement_analysis: str = Field(
        description="Evaluation of whether readers have reasons to respond, comment, share, or save."
    )
    cta_analysis: str = Field(
        description="Evaluation of the call-to-action clarity and positioning."
    )
    audience_analysis: str = Field(
        description="Evaluation of whether the content is appropriate for its intended audience based on text clues."
    )
    tone: str = Field(
        description="Identified tone (e.g. Professional, Conversational, Educational, Promotional, Neutral)"
    )
    suggestions: List[SuggestionItem] = Field(
        description="3 to 5 specific actionable improvements with issue, recommendation, and rationale",
        min_length=3,
        max_length=5,
    )
    improved_post: str = Field(
        description="An improved version of the post that preserves original facts and meaning without clickbait."
    )


def generate_rule_based_fallback(text: str, metrics: Dict[str, Any], score_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate high-quality rule-based fallback analysis when Gemini is unavailable.
    Provides complete structured feedback derived from deterministic metrics.
    """
    total_score = score_data.get("total_score", 70)
    has_cta = metrics.get("has_cta", False)
    has_question = metrics.get("has_question", False)
    word_count = metrics.get("word_count", 0)
    first_line = metrics.get("first_line", "")
    hashtags = metrics.get("hashtags", [])
    readability_grade = metrics.get("readability_grade", "Standard")

    strengths = []
    if word_count > 0:
        strengths.append(f"Clear focus with a concise length of {word_count} words.")
    if readability_grade in ("Easy / Conversational", "Very Easy"):
        strengths.append(f"Highly accessible reading level ({readability_grade}).")
    elif readability_grade == "Standard":
        strengths.append("Balanced tone suitable for general professional audiences.")
    if has_question:
        strengths.append("Uses questions to actively encourage reader response and comments.")
    if has_cta:
        strengths.append("Includes an explicit call-to-action to guide reader next steps.")
    if len(hashtags) in range(1, 6):
        strengths.append(f"Well-calibrated hashtag count ({len(hashtags)}) for topic discovery.")

    # Ensure at least 2 strengths
    if len(strengths) < 2:
        strengths.append("Direct communication style without unnecessary filler language.")
    if len(strengths) < 2:
        strengths.append("Cohesive message structure from opening to conclusion.")

    areas_for_improvement = []
    if not has_cta:
        areas_for_improvement.append("Missing a direct call-to-action to prompt audience next steps.")
    if not has_question:
        areas_for_improvement.append("Lacks an explicit question or conversation prompt to stimulate comments.")
    if len(first_line) > 120:
        areas_for_improvement.append("Opening hook is relatively long; a punchier first line stops the scroll faster.")
    elif len(first_line) < 20 and word_count > 40:
        areas_for_improvement.append("Opening sentence could be more intriguing to build anticipation.")
    if len(hashtags) == 0:
        areas_for_improvement.append("No hashtags included; 2-3 relevant tags could improve discoverability.")
    elif len(hashtags) > 7:
        areas_for_improvement.append("High hashtag density may make the post look cluttered.")

    if len(areas_for_improvement) < 2:
        areas_for_improvement.append("Consider breaking longer paragraphs into 1-2 sentence chunks for mobile scanning.")
    if len(areas_for_improvement) < 2:
        areas_for_improvement.append("Add a closing question to invite peers to share their perspectives.")

    # Tailor suggestions
    suggestions = []
    if not has_cta:
        suggestions.append({
            "title": "Add a Concrete Call-to-Action",
            "issue": "The post ends without a clear instruction for the reader.",
            "recommendation": "End with an actionable prompt such as 'Save this for your next campaign' or 'Link in bio for details'.",
            "reason": "Clear CTAs significantly improve post conversion and follow-through.",
        })
    else:
        suggestions.append({
            "title": "Sharpen Call-to-Action Placement",
            "issue": "CTA can be separated visually for higher contrast.",
            "recommendation": "Place the CTA on its own distinct line at the bottom with clean spacing.",
            "reason": "Visual separation draws the eye directly to the final action item.",
        })

    if not has_question:
        suggestions.append({
            "title": "Incorporate a Conversation Starter",
            "issue": "Content is primarily broadcast-oriented rather than conversational.",
            "recommendation": "Add a focused question at the end: 'How does your team handle this?' or 'What would you add?'",
            "reason": "Social algorithms heavily prioritize posts with active comment discussions.",
        })
    else:
        suggestions.append({
            "title": "Make Questions More Specific",
            "issue": "Broad questions yield fewer responses than targeted prompts.",
            "recommendation": "Ask a specific binary or multiple-choice question rather than an open-ended essay prompt.",
            "reason": "Lower friction questions encourage quick comment responses from busy readers.",
        })

    suggestions.append({
        "title": "Optimize Paragraph Cadence for Mobile",
        "issue": "Readers on mobile devices skim past dense text blocks.",
        "recommendation": "Keep paragraphs under 2-3 lines and use bullet points or line breaks between thoughts.",
        "reason": "High visual scannability increases average dwell time and comprehension.",
    })

    # Rule-based improved post synthesis
    improved_lines = []
    if first_line:
        improved_lines.append(first_line)
    
    # Body
    body_paragraphs = text.split("\n\n")
    if len(body_paragraphs) > 1:
        for p in body_paragraphs[1:]:
            if p.strip() and not any(cta in p for cta in metrics.get("detected_ctas", [])):
                improved_lines.append(p.strip())
    else:
        improved_lines.append(text.strip())

    if not has_question:
        improved_lines.append("What's your take on this? Let me know in the comments below ðŸ‘‡")
    if not has_cta:
        improved_lines.append("ðŸ“Œ Save this post for your next planning session.")

    improved_post = "\n\n".join(improved_lines)

    return {
        "overall_assessment": (
            f"The content demonstrates a solid foundation with an engagement readiness score of {total_score}/100. "
            f"Its readability level is rated '{readability_grade}', making it accessible to target readers. "
            "Applying structured formatting and interactive hooks will enhance performance."
        ),
        "strengths": strengths[:4],
        "areas_for_improvement": areas_for_improvement[:4],
        "hook_analysis": (
            f"The opening line ('{first_line[:60]}...') is {len(first_line)} characters. "
            "A concise, curiosity-driven first sentence effectively captures audience attention in competitive feeds."
        ),
        "clarity_analysis": (
            f"Sentence length averages {metrics.get('average_sentence_length', 12)} words per sentence. "
            f"The readability rating is {readability_grade}, indicating good clarity."
        ),
        "engagement_analysis": (
            "The post provides informative value. Introducing direct conversational prompts will encourage readers "
            "to share personal experiences or opinions."
        ),
        "cta_analysis": (
            "An explicit call-to-action provides immediate direction for engaged readers to interact further."
            if has_cta else
            "No explicit call-to-action detected. Adding a clear next step will increase follow-through."
        ),
        "audience_analysis": (
            f"Content length ({word_count} words) and structure are aligned with modern social feed expectations."
        ),
        "tone": "Professional & Informative",
        "suggestions": suggestions[:4],
        "improved_post": improved_post,
    }


def analyze_with_gemini(
    text: str,
    metrics: Dict[str, Any],
    score_data: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Perform semantic analysis using Google Gemini via the official google-genai SDK.
    Gracefully falls back to deterministic rule-based analysis if Gemini is unavailable.

    Returns:
        Dict containing structured review, analysis fields, suggestions, improved post,
        and 'ai_status' ('success' or 'fallback').
    """
    settings = get_settings()
    api_key = settings.GEMINI_API_KEY
    model_name = settings.GEMINI_MODEL or "gemini-3.6-flash"

    # Fallback if API key is missing
    if not api_key or not api_key.strip():
        logger.info("GEMINI_API_KEY not configured. Using deterministic rule-based analysis fallback.")
        fallback = generate_rule_based_fallback(text, metrics, score_data)
        fallback["ai_status"] = "fallback"
        fallback["ai_notice"] = "AI analysis is currently unavailable. The built-in content analysis is still available."
        return fallback

    system_prompt = (
        "You are an expert, professional social media content strategist and editorial analyst. "
        "Your task is to analyze the provided social media draft and return a strict, detailed, and actionable critique. "
        "Rules:\n"
        "1. Analyze ONLY the supplied text.\n"
        "2. Do NOT invent factual claims or change the author's core premise.\n"
        "3. Avoid clickbait or hyperbolic marketing clichÃ©s ('revolutionary', 'game-changing', 'mind-blown').\n"
        "4. In the improved version, maintain an authentic, professional tone while improving structure, clarity, hook, and CTA.\n"
        "5. Do NOT invent a numerical score; our backend calculates the score deterministically.\n"
        "6. Provide 2-4 concrete strengths, 2-4 areas for improvement, and 3-5 specific actionable suggestions."
    )

    user_prompt = (
        f"Please analyze this social media content:\n\n"
        f"--- CONTENT BEGIN ---\n"
        f"{text}\n"
        f"--- CONTENT END ---\n\n"
        f"Deterministic Context:\n"
        f"- Word Count: {metrics.get('word_count', 0)}\n"
        f"- Sentences: {metrics.get('sentence_count', 0)}\n"
        f"- Readability: {metrics.get('readability_grade', 'N/A')}\n"
        f"- Has CTA: {metrics.get('has_cta', False)}\n"
        f"- Has Question: {metrics.get('has_question', False)}\n"
        f"- Calculated Engagement Readiness Score: {score_data.get('total_score', 0)}/100\n"
    )

    try:
        client = genai.Client(api_key=api_key.strip())
        response = client.models.generate_content(
            model=model_name,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
                response_schema=StructuredGeminiAnalysis,
                temperature=0.3,
            ),
        )

        if not response or not response.text:
            raise ValueError("Empty response received from Gemini API.")

        parsed = StructuredGeminiAnalysis.model_validate_json(response.text)
        result = parsed.model_dump()
        result["ai_status"] = "success"
        result["ai_model"] = model_name
        return result

    except Exception as e:
        logger.warning("Gemini analysis call failed: %s. Falling back to rule-based analysis.", str(e))
        fallback = generate_rule_based_fallback(text, metrics, score_data)
        fallback["ai_status"] = "fallback"
        fallback["ai_notice"] = "AI analysis is currently unavailable. The built-in content analysis is still available."
        return fallback
