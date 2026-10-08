"""
pytest data/app_data/12-research-papers/02-transformers-and-llms/01-bahdanau-attention/02-attention-weights/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-bahdanau-attention-weights")
attention_weights = _module.attention_weights


import numpy as np


def test_1_weights_sum_to_one():
    assert abs(attention_weights(np.array([0.3, -1.0, 2.0])).sum() - 1.0) < 1e-12


def test_2_equal_scores_give_uniform_weights():
    np.testing.assert_allclose(attention_weights(np.zeros(4)), [0.25] * 4)


def test_3_matches_a_hand_computed_case():
    np.testing.assert_allclose(attention_weights(np.array([0.0, np.log(3.0)])), [0.25, 0.75])


def test_4_is_stable_for_large_scores():
    np.testing.assert_allclose(attention_weights(np.array([1000.0, 1000.0])), [0.5, 0.5])


def test_5_higher_score_gets_higher_weight():
    w = attention_weights(np.array([1.0, 2.0, 0.5]))
    assert w[1] > w[0] > w[2]


def test_6_does_not_mutate_scores():
    s = np.array([1.0, 2.0])
    attention_weights(s)
    np.testing.assert_array_equal(s, [1.0, 2.0])

