"""
pytest data/app_data/01-classical-ml/07-evaluation/03-bias-variance-tradeoff/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-classical-ml/07-evaluation/{Path(__file__).resolve().parent.name}")
polynomial_features = _module.polynomial_features
fit_polynomial = _module.fit_polynomial
predict_polynomial = _module.predict_polynomial
bias_variance_decomposition = _module.bias_variance_decomposition


def test_polynomial_features_matches_hand_computation():
    x = np.array([2.0, 3.0])
    result = polynomial_features(x, degree=2)
    assert np.allclose(result, [[1.0, 2.0, 4.0], [1.0, 3.0, 9.0]])


def test_fit_polynomial_recovers_exact_coefficients_on_noiseless_data():
    x = np.linspace(-2, 2, 10)
    y = 3.0 + 2.0 * x - 1.0 * x**2  # true coefficients [3, 2, -1]
    coefficients = fit_polynomial(x, y, degree=2)
    assert np.allclose(coefficients, [3.0, 2.0, -1.0], atol=1e-8)


def test_predict_polynomial_matches_fit_on_training_points():
    x = np.array([0.0, 1.0, 2.0, 3.0])
    y = x**2
    coefficients = fit_polynomial(x, y, degree=2)
    predictions = predict_polynomial(coefficients, x)
    assert np.allclose(predictions, y, atol=1e-8)


def test_bias_variance_decomposition_matches_hand_computation():
    # 3 "models" predicting the same 2 test points.
    predictions = np.array([[1.0, 5.0], [3.0, 5.0], [2.0, 5.0]])
    targets = np.array([2.0, 5.0])
    # mean_prediction = [2.0, 5.0] -- matches targets exactly -> bias^2 = 0
    # variance of column 0: values [1,3,2], mean 2, var = ((1)^2+(1)^2+0)/3 = 2/3
    # variance of column 1: values [5,5,5], var = 0
    # mean variance = (2/3 + 0)/2 = 1/3
    bias_squared, variance, total = bias_variance_decomposition(predictions, targets)
    assert np.isclose(bias_squared, 0.0)
    assert np.isclose(variance, 1.0 / 3.0)
    assert np.isclose(total, bias_squared + variance)


def test_bias_variance_decomposition_nonzero_bias():
    predictions = np.array([[0.0], [0.0], [0.0]])  # all models always predict 0
    targets = np.array([4.0])
    bias_squared, variance, _ = bias_variance_decomposition(predictions, targets)
    assert np.isclose(bias_squared, 16.0)  # (0-4)^2
    assert np.isclose(variance, 0.0)  # every model agrees (with each other)


def test_underfitting_shows_high_bias_relative_to_a_better_fit():
    # A degree-1 (linear) fit to sin(x) can never represent the curve,
    # regardless of training data -- high, unavoidable bias. A degree-3
    # fit captures the shape much better, with comparably small variance.
    x_test = np.linspace(-3, 3, 30)
    y_true_test = np.sin(x_test)

    def train_set(seed):
        rng = np.random.default_rng(seed)
        x = rng.uniform(-3, 3, 20)
        y = np.sin(x) + rng.normal(scale=0.2, size=20)
        return x, y

    def run(degree):
        predictions = []
        for i in range(30):
            x, y = train_set(i)
            coefficients = fit_polynomial(x, y, degree)
            predictions.append(predict_polynomial(coefficients, x_test))
        return bias_variance_decomposition(np.array(predictions), y_true_test)

    bias_sq_linear, _, _ = run(1)
    bias_sq_cubic, _, _ = run(3)

    assert bias_sq_linear > bias_sq_cubic  # linear can't capture the curve at all


def test_overfitting_shows_high_variance_relative_to_underfitting():
    # A high-degree polynomial fit to only 20 noisy points can wiggle
    # through the specific noise in each training sample -- wildly
    # different fitted curves from one resample to the next, hence much
    # higher variance than the stable (if biased) linear fit.
    x_test = np.linspace(-3, 3, 30)
    y_true_test = np.sin(x_test)

    def train_set(seed):
        rng = np.random.default_rng(seed)
        x = rng.uniform(-3, 3, 20)
        y = np.sin(x) + rng.normal(scale=0.2, size=20)
        return x, y

    def run(degree):
        predictions = []
        for i in range(30):
            x, y = train_set(i)
            coefficients = fit_polynomial(x, y, degree)
            predictions.append(predict_polynomial(coefficients, x_test))
        return bias_variance_decomposition(np.array(predictions), y_true_test)

    _, variance_linear, _ = run(1)
    _, variance_overfit, _ = run(9)

    assert variance_overfit > 100 * variance_linear


def test_variance_is_computed_across_models_not_across_test_points():
    # Directly targets a mutant that computes variance along the wrong
    # axis (across test points instead of across models): with models
    # that vary a lot from each other but whose predictions are
    # constant across test points, axis=0 variance (correct) is large,
    # axis=1 variance (wrong axis) would be exactly 0 for every model.
    predictions = np.array([[1.0, 1.0, 1.0], [5.0, 5.0, 5.0], [9.0, 9.0, 9.0]])
    targets = np.array([5.0, 5.0, 5.0])
    _, variance, _ = bias_variance_decomposition(predictions, targets)
    assert variance > 1.0
