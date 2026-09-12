"""
pytest data/app_data/01-classical-ml/07-evaluation/09-validation-curves/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

validation_curve = load_solution(
    f"01-classical-ml/07-evaluation/{Path(__file__).resolve().parent.name}"
).validation_curve
fit_polynomial = load_solution(
    "01-classical-ml/07-evaluation/03-bias-variance-tradeoff"
).fit_polynomial
predict_polynomial = load_solution(
    "01-classical-ml/07-evaluation/03-bias-variance-tradeoff"
).predict_polynomial


def test_returns_one_pair_per_param_value():
    def fit_and_evaluate(p):
        return float(p), float(p) * 2

    train_errors, val_errors = validation_curve(fit_and_evaluate, [1, 2, 3, 4])
    assert train_errors.shape == (4,)
    assert val_errors.shape == (4,)


def test_preserves_the_given_order():
    def fit_and_evaluate(p):
        return float(p), float(p)

    train_errors, _ = validation_curve(fit_and_evaluate, [9, 1, 5])
    assert list(train_errors) == [9.0, 1.0, 5.0]


def test_train_and_val_errors_are_not_swapped():
    def fit_and_evaluate(p):
        return float(p), -float(p)

    train_errors, val_errors = validation_curve(fit_and_evaluate, [1, 2, 3])
    assert list(train_errors) == [1.0, 2.0, 3.0]
    assert list(val_errors) == [-1.0, -2.0, -3.0]


def test_calls_fit_and_evaluate_once_per_param_value():
    call_log = []

    def fit_and_evaluate(p):
        call_log.append(p)
        return 0.0, 0.0

    validation_curve(fit_and_evaluate, [0.1, 0.5, 1.0])
    assert call_log == [0.1, 0.5, 1.0]


def test_shows_the_classic_u_shape_against_polynomial_degree():
    # The actual point of the exercise: sweeping polynomial degree on a
    # small, fixed, noisy training set should show training error
    # decreasing roughly monotonically, while validation error dips to
    # a minimum in the middle and then rises again at high degree
    # (overfitting).
    rng = np.random.default_rng(0)
    x_train = rng.uniform(-3, 3, 25)
    y_train = np.sin(x_train) + rng.normal(scale=0.2, size=25)
    x_val = rng.uniform(-3, 3, 50)
    y_val = np.sin(x_val)

    def fit_and_evaluate(degree):
        coefficients = fit_polynomial(x_train, y_train, degree)
        train_error = float(np.mean((predict_polynomial(coefficients, x_train) - y_train) ** 2))
        val_error = float(np.mean((predict_polynomial(coefficients, x_val) - y_val) ** 2))
        return train_error, val_error

    degrees = [1, 3, 5, 9, 12]
    train_errors, val_errors = validation_curve(fit_and_evaluate, degrees)

    assert train_errors[0] > train_errors[-1]  # training error trends down overall
    best_idx = int(np.argmin(val_errors))
    assert 0 < best_idx < len(degrees) - 1  # the minimum is NOT at either extreme
    assert val_errors[-1] > val_errors[best_idx]  # overfitting climbs back up at high degree
