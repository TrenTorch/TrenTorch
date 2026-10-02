"""
pytest tests.py
"""

from _load import load_solution

score_transcript = load_solution(__file__).score_transcript

RUBRIC = {
    "task complete": 10,
    "apologize": -2,
    "error": -5,
}


def test_1_single_positive_pattern():
    transcript = [("assistant", "task complete, all done")]
    assert score_transcript(transcript, RUBRIC) == 10


def test_2_negative_pattern_reduces_score():
    transcript = [("assistant", "sorry, an error occurred")]
    assert score_transcript(transcript, RUBRIC) == -5


def test_3_multiple_patterns_across_multiple_turns_sum():
    transcript = [
        ("assistant", "let me apologize for the delay"),
        ("assistant", "task complete now"),
    ]
    assert score_transcript(transcript, RUBRIC) == -2 + 10


def test_4_pattern_repeated_within_one_turn_counts_once():
    transcript = [("assistant", "error, error, error everywhere")]
    assert score_transcript(transcript, RUBRIC) == -5


def test_5_no_pattern_matches_zero_score():
    transcript = [("assistant", "hello there")]
    assert score_transcript(transcript, RUBRIC) == 0


def test_6_multiple_patterns_matching_the_same_turn_all_count():
    transcript = [("assistant", "let me apologize for the error, task complete anyway")]
    assert score_transcript(transcript, RUBRIC) == -2 + -5 + 10


def test_7_empty_transcript_scores_zero():
    assert score_transcript([], RUBRIC) == 0


def test_8_empty_rubric_scores_zero_regardless_of_content():
    assert score_transcript([("assistant", "task complete")], {}) == 0
