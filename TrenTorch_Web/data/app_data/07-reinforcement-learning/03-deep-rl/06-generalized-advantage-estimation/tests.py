import numpy as np
from pathlib import Path

_module = __import__(Path(__file__).stem.replace("-", "_").replace("tests", "solution"))
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
    deltas = rewards + 0.99 * next_values - values
    assert np.allclose(gae, deltas)


def test_gae_lambda_1():
    """GAE with λ=1 sums all future residuals."""
    values = [1.0, 1.0, 1.0]
    rewards = [1.0, 1.0, 0.0]
    next_values = [1.0, 1.0, 0.0]

    gae = compute_gae(values, rewards, next_values, gamma=1.0, lambda_=1.0)

    # With γ=1, λ=1: should accumulate all returns
    assert gae[2] == 0.0  # Last residual
    assert gae[1] == 1.0  # Sum of last two
    assert gae[0] == 2.0  # Sum of all


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

    # Low λ = low advantage, high λ = high advantage
    assert gae_low < gae_high
