"""
pytest data/app_data/12-research-papers/09-sequence-models-and-attention/04-show-attend-tell/01-soft-context/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-sat-soft-context")
soft_context = _module.soft_context


import numpy as np


def test_1_one_hot_attention_picks_a_location():
    feats = np.array([[1.0, 2.0], [3.0, 4.0]])
    np.testing.assert_allclose(soft_context(np.array([0.0, 1.0]), feats), [3.0, 4.0])


def test_2_uniform_attention_averages():
    feats = np.array([[0.0], [4.0]])
    np.testing.assert_allclose(soft_context(np.array([0.5, 0.5]), feats), [2.0])


def test_3_output_has_feature_dimension():
    assert soft_context(np.ones(4) / 4, np.ones((4, 7))).shape == (7,)


def test_4_result_lies_in_feature_hull():
    feats = np.array([[0.0], [10.0]])
    out = soft_context(np.array([0.3, 0.7]), feats)
    assert 0.0 <= out[0] <= 10.0


def test_5_matches_hand_value():
    np.testing.assert_allclose(soft_context(np.array([0.25, 0.75]), np.array([[4.0], [8.0]])), [7.0])


def test_6_does_not_mutate_inputs():
    feats = np.ones((2, 2))
    soft_context(np.array([0.5, 0.5]), feats)
    np.testing.assert_array_equal(feats, np.ones((2, 2)))

