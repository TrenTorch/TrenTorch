"""
pytest data/app_data/03-dl-training/01-optimizers/02-sgd-momentum/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"03-dl-training/01-optimizers/{Path(__file__).resolve().parent.name}")
sgd_momentum_step = _module.sgd_momentum_step


def test_first_step_with_zero_velocity_matches_plain_sgd():
    params = [np.array([1.0, 2.0])]
    grads = [np.array([0.5, 1.0])]
    velocities = [np.array([0.0, 0.0])]
    new_params, new_velocities = sgd_momentum_step(params, grads, velocities, lr=0.1, momentum=0.9)
    assert np.allclose(new_params[0], [0.95, 1.9])
    assert np.allclose(new_velocities[0], [0.5, 1.0])


def test_velocity_update_matches_hand_computation():
    velocities = [np.array([2.0])]
    grads = [np.array([1.0])]
    params = [np.array([0.0])]
    _, new_velocities = sgd_momentum_step(params, grads, velocities, lr=0.1, momentum=0.9)
    # 0.9*2.0 + 1.0 = 2.8
    assert np.isclose(new_velocities[0][0], 2.8)


def test_matches_known_oracle_across_multiple_steps_from_pytorch():
    # generated once, offline, via torch.optim.SGD(momentum=0.9)
    params = [np.array([1.0, 2.0])]
    velocities = [np.array([0.0, 0.0])]
    expected_after_each_step = [
        [0.8, 1.6],
        [0.46, 0.92],
        [0.062, 0.124],
    ]
    for expected in expected_after_each_step:
        grads = [2.0 * params[0]]
        params, velocities = sgd_momentum_step(params, grads, velocities, lr=0.1, momentum=0.9)
        assert np.allclose(params[0], expected, atol=1e-6)


def test_zero_momentum_reduces_to_plain_sgd():
    params = [np.array([3.0])]
    grads = [np.array([1.0])]
    velocities = [np.array([5.0])]  # nonzero prior velocity, should be ignored
    new_params, new_velocities = sgd_momentum_step(params, grads, velocities, lr=0.1, momentum=0.0)
    assert np.allclose(new_velocities[0], [1.0])  # 0*5 + 1 = 1
    assert np.allclose(new_params[0], [2.9])  # 3.0 - 0.1*1.0


def test_momentum_accelerates_movement_in_a_consistent_gradient_direction():
    # Consecutive same-sign gradients should make momentum move FARTHER
    # per step than plain SGD (lr alone) would.
    params = [np.array([0.0])]
    velocities = [np.array([0.0])]
    grads = [np.array([1.0])]
    distances = []
    for _ in range(3):
        prev = params[0][0]
        params, velocities = sgd_momentum_step(params, grads, velocities, lr=0.1, momentum=0.9)
        distances.append(abs(params[0][0] - prev))
    assert distances[2] > distances[0]  # movement per step grows


def test_sgd_momentum_step_does_not_use_raw_gradient_for_the_param_update():
    # Directly targets a mutant that steps using the raw gradient
    # instead of the blended velocity (i.e. ignoring momentum for the
    # param update itself, even though it still updates the velocity).
    params = [np.array([0.0])]
    grads = [np.array([1.0])]
    velocities = [np.array([10.0])]  # large prior velocity
    new_params, new_velocities = sgd_momentum_step(params, grads, velocities, lr=1.0, momentum=0.9)
    # new_velocity = 0.9*10 + 1 = 10.0, so new_param = 0 - 1.0*10.0 = -10.0
    assert np.isclose(new_params[0][0], -10.0)
    assert not np.isclose(new_params[0][0], -1.0)  # what a raw-gradient-only step would give
