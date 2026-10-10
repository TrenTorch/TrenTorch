import pytest
import numpy as np
from pathlib import Path

from _load import load_solution

_module = load_solution(__file__)
compute_gae = _module.compute_gae


def test_basic_gae():
    """Basic GAE computation."""
    values = [1.0, 2.0, 1.0]
    rewards = [1.0, 0.0, 0.0]
    next_values = [2.0, 1.0, 0.0]

    gae = compute_gae(values, rewards, next_values)

    assert gae.shape == (3,)
    assert np.all(np.isfinite(gae))


def test_gae_lambda_0():
    """GAE with λ=0 equals TD residuals."""
    values = [1.0, 2.0]
    rewards = [1.0, 0.0]
    next_values = [2.0, 0.0]

    gae = compute_gae(values, rewards, next_values, gamma=0.99, lambda_=0.0)

    # Should match TD residuals
    deltas = np.array(rewards) + 0.99 * np.array(next_values) - np.array(values)
    np.testing.assert_allclose(gae, deltas)  # [2.98, -2.0]


def test_gae_lambda_1():
    """GAE with λ=1 sums all future residuals."""
    values = [1.0, 1.0, 1.0]
    rewards = [1.0, 1.0, 0.0]
    next_values = [1.0, 1.0, 0.0]

    gae = compute_gae(values, rewards, next_values, gamma=1.0, lambda_=1.0)

    # deltas = [1, 1, -1]; with gamma=1, lambda=1 each advantage is the sum of later deltas
    np.testing.assert_allclose(gae, [1.0, 0.0, -1.0])


def test_gae_shape():
    """GAE output shape matches input."""
    T = 10
    values = np.ones(T)
    rewards = np.ones(T)
    next_values = np.ones(T)

    gae = compute_gae(values, rewards, next_values)

    assert gae.shape == (T,)


def test_gae_convergence():
    """GAE converges with different λ."""
    values = [1.0, 1.0]
    rewards = [10.0, 0.0]
    next_values = [0.0, 0.0]

    gae_low = compute_gae(values, rewards, next_values, lambda_=0.0)[0]
    gae_high = compute_gae(values, rewards, next_values, lambda_=1.0)[0]

    # deltas = [9, -1]; lambda=0 keeps 9.0, lambda=1 adds gamma*(-1) = 8.01
    assert gae_low == pytest.approx(9.0)
    assert gae_high == pytest.approx(8.01)
