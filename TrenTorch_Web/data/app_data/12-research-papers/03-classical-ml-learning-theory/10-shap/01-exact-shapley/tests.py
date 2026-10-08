"""
pytest data/app_data/12-research-papers/03-classical-ml-and-learning-theory/10-shap/01-exact-shapley/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-shap-exact-shapley")
shapley_exact = _module.shapley_exact


import numpy as np


def test_1_linear_model_gives_weight_times_difference():
    w = np.array([2.0, -1.0])
    f = lambda v: float(w @ v)
    phi = shapley_exact(f, np.array([3.0, 4.0]), np.zeros(2))
    np.testing.assert_allclose(phi, [6.0, -4.0], atol=1e-9)


def test_2_efficiency_sums_to_the_output_difference():
    f = lambda v: float(v[0] * v[1] + v[2])
    x = np.array([2.0, 3.0, 1.0])
    b = np.zeros(3)
    phi = shapley_exact(f, x, b)
    assert abs(phi.sum() - (f(x) - f(b))) < 1e-9


def test_3_single_feature_gets_the_full_difference():
    f = lambda v: float(3.0 * v[0])
    np.testing.assert_allclose(shapley_exact(f, np.array([2.0]), np.array([0.0])), [6.0])


def test_4_irrelevant_feature_gets_zero():
    f = lambda v: float(v[0] ** 2)
    phi = shapley_exact(f, np.array([3.0, 100.0]), np.array([1.0, 0.0]))
    assert abs(phi[1]) < 1e-9


def test_5_symmetric_features_get_equal_credit():
    f = lambda v: float(v[0] + v[1])
    phi = shapley_exact(f, np.array([1.0, 1.0]), np.array([0.0, 0.0]))
    assert abs(phi[0] - phi[1]) < 1e-9


def test_6_does_not_mutate_inputs():
    x = np.array([1.0, 2.0])
    b = np.zeros(2)
    shapley_exact(lambda v: float(v.sum()), x, b)
    np.testing.assert_array_equal(x, [1.0, 2.0])

