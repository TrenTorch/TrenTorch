"""
pytest data/app_data/01-classical-ml/07-evaluation/08-learning-curves/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

learning_curve = load_solution(
    f"01-classical-ml/07-evaluation/{Path(__file__).resolve().parent.name}"
).learning_curve
fit_polynomial = load_solution(
    "01-classical-ml/07-evaluation/03-bias-variance-tradeoff"
).fit_polynomial
predict_polynomial = load_solution(
    "01-classical-ml/07-evaluation/03-bias-variance-tradeoff"
).predict_polynomial


def test_returns_one_pair_per_train_size():
    def fit_and_evaluate(n):
        return float(n), float(n) * 2

    train_errors, val_errors = learning_curve(fit_and_evaluate, [10, 20, 30])
    assert train_errors.shape == (3,)
    assert val_errors.shape == (3,)


def test_preserves_the_given_order_not_sorted():
    def fit_and_evaluate(n):
        return float(n), float(n)

    train_errors, _ = learning_curve(fit_and_evaluate, [50, 10, 30])
    assert list(train_errors) == [50.0, 10.0, 30.0]


def test_train_and_val_errors_are_not_swapped():
    def fit_and_evaluate(n):
        return float(n), -float(n)  # asymmetric, easy to catch a swap

    train_errors, val_errors = learning_curve(fit_and_evaluate, [1, 2, 3])
    assert list(train_errors) == [1.0, 2.0, 3.0]
    assert list(val_errors) == [-1.0, -2.0, -3.0]


def test_calls_fit_and_evaluate_exactly_once_per_size():
    call_log = []

    def fit_and_evaluate(n):
        call_log.append(n)
        return 0.0, 0.0

    learning_curve(fit_and_evaluate, [5, 15, 25, 35])
    assert call_log == [5, 15, 25, 35]


def test_underfit_model_shows_both_errors_plateau_at_a_similarly_high_value():
    rng = np.random.default_rng(0)
    x_all = rng.uniform(-3, 3, 200)
    y_all = np.sin(x_all) + rng.normal(scale=0.2, size=200)
    x_val = rng.uniform(-3, 3, 50)
    y_val = np.sin(x_val)

    def fit_and_evaluate(n):
        x, y = x_all[:n], y_all[:n]
        coefficients = fit_polynomial(x, y, degree=0)  # a constant -- can't fit sin(x) at all
        train_error = float(np.mean((predict_polynomial(coefficients, x) - y) ** 2))
        val_error = float(np.mean((predict_polynomial(coefficients, x_val) - y_val) ** 2))
        return train_error, val_error

    train_errors, val_errors = learning_curve(fit_and_evaluate, [10, 50, 100, 150])
    # more data does not meaningfully close the gap for a model this
    # simple -- both stay in the same high, similar range throughout
    assert np.all(train_errors > 0.3)
    assert np.all(val_errors > 0.3)
    assert abs(val_errors[-1] - val_errors[0]) < 0.2


def test_well_specified_model_shows_validation_error_converging_toward_training_error():
    rng = np.random.default_rng(0)
    x_all = rng.uniform(-3, 3, 200)
    y_all = np.sin(x_all) + rng.normal(scale=0.2, size=200)
    x_val = rng.uniform(-3, 3, 50)
    y_val = np.sin(x_val)

    def fit_and_evaluate(n):
        x, y = x_all[:n], y_all[:n]
        coefficients = fit_polynomial(x, y, degree=3)  # a much better fit for sin(x)
        train_error = float(np.mean((predict_polynomial(coefficients, x) - y) ** 2))
        val_error = float(np.mean((predict_polynomial(coefficients, x_val) - y_val) ** 2))
        return train_error, val_error

    train_errors, val_errors = learning_curve(fit_and_evaluate, [10, 50, 100, 150])
    # validation error should drop substantially as training size grows,
    # and end up close to (not wildly above) the training error
    assert val_errors[0] > val_errors[-1]
    assert abs(val_errors[-1] - train_errors[-1]) < 0.05
