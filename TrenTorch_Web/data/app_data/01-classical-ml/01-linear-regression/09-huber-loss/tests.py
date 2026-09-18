"""
pytest data/app_data/01-classical-ml/01-linear-regression/09-huber-loss/tests.py
"""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-classical-ml/01-linear-regression/{Path(__file__).resolve().parent.name}")
huber_loss = _module.huber_loss


def test_huber_loss_zero_when_input_equals_target():
    x = np.array([1.0, 2.0, 3.0])
    assert np.isclose(huber_loss(x, x), 0.0)


def test_huber_loss_matches_known_oracle_values():
    # generated once, offline, via torch.nn.functional.huber_loss
    input_ = np.array([0.0, 0.5, 1.0, 2.0, 5.0])
    target = np.array([0.0, 0.0, 0.0, 0.0, 0.0])
    expected = np.array([0.0, 0.125, 0.5, 1.5, 4.5])
    assert np.allclose(huber_loss(input_, target, delta=1.0, reduction="none"), expected)


def test_huber_loss_quadratic_branch_matches_mse_for_small_errors():
    # Within the quadratic region, huber == 0.5 * squared_error.
    input_ = np.array([0.3])
    target = np.array([0.0])
    result = huber_loss(input_, target, delta=1.0, reduction="none")[0]
    assert np.isclose(result, 0.5 * 0.3**2)


def test_huber_loss_linear_branch_grows_linearly_for_large_errors():
    # Beyond delta, doubling the error should roughly double the
    # incremental loss added (linear growth), not quadruple it (which
    # squared error would do).
    target = np.array([0.0])
    delta = 1.0
    loss_at_5 = huber_loss(np.array([5.0]), target, delta=delta, reduction="none")[0]
    loss_at_10 = huber_loss(np.array([10.0]), target, delta=delta, reduction="none")[0]
    # linear region: loss(x) = delta*(x - 0.5*delta), so loss(10)-loss(5) = delta*5
    assert np.isclose(loss_at_10 - loss_at_5, delta * 5.0)


def test_huber_loss_is_continuous_at_the_delta_boundary():
    # The two branches must agree exactly at |error| == delta, no jump.
    target = np.array([0.0])
    delta = 2.0
    just_at_delta = huber_loss(np.array([delta]), target, delta=delta, reduction="none")[0]
    expected = 0.5 * delta**2
    assert np.isclose(just_at_delta, expected)


def test_huber_loss_smaller_delta_switches_to_linear_sooner():
    input_ = np.array([3.0])
    target = np.array([0.0])
    small_delta_loss = huber_loss(input_, target, delta=0.5, reduction="none")[0]
    large_delta_loss = huber_loss(input_, target, delta=5.0, reduction="none")[0]
    # error=3 is beyond delta=0.5 (linear) but within delta=5.0 (quadratic)
    assert np.isclose(small_delta_loss, 0.5 * (3.0 - 0.25))  # delta*(|e|-0.5*delta)
    assert np.isclose(large_delta_loss, 0.5 * 3.0**2)  # 0.5*e^2


def test_huber_loss_mean_matches_sum_divided_by_n():
    input_ = np.array([0.3, 5.0, -2.0])
    target = np.array([0.0, 0.0, 0.0])
    mean_loss = huber_loss(input_, target, reduction="mean")
    sum_loss = huber_loss(input_, target, reduction="sum")
    assert np.isclose(sum_loss, mean_loss * 3)


def test_huber_loss_raises_on_invalid_reduction():
    x = np.array([1.0])
    with pytest.raises(ValueError):
        huber_loss(x, x, reduction="bogus")


def test_huber_loss_does_not_apply_quadratic_formula_beyond_delta():
    # Directly targets a mutant that always uses the quadratic branch
    # regardless of the delta threshold (i.e. reduces to plain squared
    # error everywhere). At error=5, delta=1: correct Huber gives 4.5,
    # a squared-error mutant would give 12.5.
    input_ = np.array([5.0])
    target = np.array([0.0])
    result = huber_loss(input_, target, delta=1.0, reduction="none")[0]
    assert np.isclose(result, 4.5)
    assert not np.isclose(result, 12.5)
