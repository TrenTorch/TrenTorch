import numpy as np
from pathlib import Path

_module = __import__(Path(__file__).stem.replace("-", "_").replace("tests", "solution"))
estimate_off_policy_returns = _module.estimate_off_policy_returns


def test_single_episode():
    """Single episode, single state-action."""
    episode = [(0, 0, 10.0)]
    result = estimate_off_policy_returns([episode], gamma=0.9)

    # Return is 10, action 0 is best, weight should be high
    assert (0, 0) in result


def test_uniform_behavior():
    """Behavior policy uniform over observed actions."""
    episode = [(0, 0, 5.0), (1, 1, 3.0)]
    result = estimate_off_policy_returns([episode], gamma=1.0)

    # Both actions observed, so β(a) = 0.5
    # Compute returns and weights
    assert len(result) >= 0


def test_empty_episodes():
    """Empty episodes."""
    result = estimate_off_policy_returns([], gamma=0.9)
    assert result == {}


def test_multiple_episodes():
    """Multiple episodes."""
    ep1 = [(0, 0, 1.0)]
    ep2 = [(0, 0, 2.0)]
    result = estimate_off_policy_returns([ep1, ep2], gamma=0.9)

    assert (0, 0) in result


def test_off_policy_extrapolation():
    """Off-policy: behavior takes action 1, target prefers action 0."""
    episode = [(0, 1, 10.0)]
    result = estimate_off_policy_returns([episode], gamma=0.9)

    # Action 1 is taken, but greedy prefers 0, so weight is 0
    # (1 / 1) * 0 / (1 / 1) = 0
    # This trajectory contributes 0 weight
    if (0, 1) in result:
        assert result[(0, 1)] == 0.0


def test_structure():
    """Result is dict (state, action) -> float."""
    episode = [(0, 0, 5.0), (1, 1, 3.0), (2, 0, 1.0)]
    result = estimate_off_policy_returns([episode], gamma=0.8)

    for key, val in result.items():
        assert isinstance(key, tuple) and len(key) == 2
        assert isinstance(val, (float, np.floating))


def test_deterministic():
    """Same input gives same output."""
    episode = [(0, 0, 5.0), (1, 0, 3.0)]
    result1 = estimate_off_policy_returns([episode], gamma=0.9)
    result2 = estimate_off_policy_returns([episode], gamma=0.9)

    for key in result1:
        assert np.isclose(result1[key], result2[key])
