"""
pytest data/app_data/01-classical-ml/03-regularized-linear-models/03-lasso-regression/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"01-classical-ml/03-regularized-linear-models/{Path(__file__).resolve().parent.name}"
)
soft_threshold = _module.soft_threshold
lasso_regression_coordinate_descent = _module.lasso_regression_coordinate_descent


def test_soft_threshold_zeros_out_small_values():
    result = soft_threshold(np.array([0.05, -0.05]), threshold=0.1)
    assert np.array_equal(result, [0.0, 0.0])


def test_soft_threshold_shrinks_large_values_by_threshold():
    result = soft_threshold(np.array([5.0, -5.0]), threshold=1.0)
    assert np.allclose(result, [4.0, -4.0])


def test_soft_threshold_preserves_sign():
    positive = soft_threshold(np.array([3.0]), threshold=1.0)[0]
    negative = soft_threshold(np.array([-3.0]), threshold=1.0)[0]
    assert positive > 0.0
    assert negative < 0.0
    assert np.isclose(positive, -negative)


def test_lasso_matches_sklearn_lasso():
    rng = np.random.default_rng(0)
    x = rng.normal(size=(200, 6))
    true_w = np.array([2.0, 0.0, 0.0, -1.0, 0.0, 3.0])
    y = x @ true_w + 3.0 + rng.normal(scale=0.3, size=200)
    weight, bias = lasso_regression_coordinate_descent(x, y, alpha=0.3, epochs=200)

    from sklearn.linear_model import Lasso

    reference = Lasso(alpha=0.3, max_iter=10000).fit(x, y)
    assert np.allclose(weight.flatten(), reference.coef_, atol=1e-4)
    assert np.isclose(bias[0], reference.intercept_, atol=1e-4)


def test_lasso_produces_exact_zeros_for_irrelevant_features():
    # The defining property this question exists to demonstrate: unlike
    # Ridge, Lasso can drive irrelevant feature weights to EXACTLY zero.
    rng = np.random.default_rng(1)
    x = rng.normal(size=(300, 5))
    true_w = np.array([3.0, 0.0, 0.0, 0.0, -2.0])  # only features 0 and 4 matter
    y = x @ true_w + rng.normal(scale=0.1, size=300)
    weight, _ = lasso_regression_coordinate_descent(x, y, alpha=0.5, epochs=200)
    assert np.isclose(weight[0, 1], 0.0, atol=1e-8)
    assert np.isclose(weight[0, 2], 0.0, atol=1e-8)
    assert np.isclose(weight[0, 3], 0.0, atol=1e-8)
    assert abs(weight[0, 0]) > 0.5
    assert abs(weight[0, 4]) > 0.5


def test_larger_alpha_produces_sparser_solutions():
    rng = np.random.default_rng(2)
    x = rng.normal(size=(300, 8))
    true_w = np.zeros(8)
    true_w[[0, 3, 6]] = [3.0, -2.0, 1.5]
    y = x @ true_w + rng.normal(scale=0.2, size=300)

    weak_weight, _ = lasso_regression_coordinate_descent(x, y, alpha=0.01, epochs=200)
    strong_weight, _ = lasso_regression_coordinate_descent(x, y, alpha=2.0, epochs=200)

    weak_nonzero = np.sum(np.abs(weak_weight) > 1e-6)
    strong_nonzero = np.sum(np.abs(strong_weight) > 1e-6)
    assert strong_nonzero <= weak_nonzero


def test_soft_threshold_is_not_confused_with_plain_shrinkage():
    # Directly targets a mutant that shrinks toward zero without ever
    # snapping to exact zero (e.g. multiplying by a constant factor
    # instead of subtracting the threshold): a value smaller than the
    # threshold must become EXACTLY 0.0, not just a smaller nonzero number.
    result = soft_threshold(np.array([0.3]), threshold=0.5)[0]
    assert result == 0.0
