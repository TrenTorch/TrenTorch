"""
pytest data/app_data/12-research-papers/08-inference-distributed-and-production/07-speculative-decoding/01-acceptance/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-spec-acceptance")
acceptance_prob = _module.acceptance_prob


def test_1_draft_undervalued_by_target_is_accepted_always():
    assert acceptance_prob(0.6, 0.3) == 1.0


def test_2_hand_value_when_target_is_smaller():
    assert abs(acceptance_prob(0.2, 0.4) - 0.5) < 1e-12


def test_3_equal_probabilities_accept_always():
    assert acceptance_prob(0.3, 0.3) == 1.0


def test_4_result_is_between_zero_and_one():
    assert 0.0 <= acceptance_prob(0.1, 0.9) <= 1.0


def test_5_returns_a_float():
    assert isinstance(acceptance_prob(0.5, 0.5), float)


def test_6_zero_target_probability_is_rejected():
    assert acceptance_prob(0.0, 0.5) == 0.0

