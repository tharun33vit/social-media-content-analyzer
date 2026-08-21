"""Deterministic content analyzer and 100-point engagement scoring engine."""

import re
from typing import Any, Dict, List


CTA_PATTERNS = [
    r"\b(?:click|tap)\b(?:\s+(?:here|the\s+link|below|on))?",
    r"\blink\s+in\s+(?:bio|comments|description)\b",
    r"\b(?:comment|drop|share)\s+(?:below|your|down|thoughts)\b",
    r"\b(?:follow|subscribe|join|sign\s*up|register)\b",
    r"\b(?:save\s+this|save\s+for\s+later|bookmark|repost|retweet)\b",
    r"\b(?:dm\s+me|send\s+a\s+message|reach\s+out|check\s+out|let\s+me\s+know)\b",
    r"\b(?:what\s+do\s+you\s+think|agree\s*\?|thoughts\s*\?)\b",
]

CONVERSATION_TRIGGERS = [
    r"\bwhat\s+are\s+your\b",
    r"\bwhat\s+do\s+you\b",
    r"\bhave\s+you\s+ever\b",
    r"\bhow\s+do\s+you\b",
    r"\bwhich\s+one\b",
    r"\blet\s+me\s+know\b",
    r"\bdrop\s+a\b",
    r"\bthoughts\s*\?",
    r"\bagree\s*\?",
]


def count_syllables(word: str) -> int:
    """Heuristic syllable counter for readability calculations."""
    word = word.lower().strip()
    if not word:
        return 0
    if len(word) <= 3:
        return 1
    word = re.sub(r"(?:[^laeiouy]|ed|es|e)$", "", word)
    word = re.sub(r"^y", "", word)
    matches = re.findall(r"[aeiouy]{1,2}", word)
    return max(1, len(matches))


def calculate_flesch_reading_ease(words: List[str], sentences: List[str]) -> float:
    """Calculate standard Flesch Reading Ease score."""
    if not words or not sentences:
        return 0.0

    total_words = len(words)
    total_sentences = max(1, len(sentences))
    total_syllables = sum(count_syllables(w) for w in words)

    asl = total_words / total_sentences
    asw = total_syllables / total_words

    score = 206.835 - (1.015 * asl) - (84.6 * asw)
    return round(max(0.0, min(100.0, score)), 1)


def analyze_deterministic_metrics(text: str) -> Dict[str, Any]:
    """
    Perform objective, deterministic text analysis.

    Returns:
        Dict containing word, character, sentence, paragraph, hashtag, mention,
        URL, question, CTA, hook, and readability metrics.
    """
    normalized_text = text.strip()
    if not normalized_text:
        return {
            "word_count": 0,
            "character_count": 0,
            "sentence_count": 0,
            "paragraph_count": 0,
            "hashtag_count": 0,
            "hashtags": [],
            "mention_count": 0,
            "mentions": [],
            "url_count": 0,
            "urls": [],
            "question_count": 0,
            "has_question": False,
            "cta_count": 0,
            "has_cta": False,
            "detected_ctas": [],
            "first_line": "",
            "first_line_length": 0,
            "average_sentence_length": 0.0,
            "readability_score": 0.0,
            "readability_grade": "N/A",
        }

    # Paragraphs
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", normalized_text) if p.strip()]
    paragraph_count = max(1, len(paragraphs))

    # Lines & First Line (Hook)
    lines = [line.strip() for line in normalized_text.splitlines() if line.strip()]
    first_line = lines[0] if lines else ""

    # Words
    raw_words = re.findall(r"\b[\w'-]+\b", normalized_text)
    word_count = len(raw_words)
    character_count = len(normalized_text)

    # Sentences (splitting on punctuation while respecting abbreviations)
    sentence_splits = [s.strip() for s in re.split(r"[.!?]+(?:\s+|\n+|$)", normalized_text) if s.strip()]
    sentence_count = max(1, len(sentence_splits))
    avg_sentence_len = round(word_count / sentence_count, 1) if sentence_count > 0 else 0.0

    # Hashtags
    hashtags = re.findall(r"#\w+", normalized_text)
    # Mentions
    mentions = re.findall(r"@\w+", normalized_text)
    # URLs
    urls = re.findall(r"https?://\S+|www\.\S+", normalized_text)

    # Questions
    questions = re.findall(r"\?", normalized_text)
    question_count = len(questions)

    # CTAs
    detected_ctas: List[str] = []
    for pattern in CTA_PATTERNS:
        matches = re.findall(pattern, normalized_text, flags=re.IGNORECASE)
        for m in matches:
            if m.strip() and m.strip() not in detected_ctas:
                detected_ctas.append(m.strip())

    # Readability
    readability_score = calculate_flesch_reading_ease(raw_words, sentence_splits)
    if readability_score >= 80:
        readability_grade = "Very Easy"
    elif readability_score >= 65:
        readability_grade = "Easy / Conversational"
    elif readability_score >= 50:
        readability_grade = "Standard"
    elif readability_score >= 30:
        readability_grade = "Fairly Difficult"
    else:
        readability_grade = "Difficult / Academic"

    return {
        "word_count": word_count,
        "character_count": character_count,
        "sentence_count": sentence_count,
        "paragraph_count": paragraph_count,
        "hashtag_count": len(hashtags),
        "hashtags": hashtags,
        "mention_count": len(mentions),
        "mentions": mentions,
        "url_count": len(urls),
        "urls": urls,
        "question_count": question_count,
        "has_question": question_count > 0,
        "cta_count": len(detected_ctas),
        "has_cta": len(detected_ctas) > 0,
        "detected_ctas": detected_ctas,
        "first_line": first_line,
        "first_line_length": len(first_line),
        "average_sentence_length": avg_sentence_len,
        "readability_score": readability_score,
        "readability_grade": readability_grade,
    }


def calculate_engagement_score(metrics: Dict[str, Any], text: str) -> Dict[str, Any]:
    """
    Calculate a transparent 100-point Content & Engagement Readiness Score.

    7 Structured Dimensions:
    1. Hook / Opening (20 pts)
    2. Clarity & Readability (20 pts)
    3. Engagement Potential (20 pts)
    4. Call-to-Action (15 pts)
    5. Content Structure (10 pts)
    6. Hashtag & Metadata Strategy (5 pts)
    7. Audience Relevance & Format Fit (10 pts)
    """
    if not text or not text.strip() or metrics.get("word_count", 0) == 0:
        return {
            "total_score": 0,
            "verdict": "No readable content detected to evaluate.",
            "breakdown": {
                "hook_opening": {"score": 0, "max": 20, "label": "Hook & Opening"},
                "clarity_readability": {"score": 0, "max": 20, "label": "Clarity & Readability"},
                "engagement_potential": {"score": 0, "max": 20, "label": "Engagement Potential"},
                "call_to_action": {"score": 0, "max": 15, "label": "Call-to-Action"},
                "content_structure": {"score": 0, "max": 10, "label": "Content Structure"},
                "hashtag_strategy": {"score": 0, "max": 5, "label": "Hashtag Strategy"},
                "audience_format": {"score": 0, "max": 10, "label": "Audience & Format Fit"},
            },
            "disclaimer": "This score is an analytical heuristic for engagement readiness, not a guarantee of impressions, reach, or likes.",
        }

    first_line = metrics.get("first_line", "")
    first_line_len = len(first_line)
    word_count = metrics.get("word_count", 0)
    avg_sentence_len = metrics.get("average_sentence_length", 0.0)
    readability = metrics.get("readability_score", 0.0)
    question_count = metrics.get("question_count", 0)
    detected_ctas = metrics.get("detected_ctas", [])
    paragraph_count = metrics.get("paragraph_count", 1)
    hashtag_count = metrics.get("hashtag_count", 0)

    # 1. Hook / Opening (Max 20 pts)
    hook_score = 0
    if 25 <= first_line_len <= 110:
        hook_score += 10
    elif 12 <= first_line_len < 25 or 110 < first_line_len <= 160:
        hook_score += 7
    elif first_line_len > 0:
        hook_score += 4

    # Hook engagement triggers (question mark in hook, numbers, or strong opener)
    if "?" in first_line:
        hook_score += 6
    elif re.search(r"\b(?:\d+|how\s+to|why|stop|never|secret|guide|lesson|framework)\b", first_line, re.I):
        hook_score += 6
    else:
        hook_score += 3

    if len(first_line.split()) >= 4:
        hook_score += 4
    else:
        hook_score += 2
    hook_score = min(20, hook_score)

    # 2. Clarity & Readability (Max 20 pts)
    clarity_score = 0
    # Sentence length
    if 8 <= avg_sentence_len <= 18:
        clarity_score += 10
    elif 18 < avg_sentence_len <= 24:
        clarity_score += 7
    elif 4 <= avg_sentence_len < 8:
        clarity_score += 6
    else:
        clarity_score += 4

    # Readability score
    if 60 <= readability <= 85:
        clarity_score += 10
    elif 50 <= readability < 60 or 85 < readability <= 95:
        clarity_score += 8
    elif 35 <= readability < 50:
        clarity_score += 5
    else:
        clarity_score += 3
    clarity_score = min(20, clarity_score)

    # 3. Engagement Potential (Max 20 pts)
    engagement_score = 0
    # Questions
    if 1 <= question_count <= 3:
        engagement_score += 8
    elif question_count > 3:
        engagement_score += 5
    else:
        engagement_score += 2

    # Conversation triggers
    has_conv_trigger = any(re.search(p, text, re.I) for p in CONVERSATION_TRIGGERS)
    if has_conv_trigger:
        engagement_score += 6
    else:
        engagement_score += 2

    # Reader-oriented pronouns (you, your, we)
    you_count = len(re.findall(r"\b(?:you|your|you're|we|our)\b", text, re.I))
    if you_count >= 2:
        engagement_score += 6
    elif you_count == 1:
        engagement_score += 4
    else:
        engagement_score += 2
    engagement_score = min(20, engagement_score)

    # 4. Call-to-Action (Max 15 pts)
    cta_score = 0
    if len(detected_ctas) >= 1:
        cta_score += 10
        # Position check: is CTA in bottom half or separate line?
        last_paragraph = text.split("\n\n")[-1] if "\n\n" in text else text
        if any(cta.lower() in last_paragraph.lower() for cta in detected_ctas):
            cta_score += 5
        else:
            cta_score += 3
    else:
        cta_score = 2  # Baseline minimal score when no explicit CTA is present
    cta_score = min(15, cta_score)

    # 5. Content Structure (Max 10 pts)
    structure_score = 0
    if paragraph_count >= 2:
        structure_score += 6
    elif "\n" in text:
        structure_score += 4
    else:
        structure_score += 2

    # Scannability / lists / emojis / bullet formatting
    if re.search(r"(?:^|\n)\s*(?:[•\-*]|\d+\.)", text):
        structure_score += 4
    elif paragraph_count >= 3:
        structure_score += 4
    else:
        structure_score += 2
    structure_score = min(10, structure_score)

    # 6. Hashtag & Metadata Strategy (Max 5 pts)
    hashtag_score = 0
    if 1 <= hashtag_count <= 5:
        hashtag_score = 5
    elif 6 <= hashtag_count <= 8:
        hashtag_score = 3
    elif hashtag_count > 8:
        hashtag_score = 2
    else:
        # Zero hashtags is common on some platforms (LinkedIn/X long-form), given reasonable partial credit
        hashtag_score = 3

    # 7. Audience Relevance & Format Fit (Max 10 pts)
    audience_score = 0
    if 40 <= word_count <= 260:
        audience_score += 6
    elif 25 <= word_count < 40 or 260 < word_count <= 450:
        audience_score += 5
    elif 450 < word_count <= 800:
        audience_score += 3
    else:
        audience_score += 2

    # Formatting balance (mentions, link placement, character balance)
    if len(metrics.get("urls", [])) <= 2:
        audience_score += 4
    else:
        audience_score += 2
    audience_score = min(10, audience_score)

    total_score = hook_score + clarity_score + engagement_score + cta_score + structure_score + hashtag_score + audience_score
    total_score = max(0, min(100, total_score))

    # Verdict summary
    if total_score >= 85:
        verdict = "High engagement readiness with a compelling hook, balanced structure, and clear action path."
    elif total_score >= 70:
        verdict = "Good foundational post with strong readability and minor room for stronger audience interaction."
    elif total_score >= 55:
        verdict = "Moderate readiness. Would benefit from a sharper opening hook, clearer CTA, or tighter paragraph breaks."
    else:
        verdict = "Needs improvement in hook strength, conversational pacing, and explicit next steps for readers."

    breakdown = {
        "hook_opening": {"score": hook_score, "max": 20, "label": "Hook & Opening"},
        "clarity_readability": {"score": clarity_score, "max": 20, "label": "Clarity & Readability"},
        "engagement_potential": {"score": engagement_score, "max": 20, "label": "Engagement Potential"},
        "call_to_action": {"score": cta_score, "max": 15, "label": "Call-to-Action"},
        "content_structure": {"score": structure_score, "max": 10, "label": "Content Structure"},
        "hashtag_strategy": {"score": hashtag_score, "max": 5, "label": "Hashtag Strategy"},
        "audience_format": {"score": audience_score, "max": 10, "label": "Audience & Format Fit"},
    }

    return {
        "total_score": total_score,
        "verdict": verdict,
        "breakdown": breakdown,
        "disclaimer": "This score is an analytical heuristic for engagement readiness, not a guarantee of impressions, reach, or likes.",
    }
