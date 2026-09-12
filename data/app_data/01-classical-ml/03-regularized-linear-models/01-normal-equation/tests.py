"""
pytest data/app_data/01-classical-ml/03-regularized-linear-models/01-normal-equation/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"01-classical-ml/03-regularized-linear-models/{Path(__file__).resolve().parent.name}"
)
closed_form_linear_regression = _module.closed_form_linear_regression


def test_closed_form_matches_known_linear_relationship_exactly():
    # Perfectly noiseless data: y = 2x + 3, the closed form should
    # recover this exactly (up to floating-point precision).
    x = np.array([[1.0], [2.0], [3.0], [4.0]])
    y = np.array([5.0, 7.0, 9.0, 11.0])
    weight, bias = closed_form_linear_regression(x, y)
    assert np.isclose(weight[0, 0], 2.0, atol=1e-8)
    assert np.isclose(bias[0], 3.0, atol=1e-8)


def test_closed_form_returns_correct_shapes():
    rng = np.random.default_rng(0)
    x = rng.normal(size=(50, 4))
    y = rng.normal(size=50)
    weight, bias = closed_form_linear_regression(x, y)
    assert weight.shape == (1, 4)
    assert bias.shape == (1,)


def test_closed_form_matches_sklearn_linear_regression():
    rng = np.random.default_rng(1)
    x = rng.normal(size=(200, 3))
    true_w = np.array([2.0, -1.0, 0.5])
    y = x @ true_w + 3.0 + rng.normal(scale=0.1, size=200)
    weight, bias = closed_form_linear_regression(x, y)

    from sklearn.linear_model import LinearRegression

    reference = LinearRegression().fit(x, y)
    assert np.allclose(weight.flatten(), reference.coef_, atol=1e-6)
    assert np.isclose(bias[0], reference.intercept_, atol=1e-6)


def test_closed_form_achieves_lower_or_equal_mse_than_gradient_descent():
    # The exact solution should never be beaten by an iterative
    # approximation (Full Linear Regression Training Loop), it IS the
    # global minimum of MSE for this convex problem.
    train_linear_regression = load_solution(
        "01-classical-ml/01-linear-regression/05-training-loop"
    ).train_linear_regression

    rng = np.random.default_rng(2)
    x = rng.normal(size=(100, 3))
    true_w = np.array([1.5, -2.0, 0.5])
    y = x @ true_w + 1.0 + rng.normal(scale=0.5, size=100)

    closed_weight, closed_bias = closed_form_linear_regression(x, y)
    gd_weight, gd_bias = train_linear_regression(x, y, lr=0.01, epochs=200)

    closed_predictions = x @ closed_weight.T + closed_bias
    gd_predictions = x @ gd_weight.T + gd_bias
    closed_mse = np.mean((closed_predictions.flatten() - y) ** 2)
    gd_mse = np.mean((gd_predictions.flatten() - y) ** 2)

    assert closed_mse <= gd_mse + 1e-6


def test_closed_form_handles_a_singular_design_matrix_gracefully():
    # Two perfectly correlated features make X^T X singular; pinv must
    # still produce a finite, sensible least-squares solution rather
    # than crashing (the exact "Matrix inverse, and when it does not
    # exist" scenario).
    x_base = np.array([[1.0], [2.0], [3.0], [4.0]])
    x = np.hstack([x_base, 2.0 * x_base])  # second column is a multiple of the first
    y = np.array([5.0, 7.0, 9.0, 11.0])
    weight, bias = closed_form_linear_regression(x, y)
    assert np.all(np.isfinite(weight))
    assert np.all(np.isfinite(bias))


def test_closed_form_uses_pinv_not_a_literal_inverse_that_would_crash():
    # Directly targets a mutant that uses np.linalg.inv(X.T @ X) instead
    # of np.linalg.pinv(X): on a singular design matrix, inv() raises
    # LinAlgError, while pinv() succeeds gracefully.
    x_base = np.array([[1.0], [2.0], [3.0]])
    x = np.hstack([x_base, 3.0 * x_base])  # exactly singular X^T X
    y = np.array([1.0, 2.0, 3.0])
    weight, bias = closed_form_linear_regression(x, y)  # must not raise
    assert np.all(np.isfinite(weight))
