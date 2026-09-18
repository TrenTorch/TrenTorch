"""
pytest data/app_data/01-classical-ml/03-regularized-linear-models/06-ridge-regression-gaussian-elimination/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"01-classical-ml/03-regularized-linear-models/{Path(__file__).resolve().parent.name}"
)
gaussian_elimination_solve = _module.gaussian_elimination_solve
ridge_regression_predict = _module.ridge_regression_predict


def test_gaussian_elimination_requires_pivoting_to_avoid_a_zero_pivot():
    # A naive elimination (always eliminate using row k as-is) hits a
    # zero pivot at column 0 here and either crashes or produces NaN.
    # Only swapping in the larger row first (partial pivoting) survives.
    a = np.array([[0.0, 1.0], [1.0, 1.0]])
    b = np.array([1.0, 3.0])
    x = gaussian_elimination_solve(a, b)
    assert np.allclose(a @ x, b, atol=1e-8)
    assert np.allclose(x, [2.0, 1.0], atol=1e-8)


def test_gaussian_elimination_matches_numpy_solve_on_random_systems():
    rng = np.random.default_rng(0)
    for n in (2, 3, 5, 8):
        a = rng.normal(size=(n, n)) + n * np.eye(n)  # diagonally dominant, well-conditioned
        b = rng.normal(size=n)
        x = gaussian_elimination_solve(a, b)
        expected = np.linalg.solve(a, b)
        assert np.allclose(x, expected, atol=1e-6)


def test_ridge_matches_the_exact_line_from_example_one():
    # y = 2x + 1 exactly, lam=0: closed form should recover it exactly.
    x = np.array([[1.0], [2.0], [3.0]])
    y = np.array([3.0, 5.0, 7.0])
    queries = np.array([[4.0], [5.0]])
    predictions = ridge_regression_predict(x, y, 0.0, queries)
    assert np.allclose(predictions, [9.0, 11.0], atol=1e-6)


def test_ridge_matches_example_two_with_regularization():
    x = np.array([[1.0, 1.0], [2.0, 1.0], [1.0, 2.0], [2.0, 2.0]])
    y = np.array([4.0, 7.0, 3.0, 6.0])
    queries = np.array([[3.0, 3.0], [0.0, 0.0]])
    predictions = ridge_regression_predict(x, y, 0.5, queries)
    assert np.allclose(predictions, [60.0 / 7.0, 8.0 / 7.0], atol=1e-4)


def test_lambda_zero_matches_the_plain_normal_equation():
    rng = np.random.default_rng(1)
    x = rng.normal(size=(60, 3))
    true_w = np.array([2.0, -1.0, 0.5])
    y = x @ true_w + 3.0 + rng.normal(scale=0.05, size=60)
    queries = rng.normal(size=(10, 3))

    predictions = ridge_regression_predict(x, y, 0.0, queries)

    # Independent oracle: solve the same augmented normal equation with
    # numpy's own solver directly, never routing through the student's
    # gaussian_elimination_solve.
    x_aug = np.hstack([x, np.ones((60, 1))])
    theta = np.linalg.solve(x_aug.T @ x_aug, x_aug.T @ y)
    q_aug = np.hstack([queries, np.ones((10, 1))])
    expected = q_aug @ theta
    assert np.allclose(predictions, expected, atol=1e-4)


def test_this_question_regularizes_the_bias_unlike_ridge_regression_l2():
    # Deliberately the OPPOSITE convention from `Ridge Regression (L2)`:
    # here the bias IS penalized, so a large lam should shrink it toward
    # zero too, not leave it untouched.
    rng = np.random.default_rng(2)
    x = rng.normal(size=(200, 2))
    y = x @ np.array([1.0, 1.0]) + 1000.0 + rng.normal(scale=0.1, size=200)

    weak = ridge_regression_predict(x, y, 0.001, np.zeros((1, 2)))[0]
    strong = ridge_regression_predict(x, y, 1e6, np.zeros((1, 2)))[0]
    # A prediction at the origin is just the bias term -- under an
    # enormous lam, a bias that's actually regularized collapses toward
    # zero; a mutant that zeroes the last diagonal entry (copying the
    # OTHER question's convention) would leave it near 1000 instead.
    assert abs(strong) < abs(weak) / 10


def test_handles_perfectly_correlated_features():
    x_base = np.array([[1.0], [2.0], [3.0], [4.0], [5.0]])
    x = np.hstack([x_base, 2.0 * x_base])  # second feature is an exact multiple of the first
    y = np.array([2.0, 4.0, 6.0, 8.0, 10.0])
    predictions = ridge_regression_predict(x, y, 1.0, np.array([[6.0, 12.0]]))
    assert np.all(np.isfinite(predictions))


def test_predict_returns_one_value_per_query():
    rng = np.random.default_rng(3)
    x = rng.normal(size=(30, 4))
    y = rng.normal(size=30)
    queries = rng.normal(size=(7, 4))
    predictions = ridge_regression_predict(x, y, 0.5, queries)
    assert predictions.shape == (7,)
