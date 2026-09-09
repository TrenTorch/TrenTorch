"""
pytest data/classical-ml/linear-regression/02-mse-loss/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _load import load_solution  # noqa: E402

mse_loss = load_solution(Path(__file__).resolve().parent.name).mse_loss


def test_zero_loss_when_predictions_are_exact():
    y = np.array([1.0, 2.0, 3.0])
    assert mse_loss(y, y) == 0.0


def test_matches_hand_computed_value():
    # errors are [1, -1] -> squared [1, 1] -> mean 1.0
    assert np.isclose(mse_loss(np.array([2.0, 1.0]), np.array([1.0, 2.0])), 1.0)


def test_returns_plain_python_float_not_array():
    # A real, common bug: returning np.float64 or a 0-d array, which
    # silently breaks any code downstream expecting isinstance(x, float).
    result = mse_loss(np.array([1.0, 2.0]), np.array([1.5, 2.5]))
    assert isinstance(result, float)


def test_symmetric_to_sign_of_error():
    # Being 2 too high and 2 too low must cost exactly the same --
    # verifies squaring is actually happening, not e.g. abs() (which
    # would "pass" this specific case but is a different loss entirely).
    y = np.array([3.0])
    assert np.isclose(mse_loss(np.array([5.0]), y), mse_loss(np.array([1.0]), y))


def test_large_error_penalized_more_than_proportionally():
    # MSE grows quadratically, not linearly. Doubling the error must
    # more than double the loss -- the entire reason MSE beats MAE here.
    y = np.array([0.0])
    small = mse_loss(np.array([1.0]), y)
    large = mse_loss(np.array([2.0]), y)
    assert large > 2 * small


def test_single_sample_works():
    assert np.isclose(mse_loss(np.array([5.0]), np.array([3.0])), 4.0)
