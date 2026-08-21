"""Tests for deterministic content analyzer and 100-point engagement scoring engine."""

from app.services.content_analyzer import analyze_deterministic_metrics, calculate_engagement_score


def test_deterministic_metrics_calculation():
    """Verify objective counting metrics."""
    sample_text = (
        "Are you launching your product this month?\n\n"
        "Here are 3 tips to boost organic signups:\n"
        "- Clear value proposition\n"
        "- Social proof testimonials\n\n"
        "Comment below with your thoughts! Visit https://example.com for more info.\n"
        "#ProductLaunch #Startups @techfounder"
    )

    metrics = analyze_deterministic_metrics(sample_text)
    assert metrics["word_count"] > 20
    assert metrics["sentence_count"] >= 3
    assert metrics["paragraph_count"] >= 3
    assert metrics["hashtag_count"] == 2
    assert "#ProductLaunch" in metrics["hashtags"]
    assert metrics["mention_count"] == 1
    assert "@techfounder" in metrics["mentions"]
    assert metrics["url_count"] == 1
    assert metrics["has_question"] is True
    assert metrics["has_cta"] is True
    assert "comment below" in [c.lower() for c in metrics["detected_ctas"]]
    assert metrics["first_line"] == "Are you launching your product this month?"
    assert metrics["readability_score"] > 0


def test_calculate_engagement_score_bounds():
    """Verify that the engagement score calculates between 0 and 100 with full breakdown."""
    sample_text = (
        "Do you want to double your reach without spending on ads?\n\n"
        "Focus on these two strategies:\n"
        "1. Write strong, curiosity-driven hooks.\n"
        "2. Engage with commenters in the first 30 minutes.\n\n"
        "What is your top engagement tip? Share your thoughts below 👇\n\n"
        "#SocialGrowth #MarketingTips"
    )
    metrics = analyze_deterministic_metrics(sample_text)
    score_data = calculate_engagement_score(metrics, sample_text)

    assert 0 <= score_data["total_score"] <= 100
    assert "verdict" in score_data
    assert "disclaimer" in score_data
    assert "breakdown" in score_data

    breakdown = score_data["breakdown"]
    assert "hook_opening" in breakdown
    assert "clarity_readability" in breakdown
    assert "engagement_potential" in breakdown
    assert "call_to_action" in breakdown
    assert "content_structure" in breakdown
    assert "hashtag_strategy" in breakdown
    assert "audience_format" in breakdown

    # Sum of max points must equal 100
    total_max = sum(item["max"] for item in breakdown.values())
    assert total_max == 100


def test_empty_text_metrics():
    """Verify empty text produces 0 metrics and reasonable baseline score."""
    metrics = analyze_deterministic_metrics("")
    assert metrics["word_count"] == 0
    score_data = calculate_engagement_score(metrics, "")
    assert score_data["total_score"] <= 30
