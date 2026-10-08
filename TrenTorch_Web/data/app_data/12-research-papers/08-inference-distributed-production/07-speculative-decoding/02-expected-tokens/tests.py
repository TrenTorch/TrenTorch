"""
pytest data/app_data/12-research-papers/08-inference-distributed-and-production/07-speculative-decoding/02-expected-tokens/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-spec-expected-tokens")
expected_tokens_accepted = _module.expected_tokens_accepted


def test_1_zero_acceptance_gives_one_token():
    assert abs(expected_tokens_accepted(0.0, 4) - 1.0) < 1e-12


def test_2_hand_value():
    assert abs(expected_tokens_accepted(0.5, 2) - 1.75) < 1e-12


def test_3_more_drafts_help_when_acceptance_is_high():
    assert expected_tokens_accepted(0.9, 8) > expected_tokens_accepted(0.9, 2)


def test_4_result_is_at_least_one():
    assert expected_tokens_accepted(0.3, 3) >= 1.0


def test_5_result_is_at_most_gamma_plus_one():
    assert expected_tokens_accepted(0.99, 5) <= 6.0 + 1e-9


def test_6_returns_a_float():
    assert isinstance(expected_tokens_accepted(0.5, 1), float)

