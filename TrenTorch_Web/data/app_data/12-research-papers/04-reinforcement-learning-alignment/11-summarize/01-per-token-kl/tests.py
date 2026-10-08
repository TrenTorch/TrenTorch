"""
pytest data/app_data/12-research-papers/04-reinforcement-learning-and-alignment/11-summarize/01-per-token-kl/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-summarize-per-token-kl")
per_token_kl = _module.per_token_kl


import numpy as np


def test_1_identical_models_give_zero_kl():
    assert abs(per_token_kl(np.array([-1.0, -2.0]), np.array([-1.0, -2.0]))) < 1e-12


def test_2_matches_a_hand_value():
    assert abs(per_token_kl(np.array([-1.0, -1.0]), np.array([-2.0, -3.0])) - 3.0) < 1e-12


def test_3_policy_more_confident_than_reference_is_positive():
    assert per_token_kl(np.array([-0.1]), np.array([-2.0])) > 0


def test_4_returns_a_python_float():
    assert isinstance(per_token_kl(np.zeros(2), np.zeros(2)), float)


def test_5_longer_sequences_accumulate_more():
    a = per_token_kl(np.array([-1.0]), np.array([-2.0]))
    b = per_token_kl(np.array([-1.0, -1.0]), np.array([-2.0, -2.0]))
    assert abs(b - 2 * a) < 1e-12


def test_6_does_not_mutate_inputs():
    lp = np.array([-1.0])
    per_token_kl(lp, np.array([-2.0]))
    np.testing.assert_array_equal(lp, [-1.0])

