"""
pytest data/app_data/12-research-papers/07-agentic-systems/08-generative-agents/02-retrieval-score/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-ga-retrieval-score")
retrieval_score = _module.retrieval_score


def test_1_equal_inputs_return_that_value():
    assert abs(retrieval_score(0.6, 0.6, 0.6) - 0.6) < 1e-12


def test_2_hand_value():
    assert abs(retrieval_score(0.3, 0.6, 0.9) - 0.6) < 1e-12


def test_3_higher_relevance_raises_the_score():
    assert retrieval_score(0.5, 0.5, 0.9) > retrieval_score(0.5, 0.5, 0.1)


def test_4_zero_inputs_give_zero():
    assert retrieval_score(0.0, 0.0, 0.0) == 0.0


def test_5_returns_a_float():
    assert isinstance(retrieval_score(1.0, 1.0, 1.0), float)


def test_6_result_is_within_the_input_range():
    assert 0.0 <= retrieval_score(0.2, 0.8, 0.5) <= 1.0

