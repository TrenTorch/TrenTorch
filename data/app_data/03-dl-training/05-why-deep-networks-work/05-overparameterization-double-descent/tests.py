"""
pytest data/app_data/03-dl-training/05-why-deep-networks-work/05-overparameterization-double-descent/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"03-dl-training/05-why-deep-networks-work/{Path(__file__).resolve().parent.name}")
build_features = _module.build_features
fit_min_norm = _module.fit_min_norm
train_and_test_mse = _module.train_and_test_mse


def _make_data():
    rng_data = np.random.RandomState(0)
    n_train = 20
    x_train = np.linspace(-3, 3, n_train)
    y_train = np.sin(x_train) + rng_data.randn(n_train) * 0.3
    x_test = np.linspace(-3, 3, 100)
    y_test = np.sin(x_test)
    return x_train, y_train, x_test, y_test


def test_build_features_returns_correct_shape():
    x = np.linspace(-1, 1, 10)
    weight = np.random.randn(5)
    bias = np.random.randn(5)
    hidden = build_features(x, weight, bias)
    assert hidden.shape == (10, 5)


def test_build_features_values_are_between_zero_and_one():
    x = np.linspace(-5, 5, 20)
    weight = np.random.randn(4)
    bias = np.random.randn(4)
    hidden = build_features(x, weight, bias)
    assert np.all(hidden >= 0.0)
    assert np.all(hidden <= 1.0)


def test_fit_min_norm_exactly_fits_an_overdetermined_consistent_system():
    hidden = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    true_weight = np.array([2.0, 3.0])
    y = hidden @ true_weight
    fitted = fit_min_norm(hidden, y)
    assert np.allclose(fitted, true_weight, atol=1e-8)


def test_fit_min_norm_returns_the_minimum_norm_solution_when_underdetermined():
    # A single equation, many solutions: hidden @ w = y with hidden shape (1, 3)
    hidden = np.array([[1.0, 1.0, 1.0]])
    y = np.array([3.0])
    fitted = fit_min_norm(hidden, y)
    # the minimum-norm solution to x+y+z=3 is [1,1,1] (equal spread)
    assert np.allclose(fitted, [1.0, 1.0, 1.0], atol=1e-6)


def test_train_mse_reaches_zero_once_num_features_matches_training_set_size():
    x_train, y_train, x_test, y_test = _make_data()
    rng = np.random.RandomState(1)
    train_mse, _ = train_and_test_mse(x_train, y_train, x_test, y_test, num_features=20, rng=rng)
    assert train_mse < 1e-6


def test_train_mse_reaches_zero_when_heavily_overparameterized():
    x_train, y_train, x_test, y_test = _make_data()
    rng = np.random.RandomState(1)
    train_mse, _ = train_and_test_mse(x_train, y_train, x_test, y_test, num_features=200, rng=rng)
    assert train_mse < 1e-6


def test_underparameterized_regime_has_nonzero_train_error_on_noisy_data():
    x_train, y_train, x_test, y_test = _make_data()
    rng = np.random.RandomState(1)
    train_mse, _ = train_and_test_mse(x_train, y_train, x_test, y_test, num_features=5, rng=rng)
    assert train_mse > 1e-3


def test_heavily_overparameterized_model_still_generalizes_reasonably():
    # The core "more parameters than data can still generalize" claim:
    # a model with 10x more features than training samples should still
    # achieve bounded, reasonable test error, not blow up.
    x_train, y_train, x_test, y_test = _make_data()
    rng = np.random.RandomState(1)
    _, test_mse = train_and_test_mse(x_train, y_train, x_test, y_test, num_features=200, rng=rng)
    assert test_mse < 1.0


def test_double_descent_test_error_falls_again_past_the_interpolation_threshold():
    # With this specific seeded setup, test error at the interpolation
    # threshold (num_features == n_train == 20) is measurably worse than
    # test error well past it (num_features == 200), the signature shape
    # of double descent.
    x_train, y_train, x_test, y_test = _make_data()
    _, mse_at_threshold = train_and_test_mse(
        x_train, y_train, x_test, y_test, num_features=20, rng=np.random.RandomState(1)
    )
    _, mse_overparameterized = train_and_test_mse(
        x_train, y_train, x_test, y_test, num_features=200, rng=np.random.RandomState(1)
    )
    assert mse_overparameterized < mse_at_threshold


def test_train_and_test_features_use_the_same_weight_and_bias_draw():
    # Directly targets a mutant that draws weight/bias TWICE (once for
    # train, once for test) instead of sharing a single draw: train and
    # test features would then live in unrelated random feature spaces,
    # and the fitted output_weight (learned in the TRAIN feature space)
    # would produce near-meaningless, high-error predictions on test
    # features, even for an easy, low-noise target.
    x_train = np.linspace(-1, 1, 30)
    y_train = x_train.copy()  # trivial, perfectly learnable linear target
    x_test = np.linspace(-1, 1, 30)
    y_test = x_test.copy()
    _, test_mse = train_and_test_mse(x_train, y_train, x_test, y_test, num_features=30, rng=np.random.RandomState(0))
    assert test_mse < 1e-4
