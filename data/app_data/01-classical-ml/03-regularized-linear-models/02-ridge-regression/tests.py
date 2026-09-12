"""
pytest data/app_data/01-classical-ml/03-regularized-linear-models/02-ridge-regression/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"01-classical-ml/03-regularized-linear-models/{Path(__file__).resolve().parent.name}"
)
ridge_regression_closed_form = _module.ridge_regression_closed_form

closed_form_linear_regression = load_solution(
    "01-classical-ml/03-regularized-linear-models/01-normal-equation"
).closed_form_linear_regression


def test_ridge_with_zero_alpha_matches_plain_normal_equation():
    rng = np.random.default_rng(0)
    x = rng.normal(size=(50, 3))
    y = rng.normal(size=50)
    ridge_weight, ridge_bias = ridge_regression_closed_form(x, y, alpha=0.0)
    plain_weight, plain_bias = closed_form_linear_regression(x, y)
    assert np.allclose(ridge_weight, plain_weight, atol=1e-6)
    assert np.allclose(ridge_bias, plain_bias, atol=1e-6)


def test_ridge_matches_sklearn_ridge():
    rng = np.random.default_rng(1)
    x = rng.normal(size=(100, 4))
    true_w = np.array([2.0, -1.0, 0.5, 3.0])
    y = x @ true_w + 3.0 + rng.normal(scale=0.5, size=100)
    weight, bias = ridge_regression_closed_form(x, y, alpha=2.0)

    from sklearn.linear_model import Ridge

    reference = Ridge(alpha=2.0).fit(x, y)
    assert np.allclose(weight.flatten(), reference.coef_, atol=1e-6)
    assert np.isclose(bias[0], reference.intercept_, atol=1e-6)


def test_larger_alpha_shrinks_weights_toward_zero():
    rng = np.random.default_rng(2)
    x = rng.normal(size=(80, 3))
    true_w = np.array([5.0, -3.0, 2.0])
    y = x @ true_w + rng.normal(scale=1.0, size=80)

    weak_weight, _ = ridge_regression_closed_form(x, y, alpha=0.01)
    strong_weight, _ = ridge_regression_closed_form(x, y, alpha=100.0)
    assert np.linalg.norm(strong_weight) < np.linalg.norm(weak_weight)


def test_ridge_never_regularizes_the_bias():
    # A dataset shifted far from zero should still recover roughly the
    # true intercept even under strong regularization, since the bias
    # itself isn't penalized.
    rng = np.random.default_rng(3)
    x = rng.normal(size=(200, 2))
    y = x @ np.array([1.0, 1.0]) + 1000.0 + rng.normal(scale=0.1, size=200)
    _, bias = ridge_regression_closed_form(x, y, alpha=10.0)
    assert bias[0] > 500.0  # bias should stay large despite strong regularization


def test_ridge_handles_a_singular_design_matrix_that_breaks_plain_regression():
    # The exact scenario the identity-matrix addition exists to fix:
    # two perfectly correlated features make the unregularized system
    # singular, ridge's added term keeps it invertible.
    x_base = np.array([[1.0], [2.0], [3.0], [4.0], [5.0]])
    x = np.hstack([x_base, 2.0 * x_base])
    y = np.array([2.0, 4.0, 6.0, 8.0, 10.0])
    weight, bias = ridge_regression_closed_form(x, y, alpha=1.0)
    assert np.all(np.isfinite(weight))
    assert np.all(np.isfinite(bias))


def test_ridge_does_not_regularize_the_bias_entry_of_the_penalty_matrix():
    # Directly targets a mutant that applies alpha to the full identity
    # matrix, including the bias position, instead of zeroing it out.
    # With a heavily shifted dataset and strong alpha, failing to
    # exclude the bias would shrink it substantially toward zero.
    rng = np.random.default_rng(4)
    x = rng.normal(size=(300, 2))
    true_bias = 500.0
    y = x @ np.array([1.0, 1.0]) + true_bias + rng.normal(scale=0.1, size=300)
    _, bias = ridge_regression_closed_form(x, y, alpha=50.0)
    assert bias[0] > 400.0  # a mutant that regularizes the bias would shrink this dramatically
