"""
pytest data/app_data/03-dl-training/05-why-deep-networks-work/01-universal-approximation/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"03-dl-training/05-why-deep-networks-work/{Path(__file__).resolve().parent.name}")
sigmoid = _module.sigmoid
random_hidden_features = _module.random_hidden_features
fit_output_weights = _module.fit_output_weights
approximate_function = _module.approximate_function


def test_random_hidden_features_has_correct_shape():
    x = np.linspace(-1, 1, 20)
    rng = np.random.RandomState(0)
    hidden = random_hidden_features(x, num_hidden=7, rng=rng)
    assert hidden.shape == (20, 7)


def test_random_hidden_features_values_are_between_zero_and_one():
    x = np.linspace(-5, 5, 30)
    rng = np.random.RandomState(1)
    hidden = random_hidden_features(x, num_hidden=5, rng=rng)
    assert np.all(hidden >= 0.0)
    assert np.all(hidden <= 1.0)


def test_fit_output_weights_exactly_reconstructs_a_perfectly_fittable_target():
    hidden = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    true_weight = np.array([2.0, 3.0])
    y = hidden @ true_weight
    fitted = fit_output_weights(hidden, y)
    assert np.allclose(fitted, true_weight, atol=1e-8)


def test_approximate_function_returns_predictions_matching_y_shape():
    x = np.linspace(-2, 2, 50)
    y = np.sin(x)
    rng = np.random.RandomState(0)
    pred, mse = approximate_function(x, y, num_hidden=20, rng=rng)
    assert pred.shape == y.shape


def test_approximate_function_mse_is_nonnegative():
    x = np.linspace(-2, 2, 50)
    y = np.sin(x)
    rng = np.random.RandomState(0)
    _, mse = approximate_function(x, y, num_hidden=10, rng=rng)
    assert mse >= 0.0


def test_wider_hidden_layer_approximates_a_nonlinear_function_much_better():
    x = np.linspace(-3, 3, 200)
    y = np.sin(x)
    _, mse_narrow = approximate_function(x, y, num_hidden=3, rng=np.random.RandomState(0))
    _, mse_wide = approximate_function(x, y, num_hidden=50, rng=np.random.RandomState(0))
    assert mse_wide < mse_narrow / 10.0


def test_wide_enough_network_achieves_near_zero_error_on_sin():
    x = np.linspace(-3, 3, 200)
    y = np.sin(x)
    _, mse = approximate_function(x, y, num_hidden=50, rng=np.random.RandomState(0))
    assert mse < 1e-6


def test_approximating_a_perfectly_linear_target_also_works_with_few_hidden_units():
    x = np.linspace(-1, 1, 50)
    y = 2.0 * x + 1.0
    _, mse = approximate_function(x, y, num_hidden=20, rng=np.random.RandomState(0))
    assert mse < 1e-4


def test_fit_output_weights_uses_least_squares_not_the_raw_pseudoinverse_of_y():
    # Directly targets a mutant that solves the wrong linear system (e.g.
    # swapping the arguments to lstsq, solving hidden = y @ weight-shaped
    # nonsense instead of hidden @ weight = y): the correctly-fit weights
    # must satisfy hidden @ weight ≈ y closely for an overdetermined,
    # well-conditioned system.
    rng = np.random.RandomState(2)
    hidden = rng.randn(30, 4)
    true_weight = np.array([1.0, -2.0, 0.5, 3.0])
    y = hidden @ true_weight
    fitted = fit_output_weights(hidden, y)
    assert np.allclose(hidden @ fitted, y, atol=1e-6)
