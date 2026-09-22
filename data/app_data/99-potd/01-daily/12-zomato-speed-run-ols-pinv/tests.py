"""
pytest data/app_data/99-potd/01-daily/12-zomato-speed-run-ols-pinv/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"99-potd/01-daily/{Path(__file__).resolve().parent.name}")
ols_fit_predict = _module.ols_fit_predict


def test_example_recovers_an_exact_linear_fit():
    X = np.array([[1.0], [2.0], [3.0]])
    y = np.array([5.0, 7.0, 9.0])
    Q = np.array([[4.0], [5.0]])
    w, predictions = ols_fit_predict(X, y, Q)
    np.testing.assert_allclose(w, [3.0, 2.0], atol=1e-6)
    np.testing.assert_allclose(predictions, [11.0, 13.0], atol=1e-6)


def test_perfect_collinearity_does_not_crash_and_predicts_correctly():
    rng = np.random.default_rng(1)
    x1 = rng.uniform(0, 10, size=20)
    X = np.column_stack([x1, 2.0 * x1])  # second column is an exact multiple of the first
    true_w = np.array([1.5, 3.0])  # any split between the two collinear columns fits equally well
    y = 1.0 + X @ true_w
    Q = np.array([[5.0, 10.0], [0.0, 0.0]])
    w, predictions = ols_fit_predict(X, y, Q)
    assert np.isfinite(w).all()
    expected_predictions = 1.0 + Q @ true_w
    np.testing.assert_allclose(predictions, expected_predictions, atol=1e-3)


def test_underdetermined_system_matches_predictions_not_weights():
    # n=1, d=1: infinitely many exact-fit lines through the origin and one
    # point. Only the prediction at the same x is pinned down.
    X = np.array([[2.0]])
    y = np.array([10.0])
    Q = np.array([[2.0]])
    w, predictions = ols_fit_predict(X, y, Q)
    np.testing.assert_allclose(predictions, [10.0], atol=1e-4)


def test_wildly_different_feature_scales_still_fit_well():
    rng = np.random.default_rng(2)
    n = 200
    distance_m = rng.uniform(100, 20000, size=n)  # meters
    flag = rng.integers(0, 2, size=n).astype(float)  # 0/1
    X = np.column_stack([distance_m, flag])
    true_w = np.array([0.01, 5.0])
    noise = rng.normal(0, 0.1, size=n)
    y = 3.0 + X @ true_w + noise
    Q = np.array([[5000.0, 1.0], [1000.0, 0.0]])
    w, predictions = ols_fit_predict(X, y, Q)
    expected = 3.0 + Q @ true_w
    np.testing.assert_allclose(predictions, expected, atol=1.0)


def test_matches_a_numpy_lstsq_reference_on_well_posed_systems():
    rng = np.random.default_rng(3)
    for _ in range(10):
        n = rng.integers(10, 50)
        d = rng.integers(1, 5)
        X = rng.uniform(-10, 10, size=(n, d))
        true_w = rng.uniform(-5, 5, size=d + 1)
        X_aug = np.hstack([np.ones((n, 1)), X])
        y = X_aug @ true_w
        m = rng.integers(1, 5)
        Q = rng.uniform(-10, 10, size=(m, d))
        w, predictions = ols_fit_predict(X, y, Q)
        np.testing.assert_allclose(w, true_w, atol=1e-4)
        Q_aug = np.hstack([np.ones((m, 1)), Q])
        np.testing.assert_allclose(predictions, Q_aug @ true_w, atol=1e-4)
