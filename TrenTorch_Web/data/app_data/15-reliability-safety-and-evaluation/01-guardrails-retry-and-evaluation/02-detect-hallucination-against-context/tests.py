"""
pytest data/app_data/15-reliability-safety-and-evaluation/01-guardrails-retry-and-evaluation/02-detect-hallucination-against-context/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

detect_hallucination = load_solution(
    f"15-reliability-safety-and-evaluation/01-guardrails-retry-and-evaluation/{Path(__file__).resolve().parent.name}"
).detect_hallucination


def test_1_grounded_claim_found_in_context():
    context = ["The Eiffel Tower was completed in 1889."]
    claims = ["The Eiffel Tower was completed in 1889."]
    assert detect_hallucination(claims, context) == [False]


def test_2_hallucinated_claim_not_in_any_context_sentence():
    context = ["The Eiffel Tower was completed in 1889."]
    claims = ["The Eiffel Tower is made of gold."]
    assert detect_hallucination(claims, context) == [True]


def test_3_claim_found_as_substring_of_a_longer_context_sentence():
    context = ["Paris, home to the Eiffel Tower, completed in 1889, is the capital of France."]
    claims = ["completed in 1889"]
    assert detect_hallucination(claims, context) == [False]


def test_4_mixed_batch_of_grounded_and_hallucinated_claims():
    context = ["Water boils at 100C at sea level.", "The sky appears blue due to Rayleigh scattering."]
    claims = ["Water boils at 100C at sea level.", "The moon is made of cheese.", "Rayleigh scattering"]
    assert detect_hallucination(claims, context) == [False, True, False]


def test_5_claim_must_match_a_single_context_sentence_not_span_two():
    context = ["Part one of the fact.", "Part two of the fact."]
    claims = ["Part one of the fact. Part two of the fact."]
    assert detect_hallucination(claims, context) == [True]


def test_6_empty_context_flags_every_claim():
    assert detect_hallucination(["anything"], []) == [True]


def test_7_case_sensitive_near_miss_is_still_hallucinated():
    context = ["The Eiffel Tower was completed in 1889."]
    claims = ["the eiffel tower was completed in 1889."]
    assert detect_hallucination(claims, context) == [True]
