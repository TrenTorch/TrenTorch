"""
pytest data/app_data/01-classical-ml/01-linear-regression/08-l1-loss-mae/tests.py
"""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-classical-ml/01-linear-regression/{Path(__file__).resolve().parent.name}")
l1_loss = _module.l1_loss


def test_l1_loss_zero_when_input_equals_target():
    x = np.array([1.0, 2.0, 3.0])
    assert np.isclose(l1_loss(x, x), 0.0)


def test_l1_loss_mean_matches_hand_computation():
    input_ = np.array([1.0, 2.0, 3.0, 4.0])
    target = np.array([1.5, 1.5, 3.5, 3.0])
    # abs errors: 0.5, 0.5, 0.5, 1.0 -> mean = 2.5/4 = 0.625
    assert np.isclose(l1_loss(input_, target, "mean"), 0.625)


def test_l1_loss_sum_is_n_times_mean():
    input_ = np.array([1.0, 2.0, 3.0, 4.0])
    target = np.array([1.5, 1.5, 3.5, 3.0])
    mean_loss = l1_loss(input_, target, "mean")
    sum_loss = l1_loss(input_, target, "sum")
    assert np.isclose(sum_loss, mean_loss * input_.size)


def test_l1_loss_none_returns_elementwise_absolute_errors():
    input_ = np.array([1.0, 5.0])
    target = np.array([4.0, 1.0])
    result = l1_loss(input_, target, "none")
    assert np.allclose(result, [3.0, 4.0])


def test_l1_loss_raises_on_invalid_reduction():
    x = np.array([1.0, 2.0])
    with pytest.raises(ValueError):
        l1_loss(x, x, reduction="invalid")


def test_l1_loss_is_less_sensitive_to_outliers_than_squared_error_would_be():
    # The core contrast this question exists to demonstrate: an outlier
    # of magnitude 10 contributes 10 to L1 loss (before averaging), not
    # 100 the way it would to a squared-error loss.
    input_ = np.array([0.0])
    target = np.array([10.0])
    result = l1_loss(input_, target, "sum")
    assert np.isclose(result, 10.0)
    assert result != 100.0  # would be 100 if squared like MSE


def test_l1_loss_treats_positive_and_negative_errors_symmetrically():
    over = l1_loss(np.array([5.0]), np.array([3.0]), "none")
    under = l1_loss(np.array([3.0]), np.array([5.0]), "none")
    assert np.isclose(over[0], under[0])


def test_l1_loss_does_not_square_the_error():
    # Directly targets a mutant that copies MSE's squared-error formula
    # instead of using absolute value. At error=3, absolute gives 3,
    # squared gives 9, clearly different.
    input_ = np.array([0.0])
    target = np.array([3.0])
    result = l1_loss(input_, target, "none")[0]
    assert np.isclose(result, 3.0)
    assert not np.isclose(result, 9.0)
