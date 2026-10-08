"""
pytest data/app_data/12-research-papers/03-classical-ml-and-learning-theory/10-shap/03-linear-shap/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-shap-linear")
linear_shap = _module.linear_shap


import numpy as np


def test_1_matches_a_hand_value():
    np.testing.assert_allclose(linear_shap(np.array([2.0, -1.0]), np.array([3.0, 4.0]), np.array([1.0, 1.0])), [4.0, -3.0])


def test_2_input_at_the_mean_gives_zero_attributions():
    np.testing.assert_allclose(linear_shap(np.array([5.0, 2.0]), np.array([1.0, 1.0]), np.array([1.0, 1.0])), 0.0)


def test_3_attributions_sum_to_the_prediction_difference():
    w = np.array([1.0, 2.0, -3.0])
    x = np.array([4.0, 0.0, 1.0])
    m = np.array([1.0, 1.0, 1.0])
    phi = linear_shap(w, x, m)
    assert abs(phi.sum() - (w @ x - w @ m)) < 1e-12


def test_4_output_shape_matches_features():
    assert linear_shap(np.ones(4), np.ones(4), np.zeros(4)).shape == (4,)


def test_5_zero_weight_gives_zero_attribution():
    assert linear_shap(np.array([0.0]), np.array([9.0]), np.array([1.0]))[0] == 0.0


def test_6_does_not_mutate_inputs():
    x = np.array([2.0])
    linear_shap(np.array([1.0]), x, np.array([0.0]))
    np.testing.assert_array_equal(x, [2.0])

