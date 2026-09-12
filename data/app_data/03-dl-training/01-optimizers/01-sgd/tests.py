"""
pytest data/app_data/03-dl-training/01-optimizers/01-sgd/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"03-dl-training/01-optimizers/{Path(__file__).resolve().parent.name}")
sgd_step = _module.sgd_step


def test_sgd_step_matches_hand_computation():
    params = [np.array([1.0, 2.0])]
    grads = [np.array([0.5, 1.0])]
    result = sgd_step(params, grads, lr=0.1)
    assert np.allclose(result[0], [0.95, 1.9])


def test_sgd_step_matches_known_oracle_from_pytorch():
    # generated once, offline, via torch.optim.SGD
    w = np.array([1.0, 2.0])
    grad = 2 * w  # d(w^2)/dw
    result = sgd_step([w], [grad], lr=0.1)
    assert np.allclose(result[0], [0.8, 1.6])


def test_sgd_step_handles_multiple_parameters_independently():
    params = [np.array([1.0]), np.array([10.0, 20.0])]
    grads = [np.array([2.0]), np.array([1.0, 1.0])]
    result = sgd_step(params, grads, lr=0.5)
    assert np.allclose(result[0], [0.0])
    assert np.allclose(result[1], [9.5, 19.5])


def test_sgd_step_does_not_mutate_input_arrays():
    params = [np.array([1.0, 2.0])]
    grads = [np.array([0.5, 1.0])]
    params_copy = [p.copy() for p in params]
    sgd_step(params, grads, lr=0.1)
    assert np.array_equal(params[0], params_copy[0])


def test_sgd_step_with_zero_learning_rate_leaves_params_unchanged():
    params = [np.array([3.0, 4.0])]
    grads = [np.array([100.0, -50.0])]
    result = sgd_step(params, grads, lr=0.0)
    assert np.allclose(result[0], params[0])


def test_sgd_step_moves_opposite_the_gradient_direction():
    params = [np.array([0.0])]
    grads = [np.array([1.0])]  # positive gradient
    result = sgd_step(params, grads, lr=0.1)
    assert result[0][0] < 0.0  # should move DOWN, opposite the gradient


def test_sgd_step_does_not_add_the_gradient_instead_of_subtracting():
    # Directly targets a mutant that adds lr*grad instead of subtracting
    # it, which would move parameters UP the gradient (toward higher
    # loss) instead of down.
    params = [np.array([5.0])]
    grads = [np.array([1.0])]
    result = sgd_step(params, grads, lr=1.0)
    assert np.isclose(result[0][0], 4.0)
    assert not np.isclose(result[0][0], 6.0)
