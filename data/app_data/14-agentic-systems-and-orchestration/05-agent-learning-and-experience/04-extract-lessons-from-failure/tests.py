"""
pytest data/app_data/14-agentic-systems-and-orchestration/05-agent-learning-and-experience/04-extract-lessons-from-failure/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

extract_lesson = load_solution(
    f"14-agentic-systems-and-orchestration/05-agent-learning-and-experience/{Path(__file__).resolve().parent.name}"
).extract_lesson

KEYWORDS = {
    "timeout": "Add a retry with backoff for slow external calls.",
    "permission denied": "Check the tool's credentials before running.",
    "not found": "Validate the target exists before acting on it.",
}


def test_1_matching_pattern_returns_its_lesson():
    assert (
        extract_lesson("request failed: timeout after 30s", KEYWORDS)
        == "Add a retry with backoff for slow external calls."
    )


def test_2_no_match_returns_generic_fallback():
    assert (
        extract_lesson("something totally unexpected happened", KEYWORDS)
        == "No specific lesson identified -- investigate manually."
    )


def test_3_first_matching_pattern_wins_when_multiple_match():
    keywords = {"error": "generic error lesson", "timeout": "timeout-specific lesson"}
    assert extract_lesson("error: timeout occurred", keywords) == "generic error lesson"


def test_4_pattern_matches_as_plain_substring():
    assert (
        extract_lesson("file not found on disk", KEYWORDS)
        == "Validate the target exists before acting on it."
    )


def test_5_empty_error_keywords_always_falls_back():
    assert (
        extract_lesson("timeout", {}) == "No specific lesson identified -- investigate manually."
    )


def test_6_case_sensitive_matching():
    assert (
        extract_lesson("TIMEOUT occurred", KEYWORDS)
        == "No specific lesson identified -- investigate manually."
    )
